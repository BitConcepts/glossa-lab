# Spec 062 — Adjudication (DRAFT, 2026-10-21)

> Draft adjudication for the successor spec to
> Spec 061, opened under the owner's
> amendment-queue commission of 2026-10-21
> (item 3). Sections 1–4 are the draft's own
> record: the verified failure, the decisions
> decided by this draft, the candidate repairs
> with their draft-level measurements, and the
> twice-derived acceptance tests. Section 5
> lists what only the freeze may decide, each
> item **OWNER-APPROVAL**. Nothing here
> freezes, files, or executes anything.

## 1. Inputs read at this draft

- Spec 061's frozen record in full:
  `specs/061-arm-a-precision/spec.md` (§4.7 +
  §5 in particular), `adjudication.md`
  (DD-061-1…DD-061-17, §6 on arm A2),
  `claims.json` (F061-C01…C15), `freeze.json`,
  and `outcome.md` (Phase-423, executed
  2026-10-21).
- Spec 028's frozen record:
  `specs/028-harappa-robustness/spec.md`,
  `pipeline393.py` (SHA-256 `6c2ff91c…`),
  `build_calibration.py`, `calibration.json`
  (SHA-256 `4198747b…`), `margins-audit.json`.
- The campaign plan approved AS WRITTEN on
  2026-10-21 (member 18, design D-27 arm A1;
  decisions E-1 and E-3).

## 2. The defect, verified (DEF-062-1 = DEFECT INHERITED FROM SPEC 061'S FREEZE)

- **DEF-062-1 — Spec 061's frozen calibration
  cannot impose either scenario's θ.** The
  frozen construction (DD-061-13 step 3)
  defines A(b) as the frozen estimator applied
  to the constructed population *in
  expectation*: every inscription at a site
  carries the same expected proportion vector
  p_s(b), so within-site variation is exactly
  zero, all variation the estimator sees is
  between sites, and its adjusted R² is 1.0 at
  any boost above 1. Recomputed on the pinned
  record at Phase-423: **A(1) =
  −0.0025188916876574316** (= 1 − 1592/1588,
  the frozen formula's null offset at
  n = 1,593, g = 5) and **A(1.5) = A(2) =
  A(3) = 1.0 exactly**. A takes no value
  between those, so no b in [1, 3] achieves
  |A(b) − θ| ≤ 1e-6 for θ₁ =
  0.00878393455594817 or θ₂ = 0.015, and
  Spec 061 closed **CANNOT BE RUN AS WRITTEN**
  at gate 0.5. Gates 0.1–0.4 passed; gate 0.3
  reproduced the recorded Arm A summary
  digit-for-digit. The precision question,
  the scenarios, the frame, and the trial
  machinery are intact; only the calibration
  definition is broken.
- The predecessor record names the mechanism
  and the repair direction itself (Spec 061
  `outcome.md` §3): Spec 028's recorded
  positive control at boost 3.0 (median
  adjusted R² 0.023963353007570576) "is a
  median over *generated* worlds, where each
  inscription's tokens are actually drawn
  from its site's composition, inscription by
  inscription. The drawing is what creates
  inside-a-site variation"; and "a calibration
  defined over generated worlds … is a
  different definition, and adopting one is an
  amendment act under a new planning gate —
  never a run-time substitution inside this
  frozen contract." This spec is that act, in
  successor form (DD-062-2).

## 3. Candidate repairs, derived on the record and measured at draft level

All four candidates share what is not in
dispute: DD-061-13 steps 1–2 (pooled
composition; imposed composition p_s(b) by
boosting the site's 10-sign positive-control
set and renormalising), the bracket [1, 3],
the bisection form (≤ 100 iterations,
|A(b) − θ| ≤ 1e-6), and the calibration level
of Spec 028's positive control — per draw, one
generated population over the full template,
then the frozen cell rarefaction (6 included
cells × 49 = 294 inscriptions), adjusted R²
per draw with permutations off, median over
199 draws. They differ only in how a draw's
population is generated around p_s(b).

