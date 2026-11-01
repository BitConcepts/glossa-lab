# Spec 077 — Three-Witness Sign-List Triangulation + Token 999 (Method M7)

**FROZEN — 2026-10-26.** This is the M7 design draft of
2026-10-25 (program goal record,
`2026-10-25-spec-draft-m7-signary-triangulation.md`), as
amended by that draft's own 2026-10-25 iteration-pass
amendment, carried into frozen form. The draft's sections
are preserved in substance; the freeze-fixed completions
of §0 below are the only additions, and each is marked as
a completion, not draft text. The freeze record is
`freeze.md` / `freeze.json` in this directory; the
drafting rulings are `adjudication.md` (DD-077-1 …
DD-077-8).

## 0. Freeze-fixed completions

- **FF-1 (numbering).** This design is Spec 077, Phase
  443, claim family F077. Directory:
  `specs/077-signary-triangulation`.
- **FF-2 (the witness set).** The draft's §2 names the
  external lists as "Mahadevan 1977 sign list; Wells 1998
  sign list / Wells 2006". What the program holds, and
  what this freeze counts, is fixed here: (a) the
  Mahadevan 1977 sign list, as the single extraction made
  under the trigger-census instrument and filed as dataset
  v3 (the draft's amendment forbids a second extraction);
  (b) the Wells 1998 sign list, as the extraction filed
  from the held thesis. "Wells 2006" in the draft names
  Wells's 2006 doctoral continuation of the same list; it
  is held in plate form only (its sign plates, PhD Fig.
  3.2) and has never been extracted as a sign list, so it
  is not a counted witness — the counted Wells witness is
  the 1998 list the draft's §3 itself pins by hash. The
  Wells/ICIT list in its 2015 form (Registry v2's
  `wells_ids` surface) is **not** a counted witness: the
  557-sign population is keyed in that list's own numbers,
  so counting it would make C01 true by construction
  (557 of 557) and the claim would test nothing.
- **FF-3 (match rules, operationalized).** A population
  sign is a Wells/ICIT code as enumerated in Spec 075's
  machine record (`keyed_population`, 556 entries, plus
  token 999). Its registry token is `W` followed by the
  zero-padded code (DD-074-8's token form). A sign's
  Mahadevan number set M(s) is the union of `mahadevan_ids`
  over Registry v2's `parpola_1982` rows whose `wells_ids`
  contain that token. Sign s is **M77-witnessed** when
  some m in M(s) is a sign number of the M77 dataset v3,
  subject to FF-4. Sign s is **Wells-1998-witnessed** when
  some m in M(s), subject to FF-4, appears as a
  `mahadevan_xref_fig36` value in the Wells 1998 dataset
  (Figure 3.6's glyph-anchored pairings are the only
  printed Mahadevan cross-references in the thesis; the
  extraction record establishes that Wells-1998 numbers do
  not join the registry directly). Sign s is **witnessed**
  when it is witnessed by either list.
- **FF-4 (the 13 duplicated Mahadevan ids).** The 13 ids
  named in Spec 073's keying-surface accounting (M002,
  M050, M064, M076, M099, M103, M161, M167, M168, M199,
  M216, M264, M409) are each claimed by two Registry v2
  rows. Before counting, the execution's step-0 record
  states, for each id, its two claiming rows and their
  `wells_ids` sets. Sign s is witnessed through a
  duplicated id m only when exactly one of m's two
  claiming rows carries s's token — the collision is
  between rows, and a sign reaches m through its own row
  or not at all. When both claiming rows carry s's token,
  or the step-0 record cannot state the claiming rows,
  the id is unresolved for s and counts as NOT witnessed
  for s (the draft's conservative direction, §4.3).
- **FF-5 (ancestry adjustment, operationalized).** The
  ancestry map is filed at §4.1, before any counting, as
  the draft requires. Its finding is that both witness
  lists descend from one lineage: Wells 1998 descends from
  Mahadevan's concordance. Counting shared-ancestry lists
  as one source is therefore administered as the
  **root-list reading**: a sign is ancestry-adjusted
  witnessed when it is witnessed in the lineage's root
  list (M77). The outcome record reports both numbers —
  the raw share (witnessed in any list) and the adjusted
  share (M77-witnessed) — and the falsifier applies to
  the adjusted number, per the draft §4.1. (The merged
  reading, under which a sign witnessed only in the
  descendant list still counts, equals the raw share by
  construction; it is reported, not used, because under
  it the draft's "if it is lower" could never occur.)
- **FF-6 (token 999's reference behavior).** Fixed from
  Spec 075's frozen population construction (§3 of that
  spec, over its pinned inputs), derived at this freeze
  and re-derived as a check at step 0: in the primary
  population, token 999 occurs **2** times, in **0** of
  them text-final — final-position rate **0.0**. (Context,
  not used: 999 appears in 15 rows of the documented +
  corroborated population.) C02's conditions are therefore
  administered in absolute counts: condition 1 (occurrence
  count within 20% of 2) admits a witness total of exactly
  **2**; condition 2 (final-position rate within 10 points
  of 0.0) admits a final rate of at most **0.10** — at a
  total of 2, a final count of **0**. The rejected
  alternative (reading "occurrence count" as a share of
  each list's own corpus) is recorded at DD-077-8; at
  these counts the two readings admit the same M77
  candidates, and the draft's pairing of "occurrence
  count" with "population behavior" supports the absolute
  reading.
- **FF-7 (the Table I input for C02's M77 arm).** C02
  needs, for each M77 sign, an occurrence total and a
  final count. The only source is Mahadevan's Table I
  (printed pp. 717–723; per-sign SOL/INI/MED/FIN/TOT;
  printed totals row SOL 190 / INI 3010 / MED 7196 /
  FIN 2976 / TOT 13372). This freeze pins Table I by its
  **acceptance form**, not by a hash, because the
  adjudicated dataset had not landed when this freeze was
  built (DD-077-6 records the deviation and its reason):
  the file `m77_table1_occurrences.csv` in the canonical
  store (`glossa-corpus/indus/sources/mahadevan-1977/`),
  one row per M77 sign, in which (i) every row's five
  cells satisfy TOT = SOL+INI+MED+FIN wherever all five
  are present, (ii) the column sums over the complete
  rows, plus the per-column residuals stated in the
  dataset's landing record for the rows that are not
  complete, equal the printed totals row exactly, and
  (iii) any cell the adjudication could not settle is
  carried EMPTY under the extraction's stated certainty
  rule, never guessed, and the rows carrying empty
  cells are exactly the rows the landing record names
  as unsettled. Step 0 verifies the landed file and
  its landing record against this form, verifies the
  reconciliation arithmetic itself, and records the
  file's SHA-256; that hash then binds the execution. A sign whose TOT or FIN cell
  is empty cannot be shown to meet C02's conditions and
  cannot be 999's identity. If the file has not landed in
  this form when step 0 runs, the execution closes
  **CANNOT BE RUN AS WRITTEN** (input not verified) and no
  counting runs; that closure is an execution state, not
  a verdict, and the execution runs once, as frozen, when
  step 0 passes.
- **FF-8 (sensitivity S2, operationalized).** Registry v2
  was built from Parpola 1982's list, the ICIT/Wells list,
  and Yajnadevam's glyph list (Spec 073 record). None of
  those is a counted witness under FF-2, so S2's exclusion
  set — signs whose only witness is a list the registry
  itself was built from — is empty under the frozen
  definitions, and S2's share equals the raw share. The
  outcome record states this and its reason rather than
  presenting a recomputation that excludes nothing as if
  it were a separate measurement; the circularity S2
  guards is carried openly by FF-2's exclusion of the
  ICIT surface and by the ancestry map.

## 1. Purpose

Test whether the program's signary — the 557-sign
population frame behind Rung 1 — is witnessed by sign
lists that did not come from the program: Mahadevan 1977
and Wells 1998/2006, mapped against Registry v2.
Includes a named attack on token 999, the one population
sign with no published identity (Spec 073 record).

## 2. Claims

- **F077-C01 (= draft D-M7-C01).** At least 90% of the
  557 population signs are witnessed in at least one
  external list (Mahadevan 1977 sign list; Wells 1998 sign
  list / Wells 2006), under the match rules of §4.
  *Falsifier:* below 90% → NOT SUPPORTED at the stated
  level; the closure word is SIGNARY NOT WITNESSED AT THE
  STATED LEVEL, and Rung 1's placement must be argued down
  on this record. The bar in counts: at least **502** of
  557 signs (501 of 557 is 89.95%, below the stated
  level). The falsifier applies to the
  ancestry-adjusted share when it is lower than the raw
  share (§4.1, FF-5).
- **F077-C02 (= draft D-M7-C02, token 999).** A witness
  sign is token 999's identity only if it matches on
  **both**: occurrence count within 20% of 999's
  population behavior **and** final-position rate within
  10 points. *Falsifier / default:* if no witness sign
  meets both, 999 stands NO PUBLISHED IDENTITY, with the
  attack recorded as run. Administered per FF-6/FF-7: an
  M77 sign meets both when its Table I TOT is 2 and its
  FIN is 0; a Wells 1998 sign meets both when its dataset
  total is 2 and the M77 sign paired to it in Figure 3.6
  has Table I FIN/TOT at most 0.10 — a Wells sign with no
  Figure 3.6 pairing has no final-position rate in its own
  list and cannot meet the second condition.
- The register (`claims.json`) carries eight further
  claims, F077-C03 … F077-C10: the step-0 pin
  verification; the population reproduction and 999's
  reference behavior; the ancestry map; the 13-id
  resolution; sensitivities S1 and S2; the gap-list
  deliverable; and the Table I input condition. Each
  carries its own falsifier in the register.

## 3. Inputs (pinned at this freeze)

- Registry v2: `data/crosswalks/canonical_sign_registry_v2.csv`,
  SHA-256 `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`;
  1,013 rows (396 parpola_1982 + 407 yajnadevam_glyphid +
  210 icit_wells — Spec 073 record).
- The 557-sign population enumeration: Spec 075's machine
  record `reports/phase441_results.json`, SHA-256
  `f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29`.
- M77 sign list: the trigger-census instrument's single
  extraction, dataset v3 —
  `glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.csv`,
  SHA-256 `9c619bfe2520e63e2968be0ab4ddc9cef1f9aff7dfa3f8eddbf58f21fb414f7e`
  (JSON twin `4d385e340cc780c9d59598894e73ec22887898c66b29965f632a63879d2f6976`);
  417 rows; 179 dagger-flagged / 238 not / 0 uncertain,
  equal to the printed §11.4 total exactly. Extracted from
  the held full volume (SHA-256 `ef68fe8d…e110`, printed
  pp. 32–162 — **numbers only**: the scan is ~150 dpi
  image-only; numbers are OCR-legible, glyph shapes are
  not, and NO shape-matching claim may be made from the
  scan). Extraction and verification records:
  `glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list_extraction_2026-10-25.md`,
  `…/m77_sign_list_full_verification_2026-10-25.md`,
  `…/m77_sign_list_visual_adjudication_2026-10-25.md`
  (the draft §4.2's printed error rate: the verification
  record's per-cell machine-consensus error of about
  0.26% before adjudication; every cell of dataset v3 was
  adjudicated, and the §11.4 checksum closes exactly).
- Wells 1998 sign list: the extraction from the held
  thesis —
  `glossa-corpus/indus/sources/wells-1998/wells1998_sign_list.csv`,
  SHA-256 `22bde128551adbd6d91cd76bb41b4f40199ab3e45af76d500a1008d27c5bea95`
  (JSON twin `bdcb8ef32f5172e4d1ddbb057e4344bccbc7aeacc1928d86c2175c12290a4bf0`);
  588 rows (587 printed entries + sign 407 carried as an
  explicit NOT PRINTED row; only printed entries count as
  list members). Thesis held local, SHA-256
  `5720dc010acc68d6b50827fa89fb7bf3c4c0eb0aee67597e7662e5fd74508906`;
  the thesis PDF is restricted and never enters git.
  Figure 3.6 cross-references:
  `glossa-corpus/indus/sources/wells-1998/wells1998_fig36_crossrefs.csv`,
  SHA-256 `b0ef40da7cd65cdcb6910fd2b1e6aeae4eac47cb31cbe2b2c6205f2ac5da270d`
  (55 pairings over 17 distinct Mahadevan targets).
  Extraction record:
  `glossa-corpus/indus/sources/wells-1998/wells_1998_sign_list_extraction_2026-10-25.md`.
- The `mahadevan_m77_raw.txt` canonical pin (red team
  C-7, adopted in Spec 073's accounting):
  `data/mahadevan_m77_raw.txt`, SHA-256
  `11441e38286784a1f4215f73d91cbba8acd153b7e5b30daed9252f9f7b77304a`.
- Table I occurrences: pinned by acceptance form at FF-7;
  step 0 records the landed file's SHA-256.
- Restricted-local derivation inputs for F077-C04 (never
  in git; cited by hash only): the Shakti corpus
  `sanitized_corpus.json`, SHA-256
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`,
  and the row grades `shakti_row_grades_2026-10-22.csv`,
  SHA-256
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`,
  under Spec 075's frozen population construction.

## 4. Method

1. **Step 0: pins and the witness-ancestry map.** Before
   counting, step 0 verifies every §3 pin first-hand,
   verifies the actual columns and content of every
   witness table and crosswalk counted from (the draft
   amendment's binding rule: verify tables, not
   descriptions — the `positional_class` dictionary/table
   divergence recorded in the amendment is the standing
   example; M7's counting does not use `positional_class`),
   reproduces the population (3,045 analyzable rows / 557
   distinct signs / 550 in sequences of length ≥ 2) and
   999's reference behavior (FF-6), files the 13-id
   resolution table (FF-4), and verifies the Table I input
   (FF-7). Any failure closes the execution CANNOT BE RUN
   AS WRITTEN, naming the failed item.
   **The ancestry map, filed here before counting:**
   - *Mahadevan 1977* — the concordance itself (ASI
     Memoir 77), compiled from the published corpus of its
     day. The root list of the modern tradition.
   - *Parpola 1982/1994* — a re-numbering of Mahadevan's
     signs with his crosswalk printed; descends from M77.
     Registry v2's `parpola_1982` rows, and with them the
     `mahadevan_ids` column this spec matches through,
     descend from Parpola.
   - *Wells 1998* — Wells's corpus is Mahadevan's
     concordance texts re-segmented, and his sign list
     re-divides Mahadevan's material; his Figure 3.6
     expressly compares his divisions against Mahadevan
     1977, Fairservis 1992 and Parpola 1994. Descends from
     M77 (with Parpola, itself of the same lineage).
   - *Wells 2006 / Wells 2015 (ICIT)* — the same scholar's
     continuation of the 1998 list; descends from Wells
     1998, and so from M77.
   - *Registry v2* — built by the program from Parpola
     1982, the ICIT list and Yajnadevam's glyph list (Spec
     073 record); its crosswalk columns are derivatives of
     the M77 lineage. Yajnadevam's rows carry no crosswalk
     data and are not a witness.
   Finding: the two counted witness lists share one
   lineage. FF-5 administers the adjustment.
2. **Extraction.** Complete before this freeze (dataset
   v3; the Wells 1998 dataset), under the
   trigger-census instrument's single pass per source
   (draft amendment §1). No new extraction is commissioned
   by this spec, and none may be substituted.
3. **Matching.** By sign number through the registry's
   crosswalk columns, per FF-3 and FF-4.
4. **Token 999 attack.** Per F077-C02 as administered by
   FF-6/FF-7. The candidate table (every witness sign
   meeting condition 1, with its condition-2 reading) is
   filed in the outcome record whether or not any
   candidate meets both conditions.

## 5. Verdict bands

Per F077-C01/C02. Any shortfall names the unwitnessed
signs by list position (their Wells codes) — the gap list
is a deliverable either way (it is the shopping list for
ICIT-route questions if the owner opens Gate G1). The
execution-level closure words are: EXECUTED; CANNOT BE
RUN AS WRITTEN (step-0 closure, FF-7).

## 6. Sensitivities

- **S1:** recompute with the ancestry map's strictest
  reading (all lists sharing any lineage counted as one).
  On the §4.1 map every witness shares the M77 lineage, so
  S1's number equals the ancestry-adjusted share of FF-5;
  the outcome record reports it on its own line and says
  why the two coincide.
- **S2:** recompute excluding signs whose only witness is
  a list the registry itself was built from (circularity
  check), administered per FF-8.

## 7. What this spec does not establish

Any reading's value; that a witnessed sign is the *same*
sign in every tradition beyond the crosswalk's own claim
(the crosswalk is the program's — S2 exists because of
it); anything about glyph shapes (the M77 scan cannot
carry them). A SUPPORTED verdict establishes witness
presence of the signary by sign number under the stated
match rules, and nothing about the correctness of any
list's divisions; a NOT SUPPORTED verdict establishes
that the frame is not witnessed at the stated level on
this record, and nothing about whether the frame's signs
are real — only that external lists, under these rules,
do not attest 90% of them.

## 8. Execution

One run, as frozen, after this freeze merges on genuine
CI including the required C4 check. The runner is
`backend/scripts/phase443_signary_triangulation.py`; its
machine record is `reports/phase443_results.json`; the
human records are `step0-record.md` and `outcome.md` in
this directory. The anchors file
(`backend/reports/INDUS_FINAL_ANCHORS.json`, SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`)
is read for context only and must be byte-identical after
the run. No re-run under altered parameters; a premise
failure at step 0 is a halt-and-report under FF-7, never
an invitation to adjust a bar, a match rule, or an input.

## 9. Cost / dependencies

Days (the draft's estimate; the extractions it waited on
are complete). Depends on the C-7 canonical pin (adopted,
Spec 073 accounting), on the trigger-census instrument's
single M77 extraction (complete, dataset v3), and — for
C02's M77 arm only — on the Table I adjudication landing
in the form FF-7 pins.
