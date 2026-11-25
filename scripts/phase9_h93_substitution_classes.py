"""H9.3: paradigmatic classes from substitutions in minimal pairs, compared
across the two transcriptions. Pre-registered in docs/JOURNAL.md."""
import collections, csv, json
import networkx as nx
import numpy as np
from sklearn.metrics import adjusted_rand_score
from indus.corpus import ROOT, load_icit, load_kp1979


def graph(f):
    u = sorted({tuple(l.tokens) for l in f() if l.complete and l.direction != "unknown" and "?" not in l.tokens})
    by_key = collections.defaultdict(set)
    for s in u:
        for i in range(len(s)):
            by_key[(len(s), i, s[:i] + s[i + 1:])].add(s[i])
    w = collections.Counter()
    for signs in by_key.values():
        signs = sorted(signs)
        for a in range(len(signs)):
            for b in range(a + 1, len(signs)):
                w[(signs[a], signs[b])] += 1
    G = nx.Graph()
    for (a, b), c in w.items():
        G.add_edge(a, b, weight=c)
    keep = [n for n in G if G.degree(n, weight="weight") >= 2]
    G = G.subgraph(keep).copy()
    comms = nx.community.louvain_communities(G, weight="weight", resolution=1.0, seed=20261125)
    lab = {n: i for i, c in enumerate(comms) for n in c}
    return G, comms, lab


Gi, Ci, li = graph(load_icit)
Gk, Ck, lk = graph(load_kp1979)
rows = [r for r in csv.DictReader(open(ROOT / "results" / "phase1_concordance.tsv"), delimiter="\t")
        if int(r["support"]) >= 3 and float(r["purity"]) >= 0.8]
tc = collections.Counter(r["kp1979_sign"] for r in rows)
pairs = sorted((r["icit_sign"], r["kp1979_sign"]) for r in rows if tc[r["kp1979_sign"]] == 1 and r["icit_sign"] in li and r["kp1979_sign"] in lk)
a = np.array([li[x] for x, _ in pairs]); b = np.array([lk[y] for _, y in pairs])
obs = adjusted_rand_score(a, b)
rng = np.random.default_rng(20261125)
null = np.array([adjusted_rand_score(a, rng.permutation(b)) for _ in range(10000)])
res = {"icit_nodes": Gi.number_of_nodes(), "icit_classes": len(Ci), "kp_nodes": Gk.number_of_nodes(), "kp_classes": len(Ck),
       "linked_signs": len(pairs), "ari": float(obs), "null_mean": float(null.mean()), "null_sd": float(null.std()),
       "p_value": float((np.sum(null >= obs) + 1) / 10001),
       "icit_classes_list": sorted([sorted(c) for c in Ci if len(c) >= 3], key=len, reverse=True)[:12]}
(ROOT / "results" / "phase9_h93_substitution_classes.json").write_text(json.dumps(res, indent=1))
print({k: v for k, v in res.items() if k != "icit_classes_list"})
for c in res["icit_classes_list"][:10]: print(len(c), c[:25])
