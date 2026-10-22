# Spec 067 — The Seal/Tablet Difference on the Enlarged Join (Spec 059's Question Re-Run Against the Spec 066 Catalogue Layer v2)

> ## FROZEN — 2026-10-21
>
> Frozen at the freeze act of 2026-10-21 under the
> owner's approval of 2026-10-21 (amendment
> package Item 7 §6: the successor spec to
> Spec 059, authorised in the same approval
> that authorised the Spec 066 intake). The AEE
> lifecycle hooks ran at the freeze gate and
> passed over the recovered register
> (`aee/freeze-aee-note.md`); the freeze record
> is `freeze.md` / `freeze.json` in this
> directory, and the spec's OSF contract
> registration is filed at the freeze under
> campaign decision E-1
> (`osf-spec-registration.md`). **Execution
> is a separate later act**: it runs as
> Phase-429 (DD-067-13), only after this freeze
> has merged, the registration's approval act
> has completed, and a separate execution order
> is given. No new quantity has been computed
> by the freeze itself: no join against the
> merged catalogue layer v2 has been run by
> this spec, no join census on the enlarged
> layer exists yet, and no F1 quantity on any
> enlarged set has been calculated.

**Design source:** Spec 059's frozen design
(design D-22, re-run unchanged in its test
machinery), as closed at step 0 in Phase-421
and unblocked by the act its own outcome
named — "a more complete published object
catalogue entering through Phase-130 intake" —
executed as Spec 066 (Phase-428). The
authoritative draft for this successor is
amendment-queue Item 7 §6 (research notes,
2026-10-21), approved by the owner 2026-10-21.

**Claim under test:** `STUDY-SPEC-024/F1` —
within sites, a text's final sign falls in the
frozen TERMINAL14 class at different rates on
seals than on tablets; standing **SETTLED —
SUPPORTED** on the joined subset of one lineage
layer (odds ratio 2.384, interval [1.847, 3.077],
family q = 0.00015; stable under
leave-one-site-out in Phase-141). Spec 059's
replication attempt closed at step 0, JOIN GATE
NOT MET; that record stands exactly as written
and is cited here, never patched.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the two records it stands on

Spec 024's family member F1 (Stage 2(a),
Phase-136) asked whether the closing-sign
behaviour of inscriptions differs between seals
and tablets, once site is controlled within
site strata. Its frozen protocol
(`specs/024-evidence-integration/stage2a-freeze.md`)
joined the ICIT-lineage (horus84) layer to the
CISI catalogue by **catalogue concordance**: a
row joined if and only if its `cisi` value was
a printed catalogue ID in exactly one volume,
matched as an exact string.

The recorded flow (`reports/phase136_results.json`):

| Step | Count |
|---|---|
| ICIT-lineage layer rows | 5,679 |
| Matched (cisi in exactly one volume) | 2,895 |
| Ambiguous (value `H-311`, in both volumes) | 2 |
| Unmatched | 2,782 |
| Unjoinable-or-ambiguous share | **49.0%** (2,784 of 5,679) |
| Typed (catalogue object_type filled) | 2,752 — Seals 1,588; Tablets 1,088; Graffiti 69; Objects 7 |
| Restricted to {Seals, Tablets} | 2,676 |
| Terminal mapped (W→P, frozen machinery) | 2,195 |
| Analysis population in eligible strata | 2,062 |

On that joined subset the test returned:
Cochran–Mantel–Haenszel chi-square 47.0047;
permutation raw p = 0.0001 (B = 9,999, seed
20261009); Mantel–Haenszel common odds ratio
**2.384**, 95% CI **[1.847, 3.077]**; verdict
**SUPPORTED** after the Spec 024 family
Benjamini–Hochberg correction (family
**q = 0.00015**, combined Stage 2 report).
Phase-141's leave-one-site-out rerun found F1
**STABLE**: every dropped-site subset remained
estimable with its odds-ratio interval
excluding 1.

Spec 059 then asked whether the same test
replicates on a corpus joined through object
identifiers rather than catalogue concordance,
gated at step 0 on whether the better join is
in fact better (bar adopted at DD-059-7:
joined share ≥ 61.0%, ≥ 3,465 of 5,679 rows).
Executed as Phase-421, it closed at step 0,
**JOIN GATE NOT MET**: the object-ID join
joined 2,899 of 5,679 rows (51.05%) against the
vols. 1–2 catalogue layer (7,705 rows, 3,493
distinct objects) — 566 rows short of the bar.
Of the 2,780 unjoined rows, 661 carried no
identifier and 2,119 carried identifiers
resolving to zero catalogue objects. No F1
quantity was computed, and F1 stands exactly
as recorded. The unblocking act named in
Spec 059's frozen outcome wording is: "a more
complete published object catalogue entering
through Phase-130 intake."

