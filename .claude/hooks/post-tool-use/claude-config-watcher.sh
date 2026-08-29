#!/usr/bin/env bash
# claude-config-watcher — .claude/** veya CLAUDE.md değişikliklerini yakalar:
#   1) operatöre bildirir
#   2) proje .claude/CHANGELOG.md'ye satır ekler
#   3) claude-foundation'a "sync gerekli" sinyali bırakır
# Event: PostToolUse | Matcher: Edit|Write|MultiEdit
# Governance: claude-foundation/docs/GOVERNANCE.md (#0010)
# Kaynak ilham: tof-camera-mastery'nin .claude değişiklik izleyicisi (genişletildi)
set -euo pipefail

INPUT="$(cat)"
PARSED="$(printf '%s' "$INPUT" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    ti = d.get("tool_input", {})
    print((d.get("tool_name") or "") + "\t" + (ti.get("file_path") or ti.get("path") or ""))
except Exception:
    pass
')"
TOOL="$(printf '%s' "$PARSED" | cut -f1)"
FILE_PATH="$(printf '%s' "$PARSED" | cut -f2)"

[[ -z "$FILE_PATH" ]] && exit 0

# claude-foundation kendi sources/ aynasını izleme (yanlış pozitif önle).
# Worktree'ler burada da elenir: içeride kendi .claude/'u olan bir çalışma kopyası
# aşağıdaki $REL eşleşmesinden (son /.claude/ parçası alınır) kaçardı.
case "$FILE_PATH" in
  */claude-foundation/sources/*|*/claude-foundation/kit/*) exit 0 ;;
  */.claude/worktrees/*) exit 0 ;;
esac

# İlgili mi? Hangi merkez repoya ait?
#   .claude/** + CLAUDE.md  → claude-foundation (AI altyapısı)
#   .ceran/**               → developer-toolkit (ekosistem manifesti)
#   tasarım token dosyaları → ceran-design-system
TARGET_REPO="claude-foundation"
case "$FILE_PATH" in
  */.claude/*)            REL=".claude/${FILE_PATH##*/.claude/}" ;;
  */CLAUDE.md|CLAUDE.md)  REL="CLAUDE.md" ;;
  */CLAUDE.local.md|CLAUDE.local.md) REL="CLAUDE.local.md" ;;
  */.ceran/*)             REL=".ceran/${FILE_PATH##*/.ceran/}"; TARGET_REPO="developer-toolkit" ;;
  */tokens.css|*/tokens.json|*/design-tokens.*)
                          REL="${FILE_PATH##*/}"; TARGET_REPO="ceran-design-system" ;;
  *) exit 0 ;;
esac

