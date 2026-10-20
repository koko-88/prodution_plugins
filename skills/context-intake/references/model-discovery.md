# Actor, document and model discovery

For exact source variants, host adapters and current project-policy comparisons,
consult [the detailed model routes](coverage-models.md) only when needed. Those
source-specific comparisons distinguish historical audit claims from current files.

## Product-model lens

Distinguish initiating and supporting actors, including scheduled processes and
external systems. Connect an actor's goal to use cases and an end-to-end journey.
For a material use case retain trigger, preconditions, main flow, alternatives,
failures and postconditions. Separate normative business rules, functional behavior,
quality requirements, external constraints and vocabulary/context boundaries.
Use stable IDs and source links instead of writing one mandatory document per kind.

ProductShape explore grounds questions in specific model holes. Define turns stated
intent into proposed artifacts with traceability; recovery infers candidates from
existing evidence. These are different operations. Treat recovered candidates as
proposed and record provenance, confidence, contradictory evidence and freshness.
An accepted model is an owner artifact; intake must not replace it or start a
CHG-INITIAL/change lifecycle. Existing rules may describe intended behavior that
current code violates, so preserve both.

Graph-guided refine uses neighbors as review candidates, not automatic scope.
Classify each as affected, checked/unaffected or uncertain; retain consciously
excluded neighbors and parked questions. A coherent large outcome need not be
split just because a graph has many nodes. Rank questions by product risk and
record the person's actual answer. Silence does not raise confidence. Narrative
readiness is judgment, separate from structural validation. Bind-consumers adds
claim-level citations and visible drift without changing a spec's meaning; running
its citation/scope mutation workflow is delegated.

## GSD lenses and distinct modes

Exploration follows the person's thread; concrete walkthroughs and contextual
domain probes reveal hidden ambiguity. The shared core imports the questioning
technique, not a required domain vocabulary, project initializer or research phase.
New-project and new-milestone distinguish initial vision from a bounded increment;
recover earlier decisions and existing requirements before eliciting a new delta.
An existing PRD can bypass repeated foundational interviewing, with remaining gaps
still explicit. Onboarding and ingestion help locate canonical ADR/PRD/SPEC/RFC
sources; do not run full mapping/scaffolding during intake.

The source discuss variants differ meaningfully:

- **Default**: sequential answers shape the next question; its four-question
  sittings are pacing, not shared completeness requirements.
- **Batch**: small grouped questions; shared intake additionally enforces
  independent prerequisites and user pacing consent.
- **Analyze**: compare options with grounded consequences before asking. Agent
  recommendations stay proposals.
- **Advisor**: research-backed comparisons calibrated to the owner's knowledge.
  Translate technical choices into outcomes. Actual research/model orchestration
  belongs to acquisition, not the generic entry.
- **Power**: asynchronous questions and resumable answers. Use an optional linked
  questionnaire only when requested; do not mandate JSON/HTML/context artifacts.
- **Evidence-first assumptions**: inspect relevant evidence first, then present
  a claim, source and consequence if wrong; ask primarily for corrections.
- **`--assumptions` explanation**: disclose assumptions conversationally. It is
  distinct from configured assumptions-analysis mode and its context creation.
- **All/text**: area selection and accessible plain-text rendering are interaction
  overlays, not new authority to decide or execute.
- **Auto/chain**: source modes can select recommended answers and advance to
  planning/execution. This lifecycle is excluded; shared intake may use only
  harmless clearly labeled provisional defaults, never invent owner decisions.

Spec-phase's goal/boundary/constraint/acceptance rubric exposes uncertainty;
its numerical score is an agent judgment, not a validated probability. Its bounded
rounds, optional extended discussion and fast derivation from adequate evidence
remain distinct pacing/depth choices under policy.md.

Edge probes examine applicable boundary, adjacency, empty, encoding, ordering,
precision, idempotency and concurrency dimensions. Omitted or inapplicable
dimensions need a reason where material. Distinguish resolved, dismissed and
unresolved; a missing classifier cue is not proof that a behavior is edge-free.
Prohibition probing first considers unwanted transformations of the feature, then
filters out irrelevant routine engineering concerns. Keep bespoke owner constraints
and refer canonical security/compliance facts to the proper specialist. Mechanical
versus judgment-based downstream verification is a handoff pointer; the shared
skill does not run enforcement engines or QA.

SPIDR's Spike/Paths/Interfaces/Data/Rules axes can reveal distinct scenario branches
or a research unknown. Use them to clarify boundaries; do not create phases,
split into technical layers or produce the final implementation plan.
Reversibility prioritizes decisions by actual undo consequences; do not reask an
already accepted owner decision. A thinking-partner comparison is opt-in when a
real tradeoff is open, and skippable when the person already decided.

## Document contradictions and Spec Kit

Record conflicting claims with source, authority, scope and consequence. Preserve
both locked variants until an accountable owner resolves them. Distinguish a
mechanically demonstrable conflict from semantic interpretation or a question.
Source document-ingestion approval is not approval to overwrite owner documents,
create a planning scaffold or merge locked criteria into an invented compromise.

Spec Kit specify contributes actor-centered scenarios and bounded success criteria;
clarify contributes an ambiguity taxonomy ranked by impact and uncertainty, one
question at a time with a five-question pacing cap. Checklist checks requirement
quality rather than application correctness. Analyze detects cross-artifact
inconsistency. Converge assesses code against spec/plan/tasks and appends missing
work to the task list; it is downstream work, not an intake algorithm. Specify's
three-question batch/default policy differs from clarify's sequential five-question
policy. Shared intake preserves pacing choices without guessing material owner
decisions. Preserve their project
policies separately in the ledger. The shared handoff links the existing spec
instead of overwriting it or inheriting its branch/scripts/approval lifecycle.
