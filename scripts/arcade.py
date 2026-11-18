"""
The arcade cabinet: three panels that make the profile feel alive.

  companion.svg  BYTE, a pixel robot whose mood follows the real commit streak
  ticker.svg     $ANKIT - weekly contributions drawn as trading candles
  votes.svg      Game Mode - visitors vote for the next quest via issues

companion and ticker are 600 wide so the README can set them side by side
as a bento row; votes is full width.
"""
import json
import os

import profile as P
from design import (BG0, BG2, INK, DIM, FAINT, CREAM, ROSE, MINT, VIOLET, PURPLE, INKK, uid,
                    esc, card, page, section_header, ev, brut, sticker)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HW = 600  # half-width canvas
PAD = 46


def fmt(n):
    return "-" if n is None else format(int(n), ",")


# ================================================================ companion
# 16 x 15 sprite. K ink outline, B body, S screen, A antenna light, L legs.
# Eyes and mouth are drawn separately so each mood can swap them.
SPRITE = [
    ".......AA.......",
    ".......KK.......",
    "....KKKKKKKK....",
    "...KBBBBBBBBK...",
    "..KBSSSSSSSSBK..",
    "..KBSSSSSSSSBK..",
    "KKKBSSSSSSSSBKKK",
    "KBKBSSSSSSSSBKBK",
    "KKKBSSSSSSSSBKKK",
    "..KBSSSSSSSSBK..",
    "...KBBBBBBBBK...",
    "....KKKKKKKK....",
    "...KBBKBBKBBK...",
    "..KBBBBBBBBBBK..",
    "...KLK....KLK...",
]

# eye / mouth pixels per mood, in sprite cells (col, row)
FACES = {
    "hyped": dict(eyes=[(5, 5), (6, 4), (7, 5), (9, 5), (10, 4), (11, 5)],
                  mouth=[(6, 8), (7, 9), (8, 9), (9, 8)]),
    "on": dict(eyes=[(6, 5), (6, 6), (10, 5), (10, 6)],
               mouth=[(7, 8), (8, 8), (9, 8)]),
    "asleep": dict(eyes=[(5, 6), (6, 6), (7, 6), (9, 6), (10, 6), (11, 6)],
                   mouth=[(8, 8)]),
}


def _mood(d):
    cur = int(d.get("current") or 0)
    if cur >= 3:
        return "hyped", "%d-day streak. We are unstoppable!" % cur, MINT
    if cur >= 1:
        return "on", "Day %d of a fresh streak. Keep pushing!" % cur, CREAM
    return "asleep", "No commits today... wake me with a push.", ROSE


