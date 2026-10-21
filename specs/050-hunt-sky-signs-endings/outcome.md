# Spec 050 / Phase-416 — Outcome record (EXECUTED 2026-10-21 — CLOSED AT STEP 0 — ASSET NOT FROZEN)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 050 contract
> (freeze digest
> `fdcbae649554fa73237a9b5d52cccadfe72fc4117880f8eabcc3242f45f8b1a1`)
> as **Phase-416**, in Wave 3 Group 3 of the
> runnable-experiments campaign (plan approved
> AS WRITTEN on 2026-10-21). The execution gate
> was satisfied before the run: OSF registration
> **uwdmy** is APPROVED + PUBLIC (DOI
> 10.17605/OSF.IO/UWDMY). Step 0 ran in the
> frozen order, fail-closed, and its first gate
> closed the execution: gate 0.1 (Asset A digest
> assertion) found no frozen Asset A on record —
> the fixed pin source does not exist, so there
> is no recorded digest to assert. Outcome:
> **CLOSED AT STEP 0 — ASSET NOT FROZEN** — a
> not-run dependency closure, not a verdict. No
> join was made, no quantity was computed, and
> the claim stands UNTESTED as recorded.

## Headline (spec §5.2 wording, CLOSED AT STEP 0 — ASSET NOT FROZEN form)

"Spec 050 closed at step 0: Asset A is not frozen
on record — Spec 045's `asset-a-freeze.json`
does not exist at this execution. No join was made
and no quantity was computed. The claim stands
UNTESTED as recorded. This is a dependency closure
under the campaign's cluster rule, not a verdict
on the claim."

Claim:
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
— UNTESTED (Phase-104, RULE-CLASS), unchanged.
The §9 headline quantities a completed run would
carry — the Asset A digest, the celestial class's
census, the pooled rates R_sky and R_cmp, the
enrichment ratio, the exact test's result, and the
half-of-occurrences share — do not exist under
this spec, and this record says so rather than
supplying substitutes. Position is not meaning
(spec §7, limit 1): this closure states nothing
about sky signs, calendars, cycles, or any sign's
content — it states only that the frozen asset
this test consumes was never built, so the test
could not be run. Spec 037's census caution —
object-type labels diverging between compilations
in 49% of matched cases — is restated here, as it
travels with every statement under this spec and
with the asset this spec would have consumed;
Asset A's construction was the design's answer to
that caution, and that construction was never
reached.

## 1. What was executed

Gate 0.1 only (spec §3), executed as a foreground
record verification at the execution base,
`main` at
`3e75d7b0707a210598e90df5d92d92253cf9435b`
(the current `origin/main` at the execution turn,
re-read at the start of the act). Gate 0.1 reads
the Asset A SHA-256 from the fixed pin source —
Spec 045's
`specs/045-hunt-depicted-kinds/asset-a/asset-a-freeze.json`
(§2.3; DD-050-11) — and asserts it against the
recomputed digest of the canonical
`asset-a/depicted-kind-classification.csv` before
any join and before any counting. The pin source
does not exist, and neither does the canonical
CSV, so no digest exists to read or assert, and
the gate's unfrozen-or-absent branch fired as
written. The absence was verified first-hand at
the execution base by two independent routes:

- **Route 1 — the local tree.** In a fresh
  isolated clone of `origin/main` at the base
  commit (the stale local checkout was never
  touched): the directory listing of
  `specs/045-hunt-depicted-kinds/` carries its
  nine standing entries (and its `aee/` set) and
  no `asset-a/` directory; direct existence tests
  for `asset-a/`, for
  `asset-a/asset-a-freeze.json`, and for
  `asset-a/depicted-kind-classification.csv` all
  return absent; and the full recursive tree
  listing at the base commit (`git ls-tree -r
  HEAD`, 5,718 file paths) contains no path
  carrying `asset-a/`, `asset-a-freeze`, or
  `depicted-kind-classification`.
