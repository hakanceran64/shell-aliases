# Skills — kanonik format

Claude Code'da **custom command'lar skill'lere birleştirildi** (Claude Docs). `.claude/commands/*.md`
hâlâ çalışır ama **legacy**; bu kit **skills-first**'tür. Bir skill, kendi klasöründe bir **`SKILL.md`**
dosyasıdır; komut adı **klasör adından** gelir (`skills/hasat/SKILL.md` → `/hasat`). Yardımcı dosyalar
(`*-template.md`, `checklist.md`, `scripts/`) aynı klasörde durur ve `SKILL.md`'den linklenir.

## Bu dizinde ne durur — yalnız PROJE skill'leri (DECISIONS#0046)

Paylaşılan skill'ler 2026-09-06'dan (kit v3.0.0) itibaren buraya **kopyalanmaz**; `ceran`
marketplace'inin plugin'lerinden gelir ve `.claude/settings.json` → `enabledPlugins` ile açılır
(`dev eco sync` yazar). Plugin skill'leri **namespace'lidir**, proje skill'leri çıplaktır — çakışma
yapısal olarak imkânsız.

| Plugin | Komutlar | Nasıl gelir |
|--------|----------|-------------|
| `ceran-core` | `/ceran-core:assess` · `feature-spec` · `tasks` · `bugfix` (fikir → spec → görev → bug akışı) · `adr` · `audit` · `changelog-draft` · `ship` (commit + her remote'a push) | her üyede (kit öntanımlısı) |
| `ceran-pulse` | `/ceran-pulse:insights` (+ oturum kaydı hook'ları) | her üyede; manifestte `plugins.disable` ile kapatılır |
| `ceran-web-ui` | `/ceran-web-ui:animate` · `ui-craft` · `review-animations` · `improve-animations` · `find-animation-opportunities` · `animation-vocabulary` · `apple-design` · `pick-ui-library` · `ui-prototype` · `sonner` | web profilleri (`react` · `astro-web` · `node-web`) `.includes` → `web-ui` |
| `ceran-ai-team` | `/ceran-ai-team:spec` · `/ceran-ai-team:build-feature` | manifestte `profiles: [<stack>, ai-team]` açık beyanı |
| `ceran-learning-vault` | `/ceran-learning-vault:validate-note` · `sync-index` · `project-status` · `generate-kata` · `anki-generate` · `add-antipattern` | `learning-vault` profili |

Kaynak: `claude-foundation/plugins/<ad>/skills/`. Katalog ve sürüm: `claude-foundation/.claude-plugin/marketplace.json`.
Eski kopyalar `kit/tombstones.yaml` (ve profil `tombstones.yaml`'ları) ile `dev eco sync` tarafından kaldırılır.

### Kitte kalan tek skill: `mermaid-check`

| Skill | Komut | İnvocation | Görev |
|-------|-------|------------|-------|
| [`mermaid-check`](mermaid-check/SKILL.md) | `/mermaid-check` | her ikisi | mermaid diyagram doğrulama — **`validate.py` bir kalite kapısı aracıdır**: `quality.json` ve CI proje ağacından çağırır, bu yüzden plugin'e taşınmadı |
| [`_TEMPLATE.md`](_TEMPLATE.md) | — | — | yeni proje skill'i iskeleti (skill değil, kopyalanır) |

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

## Proje skill'i yazarken

- Ad çıplak ve projeye özgü olsun (`/hasat`, `/sinav-uret`); plugin adlarıyla (`adr`, `audit`, `spec`…)
  çakışmaz ama aynı adı vermek okuyanı yanıltır.
- Bir plugin skill'ini genişletmek istiyorsan **kopyalama** — proje skill'i plugin skill'ini
  `/ceran-core:adr` diye çağırmaz (skill skill çağıramaz); sözleşme dosya biçimidir. Ortak parça
  gerekiyorsa `claude-foundation/plugins/`'e taşı, sürüm yükselt.
- `SKILL.md` adı büyük harfle yazılır; küçük harfli ad harf-duyarlı FS'te kaydolmaz
  (`new-project.sh --check` bunu bulgu sayar).
