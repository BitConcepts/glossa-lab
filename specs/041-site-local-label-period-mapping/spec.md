# Spec 041 — Site × Local-Label Period Mapping

> ## DRAFT — COMMISSIONED 2026-10-21; FREEZE IS A SEPARATE OWNER GATE
>
> This draft is commissioned by the owner's order of
> 2026-10-21 ("address all these remaining items now"),
> which takes up the item Spec 040's closure record
> (§3, "What would satisfy the gate") left as an owner
> decision: a separately governed act producing the
> placement mapping. The order commissions this
> **draft**. It is not a freeze order and not an
> execution order: the freeze (lifecycle hooks,
> decisions, digest, phase allocation) and the
> execution each remain separate owner gates, as with
> Specs 036–040. Drafts are standing pre-approved;
> nothing in this file has been frozen, filed, or run.

**Parent records:** Spec 040 (D-25, closed
NOT-YET-TESTABLE — dependency gate, 2026-10-20) ·
Spec 039 (gazetteer period-assignment act, executed
Phase-403) · Spec 025 / Phase-139 / Phase-140 /
Phase-385 (the G1 record) · **Phases:** none
allocated (allocation is a freeze act) · **Date of
proposal:** 2026-10-21.

**AI disclosure:** this proposal is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.

---

## 1. Why this spec exists

Spec 040 (D-25) asked whether Spec 025's G1 site
association survives when inscriptions are compared
only within the same coarse period. Its freeze-stage
dependency gate (spec §1) failed on two of four
conditions, verified first-hand at the freeze act and
recorded in Spec 040's outcome record:

- **Condition 2 — FAILED.** Spec 039's executed
  artifact assigns each *site* a **set** of coarse
  labels (the periods its published record spans).
  Spec 040 §4.1 consumes a different thing: for each
  inscription, its site and its **recorded local
  chronological label(s)** map to exactly one coarse
  period, to `UNASSIGNED`, or to a flagged contested
  assignment. The gazetteer artifact carries no
  local-label key; local period names appear only
  inside prose evidence strings, and reconstructing
  per-label pairings from that prose would be analyst
  judgement at execution time, which Spec 040 §4.3
  forbids.
- **Condition 4 — FAILED.** Three of the seven G1
  population sites — Chanhu-daro, Dholavira,
  Nausharo — have no gazetteer rows at all.

Spec 040's interface was not loosened to fit the
product (its DD-040-3), and G1 stands exactly as
Spec 025 and Phase-385 left it: SUPPORTED under
composition and preservation control, governing basic
CI [0.1838, 0.2102], with the rider **chronology is
NOT controlled** stated wherever G1 is stated.

The closure record (§3) states what would satisfy
the gate, and this spec is that act, commissioned on
the owner's order:

> A future, separately governed act producing a
> frozen, machine-readable mapping keyed by site ×
> the layer's recorded local chronological label(s)
> to one coarse period (or UNASSIGNED), every
> mapping carrying its published citation and
> locator and its contested flag, covering the
> population's seven sites — an artifact built to
> section 4's interface under the
> published-determinations-only standard.

One substitution must be named now, not discovered
later: Spec 040 §1 as written names **Spec 039's
product** as the artifact its gate inspects. This
act's product is not Spec 039's product. Nothing in
this spec rewrites Spec 040 §1. A future Spec 040
freeze act must record the substitution openly —
accepting this act's artifact, built to §4's
interface, in the place §1 describes — or decline
it. That decision belongs to that freeze and to the
owner; this draft only refuses to let it pass
unnoticed (§10, claim F041-C13).

## 2. The record the design stands on

### 2.1 The population — derived from the record

The G1 population is the Phase-137 F3 analysis
population, reproduced by rule in the Phase-140
freeze record (§2) and re-verified in the Phase-139
report (§1):

