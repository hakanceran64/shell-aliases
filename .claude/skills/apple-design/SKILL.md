---
name: apple-design
description: Apple'ın arayüz tasarımı ve akışkan, fiziksel hareket yaklaşımının web'e çevrilmiş hâli. Jest güdümlü UI, spring animasyonları, drag/swipe/sheet etkileşimleri, momentum ve kesilebilir geçişler, yarı saydam materyaller ve derinlik, tipografi (optical sizing, tracking, leading), reduced-motion ya da Apple tarzı arayüzlerin arkasındaki tasarım temelleri (feedback, uzamsal tutarlılık, kendini tutma) üzerinde çalışırken kullan.
when_to_use: "'iOS gibi hissetsin', 'spring ayarları', 'sheet/drawer jesti', 'glass/blur yüzey', 'Apple tarzı', '/apple-design'"
---

# Apple design

Apple'ın arayüzleri nasıl "bilgisayar gibi" olmaktan çıkarıp kullanıcının uzantısı hâline
getirdiği. Kaynak: Apple'ın WWDC tasarım oturumları — başta *Designing Fluid Interfaces*
(WWDC 2018) — damıtılıp web platformuna (CSS, Pointer Events, `requestAnimationFrame`, Motion /
Framer Motion gibi spring kütüphaneleri) çevrildi.

Ana fikir: **bir arayüz, hareket ekrandaki mevcut değerden başladığında, kullanıcının hızını
devraldığında, momentumu ileri yansıttığında ve her an yakalanıp tersine çevrilebildiğinde canlı
hisseder.** Spring'ler bunu doğal kılan araçtır, çünkü doğaları gereği kesilebilir ve hız
farkındadırlar.

## Çekirdek fikir

Bir arayüz, fiziksel dünya gibi davrandığında akışkandır: anında yanıt verir, sürekli hareket eder,
momentum taşır, sınırlarda direnir ve hareket ortasında yönlendirilebilir.

Apple tasarımı dört insani ihtiyaca hizmet olarak çerçeveler: **güvenlik/öngörülebilirlik, anlama,
başarma ve keyif.** Aşağıdaki her kural bunlardan birine hizmet eder.

## 1. Yanıt — gecikmeyi öldür

Gecikme belirdiği an doğrudanlık hissi uçurumdan düşer. Yanıt, her şeyin üzerine kurulduğu temeldir.

- **Pointer-down'da yanıt ver, bırakışta değil.** Butonu basıldığı anda vurgula. Feedback için
  `click`/touch-up beklemek ölü hissettirir.
- **Her gecikmeye karşı tetikte ol.** Debounce'ları, yapay zamanlayıcıları, geçiş beklemelerini ve
  ~300ms tap gecikmesini denetle. Girdi yolundaki zorunlu olmayan her şey regresyondur.
- **Feedback etkileşim *sırasında* sürekli olmalı**, yalnız sonunda değil. Drag, slider ya da
  drawer'da UI'ı pointer ile 1:1 güncelle — jest tamamlandığında animate etmekle yetinme.

```css
/* Feedback basışta yaşar ve anındadır */
.button:active {
  transform: scale(0.97);
  transition: transform 100ms ease-out;
}
```

## 2. Doğrudan manipülasyon — 1:1 takip

Kullanıcı bir şeyi sürüklediğinde parmağa yapışık kalmalı — ve **nereden tuttuğunun** ofsetine
saygı göstermeli. Tutuşta öğenin merkezine sıçramak illüzyonu anında bozar.

- Pointer Events + `setPointerCapture` kullan; imleç öğenin sınırlarından çıksa da takip sürer.
- Yalnız güncel noktayı değil, kısa bir **hız/konum geçmişi** tut (son birkaç `pointermove`) —
  bırakışta hıza ihtiyacın olacak.

```js
el.addEventListener('pointerdown', (e) => {
  el.setPointerCapture(e.pointerId);
  const grabOffset = e.clientY - el.getBoundingClientRect().top; // nereden tuttuğuna saygı göster
  // ...hız için konum + zaman damgası geçmişini tut
});
```

