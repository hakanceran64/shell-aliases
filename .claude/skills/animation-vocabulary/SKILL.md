---
name: animation-vocabulary
description: Bir web animasyonunun ya da motion efektinin belirsiz tarifini tam terimine çeviren ters sözlük ("popover açılırken olan zıplama şeyi" → Pop in; "iOS'taki lastik gibi kaydırma" → Rubber-banding). Kullanıcı "şuna ne deniyor?" diye sorduğunda ya da bir efekti adını bilmeden tarif edip AI'a/tasarımcıya doğru kelimeyle sormak istediğinde kullan. Efekti adlandırmak içindir; tasarlamak ya da inşa etmek için değil.
when_to_use: "'buna ne deniyor', 'şu efektin adı ne', 'doğru terim ne', '/animation-vocabulary'"
argument-hint: "[efektin tarifi]"
---

# Animasyon sözlüğü

Bir hareket ya da efektin belirsiz tarifini kesin terime çevir; kullanıcı ne isteyeceğini bilsin.

Terimler **İngilizce** kalır — kullanıcının bir AI'a, kütüphane dokümanına ya da tasarımcıya
söyleyeceği kelime odur. Açıklamalar Türkçedir.

## Hızlı başlangıç

Kullanıcı efekti gevşek biçimde tarif eder; sen eşleşen terim(ler)i şu formatta döndürürsün:

```
**Stagger** — Birkaç öğeyi aralarında küçük gecikmelerle art arda animate etmek; bir kaskad etkisi yaratır.
```

Birden çok terim uyuyorsa en iyi eşleşmeyi başa koy, ardından 1–2 alternatifi farklarını tek
satırda belirterek ver.

## Talimatlar

1. **Anahtar kelimeyi değil niyeti oku.** Kullanıcılar teknik adı değil, *gördüklerini* ya da
   *hissettiklerini* tarif eder ("yaylanıyor", "kayıp gidiyor", "kendini çiziyor"). Duyguyu
   sözlükteki terimle eşleştir.
2. **Sözlüğü birebir alıntıla.** Açıklamalar kanoniktir — olduğu gibi kullan, kendi cümlenle
   yeniden yazma.
3. **Yakın terimleri ayrıştır.** İki terim yarışıyorsa (*Clip-path* vs *Mask*, *Pop in* vs
   *Bounce*, *Shared element transition* vs *Layout animation*) kullanıcının seçebilmesi için
   karşılaştır.
4. **Tam eşleşme yoksa** en yakın terimi ver ve bunun bir yaklaşıklık olduğunu açıkça söyle, ya da
   efekti sözlüğün kelimeleriyle tarif et (ör. "bu, *scale-in* girişlerinin *stagger*'ı").
5. **Sözlüğün dışına çıkma.** Bir terim gerçekten burada yoksa uydurmak yerine olmadığını söyle —
   yine de kavramı bu kelimelerle açıklayabilirsin.
6. **Kısa tut.** Adlandırma sorusu bir ad ister, deneme değil. Terimle başla; istenirse genişlet.

## Örnekler

**Örnek 1 — hisse dayalı**
Kullanıcı: "Popover'ın tıkladığın butonun içinden büyüyor gibi görünmesine ne deniyor?"
Çıktı:
```
**Origin-aware animation** — Bir öğe kendi merkezinden (CSS'in öntanımlısı) değil, tetikleyicisinden
büyüyerek animate olur; popover'ın onu açan butondan çıkması gibi.
```

**Örnek 2 — ayrıştırma**
Kullanıcı: "Bir görselin başka bir görsele dönüştüğü şey."
Çıktı:
```
**Morph** — Bir şekil pürüzsüzce başka bir şekle dönüşür, ör. Dynamic Island.

Yakın alternatifler:
- **Crossfade** — aynı yerde sadece birbirinin üzerine fade oluyorlarsa.
- **Shared element transition** — bir öğe bir konumdan diğerine yol alıp dönüşüyorsa.
```

**Örnek 3 — fizik hissi**
Kullanıcı: "iOS'ta fazla çekince direnen ve geri yaylanan kaydırma."
Çıktı:
```
**Rubber-banding** — Sınırın ötesine sürüklediğinde direnç ve geri yaylanma (iOS overscroll hissi).
```

