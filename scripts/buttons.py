"""
Clickable buttons for the README.

GitHub keeps an <img> wrapped in a link clickable, so every navigation link
in the README is a small SVG button inside a link rather than bare underlined
text (which GitHub also renders with emoji arrows). Buttons have a
transparent background so they sit cleanly on both the dark and light theme.

Primary buttons - the way forward - have a light face. Secondary ones are
graphite with a hairline border and a short beam of accent light that
travels around it. The chevron nudges the way the button goes.

    python scripts/build.py   # writes btn/*.svg alongside the panels
"""
import zlib

import profile as P
from design import INK, CREAM, ROSE, MINT, VIOLET, esc, svg_open
from icons import icon

H = 42          # button height
R = 10          # corner radius
FS = 14         # label size
SANS = "'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,sans-serif"


def _tw(label, fs=FS):
    """Rendered width estimate for the sans label; pinned with textLength."""
    narrow = sum(1 for c in label if c in "iIl.,:;'|1 ")
    wide = sum(1 for c in label if c in "MWmw@")
    return fs * (0.6 * (len(label) - narrow - wide) + 0.3 * narrow + 0.86 * wide)


def _glyph(kind, x, y, col):
    """Thin stroke chevrons - the arrows are drawn, never emoji."""
    d = {"next": f"M{x} {y - 5}l5 5-5 5", "prev": f"M{x + 5} {y - 5}l-5 5 5 5",
         "up": f"M{x} {y + 3}l5-5 5 5", "out": f"M{x} {y + 5}l9-9M{x + 2} {y - 4}h7v7"}[kind]
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _perimeter(x, y, w, h, r):
    return (f"M{x + r} {y}H{x + w - r}A{r} {r} 0 0 1 {x + w} {y + r}V{y + h - r}"
            f"A{r} {r} 0 0 1 {x + w - r} {y + h}H{x + r}A{r} {r} 0 0 1 {x} {y + h - r}"
            f"V{y + r}A{r} {r} 0 0 1 {x + r} {y}Z")


def button(label, col, kind="next", style="secondary", lead_icon=None):
    """primary: light face, dark text - the one obvious way forward.
    secondary: graphite face, hairline border, and a short beam of the accent
    colour that travels around the border. The chevron nudges the way the
    button goes."""
    pad = 16
    lead = 26 if lead_icon else 0
    gw = 18 if kind else 0
    tw = _tw(label)
    w = int(pad + (gw if kind == "prev" else 0) + lead + tw + (gw if kind and kind != "prev" else 0) + pad)
    x, y = 1.5, 1.5
    Wd, Ht = w + 3, H + 6
    cy = y + H / 2
    seed = zlib.crc32(label.encode()) % 1000 / 1000.0
    nud = {"next": "translateX(3px)", "prev": "translateX(-3px)", "up": "translateY(-2px)",
           "out": "translate(2px,-2px)"}.get(kind, "none")
    primary = style == "primary"
    face = "#f0f3f6" if primary else "#161b22"
    ink = "#0d1117" if primary else INK
    gcol = "#0d1117" if primary else col
    css = ("text{font-family:%s}"
           ".nd{animation:nd 2.4s cubic-bezier(.45,0,.25,1) infinite}"
           "@keyframes nd{0%%,55%%,100%%{transform:none}75%%{transform:%s}}"
           "@keyframes beam{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}"
           ".bm{animation:beam 4.5s linear %.2fs infinite}" % (SANS, nud, -seed * 4.5))
    per = _perimeter(x, y, w, H, R)
    parts = [svg_open(Wd, Ht), "<style>%s</style>" % css]
    if primary:
        # a soft accent underglow, then the light face with a hairline top edge
        parts.append(f'<rect x="{x + 6}" y="{y + 4}" width="{w - 12}" height="{H}" rx="{R}" fill="{col}" opacity="0.35"/>')
        parts.append(f'<path d="{per}" fill="{face}"/>')
        parts.append(f'<rect x="{x + R}" y="{y + 0.8}" width="{w - 2 * R}" height="1" fill="#ffffff"/>')
    else:
        parts.append(f'<path d="{per}" fill="{face}" stroke="#ffffff" stroke-opacity="0.12" stroke-width="1"/>')
        parts.append(f'<path class="bm" d="{per}" fill="none" stroke="{col}" stroke-width="1.4" '
                     f'stroke-linecap="round" pathLength="100" stroke-dasharray="16 84" stroke-dashoffset="0"/>')
    tx = x + pad
    if kind == "prev":
        parts.append(f'<g class="nd">{_glyph("prev", tx, cy, gcol)}</g>')
        tx += gw
    if lead_icon:
        parts.append(icon(lead_icon, tx, cy - 9, 18, col if not primary else ink, 1.8, 1))
        tx += lead
    parts.append(f'<text x="{tx:.1f}" y="{cy + FS * 0.35:.1f}" font-size="{FS}" font-weight="600" letter-spacing="0.1" '
                 f'fill="{ink}" textLength="{tw:.1f}" lengthAdjust="spacing">{esc(label)}</text>')
    if kind and kind != "prev":
        parts.append(f'<g class="nd">{_glyph(kind, tx + tw + 9, cy, gcol)}</g>')
    parts.append("</svg>")
    return "\n".join(parts)


