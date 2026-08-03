# Audit Checklist — 8 eksen

Her eksen `✅ / ⚠️ / ❌` puanlanır; her bulguya `dosya:satır` kanıtı.

## 1. Mimari & Katmanlar
- Katman sınırları korunuyor mu? (presentation→domain→data yön kuralı, yasak import yok)
- SOLID ihlalleri (God Object, sızan bağımlılık, somut bağımlılık)
- Modülerlik: tek sorumluluk, döngüsel bağımlılık var mı?

## 2. Kod Kalitesi
- `05-kod-kalitesi` anti-pattern'leri: Magic Number, Primitive Obsession, Dead Code, Shotgun Surgery
- Fonksiyon boyutu/karmaşıklığı, isimlendirme, gereksiz yorum
- DRY/KISS/YAGNI ihlalleri, kopyalanmış kod blokları

## 3. Güvenlik
- Hardcoded secret/credential/token (maskele!), `.env` git'te mi?
- Girdi doğrulama, path traversal, injection yüzeyleri
- Bağımlılık riski (bilinen zafiyet, terk edilmiş paket), dosya izinleri

## 4. Testler
- Test var mı, kritik yolları kapsıyor mu? Kırık/atlanan test?
- Test edilebilirlik (DI, saf fonksiyon), regression test kültürü

## 5. Dokümantasyon
- README güncel ve doğru mu? Kurulum/çalıştırma adımları işliyor mu?
- `CLAUDE.md` gerçeği yansıtıyor mu (drift)? ADR'lar mevcut/güncel mi?
- Public API/komut dokümante mi?

## 6. `.claude` Sağlığı
- `rules/` çekirdek set tam mı, `settings.json` geçerli mi?
- `skills/agents/hooks` çalışır ve tutarlı mı (format, isim)?
- `.claude/CHANGELOG.md` ile gerçek durum arasında drift?
- `claude-foundation` ile senkron mu (governance)?

## 7. Bağımlılık & Borç
- TODO/FIXME/HACK yoğunluğu ve yaşı
- Güncel olmayan bağımlılıklar, lock dosyası tutarlılığı
- Ölü kod / kullanılmayan dosyalar

## 8. Git Hijyeni
- Commit konvansiyonu (Conventional Commits, atfsız) uygulanıyor mu?
- Branch durumu, commit edilmemiş yığılma, büyük binary'ler
- `.gitignore` kapsamı (build çıktısı, secret, `settings.local.json`)
