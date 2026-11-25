"""Phase 2 baseline: descriptive structure of both corpora.

Outputs results/phase2_baseline.json and results/phase2_baseline.md.
Run: PYTHONPATH=src python scripts/phase2_baseline.py
"""
from __future__ import annotations

import collections
import json
import math
import pathlib
import random

import numpy as np

from indus.corpus import ROOT, load_icit, load_kp1979

OUT = ROOT / "results"
RNG = random.Random(20261125)


def H(counter: collections.Counter) -> float:
    n = sum(counter.values())
    return -sum(c / n * math.log2(c / n) for c in counter.values() if c)


def cond_entropy(seqs):
    """H(X_{i+1} | X_i) over within-line bigrams, with line boundary symbols."""
    big = collections.Counter()
    for s in seqs:
        s = ["<s>"] + s + ["</s>"]
        big.update(zip(s, s[1:]))
    left = collections.Counter()
    for (a, _), c in big.items():
        left[a] += c
    n = sum(big.values())
    return -sum(c / n * math.log2(c / left[a]) for (a, _), c in big.items())


def shuffle_within(seqs):
    out = []
    for s in seqs:
        s = s[:]
        RNG.shuffle(s)
        out.append(s)
    return out


def positional(seqs, min_count=10):
    """Initial / medial / final / solo counts and a final-vs-initial index."""
    pos = collections.defaultdict(lambda: collections.Counter())
    for s in seqs:
        if len(s) == 1:
            pos[s[0]]["solo"] += 1
            continue
        pos[s[0]]["initial"] += 1
        pos[s[-1]]["final"] += 1
        for t in s[1:-1]:
            pos[t]["medial"] += 1
    rows = []
    for sign, c in pos.items():
        tot = sum(c.values())
        if tot < min_count:
            continue
        rows.append({
            "sign": sign, "n": tot,
            "initial": c["initial"] / tot, "medial": c["medial"] / tot,
            "final": c["final"] / tot, "solo": c["solo"] / tot,
        })
    rows.sort(key=lambda r: -r["n"])
    return rows


def branching_boundaries(seqs, max_n=3):
    """Mean right-branching entropy after each n-gram; low values inside units.

    Returns the most frequent recurrent n-grams (2..4) with their counts and the
    number of distinct lines they occur in. Units that recur across many
    *different* lines are candidates for word-like segments.
    """
    grams = collections.Counter()
    lines_with = collections.defaultdict(set)
    for i, s in enumerate(seqs):
        for n in range(2, 5):
            for j in range(len(s) - n + 1):
                g = tuple(s[j:j + n])
                grams[g] += 1
                lines_with[g].add(tuple(s))
    rows = [{"ngram": " ".join(g), "n": len(g), "count": c,
             "distinct_lines": len(lines_with[g])}
            for g, c in grams.items() if len(lines_with[g]) >= 5]
    rows.sort(key=lambda r: (-r["distinct_lines"], -r["n"]))
    return rows[:60]


def summarise(name, lines):
    comp = [l.tokens for l in lines if l.complete and l.direction != "unknown"]
    uniq = sorted({tuple(s) for s in comp})
    uniq = [list(s) for s in uniq]
    toks = collections.Counter(t for s in uniq for t in s)
    lens = [len(s) for s in uniq]
    freqs = np.array(sorted(toks.values(), reverse=True), dtype=float)
    ranks = np.arange(1, len(freqs) + 1)
    slope = float(np.polyfit(np.log(ranks), np.log(freqs), 1)[0])
    ce = cond_entropy(uniq)
    shuf = [cond_entropy(shuffle_within(uniq)) for _ in range(20)]
    long_lines = [s for s in uniq if len(s) >= 3]
    ce_long = cond_entropy(long_lines)
    shuf_long = [cond_entropy(shuffle_within(long_lines)) for _ in range(20)]
    return {
        "corpus": name,
        "lines_total": len(lines),
        "lines_complete_known_direction": len(comp),
        "lines_unique": len(uniq),
        "duplicate_share": 1 - len(uniq) / max(1, len(comp)),
        "sign_types": len(toks),
        "tokens_unique_lines": int(sum(toks.values())),
        "hapax_types": sum(1 for c in toks.values() if c == 1),
        "types_lt5": sum(1 for c in toks.values() if c < 5),
        "length_median": float(np.median(lens)),
        "length_mean": float(np.mean(lens)),
        "length_max": int(max(lens)),
        "length_hist": dict(collections.Counter(lens)),
        "unigram_entropy_bits": H(toks),
        "zipf_slope": slope,
        "cond_entropy_bits": ce,
        "cond_entropy_within_shuffle_mean": float(np.mean(shuf)),
        "cond_entropy_within_shuffle_sd": float(np.std(shuf)),
        "cond_entropy_len3plus": ce_long,
        "cond_entropy_len3plus_shuffle_mean": float(np.mean(shuf_long)),
        "top_signs": toks.most_common(25),
        "positional": positional(uniq)[:40],
        "recurrent_ngrams": branching_boundaries(uniq),
    }


def md(res):
    out = ["# Phase 2 baseline statistics", "",
           "Generated file. Script: `scripts/phase2_baseline.py`.",
           "Unit of analysis: complete lines (both ends preserved, no damaged sign) with recorded direction; identical strings counted once.", ""]
    for r in res:
        out += [f"## Corpus `{r['corpus']}`", "",
                "| Item | Value |", "|---|---:|"]
        for k in ["lines_total", "lines_complete_known_direction", "lines_unique",
                  "duplicate_share", "sign_types", "tokens_unique_lines", "hapax_types",
                  "types_lt5", "length_median", "length_mean", "length_max",
                  "unigram_entropy_bits", "zipf_slope", "cond_entropy_bits",
                  "cond_entropy_within_shuffle_mean", "cond_entropy_len3plus",
                  "cond_entropy_len3plus_shuffle_mean"]:
            v = r[k]
            out.append(f"| {k} | {v:.3f} |" if isinstance(v, float) else f"| {k} | {v} |")
        out += ["", "### Positional distribution (40 most frequent signs)", "",
                "| Sign | n | Initial | Medial | Final | Solo |", "|---|---:|---:|---:|---:|---:|"]
        for p in r["positional"]:
            out.append(f"| {p['sign']} | {p['n']} | {p['initial']:.2f} | {p['medial']:.2f} | {p['final']:.2f} | {p['solo']:.2f} |")
        out += ["", "### n-grams recurring across lines (top 60 by number of distinct lines)", "",
                "| n-gram (reading order) | Length | Occurrences | Distinct lines |", "|---|---:|---:|---:|"]
        for g in r["recurrent_ngrams"]:
            out.append(f"| {g['ngram']} | {g['n']} | {g['count']} | {g['distinct_lines']} |")
        out.append("")
    return "\n".join(out)


def main():
    OUT.mkdir(exist_ok=True)
    res = [summarise("icit", load_icit()), summarise("kp1979", load_kp1979())]
    (OUT / "phase2_baseline.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    (OUT / "phase2_baseline.md").write_text(md(res))
    for r in res:
        print(r["corpus"], {k: r[k] for k in ["lines_unique", "sign_types", "hapax_types",
              "length_median", "zipf_slope", "cond_entropy_bits",
              "cond_entropy_within_shuffle_mean", "cond_entropy_len3plus",
              "cond_entropy_len3plus_shuffle_mean"]})


if __name__ == "__main__":
    main()
