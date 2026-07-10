# Reporting Quality Proof Kit

**Framework-level decision artifact for determining whether a report is traceable, reconcilable, and safe to use for operational or financial decisions.**

**Artifact class:** Reusable decision artifact.  
**Current maturity:** Public reporting-quality framework; no customer report, production dataset, or executed validation receipt is included.

## Buyer question

Can exported numbers be traced to approved sources, field definitions, calculations, filters, totals, refresh behavior, exceptions, and accountable owners?

## Decision this supports

Use this framework to decide whether a report is ready for decision use, requires targeted remediation, or must be rebuilt around a clearer source and metric contract.

## Best for

- Teams reviewing dashboards, exports, operational reports, management metrics, or financial summaries.
- Technical leaders preparing a reporting migration or quality initiative.
- Buyers who need evidence that a report can be trusted before automating decisions around it.

## Fastest review route

1. Name the decision the report supports and the owner accountable for it.
2. Define each metric, field, calculation, filter, time window, and source system.
3. Trace sample outputs back to source rows and transformation rules.
4. Test nulls, duplicates, joins, totals, refresh timing, and exception behavior.
5. Record discrepancies, remediation priority, and owner signoff requirements.

## Review areas

- decision purpose and report owner;
- field and metric definitions;
- source-system lineage and transformation rules;
- joins, filters, grouping, and date-window behavior;
- null, duplicate, late, and missing-record handling;
- record-count, subtotal, and financial-total reconciliation;
- refresh schedule, stale-data signals, and snapshot timing;
- export formatting and downstream consumption;
- exception notes, limitations, and signoff;
- access, privacy, retention, and audit requirements.

## Expected decision packet

A completed review should produce:

```text
report-purpose-and-owner.md
field-and-metric-dictionary.md
source-lineage-map.md
validation-matrix.md
reconciliation-results.md
exception-register.md
remediation-priority.md
signoff-record.md
```

The filenames are a recommended packet structure, not generated artifacts in the current framework.

## Acceptance questions

- Can every material number be traced to an approved source and rule?
- Do totals reconcile at the level required by the decision owner?
- Are filters and time windows visible rather than implied?
- Are nulls, duplicates, exclusions, and stale data surfaced honestly?
- Can a reviewer reproduce the result from the documented inputs?
- Is there a named owner for correcting discrepancies?

## Proof boundary

This public framework demonstrates reporting-quality judgment. It does not validate a customer report, inspect private financial data, certify a dashboard, access production credentials, or provide executed lineage and reconciliation evidence.

Private reports, customer records, financial data, internal exports, production credentials, and restricted screenshots remain outside the public proof boundary.

## What to send

For a scoped private review, prepare only approved material:

- a redacted schema or representative sample;
- metric and field definitions;
- known filters and refresh behavior;
- one or more known discrepancies;
- the report owner and decision being supported.

## Canonical next action

- [Start the TSmithCode Software Discovery Diagnostic](https://tsmithcode.ai/software-discovery-diagnostic)
- [Review software consulting pricing](https://tsmithcode.ai/software-consulting-pricing)
- [Open all TSmithCode software proof kits](https://tsmithcode.ai/software-proof-kits)
- [Return to the TSmithCode proof hub](../../README.md)

The governing standard is [TSmithCode Public Proof Standard](../../docs/TSMITHCODE_PUBLIC_PROOF_STANDARD.md).
