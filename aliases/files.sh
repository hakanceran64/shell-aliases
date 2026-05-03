# File & Directory Aliases

# ls -lAh: long format, all files (including hidden), human-readable sizes
# Örnek: ll ~/Documents
alias ll='ls -lAh'

# du -sh: her öğenin toplam boyutu, human-readable
# sort -rh: insan okunabilir sayıları büyükten küçüğe sırala (1G > 500M > 2K)
# .[^.]*: tek nokta (.) ve çift nokta (..) hariç gizli dosyaları dahil et
# Örnek: cd ~ && sizes
alias sizes='du -sh -- * .[^.]* 2>/dev/null | sort -rh'

# mkdir -p: iç içe dizinleri de oluşturur, zaten varsa hata vermez
# Örnek: mkcd src/components/ui
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# rm yerine Çöp Kutusu'na taşı — Finder'dan kurtarılabilir
# Birden fazla dosya: trash *.log *.tmp
# "$@": tüm argümanları iletir
alias trash='mv "$@" ~/.Trash/'
