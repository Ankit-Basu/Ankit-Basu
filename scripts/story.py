"""
The story-mode panels: the hero with the self-drawing portrait, the chapter
cards, the origin timeline, the 3D contribution city and the project vault.

The look is a deliberate hybrid. Content sits on frosted glass (design.card);
the narrative layer that frames it - chapter numerals, rarity stickers, the
PRESS START tag - is neo-brutalist (design.brut / design.sticker): flat
saturated blocks, thick ink borders, hard offset shadows.

Every animation here follows the same rule as the rest of the profile: the
element's own attributes are its resting, fully-rendered state, so a renderer
that never runs the animation still shows a complete panel.
"""
import json
import math
import os

import profile as P
from design import (BG0, BG2, INK, DIM, FAINT, CREAM, ROSE, MINT, VIOLET, PURPLE, INKK, RARITY,
                    esc, rr, card, chip_row, page, section_header, uid, ev,
                    brut, sticker)
from icons import icon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 1200
PAD = 46

TIERS = [(3000, "GRANDMASTER"), (1500, "ARCHITECT"), (700, "ENGINEER"),
         (250, "BUILDER"), (0, "INITIATE")]


def fmt(n):
    return "-" if n is None else format(int(n), ",")


def _read(rel):
    p = os.path.join(ROOT, rel)
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else None


# ================================================================ hero
PORTRAIT_CYCLE = 16  # seconds for one draw -> reveal -> hold -> reset loop


def _portrait(s, fx, fy, size):
    """The sketch draws itself stroke by stroke, the photo resolves through it,
    holds, and the whole thing resets. Resting state: photo + faint lines."""
    sk = _read("data/sketch.json")
    av = _read("data/avatar.txt")
    sk = json.loads(sk) if sk else {"paths": [], "waves": 1, "box": 1000}
    waves = sk.get("waves", 12)
    scale = size / float(sk.get("box", 1000))
    T = PORTRAIT_CYCLE

    css = []
    for wv in range(waves + 1):
        if wv == 0:
            a, b = 1.0, 14.0
        else:
            a = 8.0 + (wv - 1) * 3.4
            b = a + 9.0
        css.append(
            "@keyframes dw%d{0%%,%.1f%%{stroke-dashoffset:1;opacity:1}"
            "%.1f%%,58%%{stroke-dashoffset:0;opacity:1}70%%,88%%{stroke-dashoffset:0;opacity:.22}"
            "95%%,100%%{stroke-dashoffset:0;opacity:0}}"
            ".w%d{animation:dw%d %ds cubic-bezier(.45,.05,.35,1) infinite}" % (wv, a, b, wv, wv, T))
    css.append("@keyframes phot{0%,50%{opacity:0}64%,90%{opacity:1}97%,100%{opacity:0}}"
               ".phot{animation:phot " + str(T) + "s ease-in-out infinite}")
    css.append("@keyframes scn{0%%{transform:translateY(0);opacity:.95}55%%{transform:translateY(%dpx);opacity:.95}"
               "56%%,100%%{transform:translateY(%dpx);opacity:0}}"
               ".scn{animation:scn %ds linear infinite}" % (size, size, T))
    # HUD captions that narrate the loop
    css.append("@keyframes hud1{0%,51%{opacity:1}52%,100%{opacity:0}}"
               "@keyframes hud2{0%,51%{opacity:0}52%,92%{opacity:1}93%,100%{opacity:0}}"
               "@keyframes hud3{0%,92%{opacity:0}93%,100%{opacity:1}}"
               + "".join(".hud%d{animation:hud%d %ds steps(1) infinite}" % (k, k, T) for k in (1, 2, 3)))

    cx, cy = fx + size / 2, fy + size / 2
    clip, msk = "pf_" + s, "pm_" + s
    out = [f"""<defs>
    <clipPath id="{clip}"><path d="{rr(fx, fy, size, size, 46)}"/></clipPath>
    <linearGradient id="ink_{s}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1000">
      <stop offset="0%" stop-color="{MINT}"/><stop offset="50%" stop-color="{CREAM}"/>
      <stop offset="100%" stop-color="{ROSE}"/>
    </linearGradient>
    <linearGradient id="scg_{s}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{MINT}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{MINT}" stop-opacity="1"/>
      <stop offset="100%" stop-color="{MINT}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="pvg_{s}" cx="50%" cy="40%" r="70%">
      <stop offset="55%" stop-color="{BG0}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{BG0}" stop-opacity="0.55"/>
    </radialGradient>
    <mask id="{msk}" maskUnits="userSpaceOnUse" x="{fx}" y="{fy}" width="{size}" height="{size}">
      <circle cx="{cx - size * 0.08:.0f}" cy="{cy - size * 0.1:.0f}" r="{size * 0.9:.0f}" fill="#ffffff">
        <animate attributeName="r" values="0;0;{size * 0.9:.0f};{size * 0.9:.0f}"
                 keyTimes="0;0.5;0.66;1" dur="{T}s" repeatCount="indefinite"
                 calcMode="spline" keySplines="0 0 1 1;0.22 1 0.36 1;0 0 1 1"/>
      </circle>
    </mask>
  </defs>"""]

    # glass plinth behind the frame
    out.append(card(s, fx - 16, fy - 16, size + 32, size + 32, r=58, tint=VIOLET, tint_op=0.18))
    out.append(f'<g clip-path="url(#{clip})">')
    out.append(f'<rect x="{fx}" y="{fy}" width="{size}" height="{size}" fill="{BG0}" fill-opacity="0.72"/>')
    out.append(f'<rect x="{fx}" y="{fy}" width="{size}" height="{size}" fill="url(#grid_{s})"/>')
    if av:
        out.append(f'<g class="phot" mask="url(#{msk})">'
                   f'<image x="{fx}" y="{fy}" width="{size}" height="{size}" '
                   f'preserveAspectRatio="xMidYMid slice" href="{av}" xlink:href="{av}"/>'
                   f'<rect x="{fx}" y="{fy}" width="{size}" height="{size}" fill="url(#pvg_{s})"/></g>')
    out.append(f'<g transform="translate({fx},{fy}) scale({scale:.4f})" fill="none" '
               f'stroke="url(#ink_{s})" stroke-linecap="round" stroke-linejoin="round" '
               f'filter="url(#glowS_{s})">')
    for p in sk["paths"]:
        sw = 7.5 if p.get("k") == "sil" else 5.2
        out.append(f'<path class="w{p["w"]}" d="{p["d"]}" stroke-width="{sw}" pathLength="1" '
                   f'stroke-dasharray="1 1" stroke-dashoffset="0" opacity="0.22"/>')
    out.append("</g>")
    out.append(f'<rect class="scn" x="{fx}" y="{fy - 1}" width="{size}" height="2.4" '
               f'fill="url(#scg_{s})" opacity="0" filter="url(#glowS_{s})"/>')
    out.append("</g>")
    # corner brackets: a camera viewfinder framing the subject
    L = 22
    for (bx, by, dx, dy) in [(fx + 14, fy + 14, 1, 1), (fx + size - 14, fy + 14, -1, 1),
                             (fx + 14, fy + size - 14, 1, -1), (fx + size - 14, fy + size - 14, -1, -1)]:
        out.append(f'<path d="M{bx} {by + dy * L}V{by}H{bx + dx * L}" fill="none" stroke="{CREAM}" '
                   f'stroke-opacity="0.75" stroke-width="2"/>')
    out.append(f'<path d="{rr(fx, fy, size, size, 46)}" fill="none" stroke="url(#rim_{s})" stroke-width="1.6"/>')

    n = len(sk["paths"])
    hy = fy + size + 46
    out.append(f"""<g class="mono" font-size="10.4" letter-spacing="1.8" text-anchor="middle">
    <text class="hud1" x="{cx}" y="{hy}" fill="{MINT}" opacity="0">&#9679; TRACING {n} STROKES&#8230;</text>
    <text class="hud2" x="{cx}" y="{hy}" fill="{CREAM}">&#9679; RENDER COMPLETE &#183; PLAYER ONLINE</text>
    <text class="hud3" x="{cx}" y="{hy}" fill="{ROSE}" opacity="0">&#9679; RESPAWNING&#8230;</text>
  </g>""")
    return "\n  ".join(out), "\n    ".join(css)


