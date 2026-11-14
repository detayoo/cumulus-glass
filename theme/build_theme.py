import json, os, sys, zipfile

out = sys.argv[1]
ext = os.path.join(out, "extension")
os.makedirs(os.path.join(ext, "themes"), exist_ok=True)

# Palette sampled from the reference: deep zenith blue -> horizon cerulean, sunlit cream clouds
P = {
    "zenith":   "#06245c",  # deepest sky, chrome
    "sky":      "#0a2d6b",  # editor
    "sky2":     "#0d3578",  # raised surfaces
    "sky3":     "#13428e",  # selection / hover
    "line":     "#1a4a94",  # borders
    "line2":    "#25599f",
    "horizon":  "#2f8fe0",  # accent
    "horizon2": "#5cb6f2",
    "cloud":    "#f4f1dc",  # main text, sunlit cream
    "shade":    "#b9d3ea",  # cloud shadow
    "mist":     "#7fa3cf",  # muted
    "haze":     "#5878a8",  # comments / disabled
    "sun":      "#ffe9a3",
    "peach":    "#ffc7a1",
    "mint":     "#9ee8d6",
    "ice":      "#cfeaff",
    "cyan":     "#7fd6ff",
    "rose":     "#ff9fb2",
    "lilac":    "#c7b8ff",
}
c = P

