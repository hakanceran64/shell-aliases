# Kural 04: İzinler

**Severity:** error/warning · **Stages:** her tool çağrısı

## Kural

`.claude/settings.json` `permissions` bloğu izin matrisini tanımlar. Üç seviye:

| Seviye | Anlam | Örnek |
|--------|-------|-------|
| `allow` | sorulmadan çalışır | read-only git, `git commit`/`git push` (force hariç), `ls/grep/cat`, build araçları, hook script'leri |
| `ask` | her seferinde onay sorulur | `git pull`, `gh`, paket kurulumu, `rm`, `mv` |
| `deny` | hiçbir koşulda çalışmaz | `rm -rf /`, force push, `curl\|sh`, `.env`/secret okuma |

## `deny` bir tabandır

Kit'in `deny` listesi **asgari**dir: proje genişletebilir, **daraltamaz**. Bir projenin kendi
izin matrisini sahiplenmesi (`.ceran/ecosystem.yaml` → `local: [settings.json]`) yalnız
`allow`/`ask` için geçerlidir; `deny` girdilerini düşürmek 02-guvenlik'i delmek demektir.

`local` beyanı sync'i durdurduğu için bu taban otomatik gelmez — yeni bir kit `deny` girdisi
eklendiğinde sahiplenen projelere elle taşınır.

## İlkeler

- **En az ayrıcalık:** yeni bir komut gerekiyorsa önce `ask` ile başla; güvenli ve sık ise `allow`'a taşı.
- **Mutlak path yok:** izinler taşınabilir olmalı (`Bash(cmd:*)` formu, repo-yolu gömme yok).
- **Yıkıcı = deny:** geri-alınamaz operasyonlar `deny`'de, [02-guvenlik.md](02-guvenlik.md) ile hizalı.
- **Yerel override:** makineye-özel izinler `settings.local.json`'a (gitignore'lu) yazılır, kit'e girmez.
- **MCP:** `enableAllProjectMcpServers` ile proje `.mcp.json` server'ları otomatik etkin;
  dış erişim `WebFetch(domain:...)` ile beyaz listelenir.

## İlgili

- [settings.json](../settings.json) · [settings.local.json.example](../settings.local.json.example)
