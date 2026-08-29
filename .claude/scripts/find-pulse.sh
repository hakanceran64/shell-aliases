#!/usr/bin/env bash
# find-pulse — `pulse` binary'sinin yerini bulur (ceran-pulse oturum kaydedicisi).
#
# İki hook (session-start/pulse-resume, stop/pulse-record) bunu source eder.
# Ayrı dosya olmasının sebebi: arama sırası TEK yerde dursun. İki kopyada
# tutulsaydı biri güncellenip diğeri unutulduğunda açılış ile kapanış farklı
# binary'leri çağırabilirdi — ve bu, oturumların yarısının kaydedilmemesi
# demek olurdu.
#
# Kullanım:  PULSE="$(find_pulse)" || exit 0

# find_pulse, çalıştırılabilir pulse yolunu basar; bulamazsa 1 döner.
#
# Sıra: PATH (kullanıcının kendi kurulumu kazanır) → ekosistem ağacındaki
# derlenmiş binary → ~/.local/bin. Ortam değişkeni PULSE_BIN hepsini ezer;
# test düzeneği ve geçici sürümler için.
find_pulse() {
    if [[ -n "${PULSE_BIN:-}" && -x "${PULSE_BIN}" ]]; then
        printf '%s\n' "$PULSE_BIN"
        return 0
    fi
    local found
    found="$(command -v pulse 2>/dev/null)" && [[ -n "$found" ]] && {
        printf '%s\n' "$found"
        return 0
    }
    local candidate
    for candidate in \
        "${CERAN_ECOSYSTEM_ROOT:-}/tools/ceran-pulse/bin/pulse" \
        "$HOME/.local/bin/pulse"
    do
        [[ -x "$candidate" ]] && { printf '%s\n' "$candidate"; return 0; }
    done
    return 1
}
