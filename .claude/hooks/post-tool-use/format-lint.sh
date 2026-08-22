#!/usr/bin/env bash
# format-lint — düzenlenen dosyayı projenin formatter'ı ile biçimlendirir, linter'ı ile denetler.
# Event: PostToolUse | Matcher: Edit|Write|MultiEdit
# Sözleşme: .claude/quality.json → on_edit[] (match glob · format · lint; {file} yer tutucu)
# Exit: 0 = temiz veya atlandı · 2 = lint bulgusu (stderr Claude'a feedback olur)
#
# Fail-open: quality.json yok · glob eşleşmedi · araç kurulu değil → sessizce 0.
# Böylece toolchain'i olmayan makinede oturum kilitlenmez; kapı yalnız araç varken kapanır.
# on_edit komutları TEK DOSYA kapsamlı ve hızlı olmalı (hook timeout'u paylaşılır).
set -uo pipefail

INPUT="$(cat)"
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
CONF="$ROOT/.claude/quality.json"
[[ -f "$CONF" ]] || exit 0

# Eşleşen kuralı çöz: "<format|lint>\t<komut>" satırları. Yol shlex ile kaçırılır.
RESOLVED="$(printf '%s' "$INPUT" | CONF="$CONF" ROOT="$ROOT" python3 -c '
import fnmatch, json, os, shlex, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = data.get("tool_input") or {}
file_path = tool_input.get("file_path") or tool_input.get("path") or ""
if not file_path:
    sys.exit(0)

root = os.environ["ROOT"]
relative_path = os.path.relpath(file_path, root)
if relative_path.startswith(".."):      # proje dışı dosya — dokunma
    sys.exit(0)

try:
    with open(os.environ["CONF"]) as handle:
        config = json.load(handle)
except Exception:
    sys.exit(0)

for rule in config.get("on_edit") or []:
    pattern = rule.get("match") or ""
    if not pattern:
        continue
    if not (fnmatch.fnmatch(relative_path, pattern)
            or fnmatch.fnmatch(os.path.basename(relative_path), pattern)):
        continue
    for kind in ("format", "lint"):
        command = (rule.get(kind) or "").strip()
        if command:
            print(kind + "\t" + command.replace("{file}", shlex.quote(relative_path)))
    break
')"

[[ -n "$RESOLVED" ]] || exit 0

STATUS=0
while IFS=$'\t' read -r KIND COMMAND; do
  [[ -n "${COMMAND:-}" ]] || continue
  BIN="${COMMAND%% *}"
  # Araç yoksa sessizce atla (fail-open). Göreli yol da desteklenir: ./node_modules/.bin/*
  ( cd "$ROOT" && command -v "$BIN" >/dev/null 2>&1 ) || continue

  OUTPUT="$(cd "$ROOT" && eval "$COMMAND" 2>&1)"; RC=$?
  if [[ "$KIND" == "lint" && "$RC" -ne 0 ]]; then
    {
      printf '%s\n' "[format-lint] LINT BULGUSU (exit $RC): $COMMAND"
      printf '%s\n' "$OUTPUT" | head -40
      printf '%s\n' "[format-lint] Düzelt ve devam et. Kapı: .claude/quality.json → on_edit"
    } >&2
    STATUS=2
  fi
done <<< "$RESOLVED"

exit "$STATUS"
