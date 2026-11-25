"""H9.4: substitution classes x object subtype (site-stratified CMH);
discovery train / confirmation strict held-out. Pre-registered in docs/JOURNAL.md."""
import collections, importlib.util, json, pathlib, sys
from indus.corpus import ROOT, load_icit, strict_heldout

here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("c2", here / "phase6_c2_association_scan.py")
c2 = importlib.util.module_from_spec(spec); sys.modules["c2"] = c2; spec.loader.exec_module(c2)
h93 = json.loads((ROOT / "results" / "phase9_h93_substitution_classes.json").read_text())
classes = {f"class{i}": set(c) for i, c in enumerate(h93["icit_classes_list"]) if len(c) >= 10}
tr = c2.build("train")
ho_all = c2.build("heldout")
u = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
strict = strict_heldout(u, "icit")
ho = {s: d for s, d in ho_all.items() if s in strict}


def tables(info, cname, value):
    st = collections.defaultdict(lambda: [[0, 0], [0, 0]])
    for s, d in info.items():
        if len(d["subtype"]) != 1 or None in d["subtype"]:
            continue
        k = next(iter(d["site"])) if len(d["site"]) == 1 else "mixed"
        st[k][0 if set(s) & classes[cname] else 1][0 if next(iter(d["subtype"])) == value else 1] += 1
    return list(st.values())


vc = collections.Counter(next(iter(d["subtype"])) for d in tr.values() if len(d["subtype"]) == 1 and None not in d["subtype"])
values = sorted(v for v, c in vc.items() if c >= 30)
tests = []
for v in values:
    for c in sorted(classes):
        o, p = c2.cmh(tables(tr, c, v))
        tests.append({"class": c, "size": len(classes[c]), "value": v, "odds_train": o, "p_train": p})
m = len(tests); order = sorted(range(m), key=lambda i: tests[i]["p_train"]); k = 0
for r, i in enumerate(order, 1):
    if tests[i]["p_train"] <= 0.05 * r / m:
        k = r
disc = [tests[i] for i in order[:k]]; thr = 0.01 / max(1, len(disc))
for t in disc:
    alt = "greater" if t["odds_train"] > 1 else "less"
    o, p = c2.cmh(tables(ho, t["class"], t["value"]), alternative=alt)
    t.update(direction=alt, odds_heldout=o, p_heldout=p, confirmed=bool(p < thr))
res = {"classes": {c: sorted(v) for c, v in classes.items()}, "values": values, "n_tests": m, "n_discovered": len(disc),
       "threshold": thr, "n_confirmed": sum(t["confirmed"] for t in disc), "discovered": disc}
(ROOT / "results" / "phase9_h94_classes_objects.json").write_text(json.dumps(res, indent=1, default=float))
for c, v in classes.items(): print(c, len(v), sorted(v)[:12])
print({k_: v for k_, v in res.items() if k_ not in ("discovered", "classes")})
for t in disc:
    print(t["class"], t["value"], round(t["odds_train"], 2), f"{t['p_train']:.1e}", round(t["odds_heldout"], 2), f"{t['p_heldout']:.1e}", "CONFIRMED" if t["confirmed"] else "")
