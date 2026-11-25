# Final report (living draft): an attempt to decipher the Indus script

Status of this draft: 2026-11-25. The report is updated as work continues until 2026-12-25. Every result cited here is documented, with its pre-registration, in `docs/JOURNAL.md`; the data used for each decision are listed in `docs/DATA_LEDGER.md`; detailed phase reports are in `reports/`.

## 1. Aim and criteria

The project set out to decipher the Indus script as far as verifiable evidence allows. Success was defined before any analysis in four levels (`ROADMAP.md`): L1 structural results; L2 semantic or functional categories that predict information outside the texts; L3 sound values that predict unseen texts better than control languages; L4 full decipherment.

## 2. Material and method

- Two machine-readable transcriptions of largely the same objects (ICIT-style source, 5,679 records; Koskenniemi & Parpola 1979, 4,066 inscriptions), linked by a sign concordance derived from 929 aligned texts.
- Test data that were not used to form hypotheses: a strict held-out split without near-duplicate texts; 117 lines from ten sites first excavated after 1979; the second transcription for replication.
- Reference systems: proto-Elamite, proto-cuneiform, Sumerian and Akkadian texts (CDLI); non-linguistic symbol systems (Sproat 2014); Sanskrit, Old Tamil, Sumerian and Akkadian word data for sound models; sign images keyed to ICIT numbers.
- Every test was pre-registered in the journal; controls preserve every rule already established; all scripts are deterministic and re-run by `scripts/run_all.py`.

## 3. Results

### L1 — structure (achieved)

1. The texts are read right to left; order regularities learned from the 1979 corpus predict inscriptions from later excavations only in that direction (F3, F3b).
2. Lines have an initial zone, a medial zone and a closing zone; zones agree between the two transcriptions (Q2a) and predict later finds (B1).
3. The closing signs form a cluster with a fixed internal order, 740 before 400 or 090 (H3.3, H3.4, R1).
4. Stroke signs of one to ten strokes form a numeral notation: particular counts are followed by particular signs (4–9 strokes → 390–407; 7 → 585/575; three long strokes → 520) in both transcriptions and on strict held-out data (H3.10–H3.12, R1, R2), and for 4–9 strokes also on later finds (F2); texts that are identical except for the count are six to eight times more frequent than chance, also after normalisation of writing variants (H9.1, R4).
5. Recurring multi-sign units and formulae with variable slots: units learned from the 1979 corpus recur in later finds (B4); signs that substitute for one another form classes (numerals; closing and counted-item signs; fish-shaped signs with single strokes; others) that agree between transcriptions for fine-grained classes, robust to the random seed (H9.3, R6); 131 formulae with a variable slot are listed in `docs/FORMULAE.md`. Longer texts have a nested structure: parts obtained by recursive splitting at the weakest link are complete short texts about three times as often as in controls (CT18).
6. Near-variant sign shapes are used alike on unused data (G2), while shape in general does not predict usage (G1) and added marks do not shift position consistently (M1).
7. The two lines of a two-line inscription form one text that is closed once, in both transcriptions (ML1, ML1k); the formulae found in one transcription recur in the other (KF1: 75 % of formula frames vs 7.9 % of control frames), and formulae learned from the training data recur in later finds (F5: 9 strings vs 4.8 for rule-preserving controls, p = 0.0008); long and short stroke signs do not combine in a fixed order (NUM2).
8. In a family-wise review over all 38 tests decided on fresh or strict held-out data, the direction test, the closing-cluster order, the count–item pairs, the positional template, the recurring units and the nested structure survive a Holm correction at α = 0.01 (R7, with the permutation tests re-run with 10,000 draws, R7b).

### L2 — semantic or functional categories (achieved only in narrow, functional scope)

- **Confirmed (narrow, functional):** the jar sign 740 closes seal texts more often than tablet texts at Harappa and Mohenjo-daro (site-stratified; the 'other sites' stratum has a single tablet text), in a single pre-registered test on data not used for this question (CT15; odds ratio 4.3, p = 0.0022). What the closing sign means (a genitive, a title, a classifier) is not established. The result passes its own threshold; in the family-wise review over all 38 tests decided on unused data (R7) it survives a Holm correction at α = 0.05 and false-discovery control at q = 0.01, but not a Holm correction at α = 0.01, so it is not beyond doubt. A replication in KP1979 points the same way but has almost no power (three tablet texts; CT15k, p = 0.21). Tags, objects with seal-type legends never used as a class before, follow the seal pattern (740 final in 14 of 16; tablets 54 %; CT15t, p = 0.0068), although tags come mostly from one site. Incised pottery inscriptions that contain 740 also end in it (11 of 12; CT15s, too few stamped pots to test), so the closing function is not confined to seal legends; it is tablets that stand apart.

