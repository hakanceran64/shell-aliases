---
name: insights
description: Ekosistem çıkarımlarını okur ve harekete çevirir — hangi repo bakımsız, zaman planın dışına nereden akıyor. Sayıyı `pulse insights` üretir; bu skill onu yorumlar ve sıradaki adımı seçer.
when_to_use: "Tetikleyiciler: '/insights', 'hangi repo bakımsız', 'nerede kaldık', 'zaman nereye gitti', 'neye bakmalıyım'"
allowed-tools: Read, Glob, Grep, Bash(pulse:*), Bash(git log:*), Bash(git status:*)
---

# Ekosistem çıkarımları

`pulse insights` iki soruya cevap verir: **hangi repo bakımsız** ve **zaman planın
dışına nereden akıyor**. Bu skill o çıktıyı okur, ne anlama geldiğini söyler ve
sıradaki işi seçer.

## Çalıştır

```
pulse insights                        # son 30 gün
pulse insights --since 90d --limit 10
```

`pulse` yoksa (`command -v pulse` boş): kurulum `ceran-pulse` reposunda
`make install`. Kurulu değilse **dur ve söyle** — elle hesaplamaya kalkma.

## Değişmez kural — sayıyı YENİDEN ÜRETME

Çıktıdaki her sayı deterministik olarak hesaplanmıştır. Senin işin onu
**yorumlamak**, tekrar türetmek değil.

- Komut "ölçüm tabanı yetersiz" diyorsa, **kendi tahminini koyma**. Eksik olan
  ölçümdür; onu muhakemeyle dolduramazsın.
- "Oturum ekseni sayılmadı" satırı bir kusur değil, bir **beyandır**: kayıt
  pencereden gençken oturum yokluğu repo hakkında bir şey söylemez.
- Bulgu yoksa "bulgu yok" de. Boş bir listeyi doldurmak için eşik gevşetme.

Gerekçe: bu ekosistemin kuralı, ölçülemeyeni ölçülmüş gibi sunmamaktır
(`ceran-pulse/CLAUDE.md` kural 7). Yanlış bir "yolundasın", cevapsızlıktan pahalıdır.

## Çıktıyı okuma

| Bölüm | Ne demek | Ne yap |
|---|---|---|
| **VERİ GÜVENİ** | Ölçümün kendisi bozuk — kapanmamış oturum ya da damgasıyla çelişen süre | Önce bunu çöz; altındaki her sayı buna dayanıyor |
| **BAKIMSIZ REPO** | Açık işi var ama pencerede gerçek iş commit'i yok | En üsttekini seç: gecikmiş iş > durgunluk > iş yükü |
| **ZAMAN PLANIN DIŞINDA** | Ölçülen zaman plana bağlanamıyor | İşe bağsız oturum → `pulse task`; plansız repo → `pulse plan` |
| "Eşiğe en yakın" | Bulgu yok, ama bunlar sınıra yaklaşmış | Bilgi; aksiyon gerekmez |

Bakımsızlık üç sinyalin çarpımıdır ve üçü de düzeltilmiş hâlleriyle kullanılır:
rollout commit'leri (`.claude/`, `.ceran/`, README) sayılmaz — yoksa `dev eco sync`
bütün repoları "bugün çalışılmış" gösterir; açık işi olmayan repo **boştadır**,
bakımsız değil; ve yerelde olmayan repo hakkında bulgu üretilmez.

## Bulgudan işe

1. **En üstteki bulguyu** al (sıralama zaten müdahale önceliğine göre).
2. O reponun bağlamını oku: `pulse progress --repo <ad>` + reponun `TODO.md`'si.
3. Kullanıcıya **tek bir sonraki adım** öner — liste değil, seçim.
4. Kabul ederse o repoya geç ve oturumu işe bağla: `pulse task <kimlik>`.

Kendiliğinden görev açma, repo değiştirme ya da commit atma: bu skill **okur ve
önerir**. Oturum ≠ görev kuralı burada da geçerlidir.

## İlgili

- Ham tablolar: `pulse board` · `pulse report` · `pulse progress`
- Derin git denetimi: `backup-system/scripts/sync_check.sh --fetch`
- Kaynak: `ceran-pulse` (komutun kendisi ve gerekçesi README'de)
