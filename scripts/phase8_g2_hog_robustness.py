"""G2 robustness (not pre-registered): repeat G2 with a shape measure based on
histograms of edge orientation (HOG-like; 4 x 4 cells of a 32 x 32 image,
9 orientation bins), which reflects internal structure rather than mainly the
outline and aspect ratio. Close-shape pairs = top 5 % by this measure.
Usage measured on strict held-out + fresh data, as in G2."""
import collections, json, pathlib
import numpy as np
from PIL import Image
from scipy.spatial.distance import jensenshannon
from scipy.stats import mannwhitneyu
from indus.corpus import ROOT, load_icit, strict_heldout

GL = ROOT / "data" / "raw" / "glyphs" / "bmps"


def img32(sign):
    a = np.array(Image.open(GL / f"S{sign}.bmp").convert("L")) < 128
    if a.sum() == 0:
        a = ~a
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = max(h, w)
    sq = np.zeros((s, s), bool); sq[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = a
    return np.asarray(Image.fromarray((sq * 255).astype(np.uint8)).resize((32, 32), Image.BILINEAR), float) / 255


def hog(sign):
    im = img32(sign)
    gy, gx = np.gradient(im)
    mag = np.hypot(gx, gy); ang = (np.arctan2(gy, gx) % np.pi) / np.pi * 9
    b = np.minimum(ang.astype(int), 8)
    f = np.zeros((4, 4, 9))
    for i in range(32):
        for j in range(32):
            f[i // 8, j // 8, b[i, j]] += mag[i, j]
    f = f.ravel()
    return f / (np.linalg.norm(f) + 1e-12)


FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
lines = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in lines})
data = set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in lines if l.meta["site"] in FRESH}
ctx = collections.defaultdict(collections.Counter); n = collections.Counter()
for s in sorted(data):
    e = ["<s>"] + list(s) + ["</s>"]
    for i in range(1, len(e) - 1):
        n[e[i]] += 1; ctx[e[i]]["L:" + e[i - 1]] += 1; ctx[e[i]]["R:" + e[i + 1]] += 1
signs = sorted(t for t in n if n[t] >= 5 and t != "?" and (GL / f"S{t}.bmp").exists())
H = np.array([hog(t) for t in signs]); sim = H @ H.T
keys = sorted({k for t in signs for k in ctx[t]})
P = np.array([[ctx[t][k] for k in keys] for t in signs], float); P /= P.sum(1, keepdims=True)
iu = np.triu_indices(len(signs), 1)
cs = np.array([1 - jensenshannon(P[i], P[j], base=2) for i, j in zip(*iu)]); ss = sim[iu]
close = ss >= np.quantile(ss, 0.95)
U, p = mannwhitneyu(cs[close], cs[~close], alternative="greater")
top = sorted([(signs[i], signs[j], round(float(ss[k]), 3), round(float(cs[k]), 3)) for k, (i, j) in enumerate(zip(*iu)) if close[k]],
             key=lambda x: -x[2])[:30]
res = {"signs": len(signs), "close_pairs": int(close.sum()), "median_ctx_close": float(np.median(cs[close])),
       "median_ctx_other": float(np.median(cs[~close])), "p_value": float(p), "top_shape_pairs": top}
(ROOT / "results" / "phase8_g2_hog_robustness.json").write_text(json.dumps(res, indent=1))
print({k: v for k, v in res.items() if k != "top_shape_pairs"}); print(top[:20])
