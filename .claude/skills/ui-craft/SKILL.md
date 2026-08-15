---
name: ui-craft
description: Web arayüzünde "doğru hissettiren" detayların referansı — animasyon karar çerçevesi (animate mi etmeli · amaç · easing · süre), spring temelleri, bileşen cilası ve zorunlu Before/After review formatı. Arayüz kodu yazarken ya da UI cilası tartışılırken kullan; tek bir animasyonu inşa etmek için `/animate`, mevcut motion'ı denetlemek için `/review-animations`.
when_to_use: "'bu buton nasıl daha iyi hissettirir', 'UI cilası', 'design engineering', '/ui-craft'"
---

# UI Craft — tasarım mühendisliği referansı

Arayüzde her detay birikir. Bu skill, "çalışıyor" ile "doğru hissettiriyor" arasındaki farkı
oluşturan kararların kanonik listesidir. Uygulama kalıpları ve derinlemesine teknikler için
[PATTERNS.md](PATTERNS.md).

**Kapsam:** web arayüzü (CSS · React/Vue/Svelte/Astro · Motion). Bu skill kod yazmaz; karar verir
ve gözden geçirir. Tek bir animasyonu baştan kurmak → `/animate`. Bir diff'i denetlemek →
`/review-animations`. Tüm kod tabanını taramak → `/improve-animations`.

## Çekirdek ilkeler

**Taste öğrenilir, doğuştan gelmez.** İyi zevk kişisel tercih değil, eğitilmiş bir sezgidir: iyi
işlere maruz kalarak, bir şeyin neden iyi hissettirdiğini düşünerek ve tekrarlayarak gelişir.
UI yazarken sadece çalıştırma — en iyi arayüzlerin neden öyle hissettirdiğini tersine mühendislik yap.

**Görünmeyen detaylar birikir.** Kullanıcıların çoğu detayı bilinçli fark etmez; amaç da budur.
Bir özellik tam beklendiği gibi davrandığında kimse durup düşünmez. Görünmez doğruluğun toplamı,
insanların nedenini bilmeden sevdiği arayüzleri üretir.

**Güzellik kaldıraçtır.** İnsanlar araçları yalnız işlevine değil, bütün deneyimine göre seçer.
İyi öntanımlılar ve iyi animasyonlar gerçek bir farklılaştırıcıdır.

## Zorunlu review formatı

UI kodu gözden geçirirken **markdown tablosu** kullan. "Before:" / "After:" satırlarından oluşan
liste **kullanma**.

| Before | After | Neden |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Property'yi adıyla yaz; `all` istenmeyen property'leri GPU dışında animate eder |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Gerçek dünyada hiçbir şey yoktan var olmaz |
| Dropdown'da `ease-in` | `ease-out` + güçlü custom curve | `ease-in` kullanıcının en dikkatli baktığı anı geciktirir |
| Buton'da `:active` state yok | `:active { transform: scale(0.97) }` | Buton basıldığını hissettirmeli |
| Popover'da `transform-origin: center` | `var(--transform-origin)` | Popover tetikleyicisinden büyümeli (modal hariç — o ortada kalır) |

"Neden" sütunu kısa gerekçeyi taşır. Her bulguyu `dosya:satır` ile göster.

## Animasyon karar çerçevesi

Animasyon kodu yazmadan önce şu dört soruyu **sırayla** yanıtla.

### 1. Bu animate etmeli mi?

**Soru:** kullanıcı bunu ne sıklıkta görecek?

| Sıklık | Karar |
| --- | --- |
| Günde 100+ (klavye kısayolu, command palette) | **Animasyon yok. Asla.** |
| Günde onlarca (hover, liste gezinme) | Kaldır ya da fark edilmeyecek kadar azalt |
| Ara sıra (modal, drawer, toast) | Standart animasyon |
| Nadir / ilk kez (onboarding, kutlama, başarı) | Delight bütçesi burada |

**Klavyeyle başlatılan aksiyonları asla animate etme.** Günde yüzlerce kez tekrarlanırlar;
animasyon onları yavaş ve kullanıcının aksiyonundan kopuk hissettirir. Raycast'in aç/kapa
animasyonu yoktur — günde yüzlerce kez açılan bir şey için doğru olan budur.

### 2. Amacı ne?

Her animasyon "bu neden animate ediyor?" sorusunu yanıtlamalı. Geçerli amaçlar:

- **Feedback** — arayüzün kullanıcıyı duyduğunu doğrulamak (basınca ölçek küçülmesi)
- **Uzamsal tutarlılık** — nereden gelip nereye gittiğini göstermek (toast aynı kenardan girer ve çıkar)
- **State göstergesi** — durum değişimini okunur kılmak
- **Sarsıcı değişimi önlemek** — ışınlanan içeriğe köprü kurmak
- **Açıklama** — bir özelliğin nasıl çalıştığını göstermek (yalnız pazarlama/onboarding)
- **Delight** — yalnızca "nadir / ilk kez" katmanında

Amacı bu kelimelerden biriyle adlandıramıyorsan yapma. Sık görülen bir öğede "havalı duruyor"
durma sebebidir.

Ayrıca **işlevi** kontrol et: kullanıcının okuduğu ya da üzerinde işlem yaptığı veri, stil için
hareket etmemeli. Dekoratif mouse-tracking pazarlama sayfasına aittir, bankacılık uygulamasındaki
grafiğe değil.

