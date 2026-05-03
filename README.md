# shell-aliases

Günlük terminali kullanımını hızlandırmak için hazırlanmış zsh alias ve fonksiyon koleksiyonu. Dosya yönetiminden git'e, ağ araçlarından sistem izlemeye kadar sık kullanılan işlemleri tek komuta indirger.

---

## Kurulum

```bash
git clone git@github.com:hakanceran64/shell-aliases.git
cd shell-aliases
chmod +x install.sh
./install.sh
source ~/.zshrc
```

> Kurulum, `~/.zshrc` dosyasına her alias dosyası için bir `source` satırı ekler.  
> Repo'yu güncellediğinde (`git pull`) alias'lar otomatik olarak güncellenir — tekrar kurulum gerekmez.

## Kaldırma

```bash
./uninstall.sh
source ~/.zshrc
```

---

## İçindekiler

- [Dosya & Dizin](#dosya--dizin)
- [Git](#git)
- [Ağ](#ağ)
- [Sistem](#sistem)
- [Yardımcı](#yardımcı)

---

## Dosya & Dizin

### `ll` — Detaylı dosya listesi

```bash
alias ll='ls -lAh'
```

`ls -lAh` kısaltması. Gizli dosyalar (`.` ile başlayanlar) dahil tüm öğeleri izinler, sahip, boyut ve tarih ile listeler. Boyutları insan okunabilir formatta gösterir (KB, MB, GB).

**Örnek çıktı:**
```
drwxr-xr-x   5 ceran  staff   160B  3 May 11:20 .git
-rw-r--r--   1 ceran  staff   2.4K  3 May 11:20 README.md
-rwxr-xr-x   1 ceran  staff   420B  3 May 11:18 install.sh
```

**En iyi kullanım senaryoları:**
```bash
# Bir projeye girince ilk şey
cd my-project && ll

# Gizli config dosyalarını kontrol et (.env, .gitignore vb.)
ll ~/Documents/GitHub/my-app

# Dosya izinlerini doğrula (deploy öncesi executable mı?)
ll bin/
```

---

### `sizes` — Boyuta göre sıralı liste

```bash
alias sizes='du -sh -- * .[^.]* 2>/dev/null | sort -rh'
```

Bulunduğun dizindeki tüm klasör ve dosyaların (gizliler dahil) disk kullanımını büyükten küçüğe sıralar. `du -sh` ile her öğenin toplam boyutunu alır, `sort -rh` ile insan okunabilir sayıları doğru sıralar (örn. 1G > 500M > 2K).

**Örnek çıktı:**
```
5.0G    GitHub
2.3G    Downloads
840M    node_modules
120M    .cache
4.0K    README.md
```

**En iyi kullanım senaryoları:**
```bash
# Disk doldu, nerede yer var? Ana dizinden başla
cd ~ && sizes

# node_modules mı, cache mi yer yiyor?
cd my-project && sizes

# Hangi log dosyası şişmiş?
cd /var/log && sizes

# Arşivlemeden önce en büyük klasörleri bul
cd ~/Documents && sizes | head -5
```

---

### `mkcd` — Klasör oluştur ve içine gir

```bash
mkcd() {
    mkdir -p "$1" && cd "$1"
}
```

`mkdir` + `cd` kombinasyonu. `-p` flag'i ile iç içe geçmiş klasör yapısını tek seferde oluşturur; ara dizinler yoksa onları da yaratır.

**En iyi kullanım senaryoları:**
```bash
# Yeni proje başlatırken
mkcd ~/Documents/GitHub/my-new-project
git init

# İç içe klasör yapısı oluştur
mkcd src/components/ui/buttons
# → src/, components/, ui/, buttons/ hepsini oluşturur ve buttons/ içine girer

# Geçici çalışma alanı
mkcd /tmp/test-build && cmake .. && make
```

---

### `trash` — Güvenli silme

```bash
alias trash='mv "$@" ~/.Trash/'
```

`rm` yerine macOS Çöp Kutusu'na taşır. Yanlışlıkla silinen dosyalar Finder üzerinden kurtarılabilir. Birden fazla dosyayı aynı anda taşıyabilir.

**En iyi kullanım senaryoları:**
```bash
# Tek dosya
trash old-config.json

# Birden fazla dosya
trash *.log *.tmp

# Klasör
trash node_modules/

# Dikkat: rm yerine kullanma alışkanlığı edin
# rm -rf build/   →   trash build/
```

> **Not:** Çöp Kutusu'nu komutla boşaltmak için: `rm -rf ~/.Trash/*`

---

## Git

### `gst` — Hızlı status

```bash
alias gst='git status'
```

**En iyi kullanım senaryoları:**
```bash
# Commit öncesi ne değişti?
gst

# Staged/unstaged ayrımını hızlı gör
gst
```

---

### `glog` — Grafikli commit geçmişi

```bash
alias glog='git log --oneline --graph --decorate --all'
```

Her commit tek satırda gösterilir. `--graph` branch/merge yapısını ASCII art ile çizer. `--decorate` HEAD, branch ve tag isimlerini ekler. `--all` uzak branch'leri de dahil eder.

**Örnek çıktı:**
```
* a3f82c1 (HEAD -> main, origin/main) Add network aliases
* 7b1d4e0 Add git aliases
| * 9c2f3a1 (feature/system-aliases) Add system aliases
|/
* 1a0b2c3 Initial commit
```

**En iyi kullanım senaryoları:**
```bash
# Merge öncesi branch durumunu gör
glog

# Hangi commit ne zaman ayrıldı?
glog | head -20

# Belirli bir dosyanın geçmişi
git log --oneline --follow -- src/utils.js
```

---

### `undocommit` — Son commit'i geri al

```bash
alias undocommit='git reset --soft HEAD~1'
```

Son commit'i geri alır ama değişiklikleri staged (hazır) olarak bırakır. Commit mesajını düzeltmek veya değişiklikleri yeniden düzenlemek için idealdir. `--soft` sayesinde hiçbir kod kaybı olmaz.

**En iyi kullanım senaryoları:**
```bash
# Yanlış commit mesajı yazdın
undocommit
git commit -m "Doğru mesaj"

# İki commit'i tek birleştirmek istiyorsun
undocommit   # son commit geri alındı, değişiklikler staged
# önceki commit'in değişiklikleri zaten orada
git commit -m "İkisini kapsayan tek commit"

# Push'tan önce fark ettim, commit içeriğini düzenleyeyim
undocommit
# dosyaları düzenle
git add -p   # seçerek stage et
git commit -m "Temiz commit"
```

> **Dikkat:** `git push` yaptıktan sonra kullanmak history'yi değiştirir; paylaşılan branch'lerde sorun yaratır.

---

## Ağ

### `myip` — Dış IP adresi

```bash
alias myip='curl -s https://icanhazip.com'
```

Sunucunun veya bilgisayarın internet üzerinde göründüğü IP adresini döner. `icanhazip.com` yalnızca IP döndürür, parse etmeye gerek yoktur.

**En iyi kullanım senaryoları:**
```bash
# VPN açık mı kontrol et
myip   # VPN kapalıyken not al, sonra VPN'i aç ve tekrar çalıştır

# Sunucunun IP'sini script'te kullan
SERVER_IP=$(myip)
echo "Firewall'a $SERVER_IP ekle"

# Farklı ağlarda test ederken hangi IP'den görünüyorsun?
myip
```

---

### `ports` — Açık portlar

```bash
alias ports='lsof -i -P -n | grep LISTEN'
```

Sistemde aktif olarak dinleme yapan tüm processleri ve portları listeler. `-P` port numaralarını isim yerine sayı olarak gösterir. `-n` hostname çözümlemesini atlar, çıktı hızlanır.

**Örnek çıktı:**
```
node      1234  ceran   21u  IPv4  ...  TCP *:3000 (LISTEN)
postgres  5678  ceran   5u   IPv6  ...  TCP *:5432 (LISTEN)
nginx     9012  root    6u   IPv4  ...  TCP *:80 (LISTEN)
```

**En iyi kullanım senaryoları:**
```bash
# Hangi port kullanımda?
ports | grep 3000

# Dev server çalışıyor mu?
ports | grep node

# Belirli port'u hangi process tutuyor?
ports | grep 8080

# Tüm açık portlara genel bakış
ports
```

---

## Sistem

### `cpu` — CPU kullanan processler

```bash
alias cpu='ps aux | sort -rk 3 | head -10'
```

CPU kullanım yüzdesine göre sıralanmış ilk 10 process'i gösterir. `sort -rk 3` üçüncü kolonu (CPU%) büyükten küçüğe sıralar.

**Örnek çıktı:**
```
USER   PID  %CPU %MEM    VSZ   RSS  COMMAND
ceran  823  98.2  1.4  ...     ... node
ceran  412  12.4  3.2  ...     ... Xcode
```

**En iyi kullanım senaryoları:**
```bash
# Fan çılgın gibi dönüyor, neden?
cpu

# Build işlemi bitti mi?
cpu | grep xcodebuild

# Hangi process sistemi yavaşlatıyor?
cpu

# Daha canlı izleme için (q ile çık)
top -o cpu
```

---

### `flushdns` — DNS cache temizle

```bash
alias flushdns='sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder && echo "DNS flushed"'
```

macOS'un DNS önbelleğini temizler ve mDNSResponder servisini yeniden başlatır. `sudo` gerektirir.

**En iyi kullanım senaryoları:**
```bash
# Yeni bir domain yayına aldın ama eski IP görünüyor
flushdns

# /etc/hosts'a yeni satır ekledin, hemen aktif olsun
flushdns

# VPN sonrası DNS sorunları yaşıyorsun
flushdns

# Bir siteye erişemiyorsun ama başkası erişebiliyor
flushdns
```

---

### `showfiles` / `hidefiles` — Finder gizli dosyalar

```bash
alias showfiles='defaults write com.apple.finder AppleShowAllFiles YES && killall Finder'
alias hidefiles='defaults write com.apple.finder AppleShowAllFiles NO && killall Finder'
```

Finder'ı yeniden başlatarak gizli dosyaları (`.` ile başlayanları) gösterir veya gizler. Terminalde zaten görünürler; bu alias sadece Finder için gereklidir.

**En iyi kullanım senaryoları:**
```bash
# .env, .DS_Store, .gitignore'u Finder'da görmek istiyorsun
showfiles

# Kullanıcıya teslim etmeden önce gizlileri tekrar sakla
hidefiles

# macOS sistem dosyalarına Finder üzerinden erişmek
showfiles
# işin bitince
hidefiles
```

---

## Yardımcı

### `week` — Hafta numarası

```bash
alias week='date +%V'
```

ISO 8601 standardına göre yılın kaçıncı haftasında olduğunu gösterir (01–53).

**En iyi kullanım senaryoları:**
```bash
# Sprint numarası = hafta numarası mı?
week

# Log dosyası veya klasör ismine hafta ekle
mkdir "sprint-$(week)-notes"

# Script içinde tarih bazlı mantık
if [ $(week) -gt 40 ]; then echo "Yılın son çeyreği"; fi
```

---

### `path` — PATH içeriği

```bash
alias path='echo $PATH | tr ":" "\n"'
```

`$PATH` ortam değişkenini `:` ayracından bölerek her dizini ayrı satırda gösterir. Hangi dizinlerin PATH'te olduğunu ve sırasını anlamak için kullanışlıdır.

**Örnek çıktı:**
```
/opt/homebrew/bin
/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbin
```

**En iyi kullanım senaryoları:**
```bash
# Bir komut neden bulunamıyor?
path   # ilgili dizin PATH'te mi?

# Birden fazla Python/Node versiyonu var, hangisi önce geliyor?
path | grep python
path | grep node

# Yeni tool kurulumu sonrası PATH'e eklendi mi?
path | grep homebrew

# Hangi sırayla aranıyor? (önce gelen öncelikli)
path
```

---

### `reload` — Shell'i yeniden yükle

```bash
alias reload='source ~/.zshrc && echo "~/.zshrc reloaded"'
```

`~/.zshrc` dosyasını yeniden yükler. Terminali kapatıp açmaya gerek kalmaz.

**En iyi kullanım senaryoları:**
```bash
# Yeni alias ekledin, hemen aktif olsun
reload

# Ortam değişkeni tanımladın
reload

# Bu repo'yu güncelledin
git pull && reload

# shell-aliases'e yeni alias ekledin
reload
```

---

## Yapı

```
shell-aliases/
├── aliases/
│   ├── files.sh      # ll, sizes, mkcd, trash
│   ├── git.sh        # gst, glog, undocommit
│   ├── network.sh    # myip, ports
│   ├── system.sh     # cpu, flushdns, showfiles, hidefiles
│   └── utils.sh      # week, path, reload
├── install.sh
├── uninstall.sh
└── README.md
```

## Katkı

Yeni alias eklemek için:
1. İlgili `aliases/*.sh` dosyasını düzenle
2. Zaten kuruluysa değişiklikler otomatik aktif olur (`reload` ile anında)
3. Yeni kategori gerekiyorsa `aliases/yeni.sh` oluştur ve `install.sh`'e `source` satırını ekle