## 3. Kesilebilirlik — en önemli tek ilke

Her animasyon her an kesilebilir ve yeniden yönlendirilebilir olmalı. Kullanıcı uçan bir öğeyi
yakalayıp animasyonun bitmesini beklemeden tersine çevirebilmeli. Kapanan bir modal'ı yeniden
yakalarsa parmağı takip etmeli — önce kapanmayı bitirip sonra yeniden açılmamalı.

- **Geçiş sırasında girdiyi asla kilitleme.**
- **Her zaman *presentation* (mevcut) değerden animate et, hedef değerden değil.** Kesilme anında
  öğenin canlı ekran transform'unu oku ve yeni animasyonu oradan başlat. Mantıksal/hedef değerden
  başlamak görünür bir sıçrama yaratır.
- **Jest güdümlü hiçbir şeyde CSS transition ve `@keyframes` kullanma** — uçarken pürüzsüzce
  yakalanıp tersine çevrilemezler. Spring'ler öntanımlı olarak mevcut değerden animate eder.
- **Jest tersine döndüğünde hızı harmanla, sert kesme.** Dönüşte bir animasyonu diğeriyle
  değiştirmek hız süreksizliği — bir "tuğla duvar" — yaratır. Yeniden hedeflemede mevcut hızı
  taşıyan bir spring kütüphanesi seç. (iOS'ta bunu *additive animations* yapar.)
- **2B hareketi bağımsız X ve Y spring'lerine ayır.** 2B mesafe üzerindeki tek bir spring, X ve Y
  farklı hızlara sahip olduğunda senkronu kaybeder.

## 4. Animasyon değil davranış — spring kullan

Önceden yazılmış, sabit süreli bir animasyon yeni girdiye yanıt veremez. Spring verebilir — yeni
girdi yalnız hedefi değiştirir, hareket sürekli kalır. Kullanıcının dokunabildiği her şeyde
spring'e uzan.

Apple, fizik üçlüsünü (mass/stiffness/damping) bilinçli olarak tasarımcı dostu iki parametreyle
değiştirdi:

- **Damping ratio** — aşımı kontrol eder. `1.0` = kritik sönümlü, zıplama yok, pürüzsüz yerleşme.
  `< 1.0` = aşar ve salınır. Düşük = daha zıplak.
- **Response** — değerin hedefe ne kadar hızlı ulaştığı, saniye cinsinden. Düşük = daha çevik.
  **Bu "duration" değildir** — spring'in sabit süresi yoktur; yerleşme süresi parametrelerden doğar.

**Öntanımlılar:**
- Çoğu UI'ı **damping `1.0`** (kritik sönümlü) ile başlat — zarif ve dikkat dağıtmayan.
- Zıplamayı (**damping ~`0.8`**) **yalnız jestin kendisi momentum taşıdıysa** ekle (fiske, fırlatma,
  drag bırakışı). Yeni fade in olmuş bir menüde aşım yanlış hissettirir; fiskelediğin bir kartta
  doğru hissettirir.

**Apple'ın kullandığı somut değerler:**

| Etkileşim | Damping | Response |
| --- | --- | --- |
| Taşıma / yeniden konumlandırma (ör. PiP) | `1.0` | `0.4` |
| Döndürme | `0.8` | `0.4` |
| Drawer / sheet | `0.8` | `0.3` |

**Web karşılığı (Motion / Framer Motion):** `bounce` + `duration` spring API'si Apple'ın
damping + response'una yakın eşlenir. Güvenli bir ev stili: her yerde `damping: 1.0`; bounce'ı
momentum güdümlü, fiziksel etkileşimlere sakla.

```js
import { animate } from 'motion';

// Kritik sönümlü öntanımlı (aşım yok)
animate(el, { y: 0 }, { type: 'spring', bounce: 0, duration: 0.4 });

// Momentum etkileşimi — biraz zıplama, yalnız öncesinde bir fiske olduğu için
animate(el, { y: target }, { type: 'spring', bounce: 0.2, duration: 0.4 });
```

## 5. Hız devri — drag ile animasyon arasındaki dikiş

Jest bittiğinde animasyon **parmağın tam hızıyla devam etmeli**; sürükleme ile animasyon arasında
görünür bir dikiş olmamalı. "Akışkan"ı "iyi"den ayıran detay budur.

Pointer'ın bırakış hızını spring'in başlangıç hızı olarak geçir. Bazı spring API'leri **göreli**
hız ister — hedefe kalan mesafeye böl:

```
relativeVelocity = gestureVelocity / (targetValue − currentValue)
```

Örnek: öğe `y=50`, hedef `y=150` (100px kaldı), parmak 50px/s → başlangıç spring hızı
`50 / 100 = 0.5`. Motion / Framer Motion mutlak px/s hızı doğrudan alır (`velocity` seçeneği),
yani genelde ham değeri verirsin.

## 6. Momentum projeksiyonu — jestin *gittiği* yere animate et

Bırakma noktasından en yakın sınıra yapışma. Hızı kullanarak **yerleşme konumunu projekte et** —
tıpkı scroll yavaşlaması gibi — sonra o projeksiyona en yakın hedefe yapış. Bir fiskeyi "fırlatma"
gibi hissettiren şey budur.

Apple'ın *Designing Fluid Interfaces* örnek kodundaki projeksiyon fonksiyonu:

```js
// decelerationRate ≈ 0.998 normal scroll hissi için; 0.99 daha çevik
function project(initialVelocity /* px/s */, decelerationRate = 0.998) {
  return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
}

const projectedEndpoint = currentPosition + project(releaseVelocity);
const target = nearestSnapPoint(projectedEndpoint);    // hedefi projeksiyondan seç
animateSpringTo(target, { velocity: releaseVelocity }); // sonra hızı devret (§5)
```

Not: fizik kitaplarındaki `v²/(2·decel)` Apple'ın kullandığı **değildir** — yukarıdaki üstel
sönümleme formunu kullan. İyi bottom-sheet ve carousel'lerin (Vaul, Embla) standart davranışı budur.

## 7. Uzamsal tutarlılık — simetrik yollar, çapalanmış origin'ler

- **Girdiği yoldan çık.** Sağdan kayarak giren panel sağa doğru kapanmalı. Sağdan girip alttan
  çıkmak kopuk ve kafa karıştırıcı hissettirir.
- **Etkileşimleri kaynağına çapalayın.** Menü, popover ya da sheet onu tetikleyen öğeden
  doğmalı — `transform-origin`'i tetikleyiciye ayarla.
- **Tersine çevrilebilir geçişlerde easing'i aynala** ki gidiş yolu dönüş yoluyla eşleşsin (iki yön
  için ters cubic-bezier kontrol noktaları).

