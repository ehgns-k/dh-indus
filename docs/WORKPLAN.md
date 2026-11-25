# Work plan (from 2026-11-25 to 2026-12-25)

This plan breaks the phases of `ROADMAP.md` into work packages with inputs, methods, outputs and decision gates. It is revised when a gate is reached; revisions are recorded in `docs/JOURNAL.md`.

## 1. Position at the start of the plan

| Level | Status |
|---|---|
| L1 structural | Met in narrow scope: terminal-cluster order (H3.3, H3.4); count–item pairing (H3.10–H3.12, fresh-data F2); shared order and reading direction on post-1979 finds (F3) |
| L2 semantic categories | Not met. Tested so far without success: object type (H3.5, H3.7, H4.1), seal motif (H4.2) |
| L3 phonetic | Not attempted |

Constraints found so far:
1. **Data volume.** About 2,100 unique complete lines per corpus; median length 4.
2. **Held-out depletion.** The 20 % held-out set has been used for several questions. Every new question that uses it is logged in `docs/DATA_LEDGER.md`, and the number of held-out tests is reported with every result.
3. **Fresh data.** Only 93 strings from two post-1979 sites (Dholavira, Nausharo) are usable so far.
4. **Undecoded metadata.** KP1979 type and icon codes refer to tables of the 1973 concordance (KP1979, §6.3–6.4), which is not available here. Only ICIT metadata are decoded.
5. **Network.** Full texts of most publications cannot be opened from the working environment; literature claims rest on abstracts and excerpts.
6. **Controls.** Controls must preserve every structural rule already established (lesson from H4.3).

## 2. Work packages

### WP-A Infrastructure and data integrity (continuous; main work days 2–4)

| Task | Method | Output | Done when |
|---|---|---|---|
| A1 Data-use ledger | List every test with the split it used | `docs/DATA_LEDGER.md` | All tests so far are listed |
| A2 Rule-preserving controls | Shared generator of control texts that keeps line length, the final sign, the terminal cluster and the count–item bigrams, and permutes only the rest | `src/indus/controls.py` | Used by every new test |
| A3 More fresh data | Confirm excavation dates of further post-1979 sites (Farmana, Kanmer, Bhirrana, Khirsara, Gola Dhoro, Rakhigarhi) from sources | Extended fresh set | Each site has a cited start date or is excluded |
| A4 Object-level link | Match KP1979 inscriptions to ICIT records (CISI numbers, text alignment, site) | Link table | ≥ 80 % of aligned KP lines linked to one record |

### WP-B Structural grammar: consolidate L1 (days 2–8)

| Task | Question | Test data |
|---|---|---|
| B1 Positional template | Can a line be described as initial zone + medial zone + terminal cluster, with sign classes tied to zones? | Built on KP training; tested on ICIT held-out and fresh set, by log-loss against a bigram model |
| B2 Numeral system | Full table of counts × following signs; short vs long strokes; is any count above 9 written as one sign (base question, claim C25)? | Descriptive on all data; tests on fresh set |
| B3 Allographs | Do signs that one list splits and the other merges (concordance) behave as one sign distributionally? | Training split |
| B4 Recurring units | Minimum-description-length segmentation; do the units recur at post-1979 sites? | Fresh set |

Gate G1 (day 8): L1 is consolidated if B1 or B4 gives a description that predicts fresh data better than the bigram baseline. If neither does, the L1 claim stays at the narrow results above.

### WP-C External correlates: route to L2 (days 3–14)

| Task | External variable | Notes |
|---|---|---|
| C1 Copper tablets | Motif on copper tablets (`TAB:C`) | Many copper tablets share text and motif; the test must use distinct texts only |
| C2 Material and size | Material; seal size (ICIT mm fields) | Site-stratified |
| C3 Count–item group | Does the KP 86 / ICIT 390–407 group, or the count–item construction, favour particular object types or materials? | Pre-registered; site-stratified |
| C4 Regional variation | Sign and construction frequencies by region | Uses all sites with ≥ 30 lines |

