#!/bin/sh
# Cumulus Glass installer for macOS and Linux.
#
#   curl -fsSL https://raw.githubusercontent.com/detayoo/cumulus-glass/main/install.sh | sh
#
# Options (after "sh -s --" when piping):
#   --yes             change VS Code settings without asking
#   --no-settings     leave VS Code settings alone and print what to add
#   --with-chat-panel also apply the optional Claude Code chat panel patch
#
# Environment overrides: CUMULUS_CODE (path to the VS Code CLI), CUMULUS_BASE (where to download files from).

set -eu

BASE="${CUMULUS_BASE:-https://github.com/detayoo/cumulus-glass/releases/latest/download}"
ASSUME_YES=0
SETTINGS=1
CHAT_PANEL=0
for arg in "$@"; do
  case "$arg" in
    --yes|-y) ASSUME_YES=1 ;;
    --no-settings) SETTINGS=0 ;;
    --with-chat-panel) CHAT_PANEL=1 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

say() { printf '%s\n' "$*"; }
step() { printf '\n==> %s\n' "$*"; }
fail() { printf '\nError: %s\n' "$*" >&2; exit 1; }

case "$(uname -s)" in
  Darwin) SETTINGS_FILE="$HOME/Library/Application Support/Code/User/settings.json" ;;
  Linux) SETTINGS_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/Code/User/settings.json" ;;
  *) fail "This installer supports macOS and Linux. On Windows, follow docs/setup.md." ;;
esac

if [ -n "${CUMULUS_CODE:-}" ]; then
  CODE="$CUMULUS_CODE"
elif command -v code >/dev/null 2>&1; then
  CODE="code"
elif [ -x "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" ]; then
  CODE="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
else
  fail "Couldn't find VS Code's 'code' command. In VS Code, run 'Shell Command: Install code command in PATH', then run this again."
fi
command -v curl >/dev/null 2>&1 || fail "curl is required."

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

step "Downloading Cumulus Glass"
for f in cumulus-theme.vsix cumulus-glass.css chat-panel-glass.css patch-chat-panel.sh; do
  curl -fsSL "$BASE/$f" -o "$TMP/$f" || fail "Couldn't download $f from $BASE"
done

step "Installing files into ~/.vscode"
mkdir -p "$HOME/.vscode/cumulus"
cp "$TMP/cumulus-glass.css" "$HOME/.vscode/cumulus-glass.css"
cp "$TMP/chat-panel-glass.css" "$TMP/patch-chat-panel.sh" "$HOME/.vscode/cumulus/"
chmod +x "$HOME/.vscode/cumulus/patch-chat-panel.sh"
say "~/.vscode/cumulus-glass.css"

step "Installing the theme and the Custom CSS and JS Loader"
"$CODE" --install-extension "$TMP/cumulus-theme.vsix" --force >/dev/null 2>&1 || fail "Couldn't install the Cumulus theme extension."
"$CODE" --install-extension be5invis.vscode-custom-css >/dev/null 2>&1 || fail "Couldn't install be5invis.vscode-custom-css."
say "Installed Cumulus and Custom CSS and JS Loader"

manual_settings() {
  cat <<'EOF'

Add these to your VS Code settings (Preferences: Open User Settings (JSON)):

  "vscode_custom_css.imports": ["file://${userHome}/.vscode/cumulus-glass.css"],
  "workbench.colorTheme": "Cumulus Glass",
  "workbench.experimental.modernUI": true,
  "terminal.integrated.enableImages": true

If you already have vscode_custom_css.imports, add the Cumulus entry to that list.
EOF
}

if [ "$SETTINGS" -eq 1 ] && [ "$ASSUME_YES" -eq 0 ]; then
  if [ -r /dev/tty ] && { exec 3</dev/tty; } 2>/dev/null; then
    printf '\nUpdate your VS Code settings to turn on Cumulus Glass? A backup is made first. [Y/n] '
    read -r answer <&3 || answer=""
    exec 3<&-
    case "$answer" in [nN]*) SETTINGS=0 ;; esac
  else
    say "No terminal to ask in, so your settings were left alone. Re-run with --yes to update them."
    SETTINGS=0
  fi
fi

if [ "$SETTINGS" -eq 1 ]; then
  step "Updating VS Code settings"
  if ! command -v python3 >/dev/null 2>&1 || ! python3 -c "" >/dev/null 2>&1; then
    say "python3 isn't available, so settings weren't changed automatically."
    manual_settings
  else
    mkdir -p "$(dirname "$SETTINGS_FILE")"
    [ -f "$SETTINGS_FILE" ] || printf '{}\n' > "$SETTINGS_FILE"
    BACKUP="$SETTINGS_FILE.cumulus-backup-$(date +%Y%m%d%H%M%S)"
    cp "$SETTINGS_FILE" "$BACKUP"
    if python3 - "$SETTINGS_FILE" <<'PY'
