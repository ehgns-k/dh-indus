"""L3a robustness check (10,000 relabellings; not the pre-registered count). L3a: are ICIT signs that KP1979 merges contextually distinct? Training split.
Pre-registered in docs/JOURNAL.md (fourteenth working session)."""
import collections, csv, itertools, json, random
import numpy as np
from scipy.spatial.distance import jensenshannon
from indus.corpus import ROOT, is_heldout, load_icit

rows = [r for r in csv.DictReader(open(ROOT / "results" / "phase1_concordance.tsv"), delimiter="\t")
        if int(r["support"]) >= 3 and float(r["purity"]) >= 0.8]
u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
tr = [list(s) for s in u if not is_heldout(list(s), "icit")]
occ = collections.defaultdict(list)  # sign -> list of (prev, next) contexts
for s in tr:
    e = ["<s>"] + s + ["</s>"]
    for i in range(1, len(e) - 1):
        occ[e[i]].append(("L:" + e[i - 1], "R:" + e[i + 1]))
groups = collections.defaultdict(list)
for r in rows:
    if len(occ[r["icit_sign"]]) >= 15:
        groups[r["kp1979_sign"]].append(r["icit_sign"])
groups = {k: sorted(v) for k, v in groups.items() if len(v) >= 2}
pairs = [(k, a, b) for k, v in sorted(groups.items()) for a, b in itertools.combinations(v, 2)]

def js(oa, ob):
    ca = collections.Counter(x for o in oa for x in o); cb = collections.Counter(x for o in ob for x in o)
    keys = sorted(set(ca) | set(cb))
    pa = np.array([ca[k] for k in keys], float); pb = np.array([cb[k] for k in keys], float)
    return float(jensenshannon(pa / pa.sum(), pb / pb.sum(), base=2))

rng = random.Random(20261125)
thr = 0.01 / max(1, len(pairs))
res = []
for k, a, b in pairs:
    oa, ob = occ[a], occ[b]
    obs = js(oa, ob)
    pool = oa + ob; null = []
    for _ in range(10000):
        rng.shuffle(pool); null.append(js(pool[:len(oa)], pool[len(oa):]))
    p = (sum(x >= obs for x in null) + 1) / 10001
    fin = lambda o: sum(x[1] == "R:</s>" for x in o) / len(o)
    res.append({"kp": k, "a": a, "b": b, "n_a": len(oa), "n_b": len(ob), "js": obs, "null_mean": float(np.mean(null)),
                "p": p, "distinct": bool(p < thr), "final_share_a": round(fin(oa), 2), "final_share_b": round(fin(ob), 2)})
out = {"groups": groups, "n_pairs": len(pairs), "threshold": thr, "pairs": res}
(ROOT / "results" / "phase3_l3a_allographs_10k.json").write_text(json.dumps(out, indent=1))
print("groups", groups, "pairs", len(pairs), "thr", thr)
for r in res:
    print(r["kp"], r["a"], r["b"], r["n_a"], r["n_b"], round(r["js"], 3), round(r["null_mean"], 3), r["p"], "DISTINCT" if r["distinct"] else "", r["final_share_a"], r["final_share_b"])
