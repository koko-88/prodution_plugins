# Intake Handoff contract 1.0.0

The authoritative record is **relative to the consumer project**:
`docs/intake/<stable-request-slug>/HANDOFF.md`. Never substitute the plugin's
checkout/cache directory for the consumer workspace. Explicitly use `--workspace`.
If multiple consumer roots are plausible, resolve that before writing. File
authorization permits this record; discussion-only authorization does not.

The fixed ten headings and machine block fields are defined by
`../assets/handoff.schema.json`; `../assets/HANDOFF.md` is the versioned template.
The validator enforces this contract without third-party libraries. Every section
also needs explanatory text. Keep required headings even for an inapplicable
section, writing `not applicable: <reason>`. Arrays may be empty with an explained
reason/unknown; that is structurally valid, not proof of semantic adequacy.

## Path, identity and resume

Use `python <skill>/scripts/intake.py locate --workspace <consumer> --goal
<original-goal> [--request-id <stable-id>]` to compute identity without writing.
It normalizes Unicode/whitespace/case, derives SHA-256 from the original ID (or
goal), and appends twelve digest characters to a safe readable slug. Non-Latin
goals have the same stable digest fallback. Use an explicit request ID to
distinguish separate requests with the same goal. Never derive a new slug from
the latest follow-up wording: recover the original identity/path first.

To initialize after file authorization: `python <skill>/scripts/intake.py init
--workspace <consumer> --goal <original-goal> --request-id <id> --owner <owner>
--write`. It creates one explicitly incomplete, `blocked_evidence` record and
refuses overwrites. Complete it in place with normal file tools, or prepare the
same Markdown in an authorized temporary location and publish with `put` below.
Do not leave an initialized scaffold represented as a finished intake.

Validate: `python <skill>/scripts/intake.py validate <absolute-handoff-path>
--workspace <consumer>`. The result includes its SHA-256 for safe updates.
Publish a prepared document: `python <skill>/scripts/intake.py put --workspace
<consumer> --content <draft-file> --expected-sha <last-sha> --write`.
Omit `--expected-sha` only for initial publication. Existing identity cannot change;
stale updates, lock collisions, path traversal and linked output paths are refused.
Keep consumer permissions and avoid concurrent manual edits. The writer is a
local cooperating-writer guard, not a filesystem security boundary against a
malicious process replacing directories during execution.

## Machine blocks

Keep requirement traceability within the existing prose sections; no new schema
keys or parallel requirements document are required. Assign stable requirement
IDs (for example `R1`), state the requirement and its source evidence ID, classify
it as owner-confirmed/proposed/unknown, and point to its scenario/decision/gap IDs.
Put functional outcomes in Intent/Scope, quality and dependencies in Constraints,
and prohibitions in Scope & Exclusions. Link existing authoritative requirements
instead of silently replacing them. On correction, retain superseded history and
update every affected link. Review every explicit prompt requirement before
readiness; structural validation alone cannot detect a silently omitted requirement.

For an end-to-end multi-domain request, the `domain` and `next_receiver` strings
can name the affected domains/owners; `readiness.actions` names each acquisition
request and shared dependencies. Keep one identity/path and the version 1.0.0
shape. Separate factory execution remains outside the intake's authorization.

Each designated section has exactly one fenced `json` object with the named
wrapper; no JSON frontmatter/parser dependency is needed. Names, types and required
fields are fixed by the schema descriptor; unknown fields/version fail validation.

- `identity`: ID/schema/request key/slug/domain/scope/status, accountable owner,
  updated-by and timezone-aware updated-at, relative canonical path, approval.
  `approval` is `not_requested`, `not_confirmed` or `owner_confirmed`; the last
  requires a sourced accepted decision. Use `unknown`/`unassigned` honestly.
- `evidence`: IDs, claim, kind (`observed`, `desired`, `document`, `proposal`),
  evidence class from policy.md, accessible source pointer, authority and observed
  timestamp. User statements can point to `conversation:<turn-or-quote-anchor>`.
- `scenarios`: IDs, actor, goal, trigger/preconditions/main path/postconditions as
  text; alternatives/failures/rules as string arrays; status
  `proposed|confirmed|superseded`; sources as evidence IDs. Rules carry IDs in their
  strings, e.g. `R1: A duplicate must not create a second charge (E2)`.
- `decisions`: IDs, statement, `accepted|proposed|provisional|contradicted|superseded`,
  origin, authority, evidence IDs, consequence. Use contradicted/superseded entries
  to preserve assumption/correction history; proposals never become accepted by
  the agent's preference. Accepted entries require source and owner authority.
- `gaps`: IDs; type from policy.md; question, impact, boolean blocking,
  `open|resolved|deferred`, owner, acquisition route, dependency gap IDs and evidence
  IDs. Dependencies must exist and be acyclic. A blocking gap cannot be deferred
  without explicitly changing its blocking consequence and explaining why.
- `readiness`: status, sufficiently-known text, next receiver, action string array,
  limitation string array. Same status as identity, derived from all open blockers
  by policy.md's deterministic precedence. Actions are acquisition requests, not
  a downstream implementation plan or authorization to execute.

Sources/decisions/scenarios/gaps have globally unique IDs within the record.
Every source reference resolves to an evidence record; source pointers themselves
remain human/researcher-verifiable. Prefer consumer-relative pointers and reachable
URLs over developer-machine absolute paths. Include source date/authority and
inspection limits; do not dump source text. Link existing PRDs/use cases/ADRs in
Context Pointers without silently replacing them.

## Validation limits

Structural checks detect missing/order/duplicate headings, malformed JSON, missing
fields, invalid references, cyclic dependencies, placeholders, unsafe paths and
inconsistent blockers/readiness. They cannot certify source truth, actual user
approval, scenario completeness, domain correctness or whether a question was
leading. Behavioral cases and independent review test those separately.
