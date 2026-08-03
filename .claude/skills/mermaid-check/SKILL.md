---
name: mermaid-check
description: Markdown dosyalarındaki mermaid bloklarının sözdizimsel geçerliliğini doğrular. Tetikleyiciler — ".md yazıldı/düzenlendi", "mermaid kontrol et", "diyagram doğrula", "graph TD hatası".
allowed-tools: Bash, Read
---

# mermaid-check

`.md` dosyalarındaki ` ```mermaid ` bloklarını sözdizimsel olarak doğrular.
Bağımlılık yok — saf Python 3, ağ erişimi gerektirmez.

## Ne zaman kullan

- Bir `.md` dosyasına diyagram yazdıktan/değiştirdikten **hemen sonra**
- Doküman ağırlıklı bir repoda commit öncesi
- "diyagram bozuk görünüyor" / "mermaid render olmuyor" şikayetinde

## Kullanım

```bash
python3 .claude/skills/mermaid-check/validate.py <dosya.md> [dosya2.md ...]
python3 .claude/skills/mermaid-check/validate.py $(git diff --name-only --cached -- '*.md')
```

Çıkış: 0 tüm bloklar geçerli · 1 en az bir blok hatalı (satır + sebep basılır).

## Yakaladığı yaygın hatalar

| Hata | Doğrusu |
|---|---|
| `graph TD;` (eski sözdizimi) | `flowchart TD` |
| `A[node (1)]` — tırnaksız parantez | `A["node (1)"]` |
| `A → B` — unicode ok | `A --> B` |
| kapanmamış `subgraph` | her `subgraph` için `end` |
| tanımsız `:::myClass` | önce `classDef myClass ...` |
| düğüm metninde tırnaksız `:` `{}` `[]` | metni `"..."` içine al |

## Otomatikleştirme (opsiyonel)

Diyagram ağırlıklı repolarda `PostToolUse` hook'u ile `.md` yazımlarında
otomatik tetiklenebilir. Hook kit'te **varsayılan değildir** — her repo
diyagram ağırlıklı olmadığı için opt-in bırakıldı. Etkinleştirmek için
`.claude/settings.json` → `hooks.PostToolUse`:

```json
{ "matcher": "Edit|Write",
  "hooks": [{ "type": "command",
              "command": "python3 \"${CLAUDE_PROJECT_DIR:-.}/.claude/skills/mermaid-check/validate.py\"",
              "timeout": 30 }] }
```

## Kaynak

`Node`, `Roadmaps` ve `fire-and-water` repolarında **birebir aynı** (MD5 eşit)
`validate.py` bulundu; alan-bağımsız olduğu doğrulandıktan sonra kit'e alındı.
Üç kopya yerine tek kaynak.
