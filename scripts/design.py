"""
Design system for the profile README SVGs.

Everything here is authored to survive GitHub's rendering pipeline:
  - the SVG is loaded as <img>, so no JS, no <foreignObject>, no web fonts, no <a>
  - CSS @keyframes and SMIL both animate fine
  - SVG filters (blur / turbulence / drop-shadow) render fine

Glassmorphism is faked the only way it can be inside an <img>: blurred colour
blobs underneath, a translucent gradient pane on top, a bright specular top
edge, a fading hairline border, and a whisper of noise grain.
"""
import re

# ---------------------------------------------------------------- palette
# "Midnight Arcade": a synthwave night. The accent names are historical
# (the profile started in cream / rose / mint / violet) and are kept so the
# layout code reads the same; the comment says what each one is now.
BG0 = "#0d1117"    # GitHub's own dark page colour, so panels melt into the page
BG1 = "#0d1117"
BG2 = "#161b22"    # GitHub's raised surface
INK = "#f0f3f6"    # primary text
DIM = "#9da7b3"    # secondary text
FAINT = "#6e7681"  # tertiary text

CREAM = "#ffc857"   # amber - legendary / primary accent
ROSE = "#ff4fa0"    # hot magenta - epic / secondary accent
MINT = "#2ee6ff"    # electric cyan - rare / tertiary accent
VIOLET = "#b6ff4f"  # acid lime - mythic / quaternary accent
GOLD = "#ffd479"
PURPLE = "#8b5cff"  # the horizon glow

RARITY = {
    "MYTHIC": VIOLET,
    "LEGENDARY": CREAM,
    "EPIC": ROSE,
    "RARE": MINT,
    "UNCOMMON": "#9d8cff",
}

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',ui-monospace,Consolas,monospace"
SANS = "'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,sans-serif"

W = 1200  # canonical canvas width


# ---------------------------------------------------------------- helpers
def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


_uid = [0]


def uid(prefix="i"):
    _uid[0] += 1
    return prefix + str(_uid[0])


def rr(x, y, w, h, r):
    """Rounded-rect path, used where <rect> cannot carry a gradient stroke."""
    return ("M%s,%s H%s A%s,%s 0 0 1 %s,%s V%s A%s,%s 0 0 1 %s,%s H%s "
            "A%s,%s 0 0 1 %s,%s V%s A%s,%s 0 0 1 %s,%s Z" % (
                x + r, y, x + w - r, r, r, x + w, y + r, y + h - r, r, r,
                x + w - r, y + h, x + r, r, r, x, y + h - r, y + r, r, r, x + r, y))


def top_edge(x, y, w, r):
    """Only the top arc of a rounded rect - the specular highlight."""
    return ("M%s,%s A%s,%s 0 0 1 %s,%s H%s A%s,%s 0 0 1 %s,%s" % (
        x + 1, y + r, r, r, x + r, y + 1, x + w - r, r, r, x + w - 1, y + r))


# ---------------------------------------------------------------- defs
def base_defs(scope):
    """Filters and gradients every panel shares. `scope` keeps ids unique."""
    s = scope
    return """
  <defs>
    <linearGradient id="pane_S" x1="0" y1="0" x2="0.7" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.115"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.052"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.022"/>
    </linearGradient>

    <linearGradient id="rim_S" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.46"/>
      <stop offset="22%" stop-color="#ffc857" stop-opacity="0.18"/>
      <stop offset="48%" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="74%" stop-color="#ff4fa0" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2ee6ff" stop-opacity="0.34"/>
    </linearGradient>

    <linearGradient id="refr_S" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2ee6ff" stop-opacity="0"/>
      <stop offset="30%" stop-color="#2ee6ff" stop-opacity="0.45"/>
      <stop offset="70%" stop-color="#ff4fa0" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#ff4fa0" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="spec_S" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="22%" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="60%" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="sheen_S" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.17"/>
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0.17"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bg_S" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="BG1_"/>
      <stop offset="55%" stop-color="BG0_"/>
      <stop offset="100%" stop-color="BG0_"/>
    </linearGradient>

    <radialGradient id="vig_S" cx="50%" cy="42%" r="72%">
      <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.28"/>
    </radialGradient>

    <filter id="blob_S" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="96"/>
    </filter>
    <filter id="soft_S" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <filter id="glow_S" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowS_S" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="1.8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="drop_S" x="-30%" y="-30%" width="160%" height="180%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000000" flood-opacity="0.55"/>
    </filter>
    <filter id="dropS_S" x="-30%" y="-30%" width="160%" height="180%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.45"/>
    </filter>

    <filter id="grain_S" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.032"/></feComponentTransfer>
    </filter>

    <pattern id="grid_S" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="11" cy="11" r="0.9" fill="#ffffff" fill-opacity="0.05"/>
    </pattern>
    <pattern id="scan_S" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#000000" fill-opacity="0.16"/>
    </pattern>
  </defs>""".replace("_S", "_" + s).replace("BG1_", BG1).replace("BG0_", BG0)


