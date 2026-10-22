# Spec 063 / Phase-425 — Outcome record (EXECUTED 2026-10-22 — RECOVERED)

> ## EXECUTED — 2026-10-22
>
> Executed under the frozen Spec 063 contract
> (freeze digest
> `dc24a10ec177d5f1eb3b73d29ab6f646b4c77b02ae30da2ca86002cc57a49ed9`
> in `freeze.json` as merged), as **Phase-425**,
> under the owner's execution order of
> 2026-10-22 (the separate execution order
> DD-063-13 awaited). The execution gate was
> satisfied before the run: OSF registration
> **kfet5** is APPROVED + PUBLIC
> (`reviews_state` accepted, not pending, not
> withdrawn; API-verified 2026-10-22). Base
> for the run: `main` at `689a5499`. Outcome:
> **RECOVERED** — step 0 passed in full,
> including the thesis file asserted to its
> frozen digest on the local file before any
> plate was read; two independent descriptor
> derivations from the thesis plate agree with
> each other and sustain the preserved
> reference's descriptor; continuity passes on
> the anchors' agreement; and the drawn sign
> is identified at step M by route 2, route 1
> having been attempted and failed. Candidate
> K-1 therefore passes R-1 through R-5 and
> enters the lifecycle at the created stage,
> untested. No statement about what sign 821
> means is made.

## 1. What was executed

The frozen contract's execution shape (spec
§13), in order. Graph-first build (H15/H23):
experiment script
`backend/scripts/phase425_sign821_identification.py`;
graph module
`backend/glossa_lab/experiment_graph_phase425.py`
(node `IndusPhase425Sign821Identification`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The run's own
records: `reports/phase425_results.json`
(SHA-256
`c7b246e94258519e251acaf3a97179de02da1e453f01ef37945cca2a48737752`)
and `reports/phase425_identification_report.md`
(SHA-256
`67f753bfaeb448fd69ac0dde362d70907a03ea093f5f63917214343cae63e15b`);
the script is deterministic and a second run
reproduced both output files byte-identically.
The evidence of record:
`specs/063-sign821-identification-successor/identification-record.md`
(SHA-256
`4a0d62a6337daac2293d42e1e9cd77de40d027353223a189c7e2a984f6810c16`)
— the gate record, both derivation sheets,
the reconciliation and comparison, the step C
statement, and the route record with the
traps asserted, in full.

**Headline (spec §6.1 wording, RECOVERED
form).** "Identification of the drawn sign on
the new record (preserved drawn-form reference
`drawn-form-reference-821.json`, digest
695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999)
completes the recovery Spec 056 could not
finish. Candidate K-1 — ‘sign 821, in the
Dholavira signboard contexts, has a meaning of
‘city’, either as a determinative or as a
word’ (Wells 2015, printed p. 92) — passes
R-1 through R-5: the argument conditions stand
as adjudicated in Spec 056's executed record,
and R-3 is satisfied under Spec 063 §5 by route
2 (the list's own entry, through the preserved
reference), the sign list named from the
document itself (Wells 2011, as given in Wells
2015, Chapter 2 / Figure 2.6). Falsification
condition, from the passage's own logic: sign
821 in Dholavira signboard contexts shown to
carry a different established value, or the
signboard sequence's locative (place-name)
element shown to be carried by other signs,
with sign 821 outside it — with the passage's
own ruling respected, that the non-attestation
of eyil-ay / eyil-i is not a nullification of
the reading and cannot serve as the condition.
The claim enters the lifecycle at the created
stage, untested, as an appended restatement on
the fragment's own record; a test design is
recorded with it and no test has been run.
Recovery establishes that the passage argues
this and that its subject is identified in the
program's claim form — it establishes nothing
about whether the argument is right, and
nothing about what sign 821 means."

**The preserved reference (spec §8, element
1).**
`specs/063-sign821-identification-successor/drawn-form-reference-821.json`,
schema `glossa.drawn-form-reference/1`,
SHA-256
`695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999`
(5,689 bytes) — the freeze-pinned digest,
recomputed at gate 0.1. Text only; no image
is committed anywhere in this spec, and none
was committed by this execution.

**Fence sentence (spec §8, element 8).**
"This act is identification on a preserved
reference. It establishes, at most, whether
the drawn sign candidate K-1 names is
identified in the program's claim form —
never whether K-1's suggested meaning is
right, and nothing about sign 821 itself
beyond the identification."

## 2. Step 0, gate by gate (all passed)

- **0.1 Input integrity — PASS.** Every §2
  input was recomputed at the run's base and
  equalled its freeze-record value: held
  cleaned text `62acf855…`; crosswalk registry
  `8a0b2a82…`; Phase-123 witness `ecbc37a4…`;
  Spec 056 freeze file `8a7d1390…` (digest
  `64c28ce1…`); Spec 056 outcome `ff16184a…`;
  Spec 056 extraction record `ad4a3f74…`;
  Phase-104 evaluation `2d0b83e8…`; lane-2
  drafts `3f645c9a…`; anchors `df0cf620…`;
  preserved reference `695dd35d…`. The Spec
  063 freeze record's own digest asserted
  (`dc24a10e…`). The claim record was asserted
  in the Spec 038 form: its freeze-time hash
  `bd0f7abd…` stands as the definition
  constant in the Spec 063 `freeze.json`, and
  the fragment's facts were asserted on the
  live file — entry present, wording,
  UNTESTED status, created stage, and the
  appended `spec056_closure` entry present
  with outcome IDENTIFICATION FAILED. The
  passage of record (held-text lines
  2783–2871) recomputed to 5,354 bytes,
  SHA-256 `51d6fb3a…`. The phase script
  re-verifies all of this fail-closed before
  any output is written.
- **0.2 Thesis file asserted — PASS, before
  any plate was read.** The local file
  `Wells2006_PhD_EpigraphicApproachesToIndusWriting.pdf`
  (held locally under
  `downloads/wells-phd-thesis-2006/`; open
  deposit, not committed) recomputed to
  SHA-256
  `4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e`,
  19,313,853 bytes — the frozen pin exactly.
  No other copy, edition, or download was
  used.
- **0.3 Reference producible — PASS.** The
  preserved reference stands at its pinned
  digest, and the plate page — thesis p. 92 /
  PDF p. 104, Figure 3.2 — was produced from
  the pinned local file asserted at gate 0.2:
  the file carries 296 PDF pages, and page
  104's embedded plate image (`Im106.tiff`,
  47,034 bytes, SHA-256 `961ed7de…`) was
  extracted from that file and rendered for
  the step D readings. The render was an
  execution artefact only and is not
  committed.

