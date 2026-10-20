# Intake Handoff

## Identity & Stage

```json
{"identity":{"id":"OPS-32","schema_version":"1.0.0","request_key":"f4238c14ac021d78b3f0c75e55f1f0254def3d5b0825185503f21bac46e6611d","slug":"ops-32-f4238c14ac02","domain":"facilities operations automation","scope":"Weekly aggregate room-usage reporting for Facilities","status":"ready_for_domain_acquisition","owner":"operations owner","updated_by":"intake-agent","updated_at":"2026-10-19T13:36:39Z","canonical_path":"docs/intake/ops-32-f4238c14ac02/HANDOFF.md","approval":"owner_confirmed"}}
```

This is the canonical intake record for original request OPS-32 and original goal “Weekly aggregate room usage.” The operations owner directly authorized this handoff and the stated desired behavior.

## Intent & Outcomes

Facilities needs a dependable aggregate view of room usage delivered weekly, without retaining personal identifiers.

- R1 — owner-confirmed (E1; S1, D1): produce an aggregate weekly room-usage report for Facilities each Monday at 09:00 UTC.
- R2 — owner-confirmed (E1; S1, D2): never retain personal identifiers.
- R3 — owner-confirmed (E1; S1, D3): delivery by email to the facilities mailbox is accepted.
- R4 — owner-confirmed (E1; G1, G2, D4): treat actual data and integration capability as nonblocking research gaps for the automation factory.

Success measures beyond correct schedule, aggregate scope, accepted delivery channel, and prohibition on retaining personal identifiers are unknown and are not required to begin domain acquisition.

## Current State & Evidence

```json
{"evidence":[{"id":"E1","claim":"The operations owner requires an aggregate weekly room-usage report for Facilities every Monday at 09:00 UTC, prohibits retention of personal identifiers, accepts email delivery to the facilities mailbox, and assigns actual data and integration capability as nonblocking research gaps for the automation factory.","kind":"desired","class":"direct","source":"conversation:USER-REQUEST","authority":"operations owner","observed_at":"2026-10-19T13:36:39Z"}]}
```

No existing data source, integration, report implementation, or current delivery behavior was asserted or inspected. E1 establishes desired behavior only.

## Actors & Scenarios

```json
{"scenarios":[{"id":"S1","actor":"Facilities","goal":"Receive an aggregate weekly room-usage report","trigger":"Each Monday at 09:00 UTC","preconditions":"The automation factory has acquired a usable room-usage data source and an operational email integration for the facilities mailbox.","main_path":"The future automation obtains the relevant weekly room-usage data, aggregates it without retaining personal identifiers, and emails the report to the facilities mailbox at the scheduled time.","alternatives":["Email is the accepted delivery channel; any alternative channel requires a new owner decision."],"failures":["Required room-usage data is unavailable or unsuitable for aggregation.","The facilities mailbox or email integration is unavailable.","Processing would retain a personal identifier, in which case delivery must not proceed through that noncompliant path."],"postconditions":"Facilities has the weekly aggregate report, and no personal identifiers have been retained.","rules":["R1: Deliver the aggregate weekly room-usage report each Monday at 09:00 UTC (E1).","R2: Never retain personal identifiers (E1).","R3: Email delivery to the facilities mailbox is accepted (E1)."],"status":"confirmed","sources":["E1"]}]}
```

S1 is the representative desired journey. Concrete source systems, aggregation definitions, reporting interval boundaries, and integration mechanics remain acquisition work rather than intake decisions.

## Scope & Exclusions

In scope: the desired weekly aggregate room-usage report, its Facilities beneficiary, Monday 09:00 UTC schedule, prohibition on retaining personal identifiers, accepted email delivery, and research routing for missing data/integration facts.

Out of scope: implementing automation, selecting a stack, initializing planning, contacting Facilities, sending email, or asserting that any data source or integration is operational. No other output artifact is authorized. The handoff does not authorize downstream execution.

