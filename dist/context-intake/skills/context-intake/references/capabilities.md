# Required capabilities and host bindings

Use this table only when the current gap needs evidence or file output. Tool names
below identify verified Codex routes, not tools this package creates. Discover the
current host's equivalent operation and effective permission before use. Installed,
exposed, connected, operational and verified for this request are separate states.
Never copy a developer's absolute paths, credentials or global MCP registry into a
consumer project. No new MCP service is needed for these bindings.

| Required capability | Codex binding | Cursor / Cline binding | If unavailable |
| --- | --- | --- | --- |
| Recover owner intent and decisions | Current conversation; previously supplied canonical handoff and owner documents. Explicitly authorized same-project history may use `mcp__codex_app__read_thread` when a thread ID is known. | Current task history and accessible owner documents; host history tools only when authorized. | Preserve established answers; record missing history and its impact. Do not claim inaccessible turns were read. |
| Local file discovery/read/search | `exec_command` with bounded `rg`/file reads; read consumer instructions first. | Existing read/search/list tools, or bounded terminal commands. | `repo_fact` gap naming the required file/source; block only if needed to frame the acquisition request. |
| Repository evidence | Read-only Git and `rg`; registered Serena `mcp__serena__serena_repl` for a targeted file/symbol after its `initial_instructions`. Registered GitHub search/read tools for a known relevant repository. | Existing local Git/search and any already connected corresponding MCP. | Prefer another permitted local route; otherwise preserve a concrete evidence gap. No checkout, writes, indexing or blanket analysis. |
| Internal documents | Local canonical docs first. Connected `mcp__codex_apps__google_drive_search` and `google_drive_fetch` for the named project/document with authorized access. | Local docs and the current host's already connected document search/read. | Record an owner/source/access route. An empty search does not establish absence or authority. No new account or outreach. |
| Public/versioned facts | `web__run` official-source lookup; registered Context7 `mcp__context7__resolve_library_id` then `query_docs` for the precise fact/version. | Host web/official docs tools or existing Context7 integration. | Record `external_fact` with authoritative source/version and question. Never use Firecrawl or a paid fallback. |
| Stable handoff identity, write and validation | Bundled `scripts/intake.py` through the existing terminal/Python runtime, always with explicit consumer `--workspace`. | The identical bundled helper through the host terminal. | Python 3.10+ is required for guarded publication. Read-only discussion can continue; do not claim a canonical validated file. |
| Classification and routing | `policy.md`, relevant conditional methods and `adapters.md`; semantic readiness review by the agent. | Same canonical skill and contract. | Preserve typed gaps and unknown domain/owner; no invented specialist or success. |

Serena's tool facade may change across versions: read its returned manual instead
of assuming a symbol API. A requested onboarding/project initializer is a separate
mutation; it is unnecessary for a simple native file read. Prefer native search
when it resolves the same bounded fact with less work.

REA and Repomix are considered specialist/delegated routes: presence in the host
does not justify binary inspection, browser capture or whole-repo packaging during
intake. Figma, n8n, QA, build/evaluation and authoring tools retain their specialist
or build-time ownership. Never run those lifecycles to fill an ordinary intake gap.

Before an operation, identify the one claim it could establish. Afterwards retain
source, date, scope, result and limits in the handoff. A configured MCP or successful
public read does not prove private-repository/document access. Handle permission,
auth and tool failures honestly; do not retry through broader scopes or providers.
