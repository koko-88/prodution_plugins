# Scenario and quality lenses

Start with the actor's goal and a concrete episode. Actors include the beneficiary,
operator, administrator, external system, API client and scheduled job where
relevant. Distinguish the initiating actor from supporting participants. Do not
invent personas or force human UI journeys onto system processes.

Give each material scenario an ID. Capture: actor/goal; trigger; preconditions;
normal sequence; alternatives; failure and recovery; resulting state/postconditions;
applicable rule IDs; evidence IDs; proposed versus confirmed status. A short case
may express this in a few sentences; expand only when consequences justify it.

Probe only relevant dimensions: absent/invalid input, permission boundaries,
duplicate delivery, retry/idempotency expectations, concurrent work, partial
completion, rate limits, timeouts, cancellation, stale state, time zones and
scheduled execution. Ask who decides the desired policy; inspect/research the
actual limits. Do not prescribe retry algorithms or architecture during intake.

For business-rule ambiguity, use a small **Story -> Rules -> Examples -> Questions**
map, assigning stable IDs and linking unanswered questions to gap owners. Keep a
counterexample when it exposes a boundary. This adapts [Cucumber Example
Mapping](https://cucumber.io/docs/bdd/example-mapping/); no Cucumber installation,
Gherkin conversion or executable test suite is required.

For consequential quality attributes, identify the stakeholder and operational
context before asking for thresholds. Use stimulus, affected subject, environment,
desired response and measurable response criteria where known. Record unknown
criteria as gaps; label suggested numbers as proposals. The [SEI Quality Attribute
Workshop](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/)
supports stakeholder prioritization before architecture; [arc42 quality
scenarios](https://docs.arc42.org/section-10/) supply the compact scenario form.
This is a lens, not a mandatory architecture workshop.

For event-heavy cross-system processes, map a few actual past-tense domain events
in sequence, then actors/commands, policy reactions, boundaries and unanswered
hotspots. Preserve competing timelines. Adapt [EventStorming's collaborative
exploration](https://www.eventstorming.com/) without installing a tool, running a
full workshop automatically or assuming an event-driven implementation.

Synthetic examples help expose a missing dimension; they never prove production
frequencies, business rules or user approval. Label them proposed and route
empirical claims to validation. A reported bug uses the same lens: current versus
expected behavior, minimal trigger, affected actors, impact and evidence freshness.
