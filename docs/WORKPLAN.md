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

Gate G4 (L3 claim): only if the pre-registered held-out fit beats every control language at p < 0.01 and the false-positive rate of the procedure has been measured. Added after E2b: the acceptance criterion must have a rate below 0.1 under random sign-value assignments with the same reading freedoms. Otherwise the outcome is reported as "no phonetic decipherment supported".

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

### Additions to the priority list (eleventh working session)

| Priority | Task | Idea |
|---|---|---|
| P4a | E3 calibrated phonetic-assignment search | fit sign-to-sound assignments under each candidate language and compare held-out gains; positive controls with hidden known scripts (running) |
| P4b | E4 family coherence | if an assignment is right, graphic variants of one sign (for example the fish family KP 48–63, the stroke series) should receive related values; test the fitted E3 assignments for coherence within families against random assignments, as a check independent of the language model |
| P4c | E5 boundary-aware fitting | use the established structure (terminal cluster, count–item pairs, recurring units) to cut lines into word-like units before fitting, and repeat E3; tests whether structure improves the phonetic signal |
| P4d | E6 logographic alternative | instead of syllables, assign words (whole lexical items) to frequent signs and test held-out gains, to compare logographic and syllabic readings under the same calibration |

### Revision after E3 and E3b (eleventh working session)

Unconstrained phonetic fitting has no power on a corpus of this size (E3, E3b). The remaining L3 routes require an independent constraint, fixed before any fitting:

| Priority | Task | Constraint |
|---|---|---|
| P4e | Rebus-constrained fitting | values of pictographic signs restricted, before fitting, to words for the depicted object in each candidate language (from the sign drawings and a fixed word list); calibrated with the same positive-control design |
| P4f | External names | test whether any recurring Indus unit can be matched to names associated with the Indus region in external (Mesopotamian) sources under a pre-registered rule, with the E2b random-assignment calibration |
| P4b–P4d | as listed above | E4–E6 are kept but are lower priority, because they share the weakness of E3 |

### Revision after E3c (twelfth working session)

WP-E is closed: no calibrated route to L3 is available with the accessible data (E3, E3b, E3c; assessment of P4e and P4f in the journal). Revised priorities for the remaining time:

| Priority | Task |
|---|---|
| Q1 | Extend the functional L2 result: which signs immediately before the closing sign vary with object class; whether the count–item construction differs by object class (site-stratified, discovery on train, confirmation on held-out or fresh data) |
| Q2 | Sign classes: combine positional zones, concordance families and the C2 associations into one documented sign classification (descriptive), with a reproducibility check across the two transcriptions |
| Q3 | Review pass (WP-F1) over all supported results: leakage, controls, multiple comparisons |
| Q4 | Phase reports and the final report |

## 5. Long-horizon agenda (added 2026-11-25, thirteenth session)

The short tests that the current data allow have largely been run. The remaining weeks are planned as larger, multi-session projects, each with its own pre-registrations. Scheduled sessions work through them in this order and may run several hours of computation per session.

| Order | Project | Goal | First steps |
|---|---|---|---|
| L-1 | **Numeral system** | Describe and test the stroke notation as fully as the data allow: counts per series; partner signs per count; whether counts combine (for example two stroke signs in a row); the base question (claim C25); comparison with the numerical systems of proto-cuneiform and proto-Elamite in the CDLI data under the same tokenisation | descriptive tables on training data; pre-registered tests on strict held-out and fresh data |
| L-2 | **Glyph-shape data** | Obtain sign images or shape descriptions (sign-list scans, open image datasets of Indus signs) and build shape features, so that pictographic and allograph questions can be asked with an independent source of information | survey of open image datasets; extraction from the KP1979 sign-list scans |
| L-3 | **Allographs** | Use the two transcriptions' disagreements (concordance splits and merges) and shape features (L-2) to propose and test allograph groups; re-run key L1 tests with merged groups | from `docs/SIGN_CONCORDANCE.md` |
| L-4 | **New data watch** | Search for inscriptions published after the ICIT-style source (excavation reports, open datasets) to obtain unused data for confirming the L2 candidate | sourced list of new finds |
| L-5 | **Reports** | Phase reports for phases 3–7 and the final report, written so that every claim cites the test and data behind it | from interim report 2 |

