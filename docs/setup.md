# Setup

This turns on the full Cumulus Glass look. If you only want the color theme, install `cumulus-theme.vsix` from the [latest release](https://github.com/detayoo/cumulus-glass/releases/latest) and choose **Cumulus**. You can skip the rest.

## Quick install (macOS and Linux)

```sh
curl -fsSL https://raw.githubusercontent.com/detayoo/cumulus-glass/main/install.sh | sh
```

This does steps 1 to 3 below for you. It asks before touching your settings and keeps a backup. Then do [step 4](#4-enable-it-and-restart).

## Manual install (Windows, or building from source)

## 1. Build and install the files

You need Python 3.9 or newer and Pillow (`pip install pillow`).

```sh
git clone https://github.com/detayoo/cumulus-glass.git
cd cumulus-glass
python3 build.py --install
code --install-extension dist/cumulus-theme-*.vsix
```

On Windows, use `code --install-extension` with the full file name from `dist\`.

`--install` copies:

- `dist/cumulus-glass.css` to `~/.vscode/cumulus-glass.css`
- the chat panel patch files to `~/.vscode/cumulus/`. They're unused unless you [opt in](chat-panel.md).

If `code` isn't on your PATH, run **Shell Command: Install 'code' command in PATH** from the Command Palette. You can also drag the `.vsix` onto the Extensions view.

## 2. Install the Custom CSS and JS Loader

Install [Custom CSS and JS Loader](https://marketplace.visualstudio.com/items?itemName=be5invis.vscode-custom-css) (`be5invis.vscode-custom-css`) from the Extensions view.

## 3. Add these settings

Open **Preferences: Open User Settings (JSON)** and add:

```jsonc
{
  "vscode_custom_css.imports": ["file://${userHome}/.vscode/cumulus-glass.css"],
  "workbench.colorTheme": "Cumulus Glass",
  "workbench.experimental.modernUI": true,
  "terminal.integrated.enableImages": true
}
```

- `vscode_custom_css.imports` loads the glass layer. If you already have imports, add this one to the list.
- `workbench.experimental.modernUI` makes the sidebar, editor and panel float as separate cards. Recent VS Code versions turn it on by default.
- `terminal.integrated.enableImages` lets the terminal be transparent so the glass shows through.

## 4. Enable it and restart

1. Run **Enable Custom CSS and JS** from the Command Palette.
2. Quit VS Code completely (Cmd+Q / Alt+F4) and open it again. A window reload isn't enough.

You may see **"Your Code installation appears to be corrupt."** That's expected. The loader works by editing VS Code's own files, and VS Code notices. Click the gear and choose **Don't Show Again**.

On some systems the loader needs write access to the VS Code install folder. If enabling fails, see the [loader's README](https://github.com/be5invis/vscode-custom-css#getting-started) for your platform.

## After a VS Code update

VS Code updates replace the files the loader edited, so the glass disappears. Run **Reload Custom CSS and JS**, then fully restart VS Code.

## After you change the CSS

Edit `glass/cumulus-glass.template.css`, then run `python3 build.py --install`. In VS Code, run **Reload Custom CSS and JS** and restart.

## Turning it off

- Switch to another theme. The glass CSS only applies while **Cumulus Glass** is active, so other themes are unaffected.
- To remove it completely, run **Disable Custom CSS and JS** and restart.

## Requirements

- A recent VS Code. Squircle corners use the CSS `corner-shape` property, which needs Chromium 139 or newer inside VS Code. Older versions show ordinary rounded corners, and everything else works.
- Your OS's **Reduce transparency** setting is respected: Cumulus Glass falls back to solid blue panels with the same shapes.
