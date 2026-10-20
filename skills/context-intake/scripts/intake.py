"""Version 1 handoff contract, deterministic paths and guarded writes. Stdlib only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import unicodedata

ASSETS = Path(__file__).resolve().parent.parent / "assets"
SCHEMA = json.loads((ASSETS / "handoff.schema.json").read_text(encoding="utf-8"))


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def timestamp(value):
    require(nonblank(value), "timestamp must be a string")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(dt.tzinfo is not None, "timestamp needs an explicit timezone")
    except ValueError as exc:
        raise ContractError(f"invalid timestamp: {value}") from exc


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse(text):
    require(not re.search(r"REPLACE-|REQUEST-ID|\{\{[A-Z_ -]+\}\}", text), "unfilled template token")
    lines = text.splitlines()
    headings, sections, titles = [], {}, []
    current, fenced, fence_kind, block_lines = None, False, "", []
    for line in lines:
        if line.startswith("```"):
            if fenced:
                if fence_kind == "json":
                    require(current is not None, "JSON block outside a section")
                    try:
                        block = json.loads("\n".join(block_lines), object_pairs_hook=strict_object)
                    except json.JSONDecodeError as exc:
                        raise ContractError(f"invalid JSON in {current}: {exc}") from exc
                    sections[current]["blocks"].append(block)
                fenced = False
            else:
                require(line.strip() in ("```json", "```text", "```"), "unsupported fence")
                fenced, fence_kind, block_lines = True, line[3:].strip(), []
            continue
        if fenced:
            block_lines.append(line)
        elif line.startswith("## "):
            current = line[3:]
            headings.append(current)
            require(current not in sections, f"duplicate heading: {current}")
            sections[current] = {"blocks": [], "prose": []}
        elif line.startswith("# "):
            titles.append(line[2:])
        elif current:
            sections[current]["prose"].append(line)
    require(not fenced, "unclosed code fence")
    require(titles == [SCHEMA["title"]], "expected exactly '# Intake Handoff'")
    require(headings == SCHEMA["headings"], "required headings missing, extra or out of order")
    result = {}
    for heading, section in sections.items():
        prose = "\n".join(section["prose"]).strip()
        require(bool(prose), f"missing explanatory text: {heading}")
        if "not applicable" in prose.lower():
            require(bool(re.search(r"not applicable.{0,20}(?:because|reason|:|-).+", prose, re.I)),
                    f"not applicable needs a reason: {heading}")
        key = SCHEMA["blocks"].get(heading)
        if key:
            require(len(section["blocks"]) == 1, f"expected one JSON block in {heading}")
            block = section["blocks"][0]
            require(isinstance(block, dict) and set(block) == {key}, f"expected {key} wrapper")
            result[key] = block[key]
        else:
            require(not section["blocks"], f"unexpected JSON block in {heading}")
    return result


def fields(record, names, where):
    require(isinstance(record, dict), f"{where} must be an object")
    require(set(record) == set(names), f"{where} fields must be exactly {names}")


def derived_status(gaps):
    blocking = [g for g in gaps if g["blocking"] and g["state"] == "open"]
    for gap_type, status in (("user_decision", "needs_user_decision"),
                             ("other_stakeholder", "needs_other_stakeholder")):
        if any(g["type"] == gap_type for g in blocking):
            return status
    return "blocked_evidence" if blocking else "ready_for_domain_acquisition"


def validate(text, *, path=None, workspace=None):
    data = parse(text)
    ident, readiness = data["identity"], data["readiness"]
    fields(ident, SCHEMA["identity_fields"], "identity")
    require(all(nonblank(v) for v in ident.values()), "identity fields must be nonblank strings")
    require(ident["schema_version"] == SCHEMA["schema_version"], "unsupported schema version")
    require(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", ident["slug"]), "invalid slug")
    require(re.fullmatch(r"[a-f0-9]{64}", ident["request_key"]), "invalid request key")
    require(ident["approval"] in ("not_requested", "not_confirmed", "owner_confirmed"), "invalid approval")
    require(ident["status"] in SCHEMA["statuses"], "invalid status")
    timestamp(ident["updated_at"])
    relative = f"docs/intake/{ident['slug']}/HANDOFF.md"
    require(ident["canonical_path"] == relative, "canonical path does not match slug")
    if workspace is not None and path is not None:
        require(Path(path).resolve() == safe_target(workspace, relative), "handoff is outside canonical consumer path")
    all_ids = set()
    for kind in ("evidence", "scenarios", "decisions", "gaps"):
        require(isinstance(data[kind], list), f"{kind} must be an array")
        for row in data[kind]:
            fields(row, SCHEMA[{"evidence": "evidence_fields", "scenarios": "scenario_fields",
                               "decisions": "decision_fields", "gaps": "gap_fields"}[kind]], kind)
            require(nonblank(row["id"]) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", row["id"]), "invalid record ID")
            require(row["id"] not in all_ids, f"duplicate record ID: {row['id']}")
            all_ids.add(row["id"])
    evidence_ids = {r["id"] for r in data["evidence"]}
    for row in data["evidence"]:
        require(all(nonblank(v) for v in row.values()), "evidence fields must be nonblank strings")
        require(row["kind"] in ("observed", "desired", "document", "proposal"), "invalid evidence kind")
        require(row["class"] in SCHEMA["evidence_classes"], "invalid evidence class")
        timestamp(row["observed_at"])
    for kind in ("scenarios", "decisions", "gaps"):
        for row in data[kind]:
            require(isinstance(row["sources"], list) and all(isinstance(s, str) and s in evidence_ids for s in row["sources"]),
                    f"{row['id']} has an unknown evidence reference")
    for row in data["scenarios"]:
        for name in ("actor", "goal", "trigger", "preconditions", "main_path", "postconditions"):
            require(nonblank(row[name]), f"scenario {name} must be nonblank text")
        for name in ("alternatives", "failures", "rules"):
            require(isinstance(row[name], list) and all(nonblank(v) for v in row[name]), f"scenario {name} must be a string array")
        require(row["status"] in ("proposed", "confirmed", "superseded"), "invalid scenario status")
        require(row["status"] != "confirmed" or row["sources"], "confirmed scenario requires evidence")
    for row in data["decisions"]:
        require(row["status"] in ("accepted", "proposed", "provisional", "contradicted", "superseded"), "invalid decision status")
        require(all(nonblank(row[k]) for k in ("statement", "origin", "authority", "consequence")), "decision needs origin, authority and consequence")
        if row["status"] == "accepted":
            require(row["sources"] and row["authority"].lower() not in ("unknown", "unassigned", "agent", "intake-agent"), "accepted decision needs owner evidence")
    if ident["approval"] == "owner_confirmed":
        require(any(d["status"] == "accepted" for d in data["decisions"]), "owner confirmation requires a sourced accepted decision")
    gap_ids = {r["id"] for r in data["gaps"]}
    for row in data["gaps"]:
        require(row["type"] in SCHEMA["gap_types"], "invalid gap type")
        require(type(row["blocking"]) is bool, "blocking must be boolean")
        require(row["state"] in ("open", "resolved", "deferred"), "invalid gap state")
        require(not (row["blocking"] and row["state"] == "deferred"), "blocking gaps cannot be silently deferred")
        require(all(nonblank(row[k]) for k in ("question", "impact", "owner", "route")), "gap needs question, impact, owner and route")
        require(isinstance(row["depends_on"], list) and all(isinstance(v, str) and v in gap_ids and v != row["id"] for v in row["depends_on"]), "invalid gap dependency")
    graph = {g["id"]: g["depends_on"] for g in data["gaps"]}
    done, visiting = set(), set()
    def visit(node):
        require(node not in visiting, "cyclic gap dependencies")
        if node not in done:
            visiting.add(node)
            for dep in graph[node]:
                visit(dep)
            visiting.remove(node)
            done.add(node)
    for node in graph:
        visit(node)
    fields(readiness, SCHEMA["readiness_fields"], "readiness")
    require(all(nonblank(readiness[k]) for k in ("status", "sufficiently_known", "next_receiver")), "incomplete readiness")
    for key in ("actions", "limitations"):
        require(isinstance(readiness[key], list) and all(nonblank(v) for v in readiness[key]), f"readiness {key} must be a string array")
    require(readiness["actions"], "handoff needs at least one next action")
    require(ident["status"] == readiness["status"] == derived_status(data["gaps"]), "blocker/status inconsistency")
    return data


def safe_target(workspace, relative):
    root = Path(workspace).resolve(strict=True)
    require(root.is_dir(), "consumer workspace must be a directory")
    rel = Path(relative)
    require(not rel.is_absolute() and ".." not in rel.parts and not rel.drive, "unsafe relative path")
    target = root / rel
    require(target.resolve().is_relative_to(root), "path escapes consumer workspace through a link")
    # Reject even internal symlink/junction redirection to keep one physical record.
    for parent in [target, *target.parents]:
        if parent == root:
            break
        require(not parent.is_symlink() and not (hasattr(parent, "is_junction") and parent.is_junction()), "linked handoff paths are unsupported")
    return target


def identity(goal, request_id=None):
    require(nonblank(request_id or goal), "provide goal or explicit request ID")
    seed = unicodedata.normalize("NFKC", request_id or goal).strip()
    normalized = " ".join(seed.split()).casefold()
    key = hashlib.sha256((("id:" if request_id else "goal:") + normalized).encode()).hexdigest()
    ascii_seed = unicodedata.normalize("NFKD", normalized).encode("ascii", "ignore").decode()
    prefix = re.sub(r"[^a-z0-9]+", "-", ascii_seed).strip("-")[:60].rstrip("-") or "request"
    slug = f"{prefix}-{key[:12]}"
    return {"id": request_id or f"REQ-{key[:12]}", "request_key": key, "slug": slug,
            "canonical_path": f"docs/intake/{slug}/HANDOFF.md"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_handoff(workspace, text, expected_sha=None):
    data = validate(text)
    target = safe_target(workspace, data["identity"]["canonical_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    # The lock avoids simultaneous cooperating writers. Refuse stale updates.
    lock = target.parent / ".intake-write.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ContractError("another writer holds the intake lock; inspect before retrying") from exc
    tmp = None
    try:
        os.close(fd)
        safe_target(workspace, data["identity"]["canonical_path"])
        if target.exists():
            require(expected_sha is not None and digest(target) == expected_sha, "update requires current --expected-sha")
            prior = validate(target.read_text(encoding="utf-8"))
            for name in ("id", "request_key", "slug", "canonical_path"):
                require(prior["identity"][name] == data["identity"][name], "request identity collision; use explicit distinct request ID")
        else:
            require(expected_sha is None, "cannot update a missing handoff")
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=target.parent, delete=False) as stream:
            tmp = Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        validate(tmp.read_text(encoding="utf-8"))
        os.replace(tmp, target)
        return target
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("path", type=Path)
    check.add_argument("--workspace", type=Path)
    locate = sub.add_parser("locate", help="compute path without writing")
    init = sub.add_parser("init", help="create an explicitly incomplete handoff; no overwrite")
    for item in (locate, init):
        item.add_argument("--workspace", required=True, type=Path)
        item.add_argument("--goal", default="")
        item.add_argument("--request-id")
    init.add_argument("--owner", default="unassigned")
    init.add_argument("--write", action="store_true", help="required to authorize the write")
    put = sub.add_parser("put", help="validate and atomically publish a prepared handoff")
    put.add_argument("--workspace", required=True, type=Path)
    put.add_argument("--content", required=True, type=Path)
    put.add_argument("--expected-sha")
    put.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            data = validate(args.path.read_text(encoding="utf-8"), path=args.path, workspace=args.workspace)
            result = {"valid": True, "schema_version": SCHEMA["schema_version"], "status": data["identity"]["status"], "sha256": digest(args.path)}
        elif args.command in ("locate", "init"):
            ident = identity(args.goal, args.request_id)
            target = safe_target(args.workspace, ident["canonical_path"])
            result = {**ident, "absolute_path": str(target), "exists": target.exists()}
            if target.exists():
                prior = validate(target.read_text(encoding="utf-8"))
                require(prior["identity"]["request_key"] == ident["request_key"], "request identity collision")
                result["sha256"] = digest(target)
            if args.command == "init":
                require(args.write, "init requires --write; use locate for read-only discussion")
                require(not target.exists(), "handoff exists; resume it instead of reinitializing")
                text = (ASSETS / "HANDOFF.md").read_text(encoding="utf-8")
                text = text.replace("REQUEST-ID", "initial").replace("REPLACE-REQUEST-KEY", ident["request_key"]).replace("REPLACE-SLUG", ident["slug"])
                data = parse(text)
                data["identity"].update(ident, owner=args.owner, updated_at=datetime.now(timezone.utc).isoformat())
                text = re.sub(r'```json\n.*?\n```', lambda m: "```json\n" + json.dumps({"identity": data["identity"]}, ensure_ascii=False) + "\n```", text, count=1, flags=re.S)
                write_handoff(args.workspace, text)
                result["sha256"] = digest(target)
        else:
            require(args.write, "put requires --write")
            target = write_handoff(args.workspace, args.content.read_text(encoding="utf-8"), args.expected_sha)
            result = {"path": str(target), "sha256": digest(target)}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ContractError, OSError, TypeError, KeyError, RecursionError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
