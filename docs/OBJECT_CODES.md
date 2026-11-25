# Object-type and text-class codes in the ICIT-style corpus

This note records what the codes in the `type` and `class` columns of `data/raw/icit2025.csv` mean, and how sure we can be. The file has 5,679 rows (one row per text line or side; 4,694 distinct object numbers in the `id` column).

## Sources consulted

| Ref | Source | What it gives |
|---|---|---|
| Y | Yajnadevam, `indus-website`, file `src/data/usefulMaps.js` (github.com/yajnadevam/indus-website, shallow clone, November 2026) | A map named `qualityMap` from `type` codes to coarse display labels: Seal, Tablet, Tag, Pottery, Rod, Bangle, Misc., Other, and "Impression" for `IMPL` with the author's own comment "Not too sure about this". It maps `TAB:C` to "Tag". No sub-type meanings and no `class` codes. |
| L | Yajnadevam, `lipi` (github.com/yajnadevam/lipi) | Contains `src/assets/data/inscriptions.csv`, the same table as our CSV, but no code table for `type` or `class`. |
| W | B. K. Wells, *The Archaeology and Epigraphy of Indus Writing* (Archaeopress, 2015), ch. 3 "continuum of text classification of Indus texts by sign distribution and clustering", with an appendix on automated segmentation by A. Fuls | Seen only through search-engine excerpts of the table of contents and figure captions (Perlego and Archaeopress pages); the book itself was not available. The excerpts name the text classes "Patterned" vs "Complex", "Long Patterned" (6+ signs), "Short Patterned", "Long Complex" and "Short Segment"; a second excerpt (citing Wells 2015 via Fuls 2024, *Iranian Journal of Archaeological Studies*) speaks of "Long and Short Pattern texts (with initial, medial and terminal clusters) and Single Segments". |
| F | A. Fuls, *Documentation of the Online Indus Writing Database* (Berlin 2010; epigraphica.de / user.tu-berlin.de/fuls) | Seen only through a search excerpt; it defines sign-function codes (ITM, LOG, NUM, PTM, SHN, ...) but the excerpt shows no object-type or text-class table. The PDF itself could not be downloaded (host blocked from this environment). |
| E | Search-engine summary (no page identified; probably drawn from Mukhopadhyay 2023, *Humanities and Social Sciences Communications* 10, which uses ICIT) | States ICIT object types SEAL (seals), TAG ("clay objects with impressions of intaglio seals"), BNGL (bangles), ROD ("cylindrical shaped artefacts of any material"), IMPL (implements or tools), BEAD, MDLN (medallions), MISC (other types), and tablet sub-types TAB:B (bas-relief), TAB:I (incised) and copper tablets. The excerpt was garbled (it called the copper-tablet code `TAG:R`). Treated as a weak source; each claim below is checked against the data. |
| D | The CSV itself | Counts and cross-tabulations computed with pandas (scripts kept outside the repository). "Inferred from the data" means the meaning is read off these figures only. |

Pages on epigraphica.de, user.tu-berlin.de, archaeopress.com, nature.com and arxiv.org could not be fetched from this environment, so the primary ICIT documentation has not been read directly. Every meaning below that rests only on E or W excerpts should be checked against the ICIT help pages or Wells 2015 when they become accessible.

## Object type (`type` column)

Data columns: count = rows in the CSV; then the three commonest values of `material`, `shape`, `symbol` (motif) and `site` ("-" = not recorded).

