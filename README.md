# shell-aliases

Günlük kullanım için faydalı zsh alias ve fonksiyon koleksiyonu.

## Kurulum

```bash
git clone git@github.com:hakanceran64/shell-aliases.git
cd shell-aliases
chmod +x install.sh
./install.sh
source ~/.zshrc
```

## Kaldırma

```bash
./uninstall.sh
source ~/.zshrc
```

---

## Aliases

### Dosya & Dizin (`aliases/files.sh`)

| Komut | Açıklama |
|-------|----------|
| `ll` | Gizli dosyalar dahil detaylı liste (`ls -lAh`) |
| `sizes` | Bulunduğun dizindeki tüm öğeleri boyuta göre büyükten küçüğe listeler |
| `mkcd <dir>` | Klasör oluşturur ve içine girer |
| `trash <file>` | Dosyayı kalıcı silmek yerine Çöp Kutusu'na taşır |

### Git (`aliases/git.sh`)

| Komut | Açıklama |
|-------|----------|
| `gst` | `git status` |
| `glog` | Renkli, grafikli commit geçmişi |
| `undocommit` | Son commit'i geri alır, değişiklikler staged olarak kalır |

### Ağ (`aliases/network.sh`)

| Komut | Açıklama |
|-------|----------|
| `myip` | Dış IP adresini gösterir |
| `ports` | Dinleme modundaki tüm portları listeler |

### Sistem (`aliases/system.sh`)

| Komut | Açıklama |
|-------|----------|
| `cpu` | En çok CPU kullanan 10 process |
| `flushdns` | macOS DNS cache'ini temizler |
| `showfiles` | Finder'da gizli dosyaları gösterir |
| `hidefiles` | Finder'da gizli dosyaları gizler |

### Yardımcı (`aliases/utils.sh`)

| Komut | Açıklama |
|-------|----------|
| `week` | Yılın kaçıncı haftasında olduğunu gösterir |
| `path` | `$PATH` içeriğini her satıra bir entry olacak şekilde gösterir |
| `reload` | `~/.zshrc` dosyasını yeniden yükler |

---

## Yapı

```
shell-aliases/
├── aliases/
│   ├── files.sh
│   ├── git.sh
│   ├── network.sh
│   ├── system.sh
│   └── utils.sh
├── install.sh
├── uninstall.sh
└── README.md
```
