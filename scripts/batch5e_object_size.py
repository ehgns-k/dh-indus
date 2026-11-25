"""SZ1, SZ2, FACE3: object size as an external variable. Pre-registered in docs/JOURNAL.md
(twenty-fourth session). Output: results/batch5e_object_size.json"""
import collections, json, math, random
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
from indus.corpus import ROOT, load_icit, is_heldout, strict_heldout

FRESH = {"Dholavira", "Nausharo", "Farmana", "Gola Dhoro (Bagasra)", "Lakhanjo-daro", "Kanmer",
         "Bhirrana", "Khirsara", "Shikarpur", "Ganweriwala"}
d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")
H = dict(zip(d["id"], pd.to_numeric(d["horizontal(mm)"], errors="coerce")))
V = dict(zip(d["id"], pd.to_numeric(d["vertical(mm)"], errors="coerce")))

lines = load_icit()
faces = collections.defaultdict(lambda: collections.defaultdict(list))
for l in lines:
    faces[l.object_id.split(".")[0]][l.object_id].append(l)
objs = []
for o in sorted(faces):
    fs = faces[o]
    ls = [x for k in sorted(fs) for x in sorted(fs[k], key=lambda y: y.line_no)]
    if not ls or any(not x.complete or "?" in x.tokens or not x.tokens for x in ls):
        continue
    size = None
    for k in sorted(fs):
        h, v = H.get(k), V.get(k)
        if h and v and h > 0 and v > 0 and not (math.isnan(h) or math.isnan(v)):
            size = math.log(h * v); break
    if size is None:
        continue
    text = tuple(t for x in ls for t in x.tokens)
    objs.append({"id": o, "type": ls[0].meta["type"], "site": ls[0].meta["site"], "text": text,
                 "faces": [tuple(x.tokens) for x in ls], "size": size})

res = {}
# ---- SZ1
seal = [x for x in objs if x["type"] == "SEAL:S"]
rho, p = spearmanr([x["size"] for x in seal], [len(x["text"]) for x in seal])
res["SZ1"] = {"objects": len(seal), "spearman": float(rho), "p_one_sided": float(p / 2 if rho > 0 else 1 - p / 2),
              "verdict": "supported" if rho > 0 and p / 2 < 0.01 else "not supported"}

# ---- residual size
strata = collections.defaultdict(list)
for x in objs:
    strata[(x["type"], x["site"], min(len(x["text"]), 8))].append(x)
for k, v in strata.items():
    if len(v) >= 2:
        m = sum(y["size"] for y in v) / len(v)
        for y in v:
            y["resid"] = y["size"] - m

# ---- SZ2
all_strings = sorted({tuple(l.tokens) for l in lines if l.complete and l.direction != "unknown"})
strict = set(strict_heldout(all_strings, "icit"))
def is_train(x):
    return x["site"] not in FRESH and not is_heldout(list(x["text"]), "icit") and x["text"] not in strict
def is_conf(x):
    return x["site"] in FRESH or x["text"] in strict
S = [x for x in seal if "resid" in x]
disc = [x for x in S if is_train(x)]
conf = [x for x in S if is_conf(x) and not is_train(x)]
cnt = collections.Counter(t for x in disc for t in set(x["text"]))
cands = []
for t in sorted(s for s, n in cnt.items() if n >= 20):
    a = [x["resid"] for x in disc if t in x["text"]]; b = [x["resid"] for x in disc if t not in x["text"]]
    u, pv = mannwhitneyu(a, b, alternative="two-sided")
    if pv < 0.01:
        cands.append({"sign": t, "n_disc": len(a), "median_with": float(np.median(a)), "median_without": float(np.median(b)),
                      "direction": "larger" if np.median(a) > np.median(b) else "smaller", "p_disc": float(pv)})
k = len(cands)
for c in cands:
    a = [x["resid"] for x in conf if c["sign"] in x["text"]]; b = [x["resid"] for x in conf if c["sign"] not in x["text"]]
    c["n_conf"] = len(a)
    if len(a) < 5:
        c["status"] = "insufficient data"; continue
    alt = "greater" if c["direction"] == "larger" else "less"
    c["p_conf"] = float(mannwhitneyu(a, b, alternative=alt).pvalue)
    c["median_with_conf"] = float(np.median(a)); c["median_without_conf"] = float(np.median(b))
    c["status"] = "confirmed" if c["p_conf"] < 0.01 / k else "not confirmed"
res["SZ2"] = {"discovery_objects": len(disc), "confirmation_objects": len(conf), "signs_scanned": sum(1 for n in cnt.values() if n >= 20),
              "candidates": cands, "threshold": 0.01 / k if k else None,
              "verdict": "supported" if any(c.get("status") == "confirmed" for c in cands) else "not supported"}

# ---- FACE3
NUMV = {"032": 2, "033": 3, "034": 4}
rows = []
for x in objs:
    if len(x["faces"]) != 2 or not x["type"].startswith("TAB"):
        continue
    a, b = x["faces"]
    isn = lambda f: len(f) == 2 and f[1] == "700" and f[0] in NUMV
    if isn(a) != isn(b):
        num, txt = (a, b) if isn(a) else (b, a)
        rows.append((txt, NUMV[num[0]], x["size"]))
ser = collections.defaultdict(list)
for txt, c, s in rows:
    ser[txt].append((c, s))
ser = {t: v for t, v in ser.items() if len(v) >= 2 and len({c for c, _ in v}) > 1}
n_obj = sum(len(v) for v in ser.values())
def stat(series):
    cs, ss = [], []
    for v in series:
        mc = sum(c for c, _ in v) / len(v); ms = sum(s for _, s in v) / len(v)
        cs += [c - mc for c, _ in v]; ss += [s - ms for _, s in v]
    return float(spearmanr(cs, ss)[0])
keys = sorted(ser)
obs = stat([ser[t] for t in keys]) if n_obj else None
rng = random.Random(20261125); null = []
if n_obj >= 30:
    for _ in range(10000):
        perm = []
        for t in keys:
            cs = [c for c, _ in ser[t]]; rng.shuffle(cs)
            perm.append([(c, s) for c, (_, s) in zip(cs, ser[t])])
        null.append(stat(perm))
    p2 = (sum(abs(x) >= abs(obs) for x in null) + 1) / 10001
else:
    p2 = None
res["FACE3"] = {"objects_with_numeral_face_and_size": len(rows), "series_with_varying_counts": len(ser), "objects_in_them": n_obj,
                "spearman_within_series": obs, "p_two_sided": p2,
                "verdict": "insufficient data" if n_obj < 30 else ("supported" if p2 < 0.01 else "not supported")}
(ROOT / "results" / "batch5e_object_size.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1)[:3000])
