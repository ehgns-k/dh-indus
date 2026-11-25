"""D7: combinatorial sparsity (CT27 density) across reference systems. Pre-registered in
docs/JOURNAL.md (twenty-sixth session). Output: results/batch7b_d7_sparsity.json"""
import collections, json, random
import numpy as np
from indus.corpus import ROOT, load_icit, load_kp1979
from indus.reference import load_reference, load_sproat

LONG2SHORT = {"144": "121", "145": "122", "147": "123", "150": "124", "151": "125"}
def normalise(s):
    s = [LONG2SHORT.get(t, t) for t in s]; out, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] == "121" and s[i + 1] == "121":
            out.append("122"); i += 2
        else:
            out.append(s[i]); i += 1
    return tuple(out)
def density(lines, rng):
    lines = lines[:]; rng.shuffle(lines); out = []; n = 0
    for s in lines:
        out.append(s); n += len(s)
        if n >= 9000: break
    c = collections.Counter(t for s in out for t in s); top = [t for t, _ in c.most_common(50)]
    seen = {(a, b) for s in out for a, b in zip(s, s[1:])}
    return sum((a, b) in seen for a in top for b in top) / 2500, n
uniq = lambda ls: [tuple(s) for s in sorted({tuple(x) for x in ls if len(x) > 0})]
C = {"icit": uniq(l.tokens for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens),
     "kp1979": uniq(normalise(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens)}
REF = load_reference()
for k, v in REF.items(): C[k] = uniq(v)
SP = load_sproat()
for k, v in SP.items():
    if sum(len(x) for x in uniq(v)) >= 9000: C["sproat_" + k] = uniq(v)
rng = random.Random(20261125)
D = {k: [] for k in C}; tokens = {}
for _ in range(20):
    for k in sorted(C):
        dv, n = density(C[k], rng); D[k].append(dv); tokens[k] = n
cdli = sorted(REF)
res = {"mean_density": {k: float(np.mean(v)) for k, v in D.items()}, "sd": {k: float(np.std(v)) for k, v in D.items()},
       "tokens_per_sample": tokens}
for ind in ("icit", "kp1979"):
    nearest = [min(cdli, key=lambda c: abs(D[c][r] - D[ind][r])) for r in range(20)]
    cnt = collections.Counter(nearest)
    res[f"nearest_{ind}"] = dict(cnt)
    res[f"pass_{ind}"] = cnt["proto_elamite"] + cnt["proto_cuneiform"] >= 19
res["verdict"] = "supported" if res["pass_icit"] and res["pass_kp1979"] else "not supported"
(ROOT / "results" / "batch7b_d7_sparsity.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