## 8. Jestin yönünde ipucu ver

İnsanlar bir yörüngeden son durumu tahmin eder. Ara hareket nereye gidildiğini haber vermeli —
Control Center modülleri "parmağına doğru büyür ve dışa açılır". Ara kareler sonucu körlemesine
interpole etmesin, ona işaret etsin.

## 9. Rubber-banding — yumuşak sınırlar

Kenarda sert durmak yerine kademeli olarak diren. Sert duruş "donmuş" okunur; sürekli direnç
"duyarlı, ama burada başka bir şey yok" okunur. Kullanıcı sınırın ötesine ne kadar sürüklerse
sönümlemeyi o kadar artır.

```js
// Sınırın ötesine gidildikçe öğe daha az takip eder — gerçek şeyler durmadan önce yavaşlar
function rubberband(overshoot, dimension, constant = 0.55) {
  return (overshoot * dimension * constant) / (dimension + constant * Math.abs(overshoot));
}
```

## 10. Jest tasarım detayları (his kontrol listesi)

- **Tap:** touch-*down*'da vurgula (anında), touch-*up*'ta işle. Hedef çevresine ~10px histerezis /
  dokunma payı ekle; sürükleyip uzaklaşarak iptal edip geri gelmeye izin ver.
- **Drag/swipe:** bir yöne bağlanmadan önce küçük bir hareket eşiği (~10px histerezis) iste, sonra
  1:1 takip et.