colors = {
    "foreground": c["cloud"],
    "descriptionForeground": c["mist"],
    "disabledForeground": c["haze"],
    "errorForeground": c["rose"],
    "focusBorder": c["horizon"],
    "selection.background": c["horizon"] + "66",
    "icon.foreground": c["shade"],
    "widget.border": c["line"],
    "widget.shadow": "#00000000",
    "scrollbar.shadow": "#00000000",
    "sash.hoverBorder": c["horizon"],
    "progressBar.background": c["horizon2"],

    "titleBar.activeBackground": c["zenith"],
    "titleBar.inactiveBackground": c["zenith"],
    "titleBar.activeForeground": c["shade"],
    "titleBar.inactiveForeground": c["mist"],
    "titleBar.border": c["line"],
    "commandCenter.background": c["sky"],
    "commandCenter.border": c["line"],
    "commandCenter.foreground": c["shade"],
    "commandCenter.activeBackground": c["sky2"],

    "activityBar.background": c["zenith"],
    "activityBar.foreground": c["cloud"],
    "activityBar.inactiveForeground": c["mist"],
    "activityBar.border": c["line"],
    "activityBar.activeBorder": c["horizon2"],
    "activityBarBadge.background": c["horizon"],
    "activityBarBadge.foreground": "#ffffff",
    "activityBarTop.foreground": c["cloud"],
    "activityBarTop.inactiveForeground": c["mist"],
    "activityBarTop.activeBorder": c["horizon2"],

    "sideBar.background": c["zenith"],
    "sideBar.foreground": c["shade"],
    "sideBar.border": c["line"],
    "sideBarTitle.foreground": c["cloud"],
    "sideBarSectionHeader.background": c["zenith"],
    "sideBarSectionHeader.foreground": c["cloud"],
    "sideBarSectionHeader.border": c["line"],
    "sideBarActivityBarTop.border": c["line"],

    "list.hoverBackground": c["sky2"],
    "list.hoverForeground": c["cloud"],
    "list.activeSelectionBackground": c["sky3"],
    "list.activeSelectionForeground": "#ffffff",
    "list.inactiveSelectionBackground": c["sky2"],
    "list.inactiveSelectionForeground": c["cloud"],
    "list.focusOutline": c["horizon"],
    "list.highlightForeground": c["sun"],
    "list.focusHighlightForeground": c["sun"],
    "list.errorForeground": c["rose"],
    "list.warningForeground": c["sun"],
    "list.dropBackground": c["horizon"] + "33",
    "tree.indentGuidesStroke": c["line2"],
    "tree.inactiveIndentGuidesStroke": c["line"],

    "editor.background": c["sky"],
    "editor.foreground": c["cloud"],
    "editorLineNumber.foreground": c["haze"],
    "editorLineNumber.activeForeground": c["cloud"],
    "editorCursor.foreground": c["sun"],
    "editor.lineHighlightBackground": "#ffffff0a",
    "editor.lineHighlightBorder": "#00000000",
    "editor.selectionBackground": c["horizon"] + "55",
    "editor.inactiveSelectionBackground": c["horizon"] + "30",
    "editor.selectionHighlightBackground": c["horizon2"] + "26",
    "editor.wordHighlightBackground": c["horizon2"] + "26",
    "editor.wordHighlightStrongBackground": c["sun"] + "22",
    "editor.findMatchBackground": c["sun"] + "55",
    "editor.findMatchHighlightBackground": c["sun"] + "26",
    "editor.findRangeHighlightBackground": "#ffffff0d",
    "editor.rangeHighlightBackground": "#ffffff0d",
    "editorBracketMatch.background": c["horizon"] + "40",
    "editorBracketMatch.border": c["horizon2"],
    "editorIndentGuide.background1": c["line"],
    "editorIndentGuide.activeBackground1": c["line2"],
    "editorWhitespace.foreground": c["line2"],
    "editorRuler.foreground": c["line"],
    "editorCodeLens.foreground": c["haze"],
    "editorInlayHint.background": c["sky2"],
    "editorInlayHint.foreground": c["mist"],
    "editorLink.activeForeground": c["horizon2"],
    "editorBracketHighlight.foreground1": c["sun"],
    "editorBracketHighlight.foreground2": c["cyan"],
    "editorBracketHighlight.foreground3": c["lilac"],
    "editorBracketHighlight.foreground4": c["mint"],
    "editorBracketHighlight.foreground5": c["peach"],
    "editorBracketHighlight.foreground6": c["ice"],
    "editorError.foreground": c["rose"],
    "editorWarning.foreground": c["sun"],
    "editorInfo.foreground": c["cyan"],
    "editorHint.foreground": c["mint"],
    "editorGutter.addedBackground": c["mint"],
    "editorGutter.modifiedBackground": c["horizon2"],
    "editorGutter.deletedBackground": c["rose"],
    "editorOverviewRuler.border": "#00000000",
    "editorStickyScroll.background": c["sky"],
    "editorStickyScrollHover.background": c["sky2"],
    "editorStickyScroll.border": c["line"],

    "editorGroup.border": c["line"],
    "editorGroupHeader.tabsBackground": c["zenith"],
    "editorGroupHeader.tabsBorder": c["line"],
    "editorGroupHeader.noTabsBackground": c["sky"],
    "tab.activeBackground": c["sky"],
    "tab.activeForeground": c["cloud"],
    "tab.inactiveBackground": c["zenith"],
    "tab.inactiveForeground": c["mist"],
    "tab.hoverBackground": c["sky2"],
    "tab.border": c["line"],
    "tab.activeBorder": c["sky"],
    "tab.activeBorderTop": c["horizon2"],
    "tab.unfocusedActiveBorderTop": c["line2"],
    "tab.activeModifiedBorder": c["sun"],
    "breadcrumb.background": c["sky"],
    "breadcrumb.foreground": c["mist"],
    "breadcrumb.focusForeground": c["cloud"],
    "breadcrumb.activeSelectionForeground": c["cloud"],

    "editorWidget.background": c["sky2"],
    "editorWidget.border": c["line2"],
    "editorWidget.foreground": c["cloud"],
    "editorSuggestWidget.background": c["sky2"],
    "editorSuggestWidget.border": c["line2"],
    "editorSuggestWidget.selectedBackground": c["sky3"],
    "editorSuggestWidget.highlightForeground": c["sun"],
    "editorSuggestWidget.focusHighlightForeground": c["sun"],
    "editorHoverWidget.background": c["sky2"],
    "editorHoverWidget.border": c["line2"],
    "editorHoverWidget.foreground": c["cloud"],
    "quickInput.background": c["sky2"],
    "quickInput.foreground": c["cloud"],
    "quickInputList.focusBackground": c["sky3"],
    "quickInputTitle.background": c["sky3"],
    "pickerGroup.foreground": c["horizon2"],
    "pickerGroup.border": c["line2"],
    "peekView.border": c["horizon"],
    "peekViewEditor.background": c["zenith"],
    "peekViewResult.background": c["sky2"],
    "peekViewTitle.background": c["sky2"],
    "peekViewEditor.matchHighlightBackground": c["sun"] + "40",
    "peekViewResult.matchHighlightBackground": c["sun"] + "40",

    "input.background": c["sky"],
    "input.foreground": c["cloud"],
    "input.border": c["line2"],
    "input.placeholderForeground": c["haze"],
    "inputOption.activeBorder": c["horizon2"],
    "inputOption.activeBackground": c["horizon"] + "40",
    "inputValidation.errorBorder": c["rose"],
    "inputValidation.errorBackground": c["sky2"],
    "inputValidation.warningBorder": c["sun"],
    "inputValidation.warningBackground": c["sky2"],
    "inputValidation.infoBorder": c["cyan"],
    "inputValidation.infoBackground": c["sky2"],
    "inlineChatInput.border": c["line2"],
    "dropdown.background": c["sky2"],
    "dropdown.listBackground": c["sky2"],
    "dropdown.border": c["line2"],
    "dropdown.foreground": c["cloud"],
    "checkbox.background": c["sky"],
    "checkbox.border": c["line2"],
    "checkbox.foreground": c["cloud"],

    "button.background": c["horizon"],
    "button.foreground": "#ffffff",
    "button.hoverBackground": c["horizon2"],
    "button.border": "#00000000",
    "button.secondaryBackground": c["sky3"],
    "button.secondaryForeground": c["cloud"],
    "button.secondaryHoverBackground": c["line2"],
    "badge.background": c["horizon"],
    "badge.foreground": "#ffffff",
    "toolbar.hoverBackground": "#ffffff14",
    "toolbar.activeBackground": "#ffffff1f",
    "textLink.foreground": c["horizon2"],
    "textLink.activeForeground": c["ice"],
    "textCodeBlock.background": c["zenith"],
    "textPreformat.background": c["zenith"],
    "textPreformat.foreground": c["sun"],
    "textBlockQuote.background": c["sky2"],
    "textBlockQuote.border": c["horizon"],
    "textSeparator.foreground": c["line2"],

    "menu.background": c["sky2"],
    "menu.foreground": c["cloud"],
    "menu.border": c["line2"],
    "menu.selectionBackground": c["sky3"],
    "menu.selectionForeground": "#ffffff",
    "menu.separatorBackground": c["line2"],
    "menubar.selectionBackground": c["sky2"],

    "panel.background": c["zenith"],
    "panel.border": c["line"],
    "panelTitle.activeForeground": c["cloud"],
    "panelTitle.inactiveForeground": c["mist"],
    "panelTitle.activeBorder": c["horizon2"],
    "panelSectionHeader.background": c["zenith"],
    "panelInput.border": c["line2"],
    "terminal.background": "#00000000",
    "terminal.foreground": c["cloud"],
    "terminalCursor.foreground": c["sun"],
    "terminal.selectionBackground": c["horizon"] + "55",
    "terminal.border": c["line"],
    "terminal.ansiBlack": "#0a1f45",
    "terminal.ansiRed": c["rose"],
    "terminal.ansiGreen": c["mint"],
    "terminal.ansiYellow": c["sun"],
    "terminal.ansiBlue": c["horizon2"],
    "terminal.ansiMagenta": c["lilac"],
    "terminal.ansiCyan": c["cyan"],
    "terminal.ansiWhite": c["shade"],
    "terminal.ansiBrightBlack": c["haze"],
    "terminal.ansiBrightRed": "#ffbfcb",
    "terminal.ansiBrightGreen": "#c4f5e8",
    "terminal.ansiBrightYellow": "#fff3c9",
    "terminal.ansiBrightBlue": "#9ad3ff",
    "terminal.ansiBrightMagenta": "#ddd3ff",
    "terminal.ansiBrightCyan": c["ice"],
    "terminal.ansiBrightWhite": "#ffffff",

    "statusBar.background": c["zenith"],
    "statusBar.foreground": c["shade"],
    "statusBar.border": c["line"],
    "statusBar.noFolderBackground": c["zenith"],
    "statusBar.debuggingBackground": c["horizon"],
    "statusBar.debuggingForeground": "#ffffff",
    "statusBarItem.hoverBackground": "#ffffff14",
    "statusBarItem.remoteBackground": c["horizon"],
    "statusBarItem.remoteForeground": "#ffffff",
    "statusBarItem.prominentBackground": c["sky3"],

    "notifications.background": c["sky2"],
    "notifications.foreground": c["cloud"],
    "notifications.border": c["line2"],
    "notificationCenterHeader.background": c["sky3"],
    "notificationToast.border": c["line2"],
    "notificationsErrorIcon.foreground": c["rose"],
    "notificationsWarningIcon.foreground": c["sun"],
    "notificationsInfoIcon.foreground": c["cyan"],

    "scrollbarSlider.background": c["shade"] + "1f",
    "scrollbarSlider.hoverBackground": c["shade"] + "33",
    "scrollbarSlider.activeBackground": c["shade"] + "4d",
    "minimap.background": "#00000000",
    "minimap.selectionHighlight": c["horizon"] + "80",
    "minimapSlider.background": c["shade"] + "14",

    "gitDecoration.addedResourceForeground": c["mint"],
    "gitDecoration.untrackedResourceForeground": c["mint"],
    "gitDecoration.modifiedResourceForeground": c["horizon2"],
    "gitDecoration.deletedResourceForeground": c["rose"],
    "gitDecoration.conflictingResourceForeground": c["peach"],
    "gitDecoration.ignoredResourceForeground": c["haze"],
    "diffEditor.insertedTextBackground": c["mint"] + "22",
    "diffEditor.removedTextBackground": c["rose"] + "22",
    "diffEditor.insertedLineBackground": c["mint"] + "14",
    "diffEditor.removedLineBackground": c["rose"] + "14",

    "debugToolBar.background": c["sky2"],
    "welcomePage.tileBackground": c["sky2"],
    "welcomePage.tileHoverBackground": c["sky3"],
    "walkThrough.embeddedEditorBackground": c["zenith"],
    "settings.headerForeground": c["cloud"],
    "settings.modifiedItemIndicator": c["horizon2"],
    "keybindingLabel.background": c["sky3"],
    "keybindingLabel.foreground": c["cloud"],
    "keybindingLabel.border": c["line2"],
    "keybindingLabel.bottomBorder": c["line2"],
    "chat.requestBackground": c["sky2"],
    "chat.requestBorder": c["line2"],
    "chat.slashCommandBackground": c["horizon"] + "40",
    "chat.slashCommandForeground": c["ice"],
}

