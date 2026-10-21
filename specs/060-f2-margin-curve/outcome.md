# Spec 060 — Outcome Record (Phase-422)

> ## EXECUTED — 2026-10-21 — COMPOSITION DOES NOT (arm 2); margin curve published (arm 1, sensitivity)
>
> This record is the outcome record for Spec 060
> (design D-23), executed as Phase-422 under the
> runnable-experiments campaign approved by the
> owner AS WRITTEN on 2026-10-21 (Wave 3, Group 2:
> the independent executions). The frozen contract
> is `freeze.md` / `freeze.json` in this directory
> (freeze digest
> `8c04b1a8bf742d80ea6da41021fe569686a854cdecd1cb22f4b12f1c385be1a3`);
> its OSF registration **8ywxc** is APPROVED +
> PUBLIC (DOI 10.17605/OSF.IO/8YWXC), so the
> execution rule in the freeze record is satisfied.
> Base for the execution: `origin/main` at
> `3200b7b5b6841a7b9567a81368bf84004fd17255`.

## Headlines (spec §6, pre-written wordings)

**Arm 1 (§6.1, sensitivity display):** "Margin curve
for STUDY-SPEC-024/F2-HOLDAT (sensitivity display —
the recorded verdict at the declared margin 0.10
stands, CONTRADICTED, and is not moved by this
curve): governing basic-bootstrap interval
[0.058939204306206666, 0.0777941604081594], point V
0.11539837515155212, on the Holdat layer's
1,670-inscription analysis population, recomputed
under the Phase-384 v2 estimator. At margin 0.05:
SUPPORTED AT 0.05. At 0.075: STRADDLES 0.075. At
0.10: CONTRADICTED AT 0.10. At 0.125: CONTRADICTED
AT 0.125. At 0.15: CONTRADICTED AT 0.15."

**Arm 2 (§6.3, the falsifier):** "On the population
the two layers share — 6 sites (Chanhu-daro,
Dholavira, Harappa, Kalibangan, Lothal,
Mohenjo-daro), object type SEAL, 1516 Holdat
inscriptions and 2139 ICIT inscriptions — the
Holdat governing interval
[0.055251710457321024, 0.07607996659365032] and the
ICIT governing interval
[0.08368810617885544, 0.10835095759573735] still
exclude each other. Composition, in the form of
site and object-type mix, does not explain the
layer disagreement on this population. This
outcome stands **alongside** the finished record
of Spec 034 (design D-20, complete): on 169
matched objects — all Mohenjo-daro seals — the two
compilations' positional profiles agree (median
distance 0.025694; ATTRIBUTED TO COMPOSITION). Both
statements stand; neither edits the other. What
carries the remaining disagreement — the layers'
site-effect estimation, their sign treatment at
repertoire level, or selection beyond the matched
slice — is not adjudicated by this spec, and no
successor study is designed, registered, or implied
by this outcome; any successor enters through its
own planning gate. No verdict moves: F2 stands
CONTRADICTED at 0.10 and F3 stands SUPPORTED at
0.10, exactly as recorded."

The two governing intervals on the shared
population are separated by a gap of about 0.0076
(the ICIT lower bound 0.0837 against the Holdat
upper bound 0.0761); both point estimates and both
intervals are reported in full in §2 below, as
spec §10 requires, so a reader can see the sizes,
not just the word.

**No verdict moves under this spec: F2 stands
CONTRADICTED at the declared margin 0.10 and F3
stands SUPPORTED at the declared margin 0.10,
exactly as recorded.**

## 1. What was executed

