#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHELL_RC="$HOME/.zshrc"
MARKER="# shell-aliases"

if grep -q "$MARKER" "$SHELL_RC" 2>/dev/null; then
    echo "Already installed. Run uninstall.sh first to reinstall."
    exit 0
fi

echo "" >> "$SHELL_RC"
echo "$MARKER" >> "$SHELL_RC"
for file in "$REPO_DIR"/aliases/*.sh; do
    echo "source \"$file\"" >> "$SHELL_RC"
done

echo "Installed. Run: source ~/.zshrc"