def tc(scope, fg, style=None):
    s = {"foreground": fg}
    if style is not None:
        s["fontStyle"] = style
    return {"scope": scope, "settings": s}

tokens = [
    tc(["comment", "punctuation.definition.comment", "string.comment"], "#8eaad6", "italic"),
    tc(["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new", "keyword.operator.expression", "keyword.operator.logical.python"], c["cyan"]),
    tc(["keyword.control.import", "keyword.control.export", "keyword.control.from", "keyword.control.flow", "keyword.control.return"], c["lilac"], "italic"),
    tc(["keyword.operator", "punctuation.separator", "punctuation.terminator", "punctuation.accessor"], c["shade"]),
    tc(["punctuation", "meta.brace", "punctuation.definition.tag"], c["mist"]),
    tc(["string", "string.template", "punctuation.definition.string"], c["sun"]),
    tc(["constant.character.escape", "string.regexp"], c["peach"]),
    tc(["punctuation.definition.template-expression", "punctuation.section.embedded"], c["horizon2"]),
    tc(["constant.numeric", "constant.language", "constant.language.boolean", "constant.language.null", "support.constant"], c["peach"]),
    tc(["variable.other.constant", "variable.other.enummember"], c["peach"]),
    tc(["variable", "meta.definition.variable", "variable.other.readwrite"], c["cloud"]),
    tc(["variable.parameter", "meta.parameter"], c["ice"], "italic"),
    tc(["variable.language.this", "variable.language.self", "variable.language.super"], c["lilac"], "italic"),
    tc(["entity.name.function", "support.function", "meta.function-call entity.name.function", "variable.function"], "#ffffff"),
    tc(["entity.name.type", "entity.name.class", "support.class", "support.type", "entity.other.inherited-class", "entity.name.type.interface", "entity.name.namespace"], c["mint"]),
    tc(["variable.other.property", "variable.other.object.property", "support.variable.property", "meta.object-literal.key", "support.type.property-name"], c["shade"]),
    tc(["entity.name.tag", "support.class.component"], c["horizon2"]),
    tc(["entity.name.tag.tsx support.class.component", "entity.name.tag.jsx support.class.component"], c["mint"]),
    tc(["entity.other.attribute-name"], c["cyan"], "italic"),
    tc(["entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css", "entity.name.tag.css"], c["horizon2"]),
    tc(["support.type.property-name.css", "support.type.vendored.property-name.css"], c["shade"]),
    tc(["support.constant.property-value.css", "keyword.other.unit"], c["peach"]),
    tc(["entity.name.function.decorator", "meta.decorator", "punctuation.decorator"], c["lilac"]),
    tc(["markup.heading", "entity.name.section"], c["horizon2"], "bold"),
    tc(["markup.bold"], c["cloud"], "bold"),
    tc(["markup.italic"], c["cloud"], "italic"),
    tc(["markup.inline.raw", "markup.fenced_code"], c["sun"]),
    tc(["markup.underline.link", "string.other.link"], c["cyan"]),
    tc(["markup.list punctuation.definition.list"], c["horizon2"]),
    tc(["markup.quote"], c["mist"], "italic"),
    tc(["markup.inserted"], c["mint"]),
    tc(["markup.deleted"], c["rose"]),
    tc(["markup.changed"], c["horizon2"]),
    tc(["invalid", "invalid.illegal"], c["rose"]),
    tc(["support.type.property-name.json"], c["shade"]),
    tc(["source.json meta.structure.dictionary.json > string.quoted.json > punctuation.string"], c["shade"]),
    tc(["source.env variable.other", "source.dotenv variable.other"], c["cyan"]),
]

