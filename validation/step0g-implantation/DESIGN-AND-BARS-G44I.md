# G44-I validation run — design-and-bars record

**Governing draft:** `2026-10-26-spec-draft-step0g-implantation-instrument.md`
(goal files dir; SHA-256
`53b4ae9e3b00c13643057119b073a8fa14af8216101928608f66a6e2125389da`).
**Run authorized by:** the owner's word, 2026-10-26 ("Do the validation run").
**Written before any implementation**, per draft §10 step 1. Implementation
follows this record; any discrepancy between code and record is a defect in
the code. This record restates draft §§2–7 (scoring rules, split rule, quota
and budget rules, selection algorithm, caps, ledger rules, gate checks, legs,
bars, calibration checks), identifies the pinned population, and pins the
implementation-level details the draft leaves to the run (draw order,
tie-breaks, rounding), each marked **[pin]**.

**Standing position: the script is not deciphered.** The real 44 pending
anchors are never scored in this run. The designated signs are synthetic
implants, labels G44I-01…G44I-44 (main run) and G44IF-01…G44IF-44 (leg-3
arm 3B, fake background).

---

## 1. Pinned population (draft §3.1) and step 0

Spec 075 §3 construction, from pinned inputs (SHA-256 verified before use):

- Corpus: `sanitized_corpus.json` (Shakti deposit, program research notes),
  SHA-256 `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`.
- Row grades: `shakti_row_grades_2026-10-22.csv`,
  SHA-256 `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`.
- Registry v2: `canonical_sign_registry_v2.csv`,
  SHA-256 `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71` (pin check only; the construction below does not join on it).
- M77 dataset v3: `m77_sign_list.csv`, SHA-256 prefix `9c619bfe` (pin check only).

Construction: keep corpus rows whose grade is `documented-lineage`; drop
rows that are empty or all-`000`; the inscription's sequence is its symbols
with `000` removed. Population order = corpus file order after filtering.
**Step 0 target (must match exactly before anything is built): 3,045
inscriptions / 557 sign types / 11,805 tokens / 550 signs attested in
sequences of length ≥ 2.** Role totals (FIRST / MIDDLE / LAST / ONLY slot
counts by the §2 class rule) are computed from this population and printed
in the run output before implementation of the legs proceeds.

## 2. Scoring rules (draft §2, restated)

- Classes by rule from the token stream: length-1 inscription token = ONLY;
  first token = FIRST; last = LAST; any other = MIDDLE.
- A reading is a prediction pair (position class, neighbor class). The
  instrument scores pairs only.
- Profile p(s): the four-class share distribution of s's attestations in the
  **fitting population**, for every sign attested there.
- Position component of sign s under predicted class c*: share of s's
  scoring-population attestations in class c*.
- Neighbor evidence of one attestation for class c: mean, over its adjacent
  signs **that have a fitting profile**, of p(neighbor)[c]; an attestation
  with no profiled adjacent sign is not neighbor-bearing. Neighbor component
  = mean neighbor evidence for c* over s's neighbor-bearing scoring
  attestations. Solo attestations contribute to the position component only.
  A sign with no neighbor-bearing scoring attestations is NEIGHBOR-UNSCORED:
  its accuracy is its position component alone, flagged by name.
- Attestation floor: a sign is scored only with ≥ 10 scoring attestations;
  below-floor signs are filed unscored by name.
- Sign accuracy = mean of position and neighbor components (position alone
  if NEIGHBOR-UNSCORED). Batch score B = mean sign accuracy over scored
  signs.
- **Baseline (leg 1B), defined exactly:** per sign, from the fitting
  population alone — position prediction = argmax of p(s); neighbor
  prediction = argmax of the sign's mean neighbor evidence in the fitting
  population. Ties break to the first class in the order FIRST, MIDDLE,
  LAST, ONLY. Fallbacks **[pin, carried from G44-S]**: a sign with no
  fitting profile takes the corpus profile's argmax (position) and, if it
  also has no fitting neighbor evidence, the corpus profile's argmax
  (neighbor); a sign with a profile but no fitting neighbor evidence takes
  its profile's argmax as neighbor prediction. (Designated signs always
  have fitting profiles and fitting neighbor evidence by construction; the
  fallbacks bind only in leg 3, as in G44-S.)
- No scorer change from G44-S §2.1 (draft §2.2). No implantation-aware
  branch anywhere in scoring.

