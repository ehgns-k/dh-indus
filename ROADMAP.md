# Research roadmap: an attempt to decipher the Indus script (2026-11-25 to 2026-12-25)

## 1. Aim and premises

The aim of this project is to analyse the Indus script material systematically and to attempt a partial or full decipherment within the limits of what can be verified. The Indus script is currently undeciphered, and scholars disagree even on whether it records language (bibliography section C: Farmer, Sproat & Witzel 2004; Rao et al. 2009).

The data conditions are as follows. All figures were computed in `results/phase2_baseline.md`.

| Item | ICIT-style transcription | Koskenniemi & Parpola 1979 |
|---|---:|---:|
| Complete, deduplicated lines | 2,059 | 2,123 |
| Sign types | 607 | 367 |
| Signs occurring once | 214 | 100 |
| Median line length | 4 | 4 |

The texts are short, no bilingual text is known, and about one third of the signs occur only once. A phonetic decipherment is therefore likely to fail, and this is taken as a premise from the start. For this reason the success criteria below are divided into levels.

## 2. Success criteria (pre-registered)

The criteria are written down before the analyses so that they cannot be changed after seeing the results. A level can be claimed only if the criteria of the levels below it are met.

| Level | Name | Conditions |
|---|---|---|
| L1 | Structural partial decipherment | A structural result (sign classes, segmentation into word-like units, function of terminal signs, etc.) is (a) reproduced independently in both corpora and (b) explains the data significantly better than a random control model (p < 0.01). |
| L2 | Partial decipherment of semantic categories | A semantic category (numeral, title, commodity, place name, etc.) is assigned to particular signs or sign sequences, and the assignment predicts information outside the text (object type, iconography, find site) on held-out data. |
| L3 | Partial phonetic decipherment | Under a specific language hypothesis, sound values are assigned to some signs, and the resulting system predicts held-out data significantly better than the same procedure applied to other (control) languages. The false-positive rate is measured by control experiments and reported alongside. |
| L4 | Full decipherment | Most of the corpus is read consistently, and the readings agree with independent evidence (for example proper names in external texts). Not expected within this period. |

The word "deciphered" is used only at L3 or above. L1 and L2 results are called "structural results" and "semantic-category hypotheses".

## 3. Plan by phase

| Phase | Period (planned) | Content | Outputs |
|---|---|---|---|
| 0. Setup | Day 1 | Repository layout, success criteria, working rules | `ROADMAP.md`, `docs/METHOD.md` |
| 1. Data collection | Days 1–3 | Obtain public corpora, record pinned versions and checksums, normalise, build a sign-number concordance between the two corpora | `data/sources.tsv`, `src/indus/corpus.py`, `docs/SIGN_CONCORDANCE.md` |
| 2. Bibliography | Days 1–5 | Verified bibliography; register of earlier claims, each converted into a testable form | `docs/BIBLIOGRAPHY.md`, `docs/CLAIMS_REGISTER.md` |
| 3. Structural analysis | Days 3–10 | Positional distributions, segmentation, distributional sign clustering, allograph merging, numeral system, correlation with iconography and object type | `results/phase3_*` |
| 4. Script typology | Days 8–15 | Compare sign inventory and distributions with known logographic, syllabic and non-linguistic systems; design control models | `results/phase4_*` |
| 5. Language hypotheses | Days 12–22 | Constrained search under Proto-Dravidian, Indo-Aryan, Munda and unknown-language hypotheses; measure false-positive rates with control languages | `results/phase5_*` |
| 6. Falsification and cross-validation | Days 18–28 | Apply pre-registered predictions to held-out data; an independent review unit tries to refute the results | `reports/REVIEW_*.md` |
| 7. Synthesis | Days 28–30 | Report results against the success criteria, including failed approaches | `reports/FINAL_REPORT.md` |

Phases may overlap. Progress is recorded by date in `docs/JOURNAL.md`.

## 4. Approaches to be tried

Each approach is recorded even when the result is negative. A failed approach is also a result.

1. Positional distribution and segmentation: signs that prefer initial or final position; estimation of word-like units by boundary entropy.
2. Distributional semantics: represent signs by their left and right contexts, cluster them, and look for allograph candidates and functional classes.
3. Numeral system: repetition patterns of stroke signs, position of quantity markers, comparison with weights and measures.
4. Correlation with external information: animal iconography, object type (seal, incised tablet, pottery inscription), and sign distribution by find site.
5. Script typology: compare sign inventory size, frequency distribution and repetition structure with known writing systems and non-linguistic symbol systems.
6. Constrained phonetic search: use syllable structure and phoneme distributions of each candidate language as priors, and apply the same procedure to control languages.
7. Rebus hypotheses: convert previously proposed picture–sound correspondences (for example the fish sign) into pre-registered predictions and test them.
8. External proper names: examine possible correspondences with names connected with the Indus region in Mesopotamian texts.
