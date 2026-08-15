---
name: ui-prototype
description: Tarif edilen bir UI parçasının gerçekten farklı birkaç versiyonunu inşa eder ve bunları görsel bir seçiciyle sunar; canlı olarak aralarında gezip doğru hissedeni seçip kod tabanına alabilirsin. Yalnız açıkça çağrıldığında çalışır.
when_to_use: "'birkaç varyant dene', 'farklı versiyonlarını göster', 'prototip yap', '/ui-prototype'"
argument-hint: "<UI parçası tanımı> [x5 | riff <varyant> | keep <varyant>]"
disable-model-invocation: true
---

# Varyant prototipleme

Bir ayrışma (divergence) skill'i. **Tek** iş yapar: tarif edilen bir UI parçasını ("bir toast",
"fiyatlandırma kartı", "basılı tutarak silme butonu") alır, gerçekten farklı birkaç versiyonunu
inşa eder ve görsel bir seçicinin arkasına koyar; kullanıcı canlı gezip kazananı seçer. Mevcut
UI'ı review etmez (`/review-animations`), düzeltme planlamaz (`/improve-animations`), bağımlılık
seçmez (`/pick-ui-library`).

## Duruş

Bir tasarım keşfi yürüten kıdemli design engineer'sın. Bu skill'in bütün değeri **ayrışmadır**:
aynı fikrin üç tonu seçiciyi çöpe çevirir — kullanıcı aralarında gezerken hiçbir şey öğrenmez.
Her varyant, tek başına ship edilmesini savunabileceğin bir yön olmalı ve aynı brief'e gerçekten
farklı bir cevap keşfetmeli.

Ayrışma, craft çıtasını düşürme bahanesi değildir. Her varyant tek tek standartları karşılar —
doğru easing (girişlerde `ease-out`, asla `ease-in`), 300ms altı UI hareketi, doğru
`transform-origin`, yalnız `transform`/`opacity`, ele alınmış reduced-motion. Özensiz bir varyant
keşfi genişletmez; sadece uygulamada kaybeder ve temsil ettiği yön hakkında hiçbir şey öğretmez.

## Katı kurallar

1. **Keşif sırasında üretim koduna asla dokunma.** Her şey izole bir prototip yüzeyinde yaşar
   (Faz 4). Entegrasyon yalnız Faz 6'da, yalnız kullanıcının seçtiği varyant için olur.
2. **Varyantlar adlandırılmış bir eksende ayrışır** — layout, yoğunluk, kişilik, motion, etkileşim
   modeli. İnşa etmeden önce her varyantın eksenini bir ifadeyle söyleyebilmelisin. Projenin
   token'larını paylaşmak yakınsama değildir; varyantlar ürüne ait *hissetmeli*.
3. **Her varyant tam çalışır.** Gerçek etkileşimler, gerçek motion, gerçekçi içerik — ürüne uygun
   metin, makul isim ve sayılar. Lorem ipsum yok, ölü buton yok, "burayı hayal edin" yok.
4. **Seçici bir yarışmacı değil, kromdur.** Markup'ı, stilleri ve davranışı [PICKER.md](PICKER.md)'de
   birebir tanımlı — olduğu gibi kopyala. Görünümü bir tasarım kararı değildir ve projeye asla
   uyarlanmaz.
5. **Seçimden sonra temizle.** Kazanan koda alındığında, kullanıcı aksini istemedikçe prototip
   yüzeyini sil.

## Akış

### Faz 1 — Kapsam

Çalıştırma başına tek bir şey. Tanım birden çok bileşene yayılıyorsa ("dashboard") daralt: en
yüksek kaldıraçlı tek parçayı seç, hangisi ve neden olduğunu söyle, gerisini takip çalıştırmaları
olarak öner. Brief'i tek cümlede yeniden ifade et — bu şey ne, nerede yaşayacak, ne yapmalı.

### Faz 2 — Keşif

Hiçbir şey tasarlamadan önce varyantların üzerinde duracağı zemini haritala:

- **Stack**: framework, styling sistemi (Tailwind, CSS modules, vanilla), varsa motion kütüphanesi.
- **Token'lar**: renkler, radius, spacing, font, easing/duration değişkenleri. Varyantlar bunları
  kullanır — her varyant yarın bu üründe ship edilebilecekmiş gibi görünmeli. Proje
  `ceran-design-system` tüketiyorsa (`.ceran/ecosystem.yaml`) token'ların kaynağı orasıdır;
  prototip için yeni bir palet uydurma.
- **Kişilik**: oyuncul bir tüketici uygulaması mı, net bir dashboard mı? En cesur varyantın ne
  kadar ileri gidebileceğini bu sınırlar.
- **Bağlam**: parça nerede render oluyor — hangi arka planın önünde, hangi komşuların yanında,
  hangi boyutlarda.

Proje yoksa (boş dizin ya da kullanıcı sadece keşfediyorsa) Faz 4'teki standalone dala geç ve
ölçülü bir öntanımlı görünüm seç: nötr griler, tek bir vurgu rengi, sistem font yığını.

### Faz 3 — Yönleri seç

Öntanımlı **3 varyant**; kullanıcı isterse ya da tasarım alanı gerçekten genişse 5'e kadar.
5'ten fazlası karşılaştırmayı sulandırır.

