"""
Chapter title cards.

Each card is a scene, not a caption: a bold gradient numeral, the chapter's
narrative title with a narrator line that types itself out, a six-step
progress rail - and on the right, an illustration drawn from real data that
is unique to that chapter:

  01 Origin      isometric towers, one per year, rising with contributions
  02 Arsenal     a radar chart of skill proficiency with a sweeping scanner
  03 Builds      a star map of the projects, sized by GitHub stars
  04 Battle log  a glowing area chart of the last twelve months
  05 Trophies    an isometric podium with medals
  06 Quest       a mission dial for the current main quest

Motion is transform / opacity / dash-offset only (see design.page()).
"""
import collections
import math
import random

import profile as P
from design import (BG0, INK, DIM, FAINT, CREAM, ROSE, MINT, VIOLET, PURPLE,
                    esc, card, page, uid, ev, sticker)

W = 1200
PAD = 46
H = 244


def fmt(n):
    return "-" if n is None else format(int(n), ",")


def _shade(hexcol, k):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(c * k) for c in (r, g, b))


def _prism(cx, base, hgt, a, b, col):
    """An isometric block standing on (cx, base): top, left and right faces."""
    t = base - hgt
    top = f"{cx},{t - b} {cx + a},{t} {cx},{t + b} {cx - a},{t}"
    left = f"{cx - a},{t} {cx},{t + b} {cx},{base + b} {cx - a},{base}"
    right = f"{cx},{t + b} {cx + a},{t} {cx + a},{base} {cx},{base + b}"
    return (f'<polygon points="{left}" fill="{_shade(col, 0.55)}"/>'
            f'<polygon points="{right}" fill="{_shade(col, 0.38)}"/>'
            f'<polygon points="{top}" fill="{col}"/>')


# ================================================================ illustrations
def ill_years(x, y, w, h, col, d):
    tot = collections.Counter()
    for day, n in d.get("calendar") or []:
        tot[day[:4]] += n
    years = sorted(tot)[-4:]
    peak = max([tot[k] for k in years] or [1]) or 1
    ramp = [PURPLE, ROSE, CREAM, MINT]
    base = y + h - 30
    colw = w / max(1, len(years))
    out = [f'<path d="M{x + 6} {base + 12}H{x + w - 6}" stroke="#ffffff" stroke-opacity="0.08"/>']
    for k, yr in enumerate(years):
        cx = x + colw * (k + 0.5)
        hg = 6 + (h - 78) * (tot[yr] / peak)
        c = ramp[k % 4]
        out.append(f'<g class="{ev(3 + k * 2)}">{_prism(round(cx), round(base), round(hg), 24, 11, c)}'
                   f'<text class="mono" x="{cx:.0f}" y="{base - hg - 20:.0f}" text-anchor="middle" font-size="10" '
                   f'font-weight="700" fill="{INK}">{fmt(tot[yr])}</text>'
                   f'<text class="mono" x="{cx:.0f}" y="{base + 30:.0f}" text-anchor="middle" font-size="9.4" '
                   f'letter-spacing="1.4" fill="{DIM}">{yr}</text></g>')
    # the climb, as a dashed arrow over the towers
    out.append(f'<path d="M{x + colw * 0.5:.0f} {y + 26}C{x + w * 0.45:.0f} {y + 20} {x + w * 0.6:.0f} {y + 10} '
               f'{x + colw * (len(years) - 0.5) - 6:.0f} {y + 4}" fill="none" stroke="{col}" stroke-opacity="0.5" '
               f'stroke-width="1.2" stroke-dasharray="3 5" class="flow"/>')
    return "".join(out), ""


