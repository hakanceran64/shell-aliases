# System Aliases

# ps aux: tüm processleri göster
# sort -rk 3: 3. kolon olan %CPU'ya göre büyükten küçüğe sırala
# head -10: ilk 10 process
# Örnek: cpu | grep node  (node process'i ne kadar CPU kullanıyor?)
alias cpu='ps aux | sort -rk 3 | head -10'

# dscacheutil -flushcache: DNS önbelleğini temizle
# killall -HUP mDNSResponder: DNS servisini yeniden başlat
# Kullanım: /etc/hosts değişikliği, yeni domain, VPN sonrası sorun
alias flushdns='sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder && echo "DNS flushed"'

# defaults write: macOS tercihleri veritabanına yaz
# killall Finder: Finder'ı yeniden başlatarak değişikliği uygula
# showfiles ile başla, işin bitince hidefiles ile gizle
alias showfiles='defaults write com.apple.finder AppleShowAllFiles YES && killall Finder'
alias hidefiles='defaults write com.apple.finder AppleShowAllFiles NO && killall Finder'