semantic = {
    "parameter": {"foreground": c["ice"], "italic": True},
    "property": c["shade"],
    "enumMember": c["peach"],
    "variable.readonly": c["cloud"],
    "variable.defaultLibrary": c["horizon2"],
    "function": "#ffffff",
    "method": "#ffffff",
    "class": c["mint"],
    "interface": c["mint"],
    "type": c["mint"],
    "typeParameter": {"foreground": c["mint"], "italic": True},
    "namespace": c["mint"],
    "decorator": c["lilac"],
}

theme = {
    "$schema": "vscode://schemas/color-theme",
    "name": "Cumulus",
    "type": "dark",
    "semanticHighlighting": True,
    "colors": colors,
    "tokenColors": tokens,
    "semanticTokenColors": semantic,
}
for rule in theme["tokenColors"]:
    st = rule["settings"].get("fontStyle")
    if st is not None:
        rule["settings"]["fontStyle"] = " ".join(w for w in st.split() if w != "italic")
theme["tokenColors"].append({"scope": ["comment", "variable.parameter", "meta.parameter", "variable.language", "keyword.control", "entity.other.attribute-name", "markup.italic", "markup.quote", "storage.modifier", "storage.type"], "settings": {"fontStyle": ""}})
for k, v in list(theme["semanticTokenColors"].items()):
    if isinstance(v, dict):
        v["italic"] = False
    else:
        theme["semanticTokenColors"][k] = {"foreground": v, "italic": False}
