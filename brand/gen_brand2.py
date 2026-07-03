"""Yggdrasil AI Labs brand cards, v2 — Muninn terminal tone.
Bracket tags, // separators, uppercase mono, subtle CRT scanlines,
org-green glyph on near-black.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from gen_brand import draw_glyph, BG, LINE, DOT, CORE, DIM, FONT_DIR

TEXT = (224, 240, 232)
MUTED = (128, 156, 144)


def spaced(d, xy, s, font, fill, tracking=0):
    """Draw text with letter-spacing (PIL has none built in)."""
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x


def scanlines(img, step=4, alpha=26):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    for y in range(0, img.size[1], step):
        dd.line([(0, y), (img.size[0], y)], fill=(0, 0, 0, alpha), width=2)
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def card(name, bracket, slashes, out, repo=None,
         footer="github.com/Yggdrasil-AI-labs"):
    SS = 4
    W, H = 1280, 640
    img = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)
    draw_glyph(d, int(W * 0.81) * SS, int(H * 0.47) * SS, int(H * 0.30) * SS, SS)
    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)

    f_tag = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 26)
    f_name = ImageFont.truetype(f"{FONT_DIR}\\consolab.ttf", 88)
    f_sub = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 30)
    f_slash = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 32)
    f_foot = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 26)

    x = 84
    # bracket tag
    spaced(d, (x, 118), f"[ {bracket} ]", f_tag, DOT, tracking=3)
    # big uppercase name
    spaced(d, (x, 168), name.upper(), f_name, TEXT, tracking=4)
    y = 290
    # repo sub-line when the headline is a codename
    if repo:
        spaced(d, (x, y), f"[ {repo} ]", f_sub, MUTED, tracking=2)
        y += 56
    y += 8
    # slash-delimited tagline lines
    for ln in slashes:
        d.text((x, y), f"/ {ln} /", font=f_slash, fill=(168, 196, 184))
        y += 50
    # footer
    f_foot = ImageFont.truetype(f"{FONT_DIR}\\consola.ttf", 23)
    rule_w = 1080
    d.line([(x, H - 100), (x + rule_w, H - 100)], fill=(32, 56, 48), width=2)
    d.text((x, H - 76), f"> {footer}", font=f_foot, fill=DIM)
    tag = "[ MIT // NO TELEMETRY ]"
    tw = d.textlength(tag, font=f_foot)
    d.text((x + rule_w - tw, H - 76), tag, font=f_foot, fill=MUTED)

    img = scanlines(img)
    img.save(out, "PNG")
    print("wrote", out)


CARDS = {
    "adsb-to-wdgwars": dict(
        name="Muninn", repo="adsb-to-wdgwars", bracket="WDG // ADS-B INGEST NODE",
        slashes=["13 receiver dialects → one json schema",
                 "cli + in-browser (pyodide/wasm)"]),
    "meshcore-to-wdgwars": dict(
        name="Heimdall", repo="meshcore-to-wdgwars", bracket="WDG // LORA MESH INGEST",
        slashes=["meshcore telemetry → normalized records",
                 "cli + in-browser (pyodide/wasm)"]),
    "wigle-to-wdgwars": dict(
        name="wigle-to-wdgwars", bracket="WDG // WIGLE INGEST",
        slashes=["wigle wi-fi + ble wardrive csvs",
                 "→ structured records"]),
    "gungnir": dict(
        name="Gungnir", repo="gungnir", bracket="WDG // TRANSPORT CORE",
        slashes=["hmac-signed envelope / retry / cooldown",
                 "silent-drop detection / one client, many tools"]),
    "wdgwars-api-tester": dict(
        name="wdgwars-api-tester", bracket="WDG // API PROBE",
        slashes=["contract tests for an undocumented api",
                 "probe quorum / 404 fingerprinting"]),
    "leakguard": dict(
        name="leakguard", bracket="DISCLOSURE GATE",
        slashes=["secrets / pii / internal identifiers",
                 "stdlib-only core / your rules stay local"]),
    ".github": dict(
        name="Yggdrasil AI Labs", bracket="SELF-HOSTED AI // SIGINT LAB",
        slashes=["real-world rf → structured data",
                 "local-first / gated ci/cd / built to find the limits"]),
    "wdgo-onramp": dict(
        name="wdgo-onramp", bracket="WDG // NEWCOMER ONRAMP",
        slashes=["leveled path: wigle basics →",
                 "advanced multi-source capture"],
        footer="hiroalleycat.github.io/wdgo-onramp"),
}

if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand")
    os.makedirs(outdir, exist_ok=True)
    targets = sys.argv[1:] or list(CARDS)
    for key in targets:
        cfg = dict(CARDS[key])
        fname = "org-profile" if key == ".github" else key
        card(cfg.pop("name"), cfg.pop("bracket"), cfg.pop("slashes"),
             os.path.join(outdir, f"{fname}-social.png"), **cfg)
