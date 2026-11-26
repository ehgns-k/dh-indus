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

### H6.1 result: supported on fresh data

Script: `scripts/phase6_h61_numeral_series.py`; results: `results/phase6_h61_numeral_series.json`.

| Series (fresh sets 1+2) | Followed by A (390–407, 585, 575) | Followed by B (520) | Other / line end |
|---|---:|---:|---:|
| Short strokes (30) | 8 | 0 | 22 |
| Long strokes (27) | 0 | 4 | 23 |

χ² = 11.9; permutation p = 0.0012 (< 0.01). **H6.1 is supported.** At sites excavated after 1979, the short and long stroke series take disjoint sets of partner signs: short strokes go with the 390–407 group and 585/575, long strokes with 520, never the reverse.

Interpretation and level. This is the pattern expected if the two series are two numeral notations used for different classes of counted items, as in proto-cuneiform, where the kind of goods determines the numerical system. The result is structural (L1): the prediction concerns signs inside the text, not information outside it, so it does not meet the ROADMAP definition of L2. It is, however, the most specific evidence so far for a **numeral-system reading** of the stroke signs: counts, series and partner signs form a consistent system that is reproduced on independent finds.

---

## 2026-11-25 (day 1, fourteenth working session): long-horizon project L-1 (numeral system)

### Descriptive (training split): stroke signs in sequence

Lines by number of stroke signs (training): KP1979 0: 993, 1: 461, 2: 186, 3: 40, 4: 11, 5: 1; ICIT 0: 985, 1: 568, 2: 98, 3: 12. Adjacent stroke–stroke pairs are frequent in KP1979 (long 1 + long 1: 61; short 1 + short 1: 42; short 1 + long 1 and long 1 + short 1: 37 each) but rare in ICIT (largest: short 1 + short 4: 6; short 1 + short 3: 6; long 3 + long 3: 5).

### Split/merge differences between the transcriptions (descriptive)

Script: `scripts/phase3_split_merge_strokes.py`; results: `results/phase3_split_merge.json`. ICIT strings (mapped to KP numbering) were compared with KP strings that differ only in that one ICIT sign corresponds to two KP signs. The recurring cases include:

| ICIT sign | KP pair | Cases | Example (ICIT / KP) |
|---|---|---:|---|
| 032 | 144 144 | 15 | `032 226` / `144 144 57` |
| 032 | 121 144 | 14 | `032 390 001 004 900 154` / `121 144 86 121 124 154 4` |
| 032 | 121 121 | 12 | `032` / `121 121` |
| 032 | 144 121 | 9 | `003 645 032 590` / `123 240 144 121 276` |

(Other entries of the table, for example ICIT 740 ↔ KP `325 98`, are partly coincidental matches between different texts and are not interpreted.)

**Finding.** A pair of single strokes that KP1979 writes as two signs (121/144 in any combination) is written by the ICIT-style source as one sign, 032, which elsewhere corresponds to KP 145 (two long strokes). The frequent single-stroke chains of KP1979 are therefore mostly a transcription convention for a **two-stroke** sign, not sequences of separate "1"s.

**Consequences.**
- The KP count distribution over-counts "1" and under-counts "2" (KP 122 is rare because two strokes are mostly written 121 121 or 144 144).
- Tests that used counts 3–9 (H3.10, H3.12, F2) and the ICIT sets of H6.1 are not affected. The KP part of H3.8/H3.9 included 121 (count 1) and is affected: part of the "count 1" occurrences are halves of a two-stroke sign. Those tests were not supported in any case; their conclusion does not change.
- For future numeral work, KP sequences 121/144 + 121/144 should be treated as one two-stroke sign, and ICIT 032 as "two strokes". This normalisation is added to the work plan (L-3) and is applied in the next tests.

### Pre-registration of L3a (are KP-merged ICIT signs contextually distinct? before running)

**Groups.** From the concordance (support ≥ 3, purity ≥ 0.8): KP signs that receive two or more ICIT signs, keeping ICIT members with ≥ 15 occurrences in the ICIT training split. All pairs within such groups are tested.

**Statistic.** Jensen–Shannon divergence between the context distributions of the two ICIT signs (previous sign or line start, and next sign or line end, pooled), training split.

**Null (free variation).** For each pair (a, b) with occurrence counts n_a and n_b: the occurrences of both are pooled and randomly relabelled into groups of sizes n_a and n_b (1,000 times); p = share of relabellings with divergence at least as large as observed. Under the null the two signs are interchangeable variants of one sign.

**Decision.** Bonferroni over the number of pairs at 0.01. A pair below the threshold is recorded as **contextually distinct** (the ICIT distinction is supported by usage, and the KP merger loses information); otherwise as **not distinguishable** (consistent with allographs). This is a descriptive classification decided on the training split.

### L3a result: three of ten KP-merged pairs are contextually distinct

Scripts: `scripts/phase3_l3a_allographs.py` (pre-registered, 1,000 relabellings), `scripts/phase3_l3a_allographs_10k.py` (robustness check, 10,000 relabellings); results: `results/phase3_l3a_allographs.json`, `results/phase3_l3a_allographs_10k.json`.

Eight KP signs receive two or more frequent ICIT signs; 10 pairs; threshold 0.01/10 = 0.001.

| KP sign | ICIT pair | n | JS (null mean) | p (1,000) | p (10,000) | Final share | Decision |
|---|---|---|---|---:|---:|---|---|
| 1 | 151 / 158 | 44 / 16 | 0.80 (0.60) | 0.0010 | 0.0001 | 0.89 / 0.38 | distinct |
| 325 | 617 / 741 | 32 / 118 | 0.89 (0.70) | 0.0010 | 0.0001 | 0.56 / 0.03 | distinct |
| 86 | 390 / 407 | 142 / 43 | 0.57 (0.49) | 0.0010 | 0.0005 | 0.46 / 0.67 | distinct |
| 364 | 803 / 806 | 75 / 61 | 0.61 (0.50) | 0.0020 | 0.0001 | 0.00 / 0.00 | not distinguishable by the registered test (distinct in the robustness check) |
| 4 | 154 / 156 | 25 / 31 | 0.60 (0.53) | 0.015 | 0.016 | 0.84 / 0.81 | not distinguishable |
| 86 | 405 / 407 | 43 / 43 | 0.49 (0.44) | 0.070 | 0.059 | 0.53 / 0.67 | not distinguishable |
| 383 | 817 / 861 | 99 / 131 | 0.38 (0.37) | 0.11 | 0.11 | 0.04 / 0.05 | not distinguishable |
| 86 | 390 / 405 | 142 / 43 | 0.50 (0.48) | 0.19 | 0.21 | 0.46 / 0.53 | not distinguishable |
| 355 | 790 / 850 | 18 / 20 | 0.71 (0.68) | 0.25 | 0.26 | 0.22 / 0.10 | not distinguishable |
| 316 | 705 / 706 | 83 / 42 | 0.51 (0.52) | 0.68 | 0.70 | 0.01 / 0.02 | not distinguishable |

Note on resolution: with 1,000 relabellings the smallest attainable p is 0.000999, just below the threshold 0.001; the three pairs that pass do so at that floor. The 10,000-relabelling check confirms them (p ≤ 0.0005) and would add 803/806; the registered decision is kept, and 803/806 is reported as distinct only in the robustness check.

**Findings.**
- **617 / 741 (both KP 325, the most frequent "jar"-type sign).** 741 is almost never line-final (0.03), 617 often is (0.56). KP1979 merges a sign that closes lines with one that never does. In KP-based analyses, sign 325 therefore mixes two distinct usages.
- **151 / 158 (both KP 1).** 151 is a closing sign (0.89 final), 158 is not (0.38).
- **390 / 407 (both KP 86).** 407 is more often line-final (0.67 vs 0.46) and differs in context; 405 cannot be distinguished from either.
- Seven pairs show no detectable difference and are consistent with free variants (allographs) at this sample size, for example 817 / 861 (both line-initial signs, KP 383) and 705 / 706 (KP 316).

**Consequence.** The ICIT distinctions 617/741, 151/158 and 390/407 are supported by usage; analyses that merge them (KP numbering) lose information. This is recorded in `docs/SIGN_CONCORDANCE.md`.

### Pre-registration of L3b (reverse direction; before running)

Same test as L3a in the other direction: ICIT signs that receive two or more frequent KP signs (concordance rows with support ≥ 3 and purity ≥ 0.5, grouped by ICIT sign; KP members with ≥ 15 occurrences in the KP training split); contexts from the KP training split; 1,000 relabellings; Bonferroni 0.01 / number of pairs.

### L3b result: none distinct by the registered test (design flaw); six pairs distinct in the robustness check

Scripts: `scripts/phase3_l3b_allographs_kp.py` (registered), `scripts/phase3_l3b_allographs_kp_10k.py` (robustness check); results: `results/phase3_l3b_allographs_kp.json`, `results/phase3_l3b_allographs_kp_10k.json`.

**Design flaw in the registration.** With 15 pairs the threshold is 0.01/15 = 0.00067, below the smallest p attainable with 1,000 relabellings (0.000999). The registered test therefore could not declare any pair distinct, and by the registered rule **no pair is distinct**. The flaw is recorded here; from now on the number of relabellings is set so that the smallest attainable p is at most one tenth of the threshold. In addition, the pair 121/144 entered twice (as members of ICIT 001 and of ICIT 031), so there are 14 distinct pairs, not 15.

Robustness check with 10,000 relabellings (threshold unchanged), unique pairs:

| ICIT sign | KP pair | p (10,000) | Final shares | Note |
|---|---|---:|---|---|
| 001 / 031 | 121 / 144 | 0.0001 | 0.08 / 0.07 | short vs long single stroke differ in context |
| 002 | 119 / 122 | 0.0001 | 0.03 / 0.18 | |
| 033 | 123 / 147 | 0.0001 | 0.05 / 0.08 | three short vs three long strokes differ |
| 240 | 50 / 62 | 0.0001 | 0.06 / 0.01 | fish-shaped variants |
| 240 | 56 / 62 | 0.0001 | 0.05 / 0.01 | fish-shaped variants |
| 740 | 324 / 325 | 0.0001 | 0.71 / 0.56 | the two KP "jar" variants differ |

Not distinguishable: 50/56, 50/58, 56/58 (fish-shaped variants), 324/326, 325/326.

**Findings (robustness level).**
- The ICIT-style source merges some distinctions that KP1979 makes and that are visible in usage: short vs long strokes (KP 121/144 → ICIT 001 or 031; KP 123/147 → ICIT 033), the jar variants KP 324/325 (→ ICIT 740), and some fish-shaped variants.
- **Consequence for earlier tests.** ICIT 033 was used as "three long strokes" (H3.12b, H6.1). The concordance shows that ICIT 033 also covers some KP 123 (three short strokes) occurrences. In H6.1 this would, if anything, mix the two series and weaken the separation that was found; it cannot create it. H3.12b was confirmed in KP1979 with the unambiguous KP 147, so its conclusion stands.
- Neither transcription is uniformly finer: each merges distinctions that the other keeps and that matter in usage. A combined sign inventory that keeps all usage-supported distinctions from both lists would be the best basis for further work (work plan L-3).

### D3 (descriptive): estimated size of the sign inventory

Script: `scripts/phase4_d3_inventory.py`; results: `results/phase4_d3_inventory.json`. Classic Chao1 estimator of the total number of sign types, with the variance of Chao (1987) and a log-normal 95 % interval, all corpora at 9,000 tokens from unique lines (Pictish and totem poles: all their tokens). A first version used a token bootstrap for the interval, which is biased for this estimator (its intervals did not contain the estimate); it was replaced before any result was recorded.

| Corpus | Observed types | Singletons | Chao1 | 95 % interval |
|---|---:|---:|---:|---|
| Indus (ICIT) | 601 | 212 | 830 | 762–928 |
| Indus (KP1979) | 359 | 100 | 511 | 448–617 |
| proto-Elamite | 554 | 180 | 820 | 732–950 |
| proto-cuneiform | 859 | 327 | 1,383 | 1,247–1,568 |
| Sumerian Ur III administrative | 680 | 206 | 933 | 855–1,044 |
| Sumerian OB literary | 766 | 288 | 1,133 | 1,035–1,267 |
| Akkadian OB letters | 451 | 138 | 612 | 555–702 |
| Pictish (764 tokens) | 85 | 38 | 145 | 111–225 |

Observations:
- The two Indus transcriptions differ in granularity (ICIT about 830 types, KP1979 about 510), as expected from the split/merge differences (L3a, L3b). Either estimate is far above the size of any syllabary or alphabet and in the range of the proto-administrative and logo-syllabic systems here.
- For the cuneiform corpora the types are transliteration values (one sign can have several readings), so their numbers overstate the sign inventory; the comparison with them is indicative only. The proto-Elamite figure (signs, not readings) is the cleanest comparison and is almost identical to the ICIT figure.
- An inventory of several hundred signs excludes a purely syllabic or alphabetic system, if the signs are writing at all; it is compatible with a logo-syllabic script and with a proto-administrative system of the proto-Elamite kind.

### Pre-registration of H7.1 (class-based grammar by a hidden Markov model; before running)

**Question.** Is the order of signs better described by a small number of hidden classes (a class grammar) than by sign-to-sign transitions?

**Model.** A hidden Markov model with **8 states** (fixed now), trained by Baum–Welch (50 iterations, 3 random starts, best training likelihood kept) on ICIT training lines (unique, complete, reading order), with start and end transitions; emission and transition probabilities smoothed by adding 0.01. Unknown signs in test lines receive the probability of an unseen sign under add-0.1 smoothing in both models.

**Comparison.** The bigram model of F3 (add-0.1, trained on the same lines in ICIT numbering).

**Test data.** Fresh sets 1 and 2 (all ICIT lines from post-1979 sites, unique, complete; not used to train either model).

**Statistic.** Per-line mean log-probability per token (including the end symbol) under each model; one-sided sign test over lines (HMM better than bigram).

**Prediction.** HMM better on more lines than the bigram, p < 0.01. The state composition (most probable signs per state) is reported descriptively and compared with the positional zones (Q2).

### H7.1 result: not supported; the learned states reproduce the established structure

Script: `scripts/phase3_h71_hmm.py`; results: `results/phase3_h71_hmm.json`.

On the 117 fresh lines the 8-state HMM is better than the bigram model on 43 lines (sign test p = 0.9985); mean log-probability per token −3.73 (HMM) vs −3.58 (bigram). **H7.1 is not supported**: eight classes are too coarse to predict new texts as well as sign-to-sign transitions.

The learned states, however, recover without supervision the structure established by the tests (descriptive):

| State | Start prob. | End prob. | Most probable signs | Corresponds to |
|---|---:|---:|---|---|
| 4 | 0.32 | 0.00 | 861, 820, 817, 920, 692 | initial zone (Q2) |
| 1 | 0.25 | 0.04 | 003, 590, 004, 032, 840, 005 | stroke signs (numerals) and others |
| 0 | 0.18 | 0.01 | 031, 001, 741, 032, 140, 900 | single and double strokes, 741 |
| 5 | 0.22 | 0.00 | 240, 235, 220, 233, 032, 415 | fish-shaped family |
| 2 | 0.00 | 0.48 | 390, 220, 368, 407, 405, 700 | count–item partners (390–407) |
| 3 | 0.00 | 0.03 | 002, 060, 741, 001 | medial signs, 002 |
| 6 | 0.03 | 0.01 | 740, 100, 760, 033, 176 | medial |
| 7 | 0.00 | 0.86 | 740, 400, 520, 090, 151, 527 | terminal cluster |

The states that end lines (7, and 2 with end probability 0.48) contain the terminal set and the partners of the numerals, the states that start lines contain the initial-zone signs and the numerals, and the fish-shaped signs form their own state. An unsupervised model trained only on the training split thus arrives at the same functional grouping (initial signs, numerals, counted items, fish-shaped signs, closing signs) as the hypothesis tests, which is a useful consistency check, although the model does not predict better than the bigram.

### H6.1 robustness check: the result depends on sign 033

Script: `scripts/phase6_h61_without_033.py`; results: `results/phase6_h61_without_033.json`. Not pre-registered; run because L3b showed that ICIT 033 also covers KP 123 (three short strokes).

With 033 removed from the long series: short strokes 30 (8 followed by the A group), long strokes 17 (0 followed by A, 1 by 520); χ² = 6.9, permutation p = 0.015. The separation keeps its direction (no long stroke is followed by an A-group sign), but it no longer reaches p < 0.01, because three of the four 520 followers in the long series follow 033.

**Assessment.** H6.1 remains supported as registered, but its strength rests largely on the sign 033 → 520 pairing, and the identity of 033 (three long strokes or, in part, three short strokes) is not settled between the two transcriptions. The interpretation "two numeral notations for different classes of items" is therefore weaker than stated in the first H6.1 entry and is downgraded to "suggested". The README entry is adjusted accordingly.

### R2 (review): leave-one-sign-out check of H3.10 on the strict held-out set

Script: `scripts/review_r2_h310_leave_one_out.py`; results: `results/review_r2_h310_leave_one_out.json`. Not pre-registered (review).

- KP1979: the result passes (p < 0.01) whichever stroke sign is left out (p from 3.3 × 10⁻⁶ to 3.6 × 10⁻³).
- ICIT: it passes when any single target sign is left out, and when 005, 016, 017 or 034 is left out; it fails when 004 (four strokes) is left out (2 of 9 bigrams; p = 0.026).

H3.10 does not rest on one sign in KP1979. In the ICIT strict held-out set the counts are small (12 bigrams after the stroke set), and the sign 004 carries a large share. The result stands, with the note that its ICIT replication on strict held-out data is driven mainly by four-stroke signs; the post-1979 confirmation (F2) is independent of this.

### Repetition within lines depends on the transcription (descriptive)

Script: `scripts/phase3_repetition.py`; results: `results/phase3_repetition.json`. Share of unique lines (length ≥ 2) containing some sign twice: **ICIT 0.038, KP1979 0.167**. Most KP repetitions are adjacent doublings of the same sign (144 144: 71; 121 121: 51; 268 268: 49), which the ICIT-style source writes as single composite signs (for example ICIT 032 ↔ KP 121/144 + 121/144; ICIT 617 ↔ KP 268 268, split/merge table). The low repetition rate of the Indus texts, an argument used in the debate on whether the signs are writing (claims register C9), is therefore largely a property of how a transcription segments doubled signs, not of the inscriptions themselves.

### D1 robustness with the KP1979 transcription (not pre-registered)

Script: `scripts/phase4_d1_kp_robustness.py`; results: `results/phase4_d1_kp_robustness.json`.

With KP1979 in place of the ICIT-style source, the nearest reference corpus is still proto-Elamite (mean distance 2.70), followed by Akkadian letters (3.22), Ur III administrative (3.74), OB literary (3.99) and proto-cuneiform (4.74); an administrative corpus is nearer than both non-administrative ones in 19 of 20 resamples. The D1 placement next to proto-Elamite holds for both transcriptions.

**Correction.** The D1 and D2 entries noted that the Indus corpus shares a very low repetition rate with proto-cuneiform and proto-Elamite. With KP1979 the repetition rate is 0.166, higher than in proto-Elamite (0.068) and close to OB literary Sumerian (0.181). That observation depends on the transcription and is withdrawn. The other D1 observations (direction asymmetry, final concentration, closeness to proto-Elamite) are unaffected.

---

## 2026-11-25 (day 1, fourteenth working session, continued): long-horizon project L-2 (glyph shapes)

### Glyph data

`docs/GLYPH_DATA_SURVEY.md` surveys 16 open resources. The most useful for shape work is https://github.com/decipher-indus/font-generation (commit `ad564ff`): binary images of 726 signs keyed to ICIT numbers (`bmps/S###.bmp`). According to its download script the images were taken from the ICIT sign list; the repository states no licence. The images are therefore used for analysis only and are **not** redistributed here; `scripts/fetch_glyphs.py` downloads them at the pinned commit.

### Pre-registration of G1 (shape and usage; before running)

**Question.** Do signs that look alike also behave alike in the texts? If shape carries function (families of related signs), shape similarity and context similarity should be correlated.

- **Signs:** ICIT signs with ≥ 15 occurrences in the training split that have an image.
- **Shape similarity:** each image cropped to its bounding box, padded to a square, resized to 32 × 32, blurred with a Gaussian filter (σ = 1.5 pixels), flattened; cosine similarity between signs.
- **Context similarity:** 1 − Jensen–Shannon divergence between the pooled previous-sign / next-sign distributions of two signs (as in L3a), training split.
- **Test:** Mantel test, Spearman correlation between the two similarity matrices (upper triangles), 10,000 permutations of sign labels (smallest attainable p = 0.0001, one hundredth of the threshold).
- **Prediction:** positive correlation, p < 0.01.
- **Descriptive follow-up:** the sign pairs that are most similar in both respects are listed.

### G1 result: not supported (no global correlation)

Script: `scripts/phase8_g1_shape_usage.py`; results: `results/phase8_g1_shape_usage.json`. 82 signs; Spearman correlation between shape and context similarity 0.007; permutation mean 0.000 (SD 0.049); p = 0.43. Across all pairs of frequent signs, looking alike does not go with being used alike.

Descriptive: the pairs most similar in both respects are known families: the initial signs 817 / 861 / 820, the fish-shaped signs 231 / 233 / 235 / 240 / 220, the count–item partners 390 / 405 / 407, 803 / 806, 154 / 156, 705 / 706. This suggests a local rather than a global relation: very close shapes may share usage even though shape similarity in general does not. Because this was seen in the training data, it is tested on other data below.

### Pre-registration of G2 (local shape–usage relation; before running)

- **Close-shape pairs:** among ICIT signs with an image, the 5 % of pairs with the highest shape similarity (defined by shape alone, as in G1).
- **Usage data not used in G1:** the strict held-out set together with fresh sets 1 and 2; signs with ≥ 5 occurrences there.
- **Statistic:** context similarity (1 − JS, as in G1) computed on these data only; one-sided Mann–Whitney test, close-shape pairs vs all other pairs among the same signs.
- **Prediction:** close-shape pairs have higher context similarity, p < 0.01.

### G2 result: supported — very similar shapes share usage on unused data

Script: `scripts/phase8_g2_close_shapes.py`; results: `results/phase8_g2_close_shapes.json`.

82 signs with ≥ 5 occurrences in the strict held-out and fresh data; 3,321 pairs; 167 close-shape pairs (shape similarity ≥ 0.807). Median context similarity: close-shape pairs 0.104, other pairs 0.084; one-sided Mann–Whitney p = 0.0017. **G2 is supported.**

