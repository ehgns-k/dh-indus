# Research log

New entries are appended below. Each entry gives the date, the work done, the results, and the next steps.

---

## 2026-11-25 (day 1)

### Work done

1. Set up the repository and wrote the research phases and success criteria (`ROADMAP.md`, `docs/METHOD.md`).
2. Obtained two public corpora at pinned versions (`data/sources.tsv`).
   - ICIT-style secondary transcription: 5,679 records, with find site, object type and writing direction.
   - Machine reading of Koskenniemi & Parpola (1979): 4,066 inscriptions.
3. Wrote the normalisation module (`src/indus/corpus.py`).
4. Computed baseline statistics (`scripts/phase2_baseline.py` → `results/phase2_baseline.md`).
5. Defined the held-out set: texts whose SHA-256 value modulo 5 equals 0 (about 20 %). Identical strings always fall on the same side (`is_heldout`).

### Checking the reading order

I checked the direction in which the `text` column of the ICIT-style transcription is stored. Sign 740 is the most frequent sign in this source. Taking the stored order at face value, 740 most often comes first both in lines recorded as `R/L` and in lines recorded as `L/R` (`R/L`: first position 914 times; `L/R`: first position 40 times; counted in storage order). I therefore concluded that the column is stored in a single normalised orientation regardless of the recorded direction, and reversed all lines into reading order. After reversal, 740 most often comes last in both directions.

The Koskenniemi & Parpola (1979) reading is documented as having the rightmost sign as its first token (upstream repository, `digitized/README.md`). The most frequent sign in this source, 325, is also concentrated in final position (final 444 times, initial 22 times). The direction handling of the two sources is consistent.

### Summary of results

| Item | ICIT-style | KP1979 |
|---|---:|---:|
| Complete, deduplicated lines | 2,059 | 2,123 |
| Sign types | 607 | 367 |
| Signs occurring once | 214 | 100 |
| Median line length | 4 | 4 |
| Conditional entropy H(next sign \| current sign), bits | 3.77 | 3.88 |
| Same, mean over within-line shuffles | 4.77 | 4.91 |

Shuffling the order of signs within a line raises the conditional entropy by about 1 bit. This shows only that sign order is rule-governed; it is not evidence that the system records language. It has been argued that non-linguistic symbol systems can also have ordering rules (bibliography section C).

Signs with a strong preference for final position (ICIT numbers): 740 (final share 0.72), 400 (0.88), 520 (0.84), 090 (0.76), 151 (0.87). Signs with a strong preference for initial position: 817 (0.88), 820 (0.75), 861 (0.71), 920 (0.65). Signs almost confined to medial position: 002 (0.95), 060 (0.96), 100 (0.95), 760 (0.97).

### Limitations

- The baseline statistics were computed on the whole data set before the held-out set was defined. They are descriptive statistics and are not used for hypothesis tests. Later hypotheses are formed without the held-out data.
- The number of sign types in the ICIT-style source (607) is larger than in the classical sign lists. Allographs or ligatures may have received separate numbers.
- According to the upstream description, the KP1979 reading has not been fully proofread.

### Next steps

1. Build a sign-number concordance between the two corpora (by locating and aligning the same inscriptions in both).
2. Complete the verified bibliography and write the register of earlier claims.
3. Phase 3 structural analysis: segmentation, distributional clustering, numeral system.

### Addendum: sign-number concordance (same day)

The sign-number correspondence between the two corpora was estimated by text alignment (`docs/SIGN_CONCORDANCE.md`). Of 929 aligned line pairs, 594 agree at every position. Cases were found where the two sign lists draw allograph boundaries differently, for example ICIT 740 corresponding to both KP 325 and 324, and ICIT 390, 405, 406 and 407 all corresponding to KP 86. With this concordance, later structural results can be compared directly between the two corpora.

### Pre-registration of phase 3 hypotheses (same day, written before analysis)

The analyses use only the training data (about 80 %), excluding the held-out set.

