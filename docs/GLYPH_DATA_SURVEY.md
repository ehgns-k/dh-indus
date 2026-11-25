# Survey of open glyph data for Indus signs

## 1. Introduction

Questions about pictographic signs and allographs need shape information for each sign: an image, a vector outline, a font glyph or a structured shape description. That information is only useful here if it is tied to a standard sign numbering: Mahadevan 1977 (M), Koskenniemi–Parpola 1979 / Parpola 1982/1994 (KP or P), or the ICIT numbering of Wells and Fuls (three-digit codes such as 001, 002, 390, 740).

This survey lists the open resources that were downloaded and inspected (shallow clones, November 2026). Each entry records what the files actually contain. A claim that is not backed by an inspected file is marked as such. Repository paths are given relative to the repository root. "Licence" means the licence stated in the repository, either as a licence file or in the README. Where a font carries its own licence or copyright in its `name` table, that is also given.

Several cross-checks were made between resources:

- In three independent sources, the glyphs for ICIT 001, 002, 003, 151, 342, 390, 392, 740, 741 and 920 were rendered and compared: the ICIT sign-list images in `decipher-indus/font-generation`, the PUA fonts that encode ICIT numbers, and the ICIT-indexed font table in `yajnadevam/indus-website`. They agree.
- The Mahadevan images in `ejhong/rongo` were checked at M001, M002, M012, M342 and other signs. M342 is the jar sign.
- The P numbers in `mayig/indus-valley-script-corpus` were compared with the sign ranks of the 1979 sign list digitised in `koskenni/indus` (see 3.8).

## 2. Summary table

Abbreviations: ICIT = Wells/Fuls three-digit sign numbers; KP = Koskenniemi–Parpola 1979 sign rank; M = Mahadevan 1977; PUA = Unicode Private Use Area.

