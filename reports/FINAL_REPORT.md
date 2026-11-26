# Final report: an attempt to decipher the Indus script

Status: 2026-11-26 (consolidated version; it will be revised if further work changes any result before 2026-12-25). Every result cited here is documented with its pre-registration in `docs/JOURNAL.md`. The data used for each decision are listed in `docs/DATA_LEDGER.md`, and detailed phase reports are in `reports/`.

## Summary

The project tested, with pre-registered and reproducible analyses, how far the Indus inscriptions can be deciphered from the accessible evidence. Success was defined in advance in four levels.

- **L1 (structure): achieved.** The inscriptions follow a consistent organisation that holds across transcriptions, sites, object classes and later excavations:
  - a right-to-left reading order;
  - a positional template with a closing cluster of fixed internal order;
  - a stroke numeral notation tied to particular counted signs;
  - recurring units and formulae with variable slots;
  - a nested structure of longer texts.
- **L2 (function): achieved only in a narrow form.** The jar sign 740 closes seal legends more often than tablet texts, on data not used for the question (odds ratio 4.3, bootstrap interval 1.5–16). What the sign means is not established. Further associations between signs and objects remain candidates; confirming them would need several hundred to several thousand new inscriptions.
- **L3 (sound values): not achieved.** Phonetic fitting cannot identify even known languages hidden as ciphers unless 25–35 frequent sign values are known in advance. No Indus sign value is known independently.
- **Writing or not: undecided.** The Indus corpus is statistically closest to proto-Elamite, but no statistic tried separates writing from non-linguistic symbol systems.

## 1. Aim and success criteria

`ROADMAP.md` defined four levels before any analysis:
- L1: structural results that hold on data not used to find them.
- L2: semantic or functional categories that predict information outside the texts.
- L3: sound values that predict unseen texts better than control languages.
- L4: full decipherment.

## 2. Material and method

**Transcriptions.**
- An ICIT-style secondary transcription (5,679 records), with object type, site, motif, dimensions and other fields.
- The machine reading of Koskenniemi & Parpola (1979; 4,066 inscriptions).
- The two are linked by a sign concordance estimated from 929 aligned texts (`docs/SIGN_CONCORDANCE.md`).

**Unused test data.**
- A strict held-out split of the strings, with no training string within edit distance 1.
- 117 lines from ten sites first excavated after 1979 (fresh sets).
- The second transcription, for replication.
- A set of 64 strings of unknown writing direction.
- All decisions on these sets were reviewed together for multiple testing (R7).

**Reference material.**
- CDLI corpora: proto-Elamite, proto-cuneiform, Sumerian and Akkadian.
- Non-linguistic symbol systems (Sproat 2014).
- Word data in Sanskrit (Ṛgveda; Monier-Williams), Old Tamil (Sangam), Sumerian and Akkadian.
- Sign images keyed to the ICIT numbers.

**Rules.**
- Every test was pre-registered in the journal.
- Controls preserve every rule already established.
- Permutation counts allow p-values one tenth of the threshold.
- All scripts are deterministic and re-run by `scripts/run_all.py`; reproducibility checks R3, R5, R8 and R9 found no differences.

## 3. L1 — structure (achieved)

