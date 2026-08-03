#!/usr/bin/env bash
# wrap-up — oturum kapanışında commit edilmemiş değişiklik özeti
# Event: Stop | Matcher: *
# Kaynak: fire-and-water wrap-up (proje-bağımsız)
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$PROJECT_ROOT"

if git rev-parse --git-dir >/dev/null 2>&1; then
  CHANGED="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
else
  CHANGED=0
fi
if [[ "$CHANGED" -gt 0 ]]; then
  {
    echo "[wrap-up] $CHANGED dosya commit edilmemiş. Commit etmeyi unutma."
    git status --porcelain 2>/dev/null | head -10
  } >&2
fi

exit 0
