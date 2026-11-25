"""WP D1: place the Indus corpus among reference corpora of known function.
Pre-registered in docs/JOURNAL.md (2026-11-25, sixth working session).
Run: PYTHONPATH=src python scripts/phase4_d1_typology.py
"""
from __future__ import annotations

import collections
import json
import math
import random

import numpy as np

from indus.corpus import ROOT, load_icit
from indus.reference import load_reference

N_LINES, N_RES, N_CTRL = 2000, 20, 20
ADMIN = {"proto_elamite", "proto_cuneiform", "sumerian_ur3_admin"}
NONADMIN = {"sumerian_ob_literary", "akkadian_ob_letters"}


def length_targets(indus):
    h = collections.Counter(min(len(s), 13) for s in indus)
    tot = sum(h.values())
    return {k: round(N_LINES * v / tot) for k, v in h.items()}


def resample(lines, targets, rng):
    by = collections.defaultdict(list)
    for s in lines:
        if 1 <= len(s) <= 13:
            by[len(s)].append(s)
    out = []
    for k, n in targets.items():
        pool = by.get(k, [])
        out += rng.sample(pool, n) if len(pool) >= n else list(pool)
    return out


def bigram_model(train):
    big = collections.defaultdict(collections.Counter)
    V = {t for s in train for t in s} | {"</s>", "<unk>"}
    for s in train:
        e = ["<s>"] + s + ["</s>"]
        for x, y in zip(e, e[1:]):
            big[x][y] += 1
    tot = {x: sum(c.values()) for x, c in big.items()}
    nV = len(V)

    def ll(seq):
        e = ["<s>"] + seq + ["</s>"]
        return -sum(math.log((big[x][y] + 0.1) / (tot.get(x, 0) + 0.1 * nV)) for x, y in zip(e, e[1:])) / (len(e) - 1)
    return ll, big


def ctrl(seq, rng):
    head = seq[:-1]
    rng.shuffle(head)
    return head + seq[-1:]


def stats(sample, rng):
    sample = sample[:]
    rng.shuffle(sample)
    cut = int(0.8 * len(sample))
    tr, te = sample[:cut], [s for s in sample[cut:] if len(s) >= 2]
    ll, _ = bigram_model(tr)
    s1 = float(np.mean([ll(s[::-1]) - ll(s) for s in te]))
    n = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
    for s in tr:
        for t in s:
            n[t] += 1
        if len(s) > 1:
            ini[s[0]] += 1; fin[s[-1]] += 1
    zone = {t: (0 if ini[t] / n[t] >= 0.5 else 2 if fin[t] / n[t] >= 0.5 else 1) for t in n if n[t] >= 5}

    def inv(seqs):
        k = 0
        for s in seqs:
            z = [zone[t] for t in s if t in zone]
            k += sum(1 for i in range(len(z)) for j in range(i + 1, len(z)) if z[i] > z[j])
        return k
    lines_with = collections.defaultdict(set)
    for i, s in enumerate(tr):
        for k in (2, 3):
            for j in range(len(s) - k + 1):
                lines_with[tuple(s[j:j + k])].add(i)
    units = {g for g, ls in lines_with.items() if len(ls) >= 3}

    def cov(seqs):
        c = 0
        for s in seqs:
            cv = set()
            for k in (2, 3):
                for j in range(len(s) - k + 1):
                    if tuple(s[j:j + k]) in units:
                        cv.update(range(j, j + k - 1))
            c += len(cv)
        return c
    ci = [inv([ctrl(s, rng) for s in te]) for _ in range(N_CTRL)]
    cc = [cov([ctrl(s, rng) for s in te]) for _ in range(N_CTRL)]
    s2 = 1 - inv(te) / np.mean(ci) if np.mean(ci) > 0 else 0.0
    s3 = cov(te) / np.mean(cc) if np.mean(cc) > 0 else float("nan")
    multi = [s for s in sample if len(s) >= 2]
    s4 = float(np.mean([len(set(s)) < len(s) for s in multi]))
    types = collections.Counter(t for s in sample for t in s)
    s5 = sum(1 for c in types.values() if c == 1) / len(types)
    f = collections.Counter(s[-1] for s in multi)
    s6 = sum(c for _, c in f.most_common(3)) / len(multi)
    return [s1, float(s2), float(s3), s4, s5, s6]


def synthetic(indus, targets, rng):
    _, big = bigram_model(indus)
    out = []
    for k, n in targets.items():
        made = 0
        while made < n:
            s, prev = [], "<s>"
            while len(s) < k:
                c = big[prev]
                opts = [t for t in c if t != "</s>"]
                if not opts:
                    break
                t = rng.choices(opts, weights=[c[o] for o in opts])[0]
                s.append(t); prev = t
            if len(s) == k:
                out.append(s); made += 1
    return out


def main():
    rng = random.Random(20261125)
    indus = sorted({tuple(l.tokens) for l in load_icit() if l.complete and l.direction != "unknown"})
    indus = [list(s) for s in indus]
    targets = length_targets(indus)
    refs = {k: sorted({tuple(s) for s in v}) for k, v in load_reference().items()}
    refs = {k: [list(s) for s in v] for k, v in refs.items()}
    corpora = {"indus_icit": indus, **refs}
    names = ["S1_direction", "S2_template", "S3_units", "S4_repetition", "S5_hapax", "S6_final_conc"]
    vals = collections.defaultdict(list)
    for r in range(N_RES):
        for k, lines in corpora.items():
            vals[k].append(stats(resample(lines, targets, rng), rng))
        vals["synthetic_bigram"].append(stats(synthetic(indus, targets, rng), rng))
        print("resample", r + 1, flush=True)
    real = list(corpora)
    arr = {k: np.array(v) for k, v in vals.items()}
    means = np.array([arr[k].mean(0) for k in real])
    mu, sd = means.mean(0), means.std(0)
    wins = 0
    dists = []
    for r in range(N_RES):
        z = {k: (arr[k][r] - mu) / sd for k in arr}
        d = {k: float(np.linalg.norm(z["indus_icit"] - z[k])) for k in arr if k != "indus_icit"}
        dists.append(d)
        wins += min(d[k] for k in ADMIN) < min(d[k] for k in NONADMIN)
    res = {"statistics": names,
           "means": {k: dict(zip(names, map(float, arr[k].mean(0)))) for k in arr},
           "sds": {k: dict(zip(names, map(float, arr[k].std(0)))) for k in arr},
           "mean_distance_to_indus": {k: float(np.mean([d[k] for d in dists])) for k in dists[0]},
           "D1_admin_closer_count": wins, "D1_supported": wins >= 19,
           "sample_sizes": {k: len(resample(v, targets, random.Random(0))) for k, v in corpora.items()}}
    (ROOT / "results" / "phase4_d1_typology.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
