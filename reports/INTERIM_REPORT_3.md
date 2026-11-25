# Interim report 3 (2026-11-25, evening)

This report summarises the work since interim report 2. Details and pre-registrations are in `docs/JOURNAL.md`; data use in `docs/DATA_LEDGER.md`; claim verdicts in `docs/CLAIMS_EVALUATION.md`.

## 1. New structural results (L1)

| Test | Result |
|---|---|
| H9.1, R4 | Texts identical except for the stroke count are six to eight times more frequent than chance in both transcriptions, also after normalising short/long variants and split strokes |
| H9.3 | Classes of mutually substituting signs agree between the transcriptions (ARI 0.169, p = 0.0001) |
| CT17, CT18 | Longer texts can be divided into complete short texts more often than controls (weak form), and recursive splitting at the weakest link yields complete short texts three times as often as controls (both transcriptions) |
| CT10 | Within-line repetition rises with text length |
| G2 (with structural shape measure) | Near-variant shapes are used alike on unused data |

## 2. Function and meaning (L2)

| Test | Result |
|---|---|
| CT15 | The jar sign 740 closes seal legends more often than tablet texts, in every site stratum, on data not used for the question (OR 4.3, p = 0.0022); not beyond a family-wise correction over the questions decided on the same held-out data |
| CT15t | Tags (seal-type legends, mostly Lothal) follow the seal pattern (14 of 16 final; tablets 54 %; p = 0.0068) |
| CT15k | Replication in KP1979: same direction, no power (three tablet texts) |
| CT15s | Too few stamped pots; incised pottery also ends in 740 (11 of 12) — tablets are the class that stands apart |
| CT28 | Seal legends are individual-specific: their stems are far more diverse than tablet stems at both main sites |
| CT16 | The jar sign does not co-occur with numerals (opposite of the unit-of-measure claim) |
| H9.2, H9.4, H10.1, T1 | Count-variable formulae are not tied to tablets; one sign class avoids copper tablets (candidate); name-like slot fillers are not more site-specific; no chronological variants detected |

The project's L2 status is therefore "narrow and functional": the closing sign distinguishes seal-type legends from tablet texts, and seal legends are individual-specific. No sign has been assigned a meaning.

## 3. Published claims

All 35 claims are now evaluated. New verdicts in this period: C26 (the "trader" sequence behaves as a fixed three-sign unit plus the closing jar sign, not as two pairs; not supported), C3 (mirror pairs consistent with allographs, low power), C18 (recursive structure supported), C15 (closing function supported, genitive reading untestable), C16 (not supported), C10 (supported), C28 (seal legends individual-specific; undecided between names and other readings).

## 4. Phonetic decipherment (L3)

Unchanged: no calibrated route. The phonetic searches were made deterministic (R3); their run-to-run variation before that change is itself evidence that their rankings carry no information.

## 5. Reproducibility

`scripts/run_all.py` re-runs all analyses; with a different hash seed the 74 non-phonetic analyses reproduce every committed result file exactly (R5), and the phonetic searches give byte-identical results under different hash seeds (R3).
