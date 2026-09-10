<!-- SUBLUNA-MANAGED: uninstall breadcrumb. -->

# Remove SubLuna

From this repository, run:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/subluna.ps1 uninstall
Linux/macOS: sh scripts/subluna.sh uninstall
```

Without the repository, run:

```text
codex plugin remove subluna@subluna
codex plugin marketplace remove subluna
```

Then start a new Codex task. Existing tasks retain the context they started with.

SubLuna creates no global `AGENTS.md` block and copies no standalone skill into `~/.codex/skills`. Codex owns the installed plugin cache and removes it through `codex plugin remove`. The repository launcher also removes the downloaded runtime from `plugins/subluna/bin`.

To look for residue, use `codex plugin list --available --json`, `codex plugin marketplace list --json`, and search `~/.codex` plus `~/.agents` for `subluna`. Do not delete a match until you confirm it belongs to this plugin.