BASE_CSS = """
    .mono { font-family:MONO_; }
    .sans { font-family:SANS_; }
    text { font-family:SANS_; }
    @keyframes drift  { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(38px,-26px) scale(1.14)} }
    @keyframes drift2 { 0%,100%{transform:translate(0,0) scale(1.06)} 50%{transform:translate(-44px,30px) scale(.9)} }
    @keyframes drift3 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(26px,34px)} }
    @keyframes breathe{ 0%,100%{opacity:.30} 50%{opacity:.72} }
    @keyframes blink  { 0%,45%{opacity:1} 50%,95%{opacity:.15} 100%{opacity:1} }
    @keyframes sweep  { 0%{transform:translateX(-115%)} 62%,100%{transform:translateX(115%)} }
    @keyframes rise   { 0%{transform:translateY(0);opacity:0} 12%{opacity:.75} 86%{opacity:.75} 100%{transform:translateY(-180px);opacity:0} }
    @keyframes spin   { from{transform:rotate(0)} to{transform:rotate(360deg)} }
    @keyframes spinR  { from{transform:rotate(360deg)} to{transform:rotate(0)} }
""".replace("MONO_", MONO).replace("SANS_", SANS)


# --- staggered entrances -------------------------------------------------
# The stagger is baked into the keyframe percentages rather than expressed as
# animation-delay + fill-mode:both. That matters: with fill-mode the element
# sits at opacity 0 until its animation starts, so anything that stops the
# animation running (a renderer that samples frame 0, a cached first paint)
# leaves the card blank. Here the element's own attributes are already the
# final state, so no animation at all still renders a complete, correct card.
EV_N = 26
EV_DUR = 1.7
EV_STEP = 0.105


def _stagger_css():
    # Deliberately fades in from 0.5, not from 0. A profile README is the first
    # thing a visitor sees, and anything that samples the very first frame -
    # an image preview, a slow decode, a client that doesn't run the animation
    # to completion - would otherwise catch a page of blank cards. Starting
    # half-lit means the worst case is "dimmer than intended", never "empty",
    # while the cascade still reads as a reveal.
    out = []
    for i in range(EV_N):
        hold = min(72.0, (i * EV_STEP) / EV_DUR * 100.0)
        out.append("@keyframes ev%d{0%%,%.1f%%{opacity:.5;transform:translateY(14px)}"
                   "100%%{opacity:1;transform:translateY(0)}}" % (i, hold))
        out.append(".ev%d{animation:ev%d %.2fs cubic-bezier(.22,1,.36,1);}" % (i, i, EV_DUR))
    return "\n    ".join(out)


BASE_CSS += "    " + _stagger_css() + "\n"


def ev(i):
    """Class attribute for the i-th staggered entrance."""
    return "ev%d" % min(int(i), EV_N - 1)


def lighten(hexcol, amt=0.42):
    """Pull a colour toward white - used so a dark language colour stays legible."""
    h = hexcol.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return hexcol
    r, g, b = (int(c + (255 - c) * amt) for c in (r, g, b))
    return "#%02x%02x%02x" % (r, g, b)


