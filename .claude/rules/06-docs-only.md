# Kural 06: Docs-Only Proje Disiplini

**Severity:** error · **Stages:** `docs/**/*.md`, `README.md`
**Kaynak:** Home-SYNC (genelleştirildi)

Bu profil, kaynak kod değil **dokümantasyon** üreten projeler içindir (planlama, mimari, wiki, bilgi tabanı).

## Stack kararları (toolchain)

> **Toolchain sürümlerinin kanonik kaynağı:** `devkit-wiki/registry/stack-registry.yaml`
> (profil `docs-only`; foundation'da vendored kopya: `wiki/registry/stack-registry.yaml`).
> Aşağıdaki tablo oradan türetilmiştir — sürüm değişecekse **önce registry'de** değiştir,
> sonra burayı güncelle. Upstream'de `lint-wiki.sh` referansların varlığını, foundation'da
> `tests/registry-sync.py` tablodaki araçların registry ile eşleştiğini doğrular.


Üretim kodu olmadığından build/lint/test **toolchain yok**. Önerilen kontroller: markdown lint, mermaid
render kontrolü, ölü link taraması. Diğer yeni-proje kararları (license/ADR/git) için
`claude-foundation/docs/NEW-PROJECT-DECISIONS.md`.

## Sınırlar (asla çiğnenmez)

- **Üretim kodu yazma** — bu repo doküman üretir; kod örnekleri yalnız açıklama amaçlıdır.
- **Tek kaynak ilkesi:** aynı bilgiyi birden fazla dosyaya koyma; ilgili dosyaya link ver.
- **Numara/yol sabit:** mevcut `docs/NN-...` numaralarını yeniden düzenleme — linkler kırılır.
- **Task durumu** ayrı backlog/agile alanına ait; `docs/*.md` içine yazma.

## Doküman yapısı

Her `docs/*.md`:
1. `# NN — Başlık` + bir cümle açıklama (dosya başı).
2. **En az 1 mermaid diyagramı** (ASCII yasak — bkz. aşağı).
3. Sonda **"Sıradaki"** bölümü: ilgili dosyalara link + 1 cümle gerekçe.
4. 1000+ satır → böl.

## Mermaid zorunlu

Tüm diyagramlar **mermaid** ile yazılır; ASCII/`art` diyagram yasak. Render edilebilirlik kontrol edilir.

## ADR süreci

Mimari kararlar `adr` skill'i ile kaydedilir; numara atlanmaz, eski ADR silinmez (Superseded).

## İlgili

- Tam set: `sources/Home-SYNC/.claude/` (skills: `adr`, `check-mermaid`, `doc-audit`; hook: `validate-no-code.sh`).
- Çekirdek: [adr skill](../skills/adr/SKILL.md)
