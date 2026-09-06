# shell-aliases — Claude Code Context

> Bu dosya ekosistem rollout'unda **registry'den bilinen gerçeklerle** üretildi
> (2026-08-03). İçindeki her şey doğrulanmıştır; eksik olan yerler aşağıdaki
> "Genişlet" bölümünde açıkça listelenmiştir — uydurma bilgi yoktur.

## Özet

Günlük terminali kullanımını hızlandırmak için hazırlanmış zsh alias ve fonksiyon koleksiyonu. Dosya yönetiminden git'e, ağ araçlarından sistem izlemeye kadar sık kullanılan işlemleri tek komuta indirger.

- **Teknoloji:** Markdown / doküman — üretim kodu yok
- **Çalışma dizini:** `/Users/ceran/Backup/GitHub/hakanceran64/devenv/shell-aliases`
- **Ekosistem profili:** docs-only

- Son commit: 2026-05-04 · Commit sayısı: 2 · Remote: gitlab, origin

## Kurallar (bağlayıcı)

`.claude/rules/` altındaki dosyalar **otomatik yüklenir** ve bağlayıcıdır:

- `01-dil` — çıktı Türkçe, kod/commit İngilizce
- `02-guvenlik` — yıkıcı operasyonlar onay/yasak
- `03-commit` — Conventional Commits, AI atfı YOK
- `04-izinler` — izin matrisi
- `05-kod-kalitesi` — SOLID · Clean Code · anti-pattern yasakları
- `06-docs-only` — Markdown / doküman — üretim kodu yok

## Ekosistem

Bu repo CERAN Development Ecosystem üyesidir. Ne tükettiği
`.ceran/ecosystem.yaml`'da beyan edilir, ne kurulu olduğu
`.ceran/lock.yaml`'da yazar (üretilen — elle düzenlenmez).

```bash
dev eco status          # ne kurulu, drift var mı
dev eco sync --check    # ekosistemle uyumlu mu (CI)
dev eco sync            # merkez güncellemelerini al
```

## `.claude` altyapısı

| Bileşen | Yer |
|---------|-----|
| Kurallar | `.claude/rules/` |
| Plugin'ler (K2) | `.claude/settings.json` → `enabledPlugins` — `ceran-core` (`/ceran-core:adr` · `audit` · `changelog-draft` · `ship`; code-reviewer · commit-scribe · doc-writer; format-lint · watcher hook'ları) · `ceran-pulse` (oturum kaydı, `/ceran-pulse:insights`) |
| Skills | `.claude/skills/` — yalnız proje skill'leri (çıplak ad) + `mermaid-check` (kapı aracı) |
| Agents | `.claude/agents/` — yalnız proje agent'ları |
| Hooks | `.claude/hooks/` — yalnız proje hook'ları; paylaşılanlar plugin'de, guard'lar K0/K1 `ceran-hooks`'ta |
| Memory | `.claude/memory/` (+ `MEMORY.md` index) |

## Genişlet (bu dosyanın bilmediği şeyler)

Aşağıdakiler otomatik üretilemez — projeyi bilen kişi doldurur:

- Projenin amacı ve hedef kitlesi (bir-iki cümle)
- Mimari katmanlar ve aralarındaki bağımlılık yönü
- Kurulum / build / test komutları
- Kritik mimari kararlar ve gerekçeleri (varsa `docs/adr/`'ye ADR olarak)
- Bilinen tuzaklar / gotcha'lar

---
**Governance:** Bu projenin `.claude/**` veya `CLAUDE.md` dosyaları değişirse
`claude-config-watcher` hook'u durumu operatöre ve `claude-foundation`'a bildirir.