## Constraints & Dependencies

The schedule is fixed at Monday 09:00 UTC (R1). Personal identifiers must never be retained (R2); downstream acquisition must determine a compliant aggregation path before implementation. Email to the facilities mailbox is an accepted delivery choice (R3), but mailbox details and operational access are not established. A usable room-usage source and working delivery integration are dependencies whose availability is intentionally nonblocking at intake (R4; G1, G2).

## Decisions & Assumptions

```json
{"decisions":[{"id":"D1","statement":"The report cadence is weekly, with delivery each Monday at 09:00 UTC.","status":"accepted","origin":"operations owner request","authority":"operations owner","sources":["E1"],"consequence":"The automation factory must preserve this schedule when assessing feasibility."},{"id":"D2","statement":"Personal identifiers must never be retained.","status":"accepted","origin":"operations owner request","authority":"operations owner","sources":["E1"],"consequence":"Data handling and aggregation approaches that retain personal identifiers are excluded."},{"id":"D3","statement":"Email to the facilities mailbox is an accepted delivery channel.","status":"accepted","origin":"operations owner request","authority":"operations owner","sources":["E1"],"consequence":"The automation factory may investigate email delivery without reopening the channel decision."},{"id":"D4","statement":"Actual data and integration capability are nonblocking research gaps for the automation factory.","status":"accepted","origin":"operations owner request","authority":"operations owner","sources":["E1"],"consequence":"Intake can be ready while G1 and G2 remain open; capability must not be invented."}]}
```

No technical architecture, data source, report format, aggregation formula, mailbox address, or integration provider is assumed.

## Open Gaps & Owners

```json
{"gaps":[{"id":"G1","type":"repo_fact","question":"What actual room-usage data is available, where is it sourced, what period does a weekly report cover, and can it support aggregation without retaining personal identifiers?","impact":"Determines report feasibility, compliant data handling, and the precise aggregation semantics.","blocking":false,"state":"open","owner":"automation factory","route":"Inspect authorized consumer-system documentation, configurations, schemas, and sample metadata; obtain Facilities-owned definitions where repository evidence is insufficient, without ingesting personal identifiers into the handoff.","depends_on":[],"sources":["E1"]},{"id":"G2","type":"repo_fact","question":"What operational integration capability exists for scheduled email delivery to the facilities mailbox?","impact":"Determines whether and how the accepted delivery route can be implemented.","blocking":false,"state":"open","owner":"automation factory","route":"Inspect authorized integration configuration and capability documentation, then verify mailbox addressing and access with the accountable system owner before implementation.","depends_on":[],"sources":["E1"]}]}
```

Both gaps are deliberately nonblocking for domain acquisition. They remain open facts and must not be treated as confirmed capabilities.

## Context Pointers

The authoritative source for desired behavior is E1 (`conversation:USER-REQUEST`). No consumer-workspace PRD, use case, ADR, data contract, or integration specification was identified as an authoritative pointer during this bounded intake.

## Readiness & Next Handoff

```json
{"readiness":{"status":"ready_for_domain_acquisition","sufficiently_known":"The accountable owner, Facilities beneficiary, aggregate weekly reporting outcome, Monday 09:00 UTC schedule, no-personal-identifier-retention prohibition, accepted email channel, exclusions, and research ownership are established.","next_receiver":"automation factory","actions":["Acquire evidence for G1 about available room-usage data, weekly aggregation semantics, and compliant handling without retaining personal identifiers.","Acquire evidence for G2 about operational scheduled-email capability and the facilities mailbox integration."],"limitations":["No actual room-usage data source has been confirmed.","No email or scheduling integration has been confirmed operational.","Report format and detailed aggregation semantics are not yet established.","This handoff does not authorize automation implementation or planning initialization."]}}
```

The handoff is ready for the automation factory’s bounded domain acquisition. G1 and G2 are explicit nonblocking research gaps; downstream work must verify them without interpreting this record as implementation authorization.
