"""CT22k, F5k, FACE4k, FACE5, NUM3. Pre-registered in docs/JOURNAL.md (twenty-sixth session).
Output: results/batch7_kp_replications.json"""
import collections, csv, itertools, json, random
import numpy as np
from scipy.spatial.distance import jensenshannon
from indus.corpus import ROOT, load_icit, load_kp1979, is_heldout, strict_heldout
from indus.controls import control

LONG2SHORT = {"144": "121", "145": "122", "147": "123", "150": "124", "151": "125"}


def norm(s):
    s = [LONG2SHORT.get(t, t) for t in s]
    out, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] == "121" and s[i + 1] == "121":
            out.append("122"); i += 2
        else:
            out.append(s[i]); i += 1
    return tuple(out)


FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
ok = lambda l: l.complete and "?" not in l.tokens and len(l.tokens) > 0
res = {}
kp = load_kp1979()
kp_raw = sorted({tuple(l.tokens) for l in kp if l.complete})
kp_strict = sorted({norm(s) for s in strict_heldout(kp_raw, "kp1979") if "?" not in s})

# ---- CT22k
FISH = ["53", "56", "57", "58", "60", "61", "62", "63"]
ctx = collections.defaultdict(collections.Counter); n = collections.Counter()
for s in kp_strict:
    e = ["<s>"] + list(s) + ["</s>"]
    for i in range(1, len(e) - 1):
        n[e[i]] += 1; ctx[e[i]]["L:" + e[i - 1]] += 1; ctx[e[i]]["R:" + e[i + 1]] += 1
pool = sorted(t for t in n if n[t] >= 5)
keys = sorted({k for t in pool for k in ctx[t]})
P = {t: np.array([ctx[t][k] for k in keys], float) / sum(ctx[t].values()) for t in pool}
msim = lambda g: float(np.mean([1 - jensenshannon(P[a], P[b], base=2) for a, b in itertools.combinations(g, 2)]))
fish = [t for t in FISH if t in P]
if len(fish) >= 3:
    obs = msim(fish); others = [t for t in pool if t not in FISH]
    cands = {f: [t for t in others if n[f] / 1.5 <= n[t] <= n[f] * 1.5] or others for f in fish}
    rng = random.Random(20261125); null = []
    for _ in range(10000):
        g = []
        for f in fish:
            c = [t for t in cands[f] if t not in g] or [t for t in others if t not in g]
            g.append(rng.choice(c))
        null.append(msim(g))
    null = np.array(null); p = float((np.sum(null >= obs) + 1) / 10001)
    res["CT22k"] = {"strings": len(kp_strict), "fish_used": fish, "counts": {f: n[f] for f in fish}, "mean_similarity": obs,
                    "null_mean": float(null.mean()), "null_sd": float(null.std()), "p_value": p,
                    "verdict": "supported" if p < 0.01 else "not supported"}
else:
    res["CT22k"] = {"fish_used": fish, "verdict": "insufficient data"}

# ---- F5k
conc = {}
with open(ROOT / "results" / "phase1_concordance.tsv") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        conc[r["icit_sign"]] = r["kp1979_sign"]
train = sorted({norm(s) for s in kp_raw if "?" not in s and not is_heldout(list(s), "kp1979")})
by_key = collections.defaultdict(set)
for s in train:
    for i in range(len(s)):
        by_key[(s[:i], s[i + 1:])].add(s[i])
T = {k for k, v in by_key.items() if len(v) >= 3 and len(k[0]) + len(k[1]) + 1 >= 3}
match = lambda s: any((s[:i], s[i + 1:]) in T for i in range(len(s)))
def mapped(s):
    try:
        return norm([conc[t] for t in s])
    except KeyError:
        return None
icit = load_icit()
fresh = sorted({tuple(l.tokens) for l in icit if l.complete and l.direction != "unknown" and "?" not in l.tokens
                and l.meta["site"] in FRESH and len(l.tokens) >= 3})
fresh = [s for s in fresh if mapped(s) is not None]
obs = sum(match(mapped(s)) for s in fresh)
rng = random.Random(20261125); null = []
for _ in range(10000):
    null.append(sum(match(mapped(control(list(s), "icit", rng))) for s in fresh))
p = (sum(x >= obs for x in null) + 1) / 10001
res["F5k"] = {"kp_train_strings": len(train), "templates": len(T), "fresh_mapped": len(fresh), "matching_real": obs,
              "matching_control_mean": sum(null) / len(null), "p_value": p,
              "matched": [" ".join(s) for s in fresh if match(mapped(s))],
              "verdict": "insufficient data" if obs < 5 else ("supported" if p < 0.01 else "not supported")}

