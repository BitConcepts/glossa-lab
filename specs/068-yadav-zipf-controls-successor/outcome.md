# Spec 068 / Phase-430 — Outcome record (EXECUTED 2026-10-22 — COMPARISON UNINFORMATIVE)

> ## EXECUTED — 2026-10-22
>
> Executed under the frozen Spec 068 contract
> (freeze digest
> `ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d`),
> as **Phase-430**, under the owner's execution
> order of 2026-10-22, given with the freeze
> rulings, after freeze PR #342 merged to `main`
> (merge commit `9bdb21d0e32a096abd87525a2dc159b7685dfd79`;
> CI run 39869769204, 7 of 7 jobs success) and
> after OSF registration **3pbwe** was filed
> (2026-10-22T23:21:54Z). The registration stood
> **pending approval** at execution; that state
> is recorded here as it stands, per freeze.md
> §7 — it is not rounded up. Outcome:
> **COMPARISON UNINFORMATIVE** — all seven
> step-0 gates passed and every system was
> fitted, but the linguistic positive control,
> Linear B, did not fit the curve strictly
> better than every non-linguistic control (it
> fitted worst of all five systems), so under
> the frozen headline rule the comparison
> cannot judge the script. The claim
> `yadav_2009_arxiv_manual_001` stands exactly
> as recorded; per the §7 wording for this
> outcome, **no strength label is added**. The
> Indus quantities below are a new baseline on
> the Shakti corpus, reported for the record.

## Headline (spec §10 block, in order)

> This corpus is an ICIT-lineage corpus.
> Agreement between it and the program's
> earlier ICIT-lineage layer is consistency
> within one tradition, not independent
> corroboration.
>
> Corpus: the Shakti corpus (restricted-local;
> corpus SHA-256
> `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`;
> row-grades SHA-256
> `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`),
> under the intake record
> `docs/decisions/2026-10-22-shakti-corpus-intake-record.md`.
> Step-0 census: 5,704 rows; 5,536 analyzable;
> grades 3,212 documented-lineage / 2,087
> undocumented-corroborated / 405
> undocumented-uncorroborated; 18,065 tokens;
> 713 distinct signs; 77 sites. Population:
> limb B (DD-068-7) — the full ICIT sign
> inventory of the restricted corpus; primary
> fit population the analyzable
> documented-lineage rows (3,045 rows, 11,805
> tokens, 557 distinct signs).
>
> | System | V | N | α | q | NRMSE_log | R²_log | gap Δ |
> |---|---|---|---|---|---|---|---|
> | Indus primary (documented-lineage) | 557 | 11,805 | 2.004 | 19.9 | 0.1584 | 0.9892 | — |
> | N1 Mesopotamian numerical signs (published proto-cuneiform counts, SFU NatLang dataset; §2) | 12 | 1,981 | 3.0 | 0.66 | 0.5335 | 0.9312 | +0.3752 |
> | N2 Heraldic charges (Dering Roll, 324 shields; §2) | 57 | 825 | 2.878 | 20.0 | 0.1839 | 0.9704 | +0.0255 |
> | N3 Synthetic emblem inventory (Yule–Simon, median of 99) | 1,181 (median) | 11,805 | 1.16 | 0.0 | 0.2405 | — | +0.0821 |
> | P1 Linear B (DAMOS transliterations; §2) | 89 | 47,292 | 3.0 | 17.45 | 0.9229 | 0.7658 | +0.7646 |
>
> N3 replicate distribution: NRMSE_log median
> 0.2405, central 90% interval [0.2035, 0.2869];
> as-well share 0.00 (no replicate fitted as
> well as the Indus primary). NEAR MISS
> (0 < Δ ≤ 0.02): **none** — the closest
> control, heraldic charges at Δ = +0.0255,
> sits above the frozen band and is not named
> one.
>
> Positive-control outcome: **NOT MET** —
> Linear B (0.9229) does not fit strictly
> better than every non-linguistic control; it
> fits worse than all three (0.5335, 0.1839,
> 0.2405). The falsifier does not fire: no
> non-linguistic control fits as well as the
> Indus primary (0.1584).
>
> **COMPARISON UNINFORMATIVE** — "The
> comparison cannot judge the script: the
> linguistic positive control, Linear B sign
> frequencies (fit error 0.9229), does not fit
> strictly better than every non-linguistic
> control (Mesopotamian numerical signs
> 0.5335; heraldic charges 0.1839; the
> synthetic emblem process, median 0.2405), so
> the measures used here do not separate the
> one certain writing system in the set from
> systems that are not writing. The Indus
> quantities on the Shakti restricted corpus
> (0.1584, exponent 2.004) are reported for
> the record as a new baseline and support no
> separability conclusion either way. The
> claim stands exactly as recorded, with no
> strength label added."
>
> Sensitivity fit (in full): documented +
> corroborated rows — V 707, N 17,216,
> α 1.96, q 20.0, NRMSE_log 0.1544,
> R²_log 0.9901. Against the same controls its
> verdict-relevant ordering is the same as the
> primary's (no control fits as well; the
> positive control does not pass), so the
> ordering does not change between the grade
> sets — the result is **not grade-sensitive**.
> Subsampling (median [central 90% interval],
> 99 replicates per level): primary halves —
> α 1.823, NRMSE_log 0.1739 [0.1589, 0.1874];
> primary quarters — α 1.632, NRMSE_log
> 0.1884 [0.1763, 0.2131]; sensitivity halves
> — α 1.793, NRMSE_log 0.1687 [0.1592,
> 0.1793]; sensitivity quarters — α 1.619,
> NRMSE_log 0.1867 [0.1703, 0.2067]. §6.3: no
> separate full-inventory fit exists under
> limb B; the primary already is that fit.
>
> This result is a strength label for a
> recorded curve fit, measured as a new
> baseline on the Shakti corpus. It is not
> evidence that the script encodes language,
> it changes no verdict, and it neither
> confirms nor corrects any Phase-43 quantity.

