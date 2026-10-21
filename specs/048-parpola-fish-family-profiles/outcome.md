# Spec 048 / Phase-408 — Outcome record (EXECUTED 2026-10-21 — STRICT CORPUS NOT PINNABLE, gate 0.3)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 048 contract
> (freeze digest
> `56beec70957ac64e5f17e3bb889e66c9becfe7a7a55b49bc59e5a232c642a846`),
> as **Phase-408**, in Wave 3 Group 3 of the
> runnable-experiments campaign (plan approved
> AS WRITTEN on 2026-10-21). The execution gate
> was satisfied before the run: OSF registration
> **eqpab** is APPROVED + PUBLIC (DOI
> 10.17605/OSF.IO/EQPAB). Outcome: **STRICT
> CORPUS NOT PINNABLE** — gate 0.3 (strict
> corpus identification, pin, and measure
> reproduction) failed on observed values.
> Gates 0.1 and 0.2 passed in full. No
> ending-follower rate was computed for any
> sign, no census exists, no control was
> entered, and the claim stands exactly as
> recorded.
>
> **This record is internal under the campaign's
> Roif gate (R-7); it is not a publication.**

## Headline (spec §6 wording, STRICT CORPUS NOT PINNABLE form)

"Spec 048 closed at step 0, gate 0.3: the
strict corpus layer of record could not be
uniquely identified and pinned, or the pinned
layer does not reproduce the Phase-43 T2.4
reference points (the V3 / Mahadevan-lineage
layer's data file — the Firestore 'indusarrays'
dump the V3 loader reads — is absent from the
tree, so the loader loads zero sequences and
the layer cannot be exported whole or pinned;
no database copy exists in the execution tree;
and no other layer in the tree is the corpus
the Phase-43 record names (its source at 3,916
records, against 5,679 records for the
site-attributed layer, 15,508 mixed-source
objects for the V1 export, and 3,085
ICIT-encoded sequences), so the T2.4 reference
points (sign 72 — 181 occurrences,
ending-follower fraction 25.9%; sign 267 — 356
occurrences, 3.8%) cannot be re-derived from a
pinned layer). No ending-follower rate was
computed. This closure is a statement about
runnability, not about the claim; the claim
stands exactly as recorded."

Claim:
`parpola_2010_dravidian_solution_manual_002`
— "The fish sign (meen in Dravidian) is the
primary rebus sign in the Indus script" —
standing **IN QUESTION, partially supported**,
unchanged: Mahadevan sign 72 passed its
Phase-43 T2.4 positional test; sign 267, the
family's most frequent member, failed it. Its
record was not edited and no dated append was
made to it (see §5, F048-C02). The §9 headline
quantities that a completed run would carry —
the pinned corpus labels and digests for both
arms, the per-member tables for both arms, the
token-weighted family rates and passing
shares, the control figures, and the 72/64/70
sensitivity — do not exist under this spec,
and this record says so rather than supplying
substitutes. The Roif-hold sentence is carried
as §9 requires: "This record is internal under
the campaign's Roif gate (R-7); it is not a
publication."

## 1. What was executed

Step 0 only (spec §3, gates in frozen order),
under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase408_fish_family_step0.py`;
graph module
`backend/glossa_lab/experiment_graph_phase408.py`
(node `IndusPhase408FishFamilyStep0`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`, 497 nodes total).
The script contains the step-0 gate machinery
only — the digest assertion under Spec 044
§4.2's exclusion rule, the join, and the gate
0.3 identification attempt — and no T2.4 rate
computation, no census, and no control code,
because a gate 0.3 failure closes the execution
before any of those can run, by the frozen
design. The run's own records:
`reports/phase408_results.json` (SHA-256
`c08e775c7f70af0b95dc1e059a4116c65c5d37f0653d6eec06df198c505ef6f3`)
and `reports/phase408_step0_report.md` (SHA-256
`9dca830c4c281b65df7494acea5b3c65600bcfc31135f10d5627bcf3361dbac6`)
— both digests derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced both
output files byte-identically. The run's base
was `main` at
`3e75d7b0707a210598e90df5d92d92253cf9435b`.
Foundation check (H21) at the run, on this
checkout with the two gitignored Holdat CSVs
copied from the existing local downloads
(corpus CSV SHA-256 `62d14d2b…` and roles CSV
SHA-256 `eb6d3b6a…`, both verified first):
**40 passed / 0 failed / 8 warnings** — the
standing figure. The frozen contract's own
tests also pass locally in the adopted
environment (aee 1.5.0 venv:
`test_spec048_freeze.py` and
`test_experiment_graph.py`, 51 passed /
1 skipped).

