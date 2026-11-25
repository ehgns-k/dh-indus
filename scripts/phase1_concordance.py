"""Phase 1: infer a sign-number concordance between the ICIT-style
transcription and the Koskenniemi & Parpola (1979) corpus.

Neither source gives a mapping between its sign numbers and the other's.
Because both corpora transcribe largely the same objects, identical texts
should appear in both. The procedure is:

1. Seed: soft EM alignment of same-length lines (each ICIT line may align
   to any KP line of the same length, or to none), giving a translation
   table. (A first attempt seeding by frequency/position profiles with the
   Hungarian algorithm aligned only 25 pairs and was dropped; `seed`.)
2. Align: for every pair of same-length unique lines (ICIT, KP), count how
   many positions agree under the current mapping. Pairs with agreement
   >= threshold and a unique best partner are taken as the same text.
3. Update: each ICIT sign is mapped to the KP sign it is most often aligned
   with (minimum support 2). Repeat 2-3 until the mapping is stable.

The mapping is many-to-one in general (allographs may be split in one
system and merged in the other). Output: results/phase1_concordance.tsv
and results/phase1_concordance.md.
"""
from __future__ import annotations

import collections
import math

import numpy as np
from scipy.optimize import linear_sum_assignment

from indus.corpus import ROOT, load_icit, load_kp1979

OUT = ROOT / "results"


def uniq_lines(lines):
    return sorted({tuple(l.tokens) for l in lines if l.complete and l.direction != "unknown"})


def profile(seqs):
    cnt = collections.Counter()
    pos = collections.defaultdict(lambda: np.zeros(3))
    for s in seqs:
        for i, t in enumerate(s):
            cnt[t] += 1
            k = 0 if i == 0 else (2 if i == len(s) - 1 else 1)
            pos[t][k] += 1
    return cnt, pos


