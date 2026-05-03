#!/usr/bin/env bash
set -e

SHELL_RC="$HOME/.zshrc"
MARKER="# shell-aliases"

if ! grep -q "$MARKER" "$SHELL_RC" 2>/dev/null; then
    echo "Not installed."
    exit 0
fi

# Remove the marker line and all source lines that follow it belonging to this repo
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
grep -v "$MARKER" "$SHELL_RC" | grep -v "source \"$REPO_DIR" > "$SHELL_RC.tmp"
mv "$SHELL_RC.tmp" "$SHELL_RC"

echo "Uninstalled. Run: source ~/.zshrc"
