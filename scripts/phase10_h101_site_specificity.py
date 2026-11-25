"""H10.1: are name-like slot fillers (class 0) more site-specific than
conventional signs (class 1, class 2, stroke signs)? Pre-registered in
docs/JOURNAL.md (seventeenth session)."""
import collections, json
import numpy as np
from scipy.spatial.distance import jensenshannon
from indus.corpus import ROOT, load_icit

h93 = json.loads((ROOT / "results" / "phase9_h93_substitution_classes.json").read_text())
cls = {s: i for i, c in enumerate(h93["icit_classes_list"]) for s in c}
STROKE = {"001", "003", "004", "034", "005", "016", "017", "031", "032", "033", "035"}
sites = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown":
        st = l.meta["site"]; sites[tuple(l.tokens)].add(st if st in ("Harappa", "Mohenjo-daro") else "other")
S = ["Harappa", "Mohenjo-daro", "other"]
cnt = collections.defaultdict(lambda: np.zeros(3)); tot = np.zeros(3)
for s, st in sites.items():
    if len(st) != 1:
        continue
    k = S.index(next(iter(st)))
    for t in s:
        if t != "?":
            cnt[t][k] += 1; tot[k] += 1
base = tot / tot.sum()
signs = [t for t in cnt if cnt[t].sum() >= 15]
group = {}
for t in signs:
    if cls.get(t) == 0 and t not in STROKE:
        group[t] = "name"
    elif t in STROKE or cls.get(t) in (1, 2):
        group[t] = "conv"
signs = sorted(group)
spec = {t: float(jensenshannon(cnt[t] / cnt[t].sum(), base, base=2)) for t in signs}
freq = np.array([cnt[t].sum() for t in signs]); tert = np.digitize(freq, np.quantile(freq, [1 / 3, 2 / 3]))
lab = np.array([group[t] for t in signs]); val = np.array([spec[t] for t in signs])
def stat(l):
    return val[l == "name"].mean() - val[l == "conv"].mean()
obs = stat(lab); rng = np.random.default_rng(20261125); null = []
for _ in range(10000):
    l2 = lab.copy()
    for b in range(3):
        idx = np.where(tert == b)[0]; l2[idx] = rng.permutation(l2[idx])
    null.append(stat(l2))
null = np.array(null)
res = {"n_name": int((lab == "name").sum()), "n_conv": int((lab == "conv").sum()),
       "mean_spec_name": float(val[lab == "name"].mean()), "mean_spec_conv": float(val[lab == "conv"].mean()),
       "difference": float(obs), "null_mean": float(null.mean()), "null_sd": float(null.std()),
       "p_value": float((np.sum(null >= obs) + 1) / 10001),
       "most_specific": sorted(((spec[t], t, group[t], cnt[t].tolist()) for t in signs), reverse=True)[:15]}
(ROOT / "results" / "phase10_h101_site_specificity.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "most_specific"}, indent=1))
for x in res["most_specific"][:12]: print(x)
