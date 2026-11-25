# Phase 3 report: structure of the Indus inscriptions

Status: 2026-11-25. All tests were pre-registered in `docs/JOURNAL.md`; the data used for each decision are listed in `docs/DATA_LEDGER.md`. Sign numbers are ICIT-style numbers unless marked KP (Koskenniemi & Parpola 1979).

## 1. Data and controls

- Two transcriptions of largely the same objects: the ICIT-style source (5,679 records) and KP1979 (4,066 inscriptions), linked by a sign concordance obtained from 929 aligned line pairs (`docs/SIGN_CONCORDANCE.md`).
- Three kinds of test data: the strict held-out split (held-out strings without a training string within edit distance 1; review R1), inscriptions from ten sites first excavated after 1979 (`docs/FRESH_SITES.md`), and, for replication, the other transcription.
- Controls that keep every established rule (`src/indus/controls.py`).

## 2. Established structural results

### 2.1 Reading direction and order

Sequential regularities learned from KP1979 predict inscriptions from sites excavated after 1979, and only in the right-to-left reading order: forward bigram better than reversed on 57 of 63 strings (fresh set 1) and 14 of 15 (fresh set 2) (F3, F3b).

### 2.2 Positional template

Signs fall into an initial zone, a medial zone and a terminal zone. The zones, computed independently in the two transcriptions, agree for 91 % of linked signs (Q2a). A template initial → medial → terminal, learned from KP1979, has fewer inversions in post-1979 inscriptions than rule-preserving controls (31 vs 55.7; B1).

### 2.3 Terminal cluster

Line-final signs form a cluster with a fixed internal order: 740 before 400 or 090 (KP 324/325 before 98 or 13). Held-out agreement 0.97 (ICIT) and 0.91 (KP1979) (H3.3), reproduced across Harappa and Mohenjo-daro (H3.4) and on the strict held-out set (R1). Terminal signs do not mark word boundaries inside lines (H3.1, not supported).

### 2.4 Numerals and count–item pairs

- Signs consisting of one to ten short strokes, and of one to five long strokes, are identified from the printed sign list; ICIT and KP numbers agree with stroke counts (B2, B3). KP1979 often writes a two-stroke sign as two single strokes (split/merge analysis).
- Specific counts are followed by specific signs: 4–9 short strokes → 390 / 405 / 406 / 407 (KP 86); 7 short strokes → 585 / 575 (KP 288 / 289); 3 long strokes → 520 (KP 217). Held-out data in both transcriptions (H3.10, H3.12), against matched controls (H3.11), on the strict held-out set (R1), and for 4–9 strokes also on post-1979 inscriptions (F2). In KP1979 the result does not depend on any single stroke sign; in the ICIT strict held-out set it depends mostly on four-stroke signs (R2).
- Short and long strokes take disjoint partner signs on post-1979 inscriptions (H6.1, p = 0.0012); the result rests largely on sign 033, whose identity differs between the transcriptions, so the reading as two numeral notations is only suggested.

### 2.5 Recurring units and sign families

- Two- and three-sign units recurring in KP1979 recur in post-1979 inscriptions more often than in rule-preserving controls (84 vs 37.2 covered pairs; B4).
- Signs that are near-variants in shape (a base form with added marks) are used in similar contexts on data not used to see the pattern (G2; confirmed with a structural shape measure). Across all signs, shape does not predict usage (G1), and added marks do not shift position consistently (M1).
- An unsupervised eight-state model recovers the same grouping (initial signs, numerals, counted items, fish-shaped signs, closing signs), although it does not predict new texts better than a bigram model (H7.1).

### 2.6 Sign inventory

The estimated total number of sign types (Chao1) is about 830 in the ICIT transcription and about 510 in KP1979, the difference reflecting how finely the two lists split variants (D3; allograph tests L3a, L3b).

### 2.7 Formulae with a variable count and substitution classes (added later the same day)

- Texts that are identical except for the number of strokes in one slot are six to eight times more frequent than chance in both transcriptions (ICIT 94 vs 15.2 expected; KP1979 183 vs 23.0); about half differ by two or more strokes (H9.1). The KP1979 result holds after short/long variants and split strokes are normalised (R4: 84 vs 12.4 expected).
- Signs that replace one another in otherwise identical texts form classes (numerals; closing and counted-item signs; fish-shaped signs with single strokes; others) that agree between the transcriptions (ARI 0.169, p = 0.0001; H9.3).

### 2.8 Lines, faces, directions and object classes (added later, twenty-fourth to twenty-eighth sessions)

| Test | Result |
|---|---|
| ML1, ML1k | The two lines of a two-line inscription form one text, closed once (ICIT p = 0.0001; KP p = 0.0023) |
| ML2 | Line breaks are not at segment boundaries (p = 0.43, 0.46) |
| FACE1, FACE4 | The faces of a two- or three-face object form one text, closed once (p = 0.0001); not replicated for three-face objects in KP1979 (FACE4k, p = 0.33) |
| FACE2 | Tablets with the same text tend to carry the same count on their numeral face (ICIT p = 0.0001; KP p = 0.0093) |
| KF1, F5, F5k | Formulae recur across transcriptions and in later finds |
| DIR1, DIR2 | Lines written left to right, and lines of unknown direction, follow the normalised order (105/122; 84/127) |
| SX1 | Order regularities learned at other sites predict Harappa and Mohenjo-daro forward |
| PT1–PT3 | Template, units and count–item pairing carry over from seals and tablets to other objects; for pottery only the units and the pairing are shown |

## 3. Results that were not supported

| Hypothesis | Test |
|---|---|
| Terminal signs mark word boundaries | H3.1 |
| Stroke signs form one distributional paradigm | H3.8, H3.9 |
| Sign 119 / 002 introduces numbers | H5.1, H5.1b |
| Numeral + fish signs name star groups (published claim C23) | H3.13, H3.14 |
| An eight-class hidden Markov model predicts new texts better than bigrams | H7.1 |
| Added marks shift position consistently | M1 |
| Inscriptions found abroad are less predictable | H8.1 (p = 0.011; Gulf lines lack the terminal cluster, descriptive) |

## 4. Corrections made during the phase

- Near-duplicate texts across the held-out split (R1); results re-decided on the strict held-out set.
- Non-deterministic control sets in H3.8/H3.9 (fixed).
- Too lenient control in H4.3 (led to the rule-preserving control generator).
- Inconsistent sign set in H5.1 (verdict kept; corrected test H5.1b).
- Insufficient permutation resolution in L3b (rule added to `docs/METHOD.md`).
- A shape measure dominated by outline (robustness check with a structural measure).
- Withdrawal of the "low repetition" observation, which depends on the transcription.

## 5. Summary

The inscriptions follow a consistent organisation that holds across sites, across the two transcriptions and on finds made after the main corpus was published: a fixed right-to-left order; initial, medial and closing zones; a closing cluster with a fixed internal order; a stroke notation in which particular counts go with particular following signs; recurring multi-sign units; and families of near-variant signs with similar usage. These are structural (L1) results. They do not identify the meaning or the sound of any sign.
