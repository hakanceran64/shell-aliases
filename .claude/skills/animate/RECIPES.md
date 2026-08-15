# Animasyon reçeteleri

En sık gelen durumların hazır implementasyonları. Reçeteden başla, sonra uyarla — sıfırdan
kurma.

Eğriler `SKILL.md`'de tanımlı `--ease-out`, `--ease-in-out` ve `--ease-drawer` token'larıdır.

---

## Buton basma

Basılabilir her öğe. Arayüzün kullanıcıyı duyduğunun anında kanıtı.

```css
.button {
  transition: transform 160ms var(--ease-out);
}

.button:active {
  transform: scale(0.97);
}
```

`scale()` çocukları da ölçekler — etiket ve ikonlar birlikte gelir; fiziksel bir basış gibi
okunmasının sebebi bu.

Burada hover gate'i gerekmez: `:active` dokunmatikte gerçek bir basıştır. `:hover` stilini ayrıca
gate'le.

---

## Dropdown, popover, menü, select

Havadan değil, tetikleyicisinden büyür.

```css
.popover {
  transform-origin: var(--transform-origin); /* Base UI sağlar */
  transition:
    opacity 200ms var(--ease-out),
    transform 200ms var(--ease-out);
}

.popover[data-starting-style],
.popover[data-ending-style] {
  opacity: 0;
  transform: scale(0.95);
}
```

`transform-origin` işin bütün özü — panel tıkladığın şeyden çıkmış görünmeli.

---

## Tooltip

Popover'la aynı şekil, daha hızlı; artı çoğu implementasyonun kaçırdığı detay.

```css
.tooltip {
  transform-origin: var(--transform-origin);
  transition:
    transform 125ms var(--ease-out),
    opacity 125ms var(--ease-out);
}

.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}

/* Bir tooltip açıkken komşuları anında açılır */
.tooltip[data-instant] {
  transition-duration: 0ms;
}
```

İlk gecikme kazara tetiklenmeyi önler. Sonrasında hem gecikmeyi hem animasyonu atlamak tüm
toolbar'ı hızlandırır.

---

## Modal

Ortada kalan tek popover.

```css
.modal {
  transform-origin: center; /* muaf — bir tetikleyiciye bağlı değil */
  transition:
    opacity 250ms var(--ease-out),
    transform 250ms var(--ease-out);
}

.modal[data-starting-style],
.modal[data-ending-style] {
  opacity: 0;
  transform: scale(0.96);
}

.backdrop {
  transition: opacity 250ms var(--ease-out);
}
```

Backdrop'ın opacity'sini onunla birlikte animate et ki tek bir yüzey gibi okunsunlar.

---

## Drawer / sheet

```css
.drawer {
  transform: translateY(0);
  transition: transform 500ms var(--ease-drawer);
}

.drawer[data-closed] {
  transform: translateY(100%);
}
```

Vaul drawer'ı içeri animate etmeden önce böyle gizler.

Üzerine drag eklendiğinde bu bir jest problemine dönüşür — aşağıdaki **Drag ile kapatma**'ya bak.

---

## Toast

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 400ms ease,
    transform 400ms ease;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

- `ease-out` yerine `ease`, tipik UI'dan biraz yavaş: Sonner'ın zarif okunmasının sebebi kısmen
  hareketin genel UI bütçesine değil bileşenin kişiliğine göre ayarlanmış olması.
- `@starting-style` yoksa mount bayrağına düş:

```jsx
useEffect(() => { setMounted(true); }, []);
// <div data-mounted={mounted}>
```

Toast'lar yığılıp liste yeniden akarken opacity değişimi height değişimiyle uyumlu çalışmalı.
Bu ikilinin formülü yoktur — doğru hissedene kadar ayarla, ertesi gün tekrar bak.

---

## Accordion / collapse

```css
.content {
  overflow: hidden;
  transition:
    height 200ms var(--ease-out),
    opacity 200ms var(--ease-out);
}
```

Kısa tut — bu, her frame'de layout maliyeti olan nadir animasyonlardan biri; uzun süre hem pahalı
hem ağır hissettirir. İçerik yüksekliğini JS'te ölç (ya da bunu veren headless bir primitive
kullan); `auto`'ya animate etme.

---

## Grup girişini kademelendir (stagger)

