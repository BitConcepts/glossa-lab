# Spec 093 — Plan

Stages in dependency order. Each stage names its
requirement, its behavior statement, and its acceptance
mode (test / gate / human-as-oracle) per the Autonomous
Execution Doctrine. The claims in `claims.md` are the
normative text; this plan is the order of work. **No stage
runs before the owner's block ratification of the package
(Stage 0), and no computation runs before its stage's
freeze.**

## Stage 0 — Ratification and adoption

- **Requirement**: the package, as ratified, is recorded;
  claims C093-1..14 are appended through the sanctioned
  intake as the spec's only adoption ledger diff; the spec
  directory receives its program-map assignment in the same
  landing, so the assignment gate the draft PR fails is
  discharged by the adoption itself.
- **Behavior**: the ratification act is recorded beside the
  package (the Spec 090 pattern); the bundle is generated
  from claims.md by script, assessed under the pinned AEE,
  and the gate runs before and after the append.
- **Acceptance**: gate.

## Stage 1 — Inventory completion, normalization, and the join

- **Requirement**: FR-093-01, FR-093-02, FR-093-09. The
  grounding inventory is completed against any source it
  missed (C093-2's amendment path), the `material` free
  text is normalized to a registered material-class
  vocabulary (rules filed, ambiguous and non-material
  values dispositioned by rule, never by eye at pass time),
  and the museum↔text join is designed, frozen, and
  precision-audited on a hand-checked sample (C093-9).
- **Behavior**: the stage produces three records — a
  completed census (the grounding record, amended),
  a normalization register (vocabulary + rules + the
  disposition counts), and a join record (procedure,
  sample, measured precision, error census). The
  artifact-typology and period-per-record absences are
  confirmed as register-bound gaps, not patched over with
  inference.
- **Acceptance**: test (each census count recomputable
  from the pinned files; the join audit's sample and
  precision stated and recomputable from the audit's own
  record).
- **Gate note**: Stage 2's field definitions consume this
  stage's vocabularies; Stage 4's material arm consumes
  this stage's join or records that it cannot.

## Stage 2 — The channel-independence administration

- **Requirement**: FR-093-03, FR-093-04. The material-
  context projection is defined formally against G1
  §2.1's state (the tuple per object, under Stage 1's
  vocabularies, over a named population), and C093-1 is
  administered: per field (D-093-3), a pre-registered
  prediction test — can the field be recovered from the
  object's sequence table plus bookkeeping features
  (source system, frame, derivation facts) at or above
  the frozen bar, on held-out objects, against permutation
  controls?
- **Behavior**: a freeze record precedes every computation
  (population, fields, features, bars, control behavior,
  floors); computations are Spec 089 runs; an auditor who
  did not compute recomputes; the outcome is recorded as
  C093-1's standing in spec.md §5's vocabulary, with the
  per-field table on its face.
- **Acceptance**: human-as-oracle (the stage reviewer
  against the freeze, the run records, and the bar).
- **Gate note**: this stage is the spec's gate. Stage 4
  does not start until the standing is recorded, and no
  Stage 4 statement may cite a field whose standing fell.

## Stage 3 — Comparanda register v1

- **Requirement**: FR-093-05, FR-093-06. The register is
  built as a versioned in-repo artifact: each entry names
  comparanda set, transmission mechanism (with its source),
  fixed window, and compared practice (C093-4). Seeding
  per D-093-7: the corpus catalogue's 39 corpora and the
  contact-zone records (the 14 excavated seals' find
  contexts; the Meluhha documentary record by period and
  provenience; the Gulf/Dilmun typology population).
- **Behavior**: entries are committed before any Stage 4
  comparison cites them; the register's amendment rule is
  C093-5's (supersession voids predecessor results in the
  same act). Wide-window entries state their continuity
  mechanism at span or are not entered.
- **Acceptance**: gate (a mechanical check that every
  entry carries the four required elements; a comparison
  citing a missing or postdated entry fails the stage
  record's own check).

## Stage 4 — First computed passes

- **Requirement**: FR-093-07, FR-093-08, and FR-093-02's
  population binding. Passes, in order:
  (a) **Site pass** — sequence behavior (length and
  sign-choice distributions, defined in the freeze)
  conditioned on site over the frozen population from the
  966, permutation controls within source strata, Harappa
  as the held-out replication arm where the freeze's
  floors allow; a design asking for more arms than the
  counts carry records CANNOT BE ADMINISTERED with the
  counts shown.
  (b) **Material pass** — the same conditioning on
  material class, only over the Stage 1 join's audited
  population and only if the join cleared its floor
  (D-093-4); otherwise CANNOT BE ADMINISTERED, recorded,
  and the front proceeds without it.
  (c) **Contact-context pass** — the 14 excavated seals and
  the Meluhha record treated as an evidence class under a
  Stage 3 register entry: what the find contexts do and do
  not license, stated as a bounded qualitative
  administration against the entry's frozen expectations,
  never as a population statistic (n=14).
- **Behavior**: each pass has its own freeze, its own runs,
  its own auditor; divergences junction under Spec 089;
  outcomes are ACCEPTED / NOT YET / CANNOT BE ADMINISTERED
  per pass, in §5's vocabulary, with C093-1's standing
  cited as premise on every accepted statement (C093-7).
- **Acceptance**: test (bars adjudged mechanically on the
  audited runs) with human-as-oracle on the outcome
  record's wording.

## Stage 5 — The projected-constraints extension build

- **Requirement**: FR-093-11. The matrix generator emits
  the material-context domain's rows from the ledger
  family; the program map gains its material-context
  layer (taxonomy domain + generated nodes) citing ledger
  ids; the ledger gate gains the checks that verify the
  culture layer's citations and one-way flow, in the
  standing gate profile's form (new checks counted, none
  weakened).
- **Behavior**: generated files are regenerated, never
  hand-edited (C093-11); the gate runs in both modes
  before and after; a culture-side statement that cannot
  cite a ledger id does not reach a surface.
- **Acceptance**: gate (the extended gate profile passing
  with the culture layer present, and a seeded-violation
  check: a culture-layer citation to a nonexistent ledger
  id fails the gate).

## Stage 6 — Culture-side gap register v1 and closeout

- **Requirement**: FR-093-12, C093-12, C093-14. GR-093
  entries are appended to the gap register under their
  own section (D-093-5), each carrying what is not known,
  a falsifier, an acceptance test, and an honesty type;
  the register's completeness checks are extended in the
  same landing to count the new section. The opening
  entries cover at least: the ductus/writing-style arm
  (no field exists), iconography (no coding exists),
  artifact typology beyond seal/unknown, period per
  record, the material join's residual coverage, and any
  gap a stage's outcome record named. The spec closes
  with its outcome record and the VEXA report.
- **Behavior**: the closeout states per stage what was
  administered, accepted, or stopped (with counts), what
  the channel's standing is, and what the register now
  carries — and nothing stronger.
- **Acceptance**: gate (register completeness with the
  new section counted; the outcome record's presence and
  vocabulary) + test (the recorded VEXA send matches the
  outcome record's words).