- **Layer:** the ICIT-lineage layer (horus84),
  `inscriptions.csv` — 5,679 rows × 38 fields,
  1,190,884 bytes, SHA-256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`
  (Spec 025 §3). The layer file is an acquired
  input, consumed read-only and hash-asserted; it
  is not committed to this repository.
- **Rule (Phase-137, verbatim):** sites eligible at
  ≥ 30 inscriptions AND ≥ 100 parsed tokens; rows
  with ≥ 1 parsed token.
- **The seven sites, with their population counts**
  (Phase-139 report §1): **Chanhu-daro (74),
  Dholavira (238), Harappa (2,717), Kalibangan
  (212), Lothal (208), Mohenjo-daro (1,923),
  Nausharo (38)** — 5,410 inscriptions.

### 2.2 How inscriptions carry local chronological labels

Each layer row carries its local chronological
labels in two fields, `period` and `phase`, recorded
by site excavation/reporting traditions. The layer's
missing sentinel is `-` for both fields (phase is
also blank on 2 full-layer rows). Coverage on the
population (Spec 025 §3.1, reproduced exactly by
Phase-139, report §2):

| Field | Informative on the population (n = 5,410) |
|---|---|
| `period` | 2,266 (41.9%) |
| `phase` | 2,638 (48.8%) |
| both | 1,788 (33.0%) |
| either (union) | 3,116 (57.6%) |
| neither | 2,294 (42.4%) |

Coverage is structural, not random (Spec 025 §3.2):
per-site `period` / `phase` informative shares are
Harappa 38.0% / 59.1% (both together: 0.6%),
Mohenjo-daro 41.8% / 41.5%, Kalibangan 74.5% /
59.0%, Lothal 46.2% / 50.5%, Dholavira 58.4% /
0.4%, Chanhu-daro 0.0% / 0.0%, Nausharo 100.0% /
7.9%. Two consequences this design accepts rather
than repairs: (i) no mapping, however complete, can
place the 42.4% of rows that record no label at
all — the coverage report must carry that ceiling
in its headline (§8); (ii) at Harappa the two
fields are informative on almost disjoint row sets,
so whether phase-field cells may place a row whose
period is unrecorded is the single largest coverage
question in the act — and it is a question about
the *consumer's* join rule, reserved accordingly
(§8).

### 2.3 The attested vocabularies, as recorded

The vocabularies are site-local (Spec 025 §3.3): the
same numeral does not denote the same chronological
unit at two sites. The most complete value-level
record in the repo is the Phase-139 citation
register (`data/evidence_integration/
phase139_citation_register.json`), built for Spec
025's harmonization. It records 35 mapped
(site, field, value) cells, the unmapped cells with
their reasons, and the unmapped classes:

- **Harappa** — period: `1, 2, 3, 4, 4/5, 5` mapped;
  `2/3`, `3/4` unmapped (boundary-spanning). Phase:
  `A, A-C, B, B/C, C` mapped; `B?` unmapped
  (queried); `Ravi` (1 row, never consulted);
  the Vats-era `Stratum I–VII` class unmapped (837
  rows — exactly Harappa's phase-only rows; no
  correlation to the HARP periodization was
  citable).
- **Dholavira** — period: `1, 2, 3, 4, 4/5, 5, 6`
  mapped; `5/6` unmapped (spanning); `5?` unmapped
  (queried). Phase: `F` unmapped (opaque).
- **Kalibangan** — period: `1, 2` mapped. Phase:
  `Early, Middle, Late` recorded as a class, never
  examined (period precedence made them
  unnecessary).
- **Lothal** — period: `A` mapped; `II` (1 row) not
  a label in Rao's scheme; the `Layer 2–15` class
  unmapped (105 rows carry layer-number period
  labels). Phase: `I, II, II-III, III, IV` mapped;
  `V` mapped (Late).
- **Mohenjo-daro** — period: `Early, Intermediate,
  Late` mapped. Phase: `I, II, III, IA, IB` class
  unmapped; singletons `II/III`, `III?` recorded
  (no population row depends on them: every
  phase-informative Mohenjo-daro row also carries a
  period value).
- **Nausharo** — period: `1, 2, 3` mapped; `4`
  unmapped (no Period IV exists in Jarrige's
  published scheme). Phase: `B, C` unmapped.
- **Chanhu-daro** — no informative period or phase
  value on any row.

This register is a **finding aid for this act, not
its census and not its evidence** (§3.3): it
records the cells one earlier audit consulted,
summarizes some vocabularies as classes rather than
distinct values, and was built under a precedence
rule this act does not use (§7.3). The act's own
value-level census is a step-0 product (§6, G0.3).

### 2.4 Why the Phase-139 harmonization does not already satisfy the interface

The Phase-139 `chron_band` is the obvious candidate
and it does not qualify, for reasons of record, not
of quality:

1. Its bands are **site-relative** (early / middle /
   late relative to each site's published sequence,
   Spec 025 §11 Q2(a)); Spec 040 §4.1 consumes the
   coarse codes `EARLY` / `MATURE` / `LATE`. The two
   vocabularies are close and are not the same
   object.
2. Its citations are **scheme-level** (7 citations
   for 35 cells), including restatements without
   pagination (a colloquium summary of another
   excavator's stages; a web concordance). The
   standard this act carries (§3) requires a
   locator per determination and verification in
   the publication's own text or a paginated
   published restatement.
3. It has **no contested mechanism**: a precedence
   rule (a mapped period cell wins over a mapped
   phase cell) with disagreements counted, not dual
   determinations retained under a contested flag.
4. Whole classes were deliberately left unexamined
   under that precedence (Kalibangan phase labels;
   Mohenjo-daro phase labels). The §4.1 interface
   resolves each attested label on its own evidence.
5. It is **constructed context (Class C)** and
   Spec 040 §4.3 bars it as the placement source by
   name: "The Phase-139 `chron_band` harmonization
   … D-25 replaces it as the primary period
   source."

## 3. The evidence standard (carried, not re-invented)

### 3.1 Published determinations only

The owner's evidence-standard decision of
2026-10-20 (Spec 039, Option 1) governs this act
unchanged: a mapping cell may rest **only** on a
published period determination — a publication's
own assignment of the site's local label (or its
local scheme) to a period — never on a
program-derived inference. Dates never assign a
period: no radiocarbon-to-period conversion, no
inheritance from the chronology spine's dated
contexts, no borrowing of a site-level label, no
analyst reconciliation.

### 3.2 The venue and locator test (DD-039-3, carried verbatim in substance)

A determination counts as published **if and only
if** it appears, **with a locator (page or
table)**, in (a) a peer-reviewed journal article,
(b) that article's published supplementary
material, or (c) a published excavation or survey
report in a named series. Not published under this
test: project-internal datasets and databases;
data deposits that are not period determinations;
unpublished survey records; and doctoral theses (a
thesis may corroborate; it does not solely ground
a cell). **Conservative default:** where a
determination's venue is doubtful, it does not
count, and the cell is treated as having no
determination from that source. A freeze may
widen the venue list openly; it may not narrow
the locator requirement.

For this act the primary sources are the sites'
published stratigraphic authorities — excavation
reports and site monographs stating the local
scheme and its period concordance (the class of
sources the Phase-139 register's citations name:
Marshall 1931 and Mackay 1938 for Mohenjo-daro;
Rao 1979 for Lothal; Jarrige 1993 for Nausharo;
Lal & Thapar for Kalibangan; Bisht for Dholavira;
the Meadow & Kenoyer periodization for Harappa) —
each admissible only as it passes the venue and
locator test above.

### 3.3 The verification bar

Following Spec 039's execution discipline, a
determination is **verified** only when it has
been read in the publication's own text, or in a
published restatement quoting it **with
pagination**. Anything else — a summary without
pagination, a secondary concordance, the Phase-139
citation register, the Phase-394 chronology spine,
a compilation's site list — is a **locator aid**:
it may point to the publication; it never grounds
a cell. A cell whose only support is a locator aid
is UNASSIGNED with reason DETERMINATION_UNVERIFIED
(§5.3) until the publication itself is read.

## 4. Inputs (pinned; to be re-pinned at the freeze)

| Input | Pin / state |
|---|---|
| ICIT-lineage layer (horus84 `inscriptions.csv`) | SHA-256 `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`; 5,679 rows × 38 fields; 1,190,884 bytes (Spec 025 §3) |
| Phase-137 results (`reports/phase137_results.json`) | The population record (rule, counts, profile configuration) |
| Phase-139 results + report (`reports/phase139_results.json`, `reports/phase139_report.md`) | The reproduced census tables (§2.2) and gate record |
| Phase-139 harmonized covariates (`data/evidence_integration/phase139_harmonized_covariates.json`) | SHA-256 `a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413`; carries `period_raw` / `phase_raw` per population inscription — a convenience copy; the layer is the source of record and step 0 asserts the copy against it (G0.3) |
| Phase-139 citation register (`data/evidence_integration/phase139_citation_register.json`) | Locator aid only (§3.3); never a determination source |
| Spec 040 spec + closure (`specs/040-d25-g1-chronology-controlled/spec.md` §§1, 4; `outcome.md` dependency-gate record) | The interface this artifact is built to, and the closure this act does not amend |
| Spec 039 adjudication (`specs/039-gazetteer-period-assignment/adjudication.md`, DD-039-3) | The carried evidence standard |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` — the **current** pin (see note); asserted byte-identical before and after; this act moves no anchor |

