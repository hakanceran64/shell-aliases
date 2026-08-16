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

### UI craft → artık `profiles/web-ui/` altında

10 UI craft skill'i (`ui-craft`·`animate`·`review-animations`·`improve-animations`·
`find-animation-opportunities`·`animation-vocabulary`·`apple-design`·`pick-ui-library`·
`ui-prototype`·`sonner`) çekirdek kitten **paylaşılan `web-ui` overlay'ine** taşındı
(`claude-foundation/profiles/web-ui/`, DECISIONS#0022). Bunlar yalnız web stack'i beyan eden
projelere iner — `astro-web`, `react`, `node-web` profilleri `.includes` ile `web-ui`'yi çeker.

Sebebi: web arayüzü olmayan projelerin (C++/ROS2, Python, docs-only) `.claude/skills/` dizini
kullanılmayan 10 skill taşıyordu; `description` daraltması onları tetiklenmez kılıyordu ama
listeden ve bakım yükünden çıkarmıyordu. Katalog: [`profiles/web-ui/README.md`](../../../profiles/web-ui/README.md).

> Yan etkili akışlar (`commit-push-pr`, `audit`, `review-animations`, `improve-animations`,
> `ui-prototype`, `pick-ui-library`) `disable-model-invocation: true` ile yalnız kullanıcı
> tarafından tetiklenir — Claude bunları kendi başına çalıştırmaz.
> Proje-özel skill'ler (ör. `flutter-feature`) profil paketleriyle eklenir.

Web projesi olmayan bir repoda bu skill'ler artık **hiç kurulmaz**; gerekiyorsa projenin
`.ceran/ecosystem.yaml` dosyasına ilgili web profili eklenir.
