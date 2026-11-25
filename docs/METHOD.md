# Working method and workflow

## 1. Work units

The research is divided into six work units that can proceed independently. Each unit takes defined inputs and leaves defined outputs. Several units may run at the same time.

| Unit | Input | Output | Notes |
|---|---|---|---|
| A. Data | Public corpora | `data/sources.tsv`, `src/indus/corpus.py`, concordance | Raw data are not committed; they are downloaded at pinned versions |
| B. Literature | Scholarly databases, publisher records | `docs/BIBLIOGRAPHY.md`, `docs/CLAIMS_REGISTER.md` | Every entry records how it was verified |
| C. Structure | Normalised data from A | `results/phase3_*` | Results must replicate in both corpora |
| D. Typology | A, C | `results/phase4_*` | Control models are required |
| E. Language hypotheses | A, C, claims register from B | `results/phase5_*` | A control-language experiment is required for each hypothesis |
| F. Review | Results of the other units | `reports/REVIEW_*.md` | Its only role is to try to refute results |

## 2. Cycle

Each working session follows these steps.

1. Read the last entry of `docs/JOURNAL.md` and `ROADMAP.md`, and decide the next task.
2. Write the hypothesis in `docs/JOURNAL.md` first, together with the result it predicts if it is true.
3. Write the analysis script in `scripts/` and run it. Results are generated automatically in `results/`.
4. Compare the result with the prediction and record it. If they differ, say so.
5. The review unit (F) checks for missing controls, data leakage, multiple comparisons and similar problems.
6. Commit the changes and push them to the remote repository.

## 3. Rules

- Raw data: used only at a pinned commit with SHA-256 checksum (`scripts/fetch_data.py`).
- Reading order: all normalised data are stored in reading order. See the `docs/JOURNAL.md` entry of 2026-11-25 for the evidence.
- Duplicates: the same string often appears on several objects (for example several impressions of one seal), so frequency statistics are computed by default on deduplicated lines.
- Leakage: decipherment proposals contained in the raw data (for example the `sanskrit` and `translation` columns of the ICIT-style transcription) are never used.
- Held-out data: the held-out set used for prediction tests from phase 3 onward is fixed in advance and is not inspected while hypotheses are formed.
- Multiple comparisons: when several hypotheses are tested, their number is recorded and corrected for.
- Citation: factual claims from the literature cite an entry of `docs/BIBLIOGRAPHY.md`. Claims for which no source can be found are not written.

- Permutation tests: the number of permutations is chosen so that the smallest attainable p-value is at most one tenth of the decision threshold (added after L3b).
- Held-out tests use the strict held-out set without near-duplicates (added after R1).
- **Rules and examples in registrations (added after AR1).** Where a registration gives both a rule and examples, the examples are checked against the rule before the registration is committed. If they still disagree, the rule takes precedence, and the analysis is also run with the examples' reading; the result counts as supported only if both readings pass.
