#!/usr/bin/env bash
# verify.sh — .claude/quality.json → verify{} komutlarını sırayla çalıştırır (repo-geneli kalite kapısı).
#
# Kullanım:
#   bash .claude/scripts/verify.sh                # format → lint → typecheck → test
#   bash .claude/scripts/verify.sh lint test      # yalnız seçilen adımlar
#   bash .claude/scripts/verify.sh --strict       # araç kurulu değilse ATLAMA, HATA ver (CI)
#
# Exit: 0 = tüm adımlar geçti veya tanımsız · 1 = bir adım başarısız (ilk hatada durur)
#
# Tanımsız (boş) komut atlanır: her profilde her adım anlamlı değildir (ör. docs-only'de test yok).
# --strict CI içindir: orada "araç yok" sessiz geçilirse kapı yeniden tavsiyeye döner.
#
# Adımlardan ÖNCE kit politikaları koşar (yapılandırılamaz, hep açık): şu an yalnız model
# politikası (check-models.sh). Bunlar quality.json'a bağlı değildir çünkü stack'e değil KİTE
# aittir; profil dosyasına konsaydı her profilde tekrarlanır ve biri unutulduğunda sessizce düşerdi.
# Script yoksa atlanır (eski kit vendor'lamış proje kilitlenmesin); varsa ihlalde kapı KAPANIR.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONF="$ROOT/.claude/quality.json"

STRICT=0; STEPS=()
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}"; exit 0 ;;
    -*) echo "HATA: bilinmeyen seçenek: $arg" >&2; exit 2 ;;
    *) STEPS+=("$arg") ;;
  esac
done
[[ ${#STEPS[@]} -eq 0 ]] && STEPS=(format lint typecheck test)

if [[ ! -f "$CONF" ]]; then
  echo "verify: .claude/quality.json yok — kalite kapısı tanımlı değil." >&2
  [[ "$STRICT" -eq 1 ]] && exit 1
  exit 0
fi

# --- kit politikaları (yapılandırılamaz) ---------------------------------
POLICY="$ROOT/.claude/scripts/check-models.sh"
if [[ -f "$POLICY" ]]; then
  if OUT="$(bash "$POLICY" "$ROOT" 2>&1)"; then
    printf '  ✓ %-9s model politikası\n' "politika"
  else
    printf '  ✗ %-9s model politikası\n' "politika"
    printf '%s\n' "$OUT" >&2
    echo "verify: 'politika' adımı geçmedi." >&2
    exit 1
  fi
else
  printf '  · %-9s check-models.sh yok — atlandı\n' "politika"
fi

FAILED=""
for step in "${STEPS[@]}"; do
  CMD="$(CONF="$CONF" STEP="$step" python3 -c '
import json, os, sys
try:
    with open(os.environ["CONF"]) as handle:
        print(((json.load(handle).get("verify") or {}).get(os.environ["STEP"]) or "").strip())
except Exception:
    sys.exit(1)
')" || { echo "verify: quality.json okunamadı" >&2; exit 1; }

  if [[ -z "$CMD" ]]; then
    printf '  · %-9s tanımsız — atlandı\n' "$step"
    continue
  fi

  BIN="${CMD%% *}"
  if ! ( cd "$ROOT" && command -v "$BIN" >/dev/null 2>&1 ); then
    if [[ "$STRICT" -eq 1 ]]; then
      printf '  ✗ %-9s araç yok: %s (--strict)\n' "$step" "$BIN"
      FAILED="$step"; break
    fi
    printf '  ⚠ %-9s araç yok: %s — atlandı\n' "$step" "$BIN"
    continue
  fi

  printf '  → %-9s %s\n' "$step" "$CMD"
  if ! ( cd "$ROOT" && eval "$CMD" ); then
    printf '  ✗ %-9s BAŞARISIZ\n' "$step"
    FAILED="$step"; break
  fi
  printf '  ✓ %-9s geçti\n' "$step"
done

if [[ -n "$FAILED" ]]; then
  echo "verify: '$FAILED' adımı geçmedi." >&2
  exit 1
fi
echo "verify: kalite kapısı geçildi."
