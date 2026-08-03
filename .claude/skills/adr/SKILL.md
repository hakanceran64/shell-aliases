---
name: adr
description: Yeni bir ADR (Architectural Decision Record) ekle — mimari bir karar alındığında veya tartışıldığında kullan
when_to_use: "Tetikleyiciler: 'yeni ADR', 'mimari karar kaydet', 'bunu ADR yap', /adr"
argument-hint: "[karar başlığı]"
allowed-tools: Read, Edit, Write, Bash(ls:*), Bash(git log:*)
---

# Yeni ADR

Kullanıcının tarif ettiği mimari kararı `adr-template.md` formatında ADR dizinine ekle.

## Adımlar

1. ADR dizinini bul (`docs/adr/`, `.claude/adr/` veya `docs/10-decisions.md`) — son numarayı tespit et (yeni = N+1).
2. Gerekirse kullanıcıya sor:
   - **Bağlam:** Hangi problemi çözüyor? Neden şimdi?
   - **Seçenekler:** Hangi alternatifler değerlendirildi?
   - **Karar:** Hangisi seçildi?
   - **Gerekçe:** 3-5 madde
   - **Sonuçlar:** pozitif sonuçlar + kabul edilen trade-off'lar
3. ADR'ı `NNNN-kebab-baslik.md` olarak `adr-template.md` formatında yaz.
4. Kritik bir karar ise `CLAUDE.md`'deki "Kritik mimari kararlar" tablosuna ekle.
5. Gerekirse mermaid diyagramı ekle (karar ağacı / mimari).

## Kısıtlar

- ADR numaraları atlanmaz, geri kullanılmaz.
- Mevcut ADR'lar silinmez — eskiyince "Superseded by ADR-N" notu eklenir.
- `$ARGUMENTS` boşsa konuyu kullanıcıdan iste.

## İlgili

- `adr-template.md` (yanında) · [03-commit.md](../../rules/03-commit.md)
