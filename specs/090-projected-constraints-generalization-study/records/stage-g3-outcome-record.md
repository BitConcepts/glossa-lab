# Stage G3 outcome record (T403) — Spec 090 (2026-11-12)

**Scope:** tasks.md T403 — the computation of the frozen
separator's profiles over H1 — executed on branch
`spec090-g3-run` at base main `96894f9c` (merge of PR
#559, the T402 freeze), with the bar of package §5
adjudged mechanically on the resulting profiles in §4
below. Inputs: the freeze record
(`records/stage-g3-freeze-record.md`), whose pins,
extraction rules, case list, seed, and bar govern every
quantity here; the owner's ruling of 2026-11-12 recorded
in the freeze's §5 (the held-out verification stands
under §3's criterion as written; T403 authorized on the
freeze's merge). The executing tool is
`tools/spec090/run_g3.py` (version 1.0.0, committed at
`50ece623` on this branch before any run), run under
CPython 3.12.3.

**Stage outcome: SEPARATED** — the bar of §5 met in
full on the profiles of §3, adjudged in §4. The
study-level outcome remains **INSTANTIATES-path** (now
with G3 attempted at stage strength); the bare
INSTANTIATES verdict is not issued here and remains
reserved to the independent reader over the full
G1–G5 bar (package §6).

## 1. The administration as run

Each frozen case was executed exactly once as a
Spec 089 run on the `study` surface (run-defs v2),
each minting its run id at execution start and writing
its run record into this spec's `records/` store
through the registered library writer, which appended
the index `entry` acts to `records/run-index.jsonl`.
Every case carries exactly one run record:

| Case | Run id | Record |
|---|---|---|
| A0 | `study-20261112T152008Z-ec336a` | `study-20261112T152008Z-ec336a.json` |
| A1 | `study-20261112T152009Z-22d5aa` | `study-20261112T152009Z-22d5aa.json` |
| A2 | `study-20261112T152010Z-82d88c` | `study-20261112T152010Z-82d88c.json` |
| A3 | `study-20261112T152010Z-2ca7ad` | `study-20261112T152010Z-2ca7ad.json` |
| C1 | `study-20261112T152011Z-aa19c6` | `study-20261112T152011Z-aa19c6.json` |
| C2 | `study-20261112T152011Z-95250e` | `study-20261112T152011Z-95250e.json` |

No execution refused, and no absence record stands in
the store. Before any profile was computed, the tool
verified both pinned source files by SHA-256 in the
executing clone (snapshot `08fc96c8…`, flat file
`878fd223…` — both agreeing with freeze §1) and the
extraction reproduced the freeze's permitted counts
exactly (2,906 records, 12,639 tokens; freeze §3), or
the run would have refused under a minted id.

## 2. Verification of the computation

Three legs stand behind the profiles of §3.

**(a) A second full execution, byte-identical.** The
whole administration was executed a second time from
a clean state (same tool commit, same frozen inputs)
into a separate verification store. The two executions
of each case are comparable under run-key v1 (every
constitutive key component agrees), and on the `study`
surface's registered determinism their result blocks
must agree byte-for-byte. They do, for all six cases
(SHA-256 of the canonical result-block serialization;
the administration's and the verification run's hashes
are the same value, stated once per case):

| Case | Verification run id | Result-block SHA-256 (both runs) |
|---|---|---|
| A0 | `study-20261112T152017Z-3414a6` | `801b36a145c952a5346a35fd158cca4654353feb31cabf82c7b92633e1a0b70f` |
| A1 | `study-20261112T152017Z-630247` | `c9c8918162a0f25b4a8623ac13ebf707924cb04811349aa90083cc8d31e5ce04` |
| A2 | `study-20261112T152018Z-d7757f` | `1617cea688152955100e5e03f106d8299320a46aedf912f130ec015c4b958d0b` |
| A3 | `study-20261112T152019Z-844852` | `242fb3895baa5ab52aadefac764d789e70030544bd92533b5d713e8a638da6d3` |
| C1 | `study-20261112T152019Z-c52845` | `8db4a284db0a4790dc5d076a7048f549099767e33d70757df606595af9f783f3` |
| C2 | `study-20261112T152020Z-d845ea` | `1672a6c90f7dbf4dcb1366b77886c2cf0707a08f98021f09e568fc85231167f3` |

An identical comparable pair raises no junction
(run-defs v2 §5, §10's precedent shape). The
verification store is working evidence, not the store
of record; the records of §1 govern.

**(b) A hand-worked toy table.** `tools/spec090/check_g3.py`
carries a four-object toy table whose profiles for A0,
A1, and A3 are derived by hand in its docstring from
the freeze's definitions (every component, including
the one-token-sequence positional rule), together with
the A2 floor refusal (the toy's largest multiplicity
is 6, below the floor of 10), C1's determinism and
profile invariance, and C2's identity. The tool
reproduces every hand value exactly: 16 checks, 16
PASS, exit 0.

**(c) Arithmetic identities on every profile.** For
each of the six administration profiles, the following
identities — consequences of the component definitions,
independent of the tool's counting loops — were
checked and hold: Σ M = token total; Σ L counts =
object count; Σ (length × count) over L = token total;
Σ initial over X = object count; Σ final over X =
object count; Σ medial over X = token total − Σ
initial − Σ final + (length-1 count); Σ B = token
total − object count; |M| = |X| = the inventory size.

The audit form tasks.md T404 names (a worker other
than the computer) is an acceptance act of the stage
reviewer and is not claimed by this record; T404's
acceptance and T405's report to the VEXA chat remain
open after this landing, on the strength of the run
records above, which any re-computation can be checked
against byte-for-byte.

## 3. The profiles

All six tables stand over the same objects and tokens:
**2,906 objects, 12,639 tokens** in every case (the
case rules reassign types; they create and destroy
neither objects nor tokens). The full profiles are in
the run records of §1; each profile's SHA-256 below is
over its canonical serialization in the record.

**A0 — the recorded coding.** Inventory **527**.
Profile SHA-256
`6e58de70a7e92c8abc121b4a79486d55e0ecf71795f120589a85eba89f84edfa`.
M's head: 1274, 680, 615, 342, 338, 317, 261, 255, 219,
209, 206, 192; 159 codes are hapax (multiplicity 1).
L, in full (length × count): 1×84, 2×387, 3×633,
4×597, 5×500, 6×305, 7×205, 8×109, 9×37, 10×27, 11×17,
12×1, 13×1, 14×3. B ranges over 3,188 distinct adjacent
ordered pairs.

**A1 — the positional split.** The most frequent code
is **342** (multiplicity 1,274); of its 1,274 tokens
exactly **1** stands in initial position and 1,273 do
not, so the split's initial type is exercised by a
single token. Inventory **528** (+1, as the rule
designs). Profile SHA-256
`868a2cae71b88992b150f783eec8e9e47e4fc359ae5645a1644aeb0d4081bc01`.

**A2 — the tail merger.** The two least frequent codes
at or above the floor of 10 are **\*015** and **\*267**,
each at multiplicity exactly **10** — the floor binds
with no slack; every other code below them in frequency
is below the floor. Inventory **526** (−1). Profile
SHA-256
`805dcc3119f23efcc27e9e77b48bf5fadc5ec699c2ae1b94c8c85bfdbe31fd20`.

**A3 — the head merger.** The two most frequent codes,
**342** (1,274) and **000** (680), merged into one type
of multiplicity 1,954. Inventory **526** (−1). Profile
SHA-256
`3e1eb15d777eb8d7dc7c4689633f90738ab6e0fddeee106b5bded5889f306bbb`.
B ranges over 3,071 distinct adjacent ordered pairs.

**C1 — the relabeling control.** 527 codes permuted by
the frozen seed's bijection (bijection SHA-256
`cc4c4803984d60043cace35b473d167c7777c77e47e47d43f28111b0896bc61b`).
Profile identical to A0's in every component (the same
profile SHA-256 as A0).