**Draft-level demonstration.** Each candidate
was implemented in a scratch script on
synthetic/planted data and run before this
draft was written. Planted population:
the recorded Arm A margins (5 sites; totals
1,302 / 111 / 74 / 54 / 52; the recorded
10 site×type cell counts) with planted
composition parameters — 80 composition
columns (the 50 sign-set columns, 10 per site
and disjoint as on the record, plus 30 non-set
columns; the record has 125 sign columns), a
planted pooled composition p_k ∝ 1/(rank + 9)
over a seeded shuffle, and planted legible
lengths from [2…7] with stated probabilities
(mean 3.95; record cell means 3.88–4.96).
The estimator is the frozen `pipeline393`
machinery imported verbatim (pin
`6c2ff91c…`); the one computational shortcut
(a scipy cityblock distance for the
full-population probes) was verified against
`pipeline393.permanova` in-script (maximum
absolute difference 2.220446049250313e-16,
summation order only). Environment of the
demonstration runs: this drafting machine,
Python 3 with NumPy 1.26.4 / SciPy 1.11.4 —
not the execution environment of record;
the numbers below are draft-level planted
values, cited under claim F062-C15, never as
corpus quantities. W = 199 draws throughout
(the frozen replication count), except where
a probe states otherwise.

### R-1 (LEAD, adopted by this draft) — Per-inscription Dirichlet drawing around the imposed composition, fixed-uniform coupling

Defined in spec §4.7-R step 3-R in full.
Per draw and inscription, the proportion row
is a Dirichlet draw centred exactly on the
site's imposed composition p_s(b), with
concentration κ_i = n_legible(i) − 1 chosen
so the row's per-column variance equals the
frozen token drawing's multinomial proportion
variance p(1 − p)/n_legible(i). The draws are
coupled across b by fixed uniforms through
the gamma quantile function, so A_R(b) is a
deterministic continuous function of b
(spec §4.7-R step 3-R.4 gives the continuity
argument); the rarefaction selections are
likewise fixed before any b is evaluated.

Measured on the planted population (W = 199):

| b | A_R(b) |
|---|---|
| 1.00 | -8.586525414577828e-05 |
| 1.25 | 0.0007616440719377948 |
| 1.50 | 0.0025978807159117157 |
| 1.75 | 0.005509778833977075 |
| 2.00 | 0.008949443113814848 |
| 2.25 | 0.013018216729352106 |
| 2.50 | 0.01773222015474929 |
| 2.75 | 0.02241775248722533 |
| 3.00 | 0.027494277151578816 |

A_R is strictly increasing on this scan grid,
brackets both θ values, and bisection on
[1, 3] achieves the frozen tolerance for both
scenarios: **θ₁: b\* = 1.988037109375,
A_R(b\*) = 0.008783005998216353, |A_R(b\*) − θ₁| =
9.285577318163263e-07 ≤ 1e-6; θ₂: b\* = 2.3564453125,
A_R(b\*) = 0.015000831926602287, |A_R(b\*) − θ₂| =
8.319266022877025e-07 ≤ 1e-6.** Cross-check at the
record's comparison point: A_R(3) on planted
data sits beside the verbatim redraw's
planted value (R-2 below) and Spec 028's
recorded 0.023963353007570576 — three
constructions agreeing in magnitude at the
boost where the record reports one.

### R-2 — Verbatim redraw-per-b (Spec 028's positive-control manner, exactly)

Per draw, the population is regenerated by
the frozen `synthetic_entries` under p_s(b)
(integer token counts), then rarefied; A(b)
is the median over draws — the quantity Spec
028's calibration reports, and the definition
Spec 061's outcome record suggests by name.
Measured on the planted population it
calibrates in magnitude (independent stream,
W = 199: A(1) = -0.00035540152823854143, A(2) = 0.00675040337594357,
A(3) = 0.021062390433571387, the last beside the recorded
0.023963353007570576). Its defect is the
tolerance: as a function of b it is either a
Monte Carlo estimate re-drawn at each b
(noisy, not monotone — no bisection target
exists) or, coupled by common random numbers
(fixed token uniforms, inverse-CDF drawing,
fixed rarefaction selections), a deterministic
**step function**: tokens flip discretely as
b crosses thresholds. Measured with common
random numbers at b₀ = 2.0 (W = 199):
at b = 2.0 the coupled median is 0.006554746700947245; increasing b by 0.001 moves it by 2.1884743873989976e-05, by 0.01 moves it by 0.0005387360447398626, and by 0.05 moves it by 0.0007589132599372661 — and two independent streams for the same quantity at b = 2.0 differ by 0.000195656674996325 (0.00675040337594357 vs 0.006554746700947245) in any case. A step function whose jumps
near the root are of order 2.2e-05 to 7.6e-04 —
three orders of magnitude above the frozen
1e-6 tolerance — cannot promise
|A(b\*) − θ| ≤ 1e-6 in general. Adopting R-2
therefore requires the freeze to amend the
tolerance itself (a stated, record-derived
bound would be needed, e.g. ≤ 5e-4, still
inside Scenario 1's margin distance
0.00121606544405183 but consuming over 40% of
it) — a larger change to the frozen contract
than R-1, which meets the tolerance as
carried. **Not adopted by this draft;
preserved as the freeze's open alternative
(OP-062-4), adoptable only openly at the
freeze with its tolerance change recorded.**