**Note on the anchors pin.** Spec 040's draft
carried the superseded value `eccea6d5…`; its
closure record (§3, secondary finding) establishes
that the anchors file has recomputed to
`df0cf620…` since 2026-10-12 (Spec 029 Phase H),
on current main and at that draft's own base. This
draft carries the refreshed pin, and any freeze of
this spec re-verifies it before use.

## 5. The mapping schema

### 5.1 The cell

The artifact is a set of **cells**, one per attested
local label. A cell is keyed by the triple:

- `site` — the layer's site string, **verbatim**
  (e.g. `Mohenjo-daro`). The key space is the
  layer's, not the gazetteer's `program_site_id`
  space: the consumer joins on layer rows
  (Spec 040 §4.1).
- `field` — `period` or `phase`: the layer field
  the label is recorded in. The same string in the
  two fields is two cells (Harappa phase `A` and a
  period value are different records with different
  published referents).
- `local_label` — the label string **verbatim** as
  recorded in the layer, including its uncertainty
  and span marks (`5?`, `2/3`, `A-C`, `Layer 15`).
  No normalization, no trimming of query marks, no
  splitting of spans: normalization is a mapping
  decision and is recorded as one, or the label is
  unassigned.

### 5.2 The value

Each cell carries exactly one `coarse_period` in
the Spec 040 §4.1 vocabulary: `EARLY`, `MATURE`,
`LATE`, or `UNASSIGNED` — the coarse codes, not
Spec 039's display strings and not Phase-139's
site-relative band names. Each cell also carries a
`status`:

- **MAPPED** — `coarse_period` is EARLY, MATURE,
  or LATE, grounded under §5.3.
- **CONTESTED** — two admissible published
  determinations assign the same cell different
  coarse periods (§7.2). `coarse_period` is
  `UNASSIGNED` for every binding use; both
  determinations are retained.
- **UNASSIGNED** — no admissible determination
  grounds a coarse period; `coarse_period` is
  `UNASSIGNED` and `unassigned_reason` (§5.4) is
  present.

### 5.3 The determination record

Every MAPPED cell carries exactly one determination
record; every CONTESTED cell carries two or more.
A determination record is:

- `citation` — the publication, in full.
- `locator` — page, table, or section where the
  determination appears (required by §3.2; a
  record without a locator is not a determination
  record).
- `mapping_rule` — the rule the publication's own
  text states or directly supports, in words (e.g.
  "the report's concordance assigns local Period 3
  (3A–3C) to the Mature Harappan period"). The rule
  is the publication's, quoted or closely
  paraphrased — never the analyst's synthesis of
  several publications.
- `verification` — `OWN_TEXT` (read in the
  publication itself) or `PAGINATED_RESTATEMENT`
  (read in a published restatement quoting it with
  pagination), naming the restatement in the
  second case.

A CONTESTED cell additionally carries
`contested: true` and may carry a
`sensitivity_label` **only** as the freeze decides
(DD-041-5, OPEN): Spec 040 §4.4 consumes a frozen
sensitivity label per contested mapping and treats
its absence as NOT ESTIMABLE for that mapping; the
schema therefore reserves the field, nullable,
rather than pretending the question away.

### 5.4 Unassigned reasons (enumerated; extension is a freeze amendment)

- `NO_PUBLISHED_DETERMINATION` — no published
  determination for this label was found in the
  sources the act's scope reached.
- `DETERMINATION_UNVERIFIED` — a determination is
  reported by a locator aid but could not be
  verified to the §3.3 bar within the act's scope.
- `SPANS_COARSE_BOUNDARY` — the label is by its
  published construction transitional across a
  coarse boundary (Harappa `2/3`, Dholavira `5/6`);
  no single coarse period is the publication's
  own assignment.
- `NOT_IN_PUBLISHED_SCHEME` — the label does not
  exist in the site's published scheme (Nausharo
  `4`).