### Progress and additions (fourteenth session)

- L-1: split/merge of strokes found (KP 121/144 pairs = ICIT 032); numeral partner results reviewed (R2; H6.1 depends on 033).
- L-2: glyph images obtained (726 ICIT signs); G1 negative, G2 positive (near-variant shapes share usage).
- L-3: allograph tests L3a/L3b done.
- New items:
  - **L-2b Modifiers.** Using the mayig feature coding (Parpola signs with feature vectors) or shape differences, identify recurring modifications (added strokes above, enclosure, crossing) and test whether a modification shifts usage in the same direction across different base signs (diacritic-like behaviour). Discovery on training data, confirmation on strict held-out and fresh data.
  - **L-3b Combined inventory.** A sign list that keeps every distinction supported by usage in either transcription (L3a, L3b), with a mapping from both numberings; rerun key L1 tests on it.

### Progress and additions (twenty-fourth session)

- L-1: numeral order compared with proto-Elamite and proto-cuneiform (NUM1); no fixed order of long and short strokes (NUM2); numeral faces of two-face Harappa tablets (FACE2, FACE3).
- L-3b: combined inventory done (`docs/COMBINED_INVENTORY.md`).
- Review: family-wise review of all tests on unused data (R7, R7b); all analyses re-run (`scripts/run_all.py`).
- New external variable: object size (SZ1–SZ4). No sign predicts seal size on unused data.
- New items:
  - **L-6 Chronology at Mohenjo-daro** (first test T2 done in this session: no change detected). The source gives Early / Intermediate / Late levels for about 800 Mohenjo-daro records (`period`) and depths. Use them as an external variable (discovery on training strings, confirmation on strict held-out), after checking how the levels were assigned.
  - **L-7 `cult` codes.** The `cult` column (SAN, Trough, SAF, RAN …; 1,457 records) is undocumented. Survey its meaning before any use.
  - **L-8 Numeral faces.** Check against the CISI 3.1 photographs whether the counts on the numeral faces were read correctly, if the volumes become accessible.

### Revision after the fortieth session (2026-11-26)

- Work package E (phonetic route) is closed (E3–E3zd). The data and methods available here give no information about the language of the inscriptions, and the requirement for any future attempt is stated in `docs/FUTURE_DATA.md`.
- The external variables of the source have been tried (object type, motif and its details, material, size, level, excavation area), as have all accessible unused sets (strict held-out, fresh sites, unknown-direction lines).
- Remaining priorities:
  - **F1. Final report.** Rewrite `reports/FINAL_REPORT.md` as a consolidated text rather than a living draft, with one section per level and a table of every decisive test.
  - **F2. Full reproducibility.** Run `scripts/run_all.py` without `--skip-heavy`, i.e. all phonetic experiments included, and record differences.
  - **F3. Literature checks.** Retry the sources that could not be reached (CISI 3.1, Wells 2011, ICIT documentation) if access becomes possible, and correct the code meanings in `docs/OBJECT_CODES.md`.
  - **F4. New data watch.** Repeat the survey of newly published inscriptions (`docs/NEW_DATA_SURVEY.md`) once a week. Any new, unused inscriptions would allow the confirmatory tests planned in `docs/FUTURE_DATA.md`.

## Revision of 2026-11-28: maintenance mode

From 2026-11-28 the work runs once a week and covers only F3 (literature retry), F4 (new-data watch) and the upkeep of the reports. No new hypothesis test is registered on the data already used. If new, unused inscriptions become accessible, the confirmatory tests in `docs/FUTURE_DATA.md` are registered and run. The final report is completed after 2026-12-25.
