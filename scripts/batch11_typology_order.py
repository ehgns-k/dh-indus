"""D8 (order rigidity), D9 (positional rigidity), D10 (rank-frequency slope).
Pre-registered in docs/JOURNAL.md (thirtieth session). Output: results/batch11_typology_order.json"""
import collections, json, math, random
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
uniq = lambda ls: [tuple(s) for s in sorted({tuple(x) for x in ls if len(x) > 0})]
C = {"icit": uniq(l.tokens for l in load_icit() if l.complete and l.direction != "unknown" and "?" not in l.tokens),
     "kp1979": uniq(normalise(l.tokens) for l in load_kp1979() if l.complete and "?" not in l.tokens)}
REF = load_reference()
for k, v in REF.items(): C[k] = uniq(v)
for k, v in load_sproat().items():
    if sum(len(x) for x in uniq(v)) >= 9000: C["sproat_" + k] = uniq(v)

def sample(lines, rng):
    lines = lines[:]; rng.shuffle(lines); out = []; n = 0
    for s in lines:
        out.append(s); n += len(s)
        if n >= 9000: break
    return out
def d8(sm):
    c = collections.Counter((a, b) for s in sm for a, b in zip(s, s[1:]) if a != b)
    fr = [p for p, v in c.items() if v >= 3]
    return sum(1 for a, b in fr if c[(b, a)] == 0) / len(fr) if fr else float("nan")
def d9(sm):
    pos = collections.defaultdict(collections.Counter)
    for s in sm:
        if len(s) >= 3:
            for i, t in enumerate(s):
                pos[t]["I" if i == 0 else "F" if i == len(s) - 1 else "M"] += 1
    f = collections.Counter(t for s in sm for t in s)
    top = [t for t, _ in f.most_common(50) if sum(pos[t].values()) > 0]
    return float(np.mean([max(pos[t].values()) / sum(pos[t].values()) for t in top]))
def d10(sm):
    f = sorted(collections.Counter(t for s in sm for t in s).values(), reverse=True)[:50]
    x = np.log(np.arange(1, len(f) + 1)); y = np.log(f)
    return float(np.polyfit(x, y, 1)[0])
rng = random.Random(20261125); V = {m: {k: [] for k in C} for m in ("D8", "D9", "D10")}
for _ in range(20):
    for k in sorted(C):
        sm = sample(C[k], rng)
        V["D8"][k].append(d8(sm)); V["D9"][k].append(d9(sm)); V["D10"][k].append(d10(sm))
FULL = ["sumerian_ur3_admin", "sumerian_ob_literary", "akkadian_ob_letters"]
res = {}
for m in ("D8", "D9"):
    r = {"mean": {k: float(np.mean(v)) for k, v in V[m].items()}, "sd": {k: float(np.std(v)) for k, v in V[m].items()}}
    for ind in ("icit", "kp1979"):
        r[f"higher_than_all_full_writing_{ind}"] = int(sum(all(V[m][ind][i] > V[m][f][i] for f in FULL) for i in range(20)))
    r["verdict"] = "supported" if min(r["higher_than_all_full_writing_icit"], r["higher_than_all_full_writing_kp1979"]) >= 19 else "not supported"
    res[m] = r
r = {"mean": {k: float(np.mean(v)) for k, v in V["D10"].items()}, "sd": {k: float(np.std(v)) for k, v in V["D10"].items()}}
lo = min(r["mean"][p] - 2 * r["sd"][p] for p in ("proto_elamite", "proto_cuneiform"))
hi = max(r["mean"][p] + 2 * r["sd"][p] for p in ("proto_elamite", "proto_cuneiform"))
r["proto_range"] = [lo, hi]
r["decision"] = "like the proto-administrative corpora" if all(lo <= r["mean"][i] <= hi for i in ("icit", "kp1979")) else "not like the proto-administrative corpora"
res["D10"] = r
(ROOT / "results" / "batch11_typology_order.json").write_text(json.dumps(res, indent=1))
for m, r in res.items():
    print(m, {k: round(v, 3) for k, v in r["mean"].items()}, {k: v for k, v in r.items() if k not in ("mean", "sd")})
