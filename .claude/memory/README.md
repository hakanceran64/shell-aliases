# memory/

Oturumlar arası taşınan kalıcı, **proje-özel** bağlam. Claude Code'un global memory sisteminin bu repo
bağlamındaki tamamlayıcısıdır.

## Türler

- **user** — kullanıcının rolü, tercihleri, bilgisi
- **feedback** — "şunu yap / şunu yapma" rehberliği (sebebiyle)
- **project** — süregelen iş, hedef, tarih, neden
- **reference** — dış sistemlere (URL, dashboard, ticket) işaret

## İndeks

[`MEMORY.md`](MEMORY.md) — her memory için tek satırlık pointer. Her oturumda yüklenir.

## Format

Her memory tek bir markdown dosyasıdır:

```markdown
---
name: kebab-case-slug
description: tek satır özet — recall'da alaka kararı için kullanılır
metadata:
  type: user | feedback | project | reference
---

İçerik. feedback/project için **Neden:** ve **Nasıl uygula:** satırları ekle.
Diğer memory'lere [[name]] ile link ver.
```

### Opsiyonel: kanıt + güven (instinct deseni)

feedback memory'lerde, kuralın neye dayandığını ve ne kadar kesin olduğunu belirtmek için
(everything-claude-code "instincts" kavramından uyarlandı):

```markdown
**Evidence:** mainline commit geçmişi tutarlı şekilde Conventional Commits kullanıyor.
**Confidence:** 0.9
```

Yüksek güvenli + kanıtlı feedback'lere daha çok güvenilir; düşük güvenli olanlar gözden geçirilir.

## Kurallar

- Yeni memory kaydetmeden önce aynı konuyu kapsayan dosya var mı bak — varsa onu güncelle.
- Repo'nun zaten kaydettiğini (kod yapısı, git geçmişi, CLAUDE.md) memory'ye yazma.
- Yanlış çıkan memory'yi sil. Göreli tarihleri mutlak tarihe çevir.
