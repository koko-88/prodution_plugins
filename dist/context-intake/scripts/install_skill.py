"""Install the same skill into a chosen consumer workspace; never overwrite. Stdlib only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent.parent
HOSTS = {"cursor": ".cursor", "cline": ".cline", "codex": ".agents"}


def target_path(workspace, host):
    root = Path(workspace).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Consumer workspace must be a directory")
    target = root / HOSTS[host] / "skills" / "context-intake"
    for path in (target, *target.parents):
        if path == root:
            break
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError("Linked install paths are unsupported")
    if not target.resolve().is_relative_to(root):
        raise ValueError("Install path escapes consumer workspace")
    return target


def install(workspace, host, *, write=False, source=ROOT):
    target = target_path(workspace, host)
    origin = Path(source).resolve(strict=True) / "skills/context-intake"
    if not (origin / "SKILL.md").is_file():
        raise ValueError("Source skill is missing")
    if target.exists():
        raise ValueError("Skill already exists; preserve it and review an upgrade manually")
    for path in (origin, *origin.rglob("*")):
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError("Linked source paths are unsupported")
    result = {"host": host, "target": str(target), "written": False}
    if write:
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".context-intake-install-", dir=target.parent) as tmp:
            stage = Path(tmp) / "context-intake"
            shutil.copytree(origin, stage, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            # mkdir reserves the destination without replacing an existing owner directory.
            target.mkdir()
            try:
                shutil.copytree(stage, target, dirs_exist_ok=True)
            except OSError:
                # Preserve partial data for inspection; never delete a consumer directory.
                raise
        result["written"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--host", required=True, choices=HOSTS)
    parser.add_argument("--write", action="store_true", help="required for workspace installation")
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.workspace, args.host, write=args.write)))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"written": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