| # | Resource (commit) | Licence | Content | Signs | Numbering | Mapping to ICIT / Parpola | Usable for shape similarity |
|---|---|---|---|---|---|---|---|
| 1 | decipher-indus/font-generation (`ad564ff`) | none stated (font `name` table: "Copyright (c) 2024, मयूख दास") | ICIT sign-list raster images (JPEG), potrace SVG outlines, bitmaps, TTF/WOFF2 font | 726 (725 in `signs_small`) | ICIT (`S###`, 000–999); font codepoint = U+E000 + ICIT number | ICIT is the native key; no Parpola mapping | Yes: best per-sign shape data keyed to ICIT |
| 2 | decipher-indus/font (`c8a02a3`) | GPL-3.0 (LICENSE) | TTF/WOFF2 font + FontForge `.sfd` | 729 codepoints, U+E000–U+E3E9 | U+E000 + ICIT number | ICIT only | Yes, by rendering glyphs |
| 3 | exceptnull/indus-character-map (`344b76a`) | MIT (LICENSE), but the font files are byte-identical to #2 (GPL-3.0) | Web character map + copy of the #2 font | 729 | U+E000 + ICIT number | ICIT only | Same as #2 |
| 4 | sandrocottusm7/font (`68457ff`) | GPL-3.0 (LICENSE) | TTF font | 723 codepoints, U+E000–U+E3E7 | U+E000 + ICIT number | ICIT only | Yes, by rendering glyphs |
| 5 | yajnadevam/indus-website (`2434249`) | GPL-3.0 (LICENSE); bundled font: "© Shabir Kumbhar … 2017. All Rights Reserved" | SQL table ICIT ID → codepoint(s) in the SK Indus Script font; table of 69 "similar glyph" pairs | 698 ICIT IDs | ICIT | ICIT → font codepoint; no Parpola mapping | Partly: font glyphs are rendered via this table; the font licence is restrictive |
| 6 | mayig/indus-valley-script-corpus (`ad2f1e2`) | MIT (LICENSE) | JSON per Parpola sign: description, Parpola variant codes, Wells numbers, Mahadevan numbers, schema of shape features; partial CISI corpus | 396 P signs (P000–P396); 498 Wells numbers; 359 Mahadevan numbers | P (= KP 1979 rank), V (1965 variant code), W (= ICIT), M | **Yes: Wells/ICIT → Parpola and Mahadevan → Parpola**, in `features/P###.json` | Indirectly: feature schemas, not images; serves as the bridge between image sets |
| 7 | koskenni/indus (`60f6e28`) | none stated (contains the Helda reprint PDF of Koskenniemi & Parpola 1979) | Digitised 1979 sign list and corpus; binary glyph templates cut from the sign list (in a pickle) | 687 sign-list entries, 401 ranks | KP 1979 rank + 1965 variant code | KP and variant code only | Yes: one template image per KP allograph |
| 8 | ejhong/rongo (`bb714c7`, archived, moved to ejhong/birdmen) | README: "Code and derived data: MIT licence. Catalogue images are reproduced for scholarly comparison." No licence file | Per-sign PNG crops from Mahadevan 1977 sign list, 64×64 skeletons, complexity counts, source scans | 417 | M (001–417) | M only | Yes (low resolution); see 3.9 |
| 9 | HimanshuAttri/IndusValleyScriptDataset (`c78ad4b`) | none stated | PNG per sign, 256×256, with printed sign number inside the image | 418 files | File index 1–418 ≠ printed number; printed numbers follow Mahadevan 1977 | None in files | Weak: tiny glyphs, labels inside image |
| 10 | Cmathiaz/Indus-Valley-Script-fonts (`f9e04d7`) | README: none stated; font `name` table: SIL Open Font License 1.1, "Copyright (c) 2016, C. Mathiazhagan" | TTF font | 327 PUA glyphs, U+E000–U+E146 | Own sequence | None | Only with a manual mapping |
| 11 | akksshhaay/Indus-Alphabates-Dataset (`4e8c06a`) | none stated | 1840 small images (70×54 PNG data with `.bmp` names) | 1840 images of signs and variants | Own file index (`PPRRCCNN.bmp`) | None | Only after manual labelling |
| 12 | akksshhaay/Indus-Script-Contour-Clustering (`c408c30`) | none stated | Same 1840 glyphs downscaled to 18×14 BMP; contour histograms (CSV); dendrogram images | 1840 | Same file index | None | Has precomputed features, but no sign numbers |
| 13 | akksshhaay/Indus_Script_Clustering (`4d09fb4`) | none stated | C# clustering application, dendrogram JPEGs; data paths point to absent local files | — | — | None | No data |
| 14 | tpsatish95/indus-script-ocr (`3bc0c2f`) | Apache-2.0 (LICENCE) | OCR pipeline code; Caffe models stored as Git LFS pointers only | — | — | None | No sign data |
| 15 | JaidevSK/Harappan-Script-PDF-Maker (`19ffb48`) | none stated | 396 small PNG glyphs (`final/1.png` …) and a reference sheet | 396 | Own index 1–396 | None | Only with a manual mapping |
| 16 | shibenb/indus-seal-generator (`4150caf`) | MIT (LICENSE) | 50 signed-distance-field images `assets/sdfs/S###.png` | 50 | `S###` file names (appear to be ICIT-style) | Not verified | Too few signs |

## 3. Notes on each resource

### 3.1 decipher-indus/font-generation
URL: https://github.com/decipher-indus/font-generation, commit `ad564ff6c8d437182ae557bd4ea23f8aed3ec984`. The repository has no README or licence file.

- `signs/S###.jpg`: 726 grayscale JPEGs, about 204×295 px at 300 dpi, numbered `S000`–`S999`. `download_signs.sh` shows that they were downloaded from the ICIT sign list (`https://www.indus.epigraphica.de/signlist/small/S###.jpg`), which is behind a login. The images are therefore ICIT drawings. Their copyright lies with the ICIT authors, and redistribution rights are not stated.
- `signs_small/S###.jpg`: 725 colour thumbnails (51×74). `S998` is missing.
- `bmps/S###.bmp`: 726 binarised bitmaps (PBM data, 408×590), produced with `mkbitmap`.
- `svgs/S###.svg`: 726 potrace vector outlines (`convert-svgs.sh`).
- `indus-font.ttf` / `.woff2`: 726 glyphs. Codepoint = U+E000 + the number in the file name (`generate-font.py`).
- Verified correspondence: S001/S002/S003 = one, two and three strokes; S151 = man carrying two loads; S342 = horned animal; S390 = tree; S740 = jar with handles; S741 = jar with inner stroke; S920 = "bracket" sign.
- Mapping: the key is ICIT itself. There is no Parpola or Mahadevan mapping.
- Shape similarity: well suited. Every ICIT sign has a raster image of uniform style, a binary bitmap and a vector outline.

