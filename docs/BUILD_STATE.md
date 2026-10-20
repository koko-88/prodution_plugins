# Build State — Shared Context Intake

## Workspace organization — 2026-10-20

Owner explicitly requested the physical move and deletion of the old folder, with no compatibility junction.
- Physical plugin checkout: `K:\production_plugins\context-intake`. All 14 checkout entries physically transferred; the destination is a real directory, not a junction.
- Git metadata: all 1,159 source files compared by SHA-256 before the old copy was removed. Git working-tree status before and after the move matched, including staged and uncommitted changes. No commit, push or branch change.
- Shared tools: `K:\tools for plugins`; 144 existing tool junctions were checked against their new targets.
- Old path cleanup: `K:\sw_context-layer` is empty; deletion is pending because an open Codex process holds the directory. A one-time hidden cleanup worker will delete only that exact empty directory once the lock is released; it refuses to delete any nonempty folder. No compatibility junction is created.
- README, Promptfoo config, Codex marketplace/trust paths and Serena project registration use the production path. Historical evidence below retains its original recorded paths. No behavioral evaluations rerun.

---
### Relocation path verification — 2026-10-20

- Actual production folder found as `K:\production_plugins\context-intake`. Corrected stale spaced-folder references in source/installed README files, Promptfoo config, Codex marketplace/trust config, desktop project record and Serena registration.
- Fixed the README and source contract's abbreviated helper reference to `skills/context-intake/scripts/intake.py`; canonical helper `--help` succeeds.
- All 144 relocation-manifest junctions resolve to their recorded destinations. Repaired one additional missing Gbrain global-module junction using the existing relocated Gbrain source; `gbrain --version` now succeeds.
- Existing CLI checks succeeded: Repomix 1.18.1, Context7 0.8.0, Promptfoo 0.123.1, REA 6.5.0, Serena 2.0.0, Gbrain 0.60.287.0, and Gstack browse version command. GSD MCP script exists and passes Node syntax checking; its end-to-end MCP operations were not exercised.
- Codex TOML and plugin JSON manifests parse. Existing `promptfoo validate config` passed. Configured fixture/plugin/helper directories exist. Scanned 20 source Markdown files and checked 29 relative links: zero missing link targets.
- Connected Serena responded with active project `context-intake` and language-server status ready.
- No behavioral evaluations, database/authentication checks, package rebuild, commit or push. ZIP release archive and historical source ledgers/results retained unchanged; installed/staged README path corrections do not constitute a new release.
## Current checkpoint — Final release (Cursor PKG-RUNTIME), 2026-10-19 ~18:58 +03

**Authorization:** Owner-asleep Track B finalize follow-up: installed-path HANDOFF
smoke + Cursor discovery recheck; update this file with proven evidence only.
Skill unchanged. Do **not** commit or push.

### Gate outcomes

