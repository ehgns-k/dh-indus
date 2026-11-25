# Data-use ledger

Every hypothesis test is listed with the data it was decided on. "Train" = non-held-out unique strings; "held-out" = the fixed 20 % split (`is_heldout`); "fresh" = post-1979 sites (Dholavira, Nausharo); "all" = both splits.

| Test | Corpus | Decision data | Result | Note |
|---|---|---|---|---|
| H3.1 | ICIT, KP | train | not supported | |
| H3.2 | ICIT, KP | train | partly supported | k not fixed in advance |
| H3.3 | ICIT, KP | held-out | supported | |
| H3.4 | ICIT | all, split by site | supported | |
| H3.5 | ICIT | train (Harappa) → Mohenjo-daro strings | not supported | |
| H3.6 | ICIT | train (Harappa) → Mohenjo-daro strings | supported, narrowly | |
| H3.7 | ICIT | held-out | not supported | |
| H3.8 | ICIT, KP | train | not supported | |
| H3.9 | ICIT, KP | held-out | not supported | |
| H3.10 | ICIT, KP | held-out | supported | |
| H3.11 | ICIT, KP | train | passed | robustness check |
| H3.12 | ICIT, KP | held-out | supported | |
| H3.13 | ICIT, KP | held-out | not supported | |
| H3.14 | ICIT, KP | held-out | not supported | |
| H4.1 | ICIT | held-out | not supported | |
| H4.2 | ICIT | held-out | not supported | |
| H4.3 | ICIT | held-out (tablets) | supported, weak under strict control | |
| F1 | ICIT (rule from KP train) | fresh | insufficient data | |
| F2 | ICIT (rule from KP train) | fresh | supported | |
| F3 | ICIT (model from KP train) | fresh | supported | |
| C1 | ICIT | all copper-tablet strings | not supported | not held-out; motif coding inconsistent |
| F2b | ICIT (rule from KP train) | fresh set 2 | not supported | 3 bigrams only |
| F3b | ICIT (model from KP train) | fresh set 2 | supported (direction) | |
| B1 | ICIT (zones from KP train) | fresh sets 1+2 | supported | rule-preserving controls |
| B4 | ICIT (units from KP train) | fresh sets 1+2 | supported | rule-preserving controls |
| H5.1 | ICIT, KP | held-out | not supported | KP passes, ICIT fails; control amended before running |
| H5.1b | ICIT | fresh sets 1+2 | not supported | corrected stroke set |
| D1 | ICIT + CDLI reference corpora | all ICIT unique complete lines (resampled) | supported | typology, descriptive; no non-linguistic corpus |
| D2 | ICIT + CDLI + Sproat (2014) corpora | all (resampled to 300 lines) | G3 undecided | leave-one-out 5/7 |

Count of tests decided on the held-out split so far: 11 (H3.3, H3.7, H3.9, H3.10, H3.12, H3.13, H3.14, H4.1, H4.2, H4.3, and the H3.5 secondary set). Count decided on fresh data: 3.

The supported held-out results remain significant after a Bonferroni correction over these 11 tests (0.01/11 ≈ 0.0009) except where noted: H3.3 (p ≤ 3.8 × 10⁻⁷), H3.10 (p ≤ 7.5 × 10⁻⁹), H3.12 (p ≤ 3.4 × 10⁻⁷) pass; H4.3 (p = 0.001) does not.
