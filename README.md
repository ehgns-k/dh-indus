# dh-indus: research repository for the decipherment of the Indus script

This repository records an attempt to analyse the Indus script material with reproducible methods and to attempt a decipherment according to staged success criteria. The research plan and success criteria are in [ROADMAP.md](ROADMAP.md), the working method in [docs/METHOD.md](docs/METHOD.md), and the dated research log in [docs/JOURNAL.md](docs/JOURNAL.md).

## Current status

The Indus script is undeciphered. Results in this repository are labelled with the levels (L1–L4) of [ROADMAP.md](ROADMAP.md) section 2, and `docs/JOURNAL.md` records which level's criteria each result meets.

| Date | Level | Result |
|---|---|---|
| 2026-11-25 | L1 (narrow scope) | Fixed order within the line-final sign cluster, reproduced on held-out data and across find sites (H3.3, H3.4) |
| 2026-11-25 | Not met | The hypothesis that terminal signs mark word boundaries (H3.1) was not supported |
| 2026-11-25 | L1 (narrow scope) | Signs of 4–9 short strokes are followed by one particular sign group (KP 86 / ICIT 390–407) far more often than other signs are; held-out data, both transcriptions (H3.10), robust to matched controls (H3.11), and confirmed on inscriptions from sites excavated after 1979 (F2) |
| 2026-11-25 | Not met | Seal vs tablet texts transfer across sites (H3.5); stroke signs share following contexts (H3.8); 090- vs 400-final lines tied to object type (H3.7) |
| 2026-11-25 | L1 (narrow scope) | Order regularities learned from the 1979 corpus predict later finds from Dholavira and Nausharo, only in the right-to-left reading direction (F3) |
| 2026-11-25 | L1 (gate G1 passed) | A positional template (initial → medial → terminal zones) and a lexicon of recurring sign units, learned from the 1979 corpus, predict inscriptions from ten sites excavated after 1979, against controls that keep all earlier rules (B1, B4) |
| 2026-11-25 | Typology (descriptive) | Among five reference corpora from the CDLI, the Indus corpus is statistically closest to proto-Elamite and proto-cuneiform (proto-administrative systems), not to Sumerian or Akkadian full writing (D1) |
| 2026-11-25 | Undecided (gate G3) | With the non-linguistic corpora of Sproat (2014) added, the statistics used cannot separate writing from non-linguistic symbol systems, so the linguistic status of the Indus signs remains open (D2) |
| 2026-11-25 | L2 candidate (downgraded in review) | The sign that closes a line varies with the kind of object (line-final 407 and 154 on rectangular seals without motif; 400 avoided on motif-bearing seals), consistent in two transcriptions and two object classifications (C2, C2k); after near-duplicate texts were removed from the held-out data, the effect sizes stayed the same but the strict thresholds were not reached (R1) |
| 2026-11-25 | Test of a published claim | Under the normalisation used by the published Sanskrit reading (claim C33), 29 % of random letter strings of the same composition can also be divided into Sanskrit dictionary words (proposed readings: 84 %), so readability alone is weak evidence for that decipherment (E2) |
| 2026-11-25 | Test of a published claim | With the same reading freedoms, random (unfitted) sign-value assignments make 84 % of Indus lines readable as Sanskrit dictionary words, the same rate as the published readings, so readability gives no evidence for that decipherment (E2b) |
| 2026-11-25 | Method test (negative) | Fitting sign-to-sound assignments under sound-sequence models of Sanskrit, Old Tamil, Sumerian and Akkadian cannot identify the language even of known cuneiform texts hidden as ciphers, so no language preference for the Indus inscriptions is claimed (E3, E3b) |
| 2026-11-25 | Method test (negative) | The phonetic search fails on known scripts even with 8,000 lines, so the failure is not a matter of corpus size; no calibrated route to a phonetic decipherment is available with the accessible data (E3c) |
| 2026-11-25 | Review | All L1 held-out results pass again on a strict held-out set without near-duplicate texts (R1) |
| 2026-11-25 | Method test (negative) | With equal amounts of running text for Sanskrit (Ṛgveda), Old Tamil, Sumerian and Akkadian, the phonetic search still cannot identify the language of known texts hidden as ciphers; the Indus ranking is therefore not interpreted (E3d) |
| 2026-11-25 | L1 (with a caveat) | Short-stroke and long-stroke signs take disjoint sets of partner signs at sites excavated after 1979 (H6.1); the result depends largely on one sign (033) whose identity differs between the two transcriptions, so the reading as two numeral notations is only suggested |
| 2026-11-25 | L1 | Signs that are near-variants in shape (a base form with added marks) are used in similar contexts, tested on data not used to notice the pattern, and confirmed with a second, structural shape measure; across all signs, shape does not predict usage, and added marks do not shift position consistently (G1, G2, M1) |
| 2026-11-25 | L1 | Texts that are identical except for the number of strokes in one slot are six to eight times more frequent than chance, in both transcriptions; about half differ by two or more strokes, so they are not misreadings. This fits fixed formulae with a variable quantity (H9.1) |

The full list of tests, including failed ones, is in `docs/JOURNAL.md`.

## Layout

```
ROADMAP.md              research phases, success criteria
docs/METHOD.md          work units, cycle, rules
docs/JOURNAL.md         dated research log
docs/BIBLIOGRAPHY.md    verified bibliography
docs/SIGN_CONCORDANCE.md  sign-number concordance between the two corpora
data/sources.tsv        list of raw sources (pinned commit, SHA-256)
scripts/fetch_data.py   download and verify the raw sources
src/indus/corpus.py     normalise both corpora into lines in reading order
scripts/phase*_*.py     analyses by phase
results/                analysis output (generated by the scripts)
reports/                phase reports and review reports
```

## Reproduction

```bash
pip install -r requirements.txt
python scripts/fetch_data.py
PYTHONPATH=src python scripts/phase2_baseline.py
PYTHONPATH=src python scripts/phase1_concordance.py
PYTHONPATH=src python scripts/phase3_structure.py
PYTHONPATH=src python scripts/phase3_h33_heldout.py
PYTHONPATH=src python scripts/phase3_h34_sites.py
```

## Data sources

The raw data are not included in this repository. `scripts/fetch_data.py` downloads the pinned versions listed in `data/sources.tsv` and checks their checksums.

- ICIT-style secondary transcription: <https://github.com/horus84/Computational_Linguistics> (commit `ac44f08`)
- Machine reading of Koskenniemi & Parpola (1979), *Corpus of Texts in the Indus Script*: <https://github.com/koskenni/indus> (commit `60f6e28`)

Reference corpora for the typology phase come from the CDLI bulk data (<https://github.com/cdli-gh/data>, August 2022), fetched by `scripts/fetch_cdli.py`. Non-linguistic reference corpora come from Sproat (2014) (<https://github.com/rwsproat/non-linguistic-symbols>, Apache License 2.0), fetched by `scripts/fetch_sproat.py`.

The two sources use different sign-numbering systems. Neither replaces the original photographs or a primary concordance.