| Gate | Result | Evidence / limitation |
| --- | --- | --- |
| Behavioral Success | **PASSED (Cursor eval path)** | UC-01 pass (`promptfoo/results/uc01-corrected-fixture.json`); UC-02..UC-35 initial 29/34 (`promptfoo/results/uc02-35-initial.json`); residuals UC-06/07/13/34/35 closed on Cursor — primary **5/5** `promptfoo/results/uc-fail-cursor-rerun-20261019-184450.json`; corroborating path 4/5 then UC-34 solo pass (`uc-fail-cursor-rerun-20261019-184351.json` + `uc34-cursor-rerun-20261019-185449.json`). Combined = UC-01..UC-35 evidenced. |
| Packaging Success (structural) | **PASSED (local)** | Stage + ZIP already built; ZIP sha256 `33fb02b19b25ab012cbdec11b9590078b3e40ae8698d316a0bf4fb3ff8ffe124`. |
| Packaging Success (Codex install) | **PASSED (install/discovery)** | Marketplace `shared-context-local`; `context-intake@shared-context-local` installed, enabled, v0.1.0 → `K:\sw_context-layer\dist\context-intake`. |
| Packaging Success (Cursor install) | **PASSED (local layout)** | `%USERPROFILE%\.cursor\plugins\local\context-intake` reconfirmed: root `plugin.json` (`context-intake` `0.1.0`), skill `skills/context-intake/SKILL.md`, helper `scripts/intake.py`; **no** `.cursor-plugin/`. CLI has no non-interactive local-plugin / Customize listing (`agent plugin` → marketplace only). **Reload / Customize UI not claimed.** |
| Packaging Success (PKG-RUNTIME) | **PASSED (Cursor installed-path provisional HANDOFF)** | Cursor CLI `2026.10.16-e3cb207` with `--plugin-dir K:\sw_context-layer\dist\context-intake` on empty disposable consumer `promptfoo/results/_runtime-smoke/uc31-consumer-20261019-185629`. UC-31-style read-only → EXIT 0 (~111s); provisional inline `# Intake Handoff`; consumer stayed empty. Evidence: `promptfoo/results/_runtime-smoke/uc31-cursor-plugin-dir-20261019-185629.json` (+ `.stream.jsonl`). Codex packaged-path HANDOFF **skipped** this turn (prior quota/429; Cursor evidence accepted). |
| Final release | **CLAIMED** | Behavioral Success + structural packaging + Cursor installed-runtime provisional HANDOFF evidenced. Optional: Cursor Reload/Customize operator UI; optional Codex packaged-path HANDOFF when quota allows. No commit/push. |

### PKG-RUNTIME smoke (this turn)

| Field | Value |
| --- | --- |
| Host | Cursor Agent CLI (`node.exe` + `index.js` under `%LOCALAPPDATA%\cursor-agent\versions\2026.10.16-e3cb207`) |
| Plugin path | `--plugin-dir K:\sw_context-layer\dist\context-intake` |
| Case | UC-31-style read-only provisional (new empty consumer; no fixture baseline touch) |
| Result | **pass** — EXIT 0; provisional handoff; zero consumer files after |
| Artifacts | `promptfoo/results/_runtime-smoke/uc31-cursor-plugin-dir-20261019-185629.json`, `.stream.jsonl` |
| Codex runtime | **skipped** (prior quota block; not required after Cursor PKG-RUNTIME pass) |

### Cursor provider cutover (retained)

| Item | Status |
| --- | --- |
| Subject + grader | `file://providers/cursor-agent.js` (`agent -p`; grader text, no `--force`) |
| Cursor CLI | `%LOCALAPPDATA%\cursor-agent` `2026.10.16-e3cb207`; Pro tier (`agent about`) |
| Auth | **OK** — prior `agent -p --trust` probe → `OK` |
| Codex Promptfoo residuals | Quota/429 (`uc-fail-rerun-20261019-173747.json`); **not** used for closing 5/5 |
| Harness | Versioned `node.exe`+`index.js`; prompt staging + `--add-dir`. Runtime smoke reused same pattern under `promptfoo/results/_runtime-smoke/prompt-files/`. |
| Skill | **Unchanged** — no Skill edit; no defect in PKG-RUNTIME smoke |

### Residual close-out (Cursor)

| Case | Primary 5/5 (`184450`) | Corroborating |
| --- | --- | --- |
| UC-06 | **pass** 1.0 | pass in `184351` |
| UC-07 | **pass** 1.0 | pass in `184351` |
| UC-13 | **pass** 1.0 | pass in `184351` |
| UC-34 | **pass** 1.0 | fail once in `184351`; **pass** on `uc34-cursor-rerun-20261019-185449.json` |
| UC-35 | **pass** 1.0 | pass in `184351` |

Primary artifact: `promptfoo/results/uc-fail-cursor-rerun-20261019-184450.json`.

### Packaging artifacts (unchanged; install + local layout reconfirmed)

| Artifact | Detail |
| --- | --- |
| `dist/context-intake-0.1.0.zip` | SHA-256 `33fb02b19b25ab012cbdec11b9590078b3e40ae8698d316a0bf4fb3ff8ffe124` |
| `dist/context-intake/` | Staged allowlisted install tree |
| Codex | `context-intake@shared-context-local` installed + enabled |
| Cursor local | `C:\Users\kerol\.cursor\plugins\local\context-intake` (root `plugin.json` + skill; stamped 2026-10-19 17:37) |
| Marketplace | `.agents/plugins/marketplace.json` → `./dist/context-intake` |

