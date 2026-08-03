# Skill şablonu (kopyala-başla)

Yeni skill: `mkdir skills/<ad> && cp _TEMPLATE.md skills/<ad>/SKILL.md`, sonra düzenle.
Bu dosya tek başına bir skill **değildir** (klasör/`SKILL.md` olmadığı için kaydolmaz).

```markdown
---
name: skill-adi                  # opsiyonel; varsayılan = klasör adı (komut adı klasörden gelir)
description: Ne yapar + ne zaman tetiklenir (Türkçe, tek cümle; anahtar kullanım başa)
when_to_use: "Tetikleyiciler: '...', '/skill-adi'"   # opsiyonel
argument-hint: "[arg]"           # opsiyonel
allowed-tools: Read, Edit, Write # opsiyonel; aktifken izinsiz kullanılacak araçlar
# disable-model-invocation: true # yalnız kullanıcı tetiklesin (yan etkili işler: /deploy, /commit)
# user-invocable: false          # yalnız Claude görsün (arka plan bilgisi)
# paths: "lib/**/*.dart"         # sadece eşleşen dosyalarda otomatik yükle
# context: fork                  # izole subagent'ta çalıştır
# agent: Explore                 # fork için subagent tipi
---

# {{Başlık}}

`$ARGUMENTS` için {{ana amaç}}.

## Adımlar
1. {{...}}

## Çıktı
{{format}}

## Kısıtlar
- {{ne yapılMAZ}}; `$ARGUMENTS` boşsa kullanıcıdan iste.
```

## Notlar (Claude Docs)

- Komut adı **klasör adından** gelir: `skills/deploy/SKILL.md` → `/deploy`.
- Dinamik bağlam: satır başında `` !`komut` `` çalıştırılıp çıktısı gömülür.
- Argüman: `$ARGUMENTS`, `$ARGUMENTS[N]`/`$N`, `arguments:` ile isimli `$ad`.
- Destekleyici dosyalar (`template.md`, `checklist.md`, `scripts/`) `SKILL.md`'den linklenir; `${CLAUDE_SKILL_DIR}` ile yol verilir.
- `SKILL.md`'yi < 500 satır tut; detayı ayrı dosyaya al.