- `LABEL_UNCERTAIN_IN_LAYER` — the layer itself
  records the label as queried (`5?`, `B?`) and no
  admissible determination resolves the queried
  label as recorded.

### 5.5 Completeness

Every (site, field, local_label) triple attested
on at least one population row appears in the
artifact **exactly once** — MAPPED, CONTESTED, or
UNASSIGNED with its reason. There are no silent
omissions: completeness is a mechanical check
against the step-0 census (§6, G0.3), run before
the artifact is pinned and reported in the
coverage report. Labels attested only on
non-population rows are enumerated in the coverage
report's secondary census; they are not cells
(the consumer's join covers the population).

### 5.6 Form

Two files, under `data/evidence_integration/`
(paths fixed by this draft; the freeze pins their
SHA-256):

- `site_period_mapping.jsonl` — one JSON object
  per cell (§5.1–§5.4), in key order.
- `site_period_mapping_meta.json` — provenance:
  the layer pin, the standard carried (§3), the
  census pins, cell counts by status, the freeze
  digest of this spec (entered at the freeze),
  and the AI disclosure.

## 6. Step 0 — fail-closed gates (margins and census only)

Step 0 runs before any cell is constructed. Any
gate failure closes the act at step 0 with **no
artifact** — a recorded step-0 closure, not a
partial product.

- **G0.1 — Layer identity.** The layer file hashes
  to the §4 pin (`c368f290…`), with 5,679 rows × 38
  fields. Any mismatch stops the act.
- **G0.2 — Population reproduction.** The
  Phase-137 rule applied to the layer yields
  exactly the seven named sites and 5,410 rows,
  asserted against `reports/phase137_results.json`
  and the Phase-139 report §1 counts.
- **G0.3 — Label census.** The value-level census
  is produced from the layer: for each population
  site × field, every distinct informative value
  with its row count. Its headline counts must
  reproduce the recorded tables exactly —
  population period 2,266, phase 2,638, both
  1,788, union 3,116 (Spec 025 §3.1; Phase-139
  report §2) — and the Phase-139 covariates
  file's `period_raw` / `phase_raw` values must
  agree with the layer's on every population row.
  Any mismatch stops the act. The census is
  committed as a step-0 artifact; it is the
  completeness denominator of §5.5.
- **G0.4 — Anchors.** The anchors file hashes to
  the refreshed pin (`df0cf620…`, §4 note) before
  construction and is asserted byte-identical
  after the act.
- **G0.5 — Source admissibility.** Every source
  the construction expects to use is classified
  against §3.2 *before* extraction: admissible
  determination source, or locator aid. The
  classification list is committed with the step-0
  record. A source reclassified mid-construction
  is recorded as a dated deviation with the cells
  it touched re-examined under the new class.
- **G0.6 — No-computation fence.** Step 0 computes
  margins and census counts only: no repertoire
  quantity, no association statistic, no G1
  quantity of any kind (the Phase-139 fence,
  carried). The construction stages likewise
  compute no inscription-level join: the artifact
  is cells, and the join is a future consumer's
  act (§8).

## 7. Construction rules

### 7.1 Extraction

For each attested cell, the construction seeks the
site publication's own assignment of that local
label (or of the local scheme containing it) to a
coarse period. One cell, one determination: a cell
is MAPPED when a single admissible, verified
determination assigns it exactly one coarse
period. Where a publication assigns a label to a
span crossing a coarse boundary, the cell is
UNASSIGNED / `SPANS_COARSE_BOUNDARY` — the span is
the publication's statement and is recorded as
such; it is never split by proportion, midpoint,
or majority of years.

### 7.2 Contested cells — no reconciliation

Where two admissible determinations assign the
same cell **different** coarse periods, the cell
is CONTESTED: both determinations are retained
verbatim (citation, locator, mapping rule,
verification), `contested: true` is set, and the
binding `coarse_period` is `UNASSIGNED`. No
preference rule applies — not source tier, not
recency, not the hierarchy of DD-039-2 (which
orders presentation, never truth): under this
act, disagreement between admissible publications
is a fact of the record, and the cell carries it.
A future consumer's primary computation excludes
contested cells (Spec 040 §4.2/§4.4 posture); its
sensitivity treatment is that consumer's freeze
decision, prepared for — not made — by this act
(§5.3, DD-041-5).

### 7.3 No precedence, no skipping

Phase-139's precedence rule (period cell wins over
phase cell) is **not** carried: it was a covariate
construction rule for a sensitivity panel, and
under it whole label classes were never examined.
Here every attested cell is resolved on its own
published evidence — including the classes
Phase-139 left unexamined (Kalibangan phase
`Early / Middle / Late`; Mohenjo-daro phase
labels; Harappa `Stratum I–VII`; Lothal `Layer
2–15`; Nausharo phase `B, C`; Dholavira phase
`F`) — or is UNASSIGNED with its reason. A class
for which no published correlation exists is a
legitimate, expected outcome for part of the
vocabulary; recording it honestly is the act's
work, not its failure.