## 2. Step 0, gate by gate

**Integrity pins (spec §2), asserted before
any gate quantity — PASS.** Every §2 input
that carries a byte pin recomputes to its
freeze value: the Phase-43 results file
`78a6c219…`, the anchors file
`df0cf620…` (census re-read: 287 anchors, 94
`strict_sa_independent`; M072 present with
validation status `pending_non_sa_validation`,
per DD-048-18), the Mahadevan–Parpola crosswalk
`9ebd7723…`, and the Spec 033 spec `eaea0e2e…`.
Each pin was verified in the foreground by two
independent routes — the working-tree files
and the GitHub contents API at the run's base
commit — with identical results, and again by
the phase machinery in the worktree. The claim
file is handled in the Spec 038 form the
freeze test itself uses: its freeze-time hash
`3202aeca…` is a definition constant, and
manual_002's facts are asserted on the live
file (exactly one entry; status
`partially_supported`; stage `explained`;
sign_ids Mahadevan [72, 64, 70]; the
not-understood text naming the sign-by-sign
family test on the strict corpus). The live
file at the execution base hashes to
`7750680e…`: it differs from the freeze-time
bytes because the extracted-claims store was
regenerated wholesale after the freeze (Spec
058's execution, 2026-10-21) — for manual_002
the only changed field is `extracted_at`. That
store regeneration is a pre-existing condition
of `main` at the execution base, not an act of
this execution, and the freeze contract's own
test prescribes exactly this handling.

- **0.1 Asset F digest assertion — PASS.**
  Asset F's canonical file
  (`specs/044-fish-sign-coastal-residue/asset-f-fish-family.json`,
  whole-file SHA-256 `193a9754…`, 7 members) was
  exhibited. Its digest, recomputed over the
  canonical bytes with the `digest` field
  excluded (Spec 044 §4.2's rule, in Spec 044's
  own canonical serialisation), is
  `ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`
  — identical to the digest recorded in Spec
  044's step-0 outcome record, the pin source
  this freeze fixed (DD-048-9), and identical to
  the file's own `digest` field. The
  recomputation was verified by two independent
  routes (the phase machinery in the worktree,
  and an independent recomputation over the
  contents-API bytes), agreeing exactly. The
  asset was not rebuilt, re-derived, or
  substituted.
- **0.2 Membership join and cross-check —
  PASS.** Every Asset F member carries a
  `mahadevan_number` locator and joins through
  the pinned crosswalk, with the crosswalk's
  Parpola locator agreeing in every case:
  M047 (Mahadevan 47, Parpola 47, fish (plain)),
  M048 (48, 48, fish-with-roof), M050 (50, 50,
  fish-with-fins), M052 (52, 52,
  fish-with-trefoil), M060 (60, 60, fish
  (variant; 'badly drawn')), M145 (145, 145,
  fish with two horizontal lines), M147 (147,
  147, fish (sign-list variant)) — all seven
  **MAPPED**, none **UNMAPPED**. Cross-check,
  reported and never a membership source: of
  the claim record's named trio (Mahadevan 72,
  64, 70), **none** is an Asset F member; of
  the Phase-43 six candidates (267, 72, 65,
  59, 60, 70), only **60** is. Every divergence
  is named here and in the step-0 record; the
  cross-check adds and removes no member.
