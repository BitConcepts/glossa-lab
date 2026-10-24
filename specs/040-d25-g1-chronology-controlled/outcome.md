# Spec 040 — Outcome record (SKELETON — NOT EXECUTED)

> ## NOT EXECUTED — 2026-10-20
>
> This is the pre-written outcome skeleton for
> Spec 040 (design D-25). The spec is a draft;
> its freeze is barred until Spec 039 has
> executed (spec §1), and its execution is a
> separate owner order under the phase number
> the freeze allocates. Nothing in this file
> is a result. At execution, the outcome is
> appended below the skeleton marker as a
> dated entry; this skeleton is not edited
> into a result after the fact.

## What an execution will record here

1. **Gate record.** The dependency
   re-verification (Spec 039 freeze digest,
   outcome, and assignment-artifact SHA-256 as
   named in Spec 040's freeze record); the
   input-integrity checks against spec §3; the
   §4.1 join census (exactly one assignment
   row per population inscription).
2. **Margins (spec §5).** Assigned and
   unassigned counts and shares, overall, by
   site, and by coarse period; distinct sites
   with assigned inscriptions per period; the
   contested-excluded count; permutable
   inscriptions under the primary strata; and
   the gate's three arms, each marked pass or
   fail with its numbers.
3. **Regression (spec §7).** The
   composition-only and composition ×
   preservation reproductions, quantity by
   quantity against the Phase-137/Phase-140
   records, each marked exact or the run's
   INVALID stop recorded.
4. **Primary (spec §6), if reached.** The
   analysis population and sites; the profile
   table's dimensions and sparsity disclosure;
   observed χ²; the permutation record (B,
   seed, count ≥ observed, null median and
   95th percentile, permutable N, raw p);
   Cramér's V; per-site total-variation
   distances; the bootstrap record (B, seed,
   percentile interval, governing basic
   interval, bootstrap median).
5. **Outcome (spec §6.4 / §9).** Exactly one
   of: SUPPORTED — CHRONOLOGY CONTROLLED ·
   WEAKENED — RIDER CONFIRMED AS MATERIAL ·
   CONTRADICTED AT THE DECLARED MARGIN ·
   NOT-YET-TESTABLE (gate named) · INVALID
   (stop condition named). For a §6.4 outcome,
   the interval and margin are stated beside
   the word, and the size of any change from
   the Phase-385 interval [0.1838, 0.2102] is
   reported.
6. **Sensitivities (spec §8).**
   Contested-included quantities beside the
   primary's; the leave-one-site-out table;
   the named drop-Harappa reading (or NOT
   APPLICABLE with its reason); the recorded
   companions as recorded. Each labelled
   SENSITIVITY; none moves the outcome.
7. **Claim consequence.** The dated append
   made to the G1 record under spec §6.4 and
   F040-C15 (rider retired / G1 restated as a
   period-confounded association /
   chronology-controlled form contradicted at
   the margin), or the statement that no
   consequence arose (NOT-YET-TESTABLE /
   INVALID) and G1 stands unchanged.
8. **Integrity.** Anchors SHA-256 asserted
   byte-identical before and after; the
   foundation check as measured; the
   experiment-graph node as registered and
   verified.

## Headline rule (spec §10)

Every statement of the outcome carries the
lineage label "ICIT-lineage layer (horus84)",
the assignment census, and — for a §6.4
outcome — the governing interval and the
margin. A G1 quotation from before the
execution carries the standing rider verbatim
unless a SUPPORTED outcome has retired it by
append.

---

*Skeleton ends. Execution appends below this
line, dated, without editing the above.*

---

## DEPENDENCY-GATE RECORD - appended 2026-10-20 (the freeze act)

**State: NOT-YET-TESTABLE - dependency gate.**
The freeze does not proceed. No freeze digest
was computed, no execution phase number was
allocated (DD-040-10 remains open), the AEE
lifecycle hooks were not run, no OSF
registration was filed, and nothing was
executed. This record is the spec's outcome;
it is recorded at the freeze stage because the
gate that failed is the freeze-stage gate
(spec section 1; tasks L5).

**Headline (spec section 10 form).** On the
ICIT-lineage layer (horus84), Spec 040 (D-25)
closes **NOT-YET-TESTABLE - dependency gate**.
No assignment census exists under this spec:
no label was joined, no margin was computed,
and no repertoire quantity was calculated -
the gate verification below is the whole
record. No consequence arises for G1:
`STUDY-SPEC-025/G1` stands exactly as Spec 025
and Phase-385 left it, SUPPORTED under
composition and preservation control with the
standing rider, quoted verbatim wherever the
claim is stated: **chronology is NOT
controlled in the primary test**.

### 1. The verification (spec section 1, condition by condition)

Verified first-hand at the freeze act,
2026-10-20, against the merged record:

- **Condition 1 - SATISFIED.** Spec 039 has
  executed: freeze digest
  `ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742`
  (freeze PR #226 merged at `05f961fc`), its
  execution (Phase-403) recorded in record PR
  #234 (merged `14d15411`) and completion PR
  #235 (merged `a61da697`, the main this record
  lands on). Its outcome record is merged and
  is named here.
- **The artifact's identity - VERIFIED.**
  `data/movement/gazetteer_rows_assigned.jsonl`
  recomputed from main: SHA-256
  `64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4`,
  36 rows, 30 sites - the artifact and hash
  the freeze act was given.
- **Condition 2 - FAILED.** The artifact does
  not resolve the chronological placement of
  G1 inscriptions at site-period resolution in
  the section 4 sense. Its assignment unit is
  the site: Spec 039's own governed record
  states that assignments are per
  `program_site_id`, carried identically onto
  all of a site's rows (F039-C04), and that
  the site is the assignment unit (F039-C06).
  Each assigned site carries a **set** of
  coarse labels - the periods its published
  record spans (harappa: Early, Mature, and
  Late Harappan; mohenjo daro: Mature and Late
  Harappan; kalibangan: Early and Mature
  Harappan; lothal: Mature and Late Harappan) -
  not a mapping from an inscription's recorded
  local chronological label to exactly one
  coarse period. The assignment schema carries
  no local-label key: its fields are the label
  set, the mapping-rule list, the evidence
  (citation, locator, prose `published_value`,
  `mapped_labels` as a set), the contested
  flag, and the reviewer. Local period names
  (the Harappa five-period sequence, the
  Mohenjo-daro Phases A/B) appear only inside
  prose evidence strings; reconstructing a
  per-label pairing from that prose would be
  analyst judgement at execution time, which
  section 4.3 forbids.
- **Condition 3 - SATISFIED IN FORM; does not
  cure condition 2.** Every recorded
  assignment carries its published source
  citation and locator, the mapping rule
  applied, and its contested flag, and rests
  on published determinations only (Spec 039
  outcome: F039-C02, C03, C07, C08 HELD; one
  contested assignment, banawali, is flagged
  and both determinations retained). The
  citations support site-level determinations;
  they are not inscription placements.
- **Condition 4 - FAILED.** The artifact's
  join key (`program_site_id`) does not cover
  the G1 population. Of the seven population
  sites, chanhu-daro, dholavira, and nausharo
  have no rows in the artifact at all - they
  are not among the gazetteer's 30 sites - and
  for the four sites present the key yields
  label sets, not the exactly-one assignment
  row per population inscription that
  section 4.1 requires. Section 1 states the
  rule this fails under: a site-level
  occupation label by itself does not satisfy
  the gate, and section 4.3 forbids borrowing
  it for every inscription of the site.

### 2. Why the interface is not loosened

DD-040-3, a draft-fixed reading, governs: if
Spec 039's executed product cannot support
this interface, section 1's gate fails and the
honest state is NOT-YET-TESTABLE - the
interface is not loosened to fit the product.
Spec 039's own fences say the same from its
side: its labels "are finding aids, not dating
evidence", and "no chronology scenario, spine
row, or timing computation consumes an
assignment as a date" (Spec 039 spec.md; its
outcome HELD the same under F039-C15). The
gazetteer act did the work it was designed and
frozen to do - it changed the period screen
for the movement questions (Spec 031's
margins verification re-ran over its output,
and Q7 still closes at the link-mass floor).
It was not designed to place inscriptions, and
this spec does not retrofit it into a placing
instrument after the fact.