### 7.4 Dual verification

Every MAPPED and CONTESTED cell is independently
re-verified before the artifact is pinned: a
second pass opens each cited locator and reads
the determination there. A cell whose
determination does not read as recorded is
reclassified under the rules — to CONTESTED if a
second admissible reading stands, to UNASSIGNED /
`DETERMINATION_UNVERIFIED` if none does — and the
reclassification is recorded in the coverage
report. No cell is edited into agreement.

## 8. The row-level question this act deliberately does not decide

The artifact maps **labels**. How a future consumer
turns an inscription's recorded label(s) into one
period stratum is Spec 040 §4.2's business, decided
by that spec's future freeze — including the
question §2.2 flags: what happens when a row
carries two informative labels whose cells differ,
or one mapped and one unassigned label. So that
decision is made on numbers, the coverage report
publishes inscription-row placement counts under
each of three candidate derivations, by site and by
coarse period:

- **A — agreement of mapped labels** (the
  §1-condition-2 literal reading): a row is placed
  iff at least one of its labels is MAPPED and
  every MAPPED label agrees; a row whose only
  mappings are contested is unplaced; whether an
  UNASSIGNED cell vetoes a placed row is stated
  for both readings (A1: no veto; A2: veto).
- **B — period precedence** (the Phase-139
  precedent): the period cell governs when MAPPED;
  the phase cell governs only when the period
  value is unrecorded.
- **C — phase-eligible union**: either field's
  MAPPED cell places the row; disagreement between
  two MAPPED cells leaves the row unplaced.

For every candidate: placed rows overall and by
site; placed rows by coarse period; unplaced rows
split by cause (no informative label; labels
attested but all UNASSIGNED; disagreement;
contested-only). The report states the ceiling
with the counts: at most 3,116 of 5,410 rows
(57.6%) carry any label, so no derivation places
more than that share, and the mapping's own
coverage further bounds each candidate. **This act
adopts no derivation and reports no preferred
one**; the counts are the deliverable.

## 9. Deliverables

1. The step-0 record: gate outcomes G0.1–G0.6 and
   the value-level census (committed).
2. The mapping artifact (§5.6), pinned by SHA-256
   in the outcome record.
3. The coverage report: cell counts by site ×
   field × status; the §8 placement counts under
   derivations A1/A2/B/C; the secondary
   (full-layer) attestation census; the dual-
   verification record, including every
   reclassification; the ceiling statement (§8).
4. The outcome record in this directory: the
   artifact's pin, the gate and construction
   record, claim consequences per claim, and the
   statement — in the Spec 040 §10 headline form —
   of what the artifact is and is not for.
5. The experiment-graph node for the execution
   phase (graph-first, H15/H23), registered and
   verified before any run; the LEDGER entry; the
   foundation check as measured at the record
   merge.

## 10. Fences — what this act does not do

- **It does not re-run G1.** No repertoire
  quantity, permutation, interval, or verdict is
  computed under this spec, at any stage (G0.6).
- **It does not amend any frozen record.** Spec
  040's closure stands as recorded — including
  its NOT-YET-TESTABLE state and the open
  DD-040-1/5/6/9/10. Spec 039's artifact stands
  byte-identical. Spec 025, Phase-140, and
  Phase-385 stand. G1's rider stands verbatim.
- **It does not satisfy Spec 040's gate by
  existing.** Satisfaction is judged by a future
  Spec 040 freeze act against §1, which as
  written names Spec 039's product (§1 of this
  spec); the substitution decision is that
  freeze's, openly recorded, or the gate fails
  again. A satisfied dependency would still
  require that freeze act (hooks, the DD-040
  decisions, a digest) and a separate execution
  order, exactly as Spec 040's closure states.
