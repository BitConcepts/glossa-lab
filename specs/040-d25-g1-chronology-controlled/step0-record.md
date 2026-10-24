# Spec 040 — Step-0 record (Phase-439 execution)

Execution act under the frozen contract (freeze
digest
`16aeeb7017f34f079742e56f13bfd88e3955ce75722693eae87fbbbaa9927515`;
OSF registration `2rgtb`, approved and public at
this run). Executed 2026-10-24 under the owner's
execution order of 2026-10-24 (19:04 EDT), at
the execution venue (program VM). Execution
base: `1978a4a6` (main at the order: PR #367
merged).

**Venue note, recorded plainly.** The fresh git
worktree off origin/main created for this run
was reaped by the VM write restriction mid-run
(the checked-out tree vanished, as standalone
clones had earlier in the day; the host
repository and older trees were unaffected).
The run therefore executed in a minimal tree
assembled from origin/main through the GitHub
API, holding only the run's inputs at their
repo-relative paths — every input hash-verified
at gate 1 below before any use, so the
substitution of venue machinery changed no
input and no rule. The record was landed on
the repository through the git-data API for
the same reason. The phase script's own venue
line in the machine record states this.

**Verdict: STEP 0 PASSED — all three gates, in
order, fail-closed.** The margins gate then ran
and FAILED on arms 1 and 2 (arm 3 passed); the
execution closes **NOT-YET-TESTABLE** under
spec §5 / DD-040-5. No repertoire quantity was
computed.

## Gates (in order)

- **Gate 1 — pin verification (tasks E2):
  PASS.** Every freeze §3 pin recomputed at
  execution against origin/main content:
  Spec 041 artifact
  `1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67`
  ✓; its meta `bda1017d…` ✓; Spec 041 step-0
  census `b57fb6b1…` ✓; Spec 039 artifact
  `64f288d3…` ✓; Phase-139 covariates
  `a0f0d05a…` ✓; chronology spine `9dc2fba5…`
  ✓; anchors `df0cf620…` ✓. The recorded
  freeze digests stand (Spec 039 `ec53a841…`;
  Spec 041 `fe618886…`), and the Spec 040
  freeze record replays exactly
  (framework026 `verify_freeze` over every
  covered source: no problems; digest
  `16aeeb70…`). The ICIT-lineage layer
  (horus84 `inscriptions.csv`) was asserted at
  its pin `c368f290…` (1,190,884 bytes) before
  any use, from the venue's held copy — itself
  re-acquired earlier the same day from the
  layer's pinned source
  (horus84/Computational_Linguistics at
  `ac44f08c`, the pattern of Spec 041's gate
  G0.1) after the sweep's local copy proved
  absent and the main checkout's downloads copy
  hashed to a different file (`c22d39c3…`, not
  the layer of record; not used). The pin, not
  the provenance path, is what this gate
  governs, and it held exactly.
- **Gate 2 — population reproduction and the
  §4.1 join under A1 (tasks E2): PASS.** The
  Phase-137 population reproduces exactly from
  the pinned covariates: 5,410 rows, IDs
  unique, by site Chanhu-daro 74, Dholavira
  238, Harappa 2,717, Kalibangan 212, Lothal
  208, Mohenjo-daro 1,923, Nausharo 38. The
  covariates agree with the layer on every
  population row under the Phase-139 value
  convention (site equal; period/phase equal
  after stripping, a value unrecorded iff the
  stripped form is `""` or `"-"`): 5,410 rows
  checked, 0 mismatches. The label margins
  reproduce exactly (period 2,266; phase
  2,638; both 1,788; union 3,116; neither
  2,294), and the census built from the
  covariates equals the artifact's 78
  (site, field, local label) triples exactly,
  every `attested_rows` equal. The §4.1 join
  under derivation A1 yields exactly one
  assignment row for each of the 5,410
  population inscription IDs — no missing ID,
  duplicate, extra row, or site mismatch — and
  reproduces the freeze §3 counts exactly:
  **1,457 placed** (EARLY 32, MATURE 1,386,
  LATE 39); 3,953 unplaced (2,294 no
  informative label; 1,658 all labels
  UNASSIGNED; 1 disagreement, unplaced).
  Placed by site: Dholavira 133, Harappa
  1,021, Kalibangan 157, Lothal 108, Nausharo
  38, Mohenjo-daro 0, Chanhu-daro 0.
- **Gate 3 — determinism: PASS.** The step-0 +
  margins computation was run twice from the
  pinned inputs inside the execution, and the
  two canonical records are identical. The
  phase script was then run twice more at the
  venue; both runs produced
  `reports/phase439_results.json` at SHA-256
  `bccb59c4db388d12fb7f8ac2c56ca0d4b119d8cf2dae8f8ad053e7fe7765b0f1`,
  byte-identical.

## The margins gate (spec §5, tasks E3)

Margins only — no profile table, no
permutation, no interval:

- Assigned 1,457 of 5,410 (26.9%); unassigned
  3,953 (73.1%): no informative label 2,294;
  all labels UNASSIGNED 1,658; 1 disagreement
  left unplaced; contested-excluded 0 (the
  accepted artifact carries zero CONTESTED
  cells; §8.1 stands NOT APPLICABLE).
- Assigned by period: EARLY 32, MATURE 1,386,
  LATE 39.
- Distinct sites with ≥ 1 assigned inscription:
  EARLY 1 (Harappa); MATURE 5 (Dholavira,
  Harappa, Kalibangan, Lothal, Nausharo); LATE
  2 (Dholavira, Lothal).
- Permutable inscriptions under the §6 primary
  strata (composition × preservation ×
  period): 1,205, in 36 of 65 strata holding
  ≥ 2 distinct sites.
- **Arm 1 — FAIL.** EARLY retains 1 distinct
  site and LATE 2, against the required 5
  (MATURE retains 5).
- **Arm 2 — FAIL.** The unassigned share is
  73.1% of the population, against the ≤ 40%
  arm.
- **Arm 3 — PASS.** Permutable inscriptions
  number 1,205, against the ≥ 1,000 arm
  (DD-040-6, retained).

The gate requires all three arms; the
execution therefore closes **NOT-YET-TESTABLE**
(DD-040-5) at the margins gate. The §7
comparability regression (tasks E4) and the
§6 primary (tasks E5) and §8 sensitivities
(tasks E6) were NOT REACHED — spec §13 places
the regression and the primary after the
margins gate, and §5 forbids computing any
outcome quantity past a failed gate. The
freeze record's §4 forecast — this closure,
on these arms — is what the recomputed
margins in fact produced; the margins were
recomputed from the pinned inputs at this
run, not carried from the freeze.

## Anchors

`backend/reports/INDUS_FINAL_ANCHORS.json`
asserted byte-identical before and after the
run: SHA-256 `df0cf620…` at both readings. No
anchor moved; no PRED contact.

## What this step-0 record is

The dependency settlement the freeze recorded
is re-verified, the join the freeze verified
is re-run for outcome purposes, and the
margins the design's gate governs are measured
on the pinned inputs — and the gate closes the
design, exactly as its text provides. This is
a statement about the assignment the published
record supports, not a verdict on G1:
`STUDY-SPEC-025/G1` stands exactly as Spec 025
and Phase-385 left it — SUPPORTED under
composition and preservation control, with the
standing rider, quoted verbatim wherever the
claim is stated: **"Chronology is NOT
controlled in the primary test: period/phase
(chronology) remain uncontrolled confounders;
the S-chron sensitivity bound is reported
alongside, never as the controlled verdict."**

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
