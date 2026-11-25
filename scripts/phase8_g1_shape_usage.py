"""G1: correlation between glyph-shape similarity and context similarity
(Mantel test). Pre-registered in docs/JOURNAL.md (fourteenth session)."""
import collections, json, random
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.spatial.distance import jensenshannon
from scipy.stats import spearmanr
from indus.corpus import ROOT, is_heldout, load_icit

GL = ROOT / "data" / "raw" / "glyphs" / "bmps"


def shape_vec(sign):
    p = GL / f"S{sign}.bmp"
    if not p.exists():
        return None
    a = np.array(Image.open(p).convert("L")) < 128  # ink = True
    if a.sum() == 0:
        a = ~a
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = max(h, w)
    sq = np.zeros((s, s), bool); sq[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = a
    im = Image.fromarray((sq * 255).astype(np.uint8)).resize((32, 32), Image.BILINEAR)
    v = gaussian_filter(np.asarray(im, float) / 255, 1.5).ravel()
    return v / (np.linalg.norm(v) + 1e-12)


u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
tr = [list(s) for s in u if not is_heldout(list(s), "icit")]
ctx = collections.defaultdict(collections.Counter); n = collections.Counter()
for s in tr:
    e = ["<s>"] + s + ["</s>"]
    for i in range(1, len(e) - 1):
        n[e[i]] += 1; ctx[e[i]]["L:" + e[i - 1]] += 1; ctx[e[i]]["R:" + e[i + 1]] += 1
signs = sorted(t for t in n if n[t] >= 15 and t != "?" and shape_vec(t) is not None)
S = np.array([shape_vec(t) for t in signs]); shape_sim = S @ S.T
keys = sorted({k for t in signs for k in ctx[t]})
P = np.array([[ctx[t][k] for k in keys] for t in signs], float); P /= P.sum(1, keepdims=True)
m = len(signs); ctx_sim = np.ones((m, m))
for i in range(m):
    for j in range(i + 1, m):
        ctx_sim[i, j] = ctx_sim[j, i] = 1 - jensenshannon(P[i], P[j], base=2)
iu = np.triu_indices(m, 1)
obs = spearmanr(shape_sim[iu], ctx_sim[iu]).correlation
rng = np.random.default_rng(20261125); null = []
for _ in range(10000):
    perm = rng.permutation(m)
    null.append(spearmanr(shape_sim[iu], ctx_sim[perm][:, perm][iu]).correlation)
null = np.array(null)
p = float((np.sum(null >= obs) + 1) / 10001)
both = sorted(((shape_sim[i, j] + ctx_sim[i, j], signs[i], signs[j], round(float(shape_sim[i, j]), 3), round(float(ctx_sim[i, j]), 3))
               for i, j in zip(*iu)), reverse=True)[:25]
res = {"signs": len(signs), "spearman": float(obs), "null_mean": float(null.mean()), "null_sd": float(null.std()),
       "p_value": p, "top_pairs_shape_plus_context": [b[1:] for b in both]}
(ROOT / "results" / "phase8_g1_shape_usage.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "top_pairs_shape_plus_context"}, indent=1))
for b in both[:25]: print(b[1:])
