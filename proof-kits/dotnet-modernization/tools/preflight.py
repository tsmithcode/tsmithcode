#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

REQUIRED_FILES = [
    "README.md",
    ".gitignore",
    "Directory.Build.props",
    "global.json",
    "openapi.yaml",
    "run-proof.sh",
    "run-proof.ps1",
    "fixtures/legacy-orders.csv",
    "fixtures/modern-orders.json",
    "src/LegacyOrderEngine/LegacyOrderEngine.csproj",
    "src/LegacyOrderEngine/LegacyOrderProcessor.cs",
    "src/Modernization.Core/Modernization.Core.csproj",
    "src/Modernization.Core/Modernization.cs",
    "src/Modernization.Api/Modernization.Api.csproj",
    "src/Modernization.Api/Program.cs",
    "tests/Modernization.ProofTests/Modernization.ProofTests.csproj",
    "tests/Modernization.ProofTests/Program.cs",
    "tools/preflight.py",
    "tools/proof_harness.py",
    "docs/architecture-and-decisions.md",
    "docs/brand-and-engagement-routing.md",
    "docs/business-case.md",
    "docs/architecture-before.svg",
    "docs/architecture-after.svg",
    "media/flagship-social-card.svg",
    "media/three-minute-demo-script.md",
]

XML_FILES = [
    "Directory.Build.props",
    "src/LegacyOrderEngine/LegacyOrderEngine.csproj",
    "src/Modernization.Core/Modernization.Core.csproj",
    "src/Modernization.Api/Modernization.Api.csproj",
    "tests/Modernization.ProofTests/Modernization.ProofTests.csproj",
    "docs/architecture-before.svg",
    "docs/architecture-after.svg",
    "media/flagship-social-card.svg",
]

SOURCE_MARKERS = {
    "README.md": [
        "Brand and engagement routing",
        "This repository is a TSmithCode.ai artifact",
        "Related CAD and engineering automation lane",
    ],
    "docs/brand-and-engagement-routing.md": [
        "TSmithCode.ai",
        "CAD Guardian LLC",
        "not as interchangeable identities",
        "Evidence before claims",
        "Route it to CAD Guardian",
    ],
    "src/LegacyOrderEngine/LegacyOrderProcessor.cs": [
        "LegacyOrderProcessor",
        "CUSTOMER_REQUIRED",
        "INVALID_LINE",
    ],
    "src/Modernization.Core/Modernization.cs": [
        "IdempotencyKey",
        "OutboxMessage",
        "JsonSerializer.Serialize",
        "order.accepted.v1",
    ],
    "src/Modernization.Api/Program.cs": [
        'MapGet("/health"',
        'MapPost("/api/v1/orders"',
        "X-Correlation-ID",
        "Results.Problem",
    ],
    "tests/Modernization.ProofTests/Program.cs": [
        "LegacyCharacterization",
        "ModernParity",
        "IdempotencyBoundary",
        "ValidationBoundary",
        "OutboxReceipt",
    ],
    "openapi.yaml": [
        "openapi: 3.0.3",
        "/api/v1/orders:",
        "Idempotency-Key",
        "application/problem+json",
    ],
}


def check(name: str, condition: bool, detail: str) -> dict[str, object]:
    return {"name": name, "status": "PASS" if condition else "FAIL", "detail": detail}