# ---- FACE4k
TERM = {"324", "325", "98", "217", "326", "1", "13", "4", "301"}
byk = collections.defaultdict(list)
for l in kp:
    byk[l.object_id].append(l)
multi = [sorted(v, key=lambda x: x.line_no) for o, v in sorted(byk.items()) if len(v) >= 3 and all(ok(x) for x in v)]
flags = [[x.tokens[-1] in TERM for x in m] for m in multi]
obs = sum(sum(f) == 1 for f in flags); pool_f = [x for f in flags for x in f]
rng = random.Random(20261125); null = []
for _ in range(10000):
    q = pool_f[:]; rng.shuffle(q); i = 0; c1 = 0
    for f in flags:
        c1 += sum(q[i:i + len(f)]) == 1; i += len(f)
    null.append(c1)
p = (sum(x >= obs for x in null) + 1) / 10001
res["FACE4k"] = {"objects": len(multi), "records_per_object": dict(collections.Counter(len(m) for m in multi)),
                 "lines_codes": dict(collections.Counter(m[0].meta["lines_code"] for m in multi)),
                 "closing_records_per_object": dict(collections.Counter(sum(f) for f in flags)),
                 "exactly_one": obs, "null_mean": sum(null) / len(null), "p_value": p,
                 "verdict": "insufficient data" if len(multi) < 20 else ("supported" if p < 0.01 else "not supported")}

# ---- FACE5 and NUM3
NUMV = {"032": 2, "033": 3, "034": 4}
STROKE = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
faces = collections.defaultdict(lambda: collections.defaultdict(list))
for l in icit:
    faces[l.object_id.split(".")[0]][l.object_id].append(l)
units = collections.defaultdict(lambda: {"types": set(), "counts": collections.Counter()})
pre700 = collections.Counter(); single = 0
for o in sorted(faces):
    fs = faces[o]
    if len(fs) == 1:
        for v in fs.values():
            for x in v:
                if ok(x):
                    t = x.tokens
                    for i in range(1, len(t)):
                        if t[i] == "700":
                            pre700[t[i - 1]] += 1
        continue
    if len(fs) != 2 or not all(len(v) == 1 and ok(v[0]) for v in fs.values()):
        continue
    a, b = [fs[k][0] for k in sorted(fs)]
    isn = lambda f: len(f) >= 2 and f[-1] == "700" and all(x in STROKE for x in f[:-1])
    if isn(a.tokens) != isn(b.tokens):
        num, txt = (a, b) if isn(a.tokens) else (b, a)
        if a.meta["type"] in ("TAB:B", "TAB:I") and len(num.tokens) == 2 and num.tokens[0] in NUMV:
            u = units[tuple(txt.tokens)]
            u["types"].add(a.meta["type"]); u["counts"][NUMV[num.tokens[0]]] += 1
rows = []
for t, u in sorted(units.items()):
    if len(u["types"]) != 1:
        continue
    mc = u["counts"].most_common()
    if len(mc) > 1 and mc[0][1] == mc[1][1]:
        continue
    rows.append((next(iter(u["types"])), mc[0][0]))
def chi2(rs):
    tab = collections.Counter(rs); ty = ["TAB:B", "TAB:I"]; cs = [2, 3, 4]
    N = len(rs); x = 0.0
    for a in ty:
        ra = sum(tab[(a, c)] for c in cs)
        for c in cs:
            cc = sum(tab[(b, c)] for b in ty); e = ra * cc / N
            if e > 0:
                x += (tab[(a, c)] - e) ** 2 / e
    return x
types = [r[0] for r in rows]; cnts = [r[1] for r in rows]
obs = chi2(rows); rng = random.Random(20261125); null = []
for _ in range(10000):
    tt = types[:]; rng.shuffle(tt); null.append(chi2(list(zip(tt, cnts))))
p = (sum(x >= obs for x in null) + 1) / 10001
nB = types.count("TAB:B"); nI = types.count("TAB:I")
res["FACE5"] = {"units": len(rows), "TAB:B": nB, "TAB:I": nI,
                "table": {f"{a}|{c}": collections.Counter(rows)[(a, c)] for a in ("TAB:B", "TAB:I") for c in (2, 3, 4)},
                "chi2": obs, "p_value": p,
                "verdict": "insufficient data" if min(nB, nI) < 10 else ("supported" if p < 0.01 else "not supported")}
res["NUM3"] = {"signs_before_700_in_one_face_texts": dict(pre700.most_common(15)),
               "stroke_counts_before_700": {k: v for k, v in pre700.items() if k in STROKE}}
(ROOT / "results" / "batch7_kp_replications.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, json.dumps(v, default=float)[:700])
