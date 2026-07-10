# TSmithCode Public Proof Standard

**Status:** Public-facing operating standard  
**Applies to:** TSmithCode software proof kits, operational proofs, production-system proofs, reusable decision artifacts, authority-support repositories, and technical reference libraries.

## Purpose

Every public TSmithCode artifact should help a serious evaluator answer a decision question quickly, inspect the evidence safely, understand the boundary of the proof, and take the correct next action.

## Brand architecture

- **TSmithCode.ai** is the general software consulting, software-architecture authority, and hiring-evaluation brand.
- **CAD Guardian LLC** is the legal/procurement entity and the specialist CAD, Autodesk, SolidWorks, BIM, Vault, PDM/PLM, drawing, BOM, and engineering-workflow service line.
- The two brands use one evidence-first delivery system, but they are not presented as interchangeable identities.
- General software work routes through TSmithCode. CAD and engineering-platform work routes through CAD Guardian.
- Engagement paperwork may be issued by CAD Guardian LLC while the technical proof remains in the correct public brand lane.

## Public proof classes

1. **Runnable evaluation kit** — clone, run, inspect generated evidence, and decide whether a bounded funded slice is justified.
2. **Operational proof** — demonstrates how an environment, workflow, or system is inspected, measured, automated, and documented.
3. **Production-system proof** — demonstrates controlled execution, recovery, release preparation, or media-production operations.
4. **Reusable decision artifact** — a template that converts discovery into an inspectable technical or business decision packet.
5. **Authority-support artifact** — supports identity, experience, claims, or role evaluation without pretending to be executable implementation proof.
6. **Reference library** — durable code or API guidance that routes evaluators to a stronger runnable proof when execution evidence is required.

## Required evaluator structure

Each repository should make the following visible near the top of its README, adapted to the artifact class:

- evaluator or buyer question;
- decision this proves;
- best-fit audience;
- fastest review or run route;
- expected evidence or outputs;
- proof boundary;
- what to send or share;
- canonical next action;
- relationship to the wider TSmithCode and CAD Guardian proof system.

## Evidence and claim controls

- Use public, synthetic, owner-approved, or explicitly licensed inputs.
- Do not publish client files, source code, credentials, private screenshots, raw correspondence, meeting links, opportunity notes, or restricted account data.
- Do not present illustrative assumptions as customer results.
- Commands, filenames, output paths, and links must match the repository.
- Generated artifacts should be ignored or held for review before publication unless they are deliberately approved examples.
- Licensed or native runtime boundaries must be explicit.
- Missing tools, unsupported runtimes, and failed gates are reported honestly.

## Language and visual rules

- Use concise enterprise language focused on decisions, evidence, risk, and handoff.
- Do not expose internal control phrases such as “absolute ceiling,” private workflow prompts, or opportunity-specific preparation notes.
- Avoid unsupported superlatives and vague claims of production readiness.
- Where visual assets exist, use the TSmithCode dark-navy, cyan, teal, white, and restrained-neutral family consistently.
- Keep heading order, CTA language, and proof-boundary terminology consistent across repositories.
- State the artifact class explicitly so a reference library is not mistaken for a runnable proof kit.

## Canonical routing

### TSmithCode software consulting

- Software proof kits: https://tsmithcode.ai/software-proof-kits
- Software discovery diagnostic: https://tsmithcode.ai/software-discovery-diagnostic
- Pricing: https://tsmithcode.ai/software-consulting-pricing
- Consulting contact: https://tsmithcode.ai/software-consulting-contact

### TSmithCode hiring evaluation

- Resume: https://tsmithcode.ai/software-leadership/resume
- Technical-screen videos: https://tsmithcode.ai/software-leadership/videos
- Hiring contact: https://tsmithcode.ai/software-leadership/contact

### CAD Guardian specialist consulting

- Services: https://www.cadguardian.com/services
- Consulting contact: https://www.cadguardian.com/contact

## Repository role matrix

| Repository | Public role |
|---|---|
| `tsmithcode/tsmithcode` | Authority hub and runnable software proof-kit system |
| `tsmithcode/tsmithcode-ai-workstation-profiler` | Operational workstation-readiness proof |
| `tsmithcode/m5-max-ai-workstation-video-command-center` | Production-control and one-person media-operations proof |
| `tsmithcode/opportunity-technical-alignment-template` | Reusable technical decision artifact |
| `tsmithcode/tsmithcode-software-architect-resume` | Authority-support and resume-generation system |
| `tsmithcode/autocad-api-snippets` | AutoCAD .NET reference library; runnable CAD proof is routed to CAD Guardian |

## Release gate

Before a public change is merged:

- the repository role is correct and explicit;
- the required evaluator sections are present;
- public links and commands are checked;
- local user paths and private markers are absent;
- the public/private boundary is visible;
- visual assets are readable at repository-preview scale;
- the repository’s verification command is run when one exists;
- an executable proof is not called complete without a real execution receipt;
- unresolved release blockers are documented and the change remains unmerged or draft.