| Code | Meaning | Source or evidence | Count | Material | Shape | Symbol | Sites |
|---|---|---|---:|---|---|---|---|
| `SEAL:S` | Seal, square, normally with an animal motif (standard stamp seal) | "Seal": Y. "Square" and "motif": inferred from the data (square 1,739 of 1,777; motif present in most rows) | 1777 | Steatite 1459, - 270, Faience 23 | square 1739, - 35, rectangular 2 | Bull1:W 407, Bull1 252, Bull1:J 202 | Mohenjo-daro 1100, Harappa 318, Dholavira 87 |
| `SEAL:R` | Seal, rectangular, usually without motif (inscription-only seal) | "Seal": Y. "Rectangular, no motif": inferred from the data (rectangular or cuboid-convex 341 of 388; symbol None 365) | 388 | Steatite 270, - 94, Clay 12 | cuboid-convex 188, rectangular 153, cuboid 28 | None 365, - 11, Bult 9 | Mohenjo-daro 202, Harappa 101, Dholavira 34 |
| `SEAL:C` | Seal, circular (includes "Gulf-type" round seals) | "Seal": Y. "Circular": inferred from the data (shape circular 30 of 32; finds at Ur and other non-Indus sites) | 32 | - 19, Steatite 13 | circular 30, - 2 | Gaur 18, None 4, - 3 | Mohenjo-daro 7, Unknown 5, Ur 5 |
| `SEAL:CY` | Cylinder seal | "Seal": Y. "Cylinder": inferred from the data (shape cylindrical 9 of 9, cross-section circular 9) | 9 | Steatite 5, - 3, Stone 1 | cylindrical 9 | None 3, Scene 2, Phyt 1 | Harappa 3, Unknown 2, Kalibangan 1 |
| `SEAL:L` | Seal, sub-type L; meaning of "L" unknown | "Seal": Y. Only 2 rows (oval agate seal from Lothal; rectangular-rounded steatite from Mohenjo-daro); data too thin to infer the letter | 2 | Agate 1, Steatite 1 | oval 1, rectangular-rounded 1 | None 2 | Lothal 1, Mohenjo-daro 1 |
| `SEAL` | Seal, sub-type not recorded | Y; inferred from the data (shape mostly unrecorded, 70 of 82) | 82 | Steatite 50, - 27, metal 1 | - 70, square 5, rectangular 3 | - 53, None 24, Mult 1 | Mohenjo-daro 41, Harappa 18, Dholavira 14 |
| `TAB:B` | Tablet in bas-relief (moulded) | "Tablet": Y. "Bas-relief": E. Fits the data: faience and clay (moulded materials), rectangular/cylindrical/prism, mostly two-sided (sides = 2 in 734 rows), almost all from Harappa | 1108 | Faience 583, - 265, Clay 207 | rectangular 498, cylindrical 154, prism 116 | None 663, Mult 80, Gavi 52 | Harappa 939, Mohenjo-daro 144, Kalibangan 6 |
| `TAB:I` | Incised tablet | "Tablet": Y. "Incised": E. Fits the data: steatite (a carved material), small rectangular/prism objects, two-sided, Harappa | 952 | Steatite 789, - 150, Faience 6 | rectangular 462, prism 175, - 139 | None 778, Bult 87, Fish 37 | Harappa 921, Dholavira 18, Mohenjo-daro 8 |
| `TAB:C` | Copper tablet | "Copper tablets": E (code garbled there). Inferred from the data: material Copper in 229 of 230 rows, all but one from Mohenjo-daro. Y labels it "Tag", which the data do not support | 230 | Copper 229, - 1 | rectangular 166, square 45, rectangular-round 13 | None 72, Othr 57, - 22 | Mohenjo-daro 229, Kalibangan 1 |
| `TAG` | Tag (sealing): clay object bearing a seal impression; sub-type not recorded | "Tag": Y. "Clay object with impression of an intaglio seal": E. Fits the data: clay/terracotta, seal motifs (Bull1 54), mostly from Lothal and Dholavira | 172 | Clay 99, - 43, Terracotta 21 | - 141, rectangular 11, square 10 | - 94, Bull1 54, None 14 | Lothal 70, Dholavira 69, Kalibangan 10 |
| `TAG:L` | Tag (sealing), sub-type L; letter unknown | "Tag": Y. Data: clay, Bull1 motif, Kalibangan 18; 12 rows record 4 sides | 40 | Clay 20, - 20 | - 36, circular 3, square 1 | Bull1 17, None 7, - 6 | Kalibangan 18, Harappa 6, Lothal 6 |
| `TAG:P` | Tag (sealing), sub-type P; letter unknown | "Tag": Y. Data: clay, mostly circular | 15 | Clay 14, - 1 | circular 9, square 3, - 2 | Bull1 8, None 3, Othr 1 | Mohenjo-daro 6, Harappa 4, Lothal 3 |
| `TAG:B` | Tag (sealing), sub-type B; letter unknown | "Tag": Y. Data: 10 clay sealings from Lothal, all with elephant motif and class IT, length 4 (apparently impressions of one seal) | 10 | Clay 9, - 1 | square 6, - 4 | Elep 10 | Lothal 10 |
| `TAG:O` | Tag (sealing), sub-type O; letter unknown | "Tag": Y | 6 | Clay 5, Faience 1 | - 3, square 2, rectangular 1 | Bull1 5, None 1 | Mohenjo-daro 5, Lothal 1 |
| `TAG:W` | Tag (sealing), sub-type W; letter unknown | "Tag": Y | 6 | Clay 4, - 2 | - 6 | - 4, Bull1 2 | Mohenjo-daro 3, Rakhigarhi 2, Lothal 1 |
| `TAG:C` | Tag, sub-type C; letter unknown | "Tag": Y. Data: faience/paste, cuboid, Mohenjo-daro; not clay, so possibly not a sealing | 4 | Faience 3, Paste 1 | cuboid 3, - 1 | Mult 4 | Mohenjo-daro 4 |
| `TAG:R` | Tag (sealing), sub-type R; letter unknown | "Tag": Y. E calls `TAG:R` copper tablets, but all 4 rows are clay, so E is not followed here | 4 | Clay 4 | - 4 | None 3, Bull1 1 | Harappa 3, Mohenjo-daro 1 |
| `TAG:PC` | Tag, sub-type PC; letter unknown | Not in Y. Data: 5 rows from Dholavira, no material or shape recorded | 5 | - 5 | - 5 | - 5 | Dholavira 5 |
| `POT:T:g` | Pottery: graffito (sign scratched on a pot or sherd) | "Pottery": Y. "Graffito" for "g": inferred from the data (clay sherds without recorded shape or motif; class NU and single signs common) and from the usual pairing of incised vs stamped pottery marks; no source found for the letter | 539 | Clay 480, - 43, Terracotta 6 | - 539 | None 369, - 169, Mult 1 | Harappa 293, Kalibangan 89, Mohenjo-daro 48 |
| `POT:T:s` | Pottery: stamped (seal-impressed) inscription | "Pottery": Y. "Stamped" for "s": inferred from the data (some rows record rectangular or square shapes, i.e. the stamp outline); no source found for the letter | 73 | Clay 70, Steatite 1, - 1 | - 50, rectangular 14, square 8 | None 71, - 1, Bull1 1 | Harappa 50, Mohenjo-daro 22, Tepe Yahya 1 |
| `POT:T:S` | Probably a spelling variant of `POT:T:s` | Inferred (single row, Harappa, clay) | 1 | Clay 1 | - 1 | None 1 | Harappa 1 |
| `POT:T:p` | Pottery, sub-type p; letter unknown (perhaps painted) | "Pottery": Y. "Painted" is a guess not supported by any source; the data only show sherds from smaller sites (Surkotada, Shikarpur, Gumla) | 19 | Ceramic 9, Clay 6, - 4 | - 19 | - 11, None 8 | Surkotada 4, Shikarpur 3, Gumla 2 |
| `POT:M` | Pottery, sub-type M; meaning unknown | Not in Y. 3 rows, Harappa | 3 | Clay 2, - 1 | - 3 | - 2, None 1 | Harappa 3 |
| `POT:D` | Pottery, sub-type D; meaning unknown | Not in Y. 1 row, Harappa | 1 | Ceramic 1 | - 1 | None 1 | Harappa 1 |
| `BNGL` | Bangle | Y; E. Fits the data (stoneware 40 of 50; stoneware bangles are a known inscribed class at Mohenjo-daro and Harappa) | 50 | Stoneware 40, - 5, Clay 2 | - 50 | None 49, - 1 | Mohenjo-daro 41, Harappa 7, Bala-kot 1 |
| `ROD` | Rod: cylindrical object of any material (mostly ivory rods/sticks) | Y ("Rod"); E. Fits the data (ivory 35, bone 4) | 42 | Ivory 35, Bone 4, Copper 3 | - 37, conical 2, cylindrical 2 | None 37, Bult 2, Mult 1 | Mohenjo-daro 32, Harappa 7, Kalibangan 2 |
| `IMPL` | Implement (tool or weapon) | E ("implements or tools"). Fits the data: copper 16, gold 2, shapes dagger 2 and axe 1. Y's label "Impression" is marked unsure by its author and is not supported by the data | 23 | Copper 16, Terracotta 5, Gold 2 | - 15, circular 5, dagger 2 | None 17, Bull1 5, - 1 | Mohenjo-daro 10, Kanmer 5, Harappa 4 |
| `BEAD` | Bead | E. 2 rows (elliptical and square) | 2 | Clay 1, - 1 | elliptical 1, square 1 | None 1, Othr 1 | Harappa 2 |
| `MDLN` | Medallion | E. 2 rows, both circular, two-sided | 2 | - 2 | circular 2 | None 2 | Mohenjo-daro 2 |
| `MISC` | Miscellaneous / other object types | Y ("Misc."); E. Includes the Dholavira signboard (note field) | 81 | Terracotta 23, - 14, Clay 13 | - 65, square 2, circular 2 | None 63, - 13, Elep 1 | Harappa 28, Kalibangan 23, Mohenjo-daro 10 |
| `Unknown` | Object type not recorded | Self-explanatory; 1 row | 1 | - 1 | - 1 | - 1 | Rakhigarhi 1 |