def ill_radar(x, y, w, h, col, d):
    cx, cy = x + w / 2, y + h / 2 + 2
    R = min(w, h) / 2 - 28
    items = P.PROFICIENCY[:4]
    short = ["Java / DSA", "Full stack", "Cloud", "AI / DL"]
    ang = [-90, 0, 90, 180]
    pt = lambda a, r: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    out = []
    for f in (0.34, 0.67, 1.0):
        ring = " ".join("%.1f,%.1f" % pt(a, R * f) for a in ang)
        out.append(f'<polygon points="{ring}" fill="none" stroke="#ffffff" stroke-opacity="{0.06 + f * 0.05:.2f}"/>')
    for a in ang:
        ex, ey = pt(a, R)
        out.append(f'<path d="M{cx:.1f} {cy:.1f}L{ex:.1f} {ey:.1f}" stroke="#ffffff" stroke-opacity="0.08"/>')
    # scanner sweep
    sid = uid("sw")
    out.append(f'<linearGradient id="{sid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
               f'<stop offset="1" stop-color="{col}" stop-opacity="0.35"/></linearGradient>'
               f'<g style="animation:spin 6s linear infinite;transform-origin:{cx:.1f}px {cy:.1f}px">'
               f'<path d="M{cx:.1f} {cy:.1f}L{cx + R:.1f} {cy:.1f}A{R:.1f} {R:.1f} 0 0 0 {pt(-28, R)[0]:.1f} {pt(-28, R)[1]:.1f}Z" '
               f'fill="url(#{sid})"/></g>')
    poly = " ".join("%.1f,%.1f" % pt(a, R * it[1] / 100.0) for a, it in zip(ang, items))
    out.append(f'<polygon class="trace" points="{poly}" fill="{col}" fill-opacity="0.16" stroke="{col}" '
               f'stroke-width="1.8" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0"/>')
    for k, (a, it) in enumerate(zip(ang, items)):
        px, py = pt(a, R * it[1] / 100.0)
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.4" fill="{it[2]}" class="tw" '
                   f'style="animation-delay:{-k * 0.6:.1f}s"/>')
        lx, ly = pt(a, R + 16)
        anchor = {-90: "middle", 0: "start", 90: "middle", 180: "end"}[a]
        dy = {-90: -2, 0: 4, 90: 12, 180: 4}[a]
        out.append(f'<text class="mono" x="{lx:.1f}" y="{ly + dy:.1f}" text-anchor="{anchor}" font-size="9.4" '
                   f'fill="{DIM}">{esc(short[k])} <tspan fill="{it[2]}" font-weight="700">{it[1]}</tspan></text>')
    return "".join(out), ""


def ill_stars(x, y, w, h, col, d):
    stars = {r["name"]: r["stars"] for r in d.get("top_repos", [])}
    pos = [(0.12, 0.52), (0.33, 0.2), (0.5, 0.6), (0.69, 0.22), (0.9, 0.5), (0.7, 0.86)]
    nodes = []
    for (fx, fy), pr in zip(pos, P.PROJECTS):
        n = stars.get(pr["repo"] or "", 0)
        nodes.append((x + fx * w, y + 10 + fy * (h - 34), 3 + 2.1 * math.sqrt(n), pr["title"], n))
    rnd = random.Random(11)
    out = []
    for _ in range(34):
        out.append(f'<circle cx="{x + rnd.uniform(0, w):.0f}" cy="{y + rnd.uniform(0, h - 10):.0f}" '
                   f'r="{rnd.uniform(0.5, 1.2):.1f}" fill="#ffffff" opacity="{rnd.uniform(0.15, 0.45):.2f}"/>')
    links = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (0, 2)]
    for a, b in links:
        (ax, ay, *_), (bx, by, *_) = nodes[a], nodes[b]
        out.append(f'<path d="M{ax:.0f} {ay:.0f}L{bx:.0f} {by:.0f}" stroke="{col}" stroke-opacity="0.35" '
                   f'stroke-width="1" stroke-dasharray="2 4" class="flow"/>')
    for k, (nx, ny, r, name, n) in enumerate(nodes):
        c = [CREAM, VIOLET, ROSE, ROSE, MINT, MINT][k]
        if n >= 5:
            out.append(f'<circle cx="{nx:.0f}" cy="{ny:.0f}" r="{r + 4:.1f}" fill="none" stroke="{c}" '
                       f'stroke-opacity="0.6" class="halo" style="transform-origin:{nx:.0f}px {ny:.0f}px"/>')
        out.append(f'<circle cx="{nx:.0f}" cy="{ny:.0f}" r="{r:.1f}" fill="{c}" class="tw" '
                   f'style="animation-delay:{-k * 0.7:.1f}s"/>')
        lab = name + ("  %d★" % n if n else "")
        out.append(f'<text class="mono" x="{nx:.0f}" y="{ny + r + 15:.0f}" text-anchor="middle" font-size="8.6" '
                   f'fill="{INK if n >= 5 else DIM}">{esc(lab)}</text>')
    return "".join(out), ""


