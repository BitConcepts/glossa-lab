# Spec 030 — Q6 Chronology-Spine Extension (Design Draft)

> ## DRAFT — NOT FROZEN (2026-10-12)
>
> Design draft prepared at the owner's direction
> (2026-10-12: "Do all we can do today, no reaching out
> yet"). This is internal design work only: it freezes
> nothing, executes nothing, and contacts no one. It
> returns to the owner as a decision packet; §9 lists the
> asks an adjudication would need to answer.
>
> Placement: this design takes the next spec number
> (030) rather than living under `specs/027/`, following
> the repository's convention that a new study line gets
> its own spec directory (Spec 028 was likewise a
> follow-up to Spec 027 with its own number). The Q6
> *question* remains owned by Spec 027 (§8.2, claim
> F027-C16); this spec owns only the data extension that
> could make Q6 freezable. Governed claims for this
> design are in `claims.json` (F030-C01…C07, all draft).

## 1. Purpose

Spec 027 Stage 0 (Phase-391) built the chronology spine
(177 traced rows) and assessed Q6 timing-support against
criteria frozen **before the spine existed**
(`specs/027-movement-culture-language/stage0-freeze.md`
§4). The assessment returned **NOT-YET-TESTABLE**: three
of four criteria failed. Q6 therefore remains
registered-blocked, and F027-C16 forbids a Q6 freeze
until the §8.2 support conditions are shown.

This spec designs the **spine extension**: the audited,
traced additions that could let the *same frozen
criteria* pass on re-test — or could show, on margins
only, that they still cannot pass from lawfully usable
sources. The extension study mints no timing verdict.
Its only verdict-shaped output is the re-run §4
assessment (SUPPORTED-FOR-FREEZE-DESIGN or
NOT-YET-TESTABLE, with criterion-level values), exactly
as Stage 0's was. A Q6 freeze, if the re-test ever
supports one, is a separate later act under Spec 027
§8.2 with its own freeze and owner gate.

## 2. The frozen criteria and the measured gaps

Criteria (stage0-freeze.md §4, verbatim thresholds; the
window is 5250–3850 BP, i.e. 3300–1900 BCE; "d/a" =
`direct` or `associated` context-association grade).
Stage 0 values from `reports/phase391_results.json`,
verified at row level against
`data/movement/chronology_rows.jsonl` on 2026-10-12:

| # | Criterion (frozen) | Threshold | Stage 0 | Gap |
|---|---|---|---|---|
| C1 | Program regions each contributing ≥2 distinct sites with ≥1 d/a row | ≥3 regions | **1** (PK only) | 2 more regions at ≥2 d/a sites |
| C2 | Distinct sites with ≥1 d/a row in the window | ≥10 sites | **5** | +5 window d/a sites |
| C3 | Short-lived share among window d/a rows | ≥0.50 | **0.0** (0 of 31) | the binding constraint (§3.3) |
| C4 | Median reported 1σ among window d/a rows | ≤80 BP | **70 BP — PASS** | must not regress (§3.4) |

The 31 window d/a rows sit at exactly five sites —
Islam Chowki, Shahr-i Sokhta, Sheri Khan Tarakai 3,
Sheri Khan Tarakai 4, Ter Kala Dheri — and are **all**
graded `associated` and **all** long-lived material
(30) or unknown (1). Not one is short-lived.

## 3. Gap anatomy — what exactly is missing, per criterion

Regions are as recorded on spine rows (country codes:
PK, IN, IR, FI, TM). The region scheme is inherited,
not redesigned; re-regioning would be a criteria
change, which C01 (claims register) forbids here.

### 3.1 C1 — regions

- **PK qualifies**: 5 d/a sites (Islam Chowki,
  Mehrgarh, Sheri Khan Tarakai 3, Sheri Khan Tarakai 4,
  Ter Kala Dheri). Note Mehrgarh's d/a status rests
  entirely on the Mutin et al. 2025 rows, scenario
  **CONTESTED** — see the sensitivity rule in §5.
- **IN — the primary route.** 44 rows, 10 sites, **zero
  graded**: Hiregudda (13 rows), Sannarachamma (12),
  Qasim Bagh (10), Ojiyana (3), and single rows for
  Banawali, Kanispur, Khirsara, Kunal, Piklihal,
  Tigrana. IN already carries 22 short-lived rows
  (unassessed). Grading uplift (§4, R1) plus targeted
  extraction (R3/R4) has ten candidate sites to reach
  ≥2; no other region offers this depth.
- **TM — the cheap second route.** Three sites
  (Chagylly, Mullali, Yalangach), one row each, all
  unassessed. Whether any can be graded depends wholly
  on what the origin publications record; a desk audit
  (R1) answers this at near-zero cost.
- **IR — the hard route.** Shahr-i Sokhta is the
  spine's *only* Iranian site (32 rows). No second IR
  site exists anywhere in the Stage 0 sources, so IR
  ≥2 requires new data (§4, R3 search scope), not
  grading.
- **FI cannot qualify.** One site (Joenniemi, a
  far-northern record inside the frozen lat/long box).
  Recorded so the freeze does not chase it.

**C1 is met iff IN reaches ≥2 d/a sites AND at least
one of {TM, IR} reaches ≥2** (PK standing). The design
pursues IN as the plan of record, TM as the parallel
cheap audit, IR as a search — in that order.

### 3.2 C2 — window sites

Five window d/a sites; ten required. In-spine grade-up
candidates (window rows currently `unassessed`):
Tigrana (1 row), Qasim Bagh (1), Sheri Khan Tarakai
base cluster (6), Joenniemi (3). Even if **every**
grade-up succeeds, the ceiling is **9** — so at least
one genuinely new window-dated d/a site from extraction
is mathematically required, and prudently several,
since grade-ups fail whenever the origin record does
not name a feature.

Two cautions the freeze must carry:

- The Sheri Khan Tarakai base cluster is a separate
  `program_site_id` only because name normalisation kept
  it separate from clusters 3/4 (Stage 0 conflict
  report). It earns C2 credit only if origin-record
  tracing shows it is a distinct site assertion, not
  the same physical site under a variant name.
- A site-name match is not an occupation date. The
  spine's single "Harappa" row (OxA-30061, wheat,
  3499 BP, cited to Guedes & Bocinsky 2018) is a
  crop-context date outside the window — it is evidence
  about why grading inspects contexts, not a Harappa
  chronology.

