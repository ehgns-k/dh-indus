"""DIR2: unknown-direction lines follow the normalised order. Pre-registered in docs/JOURNAL.md
(twenty-seventh session). Output: results/batch8b_dir2_unknown.json"""
import collections, json, math
from scipy.stats import binomtest
from indus.corpus import ROOT, load_icit

L = [l for l in load_icit() if l.complete and "?" not in l.tokens and l.tokens]
V = len({t for l in L for t in l.tokens}) + 2
unk = sorted({tuple(l.tokens) for l in L if l.direction == "unknown" and len(l.tokens) >= 2})
known = sorted({tuple(l.tokens) for l in L if l.direction != "unknown"} - set(unk))
c = collections.defaultdict(collections.Counter)
for s in known:
    e = ["<s>"] + list(s) + ["</s>"]
    for x, y in zip(e, e[1:]):
        c[x][y] += 1
n = {x: sum(v.values()) for x, v in c.items()}
loss = lambda s: -sum(math.log((c[x][y] + 0.1) / (n.get(x, 0) + 0.1 * V)) for x, y in zip(["<s>"] + list(s), list(s) + ["</s>"])) / (len(s) + 1)
w = sum(loss(s) < loss(s[::-1]) for s in unk); ties = sum(loss(s) == loss(s[::-1]) for s in unk)
p = binomtest(w, len(unk) - ties, 0.5, alternative="greater").pvalue
types = collections.Counter(l.meta["type"] for l in L if l.direction == "unknown")
res = {"strings": len(unk), "forward_wins": w, "ties": ties, "p": p, "types": dict(types.most_common(8)),
       "verdict": "supported" if p < 0.01 else "not supported"}
(ROOT / "results" / "batch8b_dir2_unknown.json").write_text(json.dumps(res, indent=1))
print(res)
