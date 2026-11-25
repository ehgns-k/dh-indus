# Data-use ledger

Every hypothesis test is listed with the data it was decided on. "Train" = non-held-out unique strings; "held-out" = the fixed 20 % split (`is_heldout`); "fresh" = sites first excavated after 1979 (fresh set 1: Dholavira, Nausharo; fresh set 2: eight further sites, `docs/FRESH_SITES.md`); "all" = both splits.

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
| C2 | ICIT | discovery train, confirmation held-out | 6 of 40 confirmed | 14th held-out question; Bonferroni 0.01/40 ; R1: fails strict thresholds → L2 candidate |
| F4 | ICIT | fresh sets 1+2 | not supported (p = 0.0104) | direction agrees with C2 |
| E2 | proposed readings (claim C33) | all readings | readability not discriminating | control rate 0.29 |
| E2b | ICIT lines, random assignments | all lines ≤ 10 signs | random assignments readable at 0.84 | same as proposed readings |
| C2k | KP | discovery train, confirmation held-out | 1 of 10 confirmed (11 × final 98) | replicates C2 (400 avoided on motif seals) ; R1: fails strict threshold → L2 candidate |
| E3 | ICIT + two cuneiform ciphers | held-out (ICIT fixed split; ciphers 80/20) | method has no power | positive control 2 failed |
| E3b | same | same | method has no power | both positive controls failed |
| E3c | two cuneiform ciphers, 8,000 lines | 80/20 | method has no power | failure not due to corpus size |
| C3 | ICIT | discovery train, confirmation held-out | 1 of 5 confirmed (TAB:I short) | 15th held-out question; not counted as L2 |
| R1 | ICIT, KP | strict held-out (no near-duplicates) | L1 results pass; C2/C2k fail strict thresholds | review; L2 downgraded to candidate |
| Q2a | ICIT, KP | train (each) | supported (zone agreement 0.91) | reproducibility of the descriptive classification |
| E3d | ICIT strict held-out + two ciphers | as E3b | method has no power | equalised running-text models; Indus row not interpreted |
| H6.1 | ICIT | fresh sets 1+2 | supported (p = 0.0012) | short and long strokes take disjoint partners; without 033 p = 0.015 (robustness) |
| L3a | ICIT | train | 3 of 10 KP-merged pairs distinct | descriptive classification; robustness check with 10,000 relabellings |
| L3b | KP | train | none by registered test (resolution flaw); 6 distinct in robustness check | descriptive classification |
| D3 | ICIT, KP, reference corpora | all unique lines (9,000 tokens) | descriptive (Chao1: ICIT 830, KP 511, proto-Elamite 820) | not a test |
| H7.1 | ICIT | fresh sets 1+2 | not supported (HMM worse than bigram) | states reproduce the functional grouping (descriptive) |
| R2 | ICIT, KP | strict held-out | H3.10 robust in KP; in ICIT depends on 004 | review |
| D1-KP | KP + CDLI reference corpora | resampled | proto-Elamite nearest on average (2.70); administrative corpus nearer in 19/20 | robustness; low-repetition observation withdrawn |
| G1 | ICIT + glyph images | train | not supported (no global shape–usage correlation) | |
| G2 | ICIT + glyph images | strict held-out + fresh | supported (p = 0.0017) | close-shape pairs share usage |
| H8.1 | ICIT | abroad lines vs strict held-out home lines | not supported (p = 0.011) | Gulf lines lack the terminal cluster (descriptive) |
| M1 | ICIT + glyph images | train | not supported (both shape measures) | |
| G2-HOG | ICIT + glyph images | strict held-out + fresh | G2 holds (p = 0.0074) | robustness with a structural shape measure |
| H9.1 | ICIT, KP | all unique complete strings | supported (p = 0.0001 both) | texts differing only in the stroke count |
| H9.2 | ICIT | all strings; secondary strict held-out + fresh | not supported (p = 0.58; 0.093) | count-variable formulae not concentrated on tablets |
| H9.3 | ICIT, KP | all unique complete strings | supported (ARI 0.169, p = 0.0001) | substitution classes agree across transcriptions |
| H9.4 | ICIT | discovery train, confirmation strict held-out | 1 of 6 confirmed (class 4 avoids TAB:C) | L2 candidate |
| T1 | ICIT (Harappa, periods 3B/3C) | all records with period | not supported (mostly insufficient data) | |
| H10.1 | ICIT | all unique strings | not supported (p = 0.67) | name-like slot fillers not more site-specific |
| R3 | all | – | review: all analyses re-run; phonetic searches made deterministic; conclusions unchanged | |
| R4 | KP (normalised strokes) | all unique complete strings | H9.1 holds (84 vs 12.4, p = 0.0001) | review |
| H9.6 | ICIT, KP (normalised) | all unique complete strings | not supported (ICIT p = 0.0022; KP p = 0.050) | substituted counts closer than chance in both, significant in one |
| D4 | ICIT, KP, reference corpora | resampled | not supported (0/20) | statistic measures numbered formulae, not genre |
| CT16 | ICIT, KP | strict held-out (+ fresh for ICIT) | not supported (opposite direction) | claim C16 |
| CT17 | ICIT, KP | strict held-out | supported (p = 0.001 both) | claim C17 |
| CT10 | ICIT | all unique strings | supported | claim C10 |
| G3 | ICIT + glyph images | strict held-out + fresh | insufficient data (2 mirror pairs) | claim C3 |
| CT18 | ICIT, KP | strict held-out | supported (p = 0.001 both) | claim C18 |
| CT15 | ICIT | strict held-out + fresh | supported (OR 4.3, p = 0.0022) | claim C15; functional L2 in narrow scope; fails a family-wise correction over the ≥ 11 questions decided on the strict held-out set |
| D5 | ICIT, KP, reference corpora | resampled | not supported (13/20 nearest proto-Elamite) | same average ordering as D1 |
| CT26 | ICIT, KP | all unique strings | not supported (sequence is ABC + D) | claim C26 |
| CT3 | ICIT | all unique strings | no mirror pair distinct (low power) | claim C3 |
| CT15k | KP | strict held-out | not supported (p = 0.21; 3 tablet texts) | replication of CT15, underpowered |
| CT15t | ICIT | all tag and tablet strings with 740 | supported (OR 6.0, p = 0.0068) | tags never used before as a class; site-confounded |
| CT28 | ICIT | all records, Harappa and Mohenjo-daro | supported (difference 0.49, 1,000/1,000 subsamples) | seal stems individual-specific |
| CT15s | ICIT | all pottery strings | insufficient data (3 stamped strings with 740) | incised pottery also ends in 740 (11/12) |
| CT31c | ICIT | all Harappa tablet and all seal records | not supported (p = 0.013) | claim C31c |
| CT32a | ICIT | Harappa records | supported (2.84 vs 1.05 records per text) | claim C32a |
| CT19 | ICIT, KP, D2 corpora | 300-line samples | not supported (inside both ranges) | claim C19 |
| CT25 | KP (normalised) | all unique strings | drop after seven (6 observed vs 34.5 predicted) | claim C25; base undecided |
| CT14 | ICIT | all unique strings | supported (740 most diverse left context) | claim C14; corrects earlier descriptive reading |
| R6 | ICIT, KP | all unique strings | H9.3 robust at resolution ≥ 1.0, weak at 0.6–0.8 | review |
| CT27 | ICIT, KP, Akkadian letters | 9,000-token resamples | supported (20/20 both) | claim C27 |
| CT28k | KP | all records with seal/tablet codes | supported (1,000/1,000) | replication of CT28 |
| CT14k | KP (normalised) | all unique strings | supported (jar sign rank 1 of 24) | replication of CT14 |
| CT25b | KP (normalised) | all unique strings | drop after seven remains (6 vs 18.1) | robustness of CT25 |
| CT32k | KP | all records with seal/tablet codes | supported (2.61 vs 1.10 records per text) | replication of CT32a |
| CT22 | ICIT | strict held-out + fresh | supported (p = 0.0009) | claim C22, distributional part |