**C2 — the identity control.** Profile identical to
A0's in every component (the same profile SHA-256 as
A0).

One component never differs: **L is identical across
all six tables**, as it must be — no case rule changes
a sequence's length, so the length histogram is the
same multiset throughout, and no separation below
rests on it.

## 4. The bar, adjudged mechanically (package §5, frozen verbatim)

**Condition 1 — Distinctness.** For each pair, the
named components in which the profiles differ:

| Pair | Differing components |
|---|---|
| (A0, A1) | inventory size, M, X |
| (A0, A2) | inventory size, M, X |
| (A0, A3) | inventory size, M, X, B |

Each pair differs in at least one named component.
**Condition 1 holds.** (For A1 and A2, B did not
differ: the pair-count multiset is blind to which
pairs carry the counts, and the splits' and merger's
redistributions left that multiset unchanged — the
named coarsening of package §2, observed in the
non-blocking direction. A3's merger did move B.)

**Condition 2 — Invariance.** (A0, C1): identical in
every component. (A0, C2): identical in every
component. **Condition 2 holds.**

**Condition 3 — No count separation.** Every compared
table has object count 2,906 and token total 12,639
(§3); there is no difference in object count or token
total between any compared pair for a component
difference to run through. **Condition 3 holds.**

All three conditions hold on the administration's
profiles, verified as §2 states. The stage outcome
is therefore **SEPARATED**, in §6's vocabulary: one
separator, defined from the G1 document's terms,
computed over records the derivation did not use,
distinguishing the frozen agreed-distinct cases and
refusing the controls.

**ANALOGY pressure (§6), recorded as named.** The
package names in advance the pressure that differences
of this kind are bookkeeping about codings rather than
distinctions between candidate states. The stage does
not grade its own §4 judgment call. What the
administration's evidence bears on it is stated here
for the reader: the separated cases are re-codings of
the same objects in G1 §2.1's naming mode (a split, two
mergers), the controls behaved as D5's invariance
clause requires, and no leg of the administration
failed in a way that would collapse the §4 judgment
from inside the run. The pressure stands as the
reader's to weigh, with the profiles before them.

