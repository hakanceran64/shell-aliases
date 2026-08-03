# Hooks — kanonik set

Olay-bazlı, **proje-bağımsız** hook'lar. Hepsi bağımsız `.sh` dosyası (test edilebilir, yeniden
kullanılabilir). Bağlama `../settings.json` içindedir.

| Olay | Hook | Görev |
|------|------|-------|
| SessionStart | `session-start/show-context.sh` | proje · branch · kirli dosya · mevcut .claude bölümleri |
| UserPromptSubmit | `user-prompt-submit/inject-context.sh` | her prompt'a güncel proje bağlamı (JSON) |
| PreToolUse(Bash) | `pre-tool-use/bash-guard.sh` | yıkıcı komutları engelle (exit 2) |
| PostToolUse(Edit\|Write) | `post-tool-use/claude-config-watcher.sh` | **`.claude`/`CLAUDE.md` değişikliğini bildir + changelog + foundation sync sinyali** |
| Stop | `stop/wrap-up.sh` | commit edilmemiş dosya özeti (async) |

## claude-config-watcher (governance)

Projedeki `.claude/**` veya `CLAUDE.md` her değiştiğinde:
1. Operatöre `📢` ile bildirir,
2. `.claude/CHANGELOG.md`'ye satır ekler,
3. foundation'a iki sinyal bırakır: insan-okunur `docs/SYNC-QUEUE.md` + makine-okunur
   `docs/sync-queue.jsonl` (işlenebilir).

İşleme: foundation'da `scripts/sync-review.sh` — `--list` (göster), `--issue` (GitHub issue aç),
`--clear` (issue'suz arşivle); ardından `scripts/sync-sources.sh` arşivi tazeler. Foundation konumu
`CLAUDE_FOUNDATION_DIR` ile ayarlanır (varsayılan `$HOME/Backup/GitHub/Node/claude-foundation`).
Bkz. `claude-foundation/docs/GOVERNANCE.md`.

## Notlar

- Hook'lar `bash .claude/hooks/...` ile çağrılır → `chmod +x` şart değil ama önerilir.
- JSON parse için `python3` kullanılır (macOS/Linux'ta hazır).
- `set -euo pipefail` + sessiz `|| true` ile asla oturumu kilitlemez.
