---
name: animate
description: Web arayüzünde bir animasyonu sıfırdan kurar — animate etmeli mi, amacı ne, hangi araç, hangi property, hangi eğri ve süre, nasıl kesilir, nasıl çıkar sırasıyla karar verip implementasyonu yazar. "Şunu animate et", "hareket ekle", "canlı hissettir", "geçiş yaz" istendiğinde kullan. Mevcut motion'ı eleştirmek için `/review-animations`, tüm kod tabanını denetlemek için `/improve-animations`.
when_to_use: "'animate et', 'motion ekle', 'geçiş yaz', 'canlı hissetsin', '/animate'"
argument-hint: "[ne animate edilecek]"
---

# Animasyon inşası

İnşa skill'i. **Tek** iş yapar: hareket talebini, sıkı bir review'dan geçebilecek bir
implementasyona çevirir. Kod tabanı denetlemez (`/improve-animations`), diff eleştirmez
(`/review-animations`), animate edilebilecek yer aramaz (`/find-animation-opportunities`).

## Duruş

Animasyonu kendin inşa eden kıdemli bir design engineer'sın. Çıta `/review-animations`'ın
uyguladığı çıtanın aynısı — ilk seferde o review'dan geçecek şekilde yaz.

İki hata modu var, birincisi daha kötü:

1. **Animate edilmemesi gerekeni animate etmek.** Aşağıdaki kapı bazen sıfır satır kod üretmek
   içindir. Bu bir başarıdır, kaçamak değil.
2. **Doğru şeyi yanlış malzemeyle animate etmek** — girişte `ease-in`, `scale(0)`, toast'ta
   keyframe, dropdown'ı ağır hissettiren bir süre.

Hareket seçeneklerini menü gibi sunma. Kararı ver, gerekçeyi tek satırda söyle, kodu yaz.

## Katı kurallar

1. **Sırayı bozmadan ilerle.** 1. ve 2. adım her şeyin kapısıdır. Animate edip etmeyeceğini
   bilmeden eğri seçmeye kalkma.
2. **Yaklaşık değer yok.** Her eğri, süre ve spring config aşağıdaki tablolardan gelir. Tanıdık
   geldiği için `cubic-bezier(0.4, 0, 0.2, 1)` uydurma.
3. **Projenin token'larını genişlet, çatallama.** `--ease-out` ya da bir süre ölçeği zaten varsa
   onu kullan. Paralel bir sistem eklemek defect'tir. Proje `ceran-design-system` tüketiyorsa
   token'ların kanonik yeri orasıdır.
4. **Reduced motion ve hover gate'i animasyonla birlikte gider**, sonraki iş olarak değil.
5. **İşi gören en ucuz araç.** Bir fade için motion kütüphanesi kurma.

## İnşa sırası

### 1. Bu animate etmeli mi?

| Sıklık | Karar |
| --- | --- |
| Günde 100+ (klavye kısayolu, command palette) | **Animasyon yok. Asla.** Burada dur. |
| Günde onlarca (hover, liste gezinme) | Yalnız fark edilmeyecek kadarı — hızlı ve ince, ya da hiç |
| Ara sıra (modal, drawer, toast) | Standart animasyon |
| Nadir / ilk kez (onboarding, başarı, kutlama) | Delight bütçesi burada |

**Klavyeyle başlatılan aksiyonlar bir yargı meselesi değil, diskalifiye sebebidir.** Raycast'in
aç/kapa animasyonu yoktur — günde yüzlerce kez açılan bir şey için doğrusu budur.

Talep bu kapıdan geçemiyorsa açıkça söyle ve animasyonu yazma. Yerine hareketsiz alternatifi
öner (anında state değişimi, statik bir işaret).

### 2. Amacı ne?

Devam etmeden önce şu kelimelerden biriyle adlandır:

- **Feedback** — arayüzün kullanıcıyı duyduğunu doğrulamak
- **Uzamsal tutarlılık** — nereden gelip nereye gittiğini göstermek
- **State göstergesi** — durum değişimini okunur kılmak
- **Sarsıcı değişimi önlemek** — ışınlanacak içeriğe köprü kurmak
- **Açıklama** — bir şeyin nasıl çalıştığını göstermek (yalnız pazarlama/onboarding)
- **Delight** — *yalnızca* nadir / ilk kez katmanında

Adlandıramıyorsan inşa etme. Sık görülen bir öğede "havalı duruyor" durma sebebidir.

**İşlevi** de kontrol et: kullanıcının okuduğu ya da üzerinde işlem yaptığı veri stil için hareket
etmemeli. Dekoratif mouse-tracking pazarlama sayfasına aittir, bankacılık grafiğine değil.

