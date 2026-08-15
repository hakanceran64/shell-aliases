# Plan şablonu

`/improve-animations`'ın yazdığı her plan bu yapıyı izler. Uygulayıcı, sıfır bağlamı ve sıfır
zevki olan daha zayıf bir model olabilir — plan her şeyi, tam olarak içermeli. "Yukarıdaki
denetim" ya da "konuştuğumuz easing" gibi referanslar yasak.

```markdown
# NNN — <Kısa emir kipi başlık>

- **Durum**: TODO
- **Commit**: <plan yazılırken `git rev-parse --short HEAD` çıktısı>
- **Severity**: HIGH | MEDIUM | LOW
- **Kategori**: <denetim kategorisi>
- **Tahmini kapsam**: <n dosya, kabaca boyut>

## Sorun

Ne yanlış, nerede ve ürünün hissine neden zarar veriyor. Her konumu `yol/dosya.tsx:123` biçiminde
göster ve mevcut kodu birebir alıntıla:

​```css
/* src/components/dropdown.css:14 — mevcut */
.dropdown { transition: all 400ms ease-in; }
​```

## Hedef

Tam bitiş durumu. Her değer açıkça yazılır — eğriler, süreler, spring config'leri, media query'ler.
Asla "daha güzel bir easing kullan" deme:

​```css
/* hedef */
.dropdown {
  transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out);
  transform-origin: var(--transform-origin);
}
​```

## Uyulacak repo konvansiyonları

Bu kod tabanı bunu zaten nasıl yapıyor; uygulayıcının taklit edeceği bir örnekle (token adları,
dosya yerleşimi, prop kalıpları):

- Easing token'ları `src/styles/tokens.css`'te yaşıyor; yeni eğriler oraya eklenir, ör.
  `--ease-out: cubic-bezier(0.23, 1, 0.32, 1);`
- Proje `ceran-design-system` tüketiyorsa (`.ceran/ecosystem.yaml`), token'ın kanonik kaynağı
  orasıdır — projede lokal bir kopya üretme, gerekiyorsa planda bunu açıkça belirt.
- <bunu zaten doğru yapan örnek dosya:satır>

## Adımlar

1. <Adım başına tek somut düzenleme: dosya, ne değişiyor, sonuçta oluşan kod.>
2. …

## Sınırlar

- <Kapsam dışı dosya/bileşen>'e DOKUNMA.
- Markup/yapı DEĞİŞTİRME — yalnız motion property'leri (bir adım aksini söylemedikçe).
- Yeni bağımlılık EKLEME.
- Bir adım bulduğun kodla eşleşmiyorsa (commit damgasından beri drift olmuşsa) doğaçlama yapma,
  DUR ve raporla.

## Doğrulama

- **Mekanik**: <tam komutlar — typecheck, lint, build — ve beklenen sonuç>.
- **His kontrolü**: UI'ı çalıştır, <etkileşim>'i tetikle ve şunları doğrula:
  - <gözlemlenebilir kontrol, ör. "dropdown merkezden değil tetikleyicisinden ölçekleniyor">
  - <ör. "toggle'a hızlı hızlı basmak animasyonu sıfırdan başlatmıyor">
  - DevTools → Animations panelinde oynatmayı %10'a al ve <detay>'ı doğrula.
  - `prefers-reduced-motion`'ı aç (Rendering paneli) ve hareketin kalktığını ama opacity
    feedback'inin kaldığını doğrula.
- **Bitti sayılır**: <makine ya da gözle kontrol edilebilir tamamlanma ölçütü>.
```

## Plan yazarına notlar

- Bulgu başına bir plan. İki bulgu aynı dosyaları ve aynı düzeltme kalıbını paylaşıyorsa (ör. aynı
  easing token'ının bileşenler arası değişimi) tek planda birleşebilir.
- Her değeri [AUDIT.md](AUDIT.md)'den al — asla ezberden yaklaşık yazma.
- His kontrolü opsiyonel değildir. Motion mekanik olarak doğru olup yine de yanlış hissedebilir;
  uygulayıcıya (ya da diff'i gözden geçiren insana) ağır çekimde bakacağı somut şeyler ver.
- Planları yazdıktan sonra `docs/plans/README.md`'yi oluştur ya da güncelle: planlar tablosu
  (numara, başlık, severity, durum), önerilen uygulama sırası ve planlar arası bağımlılıklar.
- Plan uygulandıktan sonra değişiklik `/review-animations` çıtasından geçmeli; kalıcı bir motion
  kararı doğduysa `/adr` ile kaydet.