## 3. Split (draft §3.2)

The 3,045 inscriptions in pinned order are shuffled by the split seed and
dealt alternately: positions 0, 2, 4, … of the shuffled list to the
**fitting compilation** (1,523 inscriptions), the rest to the **scoring
compilation** (1,522). **[pin]** `random.Random(split_seed).shuffle` on the
index list; compilations keep dealt order. Real signs keep real identities
in both. Sequence overlap (scoring inscriptions whose exact sequence also
appears in the fitting compilation, overall and for length-1 separately) is
measured at the recount step on the implanted streams and reported, never
filtered; the same counts on the unimplanted streams are reported alongside
for context.

## 4. Ledger (draft §5) — draw order and pins

One stream, `random.Random(model_seed)`, consumed in exactly this order
**[pin]**:

1. For each sign G44I-01…G44I-44 in label order: position class drawn by
   `rng.choices([FIRST, MIDDLE, LAST, ONLY], weights=[0.32, 0.32, 0.32, 0.04])`.
2. ONLY cap (draft §4.7/§5): if more than 3 signs drew ONLY, the 4th and
   later ONLY draws in label order are reassigned to the remaining class
   with the fewest designated signs currently assigned, ties broken in the
   order FIRST, MIDDLE, LAST **[pin]**. Reassignments recorded.
3. For each sign in label order: concentration `a(s)` =
   `rng.uniform(0.55, 0.70)` if its final position class is ONLY, else
   `rng.uniform(0.55, 0.85)`.
4. For each sign in label order: neighbor class `d*(s)` = `rng.randrange(4)`
   (uniform over the four classes) — subject to the §4.7 eligibility
   reassignment after the census (step 8 below), applied and recorded
   before the ledger is hashed.
5. For each sign in label order: target neighbor mass `m(s)` =
   `rng.uniform(0.55, 0.85)`.
6. Quotas: for compilation in (fitting, scoring), for each sign in label
   order: `rng.randint(20, 28)` if ONLY-planted, else `rng.randint(20, 40)`.
7. Budget scaling per compilation (draft §4.3): budget =
   `floor(0.20 × compilation token count)` **[pin]**. If drawn quotas sum
   above budget: scaled_i = quota_i × budget / sum; q_i = floor(scaled_i),
   raised to 18 if below 18; then the difference budget − Σq_i is
   distributed one token at a time — added to signs in order of largest
   fractional remainder (scaled_i − floor(scaled_i)), ties by label order;
   removed from signs with q_i > 18 in order of smallest fractional
   remainder, ties by reverse label order **[pin]**. Scaled quotas are the
   ledger quotas.
8. Position cells per compilation (draft §4.4): planted cell =
   round-half-up(a(s) × quota) **[pin: round-half-up carried from
   G44-S2]**; the remaining quota − planted tokens are distributed over the
   other three classes in proportion to **that compilation's realized slot
   base shares**: ideal_c = remaining × share_c / Σ shares(others);
   cell_c = floor(ideal_c); leftover distributed one token at a time to
   the class with the largest (ideal_c − cell_c), ties by class order
   FIRST, MIDDLE, LAST, ONLY, planted class excluded **[pin]**.
