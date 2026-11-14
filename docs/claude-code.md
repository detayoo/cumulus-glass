# Claude Code panel (optional)

The [Claude Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) chat panel runs in a webview, which the glass CSS can't reach. This optional patch styles it to match.

**This edits another extension's files.** It's unofficial, it may stop matching after a Claude Code update, and it makes a backup so you can undo it.

## What it changes

- The input box becomes glass, with a blue focus ring in every permission mode.
- The send button is blue and uses Hugeicons' SendHorizontal icon. The Auto mode button uses MagicWand01.
- The model and mode pills become glass chips.
- Orange and pink accents become blue, and italics are turned off.
- It fixes tool IN/OUT previews going blank. Claude Code fades long previews with a mask made from the panel background color. Cumulus Glass makes that color transparent, which hid the text. The patch makes the mask solid black instead, which fades the same way in every theme.

Apart from the mask fix, all of it applies only while Cumulus Glass is active.

## Install

`python3 build.py --install` copies the patch files to `~/.vscode/cumulus/`. Then run:

```sh
~/.vscode/cumulus/patch-claude-code.sh
```

Then run **Developer: Reload Window** in VS Code. This restarts any running Claude Code session.

From then on, the companion extension re-applies the patch automatically when Claude Code updates, and offers to reload. You can also run it by hand: **Cumulus: Re-apply Claude Code glass**.

### Optional: a Claude Code slash command

To re-apply it from inside Claude Code with `/cumulus-glass`:

```sh
mkdir -p ~/.claude/commands
cp claude-code/cumulus-glass.md ~/.claude/commands/
```

If Claude Code asks for permission to run the script, approve it, or replace `~` with your full home path in the file.

## If it stops working

Claude Code's CSS uses generated class names such as `inputContainer_cKsPxg`, which can change between versions. The script prints a `warning:` line for any class it can't find. When that happens, the input box styling in `claude-code/claude-code-glass.css` needs its class names updated for the new version.

## Undo

The script backs up the original file once, as `index.css.cumulus-backup`, next to it. To restore it:

```sh
for f in ~/.vscode/extensions/anthropic.claude-code-*/webview/index.css.cumulus-backup; do
  cp "$f" "${f%.cumulus-backup}"
done
```

Then delete `~/.vscode/cumulus/patch-claude-code.sh` so the companion extension stops re-applying it, and reload the window. Updating Claude Code also removes the patch.
