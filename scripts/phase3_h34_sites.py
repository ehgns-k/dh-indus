"""H3.4: terminal-cluster order learned at one site predicts the other site."""
import collections, json
from scipy.stats import binomtest
from indus.corpus import ROOT, load_icit

prev = json.loads((ROOT / "results" / "phase3_structure.json").read_text())
T = set(prev["H3.1"]["icit"]["terminal_signs"])
sites = collections.defaultdict(set)
for l in load_icit():
    if l.complete and l.direction != "unknown":
        sites[tuple(l.tokens)].add(l.meta["site"])
by = collections.defaultdict(list)
for s, st in sites.items():
    if len(st) == 1:
        by[next(iter(st))].append(list(s))

def pairs(seqs):
    return collections.Counter((s[i], s[i+1]) for s in seqs for i in range(len(s)-1)
                               if s[i] in T and s[i+1] in T and s[i] != s[i+1])

def predict(src, dst):
    ps, pd = pairs(by[src]), pairs(by[dst])
    dom = {frozenset(p): p for p, c in ps.items() if c > ps.get(p[::-1], 0)}
    agree = sum(c for p, c in pd.items() if dom.get(frozenset(p)) == p)
    total = sum(c for p, c in pd.items() if frozenset(p) in dom)
    return {"src": src, "dst": dst, "agree": agree, "total": total,
            "rate": agree / total if total else None,
            "p_value": binomtest(agree, total, 0.5, alternative="greater").pvalue if total else None,
            "dst_pairs": {f"{a}>{b}": c for (a, b), c in pd.most_common()}}

res = [predict("Harappa", "Mohenjo-daro"), predict("Mohenjo-daro", "Harappa")]
others = [s for s in by if s not in ("Harappa", "Mohenjo-daro")]
by["Other"] = [x for s in others for x in by[s]]
by["H+M"] = by["Harappa"] + by["Mohenjo-daro"]
res.append(predict("H+M", "Other"))
for r in res:
    print(r["src"], "->", r["dst"], r["agree"], r["total"], r["rate"], r["p_value"])
(ROOT / "results" / "phase3_h34_sites.json").write_text(json.dumps(res, indent=1))