Close-shape pairs with the most similar usage include the initial signs 817 / 861 / 820, the count–item partners 390 / 405 / 407, the fish-shaped signs 231 / 233 / 235 / 236 / 240, and 705 / 706, 690 / 692, 803 / 806, 415 / 416.

**Interpretation.** Shape similarity does not predict usage across the whole sign inventory (G1), but signs that are near-variants of one another (a basic form with added strokes, marks or enclosures) are used in similar contexts, also on data not used to see the pattern. This supports the view that part of the sign inventory consists of families built from a base sign with modifications, and that family membership is functionally meaningful. It is a structural result (L1); it does not say what the modifications mean.

### L-4: survey of unused inscription data

`docs/NEW_DATA_SURVEY.md` lists inscriptions published outside the ICIT-style source and other machine-readable datasets. Main conclusion: no dataset adds more than a handful of objects; the largest accessible group of possibly unused inscriptions is the Surkotada pottery inscriptions (Joshi 1990, ASI Memoir 87), followed by single objects (Binjor, Tell Jokha / Umma, some Dholavira seals in Bisht 2015, and others). In total a few dozen mostly short inscriptions, which would have to be transcribed from published photographs.

**Consequence for the L2 candidate.** The candidate concerns seals and tablets (closing sign vs object class). The accessible unused material consists mostly of pottery inscriptions and single seals, so a confirmatory test of the candidate with adequate power is not possible with data that can be obtained here. This is recorded as a limitation; the candidate stays a candidate.

---

## 2026-11-25 (day 1, fourteenth working session, continued): inscriptions found abroad

### Pre-registration of H8.1 (before running)

**Idea.** Indus seals and inscribed objects found in the Persian Gulf, Mesopotamia and Central Asia may record names, titles or contents that differ from those at home sites (for example foreign names or a different language). If so, their sign sequences should be less predictable under a model of home-site texts.

- **Abroad lines:** ICIT complete lines with recorded direction, length ≥ 2, region `Persian Gulf`, `Mesopotamia` or `Central Asia` (the region `Iranian Plateau` is excluded because it includes sites within the Indus sphere in Balochistan); strings that also occur at a home site are removed.
- **Home comparison lines:** the strict held-out set, home regions only, length ≥ 2.
- **Model:** bigram (add-0.1) trained on ICIT training lines from home regions only.
- **Statistic:** mean log-loss per token (including line end). One-sided Mann–Whitney test, abroad > home.
- **Prediction:** p < 0.01. Fewer than 8 abroad lines → "insufficient data".
- **Also reported (descriptive):** the abroad lines, their sites, and the share of their signs that are rare (< 5 training occurrences).

### H8.1 result: not supported (p = 0.011)

Script: `scripts/phase8_h81_abroad.py`; results: `results/phase8_h81_abroad.json`.

15 abroad lines (Gulf, Mesopotamia, Central Asia) vs 228 strict held-out home lines. Mean log-loss per token: abroad 5.09, home 4.31; one-sided Mann–Whitney p = 0.011. The direction is the predicted one, but p ≥ 0.01, so **H8.1 is not supported**.

