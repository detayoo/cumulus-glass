const vscode = require("vscode");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFile } = require("child_process");

const SCRIPT = path.join(os.homedir(), ".vscode", "cumulus", "patch-chat-panel.sh");
const MARKER = "cumulus-glass:start";

function claudeCodeCss() {
  const ext = vscode.extensions.getExtension("anthropic.claude-code");
  if (!ext) return null;
  const css = path.join(ext.extensionPath, "webview", "index.css");
  return fs.existsSync(css) ? css : null;
}

function allPatched() {
  const root = path.join(os.homedir(), ".vscode", "extensions");
  let dirs = [];
  try {
    dirs = fs.readdirSync(root).filter((d) => d.startsWith("anthropic.claude-code-"));
  } catch {
    return true;
  }
  return dirs.every((d) => {
    const css = path.join(root, d, "webview", "index.css");
    try {
      return !fs.existsSync(css) || fs.readFileSync(css, "utf8").includes(MARKER);
    } catch {
      return true;
    }
  });
}

function glassActive() {
  return vscode.workspace.getConfiguration("workbench").get("colorTheme") === "Cumulus Glass";
}

function runPatch() {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(SCRIPT)) {
      reject(new Error(`Patch script not found at ${SCRIPT}`));
      return;
    }
    execFile("/bin/sh", [SCRIPT], (err, stdout, stderr) => {
      if (err) reject(new Error(stderr || err.message));
      else resolve(stdout);
    });
  });
}

async function offerReload(message) {
  const choice = await vscode.window.showInformationMessage(message, "Reload Window");
  if (choice === "Reload Window") {
    vscode.commands.executeCommand("workbench.action.reloadWindow");
  }
}

async function apply({ manual }) {
  const css = claudeCodeCss();
  if (!css) {
    if (manual) vscode.window.showWarningMessage("Cumulus: Claude Code isn't installed, so there's nothing to patch.");
    return;
  }
  if (!manual && (!glassActive() || allPatched() || !fs.existsSync(SCRIPT))) return;
  try {
    const out = await runPatch();
    const warning = out.split("\n").find((line) => line.startsWith("warning:"));
    if (warning) {
      vscode.window.showWarningMessage(`Cumulus: ${warning.replace("warning: ", "")}`);
    }
    await offerReload(
      manual
        ? "Cumulus: chat panel glass re-applied. Reload to see it."
        : "Cumulus: the chat panel needed its glass styling, so it was applied. Reload to see it."
    );
  } catch (err) {
    vscode.window.showErrorMessage(`Cumulus: couldn't patch the chat panel. ${err.message}`);
  }
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("cumulus.patchChatPanel", () => apply({ manual: true }))
  );
  context.subscriptions.push(
    vscode.extensions.onDidChange(() => apply({ manual: false }))
  );
  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("workbench.colorTheme")) apply({ manual: false });
    })
  );
  apply({ manual: false });
}

function deactivate() {}

module.exports = { activate, deactivate };
