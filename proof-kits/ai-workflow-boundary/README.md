# AI Workflow Boundary Proof Kit

**Framework-level decision artifact for placing AI inside explicit, reviewable operating boundaries rather than relying on hype or implicit trust.**

**Artifact class:** Reusable decision artifact.  
**Current maturity:** Public AI-governance framework; no production agent, private prompt set, model benchmark, or deployed automation is included.

## Buyer question

Are allowed inputs, prohibited data, reviewer responsibility, generated-output rules, fallback behavior, logging, evaluation, and approval gates explicit enough to adopt the workflow safely?

## Decision this supports

Use this framework to decide whether an AI-assisted task is ready for a controlled pilot, requires narrower authority, needs additional evaluation, or should remain human-only.

## Best for

- Teams adding AI to intake, drafting, classification, extraction, search, coding, reporting, or internal operations.
- Technical and business leaders defining human approval and accountability.
- Buyers who need a bounded adoption decision before private data or production actions are introduced.

## Fastest review route

1. Define the task, user, business decision, and maximum allowed consequence.
2. Separate allowed inputs from prohibited, restricted, or approval-gated data.
3. Define output format, evidence requirements, and reviewer responsibility.
4. Specify tool access, action authority, fallback, timeout, and stop conditions.
5. Build an evaluation set with representative success, ambiguity, and failure cases.
6. Record logging, retention, monitoring, incident, and adoption gates.

## Review areas

- task purpose and accountable owner;
- allowed, prohibited, and approval-gated inputs;
- prompt, retrieval, tool, and model boundaries;
- output schema, citations, provenance, and uncertainty;
- human-review and approval requirements;
- permitted actions and prohibited side effects;
- fallback, retry, escalation, and manual completion;
- evaluation dataset and acceptance rubric;
- hallucination, privacy, security, bias, and misuse risks;
- logging, retention, audit, monitoring, and incident response;
- rollout stages, kill switch, and adoption decision.

## Expected decision packet

A completed review should produce:

```text
task-and-authority-boundary.md
input-and-data-policy.md
output-and-provenance-contract.md
human-review-checklist.md
evaluation-rubric.md
fallback-and-escalation-path.md
audit-and-retention-requirements.md
pilot-adoption-decision.md
```

The filenames are a recommended packet structure, not generated artifacts in the current framework.

## Acceptance questions

- Is the task narrow enough that success and failure can be evaluated?
- Are sensitive inputs and prohibited actions explicit?
- Can a reviewer trace material outputs to approved evidence?
- Does the system fail safely when tools, models, or context are unavailable?
- Is human responsibility preserved for consequential decisions?
- Can the workflow be disabled, audited, and completed manually?
- Are adoption claims limited to the evidence actually collected?

## Proof boundary

This public framework demonstrates AI-workflow boundary and governance judgment. It does not establish model quality, production safety, regulatory compliance, customer ROI, or readiness for autonomous action.

Synthetic examples only. Private prompts, internal data, customer records, credentials, production agents, unrestricted tool access, and confidential evaluation sets remain outside the public proof boundary.

## What to send

For a scoped private review, prepare only approved material:

- a redacted task description;
- representative approved inputs and desired outputs;
- prohibited data and actions;
- human reviewer and decision owner;
- success, ambiguity, and failure examples;
- the pilot decision that must be made.

## Canonical next action

- [Start the TSmithCode Software Discovery Diagnostic](https://tsmithcode.ai/software-discovery-diagnostic)
- [Review software consulting pricing](https://tsmithcode.ai/software-consulting-pricing)
- [Open all TSmithCode software proof kits](https://tsmithcode.ai/software-proof-kits)
- [Return to the TSmithCode proof hub](../../README.md)

The governing standard is [TSmithCode Public Proof Standard](../../docs/TSMITHCODE_PUBLIC_PROOF_STANDARD.md).
