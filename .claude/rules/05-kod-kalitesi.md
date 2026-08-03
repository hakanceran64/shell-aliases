# Kural 05: Kod Kalitesi

**Severity:** error · **Stages:** tüm kod yazımı (dil bağımsız)

## SOLID

| Prensip | Özet |
|---------|------|
| **S** — Single Responsibility | Her sınıf/fonksiyonun tek değişim nedeni olur |
| **O** — Open/Closed | Mevcut kodu değiştirmeden genişlet (yeni dosya/strateji, `if`-zinciri değil) |
| **L** — Liskov Substitution | Alt tip, üst tipin yerine davranışı bozmadan geçer |
| **I** — Interface Segregation | İstemci kullanmadığı arayüze bağımlı olmaz |
| **D** — Dependency Inversion | Yüksek seviye modül soyutlamaya bağımlı; somut detaya değil |

## Clean Code

- **İsimlendirme:** amacı açıklayan isimler (`confThreshold` → `confidenceThreshold`); boolean'da
  `is`/`has`/`can`; fonksiyonlar eylem ismi; kısaltma yok (`idx`/`tmp` → `frameIndex`/`tempBuffer`);
  sabitler `BÜYÜK_HARF`.
- **Fonksiyon:** tek iş yapar; ~20 satır sınırı; parametre ≤ 3 (fazlası → struct/obje); yan etkisiz
  ya da ismi yan etkiyi açıklar.
- **Yorum:** varsayılan **yok** — iyi isim açıklar. Yorum yalnızca **"neden"** için (gizli kısıtlama,
  workaround, sürpriz). Kodu anlatan yorumu sil, kodu düzelt.

```text
// YANLIŞ: Frame'i alır
auto frame = camera.requestFrame(200);
// DOĞRU: Neden 200ms — SDK minimum timeout öneriyor
auto frame = camera.requestFrame(FRAME_TIMEOUT_MS);
```

## DRY · KISS · YAGNI

- **DRY:** aynı mantık iki yerde → ortak fonksiyona taşı.
- **KISS:** en basit çözüm önce; karmaşıklık savunulabilmeli.
- **YAGNI:** gelecek için spekülatif kod/soyutlama yazma.

## Yasak anti-pattern'ler

| Anti-Pattern | Açıklama |
|--------------|----------|
| **God Object** | Her şeyi bilen/yapan sınıf |
| **Magic Number** | Anlamı belirsiz sabit → isimli sabit |
| **Primitive Obsession** | İlkel tip yığını → sarmalayıcı tip |
| **Dead Code** | Kullanılmayan kod → derhal sil (git geçmişi tutar) |
| **Shotgun Surgery** | Bir değişiklik çok dosyaya yayılır → sorumluluğu merkezileştir |
| **Feature Envy** | Sınıf başka sınıfın verisine aşırı erişir → veriyi taşı |

> Kaynak: `tof-camera-mastery` genel prensipler + `fire-and-water` architecture rule (genelleştirildi).
