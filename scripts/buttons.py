"""
Clickable buttons for the README.

GitHub keeps an <img> wrapped in a link clickable, so every navigation link
in the README is a small SVG button inside a markdown link rather than bare
underlined text (which GitHub also renders with emoji arrows). Buttons have a
transparent background so they sit cleanly on both the dark and light theme,
use the same neo-brutalist block as the story layer, and carry one cheap
motion each: the arrow nudges the way the button goes, and a sheen passes
over it now and then.

    python scripts/build.py   # writes btn/*.svg alongside the panels
"""
import zlib

import profile as P
from design import BG2, INK, DIM, CREAM, ROSE, MINT, VIOLET, PURPLE, INKK, esc, svg_open
from icons import icon

H = 46          # button face height
OFF = 5         # hard shadow offset
FS = 12.5       # label size
CW = FS * 0.64  # mono bold advance, generous so labels never clip


def _arrow(kind, x, y, col):
    """Drawn arrow glyphs - never the emoji ones."""
    if kind == "next":
        return f'<path d="M{x} {y - 7}l9 7-9 7z" fill="{col}"/>'
    if kind == "prev":
        return f'<path d="M{x + 9} {y - 7}l-9 7 9 7z" fill="{col}"/>'
    if kind == "up":
        return f'<path d="M{x} {y + 5}l7-9 7 9z" fill="{col}"/>'
    if kind == "out":
        return (f'<path d="M{x} {y + 6}L{x + 10} {y - 4}M{x + 2} {y - 5}H{x + 11}V{y + 4}" fill="none" '
                f'stroke="{col}" stroke-width="2.4" stroke-linecap="square"/>')
    return ""


def button(label, col, kind="next", style="solid", lead_icon=None, shadow=None):
    """One button. style: solid (accent face, ink text) or dark (ink face,
    accent text and border). kind picks the arrow and which way it nudges."""
    shadow = shadow or {CREAM: ROSE, ROSE: PURPLE, MINT: ROSE, VIOLET: MINT}.get(col, ROSE)
    face, ink = (col, INKK) if style == "solid" else (BG2, col)
    pad = 18
    lead = 26 if lead_icon else 0
    arrow_w = 22 if kind else 0
    tw = len(label) * CW
    w = int(pad + lead + tw + (12 + arrow_w if kind else 0) + pad)
    Wd, Ht = w + OFF + 3, H + OFF + 3
    seed = zlib.crc32(label.encode()) % 1000 / 1000.0
    nud = {"next": "translateX(4px)", "prev": "translateX(-4px)", "up": "translateY(-3px)",
           "out": "translate(2px,-2px)"}.get(kind, "none")
    css = (".nd{animation:nd 1.1s steps(2,end) infinite}"
           "@keyframes nd{0%%,100%%{transform:none}50%%{transform:%s}}"
           "@keyframes sh{0%%,70%%{transform:translateX(-80px)}100%%{transform:translateX(%dpx)}}"
           ".sh{animation:sh 3.8s cubic-bezier(.4,0,.2,1) %.2fs infinite}"
           "text{font-family:'JetBrains Mono','Fira Code',ui-monospace,Consolas,monospace}"
           % (nud, w + 80, -seed * 3.8))
    x, y = 1.5, 1.5
    cy = y + H / 2
    parts = [svg_open(Wd, Ht), "<style>%s</style>" % css,
             f'<rect x="{x + OFF}" y="{y + OFF}" width="{w}" height="{H}" rx="9" fill="{shadow}" '
             f'stroke="{INKK}" stroke-width="2.6"/>',
             f'<rect x="{x}" y="{y}" width="{w}" height="{H}" rx="9" fill="{face}" stroke="{INKK if style == "solid" else col}" '
             f'stroke-width="2.6"/>',
             f'<clipPath id="c"><rect x="{x}" y="{y}" width="{w}" height="{H}" rx="9"/></clipPath>'
             f'<g clip-path="url(#c)"><rect class="sh" x="{x}" y="{y}" width="34" height="{H}" fill="#ffffff" '
             f'opacity="{0.35 if style == "solid" else 0.08}" transform="skewX(-20)"/></g>']
    tx = x + pad
    if kind == "prev":
        parts.append(f'<g class="nd">{_arrow("prev", tx, cy, ink)}</g>')
        tx += arrow_w + 12
    if lead_icon:
        parts.append(icon(lead_icon, tx, cy - 10, 20, ink, 2.0, 1))
        tx += lead
    parts.append(f'<text x="{tx}" y="{cy + FS * 0.36:.1f}" font-size="{FS}" font-weight="800" letter-spacing="0.6" '
                 f'fill="{ink}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>')
    if kind and kind != "prev":
        parts.append(f'<g class="nd">{_arrow(kind, tx + tw + 12, cy, ink)}</g>')
    parts.append("</svg>")
    return "\n".join(parts)


