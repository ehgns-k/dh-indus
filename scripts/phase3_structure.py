"""Phase 3: tests of pre-registered hypotheses H3.1 and H3.2 (docs/JOURNAL.md).

Only the training split (not `is_heldout`) is used.
Run: PYTHONPATH=src python scripts/phase3_structure.py
"""
from __future__ import annotations

import collections
import csv
import json
import random

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

from indus.corpus import ROOT, is_heldout, load_icit, load_kp1979

OUT = ROOT / "results"
SEED = 20261125
N_PERM = 1000


def train_lines(name):
    lines = load_icit() if name == "icit" else load_kp1979()
    u = sorted({tuple(l.tokens) for l in lines if l.complete and l.direction != "unknown"})
    return [list(s) for s in u if not is_heldout(list(s), name)]


def pos_shares(seqs):
    n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
    for s in seqs:
        for t in s:
            n[t] += 1
        if len(s) > 1:
            ini[s[0]] += 1
            fin[s[-1]] += 1
    return n, {t: ini[t] / n[t] for t in n}, {t: fin[t] / n[t] for t in n}


# ---------------------------------------------------------------- H3.1
def h31(seqs, rng):
    n, ini, fin = pos_shares(seqs)
    eligible = [t for t in n if n[t] >= 30]
    T = {t for t in eligible if fin[t] >= 0.6}
    pairs = [(s[i], s[i + 1]) for s in seqs for i in range(1, len(s) - 1)]

    def stat(group):
        a = [ini[b] for x, b in pairs if x in group]
        o = [ini[b] for x, b in pairs if x not in group]
        if not a or not o:
            return float("nan"), 0
        return float(np.mean(a) - np.mean(o)), len(a)

    obs, n_med = stat(T)
    null = []
    for _ in range(N_PERM):
        g = set(rng.sample(eligible, len(T)))
        null.append(stat(g)[0])
    null = np.array(null)
    p = float((np.sum(null >= obs) + 1) / (len(null) + 1))
    # descriptive: most common followers of medial T signs
    foll = collections.Counter(b for x, b in pairs if x in T)
    return {"terminal_signs": sorted(T, key=lambda t: -n[t]), "medial_occurrences": n_med,
            "observed_diff": obs, "null_mean": float(null.mean()), "null_sd": float(null.std()),
            "p_value": p, "top_followers": [(b, c, round(ini[b], 2)) for b, c in foll.most_common(10)]}


# ---------------------------------------------------------------- H3.2
def context_vectors(seqs, min_count=10, top_ctx=80):
    n = collections.Counter(t for s in seqs for t in s)
    signs = sorted([t for t in n if n[t] >= min_count], key=lambda t: -n[t])
    ctx_vocab = ["<s>", "</s>"] + [t for t, _ in n.most_common(top_ctx)]
    ci = {c: i for i, c in enumerate(ctx_vocab)}
    si = {t: i for i, t in enumerate(signs)}
    M = np.zeros((len(signs), 2 * len(ctx_vocab)))
    for s in seqs:
        ext = ["<s>"] + s + ["</s>"]
        for j in range(1, len(ext) - 1):
            t = ext[j]
            if t not in si:
                continue
            l, r = ext[j - 1], ext[j + 1]
            if l in ci:
                M[si[t], ci[l]] += 1
            if r in ci:
                M[si[t], len(ctx_vocab) + ci[r]] += 1
    # PPMI
    tot = M.sum()
    pr = M.sum(1, keepdims=True) / tot
    pc = M.sum(0, keepdims=True) / tot
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((M / tot) / (pr * pc))
    X = np.nan_to_num(np.maximum(pmi, 0))
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    return signs, X


def load_concordance(min_support=3, min_purity=0.8):
    rows = list(csv.DictReader(open(OUT / "phase1_concordance.tsv"), delimiter="\t"))
    good = [r for r in rows if int(r["support"]) >= min_support and float(r["purity"]) >= min_purity]
    targets = collections.Counter(r["kp1979_sign"] for r in good)
    return {r["icit_sign"]: r["kp1979_sign"] for r in good if targets[r["kp1979_sign"]] == 1}


def h32(icit, kp, rng, ks=(5, 6, 7, 8, 10, 12)):
    conc = load_concordance()
    si, Xi = context_vectors(icit)
    sk, Xk = context_vectors(kp)
    ki = {t: i for i, t in enumerate(sk)}
    shared = [(a, conc[a]) for a in si if a in conc and conc[a] in ki]
    ia = [si.index(a) for a, _ in shared]
    kb = [ki[b] for _, b in shared]
    out = {"shared_signs": len(shared), "by_k": {}}
    for k in ks:
        li = KMeans(k, n_init=20, random_state=SEED).fit_predict(Xi)
        lk = KMeans(k, n_init=20, random_state=SEED).fit_predict(Xk)
        a, b = li[ia], lk[kb]
        obs = adjusted_rand_score(a, b)
        null = np.array([adjusted_rand_score(a, rng.permutation(b)) for _ in range(N_PERM)])
        p = float((np.sum(null >= obs) + 1) / (N_PERM + 1))
        out["by_k"][k] = {"ari": float(obs), "null_mean": float(null.mean()),
                          "null_sd": float(null.std()), "p_value": p}
        if k == 8:
            clusters = collections.defaultdict(list)
            for (s, _), c in zip(shared, a):
                clusters[int(c)].append(s)
            out["icit_clusters_k8_shared"] = dict(clusters)
            full = collections.defaultdict(list)
            for s, c in zip(si, li):
                full[int(c)].append(s)
            out["icit_clusters_k8_all"] = dict(full)
    return out


def main():
    rng = random.Random(SEED)
    nrng = np.random.default_rng(SEED)
    icit, kp = train_lines("icit"), train_lines("kp1979")
    res = {"train_lines": {"icit": len(icit), "kp1979": len(kp)},
           "H3.1": {"icit": h31(icit, rng), "kp1979": h31(kp, rng)},
           "H3.2": h32(icit, kp, nrng)}
    (OUT / "phase3_structure.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in res.items() if k != "H3.2"}, indent=1, ensure_ascii=False)[:3000])
    print(json.dumps(res["H3.2"]["by_k"], indent=1), res["H3.2"]["shared_signs"])


if __name__ == "__main__":
    main()