- **Olası tüm jestleri ilk hareketten itibaren paralel algıla**, niyet netleşince kaybedenleri
  kararlılıkla iptal et. Yalnız *son* durumu bildiren recognizer'lardan (`swipeleft` türü olaylar)
  kaçın — feedback için gereken sürekli takibi çöpe atarlar.
- **Ayrıştırma gecikmelerini en aza indir.** Çift dokunma algılama tek dokunmayı kaçınılmaz olarak
  geciktirir; bu bedeli yalnız çift dokunmanın gerçekten var olduğu yerde öde.

## 11. Kare düzeyinde pürüzsüzlük

Pürüzsüzlük yalnız kare hızıyla değil, karelerin *içindekiyle* ilgilidir.

- Kare başına konum değişimini algı eşiğinin altında tut; yoksa stroboskopik görünür.
- Çok hızlı hareket için ince bir **motion blur / esneme** hızı kodlar ve keskin bir çizgiden daha
  iyi okunur.
- `requestAnimationFrame` web'in ekran senkronlu saatidir (Apple'da `CADisplayLink`). Yalnız
  compositor dostu property'leri — `transform` ve `opacity` — animate et; hareket yaklaşırken
  `will-change` ile ipucu ver.

## 12. Materyaller ve derinlik — saydamlık hiyerarşi taşır

Apple yarı saydam materyalleri, yapı getirirken odağı çalmayan yüzen bir işlevsel katman olarak
kullanır. Web'de `backdrop-filter` ile yaklaş.

- **Nav/toolbar/sheet'leri yarı saydam katman olarak kur** (`backdrop-filter: blur()` + yarı
  saydam arka plan), içerik altından aksın — sabit bir şerit tüketen opak çubuklar değil.
- **Materyal ağırlığı hiyerarşi kodlar:** koyu/ağır materyaller yapısal bölgeleri ayırır (sidebar);
  hafif materyaller etkileşimli öğelere dikkat çeker. **Hafif yarı saydam bir yüzeyi diğerinin
  üstüne asla yığma** — okunabilirlik çöker.
- **Büyük yüzeyler daha kalın okunmalı:** küçük çiplerden daha güçlü blur ve daha derin gölge.
  Bağlam duyarlı gölge düşün — yoğun/metinli içerik üzerinde daha ağır, düz arka planda daha hafif.
- **Odaklamak için karart, akışı korumak için ayır.** Modal bir görev, yüzeyi karartma perdesiyle
  eşler ve arka planı geri/aşağı iter. Paralel, engellemeyen bir panel perdesiz saydamlık ve ofset
  kullanır. Yığılmış sheet'lerde her üst katmanı kademeli karart ve geri it.
- **Vibrancy metni değişen arka planlarda okunur tutar.** Blur'lu/yarı saydam yüzeylerde düz gri
  metin kullanma — daha yüksek kontrast, biraz daha kalın ağırlık ve küçük bir letter-spacing artışı
  kullan. Rengi yarı saydam ön plana değil, opak bir katmana koy.
- **Sert ayraç değil scroll kenar efekti.** Sticky header altına 1px kenarlık koymak yerine,
  içeriğin yüzen kroma değdiği yerde küçük bir blur/gradyan maskesi soldur.
- **Sadece fade değil, materyalleş.** Cam/blur yüzeylerde giriş/çıkışta blur yarıçapı ile ölçeği
  birlikte animate et; yüzey düz bir opacity fade'i yerine gerçekten gelen bir materyal gibi okunsun.

