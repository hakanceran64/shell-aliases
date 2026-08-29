#!/usr/bin/env bash
# pulse-record — oturumu kapatır: süre + o aralıkta düşen commit'ler.
# Event: Stop | Matcher: *
#
# `wrap-up.sh`'ın aksine ASYNC DEĞİL. Bu hook veri YAZAR; async koşup süreç
# kapanışında kesilirse oturum hiç kaydedilmez ve kullanıcı kaybettiğini
# bilmez. pulse'ın kendi zaman aşımı 2 saniyedir ve ulaşamazsa kuyruğa alır,
# yani senkron beklemenin üst sınırı zaten kısadır.
#
# FAIL-OPEN: pulse yoksa ya da hata verirse sessizce geçilir.
set -uo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$HOOK_DIR/../../scripts/find-pulse.sh" 2>/dev/null || exit 0

INPUT="$(cat 2>/dev/null || true)"

PULSE="$(find_pulse)" || exit 0
printf '%s' "$INPUT" | "$PULSE" record >&2 || true
exit 0