### 3.2 decipher-indus/font, exceptnull/indus-character-map, sandrocottusm7/font
- decipher-indus/font (`c8a02a373a7cb449d1fe1f03e781e4510f6bb201`, GPL-3.0): `IndusFont.ttf` has 729 codepoints, U+E000–U+E3E9. `IndusFont.sfd` is the editable source.
- exceptnull/indus-character-map (`344b76a9292726a58ed1db3cea0b09510b3fba01`, MIT): `fonts/IndusFont.ttf` and `fonts/IndusFont.sfd` are byte-identical (MD5) to the decipher-indus/font files. The README credits that source. The font is therefore GPL-3.0 despite the repository's MIT licence. `html-gen.py` only lists the codepoints U+E000–U+E3E9 as "decimal value = codepoint − 0xE000".
- sandrocottusm7/font (`68457fff46b8d47620c59ab7cee2894b2ada4634`, GPL-3.0): `indus-font.ttf` has 723 codepoints, U+E000–U+E3E7. It is a different file with the same encoding.
- All three use the same encoding as #1: codepoint = U+E000 + ICIT number. This was checked by rendering ICIT 001, 002, 003, 151, 342, 390, 392, 740, 741 and 920. Shapes can be rasterised from them at any resolution. Compared with the #1 font, decipher-indus/font has U+E3E3–E3E5 and U+E3E9 in addition and lacks U+E21B (ICIT 539).

### 3.3 yajnadevam/indus-website
URL: https://github.com/yajnadevam/indus-website, commit `2434249618b1e74de3f26d28b90dfde093c3dd94`, GPL-3.0.

- `src/data/usefulMaps.js` contains only two lookup tables: object-type codes (e.g. `SEAL:S`) and iconography codes (e.g. `Bull1`). It holds no sign shapes.
- `population-script.sql`, table `GLYPH (GLYPHID, UNICODE)`, file lines 160–521: 700 rows. GLYPHID is the ICIT sign number. The values are HTML entities for codepoints in `src/assets/fonts/sk_indus_script-webfont.ttf` (e.g. `(740,"&#xE61B;")`, `(390,"&#xE1E4;")`). Of the 698 real IDs, 631 map to a single PUA codepoint and 52 to a sequence of several codepoints (composite signs). Fifteen IDs carry the placeholder U+2047. All 698 IDs are among the 726 ICIT numbers of #1.
- Table `GLYPHSIMILARITY (GLYPHID1, GLYPHID2)`, around line 9875: 69 pairs in 14 groups (e.g. 465 with 466–475; 263 with 264–272; 340 with 341–347). It is a hand-made grouping of similar ICIT signs that can serve as an external check for allograph clusters.
- The font name table reads "SK Indus Script © Shabir Kumbhar … 2017. All Rights Reserved", so the font is not openly licensed.

### 3.4 mayig/indus-valley-script-corpus
URL: https://github.com/mayig/indus-valley-script-corpus, commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`, MIT (copyright 2024 Michael Carlson).

- `features/P###.json` (396 files, P000–P396, plus `features/default_features.json`). Format, using P086 as the example:
  `{"id":"P086","description":"Simple tree with branches at the top","parpola_graphemes":["V126","V127","V151","V508"],"wells_graphemes":["W390","W392","W405","W406","W407","W408"],"mahadevan_graphemes":["M161","M162","M167","M168","M169"],"features":[{"branch_factor":"integer","description":"…"}, …]}`
- Coverage: 331 P signs list at least one Wells number, giving 498 distinct W numbers in total. No W number appears under more than one P sign, so the mapping is many-to-one from Wells to Parpola. 334 P signs list Mahadevan numbers, giving 359 distinct M numbers, 13 of which appear under more than one P sign. 227 P signs define sign-specific features.
- The W numbers are ICIT numbers. All 498 occur among the ICIT images of #1, and spot checks agree in shape: W001/W002 = short strokes (P121/P122), W151 = P001 "person carrying two burdens", W390 = P086 tree, W740 = P324 jar, W741 = P325 jar with stroke.
- The P numbers are the sign ranks of Koskenniemi–Parpola 1979, and the V codes are the 1965 variant codes. For 356 of 396 P signs the set of V codes is identical to the set of variant codes listed for the same rank in `koskenni/indus/digitized/sign_list.tsv`, and for 370 the sets overlap. The README calls the source "Parpola (1982)".
- The feature vectors themselves are attached to sign tokens in `corpus/m001_m099/` and `corpus/m100_m199/` (182 files, Mohenjo-daro only). `features/` gives the schema (feature names and coding), not per-sign shape values.
- The mapping is one-way and partial. Each W number is assigned to exactly one P sign. For example, W740 → P324 only, whereas the alignment-based concordance in `docs/SIGN_CONCORDANCE.md` finds ICIT 740 aligned with KP 325 (352 times) more often than with KP 324 (131 times). Such disagreements should be checked before the mapping is used as ground truth.

