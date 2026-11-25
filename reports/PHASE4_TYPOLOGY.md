# Phase 4 report: what kind of system is the Indus script?

Status: 2026-11-25. Details and pre-registrations in `docs/JOURNAL.md`; data use in `docs/DATA_LEDGER.md`.

## 1. Reference material

| Group | Corpora | Source |
|---|---|---|
| Proto-administrative systems | proto-Elamite; proto-cuneiform (Uruk IV–III) | CDLI bulk data |
| Full writing | Sumerian Ur III administrative; Sumerian Old Babylonian literary; Akkadian Old Babylonian letters | CDLI bulk data |
| Non-linguistic symbol systems | barn stars, totem poles, weather icons, Asian emoticons (kudurrus excluded: too few documents) | Sproat (2014) corpora |
| Disputed systems | Pictish symbols, Vinča signs | Sproat (2014) corpora |

## 2. Results

### 2.1 Placement among reference systems (D1; robustness with KP1979)

Six statistics (direction asymmetry, positional template strength, recurring units, within-line repetition, hapax share, concentration of line-final signs), computed identically on samples matched to the Indus length distribution:

- The Indus corpus is closest to **proto-Elamite** (ICIT: distance 2.31; KP1979: 2.70), and closer to an administrative corpus than to any non-administrative one in 20/20 (ICIT) and 19/20 (KP1979) resamples.
- Leaving out any one statistic keeps a proto-administrative corpus nearest.
- A bigram model fitted to the Indus texts does not reproduce their profile; the texts obey constraints beyond first-order transitions (a fixed line end).
- The low within-line repetition reported for the ICIT transcription (0.038) is **not** a property of the inscriptions: KP1979, which writes doubled signs as two signs, has 0.167. An earlier observation based on it was withdrawn.

### 2.2 Writing or not (gate G3: undecided)

With non-linguistic systems added (D2), a leave-one-out check misclassified two of seven known corpora (totem poles and emoticons as writing). The statistics do not separate writing from non-writing, in line with the caution of Sproat (2014) and Raghavendra (2026). No claim about the linguistic status of the Indus signs is made.

### 2.3 Size of the sign inventory (D3)

Estimated total number of sign types (Chao1, 9,000 tokens): ICIT 830 (95 % interval 762–928), KP1979 511 (448–617), proto-Elamite 820 (732–950). The inventory is far larger than any syllabary or alphabet and comparable to proto-Elamite.

### 2.4 Sound-sequence regularity (from E3b–E3d)

Sound-sequence models of four natural languages all gain from the real Indus sign order, while a pseudo-language does not. The same holds for cuneiform texts hidden as ciphers. The order of the Indus signs therefore has local regularities of a kind that natural-language sound models can exploit; this does not identify a language and does not decide G3.

## 3. Conclusion

Statistically the Indus inscriptions resemble the proto-administrative systems of the late fourth millennium BCE (proto-Elamite most closely) more than Sumerian or Akkadian full writing, in both transcriptions. Whether the signs record a spoken language cannot be decided with these methods.