def ill_spark(x, y, w, h, col, d):
    tot = collections.Counter()
    for day, n in d.get("calendar") or []:
        tot[day[:7]] += n
    months = sorted(tot)[-12:]
    vals = [tot[m] for m in months]
    peak = max(vals or [1]) or 1
    top, bot = y + 22, y + h - 30
    xs = [x + 8 + i * (w - 16) / max(1, len(vals) - 1) for i in range(len(vals))]
    ys = [bot - (bot - top) * v / peak for v in vals]
    gid = uid("ag")
    line = "M" + " L".join("%.1f %.1f" % p for p in zip(xs, ys))
    area = line + " L%.1f %.1f L%.1f %.1f Z" % (xs[-1], bot, xs[0], bot)
    out = [f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0.4"/>'
           f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>']
    for g in range(3):
        gy = top + g * (bot - top) / 2
        out.append(f'<path d="M{x} {gy:.0f}H{x + w}" stroke="#ffffff" stroke-opacity="0.06"/>')
    out.append(f'<path d="{area}" fill="url(#{gid})"/>')
    out.append(f'<path class="trace" d="{line}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" '
               f'pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0"/>')
    names = "JFMAMJJASOND"
    for i, (px, py, m) in enumerate(zip(xs, ys, months)):
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{BG0}" stroke="{col}" stroke-width="1.4"/>')
        out.append(f'<text class="mono" x="{px:.1f}" y="{bot + 20:.0f}" text-anchor="middle" font-size="8.6" '
                   f'fill="{FAINT}">{names[int(m[5:]) - 1]}</text>')
    lx, ly = xs[-1], ys[-1]
    out.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4" fill="{col}"/>'
               f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4" fill="none" stroke="{col}" class="ping" '
               f'style="transform-origin:{lx:.1f}px {ly:.1f}px"/>')
    pk = vals.index(peak)
    out.append(f'<text class="mono" x="{x + w}" y="{y + 8}" text-anchor="end" font-size="9" fill="{DIM}">'
               f'12 MONTHS &#183; PEAK <tspan fill="{col}" font-weight="700">{peak}</tspan> IN '
               f'{["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"][int(months[pk][5:]) - 1]}</text>')
    return "".join(out), ""


def ill_podium(x, y, w, h, col, d):
    T = P.TROPHIES
    spots = [  # (slot x fraction, block height, rank, trophy, medal colour)
        (0.2, 52, 2, T[1], "#cbd5e1"),
        (0.5, 76, 1, T[0], CREAM),
        (0.8, 36, 3, T[3], "#f0b38a"),
    ]
    base = y + h - 16
    out = []
    for k, (fx, bh, rank, tr, mc) in enumerate(spots):
        cx = round(x + fx * w)
        out.append(f'<g class="{ev(3 + k * 2)}">{_prism(cx, base, bh, 44, 17, _shade(mc, 0.85))}'
                   f'<text class="sans" x="{cx - 20}" y="{base - bh / 2 + 16:.0f}" text-anchor="middle" font-size="20" '
                   f'font-weight="800" fill="#0d1117" fill-opacity="0.75">{rank}</text></g>')
        # stacked above the block: value, label, then the medal on its ribbon
        my = base - bh - 17 - 18
        out.append(f'<g class="bob" style="animation-delay:{-k * 0.5:.1f}s">'
                   f'<path d="M{cx - 7} {my - 14}L{cx} {my - 3}L{cx + 7} {my - 14}" fill="none" stroke="{mc}" stroke-width="2.4" stroke-opacity="0.6"/>'
                   f'<circle cx="{cx}" cy="{my}" r="11" fill="{mc}"/>'
                   f'<circle cx="{cx}" cy="{my}" r="6.5" fill="none" stroke="#0d1117" stroke-opacity="0.35" stroke-width="1.4"/>'
                   f'</g>')
        out.append(f'<text class="sans" x="{cx}" y="{my - 41:.0f}" text-anchor="middle" font-size="14" font-weight="800" '
                   f'fill="{INK}">{esc(tr[3])}</text>'
                   f'<text class="mono" x="{cx}" y="{my - 21:.0f}" text-anchor="middle" font-size="8" letter-spacing="1.2" '
                   f'fill="{DIM}">{esc(tr[4])}</text>')
    return "".join(out), ""


