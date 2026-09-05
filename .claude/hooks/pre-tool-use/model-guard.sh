#!/usr/bin/env bash
# model-guard — yasak model (haiku · eski nesil tam kimlik) kullanımını engeller.
# Politika: kit/.claude/agents/README.md → Model politikası (DECISIONS#0040).
# Event: PreToolUse | Matcher: Task|Agent|Write|Edit|MultiEdit
# Input: stdin JSON ({tool_name, tool_input{...}})
# Exit: 0 = izin ver, 2 = engelle (stderr Claude'a feedback olur)
#
# İki yüzeyi birden kapatır:
#   1) Çalışma anı — bir subagent `model: haiku` ile çağrılırsa çağrı engellenir.
#   2) Yapılandırma — `.claude/agents/*.md`, `skills/**/SKILL.md` ve `settings*.json`
#      dosyalarına haiku YAZILMASI engellenir (dosya diske hiç düşmez).
# haiku ve eski nesil tam kimlikler (claude-3*, claude-{opus,sonnet}-4*) engellenir; tanınmayan
# değer işi durdurmaz — `opus`, `sonnet`, `inherit`, `claude-opus-5`, `sonnet[1m]` serbesttir.
set -uo pipefail

INPUT="$(cat)"

VERDICT="$(printf '%s' "$INPUT" | python3 -c '
import json, re, sys

# haiku (her sürüm) + eski nesil TAM kimlikler (claude-3*, claude-{opus,sonnet}-4*): model alias ile
# yazılır (`opus` · `sonnet` · `inherit`), kimlik sabitlenmez — sabitlenen kimlik model değişince
# sessizce eskir (DECISIONS#0043).
BLOCKED = re.compile(r"haiku|claude-3(?:[-.]|$)|claude-(?:opus|sonnet)-4(?:[-.\[]|$)", re.IGNORECASE)
# Korunan yapılandırma dosyaları (repo köküne göre eşleşir; mutlak yol da çalışır).
GUARDED = (
    re.compile(r"(^|/)\.claude/agents/[^/]+\.md$"),
    re.compile(r"(^|/)\.claude/skills/.+/SKILL\.md$"),
    re.compile(r"(^|/)\.claude/settings(\.local)?\.json$"),
)
# frontmatter `model: x` veya JSON `"model": "x"`
MODEL_DECL = re.compile(r"""^\s*["\x27]?model["\x27]?\s*:\s*["\x27]?([^"\x27,\n]+)""", re.MULTILINE)
# settings*.json tek satıra sığabilir ({"model": "..."}); orada satır başı şartı aranmaz.
MODEL_DECL_JSON = re.compile(r"""["\x27]?model["\x27]?\s*:\s*["\x27]?([^"\x27,\n}]+)""")

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool = data.get("tool_name") or ""
ti = data.get("tool_input") or {}


def fail(where, value):
    print(f"{where}\t{value.strip()}")
    sys.exit(0)


if tool in ("Task", "Agent"):
    model = str(ti.get("model") or "")
    if BLOCKED.search(model):
        fail(f"{tool} cagrisindaki model parametresi", model)
    sys.exit(0)

if tool in ("Write", "Edit", "MultiEdit"):
    path = str(ti.get("file_path") or ti.get("path") or "")
    if not any(rx.search(path) for rx in GUARDED):
        sys.exit(0)

    chunks = []
    if tool == "Write":
        chunks.append(str(ti.get("content") or ""))
    elif tool == "Edit":
        chunks.append(str(ti.get("new_string") or ""))
    else:
        for e in ti.get("edits") or []:
            chunks.append(str((e or {}).get("new_string") or ""))

    decl = MODEL_DECL_JSON if path.endswith(".json") else MODEL_DECL
    for chunk in chunks:
        for m in decl.finditer(chunk):
            if BLOCKED.search(m.group(1)):
                fail(path, m.group(1))
sys.exit(0)
')"

[[ -n "$VERDICT" ]] || exit 0

WHERE="${VERDICT%%$'\t'*}"
VALUE="${VERDICT##*$'\t'}"

{
  printf '%s\n' "[model-guard] ENGELLENDİ — haiku ve eski nesil model kimlikleri yasak (agents/README.md → Model politikası)."
  printf '%s\n' "  Yer:   $WHERE"
  printf '%s\n' "  Değer: $VALUE"
  printf '%s\n' "  İzinli: opus (Opus 5) · sonnet (Sonnet 5) — alias yaz, tam kimlik sabitleme."
  printf '%s\n' "  Gerekçe: 'basit iş' diye ayrılan adım da kural ihlal edebilir ve ucuz model"
  printf '%s\n' "  bunu sessizce kaçırır. Maliyet modeli küçülterek değil BAĞLAMI küçülterek düşer."
} >&2
exit 2
