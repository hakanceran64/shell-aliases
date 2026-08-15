# UI Craft — uygulama kalıpları

`SKILL.md`'deki karar çerçevesinin uygulama tarafı. Bir bileşen inşa ederken ya da bir cila
sorusuna yanıt ararken buradan başla.

## Bileşen inşa ilkeleri

### Butonlar duyarlı hissettirmeli

`:active`'de `transform: scale(0.97)`. Anında feedback verir; arayüz kullanıcıyı gerçekten
dinliyormuş gibi hissettirir.

```css
.button {
  transition: transform 160ms var(--ease-out);
}

.button:active {
  transform: scale(0.97);
}
```

Basılabilir her öğe için geçerli. Ölçek ince olmalı (0.95–0.98).

### Asla `scale(0)`'dan animate etme

Gerçek dünyada hiçbir şey tamamen yok olup yeniden belirmez. `scale(0)`'dan gelen öğeler
hiçlikten çıkmış gibi görünür. `scale(0.9)` ya da üstünden başla, `opacity` ile birleştir.
Sönmüş bir balonun bile görünür bir şekli vardır.

```css
/* Kötü */
.entering { transform: scale(0); }

/* İyi */
.entering { transform: scale(0.95); opacity: 0; }
```

### Popover'lar origin-aware olmalı

Popover tetikleyicisinden büyümeli, merkezinden değil. Öntanımlı `transform-origin: center`
neredeyse her popover için yanlıştır. **İstisna: modal** — bir tetikleyiciye bağlı olmadığı,
viewport'ta ortada belirdiği için `center` doğrudur.

```css
/* Base UI bu değişkeni kendisi sağlar */
.popover { transform-origin: var(--transform-origin); }
```

### Tooltip: sonraki hover'larda gecikmeyi atla

Tooltip'ler kazara tetiklenmeyi önlemek için gecikmeli açılmalı. Ama bir tooltip açıldıktan sonra
komşularına gelindiğinde gecikmesiz ve animasyonsuz açılmalı. Bu, ilk gecikmenin amacını bozmadan
her şeyi hızlandırır.

```css
.tooltip {
  transform-origin: var(--transform-origin);
  transition: transform 125ms var(--ease-out), opacity 125ms var(--ease-out);
}

.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}

/* Sonraki tooltip'lerde animasyonu atla */
.tooltip[data-instant] { transition-duration: 0ms; }
```

### Kesilebilir UI için keyframe değil transition

CSS transition'ları animasyon ortasında kesilip yeni hedefe yönlendirilebilir; keyframe'ler
sıfırdan başlar. Hızla tetiklenebilen her etkileşimde (toast eklenmesi, toggle) transition daha
pürüzsüz sonuç verir.

```css
/* Kesilebilir — dinamik UI için doğru */
.toast { transition: transform 400ms ease; }

/* Kesilemez — dinamik UI'da kaçın */
@keyframes slideIn { from { transform: translateY(100%); } to { transform: translateY(0); } }
```

### Kusurlu geçişleri blur ile maskele

İki state arasındaki crossfade, easing ve süre denemelerine rağmen yanlış hissettiriyorsa geçiş
sırasında hafif `filter: blur(2px)` ekle.

**Blur neden işe yarar:** blur olmadan crossfade sırasında iki ayrı nesne görürsün — eski ve yeni
state üst üste. Bu doğal görünmez. Blur ikisini harmanlayarak gözü tek bir pürüzsüz dönüşüm
algılamaya iter.

Blur'u 20px altında tut; ağır blur pahalıdır, özellikle Safari'de.

### Giriş için `@starting-style`

JS olmadan giriş animasyonunun modern CSS yolu:

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

React'te `useEffect` ile `mounted: true` kurma kalıbının yerini alır. Tarayıcı desteği yetmiyorsa
`data-mounted` kalıbına düş:

```jsx
useEffect(() => { setMounted(true); }, []);
// <div data-mounted={mounted}>
```

## CSS transform

### `translate` yüzdeleri

`translate()` içindeki yüzde değerleri öğenin **kendi boyutuna** görelidir. `translateY(100%)`
öğeyi kendi yüksekliği kadar taşır — gerçek boyutu ne olursa olsun. Sonner toast'ları, Vaul da
drawer'ı böyle konumlandırır.

```css
.drawer-hidden { transform: translateY(100%); }  /* drawer yüksekliğinden bağımsız çalışır */
```

Sabit piksel yerine yüzdeyi tercih et: daha az hataya açık ve içeriğe uyum sağlar.

### `scale()` çocukları da ölçekler

`width`/`height`'in aksine `scale()` öğenin çocuklarını da ölçekler. Butonu basınca ölçeklerken
font, ikon ve içerik orantılı küçülür — bu bir bug değil, özellik.

### Derinlik için 3D transform

`rotateX()` / `rotateY()` + `transform-style: preserve-3d` ile CSS'te gerçek 3D. Yörünge
animasyonları, kart çevirme ve derinlik efektleri JS'siz mümkün.