That act has now been executed. Spec 066
(Phase-428), under the owner's approval of
amendment package Item 7, graded all 2,101
distinct well-formed CISI Vol. 3.1 portion
numbers under its frozen ladder (VERIFIED
2,089 / CONFLICT 12 / UNRESOLVED 0; conflict
share 0.57% against its 20% halt cap; stratum
true-non-identity attributions 0) and built
the **merged catalogue layer v2** — vols. 1–2
plus the VERIFIED 3.1 objects — held in the
restricted local store only and pinned in
Spec 066's outcome (freeze digest
`0b81d8421c8fe66b486b2c729bb7e978faa6327c74b8f1bff7984128a31aa355`).
Spec 066 ran no join and computed no F1
quantity; its §7 projection (4,676 rows,
82.34%) is recorded there as a projection with
no standing as a result, and it has no
standing here either (§3.4).

### 1.1 The question, in plain words

Spec 059's design was sound and its gate was
honest: the catalogue the programme then held
simply did not contain the objects this
layer's rows reference. The programme now
holds a fuller catalogue, built lawfully
through the intake Spec 059's outcome named.
This spec is Spec 059's question asked again
against that fuller catalogue, with Spec 059's
design — its machinery, its gate form, its
verdict words — carried unchanged, and with
one addition Item 7 §6 makes mandatory: a
step-0 census of type fill on the newly joined
objects, taken before any F1 quantity exists,
because a fuller join is not a fuller F1 test
by itself (§3.4).

### 1.2 The hypothesis and its falsifier

**Hypothesis (gate-passed case only).** The
seal/tablet difference in TERMINAL14 endings,
within sites, replicates on the enlarged
object-ID-joined set at comparable size.

**Falsifier.** On the enlarged set, the
within-site test's interval for the odds ratio
includes 1.0, or the point estimate falls
below 1.5 — meaning the original result was
partly an artefact of which rows could be
joined.

The hypothesis is specified **only** for the
case in which the step-0 gate passes. If the
gate fails, no hypothesis under this spec is
tested, no F1 quantity is computed on the new
join, and the claim's record gains the gate
closure and nothing else (§3.5).

## 2. Inputs (pinned at this draft; re-asserted at the freeze — all pins verified, `freeze.md` §2)