```css
.toolbar {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  border-top: 1px solid rgba(255, 255, 255, 0.4); /* parlak üst kenar = materyale çarpan ışık */
}
```

## 13. Çok modlu feedback — hareket + ses + haptik

Duyuları birleştirmenin üç kuralı (*Designing Audio-Haptic Experiences*):

1. **Nedensellik** — feedback'e neyin sebep olduğu apaçık olmalı. Gerçek nedensel olayda tetikle
   (toggle'ın dönmesi, öğenin yerine oturması) ve karakterini aksiyonun fizikselliğiyle eşle.
2. **Uyum** — görsel, ses ve haptik **aynı karede** tetiklenmeli. Aralarındaki gecikme illüzyonu
   yok eder. Bir CSS geçişinin sesi/haptiği (Vibration API) geciktirmesine izin verme.
3. **Fayda** — feedback'i yalnız yerini hak ettiği yere ekle. Haptik/sesi anlamlı anlara sakla
   (başarı, hata, işleme, yerine oturma). Aşırı feedback kullanıcıya hepsini görmezden gelmeyi
   öğretir.

## 14. Reduced motion ve erişilebilirlik

Reduced motion *hiç* feedback yok demek değildir — daha yumuşak, vestibüler olmayan bir karşılık
demektir. Üç bağımsız sinyale yanıt ver ve bunları bileşenlerine göm:

- **`prefers-reduced-motion: reduce`** — slide/spring/parallax yerine kısa opacity **crossfade**
  veya statik geçiş. Elastik/aşım hareketlerini kaldır. Anlamayı kolaylaştıran opacity/renk
  değişimlerini koru.
- **`prefers-reduced-transparency: reduce`** — yarı saydam yüzeyleri buzlandır/opaklaştır: arka
  plan opaklığını yükselt, blur'u kaldır.
- **`prefers-contrast: more`** — neredeyse opak arka planlar ve tanımlı, kontrastlı bir kenarlık.

Ayrıca: viewport'u kaplayan hareketli arka planlardan, yavaş döngüsel salınımlardan (0.2 Hz
civarı / 5 saniyede bir tur) ve ani parlaklık sıçramalarından kaçın (koyu↔açık tema geçişini ease
et). Büyük hareketli nesneleri yol alırken yarı saydam yap; büyük yüzeyleri büyük bir yeniden
konumlandırma sırasında soldurup yerleştiğinde geri getir.

```css
@media (prefers-reduced-motion: reduce) {
  .sheet { transition: opacity 200ms ease; transform: none !important; }
}
@media (prefers-reduced-transparency: reduce) {
  .toolbar { background: white; backdrop-filter: none; }
}
```

## 15. Tipografi — optical sizing, tracking, leading

Apple tipografiyi boyutla birlikte şekil değiştirecek şekilde tasarlar; aynı disiplin web'de de
geçerli. (*The Details of UI Typography*, WWDC 2020.)

- **Tracking (letter-spacing) boyuta özeldir — asla tüm boyutlara tek değer verme.** Büyük display
  metni *negatif* tracking ister (büyüdükçe harfler fazla ayrık okunur); küçük metin okunabilirlik
  için hafif *pozitif* ister. Sabit bir `letter-spacing` bir yerde mutlaka yanlıştır. Başlıkları
  sıkılaştır, gövdeyi `0`'a yakın bırak.
- **Leading (line-height) boyutla ters orantılı.** Büyük başlıklarda sıkı, gövde metninde daha
  gevşek. Uzun çıkıntılı yazı sistemlerinde artır; yoğun, bilgi ağırlıklı UI'da sıkılaştır.
- **Hiyerarşiyi weight + size + leading'i bir küme olarak kurarak yap,** yalnız boyutla değil.
  Vurguyu ağırlıkla yap — daha fazla yer kaplamadan varlık katar.
- **Kullanıcının metin boyutu ayarına saygı göster** (Dynamic Type). Layout'u metinle *birlikte*
  ölçekle — boşluklar `rem`/`em`, sabit px değil.
