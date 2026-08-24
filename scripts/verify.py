"""
Sanity-check the generated panels before they get committed.

The daily workflow commits whatever build.py produces, so this runs in
between as a gate. It catches the failures that are invisible in a diff but
obvious to a visitor:

  * malformed XML                    -> GitHub shows a broken image
  * duplicate element ids            -> gradients and clip paths bleed together
  * url(#...) pointing at nothing    -> shapes render black or disappear
  * a class with no matching rule    -> silently unstyled / unanimated
  * animation-fill-mode: both        -> the card is blank until its animation
                                        runs, so anything that samples the
                                        first frame shows an empty panel

    python scripts/verify.py
"""
import collections
import glob
import os
import re
import sys
import xml.dom.minidom

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANELS = ["banner", "divider", "loadout", "projects", "stats",
          "trophies", "questlog", "footer"]


def check(path):
    name = os.path.basename(path)
    src = open(path, encoding="utf-8").read()
    problems = []

    try:
        xml.dom.minidom.parseString(src.encode("utf-8"))
    except Exception as e:
        return ["%s: invalid XML - %s" % (name, e)]

    ids = re.findall(r'\sid="([^"]+)"', src)
    dup = sorted(k for k, v in collections.Counter(ids).items() if v > 1)
    if dup:
        problems.append("%s: duplicate ids %s" % (name, dup[:5]))

    refs = set(re.findall(r"url\(#([^)]+)\)", src))
    missing = sorted(refs - set(ids))
    if missing:
        problems.append("%s: references undefined ids %s" % (name, missing[:5]))

    styles = " ".join(re.findall(r"<style>(.*?)</style>", src, re.S))
    used = {c for grp in re.findall(r'class="([^"]+)"', src) for c in grp.split()}
    undef = sorted(c for c in used if ("." + c) not in styles)
    if undef:
        problems.append("%s: classes with no rule %s" % (name, undef[:6]))

    if re.search(r"animation:[^;\"']*\b(both|backwards)\b", src):
        problems.append("%s: uses fill-mode both/backwards - content would be "
                        "invisible on the first painted frame" % name)

    if not re.search(r"viewBox=\"0 0 \d+ \d+\"", src):
        problems.append("%s: missing a viewBox, so it will not scale" % name)

    return problems


def main():
    problems, seen = [], 0
    for panel in PANELS:
        path = os.path.join(ROOT, panel + ".svg")
        if not os.path.exists(path):
            problems.append("%s.svg is missing" % panel)
            continue
        seen += 1
        problems += check(path)

    for path in sorted(glob.glob(os.path.join(ROOT, "*.svg"))):
        if os.path.splitext(os.path.basename(path))[0] not in PANELS:
            print("note: %s is not referenced by the README"
                  % os.path.basename(path))

    if problems:
        print("FAILED (%d problem%s)" % (len(problems), "" if len(problems) == 1 else "s"))
        for p in problems:
            print("  - " + p)
        return 1
    print("all %d panels OK" % seen)
    return 0


if __name__ == "__main__":
    sys.exit(main())
