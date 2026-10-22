# Spec 024 — Stage 1 Freeze Record 2 (Phase-135):
# Codebook Clarification + Re-Pilot Freeze

> ## FROZEN 2026-10-09 — clarification amendment
> ## and fresh-sample re-pilot
>
> Owner approval: Tristen Pierson, 2026-10-09 —
> "Run the combined path — clarify the boundary,
> re-pilot fresh, freeze Stage 2(b) only if the
> gates pass, publish the combined record."
> This record was committed **before the Phase-135
> frame was drawn and before any re-pilot image
> was viewed by any coder**. It amends the
> Stage 1 codebook of `stage1-freeze.md` in one
> respect only — the legibility boundary (§2) —
> and freezes the Phase-135 re-pilot (§4). The
> 12-code taxonomy, the primary-motif precedence
> rule, and every gate threshold of
> `stage1-freeze.md` are **unchanged** (§3).

## 1. Basis

Phase-134 (PR #111, merged `c4a3ef4c`) measured
exact primary-motif agreement **0.84** and
Cohen's κ **0.7885** on a fresh 100-object frame:
proceed gate NOT MET (agreement arm, one object
short of 0.85), stop rule NOT FIRED → **MIDDLE
BAND** under the frozen §4.5 rule
(`reports/phase134_pilot_report.md`). The
disagreement mass was concentrated on a single,
nameable boundary: **10 of the 16 disagreements
involve ILLEGIBLE on one side** — whether a
depiction is present and classifiable at all —
rather than animal identity among clearly
visible depictions. The owner directed the
combined path: clarify that boundary from the
pilot's own adjudicated record, re-pilot on a
fresh sample under identical gates, and freeze
a Stage 2(b) design only if the proceed gate is
met. This record executes the first step.

## 2. The clarification (boundary only)

The rules below define **only** the boundary
among `ILLEGIBLE`, `SCRIPT_ONLY`, and
`GEOMETRIC`, and the classifiability threshold
that separates a classifiable depiction from
`ILLEGIBLE`. They are distilled from the 16
adjudicated Phase-134 disagreements: in each
worked example the adjudicated outcome defines
the intended reading of the boundary, and the
adjudicator's ruling is quoted. No rule loosens
any code's definition; the frozen §4.3 visual
definitions stand as written.

### Rule B1 — Classifiability threshold

A depiction is classifiable only when at least
one **diagnostic feature** of a specific code is
discernible in the photograph: horn number or
shape, a shoulder hump, trunk or ear, skin-fold
bands, body build. A surviving animal fragment —
a head/neck corner, a truncated body section,
hindquarters alone — that carries **no**
discernible diagnostic feature is `ILLEGIBLE`,
however suggestive its outline.

Worked examples (adjudicated `ILLEGIBLE`):

- `cisi:v2:M-980` (A `ILLEGIBLE` / B `UNICORN`):
  "only a tiny corner of a head/neck with a
  curved line survives at the bottom edge, too
  fragmentary to distinguish a unicorn from
  another bovine."
- `cisi:v2:M-1208` (A `ILLEGIBLE` / B `UNICORN`):
  "Only a truncated horizontal body fragment with
  folded/striped detail survives at the lower
  edge … head, horn and legs are not discernible
  and the rest of the face is worn blank, so the
  animal cannot be classified."
- `cisi:v2:H-543` (A `ILLEGIBLE` / B `UNICORN`):
  "only the hindquarters, long tail and hind
  legs of an animal survive at the lower right,
  its head and forequarters are lost to the
  eroded area, so it cannot be classified."
- `cisi:v1:M-477` (A `ILLEGIBLE` / B `ELEPHANT`,
  gold `ILLEGIBLE`): "no trunk, ear, horn, hump
  or other species feature is discernible in the
  photo, so the animal cannot be classified as
  an elephant."

### Rule B2 — Eroded or broken depiction field

Where the object's composition reserves a
depiction field (e.g. the field below an
inscription row) and that field survives only
as a blank, eroded surface with faint traces —
or where a fragment of a depiction survives at
a break — a depiction may have existed but
cannot be classified: `ILLEGIBLE`, not
`SCRIPT_ONLY`.

Worked examples (adjudicated `ILLEGIBLE`):

- `cisi:v1:C-7` (A `ILLEGIBLE` / B `SCRIPT_ONLY`,
  gold `ILLEGIBLE`): "the large lower depiction
  field below it is blank and eroded with only
  faint traces, so a depiction may have existed
  there but cannot be classified from the
  photo."
- `cisi:v2:M-1164` (A `SCRIPT_ONLY` /
  B `ILLEGIBLE`, gold `ILLEGIBLE`): "at the
  broken bottom edge a truncated striped fringe
  of a depiction does survive; it is too
  fragmentary to classify, so the face is not
  script-only."

### Rule B3 — No depiction is not an illegible depiction

`ILLEGIBLE` requires positive evidence of a
depiction (Rule B1/B2). Surface erosion, wear,
or plain grooved surfaces — with no depiction
outline, no surviving depiction fragment, and
no reserved depiction field — mean **no
depiction is present**: code `SCRIPT_ONLY`
when inscription or marks are present.

Worked examples (adjudicated `SCRIPT_ONLY`):

- `cisi:v2:H-667` (A `ILLEGIBLE` /
  B `SCRIPT_ONLY`): "the bright worn area at
  one edge is surface erosion with no outline,
  legs, horn or other depiction discernible."
- `cisi:v2:H-852` (A `ILLEGIBLE` /
  B `SCRIPT_ONLY`): "no creature, human or
  depiction area is present on any face" —
  faces show only vertical script-like
  signs/strokes and plain grooved surfaces.
- `cisi:v2:Rhd-3` (A `SCRIPT_ONLY` /
  B `ILLEGIBLE`): "no depiction is present and
  there is no damaged depiction area to be
  illegible" — two plain pottery sherds, one
  short incised slit mark.

### Rule B4 — Script row vs geometric design

Marks arranged in a line as inscription
characters are **script** — including an
individual sign with internal geometry (a
spoked or cross-filled oval sign is a
character, not a design). `GEOMETRIC` requires
a deliberate geometric/linear **design** as the
sole marking, standing outside a script row. A
single short slit or stroke functioning as a
mark is not a geometric design.

Worked examples:

- `cisi:v2:M-1178` (A `GEOMETRIC` /
  B `SCRIPT_ONLY`, adjudicated `SCRIPT_ONLY`):
  "these are script characters in a line, not a
  geometric design" — a spoked oval sign flanked
  by curved and short-stroke signs.
- `cisi:v2:Rhd-56` (A `GEOMETRIC` /
  B `ILLEGIBLE`, adjudicated `GEOMETRIC`):
  "the sole marking is a geometric/linear
  design" — a small clearly incised zigzag; "no
  creature, human or script row, and no damaged
  depiction area."
- `cisi:v2:Rhd-3` (above, Rule B3): a single
  short incised slit mark was ruled a mark, not
  a design — the `SCRIPT_ONLY` side of this
  rule.

### Rule B5 — The positive side: when damage does not defeat classification

Cropping or damage does **not** make an object
`ILLEGIBLE` when a diagnostic feature remains
discernible. These adjudicated outcomes anchor
the positive side of the threshold; they apply
the frozen §4.3 definitions, they do not extend
them.

- `cisi:v1:M-573` (A `ZEBU` / B `UNICORN`,
  adjudicated `UNICORN`): "a single long horn
  is shown in profile, with collar/shoulder
  bands"; "back line is straight with no
  protruding shoulder hump" — horn number and
  back line discernible, so classifiable.
- `cisi:v1:M-254` (A `UNICORN` / B `BUFFALO`,
  adjudicated `UNICORN`): "a single large
  curved horn shown in profile; no hump and no
  pair of sideways-sweeping buffalo horns."
- `cisi:v1:C-15` (A `UNICORN` /
  B `GOAT_ANTELOPE`, adjudicated `UNICORN`):
  "bulky bovine body with stout legs in
  profile … the build is bovine, not a slender
  goat/antelope" — body build as the diagnostic
  feature.
- `cisi:v1:M-555` (A `RHINOCEROS` /
  B `BUFFALO`, gold `RHINOCEROS`, adjudicated
  `RHINOCEROS`): "distinct vertical skin-fold
  bands across the body and shoulder; no large
  curved buffalo horns or hump are shown."
- `cisi:v1:K-43` (A `GOAT_ANTELOPE` /
  B `COMPOSITE`, adjudicated `COMPOSITE`): "A
  single torso with four legs bears multiple
  horned heads on striped necks rising at
  different ends … it is one multi-headed
  figure, not two separate quadrupeds" —
  precedence rule 2 applied to one body, not
  two animals.

Application order for a coder facing the
boundary: (1) Is a depiction present, or a
depiction field/fragment surviving? If no →
`SCRIPT_ONLY` / `GEOMETRIC` per Rule B4. (2) If
yes, is a diagnostic feature discernible? If
no → `ILLEGIBLE` (Rules B1–B2). If yes → the
frozen §4.3 code for that feature, under the
frozen precedence rule (Rule B5).

## 3. Invariants (unchanged, restated so there is no ambiguity)

- The 12-code taxonomy and visual definitions
  of `stage1-freeze.md` §3: **unchanged**.
- The primary-motif precedence rule:
  **unchanged**.
- The gates of spec §4.5 / `stage1-freeze.md`
  §7: **unchanged by any amount** — proceed
  gate exact agreement ≥ 0.85 **and** κ ≥ 0.75;
  stop rule exact agreement < 0.70 **or**
  κ < 0.50; middle band otherwise.
- Metric definitions (`stage1-freeze.md` §5),
  record schema (§4), blindness (§4.4), the
  §6 descriptive concordance fence, and the §8
  fences: **unchanged**.
- The Phase-134 numbers stand as measured;
  nothing in this clarification revises them.

## 4. Phase-135 re-pilot (frozen values)

- **Population:** the frozen §4.2 eligible
  population of `stage1-freeze.md` §2 (3,245
  objects) **minus the 100 Phase-134 frame
  objects** → **3,145 objects**. The re-pilot
  sample is entirely fresh objects; the frame
  script asserts zero overlap with the
  Phase-134 frame and the report prints the
  check.
- **Canonical key, eligibility, site groups:**
  as `stage1-freeze.md` §2, unchanged.
- **Size:** exactly **100** objects.
- **Allocation:** proportional to the 9
  (site group × object type) cell populations
  of the reduced population by largest
  remainder, minimum 2 per non-empty cell,
  adjusted to total exactly 100. Cell
  populations and quotas are printed by the
  frame script into the frame record.
- **Selection:** within each cell, objects are
  ordered by `sha256("phase135-20261009|" +
  canonical_key)` ascending (hex) and the
  first `quota` are taken. Seed string:
  `phase135-20261009` (new phase salt; the only
  change to the draw rule).
- **Replacement rule:** as `stage1-freeze.md`
  §2, unchanged (pre-coding only, next in the
  same cell's hash order, logged).
- **Gold subset:** the drawn frame in the same
  hash order, indices 0, 5, 10, …, 95 → **20
  objects**, triple-coded.
- **Codebook as executed:** the frozen §4.3
  codebook **plus §2 of this record**. The
  worked examples of §2 are part of the
  codebook and are the **only** Phase-134
  material a coder may see; coders receive no
  other pilot-1 output (no pilot-1 codes, no
  metrics, no report).
- **Protocol:** two independent blinded AI
  coders (pass A, pass B), a blinded gold coder
  (20 objects), and a separate adjudicator for
  all disagreements — identical in every
  procedural respect to Phase-134, including
  batching (4 × 25 per main pass), packet
  contents (canonical keys + image paths only),
  record schema, effort measurement from
  record-file timestamps, and the rule that
  **all reported quantities are computed by
  script from the on-disk records, never from
  coder self-reports**.
- **AI disclosure (constitution §VI):** all
  coding roles are executed by AI agents
  (Muse Spark, via Muse) in
  blinded role-isolated instances, at the
  direction of Tristen Pierson. Agreement
  numbers are properties of *this coding
  pipeline*, never of human expert coding.
  This disclosure appears in every artifact of
  the phase.

## 5. Branch obligations (frozen by the owner's combined-path approval)

- **Proceed gate met** (agreement ≥ 0.85 and
  κ ≥ 0.75): the motif arm is eligible for
  Stage 2(b); a Stage 2(b) **design** is
  drafted and frozen under spec §5.3 / §5.1
  discipline (design only — execution requires
  a further owner go).
- **Stop rule fired** (agreement < 0.70 or
  κ < 0.50): the motif arm **closes**; the
  re-pilot report states the closure plainly
  and no Stage 2(b) design is drafted.
- **Middle band again:** no Stage 2(b) design;
  the re-pilot report presents both pilots'
  numbers side by side and frames the owner's
  decision without a recommendation dressed as
  a verdict.
- **All branches:** the combined motif-arm
  record (Phase-134 + this clarification +
  Phase-135, and the Stage 2(b) freeze or the
  closure / second-middle-band statement as
  applicable) is published as Zenodo v4.7.0
  through the mandatory release gate, per the
  owner's approval quoted above. Codes and
  logs only — no images, ever.
