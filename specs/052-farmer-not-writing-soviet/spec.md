# Spec 052 — Farmer's "Not Writing at All" Thesis: the Soviet-Compilation Consistency Check (Design D-01, Arm A Only)

> ## FROZEN — 2026-10-23
>
> Frozen at the freeze act of 2026-10-23 under
> the owner's mini-gate approval of the same
> day (2026-10-23, 22:59 EDT, "Approve both
> mini-gates as specified"; recorded in
> `adjudication.md` §10). This spec is frozen
> **as amended**: the amendment
> (`amendment.md` — battery NB-1 on the Shakti
> corpus layer, amended step-0 gates A–D,
> re-pointed outcome semantics) governs
> wherever it and the unamended draft disagree.
> As drafted (design D-01, arm A only, the
> Soviet-compilation consistency check), this
> spec's freeze attempt of 2026-10-21 failed
> at gate 0.5 (BATTERY NOT PINNABLE), and arm A
> as designed was closed by the owner's
> rulings of 2026-10-23 (`adjudication.md`
> §§8–9); the unamended text below stands as
> the record of that design and is not
> rewritten.
>
> The AEE lifecycle hooks ran first, at the
> freeze gate (tasks L4, per DD-038-10):
> after_specify, after_plan and after_tasks
> over the claim register, which was recovered
> in three rounds at the freeze (0.5-draft →
> 0.8-draft) before the freeze digest was
> computed over it exactly once. Pins, the
> freeze-stage exhibits, and the machine
> record are in `freeze.md` / `freeze.json`.
> The OSF registration for the frozen spec was
> filed at the freeze
> (`osf-spec-registration.md`). This freeze
> executes nothing: execution requires a
> separate owner order.
>
> The execution phase number is **Phase-437**,
> allocated at this freeze act from the merged
> record as it stands (DD-052-6; the highest
> phase report on main at the freeze was
> Phase-436, Spec 073).

**Design source:** D-01 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
§D-01, read in full at this draft).

**Claims under test:** the parent claim
`farmer_sproat_witzel_2004_manual_001`
(SETTLED — contradicted), and its three
restatement fragments
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001`,
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002`,
and
`without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001`
(each SETTLED as a restatement of the parent
proposition).

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

Farmer, Sproat and Witzel's thesis is that the
Indus signs do not encode spoken language at
all — that the script is "not writing at all,"
a set of non-linguistic emblems. The parent
claim stands **contradicted** on three items
of evidence, as its record states
(`glossa-indus/claims/extracted_claims/farmer_sproat_witzel_2004.json`,
SHA-256 `c4cf441f…`, read at this draft):

1. **Published conditional entropy** (Rao and
   colleagues, 2009): how predictable each sign
   is from the signs before it falls in the
   range seen for real language writing. This
   item was produced entirely outside this
   program, and specialists still debate it.
2. **The Phase-43 positional battery's
   word-ending-like signs:** 20 signs classed
   TERMINAL_STRONG — they sit at the ends of
   texts the way word endings do.
3. **The Phase-43 battery's fixed two-sign
   opening formula:** the pair [M77/267][M77/99]
   recurring at inscription starts (recorded in
   `outputs/phase43_all.json` §T2_3 as the top
   candidate pair: bigram count 251, dominance
   0.74, first-sign initial rate 0.806).

Items 2 and 3 — two of the three — were
produced by this program, on corpora from one
lineage (Mahadevan/ICIT). The claim's own
not-understood text names the residue exactly:
the same positional check on a genuinely
independent corpus. The three fragment records
carry no separate substance — they restate
this claim — so this design is their residue
design too. Their bookkeeping disposition
(carry-over, own record, or retirement) is a
record act, not an experiment, and is handled
outside this spec (design D-01; §4.2 below).

### 1.1 The question, in plain words