def _typing(s, x, y, roles, fs=21):
    """Roles type out, hold, delete, and hand over to the next. Resting state
    is the first role, fully typed."""
    n = len(roles)
    cw = fs * 0.602
    slot = 100.0 / n
    T = 3.2 * n
    css, out = [], []
    caret = [(0.0, 0.0)]
    for i, role in enumerate(roles):
        full = len(role) * cw
        a = i * slot
        b, c, d = a + slot * 0.38, a + slot * 0.80, a + slot * 0.96
        k = "ty%d" % i
        css.append("@keyframes %s{0%%,%.2f%%{width:0;opacity:1}%.2f%%,%.2f%%{width:%.1fpx}"
                   "%.2f%%,100%%{width:0}}" % (k, a, b, c, full, d))
        css.append("@keyframes %so{0%%,%.2f%%{opacity:0}%.2f%%,%.2f%%{opacity:1}%.2f%%,100%%{opacity:0}}"
                   % (k, max(a - 0.01, 0), a + 0.01, d, min(d + 0.01, 100)))
        css.append(".%s{animation:%s %.1fs linear infinite}.%so{animation:%so %.1fs steps(1) infinite}"
                   % (k, k, T, k, k, T))
        caret += [(a, 0.0), (b, full), (c, full), (d, 0.0)]
        cid = uid("tc")
        out.append(f'<clipPath id="{cid}"><rect class="{k}" x="{x}" y="{y - fs}" '
                   f'width="{full + 2 if i == 0 else 0:.1f}" height="{fs * 1.5}"/></clipPath>')
        # textLength pins the rendered width, so the caret lands on the last
        # letter whichever monospace font the viewer's system substitutes
        out.append(f'<text class="mono {k}o" x="{x}" y="{y}" font-size="{fs}" font-weight="700" '
                   f'textLength="{full:.1f}" lengthAdjust="spacingAndGlyphs" '
                   f'fill="{CREAM}" clip-path="url(#{cid})" opacity="{1 if i == 0 else 0}">{esc(role)}</text>')
    caret.append((100.0, 0.0))
    frames = "".join("%.2f%%{transform:translateX(%.1fpx)}" % (p, v) for p, v in caret)
    css.append("@keyframes tcar{%s}.tcar{animation:tcar %.1fs linear infinite}" % (frames, T))
    out.append(f'<rect class="tcar" x="{x + 3}" y="{y - fs * 0.82:.1f}" width="{fs * 0.5:.1f}" '
               f'height="{fs * 0.98:.1f}" fill="{MINT}" style="transform:translateX({len(roles[0]) * cw:.1f}px)">'
               f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" '
               f'repeatCount="indefinite"/></rect>')
    return "\n  ".join(out), "\n    ".join(css)


