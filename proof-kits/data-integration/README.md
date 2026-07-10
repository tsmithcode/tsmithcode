# Data Integration Readiness Proof Kit

**Framework-level decision artifact for exposing schema, ownership, validation, exception, and reconciliation risk before integration work begins.**

**Artifact class:** Reusable decision artifact.  
**Current maturity:** Public decision framework; no executable connector or customer-system adapter is included.

## Buyer question

Can the source and target systems be connected without hiding data ownership, quality, exception, duplication, or source-of-truth risk?

## Decision this supports

Use this framework to decide whether the next funded step should be source cleanup, contract mapping, a private-sample diagnostic, or a bounded first integration slice.

## Best for

- Teams connecting ERP, CRM, quoting, reporting, file, database, or API workflows.
- Technical leaders preparing a migration or synchronization effort.
- Buyers who need a clear data-quality and ownership decision before implementation.

## Fastest review route

1. Name the source system, target system, and business decision the integration must support.
2. Identify owners for each source, transformation, exception path, and target record.
3. Map required fields, identifiers, null rules, duplicates, reference data, and validation behavior.
4. Define reject handling, retry or replay behavior, reconciliation, and operational evidence.
5. Choose the smallest private-sample slice that can prove the contract safely.

## Review areas

- source and target ownership;
- field names, types, formats, units, and required values;
- primary, natural, and idempotency keys;
- null, duplicate, stale, and invalid-record handling;
- transformations and reference-data dependencies;
- rejects, retries, replay, and manual correction;
- record-count and financial-total reconciliation;
- lineage, timestamps, logging, and support ownership;
- source-of-truth and conflict-resolution decisions;
- security, retention, and private-data handling.

## Expected decision packet

A completed review should produce:

```text
source-target-map.md
field-contract.md
validation-matrix.md
exception-register.md
reconciliation-plan.md
ownership-map.md
first-slice-decision.md
```

The filenames are a recommended packet structure, not generated artifacts in the current framework.

## Acceptance questions

- Can every required target field be traced to an approved source or explicit rule?
- Are duplicate and idempotency decisions testable?
- Is invalid data rejected visibly instead of silently coerced?
- Can source and target counts, totals, and exceptions be reconciled?
- Is there a named owner for operational failures and correction?
- Is the first slice narrow enough to reverse or replay safely?

## Proof boundary

This public framework demonstrates integration-readiness judgment. It does not include a deployed pipeline, live API connection, production credentials, customer export, performance benchmark, or executed reconciliation receipt.

No customer data, credentials, private schemas, production logs, raw correspondence, or restricted source files belong in this public proof surface.

## What to send

For a scoped private review, prepare only approved material:

- a redacted or synthetic representative sample;
- source and target system descriptions;
- required output fields and identifiers;
- known null, duplicate, and exception examples;
- the decision owner and desired business outcome.

## Canonical next action

- [Start the TSmithCode Software Discovery Diagnostic](https://tsmithcode.ai/software-discovery-diagnostic)
- [Review software consulting pricing](https://tsmithcode.ai/software-consulting-pricing)
- [Open all TSmithCode software proof kits](https://tsmithcode.ai/software-proof-kits)
- [Return to the TSmithCode proof hub](../../README.md)

The governing standard is [TSmithCode Public Proof Standard](../../docs/TSMITHCODE_PUBLIC_PROOF_STANDARD.md).
