# Shared Context Intake — Plugin Build Contract

**Contract status:** Canonical implementation, tooling and packaging contract (2026-10-19); **not** proof of Behavioral Success, successful installation, or release certification.  
**Owner intent source:** [`GOAL_AND_USE_CASES.md`](GOAL_AND_USE_CASES.md). The contract supplements that file; where statements conflict, retain the conflict and request the affected owner decision instead of silently choosing.

## 1. Product outcome and boundary

- **Product identity:** Shared Context Intake, a reusable domain-neutral capability upstream of specialized Software, n8n, UI/UX, and future factory context acquisition. Its current authored entry is `skills/context-intake/SKILL.md`.
- **Problem solved:** Recover known facts, frame owner intent/actors/scenarios, classify requirements and consequential gaps, question the correct decision owner proportionately, and issue one evidence-linked downstream intake handoff. Do not re-interview for known accepted choices.
- **Canonical runtime output:** exactly one `docs/intake/<stable-request-slug>/HANDOFF.md` in the **consumer project** when writing has been authorized, following `skills/context-intake/assets/HANDOFF.md` and `handoff.schema.json` version `1.0.0`. Existing `skills/context-intake/scripts/intake.py` supports deterministic identity, initialization, validation and guarded updates.
- **Outside product scope:** domain-specific full source ingestion, architecture/tech-stack selection, code feature implementation, creation of n8n flows, UI reconstruction, downstream QA, automatic downstream factory invocation, and installation of speculative services. Only relevant bounded read-only fact checks belong in shared intake.
- **Cost/security boundaries:** no Firecrawl credit consumption, unauthorized code/workspace mutation, silent global installation, unapproved external messages, or invented decisions or source access.

## 2. Reuse policy: build from the existing implementation

The committed/current repository and recorded owner decisions govern the current implementation; the clean ZIP remains a historical reference, not a replacement for newer local edits. Keep the 1-entry skill, references, versioned output template, validator/helper and augmented ledger intact unless a separately evidenced defect warrants a specific change. Do not replay all origin skills, re-run discovery, paste source instruction text, or convert all variants into always-on steps. Adapt the component layout only when the chosen host schema requires it. Previously authored manifests, packaging scripts and tests are **historical implementation evidence**: inspect what actually exists in the current working tree and reuse only the relevant authorized pieces. Do not overwrite newer local files with an older ZIP snapshot.

Sources already account for **442** distinct source records, **519** variant records, and **5** `blocked_unverified` entries; see `docs/coverage/coverage-summary.json` for exact IDs and reasons. Source-coverage status is **not** behavioral-test success.

## 3. Capability inventory and component ownership

