# Spec 024 — Stage 1 Freeze Record (Phase-134)

> ## FROZEN 2026-10-09 — Stage 1 motif-coding pilot
>
> Owner go: Tristen Pierson, 2026-10-09 — "Approve
> the Stage 1 motif-coding pilot" (the separate
> post-Stage-0 go that spec §4 and Decision Ask 2
> reserved). Coder basis: blinded AI double-coding
> with the Phase-132 disclosure, settled at the
> Spec 024 freeze (Decision Ask 3). This freeze was
> committed **before any sample image was viewed
> by any coder** and before the frame was drawn.
> Spec §4 governs; this record sets the values §4.2
> left to the stage freeze (final size, strata,
> draw rule, seed) and freezes the codebook,
> record schema, and metric definitions.

## 1. Premise correction of record (population)

The Stage 0 report and the execution brief refer
to the sample population in shorthand as the "909
catalogue objects carrying `motif_chapter`."
Verification from the catalogue files (this
freeze) shows that population is **degenerate as
a sampling frame for a taxonomy-wide reliability
pilot**: of the 909 distinct objects carrying a
`motif_chapter` value, **899 (98.9%)** carry a
unicorn-chapter value (OCR variants `unicorn`,
`unicorm`, `unicom`, `unicon`, `uricorn`,
`unico`); the remainder are section headers
(`SEALS` ×4, `SEALSIMPRESSIONS` ×3) and one
composite header (`tigerwithzebu` ×3). A frame
drawn from that subset could not exercise the
§4.3 taxonomy and would manufacture agreement.

The frozen spec §4.2 governs, and this freeze
follows it: the population is **all catalogue
objects carrying an adjudicated volume-scoped
object key and at least one extractable
photograph**, stratified by site and object type
(§2 below). The `motif_chapter` values of sampled
objects are used only for the post-hoc descriptive
concordance count of §6 — unblinded after coding,
reported as concordance, never as accuracy and
never as a coding input (§4.4).

## 2. Frame (frozen)

- **Canonical key:** `cisi:v{volume}:{cisi_id}`
  (volume-scoped, per §3.3 / the H-311 lesson).
  Holdat `cisi_number` is prohibited as a key
  anywhere in this stage.
- **Eligibility:** a catalogue object (distinct
  volume-scoped key) with ≥1 photo row whose
  `photo_box_xywh` parses to four integers, and
  `object_type` ∈ {Seals, Tablets, Graffiti}.
  Site group: `Mohenjo-Daro` / `Harappa` /
  `Other` (every other site value, including
  blank, groups as Other). Eligible population
  as computed at freeze: **3,245 objects**
  (excluded: 249 — no parseable photo box or
  object type outside the three strata).
- **Size:** exactly **100** objects.
- **Allocation:** proportional to the 9
  (site group × object type) cell populations
  by largest remainder, minimum 2 per non-empty
  cell, adjusted by largest-remainder residuals
  to total exactly 100. Cell populations and
  quotas are printed by the frame script into
  the frame record.
- **Selection:** within each cell, objects are
  ordered by `sha256("phase134-20261009|" +
  canonical_key)` ascending (hex) and the first
  `quota` are taken. Seed string:
  `phase134-20261009`.
- **Replacement rule:** if image-packet prep
  fails for a drawn object (no photo row yields
  a crop — missing page render or unparseable
  box on every row), the next object in the same
  cell's hash order replaces it. Failures and
  replacements are logged in the frame record.
  Replacements occur **only before coding
  starts**; the frame locks when the first
  coder packet is issued.
- **Gold subset:** the drawn frame, sorted by
  the same hash, indices 0, 5, 10, …, 95 →
  **20 objects**, triple-coded by a third
  blinded coder (§4.4 drift measurement).

## 3. Codebook as frozen (§4.3 categories)

Coders classify **what is depicted** — the
primary motif of the inscribed face. Exactly one
primary code per object, from:

| Code | Category | Visual definition (depictions only) |
|---|---|---|
| `UNICORN` | Unicorn | Single-horned bovine in profile (one horn visible/drawn), often with a manger/trough or collar-like bands |
| `ZEBU` | Zebu / bull | Humped bull, two horns |
| `BUFFALO` | Buffalo | Bovine with large curved horns sweeping sideways/back, no hump |
| `ELEPHANT` | Elephant | Elephant, with or without rider/howdah cloth |
| `RHINOCEROS` | Rhinoceros | Massive body, one or two horns on the snout, thick folded skin |
| `GOAT_ANTELOPE` | Goat / antelope | Slender horned quadruped (goat, ibex, markhor, antelope-like), no hump |
| `TIGER` | Tiger | Striped feline |
| `COMPOSITE` | Composite creature | A single creature of mixed anatomy (combined body parts, multi-headed, human-animal hybrids as one figure) |
| `HUMAN_CULT` | Human figures / cult-narrative scene | Human figure(s) as principal actors — processions, combat, deity-in-tree, offering and narrative scenes |
| `GEOMETRIC` | Geometric design | The depiction is a geometric/linear design only (no creature or human figure) |
| `SCRIPT_ONLY` | Script only / no depiction | No depiction on the inscribed face — inscription only |
| `ILLEGIBLE` | Illegible / cannot code | A depiction area exists (or may exist) but is too damaged, faint, or unclear in the photograph to classify |

