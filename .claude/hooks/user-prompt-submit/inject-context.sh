#!/usr/bin/env bash
# inject-context — kullanıcı prompt'una güncel proje bağlamını ekle
# Event: UserPromptSubmit | Matcher: *
# Output: stdout'a hookSpecificOutput.additionalContext JSON (UserPromptSubmit şeması)
# Kaynak: fire-and-water inject-context (proje-bağımsız hale getirildi)
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$PROJECT_ROOT"

PROJECT="$(basename "$PROJECT_ROOT")"
LOCAL_DATE="$(date +%F)"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '-')"
if git rev-parse --git-dir >/dev/null 2>&1; then
  DIRTY="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
else
  DIRTY=0
fi

# JSON'u güvenli üret (proje/branch adındaki özel karakterler kaçırılır)
python3 - "$PROJECT" "$LOCAL_DATE" "$BRANCH" "$DIRTY" <<'PY'
import json, sys
project, date, branch, dirty = sys.argv[1:5]
ctx = (
    f"## Proje Bağlamı ({project})\n"
    f"- Tarih: {date} | branch: {branch} | kirli dosya: {dirty}\n"
    "- Kurallar .claude/rules/ altında otomatik bağlayıcıdır."
)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": ctx,
    }
}, ensure_ascii=False))
PY

exit 0
