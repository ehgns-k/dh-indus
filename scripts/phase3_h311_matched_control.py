"""H3.11 (robustness check for H3.10, training split): compare the share of
next-sign = target after the 4-9 stroke signs with the same share after
random sign sets matched one-to-one for frequency (within a factor 1.5) and
medial share (within 0.15). 1,000 draws.
"""
import collections, json, random
import numpy as np
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

SETS = {"kp1979": (["124", "125", "126", "127", "128", "129"], {"86"}),
        "icit": (["004", "034", "005", "016", "017"], {"390", "405", "406", "407"})}
rng = random.Random(20261125)
res = {}
for name, (S, T) in SETS.items():
    L = load_icit() if name == "icit" else load_kp1979()
    u = sorted({tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"})
    tr = [s for s in u if not is_heldout(list(s), name)]
    n = collections.Counter(); med = collections.Counter()
    foll = collections.defaultdict(collections.Counter)
    for s in tr:
        for i, t in enumerate(s):
            n[t] += 1
            if 0 < i < len(s) - 1:
                med[t] += 1
            if i + 1 < len(s):
                foll[t][s[i + 1] in T] += 1
    def share(group):
        hit = sum(foll[g][True] for g in group); tot = sum(foll[g][True] + foll[g][False] for g in group)
        return hit / tot if tot else float("nan")
    S = [s for s in S if n[s] > 0]
    cands = {}
    for s in S:
        ms = med[s] / n[s]
        cands[s] = sorted(t for t in n if t not in S and t not in T and t != "?"
                          and n[s] / 1.5 <= n[t] <= n[s] * 1.5 and abs(med[t] / n[t] - ms) <= 0.15)
    obs = share(S)
    null = np.array([share([rng.choice(cands[s]) for s in S]) for _ in range(1000)])
    res[name] = {"observed_share": obs, "null_mean": float(np.nanmean(null)), "null_sd": float(np.nanstd(null)),
                 "null_max": float(np.nanmax(null)),
                 "p_value": float((np.sum(null >= obs) + 1) / 1001),
                 "candidates_per_sign": {s: len(c) for s, c in cands.items()}}
(ROOT / "results" / "phase3_h311_matched_control.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
