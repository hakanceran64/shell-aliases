# Seçici (picker)

Seçicinin görünümü **bir tasarım kararı değildir** — bu spec'tir. Aşağıdaki markup'ı, CSS'i ve
bağlantıları birebir kopyala; çalıştırma başına değişen tek şey varyant adları ve sayısıdır. Her
projede aynı kalır ki her zaman düzenek kromu gibi okunsun, asla yargılanan tasarımın parçası gibi
değil.

Alt-orta konumlanmış, yüzen koyu bir pill'dir. Koyu cam her sayfanın üstünde çalışır — açık da
olsa koyu da — bu yüzden temaya duyarlı değildir.

## Markup

Önce kayan vurgu span'i, varyant başına bir buton, ince bir ayraç, sonra replay butonu (yalnız en
az bir varyantın yeniden tetiklenecek hareketi varsa):

```html
<nav class="proto-picker" aria-label="Prototype variants">
  <span class="proto-picker-highlight" aria-hidden="true"></span>
  <button class="proto-picker-item" data-active aria-current="true">Quiet</button>
  <button class="proto-picker-item">Editorial</button>
  <button class="proto-picker-item">Playful</button>
  <span class="proto-picker-divider" aria-hidden="true"></span>
  <button class="proto-picker-item proto-picker-replay" aria-label="Replay animation (R)">↻</button>
</nav>
```

Bir framework içinde class adlarını ve yapıyı koru; yalnız render sözdizimi değişir.

## Stiller

```css
.proto-picker {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2147483647;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 4px;
  border-radius: 999px;
  background: rgba(10, 10, 10, 0.82);
  -webkit-backdrop-filter: blur(12px) saturate(1.4);
  backdrop-filter: blur(12px) saturate(1.4);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.08) inset,
    0 8px 24px rgba(0, 0, 0, 0.24),
    0 2px 6px rgba(0, 0, 0, 0.12);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 13px;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  user-select: none;
  -webkit-user-select: none;
}

.proto-picker-highlight {
  position: absolute;
  top: 4px;
  left: 0;
  height: 28px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  will-change: transform;
}

/* Kayma yalnız ilk paint'ten sonra (data-ready) açılır; yükleme animasyonlu olmasın. */
.proto-picker[data-ready] .proto-picker-highlight {
  transition:
    transform 250ms cubic-bezier(0.23, 1, 0.32, 1),
    width 250ms cubic-bezier(0.23, 1, 0.32, 1);
}

@media (prefers-reduced-motion: reduce) {
  .proto-picker[data-ready] .proto-picker-highlight { transition: none; }
}

.proto-picker-item {
  position: relative; /* vurgunun üstünde durur */
  display: flex;
  align-items: center;
  height: 28px;
  padding: 0 12px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: rgba(255, 255, 255, 0.55);
  font: inherit;
  cursor: pointer;
  transition: color 150ms ease-out;
}

.proto-picker-item:hover {
  color: rgba(255, 255, 255, 0.85);
}

.proto-picker-item:active {
  transform: scale(0.97);
}

.proto-picker-item:focus-visible {
  outline: 2px solid rgba(255, 255, 255, 0.4);
  outline-offset: 2px;
}

.proto-picker-item[data-active] {
  color: #fff;
}

.proto-picker-divider {
  width: 1px;
  height: 16px;
  margin: 0 4px;
  background: rgba(255, 255, 255, 0.12);
}

.proto-picker-replay {
  padding: 0 10px;
  font-size: 14px;
}

.proto-picker[data-position="top"] {
  bottom: auto;
  top: 24px;
}
```

## Kurallar

- **Birebir.** Bu değerler spec'tir. Proje font'u yok, marka rengi yok, tema değiştirme yok, ek
  gölge veya kenarlık yok. `ceran-design-system` token'ları buraya **girmez** — seçici bilinçli
  olarak üründen ayrı okunur.
- **Vurgu kayar; varyant değişimi anında kalır.** Aktif pill butonlar arasında animate olur
  (250ms, güçlü ease-out) — bu, seçicinin kendisi üzerindeki uzamsal feedback'tir. Önizlenen
  varyant ise geçişsiz değişir. `width` geçişi, transform/opacity kuralına bilinçli bir
  istisnadır: öğe 28px yüksekliğinde, mutlak konumlu ve layout bağımlısı yok; paint maliyeti
  ihmal edilebilir.
