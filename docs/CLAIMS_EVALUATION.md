# Evaluation of the claims register

Status: 2026-11-25. Each claim of `docs/CLAIMS_REGISTER.md` is set against the tests of this project. Verdicts:
- **supported**: a pre-registered test of the claim's prediction passed;
- **not supported**: a pre-registered test failed, or the claim's figure is contradicted;
- **consistent**: descriptive figures agree with the claim, without a decisive test;
- **undecided**: the available tests cannot decide;
- **not tested**: no test was possible with the data available here.
Test labels refer to entries in `docs/JOURNAL.md`; figures for descriptive checks are in `results/claims_descriptive.json`.

| Claim | Short title | Verdict | Evidence |
|---|---|---|---|
| C1 | Right-to-left direction (crowding of signs) | consistent | Layout not tested; order learned from KP1979 predicts later finds only right to left (F3, F3b) |
| C2 | Direction from initial/final asymmetry | supported | Final-sign distribution far more concentrated than initial (4.8 vs 7.1 bits, ICIT); direction tests F3, F3b |
| C3 | Multi-directional writing; mirrored signs as allographs | undecided | Automatic mirror detection on the sign images finds only two pairs among frequent signs (G3); the clearest, 920/921, is not used like an allograph pair (different following signs) |
| C4 | Sign inventory 417–694 | consistent | Estimated totals 511 (KP1979) and 830 (ICIT); the figure depends on allograph decisions (D3, L3a, L3b) |
| C5 | About 400 graphemes, a quarter singletons | consistent | KP1979: 100 of 367 types occur once (27 %) |
| C6 | About five signs per inscription; longest 14 and 26 | consistent | Mean line length 4.5–4.6; longest line 13–14; longest object 17 (ICIT) and 28 (KP1979) signs |
| C7 | Mean 4.6 signs; longest face 17 | consistent | As C6 |
| C8 | Many singletons and rare signs | consistent | 214 of 607 (ICIT) and 100 of 367 (KP1979) types occur once |
| C9 | No sign repetition as in phonetic scripts | not supported as a property of the inscriptions | Within-line repetition is 3.8 % in ICIT but 16.7 % in KP1979, which writes doubled signs as two signs; the figure depends on the transcription |
| C10 | Short texts explain the low repetition | supported | Repetition rises with length (CT10) |
| C11 | One sign about 10 %; 69 signs cover 80 % | consistent (ICIT) | ICIT: 740 has 10.7 %, 82 signs cover 80 %; KP1979 splits the jar sign (325: 6.4 %; 63 signs) |
| C12 | Well-defined initial and final signs | supported | Positional zones reproduced across transcriptions (Q2a); template on later finds (B1) |
| C13 | The jar sign is the most frequent sign | supported | ICIT 740, rank 1; identified with the jar shape from the sign image |
| C14 | Jar sign as a Dravidian suffix | undecided (reading); distributional prediction not supported | 740 follows a narrow set of signs (left-neighbour variety 0.19, among the lowest of the frequent signs), unlike a freely attaching suffix; the reading itself cannot be tested |
| C15 | Final sign as a genitive ("of X") | function supported; reading undecided | On data not used before, 740 closes seal texts more often than tablet texts in every site stratum (CT15, OR 4.3, p = 0.0022); whether the closing function is a genitive cannot be tested |
| C16 | Jar sign as a unit of measure | not supported | Texts with 740 contain numerals less often than other texts, in both transcriptions (CT16) |
| C17 | Long texts consist of frequent 2–4-sign units | supported (weak form) | Recurring units predict later finds (B4); long texts divisible into short complete texts more often than controls, though only 4–8 % fully (CT17) |
| C18 | Recursive segmentation structure | supported | Parts from recursive splitting at the weakest link are complete texts about three times as often as for controls, both transcriptions (CT18) |
| C19 | Conditional entropy closer to languages | undecided | Statistics do not separate writing from non-linguistic systems (D2) |
| C20 | Entropy measures classify the system as non-linguistic | undecided | As C19 |
| C21 | Markov model of sign order; West Asian texts differ | (a) consistent; (b) not supported at the threshold | Bigram restores a masked sign first in 29 % and within five in 52 % of strict held-out lines; abroad texts less predictable, p = 0.011 (H8.1) |
| C22 | Fish sign = *mīn* "fish/star" | undecided (reading) | The fish-shaped signs form a coherent usage class (G2, H9.3); they are not preferentially preceded by numerals (H3.13) |
| C23 | Numeral + fish as star names (3, 6, 7) | not supported | H3.13, H3.14; seven strokes go with 585/575, almost never with a fish sign |
| C24 | Stroke numerals up to nine; semicircles as tens | supported for strokes; semicircles not tested | Counts 1–10 attested; count-specific partners (H3.10, H3.12, F2); variable numeral slot (H9.1, R4); arc signs too rare |
| C25 | Base unknown, possibly 8 or 10 | undecided | Counts 8, 9, 10 attested but rare (B2) |
| C26 | Four-sign sequence "trader" + title | not tested | Sequence not identified |
| C27 | Logograms, not phonograms | consistent (descriptive) | Bigram density of frequent signs 0.29, like proto-Elamite (0.27) and below syllabic Akkadian graphemes (0.41) |
| C28 | Seal texts are not owners' names | undecided | 1,453 distinct texts on 1,585 seal lines; few texts repeat across sites (44); compatible with names and with other readings |
| C29 | Tablets as licences | undecided | Seal and tablet texts differ within Harappa (H3.5 exploratory) but the difference does not transfer across sites (H3.5); closing sign by object class is an L2 candidate (C2, C2k) |
| C30 | Motifs as emblems; text independent of motif | consistent | Text does not predict the motif (H4.2, C1) |
| C31 | Tablets as ration records | partly supported | Variable numeral slots in fixed formulae exist (H9.1, R4), but numerals are not more frequent on tablets (H4.1) and count-variable formulae are not concentrated on tablets (H9.2) |
| C32 | Miniature tablet texts repeat seal endings | weakly supported | H4.3 passed as registered but not under the strict control |
| C33 | Proto-abugida recording Sanskrit | not supported as evidence | Random sign-value assignments with the same reading freedoms are as readable as the published readings (E2, E2b) |
| C34 | Indus statistics fit no non-linguistic baseline cleanly | consistent | No clean separation of systems (D2) |
| C35 | The measures are not specific to language | supported | Leave-one-out misclassifies two of seven known systems (D2) |