### R-3 — Draw-then-tilt (multinomial draws under the pooled composition, drawn vectors tilted by b)

Worlds are drawn once under the pooled
composition by `synthetic_entries`; for boost
b, each drawn count vector's site sign-set
columns are multiplied by b; A(b) is the
rarefied median over draws. Continuous in b
(the tilt is continuous and the worlds are
fixed), but measured **too weak to calibrate**
on the planted population (W = 49 probe):
A(1) = −0.000104, A(2) = 0.001929, **A(3) =
0.004032** — it brackets neither θ. The
mechanism is visible: at a mean legible
length near 4, most inscriptions draw no
boosted sign at all, and tilting a realised
count vector cannot move them; the
construction's centre is also only
approximate (the tilt of a draw is not centred
on p_s(b)). **Rejected on measurement, not
on taste** — the draft's first lead, displaced
by its own probe; the probe is recorded here
so the rejection is checkable.

### R-4 — Dirichlet draw-then-tilt

As R-3 with continuous Dirichlet proportion
rows around the pooled composition, then
tilted. Measured at the full-population level
(W = 19 probe): A(1) = −0.000054, A(2) =
0.001026, A(3) = 0.002790 — weaker still, for
R-3's reasons. **Rejected on measurement.**
R-1 is this candidate's centre-exact repair:
draw around p_s(b) itself instead of drawing
around the pooled composition and tilting.

### Why R-1 and not a patch to the level or the tolerance

The frozen A failed for one reason only —
zero within-site variation — and R-1 is the
smallest change that repairs exactly that:
every other element of DD-061-13 (steps 1, 2,
4), of the frame (DD-061-9…DD-061-12), and of
the gate structure (0.1–0.4 verbatim; 0.5-R
verifying the same bracket, tolerance, and
iteration bound) is carried unchanged. R-1's
two genuine novelties are both derived, not
invented: the Dirichlet centre is the imposed
composition itself, and its concentration is
fixed by variance-matching to the record's own
token drawing (κ_i = n_legible(i) − 1). Its
known cost is stated in spec §8: calibration
rows are continuous proportions where trial
rows are token counts — same centre, same
per-column variance, different higher
moments.

## 4. Decisions decided by this draft (DECIDED-BY-DRAFT)

- **DD-062-1 — Successor, not amendment.**
  Spec 061's closed record is never patched;
  the repair is filed as this new successor
  spec (claim F062-C05). Ground: DEF-062-1
  and the executed-spec form (Spec 061's
  `outcome.md` §5: its frozen files are
  digest-covered and were not edited even by
  its own execution).
- **DD-062-2 — The precision question,
  scenarios, frame, gates 0.1–0.4, trial
  construction, resolution and target rules,
  outcomes, reporting, and limits are carried
  from Spec 061 verbatim in substance.**
  Only §4.7 step 3 (the calibration) and its
  gate (0.5-R) change. Ground: Spec 061's
  gates 0.1–0.4 passed and its gate 0.3
  reproduced the recorded distribution
  exactly; nothing else in the contract is
  implicated by the failure.
- **DD-062-3 — Gate 0.3 is preserved by
  construction, and the fencing argument is
  stated in the spec (§3, gate 0.3)**: the
  gate is a function of the §2 pins, the
  frozen machinery, seed 20261012, and
  R/B — none of which the repair touches —
  and the calibration consumes none of its
  inputs and shares no RNG stream with it.
- **DD-062-4 — Construction R-1 is the
  draft's calibration** (spec §4.7-R), on the
  §3 measurements: it is the only candidate
  that is centre-exact, within-site-varying,
  continuous in b, and able to meet the
  carried 1e-6 tolerance. R-2 is preserved as
  the freeze's alternative (OP-062-4); R-3
  and R-4 are rejected on measurement.
