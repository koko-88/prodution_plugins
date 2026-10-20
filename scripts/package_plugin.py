"""Build an allowlisted, self-contained private plugin ZIP. Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "plugin.json", ".codex-plugin/plugin.json", "README.md",
    "scripts/package_plugin.py", "scripts/install_skill.py",
)
TREES = ("skills/context-intake", "docs/coverage")


def source_files(root):
    root = Path(root).resolve(strict=True)
    files = [root / name for name in FILES]
    for name in TREES:
        base = root / name
        if not base.is_dir():
            raise ValueError(f"Missing required tree: {name}")
        files.extend(p for p in base.rglob("*") if p.is_file()
                     and "__pycache__" not in p.parts and p.suffix != ".pyc")
    for path in files:
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Missing or linked package file: {path}")
        for parent in path.parents:
            if parent == root:
                break
            if parent.is_symlink() or (hasattr(parent, "is_junction") and parent.is_junction()):
                raise ValueError(f"Linked package directory: {parent}")
    return sorted(set(files))


def check(root):
    root = Path(root).resolve(strict=True)
    files = source_files(root)
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    legacy = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("Unexpected portable manifest schema")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest["name"]) or len(manifest["name"]) > 64:
        raise ValueError("Invalid plugin name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        raise ValueError("Expected stable SemVer")
    for key in ("name", "version", "description"):
        if manifest[key] != legacy[key]:
            raise ValueError(f"Compatibility manifest drift: {key}")
    ui = manifest["extensions"]["com.openai"]["interface"]
    if ui != legacy["interface"] or len(ui["shortDescription"]) > 30:
        raise ValueError("Presentation drift or subtitle longer than 30 characters")
    if not isinstance(ui["capabilities"], list):
        raise ValueError("Invalid capabilities")
    skill = root / "skills/context-intake/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\nname: context-intake\ndescription: ") or text.count("\n---\n") < 1:
        raise ValueError("Invalid skill frontmatter")
    if len(skill.read_bytes()) > 1024 * 1024:
        raise ValueError("Skill exceeds portable size limit")
    for path in files:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        if path.suffix == ".md" and path.is_relative_to(root / "skills"):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                if not resolved.is_relative_to(root) or not resolved.is_file():
                    raise ValueError(f"Unresolved local link in {path.name}: {target}")
    return manifest, files


def build(root, output):
    root, output = Path(root).resolve(strict=True), Path(output).resolve()
    manifest, files = check(root)
    if output.exists():
        raise ValueError("Output exists; choose a new path or explicitly remove the old build")
    if output.suffix.lower() != ".zip" or any(output.is_relative_to(root / tree) for tree in TREES):
        raise ValueError("Output must be a ZIP outside component directories")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(f"{manifest['name']}/{path.relative_to(root).as_posix()}", (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity failure")
        for path in files:
            name = f"{manifest['name']}/{path.relative_to(root).as_posix()}"
            if archive.read(name) != path.read_bytes():
                raise ValueError(f"Archive/source mismatch: {name}")
    return {"archive": str(output), "files": len(files), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stage", type=Path, help="also create a fresh allowlisted local install directory")
    parser.add_argument("--check", action="store_true", help="read-only component/link checks")
    args = parser.parse_args()
    try:
        if args.check:
            manifest, files = check(args.source)
            result = {"valid": True, "name": manifest["name"], "version": manifest["version"], "files": len(files)}
        else:
            if args.stage and args.stage.exists():
                raise ValueError("Stage exists; preserve it and choose a fresh staging path")
            version = json.loads((args.source / "plugin.json").read_text(encoding="utf-8"))["version"]
            result = build(args.source, args.output or ROOT / "dist" / f"context-intake-{version}.zip")
            if args.stage:
                _, files = check(args.source)
                stage = args.stage.resolve()
                if any(stage.is_relative_to(args.source.resolve() / tree) for tree in TREES):
                    raise ValueError("Stage must be outside component directories")
                stage.mkdir(parents=True)
                for path in files:
                    dest = stage / path.relative_to(args.source.resolve())
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, dest)
                check(stage)
                result["stage"] = str(stage)
        print(json.dumps(result))
        return 0
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
