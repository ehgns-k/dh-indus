"""H3.6: seal vs TAB:B texts, trained at Harappa, tested at Mohenjo-daro.
Pre-registered in docs/JOURNAL.md. Same design as H3.5.
"""
import collections, json
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("h35", pathlib.Path(__file__).with_name("phase3_h35_objecttype.py"))
h35 = importlib.util.module_from_spec(spec); spec.loader.exec_module(h35)
from indus.corpus import ROOT, is_heldout, load_icit

def coarse(t):
    t = t.strip()
    if t.startswith("SEAL"):
        return "SEAL"
    if t.startswith("TAB:B"):
        return "TAB_B"
    return None

info = collections.defaultdict(lambda: (set(), set()))
for l in load_icit():
    if l.complete and l.direction != "unknown":
        k = tuple(l.tokens)
        info[k][0].add(coarse(l.meta["type"])); info[k][1].add(l.meta["site"])
data = [(list(s), next(iter(t)), st) for s, (t, st) in info.items() if len(t) == 1 and None not in t]
tr = [(s, y) for s, y, st in data if st == {"Harappa"} and not is_heldout(s, "icit")]
te = [(s, y) for s, y, st in data if st == {"Mohenjo-daro"}]
dv = DictVectorizer(); X = dv.fit_transform([h35.feats(s) for s, _ in tr]); y = np.array([b for _, b in tr])
Xte = dv.transform([h35.feats(s) for s, _ in te]); yte = [b for _, b in te]
def ev(lab):
    m = LogisticRegression(max_iter=2000, class_weight="balanced").fit(X, lab)
    return balanced_accuracy_score(yte, m.predict(Xte)), m
obs, m = ev(y); rng = np.random.default_rng(20261125)
null = np.array([ev(rng.permutation(y))[0] for _ in range(200)])
names = np.array(dv.get_feature_names_out()); coef = m.coef_[0]; o = np.argsort(coef)
res = {"train": dict(collections.Counter(y.tolist())), "test": dict(collections.Counter(yte)),
       "balanced_accuracy": obs, "null_mean": float(null.mean()), "null_sd": float(null.std()),
       "p_value": float((np.sum(null >= obs) + 1) / 201), "positive_class": m.classes_[1],
       "top_features_positive": [(names[i], round(float(coef[i]), 2)) for i in o[::-1][:12]],
       "top_features_negative": [(names[i], round(float(coef[i]), 2)) for i in o[:12]]}
(ROOT / "results" / "phase3_h36_tabB.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
