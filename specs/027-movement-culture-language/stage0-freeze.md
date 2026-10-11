# Spec 027 — Stage 0 Freeze Record (Phase-391)

> ## FROZEN at the Stage 0 merge (2026-10-11)
>
> Basis: Spec 027 as frozen 2026-10-11 (PR #147, main
> `d9fa0806`; adjudication in `adjudication.md`: Ask 1 → 0A).
> This record freezes Stage 0's sources, schemas, rules, and
> assessment criteria BEFORE the build runs. Any deviation is
> recorded here as a dated amendment BEFORE it is relied on.
> The machine freeze record is `stage0-freeze.json` (Spec 026
> `framework026.build_freeze` digest over this file, the build
> script, the graph module, and the tests).

## 1. Phase and products

- **Phase-391** — Spec 027 Stage 0: source-asserted settlement
  gazetteer + traced chronology spine. Descriptive only
  (spec §6, FR-027-2/3/4). Stage 0 mints **no** movement,
  culture, language, or repertoire verdict.
- Script: `backend/scripts/phase391_stage0_spine.py`.
- Graph module: `backend/glossa_lab/experiment_graph_phase391_392.py`
  (Phase-391 node registered before the run, H23).
- Data products (tracked): `data/movement/gazetteer_rows.jsonl`,
  `data/movement/chronology_rows.jsonl`,
  `data/movement/source_register.json`,
  `data/movement/stage0_meta.json`.
- Reports: `reports/phase391_results.json`,
  `reports/phase391_stage0_report.md`.
- Release package (Ask 4): `stage0-release/` in this spec
  directory — gazetteer CSV of `verified_open` rows only +
  manifest; the repo release gate is run against it in this
  stage. **No external deposit is made.**

## 2. Sources, versions, licence states (spec §5.1)

Inputs live in the gitignored local store
`corpora/downloads/spec027_stage0/`; the build asserts each
input's sha256 against §2.1 and fails loud on mismatch.

### 2.1 Data sources (rows built)