- **Custom font'tan önce platformun sistem font'unu öntanımlı al**; optical sizing, tracking
  tabloları ve okunabilirlik ayarları zaten içindedir. Gerekçesiz override etme.

```css
:root { font: 100%/1.5 system-ui, sans-serif; } /* gövde: sistem font'u, rahat leading */

.display {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.05;        /* büyük metinde sıkı leading */
  letter-spacing: -0.02em;  /* büyüdükçe negatif tracking */
  font-optical-sizing: auto;
}
```

## 16. Tasarım temelleri — sekiz ilke

Yukarıdaki hareket ve craft, Apple'ın sekiz tasarım ilkesine hizmet eder (*Principles of Great
Design*, WWDC 2026). Bunları akıl yürütürken kullandığın adlar olarak al:

1. **Purpose (amaç).** Niyetle üret; neyi *inşa etmeyeceğine* karar ver. Her özellik kullanıcının
   zamanını, dikkatini ve güvenini ister — bu bütçeyi yalnız karşılığını verdiği yerde harca.
2. **Agency (kontrol).** İnsanları kontrolde tut: seçenek sun, tek bir yolu dayatma. Bunu
   bağışlayıcılıkla destekle — kaymalar için kolay geri alma, onay diyaloğu yalnız gerçekten yıkıcı
   ve geri alınamaz aksiyonlarda (az kullan; aşırısı insanlara tıklayıp geçmeyi öğretir).
3. **Responsibility (sorumluluk).** Kullanıcının çıkarına davran. Gizlilik: doğru anda, yalnız
   gerekeni, şeffafça iste. Güvenlik: kötüye kullanımı ve zararı öngör — özellikle AI'da (alerji
   farkındalıklı bir tarif uygulaması zararlı bir malzeme önermemeli). Önizleme, onay ve uyarı ekle;
   riski değerinden büyük olan bir özelliği kes.
4. **Familiarity (aşinalık).** İnsanların zaten bildiğinin üzerine kur. Ne fazla birebir ne fazla
   soyut metaforlar kullan (çöp kutusu = sil) ve fiziğine saygı göster. Tutarlı ol: aynı görünen
   şeyler aynı davranmalı ve aynı yerde olmalı ki insanlar ne olacağını tahmin edebilsin. Tanıdık
   bir kalıbı ancak daha iyi olduğunu kanıtlayabiliyorsan boz — sonra da varsayma, test et.
5. **Flexibility (esneklik).** Farklı bağlamlar, cihazlar ve yeteneklerin tüm yelpazesi için
   tasarla. Platforma (iPhone = hızlı dokunma; masaüstü = hassas imleçle derin iş akışları) ve
   duruma uyum sağla. Kapsayıcı tasarla (yaş, dil, uzmanlık, erişilebilirlik). Tek bir layout herkese
   uymuyorsa kişiselleştirmeye izin ver.
6. **Simplicity — minimalizm değil.** Gereksizi ayıkla ki ana amaç parlasın; her şeyi tek bir yere
   gömmek minimal görünür ama basit değildir. Özlü (sade dil, jargonsuz, daha az adım) ve net
   (hiyerarşi — sıra, boşluk, kontrast — ile en önemli şey en bariz olsun) ol. Her öğe yerini hak
   etmeli; bazen bağlam *eklemek* basitleştirir. Yaygın yolu önce göster, ileri seçenekleri bir
   seviye altta tut.
7. **Craft (işçilik).** Ödün vermeyen detay dikkati güven inşa eder. Güzel tipografi, açık/koyuya
   uyum sağlayan renkler, net ikonografi ve anında, doğal feedback veren duyarlı animasyonlar.
   Hiçbir şey rastgele değildir — her boşluk, zamanlama ve hizalama değeri savunabileceğin bilinçli
   bir seçimdir. Titrek scroll, hizasız ikonlar ve döndürmede bozulan layout'lar özensizlik okunur.