The full frozen contract (spec §12 execution shape;
tasks E1–E6), under the graph-first build
(H15/H23): experiment script
`backend/scripts/phase422_f2_margin_curve.py`;
graph module
`backend/glossa_lab/experiment_graph_phase422.py`
(node `IndusPhase422F2MarginCurve`); registration
in `backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (node present in
`ATOMIC_NODES`). The run's own records:
`reports/phase422_results.json` (the machine
record) and `reports/phase422_report.md`.

Both arms were computed with the Phase-384 v2
estimator **unchanged** — its population builder,
bootstrap, and interval functions imported from
the pinned script itself (SHA-256 `3313394e…`),
never copied or re-implemented: inscription-level
bootstrap within site, site sizes fixed, B = 9,999,
seed 20261012, the basic bootstrap interval
governing. Gate 0.3 ran on one
`default_rng(20261012)` stream, F2 first then F3,
exactly as the Phase-384 v2 script runs them; arm
2's pair ran on a fresh `default_rng(20261012)`
stream, Holdat first then ICIT, mirroring that
order (recorded in the machine record). A second
full run of the script reproduced every quantity
byte-identically (the only difference between the
two runs' products was a margin-label formatting
correction in arm 1's cell words, made between the
runs; every number is identical across both runs).

## 2. The gates and the arms, in order, with observed values

- **Gate 0.1 — PASS. Input integrity.** Every
  spec §3 input hashes to its stated value,
  verified by two independent routes in the
  foreground (the script's hashlib route and
  `sha256sum`, with the git-blob route agreeing
  on the repository files): Phase-137 results
  `18f86f45…`; Phase-137 machinery `e00dacf4…`;
  Phase-384 results `dda6092d…`; Phase-384 v2
  estimator `3313394e…`; Phase-384 contract v2
  `f0a67bd7…`; Phase-384 freeze v2 `5749c6b8…`;
  Spec 034 outcome `c0cc615d…`; Spec 024
  specification `a817f698…`; anchors
  `df0cf620…`; and the two held layers at the
  Phase-137 loaders' default paths (DD-060-15):
  Holdat (`indus_corpus 2.csv`) `62d14d2b…`,
  ICIT lineage (`inscriptions.csv`) `c368f290…`
  — both exactly their Phase-137-recorded pins.
- **Gate 0.2 — PASS. Population reproduction,
  both layers.** The Phase-137 loaders and the
  frozen population rule reproduce each recorded
  profile table **exactly** (every cell): Holdat
  1,670 inscriptions, table 9 × 98, χ²
  745.9530278664301 recomputed against
  745.9530278664314 recorded, V
  0.11539837515155212 against 0.11539837515155221;
  ICIT 5,410 inscriptions, table 7 × 187, χ²
  4966.36222836514 against 4966.362228365138, V
  0.21900847512892316 against 0.2190084751289231
  (χ² and V within the Phase-384 v2 contract's
  own 1e-9 tolerances; the tables themselves are
  cell-for-cell identical).
- **Gate 0.3 — PASS. Estimator regression.** The
  Phase-384 v2 estimator, run unchanged on the
  two full-layer populations, reproduces the
  recorded governing intervals **exactly**, float
  for float, on every recorded field: F2 basic
  [0.058939204306206666, 0.0777941604081594],
  percentile [0.15300258989494483,
  0.17185754599689756], bootstrap median
  0.16180470665653984; F3 basic
  [0.18229651053139323, 0.21036863506165235],
  percentile [0.22764831519619397,
  0.2557204397264531], bootstrap median
  0.24066234010740262.
- **Gate 0.4 — PASS. Shared-population census.**
  The site intersection re-derived from the
  pinned layers is the recorded six sites:
  Chanhu-daro, Dholavira, Harappa, Kalibangan,
  Lothal, Mohenjo-daro. On the shared population
  (SEAL, DD-060-12: Holdat whole, ICIT restricted
  to its recorded SEAL class): **1,516 Holdat
  inscriptions and 2,139 ICIT inscriptions**,
  both far above the frozen floors (5 sites; 500
  inscriptions in either layer), so arm 2 ran.
  Per-site counts (Holdat / ICIT SEAL):
  Chanhu-daro 78 / 59; Dholavira 106 / 136;
  Harappa 492 / 440; Kalibangan 110 / 58; Lothal
  124 / 94; Mohenjo-daro 606 / 1,352.
- **Arm 1 — the margin curve (sensitivity).** In
  the headline above: the recomputed governing
  interval is the recorded interval itself (gate
  0.3), the point estimate V 0.1154, and the five
  cell words are SUPPORTED AT 0.05, STRADDLES
  0.075, CONTRADICTED AT 0.10, CONTRADICTED AT
  0.125, CONTRADICTED AT 0.15. The curve is
  labelled sensitivity in every product of this
  execution; no cell replaces the recorded
  verdict at 0.10.
- **Arm 2 — COMPOSITION DOES NOT.** On the
  shared population, under identical code, each
  layer in its own sign numbering (signs never
  pooled, mapped, or harmonised, F060-C14): the
  Holdat layer's governing interval is
  [0.055251710457321024, 0.07607996659365032],
  point V 0.11537928745216733, χ²
  422.9343117412524, table 6 × 94, on all 1,516
  census inscriptions (percentile interval
  [0.15467860831068433, 0.17550686444701363],
  bootstrap median 0.16435039413852193); the
  ICIT-lineage layer's governing interval is
  [0.08368810617885544, 0.10835095759573735],
  point V 0.13488340055820888, χ²
  803.9721678622018, table 6 × 118, on all 2,139
  census inscriptions (percentile interval
  [0.16141584352068042, 0.18607869493756232],
  bootstrap median 0.17281238758804135). The
  estimator populations are the census
  populations — no shared site dropped out
  under the estimator's frozen rule in either
  layer. The intervals still exclude each
  other: this is the falsifier's outcome, in
  the §6.3 wording of the headline, under the
  corrected D-20 hand-off (spec §2).
- **Period mix (F060-C13, DD-060-13).** For the
  Holdat layer: PERIOD MIX NOT DESCRIBED FOR
  THIS LAYER - FIELD NOT CARRIED. For the
  ICIT-lineage layer: PERIOD MIX NOT DESCRIBED
  FOR THIS LAYER - FIELD NOT CARRIED. No period
  assignment was imported from any other source,
  including any Spec 041-style assignment, and
  period is never treated as controlled under
  this spec.

## 3. What this outcome does and does not establish

Arm 1 establishes the shape of the settled F2
verdict as a function of the margin, on the grid
frozen in advance — nothing more: a cell word at
any margin other than the declared 0.10 is a
statement about that margin, never a verdict
(spec §9, limit 4). Arm 2 establishes that, on
the population the two layers share (six sites,
SEAL texts), the two layers' site effects still
exclude each other — so site mix and object-type
mix, in the form this design tests them, do not
explain the layer disagreement. **This does not
establish** that there is no site effect in the
Holdat layer; it does not establish which
compilation is right; it does not adjudicate
among the named candidate carriers of the
remaining disagreement (site-effect estimation,
sign treatment at repertoire level, selection
beyond Spec 034's matched slice); and it neither
widens nor narrows Spec 034's slice (169 matched
objects, all Mohenjo-daro seals), whose finished
attribution stands exactly as recorded alongside
this outcome. Restricting the ICIT layer to SEAL
texts and six sites changed that layer's mix (its
full-population governing interval [0.1823,
0.2104] moved to [0.0837, 0.1084] on the shared
population, its point V from 0.2190 to 0.1349),
while the Holdat layer's interval barely moved
([0.0589, 0.0778] to [0.0553, 0.0761]) — both
full-population intervals are on the record at
gate 0.3 beside the shared intervals, so the
restriction's effect on the inputs is visible,
not just its effect on the answer (spec §7).

## 4. Claim consequences (governed register)

One line per governed claim, F060-C01…C15.

- **F060-C01** (an outcome states only the two
  residue results): HELD — this record states
  the margin curve and the shared-population
  result only.
- **F060-C02** (F2-HOLDAT stands SETTLED —
  CONTRADICTED at 0.10): HELD — re-asserted
  exactly at gates 0.1–0.3; the verdict stands
  as recorded.
- **F060-C03** (the shared-population intervals
  overlap): NOT SUPPORTED — the intervals
  exclude each other; the outcome is COMPOSITION
  DOES NOT under F060-C12.
- **F060-C04** (a non-overlap outcome is recorded
  as COMPOSITION DOES NOT in the §6.3 wording,
  alongside Spec 034): HELD — the headline
  carries that wording, both-statements-stand
  and no-successor sentences included.
- **F060-C05** (design D-20 is complete): HELD —
  arm 2 was run and worded against Spec 034's
  finished record (pin re-asserted at gate 0.1);
  no pending D-20 appears anywhere in this
  execution's products.
- **F060-C06** (no verdict moves): HELD — the
  no-verdict-moves sentence appears in every
  product; Spec 024's, Phase-137's, and
  Phase-384's files are untouched (their pins
  re-asserted at gate 0.1 and unchanged).
- **F060-C07** (both arms computed with the
  Phase-384 v2 estimator unchanged): HELD — the
  estimator's own functions were imported from
  the pinned script; gate 0.3 is its exact
  reproduction check, and it passed float for
  float. No synthetic calibration was introduced
  (DD-060-14).
- **F060-C08** (arm 1 reports the curve on the
  fixed grid, labelled sensitivity): HELD —
  exactly the five grid margins, each word
  derivable from the published governing
  interval by the frozen rule, sensitivity label
  in every product.
- **F060-C09** (the shared population is
  constructed under the SEAL reading): HELD —
  the gate-0.4 census is derivable from the two
  analysis populations by that restriction alone
  (DD-060-12).
- **F060-C10** (TOO THIN closes arm 2 when the
  census fails its floors): NOT FIRED — the
  census passed its floors (6 sites; 1,516 /
  2,139 inscriptions), so arm 2 computed.
- **F060-C11** (execution stops before any arm
  quantity on a gate 0.1–0.3 failure): HELD in
  form — all three gates passed in order,
  before any arm quantity, and their verdicts
  precede the quantities in the machine record.
- **F060-C12** (arm 2's headline is assigned by
  §5.2's mapping alone): HELD — COMPOSITION DOES
  NOT is derivable from the two published
  governing intervals by the frozen definition
  (they exclude each other); no fourth or
  graded word was introduced.
- **F060-C13** (period mix described per layer
  insofar as the layer carries it): HELD — the
  frozen stated-unavailability wording stands
  for both layers (DD-060-13); nothing was
  imported and period is nowhere treated as
  controlled.
- **F060-C14** (each layer computed inside its
  own sign numbering): HELD — the only
  cross-layer operation in the run is the
  comparison of the two governing intervals.
- **F060-C15** (no outcome establishes that there
  is no site effect in Holdat, or which
  compilation is right): HELD — §3 of this
  record states those limits in the terms the
  claim requires.

## 5. Records

- Machine record: `reports/phase422_results.json`;
  report: `reports/phase422_report.md`.
- Graph node: `IndusPhase422F2MarginCurve`
  (registered and verified by import before the
  run).
- Dated append to `STUDY-SPEC-024/F2-HOLDAT`'s
  record (DD-060-1): the claim's frozen records
  (Spec 024, Phase-137, Phase-384) are never
  edited by this spec; the dated append for this
  execution is this outcome record and the root
  LEDGER entry, exactly as the executed-spec form
  (Specs 035–039, 044) records it.
- Root LEDGER entry: "Spec 060 executed
  (Phase-422)" entry added with this record.
- Foundation check (H21): run at the run tree
  before this record landed — **40 passed /
  0 failed / 8 warnings**, the standing figure.
  The regenerated report file is not landed
  with this record: regeneration in this
  worktree stamps the claims-store digest of
  the worktree's clean store copies
  (`7d4abb07…`) where the committed report
  carries the stamp of the tree it was
  generated in (`6743f1b0…`); the check's
  figures (40/0/8; anchors `df0cf620…`) are the
  same either way, the committed report passes
  its Phase J disk tests as it stands in this
  tree, and re-stamping it is outside this
  execution's scope.
- Anchors: asserted byte-identical before and
  after (`df0cf620…`, §2 gate 0.1).
- Local-environment disclosure: in this VM's
  existing glossa-lab venv, the freeze test
  `test_register_integrity` fails with a
  TypeError from the venv's AEE loader version
  (the conftest's `strict` keyword) — the same
  failure occurs in an untouched worktree at
  the same base, the register file is
  byte-identical to main and untouched by this
  execution, and the same class of local-only
  failure was disclosed on Spec 044's outcome
  record. The PR's CI run is the figure of
  record.
- CI and suite state at the record merge:
  *(completed by append in the landing record
  once the record PR's genuine CI run is read
  from its own job conclusions — the merge is
  made only on that run's genuine 7/7 green.)*

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
