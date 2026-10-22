# Spec 068 — Yadav's Zipf Fit: What Is a Curve Fit Worth? — Successor on the Shakti Corpus (Amendment S-053)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-22
>
> Drafted under the owner's 2026-10-22 readiness
> decisions, decision 2: drafting a successor to
> Spec 053 on the Shakti corpus is approved, under
> Amendment S-053 as proposed in §1.5 of the Shakti
> readiness assessment
> (`~/workspace/research_notes/shakti-readiness-proposals-2026-10-22.md`),
> as a new spec with a new OSF registration, with a
> documented-lineage-only primary fit and a
> documented + corroborated sensitivity fit, with
> the strict-sign-set choice ruled at this spec's
> freeze, and with decision 2c accepted on the
> record: the result is a new baseline, and it
> neither confirms nor corrects Phase-43. Drafts
> are pre-approved standing in this program; **the
> freeze, the execution, and the OSF registration
> of Spec 068 are separate later owner acts.** No
> AEE lifecycle hooks have run on this draft; they
> are a freeze gate, on the posture for draft
> registers recorded in DD-038-10. Nothing in this
> draft has been run, frozen, registered, fitted,
> or computed.
>
> The execution phase number is **UNASSIGNED** at
> this draft. It is allocated at the freeze act,
> from the merged record as it then stands.

**Design source:** Spec 053
(`specs/053-yadav-zipf-controls/`, frozen
2026-10-21, closed at its own step 0 as STRICT
CORPUS NOT PINNABLE) — its question, its frozen
estimator, its named controls, and its comparison
rule are this successor's substance, carried
under the corpus substitution of Amendment S-053
(§2.1). The readiness assessment that proposed
the amendment (§§1.5–1.6 of the memo named in the
banner) and the provenance audit it rests on
(`~/workspace/research_notes/shakti-provenance-audit-2026-10-22.md`)
were read first-hand at this draft.

**Claim under test:** the same claim as Spec 053,
`yadav_2009_arxiv_manual_001` — "Indus script
sign frequencies follow a Zipf-Mandelbrot
distribution" — standing **SETTLED, strongly
supported** on its recorded test. This successor
tests only the residue Spec 053 tested: what that
recorded fit is *worth*, measured against named
controls. It does not re-open Spec 053, whose
closure record stands, and it changes no verdict
(§8, limit 2).

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim, the question, and the falsifier

### 1.1 The record the claim stands on

Spec 053's record, restated from its frozen text:
the verdict stands — on the corpus the program
fitted, the sign frequencies do follow the
Zipf-Mandelbrot curve, and the recorded exponent
(about 1.35) sits in the range Yadav's original
work reported. The residue is what that fit is
*worth*: a Zipf-style curve is weak evidence
about meaning, because many systems that are not
language at all — and some random processes —
produce similar curves, and the exponent's exact
value moves with corpus size and with how signs
are split or merged. Spec 053 designed the
control comparison for that residue, froze it,
and then closed at its step-0 gate 0.3 because
the V3 / Mahadevan-lineage corpus layer of
record could not be identified and pinned in
the execution tree. No fit was computed under
Spec 053. This successor runs the same
comparison on a different, pinnable Indus
distribution — the Shakti corpus, under the
substitution of §2.1 — and on no other terms.

### 1.2 The question, in plain words (Spec 053's, unchanged)

Fit one identical curve-fitting rule to the
script and to symbol systems that are certainly
not writing. If the non-writing systems fit the
curve as well as the script does, then the
script's good fit, on its own, says almost
nothing — and the claim's record should carry
that strength label in so many words. If every
non-writing system fits strictly worse, the fit
is separable on these measures, and the record
should carry that instead. Either way the
product is an honest strength label for a
settled claim — not a new verdict on the claim
(§7, limit 2).

### 1.3 The falsifier, first

**Falsifier.** At least one named non-linguistic
control system fits the curve **as well as or
better than** the Indus distribution of record
for this spec (§2.1: the Shakti restricted
corpus, primary fit) does, under the identical
fitting rules of §5 — the estimator frozen by
Spec 053. "Fits as well" is mechanical, exactly
as Spec 053 fixed it: a control fits as well
iff its primary fit error (§5.2) is less than
or equal to the Indus primary fit error. No
tolerance band enters the verdict rule; near
misses are reported, not verdicts (§5.3).

Everything below is written so that this
falsifier can fire: the corpus is identified
and pinned before any fitting (§4, gates 0.3
and 0.4), the control set is named and frozen
as cited data before any fit (§4, gate 0.6),
the estimator and the comparison rule are the
ones Spec 053 froze (§5), the step-0 gates run
before any fit quantity exists (§4), and every
outcome — including the falsifier's own word,
NOT SEPARABLE — is pre-written in §7 before
any result can be known.

### 1.4 The hypothesis

**Hypothesis.** The Indus fit — on the primary
population of §2.1, under the population limb
the freeze chooses (§2.2) — is *distinguishable*
from the fits of the named non-linguistic
control systems: every non-linguistic control's
primary fit error is strictly greater than the
Indus primary fit error, under §5's rules — and
the comparison itself is informative, in the
sense §5.4 fixes: the linguistic positive
control fits strictly better than every
non-linguistic control.

## 2. The corpus substitution, and the one open freeze item

### 2.1 Amendment S-053 — the draft's corpus-substitution basis, quoted and cited

