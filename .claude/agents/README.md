# Agents — kanonik format

Her agent **düz `agents/<name>.md`** dosyasıdır (native Claude Code formatı; klasör/`AGENT.md`
desteklenmez).

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

## Mevcut agents

| Agent | Model | Görev |
|-------|-------|-------|
| [`commit-scribe`](commit-scribe.md) | sonnet | Conventional Commit mesajı yazar |
| [`code-reviewer`](code-reviewer.md) | sonnet | diff'i kalite/güvenlik/kural açısından inceler |
| [`doc-writer`](doc-writer.md) | sonnet | README/doc/yorum yazar — Türkçe, mermaid'li |

> **Paralel geliştirme ekibi** (`software-architect` · `senior-developer` · `design-specialist` ·
> `test-engineer`) çekirdek kitte **değil**, paylaşılan `ai-team` overlay'indedir
> (`claude-foundation/profiles/ai-team/README.md`). Ekibi kullanacak proje `.ceran/ecosystem.yaml`
> içinde `ai-team`'i açıkça beyan eder — DECISIONS#0040.

## Model politikası

**Yalnız `opus` ve `sonnet` kullanılır. `haiku` her sürümüyle yasaktır** (DECISIONS#0040).

| Model | Nerede |
|-------|--------|
| `opus` | mimari planlama, tasarım muhakemesi, çok-adımlı orkestrasyon |
| `sonnet` | kod yazımı, test, review, doc (**varsayılan**) |
| ~~`haiku`~~ | **hiçbir yerde** — "basit iş" istisnası yok |

Model **alias** ile yazılır (`opus` · `sonnet` · `inherit`); tam kimlik sabitlenmez. Eski nesil kimlikler
(`claude-3*`, `claude-opus-4*`, `claude-sonnet-4*`) `model-guard` ve `check-models` tarafından reddedilir
(DECISIONS#0043) — sabitlenen kimlik model değişince sessizce eskir, alias merkezden ilerler.

**Neden:** maliyet **modeli küçülterek** değil **bağlamı küçülterek** düşürülür. Bağlamı dar tutan
tasarım (bkz. `profiles/ai-team/`) hem daha ucuzdur hem de muhakemeyi feda etmez. "Mekanik" görünen
bir adım da kural ihlal edebilir — silinen bir test, susturulan bir lint, sızdırılan bir sır — ve
ucuz model bunu sessizce kaçırır. Sessiz ihlal, tasarruf ettiği token'dan pahalıdır.

**Kapsam:** agent frontmatter'ı · skill frontmatter'ı · `settings*.json` · `Agent`/`Task` çağrısındaki
`model` parametresi · CLI `--model`.

**Zorlama** (beyan değil, çalıştırılabilir):

| Katman | Ne yapar |
|--------|----------|
| `ceran-hooks model-guard` (K0 managed / K1 `~/.claude`, `claude-foundation/ceran-hooks`) | Oturum içinde `Agent`/`Task` çağrısını ve korunan dosyalara yazmayı **engeller** (exit 2) — **allowlist**: `policy/models.yaml`; projeden kaldırılamaz |
| [`../scripts/check-models.sh`](../scripts/check-models.sh) | Depoyu tarar; dosya nereden gelirse gelsin (başka makine, merge, elle düzenleme) kapıyı kapatır — CI adımı |

Allowlist: yalnız `opus`, `sonnet`, `inherit` ve kanonik `claude-{opus,sonnet}-5` (`[1m]`/tarih eki biçim
varyantı) geçer; başka her değer engellenir (DECISIONS#0044). Gövde metninde geçen "haiku" kelimesi bulgu değildir — yalnız `model:` **beyanı** sayılır.