- **İzin verilen tek değişiklik:** bir varyant ekranın alt-ortasını kaplıyorsa (toast yığını,
  bottom sheet, dock) `data-position="top"` ver ki seçici işi örtmesin. Başka hiçbir şeyi
  değiştirilemez.
- **Replay koşulludur.** Replay butonunu ve ayracını yalnız en az bir varyantın yeniden
  tetiklenmeye değer bir giriş ya da state animasyonu varsa render et; statik bir karşılaştırma
  daha kısa bir pill alır.

## Davranış sözleşmesi

Düzeneğin nasıl render ettiğinden bağımsız olarak sözleşme sabittir:

- `1–N` sayı tuşları ve `←`/`→` varyant değiştirir; `R` yeniden oynatır. Focus bir input,
  textarea, select ya da contenteditable içindeyken veya bir modifier tuşu basılıyken klavye
  olaylarını yok say.
- Bir öğeye tıklamak ona geçer; her an tam olarak bir öğe `data-active` ve `aria-current="true"`
  taşır ve vurgu ona kayar.
- Seçim, yeniden yüklemede URL parametresiyle (`?v=2`) korunur; yoksa 1. varyanta düşer. Vurgu
  ilk konumunu animasyonsuz alır (`data-ready` ilk paint'ten sonra eklenir).
- Geçiş varyantı yeniden mount eder (giriş animasyonları tekrar oynasın); replay tuşu değiştirmeden
  yeniden mount eder.

## Referans bağlantı kodu

Standalone-HTML dalı için birebir; bir framework içinde aynı davranışı deyimsel şekilde ifade et
(`innerHTML` yerine state, `requestAnimationFrame` yerine key'li yeniden mount, vurgu ölçümü için
ref + layout effect).

```js
// `variants`, seçici sırasına göre varyant başına bir render fonksiyonu içeren dizidir.
const stage = document.getElementById('stage');
const picker = document.querySelector('.proto-picker');
const highlight = picker.querySelector('.proto-picker-highlight');
const items = [...picker.querySelectorAll('.proto-picker-item:not(.proto-picker-replay)')];
const replay = picker.querySelector('.proto-picker-replay');
let current = 0;

function moveHighlight() {
  const el = items[current];
  highlight.style.width = el.offsetWidth + 'px';
  highlight.style.transform = `translateX(${el.offsetLeft}px)`;
}

function mount(i) {
  stage.innerHTML = '';
  // Önce temizle, sonraki frame'de render et; giriş animasyonları tekrar oynasın.
  requestAnimationFrame(() => { stage.innerHTML = variants[i](); });
}

function setActive(i) {
  if (i < 0 || i >= variants.length) return;
  current = i;
  items.forEach((el, j) => {
    el.toggleAttribute('data-active', j === i);
    if (j === i) el.setAttribute('aria-current', 'true');
    else el.removeAttribute('aria-current');
  });
  moveHighlight();
  const url = new URL(location);
  url.searchParams.set('v', i + 1);
  history.replaceState(null, '', url);
  mount(i);
}

items.forEach((el, i) => el.addEventListener('click', () => setActive(i)));
replay?.addEventListener('click', () => mount(current));
window.addEventListener('resize', moveHighlight);

document.addEventListener('keydown', (e) => {
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable) return;
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const num = parseInt(e.key, 10);
  if (num >= 1 && num <= variants.length) setActive(num - 1);
  else if (e.key === 'ArrowRight') setActive((current + 1) % variants.length);
  else if (e.key === 'ArrowLeft') setActive((current - 1 + variants.length) % variants.length);
  else if (e.key === 'r' || e.key === 'R') mount(current);
});

setActive((parseInt(new URLSearchParams(location.search).get('v'), 10) || 1) - 1);
// Kaymayı yalnız ilk paint'ten sonra aç; yükleme animasyonlu olmasın.
requestAnimationFrame(() => requestAnimationFrame(() => picker.setAttribute('data-ready', '')));
```