Kod yazmadan önce kümeyi listele: her biri için bir ad ve bir eksen. Adlar yönü tarif eder —
"Sakin", "Editoryal", "Oyuncul", "Yoğun" — asla "Seçenek A/B/C". Önerilen iki yön yalnız vurgu
rengi ya da metinde farklılaşıyorsa bunlar tek bir yöndür; birini gerçek bir alternatifle değiştir
(farklı layout, farklı etkileşim modeli, farklı motion hikâyesi).

**Tamamlanma ölçütü:** her varyantın bir adı ve belirtilmiş bir ekseni var ve hiçbir iki varyant
aynı eksen konumunu paylaşmıyor.

### Faz 4 — Seçici düzeneğini kur

Var olana göre iki dal:

- **Dev sunucusu olan bir projede** — izole bir route ya da sayfa (`/prototypes/<slug>` ya da
  framework'ün karşılığı), varyant başına bir dosya artı küçük bir düzenek dosyası. Prototip
  yüzeyinden üretim koduna hiçbir import olmaz.
- **Proje yok / statik bağlam** — kullanıcının doğrudan tarayıcıda açabileceği tek, kendi kendine
  yeten bir HTML dosyası.

Seçicinin markup'ı, stilleri, klavye bağlantıları ve konumu [PICKER.md](PICKER.md)'den birebir
gelir — şimdi yükle ve tam olarak onu kur. Seçicinin ötesinde düzenek, **aynı anda tek varyantı,
tam boyutta, gerçekçi çevre bağlamıyla** render etmeli — toast'ın arkasında bir sayfa, kartın
yanında kardeşleri, butonun içinde bir form olmalı. Yan yana küçük önizlemeler boşluk ve ölçeği
bozar; UI'ı pul boyutunda asla yargılama. Geçiş **anında** olur — varyant değiştirme oturum başına
100+ kez yapılan bir aksiyondur; sıklık kuralı gereği hiç animasyon almaz.

Bu ekosistemde dev sunucusu ayağa kaldırmak için Bash değil, tarayıcı önizleme akışını kullan
(`.claude/rules/` içindeki proje kuralları).

### Faz 5 — Doğrula ve devret

Düzeneği çalıştır. Her varyantın render olduğunu, her etkileşimin yanıt verdiğini ve konsolun
temiz olduğunu doğrula — kullanıcıya göstermeden önce hepsini kendin gez. Tarayıcı aracı varsa her
varyantın ekran görüntüsünü al.

Sonra kümeyi sun ve **dur — seçim kullanıcınındır**:

| # | Varyant | Eksen | Ne zaman doğru seçim | Bedeli |
| --- | --- | --- | --- | --- |
| 1 | Sakin | Az motion, gölge yerine kenarlık | Ürün her gün kullanılan bir araçsa | En az akılda kalıcı |
| 2 | Editoryal | Büyük tipografi, cömert boşluk | An ağırlığı hak ediyorsa | Dikey alan yer |

Seçicinin nerede çalıştığını (URL ya da dosya yolu) ve gezinme tuşlarını söyleyerek kapat.

**Tamamlanma ölçütü:** her varyant seçiciden ulaşılabilir ve doğru davranıyor; konsol hatası yok;
tablo her varyantın ödünleşimini dürüstçe adlandırıyor.

### Faz 6 — Seçim üzerine koda al

Kullanıcı seçtiğinde: o varyantı ait olduğu yere, projenin mevcut konvansiyonlarını izleyerek
(dosya yerleşimi, adlandırma, token kullanımı) entegre et; sonra 5. katı kural gereği prototip
yüzeyini sil. Kullanıcı bunun yerine bir tur daha istiyorsa düzeneği koru ve yöneldikleri yönün
*etrafında* ayrışarak Faz 3'ü tekrarla.

## Çağırma varyantları

| Çağırma | Davranış |
| --- | --- |
| `<tanım>` | Tam akış: kapsam → keşif → 3 varyant → seçici → seçimi bekle |
| `<tanım> x5` | Aynısı, o kadar varyantla (en fazla 5) |
| `riff <varyant>` | Yeni tur: düzeneği koru, adı verilen varyantın yönü etrafında yeni bir küme üret |
| `keep <varyant>` | O varyantı kod tabanına al ve prototip yüzeyini sil |
| `keep <varyant>, seçici kalsın` | Koda al ama prototip yüzeyini bırak |

## Ton

Her varyantı dürüstçe sat — ne zaman kazandığına bir satır, neye mal olduğuna bir satır. Tabloda
asla önceden favori seçme; kullanıcı hangisini seçeceğini sorarsa yanıtı yalnız estetiğe değil,
ürünün kişiliğine ve kullanım sıklığına dayandır. İnşa ederken iki varyant yakınsadıysa birini kes
ve bunu söyle: gerçekten farklı iki yönlü bir seçici, üçe şişirilmiş olandan iyidir.

---
> Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, Emil Kowalski) —
> ekosisteme uyarlandı (upstream adı: `prototype`). Uyarlama notları:
> `claude-foundation/docs/UPSTREAM-SKILLS.md`.