# ---------------------------------------------------------------- pieces
def frame(scope, w, h, blobs=None, grid=True, vignette=True):
    """Flat backdrop in GitHub's own dark page colour, plus a faint dot grid.

    Deliberately no drifting colour blobs, vignette or gradient wash: on a
    profile those read as generic filler, and a flat base lets the panels
    melt into the page so the README reads as one canvas. Colour comes only
    from intentional places - accents, card tints, the hero sun. `blobs` and
    `vignette` are accepted and ignored so the panel code stays unchanged.
    """
    s = scope
    out = ['<rect width="%s" height="%s" fill="%s"/>' % (w, h, BG0)]
    if grid:
        out.append('<rect width="%s" height="%s" fill="url(#grid_%s)"/>' % (w, h, s))
    return "\n  ".join(out)


def grain(scope, w, h):
    return ('<rect width="%s" height="%s" rx="26" filter="url(#grain_%s)" opacity="0.9" '
            'style="mix-blend-mode:overlay"/>' % (w, h, scope))


def card(scope, x, y, w, h, r=18, tint=None, tint_op=0.16, shadow=True,
         sheen=False, sheen_delay=0, cls="", style=""):
    """One frosted-glass pane."""
    s = scope
    attrs = ""
    if cls:
        attrs += ' class="%s"' % cls
    if style:
        attrs += ' style="%s"' % style
    g = ["<g%s>" % attrs]
    # Performance: these panels are <img> SVGs, and while any animation in
    # the image runs the browser repaints the whole image every frame -
    # including every filter. So the glass is built from filter-free parts:
    # the shadow is an offset translucent copy of the pane, and the inner
    # tint light is a radial gradient rather than a blurred ellipse.
    if shadow:
        g.append('<path d="%s" fill="#000000" fill-opacity="0.32" transform="translate(0 7)"/>'
                 % rr(x + 3, y, w - 6, h, r))
    if tint:
        gid = uid("tg")
        g.append('<radialGradient id="%s" cx="0.3" cy="0.05" r="0.85">'
                 '<stop offset="0" stop-color="%s" stop-opacity="%.3f"/>'
                 '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
                 % (gid, tint, min(1.0, tint_op * 1.7), tint))
    g.append('<path d="%s" fill="%s"/>' % (rr(x, y, w, h, r), BG0))
    if tint:
        g.append('<path d="%s" fill="url(#%s)"/>' % (rr(x, y, w, h, r), gid))
    g.append('<path d="%s" fill="url(#pane_%s)"/>' % (rr(x, y, w, h, r), s))
    g.append('<path d="%s" fill="none" stroke="url(#rim_%s)" stroke-width="1.2"/>'
             % (rr(x, y, w, h, r), s))
    g.append('<path d="%s" fill="none" stroke="url(#spec_%s)" stroke-width="1.4"/>'
             % (top_edge(x, y, w, r), s))
    if h > 60:
        g.append('<rect x="%.0f" y="%.1f" width="%.0f" height="1.2" rx="0.6" fill="url(#refr_%s)"/>'
                 % (x + r, y + h - 2.5, w - 2 * r, s))
    if sheen:
        cid = uid("cl")
        g.append('<clipPath id="%s"><path d="%s"/></clipPath>'
                 '<g clip-path="url(#%s)"><rect x="%.0f" y="%s" width="%.0f" height="%s" '
                 'fill="url(#sheen_%s)" style="animation:sweep 6.5s cubic-bezier(.4,0,.2,1) %ss infinite"/></g>'
                 % (cid, rr(x, y, w, h, r), cid, x - w * 0.5, y, w * 0.5, h, s, sheen_delay))
    g.append("</g>")
    return "\n  ".join(g)


