---
name: audit
description: Tüm projeyi gözden geçirir; mimari, güvenlik, kalite, test, doküman ve .claude sağlığı eksenlerinde bir audit raporu üretir ve bulgulardan backlog task'leri açar. Manuel çalıştırılır.
when_to_use: "Tetikleyiciler: '/audit', 'projeyi denetle', 'audit raporu çıkar', 'sağlık taraması yap'"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(git log:*), Bash(git status:*), Bash(ls:*), Bash(find:*), Bash(grep:*), Bash(wc:*), Bash(cloc:*)
---

# Proje Audit

Projeyi uçtan uca denetle, `docs/audit/AUDIT-<tarih>.md` raporu üret ve bulgulardan
`docs/backlog/BACKLOG.md`'ye task'ler aç. Derin muhakeme için ultrathink kullan.

## Hızlı bağlam (otomatik enjekte)

- Dosya ağacı (özet): !`git ls-files 2>/dev/null | head -200`
- Dosya/dizin sayısı: !`git ls-files 2>/dev/null | wc -l`
- Son commit'ler: !`git log --oneline -15 2>/dev/null`
- Çalışma ağacı durumu: !`git status --short 2>/dev/null`
- `.claude` envanteri: !`find .claude -type f 2>/dev/null | sort`
- TODO/FIXME borcu: !`grep -rniE "TODO|FIXME|HACK|XXX" --include=*.* -l . 2>/dev/null | grep -v node_modules | head -30`

## Yöntem

1. **Kapsamı belirle.** Yukarıdaki bağlam + `Glob`/`Grep` ile dilleri, katmanları, test/build
   yapılandırmasını tespit et. Büyük dosyaları ve giriş noktalarını oku.
2. **Eksen eksen denetle.** [`checklist.md`](checklist.md)'deki 8 ekseni uygula; her bulguya
   `dosya:satır` kanıtı ver. Spekülasyon değil, gözlem.
3. **Puanla.** Her eksen için `✅ iyi · ⚠️ dikkat · ❌ sorun` ve kısa gerekçe.
4. **Rapor yaz.** [`report-template.md`](report-template.md)'i doldur → `docs/audit/AUDIT-<YYYY-MM-DD>.md`.
   Dizin yoksa oluştur. Aynı gün ikinci audit ise `-2` ekle.
5. **Backlog'a task aç.** `⚠️`/`❌` her bulgu için `docs/backlog/BACKLOG.md`'ye bir task ekle
   (dosya yoksa oluştur). Format:
   ```
   - [ ] [P{1|2|3}] {eksen}: {kısa başlık} — {dosya:satır} (AUDIT-<tarih>)
   ```
   Öncelik: `❌`→P1, `⚠️`→P2, iyileştirme önerisi→P3.
6. **Özet dön.** Operatöre: eksen skorları tablosu + en kritik 3 task + rapor yolu.

## Kısıtlar

- **Salt analiz** — bu skill kod düzeltmez, yalnız rapor + task üretir.
- Mevcut backlog task'lerini tekrarlama; `BACKLOG.md`'yi okuyup yinelenenleri atla.
- Rapor Türkçe; `dosya:satır` referansları zorunlu.
- Hassas içerik (secret) bulursan raporda **maskeleyerek** bildir, içeriği yazma.

## İlgili

- [checklist.md](checklist.md) · [report-template.md](report-template.md)
- Kurallar: [05-kod-kalitesi](../../rules/05-kod-kalitesi.md) · [02-guvenlik](../../rules/02-guvenlik.md)
