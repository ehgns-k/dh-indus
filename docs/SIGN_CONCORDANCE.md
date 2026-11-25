# Sign-number concordance (ICIT-style ↔ KP1979)

The two corpora use different sign-numbering systems. Since both sources largely transcribe the same objects, identical texts were located in both and aligned, and the sign correspondences were estimated from that alignment.

- Script: `scripts/phase1_concordance.py`
- Full table: `results/phase1_concordance.tsv`
- Summary: `results/phase1_concordance.md`

## Method

1. Lines of equal length are aligned position by position. An EM procedure, in which the KP line corresponding to each ICIT line (or the absence of one) is a latent variable, yields a table of sign-correspondence probabilities.
2. Starting from this table, only line pairs whose positional agreement is above a threshold (0.75, lowered to 0.67) and that have a unique best partner are treated as the same text, and the correspondences are recomputed.

A first attempt paired the 60 most frequent signs by frequency and positional distribution alone and then ran the same procedure. It aligned only 25 line pairs and was discarded.

## Results (2026-11-25)

- 929 aligned line pairs, of which 594 agree at every position.
- Correspondences with support ≥ 3 and purity ≥ 0.8: 167 ICIT signs.
- Some correspondences are not one-to-one. For example, ICIT 740 corresponds to both KP 325 (352 times) and KP 324 (131 times). Conversely, ICIT 390, 405, 406 and 407 all correspond to KP 86. In such cases one system splits what the other merges, which means the two sign lists draw allograph boundaries differently. These cases are candidates for the allograph review in phase 3.

## Limitations

- Readings of different length (where one source reads one sign more or fewer) were not aligned.
- Rare signs have little support, so their correspondences are uncertain.

## Allograph test of KP-merged signs (L3a, 2026-11-25)

Of ten pairs of frequent ICIT signs that KP1979 merges into one sign, three differ significantly in context and are treated as distinct signs: 617/741 (KP 325), 151/158 (KP 1), 390/407 (KP 86). The other seven pairs show no detectable difference and are consistent with allographs. See `docs/JOURNAL.md` (L3a) and `results/phase3_l3a_allographs.json`.

## Split strokes (2026-11-25)

KP1979 often writes a pair of single strokes as two signs (121/144 + 121/144) where the ICIT-style source writes one two-stroke sign (032). See `results/phase3_split_merge.json`.
