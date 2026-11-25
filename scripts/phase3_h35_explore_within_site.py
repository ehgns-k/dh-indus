"""Exploratory (not pre-registered) follow-up to H3.5: seal vs tablet within
Harappa only (train: non-held-out, test: held-out). Also reports which tablet
subtypes occur in train and test, since Harappa tablets are mostly TAB:B/TAB:I
and Mohenjo-daro tablets mostly TAB:C.
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

data = h35.strings_by_site()
har = [(s, y) for s, y, st in data if st == {"Harappa"}]
tr = [(s, y) for s, y in har if not is_heldout(s, "icit")]
te = [(s, y) for s, y in har if is_heldout(s, "icit")]
dv = DictVectorizer(); X = dv.fit_transform([h35.feats(s) for s, _ in tr]); y = np.array([b for _, b in tr])
def ev(lab):
    m = LogisticRegression(max_iter=2000, class_weight="balanced").fit(X, lab)
    return balanced_accuracy_score([b for _, b in te], m.predict(dv.transform([h35.feats(s) for s, _ in te])))
obs = ev(y); rng = np.random.default_rng(1)
null = np.array([ev(rng.permutation(y)) for _ in range(200)])
sub = collections.Counter()
for l in load_icit():
    if l.complete and l.direction != "unknown" and l.meta["type"].startswith("TAB"):
        sub[(l.meta["site"] if l.meta["site"] in ("Harappa", "Mohenjo-daro") else "other", l.meta["type"].strip())] += 1
res = {"status": "exploratory, not pre-registered", "train": dict(collections.Counter(y.tolist())),
       "test": dict(collections.Counter(b for _, b in te)), "balanced_accuracy": obs,
       "null_mean": float(null.mean()), "p_value": float((np.sum(null >= obs) + 1) / 201),
       "tablet_subtypes_by_site": {f"{a}|{b}": c for (a, b), c in sub.most_common()}}
(ROOT / "results" / "phase3_h35_explore_within_site.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
