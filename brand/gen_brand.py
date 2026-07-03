"""Yggdrasil AI Labs brand asset generator.
Recreates the org avatar glyph (node-tree) as vector math, renders:
  - social preview cards (1280x640 PNG) per repo
  - favicon.svg (scalable, same glyph)
Colors sampled from the live org avatar.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

BG = (13, 26, 23)          # near-black dark teal
LINE = (46, 200, 141)      # spoke green
DOT = (87, 226, 172)       # terminal mint
CORE = (234, 247, 240)     # center dot, near-white
DIM = (110, 150, 135)      # footer text

FONT_DIR = r"C:\Windows\Fonts"


def draw_glyph(d: ImageDraw.ImageDraw, cx, cy, s, ss=4):
    """Draw the node-tree glyph centered at (cx, cy), s = half-height.
    ss = supersample factor already applied to coords by caller."""
    lw = int(s * 0.11)
    dot_r = int(s * 0.10)
    ring_r = int(s * 0.18)
    gap_r = int(s * 0.27)
    junc = s * 0.44          # where diagonals meet the trunk

    # spoke endpoints: up, up-left, up-right, down, down-left, down-right
    pts = [
        (cx, cy - s),
        (cx - s * 0.68, cy - s * 0.82),
        (cx + s * 0.68, cy - s * 0.82),
        (cx, cy + s),
        (cx - s * 0.68, cy + s * 0.82),
        (cx + s * 0.68, cy + s * 0.82),
    ]
    anchors = [
        (cx, cy - junc), (cx, cy - junc), (cx, cy - junc),
        (cx, cy + junc), (cx, cy + junc), (cx, cy + junc),
    ]
    for (px, py), (ax, ay) in zip(pts, anchors):
        d.line([(ax, ay), (px, py)], fill=LINE, width=lw)
    # trunk segments from ring gap to the junctions
    d.line([(cx, cy - gap_r), (cx, cy - junc)], fill=LINE, width=lw)
    d.line([(cx, cy + gap_r), (cx, cy + junc)], fill=LINE, width=lw)
    # round the junctions
    jr = lw // 2
    for jy in (cy - junc, cy + junc):
        d.ellipse([cx - jr, jy - jr, cx + jr, jy + jr], fill=LINE)
    # terminal dots
    for px, py in pts:
        d.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r], fill=DOT)
    # central ring (outlined, dark gap inside) + core
    d.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
              outline=LINE, width=int(lw * 0.8))
    core_r = int(s * 0.07)
    d.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r], fill=CORE)


def wrap(text, font, max_w, d):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(repo, tagline, out, codename=None,
         footer="Yggdrasil AI Labs  ·  github.com/Yggdrasil-AI-labs"):
    SS = 4
    W, H = 1280, 640
    img = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)

    # glyph on the right third
    draw_glyph(d, int(W * 0.80) * SS, int(H * 0.46) * SS, int(H * 0.30) * SS, SS)

    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)

    f_name = ImageFont.truetype(f"{FONT_DIR}\\consolab.ttf", 68)
    f_code = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 40)
    f_tag = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 33)
    f_foot = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 26)

    x, y = 84, 150
    if codename:
        d.text((x, y - 62), codename, font=f_code, fill=DOT)
    d.text((x, y), repo, font=f_name, fill=(240, 250, 245))
    y += 100
    for ln in wrap(tagline, f_tag, 700, d):
        d.text((x, y), ln, font=f_tag, fill=(168, 196, 184))
        y += 48
    # footer
    d.line([(x, H - 96), (x + 700, H - 96)], fill=(32, 56, 48), width=2)
    d.text((x, H - 76), footer, font=f_foot, fill=DIM)
    img.save(out, "PNG")
    print("wrote", out)


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect width="100" height="100" rx="18" fill="#0D1A17"/>
<g stroke="#2EC88D" stroke-width="6" stroke-linecap="round" fill="none">
  <path d="M50 20 L50 39"/><path d="M50 61 L50 80"/>
  <path d="M50 34 L27 22"/><path d="M50 34 L73 22"/>
  <path d="M50 66 L27 78"/><path d="M50 66 L73 78"/>
  <circle cx="50" cy="50" r="9"/>
</g>
<g fill="#57E2AC">
  <circle cx="50" cy="18" r="5"/><circle cx="25" cy="21" r="5"/><circle cx="75" cy="21" r="5"/>
  <circle cx="50" cy="82" r="5"/><circle cx="25" cy="79" r="5"/><circle cx="75" cy="79" r="5"/>
</g>
<circle cx="50" cy="50" r="3.4" fill="#EAF7F0"/>
</svg>
"""

REPOS = {
    "adsb-to-wdgwars": ("Muninn", "Normalizes 13 ADS-B receiver dialects into one JSON schema. CLI and in-browser (Pyodide/WASM)."),
    "meshcore-to-wdgwars": ("Heimdall", "LoRa / MeshCore mesh telemetry to normalized records. CLI and in-browser (Pyodide/WASM)."),
    "wigle-to-wdgwars": (None, "WiGLE Wi-Fi / BLE wardrive CSVs to structured records."),
    "gungnir": (None, "Shared HMAC-signed transport client: integrity, retry, cooldown, silent-drop detection."),
    "wdgwars-api-tester": (None, "Contract-testing harness for an undocumented HTTP API. Probe quorum + 404 fingerprinting."),
    "leakguard": (None, "Pre-publish disclosure scanner: secrets, PII, internal identifiers. Stdlib-only core; your rule inventory stays local."),
    ".github": (None, "Self-hosted AI & SIGINT lab. RF to structured data, on gated CI/CD."),
}

if __name__ == "__main__":
    import os
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "favicon.svg"), "w") as f:
        f.write(FAVICON_SVG)
    print("wrote favicon.svg")
    targets = sys.argv[1:] or list(REPOS)
    for name in targets:
        code, tag = REPOS[name]
        fname = "org-profile" if name == ".github" else name
        card(name if name != ".github" else "Yggdrasil AI Labs",
             tag, os.path.join(outdir, f"{fname}-social.png"), codename=code)
    if not sys.argv[1:]:
        card("wdgo-onramp",
             "Leveled onramp for new wardrivers: WiGLE basics to advanced multi-source capture.",
             os.path.join(outdir, "wdgo-onramp-social.png"),
             footer="hiroalleycat.github.io/wdgo-onramp")
