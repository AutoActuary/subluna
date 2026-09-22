#!/usr/bin/env python3
# SUBLUNA-MANAGED: installer, uninstaller, and diagnostic entry point.
"""Manage the SubLuna marketplace and plugin without editing unrelated config."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any


PLUGIN = "subluna"
MARKETPLACE = "subluna"
MARKETPLACE_FILE = Path(".agents/plugins/marketplace.json")
RUNTIME_VERSION = "v0.3.4"
RUNTIME_REPOSITORY = "https://github.com/AutoActuary/subluna/releases/download"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def npm_codex_command(launcher: Path) -> list[str] | None:
    node_name = "node.exe" if os.name == "nt" else "node"
    node = launcher.parent / node_name
    if not node.is_file():
        resolved = shutil.which(node_name)
        node = Path(resolved) if resolved else node
    script = launcher.parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
    if node.is_file() and script.is_file():
        return [str(node), str(script)]
    return None


def find_codex() -> list[str] | None:
    configured = os.environ.get("CODEX_CLI_PATH")
    if configured and Path(configured).is_file():
        path = Path(configured)
        if path.suffix.lower() in (".cmd", ".ps1"):
            return npm_codex_command(path)
        return [str(path)]
    if os.name == "nt":
        local = os.environ.get("LOCALAPPDATA")
        if local:
            candidates = list((Path(local) / "OpenAI/Codex/bin").glob("*/codex.exe"))
            candidates.extend((Path(local) / "OpenAI/Codex/bin").glob("codex.exe"))
            if candidates:
                return [str(max(candidates, key=lambda path: path.stat().st_mtime))]
        native = shutil.which("codex.exe")
        if native:
            return [native]
        npm_launcher = shutil.which("codex.cmd") or shutil.which("codex.ps1")
        return npm_codex_command(Path(npm_launcher)) if npm_launcher else None
    executable = shutil.which("codex")
    return [executable] if executable else None


def run_codex(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = find_codex()
    if command is None:
        raise RuntimeError("Codex CLI is not on PATH.")
    return subprocess.run(
        [*command, *args],
        check=check,
        text=True,
        capture_output=True,
    )


def runtime_asset() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    architecture = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "arm64": "aarch64",
        "aarch64": "aarch64",
    }.get(machine)
    supported = {
        ("windows", "x86_64"),
        ("windows", "aarch64"),
        ("linux", "x86_64"),
        ("linux", "aarch64"),
        ("darwin", "x86_64"),
        ("darwin", "aarch64"),
    }
    if architecture is None or (system, architecture) not in supported:
        raise RuntimeError(f"No SubLuna runtime for {system}/{machine}.")
    suffix = ".exe" if system == "windows" else ""
    return f"subluna-hook-{system}-{architecture}{suffix}"


def runtime_paths() -> tuple[Path, Path]:
    suffix = ".exe" if os.name == "nt" else ""
    directory = repo_root() / "plugins/subluna/bin"
    return directory / f"subluna-hook{suffix}", directory / "runtime-version.txt"


def ensure_runtime() -> Path:
    target, marker = runtime_paths()
    supplied = os.environ.get("SUBLUNA_RUNTIME_BINARY")
    if supplied:
        source = Path(supplied).resolve()
        if not source.is_file():
            raise RuntimeError(f"SUBLUNA_RUNTIME_BINARY does not exist: {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    else:
        if target.is_file() and marker.is_file():
            if marker.read_text(encoding="utf-8").strip() == RUNTIME_VERSION:
                return target
        target.parent.mkdir(parents=True, exist_ok=True)
        asset = runtime_asset()
        base = f"{RUNTIME_REPOSITORY}/{RUNTIME_VERSION}/{asset}"
        try:
            binary = urllib.request.urlopen(base, timeout=30).read()
            checksum = urllib.request.urlopen(f"{base}.sha256", timeout=30).read().decode()
        except OSError as exc:
            raise RuntimeError(f"Could not download the native SubLuna runtime: {exc}") from exc
        expected = checksum.split()[0].lower()
        actual = hashlib.sha256(binary).hexdigest()
        if actual != expected:
            raise RuntimeError("Downloaded SubLuna runtime failed its SHA-256 check.")
        target.write_bytes(binary)

    if os.name != "nt":
        target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    marker.write_text(f"{RUNTIME_VERSION}\n", encoding="utf-8")
    return target


def app_server_request(method: str, params: dict[str, Any]) -> Any:
    command = find_codex()
    if command is None:
        raise RuntimeError("Codex CLI is not on PATH.")
    process = subprocess.Popen(
        [*command, "app-server", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert process.stdin and process.stdout

    def send(message: dict[str, Any]) -> None:
        process.stdin.write(json.dumps(message) + "\n")
        process.stdin.flush()

    def receive(response_id: int) -> Any:
        for _ in range(20):
            line = process.stdout.readline()
            if not line:
                break
            response = json.loads(line)
            if response.get("id") == response_id:
                if "error" in response:
                    raise RuntimeError(str(response["error"]))
                return response.get("result")
        raise RuntimeError("Codex app server did not return a hook status.")

    try:
        send(
            {
                "method": "initialize",
                "id": 0,
                "params": {
                    "clientInfo": {
                        "name": "subluna_doctor",
                        "title": "SubLuna doctor",
                        "version": "0.3.4",
                    }
                },
            }
        )
        receive(0)
        send({"method": "initialized", "params": {}})
        send({"method": method, "id": 1, "params": params})
        return receive(1)
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def parse_json_output(result: subprocess.CompletedProcess[str]) -> Any:
    return json.loads(result.stdout or "{}")


def marketplace_entries() -> list[dict[str, Any]]:
    result = run_codex("plugin", "marketplace", "list", "--json")
    payload = parse_json_output(result)
    return list(payload.get("marketplaces", []))


def install() -> int:
    root = repo_root()
    ensure_runtime()
    expected = root.resolve()
    existing = next((m for m in marketplace_entries() if m.get("name") == MARKETPLACE), None)
    if existing:
        current = Path(str(existing.get("root", ""))).resolve()
        if current != expected:
            raise RuntimeError(
                f"Marketplace '{MARKETPLACE}' already points to {current}, not {expected}. "
                "Remove or rename that marketplace before installing SubLuna."
            )
    else:
        run_codex("plugin", "marketplace", "add", str(root), "--json")
    run_codex("plugin", "add", f"{PLUGIN}@{MARKETPLACE}", "--json")
    print(
        "SubLuna files are installed, but automatic activation is not complete yet.\n"
        "Start a new Codex CLI session, enter /hooks, review the SubLuna hook, and choose Trust.\n"
        "Then run this launcher with 'verify'."
    )
    return doctor()


def uninstall() -> int:
    plugin_result = run_codex(
        "plugin", "remove", f"{PLUGIN}@{MARKETPLACE}", "--json", check=False
    )
    market_result = run_codex(
        "plugin", "marketplace", "remove", MARKETPLACE, "--json", check=False
    )
    failures = []
    for label, result in (("plugin", plugin_result), ("marketplace", market_result)):
        message = f"{result.stdout}\n{result.stderr}".lower()
        if result.returncode and not any(
            phrase in message
            for phrase in (
                "not found",
                "unknown marketplace",
                "not installed",
                "not configured",
            )
        ):
            failures.append(f"{label}: {(result.stderr or result.stdout).strip()}")
    if failures:
        raise RuntimeError("SubLuna uninstall failed: " + "; ".join(failures))
    runtime_directory = repo_root() / "plugins/subluna/bin"
    if runtime_directory.is_dir():
        shutil.rmtree(runtime_directory)
    print("SubLuna plugin and marketplace registration removed. Start a new task.")
    return 0


def doctor() -> int:
    root = repo_root()
    ensure_runtime()
    required = [
        root / MARKETPLACE_FILE,
        root / "plugins/subluna/.codex-plugin/plugin.json",
        root / "plugins/subluna/hooks/hooks.json",
        runtime_paths()[0],
        runtime_paths()[1],
        root / "plugins/subluna/skills/subluna/SKILL.md",
        root / "plugins/subluna/skills/subluna/references/policy.md",
        root / "plugins/subluna/skills/subluna/references/delegation-guide.md",
        root / "scripts/subluna.sh",
        root / "scripts/subluna.ps1",
        root / "UNINSTALL.md",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        print("Missing SubLuna files:\n" + "\n".join(missing), file=sys.stderr)
        return 1
    if find_codex() is None:
        print("Codex CLI is not on PATH.", file=sys.stderr)
        return 1
    marketplace = json.loads((root / MARKETPLACE_FILE).read_text(encoding="utf-8"))
    manifest = json.loads(
        (root / "plugins/subluna/.codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    if marketplace.get("name") != MARKETPLACE or manifest.get("name") != PLUGIN:
        print("SubLuna identifiers do not match the installer.", file=sys.stderr)
        return 1
    print("SubLuna doctor passed.")
    return 0


def verify() -> int:
    if doctor() != 0:
        return 1
    payload = app_server_request("hooks/list", {"cwds": [str(repo_root())]})
    hooks = [
        hook
        for entry in payload.get("data", [])
        for hook in entry.get("hooks", [])
        if hook.get("pluginId") == f"{PLUGIN}@{MARKETPLACE}"
        and hook.get("eventName") == "userPromptSubmit"
    ]
    if hooks and hooks[0].get("enabled") and hooks[0].get("trustStatus") == "trusted":
        print("SubLuna verified: its hook is enabled and trusted for Sol and Astra turns.")
        return 0
    status = hooks[0].get("trustStatus", "missing") if hooks else "missing"
    print(
        f"SubLuna automatic activation is not ready. Hook status: {status}.\n"
        "Start a new Codex CLI session, enter /hooks, review the SubLuna hook, and choose Trust.\n"
        "Run this verification again afterward.",
        file=sys.stderr,
    )
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Install, remove, or check SubLuna.")
    parser.add_argument("command", choices=("install", "uninstall", "doctor", "verify"))
    args = parser.parse_args()
    try:
        return {
            "install": install,
            "uninstall": uninstall,
            "doctor": doctor,
            "verify": verify,
        }[args.command]()
    except (OSError, RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"SubLuna {args.command} failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
