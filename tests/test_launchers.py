# SOLUTE-MANAGED: platform launcher tests for Windows and POSIX systems.

from __future__ import annotations

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins/solute"


def powershell() -> str | None:
    return shutil.which("powershell.exe") or shutil.which("pwsh")


def manager_command(action: str) -> list[str]:
    if os.name == "nt":
        shell = powershell()
        if shell is None:
            raise unittest.SkipTest("PowerShell is unavailable")
        return [
            shell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "scripts/solute.ps1"),
            action,
        ]
    return ["sh", str(ROOT / "scripts/solute.sh"), action]


def hook_command() -> list[str]:
    suffix = ".exe" if os.name == "nt" else ""
    runtime = PLUGIN_ROOT / f"bin/solute-hook{suffix}"
    if not runtime.is_file():
        raise unittest.SkipTest("Solute runtime is not staged")
    return [str(runtime)]


class LauncherTests(unittest.TestCase):
    def test_manager_launcher_runs_doctor(self) -> None:
        result = subprocess.run(
            manager_command("doctor"),
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Solute doctor passed", result.stdout)

    def test_hook_launcher_activates_for_sol(self) -> None:
        event = {
            "hook_event_name": "UserPromptSubmit",
            "model": "gpt-5.6-sol",
            "prompt": "Fix the failing test",
        }
        env = os.environ.copy()
        env["PLUGIN_ROOT"] = str(PLUGIN_ROOT)
        result = subprocess.run(
            hook_command(),
            input=json.dumps(event),
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Use Luna `high`", context)
        self.assertIn("Use Luna `xhigh`", context)

    def test_hook_launcher_is_silent_for_terra(self) -> None:
        event = {
            "hook_event_name": "UserPromptSubmit",
            "model": "gpt-5.6-terra",
            "prompt": "Fix the failing test",
        }
        env = os.environ.copy()
        env["PLUGIN_ROOT"] = str(PLUGIN_ROOT)
        result = subprocess.run(
            hook_command(),
            input=json.dumps(event),
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