Gate G2 (L2 claim): a sign or sign group is assigned a semantic category, and a pre-registered prediction about an external variable succeeds on data not used to form the hypothesis (held-out or fresh), with site control, at p < 0.01 after correction for the number of L2 tests. If G2 is not met by day 14, L2 is reported as not achieved and the remaining time goes to WP-D and WP-E as conditional analyses.

### WP-D Script typology (days 8–16)

| Task | Method |
|---|---|
| D1 Synthetic baselines | Rule-preserving generators (A2) at several levels of structure; measure which statistics separate the real corpus from each |
| D2 Reference systems | Obtain comparison corpora (known logo-syllabic scripts, non-linguistic symbol systems) if accessible; otherwise D1 only |
| D3 Specificity | For each statistic, estimate how often a non-linguistic system would pass it (following the caution of Raghavendra 2026, bibliography section D) |

Gate G3: if no statistic separates linguistic from non-linguistic systems with a measured false-positive rate below 0.1, the question "is it writing?" is reported as undecided, and WP-E results are labelled conditional on the linguistic assumption.

### WP-E Language hypotheses: L3 attempts (days 14–24)

| Task | Method |
|---|---|
| E1 Lexical resources | Check access to digital lexicons (Proto-Dravidian, Vedic/Indo-Aryan, Munda) |
| E2 Proposal testing | Turn published readings (Parpola, Mahadevan, the Sanskrit claim C33) into predictions about sign distributions, and test them on fresh data |
| E3 Constrained mapping | Map recurring units (B4) to lexicon items under constraints from the structural results (count–item construction, terminal cluster); evaluate on held-out/fresh data against control lexicons with matched phonotactics and unrelated languages |

Gate G4 (L3 claim): only if the pre-registered held-out fit beats every control language at p < 0.01 and the false-positive rate of the procedure has been measured. Otherwise the outcome is reported as "no phonetic decipherment supported".

### WP-F Review and reporting (continuous; days 26–30)

- F1: after every working session, check new results for leakage, lenient controls and multiple comparisons; record findings in the journal.
- F2: phase reports in `reports/`.
- F3: final report against the success criteria, including all failed tests (days 28–30).

## 3. Schedule

| Days | Main packages |
|---|---|
| 1 (done) | Setup, data, concordance, phase 3 tests, fresh-data tests |
| 2–4 | A1–A3, C1, B2 |
| 4–8 | B1, B3, B4, A4, C2–C3; gate G1 |
| 8–14 | C3–C4, D1; gate G2 |
| 14–16 | D2–D3; gate G3 |
| 14–24 | E1–E3; gate G4 |
| 24–30 | F2–F3 |

Each scheduled working session takes the earliest unfinished task whose inputs are ready, records a pre-registration before every test, and ends with a commit.

## 4. Priority list (revised 2026-11-25, after gates G1–G3)

G1 passed, G2 not met, G3 undecided. The remaining time is ordered by expected value for the success criteria:

| Priority | Task | Package | Why now | Decision data |
|---|---|---|---|---|
| P1 | Systematic sign × metadata association scan (object subtype, material, motif, site region): discovery with false-discovery-rate control on the training split, confirmation of the top associations on the held-out split | C2–C4 | The only route to L2 with the metadata available | train → held-out |
| P2 | False-positive test of the published Sanskrit reading (claim C33): with the proposal's own sign values, normalisation rules and dictionary, how often do random sign-value mappings also give "readable" texts? | E2 | A public decipherment claim that can be tested directly; result informs G4 methodology | all strings (the claim covers the whole corpus) |
| P3 | Structural analogy with proto-Elamite entries ("item , number"): does the Indus count–item construction occupy the same place in the line as proto-Elamite numerals, and do lines with counts have the proto-Elamite entry shape? | C/D | D1 placed the Indus corpus next to proto-Elamite | ICIT training; confirmation on fresh sets |
| P4 | Conditional constrained mapping (WP-E3) under candidate languages, with control lexicons | E3 | Required by the plan; expected to be negative | held-out/fresh |
| P5 | Phase reports and final report | F | Days 26–30 | – |

Each scheduled session takes the highest unfinished priority.