- **Route 2 — the GitHub API, at the same
  commit.** The contents API returns **404 Not
  Found** for both
  `specs/045-hunt-depicted-kinds/asset-a` and
  `specs/045-hunt-depicted-kinds/asset-a/asset-a-freeze.json`
  at `ref=main`; and the git-trees API, read
  recursively at the base commit (6,124 entries,
  `truncated: false`), contains no path carrying
  `asset-a/`, `asset-a-freeze`, or
  `depicted-kind-classification` — the Spec 045
  directory's 17 tree entries are exactly its
  standing files, with no `asset-a/` subtree.

The two routes agree: **Asset A is not frozen on
record, and no Asset A digest exists anywhere in
the tree.** No phase script, experiment-graph
node, results JSON, or run report was created for
this closure: gate 0.1's absence branch is a
record check, its finding is the absence itself,
and building run machinery or a results artifact
would dress a non-run in a run's clothing. No
substitute asset, substitute digest, or stand-in
file of any kind was created, and Asset A was not
reconstructed from Spec 045's materials or from
any other source.

## 2. Step 0, gate by gate

- **0.1 Asset A digest assertion — FAIL, in its
  absent branch (the execution closes here).**
  Asset A is not frozen: Spec 045's execution
  record is on record (cited in §3), but no
  `asset-a-freeze.json` exists at the pin source
  this spec's freeze fixed, and no canonical CSV
  exists to recompute a digest from. The gate's
  frozen wording for exactly this state is
  **CLOSED AT STEP 0 — ASSET NOT FROZEN**: a
  dependency closure, not a verdict; the claim
  stands UNTESTED as recorded. The gate's other
  branch — ASSET PIN MISMATCH — does not arise:
  a mismatch requires a presented asset and a
  recorded digest, and neither exists.
- **0.2 Input integrity — NOT REACHED.** The
  execution stopped at gate 0.1; the §6 pins were
  not re-asserted as a gate act, and this record
  claims no finding under this gate. (The anchors
  assertion in §5 is this record's own integrity
  statement, not a gate-0.2 act.)
- **0.3 Coverage and join completeness — NOT
  REACHED.** No Asset A row exists for any sign,
  so no coverage question arises; an absent row
  was not treated as non-celestial by default —
  no comparison class was formed at all.
- **0.4 Class census — NOT REACHED.** No census
  exists: there is no celestial class to
  enumerate, no member sign, and no total. The
  TOO THIN closure does not arise — it requires a
  frozen class whose totals can be counted, and
  no class exists.
- **0.5 Positional reproduction — NOT REACHED.**
  No reproduction was attempted under this spec,
  and no positional quantity exists.
- **0.6 Freeze-order proof — NOT REACHED as a
  gate act.** Its substance is recorded here for
  the reader: this spec froze on 2026-10-21
  quoting Spec 045's freeze digest
  `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`
  as its contract anchor and fixing the pin
  source (DD-050-11); Asset A never froze; and no
  join of Asset A to the corpus under this spec
  precedes or follows either act, because no join
  was ever made.

## 3. The dependency: Spec 045's terminal record, cited

Asset A was to be built and frozen inside Spec
045 (design D-05) at its execution step 1. Spec
045 executed as Phase-411 in Wave 3 Group 1 and
closed **INVALID at its step-0 gate 0.2**
(positional reproduction), before its step 1:
execution PR #268 merged to `main` as merge
commit `c97c8d4c7153bd60917b1064c8eaf1cfa748549b`,
with its landing record appended by PR #269. Its
outcome record
(`specs/045-hunt-depicted-kinds/outcome.md`, §3)
states the consequence in plain words, and this
closure is that consequence arriving for design
D-13:

> Asset A was **not built**: the step-0 closure
> precedes step 1 in the execution order, so build
> gates A1–A6 never ran, no sign was classified,
> and no `asset-a/` directory, CSV, or
> `asset-a-freeze.json` exists. There is therefore
> **no Asset A digest** for any dependent to pin.
> Specs for D-06 and D-13 consume Asset A by
> digest, and no digest exists.

Spec 050 is the D-13 consumer named there. Its
own frozen contract anticipated exactly this
state and pre-wrote its handling: gate 0.1's
absent branch and the §5.2 wording this record's
headline carries, fixed at the freeze under the
coordinator pin-timing ruling DD-050-11 — no
Asset A digest was asserted at the freeze because
none existed, and none has come into existence
since.

