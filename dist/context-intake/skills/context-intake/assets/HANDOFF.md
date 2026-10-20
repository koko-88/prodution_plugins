# Intake Handoff

## Identity & Stage

```json
{"identity":{"id":"REQUEST-ID","schema_version":"1.0.0","request_key":"REPLACE-REQUEST-KEY","slug":"REPLACE-SLUG","domain":"unknown","scope":"Describe the bounded request","status":"blocked_evidence","owner":"unassigned","updated_by":"intake-agent","updated_at":"2026-10-18T00:00:00Z","canonical_path":"docs/intake/REPLACE-SLUG/HANDOFF.md","approval":"not_requested"}}
```

Use the helper to populate identity. A summary does not establish owner approval.

## Intent & Outcomes

State desired outcome, beneficiaries and current pain. Capture each explicit requirement with a stable R-ID, source E-ID, confirmed/proposed/unknown status and related scenario/decision/gap IDs. Mark unknown measures and why.

## Current State & Evidence

```json
{"evidence":[]}
```

Distinguish observed behavior from desired behavior; add evidence with source, authority and freshness.

## Actors & Scenarios

```json
{"scenarios":[]}
```

Capture a representative actor goal and relevant alternatives/failures, or explicitly state not applicable with reason.

## Scope & Exclusions

State in scope, out of scope, prohibitions and deferred choices. Preserve all stated requirements across the end-to-end journey, including cross-domain boundaries; explain each material exclusion.

## Constraints & Dependencies

State genuine constraints and dependencies, or not applicable with reason.

## Decisions & Assumptions

```json
{"decisions":[]}
```

Record accepted decisions with authority/origin; keep defaults, proposals and contradicted assumptions labeled.

## Open Gaps & Owners

```json
{"gaps":[{"id":"G1","type":"repo_fact","question":"What evidence and intent are established?","impact":"The acquisition request cannot yet be framed.","blocking":true,"state":"open","owner":"intake-agent","route":"Recover the user's request and accessible authoritative sources.","depends_on":[],"sources":[]}]}
```

Classify remaining unknowns and their consequences. Resolved entries may remain as history.

## Context Pointers

Link authoritative deeper documents and external references. Keep existing canonical specs intact.

## Readiness & Next Handoff

```json
{"readiness":{"status":"blocked_evidence","sufficiently_known":"No completed intake yet.","next_receiver":"intake-agent","actions":["Recover and classify established context."],"limitations":["Template initialization is not semantic completion."]}}
```

Explain what is sufficiently known, who acquires what next, and why unresolved gaps do or do not block.
