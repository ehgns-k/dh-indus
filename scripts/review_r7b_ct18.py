"""R7b: copy of scripts/claims_ct18_recursive.py with 10,000 control draws (generated; pre-registered in docs/JOURNAL.md, twenty-fourth session). CT18 (claim C18): parts produced by recursive splitting at the weakest PMI
link recur as complete texts. Pre-registered in docs/JOURNAL.md."""
import collections, json, math, random
import numpy as np
from indus.controls import control
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979, strict_heldout

res = {}
for name, f in [("icit", load_icit), ("kp1979", load_kp1979)]:
    u = sorted({tuple(l.tokens) for l in f() if l.complete and l.direction != "unknown" and "?" not in l.tokens})
    tr = [s for s in u if not is_heldout(list(s), name)]
    complete = set(tr)
    uni = collections.Counter(t for s in tr for t in s); big = collections.Counter(p for s in tr for p in zip(s, s[1:]))
    N1 = sum(uni.values()); N2 = sum(big.values()); V = len(uni)
    def pmi(a, b):
        return math.log((big[(a, b)] + 0.5) / (N2 + 0.5 * V * V)) - math.log((uni[a] + 0.5) / (N1 + 0.5 * V)) - math.log((uni[b] + 0.5) / (N1 + 0.5 * V))
    def parts(s):
        out = []
        def rec(x):
            if len(x) in (2, 3):
                out.append(tuple(x))
            if len(x) >= 3:
                k = min(range(len(x) - 1), key=lambda i: (pmi(x[i], x[i + 1]), i))
                rec(x[:k + 1]); rec(x[k + 1:])
        rec(list(s)); return out
    def share(lines):
        ps = [p for s in lines for p in parts(s)]
        return sum(p in complete for p in ps) / len(ps) if ps else float("nan")
    test = [list(s) for s in sorted(strict_heldout(u, name)) if len(s) >= 4]
    obs = share(test); rng = random.Random(20261125)
    null = np.array([share([control(s, name, rng) for s in test]) for _ in range(10000)])
    p = float((np.sum(null >= obs) + 1) / 10001)
    res[name] = {"lines": len(test), "share_real": obs, "control_mean": float(null.mean()), "control_sd": float(null.std()),
                 "p_value": p, "pass": bool(p < 0.01)}
    print(name, res[name])
(ROOT / "results" / "review_r7b_ct18.json").write_text(json.dumps(res, indent=1))