theme["semanticTokenColors"]["*"] = {"italic": False}
json.dump(theme, open(os.path.join(ext, "themes", "cumulus.json"), "w"), indent=2)

CLEAR = "#00000000"
glass_overrides = {
    "editor.background": "#03103240",
    "editorPane.background": CLEAR,
    "editorGutter.background": CLEAR,
    "minimap.background": CLEAR,
    "sideBar.background": CLEAR,
    "sideBarSectionHeader.background": CLEAR,
    "sideBarStickyScroll.background": "#041640f0",
    "activityBar.background": CLEAR,
    "titleBar.activeBackground": CLEAR,
    "titleBar.inactiveBackground": CLEAR,
    "statusBar.background": CLEAR,
    "statusBar.noFolderBackground": CLEAR,
    "panel.background": CLEAR,
    "panelSectionHeader.background": CLEAR,
    "terminal.background": CLEAR,
    "breadcrumb.background": CLEAR,
    "editorGroupHeader.tabsBackground": CLEAR,
    "editorGroupHeader.noTabsBackground": CLEAR,
    "tab.inactiveBackground": CLEAR,
    "tab.activeBackground": CLEAR,
    "tab.unfocusedActiveBackground": CLEAR,
    "tab.hoverBackground": CLEAR,
    "tab.border": CLEAR,
    "tab.activeBorder": CLEAR,
    "tab.activeBorderTop": CLEAR,
    "tab.unfocusedActiveBorderTop": CLEAR,
    "activityBar.activeBorder": CLEAR,
    "modernUI.shellBackground": CLEAR,
    "editorStickyScroll.background": "#061e52f0",
    "input.background": "#03103266",
    "checkbox.background": "#03103266",
    "textCodeBlock.background": "#03103261",
    "textPreformat.background": "#03103261",
    "list.hoverBackground": "#c8e1ff17",
    "list.activeSelectionBackground": "#5cb6f247",
    "list.inactiveSelectionBackground": "#5cb6f226",
    "toolbar.hoverBackground": "#c8e1ff1a",
    "editorWidget.background": "#0a2c6ce6",
    "editorHoverWidget.background": "#0a2c6cf0",
    "editorSuggestWidget.background": "#0a2c6cf0",
    "menu.background": "#0a2c6cf2",
    "dropdown.background": "#0a2c6cf2",
    "quickInput.background": "#0a2c6ce6",
    "notifications.background": "#0a2c6ce6",
    "chat.requestBackground": "#c8e1ff12",
    "sideBar.border": "#c8e1ff21",
    "sideBarActivityBarTop.border": "#c8e1ff21",
    "panel.border": "#c8e1ff21",
    "editorGroup.border": "#c8e1ff21",
    "editorGroupHeader.tabsBorder": "#c8e1ff1a",
    "titleBar.border": CLEAR,
    "statusBar.border": CLEAR,
    "activityBar.border": CLEAR,
    "widget.border": "#c8e1ff38",
    "editorWidget.border": "#c8e1ff38",
    "editorHoverWidget.border": "#c8e1ff38",
    "editorSuggestWidget.border": "#c8e1ff38",
    "menu.border": "#c8e1ff38",
    "notifications.border": "#c8e1ff38",
    "input.border": "#c8e1ff38",
    "dropdown.border": "#c8e1ff38",
}
glass_theme = json.loads(json.dumps(theme))
glass_theme["name"] = "Cumulus Glass"
glass_theme["colors"].update(glass_overrides)
for rule in glass_theme["tokenColors"]:
    if "comment" in rule["scope"]:
        rule["settings"]["foreground"] = "#a3bde3"
