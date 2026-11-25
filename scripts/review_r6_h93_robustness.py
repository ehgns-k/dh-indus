"""R6 (review, not pre-registered): robustness of H9.3 to the Louvain
resolution (0.6, 0.8, 1.0, 1.2, 1.5) and to the random seed (5 seeds)."""
import collections, csv, importlib.util, json, pathlib, sys
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
    for (a, b), c in sorted(w.items()):
        G.add_edge(a, b, weight=c)
    return G.subgraph([n for n in G if G.degree(n, weight="weight") >= 2]).copy()

Gi, Gk = graph(load_icit), graph(load_kp1979)
rows = [r for r in csv.DictReader(open(ROOT / "results" / "phase1_concordance.tsv"), delimiter="\t")
        if int(r["support"]) >= 3 and float(r["purity"]) >= 0.8]
tc = collections.Counter(r["kp1979_sign"] for r in rows)
res = {}
rng = np.random.default_rng(20261125)
for resol in (0.6, 0.8, 1.0, 1.2, 1.5):
    for seed in (1, 2, 3, 4, 5):
        li = {n: i for i, c in enumerate(nx.community.louvain_communities(Gi, weight="weight", resolution=resol, seed=seed)) for n in c}
        lk = {n: i for i, c in enumerate(nx.community.louvain_communities(Gk, weight="weight", resolution=resol, seed=seed)) for n in c}
        pairs = sorted((r["icit_sign"], r["kp1979_sign"]) for r in rows if tc[r["kp1979_sign"]] == 1 and r["icit_sign"] in li and r["kp1979_sign"] in lk)
        a = np.array([li[x] for x, _ in pairs]); b = np.array([lk[y] for _, y in pairs])
        obs = adjusted_rand_score(a, b)
        null = np.array([adjusted_rand_score(a, rng.permutation(b)) for _ in range(2000)])
        res[f"res{resol}|seed{seed}"] = {"ari": float(obs), "p": float((np.sum(null >= obs) + 1) / 2001)}
summary = {"min_ari": min(v["ari"] for v in res.values()), "max_ari": max(v["ari"] for v in res.values()),
           "max_p": max(v["p"] for v in res.values()), "runs": len(res)}
(ROOT / "results" / "review_r6_h93_robustness.json").write_text(json.dumps({"summary": summary, "runs": res}, indent=1))
print(summary)
for k, v in res.items(): print(k, round(v["ari"], 3), v["p"])