Further candidates:

- The closing sign depends on the kind of object (400 avoided on motif seals and favoured on tablets; 407 and 154 on rectangular seals without motif), consistent in both transcriptions and two object classifications (C2, C2k), with unchanged effect sizes but below the strict thresholds after near-duplicate removal (R1).
- A substitution class containing 002 and 090 is absent from copper tablets (H9.4), but the class has no interpretation fixed in advance.
- Tests of object type, motif, site and period against numerals, motifs, name-like slots and chronological variants were negative (H3.5, H4.1, H4.2, C1, H9.2, H10.1, T1). Unused seal and tablet inscriptions, which a confirmation would need, are not available in accessible form (`docs/NEW_DATA_SURVEY.md`).

### L3 — sound values (not achieved; no calibrated route found)

- Under the reading rules of a published Sanskrit decipherment, random sign-value assignments make as many Indus lines readable (84 %) as the published readings (E2, E2b).
- A calibrated search for sign-to-sound assignments under Sanskrit, Old Tamil, Sumerian and Akkadian sound models could not identify the language even of known cuneiform texts hidden as ciphers, in four variants and with up to 8,000 lines (E3–E3d, R3). No language preference is claimed.

### Typology

The Indus corpus is statistically closest to proto-Elamite in both transcriptions (D1, D1-KP); proto-cuneiform is second for the ICIT transcription but farthest for KP1979; its estimated inventory of 510–830 signs is comparable to proto-Elamite (D3). The statistics used cannot separate writing from non-linguistic symbol systems (D2), so whether the signs record a language remains open. One descriptive difference from proto-Elamite is clear: Indus numerals precede the sign they go with (71 % of cases), whereas proto-Elamite entries put the sign before the numeral (NUM1).

### Published claims

All 35 claims of the claims register are evaluated in `docs/CLAIMS_EVALUATION.md`. Among others: the low repetition of signs is a property of the transcription, not of the inscriptions (C9), and repetition rises with text length (C10, CT10); the jar sign is the most frequent sign (C13), has the most diverse left context of all frequent signs in both transcriptions (C14, CT14, CT14k), closes seal legends more than tablet texts (C15, CT15) and does not behave like a unit of measure (C16, CT16); longer texts have a nested structure (C17, C18; CT17, CT18); conditional entropy does not separate writing from non-linguistic systems (C19, CT19); the fish-shaped signs form one usage class (C22, CT22), but numeral + fish star names are not supported (C23); frequent signs combine less freely than in a syllabic script (C27, CT27); stroke counts drop sharply after seven, also without the fixed pairing 7 + 288/289, but the base remains undecided (C25, CT25, CT25b); Mahadevan's "trader" sequence behaves as a fixed three-sign unit plus the jar sign, not as two pairs (C26, CT26); Harappa tablets were made in series while seals are individual, in both transcriptions (C32, CT32a; CT28, CT28k); the published Sanskrit readings are not evidence for the proposed values (C33).

## 4. Assessment

The project achieved L1 in broad scope: the Indus inscriptions follow a consistent, reproducible organisation of short formulae with a right-to-left order, fixed closing signs and a numeral notation tied to particular signs, which holds across sites, transcriptions and later finds. It achieved L2 only in a narrow, functional form (the jar sign as the characteristic closing sign of seal legends) and did not achieve L3. With about two thousand short texts, no bilingual and no unused inscriptions of the relevant kinds, the main obstacle to further progress is the evidence, not the methods: calibrated tests showed that the phonetic methods available cannot identify a language from data of this size, and the meaning candidates could not be confirmed for lack of unused material.

## 5. Errors found and corrected

The journal records every error found during the work, among them: near-duplicate texts across the held-out split (R1), non-deterministic control sets and seeds (R3), a too lenient control (H4.3), an inconsistent sign set (H5.1), insufficient permutation resolution (L3b), a shape measure dominated by outline (G2 robustness), a biased confidence interval (D3), and the withdrawal of an observation that depended on the transcription (repetition).
