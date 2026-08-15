# Sonner API referansı

Kesin prop'lar, tipler ve öntanımlı değerler. `toast()`'a geçilen seçenekler, Toaster'ın
`toastOptions`'ında ayarlanan aynı seçenekleri ezer.

## `<Toaster />`

| Prop | Tip | Öntanımlı | Açıklama |
| --- | --- | --- | --- |
| `theme` | `string` | `'light'` | `'light'`, `'dark'` ya da `'system'`. |
| `richColors` | `boolean` | `false` | Error ve success state'lerini renklendirir. |
| `expand` | `boolean` | `false` | Toast'lar öntanımlı olarak açık (yoksa hover'da açılır). |
| `visibleToasts` | `number` | `3` | Görünür toast sayısı. |
| `id` | `string` | – | Toaster id'si; `toast()`'ın `toasterId` seçeneğiyle hedeflenir. |
| `position` | `string` | `'bottom-right'` | `top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right`. |
| `closeButton` | `boolean` | `false` | Tüm toast'lara kapatma butonu ekler. |
| `offset` | `string \| number \| object` | `'32px'` | Ekran kenarlarından ofset. Nesne biçimi kenar bazlıdır: `{ bottom: '24px', right: '16px' }`. |
| `mobileOffset` | `string \| number \| object` | `'16px'` | Ekran genişliği < 600px olduğunda ofset. |
| `swipeDirections` | `array` | konuma göre | İzin verilen swipe-to-dismiss yönleri. |
| `dir` | `string` | `'ltr'` | Metin yönü. |
| `hotkey` | `string` | `⌥/alt + T` | Toaster alanına focus veren klavye kısayolu. |
| `invert` | `boolean` | `false` | Açık modda koyu toast, koyu modda açık. |
| `toastOptions` | `object` | – | Her toast'a uygulanan öntanımlı seçenekler (aşağıdaki `toast()` seçeneklerinden herhangi biri). |
| `gap` | `number` | `14` | Açıkken toast'lar arası boşluk. |
| `icons` | `object` | – | Öntanımlı ikonları değiştirir: `{ success, info, warning, error, loading }`; `null` birini kaldırır. |

## `toast()` seçenekleri

`toast(message, options)` — mesaj bir string, JSX ya da JSX döndüren bir fonksiyondur. Toast'ın
id'sini döndürür.

| Seçenek | Tip | Öntanımlı | Açıklama |
| --- | --- | --- | --- |
| `description` | `ReactNode` | – | Başlığın altına render edilir; JSX döndüren fonksiyon da kabul eder. |
| `closeButton` | `boolean` | `false` | Kapatma butonu ekler. |
| `invert` | `boolean` | `false` | Açık modda koyu toast, koyu modda açık. |
| `duration` | `number` | `4000` | Otomatik kapanmadan önceki milisaniye. `Infinity` toast'ı kalıcı kılar. |
| `position` | `string` | `'bottom-right'` | Bu toast'ın konumu. |
| `dismissible` | `boolean` | `true` | `false` ise kullanıcı toast'ı kapatamaz. |
| `icon` | `ReactNode` | – | Metnin önündeki ikon; `null` öntanımlıyı kaldırır. |
| `action` | `ReactNode \| { label, onClick }` | – | Birincil buton; `onClick` içinde `event.preventDefault()` çağrılmadıkça tıklama toast'ı kapatır. |
| `cancel` | `ReactNode \| { label, onClick }` | – | İkincil buton; tıklama toast'ı kapatır. |
| `actionButtonStyle` | `object` | `{}` | Action butonunun stilleri. |
| `cancelButtonStyle` | `object` | `{}` | Cancel butonunun stilleri. |
| `id` | `string` | – | Custom id; aynı id ile `toast()`'ı tekrar çağırmak mevcut toast'ı günceller. |
| `testId` | `string` | – | e2e testleri için `data-testid` olarak render edilir. |
| `toasterId` | `string` | – | Bu toast'ın render edileceği toaster'ın id'si. |
| `style` | `object` | – | Toast için satır içi stiller. |
| `classNames` | `object` | – | Parça bazlı class'lar: `{ toast, title, description, actionButton, cancelButton, closeButton }`. `unstyled` değilse `!important` gerekir. |
| `unstyled` | `boolean` | `false` | Tüm öntanımlı stilleri kaldırır. |
| `onDismiss` | `(toast) => void` | – | Kapatma butonuna tıklandığında ya da toast swipe ile kapatıldığında tetiklenir. |
| `onAutoClose` | `(toast) => void` | – | Toast `duration` sonunda kendiliğinden kapandığında tetiklenir. |
| `containerAriaLabel` | `string` | `'Notifications'` | Toast container'ının ARIA etiketi. |

## Fonksiyonlar

| Fonksiyon | Amaç |
| --- | --- |
| `toast(message, opts?)` | Toast render eder; id'sini döndürür. |
| `toast.success / .error / .info / .warning(message, opts?)` | Eşleşen ikonlu tipli toast. |
| `toast.loading(message, opts?)` | Spinner'lı toast; id ile güncelle. |
| `toast.promise(promise, { loading, success, error })` | Promise ile çözülen loading toast'ı; `success`/`error` string, JSX, sonucun fonksiyonu ya da toast seçenekleri nesnesi kabul eder. |
| `toast.custom((t) => jsx, opts?)` | Headless toast — senin JSX'in, Sonner'ın davranışı. |
| `toast.dismiss(id?)` | Bir toast'ı kapatır; id'siz çağrılırsa hepsini. |
| `toast.getActiveToasts()` | Tüm aktif toast'lar; React dışında da kullanılabilir. |
| `useSonner()` | `{ toasts }` döndüren React hook'u. |
