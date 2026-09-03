# SOLUTE-MANAGED: tests for Solute activation and injected policy.

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins/solute"


def hook_command() -> list[str]:
    suffix = ".exe" if os.name == "nt" else ""
    runtime = PLUGIN_ROOT / f"bin/solute-hook{suffix}"
    if not runtime.is_file():
        raise unittest.SkipTest("Solute runtime is not staged")
    return [str(runtime)]


def run_hook(model: str, prompt: str = "Fix the failing tests") -> subprocess.CompletedProcess[str]:
    event = {
        "hook_event_name": "UserPromptSubmit",
        "model": model,
        "prompt": prompt,
    }
    env = os.environ.copy()
    env["PLUGIN_ROOT"] = str(PLUGIN_ROOT)
    return subprocess.run(
        hook_command(),
        input=json.dumps(event),
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


class HookTests(unittest.TestCase):
    def test_activates_for_current_and_future_sol_slugs(self) -> None:
        for model in ("gpt-5.6-sol", "gpt-5.7-sol", "vendor-sol-preview", "sol"):
            with self.subTest(model=model):
                payload = json.loads(run_hook(model).stdout)
                context = payload["hookSpecificOutput"]["additionalContext"]
                self.assertIn("Use Luna `high`", context)
                self.assertIn("Use Luna `xhigh`", context)

    def test_does_not_activate_for_other_models(self) -> None:
        for model in ("gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.5", ""):
            with self.subTest(model=model):
                self.assertEqual(run_hook(model).stdout, "")

    def test_optout_is_case_insensitive_and_accepts_skill_forms(self) -> None:
        prompts = (
            "No solute for this one",
            "NO /SOLUTE",
            "No $solute today",
            "Don't use /solute for this one",
            "DO NOT USE SOLUTE",
            "Please don't use $solute today",
            "No [$solute:solute](C:/plugins/solute/skills/solute/SKILL.md)",
            "Don’t use [$solute](C:/skills/solute/SKILL.md)",
        )
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                self.assertEqual(run_hook("gpt-5.6-sol", prompt).stdout, "")

    def test_policy_uses_absolute_guide_path(self) -> None:
        payload = json.loads(run_hook("gpt-5.6-sol").stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("stop Luna workers", context)
        self.assertIn("ignore their results for that turn", context)
        self.assertNotIn("`delegation-guide.md`", context)
        self.assertIn(str(PLUGIN_ROOT / "skills/solute/references/delegation-guide.md"), context)


if __name__ == "__main__":
    unittest.main()
