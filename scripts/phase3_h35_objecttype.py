"""H3.5: do seal texts and tablet texts differ in a way that transfers from
Harappa to Mohenjo-daro? Pre-registered in docs/JOURNAL.md.
Run: PYTHONPATH=src python scripts/phase3_h35_objecttype.py
"""
import collections
import json

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

from indus.corpus import ROOT, is_heldout, load_icit

SEED = 20261125
N_PERM = 200


def coarse(t):
    t = t.strip()
    if t.startswith("SEAL"):
        return "SEAL"
    if t.startswith("TAB"):
        return "TAB"
    return None


def strings_by_site():
    info = collections.defaultdict(lambda: (set(), set()))
    for l in load_icit():
        if not (l.complete and l.direction != "unknown"):
            continue
        key = tuple(l.tokens)
        info[key][0].add(coarse(l.meta["type"]))
        info[key][1].add(l.meta["site"])
    out = []
    for s, (types, sites) in info.items():
        if len(types) == 1 and None not in types:
            out.append((list(s), next(iter(types)), sites))
    return out


def feats(s):
    f = collections.Counter(f"sign={t}" for t in s)
    f[f"first={s[0]}"] = 1
    f[f"last={s[-1]}"] = 1
    f[f"len={min(len(s), 8)}"] = 1
    return dict(f)


def main():
    data = strings_by_site()
    train = [(s, y) for s, y, st in data if st == {"Harappa"} and not is_heldout(s, "icit")]
    test = [(s, y) for s, y, st in data if st == {"Mohenjo-daro"}]
    test_ho = [(s, y) for s, y in test if is_heldout(s, "icit")]
    dv = DictVectorizer()
    Xtr = dv.fit_transform([feats(s) for s, _ in train])
    ytr = np.array([y for _, y in train])

    def evaluate(labels, rows):
        m = LogisticRegression(max_iter=2000, class_weight="balanced").fit(Xtr, labels)
        X = dv.transform([feats(s) for s, _ in rows])
        return balanced_accuracy_score([y for _, y in rows], m.predict(X)), m

    obs, model = evaluate(ytr, test)
    obs_ho, _ = evaluate(ytr, test_ho)
    rng = np.random.default_rng(SEED)
    null = np.array([evaluate(rng.permutation(ytr), test)[0] for _ in range(N_PERM)])
    p = float((np.sum(null >= obs) + 1) / (N_PERM + 1))
    names = np.array(dv.get_feature_names_out())
    coef = model.coef_[0]  # positive = class model.classes_[1]
    order = np.argsort(coef)
    res = {
        "train": dict(collections.Counter(ytr.tolist())),
        "test_primary": dict(collections.Counter(y for _, y in test)),
        "test_heldout": dict(collections.Counter(y for _, y in test_ho)),
        "balanced_accuracy_primary": obs,
        "balanced_accuracy_heldout": obs_ho,
        "null_mean": float(null.mean()), "null_sd": float(null.std()), "p_value": p,
        "positive_class": model.classes_[1],
        "top_features_positive": [(names[i], round(float(coef[i]), 2)) for i in order[::-1][:15]],
        "top_features_negative": [(names[i], round(float(coef[i]), 2)) for i in order[:15]],
    }
    (ROOT / "results" / "phase3_h35_objecttype.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
