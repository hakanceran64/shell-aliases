# 1. Mimari kararları kaydet

- **Durum:** accepted
- **Tarih:** 2026-09-06

## Bağlam

Bu proje CERAN Development Ecosystem üyesidir (ekosisteme sonradan katıldı; ADR tohumu Faz 4 dalga 2 rollout'uyla eklendi).
Mimari kararların *neden* alındığı, kodun kendisinden okunamaz;
zamanla "bu neden böyle?" sorusu cevapsız kalır.

## Karar

Önemli mimari kararlar bu dizinde ADR olarak kaydedilir
(`docs/adr/NNNN-slug.md`). Yeni ADR için: `/ceran-core:adr`.

Bu projenin devraldığı ekosistem kararları burada tekrarlanmaz — kaynakları:

| Konu | Nerede |
|---|---|
| Ekosistem mimarisi | `claude-foundation/docs/DECISIONS.md` |
| Stack seçimi (`docs-only`) | `devkit-wiki/registry/stack-registry.yaml` |
| Tasarım token'ları | `ceran-design-system/` |
| Ortak modüller | `shared-modules/` |

## Sonuçlar

Kararın gerekçesi kaybolmaz; yeni katılan (insan ya da agent) `docs/adr/`'yi
okuyarak bağlamı edinir.
