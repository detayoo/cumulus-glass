#!/bin/sh
# Re-apply after every update of the Claude Code extension, then run "Developer: Reload Window".
# 1. Claude Code fades long tool IN/OUT previews with a mask built from the panel background color;
#    Cumulus Glass makes that color transparent, which hid the text. A mask only reads alpha,
#    so solid black gives the same fade in every theme.
# 2. Appends chat-panel-glass.css from this folder (glass input box, scoped to Cumulus Glass).
GLASS="$(cd "$(dirname "$0")" && pwd)/chat-panel-glass.css"
for d in "$HOME"/.vscode/extensions/anthropic.claude-code-*/webview; do
  f="$d/index.css"
  [ -f "$f" ] || continue
  [ -f "$f.cumulus-backup" ] || cp "$f" "$f.cumulus-backup"
  sed -i '' 's/linear-gradient(to bottom,var(--app-primary-background)50px,transparent 60px)/linear-gradient(to bottom,#000 50px,transparent 60px)/' "$f"
  sed -i '' '/cumulus-glass:start/,/cumulus-glass:end/d' "$f"
  cat "$GLASS" >> "$f"
  for c in inputContainer_cKsPxg inputFooter_gGYT1w sendButton_gGYT1w modelPill_gGYT1w; do
    grep -q "\.$c[{:]" "$f.cumulus-backup" || echo "warning: .$c not found in this extension version; the input glass may need updating"
  done
  echo "patched: $f"
done
