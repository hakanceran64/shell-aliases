# Agents — kanonik format

Her agent **düz `agents/<name>.md`** dosyasıdır (native Claude Code formatı; klasör/`AGENT.md`
desteklenmez).

## Bu dizinde ne durur — yalnız PROJE agent'ları (DECISIONS#0046)

Paylaşılan agent'lar 2026-09-06'dan (kit v3.0.0) itibaren buraya **kopyalanmaz**; `ceran`
marketplace'inin plugin'lerinden gelir (`.claude/settings.json` → `enabledPlugins`, `dev eco sync` yazar):

| Plugin | Agent | Model | Görev |
|--------|-------|-------|-------|
| `ceran-core` | `code-reviewer` | sonnet | diff'i kalite/güvenlik/kural açısından inceler |
| `ceran-core` | `commit-scribe` | sonnet | Conventional Commit mesajı yazar |
| `ceran-core` | `doc-writer` | sonnet | README/doc/yorum yazar — Türkçe, mermaid'li |
| `ceran-ai-team` | `software-architect` · `design-specialist` | opus | mimari spec + iskelet dalgası · tasarım spec'i |
| `ceran-ai-team` | `senior-developer` · `test-engineer` | sonnet | iş paketi gövdesi · vaka matrisi + kapı |
| `ceran-learning-vault` | `note-validator` · `cross-reference-builder` | sonnet | kasa sayfası doğrulama · wikilink bütünlüğü |

Kaynak: `claude-foundation/plugins/<ad>/agents/`. `ai-team` yalnız manifestte açık beyanla gelir
(`profiles: [<stack>, ai-team]` — DECISIONS#0040); `learning-vault` profiliyle gelir.

## Frontmatter standardı

```markdown
---
name: kebab-case-slug          # EN, dosya adıyla aynı
description: Türkçe — ne yapar + ne zaman çağrılır (tetikleyiciler net)
tools: Read, Write, Edit, Glob, Grep, Bash(git diff:*)   # opsiyonel kısıtlama
model: sonnet                  # orkestrasyon: opus | kod/doc: sonnet
# permissionMode: acceptEdits  # opsiyonel
# maxTurns: 30                 # opsiyonel
---
```

Proje agent'ı adı `<alan>-<rol>` biçiminde olsun (`content-strategist`, `printer-profile-doctor`);
plugin agent'larıyla aynı adı verme — aynı ad iki yerde tanımlıysa hangisinin çalıştığı okunmaz.

## Model politikası

**Yalnız `opus` ve `sonnet` kullanılır. `haiku` her sürümüyle yasaktır** (DECISIONS#0040).

| Model | Nerede |
|-------|--------|
| `opus` | mimari planlama, tasarım muhakemesi, çok-adımlı orkestrasyon |
| `sonnet` | kod yazımı, test, review, doc (**varsayılan**) |
| ~~`haiku`~~ | **hiçbir yerde** — "basit iş" istisnası yok |

Model **alias** ile yazılır (`opus` · `sonnet` · `inherit`); tam kimlik sabitlenmez. Zorlama K0/K1
`ceran-hooks model-guard` **allowlist**'idir (`policy/models.yaml`, DECISIONS#0044): tanınmayan değer
geçmez, eski nesil kimlikler (`claude-3*`, `claude-opus-4*`, `claude-sonnet-4*`) reddedilir;
`check-models.sh` aynı politikayı CI'da statik tarar.

**Neden:** maliyet **modeli küçülterek** değil **bağlamı küçülterek** düşürülür. Bağlamı dar tutan
tasarım (bkz. `ceran-ai-team` plugin'i) hem daha ucuzdur hem de muhakemeyi feda etmez. "Mekanik" görünen
bir adım da kural ihlal edebilir — silinen bir test, susturulan bir lint, sızdırılan bir sır — ve
ucuz model bunu sessizce kaçırır. Sessiz ihlal, tasarruf ettiği token'dan pahalıdır.
