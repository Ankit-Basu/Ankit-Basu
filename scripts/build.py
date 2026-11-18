"""
Render every SVG panel of the profile README.

    python scripts/fetch_stats.py   # refresh data/stats.json from the GitHub API
    python scripts/build.py         # redraw the panels from that data

Layout lives here, wording lives in profile.py, numbers live in data/stats.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import profile as P  # noqa: E402
from design import (BG0, BG2, INK, DIM, FAINT, CREAM, ROSE, MINT, VIOLET,  # noqa: E402
                    RARITY, esc, rr, card, chip_row, xpbar, ring, page,
                    section_header, uid, ev, lighten)
from icons import icon  # noqa: E402
import story  # noqa: E402
import arcade  # noqa: E402
import game  # noqa: E402
import buttons  # noqa: E402
from design import sticker, brut, INKK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 1200
PAD = 46

LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Java": "#b07219", "C++": "#f34b7d", "C": "#555555", "C#": "#178600",
    "HTML": "#e34c26", "CSS": "#563d7c", "SCSS": "#c6538c", "PHP": "#4F5D95",
    "Blade": "#f7523f", "Shell": "#89e051", "Go": "#00ADD8", "Rust": "#dea584",
    "Kotlin": "#A97BFF", "Swift": "#F05138", "Ruby": "#701516", "Dart": "#00B4AB",
    "Vue": "#41b883", "Jupyter Notebook": "#DA5B0B", "Dockerfile": "#384d54",
}

TIERS = [(3000, "GRANDMASTER"), (1500, "ARCHITECT"), (700, "ENGINEER"),
         (250, "BUILDER"), (0, "INITIATE")]


def load():
    p = os.path.join(ROOT, "data", "stats.json")
    if not os.path.exists(p):
        raise SystemExit("data/stats.json missing - run scripts/fetch_stats.py first")
    return json.load(open(p, encoding="utf-8"))


def fmt(n):
    return "-" if n is None else format(int(n), ",")


def load_avatar():
    """The profile photo, pre-cropped and base64'd into data/avatar.txt.

    It has to be embedded rather than referenced: GitHub renders these panels
    through <img>, and an SVG loaded that way is not allowed to fetch external
    resources, so <image href="profile.jpg"> would silently render nothing.
    Regenerate with scripts/make_avatar.py after changing profile.jpg.
    """
    p = os.path.join(ROOT, "data", "avatar.txt")
    if not os.path.exists(p):
        print("  note: data/avatar.txt missing - banner will omit the portrait")
        return None
    return open(p, encoding="utf-8").read().strip()


def write(name, svg):
    path = os.path.join(ROOT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("  %-16s %6.1f KB" % (name, len(svg) / 1024.0))


# ================================================================ loadout
def build_loadout():
    s = "l"
    body = [section_header(s, PAD, 62, "PLAYER LOADOUT", "Skills, Credentials & Arsenal")]

    tw, gap = 262, 20
    for i, (val, lab, sub, pct, col, ic) in enumerate(P.CREDS):
        x = PAD + i * (tw + gap)
        body.append(f'<g class="{ev(1 + i)}">')
        body.append(card(s, x, 116, tw, 124, r=18, tint=col, tint_op=0.15,
                         sheen=True, sheen_delay=i * 0.8))
        body.append(ring(s, x + 54, 178, 30, pct, col, sw=5, delay=0.4 + i * 0.12))
        body.append(icon(ic, x + 44, 168, 20, col, 1.8, 0.95))
        body.append(f'<text class="sans" x="{x + 100}" y="{172}" font-size="30" '
                    f'font-weight="800" fill="{INK}" letter-spacing="-0.8">{esc(val)}</text>')
        body.append(f'<text class="mono" x="{x + 100}" y="{192}" font-size="9.6" '
                    f'letter-spacing="2.2" fill="{col}" fill-opacity="0.92" font-weight="600">{esc(lab)}</text>')
        body.append(f'<text x="{x + 100}" y="{213}" font-size="10.6" fill="{DIM}">{esc(sub)}</text>')
        body.append("</g>")

    # -- arsenal
    body.append(f'<g class="ev5">')
    body.append(card(s, PAD, 264, 716, 200, r=20, tint=CREAM, tint_op=0.08))
    body.append(f'<text class="mono" x="{PAD + 26}" y="292" font-size="10.5" letter-spacing="3" '
                f'fill="{CREAM}" fill-opacity="0.9" font-weight="600">ARSENAL</text>')
    body.append(f'<rect x="{PAD + 26}" y="300" width="664" height="1" fill="#ffffff" opacity="0.08"/>')
    for gi, (label, col, items) in enumerate(P.ARSENAL):
        gy = 322 + gi * 50
        body.append(f'<text class="mono" x="{PAD + 26}" y="{gy}" font-size="9.4" letter-spacing="2.2" '
                    f'fill="{col}" fill-opacity="0.85">{esc(label)}</text>')
        row, _ = chip_row(s, PAD + 26, gy + 8, items, cols=[col], gap=6, fs=10.6, h=21)
        body.append(row)
    body.append("</g>")

    # -- proficiency
    body.append(f'<g class="ev6">')
    body.append(card(s, 782, 264, 372, 200, r=20, tint=VIOLET, tint_op=0.10))
    body.append(f'<text class="mono" x="808" y="292" font-size="10.5" letter-spacing="3" '
                f'fill="{VIOLET}" fill-opacity="0.9" font-weight="600">PROFICIENCY MATRIX</text>')
    body.append('<rect x="808" y="300" width="320" height="1" fill="#ffffff" opacity="0.08"/>')
    for i, (label, pct, col) in enumerate(P.PROFICIENCY):
        y = 326 + i * 36
        body.append(f'<text x="808" y="{y}" font-size="11.6" fill="{DIM}">{esc(label)}</text>')
        body.append(f'<text class="mono" x="1128" y="{y}" text-anchor="end" font-size="11" '
                    f'font-weight="700" fill="{col}">{pct}%</text>')
        body.append(xpbar(s, 808, y + 7, 320, pct, col, h=6, delay=0.8 + i * 0.14))
    body.append("</g>")

    # -- certifications
    body.append(f'<g class="ev7">')
    body.append(card(s, PAD, 490, 1108, 46, r=15, tint=MINT, tint_op=0.08, shadow=False))
    body.append(icon("medal", PAD + 22, 502, 21, MINT, 1.7, 0.9))
    body.append(f'<text class="mono" x="{PAD + 54}" y="518" font-size="10" letter-spacing="2.4" '
                f'fill="{MINT}" fill-opacity="0.9" font-weight="600">CERTIFIED</text>')
    cx = PAD + 150
    for i, (issuer, title) in enumerate(P.CERTS):
        if i:
            body.append(f'<text x="{cx - 14}" y="519" font-size="12" fill="{FAINT}">&#8226;</text>')
        body.append(f'<text x="{cx}" y="519" font-size="11.6">'
                    f'<tspan fill="{CREAM}" font-weight="600">{esc(issuer)}</tspan>'
                    f'<tspan fill="{DIM}">  {esc(title)}</tspan></text>')
        cx += int((len(issuer) + len(title)) * 6.4) + 40
    body.append("</g>")

    blobs = [(180, 180, 250, CREAM, 0.22, "drift"),
             (620, 420, 240, ROSE, 0.20, "drift2"),
             (1030, 200, 240, VIOLET, 0.22, "drift3")]
    return page(s, W, 570, "", "\n  ".join(body), blobs)


# ================================================================ stats
def build_stats(d):
    s = "s"
    body = [section_header(s, PAD, 62, "LIVE TELEMETRY", "GitHub Activity & Reach", MINT)]

    # sync badge
    body.append(f"""<g class="ev1">
    {card(s, 900, 40, 254, 30, r=15, tint=MINT, tint_op=0.14, shadow=False)}
    <circle cx="922" cy="55" r="3.8" fill="{MINT}"><animate attributeName="opacity"
            values="1;.25;1" dur="1.9s" repeatCount="indefinite"/></circle>
    <text class="mono" x="936" y="59" font-size="9.4" letter-spacing="1.5" fill="{DIM}">
      SYNCED {esc(d.get('synced_at', ''))}</text>
  </g>""")

    tiles = [("pulse", fmt(d.get("total_contributions")), "TOTAL CONTRIBUTIONS",
              "since " + d["created_at"][:7], CREAM),
             ("flame", fmt(d.get("longest")), "LONGEST STREAK", "consecutive days", ROSE),
             ("repo", fmt(d["repos"]), "PUBLIC REPOSITORIES", "%s forks" % d["forks"], MINT),
             ("star", fmt(d["stars"]), "STARS EARNED", "%s followers" % d["followers"], VIOLET)]
    tw, gap = 262, 20
    for i, (ic, val, lab, sub, col) in enumerate(tiles):
        x = PAD + i * (tw + gap)
        body.append(f'<g class="{ev(1 + i)}">')
        body.append(card(s, x, 116, tw, 118, r=18, tint=col, tint_op=0.16,
                         sheen=True, sheen_delay=i * 0.7))
        body.append(icon(ic, x + 22, 138, 22, col, 1.8, 0.9))
        body.append(f'<text class="sans" x="{x + 22}" y="{194}" font-size="38" font-weight="800" '
                    f'fill="{INK}" letter-spacing="-1.4">{val}</text>')
        body.append(f'<text class="mono" x="{x + 22}" y="{214}" font-size="9.2" letter-spacing="1.9" '
                    f'fill="{col}" fill-opacity="0.9" font-weight="600">{esc(lab)}</text>')
        body.append(f'<text class="mono" x="{x + tw - 22}" y="{155}" text-anchor="end" '
                    f'font-size="9.6" fill="{DIM}" fill-opacity="0.85">{esc(sub)}</text>')
        body.append("</g>")

    # -- languages
    langs = sorted(d["languages"].items(), key=lambda kv: -kv[1]["size"])[:6]
    total = sum(v["size"] for _, v in langs) or 1
    body.append('<g class="ev5">')
    body.append(card(s, PAD, 258, 600, 180, r=20, tint=CREAM, tint_op=0.09))
    body.append(f'<text class="mono" x="{PAD + 26}" y="288" font-size="10.5" letter-spacing="3" '
                f'fill="{CREAM}" fill-opacity="0.9" font-weight="600">LANGUAGE DISTRIBUTION</text>')
    body.append(f'<rect x="{PAD + 26}" y="296" width="548" height="1" fill="#ffffff" opacity="0.08"/>')
    for i, (name, meta) in enumerate(langs):
        y = 318 + i * 20
        pct = 100.0 * meta["size"] / total
        col = LANG_COLORS.get(name, meta.get("color") or "#8fb8c9")
        # CSS is #563d7c, C is #555555 - fine as a dot, unreadable as text
        txt = lighten(col, 0.5)
        body.append(f'<circle cx="{PAD + 32}" cy="{y - 4}" r="4" fill="{col}"/>')
        body.append(f'<text x="{PAD + 44}" y="{y}" font-size="11.4" fill="{DIM}">{esc(name)}</text>')
        body.append(xpbar(s, PAD + 168, y - 8, 320, pct, lighten(col, 0.18), h=6,
                          delay=0.7 + i * 0.09, track=0.08))
        body.append(f'<text class="mono" x="{PAD + 574}" y="{y}" text-anchor="end" font-size="10.4" '
                    f'font-weight="700" fill="{txt}">{pct:.1f}%</text>')
    body.append("</g>")

    # -- right panel: real heatmap when the calendar is available
    body.append('<g class="ev6">')
    body.append(card(s, 666, 258, 488, 180, r=20, tint=MINT, tint_op=0.10))
    cal = d.get("calendar") or []
    if cal:
        weeks = 30
        recent = cal[-weeks * 7:]
        peak = max([n for _, n in recent] or [1]) or 1
        # Bucket by quartiles of the active days. A linear ramp against the
        # peak lumps almost everything into level 1 whenever one busy day
        # dwarfs the rest, which flattens the whole grid to a single tone.
        active = sorted(n for _, n in recent if n > 0)
        cuts = [active[int(len(active) * q)] for q in (0.25, 0.5, 0.75)] if active else [1, 2, 3]
        body.append('<text class="mono" x="692" y="288" font-size="10.5" letter-spacing="3" '
                    'fill="%s" fill-opacity="0.9" font-weight="600">'
                    'CONTRIBUTION HEATMAP &#183; LAST 30 WEEKS</text>' % MINT)
        body.append('<rect x="692" y="296" width="436" height="1" fill="#ffffff" opacity="0.08"/>')
        step, cell = 14.3, 11.6
        for idx, (day, n) in enumerate(recent):
            cx = 694 + (idx // 7) * step
            cy = 308 + (idx % 7) * step
            lvl = 0 if n == 0 else 1 + sum(1 for c in cuts if n > c)
            fill = ["#ffffff", MINT, MINT, MINT, MINT][lvl]
            op = [0.06, 0.18, 0.38, 0.62, 0.92][lvl]
            dl = 0.6 + (idx // 7) * 0.018
            body.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell}" height="{cell}" rx="3" '
                        f'fill="{fill}" opacity="{op}" class="{ev(6 + idx // 7)}"/>')
        body.append(f'<text class="mono" x="692" y="425" font-size="9" fill="{DIM}">LESS</text>')
        for j in range(5):
            fill = ["#ffffff", MINT, MINT, MINT, MINT][j]
            op = [0.06, 0.18, 0.38, 0.62, 0.92][j]
            body.append(f'<rect x="{728 + j * 15}" y="416" width="11" height="11" rx="3" '
                        f'fill="{fill}" opacity="{op}"/>')
        body.append(f'<text class="mono" x="{728 + 5 * 15 + 4}" y="425" font-size="9" fill="{DIM}">MORE</text>')
        body.append(f'<text class="mono" x="1128" y="425" text-anchor="end" font-size="9.4" '
                    f'fill="{DIM}">PEAK {peak}/DAY</text>')
    else:
        body.append('<text class="mono" x="692" y="288" font-size="10.5" letter-spacing="3" '
                    'fill="%s" fill-opacity="0.9" font-weight="600">PROFILE SIGNAL</text>' % MINT)
        body.append('<rect x="692" y="296" width="436" height="1" fill="#ffffff" opacity="0.08"/>')
        rows = [("users", "Followers", fmt(d["followers"]), CREAM),
                ("fork", "Forks of my work", fmt(d["forks"]), ROSE),
                ("clock", "Years on GitHub", str(d.get("years_active", "-")), MINT),
                ("flame", "Current streak",
                 "%s day%s" % (fmt(d.get("current")), "" if d.get("current") == 1 else "s"),
                 VIOLET)]
        for i, (ic, lab, val, col) in enumerate(rows):
            y = 324 + i * 30
            body.append(icon(ic, 694, y - 14, 18, col, 1.7, 0.85))
            body.append(f'<text x="722" y="{y}" font-size="12" fill="{DIM}">{esc(lab)}</text>')
            body.append(f'<text class="sans" x="1128" y="{y + 1}" text-anchor="end" font-size="17" '
                        f'font-weight="800" fill="{col}">{esc(val)}</text>')
            if i < 3:
                body.append(f'<rect x="694" y="{y + 11}" width="434" height="1" fill="#ffffff" opacity="0.06"/>')
    body.append("</g>")

    body.append(f'<text class="mono" x="{W // 2}" y="462" text-anchor="middle" font-size="9.6" '
                f'letter-spacing="1.6" fill="{FAINT}">'
                f'PULLED STRAIGHT FROM THE GITHUB API &#183; REBUILT DAILY BY GITHUB ACTIONS</text>')

    blobs = [(200, 180, 250, MINT, 0.20, "drift"),
             (700, 380, 250, CREAM, 0.18, "drift2"),
             (1050, 200, 230, VIOLET, 0.20, "drift3")]
    return page(s, W, 480, "", "\n  ".join(body), blobs)


# ================================================================ trophies
def build_trophies(d):
    s = "t"
    css = """
    @keyframes halo{0%,100%{opacity:.20}50%{opacity:.55}}
    """
    body = [section_header(s, PAD, 62, "UNLOCKED", "Achievements & milestones", VIOLET)]

    tw, gap = 262, 20
    for i, (ic, title, sub, val, unit, col) in enumerate(P.TROPHIES):
        x = PAD + i * (tw + gap)
        cx = x + tw // 2
        body.append(f'<g class="{ev(1 + i)}">')
        body.append(card(s, x, 112, tw, 196, r=20, tint=col, tint_op=0.18,
                         sheen=True, sheen_delay=i * 0.85))
        # medallion
        body.append(f'<circle cx="{cx}" cy="158" r="30" fill="{col}" fill-opacity="0.09" '
                    f'stroke="{col}" stroke-opacity="0.38" stroke-width="1.3"/>')
        body.append(f'<circle cx="{cx}" cy="158" r="35" fill="none" stroke="{col}" '
                    f'stroke-width="1" stroke-opacity="0.3" stroke-dasharray="3 7" '
                    f'style="animation:halo 3.6s ease-in-out {i * 0.35}s infinite"/>')
        body.append(icon(ic, cx - 14, 144, 28, col, 1.6, 1.0))
        body.append(f'<text class="sans" x="{cx}" y="{206}" text-anchor="middle" font-size="15.5" '
                    f'font-weight="700" fill="{INK}">{esc(title)}</text>')
        body.append(f'<text x="{cx}" y="{225}" text-anchor="middle" font-size="10.8" '
                    f'fill="{DIM}">{esc(sub)}</text>')
        body.append(f'<rect x="{x + 42}" y="238" width="{tw - 84}" height="1" fill="#ffffff" opacity="0.09"/>')
        body.append(f'<text class="sans" x="{cx}" y="{278}" text-anchor="middle" font-size="30" '
                    f'font-weight="800" fill="{col}" letter-spacing="-1">{esc(val)}</text>')
        body.append(f'<text class="mono" x="{cx}" y="{294}" text-anchor="middle" font-size="8.8" '
                    f'letter-spacing="2.2" fill="{DIM}">{esc(unit)}</text>')
        body.append("</g>")

    # live milestone strip
    strip = [("star", "%s STARS EARNED" % d["stars"], CREAM),
             ("users", "%s FOLLOWERS" % d["followers"], ROSE),
             ("repo", "%s PUBLIC REPOS" % d["repos"], MINT),
             ("clock", "%s YEARS BUILDING" % d.get("years_active", "-"), VIOLET)]
    body.append('<g class="ev7">')
    body.append(card(s, PAD, 330, 1108, 46, r=15, tint=CREAM, tint_op=0.07, shadow=False))
    seg = 1108 // 4
    for i, (ic, label, col) in enumerate(strip):
        cx = PAD + seg * i + seg // 2
        body.append(icon(ic, cx - 58, 342, 20, col, 1.7, 0.9))
        body.append(f'<text class="mono" x="{cx - 30}" y="{359}" font-size="10.4" letter-spacing="1.8" '
                    f'fill="{DIM}" font-weight="600">{esc(label)}</text>')
        if i:
            body.append(f'<rect x="{PAD + seg * i}" y="344" width="1" height="18" fill="#ffffff" opacity="0.1"/>')
    body.append("</g>")

    # -- achievement toasts: slide in, hold, slide out, one after another.
    # Resting state is the first toast, fully shown.
    stars = {r["name"]: r["stars"] for r in d.get("top_repos", [])}
    toasts = [("flame", "%s-day streak" % fmt(d.get("longest")), "Longest run without missing a day", MINT),
              ("star", "SheShield hit %s stars" % stars.get("SheShield", d["stars"]), "Most-starred build", CREAM),
              ("pulse", "%s contributions" % fmt(d.get("total_contributions")), "And still counting", ROSE)]
    T, n = 15.0, len(toasts)
    slot = 100.0 / n
    tx, ty, tw, th = 806, 30, 348, 58
    for k, (ic, name, sub, col) in enumerate(toasts):
        a = k * slot
        css += ("@keyframes tst%d{0%%,%.2f%%{transform:translateX(40px);opacity:0}"
                "%.2f%%,%.2f%%{transform:translateX(0);opacity:1}%.2f%%,100%%{transform:translateX(40px);opacity:0}}"
                ".tst%d{animation:tst%d %.0fs cubic-bezier(.22,1,.36,1) infinite}\n"
                % (k, a, a + 3, a + slot - 3, a + slot, k, k, T))
        body.append(f'<g class="tst{k}" opacity="{1 if k == 0 else 0}">'
                    f'{brut(tx, ty, tw, th, BG2, col, r=29, off=4, bw=2.4)}'
                    f'<circle cx="{tx + 29}" cy="{ty + 29}" r="19" fill="{col}" stroke="{INKK}" stroke-width="2"/>'
                    f'{icon(ic, tx + 19, ty + 19, 20, INKK, 2.2, 1)}'
                    f'<text class="mono" x="{tx + 60}" y="{ty + 24}" font-size="9" letter-spacing="2" '
                    f'fill="{col}" font-weight="800">ACHIEVEMENT UNLOCKED</text>'
                    f'<text class="sans" x="{tx + 60}" y="{ty + 44}" font-size="14.5" font-weight="800" '
                    f'fill="{INK}">{esc(name)}</text>'
                    f'<text x="{tx + tw - 18}" y="{ty + 44}" text-anchor="end" font-size="10" '
                    f'fill="{DIM}">{esc(sub)}</text></g>')

    return page(s, W, 400, css, "\n  ".join(body), None)


# ================================================================ quest log
def build_questlog():
    s = "q"
    prompt = "cat now_building.md"
    css = """
    @keyframes type{0%,22%{width:0}100%{width:176px}}
    .tyw{animation:type 2.4s steps(22,end);}
    @keyframes scan{0%{transform:translateY(-40px)}100%{transform:translateY(320px)}}
    """

    body = [card(s, 40, 40, 1120, 296, r=22, tint=MINT, tint_op=0.09)]

    # window chrome
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        body.append(f'<circle cx="{72 + i * 20}" cy="72" r="5.5" fill="{c}" opacity="0.9"/>')
    body.append(f'<text class="mono" x="600" y="76" text-anchor="middle" font-size="11.2" '
                f'letter-spacing="1.2" fill="{DIM}">ankit@system: ~/production</text>')
    body.append(f'<text class="mono" x="1128" y="76" text-anchor="end" font-size="9.6" '
                f'letter-spacing="1.6" fill="{MINT}" fill-opacity="0.8">&#9679; LIVE</text>')
    body.append('<rect x="40" y="94" width="1120" height="1" fill="#ffffff" opacity="0.09"/>')

    # prompt with typing reveal
    cid = uid("ty")
    body.append(f"""<g>
    <text class="mono" x="72" y="128" font-size="12.8">
      <tspan fill="{MINT}">ankit@system</tspan><tspan fill="{DIM}">:</tspan
      ><tspan fill="{VIOLET}">~/production</tspan><tspan fill="{DIM}">$ </tspan></text>
    <clipPath id="{cid}"><rect class="tyw" x="280" y="112" width="176" height="24"/></clipPath>
    <text class="mono" x="280" y="128" font-size="12.8" fill="{CREAM}"
          clip-path="url(#{cid})">{prompt}</text>
  </g>""")

    for i, (title, desc, pct, col) in enumerate(P.QUESTS):
        y = 172 + i * 34
        body.append(f'<g class="{ev(9 + i)}">')
        body.append(f'<text class="mono" x="72" y="{y}" font-size="12.4" fill="{col}" '
                    f'font-weight="600">&#9656; {esc(title)}</text>')
        body.append(f'<text x="268" y="{y}" font-size="11.6" fill="{DIM}">{esc(desc)}</text>')
        body.append(xpbar(s, 800, y - 9, 250, pct, col, h=6, delay=1.8 + i * 0.14, track=0.09))
        body.append(f'<text class="mono" x="1128" y="{y}" text-anchor="end" font-size="11" '
                    f'font-weight="700" fill="{col}">{pct}%</text>')
        body.append("</g>")

    body.append(f'<text class="mono" x="72" y="316" font-size="12.8">'
                f'<tspan fill="{MINT}">ankit@system</tspan><tspan fill="{DIM}">:</tspan>'
                f'<tspan fill="{VIOLET}">~/production</tspan><tspan fill="{DIM}">$</tspan>'
                f'<tspan fill="{CREAM}" style="animation:blink 1.1s steps(1) infinite"> &#9646;</tspan></text>')

    # CRT scanline
    scid = uid("sc")
    body.append(f'<clipPath id="{scid}"><path d="{rr(40, 40, 1120, 296, 22)}"/></clipPath>'
                f'<g clip-path="url(#{scid})" opacity="0.5">'
                f'<rect x="40" y="40" width="1120" height="34" fill="url(#sheen_{s})" '
                f'style="animation:scan 7s linear infinite"/></g>')

    # currently learning
    body.append('<g class="ev21">')
    body.append(card(s, 40, 352, 1120, 44, r=15, tint=VIOLET, tint_op=0.08, shadow=False))
    body.append(icon("cpu", 66, 364, 20, VIOLET, 1.7, 0.9))
    body.append(f'<text class="mono" x="98" y="379" font-size="10" letter-spacing="2.4" '
                f'fill="{VIOLET}" fill-opacity="0.9" font-weight="600">LEVELLING UP</text>')
    row, _ = chip_row(s, 240, 363, P.LEARNING, cols=[CREAM, ROSE, MINT, VIOLET],
                      gap=8, fs=10.8, h=22)
    body.append(row)
    body.append("</g>")

    blobs = [(240, 150, 240, MINT, 0.18, "drift"),
             (820, 260, 250, VIOLET, 0.20, "drift2")]
    return page(s, W, 416, css, "\n  ".join(body), blobs)


# ================================================================ footer
def build_footer():
    s = "f"
    links = [("github", "GITHUB", P.GITHUB, CREAM),
             ("linkedin", "LINKEDIN", P.LINKEDIN, MINT),
             ("instagram", "INSTAGRAM", P.INSTAGRAM, ROSE),
             ("mail", "EMAIL", P.EMAIL, VIOLET)]
    body = []
    tw, gap = 262, 20
    for i, (ic, plat, handle, col) in enumerate(links):
        x = PAD + i * (tw + gap)
        body.append(f'<g class="{ev(1 + i)}">')
        body.append(card(s, x, 46, tw, 78, r=18, tint=col, tint_op=0.16,
                         sheen=True, sheen_delay=i * 0.75))
        body.append(f'<circle cx="{x + 40}" cy="85" r="21" fill="{col}" fill-opacity="0.10" '
                    f'stroke="{col}" stroke-opacity="0.35"/>')
        body.append(icon(ic, x + 27, 72, 26, col, 1.8, 0.95))
        body.append(f'<text class="mono" x="{x + 74}" y="{80}" font-size="9.4" letter-spacing="2.4" '
                    f'fill="{col}" fill-opacity="0.9" font-weight="600">{plat}</text>')
        fs = 12.5 if len(handle) < 20 else 10.2
        body.append(f'<text x="{x + 74}" y="{99}" font-size="{fs}" fill="{INK}">{esc(handle)}</text>')
        body.append("</g>")

    body.append(f'<g class="ev5">')
    body.append(f'<text class="mono" x="{W // 2}" y="172" text-anchor="middle" font-size="12" '
                f'letter-spacing="5.6" fill="{CREAM}" fill-opacity="0.92" font-weight="600" '
                f'filter="url(#glowS_{s})">{esc(P.MOTTO)}</text>')
    body.append(f'<rect x="{W // 2 - 190}" y="184" width="380" height="1" fill="url(#spec_{s})"/>')
    body.append(f'<text x="{W // 2}" y="212" text-anchor="middle" font-size="14" '
                f'font-style="italic" fill="{DIM}">&#8220;{esc(P.QUOTE)}&#8221;</text>')
    body.append(f'<text class="mono" x="{W // 2}" y="238" text-anchor="middle" font-size="9.6" '
                f'letter-spacing="2.6" fill="{FAINT}">{esc(P.LOCATION.upper())}</text>')
    body.append("</g>")

    blobs = [(240, 120, 250, CREAM, 0.20, "drift"),
             (640, 210, 260, ROSE, 0.18, "drift2"),
             (1000, 120, 240, VIOLET, 0.20, "drift3")]
    st, stw = sticker(W // 2 - 92, 262, "TO BE CONTINUED \u25B8", CREAM, ROSE, fs=11, h=28)
    body.append('<g class="ev6"><g style="animation:breathe2 2.4s ease-in-out infinite">%s</g></g>' % st)
    css = "@keyframes breathe2{0%,100%{opacity:1}50%{opacity:.72}}"
    return page(s, W, 316, css, "\n  ".join(body), blobs, use_particles=12)


# ================================================================ main
def main():
    d = load()
    print("building panels from data synced %s" % d.get("synced_at"))
    write("banner.svg", story.build_hero(d))
    write("hud.svg", game.build_hud(d))
    write("marquee.svg", arcade.build_marquee())
    write("marquee2.svg", arcade.build_marquee(flip=True))
    write("credits.svg", arcade.build_credits(d))
    for i in range(len(P.CHAPTERS)):
        write("chapter%d.svg" % (i + 1), story.build_chapter(i))
    write("timeline.svg", story.build_timeline())
    write("loadout.svg", build_loadout())
    write("skilltree.svg", game.build_skilltree())
    write("projects.svg", story.build_vault(d))
    write("stats.svg", build_stats(d))
    write("city.svg", story.build_city(d))
    write("companion.svg", arcade.build_companion(d))
    write("ticker.svg", arcade.build_ticker(d))
    write("trophies.svg", build_trophies(d))
    boss_pct = next((q[2] for q in P.QUESTS if q[0] == P.BOSS["quest"]), 0)
    write("boss.svg", game.build_boss(boss_pct))
    write("questlog.svg", build_questlog())
    write("votes.svg", arcade.build_votes())
    write("footer.svg", build_footer())
    os.makedirs(os.path.join(ROOT, "btn"), exist_ok=True)
    buttons.build_all(write)
    print("done")


if __name__ == "__main__":
    main()