Y also lists a code `Oth` ("Other") that does not occur in our CSV.

## Text class (`class` column)

No source found gives the two-letter codes as such. Wells 2015 (W, via excerpts) uses class names whose initials match four codes; all other meanings are inferred from the data. Data columns: count; text length in signs (median, range; three-digit sign numbers in `text`); commonest object types, materials, sites.

Shared observations behind the inferences: every row in `??` contains the illegible-sign code `000` (1,341 of 1,341) and none is marked complete; every row in `UC` has a break marker `[` or `]` in the text (666 of 666), none contains `000`, and none is marked complete; every row in all other classes is marked complete (`complete` = Y). Rows in `2L`, `3L` and `PA` all contain the line separator `/`.

| Code | Meaning | Source or evidence | Count | Length median (range) | Object types | Materials | Sites |
|---|---|---|---:|---|---|---|---|
| `LP` | Long Patterned text | W ("Long Patterned", 6+ signs). Fits the data: length 7 (5-13), mostly seals | 212 | 7 (5-13) | SEAL:S 163, SEAL:R 33, TAB:B 11 | Steatite 162, - 43, Faience 4 | Mohenjo-daro 133, Harappa 52, Dholavira 6 |
| `SP` | Short Patterned text | W ("Short Patterned"). Fits the data: length 5 (3-7); commonest final signs 861, 817, 501, 820 | 225 | 5 (3-7) | SEAL:S 141, TAB:B 61, SEAL:R 12 | Steatite 138, - 62, Faience 13 | Mohenjo-daro 98, Harappa 92, Chanhu-daro 8 |
| `LC` | Long Complex text | W ("Long Complex"). Fits the data: length 7 (6-12), more varied sign inventory than LP | 127 | 7 (6-12) | SEAL:S 53, TAB:B 21, SEAL:R 17 | Steatite 65, Copper 18, - 13 | Mohenjo-daro 71, Harappa 26, Kalibangan 11 |
| `SC` | Probably Short Complex text | Inferred by analogy with LP/SP/LC (no source names "Short Complex"). Data: length 3 (2-9), complete | 606 | 3 (2-9) | SEAL:S 215, TAB:B 120, TAB:I 102 | Steatite 313, - 102, Faience 69 | Harappa 272, Mohenjo-daro 210, Dholavira 31 |
| `SS` | Short Segment (W: "Short Segment"; another excerpt: "Single Segment") | W; the expansion of the second S is uncertain. Data: length 3 (2-5), complete | 709 | 3 (2-5) | SEAL:S 224, TAB:I 195, TAB:B 149 | Steatite 400, - 93, Faience 82 | Harappa 374, Mohenjo-daro 265, Dholavira 14 |
| `TS` | Single-sign text (expansion of letters unknown) | Inferred from the data: length 1 in 166 of 168 rows; the single sign varies (440, 740, 840, 540, ...) | 168 | 1 (1-3) | SEAL:S 35, MISC 24, POT:T:g 23 | Clay 46, Steatite 33, - 23 | Mohenjo-daro 60, Harappa 58, Kalibangan 18 |
| `NU` | Numeral-only text | Inferred from the data: 90% of rows consist only of signs numbered below 100 (stroke/numeral signs 031-034 most frequent); length 1 in 140 rows; mostly pottery graffiti | 167 | 1 (1-6) | POT:T:g 122, SEAL:S 8, POT:T:s 7 | Clay 128, Steatite 9, - 8 | Harappa 123, Mohenjo-daro 15, Kalibangan 9 |
| `VN` | Sign 700 followed by a numeral | Inferred from the data: 700 in 98% of rows, first in 343 of 355; second sign 033/034/032; Harappa tablets | 355 | 2 (1-3) | TAB:I 172, TAB:B 163, POT:T:g 13 | Steatite 157, Faience 118, - 54 | Harappa 350, Kalibangan 1, Lothal 1 |
| `NV` | Numeral followed by sign 700 | Inferred from the data: 700 last in 62 of 63 rows, preceded by 033/032/034; mirror order of VN | 63 | 2 (2-3) | TAB:B 45, TAB:I 15, POT:T:g 3 | Faience 34, Steatite 15, - 10 | Harappa 62, Mohenjo-daro 1 |
| `VX` | Sign 700 with other (non-numeral-only) signs | Inferred from the data: 700 in 27 of 27 rows, length 3-6 | 27 | 4 (3-6) | TAB:B 14, TAB:I 7, TAB:C 2 | - 9, Steatite 7, Clay 5 | Harappa 18, Mohenjo-daro 8, Kalibangan 1 |
| `PN` | Short text, mostly sign 390 (or 405) plus a numeral | Inferred from the data: first sign 390 in 29 of 53, last sign a numeral (003, 004, 005, 016) | 53 | 2 (1-3) | SEAL:S 25, POT:T:g 10, SEAL:R 5 | Steatite 26, Clay 12, - 7 | Mohenjo-daro 20, Harappa 13, Kalibangan 9 |
| `ZN` | Very short text built on sign 220 or 942 | Inferred from the data: 220 in 18 of 44 rows, 942 in 7; length 1-2 | 44 | 1 (1-2) | SEAL:S 10, TAB:B 9, POT:T:g 7 | Clay 19, Steatite 16, - 5 | Harappa 18, Mohenjo-daro 17, Banawali 2 |
| `AN` | Very short text (1-2 signs) of another kind; letters unexplained | Inferred from the data only as "short": signs 090, 144, 154 recur | 20 | 2 (1-2) | POT:T:g 8, TAB:B 4, SEAL:S 4 | Clay 7, Steatite 6, Faience 4 | Harappa 10, Mohenjo-daro 4, Lothal 3 |
| `MT` | Medium-length text; letters unexplained (perhaps "medial-terminal" segment, unconfirmed) | Inferred from the data: length 4 (2-7); first sign 740, 400 or 520; last sign 240, 235, 415, 220 | 330 | 4 (2-7) | TAB:B 99, SEAL:S 97, TAB:I 50 | Steatite 147, - 56, Faience 54 | Mohenjo-daro 155, Harappa 154, Lothal 9 |
| `IT` | Text of 3-10 signs; letters unexplained (perhaps "initial-terminal", unconfirmed) | Inferred from the data: first sign 740 in 169 of 276; last sign 817, 820, 861; mostly square seals | 276 | 5 (3-10) | SEAL:S 186, TAB:B 31, SEAL:R 23 | Steatite 192, Clay 32, - 31 | Mohenjo-daro 181, Harappa 54, Lothal 21 |
| `IM` | Text of 3-6 signs mostly beginning with sign 390; letters unexplained | Inferred from the data: first sign 390 in 44 of 78; last sign 861, 817, 820 | 78 | 4 (3-6) | SEAL:S 49, SEAL:R 10, TAB:B 8 | Steatite 47, - 17, Clay 7 | Mohenjo-daro 41, Harappa 18, Lothal 6 |
| `MS` | Text of 4-9 signs; letters unexplained | Inferred from the data: commonest last signs 705 and 706; many copper tablets | 88 | 6 (4-9) | SEAL:S 25, TAB:C 25, SEAL:R 19 | Steatite 38, Copper 25, Clay 14 | Mohenjo-daro 58, Harappa 13, Lothal 13 |
| `LT` | Long text, mainly on copper tablets; letters unexplained | Inferred from the data: length 7 (5-11), first sign 740 in 34 of 38, last sign 806 or 803; repeated identical texts | 38 | 7 (5-11) | TAB:C 20, TAB:B 14, SEAL:S 2 | Copper 20, Clay 8, Steatite 4 | Mohenjo-daro 24, Harappa 14 |
| `IC` | Rare class; letters unexplained | 6 square seals, length 4-5; too few to infer | 6 | 5 (4-5) | SEAL:S 6 | Steatite 4, - 2 | Mohenjo-daro 3, Nausharo 2, Unknown 1 |
| `CT` | Rare class; letters unexplained | 4 rows, length 4-8; too few to infer | 4 | 5.5 (4-8) | SEAL:S 2, SEAL:R 1, TAB:C 1 | Steatite 3, Copper 1 | Mohenjo-daro 3, Harappa 1 |
| `2L` | Two-line text | Inferred from the data: every row contains exactly one line separator `/` (63 of 63) | 63 | 7 (2-13) | SEAL:S 52, POT:T:g 5, TAB:C 2 | Steatite 49, Clay 5, Copper 3 | Mohenjo-daro 34, Chanhu-daro 12, Harappa 10 |
| `3L` | Three-line text | Inferred from the data: two `/` separators in each of the 3 rows | 3 | 10 (4-17) | SEAL:S 2, IMPL 1 | Steatite 2, Copper 1 | Mohenjo-daro 2, Harappa 1 |
| `PA` | Text with one sign set apart on its own line, then the main text; letters unexplained | Inferred from the data: all 10 rows have the form `X/...` with a single sign before `/`; all square seals from Mohenjo-daro | 10 | 7 (4-7) | SEAL:S 10 | Steatite 10 | Mohenjo-daro 10 |
| `UC` | Unclassified because the text is broken (incomplete, but all visible signs legible) | Inferred from the data: break marker in 666 of 666 rows, no `000`, none complete | 666 | 2 (1-10) | TAB:I 162, POT:T:g 129, SEAL:S 111 | Steatite 279, Clay 162, - 126 | Harappa 384, Mohenjo-daro 147, Dholavira 33 |
| `??` | Unclassified because the text contains an illegible sign (`000`), often also broken | Inferred from the data: `000` in 1,341 of 1,341 rows, break marker in 58%, none complete | 1341 | 3 (1-16) | SEAL:S 355, TAB:B 220, TAB:I 212 | Steatite 511, Clay 305, - 297 | Harappa 600, Mohenjo-daro 363, Dholavira 118 |