## 5. The carried items

**The object-overlap item (freeze §4).** Carried
exactly as frozen: **not measurable by the specified
route**. H1's records carry identifiers; the flat file
carries none (1,669 lines of bare code sequences, no
line enumerable by IM77 text number in any in-repo
record), so no overlap number exists to carry. The
populations stand side by side — 2,906 H1 records;
1,669 flat-file inscriptions — and the untouched
criterion does not turn on the overlap (package §3.1:
it "holds either way"). No substitute measurement was
invented for this record.

**The held-out verification and Spec 076 (freeze §5),
in substance.** Spec 076 (`specs/076-projected-constraint-corpus-model/`,
closed ASSUMPTION SET DOES NOT HOLD) published, over
the same snapshot `indusscript-m77` frame (the same
2,906 records), a sequence-length profile (1×225,
2×531, 3×563, 4×521, 5×444, 6×249, 7×189, 8×82, 9×32,
10×28, 11×11, 12×2, 13×1, 14×2) and positional slot
aggregates (Σ initial 2,655; Σ final 2,655; Σ solo
225; Σ medial 5,972), under a token construction that
drops the 680 `000` tokens and 452 `*`-marked tokens
H1 as frozen keeps (its frame: 2,880 non-empty
sequences, 11,507 tokens); Spec 033's pipeline census
had recorded the same frame's token totals earlier
still. The enumerated verification stands (Spec 077's
frozen record and the anchor-support audit computed no
table, profile, or per-record quantity over H1), and
the owner ruled on 2026-11-12 that the verification
stands under §3's criterion as written. Accordingly,
what this administration establishes under claim
C090-19 is reported at the strength the freeze
supports: **the profiles of §3 are the first computed
under Spec 090's separator over a set held out from
Spec 090's own design process under the enumerated
criterion, with one adjacent length profile under a
different token construction pre-existing in the
frozen records** — and not as a first-profile-by-anyone
claim at full strength. (Under the frozen construction,
which drops nothing, H1's own length histogram is the
one stated at §3 for A0 — a different quantity from
Spec 076's, over a different sequence population.)

## 6. Claims and boundaries

No claim's status, stage, or score is changed by this
landing, and the claims ledger receives no lines from
it: the G3 stage's ledger diff remains exactly the
adoption append of C090-17..24 (C090-23). The claims
this act bears on, at the strength the evidence
supports:

- **C090-17** — the profiles computed are those of the
  frozen definition and no other; every constant in the
  tool is the freeze's.
- **C090-18** — the extraction of §2 of the freeze was
  executed as stated; the overlap limb stands as §5
  above records it.
- **C090-19** — the freeze (merged 2026-11-12) precedes
  every profile computed here (first run
  2026-11-12T15:20:08Z); reported at the capped
  strength of §5 above.
- **C090-20** — the controls' audited profiles equal
  A0's in every component; the invariance the claim
  tests held on this administration.
- **C090-21** — the outcome was adjudged by §5's three
  conditions over the frozen case list and definitions;
  nothing was added, dropped, re-weighted, or re-run.
- **C090-22** — no restricted material entered the
  stage: H1 enters this record as statistics and
  computed profiles only; no CISI material plays any
  part (the `mayig-cisi` subset is excluded by the
  frozen filter).
- **C090-23** — discharged in the negative form the
  claim requires: this landing's claims-ledger diff is
  empty.
- **C090-24** — the outcome is recorded here in the
  skeleton's vocabulary (SEPARATED; study level
  INSTANTIATES-path at most). The report to the VEXA
  chat (T405, D-090-10) remains owed and is the parent
  seat's act, as T302's delivery was; this record does
  not claim it.

No convergence step was taken or implied. The formal
verdict over the full G1–G5 bar belongs to the
independent reader under the judging protocol. G3
stands attempted under the stage amendment ratified
2026-11-06, as D-090-5 provides; G4 and G5 remain
unattempted and are barred to this stage (C090-15 as
it continues under D-090-5).

## 7. Reproducibility

- Tool: `tools/spec090/run_g3.py` (version 1.0.0) and
  `tools/spec090/check_g3.py`, committed at `50ece623`
  on this branch (the run records' `code_version`).
- The administration, from the repo root at that
  commit, per case:
  `python3 tools/spec090/run_g3.py run-case --case <A0|A1|A2|A3|C1|C2> --store specs/090-projected-constraints-generalization-study/records`
- The hand-check: `python3 tools/spec090/check_g3.py`
  (16 checks, all PASS, exit 0).
- The verification re-execution used the same commands
  with the verification store as `--store`; §2(a)
  states its run ids and the shared result hashes.
- Result-block and profile hashes: §2(a) and §3. A
  re-computation that reproduces those hashes from the
  frozen inputs has reproduced the administration.

*T403's "does not establish" line:* the outcome —
computation produces profiles, not verdicts. The
SEPARATED of §4 is the bar's mechanical adjudication
on those profiles, stated here because the stage's
record requires it; it is not a verdict on the domain,
and it establishes nothing about the Indus script,
which remains undeciphered.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