## 1. What was executed

The frozen contract end to end: step 0 in its
frozen order (gates 0.1–0.7), then — every gate
having passed — the Indus primary fit, the
Indus sensitivity fit, and the four control
systems under Spec 053's one frozen estimator;
the §5 comparison rule applied mechanically on
the primary fit; the §6.1 grade sensitivity
and §6.2 subsampling tables in full. The
estimator implementation of record is
Phase-413's `fit_zipf_mandelbrot`, imported
and run for gate 0.2 and as the cross-check
for every system fit: the run's vectorised
evaluation of the identical grid objective
agreed with it exactly on all five systems
(α, q, and NRMSE_log identical in the machine
record). The script is deterministic: the
record was regenerated once when the control
tables were re-issued with LF line endings,
so the committed table bytes are the bytes
the record cites (quantities and outcome
unchanged), and the final record then
reproduced byte-identically on a second full
run (results SHA-256 `ca83af8f…`, report
SHA-256 `e7597718…`; re-verified at the
landing).

## 2. Step 0, gate by gate

- **0.1 Input integrity — PASS.** Every §3 pin
  recomputed to its freeze-record value: the
  claim file at its DD-068-8 re-pinned hash
  (`ec31778a…`), the anchors file
  (`df0cf620…`; census 287 anchors, 94
  `strict_sa_independent`), the crosswalk
  (`4ace1a61…`), the intake record
  (`bd14e2b1…`, standing as §3 requires with
  both pins, gates S1–S4, and the census), the
  Spec 068 freeze digest (`ab890859…`), and
  Spec 053's freeze digest (`fd2d5cb8…`).
- **0.2 Estimator self-test — PASS.** Planted
  α 1.20, q 2.0 (V 200, N 50,000, seed
  20261021) recovered as α 1.256 (error 0.056,
  tolerance 0.10) and q 2.72 (error 0.72,
  tolerance 1.0), by Phase-413's own functions.
- **0.3 Shakti identity (S1) — PASS.** Both
  restricted-local files recompute to the
  intake record's pins (corpus `345241b1…`;
  row grades `02394241…`).
- **0.4 Census (S2) + restricted census —
  PASS.** The audit census reproduces exactly
  (5,704 rows; 5,536 analyzable; grades 3,212
  / 2,087 / 405; 4,904 of 5,536 analyzable
  rows (88.6%) carrying a CISI identifier;
  18,065 tokens; 713 distinct signs; 77
  sites). This successor's own census, which
  governs: primary 3,212 rows, 3,045
  analyzable, 11,805 tokens, 557 distinct
  signs; sensitivity 5,299 rows, 5,131
  analyzable, 17,216 tokens, 707 distinct
  signs — the draft's derived expectations
  confirmed by measurement.
- **0.5 Population act — PASS.** Limb B
  re-read from the freeze record: the
  populations are the full ICIT sign inventory
  of the restricted corpus, as stated in the
  machine record; no mapping act was
  performed and neither population is
  described as a strict population.