| Result | Main tests |
|---|---|
| Reading order right to left; order regularities predict later finds, the two main sites when left out, and lines written left to right once mirrored | F3, F3b, SX1, DIR1, DIR2 |
| Positional template (initial, medial, closing zones), reproduced across transcriptions, on later finds, when each main site is left out, and on tags, bangles and other objects | Q2a, B1, SX3, PT2, PT2k |
| Closing cluster with fixed internal order (740 before 400 or 090), in every object class and both transcriptions | H3.3, H3.4, R1, H3.3c, H3.3ck |
| Stroke numerals with count-specific partner signs (4–9 strokes → 390–407; 7 → 585/575; three long strokes → 520), on strict held-out data, later finds and other objects, in both transcriptions | H3.10–H3.12, R1, R2, F2, H6.1, PT3, PT3k, H3.10c |
| Texts identical except for the count: six to eight times more frequent than chance | H9.1, R4 |
| Recurring units and formulae with variable slots, reproduced across transcriptions and in later finds | B4, SX4, KF1, F5, F5k, U3; `docs/FORMULAE.md`, `docs/FORMULAE_KP.md` |
| Substitution classes agreeing between transcriptions; the fish-shaped signs form one usage class | H9.3, R6, CT22, CT22k, CT22b |
| Nested structure: parts of long texts recur as complete short texts | CT17, CT18, CT18c |
| Near-variant sign shapes used alike | G2 |
| Lines and faces of one object form one text, closed once; line breaks fall where space ends | ML1, ML1k, FACE1, FACE4, ML2 |
| Numeral faces of Harappa tablets (two to four strokes with sign 700); identical texts tend to share the count, which still varies within a series | FACE2, NUM3 |

In the family-wise review over 49 tests decided on unused data, 14 survive a Holm correction at α = 0.01 (R7). They cover:
- the direction test;
- the closing-cluster order;
- the count–item pairs;
- the positional template;
- the recurring units;
- the nested structure.

Not supported or undecided:
- a fixed order of long and short strokes (NUM2);
- the template on the unknown-direction set, whose direction is uncertain (U2);
- the three-face result in KP1979 (FACE4k).

## 4. L2 — functional categories (narrow)

**Confirmed (narrow).** The jar sign 740 closes seal texts more often than tablet texts at Harappa and Mohenjo-daro, on strict held-out and fresh data not used for this question (CT15: Mantel–Haenszel odds ratio 4.3, p = 0.0022).
- Robustness:
  - not a length effect (CT15r);
  - bootstrap 95 % interval 1.5–16 (CT15b);
  - tags follow the seal pattern (CT15t);
  - incised pottery that contains 740 also ends in it (CT15s).
- Limits:
  - it survives Holm at α = 0.05 but not at α = 0.01 over 49 tests (R7);
  - the KP1979 replication has almost no power (CT15k).
- What the closing sign means (a genitive, a title, a classifier) cannot be tested with these data.

**Related functional findings.**
- Seal legends are individual, while tablet texts repeat in series. This holds in both transcriptions and without the numeral faces (CT28, CT28k, CT28n, CT32a, CT32k).
- The individuality of seals lies in combinations of common signs, not in rare signs (CT28h, CT28hk).

**Candidates not confirmed.**
- The closing sign varies with the kind of object (C2, C2k).
- A sign class is absent from copper tablets (H9.4).
- Seals and tablets share fewer formula frames than chance in ICIT only (KF2, KF2k).
- The lead "405 on unicorn seals of variant W" (MO2b).

**External variables with no confirmed association** on unused data: motif and its details (H4.2, MO2a, MO2b, MO1k); object size (SZ2, SZ4); chronological level (T1, T2); excavation area (AR1, AR1h); manufacture technique of tablets (FACE5); site (SX2, H10.1).

**Data requirement.** Power simulations show that confirming the candidates would need 400–1,600 new inscriptions of the right kinds at the observed effect sizes, and up to several thousand at halved effects (PW1–PW4; `docs/FUTURE_DATA.md`). No such unused material is accessible (`docs/NEW_DATA_SURVEY.md`).

## 5. L3 — sound values (not achieved)