```css
.wrapper { transform-style: preserve-3d; }

@keyframes orbit {
  from { transform: translate(-50%, -50%) rotateY(0deg)   translateZ(72px) rotateY(360deg); }
  to   { transform: translate(-50%, -50%) rotateY(360deg) translateZ(72px) rotateY(0deg); }
}
```

## `clip-path` ile animasyon

`clip-path` yalnız şekil aracı değil; CSS'in en güçlü animasyon araçlarından biri.

`clip-path: inset(top right bottom left)` dikdörtgen bir kırpma bölgesi tanımlar; her değer
öğeyi o kenardan "yer".

```css
.hidden  { clip-path: inset(0 100% 0 0); }  /* sağdan tamamen gizli */
.visible { clip-path: inset(0 0 0 0); }     /* tamamen görünür */
```

**Kullanım alanları:**

- **Hold-to-delete:** renkli overlay'de `inset(0 100% 0 0)` → `:active`'de 2s `linear` ile
  `inset(0 0 0 0)`; bırakınca 200ms `ease-out` ile geri.
- **Kusursuz renk geçişli tab'lar:** tab listesini kopyala, kopyayı "aktif" stille (farklı arka
  plan, farklı metin rengi) biçimlendir, kopyayı yalnız aktif tab görünecek şekilde kırp ve tab
  değişiminde clip'i animate et. Tek tek renk geçişlerinin zamanlamasıyla asla ulaşılamayacak bir
  senkronizasyon verir.
- **Scroll reveal:** `inset(0 0 100% 0)` → `inset(0 0 0 0)`; `IntersectionObserver` ya da Motion'ın
  `useInView` (`{ once: true, margin: "-100px" }`) ile tetikle.
- **Karşılaştırma slider'ı:** iki görseli üst üste koy, üsttekini `inset(0 50% 0 0)` ile kırp, sağ
  inset değerini sürükleme konumuna göre ayarla. Ek DOM yok, tamamen donanım hızlandırmalı.

## Jest ve drag

- **Momentum ile kapatma.** Eşiği geçmeyi zorunlu kılma; hızı hesapla
  (`Math.abs(dragDistance) / elapsedTime`). Hız ~0.11'i aşıyorsa mesafeden bağımsız kapat. Hızlı
  bir fiske yetmeli.

  ```js
  const timeTaken = Date.now() - dragStartTime.current;
  const velocity = Math.abs(swipeAmount) / timeTaken;
  if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) dismiss();
  ```

- **Sınırda damping.** Kullanıcı doğal sınırın ötesine sürüklediğinde direnç uygula: ne kadar çok
  sürüklerse öğe o kadar az hareket etsin. Gerçek hayatta hiçbir şey aniden durmaz, önce yavaşlar.
- **Pointer capture.** Drag başlar başlamaz öğe tüm pointer event'lerini yakalasın; böylece
  imleç öğenin sınırlarından çıksa da sürükleme devam eder.
- **Çoklu dokunma koruması.** Drag başladıktan sonra gelen dokunma noktalarını yok say
  (`if (isDragging) return`). Yoksa drag ortasında parmak değiştirmek öğeyi zıplatır.
- **Duvar değil sürtünme.** Yukarı sürüklemeyi tamamen engellemek yerine artan dirençle izin ver.

## Performans

- **Yalnız `transform` ve `opacity` animate et.** Bunlar layout ve paint'i atlayıp GPU'da çalışır.
  `padding`, `margin`, `height`, `width` üç render adımını da tetikler.
- **CSS değişkenleri kalıtsaldır.** Parent'ta bir CSS değişkenini değiştirmek tüm çocukların
  stilini yeniden hesaplatır. Çok öğeli bir drawer'da container üzerinde `--swipe-amount`
  güncellemek pahalı bir recalc'a yol açar; `transform`'u doğrudan öğeye yaz.

  ```js
  element.style.setProperty('--swipe-amount', `${d}px`);  // kötü: tüm çocuklarda recalc
  element.style.transform = `translateY(${d}px)`;         // iyi: yalnız bu öğe
  ```

- **Motion (Framer Motion) kısayolları donanım hızlandırmalı DEĞİL.** `x`/`y`/`scale` prop'ları
  ana iş parçacığında `requestAnimationFrame` ile çalışır. Donanım hızlandırması için tam
  `transform` string'ini kullan:

  ```jsx
  <motion.div animate={{ x: 100 }} />                          // yük altında frame düşürür
  <motion.div animate={{ transform: "translateX(100px)" }} />  // donanım hızlandırmalı
  ```

- **Yük altında CSS animasyonları JS'i yener.** CSS animasyonları ana iş parçacığı dışında çalışır;
  tarayıcı yeni sayfa yüklerken rAF tabanlı animasyonlar frame düşürür. Önceden belirlenmiş
  hareket için CSS, dinamik ve kesilebilir hareket için JS.
