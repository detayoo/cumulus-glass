# Development

Rules for changing the theme itself. For installing it, see [AGENTS.md](../AGENTS.md) or [Setup](setup.md).

## Design rules (keep these)

- **No italics anywhere.** Not in token colors, semantic tokens, tabs, or the chat panel.
- **Blues only for accents.** No orange or pink.
- **Squircle corners** (`corner-shape: squircle`) at roughly 1.8× a normal radius. Smaller squircles look sharper than plain rounded corners, not softer.
- **Sidebar and editor cards use the same radius and shape.** The editor's outer `.part.editor` layer needs `corner-shape` too, or the corners won't match.
- **Cloud art only where no text sits:** the empty editor, the activity bar lane, and the title bar either side of the command center.
- **Icons in the chat panel patch are Hugeicons:** SendHorizontal for send, MagicWand01 for Auto.
- **Readability:** card and editor tints stay at alpha 0.66 or above.

## Technical rules

- **Scope every glass rule under `.monaco-workbench.monaco-workbench[class*="cumulus-glass"]`**, so other themes are never affected.
- **Never put `backdrop-filter` on the workbench, panels or any editor ancestor.** It breaks the positioning of editor menus and suggestions. Big cards fake the frost with a pre-blurred image and `background-attachment: fixed`. Real blur is only for leaf popups.
- **Keep the `prefers-reduced-transparency` fallback in sync** when adding new surfaces.
- **Rebuild with `python3 build.py`.** Never hand-edit files in `dist/`.
- **Version numbers live only in `theme/build_theme.py`.** It appears three times: the `package.json` version, the manifest `Version`, and the `.vsix` filename. Docs use `cumulus-theme-*.vsix` or the release's unversioned `cumulus-theme.vsix`, so they don't need bumping.
- **Update the docs in the same change.** If behavior, settings, file names or steps change, update `README.md`, the matching file in `docs/` and this file, so they never drift from the code.

## Releasing

`install.sh` downloads from the latest GitHub release, so a change reaches users only after a release.

1. Bump the version in `theme/build_theme.py`.
2. Commit and push.
3. Tag and push the tag:
   ```sh
   git tag v1.5.3 && git push origin v1.5.3
   ```

The `Release` workflow (`.github/workflows/release.yml`) checks that the tag matches the version, builds everything, and publishes a release with `cumulus-theme.vsix`, `cumulus-glass.css`, `chat-panel-glass.css` and `patch-chat-panel.sh`.

If you change `install.sh`, test it against a throwaway `HOME`, with `CUMULUS_BASE=file://<folder with the four files>` and `CUMULUS_CODE` pointing at a stub script, so your own setup isn't touched.

## Before you commit

1. `python3 build.py` runs cleanly.
2. Install the `.vsix`, run `build.py --install`, and have the user confirm the change in VS Code in Cumulus Glass. Also check one other theme still looks normal.
3. If the chat panel patch changed, run it against a copy of the extension's `index.css` first and confirm `patched:` with no `warning:`.
