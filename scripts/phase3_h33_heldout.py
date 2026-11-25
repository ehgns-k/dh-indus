"""H3.3: fixed order inside terminal-sign clusters, tested on the held-out split.
Run: PYTHONPATH=src python scripts/phase3_h33_heldout.py
"""
import collections, json
from scipy.stats import binomtest
from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

def split(name):
    L = load_icit() if name == "icit" else load_kp1979()
    u = sorted({tuple(l.tokens) for l in L if l.complete and l.direction != "unknown"})
    tr = [list(s) for s in u if not is_heldout(list(s), name)]
    ho = [list(s) for s in u if is_heldout(list(s), name)]
    return tr, ho

res = {}
prev = json.loads((ROOT / "results" / "phase3_structure.json").read_text())
for name in ["icit", "kp1979"]:
    T = set(prev["H3.1"][name]["terminal_signs"])
    tr, ho = split(name)
    def pairs(seqs):
        return collections.Counter((s[i], s[i+1]) for s in seqs for i in range(len(s)-1)
                                   if s[i] in T and s[i+1] in T and s[i] != s[i+1])
    ptr, pho = pairs(tr), pairs(ho)
    dom = {}
    for (a, b), c in ptr.items():
        key = frozenset((a, b))
        if c > ptr.get((b, a), 0):
            dom[key] = (a, b)
    agree = sum(c for p, c in pho.items() if dom.get(frozenset(p)) == p)
    total = sum(c for p, c in pho.items() if frozenset(p) in dom)
    bt = binomtest(agree, total, 0.5, alternative="greater") if total else None
    res[name] = {"terminal_set": sorted(T), "train_pairs": {f"{a}>{b}": c for (a, b), c in ptr.most_common()},
                 "heldout_pairs": {f"{a}>{b}": c for (a, b), c in pho.most_common()},
                 "agree": agree, "total": total, "rate": agree / total if total else None,
                 "p_value": bt.pvalue if bt else None}
    print(name, agree, total, res[name]["rate"], res[name]["p_value"])
    print("  train", list(res[name]["train_pairs"].items())[:8])
    print("  held ", list(res[name]["heldout_pairs"].items())[:8])
(ROOT / "results" / "phase3_h33_heldout.json").write_text(json.dumps(res, indent=1))