### 3.5 koskenni/indus
URL: https://github.com/koskenni/indus, commit `60f6e28bd058aa91edafc55b9b5102b0f6867dd5`. The repository has no licence file. `indus_corpus_1979.pdf` is the University of Helsinki Helda reprint (hdl 10138/342677).

- `digitized/sign_list.tsv`: 687 rows with the columns `sign, variant_code, underlined, pdf_page, column, row`. There are 401 ranks (KP 1979 numbers), and `variant_code` is the 1965 code.
- `digitized/pipeline/templates.pkl` (25.8 MB, a Python pickle that contains only numpy arrays): a list of 687 dicts with the keys `rank, code, ul, img, w, h, top, vec`. `img` is a binary uint8 crop of the plotter-drawn sign from the 1979 sign list, about 110 px high. `vec` is a 42×160 blurred float canvas used for template matching. There is one template per allograph (variant code). The file was loaded with a restricted unpickler for inspection.
- `digitized/proofsheets/p###_colN.png` (114 files): scan strips with recognised signs re-plotted underneath.
- Shape similarity: good for KP allographs. All glyphs are drawn in one uniform plotter style, which avoids differences in drawing hand. They are keyed only to KP rank and variant code. Through #4 (P = KP rank) they can be linked to ICIT.

### 3.6 ejhong/rongo
URL: https://github.com/ejhong/rongo, commit `bb714c77c3f377cdae9b6e9a8cc5eaeab210cd2d` (archived; merged into ejhong/birdmen on 10 September 2026).

- `data/glyphs/indus/001.png` … `417.png`: crops from the Mahadevan 1977 sign list (pp. 32–35). They are small grayscale images (e.g. 25×40 px).
- `data/glyphs/indus_manifest.json`: a list of 417 records with the keys `page, row, col, number, ocr, ocr_conf, label_box, glyph_box, ocr_agrees, status, file`. Status is `ok` for 180 records and `check_ocr` for 237. The numbering comes from the grid position, and OCR of the printed number was used only as a check.
- `data/norm/indus/###.png`: 64×64 skeletons. `data/norm/indus.json` adds `length, endpoints, junctions, loops` per sign.
- `data/raw/mahadevan/`: the source PDF and page scans, including eight pages of the variant tables (`variants-000.jpg` … `variants-007.jpg`) that have not been processed.
- Mapping: M numbers only. They can be linked to Parpola and ICIT through the `mahadevan_graphemes` lists in #4.

### 3.7 HimanshuAttri/IndusValleyScriptDataset
Commit `c78ad4b10f4ccbe7df7ba6f5388c39068a0a5126`, licence none stated. There are 418 PNGs, `1.png`–`418.png`, at 256×256 RGBA. Each glyph occupies only about 20–40 px and has its printed sign number (with daggers) beneath it inside the image. The file index does not equal the printed number: `2.png` shows "101", `12.png` "11", `418.png` "347†". The dagger convention and number range match the Mahadevan 1977 sign list, but the README names no source. Without a table from file index to printed number, the files are not usable.

### 3.8 Cmathiaz/Indus-Valley-Script-fonts
Commit `f9e04d73afd3d677c97dc812a19b052e934eae53`. The README states no licence. `ivfonts.ttf` carries SIL OFL 1.1 ("Copyright (c) 2016, C. Mathiazhagan"; reserved font name "ivfonts") in its `name` table. It has 327 glyphs at U+E000–U+E146 in the author's own order and no concordance to any sign list.

