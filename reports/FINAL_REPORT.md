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
4. Stroke signs of one to ten strokes form a numeral notation: particular counts are followed by particular signs (4–9 strokes → 390–407; 7 → 585/575; three long strokes → 520) in both transcriptions, on strict held-out data and on later finds (H3.10–H3.12, F2, R1, R2); texts that are identical except for the count are six to eight times more frequent than chance, also after normalisation of writing variants (H9.1, R4).
5. Recurring multi-sign units and formulae with variable slots: units learned from the 1979 corpus recur in later finds (B4); signs that substitute for one another form classes (numerals; closing and counted-item signs; fish-shaped signs with single strokes; others) that agree between transcriptions (H9.3); 131 formulae with a variable slot are listed in `docs/FORMULAE.md`. Longer texts have a nested structure: parts obtained by recursive splitting at the weakest link are complete short texts about three times as often as in controls (CT18).
6. Near-variant sign shapes are used alike on unused data (G2), while shape in general does not predict usage (G1) and added marks do not shift position consistently (M1).

### L2 — semantic or functional categories (achieved only in narrow, functional scope)

- **Confirmed (narrow, functional):** the jar sign 740 closes seal texts more often than tablet texts, in every site stratum, in a single pre-registered test on data not used for this question (CT15; odds ratio 4.3, p = 0.0022). What the closing sign means (a genitive, a title, a classifier) is not established. The result passes its own threshold but would not survive a family-wise correction over the eight questions decided on the strict held-out data (0.01/8), so it is not beyond doubt. A replication in KP1979 points the same way but has almost no power (three tablet texts; CT15k, p = 0.21). Tags, objects with seal-type legends never used as a class before, follow the seal pattern (740 final in 14 of 16; tablets 54 %; CT15t, p = 0.0068), although tags come mostly from one site.

Further candidates:

- The closing sign depends on the kind of object (400 avoided on motif seals and favoured on tablets; 407 and 154 on rectangular seals without motif), consistent in both transcriptions and two object classifications (C2, C2k), with unchanged effect sizes but below the strict thresholds after near-duplicate removal (R1).
- A substitution class containing 002 and 090 is absent from copper tablets (H9.4), but the class has no interpretation fixed in advance.
- Tests of object type, motif, site and period against numerals, motifs, name-like slots and chronological variants were negative (H3.5, H4.1, H4.2, C1, H9.2, H10.1, T1). Unused seal and tablet inscriptions, which a confirmation would need, are not available in accessible form (`docs/NEW_DATA_SURVEY.md`).

### L3 — sound values (not achieved; no calibrated route found)

- Under the reading rules of a published Sanskrit decipherment, random sign-value assignments make as many Indus lines readable (84 %) as the published readings (E2, E2b).
- A calibrated search for sign-to-sound assignments under Sanskrit, Old Tamil, Sumerian and Akkadian sound models could not identify the language even of known cuneiform texts hidden as ciphers, in four variants and with up to 8,000 lines (E3–E3d, R3). No language preference is claimed.

### Typology

The Indus corpus is statistically closest to proto-Elamite, then proto-cuneiform, in both transcriptions (D1); its estimated inventory of 510–830 signs is comparable to proto-Elamite (D3). The statistics used cannot separate writing from non-linguistic symbol systems (D2), so whether the signs record a language remains open.

### Published claims

All 35 claims of the claims register are evaluated in `docs/CLAIMS_EVALUATION.md`. Among others: the low repetition of signs is a property of the transcription, not of the inscriptions (C9); the jar sign does not behave like a unit of measure (C16, CT16); numeral + fish star names are not supported (C23); the published Sanskrit readings are not evidence for the proposed values (C33).

## 4. Assessment

The project achieved L1 in broad scope: the Indus inscriptions follow a consistent, reproducible organisation of short formulae with a right-to-left order, fixed closing signs and a numeral notation tied to particular signs, which holds across sites, transcriptions and later finds. It achieved L2 only in a narrow, functional form (the jar sign as the characteristic closing sign of seal legends) and did not achieve L3. With about two thousand short texts, no bilingual and no unused inscriptions of the relevant kinds, the main obstacle to further progress is the evidence, not the methods: calibrated tests showed that the phonetic methods available cannot identify a language from data of this size, and the meaning candidates could not be confirmed for lack of unused material.

## 5. Errors found and corrected

The journal records every error found during the work, among them: near-duplicate texts across the held-out split (R1), non-deterministic control sets and seeds (R3), a too lenient control (H4.3), an inconsistent sign set (H5.1), insufficient permutation resolution (L3b), a shape measure dominated by outline (G2 robustness), a biased confidence interval (D3), and the withdrawal of an observation that depended on the transcription (repetition).
