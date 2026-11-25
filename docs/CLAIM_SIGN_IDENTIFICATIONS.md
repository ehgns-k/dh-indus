# Sign identifications for claims C26 and C3

Purpose: make claims C26 and C3 (`docs/CLAIMS_REGISTER.md`) testable by naming the signs involved in the numbering systems used here. Compiled 2026-11-25.

Numbering systems:
- **M**: Mahadevan 1977 sign numbers.
- **P / KP**: Parpola sign numbers. In `mayig/indus-valley-script-corpus` (`features/P###.json`) the `id` P### is the same number as the KP1979 sign rank in `data/raw/kp1979_signs.tsv`. This was checked for the signs below: the 1965 variant codes listed under each P number match the variant codes listed under the same KP rank (for example P324 = V204, V526 = KP 324; P325 = V205, V209 = KP 325).
- **ICIT**: three-digit Wells/ICIT codes as in `data/raw/icit2025.csv` (W### in mayig).

Mapping sources:
- (a) mayig `features/P###.json`, fields `wells_graphemes` and `mahadevan_graphemes`: a hand-made list. Called "mayig" below.
- (b) `results/phase1_concordance.tsv`: the alignment-based ICIT ↔ KP1979 concordance. Called "concordance" below. Figures are support / aligned total and purity.

Certainty terms used below:
- **exact**: the sign appears in the named field of the mapping source, and the two sources agree.
- **many-to-one**: one system splits what the other merges. The mapping is exact at the level of the group, not of the single sign.
- **conflict**: the two mapping sources disagree.
- **not found**: no entry in the source.

Occurrence counts are raw counts over all rows of `data/raw/icit2025.csv` and `data/raw/kp1979_ins.tsv` (not deduplicated). Raw ICIT `text` strings are stored in reverse reading order (see `docs/JOURNAL.md`, "Checking the reading order"). All sequences below are given in reading order unless a raw string is quoted.

---

## C26. Mahadevan's four-sign sequence "merchant of the city"

### The sequence in Mahadevan's own terms

Mahadevan (2014) calls the sequence ABCD and reads it as two pairs, AB and CD:

| Position | Mahadevan's name | Mahadevan 1977 no. | Proposed reading (from excerpts) |
|---|---|---|---|
| A | "wolf" (the back of a wolf) | 51 | māṟ- "exchange (of goods), barter; one who barters, trader, merchant" (DEDR 4834) |
| B | "hook" (elongated Z-shaped hook) | 130 | koḷ "take, receive, buy; buyer" (DEDR 2151, via koḷ "hook") |
| C | "open crossroads" | 149 | pāṭ(i) / puṟa "settlement, city" |
| D | "jar" | 342 | -(a)ṉṟ "he of the" (masculine singular suffix; compare C14) |

Excerpts say that the whole sequence is read māṟ-koḷ-pāṭ-(a)ṉṟ, glossed "merchant of the city". Mahadevan relates the sequence to Pandyan dynastic titles in Old Tamil and to the Vedic deity Pūṣan. The related sign 150, "closed crossroads", is read aka in the same excerpts. It is not part of the sequence.

Sources (all seen only as search-engine excerpts; full texts were not reachable from this environment):
- Mahadevan, I. 2014. *Dravidian Proof of the Indus Script via the Rig Veda: A Case Study*. Indus Research Centre, Roja Muthiah Research Library, Bulletin No. 4, November 2014. https://rmrl.in/bulletin/bulletin-No-4-Nov-2014.pdf ; https://www.harappa.com/content/dravidian-proof-indus-script-rig-veda-case-study
- Critical review naming sign 51 ("wolf"), sign 130 ("elongated Z-shaped hook", compared with an S-shaped copper fish hook from Khirsara, DEDR 2151 koḷ) and signs 149/150 ("open"/"closed crossroads"): "Iravatham Mahadevan's Reading of Indus Script: A Critical Review", https://www.researchgate.net/publication/370480645 ; https://www.academia.edu/101124192
- Summary giving "'wolf' + 'hook' + 'open crossroads' + 'jar'" and the reading māṟ-koḷ-pāṭ-(a)ṉṟ: https://www.academia.edu/37519869 ; press report https://www.tamilnet.com/art.html?catid=13&artid=37488
- Blog discussion of the same four signs on seal H-12 (the first sign compared with Fairservis's "prawn"): http://indusscriptmore.blogspot.com/2014/11/merchant-of-city-or-master-who-collects.html
- Sign 342 in Mahadevan 1977 is the most frequent sign (the "jar"): Yadav et al. 2010, *PLoS ONE* 5(3): e9506, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009506

The excerpts give the Mahadevan numbers 51, 130, 149 and 342 directly. They do not show which excerpt comes from which page. Those numbers should be checked against the bulletin's figures when the PDF can be opened.

### Mapping to the project's numbering

| Pos. | M | mayig P (= KP) | mayig ICIT | Concordance ICIT → KP | Certainty |
|---|---|---|---|---|---|
| A wolf | M051 | P073 ("unknown asymmetric animal ... fish with asymmetric fins and legs") | 255 | 255 → 73 (43/43, 1.00) | **exact** |
| B hook | M130 | P188 ("vertical line with diagonal going down from top right, diagonal going up from bottom left") | 435, 436 | 435 → 188 (25/25, 1.00); 436 → 188 (2/2) | **many-to-one**: ICIT 435 and its mirror form 436 are both KP 188 / M130 (see C3) |
| C open crossroads | M149 | P255 ("two nested greater-than symbols, touching two nested less-than symbols") | 690 | 690 → 255 (26/26, 1.00) | **exact** |
| D jar | M342 | P324 (plain jar) | 740 | 740 → 325 (352/506, 0.70), also 324 (131) | **many-to-one with conflict**: mayig puts ICIT 740 = P324 and ICIT 741 = P325 (jar with a stroke inside); the concordance aligns ICIT 740 mostly with KP 325 and partly with KP 324 |

Related signs that are not part of the sequence: M052 = P074 = ICIT 256 (the "wolf" attached to a tall stroke); M150 "closed crossroads" = P256 = ICIT 692 (concordance 692 → 256, 0.97).

### The sequence in the corpora

The identification is supported by the corpora themselves. The four signs form a frequent fixed string in both transcriptions, in the expected order, with the jar last:

- **ICIT, reading order 255-435-690-740**: 31 rows; **255-436-690-740**: 3 rows; 34 in all. The raw strings are `740-690-435-255` and `740-690-436-255`. Examples: H-12 (`+740-690-435-255-803-220-240-235-002-817+`, the seal named in the blog post above), H-61, H-1937, H-1938, K-10. The three rows with 436 are the repeated crocodile tablets (for example H-278, H-871: `740-407-590-690-436-255-...`).
- **ICIT, the three signs 255-435/436-690 followed by**: 740 (34 times), 590 (11), 176 (1), 921 (1).
- **KP1979, reading order 73 188 255 + X**: 43 occurrences of 73 188 255, followed by 325 (14), 324 (12), 276 (7), 326 (6), and once each by 325*, 194, 396, 398.

**ICIT form for testing C26: 255 – 435 (or 436) – 690 – 740.** In KP1979 the form is 73 – 188 – 255 – 324/325, and in the more general form the final jar is any of KP 324–326. For the test, decide in advance whether D is ICIT 740 only, or the jar family 740–744, which corresponds to KP 324–326. The excerpts do not say whether Mahadevan's frequency counts for the sequence include the jar variants.

---

## C3. Mirror-image sign pairs said to be allographs

### Published list

The only published list found is in Daggumati, S. & P. Z. Revesz. 2021. "A method of identifying allographs in undeciphered scripts and its application to the Indus Valley Script". *Humanities and Social Sciences Communications* 8: 50. https://doi.org/10.1057/s41599-021-00713-0 ; https://www.nature.com/articles/s41599-021-00713-0 (open access).

- Table 1 lists 23 pairs of mirrored signs. In each pair the left sign is the original and the right sign is its mirror. The table gives ICIT frequencies, the CISI artefacts and a type of mirroring (types 1–8). The paper's words are: "We claim that all the 23 pairs of mirrored signs are allographs". The originals occur 1,659 times and the mirrors 110 times (about 6.7 %). Every mirror occurs fewer than 20 times.
- The sign list and frequencies are taken from ICIT (Wells & Fuls), so the numbering is ICIT/Wells. In the article, though, the signs are printed as glyph images, not as numbers, in Table 1 and in the running text. The numbers could therefore not be read from the text. The only number printed in the text is "sign 851".
- The article text was read from a plain-text copy of the open-access PDF in a public GitHub repository (https://github.com/Cuuper22/ivc, file `evidence/tmp/h1302_h1303_direction_prior_work/daggumati_revesz_2021_allographs_nature_article.pdftotext.txt`). The publisher's site was not reachable from this environment.

### Reconstruction of the pairs in ICIT numbers

For most pairs the text names the artefacts on which the mirror occurs and how often. These were matched against `data/raw/icit2025.csv`: for each paragraph, the rare ICIT sign that occurs on the named artefacts was located. **This is a reconstruction, not a reading of Table 1.** The mirror sign is reliable when the artefacts and the counts agree. The "original" is usually inferred: it is the frequent neighbouring ICIT code with the same shape, and mayig groups the two under one P number with an orientation feature. Counts in the 2025 ICIT file differ slightly from the paper's counts, which came from the ICIT of about 2020.

| # | Mirror (ICIT) | Raw occ. | Paper's evidence (artefacts, counts) | Original (ICIT) | mayig P / M | Concordance KP | Certainty of identification | Certainty of mapping |
|---|---|---:|---|---|---|---|---|---|
| 1 | **436** | 17 | "17 mirrored occurrences", 11 on H-278–H-284 and H-871–H-873; also H-1154, H-1835, H-2039, M-189 (all present in ICIT on 436) | 435 (75) | P188 for both, `facing` feature / M130 | 435 → 188, 436 → 188 | mirror high; original high | exact (many-to-one) |
| 2 | **921** | 16 | "appears 15 times"; "bow sign" (Fig. 3); H-8, H-161, H-1657, H-64, M-245, M-779, M-1141, M-1737, M-1826, M-1272, H-209, H-482, M-494, M-239 (14 of the 16 named artefacts carry 921) | probably 920 (150) | 921 = P165 / M301; 920 = P160 / M293 | 921 → 165 (0.90); 920 → 160 (0.95) | mirror high; original probable | exact, but the two forms are separate signs in KP and in Mahadevan |
| 3 | **408** | 9 | "rake sign" (Fig. 2); H-1413, H-1745, H-1930, M-599, M-600, M-749 (all on 408) | 405 or 407 (118, 142); not determined | P086 for 405–408 / M161–M169 | 405, 406, 407 → 86 | mirror high; original undetermined | many-to-one (KP 86 merges 390, 392, 405–408) |
| 4 | **406** | 12 | "12 occurrences of the mirrored sign"; Lothal L-28, L-37, L-210; H-663; also H-50 and M-1350, the two seals shown in Fig. 2 | 405 or 407; not determined | P086 / M161–M169 | 406 → 86 | mirror high; original undetermined | many-to-one |
| 5 | **402** | 2 | "Out of 455 occurrences of [the sign] only three occur as a mirror"; L-251, M-1233 (K-77/K-68 compared) | 400 (499) | P098 for both, `direction` feature / M176 | 400 → 98, 402 → 98 | high | exact (many-to-one) |
| 6 | **551** | 3 | four occurrences: H-1468, M-62 (with the original on the same seal), K-6, K-56 | 550 (122) | 551 = P234, 550 = P230; both M216 | 550 → 224 (0.86); 551 not in concordance | high | conflict for 550 (P230 against KP 224); 551 not found in concordance |
| 7 | **622** | 2 | three occurrences: K-6, M-747, M-782 ("direction should be that of the original"; the 2025 ICIT has 621 on M-782) | 621 (9 in concordance) | P265 for both, `crossbar_location` feature / M242 | 621 → 265 (0.90) | high | exact for 621; 622 not in concordance |
| 8 | **797** | 4 | four occurrences: M-600, B-4, H-2104, H-632 (H-632 not in ICIT; ICIT also has H-362) | probably 798 (149) | P075 for 193, 797, 798, `direction` feature / M053 | 798 → 75 (60/60); 797 → 50 (2/2) | mirror high; original probable | conflict for 797 (P075 against KP 50) |
| 9 | **062** | 3 | four occurrences: H-305 (wrongly coded), H-1864, H-2124, M-664 | probably 061 (93) | P204 for 061–063, `facing` feature / M124, M125 | 061 → 204, 062 → 204 | mirror high; original probable (063 is in the same group) | exact (many-to-one) |
| 10 | **177** | 3 | "five times in Harappa and once in Mohenjo-Daro": H-232, H-1302, H-1303, H-1822, ivory rod M-[1]650, H-853 (ICIT now: H-232, H-853, C-91) | probably 176 (217) | P194 for 176–179 / M048 | 176 → 194 (47/47); 177 → 288 (1/1) | medium | conflict for 177 (one aligned case only) |
| 11 | **526** | 13 | "the mirrored sign occurs 10 times", always terminal; H-344, L-9, H-2084 (all on 526) | 527 (63) | P301 for both, `flipped` feature / M254 | 526 → 301, 527 → 301 | high | exact (many-to-one) |
| 12 | **126** | 2 | "occurs only twice in comparison to the original which occurs 57 times"; H-298, H-1920 | 125 (58) | P035 for both, `facing` feature / M028 | 125 → 35; 126 → 123 (1/1) | high | conflict for 126 (one aligned case) |
| 13 | **442** | 4 | "five occurrences": H-795, K-45, M-1783, M-2027, M-632 (four of the five on 442) | not determined (440 or 443?) | 440 = P283 / M127; 442 not found in mayig | 440 → 283; 442 not found | mirror medium; original undetermined | not found |
| 14 | **492** and **494** | 1, 2 | paragraph on two signs: M-331 (boustrophedonic), H-1902, M-402; the paper concludes that these are not true mirrors | not determined (491/495?) | not found in mayig | 491, 495 → 210 | medium | not found |
| 15 | **307** | 2 | "two seals": K-18, M-745; the paper concludes that both are the original | not determined (308?) | P206 for 307–309 / M181 | 307 not found | medium | many-to-one (mayig only) |
| 16 | **710** | 5 | "two occurrences, one in Harappa and one in Mohenjo-daro"; M-784 named | not determined | P323 for 708–710; no M number | 710 → 323 (2/2) | low | many-to-one (mayig only); no Mahadevan number |
| 17 | **102** | 1 | "one account of the mirrored sign" on H-1775 (102 occurs once, on H-1775) | not determined | not found in mayig | not found | low (one artefact, one rare sign) | not found |

Not identified (about six of the 23 pairs): the pair whose mirror occurs only once, at Lothal; the pair whose mirror occurs once at Mohenjo-daro against 11 originals at Harappa (the text mentions "the tick of sign 851"; ICIT 851 has 7 raw occurrences, all at Harappa, so the mirror is not established); the pair discussed with copper tablets and seal L-36, which the paper says does not exist as a mirror; and the two Mohenjo-daro-only pairs whose paragraphs name no artefacts. Table 1 itself (an image) is needed to complete the list.

### A second, unpublished source of orientation pairs

mayig records left/right orientation as a feature within one P sign (field names `mirror`, `flipped`, `facing`, `direction`, `crossbar_location`, `raised_arm`, `branch_direction`, `curve`, `orientation`). This means Parpola's list already treats such forms as variants of one sign. Signs with such a feature that have two or more ICIT numbers are P035 (125, 126), P040 (110, 111), P066 (264, 266, 268), P075 (193, 797, 798), P082 (205–209), P086 (390, 392, 405–408), P098 (400, 402), P188 (435, 436), P194 (176–179), P204 (061–063), P265 (621, 622), P301 (526, 527), P332 (752, 760) and P371 (815, 816). The list is hand-made and not a published claim. It can serve as an independent check on the reconstructed pairs: ten of the 17 rows above (1, 3, 4, 5, 7, 8, 9, 10, 11, 12) fall inside one of these groups.

### Notes for the C3 test

- Pairs 1, 5, 6, 7, 11 and 12 are the most secure. For each of them both the mirror and the original are fixed by the paper's artefact list and counts and by a shape grouping in mayig. A first test can use these six pairs, with pairs 2–4 and 8–10 as a second tier.
- The paper itself classes most mirror occurrences as errors, boustrophedon, crowding or location anomalies. Only pair 2 (921, the "bow sign") is put forward as possibly meaningful (type 5). It also concludes that some ICIT mirror codes are wrong, for example in pairs 7, 14 and 15. A context-similarity test should report results with and without those artefacts.
- The concordance and mayig disagree for 550, 797, 177 and 126. In those cases the rare form was aligned only once or twice. KP1979 merges several of these pairs into one sign (KP 86, 98, 188, 204, 301), so in KP1979 the C3 test can be run only for pairs that KP keeps apart: 920/921 (KP 160/165) and 550/551 (KP 224 or 230/234).

### Overlap between C26 and C3

The hook sign in C26 is ICIT 435, and its mirror, ICIT 436, is pair 1 of the C3 list. Three of the 34 ICIT occurrences of the C26 sequence use 436. All three are on the repeated crocodile tablets that Daggumati & Revesz describe as "one repeated mistake".
