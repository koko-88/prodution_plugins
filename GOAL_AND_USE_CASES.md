# Shared Context Intake — Goal, Scenarios, and Scope

**Status:** Canonical product goal and use-case catalog (2026-10-19); not a record of implementation or evaluated success. This document preserves owner-confirmed direction and the 35 candidate use cases without converting scenarios into automatically executable tests.

## 1. Goal — confirmed

Build **one reusable, domain-neutral Context Intake Skill** for Codex/agent workflows. Given a natural-language request and any already-accessible information, understand the real desired outcome and affected people/systems, discover materially relevant scenarios and user-owned decisions, distinguish observations from wishes and proposals, identify gaps/dependencies/contradictions, and produce a stable evidence-linked Intake Handoff for the next **specialized domain context acquisition** stage.

Re-use mature existing methods (Matt Pocock Grilling, gstack, GSD, ProductShape, Spec Kit and relevant peers) using Skill Creator. **Preserve every distinct relevant behavioral variant** through conditional modes or an explicitly justified specialist/exclusion status; do not mechanically concatenate unrelated original Skills. Avoid repeated questions and unnecessary credits. The same entry skill must serve Software, UI/UX, n8n and future factories.

The project goal is a **reliable intake and routing contract**, not a new coding agent, custom orchestrator or speculative framework.

## 2. Inputs and outputs — confirmed

**Inputs:** User goal/feature/problem, previous accepted decisions, existing canonical docs, relevant system/repository facts if available, and access to optional existing tools. A new/greenfield request may have no existing system; a brownfield request may have code/workflows/design/docs to inspect only as needed to frame intent. Never infer that greenfield means external evidence is unnecessary.

**Output:** One versioned canonical `docs/intake/<stable-request-slug>/HANDOFF.md` under the **consumer project workspace** when file writing is authorized. Fixed headings cover identity, intent, observed state and evidence, actors/scenarios, scope, constraints, decisions, open gaps/owners, context pointers and readiness for the next domain. The handoff is **not** the final product PRD or implementation plan and does not itself launch the downstream factory.

**Evidence policy:** Explicit owner decisions must be preserved with provenance. Code documents *current* behavior; it is not automatic approval of *desired* behavior. Facts which need specialized research should be typed and delegated, not fabricated or asked of an uninformed user.

## 3. User journeys — proposed scenario coverage for Skill Creator

The following scenarios represent distinct, important modes and risks. Labels `UC-*` are coverage IDs, not automatic evaluation fixtures. Before implementation of a new mode, verify its unique value against the existing `references/` and ledger.

### Entry and goal framing

- **UC-01 — Clear/complete request (fast path):** Agent uses existing facts, asks zero ceremonial questions, produces or proposes a handoff only if authorized.
- **UC-02 — Vague feature/idea:** Agent discovers desired outcome, beneficiary, pain/status quo, scope and important decisions through proportionate clarification.
- **UC-03 — Solution-first but problem-unclear:** Agent neutrally challenges a materially risky premise; records goal separate from suggested means.
- **UC-04 — Brownfield change:** Agent recovers relevant existing architecture/behavior/spec facts without doing a full domain inspection; distinguishes current vs desired.
- **UC-05 — Greenfield request:** Agent works with prompt, authoritative documents and relevant external research pointers without inventing an existing system.
- **UC-06 — Resume after pause/follow-up:** Agent preserves stable request ID and settled choices; updates the same handoff without re-asking.
- **UC-07 — Corrected understanding:** User overturns a premise/decision; agent updates affected assumptions, scenarios, gaps and handoff provenance.
- **UC-08 — Existing PRD, approved spec or contract:** Agent links authoritative artifacts; raises contradictions instead of overwriting them.

### Actors, use cases and requirements

- **UC-09 — Multiple actors/stakeholders:** Capture primary/supporting actors, owners, roles and user journeys without assuming one 'user' role.
- **UC-10 — Non-human/scheduled/API actors:** Account for jobs, callbacks, integrations, webhooks and external systems as actors or triggers.
- **UC-11 — Alternative/failure/edge paths:** Capture relevant negative states, partial failures, cancellation/retry, and postconditions without expanding the scope arbitrarily.
- **UC-12 — Quality attributes and nonfunctional boundaries:** Capture real security/privacy/reliability/accessibility/performance constraints; leave unknown targets unguessed.
- **UC-13 — Prohibitions and anti-goals:** Explicitly capture what must **not** happen, permissions, data boundaries and excluded outcomes.
- **UC-14 — Business rules and bounded contexts:** Surface relevant domain rules and conflicts; delegate deep domain modeling to appropriate owners.
- **UC-15 — Operational risks:** Surface consequential idempotency, rate limits, concurrency, failure recovery or integration boundary questions when genuinely applicable.

### Questions and knowledge authority

