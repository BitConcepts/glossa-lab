# Spec 064 / Phase-426 — Outcome record (EXECUTED 2026-10-22 — IDENTIFICATION FAILED, continuity/discrimination not sustained)

> ## EXECUTED — 2026-10-22
>
> Executed under the frozen Spec 064 contract
> (freeze digest
> `cfeb7baf71fad26e81ca80a08395c87a07d158974480923fd38eb2fed854c405`
> in `freeze.json`), as **Phase-426**, under the
> separate execution order for this spec (the
> DD-064-17 gate). The execution gate was
> satisfied before the run: OSF registration
> **s6hr9** is APPROVED + PUBLIC (approved and
> API-verified 2026-10-22: public, not pending,
> not withdrawn, reviews state accepted).
> Outcome: **IDENTIFICATION FAILED
> (continuity/discrimination not sustained)** —
> step 0 passed in full, step 1 named the
> source's list from the book's own apparatus,
> step D derived the drawn-form descriptor twice
> from the thesis plate and sustained the
> preserved reference, and step C — mandatory in
> this successor — was not sustained by either
> independent derivation, so the run closed
> under its pre-registered closure before step M
> and before any scoring. No list was scored, no
> statement about the sign is made, and nothing
> is fed to Asset A. The preserved reference's
> continuity status is **QUALIFIED** — anchored
> at family level only — and it is carried on
> this record as on every product of this run,
> never upgraded and never dropped.

## 1. What was executed

