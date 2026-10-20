"""Narrow packaging and handoff operational checks; not the 35-case behavioral evaluation."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


intake = load("intake", "skills/context-intake/scripts/intake.py")
package = load("package", "scripts/package_plugin.py")
installer = load("installer", "scripts/install_skill.py")


def handoff(*, request_id="SMOKE-01", blocking=False):
    """Independent bounded local fixture: an owner requests read-only order lookup."""
    ident = intake.identity("Let support staff look up an order status", request_id)
    ident.update(schema_version="1.0.0", domain="software + UI/UX", scope="Order status lookup only",
                 status="blocked_evidence" if blocking else "ready_for_domain_acquisition",
                 owner="test-owner", updated_by="operational-smoke", updated_at="2026-10-19T12:00:00Z",
                 approval="not_requested")
    records = {
        "identity": ident,
        "evidence": [{"id": "E1", "claim": "Support may view order status but must not modify orders.",
                      "kind": "desired", "class": "direct", "source": "fixture:owner-request",
                      "authority": "test-owner", "observed_at": "2026-10-19T12:00:00Z"}],
        "scenarios": [{"id": "S1", "actor": "support staff", "goal": "View order status",
                       "trigger": "Customer asks about an order", "preconditions": "Staff have authorized access",
                       "main_path": "Look up the supplied order reference and view its status",
                       "alternatives": ["Unknown reference returns no matching order"],
                       "failures": ["Unavailable status is reported without guessing"],
                       "postconditions": "Staff know the observed status; the order is unchanged",
                       "rules": ["R1: View status only (E1)"], "status": "confirmed", "sources": ["E1"]}],
        "decisions": [{"id": "D1", "statement": "Order modification is excluded", "status": "accepted",
                       "origin": "fixture:owner-request", "authority": "test-owner", "sources": ["E1"],
                       "consequence": "Acquisition must preserve read-only behavior"}],
        "gaps": [{"id": "G1", "type": "repo_fact", "question": "Where is the existing order status source?",
                  "impact": "Locates the acquisition target", "blocking": blocking, "state": "open",
                  "owner": "software acquisition", "route": "Read the relevant status interface",
                  "depends_on": [], "sources": ["E1"]}],
        "readiness": {"status": ident["status"], "sufficiently_known": "Actor, desired behavior and exclusions are known",
                      "next_receiver": "Software and UI/UX acquisition owners",
                      "actions": ["Software: locate existing order status interface", "UI/UX: recover staff lookup states"],
                      "limitations": ["This fixture verifies the contract, not stakeholder truth or model behavior"]},
    }
    prose = {
        "Identity & Stage": "Pre-domain intake in an isolated operational fixture.",
        "Intent & Outcomes": "R1: Support views order status. Owner-confirmed by E1; covered by S1 and D1.",
        "Current State & Evidence": "E1 establishes desired behavior; current implementation remains unknown.",
        "Actors & Scenarios": "S1 covers lookup, unknown references and unavailable status.",
        "Scope & Exclusions": "R1 includes lookup only. Editing orders is prohibited by E1 and D1.",
        "Constraints & Dependencies": "Access must be authorized. Concrete technology choices remain downstream.",
        "Decisions & Assumptions": "D1 preserves the explicit owner prohibition; no stack is chosen.",
        "Open Gaps & Owners": "G1 is routed to the software acquisition owner with its consequence stated.",
        "Context Pointers": "fixture:owner-request is the source for E1; no production access is used.",
        "Readiness & Next Handoff": "One handoff serves both acquisition owners; it does not authorize execution.",
    }
    return records, prose


def render(records, prose):
    parts = ["# Intake Handoff\n"]
    for heading in intake.SCHEMA["headings"]:
        parts.append(f"## {heading}\n\n{prose[heading]}\n")
        key = intake.SCHEMA["blocks"].get(heading)
        if key:
            parts.append("```json\n" + json.dumps({key: records[key]}) + "\n```\n")
    return "\n".join(parts)


class HandoffChecks(unittest.TestCase):
    def test_stable_identity_and_non_latin_goal(self):
        self.assertEqual(intake.identity("  ONE  Goal "), intake.identity("one goal"))
        self.assertEqual(intake.identity("changed prompt", "OPS-14"), intake.identity("original", "OPS-14"))
        self.assertRegex(intake.identity("متابعة طلب")['slug'], r"^request-[a-f0-9]{12}$")

    def test_read_only_path_calculation_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = intake.safe_target(tmp, intake.identity("lookup")["canonical_path"])
            self.assertFalse(path.exists())
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_publish_resume_and_stale_update(self):
        records, prose = handoff()
        with tempfile.TemporaryDirectory() as tmp:
            text = render(records, prose)
            path = intake.write_handoff(tmp, text)
            result = intake.validate(path.read_text(), path=path, workspace=tmp)
            self.assertEqual(result["identity"]["schema_version"], "1.0.0")
            before = path.read_bytes()
            with self.assertRaises(intake.ContractError):
                intake.write_handoff(tmp, text, "0" * 64)
            self.assertEqual(path.read_bytes(), before)
            prose["Intent & Outcomes"] += " Owner correction preserved under R1."
            intake.write_handoff(tmp, render(records, prose), intake.digest(path))
            self.assertEqual(len(list(Path(tmp).rglob("HANDOFF.md"))), 1)
            self.assertFalse(list(Path(tmp).rglob(".intake-write.lock")))

    def test_collision_and_cooperating_writer_lock(self):
        records, prose = handoff()
        with tempfile.TemporaryDirectory() as tmp:
            path = intake.write_handoff(tmp, render(records, prose))
            before = path.read_bytes()
            records["identity"]["id"] = "ANOTHER-REQUEST"
            with self.assertRaises(intake.ContractError):
                intake.write_handoff(tmp, render(records, prose), intake.digest(path))
            lock = path.parent / ".intake-write.lock"
            lock.touch()
            with self.assertRaises(intake.ContractError):
                intake.write_handoff(tmp, render(records, prose), intake.digest(path))
            self.assertTrue(lock.exists())
            self.assertEqual(path.read_bytes(), before)

    def test_traversal_and_linked_output_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(intake.ContractError):
                intake.safe_target(tmp, "../outside/HANDOFF.md")
            root = Path(tmp)
            (root / "other").mkdir()
            try:
                (root / "docs").symlink_to(root / "other", target_is_directory=True)
            except OSError:
                self.skipTest("OS did not permit symlink creation; traversal assertion passed")
            with self.assertRaises(intake.ContractError):
                intake.safe_target(tmp, "docs/intake/id/HANDOFF.md")

    def test_readiness_and_provenance_fail_closed(self):
        records, prose = handoff(blocking=True)
        text = render(records, prose)
        self.assertEqual(intake.validate(text)["identity"]["status"], "blocked_evidence")
        variants = []
        bad = copy.deepcopy(records)
        bad["decisions"][0]["sources"] = []
        variants.append(bad)
        bad = copy.deepcopy(records)
        bad["gaps"][0]["state"] = "deferred"
        variants.append(bad)
        bad = copy.deepcopy(records)
        bad["readiness"]["status"] = "ready_for_domain_acquisition"
        variants.append(bad)
        bad = copy.deepcopy(records)
        bad["scenarios"][0]["sources"] = ["MISSING"]
        variants.append(bad)
        for bad in variants:
            with self.subTest(bad=bad), self.assertRaises(intake.ContractError):
                intake.validate(render(bad, prose))

    def test_cyclic_dependencies_and_duplicate_keys_fail(self):
        records, prose = handoff()
        second = copy.deepcopy(records["gaps"][0])
        second.update(id="G2", depends_on=["G1"])
        records["gaps"][0]["depends_on"] = ["G2"]
        records["gaps"].append(second)
        with self.assertRaises(intake.ContractError):
            intake.validate(render(records, prose))
        records, prose = handoff()
        with self.assertRaises(intake.ContractError):
            intake.validate(render(records, prose).replace('"id": "E1"', '"id": "E1", "id": "E2"'))


class PackageChecks(unittest.TestCase):
    def test_self_contained_archive_and_unpacked_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "plugin.zip"
            result = package.build(ROOT, output)
            self.assertGreater(result["files"], 20)
            with zipfile.ZipFile(output) as z:
                names = z.namelist()
                self.assertIn("context-intake/.codex-plugin/plugin.json", names)
                self.assertIn("context-intake/docs/coverage/variant-ledger.json", names)
                self.assertFalse(any("marketplace.json" in n or ".tool-storage" in n or "__pycache__" in n for n in names))
                z.extractall(Path(tmp) / "unpacked")
            package.check(Path(tmp) / "unpacked/context-intake")
            with self.assertRaises(ValueError):
                package.build(ROOT, output)

    def test_workspace_adapters_do_not_overwrite(self):
        for host in ("cursor", "cline", "codex"):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as tmp:
                result = installer.install(tmp, host)
                self.assertFalse(result["written"])
                self.assertEqual(list(Path(tmp).iterdir()), [])
                result = installer.install(tmp, host, write=True)
                target = Path(result["target"])
                self.assertEqual((target / "SKILL.md").read_bytes(), (ROOT / "skills/context-intake/SKILL.md").read_bytes())
                with self.assertRaises(ValueError):
                    installer.install(tmp, host, write=True)


if __name__ == "__main__":
    unittest.main()