## Sözlük

### Girişler ve çıkışlar — öğeler nasıl belirir ve kaybolur
- **Fade in / Fade out** — Öğe opacity değişerek belirir ya da kaybolur.
- **Slide in** — Öğe ekran dışından kayarak girer (sol, sağ, üst ya da alt).
- **Scale in** — Öğe belirirken küçükten tam boyuta büyür; genelde fade ile birlikte.
- **Pop in** — Öğe hafif bir aşımla, yerine zıplayarak belirir.
- **Reveal** — İçerik kademeli olarak açığa çıkar; genelde clip-path ya da mask animasyonuyla.
- **Enter / Exit** — Bir öğenin ekrana eklendiğinde ya da kaldırıldığında oynattığı animasyon.

### Sıralama ve zamanlama — birden çok öğeyi veya anı eşgüdümlemek
- **Keyframes** — Animasyonda tanımlı noktalar (0%, 50%, 100%); tarayıcı aralarını doldurur.
- **Interpolation / Tween** — Başlangıç ve bitiş değeri arasındaki tüm ara kareleri üretmek.
- **Stagger** — Birkaç öğeyi aralarında küçük gecikmelerle art arda animate etmek; kaskad yaratır.
- **Orchestration** — Birden çok animasyonu tek bir eşgüdümlü hareket gibi hissettirecek şekilde
  bilinçli zamanlamak.
- **Delay** — Animasyon başlamadan önceki süre.
- **Duration** — Animasyonun sürdüğü süre.
- **Fill mode** — Öğenin, animasyon başlamadan önce ya da bittikten sonra ilk/son kare stillerini
  koruyup korumadığı (ör. `forwards`).
- **Stepped animation** — Ayrık adımlara bölünmüş animasyon; geri sayım sayacı gibi.