8. **Delight (keyif).** Diğer yedisini doğru yapmanın sonucudur, üstüne serpilen konfeti değil.
   İnsanların hissetmesini istediğin duyguyu (sakinlik, güven, heyecan) belirle ve her kararda
   pekiştir.

Bunlara hizmet eden taktik kurallar:

- **Feedback dört türlüdür:** durum, tamamlanma, uyarı, hata. Anlamlı aksiyonları onayla, süregelen
  durumu göster, sorunlardan önce uyar, satır içinde doğrula (submit'te değil).
- **Yön bulma.** Her ekran şunları yanıtlamalı: Neredeyim? Nereye gidebilirim? Orada ne var? Nasıl
  çıkarım? Kullanıcıyı asla kapana kıstırma.
- **Gruplama ve eşleme.** Yakınlık ilişki ima eder; kontrolü etkilediği şeyin yanına koy ve
  kontrolleri değiştirdikleri şeyi yansıtacak biçimde diz. Bir kontrolü açıklamak için etikete
  ihtiyacın varsa eşleme zayıftır.
- **Doğrudan, spesifik etiketler güvenli genel olanları yener.** Gezinme öğelerini içeriklerine göre
  adlandır ("İlerleme", "Kitaplık"), belirsiz şemsiyelere göre değil ("Ana Sayfa").

## 17. Süreç

- **Etkileşimli prototip yap — etkileşimli bir demo "bir milyon statik tasarıma" bedeldir.** Arayüzü
  inşa edip onunla oynayarak keşfedersin; çalışan bir prototip aynı zamanda vasat bir nihai
  implementasyonu engelleyen somut bir çıta koyar. (Bu ekosistemde: `/ui-prototype`.)
- **Etkileşim ve görseli birlikte tasarla.** "Birinin nerede bitip diğerinin nerede başladığını
  ayırt edememelisin." Motion, piksellerden sonra eklenen bir katman değildir.
- **Gerçek bağlamda gerçek insanlarla test et** ve motion'ı taze gözle gözden geçir — tam hızda
  görünmeyeni yakalamak için ağır çekimde / kare kare oynat.

## Hızlı referans

| İhtiyaç | Teknik | Somut değer |
| --- | --- | --- |
| Öntanımlı UI spring'i | Kritik sönümlü, aşımsız | `damping 1.0`, `response 0.3–0.4` |
| Momentum / fiske spring'i | Az sönümlü, hafif zıplama | `damping ~0.8`, `response 0.3–0.4` |
| Jest → spring hızı | Bırakış hızını devret | normalize ise `gestureVelocity / (target − current)` |
| Fiske iniş noktası | Momentumu projekte et | `current + (v/1000)·d/(1−d)`, `d ≈ 0.998` |
| Temiz kesilme | Presentation (canlı) değerden başla | ekrandaki transform'u oku |
| Dönüşte "tuğla duvar"ı önle | Yeniden hedeflemede hızı taşı | hızı harmanlayan spring |
| Tersine çevrilebilir geçiş | Easing eğrisini aynala | ters cubic-bezier |
| Geri dönüş mü, işleme mi | Konumu değil hız **işaretini** kullan | bırakış anında |
| 1:1 drag | Pointer Events + capture | tutuş ofsetine saygı göster |
| Feedback | Pointer-down'da, sürekli | asla yalnız sonda değil |
| Sınır | Sert durma, rubber-band | kademeli direnç |
| Yarı saydam krom | `backdrop-filter` katmanı | içerik altından aksın |
| Type tracking | Boyuta özel, asla sabit | büyük metni sıkılaştır (`-0.02em`), gövde `0`'a yakın |
| Reduced motion | Slide/spring değil crossfade | `@media (prefers-reduced-motion)` |

---
> Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, Emil Kowalski) —
> ekosisteme uyarlandı. Uyarlama notları: `claude-foundation/docs/UPSTREAM-SKILLS.md`.