import json, re, sys

sys.excepthook = lambda kind, err, tb: print(f"settings.json couldn't be read or updated: {err}", file=sys.stderr)
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
ENTRY = "file://${userHome}/.vscode/cumulus-glass.css"


def strip_jsonc(s):
    out, i, n, in_str = [], 0, len(s), False
    while i < n:
        c = s[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(s[i + 1])
                i += 1
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
            out.append(c)
        elif s.startswith("//", i):
            while i < n and s[i] != "\n":
                i += 1
            continue
        elif s.startswith("/*", i):
            end = s.find("*/", i + 2)
            i = n if end < 0 else end + 2
            continue
        else:
            out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def parse(s):
    data = json.loads(strip_jsonc(s) or "{}")
    if not isinstance(data, dict):
        raise ValueError("settings.json is not an object")
    return data


before = parse(text)


def set_scalar(t, key, literal):
    pattern = re.compile(r'("' + re.escape(key) + r'"\s*:\s*)(true|false|null|-?\d+(?:\.\d+)?|"(?:[^"\\]|\\.)*")')
    if key in before:
        new, count = pattern.subn(lambda m: m.group(1) + literal, t, count=1)
        if count:
            return new, True
    return t, False


def add_key(t, key, literal):
    end = t.rfind("}")
    head = t[:end]
    stripped = strip_jsonc(head).rstrip()
    sep = "" if stripped.endswith("{") or stripped.endswith(",") else ","
    head = head.rstrip()
    return head + sep + "\n  " + json.dumps(key) + ": " + literal + "\n" + t[end:]


changes = []
imports = before.get("vscode_custom_css.imports")
if isinstance(imports, list) and any("cumulus-glass.css" in str(x) for x in imports):
    pass
elif isinstance(imports, list):
    m = re.search(r'("vscode_custom_css\.imports"\s*:\s*\[)', text)
    if not m:
        raise ValueError("couldn't find vscode_custom_css.imports")
    sep = "" if not imports else ", "
    text = text[: m.end()] + json.dumps(ENTRY) + sep + text[m.end():]
    changes.append("added Cumulus to vscode_custom_css.imports")
else:
    text = add_key(text, "vscode_custom_css.imports", json.dumps([ENTRY]))
    changes.append("set vscode_custom_css.imports")

for key, value in (
    ("workbench.colorTheme", "Cumulus Glass"),
    ("workbench.experimental.modernUI", True),
    ("terminal.integrated.enableImages", True),
):
    if before.get(key) == value:
        continue
    literal = json.dumps(value)
    text, done = set_scalar(text, key, literal)
    if not done:
        text = add_key(text, key, literal)
    old = before.get(key)
    changes.append(f"{key}: {json.dumps(old)} -> {literal}" if key in before else f"set {key}")

after = parse(text)
assert any("cumulus-glass.css" in str(x) for x in after["vscode_custom_css.imports"])
assert after["workbench.colorTheme"] == "Cumulus Glass"
assert after["workbench.experimental.modernUI"] is True
assert after["terminal.integrated.enableImages"] is True
for k, v in before.items():
    if k not in ("vscode_custom_css.imports", "workbench.colorTheme", "workbench.experimental.modernUI", "terminal.integrated.enableImages"):
        assert after.get(k) == v, k

open(path, "w", encoding="utf-8").write(text)
for c in changes or ["already set up"]:
    print(c)
PY
    then
      if cmp -s "$BACKUP" "$SETTINGS_FILE"; then rm -f "$BACKUP"; else say "Backup: $BACKUP"; fi
    else
      cp "$BACKUP" "$SETTINGS_FILE"
      rm -f "$BACKUP"
      say "Couldn't update settings safely, so they were left unchanged."
      manual_settings
    fi
  fi
else
  manual_settings
fi

if [ "$CHAT_PANEL" -eq 1 ]; then
  step "Applying the chat panel patch"
  "$HOME/.vscode/cumulus/patch-chat-panel.sh"
fi

cat <<'EOF'

==> Almost done. Two steps only you can do, inside VS Code:

  1. Open the Command Palette and run "Enable Custom CSS and JS".
  2. Quit VS Code completely and open it again (a window reload isn't enough).

If VS Code then says "Your Code installation appears to be corrupt", choose
"Don't Show Again". It's caused by the CSS loader and is harmless.

After a VS Code update, run "Reload Custom CSS and JS" and restart.
EOF
