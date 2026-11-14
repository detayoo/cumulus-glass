import math, random, sys, os

out = sys.argv[1]
os.makedirs(out, exist_ok=True)

DEFS = """<defs>
<radialGradient id="puff" cx="0.45" cy="0.36" r="0.62" fx="0.42" fy="0.22">
  <stop offset="0" stop-color="#fffbe2"/>
  <stop offset="0.38" stop-color="#f8f4dc"/>
  <stop offset="0.7" stop-color="#e3ebe4"/>
  <stop offset="0.9" stop-color="#c3d7e6"/>
  <stop offset="1" stop-color="#a9c6e3" stop-opacity="0.9"/>
</radialGradient>
<radialGradient id="puffLow" cx="0.45" cy="0.36" r="0.62" fx="0.42" fy="0.22">
  <stop offset="0" stop-color="#f1f3e6"/>
  <stop offset="0.45" stop-color="#dfe8ea"/>
  <stop offset="0.8" stop-color="#bcd2e6"/>
  <stop offset="1" stop-color="#94b7dc" stop-opacity="0.9"/>
</radialGradient>
<radialGradient id="glass" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
  <stop offset="0.68" stop-color="#d8ecff" stop-opacity="0.04"/>
  <stop offset="0.9" stop-color="#cfe6ff" stop-opacity="0.20"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0.50"/>
</radialGradient>
<linearGradient id="spec" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="1"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="1"/>
</linearGradient>
</defs>"""


def puff(x, y, r, low=False):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#{'puffLow' if low else 'puff'})"/>'


def cumulus(rng, x0, x1, base, peak, scale=1.0):
    """Billowing cumulus: the outline is the union of round lobes (a tall tower plus shoulders),
    filled with puffs drawn top-down so each lower puff leaves a shaded scallop."""
    width = x1 - x0
    tower = x0 + width * rng.uniform(0.38, 0.55)
    lobes = [(tower, base - peak, width * 0.22)]
    for _ in range(9):
        cx = rng.uniform(x0 + width * 0.05, x1 - width * 0.05)
        falloff = 1 - abs(cx - tower) / width
        lobes.append((cx, (base - peak) * rng.uniform(0.35, 0.8) * falloff, width * rng.uniform(0.08, 0.16)))

    def top(x):
        best = base + 999
        for cx, h, w in lobes:
            d = (x - cx) / w
            if abs(d) < 1:
                best = min(best, base - h * math.sqrt(1 - d * d))
        return best

    pts = []
    y = peak - 10
    while y < base + 30 * scale:
        x = x0
        while x < x1:
            t = top(x)
            if y >= t - 4:
                depth = (y - peak) / max(1, base - peak)
                edge = y - t < 26 * scale
                r = rng.uniform(18, 34) * scale if edge else rng.uniform(12, 26) * scale * (0.8 + 0.6 * depth)
                low = rng.random() < max(0.0, depth - 0.25) ** 1.4 * 1.6
                pts.append((x + rng.uniform(-7, 7) * scale, y + rng.uniform(-4, 4) * scale, r, low))
            x += rng.uniform(16, 26) * scale
        y += rng.uniform(13, 19) * scale
    pts.sort(key=lambda p: p[1])
    return "".join(puff(*p) for p in pts)


def trail(rng, ax, ay, bx, by, n, rmax):
    parts = []
    for i in range(n):
        t = i / max(1, n - 1)
        x = ax + (bx - ax) * t + rng.uniform(-6, 6)
        y = ay + (by - ay) * t + rng.uniform(-4, 4)
        r = rmax * (1 - 0.75 * t) * rng.uniform(0.7, 1.1)
        if rng.random() < 0.18:
            continue
        cluster = [(x, y, r)]
        for _ in range(rng.randint(1, 3)):
            cluster.append((x + rng.uniform(-r, r) * 1.1, y + rng.uniform(-r * 0.6, r * 0.3), r * rng.uniform(0.5, 0.85)))
        cluster.sort(key=lambda p: p[1])
        parts += [puff(*p) for p in cluster]
    return "".join(parts)


def glass_bubble(x, y, r):
    a = math.radians(-135)
    sx, sy = x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55
    return (
        f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#glass)" stroke="#ffffff" stroke-opacity="0.38" stroke-width="1"/>'
        f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{r*0.34:.1f}" ry="{r*0.16:.1f}" fill="url(#spec)" transform="rotate(-40 {sx:.1f} {sy:.1f})"/>'
        f'<circle cx="{x + r*0.5:.1f}" cy="{y + r*0.52:.1f}" r="{max(1.2, r*0.07):.1f}" fill="#ffffff" fill-opacity="0.55"/></g>'
    )


def svg(w, h, body, opacity=1.0):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{DEFS}'
            f'<g opacity="{opacity}">{body}</g></svg>')


rng = random.Random(7)

# Empty editor: big mound left, smaller one right, trails drifting up-right, a few glass bubbles.
W, H = 1600, 640
body = ""
body += trail(rng, 560, 390, 1000, 190, 18, 9)
body += trail(rng, 1180, 470, 1560, 300, 14, 8)
body += trail(rng, 120, 330, 420, 230, 10, 7)
body += cumulus(rng, -40, 760, 660, 230, 1.0)
body += cumulus(rng, 1080, 1680, 660, 400, 0.85)
for bx, by, br in [(1180, 230, 46), (1290, 150, 22), (860, 330, 30), (1420, 300, 14), (700, 170, 12), (1100, 360, 9)]:
    body += glass_bubble(bx, by, br)
open(os.path.join(out, "empty-editor.svg"), "w").write(svg(W, H, body, 0.92))

# Activity bar lane: a slim diagonal trail of tiny puffs plus two glass bubbles (no text lives here).
rng = random.Random(11)
body = trail(rng, 10, 330, 38, 40, 14, 6.5)
body += glass_bubble(30, 250, 7) + glass_bubble(16, 120, 4.5)
open(os.path.join(out, "lane.svg"), "w").write(svg(48, 360, body, 0.55))

# Title bar: short trails either side of the centered command center.
rng = random.Random(3)
body = trail(rng, 8, 26, 250, 10, 12, 6) + glass_bubble(200, 18, 5)
open(os.path.join(out, "title-left.svg"), "w").write(svg(260, 36, body, 0.6))
rng = random.Random(5)
body = trail(rng, 10, 12, 250, 26, 12, 6) + glass_bubble(60, 20, 4)
open(os.path.join(out, "title-right.svg"), "w").write(svg(260, 36, body, 0.6))

for f in sorted(os.listdir(out)):
    print(f, os.path.getsize(os.path.join(out, f)))