Descriptive observation (seen after the test; not tested): only 2 of the 15 abroad lines end in a sign of the terminal set (Kish: `… 590 390 740`; Gonur Depe: `… 590 390 740`), and those two have low log-loss (3.3, 3.8). The lines from Gulf sites (Saar, Janabiyah, Karzakan, Qala'at al-Bahrain, Hajar, Salut) all lack the terminal cluster and have the highest log-loss (5.2–7.0). If tested on new material, the prediction would be that Gulf finds lack the closing cluster that marks home-site seals. No unused abroad material is available here to test this.

---

## 2026-11-25 (day 1, fifteenth working session, 10:18 UTC): L-2b, do added marks behave like modifiers?

### Pre-registration of M1 (before running)

**Idea.** G2 showed that near-variant shapes share usage. If the added parts of a variant (extra strokes, marks, enclosures) act like modifiers with a consistent function, the marked member of a pair should shift position in the line in a consistent direction across many different base signs.

- **Pairs (shape only):** ICIT sign pairs with shape similarity ≥ 0.807 (the top-5 % cut of G2), both signs with ≥ 10 occurrences in the training split.
- **Marked member:** the sign with more ink (more black pixels in the normalised 32 × 32 image of G1); pairs whose ink differs by less than 5 % are excluded as undecidable.
- **Positional measures (training split):** initial share and final share of each sign.
- **Test:** for each measure, a two-sided sign test over pairs of (marked − unmarked); Bonferroni over the two measures, threshold 0.005.
- **Prediction:** at least one measure shifts consistently (p < 0.005). Otherwise marks are recorded as not shifting position consistently.

### M1 result: not supported; a limitation of the G1/G2 shape measure; G2 holds under a better measure

Scripts: `scripts/phase8_m1_marks.py` (pre-registered), `scripts/phase8_g2_hog_robustness.py`, `scripts/phase8_m1_hog_robustness.py` (robustness checks); results in the corresponding `results/phase8_*.json`.

**M1.** 245 near-variant pairs; the more-marked member has a higher initial share in 133 pairs and a lower one in 112 (p = 0.20), a higher final share in 115 and a lower one in 123 (p = 0.65). Added marks do not shift position consistently. **Not supported.**

**Limitation found.** The list of M1 pairs showed that the shape measure of G1, G2 and M1 (blurred 32 × 32 images, cosine similarity) pairs signs of quite different design when both are tall and narrow, for example the single stroke 001 with fish-shaped signs. The measure is dominated by outline and proportions rather than internal structure.

**Robustness with a structural measure.** A histogram-of-edge-orientation measure (4 × 4 cells, 9 orientations) gives sensible nearest pairs (the stroke series 031 / 032 / 033, the jar-type variants 741 / 742 / 745, 231 / 233, 690 / 692, 004 / 005). With it:
- G2 (usage on strict held-out + fresh data): close-shape pairs median context similarity 0.094 vs 0.084 for other pairs; p = 0.0074. **G2 holds**, with a smaller effect than first reported.
- M1: 238 pairs; initial share p = 0.48, final share p = 0.84. **M1 remains not supported.**

G1 was not repeated with the new measure, because its conclusion (no global correlation) was negative and a coarser measure cannot have hidden a positive correlation that a finer one would reveal more weakly; this is noted as an untested possibility.

---

## 2026-11-25 (day 1, sixteenth working session): templates with a variable numeral slot

### Pre-registration of H9.1 (before running)

**Idea (claims register C31b).** If some inscriptions are records that repeat a fixed formula with a changing quantity, the corpus should contain texts that are identical except for the stroke sign. H3.8 tested a weaker form (similar contexts) and failed; this test looks directly at minimal pairs.

- **Minimal pairs:** pairs of unique complete strings of equal length that differ in exactly one position; the substitution at that position is the unordered sign pair {a, b}.
- **Stroke sets:** ICIT {001, 003, 004, 034, 005, 016, 017, 031, 032, 033, 035}; KP1979 {121–130, 144, 145, 147, 150, 151}.
- **Statistic:** number of minimal pairs whose substitution has both a and b in the stroke set.
- **Null:** 10,000 random sets in which each stroke sign is replaced by a non-stroke sign of similar frequency (within a factor of 1.5 in all unique strings); the statistic is recomputed for each set. The pairs themselves do not change, only the set; smallest attainable p = 0.0001.
- **Data:** all unique complete strings of each corpus (this question has not been examined before; minimal pairs are a property of the whole corpus).
- **Prediction:** more stroke–stroke substitutions than in the null sets, p < 0.01, in both corpora.

### H9.1 result: supported in both corpora — texts that differ only in the count are common

Scripts: `scripts/phase9_h91_numeral_slot.py` (pre-registered), `scripts/phase9_h91_count_differences.py` (breakdown, not pre-registered); results: `results/phase9_h91_numeral_slot.json`, `results/phase9_h91_count_differences.json`.

| Corpus | Minimal pairs | Stroke–stroke substitutions | Null mean (SD), max | p |
|---|---:|---:|---:|---:|
| ICIT | 3,609 | 94 | 15.2 (9.4), 71 | 0.0001 |
| KP1979 | 6,322 | 183 | 23.0 (11.2), 82 | 0.0001 |

**H9.1 is supported.** Among texts that differ in exactly one sign, the differing signs are both stroke signs six to eight times as often as for frequency-matched random sign sets.

Breakdown of the stroke–stroke substitutions (not pre-registered):

| Kind of substitution | ICIT | KP1979 |
|---|---:|---:|
| Same count, short vs long strokes | 6 | 49 |
| Count differs by 1 | 42 | 42 |
| Count differs by 2 | 26 | 37 |
| Count differs by 3 or more | 20 | 55 |

Three explanations were considered in advance of the breakdown: changing quantities in a fixed formula, different readings of the stroke count of copies of the same text, and short and long variants of the same count. Short/long substitutions with the same count are frequent in KP1979 (49, of which 41 within the same site and object type), which fits the third explanation and the split/merge findings. But about half of the substitutions involve count differences of two or more strokes (ICIT 46 of 94, KP 92 of 183), which are unlikely to be misreadings of the same text. Example (ICIT): `003 390 …` beside `005 390 …` (see results file).

**Interpretation.** The corpus contains texts that repeat the same formula with a different number of strokes in the same slot. This is what record-like texts with a variable quantity would look like (claim C31b, administrative records). It is a structural (L1) result: it shows a variable numeral slot within otherwise fixed formulae, without identifying what is counted. It strengthens the numeral reading of the stroke signs more directly than H3.8, which looked only at shared contexts and failed.

### Pre-registration of H9.2 (do variable-count formulae belong to tablets? before running)

**Hypothesis (claim C31).** If formulae with a variable count are records, the texts involved should be on record-like objects (tablets) more often than on seals.

- **Units:** ICIT unique complete strings with one coarse object type (`SEAL*` or `TAB*`) and one site stratum (Harappa, Mohenjo-daro, other).
- **Groups:** "count-variable" strings = strings that take part in at least one stroke–stroke minimal pair (H9.1); "other" = strings that take part in at least one minimal pair but none with a stroke–stroke substitution (so both groups are formulaic texts with near-variants).
- **Test:** Cochran–Mantel–Haenszel test (site strata) on (group) × (tablet vs seal), one-sided: tablets over-represented among count-variable strings.
- **Primary (L2 candidate):** all strings; p < 0.01.
- **Secondary (decides L2):** only strings from the strict held-out set or the fresh sets (partners may be anywhere); p < 0.01. Only if the secondary test passes is the result counted as L2.

### H9.2 result: not supported — count-variable formulae are not concentrated on tablets

Script: `scripts/phase9_h92_formula_objects.py`; results: `results/phase9_h92_formula_objects.json`.

| Stratum (all strings) | Count-variable: tablet / seal | Other formulaic: tablet / seal |
|---|---:|---:|
| Harappa | 15 / 4 | 210 / 63 |
| Mohenjo-daro | 1 / 14 | 44 / 266 |
| Other sites | 1 / 7 | 9 / 85 |

Primary (all strings): CMH odds ratio 0.91, p = 0.58. Secondary (strict held-out and fresh strings): odds ratio 5.3, p = 0.093 on very few strings. **H9.2 is not supported**; no L2 result.

The tablet share among count-variable texts is the same as among other formulaic texts at each site: tablets dominate at Harappa and seals at Mohenjo-daro for both groups. Formulae with a variable count occur on seals as much as on tablets. This does not fit a simple division in which seals carry names and tablets carry quantities; it is compatible with seals that themselves state quantities or ranks, or with numerals that are part of names or titles (for example the recurrent "7 + 585/575").

### Pre-registration of H9.3 (substitution classes reproduced across transcriptions; before running)

**Idea.** Signs that replace one another in otherwise identical texts fill the same slot of a formula. Grouping signs by these substitutions gives paradigmatic classes. If they are real, classes built independently from the two transcriptions should agree.

- **Graph:** for each corpus separately, nodes are signs, edge weights are the numbers of minimal pairs (H9.1 definition, all unique complete strings) in which two signs substitute for each other; nodes with total weight ≥ 2.
- **Classes:** Louvain community detection (networkx, resolution 1.0, seed 20261125).
- **Comparison:** for one-to-one concordance pairs (support ≥ 3, purity ≥ 0.8) present in both graphs, adjusted Rand index between ICIT classes and KP classes.
- **Null:** 10,000 permutations of the KP class labels over the linked signs.
- **Prediction:** ARI above the null, p < 0.01.

### H9.3 result: supported — substitution classes agree across transcriptions

Script: `scripts/phase9_h93_substitution_classes.py`; results: `results/phase9_h93_substitution_classes.json`.

Substitution graphs: ICIT 263 signs in 9 classes; KP1979 203 signs in 7 classes. For 69 one-to-one linked signs, ARI = 0.169; permutation mean 0.000 (SD 0.022); p = 0.0001. **H9.3 is supported.**

The ICIT classes (largest ones) group, among others:
- the short-stroke numerals 003, 004, 005, 016, 017, 034 with 035 (one class);
- the closing and count-partner signs 151, 154, 156, 390, 400, 405, 407 (one class);
- the fish-shaped signs 220, 231, 233, 235, 240 together with the single and long strokes 001, 031, 033 (one class);
- the sign family 467–475 (a class of its own).

Compared with H3.2 (classes from contexts; agreement 0.05–0.24 depending on the number of clusters, not fixed in advance), the substitution classes are defined without a free parameter and agree well beyond chance. As before, the two transcriptions cover largely the same objects, so this is agreement between independent transcriptions, not between independent samples.

**Interpretation.** The formulaic texts have slots that are filled from distinct classes of signs: a numeral class, a class of closing and counted-item signs, a class containing the fish-shaped signs, and others. This is the clearest picture so far of the paradigmatic organisation of the inscriptions (L1).

### Pre-registration of H9.4 (substitution classes and object class; before running)

- **Classes:** the ICIT substitution classes of H9.3 with ≥ 10 signs (defined from text-internal substitutions only; no object information enters their definition).
- **Feature:** a string contains at least one member of the class.
- **Values:** ICIT object subtypes with ≥ 30 training strings (as in C2).
- **Test:** site-stratified Cochran–Mantel–Haenszel; discovery on the training split with false-discovery rate q = 0.05; confirmation on the **strict** held-out split, one-sided in the discovered direction, Bonferroni 0.01 / number discovered.
- **L2 rule:** a confirmed association counts as L2 if the class has a structural interpretation established before this test (numeral class; closing / counted-item class; fish-shaped class). Otherwise it is an L2 candidate.

### H9.4 result: one association confirmed; an L2 candidate, not L2

Script: `scripts/phase9_h94_classes_objects.py`; results: `results/phase9_h94_classes_objects.json`.

Seven substitution classes with ≥ 10 signs × 6 object subtypes = 42 tests; 6 discovered; threshold 0.01/6 = 0.0017.

| Class (members, first ones) | Subtype | OR train | OR strict held-out | p | Confirmed |
|---|---|---:|---:|---:|---|
| class 4 (002, 090, 096, 097, 098, 104, …; 33 signs) | TAB:C | 0.12 | 0.00 | 3.9 × 10⁻⁴ | yes |
| class 4 | SEAL:S | 2.55 | 1.85 | 0.019 | no |
| class 3 (001, 007, 013, 031, 033, …, fish-shaped 220–240) | TAB:I | 0.44 | – | 0.99 | no |
| class 3 | SEAL:R | 1.75 | 1.05 | 0.45 | no |
| class 6 (042, 048, 152, 222, …) | TAB:B | 3.25 | 0.73 | 0.63 | no |
| class 4 | SEAL:R | 0.60 | 2.44 | 0.98 | no |

The confirmed association: texts on copper tablets (`TAB:C`) almost never contain a member of class 4, which includes the frequent medial sign 002 and the closing sign 090. The class is not one of the three classes with a structural interpretation fixed before the test (numerals; closing / counted-item signs; fish-shaped signs), so by the registered rule it is an **L2 candidate**, not an L2 result. Note that 090 is a terminal sign: the observation agrees with C2, where copper tablets favoured 407 as the closing sign.

### Formulae with a variable slot (descriptive)

Script: `scripts/phase9_formulae.py`; results: `results/phase9_formulae.json`; table: `docs/FORMULAE.md`.

131 templates in the ICIT corpus take at least three different signs in one slot (slot initial 65, medial 34, final 32). Examples:
- `_ 390` (14 fillers): 7 stroke signs and 6 other members of the numeral class 2 — the numeral slot before the counted-item sign.
- `003 _`, `004 _`, `005 _` (10, 9, 9 fillers): almost all from class 1 (closing and counted-item signs) — the item slot after a numeral.
- `_ 400` (15 fillers): all from class 4.
- `_ 740` (57 fillers): mostly class 0.
16 templates take two or more stroke signs in the same slot.

The formula table is the most direct description so far of how the inscriptions are built: short formulae whose slots are filled from particular sign classes, with numerals and counted items in fixed positions relative to each other.

---

## 2026-11-25 (day 1, seventeenth working session): chronology at Harappa

The ICIT-style `time` field records excavation periods for 3,067 records, mostly from Harappa (for example `Period 3B`, `Period 3B/C`, `Period 3C-1` … `3C-4`, `Period 4`). Only the order of the periods is used here; no absolute dates are assumed, because none were checked against a source in this session.

### Pre-registration of T1 (chronological variants; before running)

**Question.** Are some sign variants that are not distinguishable by context (L3a) chronological variants, that is, is the choice between them tied to the period?

- **Pairs:** the seven L3a pairs recorded as "not distinguishable": 154/156, 405/407, 817/861, 390/405, 790/850, 705/706, and 803/806 (not distinguishable by the registered test).
- **Data:** Harappa records whose `time` is unambiguously Period 3B (`Period 3B`, `3B-1`, `3B-2`) or Period 3C (`Period 3C`, `3C-1` … `3C-4`); each distinct (text, period) combination counted once.
- **Test:** for each pair, Fisher exact test (two-sided) on (variant a vs b) × (3B vs 3C), counting occurrences in the texts; Bonferroni over the pairs that have at least 5 occurrences in each period (threshold 0.01 / number of such pairs).
- **Prediction:** at least one pair shows a period dependence. Pairs with too few occurrences are reported as "insufficient data".

### T1 result: not supported (mostly insufficient data)

Script: `scripts/phase10_t1_chronological_variants.py`; results: `results/phase10_t1_chronological_variants.json`. Distinct Harappa texts with an unambiguous period: 129 (Period 3B) and 416 (Period 3C).

Testable pairs (≥ 5 occurrences in each period): 154/156 (p = 0.61), 817/861 (p = 1.0), 390/405 (p = 0.22); threshold 0.0033. The other four pairs have too few Period 3B occurrences. **T1 is not supported**: no evidence that the context-indistinguishable variants are chronological variants, but the Period 3B sample is small.

### Pre-registration of H10.1 (name-like slot fillers are more site-specific; before running)

**Idea.** If seal and tablet formulae consist of a name-like part and conventional parts (numerals, counted items, closing signs), the name-like signs should vary more between sites than the conventional ones, which all cities would share. The formula table shows that the initial slot of `_ 740` is filled mostly by substitution class 0, the numeral slot by class 2 and stroke signs, and the item slot after numerals by class 1.

- **Signs:** ICIT signs with ≥ 15 occurrences in all unique complete strings, in class 0 (name-like group) or in class 1 / class 2 / stroke signs (conventional group).
- **Site-specificity:** Jensen–Shannon divergence between a sign's distribution over three site strata (Harappa, Mohenjo-daro, other) and the distribution of all sign tokens over the same strata (occurrences in unique strings, each string assigned to its site; strings found at several strata are excluded).
- **Test:** difference of mean site-specificity (name-like minus conventional); null by 10,000 permutations of the group labels within frequency tertiles (to control for the higher variability of rarer signs).
- **Prediction:** name-like signs more site-specific, p < 0.01.
- **Level:** if supported, the result links a text-internal category (slot class) to an external variable (site) and is recorded as an L2 candidate, because the name-like reading of class 0 is an interpretation, not an established result.

### H10.1 result: not supported

Script: `scripts/phase10_h101_site_specificity.py`; results: `results/phase10_h101_site_specificity.json`.

25 name-like (class 0) and 36 conventional signs. Mean site-specificity 0.123 vs 0.115; difference 0.008; permutation mean 0.018 (SD 0.022); p = 0.67. **H10.1 is not supported.**

The most site-specific signs are in fact conventional ones: 700 and 400 (concentrated at Harappa), which close many Harappa tablet texts (C2). Site differences in sign use are dominated by the different mixes of object types at the sites, not by a name-like slot.

### Review R3: full re-run of all analyses; non-determinism in the phonetic searches

Script: `scripts/run_all.py` (66 analyses in dependency order); procedure in `docs/REPRODUCIBILITY.md`.

All 66 analyses ran without error. Ten result files differed from the committed versions:
- **Order only (six files):** `phase10_t1`, `phase3_split_merge`, `phase6_c1`, `phase9_formulae` and `docs/FORMULAE.md` differed only in the order of tied or dictionary items (and, for C1, which tied signs fell within a top-8 list). No number or conclusion changed (for example C1 p = 0.235 in both runs). The outputs are now sorted explicitly and are identical under different `PYTHONHASHSEED` values.
- **Phonetic searches (E3, E3b, E3c, E3d).** Their random seeds were derived from Python's `hash()` of strings, which is randomised per process, so every run fitted different assignments. The seeds now use CRC32; two runs with different hash seeds give byte-identical files.

Comparison of the three runs (first, re-run, deterministic version) for the decision variables:

| Analysis | Method has power | Indus language favoured |
|---|---|---|
| E3 | no / no / no | none / none / none |
| E3b | no / no / no | none / none / none |
| E3c | no / no / no (power at 8,000 lines) | – |
| E3d | no / no / no | none / none / none |

The registered conclusions do not change. The detailed rankings do: for example the first-ranked language for the Indus corpus in E3d was Old Tamil in the first run, Akkadian in the re-run, and Old Tamil (not clearly ahead) in the deterministic version; for the Akkadian cipher in E3b the true language Akkadian ranked last in the deterministic version. Run-to-run variation of this size is further evidence that the rankings carry no information about the language of the corpus. The journal tables for E3–E3d above report the first runs; the committed result files now hold the deterministic version.

---

## 2026-11-25 (day 1, eighteenth working session, 11:18 UTC): review R4, H9.1 with normalised KP strokes

### Pre-registration of R4 (before running)

In KP1979 the most frequent stroke–stroke substitutions of H9.1 were short vs long strokes of the same count (121↔144: 33; 123↔147: 13), which may be writing variants rather than different numbers. R4 repeats H9.1 for KP1979 on a normalised text in which:
1. long-stroke signs are replaced by the short-stroke sign of the same count (144→121, 145→122, 147→123, 150→124, 151→125);
2. after step 1, two adjacent single strokes `121 121` are merged into the two-stroke sign `122` (the split/merge finding of the fourteenth session), applied from left to right.
Unique complete strings are recomputed after normalisation. Stroke set {121–130}; null, number of null sets (10,000) and threshold (p < 0.01) as in H9.1.

### R4 result: H9.1 holds for KP1979 after normalisation

Script: `scripts/review_r4_h91_normalised_kp.py`; results: `results/review_r4_h91_normalised_kp.json`.

After merging long strokes into short strokes of the same count and `121 121` into `122`: 2,069 unique strings, 5,944 minimal pairs, 84 stroke–stroke substitutions against a null mean of 12.4 (SD 7.6, maximum 54); p = 0.0001. **H9.1 passes again.** The most frequent substitutions are now between different counts (3↔4: 9; 2↔3: 8; 1↔3, 3↔5: 5 each; 2↔4, 3↔6, 3↔7, 4↔5: 4 each). The KP1979 result therefore does not depend on short/long writing variants or on split strokes.

### Pre-registration of H9.6 (do substituted counts lie close together? before running)

**Idea.** If stroke signs denote quantities, then in formulae with a variable count, the substituted counts should tend to be close in value (records of similar quantities), so that 3↔4 is more frequent than 3↔7 beyond what the frequencies of the counts explain. If the strokes were arbitrary symbols, the size of the count difference should not matter.

- **Data:** the stroke–stroke substitutions of the minimal pairs (H9.1 definition) between **different** counts: ICIT (counts from the stroke sets, short and long series pooled by count) and KP1979 normalised as in R4.
- **Statistic:** mean absolute count difference over the substitutions.
- **Null:** 10,000 random re-pairings that keep the frequency with which each count takes part in substitutions (the members of all substitution pairs are pooled and randomly re-paired, discarding same-count pairs and re-drawing).
- **Prediction:** observed mean difference smaller than in the null, p < 0.01, in both corpora.

**Clarification of the H9.6 null (before any result was obtained).** The first implementation re-drew the whole pairing until no pair had equal counts; because count 3 dominates, such a pairing almost never occurs and the program did not finish. The null is therefore implemented as: random re-pairing of the pooled members, then **dropping** same-count pairs and averaging over the remaining pairs. Statistic, number of re-pairings and threshold are unchanged.

### H9.6 result: not supported (passes in ICIT, fails in KP1979)

Script: `scripts/phase9_h96_count_distance.py`; results: `results/phase9_h96_count_distance.json`.

| Corpus | Substitutions (different counts) | Mean count difference | Null mean (SD) | p |
|---|---:|---:|---:|---:|
| ICIT | 88 | 1.84 | 2.16 (0.11) | 0.0022 |
| KP1979 (normalised) | 84 | 2.61 | 2.87 (0.16) | 0.050 |

Distribution of differences: ICIT 1: 42, 2: 26, 3: 13, 4: 6, 5: 1; KP1979 1: 29, 2: 20, 3: 13, 4: 11, 5: 5, 6–9: 6. In both corpora substituted counts are closer together than random re-pairings would give, but only the ICIT result reaches p < 0.01; by the registered rule (both corpora) **H9.6 is not supported**. The evidence that the strokes carry magnitude (and are not merely distinct symbols) is therefore suggestive, not established.

---

## 2026-11-25 (day 1, nineteenth working session): numeral variation compared across systems

### Pre-registration of D4 (before running)

**Question.** How does the Indus corpus compare with the reference systems in the share of minimal-pair substitutions that are numeral ↔ numeral (the statistic behind H9.1)?

- **Corpora:** Indus (ICIT; and KP1979 normalised as in R4), proto-Elamite, proto-cuneiform, Sumerian Ur III administrative, Sumerian OB literary, Akkadian OB letters.
- **Numeral tokens:** Indus stroke signs (ICIT set of H9.1; KP 121–130 after normalisation); cuneiform tokens containing a numeral group, i.e. a parenthesis (for example `3(disz)`, `1(N01)`).
- **Sampling:** 20 resamples of 2,000 unique lines matched to the ICIT length distribution (as in D1); statistic = numeral↔numeral substitutions / all minimal-pair substitutions; mean over resamples.
- **Prediction (ordinal, from the administrative reading of claim C31 and the D1 result):** the Indus share is lower than that of each administrative corpus (proto-Elamite, proto-cuneiform, Ur III administrative) and higher than that of each non-administrative corpus (OB literary, OB letters). Decision: the prediction holds if all five comparisons go in the predicted direction in at least 19 of 20 resamples.

### D4 result: prediction not supported; the statistic measures numbered formulae, not genre

Script: `scripts/phase4_d4_numeral_variation.py`; results: `results/phase4_d4_numeral_variation.json`.

Mean share of numeral↔numeral substitutions among minimal-pair substitutions (20 resamples):

| Corpus | Share |
|---|---:|
| Sumerian OB literary | 0.394 |
| Sumerian Ur III administrative | 0.133 |
| proto-Elamite | 0.092 |
| proto-cuneiform | 0.034 |
| Indus (KP1979, normalised) | 0.028 |
| Indus (ICIT) | 0.026 |
| Akkadian OB letters | 0.022 |

The predicted order held in 0 of 20 resamples. **D4 is not supported.**

The OB literary value was checked before interpretation: its numeral tokens are real numerals (`1(disz)`, `7(disz)`, `1(u)` …; 2,239 tokens in all), and its numeral minimal pairs come from numbered formulae such as `5(disz) mu i3 ak` / `6(disz) mu i3 ak` ("ruled 5 / 6 years", king-list type) and `2(disz) kam-ma …` / `3(disz) kam-ma …` (ordinals). The statistic therefore measures how much of a corpus consists of short formulae with a numeral slot, which literary collections can also contain; it does not separate administrative from non-administrative texts.

For the Indus corpus the share (0.026–0.028) is close to proto-cuneiform (0.034) and the Akkadian letters (0.022) and well below proto-Elamite (0.092) and the Ur III administrative texts (0.133): numeral slots exist (H9.1) but form a small part of the Indus formulae.

### Visual check of key signs (descriptive)

The ICIT-keyed images of the stroke signs (003, 004, 005, 016, 017, 031, 032, 033, 035), the count partners (390, 405, 406, 407, 520, 575, 585) and the closing signs (740, 400, 090) and 002 were inspected. The stroke counts read earlier from the KP1979 sign list agree with the ICIT images (for example 016 = three over three, 017 = four over three short strokes; 033 = three long strokes). ICIT 740 is a U-shaped vessel with two lateral attachments, which matches the "jar" sign of the literature; this identification had been assumed in the claims register and is now checked against the image. Shape descriptions are collected in `docs/COUNTED_ITEMS.md`, marked as descriptions only.

---

## 2026-11-25 (day 1, twentieth working session): evaluating the claims register

Plan: give every claim in `docs/CLAIMS_REGISTER.md` a verdict based on the tests of this project, and run new tests for claims that are testable now but have not been tested. Result: `docs/CLAIMS_EVALUATION.md`.

### Pre-registration of three claim tests (before running)

**CT16 (claim C16, the "jar" sign as a unit of measure).** Lines containing the jar sign (ICIT 740; KP 324/325) contain a stroke numeral more often than lines without it. Data: strict held-out set of each corpus, plus the fresh sets for ICIT. One-sided Fisher exact test; p < 0.01 in both corpora. Numeral sets as in H9.1 (KP normalised as in R4).

**CT17 (claim C17, long texts are built from short texts).** For each held-out line of length ≥ 5 (strict held-out set), test whether it can be divided completely into segments that occur as complete texts of length 2–4 in the training split (one single-sign remainder allowed). Compare the share of divisible lines with the same share for rule-preserving control versions of the same lines (`src/indus/controls.py`, 1,000 control sets). Prediction: real lines divisible more often, p < 0.01, both corpora.

**CT10 (claim C10, repetition rises with length).** In ICIT unique complete lines (the transcription in which doubled signs are single signs, so that repetition is not a writing convention), the share of lines with a repeated sign increases with line length: Cochran–Armitage-type test by a one-sided Spearman correlation between length (2–13) and the presence of a repetition, p < 0.01. Data: all unique strings (descriptive claim about the corpus).

### Results of the claim tests

Script: `scripts/claims_tests.py`; results: `results/claims_tests.json`.

| Test | Corpus | Result | Verdict |
|---|---|---|---|
| CT16 jar sign with numerals | ICIT (strict held-out + fresh) | lines with 740: 55/153 contain a numeral; other lines 89/183; OR 0.59, p = 0.99 | not supported (opposite direction) |
| CT16 | KP1979 (strict held-out, normalised) | 45/114 vs 60/113; OR 0.58, p = 0.99 | not supported (opposite direction) |
| CT17 long texts built from short texts | ICIT | 8.0 % of 162 long lines divisible; controls 0.6 % (SD 0.6 %); p = 0.001 | supported |
| CT17 | KP1979 | 4.2 % of 167; controls 0.4 % (SD 0.5 %); p = 0.001 | supported |
| CT10 repetition rises with length | ICIT | Spearman 0.19, p = 1.4 × 10⁻¹⁷; share with repetition from 0.3 % (length 2) to 16 % (length 9) | supported |

CT16: texts with the jar sign contain numerals less often, not more, which does not fit a reading of 740 as a unit of measure attached to quantities (claim C16). CT17: long texts can be divided into complete short texts much more often than rule-preserving reorderings, although only a small share of long texts (4–8 %) can be divided completely; this supports C17 in a weak form. CT10 supports C10: the low repetition of the Indus texts is largely a matter of their shortness (and, as found earlier, of transcription).

### Descriptive figures for further claims

Script: `scripts/claims_descriptive.py`; results: `results/claims_descriptive.json`.

- C2: entropy of the initial-sign distribution 7.09 bits (ICIT) / 6.59 (KP) vs final-sign distribution 4.78 / 4.89 — line ends are much more concentrated.
- C6/C7: mean length of unique lines 4.49 (ICIT) / 4.61 (KP); longest line 13 / 14 signs; mean signs per object 4.09 / 4.96; longest object 17 / 28 signs.
- C11/C13: the most frequent sign is 740 in ICIT with 10.7 % of tokens (KP: 325 with 6.4 %, the jar sign being split between KP 324 and 325); 82 (ICIT) / 63 (KP) signs cover 80 % of tokens.
- C14: left-neighbour variety of 740 (distinct preceding signs per occurrence) is 0.19, among the lowest of the 20 most frequent signs (initial signs 817, 861: 0.79–0.88); 740 follows a limited set of signs, which is not what a freely attaching suffix would show.
- C15: share of 740 occurrences in line-final position by object type: SEAL:S 0.82, TAB:C 0.84, SEAL:R 0.72, TAB:B 0.58, TAB:I 0.37.
- C21a: restoring one masked sign per strict held-out line with a bigram model: correct first guess 29 %, within the top five 52 % (227 lines).
- C27: among the 50 most frequent signs, the share of possible ordered pairs that occur (9,000-token samples): Indus 0.29, proto-Elamite 0.27, Ur III administrative 0.24, Akkadian OB letters (syllabic graphemes) 0.41.
- C28: 1,585 seal lines carry 1,453 distinct texts; 78 texts occur on more than one seal record and 44 at more than one site.

---

## 2026-11-25 (day 1, twenty-first working session): extended batch

The scheduled task was revised so that each run completes a batch of at least four pre-registered analyses (the user asked for longer, more substantial runs). A background survey identifies the signs of claims C26 and C3 in the project's numbering.

### Pre-registration of G3 (claim C3: mirror-image signs; before running)

- **Mirror pairs (shape only):** for signs with an image and ≥ 10 occurrences in the training split, the structural shape descriptor of the G2 robustness check (edge-orientation histogram, `scripts/phase8_g2_hog_robustness.py`) is computed for each image and for its left–right mirror image. A pair (a, b) is a mirror pair if the similarity of a with mirrored b is ≥ 0.90 and exceeds the similarity of a with unmirrored b by at least 0.05 (so that symmetric signs, which match their own mirror image, are not counted).
- **Usage:** context similarity (1 − Jensen–Shannon divergence of previous/next-sign distributions) on the strict held-out set plus fresh sets 1 and 2, as in G2.
- **Test:** one-sided Mann–Whitney, mirror pairs vs all other pairs among the same signs, p < 0.01. Fewer than 5 mirror pairs → "insufficient data".
- **Claim C3** predicts that mirror pairs are allographs, i.e. used alike.

### G3 result: insufficient data (two mirror pairs)

Script: `scripts/phase8_g3_mirror_pairs.py`; results: `results/phase8_g3_mirror_pairs.json`.

Among 103 frequent signs, only two pairs meet the mirror criterion: 920/921 (mirror similarity 0.997, direct 0.14) and 900/921 (0.92 vs 0.08). With fewer than five pairs the test is **insufficient data**.

Descriptive (all unique lines): 920 (103 occurrences) is mostly line-initial (0.65) and followed by 060 in 52 cases; its mirror image 921 (13 occurrences) is followed by 070 (5), 072, 690. The one clear mirror pair is therefore not used like an allograph pair, which does not fit claim C3 for this pair; the evidence is too thin for a general verdict.

### Pre-registration of CT18 (claim C18: recursive segmentation; before running)

- **Splitting rule:** pointwise mutual information (PMI) of adjacent sign pairs from the training split (add-0.5 smoothing); a line is split at the adjacent pair with the lowest PMI, and each part of length ≥ 3 is split again, recursively.
- **Units:** all parts of length 2 and 3 produced by the recursion.
- **Statistic:** share of these parts that occur as complete texts in the training split.
- **Data:** strict held-out lines of length ≥ 4 in each corpus; controls: rule-preserving reorderings of the same lines (`src/indus/controls.py`), 1,000 control sets, split by the same rule.
- **Prediction:** the share is higher for real lines than for controls, p < 0.01, in both corpora.

### CT18 result: supported in both corpora

Script: `scripts/claims_ct18_recursive.py`; results: `results/claims_ct18_recursive.json`.

| Corpus | Lines | Parts that are complete texts (real) | Controls mean (SD) | p |
|---|---:|---:|---:|---:|
| ICIT | 203 | 0.207 | 0.077 (0.009) | 0.001 |
| KP1979 | 201 | 0.172 | 0.059 (0.008) | 0.001 |

Splitting held-out lines recursively at their weakest link produces parts that occur as complete texts elsewhere about three times as often as for rule-preserving reorderings. **Claim C18 is supported**: the longer texts have a nested structure in which sub-sequences are themselves complete short texts.

### Pre-registration of CT15 (claim C15: jar sign as a genitive on seals; before running)

Among ICIT lines that contain 740, the share in which 740 is the final sign is higher on seals (`SEAL*`) than on tablets (`TAB*`). Data: strict held-out strings plus fresh sets (ICIT), single coarse object type, site strata Harappa / Mohenjo-daro / other. Test: one-sided Cochran–Mantel–Haenszel, p < 0.01.

### CT15 result: supported — the jar sign closes seal texts more often than tablet texts

Script: `scripts/claims_ct15_jar_final.py`; results: `results/claims_ct15_jar_final.json`.

Lines containing 740 (strict held-out + fresh sets), 740 final / not final:

| Site stratum | Seals | Tablets |
|---|---:|---:|
| Harappa | 11 / 7 | 6 / 11 |
| Mohenjo-daro | 47 / 14 | 1 / 5 |
| Other sites | 31 / 8 | 1 / 0 |

Cochran–Mantel–Haenszel odds ratio 4.3, one-sided p = 0.0022. **CT15 is supported**, with the same direction in each stratum.

**Level.** This is a single pre-registered test of a functional category (the jar sign as the closing element of a legend) against an external variable (seal vs tablet), on data not used for this question, stratified by site. It confirms in one specific form the functional L2 candidate found in C2/C2k (the closing sign depends on the kind of object). It is recorded as **L2 in narrow, functional scope**: 740 is the characteristic closing sign of seal legends. The genitive reading of claim C15 ("of X") is one interpretation of this function and is not itself established; the result is also compatible with other closing functions (a title, a classifier, a mark of the seal-owner formula).

**Caveat on CT15 (family-wise correction).** The strict held-out set (with or without the fresh sets) has now been used to decide about eight questions (R1, G2, H9.4, CT16, CT17, CT18, G3, CT15). CT15 passes its own registered threshold (p = 0.0022 < 0.01), but it would not pass a family-wise correction over these questions (0.01/8 = 0.00125). The narrow functional L2 result is therefore recorded with this caveat: it is the strongest evidence for a function of a sign that the project has produced, but it is not beyond doubt.

### Pre-registration of D5 (typology with formula statistics; before running)

Three formula statistics, computed identically on 20 resamples of 2,000 unique lines matched to the ICIT length distribution (as in D1), for the Indus corpus (ICIT; KP1979 normalised as in R4) and the five CDLI reference corpora:
- **F1 recursive recurrence:** within each sample (80/20 split), the share of parts from recursive weakest-PMI splitting of test lines (length ≥ 4) that are complete training lines, divided by the same share for test lines with all but the final sign shuffled (20 shuffles).
- **F2 minimal-pair density:** minimal pairs (strings differing in one position) per line.
- **F3 formula richness:** templates with ≥ 3 different fillers in one slot per 1,000 lines.
Distances on z-scored means as in D1. **Prediction:** the reference corpus nearest to ICIT is proto-Elamite, in ≥ 19 of 20 resamples (per-resample distances).

### D5 result: not supported by the registered criterion (13 of 20); same ordering on average

Script: `scripts/phase4_d5_formula_typology.py`; results: `results/phase4_d5_formula_typology.json`.

| Corpus | F1 recursive recurrence ratio | F2 minimal pairs per line | F3 formulae per 1,000 lines |
|---|---:|---:|---:|
| Indus (ICIT) | 2.72 | 1.71 | 62.6 |
| Indus (KP1979, normalised) | 2.64 | 1.03 | 63.9 |
| proto-Elamite | 1.42 | 2.21 | 61.7 |
| proto-cuneiform | 1.62 | 1.55 | 34.7 |
| Sumerian Ur III administrative | 2.36 | 0.34 | 31.3 |
| Sumerian OB literary | 3.01 | 0.35 | 17.0 |
| Akkadian OB letters | 3.97 | 0.15 | 16.6 |

Proto-Elamite is the nearest reference corpus in 13 of 20 resamples (proto-cuneiform 6, Ur III administrative 1); the registered criterion (≥ 19) is not met, so **D5 is not supported**. On average the ordering is the same as in D1: KP1979 (the other Indus transcription, 0.90, a sanity check), then proto-Elamite (1.67), proto-cuneiform (2.06), Ur III administrative (2.50), OB literary (3.02), Akkadian letters (3.48). The Indus corpus resembles the proto-administrative corpora in the density of minimal pairs and formulae (F2, F3), and the full-writing corpora in its recursive recurrence (F1).

### Claim sign identifications (C26, C3)

`docs/CLAIM_SIGN_IDENTIFICATIONS.md` identifies (from search-engine excerpts and the sign mappings of the mayig corpus and the project concordance) the four-sign sequence of claim C26 as Mahadevan 51–130–149–342 = ICIT 255–435 (or its mirror 436)–690–740 = KP1979 73–188–255–324/325, a frequent fixed string (ICIT 34 records; KP1979 43 occurrences of 73 188 255). It also reconstructs, from the artefact lists in Daggumati & Revesz (2021), the ICIT numbers of 17 of their 23 mirror pairs, six of them securely: 436/435, 402/400, 551/550, 622/621, 526/527, 126/125.

### Pre-registration of CT26 (claim C26, structural part; before running)

Sequence A B C D = ICIT 255 435 690 740 (436 counted as 435) and KP1979 73 188 255 {324, 325}. Data: all unique complete strings (the claim concerns the corpus as a whole).
- (a1) PMI(B, C) is lower than both PMI(A, B) and PMI(C, D) (PMI from adjacent-pair counts in all unique strings, add-0.5 smoothing).
- (a2) AB occurs in at least 3 strings without CD following, CD occurs in at least 3 strings without AB preceding, and BC occurs without A before and without D after in fewer strings than either.
- Verdict: the two-part structure AB + CD is supported if (a1) and (a2) hold in both corpora.

### Pre-registration of CT3 (claim C3, six secure mirror pairs; before running)

For each of the six pairs 436/435, 402/400, 551/550, 622/621, 526/527, 126/125: relabelling test of L3a (Jensen–Shannon divergence of pooled previous/next-sign contexts; all unique complete ICIT strings, because the mirror forms are rare), 10,000 relabellings; Bonferroni threshold 0.01/6. Claim C3 predicts that no pair is contextually distinct. Pairs whose mirror form has fewer than 5 occurrences are reported but have almost no power.

### CT26 result: not supported — the sequence divides as ABC + D, not AB + CD

Script: `scripts/claims_ct26_ct3.py`; results: `results/claims_ct26_ct3.json`.

| Corpus | PMI(A,B) | PMI(B,C) | PMI(C,D) | AB without CD | CD without AB | BC alone |
|---|---:|---:|---:|---:|---:|---:|
| ICIT | 1.76 | 1.69 | −1.41 | 12 | 6 | 0 |
| KP1979 | 2.82 | 2.85 | −0.45 | 21 | 7 | 0 |

Condition (a2) holds, but (a1) fails in both corpora: the link between B and C is as strong as that between A and B, and the weakest link is between C and D (690 and the jar sign), whose PMI is negative because the jar sign follows very many signs. By the registered rule **CT26 is not supported**. In both transcriptions the sequence behaves as a fixed three-sign unit ABC followed by the closing jar sign, not as two pairs AB + CD; this does not fit the two-part analysis of claim C26. (The Dravidian reading itself is not testable here.)

### CT3 result: no pair contextually distinct (low power)

| Mirror / original | Occurrences | p (10,000 relabellings) |
|---|---|---:|
| 436 / 435 | 4 / 37 | 0.74 |
| 402 / 400 | 1 / 211 | 0.32 |
| 526 / 527 | 9 / 44 | 0.98 |
| 126 / 125 | 2 / 46 | 0.74 |
| 551 / 550, 622 / 621 | mirror form not in complete lines | – |

None of the four testable pairs is distinct (threshold 0.0017). This is consistent with claim C3 (mirror forms as allographs), but with mirror forms occurring 1–9 times the test has very little power; the result is recorded as "consistent, low power".

### Pre-registration of CT15k (replication of CT15 in KP1979; before running)

KP1979 strict held-out strings have not been used for this question (R1 used them for code 11 × final 98). Among KP strict held-out strings that contain the jar sign (324 or 325) and carry one object code, the share with the jar sign in final position is higher for seal codes {11, 23} than for tablet codes {62, 67, 72, 75} (codes identified in C2k). One-sided Fisher exact test (KP has no decoded site field), p < 0.01.

### CT15k result: not supported (underpowered; same direction)

Script: `scripts/claims_ct15k_jar_final_kp.py`; results: `results/claims_ct15k_jar_final_kp.json`. KP strict held-out strings with the jar sign: seals 67 final / 27 not final; tablets 1 / 2. Odds ratio 5.0, one-sided p = 0.21. The direction agrees with CT15, but only three tablet texts with the jar sign remain in the KP strict held-out set, so the replication has almost no power. **CT15k is not supported**; the narrow functional L2 result rests on CT15 alone, with the family-wise caveat noted there.

### Review R5: all non-phonetic analyses reproduce exactly

`scripts/run_all.py --skip-heavy` with `PYTHONHASHSEED=5` (74 analyses): no failures, and no committed result file changed.

### Pre-registration of CT15t (tags as independent evidence for CT15; before running)

**Idea.** If 740 is the characteristic closing sign of seal legends (CT15), objects that carry seal impressions or seal-like legends, the tags (`TAG*`, mostly from Lothal), should show the seal pattern rather than the tablet pattern. Tags were never used as a class in any earlier test (no tag subtype reached the 30-string minimum of C2).
- **Data:** all ICIT unique complete strings with one coarse object type, `TAG*` or `TAB*`, that contain 740.
- **Test:** one-sided Fisher exact test: share of strings with 740 in final position higher for tags than for tablets, p < 0.01.
- **Limitation stated in advance:** tags come mostly from Lothal, tablets mostly from Harappa and Mohenjo-daro, so site and object type are confounded; the test cannot be stratified by site.

### CT15t result: supported — tags follow the seal pattern

Script: `scripts/claims_ct15t_tags.py`; results: `results/claims_ct15t_tags.json`.

Strings containing 740, with 740 final / not final: tags 14 / 2 (0.88); tablets 130 / 111 (0.54); seals, for reference, 523 / 140 (0.79). One-sided Fisher exact test tags vs tablets: odds ratio 6.0, p = 0.0068. **CT15t is supported.** Tags, which carry seal-type legends, show the seal pattern of the closing sign, not the tablet pattern, on objects never used as a class before.

Limitation (stated in advance): tags come mostly from Lothal and cannot be compared with tablets of the same site, so a site effect cannot be excluded. With this limitation, CT15t adds independent support to the narrow functional L2 result of CT15.

### Pre-registration of CT28 (claim C28: are seal texts name-like? before running)

**Idea.** If seal legends name individual owners, the part of a seal text before its closing cluster (the "stem") should be more diverse than the stems of tablet texts, which repeat formulae.
- **Records:** all ICIT complete records with recorded direction (each record counted, so that repeated texts on several objects count as repetitions), coarse type `SEAL*` or `TAB*`, at Harappa or Mohenjo-daro.
- **Stem:** the text with its final run of terminal-set signs removed (terminal set as in `src/indus/controls.py`).
- **Statistic:** share of distinct stems among n records, with n equal for seals and tablets within each site (n = the smaller count at that site), averaged over sites and over 1,000 random subsamples.
- **Test:** the difference (seal share − tablet share) is positive in at least 99 % of the 1,000 subsamples (two sites pooled as above).
- **Prediction (claim C28's alternative, names):** seal stems more diverse. A positive result is compatible with names but also with individual licences; a negative result speaks against seals carrying individual names.

### CT28 result: supported — seal stems are far more diverse than tablet stems

Script: `scripts/claims_ct28_stem_diversity.py`; results: `results/claims_ct28_stem_diversity.json`.

Records: Harappa 274 seals / 1,173 tablets; Mohenjo-daro 1,003 seals / 266 tablets; subsamples of 274 and 266 per class and site. The share of distinct stems is on average 0.49 higher for seals than for tablets, and higher in all 1,000 subsamples. **CT28 is supported.**

Seal legends are almost always individual (their stems rarely repeat), whereas tablet texts repeat a limited set of stems (consistent with tablets made in series). This is what owners' names would produce, which claim C28 denies; it is equally what individual licences or titles with personal elements would produce. For C28 the verdict stays undecided, but the evidence now shows that seal legends are individual-specific in a way tablet texts are not.

### Pre-registration of CT15s (stamped vs incised pottery; before running)

**Prediction from the functional reading of 740 (CT15).** Pottery stamped with a seal (`POT:T:s`) carries seal legends; pottery with incised graffiti (`POT:T:g`) does not. Among ICIT unique complete strings with one of these two types that contain 740, the share with 740 in final position is higher for stamped than for incised pottery. One-sided Fisher exact test, p < 0.01; fewer than 5 strings with 740 in either group → "insufficient data". This question has not been examined before.

### CT15s result: insufficient data

Script: `scripts/claims_ct15s_pottery.py`; results: `results/claims_ct15s_pottery.json`. Only 3 stamped-pottery strings contain 740 (all with 740 final); incised pottery: 11 of 12 with 740 final. With fewer than 5 strings in one group the result is "insufficient data". Descriptively, incised pottery inscriptions that contain 740 also end in it, so the closing function of 740 is not confined to seal legends; this tempers the reading of CT15 as specific to seals and is noted in the final report.

### Pre-registration of CT31c (claim C31c: tablets share their non-numeral part with seals; before running)

- **Tablet stems:** distinct stems (text without its final terminal-set run, as in CT28) of ICIT tablet records (`TAB*`) from Harappa, with stroke numerals also removed; stems of length ≥ 2.
- **Seal stem set:** stems of all seal records (`SEAL*`, all sites), with stroke numerals removed.
- **Statistic:** share of tablet stems that occur in the seal stem set.
- **Control:** the same share for rule-preserving reorderings of the tablet stems (`src/indus/controls.py` applied to the stems), 1,000 control sets.
- **Prediction:** real share above controls, p < 0.01.

### CT31c result: not supported (p = 0.013)

Script: `scripts/claims_ct31c_shared_stems.py`; results: `results/claims_ct31c_shared_stems.json`. Of 275 distinct Harappa tablet stems (numerals removed, length ≥ 2), 10.2 % also occur among 1,332 seal stems; rule-preserving reorderings reach 8.9 % on average (SD 0.5 %); p = 0.013. The excess is small and does not reach p < 0.01. **CT31c is not supported**: tablet texts do not, beyond chance, repeat the non-numeral parts of seal legends. Shared stems include the C26 sequence `255 435 690`.

---

## 2026-11-25 (day 1, twenty-second working session, 14:18 UTC): batch of claim tests

Plan: (1) consistency review of the summary documents (background); (2) CT32a, copies per text on tablets vs seals (claim C32a); (3) CT19, conditional entropy of the Indus corpus against linguistic and non-linguistic corpora (claim C19); (4) CT25, a drop in stroke-count frequency after seven (claim C25); (5) CT14, left-neighbour diversity of the jar sign (claim C14); (6) report updates.

### Pre-registrations (before running)

**CT32a (claim C32a).** At Harappa, texts on tablets occur on more objects per distinct text than texts on seals. Records (complete, direction known) of coarse type `TAB*` or `SEAL*` at Harappa; statistic: mean number of records per distinct text (tablets minus seals); null: 10,000 permutations of the type labels among records; one-sided, p < 0.01.

**CT19 (claim C19, Rao et al. 2009).** Bigram conditional entropy H(next | current), divided by the unigram entropy of the same sample, for 20 samples of 300 unique lines (all corpora as in D2: Indus ICIT and KP1979, the three full-writing corpora, the four non-linguistic corpora). The claim predicts that the Indus value lies within the range spanned by the full-writing corpora and outside the range spanned by the non-linguistic corpora. Decision: the claim's prediction holds if both conditions hold for the mean over samples, for ICIT and for KP1979.

**CT25 (claim C25: base).** For short-stroke counts 1–9 in KP1979 normalised as in R4 (all unique strings), fit a log-linear decline of frequency on counts 3–7 (least squares on log counts) and predict counts 8 and 9. A base-8-like system predicts that the observed sum of counts 8 + 9 is far below the prediction. Decision: observed (8 + 9) below the 1st percentile of a Poisson distribution with the predicted mean → "drop after seven"; otherwise "no evidence of a drop".

**CT14 (claim C14: the jar sign as a freely attaching suffix).** Distinct left neighbours of 740 among 100 randomly chosen occurrences (rarefaction, 1,000 draws, all unique ICIT strings), compared with the same quantity for the other signs with ≥ 100 occurrences. The suffix reading predicts high diversity; decision: the claim's prediction holds if the mean rarefied diversity of 740 is above the median of the other signs.

### Results CT32a, CT19, CT25, CT14

Script: `scripts/claims_batch2.py`; results: `results/claims_batch2.json`.

- **CT32a: supported.** At Harappa, tablet texts occur on 2.84 records per distinct text, seal texts on 1.05; permutation mean of the difference 0.49; p = 0.0001. Tablets were made in series with identical texts, seals were individual (compare CT28).
- **CT19: not supported.** Conditional entropy divided by unigram entropy (300-line samples): Indus 0.43 (ICIT) and 0.48 (KP1979); full writing 0.38–0.50; non-linguistic 0.43 (totem poles) to 0.92 (weather icons). The Indus values lie inside the full-writing range but also inside the non-linguistic range (both transcriptions), so the measure does not place the Indus corpus with writing as claim C19 requires.
- **CT25: drop after seven.** Short-stroke counts (KP1979 normalised): 1: 248, 2: 273, 3: 236, 4: 51, 5: 54, 6: 28, 7: 50, 8: 5, 9: 1. A log-linear decline fitted to counts 3–7 predicts 34.5 occurrences of 8 and 9; 6 are observed (Poisson cdf 3 × 10⁻⁹). By the registered rule there is a **drop after seven**. Two cautions: count 7 is raised by the fixed pairing 7 + 585/575 (H3.12a), and a decimal system in which large single-group numbers were rarely needed would also show a drop. The base remains **undecided**; the drop is recorded as a fact.
- **CT14: supported.** Rarefied to 100 occurrences, 740 has 55.2 distinct left neighbours, the highest of the 22 signs with ≥ 100 occurrences (median of the others 27.5). The jar sign follows a wider variety of signs than any other frequent sign, as a freely attaching final element would.

**Correction.** The descriptive entry for C14 (`results/claims_descriptive.json`, "left-neighbour types per occurrence", 0.19 for 740) and its use in `docs/CLAIMS_EVALUATION.md` ("740 follows a narrow set of signs") were wrong in interpretation: distinct neighbours per occurrence fall automatically with frequency, and 740 is the most frequent sign. With frequency controlled by rarefaction (CT14), 740 has the most diverse left context of all frequent signs. The claims evaluation is corrected.

### R6 (review): robustness of H9.3 to resolution and seed

Script: `scripts/review_r6_h93_robustness.py`; results: `results/review_r6_h93_robustness.json`. Not pre-registered.

| Louvain resolution | ARI over five seeds | p (2,000 permutations) |
|---|---|---|
| 0.6 | 0.005–0.089 | 0.003–0.31 |
| 0.8 | 0.055–0.080 | 0.003–0.015 |
| 1.0 (registered) | 0.185–0.218 | ≤ 0.0005 |
| 1.2 | 0.242–0.320 | ≤ 0.0005 |
| 1.5 | 0.102–0.207 | ≤ 0.001 |

The agreement between the transcriptions holds for every seed at the registered resolution and at finer resolutions (1.0–1.5), but is weak and not always significant when the graphs are cut into a few large classes (0.6–0.8). H9.3 stands, with the qualification that the agreement concerns fine-grained substitution classes, not a coarse division of the inventory.

### Consistency review of the summary documents (corrections)

A review compared every number and verdict in the summary documents with this journal and the result files. Corrections made:
- **CT15 strata.** The sentence above, "with the same direction in each stratum", is wrong against its own table: in the "other sites" stratum the single tablet text ends in 740 (tablet share 1.00 vs seals 0.79). The direction holds at Harappa and Mohenjo-daro; the pooled CMH result (OR 4.3, p = 0.0022) is unchanged. All summaries now say "at Harappa and Mohenjo-daro (site-stratified; the 'other sites' stratum has a single tablet text)".
- **Family-wise count.** The CT15 caveat listed eight questions on the strict held-out set; H8.1, H9.2 (secondary) and E3d were also decided on it, so the count is at least eleven (0.01/11 ≈ 0.0009). CT15 fails this correction either way.
- **D1 in KP1979.** Proto-Elamite is nearest in both transcriptions, but proto-cuneiform is second only for ICIT and farthest for KP1979. Summaries that said "then proto-cuneiform, in both transcriptions" were corrected; the README no longer cites D3 and D5 as evidence of closeness.
- **F2 scope.** F2 tested only 4–9 strokes → 390–407 on later finds; summaries that implied all count–item pairings were confirmed on later finds were corrected.
- **Other corrections:** CT16 wording (texts with the jar sign contain numerals less often); H9.3 (the short-stroke numerals form one class; 001, 031 and 033 fall in the class with the fish-shaped signs); COUNTED_ITEMS (002 and the L3b status of KP 119/122; H9.1 is the variable-slot test); claims evaluation C4 (consistent for KP1979 only), C15 (caveats added), C29 (H3.6 exception), verdict labels "partly / weakly supported" defined; data ledger (fresh-set definition, D1-KP note, C2/C2k downgrade notes, held-out question counts); phase 5–7 report (narrow functional L2 added, gate G2 restated).

---

## 2026-11-25 (day 1, twenty-third working session, 15:18 UTC): replications and claim C27

Plan: (1) background survey of the meaning of the ICIT object and class codes; (2) CT27; (3) CT28k; (4) CT14k; (5) CT25b; (6) documents.

### Pre-registrations (before running)

**CT27 (claim C27: logograms rather than phonograms).** A syllabic system lets frequent signs combine freely, so the share of possible ordered pairs among its 50 most frequent signs that actually occur (bigram density) is high; a logographic system with semantic restrictions gives a sparser matrix. For 20 resamples of 9,000 tokens (unique lines) the bigram density of the 50 most frequent signs is computed for the Indus corpus (ICIT) and for the Akkadian OB letters (syllabic graphemes). Prediction: Indus density lower than Akkadian in ≥ 19 of 20 resamples. KP1979 (normalised as in R4) is reported in the same way as a second transcription.

**CT28k (replication of CT28 in KP1979).** Stems (text without the final run of KP terminal-set signs of `src/indus/controls.py`) of KP records with seal codes {11, 23} vs tablet codes {62, 67, 72, 75} (codes identified in C2k); share of distinct stems among n records with n equal for both classes (the smaller count), 1,000 subsamples; prediction: seal share higher in ≥ 99 % of subsamples. (KP has no decoded site field, so no stratification.)

**CT14k (replication of CT14 in KP1979).** Rarefied left-neighbour diversity (100 occurrences, 1,000 draws) of the jar sign in KP1979 (324 and 325 pooled as one sign, as ICIT 740 pools them) compared with the other KP signs with ≥ 100 occurrences (normalised as in R4). Prediction: the jar sign above the median of the others.

**CT25b (robustness of CT25).** As CT25, but removing from the counts every occurrence of 7 strokes directly followed by 288 or 289 (the fixed pairing of H3.12a) before fitting counts 3–7 and predicting 8 + 9. Reported as a robustness check: whether the drop after seven remains (observed 8 + 9 below the 1st percentile of the Poisson prediction).

### Results CT27, CT28k, CT14k, CT25b

Script: `scripts/claims_batch3.py`; results: `results/claims_batch3.json`.

- **CT27: supported.** Bigram density of the 50 most frequent signs (9,000-token samples): Indus ICIT 0.283, KP1979 0.332, Akkadian OB letters (syllabic graphemes) 0.401. The Indus value is lower than the Akkadian one in 20 of 20 resamples for both transcriptions. Frequent Indus signs combine less freely than the graphemes of a syllabic script, as claim C27 (logograms in functional classes) predicts. This does not show that the signs are logograms of a language; a non-linguistic system with restricted combinations would also be sparse.
- **CT28k: supported (replication).** KP1979 records with seal codes (1,490) vs tablet codes (952), subsamples of 952: the share of distinct stems is 0.57 higher for seals, higher in 1,000 of 1,000 subsamples. CT28 is reproduced in the independent transcription with its independent object classification.
- **CT14k: supported (replication).** In KP1979 (324 and 325 pooled), the jar sign has a rarefied left-neighbour diversity of 51.1 (100 occurrences), the highest of 24 signs with ≥ 100 occurrences (median of the others 25.0). CT14 is reproduced.
- **CT25b: the drop after seven remains.** With the fixed pairing 7 + 288/289 removed, the count of seven falls from 50 to 24; the fit on counts 3–7 predicts 18.1 occurrences of 8 + 9; 6 are observed (Poisson cdf 0.001). The drop after seven is not an artefact of the fixed pairing. The base remains undecided (a decimal system with rarely needed large single-group numbers would show the same).

### Pre-registrations (continued, before running)

**CT32k (replication of CT32a in KP1979).** KP records with tablet codes {62, 67, 72, 75} occur on more records per distinct text than records with seal codes {11, 23}. Statistic: difference of mean records per distinct text; null: 10,000 permutations of the class labels; one-sided p < 0.01. (KP records are inscriptions; repeated texts on different objects appear as different records.)

**CT22 (claim C22, distributional part: the fish signs form one class).** ICIT fish-shaped set {220, 222, 226, 231, 233, 235, 236, 240, 241}. Mean pairwise context similarity (1 − JS of previous/next-sign distributions) of the set members with ≥ 5 occurrences, computed on the strict held-out set plus fresh sets 1 and 2; null: 10,000 random sets of the same size from signs with ≥ 5 occurrences there, each member matched to a fish sign by frequency (within a factor of 1.5 where possible). Prediction: fish set more similar, p < 0.01.

### Results CT32k and CT22

Script: `scripts/claims_batch4.py`; results: `results/claims_batch4.json`.

- **CT32k: supported (replication).** KP1979: tablet texts occur on 2.61 records per distinct text, seal texts on 1.10; p = 0.0001. CT32a is reproduced with the independent transcription and object codes.
- **CT22: supported.** On the strict held-out and fresh data, six fish-shaped signs have at least 5 occurrences (220, 231, 233, 235, 236, 240); their mean pairwise context similarity is 0.211, against 0.104 (SD 0.025) for frequency-matched random sets; p = 0.0009. The plain and modified fish-shaped signs are used in similar contexts, as a single functional class would be (claim C22, distributional part; compare G2 and H9.3). The reading of the fish sign as *mīn* "fish/star" is not tested by this.

### Meaning of the ICIT object and class codes

`docs/OBJECT_CODES.md` collects what could be found about the codes. Findings relevant to earlier tests:
- `SEAL:S` (square, motif), `SEAL:R` (rectangular, no motif) and `TAB:C` (copper tablet) agree with the meanings inferred from the data in C2 and C1.
- `TAB:B` (bas-relief tablets) and `TAB:I` (incised tablets) have only a weak source (a search-engine summary).
- The pottery letters `g` (incised graffito) and `s` (stamped) are likely but unsourced; CT15s relied on this reading, so its descriptive note ("incised pottery also ends in 740") carries this uncertainty.
- The `class` field is a classification derived from the text itself (for example `NU` numeral-only texts, `VN` sign 700 followed by a numeral). It was never used as an external variable in any test of this project; tests that used it would be circular.

---

## 2026-11-25 (day 1, twenty-fourth working session, 16:18 UTC): multi-line texts, combined numerals, formulae across transcriptions

### Plan of the run

1. ML1, ML1k: do the lines of a two-line object form one text or separate texts? (ICIT; KP1979 replication)
2. NUM2: do different stroke signs combine in a fixed order, as the units of a multi-unit numeral notation would? (ICIT, KP1979)
3. NUM1: order of numeral and counted sign in the Indus texts compared with proto-Elamite and proto-cuneiform (L-1, descriptive comparison with a decision stated in advance)
4. KF1: formula table for KP1979 and reproduction of the ICIT formulae across transcriptions
5. R7: family-wise review of all decisive p-values
6. L-3b: combined sign inventory (descriptive document)
7. Literature notes on numeral order and multi-line texts (survey done in parallel; see below)
8. Interim report 4; README, claims evaluation, final report

### Pre-registrations (before running)

**ML1 (ICIT).** Objects with exactly two lines, both complete and without unreadable signs. A line "closes" if its last sign in reading order is in the ICIT terminal set {740, 400, 520, 090, 151, 407, 527, 156}.
- Hypothesis: the two lines form one continuous text, which is closed only once.
- Statistic: number of objects in which exactly one of the two lines closes.
- Null: 10,000 random re-pairings of the lines, within groups of objects with the same `type` value. This keeps the closing rate and tests only dependence within objects.
- Prediction: the statistic exceeds the null, one-sided p < 0.01 (smallest attainable p ≈ 0.0001).
- Insufficient data: fewer than 30 objects.
- Descriptive: the number of objects where both lines close (one-sided p in the other direction); and, among objects with exactly one closing line, whether it is line 0 or line 1 of the source.

**ML1k (KP1979).** The same test for KP objects with exactly two records, both complete and without `?`, using `lines_code` 2. The meaning of the code (two lines on one face, as opposed to 6 for different faces) is inferred from the data, not from a source. Terminal set: {324, 325, 98, 217, 326, 1, 13, 4, 301}; groups: `type_code`. Code 6 is reported descriptively.

**NUM2 (ICIT, KP1979).** All unique complete strings without `?`. Count the adjacent pairs (a, b) in reading order where both signs are stroke signs and a ≠ b.
- ICIT stroke sets: short {001, 003, 004, 034, 005, 016, 017}; long {031, 032, 033, 035}.
- KP stroke sets: short 121–130; long {144, 145, 147, 150, 151}.
  - First, any adjacent pair of 121/144 (in any combination) is merged into one two-stroke token of unknown length class. These pairs are how KP writes the ICIT two-stroke sign 032 (fourteenth session).
  - Merged tokens are excluded from the order count.
- Pair types: LS (long then short) and SL (short then long).
- Hypothesis: long and short strokes are units of a multi-unit notation written in a fixed order.
- Prediction: one order makes up at least 80 % of LS + SL pairs, with a two-sided binomial p < 0.01, in each transcription separately.
- Insufficient data: fewer than 10 LS + SL pairs.
- Descriptive: pairs of two different short (or two different long) signs.

**NUM1 (descriptive comparison, L-1).** For each numeral token that has a non-numeral neighbour within the line on exactly one side, record whether that neighbour follows or precedes it.
- Indus: ICIT, in reading order, with the stroke signs of NUM2 as numerals.
- Proto-Elamite and proto-cuneiform: CDLI lines, tokens containing `(N` as numerals.
- Statistic: share of "neighbour follows" (the numeral comes before the sign).
- Decision stated in advance: the Indus order is called "like proto-Elamite" if its share and the proto-Elamite share are on the same side of 0.5, and "like proto-cuneiform" otherwise. The proto-cuneiform order is the editorial order of the CDLI transliteration (see literature notes).

**KF1 (cross-transcription reproduction of formulae).**
- Build the formula table for KP1979 (normalised as in R4) with the method of `scripts/phase9_formulae.py`: templates with one variable slot and at least three different fillers.
- Map each sign of each ICIT formula frame (the template without the slot) to its KP counterpart through the concordance (`results/phase1_concordance.tsv`, best match).
- A frame is reproduced if the mapped frame takes at least two different fillers in KP.
- Control: ICIT frames with exactly one filler, of the same length distribution (all of them, stratified by length).
- Prediction: formula frames are reproduced more often than control frames; Fisher exact one-sided p < 0.01.
- This is a check across transcriptions of the same objects, not a test on unused data.

**R7 (review).** List the decisive p-value of every supported result decided on held-out, strict held-out or fresh data, and apply Holm and Benjamini–Hochberg corrections over that family (α = 0.01 and 0.05). Report which results survive.

**R7b (added before running R7's corrections, after seeing the R7 table).** The permutation p-values of B1, B4, CT17 and CT18 are bounded below by 1/1001 (1,000 control draws), which is too coarse for a family-wise correction over about 40 tests. They are re-run unchanged except for 10,000 control draws (scripts `review_r7b_*.py`, generated from the original scripts). The verdicts of the original tests are not changed by this; R7 is recomputed with the new p-values.

### Results ML1, ML1k, NUM2, NUM1, KF1

Script: `scripts/batch5_lines_numerals_formulae.py`; results: `results/batch5_lines_numerals_formulae.json`; KP formula table: `docs/FORMULAE_KP.md`.

- **ML1: supported.** 76 ICIT objects have two complete lines.
  - Exactly one line closes with a terminal sign on 47 objects, against 33.0 under random re-pairing (p = 0.0001).
  - Both lines close on only 3 objects, against 10.0 expected (p = 0.0001 in the other direction).
  - The two lines of an object behave as one text that is closed once, not as two separate texts.
  - When one line closes, it is line 1 of the source in 36 cases and line 0 in 11. This agrees with the description, quoted in the literature notes below, that the final (leftmost) signs of longer inscriptions are moved to the second line.
- **ML1k: supported (replication).**
  - KP objects with `lines_code` 2 and two complete records (80 objects): exactly one closes on 47, against 34.8 expected (p = 0.0023); both close on 3, against 9.1 expected.
  - In KP the closing record is more often record 0 (30 vs 17). KP therefore orders the lines of an object differently from the ICIT-style source. Which line comes first on the object cannot be decided from the codes.
  - `lines_code` 6 (437 objects; probably different faces, unsourced): exactly one closes on 329, against 213.9 expected (p = 0.0001); the closing record is record 0 in 322 cases. On these objects one record carries the closed text and the other does not. This is reported descriptively, because the meaning of the code is not established.
- **NUM2: not supported (ICIT); insufficient data (KP).**
  - ICIT: long-then-short 22, short-then-long 11 (67 %, binomial p = 0.080). A fixed order of long and short strokes, as in a multi-unit notation, is not shown.
  - KP: after merging the 121/144 pairs, only 9 long–short pairs remain.
  - Descriptive: adjacent pairs of two different short-stroke signs are not rare (ICIT 20, KP 29). In both transcriptions the most frequent pattern is a single stroke followed by another count: ICIT `001 003` 7, `001 004` 6; KP `121 124` 5, `121 123` 5, `121 125` 4. This pattern was seen after the test and is not tested; no unused data are left on which to test it.
- **NUM1 (descriptive comparison): "like proto-cuneiform" by the rule stated in advance.**
  - Share of numerals followed rather than preceded by a non-numeral sign: Indus (ICIT) 0.71 (305 vs 124), proto-Elamite 0.004, proto-cuneiform 0.98.
  - In the Indus texts the numeral comes before the sign it goes with (as in H3.10), the opposite of the proto-Elamite entries. The proto-cuneiform order is the order of the CDLI transliteration, which for that script is partly an editorial convention (literature notes).
  - The Indus order therefore separates the Indus texts from proto-Elamite, the system they are otherwise closest to (D1). This is a descriptive difference, not a test.
- **KF1: supported (check across transcriptions).**
  - Of 147 ICIT formula frames that can be mapped through the concordance, 110 (75 %) take two or more fillers in KP1979, against 301 of 3,830 (7.9 %) single-filler control frames (odds ratio 34.9, p < 10⁻⁸⁰).
  - KP1979 has 126 formula templates (`docs/FORMULAE_KP.md`). The formulae are a property of the inscriptions, not of one transcription.

### Literature notes on numeral order and multi-line texts

A literature survey was run in parallel. The sites cdli.ox.ac.uk and arxiv.org could not be reached from the working environment. The quotations below are therefore the excerpts returned by a search engine and have not been checked against the full texts.

- CDLI wiki, "Proto-Elamite writing phases" (<https://cdli.ox.ac.uk/wiki/proto-elamite_writing_phases>), excerpt: tablets from Iran "can be distinguished from Mesopotamian ones only by the order of the numerical signs and non numerical signs; in Iran the numerical signs follow the object they qualify".
- Encyclopaedia Iranica, "Proto-Elamite" (<https://www.iranicaonline.org/?p=9917>), excerpt: "each entry normally includes an ideogram followed by a numerical notation, a divergence from the strict sequence of numerical sign followed by ideogram in proto-cuneiform texts".
- CDLB 2021:6 (<https://cdli.earth/articles/cdlb/2021-6>), excerpt: proto-cuneiform signs "are not inscribed on tablets in a strictly linear order".
- Mahadevan, review of Parpola on harappa.com (<https://www.harappa.com/script/maha6.html>), excerpt: "shorter inscriptions start at the right edge, leaving blank space nearer the left edge, and the left-most signs of the longer inscriptions are displaced to the second line"; internal evidence was "obtained by comparing single-line and two-line sequences of identical inscriptions".

Analysis:
- The NUM1 figures agree with these excerpts. Proto-Elamite puts the sign before the numeral, and proto-cuneiform puts the numeral first.
- The ML1 result agrees with the description of the second line as the continuation of one text.
- No source was found on whether Koskenniemi & Parpola read doubled signs as "two" or as a plural. This is not known.

### Results R7 and R7b (family-wise review)

Scripts: `scripts/review_r7_familywise.py`, `scripts/review_r7b_*.py`; results: `results/review_r7_familywise.json`, `results/review_r7b_*.json`.

- **R7b.** With 10,000 control draws, B1, B4, CT17 (both transcriptions) and CT18 (both) all give p = 0.0001 (the smallest attainable). Their verdicts are unchanged.
- **R7 family.** 37 tests decided on fresh data or on the strict held-out set: F2, F3, F2b, F3b, B1, B4, H5.1b, F4, H6.1, H7.1, the R1 re-tests of H3.3, H3.10 and H3.12, H8.1, H9.2 (secondary), G2, the six H9.4 confirmations, CT16, CT17, CT18, CT15, CT15k and CT22.
  - The C2 and C2k associations are not included. They were selected on the full held-out split, and their registered families (0.01/40 and 0.01/10) are failed after R1.
  - The family includes failed tests, as it should.
- Tests surviving each correction:
  - Holm at α = 0.01: 15 tests survive. They are the F3 direction test; H3.3 (ICIT), H3.10 (both) and H3.12a/b (H3.12a ICIT, H3.12b both); B1; B4; CT17 (both); CT18 (both); F2; and H9.4 class 4 × copper tablets.
  - Holm at α = 0.05: these and F3b, H3.3 (KP), H3.12a (KP), CT22, F3 bigram vs unigram, H6.1, G2 and CT15, 23 in all.
  - Benjamini–Hochberg at q = 0.01: the same 23; at q = 0.05: 26 (adding F4, H8.1 and H9.4 class 4 × motif seals, which were registered as failed and stay failed).
- Consequences:
  - The core L1 results (direction, closing cluster, count–item pairs, template, recurring units, nested structure) survive the strictest correction applied here.
  - CT15, the functional L2 result, survives Holm at α = 0.05 and false-discovery control at q = 0.01, but not Holm at α = 0.01. Its earlier description ("would not survive a family-wise correction over the strict held-out questions at 0.01") stays true for the family-wise error rate at 0.01. It is now stated with these figures.
  - H9.4 class 4 × copper tablets survives even Holm at α = 0.01. It remains an L2 candidate only because the class has no interpretation fixed in advance, not because of multiple testing.

### Pre-registration of ML2 (before running)

**ML2 (line breaks at segment boundaries).** If a two-line inscription is one text (ML1), the scribe may break it at the boundary of a recurring segment, or simply where the space runs out.
- Data:
  - ICIT objects of ML1 (two complete lines).
  - KP objects of ML1k with `lines_code` 2.
- Text of each object: the two lines joined, with the line that closes put last. If neither or both lines close, the ICIT order (line 0, line 1) is used, and the KP order is reversed (record 1, record 0), following the majority order in ML1/ML1k.
- Statistic: share of line parts (two per object) that occur as complete single-line texts on other objects (unique complete strings of single-line objects; strings of the object itself are not counted).
- Control: for each object, the joined text is cut at a random position, other than the real one, that leaves at least one sign on each side; 10,000 draws.
- Prediction: the real share is higher, one-sided p < 0.01, in each transcription.
- Insufficient data: fewer than 30 objects.

### Result ML2: not supported

Script: `scripts/batch5b_ml2_line_breaks.py`; results: `results/batch5b_ml2_line_breaks.json`.

ICIT: 25.7 % of line parts occur as complete single-line texts elsewhere, against 24.9 % for random cuts (p = 0.43). KP: 15.0 % against 14.6 % (p = 0.46). Objects whose joined text has only two signs (ICIT 6, KP 4) keep their real cut in the control, because no other cut exists. The line break of a two-line inscription does not fall at segment boundaries more often than a random cut. This fits the description of signs being moved to the second line when the space runs out, rather than a break at a boundary in the text. ML1 and ML2 together: one text per object, broken where the space ends.

### L-3b combined sign inventory (descriptive)

`docs/COMBINED_INVENTORY.md` (script `scripts/l3b_combined_inventory.py`) combines the allograph decisions of L3a and L3b.
- Rule: a group is merged only if no pair inside it differs in usage.
- Merged: ICIT 705/706, 790/850, 817/861 and 154/156; KP 50/56/58 (fish-shaped) and 325/326.
- Kept separate: ICIT 151/158, 617/741, 803/806 and 390/405/407; KP 324/325/326, 119/122, 123/147 and 62 vs 50/56.
- Result: 713 ICIT types − 4 + 5 = 714 units. The allograph decisions supported by usage do not change the inventory estimate of D3 in any material way.
- No key L1 test is re-run on the combined list. Its merges concern rare signs outside the tested sets, and its splits cannot be applied to ICIT tokens without a per-token alignment.

### Pre-registration of F5 (before running)

**F5 (formulae learned from training data recur in later finds).**
- Formulae: templates of length ≥ 3 with one variable slot and at least three different fillers. They are found, as in `scripts/phase9_formulae.py`, on ICIT training strings only (not `is_heldout`, and not from the ten fresh sites).
- Test strings: unique complete ICIT strings of length ≥ 3, without `?`, from fresh sets 1 and 2.
- A string matches if it equals a template with any sign (including signs not seen in training) in the slot.
- Statistic: number of fresh strings matching at least one template.
- Control: each fresh string is replaced by a rule-preserving control (`indus.controls.control`; keeps the length, the closing cluster and the count–item pairs); 10,000 draws.
- Prediction: more real strings match than control strings, one-sided p < 0.01.
- Insufficient data: fewer than 5 real matches.
- This adds one question to the fresh data (R7 family: 38).

### Result F5: supported

Script: `scripts/batch5c_f5_formulae_fresh.py`; results: `results/batch5c_f5_formulae_fresh.json`.
- 52 formula templates of length ≥ 3 were found on 1,561 training strings.
- Of 86 fresh strings of length ≥ 3, 9 fit a template (for example `861 002 016 390`, `817 002 222 740`, `920 740 400`), against 4.8 on average for rule-preserving controls (p = 0.0008).
- Formulae with a variable slot learned from the older corpus recur in later finds beyond what the established rules (length, closing cluster, count–item pairs) explain. The effect is small in absolute terms: most fresh strings fit no training formula.
- R7 recomputed with F5 (38 tests): Holm 0.01 keeps the same 15 tests; F5 survives Holm 0.05 and BH 0.01.

### Two-face objects: observation and pre-registrations FACE1, FACE2 (before running)

**Observation (descriptive, made while checking ML1k).**
- Of the KP objects with `lines_code` 6 and exactly one closing record, 329 have a non-closing record. In 240 of these it contains stroke signs, and it is mostly a stroke numeral followed by KP 310: `147 310` 59, `123 310` 35, `124 310` 25, `145 310` 25.
- The ICIT-style source records the faces of an object as `object_id` suffixes (`162.1`, `162.2`). In it, 246 two-face objects have one face of the form "stroke numeral(s) + 700" in reading order (ICIT 700 = KP 310), almost all of them Harappa tablets (`TAB:B` 123, `TAB:I` 119).
- So these tablets carry a numeral face and a text face.

**FACE1 (ICIT; replication KP `lines_code` 6).** On two-face objects with one complete line per face, and where neither face is a numeral + 700 (KP 310) face, the two faces behave as one text closed once.
- Same statistic, null and decision as ML1 (exactly one face closes; 10,000 re-pairings within object type; one-sided p < 0.01).
- Insufficient data: fewer than 30 objects.

**FACE2 (ICIT; replication KP).** On the two-face objects with a numeral face, the numeral face is fixed for a given text: objects whose text faces are identical have identical numeral faces more often than chance.
- Data: ICIT objects as in the observation (246). For KP, objects with `lines_code` 6 and two complete records, one of which consists of stroke signs followed by 310.
- Statistic: share of pairs of objects with identical text faces that also have identical numeral faces.
- Null: the numeral faces are permuted among all objects of the same object type; 10,000 draws.
- Prediction: the share is higher, one-sided p < 0.01.
- Insufficient data: fewer than 10 groups of identical text faces.
- The lower tail is reported descriptively. A result in that direction would mean the count varies within a series of identical texts.

### Results FACE1, FACE2

Scripts: `scripts/batch5d_two_face_objects.py`, `scripts/batch5d_face2_robustness.py` (post hoc); results: `results/batch5d_two_face_objects.json`, `results/batch5d_face2_robustness.json`.

- **FACE1: supported (both transcriptions).** On two-face objects without a numeral face, exactly one face closes:
  - ICIT: 175 of 258 objects, against 126.3 expected (p = 0.0001); both faces close on 27, against 51.3 expected.
  - KP (`lines_code` 6): 123 of 195, against 92.1 expected (p = 0.0001).
  - As with two lines on one face (ML1), the faces of one object carry one text, closed once.
- **FACE2: supported (both transcriptions).**
  - ICIT: 246 objects, 37 groups of identical text faces, 517 pairs. Identical numeral faces in 52.2 % of the pairs, against 33.9 % under permutation (p = 0.0001).
  - KP: 242 objects, 38 groups. 24.2 % against 17.5 % (p = 0.0093). The KP figure is lower because KP writes the same count in several ways (`145 310`, `144 121 310`, `121 121 310` for two strokes).
- Post-hoc robustness (descriptive). The pair statistic is dominated by the largest group (ICIT `176 740 400`, 30 objects, 435 of 517 pairs). Without this group the ICIT share is 62.2 % against 33.0 % (p = 0.0001), and with every group weighted equally it is 56.6 % against 32.8 % (p = 0.0002). KP: 29.0 % against 17.3 % (p = 0.0029), and 33.3 % against 16.7 % (p = 0.0010).
- Interpretation:
  - The numeral face of these Harappa tablets is not independent of the text on the other face. Objects with the same text tend to carry the same count.
  - The count is not fixed, though. The largest series `176 740 400` has three strokes on 20 objects, four on 8 and two on 2.
  - In the ICIT transcription the numeral face takes only three values: two (032), three (033) or four (034) strokes, with 700.
  - The tablets were made in series (CT32a), and the count belongs partly to the series. It varies within a series more than a fixed label would.
  - What the count records is not established. No published discussion of these numeral faces was checked in this session; this is an open item for the literature survey.

### Object size as an external variable: pre-registrations SZ1, SZ2, FACE3 (before running)

The ICIT-style source records object dimensions (`horizontal(mm)`, `vertical(mm)`, `thickness(mm)`; non-zero for 1,488 `SEAL:S`, 683 `TAB:B`, 617 `TAB:I`, 313 `SEAL:R`, 204 `TAB:C` records). No earlier test has used them. Size is information outside the texts. If a sign predicts the size of the object on unused data, beyond text length and site, that would be a functional association of the L2 kind.

Common definitions:
- Unit: one object (`object_id` without the face suffix). Its text is all its lines joined in reading order, faces in suffix order.
- Its size is the log of horizontal × vertical (mm²), taken from the first face that has both values > 0.
- Objects with any incomplete line or a `?` are excluded.
- Residual size: log area minus the mean log area of objects of the same type, the same site and the same text length (lengths ≥ 8 pooled). Objects that are alone in their stratum are dropped.

**SZ1 (sanity check).** On `SEAL:S` objects, log area and text length are positively correlated (Spearman, one-sided p < 0.01, all objects). This is expected if longer legends need larger seals; a failure would mean that the size data cannot be used.

**SZ2 (discovery and confirmation scan, `SEAL:S`).**
- Discovery set: objects whose text is a training string (not `is_heldout`), from sites other than the ten fresh sites.
- Confirmation set: objects whose text is in the strict held-out set, plus objects from the fresh sites.
- For every sign that occurs in at least 20 discovery objects, compare the residual size of objects containing it with that of the others (Mann–Whitney, two-sided). Signs with discovery p < 0.01 are candidates.
- Each candidate is tested on the confirmation set in its discovered direction (one-sided Mann–Whitney), with the Bonferroni threshold 0.01/k for k candidates.
- Prediction: at least one candidate is confirmed. If there are no candidates, the result is "not supported".
- Insufficient data for a candidate: fewer than 5 confirmation objects contain it.

**FACE3 (numeral faces and tablet size).**
- Data: the ICIT two-face tablets of FACE2 with size data.
- Question: within series of identical text faces, is the count on the numeral face (2, 3, 4 strokes: 032, 033, 034; other faces excluded) related to the log area of the object?
- Statistic: Spearman correlation of count and log area, computed after centring both within each text series of at least 2 objects.
- Null: counts permuted within series; 10,000 draws.
- Prediction: none on direction; two-sided p < 0.01.
- Insufficient data: fewer than 30 objects in series with varying counts.

### Results SZ1, SZ2, FACE3

Script: `scripts/batch5e_object_size.py`; results: `results/batch5e_object_size.json`.

- **SZ1: passed (sanity check).** On 1,180 `SEAL:S` objects with size data, log area and text length are correlated (Spearman 0.42, p < 10⁻⁵⁰). The size data behave as expected.
- **SZ2: not supported.**
  - Discovery: 880 seals. Of 43 signs scanned, three are candidates: 590 on smaller seals (p = 0.0007), and 692 (p = 0.0059) and 706 (p = 0.0001) on larger seals, beyond text length, site and type.
  - Confirmation: 166 seals. All three go in the discovered direction (p = 0.038, 0.033, 0.026; 14, 5 and 6 objects), but none reaches the threshold 0.0033.
  - No sign is shown to predict seal size. The consistent direction is noted, but a combined test was not registered, and none is claimed. Three confirmation objects have a residual of exactly zero (strata of identical sizes). This does not affect the tests.
- **FACE3: not supported.** Among 64 tablets in 17 series of identical text with varying counts, the within-series correlation of count and log area is 0.009 (p = 0.95). The count on the numeral face does not go with the size of the tablet.
- The data-use ledger now counts SZ2's confirmation as one more question decided on the strict held-out and fresh data (R7 family: 39; not recomputed, since SZ2 failed and would not change the surviving set).

### Literature notes on the numeral faces of Harappa tablets

The hosts holding the full texts (harappa.com, helda.helsinki.fi, nature.com) could not be reached from the working environment. The excerpts below are search-engine excerpts and have not been checked against the full texts.
- Kenoyer & Meadow (2010), "Inscribed objects from Harappa excavations 1986–2007" (CISI 3.1), excerpt: "the tablets (or tokens) are common at Harappa, and multiple copies were often produced".
- Parpola, "Indus writing" (<https://www.harappa.com/sites/default/files/pdf/indus-writing.pdf>), excerpt: one side of most Harappa tablets "usually has nothing but this pot-sign, preceded by one to four vertical strokes". The sign is described as "U-shaped".
- A paper on helda.helsinki.fi (attribution to Parpola not confirmed), excerpt: the reverse sides "have the signs VII, VIII or VIIII, probably meaning 'two/three/four pots (of offerings)'".

Analysis:
- The excerpts agree with the data: the numeral face is a count of two to four strokes with one sign (FACE2: in ICIT only 032, 033 and 034 with 700, and one 031).
- Whether the count is constant within a series of identical texts was not found in the excerpts. FACE2 shows that it is partly tied to the series but varies within it. The reading "pots of offerings" is not tested by any analysis here.

### Pre-registration of SZ4 (before running)

**SZ4 (seals with identical legends are similar in size).** Seal legends are mostly individual (CT28). If the few seals that share a legend belong together (made as a set, or for the same holder), they should be closer in size than other seals of the same kind.
- Data: `SEAL:S` objects with size data, as in SZ1, all of them.
- Pairs: two objects with identical text from different records. Pairs with the same non-empty `excavation-idno` are dropped (possible double records).
- Statistic: mean absolute difference of log area over these pairs.
- Null: for each pair, the second object is replaced by a random `SEAL:S` object of the same site and text length (excluding the first object); 10,000 draws.
- Prediction: the real mean difference is smaller, one-sided p < 0.01.
- Insufficient data: fewer than 20 pairs.
- Descriptive: the number of pairs with exactly equal dimensions.

### Result SZ4: not supported

Script: `scripts/batch5f_sz4_identical_seals.py`; results: `results/batch5f_sz4_identical_seals.json`.
- 49 legends occur on more than one square seal, giving 131 pairs. 80 of the pairs are from different sites, and only 3 have equal dimensions.
- The mean absolute difference of log area is 0.515, against 0.530 for random partners of the same site and length (p = 0.33).
- Seals that share a legend are no more alike in size than other seals. Shared legends are mostly short (for example `910 740`, `061 740`) and found at different sites. They look like common short legends rather than matching sets.

**FACE2, KP with normalised counts (post hoc, descriptive).** When the KP numeral faces are reduced to stroke counts (121/144 = 1, 122/145 = 2, 123/147 = 3, 124/150 = 4, summed), the counts are 2 (76), 3 (116), 4 (48) and 1 (2). Tablets with identical text share the count in 47.7 % of pairs, against 37.5 % under permutation (p = 0.0049). The KP result of FACE2 is therefore not an artefact of KP's several spellings of one count.

### Pre-registration of T2 (before running)

**T2 (chronological change of sign use at Mohenjo-daro).**
- The source assigns Mohenjo-daro records to Early / Intermediate / Late levels (`period`; for `SEAL:S`, Early 29, Intermediate 291, Late 231). How the levels were assigned (by depth, by excavator's stratum) is not documented in the source, so this is noted as a limitation.
- Unit: `SEAL:S` and `SEAL:R` objects from Mohenjo-daro with level Intermediate or Late; texts as in SZ2 (complete, without `?`).
- Discovery: objects whose text is a training string. For every sign in at least 15 discovery objects, compare the share of objects containing it between the two levels (Fisher exact, two-sided). Signs with p < 0.01 are candidates.
- Confirmation: objects whose text is in the strict held-out set. One-sided Fisher test in the discovered direction, with Bonferroni threshold 0.01/k.
- Prediction: at least one candidate is confirmed.
- Insufficient data for a candidate: fewer than 5 confirmation objects contain it.
- In addition (descriptive): the share of legends ending in 740 in each level, on all objects.

### Result T2: not supported

Script: `scripts/batch5g_t2_mohenjodaro_levels.py`; results: `results/batch5g_t2_mohenjodaro_levels.json`.
- 466 Mohenjo-daro seals (Intermediate 244, Late 222): 381 discovery and 52 confirmation objects.
- Of 34 signs scanned, none differs between the levels at p < 0.01 in the discovery set, so there are no candidates.
- Descriptive: legends ending in 740 make up 36 % of seals in the Intermediate levels and 42 % in the Late levels.
- No change of sign use between the Intermediate and Late levels of Mohenjo-daro is detected. This agrees with the negative chronological test at Harappa (T1). With these sample sizes, only large changes could have been found.

### Reproducibility check (R8)

`scripts/run_all.py --skip-heavy` re-ran every analysis up to R7 with no failures and no changed result files. The analyses added later in this session were re-run separately (FACE1–FACE3, SZ1–SZ4, T2), also without changes. All analyses of this session are listed in `scripts/run_all.py`.

### End of the twenty-fourth session

Pre-registered analyses in this session:
- Supported: ML1, ML1k, KF1, F5, FACE1, FACE2.
- Not supported: NUM2, ML2, SZ2, SZ4, FACE3, T2.
- Sanity check passed: SZ1.
- Descriptive comparison: NUM1.
- Reviews: R7, R7b, R8.
The level assessment is unchanged: L1 achieved, L2 only in narrow functional scope (CT15), L3 not achieved.

---

## 2026-11-25 (day 1, twenty-fifth working session, 17:18 UTC): iconographic detail, robustness of CT15, multi-face objects

### Plan of the run

1. MO2a, MO2b: do signs vary with iconographic details of unicorn seals (the object in front of the animal, `cult`; the suffix of the `Bull1` code)? These details have not been used before. C2 used only the base motif, and it found no motif association even on training data.
2. MO1k: sign × motif scan in KP1979 with its own icon codes (not scanned before; C2k used type codes only).
3. CT15r: robustness of CT15 to text length.
4. FACE4: objects with three or more faces.
5. Survey of the meaning of the `cult` codes and `Bull1` suffixes (background, in parallel).
6. Updates of ledger, claims, reports; reproducibility run.

### Pre-registrations (before running)

Common scan design for MO2a, MO2b and MO1k:
- Unit: one object, with its text as in SZ2 (all faces and lines joined; complete, no `?`).
- Discovery: objects whose text is a training string. For every sign in at least 15 discovery objects, a two-sided Fisher exact test of presence × binary variable; candidates have p < 0.01.
- Confirmation: objects whose text is in the strict held-out set, plus objects from the fresh sites (ICIT only). Each candidate gets a one-sided Fisher test in its discovered direction, with Bonferroni threshold 0.01/k.
- Prediction: at least one candidate is confirmed. If there are no candidates, the result is "not supported".
- Insufficient data for a candidate: fewer than 5 confirmation objects contain it.

**MO2a (ICIT).** `SEAL:S` objects with a `Bull1` motif (any suffix) and a `cult` code in {SAN, SAF, RAN, RAF, RBF, S}. Variable: `cult` = SAN (the most frequent code) vs any other of these codes. The meaning of the codes is not known at registration (survey in progress). The test asks only whether the text co-varies with this physical detail.

**MO2b (ICIT).** `SEAL:S` objects with motif code `Bull1:W`, `Bull1:J`, `Bull1:S`, `Bull1:I` or `Bull1:L`. Variable: suffix W (the most frequent) vs the others.

**MO1k (KP1979).** Records with `type_code` 11 (seals) and an icon code. Variable: icon code 40 (the most frequent; probably the unicorn, not checked) vs all other icon codes except 99 (excluded: possibly "unknown"; unsourced). Discovery: KP training strings (not `is_heldout`); confirmation: KP strict held-out strings.

**CT15r (robustness of CT15).** The CT15 data and test, with the CMH strata defined by site stratum × text-length band (2, 3, 4, ≥ 5 signs) instead of site stratum alone. Tablet texts are shorter on average, and the final position of 740 could depend on length. Prediction: one-sided p < 0.01. A failure would mean CT15 is partly a length effect.

**FACE4 (ICIT).** Objects with three or more faces, each face one complete line without `?`.
- Statistic: number of objects on which exactly one face closes.
- Null: faces re-assigned at random among these objects, keeping each object's number of faces; 10,000 draws.
- Prediction: more objects with exactly one closing face than under the null, one-sided p < 0.01.
- Insufficient data: fewer than 20 objects.
- The ICIT objects of this kind are mostly incised tablets from Harappa (to be reported).

### Results MO2a, MO2b, MO1k, CT15r, FACE4

Script: `scripts/batch6_iconography_faces.py`; results: `results/batch6_iconography_faces.json`.

- **MO2a: not supported.** 623 discovery and 118 confirmation unicorn seals; codes SAN 552, SAF 96, RAN 69, RAF 51, RBF 19, S 17. Of 47 signs, none differs between SAN and the other codes at p < 0.01 in the discovery set.
- **MO2b: not supported.**
  - 597 discovery and 110 confirmation unicorn seals; suffixes W 328, J 171, S 140, I 84, L 41. The suffixes occur at every main site, so they are not site codes.
  - Four candidates: 240 more often with W, 390 less often, 798 more often, and 405 more often (18 of 261 W seals against 0 of 336 others).
  - On the confirmation set, 240, 390 and 798 are not confirmed (p = 0.20, 0.19, 0.79).
  - 405 goes the same way (3 of 45 against 0 of 65) but has too few cases.
  - The 405 pattern is noted as a lead. No unused data remain to test it.
- **MO1k: not supported.** 898 discovery and 154 confirmation KP seals; two candidates (154 and 50 more often with icon 40). 154 has too few confirmation cases; 50 is not confirmed (p = 0.50).
- **CT15r: supported (robustness).** With CMH strata by site × length band, 740 closes seal texts more often than tablet texts (OR 5.7, p = 0.0010).
  - The length-2 band is empty: every two-sign text with 740 has a training string within edit distance 1 and is therefore not in the strict held-out set.
  - CT15 is not a length effect.
- **FACE4: supported.** 38 ICIT objects with three faces (Harappa 34; `TAB:I` 30, `TAB:B` 8). Exactly one face closes on 30, against 17.0 expected (p = 0.0001). The closing-face counts are 0 on 6 objects, 2 on 1 and 3 on 1.
  - Several three-face tablets combine a text face with one or two numeral faces (`176 740 400 / 033 700 / 033 700`).
  - As for two faces (FACE1), the faces of one object carry one closed text.

The survey of the `cult` codes and `Bull1` suffixes found no definition; see `docs/OBJECT_CODES.md`.

### R7 recomputed (45 tests)

The confirmation tests of SZ2 (3), MO2b (3) and MO1k (1) were added to the family, which now has 45 tests (MO2a and T2 had no candidates).
- Holm at α = 0.01 keeps 13 tests: the F3 direction test, H3.3 (ICIT), H3.10 (both transcriptions), H3.12a (ICIT), H3.12b (both), B1, B4, CT17 (both) and CT18 (both).
- F2 (p = 0.00037) and H9.4 class 4 × copper tablets (p = 0.00039) no longer survive Holm at α = 0.01. Both still survive Holm at α = 0.05. The statement of the previous session that H9.4 survives even Holm at 0.01 is therefore withdrawn for the larger family.
- Holm at α = 0.05 keeps 24 tests, including CT15, F5, CT22, H6.1 and G2. Benjamini–Hochberg at q = 0.01 keeps 24.
- The count–item pairing is still covered at α = 0.01 by the strict held-out tests H3.10 and H3.12.

### Pre-registration of AR1, AR1h (before running)

**AR1 (rare signs cluster within a site).** If rare signs were local (for example parts of names, or signs of a local group of users), seals sharing a rare sign should come from the same part of the site more often than chance.
- Data: Mohenjo-daro seal objects (`SEAL…` types), text as in SZ2 (complete, no `?`).
- Main area: the letters of `area-section` before the first non-letter (DKG., DK-, DKC → "DK"; HRB, HR- → "HR"; VSA → "VS"). Objects whose area has no letters are excluded.
- Rare sign: a sign occurring in 2 to 5 of these objects. Pairs: all pairs of objects sharing at least one rare sign.
- Statistic: share of these pairs whose objects have the same main area.
- Null: the area labels are permuted among the objects; 10,000 draws.
- Prediction: the real share is higher, one-sided p < 0.01.
- Insufficient data: fewer than 30 pairs.
- Limitation stated in advance: the main areas were excavated and published by different excavators. Clustering could also come from differences in how signs were drawn or recorded, not from use.

**AR1h (Harappa).** The same for Harappa seal objects, with the main area as the first letter group of `area-section` (AB-, F-, FTrench … → "AB", "F", "FTrench"; '--' excluded).

### Result AR1, AR1h: not supported

Script: `scripts/batch6b_ar1_areas.py`; results: `results/batch6b_ar1_areas.json`.

**Error in the registration.** The registered rule for the main area (the letters before the first non-letter) gives "DKG" for `DKG.`, while the registered examples give "DK". The registration therefore did not fix the grouping uniquely. Both readings were run, and AR1 was to count as supported only if both passed.

Results:
- Mohenjo-daro, by the rule: 936 seals, 150 rare signs, 461 pairs. 35.1 % of the pairs come from the same area, against 28.8 % under permutation (p = 0.019).
- Mohenjo-daro, by the examples (DK, HR, VS, SD …): 68.8 % against 62.4 % (p = 0.032).
- Harappa (AR1h): 216 seals, 224 pairs. 19.2 % against 21.6 % (p = 0.79).

In neither reading and at neither site do seals sharing a rare sign come from the same area significantly more often. At Mohenjo-daro the direction is positive but weak, and it is open to the recording confound stated in advance.

From now on, a registered rule takes precedence over its examples. The examples are checked against the rule before registration.

### End of the twenty-fifth session

- Pre-registered analyses:
  - Supported: CT15r (robustness), FACE4.
  - Not supported: MO2a, MO2b, MO1k, AR1, AR1h.
- R7 was recomputed with 45 tests. `scripts/run_all.py` now runs R7 last, because it reads the results of later scripts.
- No new external variable (iconographic detail, object size, chronological level, excavation area) is predicted by the signs on unused data.
- The functional L2 result (CT15) holds and is not a length effect.

---

## 2026-11-25 (day 1, twenty-sixth working session, 18:18 UTC): replications in KP1979 and the numeral faces

### Plan of the run

1. CT22k: replication of CT22 (fish-shaped signs form a usage class) in KP1979.
2. F5k: formulae learned from KP1979 training data recur in the post-1979 finds (independent discovery transcription).
3. FACE4k: replication of FACE4 (objects with three or more faces) in KP1979.
4. FACE5: do the counts on numeral faces differ between moulded (`TAB:B`) and incised (`TAB:I`) tablets?
5. NUM3 (descriptive): sign 700 inside one-face texts, compared with the numeral faces.
6. Interim report 5; README, claims, final report; reproducibility.

### Pre-registrations (before running)

**CT22k.**
- Fish set in KP1979: the best concordance matches of the ICIT fish-shaped signs, {53, 56, 57, 58, 60, 61, 62, 63} (`results/phase1_concordance.tsv`).
- Data: KP strict held-out strings, normalised as in R4.
- Members with at least 5 occurrences are used. The statistic, null (10,000 frequency-matched random sets) and decision (one-sided p < 0.01) are as in CT22.
- Insufficient data: fewer than 3 members with at least 5 occurrences.

**F5k.**
- Formula templates of length ≥ 3 with at least three fillers are found on KP1979 training strings (normalised as in R4; not `is_heldout`).
- The fresh ICIT strings of length ≥ 3 are mapped sign by sign to KP through the concordance (best match, then normalised). Strings with an unmappable sign are dropped.
- Statistic: number of mapped fresh strings that fit a template.
- Control: rule-preserving ICIT controls of each fresh string (`indus.controls.control`), mapped in the same way; 10,000 draws.
- Prediction: one-sided p < 0.01. Insufficient data: fewer than 5 real matches.

**FACE4k.**
- KP objects with three or more records, all complete without `?` (any `lines_code`).
- The KP terminal set is used. The statistic, null and decision are as in FACE4.
- Insufficient data: fewer than 20 objects.

**FACE5.**
- Unit: distinct text faces among the ICIT numeral tablets of FACE2. Each unit takes its type (`TAB:B` or `TAB:I`; units with both are dropped) and the count of its most frequent numeral face (032 = 2, 033 = 3, 034 = 4; ties dropped).
- Question: does the count distribution differ between moulded and incised tablets? This is an external, physical variable (the technique of manufacture).
- Statistic: χ² of the 2 × 3 table. Null: 10,000 permutations of the type labels among units.
- Prediction: p < 0.01. Insufficient data: fewer than 10 units of either type.

**NUM3 (descriptive).** In one-face ICIT texts (objects with a single face), count the signs that precede 700 and the counts of stroke signs before it. Compare with the numeral faces (2–4 strokes only).

### Results CT22k, F5k, FACE4k, FACE5, NUM3

Script: `scripts/batch7_kp_replications.py`; results: `results/batch7_kp_replications.json`.

- **CT22k: supported (replication).**
  - In the KP strict held-out strings, four fish-shaped signs have at least 5 occurrences (56, 58, 60, 62).
  - Their mean pairwise context similarity is 0.265, against 0.104 (SD 0.030) for frequency-matched sets (p = 0.0007).
  - The fish-shaped signs form one usage class in both transcriptions.
- **F5k: supported.**
  - 46 formula templates were found on 1,657 KP1979 training strings. Of 70 fresh ICIT strings that map to KP, 10 fit a KP template, against 4.7 for rule-preserving controls (p = 0.0003).
  - Formulae found in the 1979 transcription recur in finds made after 1979. The matches largely overlap those of F5 (for example `861 002 016 390`, `920 740 400`).
- **FACE4k: not supported.**
  - 28 KP objects have three or more complete records. Exactly one record closes on 14, against 12.4 expected (p = 0.33). The closing counts are 0 on 8 objects, 2 on 4 and 3 on 2.
  - The KP objects mix several `lines_code` values (7: 15, 6: 5, 3: 3, and others) whose meanings are not known. Some may be separate inscriptions rather than faces of one object.
  - The ICIT result (FACE4) is therefore not replicated. The disagreement may come from how the two sources group records into objects, but this was not tested.
- **FACE5: not supported.** 144 distinct text faces (moulded 85, incised 59). Counts 2/3/4: moulded 30/34/21, incised 18/17/24 (χ² = 4.3, p = 0.12). The count on the numeral face does not differ between moulded and incised tablets.
- **NUM3 (descriptive).** In one-face texts, sign 700 occurs only 17 times. 11 of these follow a stroke sign (033: 4, 004: 4, 034: 2, 003: 1). Sign 700 is therefore almost confined to the numeral faces and to numeral contexts. On the numeral faces themselves it follows only 2–4 strokes (FACE2).

R7 recomputed with CT22k and F5k (47 tests). Holm at α = 0.01 keeps the same 13 tests. CT22k and F5k survive Holm at α = 0.05, as do CT15, F5 and CT22.

### Pre-registration of D7 (before running)

**D7 (combinatorial sparsity across reference systems; typology).** CT27 found that frequent Indus signs combine less freely than the graphemes of syllabic Akkadian letters. D7 asks where the Indus value lies among all reference corpora.
- Statistic: the CT27 density, the share of the 50 × 50 ordered pairs of the 50 most frequent signs that occur as adjacent pairs, in a sample of about 9,000 tokens of unique lines.
- Corpora:
  - Indus: ICIT and KP1979 (normalised).
  - The CDLI reference corpora: proto-Elamite, proto-cuneiform, Ur III administrative Sumerian, OB literary Sumerian, OB Akkadian letters and Old Assyrian letters, where available in `indus.reference`.
  - Sproat (2014) corpora with at least 9,000 tokens (descriptive only).
- 20 resamples per corpus.
- Prediction (from the D1 placement): in at least 19 of 20 resamples, the CDLI corpus whose density is nearest to the Indus value is proto-Elamite or proto-cuneiform, for each transcription separately.

### Result D7: not supported (transcription-dependent)

Script: `scripts/batch7b_d7_sparsity.py`; results: `results/batch7b_d7_sparsity.json`.

Mean density (20 resamples of about 9,000 tokens):

| Corpus | Density |
|---|---:|
| Sproat weather icons | 0.057 |
| Sumerian Ur III administrative | 0.242 |
| proto-Elamite | 0.266 |
| proto-cuneiform | 0.268 |
| Indus (ICIT) | 0.283 |
| Indus (KP1979, normalised) | 0.331 |
| Sumerian OB literary | 0.357 |
| Akkadian OB letters | 0.402 |
| Sproat Asian emoticons | 0.407 |

- For ICIT, the nearest CDLI corpus is proto-cuneiform (14 resamples) or proto-Elamite (6); the prediction holds.
- For KP1979, the nearest is OB literary Sumerian in all 20 resamples; the prediction fails. D7 is therefore not supported.
- KP1979 writes more distinctions as separate signs than the ICIT source. Its frequent signs then combine more freely, and its density falls between the proto-administrative corpora and the literary corpus.
- The administrative corpora are sparser than the literary and letter corpora. A non-linguistic system lies at each end (weather icons very sparse, emoticons dense).
- The density measure therefore depends on the transcription, as the repetition measure did. It does not separate writing from non-writing.

### End of the twenty-sixth session

- Pre-registered analyses:
  - Supported: CT22k, F5k.
  - Not supported: FACE4k, FACE5, D7.
  - Descriptive: NUM3.
- The new scripts were re-run without changes in their results.
- Interim report 5 was written.
- The level assessment is unchanged.

---

## 2026-11-25 (day 1, twenty-seventh working session, 19:18 UTC): direction variants, sites, numeral partners

### Plan of the run

1. DIR1: do the 216 lines recorded as written left to right (`L/R`) follow the same order as the right-to-left lines, once normalised? This checks the direction normalisation of the first session.
2. SX1: leave-one-site-out. Do order regularities learned at the other sites predict each main site, in the reading direction only?
3. SX2: do Harappa and Mohenjo-daro seal legends differ in sign use beyond chance?
4. D6: how specific is the partner of a numeral in the Indus texts, compared with proto-Elamite and proto-cuneiform? (descriptive, with a decision rule)
5. R7 update; README, claims, reports; reproducibility.

### Pre-registrations (before running)

**DIR1.**
- Model: a bigram model with add-0.1 smoothing over the ICIT vocabulary, trained on unique complete `R/L` strings in reading order. Strings that also occur as `L/R` lines are excluded.
- Test: unique complete `L/R` strings of length ≥ 2, in reading order (`indus.corpus`, i.e. after the normalisation).
- Statistic: number of strings with a lower mean log-loss forward than reversed.
- Prediction: forward wins more often, sign test one-sided p < 0.01.
- If the normalisation were wrong for `L/R` lines, the reversed order would win.

**SX1.** For each site with at least 150 unique complete strings (expected: Harappa, Mohenjo-daro, and possibly Lothal, Kalibangan, Chanhu-daro, Dholavira):
- train the same bigram model on the strings of all other sites (strings occurring at the held-out site are excluded);
- on the held-out site's strings, count forward wins over reversed.
- Prediction: forward wins at every such site, sign test one-sided p < 0.01 at each (Bonferroni over sites: 0.01/m).

**SX2.**
- Data: `SEAL:S` legends from Harappa and Mohenjo-daro (unique strings per site; strings found at both sites are dropped).
- Statistic: Jensen–Shannon divergence between the sign-frequency distributions of the two sites, restricted to signs with at least 10 occurrences in the pooled data.
- Null: site labels permuted among strings; 10,000 draws.
- Prediction: the real divergence is larger, one-sided p < 0.01.
- Descriptive: the signs that contribute most.

**D6 (descriptive comparison).**
- A numeral token is paired with its partner: in the Indus texts (ICIT) the next sign after a stroke sign; in proto-Elamite the sign before the numeral group; in proto-cuneiform the sign after the numeral group. Numeral tokens are reduced to their unit: Indus stroke sign as is; CDLI `n(Nxx)` → `Nxx`.
- Statistic: Theil's uncertainty coefficient U(partner | numeral unit), on 20 resamples of 300 pairs per corpus.
- Decision rule stated in advance: the Indus value is called "within the proto-administrative range" if its mean lies between the two proto means, ± 2 resample SDs.

### Results DIR1, SX1, SX2, D6

Script: `scripts/batch8_direction_sites.py`; results: `results/batch8_direction_sites.json`.

- **DIR1: supported.**
  - Of 122 unique `L/R` strings (mostly Harappa tablets: `TAB:B` 54, `TAB:I` 48; seals 36), 105 have a lower log-loss forward than reversed under a model trained on `R/L` strings (p < 10⁻¹⁶).
  - Once normalised, the lines written left to right follow the same order as the others. This confirms the direction normalisation of the first session: the direction of writing varies, but the order of the text is the same.
- **SX1: supported.**
  - Only Harappa and Mohenjo-daro have at least 150 unique strings. A model trained on the other sites reads the held-out site forward better than reversed in 626 of 687 strings (Harappa) and 1,030 of 1,090 (Mohenjo-daro); both p < 10⁻¹⁰⁰.
  - The sequential regularities are shared across the two main sites.
- **SX2: not supported.**
  - 179 Harappa and 801 Mohenjo-daro square-seal legends (strings shared by both sites removed), 77 signs. The Jensen–Shannon divergence is 0.030, against 0.025 under permutation (p = 0.14).
  - The sign use of seal legends at the two main sites does not differ detectably.
  - Descriptive: the largest contributions come from 405 (Harappa 12, Mohenjo-daro 9 occurrences) and from 923, 226 and 705, which are more frequent at Mohenjo-daro.
- **D6 (descriptive): "outside the proto-administrative range".**
  - U(partner | numeral) is 0.34 (SD 0.011) for the Indus texts, against 0.20 (proto-Elamite) and 0.18 (proto-cuneiform).
  - The partner of an Indus numeral depends more on the numeral than in either proto-administrative system.
  - Limitation: the Indus numeral "unit" is the count sign itself (each count is its own sign), whereas the CDLI unit was reduced to the unit sign without its count. The comparison therefore measures count-specific partners in the Indus texts (H3.10, H3.12) against unit-specific partners in the proto-administrative texts. The two are not strictly equivalent.

**D6b (post hoc, descriptive) and correction of D6.**
- With the CDLI numerals kept with their counts (for example `3(N01)`), U(partner | numeral) is 0.40 (proto-Elamite) and 0.36 (proto-cuneiform), against 0.34 for the Indus texts.
- The numeral vocabularies differ greatly: 11 Indus stroke signs, 99 and 207 CDLI numeral tokens. With 300 pairs per resample, U rises with the number of categories, so neither version is a fair comparison.
- The D6 statement that Indus numeral partners are more specific than those of the proto-administrative systems is therefore withdrawn. The comparison is recorded as inconclusive.

### Pre-registration of DIR2 (before running)

**DIR2.** Most analyses exclude the 1,228 ICIT lines whose direction is recorded as unknown. DIR2 asks whether these lines, in the normalised order, follow the same order as the others, so that they could be used in later work.
- Model: as in DIR1, trained on unique complete `R/L` and `L/R` strings, excluding strings that also occur with unknown direction.
- Test: unique complete unknown-direction strings of length ≥ 2.
- Prediction: forward wins, sign test one-sided p < 0.01.

### Result DIR2: supported (weakly)

Script: `scripts/batch8b_dir2_unknown.py`; results: `results/batch8b_dir2_unknown.json`.
- Only 139 unique complete strings of length ≥ 2 have unknown direction. Most unknown-direction lines are fragments or single signs, and pottery graffiti and seals are the most frequent types.
- Forward wins in 84 of the 127 strings without a tie (66 %; p = 0.0002).
- The unknown-direction lines follow the normalised order more often than not. The margin is smaller than for `R/L` or `L/R` lines (DIR1: 86 %, SX1: 91–95 %).
- They could be included in later analyses in the normalised order, but with less certainty about their direction.

### End of the twenty-seventh session

- Pre-registered analyses:
  - Supported: DIR1, SX1, DIR2.
  - Not supported: SX2.
  - Inconclusive: D6 (descriptive), with the post-hoc check D6b.
- The new scripts reproduce their results.
- None of these analyses used the strict held-out or fresh data, so the R7 family is unchanged (47).

---

## 2026-11-25 (day 1, twenty-eighth working session, 20:18 UTC): generalisation across object classes; typology with a seventh statistic

### Plan of the run

1. PT1: do the positional template (B1-type) and the recurring units (B4-type) learned from seals and tablets carry over to pottery inscriptions?
2. PT2: the same for the other inscribed objects (bangles, implements, tags, miscellaneous).
3. D2b: does adding the combinatorial density (CT27) as a seventh statistic let the D2 method separate writing from non-linguistic systems?
4. R9: full reproducibility run.
5. Updates of ledger, README, claims, reports.

### Pre-registrations (before running)

**PT1 and PT2.**
- Training: all unique complete ICIT strings (length ≥ 2, no `?`) from objects of types `SEAL…` and `TAB…`.
- Test:
  - PT1: unique strings from pottery (`POT…`).
  - PT2: unique strings from all other types.
  - Test strings that also occur on seals or tablets are removed from the test set, not from training.
- Primary test set: lines of known direction. Secondary (descriptive): including unknown-direction lines (DIR2).
- Zones and units are defined on the training strings with the B1 and B4 rules: zone by initial share ≥ 0.5 or final share ≥ 0.5 among signs with ≥ 10 occurrences; units are 2–3-grams in ≥ 5 training lines, excluding built-in pairs.
- Statistics: inversions (fewer is better) and covered positions (more is better).
- Controls: ICIT rule-preserving controls, 10,000 draws.
- Prediction: for each class, B1-type p < 0.01 and B4-type p < 0.01 (one-sided).
- Insufficient data: fewer than 20 test strings with at least two zoned signs.

**D2b.**
- The D2 design (300-line samples, 20 resamples, leave-one-corpus-out over the seven known corpora: three full-writing, four non-linguistic), with a seventh statistic S7: the share of the 20 × 20 ordered pairs of the 20 most frequent signs of the sample that occur adjacent in it.
- Decision: the statistics separate writing from non-writing if all seven known corpora are classified correctly. Only then is the Indus assignment interpreted.

### Results PT1, PT2, D2b

Scripts: `scripts/batch9_object_classes.py`, `scripts/batch9b_d2b_density.py`; results: `results/batch9_object_classes.json`, `results/batch9b_d2b_density.json`.

- **PT1 (pottery): partly supported.**
  - Primary set: 54 strings of known direction, 36 with two zoned signs.
  - Units learned from seals and tablets cover 16 positions, against 9.2 for controls (p = 0.0007).
  - The positional template is not shown: 6 inversions, against 8.0 for controls (p = 0.26). The test has little power, because pottery inscriptions are short and the controls also produce few inversions.
  - With the unknown-direction lines (93 strings) the result is the same: units p = 0.0004, template p = 0.26.
  - The pottery inscriptions share the recurring units of the seals and tablets. Whether they follow the same positional template cannot be decided with these data.
- **PT2 (other objects: tags, bangles, rods, implements, miscellaneous): supported.**
  - 67 strings of known direction. 13 inversions, against 29.5 for controls (p = 0.0005); 67 covered positions, against 32.1 (p = 0.0001).
  - With unknown-direction lines (96 strings): p = 0.0014 and 0.0001.
  - The template and the units learned from seals and tablets carry over to every other kind of inscribed object.
- **D2b: not supported.**
  - With the seventh statistic, leave-one-out again classifies 5 of 7 known corpora correctly; totem poles and Asian emoticons are again classed as writing.
  - The seven statistics still do not separate writing from non-linguistic systems. Gate G3 remains undecided.
  - The Indus samples are assigned to "linguistic" in 20 of 20 resamples. As in D2, this is not interpreted, because the method fails on known corpora.

### Pre-registration of PT3 (before running)

**PT3 (count–item pairing on objects other than seals and tablets).**
- Data: unique complete ICIT strings (no `?`) from pottery and other non-seal, non-tablet objects (as in PT1 + PT2, any direction).
- Statistic: Fisher exact test, one-sided. It compares the share of bigrams whose second sign is in {390, 405, 406, 407} after a 4–9-stroke sign {004, 034, 005, 016, 017} with that after any other sign.
- Prediction: p < 0.01. Insufficient data: fewer than 5 bigrams after the stroke set.
- Data note: the H3.10 rule was found on training strings of all object types. Some of these strings may have been among them, so this is a test of the rule on an object class, not on unused data.

### Result PT3: supported

Script: `scripts/batch9c_pt3_count_pairs.py`; results: `results/batch9c_pt3_count_pairs.json`.
- On 217 strings from pottery and other objects, 7 of 26 bigrams after a 4–9-stroke sign end in 390–407, against 13 of 422 after other signs (OR 11.6, p = 0.00004).
- The count–item pairing is not confined to seals and tablets.

### End of the twenty-eighth session

- Pre-registered analyses:
  - Supported: PT2, PT3.
  - Partly supported: PT1 (units yes, template undecided).
  - Not supported: D2b.
- The L1 structure (template, units, count–item pairing) holds on every class of inscribed object. Gate G3 (writing or not) remains undecided.

### Reproducibility check (R9)

`scripts/run_all.py --skip-heavy` re-ran every analysis in the repository, including all those added since R8, with no failures and no changed result files.

---

## 2026-11-25 (day 1, twenty-ninth working session, 21:18 UTC): replications in KP1979 and rare signs by object class

### Plan of the run

1. PT2k, PT3k: replication of PT2 (template and units on other objects) and PT3 (count–item pairing on other objects) in KP1979.
2. CT28h, CT28hk: do seal legends contain more rare signs than tablet texts? This is a further prediction of the individual-legend reading of CT28 (claim C28).
3. Updates; reproducibility of the new scripts.

### Pre-registrations (before running)

**PT2k.**
- Training: unique complete KP strings (normalised as in R4; length ≥ 2; no `?`) with type codes {11, 23, 62, 67, 72, 75}. These are the seal and tablet codes used in C2k, CT28k and CT32k.
- Test: unique strings with any type code whose first digit is not 1, 2, 6 or 7. The assumption that the 1x/2x codes are seals and the 6x/7x codes tablets is inferred from the data, not sourced. Test strings also found in training are dropped.
- Statistics, KP rule-preserving controls (10,000 draws), decision and insufficient-data rule as in PT2.

**PT3k.**
- Data: the PT2k test strings.
- Fisher exact test, one-sided: the share of bigrams ending in 86 after the 4–9-stroke signs {124–129} is compared with that after other signs.
- Prediction: p < 0.01. Insufficient data: fewer than 5 bigrams after the stroke set.

**CT28h (ICIT).**
- Data: Harappa and Mohenjo-daro; unique strings per site and object class, seal (`SEAL…`) or tablet (`TAB…`). Strings found in both classes at a site are dropped.
- Stem: the string without its terminal cluster (ICIT terminal set, maximal final run).
- Rare sign: a sign occurring in at most 3 unique complete ICIT strings overall.
- Statistic: the sum over the two sites of (share of rare tokens among seal stem tokens − the same share for tablet stems).
- Null: class labels permuted among the strings of each site; 10,000 draws.
- Prediction: seals have more rare signs, one-sided p < 0.01.

**CT28hk (KP1979).** The same with KP codes {11, 23} vs {62, 67, 72, 75}, without site strata (KP has no site field in this source), the KP terminal set, and rarity counted on KP unique strings.

### Results PT2k, PT3k, CT28h, CT28hk

Script: `scripts/batch10_kp_classes_rare.py`; results: `results/batch10_kp_classes_rare.json`.

- **PT2k: supported (replication).**
  - 184 KP test strings from other object codes (mostly 51, 91, 81 and 52), 167 of them with two zoned signs.
  - 75 inversions, against 124.7 for controls (p = 0.0001); 197 covered positions, against 93.9 (p = 0.0001).
  - Note: the KP rule-preserving controls were applied to normalised strings, in which the long-stroke pair 147 → 217 appears as 123 → 217 and is not kept as a unit. This makes the controls slightly less strict for that pair.
- **PT3k: supported (replication).** After the 4–9-stroke signs, 5 of 23 bigrams end in 86, against 24 of 545 after other signs (OR 6.0, p = 0.0043).
- **CT28h: not supported.**
  - Harappa 256 seal and 421 tablet strings; Mohenjo-daro 988 and 120. The share of rare signs in seal stems is not higher than in tablet stems: the summed difference is −0.021 (p = 0.87).
- **CT28hk: not supported.**
  - 1,328 seal and 334 tablet strings; difference +0.006 (p = 0.11).
- CT28 found seal stems more diverse than tablet stems. They are not built from rarer signs, so their individuality lies in the combination of common signs, not in a special stock of rare signs. A reading in which seal legends contain names written with special rare signs would have predicted the opposite. The test does not decide claim C28 either way.

### End of the twenty-ninth session

- Pre-registered analyses:
  - Supported: PT2k and PT3k (replications).
  - Not supported: CT28h, CT28hk.
- The script reproduces its results on re-run.
- The level assessment is unchanged.

---

## 2026-11-25 (day 1, thirtieth working session, 22:18 UTC): typology of order and frequency; consistency review

### Plan of the run

1. D8: order rigidity of sign pairs, compared with the reference corpora.
2. D9: positional rigidity of signs, compared with the reference corpora.
3. D10: shape of the rank–frequency distribution, compared with the reference corpora.
4. R10: consistency review of README, claims evaluation and final report against the ledger and the result files.
5. Interim report 6.

### Pre-registrations (before running)

Common design:
- 20 resamples of about 9,000 tokens of unique lines, as in CT27 and D7.
- Corpora: ICIT; KP1979 (normalised); the five CDLI corpora; the Sproat corpora with at least 9,000 tokens (weather icons, Asian emoticons; descriptive only).
- The predictions concern the CDLI corpora. They are stated for each Indus transcription separately, and a prediction holds only if it holds in at least 19 of 20 resamples for both transcriptions.

**D8 (order rigidity).**
- Statistic: among ordered pairs of different signs (a, b) that occur adjacent at least 3 times in the sample, the share whose reverse (b, a) never occurs adjacent.
- Prediction: the Indus value is higher than that of each of the three full-writing CDLI corpora (Ur III administrative, OB literary, OB letters).

**D9 (positional rigidity).**
- Statistic: for the 50 most frequent signs, the mean share of their occurrences (in lines of length ≥ 3) that fall in their modal position class (initial / medial / final).
- Prediction: the Indus value is higher than that of each full-writing CDLI corpus.

**D10 (rank–frequency shape).**
- Statistic: the slope of log frequency against log rank for ranks 1–50 (least squares).
- Prediction: none on direction. The decision rule is that the Indus slope is called "like the proto-administrative corpora" if it lies within the range of proto-Elamite and proto-cuneiform (± 2 resample SDs), for both transcriptions.

### Results D8, D9, D10

Script: `scripts/batch11_typology_order.py`; results: `results/batch11_typology_order.json`.

| Corpus | D8 order rigidity | D9 positional rigidity | D10 rank–frequency slope |
|---|---:|---:|---:|
| Indus (ICIT) | 0.726 | 0.757 | −0.70 |
| Indus (KP1979) | 0.649 | 0.740 | −0.74 |
| proto-Elamite | 0.871 | 0.717 | −0.75 |
| proto-cuneiform | 0.842 | 0.640 | −0.66 |
| Sumerian Ur III administrative | 0.857 | 0.734 | −0.46 |
| Sumerian OB literary | 0.674 | 0.835 | −0.56 |
| Akkadian OB letters | 0.596 | 0.778 | −0.65 |
| Sproat Asian emoticons | 0.287 | 0.902 | −1.11 |
| Sproat weather icons | 0.006 | 0.652 | −1.91 |

- **D8: not supported.** The Indus order rigidity is not higher than that of every full-writing corpus. It lies between the letters and literary texts (0.60–0.67) and the administrative corpora (0.84–0.87, including Ur III administrative Sumerian). The administrative corpora, with their fixed entry formats, are the most rigid.
- **D9: not supported.** The positional rigidity of the Indus signs (0.74–0.76) lies inside the range of the full-writing corpora (0.73–0.84). The fixed positions found in B1 and Q2a are therefore not unusual by this measure.
- **D10: "like the proto-administrative corpora" by the stated rule.** The Indus slopes (−0.70, −0.74) lie within the proto-Elamite/proto-cuneiform range (−0.76 to −0.63). The OB letters (−0.65) also fall in that range, so the measure does not single out the proto-administrative group.
- In these measures the Indus corpus behaves like an ordinary member of the reference group, not like either extreme. None of the three separates writing from non-writing, because the two non-linguistic corpora lie at opposite ends on D8 and D10.

### Pre-registration of CT15b (before running)

**CT15b (stability of the CT15 effect size).**
- Data: the CT15 data (strict held-out + fresh strings containing 740, one object class, site strata).
- Method: 10,000 stratified bootstrap resamples, drawing strings with replacement within each site stratum. The Mantel–Haenszel odds ratio is computed for each resample; a resample whose denominator is zero gives an infinite odds ratio, which is counted as > 1.
- Prediction: the 2.5th percentile of the bootstrap distribution is above 1.

### Result CT15b: supported

Script: `scripts/batch11b_ct15b_bootstrap.py`; results: `results/batch11b_ct15b_bootstrap.json`.
- Mantel–Haenszel odds ratio 4.33 (as in CT15); bootstrap median 4.55; 95 % interval 1.49–16.0.
- 0.5 % of the resamples give an odds ratio ≤ 1, and 0.01 % give an infinite one.
- The effect is positive in the large majority of resamples. Its size is uncertain: it lies anywhere between about 1.5 and 16.

### Consistency review (R10)

- Every test label cited in `README.md`, `reports/FINAL_REPORT.md` and `docs/CLAIMS_EVALUATION.md` has a row in `docs/DATA_LEDGER.md`. This was checked by script: the labels found in the three files were compared with the ledger's first column, and none was missing.
- The figures quoted for the main results (CT15, CT15r, CT15b, F5, F5k, CT22, CT22k, R7) were compared with the result files and agree.

### End of the thirtieth session

- Pre-registered analyses:
  - Supported: CT15b (robustness).
  - Not supported: D8, D9.
  - Descriptive: D10.
- Review: R10. The level assessment is unchanged.

---

## 2026-11-25 (day 1, thirty-first working session, 23:18 UTC): robustness across sites and object classes

### Plan of the run

1. SX3: leave-one-site-out test of the positional template (B1 type).
2. SX4: leave-one-site-out test of the recurring units (B4 type).
3. H3.3c: the fixed order inside the closing cluster, within each object class.
4. CT22b: stability of the CT22 result (fish-shaped signs as a usage class) under resampling of strings.
5. Updates; reproducibility.

### Pre-registrations (before running)

**SX3 and SX4.**
- For Harappa and for Mohenjo-daro in turn, zones and units are learned with the PT1 rules on unique complete ICIT strings (known direction, no `?`, length ≥ 2) of all other sites. Strings found at the test site are removed from training.
- They are tested on the unique strings of the test site with ICIT rule-preserving controls (10,000 draws).
- SX3 statistic: inversions. SX4 statistic: covered positions.
- Prediction: p < 0.005 at each site (Bonferroni over the two sites).

**H3.3c.**
- For each object class (seals, tablets, other objects), unique complete ICIT strings of known direction.
- The dominant order of each adjacent pair of terminal-set signs is taken from H3.3's training result (`results/phase3_h33_heldout.json`). If it is not available there, it is recomputed on ICIT training strings of all classes (not `is_heldout`).
- In each class, the share of adjacent terminal pairs in the dominant order is tested with a binomial test against 0.5.
- Prediction: agreement ≥ 0.8 and p < 0.01 in each class with at least 10 such pairs. Classes with fewer than 10 pairs are "insufficient data".
- Data note: these strings include training strings, so this tests whether the fixed order holds within every class, not on unused data.

**CT22b.**
- The CT22 data (strict held-out + fresh ICIT strings).
- 1,000 bootstrap resamples of the strings (with replacement). In each, the CT22 statistic is computed: mean pairwise context similarity of the fish-shaped signs with ≥ 5 occurrences in the resample, minus the mean of 200 frequency-matched random sets.
- Prediction: the difference is positive in at least 99 % of resamples.

### Results SX3, SX4, H3.3c, CT22b

Script: `scripts/batch12_sites_classes.py`; results: `results/batch12_sites_classes.json`.

- **SX3: supported.** With zones learned at the other sites:
  - Harappa strings show 126 inversions, against 282.0 for controls (p = 0.0001).
  - Mohenjo-daro strings show 354, against 820.0 (p = 0.0001).
- **SX4: supported.** With units learned at the other sites:
  - Harappa: 650 covered positions, against 292.4 (p = 0.0001).
  - Mohenjo-daro: 1,164, against 426.5 (p = 0.0001).
- **H3.3c: supported.** The dominant order inside the closing cluster holds in every object class:
  - seals 79 of 90 (88 %, p < 10⁻¹³);
  - tablets 115 of 120 (96 %, p < 10⁻²⁷);
  - other objects 10 of 11 (91 %, p = 0.0059).
- **CT22b: supported.** In all 1,000 bootstrap resamples, the fish-shaped signs are more similar in context than frequency-matched sets. Median difference 0.060; 95 % interval 0.025–0.100.
- The positional template, the recurring units and the closing order do not depend on one site or one object class. The fish-sign class is stable under resampling.

### End of the thirty-first session

Pre-registered analyses SX3, SX4, H3.3c and CT22b are all supported (robustness). The level assessment is unchanged.

---

## 2026-11-26 (day 2, thirty-second working session, 00:18 UTC): structure within object classes

### Plan of the run

1. CT18c: nested structure (CT18) within seals and within tablets separately.
2. H3.10c: count–item pairing (H3.10) within seals and within tablets separately.
3. H3.3ck: closing-cluster order by object class in KP1979 (replication of H3.3c).
4. KF2: are formula frames shared between seal and tablet texts more or less often than chance?
5. Updates; reproducibility.

### Pre-registrations (before running)

**CT18c.**
- The CT18 procedure (PMI model from ICIT training strings; recursive splitting; parts compared with complete training texts) is applied to the strict held-out lines of length ≥ 4.
- The lines are split by object class: lines occurring only on seals, or only on tablets.
- Controls: 10,000 rule-preserving controls per class.
- Prediction: one-sided p < 0.005 in each class (Bonferroni over two classes).
- Insufficient data: fewer than 30 lines in a class.

**H3.10c.**
- ICIT unique complete strings occurring only on seals, or only on tablets.
- In each class, a one-sided Fisher test compares the share of bigrams ending in {390, 405, 406, 407} after the 4–9-stroke signs {004, 034, 005, 016, 017} with that after other signs.
- Prediction: p < 0.005 in each class.
- Insufficient data: fewer than 5 bigrams after the stroke set.
- Data note: these strings include training strings, so this checks the rule within classes, not on unused data.

**H3.3ck.**
- KP unique complete strings by class: seal codes {11, 23}, tablet codes {62, 67, 72, 75}, other codes.
- Dominant orders come from the KP training pairs of H3.3 (`results/phase3_h33_heldout.json`). Decision as in H3.3c.

**KF2.**
- ICIT formula frames as in `docs/FORMULAE.md`: frames with at least three fillers, computed on unique complete strings of seals and tablets only.
- A frame is shared if at least one of its filled strings occurs on a seal and at least one on a tablet.
- Statistic: number of shared frames.
- Null: the seal/tablet labels are permuted among the strings (strings on both classes are dropped first); 10,000 draws.
- Prediction: none on direction; two-sided p < 0.01.

### Results CT18c, H3.10c, H3.3ck, KF2

Script: `scripts/batch13_within_classes.py`; results: `results/batch13_within_classes.json`.

- **CT18c: supported.** Nested structure on the strict held-out lines:
  - Seals (159 lines): 21.1 % of recursive parts are complete texts, against 7.5 % for controls (p = 0.0001).
  - Tablets (37 lines): 19.0 % against 8.9 % (p = 0.0001).
- **H3.10c: supported.** The count–item pairing holds within each class:
  - seals: 45 of 111 bigrams after a 4–9-stroke sign end in 390–407, against 164 of 5,264 after other signs (OR 21.2);
  - tablets: 9 of 34 against 34 of 1,364 (OR 14.1);
  - both p < 10⁻⁶.
- **H3.3ck: supported (replication).** In KP1979 the dominant closing order holds for seal codes (46 of 53), tablet codes (50 of 52) and other codes (37 of 42). The "other" codes are a mixture whose meanings are not known.
- **KF2: difference found (fewer shared frames than chance).**
  - 98 formula frames on 1,870 strings (1,389 seal-only, 481 tablet-only). 53 frames are filled on both seals and tablets, against 67.1 under permutation of the class labels (two-sided p = 0.0038).
  - Seals and tablets use partly different formulae.
  - The tests used all strings, which were used before for other questions (C2, CT31c, H3.5). The result is therefore not an L2 confirmation on unused data. It agrees with the earlier findings that the closing sign (C2, CT15) and the stems (CT31c) differ between the classes.
- The core L1 results (nested structure, count–item pairing, closing order) hold within each object class.

### End of the thirty-second session

All four pre-registered analyses gave the predicted results. Three are robustness checks of L1 (CT18c, H3.10c, H3.3ck), and one is a descriptive difference between object classes (KF2). The level assessment is unchanged.

---

## 2026-11-26 (day 2, thirty-third working session, 01:18 UTC): replications in KP1979 and a confound check of CT28

### Plan of the run

1. CT28n: CT28 without numeral faces. In the ICIT-style source the numeral faces of Harappa tablets (for example `033 700`) are separate lines that repeat very often. They alone could make tablet texts look less diverse.
2. KF2k: replication of KF2 (formula frames shared between seals and tablets) in KP1979.
3. CT18ck: replication of CT18c (nested structure within each object class) in KP1979.
4. H3.10ck: replication of H3.10c (count–item pairing within each object class) in KP1979.
5. Updates; reproducibility.

### Pre-registrations (before running)

**CT28n.**
- The CT28 design (records at Harappa and Mohenjo-daro; stems without the terminal cluster; 1,000 subsamples of equal size per site), but excluding records whose text consists only of stroke signs, or of stroke signs followed by 700.
- Prediction: seal stems are more diverse in at least 99 % of subsamples.
- A failure would mean that CT28 was produced by the numeral faces.

**KF2k.**
- KP unique complete strings (normalised as in R4) occurring only with seal codes {11, 23} or only with tablet codes {62, 67, 72, 75}.
- Frames, statistic, null and decision as in KF2 (two-sided p < 0.01).
- If significant, the direction is reported.

**CT18ck.**
- The CT18 procedure in KP1979 (PMI from KP training strings; strict held-out lines of length ≥ 4), split by class (strings occurring only with seal codes, or only with tablet codes).
- 10,000 controls per class; one-sided p < 0.005 in each class.
- Insufficient data: fewer than 30 lines in a class.

**H3.10ck.**
- KP unique complete strings by class (seal codes, tablet codes).
- One-sided Fisher test of bigrams ending in 86 after {124–129} against other signs.
- Prediction: p < 0.005 in each class. Insufficient data: fewer than 5 bigrams after the stroke set.

### Results CT28n, KF2k, CT18ck, H3.10ck

Script: `scripts/batch14_ct28n_kp_classes.py`; results: `results/batch14_ct28n_kp_classes.json`.

- **CT28n: supported.** Excluding numeral-only records removes 313 Harappa tablet records and 5 seal records. Seal stems remain more diverse in 1,000 of 1,000 subsamples (mean difference 0.43, against 0.49 in CT28). CT28 is not produced by the numeral faces.
- **KF2k: not supported.**
  - 70 frames on 1,528 KP strings (1,274 seal-only, 254 tablet-only). 28 shared frames against 33.6 under permutation (two-sided p = 0.23). The direction agrees with KF2, but the difference is not significant.
  - The ICIT result KF2 is therefore not replicated. Fewer tablet strings and frames in KP1979 give the test less power.
- **CT18ck: insufficient data.** Seal-only strict held-out lines (158) show the nested structure (18.3 % against 6.0 %, p = 0.0001). Only 8 tablet-only lines remain.
- **H3.10ck: not supported.**
  - Seal codes: 33 of 93 bigrams after 124–129 end in 86, against 148 of 5,124 (OR 18.5, p < 10⁻²⁵).
  - Tablet codes: 3 of 16 against 26 of 886 (OR 7.6, p = 0.013), above the threshold 0.005. The direction agrees, but there are few cases.
- Consequences:
  - The class difference in formula sharing (KF2) is weakened. It holds in one transcription only.
  - The within-class robustness of L1 is shown for seals in both transcriptions. For tablets it is shown in ICIT (CT18c, H3.10c); in KP1979 there are too few tablet texts.

### End of the thirty-third session

- Supported: CT28n.
- Not supported: KF2k, H3.10ck (tablet part).
- Insufficient data: CT18ck (tablet part).
- The level assessment is unchanged.

---

## 2026-11-26 (day 2, thirty-fourth working session, 02:18 UTC): how much new data would a confirmation need?

The tests that the accessible data allow have largely been run. What remains open are L2 candidates and leads that cannot be decided without unused inscriptions: the C2 associations, H9.4, the MO2b lead (405 on unicorn seals of variant W) and the KP replication of CT15. This session estimates, by simulation, how many new inscriptions a confirmatory test of each would need. This is planning information for the final report and for future work; it is not a test of any hypothesis.

### Plan of the run

1. PW1: power for confirming the six C2 associations.
2. PW2: power for H9.4 (class 4 avoids copper tablets).
3. PW3: power for the MO2b lead (405 × Bull1:W).
4. PW4: power for a replication of CT15 (740 closes seal texts more often than tablet texts).
5. `docs/FUTURE_DATA.md`: the results as a list of data requirements.
6. Updates.

### Pre-registration (before running)

**Common design.**
- Effect sizes are taken from all ICIT unique complete strings, as presence rates p₁ (sign present, given the class value) and p₀ (sign present, otherwise) and the class share q. They are therefore optimistic: the associations were selected for their size (winner's curse).
- Each scenario is also simulated with the log odds ratio halved, keeping p₀.
- For N new inscriptions (N in 50, 100, 200, 400, 800, 1,600, 3,200, 6,400), 2,000 simulated datasets are drawn. Each inscription is in the class with probability q and contains the sign with probability p₁ or p₀.
- A one-sided Fisher test is applied at the threshold of the confirmatory family.
- Reported: the smallest N in the grid with power ≥ 0.8 for each scenario ("> 6,400" if none).

**PW1.** The six C2 associations (region Inter-Riverine × 400; SEAL:R × 806, 407, 154; SEAL:S × 400 (less), SEAL:S × 741), each at α = 0.01/6, among seals and tablets (subtype) or all strings (region).

**PW2.** Presence of any class 4 sign of H9.4 × TAB:C (less), α = 0.01, among strings with an object subtype.

**PW3.** 405 × `Bull1:W` among unicorn seals with a suffix code, α = 0.01. p₀ = 0 is replaced by (0 + 0.5)/(n + 1).

**PW4.** Among strings containing 740 on a seal or tablet: final position × seal vs tablet, α = 0.01. The rates are taken from the CT15 strata, pooled.

### Results PW1–PW4

Script: `scripts/batch15_power.py`; results: `results/batch15_power.json`.

| Scenario | p₁ | p₀ | class share | N for 80 % power (observed effect) | N (log odds halved) |
|---|---:|---:|---:|---:|---:|
| C2 Inter-Riverine × 400 | 0.205 | 0.049 | 0.34 | 400 | 1,600 |
| C2 SEAL:R × 806 | 0.163 | 0.025 | 0.11 | 800 | 6,400 |
| C2 SEAL:R × 407 | 0.110 | 0.014 | 0.11 | 800 | 6,400 |
| C2 SEAL:R × 154 | 0.081 | 0.009 | 0.11 | 1,600 | > 6,400 |
| C2 SEAL:S × 400 (less) | 0.042 | 0.198 | 0.62 | 400 | 800 |
| C2 SEAL:S × 741 | 0.106 | 0.029 | 0.62 | 800 | 6,400 |
| H9.4 class 4 × TAB:C (less) | 0.111 | 0.476 | 0.03 | 800 | 3,200 |
| MO2b 405 × Bull1:W | 0.060 | 0.001 | 0.44 | 400 (unicorn seals) | 6,400 |
| CT15 replication (strings with 740) | 0.787 | 0.545 | 0.74 | 400 | 800 |

- N counts new, distinct inscriptions of the relevant kind: seals and tablets for C2 and H9.4; unicorn seals with a variant code for MO2b; seal and tablet texts containing 740 for CT15.
- For comparison, the ten post-1979 sites used as fresh data provide 117 unique lines, and the whole ICIT-style source has 5,679 records.
- Even under the optimistic effect sizes, a confirmation of the L2 candidates needs several hundred to over a thousand new inscriptions of the right kinds. With the effect sizes halved (a likely correction for selection), it needs several thousand, more than the present corpus.
- This explains, in numbers, why the L2 candidates could not be confirmed and the narrow L2 result is not beyond doubt. It also gives the scale of new material that future work would need.

---

## 2026-11-26 (day 2, thirty-fifth working session, 03:18 UTC): positive controls for the phonetic method, in the languages proposed for the Indus script

The phonetic search (E3–E3d) failed on its positive controls, which were cuneiform texts hidden as ciphers. Those controls have a weakness: cuneiform sign values (for example `lugal`) are not all expressible in the method's value set (V, CV or C syllables), so even the true assignment cannot be represented. This session builds positive controls that the method can represent exactly: Sanskrit (Ṛgveda) and Old Tamil text, split into the method's syllable units and hidden as ciphers. These are also the two languages most often proposed for the Indus script.

### Plan of the run

1. E3e: the search on syllabic ciphers of Sanskrit and Old Tamil of Indus size (2,000 lines).
2. E3f: the same at 8,000 lines.
3. E3g: an oracle check. Under the true decipherment of each cipher, does the scoring measure favour the true language? If not, the measure cannot identify a language even with the right assignment.
4. E3h: the cuneiform ciphers of E3d at 16,000 lines (power curve beyond E3c).
5. Updates.

### Pre-registrations (before running)

**Cipher construction (E3e–E3g).**
- For Sanskrit and Old Tamil, the word lists of E3d are divided into blocks of 50 words and shuffled with seed 20261125, as in `phonetic.equalised`.
- The first blocks, up to 20,000 tokens, form the language model, exactly as in E3d. The following blocks are the cipher source, so model and cipher do not share text.
- Each word is split greedily into units of the value set: consonant + vowel → CV; a vowel → V; any other consonant → C.
- A line is two consecutive words of the cipher source, as a sequence of units. Lines of 2–10 units are kept, unique lines only, and N are sampled with seed 20261126.
- Each unit type is replaced by an arbitrary code, and the lines are split 80/20 into training and test, as in `phonetic.cipher_lines`.

**E3e (N = 2,000) and E3f (N = 8,000).**
- The E3b/E3d measure (Δ′ = gain under the fitted assignment minus gain on within-line reordered text), with the five E3d models (equalised Sanskrit, Tamil, Sumerian and Akkadian, and a pseudo-language).
- Decision: the method has power if each cipher ranks its true language first and that language is clearly ahead of every other (bootstrap p < 0.01, as in E3d).

**E3g (oracle).**
- For the E3e ciphers, the true assignment (each code mapped back to its unit) is scored with the same Δ′ measure under each model, in place of the fitted assignment.
- Prediction: the true language ranks first for both ciphers.
- If it does not, the measure itself cannot identify the language, whatever the search finds.

**E3h.**
- The E3d design with the two cuneiform ciphers at 16,000 lines, or as many unique lines as the corpus provides.
- Decision as in E3c.

### Result E3g (oracle): the measure identifies the language under the true assignment

Script: `scripts/batch16_phonetic_controls.py e3g`; results: `results/batch16_e3g.json`.
- Syllabic ciphers of 2,000 lines: 1,600 training and 400 test lines; 98 unit types (Sanskrit) and 65 (Tamil).
- With the true assignment, Δ′ is:
  - Sanskrit cipher: 0.727 under the Sanskrit model, against 0.081 at most for any other.
  - Tamil cipher: 0.818 under the Tamil model, against 0.117 at most.
- Both true languages are clearly ahead.
- The scoring measure can therefore identify the language once the right assignment is known. Any failure of the search (E3e) lies in finding the assignment, not in scoring it.

### Result E3e: the search has no power at 2,000 lines

Script: `scripts/batch16_phonetic_controls.py e3e`; results: `results/batch16_e3e.json`.
- Sanskrit cipher: Δ′ is 0.282 under the Sanskrit model, against 0.163 at most for any other. The true language is first and clearly ahead.
- Tamil cipher: Δ′ is 0.330 under the Sanskrit model and 0.215 under the Tamil model. The wrong language is first and clearly ahead.
- By the registered rule, the method has no power: a fitted assignment for Old Tamil text is better explained by the Sanskrit model than by the Tamil model.
- Together with E3g, the failure lies in the search. With the true assignment, the Tamil model wins by a wide margin (0.818 against 0.070). With assignments found by the search, the Sanskrit model wins.
- The Sanskrit model appears to fit any assignment the search finds better than the other models do. A search result favouring Sanskrit for the Indus signs would therefore mean nothing.

### Results E3f, E3h: no power at 8,000 and 16,000 lines either

Script: `scripts/batch16_phonetic_controls.py e3f`, `... e3h`; results: `results/batch16_e3f.json`, `results/batch16_e3h.json`.

| Cipher | Lines | Sanskrit | Tamil | Sumerian | Akkadian | Pseudo | First | True |
|---|---:|---:|---:|---:|---:|---:|---|---|
| Sanskrit (E3f) | 8,000 | 0.295 | 0.168 | 0.115 | 0.099 | 0.000 | Sanskrit | Sanskrit |
| Old Tamil (E3f) | 8,000 | 0.333 | 0.156 | 0.102 | 0.150 | −0.004 | Sanskrit | Tamil |
| Akkadian letters (E3h) | 16,000 | 0.258 | 0.193 | 0.137 | 0.137 | 0.019 | Sanskrit | Akkadian |
| Sumerian Ur III (E3h) | 16,000 | 0.207 | 0.182 | 0.084 | 0.119 | 0.013 | Sanskrit | Sumerian |

- In all four ciphers the Sanskrit model comes first. By the registered rule the method has no power at either size.
- More data does not help. From 2,000 to 8,000 lines the Tamil cipher's margin in favour of the wrong language stays the same.

### Assessment of the phonetic route (E3–E3h)

- The scoring measure works when the true assignment is given (E3g).
- The search does not find assignments that favour the true language. For every cipher tried (two cuneiform and two syllabic, from 2,000 to 16,000 lines), the assignments it finds are best explained by the Sanskrit model.
- The likely cause is that the Ṛgveda model, even when equalised in size, assigns high probability to the kind of short, vowel-rich syllable sequences that any fitted assignment produces. This was not tested further.
- The consequence for the Indus inscriptions is clear. Search-based phonetic fitting of this kind is biased towards one language whatever the input. No language preference for the Indus script can be drawn from it, and claims based on similar unconstrained fitting should be read with this in mind.
- Gate G4 (L3) remains unmet. The conclusion of E3c and E3d is strengthened: the failure is not a matter of corpus size (2,000–16,000 lines) or of representability (the syllabic ciphers are exactly representable).

### End of the thirty-fifth session

- Pre-registered analyses:
  - E3g (oracle): supported.
  - E3e, E3f, E3h: the method has no power.
- The level assessment is unchanged.

---

## 2026-11-26 (day 2, thirty-sixth working session, 04:18 UTC): why the phonetic search favours Sanskrit, and how many known values would rescue it

E3e–E3h showed that the search ranks the Sanskrit model first for every cipher, while the scoring identifies the true language when the true assignment is given (E3g). This session tests three explanations and measures how much prior knowledge of sign values the method would need. That last measurement is the practical question behind the work-plan route P4e (values fixed in advance from the pictographs).

### Plan of the run

1. E3i: without the Sanskrit model, does the Tamil cipher rank Tamil first?
2. E3j: with a Sanskrit model from dictionary headwords (Monier-Williams) instead of the Ṛgveda, does the bias persist?
3. E3k: with more search effort (8 sweeps, 6 restarts instead of 4 and 2), does the Tamil cipher rank Tamil first?
4. E3m: if a fraction f of the 100 most frequent signs is fixed at its true value before fitting, from what f on does the true language win?
5. Updates.

### Pre-registrations (before running)

All four use the 2,000-line syllabic ciphers of E3e (same construction and seeds), the E3b/E3d Δ′ measure and the bootstrap decision of E3d. "Success" for a cipher means that its true language is first and clearly ahead of every other model in the set.

**E3i.** Models: Tamil, Sumerian, Akkadian, pseudo (E3d models without Sanskrit). Prediction: success for the Tamil cipher. The Sanskrit cipher is reported descriptively.

**E3j.** Models: the E3d models with Sanskrit replaced by 20,000 tokens of Monier-Williams headwords (`phonetic.sanskrit_words`, equalised with the same function and seed). Prediction, if the bias comes from the Ṛgveda text: the Tamil cipher succeeds. If the Sanskrit model still wins for the Tamil cipher, the bias is not specific to that source.

**E3k.** E3d models; search with 8 sweeps and 6 restarts. Prediction, if the failure is due to search depth: both ciphers succeed.

**E3m.**
- E3d models.
- Before fitting, a fraction f ∈ {0.10, 0.25, 0.50} of the 100 most frequent cipher signs is fixed at its true value. The signs are chosen at random with seed 20261126, the same set for all models.
- The remaining signs are fitted by the same search, and the fixed signs are not changed.
- Reported: for each cipher, the smallest f with success ("> 0.50" if none). No prediction.

### Results E3i, E3j, E3k, E3m

Script: `scripts/batch17_phonetic_diagnosis.py`; results: `results/batch17_e3i.json` … `batch17_e3m.json`.

- **E3i (without the Sanskrit model): not supported.**
  - Tamil cipher: Tamil first (0.215), but not clearly ahead of Akkadian (0.180, p = 0.047) or Sumerian (0.174, p = 0.040).
  - Sanskrit cipher (descriptive): Tamil first (0.163), not clearly ahead.
  - Without Sanskrit the true language leads for the Tamil cipher, but the margin is too small to decide.
- **E3j (dictionary Sanskrit model): the bias persists.**
  - Tamil cipher: Sanskrit (headwords) 0.430 against Tamil 0.215.
  - Sanskrit cipher: Sanskrit first (0.382).
  - The bias is not specific to the Ṛgveda text. Sanskrit models from either source absorb fitted assignments best.
- **E3k (more search effort): not supported.**
  - Tamil cipher: Sanskrit 0.285 against Tamil 0.270, not separated (p = 0.32).
  - More search effort narrows the gap but does not remove it. The search depth contributes to the failure, but it is not the whole cause.
- **E3m (known values): the true language wins once enough values are known.**
  - Sanskrit cipher: success from f = 0.10, i.e. 10 of the 100 most frequent signs fixed (0.441 at f = 0.50).
  - Tamil cipher: success from f = 0.25, i.e. 25 signs fixed. Tamil 0.450 against Sanskrit 0.278; at f = 0.10 Sanskrit (0.258) and Tamil (0.253) are still level.

### What E3e–E3m mean for the Indus script

- The method can identify a language once roughly a quarter of the frequent sign values are known correctly in advance. Without that knowledge it falls back on whichever model absorbs arbitrary syllable strings best, here Sanskrit.
- For the Indus script no sign value is known independently. Route P4e would need about 25 of the 100 most frequent signs to carry correct values fixed in advance, for example from the pictographs, and those values would have to be right.
- This applies to an alphabetic-syllabic language whose units are those of the value set. A logographic script, which the combinatorial evidence suggests (CT27), would need more.
- No such set of values exists. The phonetic route stays closed for the Indus inscriptions, and the requirement is now stated in numbers (`docs/FUTURE_DATA.md`).

### End of the thirty-sixth session

- Pre-registered analyses:
  - Not supported: E3i, E3k.
  - Bias persists: E3j.
  - Descriptive threshold: E3m (f = 0.10 for Sanskrit, 0.25 for Tamil).
- The level assessment is unchanged.