**Primary-motif rule (precedence):**
1. If human figures are the principal actors of
   an apparent narrative or ritual composition →
   `HUMAN_CULT` (even if animals are present).
2. Else if the principal figure is a single
   mixed-anatomy creature → `COMPOSITE`.
3. Else the single dominant animal → its code.
4. Else, if two animals are coequal principals,
   the one occupying the centre/foreground.
5. `GEOMETRIC` only when the depiction is
   design alone; `SCRIPT_ONLY` only when no
   depiction is present; `ILLEGIBLE` when a
   depiction cannot be classified from the
   photograph. A seal's reverse/boss side is not
   a depiction: code from the inscribed face(s).

**Secondary motifs:** coders may list additional
depicted elements as further codes from the same
list (never entering the gate metrics).

The codebook contains no sign meanings and no
reading hypotheses (boundary 1). Any deviation
from this taxonomy in execution is named in the
pilot report, never silently adopted.

## 4. Protocol (frozen; §4.4 pattern)

- **Two independent blinded AI coders** (pass A,
  pass B), role-isolated instances, blind to each
  other, to Holdat `iconography`, to mayig motif
  labels, and to the catalogue's `motif_chapter`
  for sampled rows. Coder packets contain only:
  canonical key, image files, this codebook.
  Coders are instructed to consult nothing else —
  no catalogue, no compilation, no web.
- **Gold coder** (pass G): a third blinded coder
  codes the 20 gold objects only, under the same
  blindness.
- **Records:** one JSON record per object per
  pass, written to the pass's own directory in
  the local store: `{canonical_key, primary_motif,
  secondary_motifs, note, coder_role, batch}`.
  The `note` is a one-line visual description
  (what the coder saw), for the adjudicator.
- **Adjudication:** a separate third pass rules
  every A/B disagreement from the images plus
  both records, writing the adjudicated code and
  a ruling note per disagreement. Agreements
  stand as coded. The full disagreement log is
  preserved and published with the codes.
- **Effort:** measured from the on-disk record
  files' modification times within each batch
  (batch-start marker to first record = setup;
  successive record deltas = per-object effort).
  The method and its caveat are stated in the
  report. **All reported quantities are computed
  by script from the on-disk records — never
  from coder self-reports** (Phase-132 §4(d)
  process finding).
- **AI disclosure (constitution §VI):** all
  coding roles are executed by AI agents (Muse
  Spark, via Muse) in blinded role-isolated
  instances, at the direction of Tristen
  Pierson. Agreement numbers are properties of
  *this coding pipeline*, never of human expert
  coding. This disclosure appears in every
  artifact of the stage.

## 5. Metrics (definitions frozen)

All computed **pre-adjudication** on the full
100-object sample unless stated:

- **Exact agreement:** share of objects with
  pass A primary == pass B primary.
- **Cohen's κ:** unweighted, over the 12 frozen
  categories, on the same A/B pairs; both
  coders' category marginals published with it.
- **Per-category agreement:** per category,
  agreements ÷ objects coded that category by
  either coder (union), with per-coder counts.
- **Confusion structure:** counts of every
  (A code, B code) disagreement pair.
- **Adjudication rate:** disagreements ÷ 100.
- **Gold drift:** on the 20 gold objects —
  pairwise exact agreement A–B, A–G, B–G, and
  the three-way unanimity rate.
- **Effort:** per-object seconds per §4
  (median, mean, totals per pass).

## 6. Descriptive concordance (post-hoc; fenced)

After adjudication, and only as descriptive
concordance (never validation, never accuracy):
adjudicated primary vs the catalogue
`motif_chapter` family for sampled objects that
carry one — chapter families mapped as:
unicorn-family strings → `UNICORN`;
`tigerwithzebu` and section headers → recorded
as non-mappable and excluded from the count.
Holdat `iconography` is **not** compared (the
sample is keyed to CISI objects and the Holdat
join does not exist — Phase-131/133).

## 7. Gates (§4.5, verbatim effect)

- **Proceed gate:** exact agreement ≥ 85% **and**
  κ ≥ 0.75 → the motif arm is **eligible** for a
  Stage 2(b) design. Eligibility only: Stage 2(b)
  requires its own freeze and owner go. No
  association test runs in this phase.
- **Stop-rule:** exact agreement < 70% **or**
  κ < 0.50 → the motif arm **closes**; the pilot
  report states the failure plainly.
- **Middle band:** neither gate → the report
  presents the numbers and frames the owner's
  decision, without a recommendation dressed as
  a verdict. No silent middle path.

## 8. Fences

No association statistics of any kind. No anchor
changes, no PRED changes (boundary 1). Codes,
codebook, logs, and counts are publishable
facts; images and crops never leave the local
store and never enter git (boundary 5).
Dataset publication beyond the repo (Zenodo) is
**not** authorized by this freeze — the pilot
report frames it as an owner decision alongside
the gate verdict.
