# Network Aliases

# curl -s: silent mod, progress bar gösterme
# icanhazip.com: sadece IP döndürür, parse gerekmez
# Örnek: VPN kontrolü → myip (önce), VPN aç, myip (sonra)
# Script içinde: SERVER_IP=$(myip)
alias myip='curl -s https://icanhazip.com'

# lsof -i: ağ bağlantılarını listele
# -P: port numaralarını isim yerine sayı olarak göster (80 yerine "http" değil)
# -n: hostname çözümlemesini atla (daha hızlı)
# grep LISTEN: sadece dinleme yapanları filtrele
# Örnek: ports | grep 3000  (o port meşgul mu?)
alias ports='lsof -i -P -n | grep LISTEN'
