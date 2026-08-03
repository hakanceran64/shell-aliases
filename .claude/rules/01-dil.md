# Kural 01: Çıktı Dili

**Severity:** error · **Stages:** her-zaman

## Kural

Kullanıcıya dönen **tüm çıktı Türkçe** olur. Teknik terimler, kod ve identifier'lar İngilizce kalır.
Commit mesajı bu kuralın tek istisnasıdır → **İngilizce** ([03-commit.md](03-commit.md)).

## Kapsam

| Çıktı türü | Dil |
|-----------|-----|
| Sohbet yanıtı, açıklama, log | Türkçe |
| README, doc, ADR, kod yorumu | Türkçe |
| Commit mesajı (subject + body) | **İngilizce** |
| Kod, identifier, fonksiyon/dosya adı | İngilizce |
| Config key, frontmatter `name` | İngilizce |
| Skill/agent `description` | Türkçe |

## Teknik terim (çevrilmez)

`agent`, `skill`, `hook`, `command`, `commit`, `branch`, `merge`, `build`, `lint`, `test`, `mock`,
`fixture`, `port`, `adapter`, `use case`, `entity`, `value object`, `frontmatter`, `idempotent`,
`SOLID`, `TDD`, `container`, `devcontainer`, `RLS`, `CAS`.

## Yanlış / Doğru

```text
✗ "compiler" → "derleyici"        ✓ "build" — olduğu gibi
✗ "hooks" → "kancalar"            ✓ "hook dizini"
✗ Saf İngilizce yanıt             ✓ Türkçe düzyazı + İngilizce teknik terim
```

İç akıl yürütme İngilizce olabilir; **kullanıcıya görünen** metin Türkçe yazılır.
