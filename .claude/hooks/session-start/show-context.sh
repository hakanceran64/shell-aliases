#!/usr/bin/env bash
# show-context — oturum açılışında proje özetini göster
# Event: SessionStart | Matcher: *
# Kaynak: fire-and-water show-roster (proje-bağımsız hale getirildi)
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$PROJECT_ROOT"

PROJECT="$(basename "$PROJECT_ROOT")"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '-')"
if git rev-parse --git-dir >/dev/null 2>&1; then
  DIRTY="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
else
  DIRTY=0
fi

{
  echo "📁 $PROJECT | branch: $BRANCH | kirli dosya: $DIRTY"
  [[ -f CLAUDE.md ]]        && echo "Bağlam: CLAUDE.md"
  [[ -d .claude/rules ]]    && echo "Kurallar: .claude/rules/"
  [[ -d .claude/skills ]]   && echo "Skills: .claude/skills/"
  [[ -d .claude/agents ]]   && echo "Agents: .claude/agents/"
} >&2

exit 0
