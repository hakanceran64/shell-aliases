---
name: sonner
description: Sonner (React toast kütüphanesi) rehberi — kurulum ve Toaster bağlama, doğru toast() çağrısını seçme, promise ve loading toast'ları, güncelleme/kapatma/kalıcı kılma, styling, tema ve ikonlar, konumlandırma ve çoklu toaster. Sonner ile çalışırken ya da sorun giderirken kullan: görünmeyen toast, iki kez görünen toast, stilini kaybeden toast, Tailwind class'larını yok sayan toast, modal'ın arkasında kalan toast, dark mode'u izlemeyen toast.
when_to_use: "'toast çalışmıyor', 'sonner', 'bildirim stili', '/sonner'"
---

# Sonner ile çalışmak

[Sonner](https://sonner.emilkowal.ski) toast kütüphanesi için rehber skill'i. Bir görev Sonner
içeriyorsa — bağlamak, toast render etmek, stillendirmek ya da düzeltmek — önce bu dosyadan
yanıtla. `<Toaster />` ve `toast()` için tam prop tabloları [API.md](API.md)'de; kesin bir prop
adı, tip ya da öntanımlı değer gerektiğinde oku.

Toast'a gerçekten ihtiyaç olup olmadığı ayrı bir sorudur; kütüphane seçimi için
`/pick-ui-library`, toast giriş/çıkış hareketini ayarlamak için `/animate`.

## Kurulum

İki parça, sadece iki:

1. **Bir tane `<Toaster />`, bir kez mount edilir**, mümkün olduğunca köke yakın (Next.js'te
   `layout.tsx` — server component içinde çalışır). Sayfa başına ya da koşullu render etme; ikinci
   bir Toaster her toast'ı çiftler.
2. **`toast()` client kodundan çağrılır** — event handler, effect, callback. Düz bir fonksiyondur;
   hook ya da provider gerekmez. Ama sunucuda hiçbir şey yapmaz: bir server action içinde sonucu
   döndür ve `toast()`'ı onu alan client kodunda çağır.

```jsx
import { Toaster } from 'sonner'; // bir kez, layout'ta
import { toast } from 'sonner';   // client tarafında her yerde
```

## Doğru çağrıyı seçmek

| İstediğin | Çağrı |
| --- | --- |
| Düz mesaj | `toast('Başlık')` — ikinci satır için `{ description }` |
| Success / error / info / warning ikonu | `toast.success('…')`, `toast.error('…')` vb. |
| State'i kendin yönetirken spinner | `toast.loading('…')`, sonra id ile güncelle |
| Promise'e bağlı loading → success/error | `toast.promise(promise, { loading, success, error })` — success/error, çözülen değeri/hatayı alan fonksiyon kabul eder |
| Bir şey yapan buton | `{ action: { label, onClick } }` — `onClick` içinde `event.preventDefault()` çağrılmadıkça toast'ı kapatır; `cancel` ikincil varyanttır |
| Custom JSX, öntanımlı toast kabuğu | `toast(<jsx />)` |
| Custom JSX, hiç stil yok | `toast.custom((t) => <jsx />)` — headless; `t` kapatma için id verir |

## Reçeteler

**Toast güncelleme** — aynı `id` ile `toast()`'ı tekrar çağır; yalnız verdiğin prop'lar değişir.
`toast.success(…, { id })`'e geçmek tipi değiştirir. `toast.promise` olmadan loading → success
akışı böyle kurulur:

```jsx
const id = toast.loading('Yükleniyor…');
toast.success('Yüklendi', { id });
```

**Kalıcı kılma** — `{ duration: Infinity }`. **Kapatma** — `toast.dismiss(id)` ya da hepsi için
`toast.dismiss()`. **Aktif toast'ları okuma** — React'te `useSonner()`, dışında
`toast.getActiveToasts()`.

**Metinde link ya da bileşen** — başlık veya açıklama için fonksiyon geçir:
`toast(() => <a href="…">Görüntüle</a>)`.

**Çoklu toaster** — her birine bir `id` ver ve `toast('…', { toasterId: 'canvas' })` ile hedefle.
`toasterId` olmadan her toaster o toast'ı render eder.

**Kapanış callback'leri** — `onDismiss` kapatma butonu ya da swipe'ta, `onAutoClose` zaman aşımında
tetiklenir. Ayrıdırlar; tek bir "kapandı" callback'i yoktur.

## Styling — tırmanma merdiveni

Değişikliğin gerektirdiği kadar tırman. En üst basamağa erken atlamak sorun değil (önerilen bitiş
durumu odur); ortada takılıp kalmak sorundur.

1. **Öntanımlılar** — artı Toaster'da renkli success/error için `richColors`, temaya ters düşmek
   için `invert`.
2. **Satır içi ayarlar** — tüm toast'lar için Toaster'da `toastOptions={{ style: {…} }}`, ya da
   çağrı başına `style`.
3. **Parçalara class** — `toastOptions={{ classNames: { toast, title, description, actionButton,
   cancelButton, closeButton } }}`. Sonner'ın enjekte ettiği stiller cascade'i kazanır, bu yüzden
   her class'ın `!important` olması gerekir (Tailwind: `!text-red-900`). Birkaç şeyden fazlasını
   important işaretliyorsan dur — headless'a geç.
4. **Headless** — kendi JSX'inle `toast.custom()`; Sonner'ın konumlandırma, yığma ve swipe'ı kalır.
   Design system toast'ı için önerilen yaklaşım budur: kendi `toast()` soyutlamana sar.
   (`unstyled: true` ara bir çözüm olarak var, ama aynı çabayla headless daha fazla kontrol verir.)

**Ekosistem notu:** proje `ceran-design-system` tüketiyorsa 4. basamağı seç ve toast'ı design
system token'larıyla (renk, radius, spacing) kur. Elle hex ve px yazmak drift üretir.

**İkonlar** — tip başına öntanımlıları Toaster'ın `icons` prop'uyla, toast başına `icon` ile
değiştir; `null` kaldırır.

**Tema** — `theme` öntanımlı olarak `'light'`'tır ve işletim sistemini **izlemez**.
`theme="system"` geç ya da tema sağlayıcını bağla: `next-themes`'ten
`<Toaster theme={resolvedTheme} />`.

## Sorun giderme

| Belirti | Sebep → düzeltme |
| --- | --- |
| Toast hiç görünmüyor | Mount edilmiş `<Toaster />` yok ya da unmount olmuş (koşullu render, sayfa başına yerleştirme). Kökte bir tane mount et. Server action'dan çağırıyorsan: `toast()` yalnız client'ta çalışır — action'ın sonucunu client'ta kullan. |
| Aynı toast iki kez görünüyor | İki Toaster mount edilmiş (layout **ve** sayfa) — birini bırak. Ya da `toast()` bir effect içinde, React StrictMode'un dev çift çağrısıyla tetikleniyor — event handler'dan tetikle ya da sabit bir `id` geçir ki ikinci çağrı çiftlemek yerine güncellesin. |
| Tailwind/CSS class'ları etkisiz | Öntanımlı stiller onları eziyor. `!important` işaretle ya da `unstyled`/headless kullan (yukarıdaki merdiven). |
| Toast'lar tamamen stilsiz render oluyor (Astro'da, view transition'larda yaygın) | Sonner'ın enjekte ettiği stylesheet kayboldu — layout'ta açıkça import et: `import 'sonner/dist/styles.css'`. |
| Shadow DOM içinde stilsiz | Stiller shadow root'a değil `document.head`'e iniyor. İçinde `[data-sonner-toaster]` geçen style tag'ini shadow root'a kopyala. |
| Toast modal/overlay'in arkasında ya da kırpılıyor | Bir üst öğe stacking context yaratıyor (`transform`, `filter`, `overflow`) ya da overlay z-index'te toaster'ı geçiyor. `<Toaster />`'ı dialog/portal container'ın dışına, doküman köküne taşı. |
| Dark mode yok sayılıyor | `theme` öntanımlı `'light'` — `theme="system"` ayarla ya da çözülmüş temayı geç. |
| Success/error yeşil/kırmızı değil gri | Öntanımlı bu. Toaster'a `richColors` ekle. |
| Toast hiç kapanmıyor | `duration: Infinity`, `dismissible: false` ya da hiç sonuçlanmayan bir promise'li `toast.promise` — loading toast sonsuza kadar bekler. |
| `toast.promise` loading'de takılı | İlk argüman olarak bir promise (ya da promise döndüren fonksiyon) ister ve promise gerçekten resolve/reject olmalı. |
| Swipe-to-dismiss yanlış yöne gidiyor / çalışmıyor | Yönler `position`'dan türer. Toaster'da `swipeDirections` ile override et. |
| Toast her toaster'da görünüyor | Çoklu toaster hedefleme ister: her Toaster'a `id` ver ve `toast()` çağrısında `toasterId` geç. |
| Mobilde toast ekran kenarına fazla yakın | `offset` (masaüstü, öntanımlı 32px) ve `mobileOffset` (<600px, öntanımlı 16px) — sayı, CSS string'i ya da kenar bazlı nesne. |

---
> Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, Emil Kowalski) —
> ekosisteme uyarlandı (upstream adı: `ask-sonner`). Uyarlama notları:
> `claude-foundation/docs/UPSTREAM-SKILLS.md`.