## Uncertain codes

- Firm (source plus data agree): `SEAL*` as seals, `TAB:B` bas-relief tablet, `TAB:I` incised tablet, `TAB:C` copper tablet (data decisive, source garbled), `TAG` as sealing, `BNGL`, `ROD`, `IMPL`, `MISC`; classes `LP`, `SP`, `LC` (names from Wells 2015, seen only in excerpts).
- Seal sub-type letters S, R, C, CY are read from the `shape` field, not from a codebook. `SEAL:L` remains unexplained.
- Tag sub-type letters (`TAG:L`, `P`, `B`, `O`, `W`, `C`, `R`, `PC`) are all unexplained. One excerpt mentions sealings "on textile or reed, wooden strips, and boxes", which suggests the letters record what the sealing was pressed against, but no code-to-letter mapping was found.
- Pottery letters: `g` (graffito) and `s` (stamped) are likely but unsourced; `p`, `M`, `D` are unexplained.
- Yajnadevam's map gives `IMPL` = "Impression" (marked unsure by its author) and `TAB:C` = "Tag"; both conflict with the material and shape fields and are not followed here.
- `SS`: Wells's class names include "Short Segment" and "Single Segment"; which one the code stands for is not settled.
- `SC` as "Short Complex" is an analogy, not a sourced name.
- All other class codes (`TS`, `NU`, `VN`, `NV`, `VX`, `PN`, `ZN`, `AN`, `MT`, `IT`, `IM`, `MS`, `LT`, `IC`, `CT`, `PA`, `2L`, `3L`, `UC`, `??`) are described only by what the texts in them share; the letters themselves are not expanded by any source found. The descriptions for `UC`, `??`, `2L`, `3L`, `TS`, `NU`, `VN`, `NV` and `VX` are near-exact (true for 90-100% of rows); the others are tendencies.
- To settle these, the ICIT help pages (epigraphica.de / user.tu-berlin.de/fuls) and Wells 2015, chapter 3, should be read directly; they could not be reached from this environment.

## `cult` codes and `Bull1` suffixes (added twenty-fifth session)

A survey found no definition of the `cult` codes (SAN, SAF, RAN, RAF, RBF, S) or of the suffixes of `Bull1` (W, J, S, I, L). The ICIT host could not be reached. The only lead, a search-engine excerpt from a paper that could not be found again, says that a "SAN cult object" was "classified by Wells (2011)" (B. K. Wells, *Epigraphic Approaches to Indus Writing*, 2011). Their meanings are therefore not known.

Analysis of the data shows two things. `cult` is filled mainly for unicorn seals (SAN, SAF, RAN, RAF, RBF, S) and for other animals with `Trough`, so it appears to code the object in front of the animal. The `Bull1` suffixes occur at all main sites, so they are not site codes. Tests MO2a and MO2b used both fields only as physical details, without interpreting them.