- **UC-16 — Independent questions:** Use a manageable decision-frontier batch when questions have no dependency and the user consents to batching.
- **UC-17 — Dependent questions:** Ask in sequence when earlier answers invalidate later questions.
- **UC-18 — User prefers one question:** Respect that interaction mode even when a batch is theoretically possible.
- **UC-19 — Deep grilling requested:** Preserve long-form exploration until consequential decisions are resolved or explicitly deferred; avoid default interrogation.
- **UC-20 — Budgeted intake:** Honor a question/time budget as a pacing control while keeping important unknowns visible.
- **UC-21 — Repo/internal/external fact available:** Inspect narrow read-only evidence where appropriate, or route to domain acquisition; do not quiz the user on searchable facts.
- **UC-22 — Unavailable tool or missing evidence:** Record the limitation and acquisition route; do not silently guess or demand installation.
- **UC-23 — Conflicting sources:** Distinguish owner authority, current observations, stakeholder statements and possible staleness; don't vote conflicts away.
- **UC-24 — Proposed default versus accepted decision:** Clearly label recommendations as provisional; never infer consent from silence or summaries.
- **UC-25 — Other stakeholder owns decision:** Identify owner and blocking consequence; no unauthorized outreach.
- **UC-26 — Existing workflow or legal/security boundary:** Preserve explicit scope and permissions; do not invoke lifecycle skills with side effects merely to gather intake.

### Cross-factory, lifecycle and output safety

- **UC-27 — Software factory consumer:** Produce relevant software context pointers without adopting a software-only intake schema.
- **UC-28 — n8n workflow consumer:** Describe user intent, actors, integrations and gaps without constructing a workflow or launching tools.
- **UC-29 — UI/UX factory consumer:** Capture journeys/states/design constraints without performing visual reconstruction or choosing UI stack.
- **UC-30 — Unknown/new domain:** Remain domain-neutral, identify unknown specialist, hand off concrete research questions.
- **UC-31 — Read-only discussion:** If files are not authorized, give an inline provisional handoff; do not initialize or write documents.
- **UC-32 — Authorized file output:** Write only the one canonical HANDOFF path using template/schema; expose unresolved blockers instead of false readiness.
- **UC-33 — Resume/concurrent edits/collisions:** Preserve stable ID, prevent accidental overwrite and flag inconsistent owner edits.
- **UC-34 — Skill overlap/unrelated request:** Don't hijack ordinary implementation, research, code review or QA tasks.
- **UC-35 — Token/cost-conscious operation:** Load only the relevant references and tools; no blanket repo scans or firecrawl calls by default.

## 4. Modes to preserve — confirmed design requirement

Fast path; sequential interviewing; independent decision-frontier batches; deep grilling; budgeted clarification; evidence-first/brownfield; stakeholder interview; premise check; and read-only discussion. Mode choice depends on dependencies, impact, user preferences and available evidence, not a universal questionnaire. Detailed origin and disposition are preserved in the provenance ledger.

## 5. Boundaries — confirmed

This Skill **does not** choose the technical stack, write application features, run complete software/workflow/UIUX inspections, perform final QA, launch other factories automatically, or alter tracker state. Specialized context acquisition belongs to separate factory capabilities; limited read-only fact checks are permissible during intake where material. Do not install duplicate tooling or burn Firecrawl credits.

**Build-stage authority:** This document defines **what the plugin must accomplish**, not which build stage is authorized to run. Current owner permissions and factual progress are recorded in `docs/BUILD_STATE.md`, interpreted with the owner's latest explicit request and `AGENTS.md`. In the present documentation-alignment task, edits to the named Markdown documents are authorized; testing, evaluation execution, packaging, installation, and runtime changes are not authorized. Do not turn older historical restrictions or proposals into permanent product requirements.

## 6. Behavioral Success acceptance — use cases are the source, not the test runner

The Skill must preserve sourced decisions, trace every adopted variant or justified exclusion, produce the stable contract, avoid invented requirements/approval, choose proportionate questions, route code vs domain research correctly, and avoid unwanted file edits. **Behavioral Success** requires evidence against the applicable UC-01..UC-35 in `evals/cases.yaml` using an **owner-approved Promptfoo evaluation configuration, independent fixtures/oracles and accessible host/provider**. The current YAML catalog is not executable as-is; no tests or fixtures are authorized merely by their mention here. Per-case results (pass/fail/blocked/not run), evidence pointers, and outstanding gaps belong in `docs/BUILD_STATE.md`. Source/variant coverage is **not** behavioral success.

**Ordering:** Behavioral Success is reviewed before Packaging Success. Packaging is governed by `PLUGIN_CONTRACT.md` and existing official creator/host tooling; no new packaging test infrastructure is implicitly authorized.

## 7. Existing knowledge and source of truth

- `skills/context-intake/SKILL.md` — current skill entry and routing.
- `skills/context-intake/references/` — distilled conditional methods and conflicts.
- `skills/context-intake/assets/` — stable Handoff template/schema.
- `docs/coverage/COVERAGE.md` — provenance summary, including the known unverified source claims.
- `docs/coverage/variant-ledger.json` and `coverage-matrix.md` — authoritative maintenance traceability; load only for specific coverage work.

**Open sources:** Current coverage report records five `blocked_unverified` entries, not a 100% source-parity claim. Other unstated product decisions remain unconfirmed, not guessed.
