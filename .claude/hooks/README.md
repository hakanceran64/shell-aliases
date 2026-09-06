# Hooks — proje katmanı (K3)

Olay-bazlı, **proje bağlamı gerektiren** hook'lar. Bağlama `../settings.json` içindedir.

| Olay | Hook | Görev |
|------|------|-------|
| SessionStart | `session-start/pulse-resume.sh` | oturumu NodeFlow'da açar, "nerede kalmıştın" (ceran-pulse) |
| PostToolUse(Edit\|Write) | `post-tool-use/claude-config-watcher.sh` | **`.claude`/`CLAUDE.md` değişikliğini bildir + changelog + foundation sync sinyali** |
| PostToolUse(Edit\|Write) | `post-tool-use/format-lint.sh` | **düzenlenen dosyayı formatla + lint'le; bulgu varsa exit 2** |
| Stop | `stop/pulse-record.sh` | oturumu kapatır: süre + commit'ler (ceran-pulse) |

## Kitten çıkanlar — K0/K1'de tek nüsha (DECISIONS#0044)

`bash-guard` · `model-guard` · `show-context` · `inject-context` · `wrap-up` 2026-09-06'da kitten
kaldırıldı (`kit/tombstones.yaml`). Karşılıkları `claude-foundation/ceran-hooks` Go binary'sinde
(`~/.ceran/bin/ceran-hooks`), kullanıcı katmanında (`~/.claude/settings.json`, `dev eco home install`)
ve managed katmanda (`/Library/Application Support/ClaudeCode/managed-settings.json`) koşar:

| Eski kit hook'u | Yeni | Fark |
|-----------------|------|------|
| `pre-tool-use/bash-guard.sh` | `ceran-hooks bash-guard` | aynı 17 desen |
| `pre-tool-use/model-guard.sh` | `ceran-hooks model-guard` | **allowlist** (`policy/models.yaml`): yalnız `opus` · `sonnet` · `inherit` |
| `session-start/show-context.sh` · `user-prompt-submit/inject-context.sh` · `stop/wrap-up.sh` | `ceran-hooks session-context` | tek alt komut, olayı JSON'dan seçer |

Proje bu guard'ları **kaldıramaz**: kayıtları projenin `settings.json`'ında değil.
Üye repoda kopyaları kaldıysa `dev eco sync` dokunulmamış olanı siler; özelleştirilmişi
`lingering` olarak raporlar.

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

## format-lint (kalite kapısı)

`kod-kalitesi` (K1) ve profil `06-*` kurallarının **çalıştırılabilir** karşılığı. Sözleşme
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

## Model politikası (statik yüzey)

`scripts/check-models.sh` (CI adımı, `verify.sh` politika adımı) depoyu tarar; dosya nereden
gelirse gelsin (başka makine, merge, elle düzenleme) kapıyı kapatır. Oturum içi yüzey K0/K1'deki
`ceran-hooks model-guard`'dır; ikisi aynı kuralın iki yüzeyidir (`policy/models.yaml`).

## Notlar

- Hook'lar `bash .claude/hooks/...` ile çağrılır → `chmod +x` şart değil ama önerilir.
- JSON parse için `python3` kullanılır (macOS/Linux'ta hazır).
- `set -euo pipefail` + sessiz `|| true` ile asla oturumu kilitlemez.