- **0.3 Strict corpus identification, pin, and
  measure reproduction — FAIL (the execution
  closes here).** The gate requires the V3 /
  Mahadevan-lineage layer (Spec 033 §4;
  DD-048-10) to be identified from the
  database as the layer the Phase-43 framework
  used, exported in full, pinned by digest,
  and the T2.4 reference points re-derived
  from the pinned layer. The attempt was
  mechanical, in four parts, and every part is
  in the run's record:
  - **C1 — the V3 layer itself is absent.**
    The V3 corpus has exactly one loader of
    record (`backend/glossa_lab/data/indus_corpus_v3.py`),
    and it reads one data file:
    `glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl`
    — the Firestore 'indusarrays' dump. That
    file does not exist in the tree (the tracked
    `sources/rmrl/` directory holds only its
    bulletin and provenance files, and a
    contents-API read of the dump path at the
    execution base returns Not Found). The
    loader was imported from its file and run
    in this tree: it loads **zero** records and
    **zero** sequences — by its own code a
    missing file yields an empty record list.
    A layer that cannot be loaded cannot be
    exported whole or pinned.
  - **C2 — no database copy exists to identify
    it from.** The execution tree holds no
    database at all (`backend/data/` does not
    exist in the tree; a contents-API read at
    the execution base returns Not Found). The
    layer is not held in any database this run
    can reach.
  - **C3 — what the layer would have to be.**
    The pinned Phase-43 record names its
    corpus exactly: §T1_1 — source
    "indusscript.in Firestore 'indusarrays'
    (2026-05-14)", 3,916 records, 3,137
    sequences, 2,665 dockeys, 12,494 sign
    instances; and §T2_4's reference points —
    candidates [267, 72, 65, 59, 60, 70]; sign
    72 at 181 occurrences, terminal fraction
    0.259, supported; sign 267 at 356
    occurrences, 0.038, not supported. That is
    the identification and reproduction
    standard gate 0.3 sets, and no candidate
    below meets it.
  - **C4 — no other layer in the tree is that
    corpus.** The site-attributed layer
    (`yajnadevam_inscriptions.csv`, SHA-256
    `c02e3d7b…`) carries 5,679 records and is
    a different layer of record (the Phase-393
    layer; the layer Specs 027/028/042/045 pin
    for their own contracts). The V1 research
    export (`indus_research.jsonl`, SHA-256
    `08fc96c8…`) carries 15,508 objects across
    five source systems in mixed sign schemes
    (PennMuseum 7,515; MetOpenAccess 4,904;
    indusscript-m77 2,906; mayig-cisi 179;
    ClevelandArtOpenAccess 4) and is labelled
    V1 in the corpus versioning record. The
    ICIT-format export (`indus_icit_format.json`,
    SHA-256 `e4ddfd06…`) carries 3,085
    ICIT-encoded sequences, a different lineage
    and encoding. The Holdat downloads path is
    absent from the tracked tree, and the
    Holdat compilation is in any case the
    distinct second compilation whose arm gate
    0.4 governs, not the Mahadevan-lineage V3
    layer. No subset rule, reconstruction, or
    substitute layer was invented to stand in
    for the missing one.
  The reproduction leg was therefore **not
  run**: there is no pinned layer to re-derive
  the reference points from, and the frozen
  wording closes the run on either leg. Gate
  0.3 fails as written. This is the same
  absence the freeze-stage records of Specs
  049 and 052 and the execution records of
  Specs 045 and 053 established for the
  Phase-43 corpus from their own sides; this
  record re-derived it first-hand against Spec
  048's own frozen gate (including running the
  V3 loader itself) and borrows none of their
  verdicts.
- **0.4 Holdat layer and crosswalk pin — NOT
  REACHED.** No judgement about the Holdat
  layer's pinnability, or about any member's
  per-sign crosswalk, is recorded or implied
  by this closure: the gate was never run,
  because the frozen order puts the primary
  corpus pin first.