### 3. Consequences and non-consequences

- **Tasks L4 (AEE lifecycle hooks) was not
  run.** The freeze AEE note fixes the order:
  the section 1 gate stands in front of the
  hooks, and "the hooks run only when that
  gate is satisfied". The register stands at
  0.5-draft; the draft digest
  `63ca1ac99ed106b7bb7cc3d0e324e7522617021ea353af2a6055d975d316ac85`
  stands as a draft digest and decides
  nothing, as its own record states.
- **DD-040-1, DD-040-5, DD-040-6, and
  DD-040-9 were not decided.** They are freeze
  decisions; no freeze occurred. They remain
  open proposals on this draft - in
  particular, the re-derived interval-at-margin
  decision rule (DD-040-1) is **not** adopted
  by this record, and the margins gate's third
  arm (DD-040-6) and the closure's word
  (DD-040-5) stand exactly as drafted.
- **No phase number is allocated.** The
  freeze order's expectation of Phase-404 is
  not taken: phase numbers are allocated by
  freeze acts, and there was none. DD-040-10
  remains open.
- **No OSF registration is filed** (DD-040-9
  untaken), and there is no execution, no
  graph node, and no margins record under
  this spec.
- **Secondary finding, recorded for any
  future freeze attempt.** The anchors pin
  carried in this draft (spec section 3 and
  the freeze definition: SHA-256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`)
  does not match the anchors file as it
  stands: `backend/reports/INDUS_FINAL_ANCHORS.json`
  recomputes to
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
  both on current main and at this draft's own
  base, unchanged since 2026-10-12 (Spec 029
  Phase H). The draft, written 2026-10-20,
  carries the superseded value. Nothing under
  this spec ran, so no before/after assertion
  arises; a future freeze of this contract
  must refresh that pin as part of finalising
  its freeze texts. This finding does not
  affect the gate outcome, which fails on
  section 1 conditions 2 and 4 alone.
- **What would satisfy the gate.** A future,
  separately governed act producing a frozen,
  machine-readable mapping keyed by site x the
  layer's recorded local chronological
  label(s) to one coarse period (or
  UNASSIGNED), every mapping carrying its
  published citation and locator and its
  contested flag, covering the population's
  seven sites - an artifact built to
  section 4's interface under the
  published-determinations-only standard.
  Whether to commission such an act is an
  owner decision. This record does not
  commission it, and this spec is not revived
  by it automatically: a satisfied dependency
  would still require a freeze act (hooks,
  decisions DD-040-1/5/6/9/10, a digest) and a
  separate execution order, as drafted.

### 4. Claim consequences (governed register, 0.5-draft)

- **F040-C02 - FIRED, as written.** Its
  verdict rule assigns exactly this state:
  no frozen Spec 039 labels in consumable
  form, no Spec 040 freeze - NOT-YET-TESTABLE
  at the dependency gate.
- **F040-C01, C03-C14 - NOT REACHED.** No
  assignment (C04), join (C03/C04), margins
  (C12), computation (C05-C08), outcome
  (C09-C11), or sensitivity (C13-C14) was
  performed or evaluated.
- **F040-C15 - HELD in form.** This closure
  is recorded by dated append under the
  ICIT-lineage label; no frozen record (Spec
  025, Phase-140, Phase-385, Spec 039) is
  edited by it. No assignment census exists
  to attach, and the record states that
  rather than omitting it.

---

## EXECUTION RECORD - appended 2026-10-24 (Phase-439)

> ## EXECUTED — 2026-10-24
>
> Executed under the frozen Spec 040 contract
> (freeze digest
> `16aeeb7017f34f079742e56f13bfd88e3955ce75722693eae87fbbbaa9927515`,
> freeze PR #366 merged at `7ece27ee`), as
> **Phase-439**, under the owner's execution
> order of 2026-10-24 (19:04 EDT), after OSF
> registration **2rgtb** was approved and
> public. Outcome: **NOT-YET-TESTABLE** —
> the §5 margins gate failed on arms 1 and 2
> (arm 3 passed) on margins recomputed from
> the pinned inputs at this run. Step 0
> passed all three gates. The §7 regression,
> the §6 primary, and the §8 sensitivities
> were not reached. No consequence arises
> for G1 (skeleton item 7): `STUDY-SPEC-025/G1`
> stands exactly as Spec 025 and Phase-385
> left it.

**Headline (spec §10 form).** On the
ICIT-lineage layer (horus84), Spec 040
(Phase-439) closes NOT-YET-TESTABLE at the
section 5 margins gate. Assignment census
under derivation A1, consuming Spec 041's
artifact `data/evidence_integration/site_period_mapping.jsonl`
(SHA-256 `1e5b54c9…`; Spec 039's artifact,
named in the freeze record, did not satisfy
section 1 and is not the consumed artifact):
assigned 1,457 of 5,410 inscriptions (26.9%),
unassigned 3,953 (73.1%) — no informative
label 2,294; all labels UNASSIGNED 1,658; 1
disagreement left unplaced; contested-
excluded 0. Margins gate: arm 1 FAIL (EARLY
retains assigned inscriptions from 1 distinct
site, MATURE from 5, LATE from 2, against the
5-site arm); arm 2 FAIL (unassigned share
73.1% against the 40% arm); arm 3 PASS
(permutable inscriptions 1,205 against the
1,000 arm, DD-040-6 retained). No profile
table, no permutation, and no interval was
computed; the section 7 regression and the
section 6 primary were not reached. G1
stands unchanged: SUPPORTED under composition
and preservation control, with the standing
rider — **"Chronology is NOT controlled in
the primary test: period/phase (chronology)
remain uncontrolled confounders; the S-chron
sensitivity bound is reported alongside,
never as the controlled verdict."**

### 1. Gate record (skeleton item 1)

Step 0 passed, in order, fail-closed (full
record: `step0-record.md` in this directory).
Gate 1 — pin verification: every freeze §3
pin recomputed against origin/main
(`1e5b54c9…`, `bda1017d…`, `b57fb6b1…`,
`64f288d3…`, `a0f0d05a…`, `9dc2fba5…`,
`df0cf620…`); the recorded Spec 039 / Spec
041 freeze digests stand; the Spec 040
freeze record replays exactly; the layer
asserted at `c368f290…` before any use (from
the venue's held copy, re-acquired from the
pinned source earlier the same day after the
sweep copy proved absent — Spec 041's G0.1
pattern; the main checkout's downloads copy
hashes to a different file and was not used).
Gate 2 — population reproduction and the
§4.1 join under A1: 5,410 rows reproduced
(by site 74 / 238 / 2,717 / 212 / 208 /
1,923 / 38), covariates in agreement with
the layer on every population row (0
mismatches), label margins exact (2,266 /
2,638 / 1,788 / 3,116 / 2,294), the census
equal to the artifact's 78 triples, and the
join yielding exactly one assignment row per
population inscription ID, reproducing the
freeze §3 A1 counts exactly. Gate 3 —
determinism: the computation run twice,
canonical records identical; two further
venue runs of the phase script produced the
machine record byte-identically (SHA-256
`bccb59c4…`).

Venue note: the fresh git worktree off
origin/main was reaped by the VM write
restriction mid-run; the run executed in a
minimal tree assembled from origin/main via
the API with every input hash-verified at
gate 1, and the record was landed through
the git-data API. No input and no rule
changed with the venue machinery
(`step0-record.md`).

### 2. Margins (skeleton item 2; spec §5)

Assigned 1,457 of 5,410 (26.9%); unassigned
3,953 (73.1%) — no informative label 2,294,
all labels UNASSIGNED 1,658, 1 disagreement
unplaced, contested-excluded 0. By period:
EARLY 32, MATURE 1,386, LATE 39. Distinct
sites per period: EARLY 1 (Harappa); MATURE
5 (Dholavira, Harappa, Kalibangan, Lothal,
Nausharo); LATE 2 (Dholavira, Lothal). By
site (population / assigned): Chanhu-daro
74 / 0; Dholavira 238 / 133 (MATURE 97, LATE
36); Harappa 2,717 / 1,021 (EARLY 32, MATURE
989); Kalibangan 212 / 157; Lothal 208 / 108
(MATURE 105, LATE 3); Mohenjo-daro 1,923 /
0; Nausharo 38 / 38. Permutable inscriptions
under the §6 primary strata: 1,205 (36 of 65
strata hold ≥ 2 distinct sites). The gate's
three arms: arm 1 FAIL, arm 2 FAIL, arm 3
PASS — the gate requires all three, so the
execution closes NOT-YET-TESTABLE (DD-040-5)
before any outcome quantity exists.

### 3. Regression and primary (skeleton items 3–5)

NOT REACHED. Spec §13 places the §7
comparability regression and the §6 primary
after the margins gate, and §5 forbids
computing any outcome quantity past a failed
gate. No profile table was built, no
permutation run, no interval estimated. The
§8 sensitivities (item 6) were likewise not
reached: no primary outcome exists to bound,
and §8.1 stands NOT APPLICABLE on the
zero-contested-cell record, as frozen.

### 4. Claim consequence (skeleton item 7)

None arose. The closure is NOT-YET-TESTABLE;
under spec §9 that class carries no §6.4
consequence, and G1 stands unchanged —
SUPPORTED under composition and
preservation control (Phase-140), governing
basic interval [0.1838, 0.2102] against the
V = 0.10 floor (Phase-385), with the
standing rider quoted verbatim in the
headline above. For the register: F040-C02
HELD (the dependency settled by the recorded
substitution and re-verified at gate 1);
F040-C04 and F040-C12 DISCHARGED AS
DESIGNED — the A1 assignment ran exactly as
frozen and the margins gate closed the
execution in its own word; F040-C05–C11 and
C13–C14 NOT REACHED with the stages they
govern; F040-C15 HELD in form (this record
is a dated append under the ICIT-lineage
label; no frozen record is edited by it).

### 5. Integrity (skeleton item 8)

Anchors asserted byte-identical before and
after: `df0cf620…` at both readings; no
anchor moved; no PRED contact. The
experiment-graph node
`IndusPhase439G1ChronologyControlled`
(`backend/glossa_lab/experiment_graph_phase439.py`)
was registered and verified before the run
(tasks E1). Records:
`reports/phase439_results.json` (the full
machine record), `reports/phase439_report.md`
(the §10 report), `step0-record.md` in this
directory. Foundation check on the merged
tree: recorded in the landing record below,
as measured.

## Landing record

Appended at merge (append-only): PR number,
merge commit, CI conclusions, and the
foundation check as measured on the merged
tree.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