| Capability | Current owner/artifact | Status/limitation |
| --- | --- | --- |
| Entry and mode routing | `skills/context-intake/SKILL.md`, `references/policy.md` | Present as authored instructions; behavioral pass not verified on clean snapshot |
| Context framing, questions, scenarios, provenance | `references/elicitation-methods.md`, `model-discovery.md`, `scenarios.md`, `coverage-*.md` | Authored references, loaded on demand; conditional variants remain conditional |
| Domain boundaries | `references/adapters.md` | References specialist systems, does **not** implement their integrations |
| Deterministic handoff contract | `assets/HANDOFF.md`, `assets/handoff.schema.json`, `references/contract.md` | Present; runtime truth/semantic quality requires separate evaluation |
| Local handoff helper | `skills/context-intake/scripts/intake.py` | Present; Python standard-library helper according to inherited README; tests not rerun here |
| Variant provenance | `docs/coverage/*` | 519 catalog entries; 5 blocked/unverified |
| Plugin packaging and host registration | Inspect current `plugin.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and any existing packaging scripts | Prior Codex transcript reports these files were created; current working-tree presence, validity, and completion require direct verification |
| Behavioral evaluation | `GOAL_AND_USE_CASES.md`, `evals/cases.yaml`, existing Promptfoo tool/plugin/CLI | 35 case specifications exist, but no approved executable Promptfoo suite and behavioral pass evidence established |

### Required runtime capabilities and existing tooling

| Runtime capability | Existing route to inspect | Required behavior / boundary |
| --- | --- | --- |
| Prior context and accepted decisions | Host conversation/context, existing consumer documents and handoff | Recover available relevant facts before asking; use permitted reads only |
| Bounded local/repo facts | Native filesystem/Git search; connected GitHub; Serena where actually callable | Read only the needed evidence; distinguish code facts from user decisions |
| Authoritative external documentation/facts | Existing web/official docs search; Context7 where actually callable | Resolve a consequential fact or record an evidence gap; no blanket research |
| Canonical HANDOFF | Existing `skills/context-intake/scripts/intake.py`, template and schema | Reuse the existing deterministic artifact contract; write only when authorized |
| Existing document connectors | Available and authenticated host-native/connected search, including Drive if present | Use only if relevant and permitted; do not assume a named connector is authenticated |

**User-confirmed local environment:** large tool installations already exist on the owner's Windows computer and are not uploaded with this Markdown bundle. **A missing upload is not evidence of a missing tool.** Identify installed/connected versions and effective capabilities from the actual target host before declaring a required capability missing. Prior Codex transcript demonstrates Serena project read and Context7 documentation lookup in that session, not verified general availability across every host/session. **REA and Repomix are delegated/specialist acquisition routes**, not automatically bundled or invoked by this pre-domain Skill. Do not bundle globally installed tools, duplicate native operations or invent an MCP server just to fill a manifest field.

**Authoring versus runtime tooling:** `@plugin-creator` and official host packaging/check tools are build/packaging tools; **Promptfoo** is a behavioral evaluation tool (existing plugin/tool/CLI where available), **not** a plugin-manifest validator. None becomes an always-on end-user skill behavior solely because it helped construct the plugin.

## 4. Distribution targets and portability

The owner intends reuse across **Codex/OpenAI, Cursor and Cline**, with Anthropic's Plugin Developer Toolkit considered as an authoring tool. Claude Code is a possible construction/testing host, not proof of universal runtime portability. Target host capability and compatibility are each unverified until the real installation/runtime probes for that host succeed.

- **Canonical source:** one upstream `skills/context-intake/` implementation, one versioned output contract, one requirements and evaluation catalog.
- **Host adapters:** only metadata/registration/routing needed for a target host; isolate these from the skill's domain-neutral behavioral rules. The exact on-disk manifest path/format is **host/version specific** and to be checked against official current schemas during implementation.
- **AGENTS.md:** the build-agent context router in this repository. Its existence alone does not prove automatic loading in every host; the host must be configured or explicitly instructed to read it. `SKILL.md` is the **runtime** entry and must not acquire build-stage authority.
- **Invocation:** explicit entry is preferred for reliable acceptance tests; implicit auto-selection is a separate measurable capability, never guaranteed.
- **Portability success:** equivalent required observable behavior and output contract, not byte-identical reasoning or model text.

## 5. Success criteria and approved mechanisms

### A. Behavioral Success — first

- Source of required behavior: `GOAL_AND_USE_CASES.md` (UC-01..UC-35) and relevant existing `SKILL.md` references. Preserve the source/variant ledger; it records method provenance, not an evaluation pass.
- Existing acceptance source: `evals/cases.yaml`, which contains **case specifications only**, not a runnable Promptfoo config. Each applicable UC must map to the actual Skill behavior/tool capability and report an evidenced `pass`, `fail`, `blocked`, or `not_run` in `docs/BUILD_STATE.md`.
- Tool: the **already available Promptfoo plugin/tool/CLI**, after its actual availability is checked. Only use **owner-authorized and independently reviewed** fixtures, provider invocation, assertions/oracles and release criteria. Do not create or execute new tests, probes, cases or an eval harness without express approval.
- Behavioral Success is **unverified** until this evidence exists. Do not use a parsed YAML file, a skill-coverage matrix or package existence as substitute evidence.

### B. Packaging Success — after Behavioral Success

- Source of the package: the **existing Skill and current repository artifacts**; use the installed `@plugin-creator`, its official instructions and current target-host manifest/installation checks. Reuse actual existing manifests, marketplace entries and scripts instead of recreating them.
- Scope: structural format, required file/resource references, declared tools/integrations, host registration and installation/invocation **as evidenced by official tooling** for each approved target host.
- For an authorized **post-install behavioral check**, use reviewed Promptfoo assets against the actual installed runtime. Keep that result separate from manifest integrity and installation status. Promptfoo does **not** certify package structure.
- **No self-authored `test_plugin.py`, `probe_codex.py`, mock runtime, extra test framework or repeated exploratory probes unless specifically authorized**. Historical tests may exist; do not repeat or treat them as passed without current evidence.
- Successful packaging of Codex is not proof of Cursor/Cline/Claude support. No installation, auth changes, publication or global dependency changes are implicitly authorized by this contract.

The owner's currently authorized stage is recorded in `docs/BUILD_STATE.md` and the most recent explicit request; this contract documents the stage gates but is not a standing permission to execute them.

## 6. External authoring toolkit handoff

When using Anthropic Plugin Developer Toolkit or any coding agent:
- Read `AGENTS.md` first; treat this contract and `GOAL_AND_USE_CASES.md` as binding **inputs**, not evidence to recreate from scratch.
- Inspect the current tree, host documentation and old packaging selectively. Reuse supported code and report only concrete missing components, constraints, host differences and decisions. Do not restart already completed discovery or run unrequested validation.
- Do not assume the Anthropic command can install or validate an OpenAI/Codex/Cursor/Cline plugin automatically. Each target needs explicit compatibility and E2E evidence.
- If a spec blocks the current goal, record it as a conflict in `docs/BUILD_STATE.md`; do not silently choose a stack, create a server, or claim completion.
- Never commit/push; owner owns Git publication.

## 7. Unresolved decisions and evidence (not inferred)

| ID | Required before | Status / how to resolve |
| --- | --- | --- |
| PD-01 | Final packaging strategy | Inspect the existing current manifests with the official creator/host documentation; Codex is the immediate target, other hosts require separate evidence and authorization |
| PD-02 | Actual tool integration config | Inspect the user-confirmed local installations and reachable connected tools in the selected host. Record required capability gaps; do not assume absent uploads imply absent tooling |
| PD-03 | Behavioral eval execution | Owner approval of independent Promptfoo fixtures, expected observations, host invocation and any execution; case catalog alone is insufficient |
| PD-04 | Final release certification | Owner-approved success thresholds and real evidence for each claimed host; do not invent release approval |

No missing fact above is to be silently filled with a plausible default.
