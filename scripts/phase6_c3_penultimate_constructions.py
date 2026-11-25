"""C3: penultimate sign and constructions x object subtype (site-stratified),
discovery train / confirmation held-out. Pre-registered in docs/JOURNAL.md."""
import collections, importlib.util, json, pathlib, sys
from indus.controls import RULES
from indus.corpus import ROOT

spec = importlib.util.spec_from_file_location("c2", pathlib.Path(__file__).with_name("phase6_c2_association_scan.py"))
c2 = importlib.util.module_from_spec(spec); sys.modules["c2"] = c2; spec.loader.exec_module(c2)
SHORT = {"001", "003", "004", "034", "005", "016", "017"}
LONG = {"031", "032", "033", "035"}


def has_pair(s):
    return any(a in x and b in y for a, b in zip(s, s[1:]) for x, y in RULES["icit"]["pairs"])


def features(s):
    f = set()
    if len(s) >= 2:
        f.add(f"penult={s[-2]}")
    if any(t in SHORT for t in s): f.add("has_short_stroke")
    if any(t in LONG for t in s): f.add("has_long_stroke")
    if has_pair(s): f.add("has_count_item_pair")
    if len(s) >= 5: f.add("length>=5")
    return f


def tables(info, feat, value):
    strata = collections.defaultdict(lambda: [[0, 0], [0, 0]])
    for s, d in info.items():
        vals = d["subtype"]
        if len(vals) != 1 or None in vals:
            continue
        st = next(iter(d["site"])) if len(d["site"]) == 1 else "mixed"
        strata[st][0 if feat in features(s) else 1][0 if next(iter(vals)) == value else 1] += 1
    return list(strata.values())


def main():
    tr, ho = c2.build("train"), c2.build("heldout")
    fc = collections.Counter(f for s in tr for f in features(s))
    feats = sorted(f for f, c in fc.items() if c >= 15)
    vc = collections.Counter(next(iter(d["subtype"])) for d in tr.values() if len(d["subtype"]) == 1 and None not in d["subtype"])
    values = sorted(v for v, c in vc.items() if c >= 30)
    tests = []
    for v in values:
        for f in feats:
            o, p = c2.cmh(tables(tr, f, v))
            tests.append({"value": v, "feature": f, "odds_train": o, "p_train": p})
    m = len(tests); order = sorted(range(m), key=lambda i: tests[i]["p_train"]); k = 0
    for r, i in enumerate(order, 1):
        if tests[i]["p_train"] <= 0.05 * r / m:
            k = r
    disc = [tests[i] for i in order[:k]]
    thr = 0.01 / max(1, len(disc))
    for t in disc:
        alt = "greater" if t["odds_train"] > 1 else "less"
        o, p = c2.cmh(tables(ho, t["feature"], t["value"]), alternative=alt)
        t.update(direction=alt, odds_heldout=o, p_heldout=p, confirmed=bool(p < thr))
    res = {"values": values, "n_features": len(feats), "n_tests": m, "n_discovered": len(disc), "threshold": thr,
           "n_confirmed": sum(t["confirmed"] for t in disc), "discovered": disc}
    (ROOT / "results" / "phase6_c3_penultimate_constructions.json").write_text(json.dumps(res, indent=1, default=float))
    print({k_: v for k_, v in res.items() if k_ != "discovered"})
    for t in disc:
        print(f"{t['value']:8s} {t['feature']:22s} OR_tr {t['odds_train']:.2f} p {t['p_train']:.1e} OR_ho {t['odds_heldout']:.2f} p {t['p_heldout']:.1e} {'CONFIRMED' if t['confirmed'] else ''}")


if __name__ == "__main__":
    main()
