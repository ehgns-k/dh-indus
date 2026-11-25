"""AR1, AR1h: rare signs cluster within a site. Pre-registered in docs/JOURNAL.md (twenty-fifth session).
Output: results/batch6b_ar1_areas.json"""
import collections, itertools, json, random, re
import pandas as pd
from indus.corpus import ROOT, load_icit

d = pd.read_csv(ROOT / "data" / "raw" / "icit2025.csv", dtype=str).fillna("")
AREA = dict(zip(d["id"], d["area-section"].str.strip()))
ok = lambda l: l.complete and "?" not in l.tokens and len(l.tokens) > 0
faces = collections.defaultdict(lambda: collections.defaultdict(list))
for l in load_icit():
    faces[l.object_id.split(".")[0]][l.object_id].append(l)
res = {}
# The registration of AR1 is ambiguous: its rule (letters before the first non-letter) gives DKG for
# "DKG.", its examples give DK. Both readings are run for Mohenjo-daro ("AR1" rule, "AR1_examples" two letters).
for site, key in (("Mohenjo-daro", "AR1"), ("Mohenjo-daro", "AR1_examples"), ("Harappa", "AR1h")):
    objs = []
    for o in sorted(faces):
        fs = faces[o]
        ls = [x for k in sorted(fs) for x in sorted(fs[k], key=lambda y: y.line_no)]
        if not ls or ls[0].meta["site"] != site or not ls[0].meta["type"].startswith("SEAL") or any(not ok(x) for x in ls):
            continue
        m = re.match(r"[A-Za-z]+", AREA.get(sorted(fs)[0], ""))
        if m:
            a = m.group(0)[:2] if key == "AR1_examples" else m.group(0)
            objs.append({"text": set(t for x in ls for t in x.tokens), "area": a})
    n = collections.Counter(t for x in objs for t in x["text"])
    rare = {t for t, c in n.items() if 2 <= c <= 5}
    by = collections.defaultdict(list)
    for i, x in enumerate(objs):
        for t in x["text"] & rare:
            by[t].append(i)
    pairs = sorted({(i, j) for v in by.values() for i, j in itertools.combinations(sorted(v), 2)})
    areas = [x["area"] for x in objs]
    share = lambda a: sum(a[i] == a[j] for i, j in pairs) / len(pairs)
    obs = share(areas) if pairs else None
    rng = random.Random(20261125); null = []
    if len(pairs) >= 30:
        for _ in range(10000):
            a = areas[:]; rng.shuffle(a); null.append(share(a))
    p = (sum(x >= obs for x in null) + 1) / 10001 if null else None
    res[key] = {"objects": len(objs), "areas": dict(collections.Counter(areas).most_common()), "rare_signs": len(rare),
                "pairs": len(pairs), "share_same_area": obs, "null_mean": sum(null) / len(null) if null else None, "p_value": p,
                "verdict": "insufficient data" if len(pairs) < 30 else ("supported" if p < 0.01 else "not supported")}
(ROOT / "results" / "batch6b_ar1_areas.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
