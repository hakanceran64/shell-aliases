# Utility Aliases

# date +%V: ISO 8601 hafta numarası (01-53)
# Örnek: mkdir "sprint-$(week)-notes"
alias week='date +%V'

# tr ":" "\n": : karakterini newline ile değiştir
# Kullanım: hangi dizin önce geliyor, tool kuruldu mu, neden bulunamıyor?
# Örnek: path | grep homebrew
alias path='echo $PATH | tr ":" "\n"'

# Yeni alias ekledikten veya .zshrc değiştirdikten sonra kullan
# Terminali kapatıp açmaya gerek kalmaz
alias reload='source ~/.zshrc && echo "~/.zshrc reloaded"'