### 3.3 C3 — short-lived share (the binding constraint)

Current window d/a pool: 31 rows, 0 short-lived. Let
*g* = long-lived/unknown window rows graded up from the
existing pool, *s* = net new short-lived window d/a rows
(including any material reclassifications, §5). The
re-test passes C3 iff

> (s) / (31 + g + s) ≥ 0.5, i.e. **s ≥ 31 + g**.

Consequences the design states plainly:

- **Floor case (g = 0): ≥31 net new short-lived window
  d/a rows are required.** There is no cheaper path;
  the single in-window short-lived row in the whole
  spine (Tigrana, wheat, 4058 BP, currently unassessed)
  is 1 toward that count if its origin record supports
  grading.
- **Long-lived grade-ups make C3 harder, row for row.**
  Grading up just the 8 long-lived window rows at the
  Sheri Khan Tarakai base cluster and Joenniemi (g = 8)
  raises the requirement to s ≥ 39 (the two
  unknown-material window rows at the base cluster and
  Qasim Bagh would raise it further). Grade-up effort must
  therefore be *selective*: prioritise sites whose
  window rows are short-lived or unknown-material, and
  count a site toward C2 through its best rows — the
  build must never grade up long-lived window rows
  merely because it can. (Grading itself stays rule-
  bound per row; the selectivity is in which origin
  records the build traces first, and the final pool is
  whatever the traced records support — §5 forbids
  excluding a traced row to game the share. If selective
  tracing order is itself judged a bias risk, Ask 3 in
  §9 puts the alternative — trace everything, accept
  the higher s requirement — to the owner.)
