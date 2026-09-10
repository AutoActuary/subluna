<!-- SUBLUNA-MANAGED: repository instructions. Removing this repository removes this file. -->

# SubLuna repository instructions

When the user asks to install this repository, read `README.md`, detect the operating system, and run the matching launcher:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/subluna.ps1 install
Linux/macOS: sh scripts/subluna.sh install
```

After installation, tell the user to open a new Codex CLI session, enter `/hooks`, review the SubLuna hook, and choose Trust. Then use the launcher with `verify`. Do not claim automatic activation until verification prints `SubLuna verified`. When the user asks to remove or uninstall SubLuna, run the launcher with `uninstall`. If the repository is unavailable, run:

```text
codex plugin remove subluna@subluna
codex plugin marketplace remove subluna
```

Do not edit global `AGENTS.md` or copy SubLuna files into loose user directories. Preserve unrelated Codex settings and plugins.

For repository changes, run the Rust and Python tests plus the validators named in `README.md`.