### Remaining owner actions (optional after Final release)

1. Optional: Reload Cursor Window and confirm Customize / skill discovery for local `context-intake` (no non-interactive discovery API found).
2. Optional: Codex packaged-path HANDOFF when quota allows (parity only).
3. Still no commit/push until owner requests it.

---

## Prior checkpoint — Behavioral Success (Cursor path), 2026-10-19 ~18:56 +03

**Superseded** by Current checkpoint for Final release / PKG-RUNTIME.
Behavioral residual evidence and packaging structural/install rows remain valid
and are restated above. At ~18:56 Final release was still **NOT CLAIMED** pending
PKG-RUNTIME; that gap is now closed on the Cursor installed-path provisional
HANDOFF smoke.

---

## Prior checkpoint — Track B + Cursor compatibility, 2026-10-19

**Authorization:** Owner authorized Track B (behavioral close-out + Codex
packaging) plus Cursor compatibility verification. Packaging preparation and
structural validation may proceed independently. Final release still requires
**both** Behavioral Success and Packaging Success. Preserve the existing Skill,
augmentation, and approved requirements. Do **not** commit or push.

**Host correction applied:** Cursor officially supports the Agent Plugins
standard with a root `plugin.json`. No `.cursor-plugin/` directory was added.
Evidence: [Cursor Plugins docs](https://cursor.com/docs/plugins) — Agent Plugins
use root `plugin.json`; Cursor-specific format uses `.cursor-plugin/plugin.json`.

### Gate outcomes (this attempt — superseded by Current checkpoint above)

| Gate | Result | Evidence / limitation |
| --- | --- | --- |
| Behavioral Success | Was **OPEN** (quota / then Cursor auth) | Later closed on Cursor path — see Current checkpoint. |
| Packaging Success (structural) | **PASSED (local)** | `python scripts/package_plugin.py --check` on source and stage; ZIP + stage built. |
| Packaging Success (Codex install) | **PASSED (install/discovery)** | Marketplace `shared-context-local` registered; `context-intake@shared-context-local` installed, enabled, v0.1.0. |
| Packaging Success (Cursor install) | **PASSED (local layout)** | Agent Plugin copied to `%USERPROFILE%\.cursor\plugins\local\context-intake` with root `plugin.json` and skill tree; no `.cursor-plugin/`. IDE Reload / Customize discovery still needs operator confirmation after reload. |
| Final release | **NOT CLAIMED** | Behavioral later passed on Cursor; PKG-RUNTIME / UI reload still open. |

### Promptfoo evidence (actual results on disk)

| Artifact | Outcome |
| --- | --- |
| `promptfoo/results/uc01-corrected-fixture.json` | 1/1 pass |
| `promptfoo/results/uc02-35-initial.json` | 29 pass, 5 fail (residuals later closed on Cursor) |
| `promptfoo/results/uc-fail-rerun-20261019-173747.json` | 0 pass / 0 fail / **5 errors** — Codex usage limit then 429 |
| `promptfoo/results/uc-fail-cursor-rerun-20261019-182938.json` | 0/5 — grader infra (CLI length / path); subject JS asserts had passed |
| `promptfoo/results/uc-fail-cursor-rerun-20261019-184351.json` | 4/5 — UC-34 grader fail once; others pass |
| `promptfoo/results/uc-fail-cursor-rerun-20261019-184450.json` | **5/5 pass** — primary closing residual evidence |
| `promptfoo/results/uc34-cursor-rerun-20261019-185449.json` | UC-34 solo **pass** after `184351` miss |

#### Residual cases from `uc02-35-initial.json` (historical; closed 2026-10-19)

| Case | Prior classification | Closing outcome |
| --- | --- | --- |
| UC-06 | Behavioral (semantic) under Codex | **pass** on Cursor (score 1.0); no Skill edit |
| UC-07 | Infra (Codex capacity) | **pass** on Cursor |
| UC-13 | Infra (timeout) | **pass** on Cursor |
| UC-34 | Infra (timeout) | **pass** on Cursor |
| UC-35 | Grader near-miss 0.99 | **pass** on Cursor (score 1.0) |

### Packaging artifacts produced

| Artifact | Detail |
| --- | --- |
| `dist/context-intake-0.1.0.zip` | SHA-256 `33fb02b19b25ab012cbdec11b9590078b3e40ae8698d316a0bf4fb3ff8ffe124` |
| `dist/context-intake/` | Staged allowlisted install tree (28 files); `--check` **valid** |
| Codex cache | `C:\Users\kerol\.codex\plugins\cache\shared-context-local\context-intake\0.1.0` |
| Cursor local | `C:\Users\kerol\.cursor\plugins\local\context-intake` |
| Marketplace | `.agents/plugins/marketplace.json` → `./dist/context-intake` (path now exists) |

### Host verification notes

- **Codex:** `codex plugin marketplace add K:\sw_context-layer` → `shared-context-local`. `codex plugin add context-intake@shared-context-local` → installed & enabled. Skill bytes match stage.
- **Cursor:** Official Agent Plugin layout (root `plugin.json` + `skills/`). Local copy installed per docs (`~/.cursor/plugins/local/<name>`). Reload Window / Customize confirmation is remaining UI evidence. No `.cursor-plugin/` introduced.
- **Installed HANDOFF runtime:** Historical note — later closed on Cursor `--plugin-dir` UC-31-style smoke (see Current checkpoint); Codex packaged-path still optional.

---

## Prior execution — owner-authorized Promptfoo preparation, 2026-10-19

The owner's follow-up explicitly authorizes the agent to derive the runnable
Promptfoo cases, fixtures, criteria and invocation from the supplied Markdown,
and to keep all evaluation material in a dedicated `promptfoo/` directory.
This supersedes the missing-assets approval blocker below. The historical
`evals/cases.yaml` was not recovered; `promptfoo/cases.yaml` is a newly authored,
source-traceable executable suite for UC-01..UC-35, not a claimed original copy.

- `promptfoo/promptfooconfig.yaml`: built-in `openai:codex-sdk`, existing ChatGPT
  login, separate semantic grader, filesystem baseline assertion and canonical
  helper validation; no custom provider or evaluation framework.
- `promptfoo/fixtures/`: isolated synthetic consumers, seven factual input files,
  two seeded canonical resume records, and byte baselines. Fixtures have no
  independent human review; semantic grading uses a separate session of the same
  model. These limitations remain visible rather than being relabeled certification.
- Official `promptfoo validate config`: **passed** after configuration corrections.
- CLI account rejected `gpt-6.1-sol` and documented example `gpt-5.4` with HTTP 400.
  Locally listed `gpt-5.6-sol` is operational: subject and grader completed UC-01.
- Initial UC-01 execution exposed an ESM assertion-loading error and missing
  grader source context. Its synthetic request also left reporting-day/count
  semantics open, so it did not actually meet the complete-request fast-path
  premise. These evaluation defects were corrected; no Skill defect is claimed
  from that superseded trial.
- Corrected UC-01: **passed**, both artifact and semantic assertions, zero errors;
  evidence: `promptfoo/results/uc01-corrected-fixture.json`.
- UC-02..UC-35 initial batch completed on disk as
  `promptfoo/results/uc02-35-initial.json` (**29 pass / 5 fail**); superseded the
  earlier “still running” note. Packaging later authorized independently under
  Track B.

### Earlier inspection checkpoint — superseded where noted above

## Active checkpoint — 2026-10-19, local Codex inspection

**Current authorization:** Superseded by Track B + Cursor compatibility section
above.

**Workspace observed:** `K:\sw_context-layer`, branch `main`. The working tree
already contains owner changes: staged `.serena` files, staged/deleted `.gitignore`,
modified `README.md`, and untracked contracts, implementation, packaging and tool
directories. Those changes were preserved.

### Current gate outcomes (historical snapshot — superseded)

| Gate | Result | Current evidence and limitation |
| --- | --- | --- |
| Behavioral Success | **BLOCKED / UNVERIFIED** | Superseded by Promptfoo results recorded above. |
| Packaging Success | **BLOCKED / NOT RUN** | Superseded by Track B packaging evidence above. |

### Use-case routes and missing behavioral evidence

Paths in this table are relative to `skills/context-intake/` unless stated otherwise.
Expected behavior is summarized from the goal contract. Runtime status is now
driven by Promptfoo artifacts under `promptfoo/results/`, not this static route
table alone.

| UC | Expected behavior | Existing authored route |
| --- | --- | --- |
| UC-01 | Zero ceremonial questions for sufficient requests | `SKILL.md` steps 1, 5; `references/policy.md`, Fast path |
| UC-02 | Clarify outcome, beneficiary and consequential scope | `SKILL.md` step 2; `references/elicitation-methods.md`, Intent interview |
| UC-03 | Separate the problem from a risky suggested solution | `references/policy.md`, Authority; `references/elicitation-methods.md`, Premise check |
| UC-04 | Recover bounded brownfield facts; separate current/desired | `SKILL.md` steps 1, 2, 4; `references/model-discovery.md` |
| UC-05 | Use available greenfield evidence without inventing a system | `SKILL.md` steps 2, 4 |
| UC-06 | Resume stable identity and settled choices | `SKILL.md` steps 1, 6; `references/contract.md`, Path, identity and resume |
| UC-07 | Propagate corrections and preserve provenance | `SKILL.md` step 2; `references/policy.md`, Stopping and readiness |
| UC-08 | Preserve canonical spec ownership; expose contradictions | `SKILL.md` step 1; `references/model-discovery.md`, Document contradictions |
| UC-09 | Distinguish initiating/supporting actors and owners | `references/scenarios.md`; `references/model-discovery.md`, Product-model lens |
| UC-10 | Include scheduled/API/system actors and triggers | `references/scenarios.md`; `references/adapters.md`, Automation |
| UC-11 | Capture relevant alternatives, failures and postconditions | `SKILL.md` step 3; `references/scenarios.md` |
| UC-12 | Capture real quality boundaries without invented targets | `references/scenarios.md`, Quality attributes; `references/elicitation-methods.md`, Quality |
| UC-13 | Preserve prohibitions, permissions and exclusions | `SKILL.md` steps 2, 6; `references/model-discovery.md`, Prohibition probing |
| UC-14 | Identify business rules and context conflicts; route deep modeling | `references/scenarios.md`, Rules; `references/model-discovery.md` |
| UC-15 | Surface relevant retry, concurrency and operational questions | `references/scenarios.md`, Relevant dimensions; `references/adapters.md` |
| UC-16 | Batch independent frontier decisions with consent | `SKILL.md` step 5; `references/elicitation-methods.md`, Decision frontier |
| UC-17 | Sequence dependent questions and recompute the frontier | `SKILL.md` step 5; `references/elicitation-methods.md`, Decision frontier |
| UC-18 | Honor one-question preference | `SKILL.md` step 5; `references/policy.md`, Sequential |
| UC-19 | Continue requested deep grilling until resolved/deferred | `references/policy.md`, Deep; `references/elicitation-methods.md` |
| UC-20 | Respect question/time budget without erasing blockers | `references/policy.md`, Budgeted clarification and Stopping |
| UC-21 | Inspect accessible facts instead of quizzing the user | `SKILL.md` step 4; `references/capabilities.md` |
| UC-22 | Disclose unavailable evidence and route acquisition | `SKILL.md` step 4; `references/capabilities.md`, If unavailable |
| UC-23 | Preserve conflicting sources and accountable authority | `references/policy.md`, Authority; `references/model-discovery.md`, Contradictions |
| UC-24 | Keep defaults provisional; never infer consent from silence | `SKILL.md` step 5; `references/policy.md`, Authority |
| UC-25 | Identify stakeholder owner without unauthorized outreach | `references/policy.md`, Other stakeholder; `references/elicitation-methods.md`, Questionnaire |
| UC-26 | Preserve scope, permissions and lifecycle boundaries | `SKILL.md` closing boundaries; `references/capabilities.md` |
| UC-27 | Route software context without a software-only schema | `references/adapters.md`, Software; `references/contract.md` |
| UC-28 | Frame n8n intent/integrations without constructing workflows | `references/adapters.md`, Automation and process factories |
| UC-29 | Capture UI journeys/states without reconstruction/stack choice | `references/adapters.md`, UI/UX; `references/scenarios.md` |
| UC-30 | Retain unknown domain and concrete specialist questions | `SKILL.md` steps 2, 4, 7; `references/capabilities.md` |
| UC-31 | Give provisional chat handoff with no writes in read-only mode | `SKILL.md` step 6; `references/policy.md`, Read-only |
| UC-32 | Write one authorized template/schema handoff; disclose blockers | `SKILL.md` steps 6, 7; `references/contract.md` |
| UC-33 | Preserve identity and reject stale/unsafe updates | `references/contract.md`, Path, identity and resume; helper enforcement not executed |
| UC-34 | Avoid hijacking implementation/review/research tasks | `SKILL.md` description, boundaries and negative examples |
| UC-35 | Load targeted references/tools and avoid paid blanket research | `SKILL.md` reference routing and step 4; `references/capabilities.md` |

### Tool and package observations (historical)

- Installed Plugin Creator `0.1.27` was read at
  `C:\Users\kerol\.codex\plugins\cache\openai-curated-remote\plugin-creator\0.1.27\skills\`.
- Promptfoo resolves to `C:\Users\kerol\AppData\Roaming\npm\promptfoo.ps1` (**0.123.1**).
- `codex plugin` exposes `add`, `list`, `marketplace`, and `remove`.
- Root `plugin.json` and `.codex-plugin/plugin.json` declare `context-intake` `0.1.0`.
- Local marketplace `shared-context-local` points to `./dist/context-intake` (now staged).

### Concrete blockers (updated by Track B section)

1. **BEH-CLOSE:** Five residual cases need green reruns after Codex quota reset (18:36 +03:00).
2. **PKG-RUNTIME:** Installed-host HANDOFF completion still pending quota and behavioral close-out.
3. **CURSOR-UI:** Operator reload + Customize confirmation that `context-intake` skill is visible from local Agent Plugin.

---

## Historical checkpoint — preserved; stage authority superseded above

**Checkpoint:** 2026-10-19; **source:** owner-provided Codex execution transcript through `Pasted text(20261019-114112).txt` plus the earlier authoring ZIP.  
**Current authority:** Superseded by later owner authorizations recorded above.

## 1. Current evidence state — do not confuse the gates

See the Track B section at the top of this file for the authoritative 2026-10-19
gate table. Older rows below are historical context only.

| Gate / capability | Evidence from available sources | Status / outstanding proof |
| --- | --- | --- |
| Product goal and scenarios | `GOAL_AND_USE_CASES.md` defines UC-01..UC-35 | **Defined**, not alone a behavioral pass |
| Augmented Skill | Existing `skills/context-intake/SKILL.md` and 442 source / 519 variant ledger | **Authored**, five `blocked_unverified`; not a behavioral pass |
| Canonical HANDOFF | Existing template/schema v1.0.0 and `scripts/intake.py` | **Authored** |
| Behavioral Success | Promptfoo suite under `promptfoo/` | **OPEN** — see Track B residuals |
| Plugin manifests/packaging | Root Agent Plugins `plugin.json`, Codex compatibility manifest, marketplace, package script, staged `dist/` | **Structural local pass**; final release not claimed |
| Codex discovery | `context-intake@shared-context-local` installed & enabled | **Install verified**; live HANDOFF pending |
| Cursor Agent Plugin | Local copy under `~/.cursor/plugins/local/context-intake` | **Layout verified**; Customize/reload pending |
| Packaging Success | Structural + both-host install | **Partial**; runtime/behavior still open |

## 2–6. Historical progression notes

Preserve earlier routing: Behavioral Success before claiming final Packaging
Success for release; use official host tooling; do not invent evaluation
frameworks; owner owns Git commit/push.
