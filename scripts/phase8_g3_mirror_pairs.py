"""G3 (claim C3): are mirror-image sign pairs used alike? Pre-registered in
docs/JOURNAL.md (twenty-first session)."""
import collections, json, pathlib
import numpy as np
from scipy.spatial.distance import jensenshannon
from scipy.stats import mannwhitneyu
from indus.corpus import ROOT, is_heldout, load_icit, strict_heldout

ns = {}
exec((pathlib.Path(__file__).with_name("phase8_g2_hog_robustness.py")).read_text().split("FRESH =")[0], ns)
img32 = ns["img32"]
GL = ROOT / "data" / "raw" / "glyphs" / "bmps"


def hog_of(im):
    gy, gx = np.gradient(im)
    mag = np.hypot(gx, gy); b = np.minimum(((np.arctan2(gy, gx) % np.pi) / np.pi * 9).astype(int), 8)
    f = np.zeros((4, 4, 9))
    for i in range(32):
        for j in range(32):
            f[i // 8, j // 8, b[i, j]] += mag[i, j]
    f = f.ravel(); return f / (np.linalg.norm(f) + 1e-12)


FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
lines = [l for l in load_icit() if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in lines})
ntr = collections.Counter(t for s in u if not is_heldout(list(s), "icit") for t in s)
data = set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in lines if l.meta["site"] in FRESH}
ctx = collections.defaultdict(collections.Counter)
for s in sorted(data):
    e = ["<s>"] + list(s) + ["</s>"]
    for i in range(1, len(e) - 1):
        ctx[e[i]]["L:" + e[i - 1]] += 1; ctx[e[i]]["R:" + e[i + 1]] += 1
signs = sorted(t for t in ntr if ntr[t] >= 10 and t != "?" and (GL / f"S{t}.bmp").exists() and sum(ctx[t].values()) > 0)
H = np.array([hog_of(img32(t)) for t in signs]); Hm = np.array([hog_of(img32(t)[:, ::-1]) for t in signs])
direct = H @ H.T; mirror = H @ Hm.T
keys = sorted({k for t in signs for k in ctx[t]})
P = np.array([[ctx[t][k] for k in keys] for t in signs], float); P /= P.sum(1, keepdims=True)
iu = np.triu_indices(len(signs), 1)
is_mirror = np.array([(mirror[i, j] >= 0.90 and mirror[i, j] - direct[i, j] >= 0.05) for i, j in zip(*iu)])
cs = np.array([1 - jensenshannon(P[i], P[j], base=2) for i, j in zip(*iu)])
pairs = [(signs[i], signs[j], round(float(mirror[i, j]), 3), round(float(direct[i, j]), 3), round(float(cs[k]), 3))
         for k, (i, j) in enumerate(zip(*iu)) if is_mirror[k]]
res = {"signs": len(signs), "mirror_pairs": pairs}
if len(pairs) < 5:
    res["status"] = "insufficient data"
else:
    U, p = mannwhitneyu(cs[is_mirror], cs[~is_mirror], alternative="greater")
    res.update(status="tested", median_ctx_mirror=float(np.median(cs[is_mirror])), median_ctx_other=float(np.median(cs[~is_mirror])), p_value=float(p))
(ROOT / "results" / "phase8_g3_mirror_pairs.json").write_text(json.dumps(res, indent=1))
print({k: v for k, v in res.items() if k != "mirror_pairs"}); print(pairs)