## 4. What this outcome does and does not establish

It establishes one fact, verified two ways at the
execution base: the frozen asset this spec
consumes does not exist on record, so Spec 050
cannot be run as written. The standing
consequence is stated plainly: **the D-13
comparison was never run, and its hypothesis is
unjudged.** No celestial class was formed, no
sign was classified under this spec, no census
was taken, and no final-position quantity — no
rate, ratio, test, or share — exists. The claim
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
stands UNTESTED, exactly as Phase-104 and this
spec's freeze left it: neither supported nor
falsified, at its endings as at every other part
not yet measured. This closure does not establish
that sky signs do or do not gather at the ends of
texts, and it does not widen the class by one
sign (§2.2): no jurisdiction-coded sign, no sign
a reader might call celestial, and no sign
classified by any worker's judgement was entered
as a stand-in for the missing asset. What would
unblock a successor is an act outside this frozen
run: Asset A built and frozen under a successor
to Spec 045 (a new freeze or an owner amendment),
after which this spec's frozen gates could be run
as written under a new execution order. This
record does not commission that act, and nothing
was repaired, re-derived, or substituted in-pass.

## 5. Claim consequences (governed register)

Executed under register 0.8-draft (frozen);
one line per claim, F050-C01…C15.

- **F050-C01** (an outcome states only whether
  Asset A's `sky_cycle` signs are enriched in
  text-final position): HELD — this record states
  no enrichment conclusion in either direction;
  it records a dependency closure only, within
  the claim's scope.
- **F050-C02** (the claim stands UNTESTED on the
  record): CHECKED — the claim's record stands as
  the freeze read it (Phase-104, RULE-CLASS,
  `stays_untested`), and this closure leaves it
  UNTESTED as recorded.
- **F050-C03** (the hypothesis: the celestial
  class's pooled final-position rate exceeds the
  comparison class's by a ratio of at least 1.5,
  with the §4.3 conditions): NOT REACHED — no
  rate was computed; the hypothesis is unjudged,
  neither supported nor falsified.
- **F050-C04** (meeting the falsifier's condition
  fixes the outcome wording as NOT SUPPORTED):
  NOT REACHED — the falsifier's condition was
  never evaluated; no ratio exists, and no NOT
  SUPPORTED wording is recorded.
- **F050-C05** (the celestial class is exactly
  the set of signs whose Asset A row carries
  `depicted_kind = sky_cycle`): NOT REACHED — the
  definition stands frozen, but no member set
  could be formed: there is no Asset A row for
  any sign.