def chip(scope, x, y, label, col=None, pad=11, fs=11.5, h=23, mono=True):
    """Small glass token. Returns (svg, width)."""
    col = col or DIM
    w = int(len(label) * (fs * 0.62) + pad * 2)
    cls = "mono" if mono else "sans"
    sv = ('<g><rect x="%s" y="%s" width="%s" height="%s" rx="%.1f" fill="#ffffff" '
          'fill-opacity="0.055" stroke="%s" stroke-opacity="0.32" stroke-width="1"/>'
          '<text class="%s" x="%.0f" y="%.0f" text-anchor="middle" font-size="%s" fill="%s" '
          'fill-opacity="0.95" letter-spacing="0.4">%s</text></g>'
          % (x, y, w, h, h / 2.0, col, cls, x + w / 2.0, y + h / 2.0 + 4, fs, col, esc(label)))
    return sv, w


def chip_row(scope, x, y, labels, cols=None, gap=7, **kw):
    out, cx = [], x
    for i, l in enumerate(labels):
        c = cols[i % len(cols)] if cols else None
        sv, w = chip(scope, cx, y, l, c, **kw)
        out.append(sv)
        cx += w + gap
    return "\n  ".join(out), cx - x - gap


def xpbar(scope, x, y, w, pct, col, h=7, delay=0.0, dur=1.6, track=0.10):
    """XP / proficiency bar.

    Two deliberate choices, both so the bar never looks broken on the first
    painted frame: it grows from a visible stub rather than from zero, and the
    stagger is expressed as a longer duration rather than an animation-delay
    (a delay without fill-mode would show the full bar, then snap back to the
    start once the animation kicked in).
    """
    fill = w * pct / 100.0
    start = min(max(fill * 0.18, h), fill)
    total = dur + delay
    k = uid("xp")
    return ("""<g>
    <rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#ffffff" fill-opacity="%s"/>
    <style>@keyframes %s{from{width:%.1fpx}to{width:%.1fpx}}
    .%s{animation:%s %.2fs cubic-bezier(.22,1,.36,1);}</style>
    <rect class="%s" x="%s" y="%s" width="%.1f" height="%s" rx="%s" fill="%s" filter="url(#glowS_%s)"/>
    <rect class="%s" x="%s" y="%s" width="%.1f" height="%s" rx="%s" fill="#ffffff" fill-opacity="0.45"/>
  </g>""" % (x, y, w, h, h / 2.0, track,
             k, start, fill, k, k, total,
             k, x, y, fill, h, h / 2.0, col, scope,
             k, x, y, fill, h, h / 2.0))


def ring(scope, cx, cy, r, pct, col, sw=6, delay=0.0, dur=1.8, track=0.10):
    """Circular progress ring. Same reasoning as xpbar: it sweeps in from a
    short visible arc, and staggers by duration rather than by delay."""
    c = 2 * 3.14159265 * r
    end = c * (1 - pct / 100.0)
    start = c * (1 - pct * 0.18 / 100.0)
    total = dur + delay
    k = uid("rg")
    return ("""<g>
    <circle cx="%s" cy="%s" r="%s" fill="none" stroke="#ffffff" stroke-opacity="%s" stroke-width="%s"/>
    <style>@keyframes %s{from{stroke-dashoffset:%.1f}to{stroke-dashoffset:%.1f}}
    .%s{animation:%s %.2fs cubic-bezier(.22,1,.36,1);}</style>
    <circle class="%s" cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"
            stroke-linecap="round" stroke-dasharray="%.1f" stroke-dashoffset="%.1f"
            transform="rotate(-90 %s %s)" filter="url(#glowS_%s)"/>
  </g>""" % (cx, cy, r, track, sw,
             k, start, end, k, k, total,
             k, cx, cy, r, col, sw, c, end, cx, cy, scope))


