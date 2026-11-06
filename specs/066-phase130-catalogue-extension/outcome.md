# Spec 066 — Outcome (Phase-428)

> ## INTAKE COMPLETE — CATALOGUE EXTENSION PINNED
>
> Executed 2026-10-21 under the frozen contract
> (freeze digest
> `0b81d8421c8fe66b486b2c729bb7e978faa6327c74b8f1bff7984128a31aa355`;
> freeze PR #314 merged 2026-10-22T03:23:41Z at
> `c6140cf199b158b25ee4cef6e3bcd9837eb000db`, CI run
> 39715444485 green 7 of 7 from the run's own
> conclusions) and the owner's approval of
> 2026-10-21 (amendment package Item 7).

## 1. The gate, on the record (step 0.1)

The CISI 3.1 portion and its extraction are
restricted research material under PROVENANCE
entry 22 of the restricted local store, quoted
verbatim:

> Classification restricted research material;
> Permitted: local research use, OCR/table
> extraction, derived statistics/counts/feature
> vectors (publishable), citation of facts; Not
> permitted: redistributing scans/page images,
> uploading to repo/Zenodo/OSF/any service,
> sharing copies, bulk reproduction beyond the
> portion; ambiguous use waits for owner ruling;
> no stricter lender terms.

Everything in this outcome honours that line:
the repository carries the extension index
(number + site section + published type class +
grade class), aggregates, pins, and records —
never scans, renders, the extraction table, or
any extracted source-row field beyond those
four. The merged catalogue layer file stays in
the restricted local store, hash-pinned only
(§6).

## 2. Step 0 — all pins asserted

Every pin in spec §2 recomputed and matched:
the portion PDF and the extraction table
(local hashes), the vols 1–2 catalogue CSVs
(local store), the horus84 `inscriptions.csv`,
and — by two routes (gh contents API and the
worktree) — the committed Phase-421 census and
results, the Phase-130 schema, and the
validator `backend/glossa_lab/intake.py`.
Candidate sets re-derived first-hand to the
spec §3 counts (2,101 distinct well-formed
portion numbers: 1,341 referenced — 1,293
zero-resolution + 48 already-joined — and 760
unreferenced; 1,790 zero-resolution census
rows). The corroboration base fact was
re-verified from the layer headers and field
inventories: the vols 1–2 and mayig layers
carry no FC/excavation/museum values, so ladder
rung 5 is UNGRADED for every candidate
(DD-066-7); no CORROB-* outcome can fire.
Repo cleanliness (step 0.4 form, run before any
join work and again before this outcome
commit): no portion-derived row-level file
exists in the tree or index; the only new
row-level file this act commits is the
extension index, carrying exactly the four
lawful columns.

## 3. The census (frozen ladder, spec §5.3)

| set | VERIFIED | CONFLICT | UNRESOLVED | total |
|---|---|---|---|---|
| referenced | 1,331 | 10 | 0 | 1,341 |
| — zero-resolution class | 1,284 | 9 | 0 | 1,293 |
| — already-joined class | 47 | 1 | 0 | 48 |
| unreferenced | 758 | 2 | 0 | 760 |
| **all candidates** | **2,089** | **12** | **0** | **2,101** |

CONFLICT by reason: NUMBER-AMBIGUOUS 11,
SITE 1. No CORROB-* (rung 5 ungraded, §2).

By site section (the committed extension
index): Mohenjo-daro 509, Harappa old 508,
Harappa HARP 1,083, one candidate spanning
Harappa old and Harappa HARP. Type classes
carried (rung 4, not a gate): seal 477, tablet
700, graffiti 561, seal impression 23, stone
object 50, ivory stick 3, other 8, unfilled
(blank/addenda heading — a recorded fact) 274,
and 5 candidates whose records span two type
classes.

Confidence gate (rung 2): the 2 low-confidence
candidates among the well-formed numbers were
hand-verified against 200-DPI page renders
before grading and confirmed as printed (both
enter VERIFIED); the other 5 low cells are the
garbled tokens, which are not candidates. The
183 medium-confidence candidates entered as
provisional VERIFIED and stand as VERIFIED
under the stratum determination (§4). An
independent recount of the local grade table
reproduces every count above exactly.

## 4. The stratum (seed 20261021, DD-066-5)

Drawn after grading in the frozen form: 30
VERIFIED, the whole CONFLICT class (12, smaller
than 15), the whole UNRESOLVED class (0, empty);
no medium supplement was needed — the VERIFIED
draw already contains 3 medium-confidence
candidates. Every sampled candidate was
hand-read on the portion's page renders
(renders stay in the restricted local store).

