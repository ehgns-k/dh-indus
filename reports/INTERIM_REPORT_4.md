# Interim report 4 (2026-11-25, night)

This report summarises the work since interim report 3. Details and pre-registrations are in `docs/JOURNAL.md` (twenty-first to twenty-fourth sessions). Data use is in `docs/DATA_LEDGER.md` and claim verdicts in `docs/CLAIMS_EVALUATION.md`.

## 1. Structure (L1)

| Test | Result |
|---|---|
| ML1, ML1k | On inscriptions with two lines, the closing sign occurs on one line only: exactly one line closes on 47 of 76 objects (ICIT; 33.0 expected, p = 0.0001), and both close on 3 (10.0 expected). KP1979 shows the same (p = 0.0023). The two lines form one text. |
| ML2 | The line break does not fall at a segment boundary more often than a random cut (ICIT p = 0.43, KP p = 0.46). The text is broken where the space ends. |
| KF1 | Of the ICIT formula frames, 75 % are also formula frames in KP1979, against 7.9 % of single-filler control frames. A KP formula table is in `docs/FORMULAE_KP.md`. |
| F5 | Formulae learned from the training data recur in later finds: 9 of 86 strings from the ten post-1979 sites fit a training formula, against 4.8 for rule-preserving controls (p = 0.0008). |
| CT22 | The plain and modified fish-shaped signs are used in similar contexts on unused data (p = 0.0009). |
| CT27 | Frequent Indus signs combine less freely than the graphemes of syllabic Akkadian letters (20/20 resamples, both transcriptions). |
| CT14k, CT25b, CT28k, CT32k | Replications and robustness checks of CT14, CT25, CT28 and CT32a; all hold. |

## 2. Numerals

| Test | Result |
|---|---|
| NUM1 (descriptive) | The Indus numeral comes before the sign it goes with (71 % of cases). Proto-Elamite entries put the sign before the numeral (99.6 %), and the CDLI transliterations of proto-cuneiform put the numeral first (98 %). |
| NUM2 | Long and short stroke signs do not combine in a fixed order (22 vs 11, p = 0.080; KP too few cases). A multi-unit notation with ordered units, as in the proto-Elamite metrological systems, is not shown. |
| CT25b | The drop in frequency after seven strokes remains after removing the fixed pairing 7 + 288/289. The base is undecided. |

## 3. Review

- **R7.** A family-wise review covered all 38 tests decided on fresh or strict held-out data, including the failed ones.
  - The core L1 results survive a Holm correction at α = 0.01: reading direction, closing-cluster order, count–item pairs, positional template, recurring units and nested structure.
  - The narrow L2 result CT15 survives Holm at α = 0.05 and false-discovery control at q = 0.01, but not Holm at α = 0.01.
- **R7b.** The tests B1, B4, CT17 and CT18, whose p-values were bounded by 1,000 control draws, were re-run with 10,000 draws. All give p = 0.0001.
- **Object codes.** The ICIT object codes were documented (`docs/OBJECT_CODES.md`). The `class` field of the source is derived from the text and was never used as an external variable.
- **Combined inventory (L-3b).** The allograph decisions supported by usage leave the inventory almost unchanged: 714 units against 713 ICIT types (`docs/COMBINED_INVENTORY.md`).

## 4. Position

L1 is achieved in broad scope and survives the strictest correction applied. L2 is achieved only in the narrow functional form of CT15, and L3 is not achieved. The tests that the accessible data allow are now largely exhausted. Most remaining questions need unused inscriptions (for confirmation of the L2 candidates) or independent constraints on sound values (for L3), and neither is available (`docs/NEW_DATA_SURVEY.md`).
