#!/bin/sh
# SUBLUNA-MANAGED: POSIX installer and uninstaller launcher.
set -eu

subluna_script="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/subluna.py"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$subluna_script" "$@"
fi
if command -v python >/dev/null 2>&1; then
    exec python "$subluna_script" "$@"
fi

echo "SubLuna requires Python 3." >&2
exit 1
