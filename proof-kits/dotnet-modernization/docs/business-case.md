# Business case: modernize the order-acceptance boundary without a rewrite gamble

## Representative enterprise problem

A legacy order workflow still runs the business, but validation, pricing, persistence, notifications, and release behavior are coupled. Retries can create duplicate work, integration success is difficult to prove, changes require broad regression testing, and migration estimates are based on incomplete assumptions.

This pattern appears across manufacturing, logistics, distribution, insurance operations, healthcare administration, construction, field service, and internal finance workflows. The specific domain changes; the modernization risks remain recognizable.

## What this proof demonstrates

- Existing behavior is characterized before code is moved.
- The first slice is selected around business value and rollback, not framework fashion.
- Pricing parity is measured rather than assumed.
- A versioned API makes validation and error behavior explicit.
- Idempotency prevents a routine retry from creating duplicate operational work.
- An outbox receipt creates a reviewable integration boundary.
- Correlation-aware logs and health evidence make operations part of acceptance.
- Synthetic migration data is reconciled by count, duplicate detection, and financial total.
- An executive decision report and engineer evidence packet are generated from the same run.

## Illustrative ROI model — not a customer result

Assume a workflow processes 2,000 orders each month and 1% require duplicate-processing or retry investigation. That produces 20 avoidable exceptions. At an illustrative 45 minutes per investigation, the workflow consumes 15 hours monthly before including financial correction, customer impact, release delay, or management review.

This is not a claimed client outcome. A paid diagnostic replaces the assumptions with measured transaction volume, exception rate, labor cost, incident history, deployment effort, and opportunity cost.

## Ten-minute engineering evaluation

1. Run `./run-proof.sh` or `./run-proof.ps1`.
2. Inspect `reports/test-receipt.json` for characterization, parity, validation, idempotency, and outbox controls.
3. Inspect `reports/api-smoke-receipt.json` for HTTP behavior, duplicate replay, correlation evidence, and validation problems.
4. Inspect `reports/reconciliation-report.json` for migration count, duplicate detection, and financial-total parity.
5. Review `openapi.yaml` and `docs/architecture-and-decisions.md`.
6. Decide whether the approach is suitable for a deeper source-system diagnostic.

## Two-minute executive evaluation

Read:

- `reports/executive-decision-brief.md`
- `reports/modernization-readiness.md`
- `reports/risk-register.md`

The decision is deliberately smaller than “rewrite the application.” It asks whether a bounded order-acceptance slice can be funded safely, what controls are required, and which decisions still depend on the real environment.

## Recommended paid next step

The [TSmithCode Software Discovery Diagnostic](https://tsmithcode.ai/software-discovery-diagnostic) maps the actual workflow, source systems, business rules, integration risks, deployment constraints, first implementation slice, estimate, and go/no-go decision packet.
