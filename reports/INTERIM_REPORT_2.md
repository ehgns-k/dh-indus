# Interim report 2 (2026-11-25, after the review pass)

This report supersedes the level assignments of interim report 1. Every result listed here is documented, with its pre-registration, in `docs/JOURNAL.md`; the data used for each decision are in `docs/DATA_LEDGER.md`.

## 1. What changed since interim report 1

1. **Review of the held-out split (R1).** 42–47 % of held-out strings had a training string that differs by one sign. All held-out results were re-decided without them. The structural (L1) results passed again; the closing-sign association (C2, C2k) kept its effect size but no longer reached the strict thresholds and is now an **L2 candidate**.
2. **Phonetic fitting closed (E3, E3b, E3c, E3d).** Four variants of a calibrated sign-to-sound search all failed to identify the language of known cuneiform texts hidden as ciphers, including with four times more data and with equal amounts of running text for every language. No language preference is claimed for the Indus inscriptions.
3. **Numeral system (H6.1).** Short-stroke and long-stroke signs take disjoint partner signs at sites excavated after 1979.
4. **Sign classes (Q2).** Positional zones computed independently in the two transcriptions agree for 91 % of linked signs; `docs/SIGN_CLASSES.md` documents 80 frequent signs with their established roles.

## 2. Results by level

### L1: structural results (met)

| Result | Evidence |
|---|---|
| Reading order and direction carry over to later finds | F3, F3b (post-1979 sites) |
| Fixed order within the line-final cluster (740 before 400 / 090) | H3.3, H3.4; strict held-out (R1) |
| Count-specific partner signs: 4–9 short strokes → 390–407; 7 → 585/575; 3 long → 520 | H3.10, H3.12; matched controls (H3.11); strict held-out (R1); post-1979 sites (F2) |
| Two numeral series with disjoint partners (depends largely on sign 033; see journal) | H6.1 (post-1979 sites) |
| Positional template and recurring units predict later finds | B1, B4 (gate G1) |
| Positional classes are the same in both transcriptions | Q2a |

### L2: semantic or functional categories (candidate only)

| Candidate | Evidence | Why not confirmed |
|---|---|---|
| The closing sign depends on the kind of object (400 avoided on motif-bearing seals, favoured on tablets; 407/154 on rectangular seals without motif) | C2 (ICIT), C2k (KP1979 with independent object codes); same effect sizes on strict held-out (R1); same direction on post-1979 sites (F4, p = 0.0104) | strict thresholds not reached once near-duplicates are removed; no unused data remain for a confirmatory test |

### L3: phonetic decipherment (not achieved; no calibrated route available)

| Finding | Evidence |
|---|---|
| Random sign-value assignments make 84 % of lines readable as Sanskrit under the rules of a published decipherment, as many as that decipherment | E2, E2b |
| Sound-sequence fitting cannot identify the language of known scripts hidden as ciphers (2,000 and 8,000 lines; unequal and equalised models) | E3, E3b, E3c, E3d |

### Is it writing? (gate G3: undecided)

The Indus corpus is statistically closest to proto-Elamite and proto-cuneiform (D1). The statistics used cannot separate writing from non-linguistic symbol systems (D2). All natural-language sound models gain from the real Indus sign order while a pseudo-language does not (E3b–E3d), which shows local, language-like regularity but does not settle the question.

## 3. Synthesis

The Indus inscriptions show a consistent internal organisation that holds across sites, across two independent transcriptions and across finds made after the main corpus was published: a fixed reading direction; a template of initial, medial and closing signs; a closing cluster with a fixed internal order; and a numeral system of short and long stroke series whose counts are paired with specific following signs. The closest statistical relatives among the reference systems are the proto-administrative scripts of the late fourth millennium BCE. Whether the signs record a spoken language could not be decided with the available statistics, and no calibrated method was found that can assign sound values with this corpus.

## 4. Remaining work

See `docs/WORKPLAN.md` (latest priority list). The main limitation for any further confirmation is the absence of unused data: new inscriptions, or an independent corpus of objects not in the ICIT-style source, would be needed to confirm the L2 candidate.