def _horizon(s, H, sun=None, hy=None, depth=None):
    """Synthwave horizon: an optional striped sun sinking behind the horizon
    line and a perspective grid floor whose rows scroll toward the viewer.
    Resting state: the rows sit at their evenly-receding positions."""
    hy = hy or H - 150
    depth = depth or H - hy
    vx = W / 2
    clip = "hzc_" + s
    out = [f"""<defs>
    <clipPath id="{clip}"><path d="{rr(0, 0, W, H, 20)}"/></clipPath>
    <linearGradient id="sun_{s}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{CREAM}"/><stop offset="55%" stop-color="{ROSE}"/>
      <stop offset="100%" stop-color="{PURPLE}"/>
    </linearGradient>
    <linearGradient id="flr_{s}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{ROSE}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{PURPLE}" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="hzl_{s}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ROSE}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{ROSE}" stop-opacity="1"/>
      <stop offset="100%" stop-color="{ROSE}" stop-opacity="0"/>
    </linearGradient>
  </defs>""", f'<g clip-path="url(#{clip})">']
    css = ["@keyframes flr{from{transform:translateY(0);opacity:0}25%%{opacity:.85}"
           "to{transform:translateY(%dpx);opacity:.85}}" % depth,
           "@keyframes sunb{0%,100%{opacity:.82}50%{opacity:1}}",
           "@keyframes band{from{transform:translateY(0)}to{transform:translateY(-18px)}}"]
    if sun:
        sx, sy, sr = sun
        msk = "sunm_" + s
        # stripes thicken toward the horizon - the classic sliced sun
        bands = "".join(
            f'<rect x="{sx - sr}" y="{sy + sr * f:.1f}" width="{2 * sr}" height="{2 + k * 1.6:.1f}" fill="#000"/>'
            for k, f in enumerate([0.02, 0.18, 0.32, 0.45, 0.56, 0.66, 0.75, 0.83, 0.9, 0.96]))
        out.append(f"""<mask id="{msk}" maskUnits="userSpaceOnUse" x="{sx - sr}" y="{sy - sr}" width="{2 * sr}" height="{2 * sr}">
      <rect x="{sx - sr}" y="{sy - sr}" width="{2 * sr}" height="{hy - (sy - sr)}" fill="#fff"/>
      <g style="animation:band 2.6s linear infinite">{bands}</g>
    </mask>
    <radialGradient id="halo_{s}"><stop offset="0.6" stop-color="{ROSE}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{ROSE}" stop-opacity="0"/></radialGradient>
    <circle cx="{sx}" cy="{sy}" r="{sr * 1.45:.0f}" fill="url(#halo_{s})"/>
    <circle cx="{sx}" cy="{sy}" r="{sr}" fill="url(#sun_{s})" mask="url(#{msk})"
            style="animation:sunb 5s ease-in-out infinite"/>""")
    out.append(f'<rect x="0" y="{hy}" width="{W}" height="{H - hy}" fill="{BG0}" fill-opacity="0.55"/>')
    out.append(f'<rect x="0" y="{hy}" width="{W}" height="{H - hy}" fill="url(#flr_{s})"/>')
    rays = []
    for k in range(-14, 15):
        rays.append(f'<path d="M{vx + k * 26:.0f} {hy}L{vx + k * 150:.0f} {H}"/>')
    out.append(f'<g stroke="{ROSE}" stroke-opacity="0.38" stroke-width="1">{"".join(rays)}</g>')
    n, T = 7, 4.2
    for i in range(n):
        # quadratic spacing is what sells the perspective
        rest = depth * ((i + 0.5) / n) ** 2
        out.append(f'<rect x="0" y="{hy}" width="{W}" height="1.2" fill="{ROSE}" opacity="0.7" '
                   f'transform="translate(0 {rest:.1f})" '
                   f'style="animation:flr {T}s cubic-bezier(.55,0,1,.45) {-T * i / n:.2f}s infinite"/>')
    # sky glow over the horizon: a gradient band, not a blur
    out.append(f'<linearGradient id="sky_{s}" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0" stop-color="{ROSE}" stop-opacity="0"/>'
               f'<stop offset="1" stop-color="{ROSE}" stop-opacity="0.2"/></linearGradient>'
               f'<rect x="0" y="{hy - 70}" width="{W}" height="70" fill="url(#sky_{s})"/>')
    out.append(f'<rect x="0" y="{hy - 3}" width="{W}" height="6" fill="url(#hzl_{s})" opacity="0.35"/>'
               f'<rect x="0" y="{hy - 1}" width="{W}" height="2" fill="url(#hzl_{s})"/>')
    out.append("</g>")
    return "\n  ".join(out), "\n    ".join(css)