def chip(numeral, label, col):
    """Chapter-select chip: a stamped numeral block, then the chapter name."""
    nw = 40
    tw = len(label) * CW
    w = int(nw + 14 + tw + 16)
    Wd, Ht = w + OFF + 3, H + OFF + 3
    x, y = 1.5, 1.5
    cy = y + H / 2
    css = "text{font-family:'JetBrains Mono','Fira Code',ui-monospace,Consolas,monospace}"
    return "\n".join([
        svg_open(Wd, Ht), "<style>%s</style>" % css,
        f'<rect x="{x + OFF}" y="{y + OFF}" width="{w}" height="{H}" rx="9" fill="{col}" stroke="{INKK}" stroke-width="2.6"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{H}" rx="9" fill="{BG2}" stroke="{col}" stroke-width="2.6"/>',
        f'<path d="M{x + 9} {y}H{x + nw}V{y + H}H{x + 9}A9 9 0 0 1 {x} {y + H - 9}V{y + 9}A9 9 0 0 1 {x + 9} {y}Z" '
        f'fill="{col}"/>',
        f'<text x="{x + nw / 2}" y="{cy + 6}" text-anchor="middle" font-size="17" font-weight="900" fill="{INKK}">'
        f'{esc(numeral)}</text>',
        f'<text x="{x + nw + 14}" y="{cy + FS * 0.36:.1f}" font-size="{FS}" font-weight="800" letter-spacing="0.6" '
        f'fill="{INK}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>',
        "</svg>"])


# anchors and short labels, in story order
STOPS = [("prologue", "PROLOGUE", None, CREAM),
         ("origin", "ORIGIN", "I", CREAM), ("arsenal", "ARSENAL", "II", ROSE),
         ("builds", "BUILDS", "III", MINT), ("battle-log", "BATTLE LOG", "IV", VIOLET),
         ("trophies", "TROPHIES", "V", CREAM), ("quest", "QUEST", "VI", ROSE),
         ("epilogue", "EPILOGUE", None, MINT)]


def build_all(write):
    """Write every button through build.write(); returns nothing."""
    write("btn/start.svg", button("PRESS START", CREAM, "next"))
    write("btn/menu.svg", button("MENU", CREAM, "up"))
    for anchor, label, num, col in STOPS:
        write("btn/prev-%s.svg" % anchor, button(label, col, "prev", style="dark"))
        write("btn/next-%s.svg" % anchor, button(label, col, "next"))
        if num:
            write("btn/ch-%s.svg" % anchor, chip(num, label, col))
    for key, label, sub, col in P.VOTE_OPTIONS:
        write("btn/vote-%s.svg" % key, button("VOTE: " + label.upper(), col, "out", lead_icon=None))
    for slug, label, col in [("SheShield", "SHESHIELD", CREAM), ("Vyapaar", "VYAPAAR", VIOLET),
                             ("Hirehearsal", "HIREHEARSAL", ROSE), ("BookMyCampus", "BOOKMYCAMPUS", ROSE),
                             ("TimedInk", "TIMEDINK", MINT), ("PII-Redaction-Tool", "PII REDACTION", MINT)]:
        write("btn/repo-%s.svg" % slug, button(label, col, "out", style="dark", lead_icon="repo"))
    for name, label, col, ic in [("github", "GITHUB", CREAM, "github"), ("linkedin", "LINKEDIN", MINT, "linkedin"),
                                 ("portfolio", "PORTFOLIO", VIOLET, "code"), ("instagram", "INSTAGRAM", ROSE, "instagram"),
                                 ("email", "EMAIL", CREAM, "mail")]:
        write("btn/social-%s.svg" % name, button(label, col, "out", style="dark", lead_icon=ic))
