---
name: pick-ui-library
description: Bir frontend işi için doğru kütüphaneyi seçer — sayı animasyonu, OTP input, grafik, command menu, virtualization, drag and drop, toast, state, styling ve dahası. Önce ekosistemin kendi kataloğuna (shared-modules · ceran-design-system · devkit-wiki tech-card'ları), sonra aşağıdaki küratörlü listeye bakar. Yalnız açıkça çağrıldığında çalışır.
when_to_use: "'hangi kütüphaneyi kullanayım', 'toast lazım', 'drag and drop için ne var', '/pick-ui-library'"
argument-hint: "[iş tanımı, ör. 'toast lazım']"
disable-model-invocation: true
---

# Doğru kütüphaneyi seçmek

Bir arama skill'i. Bir işle çağrıldığında ("toast lazım", "drag and drop için ne kullanmalıyım?")
işi aşağıdaki listeyle eşleştirir ve kütüphaneyi önerir. Bunlar bilinçli, zevke dayalı seçimlerdir
— kullanıcı istemedikçe ya da iş gerçekten kapsam dışı kalmadıkça liste dışına çıkma.

## Karar sırası

Yukarıdan aşağı in; ilk yanıt verende dur.

1. **Ekosistem zaten çözmüş mü?**
   - `shared-modules` (auth · db-helper) bu işi kapsıyorsa yeni bağımlılık ekleme.
   - Token, renk, radius, spacing, ikon → `ceran-design-system`. Proje bunu tüketiyorsa
     (`.ceran/ecosystem.yaml` → `consume.design-system`) paralel bir tema/token sistemi kurma.
2. **Katman kararı `devkit-wiki` kataloğunda mı?** Stack düzeyindeki seçimler (state yönetimi,
   render katmanı, HTTP, auth, test) tech-card'larda karara bağlanmıştır — `wiki/02-frontend/`,
   `wiki/INDEX.md`. Kart varsa **kart kazanır**; aşağıdaki liste yalnız kartın altındaki mikro
   seçimi doldurur.
3. **İşi belirle, kullanıcının andığı kütüphaneyi değil.** "Dropdown göstermem lazım" bir UI
   primitive işidir (base-ui), başka bir şey sormuş olsalar bile.
4. **Zaten kurulu olana bak.** Önce `package.json`. Proje listedeki bir kütüphaneyi zaten
   kullanıyorsa onu kullan. Rakibini kullanıyorsa (ör. Virtuoso yerine react-window) öneriyi
   belirt ama istenmedikçe bağımlılığı değiştirme.
5. **Tek bir kütüphane öner**, ne işe yaradığını tek cümlede söyle, talebin parçasıysa kur ve
   bağla. Listenin net yanıtı varken menü sunma.
6. **İş listede yoksa** bunu açıkça söyle ve kendi bilginle öner — ama küratörlü listenin dışına
   çıktığını belirt. Karar kalıcıysa `/adr` ile kaydet.

## Liste

### UI bileşenleri ve primitive'ler

| İş | Kütüphane |
| --- | --- |
| Stilsiz, erişilebilir UI bileşenleri (dialog, popover, menü, select…) | [base-ui](https://base-ui.com) |
| Command menu (⌘K paleti) | [cmdk](https://cmdk.paco.me) |
| Toast / bildirim | [Sonner](https://sonner.emilkowal.ski) — kullanım rehberi: `/sonner` |
| Tek kullanımlık şifre / doğrulama kodu input'u | [input-otp](https://input-otp.rodz.dev) |
| Özelleştirilebilir GUI / kontrol paneli | [Leva](https://github.com/pmndrs/leva) — alternatif: [dialkit](https://joshpuckett.me/dialkit) |

### Motion ve görseller

| İş | Kütüphane |
| --- | --- |
| Genel amaçlı animasyon (spring, layout animasyonu, giriş/çıkış) | [motion](https://motion.dev) (Framer Motion) |
| Sayı animasyonu (sayaç, fiyat, istatistik) | [NumberFlow](https://number-flow.barvian.me) |
| Animasyonlu metin bileşenleri | [torph](https://torph.lochie.me/) |
| 3B küre | [Cobe](https://cobe.vercel.app) |
| Dinamik OG görselleri (HTML/CSS → SVG/PNG) | [Satori](https://github.com/vercel/satori) |
| Syntax highlighting | [shiki](https://shiki.style) |

motion'a spring, layout animasyonu, exit animasyonu ya da jest güdümlü değerler gerektiğinde uzan.
Basit bir hover ya da fade bunu gerektirmez — orada düz CSS transition doğru araçtır (`/animate`).

### Grafikler

| İş | Kütüphane |
| --- | --- |
| Gerçek zamanlı / akan grafikler | [Liveline](https://github.com/benjitaylor/liveline) |
| Genel grafikler (statik ya da etkileşimli dashboard) | [recharts](https://recharts.org) |

Ayrım: veri noktaları canlı geliyor ve grafik zamanla kayıyorsa Liveline; diğer her şey recharts.

### Etkileşim ve performans

| İş | Kütüphane |
| --- | --- |
| Drag and drop | [dnd kit](https://dndkit.com) |
| Virtualization (uzun liste, büyük tablo) | [Virtuoso](https://virtuoso.dev) |

### State ve styling

| İş | Kütüphane |
| --- | --- |
| İstemci durumu yönetimi | [zustand](https://zustand.docs.pmnd.rs) |
| **Sunucu** durumu (fetch/cache/yeniden doğrulama) | [TanStack Query](https://tanstack.com/query) |
| Koşullu `className` string'i kurmak | [clsx](https://github.com/lukeed/clsx) |
| Tailwind için tip güvenli, varyant tabanlı styling | [cva](https://cva.style) |
| Tema değiştirme / dark mode (yüklemede flash yok) | [next-themes](https://github.com/pacocoursey/next-themes) |

**Durum ayrımı `devkit-wiki/02-frontend/state-management.md`'den gelir:** sunucudan gelen veriyi
global client store'a kopyalama — o TanStack Query'nin işi. zustand istemci/UI/oturum durumu
içindir. Büyük ekip + sıkı denetim + zaman yolculuğu gerekiyorsa kart Redux Toolkit'i de bir
seçenek olarak bırakır.

**Styling ayrımı:** anlık koşullu class'lar için clsx; bileşenin tiplenmiş bir API hak eden
gerçek varyantları (size, intent, state) varsa cva. Birlikte çalışırlar — cva içeride clsx tarzı
girdi kullanır. Renk/spacing/radius değerleri `ceran-design-system` token'larından gelir; cva
varyantları token'ların üstüne biner, onların yerine geçmez.

## Yakalanacak yaygın uyumsuzluklar

- **Elle ya da modal kütüphanesiyle yazılmış toast** → Sonner tam bunun için var.
- **`<div>` tabanlı dropdown/dialog, elle focus yönetimi** → base-ui; erişilebilirliği, focus
  trap'i ve kapanmayı o hallediyor.
- **Metni yeniden render ederek sayı animasyonu** → NumberFlow rakam geçişlerini düzgün yapar.
- **1000+ satırlık listeyi doğrudan render etmek** → sayfalama hilelerinden önce Virtuoso.
- **Paylaşılan durum için bileşen başına `useState` ve prop ağı** → zustand (veri sunucudan
  geliyorsa TanStack Query).
- **Üç koşul derinliğinde template-literal className üçlemesi** → clsx (varyant şeklindeyse cva).
- **Projede zaten `ceran-design-system` varken ikinci bir token/tema katmanı** → design system'i
  genişlet, çatallama.

---
> Kaynak: [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT, Emil Kowalski) —
> ekosisteme uyarlandı. Uyarlama notları: `claude-foundation/docs/UPSTREAM-SKILLS.md`.