def build_hero(d):
    s = "h"
    H = 560
    x0 = PAD + 18
    tc = int(d.get("total_contributions") or 0)
    lvl = max(1, tc // 100)
    tier = next(t for c, t in TIERS if tc >= c)

    css = ["@keyframes nsweep{0%{transform:translateX(-280px)}58%,100%{transform:translateX(620px)}}",
           "@keyframes orbit{from{transform:rotate(0)}to{transform:rotate(360deg)}}",
           "@keyframes pop{0%,100%{transform:scale(1)}50%{transform:scale(1.14)}}",
           "@keyframes wob{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(-1deg) translateY(-2px)}}"]
    body = [f"""<defs>
    <linearGradient id="nm_{s}" x1="0" y1="0" x2="1" y2="0.5">
      <stop offset="0%" stop-color="#ffffff"/><stop offset="34%" stop-color="{CREAM}"/>
      <stop offset="68%" stop-color="{ROSE}"/><stop offset="100%" stop-color="{MINT}"/>
    </linearGradient>
    <clipPath id="nc_{s}">
      <text class="sans" x="{x0 - 2}" y="196" font-size="80" font-weight="800"
            letter-spacing="-2.8">{esc(P.NAME)}</text>
    </clipPath>
  </defs>"""]
    hz, scss = _horizon(s, H, sun=(968, 250, 178))
    css.append(scss)
    body.append(hz)

    # -- PRESS START sticker (brutalist) + availability pill (glass)
    st, sw = sticker(x0, 53, "PRESS START", CREAM, fs=10.4, h=28)
    body.append(f'<g class="ev1">{st}</g>')
    px = x0 + sw + 22
    body.append(f"""<g class="ev1">
    {card(s, px, 53, 366, 28, r=14, tint=MINT, tint_op=0.2, shadow=False)}
    <circle cx="{px + 20}" cy="67" r="4.5" fill="{MINT}" filter="url(#glow_{s})"
            style="animation:pop 1.9s ease-in-out infinite;transform-origin:{px + 20}px 67px"/>
    <circle cx="{px + 20}" cy="67" r="9" fill="none" stroke="{MINT}" stroke-width="1.2" opacity="0.5">
      <animate attributeName="r" values="5;14;5" dur="2.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".65;0;.65" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <text class="mono" x="{px + 36}" y="71" font-size="10.8" letter-spacing="2.1"
          fill="{MINT}" font-weight="600">{esc(P.STATUS)}</text>
  </g>""")

    body.append(f'<text class="mono ev2" x="{x0}" y="122" font-size="11" letter-spacing="3.6" '
                f'fill="{DIM}">PROLOGUE &#183; A STORY IN SIX CHAPTERS</text>')

    # -- name with sheen
    body.append(f"""<g class="ev2">
    <text class="sans" x="{x0 - 2}" y="196" font-size="80" font-weight="800"
          letter-spacing="-2.8" fill="url(#nm_{s})">{esc(P.NAME)}</text>
    <g clip-path="url(#nc_{s})">
      <rect x="{x0 - 60}" y="120" width="160" height="90" fill="url(#sheen_{s})"
            style="animation:nsweep 5.5s cubic-bezier(.4,0,.2,1) 1.2s infinite"/>
    </g>
  </g>""")

    # -- typing roles
    ty, tcss = _typing(s, x0 + 30, 244, P.ROLES)
    css.append(tcss)
    body.append(f'<g class="ev3"><text class="mono" x="{x0}" y="244" font-size="21" '
                f'font-weight="700" fill="{MINT}">&gt;_</text>{ty}</g>')

    body.append(f'<rect class="ev3" x="{x0}" y="266" width="560" height="1" fill="url(#spec_{s})" opacity="0.7"/>')
    for i, line in enumerate(P.STORY):
        body.append(f'<text class="ev4" x="{x0}" y="{298 + i * 23}" font-size="15.5" fill="{DIM}">{esc(line)}</text>')

    chips, _ = chip_row(s, x0, 372, P.HERO_CHIPS, cols=[CREAM, ROSE, MINT, VIOLET], gap=8, fs=11, h=26)
    body.append(f'<g class="ev5">{chips}</g>')

    # -- no stat tiles here: the HUD directly under the hero carries the
    #    numbers. The floor gets a quiet cue into the story instead.
    css.append("@keyframes cue{0%,100%{transform:translateY(0);opacity:.35}50%{transform:translateY(5px);opacity:1}}"
               ".cue{animation:cue 2.2s ease-in-out infinite}")
    body.append(f'<g class="ev6"><text class="mono" x="{x0}" y="476" font-size="10" letter-spacing="3.2" '
                f'fill="{DIM}">SCROLL TO BEGIN</text>'
                f'<path class="cue" d="M{x0 + 176} 466l6 6 6-6" fill="none" stroke="{MINT}" stroke-width="1.6" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path class="cue" style="animation-delay:-.3s" d="M{x0 + 176} 474l6 6 6-6" fill="none" '
                f'stroke="{MINT}" stroke-opacity="0.5" stroke-width="1.6" stroke-linecap="round" '
                f'stroke-linejoin="round"/></g>')

    # -- portrait with orbits and the level badge
    size = 300
    fx, fy = 818, 92
    cx, cy = fx + size / 2, fy + size / 2
    body.append(f"""<g class="ev2">
    <circle cx="{cx}" cy="{cy}" r="206" fill="none" stroke="{CREAM}" stroke-opacity="0.16"
            stroke-width="1" stroke-dasharray="2 10"
            style="animation:orbit 40s linear infinite;transform-origin:{cx}px {cy}px"/>
    <circle cx="{cx}" cy="{cy}" r="190" fill="none" stroke="{ROSE}" stroke-opacity="0.2"
            stroke-width="1.4" stroke-dasharray="44 18"
            style="animation:orbit 26s linear infinite reverse;transform-origin:{cx}px {cy}px"/>
    <g style="animation:orbit 18s linear infinite;transform-origin:{cx}px {cy}px">
      <circle cx="{cx + 190}" cy="{cy}" r="4" fill="{MINT}" filter="url(#glow_{s})"/>
    </g>
  </g>""")
    pt, pcss = _portrait(s, fx, fy, size)
    css.append(pcss)
    body.append(f'<g class="ev3">{pt}</g>')

    bx, by = fx + size - 6, fy + size - 6
    body.append(f"""<g class="ev5">
    {brut(bx - 34, by - 34, 68, 68, CREAM, ROSE, r=12, off=5)}
    <text class="mono" x="{bx}" y="{by - 9}" text-anchor="middle" font-size="9" font-weight="800"
          letter-spacing="1.6" fill="{INKK}">LVL</text>
    <text class="sans" x="{bx}" y="{by + 17}" text-anchor="middle" font-size="26" font-weight="800"
          fill="{INKK}">{lvl}</text>
  </g>""")
    tl, tlw = sticker(fx - 6, fy - 30, tier, MINT, VIOLET, fs=10.5, h=26, rot=-4)
    body.append(f'<g class="ev5">{tl}</g>')

    blobs = [(250, 160, 240, CREAM, 0.28, "drift"),
             (640, 420, 220, ROSE, 0.24, "drift2"),
             (960, 200, 260, VIOLET, 0.28, "drift3"),
             (1120, 470, 180, MINT, 0.2, "drift")]
    return page(s, W, H, "\n    ".join(css), "\n  ".join(body), blobs)


# ================================================================ origin timeline
def build_timeline():
    s = "o"
    H = 600
    body = [section_header(s, PAD, 62, "WORLD MAP", "From level 1 to now", CREAM)]
    xs = [140, 370, 600, 830, 1060]
    y1, y2 = 176, 382
    nodes = [(x, y1) for x in xs] + [(x, y2) for x in reversed(xs)]
    pid = "trail_" + s
    dpath = (f"M70 {y1}H{xs[-1]}C1170 {y1} 1170 {y2} {xs[-1]} {y2}H70")
    css = ("@keyframes trail{0%,8%{stroke-dashoffset:.86}100%{stroke-dashoffset:0}}"
           ".trail{animation:trail 3.4s cubic-bezier(.45,.05,.35,1)}"
           )
    body.append(f'<path d="{dpath}" fill="none" stroke="#ffffff" stroke-opacity="0.07" stroke-width="8" '
                f'stroke-linecap="round"/>')
    body.append(f'<path id="{pid}" class="trail" d="{dpath}" fill="none" stroke="url(#refr_{s})" '
                f'stroke-width="2.4" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0"/>')
    body.append(f'<path d="{dpath}" fill="none" stroke="{CREAM}" stroke-opacity="0.35" stroke-width="1.4" '
                f'stroke-dasharray="2 9"/>')
    # the player, walking the story on loop
    body.append(f"""<g>
    <circle r="11" fill="{MINT}" fill-opacity="0.18"/>
    <rect x="-5.5" y="-5.5" width="11" height="11" rx="2" fill="{MINT}" stroke="{INKK}" stroke-width="1.6"
          transform="rotate(45)" filter="url(#glowS_{s})"/>
    <animateMotion dur="22s" repeatCount="indefinite" rotate="0" calcMode="linear">
      <mpath href="#{pid}" xlink:href="#{pid}"/>
    </animateMotion>
  </g>""")

    cw, ch = 218, 104
    for i, ((nx, ny), (when, title, l1, l2, col)) in enumerate(zip(nodes, P.TIMELINE)):
        last = i == len(P.TIMELINE) - 1
        cx = min(max(nx - cw / 2, PAD), W - PAD - cw)
        cy = ny + 26
        body.append(f'<g class="{ev(1 + i * 2)}">')
        body.append(f'<rect x="{nx - 0.5}" y="{ny + 10}" width="1" height="16" fill="{col}" opacity="0.5"/>')
        body.append(card(s, cx, cy, cw, ch, r=16, tint=col, tint_op=0.15, shadow=False))
        body.append(f'<text class="mono" x="{cx + 16}" y="{cy + 24}" font-size="9.8" letter-spacing="2" '
                    f'fill="{col}" font-weight="700">{when}</text>')
        body.append(f'<text class="sans" x="{cx + 16}" y="{cy + 47}" font-size="15" font-weight="700" '
                    f'fill="{INK}">{esc(title)}</text>')
        body.append(f'<text x="{cx + 16}" y="{cy + 68}" font-size="11" fill="{DIM}">{esc(l1)}</text>')
        body.append(f'<text x="{cx + 16}" y="{cy + 85}" font-size="11" fill="{DIM}">{esc(l2)}</text>')
        if last:
            body.append(f'<circle cx="{nx}" cy="{ny}" r="7" fill="none" stroke="{col}" stroke-width="1.6">'
                        f'<animate attributeName="r" values="7;22" dur="1.8s" repeatCount="indefinite"/>'
                        f'<animate attributeName="opacity" values=".9;0" dur="1.8s" repeatCount="indefinite"/></circle>')
            body.append(brut(nx - 9, ny - 9, 18, 18, col, ROSE, r=4, off=3, bw=2))
        else:
            body.append(f'<circle cx="{nx}" cy="{ny}" r="8" fill="{BG0}" stroke="{col}" stroke-width="2"/>'
                        f'<circle cx="{nx}" cy="{ny}" r="3.4" fill="{col}" filter="url(#glowS_{s})"/>')
        body.append("</g>")

    nx_, ny_ = nodes[len(P.TIMELINE) - 1]
    st, stw = sticker(nx_ - 30, ny_ - 58, "YOU ARE HERE ↓", MINT, ROSE, fs=10, h=24, rot=-3, off=3)
    body.append(f'<g class="ev20">{st}</g>')
    body.append(f'<text class="mono" x="{W // 2}" y="{H - 22}" text-anchor="middle" font-size="9.6" '
                f'letter-spacing="1.6" fill="{FAINT}">DATED FROM EACH REPOSITORY\'S FIRST COMMIT &#183; '
                f'THE CYAN DIAMOND IS ME, STILL WALKING</text>')
    blobs = [(240, 200, 250, CREAM, 0.2, "drift"), (700, 420, 250, ROSE, 0.18, "drift2"),
             (1040, 220, 230, MINT, 0.16, "drift3")]
    return page(s, W, H, css, "\n  ".join(body), blobs)


# ================================================================ 3D contribution city
def _shade(hexcol, k):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(c * k) for c in (r, g, b))


