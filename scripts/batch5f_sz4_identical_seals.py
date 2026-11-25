"""SZ4: seals with identical legends are similar in size. Pre-registered in docs/JOURNAL.md
(twenty-fourth session). Output: results/batch5f_sz4_identical_seals.json"""
import collections, itertools, json, math, random
import pandas as pd
from indus.corpus import ROOT, load_icit

d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")
H = dict(zip(d["id"], pd.to_numeric(d["horizontal(mm)"], errors="coerce")))
V = dict(zip(d["id"], pd.to_numeric(d["vertical(mm)"], errors="coerce")))
EX = dict(zip(d["id"], d["excavation-idno"]))
faces = collections.defaultdict(lambda: collections.defaultdict(list))
for l in load_icit():
    faces[l.object_id.split(".")[0]][l.object_id].append(l)
objs = []
for o in sorted(faces):
    fs = faces[o]
    ls = [x for k in sorted(fs) for x in sorted(fs[k], key=lambda y: y.line_no)]
    if not ls or ls[0].meta["type"] != "SEAL:S" or any(not x.complete or "?" in x.tokens or not x.tokens for x in ls):
        continue
    k0 = sorted(fs)[0]
    h, v = H.get(k0), V.get(k0)
    if not (h and v and h > 0 and v > 0) or math.isnan(h) or math.isnan(v):
        continue
    ex = EX.get(k0, "").strip()
    objs.append({"id": o, "site": ls[0].meta["site"], "text": tuple(t for x in ls for t in x.tokens),
                 "size": math.log(h * v), "hv": (h, v), "ex": ex if ex not in ("", "-") else None})
by_text = collections.defaultdict(list)
for i, x in enumerate(objs):
    by_text[x["text"]].append(i)
pairs = [(i, j) for v in by_text.values() if len(v) >= 2 for i, j in itertools.combinations(v, 2)
         if not (objs[i]["ex"] and objs[i]["ex"] == objs[j]["ex"])]
strata = collections.defaultdict(list)
for i, x in enumerate(objs):
    strata[(x["site"], len(x["text"]))].append(i)
obs = sum(abs(objs[i]["size"] - objs[j]["size"]) for i, j in pairs) / len(pairs) if pairs else None
rng = random.Random(20261125); null = []
if len(pairs) >= 20:
    for _ in range(10000):
        tot = 0
        for i, j in pairs:
            c = [k for k in strata[(objs[i]["site"], len(objs[i]["text"]))] if k != i]
            k = rng.choice(c) if c else j
            tot += abs(objs[i]["size"] - objs[k]["size"])
        null.append(tot / len(pairs))
p = (sum(x <= obs for x in null) + 1) / 10001 if null else None
res = {"objects": len(objs), "texts_shared": sum(1 for v in by_text.values() if len(v) >= 2), "pairs": len(pairs),
       "equal_dimensions": sum(objs[i]["hv"] == objs[j]["hv"] for i, j in pairs),
       "same_site_pairs": sum(objs[i]["site"] == objs[j]["site"] for i, j in pairs),
       "mean_abs_diff_log_area": obs, "null_mean": sum(null) / len(null) if null else None, "p_value": p,
       "examples": [{"text": " ".join(objs[i]["text"]), "a": [objs[i]["site"], objs[i]["hv"]], "b": [objs[j]["site"], objs[j]["hv"]]} for i, j in pairs[:12]],
       "verdict": "insufficient data" if len(pairs) < 20 else ("supported" if p < 0.01 else "not supported")}
(ROOT / "results" / "batch5f_sz4_identical_seals.json").write_text(json.dumps(res, indent=1, default=float))
print({k: v for k, v in res.items() if k != "examples"})
for e in res["examples"]: print(e)
