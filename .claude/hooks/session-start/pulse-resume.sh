#!/usr/bin/env bash
# pulse-resume — oturumu NodeFlow'a açar ve "nerede kalmıştın" özetini basar.
# Event: SessionStart | Matcher: *
#
# Bu hook İNCEDİR ve öyle kalmalı: tüm mantık `pulse` binary'sindedir
# (hakanceran64/tools/ceran-pulse). Buraya iş yazmak, 45 üyeye dağıtılmış 45
# kopyada bakım yapmak demek olurdu.
#
# FAIL-OPEN: pulse kurulu değilse, yapılandırılmamışsa ya da NodeFlow kapalıysa
# sessizce geçilir. Bu hook her oturumun ÖNÜNDE durur; kayıt tutmak, kullanıcının
# çalışmaya başlamasından daha önemli değildir.
set -uo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$HOOK_DIR/../../scripts/find-pulse.sh" 2>/dev/null || exit 0

# stdin'deki hook JSON'ı (session_id, cwd) pulse'a aktarılır. Okumazsak boru
# dolabilir ve Claude Code yazarken bloke olur.
INPUT="$(cat 2>/dev/null || true)"

PULSE="$(find_pulse)" || exit 0
# Çıktı stderr'e: SessionStart'ın stdout'u başka amaçlarla yorumlanabilir,
# bağlam satırları oraya karışmamalı (kit'teki show-context.sh ile aynı desen).
printf '%s' "$INPUT" | "$PULSE" resume >&2 || true
exit 0