The substitution this draft stands on is the
amendment wording proposed in §1.5 of the
readiness assessment
(`shakti-readiness-proposals-2026-10-22.md`,
"Spec 053 (D-07A, Yadav Zipf controls) —
TRANSFERS WITH NAMED AMENDMENT"), adopted for
drafting by the owner's 2026-10-22 decision 2.
It is quoted here verbatim, in full, because
the draft's gates are its operative form:

> **Amendment S-053 (draft, not adopted): Corpus substitution for a
> successor to Spec 053's question.** Gate 0.3 of the successor reads:
> "The Indus distribution of record for this spec is the ShaktiOSindia
> corpus as graded in the provenance audit of 2026-10-22
> (`shakti-provenance-audit-2026-10-22.md`), restricted to rows graded
> documented-lineage (3,212 rows; 3,045 analyzable), pinned by the
> deposit file's SHA-256 `345241b1…` and the row-grades file's SHA-256
> as recorded in the successor's intake record. The gate states the
> restricted corpus's inscription count, token count, and distinct-sign
> count as measured at step 0. The V3 / Mahadevan-lineage corpus, the
> Phase-43 census (3,916 / 3,137 / 12,494), and the Phase-43 exponent
> are not inputs to this spec and no quantity in it is a reproduction
> of a Phase-43 quantity. A sensitivity fit over
> documented-lineage + undocumented-corroborated rows (5,299 rows;
> 5,131 analyzable, as graded) is reported alongside the primary fit;
> if the two fits' verdict-relevant ordering against the controls
> differs, both are reported and neither is suppressed. Rows graded
> undocumented-uncorroborated (405) enter no fit. The strict-sign-set
> restriction is [retained, keyed to ICIT space by the mapping pinned
> at step 0 / dropped, with the population stated as the full ICIT
> inventory] — the successor's freeze must choose one and record the
> choice; it may not proceed with the choice unstated."

Two pins the amendment's draft text leaves
short are stated in full in this draft, from
Proposal P-F1 (§1.6 of the same memo) and the
intake record the freeze will assert against
(§2.2 of this spec):

- Corpus file (`sanitized_corpus.json`) SHA-256:
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`
- Row-grades file SHA-256:
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`

The grade counts in the amendment are the
provenance audit's counts: 5,704 rows in the
corpus; 5,536 analyzable (rows that are not
entirely illegible — not all-`000`); grades
3,212 documented-lineage / 2,087
undocumented-corroborated / 405
undocumented-uncorroborated. Derived subset
figures used in this draft — documented-only
3,212 rows, 3,045 analyzable; documented +
corroborated 5,299 rows, 5,131 analyzable
(3,045 + 2,086: the one all-`000` corroborated
row, H-986, is in the 2,087 but not in the
analyzable subset, and is excluded from sign
analysis regardless) — are derived figures
from the audit's published counts. **This
successor's own step-0 census governs over
every derived figure in this draft** (§4,
gate 0.4).

The intake gates this successor cites the
corpus under are Proposal P-F1's, §1.6 of the
readiness assessment, in their four parts:
**S1** identity (both SHA-256 pins recompute);
**S2** census (the audit's census reproduces);
**S3** the lineage statement (§10, item 1 of
this spec — carried in the headline block of
every product); **S4** grade discipline (§6.1
of this spec). Failure of S1 or S2 closes this
spec at step 0 as **SHAKTI INTAKE NOT
REPRODUCED** (§7 wording). S3/S4 failures are
integrity findings, reported as such, not
repaired silently.

**The no-Phase-43 fence (owner decision 2c,
stated here as the draft's standing term).**
The V3 / Mahadevan corpus, the Phase-43 census,
and the Phase-43 exponent (about 1.35) are
**not inputs** to this spec. No quantity in
this spec is a reproduction or a correction
of a Phase-43 quantity. A fit measured here is
a **new baseline**: comparable to the controls
inside this spec, and to nothing in Phase-43.
The Phase-43 numbers are named in this draft
only inside this fence, so the fence can be
checked; they enter no gate, no fit, and no
comparison.

### 2.2 OPEN-068-1 — the strict-sign-set restriction (both limbs drafted; the choice is the freeze's)

Spec 053's primary population was the strict
sign set's distribution: the 94 sign identities
carrying validation status
`strict_sa_independent` in the anchors file —
identities stated in the program's existing
(Mahadevan-space) numbering. The Shakti corpus
is in ICIT (Wells/Fuls) numbering; an ICIT sign
number is not the same sign as the same
Mahadevan number. Keying the strict set into
ICIT space is therefore a substantive act, not
a clerical one, and Amendment S-053 leaves the
choice open in brackets. This draft drafts
**both limbs in full** and adopts **neither**:

- **Limb A — retained, keyed to ICIT space by
  a mapping act stated and pinned at step 0.**
  The fit population is: analyzable
  documented-lineage rows, counting only
  tokens whose ICIT sign is in the mapped
  strict set. The mapping act is a step-0 act
  (§4, gate 0.5): the step-0 record states,
  for each of the 94 strict sign identities,
  its ICIT counterpart or that it has none,
  states the basis each mapping rests on,
  and pins the mapping table by SHA-256
  digest. A strict identity with no ICIT
  counterpart contributes no types and no
  tokens, and is named in the step-0 record.
  Signs outside the mapped strict set
  contribute neither types nor tokens. If the
  mapping cannot be stated in full and pinned
  at step 0, the run closes as **STRICT
  MAPPING NOT PINNABLE** (§7 wording) and
  nothing is fitted. The freeze that chooses
  this limb must also name the mapping's basis
  source, so step 0 has a stated basis to pin
  against; a mapping invented at run time is
  not this limb.
- **Limb B — dropped, with the population
  stated as the full ICIT sign inventory of
  the restricted corpus.** The fit population
  is: analyzable documented-lineage rows,
  counting every token, by ICIT sign type —
  the full ICIT sign inventory present in the
  restricted corpus, whatever step 0 measures
  it to be. No strict restriction applies, no
  mapping act is performed, and no output may
  describe this population as a strict
  population. This limb's population differs
  from Spec 053's primary population openly,
  by the freeze's recorded choice; it is the
  same substitution posture Amendment S-053
  states for the corpus itself.

**The draft may not proceed past freeze with
the choice unstated.** The freeze must choose
one limb, record the choice and its reasons,
and restate the chosen population in the
freeze record in the terms above. Every claim
whose verdict turns on the fit population
carries this item as a claim-level dependency
(`claims.json`: F068-C02, and through it
F068-C04, F068-C06, F068-C10, and F068-C11).
An execution ordered under a freeze record
that does not state the choice is not an
execution under this spec.

## 3. Inputs (pinned where a pin exists; every pin re-asserted at the freeze)

Every repository pin in this section is carried
from Spec 053's frozen record, where it was
re-derived at that freeze by two independent
routes; each is re-asserted at this spec's
freeze against the merged record as it then
stands.

| Input | Pin / state |
|---|---|
| Spec 053 frozen record (`specs/053-yadav-zipf-controls/spec.md` and `adjudication.md` on `main`) | Read first-hand at this draft from `main` at head `2a0eb854982f52453bcd76fd4a5bcbb088eb21e8`. The estimator of its §4.2, the self-test of its gate 0.2, the controls of its gate 0.4, the comparison rule of its §4.3, the positive-control condition of its §4.4, and the floors confirmed by its DD-053-14 are carried into this spec as frozen substance (§§5–6). Its freeze decisions DD-053-11 to DD-053-19 stand; DD-053-11 is this successor's estimator authority (adjudication §1). Spec 053's own closure (STRICT CORPUS NOT PINNABLE at its gate 0.3) stands and is not re-opened by this spec. |
| Shakti corpus (`sanitized_corpus.json`, the ShaktiOSindia deposit file) | SHA-256 `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68` (Proposal P-F1, §1.6 of the readiness assessment; the provenance audit verified the file against the deposit README's pin before any counting). Held restricted-local under its GPL-3.0 terms; cited only through the intake record and the row-grades file. The corpus file itself is not a repository file of this program and no copy is committed under this spec. |
| Row-grades file (the provenance audit's row-level grades for all 5,704 rows) | SHA-256 `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739` (as recorded in the intake record, §3 of this table). Restricted-local, beside the corpus download, not in any git repository — the audit's own posture, carried here. |
| Shakti intake record (`docs/decisions/2026-10-22-shakti-corpus-intake-record.md`) | **Cited by this path as the standing record the freeze will assert against.** At this draft the file is being created in parallel and is not yet on `main` at head `2a0eb854…` (verified at this draft); the freeze may not proceed until the intake record stands on the merged record carrying the two SHA-256 pins of §2.1 and the P-F1 gates S1–S4 in their adopted form. Step 0 asserts S1 and S2 against that record (§4, gates 0.3–0.4). |
| Provenance audit (`shakti-provenance-audit-2026-10-22.md`, 2026-10-22) | The grading of record: 3,212 documented-lineage / 2,087 undocumented-corroborated / 405 undocumented-uncorroborated; the census asserted at §4 gate 0.4 of this spec; the §3 caveat that is the source of P-F1 S3's lineage statement. Read first-hand at this draft from `~/workspace/research_notes/`. |
| Readiness assessment (`shakti-readiness-proposals-2026-10-22.md`) | The amendment and gates of record: §1.5 (Amendment S-053, quoted at §2.1) and §1.6 (Proposal P-F1, gates S1–S4). Read first-hand at this draft. The owner's decision 2 adopting S-053 for drafting is recorded in the banner of this spec and in `adjudication.md`. |
| Claim record (`glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`) | SHA-256 `904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3` (Spec 053's freeze pin, re-asserted at this spec's freeze). manual_001: strongly supported, stage explained; evidence string and not-understood text as Spec 053 §1 states. This successor appends to its record only as §10 provides; it edits nothing in it. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) — the strict sign set's census source | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (Spec 053's freeze pin). Census as frozen there: 287 anchors, **94** carrying validation status `strict_sa_independent` — the strict sign set whose ICIT keying is OPEN-068-1 limb A's object. Operative only if the freeze chooses limb A; under limb B it is cited here for the record of what was dropped, and no mapping is performed. This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| Sign crosswalk (`data/crosswalks/sign_crosswalk_master.csv`) | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (Spec 053's freeze pin). Cited for numbering questions. It is **not** carried as this successor's split/merge variant source: Spec 053's sensitivity S2 built its variants from this crosswalk's structure over the Mahadevan-space population, and no ICIT-space variant source is named in Amendment S-053 — none is invented at this draft (adjudication §6, defect 4). |
| Control counts — the named systems of §4 gate 0.6 | Exactly Spec 053's frozen set (DD-053-13): the named systems and bibliographic pins stand as in Spec 053 gate 0.4, and gate 0.6 of this spec is the fixed pin source for the control tables — the exact tables and per-count locators are entered there as cited data, before any fit, and a system that cannot be entered whole closes the run CONTROL SET FREEZE FAILED. No second positive control is added. No count is typed into a script (H16). |

## 4. Step 0 — gates before any fit (fail-closed)

Execution runs these gates in order, before any
Zipf-Mandelbrot fit is computed for any system.
A failure stops the execution in the class
named; nothing is repaired at run time, and no
quantity produced before a gate failure is
quotable.

- **0.1 Input integrity.** Every §3 input that
  carries a pin hashes to its freeze-record
  value, the intake record stands on the merged
  record as §3 requires, and the anchors file
  is asserted byte-identical. A mismatch stops
  the run as **INVALID**.
- **0.2 Estimator self-test.** The §5 estimator,
  implemented once, is run on synthetic
  rank–frequency data generated from known
  Zipf-Mandelbrot parameters (α = 1.20,
  q = 2.0, V = 200 types, N = 50,000 tokens,
  seed 20261021, counts drawn by the stated
  multinomial procedure in the execution
  script) — Spec 053 gate 0.2, unchanged. The
  gate passes iff the fit recovers α within
  ±0.10 and q within ±1.0 of the generating
  values. A failure stops the run as
  **INVALID** — the comparison does not
  proceed on machinery that cannot first
  recover parameters it planted. This gate is
  the able-to-fail proof for the estimator
  (Spec 053 DD-053-3, carried).
- **0.3 Shakti intake — identity (P-F1 S1).**
  Asserted against the intake record of §3:
  the corpus file's SHA-256 recomputes to
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`,
  and the row-grades file's SHA-256 recomputes
  to
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`.
  Either recompute failing closes the run as
  **SHAKTI INTAKE NOT REPRODUCED** (§7
  wording) and nothing is fitted.
- **0.4 Shakti intake — census (P-F1 S2), and
  this successor's own restricted census.**
  Asserted against the intake record: the
  corpus counts reproduce the audit's census —
  5,704 rows; 5,536 analyzable; grade counts
  3,212 documented-lineage / 2,087
  undocumented-corroborated / 405
  undocumented-uncorroborated; 4,904 of 5,536
  analyzable rows (88.6%) carrying a CISI
  identifier. A mismatch closes the run as
  **SHAKTI INTAKE NOT REPRODUCED** and nothing
  is fitted. The same gate then measures and
  states **this successor's own
  restricted-corpus census**: for the primary
  set (documented-lineage rows only) and for
  the sensitivity set (documented +
  corroborated), each stated as rows,
  analyzable rows, inscription count, token
  count, and distinct-sign count, as measured
  at step 0. The derived figures of §2.1
  (primary 3,212 rows, 3,045 analyzable;
  sensitivity 5,299 rows, 5,131 analyzable)
  are expectations the measurement checks,
  not the measurement: **the step-0 census
  governs over them** wherever they differ.
- **0.5 The population act, under the freeze's
  chosen limb (OPEN-068-1).** The step-0 record
  restates the freeze's chosen limb and
  exhibits the fit population it defines:
  under limb A, the mapping table of §2.2 —
  every one of the 94 strict identities stated
  with its ICIT counterpart or as having none,
  its basis stated, the table pinned by
  SHA-256 in the step-0 record; a mapping that
  cannot be stated in full and pinned closes
  the run as **STRICT MAPPING NOT PINNABLE**.
  Under limb B, the step-0 record states the
  population as the full ICIT sign inventory
  of the restricted corpus, with its measured
  distinct-sign count from gate 0.4. A freeze
  record that states no limb closes the run
  here, before any fit, as **INVALID** — the
  choice unstated is a freeze defect, and
  execution does not repair it.
- **0.6 Control set freeze (cited data).** The
  control set is entered and frozen in the
  step-0 record — **before any fit, including
  the Indus fit** — exactly as Spec 053 gate
  0.4 froze it. Each system's entry is a
  canonical count table (type identifier,
  token count) with a per-system source
  citation and per-count locators where the
  source is tabular.
  - **N1 — Mesopotamian numerical signs.**
    Token frequencies of numerical signs from
    published counts of archaic Mesopotamian
    administrative tablets (bibliographic pin:
    Nissen, Damerow & Englund, *Archaic
    Bookkeeping* (1993) and the published
    archaic sign counts it reports — the exact
    table is entered with its locator at this
    gate, per Spec 053 DD-053-13). Numerical
    signs only; phonetic/syllabic signs of the
    same tablets are not this system.
  - **N2 — Heraldic charges.** Frequencies of
    charges (the devices borne on shields)
    across a published roll of arms (the roll
    and edition are entered with their citation
    at this gate, as the fixed pin source for
    this system's table, per Spec 053
    DD-053-13). The counting unit is one charge
    occurrence on one shield, as the roll
    records it.
  - **N3 — Synthetic emblem inventory.**
    Generated, not published — fully pinned in
    Spec 053 (DD-053-6, confirmed DD-053-16):
    a Yule–Simon process with innovation
    probability ρ = 0.10, seed 20261021, run to
    exactly the Indus primary fit's token total
    N (gate 0.7's count, so the synthetic system
    is size-matched to the primary population
    the freeze's limb defines); 99 replicates
    are generated, each replicate is a separate
    system instance, and N3's fit quantities
    are the medians across replicates (§5.3).
    A uniform-random inventory is **not** the
    synthetic control, for the reason Spec 053
    recorded: it produces a near-flat
    distribution by construction and could not
    test the residue's point, which is that a
    *stated random process* can produce this
    curve.
  - **P1 — Linguistic positive control.**
    Sign frequencies of a deciphered,
    certainly-linguistic script from published
    corpus counts: **Linear B** syllabic sign
    frequencies (bibliographic pin: the
    published Linear B corpus counts; the exact
    source is entered with its citation at this
    gate, per Spec 053 DD-053-13, and no second
    positive control is added).
  If any named system's counts cannot be
  entered completely as published — the whole
  inventory the source reports, not a
  selection — or any entry lacks its citation,
  the run closes as **CONTROL SET FREEZE
  FAILED** (§7 wording). No system is
  substituted, trimmed, or completed from
  another source after this gate, and no fit
  of any kind precedes it.
- **0.7 Census floors (counts only).** From
  gate 0.4's census and gate 0.5's population:
  the primary fit population's distinct types
  present and token total N are stated in the
  step-0 record. **Floors, carried from Spec
  053 (DD-053-7, confirmed DD-053-14) and
  measured on the restricted set:** the
  primary proceeds only if distinct types
  present ≥ **50** and tokens ≥ **2,000** in
  the fit population the freeze's limb defines
  over the restricted (documented-lineage)
  corpus. Below either floor the execution
  closes as **TOO THIN** (§7 wording) with the
  census as its finding; no fit is computed.
  The frozen control tables' type and token
  counts are stated alongside, for the record;
  no floor applies to a control — a control is
  the published system as it stands. No floor
  applies to the sensitivity set either: it is
  reported as measured, beside the primary.

## 5. The estimator and the comparison rule (Spec 053's, frozen — identical)

This section restates Spec 053 §4 as frozen
(DD-053-11 to DD-053-16), with only the
population references changed to this spec's
§2 populations. Nothing in the fitting rule is
new, adjusted, or re-derived here: estimator
identity with Spec 053's freeze is itself a
claim of this spec (F068-C07).

### 5.1 The distribution fitted, per system

For each system, the input is its frozen count
table (§4 gate 0.6; for the Indus primary, the
fit population of gate 0.5 over the analyzable
documented-lineage rows; for the Indus
sensitivity fit, §6.1's population). Types are
ranked by count descending; ties are broken by
type identifier ascending, so the ranking is
deterministic. The ranked counts are
f(1) ≥ f(2) ≥ … ≥ f(V), with V the number of
distinct types and N = Σ f(r) the token total.

### 5.2 The estimator (identical for every system; identical to Spec 053's)

The Zipf-Mandelbrot model f̂(r) = C / (r + q)^α
is fitted with C fixed by normalisation
(Σ f̂(r) = N — C is not a free parameter), by
minimising the sum of squared log residuals,
SSE = Σ_r (log f(r) − log f̂(r))², over a
deterministic grid: α from 0.00 to 3.00 in
steps of 0.01, q from 0.0 to 20.0 in steps of
0.1; then one refinement pass at one-tenth
steps in α and q around the best grid cell.
The same code, grid, and refinement run for
every system, the Indus included. Reported per
system: V, N, fitted α and q, SSE, and:

- **Primary fit error (the comparison
  quantity):** NRMSE_log = √(SSE / V) — the
  root-mean-square log residual. It is a ratio
  measure, so systems of different sizes are
  compared on the shape of the fit, not on
  raw counts.
- **Secondary (reported, never decisive):**
  R² in log space, 1 − SSE / Σ_r (log f(r) −
  mean log f)², and the fitted α itself.

This estimator is Spec 053's fitting rule of
record, specified completely at that spec's
freeze as a freeze-stage design decision
(DD-053-11, option (a)), which honestly
**RETIRED** the "identical to Phase-43"
reading: no Phase-43 Zipf estimator exists to
be identical to. This successor inherits that
ruling whole. Its estimator is identical to
**Spec 053's frozen estimator** — that, and
nothing about Phase-43, is the identity this
spec asserts. No estimator may be substituted
after any fitting.

### 5.3 The comparison rule — what counts as "fits as well"

Stated mechanically, in full, before any
fitting — Spec 053 §4.3, unchanged:

1. Compute NRMSE_log for the Indus primary fit
   (call it E_Indus) and for each control:
   E_N1, E_N2, E_P1, and for N3 the **median**
   NRMSE_log across its 99 replicates (E_N3),
   with the replicates' full distribution
   reported.
2. A non-linguistic control **fits as well**
   iff its error is less than or equal to
   E_Indus: E ≤ E_Indus. ("As well or better,"
   with no tolerance band — Spec 053 DD-053-2,
   confirmed with ε = 0 at DD-053-15.)
3. The **falsifier fires** iff at least one of
   N1, N2, N3 fits as well under rule 2.
4. The **gap** Δ = E_control − E_Indus is
   reported for every control. A control with
   0 < Δ ≤ 0.02 is named a **NEAR MISS** in
   every product that reports the outcome: it
   did not fire the falsifier, and it is not
   buried either. The 0.02 band is a reporting
   rule only; it changes no verdict.
5. N3's replicates are also reported against
   rule 2 individually: the share of replicates
   fitting as well is stated beside the median
   rule's outcome, so a median that hides a
   split distribution is visible as one.

### 5.4 The positive-control validity condition

Spec 053 §4.4, unchanged. The comparison is
**informative** only if the estimator and
measures can tell a known language's
distribution from the named non-linguistic
ones. Mechanically: P1 passes iff E_P1 is
strictly less than every non-linguistic
control's error (E_P1 < E_N1, E_P1 < E_N2,
E_P1 < E_N3). If P1 does not pass, the headline
is **COMPARISON UNINFORMATIVE** (§7): the
measures did not separate the one system in
the set that is certainly writing, so they are
not used to judge the script either way. This
condition is checked from the same frozen
fits; it is not a fit of its own and it is not
adjustable after the fits exist.

### 5.5 The headline rule

After all gates pass and §5.4 is evaluated,
the headline — computed on the **primary fit**
— is exactly one of:

- **SEPARABLE** — P1 passes (§5.4) and no
  non-linguistic control fits as well (§5.3
  rule 3 does not fire).
- **NOT SEPARABLE** — P1 passes and the
  falsifier fires: at least one named
  non-linguistic system fits as well as or
  better than the script.
- **COMPARISON UNINFORMATIVE** — P1 does not
  pass, whatever the Indus comparison shows.

The sensitivity fit (§6.1) does not change the
headline word. Where §6.1's grade-sensitivity
rule fires, the headline is always quoted with
its grade-sensitivity statement beside it
(§6.1, rule 3; §10) — a difference between the
fits is a finding about the corpus grades,
reported with the same prominence as the
headline, never folded into a different
headline and never dropped.

## 6. Sensitivities (reported alongside, never verdict-changing)

### 6.1 The grade sensitivity — this successor's mandated sensitivity (Amendment S-053; P-F1 S4)

The same estimator of §5.2 is fitted to the
**sensitivity population**: analyzable rows
graded documented-lineage +
undocumented-corroborated (5,299 rows; 5,131
analyzable, as derived in §2.1 — the step-0
census of gate 0.4 governs), under the same
population limb the freeze chose for the
primary (under limb A, the same pinned mapping
applies; under limb B, the full ICIT inventory
of the sensitivity set). Rows graded
undocumented-uncorroborated (405) enter **no
fit, no count, no statistic, and no argument**
under this spec (P-F1 S4). The sensitivity fit
is reported alongside the primary, in full:
its V, N, fitted α and q, NRMSE_log, R²_log,
its per-control gaps, and its verdict-relevant
ordering against the controls — that is, for
each control, whether that control fits as
well as or better than the sensitivity fit's
Indus error, and where P1 stands against the
non-linguistic controls on the sensitivity
population.

1. If the sensitivity fit's verdict-relevant
   ordering against the controls is the same
   as the primary's, both fits are reported
   and the record states that the ordering
   does not change between the grade sets.
2. If the ordering **differs** between the
   fits, **both are reported and neither is
   suppressed**: the outcome record states
   both orderings in full, and the difference
   is reported as **grade-sensitivity** —
   in the outcome record's headline block and
   wherever the result is cited — per P-F1
   S4: a result that changes between the two
   grade sets is reported as grade-sensitive
   wherever it is cited.
3. The sensitivity fit changes no headline
   word (§5.5). A grade-sensitive headline is
   quoted, in every product, with the
   sentence: "This ordering is grade-sensitive:
   it differs between the documented-lineage
   fit and the documented + corroborated fit,
   and both fits are reported."

### 6.2 Subsampling (Spec 053 S1, carried)

The Indus primary distribution is refitted on
random halves and random quarters of the
restricted corpus's **inscriptions**
(inscription-level sampling, so no fabricated
texts are created — Spec 053 DD-053-9): 99
replicates per level, seed 20261021, sampling
without replacement. Reported per level:
median and central 90% interval of fitted α
and of NRMSE_log. The table states how far
the exponent and the fit error move with
corpus size, in numbers. The same table is
reported for the sensitivity population, so
size movement and grade movement are not
confused with each other.

### 6.3 Full-inventory fit (conditional on the limb; no Phase-43 bridge)

Under **limb A** only: the same estimator
fitted to the restricted corpus's **full**
ICIT sign inventory (all types in the
analyzable documented-lineage rows, not only
the mapped strict set), reported with its V,
N, α, q, and NRMSE_log beside the primary's.
Under **limb B** the primary already is that
fit, and no separate full-inventory fit exists
or is reported as one. In either case this
fit is a sensitivity only, carries no verdict,
and — unlike Spec 053's S3 — it is **not** a
comparability bridge to any earlier
population: its exponent is reported on its
own, never beside the Phase-43 exponent as a
reproduction, a confirmation, or a correction
(§2.1's fence).

## 7. Outcome set and pre-written verdict wordings

The execution ends in exactly one headline
outcome. The outcome record's headline
paragraph uses one of these forms, with the
bracketed quantities filled from the run.
These wordings are written before any data is
touched; no other headline wording may be
used. **Every headline block carries the
lineage statement of §10 item 1, in full,
before the outcome wording** — the bracketed
placeholder [lineage statement] in the forms
below stands for that statement, quoted
verbatim, never paraphrased. **Every
adjudicated outcome attaches to the claim as a
dated bounded finding (a strength label); none
changes the claim's recorded status** (§8,
limit 2).

- **SEPARABLE:** "[lineage statement] Fitted
  under the one Zipf-Mandelbrot rule frozen by
  Spec 053, the Indus distribution of record
  for this spec — the Shakti restricted corpus
  (documented-lineage rows; [population limb];
  fit error [E_Indus], exponent [α]) — fits
  the curve strictly better than every named
  non-linguistic control — Mesopotamian
  numerical signs ([E_N1]), heraldic charges
  ([E_N2]), and the synthetic emblem process
  (median [E_N3]) — and the linguistic positive
  control, Linear B sign frequencies ([E_P1]),
  fits strictly better than every
  non-linguistic control, so the measures
  separate the set's one certain writing system
  from its non-writing systems. [The
  grade-sensitivity sentence of §6.1, where it
  applies.] On these measures, and on these
  measures only, this fit is separable from
  the non-linguistic controls. This is a new
  baseline on a new corpus and a strength
  label for the recorded fit: it is not new
  evidence that the script encodes language,
  and it neither confirms nor corrects any
  Phase-43 quantity."
- **NOT SEPARABLE:** "[lineage statement]
  Fitted under the one Zipf-Mandelbrot rule
  frozen by Spec 053, [control name(s)] fit(s)
  the curve as well as or better than the
  Indus distribution of record for this spec
  does — the Shakti restricted corpus
  (documented-lineage rows; [population limb];
  Indus fit error [E_Indus]; [control] [E],
  gap [Δ]). A system that is not writing
  produces this curve as well as the script
  does, so the recorded fit, on its own,
  carries no distinguishing weight: the claim's
  record gains this dated strength label —
  'the Zipf-Mandelbrot fit is not separable
  from named non-linguistic systems on these
  measures' — beside its standing verdict,
  which does not change. [The grade-sensitivity
  sentence of §6.1, where it applies.] What the
  script encodes is not decided by this result
  in either direction, and no Phase-43 quantity
  is confirmed or corrected by it."
- **COMPARISON UNINFORMATIVE:** "[lineage
  statement] The comparison cannot judge the
  script: the linguistic positive control,
  Linear B sign frequencies (fit error [E_P1]),
  does not fit strictly better than every
  non-linguistic control ([per-control
  errors]), so the measures used here do not
  separate the one certain writing system in
  the set from systems that are not writing.
  The Indus quantities on the Shakti restricted
  corpus ([E_Indus], exponent [α]) are reported
  for the record as a new baseline and support
  no separability conclusion either way. [The
  grade-sensitivity sentence of §6.1, where it
  applies.] The claim stands exactly as
  recorded, with no strength label added."
- **TOO THIN (step-0 closure):** "Spec 068
  closed at step 0, gate 0.7: the primary fit
  population over the Shakti restricted corpus
  carries [t] distinct types and [n] tokens as
  measured at step 0, below the frozen floors
  (50 types, 2,000 tokens). No fit was
  computed. This closure is a statement about
  runnability, not about the claim; the claim
  stands exactly as recorded."
- **SHAKTI INTAKE NOT REPRODUCED (step-0
  closure):** "Spec 068 closed at step 0, gate
  [0.3 / 0.4]: the Shakti corpus intake did not
  reproduce against the intake record —
  [the corpus file's SHA-256 recomputed to
  [observed], not the pinned value / the
  row-grades file's SHA-256 recomputed to
  [observed], not the pinned value / the
  census recomputed as [observed counts], not
  the audit's census of 5,704 rows, 5,536
  analyzable, grades 3,212 / 2,087 / 405]. No
  fit was computed. This closure is a statement
  about the intake, not about the claim; the
  claim stands exactly as recorded."
- **STRICT MAPPING NOT PINNABLE (step-0
  closure, limb A only):** "Spec 068 closed at
  step 0, gate 0.5: the freeze chose limb A,
  and the strict sign set's keying to ICIT
  space could not be stated in full and pinned
  as §2.2 requires ([reason]). No fit was
  computed. This closure is a statement about
  the mapping act, not about the claim; the
  claim stands exactly as recorded."
- **CONTROL SET FREEZE FAILED (step-0
  closure):** "Spec 068 closed at step 0, gate
  0.6: the control set could not be frozen as
  cited data as §4 requires ([system and
  reason]). No fit was computed — in
  particular, the Indus fit was not computed
  ahead of the controls. This closure is a
  statement about runnability, not about the
  claim; the claim stands exactly as recorded."
- **INVALID (integrity closure):** "Spec 068
  closed as INVALID: [the named §3 pin
  mismatched / the intake record did not stand
  as §3 requires / the estimator self-test of
  gate 0.2 failed / the anchors assertion
  failed / the freeze record stated no
  population limb / a fit is shown to precede
  its gate / a product citing the corpus
  lacked the P-F1 S3 lineage statement / rows
  graded undocumented-uncorroborated entered a
  fit or count]. No result is recorded under
  this spec."

## 8. Epistemic limits (binding on all outputs)

1. **No promotion to language evidence.** This
   comparison cannot promote the fit into
   evidence that the script encodes language —
   that is exactly the over-reading the residue
   exists to prevent. Even SEPARABLE says only
   that three named non-linguistic systems fit
   worse on these measures; it does not say the
   script is writing, and no output may present
   it as doing so.
2. **No verdict change.** The claim
   `yadav_2009_arxiv_manual_001` stands strongly
   supported on its recorded test. This spec's
   outcome appends to its record as a dated
   bounded finding (the strength label of §7);
   the recorded status, the recorded exponent,
   and the claim's own falsifier text are never
   edited. Spec 053's record is likewise never
   edited: this successor stands beside it, and
   Spec 053's step-0 closure stands as recorded.
3. **Three systems are not all non-language.**
   The control set is the named set of §4 and
   nothing larger. A reader who needs "no
   non-linguistic system fits this well" needs
   a different, larger design; this one names
   its systems so its conclusion can be quoted
   exactly as far as it reaches.
4. **A new baseline, on a new corpus, in a new
   numbering.** The Indus distribution here is
   an ICIT-numbered, provenance-graded corpus
   the earlier fit never used. No output may
   quote any quantity from this spec as a
   Phase-43 quantity reproduced, confirmed, or
   corrected, as Yadav's exponent, or as a
   measurement of the V3 / Mahadevan population.
   Under limb B the population is the full ICIT
   inventory of the restricted corpus; under
   limb A it is the mapped strict set's
   distribution in ICIT space — neither is
   Spec 053's strict population, and the
   difference is stated wherever the population
   is stated.
5. **Consistency is not independence.** The
   corpus is an ICIT-lineage corpus (§10, item
   1). Nothing in this spec is an independent
   check on any ICIT-lineage result, and no
   output may describe it as one. This spec is
   not Spec 053's arm B and does not become it
   by using a different snapshot of the same
   lineage (Spec 053 §12 stands).
6. **Published counts are taken as published.**
   Each control is its source's inventory as
   the source reports it — its completeness,
   period, and counting conventions are the
   source's. The step-0 record states each
   source's conventions beside its table; a
   dispute about a source is a dispute about
   that control, recorded as such, never
   repaired by adjusting counts.
7. Negative, uninformative, grade-sensitive,
   thin, and step-0-closure outcomes are
   recorded with the same prominence as a
   separable finding.

## 9. Controls and named confounders

- **Corpus size.** Fit error and exponent move
  with N and V. The synthetic control is
  size-matched to the Indus primary token total
  (gate 0.6); every system's V and N are
  reported beside its error; and §6.2 measures
  the Indus quantities' own movement under
  halving and quartering, so a size artefact is
  visible in the record rather than asserted
  away.
- **Grade composition (this successor's named
  confounder).** The provenance audit found
  the corroborated stratum is systematically
  different material — more incomplete, more
  damaged, shorter, and concentrated in
  different artefact types than the documented
  stratum — so a fit over both strata is a fit
  over a different population, not merely a
  larger sample. That is why the primary is
  documented-only and the combined fit is a
  labelled sensitivity (§6.1), and why a
  difference between them is reported as
  grade-sensitivity and never resolved by
  choosing the fit that reads better.
- **Inventory-size mismatch across published
  systems.** N1, N2, and P1 come at their
  published sizes; NRMSE_log is a per-type
  average of log residuals, which is the
  mitigation Spec 053 recorded, and the limit
  is stated: the comparison is of fit shape
  under one rule, not of systems equated in
  size.
- **Counting conventions differ by source.**
  Each control's unit is stated at its entry
  (gate 0.6) and held fixed; no unit is
  harmonised across systems after entry,
  because harmonisation after seeing counts is
  a discretion the design does not grant.
- **The estimator could favour a shape.** That
  is what P1 tests (§5.4): if the rule cannot
  rank the set's certain writing system above
  its non-writing systems, the run says so and
  judges nothing.
- **Sign-inventory discretion (Indus side).**
  Under limb A, the inventory is the pinned
  mapping act's output, exhibited at gate 0.5
  before any fit; under limb B, it is the
  restricted corpus's own measured inventory.
  Under neither limb is a sign list chosen for
  this test after any fit exists. §6.3 reports
  the fit's movement between the strict and
  full populations where the limb makes that
  a separate fit.

## 10. Reporting obligations

Every product of an execution carries, in its
headline block, in this order:

1. **the P-F1 S3 lineage statement, verbatim:**
   "This corpus is an ICIT-lineage corpus.
   Agreement between it and the program's
   earlier ICIT-lineage layer is consistency
   within one tradition, not independent
   corroboration." A product without the
   statement does not cite the corpus (P-F1
   S3);
2. the corpus label — the Shakti corpus as
   pinned at gates 0.3–0.4 (both digests), the
   intake record it was asserted against, its
   step-0 census (full and restricted), the
   freeze's population limb and the fit
   population it defined (under limb A, the
   mapping table's digest);
3. the frozen control tables' identity: per
   system, source citation, V, N, fitted α and
   q, NRMSE_log, R²_log, and the gap Δ against
   the Indus primary error — for **every**
   system, not only decisive ones, with N3's
   replicate distribution and NEAR MISS names
   (§5.3) included;
4. the positive-control condition's outcome
   (§5.4) stated before the headline word;
5. the headline outcome word of §7, in §7's
   pre-written wording, computed on the
   primary fit;
6. the sensitivity fit of §6.1 in full,
   beside the primary, with its ordering
   against the controls and — where the
   orderings differ — the grade-sensitivity
   sentence of §6.1 rule 3; and the
   sensitivities of §6.2 and §6.3 in full
   tables;
7. the fence sentence: "This result is a
   strength label for a recorded curve fit,
   measured as a new baseline on the Shakti
   corpus. It is not evidence that the script
   encodes language, it changes no verdict,
   and it neither confirms nor corrects any
   Phase-43 quantity."

Deliverables at execution: a results JSON
(step-0 record with all pins — the intake
assertions, the censuses, the population act,
the frozen control tables and their citations,
the self-test record — per-system fits for
the primary and the sensitivity populations,
replicate distributions, sensitivities), a
report under these headline rules, the
experiment-graph node (H15/H23, registered and
verified before the run), the outcome append
in this directory — including the dated
strength-label append to the claim's record —
and the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not. Anchors
asserted byte-identical before and after.

## 11. Stop conditions and outcome classes

Execution ends in exactly one of:

- **SEPARABLE**, **NOT SEPARABLE**, or
  **COMPARISON UNINFORMATIVE** — per §5, after
  all gates pass, on the primary fit (with the
  grade-sensitivity statement of §6.1 carried
  beside the headline where it applies).
- **TOO THIN** — gate 0.7 floors fail, measured
  on the restricted set. No fit is computed.
- **SHAKTI INTAKE NOT REPRODUCED** — gate 0.3
  (P-F1 S1) or gate 0.4 (P-F1 S2).
- **STRICT MAPPING NOT PINNABLE** — gate 0.5,
  limb A only.
- **CONTROL SET FREEZE FAILED** — gate 0.6.
- **INVALID** — a §3 pin mismatches, the
  intake record does not stand as §3
  requires, the estimator self-test fails
  (gate 0.2), the anchors assertion fails,
  the freeze record states no population limb,
  any fit is shown to precede its gate, a
  product citing the corpus lacks the P-F1 S3
  lineage statement, or rows graded
  undocumented-uncorroborated enter a fit,
  count, statistic, or argument.

## 12. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§4) — integrity; estimator
   self-test; Shakti intake gates S1 and S2
   asserted against the intake record; this
   successor's own restricted census;
   the population act under the freeze's
   limb; control set entered and frozen as
   cited data; census floors measured on the
   restricted set.
3. **Primary fits** (§5) — every system under
   the one estimator frozen by Spec 053; the
   comparison rule and the positive-control
   condition applied mechanically.
4. **Sensitivities** (§6) — the grade
   sensitivity fit, subsampling, and the
   conditional full-inventory fit — none
   changing the headline.
5. **Outcome** (§10) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured.

## 13. What this spec is not

Not a re-run of Spec 053 (its record and its
closure stand), not Spec 053's arm B (the same
fit on a corpus independent of the ICIT lineage
— this corpus *is* the ICIT lineage, §8 limit
5), not a re-run of Yadav's original fit, not
a reproduction or correction of any Phase-43
quantity, not a re-adjudication of the strongly
supported verdict, not a test of whether the
script encodes language, not design D-08 (the
opening/closing-sign claim, a separate spec),
not a new corpus intake (the intake is P-F1's
and the intake record's act; this spec cites
it at step 0), and not an authorisation to
execute. It is Spec 053's control-systems
comparison, carried onto the one pinnable
Indus distribution the program now holds under
a named amendment — designed so that its
honest outcomes, including closing at its own
step 0, are written down before any system is
fitted.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