- Most short-lived rows the spine already holds fall
  **outside** the window (Ojiyana 3830 BP, Khirsara
  3760, Kanispur 3770, Kunal 3150, Harappa 3499,
  Banawali 1860) — Late/transition dates. They cannot
  be pulled into the window; C3 mass must come from
  Mature-window contexts, which is precisely the
  published record's thinnest stratum for the Indus
  core. Whether ≥31 such traced rows exist in lawfully
  usable sources is an empirical question the route
  audits (§4) answer in order; the design does not
  presume the answer.

### 3.4 C4 — precision guard

C4 passes at 70 BP and is re-checked on the final pool.
Short-lived AMS dates in the target literature
typically report σ well under 80 BP, so the extension
is expected to hold or improve the median; the build
monitors the running median and the re-test fails
honestly if additions regress it past 80. No separate
action is designed for C4 — it is a stop condition,
not a target.

### 3.5 Joint build targets (design targets, not criteria)

The extension build is complete when, on margins only:

- **T1:** IN has ≥2 d/a sites and at least one of
  {TM, IR} has ≥2 (C1 path);
- **T2:** ≥10 window d/a sites (C2 path);
- **T3:** the C3 inequality holds with the final pool,
  with new short-lived window d/a rows spread across
  ≥4 sites not previously window-d/a where the sources
  allow (so T2 and T3 are carried by substantially the
  same new evidence, not by one site's date list);
- **T4:** final window d/a median σ ≤ 80 BP (C4 held);

or when the route audits (§4) have shown, with their
searches recorded, that the targets cannot be met from
lawfully usable sources — a **negative extension
closure**, which is a valid outcome of this study, not
a failure to be edited away (claim F030-C07).

## 4. Extension routes — candidate sources and licence posture

All postures are as recorded in Spec 027 §5/§5.1 and
the Stage 0 freeze §2; anything not lawfully reusable
is catalogued, not copied. No route involves contacting
anyone; a source that turns out `permission_required`
stops at catalogue and is reported (Ask 4, §9).

- **R5 — XRONOS re-retrieval (do first; cheapest).**
  The Stage 0 export was retrieved 2026-10-11
  (database as served, site news v1.1.1) and is
  sha256-pinned in the Stage 0 freeze. XRONOS is a
  living database. The extension re-retrieves under a
  pinned version, diffs against the Stage 0 export, and
  admits new in-box records under the Stage 0 rules
  verbatim. Licence: `verified_open` (CC BY 4.0).
- **R1 — Origin-record tracing of existing rows.**
  Every spine row already carries lab code + cited
  reference (144/144 XRONOS rows). F027-C16's own
  evidence origin group for Q6 support is
  "xronos-underlying-databases". The build resolves
  each row's origin publication/database and extracts
  what the export's flat fields dropped: feature /
  context descriptions (the input to grading under the
  frozen rule), the origin material string, and any
  sibling dated records for in-spine sites that the
  §3.1 coordinate filter excluded. Posture: the origin
  publications are read as published scholarship;
  factual assertions derived from them enter as
  `open_access_read_only` (the Phase-124 CISI
  precedent) unless the origin database is itself
  `verified_open`.
- **R2 — c14bazAAR source-database audit (D5).**
  Stage 0 recorded this route `catalogue_only` with an
  explicit gap: *no c14bazAAR source database was
  verified to add greater-Indus records beyond the
  XRONOS export* — unverified, not verified-empty. The
  extension enumerates the aggregator's current source
  databases, verifies each one's licence individually
  (postures differ per database), checks each for
  in-box records beyond XRONOS's, and ingests only
  `verified_open` databases, recording the origin
  database per row (an aggregator is never an origin
  group; Spec 027 §5, D5).
- **R4 — TwoRains published-supplement audit (D7).**
  The TwoRains Haryana survey data live in paper
  supplements "not audited for reuse" (Stage 0 freeze
  §2.2). The extension audits those supplements for
  site dates and their reuse terms. Haryana is IN
  region and holds window-adjacent Harappan sites, so
  this route serves T1/T2 if its terms allow. Posture
  until audited: `catalogue_only`.
- **R3 — Targeted published-date extraction (highest
  yield, most labour).** Excavation reports and journal
  date lists for excavated Mature Harappan sites whose
  chronology the XRONOS export lacks entirely (the
  Phase-391 report names the hole: no XRONOS dates for
  Mohenjo-Daro, Harappa, Rakhigarhi, Dholavira,
  Kalibangan, or Lothal). Priorities follow criterion
  service: IN-region sites first (T1/T2/T3 jointly),
  then a search for a second IR site's published dates
  (T1's IR branch — the search scope is defined here;
  candidate sites are established by the search, not
  pre-named). Each extracted row is traced to
  publication + table/page locator + lab code, and
  enters as `open_access_read_only` under the Phase-124
  precedent: usable in the spine, excluded from any
  CC BY release package (Ask 4 posture; Spec 027 §5.1).

**Explicitly not routes:** Possehl/Law settlement
lists (settlement data, not dates; `catalogue_only` —
they serve the gazetteer, not the spine); any further
Mutin-style single-study chronology except as
CONTESTED-scenario rows; any source whose licence is
unverified at build time.

**Route order and stop points.** R5 → R1 → R2 → R4 →
R3, with a margins-only interim assessment after each
route (same computation as §6, on the then-current
pool, outcomes uninspected beyond the four criterion
values). The owner may stop the build at any interim
assessment; if the joint targets are shown unreachable
with routes remaining, that showing is itself the
negative closure and R3's labour is never spent.

## 5. Integrity rules (binding on any future freeze of this design)

Extending stage0-freeze.md §3.3/§3.4, unchanged where
they already speak:

1. **Trace or don't build.** Every added row carries
   origin source, source locator, lab code, licence
   state, origin group, region as recorded by its
   source's geography under the Stage 0 scheme, and a
   scenario tag where applicable. A row missing any
   trace field is not built (fail loud, as Stage 0's
   validators did).
2. **One measurement, one row.** Identity is the lab
   code (with age/material as corroboration). The same
   measurement reached via XRONOS, an origin database,
   and a publication is one row with three trace
   citations — never three rows. Dedupe is run before
   any assessment, and its counts are reported.
3. **Grading by the frozen rule, on origin records.**
   `direct` only where the dated material is itself the
   claimed event; `associated` only where the *origin
   record* names a feature for the sample; otherwise
   `unassessed`. No grading by inference, and no
   exclusion of a traced row from the pool to shape a
   criterion value. The feature evidence behind every
   grade change is recorded per row (locator + the
   naming text).
4. **Material by the frozen mapping, on the origin
   string.** The Stage 0 material mapping applies to
   the origin record's material string, preserved
   verbatim. A reclassification from the XRONOS-export
   string to a different origin string is a traced
   correction (both strings kept, origin cited), never
   an inference from context.
5. **CONTESTED never silent.** Scenario tags persist at
   row level. The re-test (§6) reports every criterion
   twice: as frozen (all rows) and excluding
   CONTESTED-scenario rows. PK's C1 qualification
   currently depends on Mehrgarh's contested rows under
   the second computation (PK falls to 4 d/a sites —
   still ≥2, so C1's PK leg survives; whether any
   *other* leg depends on contested rows is reported
   the same way). Ask 2 (§9) puts to the owner whether
   the sensitivity is report-only or binding on a
   future Q6 freeze.
6. **No calibration computed.** As in v1, conventional
   ages only; calibration and any Bayesian timing
   model belong to the future Q6 freeze (Spec 027
   §8.2), not to this extension.
7. **Coordinate-less dated records.** A dated record
   whose origin carries no coordinates may enter the
   chronology for a site whose cluster the gazetteer
   already establishes, with the chronology row's
   coordinate state recorded as inherited-from-cluster
   — *proposed here, requiring freeze-level adoption*
   (Ask 1, §9), because Stage 0's §3.1 filter admitted
   only coordinate-bearing records. Gazetteer changes
   otherwise out of scope, except assigning
   `program_site_id` to genuinely new sites under the
   frozen name normalisation.

## 6. Re-test protocol (Q6 timing-support, on the extended spine)

1. Inputs pinned by sha256 (extended spine products +
   this spec's build script) before the assessment
   runs; the assessment script is registered in the
   experiment graph before execution (H23), under the
   phase number assigned at freeze (proposed:
   **Phase-394**, the first free number after
   Phase-393).
2. The assessment is the stage0-freeze.md §4 assessment
   **verbatim**: same four criteria, thresholds, window,
   and grade vocabulary, computed from spine margins and
   metadata only. No trait list is built, no
   first-appearance outcome is inspected, no timing
   model is fitted (claim F030-C05).
3. Report: per-criterion values vs thresholds, the §5.5
   CONTESTED sensitivity per criterion, dedupe counts,
   per-route row contributions, and the licence posture
   distribution of added rows.
4. Outcomes: **SUPPORTED-FOR-FREEZE-DESIGN** — a Q6
   freeze may then be *designed* under Spec 027 §8.2
   (which additionally requires the declared timing
   model, priors, and per-rival thresholds; none of
   that is in this spec) — or **NOT-YET-TESTABLE**, with
   the failed criteria and their remaining gaps
   reported, Q6 staying registered-blocked, and the
   extended spine standing as infrastructure either
   way.
5. The re-test changes no Spec 027 record. Its outcome
   is recorded here (or in this spec's outcome record)
   and referenced — never written into — Spec 027's
   freeze records.

## 7. What this design does not do

- No Q6 freeze, trait list, timing model, or verdict.
- No execution and no external contact of any kind.
  The route audits are desk audits of published
  material; any source requiring permission is
  catalogued and reported, not pursued.
- No change to any frozen criterion, threshold, grade
  rule, or material mapping (F030-C01). No period-label
  timing table as a substitute for dates (Spec 027
  §8.2; forbidden assumption ASM-PERIOD-LABEL-AS-TIMING
  is inherited).
- No anchor, PRED-2026, or sign-list contact. No
  gazetteer rebuild (see §5.7 for the one proposed
  exception).

## 8. Governed claims (summary)

Full register: `claims.json` (F030-C01…C07, all
`draft`). In one line each: the frozen criteria apply
verbatim (C01); every row is fully traced or not built
(C02); no measurement is counted twice (C03);
CONTESTED dependence is always reported (C04); the
re-test inspects margins only (C05); licence posture
follows Spec 027 §5.1 and gates any release (C06); a
negative extension outcome is a valid closure, never
grounds to loosen a criterion (C07).

## 9. Asks for adjudication (owner decisions)

1. **Coordinate-less chronology rows (§5.7).** Admit
   dated records without origin coordinates for
   gazetteer-established sites, or hold Stage 0's
   coordinate-bearing-only rule (which caps R1's yield
   at whatever the export's filter already passed)?
2. **CONTESTED sensitivity (§5.5).** Report-only, or
   binding — i.e. must a future Q6 freeze's support
   assessment hold with contested rows excluded?
3. **Tracing selectivity (§3.3).** Trace origin records
   in short-lived-first order (the design's proposal,
   with the full pool reported), or trace everything
   before any assessment (slower; raises the C3
   requirement by every long-lived grade-up)?
4. **Route scope and posture.** All five routes in the
   §4 order with interim stop points, or a subset? And
   confirm: `open_access_read_only` extraction (R3) is
   internal-spine-only, never released — mirroring the
   CISI precedent — or is R3 out of scope entirely?
5. **Phase and registration.** Register the build as
   Phase-394 at freeze, and mirror Stage 1's OSF
   registration of the frozen contract before any
   execution?

AI disclosure: drafted by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI. All figures are from the merged
record cited inline; nothing here is frozen or
executed.