### 3.9 akksshhaay repositories (Dharmsinh Desai University)
- Indus-Alphabates-Dataset (`4e8c06a20bb09e9dcdb8752283620c6523882f69`, licence none stated): `Indus Dataset/` holds 1840 files named `PPRRCCNN.bmp` (e.g. `00000000.bmp`, `16003015.bmp`) that are actually 70×54 RGBA PNG. They are all distinct. The file-name structure (17 two-digit blocks × rows × 16 columns) indicates crops from a printed grid. Each sign appears with many variants in an order that resembles the ICIT/Wells list (anthropomorphs first), but the files carry no sign numbers.
- Indus-Script-Contour-Clustering (`c408c30c72b29441b2c5d90b993baaa00e13e5fc`, licence none stated): `IndusFont1840Out5/` holds the same 1840 names as 18×14 BMPs. `histogramcontour1840.csv` gives 1840 rows of 32 integer contour-histogram values each, and `histogramcontour1840  last.csv` gives 8 values each. `outputorder.csv` is a single ordering line. The dendrograms are images.
- Indus_Script_Clustering (`4d09fb4acb9c3fef74d258e0d3d593a87ab71b21`, licence none stated): a C# application only. The CSV paths in `Grouper.cs` point to local drives and are not included.

### 3.10 tpsatish95/indus-script-ocr
Commit `3bc0c2f92c7e7926dab9efb1af29d92753d20672`, Apache-2.0. The repository holds pipeline code only. Both `weights.caffemodel` files are Git LFS pointers. The classifier in `stages/symbol_classification.py` is binary (jar / no jar). There are no sign images and no sign-list numbering.

### 3.11 Other repositories checked
- JaidevSK/Harappan-Script-PDF-Maker (licence none stated): 396 small PNGs (`final/1.png` …, e.g. 66×43) in an arbitrary order, with no numbering.
- shibenb/indus-seal-generator (MIT): 50 SDF images `assets/sdfs/S###.png`. They were not checked against ICIT.
- ram-g-athreya/indus-keyboard (Apache-2.0): Devanagari/Brahmi fonts for a decipherment proposal, not sign-list glyphs.
- seanndiamond/GlyphLens-Indus (GPL-3.0): zipped screenshots and a PDF; no sign data.
- sbhilare343/Indus-Valley-Civilization-Script-Clustering-Project (MIT): a notebook only.
- Zer0pa/Glyph-Engine (Apache-2.0): shape-descriptor code with a 12-glyph fixture and no Indus sign list.

## 4. Recommendations

### (a) Shape similarity between signs
The best source for ICIT-keyed work is **decipher-indus/font-generation**:

- `signs/S###.jpg` (raster)
- `bmps/S###.bmp` (binary)
- `svgs/S###.svg` (vector)

These cover 726 ICIT signs in one drawing style. Skeletons, distance transforms or descriptors such as HOG and shape context can be computed directly from them. If a resolution-independent source is needed, glyphs can be rendered from the GPL-3.0 font `decipher-indus/font/IndusFont.ttf` at U+E000 + ICIT number. The ICIT drawings themselves come from the ICIT database, and their redistribution terms are not stated. They should be used for analysis and not republished.

For work at the level of Parpola allographs, `koskenni/indus/digitized/pipeline/templates.pkl` supplies one uniform plotter-drawn template per KP 1979 variant code (687 entries, 401 ranks).

For Mahadevan numbers, `ejhong/rongo/data/glyphs/indus/` together with `data/glyphs/indus_manifest.json` (417 signs) is available, but its resolution is low.

`yajnadevam/indus-website` table `GLYPHSIMILARITY` (69 ICIT pairs) can serve as a small independent check of similarity clusters.

### (b) ICIT–Parpola sign-number mapping
The only explicit mapping found is **mayig/indus-valley-script-corpus**, `features/P###.json`, fields `wells_graphemes` (W### = ICIT number) and `mahadevan_graphemes` (M###), under a Parpola sign `id` that equals the KP 1979 rank. It covers 498 ICIT numbers and 396 P signs. It is hand-made, many-to-one, and differs in places from the alignment-based concordance in `docs/SIGN_CONCORDANCE.md` (e.g. ICIT 740). It is therefore best used as a second, independent concordance alongside `results/phase1_concordance.tsv`, with disagreements reviewed against the images of (a). The chain ICIT → P (#4) → KP template (#5) also gives each ICIT sign a second, independently drawn image for checking allograph decisions.
