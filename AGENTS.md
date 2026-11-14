# AGENTS.md

Instructions for coding agents (Claude Code, Codex, Cursor and others) helping someone install, customize, remove or develop Cumulus Glass. Follow the sections in order for a fresh install. Jump to the section you need for anything else.

## What you're installing

Cumulus Glass has three layers. Only the first is a normal VS Code theme.

| Layer | Files | How it loads |
|---|---|---|
| Color themes **Cumulus** and **Cumulus Glass** | `theme/` → `dist/cumulus-theme-<version>.vsix` | Installed as a VS Code extension |
| Glass layer: sky, frosted cards, squircle corners, blur, cloud art | `glass/` → `dist/cumulus-glass.css` | Injected by the third-party **Custom CSS and JS Loader** extension |
| Optional chat panel patch for the Claude Code extension | `claude-code/` | A shell script that edits that extension's `webview/index.css` |

**Cumulus Glass** (the theme) without the glass layer has transparent backgrounds and looks broken. If the user only wants colors, install the `.vsix`, set **Cumulus**, and stop.

## Ground rules

- **Ask before changing the user's VS Code settings.** Back up `settings.json` first, then merge keys into it. Never replace the file. It's JSONC (comments and trailing commas are allowed), so edit it as text, not with a strict JSON parser that would drop comments.
- **Never apply the chat panel patch unless the user explicitly asks for it.** It modifies another extension's files.
- **Some steps only the user can do.** You can't run Command Palette commands or restart VS Code. Tell the user exactly what to run and wait for them to confirm.
- **Don't edit files inside the VS Code app or other extensions** (apart from the opted-in patch). The loader handles VS Code's files.
- **Don't run `build.py --install` without saying so first.** It overwrites `~/.vscode/cumulus-glass.css` and `~/.vscode/cumulus/claude-code-glass.css` and `patch-claude-code.sh`. That's fine on a fresh install, but it replaces any hand edits the user made to those copies.

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
code --install-extension dist/cumulus-theme-<version>.vsix --force
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

See `docs/claude-code.md` for what it changes. To apply it:

```sh
~/.vscode/cumulus/patch-claude-code.sh
```

- It prints `patched: <path>` for each installed version of the extension, and backs each file up once as `index.css.cumulus-backup`.
- A `warning:` line means a class name changed in that extension version. Report it. The selectors in `claude-code/claude-code-glass.css` need updating.
- The user must then run **Developer: Reload Window**. Tell them this restarts any running chat session.
- After this, the Cumulus extension re-applies the patch automatically when the chat extension updates, but only while the theme is Cumulus Glass. Manual re-run: **Cumulus: Re-apply Claude Code glass**.

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
5. If the panel patch was applied, restore the backups as shown in `docs/claude-code.md`.

## Developing the theme

Follow these if you're changing the theme itself, not just installing it.

### Design rules (keep these)

- **No italics anywhere.** Not in token colors, semantic tokens, tabs, or the chat panel.
- **Blues only for accents.** No orange or pink.
- **Squircle corners** (`corner-shape: squircle`) at roughly 1.8× a normal radius. Smaller squircles look sharper than plain rounded corners, not softer.
- **Sidebar and editor cards use the same radius and shape.** The editor's outer `.part.editor` layer needs `corner-shape` too, or the corners won't match.
- **Cloud art only where no text sits:** the empty editor, the activity bar lane, and the title bar either side of the command center.
- **Icons in the chat panel patch are Hugeicons:** SendHorizontal for send, MagicWand01 for Auto.
- **Readability:** card and editor tints stay at alpha 0.66 or above.

### Technical rules

- **Scope every glass rule under `.monaco-workbench.monaco-workbench[class*="cumulus-glass"]`**, so other themes are never affected.
- **Never put `backdrop-filter` on the workbench, panels or any editor ancestor.** It breaks the positioning of editor menus and suggestions. Big cards fake the frost with a pre-blurred image and `background-attachment: fixed`. Real blur is only for leaf popups.
- **Keep the `prefers-reduced-transparency` fallback in sync** when adding new surfaces.
- **Rebuild with `python3 build.py`.** Never hand-edit files in `dist/`.
- **To release a version,** bump it in `theme/build_theme.py`. It appears three times: `package.json` version, the manifest `Version`, and the `.vsix` filename. Then update the version in `README.md`, `docs/setup.md` and the install commands here.
- **Update the docs in the same change.** If behavior, settings, file names or steps change, update `README.md`, the matching file in `docs/` and this file, so they never drift from the code.

### Before you commit

1. `python3 build.py` runs cleanly.
2. Install the `.vsix`, run `build.py --install`, and have the user confirm the change in VS Code in Cumulus Glass. Also check one other theme still looks normal.
3. If the chat panel patch changed, run it against a copy of the extension's `index.css` first and confirm `patched:` with no `warning:`.