- **Published reading.** Under the reading freedoms of a published Sanskrit decipherment, random sign-value assignments make 84 % of Indus lines readable, as many as the published readings (E2, E2b).
- **Phonetic search.** Twenty-four experiments (E3–E3zd) tested a calibrated search for sign-to-sound assignments, using positive controls in which known texts were hidden as ciphers. Results:
  - The scoring identifies the true language when the true assignment is given (E3g).
  - Without known values, the search fails for every cipher tried: Akkadian, Sumerian, Sanskrit and Old Tamil, from 1,000 to 16,000 lines. It favours one model whatever the input: Sanskrit under the reorder-corrected measure, Akkadian under the raw measure (E3–E3h, E3y).
  - The bias persists with other Sanskrit models, fewer candidates, fewer fitted signs and more search effort (E3i–E3x).
  - Calibration against other languages removes the bias but does not reveal the true language (E3za–E3zc).
  - Reliable identification at the size of the Indus corpus needs 25 (Sanskrit) to 35 (Old Tamil) correct values among the 100 most frequent signs, known in advance (E3m–E3v).
- **Consequence.** No Indus sign value is known independently. No statement about the language of the inscriptions can be derived from phonetic fitting. This applies equally to published decipherments that rely on unconstrained fitting.

## 6. Typology and the question of writing

- **Nearest reference system.** The Indus corpus is statistically nearest to proto-Elamite in both transcriptions (D1, D1-KP). Its estimated inventory of 510–830 signs is comparable (D3).
- **A difference from proto-Elamite.** The numeral precedes the sign it goes with (71 %), the reverse of the proto-Elamite order (NUM1).
- **Combination and order measures.**
  - Frequent signs combine less freely than syllabic graphemes (CT27).
  - Where this places the corpus among the reference systems depends on the transcription (D7).
  - In order rigidity, positional rigidity and rank–frequency shape the corpus lies within the reference range (D8–D10).
- **Writing or not.** No statistic tried separates writing from non-linguistic systems (D2, D2b, CT19), so whether the signs record a language remains open.
- **Transcription-dependent measures.** The repetition measure depends on the transcription (C9). The low repetition reported for the ICIT transcription is not a property of the inscriptions.

## 7. Published claims

All 35 claims of the claims register are evaluated in `docs/CLAIMS_EVALUATION.md`.
- Supported, or supported in their distributional part, among others:
  - direction from initial/final asymmetry and positional zones (C2, C12), with the right-to-left crowding claim consistent but not measured (C1);
  - the jar sign as the most frequent sign with the most diverse left context (C13, C14);
  - nested structure (C17, C18);
  - the fish signs as one class (C22);
  - stroke numerals (C24);
  - sparse combination (C27);
  - tablets made in series (C32).
- Not supported, among others:
  - the sign repetition argument (C9);
  - the jar sign as a unit of measure (C16);
  - the conditional-entropy argument for language (C19);
  - numeral + fish star names (C23);
  - Mahadevan's "trader" sequence as two pairs (C26);
  - published Sanskrit readings as evidence (C33).
- Readings of individual signs (C14, C15, C22) cannot be tested.

## 8. Assessment

The Indus inscriptions have a rich, consistent and reproducible structure. They are short formulae read right to left, closed by a small set of signs in fixed order, often containing counts tied to particular signs, and built from recurring units. This structure holds across the two transcriptions, the sites, the object classes and the finds made after 1979.

Beyond structure, the evidence supports one narrow functional result: the jar sign as the characteristic closing sign of seal legends. It does not support sound values. The obstacle is the evidence, not the methods:
- about two thousand short texts;
- no bilingual;
- no independently known sign value;
- no accessible unused inscriptions of the kinds needed.

Calibrated tests showed that the phonetic methods available cannot identify a language under these conditions. Confirming the functional candidates would need more inscriptions than the present corpus contains.

## 9. Errors found and corrected

The journal records every error found during the work, among them:
- near-duplicate texts across the held-out split (R1);
- non-deterministic control sets and seeds (R3);
- a too lenient control (H4.3);
- an inconsistent sign set (H5.1);
- insufficient permutation resolution (L3b, R7b);
- a shape measure dominated by outline (G2 robustness);
- a biased confidence interval (D3);
- the withdrawal of observations that depended on the transcription (repetition) or on the size of a vocabulary (D6);
- an ambiguous registration (AR1);
- an overstatement about H9.4 corrected when the review family grew (R7).