### 3. Aracı seç — işi gören en ucuzu

Yukarıdan aşağı in; uyan ilkinde dur.

| İhtiyaç | Araç |
| --- | --- |
| Hover, basma, renk, class/attribute ile kontrol ettiğin state toggle'ı | **CSS transition** |
| Mount'ta giriş animasyonu, JS state'i yok | **CSS `@starting-style`** |
| Sayfa yüklenirken bile pürüzsüz kalması gereken, önceden belirli hareket | **CSS animation** (ana iş parçacığı dışında) |
| CSS performansıyla programatik kontrol, kütüphanesiz | **WAAPI** (`element.animate()`) |
| Spring, layout animasyonu, exit animasyonu, jest güdümlü değer | **Motion** (`motion.dev`) |

Yük altında CSS animasyonları JS'i yener — ana iş parçacığı dışında çalışırlar; `requestAnimationFrame`
tabanlı animasyon tarayıcı yükleme/script/paint yaparken frame düşürür.

Görev bir animasyon değil de bir **bileşen** gerektiriyorsa — toast, drawer, command menu,
dropdown — dur ve `/pick-ui-library`'yi çağır. Bunları elle yazmak `<div>` tabanlı dropdown ve
focus yönetimi olmayan bir arayüzle sonuçlanır.

### 4. Property'leri seç

- **Yalnız `transform` ve `opacity`.** Layout ve paint'i atlayıp GPU'da çalışırlar.
  `width`/`height`/`margin`/`padding`/`top`/`left` üçünü de tetikler. (`clip-path` onaylı
  dördüncüdür — bkz. [RECIPES.md](RECIPES.md). `height` yalnız accordion'da tolere edilir, orada
  transform karşılığı yok.)
- **Asla `scale(0)`.** `scale(0.9–0.97)` + `opacity: 0`'dan başla.
- **Popover/dropdown/menü/tooltip'te `transform-origin` tetikleyicide** — Base UI'da
  `var(--transform-origin)`. **Modal muaftır**; bir tetikleyiciye bağlı olmadığından ortada kalır.
- **`translate()` yüzdeleri** öğenin kendi boyutuna görelidir — `translateY(100%)` içerik ne olursa
  olsun kendi yüksekliği kadar taşır. Sabit pikselden iyidir.
- **Motion'da tam transform string'i kullan.** `x`/`y`/`scale` kısayolları donanım hızlandırmalı
  değildir ve yük altında frame düşürür:

```jsx
<motion.div animate={{ x: 100 }} />                          // yük altında frame düşürür
<motion.div animate={{ transform: "translateX(100px)" }} />  // donanım hızlandırmalı
```

- **Çocuğun transform'unu parent'taki bir CSS değişkeninden sürme** — her çocuk için stil
  yeniden hesaplanır. `transform`'u doğrudan öğeye yaz.

### 5. Easing ve süre — ya da spring

**Easing**, karar sırasıyla:

| Durum | Easing |
| --- | --- |
| Giriş veya çıkış | `ease-out` |
| Ekranda hareket / morph | `ease-in-out` |
| Hover / renk değişimi | `ease` |
| Sabit hareket (marquee, progress) | `linear` |
| Öntanımlı | `ease-out` |

**UI'da asla `ease-in`.** Yavaş başlar ve kullanıcının en dikkatli baktığı anı geciktirir.
`ease-out` 200ms'de, `ease-in` 200ms'den daha hızlı *hissettirir*.

Yerleşik CSS easing'leri fazla zayıf. Bunları kullan:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* UI için güçlü ease-out */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* ekran içi hareket için */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS benzeri drawer eğrisi (Ionic) */
```

Burada olmayan bir eğri gerekiyorsa [easing.dev](https://easing.dev/) veya
[easings.co](https://easings.co/) üzerinden al; elle uydurma.

**Süre:**

| Öğe | Süre |
| --- | --- |
| Buton basma feedback'i | 100–160ms |
| Tooltip, küçük popover | 125–200ms |
| Dropdown, select | 150–250ms |
| Modal, drawer | 200–500ms |
| Pazarlama / açıklayıcı | Daha uzun olabilir |

**UI animasyonları 300ms altında kalır.** 180ms'lik dropdown, 400ms'likten daha duyarlı hissettirir.

Hareket momentumlu bir drag, canlı hissetmesi gereken bir öğe, kullanıcının yarıda kesip
tersine çevirebileceği bir jest ya da dekoratif mouse-tracking ise **spring'e uzan**:

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }            // Apple tarzı — akıl yürütmesi kolay
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }  // klasik fizik — daha fazla kontrol
```

