# AGENTS.md

Instructions for a coding agent (Claude Code, Codex, Cursor and others) helping someone install Cumulus Glass on their own machine. Follow the sections in order for a fresh install. Jump to Troubleshooting, Customizing or Uninstall for anything else.

## What you're installing

Cumulus Glass has three layers. Only the first is a normal VS Code theme.

| Layer | Files | How it loads |
|---|---|---|
| Color themes **Cumulus** and **Cumulus Glass** | `theme/` → `dist/cumulus-theme-<version>.vsix` | Installed as a VS Code extension |
| Glass layer: sky, frosted cards, squircle corners, blur, cloud art | `glass/` → `dist/cumulus-glass.css` | Injected by the third-party **Custom CSS and JS Loader** extension |
| Optional chat panel patch for the Claude Code extension | `extras/chat-panel/` | A shell script that edits that extension's `webview/index.css` |

**Cumulus Glass** (the theme) without the glass layer has transparent backgrounds and looks broken. If the user only wants colors, install the `.vsix`, set **Cumulus**, and stop.

## Ground rules

- **Ask before changing the user's VS Code settings.** Back up `settings.json` first, then merge keys into it. Never replace the file. It's JSONC (comments and trailing commas are allowed), so edit it as text, not with a strict JSON parser that would drop comments.
- **Never apply the chat panel patch unless the user explicitly asks for it.** It modifies another extension's files.
- **Some steps only the user can do.** You can't run Command Palette commands or restart VS Code. Tell the user exactly what to run and wait for them to confirm.
- **Don't edit files inside the VS Code app or other extensions** (apart from the opted-in patch). The loader handles VS Code's files.
- **Don't run `build.py --install` or `install.sh` without saying so first.** It overwrites `~/.vscode/cumulus-glass.css` and `~/.vscode/cumulus/chat-panel-glass.css` and `patch-chat-panel.sh`. That's fine on a fresh install, but it replaces any hand edits the user made to those copies.

## Fast path: the installer (macOS and Linux)

Ask the user for permission to change their VS Code settings, then run:

```sh
curl -fsSL https://raw.githubusercontent.com/detayoo/cumulus-glass/main/install.sh | sh -s -- --yes
```

- It downloads the latest release and installs the theme and the loader.
- It merges the four settings below into `settings.json`, keeps comments, and saves a backup next to it. It restores the file and prints manual steps if anything looks wrong.
- If the user said no to settings changes, use `--no-settings` instead of `--yes` and show them what to add.
- Add `--with-chat-panel` only if the user asked for the chat panel patch.
- If `code` isn't on PATH, set `CUMULUS_CODE` to the full path of the VS Code CLI.

