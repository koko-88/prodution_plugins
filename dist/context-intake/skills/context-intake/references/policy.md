# Mode selection and sufficiency

## Authority and conflict policy

Keep desired intent and observed behavior on separate tracks. An owner can decide
what should happen; code, runtime observations and documents establish what does
happen within their observation limits. A source's recency alone does not establish
its authority. Record source owner, date, scope and conflicting assertions.
Do not resolve conflicting stakeholder claims by popularity or the agent's taste.
Find the accountable decision owner; if unknown, make identifying that owner a gap.
Preserve contrary evidence and the consequence of choosing either claim.

Use evidence classes: **direct** (explicit owner statement or direct observation),
**supported** (multiple coherent sources support it), **inferred** (reasoned from
indirect evidence), **speculative** (testable proposal), **unknown** (not established).
Class and authority are distinct: direct observation of code is not direct approval
of a requirement. Store confirmed decisions only with a source and named authority.
An agent recommendation, default or hypothesis remains proposed/provisional.

Scope beats generic methodology. Keep a bounded request bounded. Challenge a
premise only when it materially threatens the requested outcome, cost, safety or
feasibility. Explain the consequence and ask a neutral question; do not restart
ideation. Compare broad alternatives only when that decision is actually open.
Honor prohibitions; do not infer that a positive feature request waives them.

When the user asks to clarify, test or improve an idea, select that stance
explicitly and stay with its goal. This is the limited reusable distinction from
[BMAD Forge Idea](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad-forge-idea/SKILL.md).
Its lifecycle, simulated personas and output family are not imported. BMAD's
[advanced elicitation](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad-advanced-elicitation/SKILL.md)
is critique of generated work; it cannot establish real stakeholder decisions.

## Choose a mode from the unresolved work

| Mode | Choose when | Behavior and exit |
| --- | --- | --- |
| Fast path | Outcome, actors, boundary and representative behavior are sufficiently specified | Ask zero questions; route fact work and write a validated handoff |
| Sequential | Answers change later questions, burden is high, or user prefers one at a time | Ask the highest-consequence unresolved owner question; update before the next |
| Frontier batch | Several current owner decisions have no dependency on one another | Offer a small readable batch with consent (explicit request for batching counts); preserve dependencies |
| Deep | User explicitly requests exhaustive grilling or consequences demand it | Continue until consequential decision frontier is empty or explicitly deferred; do not repeat answers |
| Budgeted clarification | User requests a time/question limit, or a bounded clarification method is selected | Prioritize ambiguity; a five-question budget is a pacing cap, never proof of completeness |
| Evidence-first | Existing system/docs can resolve facts or expose assumptions | Inspect narrowly, label observed/inferred assumptions, then ask only owner corrections |
| Stakeholder interview | Motivation, tacit practice or conflicting authority is unknown | Non-leading questions about actual episodes, workarounds and decision ownership |
| Premise check | Proposed means appear materially disconnected from the outcome | Separate goal from solution, surface evidence, preserve the bounded decision |
| Read-only | Caller authorizes discussion only or files are not authorized | No writes, no helper initialization; provide provisional chat output and acquisition route |

Inherited methods' one-question and batch defaults are conditional choices here.
Use user preference first, then decision dependence and burden. Explicit-invocation
wrappers remain explicit-only in their source systems; intake distills a method
without silently invoking the wrapper. No fixed questionnaire is compulsory.

## Rank and route gaps

For each unknown, record what changes if wrong, who owns it, and its dependencies.
Prioritize irreversible/high-impact scope and authority decisions before low-cost
reversible defaults. Ask a neutral question, explain why its answer matters, and
offer labeled proposals only if useful. Never hide a recommendation in a premise.

Types and routes:

- `user_decision`: desired behavior, priorities, tradeoffs or authorization owned
  by the caller. Ask the caller only if evidence has not already answered it.
- `other_stakeholder`: policy, business rule or operational knowledge owned by
  somebody else. Name that role/source; do not message them without authorization.
- `repo_fact`: inspect a specific file/symbol/config or delegate that inspection.
- `external_fact`: identify an official source/version and research question.
- `empirical_validation`: name an experiment/observation and success evidence.

Technical facts may remain open at pre-research handoff. They are blocking only
when missing evidence prevents framing a safe, meaningful acquisition request.
Unreachable optional tools alone do not block. If unavailable evidence is essential,
use `blocked_evidence` and identify a usable alternative or required access.

## Stopping and readiness

Stop when the intended outcome, actors, current/desired delta, boundary, material
prohibitions, representative scenario, decision authority and acquisition routes
are sufficiently clear for domain research. Cover relevant high-consequence
alternative/failure/quality risks, with open questions explicitly typed and owned.
Do not demand a final architecture, complete PRD or full QA suite at this stage.
Do not invent a metric just to satisfy a template. State that it is unknown and
whether it blocks acquisition. Empty headings are not evidence of adequacy.

Machine status is derived from **open blocking gaps** in this priority order:
`user_decision` -> `needs_user_decision`; `other_stakeholder` ->
`needs_other_stakeholder`; any other blocking type -> `blocked_evidence`; none ->
`ready_for_domain_acquisition`. Preserve all blockers even when only one primary
status fits. A ready handoff may retain nonblocking research/validation gaps.
Question budgets, time limits and user silence cannot make blockers disappear.

Before handoff, review semantics separately from the validator: are decision claims
actually owner-backed, is a concrete scenario representative, are crucial actors
missing, are facts separated from intent, and could the next factory act on the
gap routes without repeating intake? Summarize remaining risks honestly.

On correction/resume, retain IDs and original request identity. Mark superseded
decisions and invalid assumptions; update all affected scenarios, gaps and readiness.
Retain source history in the same artifact. If an upstream canonical spec differs,
link it and record the conflict; change it only with explicit authorization.
