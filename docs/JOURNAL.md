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
