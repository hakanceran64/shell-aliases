# Animasyon standartları referansı

Review'ün arkasındaki kesin değerler, eğriler ve kurallar. Bulgularda yaklaşık yazmak yerine
buradan alıntıla.

## Animate etmeli mi? (sıklık tablosu)

| Sıklık | Karar |
| --- | --- |
| Günde 100+ (klavye kısayolu, command palette) | Animasyon yok. Asla. |
| Günde onlarca (hover, liste gezinme) | Kaldır ya da ciddi biçimde azalt |
| Ara sıra (modal, drawer, toast) | Standart animasyon |
| Nadir / ilk kez (onboarding, feedback, kutlama) | Delight eklenebilir |

**Klavyeyle başlatılan aksiyonları asla animate etme** — günde yüzlerce kez tekrarlanırlar;
animasyon onları yavaş ve kopuk hissettirir. (Raycast'in aç/kapa animasyonu yoktur — günde
yüzlerce kez kullanılan bir şey için doğrusu budur.)

Geçerli hareket amaçları: uzamsal tutarlılık, state göstergesi, açıklama, feedback, sarsıcı
değişimi önleme. Sık görülen bir öğede "havalı duruyor" geçerli değildir.

## Easing

Karar sırası:

- Giriş veya çıkış → **`ease-out`** (hızlı başlar, duyarlı hissettirir)
- Ekranda hareket / morph → **`ease-in-out`**
- Hover / renk değişimi → **`ease`**
- Sabit hareket (marquee, progress) → **`linear`**
- Öntanımlı → **`ease-out`**

**UI'da asla `ease-in`.** Yavaş başlar ve kullanıcının en dikkatli baktığı anı geciktirir.
`ease-out` 200ms'de, `ease-in` 200ms'den daha hızlı *hissettirir*.

Yerleşik CSS easing'leri fazla zayıf. Güçlü custom eğriler kullan:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* UI için güçlü ease-out */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* ekran içi hareket için */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS benzeri drawer eğrisi (Ionic) */
```

Eğrileri [easing.dev](https://easing.dev/) veya [easings.co](https://easings.co/) üzerinden bul —
sıfırdan elle uydurma.

## Süre

| Öğe | Süre |
| --- | --- |
| Buton basma feedback'i | 100–160ms |
| Tooltip, küçük popover | 125–200ms |
| Dropdown, select | 150–250ms |
| Modal, drawer | 200–500ms |
| Pazarlama / açıklayıcı | Daha uzun olabilir |

**Kural: UI animasyonları 300ms altında kalır.** 180ms'lik dropdown 400ms'likten daha duyarlı
hissettirir. Hızlı spinner yüklemeyi daha hızlı hissettirir (gerçek süre aynı). İlkinden sonra
anında açılan tooltip'ler toolbar'ı hızlandırır.

## Fizikselik

- **Asla `scale(0)`.** `scale(0.9–0.97)` + `opacity: 0`'dan başla. Gerçek dünyada hiçbir şey
  yoktan var olmaz.
- **Origin-aware popover.** Merkezden değil tetikleyiciden ölçekle:
  ```css
  .popover { transform-origin: var(--transform-origin); } /* Base UI */
  ```
  **Modal muaftır** — viewport'ta ortada belirir, `transform-origin: center` doğrudur.
- **Buton basma feedback'i.** `:active`'de `transform: scale(0.97)`,
  `transition: transform 160ms ease-out`. İnce tut (0.95–0.98). Basılabilir her öğe için geçerli.

## Spring'ler

Fiziği taklit ettikleri için doğal hissettirirler; sabit süreleri yoktur, parametrelere göre
yerleşirler. Kullanım: momentumlu drag, "canlı" öğeler (Dynamic Island), kesilebilir jestler,
dekoratif mouse-tracking.

```js
// Apple tarzı (akıl yürütmesi kolay) — önerilen
{ type: "spring", duration: 0.5, bounce: 0.2 }

// Klasik fizik (daha fazla kontrol)
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

Bounce'ı ince tut (0.1–0.3); UI'ın çoğunda bounce'tan kaçın — drag-to-dismiss ve oyuncul
etkileşimlere sakla. Spring'ler kesildiğinde hızlarını korur (keyframe sıfırdan başlar); bu yüzden
kullanıcının yarıda tersine çevirebileceği jestler için idealdirler.

Mouse etkileşimleri: değeri doğrudan mouse konumuna bağlamak yerine `useSpring` ile interpole et
(doğrudan bağlamak yapay ve momentumsuz hissettirir). Bunu yalnız hareket dekoratifken yap.

## Kesilebilirlik

CSS **transition**'ları animasyon ortasında kesilip yeniden hedeflenebilir; **keyframe**'ler
sıfırdan başlar. Hızla tetiklenen her şeyde (toast eklenmesi, toggle) transition daha pürüzsüzdür.

```css
/* Kesilebilir — dinamik UI için doğru */
.toast { transition: transform 400ms ease; }

/* Kesilemez — dinamik UI'da kaçın */
@keyframes slideIn { from { transform: translateY(100%); } to { transform: translateY(0); } }
```

JS'siz giriş için `@starting-style`:

```css
.toast {
  opacity: 1; transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

Eski tarayıcı yedeği: `useEffect(() => setMounted(true), [])` + `data-mounted` attribute'u.

## Asimetrik zamanlama

Kullanıcının karar verdiği yerde yavaş, sistemin yanıt verdiği yerde hızlı.

```css
.overlay { transition: clip-path 200ms ease-out; }            /* bırakma: hızlı */
.button:active .overlay { transition: clip-path 2s linear; }  /* basma: yavaş, kararlı */
```

## Performans

- **Yalnız `transform` ve `opacity` animate et** — layout/paint'i atlayıp GPU'da çalışırlar.
  `padding`/`margin`/`height`/`width`/`top`/`left` üç render adımını da tetikler.
- **Çocuğun transform'unu parent'taki CSS değişkeninden sürme** — tüm çocuklarda stil recalc'ı
  tetikler. `transform`'u doğrudan öğeye yaz.
  ```js
  element.style.setProperty('--swipe-amount', `${d}px`); // kötü: tüm çocuklarda recalc
  element.style.transform = `translateY(${d}px)`;        // iyi: yalnız bu öğe
  ```
- **Motion kısayolları donanım hızlandırmalı DEĞİL.** `x`/`y`/`scale` ana iş parçacığında rAF ile
  çalışır ve yük altında frame düşürür. Tam transform string'ini kullan:
  ```jsx
  <motion.div animate={{ x: 100 }} />                          // yük altında frame düşürür
  <motion.div animate={{ transform: "translateX(100px)" }} />  // donanım hızlandırmalı
  ```
- **Yük altında CSS animasyonları JS'i yener** — ana iş parçacığı dışında çalışırlar; rAF tabanlı
  animasyonlar tarayıcı yükleme/script/paint yaparken takılır. Önceden belirli hareket için CSS,
  dinamik/kesilebilir için JS.
- **WAAPI**, CSS performansıyla JS kontrolü verir (donanım hızlandırmalı, kesilebilir, kütüphanesiz):
  ```js
  element.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
    { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' });
  ```

## Transform ve clip-path

- **`translate` yüzdeleri** öğenin kendi boyutuna görelidir — `translateY(100%)` boyuttan bağımsız
  olarak kendi yüksekliği kadar taşır (Sonner/Vaul toast ve drawer'ı böyle konumlandırır). Sabit
  px yerine tercih et.
- **`scale()` çocukları da ölçekler** (font, ikon, içerik) — basma feedback'i için bir özellik.
- **3D**: `rotateX/Y` + `transform-style: preserve-3d` ile JS'siz derinlik/yörünge/çevirme.
- **`clip-path: inset(t r b l)`** güçlü bir animasyon aracıdır; her değer o kenardan içeri yer.
  Kullanım: scroll reveal (`inset(0 0 100% 0)` → `inset(0 0 0 0)`), hold-to-delete overlay'i,
  kusursuz tab renk geçişi (kopyala + aktif kopyayı kırp), karşılaştırma slider'ları.

## Jest ve drag

- **Momentumla kapatma**: mesafe eşiğini zorunlu kılma — hızı hesapla
  (`Math.abs(distance)/elapsedMs`), `> ~0.11` ise kapat. Bir fiske yetmeli.
- **Sınırda damping**: doğal kenarın ötesine sürüklendikçe daha az hareket (gerçek şeyler durmadan
  önce yavaşlar).
- **Pointer capture** drag başlar başlamaz; imleç sınırların dışına çıksa da devam eder.
- **Çoklu dokunma koruması**: drag başladıktan sonra ek dokunma noktalarını yok say
  (`if (isDragging) return`) — zıplamayı önler.
- **Sert duruş yerine sürtünme** — aşırı sürüklemeyi görünmez bir duvarla reddetmek yerine artan
  dirençle karşıla.

## Kusurlu crossfade'i maskeleme

Easing/süre ayarına rağmen crossfade iki state'i üst üste gösteriyorsa geçiş sırasında ince bir
`filter: blur(2px)` ekleyip tek bir algılanan dönüşüme harmanla. Blur'u 20px altında tut (ağır
blur pahalı, özellikle Safari'de).

## Stagger

Grup girişlerini kademelendir; öğeler arası 30–80ms. Daha uzun gecikmeler yavaş hissettirir.
Stagger dekoratiftir — oynarken etkileşimi asla bloke etmemeli.

```css
.item { opacity: 0; transform: translateY(8px); animation: fadeIn 300ms ease-out forwards; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
```

## Erişilebilirlik

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* opacity/renk kalsın, hareket gitsin */
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
koru, yer/konum değişimlerini kaldır.

## Hata ayıklama (his belirsizken review'de öner)

- **Ağır çekim**: süreyi 2–5 katına çıkar ya da DevTools animasyon denetleyicisini kullan. Renkler
  temiz geçiyor mu, easing ani duruyor mu, `transform-origin` doğru mu, eşgüdümlü property'ler
  senkron mu — kontrol et.
- **Kare kare**: Chrome DevTools → Animations paneli, eşgüdümlü property'ler arasındaki zamanlama
  kaymasını gösterir.
- **Jestler için gerçek cihaz** (drawer, swipe) — telefonu bağla, dev sunucuna IP ile git, Safari
  remote devtools kullan.
- **Ertesi gün taze göz** — geliştirirken görünmeyen kusurlar sonradan ortaya çıkar.

## Uyum (cohesion)

Hareketi bileşenin kişiliğine göre ayarla: oyuncul daha zıplayabilir; profesyonel bir dashboard
net ve hızlı olmalı. Sonner kısmen doğru hissettirir çünkü easing, süre, tasarım ve hatta isim
uyum içindedir — daha zarif durması için biraz daha yavaş ve `ease-out` yerine `ease`. Giren/çıkan
listelerde opacity + height dengesi deneme yanılmadır; formülü yoktur.

## Ekosistem notu

Aynı cubic-bezier ya da süre birden çok bileşende elle tekrarlanıyorsa bu bir **konsolidasyon
bulgusudur**. Proje `ceran-design-system` tüketiyorsa motion token'larının kanonik yeri orasıdır;
tanımlı token yoksa projede tek bir dosyada topla ve `docs/SYNC-QUEUE.md` akışıyla yukarı besle.