- **0.6 Control set freeze — PASS.** The four
  systems were entered whole as cited data
  from the committed tables in
  `specs/068-yadav-zipf-controls-successor/data/`,
  before any fit: N1 table SHA-256
  `0f938c19…` (12 types, 1,981 tokens); N2
  charges table `0c618df4…` (57 types, 825
  tokens) with its blazon transcription
  `c40dc7aa…` and per-shield extraction
  record `c9244160…` (every shield's
  extraction read against its blazon at the
  table's freeze, 324 of 324; 35 shields bear
  no charge, field only, and are named in the
  extraction record); P1 table `895a1ebf…`
  (89 types, 47,292 tokens); N3 generated
  under its frozen parameters at fit time.
  Two builder's notes are recorded openly:
  (a) N1's entered table is the whole
  numerical-sign layer of the cited published
  derivation — thin relative to the full
  archaic corpus, as its citation in the
  machine record states; the two
  indeterminate-multiplicity groups were
  excluded because counting them would
  fabricate a count. (b) The pre-freeze
  research expectation for P1 (V 88,
  N ≈ 22,000) did not reproduce under the
  documented parse of the same source: the
  entered table is the source's whole
  syllabogram inventory under the counting
  rule stated in its citation (the 72 attested
  syllabary values plus 17 untransliterated
  *NN types with NN < 100, including *89 and
  *92), V 89, N 47,292. The measured table
  governs; the expectation was never a pin.
- **0.7 Census floors — PASS.** Primary:
  557 distinct types (floor 50) and 11,805
  tokens (floor 2,000).

## 3. The comparison (spec §5, applied mechanically)

No non-linguistic control fits as well as the
Indus primary (ε = 0): N1 gap +0.3752, N2 gap
+0.0255, N3 gap +0.0821 (median; as-well
share 0.00). **The falsifier does not fire.**
The positive-control condition requires
Linear B to fit strictly better than every
non-linguistic control; at 0.9229 it fits
worse than all of them. **The condition fails,
so the headline is COMPARISON UNINFORMATIVE**
regardless of the falsifier — the frozen
§5.5 mapping. In plain words: on this
estimator, the one certain writing system in
the set produces the *worst* Zipf–Mandelbrot
fit of the five systems, so a good Indus fit
on these measures cannot be read as sitting
with writing and apart from non-writing. The
Indus numbers stand as a new baseline for the
record — α 2.004 and NRMSE_log 0.1584 on the
documented-lineage population, α 1.96 and
0.1544 on the wider grade set — and no
verdict-relevant conclusion is drawn from
them in either direction.

## 4. Claim consequences (register F068-C01…C14)

- The outcome attaches to
  `yadav_2009_arxiv_manual_001` as this dated
  outcome record in the spec's directory. Per
  the §7 COMPARISON UNINFORMATIVE wording —
  "The claim stands exactly as recorded, with
  no strength label added" — no append is made
  to the claim's own record and no field of it
  changes: status strongly supported and stage
  explained stand untouched, exactly as
  F068-C03 froze them.
- F068-C04's proposition (every named
  non-linguistic control fits strictly worse
  than the Indus primary) is what the run
  measured to be true on this corpus — and it
  earns no headline, because F068-C10's
  headline is assigned by the §5 rule whole,
  and the positive-control limb of that rule
  failed. Both facts are recorded; neither is
  rounded into the other.
- No Spec 053 record, no intake gate, and no
  anchor moved: anchors asserted byte-identical
  before and after (`df0cf620…` at both
  readings).

## 5. What this outcome does not establish

- It does not establish that the script
  encodes language, and it does not establish
  the opposite: the comparison is
  uninformative by the contract's own rule,
  so it is evidence for neither reading of the
  Indus fit.
- It does not confirm or correct the Phase-43
  exponent (~1.35): no Phase-43 quantity was
  an input, and the new baseline's exponent
  (2.004) is reported on its own, never beside
  it as a reproduction or a correction.
- It does not show that Linear B is not
  writing (it is the set's certain writing
  system); it shows that this estimator, on
  these published counts, ranks its curve fit
  last — a statement about the measure's
  resolution on these tables, which is
  precisely what the positive control exists
  to test.
- It does not rehabilitate limb A: no strict
  set was fitted, and nothing here bears on
  whether one could be pinned from another
  source.
- Foundation check (H21), reported as
  measured on the execution tree: **40 checks
  passed, 0 failed, 8 warnings**.

## Landing record (appended at merge; append-only)

- Execution PR: *(recorded at the landing —
  appended below at merge).*

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