The frozen contract's execution shape (spec §12),
in order. Graph-first build (H15/H23): experiment
script `backend/scripts/phase426_concordance.py`;
graph module
`backend/glossa_lab/experiment_graph_phase426.py`
(node `IndusPhase426Sign297ConcordanceSuccessor`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The run's own records:
`reports/phase426_results.json` (SHA-256
`889e3435f5ff57c7610b6408bb6fa8ee75fe3441a75d1fdcd2d1cefcc279a758`)
and `reports/phase426_concordance_report.md`
(SHA-256
`99fa26e542e3e1915fe32d580523737c880ad9c1a1a3532945b530c04e93518f`).
The delivery of record:
`specs/064-sign297-concordance-successor/concordance-297.json`,
SHA-256
`9e765576349d4d294a4fc04f0d6750be3718dfc60fa267ea16c04c6130db7488`
(derived twice by independent routes — the
`sha256sum` tool and a Python `hashlib`
recomputation — with identical results; the script
is deterministic and a second run reproduced all
three output files byte-identically).

**Headline (spec §5.3 wording, IDENTIFICATION
FAILED form, with the §5.3 qualification sentence
appended as that section requires).** "The
fragment 'sign 297 is the horned tiger' cannot be
carried to a concordance: the descriptor's
discrimination of 297 from its neighbours in the
289–308 run was not sustained by both independent
derivations. The record stays a stated gap. No
statement about the sign is made, and nothing is
fed to Asset A. Qualification (carried from the
preserved reference, Spec 064 §1): the
identification of Wells's 297 rests on a
drawn-form reference whose continuity status is
QUALIFIED — anchored at family level only; its
step C discrimination check is part of this run's
record."

**The passage (spec §8, element 1), quoted with
its locator.** Wells (2015), printed p. 97 (held
cleaned text, lines 2938–2941):

> "Sign 532 and sign 297 are positioned in such a
> way as to resemble the position of the graphic
> element and several of their features are
> repeated in the image field. It is proposed here
> that sign 532 is a logograph for the
> anthropomorphic figure and that sign 297
> represents the horned tiger, or perhaps just
> ‘tiger’ generically."

**Fence sentence (spec §8, element 5).** "This
result settles what the published lists say the
drawn sign depicts. It is not evidence of what
the sign meant in use."

## 2. Step 0, gate by gate (all passed)

- **0.1 Input integrity — PASS.** Every spec §2
  input was recomputed at the run's base
  (`main` at `689a5499`) and each hash matches
  its frozen pin: claim record
  `997fa33699ccce3feecfe0d09f6e6a1dbd165c05cd9f255939ad96e84bc99031`;
  held cleaned text of Wells 2015
  `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e`;
  Phase-104 evaluation
  `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d`;
  crosswalk registry (803 rows)
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`;
  Phase-123 Wells segmentation witness (157 rows)
  `ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da`;
  lane-2 adopted drafts
  `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb`;
  Spec 046 closure delivery (standing unedited)
  `772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`;
  and the preserved drawn-form reference record
  `33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4`.
  The phase script re-verifies all eight pins
  fail-closed before any output is written.
- **0.2 Source producible — PASS.** The source
  book was produced from the program's held copy
  (the pin-verified cleaned text) and the §1
  passage was located in it verbatim (quoted
  above).
- **0.3 All four lists producible or citable —
  PASS.** Each list of record is accounted for
  with its citation and locator form, verified
  against the program's citation record
  (CITATIONS.md): **WELLS** — HELD (the held
  cleaned text itself; §A.7; locator chapter/
  figure plus the book's own sign number);
  **CISI** — HELD (Vols. 1–2, §§A.2–A.3; the
  Phase-124 catalogue layers: committed local-store
  manifest present); **PARPOLA** — CITABLE
  (*Deciphering the Indus Script*, 1994, §C.1;
  locator P-number; the registry is keyed to
  Parpola 1982 numbering); **MAHADEVAN** —
  CITABLE (*The Indus Script: Texts, Concordance
  and Tables*, MASI No. 77, 1977, §A.1; locator
  M-number plus concordance/tables page or entry;
  Mahadevan crosswalk data held in the pinned
  registry).
- **0.4 Reference producible — PASS.** The
  preserved reference record exists at its pinned
  digest (`33ee22ec…`, asserted at gate 0.1) with
  its continuity status QUALIFIED as frozen. The
  local thesis file (Wells 2006 PhD thesis, local
  research store only, not committed) was asserted
  against its §2 pin **before any plate was
  read**: SHA-256
  `4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e`,
  19,313,853 bytes — matching the pin exactly.
  The plate page it cites was then produced from
  that file: Figure 3.2, "The Indus signs by sign
  number", thesis p. 90 / PDF p. 102 (of 296 PDF
  pages), read by render at execution; its bottom
  row carries signs 295–308 with 297 the third
  entry, exactly as the reference record states.
  No image is committed anywhere in this run; the
  plate reads below are text records of that
  inspection.

## 3. Step 1 — identification

**1.1 The source's sign list, named from the
document — NAMED.** The passage names no list at
the passage itself; the book's apparatus names
it: "Chapter 2 gives the Indus sign list used in
this analysis"; "The sign list used here (Wells
2011)"; Chapter 2 is "The Indus Sign List" and
its Figure 2.6 is "An Indus Sign List". The
numbering of the passage is Wells's own — Wells
2011, as given in Wells 2015, Chapter 2 /
Figure 2.6 — exactly the list of record fixed at
the freeze (DD-046-10, carried by DD-064-18).

**Step D — the descriptor, derived twice.** Two
independent derivations from the thesis plate
(Figure 3.2, thesis p. 90 / PDF p. 102), each
recorded from the plate before comparison with
the preserved descriptor. (The executor had read
the frozen spec in full, as the execution order
requires; the sheets were recorded feature-first
from the plate renders, and their divergences
from the preserved wording — recorded openly in
the comparison below — are the evidence the
wording was checked, not inherited.)

*Derivation A* (first plate read: full-page
render of PDF p. 102 at 300 dpi, read in page
context). Plate locator: Figure 3.2, thesis
p. 90 / PDF p. 102; bottom row, signs 295–308;
297 the third entry. Features read for 297: a
bundle of long parallel strokes; bent once, at a
single bend whose point is at the left; the
upper portions slant steeply down to the left;
the lower portions run down from the bend and
splay slightly apart at the base; stroke count
read as four at the base, three clear above the
bend. Neighbour set discriminated against: the
plates' bent-ray run, signs 289–308 — the upper
row (289–294) are compact chevron forms with no
long lower run; in the bottom row, 295 carries a
single broad upper stroke, 296 and 304 keep
their upper portions near-vertical, and 307 and
308 carry a looped head; 299, 300, 301, 302,
303, 305 and 306 are the same bent bundle in
differing widths and counts.

*Derivation B* (second plate read: independent
re-render of PDF p. 102; per-sign cell crops at
600–700 dpi; stroke counts at the top edge and
at the base of each glyph). Plate locator as A.
Features read for 297: three distinct strokes
above the bend; four distinct stroke ends at the
base; a single sharp bend, point at the left, at
about 55–60% of the glyph height; upper portions
slant about 50 degrees from vertical, down to
the left; lower portions slant about 30 degrees
from vertical, down to the right — more vertical
than the uppers, not strictly near-vertical;
moderate basal splay. Neighbour counts read:
295 — 1 above / 4 at base, single broad upper
stroke; 296 — 3/4, uppers near-vertical, bend
shallow; 299 — 2–3 above / 4 at base, same steep
slant, same sharp bend, same basal splay as 297;
300 — 2–3/4, bundle narrower, bend shallower;
301 — 2/4, small narrow bundle; 302 — 3/4–5,
same steep slant, sharp bend and splay as 297;
303 — 3/4, same as 297; 304 — 3/4, uppers
near-vertical; 305 — 4/4, uppers more vertical,
chevron-like; 306 — 3–4/5, uppers more vertical;
307, 308 — looped head, 2–3 strokes; 289–294 —
compact chevron forms, lower runs markedly
shorter than 297's long lower run.

*Reconciliation.* The two derivations agree on
every feature: family (a parallel bent bundle),
the single sharp bend, the steep upper slant
down-left, the lower run with basal splay, and
the counts within reading tolerance (three clear
above the bend, four at the base). No unsettled
disagreement arose. Reconciled descriptor: "A
bundle of long parallel strokes bent once at a
single sharp bend — three strokes clear above
the bend and four stroke ends at the base: the
upper portions slant steeply down to the left;
below the bend the strokes run down to the
right, more vertical than the uppers, splaying
at the base. A member of the thesis plates'
bent-ray run (signs 289–308)."

*Comparison with the preserved descriptor —
AGREEMENT; the reference is sustained.* Both
derivations confirm the preserved descriptor's
feature set. Two noted readings loosen its
wording without changing any feature it asserts:
(1) its "four" strokes is the count at the base —
three are clear above the bend, where the
innermost strokes merge in the scan; (2) its
"near-vertical" lower portions read on the plate
as slanting down to the right at about 30 degrees
from vertical — more vertical than the uppers,
not strictly vertical. These are judged **not
material**: the preserved record itself carries
discrimination, not description, as the open
step (its recorded limitation), so the run does
not close as IDENTIFICATION FAILED (reference
not sustained); it proceeds to step C.

**Step C — continuity / discrimination
(MANDATORY) — NOT SUSTAINED.** The run states,
from the record, what anchors the plate number
to the 2011/2015 numbering: the family anchor —
registry row P205 ("Prismed light rays, with
opposite slanting on top vs bottom, more rays on
bottom"), whose `wells_ids` cell groups
W289–W306 as one Parpola sign's Wells
counterparts — carried at its frozen status:
**corroboration only, expressly NOT an
identification**. It corroborates that the 2015
list's 289–306 numbers belong to the bent-ray
family the plate shows, and nothing more. No
record the program holds anchors the number 297
individually from the 2015 side. Each derivation
was then required to affirm that the reconciled
descriptor picks out the plate's 297 and no
neighbour in the 289–308 run. **Neither
affirms it:**

- Derivation A: "I cannot affirm that the
  descriptor picks out plate 297 and no
  neighbour. Signs 299, 302 and 303 present the
  same feature set — a parallel bundle bent once,
  uppers slanting steeply down-left, lowers
  running down from the bend with a basal splay —
  and nothing in the features I read separates
  297 from them. What fixes 297 on the plate is
  its printed position and number, which is the
  number-only reading the protocol names as a
  trap when it is used without this check."
- Derivation B: "I cannot affirm the
  discrimination. Counted feature by feature,
  signs 299, 302 and 303 match 297 on every
  feature the descriptor states (parallel bundle,
  single bend, steep upper slant, lower run with
  basal splay, four stroke ends at the base);
  300, 301, 305 and 306 differ only in degree
  (width, bend sharpness, slant) on features the
  descriptor does not quantify. The descriptor
  fixes the family and 297's place in the run; it
  does not pick out 297 alone."

The execution therefore closes at step C under
the frozen, pre-registered class
**IDENTIFICATION FAILED (continuity/discrimination
not sustained)**, with the §5.3 wording at §1
above. The preserved reference's continuity
status remains **QUALIFIED**, exactly as its
record states; this run does not upgrade it, and
Spec 064's own §10 named this the successor's
soft step, checked here with its failure closure
pre-registered.

**Step M — not reached.** No route was
attempted and no match is recorded. The frozen
routes stand untested by this run: Route 1
(registry, by drawn form) and Route 2 (the
preserved reference cited as the source list's
own entry). For the record, the registry and
witness facts were recomputed at the run: the
pinned registry's only `W297` value sits inside
the 17-value `wells_ids` cell on the P205 row
(not a singleton; the family anchor, not an
identification); P297 is the "Ladder motif" with
`wells_ids` empty; no registry description names
a tiger (0 of 803); the Phase-123 witness
carries no grapheme 297, and its M297 row's
Wells grapheme is 924. The traps are asserted as
traps in the run's record, in full: P205's
`wells_ids` cell used as an identification; P297
"Ladder motif"; witness M297 (Wells grapheme
924); P205's Mahadevan crosswalk M180 used as
W297's identity; and any number-only match,
including a plate number read without step C.
No number-match was used or attempted at any
point (F064-C07).

## 4. Step 2 — scoring (not reached)

No list was opened for scoring, no row exists,
no concurrence state was computed, and the
§5.2 mapping was not engaged. The delivery
carries the frozen closure form instead of rows
(spec §6): `signs` is an empty array and the top
level carries `closure: {class, wording}`. An
empty feed is a stated state, never an absent
file: **nothing is fed to Asset A**. Spec 046's
closure already satisfied Asset A's timing rule
in closure form; Asset A proceeds on the record
it already has and records this successor's
closure, per spec §8 — the asset may not
reconstruct any feed from its own labels.

## 5. What this outcome does and does not establish

It establishes that the preserved drawn-form
reference survives its step D check — two
independent derivations from the thesis plate
confirm its descriptor's feature set — and that
its continuity does not survive step C: the
descriptor fixes the bent-ray family and 297's
place in the run, but it does not discriminate
297 from its nearest neighbours (299, 302, 303),
so the drawn sign is not identified under this
contract and the concordance question cannot be
carried to scoring. The identification of
Wells's 297 rests on a drawn-form reference
whose continuity status is **QUALIFIED** —
anchored at family level only; its step C
discrimination check is part of this run's
record. It does **not** establish anything about
the sign itself: not that Wells's identification
is wrong, not that any list disagrees with it,
not that the plate's 297 is some other sign, and
nothing about what the sign meant in use (spec
§9). The hypothesis of §1.2 was neither supported
nor falsified on concurrence grounds — no list
was scored, so the falsifier's concurrence test
never ran; what fired is the mandatory
continuity/discrimination gate in front of it.
What would remove the qualification stands as
the reference record states it: a descriptor
derived from the published Wells 2015 artefact
itself (an owner-approved acquisition), or a
published drawn-form cross-match for this sign
entering the program's holds. The record stays a
stated gap.

## 6. Claim consequences (governed register)

Executed under register 0.7-draft (frozen); one
line per claim, F064-C01…C15.

- **F064-C01** (an outcome states only published-
  list concurrence on this sign's identification):
  HELD — the outcome states no concurrence and
  nothing about the sign; it records a continuity/
  discrimination gap only, at the identification
  layer.
- **F064-C02** (the record under test is this
  fragment): CHECKED — the claim record was read
  and pin-verified at gate 0.1; its verbatim
  wording, UNTESTED status, and Phase-104
  RULE-NUM stop are as the frozen record states.
- **F064-C03** (the identification is the
  published consensus): NOT REACHED — no list was
  scored; the hypothesis is unjudged, neither
  supported nor falsified on concurrence grounds.
- **F064-C04** (a non-concurrence outcome is
  recorded with CONSENSUS-level prominence):
  NOT REACHED in its scoring sense — no
  non-concurrence outcome arose; the closure is
  recorded with the same prominence (§9.6 of the
  spec: closures publish with the same prominence).
- **F064-C05** (execution closes at step 0 on a
  step-0 gate failure): HELD — the gates ran in
  the frozen order (0.1–0.4) before any
  identification work; all passed, so no step-0
  closure arose.
- **F064-C06** (step 1 identifies the drawn sign
  by drawn form, through the preserved reference
  and the frozen protocol): FIRED — step 1 named
  the list from the apparatus, step D sustained
  the preserved reference, and the execution
  closed as IDENTIFICATION FAILED
  (continuity/discrimination not sustained) at
  step C, with the reason named, exactly as this
  claim's boundary and DD-064-11 pre-register.
- **F064-C07** (cross-list matching is by drawn
  sign; numbers are not identities): HELD — no
  number-match was used or attempted; all five
  frozen traps (including witness M297 →
  grapheme 924, M180 as W297's identity, and a
  plate number read without step C) were asserted
  as traps in the run's record, and the run
  refused to let the plate's printed number do
  the descriptor's work.
- **F064-C08** (Wells scores as SOURCE, never
  toward CONSENSUS): NOT REACHED — no rows were
  scored, so the counting rule was not engaged.
- **F064-C09** (each row carries one scored state
  from AGREE / DISAGREE / SILENT): NOT REACHED —
  no rows exist.
- **F064-C10** (the concurrence state comes from
  the §5.2 mapping over the four rows): NOT
  REACHED — no rows, no state computed.
- **F064-C11** (the delivery is
  `concordance-297.json` in this spec's
  directory, in the §6 form, produced on every
  terminal outcome): HELD — the file was produced
  in this spec's directory in the closure form
  (empty `signs`, `closure` block, producer_spec
  064), digest recorded in §1; Spec 046's closure
  delivery in its own directory is unedited
  (asserted at gate 0.1 and again at §7 below).
- **F064-C12** (the concordance draws solely on
  published-list sources; no Asset A material,
  labels, or positional results): HELD — the run
  consulted only the §2 pinned set, the citation
  record, the crosswalk registry as matching
  instrument, the Phase-123 witness, and the
  preserved reference; no Asset A material,
  depicted-kind label, or positional result was
  consulted at any point.
- **F064-C13** (every outcome product carries the
  §8 reporting elements): HELD in the closure
  form the claim's own boundary prescribes — the
  passage quoted with its locator (§1), the
  closure wording and closure block in place of
  rows the run does not have, the gate-0.3
  accounting for all four lists (§2), the
  delivery exactly as delivered (§4), the fence
  sentence (§1), and the successor's
  identification record (§3): the reference's
  digest, both step D derivation sheets and their
  reconciliation, the step C statement with the
  family anchor at its frozen status, the step M
  routes recorded as not reached with the traps
  asserted, and the reference's QUALIFIED
  continuity status stated wherever this record
  states the run's result.
- **F064-C14** (an outcome establishes
  identification-layer agreement only): HELD —
  no statement beyond the identification layer
  is made; no generalisation from this one sign,
  and no reading of any inscription.
- **F064-C15** (Spec 046's records stand
  unedited; this successor's outcome is recorded
  by dated appends): HELD — the append was made
  to the claim
  `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`'s
  record as a new `spec064_check` entry
  (Phase-426, 2026-10-22, the §5.3 wording with
  its qualification sentence, the delivery
  digest), beside Spec 046's `first_check` entry,
  which is unedited; verification at the act:
  removing the appended segment (2,669 bytes;
  segment SHA-256
  `fc973395394d87fd43c9ff31f0929c093424b79b298f27459c66660d170e9fcf`)
  reproduces the pre-act file byte-identically,
  and the claim's status and stage are unchanged.
  Spec 046's frozen record, outcome, and closure
  delivery were not modified by any act in this
  run. The Phase-104 evaluation and the lane-2
  adopted explanation were not edited.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 7. Records

- Delivery: `specs/064-sign297-concordance-successor/concordance-297.json`
  (SHA-256 in §1); results record:
  `reports/phase426_results.json`; report:
  `reports/phase426_concordance_report.md`.
- Claim successor-check append: `spec064_check`
  entry on the claim's record (see F064-C15
  above), in the Spec 038 append form; tests
  assert the regeneration-preserved facts only
  (the fragment's status and stage, the unedited
  Spec 046 first check beside it, and the
  append's own facts against the delivery).
- Root LEDGER entry: "Spec 064 (Phase-426)" entry
  added with this record.
- Handover to Spec 045: the empty-feed closure
  state is the delivery; Asset A proceeds on the
  record it already has (Spec 046's closure) and
  records this successor's closure — no other
  handover artefact exists, by design.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges, in the Spec 039 completion pattern —
  this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