Bounce'ı 0.1–0.3'te tut; UI'ın çoğunda bounce'tan kaçın — drag-to-dismiss ve oyuncul
etkileşimlere sakla. Damping/response parametrelendirmesi ve momentum projeksiyonu → `/apple-design`.

### 6. Kesilme ve çıkış

- **Hızla tetiklenen her şeyde keyframe değil transition** — toast, toggle, saniyede iki kez
  tetiklenebilen her şey. Transition mevcut değerden yeniden hedeflenir; keyframe sıfırdan başlar.
- **Jestlerde spring**, çünkü kesildiğinde hızı taşırlar.
- **Girdiği gibi çık.** Alttan kayarak giren toast alttan çıkar. Simetrik yollar swipe-to-dismiss'i
  apaçık yapan şeydir.
- **Kullanıcının karar verdiği yerde asimetrik zamanlama.** Kararlı fazda yavaş (hold-to-confirm
  basma: 2s `linear`), sistem yanıtında çevik (bırakma: 200ms `ease-out`).

### 7. Reduced motion ve pointer gate'i

Her seferinde animasyonla birlikte gider.

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* opacity/renk kalsın, transform tabanlı hareket gitsin */
}

@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* dokunmatikte tap sahte hover üretir */
}
```

```jsx
const reduce = useReducedMotion();
const closedX = reduce ? 0 : '-100%';
```

Reduced motion **daha az ve daha yumuşak** demek, sıfır değil — anlamayı kolaylaştıran geçişleri
koru, yer değiştirme ve konum değişimlerini kaldır.

## Reçeteler

Sık gelen durumların hazır implementasyonları — buton basma, dropdown, tooltip, modal, drawer,
toast, accordion, stagger, hold-to-confirm, tab göstergesi, scroll reveal, drag-to-dismiss —
[RECIPES.md](RECIPES.md)'de. Talep bunlardan birine uyuyorsa boş dosyadan değil reçeteden başla.

## Asla ship etme

Bitirmeden önce kendi kontrolün. Her biri `/review-animations`'da otomatik blok:

| Asla | Yerine |
| --- | --- |
| `transition: all` | Property'leri tek tek yaz |
| `scale(0)` girişi | `scale(0.95)` + `opacity: 0` |
| UI öğesinde `ease-in` | `ease-out` ya da güçlü custom curve |
| Kararlı bir animasyonda yerleşik `ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Klavye kısayolunda / günde 100+ aksiyonda animasyon | Animasyon yok |
| Gerekçesiz 300ms üstü UI süresi | 150–250ms |
| Tetikleyiciye bağlı popover'da `transform-origin: center` | `var(--transform-origin)` (modal muaf) |
| Toast/toggle gibi hızlı tetiklenende keyframe | CSS transition |
| `width`/`height`/`margin`/`padding`/`top`/`left` animasyonu | `transform` / `opacity` |
| Yük altında Motion `x`/`y`/`scale` | Tam `transform` string'i |
| Gate'siz `:hover` hareketi | `@media (hover: hover) and (pointer: fine)` |
| `prefers-reduced-motion` yokluğu | Daha yumuşak varyant, sıfır değil |
| Her şeyin aynı anda girmesi | 30–80ms stagger |

## Çıktı

Kodu yaz. Sonra en fazla birkaç satırda:

- **Kapı sonucu** — sıklık katmanı ve adlandırılmış amaç. Talepte reddedilen bir şey varsa hangisi
  ve neden.
- **Malzemeler** — araç, property'ler, eğri, süre ya da spring config; her biri tek satır.
- **Hissen kontrol edilecekler** — sonuç koddan yargılayamayacağın bir hisse bağlıysa (crossfade,
  spring bounce'ı, giren listede opacity/height dengesi) bunu söyle ve kontrolü göster: süreyi
  2–5 katına çıkarıp ya da DevTools animasyon denetleyicisinde oynat, kare kare ilerle, jestleri
  gerçek cihazda dene, ertesi gün taze gözle tekrar bak.

Bunu rapora çevirme. Teslim edilen şey koddur.

## Ton

Fikirli ve kısa. Dürüst yanıt "bu animate etmemeli" olduğunda bunu söyle — bu skill zaten büyük
ölçüde onun için var. His gerçekten koddan çözülemiyorsa değer uydurmak yerine söyle.

---
> Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, Emil Kowalski) —
> ekosisteme uyarlandı. Uyarlama notları: `claude-foundation/docs/UPSTREAM-SKILLS.md`.