| Input | Pin / state |
|---|---|
| Merged catalogue layer v2 (`cisi_catalogue_layer_v2.csv`; restricted local store, never committed) | SHA-256 `cd0c2ba8823678be9f7573616528ae0b6be2fe579dc7e34c93add421c80886ad`, 2,655,958 bytes, 9,741 rows, 5,529 distinct objects — **as pinned in Spec 066's outcome**; asserted on the local file at the freeze by recompute, and asserted again at step 0 before any join work (DD-067-9) |
| Spec 066 extension index (`data/intake/cisi31_extension_index.csv`, committed) | SHA-256 `be20439a094d4196352bd8c31fd8eeee3f92cd81d8443786a1c520d8355f2540`, 78,531 bytes, 2,101 rows — recomputed at the freeze from the merged record by two independent routes (DD-067-9) |
| Spec 066 freeze record (`specs/066-phase130-catalogue-extension/freeze.json`) | Freeze digest `0b81d8421c8fe66b486b2c729bb7e978faa6327c74b8f1bff7984128a31aa355` — the intake contract this spec's catalogue input was built under |
| Phase-421 census (`reports/phase421_join_census.json`) | SHA-256 `952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8` — Spec 059's executed gate census (the demand side Spec 066 graded against) |
| Phase-421 results (`reports/phase421_results.json`) | SHA-256 `3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f` |
| Phase-136 results (`reports/phase136_results.json`) | SHA-256 `11a0741317f50d9b8c2791fbfdd42ebec0f2a250d6f76809a2dec29fef857022` |
| Spec 024 Stage 2(a) freeze (`specs/024-evidence-integration/stage2a-freeze.md`) | SHA-256 `c65a4b9ba7820f8dcf65fccfe64b8c271e488b036a754c76c45cd19f7cb4b94c` |
| Phase-136 builder (`backend/scripts/phase136_terminal_type.py`) | SHA-256 `d5ceec463bd271cd900fd2e5dbe2efb5b9e5f2b36444942b1d6cab12a6ee8871` |
| Phase-141 report (`reports/phase141_report.md`) | SHA-256 `d442f8d2bcd1e7500c6df169f1dda0d8f48117c349e1710b34ff83011c7e4347` |
| Combined Stage 2 report (`reports/phase136_137_138_stage2_report.md`) | SHA-256 `6a4f5d2651ddc8316cf69d65ff6f4d29a7138ddc528c68310e6f07047eaed062` |
| Canonical sign registry (`data/crosswalks/canonical_sign_registry.csv`) — the frozen W→P mapping substrate | SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` |
| ICIT-lineage (horus84) inscription layer (5,679 rows; local store, as at Phase-136) | SHA-256 `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`, 1,190,884 bytes — **as recorded in `reports/phase136_results.json`**; re-asserted by recompute at the freeze |
| CISI catalogue layer, vol. 1 (`cisi_vol1_catalogue.csv`; local store, gitignored) | SHA-256 `e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e`, 804,665 bytes — **as recorded**; the gate-0.2 reproduction resolves against the vols. 1–2 layer exactly as frozen in Spec 024/059 |
| CISI catalogue layer, vol. 2 (`cisi_vol2_catalogue.csv`; local store, gitignored) | SHA-256 `e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9`, 1,431,631 bytes — **as recorded** |
| Phase-130 intake schema (`data/intake/intake_dataset_schema_v1.json`, schema_version `1.0`; Spec 021) | SHA-256 `b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b` (6,197 bytes); validator `backend/glossa_lab/intake.py` SHA-256 `02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03` (18,867 bytes) — pinned at DD-059-9, carried unchanged |
| Spec 034 route-(b) construction (`backend/glossa_lab/phase398_matched_object.py`, `build_intake_dataset`) | SHA-256 `278f16b0ae8b02b77412cc925ac9e767110f5d5461729b73e8c122a9ff7673f0` (40,104 bytes) — pinned at DD-059-9, carried unchanged |
| ICIT converted keyed layer v2 (`corpora/downloads/icit_fieldcady/icit_converted_v2_keyed.json`; local store, gitignored) | SHA-256 `bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8`, 1,586,137 bytes — the programme-built converted form of the pinned lineage layer: the same 5,679 rows and the same `cisi` values, not a second source (DD-059-9, carried) |
| Spec 059 outcome (`specs/059-f1-object-join/outcome.md`) — the closure this spec succeeds | Cited, never patched; its census and closure wording are the record §1 stands on |
| Spec 066 outcome (`specs/066-phase130-catalogue-extension/outcome.md`) — the intake record | The merged layer's pin, counts, and fences are taken from this record |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft, fresh). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

**The join's sources are named and pinned in
the DD-059-9 form, carried into this freeze as
DD-067-9:**

- **Lineage side:** the pinned ICIT-lineage
  (horus84) inscription layer itself (SHA-256
  `c368f290…` above). Each row's published CISI
  object reference is its `cisi` field, carried
  as `provenance.object_id` exactly as Spec
  034's route-(b) construction carried it (the
  pinned Phase-398 builder above). The layer's
  programme-built converted form, the ICIT
  converted keyed layer v2 (pinned above),
  carries the same rows and the same `cisi`
  values and is the same source in converted
  form, not a second source.
- **Catalogue side:** the pinned **merged
  catalogue layer v2** (SHA-256 `cd0c2ba8…`
  above), whose object key is its `cisi_id`
  column — 9,741 rows, 5,529 distinct objects
  (the vols. 1–2 base of 7,705 rows / 3,493
  distinct objects plus 2,036 new VERIFIED
  Spec 066 objects; 53 collisions recorded in
  Spec 066's local build record, the existing
  object standing in each). The layer is held
  in the restricted local store and is never
  committed; gate 0.1 asserts its pin on the
  local file before any join work.
- **Schema and validator:** the Phase-130
  intake schema and `glossa_lab/intake.py`,
  pinned above.

Gate 0.1 asserts every one of these pins;
a mismatch stops the run as INVALID (§3.1).

## 3. Step 0 — the join gate, with the type-fill census (fail-closed, gate-first)

Execution runs these checks **in order**. The
gate is decided on census counts alone, before
any F1 quantity exists on the new join. No
failure is repaired at run time.

### 3.1 Gate 0.1 — input integrity

Every §2 input hashes to its freeze-record
value — including the merged catalogue layer
v2, asserted on the local file (SHA-256,
byte count, 9,741 rows, 5,529 distinct
objects) **before any join work** — and the
Phase-130 schema validates the join dataset
built at gate 0.3 (verdict `pass`). A mismatch
or a validation failure stops the run as
**INVALID — PIN FAILURE** (a §2 or DD-067-9
pin mismatch) or **INVALID — CENSUS FAILURE**
(the join dataset fails Phase-130 validation);
the two classes are named here so an INVALID
closure states which class fired.

### 3.2 Gate 0.2 — original-join reproduction

The original concordance join is re-run on the
pinned layer and the pinned vols. 1–2 catalogue
under its frozen rule (exact string; a row
joins iff its `cisi` value is a printed
catalogue ID in exactly one volume), and must
reproduce the recorded census **exactly**:
5,679 layer rows; 2,895 matched; 2 ambiguous;
2,782 unmatched. A mismatch stops the run as
**INVALID — CENSUS FAILURE** — the gate's
baseline (51.0%) is the recorded one, and a run
that cannot reproduce it has no baseline to
beat. This reproduction is against the
vols. 1–2 layer, exactly as Spec 059 ran it;
it contributes no row to the enlarged set.

### 3.3 Gate 0.3 — the object-identifier join census (against layer v2)

The join is rebuilt **through object
identifiers only**, exactly as in Spec 059
§3.3, with the single change the successor
exists for: resolution is against the pinned
merged catalogue layer v2 (§2) instead of the
vols. 1–2 layer.

- Each lineage row's object identifier is
  carried as cited provenance data under the
  Phase-130 intake schema — the route Spec 034
  proved at scale and Spec 059 executed
  (5,018 ICIT inscriptions admitted through
  the schema, validation verdict pass, joined
  on `provenance.object_id` only).
- A row is **joined** iff its object
  identifier resolves to **exactly one** object
  in the merged catalogue layer v2. Rows
  resolving to zero catalogue objects are
  **unjoined**; rows resolving to more than
  one are **ambiguous**; both classes are
  counted and neither enters the joined set.
- **String identity is never a join key.**
  No name string, number string, `cisi` field
  string, or `cisi_number` string is matched
  as identity at any point in this join (§7.1
  states the boundary and its ground: Spec
  037's census).
- The unit of the census is the **layer row**,
  as in the original flow; if two joined rows
  resolve to the same catalogue object, both
  count as joined rows, and the distinct-object
  count is reported descriptively alongside
  (DD-067-2).
- The census reports: layer rows; joined rows
  and share; unjoined rows (split as no
  identifier carried / identifier resolving to
  zero objects in layer v2); ambiguous rows;
  distinct catalogue objects joined to; and
  the joined set's site and object-type mix.

### 3.4 Gate 0.4 — the type-fill census (mandatory; before any F1 quantity)

A fuller join is not a fuller F1 test by
itself: F1 eligibility under the frozen
Phase-136 flow runs on typed objects (typed →
{Seals, Tablets} → eligible strata). Item 7
§6 therefore makes this census a step-0 gate
of this spec, taken **before any F1 quantity
exists**:

- **Newly joined objects.** The objects the
  gate-0.3 join newly reaches — the joined
  rows that Spec 059's Phase-421 census
  recorded as unjoined (identifier resolving
  to zero objects in the vols. 1–2 layer), and
  the distinct catalogue objects they resolve
  to in layer v2 — are censused for type fill:
  how many carry a filled catalogue
  `object_type`, and how many carry type
  **unfilled**. The intake record states the
  expectation this census measures, without
  asserting its outcome: 126 of the 1,293
  overlap numbers carried only a blank plate
  heading in the portion, so their catalogue
  objects enter layer v2 with type unfilled;
  the previously joined set already carried
  143 unfilled-type objects (Phase-421
  census). Both figures are expectations from
  the intake record, not results of this spec.
- **The whole joined set.** Type fill is
  censused over the full gate-0.3 joined set
  in the same pass: filled / unfilled counts;
  the typed mix (Seals / Tablets / Graffiti /
  Objects / Seal impressions / unfilled, as
  layer v2 records them); and the resulting
  **eligible seal/tablet strata** under the
  frozen Phase-136 eligibility mapping
  (§4.1 steps 1–2 and 5 applied as a census:
  restriction to {Seals, Tablets}, then the
  stratum rule N ≥ 20 with ≥5 Seals and ≥5
  Tablets, reported per site) — stated as
  census counts, with no terminal mapping, no
  statistic, and no F1 quantity computed.
- The census is published with the gate
  census whichever way the gate falls. A
  gate-passed join whose typed seals/tablets
  in eligible strata are too few for the
  frozen estimability rule closes as **NOT
  ESTIMABLE** under the frozen mapping (§5) —
  Spec 059 §5's provision, carried: the
  type-fill census is what shows that
  condition at step 0, before any test is
  attempted.

### 3.5 Gate 0.5 — the gate comparison

**The bar, adopted openly at this freeze
(DD-067-7, in the DD-059-7 form):** the
object-ID join against layer v2 must reach a
joined share of **≥ 61.0% of 5,679 rows —
≥ 3,465 joined rows** (0.61 × 5,679 =
3,464.19; 3,464 rows = 60.997% and fails).

- **Basis, stated on the record.** This is
  Spec 059's bar, carried unchanged. The
  successor re-runs Spec 059's design on the
  same layer, the same denominator, and the
  same original baseline (2,895 of 5,679,
  51.0%); the enlargement standard the design
  fixed at DD-059-7 — the original share plus
  ten points, in the design's own stated
  reading, the strictest of the three readings
  recorded there — is the standard a successor
  must meet for its enlarged set to count as
  the enlargement the design required. No new
  bar is derived, and in particular no bar is
  derived from Spec 066's projection: the
  intake's projected joined count (4,676 rows,
  82.34%, Spec 066 outcome §7) is a projection
  over grades, recorded as a projection with
  **no standing** — the gate is judged on this
  execution's own census, against the carried
  bar, and a projection neither lowers nor
  raises it. If a different bar had been
  adopted, the adjudication would have had to
  say why, on the record, before freezing;
  DD-067-7 records that the carried bar is
  adopted and why.
- The comparison is like-for-like: the
  original 51.0% is the matched share *before*
  any object-type restriction or terminal
  mapping (2,895 of 5,679), and the new share
  is taken at the same point in the flow —
  joined to the catalogue, before typing,
  restriction, or mapping (§4.1 then applies
  the frozen flow to the joined set).

### 3.6 The gate closure (pre-written)

If gate 0.5 fails, the execution **closes at
step 0, unscored**, with this wording (the
bracketed quantities filled from the census):

> "CLOSED AT STEP 0 — JOIN GATE NOT MET. The
> object-identifier join against the merged
> catalogue layer v2 joined [n] of 5,679
> lineage rows ([x]%), against the original
> concordance join's 51.0% and the gate fixed
> in advance at 61.0% or more (≥ 3,465 rows,
> carried from Spec 059 at DD-067-7). The
> enlarged joined set this design required
> does not exist on the enlarged catalogue
> data either, so no F1 quantity was computed
> and `STUDY-SPEC-024/F1` stands exactly as
> recorded — SUPPORTED on its original joined
> subset, its 'on the joined subset' scope
> unchanged. The unjoined share is a measured
> property of the enlarged catalogue data,
> not an oversight."

The gate census and the type-fill census are
published as the closure's finding, whichever
way the gate falls (joined / unjoined /
ambiguous counts, by route and by site; type
fill on the newly joined objects and on the
whole joined set), exactly as Spec 059's gate
census was published at its closure.

## 4. The primary test (gate-passed case only)

Nothing in this section runs unless gate 0.5
passes. If it passes, the frozen Phase-136
flow is applied to the enlarged joined set,
**unchanged in every particular** — Spec 059
§4 carried verbatim in substance:

### 4.1 The frozen flow on the enlarged set

1. The joined object's catalogue `object_type`
   (Class O), as in the original flow: filled /
   unfilled counted; unfilled excluded, counted.
2. Restriction to object types {Seals, Tablets};
   Graffiti, Objects, Seal impressions, and any
   other recorded type excluded and reported
   descriptively, as frozen.
3. Sequence parse by the established convention
   (`re.findall(r"\d{3}", text)` in recorded
   reading order; terminal sign = last parsed
   code).
4. Terminal mapping by the frozen Spec 018 §3
   canonical map (Wells → Parpola) via the
   frozen machinery (`build_sign_maps` /
   `SignMapper.map_w` over the pinned registry,
   its frozen conflict rule); UNK terminals
   excluded, counted.
5. Stratum eligibility, mechanically: a site
   stratum enters iff its analysis-population
   N ≥ 20 and it contains ≥5 Seals and ≥5
   Tablets (the original run's eligible strata
   were Mohenjo-daro, Harappa, Kalibangan; the
   enlarged set's strata are whatever the rule
   returns, reported in full).
6. Estimability, mechanically (the frozen
   rule): the test executes iff, on the
   eligible-strata population, (i) ≥2 eligible
   strata, and (ii) the pooled 2×2 table's
   expected counts are ≥5 in at least 80% of
   its 4 cells. Failure → **NOT ESTIMABLE**,
   cell counts shown, no p-value (§5). The
   gate-0.4 type-fill census is this rule's
   step-0 shadow: a joined set whose typed
   strata cannot satisfy it is already known
   at step 0, and the outcome is recorded on
   the same frozen terms.

### 4.2 The test statistic and effect sizes

- **Statistic:** Cochran–Mantel–Haenszel
  chi-square (no continuity correction) over
  the eligible strata's 2×2 (type × outcome)
  tables; outcome = terminal mapped P sign ∈
  **TERMINAL14** = {P020, P076, P095, P099,
  P108, P125, P210, P226, P256, P346, P359,
  P378, P384, P385} (frozen, Spec 018 §3).
- **Null distribution:** permutation — within
  each stratum, object-type labels shuffled;
  B = 9,999; seed 20261009; p = (1 + #{perm ≥
  obs}) / (1 + B); Python stdlib
  `random.Random(20261009)`. No asymptotic
  p-value is reported as a result.
- **Effect sizes (reported regardless of
  verdict):** Mantel–Haenszel common odds
  ratio with 95% CI (Robins–Breslow–Greenland);
  the crude odds ratio, labelled uncontrolled;
  per-stratum odds ratios and observed
  TERMINAL14 shares by type (descriptive).

### 4.3 The family correction

The confirmatory family under this spec is
its single primary test, as confirmed for
Spec 059 at DD-059-8 and carried at DD-067-8:
the Benjamini–Hochberg adjustment at q = 0.05
is over one p-value and the adjusted q equals
the raw p. The Spec 024 family (F1/F2/F3) was
corrected once, in its combined report, and
is closed; it is not re-opened or re-run by
this spec. Every verdict wording in §5 is
stated in terms of that adjusted q.

### 4.4 Leave-one-site-out (descriptive)

The Phase-141 leave-one-site-out rerun is
repeated on the enlarged set with the same
machinery and parameters, and reported
descriptively with the outcome: each
dropped-site subset's estimability, odds
ratio, and interval. As in Phase-141, LOSO
**mints no verdict** and changes no verdict
word; it qualifies the outcome's summary
language only, and the outcome record says
which sites, if any, are load-bearing.

### 4.5 The covariate comparison (reported either way)

Whether or not the test replicates, the
execution reports a stated comparison of the
**joined and unjoined rows** on every
covariate the data carries — site, object
type (for rows the catalogue types), text
length, and preservation as recorded — so the
still-silent share is at least described; and
the same comparison between the original
joined set and the rows the object-ID join
against layer v2 adds, so what the enlargement
changed is on record. A covariate the data
does not carry is named as not carried, never
reconstructed.

## 5. Criteria fixed in advance, and pre-written verdict wordings

After all gates pass and the test is
estimable, the outcome is exactly one of
**REPLICATED**, **WEAKENED**, or **NOT
REPLICATED**, by these rules (design D-22's,
carried through Spec 059; precedence per
DD-067-3, confirming DD-059-3):

- **REPLICATED:** adjusted q below 0.05 **and**
  the odds-ratio interval entirely above 1.5.
- **WEAKENED:** adjusted q below 0.05, the
  interval does **not** include 1.0, but it
  reaches below 1.5.
- **NOT REPLICATED:** adjusted q at or above
  0.05, **or** the odds-ratio interval includes
  1.0. (An interval including 1.0 is NOT
  REPLICATED even if q is below 0.05 — the
  design's falsifier names inclusion of 1.0
  first; DD-067-3.)

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- REPLICATED: "On the enlarged object-ID-joined
  set ([n] of 5,679 lineage rows, [x]%, against
  the original join's 51.0%), the seal/tablet
  difference in TERMINAL14 endings replicates
  within sites: Mantel–Haenszel odds ratio
  [r], 95% CI [lo–hi], entirely above 1.5,
  family-adjusted q = [q]. The original F1
  result was not an artefact of which rows the
  concordance join could reach, at this test's
  resolution. [LOSO sentence.] This is a
  statement about recorded use in this lineage
  layer, not about what the difference means."
- WEAKENED: "On the enlarged object-ID-joined
  set ([n] of 5,679 rows, [x]%), the seal/tablet
  difference in TERMINAL14 endings remains
  detectable within sites (family-adjusted
  q = [q]) but smaller than the original
  estimate: Mantel–Haenszel odds ratio [r],
  95% CI [lo–hi], reaching below 1.5 (original:
  2.384 [1.847–3.077] on 51.0% joined). Part of
  the original result's size was a property of
  which rows could be joined. [LOSO sentence.]"
- NOT REPLICATED: "On the enlarged
  object-ID-joined set ([n] of 5,679 rows,
  [x]%), the seal/tablet difference in
  TERMINAL14 endings does not replicate within
  sites: [family-adjusted q = [q] at or above
  0.05 / the odds-ratio interval [lo–hi]
  includes 1.0], point estimate [r] (original:
  2.384 [1.847–3.077] on 51.0% joined). The
  design's falsifier has fired: the original
  result was partly an artefact of which rows
  could be joined. The original verdict stands
  as recorded on its subset; this outcome is
  appended as its replication record.
  [LOSO sentence.]"
- NOT ESTIMABLE: "The object-ID join against
  layer v2 passed its gate ([n] of 5,679 rows,
  [x]%), but the enlarged set fails the frozen
  estimability rule ([failed clause]; cell
  counts shown in the record; the step-0
  type-fill census is part of that record). No
  p-value was computed and no verdict under
  this spec exists. `STUDY-SPEC-024/F1` stands
  exactly as recorded."

**The §5 re-statement rule, exactly as
Spec 059 reserved it.** In every gate-passed
outcome, the claim's wording gains or loses
the phrase "on the joined subset" as the
evidence dictates, by appended record only
(§7.2): REPLICATED on a materially enlarged
set is the outcome under which the phrase's
scope is re-stated to the enlarged share
actually joined; WEAKENED and NOT REPLICATED
keep the phrase and add the enlarged-set
result beside it. `STUDY-SPEC-024/F1` stands
as recorded unless a gate-passed execution
under this spec earns that re-statement. The
exact re-statement sentence is part of the
outcome record, written from the frozen
wordings above, not improvised. A gate
closure or a NOT ESTIMABLE outcome earns no
re-statement: the phrase and the scope stand
unchanged.

## 6. Controls and named confounders

- **Join-selection bias** is the confounder
  that motivates the design; the §4.5 covariate
  comparison is its control, and it is reported
  whether or not the test replicates. The gate
  itself is the prior control: an enlargement
  too small to change the selection is closed
  at step 0 rather than run.
- **Type fill is now a measured quantity, not
  an assumption.** The gate-0.4 census counts
  unfilled types on the newly joined objects
  and on the whole joined set before any test;
  the enlarged set's typed composition is on
  record whichever way the gate falls.
- **Genre differences** (ownership marks versus
  accounts) and **preservation differences**
  between object types: the within-site design
  controls place, not kind. This limit is
  stated in the verdict wording's scope, as
  the original report stated it.
- **Compilation-internal association:** the
  lineage's transcriptions and the catalogue's
  typing were both made within one scholarly
  tradition (Phase-136's adversarial note). The
  within-site control does not imply more
  independence than exists; no output may
  present the enlarged join as independent
  corroboration of the catalogue's typing.
- **Object-type disagreement across
  compilations** (Spec 037: object type is the
  dominant conflict axis in its census). Type
  under this spec is the joined catalogue
  object's recorded type in layer v2, as in
  the original test; the limit travels with
  the result. Layer v2's 3.1-object types are
  the published plate-heading classes as
  graded by Spec 066; they are carried, not
  re-graded, by this spec.

## 7. Epistemic limits (binding on all outputs)

### 7.1 The string-identity boundary

This design joins on **object IDs, never on
string identity**. The ground is Spec 037's
census: of 693 CISI↔corpus exact-string
matches, 269 verified as same-object joins
under the frozen grading ladder, 341 were
CONFLICT (49.21% — mostly on object type), and
83 were UNRESOLVED. A string match is a
candidate, never an identity. Accordingly: no
step of this spec's join, census, or test may
treat equality of any string (a catalogue
number string, a name, the layer's `cisi`
field, a `cisi_number`) as evidence that two
records concern the same physical object. The
original concordance join is re-run at gate
0.2 **only** to reproduce the recorded
baseline the gate is stated against; it
contributes no row to the enlarged set.

### 7.2 The frozen outcomes stand

Spec 024 F1's SUPPORTED verdict on its joined
subset and Spec 059's JOIN GATE NOT MET
closure are records of their own frozen
designs and are **not edited, superseded, or
re-adjudicated** by anything this spec finds.
This spec's outcome — gate closure, NOT
ESTIMABLE, or a §5 verdict — appends to the
claim `STUDY-SPEC-024/F1` as a dated
replication record beside them, and appends
beside Spec 059's record in the same
append-only posture (DD-067-1).

### 7.3 Restricted discipline (binding)

The merged catalogue layer v2 is a product of
restricted material (the Phase-130 gate,
PROVENANCE entry 22; Spec 066 §4's lawful
line). It stays in the restricted local store,
hash-pinned only, never committed, never
uploaded, never shared. Row-level products of
this spec's execution that derive from the
merged layer (the per-row join census against
layer v2, any row-level joined-set file) stay
restricted-local in the same way: they are
named in the outcome record **by filename and
counts only**. The committed products of an
execution are aggregates, the gate and
type-fill censuses in aggregate form, and the
results record in Spec 059's form (results
JSON, census summary, report). No scan, page
image, extraction row, or extracted source-row
field beyond Spec 066 §4's item-1 fact list
enters any product of this spec.

### 7.4 What no outcome establishes

- **Not what the difference means.** Genre,
  habit, and survival remain live explanations,
  named as such; this test re-measures an
  association on a larger joined share and
  adjudicates nothing among them.
- **Nothing about corpora outside this
  lineage.** Every output carries the lineage
  label and the sentence: results describe
  this lineage layer, and (gate-passed) its
  object-ID-joined subset, not the Indus
  corpus in general.
- **Nothing about sign meanings.** TERMINAL14
  is a frozen descriptive class; membership in
  it is a fact about use, prior to any reading.
- **A gate closure establishes nothing about
  the claim.** It is a statement about the
  enlarged catalogue data's joinability
  (§3.6), and the record says so.
- **The intake's projection establishes
  nothing here.** Spec 066's projected joined
  count (4,676 rows, 82.34%) is arithmetic
  over grades, not a join result; no output
  of this spec may cite it as one.

## 8. Risks and honest weaknesses

- **The gate may honestly fail again.** The
  projection says it should not, but a
  projection is not a census: whether the
  layer-v2 join in fact reaches the carried
  bar is exactly what gate 0.3/0.5 measures,
  and a second closure at step 0 is a
  realistic, pre-registered outcome of this
  spec.
- **Type fill may make a passed gate
  inestimable.** 126 of the overlap numbers
  entered layer v2 with type unfilled, and
  the previously joined set already carried
  143 unfilled-type objects. If the newly
  joined typed seals/tablets are too few in
  eligible strata, the honest outcome is NOT
  ESTIMABLE under the frozen mapping — which
  is why the type-fill census is a step-0
  gate (§3.4), not a surprise at §4.
- **Enlargement changes the strata.** Sites
  thin in the original joined set may become
  eligible, and the eligible-strata population
  will differ from the original 2,062; the
  comparison to the original result is
  therefore a replication on an enlarged set,
  not a paired re-measurement of identical
  rows — except for the §4.5 added-rows
  comparison, which is descriptive.
- **Three sites carried the original test.**
  If the enlarged set's eligibility returns
  the same three strata, the replication
  inherits that thinness; it is stated, not
  repaired.
- **Layer v2 is one merged layer.** Its 3.1
  objects were graded under Spec 066's ladder
  against the extraction as delivered; the 12
  CONFLICT candidates never entered it. This
  spec resolves against the layer as pinned;
  it does not re-grade the intake.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **INVALID** — a §2 pin mismatches (class:
  PIN FAILURE, gate 0.1); the Phase-130
  validation of the join dataset fails
  (class: CENSUS FAILURE, gate 0.3); or the
  original-join reproduction (gate 0.2) does
  not reproduce the recorded census exactly
  (class: CENSUS FAILURE). The class that
  fired is named in the closure.
- **CLOSED AT STEP 0 — JOIN GATE NOT MET** —
  gate 0.5 fails: the layer-v2 joined share
  is below the §3.5 bar. Unscored; the §3.6
  wording is the outcome; the gate and
  type-fill censuses are its finding.
- **NOT ESTIMABLE** — the gate passes but the
  enlarged set fails the frozen estimability
  rule (§4.1 step 6), including the case the
  gate-0.4 type-fill census shows at step 0:
  too few typed seals/tablets in eligible
  strata under the frozen mapping. Cell
  counts shown; no p-value.
- **REPLICATED**, **WEAKENED**, or **NOT
  REPLICATED** — per §5, after all gates pass
  and the test is estimable.

## 10. Execution shape (gated; NOT run by this freeze)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — integrity (layer v2
   asserted on the local file first), original-join
   reproduction, object-ID join census against
   layer v2, type-fill census, gate comparison.
   A gate failure ends the execution here, with
   the censuses and the §3.6 closure as its
   complete record.
3. **Primary** (§4, gate-passed only) — the
   frozen flow on the enlarged set, the test,
   LOSO, and the covariate comparisons.
4. **Outcome** (§5) — appended records only;
   anchors asserted byte-identical;
   foundation check (H21) reported as
   measured; row-level products of the merged
   layer restricted-local, named by filename
   and counts only (§7.3).

## 11. What this spec is not

Not a re-run or re-adjudication of Spec 024
or of Spec 059, not a new corpus, not a
string-identity join under any relabelling,
not a PRED evaluation, not a re-grading of
Spec 066's intake, and not an authorisation
to execute. It is Spec 059's gate-first
replication asked again on the enlarged
catalogue its predecessor's closure named —
designed so that its honest outcomes,
including a second closure at its own gate,
are written down before any row is joined.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
