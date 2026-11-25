"""Descriptive: which ICIT object subtypes correspond to KP1979 type codes?
Matches identical texts (ICIT mapped into KP numbering via the concordance)."""
import collections, csv, json
from indus.corpus import ROOT, load_icit, load_kp1979

conc = {r["icit_sign"]: r["kp1979_sign"] for r in csv.DictReader(open(ROOT / "results" / "phase1_concordance.tsv"), delimiter="\t")
        if int(r["support"]) >= 2 and float(r["purity"]) >= 0.5}
kp = collections.defaultdict(set)
for l in load_kp1979():
    if l.complete:
        kp[tuple(l.tokens)].add(l.meta["type_code"])
icit = collections.defaultdict(collections.Counter)
for l in load_icit():
    if l.complete and l.direction != "unknown" and all(t in conc for t in l.tokens):
        icit[tuple(conc[t] for t in l.tokens)][l.meta["type"].strip()] += 1
tab = collections.defaultdict(collections.Counter)
for s, codes in kp.items():
    if s in icit and len(codes) == 1:
        tab[next(iter(codes))].update(icit[s])
res = {c: dict(t.most_common(6)) for c, t in sorted(tab.items(), key=lambda x: -sum(x[1].values()))}
(ROOT / "results" / "phase6_c2k_code_meaning.json").write_text(json.dumps(res, indent=1))
for c, t in list(res.items())[:10]:
    print(c, t)
