# System Aliases

# Top CPU-consuming processes
alias cpu='ps aux | sort -rk 3 | head -10'

# Flush macOS DNS cache
alias flushdns='sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder && echo "DNS flushed"'

# Toggle hidden files in Finder
alias showfiles='defaults write com.apple.finder AppleShowAllFiles YES && killall Finder'
alias hidefiles='defaults write com.apple.finder AppleShowAllFiles NO && killall Finder'
