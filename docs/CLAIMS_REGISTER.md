# Register of Published Claims about the Indus Script

## Introduction

This register collects specific claims about the Indus script that have been made in published or publicly circulated work, and restates each one as a statement that can be tested against a digital corpus of sign sequences. The corpus is assumed to consist of lines in reading order, each with its find site, its object type (seal, tablet, pottery, tag and so on) and, for seals, the animal motif. The two corpora used in this project are described in `data/sources.tsv` and `docs/JOURNAL.md`.

The register does not judge whether a claim is true. It records what was claimed, by whom, where the claim was seen, and what observation in the corpus would count for or against it.

Rules followed in compiling the register:

1. Every entry gives the author, the year and the URL at which the claim was seen. Works listed in `docs/BIBLIOGRAPHY.md` are cited by their bibliography number (for example B8, C1).
2. The field "Source seen" states what was actually consulted. Most entries were compiled from search-engine excerpts of the pages named, because the pages themselves could not be opened directly when the register was compiled. A quotation marked "excerpt" reproduces the wording shown in such an excerpt. It must be checked against the original before it is cited in any publication. No page numbers are given, because no page was seen in its printed form.
3. A claim for which no source could be found was left out.
4. Sign numbers. The two corpora use different numbering systems (see `docs/SIGN_CONCORDANCE.md`). Where a claim names a sign by its shape (for example the "jar" or the "fish"), the testable form names the candidate sign numbers in each corpus where they are known. These identifications must be confirmed against the sign-list drawings before a test is run. In particular, the identification of the most frequent sign in each corpus (ICIT 740; KP 324/325) with the "jar" sign is assumed, not yet checked.
5. Tests of claims that predict information outside the text (find site, object type, motif) are to be run on the held-out set defined in `docs/METHOD.md`, with correction for the number of tests.

## Index

| No. | Short title | Claim type | Source | Feasible now |
|---|---|---|---|---|
| C1 | Right-to-left direction from crowding of signs | direction | Mahadevan 1977, via Yadav (lecture) | partly |
| C2 | Direction from asymmetry of initial and final signs | direction | Ashraf & Sinha 2018 | yes |
| C3 | Multi-directional writing; mirrored signs are allographs | direction / sign list | Daggumati & Revesz 2021 | partly |
| C4 | Size of the sign inventory: 417 to 694 | inventory | Daggumati & Revesz 2021 | yes |
| C5 | About 400 graphemes, about a quarter attested once | inventory | Parpola 2008 | yes |
| C6 | Inscriptions average about five signs; longest texts 14 and 26 signs | text length | Mahadevan, via Yadav (lecture); Mahadevan (agricultural signs) | yes |
| C7 | Average inscription 4.6 signs; longest on one face 17 signs | text length | Farmer (n.d.) | yes |
| C8 | Many singletons and very low-frequency signs | inventory | Farmer (n.d.) | yes |
| C9 | No sign repetition of the kind expected in phonetic scripts | repetition | Farmer, Sproat & Witzel 2004, via Parpola 2008 | yes |
| C10 | Short seal texts give little reason for repetition | repetition | Parpola 2008 | partly |
| C11 | One sign forms about 10% of the corpus; 69 signs form about 80% | frequency | Yadav et al. 2010 | yes |
| C12 | Well-defined text-initial and text-final signs; directionality | position | Yadav et al. 2010 | yes |
| C13 | The "jar" sign is the most frequent sign | frequency | secondary: Wikipedia; Mahadevan (interview) | yes |
| C14 | "Jar" sign as a Dravidian masculine singular suffix | interpretation | Mahadevan, via Mukhopadhyay 2019 | partly |
| C15 | Final sign as a genitive: "the possession of X" | interpretation | Parpola, via harappa.com | partly |
| C16 | "Jar" sign as a metrological noun in tax texts | interpretation | Mukhopadhyay 2018 (SSRN) | partly |
| C17 | Longer texts segment into frequent 2-, 3- and 4-sign units | segmentation | Yadav, Vahia, Mahadevan & Joglekar 2008 | yes |
| C18 | Recursive structure in segmentation trees | segmentation | Sinha et al. 2011 | yes |
| C19 | Conditional entropy closer to languages than to non-linguistic systems | entropy | Rao et al. 2009 (Science) | partly |
| C20 | Entropy-type measures classify Indus as non-linguistic | entropy | Sproat 2014 | partly |
| C21 | Markov model; West Asian texts differ in sign order | sequence model / site | Rao et al. 2009 (PNAS) | yes |
| C22 | Fish sign read as Dravidian *mīn* "fish" = "star" | phonetic reading | Parpola (after Heras), via harappa.com | partly |
| C23 | Numeral + fish = names of asterisms | phonetic reading | Indus Research Centre Bulletin 2 (2011) | partly |
| C24 | Stroke numerals up to nine; semicircles as tens | numerals | Parpola, via harappa.com | partly |
| C25 | The numeral base is unknown, possibly 8 or 10 | numerals | Reddy 2025 | partly |
| C26 | A four-sign sequence read as "trader, merchant" + title | phonetic reading | Mahadevan 2014 | partly |
| C27 | Signs are logograms in functional classes, not phonograms | script type | Mukhopadhyay 2019 | partly |
| C28 | Seal texts are not names of seal owners | content | Mukhopadhyay 2019 (press); Mukhopadhyay 2023 | partly |
| C29 | Tablets as licences for trades, crafts or commodities | content / object type | Mukhopadhyay 2023 | partly |
| C30 | Seal motifs as emblems of guilds or governing bodies | motif | Mukhopadhyay 2023 | yes |
| C31 | Tablets as ration records; seals generating tokens | content / object type | Rao 2018 | partly |
| C32 | Identical texts on Harappa miniature tablets, shared with a seal | duplication / object type | Meadow & Kenoyer, via harappa.com | yes |
| C33 | The script is a proto-abugida recording Sanskrit | phonetic reading | Yajnadevam (n.d.), not peer-reviewed | partly |
| C34 | Indus statistics fit no non-linguistic baseline cleanly | typology | Nair 2026 (preprint) | partly |
| C35 | The statistical measures are not specific to language | methodology | Raghavendra 2026 (preprint) | partly |

---

## A. Direction of writing

