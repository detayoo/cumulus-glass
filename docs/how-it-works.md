# How it works

## The theme is only colors

A VS Code color theme can only set colors. `theme/build_theme.py` generates two:

- **Cumulus**: solid deep-sky blues
- **Cumulus Glass**: the same palette with transparent backgrounds for the sidebar, panel, tabs, title bar, status bar and terminal, so the CSS layer can show through

When a theme is active, VS Code adds its id as a class on the workbench. `cumulus-glass.css` scopes every rule to that class, so it only applies while Cumulus Glass is active.

## The glass is faked on purpose

Real blur (`backdrop-filter`) on a large panel breaks VS Code. It changes how fixed-position elements are placed, so menus and suggestion lists inside the editor end up in the wrong spot.

So the big cards don't blur anything. Instead, each card paints a pre-blurred copy of the sky with `background-attachment: fixed`. Every card shows exactly the part of the sky that sits behind it, which looks the same as real frosted glass. A blue tint and a 1px inset highlight on the top edge finish the effect.

Real blur is used only on small floating layers that sit outside the editor's layout: menus, the Command Palette, hovers, suggestions, notifications and the find widget.

## Squircle corners

The corners use the CSS `corner-shape: squircle` property, Apple's continuous curve. VS Code's floating cards get their radius from `--vscode-cornerRadius-large`, which the CSS sets to `--cg-radius-card`. The editor has an extra outer layer with its own radius, so that layer is set to the same shape to keep the sidebar and editor corners identical.

## Images

`build.py` inlines everything into one CSS file as data URIs, so the loader only has to import a single file:

- a softened sky for the window and editor
- a half-size, heavily blurred sky for the cards
- four SVGs from `glass/bubbles.py`

## The companion extension

The `.vsix` contains the two themes and a small extension (`theme/extension.js`). It only matters if you use the [Claude Code patch](claude-code.md). It adds the **Cumulus: Re-apply Claude Code glass** command and re-applies the patch after Claude Code updates.

It does nothing if:

- the theme isn't Cumulus Glass, or
- the patch files aren't installed in `~/.vscode/cumulus/`.
