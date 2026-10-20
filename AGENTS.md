# AGENTS.md — Reusable Plugin Build Context Router

This file is a **navigation entry point**, not the implementation specification, runtime Skill, test plan, or historical build log. Any coding agent (including Codex, Cursor, Cline, or Claude) must read it explicitly if its host does not automatically load it. Follow only the files relevant to the current stage; do not preload every reference.

## 1. Resume and identify the stage

Read **`docs/BUILD_STATE.md` first**. Check its recorded state against the actual repository before relying on it. Determine what is already implemented, what is still missing, the last owner-authorized scope, and any blockers. Do not infer completion from the presence of files, and do not hard-code the current stage in this router.

The required progression is **Behavioral Success → Packaging Success**. Do not silently treat one as proof of the other. A stage can advance only on its recorded evidence and the owner's authorization.

## 2. Behavioral Success — understand and cover the use cases first

Read in this order:

1. **`GOAL_AND_USE_CASES.md`** — product goal, scope, constraints, and the specified user scenarios.
2. **The existing runtime `SKILL.md`** — locate its exact path from `docs/BUILD_STATE.md` or the repository; improve existing behavior rather than recreate it.
3. **The Skill’s `references/`** — load only references needed for a specific behavioral gap; use its index when present.
4. **`evals/cases.yaml`** — existing use-case acceptance specifications, if present; this project's catalog is **not an executable Promptfoo configuration** and is not evidence of passed evaluations.
5. **The existing HANDOFF contract** — inspect the Skill's `assets/HANDOFF.md`, `assets/handoff.schema.json`, `references/contract.md`, and `scripts/intake.py` only where a use case depends on output correctness or handoff behavior.
6. **`docs/coverage/`** — consult the source/variant ledger, if present, only when tracing a specific method or unresolved variant; catalog coverage is not a behavioral pass.

For every in-scope use case, establish the expected behavior, where the existing Skill covers it, what remains missing, and what actual evidence supports the result. Record confirmed outcomes and unresolved gaps in `docs/BUILD_STATE.md` when updates are authorized. **Do not declare Behavioral Success just because the Skill, scenarios, or coverage ledger exists.**

**Behavioral evaluation tool: Promptfoo.** When this stage is authorized for evaluation, use an existing connected Promptfoo tool/plugin or the locally available **Promptfoo CLI** (verify which is accessible). Inspect any existing Promptfoo-compatible configuration and reviewed fixtures/oracles before running it. Use the owner-approved `GOAL_AND_USE_CASES.md` and `evals/cases.yaml` to determine the required cases and assertions; **do not pass `evals/cases.yaml` directly to `promptfoo eval` as though it were runnable**. If the required config, independently reviewed fixtures, provider/host invocation, or authorization is missing, record that exact gap in `docs/BUILD_STATE.md` instead of improvising a harness or claiming success.

**Do not invent, generate, or run tests, fixtures, probes, or an evaluation framework without explicit authorization.** Use only the reviewed evaluation assets and scope the owner approved. If evidence is missing, mark Behavioral Success **unverified**, not passed.

## 3. Packaging Success — only after Behavioral Success

Read in this order:

1. **`PLUGIN_CONTRACT.md`** — required package components, intended tools, integration boundaries, and target host(s).
2. **`docs/BUILD_STATE.md`** — the completed behavioral checkpoint and remaining packaging work.
3. **The installed `@plugin-creator` instructions and current official documentation for each authorized target host** — use the existing supported creator and packaging mechanisms instead of inventing them.
4. **Existing manifests, packaging artifacts, packaging/install scripts, and actual installed/connected tool inventory** — inspect only those found in the repository (for example, `plugin.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `scripts/package_plugin.py`, or `scripts/install_skill.py`, when present). Reuse them and distinguish a locally installed tool from one that is configured, accessible, and operational in the target host.
5. **`README.md`**, when present — consult existing install/invocation instructions and avoid drafting a competing procedure.
6. **Existing approved Promptfoo evaluation assets**, if any — consult them only for an authorized post-install functional evaluation; do not treat the use-case catalog as a ready-to-run Promptfoo suite.

Use an existing, suitable, documented packaging tool or Skill. If the contract has not settled a required tool or its integration, identify that exact gap and obtain the owner's decision; **do not choose, install, or bundle a new tool by assumption**. Packaging does not justify rewriting the Skill or performing downstream domain work.

**Packaging validation tools:** use the installed `@plugin-creator` and the target host's existing official packaging/manifest/install checks for *structural* packaging evidence. Use **Promptfoo (connected tool/plugin or available CLI)** only for an **authorized post-install functional/behavioral check** against reviewed use cases and a supported host/provider invocation; Promptfoo does **not** itself validate Codex plugin manifests, installability, or package integrity. These two evidence types jointly inform Packaging Success but must remain separately recorded.

**Do not create or run self-devised packaging tests, probe scripts, test suites, or new validation infrastructure.** Use only the existing official tooling and specifically authorized, reviewed Promptfoo assets. Record each outcome, skip, and blocker separately in `docs/BUILD_STATE.md`; do not claim installation or real usability without corresponding evidence.

## 4. Execution boundaries

- **`AGENTS.md` only routes.** The goal lives in `GOAL_AND_USE_CASES.md`; implementation/tool requirements live in `PLUGIN_CONTRACT.md`; factual progress lives in `docs/BUILD_STATE.md`; runtime behavior lives in the relevant `SKILL.md`.
- Follow the owner's **current explicit instructions and authorized scope**. A prior permission or proposal does not authorize unrelated work. Within an explicitly approved scope, do not ask for the same approval repeatedly.
- Preserve the existing Skill, augmented variants, evidence, and prior work. Do not re-run source discovery or load the entire ledger without a specific reason.
- Do not invent requirements, tool availability, approvals, test results, or success claims. Surface material contradictions before building on them.