def build_companion(d):
    s = "m"
    H = 400
    mood, line, col = _mood(d)
    px = 11  # one sprite cell
    sx, sy = 46, 118
    css = """
    @keyframes hop{0%,100%{transform:translateY(0)}40%{transform:translateY(-16px)}55%{transform:translateY(-16px)}}
    @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
    @keyframes shad{0%,100%{transform:scaleX(1);opacity:.5}50%{transform:scaleX(.78);opacity:.28}}
    @keyframes ant{0%,100%{opacity:1}50%{opacity:.25}}
    @keyframes zz{0%{transform:translate(0,0);opacity:0}20%{opacity:.9}100%{transform:translate(26px,-46px);opacity:0}}
    @keyframes spk{0%,100%{transform:scale(.4);opacity:0}50%{transform:scale(1);opacity:1}}
    @keyframes blinkE{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}
    """
    move = {"hyped": "hop 1.1s cubic-bezier(.3,0,.3,1) infinite",
            "on": "bob 2.4s ease-in-out infinite",
            "asleep": "bob 4.8s ease-in-out infinite"}[mood]

    fill = {"K": "#4b3bb8", "B": MINT, "S": "#0a0e14", "A": ROSE, "L": PURPLE}
    cells = []
    for r, row in enumerate(SPRITE):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            extra = ' style="animation:ant 1.2s steps(1) infinite"' if ch == "A" else ""
            cells.append(f'<rect x="{sx + c * px}" y="{sy + r * px}" width="{px}" height="{px}" '
                         f'fill="{fill[ch]}"{extra}/>')
    # body shading: a lighter top-left edge reads as a lit pixel sprite
    cells.append(f'<rect x="{sx + 4 * px}" y="{sy + 3 * px}" width="{8 * px}" height="{px * 0.4}" '
                 f'fill="#ffffff" opacity="0.35"/>')
    face = FACES[mood]
    fcol = {"hyped": MINT, "on": CREAM, "asleep": FAINT}[mood]
    ecx, ecy = sx + 8 * px, sy + 5.5 * px
    eyes = "".join(f'<rect x="{sx + c * px}" y="{sy + r * px}" width="{px}" height="{px}" fill="{fcol}"/>'
                   for c, r in face["eyes"])
    eye_anim = ' style="animation:blinkE 4s infinite;transform-origin:%spx %spx"' % (ecx, ecy) if mood == "on" else ""
    mouth = "".join(f'<rect x="{sx + c * px}" y="{sy + r * px}" width="{px}" height="{px}" fill="{ROSE}"/>'
                    for c, r in face["mouth"])

    gw = 16 * px
    body = [section_header(s, 34, 56, "COMPANION", "Meet BYTE", MINT)]
    body.append(f'<ellipse cx="{sx + gw / 2}" cy="{sy + 15 * px + 16}" rx="{gw * 0.42}" ry="8" fill="{PURPLE}" '
                f'style="animation:shad {"1.1s" if mood == "hyped" else "2.4s"} ease-in-out infinite;'
                f'transform-origin:{sx + gw / 2}px {sy + 15 * px + 16}px"/>')
    body.append(f'<g style="animation:{move}" filter="url(#dropS_{s})">{"".join(cells)}'
                f'<g{eye_anim}>{eyes}</g>{mouth}</g>')
    if mood == "asleep":
        for i in range(3):
            body.append(f'<text class="mono" x="{sx + gw - 4}" y="{sy + 20}" font-size="{14 + i * 4}" '
                        f'font-weight="800" fill="{CREAM}" opacity="0" '
                        f'style="animation:zz 3s ease-out {i}s infinite">z</text>')
    elif mood == "hyped":
        for i, (x, y) in enumerate([(sx - 16, sy + 20), (sx + gw + 8, sy + 46), (sx + 4, sy + 120)]):
            body.append(f'<path d="M{x} {y - 7}L{x + 2} {y - 2}L{x + 7} {y}L{x + 2} {y + 2}L{x} {y + 7}'
                        f'L{x - 2} {y + 2}L{x - 7} {y}L{x - 2} {y - 2}Z" fill="{CREAM}" '
                        f'style="animation:spk 1.6s ease-in-out {i * 0.5}s infinite;transform-origin:{x}px {y}px"/>')

    # speech bubble
    bx, by, bw, bh = 254, 96, 312, 92
    body.append(f'<g class="ev2">{card(s, bx, by, bw, bh, r=16, tint=col, tint_op=0.2)}'
                f'<path d="M{bx} {by + 40}L{bx - 16} {by + 52}L{bx} {by + 58}" fill="#ffffff" fill-opacity="0.07" '
                f'stroke="#ffffff" stroke-opacity="0.2"/>'
                f'<text class="mono" x="{bx + 18}" y="{by + 28}" font-size="9.6" letter-spacing="2" '
                f'fill="{col}" font-weight="700">BYTE SAYS</text>'
                f'<text x="{bx + 18}" y="{by + 56}" font-size="13.5" fill="{INK}" font-weight="600">'
                f'{esc(line)}</text>'
                f'<text class="mono" x="{bx + 18}" y="{by + 76}" font-size="9.4" fill="{DIM}">'
                f'mood: {mood.upper()} &#183; fed by my real commit streak</text></g>')

    cal = d.get("calendar") or []
    last = next((day for day, n in reversed(cal) if n), "-")
    rows = [("CURRENT STREAK", "%s d" % fmt(d.get("current")), MINT),
            ("BEST STREAK", "%s d" % fmt(d.get("longest")), CREAM),
            ("LAST COMMIT", last[5:] if last != "-" else "-", ROSE)]
    for i, (lab, val, c) in enumerate(rows):
        x = 254 + i * 108
        body.append(f'<g class="{ev(3 + i)}">{card(s, x, 210, 96, 74, r=14, tint=c, tint_op=0.16, shadow=False)}'
                    f'<text class="mono" x="{x + 12}" y="232" font-size="7.8" letter-spacing="1.2" '
                    f'fill="{c}" font-weight="700">{lab}</text>'
                    f'<text class="sans" x="{x + 12}" y="266" font-size="22" font-weight="800" '
                    f'fill="{INK}">{esc(val)}</text></g>')

    st, _ = sticker(34, H - 70, "BYTE · LVL %d COMPANION" % max(1, int(d.get("longest") or 0) // 10),
                    MINT, ROSE, fs=9.6, h=24, off=3)
    body.append(f'<g class="ev5">{st}</g>')
    body.append(f'<text class="mono" x="{HW - 34}" y="{H - 52}" text-anchor="end" font-size="9" '
                f'fill="{FAINT}">hyped &#8805; 3 days &#183; on it 1-2 &#183; asleep at 0</text>')
    blobs = [(150, 220, 200, MINT, 0.22, "drift"), (460, 160, 200, ROSE, 0.2, "drift2")]
    return page(s, HW, H, css, "\n  ".join(body), blobs)


# ================================================================ ticker
def build_ticker(d):
    s = "k"
    H = 400
    cal = d.get("calendar") or []
    weeks = 26
    days = cal[-weeks * 7:]
    wk = [days[i:i + 7] for i in range(0, len(days), 7)]
    candles = []
    for w in wk:
        ns = [n for _, n in w]
        candles.append((ns[0], max(ns), min(ns), ns[-1], sum(ns) / len(ns)))
    this7 = sum(n for _, n in cal[-7:])
    prev7 = sum(n for _, n in cal[-14:-7])
    chg = (100.0 * (this7 - prev7) / prev7) if prev7 else (100.0 if this7 else 0.0)
    up = this7 >= prev7
    tcol = MINT if up else ROSE

    css = """
    @keyframes tape{from{transform:translateX(0)}to{transform:translateX(-50%)}}
    @keyframes ma{0%,10%{stroke-dashoffset:.9}100%{stroke-dashoffset:0}}
    .ma{animation:ma 2.6s cubic-bezier(.45,.05,.35,1)}
    @keyframes live{0%,100%{opacity:1}50%{opacity:.2}}
    """
    body = [section_header(s, 34, 56, "MARKET", "$ANKIT · commits, as candles", CREAM)]
    body.append(f'<text class="sans ev1" x="34" y="132" font-size="34" font-weight="800" fill="{INK}" '
                f'letter-spacing="-1">{fmt(this7)}</text>')
    body.append(f'<text class="mono ev1" x="{34 + len(fmt(this7)) * 20 + 14}" y="130" font-size="13" '
                f'font-weight="700" fill="{tcol}">{"&#9650;" if up else "&#9660;"} {abs(chg):.0f}%</text>')
    body.append(f'<text class="mono ev1" x="34" y="150" font-size="9.4" letter-spacing="1.4" fill="{DIM}">'
                f'CONTRIBUTIONS THIS WEEK VS LAST</text>')
    body.append(f'<g class="ev1"><circle cx="{HW - 120}" cy="125" r="4" fill="{ROSE}" '
                f'style="animation:live 1.4s steps(1) infinite"/>'
                f'<text class="mono" x="{HW - 108}" y="129" font-size="10" letter-spacing="1.6" fill="{ROSE}" '
                f'font-weight="700">LIVE &#183; 26W</text></g>')

    x0, x1, y0, y1 = 40, HW - 40, 170, 316
    body.append(card(s, 24, 160, HW - 48, 168, r=14, tint=PURPLE, tint_op=0.14, shadow=False))
    for g in range(4):
        y = y0 + 8 + g * (y1 - y0 - 8) / 3
        body.append(f'<rect x="{x0}" y="{y:.0f}" width="{x1 - x0}" height="1" fill="#ffffff" opacity="0.06"/>')
    hi = max([c[1] for c in candles] or [1]) or 1
    sy = lambda v: y1 - 6 - (y1 - y0 - 18) * (v / hi)
    step = (x1 - x0) / max(1, len(candles))
    ma = []
    for i, (o, h, l, c, mean) in enumerate(candles):
        cx = x0 + step * (i + 0.5)
        colc = MINT if c >= o else ROSE
        top, bot = sy(max(o, c)), sy(min(o, c))
        if bot - top < 2:
            top, bot = top - 1, bot + 1
        body.append(f'<g class="{ev(2 + i // 2)}">'
                    f'<rect x="{cx - 0.7:.1f}" y="{sy(h):.1f}" width="1.4" height="{sy(l) - sy(h):.1f}" fill="{colc}"/>'
                    f'<rect x="{cx - step * 0.3:.1f}" y="{top:.1f}" width="{step * 0.6:.1f}" height="{bot - top:.1f}" '
                    f'rx="1.5" fill="{colc}" fill-opacity="{0.9 if c >= o else 0.25}" stroke="{colc}" stroke-width="1"/></g>')
        ma.append((cx, sy(mean)))
    if ma:
        pts = " ".join("%.1f,%.1f" % p for p in ma)
        body.append(f'<polyline class="ma" points="{pts}" fill="none" stroke="{CREAM}" stroke-width="1.8" '
                    f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0" '
                    f'filter="url(#glowS_{s})"/>')
    body.append(f'<text class="mono" x="{x1}" y="{y0 + 4}" text-anchor="end" font-size="8.6" fill="{FAINT}">'
                f'PEAK {hi}/DAY &#183; AMBER = WEEKLY AVERAGE</text>')

    # ticker tape: repos as symbols, scrolling forever
    syms = []
    for r in d.get("top_repos", [])[:6]:
        sym = "".join(ch for ch in r["name"].upper() if ch.isalnum())[:6]
        syms.append((sym, "%d&#9733;" % r["stars"]))
    syms += [("XP", fmt(d.get("total_contributions"))), ("PRS", fmt(d.get("prs"))),
             ("REPOS", fmt(d.get("repos")))]
    item = "".join(f'<tspan fill="{CREAM}" font-weight="700">${sym}</tspan><tspan fill="{MINT}"> {val}'
                   f'  &#9650;   </tspan>' for sym, val in syms)
    clip = "tp_" + s
    body.append(f'<clipPath id="{clip}"><rect x="0" y="{H - 52}" width="{HW}" height="34"/></clipPath>')
    body.append(brut(-10, H - 52, HW + 20, 32, INKK, ROSE, r=0, off=0, bw=0))
    body.append(f'<g clip-path="url(#{clip})"><g style="animation:tape 26s linear infinite">'
                f'<text class="mono" x="12" y="{H - 31}" font-size="11" letter-spacing="1">{item}{item}</text>'
                f'</g></g>')
    body.append(f'<rect x="0" y="{H - 53}" width="{HW}" height="1.4" fill="{ROSE}"/>'
                f'<rect x="0" y="{H - 21}" width="{HW}" height="1.4" fill="{ROSE}"/>')
    blobs = [(160, 250, 220, CREAM, 0.18, "drift"), (460, 200, 200, PURPLE, 0.3, "drift2")]
    return page(s, HW, H, css, "\n  ".join(body), blobs)


# ================================================================ game mode
def load_votes():
    p = os.path.join(ROOT, "data", "votes.json")
    v = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return {k: int((v.get(k) or {}).get("votes", 0)) for k, *_ in P.VOTE_OPTIONS}


def build_votes():
    s = "g"
    W = 1200
    H = 330
    votes = load_votes()
    total = sum(votes.values())
    lead = max(votes, key=votes.get) if total else None
    css = """
    @keyframes crown{0%,100%{transform:translateY(0) rotate(-8deg)}50%{transform:translateY(-4px) rotate(-4deg)}}
    @keyframes insert{0%,100%{opacity:1}50%{opacity:.25}}
    """
    body = [section_header(s, 46, 62, "GAME MODE", "You pick my next quest", VIOLET)]
    body.append(f'<text class="mono ev1" x="1154" y="58" text-anchor="end" font-size="10.6" letter-spacing="2.4" '
                f'fill="{CREAM}" font-weight="700" style="animation:insert 1.2s steps(1) infinite">'
                f'&#9679; INSERT COIN: VOTE BELOW</text>')
    body.append(f'<text class="mono ev1" x="1154" y="80" text-anchor="end" font-size="9.6" fill="{DIM}">'
                f'{total} vote{"s" if total != 1 else ""} cast &#183; counted by a GitHub Action</text>')
    cw, gap = 262, 20
    for i, (key, label, sub, col) in enumerate(P.VOTE_OPTIONS):
        x = 46 + i * (cw + gap)
        y = 116
        n = votes[key]
        pct = (100.0 * n / total) if total else 0
        shadow = {CREAM: ROSE, ROSE: PURPLE, MINT: ROSE, VIOLET: MINT}[col]
        body.append(f'<g class="{ev(2 + i)}">')
        body.append(brut(x, y, cw, 168, BG2, shadow, r=16, off=6, bw=2.6))
        body.append(f'<rect x="{x + 1.3}" y="{y + 1.3}" width="{cw - 2.6}" height="44" rx="14" fill="{col}"/>'
                    f'<rect x="{x + 1.3}" y="{y + 30}" width="{cw - 2.6}" height="16" fill="{col}"/>'
                    f'<rect x="{x}" y="{y + 45}" width="{cw}" height="2.6" fill="{INKK}"/>')
        body.append(f'<text class="mono" x="{x + 18}" y="{y + 29}" font-size="12" font-weight="800" '
                    f'letter-spacing="1.4" fill="{INKK}">PLAYER {i + 1} &#183; {key.upper()}</text>')
        body.append(f'<text class="sans" x="{x + 18}" y="{y + 78}" font-size="17" font-weight="800" '
                    f'fill="{INK}">{esc(label)}</text>')
        body.append(f'<text x="{x + 18}" y="{y + 98}" font-size="11.2" fill="{DIM}">{esc(sub)}</text>')
        body.append(f'<rect x="{x + 18}" y="{y + 118}" width="{cw - 36}" height="12" rx="3" fill="#ffffff" '
                    f'fill-opacity="0.07" stroke="{INKK}" stroke-width="1.4"/>')
        if n:
            body.append(f'<rect x="{x + 18}" y="{y + 118}" width="{max(8, (cw - 36) * pct / 100):.1f}" '
                        f'height="12" rx="3" fill="{col}" stroke="{INKK}" stroke-width="1.4"/>')
        body.append(f'<text class="mono" x="{x + 18}" y="{y + 151}" font-size="10.4" fill="{col}" '
                    f'font-weight="700">{n} VOTE{"S" if n != 1 else ""}</text>')
        body.append(f'<text class="mono" x="{x + cw - 18}" y="{y + 151}" text-anchor="end" font-size="10.4" '
                    f'fill="{DIM}">{pct:.0f}%</text>')
        if key == lead:
            cx = x + cw - 30
            body.append(f'<g style="animation:crown 2s ease-in-out infinite;transform-origin:{cx}px {y - 4}px">'
                        f'<path d="M{cx - 14} {y + 2}L{cx - 14} {y - 14}L{cx - 6} {y - 6}L{cx} {y - 18}'
                        f'L{cx + 6} {y - 6}L{cx + 14} {y - 14}L{cx + 14} {y + 2}Z" fill="{CREAM}" '
                        f'stroke="{INKK}" stroke-width="2"/></g>')
        body.append("</g>")
    body.append(f'<text class="mono" x="{W // 2}" y="{H - 14}" text-anchor="middle" font-size="9.4" '
                f'letter-spacing="1.4" fill="{FAINT}">CLICK A QUEST UNDER THIS PANEL &#8594; SUBMIT THE ISSUE &#8594; '
                f'A BOT COUNTS YOUR VOTE AND CLOSES IT &#183; ONE VOTE PER PLAYER PER QUEST</text>')
    blobs = [(250, 200, 240, VIOLET, 0.14, "drift"), (900, 200, 240, ROSE, 0.18, "drift2")]
    return page(s, W, H, css, "\n  ".join(body), blobs)


# ================================================================ marquee
def build_marquee(flip=False):
    """Two crossing neo-brutalist bands of kinetic type, scrolling in
    opposite directions - the tape that holds the story's scenes together.
    Each band is two copies of one pinned-width string, so the loop is
    seamless and costs a single transform per band."""
    s = "q2" if flip else "q1"
    W, H = 1200, 120
    words = P.MARQUEE[::-1] if flip else P.MARQUEE
    unit = "  \u2726  ".join(words) + "  \u2726  "
    fs = 20
    L = len(unit) * fs * 0.64
    css = ("@keyframes mqL{from{transform:translateX(0)}to{transform:translateX(-%.1fpx)}}"
           "@keyframes mqR{from{transform:translateX(-%.1fpx)}to{transform:translateX(0)}}" % (L, L))
    bands = [(-2.4, ROSE, CREAM, "mqL", 34), (1.8, MINT, ROSE, "mqR", 40)]
    if flip:
        bands = [(2.2, CREAM, MINT, "mqR", 36), (-1.6, VIOLET, ROSE, "mqL", 42)]
    body = []
    for k, (rot, fill, shade, anim, dur) in enumerate(bands[::-1]):
        y = 38 + k * 6
        txt = esc(unit)
        body.append(f'<g transform="rotate({rot} 600 60)">'
                    f'<rect x="-60" y="{y + 6}" width="1320" height="40" fill="{shade}" stroke="{INKK}" stroke-width="3"/>'
                    f'<rect x="-60" y="{y}" width="1320" height="40" fill="{fill}" stroke="{INKK}" stroke-width="3"/>'
                    f'<g style="animation:{anim} {dur}s linear infinite">'
                    f'<text class="sans" x="0" y="{y + 27}" font-size="{fs}" font-weight="900" letter-spacing="1" '
                    f'fill="{INKK}" textLength="{L:.1f}" lengthAdjust="spacing">{txt}</text>'
                    f'<text class="sans" x="{L:.1f}" y="{y + 27}" font-size="{fs}" font-weight="900" letter-spacing="1" '
                    f'fill="{INKK}" textLength="{L:.1f}" lengthAdjust="spacing">{txt}</text></g></g>')
    return page(s, W, H, css, "\n  ".join(body), None, grid=False)


# ================================================================ end credits
def build_credits(d):
    s = "e"
    W, H = 1200, 380
    rows = P.CREDITS
    lh = 54
    Lh = len(rows) * lh
    wx, wy, ww, wh = 640, 40, 514, 300
    css = ("@keyframes roll{from{transform:translateY(0)}to{transform:translateY(-%dpx)}}"
           ".roll{animation:roll %ds linear infinite}"
           "@keyframes ink{0%%,8%%{stroke-dashoffset:1}40%%,100%%{stroke-dashoffset:0}}"
           ".ink{animation:ink 7s cubic-bezier(.45,.05,.35,1) infinite}"
           "@keyframes fillin{0%%,38%%{fill-opacity:0}55%%,100%%{fill-opacity:1}}"
           ".fillin{animation:fillin 7s ease-out infinite}"
           "@keyframes q{0%%,100%%{opacity:1}50%%{opacity:0}}"
           ".qm{animation:q 1s steps(1) infinite}" % (Lh, len(rows) * 2.6))
    body = []
    # left: the title card
    body.append(f'<text class="mono ev1" x="{PAD}" y="86" font-size="11" letter-spacing="3.6" fill="{DIM}">'
                f'EPILOGUE &#183; ROLL CREDITS</text>')
    for k, (word, y) in enumerate([("THE", 168), ("END", 268)]):
        body.append(f'<text class="sans ink fillin" x="{PAD - 4}" y="{y}" font-size="112" font-weight="900" '
                    f'letter-spacing="-4" fill="{[CREAM, ROSE][k]}" fill-opacity="1" stroke="{[CREAM, ROSE][k]}" '
                    f'stroke-width="2" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0">{word}</text>')
    body.append(f'<text class="sans qm" x="{PAD + 268}" y="268" font-size="112" font-weight="900" fill="{MINT}">?</text>')
    st, _ = sticker(PAD, 300, "POST-CREDITS SCENE: VOTE ABOVE \u2191", MINT, ROSE, fs=10, h=26, rot=-2)
    body.append(f'<g class="ev3">{st}</g>')

    # right: the credits window
    clip = "cw_" + s
    body.append(card(s, wx, wy, ww, wh, r=18, tint=PURPLE, tint_op=0.16))
    body.append(f'<clipPath id="{clip}"><rect x="{wx}" y="{wy + 2}" width="{ww}" height="{wh - 4}"/></clipPath>')
    col_rows = []
    for rep in (0, 1):
        for j, (role, name) in enumerate(rows):
            y = wy + 70 + (rep * len(rows) + j) * lh
            col_rows.append(f'<text class="mono" x="{wx + ww / 2}" y="{y}" text-anchor="middle" font-size="9.6" '
                            f'letter-spacing="2.6" fill="{[CREAM, ROSE, MINT, VIOLET][j % 4]}">{esc(role)}</text>'
                            f'<text class="sans" x="{wx + ww / 2}" y="{y + 21}" text-anchor="middle" font-size="15" '
                            f'font-weight="700" fill="{INK}">{esc(name)}</text>')
    body.append(f'<g clip-path="url(#{clip})"><g class="roll">{"".join(col_rows)}</g></g>')
    fade = "fd_" + s
    body.append(f'<linearGradient id="{fade}" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0" stop-color="{BG0}"/><stop offset="0.2" stop-color="{BG0}" stop-opacity="0"/>'
                f'<stop offset="0.8" stop-color="{BG0}" stop-opacity="0"/><stop offset="1" stop-color="{BG0}"/>'
                f'</linearGradient><rect x="{wx + 2}" y="{wy + 2}" width="{ww - 4}" height="{wh - 4}" rx="16" '
                f'fill="url(#{fade})"/>')
    return page(s, W, H, css, "\n  ".join(body), None, use_particles=14)