## 3. Step D — descriptor derivation, twice

Two independent derivations of the drawn-form
descriptor from the produced plate, each
performed without sight of the other and
without sight of the preserved record's
drafted descriptor wording, each recording
the plate locator, the feature list it read,
and the neighbour set it discriminated against
(identification record, §§3–4). Derivation A
read the plate sequentially in row order;
Derivation B read the named neighbour set
first and then read the target against it.

Both derivations read the same drawn form:
**two identical tall (vertical) oval outlines
side by side, touching at the vertical
midline, each oval divided by three straight
diameters — one vertical, two diagonal — into
six sectors** (8 stroke elements in all: 2
outlines and 6 diameters), the pair being the
doubled form of the single oval at 820 on the
same row. Their neighbour discriminations
agree on all five named neighbours: 818 is a
single circle with 4 sectors; 820 is the
single oval itself; 822 is a single spoked
oval flanked by paired vertical strokes; 823
is a single oval with a denser-crossed
interior; 791 is two plain ovals with no
internal strokes.

Reconciliation by the recorded features
records **full agreement — no disagreement
arose, settled or unsettled**, so the
against-identification rule (DD-056-14,
carried) was not needed. The reconciled
descriptor was then compared with the
preserved record's descriptor: **agreement on
every feature; no material difference.** The
preserved descriptor is therefore sustained —
checked, not inherited. **Step D: PASS.**

## 4. Step C — continuity, by anchors

The run states, from the record, what anchors
the plate number to the 2011/2015 numbering
(identification record, §7):

1. **The formation passage** — the 2015
   book's own Appendix II text states that
   sign 820 doubles to form sign 821
   (held-text lines 3691–3704; the passage
   quoted verbatim in the identification
   record and verified against the pinned
   held text by the phase script).
2. **The registry's 2015-form cross-match** —
   row P378 carries `wells_ids` W820,
   `mahadevan_ids` M391, description "Wheel
   with 6 spokes with even angles".
