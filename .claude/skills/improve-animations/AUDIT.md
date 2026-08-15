# Animasyon denetim kılavuzu

Sekiz denetim kategorisi, her birinde ne aranacağı ve bulgu/planlarda alıntılanacak kesin hedef
değerler. Burada geçen hiçbir değeri yaklaşık yazma — kopyala.

## 1. Amaç ve sıklık

Her animasyon "bu neden animate ediyor?" sorusunu yanıtlamalı — uzamsal tutarlılık, state
göstergesi, feedback, açıklama ya da sarsıcı değişimi önleme. Sık görülen bir öğede "havalı
duruyor" bir amaç değildir.

| Sıklık | Karar |
| --- | --- |
| Günde 100+ (klavye kısayolu, command palette) | Animasyon yok. Asla. |
| Günde onlarca (hover, liste gezinme) | Kaldır ya da ciddi biçimde azalt |
| Ara sıra (modal, drawer, toast) | Standart animasyon |
| Nadir / ilk kez (onboarding, feedback, kutlama) | Delight eklenebilir |

**Ara:** klavyeyle başlatılan aksiyonlarda animasyon, aç/kapa geçişi olan command palette'ler
(Raycast'te yoktur — doğrusu budur), sürekli görülen liste öğelerinde ya da hover state'lerinde
dekoratif hareket. En güçlü düzeltme genelde **animasyonu silmektir**.

## 2. Easing ve süre

Easing karar sırası:

- Giriş veya çıkış → **`ease-out`** (hızlı başlar, duyarlı hissettirir)
- Ekranda hareket / morph → **`ease-in-out`**
- Hover / renk değişimi → **`ease`**
- Sabit hareket (marquee, progress) → **`linear`**
- Öntanımlı → **`ease-out`**

**UI'da `ease-in` her zaman bulgudur** — yavaş başlar ve kullanıcının en dikkatli baktığı anı
geciktirir. Yerleşik CSS easing'leri kararlı hareket için fazla zayıftır; planlar güçlü custom
eğrileri (repo konvansiyonuna uygun token olarak) getirmeli:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* UI için güçlü ease-out */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* ekran içi hareket için */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS benzeri drawer eğrisi */
```

Süre bütçeleri — **UI animasyonları 300ms altında kalır**:

| Öğe | Süre |
| --- | --- |
| Buton basma feedback'i | 100–160ms |
| Tooltip, küçük popover | 125–200ms |
| Dropdown, select | 150–250ms |
| Modal, drawer | 200–500ms |
| Pazarlama / açıklayıcı | Daha uzun olabilir |

**Ara:** her yerde `ease-in`, girişlerde çıplak `ease`/`linear`, UI öğelerinde 300ms üstü süreler,
toolbar'daki her tooltip'te gecikme + animasyon (ilkinden sonra anında açılmalı).

## 3. Fizikselik ve origin

- **Asla `scale(0)`** — gerçek dünyada hiçbir şey yoktan var olmaz. Hedef: `scale(0.9–0.97)` +
  `opacity: 0`.
- **Popover/dropdown/tooltip tetikleyicisinden ölçeklenir**, merkezinden değil:
  ```css
  .popover { transform-origin: var(--transform-origin); } /* Base UI */
  ```
  **Modal muaftır** — ortada belirir; `transform-origin: center` orada doğrudur, **bulgu yazma**.
- **Basma feedback'i**: `:active`'de `transform: scale(0.97)`,
  `transition: transform 160ms ease-out`. İnce tut (0.95–0.98).

**Ara:** `scale(0)`, başlangıç transform'u olmayan saf fade girişleri, tetikleyiciye bağlı
öğelerde `transform-origin: center` (ya da hiç), basma feedback'i olmayan basılabilir öğeler.

## 4. Kesilebilirlik

CSS **transition**'ları animasyon ortasında mevcut state'ten yeniden hedeflenir; **keyframe**'ler
sıfırdan başlar. Hızla tetiklenen ya da yarıda tersine çevrilebilen her şey (yığılan toast'lar,
toggle'lar, drag'ler, aç/kapa) transition ya da spring kullanmalı.

- JS'siz giriş: `@starting-style` (eski yedek: `useEffect` içinde kurulan `data-mounted`).
- Jest güdümlü hareket spring kullanmalı — kesildiğinde hızı taşırlar.
- Spring config, Apple tarzı (önerilen): `{ type: "spring", duration: 0.5, bounce: 0.2 }`.
  Bounce'ı ince tut (0.1–0.3); görünür bounce'ı drag-to-dismiss ve oyuncul anlara sakla.
- **Asimetrik zamanlama**: kararlı fazlar (basma, basılı tutma, yıkıcı onay) daha yavaş; sistemin
  yanıtı çevik. Basma-bırakmada simetrik zamanlama bulgudur.

**Ara:** toast/toggle/hızlı tetiklenen UI'da `@keyframes`, sabit süreli keyframe ile tween yapan
jest handler'ları, hız tabanlı kapatması olmayan drag'ler (yalnız mesafe eşiği değil,
`Math.abs(distance)/elapsedMs > ~0.11`), drag sınırlarında artan sürtünme yerine sert duruş.

## 5. Performans

- **Yalnız `transform` ve `opacity` animate et.** `width`/`height`/`margin`/`padding`/`top`/`left`
  layout + paint + composite tetikler.
- **`transition: all`** istenmeyen property'leri GPU dışında animate eder — her zaman bulgu.
- **Motion `x`/`y`/`scale` kısayolları donanım hızlandırmalı değil** — ana iş parçacığında çalışır
  ve yük altında frame düşürür. Hedef: tam transform string'i,
  `animate={{ transform: "translateX(100px)" }}`.
- **Çocuğun transform'unu parent'taki CSS değişkeninden sürme** — tüm çocuklarda stil recalc'ı
  tetikler. `transform`'u doğrudan öğeye yaz.
- Yük altında CSS (ve WAAPI) rAF tabanlı JS'i yener — önceden belirli hareket için CSS,
  dinamik/jest güdümlü için JS/spring.
- Geçiş sırasındaki `filter: blur()` değerini 20px altında tut — ağır blur pahalıdır, özellikle
  Safari'de.

**Ara:** `transition: all`, animate edilen layout property'leri, yoğun sayfalarda Motion kısayol
prop'ları, çocuk transform'unu süren `setProperty('--x', …)`, CSS'in yapabileceğini yapan rAF
döngüleri.

## 6. Erişilebilirlik

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* opacity/renk kalsın, hareket gitsin */
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* dokunmatikte tap sahte hover üretir */
}
```

Reduced motion **daha az ve daha yumuşak** demek, **sıfır değil** — anlamayı kolaylaştıran
geçişleri koru, konum değişimlerini kaldır. JS'te: `useReducedMotion()` ile transform değerlerini
dallandır.

**Ara:** `prefers-reduced-motion` ele alınmamış hareketler, gate'siz `:hover` hareketi, tüm
feedback'i sıfırlayan reduced-motion implementasyonları.

## 7. Uyum ve token'lar

- Hareket ürünün kişiliğine uymalı — oyuncul daha zıplayabilir, dashboard net kalır. Bileşenler
  arası uyumsuz kişilik bulgudur.
- Eğriler ve süreler paylaşılan **token** olarak yaşamalı. Neredeyse birbirinin aynı, elle yazılmış
  beş cubic-bezier bir konsolidasyon bulgusudur. **Ekosistem:** proje `ceran-design-system`
  tüketiyorsa token'ların kanonik yeri orasıdır; plan bunu belirtmeli.
- **30–80ms stagger**'ın yeri olan yerde her şeyin aynı anda girmesi. Stagger dekoratiftir —
  etkileşimi asla bloke etmemeli.
- İki state'i üst üste gösteren sarsıcı bir crossfade, geçiş sırasında ince `filter: blur(2px)` ile
  maskelenebilir.

**Ara:** tekrarlanan, birbirine yakın easing/süreler; net bir uygulamada tek bir zıplayan bileşen;
stagger'sız liste/grid girişleri; gözle görülür şekilde çift pozlanan crossfade'ler.

## 8. Kaçırılmış fırsatlar

Ekleyici kategori — animate etmeyen ama etmesi gereken yerler:

- Işınlanan state değişimleri (içerik takası, layout sıçraması) — kısa bir geçiş sarsıcılığı
  önlerdi.
- Uzamsal olarak bağlı UI (tetikleyicisinden çıkan panel) hiçbir hareket olmadan beliriyorsa,
  nereden geldiğini açıklayan bir hareket eksiktir.
- Nadir, yüksek duygulu anlar (ilk çalıştırma, başarı, kutlama) hak ettikleri delight bütçesinin
  hiçbiri kullanılmadan render ediliyorsa.
- Araçlar: `translate` yüzdeleri (`translateY(100%)` = öğenin kendi yüksekliği) ve
  `clip-path: inset()` reveal'ları — sabit piksel ofset kullanma.

En fazla birkaç tane raporla; gerçekten gözlemlediğin UX dikişlerine dayansın, dilek listesi olmasın.
