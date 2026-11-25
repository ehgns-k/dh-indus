"""CT28: diversity of text stems on seals vs tablets (records, site-matched
subsamples). Pre-registered in docs/JOURNAL.md."""
import collections, json, random
from indus.controls import RULES
from indus.corpus import ROOT, load_icit

T = RULES["icit"]["terminal"]
def stem(s):
    s = list(s)
    while s and s[-1] in T:
        s.pop()
    return tuple(s)
rec = collections.defaultdict(list)
for l in load_icit():
    if not (l.complete and l.direction != "unknown") or l.meta["site"] not in ("Harappa", "Mohenjo-daro"):
        continue
    t = l.meta["type"].strip()
    cls = "SEAL" if t.startswith("SEAL") else "TAB" if t.startswith("TAB") else None
    if cls:
        rec[(l.meta["site"], cls)].append(stem(l.tokens))
rng = random.Random(20261125); diffs = []
sizes = {}
for _ in range(1000):
    d = []
    for site in ("Harappa", "Mohenjo-daro"):
        a, b = rec[(site, "SEAL")], rec[(site, "TAB")]
        n = min(len(a), len(b)); sizes[site] = n
        sa = rng.sample(a, n); sb = rng.sample(b, n)
        d.append(len(set(sa)) / n - len(set(sb)) / n)
    diffs.append(sum(d) / len(d))
share_pos = sum(x > 0 for x in diffs) / len(diffs)
res = {"records": {f"{k[0]}|{k[1]}": len(v) for k, v in rec.items()}, "subsample_n": sizes,
       "mean_difference": sum(diffs) / len(diffs), "share_positive": share_pos, "pass": share_pos >= 0.99}
(ROOT / "results" / "claims_ct28_stem_diversity.json").write_text(json.dumps(res, indent=1))
print(res)
