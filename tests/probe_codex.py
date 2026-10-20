"""Isolated real Codex install/discovery probe. --invoke additionally runs one bounded model smoke.

Uses a temporary CODEX_HOME and a minimal unpacked plugin, never the live tool store.
Existing auth is copied only into the private temporary home and removed on exit;
no credential is created, printed or changed in the owner's Codex home.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib.util
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import zipfile
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent


@contextmanager
def fixture_directory():
    # Python 3.13+ makes TemporaryDirectory's Windows mode 0700 owner-only.
    # That prevents the host's restricted sandbox token from reading its own
    # installed plugin. A normal inherited-permission fixture matches a regular
    # consumer workspace without changing any preexisting filesystem permissions.
    root = Path(tempfile.gettempdir()) / ("context-intake-codex-" + uuid.uuid4().hex)
    root.mkdir(mode=0o755)
    try:
        yield str(root)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def command(cli, args, env, cwd, timeout=60):
    run = subprocess.run([cli, *args], cwd=cwd, env=env, text=True, encoding="utf-8",
                         errors="replace", capture_output=True, timeout=timeout)
    if run.returncode:
        raise RuntimeError(f"Codex {' '.join(args[:3])}: {run.stderr[-1500:]} {run.stdout[-1500:]}")
    return run.stdout


def discovery(cli, env, consumer):
    process = subprocess.Popen([cli, "app-server"], env=env, cwd=consumer, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                               encoding="utf-8", errors="replace", bufsize=1)
    messages = queue.Queue()
    def reader():
        for line in process.stdout:
            try:
                messages.put(json.loads(line))
            except json.JSONDecodeError:
                pass
        messages.put({"eof": True})
    threading.Thread(target=reader, daemon=True).start()
    def request(number, method, params):
        process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": number, "method": method, "params": params}) + "\n")
        process.stdin.flush()
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            response = messages.get(timeout=max(0.1, deadline - time.monotonic()))
            if response.get("eof"):
                raise RuntimeError("App server exited before responding")
            if response.get("id") == number:
                if "error" in response:
                    raise RuntimeError(f"{method}: {response['error']}")
                return response["result"]
        raise TimeoutError(method)
    try:
        request(1, "initialize", {"clientInfo": {"name": "context-intake-smoke", "version": "0.1.0"},
                                  "capabilities": {"experimentalApi": True}})
        process.stdin.write('{"jsonrpc":"2.0","method":"initialized"}\n')
        process.stdin.flush()
        return request(2, "skills/list", {"cwds": [str(consumer)], "forceReload": True})
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def probe(invoke=False):
    cli = shutil.which("codex.cmd") or shutil.which("codex")
    if not cli:
        raise RuntimeError("Codex CLI unavailable")
    if os.name == "nt":
        # Invoke the installed native binary directly so process termination also
        # closes SQLite handles; terminating an npm .cmd wrapper is insufficient.
        candidates = list((Path(cli).parent / "node_modules/@openai/codex").glob("node_modules/@openai/codex-win32-*/vendor/*/bin/codex.exe"))
        if len(candidates) != 1:
            raise RuntimeError("Expected one installed native Codex binary for the isolated probe")
        cli = str(candidates[0])
    spec = importlib.util.spec_from_file_location("package", ROOT / "scripts/package_plugin.py")
    package = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(package)
    with fixture_directory() as tmp:
        root = Path(tmp)
        probe_home, consumer, market = root / "codex-home", root / "consumer", root / "market"
        for path in (probe_home, consumer, market / ".agents/plugins"):
            path.mkdir(parents=True)
        env = dict(os.environ, CODEX_HOME=str(probe_home), PYTHONDONTWRITEBYTECODE="1")
        archive = root / "plugin.zip"
        package.build(ROOT, archive)
        with zipfile.ZipFile(archive) as z:
            z.extractall(market)
        catalog = {"name": "context-intake-smoke", "plugins": [{"name": "context-intake",
                   "source": {"source": "local", "path": "./context-intake"},
                   "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
                   "category": "Productivity"}]}
        (market / ".agents/plugins/marketplace.json").write_text(json.dumps(catalog), encoding="utf-8")
        version = command(cli, ["--version"], env, consumer).strip()
        command(cli, ["plugin", "marketplace", "add", str(market), "--json"], env, consumer)
        install = command(cli, ["plugin", "add", "context-intake@context-intake-smoke", "--json"], env, consumer)
        listed = command(cli, ["plugin", "list", "--marketplace", "context-intake-smoke", "--json"], env, consumer)
        installed_skills = list(probe_home.glob("plugins/cache/**/skills/context-intake/SKILL.md"))
        if len(installed_skills) != 1:
            raise RuntimeError(f"Expected one installed skill, found {len(installed_skills)}; list={listed[:1000]}")
        skill = installed_skills[0]
        if skill.read_bytes() != (ROOT / "skills/context-intake/SKILL.md").read_bytes():
            raise RuntimeError("Installed skill differs from source")
        discovered = discovery(cli, env, consumer)
        encoded = json.dumps(discovered)
        found = [s for row in discovered.get("data", []) for s in row.get("skills", [])
                 if "context-intake" in s.get("name", "") and Path(s["path"]).resolve() == skill.resolve()]
        if not found or not any(s.get("enabled") is True for s in found):
            config_file = probe_home / "config.toml"
            settings = config_file.read_text() if config_file.exists() else "missing"
            errors = [r.get("errors", []) for r in discovered.get("data", [])]
            raise RuntimeError(f"Enabled skill not discovered; install={install[:1000]}; list={listed[:2000]}; settings={settings[:1000]}; errors={errors}")
        result = {"temporary_root": str(root), "host": version, "installed": True, "installed_skill_sha256": package.hashlib.sha256(skill.read_bytes()).hexdigest(),
                  "skills_list": found, "model_smoke": "not_requested", "owner_home_changed": False}
        if invoke:
            owner_home = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".codex"
            auth = owner_home / "auth.json"
            if not auth.is_file():
                raise RuntimeError("Existing Codex authentication unavailable; no login or credential creation attempted")
            shutil.copyfile(auth, probe_home / "auth.json")
            os.chmod(probe_home / "auth.json", 0o600)
            # Keep the owner's selected model when configured; copy no MCPs, hooks or other settings.
            import tomllib
            config = owner_home / "config.toml"
            selected = tomllib.loads(config.read_text(encoding="utf-8")).get("model") if config.is_file() else None
            # Disable unrelated global skills in this isolated home only. This
            # keeps the single operational smoke focused and avoids loading a
            # workstation's entire skill catalog into its model prompt.
            with (probe_home / "config.toml").open("a", encoding="utf-8") as stream:
                for row in discovered.get("data", []):
                    for other in row.get("skills", []):
                        if other.get("pluginId") is None:
                            stream.write("\n[[skills.config]]\npath = " + json.dumps(other["path"]) + "\nenabled = false\n")
            prompt = (
                "Use $context-intake:context-intake from the installed plugin. This is one authorized operational smoke in an isolated consumer workspace. "
                "Goal: support staff must be able to look up an order status using its reference, without modifying the order. "
                "The request spans Software and UI/UX acquisition. Unknown references must show no match; unavailable status must be reported without guessing. "
                "No existing system evidence has been supplied; locating its interface is a nonblocking repo_fact for software acquisition. "
                "No implementation, architecture selection, network research, other projects, or stakeholder contact. "
                "The desired outcome, actor, scope, prohibited modifications and error outcomes are owner-confirmed by this prompt; no clarification question is needed. "
                "Prepare a complete handoff following the installed skill and 1.0.0 contract, with R-ID requirement traceability and evidence pointing to conversation:smoke-owner-request. "
                "Use original request ID SMOKE-ORDER-01. Consumer workspace is " + str(consumer) + ". "
                "File output is authorized only for the one canonical HANDOFF.md. Use the installed bundled helper for identity, publication and validation. "
                "If the sandbox blocks tools, report the actual failure; do not claim completion. End with only the canonical path and validation result."
            )
            args = ["exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "workspace-write",
                    "--add-dir", str(skill.parent), "-c", 'windows.sandbox="unelevated"', "--json"]
            if selected:
                args += ["--model", selected]
            args.append(prompt)
            try:
                events_text = command(cli, args, env, consumer, timeout=240)
            finally:
                # Credential copies must not survive even when Windows delays
                # deletion of a temporary database or directory.
                (probe_home / "auth.json").unlink(missing_ok=True)
            events = [json.loads(line) for line in events_text.splitlines() if line.startswith("{")]
            handoffs = list(consumer.glob("docs/intake/*/HANDOFF.md"))
            if len(handoffs) != 1:
                raise RuntimeError(f"Expected one handoff, got {len(handoffs)}; events={json.dumps(events)[-6500:]}")
            helper = skill.parent / "scripts/intake.py"
            validated = subprocess.run([sys.executable, "-B", str(helper), "validate", str(handoffs[0]), "--workspace", str(consumer)],
                                       capture_output=True, text=True, check=True)
            validation = json.loads(validated.stdout)
            changed = [p.relative_to(consumer).as_posix() for p in consumer.rglob("*") if p.is_file()]
            if changed != [handoffs[0].relative_to(consumer).as_posix()]:
                raise RuntimeError(f"Unexpected consumer artifacts: {changed}")
            text = handoffs[0].read_text(encoding="utf-8")
            if any(word not in text.lower() for word in ("software", "ui", "order", "r1")):
                raise RuntimeError("Handoff missing material scenario or requirement traceability")
            if validation["status"] != "ready_for_domain_acquisition":
                raise RuntimeError("Nonblocking acquisition gap incorrectly blocked the supplied complete request")
            completed = [e.get("item", {}) for e in events if e.get("type") == "item.completed"]
            commands = [item.get("command", "") for item in completed if item.get("type") == "command_execution"]
            if not any("intake.py" in c and "validate" in c for c in commands):
                raise RuntimeError("No observed model command validating through the bundled helper")
            result.update(model_smoke="passed", validation=validation, consumer_files=changed,
                          model_commands=commands, model_final=[i.get("text") for i in completed if i.get("type") == "agent_message"][-1:])
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--invoke", action="store_true")
    args = parser.parse_args()
    try:
        result = probe(args.invoke)
        result["temporary_cleanup"] = "pending_windows_lock" if Path(result["temporary_root"]).exists() else "removed"
        print(json.dumps(result, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
