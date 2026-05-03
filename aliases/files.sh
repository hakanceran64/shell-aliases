# File & Directory Aliases

# Detailed list including hidden files
alias ll='ls -lAh'

# Show sizes sorted largest to smallest (files and hidden files included)
alias sizes='du -sh -- * .[^.]* 2>/dev/null | sort -rh'

# Create directory and cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Move to Trash instead of deleting permanently
alias trash='mv "$@" ~/.Trash/'
