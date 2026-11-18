"""
The game layer: the panels that make the README play like a game.

  hud.svg        the always-on HUD - level, streak hearts, XP, coins, location
  skilltree.svg  a tech tree: unlocked skills glow, the ones in training are locked
  boss.svg       the current main quest drawn as a boss fight

All motion is transform / opacity / stroke-dashoffset, with no filters - see
design.page() for why that matters in an animated <img>.
"""
import profile as P
from design import (BG0, BG2, INK, DIM, FAINT, CREAM, ROSE, MINT, VIOLET, PURPLE, INKK,
                    esc, card, page, section_header, ev, brut, sticker, uid)
from icons import icon

W = 1200
PAD = 46


def fmt(n):
    return "-" if n is None else format(int(n), ",")


def _heart(x, y, px, fill, cls=""):
    """A 7x6 pixel heart."""
    rows = [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."]
    cells = "".join(f'<rect x="{x + c * px}" y="{y + r * px}" width="{px}" height="{px}"/>'
                    for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == "X")
    c = f' class="{cls}"' if cls else ""
    return f'<g{c} fill="{fill}" style="transform-origin:{x + 3.5 * px}px {y + 3 * px}px">{cells}</g>'


# ================================================================ HUD
def build_hud(d):
    s = "u"
    H = 104
    tc = int(d.get("total_contributions") or 0)
    lvl = max(1, tc // 100)
    xp = tc % 100
    cur = int(d.get("current") or 0)
    hearts = 7
    lit = min(cur, hearts)
    css = """
    @keyframes beat{0%,100%{opacity:1}50%{opacity:.45}}
    .beat{animation:beat 1.6s ease-in-out infinite}
    @keyframes xpsh{from{transform:translateX(-120px)}to{transform:translateX(420px)}}
    @keyframes coin{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.15)}}
    @keyframes rec{0%,100%{opacity:1}50%{opacity:.2}}
    """
    body = []
    # frame: one thin ink-bordered bar, like a console HUD
    body.append(f'<rect x="{PAD - 20}" y="16" width="{W - 2 * PAD + 40}" height="72" rx="14" fill="{BG2}" '
                f'stroke="#ffffff" stroke-opacity="0.08"/>')
    # level badge
    body.append(brut(PAD, 28, 72, 48, CREAM, ROSE, r=10, off=4, bw=2.4))
    body.append(f'<text class="mono" x="{PAD + 36}" y="46" text-anchor="middle" font-size="9" font-weight="800" '
                f'letter-spacing="1.6" fill="{INKK}">LV</text>'
                f'<text class="sans" x="{PAD + 36}" y="69" text-anchor="middle" font-size="22" font-weight="900" '
                f'fill="{INKK}">{lvl}</text>')
    # HP = streak hearts
    hx = PAD + 100
    body.append(f'<text class="mono" x="{hx}" y="40" font-size="9" letter-spacing="2" fill="{ROSE}" '
                f'font-weight="800">STREAK HP</text>')
    for k in range(hearts):
        on = k < lit
        cls = "beat" if on and k == lit - 1 else ""
        sx_ = hx + k * 30
        body.append(f'<rect class="{cls}" x="{sx_}" y="52" width="24" height="10" rx="5" '
                    f'fill="{ROSE if on else "#ffffff"}" fill-opacity="{1 if on else 0.08}" '
                    f'style="transform-origin:{sx_ + 12}px 57px"/>')
    body.append(f'<text class="mono" x="{hx + hearts * 30 + 2}" y="70" font-size="10" fill="{DIM}">'
                f'{cur}d</text>')
    # XP bar
    xx, xw = hx + hearts * 30 + 48, 300
    body.append(f'<text class="mono" x="{xx}" y="40" font-size="9" letter-spacing="2" fill="{MINT}" '
                f'font-weight="800">XP</text>'
                f'<text class="mono" x="{xx + xw}" y="40" text-anchor="end" font-size="9" fill="{DIM}">'
                f'{100 - xp} TO LV {lvl + 1}</text>')
    clip = uid("xc")
    body.append(f'<clipPath id="{clip}"><rect x="{xx}" y="50" width="{xw * xp / 100:.1f}" height="16"/></clipPath>')
    body.append(f'<rect x="{xx}" y="50" width="{xw}" height="16" fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.1" stroke-width="1"/>')
    segs = "".join(f'<rect x="{xx + 2 + k * 10}" y="52" width="8" height="12" fill="{MINT}"/>' for k in range(xw // 10))
    body.append(f'<g clip-path="url(#{clip})">{segs}'
                f'<rect x="{xx}" y="50" width="60" height="16" fill="#ffffff" opacity="0.35" '
                f'style="animation:xpsh 2.8s linear infinite"/></g>')
    body.append(f'<text class="mono" x="{xx}" y="80" font-size="9" fill="{FAINT}">{fmt(tc)} XP TOTAL</text>')
    # coins = stars
    cx = xx + xw + 44
    body.append(f'<g style="animation:coin 2.4s ease-in-out infinite;transform-origin:{cx + 11}px 58px">'
                f'<circle cx="{cx + 11}" cy="58" r="11" fill="{CREAM}"/>'
                f'<text class="sans" x="{cx + 11}" y="63" text-anchor="middle" font-size="12" font-weight="900" '
                f'fill="{INKK}">&#9733;</text></g>')
    body.append(f'<text class="mono" x="{cx + 30}" y="40" font-size="9" letter-spacing="2" fill="{CREAM}" '
                f'font-weight="800">COINS</text>'
                f'<text class="sans" x="{cx + 30}" y="66" font-size="20" font-weight="900" fill="{INK}">'
                f'{fmt(d.get("stars"))}</text>')
    # location
    lx = W - PAD
    body.append(f'<text class="mono" x="{lx}" y="40" text-anchor="end" font-size="9" letter-spacing="2" '
                f'fill="{VIOLET}" font-weight="800">LOCATION</text>'
                f'<text class="sans" x="{lx}" y="62" text-anchor="end" font-size="15" font-weight="800" '
                f'fill="{INK}">Jalandhar, IN</text>'
                f'<text class="mono" x="{lx}" y="78" text-anchor="end" font-size="9" fill="{FAINT}">'
                f'<tspan fill="{ROSE}" style="animation:rec 1.2s steps(1) infinite">&#9679;</tspan>'
                f' PLAYTIME {d.get("years_active", "-")} YRS</text>')
    return page(s, W, H, css, "\n  ".join(body), None, grid=False)


# ================================================================ skill tree
def build_skilltree():
    s = "k2"
    H = 470
    css = """
    @keyframes flow{from{stroke-dashoffset:24}to{stroke-dashoffset:0}}
    .flow{animation:flow 1.1s linear infinite}
    @keyframes pulse2{0%,100%{opacity:.35}50%{opacity:.9}}
    .pls{animation:pulse2 2.6s ease-in-out infinite}
    """
    body = [section_header(s, PAD, 62, "TECH TREE", "Unlocked, and still unlocking", MINT)]
    rx, ry = 120, 280
    # root node
    body.append(brut(rx - 62, ry - 26, 124, 52, CREAM, ROSE, r=12, off=5, bw=2.6))
    body.append(f'<text class="mono" x="{rx}" y="{ry - 6}" text-anchor="middle" font-size="8.6" font-weight="800" '
                f'letter-spacing="1.6" fill="{INKK}">ROOT</text>'
                f'<text class="sans" x="{rx}" y="{ry + 13}" text-anchor="middle" font-size="14" font-weight="900" '
                f'fill="{INKK}">{esc(P.SKILL_ROOT)}</text>')
    rows = len(P.SKILL_TREE)
    top, gap = 130, 92
    x0, step = 290, 182
    for bi, (branch, col, nodes) in enumerate(P.SKILL_TREE):
        y = top + bi * gap
        # trunk from root to branch label
        body.append(f'<path d="M{rx + 62} {ry}C{rx + 110} {ry} {x0 - 110} {y} {x0 - 44} {y}" fill="none" '
                    f'stroke="{col}" stroke-opacity="0.35" stroke-width="2"/>'
                    f'<path class="flow" d="M{rx + 62} {ry}C{rx + 110} {ry} {x0 - 110} {y} {x0 - 44} {y}" fill="none" '
                    f'stroke="{col}" stroke-width="2" stroke-dasharray="4 8"/>')
        body.append(f'<text class="mono {ev(1 + bi)}" x="{x0 - 40}" y="{y - 26}" font-size="9" letter-spacing="2" '
                    f'fill="{col}" font-weight="800">{esc(branch)}</text>')
        prev = x0 - 44
        for ni, (name, unlocked) in enumerate(nodes):
            nx = x0 + ni * step
            # edge
            if unlocked:
                body.append(f'<path d="M{prev} {y}H{nx - 70}" stroke="{col}" stroke-opacity="0.35" stroke-width="2"/>'
                            f'<path class="flow" d="M{prev} {y}H{nx - 70}" stroke="{col}" stroke-width="2" '
                            f'stroke-dasharray="4 8"/>')
            else:
                body.append(f'<path d="M{prev} {y}H{nx - 70}" stroke="#ffffff" stroke-opacity="0.18" '
                            f'stroke-width="2" stroke-dasharray="2 6"/>')
            # node: a pill
            nw = 140
            g = f'<g class="{ev(2 + bi + ni)}">'
            if unlocked:
                g += (f'<rect x="{nx - 70}" y="{y - 17}" width="{nw}" height="34" rx="17" fill="{col}" '
                      f'fill-opacity="0.14" stroke="{col}" stroke-width="1.6"/>'
                      f'<rect class="pls" x="{nx - 74}" y="{y - 21}" width="{nw + 8}" height="42" rx="21" fill="none" '
                      f'stroke="{col}" stroke-opacity="0.5" style="animation-delay:{-(bi * 0.7 + ni * 0.4):.1f}s"/>'
                      f'<circle cx="{nx - 52}" cy="{y}" r="5" fill="{col}"/>'
                      f'<text x="{nx - 40}" y="{y + 4.5}" font-size="12.5" font-weight="700" fill="{INK}">{esc(name)}</text>')
            else:
                g += (f'<rect x="{nx - 70}" y="{y - 17}" width="{nw}" height="34" rx="17" fill="{BG2}" '
                      f'stroke="#ffffff" stroke-opacity="0.22" stroke-dasharray="4 4"/>'
                      f'<g transform="translate({nx - 58} {y - 8})" fill="none" stroke="{FAINT}" stroke-width="1.6">'
                      f'<rect x="0" y="6" width="12" height="10" rx="2" fill="{FAINT}" fill-opacity="0.25"/>'
                      f'<path d="M3 6V4a3 3 0 0 1 6 0v2"/></g>'
                      f'<text x="{nx - 40}" y="{y + 4.5}" font-size="12.5" font-weight="600" fill="{FAINT}">{esc(name)}</text>')
            g += "</g>"
            body.append(g)
            prev = nx + 70
    unlocked = sum(1 for _, _, ns in P.SKILL_TREE for _, u in ns if u)
    total = sum(len(ns) for _, _, ns in P.SKILL_TREE)
    st, _ = sticker(W - PAD - 200, 44, "%d / %d SKILLS UNLOCKED" % (unlocked, total), MINT, ROSE, fs=10, h=26, rot=2)
    body.append(f'<g class="ev10">{st}</g>')
    body.append(f'<text class="mono" x="{W // 2}" y="{H - 18}" text-anchor="middle" font-size="9.4" letter-spacing="1.4" '
                f'fill="{FAINT}">LOCKED NODES ARE IN TRAINING RIGHT NOW &#183; ENERGY FLOWS FROM THE ROOT</text>')
    return page(s, W, H, css, "\n  ".join(body), None)


# ================================================================ boss fight
def build_boss(quest_pct):
    s = "b"
    H = 360
    B = P.BOSS
    hp = max(0, 100 - quest_pct)
    css = """
    @keyframes wav{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}
    @keyframes shake{0%,86%,100%{transform:translate(0,0)}88%{transform:translate(-5px,2px)}90%{transform:translate(5px,-2px)}92%{transform:translate(-4px,1px)}94%{transform:translate(3px,0)}}
    .shk{animation:shake 4s linear infinite}
    @keyframes dmg{0%,84%{transform:translateY(0);opacity:0}88%{opacity:1}100%{transform:translateY(-40px);opacity:0}}
    .dmg{animation:dmg 4s ease-out infinite}
    @keyframes hit{0%,86%,100%{opacity:0}88%{opacity:.5}}
    .hit{animation:hit 4s linear infinite}
    @keyframes blinkB{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.1)}}
    @keyframes now{0%,100%{opacity:1}50%{opacity:.3}}
    .nowb{animation:now 1s steps(1) infinite}
    """
    body = []
    st, sw = sticker(PAD, 34, "BOSS ENCOUNTER", ROSE, fs=10.4, h=28)
    body.append(f'<g class="ev1">{st}</g>')
    body.append(f'<text class="sans ev1" x="{PAD}" y="104" font-size="38" font-weight="900" fill="{INK}" '
                f'letter-spacing="-1">{esc(B["name"])}</text>')
    body.append(f'<text class="ev2" x="{PAD}" y="128" font-size="13" fill="{DIM}">{esc(B["lore"])}</text>')

    # the boss: a living waveform with eyes
    bx, by, bw, bh = PAD, 150, 470, 150
    body.append(f'<g class="shk">')
    body.append(card(s, bx, by, bw, bh, r=18, tint=ROSE, tint_op=0.2))
    nb = 34
    for k in range(nb):
        x = bx + 22 + k * ((bw - 44) / nb)
        h = 26 + 70 * abs(((k * 7) % 11) / 10.0 - 0.5) * 2
        cy = by + bh / 2 + 8
        col = ROSE if k % 5 else CREAM
        body.append(f'<rect x="{x:.1f}" y="{cy - h / 2:.1f}" width="7" height="{h:.1f}" rx="3.5" fill="{col}" '
                    f'style="animation:wav {0.7 + (k % 4) * 0.18:.2f}s ease-in-out {-k * 0.09:.2f}s infinite;'
                    f'transform-origin:{x + 3.5:.1f}px {cy:.1f}px"/>')
    ex, ey = bx + bw / 2, by + 30
    for dx in (-36, 36):
        body.append(f'<g style="animation:blinkB 3.4s infinite;transform-origin:{ex + dx}px {ey}px">'
                    f'<rect x="{ex + dx - 12}" y="{ey - 9}" width="24" height="18" rx="4" fill="{INKK}" stroke="{CREAM}" stroke-width="2"/>'
                    f'<rect x="{ex + dx - 3 + (4 if dx < 0 else -4)}" y="{ey - 4}" width="8" height="8" fill="{CREAM}"/></g>')
    body.append(f'<rect class="hit" x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="18" fill="#ffffff" opacity="0"/>')
    body.append("</g>")
    body.append(f'<text class="sans dmg" x="{bx + bw - 70}" y="{by + 40}" font-size="26" font-weight="900" '
                f'fill="{CREAM}" stroke="{INKK}" stroke-width="1.5" opacity="0">-{quest_pct}%</text>')

    # HP bar
    hx, hy, hw = PAD, 318, 470
    body.append(f'<text class="mono" x="{hx}" y="{hy - 6}" font-size="9.4" letter-spacing="2" fill="{ROSE}" '
                f'font-weight="800">BOSS HP</text>'
                f'<text class="mono" x="{hx + hw}" y="{hy - 6}" text-anchor="end" font-size="9.4" fill="{DIM}">'
                f'{hp}% REMAINING</text>')
    body.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="18" fill="{BG2}" stroke="{INKK}" stroke-width="2.4"/>')
    segs = int(hw / 12)
    lit = round(segs * hp / 100)
    body.append("".join(f'<rect x="{hx + 3 + k * 12}" y="{hy + 3}" width="9" height="12" '
                        f'fill="{ROSE if k < lit else "#2a2f3a"}"/>' for k in range(segs)))

    # right: the player's moves = the quest's phases
    mx = 600
    body.append(card(s, mx, 40, W - PAD - mx, 290, r=18, tint=PURPLE, tint_op=0.16))
    body.append(f'<text class="mono" x="{mx + 24}" y="72" font-size="10" letter-spacing="2.6" fill="{MINT}" '
                f'font-weight="800">YOUR MOVES &#183; QUEST: {esc(B["quest"].upper())}</text>')
    for i, (ph, label, state) in enumerate(B["moves"]):
        y = 104 + i * 38
        col = {"done": MINT, "now": CREAM, "next": FAINT}[state]
        mark = {"done": "&#10003;", "now": "&#9654;", "next": "&#183;"}[state]
        mcls = "mono nowb" if state == "now" else "mono"
        body.append(f'<g class="{ev(3 + i)}">'
                    f'<rect x="{mx + 22}" y="{y - 16}" width="{W - PAD - mx - 44}" height="30" rx="8" '
                    f'fill="{col}" fill-opacity="{0.12 if state != "next" else 0.04}" '
                    f'stroke="{col}" stroke-opacity="{0.6 if state != "next" else 0.2}"/>'
                    f'<text class="{mcls}" x="{mx + 38}" y="{y + 4}" font-size="12" font-weight="800" fill="{col}">{mark}</text>'
                    f'<text class="mono" x="{mx + 60}" y="{y + 4}" font-size="10" fill="{col}" letter-spacing="1.4">PHASE {ph}</text>'
                    f'<text x="{mx + 140}" y="{y + 4}" font-size="13" font-weight="700" '
                    f'fill="{INK if state != "next" else DIM}">{esc(label)}</text>'
                    f'<text class="mono" x="{W - PAD - 40}" y="{y + 4}" text-anchor="end" font-size="9.4" '
                    f'fill="{col}">{state.upper()}</text></g>')
    body.append(f'<text x="{mx + 24}" y="312" font-size="12" font-style="italic" fill="{DIM}">{esc(B["weak"])}</text>')
    return page(s, W, H, css, "\n  ".join(body), None)
