# Interim report 1 (2026-11-25)

This report summarises the results of the first working day against the success criteria of `ROADMAP.md`. Details, including every failed test, are in `docs/JOURNAL.md`; the data used for each decision are listed in `docs/DATA_LEDGER.md`.

## 1. Data

| Source | Content | Use |
|---|---|---|
| ICIT-style transcription (horus84, commit `ac44f08`) | 5,679 records with site, object type, material, motif | main corpus |
| Koskenniemi & Parpola 1979, machine reading (koskenni, commit `60f6e28`) | 4,066 inscriptions, independent sign numbering and object codes | replication corpus |
| Sign concordance (this project) | 929 aligned line pairs, 594 identical | links the two numbering systems |
| Inscriptions from ten sites first excavated after 1979 | 117 lines (fresh sets 1 and 2) | data that the 1979 corpus cannot contain |
| CDLI bulk data | proto-Elamite, proto-cuneiform, Sumerian, Akkadian | typology |
| Sproat (2014) corpora | non-linguistic symbol systems | typology |

## 2. Results by level

### L1: structural results (met)

1. **Reading direction and order.** Order regularities learned from the 1979 corpus predict inscriptions from sites excavated later, and only in the right-to-left reading direction (F3, F3b).
2. **Terminal cluster.** Line-final signs form a cluster with a fixed internal order (740 before 400 or 090), on held-out data and across sites (H3.3, H3.4).
3. **Count–item pairing.** Signs of 4–9 short strokes are followed by one sign group (KP 86 / ICIT 390–407) far more often than other signs are; the seven-stroke sign by KP 288/289, the three-long-stroke sign by KP 217. Held-out data in two transcriptions, matched controls, and post-1979 sites (H3.10–H3.12, H3.11, F2).
4. **Positional template and recurring units.** An initial → medial → terminal template and a lexicon of recurring sign units, learned from the 1979 corpus, predict the post-1979 inscriptions against controls that preserve all earlier rules (B1, B4; gate G1).

### L2: semantic or functional categories (met in narrow, functional scope; **downgraded to a candidate in the review of the same day, see note below**)

- **The closing sign depends on the kind of object.** Line-final 400 (KP 98) is avoided on motif-bearing seals and favoured on tablets; 407 and 154 are favoured on rectangular seals without motif. Discovered with false-discovery-rate control and confirmed on held-out data in the ICIT corpus with site stratification (C2), and replicated in KP1979 with its independent 1973 object codes (C2k). The meaning of these signs is not identified.

### L3: phonetic decipherment (not achieved)

- No phonetic assignment was proposed by this project.
- **Test of a published phonetic claim (Sanskrit, claim C33).** Under the reading freedoms and normalisation of that proposal, random sign-value assignments make 84 % of Indus lines readable as Sanskrit dictionary words, the same rate as the published readings (E2, E2b). Readability under these rules is therefore no evidence for the proposal.

### Is it writing? (gate G3: undecided)

- The Indus corpus is statistically closest to proto-Elamite and proto-cuneiform, the two proto-administrative systems in the reference set, and further from Sumerian and Akkadian full writing (D1).
- With non-linguistic symbol systems added, the statistics used cannot separate writing from non-writing (leave-one-out 5 of 7), so no conclusion about the linguistic status is drawn (D2).

## 3. Main negative results

| Test | Result |
|---|---|
| Terminal signs mark word boundaries (H3.1) | not supported |
| Seal vs tablet texts transfer across sites (H3.5); numerals more frequent on tablets (H4.1) | not supported |
| Text predicts seal motif (H4.2); copper-tablet text and motif (C1) | not supported |
| Numeral + fish as star names, counts 3/6/7 (H3.13, H3.14) | not supported |
| Sign 119/002 introduces numbers (H5.1, H5.1b) | not supported (KP yes, ICIT no) |

## 4. Errors found and corrected

- A sign set in H5.1 was defined inconsistently between the two corpora; the verdict was kept as registered and a corrected test was run on new data (H5.1b).
- Random control sets in H3.8/H3.9 depended on Python's hash seed; fixed, conclusions unchanged.
- The control in H4.3 did not preserve an established rule; a rule-preserving control generator was introduced (WP A2).

## 5. Next steps

See `docs/WORKPLAN.md`, section 4 (priority list): structural analogy with proto-Elamite entries (P3), conditional language-hypothesis tests with the calibration of E2b (P4), and the final report (P5).


## Note added in the review (same day)

A review found that 42–47 % of held-out strings had a near-identical training string. All held-out results were re-decided without them (R1, `docs/JOURNAL.md`). The L1 results pass again. The C2/C2k association between closing sign and object class keeps its effect size but no longer reaches the strict thresholds, so it is now an **L2 candidate**, not an L2 result.
