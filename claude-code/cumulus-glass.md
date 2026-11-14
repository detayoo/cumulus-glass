---
description: Re-apply the Cumulus Glass styling to the Claude Code panel (use after a Claude Code update)
allowed-tools: Bash(~/.vscode/cumulus/patch-claude-code.sh)
---
The Cumulus Glass patch script was just run. Its output:

!`~/.vscode/cumulus/patch-claude-code.sh`

Report the result to the user in one or two short sentences:
- If it says "patched", tell them it's done and that they need to run "Developer: Reload Window" to see it. Warn that reloading restarts this Claude Code panel, so they should do it when nothing is running.
- If any line starts with "warning:", say which class name wasn't found and that the input-box styling may need updating for this Claude Code version. Offer to fix it.
- If there's an error or no output, say what went wrong. Don't retry on your own.

Do not run any other commands.
