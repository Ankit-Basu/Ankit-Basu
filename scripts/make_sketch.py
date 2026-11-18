"""
Trace profile.jpg into the line drawing the hero portrait draws itself with.

    pip install opencv-python-headless numpy
    python scripts/make_sketch.py

Pipeline: GrabCut separates the subject from the garden behind it, the mask's
outline becomes the silhouette, and Canny edges *inside* the mask become the
features (glasses, ear, eyes, beard line, jacket seams). Every edge is walked
into a single-pass polyline, simplified, smoothed into cubic Beziers and
written to data/sketch.json in a 0..1000 box that lines up exactly with the
portrait crop in data/avatar.txt (both use CROP below).

Like make_avatar.py this is an offline step: the JSON is committed, so the
daily build needs neither OpenCV nor the photo.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "profile.jpg")
OUT = os.path.join(ROOT, "data", "sketch.json")

CROP = (320, 0, 760, 440)   # keep in step with make_avatar.CROP
WORK = 840                  # working resolution for edge detection
MIN_LEN = 22                # drop edge fragments shorter than this (px @ WORK)
MAX_PATHS = 170
BUCKETS = 12                # drawing waves; build.py staggers one keyframe per wave


def walk(contour, seen):
    """findContours walks both sides of a 1px line. Keep each pixel once,
    splitting wherever the walk doubles back over pixels already used."""
    runs, cur = [], []
    for p in contour[:, 0, :]:
        key = (int(p[0]), int(p[1]))
        if key in seen:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        seen.add(key)
        cur.append(key)
    if len(cur) > 1:
        runs.append(cur)
    return runs


def plen(pts):
    import math
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def to_path(pts, s):
    """Catmull-Rom through the simplified points -> cubic Bezier path."""
    P = [(x * s, y * s) for x, y in pts]
    if len(P) == 2:
        return "M%.0f %.0fL%.0f %.0f" % (P[0] + P[1])
    d = ["M%.0f %.0f" % P[0]]
    for i in range(len(P) - 1):
        p0 = P[i - 1] if i else P[i]
        p1, p2 = P[i], P[i + 1]
        p3 = P[i + 2] if i + 2 < len(P) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append("C%.0f %.0f %.0f %.0f %.0f %.0f" % (c1 + c2 + p2))
    return "".join(d)


def main():
    try:
        import cv2
        import numpy as np
    except Exception as e:
        print("needs opencv-python-headless and numpy (%s)" % e, file=sys.stderr)
        return 1

    im = cv2.imread(SRC)
    x0, y0, x1, y1 = CROP
    c = cv2.resize(im[y0:y1, x0:x1], (WORK, WORK), interpolation=cv2.INTER_CUBIC)

    # -- subject mask
    mask = np.zeros(c.shape[:2], np.uint8)
    bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(c, mask, (40, 1, WORK - 60, WORK - 2), bg, fg, 8, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    m = (cv2.GaussianBlur(m, (0, 0), 7) > 127).astype(np.uint8) * 255

    # -- edges
    g = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    g = cv2.createCLAHE(2.5, (8, 8)).apply(g)
    g = cv2.GaussianBlur(g, (0, 0), 2.0)
    e = cv2.Canny(g, 16, 46)
    e = cv2.bitwise_and(e, cv2.erode(m, np.ones((13, 13), np.uint8)))
    sil = cv2.Canny(m, 50, 150)

    s = 1000.0 / WORK
    paths = []
    for layer, img in (("sil", sil), ("feat", e)):
        seen = set()
        cs, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for cnt in cs:
            for run in walk(cnt, seen):
                arr = np.array(run, np.int32).reshape(-1, 1, 2)
                L = cv2.arcLength(arr, False)
                if L < (MIN_LEN if layer == "feat" else 60):
                    continue
                simp = cv2.approxPolyDP(arr, 1.6, False)[:, 0, :].tolist()
                cy = sum(p[1] for p in run) / len(run)
                paths.append(dict(layer=layer, d=to_path(simp, s), len=L, y=cy))

    sil_p = [p for p in paths if p["layer"] == "sil"]
    feat = sorted((p for p in paths if p["layer"] == "feat"), key=lambda p: -p["len"])
    feat = feat[:MAX_PATHS - len(sil_p)]
    # silhouette first, then features top-to-bottom, long strokes before short
    feat.sort(key=lambda p: p["y"])
    ordered = sil_p + feat
    for i, p in enumerate(ordered):
        p["w"] = 0 if p["layer"] == "sil" else 1 + int((i - len(sil_p)) * (BUCKETS - 1) / max(1, len(feat)))
    out = [{"d": p["d"], "w": p["w"], "k": p["layer"]} for p in ordered]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"box": 1000, "crop": CROP, "waves": BUCKETS, "paths": out}, f, separators=(",", ":"))

    preview = np.full((WORK, WORK), 255, np.uint8)
    preview[cv2.bitwise_or(e, sil) > 0] = 0
    cv2.imwrite(os.path.join(ROOT, "data", "_sketch_preview.png"), preview)
    print("wrote %s: %d paths, %.1f KB" % (OUT, len(out), os.path.getsize(OUT) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