9. **Feasibility record (draft §§4.3, 4.7):** per compilation, family ONLY
   cells (sum over all 44 signs of their ONLY cells) must be ≤
   min(30, 25% of that compilation's solo slots). This cap is stated in the
   draft as enforced at ledger construction; the draft names no reduction
   operation for it (unlike the §4.3 budget, which has the scaling rule
   above). If the drawn ledger breaches the cap, the run HALTS before
   implantation and reports the breach — no operation is improvised.
   Also printed: family demand per major class vs the compilation's slot
   pools (draft §4.3 margins).
10. Expected profile q(s) recorded per compilation (draft §5): q[c*] = a(s);
    remaining mass over the other three classes in proportion to the
    compilation's realized slot base shares.

Order of operations thereafter (draft §§4.6, 5): provisional fitting
profiles (unimplanted fitting compilation) → fitting implantation →
final fitting profiles → neighbor-pool census (§5 below) → eligibility
reassignments → **ledger finalized and hashed** → scoring implantation →
independent recount and gate report, hashed → legs (§7 below) only if the
gate passes.

## 5. Implantation (draft §4) and the neighbor-pool census (§4.7)

- The only operation is relabeling real tokens to a designated label.
  Nothing is created, deleted, moved, or reordered.
- Per-source-sign cap: a real sign loses at most min(30,
  floor(0.20 × its token count in that compilation)) tokens **[pin:
  floor form of "no more than 20% or 30, whichever is smaller"]**.
- Selection (draft §4.5), per compilation: signs processed in ledger
  order = descending quota (that compilation's), ties by label; cells
  in the order FIRST, MIDDLE, LAST, ONLY. Candidate pool for a cell: all
  not-yet-relabeled tokens sitting in slots of that class whose source
  sign is below cap. Ranking: ascending |candidate neighbor evidence for
  d*(s) − m(s)|, where candidate neighbor evidence is computed per §2
  from the stage's profile table (fitting implantation: provisional
  profiles; scoring implantation: final fitting profiles) against the
  token's **current** adjacent labels **[pin]**; a candidate with no
  profiled adjacent sign has no evidence and ranks after all evidenced
  candidates **[pin]**. Ties: source sign's relabeled-away count so far
  (ascending), then inscription identifier (lexicographic), then token
  index. For ONLY cells no neighbor ranking applies: candidates are
  ordered by the tie-break keys alone **[pin, from draft §4.5]**. Take
  the top cell-count candidates. If the pool is smaller than the cell,
  implantation fails at that cell: sign, cell, and pool counts are
  recorded and the run files INCOMPLETE — IMPLANTATION DEFECT (draft
  §4.5, §6). No fallback, no relaxed cap, no second attempt.
- Census (draft §4.7): for each class c, P(c) = number of **unimplanted
  scoring-compilation** attestations having at least one profiled
  adjacent sign whose neighbor evidence for c under the final fitting
  profiles is ≥ 0.55 **[pin: §2 evidence rule]**. Class c is eligible
  iff P(c) ≥ 300. A sign drawn to an ineligible class is reassigned to
  the eligible class with the largest P(c), ties in the order FIRST,
  MIDDLE, LAST, ONLY; reassignment recorded in the ledger before hashing.

## 6. Adequacy gate (draft §6) — recount by an independent auditor

The auditor is separate code that recomputes everything from the ledger
and the final streams; it shares no functions with the implantation code.
Gate report written and hashed before any scoring. Any failure →
**INCOMPLETE — IMPLANTATION DEFECT**, no legs, no verdict, no in-run
repair.

- **R1 (exact):** per sign, per compilation, realized position-class
  counts equal the ledger cells exactly. Derived print: planted class is
  the realized positional argmax for all 44 signs in each compilation.
- **R2:** for every designated sign with a scored neighbor component —
  scoring compilation: per-sign |realized mean neighbor evidence for
  d*(s) − m(s)| ≤ 0.08; family mean of signed differences within ±0.03;
  signs whose realized neighbor argmax ≠ d*(s) are named, and more than
  4 such signs fails the check. Fitting compilation: the same per-sign
  quantity against a tolerance of 0.12 (draft §6; the wider band is the
  stated price of provisional-profile ranking). Realized means and
  argmaxes are computed per §2 from the final fitting profiles.
- **R3 (exact):** per compilation — inscription count, length multiset,
  token count, role totals identical to the unimplanted compilation;
  total relabeled ≤ 20% of compilation tokens; every real sign's
  relabeled-away count within the §5 cap; family ONLY cells within the
  §4.7 cap.
- **R4:** every designated sign's scoring attestation count equals its
  ledger quota (18–40); NEIGHBOR-UNSCORED signs listed by name. (The
  G44-S ONLY ≥ 50 aggregate is not carried — draft §6 R4, named change.)

## 7. Legs and certification (draft §7) — bars unchanged

- **Leg 1:** B(planted) ≥ 0.60; ≥ 33 of 44 signs at accuracy ≥ 0.60;
  mean position component ≥ 0.55; mean neighbor component ≥ 0.45 (over
  signs with a scored neighbor component).
- **Leg 1B:** B(planted) − B(baseline) ≥ +0.05 **and** B(planted) >
  B(baseline), baseline per §2 above, identical procedure and populations.
- **Leg 2:** 9,999 permutations of the batch's own pairs (leg-2 null
  seed); B(planted) above the 95th percentile and ≤ 5% of permutations
  at or above B(planted).