### C1. Right-to-left direction from crowding of signs
- Claim (close paraphrase): The direction of writing was inferred from the layout of signs on the objects: signs are crowded towards the left end, overflow at the left end and leave a gap at the right end. Shorter inscriptions begin at the right edge and leave blank space near the left edge, and the leftmost signs of longer inscriptions are moved to a second line. On this evidence the script runs from right to left in most cases, with a few exceptions. The slide cited reports the right-to-left direction for 83% of cases.
- Verbatim quote (if seen): none seen in the original. Excerpt (search summary of Mahadevan's account, wording not checked): "Shorter inscriptions start at the right edge, leaving blank space nearer the left edge".
- Source: Mahadevan 1977 (A1) and Parpola, as cited on lecture slides by Nisha Yadav (2024), https://www.imsc.res.in/~sitabhra/meetings/bitsscripts24/Nisha_Yadav_Lecture.pdf ; Mahadevan's account at https://www.harappa.com/content/maha6.html. Source seen: secondary, search-engine excerpts of both pages.
- Testable form: The claim is about physical layout, which a sign-sequence corpus records only indirectly. (a) Using the direction field of the ICIT-style transcription (`dir.`), compute the proportion of lines with a recorded direction that are R/L. The claim predicts a large majority, of the order of the reported 83%. (b) For texts known in both a one-line and a two-line layout, check whether the line break falls before the leftmost signs. The claim is weakened if the majority direction falls well below the reported figure, or if line breaks show no preference.
- Feasible with current data: partly. Part (a) can be run now. The ICIT field records R/L for 4,263 records and L/R for 215, but it is an editorial judgement, not an independent measurement, so the test only checks internal consistency. Part (b) needs line-layout information, which neither corpus records in a usable form.

### C2. Direction from the asymmetry of initial and final signs
- Claim (close paraphrase): In known writing systems the distribution of signs at the end of a word is more constrained than at the beginning. This asymmetry can be used to infer the direction of writing of undeciphered inscriptions, and applied to the Indus corpus it indicates right-to-left writing.
- Verbatim quote (if seen): excerpt: "We use the existence of this asymmetry to infer the direction of writing in undeciphered inscriptions that agrees with the archaeological evidence."
- Source: Ashraf, Md Izhar & Sitabhra Sinha. 2018. *PLoS ONE* 13(1): e0190735 (D5); https://pmc.ncbi.nlm.nih.gov/articles/PMC5771592 ; preprint https://arxiv.org/abs/1509.09121. Source seen: abstract, as reproduced in search-engine excerpts.
- Testable form: For deduplicated complete lines in stored reading order, compute the entropy (or Gini coefficient) of the sign distribution in the first position and in the last position. The claim predicts that the last-position distribution is more concentrated (lower entropy) than the first-position one, so that the side with the more concentrated distribution is the end of the line. Repeat with all lines reversed and against a within-line shuffle control. The claim fails for this corpus if the two distributions do not differ beyond the shuffle control, or if the more concentrated side is the beginning in reading order.
- Feasible with current data: yes. Both corpora are stored in reading order. One caution: the corpora have already been put into a single orientation by their editors, partly on the basis of earlier direction arguments, so the test checks agreement with the editorial direction rather than giving an independent result.

### C3. Multi-directional writing; mirrored signs are allographs
- Claim (close paraphrase): The Indus script was not always written from right to left. Mirrored forms of a sign often mark only the direction of writing and do not differ in meaning, so they are allographs. Merging allographs, found through the positions of signs in inscriptions, gives a smaller sign list.
- Verbatim quote (if seen): excerpt: "the mirroring of signs often denotes only the direction of writing without any difference in meaning".
- Source: Daggumati, Shruti & Peter Z. Revesz. 2021. *Humanities and Social Sciences Communications* 8 (D11); https://www.nature.com/articles/s41599-021-00713-0. Source seen: abstract, search-engine excerpts.
- Testable form: (a) Identify pairs of signs that are mirror images of each other in the sign list. For each pair, compare the vectors of positional frequencies (initial, medial, final) and of left and right neighbours. The claim predicts that mirror pairs are more similar to each other than random pairs of signs with matched frequencies. (b) Check whether lines containing a mirrored form are recorded as L/R more often than other lines. The claim is weakened if mirror pairs are no more similar than matched random pairs.
- Feasible with current data: partly. The context statistics can be computed now. Identifying mirror pairs requires the sign-list drawings, which are not yet in machine-readable form in this project.

## B. Size of the sign inventory

### C4. Size of the sign inventory: from 417 to 694
- Claim (source's wording): Estimates of the total number of Indus signs range from 417 (Mahadevan 1977) to 694 (Wells 2015). The ICIT database of Wells and Fuls is described as using a system of more than 700 signs.
- Verbatim quote (if seen): excerpt: "Estimates of the total number of Indus signs range from 417 (Mahadevan, 1977) to 694 (Wells, 2015)".
- Source: Daggumati & Revesz 2021 (D11), https://www.nature.com/articles/s41599-021-00713-0, citing Mahadevan 1977 (A1) and Wells 2015 (A11). For the ICIT sign system: Wells & Fuls, ICIT (A12), https://www.user.tu-berlin.de/fuls/Homepage/indus/menueindus.htm. Source seen: search-engine excerpt of the Daggumati & Revesz abstract; for ICIT, the description recorded in `docs/BIBLIOGRAPHY.md`.
- Testable form: This is a statement about sign lists, not about texts. It becomes testable as follows: count the sign types attested in each corpus, and estimate the total inventory, including unseen signs, with a species-richness estimator (for example Chao1) computed from the numbers of signs seen once and twice. The prediction is that the KP1979 count and estimate fall near the Mahadevan/Parpola range (about 400) and the ICIT count and estimate near the Wells range (about 700). After merging the allograph pairs identified in `docs/SIGN_CONCORDANCE.md`, the ICIT figure should move towards the smaller figure.
- Feasible with current data: yes. The baseline counts are 607 types (ICIT) and 367 types (KP1979) in complete, deduplicated lines (`results/phase2_baseline.md`). The richness estimate and the effect of merging can be computed now.

### C5. About 400 graphemes, about a quarter attested only once
- Claim (close paraphrase): The Indus script has about 400 graphemes, and around 25% of them are attested only once. Parpola accepts this fact but argues that it does not show that the system did not record language.
- Verbatim quote (if seen): none verbatim. The search excerpt paraphrases Parpola as noting that "around 25% of the about 400 graphemes of the Indus script are attested only once".
- Source: Parpola, Asko. 2008. "Is the Indus script indeed not a writing system?" (C2); https://www.harappa.com/content/indus-script-indeed-not-writing-system. Source seen: secondary, search-engine summary of the paper.
- Testable form: In the KP1979 corpus, whose sign list follows the Helsinki classification, compute the proportion of sign types that occur exactly once (i) in all lines and (ii) in deduplicated complete lines. The claim predicts a figure near 25% in a sign list of about 400 signs. Report the same figure for ICIT as a comparison. A figure far from 25% would show that the claim depends on the sign list and corpus version used.
- Feasible with current data: yes. Baseline figures exist: 100 of 367 types occur once in KP1979 and 214 of 607 in ICIT (deduplicated complete lines).

## C. Length of texts, rare signs and repetition

### C6. Inscriptions average about five signs; the longest texts have 14 and 26 signs
- Claim (close paraphrase): Indus texts are very short, averaging about five signs. The longest text in a single line has 14 signs. The longest known texts have 26 signs, written in three lines.
- Verbatim quote (if seen): excerpt from Mahadevan: "the longest known Indus texts, each consisting of 26 signs".
- Source: Mahadevan 1977 (A1), as summarised on lecture slides by Nisha Yadav (2024), https://www.imsc.res.in/~sitabhra/meetings/bitsscripts24/Nisha_Yadav_Lecture.pdf ; Mahadevan, "Agricultural signs in the Indus script", https://ageconsearch.umn.edu/record/308540/files/Agricultural%20signs%20in%20the%20Indus%20script.pdf (year not confirmed). Source seen: secondary and search-engine excerpts.
- Testable form: Compute the mean, median and maximum number of signs per line and per object (all lines of one object joined), in all records and in deduplicated complete records. The claim predicts a mean of about five, a maximum single-line length of about 14 and a maximum object length of about 26. Differences would show how far these figures depend on the corpus and on the counting unit (line or object).
- Feasible with current data: yes. Median line length is already known (4 in both corpora). Object-level length requires grouping lines by object, which both sources allow.

### C7. Average inscription 4.6 signs; the longest on one face has 17 signs
- Claim (source's wording): On Mahadevan's data, the average Indus inscription is 4.6 signs long, and the longest inscription on a single face has 17 signs. Farmer, Sproat and Witzel (2004) use the shortness of the texts as an argument that the signs do not record language.
- Verbatim quote (if seen): excerpt: "On Mahadevan's data, the average Indus inscription is barely 4.6 signs long; the longest on a single face has 17 signs."
- Source: Farmer, Steve. n.d. "Five cases of 'dubious writing' in Indus inscriptions", https://safarmer.com/indusnotes.pdf ; the argument from brevity is in Farmer, Sproat & Witzel 2004 (C1), https://hasp.ub.uni-heidelberg.de/journals/ejvs/article/view/620. Source seen: search-engine excerpt of the notes; the 2004 article only through secondary summaries.
- Testable form: As for C6, compute the mean length per inscribed face. The claim predicts a mean near 4.6 and a maximum near 17 signs per face. The linguistic argument built on this figure is not tested by the length statistic itself; it can only be compared with the lengths of short texts in known writing systems (for example seal legends), which requires comparison corpora.
- Feasible with current data: yes for the length figures. The ICIT records contain a `sides` field, and the KP1979 records mark line divisions. The comparison with other writing systems needs data not yet collected.

### C8. Many singletons and very low-frequency signs
- Claim (source's wording): Besides the high-frequency signs that make up most of the inscriptions, there is a very large number of signs that occur only once ("singletons") or very rarely. Farmer, Sproat and Witzel (2004) present this as evidence against the view that the signs record language.
- Verbatim quote (if seen): excerpt: "At the opposite end of the spectrum from the high-frequency signs that predominate in Indus inscriptions, we find an enormous number of 'singletons' and very low-frequency signs."
- Source: Farmer, n.d., https://safarmer.com/indusnotes.pdf ; Farmer, Sproat & Witzel 2004 (C1), https://hasp.ub.uni-heidelberg.de/journals/ejvs/article/view/620. Source seen: search-engine excerpt of the notes.
- Testable form: Compute the frequency spectrum (the number of sign types occurring once, twice, three times, and so on) and the proportion of tokens covered by signs of frequency 5 or less. Compare these with (a) synthetic corpora of the same size drawn from a Zipf-Mandelbrot distribution fitted to the frequent signs, and (b) samples of the same size from known logo-syllabic corpora, when such corpora are available. The claim, as an argument, predicts that the Indus spectrum has more singletons than writing systems at the same sample size.
- Feasible with current data: yes for the spectrum itself and the synthetic comparison. The comparison with known scripts needs comparison corpora.

### C9. No sign repetition of the kind expected in phonetic scripts
- Claim (close paraphrase): Within Indus inscriptions there is no convincing evidence of the random-looking sign repetition expected in phonetic or semi-phonetic scripts of the time. Where signs repeat, the repetition is of a patterned kind (for example a doubled sign).
- Verbatim quote (if seen): excerpt, as Farmer, Sproat and Witzel's argument is reproduced in a summary of Parpola 2008: "nowhere in Indus inscriptions do we find convincing evidence of the random-looking types of sign repetition expected in contemporary phonetic or semi-phonetic scripts".
- Source: Farmer, Sproat & Witzel 2004 (C1), https://hasp.ub.uni-heidelberg.de/journals/ejvs/article/view/620 ; as reproduced in Parpola 2008 (C2), https://www.harappa.com/content/indus-script-indeed-not-writing-system. Source seen: secondary, search-engine summary.
- Testable form: For each line, record whether any sign occurs more than once, and classify each repetition as adjacent (the same sign twice in a row) or non-adjacent. Compute (a) the proportion of lines with any repetition and (b) the proportion with non-adjacent repetition, as a function of line length. Compare these with the expected rates under within-line shuffling and under random sampling of signs by their corpus frequencies. The claim predicts that non-adjacent repetition is rarer than the random-sampling expectation and that most repetition is adjacent. Ideally the same rates should also be measured in short texts of known phonetic scripts of similar length.
- Feasible with current data: yes for the Indus rates and the random baselines; comparison with other scripts needs further corpora.

### C10. Short seal texts give little reason for repetition
- Claim (close paraphrase): Parpola replies that there is little reason for signs to repeat in short seal texts written in an early logo-syllabic script, and that rare signs are also found in early Chinese writing. Complete sentences are not to be expected on seals, but written noun phrases still count as language-based writing.
- Verbatim quote (if seen): excerpts: "little reason for sign repetition in short seal texts written in an early logo-syllabic script"; "even written noun phrases qualify as language-based script".
- Source: Parpola 2008 (C2), https://www.harappa.com/content/indus-script-indeed-not-writing-system. Source seen: secondary, search-engine excerpts.
- Testable form: The claim predicts that the rate of repetition depends on length and object type. Specifically, the rate of non-adjacent repetition (C9) should rise with line length, and should be higher in the longest texts and on object types with longer texts than on seals, by more than the increase expected from length alone under the random-sampling baseline. If repetition stays at or below the baseline even in the longest texts, the reply is not supported by this corpus.
- Feasible with current data: partly. Object type and length are available, but there are few long texts, so the statistical power for the longest category will be low.

## D. Frequency, position and the "jar" sign

### C11. One sign forms about 10% of the corpus; 69 signs form about 80%
- Claim (source's wording): In the corpus used by Yadav et al. (EBUDS, derived from Mahadevan 1977), 69 signs account for about 80% of the corpus and the most frequent sign (Mahadevan no. 342) alone accounts for 10%. The sign frequencies follow a Zipf-Mandelbrot law.
- Verbatim quote (if seen): excerpt: "69 signs account for about 80% of EBUDS and the most frequent sign (342) alone accounts for 10% of EBUDS".
- Source: Yadav, Nisha et al. 2010. *PLoS ONE* 5(3): e9506 (D2); https://pmc.ncbi.nlm.nih.gov/articles/PMC2841631 ; https://www.arxiv.org/abs/0901.3017. Source seen: search-engine excerpts of the article.
- Testable form: In deduplicated complete lines, compute the token share of the most frequent sign and the number of most frequent signs needed to cover 80% of tokens. The claim predicts a share near 10% and a count near 69 in a Mahadevan-type sign list (KP1979 is the closest available). Fit a Zipf-Mandelbrot curve to the rank-frequency data and report the goodness of fit.
- Feasible with current data: yes.

### C12. Well-defined text-initial and text-final signs; directionality
- Claim (source's wording): The script has well-defined signs that begin and end texts. Sign order shows directionality and strong correlations. The information content of the script lies between that of a completely random and a completely fixed order of signs.
- Verbatim quote (if seen): excerpt: "Our main results are that the script has well-defined signs which begin and end texts, that there is directionality and strong correlations in the sign order".
- Source: Yadav et al. 2010 (D2); https://pmc.ncbi.nlm.nih.gov/articles/PMC2841631. Source seen: abstract, search-engine excerpts.
- Testable form: For each sign with at least 30 occurrences, compute its share of initial and final positions. The claim predicts a set of signs whose initial (or final) share is significantly above the share expected from line length alone (binomial test with correction for the number of signs). Directionality: the bigram matrix should be asymmetric, P(a then b) ≠ P(b then a), beyond a shuffle control. Information: the conditional entropy should lie between that of within-line shuffles and that of a fixed order.
- Feasible with current data: yes. Positional shares have already been computed (`docs/JOURNAL.md`, baseline results).

### C13. The "jar" sign is the most frequent sign
- Claim (close paraphrase): The most frequently used sign is the "jar" sign (Parpola's sign 311 is cited for it). Mahadevan's 1977 concordance gives 1,395 occurrences. Mahadevan states that it makes up ten to twelve percent of all Harappan writing and occurs mostly at the end of texts.
- Verbatim quote (if seen): excerpt from Mahadevan (interview): the sign "occupies ten to twelve percent of all Harappan writing".
- Source: secondary: Wikipedia, "Indus script", https://en.wikipedia.org/wiki/Indus_script (seen only as a search-engine excerpt); Mahadevan, interview on harappa.com, https://www.harappa.com/script/mahadevantext9.html (year not confirmed). Source seen: secondary, search-engine excerpts.
- Testable form: Identify the "jar" sign in each sign list (candidates: ICIT 740; KP 324/325, which the concordance shows are split in KP but merged in ICIT). Test (a) that it is the most frequent sign type, (b) that its token share is between 10% and 12%, and (c) that its share of line-final positions is higher than that of any other sign with at least 100 occurrences.
- Feasible with current data: yes, once the identification with the drawings is confirmed. The final share of ICIT 740 has already been measured as 0.72 (`docs/JOURNAL.md`).

### C14. The "jar" sign as a Dravidian masculine singular suffix
- Claim (close paraphrase): Mahadevan read the terminal "jar" sign as the Dravidian pronominal masculine singular suffix, sometimes with an ideographic meaning of a "sacrificial vessel with food offerings". In an interview he related it to a jar associated in later Indian traditions with priestly ritual, and suggested that it probably represented the ruling elite.
- Verbatim quote (if seen): excerpts, as Mahadevan's view is reported by Mukhopadhyay: "pronominal masculine singular suffix"; "sacrificial vessel with food offerings".
- Source: Mahadevan's reading as reported in Mukhopadhyay 2019 (B8), https://www.nature.com/articles/s41599-019-0274-1 ; Mahadevan, interview, https://www.harappa.com/script/mahadevantext9.html. Source seen: secondary, search-engine excerpts.
- Testable form: A suffix that marks a noun class predicts that the sign (a) occurs at the end of a word-like segment, and so at line end or immediately before another segment; (b) follows a wide variety of preceding signs (high type count of left neighbours relative to its frequency), since it attaches to many stems; and (c) is not limited to one object type. Compute the number of distinct left neighbours of the "jar" sign and compare it with frequency-matched signs. Note that the project has found that the sign is usually followed by ICIT 400 or 090 when it is not final (H3.3 in `docs/JOURNAL.md`), which any suffix reading has to accommodate. The phonetic value itself cannot be tested by internal statistics.
- Feasible with current data: partly. The distributional predictions can be tested now; the reading as such cannot.

### C15. The final sign as a genitive: "the possession of X"
- Claim (close paraphrase): In Parpola's reading, the sign most common at the end of seal inscriptions is a possessive or genitive suffix, so that an object stamped with a seal ending in this sign would be labelled "the possession of X". Parpola also admits that the morphological markers cannot at present be identified with certainty.
- Verbatim quote (if seen): excerpts, from a review of Parpola's method: "Something stamped with a seal ending in this sign would then be labelled as 'the possession of X'"; Parpola concludes "by frankly admitting our present inability to identify morphological markers with any certainty".
- Source: Parpola 1994 (B1), as described in "Parpola's Methodology of Decipherment", https://www.harappa.com/node/3128 (author of the page not confirmed). Source seen: secondary, search-engine excerpts.
- Testable form: A genitive reading of a seal legend predicts that (a) the sign is more frequent at the end of texts on seals than on other object types (for example pottery graffiti or tablets), and (b) the part of the text before it varies more than the part after it. Compute the final share of the sign by object type, with a chi-square test, and compare the number of distinct sequences preceding the sign with the number following it.
- Feasible with current data: partly. Object type is available in both corpora; the linguistic interpretation itself is not testable from the distribution alone.

### C16. The "jar" sign as a metrological noun in tax inscriptions
- Claim (close paraphrase): The rimmed-jar sign, the most frequent sign, occurs mostly in terminal position in inscriptions that relate to taxation. Words meaning "jar" or "pitcher" were used as units of measure in early Vedic texts, the Jātakas and the Arthaśāstra, so the sign may have had a metrological function. Most inscribed objects were administrative tools such as tax tokens, trade licences and metrological records.
- Verbatim quote (if seen): none seen verbatim.
- Source: Mukhopadhyay, Bahata Ansumali. 2018 (revised 2020). "Ancient tax tokens, trade licenses and metrological records? Making sense of Indus inscribed objects through script-internal, contextual, linguistic, and ethnohistorical lenses." SSRN abstract 3189473; https://papers.ssrn.com/author=3583844. Not in `docs/BIBLIOGRAPHY.md`. Source seen: abstract, search-engine excerpt.
- Testable form: A unit of measure predicts that the sign co-occurs with numeral signs (C24) more often than expected from the frequencies of both, and that it stands next to the numerals. Compute the co-occurrence of the "jar" sign with stroke numerals in the same line, and the distribution of distances between them, against a shuffle control. The administrative reading also predicts systematic differences between object types (C29).
- Feasible with current data: partly. The test requires an agreed list of numeral signs (see C24), which has not yet been compiled.

## E. Segmentation and sequence structure

### C17. Longer texts segment into frequent 2-, 3- and 4-sign units
- Claim (source's wording): Indus texts can be segmented using statistically significant signs and sign combinations together with all texts of two, three and four signs. 88% of texts of length five and above can be segmented in this way. The method makes no assumptions about the content of the script.
- Verbatim quote (if seen): excerpt: the authors "can segment 88% of Indus texts (of length 5 and above)".
- Source: Yadav, Nisha, Mayank N. Vahia, Iravatham Mahadevan & Hrishikesh Joglekar. 2008. "Segmentation of Indus texts." *International Journal of Dravidian Linguistics* 37(1); https://www.harappa.com/content/segmentation-indus-texts. Not in `docs/BIBLIOGRAPHY.md`. Source seen: abstract, search-engine excerpt.
- Testable form: Build the inventory of complete texts of length 2 to 4 from the training data. For each held-out line of length 5 or more, test whether it can be divided entirely into segments from that inventory (allowing a single-sign remainder if the original method does so). The claim predicts a coverage near 88%. Compare the coverage with that obtained for lines shuffled within themselves; a structural claim requires coverage clearly above the shuffled value.
- Feasible with current data: yes.

### C18. Recursive structure in segmentation trees
- Claim (close paraphrase): Complex-network analysis of the sign sequences shows patterns, such as recursive structures in the segmentation trees of the sequences, which suggest that a grammar underlies the inscriptions.
- Verbatim quote (if seen): excerpt: "recursive structures in the segmentation trees of the sequences".
- Source: Sinha, Sitabhra, Md Izhar Ashraf, Raj Kumar Pan & Bryan Kenneth Wells. 2011. *Computer Speech and Language* 25 (D4); https://arxiv.org/abs/1005.4997. Source seen: abstract, search-engine excerpt.
- Testable form: Segment each line by splitting recursively at the weakest bigram link (lowest pointwise mutual information). The claim predicts that the same sub-sequences recur as units at different depths of the trees, and as complete short texts, more often than in trees built from lines shuffled within themselves. Measure the proportion of internal tree nodes whose sign sequence also occurs elsewhere as a complete line.
- Feasible with current data: yes.

### C19. Conditional entropy closer to languages than to non-linguistic systems
- Claim (close paraphrase): The conditional entropy of the Indus sign sequences is closer to that of natural languages (Sumerian, Old Tamil, Rigvedic Sanskrit, English) than to that of several non-linguistic systems (DNA, protein sequences, Fortran). The authors later stated that this increases the evidence for the linguistic hypothesis but does not prove it.
- Verbatim quote (if seen): excerpt: "the script's conditional entropy is closer to those of natural languages than various types of nonlinguistic systems".
- Source: Rao, Rajesh P. N. et al. 2009. *Science* 324: 1165 (C3); https://ui.adsabs.harvard.edu/abs/2009Sci...324.1165R/abstract ; reply to criticism in Rao et al. 2010 (C5), https://aclanthology.org/J10-4016/. Source seen: abstract, search-engine excerpts.
- Testable form: Compute the bigram conditional entropy H(next sign | current sign) as a function of the number of most frequent signs retained (the curve used by Rao et al.), for both corpora. Compute the same curve for linguistic and non-linguistic comparison corpora of the same token count. The claim predicts that the Indus curve lies within the range of the linguistic corpora and outside that of the non-linguistic ones. The project's baseline (3.77 and 3.88 bits, about 1 bit below the within-line shuffle) is a single point, not the curve.
- Feasible with current data: partly. The Indus curves can be computed now; the comparison corpora have not yet been collected.

### C20. Entropy-type measures classify the Indus system as non-linguistic
- Claim (close paraphrase): With a larger set of comparison corpora, the statistical methods previously proposed for distinguishing writing from non-linguistic symbol systems do not work as published. Sproat's own procedure classifies both the Indus and the Pictish systems as non-linguistic.
- Verbatim quote (if seen): none seen verbatim.
- Source: Sproat, Richard. 2014. *Language* 90(2): 457–481 (C7); https://research.google/pubs/a-statistical-comparison-of-written-language-and-nonlinguistic-symbol-systems/ ; press release https://www.eurekalert.org/news-releases/697414. Source seen: abstract and press release, search-engine excerpts.
- Testable form: Apply the published measures (conditional entropy, Lee et al.'s Ur and Cr statistics, and repetition rate) to the Indus corpora and to Sproat's comparison corpora, and train the classifier described in the paper on the comparison corpora only. The claim predicts that the Indus corpora are assigned to the non-linguistic class. The test should be repeated on both corpora, since the result may depend on the sign list.
- Feasible with current data: partly. The Indus side can be computed now; Sproat's comparison corpora have not yet been obtained.

### C21. A Markov model of sign order; West Asian texts differ in sign order
- Claim (close paraphrase): A first-order Markov (bigram) model captures the dependencies in Indus sign order and can be used to restore missing signs in damaged inscriptions. Indus texts found in Mesopotamia and elsewhere in West Asia use the same signs as texts from the Indus region but arrange them differently, which suggests that they may express different content.
- Verbatim quote (if seen): none seen verbatim.
- Source: Rao, Rajesh P. N. et al. 2009. *PNAS* 106(33): 13685–13690 (D1); https://homes.cs.washington.edu/~rao/PNASIndus.pdf ; press release https://www.washington.edu/news/2009/08/03/computers-unlock-more-secrets-of-the-mysterious-indus-valley-script/. Source seen: abstract and press release, as search-engine excerpts.
- Testable form: (a) Restoration: train a smoothed bigram model on training lines and mask one sign at random in each held-out line; report the proportion of masked signs ranked first and within the top five. (b) West Asia: compute the per-sign log-likelihood of lines from the regions "Mesopotamia", "Persian Gulf" and "Iranian Plateau" (ICIT `region` field) under a model trained on Indus-region lines, and compare it with held-out Indus-region lines of the same length distribution (permutation test). The claim predicts a significantly lower likelihood for the West Asian lines.
- Feasible with current data: yes. The ICIT data contain 38 records from these three regions, so the West Asian test has low power and should be reported with that limitation.

## F. Proposed readings and numerals

### C22. The fish sign read as Dravidian *mīn* "fish" = "star"
- Claim (close paraphrase): Following Heras, Parpola reads the fish sign by rebus through the Dravidian word *mīn*, which means both "fish" and "star". Modified fish signs are read as names of planets and stars; for example a "halved" fish is read as *pacu mīn*, Mercury. Mahadevan accepts the homophony as a good one but notes that it has not been proved.
- Verbatim quote (if seen): excerpt, from Mahadevan's assessment: "although I readily admit that it has not been proved".
- Source: Parpola 1994 (B1), as presented in "The 'Fish' Signs", https://www.harappa.com/node/3129 , and "The Planets", https://www.harappa.com/node/3130 (author of the pages not confirmed). Source seen: secondary, search-engine excerpts.
- Testable form: The rebus reading itself cannot be tested by sign statistics. Its distributional consequences can be: if the fish signs form a semantic class (heavenly bodies, used as names or titles), (a) plain and modified fish signs should be interchangeable in the same contexts (their left and right neighbour distributions should be more similar to each other than to frequency-matched signs); and (b) fish signs should occupy a consistent position in the line. Identify the fish-sign family in each sign list and compute neighbour-distribution similarity against a permutation control.
- Feasible with current data: partly. The test needs the fish-sign family to be identified in both sign lists from the drawings.

### C23. Numeral plus fish as names of asterisms
- Claim (close paraphrase): Sequences of a numeral followed by a fish sign are read as names of star groups: 3 + fish as Mṛgaśiras, 6 + fish as Kṛttikā (the Pleiades), 7 + fish as the Seven Sages (Saptarṣi, Ursa Major). The reading is supported by Old Tamil *aṟu-mīn* "six fish", meaning "six stars", the Pleiades. The bulletin argues that these identifications need reappraisal.
- Verbatim quote (if seen): none seen verbatim.
- Source: Indus Research Centre, Roja Muthiah Research Library. 2011. *Indus Research Centre Bulletin* No. 2 (author not confirmed); https://rmrl.in/wp-content/uploads/2023/08/Indus-Research-Centre-Bulletin-No-2-Aug-2011.pdf ; the reading goes back to Heras and Parpola (B1). Not in `docs/BIBLIOGRAPHY.md` as a separate entry. Source seen: secondary, search-engine excerpt.
- Testable form: Count the sequences "n strokes + fish sign" for each n. The reading predicts (a) that the fish sign is preceded by stroke numerals more often than other signs of similar frequency, and (b) that the numbers attested before the fish are concentrated on the values that have astronomical names (3, 6, 7) rather than spread across 1 to 9. Compare the distribution of n before the fish sign with the distribution of n before all other signs (chi-square test).
- Feasible with current data: partly. It requires the identification of the fish signs and of the stroke numerals in both sign lists.

### C24. Stroke numerals up to nine; semicircles as tens
- Claim (source's wording): The numerals are a set of short stroke signs with up to nine strokes, arranged in one or two tiers. Groups of vertical strokes (but not all of them) stand for ones, and groups of semicircles probably stand for tens.
- Verbatim quote (if seen): excerpts: "The numerals are identified as a set of short stroke signs comprising up to nine strokes arranged in one or two tiers."; "The groups of vertical strokes (but not all of them) stand for ones and groups of semicircles probably stand for tens."
- Source: Parpola, as presented at https://www.harappa.com/script/parpola12.html (from Parpola's work on the script; the exact publication was not confirmed). Source seen: secondary, search-engine excerpt.
- Testable form: Identify the stroke signs (1 to 9 strokes) and the semicircle signs in each sign list. The numeral reading predicts that (a) stroke signs occupy a consistent position relative to the sign they precede, as numerals before a counted noun would; (b) stroke signs of different counts are interchangeable in the same contexts (high similarity of neighbour distributions); (c) semicircle signs precede stroke signs when both occur together, as tens before ones; and (d) two stroke signs rarely stand next to each other except in the tens-then-ones order. Test each against a permutation control.
- Feasible with current data: partly. The sign identification has to be done first; the ICIT `class` field contains a code "NU" (167 records) that may mark numerals, and its meaning must be checked.

### C25. The numeral base is unknown, possibly 8 or 10
- Claim (source's wording): By about 2500 BC the Indus script had moved to an abridged numeral system, but it is not known for certain what its base was or whether more than one base was used. A decimal reading is plausible because the maximum stroke count reaches nine when long strokes are included; a base of eight is also considered.
- Verbatim quote (if seen): excerpt: "we do not know for sure the base or even whether they used more than one".
- Source: Reddy, Ooha Lakkadi. 2025. arXiv: 2503.21074 (D14); https://arxiv.org/pdf/2503.21074. Source seen: search-engine excerpt of the preprint.
- Testable form: Compute the distribution of stroke counts (1 to 9, short and long strokes separately). A base-10 system with separate signs for tens predicts that counts up to 9 are attested and that 10 or more strokes never occur in a single group. A base-8 system predicts a gap or sharp drop after 7. Also test whether particular stroke counts co-occur with particular object types (for example tablets).
- Feasible with current data: partly, for the same reason as C24.

### C26. A four-sign sequence read as "trader, merchant" plus a title
- Claim (close paraphrase): Mahadevan argues for the Dravidian character of the Indus language on the basis of evidence interlocked at three levels: the corpus of Indus texts, survivals in Old Tamil, and survivals in Vedic sources. A frequent four-sign sequence is analysed as a phrase of two parts, AB and CD, and sign A is read as a word meaning "exchange (of goods), barter; one who barters, trader, merchant". He did not claim a complete decipherment.
- Verbatim quote (if seen): excerpts: the interpretation rests on "firmly inter-locked evidence at three levels"; sign A is read as "exchange (of goods), barter; one who barters, trader, merchant".
- Source: Mahadevan, Iravatham. 2014. *Dravidian Proof of the Indus Script via the Rig Veda: A Case Study* (B7); https://www.harappa.com/content/dravidian-proof-indus-script-rig-veda-case-study ; https://rmrl.in/bulletin/bulletin-No-4-Nov-2014.pdf. Source seen: abstract and secondary, search-engine excerpts.
- Testable form: The structural part of the claim is testable. (a) The four-sign sequence should divide into two pairs: the pointwise mutual information between the second and third signs should be lower than within each pair, and each pair (AB, CD) should occur independently in other texts more often than the split ABC + D or A + BCD. (b) If AB is an occupational term, sign A should be followed by a limited set of signs and AB should occur in a consistent position. The Dravidian reading itself cannot be tested by internal statistics.
- Feasible with current data: partly. The sequence must first be identified in both sign lists from the published drawings.

## G. Script type and content

### C27. The signs are logograms in functional classes, not phonograms
- Claim (source's wording): Indus signs represented different content morphemes and functional morphemes, not phonograms used for spelling. Semantic co-occurrence restrictions show that most inscriptions were logographic. The signs can be sorted into nine functional classes, and the study assigns no sound values.
- Verbatim quote (if seen): excerpts: "Indus signs represented different content-morphemes and functional-morphemes—not phonograms used for spelling"; "it strongly suggests that most of the Indus inscriptions were logographic in nature".
- Source: Mukhopadhyay, Bahata Ansumali. 2019. *Palgrave Communications* 5 (B8); https://www.nature.com/articles/s41599-019-0274-1. Source seen: abstract, search-engine excerpts.
- Testable form: A phonographic (syllabic) system predicts that frequent signs combine freely, so that the matrix of observed bigrams is dense; a logographic system with semantic co-occurrence restrictions predicts many frequent sign pairs that never occur together although their frequencies would lead us to expect them. Count the frequent sign pairs (both signs with at least 30 occurrences) whose expected count is at least 5 but whose observed count is zero, and compare with within-line shuffles and, when available, with corpora of short texts in known syllabic and logographic scripts. The nine classes can be compared with distributional clusters (H3.2 in `docs/JOURNAL.md`) by the adjusted Rand index, if the class assignments are published in usable form.
- Feasible with current data: partly. The internal statistic can be computed now; the comparison with known scripts and the class assignments are not yet available.

### C28. Seal texts are not names of seal owners
- Claim (close paraphrase): The hypothesis that the seals carry Proto-Dravidian or Proto-Indo-European names of their owners does not hold (2019, as reported in the press). The inscriptions did not encode any proper noun, such as personal names, place names or names of specific organizations (2023).
- Verbatim quote (if seen): excerpts: press report of the 2019 study: "the popular hypothesis that the seals were inscribed with Proto-Dravidian or Proto-Indo-European names of the seal-owners does not hold water"; 2023 article: "the inscriptions did not encode any proper noun, such as anthroponyms, toponyms, or names of specific organizations".
- Source: Mukhopadhyay 2019 (B8), as reported in the press, reposted at https://groups.google.com/g/mintamil/c/y6qwMOl8368/m/FQn4jSkjCQAJ ; Mukhopadhyay 2023 (B9), https://www.nature.com/articles/s41599-023-02320-7. Source seen: secondary (press report) for 2019; search-engine excerpts of the article for 2023.
- Testable form: Personal names in a population of seal owners predict a large number of distinct, rarely repeated texts, with low reuse of whole texts across sites, and a diverse "name" part followed by a small set of recurring elements (titles, case markers). Formulaic administrative messages predict a smaller set of texts or text templates that recur across sites and object types. Measure (a) the proportion of distinct seal texts that occur more than once, (b) the proportion that occur at more than one site, and (c) the type-token ratio of seal texts, and compare with simulated name corpora built from a known naming system of comparable structure. These statistics can distinguish the two expectations only in degree; they cannot exclude names directly.
- Feasible with current data: partly. Statistics (a) to (c) can be computed now; a suitable comparison corpus of names is not yet available.

### C29. Tablets as licences for trades, crafts or commodities
- Claim (source's wording): Building on structural analyses showing that the script was semasiographic and/or logographic, the combinatorial patterns of signs and the geographical distribution of the inscriptions suggest that the tablets were possibly licences for specific trades, crafts or commodities issued to tax collectors, traders and artisans. The seals were mainly used to enforce rules relating to taxation, trade and commodity control.
- Verbatim quote (if seen): excerpt: "such tablets were possibly trade/craft/commodity-specific licenses issued to tax-collectors, traders, and artisans".
- Source: Mukhopadhyay, Bahata Ansumali. 2023. *Humanities and Social Sciences Communications* 10: 972 (B9); https://www.nature.com/articles/s41599-023-02320-7. Source seen: abstract, search-engine excerpts.
- Testable form: The claim predicts that sign content differs systematically by object type, and that tablet texts fall into a limited number of recurring templates. (a) Compare sign distributions of seals and tablets (chi-square on sign frequencies, and a classifier predicting object type from signs, evaluated on held-out data). (b) Measure the proportion of tablet texts that recur exactly and the proportion that share a text with a seal. (c) Test whether tablet texts co-occur with numeral signs (licence fees, according to the summary) more often than seal texts.
- Feasible with current data: partly. Object type is available in both corpora (ICIT `type`: SEAL, TAB, POT, TAG and others). The numeral identification of C24 is needed for part (c).

### C30. Seal motifs as emblems of guilds or governing bodies
- Claim (source's wording): The animal-centred iconography of the seals (bull, goat, "unicorn", tiger, elephant, scorpion and others) most probably functioned as different markers. The iconography of seals and tablets may have been the emblems of guilds, rulers or governing bodies.
- Verbatim quote (if seen): excerpt: "the seal/tablet iconographies might have been the emblems of the guilds, rulers, and/or governing bodies."
- Source: Mukhopadhyay 2023 (B9); https://www.nature.com/articles/s41599-023-02320-7. Source seen: search-engine excerpts of the article.
- Testable form: If motifs mark issuing bodies and the texts state the content of a rule or licence, the text should be largely independent of the motif, or should depend on it only through a few signs (for example a sign naming the body or its domain). (a) Test the independence of sign frequencies and motif (chi-square or mutual information between motif and the presence of each sign, with correction for the number of signs). (b) Train a classifier to predict the motif from the text and evaluate it on held-out seals; accuracy no better than predicting the majority motif (the "unicorn") would indicate independence. (c) Test whether particular motifs are concentrated at particular sites, as emblems of regional bodies would be.
- Feasible with current data: yes. The ICIT `symbol` field records the motif (for example `Bull1` variants for the "unicorn", `Zebu`, `Elep`, `Rhin`, `Tigr`, `Gaur`), and KP1979 has an `icon_code` field. The motif codes need to be grouped consistently.

### C31. Tablets as ration records; seals generating tokens
- Claim (close paraphrase): By comparison with proto-Elamite and proto-cuneiform texts, the miniature Indus tablets may have recorded rations for porters or labourers. The stamp seals may have been used to produce tokens and sealings for recurring exchanges of goods, grain, animals and labour, rather than only to mark ownership.
- Verbatim quote (if seen): none seen verbatim.
- Source: Rao, Rajesh P. N. 2018. "The Indus script and economics: A role for Indus seals and tablets in rationing and administration of labor." In a 2018 Archaeopress volume in honour of J. Mark Kenoyer, 518–525 (as given in the search excerpt); arXiv: 1812.00049; https://arxiv.org/pdf/1812.00049. Not in `docs/BIBLIOGRAPHY.md`. Source seen: abstract, search-engine excerpt.
- Testable form: A ration-record function predicts that tablet texts (a) contain numerals more often than seal texts, (b) consist of a small set of recurring templates with a variable numeral slot, and (c) share their non-numeral part with seal texts. Measure the rate of numeral signs on tablets and on seals, the number of distinct templates after the numerals are replaced by a placeholder, and the overlap of templates between tablets and seals.
- Feasible with current data: partly. Object types are available; the numeral list of C24 is needed.

### C32. Identical texts on Harappa miniature tablets, shared with a seal
- Claim (close paraphrase): Excavations at Harappa (1997) found a group of 22 three-sided miniature tablets (first described as "tiny steatite seals") carrying identical inscriptions, with further copies found elsewhere on the site. The inscription on one side of these tablets is identical to the last two signs of a seal found nearby.
- Verbatim quote (if seen): excerpts: "22 three-sided 'tiny steatite seals' containing identical inscriptions"; "The inscription on one of the three sides of the tablets is identical to the last two signs on the seal which was discovered in a nearby area."
- Source: Meadow, Richard H. & J. Mark Kenoyer, Harappa Archaeological Research Project, as reported on harappa.com, https://www.harappa.com/indus5/79.html and https://www.harappa.com/slide/90.html (year of the report taken from the excerpt). Not in `docs/BIBLIOGRAPHY.md`. Source seen: secondary, search-engine excerpts.
- Testable form: (a) Among Harappa tablets in the corpus, count the groups of objects with identical texts and compare their size with the size of identical-text groups among seals. (b) For each tablet text, test whether it occurs as the final part (suffix) of a seal text more often than random sign sequences of the same length drawn from the tablet sign distribution. The claim predicts large identical-text groups among tablets and an excess of tablet texts that match the ends of seal texts.
- Feasible with current data: yes. Both corpora record site and object type, and duplicates are retained in the raw data even though default statistics use deduplicated lines.

### C33. The script is a proto-abugida recording Sanskrit
- Claim (close paraphrase): Using cryptanalytic techniques, every sign can be read; the script is a proto-abugida, and the inscriptions are in post-Vedic Sanskrit. The decipherment is claimed to be correct because the corpus can be read beyond the unicity distance (Shannon's criterion for a credible solution of a cryptogram). The work has not been peer-reviewed and has not been accepted by scholars; critics dispute that the unicity distance is a criterion of correctness.
- Verbatim quote (if seen): none seen verbatim in the paper. Excerpt from the author's website as summarised: the correctness "is judged simply by being able to read the corpus beyond the unicity distance".
- Source: Yajnadevam (Bharath Rao). n.d. "A cryptanalytic decipherment of the Indus Script." Preprint, not peer-reviewed (B10); https://academia.edu/78867798/A_cryptanalytic_decipherment_of_the_Indus_Script ; discussion at https://list.indology.info/pipermail/indology/2025-March/060315.html ; press report https://theprint.in/feature/here-are-two-indians-whove-tried-to-crack-the-indus-script-in-last-10-years/2452190/. Source seen: search-engine excerpts of the preprint, the mailing-list discussion and the press report.
- Testable form: The proposed sign values are assigned on the whole corpus, so they cannot be tested on it directly. A fair test fixes the published sign-value table and applies it, unchanged, to lines not available when the table was made (for example lines from CISI volumes 3.2 and 3.3 that are not in the source corpus). The claim predicts that the readings of these new lines are well-formed Sanskrit at a rate clearly above that obtained (i) by applying a randomly permuted sign-value table, and (ii) by applying the same procedure to a control language with a dictionary of equal size. The rate of well-formed readings must be judged by a procedure fixed in advance (for example a dictionary and morphology checker).
- Feasible with current data: partly. The ICIT-style transcription used here contains `sanskrit` and `translation` columns that appear to derive from this decipherment; under `docs/METHOD.md` they are never used as input. A test needs the sign-value table in machine-readable form and new lines outside the source corpus.

## H. Comparative and methodological claims

### C34. The Indus statistics fit no non-linguistic baseline cleanly
- Claim (close paraphrase): Compared with two generated non-linguistic baselines (a heraldic emblem system and an administrative coding system) and seven real non-linguistic corpora, including Sproat's (2014) data, the Indus corpus (1,916 deduplicated inscriptions, 584 signs, 11,110 tokens; mean length 4.4 signs, range 2 to 17) does not match either non-linguistic model cleanly, and no attested non-linguistic system reproduces its full statistical profile. The author does not claim that this settles the question.
- Verbatim quote (if seen): none seen verbatim.
- Source: Nair, Ashish. 2026. "How non-linguistic is the Indus sign system? A synthetic-baseline scorecard." arXiv: 2604.17828 (D16), preprint, not peer-reviewed; https://arxiv.org/abs/2604.17828. Source seen: abstract and parts of the full text, as search-engine excerpts.
- Testable form: Reproduce the scorecard (brevity, cross-text repetition, singletons, positional rigidity, conditional entropy) on both corpora of this project, using the published definitions, and generate the two synthetic baselines with matched numbers of texts and signs. The claim predicts that on each corpus the Indus values fall outside the range of at least one metric for each baseline. Because the source data of the preprint derive from ICIT, the result on KP1979 is the more independent check.
- Feasible with current data: partly. The Indus metrics and synthetic baselines can be produced now; the real non-linguistic corpora must be obtained.

### C35. The statistical measures are not specific to language
- Claim (close paraphrase): An inference from a statistic to language requires that the observed value be unusual among plausible structured non-languages. A generated emblem system with compositional meanings but no sound values (SIGIL, 3,000 texts) receives the same classification as the Indus corpus on every repetition, directional-asymmetry and vocabulary test scored, and reproduces Indus-like values on entropy, frequency, positional, predictive, classifier and network measures. The measures detect organisation but cannot by themselves establish that speech is encoded.
- Verbatim quote (if seen): excerpt: "the reported outcome must be unusual among plausible structured non-languages".
- Source: Raghavendra, Nikhil. 2026. "On the non-specificity of statistical measures used in script decipherment." arXiv: 2608.02999 (D17), preprint, not peer-reviewed; https://arxiv.org/pdf/2608.02999. Source seen: abstract, search-engine excerpts.
- Testable form: For each statistic used in C2, C12, C17, C18 and C19, compute its value on the Indus corpora and its distribution over an ensemble of generated non-linguistic systems with compositional structure, matched in corpus size, sign inventory and length distribution. The claim predicts that the Indus values fall inside the central 95% of the non-linguistic ensemble for every statistic. Any statistic for which the Indus value lies outside that range would count against the claim for this corpus.
- Feasible with current data: partly. The Indus values can be computed now; the generator of the comparison systems must be obtained or rebuilt from the published description.

---

## Summary of feasibility

- Testable now with the two corpora (subject to confirming sign identifications where noted): C2, C4, C5, C6, C7, C8, C9, C11, C12, C13, C17, C18, C21, C30, C32.
- Partly testable now: C1, C3, C10, C14, C15, C16, C19, C20, C22, C23, C24, C25, C26, C27, C28, C29, C31, C33, C34, C35. The usual missing pieces are (a) identification of named sign families (numerals, fish signs, mirror pairs) from the sign-list drawings, (b) comparison corpora of known scripts and non-linguistic systems, and (c) inscriptions outside the source corpora for testing proposed readings.
- No claim in the register is wholly untestable in distributional form, but the phonetic values proposed in C14, C22, C23, C26 and C33 cannot be confirmed by internal statistics alone; only their distributional consequences can be tested.