Does a compilation of the inscriptions built
outside the Mahadevan/ICIT lineage — the
Soviet compilation, held by the program as the
Phase-121 dataset — show the same
grammar-like habits the in-lineage battery
found: signs that prefer the ends of texts,
and a fixed pair that opens them? Arm A is a
**consistency check, not a verdict machine**
(design D-01's own words): the Soviet material
is small, and its outcome narrows or widens
the stated caveat on a settled claim. It does
not re-open the verdict on its own.

### 1.2 The hypothesis and its falsifier (stated before any method)

**Hypothesis.** If the signs are a
non-linguistic emblem set, then on a corpus
compiled independently of the Mahadevan/ICIT
lineage, sign behaviour should look
emblem-like: no stable set of signs should
prefer text-final position the way word
endings do, and no fixed opening formula
should recur above chance.

**Falsifier.** The hypothesis — and with it
the residue of doubt about the contradicted
verdict — fails if the Soviet compilation
shows the same grammar-like habits: a
final-position sign set and an opening formula
at strengths comparable to the in-lineage
results, under the criteria fixed in §4.1.
In the campaign plan's one line: *the frozen
Phase-43 positional battery, run on the held
Soviet records, returns the structure writing
predicts.*

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

### 2.1 The Soviet dataset (Phase-121) — the arm A data

| Input | Pin / state |
|---|---|
| Combined dataset (`data/soviet_positional/phase121_soviet_positional_dataset.json`) | SHA-256 `8eaf2bd9bace434e9e794506517165d10fa1f986253b9aae443e46513ad51df6` (recomputed at this draft from `main`) |
| K1965-T1 (`data/soviet_positional/kondratov1965_table1_new_sign_emergence.csv`, 56 records) | SHA-256 `1dc48527c37ff368eaac44c03a26469640bd055e45c3ef163160eac466eb0ba1` |
| K1965-T2 (`data/soviet_positional/kondratov1965_table2_sign_classes.csv`, 11 records) | SHA-256 `e74fe647c920787df519a8eff1213cbf077e3b98cc4d820d684853c08abf95ad` |
| K1965-T3 (`data/soviet_positional/kondratov1965_table3_polygrams.csv`, 21 records) | SHA-256 `c08b7028a4064b69f74e69c26ba3e523a2dce1d9f6ac7b93906d6bd25ccc8c76` |
| K1965-T4 (`data/soviet_positional/kondratov1965_table4_stable_initials_finals.csv`, 9 records) | SHA-256 `e2933bf0b36c9db90de2eddac083c215a0e9c6e98dd9f4c580d359da68443f1f` |
| PI73-V1 (`data/soviet_positional/protoindica1973_volchok_yuga_festivals.csv`, 4 records) | SHA-256 `4e429b3d8d20cc82e205a01af783b61d003316eaa6ef8b85ed948fcd976b7fe4` |
| PI73-V2 (`data/soviet_positional/protoindica1973_volchok_divine_units.csv`, 3 records) | SHA-256 `c72ecaebcd6b6be0f06189dee9beb53348c061f25f8b50e89018e5828c3f639c` |
| PI73-V3 (`data/soviet_positional/protoindica1973_volchok_yuga_durations.csv`, 5 records) | SHA-256 `dd9371b06dcf6ae9d27a2192259562a83ab225d556f6a2c373d2038826835d2e` |
| Phase-121 results (`reports/phase121_soviet_positional_results.json`) | SHA-256 `d1d4f19fc4ad16af88bb58a9817ecb7c2752c766e6f399a93c729deab2c52399` (total_records 109; provenance_gaps []) |
| Phase-121 extraction memo (`reports/phase121_soviet_positional_dataset.md`) | SHA-256 `58bc887f54dd318759038dd94872f76849ebb8a0957d534ea05eb0ae602a88e1` |
| Dataset loader / validator (`backend/glossa_lab/soviet_positional.py`) | SHA-256 `e4438e1dd13710e6dc555f582e3bc40e135b844d0b4c501c054c28e978a00e67` |
| Validation run (`backend/scripts/phase121_soviet_positional.py`) | SHA-256 `75572a4b778b1ec6e133dec7dbeefd52442489bad8f77ba48271b949640a5414` |

The dataset as held, stated precisely (the
memo is the record): **109 records across
seven printed tables** extracted from the
Soviet reports (Zide & Zvelebil (eds) 1976,
translating Kondratov 1965 and the 1968 brief
report; and *Proto-Indica* 1973). Hand
verification was a **36-cell sample** across
all seven tables, re-read by eye from the
rendered pages: **36 of 36 cells matched the
printed page**. The design's compressed phrase
"36 of 36 hand-verified" is that sample, not a
cell-by-cell verification of all 109 records;
this draft states the precise version
(DD-052-4).

The tables are not alike, and the difference
is load-bearing for §3:

- **K1965-T4 is the only per-sign positional
  table**: 8 data rows of stable-initial sign
  pairs (Marshall numbers; initials 99, 160,
  232, 233 with second elements 118, 500, 501,
  507) against stable finals (66, 68, 87, 96,
  97, 124, and the pair-final headed "87—"),
  cells giving absolute frequencies, plus the
  printed Total row as the 9th record. Its
  cells sum to a computed grand total of 160
  against a printed grand total of 171 — a
  printed anomaly, extracted as printed and
  never repaired.
- K1965-T1 (new-sign emergence), T2 (sign
  classes) and T3 (polygrams) are **aggregate**
  tables: they name no individual sign's
  position.
- PI73-V1–V3 are **calendrical** tables
  (Volchok's yuga material): non-sign,
  non-positional, extracted for completeness.

### 2.2 The frozen Phase-43 battery — the test of record

| Input | Pin / state |
|---|---|
| Phase-43 results of record (`outputs/phase43_all.json`) | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (recomputed at this draft from `main`) |
| Corpus-v3 loader (`backend/glossa_lab/data/indus_corpus_v3.py`) — the loader of the corpus the battery ran on | SHA-256 `3e86c934db136ba12c7370c2696573c27b7ec0fc924f231d285360fa7346846b` |

Recorded battery quantities, read at this
draft from the pinned results file: the
battery ran on 3,137 sequences (3,916
Firestore records; 12,494 sign instances);
201 signs profiled; **terminal_strong_count
20, terminal_moderate_count 10,
initial_strong_count 40, medial_strong_count
61** (§T2_2); the ten listed TERMINAL_STRONG
signs carry final-position rates from 0.683
to 0.892 with totals from 22 to 1,318; the
§T2_3 opening-formula candidate pair is
(267, 99) with bigram count 251 and dominance
0.74.

**A defect this draft records rather than
repairs (see adjudication §6, defect 1):**
there is **no executable Phase-43 battery in
the repository on `main`** — no phase-43 code
file exists; the battery survives as its
results file and as the corpus-v3 loader
(whose underlying Firestore dump file is not
in the repository tree). The battery's
position rules, count floors, final-position
strength threshold, opening-formula
definition, and chance-baseline method are
**not stated numerically in the results
file**. §3 gate 0.5 therefore makes the
freeze — not the execution, and not this
draft — produce a battery definition derived
solely from the Phase-43 record, and closes
this spec at step 0 if any element cannot be
derived without inventing it. This draft does
not invent the missing numbers.

### 2.3 The crosswalk (compilation-disagreement control)

| Input | Pin / state |
|---|---|
| Crosswalk v1 (`data/crosswalks/parpola_mahadevan_crosswalk_v1.csv`) | SHA-256 `3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823` |
| Crosswalk v1, JSON form (`data/crosswalks/parpola_mahadevan_crosswalk_v1.json`) | SHA-256 `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb` |
| Phase-122 results (`reports/phase122_crosswalk_mayig_results.json`) | SHA-256 `b77fcf492f17c792e8984ea18ec289fe28ea3b2a744dca4a470af4a2a00d3e29` (762 pairs; 383 conflict pairs across 209 Parpola signs) |

Design D-01's control: the Soviet
compilation's sign identities pass through
the program's crosswalk, and
crosswalk-conflict pairs (383 of 762) are
reported separately, never silently dropped.

## 3. Step 0 — gates before any positional quantity (fail-closed)

Execution runs these checks in order, before
any final-position or initial-position rate is
computed. A failure stops the execution in the
class named; nothing is repaired at run time.

- **0.1 Soviet-records pin.** Every §2.1 input
  hashes to its freeze-record value, and the
  seven CSV row counts reproduce the recorded
  per-table counts (56 / 11 / 21 / 9 / 4 / 3 /
  5; total 109). A mismatch stops the run as
  **INVALID**.
- **0.2 Battery pin.** `outputs/phase43_all.json`
  hashes to its freeze-record value, and its
  recorded profile counts read back exactly
  (201 profiled; 20 terminal-strong; 40
  initial-strong; the (267, 99) candidate at
  bigram count 251, dominance 0.74). A mismatch
  stops the run as **INVALID**.
- **0.3 Provenance and anomalies.** The
  loader's provenance check returns no gaps
  (every record traces to source, printed page
  and table id, as recorded), and the printed
  anomalies are present **as printed**: the
  K1965-T3 disagreements and the K1965-T4
  column disagreements (finals 87, 124, 66;
  computed grand total 160 vs printed 171).
  An anomaly "repaired," reconciled, or absent
  stops the run as **INVALID** — the dataset
  of record is the printed one.
- **0.4 Dataset-form census.** The census
  reports, and publishes with the outcome
  either way: (a) all 109 records by table;
  (b) the records carrying per-sign positional
  information (on the record as held: the 8
  K1965-T4 data rows); (c) the count produced
  by applying the design's TOO THIN wording —
  records carrying texts of three or more
  signs — under the record-to-battery-input
  mapping the freeze froze under gate 0.5.
  If gate 0.5 froze no such mapping, the
  execution does not reach this gate (it has
  already closed under gate 0.5).
- **0.5 Battery definition (freeze-produced;
  verified here).** Before any run, the
  freeze act must have produced and frozen a
  battery definition stating, each derived
  solely from the Phase-43 record and cited
  to it: the position rules; the count floors;
  the numeric final-position strength
  threshold; the opening formula's definition
  (which pair, counted how); the chance
  baseline's method; and the exact mapping
  from the held Soviet records to battery
  inputs (including how K1965-T4's aggregated
  pair × final counts enter, and how
  crosswalk-conflict pairs are separated).
  Execution verifies the frozen definition is
  complete against this list. **Any element
  that cannot be derived from the record
  without inventing it closes the execution
  at this gate as CLOSED AT STEP 0 — BATTERY
  NOT PINNABLE**, with the missing element
  named. No element is supplied at run time,
  and no threshold is adjusted after seeing
  the Soviet data (design D-01, method).
- **0.6 TOO THIN gate.** If the gate-0.4(c)
  count is **fewer than 30**, the execution
  closes as **TOO THIN** (design D-01,
  criteria fixed in advance). The counts are
  reported either way. No positional quantity
  is computed past a failed gate.

## 4. The primary test (arm A)

The battery, exactly as frozen by gate 0.5's
definition — the same position rules, count
floors, and strength thresholds as the
Phase-43 battery that produced the in-lineage
result, with **no threshold adjusted after
seeing the data** — runs on the Soviet
dataset as mapped by that definition. The run
reports, **per sign, final-position and
initial-position rates with counts** (design
D-01, method). Crosswalk-conflict pairs are
reported separately, never silently dropped.
Exact counts are published with every rate
(the small-sample control, design D-01).
**No conditional-entropy computation is part
of arm A**: entropy enters design D-01 only in
arm B, which is not in this spec (§11).

### 4.1 Outcome mapping (fixed in advance)

Let **F** = at least one sign clears the
frozen final-position strength threshold, and
**O** = the two-sign opening formula recurs
above the battery's frozen chance baseline.

- **CONSISTENT** — F and O both hold. (Design
  D-01's criterion, verbatim in substance.)
- **INCONSISTENT** — neither F nor O holds.
  (Design D-01's criterion, verbatim in
  substance.)
- **PARTIAL** — exactly one of F, O holds.
  The design names no word for this case; the
  draft adds PARTIAL so the outcome set is
  complete before any run, and records the
  addition openly as DD-052-3 for the freeze
  to confirm or replace.
- **TOO THIN** — closed at gate 0.6.

INVALID, CLOSED AT STEP 0 — BATTERY NOT
PINNABLE, and NOT ADJUDICATED (§9) are stop
classes, not outcomes of the test.

### 4.2 The three fragments — handling under every outcome

The fragments
(`…_critique_0001`, `…_critique_0002`,
`without_kings…_language_0001`) restate the
parent proposition and carry no separate
substance (design D-01). Accordingly, under
**every** outcome class of this spec —
CONSISTENT, INCONSISTENT, PARTIAL, TOO THIN,
and every stop class:

1. the outcome is appended, as a dated entry,
   to the parent claim's record **and** to
   each fragment's record, in the same words,
   naming the outcome class and this spec;
2. no fragment receives a separate test, a
   separate verdict, or a separate caveat:
   the arm A result is a result about the one
   shared proposition;
3. each fragment's SETTLED-as-restatement
   status is **unchanged** by arm A, exactly
   as the parent's contradicted verdict is
   unchanged (§7, limit 1);
4. the fragments' bookkeeping disposition —
   carry-over, own record, or retirement — is
   **not decided by this spec**: the design
   assigns it to a record act outside the
   experiment, and this spec neither performs
   nor pre-judges that act.

### 4.3 Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- CONSISTENT: "Run on the Soviet compilation
  held by the program (109 records, Phase-121),
  the frozen Phase-43 positional battery
  returns the structure writing predicts:
  [k] sign(s) clear the frozen final-position
  threshold ([signs, rates, counts]) and the
  two-sign opening formula recurs above the
  battery's chance baseline ([formula, count,
  baseline]). The result is CONSISTENT with
  the in-lineage positional findings. It
  narrows the 'within-lineage only' caveat on
  the parent claim; the claim's contradicted
  verdict stands as recorded, and this arm
  re-opens nothing."
- INCONSISTENT: "Run on the Soviet compilation
  held by the program (109 records, Phase-121),
  the frozen Phase-43 positional battery
  returns neither of the structures writing
  predicts: no sign clears the frozen
  final-position threshold and the two-sign
  opening formula does not recur above the
  battery's chance baseline ([counts]). The
  result is INCONSISTENT with the in-lineage
  positional findings and widens the stated
  caveat on the parent claim: the positional
  evidence against the 'not writing' thesis
  now stands on one lineage only, stated more
  strongly than before. The claim's
  contradicted verdict stands as recorded —
  the published entropy item is untouched by
  this arm — and re-opening it is a formal
  act this result does not perform."
- PARTIAL: "Run on the Soviet compilation
  held by the program (109 records, Phase-121),
  the frozen Phase-43 positional battery
  returns one of the two structures writing
  predicts and not the other: [the half that
  appeared, with signs, rates and counts] is
  present; [the half that did not] is not.
  The result is PARTIAL. It neither retires
  nor widens the 'within-lineage only' caveat
  as a whole; the caveat is restated for the
  half that was tested, in the outcome record.
  The claim's contradicted verdict stands as
  recorded."
- TOO THIN: "The Soviet arm cannot carry the
  consistency check as designed: fewer than
  30 records carry texts of three or more
  signs under the frozen mapping ([census]).
  No positional quantity was computed. The
  'within-lineage only' caveat on the parent
  claim stands exactly as recorded, and arm A
  is recorded as TOO THIN, not as evidence in
  either direction."
- INVALID: "Spec 052 closed at step 0 as
  INVALID: [the failed gate and the observed
  values]. No positional quantity was
  computed, and nothing in this closure is
  evidence about the parent claim in either
  direction."
- CLOSED AT STEP 0 — BATTERY NOT PINNABLE:
  "Spec 052 closed at step 0: the frozen
  Phase-43 battery cannot be pinned from its
  record without inventing [the named
  element]. The battery survives on `main` as
  a results file, not as an executable with
  stated rules. No positional quantity was
  computed. Arm A queues as a successor
  design question; it is not repaired inside
  this spec."
- NOT ADJUDICATED: "Spec 052 is NOT
  ADJUDICATED: the battery's frozen chance
  baseline could not be computed as frozen
  ([the failure]). No outcome word is
  attached to the parent claim."

## 5. Controls and named confounders

- **Compilation disagreement (Phase-125).**
  The Soviet compilation's sign identities
  pass through the program's crosswalk;
  crosswalk-conflict pairs (383 of 762,
  Phase-122 record) are reported separately,
  never silently dropped (design D-01).
- **Small-sample noise.** Exact counts are
  published with every rate; no rate is quoted
  without its count (design D-01).
- **Printed anomalies.** The Soviet tables
  disagree with themselves in print
  (K1965-T3; K1965-T4's totals). The dataset
  of record carries the values as printed;
  gate 0.3 asserts they were not reconciled
  away, and every outcome product names the
  T4 totals disagreement (computed 160 vs
  printed 171) wherever T4 counts are used.
- **Numbering.** K1965-T4's signs are in
  Marshall numbers (the memo's record). Any
  passage from Marshall numbering to the
  battery's Mahadevan numbering is part of
  gate 0.5's frozen mapping, stated there or
  the spec closes at that gate — it is never
  improvised at run time.
- **The entropy debate itself** is not a
  confounder arm A can engage: arm A computes
  no entropy (design D-01 assigns entropy to
  arm B). No output may present arm A as
  bearing on the entropy item.

## 6. Reporting obligations

Every product of an execution carries, in its
headline paragraph:

1. the dataset label — the Soviet positional
   dataset (Phase-121; 109 records, seven
   printed tables), with its lineage posture
   as recorded: a compilation built outside
   the Mahadevan/ICIT lineage;
2. the gate-0.4 census (all three counts);
3. per sign: final-position and
   initial-position rates **with counts**;
4. the crosswalk-conflict pairs' report,
   separately from the clean pairs;
5. the outcome word of §4.1 (or the stop class
   of §9), and the §4.2 fragment appends.

Deliverables at execution: a results JSON
(census, per-sign rates and counts, formula
count against its baseline, conflict-pair
report, gate verdicts), a report under these
headline rules, the experiment-graph node
(H15/H23, registered and verified before the
run), the outcome append in this directory,
the dated appends to the parent claim's and
the three fragments' records (§4.2), and the
LEDGER entry (H1). Foundation check (H21)
after the execution phase: 0 failures, or the
outcome record says why not. Anchors asserted
byte-identical before and after — this spec
moves no anchor.

## 7. Epistemic limits (binding on all outputs)

1. **No verdict moves.** Arm A narrows or
   widens the stated caveat on a SETTLED
   claim; it does not re-open, confirm, or
   flip the parent claim's contradicted
   verdict, on its own (design D-01). A
   re-opening, if any future record argues
   for one, is a separate formal act.
2. **Consistency is not replication of the
   whole case.** Even a clean CONSISTENT
   shows grammar-like *behaviour* on this
   compilation — not what language the signs
   encode, not any sign's reading, and not
   that every part of the sign system is
   linguistic (design D-01).
3. **The Soviet material is small and
   aggregated.** 109 printed-table records —
   of which one table carries per-sign
   positional counts — cannot carry the full
   claim. That is why the design's own outcome
   words are consistency words, and no output
   may upgrade them.
4. **No entropy statement.** Arm A says
   nothing about conditional entropy, for or
   against the published result or its
   critics.
5. Negative, partial, thin, and
   not-adjudicated outcomes publish with the
   same prominence as a consistent one.

## 8. Risks and honest weaknesses

- **The battery is a record, not a program**
  (§2.2). This is the design's largest
  exposure: if the freeze cannot derive the
  battery definition from the record, arm A
  closes at gate 0.5 without running. The
  draft prices that in rather than hiding it.
- **The dataset's unit is the printed table
  row, not the inscription text.** The
  design's TOO THIN criterion is worded for
  texts; applying it to the held form depends
  on gate 0.5's frozen mapping. If no honest
  mapping exists, the closure is gate 0.5's,
  stated as such — not a silent redefinition
  of "record."
- **K1965-T4 is thin and internally
  inconsistent in print** (160 vs 171). Its
  counts are the only per-sign positional
  material the compilation offers this test.
- **The opening formula's in-lineage form is
  one pair.** Whether the Soviet compilation
  should be asked for that same pair, or for
  any fixed pair under the battery's rules,
  is a battery-definition question for gate
  0.5 — decided there, from the record,
  before any Soviet count exists.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **CONSISTENT**, **INCONSISTENT**, or
  **PARTIAL** — per §4.1, after all gates pass.
- **TOO THIN** — gate 0.6 fails. No positional
  quantity is computed.
- **INVALID** — a §2 pin mismatches (0.1,
  0.2), the population does not reproduce
  (0.1), or provenance / anomalies fail (0.3).
- **CLOSED AT STEP 0 — BATTERY NOT PINNABLE**
  — gate 0.5's definition is incomplete
  against its own list.
- **NOT ADJUDICATED** — the frozen chance
  baseline cannot be computed as frozen at
  the primary.

## 10. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — pins, provenance and
   anomalies, battery-definition verification,
   dataset-form census, TOO THIN gate.
3. **Primary** (§4) — the frozen battery on
   the mapped Soviet inputs; per-sign rates
   with counts; conflict pairs separately.
4. **Outcome** (§6) — appended records only,
   including the §4.2 appends to the parent
   and fragment records; anchors asserted
   byte-identical; foundation check reported
   as measured.

## 11. What this spec is not

Not arm B. Arm B — the identical battery plus
a conditional-entropy computation on a
genuinely independent full corpus — is
**trigger-armed and not a member of this
campaign pass** (campaign decision E-3): if
its trigger fires, it queues for a mini
planning gate; it never auto-joins, and this
spec neither designs nor authorises arm B's
execution (DD-052-1). Not an entropy test.
Not a PRED evaluation: Spec 020 adjudicated
this dataset as a source for PRED-2026-001/002
and this spec scores no prediction and
revisits no part of that adjudication. Not a
decipherment, not a sign-reading, and not an
authorisation to execute. It is the
Soviet-compilation consistency check of one
settled claim, designed so that its honest
outcomes — including closing at its own
gates — are written down before any rate is
computed.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
