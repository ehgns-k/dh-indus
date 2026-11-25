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