### 3. Hangi easing?

| Durum | Easing |
| --- | --- |
| Giriş veya çıkış | `ease-out` |
| Ekranda hareket / morph | `ease-in-out` |
| Hover / renk değişimi | `ease` |
| Sabit hareket (marquee, progress) | `linear` |
| Öntanımlı | `ease-out` |

**UI'da asla `ease-in` kullanma.** Yavaş başlar; bu da kullanıcının en dikkatli baktığı ilk anı
geciktirir. `ease-out` 200ms'de, `ease-in` 200ms'den *daha hızlı hissettirir*.

**Yerleşik CSS easing'leri fazla zayıf.** Bunları kullan:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* UI için güçlü ease-out */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* ekran içi hareket için */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS benzeri drawer eğrisi (Ionic) */
```

Listede olmayan bir eğri gerekiyorsa [easing.dev](https://easing.dev/) veya
[easings.co](https://easings.co/) üzerinden al — elle uydurma. Özellikle `cubic-bezier(0.4, 0, 0.2, 1)`
(Material'in öntanımlısı) tanıdık geldiği için yazılır ve kararlı bir animasyonda fazla zayıf kalır.

### 4. Ne kadar hızlı?

| Öğe | Süre |
| --- | --- |
| Buton basma feedback'i | 100–160ms |
| Tooltip, küçük popover | 125–200ms |
| Dropdown, select | 150–250ms |
| Modal, drawer | 200–500ms |
| Pazarlama / açıklayıcı | Daha uzun olabilir |

**Kural: UI animasyonları 300ms altında kalır.** 180ms'lik bir dropdown, 400ms'likten daha
duyarlı hissettirir.

**Algılanan performans:** hız yalnız "çevik hissettirmek" değil, uygulamanın hızının nasıl
algılandığını doğrudan etkiler. Hızlı dönen bir spinner yüklemeyi daha hızlı hissettirir (gerçek
süre aynıyken). İlk tooltip açıldıktan sonra komşularının gecikmesiz açılması tüm toolbar'ı
hızlandırır.

## Spring animasyonları

Spring'ler fiziği taklit ettikleri için süre tabanlı animasyonlardan daha doğal hissettirir.
Sabit süreleri yoktur; parametrelere göre yerleşirler.

**Ne zaman:** momentumlu drag, "canlı" hissetmesi gereken öğeler, yarıda kesilebilen jestler,
dekoratif mouse-tracking.

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }            // Apple yaklaşımı — akıl yürütmesi kolay, önerilen
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }  // klasik fizik — daha fazla kontrol
```

Bounce'ı 0.1–0.3 aralığında tut; UI'ın çoğunda bounce'tan kaçın — drag-to-dismiss ve oyuncul
etkileşimlere sakla.

**Kesilebilirlik avantajı:** spring'ler yarıda kesildiğinde hızlarını korur; CSS keyframe'leri
sıfırdan başlar. Bu yüzden kullanıcının yön değiştirebileceği jestler için spring doğru araçtır.

Apple'ın damping/response parametrelendirmesi ve momentum projeksiyonu için → `/apple-design`.

## Asla ship etme

Bitirmeden önce kendi kontrolün. Her biri `/review-animations`'da otomatik blok:

| Asla | Yerine |
| --- | --- |
| `transition: all` | Property'leri tek tek yaz |
| `scale(0)` girişi | `scale(0.95)` + `opacity: 0` |
| UI öğesinde `ease-in` | `ease-out` ya da güçlü custom curve |
| Klavye kısayolunda / günde 100+ aksiyonda animasyon | Animasyon yok |
| Gerekçesiz 300ms üstü UI süresi | 150–250ms |
| Tetikleyiciye bağlı popover'da `transform-origin: center` | `var(--transform-origin)` (modal muaf) |
| Toast/toggle gibi hızlı tetiklenende keyframe | CSS transition |
| `width`/`height`/`margin`/`padding`/`top`/`left` animasyonu | `transform` / `opacity` |
| Yük altında Motion `x`/`y`/`scale` prop'ları | Tam `transform` string'i |
| Gate'siz `:hover` hareketi | `@media (hover: hover) and (pointer: fine)` |
| `prefers-reduced-motion` yokluğu | Daha yumuşak varyant (sıfır değil) |
| Her şeyin aynı anda girmesi | 30–80ms stagger |

## Ekosistem bağlantısı

- **Motion token'ları.** Proje `ceran-design-system` tüketiyorsa (`.ceran/ecosystem.yaml` →
  `consume.design-system`), easing/duration değerleri orada **token** olmalı; bileşen dosyasına
  elle cubic-bezier yazmak konsolidasyon bulgusudur. Design system'de henüz motion token'ı
  **tanımlı değil** (2026-08-15) — bu durumda değerleri projede tek bir token dosyasında topla ve
  yukarı besle (`docs/SYNC-QUEUE.md` akışı).
- **Kütüphane seçimi** kendi başına bir karar: `/pick-ui-library`. El yapımı toast/dropdown yazma.
- **Kalıcı bir motion kararı** verildiyse `/adr` ile kaydet.

---
> Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, Emil Kowalski) —
> ekosisteme uyarlandı. Uyarlama notları: `claude-foundation/docs/UPSTREAM-SKILLS.md`.
