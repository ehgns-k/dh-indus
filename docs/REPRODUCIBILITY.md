# Reproducing the results

## 1. Environment

Python 3 with `numpy`, `scipy`, `pandas`, `scikit-learn`, `networkx` and `Pillow` (`pip install -r requirements.txt`; Pillow for the glyph analyses).

## 2. Raw data

None of the raw data are stored in this repository. Each fetch script downloads a pinned version and checks its SHA-256 (or, for the glyph images, a pinned commit):

| Script | Data |
|---|---|
| `scripts/fetch_data.py` | ICIT-style transcription; Koskenniemi & Parpola (1979) machine reading |
| `scripts/fetch_cdli.py` | CDLI bulk transliterations and catalogue (about 240 MB) |
| `scripts/fetch_sproat.py` | non-linguistic symbol corpora of Sproat (2014) |
| `scripts/fetch_mw.py` | Monier-Williams dictionary (Cologne source file) |
| `scripts/fetch_tamil.py` | Sangam Tamil anthologies |
| `scripts/fetch_rgveda.py` | Ṛgveda text layer of the Digital Corpus of Sanskrit |
| `scripts/fetch_glyphs.py` | ICIT-keyed sign images (analysis only; no licence stated upstream) |

## 3. Running everything

```bash
PYTHONPATH=src python scripts/run_all.py
```

The script runs every analysis in dependency order and lists result files that differ from the committed versions. `--skip-heavy` skips the phonetic searches (`phase7_e3*`), which take about an hour together on four cores.

## 4. Determinism

All random choices use fixed seeds. Two sources of run-to-run variation were found and removed in the review passes:
- iteration over Python sets, whose order depends on the per-process hash seed (fixed in the stroke-sign tests; review entry of the first day);
- seeds derived from Python's `hash()` of strings in the phonetic searches, which is randomised per process (replaced by CRC32; review R3), and outputs whose order among tied items was not fixed (now sorted).

The check is to run the scripts twice with different `PYTHONHASHSEED` values and compare the result files byte for byte.