def seed(icit, kp, top=60):
    ci, pi = profile(icit)
    ck, pk = profile(kp)
    a = [s for s, _ in ci.most_common(top)]
    b = [s for s, _ in ck.most_common(top)]
    def vec(c, p, s):
        v = p[s] / p[s].sum()
        return np.r_[math.log(c[s]), 3 * v]
    A = np.array([vec(ci, pi, s) for s in a])
    B = np.array([vec(ck, pk, s) for s in b])
    cost = ((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)
    r, c = linear_sum_assignment(cost)
    return {a[i]: b[j] for i, j in zip(r, c)}


def em_seed(icit, kp, iters=15, min_len=3):
    """Soft monotone alignment of same-length lines (EM, IBM-1 style without
    reordering). Returns the arg-max translation table as a dict."""
    icit = [s for s in icit if "?" not in s]
    kp = [s for s in kp if "?" not in s]
    si = sorted({t for s in icit for t in s}); sk = sorted({t for s in kp for t in s})
    ii = {t: n for n, t in enumerate(si)}; kk = {t: n for n, t in enumerate(sk)}
    by_i = collections.defaultdict(list); by_k = collections.defaultdict(list)
    for s in icit:
        if len(s) >= min_len:
            by_i[len(s)].append([ii[t] for t in s])
    for s in kp:
        if len(s) >= min_len:
            by_k[len(s)].append([kk[t] for t in s])
    T = np.full((len(si), len(sk)), 1.0 / len(sk))
    for _ in range(iters):
        C = np.full_like(T, 1e-3)
        logT = np.log(T)
        for L, A in by_i.items():
            if L not in by_k:
                continue
            A = np.array(A); B = np.array(by_k[L])
            S = np.zeros((len(A), len(B)))
            for p in range(L):
                S += logT[A[:, p]][:, B[:, p]]
            base = L * math.log(1.0 / len(sk)) + 3.0  # "no counterpart" option
            M = np.maximum(S.max(1, keepdims=True), base)
            W = np.exp(S - M)
            W = W / (W.sum(1, keepdims=True) + np.exp(base - M))
            for p in range(L):
                np.add.at(C, (np.repeat(A[:, p][:, None], len(B), 1),
                              np.repeat(B[:, p][None, :], len(A), 0)), W)
        T = C / C.sum(1, keepdims=True)
    best = T.argmax(1)
    return {si[i]: sk[best[i]] for i in range(len(si)) if T[i, best[i]] > 0.2}


def align(icit, kp, mapping, thr=0.75, min_len=3):
    by_len = collections.defaultdict(list)
    for s in kp:
        if len(s) >= min_len:
            by_len[len(s)].append(s)
    pairs = []
    for s in icit:
        if len(s) < min_len or len(s) not in by_len:
            continue
        cand = by_len[len(s)]
        mapped = [mapping.get(t) for t in s]
        scores = np.array([sum(m == k for m, k in zip(mapped, c)) for c in cand]) / len(s)
        best = scores.argmax()
        if scores[best] >= thr and (scores == scores[best]).sum() == 1:
            pairs.append((s, cand[best], float(scores[best])))
    return pairs


def update(pairs, min_support=2):
    co = collections.defaultdict(collections.Counter)
    for s, k, _ in pairs:
        for a, b in zip(s, k):
            co[a][b] += 1
    new = {}
    for a, c in co.items():
        b, n = c.most_common(1)[0]
        if n >= min_support and n / sum(c.values()) >= 0.5:
            new[a] = b
    return new, co


def main():
    icit = uniq_lines(load_icit())
    kp = uniq_lines(load_kp1979())
    mapping = em_seed(icit, kp)
    history = []
    # anneal threshold: start strict so only near-identical texts drive updates
    for it, thr in enumerate([0.75, 0.75, 0.7, 0.7, 0.67, 0.67, 0.67, 0.67]):
        pairs = align(icit, kp, mapping, thr=thr)
        new, co = update(pairs)
        merged = {**mapping, **new}
        changed = sum(merged.get(k) != mapping.get(k) for k in merged)
        history.append((it, thr, len(pairs), len(new), changed))
        print(f"iter {it} thr {thr}: aligned pairs {len(pairs)}, mapped signs {len(new)}, changed {changed}")
        mapping = merged
        if changed == 0 and it > 3:
            break
    pairs = align(icit, kp, mapping, thr=0.67)
    new, co = update(pairs, min_support=1)
    exact = sum(1 for _, _, sc in pairs if sc == 1.0)
    rows = []
    for a, c in sorted(co.items(), key=lambda kv: -sum(kv[1].values())):
        tot = sum(c.values())
        b, n = c.most_common(1)[0]
        rows.append((a, b, n, tot, n / tot, ";".join(f"{x}:{y}" for x, y in c.most_common(4))))
    with open(OUT / "phase1_concordance.tsv", "w") as f:
        f.write("icit_sign\tkp1979_sign\tsupport\taligned_total\tpurity\talternatives\n")
        for r in rows:
            f.write("\t".join(map(str, r[:4])) + f"\t{r[4]:.2f}\t{r[5]}\n")
    # many-to-one structure
    inv = collections.defaultdict(list)
    for r in rows:
        if r[2] >= 3 and r[4] >= 0.8:
            inv[r[1]].append(r[0])
    lines = ["# Phase 1 sign-number concordance (ICIT-style ↔ KP1979)", "",
             "Generated file. Script: `scripts/phase1_concordance.py`.", "",
             "## Iterations", "", "| Iteration | Agreement threshold | Aligned line pairs | Mapped signs | Changed mappings |", "|---:|---:|---:|---:|---:|"]
    lines += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in history]
    lines += ["", f"Final aligned line pairs: {len(pairs)} (of which exact matches: {exact}).",
              f"ICIT signs occurring in the alignment: {len(rows)}; with support >= 3 and purity >= 0.8: {sum(1 for r in rows if r[2] >= 3 and r[4] >= 0.8)}.", "",
              "## Several ICIT signs mapped to one KP1979 sign (allograph candidates)", "",
              "| KP1979 | ICIT signs |", "|---|---|"]
    lines += [f"| {k} | {', '.join(v)} |" for k, v in sorted(inv.items(), key=lambda kv: -len(kv[1])) if len(v) > 1]
    lines += ["", "## Concordance (top 80 by support)", "", "| ICIT | KP1979 | Support | Aligned total | Purity | Alternatives |", "|---|---|---:|---:|---:|---|"]
    lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.2f} | {r[5]} |" for r in rows[:80]]
    (OUT / "phase1_concordance.md").write_text("\n".join(lines) + "\n")
    print("final pairs", len(pairs), "exact", exact)


if __name__ == "__main__":
    main()