def build_city(d):
    s = "y"
    H = 520
    body = [section_header(s, PAD, 62, "CITY VIEW", "The city my commits built", VIOLET)]
    cal = d.get("calendar") or []
    weeks = 52
    recent = cal[-weeks * 7:]
    # align to whole weeks so each column is one Sunday-to-Saturday week
    peak = max([n for _, n in recent] or [1]) or 1
    active = sorted(n for _, n in recent if n > 0)
    cuts = [active[int(len(active) * q)] for q in (0.25, 0.5, 0.75)] if active else [1, 2, 3]
    ramp = [None, PURPLE, ROSE, CREAM, MINT]

    ox, oy = 150, 214
    a = (13.6, 4.0)    # one week along the street
    b = (-10.2, 6.0)   # one day across it
    k = 0.8
    cells = []
    for idx, (day, n) in enumerate(recent):
        w, dd = idx // 7, idx % 7
        px = ox + w * a[0] + dd * b[0]
        py = oy + w * a[1] + dd * b[1]
        cells.append((py + a[1] * k + b[1] * k, w, dd, px, py, n, day))
    cells.sort()

    css = ("@keyframes beacon{0%{opacity:.9;transform:scale(.6)}100%{opacity:0;transform:scale(2.4)}}")
    busiest = max(recent, key=lambda t: t[1]) if recent else ("-", 0)
    beacon = None
    out = []
    for _, w, dd, px, py, n, day in cells:
        A = (a[0] * k, a[1] * k)
        B = (b[0] * k, b[1] * k)
        p0 = (px, py)
        p1 = (px + A[0], py + A[1])
        p2 = (px + A[0] + B[0], py + A[1] + B[1])
        p3 = (px + B[0], py + B[1])
        lvl = 0 if n == 0 else 1 + sum(1 for c in cuts if n > c)
        cls = ev(2 + w // 3)
        if lvl == 0:
            pts = " ".join("%.1f,%.1f" % p for p in (p0, p1, p2, p3))
            out.append(f'<polygon class="{cls}" points="{pts}" fill="#ffffff" fill-opacity="0.06"/>')
            continue
        h = 5 + 92 * math.sqrt(n / peak)
        col = ramp[lvl]
        up = lambda p: (p[0], p[1] - h)
        top = " ".join("%.1f,%.1f" % p for p in (up(p0), up(p1), up(p2), up(p3)))
        fa = " ".join("%.1f,%.1f" % p for p in (p3, p2, up(p2), up(p3)))
        fb = " ".join("%.1f,%.1f" % p for p in (p1, p2, up(p2), up(p1)))
        out.append(f'<g class="{cls}"><polygon points="{fa}" fill="{_shade(col, 0.55)}"/>'
                   f'<polygon points="{fb}" fill="{_shade(col, 0.38)}"/>'
                   f'<polygon points="{top}" fill="{col}" fill-opacity="0.95"/></g>')
        if day == busiest[0]:
            tc = ((p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2 - h)
            beacon = tc
    body.append(f'<g stroke="{BG0}" stroke-width="0.4" stroke-opacity="0.5">' + "".join(out) + "</g>")
    if beacon:
        bx, by = beacon
        body.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="6" fill="none" stroke="{MINT}" stroke-width="1.6" '
                    f'style="animation:beacon 2s ease-out infinite;transform-origin:{bx:.1f}px {by:.1f}px"/>')
        body.append(f'<path d="M{bx:.1f} {by - 6:.1f}V{by - 34:.1f}" stroke="{MINT}" stroke-width="1" opacity="0.7"/>')
        lab, lw = sticker(bx - 60, by - 62, "PEAK %d" % busiest[1], MINT, VIOLET, fs=9.6, h=22, off=3)
        body.append(lab)

    # right column: numbers from the same calendar
    # the weekday that carries the most work - new information, rather than
    # repeating the streak numbers shown elsewhere
    import datetime as _dt
    wd = [0] * 7
    for day, n in recent:
        wd[_dt.date.fromisoformat(day).weekday()] += n
    busy_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][wd.index(max(wd))] if any(wd) else "-"
    year = sum(n for _, n in recent)
    activedays = sum(1 for _, n in recent if n)
    rows = [("pulse", fmt(year), "CONTRIBUTIONS · 52 WEEKS", CREAM),
            ("clock", "%d%%" % round(100.0 * activedays / max(1, len(recent))), "DAYS WITH A COMMIT", ROSE),
            ("flame", fmt(d.get("current")), "CURRENT STREAK", MINT),
            ("pulse", busy_day, "BUSIEST WEEKDAY", VIOLET)]
    rx = 900
    for i, (ic, val, lab, col) in enumerate(rows):
        y = 112 + i * 92
        body.append(f'<g class="{ev(3 + i)}">')
        body.append(card(s, rx, y, W - PAD - rx, 78, r=16, tint=col, tint_op=0.15, sheen=True, sheen_delay=i))
        body.append(icon(ic, rx + 18, y + 16, 18, col, 1.7, 0.9))
        body.append(f'<text class="sans" x="{rx + 18}" y="{y + 63}" font-size="26" font-weight="800" '
                    f'fill="{INK}">{val}</text>')
        body.append(f'<text class="mono" x="{W - PAD - 16}" y="{y + 29}" text-anchor="end" font-size="8.6" '
                    f'letter-spacing="1.4" fill="{col}" font-weight="600">{lab}</text>')
        body.append("</g>")

    # legend
    lx, ly = PAD + 4, H - 34
    body.append(f'<text class="mono" x="{lx}" y="{ly + 9}" font-size="9" fill="{DIM}">QUIET</text>')
    for j, c in enumerate(ramp[1:]):
        body.append(brut(lx + 44 + j * 20, ly, 12, 12, c, INKK, r=2, off=2, bw=1.2))
    body.append(f'<text class="mono" x="{lx + 130}" y="{ly + 9}" font-size="9" fill="{DIM}">BUSY &#183; '
                f'ONE TOWER PER DAY, ONE STREET PER WEEK &#183; REBUILT DAILY</text>')

    blobs = [(300, 300, 260, VIOLET, 0.22, "drift"), (700, 220, 240, ROSE, 0.16, "drift2"),
             (1040, 260, 220, MINT, 0.16, "drift3")]
    return page(s, W, H, css, "\n  ".join(body), blobs)


