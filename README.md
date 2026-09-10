<!-- SUBLUNA-MANAGED: public repository entry point. -->

# SubLuna

Lead-model judgment, Luna execution.

SubLuna is a Codex plugin that gives Sol and Astra user turns a compact delegation policy. The lead keeps framing, architecture, integration, verification, and final judgment. Luna handles bounded work that can be briefed and checked cheaply, with close calls routed toward Luna.

It sends no policy tokens to Terra, Luna, or other models. Codex still starts the small native gate because `UserPromptSubmit` does not support model matchers. Say `no subluna` to disable it for one turn. Avoid `$subluna` and `/subluna` in an opt-out because the composer can treat them as explicit skill invocations.

The plugin is the installable package. Its bundled skill provides the optional `$subluna` invocation supported by Codex. Automatic Sol and Astra activation comes from the plugin hook, not implicit skill selection.

Codex currently exposes the model slug, but not reasoning effort, to hooks or the running model. SubLuna therefore cannot reliably distinguish medium, high, or xhigh from low. Its automatic gate is Sol and Astra only.

## Supported systems

SubLuna supports Codex Desktop and CLI on Windows, plus Codex CLI on Linux and macOS. Its per-turn gate is a small Rust executable with no interpreter or package startup. GitHub Actions builds the release artifacts from the source in `native-hook`. The installer downloads the correct artifact and verifies its SHA-256 hash. Users do not need Rust or a compiler. Python 3 and PowerShell or POSIX `sh` are used only during installation.

## Install

Give Codex this repository and say:

```text
Install <path-to-this-repository>
```

Codex should follow `AGENTS.md` and choose the correct launcher:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/subluna.ps1 install
Linux/macOS: sh scripts/subluna.sh install
```

### Required trust step

Codex cannot trust a third-party hook on your behalf. Installation is incomplete until you do this:

1. Start a new Codex CLI session.
2. Enter `/hooks`.
3. Select the SubLuna `UserPromptSubmit` hook. Confirm that it points to `bin/subluna-hook` inside the SubLuna plugin.
4. Choose **Trust**.
5. Exit that session and run the matching launcher with `verify`:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/subluna.ps1 verify
Linux/macOS: sh scripts/subluna.sh verify
```

Only the `SubLuna verified` result confirms automatic Sol and Astra activation. Updating SubLuna changes the hook hash, so Codex will require this review again.

## Uninstall

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/subluna.ps1 uninstall
Linux/macOS: sh scripts/subluna.sh uninstall
```

The equivalent manual commands are:

```text
codex plugin remove subluna@subluna
codex plugin marketplace remove subluna
```

SubLuna does not alter global `AGENTS.md` or install loose skill files. See [UNINSTALL.md](UNINSTALL.md) for recovery and residue checks.

## Verify the repository

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/subluna.ps1 doctor
Linux/macOS: sh scripts/subluna.sh doctor
```

Run `cargo test --manifest-path native-hook/Cargo.toml`, build the release runtime, set `SUBLUNA_RUNTIME_BINARY` to that binary, then run the Python suite. The setup agent should also locate and run Codex's `validate_plugin.py` and `quick_validate.py` against `plugins/subluna` and `plugins/subluna/skills/subluna`.

The optional [delegation guide](plugins/subluna/skills/subluna/references/delegation-guide.md) records the tested mapping, limits, and brief format. It is loaded only when the compact policy leaves a worthwhile ambiguity.