- **It does not date objects.** A MAPPED cell
  places a *recorded label* in a coarse period on
  a publication's authority. An inscription with
  no recorded label is unplaced; an inscription
  whose label is UNASSIGNED is unplaced; neither
  state is a defect to be repaired by site
  reputation, depth, context, or dates.
- **No anchor, reading, or PRED contact.** The
  anchors file is asserted, never moved; no
  PRED-2026 state is touched; no sign's meaning
  is claimed anywhere in the artifact or its
  reports.

## 11. Epistemic limits (binding on all outputs)

1. Everything here describes the **ICIT-lineage
   layer (horus84)** — a derivative of the ICIT
   database in open file form, not an independent
   witness. The lineage label is mandatory in
   every headline, report, and ledger entry.
2. The mapping is a **scholarly-coding artifact**:
   its cells are only as good as the published
   determinations they quote, and its provenance
   (citation, locator, verification mode) travels
   with every use. A consumer that drops the
   provenance misquotes the artifact.
3. The local labels themselves are **records of
   excavation traditions**, unevenly kept (§2.2);
   the mapping translates vocabularies, it does
   not repair their missingness, and its coverage
   numbers must never be quoted without the
   57.6% ceiling they sit under.
4. Compilation-internal explanations remain live:
   the layer's labels and the publications'
   concordances sit inside overlapping scholarly
   traditions, and a mapping built from them does
   not manufacture independence.
5. Negative outcomes are published as found: an
   act that returns mostly UNASSIGNED cells has
   still done its work, if the record shows why,
   cell by cell.

## 12. Risks and honest weaknesses

- **Print access.** The stratigraphic authorities
  are 1931–1993 excavation literature. Cells whose
  publications cannot be obtained and read (in
  their own text or a paginated restatement)
  within the act's scope land at
  DETERMINATION_UNVERIFIED; the acquisition scope
  is an open freeze decision (DD-041-6), and the
  coverage report must state which cells it
  decided.
- **Small-vocabulary judgement concentration.** The
  attested vocabulary is small (dozens of cells),
  so a single contested or unverifiable cell moves
  row counts materially at the small sites
  (Nausharo 38 rows; Chanhu-daro's 74 rows carry
  no labels at all and cannot be placed by any
  mapping). Dual verification (§7.4) and the
  retention rule (§7.2) are the mitigations; they
  do not create evidence.
- **The Harappa phase class.** `Stratum I–VII`
  covers 837 rows — the largest single unmapped
  class. If no published correlation to the HARP
  periodization exists, those rows stay unplaced
  under every §8 derivation, and the future
  consumer's margins gate will see that honestly.
  This draft does not soften that prospect.
- **Restatement drift.** Concordances summarize;
  a restated concordance can shift a boundary the
  original text states otherwise. The
  verification bar (§3.3) prefers the publication's
  own text wherever both exist, and
  `verification` records which was used, cell by
  cell.

## 13. Execution shape (gated; NOT run by this draft)

1. **Freeze act** (owner order): AEE lifecycle
   hooks over the claim register (the Spec 035
   ordering — hooks before the digest, the digest
   computed once over the recovered register);
   the OPEN decisions of `adjudication.md` §4
   decided or expressly reserved; `freeze.md` /
   `freeze.json` finalised; the execution phase
   number allocated; the OSF decision (DD-041-7)
   taken.
2. **Execution** (separate owner order): graph-
   first build (script, graph module, registration,
   verification); step 0 (§6); extraction (§7.1);
   contested and unassigned classification
   (§§7.2–7.3); dual verification (§7.4);
   completeness check (§5.5); artifact + coverage
   report (§9); outcome record and pins.
3. Nothing at either gate re-opens §10's fences.

## 14. What this spec is not

Not a G1 rerun, not a Spec 040 revival (its freeze
is a separate future act that may still decline),
not a gazetteer amendment, not a data-acquisition
spec (sources are sought only to read
determinations, under the freeze's scope decision),
and not an authorization: if the owner declines
the freeze, the correct outcome is a one-line
record that Spec 041 was proposed and declined,
with Spec 040's closure standing as the program's
final word on the dependency.