# ================================================================ project vault
def _project_card(s, i, pr, x, y, w, h, stars, big):
    col = RARITY[pr["rarity"]]
    o = [f'<g class="{ev(1 + i)}">',
         card(s, x, y, w, h, r=20, tint=col, tint_op=0.18, sheen=True, sheen_delay=i * 0.9),
         f'<rect x="{x}" y="{y + 26}" width="3" height="{h - 52}" rx="1.5" fill="{col}" opacity="0.85" '
         f'filter="url(#glowS_{s})"/>']
    st, _ = sticker(x + 20, y + 18, pr["rarity"], col, INKK if col != VIOLET else CREAM,
                    fs=9, h=21, rot=-3, off=3)
    o.append(st)
    n = stars.get(pr["repo"] or "", 0)
    if n:
        o.append(f'<g>{icon("star", x + w - 66, y + 20, 15, CREAM, 1.8)}'
                 f'<text class="mono" x="{x + w - 22}" y="{y + 33}" text-anchor="end" font-size="12" '
                 f'font-weight="700" fill="{CREAM}">{n}</text></g>')
    isz = 34 if big else 28
    o.append(icon(pr["icon"], x + 22, y + 56, isz, col, 1.6, 0.95,
                  extra=f' style="animation:breathe 4s ease-in-out {i * 0.6}s infinite"'))
    tx = x + 22 + isz + 14
    o.append(f'<text class="sans" x="{tx}" y="{y + (80 if big else 74)}" font-size="{23 if big else 18}" '
             f'font-weight="800" fill="{INK}" letter-spacing="-0.4">{esc(pr["title"])}</text>')
    o.append(f'<text class="mono" x="{tx}" y="{y + (98 if big else 90)}" font-size="{10.2 if big else 8.2}" '
             f'letter-spacing="1.2" fill="{col}" fill-opacity="0.92">{esc(pr["sub"].upper())}</text>')
    lines = pr["body"] if big else pr.get("short", pr["body"])
    for li, line in enumerate(lines):
        o.append(f'<text x="{x + 24}" y="{y + (134 if big else 122) + li * (20 if big else 17.5)}" '
                 f'font-size="{12.6 if big else 11}" fill="{DIM}">{esc(line)}</text>')
    tech = pr["tech"] if big else pr["tech"][:3]
    row, _ = chip_row(s, x + 24, y + h - 44, tech, cols=[col], gap=6, fs=10 if big else 9.4, h=21)
    o.append(row)
    if pr.get("live"):
        # big cards have room beside the chips; small ones carry it in the
        # top corner, under the star count
        ly = y + h - 29 if big else y + (54 if n else 34)
        o.append(f'<text class="mono" x="{x + w - 22}" y="{ly}" text-anchor="end" font-size="9.6" '
                 f'fill="{MINT}" fill-opacity="0.9">&#9679; LIVE &#8599;</text>')
    o.append("</g>")
    return "\n  ".join(o)