- **DD-062-5 — The calibration level is the
  positive control's level** (generated
  population → frozen rarefaction → median of
  draw statistics), removing the
  population-versus-cell weighting difference
  Spec 061 §8 recorded; the change and its
  reason are recorded in spec §8, not made
  silently.
- **DD-062-6 — Arm A2 discipline carried
  (E-3).** Arm A2 stays unarmed and outside
  this spec; Spec 061's T* stays undefined on
  Spec 061's record; a successor target, if
  one is ever returned, is this spec's own
  and arms nothing by itself (claim
  F062-C13).

## 5. OPEN for the freeze (each blocks the freeze until decided and recorded; each is OWNER-APPROVAL)

- **OP-062-1 — Calibration seed.** The draft
  carries the frozen seed value 20261021 on a
  dedicated calibration Generator (spec
  §4.7-R step 3-R.1), so no new constant
  enters silently and the trial streams keep
  DD-061-12's discipline untouched. The
  freeze may instead fix a fresh calibration
  seed — openly, in the freeze record.
- **OP-062-2 — Execution phase number.** Not
  allocated by this draft (Phase-423 was
  Spec 061's; the next number is the
  freeze's allocation, verified against the
  root LEDGER and the frozen specs' records
  as DD-061-16 verified 423).
- **OP-062-3 — OSF registration.** Whether
  this spec files its own OSF contract
  registration at its freeze, as Spec 061 did
  under campaign decision E-1 (DD-061-14).
  The filing act itself is OWNER-APPROVAL;
  no filing is made by this draft.
- **OP-062-4 — Construction choice.** Adopt
  R-1 as drafted, or adopt R-2 (verbatim
  redraw) openly together with the tolerance
  amendment R-2 requires (§3). Either is a
  freeze act; neither may be substituted at
  run time.
- **OP-062-5 — The freeze and execution
  acts.** The freeze of this spec, and any
  later execution order, are the owner's
  acts. **OWNER-APPROVAL** for each: freeze,
  OSF filing, execution.

## 6. Acceptance tests derived twice, independently — disagreements and resolutions

Per the campaign doctrine, each claim's
acceptance test was derived twice: once from
the claim text as written (**derivation A**),
and once independently from the underlying
requirement alone — Spec 061's frozen record,
Spec 028's frozen record, or the campaign
decisions — without consulting A's wording.

| Claim | Disagreement between the derivations | Resolution in this draft |
|---|---|---|
| F062-C05 | A filed the repair as an amendment document inside Spec 061's directory; B noted Spec 061's frozen files are digest-covered, its own execution edited none of them, and its outcome record prescribes "an amendment act under a new planning gate" for a different calibration definition. | B adopted — a successor spec (DD-062-1); Spec 061's directory is not touched by any act under this spec. |
| F062-C07 | A treated gate 0.3's preservation as automatic (the gate text is carried); B required the preservation to be *shown*: which inputs the gate depends on, and that the repair touches none of them and shares no stream with it. | B adopted — the fencing argument is stated in spec §3 at gate 0.3 and in the claim's boundary, as a checkable list, not an assertion. |
| F062-C12 (construction) | A led with draw-then-tilt (R-3: worlds drawn once, tilted continuously — the smallest code change from the frozen step 4); B led with the verbatim redraw (R-2: the quantity the record reports). The draft's own probes then displaced both: R-3 cannot bracket θ (A(3) = 0.004032, W = 49 probe) and R-2 cannot meet the carried tolerance (measured CRN steps, §3). | Neither original lead survives measurement. R-1 (Dirichlet-centred, fixed-uniform coupling) is adopted (DD-062-4) as the centre-exact continuous form of B's generated-worlds idea; R-2 is preserved as the freeze's alternative with its tolerance cost named (OP-062-4); R-3/R-4 rejections are recorded with their numbers. |
| F062-C12 (level) | A kept the frozen calibration's level (full-population estimator) for minimal change; B noted the only value the record reports for candidate (b) is the rarefied-draw median (0.023963353007570576 at b = 3), and that Spec 061 §8 already flags the level difference as a limit. | B adopted (DD-062-5): the calibration sits at the positive control's level; the level change is recorded in spec §8. |
| F062-C13 | A let a successor target arm A2 under DD-061-5's rule as carried; B derived from E-3 that arming is a mini-planning-gate act for the owner, and from Spec 061's outcome that T* on the old record is undefined permanently. | B adopted — the successor's operative target is defined by the carried rule, but arming A2 is reserved to the owner's mini planning gate (DD-062-6). |