def section_header(scope, x, y, kicker, title, col=CREAM):
    """Hex bullet + uppercase kicker + display title."""
    return ("""<g class="ev0">
    <g transform="translate(%s,%s)">
      <path d="M0,-9 L7.8,-4.5 L7.8,4.5 L0,9 L-7.8,4.5 L-7.8,-4.5 Z" fill="none"
            stroke="%s" stroke-opacity="0.75" stroke-width="1.4"/>
      <circle r="3" fill="%s" style="animation:breathe 2.4s ease-in-out infinite"/>
    </g>
    <text class="mono" x="%s" y="%s" font-size="11.5" letter-spacing="3.4" fill="%s"
          fill-opacity="0.9" font-weight="600">%s</text>
    <text x="%s" y="%s" font-size="25" font-weight="700" fill="%s" letter-spacing="-0.4">%s</text>
  </g>""" % (x + 9, y - 6, col, col, x + 28, y - 1, col, esc(kicker), x, y + 27, INK, esc(title)))


def particles(scope, w, h, n=16, col=CREAM, seed=7):
    """Slow upward motes - cheap life without stealing attention."""
    import random
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(30, w - 30)
        y = rnd.uniform(h * 0.35, h - 12)
        r = rnd.uniform(0.9, 2.2)
        d = rnd.uniform(9, 18)
        dl = rnd.uniform(0, 12)
        c = col if i % 3 else ROSE
        # kept faint: any brighter and a mote drifting behind a glass card
        # reads as a stray full stop next to the text
        out.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="0.3" '
                   'style="animation:rise %.1fs linear %.1fs infinite"/>' % (x, y, r, c, d, dl))
    return "\n  ".join(out)


def svg_open(w, h):
    # xlink is declared because <image href> is SVG2; older renderers still
    # want xlink:href, and the embedded avatar has to resolve in both.
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'viewBox="0 0 %s %s" width="%s" height="%s" role="img">' % (w, h, w, h))


_FILTER_ATTR = re.compile(r'\s+filter="url\(#(?:glow|glowS|drop|dropS|soft|blob)_[A-Za-z0-9]+\)"')


def page(scope, w, h, css, body, blobs=None, grid=True, use_grain=False,
         use_particles=0, pcol=CREAM):
    # Every blur / drop-shadow filter is stripped from the finished panel.
    # In an animated <img> SVG they are re-run on every frame, which is what
    # made the profile stutter. Glows are carried by gradients and layered
    # strokes instead; grain (a full-canvas feTurbulence in overlay blend)
    # is off for the same reason.
    body = _FILTER_ATTR.sub("", body)
    parts = [svg_open(w, h), base_defs(scope),
             "<style>" + BASE_CSS + css + "</style>",
             frame(scope, w, h, blobs, grid)]
    if use_particles:
        parts.append(particles(scope, w, h, use_particles, pcol))
    parts.append(body)
    if use_grain:
        parts.append(grain(scope, w, h))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------- neo-brutalism
# The story layer (chapter cards, stickers, the PRESS START tag) is drawn
# neo-brutalist on purpose: solid saturated blocks, a thick ink border and a
# hard zero-blur offset shadow. Against the soft glass panels that contrast is
# what makes a chapter break read as a chapter break.
INKK = "#0a0f14"   # brutalist ink - near-black, used for borders and text on blocks


def brut(x, y, w, h, fill, shadow=ROSE, r=10, off=6, bw=2.6, cls="", style=""):
    attrs = (' class="%s"' % cls if cls else "") + (' style="%s"' % style if style else "")
    return ('<g%s><rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/></g>'
            % (attrs, x + off, y + off, w, h, r, shadow, INKK, bw,
               x, y, w, h, r, fill, INKK, bw))


def sticker(x, y, label, fill=CREAM, shadow=ROSE, fs=11, h=26, rot=0, off=4):
    """A brutalist label block. Returns (svg, width)."""
    w = int(len(label) * fs * 0.64 + 24)
    t = ' transform="rotate(%s %s %s)"' % (rot, x + w / 2, y + h / 2) if rot else ""
    sv = ('<g%s>%s<text class="mono" x="%.1f" y="%.1f" text-anchor="middle" font-size="%s" '
          'font-weight="800" letter-spacing="1.4" fill="%s">%s</text></g>'
          % (t, brut(x, y, w, h, fill, shadow, r=6, off=off, bw=2.2),
             x + w / 2, y + h / 2 + fs * 0.36, fs, INKK, esc(label)))
    return sv, w
