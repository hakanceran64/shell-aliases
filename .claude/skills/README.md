# Skills — kanonik format

Claude Code'da **custom command'lar skill'lere birleştirildi** (Claude Docs). `.claude/commands/*.md`
hâlâ çalışır ama **legacy**; bu kit **skills-first**'tür. Bir skill, kendi klasöründe bir **`SKILL.md`**
dosyasıdır; komut adı **klasör adından** gelir (`skills/audit/SKILL.md` → `/audit`). Yardımcı dosyalar
(`*-template.md`, `checklist.md`, `scripts/`) aynı klasörde durur ve `SKILL.md`'den linklenir.

## Frontmatter standardı (Claude Docs alanları)

```markdown
---
name: kebab-case-slug            # opsiyonel; varsayılan klasör adı
description: Türkçe tek cümle — ne yapar + ne zaman (anahtar kullanım başa)
when_to_use: "tetikleyici ifadeler"      # opsiyonel
argument-hint: "[arg]"                    # opsiyonel
allowed-tools: Read, Edit, Bash(git log:*)   # opsiyonel
disable-model-invocation: true            # yan etkili → yalnız kullanıcı tetikler
user-invocable: false                     # arka plan bilgisi → yalnız Claude
paths: "lib/**/*.dart"                     # sadece eşleşen dosyalarda otomatik yükle
context: fork                             # izole subagent
---
```

Yalnız `description` önerilir. Detay: `_TEMPLATE.md` ve [Claude Docs — skills](https://code.claude.com/docs/en/slash-commands).

## Mevcut skills

### Çekirdek (proje süreçleri)

| Skill | Komut | İnvocation | Görev |
|-------|-------|------------|-------|
| [`audit`](audit/SKILL.md) | `/audit` | yalnız kullanıcı | proje denetimi → rapor + backlog task'leri |
| [`adr`](adr/SKILL.md) | `/adr` | her ikisi | yeni ADR (mimari karar kaydı) |
| [`changelog-draft`](changelog-draft/SKILL.md) | `/changelog-draft` | her ikisi | git log'dan Keep-a-Changelog taslağı |
| [`commit-push-pr`](commit-push-pr/SKILL.md) | `/commit-push-pr` | yalnız kullanıcı | commit + push + PR |
| [`mermaid-check`](mermaid-check/SKILL.md) | `/mermaid-check` | her ikisi | mermaid diyagram doğrulama |
| [`_TEMPLATE.md`](_TEMPLATE.md) | — | — | yeni skill iskeleti (skill değil, kopyalanır) |

### UI craft (web arayüzü · design engineering)

Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT), ekosisteme uyarlandı.
Provenance, eşleme tablosu ve re-sync: `claude-foundation/docs/UPSTREAM-SKILLS.md`.

| Skill | Komut | İnvocation | Görev |
|-------|-------|------------|-------|
| [`ui-craft`](ui-craft/SKILL.md) | `/ui-craft` | her ikisi | ana referans: karar çerçevesi + cila kalıpları (+`PATTERNS.md`) |
| [`animate`](animate/SKILL.md) | `/animate` | her ikisi | animasyonu sıfırdan kurar ve yazar (+`RECIPES.md`) |
| [`review-animations`](review-animations/SKILL.md) | `/review-animations` | yalnız kullanıcı | diff/bileşen motion review'ü (+`STANDARDS.md`) |
| [`improve-animations`](improve-animations/SKILL.md) | `/improve-animations` | yalnız kullanıcı | kod tabanı denetimi → `docs/plans/` (+`AUDIT.md`, `PLAN-TEMPLATE.md`) |
| [`find-animation-opportunities`](find-animation-opportunities/SKILL.md) | `/find-animation-opportunities` | her ikisi | animate etmeyen ama etmesi gereken yerler (+reddedilenler) |
| [`animation-vocabulary`](animation-vocabulary/SKILL.md) | `/animation-vocabulary` | her ikisi | efekt tarifi → doğru terim (ters sözlük) |
| [`apple-design`](apple-design/SKILL.md) | `/apple-design` | her ikisi | akışkan arayüz: spring, jest, materyal, tipografi |
| [`pick-ui-library`](pick-ui-library/SKILL.md) | `/pick-ui-library` | yalnız kullanıcı | kütüphane seçimi (önce ekosistem kataloğu) |
| [`ui-prototype`](ui-prototype/SKILL.md) | `/ui-prototype` | yalnız kullanıcı | N varyant + görsel seçici (+`PICKER.md`) |
| [`sonner`](sonner/SKILL.md) | `/sonner` | her ikisi | Sonner toast rehberi ve sorun giderme (+`API.md`) |

> Yan etkili akışlar (`commit-push-pr`, `audit`, `review-animations`, `improve-animations`,
> `ui-prototype`, `pick-ui-library`) `disable-model-invocation: true` ile yalnız kullanıcı
> tarafından tetiklenir — Claude bunları kendi başına çalıştırmaz.
> Proje-özel skill'ler (ör. `flutter-feature`) profil paketleriyle eklenir.

**UI craft skill'leri profil-bağımsız çekirdekte durur** (kararlar: `docs/DECISIONS.md` #0021):
`description` alanları web arayüzüne dar biçimde kapsanmıştır, bu yüzden C++/ROS2, Python ya da
docs-only bir projede kendiliğinden tetiklenmezler; ama `/komut` ile her projeden erişilebilirler.
Değerlerin (easing eğrileri, süre bütçeleri) kanonik kopyası `ui-craft/PATTERNS.md` +
`animate/SKILL.md`'dedir; `review-animations/STANDARDS.md` ve `improve-animations/AUDIT.md` aynı
tabloları review/denetim çerçevesiyle yineler — birini değiştirirken diğerlerini de güncelle.
