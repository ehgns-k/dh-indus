"""H4.1 (claim C31a) and H4.2 (claim C30); pre-registered in docs/JOURNAL.md."""
import collections, json
import numpy as np
from scipy.stats import fisher_exact
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from indus.corpus import ROOT, is_heldout, load_icit

NUMERALS = {"003", "004", "034", "005", "016", "017"}
ANIMALS = {"Gaur", "Zebu", "Elep", "Rhin", "Buff", "Tigr", "Goat"}
lines = [l for l in load_icit() if l.complete and l.direction != "unknown"]

def coarse(t):
    t = t.strip()
    return "SEAL" if t.startswith("SEAL") else ("TAB" if t.startswith("TAB") else None)

def feats(s):
    f = collections.Counter(f"sign={t}" for t in s)
    f[f"first={s[0]}"] = 1; f[f"last={s[-1]}"] = 1; f[f"len={min(len(s), 8)}"] = 1
    return dict(f)

res = {}
# ---- H4.1
info = collections.defaultdict(lambda: (set(), set()))
for l in lines:
    info[tuple(l.tokens)][0].add(coarse(l.meta["type"])); info[tuple(l.tokens)][1].add(l.meta["site"])
for site in ["Harappa", "Mohenjo-daro"]:
    t = collections.Counter()
    for s, (ty, st) in sorted(info.items()):
        if len(ty) == 1 and None not in ty and st == {site} and is_heldout(list(s), "icit"):
            t[(next(iter(ty)), any(x in NUMERALS for x in s))] += 1
    table = [[t[("TAB", True)], t[("TAB", False)]], [t[("SEAL", True)], t[("SEAL", False)]]]
    odds, p = fisher_exact(table, alternative="greater")
    res[f"H4.1|{site}"] = {"table_[[tab_num,tab_no],[seal_num,seal_no]]": table,
                           "tab_share": table[0][0] / max(1, sum(table[0])),
                           "seal_share": table[1][0] / max(1, sum(table[1])), "odds_ratio": odds, "p_value": p}
# ---- H4.2
mot = collections.defaultdict(set)
for l in lines:
    if coarse(l.meta["type"]) == "SEAL":
        m = l.meta["symbol"].split(":")[0].strip()
        mot[tuple(l.tokens)].add("Bull1" if m == "Bull1" else ("other" if m in ANIMALS else None))
data = sorted((list(s), next(iter(m))) for s, m in mot.items() if len(m) == 1 and None not in m)
tr = [(s, y) for s, y in data if not is_heldout(s, "icit")]
te = [(s, y) for s, y in data if is_heldout(s, "icit")]
dv = DictVectorizer(); X = dv.fit_transform([feats(s) for s, _ in tr]); y = np.array([b for _, b in tr])
Xte = dv.transform([feats(s) for s, _ in te]); yte = [b for _, b in te]
def ev(lab):
    m = LogisticRegression(max_iter=2000, class_weight="balanced").fit(X, lab)
    return balanced_accuracy_score(yte, m.predict(Xte)), m
obs, m = ev(y); rng = np.random.default_rng(20261125)
null = np.array([ev(rng.permutation(y))[0] for _ in range(200)])
names = np.array(dv.get_feature_names_out()); coef = m.coef_[0]; o = np.argsort(coef)
res["H4.2"] = {"train": dict(collections.Counter(y.tolist())), "test": dict(collections.Counter(yte)),
               "balanced_accuracy": obs, "null_mean": float(null.mean()), "null_sd": float(null.std()),
               "p_value": float((np.sum(null >= obs) + 1) / 201), "positive_class": m.classes_[1],
               "top_positive": [(names[i], round(float(coef[i]), 2)) for i in o[::-1][:10]],
               "top_negative": [(names[i], round(float(coef[i]), 2)) for i in o[:10]]}
(ROOT / "results" / "phase4_h41_h42_claims.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
