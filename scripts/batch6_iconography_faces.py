"""MO2a, MO2b, MO1k, CT15r, FACE4. Pre-registered in docs/JOURNAL.md (twenty-fifth session).
Output: results/batch6_iconography_faces.json"""
import collections, importlib.util, json, pathlib, random, sys
import pandas as pd
from scipy.stats import fisher_exact
from indus.corpus import ROOT, load_icit, load_kp1979, is_heldout, strict_heldout

spec = importlib.util.spec_from_file_location("c2", pathlib.Path(__file__).with_name("phase6_c2_association_scan.py"))
c2 = importlib.util.module_from_spec(spec); sys.modules["c2"] = c2; spec.loader.exec_module(c2)
FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
ok = lambda l: l.complete and "?" not in l.tokens and len(l.tokens) > 0
res = {}
d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")
CULT = dict(zip(d["id"], d["cult"].str.strip()))
SYM = dict(zip(d["id"], d["symbol"].str.strip()))

icit = load_icit()
icit_strings = sorted({tuple(l.tokens) for l in icit if l.complete and l.direction != "unknown"})
icit_strict = set(strict_heldout(icit_strings, "icit"))
faces = collections.defaultdict(lambda: collections.defaultdict(list))
for l in icit:
    faces[l.object_id.split(".")[0]][l.object_id].append(l)
iobj = []
for o in sorted(faces):
    fs = faces[o]
    ls = [x for k in sorted(fs) for x in sorted(fs[k], key=lambda y: y.line_no)]
    if not ls or any(not ok(x) for x in ls):
        continue
    k0 = sorted(fs)[0]
    iobj.append({"text": tuple(t for x in ls for t in x.tokens), "type": ls[0].meta["type"], "site": ls[0].meta["site"],
                 "sym": SYM.get(k0, ""), "cult": CULT.get(k0, "")})


def scan(objs, var, train, conf):
    disc = [x for x in objs if train(x)]
    cf = [x for x in objs if conf(x) and not train(x)]
    def tab(rows, s):
        a = sum(1 for x in rows if var(x) and s in x["text"]); b = sum(1 for x in rows if var(x)) - a
        c = sum(1 for x in rows if not var(x) and s in x["text"]); e = sum(1 for x in rows if not var(x)) - c
        return [[a, b], [c, e]]
    cnt = collections.Counter(t for x in disc for t in set(x["text"]))
    cands = []
    for s in sorted(t for t, n in cnt.items() if n >= 15):
        t = tab(disc, s); o, p = fisher_exact(t)
        if p < 0.01:
            cands.append({"sign": s, "table_disc": t, "odds_disc": o, "p_disc": p, "direction": "greater" if o > 1 else "less"})
    k = len(cands)
    for c in cands:
        t = tab(cf, c["sign"]); c["table_conf"] = t
        if t[0][0] + t[1][0] < 5:
            c["status"] = "insufficient data"; continue
        c["p_conf"] = fisher_exact(t, alternative=c["direction"])[1]
        c["status"] = "confirmed" if c["p_conf"] < 0.01 / k else "not confirmed"
    return {"discovery_objects": len(disc), "discovery_with_variable": sum(1 for x in disc if var(x)),
            "confirmation_objects": len(cf), "confirmation_with_variable": sum(1 for x in cf if var(x)),
            "signs_scanned": sum(1 for n in cnt.values() if n >= 15), "candidates": cands, "threshold": 0.01 / k if k else None,
            "verdict": "supported" if any(c.get("status") == "confirmed" for c in cands) else "not supported"}


itrain = lambda x: x["site"] not in FRESH and not is_heldout(list(x["text"]), "icit") and x["text"] not in icit_strict
iconf = lambda x: x["site"] in FRESH or x["text"] in icit_strict
uni = [x for x in iobj if x["type"] == "SEAL:S" and x["sym"].startswith("Bull1")]
mo2a = [x for x in uni if x["cult"] in {"SAN", "SAF", "RAN", "RAF", "RBF", "S"}]
res["MO2a"] = scan(mo2a, lambda x: x["cult"] == "SAN", itrain, iconf)
res["MO2a"]["codes"] = dict(collections.Counter(x["cult"] for x in mo2a))
mo2b = [x for x in uni if x["sym"] in {"Bull1:W", "Bull1:J", "Bull1:S", "Bull1:I", "Bull1:L"}]
res["MO2b"] = scan(mo2b, lambda x: x["sym"] == "Bull1:W", itrain, iconf)
res["MO2b"]["codes"] = dict(collections.Counter(x["sym"] for x in mo2b))