Kullanıcının ara sıra gördüğü bir liste/grid için — her gün kaydırıp geçtiği bir liste için değil.

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms var(--ease-out) forwards;
}

.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
.item:nth-child(4) { animation-delay: 150ms; }

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Stagger dekoratiftir — oynarken etkileşimi asla bloke etmemeli.

---

## Hold to confirm

Düz tıklamayla kazara tetiklenmesi kolay olan yıkıcı aksiyonlar için.

```css
.overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms var(--ease-out); /* bırakma: çevik */
}

.button:active .overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;             /* basma: yavaş ve kararlı */
}

.button:active {
  transform: scale(0.97);
}
```

Burada `linear` doğru — dolgu bir ilerleme göstergesidir, ilerleme ease yapmaz.

---

## Renk geçişli tab göstergesi

Tab listesinde tek tek renk geçişlerinin zamanlaması hiçbir zaman tam oturmaz. Onun yerine kırp.

Tab listesini kopyala. Kopyayı aktif state olarak biçimlendir — farklı arka plan, farklı metin
rengi. Kopyayı yalnız aktif tab görünecek şekilde kırp ve değişimde clip'i animate et:

```css
.tabs-active-copy {
  clip-path: inset(0 60% 0 20%); /* aktif tab'ın konumundan sürülür */
  transition: clip-path 250ms var(--ease-in-out);
}
```

Metin ve arka plan kusursuz senkronla birlikte değişir; çünkü iki renk interpole edilmiyor, tek
bir öğe açığa çıkarılıyor.

---

## Scroll reveal

Yalnız pazarlama yüzeyleri. Kullanıcının her gün girdiği işlevsel UI'a bunu yapma.

```css
.reveal {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 600ms var(--ease-in-out);
}

.reveal[data-visible] {
  clip-path: inset(0 0 0 0);
}
```

`IntersectionObserver` ile ya da Motion'ın `useInView`'ı (`{ once: true, margin: "-100px" }`) ile
tetikle. Bir kez oynat — her kaydırmada yeniden animate etmek, okuruyla kavga eden bir arayüzdür.

---

## Drag ile kapatma

Jest reçetesi. Süre değil spring, çünkü kullanıcı hareketi yarıda tersine çevirebilir.

```js
// Mesafeyle değil, fiskeyle de kapat
const timeTaken = Date.now() - dragStartTime.current;
const velocity = Math.abs(swipeAmount) / timeTaken;

if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) {
  dismiss();
}
```

```js
// transform'u sürüklenen öğeye doğrudan yaz.
// Parent'taki bir CSS değişkeninden sürmek her çocuk için stil recalc'ı tetikler.
element.style.transform = `translateY(${distance}px)`;
```

İyi bir drag'i kötüsünden ayıran dört detay:

- **Pointer capture** drag başlar başlamaz; imleç öğenin sınırlarından çıksa da devam eder.
- **Çoklu dokunma koruması** — yeni dokunma noktalarında `if (isDragging) return`; yoksa drag
  ortasında parmak değiştirmek öğeyi zıplatır.
- **Sınırların ötesinde damping** — doğal kenarın ötesine sürüklendikçe öğe daha az hareket eder.
  Gerçek şeyler durmadan önce yavaşlar.
- **Duvar değil sürtünme** — aşırı sürüklemeyi reddetmek yerine artan dirençle izin ver.

Kesilen bir drag'in hızını koruması için spring ile yerleştir:

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }
```

---

## Oturmayan crossfade'i maskeleme

Geçiş sırasında iki state gözle görülür şekilde üst üste biniyorsa ve easing/süre ayarı bunu
düzeltmiyorsa dikişi blur'la:

```css
.content {
  transition:
    filter 200ms ease,
    opacity 200ms ease;
}

.content.transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

Blur olmadan göz, yer değiştiren iki ayrı nesne okur. Blur ikisini tek bir algılanan dönüşüme
harmanlar. 20px altında tut — ağır blur pahalıdır, özellikle Safari'de.

---

## Kütüphanesiz, programatik

Hareket JS kontrolü gerektiriyor ama bağımlılık gerektirmiyorsa WAAPI CSS düzeyinde performans verir:

```js
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
);
```

Donanım hızlandırmalı, kesilebilir, bundle maliyeti yok.
