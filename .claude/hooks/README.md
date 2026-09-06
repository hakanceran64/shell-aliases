# Hooks — proje katmanı (K3)

Bu dizin yalnız **projeye özel** hook'lar içindir (ör. bir kasa projesinin `note-lint.sh`'ı,
bir oyun projesinin `level-validate.sh`'ı). Kayıtları projenin `../settings.json`'ındadır.

## Paylaşılan hook'lar burada DEĞİL — plugin'de (DECISIONS#0046)

2026-09-06'dan (kit v3.0.0) itibaren kit hiçbir hook dosyası kopyalamaz ve `settings.json`'a
hook kaydı yazmaz. Beş proje hook'u `ceran` marketplace plugin'lerinde tek nüshadır ve
`enabledPlugins` ile gelir (`${CLAUDE_PLUGIN_ROOT}` altından, proje cwd'sinde koşar):

| Plugin | Olay | Hook | Görev |
|--------|------|------|-------|
| `ceran-core` | PostToolUse(Edit\|Write) | `hooks/format-lint.sh` | **düzenlenen dosyayı `.claude/quality.json` → `on_edit[]` ile formatla + lint'le; bulgu → exit 2** |
| `ceran-core` | PostToolUse(Edit\|Write) | `hooks/claude-config-watcher.sh` | `.claude/**` / `CLAUDE.md` değişikliğini bildir + `.claude/CHANGELOG.md` (gözlem günlüğü) |
| `ceran-core` | PostToolUse · ConfigChange | `hooks/config-validate.sh` | manifest · quality · settings · frontmatter şemaları; `ConfigChange`'de bozuk dosyayı **bloklar** (DECISIONS#0047) |
| `ceran-pulse` | SessionStart | `hooks/pulse-resume.sh` | oturumu NodeFlow'da açar, "nerede kalmıştın" (fail-open) |
| `ceran-pulse` | Stop | `hooks/pulse-record.sh` | oturumu kapatır: süre + commit'ler (senkron, fail-open) |

Eski kopyalar (`post-tool-use/*.sh`, `session-start/pulse-resume.sh`, `stop/pulse-record.sh`,
`scripts/find-pulse.sh`) `kit/tombstones.yaml` ile `dev eco sync` tarafından kaldırılır; özelleştirilmiş
bir kopya `lingering` raporlanır. Eski `settings.json` kayıtlarını `dev eco sync` (settings birleşimi)
ya da `scripts/sync-hooks.py --prune` düşürür.

## Guard'lar ve oturum bağlamı — K0/K1'de tek nüsha (DECISIONS#0044)

`bash-guard` · `model-guard` · `session-context` · `audit-log` `claude-foundation/ceran-hooks` Go
binary'sindedir (`~/.ceran/bin/ceran-hooks`), kullanıcı katmanında (`~/.claude/settings.json`,
`dev eco home install`) ve managed katmanda koşar. Proje bunları **kaldıramaz**: kayıtları projenin
`settings.json`'ında değil.

## Proje hook'u yazarken

- `hooks/<event>/<ad>.sh`, `set -uo pipefail`, stdin'deki JSON'ı oku (okumazsan boru dolabilir).
- **Fail-open**: araç yoksa sessizce 0 dön; yalnız gerçek bulguda exit 2 (stderr Claude'a geri döner).
- Kaydı `settings.json` → `hooks.<Event>[]` altına yaz; `dev eco sync` projenin kendi kayıtlarına dokunmaz.
- Paylaşılabilir bir hook yazdıysan buraya değil `claude-foundation/plugins/`'e taşı (sürümlü, tek nüsha).

## claude-config-watcher (gözlem günlüğü)

Projedeki `.claude/**`, `CLAUDE.md`, `.ceran/**` veya tasarım token dosyası her değiştiğinde (plugin hook'u):
1. Operatöre `📢` ile bildirir (hangi merkez repoyu ilgilendirdiğini söyler),
2. `.claude/CHANGELOG.md`'ye satır ekler.

Foundation'a sinyal **bırakmaz** (ceran-core 2.0.0, DECISIONS#0048): drift'i gece `dev eco doctor` ölçer,
bozuk config'i `config-validate` hook'u `ConfigChange`'de durdurur. `ceran-design-system/dist/**`
düzenlemesini **engeller** (exit 2 — üretilen dizin).

**Proje kimliği** düzenlenen dosyanın **repo kökünden** okunur (`git rev-parse --show-toplevel`),
cwd'den değil; yol da repo köküne göre yazılır.

**Sessiz kalanlar:** `settings.local.json` · `CHANGELOG.md` (kendi çıktısı) · `.ceran/lock.yaml`
(üretilen) · Claude Code'un kendi oturum state'i (`.claude/projects|plans|todos|shell-snapshots|statsig`)
· `.claude/worktrees/**` (çalışma kopyası) · foundation `kit/` · `plugins/` · `profiles/` kaynağı.

## format-lint (kalite kapısı)

`kod-kalitesi` (K1) ve profil `06-*` kurallarının **çalıştırılabilir** karşılığı; plugin hook'u
projenin `.claude/quality.json` sözleşmesini okur:

```json
{
  "profile": "python",
  "verify":  { "format": "ruff format --check .", "lint": "ruff check .", "test": "pytest -q" },
  "on_edit": [ { "match": "*.py", "format": "ruff format {file}", "lint": "ruff check {file}" } ]
}
```

- `on_edit[]` → bu hook çalıştırır: **tek dosya** kapsamlı, hızlı olmalı. İlk eşleşen kural uygulanır
  (`match` glob'u tam göreli yola veya dosya adına bakar); `{file}` kaçırılmış yol ile değişir.
- `verify{}` → CI ve commit öncesi doğrulama kullanır (`.claude/scripts/verify.sh`, repo-geneli).
- **Fail-open:** `quality.json` yok · glob eşleşmedi · araç kurulu değil → sessizce geçer. Kapı yalnız
  araç gerçekten varken kapanır; toolchain'siz makinede oturum kilitlenmez.
- Lint sıfırdan farklı dönerse hook **exit 2** verir ve çıktı Claude'a feedback olur.

Profil öntanımlıları `profiles/<profil>/.claude/quality.json`'dadır; profilsiz projeler
`quality.json.example`'ı kopyalar.

## Model politikası (statik yüzey)

`scripts/check-models.sh` (CI adımı, `verify.sh` politika adımı) depoyu tarar; dosya nereden
gelirse gelsin kapıyı kapatır. Oturum içi yüzey K0/K1'deki `ceran-hooks model-guard`'dır; ikisi
aynı kuralın iki yüzeyidir (`policy/models.yaml`).
