# Noeul styles for zsh-syntax-highlighting.
# Every color is an ANSI index, so the styles follow the terminal's Noeul palette in
# light and dark. Strings, reserved words and redirections keep the plugin's yellow.
typeset -gA ZSH_HIGHLIGHT_STYLES

# A command that exists reads as plain text. One that does not is dimmed like a comment.
ZSH_HIGHLIGHT_STYLES[arg0]='none'
ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=8'
ZSH_HIGHLIGHT_STYLES[comment]='fg=8'
ZSH_HIGHLIGHT_STYLES[precommand]='underline'
ZSH_HIGHLIGHT_STYLES[autodirectory]='underline'
ZSH_HIGHLIGHT_STYLES[suffix-alias]='underline'

# The plugin's blue and cyan defaults, muted to tx2.
ZSH_HIGHLIGHT_STYLES[globbing]='fg=7'
ZSH_HIGHLIGHT_STYLES[history-expansion]='fg=7'
ZSH_HIGHLIGHT_STYLES[global-alias]='fg=7'
ZSH_HIGHLIGHT_STYLES[rc-quote]='fg=7'
ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]='fg=7'
ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]='fg=7'
ZSH_HIGHLIGHT_STYLES[back-dollar-quoted-argument]='fg=7'