json.dump(glass_theme, open(os.path.join(ext, "themes", "cumulus-glass.json"), "w"), indent=2)

pkg = {
    "name": "cumulus-theme",
    "displayName": "Cumulus",
    "description": "An immersive deep-sky blue theme with sunlit cloud-cream text.",
    "version": "1.5.1",
    "publisher": "local",
    "engines": {"vscode": "^1.80.0"},
    "categories": ["Themes"],
    "main": "./extension.js",
    "activationEvents": ["onStartupFinished"],
    "contributes": {"commands": [{"command": "cumulus.patchClaudeCode", "title": "Re-apply Claude Code glass", "category": "Cumulus"}], "themes": [{"label": "Cumulus", "uiTheme": "vs-dark", "path": "./themes/cumulus.json"}, {"label": "Cumulus Glass", "uiTheme": "vs-dark", "path": "./themes/cumulus-glass.json"}]},
}
json.dump(pkg, open(os.path.join(ext, "package.json"), "w"), indent=2)

manifest = """<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="cumulus-theme" Version="1.5.1" Publisher="local" />
    <DisplayName>Cumulus</DisplayName>
    <Description xml:space="preserve">An immersive deep-sky blue theme with sunlit cloud-cream text.</Description>
    <Categories>Themes</Categories>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.80.0" />
    </Properties>
  </Metadata>
  <Installation><InstallationTarget Id="Microsoft.VisualStudio.Code" /></Installation>
  <Dependencies />
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
  </Assets>
</PackageManifest>
"""
ctypes = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension=".json" ContentType="application/json" /><Default Extension=".vsixmanifest" ContentType="text/xml" /></Types>
"""
vsix = os.path.join(out, "cumulus-theme-1.5.1.vsix")
with zipfile.ZipFile(vsix, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("extension.vsixmanifest", manifest)
    z.writestr("[Content_Types].xml", ctypes)
    z.write(os.path.join(ext, "package.json"), "extension/package.json")
    z.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "extension.js"), "extension/extension.js")
    z.write(os.path.join(ext, "themes", "cumulus.json"), "extension/themes/cumulus.json")
    z.write(os.path.join(ext, "themes", "cumulus-glass.json"), "extension/themes/cumulus-glass.json")
print(vsix, len(colors), "colors", len(tokens), "token rules")