def chip(numeral, label, col):
    """Chapter-select chip: the numeral in the chapter's accent, a hairline
    divider, then the chapter name - a quiet segmented-control look."""
    nw = 34
    tw = _tw(label)
    w = int(nw + 12 + tw + 16)
    x, y = 1.5, 1.5
    cy = y + H / 2
    per = _perimeter(x, y, w, H, R)
    css = "text{font-family:%s}" % SANS
    return "\n".join([
        svg_open(w + 3, H + 6), "<style>%s</style>" % css,
        f'<path d="{per}" fill="#161b22" stroke="#ffffff" stroke-opacity="0.12" stroke-width="1"/>',
        f'<text x="{x + nw / 2 + 4:.1f}" y="{cy + 4.6:.1f}" text-anchor="middle" font-size="13" font-weight="700" '
        f'fill="{col}" letter-spacing="0.5">{esc(numeral)}</text>',
        f'<rect x="{x + nw + 4}" y="{y + 11}" width="1" height="{H - 22}" fill="#ffffff" opacity="0.14"/>',
        f'<text x="{x + nw + 16}" y="{cy + FS * 0.35:.1f}" font-size="{FS}" font-weight="600" fill="{INK}" '
        f'textLength="{tw:.1f}" lengthAdjust="spacing">{esc(label)}</text>',
        "</svg>"])


# anchors and labels, in story order
STOPS = [("prologue", "Prologue", None, CREAM),
         ("origin", "Origin", "I", CREAM), ("arsenal", "Arsenal", "II", ROSE),
         ("builds", "Builds", "III", MINT), ("battle-log", "Battle log", "IV", VIOLET),
         ("trophies", "Trophies", "V", CREAM), ("quest", "Current quest", "VI", ROSE),
         ("epilogue", "Epilogue", None, MINT)]


def build_all(write):
    write("btn/start.svg", button("Press start", MINT, "next", style="primary"))
    write("btn/menu.svg", button("Menu", CREAM, "up"))
    for anchor, label, num, col in STOPS:
        write("btn/prev-%s.svg" % anchor, button(label, col, "prev"))
        write("btn/next-%s.svg" % anchor, button(label, col, "next", style="primary"))
        if num:
            write("btn/ch-%s.svg" % anchor, chip(num, label, col))
    for key, label, sub, col in P.VOTE_OPTIONS:
        write("btn/vote-%s.svg" % key, button("Vote \u00b7 " + label, col, "out"))
    for slug, label, col in [("SheShield", "SheShield", CREAM), ("Vyapaar", "Vyapaar", VIOLET),
                             ("Hirehearsal", "Hirehearsal", ROSE), ("BookMyCampus", "BookMyCampus", ROSE),
                             ("TimedInk", "TimedInk", MINT), ("PII-Redaction-Tool", "PII Redaction", MINT)]:
        write("btn/repo-%s.svg" % slug, button(label, col, "out", lead_icon="repo"))
    for name, label, col, ic in [("github", "GitHub", CREAM, "github"), ("linkedin", "LinkedIn", MINT, "linkedin"),
                                 ("portfolio", "Portfolio", VIOLET, "code"), ("instagram", "Instagram", ROSE, "instagram"),
                                 ("email", "Email", CREAM, "mail")]:
        write("btn/social-%s.svg" % name, button(label, col, "out", lead_icon=ic))