| ML1 | ICIT | all objects with two complete lines (76) | supported (p = 0.0001) | the two lines form one text closed once |
| ML1k | KP | objects with lines_code 2 and two complete records (80) | supported (p = 0.0023) | replication; code meaning inferred |
| NUM2 | ICIT, KP | all unique strings | not supported (ICIT 22 vs 11, p = 0.080); KP insufficient data | no fixed long/short order |
| NUM1 | ICIT, CDLI proto-Elamite and proto-cuneiform | all lines | descriptive: numeral before sign (0.71), unlike proto-Elamite (0.004) | not a test |
| KF1 | ICIT, KP | all unique strings | supported (75 % vs 7.9 % of control frames) | across transcriptions of the same objects |
| ML2 | ICIT, KP | objects of ML1, ML1k | not supported (p = 0.43, 0.46) | line breaks not at segment boundaries |
| F5 | ICIT (formulae from train) | fresh sets 1+2 | supported (9 vs 4.8 matches, p = 0.0008) | rule-preserving controls |
| FACE1 | ICIT, KP | all two-face objects without numeral face (258; 195) | supported (p = 0.0001 both) | one text per object, closed once |
| FACE2 | ICIT, KP | all two-face objects with a numeral + 700/310 face (246; 242) | supported (ICIT p = 0.0001; KP p = 0.0093) | count partly tied to the text series; robust without the largest group |
| R7b | as B1, B4, CT17, CT18 | as original | p = 0.0001 with 10,000 draws | review: resolution only |
| R7 | – | – | review: 15 of 38 fresh/strict tests survive Holm 0.01; CT15 survives Holm 0.05 and BH 0.01 | family-wise review |

Count of questions decided on the (full) held-out split before the review R1: 15 (H3.3, H3.7, H3.9, H3.10, H3.12, H3.13, H3.14, H4.1, H4.2, H4.3, the H3.5 secondary set, H5.1, C2, C3; see rows). From R1 on, held-out tests use the strict held-out set; questions decided on it (alone or with the fresh sets) include R1, H8.1, H9.2 (secondary), E3d, G2, H9.4, CT16, CT17, CT18, G3, CT15 and later rows (at least 11 at the time of CT15). Questions decided on fresh data are marked in the table (F2, F3, F2b, F3b, B1, B4, H5.1b, F4, H6.1, H7.1 and the fresh parts of G2, CT16, CT15).

The supported held-out results remain significant after a Bonferroni correction over these 11 tests (0.01/11 ≈ 0.0009) except where noted: H3.3 (p ≤ 3.8 × 10⁻⁷), H3.10 (p ≤ 7.5 × 10⁻⁹), H3.12 (p ≤ 3.4 × 10⁻⁷) pass; H4.3 (p = 0.001) does not.


**Review note (thirteenth session).** 42 % (ICIT) and 47 % (KP1979) of held-out strings have a training string within edit distance 1. All held-out results were re-decided on the strict held-out set (R1). From now on, held-out tests use the strict set.