All other claims (C01–C04, C06, C08–C11,
C14, C15): the two derivations agreed on the
operative check (inspection against the
stated boundary, an exact gate, or mechanical
recomputation from the published record), and
no disagreement is recorded because none
arose.

## 7. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest
   computed over the recovered register
   exactly once, at freeze), with every §2
   pin re-asserted against the merged record
   — or decline, leaving
   `STUDY-SPEC-028/ARM-A` INCONCLUSIVE with
   no computed intake target, Spec 061 closed
   as executed, and A2 unarmed on any number.
2. Decide OP-062-1…OP-062-4 (calibration seed;
   phase number; OSF; construction choice)
   and confirm or openly overturn
   DD-062-1…DD-062-6.
3. Note DEF-062-1 as the defect this spec
   exists to repair, and that the repair has
   been demonstrated at draft level on
   planted data only (§3; claim F062-C15).

**This does not establish:** the §3
demonstration establishes that construction
R-1 can calibrate on planted data. It
establishes nothing about the real corpus,
nothing about whether A_R brackets θ on the
recorded population (gate 0.5-R's
execution-time check), and nothing about the
precision question's answer.

---

*AI disclosure: drafted by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*

## 8. Freeze decisions — 2026-10-21

> ## FREEZE — 2026-10-21
>
> Recorded at the freeze act under the
> owner's approval of 2026-10-21 (amendment
> package Item 3: take Spec 062 through
> freeze and OSF filing). The AEE lifecycle
> hooks ran over the register first
> (recovered to 0.6-draft;
> `aee/freeze-aee-note.md`); the digest in
> `freeze.json` was computed exactly once
> over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). This section is append-only
> beside §§1–7, which stand unedited.

### 8.1 The composite pin — set verified complete at this freeze

