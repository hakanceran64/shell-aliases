# Git Aliases

# Örnek: gst (commit öncesi değişikliklere hızlı bak)
alias gst='git status'

# --oneline: her commit tek satır (hash + mesaj)
# --graph:   branch/merge yapısı ASCII art ile
# --decorate: HEAD, branch, tag isimlerini göster
# --all:     uzak branch'leri de dahil et
# Örnek: glog | head -20
alias glog='git log --oneline --graph --decorate --all'

# git reset --soft: commit'i geri al, değişiklikler staged olarak kalır
# --soft vs --hard: --hard değişiklikleri de siler, --soft korur
# Dikkat: push sonrası kullanmak history değiştirir
# Örnek: undocommit && git commit -m "Düzeltilmiş mesaj"
alias undocommit='git reset --soft HEAD~1'