### Hareket ve transform — konum, boyut ya da açı değiştirmek
- **Translate** — Öğeyi X ya da Y ekseninde taşımak.
- **Scale** — Öğeyi büyütmek ya da küçültmek.
- **Rotate** — Öğeyi bir nokta etrafında döndürmek.
- **Skew** — Öğeyi X ya da Y ekseninde eğerek dikdörtgen biçiminden çıkarmak.
- **3D tilt / Flip** — 3B uzayda döndürme (`rotateX`/`rotateY`) ile derinlik katmak.
- **Perspective** — 3B etkinin gücü — düşük değer derinliği abartır, izleyici daha yakınmış gibi.
- **Transform origin** — Ölçekleme ya da döndürmenin büyüdüğü/döndüğü çapa noktası.
- **Origin-aware animation** — Bir öğe kendi merkezinden (CSS'in öntanımlısı) değil,
  tetikleyicisinden büyüyerek animate olur.

### State'ler arası geçiş — bir durumu, görünümü ya da öğeyi diğerine bağlamak
- **Crossfade** — Bir öğe aynı yerde fade out olurken diğeri fade in olur.
- **Continuity transition** — Öncesi ve sonrasını görsel olarak bağlayarak kullanıcının
  yönünü korumasını sağlayan değişim. Örneğin aynı dikdörtgeni büyütüp küçültmek.
- **Morph** — Bir şekil pürüzsüzce başka bir şekle dönüşür, ör. Dynamic Island.
- **Shared element transition** — Bir öğe bir konumdan diğerine yol alıp dönüşür; küçük görselin
  karta açılması gibi.
- **Layout animation** — Bir öğenin boyutu ya da konumu değiştiğinde zıplamak yerine yeni yerine
  animate olması.
- **Accordion / Collapse** — Bir bölümün içeriği göstermek/gizlemek için yüksekliğini pürüzsüzce
  açıp kapatması.
- **Direction-aware transition** — İçerik ileri giderken bir yöne, geri gelirken tersine kayar;
  böylece gezinmenin bir yön duygusu olur.

### Scroll — kaydırmaya ya da görünümler arası geçişe bağlı hareket
- **Scroll reveal** — Öğeler viewport'a girerken fade ya da slide ile yerine gelir.
- **Scroll-driven animation** — İlerlemesi doğrudan scroll konumuna bağlı animasyon.
- **Parallax** — Kaydırırken arka plan ve ön plan farklı hızlarda hareket ederek derinlik yaratır.
- **Page transition** — Bir sayfadan/route'tan diğerine geçerken oynayan animasyon.
- **View transition** — Tarayıcının iki state ya da sayfa arasında morph yaparak ortak öğeleri
  bağlaması.

### Feedback ve etkileşim — kullanıcının aksiyonuna yanıt vermek
- **Hover effect** — İmleç öğenin üzerine geldiğinde oluşan görsel değişim.
- **Press / Tap feedback** — Tıklandığında hafif küçülme; fiziksel hissettirir.
- **Hold to confirm** — Kullanıcı butonu basılı tutarken dolan ilerleme efekti.
- **Drag** — Öğeyi tutup taşımak; bırakıldığında genelde momentumla.
- **Drag to reorder** — Listedeki öğeleri sürükleyerek yeniden sıralamak; diğerleri yer açar.
- **Swipe to dismiss** — Öğeyi ekran dışına sürükleyerek kapatmak; drawer ya da toast gibi.
- **Rubber-banding** — Sınırın ötesine sürüklediğinde direnç ve geri yaylanma (iOS overscroll hissi).
- **Shake / Wiggle** — Hatayı ya da reddedilen girdiyi bildiren hızlı sağa-sola titreme.
- **Ripple** — Dokunma noktasından yayılan daire; basışı doğrular.

### Easing — hızın animasyon boyunca nasıl değiştiği
- **Easing** — Animasyonun hızlanma/yavaşlama oranı.
- **Ease-out** — Hızlı başlar, yavaş biter. Çoğu UI'ın ve kullanıcıya yanıt veren her şeyin
  öntanımlısı.
- **Ease-in** — Yavaş başlar, hızlı biter. Genelde kaçınılır; ağır hissettirebilir.
- **Ease-in-out** — Yavaş, hızlı, yavaş. Ekranda zaten olan bir öğe A'dan B'ye giderken iyidir.
- **Linear** — Sabit hız. UI'da kaçın; spinner ve marquee'ye sakla.
- **Cubic-bezier** — Hassas kontrol için kendin tanımladığın custom easing eğrisi.
- **Asymmetric easing** — Farklı oranlarda hızlanıp yavaşlayan eğri. Simetrik olandan daha canlı
  hissettirir.

### Spring animasyonları — sabit süreli easing'e fizik tabanlı alternatif
- **Spring** — Sabit süre yerine fizikle (tension, mass, damping) sürülen hareket.
- **Stiffness / Tension** — Yayın hedefe ne kadar güçlü çektiği. Yüksek = daha çevik.
- **Damping** — Yayın ne kadar hızlı yerleştiği. Düşük damping = daha çok zıplama ve salınım.
- **Mass** — Animate edilen öğenin ne kadar ağır hissettiği. Daha çok kütle = daha yavaş.
- **Bounce** — Hedefi aşıp yerleşen yay; oyunculuk katar.
- **Perceptual duration** — Altta mikro-yerleşme sürerken bile yayın bitmiş *hissettiği* süre.
- **Momentum** — Özellikle drag ya da kesilme sonrası hızı taşıyan hareket.
- **Velocity** — Bir öğenin ne kadar hızlı ve hangi yönde hareket ettiği. Kesildiğinde yay bunu bir
  sonraki animasyona taşır; fiskelenen öğe hızını korur.
- **Interruptible animation** — Bitmesini beklemeden, uçarken pürüzsüzce yeniden yönlendirilebilen
  animasyon.

### Döngü ve ortam hareketi — kendi başına çalışan animasyonlar
- **Marquee** — Sürekli döngüde kayan metin ya da içerik.
- **Loop** — Belirli sayıda ya da sonsuz tekrarlanan animasyon.
- **Alternate (yoyo)** — Her turda başa dönmek yerine ileri oynayıp geri saran döngü.
- **Orbit** — Bir öğenin diğerinin etrafında sürekli dönmesi.
- **Pulse** — Dikkat çekmek için hafif tekrarlayan ölçek ya da opacity değişimi.
- **Float** — Statik bir öğeyi canlı ve ağırlıksız hissettiren hafif, sürekli aşağı-yukarı süzülme.
- **Idle animation** — Bir öğe etkileşim beklerken oynayan ince hareket.

### Cila ve efektler — iyiyi harikadan ayıran küçük dokunuşlar
- **Blur** — Bir öğeyi yumuşatmak ya da küçük kusurları maskelemek için kullanılan blur filtresi.
- **Clip-path** — Öğeyi bir şekle kırpmak; reveal, mask ve öncesi/sonrası slider'larında kullanılır.
- **Mask** — Bir şekil ya da gradyanla öğenin bölümlerini gizlemek/göstermek — clip-path gibi ama
  yumuşak, fade edilebilir kenarlarla.
- **Before / after slider** — İki bindirilmiş görseli karşılaştırmak için sürüklenebilir ayraç.
- **Line drawing** — Bir SVG path'in görünmez bir kalem çiziyormuş gibi kendini çizmesi.
- **Text morph** — Metin değiştiğinde karakter karakter animate olarak yeni değere dikkat çekmesi.
- **Skeleton / Shimmer** — İçerik yüklenirken gösterilen, üzerinden parıltı geçen yer tutucu.
- **Number ticker** — Bir değere doğru yuvarlanan ya da sayan rakamlar.
- **Tabular numbers** — Sabit genişlikli rakamlar; sayılar değişirken kaymazlar. Ticker, sayaç ve
  kronometrelerde şart.
- **Typewriter** — Metnin yazılıyormuş gibi karakter karakter belirmesi.

### Performans — hareketi takılmak yerine pürüzsüz kılan şeyler
- **Frame rate (FPS)** — Saniyede çizilen kare. Pürüzsüz hareket için taban 60fps; yeni ekranlarda
  120fps.
- **Jank** — Tarayıcı animasyona yetişemeyip kare düşürdüğünde görülen takılma.
- **Dropped frame** — Tarayıcının çizme süresini kaçırdığı kare; harekette küçük bir tökezleme.
- **Compositing** — GPU'nun öğeyi kendi katmanında, layout ve paint'i yenilemeden taşıması/fade
  etmesi.
- **will-change** — Bir öğenin animate edeceğini önceden bildiren CSS ipucu; tarayıcı onu kendi
  katmanına yükseltebilir.
- **Layout thrashing** — `width`, `height`, `top`, `left` gibi property'leri animate ederek
  tarayıcıyı her karede layout hesaplamaya zorlamak; jank yaratır.

### Bilinmesi gereken ilkeler — ne zaman ve nasıl animate edileceğini yönlendiren kavramlar
- **Purposeful animation** — Hareket bir işlev görmeli — yön vermek, feedback vermek, ilişki
  göstermek — sadece süslemek değil.
- **Anticipation** — Bir hareketten önce ters yönde küçük bir hazırlık; ne olacağını ima eder.
- **Follow-through** — Ana hareket durduktan sonra bazı parçaların bir süre daha devam edip
  yerleşmesi; ağırlık katar.
- **Squash & stretch** — Hareket ederken öğeyi deforme ederek ağırlık, hız ve esneklik aktarmak.
- **Perceived performance** — Doğru animasyon, arayüzü gerçekte olmadığı hâlde daha hızlı
  hissettirir.
- **Frequency of use** — Kullanıcı bir animasyonu ne kadar sık görüyorsa o kadar kısa ve ince
  olmalı.
- **Spatial consistency** — Öğenin state'ler arasında kimliğini ve konumunu koruyacak şekilde
  animate edilmesi; kullanıcı hiçbir şeyin nereye gittiğini kaybetmez.
- **Hardware acceleration** — `transform` ve `opacity` animate etmek GPU'nun hareketi pürüzsüz
  tutmasını sağlar.
- **Reduced motion** — Kullanıcının `prefers-reduced-motion` ayarına saygı göstererek hareketi
  azaltmak ya da kaldırmak.

---
> Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, Emil Kowalski) —
> ekosisteme uyarlandı. Uyarlama notları: `claude-foundation/docs/UPSTREAM-SKILLS.md`.