def ill_dial(x, y, w, h, col, d):
    quest = P.BOSS["quest"]
    pct = next((q[2] for q in P.QUESTS if q[0] == quest), 0)
    cx, cy, r = x + 78, y + h / 2 + 4, 62
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ffffff" stroke-opacity="0.07" stroke-width="10"/>']
    for k in range(10):
        a = math.radians(-90 + k * 36)
        done = k < max(1, round(pct / 10))
        x1, y1 = cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a)
        x2, y2 = cx + (r + 16) * math.cos(a), cy + (r + 16) * math.sin(a)
        out.append(f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{col if done else "#ffffff"}" '
                   f'stroke-opacity="{1 if done else 0.2}" stroke-width="2" stroke-linecap="round"/>')
    out.append(f'<circle class="trace" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="10" '
               f'stroke-linecap="round" pathLength="100" stroke-dasharray="{pct} {100 - pct}" stroke-dashoffset="0" '
               f'transform="rotate(-90 {cx} {cy})"/>')
    out.append(f'<g style="animation:spin 9s linear infinite;transform-origin:{cx}px {cy}px">'
               f'<circle cx="{cx}" cy="{cy - r - 26}" r="3.2" fill="{MINT}"/></g>')
    out.append(f'<text class="sans" x="{cx}" y="{cy + 8}" text-anchor="middle" font-size="28" font-weight="800" '
               f'fill="{INK}">{pct}%</text>'
               f'<text class="mono" x="{cx}" y="{cy + 26}" text-anchor="middle" font-size="8.4" letter-spacing="1.6" '
               f'fill="{col}">{esc(quest.upper())}</text>')
    tx = x + 176
    rows = [("NOW", next((m[1] for m in P.BOSS["moves"] if m[2] == "now"), "-"), col),
            ("NEXT", next((m[1] for m in P.BOSS["moves"] if m[2] == "next"), "-"), DIM),
            ("BOSS", P.BOSS["name"].title(), ROSE),
            ("YOU", "vote below", MINT)]
    for k, (lab, val, c) in enumerate(rows):
        yy = y + 40 + k * 32
        out.append(f'<g class="{ev(4 + k)}"><text class="mono" x="{tx}" y="{yy}" font-size="8.4" letter-spacing="1.8" '
                   f'fill="{c}">{lab}</text><text x="{tx}" y="{yy + 15}" font-size="12" font-weight="600" '
                   f'fill="{INK}">{esc(val)}</text></g>')
    return "".join(out), ""


ILLUSTRATIONS = [ill_years, ill_radar, ill_stars, ill_spark, ill_podium, ill_dial]