- Every §2 component was re-derived at this
  freeze by two independent routes — the
  contents-API raw route and the git-blob
  route — both at `main`
  `b7a8c8a42d4e1137c04ef4c0123fb4ba4dbc3736`,
  with the merged working tree agreeing as a
  third read: results
  `0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607`
  (19,753 bytes), corpus layer
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`
  (1,204,144 bytes), pipeline
  `6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e`
  (15,127 bytes), margins audit
  `15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d`
  (5,355 bytes), Spec 028 freeze record
  `376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc`
  (4,212 bytes), calibration record
  `4198747b42121fea817db2e5ad82da10cca6118fef39bb14dc13cdf56ac204ff`
  (2,404 bytes), and anchors
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
  (570,344 bytes). The routes agree
  byte-for-byte on every file and every hash
  equals its §2 pin. The pin set is Spec
  061's, unchanged (DD-062-2): the repair
  touches no input, no machinery file, and
  no recorded summary.

### 8.2 The open items (OP-062-1…OP-062-5) — decided

- **DD-062-7 — Calibration seed (OP-062-1):
  20261021, as drafted.** The draft carries
  the frozen seed value 20261021 on the
  dedicated calibration Generator (spec
  §4.7-R step 3-R.1), and the drafting
  demonstration ran with it. The freeze
  adopts the drafted value exactly and fixes
  no fresh seed: no new constant enters, the
  trial streams keep DD-061-12's discipline
  untouched, and the calibration Generator
  remains a separate object from both
  per-scenario trial Generators, created
  before them and used for nothing else. The
  simulation seed of the carried frame is
  likewise 20261021 as carried.
- **DD-062-8 — Execution phase number
  (OP-062-2): Phase-424 is allocated to
  Spec 062's execution.** Verified at this
  freeze: Phase-423 was Spec 061's
  (DD-061-16); the frozen freeze records
  allocate Phase-419…Phase-423 to Specs
  057…061 in freeze order; a repository code
  search for "Phase-424" returns no record,
  the root LEDGER allocates no Phase-424,
  and no phase424 report, script, or graph
  module exists in the tree. Phase-424 is
  the first genuinely free number after
  423, and DD-062-2's predecessor rule
  (no phase number at draft; allocation is
  a freeze act) is discharged in this
  number.
- **DD-062-9 — Construction choice
  (OP-062-4): R-1 is adopted, exactly as
  drafted.** Per-inscription Dirichlet
  drawing around the imposed composition
  p_s(b), fixed-uniform coupling through the
  gamma quantile function, κ_i =
  n_legible(i) − 1 (spec §4.7-R). Ground:
  the §3 measurements — R-1 is the only
  construction demonstrated to meet the
  frozen 1e-6 bisection tolerance without
  amending it (planted data: θ₁ bisects to
  |A_R(b*) − θ₁| = 9.29e-07 in 12
  iterations; θ₂ to 8.32e-07 in 10), it is
  centre-exact, and it restores exactly the
  within-site variation whose absence broke
  Spec 061 (DEF-062-1). **R-2 (verbatim
  redraw-per-b) is NOT adopted**: it stays
  on the record in §3 as a non-adopted
  alternative, and the tolerance amendment
  it requires is not taken — its coupled
  calibration function is a step function
  with measured jumps of 2.2e-05 to 7.6e-04
  near the root, three orders of magnitude
  above the carried tolerance. **R-3 and
  R-4 stand rejected on measurement**
  (§3: neither brackets θ), as drafted. No
  construction may be substituted at run
  time: gate 0.5-R verifies the frozen R-1
  construction, per scenario, before any
  trial.
- **DD-062-10 — OSF registration (OP-062-3):
  yes.** This spec files its own OSF
  contract registration at the freeze,
  under campaign decision E-1, as Spec 061
  filed its own (DD-061-14). The filing
  record is `osf-spec-registration.md`,
  completed by append after the filing
  exists. Arm A2 needs none and none is
  filed for it — its test is already
  registered (osf.io/7m35w).
- **DD-062-11 — The freeze and execution
  acts (OP-062-5): the freeze is taken; the
  execution is not authorised.** The freeze
  act and the OSF filing act are taken
  under the owner's approval of 2026-10-21
  (amendment package Item 3). Execution
  (Phase-424) is a separate later act: it
  begins only after this freeze has merged,
  the OSF registration's approval act has
  completed, and a separate execution order
  is given. The draft's recommendation —
  that freeze, filing, and execution remain
  separate acts — is followed exactly.
- **DD-062-12 — The DD-038-10 AEE gate
  reading is adopted** (zero correctness
  failure modes and no claim below 0.70 =
  substantive pass; FR-2.3 draft-cap
  residuals at the draft/created lifecycle
  stage are structural, recorded openly in
  `aee/freeze-aee-note.md`, never edited
  away).

### 8.3 Draft decisions confirmed or standing

DD-062-1 (successor, not amendment),
DD-062-2 (carried substance verbatim except
§4.7 step 3 and gate 0.5-R), DD-062-3 (gate
0.3 preserved by construction, fencing
argument stated), DD-062-4 (R-1 the draft's
calibration — now the freeze's, DD-062-9),
DD-062-5 (calibration at the positive
control's level), and DD-062-6 (arm A2
discipline carried, E-3) all stand as
drafted; none is overturned. DEF-062-1 is
noted as the defect this spec exists to
repair, demonstrated repaired at draft
level on planted data only (§3; claim
F062-C15).

### 8.4 Register recovery at the freeze gate

The register was recovered from 0.5-draft to
0.6-draft at the freeze gate. Unlike Spec
061's register, the draft already carried
engine evidence values and mutual
independent_of declarations, so no
loadability round was needed: round 1 over
0.5-draft returned 22 failure modes — 15
FR-2.3 draft-cap records and 7
irreducibility challenges (recorded under
the engine's coverage_gap category) on
F062-C05, C07, C09, C11, C12, C13, and C15 —
with minimum propagated score 0.72. The 7
challenged heads were restated as single
propositions with their carried clauses
moved into boundaries verbatim-in-substance,
and the freeze rulings of this section were
carried into the boundaries of F062-C03,
C06, C07, and C12. Over the recovered
0.6-draft register every hook (after_specify,
after_plan, after_tasks) carries 15 failure
modes — 15 FR-2.3 draft-cap records, zero
correctness failure modes, minimum
propagated score 0.72, no claim below the
0.70 threshold. The full hook record is in
`aee/freeze-aee-note.md`. No claim's
falsifier, scenario value, or outcome
wording changed in recovery.

**This does not establish:** the freeze
establishes only that the repaired
construction is frozen as designed. The
planted-data demonstration proved
calibratability — continuity, bracketing,
and a b* at the frozen 1e-6 tolerance on
planted data — and nothing about the real
corpus. Gate 0.5-R on the recorded
population is an execution-time check that
has not run, and the precision question's
answer does not exist until an authorised
execution computes it.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