- **Programatik CSS animasyonu için WAAPI.** JS kontrolü + CSS performansı; donanım hızlandırmalı,
  kesilebilir, kütüphanesiz.

  ```js
  element.animate(
    [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
    { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
  );
  ```

## Erişilebilirlik

Animasyon hareket hastalığı tetikleyebilir. Reduced motion, **daha az ve daha yumuşak** animasyon
demektir — sıfır değil. Anlamayı kolaylaştıran opacity/renk geçişlerini koru; yer değiştirme ve
konum animasyonlarını kaldır.

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; }  /* transform tabanlı hareket yok */
}

@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); }  /* dokunmatikte tap sahte hover üretir */
}
```

```jsx
const shouldReduceMotion = useReducedMotion();
const closedX = shouldReduceMotion ? 0 : '-100%';
```

## Sevilen bileşen inşa etme (Sonner ilkeleri)

Haftalık 13M+ npm indirmeli Sonner'ı inşa etmekten çıkan ve her bileşene uygulanabilen ilkeler:

1. **Developer experience belirleyicidir.** Hook yok, context yok, karmaşık kurulum yok. Bir kez
   `<Toaster />` koy, her yerden `toast()` çağır. Benimseme sürtünmesi azaldıkça kullanım artar.
2. **İyi öntanımlılar, seçeneklerden önemlidir.** Kutudan çıktığı gibi güzel olsun; kullanıcıların
   çoğu hiç özelleştirmez.
3. **İsim kimlik yaratır.** "Sonner" (Fransızca "çalmak"), "react-toast"tan daha zarif. Yeri
   geldiğinde keşfedilebilirliği akılda kalıcılığa feda et.
4. **Kenar durumlarını görünmez şekilde ele al.** Sekme gizliyken toast sayaçlarını duraklat,
   yığılmış toast'lar arasındaki boşlukları pseudo-element ile doldurup hover state'i koru,
   drag sırasında pointer event'lerini yakala. Kullanıcı bunları fark etmez — doğrusu da budur.
5. **Dinamik UI'da keyframe değil transition.**
6. **İyi bir dokümantasyon sitesi kur.** İnsanlar kullanmadan önce ürüne dokunabilmeli.

### Uyum (cohesion)

Sonner'ın animasyonu kısmen bütün deneyim uyumlu olduğu için tatmin edicidir: easing ve süre
kütüphanenin havasına uyar — tipik UI animasyonlarından biraz daha yavaştır ve daha zarif
hissetmek için `ease-out` yerine `ease` kullanır. Animasyon stili toast tasarımıyla, sayfa
tasarımıyla, isimle uyum içindedir.

Değer seçerken bileşenin **kişiliğini** hesaba kat: oyuncul bir bileşen daha zıplayabilir;
profesyonel bir dashboard net ve hızlı olmalı.

### Opacity + height kombinasyonu

Bir listeye öğe girip çıkarken opacity değişimi height animasyonuyla iyi çalışmalı. Bu genelde
deneme yanılmadır; formülü yoktur — doğru hissedene kadar ayarla.

### Asimetrik giriş/çıkış zamanlaması

Kullanıcının **karar verdiği** faz yavaş, sistemin **yanıt verdiği** faz hızlı olmalı.
Hold-to-delete'te basma 2s `linear`, bırakma 200ms `ease-out`.

```css
.overlay { transition: clip-path 200ms ease-out; }            /* bırakma: hızlı */
.button:active .overlay { transition: clip-path 2s linear; }  /* basma: yavaş ve kararlı */
```

## Stagger

Birden çok öğe birlikte giriyorsa görünüşlerini kademelendir. Öğeler arası 30–80ms; daha uzun
gecikmeler arayüzü yavaş hissettirir. Stagger dekoratiftir — oynarken **asla** etkileşimi bloke
etmemeli.

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms var(--ease-out) forwards;
}
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
.item:nth-child(4) { animation-delay: 150ms; }

@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
```

## Animasyon hata ayıklama

- **Ağır çekim testi.** Süreyi geçici olarak 2–5 katına çıkar ya da DevTools animasyon
  denetleyicisinde oynatma hızını düşür. Bak: renkler pürüzsüz geçiyor mu yoksa iki ayrı state
  üst üste mi görünüyor? Easing doğru mu, ani duruyor mu? `transform-origin` doğru mu? Eşzamanlı
  property'ler (opacity, transform, color) senkron mu?
- **Kare kare inceleme.** Chrome DevTools → Animations paneli, eşgüdümlü property'ler arasındaki
  zamanlama kaymasını ortaya çıkarır.
- **Gerçek cihazda test.** Dokunmatik etkileşimler (drawer, swipe) için fiziksel cihaz şart.
  Telefonu USB ile bağla, dev sunucuna IP üzerinden git, Safari remote devtools kullan.
- **Ertesi gün taze gözle bak.** Geliştirirken kaçırdığın kusurları ertesi gün fark edersin.