**H3.1 (terminal signs mark boundaries).** Signs concentrated at line end (ICIT 740, 400, 520 and others; defined as signs with a final share ≥ 0.6 and ≥ 30 occurrences in the training data) mark the end of a unit within the text.
- Prediction: when such a sign occurs line-medially, the mean "initial share" of the next sign (the proportion of that sign's occurrences that are line-initial) is higher than the mean for signs following other medial signs.
- Control: permutation test with random sign labels (1,000 permutations). Significance level 0.01.
- Replication: tested independently in KP1979 with the same definition.
- Refutation condition: if p ≥ 0.01 in either corpus, H3.1 is recorded as not supported.

**H3.2 (reproducibility of distributional sign classes).** If signs are represented by the distribution of their neighbouring signs and clustered, the cluster structure reflects real structure independent of the transcription system.
- Prediction: when the clusters obtained from ICIT are transferred to KP signs through the concordance, their agreement (adjusted Rand index, ARI) with clusters obtained independently from KP is higher than with randomly permuted cluster labels.
- Control: 1,000 label permutations. Significance level 0.01.
- Refutation condition: if p ≥ 0.01 or ARI < 0.1, recorded as not supported.

### Phase 3 results: H3.1, H3.2 (same day)

Script: `scripts/phase3_structure.py`; results: `results/phase3_structure.json`. Training lines: ICIT 1,663, KP1979 1,692.

**H3.1: not supported (in both corpora).**

| Corpus | Terminal sign set | Medial occurrences | Observed difference | Permutation mean (SD) | p |
|---|---|---:|---:|---:|---:|
| ICIT | 740, 400, 520, 090, 151, 407, 527, 156 | 295 | −0.044 | 0.003 (0.040) | 0.91 |
| KP1979 | 324, 98, 217, 326, 1, 13, 4, 301 | 229 | −0.011 | −0.003 (0.035) | 0.54 |

When a terminal sign occurs line-medially, the next sign is not an initial sign of a new unit. The most frequent next sign is in fact another terminal sign (ICIT: 400 follows 740 86 times, 090 61 times; KP1979: 98 64 times, 13 31 times). In the concordance, ICIT 400 corresponds to KP 98, so the tendency is the same in both corpora.

Interpretation: the signs preferring final position appear to form a single "terminal cluster" in which two or more of them are joined at line end, rather than marking word boundaries. This must be registered as a new hypothesis (H3.3) and tested on held-out data; for now it is only a post hoc observation.

**H3.2: partly supported (the number of clusters k was not fixed in advance).**

The clusters of the two corpora were compared on the 58 shared signs linked by the concordance (1,000 permutations; the smallest attainable p is 0.001).

| k | ARI | Permutation mean | p |
|---:|---:|---:|---:|
| 5 | 0.102 | 0.001 | 0.002 |
| 6 | 0.053 | 0.001 | 0.033 |
| 7 | 0.095 | 0.000 | 0.003 |
| 8 | 0.241 | 0.001 | 0.001 |
| 10 | 0.119 | 0.000 | 0.001 |
| 12 | 0.128 | 0.000 | 0.002 |

Because k was not fixed at pre-registration, all six values are reported. With a correction for six comparisons (Bonferroni, 0.01/6 ≈ 0.0017), only k = 8 and 10 pass; the additional condition ARI ≥ 0.1 is also met by both. For most values of k, the distributional classes agree between the two transcription systems more than by chance, but the agreement is low to moderate. Conclusion: weak evidence that the sign classes have real structure. It is too early to say that the L1 criteria are met.

### Bibliography

Wrote `docs/BIBLIOGRAPHY.md`: 62 verified entries, 5 unverified. Corrections made during verification:
- The authors of Luo et al. (2021, TACL) are Luo, Hartmann, Santus, Barzilay and Cao.
- The 2015 monograph associated with the ICIT database is Wells, *The Archaeology and Epigraphy of Indus Writing* (Archaeopress).
- Fuls, *Catalog of Indus Signs* (2023) and *Corpus of Indus Inscriptions* (2022) exist.

### Next steps

1. Pre-register H3.3: internal order of the terminal cluster (for example, whether the order 740 then 400 is fixed).
2. Write the register of earlier claims, `docs/CLAIMS_REGISTER.md`.
3. Numeral candidates: detect series of signs that substitute for one another in the same context.
4. Phase 4: obtain control data from non-linguistic symbol systems (bibliography sections C and D).

### Pre-registration of H3.3 (same day, before inspecting the held-out data)

**H3.3 (fixed order within the terminal cluster).** When two signs of the terminal set defined in H3.1 are adjacent, their order is fixed.
- Procedure: for each pair {a, b} of adjacent terminal signs in the training data, determine the dominant order. In the held-out data, count the proportion of occurrences of the same pair that follow the dominant training order.
- Prediction: agreement ≥ 0.8, binomial test (null probability 0.5) p < 0.01, in both corpora.
- Refutation condition: agreement < 0.8 or p ≥ 0.01 in either corpus.

### H3.3 result: supported (held-out data, both corpora)

Script: `scripts/phase3_h33_heldout.py`; results: `results/phase3_h33_heldout.json`.

| Corpus | Held-out pairs | Agreeing with dominant training order | Proportion | Binomial p |
|---|---:|---:|---:|---:|
| ICIT | 38 | 37 | 0.97 | 1.4 × 10⁻¹⁰ |
| KP1979 | 34 | 31 | 0.91 | 3.8 × 10⁻⁷ |

Main orders in the training data: ICIT 740 > 400 (65 times), 740 > 090 (62 times); KP1979 324 > 13 (27 times), 324 > 98 (23 times). In the concordance ICIT 090 ↔ KP 13, ICIT 400 ↔ KP 98 and ICIT 740 ↔ KP 324/325, so the two corpora show the same ordering rule. In reading order, 740 comes first, followed by 400 or 090, which ends the line.

Verdict: H3.3 meets its pre-registered criteria. The following limitations are recorded with it.
- The two corpora largely transcribe the same objects, so replication across them is replication across independent transcriptions, not across independent samples.
- Most agreeing pairs are the two pairs 740 > 400 and 740 > 090. The result is therefore closer to a fixed arrangement of a few signs than to a rule for "terminal signs in general".
- A fixed order is compatible both with the morpheme order of a language (for example the order of suffixes after a stem) and with a non-linguistic notational convention (for example a fixed arrangement of titles or unit markers). This result alone cannot distinguish the two.

Measured against the L1 criteria of the ROADMAP, H3.3 is the first case of "a structural result reproduced in two transcriptions and significant against a control model". Because of the independence limitation above, it will be recorded as meeting L1 only after a re-test with the data divided by find site (for example Harappa and Mohenjo-daro).

### Next steps (updated)

1. Re-test H3.3 by find site (Harappa / Mohenjo-daro / other), using the ICIT metadata.
2. Test whether the terminal cluster differs by object type (seal, tablet, pottery).
3. Write the register of earlier claims, `docs/CLAIMS_REGISTER.md`.
4. Numeral candidate analysis.

### Pre-registration of H3.4 (same day)

**H3.4 (replication across find sites).** The ordering rule of H3.3 is the same at different find sites.
- Procedure: use all ICIT data (training and held-out), assigning a find site to each text string (strings found at more than one site are excluded). Predict the Mohenjo-daro data from the dominant orders of the Harappa data, and the reverse.
- Prediction: agreement ≥ 0.8 and binomial p < 0.01 in both directions.

### H3.4 result: supported

Script: `scripts/phase3_h34_sites.py`; results: `results/phase3_h34_sites.json`.

| Training site → predicted site | Pairs | Agreeing | Proportion | Binomial p |
|---|---:|---:|---:|---:|
| Harappa → Mohenjo-daro | 69 | 63 | 0.91 | 2.2 × 10⁻¹³ |
| Mohenjo-daro → Harappa | 98 | 96 | 0.98 | 1.5 × 10⁻²⁶ |
| (additional, not pre-registered) Harappa + Mohenjo-daro → other sites | 21 | 17 | 0.81 | 0.0036 |

Verdict: H3.4 meets its pre-registered criteria. The ordering rule of the terminal cluster is the same in material from the two large cities.

### L1 verdict (2026-11-25)

The fixed order of the terminal cluster (H3.3, H3.4) meets the L1 conditions of the ROADMAP: (a) reproduced in both corpora and (b) p < 0.01 against a control model. It is therefore recorded as **the first L1 (structural partial decipherment) result**. Its scope is narrow: it is an ordering rule for three signs, ICIT 740, 400 and 090 (KP 324/325, 98 and 13), and says nothing about their meaning or sound values.

### Language of the repository (same day)

From this point all repository content (documents, code comments, generated reports and commit messages) is written in English. Earlier Korean documents were translated; their content was not changed.

## 2026-11-25 (day 1, continued)

### Object type and find site are confounded

Counts of complete lines with recorded direction in the ICIT-style source, by coarse object type (prefix of the `type` field) and site: tablet types `TAB:B` (Harappa 631, Mohenjo-daro 83) and `TAB:I` (Harappa 542, Mohenjo-daro 8) come mostly from Harappa, `TAB:C` (Mohenjo-daro 175) almost only from Mohenjo-daro, while seals (`SEAL*`) are frequent at both (Harappa 274, Mohenjo-daro 1,003). Any test of text against object type must therefore control for site; otherwise a classifier could learn site-specific vocabulary instead of object-specific text.

### Pre-registration of H3.5 (before running the test)

**H3.5 (seal texts and tablet texts differ in a way that transfers across sites).** The sign content of a text distinguishes seals from tablets, and the distinction learned at one site holds at another.
- Unit: unique text strings with a single coarse object type, either `SEAL*` or `TAB*`.
- Training: Harappa strings outside the held-out set.
- Test: Mohenjo-daro strings that do not also occur at Harappa (primary); Mohenjo-daro held-out strings only (secondary).
- Model: logistic regression on sign counts, initial sign, final sign and line length (fixed before the test; no tuning).
- Metric: balanced accuracy (mean of per-class recall), because the classes are unbalanced.
- Control: the same model trained on randomly permuted training labels (200 permutations).
- Prediction: balanced accuracy ≥ 0.65 and permutation p < 0.01 on the primary test set.
- Refutation condition: balanced accuracy < 0.65 or p ≥ 0.01.
- If supported, the most informative features will be listed as candidates for L2 (semantic-category) hypotheses. They are not by themselves an L2 result.

### H3.5 result: not supported

Script: `scripts/phase3_h35_objecttype.py`; results: `results/phase3_h35_objecttype.json`.

| Test set | Seal | Tablet | Balanced accuracy |
|---|---:|---:|---:|
| Mohenjo-daro, strings not found at Harappa (primary) | 882 | 96 | 0.555 |
| Mohenjo-daro, held-out strings only (secondary) | 173 | 22 | 0.568 |

Permutation control (200): mean 0.501, SD 0.039; p = 0.080. Both pre-registered conditions fail (balanced accuracy < 0.65, p ≥ 0.01). A model trained at Harappa does not separate seal texts from tablet texts at Mohenjo-daro.

### Exploratory follow-up (not pre-registered)

Script: `scripts/phase3_h35_explore_within_site.py`; results: `results/phase3_h35_explore_within_site.json`.

Within Harappa alone (train on non-held-out strings, test on Harappa held-out strings: 42 seal, 73 tablet), the same model reaches balanced accuracy 0.79 (permutation mean 0.50, p = 0.005, the smallest value attainable with 200 permutations). Seal and tablet texts therefore do differ at Harappa, but the difference does not carry over to Mohenjo-daro.

One possible reason is that "tablet" covers different subtypes at the two sites: Harappa tablets are `TAB:B` (631 lines) and `TAB:I` (542), whereas Mohenjo-daro tablets are mostly `TAB:C` (175) with some `TAB:B` (83). Since this explanation was formed after seeing the result, it is tested separately below as H3.6.

### Pre-registration of H3.6 (before running)

**H3.6 (seal vs `TAB:B` transfers across sites).** Restricting tablets to the one subtype that is common at both sites, `TAB:B`, a model trained at Harappa separates seal texts from `TAB:B` texts at Mohenjo-daro.
- Same unit, features, model, metric and control as H3.5, with the tablet class limited to `TAB:B` at both sites.
- Prediction: balanced accuracy ≥ 0.65 and permutation p < 0.01 on Mohenjo-daro strings not found at Harappa.
- Refutation condition: either condition fails.

### H3.6 result: supported, narrowly

Script: `scripts/phase3_h36_tabB.py`; results: `results/phase3_h36_tabB.json`.

Training (Harappa, non-held-out): 178 seal, 176 `TAB:B`. Test (Mohenjo-daro strings not found at Harappa): 882 seal, 41 `TAB:B`. Balanced accuracy 0.667; permutation mean 0.503 (SD 0.046); p = 0.005.

Verdict: both pre-registered conditions are met (0.667 ≥ 0.65; p < 0.01). The margin is small, and the following must be recorded:
- H3.6 was formed after H3.5 failed, so two tests of the same question were run. With a Bonferroni correction for two tests (0.01/2 = 0.005), p = 0.00498 passes only just, and it is the smallest value attainable with 200 permutations.
- The test set contains only 41 `TAB:B` strings.

The features with the largest weights (descriptive, from the training data) are: for `TAB:B`, final sign 700 (+1.32), final sign 400 (+1.32), sign 700 anywhere (+1.26), final sign 032 (+1.17); for seals, length ≥ 8 (−1.12), sign 003 (−1.04), sign 900 (−0.94), final sign 090 (−0.75).

This links to H3.3. The terminal cluster has two common forms, 740 > 400 and 740 > 090. The weights suggest that lines ending in 400 belong to tablets and lines ending in 090 belong to seals. This is tested on held-out data as H3.7.

### Pre-registration of H3.7 (before running)

**H3.7 (the two forms of the terminal cluster are tied to object type).** Among lines ending in 400 and lines ending in 090, the share of seals is higher for lines ending in 090.
- Unit: unique strings in the ICIT held-out set (all sites), with a single coarse object type (`SEAL*` vs any `TAB*`), ending in 400 or in 090.
- Test: one-sided Fisher exact test on the 2 × 2 table (final sign × object type).
- Replication: the same test in KP1979 is not possible, because that source carries no object-type field in a form decoded here; this is recorded as a limitation.
- Prediction: seal share higher for 090-final lines, p < 0.01.
- Refutation condition: p ≥ 0.01, or seal share not higher for 090-final lines.

### H3.7 result: not supported

Script: `scripts/phase3_h37_terminal_objecttype.py`; results: `results/phase3_h37_terminal_objecttype.json`.

| Final sign | Seal | Tablet | Seal share |
|---|---:|---:|---:|
| 090 | 6 | 3 | 0.67 |
| 400 | 9 | 30 | 0.23 |

One-sided Fisher exact test: odds ratio 6.7, p = 0.018. The direction is the predicted one, but p ≥ 0.01, so by the pre-registered rule H3.7 is not supported. The held-out set contains only 48 qualifying strings, so the test has little power.

The table is also confounded by site: 27 of the 30 tablets ending in 400 are from Harappa, while all 9 seals ending in 400 are from Mohenjo-daro. The test cannot separate an object-type effect from a site effect.

The held-out set has now been used for this question. A further test of the same question would need new data (for example a third corpus or newly published inscriptions), not a re-use of these strings.

### Summary of day 1 tests

| Hypothesis | Pre-registered | Result |
|---|---|---|
| H3.1 terminal signs mark unit boundaries | yes | not supported |
| H3.2 distributional classes agree across transcriptions | yes (k not fixed) | partly supported |
| H3.3 fixed order in the terminal cluster | yes | supported |
| H3.4 the same order at different sites | yes | supported |
| H3.5 seal vs tablet texts transfer across sites | yes | not supported |
| H3.6 seal vs `TAB:B` transfers across sites | yes (formed after H3.5) | supported, narrowly |
| H3.7 090-final vs 400-final tied to object type | yes | not supported (p = 0.018) |

### Stroke signs: identification from the printed sign list

The sign list of Koskenniemi & Parpola (1979), printed page [19] (page 20 of the scanned PDF in the upstream repository), shows each sign's glyph. Counting the strokes in the printed glyphs (my own reading of the scan, not a statement of the authors):
- Signs 121–130 are short vertical strokes, written in one row or in two stacked rows. The stroke counts read from the glyphs are 1 (121), 2 (122), 3 (123), 4 (124), 5 (125), 6 (126), 7 (127), 8 (128), 9 (129) and 10 (130, five over five).
- Signs 144–151 are long vertical strokes. The counts read from the glyphs are 1 (144), 2 (145), 3 (147), 4 (150) and 5 (151); 146, 148 and 149 carry additional marks.

Frequencies in KP1979 (all lines): 121: 605, 122: 49, 123: 322, 124: 127, 125: 60, 126: 45, 127: 98, 128: 5, 129: 3, 130: 1; 144: 446, 145: 102, 147: 231, 150: 24, 151: 31.

Concordance images in the ICIT-style numbering (support ≥ 3, purity ≥ 0.8): 121 → 001, 123 → 003, 124 → 004 and 034, 125 → 005, 126 → 016, 127 → 017, 151 → 035. The low ICIT numbers for the short-stroke signs agree with the stroke counts for 1, 3, 4 and 5, which is independent support for reading these glyphs as a counted series.

### Pre-registration of H3.8 (before running)

**H3.8 (short-stroke signs form one distributional paradigm).** If the short-stroke signs are numerals, they should occupy the same slots and be followed by the same kinds of signs, so their context distributions should be more similar to each other than those of random sign sets.
- Sets: KP1979 {121, 122, 123, 124, 125, 126, 127}; ICIT {001, 003, 004, 034, 005, 016, 017} (the concordance images, fixed above).
- Data: training split only.
- Statistic: mean pairwise Jensen–Shannon divergence between right-neighbour distributions (including the line end), and separately between left-neighbour distributions (including the line start).
- Control: 1,000 random sets of the same size drawn from signs with training frequency between 10 and 700 that are not in the set.
- Prediction: for right-neighbour distributions, observed mean divergence lower than in the control sets, p < 0.01, in both corpora. The left-neighbour result is reported but is not part of the decision.
- Refutation condition: p ≥ 0.01 in either corpus for right-neighbour distributions.

### H3.8 result: not supported (decision criterion); left-context result noted

Script: `scripts/phase3_h38_strokes.py`; results: `results/phase3_h38_strokes.json`. Training split.

| Corpus | Side | Observed mean JS | Control mean (SD) | p |
|---|---|---:|---:|---:|
| KP1979 | right (decision) | 0.732 | 0.818 (0.036) | 0.023 |
| ICIT | right (decision) | 0.763 | 0.808 (0.037) | 0.109 |
| KP1979 | left (reported only) | 0.598 | 0.768 (0.050) | 0.002 |
| ICIT | left (reported only) | 0.641 | 0.762 (0.045) | 0.005 |

By the pre-registered rule H3.8 is not supported: the signs that follow the stroke signs are not significantly more alike than for random sign sets. In both corpora, however, the signs that precede the stroke signs are more alike than for random sets. The most common preceding context is the start of the line (KP 143 of the counted occurrences, ICIT 83), followed by KP 119 / ICIT 002 (59 and 49), which the concordance maps onto each other (ICIT 002 → KP 119, purity 0.97).

Interpretation (to be tested, not a result): the stroke signs share a position (line-initial, or after the sign KP 119 / ICIT 002), while the sign after them varies. This pattern would be expected if the stroke signs quantify or qualify whatever follows, but other explanations are possible.

The left-context result was not the pre-registered criterion, so it is tested on the held-out set as H3.9.

### Pre-registration of H3.9 (before running)

**H3.9 (stroke signs share their preceding context).** The same sets and statistic as H3.8, but using left-neighbour distributions (including the line start) computed only from the held-out strings.
- Control: 1,000 random sets of the same size from signs with held-out frequency ≥ 3, not in the set.
- Prediction: observed mean JS lower than the control, p < 0.01, in both corpora.
- Refutation condition: p ≥ 0.01 in either corpus.
- Note: the held-out set is small, so a failure may reflect low power rather than absence of the effect. It is still recorded as a failure.

### H3.9 result: not supported (fails in KP1979)

Script: `scripts/phase3_h39_strokes_heldout.py`; results: `results/phase3_h39_strokes_heldout.json`. Held-out strings only.

| Corpus | Observed mean JS | Control mean (SD) | p |
|---|---:|---:|---:|
| KP1979 | 0.641 | 0.760 (0.055) | 0.032 |
| ICIT | 0.583 | 0.757 (0.045) | 0.001 |

ICIT meets the criterion; KP1979 does not. By the pre-registered rule (both corpora required), H3.9 is not supported. In both corpora the observed value lies on the predicted side of the control distribution, and in the held-out set several stroke signs occur fewer than 10 times (KP 125: 5, 126: 3, 127: 8), so the test has low power. The shared-preceding-context pattern of the stroke signs therefore remains a suggestion, not a result.

### Assessment of the numeral question so far

- Glyph evidence (sign list) and the agreement of the two numbering systems support treating KP 121–130 / ICIT 001, 003, 004, 005, 016, 017 as a series of signs that differ by stroke count.
- Distributional tests (H3.8, H3.9) did not reach the pre-registered thresholds. The stroke signs do not yet form a demonstrated paradigm.
- Next approaches: (a) test whether stroke count interacts with the following sign (for example, whether certain following signs take only small counts); (b) compare the short-stroke and long-stroke series (KP 121–130 vs 144–151) to see whether they are positional variants or distinct functions; (c) frequency by stroke count (does frequency fall as the count rises?), after verifying the relevant literature on frequencies of number words.

### Correction: reproducibility of the stroke-sign tests (same day)

The first runs of H3.8 and H3.9 drew their random control sets from lists whose order depended on Python's per-process hash seed, so re-running the scripts gave slightly different p-values (H3.9: 0.031 / 0.003, then 0.038 / 0.002). The scripts now sort these lists, and repeated runs give identical output. The tables above show the values of the deterministic version. No conclusion changed: H3.8 and H3.9 remain not supported, for the same reasons. The other scripts were checked: `scripts/phase3_structure.py` reproduces its committed output exactly, and the remaining tests do not draw random samples from unordered collections.

### Exploration: what follows each stroke count (training split, KP1979, not a test)

Next-sign counts after the short-stroke signs, by stroke count (top items): 1 (121): 121 ×42, 144 ×37, line end ×25; 3 (123): 56 ×13, 306 ×12, 86 ×11, 154 ×10; 4 (124): 86 ×16 of 38; 5 (125): 86 ×11 of 35; 6 (126): 86 ×7 of 25; 7 (127): 288 ×17, 289 ×8 of 45; 8 (128): 86 ×3 of 5. After the long-stroke signs: 1 (144): 144 ×61, 121 ×37; 3 (147): 217 ×24 of 79.

Observations:
- The single-stroke signs 121 and 144 are often adjacent to each other (121 → 144 ×37, 144 → 121 ×37, 144 → 144 ×61) and behave differently from the higher counts.
- Counts 4 to 8 are followed most often by KP 86. In the concordance KP 86 corresponds to ICIT 390, 405, 406 and 407 (all purity 1.00).
- Count 7 is followed mainly by 288 and 289; the long three-stroke sign 147 mainly by 217 (ICIT 520).

### Pre-registration of H3.10 (before running)

**H3.10 (higher stroke counts are followed by the KP 86 group).** Short-stroke signs with 4 to 9 strokes are followed by the sign group KP 86 / ICIT {390, 405, 406, 407} more often than other signs are.
- Sets: KP1979 counts 4–9 = {124, 125, 126, 127, 128, 129}, target {86}. ICIT counts 4–9 = {004, 034, 005, 016, 017} (concordance images; no ICIT image is known for 128 and 129), target {390, 405, 406, 407}.
- Data: held-out strings only.
- Test: one-sided Fisher exact test on the 2 × 2 table (preceding sign in set vs any other sign) × (next sign in target vs not), over all within-line bigrams.
- Prediction: odds ratio > 1, p < 0.01, in both corpora.
- Refutation condition: p ≥ 0.01 in either corpus.

### H3.10 result: supported (held-out data, both corpora)

Script: `scripts/phase3_h310_stroke_followers.py`; results: `results/phase3_h310_stroke_followers.json`.

| Corpus | After a 4–9 stroke sign: target / other | After any other sign: target / other | Share (set) | Share (other) | Odds ratio | p |
|---|---:|---:|---:|---:|---:|---:|
| KP1979 | 10 / 16 | 47 / 1,461 | 0.38 | 0.03 | 19.4 | 7.5 × 10⁻⁹ |
| ICIT | 10 / 20 | 36 / 1,380 | 0.33 | 0.03 | 19.2 | 7.2 × 10⁻⁹ |

Verdict: H3.10 meets its pre-registered criteria in both transcriptions. In held-out texts, a sign of 4 to 9 short strokes is followed by the KP 86 / ICIT 390–407 group about twelve times as often as other signs are.

Limitations:
- The counts are small (26 and 30 bigrams after the stroke set).
- The two transcriptions cover largely the same objects, so they are not independent samples (as for H3.3).
- Held-out strings are unique, but near-identical strings (for example variants of a repeated formula) can still make the bigrams less independent than the test assumes.
- The control is "all other signs". A stricter control, for example other medial signs of similar frequency, has not been run.

Interpretation: the result fits a pattern in which a counted number of strokes is followed by a particular sign or sign group, as a numeral is followed by what is counted or by a unit. This is a structural result (L1 type). It becomes an L2 (semantic-category) result only if the "counted item" reading predicts information outside the text, for example a link between the KP 86 group and a particular object type or find context. That is the next test to design.

### Next steps

1. H3.11: stricter control for H3.10 (compare with signs matched for frequency and medial share), on data not yet used for this question. Since the held-out set has now been used for this question, the stricter control must be run on the training split and reported as a robustness check only.
2. Design an L2 test for the KP 86 group: does its presence predict object type or site beyond what H3.5/H3.6 already show?
3. Check whether count 7 → 288/289 and long count 3 (147) → 217 (ICIT 520) are similar count–item pairs (training split first, then new data if available).
4. Look for further data sources (for example newly published inscriptions) to serve as a fresh test set, since the held-out set is being used up.

### H3.11 robustness check for H3.10 (training split): passed

Script: `scripts/phase3_h311_matched_control.py`; results: `results/phase3_h311_matched_control.json`.

Each stroke sign was replaced by a random sign matched for frequency (within a factor of 1.5) and medial share (within 0.15); 1,000 draws.

| Corpus | Share followed by target, stroke set | Matched sets: mean (SD), maximum | p |
|---|---:|---:|---:|
| KP1979 | 0.31 | 0.05 (0.05), 0.27 | 0.001 |
| ICIT | 0.38 | 0.04 (0.04), 0.16 | 0.001 |

No matched set reached the observed share in either corpus. The H3.10 effect therefore cannot be explained by frequency or by a general preference of medial signs for KP 86 / ICIT 390–407. This check used the training split, from which the pattern was first noticed, so it is a robustness check and not an independent confirmation; the independent confirmation is H3.10 on the held-out set.

### Pre-registration of H3.12 (before running; held-out data)

Training-split observations: KP 127 (seven short strokes) is followed by 288 (17 of 45) and 289 (8); ICIT 017, its concordance image, is followed by 585 (12) and 575 (10), which are the concordance images of KP 288 and 289 (purity 1.00). KP 147 (three long strokes) is followed by 217 (24 of 79); its ICIT image is 033 (purity 0.79), and KP 217 corresponds to ICIT 520.

**H3.12a.** The seven-stroke sign (KP 127 / ICIT 017) is followed by KP {288, 289} / ICIT {585, 575} more often than other signs are.
**H3.12b.** The three-long-stroke sign (KP 147 / ICIT 033) is followed by KP 217 / ICIT 520 more often than other signs are.
- Test: one-sided Fisher exact test over all within-line bigrams of held-out strings, as in H3.10.
- Correction: two sub-hypotheses, so the threshold is p < 0.005 for each.
- Prediction: each sub-hypothesis passes in both corpora. Each is judged separately.

### H3.12 result: both sub-hypotheses supported in both corpora

Script: `scripts/phase3_h312_count_item_pairs.py`; results: `results/phase3_h312_count_item_pairs.json`.

| Test | Corpus | After the stroke sign: target / other | After other signs: target / other | Odds ratio | p |
|---|---|---:|---:|---:|---:|
| H3.12a (7 short → 288/289) | KP1979 | 4 / 4 | 10 / 1,516 | 152 | 3.0 × 10⁻⁷ |
| H3.12a (7 short → 585/575) | ICIT | 7 / 4 | 4 / 1,431 | 626 | 4.2 × 10⁻¹⁴ |
| H3.12b (3 long → 217) | KP1979 | 6 / 8 | 31 / 1,489 | 36 | 3.4 × 10⁻⁷ |
| H3.12b (3 long → 520) | ICIT | 8 / 14 | 20 / 1,404 | 40 | 1.8 × 10⁻⁹ |

All four values are below the corrected threshold 0.005.

### Synthesis: count signs pair with specific following signs

Taken together, H3.10 and H3.12 show that the stroke signs do not combine freely with what follows. Each count, or range of counts, has a preferred following sign:

| Stroke sign (KP / ICIT) | Count read from the glyph | Preferred next sign (KP / ICIT) | Test |
|---|---|---|---|
| 124–129 / 004, 034, 005, 016, 017 | 4–9 short | 86 / 390, 405, 406, 407 | H3.10 |
| 127 / 017 | 7 short | 288, 289 / 585, 575 | H3.12a |
| 147 / 033 | 3 long | 217 / 520 | H3.12b |

Possible readings, none of which is tested yet:
1. Numeral + counted item or unit, where some items are usually counted in particular quantities.
2. Fixed compounds in which a number is part of a name or title, so that a given count recurs with a given sign.
3. A non-linguistic notation in which count and sign together form a single code.

These readings make different predictions. Reading 1 predicts that a following sign which takes several counts (KP 86) is a general counted item, and that the distribution of counts before it resembles the frequency pattern of quantities. Reading 2 predicts that the pairs recur as whole fixed strings in different texts with the same neighbours. These predictions can be tested and will be pre-registered next.

The L1 status of this result is the same as for H3.3/H3.4: reproduced in two transcriptions and significant on held-out data, with the same limitation about the transcriptions not being independent samples.

### Claims register

Wrote `docs/CLAIMS_REGISTER.md`: 35 published claims (C1–C35), each with its source and a testable form. 15 are testable with the current data, 20 only partly. The full texts of the sources could not be opened from the working environment, so the entries rest on abstracts and search-engine excerpts. This is stated in each entry, and every quotation must be checked against the original before it is cited in a report.

### Fish-shaped signs: identification from the printed sign list

In the KP1979 sign list (printed page [19]), signs 48–63 are drawn as variants of one vertical outline with a forked tail: plain (49, 50), hatched (48), with small marks above (51, 57, 59, 61, 63), with an inner stroke (56, 57), with a chevron or "roof" above (58–61), crossed (62, 63), or enclosed in brackets or combined with other signs (52–55). That these are "fish" signs is the published identification (claims register C22); the list of numbers 48–63 is my own reading of the drawings. The KP signs 288 and 289, which follow the seven-stroke sign (H3.12a), are not fish-shaped: 288 is a square frame on legs, 289 a frame open at the bottom.

KP frequencies: 50: 157, 56: 366, 58: 264, 60: 246, 62: 283; the others are below 31.

ICIT images (concordance support ≥ 3, purity ≥ 0.6): 53 → 222, 56 → 220 and 231, 57 → 226, 58 → 233, 60 → 235, 61 → 236, 62 → 240, 63 → 241. ICIT fish set fixed as {220, 222, 226, 231, 233, 235, 236, 240, 241}.

### Pre-registration of H3.13 and H3.14 (claims register C23), held-out data

The claim (C23, secondary sources): sequences "numeral + fish" are names of star groups, in particular 3, 6 and 7 + fish.

**H3.13 (fish signs are preceded by stroke signs more often than other signs are).** Held-out within-line bigrams; 2 × 2 table (preceding sign is a short-stroke sign KP 121–130 / ICIT {001, 003, 004, 034, 005, 016, 017} vs not) × (sign is in the fish set vs not). One-sided Fisher exact test.

**H3.14 (counts before fish signs concentrate on 3, 6, 7).** Among bigrams "short-stroke sign → next sign", the table (count ∈ {3, 6, 7} vs other count) × (next sign is fish vs not). Prediction: counts 3, 6 and 7 are over-represented before fish signs. One-sided Fisher exact test. KP counts read from glyphs (121 = 1 … 130 = 10); ICIT counts via the concordance (001 = 1, 003 = 3, 004 and 034 = 4, 005 = 5, 016 = 6, 017 = 7).

- Two hypotheses, so the threshold is p < 0.005 each; each must pass in both corpora.
- Disclosure: I have already seen, in the training split, that KP count 3 is often followed by 56 (a fish sign). The held-out set has not been examined for these bigrams.

### H3.13 and H3.14 results: not supported

Script: `scripts/phase3_h313_fish_numerals.py`; results: `results/phase3_h313_fish_numerals.json`.

| Test (held-out) | Corpus | Odds ratio | p |
|---|---|---:|---:|
| H3.13 stroke sign before fish | KP1979 | 0.89 | 0.69 |
| H3.13 stroke sign before fish | ICIT | 1.30 | 0.30 |
| H3.14 counts 3/6/7 before fish | KP1979 | 0.88 | 0.69 |
| H3.14 counts 3/6/7 before fish | ICIT | 1.46 | 0.45 |

Neither hypothesis passes in either corpus. On the held-out data, fish signs are not preceded by stroke signs more often than other signs are, and the counts before fish signs are not concentrated on 3, 6 and 7.

Descriptive counts on all data (not a test; the training part had partly been seen):

| Count | KP: before fish / before other | ICIT: before fish / before other |
|---:|---:|---:|
| 1 | 40 / 318 | 14 / 106 |
| 2 | 6 / 25 | – |
| 3 | 23 / 127 | 17 / 88 |
| 4 | 6 / 40 | 5 / 60 |
| 5 | 0 / 32 | 0 / 31 |
| 6 | 11 / 14 | 9 / 16 |
| 7 | 1 / 49 | 1 / 49 |

Two features stand out and are recorded as observations only:
- Six strokes are followed by a fish sign in 11 of 25 cases (KP) and 9 of 25 (ICIT), well above the overall share for stroke signs (about 12 % in KP). This agrees with one part of the published claim (6 + fish).
- Seven strokes are followed by a fish sign only once in 50 cases in each corpus. In this corpus the seven-stroke sign goes with KP 288/289 (H3.12a), not with fish signs. This does not agree with the reading of 7 + fish as a frequent name.

Both points come from the same data in which the pairing patterns were explored, so a test of "6 + fish" would need inscriptions not in either corpus. The scope of the claim also matters: the source seen was secondary, and the original may define "seven" or "fish" differently (for example including other stroke arrangements). This must be checked against Parpola (1994) before the observation is used in a report.

---

## 2026-11-25 (day 1, second working session, 06:34 UTC)

Plan for this session: test two published claims that bear on meaning (claims register C31 and C30), using the stroke-sign list established above. Both use only the ICIT-style source, because only it has decoded object-type and motif fields.

### Pre-registration of H4.1 (claim C31a; before running)

**H4.1 (tablets carry numerals more often than seals).** The claim (Rao 2018, via claims register C31) predicts that tablet texts contain numeral signs more often than seal texts.
- Numeral signs: ICIT short-stroke signs with 3 to 9 strokes, {003, 004, 034, 005, 016, 017}. The single stroke (001) is excluded, because it behaves differently (see the stroke-count exploration above).
- Unit: unique held-out strings with a single coarse object type (`SEAL*` or `TAB*`) and a single site.
- Primary test: within Harappa, one-sided Fisher exact test on (tablet vs seal) × (contains a numeral sign vs not). Secondary: the same within Mohenjo-daro (reported, not part of the decision).
- Prediction: numeral share higher on tablets, p < 0.01 (primary).
- Disclosure: in the H3.5 classifier (training data, all Harappa strings), "sign 003 present" had a weight towards seals (−1.16). This was seen before this pre-registration, and it points against the prediction.

### Pre-registration of H4.2 (claim C30; before running)

**H4.2 (the text predicts the seal motif).** Claim C30 (Mukhopadhyay 2023) treats motifs as emblems of issuing bodies, which suggests that text and motif are largely independent. H4.2 is the alternative: the text carries information about the motif.
- Unit: unique seal strings with a single motif code. Classes: `Bull1` vs all other animal codes {Gaur, Zebu, Elep, Rhin, Buff, Tigr, Goat}. Other codes and blank motifs are excluded.
- Model: logistic regression on sign counts, initial sign, final sign and length (as in H3.5); trained on non-held-out strings, tested on held-out strings.
- Metric: balanced accuracy. Control: 200 permutations of the training labels.
- Decision: H4.2 is supported if balanced accuracy ≥ 0.6 and p < 0.01. If not, the result is recorded as consistent with the independence claimed in C30, not as proof of independence.

### H4.1 result: not supported

Script: `scripts/phase4_h41_h42_claims.py`; results: `results/phase4_h41_h42_claims.json`.

| Site (held-out) | Tablets with numeral | Seals with numeral | Odds ratio | p (one-sided) |
|---|---:|---:|---:|---:|
| Harappa (primary) | 4 / 73 (0.05) | 4 / 42 (0.10) | 0.55 | 0.88 |
| Mohenjo-daro (secondary) | 7 / 22 (0.32) | 21 / 173 (0.12) | 3.38 | 0.022 |

At Harappa the direction is opposite to the prediction. At Mohenjo-daro it is in the predicted direction but does not reach p < 0.01, and Mohenjo-daro was not the decision site. The two sites behave differently, which again fits the observation (H3.5) that "tablet" covers different object classes at the two sites: Harappa tablets are mostly `TAB:B` and `TAB:I`, Mohenjo-daro tablets mostly `TAB:C`. A sharper form of C31 would name the tablet subtype; that needs the meaning of the subtype codes to be checked against a primary source first.

### H4.2 result: not supported (consistent with claim C30)

Training seals: 715 `Bull1`, 152 other animals. Held-out: 172 and 47. Balanced accuracy 0.476; permutation mean 0.493 (SD 0.038); p = 0.67.

The text gives no usable information about whether a seal carries the `Bull1` motif or another animal. This is what the independence reading of C30 expects, but a negative result with 47 minority-class test strings does not prove independence; a weak association could be missed.

### Where the numeral line of work stands

| Result | Status |
|---|---|
| Stroke signs form a counted series (glyphs; two numbering systems agree) | descriptive |
| Specific counts pair with specific following signs (H3.10–H3.12) | L1, held-out, both transcriptions |
| Stroke signs share contexts as one paradigm (H3.8, H3.9) | not supported |
| Numeral + fish as star names (H3.13, H3.14) | not supported |
| Tablets carry more numerals than seals (H4.1) | not supported at Harappa |

The count–item pairing is the strongest result so far. An L2 claim requires a semantic category that predicts something outside the text, and the two external variables tested so far (object type, motif) did not respond to the simple numeral and motif categories.

### Pre-registration of H4.3 (claim C32b; before running)

**H4.3 (tablet texts repeat the endings of seal texts).** Claim C32 (Harappa excavation report as given on harappa.com) states that a miniature-tablet inscription is identical to the last two signs of a nearby seal. The general form tested here: tablet texts occur as the final part (suffix) of seal texts more often than expected.
- Tablet strings: unique held-out strings with coarse type `TAB*` (any site), length ≥ 2, with at least two distinct signs.
- Seal strings: all unique seal strings (training and held-out), excluding any string identical to the tablet string itself.
- Statistic: share of tablet strings that equal the suffix of at least one seal string.
- Control: for each tablet string, 1,000 random reorderings of its own signs; the control share is the expected suffix-match share of the reordered strings. p is the probability, under the reordering control, of a share at least as large as observed (computed by drawing one reordering per string, 1,000 times).
- Prediction: observed share above the control, p < 0.01.
- Also reported (not part of the decision): the share of tablet strings that equal the prefix (beginning) of a seal string, under the same control.

### H4.3 result: supported as pre-registered, but mostly explained by the line-final rule

Scripts: `scripts/phase4_h43_tablet_suffix.py` (pre-registered), `scripts/phase4_h43_strict_control.py` (exploratory); results: `results/phase4_h43_tablet_suffix.json`, `results/phase4_h43_strict_control.json`.

| Test | Tablet strings | Observed share | Control mean (SD) | p |
|---|---:|---:|---:|---:|
| Suffix of a seal text, full reordering control (decision) | 102 | 0.059 (6) | 0.018 (0.010) | 0.001 |
| Prefix of a seal text, full reordering control (reported) | 102 | 0.010 (1) | 0.005 (0.005) | 0.53 |
| Suffix, control keeping the final sign fixed (exploratory) | 86 | 0.035 (3) | 0.012 (0.008) | 0.013 |

By the pre-registered rule H4.3 is supported: tablet texts match the endings of seal texts more often than reorderings of their own signs do, and they do not match the beginnings. However, four of the six matches end in 740, and the full reordering control moves 740 away from the end, which the line-final rule (H3.3) already forbids. With the final sign held in place the excess remains in the same direction (3 of 86 vs 1.2 % expected) but no longer reaches p < 0.01.

Verdict: the claim that tablet texts reproduce the endings of seal texts is supported only weakly. The pre-registered control was too lenient, because it did not respect an ordering rule established earlier. This is recorded as a lesson for later designs: controls must preserve every structural rule already established, so that a new test measures only the new effect.

The three matches that survive the strict control are `233 550 527`, `233 798 740` and `920 017 575 740 400`. The last contains the seven-stroke pairing of H3.12a (017 → 575).

### Next steps

1. Fresh data: look for inscriptions outside both corpora (for example published after 1979 and missing from the ICIT-style source), to serve as a new test set, since the held-out set has been used for several questions.
2. Phase 4 (script typology): compare the corpus with synthetic and non-linguistic baselines, with the caution from the bibliography (D section, Raghavendra 2026) that common statistical measures are not specific to language.
3. Revisit H3.2 with a pre-fixed number of clusters on a new data split, if fresh data become available.

### Search for a fresh test set: ICIT strings absent from KP1979 (not usable yet)

Idea: KP1979 contains only inscriptions known by 1979, so ICIT strings with no KP1979 counterpart could be later finds and serve as fresh test data for hypotheses formed on KP1979 alone.

Check (concordance with support ≥ 2 and purity ≥ 0.5): of 2,059 unique complete ICIT strings, 576 contain a sign without a KP image, and 847 can be mapped but do not equal any complete KP1979 line. By site, the 847 are Mohenjo-daro 417, Harappa 276, Dholavira 40, Lothal 27, Chanhu-daro 17, Kalibangan 17, others fewer.

Dholavira was excavated mainly after 1979, so its strings are plausible new finds, but the large Mohenjo-daro share shows that many of the 847 are probably the same objects read differently (a sign more or less, a different allograph decision) rather than new inscriptions. Without an object-level link between the two sources (KP1979 inscription numbers to CISI numbers), this set cannot be used as clean fresh data. Building that link is a task for a later session, using the CISI numbers in the ICIT-style source and the KP1979 type and icon codes.

### Next steps (updated)

1. Object-level link between KP1979 and the ICIT-style source (inscription numbers ↔ CISI numbers), so that post-1979 finds can be separated as a fresh test set.
2. Phase 4 (typology) with controls that preserve the rules already established (lesson from H4.3).
3. Positional "slot" description of the texts (which sign classes occupy which positions), formed on KP1979 training data and tested on ICIT held-out strings for that new question.

---

## 2026-11-25 (day 1, third working session)

### A fresh test set: sites excavated after 1979

KP1979 was published in 1979, so it cannot contain inscriptions from sites first excavated after that year. Two such sites in the ICIT-style source have a sourced start date:
- Dholavira: excavation initiated in 1989–90 by the Archaeological Survey of India under R. S. Bisht (UNESCO nomination dossier, https://whc.unesco.org/document/184545; Bisht 2015, *Excavations at Dholavira 1989–2005*, listing seen at https://www.scribd.com/document/262316120/Excavations-at-Dholavifra-1989-2005-RS-Bisht-2015). Source seen: search-engine excerpts.
- Nausharo: field seasons 1985–1988 reported by J.-F. Jarrige (catalogue record, https://ehrafarchaeology.yale.edu/traditions/aq43/documents/011). Source seen: search-engine excerpt.

Other post-1979 sites in the source (Farmana, Kanmer, Bhirrana, Khirsara, Gola Dhoro, Rakhigarhi) are not used, because their excavation dates were not confirmed from a source in this session.

**Fresh set:** complete ICIT lines with recorded direction from Dholavira (78) and Nausharo (17). Protocol: hypotheses are built from **KP1979 training data only**, carried into ICIT numbering through the concordance, and tested on the fresh set. ICIT training data from these two sites were part of earlier ICIT analyses, but no rule tested below was derived from ICIT data.

### Pre-registration of F1–F3 (before looking at the fresh set)

Mapping: an ICIT string is carried into KP numbering using concordance entries with support ≥ 2 and purity ≥ 0.5; strings containing an unmapped sign are excluded from F3.

**F1 (terminal-cluster order, H3.3, on fresh data).** Dominant orders of adjacent KP terminal signs (KP training split, as in H3.3) predict the order of the same pairs in the fresh set. Binomial test (null 0.5). Prediction: agreement ≥ 0.8, p < 0.01. If fewer than 5 qualifying pairs occur, the result is recorded as "insufficient data".

**F2 (count–item pairing, H3.10, on fresh data).** In the fresh set, KP 124–129 images {004, 034, 005, 016, 017} are followed by {390, 405, 406, 407} more often than other signs are. One-sided Fisher exact test, p < 0.01. Fewer than 5 bigrams after the stroke set → "insufficient data".

**F3 (sequential structure and reading direction carry over).** A bigram model with add-0.1 smoothing over the KP vocabulary, trained on KP1979 training lines, is compared with (a) a unigram model trained on the same lines and (b) the same bigram model applied to the fresh strings reversed. Statistic: mean per-sign log-loss on mapped fresh strings of length ≥ 2. Test: one-sided sign test over strings (bigram forward better than unigram; forward better than reversed). Prediction: both comparisons favour the forward bigram, p < 0.01 each.

### F1–F3 results (fresh set: Dholavira and Nausharo, 93 unique strings)

Script: `scripts/phase5_fresh_tests.py`; results: `results/phase5_fresh_tests.json`.

**F1: insufficient data.** No adjacent pair of KP terminal-set signs occurs in the fresh strings (after mapping). The terminal-cluster order cannot be tested here.

**F2: supported.** After a 4–9 stroke sign, the next sign is in {390, 405, 406, 407} in 4 of 8 cases; after any other sign, in 12 of 286 cases. One-sided Fisher exact test p = 0.00036. The count–item pairing found in the pre-1979 corpus holds at two sites excavated later, one of them (Dholavira) far from the sites that dominate KP1979. The count is small (8 bigrams).

**F3: supported.** 63 fresh strings could be mapped completely into KP numbering.

| Model (trained on KP1979 training lines) | Mean log-loss per sign (nats) |
|---|---:|
| Bigram, strings in reading order | 3.49 |
| Unigram | 3.93 |
| Bigram, strings reversed | 5.58 |

The forward bigram model beats the unigram model on 44 of 63 strings (sign test p = 0.0011) and beats the reversed strings on 57 of 63 (p = 8 × 10⁻¹²). Sequential regularities learned from the pre-1979 corpus carry over to later finds from other regions, and they do so only in the established reading direction. Note that F3 shows shared order and direction, not that the system is linguistic: an ordered non-linguistic notation would also pass it.

### Status of the L1 results after the fresh-data tests

| Result | Held-out (same corpora) | Other site within corpus | Fresh post-1979 sites |
|---|---|---|---|
| Terminal-cluster order (H3.3) | yes | yes (H3.4) | not testable (F1) |
| Count–item pairing, 4–9 strokes (H3.10) | yes | – | yes (F2) |
| Shared sequential structure and reading direction | – | – | yes (F3) |

The count–item pairing is now the best-supported structural result: it holds on held-out data in two transcriptions, against matched controls, and on inscriptions from sites excavated after the training corpus was published.

---

## 2026-11-25 (day 1, fourth working session)

Wrote `docs/WORKPLAN.md` (work packages A–F with decision gates G1–G4 and a schedule) and `docs/DATA_LEDGER.md` (every test with the data it was decided on). After a Bonferroni correction over the 11 tests decided on the held-out split, H3.3, H3.10 and H3.12 remain significant; H4.3 does not.

KP1979 type and icon codes cannot be decoded here: the 1979 introduction (§6.3–6.4) refers to tables in the 1973 concordance, which is not available.

### Pre-registration of C1 (copper tablets: text and motif; before running)

Copper objects in the ICIT-style source are almost all of type `TAB:C` (176 of 182 complete lines). Many carry the same text, so identical strings are already merged; in addition, strings that differ by at most one sign (edit distance ≤ 1) are merged into one group, because such near-copies could share a motif without the signs being informative. Each group keeps one representative (its most frequent string) and must have a single motif code.

**C1.** Among distinct copper-tablet text groups, texts with the same motif share more signs than texts with different motifs.
- Motif codes used: any code except `Othr`, blank, `-` and `Unknown`.
- Statistic: mean Jaccard similarity of sign sets for same-motif pairs minus that for different-motif pairs.
- Control: 10,000 permutations of motif labels among groups.
- Prediction: difference > 0, p < 0.01.
- Data: all copper-tablet strings (the set is too small to split). This is a new question, decided on data not used for any earlier motif test, but it is not held-out in the formal sense and is recorded as such in the ledger.
- If supported, the signs shared within motif groups are listed as candidates for an L2 hypothesis (a sign naming or referring to the depicted animal), to be tested on seals or other objects with the same motif.

### C1 result: not supported

Script: `scripts/phase6_c1_copper_motif.py`; results: `results/phase6_c1_copper_motif.json`.

After merging near-copies, 43 text groups remain, of which only 17 have exactly one specific motif code. Observed difference in mean Jaccard similarity (same motif minus different motif) 0.018; permutation mean 0.000 (SD 0.027); p = 0.24. Distinct copper-tablet texts that share a motif do not share more signs than texts with different motifs.

Descriptive observations (not tests):
- Most copper-tablet text groups are dominated by one motif code, because the same text recurs on several tablets with the same motif (for example `503 615 752 740` on 33 lines, mostly `Gaur`; `235 705 033 845 407 321 407` on 14 lines, all `Hare`; `706 033 923 740` on 12 lines, mostly `Elep`). The association between text and motif on copper tablets is therefore largely an association between copies of the same object type, not evidence that particular signs refer to animals.
- The motif field is not coded consistently for these objects: several lines carry two codes (for example `Gaur` and `Othr`), and one text group carries `Goat` and `Buff` in equal numbers. Motif-based tests on copper tablets need the original photographs or a primary catalogue.
- Several copper-tablet texts end in 407, a member of the group that follows the 4–9 stroke signs (H3.10), often after 845 (`… 845 407`, `… 845 061 407`). Noted for WP-C3; not tested here.

Ledger: C1 decided on all copper-tablet strings (not held-out).

### WP A2: rule-preserving controls

Added `src/indus/controls.py`. A control text keeps the line length, the line-final terminal cluster and the count–item pairs (H3.10, H3.12) in place, and permutes the remaining units. From now on, tests that use reordering controls use this generator.

### WP B2: semicircle signs (claim C24c) cannot be tested

Claim C24 says that groups of semicircles probably stand for tens. In KP1979 the arc signs 131–135 occur 5, 2, 1, 1 and 1 times, and none has a concordance image in the ICIT-style source. With 10 occurrences in total the "tens before ones" prediction cannot be tested. Recorded as infeasible with current data.

### WP A3: extended fresh set

Excavation start dates found in this session (search-engine excerpts; details and URLs in `docs/FRESH_SITES.md`):

| Site | First excavation | Lines (complete, direction known) |
|---|---|---:|
| Farmana | 2006 | 5 |
| Gola Dhoro (Bagasra) | 1996 | 5 |
| Lakhanjo-daro | 1992 (salvage), 2006 | 5 |
| Kanmer | 2005–06 | 4 |
| Bhirrana | 2003 | 3 |
| Khirsara | 2009 | 3 |
| Shikarpur | 1987 | 2 |
| Ganweriwala | after 2007 | 1 |

Rakhigarhi is excluded: sources disagree on whether excavation began in the 1960s or in 1997. The earlier fresh set (Dholavira, Nausharo) is called fresh set 1; these eight sites are fresh set 2 (about 28 lines). No test has used fresh set 2.

### Pre-registration of F2b and F3b (fresh set 2 only, before running)

Same procedures and criteria as F2 and F3 (rules and models from KP1979 training data), applied to fresh set 2 only. F2b is marked "insufficient data" if fewer than 3 bigrams follow a 4–9 stroke sign. F3b uses the sign test over mapped strings; prediction p < 0.01 for forward vs reversed. Because fresh set 2 is small, a failure of F3b's bigram-vs-unigram comparison is expected to be likely and is reported without a decision.

### F2b and F3b results (fresh set 2: 24 unique strings from eight post-1979 sites)

Script: `scripts/phase5_fresh_tests.py --set2`; results: `results/phase5_fresh_tests_set2.json`. (The script without `--set2` reproduces the committed fresh-set-1 results exactly.)

- **F1b:** insufficient data (no adjacent terminal-set pair).
- **F2b: not supported.** After a 4–9 stroke sign the target group follows in 1 of 3 cases (other signs: 3 of 68); p = 0.16. With three bigrams the test has almost no power; the direction agrees with F2.
- **F3b:** 15 strings mapped. Forward bigram beats reversed on 14 of 15 (p = 0.0005, **supported**). Forward bigram beats unigram on 11 of 15 (p = 0.059; reported without a decision, as pre-registered). Mean log-loss: forward 3.52, unigram 3.82, reversed 5.40 — the same pattern as fresh set 1.

Ledger additions: F2b, F3b on fresh set 2.

### Gate status after this session

- G1 (L1 consolidation): pending B1/B4.
- G2 (L2): no L2 result yet; tests so far (object type, motif, copper tablets) are negative.

### WP B2: numeral table (descriptive)

`scripts/phase3_numeral_table.py` → `results/phase3_numeral_table.md` (all data, unique lines; not a test).

Main points:
- **Distribution of counts.** KP1979 short strokes: 1: 386 occurrences, 2: 35, 3: 156, 4: 49, 5: 40, 6: 28, 7: 53, 8: 5, 9: 1, 10: 1. Counts above 7 are rare, but 8, 9 and 10 are attested as single signs. This is relevant to the base question (claim C25) but does not settle it: a base-8 system would not need single signs for 8–10, but their rarity could also reflect how often such numbers were needed.
- **Count-specific partners recur in both corpora.** 4, 5, 6, 8 and 9 strokes → KP 86 (ICIT 390/405/407); 7 → KP 288/289 (ICIT 585/575); 3 long → KP 217 (ICIT 520); 4 long → KP 310 (3 of 3). Count 3 (short) has no single dominant partner (KP 86, 306, 56, 154, 217 each 11–13 times).
- **Single strokes behave differently.** KP 121 (one short stroke) and 144 (one long stroke) are most often followed by each other or by themselves (121 → 121 ×51, 121 → 144 ×48, 144 → 144 ×71). This is not how a numeral "1" before a counted item would be expected to behave, and it suggests that single strokes have another function (for example a divider or a separate sign), or that sequences of single strokes write a number.
- **ICIT 001 does not behave like KP 121.** ICIT 001 is rarely line-initial (8 of 130) whereas KP 121 often is (58 of 386). The concordance link 121 → 001 may be partial (several KP single-stroke variants may map to different ICIT signs). To be checked in WP B3.

### Next working session

1. WP B1 (positional template) and B4 (recurring units), evaluated on fresh sets 1 and 2 with rule-preserving controls; gate G1.
2. WP B3: the 121/144 single-stroke question and the 121 → 001 link.
3. WP C3: does the count–item construction favour particular object types or materials (site-stratified, held-out)?

---

## 2026-11-25 (day 1, fifth working session): WP B1 and B4, gate G1

Both tests build their description from KP1979 training data only, carry the fresh strings (sets 1 and 2 combined, mapped into KP numbering as in F3) and compare them with rule-preserving controls (`src/indus/controls.py`, KP rules), 1,000 control sets. Fresh data were used before for F1–F3 (different questions); this use is logged in the ledger.

### Pre-registration of B1 (positional template)

Zones from KP training data, for signs with ≥ 10 occurrences: initial zone I if initial share ≥ 0.5; terminal zone T if final share ≥ 0.5; otherwise medial zone M. Template: a line reads I* M* T* (zones never go backwards).
- Statistic: total number of zone inversions (pairs of zoned signs i < j with zone(i) > zone(j)) over all mapped fresh strings.
- Control: the same count for rule-preserving control versions of the fresh strings.
- Prediction: fewer inversions in the real strings than in the controls, p < 0.01.

### Pre-registration of B4 (recurring units)

Units from KP training data: all 2- and 3-sign sequences that occur in at least 5 distinct training lines, excluding the count–item pairs and terminal-cluster pairs already built into the controls.
- Statistic: number of adjacent sign pairs in the fresh strings that lie inside an occurrence of some unit.
- Control: the same count for rule-preserving control versions.
- Prediction: more covered pairs in the real strings than in the controls, p < 0.01.

Gate G1 is passed if B1 or B4 is supported.

### B1 and B4 results: both supported; gate G1 passed

Script: `scripts/phase3_b1_b4_template_units.py`; results: `results/phase3_b1_b4_template_units.json`. 78 fresh strings mapped (sets 1 and 2).

| Test | Observed | Rule-preserving controls: mean (SD) | p |
|---|---:|---:|---:|
| B1 zone inversions (fewer predicted) | 31 | 55.7 (7.3) | 0.001 |
| B4 adjacent pairs inside recurring units (more predicted) | 84 | 37.2 (4.6) | 0.001 |

Zones from KP training data: 15 initial-zone signs, 83 medial, 16 terminal. Recurring units: 313 two- and three-sign sequences.

Both results hold against controls that already keep the line length, the terminal cluster and the count–item pairs. Therefore:
- **B1:** beyond the terminal cluster, the order of the rest of the line follows an initial → medial → terminal template at sites excavated after the training corpus was published.
- **B4:** multi-sign units that recur in the pre-1979 corpus recur in the later finds, and this is not explained by the rules already built into the controls.

**Gate G1: passed.** The L1 result is no longer limited to a few sign pairs. A positional template and a lexicon of recurring units, both learned from KP1979, predict inscriptions from ten sites excavated later. As before, this is a structural result. It is compatible with writing, and equally with a structured non-linguistic notation.

### Observation from the recurring units (not a test)

Units found in the fresh strings include `119 121`, `119 123`, `119 124`, `119 124 86`, `119 126`, `119 127`, `119 144`: the sign KP 119 (ICIT 002) directly before stroke signs. Together with the H3.8 left-context result (stroke signs are most often preceded by the line start or by KP 119), this suggests that 119 introduces a number. The sign 119 is the most frequent non-terminal sign in KP1979 (704 occurrences) and is almost always medial in ICIT (002: medial share 0.95). Its relation to the stroke signs is the next target (WP C3/B3): does 119 precede stroke signs more than matched controls do, and is "119 + count + item" a fixed construction?

### Pre-registration of H5.1 (sign KP 119 / ICIT 002 introduces numbers; held-out data)

**H5.1.** The sign KP 119 (ICIT 002) is followed by a stroke sign more often than signs matched to it for frequency and medial share.
- Stroke signs: KP short 121–130 and long 144–151; ICIT {001, 003, 004, 034, 005, 016, 017, 033, 035}.
- Statistic: share of occurrences of 119 / 002 in held-out strings that are followed by a stroke sign.
- Control: 1,000 draws of one matched sign (training frequency within a factor 2 of 119 / 002, training medial share within 0.15), each evaluated on the held-out strings in the same way; signs in the stroke set are excluded from the pool.
- Prediction: observed share above the matched draws, p < 0.01, in both corpora.
- Held-out use: this is the 12th question decided on the held-out split.

**Amendment to H5.1 (before any outcome was computed).** The pre-registered control could not be built: no sign lies within a factor 2 of the training frequency of KP 119 (394) or ICIT 002 (404) with a similar medial share (0.96 / 0.95); with a factor 4 or 8 only 2–8 signs qualify, too few for p < 0.01. Amended control: all other signs with training frequency ≥ 30 and training medial share ≥ 0.8 (stroke signs excluded), pooled. Test: one-sided Fisher exact test on held-out bigrams, (preceding sign is 119/002 vs a pooled medial sign) × (next sign is a stroke sign vs not). Prediction and threshold unchanged (p < 0.01 in both corpora).

### H5.1 result: not supported (passes in KP1979, fails in ICIT)

Script: `scripts/phase5_h51_sign119.py`; results: `results/phase5_h51_sign119.json`.

| Corpus | Sign → stroke / other | Pooled medial signs → stroke / other | Shares | Odds ratio | p |
|---|---:|---:|---:|---:|---:|
| KP1979 (119) | 19 / 70 | 9 / 171 | 0.21 vs 0.05 | 5.2 | 7.4 × 10⁻⁵ |
| ICIT (002) | 8 / 92 | 7 / 156 | 0.08 vs 0.04 | 1.9 | 0.16 |

By the pre-registered rule (both corpora), H5.1 is not supported. The two transcriptions disagree strongly, which points to a transcription question rather than a simple absence of the effect: ICIT 002 is more frequent than KP 119 (855 vs 704 occurrences in all lines), and the concordance link 002 → 119 may merge or split signs differently (as found for 121 → 001). Before the construction "119 + count + item" can be examined further, the correspondence of KP 119, 121, 122 and ICIT 001, 002 must be checked line by line in the aligned pairs (WP B3).

### WP B3 finding: the ICIT long-stroke series, and an error in the H5.1 sign set

Aligned line pairs (`results/phase1_concordance.tsv`) show:
- ICIT 031 ↔ KP 144 (one long stroke; 37 of 50 alignments, the rest mostly KP 121);
- ICIT 032 ↔ KP 145 (two long strokes; 34 of 45);
- ICIT 033 ↔ KP 147 (three long strokes; as found before);
- ICIT 001 ↔ KP 121 (one short stroke; 57 of 64); ICIT 002 ↔ KP 119 (279 of 287).

So the ICIT numbers 031–035 are the long-stroke series. The ICIT stroke set pre-registered for H5.1 included 033 and 035 but omitted 031 and 032, while the KP set included all long strokes. The two sets were not equivalent; this was an error in the pre-registration. The H5.1 verdict stands as recorded (not supported), because changing the set after seeing the result would not be a test. The corrected question is pre-registered below on data not used for it.

The earlier stroke tests H3.8–H3.14 used short strokes only in both corpora (KP 121–130 / ICIT 001–017), plus KP 147 / ICIT 033 in H3.12b, so they are not affected.

### Pre-registration of H5.1b (corrected sets; fresh sets 1 and 2)

Same question and test as amended H5.1, on fresh sets 1 + 2 (ICIT only; KP1979 has no fresh data), with the ICIT stroke set {001, 003, 004, 034, 005, 016, 017, 031, 032, 033, 035}. Pool of comparison signs defined from ICIT training data as in H5.1. Prediction: 002 is followed by a stroke sign more often than the pooled medial signs, one-sided Fisher p < 0.01. If fewer than 10 occurrences of 002 have a following sign in the fresh sets, the result is "insufficient data".

### H5.1b result: not supported

Script: `scripts/phase5_h51b_sign002_fresh.py`; results: `results/phase5_h51b_sign002_fresh.json`.

In the fresh sets, 002 is followed by a stroke sign in 7 of 26 cases; the pooled medial signs in 5 of 48. Odds ratio 3.2, one-sided Fisher p = 0.068. The direction agrees with KP1979 (H5.1), but the result does not reach p < 0.01. The relation "119/002 introduces a number" therefore remains supported only in KP1979 held-out data and is not established.

### Summary of this session

| Test | Result |
|---|---|
| B1 positional template, fresh data | supported |
| B4 recurring units, fresh data | supported |
| Gate G1 | passed |
| H5.1 sign 119/002 before strokes, held-out | not supported (KP yes, ICIT no; ICIT set defined wrongly) |
| H5.1b corrected sets, fresh data | not supported (p = 0.068) |

Next: WP C3 (does the count–item construction favour particular object types or materials, site-stratified) and the start of WP D (typology) with rule-preserving synthetic baselines.

---

## 2026-11-25 (day 1, sixth working session): WP D, script typology

### Reference corpora

Added `scripts/fetch_cdli.py` (CDLI bulk data from https://github.com/cdli-gh/data, last updated August 2022; checked against the Git LFS SHA-256 ids; not committed) and `src/indus/reference.py`, which builds five reference corpora from the catalogue fields period, genre and language:

| Corpus | Definition | Unique complete lines | Median length | Sign/grapheme types |
|---|---|---:|---:|---:|
| proto-Elamite | period "Proto-Elamite" | 3,549 | 3 | 602 |
| proto-cuneiform | Uruk IV and Uruk III | 10,049 | 3 | 1,391 |
| Sumerian, Ur III administrative | Ur III, Administrative, Sumerian | 296,768 | 6 | 3,066 |
| Sumerian, Old Babylonian literary | OB, Literary, Sumerian | 24,085 | 11 | 2,478 |
| Akkadian, Old Babylonian letters | OB, Letter, Akkadian | 25,690 | 8 | 1,141 |

Tokenisation is uniform and simple (see the module docstring): proto-writing signs and numeral groups (for example `7(N01)`) are tokens; cuneiform transliterations are split into graphemes. Lines with breaks or unreadable signs are dropped. The tokenisation of transliterated cuneiform into graphemes is only a rough analogue of a sign sequence, which limits the comparison.

### Pre-registration of D1 (before computing any statistic)

Each corpus is resampled 20 times to 2,000 unique lines with the ICIT length distribution (lengths 1–13; where a length bin has too few lines, all are taken). The ICIT corpus itself (unique complete lines) is resampled the same way. In each sample, lines are split 80/20 at random, and six statistics are computed:

| Statistic | Definition |
|---|---|
| S1 direction asymmetry | mean per-token log-loss of a bigram model (add-0.1, trained on the 80 %) on reversed test lines minus that on forward test lines |
| S2 template strength | 1 − (zone inversions in test lines) / (mean inversions in 20 controls that shuffle all but the final sign); zones from training lines (signs with ≥ 5 occurrences; as in B1) |
| S3 unit excess | adjacent pairs inside recurring units (2–3-grams in ≥ 3 distinct training lines) in test lines, divided by the mean for the same controls |
| S4 repetition | share of lines of length ≥ 2 that contain some sign twice |
| S5 hapax share | share of sign types occurring once in the sample |
| S6 final concentration | share of lines of length ≥ 2 that end in one of the three most frequent final signs |

A synthetic corpus generated by a bigram model fitted to ICIT is computed alongside, as a reference for what a simple Markov process reproduces.

**Prediction D1.** Readings of the Indus inscriptions as administrative records (claims register C16, C29, C31) predict that, after z-scoring each statistic across the six real corpora (using sample means), the Indus corpus is closer (Euclidean distance) to the nearest of the three administrative corpora (proto-Elamite, proto-cuneiform, Ur III administrative) than to the nearest of the two non-administrative corpora (OB literary, OB letters), in at least 19 of the 20 resamples.

**Limits stated in advance.** The comparison contains no genuinely non-linguistic corpus, so it cannot decide gate G3 ("is it writing?"); it can only place the Indus corpus among systems of different function and age. Genre and script type are confounded (the administrative corpora are also the oldest). The result is descriptive typology, not evidence of language.

### D1 result: supported (20 of 20 resamples)

Scripts: `scripts/phase4_d1_typology.py` (pre-registered), `scripts/phase4_d1_leave_one_out.py` (robustness check); results: `results/phase4_d1_typology.json`, `results/phase4_d1_leave_one_out.json`.

Mean statistics over 20 resamples (about 2,000 lines each, Indus length distribution):

| Corpus | S1 direction | S2 template | S3 units | S4 repetition | S5 hapax | S6 final conc. |
|---|---:|---:|---:|---:|---:|---:|
| Indus (ICIT) | 2.25 | 0.57 | 2.35 | 0.038 | 0.35 | 0.51 |
| proto-Elamite | 2.94 | 0.64 | 2.25 | 0.064 | 0.31 | 0.43 |
| proto-cuneiform | 1.98 | 0.75 | 2.06 | 0.035 | 0.35 | 0.06 |
| Sumerian Ur III administrative | 1.61 | 0.49 | 3.00 | 0.082 | 0.29 | 0.13 |
| Sumerian OB literary | 1.64 | 0.41 | 2.62 | 0.169 | 0.38 | 0.12 |
| Akkadian OB letters | 1.44 | 0.26 | 2.01 | 0.127 | 0.33 | 0.21 |
| Synthetic bigram (fitted to Indus) | 2.10 | 0.50 | 2.34 | 0.114 | 0.23 | 0.26 |

Mean distance to the Indus corpus (z-scored statistics): proto-Elamite 2.31, proto-cuneiform 3.16, Akkadian letters 3.88, Ur III administrative 4.07, OB literary 4.10, synthetic bigram 4.87. In all 20 resamples the nearest administrative corpus is closer than the nearest non-administrative corpus (prediction: ≥ 19). **D1 is supported.**

Robustness (not pre-registered): leaving out one statistic at a time, the nearest corpus is proto-Elamite in six of seven cases and proto-cuneiform when S6 is left out. The placement next to the two proto-administrative systems does not depend on a single statistic.

Observations:
- The Indus corpus shares with proto-cuneiform a very low rate of repeated signs within a line (0.038 and 0.035), and with proto-Elamite a strong concentration of a few signs at line end (0.51 and 0.43). In proto-Elamite the line end is typically a numeral group (entries are written "item , number"); in the Indus corpus the line end is the terminal cluster (740, 400, 090), while numerals stand early in the line.
- A bigram model fitted to the Indus corpus does **not** reproduce the Indus profile: it repeats signs three times as often (0.114) and concentrates line ends half as much (0.26). The Indus texts therefore obey constraints that a first-order Markov process does not capture (no repetition, a fixed line end), which is one more structural result.

Interpretation and limits:
- The Indus inscriptions are statistically most similar to the two proto-administrative systems of the late fourth millennium BCE, and less similar to Sumerian and Akkadian texts written in full writing. This fits the administrative readings of the claims register (C16, C29, C31), but it is not evidence for them: age, genre and script type are confounded in the reference set, and Ur III administrative texts, which are administrative but in full writing, are not close.
- Proto-cuneiform is usually described as a system that recorded administrative information largely without recording spoken language. Closeness to it is compatible with the Indus script being proto-writing, but D1 contains no non-linguistic corpus, so gate G3 remains undecided.

### Gate status

- G1: passed (B1, B4).
- G2: not met (no L2 result).
- G3: undecided; D1 places the Indus corpus with proto-administrative systems. The next step for G3 is a genuinely non-linguistic reference corpus.

---

## 2026-11-25 (day 1, seventh working session): gate G3 with non-linguistic corpora

### Non-linguistic reference corpora

The corpora of Sproat (2014, *Language* 90(2), bibliography section C) are public at https://github.com/rwsproat/non-linguistic-symbols (commit `44e1ee3`, Apache License 2.0). Each document's symbol titles, in document order, form one line. Sizes (documents, median length, symbol types): Asian emoticons 10,000 / 6 / 333; barn stars 310 / 3 / 32; kudurrus 69 / 13 / 64; Pictish symbols 283 / 3 / 85; totem poles 325 / 5 / 484; Vinča signs 591 / 1 / 185; weather icons 10,142 / 5 / 16 (all of length 5). The collection also contains an Indus corpus, which is not used here.

### Pre-registration of D2 (gate G3; before computing any statistic)

Because several non-linguistic corpora are small, every corpus is resampled 20 times to **300 unique lines** (all unique lines if fewer; no length matching), and the six statistics S1–S6 of D1 are computed in each sample with the same code.

Groups:
- **Full writing (linguistic):** Sumerian Ur III administrative, Sumerian OB literary, Akkadian OB letters.
- **Non-linguistic:** barn stars, totem poles, weather icons, Asian emoticons. Kudurrus are excluded (69 documents, too few for the train/test split).
- **To be classified:** Indus (ICIT), proto-Elamite, proto-cuneiform, Pictish, Vinča.

Decision rule for G3:
1. Leave-one-corpus-out check on the seven known corpora: each is assigned to the nearer group centroid (Euclidean distance on statistics z-scored across the seven known corpora, using sample means), with the centroids computed without it.
2. If all seven are assigned correctly (false-positive rate 0 < 0.1), the statistics are taken to separate the groups, and the Indus corpus is assigned to the nearer centroid. The assignment counts as stable if it is the same in at least 19 of 20 resamples.
3. If any known corpus is misassigned, G3 is recorded as **undecided**, and no claim about the linguistic status of the Indus corpus is made.

Limits stated in advance: seven known corpora is a small reference set; the non-linguistic corpora differ from the Indus corpus in medium and function; success would show only that the Indus statistics resemble one group, not that the Indus signs record language.

### D2 result: gate G3 undecided

Scripts: `scripts/fetch_sproat.py`, `scripts/phase4_d2_nonlinguistic.py`; results: `results/phase4_d2_nonlinguistic.json`.

Leave-one-corpus-out check on the seven known corpora: 5 of 7 assigned correctly. Totem poles and Asian emoticons, both non-linguistic, were assigned to the full-writing group. By the pre-registered rule the statistics do not separate full writing from non-linguistic symbol systems, so **G3 is undecided** and no claim is made about whether the Indus signs record language.

Sample means (300 unique lines per corpus, 20 resamples):

| Corpus | S1 dir. | S2 templ. | S3 units | S4 repet. | S5 hapax | S6 final |
|---|---:|---:|---:|---:|---:|---:|
| Indus (ICIT) | 1.58 | 0.56 | 3.06 | 0.034 | 0.49 | 0.51 |
| proto-Elamite | 1.79 | 0.58 | 2.85 | 0.037 | 0.47 | 0.43 |
| proto-cuneiform | 1.27 | 0.84 | n/a | 0.016 | 0.53 | 0.07 |
| Sumerian Ur III admin. | 1.14 | 0.45 | 4.51 | 0.159 | 0.40 | 0.18 |
| Sumerian OB literary | 0.96 | 0.43 | 4.29 | 0.597 | 0.42 | 0.16 |
| Akkadian OB letters | 1.12 | 0.29 | 3.11 | 0.363 | 0.36 | 0.26 |
| Barn stars (110 lines) | 0.00 | 0.00 | 0.96 | 0.971 | 0.16 | 0.36 |
| Totem poles | 0.55 | 0.35 | 1.83 | 0.359 | 0.72 | 0.16 |
| Weather icons | 0.03 | 0.02 | 1.02 | 0.963 | 0.02 | 0.53 |
| Asian emoticons | 1.91 | 0.94 | 1.88 | 0.732 | 0.32 | 0.82 |
| Pictish (217 lines) | 1.16 | 0.28 | 1.98 | 0.156 | 0.45 | 0.37 |
| Vinča (244 lines) | −0.03 | 0.05 | n/a | 0.323 | 0.62 | 0.25 |

("n/a": at 300 lines no recurring unit occurred in the controls, so S3 is undefined for that corpus in some resamples. This affects only corpora to be classified, not the leave-one-out decision, and the classification of these corpora is not reported as a result because G3 is undecided.)

Observations:
- The non-linguistic corpora are very heterogeneous. Asian emoticons have strong order and direction effects (S1 1.91, S2 0.94), stronger than any full-writing corpus, because emoticons are built from paired characters in fixed positions. Barn stars and weather icons have almost no order effects. A single "non-linguistic profile" does not exist in these data, which is the reason the check fails. This agrees with the caution of Sproat (2014) and Raghavendra (2026) that such statistics are not specific to language.
- Among all twelve corpora, the Indus corpus again stands next to proto-Elamite on every statistic (compare D1). The Indus corpus has a lower within-line repetition rate (0.034) than every corpus except the two proto-administrative ones (0.037, 0.016) and Pictish (0.156 is the next lowest). Low repetition is therefore shared with the proto-administrative systems rather than being unique to the Indus corpus.

### Status of the gates (end of the seventh working session)

| Gate | Status |
|---|---|
| G1 (L1 consolidated) | passed |
| G2 (L2) | not met |
| G3 (writing or not) | undecided: the available statistics cannot separate writing from non-linguistic systems |
| G4 (L3) | not attempted; under the work plan, WP-E results will be labelled conditional on the linguistic assumption |

The firm finding of phase 4 is comparative: the Indus inscriptions pattern with proto-Elamite (and, less closely, proto-cuneiform), the two proto-administrative systems of the late fourth millennium BCE in the reference set.

---

## 2026-11-25 (day 1, eighth working session): P1, sign × metadata scan

The scheduled task now runs hourly (the user asked for continuous work); a run that starts while another session is working waits for it.

### Pre-registration of C2 (association scan; before running)

**Units.** ICIT unique complete strings with recorded direction. For each metadata variable, a string is used only if all its records share one value.

**Variables and values.** Values with ≥ 30 training strings, for:
- object subtype (full `type` code, for example `SEAL:S`, `TAB:B`, `TAB:I`, `TAB:C`);
- material (lower-cased);
- motif (first part of `symbol`; blank, `-`, `Othr`, `Unknown` excluded);
- region (`region` field).

**Features.** Presence of each sign occurring in ≥ 15 training strings.

**Test.** For each (sign, value) pair: 2 × 2 table (sign present / absent) × (value / other values). For subtype, material and motif, a Cochran–Mantel–Haenszel test stratified by site (Harappa, Mohenjo-daro, other), so that site differences cannot produce an association by themselves. Region is a property of the site, so it is tested without stratification and its results are described as regional variation, not as meaning.

**Discovery.** Training split; Benjamini–Hochberg false-discovery rate q = 0.05 over all pairs.

**Confirmation.** Held-out split (the 14th question decided on it); each discovered pair is tested one-sided in its discovered direction with the same test; Bonferroni threshold 0.01 / (number of discovered pairs).

**Interpretation rule (fixed now).** A confirmed association counts toward L2 only if the sign involved belongs to a group already defined structurally (the terminal cluster, the stroke signs, the count–item targets) or the association is to an object class in a way that supports a semantic reading named in advance (stroke signs with tablets = "numerals on records", claim C31). Other confirmed associations are recorded as "confirmed sign–context associations" (L2 candidates), not as L2 results.

### C2 result: 40 associations discovered, 6 confirmed on held-out data

Script: `scripts/phase6_c2_association_scan.py`; results: `results/phase6_c2_association_scan.json`.

1,312 (sign, value) tests on the training split (82 signs); 40 pass the false-discovery-rate threshold; confirmation threshold on the held-out split 0.01/40 = 0.00025.

| Variable | Value | Sign | OR (train) | OR (held-out) | p (held-out) | Confirmed |
|---|---|---|---:|---:|---:|---|
| subtype | SEAL:R | 154 | 9.2 | 22.8 | 7.2 × 10⁻⁷ | yes |
| region | Inter-Riverine | 400 | 5.2 | 4.5 | 1.3 × 10⁻⁶ | yes (regional) |
| subtype | SEAL:R | 806 | 9.5 | 8.1 | 7.1 × 10⁻⁶ | yes |
| subtype | SEAL:R | 407 | 8.5 | 10.9 | 3.0 × 10⁻⁵ | yes |
| subtype | SEAL:S | 741 | 3.5 | 14.9 | 9.9 × 10⁻⁵ | yes |
| subtype | SEAL:S | 400 | 0.30 | 0.17 | 1.8 × 10⁻⁴ | yes (negative) |

Thirteen further associations have held-out p < 0.01 but miss the strict threshold, for example `TAB:B` × 400 (OR 3.3, p = 8.9 × 10⁻⁴), `TAB:C` × 407 (OR 6.1, p = 0.011), faience × 400 (OR 3.5, p = 0.0036).

**What `SEAL:S` and `SEAL:R` denote (from the data, not from a codebook).** Cross-tabulating the ICIT `shape` and `symbol` fields: `SEAL:R` objects are rectangular (153) or cuboid-convex (188) and almost never carry an animal motif (229 of 240 lines have none); `SEAL:S` objects carry a motif in most cases (`Bull1` 987 of 1,316 lines). `SEAL:R` therefore denotes rectangular seals without an animal motif, and `SEAL:S` the motif-bearing seals.

**Positions of the confirmed signs (all data, descriptive).** 154 is line-final in 85 % of its occurrences on `SEAL:R`; 407 in 58 % on `SEAL:R` and 59 % on `TAB:C`; 400 in 93 % on `TAB:B`; 740 in 80 % on `SEAL:S`. 741 and 806 are almost never line-final (final shares 0.01 and 0.00–0.03).

**Interpretation under the pre-registered rule.** Two confirmed associations involve members of the structurally defined terminal set (H3.1): 407 is favoured on rectangular seals without motif, and 400 is avoided on motif-bearing seals (and favoured on `TAB:B` tablets, below the strict threshold). Together with the descriptive positions, the pattern is that **the sign that closes a line varies with the kind of object**: 740 on motif-bearing seals, 407 and 154 on rectangular seals without motif and on copper tablets, 400 on `TAB:B` tablets. The test is stratified by site, so the pattern is not a difference between Harappa and Mohenjo-daro.

By the interpretation rule fixed before the scan, this counts toward L2. It is recorded as **L2 in narrow, functional scope**: the line-final signs form a category whose members predict the object class on held-out data. It does not identify what any of these signs means (for example "seal of", "tablet of", a title, or a commodity), and it is not a phonetic result. The associations of 806, 741 and 154 (154 is not in the terminal set as defined from the training data) are recorded as confirmed sign–context associations (L2 candidates).

Regional association: 400 is more frequent in the Inter-Riverine region (OR 4.5); this is regional variation and not interpreted.

### Gate G2

Met in narrow, functional scope (see above). A stronger L2 result would assign a specific meaning to a sign group and predict an external variable from it; this remains open.

### Pre-registration of F4 (C2 pattern on fresh sets 1 and 2; before running)

Among fresh-set strings (ICIT, sites excavated after 1979) whose records are all `SEAL:S` or all `SEAL:R`: the share of strings whose final sign is 407 or 154 is higher for `SEAL:R` than for `SEAL:S`. One-sided Fisher exact test, p < 0.01. If either class has fewer than 5 strings, the result is "insufficient data".

### F4 result: not supported (p = 0.0104)

Script: `scripts/phase6_f4_final_sign_fresh.py`; results: `results/phase6_f4_final_sign_fresh.json`.

On the fresh sets, 3 of 22 rectangular-seal strings end in 407 or 154, against 0 of 75 motif-seal strings. One-sided Fisher exact p = 0.0104, just above the threshold 0.01. By the pre-registered rule F4 is not supported. The direction agrees with C2, and the result is limited by the small number of rectangular seals in the fresh sets. The C2 result therefore rests on the held-out confirmation alone.

---

## 2026-11-25 (day 1, ninth working session): P2, the Sanskrit reading claim (C33)

### Materials

- The proposed readings: the `sanskrit` column of the ICIT-style source (3,831 records with an entry; entries of the form `ref:…` point to other records and are skipped). The readings are written in SLP1 transliteration with hyphens and spaces as word divisions. They are used here only as the object of the test, never as data for other analyses.
- The proposal's published procedure (https://github.com/yajnadevam/ScriptDerivation, commit `5835e8b`, `scripts/prove.sh`): it builds its dictionary from the Monier-Williams dictionary, keeps headwords that cite a source other than lexicographers only, and normalises both dictionary and readings by merging aspirated with plain stops, retroflex with dental consonants, all nasals with *n*, all sibilants with *s*, and the vocalic liquids with *r*, and by writing long vowels as double vowels.
- The Monier-Williams dictionary from the Cologne source files (`scripts/fetch_mw.py`; the Cologne site itself is blocked from the working environment, so the GitHub mirror of the same source file is used).

### Pre-registration of E2 (before running)

**Question.** How much evidence does "the reading can be divided into Sanskrit dictionary words" give, under the proposal's normalisation? If random letter strings can also be divided into dictionary words at a high rate, readability is weak evidence for the decipherment.

**Procedure.**
1. Dictionary: headwords (`k1`) of Monier-Williams entries that contain at least one `<ls>` citation other than `L.`, normalised as in `prove.sh`; only words of length ≥ 2 are used for segmentation.
2. Claimed readings: unique readings, brackets and parentheses removed, normalised in the same way, word divisions removed.
3. Segmentability: a string is segmentable if it can be divided completely into dictionary words (dynamic programming).
4. Controls, for each claimed reading: (a) 20 random strings of the same length drawn from the letter frequencies of all claimed readings; (b) 20 random reorderings of the reading's own letters.

**Outcomes reported.** Segmentability rate of the claimed readings, of control (a) and of control (b).

**Decision rule.** Readability is counted as *discriminating evidence* only if the rate for control (b) is below half the rate for the claimed readings (likelihood ratio > 2) **and** below 0.1. Otherwise it is recorded that, under the proposal's normalisation, readability as Sanskrit does not distinguish the proposed readings from random letter sequences of the same composition.

**Limits.** The proposal also uses an augmented dictionary with inflected forms (`data/aux.txt`, 35 entries, and declined forms not published as a list). Inflected forms are not added here, which lowers the rates for the claimed readings and for the controls alike. The test concerns the evidential value of the readability criterion, not the sign values themselves.

### E2 result: readability is not discriminating evidence

Script: `scripts/phase7_e2_sanskrit_readability.py`; results: `results/phase7_e2_sanskrit_readability.json`.

| Strings | Segmentable into dictionary words |
|---|---:|
| Proposed readings (1,757 unique) | 0.84 |
| Random letters, same length and letter frequencies | 0.29 |
| Reorderings of each reading's own letters | 0.29 |

Dictionary: 131,655 normalised headwords. The likelihood ratio of "segmentable" for the proposed readings against reordered letters is 0.84 / 0.29 ≈ 2.9.

By the pre-registered rule (control rate below half the claimed rate **and** below 0.1), readability is **not** discriminating evidence: under the proposal's normalisation, more than a quarter of random letter sequences of the same composition can be read as sequences of Sanskrit dictionary words. A ratio of about 3 would be weak evidence even for a single text, and it overstates the evidence here, because each proposed reading was chosen so that it matches the dictionary. A fair comparison would ask how much of the corpus could be made readable by an arbitrary assignment of sound values to signs with the same freedoms (inherent vowel optional, vowel length free, merged consonant classes). This is not computed here and is the natural next test.

Conclusion for claim C33: the published readings are mostly divisible into dictionary words, but under the normalisation used this property is shared by a large fraction of random strings, so it does not by itself support the decipherment. This agrees with the critical reception noted in the bibliography; it is not a demonstration that the proposed sign values are wrong.

### Methodological consequence for WP-E3

Any language-hypothesis test in this project must report the rate at which random or reordered strings pass the same acceptance criterion (as here), and must use a criterion with a control rate below 0.1 before readability can count as evidence.

### Pre-registration of E2b (before running)

**Question.** With the reading freedoms described in the proposal's README (a consonant sign may be read with or without the inherent vowel *a*; vowel length is free) and its normalisation, how much of the Indus corpus becomes readable under **random** sign-value assignments?

**Procedure.**
- Lines: ICIT unique complete lines with recorded direction (reading order), length ≤ 10, no damaged sign.
- Value inventory after normalisation: consonants {k, g, c, j, t, d, n, p, b, m, y, r, l, v, s, h}; vowels {a, i, u, e, o}.
- Random assignment: each sign type independently becomes a consonant (probability 0.8, uniform among consonants) or a vowel (0.2, uniform). A consonant sign is read as C or Ca; a vowel sign as V or VV (for e and o only the single form).
- A line is readable if some choice of these options gives a string that divides completely into dictionary words (the E2 dictionary, words of length ≥ 2).
- 20 random assignments.

**Outcome.** Mean and maximum share of readable lines over the 20 assignments, compared with the 0.84 segmentability of the proposed readings (E2).

**Decision rule.** If the mean share for random assignments is at least half of 0.84 (≥ 0.42), the reading freedoms alone make a large part of the corpus readable, and readability is recorded as no evidence for any particular assignment under these freedoms.

### E2b result: random assignments make the corpus as readable as the proposed readings

Script: `scripts/phase7_e2b_random_assignments.py`; results: `results/phase7_e2b_random_assignments.json`.

2,044 lines (≤ 10 signs, no damage), 603 sign types, 20 random sign-value assignments. Share of lines readable as complete sequences of Sanskrit dictionary words: mean **0.835**, range 0.713–0.920. The proposed readings reach 0.84 (E2).

By the pre-registered rule (mean ≥ 0.42) the reading freedoms alone make most of the corpus readable. An arbitrary assignment of sound values to the signs, drawn at random and not fitted in any way, yields as many "Sanskrit" readings as the published decipherment. Readability under these freedoms is therefore **no evidence** for any particular assignment, including the published one.

Remarks:
- The freedoms tested here are those stated in the proposal's README (optional inherent vowel, free vowel length) together with its normalisation. The proposal also allows sandhi and compound stems, which would make random assignments even more readable.
- The test does not show that the Indus inscriptions are not Sanskrit. It shows that this method cannot distinguish a correct assignment from a random one, so the published readings do not provide evidence either way.

### Consequence for the project (WP-E)

E2 and E2b give a concrete calibration for any phonetic decipherment attempt on this corpus: with short texts, a large dictionary and flexible reading rules, almost any assignment "reads". A phonetic hypothesis can count toward L3 only with a criterion whose rate under random assignments, computed as in E2b, is below 0.1. This requirement is added to gate G4.

---

## 2026-11-25 (day 1, tenth working session): replication of C2 in KP1979

### Pre-registration of C2k (before running)

KP1979 records an object-type code (`type_code`) for each inscription, taken from the 1973 concordance and assigned independently of the ICIT-style source. The codes are not decoded here, but they are categories of objects.

**Question.** Do the KP terminal signs (the KP terminal set of H3.1: 324, 98, 217, 326, 1, 13, 4, 301; plus 325) as line-final signs associate with KP type codes, replicating C2 in an independent transcription and classification?

**Procedure.**
- Units: KP unique complete lines; a line is used if all its records share one type code.
- Values: type codes with ≥ 30 training lines. Features: "line ends in sign t" for each t in the terminal set above.
- Test: Fisher exact test (two-sided) on the training split for each (final sign, code) pair; Benjamini–Hochberg q = 0.05; confirmation one-sided in the discovered direction on the KP held-out split, Bonferroni 0.01 / (number discovered). KP has no site field in decoded form, so no site stratification is possible; this is a limitation.
- Prediction: at least one association is confirmed.
- Interpretation: confirmed codes are then described by cross-tabulating, in the aligned line pairs of the concordance, KP type codes against ICIT subtypes (descriptive).

### C2k result: replicated in KP1979 (one association confirmed)

Scripts: `scripts/phase6_c2k_kp_typecodes.py` (pre-registered), `scripts/phase6_c2k_code_meaning.py` (descriptive); results: `results/phase6_c2k_kp_typecodes.json`, `results/phase6_c2k_code_meaning.json`.

72 tests (8 type codes × 9 final signs); 10 discovered (FDR 0.05); confirmation threshold 0.001.

| KP code | Final sign | OR (train) | OR (held-out) | p (held-out) | Confirmed |
|---|---|---:|---:|---:|---|
| 11 | 98 | 0.24 | 0.23 | 2.4 × 10⁻⁴ | yes |
| 75 | 98 | 6.9 | 10.1 | 1.0 × 10⁻³ | no (at threshold) |
| 62 | 98 | 4.9 | 5.8 | 6.1 × 10⁻³ | no |
| 11 | 324 | 1.6 | 2.2 | 5.2 × 10⁻³ | no |

**What the KP codes denote (identical texts in both corpora, descriptive).** Code 11 ↔ ICIT `SEAL:S` (346 of 371 matched texts); code 23 ↔ `SEAL:R` (43 of 48); codes 62 and 67 ↔ `TAB:B`; code 75 ↔ `TAB:I`; code 72 ↔ `TAB:C`.

**Interpretation.** The confirmed KP association says that motif-bearing seals (code 11) avoid ending a line with KP 98, which is the same sign as ICIT 400 (concordance purity 0.99). This is the C2 association "400 avoided on `SEAL:S`" reproduced in an independent transcription with an independent object classification (the 1973 codes). The tablet codes 75 (`TAB:I`) and 62 (`TAB:B`) favour line-final 98 on held-out data at p = 0.001 and 0.006, the same direction as `TAB:B` × 400 in C2, but below the strict threshold. KP has no decoded site field, so C2k is not stratified by site.

**Status of the functional L2 result.** The finding that line-final signs vary with the class of object, in particular that 400/98 closes tablet texts and is avoided on motif-bearing seals, is now confirmed on held-out data in two transcriptions with two independent object classifications. It remains a functional result: it says that the closing sign depends on the kind of document, not what the closing sign means.

---

## 2026-11-25 (day 1, eleventh working session): E3, calibrated phonetic-assignment search

### Idea

E2b showed that readability under flexible rules is no evidence. A different use of random and fitted sound values can be calibrated: for each candidate language, **search for the sign-to-sound assignment that best fits the training lines** under a statistical model of that language's sound sequences, and measure how much better the fitted assignment predicts **held-out lines** than random assignments do. If the inscriptions record language L phonetically, an assignment fitted under L should generalise better under L than assignments fitted under other languages. Because about 600 free signs can fit almost anything, only the held-out gain is used, and the whole procedure is first run on **known scripts whose language is hidden** (positive controls), to measure whether it can identify the right language at all.

### Pre-registration of E3 (before any code is run)

**Languages (sound-sequence models).** All texts are normalised to one reduced alphabet: consonants k g c j t d n p b m y r l v s h, vowels a i u e o (aspirates, retroflexes, nasals, sibilants and vowel length merged as in E2), with `#` as a word boundary.
- Sanskrit: Monier-Williams headwords (E2 dictionary source).
- Old Tamil: Sangam anthologies (Purananuru, Akananuru, Kuruntokai, Natrinai) from https://github.com/indic-corpora/sentamizh-corpus (commit `e833395`, Apache License 2.0), Tamil script transliterated by a fixed table.
- Sumerian: Old Babylonian literary texts (CDLI), graphemes of a word joined.
- Akkadian: Neo-Assyrian letters (CDLI), graphemes of a word joined.
- Pseudo-language: random strings with the pooled letter frequencies of the four languages (null model).
Model: letter trigram model with interpolated smoothing, trained on words of the language.

**Corpora to decipher.**
- Positive control 1: Akkadian Old Babylonian letters (CDLI) with every grapheme replaced by an opaque number (a cipher of a known syllabic script); lines of 2–10 signs.
- Positive control 2: Sumerian Ur III administrative texts (CDLI) as a cipher in the same way; lines of 2–10 signs (short administrative lines, closer to the Indus texts).
- Indus: ICIT unique complete lines, reading order.
Each corpus is limited to 2,000 unique lines and split 80/20 at random (Indus: the fixed held-out split).

**Assignment and search.** The 100 most frequent signs of the training lines receive values from one inventory used for all languages: V (5), CV (80) or C (16), 101 values in all; any other sign breaks the line into separately scored segments. For each (corpus, language) pair: coordinate ascent over signs (each sign in turn takes the value that maximises training log-probability), 4 sweeps, 2 random restarts; the best restart is kept.

**Measure.** Δ_L = mean held-out log-probability per sign under the fitted assignment minus the mean over 20 random assignments, for language L. Bootstrap over held-out lines (1,000 resamples) for the difference between the best and second-best language.

**Decision rules.**
1. The method has power only if, in **both** positive controls, the true language has the largest Δ and its difference to every other language has bootstrap p < 0.01. If not, the Indus results are reported as uninterpretable and no language preference is claimed.
2. If the method has power, a language is *favoured* for the Indus inscriptions only if its Δ exceeds that of every other language and of the pseudo-language with bootstrap p < 0.01.
3. Even a favoured language is not an L3 result: L3 needs sign values that predict held-out texts under a criterion with a random-assignment pass rate below 0.1 (gate G4). A favoured language would be recorded as conditional evidence, on the assumption that the signs record sounds.

**Untested hypothesis.** No usable Munda text corpus was found, so a Munda hypothesis is not tested.

**Amendment to E3 (before any result was computed).** The Neo-Assyrian letters in the CDLI dump yield only 643 Akkadian words after filtering, too few for a language model. The Akkadian model is instead trained on **Old Assyrian letters** (23,032 words): a different dialect and period from the Old Babylonian letters used as positive control 1, so the control remains a related-language decipherment, not an identity match. Word counts of the other models: Sanskrit 175,177 headwords; Old Tamil 79,353 word tokens; Sumerian (OB literary) 174,781 word tokens.

### E3 result: the method has no power (positive control 2 fails); no language preference is claimed

Script: `scripts/phase7_e3_phonetic_search.py`; results: `results/phase7_e3_phonetic_search.json`, fitted assignments in `results/phase7_e3_assignments.json`.

Mean held-out gain per sign over random assignments (nats):

| Corpus | Sanskrit | Old Tamil | Sumerian | Akkadian | Pseudo |
|---|---:|---:|---:|---:|---:|
| Cipher: Akkadian OB letters (true: Akkadian) | 3.64 | 4.59 | 4.73 | **5.21** | 4.39 |
| Cipher: Sumerian Ur III administrative (true: Sumerian) | 3.61 | 4.31 | 4.39 | **5.08** | 4.21 |
| Indus | 3.67 | 4.53 | 4.67 | **5.23** | 4.31 |

All bootstrap differences between the first and the other languages have p = 0.001.

By decision rule 1 the method has **no power**: positive control 2 picks Akkadian instead of Sumerian. The table shows why. The ranking is the same for all three corpora (Akkadian > Sumerian > Tamil > pseudo-language > Sanskrit), including the Indus corpus. The gain therefore measures a property of each language model, most likely how concentrated its letter distribution is (the Akkadian model is trained on the smallest corpus and is the most peaked; the Sanskrit model, on a large and varied headword list, the least), not how well a language fits the corpus. The "success" of positive control 1 is an artefact of the same effect.

Conclusion: E3 provides no evidence for any language. The Indus result "Akkadian first" is the artefact and must not be read as a finding. This is recorded as a failed method, which is itself useful: it shows that a held-out gain over random assignments is not comparable across languages.

### Pre-registration of E3b (corrected measure; before running)

To remove the language-model effect, each language's gain on a corpus is compared with its gain on a **control version of the same corpus** in which the signs of every line are randomly reordered (same signs, same line lengths; sequential structure destroyed; the same reordering for all languages):

Δ′_L = gain_L(real corpus) − gain_L(reordered corpus).

The language-model effect affects both terms alike and cancels; what remains is how much the sequential structure of the corpus agrees with the sound sequences of language L. Everything else (models, search, held-out split, 4 sweeps, 2 restarts, bootstrap) is as in E3; the bootstrap is over held-out lines, pairing each real line with its reordered version.

Decision rules as in E3, applied to Δ′: the method has power only if both positive controls rank their true language first with p < 0.01 against every other language; only then is an Indus preference considered.

### E3b result: the corrected method also has no power

Script: `scripts/phase7_e3b_corrected.py`; results: `results/phase7_e3b_corrected.json`.

Mean Δ′ per sign (gain on real lines minus gain on within-line reordered lines, held-out):

| Corpus | Sanskrit | Old Tamil | Sumerian | Akkadian | Pseudo |
|---|---:|---:|---:|---:|---:|
| Cipher: Akkadian OB letters (true: Akkadian) | **0.285** | 0.161 | 0.111 | 0.158 | −0.007 |
| Cipher: Sumerian Ur III administrative (true: Sumerian) | **0.229** | 0.166 | 0.099 | 0.149 | 0.006 |
| Indus | **0.294** | 0.154 | 0.117 | 0.086 | 0.006 |

Both positive controls rank Sanskrit first, not their true language; by decision rule 1 the method has **no power**, and no language preference is claimed for the Indus inscriptions. The Indus row has the same shape as the two control rows, which again indicates a property of the language models (here, the Sanskrit headword list, which contains many long compounds with repeated internal patterns), not a property of the corpus.

One part of the result is consistent across all three corpora: every real-language model gains more from the real line order than from reordered lines (Δ′ > 0.08), whereas the pseudo-language gains nothing (Δ′ ≈ 0). The sequential structure of the Indus lines, like that of the two cuneiform ciphers, is exploitable by the sound-sequence model of any natural language. This says that the Indus sign order has language-like local regularities of some kind; it does not identify a language, and it does not distinguish writing from a structured notation (gate G3).

### What E2–E3b establish about phonetic decipherment of this corpus

1. Readability under flexible rules is reached by random assignments as often as by a published decipherment (E2b).
2. Fitting sign values under a language's sound-sequence model cannot identify the language of a hidden **known** syllabic script of comparable size, by two different measures (E3, E3b).

With a corpus of about 2,000 short lines, unconstrained phonetic fitting does not have the power to choose among candidate languages. Any future L3 attempt in this project therefore needs an additional, independent constraint before it can be calibrated: for example bilingual evidence, proper names known from outside the script (claims register, external names), or pictographic (rebus) constraints fixed in advance from the sign drawings. These are the remaining routes; they are added to the work plan.

---

## 2026-11-25 (day 1, twelfth working session, 09:18 UTC): E3c, how much data would the phonetic search need?

E3 and E3b failed even on known scripts hidden as ciphers of 2,000 lines. Two explanations are possible: the corpus is too small, or the method is unsuitable at any size. The answer matters for the final report, because it says whether a phonetic search of the Indus corpus (about 2,000 lines) can succeed in principle.

### Pre-registration of E3c (power curve; before running)

- Corpora: the two positive-control ciphers of E3 (Akkadian OB letters; Sumerian Ur III administrative), built in the same way but with **8,000** lines each (80/20 split).
- Languages, models, search, measure Δ′ (E3b), bootstrap and decision rule as in E3b.
- Outcome: for each cipher, whether its true language ranks first with p < 0.01 against every other language at 8,000 lines (the 2,000-line result is E3b).
- Interpretation fixed in advance: if both ciphers succeed at 8,000 lines, the method has power only above the size of the Indus corpus, and the Indus corpus is too small for it. If either fails at 8,000 lines, the method is recorded as unsuitable for this task at the sizes tested.

### E3c result: no power at 8,000 lines either

Script: `scripts/phase7_e3c_power.py`; results: `results/phase7_e3c_power.json`. (A first run failed before computing anything because the worker processes could not import the helper modules; fixed and re-run.)

| Cipher (8,000 lines) | Sanskrit | Old Tamil | Sumerian | Akkadian | Pseudo | First |
|---|---:|---:|---:|---:|---:|---|
| Akkadian OB letters | **0.287** | 0.218 | 0.146 | 0.168 | 0.006 | Sanskrit (wrong) |
| Sumerian Ur III administrative | **0.189** | 0.184 | 0.081 | 0.105 | 0.004 | Sanskrit (wrong; not clearly ahead of Tamil, p = 0.38) |

With four times as much data the method still ranks Sanskrit first for both known scripts. By the rule fixed in advance, the method is **unsuitable for this task at the sizes tested**; the failure is not a matter of corpus size in the range 2,000–8,000 lines. The Sanskrit model's advantage appears to come from its word list (many long compounds with internal repetition), which any assignment can exploit, independently of the language of the cipher.

### Assessment of the remaining L3 routes (P4e, P4f)

The calibration rule adopted after E2b and E3 requires that a phonetic method be shown to identify the language of a known script hidden as a cipher before its result on the Indus corpus is interpreted.
- **P4e (rebus-constrained fitting)** needs, for its positive control, a known script whose signs are pictographs with known referents and known readings, in a comparable corpus. The reference corpora available here (proto-cuneiform, proto-Elamite, Sumerian, Akkadian) are transliterated by sign names or readings, not by depicted objects, so a calibrated positive control cannot be built with the data at hand. The identification of Indus pictographs would also rest on my own reading of the sign drawings (for example the fish family), which is not an independent source.
- **P4f (external names)** needs a list of names that external sources connect with the Indus region, in a form specific enough to test. The sources seen in this project (claims register) give the region name *Meluhha* and a few individuals, not a set of names large enough for a calibrated test.

Conclusion: under the standards of this project, no calibrated route to L3 is available with the data and sources accessible here. This is recorded as the outcome of WP-E. The remaining time is better used to strengthen and extend the L1 and L2 results and to prepare the reports.

### Pre-registration of C3 (Q1; before running)

Same units, object-subtype values (≥ 30 training strings), site-stratified Cochran–Mantel–Haenszel test, discovery on the training split with false-discovery rate q = 0.05 and confirmation on the held-out split (15th question on it; Bonferroni 0.01/number discovered) as in C2, but with these features:
- **penultimate sign**: "the sign immediately before the final sign is t", for every t occurring in that position in ≥ 15 training strings (strings of length ≥ 2);
- **constructions**: "contains a short-stroke sign" (ICIT 001, 003, 004, 034, 005, 016, 017), "contains a long-stroke sign" (031, 032, 033, 035), "contains a count–item pair" (as defined in `src/indus/controls.py`), "line length ≥ 5".

Prediction: at least one association is confirmed. Interpretation rule: confirmed associations of the constructions count toward L2 (a structurally defined category predicting object class); confirmed penultimate-sign associations are L2 candidates unless the sign belongs to the terminal set.

### C3 result: one association confirmed (text length), not counted as L2

Script: `scripts/phase6_c3_penultimate_constructions.py`; results: `results/phase6_c3_penultimate_constructions.json`.

162 tests (27 features × 6 object subtypes); 5 discovered; confirmation threshold 0.002.

| Subtype | Feature | OR (train) | OR (held-out) | p (held-out) | Confirmed |
|---|---|---:|---:|---:|---|
| TAB:I | length ≥ 5 | 0.21 | 0.21 | 1.0 × 10⁻³ | yes |
| SEAL:S | length ≥ 5 | 1.80 | 1.50 | 0.042 | no |
| POT:T:g | length ≥ 5 | 0.03 | 1.34 | 0.61 | no |
| SEAL:R | has short-stroke sign | 2.15 | 1.54 | 0.15 | no |
| TAB:B | penultimate sign 740 | 2.10 | 2.13 | 0.033 | no |

The only confirmed association is that `TAB:I` texts are short. Applied literally, the pre-registered rule would count "length ≥ 5" as a construction and therefore toward L2. I do not count it: text length is a physical property of small objects, not a semantic category, and listing it among the constructions was a mistake in the pre-registration. The decision is recorded here as stricter than the rule. Neither the count–item construction nor the stroke signs nor any penultimate sign is confirmed to vary with object class. The functional L2 result therefore remains limited to the closing sign (C2, C2k).

---

## 2026-11-25 (day 1, thirteenth working session): review pass (WP-F1)

### Finding: near-duplicates between training and held-out strings

The held-out split is defined on exact strings, so identical texts never cross the split. Near-identical texts can: strings that differ by one sign (a reading variant, a damaged copy, an extra stroke) fall on different sides at random. Counted now:
- ICIT: 166 of 396 held-out strings (42 %) have a training string within edit distance 1;
- KP1979: 204 of 431 (47 %).

Held-out tests therefore partly measured agreement between near-copies, which makes them easier than intended. This affects every result decided on the held-out split.

### Pre-registration of R1 (before running)

The supported held-out results are re-decided on the **strict held-out set**: held-out strings with no training string within edit distance 1. Tests and thresholds are those originally registered:
- H3.3 (terminal-cluster order; ≥ 0.8 agreement and binomial p < 0.01, both corpora);
- H3.10 (4–9 strokes → target group; Fisher p < 0.01, both corpora);
- H3.12a and H3.12b (count-specific pairs; p < 0.005 each, both corpora);
- C2 (the six confirmed associations; threshold 0.01/40);
- C2k (KP code 11 × final 98; threshold 0.001).
A result keeps its status only if it passes on the strict set; otherwise its status is downgraded in the README and the reports, with the reason. Results decided on fresh data (F2, F3, B1, B4) are unaffected, because the fresh sites are disjoint from the training corpus by date of excavation; they are listed for completeness.

### R1 result: L1 results survive; the L2 result is downgraded to a candidate

Script: `scripts/review_r1_strict_heldout.py`; results: `results/review_r1_strict_heldout.json`. Strict held-out sets: ICIT 230 of 396 strings, KP1979 227 of 431.

| Result | Corpus | Strict held-out | Passes original criterion |
|---|---|---|---|
| H3.3 terminal order | ICIT | 21 / 22 agree, p = 5.5 × 10⁻⁶ | yes |
| H3.3 terminal order | KP1979 | 14 / 15 agree, p = 4.9 × 10⁻⁴ | yes |
| H3.10 4–9 strokes → target | KP1979 | OR 23.1, p = 3.3 × 10⁻⁶ | yes |
| H3.10 4–9 strokes → target | ICIT | OR 19.0, p = 2.5 × 10⁻⁴ | yes |
| H3.12a 7 strokes → 288/289 (585/575) | KP1979 / ICIT | p = 5.1 × 10⁻⁴ / 4.0 × 10⁻⁷ | yes / yes |
| H3.12b 3 long → 217 (520) | KP1979 / ICIT | p = 1.1 × 10⁻⁷ / 1.5 × 10⁻⁶ | yes / yes |
| C2 SEAL:R × 806 | ICIT | OR 7.1, p = 3.1 × 10⁻⁴ | no (threshold 2.5 × 10⁻⁴) |
| C2 SEAL:S × 741 | ICIT | OR 12.7, p = 3.2 × 10⁻⁴ | no |
| C2 SEAL:R × 407 | ICIT | OR 8.7, p = 9.3 × 10⁻⁴ | no |
| C2 SEAL:R × 154 | ICIT | OR 13.5, p = 1.7 × 10⁻³ | no |
| C2 region × 400 | ICIT | OR 3.6, p = 1.9 × 10⁻³ | no |
| C2 SEAL:S × 400 | ICIT | OR 0.18, p = 4.0 × 10⁻³ | no |
| C2k code 11 × final 98 | KP1979 | OR 0.22, p = 0.013 | no (threshold 0.001) |

**L1.** All structural held-out results (H3.3, H3.10, H3.12a, H3.12b) pass their original criteria on the strict sets in both corpora. Together with the fresh-data results (F2, F3, B1, B4), the L1 status stands.

**L2.** The effect sizes of the C2 and C2k associations are almost unchanged on the strict sets (for example SEAL:R × 407: OR 10.9 → 8.7; code 11 × 98: OR 0.23 → 0.22), but with about half the data none reaches the strict multiple-comparison thresholds. By the rule registered for R1, the L2 result is **downgraded to an L2 candidate**: the association between closing sign and object class is consistent in two transcriptions and survives the removal of near-duplicates in direction and size, but it is not confirmed at the registered level once near-duplicates are excluded. The strict held-out data have now been looked at for this question, so a confirmatory test needs new data.

**Lesson for later tests.** All future held-out tests use the strict held-out set by default (`strict_heldout` in `src/indus/corpus.py`).

---

## 2026-11-25 (day 1, thirteenth working session, continued): E3d, equalised running-text models

### Why another attempt

In E3–E3c the language models differed in kind and size: Sanskrit was a list of 175,177 dictionary headwords (no running text), the Akkadian model was trained on 23,032 words, the others on running texts of 80,000–175,000 words. The rankings followed these differences (E3: smallest model first; E3b/E3c: headword list first). If the failure is caused by unequal models rather than by the method itself, equalising the models should restore power on the positive controls.

### Pre-registration of E3d (before running)

- **Models.** All five trained on exactly **20,000 running-text word tokens**, taken deterministically (random sample of sentences/lines with a fixed seed, then the first 20,000 words):
  - Sanskrit: the Ṛgveda text layer of the Digital Corpus of Sanskrit (O. Hellwig; CC BY 4.0; via https://github.com/tokushige-koyasan/dcs-corpus, commit `edea664`; `scripts/fetch_rgveda.py`), IAST normalised to the common alphabet;
  - Old Tamil: Sangam anthologies (as in E3);
  - Sumerian: Old Babylonian literary texts (as in E3);
  - Akkadian: Old Assyrian letters (as in E3);
  - pseudo-language: random words with the pooled letter frequencies of the four.
- **Corpora, search, measure.** As in E3b (Δ′, real minus within-line reordered, held-out lines, 2,000-line ciphers), except that the Indus held-out set is the **strict** held-out set.
- **Decision rules.** As in E3: the method has power only if both positive controls rank their true language first with bootstrap p < 0.01 against every other language; only then is an Indus language preference considered, and even then it is conditional evidence, not L3.

### Pre-registration of Q2a (zone agreement across transcriptions; before running)

Positional zones (initial / medial / terminal, defined as in B1: initial share ≥ 0.5 → initial; final share ≥ 0.5 → terminal; otherwise medial; signs with ≥ 10 training occurrences) are computed **independently** in the ICIT and KP1979 training splits. For concordance pairs with support ≥ 3, purity ≥ 0.8 and a one-to-one link, the share of pairs with the same zone is compared with 10,000 permutations of the KP zone labels among the pairs. Prediction: agreement above the permutation distribution, p < 0.01. (This is a reproducibility check of a descriptive classification; the two transcriptions describe largely the same objects.)

### Q2a result: zones agree across transcriptions (supported); sign-class table written

Script: `scripts/phase3_q2_sign_classes.py`; results: `results/phase3_q2a_zone_agreement.json`, `results/sign_classes.tsv`, `docs/SIGN_CLASSES.md`.

For 58 one-to-one linked signs, the independently computed zones agree in 53 cases (0.91); permutation mean 0.64 (SD 0.04), p = 0.0001. All five terminal-zone and all five initial-zone signs of the linked set agree; the five disagreements are between the medial zone and one of the others. The positional classification is a property of the signs, not of a particular transcription.

`docs/SIGN_CLASSES.md` lists the 80 ICIT signs with at least 20 occurrences, with their KP1979 equivalent, zones in both transcriptions, positional shares and the roles established by the tests of this project (terminal set, stroke counts, count–item targets, fish-shaped family, C2 candidate associations).

### E3d result: no power with equalised models either

Script: `scripts/phase7_e3d_equalised.py`; results: `results/phase7_e3d_equalised.json`.

| Corpus | Sanskrit (Ṛgveda) | Old Tamil | Sumerian | Akkadian | Pseudo | First (p vs second) |
|---|---:|---:|---:|---:|---:|---|
| Cipher: Akkadian OB letters | 0.178 | **0.203** | 0.133 | 0.160 | −0.002 | Tamil (p = 0.25 vs Sanskrit) — wrong |
| Cipher: Sumerian Ur III admin. | **0.184** | 0.183 | 0.108 | 0.139 | 0.010 | Sanskrit (p = 0.50 vs Tamil) — wrong |
| Indus (strict held-out) | 0.113 | **0.176** | 0.103 | 0.092 | −0.022 | Tamil (p = 0.07 vs Sumerian) |

With equal amounts of running text for every model, the large gaps between languages seen in E3–E3c disappear, which confirms that those gaps came from the models. But the positive controls still fail: neither cipher ranks its true language first, and no language is clearly ahead for either cipher. By decision rule 1 the method has **no power**, and the Indus row is **not interpreted**: Old Tamil ranks first for the Indus corpus, but it also ranks first for the Akkadian cipher, and it is not clearly ahead (p = 0.07). This row must not be cited as support for a Dravidian reading.

### Conclusion on phonetic fitting (E3–E3d)

Four variants (raw gain; gain corrected by reordered lines; 8,000-line ciphers; equalised running-text models) all fail to identify the language of known cuneiform texts hidden as ciphers. The only stable result across them is that every natural-language model gains from the real sign order while a pseudo-language does not. Phonetic fitting by sound-sequence models is closed as a route in this project.

### Pre-registration of H6.1 (two numeral series tied to different items; fresh data; before running)

**Idea.** In proto-cuneiform, different numerical sign systems are used for different kinds of goods (the counted item determines the notation). D1 placed the Indus corpus next to proto-cuneiform and proto-Elamite. The Indus script has two stroke series, short strokes and long strokes. If they are two numeral notations for different classes of items, they should be followed by different signs.

**H6.1.** On fresh sets 1 and 2 (ICIT, post-1979 sites; not yet used for any stroke question except F2, which tested only short strokes 4–9), the signs following short-stroke signs {001, 003, 004, 034, 005, 016, 017} and those following long-stroke signs {031, 032, 033, 035} differ in distribution.
- Follower classes fixed from earlier training-split results: A = {390, 405, 406, 407, 585, 575} (short-stroke partners, H3.10, H3.12a); B = {520} (long-stroke partner, H3.12b); C = all other signs and the line end.
- Test: chi-square test of independence on the 2 × 3 table (series × follower class); Fisher-type exact p by 10,000 permutations of series labels.
- Prediction: p < 0.01. If either series has fewer than 10 occurrences in the fresh sets, the result is "insufficient data".