def main() -> int:
    results: list[dict[str, object]] = []

    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    results.append(check("required-file-inventory", not missing, "missing=" + repr(missing)))

    xml_failures: list[str] = []
    for relative in XML_FILES:
        try:
            ET.parse(ROOT / relative)
        except Exception as exc:  # report exact malformed artifact
            xml_failures.append(f"{relative}: {exc}")
    results.append(check("xml-and-svg-well-formed", not xml_failures, "failures=" + repr(xml_failures)))

    try:
        global_config = json.loads((ROOT / "global.json").read_text(encoding="utf-8"))
        sdk_version = global_config["sdk"]["version"]
        roll_forward = global_config["sdk"]["rollForward"]
        global_ok = sdk_version.startswith("8.") and roll_forward == "latestFeature"
        global_detail = f"sdk={sdk_version}; rollForward={roll_forward}"
    except Exception as exc:
        global_ok = False
        global_detail = str(exc)
    results.append(check("dotnet-sdk-contract", global_ok, global_detail))

    try:
        modern = json.loads((ROOT / "fixtures" / "modern-orders.json").read_text(encoding="utf-8"))
        modern_ids = [row["legacyId"] for row in modern]
        fixture_json_ok = len(modern_ids) == len(set(modern_ids)) == 3
        fixture_json_detail = f"modernIds={modern_ids}"
    except Exception as exc:
        fixture_json_ok = False
        fixture_json_detail = str(exc)
    results.append(check("modern-fixture-json", fixture_json_ok, fixture_json_detail))

    try:
        with (ROOT / "fixtures" / "legacy-orders.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        headers = list(rows[0].keys()) if rows else []
        ids = [row["legacy_id"] for row in rows]
        duplicate_ids = sorted({value for value in ids if ids.count(value) > 1})
        csv_ok = headers == ["legacy_id", "customer_id", "quantity", "unit_price", "tier", "priority"] and duplicate_ids == ["LEG-1002"]
        csv_detail = f"rows={len(rows)}; duplicates={duplicate_ids}; headers={headers}"
    except Exception as exc:
        csv_ok = False
        csv_detail = str(exc)
    results.append(check("legacy-fixture-shape", csv_ok, csv_detail))

    marker_failures: list[str] = []
    for relative, markers in SOURCE_MARKERS.items():
        text = (ROOT / relative).read_text(encoding="utf-8") if (ROOT / relative).is_file() else ""
        for marker in markers:
            if marker not in text:
                marker_failures.append(f"{relative}: missing {marker}")
    results.append(check("architecture-and-brand-control-markers", not marker_failures, "failures=" + repr(marker_failures)))

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    github_links = re.findall(r"https://github\.com/tsmithcode/[^)\s]+", readme)
    non_public_proof_links = [link for link in github_links if not link.startswith("https://github.com/tsmithcode/tsmithcode")]
    results.append(check("public-github-link-boundary", not non_public_proof_links, "links=" + repr(github_links)))

    required_ctas = [
        "https://tsmithcode.ai/software-discovery-diagnostic",
        "https://tsmithcode.ai/software-consulting-pricing",
        "https://tsmithcode.ai/software-proof-kits",
        "https://www.cadguardian.com/",
    ]
    missing_ctas = [url for url in required_ctas if url not in readme]
    results.append(check("organization-routing-and-discovery-links", not missing_ctas, "missing=" + repr(missing_ctas)))

    routing_text = (ROOT / "docs" / "brand-and-engagement-routing.md").read_text(encoding="utf-8") if (ROOT / "docs" / "brand-and-engagement-routing.md").is_file() else ""
    routing_requirements = [
        "one opportunity-routing system",
        "Software architecture, modernization, and public technical authority",
        "C2C procurement and delivery entity for CAD and engineering automation",
        "Do not duplicate the same offer under both brands",
    ]
    missing_routing = [value for value in routing_requirements if value not in routing_text]
    results.append(check("organization-brand-routing", not missing_routing, "missing=" + repr(missing_routing)))

    public_text_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".md", ".cs", ".py", ".sh", ".ps1", ".yaml", ".yml", ".json", ".csv", ".props", ".csproj", ".svg"}
    ]

    local_path_patterns = [re.compile(r"/Users/[^/\s]+"), re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+")]
    leaked_paths: list[str] = []
    for path in public_text_files:
        text = path.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in local_path_patterns):
            leaked_paths.append(str(path.relative_to(ROOT)))
    results.append(check("no-local-user-paths", not leaked_paths, "files=" + repr(leaked_paths)))

    scanner_path = Path(__file__).resolve()
    brand_scan_files = [path for path in public_text_files if path.resolve() != scanner_path]
    blocked_brand_fragments = [
        "".join(("g", "v", "o")),
        "".join(("good", "vibes", "only")),
    ]
    brand_leaks: list[str] = []
    for path in brand_scan_files:
        normalized = re.sub(r"[^a-z0-9]+", "", path.read_text(encoding="utf-8").lower())
        for blocked in blocked_brand_fragments:
            if blocked in normalized:
                brand_leaks.append(f"{path.relative_to(ROOT)}:{blocked}")
    results.append(check("work-safe-brand-boundary", not brand_leaks, "files=" + repr(brand_leaks)))

    passed = sum(1 for result in results if result["status"] == "PASS")
    report = {
        "kit": "TSmithCode .NET Modernization Public Runnable Evaluation Kit",
        "checks": results,
        "passed": passed,
        "failed": len(results) - passed,
        "status": "PASS" if passed == len(results) else "FAIL",
    }
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "preflight-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    for result in results:
        print(f"{result['status']} {result['name']}: {result['detail']}")
    print(f"{report['status']} preflight {passed}/{len(results)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