- **0.5 Census (margins only) — NOT REACHED.**
  No census exists (there is no pinned primary
  corpus to census), so the 30-occurrence
  floor was never applied and **no TOO THIN
  judgement — per member or for the execution
  — is recorded or implied**. (The census of
  Spec 044's pinned Holdat layer, in Spec
  044's own record, is a different layer's
  census under a different contract; it is not
  this gate's census and was not borrowed.)
- **0.6 Control set freeze — NOT REACHED.**
  No control was enumerated or entered, and no
  judgement about the control set's
  enterability is recorded or implied.

## 3. What does not exist, stated plainly

No strict-corpus pin or digest; no Holdat
layer pin and no per-sign crosswalk statement
(gate 0.4); no census and no per-member TOO
THIN dispositions (gate 0.5); no frozen
control set (gate 0.6); no ending-follower
rate for any member in either arm; no
token-weighted family rate or passing share;
no 72/64/70 sensitivity; and no family
verdict. The claim
`parpola_2010_dravidian_solution_manual_002`
stands exactly as recorded — IN QUESTION,
partially supported, stage explained — and
its record was not edited.

## 4. What this closure does and does not establish

What was proven: Asset F's identity holds
under the consumed contract (gate 0.1 — the
digest asserted against Spec 044's step-0
record, not merely read from the asset); the
join is complete and clean (gate 0.2 — every
member mapped through the pinned crosswalk,
with the cross-check divergences named); the
§2 pins hold (integrity block); and the
strict corpus this spec's primary arm stands
on is not pinnable from the records and
stores the programme holds in this tree (gate
0.3). What was not established: anything
about how the fish family's members behave
positionally — the family question this spec
exists to ask remains **unattempted, not
failed on its merits** — anything about what
any fish sign meant or was pronounced, and
anything about why sign 267 behaves
differently in the Phase-43 record. The
unblocking act is a records act, not a
re-scope: the Firestore 'indusarrays' dump
(or another uniquely identified, exportable
copy of the V3 layer, pinned as a record of
record) entering the programme's tracked
stores, after which this spec's frozen gates
could be run as written under a new execution
order; any change to the gate itself would be
an amendment for the owner, queued outside
this pass.

## 5. Claim consequences (governed register)

One line per governed claim, F048-C01…C15.

- **F048-C01** (an outcome states only the
  members' positional behaviour under T2.4):
  HELD in scope — this record states no
  positional-behaviour conclusion, because
  none was computed; it records a runnability
  closure only.
- **F048-C02** (manual_002 stands IN QUESTION,
  partially supported, on the split record):
  HELD — the claim's record is untouched and
  its standing is exactly as recorded. No
  append was made to the extracted-claims
  file: its bytes are a frozen §2 pin, and
  the dated closure append for this execution
  is this outcome record and the root LEDGER
  entry (the Spec 044 form for the same
  reason).
- **F048-C03** (tested members carrying at
  least 70% pass): NOT REACHED — no member
  was tested; the hypothesis is unjudged,
  neither supported nor falsified.
- **F048-C04** (the partition's lower branch,
  at most 30%): NOT REACHED — no passing
  share exists.
- **F048-C05** (membership is exactly Asset F
  as frozen at Spec 044's step 0): CHECKED at
  gate 0.2 — held; the family counted (in
  disposition) is Asset F's seven members and
  no others.
- **F048-C06** (Asset F's byte-digest is
  asserted at gate 0.1 against Spec 044's
  step-0 outcome record): CHECKED at gate
  0.1 — held, §2 above; the digest asserted
  is `ca5fb1b5…`, recomputed, not transcribed.
- **F048-C07** (the primary arm runs on the
  strict corpus identified at gate 0.3):
  HELD in its closure branch — no arm ran on
  any substitute layer; gate 0.3's failure to
  identify that corpus is the recorded fact
  that closed the execution.
- **F048-C08** (each tested member's measure
  is the T2.4 ending-follower rate): NOT
  REACHED — no member's rate was computed in
  either arm.
- **F048-C09** (execution stops before any
  ending-follower rate on a step-0 gate
  failure): FIRED as written — gate 0.3's
  failure stopped the execution before any
  rate, census, or control quantity.
- **F048-C10** (the headline is exactly one
  member of the §6 outcome set): HELD — the
  headline is STRICT CORPUS NOT PINNABLE, in
  §6's pre-written wording with the reason
  filled in.
- **F048-C11** (a mapped member below 30
  occurrences is recorded TOO THIN): NOT
  REACHED — gate 0.5's census never ran; no
  member is recorded TOO THIN under this
  spec, and none may be quoted as such from
  this record.
- **F048-C12** (every member's disposition is
  reported): HELD in the form the closure
  allows — every member's gate 0.2
  disposition (MAPPED, all seven) is reported
  in full above and in the step-0 record; the
  census dispositions do not exist, and this
  record says so.
- **F048-C13** (the control set is the
  gate-0.6 frozen set): NOT REACHED — the
  control set was never frozen, and no
  control figure exists.
- **F048-C14** (records stay internal under
  the Roif gate): HELD — this record and its
  companions are internal; nothing was
  published or surfaced, and campaign
  reporting names this member only as
  executed — held under the Roif gate.
- **F048-C15** (no outcome establishes a
  'meen' pronunciation): HELD — no
  pronunciation or meaning statement appears
  in any product of this execution.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 6. Records

- Step-0 record: `reports/phase408_results.json`;
  report: `reports/phase408_step0_report.md`
  (digests in §1).
- Graph node: `IndusPhase408FishFamilyStep0`
  (registered and verified by import before
  the run; 497 nodes total).
- Root LEDGER entry: "Spec 048 EXECUTED
  (Phase-408)" entry added with this record.
- Tasks: E1, E2, and E3 stand ticked in
  `tasks.md` with their execution notes (E3
  with its gate 0.3 closure); E4–E5 stand
  open in form and are closed in substance by
  this record — they cannot run under this
  frozen contract, and any successor is a new
  act under a new freeze or an amendment; E6
  stands ticked as delivered in this closure
  form.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of
  the freeze (`test_spec048_freeze.py`
  enforces the pins), and the executed-spec
  form records execution here, in
  `outcome.md`. The claim file
  `parpola_2010_dravidian_solution.json` was
  likewise not edited (§5, F048-C02).
- CI and the foundation check at the record
  merge: appended below after the record PR
  merges, as a separate landing-record append
  — this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

---

## Landing record (appended 2026-10-21, after merge)

Execution PR **#297** ("Spec 048 execution
(Phase-408): STRICT CORPUS NOT PINNABLE at
gate 0.3"), branch `spec-048-phase408-execution`,
merged to main as merge commit
**654253dae950cf73ba1deecabdf9e43321cf7a5a**
(2026-10-21T19:29:40Z). The branch was based on
3e75d7b0 and synchronised with main twice
during the landing window as sibling executions
landed (Spec 050, PR #296; Spec 047 step 2,
PR #298; then Specs 050/051, PR #300); each
conflict was an append collision in LEDGER.md
(and, in the second sync, the experiment-graph
registration blocks), resolved as a union of
both sides, with the pins re-verified on the
merged content after each resolution and the
Phase-408 node present by import at the first
sync (497 nodes). The second and third syncs
were built through the GitHub git-data API
after a VM write restriction blocked local git
object writes; every API-built commit was read
back and byte-verified (parents, LEDGER.md,
and the graph file — removing the Phase-408
block from the merged graph reproduces main's
bytes exactly).

CI: the decisive run on the final head
(4b77d677) is run **39660844516** — 7 of 7 jobs
success from their own conclusions (Backend
tests (pytest); Frontend tests (Playwright);
Indus public validation checks; Evidence Graph
script smoke tests; Shell wrappers ubuntu /
macos / windows). Earlier genuine 7/7 runs on
the branch's prior heads: 39655776264
(654d4f1b) and 39658340395 (f59e4be0). (The
branch's first head, be718a4b, received no CI
runs at all because the PR stood in conflict
with main — the known mechanism — until the
first sync resolved it.)

Machine records re-verified on main at the
merge commit by two routes (contents-API raw
and git-blob decode, agreeing byte-for-byte):
reports/phase408_results.json SHA-256
c08e775c7f70af0b95dc1e059a4116c65c5d37f0653d6eec06df198c505ef6f3;
reports/phase408_step0_report.md SHA-256
9dca830c4c281b65df7494acea5b3c65600bcfc31135f10d5627bcf3361dbac6;
the anchors file at df0cf620… and Asset F's
whole-file SHA-256 at 193a9754… likewise.

Foundation check at the merge commit: **40
passed / 0 failed / 8 warnings** — the same
counts as at the run. It was executed on the
owner's desktop (TRISTEN-DESKTOP) in a fresh
clone checked out at the merge commit
(HEAD verified as 654253da…), with the two
gitignored Holdat CSVs placed from the pinned
local downloads and hash-verified on the
desktop before the run (corpus CSV 62d14d2b…,
roles CSV eb6d3b6a…), because a VM write
restriction blocked a fresh clone on this
machine (the owner's standing directive for
that case); the run's own output reads
"RESULT: 40 checks passed, 0 failed,
8 warnings" (FC exit 0).

Terminal outcome, restated in the frozen
wording: **STRICT CORPUS NOT PINNABLE**
(gate 0.3). Gates 0.1 (Asset F digest
assertion, digest ca5fb1b5…) and 0.2
(membership join — all seven members MAPPED,
none UNMAPPED) passed with the values recorded
above; gates 0.4–0.6 were not reached; no
ending-follower rate was computed; the claim
stands exactly as recorded. Gate 0.3 was
evaluated at the execution base (3e75d7b0),
as the frozen contract requires; material
that reached main afterwards does not change
this execution's record and is for a future
execution order to weigh. This record remains
internal under the campaign's Roif gate
(R-7); it is not a publication.

*AI disclosure: appended by an AI agent (Muse
Fable 5, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
