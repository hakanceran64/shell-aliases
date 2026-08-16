#!/usr/bin/env bash
# bash-guard — yıkıcı/riskli bash komutlarını engelle
# Event: PreToolUse | Matcher: Bash
# Input: stdin JSON ({tool_name, tool_input.{command}})
# Exit: 0 = izin ver, 2 = engelle (stderr Claude'a feedback olur)
# Kaynak: fire-and-water (proje-bağımsız, doğrudan miras)
set -euo pipefail

INPUT="$(cat)"
CMD="$(printf '%s' "$INPUT" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get("tool_input", {}).get("command", ""))
except Exception:
    pass
')"

[[ -z "$CMD" ]] && exit 0

# Not: rm/sudo/dd pattern'ları segment-bazlı anchoring kullanır — satır başı VEYA
# `&&` / `;` / `|` sonrası da yakalanır (ör. `cd /tmp && rm -rf ~`).
declare -a BLOCKLIST=(
  '(^|[;&|])[[:space:]]*rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*f?[[:space:]]+(/|\$HOME|~)([[:space:]]|$)'
  '(^|[;&|])[[:space:]]*sudo[[:space:]]+rm[[:space:]]+-rf'
  'git[[:space:]]+push[^|;&]*[[:space:]](--force(-with-lease)?(=[^[:space:]]*)?|-[a-zA-Z]*f[a-zA-Z]*)([[:space:]]|$)'
  'git[[:space:]]+push[^|;&]*[[:space:]]\+[^[:space:]]'
  'git[[:space:]]+reset[[:space:]]+--hard[[:space:]]+origin'
  'git[[:space:]]+filter-(repo|branch)'
  # Node'dan yükseltildi (governance loop): ikisi de izlenmeyen/submodule içeriğini
  # geri dönüşsüz siler. `-fd`/`-df` sırası fark etmesin diye iki yönlü yazıldı.
  'git[[:space:]]+clean[^|;&]*[[:space:]]-[a-zA-Z]*(fd|df)[a-zA-Z]*([[:space:]]|$)'
  'git[[:space:]]+submodule[[:space:]]+deinit[^|;&]*[[:space:]]-[a-zA-Z]*f'
  'curl[[:space:]]+.*\|[[:space:]]*(sh|bash|zsh)'
  'wget[[:space:]]+.*\|[[:space:]]*(sh|bash|zsh)'
  '(^|[;&|])[[:space:]]*dd[[:space:]]+if='
  'mkfs'
  ':\(\)\{[[:space:]]*:\|:&[[:space:]]*\}'
  'rm[[:space:]]+.*(\.env|\.git/config|id_rsa|\.ssh/)'
  'docker[[:space:]]+system[[:space:]]+prune[[:space:]]+-a[[:space:]]+--volumes'
  '--no-verify'
  '--no-gpg-sign'
)

for pattern in "${BLOCKLIST[@]}"; do
  if printf '%s\n' "$CMD" | grep -qE -- "$pattern"; then
    {
      printf '%s\n' "[bash-guard] ENGELLENDİ: pattern eşleşti → /$pattern/"
      printf '%s\n' "[bash-guard] Komut: $CMD"
      printf '%s\n' "[bash-guard] Bu komut proje policy'sine göre yıkıcı kabul edilir."
      printf '%s\n' "[bash-guard] Gerçekten gerekliyse kullanıcıdan açık onay al."
    } >&2
    exit 2
  fi
done

exit 0
