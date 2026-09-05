# Hooks — kanonik set

Olay-bazlı, **proje-bağımsız** hook'lar. Hepsi bağımsız `.sh` dosyası (test edilebilir, yeniden
kullanılabilir). Bağlama `../settings.json` içindedir.

| Olay | Hook | Görev |
|------|------|-------|
| SessionStart | `session-start/show-context.sh` | proje · branch · kirli dosya · mevcut .claude bölümleri |
| UserPromptSubmit | `user-prompt-submit/inject-context.sh` | her prompt'a güncel proje bağlamı (JSON) |
| PreToolUse(Bash) | `pre-tool-use/bash-guard.sh` | yıkıcı komutları engelle (exit 2) |
| PreToolUse(Task\|Agent\|Edit\|Write) | `pre-tool-use/model-guard.sh` | **yasak modeli (haiku · eski nesil tam kimlik) engelle** — çağrı parametresinde ve agent/skill/settings yazımında (exit 2) |
| PostToolUse(Edit\|Write) | `post-tool-use/claude-config-watcher.sh` | **`.claude`/`CLAUDE.md` değişikliğini bildir + changelog + foundation sync sinyali** |
| PostToolUse(Edit\|Write) | `post-tool-use/format-lint.sh` | **düzenlenen dosyayı formatla + lint'le; bulgu varsa exit 2** |
| Stop | `stop/wrap-up.sh` | commit edilmemiş dosya özeti (async) |

## claude-config-watcher (governance)

Projedeki `.claude/**` veya `CLAUDE.md` her değiştiğinde:
1. Operatöre `📢` ile bildirir,
2. `.claude/CHANGELOG.md`'ye satır ekler,
3. foundation'a iki sinyal bırakır: insan-okunur `docs/SYNC-QUEUE.md` + makine-okunur
   `docs/sync-queue.jsonl` (işlenebilir).

**Proje kimliği** düzenlenen dosyanın **repo kökünden** okunur (`git rev-parse --show-toplevel`),
cwd'den değil; yol da repo köküne göre yazılır. Böylece alt ağaçtaki bir `CLAUDE.md` doğru repoya
ait görünür ve aynı repodaki iki farklı `CLAUDE.md` kuyrukta ayırt edilir.

**Sinyal üretmeyenler:** `settings.local.json` · `CHANGELOG.md` (kendi çıktısı) · `.ceran/lock.yaml`
(üretilen) · Claude Code'un kendi oturum state'i (`.claude/projects|plans|todos|shell-snapshots|statsig`)
· `.claude/worktrees/**` (çalışma kopyası). Kuyrukta kalmış eski gürültü: `sync-review.sh --prune`.

İşleme: foundation'da `scripts/sync-review.sh` — `--list` (göster), `--issue` (GitHub issue aç),
`--clear` (issue'suz arşivle), `--prune` (bayat gürültüyü arşivle); ardından `scripts/sync-sources.sh`
arşivi tazeler. Foundation konumu `CLAUDE_FOUNDATION_DIR` ile ayarlanır (varsayılan
`${CERAN_ECOSYSTEM_ROOT:-$HOME/Backup/GitHub}/claude-foundation` — ekosistem kökündeki kanonik
checkout; submodule kopyası hedef gösterilirse hook uyarır ve sinyali atlar).
Bkz. `claude-foundation/docs/GOVERNANCE.md`.

## model-guard (model politikası)

`agents/README.md` → **Model politikası**'nın çalıştırılabilir karşılığı (DECISIONS#0040): yalnız
`opus` ve `sonnet`; `haiku` yasak. İki yüzeyi birden kapatır:

1. **Çalışma anı** — bir subagent `model: haiku` ile çağrılırsa çağrı engellenir.
2. **Yapılandırma** — `.claude/agents/*.md`, `skills/**/SKILL.md` ve `settings*.json` dosyalarına
   haiku **yazılması** engellenir; dosya diske hiç düşmez.

Yalnız `haiku` engellenir; tanınmayan değer işi durdurmaz (`inherit`, `claude-opus-5`, `sonnet[1m]`
serbest). `.md` dosyalarında yalnız `model:` **beyanı** sayılır — gövdede geçen "haiku" kelimesi
bulgu değildir. Bozuk JSON'da fail-open.

Depo-geneli karşılığı `scripts/check-models.sh` (CI adımı): hook yalnız bu oturumdaki yazmayı
engeller, script dosya nereden gelirse gelsin kapıyı kapatır.

## format-lint (kalite kapısı)

`05-kod-kalitesi` ve profil `06-*` kurallarının **çalıştırılabilir** karşılığı. Sözleşme
`.claude/quality.json`:

```json
{
  "profile": "python",
  "verify":  { "format": "ruff format --check .", "lint": "ruff check .", "test": "pytest -q" },
  "on_edit": [ { "match": "*.py", "format": "ruff format {file}", "lint": "ruff check {file}" } ]
}
```

- `on_edit[]` → bu hook çalıştırır: **tek dosya** kapsamlı, hızlı olmalı. İlk eşleşen kural uygulanır
  (`match` glob'u tam göreli yola veya dosya adına bakar); `{file}` kaçırılmış yol ile değişir.
- `verify{}` → CI ve commit öncesi doğrulama kullanır (repo-geneli).
- **Fail-open:** `quality.json` yok · glob eşleşmedi · araç kurulu değil → sessizce geçer. Kapı yalnız
  araç gerçekten varken kapanır; toolchain'siz makinede oturum kilitlenmez.
- Lint sıfırdan farklı dönerse hook **exit 2** verir ve çıktı Claude'a feedback olur.

Profil öntanımlıları `profiles/<profil>/.claude/quality.json`'dadır; profilsiz projeler
`quality.json.example`'ı kopyalar.

## Notlar

- Hook'lar `bash .claude/hooks/...` ile çağrılır → `chmod +x` şart değil ama önerilir.
- JSON parse için `python3` kullanılır (macOS/Linux'ta hazır).
- `set -euo pipefail` + sessiz `|| true` ile asla oturumu kilitlemez.