Then skip to [step 5](#5-hand-off-to-the-user). On Windows, or if the installer fails, use the manual steps below.

## Manual install

## 1. Check prerequisites

```sh
python3 --version                    # needs 3.9+
python3 -c "import PIL"              # Pillow; if missing: python3 -m pip install --user pillow
code --version                       # VS Code CLI
```

If `code` isn't found:
- macOS: `"/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"`, or ask the user to run **Shell Command: Install 'code' command in PATH**
- Windows: `code` is usually on PATH after install. Otherwise use `%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd`.

Platform notes:
- macOS and Linux are fully supported.
- On Windows, the theme and glass layer work. The chat panel patch is a POSIX shell script and needs Git Bash or WSL.

## 2. Build

From the repo root:

```sh
python3 build.py --install
```

Expected output:
- `dist/cumulus-glass.css` (about 265 KB)
- `dist/cumulus-theme-<version>.vsix`
- a "Copied ..." line confirming the files went to `~/.vscode/`

## 3. Install the theme and the loader

```sh
code --install-extension dist/cumulus-theme-*.vsix --force
code --install-extension be5invis.vscode-custom-css
```

## 4. Update settings (ask first)

Settings file locations:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Code/User/settings.json` |
| Linux | `~/.config/Code/User/settings.json` |
| Windows | `%APPDATA%\Code\User\settings.json` |

Back the file up, then merge these keys:

```jsonc
"vscode_custom_css.imports": ["file://${userHome}/.vscode/cumulus-glass.css"],
"workbench.colorTheme": "Cumulus Glass",
"workbench.experimental.modernUI": true,
"terminal.integrated.enableImages": true
```

- If `vscode_custom_css.imports` already exists, **append** the Cumulus entry. Don't drop the user's other imports.
- If the user already has a `workbench.colorTheme`, tell them you're changing it and what it was.

## 5. Hand off to the user

Tell the user to:

1. Run **Enable Custom CSS and JS** from the Command Palette.
2. Quit VS Code completely and reopen it. A window reload is not enough.
3. If VS Code says **"Your Code installation appears to be corrupt"**, choose **Don't Show Again**. It's caused by the loader and is harmless.

## 6. Verify with the user

Ask them to confirm they see:

- a sky photo behind the whole window, with clouds
- the sidebar, editor and panel floating as separate blue glass cards with soft squircle corners
- cumulus cloud art at the bottom of an empty editor (close all tabs to check)
- blurred, translucent menus and Command Palette
- no italic text anywhere

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Colors changed but no sky or glass | Loader not enabled, or VS Code only reloaded | Run **Enable Custom CSS and JS**, fully quit and reopen |
| Glass vanished after a VS Code update | The update replaced the files the loader edited | Run **Reload Custom CSS and JS**, fully restart |
| Panels look broken or empty | Cumulus Glass theme active without the glass layer | Enable the loader, or switch to **Cumulus** |
| "Enable Custom CSS and JS" fails with a permission error | Loader can't write to the VS Code install folder | Follow the platform steps in the [loader README](https://github.com/be5invis/vscode-custom-css#getting-started) |
| Corners are round, not squircle | VS Code is too old for CSS `corner-shape` (needs Chromium 139+) | Update VS Code. Everything else still works. |
| Terminal has a solid background | `terminal.integrated.enableImages` is off | Set it to `true` |
| Glass is solid blue | OS **Reduce transparency** is on | Intended fallback. Turn the OS setting off for glass. |

## Optional: chat panel patch (only if asked)

See `docs/chat-panel.md` for what it changes. To apply it:

```sh
~/.vscode/cumulus/patch-chat-panel.sh
```

- It prints `patched: <path>` for each installed version of the extension, and backs each file up once as `index.css.cumulus-backup`.
- A `warning:` line means a class name changed in that extension version. Report it. The selectors in `extras/chat-panel/chat-panel-glass.css` need updating.
- The user must then run **Developer: Reload Window**. Tell them this restarts any running chat session.
- After this, the Cumulus extension re-applies the patch automatically when the chat extension updates, but only while the theme is Cumulus Glass. Manual re-run: **Cumulus: Re-apply chat panel glass**.

## Customizing

All customizing follows the same loop:

1. Edit the file.
2. Run `python3 build.py --install`.
3. The user runs **Reload Custom CSS and JS** and fully restarts.

For color changes, reinstall the `.vsix` instead, and the user reloads the window.

What to edit:

- **Glass strength and corner sizes:** the variables at the top of `glass/cumulus-glass.template.css`. See `docs/customizing.md` for the table.
- **Sky image:** replace `glass/sky.jpg`, about 1700px wide, landscape, mostly blue.
- **Cloud art:** the seeds and positions in `glass/bubbles.py`.
- **Colors:** the palette at the top of `theme/build_theme.py`.

## Uninstall

1. Ask the user to run **Disable Custom CSS and JS**, then fully restart.
2. Run:
   ```sh
   code --uninstall-extension local.cumulus-theme
   ```
   Uninstall `be5invis.vscode-custom-css` too if nothing else uses it.
3. Remove the Cumulus entry from `vscode_custom_css.imports` and set another `workbench.colorTheme`.
4. Delete `~/.vscode/cumulus-glass.css` and `~/.vscode/cumulus/`.
5. If the panel patch was applied, restore the backups as shown in `docs/chat-panel.md`.
