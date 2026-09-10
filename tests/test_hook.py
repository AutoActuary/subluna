# SUBLUNA-MANAGED: tests for SubLuna activation and injected policy.

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins/subluna"
POLICY_PATH = PLUGIN_ROOT / "skills/subluna/references/policy.md"
GUIDE_PATH = PLUGIN_ROOT / "skills/subluna/references/delegation-guide.md"


def expected_context() -> str:
    return (
        POLICY_PATH.read_text(encoding="utf-8")
        .strip()
        .replace("`delegation-guide.md`", f"`{GUIDE_PATH}`")
    )


def hook_command() -> list[str]:
    suffix = ".exe" if os.name == "nt" else ""
    runtime = PLUGIN_ROOT / f"bin/subluna-hook{suffix}"
    if not runtime.is_file():
        raise unittest.SkipTest("SubLuna runtime is not staged")
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
    def test_activates_for_sol_and_astra_slugs(self) -> None:
        for model in (
            "gpt-5.6-sol",
            "vendor-sol-preview",
            "sol",
            "gpt-6-astra",
            "vendor-astra-preview",
            "astra",
        ):
            with self.subTest(model=model):
                payload = json.loads(run_hook(model).stdout)
                context = payload["hookSpecificOutput"]["additionalContext"]
                self.assertEqual(context, expected_context())

    def test_does_not_activate_for_other_models(self) -> None:
        for model in ("gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.5", ""):
            with self.subTest(model=model):
                self.assertEqual(run_hook(model).stdout, "")

    def test_optout_is_case_insensitive_and_accepts_skill_forms(self) -> None:
        prompts = (
            "No subluna for this one",
            "NO /SUBLUNA",
            "No $subluna today",
            "Don't use /subluna for this one",
            "DO NOT USE SUBLUNA",
            "Please don't use $subluna today",
            "No [$subluna:subluna](C:/plugins/subluna/skills/subluna/SKILL.md)",
            "Don’t use [$subluna](C:/skills/subluna/SKILL.md)",
        )
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                self.assertEqual(run_hook("gpt-5.6-sol", prompt).stdout, "")

    def test_policy_uses_absolute_guide_path(self) -> None:
        payload = json.loads(run_hook("gpt-5.6-sol").stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(context, expected_context())
        self.assertNotIn("`delegation-guide.md`", context)
        self.assertIn(str(GUIDE_PATH), context)


if __name__ == "__main__":
    unittest.main()