- **F050-C06** (the freeze record fixes Spec
  045's `asset-a-freeze.json` as the pin source
  for Asset A's SHA-256): FIRED as written — gate
  0.1 consulted exactly that fixed source; the
  source does not exist, and the gate's absent
  branch closed the execution.
- **F050-C07** (celestial membership comes
  solely through `depicted_kind = sky_cycle` in
  the frozen Asset A): HELD — no membership was
  assigned by any route; no sign was classified
  inside this spec or borrowed from any other
  classification.
- **F050-C08** (contested signs are excluded
  from the primary celestial class): HELD in its
  closure form — no primary class was formed, so
  no contested sign was included in one; the
  sensitivity S2 that alone could admit contested
  signs was not run.
- **F050-C09** (text-final position is the last
  sign of an inscription's recorded sequence):
  NOT REACHED — no occurrence was counted in any
  position.
- **F050-C10** (the primary denominator is the
  frequency-matched comparison class of §4.2):
  NOT REACHED — no comparison class was formed;
  in particular, no absent Asset A row was
  treated as non-celestial to form one by
  default.
- **F050-C11** (the headline verdict is assigned
  mechanically by §4.3): NOT REACHED in its
  verdict branch — no verdict word exists; the
  headline is the §5.1 closure class, assigned by
  gate 0.1, not by the §4.3 criteria.
- **F050-C12** (execution stops before any
  final-position quantity on any step-0 gate
  failure): FIRED as written — gate 0.1 failed in
  its absent branch and the execution stopped
  there; no final-position quantity was computed
  past it, and nothing was repaired at run time.
- **F050-C13** (every celestial member sign is
  reported in full): NOT REACHED — there is no
  celestial member sign to report; the per-sign
  table does not exist, and this record states
  that rather than publishing an empty table as
  if it were one.
- **F050-C14** (the headline outcome is exactly
  one of the outcome classes named in §5.1):
  HELD — the headline is CLOSED AT STEP 0 —
  ASSET NOT FROZEN, a §5.1 closure class.
- **F050-C15** (no outcome establishes calendar
  content for sky signs): HELD — no calendar,
  cycle, scheduling, or meaning statement appears
  in any product of this execution.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed at the execution base and again with
this record: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 6. Records

- This outcome record is the execution's only
  product document. No results JSON, run report,
  phase script, or graph node exists under this
  closure (§1 states why).
- Root LEDGER entry: "Spec 050 EXECUTED
  (Phase-416): CLOSED AT STEP 0 — ASSET NOT
  FROZEN" added with this record.
- Tasks: E2 (step 0, part 1) stands ticked in
  `tasks.md` with its gate-0.1 closure noted (its
  gates 0.2–0.3 not reached), and E5 (outcome)
  stands ticked as this record. E1 (graph-first
  build), E3 (step 0, part 2), and E4 (primary)
  stand open in form and are closed in substance
  by this record — they cannot run under this
  frozen contract behind a failed gate 0.1, and
  any successor is a new act under a new freeze
  or an amendment.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of the
  freeze (`test_spec050_freeze.py` enforces the
  pins), and the executed-spec form records
  execution here, in `outcome.md`.
- The campaign state file was **not** updated by
  this act; campaign bookkeeping is the
  coordinator's.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges, in the standing completion pattern —
  this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*


---

## Landing record — 2026-10-21 (appended at merge; append-only)

- Execution PR: **#296** (branch
  `spec-050-phase416-closure`), merged to `main`
  as merge commit
  **`1d954b5fc12efee9149ebd6c81251c5ce439ade4`**.
- CI: GitHub Actions run **39653934856** on the
  PR head `cc910ee4` — **7 of 7 jobs success**,
  verified from the run's own job conclusions
  (Backend tests (pytest); Frontend tests
  (Playwright); Indus public validation checks;
  Evidence Graph script smoke tests; Shell
  wrappers ubuntu / macos / windows).
- Absence re-verified on `main` at the merge
  commit: the recursive tree read at
  `1d954b5f` (5,716 files, not truncated)
  contains no `asset-a/` path, no
  `asset-a-freeze.json`, and no
  `depicted-kind-classification.csv` anywhere —
  the gate-0.1 finding stands on the merged
  record exactly as executed.
- Anchors re-verified on `main` at the merge
  commit by two routes (the contents API raw
  download and the git-blob route, blob
  `1a67e6f05f53c65f89458b24809a4f9d38a55be0`):
  `backend/reports/INDUS_FINAL_ANCHORS.json`
  SHA-256
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
  (570,344 bytes) — byte-identical, asserted.
- Foundation check (H21) at the merge commit:
  **40 checks passed, 0 failed, 8 warnings** —
  the standing figure. Method note, stated
  plainly: a fresh clone of the merge commit
  was blocked by this VM's write restriction
  (git object writes denied "Operation not
  permitted" mid-session), so the check ran on
  the standing full checkout of Spec 061's
  merge tree (`abdcac19`), with the two Holdat
  CSVs in place (corpus CSV SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  verified first). Before the run, a recursive
  blob comparison of the two trees proved they
  differ in exactly four files — `LEDGER.md`,
  this outcome record, Spec 050's `tasks.md`,
  and Spec 061's outcome record — none of which
  the foundation check or its annotation module
  reads; every input the check opens is
  byte-identical between the two trees, so the
  figure is the merge commit's figure.
- Terminal outcome stands as recorded above:
  **CLOSED AT STEP 0 — ASSET NOT FROZEN** — a
  not-run dependency closure. Asset A was never
  built and no Asset A digest exists; the D-13
  comparison was never run, its hypothesis is
  unjudged, and the claim stands UNTESTED as
  recorded.

*AI disclosure: appended by an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
