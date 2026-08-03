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

## Model politikası

- **opus** — çok-adımlı orkestrasyon, mimari planlama.
- **sonnet** — kod yazımı, review, doc (varsayılan).
- **haiku** — basit/mekanik işler; karmaşık muhakeme için kullanılmaz.
