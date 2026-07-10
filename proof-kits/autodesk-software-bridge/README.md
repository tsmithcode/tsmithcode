# Autodesk Software Bridge Proof Kit

**Framework-level decision artifact for connecting Autodesk and engineering workflows to general software systems without hiding native-runtime, file, job-state, identity, or ownership risk.**

**Artifact class:** Reusable decision artifact.  
**Current maturity:** Public architecture and integration-boundary framework; no licensed Autodesk execution, client file, production adapter, or native runtime receipt is included.

## Buyer question

Can CAD events, data contracts, job state, identity, validation, evidence, logs, and business-system handoff be bounded before implementation begins?

## Decision this supports

Use this framework to decide whether the first funded step belongs in general software architecture, CAD-native discovery, a private representative-sample pass, or a bounded bridge implementation.

## Best for

- Teams connecting AutoCAD, Inventor, Revit, Vault, or related engineering workflows to APIs, databases, ERP, GIS, reporting, queues, or internal platforms.
- Technical leaders separating desktop/native CAD concerns from cloud and enterprise-software boundaries.
- Buyers who need a clear ownership and runtime decision before sharing private drawings, models, or Vault context.

## Brand and delivery route

- **TSmithCode.ai** covers the general software side: contracts, APIs, job orchestration, data integration, cloud services, observability, internal platforms, and release readiness.
- **CAD Guardian LLC** covers the specialist CAD side: licensed Autodesk runtimes, drawings, models, Vault/PDM context, native add-ins, AutoLISP/iLogic rules, and engineering-workflow validation.
- A real engagement may use both lanes, but the public proof and buyer route should remain explicit.

## Fastest review route

1. Name the Autodesk product, version, native command or event, and business outcome.
2. Define the approved file, model, metadata, or Vault boundary.
3. Separate licensed desktop/native execution from service, API, queue, database, and reporting responsibilities.
4. Define payload, identity, validation, idempotency, job-state, retry, and evidence contracts.
5. Name ownership for runtime, queue, failure, support, and data correction.
6. Select the smallest public or approved private sample that can prove the bridge safely.

## Review areas

- Autodesk product, version, SDK, framework, and deployment model;
- native document, transaction, command, and file-lifecycle boundaries;
- drawing, model, property, BOM, sheet, and Vault/PDM ownership;
- desktop worker, job processor, service, queue, API, and database responsibilities;
- request, response, event, and file-package contracts;
- correlation, idempotency, retry, replay, timeout, and cancellation;
- identity, permissions, licensing, secrets, and environment ownership;
- validation, fixture receipts, logs, reports, and audit evidence;
- CTB/STB, fonts, xrefs, references, units, coordinates, and native dependencies where relevant;
- support, rollback, recovery, and private-sample acceptance.

## Expected decision packet

A completed review should produce:

```text
native-and-service-boundary.md
representative-payload-contract.md
job-state-model.md
identity-and-permission-map.md
validation-and-evidence-requirements.md
runtime-and-support-ownership.md
risk-register.md
first-slice-decision.md
```

The filenames are a recommended packet structure, not generated artifacts in the current framework.

## Acceptance questions

- Is licensed CAD execution clearly separated from general software services?
- Can every job be correlated from intake through native execution and handoff?
- Are duplicate, retry, timeout, cancellation, and partial-failure behaviors explicit?
- Are private files and production credentials kept behind approved access controls?
- Is the first slice testable with public or approved representative fixtures?
- Is ownership clear for CAD runtime failures and downstream integration failures?

## Proof boundary

This public framework demonstrates Autodesk-to-software integration judgment. It does not include licensed Autodesk execution, customer drawings or models, Vault data, private business systems, credentials, production performance evidence, or a deployed bridge.

Public sample architecture only. Native runtime receipts, private fixtures, customer schemas, and production logs remain outside the public proof boundary.

## What to send

For a scoped private review, prepare only approved material:

- Autodesk product and version;
- the native command, event, or repeated engineering workflow;
- one public or approved representative sample;
- desired downstream payload or business-system outcome;
- runtime, data, and support owners;
- the decision expected from the first slice.

## Canonical next action

### General software and bridge architecture

- [Start the TSmithCode Software Discovery Diagnostic](https://tsmithcode.ai/software-discovery-diagnostic)
- [Open all TSmithCode software proof kits](https://tsmithcode.ai/software-proof-kits)

### CAD-native and engineering-workflow execution

- [Review CAD Guardian services](https://www.cadguardian.com/services)
- [Contact CAD Guardian](https://www.cadguardian.com/contact)
- [Open the AutoCAD, AutoLISP, and .NET runnable proof](https://github.com/tsmithcode/cadguardian-autocad-autolisp-dotnet-proof)
- [Open the Inventor automation runnable proof](https://github.com/tsmithcode/cadguardian-inventor-automation-proof)

- [Return to the TSmithCode proof hub](../../README.md)

The governing standard is [TSmithCode Public Proof Standard](../../docs/TSMITHCODE_PUBLIC_PROOF_STANDARD.md).