# Gürültü dosyalarını atla.
#   - settings.local.json: makineye özel, kit'e girmez
#   - CHANGELOG.md: bu hook'un kendi çıktısı (yoksa sonsuz döngü)
#   - .ceran/lock.yaml: üretilen
#   - .claude/projects/**, .claude/plans/**, .claude/todos/**, .claude/shell-snapshots/**:
#     Claude Code'un KENDİ oturum state'i (memory, plan, todo, snapshot). Kit curation'ı
#     ilgilendirmez; sinyal üretirse kuyruk okunmaz hale gelir.
#   - .claude/worktrees/**: Claude Code'un çalışma kopyaları — config değil, üstelik içerideki
#     dosya proje kaynağının kopyası. sync-sources.sh bunları zaten arşivden hariç tutuyordu.
case "$REL" in
  .claude/settings.local.json|*CHANGELOG.md|.ceran/lock.yaml) exit 0 ;;
  .claude/projects/*|.claude/plans/*|.claude/todos/*|.claude/shell-snapshots/*|.claude/statsig/*) exit 0 ;;
  .claude/worktrees/*) exit 0 ;;
esac

# Üretilen tasarım çıktısına elle dokunulmuş: bu bir HATA, sinyal değil.
case "$FILE_PATH" in
  */ceran-design-system/dist/*)
    echo "⛔ [claude-config-watcher] dist/ ÜRETİLEN dizindir — elle düzenlenmez." >&2
    echo "   Değeri tokens/ altında değiştir, sonra: node build/build.mjs" >&2
    exit 2 ;;
esac

TS="$(date '+%Y-%m-%d %H:%M')"

# Proje kimliği DÜZENLENEN DOSYANIN repo kökünden gelir — `pwd`'den değil. Bash cwd'i bir alt
# dizindeyken `basename "$(pwd)"` sahte proje adı üretiyordu: 3d-printer'ın alt ağaçlarındaki
# CLAUDE.md düzenlemeleri kuyruğa "crealityhub" · "backend" · "control-center" diye üç ayrı
# proje olarak düştü ve hangi reponun sinyali olduğu kaybolmuştu.
FILE_DIR="$(cd "$(dirname "$FILE_PATH")" 2>/dev/null && pwd -P || true)"
REPO_ROOT="$(git -C "${FILE_DIR:-.}" rev-parse --show-toplevel 2>/dev/null || true)"
# git dışı bir ağaçta repo kökü yok: eski davranışa (cwd) dön — dosyanın kendi dizinine
# düşmek "rules"/"hooks" gibi anlamsız proje adları üretirdi.
[[ -z "$REPO_ROOT" ]] && REPO_ROOT="$(pwd)"
PROJECT="$(basename "$REPO_ROOT")"

# Kuyruğa yazılan yol repo köküne görelidir; aynı repoda birden fazla CLAUDE.md varsa
# (alt-ağaç) hangisinin değiştiği ayırt edilebilsin. $REL (yalnız .claude/** için anlamlı)
# gürültü eşleşmesinde kullanılmaya devam eder.
# Karşılaştırma FİZİKSEL yol üzerinden yapılır: $FILE_PATH ham gelebilir (/var/...) ama
# `git rev-parse` symlink'i açar (/private/var/...) — $FILE_DIR bu yüzden `pwd -P` ile çözülür.
FILE_ABS="${FILE_DIR:+$FILE_DIR/}$(basename "$FILE_PATH")"
case "$FILE_ABS" in
  "$REPO_ROOT"/*) REL_OUT="${FILE_ABS#"$REPO_ROOT"/}" ;;
  *)              REL_OUT="$REL" ;;
esac

# 1) Operatöre bildir
echo "📢 [claude-config-watcher] '$PROJECT' içinde değişti → $REL_OUT  [$TS]"
echo "   → $TARGET_REPO'a senkronlamayı değerlendir (sources sync / kit curation)."

# 2) Proje .claude/CHANGELOG.md (repo kökünde — cwd nerede olursa olsun tek günlük)
if [[ -d "$REPO_ROOT/.claude" ]]; then
  CL="$REPO_ROOT/.claude/CHANGELOG.md"
  [[ -f "$CL" ]] || printf '# .claude değişiklik günlüğü\n\n' > "$CL"
  printf -- '- [%s] `%s` değişti\n' "$TS" "$REL_OUT" >> "$CL"
fi

# 3) claude-foundation'a sync sinyali (varsa; aynı proje+yol zaten bekliyorsa tekrarlanmaz)
# Hedef, ekosistem kökündeki KANONİK checkout'tur — eco.py ile aynı çözümleme sırası.
FOUNDATION_DIR="${CLAUDE_FOUNDATION_DIR:-${CERAN_ECOSYSTEM_ROOT:-$HOME/Backup/GitHub/hakanceran64}/core/claude-foundation}"

# Vendor/submodule kopyası hedef gösterilirse kuyruk okunmayan bir yere yazılır.
# Sessiz veri kaybı yerine uyar ve sinyali atla (2026-08-16: Node/claude-foundation
# 2f7b14c'de çakılıyken 21 madde burada kaybolmuştu).
if git -C "$FOUNDATION_DIR" rev-parse --show-superproject-working-tree 2>/dev/null | grep -q .; then
  echo "⚠ [claude-config-watcher] FOUNDATION_DIR bir submodule checkout'u: $FOUNDATION_DIR" >&2
  echo "   Kuyruk kimse tarafından okunmaz. CLAUDE_FOUNDATION_DIR'i ekosistem checkout'una çevir." >&2
  exit 0
fi

if [[ -d "$FOUNDATION_DIR/docs" ]]; then
  QUEUE="$FOUNDATION_DIR/docs/sync-queue.jsonl"
  # sync-review.sh (read-then-truncate) ile yarışmamak için mkdir spin-lock (sınırlı deneme)
  LOCKDIR="$QUEUE.lock"
  ACQUIRED=0
  for _ in {1..25}; do
    if mkdir "$LOCKDIR" 2>/dev/null; then ACQUIRED=1; break; fi
    sleep 0.2
  done
  if [[ "$ACQUIRED" -ne 1 ]]; then
    echo "⚠ [claude-config-watcher] sync-queue lock alınamadı ($LOCKDIR) — sinyal bu sefer atlandı." >&2
    exit 0
  fi
  trap 'rmdir "$LOCKDIR" 2>/dev/null || true' EXIT
  if [[ -f "$QUEUE" ]] && grep -F "\"project\": \"$PROJECT\", \"path\": \"$REL_OUT\"" "$QUEUE" 2>/dev/null \
       | grep -qF '"status": "pending"'; then
    exit 0
  fi
  # insan-okunur checklist (SYNC-QUEUE.md'de "Bekleyenler" son bölümdür — append oraya düşer)
  SYNC_MD="$FOUNDATION_DIR/docs/SYNC-QUEUE.md"
  [[ -f "$SYNC_MD" ]] && printf -- '- [ ] [%s] **%s** → `%s` — gözden geçir / sources sync / kit curation\n' \
    "$TS" "$PROJECT" "$REL_OUT" >> "$SYNC_MD"
  # makine-okunur, işlenebilir sinyal (scripts/sync-review.sh tüketir)
  python3 -c 'import json,sys; print(json.dumps({"ts":sys.argv[1],"project":sys.argv[2],"path":sys.argv[3],"tool":sys.argv[4],"target":sys.argv[5],"status":"pending"}, ensure_ascii=False))' \
    "$TS" "$PROJECT" "$REL_OUT" "$TOOL" "$TARGET_REPO" >> "$QUEUE"
fi

exit 0
