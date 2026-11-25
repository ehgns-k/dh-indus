"""M1: does the more-marked member of a near-variant shape pair shift its
position consistently? Pre-registered in docs/JOURNAL.md (fifteenth session)."""
import collections, json, pathlib
import numpy as np
from PIL import Image
from scipy.stats import binomtest
from indus.corpus import ROOT, is_heldout, load_icit

GL = ROOT / "data" / "raw" / "glyphs" / "bmps"
ns = {}
src = pathlib.Path(__file__).with_name("phase8_g1_shape_usage.py").read_text()
exec(src.split("u = sorted(")[0], ns)
shape_vec = ns["shape_vec"]


def ink(sign):
    a = np.array(Image.open(GL / f"S{sign}.bmp").convert("L")) < 128
    if a.sum() == 0:
        a = ~a
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = max(h, w)
    sq = np.zeros((s, s), bool); sq[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = a
    return float((np.asarray(Image.fromarray((sq * 255).astype(np.uint8)).resize((32, 32), Image.BILINEAR)) > 127).sum())


u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
tr = [list(s) for s in u if not is_heldout(list(s), "icit")]
n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
for s in tr:
    for t in s: n[t] += 1
    if len(s) > 1: ini[s[0]] += 1; fin[s[-1]] += 1
signs = sorted(t for t in n if n[t] >= 10 and t != "?" and (GL / f"S{t}.bmp").exists())
V = {t: shape_vec(t) for t in signs}; I = {t: ink(t) for t in signs}
pairs = []
for i, a in enumerate(signs):
    for b in signs[i + 1:]:
        if float(V[a] @ V[b]) >= 0.807:
            ia, ib = I[a], I[b]
            if abs(ia - ib) / max(ia, ib) < 0.05:
                continue
            m, um = (a, b) if ia > ib else (b, a)
            pairs.append((m, um))
res = {"pairs": [list(p) for p in pairs], "n_pairs": len(pairs)}
for name, cnt in [("initial", ini), ("final", fin)]:
    d = [cnt[m] / n[m] - cnt[um] / n[um] for m, um in pairs]
    pos = sum(x > 0 for x in d); neg = sum(x < 0 for x in d)
    p = binomtest(pos, pos + neg, 0.5).pvalue if pos + neg else 1.0
    res[name] = {"marked_higher": pos, "marked_lower": neg, "ties": len(d) - pos - neg,
                 "mean_diff": float(np.mean(d)) if d else None, "p_value": float(p), "pass": bool(p < 0.005)}
(ROOT / "results" / "phase8_m1_marks.json").write_text(json.dumps(res, indent=1))
print(res["n_pairs"], res["initial"], res["final"])
print(pairs[:20])