- **Leg 3 calibration (printed before either arm runs):** the G44-S
  quota generator, carried exactly (tiers 4×500, 20×150, 80×40, 325×8,
  128×7 = 11,696 tokens, 557 types; deal stride 4531; length counts
  {1:244, 2:521, 3:759, 4:600, 5:380, 6:230, 7:145, 8:85, 9:52, 10:29};
  length stride 1124). Five checks: inscriptions exactly 3,045; distinct
  types exactly 557; total tokens in 11,215–12,395; most-frequent-type
  share ≥ 0.04; length-1 share in the band **[pin, carried from the
  G44-S compliance file]** 0.06–0.10 (the pinned population's solo share
  is 244/3,045 ≈ 0.0801). Any failure → neither arm runs; the run files
  INCOMPLETE with leg 3 outstanding; the generator is never tuned.
- **Arm 3A (carried from G44-S leg 3):** fake stream split [0::2] /
  [1::2] into fake fitting / fake scoring compilations; the batch is the
  44 most frequent fake signs in the fake fitting compilation (order by
  −count, then emblem id) **[pin, carried]**, each given its §2 baseline
  pair; full certification procedure including its own 9,999-permutation
  null (leg-3 null seed). Pass = the fake batch is **not certified**.
- **Arm 3B (new in the draft):** 44 fake designated signs (labels
  G44IF-01…44) implanted into the fake background by the §§4–5 mechanics
  with the draft's one deliberate substitution, pinned as follows
  **[pin]**: (i) a working ledger is drawn for the fake labels from a
  fresh `Random(model_seed)` stream in the §4 order, and the fake fitting
  compilation is implanted with it (provisional profiles = unimplanted
  fake fitting profiles); (ii) the arm's planted pairs are then **set
  to the designated signs' own baseline pairs computed on the implanted
  fake fitting compilation** — the fake background's own frequency
  summary of the implanted signs, which is what makes the certified
  batch identical in pairs to the baseline batch and its margin zero by
  construction, as the draft states; (iii) the fake scoring compilation
  is implanted targeting those pairs (cells from the working ledger's
  quotas and concentrations toward the substituted position classes;
  ranking toward the substituted neighbor classes with the drawn
  masses), ranked by the final fake fitting profiles; (iv) the full
  certification procedure runs on that batch, including a
  9,999-permutation null from a fresh `Random(leg-3 null seed)` stream.
  The §4.7 eligibility reassignment is **not** applied to substituted
  pairs (the substitution is definitional for this arm) **[pin]**. Pass
  = the batch is **not certified**. If a cell cannot be filled, the arm
  is recorded NOT RUN — IMPLANTATION FAILURE and leg 3 cannot complete.
- **Certification (draft §7.5):** VALIDATED only if legs 1, 1B, 2, and
  3 (both arms) all pass. FAILED if any leg that runs fails. INCOMPLETE
  if the §6 gate fails (INCOMPLETE — IMPLANTATION DEFECT) or leg 3
  cannot run. The verdict is this rule's output, not any auto-verdict
  string in code output.
- **OD-1 quantities (draft §8), reported with the verdict:** baseline
  full-pair agreement count with the planted pair (of 44), position-only
  and neighbor-only agreement counts, and the realized leg-1B margin.
  Leg 1B gates; OD-1 is not decided by this run.
- **K3 check (draft §9):** if the verdict is VALIDATED and baseline
  full-pair agreement ≥ 40 of 44 and the leg-1B margin ≤ 0.10, the
  verdict is recorded VALIDATED but flagged (KI-3): it does not license
  an M4 freeze without a transfer test.

## 8. Seeds (fresh; recorded before implementation)

| Purpose | Seed |
|---|---|
| Model (ledger draws; arm-3B working ledger) | 20270321 |
| Split | 20270322 |
| Leg-2 null | 20270323 |
| Leg-3 null (arms 3A and 3B permutation nulls) | 20270324 |

No predecessor seed is reused (G44: 20261026–31; G44-S: 20261201–05;
G44-S2: 20270111–17 — all spent). No seed changes after any output is
seen. Implantation and selection consume no seed (deterministic given
ledger, split, streams).

## 9. Run discipline

Standard library only. Work in this scratch directory; the protected
local checkout is not used; implanted streams stay in scratch and never
enter any repository. Stages checkpoint to disk as they complete
(population → ledger-feasibility → implantation → gate → legs), so a
platform restart loses at most one stage. Diagnostics after the verdict,
if any, are read-only on the identical streams and change no verdict.
