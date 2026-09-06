#!/usr/bin/env bash
# check-models — depodaki AI yapılandırmasında yasak model beyanı arar (haiku · eski nesil tam kimlik).
# Politika: .claude/agents/README.md → Model politikası (DECISIONS#0040).
# Kullanım: bash .claude/scripts/check-models.sh [kök]
# Exit: 0 = temiz · 1 = yasak model bulundu
#
# K0/K1 hook'u (`ceran-hooks model-guard`, allowlist) yalnız BU oturumdaki yazmayı engeller. Bu script
# dosya nereden gelirse gelsin (başka makine, merge, elle düzenleme) kapıyı kapatır;
# CI adımı olarak koşar. İkisi aynı kuralın iki yüzeyidir.
set -uo pipefail

ROOT="${1:-${CLAUDE_PROJECT_DIR:-$PWD}}"
cd "$ROOT" || { echo "check-models: kök bulunamadı: $ROOT" >&2; exit 1; }

python3 - "$ROOT" <<'PY'
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
# haiku (her sürüm) + eski nesil TAM kimlikler (claude-3*, claude-{opus,sonnet}-4*): model alias ile
# yazılır (`opus` · `sonnet` · `inherit`), kimlik sabitlenmez — sabitlenen kimlik model değişince
# sessizce eskir (DECISIONS#0043).
BLOCKED = re.compile(r"haiku|claude-3(?:[-.]|$)|claude-(?:opus|sonnet)-4(?:[-.\[]|$)", re.IGNORECASE)
MODEL_DECL = re.compile(r"""^\s*["']?model["']?\s*:\s*["']?([^"',\n]+)""", re.MULTILINE)
MODEL_DECL_LOOSE = re.compile(r"""["']?model["']?\s*:\s*["']?([^"',\n}]+)""")


def walk_models(node, path="$"):
    """JSON ağacındaki her `model` anahtarını (iç içe olanlar dahil) verir."""
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}"
            if key == "model" and isinstance(value, str):
                yield here, value
            else:
                yield from walk_models(value, here)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from walk_models(value, f"{path}[{i}]")

targets = []
targets += sorted((root / ".claude" / "agents").glob("*.md"))
targets += sorted((root / ".claude" / "skills").glob("*/SKILL.md"))
targets += [p for p in (root / ".claude").glob("settings*.json") if p.is_file()]

findings = []
for path in targets:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        continue

    rel = path.relative_to(root).as_posix()

    if path.suffix == ".json":
        # JSON'da `model` satır başında olmayabilir ({"model": "..."}); yapıyı gez.
        try:
            data = json.loads(text)
        except ValueError:
            data = None
        if data is None:
            for m in MODEL_DECL_LOOSE.finditer(text):
                if BLOCKED.search(m.group(1)):
                    findings.append((rel, text[: m.start()].count("\n") + 1, "model: " + m.group(1).strip()))
            continue
        for where, value in walk_models(data):
            if BLOCKED.search(str(value)):
                findings.append((rel, 0, f"{where} = {value}"))
        continue

    if path.suffix == ".md":
        # Yalnız frontmatter: gövdedeki "haiku" kelimesi bir beyan değildir.
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        text = text[: end if end != -1 else len(text)]

    for m in MODEL_DECL.finditer(text):
        value = m.group(1).strip()
        if BLOCKED.search(value):
            line = text[: m.start()].count("\n") + 1
            findings.append((rel, line, "model: " + value))

if findings:
    print("[check-models] YASAK MODEL — yalnız opus ve sonnet alias'ları kullanılır; haiku ve eski nesil tam kimlikler yasak (agents/README.md).")
    for rel, line, value in findings:
        where = f"{rel}:{line}" if line else rel
        print(f"  {where} — {value}")
    sys.exit(1)

print(f"[check-models] temiz — {len(targets)} dosya denetlendi (agents · skills · settings).")
PY