SHORT = {
    "Hirehearsal": ["Ora, a voice-first AI interviewer,", "runs tech, project and HR rounds",
                    "and scores every answer honestly."],
    "BookMyCampus": ["Rooms, labs and kit with approvals,", "QR check-in and no-show release,",
                     "plus a make-up class finder."],
    "TimedInk": ["Sends land on time through restarts,", "a wiped Redis and rate limits.",
                 "73 hermetic tests prove it."],
    "PII-Redaction-Tool": ["Hybrid regex + NER engine swaps", "10 PII types for realistic fakes",
                           "in .docx, tables kept intact."],
}

SHORT_SUB = {
    "BookMyCampus": "Campus booking platform",
    "TimedInk": "Fault-tolerant scheduler",
    "PII-Redaction-Tool": "Document privacy engine",
}


def build_vault(d):
    s = "p"
    H = 800
    stars = {r["name"]: r["stars"] for r in d.get("top_repos", [])}
    body = [section_header(s, PAD, 62, "PROJECT VAULT", "Featured engineering systems", ROSE)]
    big = [(PAD, 112, 541, 252), (PAD + 541 + 26, 112, 541, 252)]
    tw = (W - 2 * PAD - 3 * 20) / 4.0
    small = [(PAD + j * (tw + 20), 388, tw, 232) for j in range(4)]
    for i, pr in enumerate(P.PROJECTS):
        pr = dict(pr, short=SHORT.get(pr["repo"], pr["body"]))
        if i >= 2:
            pr["sub"] = SHORT_SUB.get(pr["repo"], pr["sub"])
        x, y, w, h = (big + small)[i]
        body.append(_project_card(s, i, pr, x, y, w, h, stars, i < 2))

    # side quests: compact brutalist-tagged glass strip
    sy = 646
    body.append(f'<g class="ev8">{card(s, PAD, sy, W - 2 * PAD, 112, r=18, tint=VIOLET, tint_op=0.1)}')
    st, stw = sticker(PAD + 22, sy + 18, "SIDE QUESTS", VIOLET, CREAM, fs=10, h=24, off=3)
    body.append(st)
    body.append(f'<text class="mono" x="{PAD + 22 + stw + 16}" y="{sy + 35}" font-size="10" fill="{DIM}">'
                f'more chapters of the same story</text>')
    cols = [CREAM, ROSE, MINT, VIOLET]
    gw4 = (W - 2 * PAD - 44 - 3 * 10) / 4.0
    for j, (t, one, repo) in enumerate(P.SIDE_QUESTS):
        col = cols[j % 4]
        cx, cy = PAD + 22 + (j % 4) * (gw4 + 10), sy + 52 + (j // 4) * 30
        wdt = gw4
        body.append(f'<rect x="{cx}" y="{cy}" width="{wdt}" height="23" rx="11.5" fill="{col}" fill-opacity="0.07" '
                    f'stroke="{col}" stroke-opacity="0.35"/>'
                    f'<text x="{cx + 12}" y="{cy + 15.5}" font-size="9.8"><tspan fill="{col}" font-weight="700">'
                    f'{esc(t)}</tspan><tspan fill="{DIM}">  {esc(one)}</tspan></text>')
        cx += wdt + 10
    body.append("</g>")
    blobs = [(220, 220, 260, CREAM, 0.2, "drift"), (860, 200, 250, VIOLET, 0.22, "drift2"),
             (300, 520, 240, MINT, 0.16, "drift3"), (960, 560, 240, ROSE, 0.2, "drift")]
    return page(s, W, H, "", "\n  ".join(body), blobs)
