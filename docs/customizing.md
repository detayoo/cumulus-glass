# Customizing

All changes follow the same loop:

1. Edit a file.
2. Run `python3 build.py --install`.
3. In VS Code, run **Reload Custom CSS and JS** and restart.

## Glass strength and corners

The variables at the top of `glass/cumulus-glass.template.css` control the look:

| Variable | Default | What it does |
|---|---|---|
| `--cg-tint-editor` | `rgba(4, 30, 94, 0.72)` | Blue tint over the sky behind the editor. Lower alpha shows more sky but less contrast. Keep it at 0.66 or above so code stays readable. |
| `--cg-tint-card` | `rgba(2, 28, 100, 0.72)` | Tint for the sidebar, panel and activity bar cards. |
| `--cg-tint-popup` | `rgba(12, 48, 112, 0.52)` | Tint for menus, the Command Palette, hovers and notifications. These also get a real backdrop blur. |
| `--cg-radius-card` | `36px` | Corner radius of the floating cards. |
| `--cg-radius-popup` | `32px` | Command Palette and notifications. |
| `--cg-radius-menu` | `24px` | Menus, suggestions, hovers, find widget. |
| `--cg-radius-control` | `16px` | Buttons, inputs, tabs, activity bar chips. |
| `--cg-radius-row` | `12px` | List rows. |
| `--cg-edge` | `rgba(210, 232, 255, 0.16)` | The thin card edge. |

The radii are large on purpose. A squircle curves more gradually than a normal rounded corner, so at the same radius it looks sharper. Roughly 1.8 times the radius you'd normally use reads right.

## Your own sky

Replace `glass/sky.jpg` with any landscape image, around 1700px wide. `build.py` makes the softened version for the editor and the heavily blurred "frost" version for the cards from it.

Skies with dark-blue areas work best. The tints assume a blue background, so a very bright or warm image will lower text contrast. Raise the tint alpha if that happens.

## Cloud art

`glass/bubbles.py` draws the cloud art as SVG: the cumulus mounds in the empty editor, the trail in the activity bar, and the puffs either side of the title bar. Each piece uses a fixed random seed, so builds are repeatable. Change a seed or the positions near the bottom of the file to get different clouds.

The art is only placed where no text sits. If you move it, keep it out of areas that show code or labels.

## Colors and syntax

`theme/build_theme.py` defines the palette at the top and generates both color themes from it. Rebuild, then reinstall the `.vsix` and reload the window to see color changes.

The themes deliberately have no italics, including in comments and semantic highlighting.
