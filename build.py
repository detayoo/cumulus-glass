"""Build Cumulus Glass into dist/.

    python3 build.py            build dist/cumulus-glass.css and dist/cumulus-theme-<version>.vsix
    python3 build.py --install  also copy the CSS and the chat panel patch files into ~/.vscode

Needs Python 3.9+ and Pillow (pip install pillow).
"""

import base64
import io
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
GLASS = os.path.join(ROOT, "glass")
ART = os.path.join(GLASS, "art")
DIST = os.path.join(ROOT, "dist")
VSCODE = os.path.join(os.path.expanduser("~"), ".vscode")


def jpeg_uri(image):
    buf = io.BytesIO()
    image.convert("RGB").save(buf, "JPEG", quality=85, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def svg_uri(name):
    with open(os.path.join(ART, name), "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()


def build_css():
    sky = Image.open(os.path.join(GLASS, "sky.jpg"))
    soft = sky.filter(ImageFilter.GaussianBlur(2.5))
    frost = sky.resize((sky.width // 2, sky.height // 2), Image.LANCZOS).filter(ImageFilter.GaussianBlur(16))

    with open(os.path.join(GLASS, "cumulus-glass.template.css")) as f:
        css = f.read()
    for key, value in {
        "__SOFT__": jpeg_uri(soft),
        "__FROST__": jpeg_uri(frost),
        "__ART_EMPTY__": svg_uri("empty-editor.svg"),
        "__ART_LANE__": svg_uri("lane.svg"),
        "__ART_TITLE_L__": svg_uri("title-left.svg"),
        "__ART_TITLE_R__": svg_uri("title-right.svg"),
    }.items():
        css = css.replace(key, value)

    out = os.path.join(DIST, "cumulus-glass.css")
    with open(out, "w") as f:
        f.write(css)
    print(f"{out} ({len(css) // 1024} KB)")


def install():
    target = os.path.join(VSCODE, "cumulus")
    os.makedirs(target, exist_ok=True)
    shutil.copy(os.path.join(DIST, "cumulus-glass.css"), os.path.join(VSCODE, "cumulus-glass.css"))
    for name in ("chat-panel-glass.css", "patch-chat-panel.sh"):
        shutil.copy(os.path.join(ROOT, "extras", "chat-panel", name), os.path.join(target, name))
    os.chmod(os.path.join(target, "patch-chat-panel.sh"), 0o755)
    print(f"Copied cumulus-glass.css to {VSCODE} and the chat panel patch files to {target}")


def main():
    os.makedirs(DIST, exist_ok=True)
    subprocess.run([sys.executable, os.path.join(GLASS, "bubbles.py"), ART], check=True, stdout=subprocess.DEVNULL)
    build_css()
    subprocess.run([sys.executable, os.path.join(ROOT, "theme", "build_theme.py"), DIST], check=True)
    if "--install" in sys.argv:
        install()


if __name__ == "__main__":
    main()