| Source | Version / retrieval | sha256 | Licence state |
|---|---|---|---|
| XRONOS full export (`xronos_data.csv`, https://xronos.ch/data.csv) | retrieved 2026-10-11; database as served (site news: v1.1.1; the CSV carries no per-file version stamp) | `8570bfd9b256ced2f9e840183ea52325b9a7079b79a2957c7db797f09c118655` | `verified_open` — CC BY 4.0, verified on the XRONOS data page 2026-10-11 |
| CISI catalogue layer, Phase-124 artifact (`cisi_vol1_catalogue.csv`, `cisi_vol2_catalogue.csv`) | Phase-124 build (Spec 024 era), from CISI Vols 1–2 as held by the program | vol1 `e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e`; vol2 `e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9` | `open_access_read_only` — factual site assertions derived from in-copyright published volumes; not in the CC BY release package |
| Mutin et al. 2025, Supplementary Information (`mutin_moesm1.pdf`, MOESM1 for doi:10.1038/s41598-025-92621-5) | publisher ESM as served 2026-10-11 | `b5eae7291aa6a1ebb643b381bbf848651f8bccde0f68ccb282e79ed977857600` | `verified_open` — CC BY 4.0 (Scientific Reports). Chronology scenario status: **CONTESTED** (spec §6.5) |

### 2.2 Catalogue-only sources (no rows built; spec §6.6)

- **Possehl published site lists** — `catalogue_only`. Book
  data; no open georeferenced download verified (movement
  report D7). Published counts as cited in secondary
  literature: Early ~477 / Mature ~1,022 / Late ~1,281 sites;
  recorded as citations, not as data.
- **Law (2011) site/resource compilations** — `catalogue_only`.
  Dissertation data; bulk-open status not verified.
- **TwoRains published survey data** — `catalogue_only`. The
  Zenodo deposit cited in the movement report (3909832) was
  inspected 2026-10-11: it is the Angourakis et al. 2020
  crop-model R project (modelling inputs, no site gazetteer).
  The project's Haryana survey site data remains in paper
  supplements not audited for reuse in this stage.
- **c14bazAAR** — `catalogue_only` as an aggregator route
  (spec §3.4): distribution is R-package `.rda`; no
  c14bazAAR source database was verified in this stage to add
  greater-Indus records beyond the XRONOS export. Not used as
  data; no origin group is created by it.
- **Wikipedia "List of Indus Valley Civilisation sites"** —
  `catalogue_only`. Inspected 2026-10-11: prose/list page
  without a source-asserted coordinate table suitable for row
  extraction under §6.2. Not used as data.

## 3. Frozen build rules

### 3.1 Region filter (chronology + XRONOS gazetteer)

Latitude 22.0–37.5, longitude 60.5–79.0 (greater Indus world,
including the Indo-Iranian borderlands of CISI Vol. 3.3).
Rows without coordinates cannot pass the filter and are
excluded from the spine (counted in the build report).

### 3.2 Gazetteer rows (spec §6.2 fields, verbatim)

One row per **source assertion about a site**:

- CISI layer: one row per (volume × distinct non-empty `site`
  value), `source_locator` = volume + the count of catalogue
  objects asserted to that site; the recorded exclusion set
  for non-site values is exactly `{"", "Addenda"}` (catalogue
  section headers, not sites — inspected 2026-10-11; any other
  value is treated as a site assertion). `period_label_as_published`
  = null (the catalogue asserts no period scheme per site);
  coordinates null, `coordinate_state` = `unknown`.
- XRONOS: one row per distinct `site` among §3.1-filtered
  records; coordinates as published (`exact_published`);
  `period_label_as_published` = the XRONOS `periods` labels
  where present, else null; `source_locator` = count of dated
  records + first record id.
- Clustering: `program_site_id` = normalised name (lowercase,
  diacritics stripped, punctuation → space, whitespace
  collapsed). No other merging. Name variants that normalise
  differently stay separate clusters and are listed in the
  conflict report (e.g. hyphenation variants are unified only
  by the stated normalisation).

### 3.3 Chronology rows (spec §6.4 fields, verbatim)

- XRONOS: every §3.1-filtered record is one row. `lab_code`
  from `labnr`; dated material from `material` verbatim;
  conventional age `bp`/`std`; calibrated values **as
  published** (`cal_bp`/`cal_std`) — in the retrieved export
  these are empty for all filtered rows, so v1 stores
  conventional ages only and computes no calibration
  (`calibration_curve` = null, recorded, not hidden).
  `source_database` in the export is empty for all filtered
  rows: the row's origin is recorded as `XRONOS` with the
  record id and the cited `reference` as the trace (spec
  §3.4: XRONOS is the origin group when the underlying record
  is traced to lab code + reference; both are present for
  144/144 filtered rows).
- Mutin et al. 2025 SI Table S2: one row per measurement line
  (including the Zazzo 2014 lines the table republishes, with
  `reference` as printed). Material = tissue as printed
  (enamel/dentine/root); site = Mehrgarh; `feature` = grave
  id as printed; scenario tag `CONTESTED` on every row of
  this source; the older Mehrgarh chronology is **not**
  entered as timing rows (it is a catalogued published period
  assertion, §2.2/spec §6.4 — no sample-level trace was
  extracted in this stage).
- Material classification (frozen mapping, applied to the
  verbatim material string, case-insensitive): `charcoal`,
  `wood`, `charred crust` → long-lived, `old_wood_risk` =
  true, `short_lived_sample` = false. Seed/grain taxa and
  plant-part strings (`wheat`, `barley`, `seed`, `triticum`,
  `lablab`, `ziziphus`) and human/animal hard tissues
  (`bone`, `enamel`, `dentine`, `root`, `tooth`) →
  `short_lived_sample` = true, `old_wood_risk` = false.
  Anything else or empty → `short_lived_sample` = `unknown`,
  `old_wood_risk` recorded true only for the long-lived set
  above, else false with the verbatim string preserved.
- Context-association grades (frozen rule): a row is `direct`
  iff the dated material is itself the claimed event — for
  v1 this applies only to the Mutin/Zazzo burial-tooth rows
  (the dated tissue is the buried individual's own), with the
  note that the *Period I occupation-start* inference drawn
  from them is the contested model step, not the grade.
  A row is `associated` iff the source names a feature for
  the sample (XRONOS `feature` non-empty). All other rows are
  `unassessed`. No row is graded `residual_or_intrusive_risk`
  by inference in v1.

### 3.4 Validators (fail loud; spec §6.6 exit criteria)

Every gazetteer and chronology row must carry source,
licence state, and origin group; every chronology row must
carry a context-association grade; every gazetteer row must
carry a coordinate state. A violation aborts the build with a
non-zero exit (no partial products are written as final).

## 4. Q6 timing-support assessment (criteria frozen here, before the spine exists)

Per spec §8.2/FR-027-9, assessed from spine margins and
metadata only — no trait-timing outcome is inspected. Q6 is
assessed **SUPPORTED-FOR-FREEZE-DESIGN** only if ALL hold:

1. ≥ 3 program regions (as recorded on spine/gazetteer rows)
   each contribute ≥ 2 distinct sites with at least one
   `direct` or `associated` chronology row;
2. ≥ 10 distinct sites hold ≥ 1 `direct`/`associated` row
   with conventional age in the 3300–1900 BCE window
   (5250–3850 BP);
3. among those window rows, ≥ 50% are `short_lived_sample` =
   true;
4. the median reported 1σ error among those window rows is
   ≤ 80 BP (dating precision materially narrower than the
   ~1,400-year window the rivals must be separated within).

Otherwise Q6 remains **NOT-YET-TESTABLE** and the specific
failed criteria are reported. This assessment binds only
whether a Q6 *freeze may be designed*; it is not a Q6 result.

## 5. What this freeze does not do

No trait list, no timing model, no Stage 1 quantity, no
anchor or PRED contact, no external deposit. The Stage 0
report's fitness-for-question table (Q1–Q9) is descriptive
(spec §6.6 item 6).

## Amendment 1 — parser anchoring fix (2026-10-11, pre-output)

The first launch aborted on the build's own row-count
assertion (Mutin Table S2 parse yielded 0 rows against the
frozen expectation of 33) before any product was written.
Cause: the Table S2 row regex anchored the grave token to
column 0, but the SI's layout text indents table rows. Fix:
the anchor allows leading whitespace. No frozen rule, count,
or criterion changed — the assertion that fired is the
freeze's own (§2.1/§3.3 expectation of 33 traced rows). The
freeze record was rebuilt over the corrected script before
the successful run; both events are recorded here per the
program's deviation discipline.

## Amendment 2 — empty-material representation (2026-10-11, pre-output)

The second launch aborted on the build's validator: five
XRONOS records in the filtered export carry an empty
`material` string, and the script represented that as a null
`dated_material`, which §6.4's contract forbids. Clarified
representation (no rule or count changed): an empty source
material string is recorded as `dated_material` = `unknown`
— the §6.4 material vocabulary's own term — with
`material_class` = `unknown` under the §3.3 mapping. The
freeze record was rebuilt over the corrected script before
the successful run.

## Amendment 3 — release CSV line endings (2026-10-11, pre-merge)

After the successful build, staging the products for commit
showed git's CRLF warning on the two release CSVs: the
`csv` module's default dialect emits CRLF terminators, so
the committed bytes would have differed from the bytes the
release gate hashed. Fix: the build's CSV writer now uses LF
terminators; all products were regenerated (content
identical; only the CSV byte representation changed) and
the release gate was re-run against the regenerated package
before merge. Recorded because this program's release
discipline treats byte identity as the substance of the gate
(the v4.2.0 lesson), not as formatting.
