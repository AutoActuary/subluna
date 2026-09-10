# SUBLUNA-MANAGED: repository consistency and uninstall breadcrumbs.

from __future__ import annotations

import importlib.util
import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "scripts/subluna.py"
SPEC = importlib.util.spec_from_file_location("subluna_manager_repository", MANAGER_PATH)
assert SPEC and SPEC.loader
MANAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MANAGER)


class RepositoryTests(unittest.TestCase):
    def test_identifiers_and_paths_match(self) -> None:
        marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (ROOT / "plugins/subluna/.codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(marketplace["name"], "subluna")
        self.assertEqual(marketplace["plugins"][0]["name"], "subluna")
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/subluna")
        self.assertEqual(manifest["name"], "subluna")

    def test_runtime_release_version_matches_source(self) -> None:
        cargo = tomllib.loads((ROOT / "native-hook/Cargo.toml").read_text(encoding="utf-8"))
        self.assertEqual(MANAGER.RUNTIME_VERSION, f"v{cargo['package']['version']}")

    def test_uninstall_breadcrumbs_exist_outside_skill_context(self) -> None:
        breadcrumbs = (
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            ROOT / "UNINSTALL.md",
            ROOT / "plugins/subluna/hooks/hooks.json",
            ROOT / "native-hook/src/main.rs",
        )
        for path in breadcrumbs:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8").lower()
                self.assertIn("subluna", text)
                self.assertTrue("remove" in text or "uninstall" in text)

    def test_skill_files_do_not_carry_uninstall_breadcrumbs(self) -> None:
        skill_root = ROOT / "plugins/subluna/skills/subluna"
        for path in skill_root.rglob("*"):
            if path.is_file():
                with self.subTest(path=path):
                    text = path.read_text(encoding="utf-8").lower()
                    self.assertNotIn("uninstall", text)
                    self.assertNotIn("plugin remove", text)

    def test_runtime_policy_stays_compact(self) -> None:
        policy = (
            ROOT / "plugins/subluna/skills/subluna/references/policy.md"
        ).read_text(encoding="utf-8")
        self.assertLess(len(policy), 1000)
        self.assertIn("delegation-guide.md", policy)

    def test_hot_path_has_no_interpreter(self) -> None:
        hooks = json.loads(
            (ROOT / "plugins/subluna/hooks/hooks.json").read_text(encoding="utf-8")
        )
        handler = hooks["hooks"]["UserPromptSubmit"][0]["hooks"][0]
        commands = f"{handler['command']} {handler['commandWindows']}".lower()
        for runtime in ("python", "powershell", "pwsh", "node", "cscript", "awk"):
            with self.subTest(runtime=runtime):
                self.assertNotIn(runtime, commands)
        self.assertIn("bin/subluna-hook", handler["command"])
        self.assertIn("bin\\subluna-hook.exe", handler["commandWindows"])
        self.assertTrue(handler["commandWindows"].startswith("cmd.exe /d /c call "))

    def test_longer_guide_is_inside_the_skill_and_not_duplicated(self) -> None:
        guide = (
            ROOT
            / "plugins/subluna/skills/subluna/references/delegation-guide.md"
        )
        self.assertTrue(guide.is_file())
        self.assertFalse((ROOT / "ECONOMICS.md").exists())


if __name__ == "__main__":
    unittest.main()
