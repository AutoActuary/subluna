# SUBLUNA-MANAGED: isolated integration test for install and uninstall.

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "scripts/subluna.py"
SPEC = importlib.util.spec_from_file_location("subluna_manager", MANAGER_PATH)
assert SPEC and SPEC.loader
MANAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MANAGER)


class InstallCycleTests(unittest.TestCase):
    @unittest.skipUnless(MANAGER.find_codex(), "Codex CLI is unavailable")
    def test_install_and_uninstall_are_clean_and_idempotent(self) -> None:
        previous = os.environ.get("CODEX_HOME")
        with tempfile.TemporaryDirectory(prefix="subluna-install-test-") as test_home:
            os.environ["CODEX_HOME"] = test_home
            try:
                self.assertEqual(MANAGER.install(), 0)
                plugins = json.loads(
                    MANAGER.run_codex("plugin", "list", "--available", "--json").stdout
                )
                self.assertEqual(
                    [item["pluginId"] for item in plugins["installed"]],
                    ["subluna@subluna"],
                )
                self.assertEqual(MANAGER.uninstall(), 0)
                plugins = json.loads(
                    MANAGER.run_codex("plugin", "list", "--available", "--json").stdout
                )
                self.assertEqual(plugins["installed"], [])
                self.assertEqual(MANAGER.marketplace_entries(), [])
                self.assertEqual(MANAGER.uninstall(), 0)
            finally:
                if previous is None:
                    os.environ.pop("CODEX_HOME", None)
                else:
                    os.environ["CODEX_HOME"] = previous
                if os.environ.get("SUBLUNA_RUNTIME_BINARY"):
                    MANAGER.ensure_runtime()


if __name__ == "__main__":
    unittest.main()
