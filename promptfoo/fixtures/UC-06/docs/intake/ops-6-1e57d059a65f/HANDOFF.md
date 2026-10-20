# Intake Handoff

## Identity & Stage

Existing canonical record; preserve original request identity.

```json
{"identity": {"id": "OPS-6", "request_key": "1e57d059a65fabd16162ffeae0939f3ffc1033debd018d4f52328e7558ad6a5e", "slug": "ops-6-1e57d059a65f", "canonical_path": "docs/intake/ops-6-1e57d059a65f/HANDOFF.md", "schema_version": "1.0.0", "domain": "automation", "scope": "Weekly aggregate room usage", "status": "ready_for_domain_acquisition", "owner": "operations owner", "updated_by": "operations owner", "updated_at": "2026-10-19T08:00:00Z", "approval": "owner_confirmed"}}
```

## Intent & Outcomes

R1: Weekly aggregate room usage for facilities; owner-confirmed E1, S1, D1.

## Current State & Evidence

The owner decision is desired behavior, not observed implementation.

```json
{"evidence": [{"id": "E1", "claim": "Owner accepted email to facilities each Monday at 09:00 UTC, with no personal identifiers.", "kind": "desired", "class": "direct", "source": "conversation:original-owner-decision", "authority": "operations owner", "observed_at": "2026-10-19T08:00:00Z"}]}
```

## Actors & Scenarios

Facilities consumes the scheduled aggregate report in S1.

```json
{"scenarios": [{"id": "S1", "actor": "facilities operator", "goal": "Review aggregate room usage", "trigger": "Monday 09:00 UTC", "preconditions": "Aggregate data is available", "main_path": "Scheduled process sends aggregate report by email", "alternatives": [], "failures": ["Delivery policy remains a nonblocking acquisition question"], "postconditions": "Facilities receives the weekly aggregate report", "rules": ["R1: Never retain personal identifiers (E1)"], "status": "confirmed", "sources": ["E1"]}]}
```

## Scope & Exclusions

Aggregate reporting only. No personal identifiers and no application implementation.

## Constraints & Dependencies

R1 privacy boundary applies; implementation facts remain G1.

## Decisions & Assumptions

D1 is accepted with original owner provenance.

```json
{"decisions": [{"id": "D1", "statement": "Use email each Monday at 09:00 UTC; never retain personal identifiers.", "status": "accepted", "origin": "original owner decision", "authority": "operations owner", "sources": ["E1"], "consequence": "Automation acquisition preserves schedule and privacy."}]}
```

## Open Gaps & Owners

G1 is nonblocking research owned by the automation factory.

```json
{"gaps": [{"id": "G1", "type": "repo_fact", "question": "Which existing data and email integration is available?", "impact": "Implementation route needs evidence; intake framing is sufficient.", "blocking": false, "state": "open", "owner": "automation factory", "route": "Inspect the consumer integration contracts during domain acquisition.", "depends_on": [], "sources": ["E1"]}]}
```

## Context Pointers

Original owner statement: conversation:original-owner-decision.

## Readiness & Next Handoff

Ready for bounded domain acquisition, not implementation or release.

```json
{"readiness": {"status": "ready_for_domain_acquisition", "sufficiently_known": "Owner, outcome, representative scenario and boundaries are established.", "next_receiver": "automation factory", "actions": ["Acquire integration and delivery-failure evidence."], "limitations": ["Integration facts are not verified."]}}
```