3. **The plate agreement** — both step D
   derivations read the thesis plate at 820
   as a single six-sector wheel in an oval
   (the drawn form P378's description states),
   and at 821 as that wheel doubled.

The formation passage, the registry anchor,
and the two derivations all agree on the
doubled six-spoke-wheel form at 820/821. The
plate number by itself anchored nothing and
was used only to locate the entries.
**Step C: PASS — continuity is sustained on
the anchors' agreement.**

## 5. Step M — the match, and the recovery test

- **Route 1 (registry, by drawn form) —
  ATTEMPTED, FAILS.** The pinned registry's
  803 rows were searched on their drawn
  descriptions: no row carries W821 in any
  form, and no row describes the reconciled
  drawn form. Its only two "6 spokes"
  descriptions are P378 (a single wheel — the
  base sign 820) and P379 (a single flanked
  wheel — the plate's 822 form). The run did
  not fall back to P378, which is the base
  sign, not the target.
- **Route 2 (the list's own entry, through
  the preserved reference) — SATISFIED; the
  route that identifies the sign.** The
  preserved reference, at its freeze-pinned
  digest, sustained at step D and anchored at
  step C, is cited as the preserved drawn-form
  reference for the source list's own entry —
  Wells 2011, as given in Wells 2015,
  Chapter 2 / Figure 2.6 (printed pp. 19–22;
  held-text captions at lines 868, 872, 876,
  880). The sign list is named from the
  document itself (held-text lines 414 and
  665).
- **Route 3 (composition) — NOT USED.**
  Exactly one route identifies the sign, and
  the frozen routes are taken in order; route
  2 satisfied the match. (The formation
  passage and the plate confirmation appear
  in this run as step C anchors and as step
  D's plate — distinct acts from a step M
  route.)

**Traps asserted in the run record, by
name:** `Yunmapped_0821` (registry row:
`yajnadevam_glyphid`, empty `wells_ids`,
frequency 10, empty description — a number
collision, not Wells's 821; asserted as a
trap, never used as evidence); sign 861
(Figure 6.12; the passage associates it with
"city" as a different sign — a
reading-confusion trap; no evidence about it
was used); P378 used as the target's match
(it is the base sign; used only as the step C
anchor); and number-only matching in any
form (none was used, including a plate number
read without step C).

**The recovery test for K-1 (§4).** **R-1
PASS, R-2 PASS, R-4 PASS, R-5 PASS** — of
record in Spec 056's executed record on the
pinned passage (DD-063-2; not re-run under
this spec). **R-3 PASS** — run afresh under
§5 on the new record, as §§3–5 above record.
K-1's verbatim quote, verified verbatim
against the pinned passage by the phase
script: "It is suggested here that sign 821,
in the Dholavira signboard contexts, has a
meaning of ‘city’, either as a determinative
or as a word." (printed p. 92; held-text
lines 2835–2836.) Its R-4 falsification
condition and its R-5 numbers and conditions
are carried in full in the restatement append
(§7 below).

**Mapping (spec §6).** Step 0 passed, step D
sustained the reference, step C passed, and a
frozen route identified the sign, so K-1
passes R-1 through R-5: the outcome is
**RECOVERED**, by route 2. IDENTIFICATION
FAILED does not fire — no limb failed.
CLOSED AT STEP 0 does not fire — every gate
passed.

## 6. What this outcome does and does not establish

It establishes that the drawn sign candidate
K-1 names is identified in the program's
claim form on the new record, and that K-1 —
the proposition Spec 056's executed record
adjudicated on the pinned passage — is
therefore recovered as a claim in proper
form: stated from the passage's own argument,
about an identified subject in a named sign
list, with a falsification condition from the
passage's own logic and the passage's stated
conditions carried. The hypothesis of spec
§1.2 is **supported** on those terms
(F063-C03's verdict rule). It does **not**
establish anything about whether K-1's
suggested meaning is right: the recovered
claim enters at created, untested, and its
truth is a future act's question. It
establishes nothing about sign 821 itself
beyond the identification — not its reading,
classification, or distribution. Recovery is
not verification, and no output of this
execution presents the claim as supported,
checked, explained, or digested in the
lifecycle sense. Spec 056's IDENTIFICATION
FAILED stands unedited as the record of the
first run; this outcome is the successor
execution's own, appended under this spec.

**This does not establish:** that sign 821
means "city" or anything else; that Wells's
suggestion is correct, plausible, or checked;
anything about sign 861, sign 297, or any
other sign or claim; or anything about the
book's other sign-821 discussions (Chapter 3;
the appendices beyond the formation passage
used as a step C anchor and step M record).

## 7. Claim consequences (governed register)

Executed under register 0.6-draft (frozen);
one line per claim, F063-C01…C15.

- **F063-C01** (an outcome states nothing
  about sign 821 itself): HELD — the outcome
  states whether K-1 is recovered in form on
  the new record; it states nothing about the
  sign beyond the identification.
- **F063-C02** (candidate K-1 is the candidate
  of record): HELD — K-1 as Spec 056's
  executed record states it, asserted at gate
  0.1 on the pinned records; no other
  candidate was before this run and no new
  extraction pass was run.
- **F063-C03** (the drawn sign can be
  identified under §5): SUPPORTED — the
  execution's outcome is RECOVERED, the
  verdict rule this claim itself fixes for
  support.
- **F063-C04** (identification fails →
  IDENTIFICATION FAILED): NOT FIRED — its
  antecedent did not arise; identification
  succeeded at route 2, and no limb failed.
- **F063-C05** (the reference is preserved as
  the committed record in this directory):
  HELD — the record recomputed to its
  freeze-pinned digest `695dd35d…` at gate
  0.1 and was the reference the protocol
  checked.
- **F063-C06** (execution stops at step 0 if
  any pinned input fails): HELD — the gates
  ran in order before any derivation; all
  passed, so no step-0 closure arose.
- **F063-C07** (the descriptor derivation is
  performed twice independently): HELD —
  two sheets, each without sight of the other
  or of the drafted wording, feature lists
  and neighbour sets recorded, reconciliation
  by features, and the comparison made only
  after reconciliation (identification
  record, §§3–6).
- **F063-C08** (a candidate is a recovered
  claim only under §4's test): HELD — the
  conjunctive test was applied as written:
  R-1, R-2, R-4, R-5 of record, R-3 run under
  §5; K-1 passes every condition.
- **F063-C09** (sign 821 is identified only
  by a route §5 freezes): HELD — the match
  rests on route 2 exactly as frozen; route 1
  was attempted on drawn descriptions and
  failed without fallback to P378; route 3
  was not used; the traps were asserted by
  name, and no number match was used in any
  form.
- **F063-C10** (the headline outcome is
  assigned by §6's mapping alone): HELD —
  the wording is §6.1's RECOVERED form,
  filled from the run, and no outcome word
  outside §6 was used.
- **F063-C11** (a recovered claim enters at
  created, untested, with a
  designed-never-run test note): HELD — the
  restatement entry was appended to the
  fragment's own claim record as a new
  `spec063_restatement` entry (Phase-425,
  2026-10-22), carrying the recovered
  proposition, its verbatim quote and
  locator, the named sign list and the
  identification (route 2 and the preserved
  reference with its digest), the R-4
  condition, the R-5 numbers and conditions,
  and the test-design note; verification at
  the act: removing the appended entry
  reproduces the pre-act file byte-identically
  (pre-act live-file SHA-256 `997fa336…`;
  post-act `c8d7a687…`), and the claim's
  status and stage in the entry are untested
  and created, stated in the append's own
  lifecycle text. The full append is carried
  in `reports/phase425_results.json`
  (`claim_restatement_append`), so its
  prescribed form survives any future
  regeneration of the store.
- **F063-C12** (on a closure outcome,
  execution writes exactly §7's entries):
  NOT REACHED — no closure outcome arose;
  no closure entry was written.
- **F063-C13** (every product carries the §8
  reporting set): HELD — the preserved
  reference identified in full (§1), both
  derivation sheets and the reconciliation
  in full (identification record), the step C
  statement, the route used and the routes
  attempted with the traps asserted by name,
  the R-1…R-5 checklist with each condition's
  basis, the outcome word with its §6.1
  wording, the recovered claim exactly as
  appended (machine record), and the fence
  sentence (§1).
- **F063-C14** (no outcome establishes that
  sign 821 means "city"): HELD — see §6.
- **F063-C15** (Spec 063 appends records
  only): HELD — the §7 append was made to
  the fragment's own record as a new
  `spec063_restatement` entry; the fragment's
  original entry and its `spec056_closure`
  append stand above it, unedited. Spec
  056's spec, freeze, extraction record, and
  outcome were re-asserted at gate 0.1 to
  their pinned digests and were not edited
  or deleted at any point.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

**Foundation check (H21), reported as
measured.** Run in the execution worktree
after the run, with the two gitignored Holdat
CSVs copied in from the main checkout's local
store (never committed; the corpus CSV
SHA-256 `62d14d2b…` equals the pin recorded
at Spec 056's landing): **40 checks passed,
0 failed, 8 warnings** — the standing figure.
The regenerated report is
`reports/foundation_check_report.json`.

## 8. Records

- Evidence: `specs/063-sign821-identification-successor/identification-record.md`
  (gate record, both sheets, reconciliation,
  step C statement, route record); results
  record: `reports/phase425_results.json`;
  report: `reports/phase425_identification_report.md`.
- Claim restatement append:
  `spec063_restatement` entry on the
  fragment's record (see F063-C11 above).
- Root LEDGER entry: "Spec 063 (Phase-425)"
  entry added with this record.
- No test was run on K-1 under this spec,
  and none arises: the test-design note in
  the restatement append is a design, and a
  test of the recovered claim is a future
  act under its own contract.
- CI and merge state: appended below after
  the record PR merges, in the predecessor
  pattern — this section is completed by
  append, not edited.

## Landing record — 2026-10-22

The execution pull request, PR #323 (`spec-063-execution`), was merged into main as merge commit de8a43e259e8592533adf5e4bbf1c1c1c339213e on 2026-10-22. The merge was made on CI run 39748439035, on head a5362fafa1d18ce134c0ae52357ba9fbb75a2b6a, in which all seven jobs concluded success: Backend tests (pytest); Frontend tests (Playwright); Evidence Graph script smoke tests; Indus public validation checks; Shell wrappers (ubuntu-latest); Shell wrappers (windows-latest); Shell wrappers (macos-latest). Two earlier genuine full-green runs stand in the PR's history — run 39744384721 on head 92170d31d3032d09a5b765a6b657b6a59ca58a84 and run 39747329548 on head 11549020c50e67315f92ccfec617672b94d66d15, each seven of seven jobs success — after which main advanced under the PR (Specs 065, 067 and 064 executing and landing in parallel) and the branch was re-merged and re-verified on the new head rather than merged on a stale green.

After the merge, the run digests were re-verified on main through the contents API: reports/phase425_results.json at SHA-256 c7b246e94258519e251acaf3a97179de02da1e453f01ef37945cca2a48737752, reports/phase425_identification_report.md at SHA-256 67f753bfaeb448fd69ac0dde362d70907a03ea093f5f63917214343cae63e15b, and this spec's identification-record.md at SHA-256 4a0d62a6337daac2293d42e1e9cd77de40d027353223a189c7e2a984f6810c16 — all as run. The anchors file backend/reports/INDUS_FINAL_ANCHORS.json stands at SHA-256 df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569, byte-identical before and after the whole run. The appended restatement stands on main under spec063_restatement on the _0001 fragment entry, the claim at the created stage with status untested, Spec 056's spec056_closure above it unedited, and Spec 064's spec064_check append on the _0002 entry standing alongside it, likewise unedited.

Foundation check at the merge: 40 passed / 0 failed / 8 warnings, as measured on this run's execution tree and again on a locally assembled near-merged tree (the union ledger and union experiment graph, with one side of the claims-store union). The report committed on main is the regeneration made by Spec 064's landing on its own merge tree, so its claims-store hash names the store without this spec's append. A regeneration against the final union store was attempted and could not be completed: the VM's intermittent write restriction, which also blocked local git writes throughout this landing, prevented assembling the complete merged tree locally. The union store itself is verified — it is what stands on main, and removing either side's append from it reproduces the other side's file byte-identically — and no foundation check reads the append entries' contents (the check counts 31 claims in 10 files on every variant of the store). This note records the position rather than presenting the committed report as a regeneration on the final tree.

Landing mechanics, for the record: the two merges of main into the execution branch (11549020c50e67315f92ccfec617672b94d66d15 and a5362fafa1d18ce134c0ae52357ba9fbb75a2b6a) and this landing branch were built through the GitHub git-data API, because the write restriction blocked local git object writes; every union resolution was verified byte-exact in memory before its commit, and each branch ref was read back after its update. CI ran genuinely on each resulting head.

The terminal outcome stands as recorded in §6: **RECOVERED**. Recovery establishes that the passage argues this and that its subject is identified in the program's claim form — it establishes nothing about whether the argument is right, and nothing about what sign 821 means.


---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
