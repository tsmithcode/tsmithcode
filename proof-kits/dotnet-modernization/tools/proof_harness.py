#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate(row: dict[str, str]) -> Decimal:
    subtotal = Decimal(row["quantity"]) * Decimal(row["unit_price"])
    rate = {"gold": Decimal("0.10"), "silver": Decimal("0.05")}.get(row["tier"].lower(), Decimal("0"))
    discount = money(subtotal * rate)
    priority = Decimal("25") if row["priority"].lower() == "true" else Decimal("0")
    taxable = subtotal - discount + priority
    return money(taxable + money(taxable * Decimal("0.07")))


def reconcile() -> dict[str, object]:
    with (ROOT / "fixtures" / "legacy-orders.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    modern = json.loads((ROOT / "fixtures" / "modern-orders.json").read_text(encoding="utf-8"))
    unique: dict[str, Decimal] = {}
    duplicates: list[str] = []
    for row in rows:
        key = row["legacy_id"]
        total = calculate(row)
        if key in unique:
            duplicates.append(key)
        else:
            unique[key] = total
    modern_map = {item["legacyId"]: Decimal(str(item["total"])) for item in modern}
    mismatches = [key for key, total in unique.items() if modern_map.get(key) != total]
    receipt = {
        "legacyRows": len(rows),
        "uniqueOrders": len(unique),
        "duplicatesDetected": sorted(set(duplicates)),
        "legacyUniqueTotal": str(sum(unique.values(), Decimal("0.00"))),
        "modernTotal": str(sum(modern_map.values(), Decimal("0.00"))),
        "mismatches": mismatches,
        "status": "PASS" if not mismatches and len(unique) == len(modern_map) else "FAIL",
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "reconciliation-report.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if receipt["status"] != "PASS":
        raise RuntimeError(f"Migration reconciliation failed: {receipt}")
    return receipt


def request_json(method: str, url: str, body: dict[str, object] | None = None, headers: dict[str, str] | None = None):
    payload = None if body is None else json.dumps(body).encode("utf-8")
    merged = {"Content-Type": "application/json", **(headers or {})}
    request = urllib.request.Request(url, data=payload, headers=merged, method=method)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8")), dict(response.headers)
    except urllib.error.HTTPError as error:
        data = json.loads(error.read().decode("utf-8"))
        return error.code, data, dict(error.headers)


def smoke(base_url: str) -> dict[str, object]:
    deadline = time.time() + 30
    health: dict[str, object] | None = None
    health_status: int | None = None
    while time.time() < deadline:
        try:
            status, candidate, _ = request_json("GET", f"{base_url}/health")
            if status == 200 and candidate.get("status") == "healthy":
                health_status = status
                health = candidate
                break
        except Exception:  # noqa: BLE001 - startup polling must tolerate connection errors
            pass
        time.sleep(1)
    if health_status != 200 or health is None:
        raise RuntimeError("API did not become healthy within 30 seconds")

    command = {"customerId": "C-200", "quantity": 4, "unitPrice": 250, "customerTier": "Silver", "priority": False}
    headers = {"Idempotency-Key": "DEMO-ORDER-200", "X-Correlation-ID": "proof-correlation-200"}
    first_status, first, first_headers = request_json("POST", f"{base_url}/api/v1/orders", command, headers)
    second_status, second, _ = request_json("POST", f"{base_url}/api/v1/orders", command, headers)
    invalid_status, invalid, _ = request_json(
        "POST",
        f"{base_url}/api/v1/orders",
        {"customerId": "", "quantity": 0, "unitPrice": 0, "customerTier": "Standard", "priority": False},
        {"Idempotency-Key": "INVALID-ORDER"},
    )
    outbox_status, outbox, _ = request_json("GET", f"{base_url}/api/v1/outbox")

    normalized_headers = {key.lower(): value for key, value in first_headers.items()}
    checks = {
        "health": health.get("status") == "healthy",
        "created": first_status == 201,
        "duplicateReturnedOriginal": second_status == 200 and second.get("wasDuplicate") is True and first.get("orderId") == second.get("orderId"),
        "validationProblem": invalid_status == 422 and invalid.get("title") == "Order validation failed",
        "singleOutboxReceipt": outbox_status == 200 and len(outbox) == 1,
        "correlationEcho": normalized_headers.get("x-correlation-id") == "proof-correlation-200",
    }
    receipt = {
        "baseUrl": base_url,
        "checks": checks,
        "firstOrder": first,
        "duplicateOrder": second,
        "invalidProblem": invalid,
        "outbox": outbox,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "api-smoke-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if receipt["status"] != "PASS":
        raise RuntimeError(f"API smoke checks failed: {checks}")
    return receipt


def evidence() -> dict[str, object]:
    preflight = json.loads((REPORTS / "preflight-report.json").read_text(encoding="utf-8"))
    test = json.loads((REPORTS / "test-receipt.json").read_text(encoding="utf-8"))
    api = json.loads((REPORTS / "api-smoke-receipt.json").read_text(encoding="utf-8"))
    migration = json.loads((REPORTS / "reconciliation-report.json").read_text(encoding="utf-8"))
    architecture_text = (ROOT / "docs" / "architecture-and-decisions.md").read_text(encoding="utf-8").lower()
    api_source = (ROOT / "src" / "Modernization.Api" / "Program.cs").read_text(encoding="utf-8")
    gates = {
        "publicArtifactPreflight": preflight["status"] == "PASS",
        "characterizationAndParity": test["failed"] == 0,
        "apiContractAndReliability": api["status"] == "PASS",
        "migrationReconciliation": migration["status"] == "PASS",
        "rollbackAndObservabilityPlan": "rollback" in architecture_text and "/health" in api_source and "X-Correlation-ID" in api_source,
    }
    score = round(sum(1 for value in gates.values() if value) / len(gates) * 100)
    report = {
        "kit": "TSmithCode .NET Modernization Proof Kit",
        "generatedAtUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "readinessScore": score,
        "decision": "GO: fund a bounded first modernization slice" if score == 100 else "HOLD: resolve failed gates",
        "gates": gates,
        "evidence": {
            "preflight": "reports/preflight-report.json",
            "tests": "reports/test-receipt.json",
            "api": "reports/api-smoke-receipt.json",
            "migration": "reports/reconciliation-report.json",
            "openApi": "openapi.yaml",
            "architecture": "docs/architecture-and-decisions.md",
        },
        "limitations": [
            "Synthetic public system; no customer source, credentials, production data, or claimed client ROI.",
            "The legacy project is a cross-platform runnable surrogate for .NET Framework-era coupling, not a redistributed client application.",
            "The in-memory repository demonstrates transaction and idempotency boundaries; a paid diagnostic selects the production data store and deployment controls.",
        ],
    }
    (REPORTS / "modernization-readiness.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown = f"# Modernization readiness report\n\n**Score:** {score}/100  \n**Decision:** {report['decision']}\n\n## Gates\n\n"
    markdown += "\n".join(f"- {'PASS' if passed else 'FAIL'} — {name}" for name, passed in gates.items())
    markdown += "\n\n## First funded slice\n\nExtract order acceptance behind a versioned API, preserve characterized pricing behavior, require idempotency, persist an outbox receipt, add correlation-aware logs, and reconcile migrated order totals before expanding scope.\n"
    (REPORTS / "modernization-readiness.md").write_text(markdown, encoding="utf-8")
    executive = f"""# Executive decision brief

## Decision

{report['decision']}

## Why this slice

The proof preserves existing pricing behavior while eliminating duplicate processing, making validation explicit, creating an auditable integration receipt, and providing a deterministic migration reconciliation.

## Illustrative business case — not a customer claim

For a workflow handling 2,000 orders per month, preventing a 1% duplicate/rework rate removes 20 avoidable exception investigations monthly. At an illustrative 45 minutes each, that is 15 hours of operational effort, before counting financial correction, customer impact, or release-risk reduction. Replace these assumptions with measured client data during discovery.

## Evidence

- Public artifact preflight: {preflight['status']}
- Readiness score: {score}/100
- Tests passed: {test['passed']}/{test['total']}
- API smoke: {api['status']}
- Migration reconciliation: {migration['status']}
"""
    (REPORTS / "executive-decision-brief.md").write_text(executive, encoding="utf-8")
    risk = """# Risk register

| Risk | Current control | Paid diagnostic decision |
|---|---|---|
| Hidden legacy behavior | Characterization and parity tests | Expand test inventory against real source and production examples |
| Duplicate processing | Idempotency key and single outbox receipt | Select durable database constraint and replay policy |
| Integration failure | Versioned event and API contract | Confirm broker, retry, dead-letter, and ownership model |
| Migration drift | Deterministic count/total reconciliation | Add field-level and exception reconciliation |
| Operational blindness | Correlation ID, health endpoint, JSON logs | Define telemetry destination, alerts, and support owner |
| Big-bang rewrite | Bounded strangler slice | Approve sequencing, rollback, and parity exit criteria |
"""
    (REPORTS / "risk-register.md").write_text(risk, encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["reconcile", "smoke", "evidence"])
    parser.add_argument("--base-url", default="http://127.0.0.1:5078")
    args = parser.parse_args()
    if args.command == "reconcile":
        result = reconcile()
    elif args.command == "smoke":
        result = smoke(args.base_url)
    else:
        result = evidence()
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