# ================================================================ the card
def build_chapter(i, d):
    num, kicker, title, line, col = P.CHAPTERS[i]
    s = "c%d" % (i + 1)
    n = len(P.CHAPTERS)
    fs = 13.5
    tw = len(line) * fs * 0.6
    T = 11.0
    css = ("@keyframes stamp{0%%{transform:translateY(12px);opacity:.5}100%%{transform:none;opacity:1}}"
           ".stamp{animation:stamp 1.2s cubic-bezier(.22,1,.36,1)}"
           "@keyframes trace{0%%,8%%{stroke-dashoffset:1}60%%,100%%{stroke-dashoffset:0}}"
           ".trace{animation:trace 2.8s cubic-bezier(.45,.05,.35,1)}"
           "@keyframes say{0%%{width:0}32%%,100%%{width:%.1fpx}}.say{animation:say %.1fs steps(%d,end) infinite}"
           "@keyframes caret{0%%,49%%{opacity:1}50%%,100%%{opacity:0}}.caret{animation:caret 1s steps(1) infinite}"
           "@keyframes tw{0%%,100%%{opacity:1}50%%{opacity:.45}}.tw{animation:tw 2.6s ease-in-out infinite}"
           "@keyframes halo{0%%{transform:scale(.8);opacity:.9}100%%{transform:scale(1.9);opacity:0}}"
           ".halo{animation:halo 2.4s ease-out infinite}"
           "@keyframes ping{0%%{transform:scale(1);opacity:.9}100%%{transform:scale(3);opacity:0}}"
           ".ping{animation:ping 1.8s ease-out infinite}"
           "@keyframes bob{0%%,100%%{transform:translateY(0)}50%%{transform:translateY(-4px)}}"
           ".bob{animation:bob 2.8s ease-in-out infinite}"
           "@keyframes flowd{from{stroke-dashoffset:24}to{stroke-dashoffset:0}}"
           ".flow{animation:flowd 1.6s linear infinite}"
           "@keyframes seg{0%%,100%%{opacity:1}50%%{opacity:.55}}"
           % (tw + 4, T, len(line)))

    body = []
    body.append(card(s, 24, 14, W - 48, H - 28, r=24, tint=col, tint_op=0.12))
    # HUD corner brackets
    L = 16
    for (bx, by, dx, dy) in [(38, 28, 1, 1), (W - 38, 28, -1, 1), (38, H - 28, 1, -1), (W - 38, H - 28, -1, -1)]:
        body.append(f'<path d="M{bx} {by + dy * L}V{by}H{bx + dx * L}" fill="none" stroke="{col}" '
                    f'stroke-opacity="0.7" stroke-width="1.4" stroke-linecap="round"/>')

    # numeral: big, solid, gradient - legible at any size
    gid = "ng_" + s
    body.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{col}"/></linearGradient>')
    nx = 70
    body.append(f'<g class="stamp">'
                f'<text class="mono" x="{nx + 2}" y="70" font-size="10" font-weight="600" letter-spacing="3.4" '
                f'fill="{col}">CHAPTER</text>'
                f'<text class="sans" x="{nx - 4}" y="160" font-size="96" font-weight="800" letter-spacing="-5" '
                f'fill="url(#{gid})">{i + 1:02d}</text>'
                f'<rect x="{nx}" y="180" width="44" height="2" rx="1" fill="{col}"/></g>')

    # text column
    tx = 230
    st, _ = sticker(tx, 46, kicker, col, fs=9.6, h=24)
    body.append(f'<g class="ev1">{st}</g>')
    body.append(f'<text class="sans ev2" x="{tx}" y="118" font-size="32" font-weight="800" fill="{INK}" '
                f'letter-spacing="-0.6">{esc(title)}</text>')
    cid = uid("say")
    body.append(f'<clipPath id="{cid}"><rect class="say" x="{tx - 2}" y="132" width="{tw + 4:.1f}" height="24"/></clipPath>'
                f'<text class="mono" x="{tx}" y="150" font-size="{fs}" fill="{DIM}" textLength="{tw:.1f}" '
                f'lengthAdjust="spacingAndGlyphs" clip-path="url(#{cid})">{esc(line)}</text>')
    # progress rail
    segw, gap = 46, 6
    for k in range(n):
        fill, op = (col, 1) if k == i else ((col, 0.4) if k < i else ("#ffffff", 0.1))
        anim = ' style="animation:seg 1.6s ease-in-out infinite"' if k == i else ""
        body.append(f'<rect x="{tx + k * (segw + gap)}" y="184" width="{segw}" height="4" rx="2" fill="{fill}" '
                    f'fill-opacity="{op}"{anim}/>')
    body.append(f'<text class="mono ev3" x="{tx + n * (segw + gap) + 8}" y="190" font-size="9" letter-spacing="1.8" '
                f'fill="{FAINT}">{i + 1:02d} / {n:02d} &#183; {"LOADING NEXT" if i < n - 1 else "FINAL CHAPTER"}</text>')

    # illustration
    dx = 806
    body.append(f'<rect x="{dx - 20}" y="44" width="1" height="{H - 88}" fill="#ffffff" opacity="0.08"/>')
    ix, iy, iw, ih = dx, 36, W - 58 - dx, H - 72
    svg, extra = ILLUSTRATIONS[i](ix, iy, iw, ih, col, d)
    body.append(f'<g class="ev2">{svg}</g>')
    return page(s, W, H, css + extra, "\n  ".join(body), None, grid=False)
