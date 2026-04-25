#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
UV="$(command -v uv || true)"

if [ -z "$UV" ]; then
    echo "uv not found on PATH. install via https://docs.astral.sh/uv/" >&2
    exit 1
fi

LABEL="local.adhan-todoist"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"

mkdir -p "$HOME/Library/LaunchAgents"

sed -e "s|__UV__|${UV}|g" -e "s|__REPO__|${REPO}|g" \
    "${REPO}/adhan-todoist.plist.template" > "${PLIST}"

launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "${PLIST}"

echo "installed: ${PLIST}"
echo "label: ${LABEL}"
echo "schedule: 01:00 daily"