# ---- MO1k
kp = load_kp1979()
kp_strings = sorted({tuple(l.tokens) for l in kp if l.complete})
kp_strict = set(strict_heldout(kp_strings, "kp1979"))
byk = collections.defaultdict(list)
for l in kp:
    byk[l.object_id].append(l)
kobj = []
for o in sorted(byk, key=lambda x: (len(x), x)):
    v = sorted(byk[o], key=lambda x: x.line_no)
    if any(not ok(x) for x in v) or v[0].meta["type_code"] != "11":
        continue
    ic = v[0].meta["icon_code"].strip()
    if ic and ic != "99":
        kobj.append({"text": tuple(t for x in v for t in x.tokens), "icon": ic,
                     "lines": [tuple(x.tokens) for x in v]})
ktrain = lambda x: all(not is_heldout(list(s), "kp1979") and s not in kp_strict for s in x["lines"])
kconf = lambda x: any(s in kp_strict for s in x["lines"])
res["MO1k"] = scan(kobj, lambda x: x["icon"] == "40", ktrain, kconf)

# ---- CT15r
L = [l for l in icit if l.complete and l.direction != "unknown"]
u = sorted({tuple(l.tokens) for l in L})
data = set(strict_heldout(u, "icit")) | {tuple(l.tokens) for l in L if l.meta["site"] in FRESH}
info = collections.defaultdict(lambda: (set(), set()))
for l in L:
    t = l.meta["type"].strip()
    info[tuple(l.tokens)][0].add("SEAL" if t.startswith("SEAL") else "TAB" if t.startswith("TAB") else None)
    s = l.meta["site"]; info[tuple(l.tokens)][1].add(s if s in ("Harappa", "Mohenjo-daro") else "other")
st = collections.defaultdict(lambda: [[0, 0], [0, 0]])
for s in sorted(data):
    if "740" not in s:
        continue
    ty, si = info[s]
    if len(ty) != 1 or None in ty or len(si) != 1:
        continue
    band = str(min(len(s), 5))
    st[next(iter(si)) + "|" + band][0 if s[-1] == "740" else 1][0 if ty == {"SEAL"} else 1] += 1
odds, p = c2.cmh(list(st.values()), alternative="greater")
res["CT15r"] = {"strata": dict(st), "odds_ratio": odds, "p_value": p, "verdict": "supported" if p < 0.01 else "not supported"}

# ---- FACE4
TERM = {"740", "400", "520", "090", "151", "407", "527", "156"}
multi = []
for o in sorted(faces):
    fs = faces[o]
    if len(fs) >= 3 and all(len(v) == 1 and ok(v[0]) for v in fs.values()):
        multi.append([fs[k][0] for k in sorted(fs)])
flags = [[f.tokens[-1] in TERM for f in m] for m in multi]
obs = sum(sum(x) == 1 for x in flags)
pool = [x for m in flags for x in m]
rng = random.Random(20261125); null = []
for _ in range(10000):
    q = pool[:]; rng.shuffle(q); i = 0; n1 = 0
    for m in flags:
        n1 += sum(q[i:i + len(m)]) == 1; i += len(m)
    null.append(n1)
p4 = (sum(x >= obs for x in null) + 1) / 10001
res["FACE4"] = {"objects": len(multi), "faces": collections.Counter(len(m) for m in multi),
                "types": dict(collections.Counter(m[0].meta["type"] for m in multi)),
                "sites": dict(collections.Counter(m[0].meta["site"] for m in multi)),
                "closing_faces_per_object": dict(collections.Counter(sum(x) for x in flags)),
                "exactly_one": obs, "null_mean": sum(null) / len(null), "p_value": p4,
                "examples": [" / ".join(" ".join(f.tokens) for f in m) for m in multi[:10]],
                "verdict": "insufficient data" if len(multi) < 20 else ("supported" if p4 < 0.01 else "not supported")}
(ROOT / "results" / "batch6_iconography_faces.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, json.dumps(v, default=float)[:900])
