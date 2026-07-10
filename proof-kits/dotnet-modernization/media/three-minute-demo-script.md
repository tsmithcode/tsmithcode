# Three-minute demonstration script

## 0:00–0:20 — The business risk

Show `docs/architecture-before.svg`.

> This is not a framework upgrade demo. It is a decision demo for a legacy workflow where validation, pricing, persistence, and downstream notifications are coupled. The question is whether one valuable capability can be extracted without losing business behavior or creating duplicate work.

## 0:20–0:45 — The evaluator promise

Show the repository README and the one-command block.

> An engineer can clone the public repository, run one command, and inspect the same evidence packet that supports the executive decision. There is no client code, production data, private credential, or fabricated customer result in this kit.

## 0:45–1:25 — Run the proof

Run `./run-proof.sh` or `./run-proof.ps1` and keep the terminal visible.

Call out the gates as they pass:

- public artifact and work-safety preflight;
- legacy characterization;
- modern pricing parity;
- duplicate replay and idempotency;
- explicit validation errors;
- one outbox receipt per accepted order;
- migration duplicate detection and financial reconciliation;
- API health, correlation, and smoke evidence.

## 1:25–2:05 — Inspect the receipts

Open:

- `reports/test-receipt.json`;
- `reports/api-smoke-receipt.json`;
- `reports/reconciliation-report.json`.

> The point is not that this synthetic app is complex. The point is that the controls are inspectable. A retry returns the original order, only one integration receipt exists, invalid input has a stable contract, and migrated financial totals reconcile.

## 2:05–2:35 — Show the target boundary

Show `docs/architecture-after.svg` and `docs/architecture-and-decisions.md`.

> The first funded slice is intentionally bounded: a versioned API, an application boundary, characterized pricing, durable-idempotency design, an outbox contract, operational evidence, and a rollback decision. The public in-memory store demonstrates the boundary; the diagnostic selects the production database, identity, deployment, telemetry, and support controls.

## 2:35–3:00 — Close on the decision

Open `reports/executive-decision-brief.md` and `reports/modernization-readiness.md`.

> Engineering and leadership receive one evidence system. The next step is not “rewrite everything.” It is a fixed-scope software discovery diagnostic that replaces synthetic assumptions with the real workflow, source systems, business rules, integration risks, measured economics, first implementation slice, estimate, and go-or-no-go packet.

End on:

- `https://tsmithcode.ai/software-discovery-diagnostic`
- `https://tsmithcode.ai/software-proof-kits`
