"""R1 (review): re-decide supported held-out results on the strict held-out set
(no training string within edit distance 1). Pre-registered in docs/JOURNAL.md."""
import collections, importlib.util, json, pathlib, sys
from scipy.stats import binomtest, fisher_exact
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979, strict_heldout

here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("c2", here / "phase6_c2_association_scan.py")
c2 = importlib.util.module_from_spec(spec); sys.modules["c2"] = c2; spec.loader.exec_module(c2)

U = {}
for name, f in [("icit", load_icit), ("kp1979", load_kp1979)]:
    U[name] = sorted({tuple(l.tokens) for l in f() if l.complete and l.direction != "unknown"})
STRICT = {n: strict_heldout(U[n], n) for n in U}
TRAIN = {n: [list(s) for s in U[n] if not is_heldout(list(s), n)] for n in U}
res = {"strict_sizes": {n: len(STRICT[n]) for n in U},
       "heldout_sizes": {n: sum(is_heldout(list(s), n) for s in U[n]) for n in U}}

# H3.3
prev = json.loads((ROOT / "results" / "phase3_structure.json").read_text())
for n in U:
    T = set(prev["H3.1"][n]["terminal_signs"])
    pairs = lambda seqs: collections.Counter((s[i], s[i + 1]) for s in seqs for i in range(len(s) - 1)
                                             if s[i] in T and s[i + 1] in T and s[i] != s[i + 1])
    ptr, pho = pairs(TRAIN[n]), pairs([list(s) for s in STRICT[n]])
    dom = {frozenset(p): p for p, c in ptr.items() if c > ptr.get(p[::-1], 0)}
    agree = sum(c for p, c in pho.items() if dom.get(frozenset(p)) == p)
    total = sum(c for p, c in pho.items() if frozenset(p) in dom)
    p = binomtest(agree, total, 0.5, alternative="greater").pvalue if total else None
    res[f"H3.3|{n}"] = {"agree": agree, "total": total, "p": p,
                        "pass": bool(total and agree / total >= 0.8 and p < 0.01)}


def fisher_bigram(n, S, T, thr):
    a = b = c = d = 0
    for s in STRICT[n]:
        for x, y in zip(s, s[1:]):
            if x in S:
                a += y in T; b += y not in T
            else:
                c += y in T; d += y not in T
    o, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    return {"table": [[a, b], [c, d]], "odds": o, "p": p, "pass": bool(p < thr)}

res["H3.10|kp1979"] = fisher_bigram("kp1979", {"124", "125", "126", "127", "128", "129"}, {"86"}, 0.01)
res["H3.10|icit"] = fisher_bigram("icit", {"004", "034", "005", "016", "017"}, {"390", "405", "406", "407"}, 0.01)
res["H3.12a|kp1979"] = fisher_bigram("kp1979", {"127"}, {"288", "289"}, 0.005)
res["H3.12a|icit"] = fisher_bigram("icit", {"017"}, {"585", "575"}, 0.005)
res["H3.12b|kp1979"] = fisher_bigram("kp1979", {"147"}, {"217"}, 0.005)
res["H3.12b|icit"] = fisher_bigram("icit", {"033"}, {"520"}, 0.005)

# C2
ho = c2.build("heldout")
ho = {s: d for s, d in ho.items() if s in STRICT["icit"]}
c2res = json.loads((ROOT / "results" / "phase6_c2_association_scan.json").read_text())
for t in c2res["discovered"]:
    if t["confirmed"]:
        o, p = c2.cmh(c2.tables_for(ho, t["variable"], t["sign"], t["value"]), alternative=t["direction"])
        res[f"C2|{t['variable']}={t['value']}|{t['sign']}"] = {"odds": o, "p": p, "pass": bool(p < 0.01 / 40)}

# C2k
codes = collections.defaultdict(set)
for l in load_kp1979():
    if l.complete:
        codes[tuple(l.tokens)].add(l.meta["type_code"])
hk = {s: next(iter(c)) for s, c in codes.items() if len(c) == 1 and s in STRICT["kp1979"]}
a = sum(1 for s, c in hk.items() if s[-1] == "98" and c == "11"); b = sum(1 for s, c in hk.items() if s[-1] == "98" and c != "11")
c_ = sum(1 for s, c in hk.items() if s[-1] != "98" and c == "11"); d = sum(1 for s, c in hk.items() if s[-1] != "98" and c != "11")
o, p = fisher_exact([[a, b], [c_, d]], alternative="less")
res["C2k|11|98"] = {"table": [[a, b], [c_, d]], "odds": o, "p": p, "pass": bool(p < 0.001)}

(ROOT / "results" / "review_r1_strict_heldout.json").write_text(json.dumps(res, indent=1, default=float))
for k, v in res.items():
    print(k, v)
