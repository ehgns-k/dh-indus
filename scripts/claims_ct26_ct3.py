"""CT26 (structure of the 'trader' sequence) and CT3 (six secure mirror pairs).
Pre-registered in docs/JOURNAL.md (twenty-first session)."""
import collections, json, math, random
import numpy as np
from scipy.spatial.distance import jensenshannon
from indus.corpus import ROOT, load_icit, load_kp1979

res = {}
SEQ = {"icit": (["255"], ["435", "436"], ["690"], ["740"]), "kp1979": (["73"], ["188"], ["255"], ["324", "325"])}
for name, f in [("icit", load_icit), ("kp1979", load_kp1979)]:
    u = sorted({tuple(l.tokens) for l in f() if l.complete and l.direction != "unknown"})
    A, B, C, D = (set(x) for x in SEQ[name])
    norm = lambda t: "B" if t in B else t
    us = [tuple(norm(t) for t in s) for s in u]
    a, b, c, d = next(iter(A)), "B", next(iter(C)), None
    uni = collections.Counter(t for s in us for t in s); big = collections.Counter(p for s in us for p in zip(s, s[1:]))
    N1, N2, V = sum(uni.values()), sum(big.values()), len(uni)
    def pmi(x, y):
        return math.log((big[(x, y)] + 0.5) / (N2 + 0.5 * V * V)) - math.log((uni[x] + 0.5) / (N1 + 0.5 * V)) - math.log((uni[y] + 0.5) / (N1 + 0.5 * V))
    pmi_ab, pmi_bc = pmi(a, b), pmi(b, c)
    pmi_cd = max(pmi(c, x) for x in D)
    ab_alone = cd_alone = bc_alone = 0
    for s in us:
        for i in range(len(s) - 1):
            if s[i] == a and s[i + 1] == b and not (i + 3 < len(s) and s[i + 2] == c and s[i + 3] in D):
                ab_alone += 1
            if s[i] == c and s[i + 1] in D and not (i >= 2 and s[i - 2] == a and s[i - 1] == b):
                cd_alone += 1
            if s[i] == b and s[i + 1] == c and not (i >= 1 and s[i - 1] == a) and not (i + 2 < len(s) and s[i + 2] in D):
                bc_alone += 1
    a1 = pmi_bc < pmi_ab and pmi_bc < pmi_cd
    a2 = ab_alone >= 3 and cd_alone >= 3 and bc_alone < min(ab_alone, cd_alone)
    res[f"CT26|{name}"] = {"pmi_AB": pmi_ab, "pmi_BC": pmi_bc, "pmi_CD": pmi_cd, "AB_without_CD": ab_alone,
                           "CD_without_AB": cd_alone, "BC_alone": bc_alone, "a1": bool(a1), "a2": bool(a2)}
res["CT26_supported"] = all(res[f"CT26|{n}"]["a1"] and res[f"CT26|{n}"]["a2"] for n in SEQ)

# CT3
u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
occ = collections.defaultdict(list)
for s in u:
    e = ["<s>"] + list(s) + ["</s>"]
    for i in range(1, len(e) - 1):
        occ[e[i]].append(("L:" + e[i - 1], "R:" + e[i + 1]))
def js(oa, ob):
    ca = collections.Counter(x for o in oa for x in o); cb = collections.Counter(x for o in ob for x in o)
    keys = sorted(set(ca) | set(cb))
    pa = np.array([ca[k] for k in keys], float); pb = np.array([cb[k] for k in keys], float)
    return float(jensenshannon(pa / pa.sum(), pb / pb.sum(), base=2))
rng = random.Random(20261125); thr = 0.01 / 6
for m, o in [("436", "435"), ("402", "400"), ("551", "550"), ("622", "621"), ("526", "527"), ("126", "125")]:
    om, oo = occ[m], occ[o]
    if not om or not oo:
        res[f"CT3|{m}/{o}"] = {"status": "missing"}; continue
    obs = js(om, oo); pool = om + oo; null = []
    for _ in range(10000):
        rng.shuffle(pool); null.append(js(pool[:len(om)], pool[len(om):]))
    p = (sum(x >= obs for x in null) + 1) / 10001
    res[f"CT3|{m}/{o}"] = {"n_mirror": len(om), "n_original": len(oo), "js": obs, "null_mean": float(np.mean(null)),
                           "p_value": p, "distinct": bool(p < thr)}
res["CT3_threshold"] = thr
(ROOT / "results" / "claims_ct26_ct3.json").write_text(json.dumps(res, indent=1))
for k, v in res.items(): print(k, v)