- Sampled VERIFIED: 30 of 30 sound — every
  number reads as extracted, in its section; no
  non-identity signal anywhere. The hand-check
  did find extraction defects in fields the
  ladder does not grade (two FC-cell misreads
  inherited from the scan's text layer, and
  several records whose key fields the
  extraction left empty although the printed
  row carries them); they are recorded in the
  local stratum record and change no grade.
- Sampled CONFLICT: 12 of 12 attributed to
  **(i) extraction error**; (ii)
  programme-side record error 0; (iii) genuine
  compilation divergence 0; (iv) **true
  non-identity 0**. The mechanisms, per
  candidate (no extracted values reproduced —
  the detail record is local): four candidates'
  second records are rows of neighbouring
  H-229x objects whose number cells the scan's
  text layer misread; one SITE conflict is a
  text-layer misread of an H-number as an
  M-number (the printed row is the H-number, in
  its own section); the remaining candidates
  are printed double- or triple-listings of one
  object under successive photo plates whose
  join-relevant data agree as printed — the
  recorded difference was manufactured by the
  extraction (photo-column text spilled into a
  data field, OCR variants of one printed
  museum value, or key fields left empty in one
  listing's record).
- Medium determination: the 3 sampled
  medium-confidence candidates all hand-read
  sound, so the medium class is covered by the
  stratum; no medium VERIFIED is demoted.

## 5. Halt evaluation (spec §5.5)

CONFLICT share of all graded candidates:
12 / 2,101 = 0.0057 (0.57%), against the frozen
cap of 20% — the share does not halt. Tripwire:
sampled candidates attributed to true
non-identity: 0 — the tripwire does not fire.
**Verdict: NO HALT.** The extension proceeds
and is pinned (§6). No ladder re-run was made
and no record was force-matched; the 12
CONFLICT candidates stand graded CONFLICT in
the index, both/all of their records retained
in the local grade table.

## 6. Build and pinning (on pass)

Merged catalogue layer v2, built and held in
the restricted local store only (one object
per distinct number; on collision the existing
vols 1–2 object stands — 53 collisions recorded
in the local build record; no duplicate, no
overwrite; the 5 garbled tokens were never
repaired into invented numbers):

- file: `cisi_catalogue_layer_v2.csv` (local)
- SHA-256:
  `cd0c2ba8823678be9f7573616528ae0b6be2fe579dc7e34c93add421c80886ad`
- bytes: 2,655,958; rows: 9,741; distinct
  objects: 5,529 (base 7,705 rows / 3,493
  objects; 2,036 new VERIFIED objects added)

Phase-130 validator over the extension dataset
form (2,089 records, one per VERIFIED object;
`license_basis` = the entry-22 gate quoted in
§1): **pass-with-warnings** — 0 errors, 2,363
warnings (the per-record empty-token warnings
of the frozen dataset form). A reject would
have halted pinning; none occurred.

Committed by this act: the extension index
`data/intake/cisi31_extension_index.csv`
(2,101 rows; columns exactly `cisi_number`,
`site_section`, `object_type_class`,
`grade_class`), the aggregate census record
`reports/phase428_results.json`, the execution
script and graph node (Phase-428), and this
outcome. Local products, named by filename and
row count only: `phase428-grade-table.csv`
(2,101 rows), `phase428-build-record.json`,
`phase428-low-verification.json` (2
candidates), `phase428-stratum-attribution.json`,
`phase428-extension-dataset.json` (2,089
records), `cisi_catalogue_layer_v2.csv`
(9,741 rows), and the page renders under
`phase428-renders/` — all in the restricted
local store, none in git.

## 7. Projection (labelled — no join has run)

Projected object-level join against the Phase-421
census, arithmetic only: 2,899 already-joined
rows + 1,777 census rows whose identifier is a
VERIFIED zero-class candidate = **4,676 rows
(82.34%)**, against the Spec 059 bar of 3,465
rows — a projected margin of +1,211 rows. This
is a projection over grades, not a join result:
no join has run under this act, and the
projection does not re-open or alter Spec 059's
recorded outcome.

## 8. What this does not establish

A VERIFIED catalogue object is not a verified
join. No F1 quantity exists from this act, and
none is claimed. STUDY-SPEC-024 / F1 stands as
recorded — SUPPORTED on its original joined
subset (MH OR 2.384 [1.847, 3.077], q=0.00015) —
and Spec 059's JOIN GATE NOT MET record stands
unpatched. The stratum attributions describe
the extraction's behaviour on the sampled
candidates; the 12 CONFLICT grades stand as
graded regardless of their attributed causes,
because the frozen ladder grades the extraction
as delivered, never a repaired reading.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
