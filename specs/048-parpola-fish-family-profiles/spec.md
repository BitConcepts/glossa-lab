# Spec 048 — Parpola's Fish-Sign Family, Sign by Sign (Design D-04)

> ## FROZEN — 2026-10-21
>
> Frozen at the freeze act of 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on
> 2026-10-21 (Wave 2 freeze wave; campaign
> decision E-1 covers this spec's OSF contract
> registration, filed at this freeze —
> `osf-spec-registration.md`). The OPEN items
> of `adjudication.md` §4 are resolved on the
> record in `adjudication.md` §7 (DD-048-9 to
> DD-048-18); DD-048-1 to DD-048-5 and
> DD-048-7 are confirmed as drafted. The AEE
> lifecycle hooks ran over the register before
> this freeze (`aee/freeze-aee-note.md`), and
> the digest in `freeze.json` was computed
> exactly once over the frozen contract.
> Execution is **Phase-408**, run under this
> frozen contract only after the freeze has
> merged, the OSF registration's approval act
> has completed, and a separate execution order
> is given. At the freeze itself no sign has
> been counted, no corpus layer has been
> pinned, and Asset F has not been built.
>
> This spec is campaign member 3 (design
> D-04) and a **consumer of Asset F**, the
> frozen fish-family list built by Spec 044
> (design D-02) at its step 0. This spec does
> not build, re-derive, or repair Asset F.
>
> **Asset F pin (coordinator's pin-timing
> ruling, DD-048-9).** Asset F is built at
> Spec 044's EXECUTION step 0 (Wave 3), so
> neither the asset nor its byte-digest exists
> at this freeze. This freeze therefore:
> (a) quotes Spec 044's freeze digest as the
> contract anchor — `6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f020fcf25691d9c8`,
> read at this freeze from PR #243's branch
> (Spec 044's freeze had not yet merged when
> read; its corrected digest, superseding its
> first freeze digest under its own pre-merge
> test repair, recorded in its `freeze.md`
> §5); (b) fixes the pin SOURCE as Spec 044's
> step-0 outcome record for the canonical file
> `specs/044-fish-sign-coastal-residue/asset-f-fish-family.json`
> (Spec 044 §4.1, §9); and (c) rules that
> gate 0.1 asserts the Asset F byte-digest at
> EXECUTION step 0 against that record —
> absence closes ASSET F NOT AVAILABLE, a
> mismatch closes ASSET F DIGEST MISMATCH,
> exactly as drafted. The fail-closed
> semantics do not change; only the pinning
> moment moves, forced by the campaign's wave
> order.
>
> **Roif gate (campaign Part 8 / R-7).** This
> is a Roif-claim experiment (campaign member
> 3; D-02 and D-04 are the fish-sign pair).
> Roif's preprint verification has landed —
> publicly posted on Academia.edu, citable —
> but publication of this experiment's results
> remains the owner's separate GATE. Records
> under this spec are internal; nothing is
> published or surfaced from this spec's
> results under this campaign; reporting names
> this member only as "executed — held under
> the Roif gate" (§7, limit 1; claim
> F048-C14).

**Design source:** D-04 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
§D-04, read in full at this draft), with the
portfolio triage of 2026-10-21 (design D-04
found RIPE: "The strict corpus, the Phase-43
T2.4 measure, and the Holdat second arm are all
in hand. Nothing in Specs 035–040 touched this
claim.").

**Claim under test:**
`parpola_2010_dravidian_solution_manual_002`
— "The fish sign (meen in Dravidian) is the
primary rebus sign in the Indus script" —
standing **IN QUESTION, partially supported**:
Mahadevan sign 72 passed its Phase-43 T2.4
positional test; sign 267, the family's most
frequent member, failed it clearly.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The claim says *the fish sign* — a family of
related fish signs — works as the script's
primary sound-sign (the 'meen' reading). The
program's Phase-43 test T2.4 asked whether the
signs that follow a fish sign behave the way
case endings should if the fish sign were a
word being read aloud. The recorded result is
a split family (read first-hand at this draft
from `outputs/phase43_all.json`, §T2_4_fish_rebus):

- **Sign 72** — 181 occurrences, ending-follower
  (terminal) fraction **25.9%**, recorded
  supported.
- **Sign 267** — 356 occurrences, ending-follower
  fraction **3.8%**, recorded not supported;
  the family's most frequent member.
- Six fish candidates were tested in total:
  **267, 72, 65, 59, 60, 70** (the Phase-43
  record's own list).

The claim's not-understood text names exactly
what would change the picture: "the same test
run sign by sign across the whole fish family
on the strict corpus, with the family's
membership fixed in advance, and an account of
why sign 267 behaves differently if the
family's reading is uniform." This spec is
that test. Its family membership is fixed in
advance by Asset F — built by Spec 044 from
Parpola's published list — not by this spec,
and not by the claim record's shorthand lists
(§4; adjudication §6, defect 1).

### 1.1 The question, in plain words

One member of the fish family behaves as the
'meen' reading predicts; the commonest member
does not. Is the family uniform — most fish-sign
occurrences followed by text-ending behaviour —
or was the one pass the exception?

### 1.2 The hypothesis and its falsifier

**Hypothesis.** If the fish family carries one
reading, its members should share the
positional behaviour the reading predicts:
what follows a fish sign should look like word
endings at similar rates across the family —
specifically, members carrying at least 70% of
the family's total occurrences pass the §5
member criterion.

**Falsifier.** The hypothesis fails if the
family's token-weighted majority behaves like
sign 267 rather than sign 72 under §6 — that
is, if members carrying 30% or less of the
family's total occurrences pass, so most
fish-sign occurrences are *not* followed by
text-ending behaviour.

## 2. Inputs (pinned at this draft where a pin exists; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json`) | SHA-256 `3202aeca1ddaf7e588ebf19b2eaf8c93d06a34ecebba20d06c1b22810dfb000c` (recomputed at this draft from `main`, head `83b6a563…`). |
| Phase-43 results (`outputs/phase43_all.json`) — the T2.4 measure of record and its reference points | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (recomputed at this draft). T2.4: candidates [267, 72, 65, 59, 60, 70]; sign 72 — 181 occ., terminal_frac 0.259, supported; sign 267 — 356 occ., terminal_frac 0.038, not supported. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) — the strict sign set's census source | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). Census read at this draft: 287 anchors, 94 carrying validation status `strict_sa_independent`. This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| Mahadevan–Parpola crosswalk (`backend/glossa_lab/data/mahadevan_parpola_crosswalk.json`) — the locator source joining Asset F members to corpus numbering | SHA-256 `9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b` (recomputed at this draft; matches the pin Spec 044's draft carries). Its citation names Parpola 1994b, sign list (= Parpola 1994a fig. 5.1, pp. 70–78). |
| **Asset F** — the fish-family list, built and frozen at Spec 044's step 0 under Spec 044 §4's contract | **No byte-digest exists at this freeze** (the asset is built at Spec 044's execution step 0, Wave 3). Contract anchor: Spec 044's freeze digest `6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f020fcf25691d9c8` (read from PR #243's branch at this freeze; DD-048-9). Pin source: Spec 044's step-0 outcome record for `specs/044-fish-sign-coastal-residue/asset-f-fish-family.json`. Gate 0.1 asserts the byte-digest at execution step 0 against that record. See §4. |
| Strict corpus (primary arm) — the V3 / Mahadevan-lineage corpus the Phase-43 framework ran on, with the strict sign set of design D-03 | **No file pin is stated at this draft, deliberately.** Spec 033 §4 states this corpus as "the program's V3/Mahadevan-lineage corpus as held in the database" — a database posture, not a pinnable repository file on `main`. The layer is therefore identified, exported, and pinned by digest at step 0, before any counting, under gate 0.3 — and the run closes if it cannot be (DD-048-3; OPEN-048-2). Inventing a pin at draft would repeat the stale-pin failure Spec 040's gate record documents. **Freeze confirmation (DD-048-10, OPEN-048-2):** "strict corpus" names this V3 / Mahadevan-lineage corpus (Spec 033 §4), identified and pinned at gate 0.3 with the T2.4 reproduction as the operative check; it is not a restriction of counted signs to the 94 strict readings. |
| Holdat layer (second arm) — the other great compilation's numbering, with the crosswalk stated per sign | **No pin at this draft, for the same reason.** The repository holds Holdat-derived files but no single layer file is asserted here as the second arm's corpus; it is identified and pinned at gate 0.4, with the per-sign crosswalk stated in the step-0 record. Failure closes the run as SECOND ARM NOT RUNNABLE (DD-048-4; OPEN-048-4). |

## 3. Step 0 — gates before any fish sign is counted (fail-closed)

Execution runs these gates in order, before any
member's ending-follower rate is computed in
either arm. A failure stops the execution in
the class named; nothing is repaired at run
time, and no count produced before a gate
failure is quotable.

- **0.1 Asset F digest assertion.** The
  execution exhibits Asset F's canonical file
  (`asset-f-fish-family.json`, preserved in
  Spec 044's directory), recomputes its SHA-256
  over the canonical bytes **with the `digest`
  field excluded** (Spec 044 §4.2's exclusion
  rule), and compares it to the digest recorded
  in Spec 044's step-0 outcome record — the pin
  source this freeze fixes (DD-048-9; the
  contract anchor is Spec 044's freeze digest,
  §2). If the file or
  Spec 044's step-0 record does not exist, the
  run closes as **ASSET F NOT AVAILABLE** (§6
  wording) — a dependency closure, not a
  verdict. If the recomputed digest differs
  from the digest in that record, the run closes as
  **ASSET F DIGEST MISMATCH** (§6 wording).
  The asset is never rebuilt, re-derived, or
  substituted under this spec, in either case.
- **0.2 Membership join and cross-check.** Each
  Asset F member is joined to the primary
  corpus's numbering by its `mahadevan_number`
  locator, through the §2 crosswalk. A member
  carrying no Mahadevan mapping is recorded
  **UNMAPPED**, listed in the step-0 record
  with the reason, and excluded from both arms'
  weighting — it is not silently dropped, and
  it is not counted as TOO THIN (DD-048-5;
  OPEN-048-7). The step-0 record also reports
  the cross-check Spec 044 §3 requires in
  reverse: Asset F's membership against the
  claim record's named trio (Mahadevan 72, 64,
  70) and the Phase-43 six candidates (267,
  72, 65, 59, 60, 70), with every divergence
  named. The cross-check adds and removes no
  member.
- **0.3 Strict corpus identification, pin, and
  measure reproduction.** The primary corpus
  layer is identified from the database as the
  V3 / Mahadevan-lineage layer the Phase-43
  framework used, exported in full, and pinned
  by SHA-256 in the step-0 record. The gate
  then re-derives the T2.4 reference points
  from the pinned layer under the Phase-43
  record's own definitions: sign 72 — 181
  occurrences, ending-follower fraction 25.9%
  (within the record's rounding); sign 267 —
  356 occurrences, 3.8%. If the layer cannot
  be uniquely identified, cannot be exported
  whole, or the reference points do not
  reproduce, the run closes as **STRICT CORPUS
  NOT PINNABLE** (§6 wording) and nothing is
  counted.
- **0.4 Holdat layer and crosswalk pin.** The
  second arm's layer is identified and pinned
  by digest, and the crosswalk from Asset F
  members (via their Mahadevan locators) to
  Holdat numbering is stated per sign in the
  step-0 record, with crosswalk-conflict pairs
  named — never silently dropped (Phase-125's
  caution). If the layer cannot be identified
  and pinned, or a tested member's crosswalk
  cannot be stated, the run closes as
  **SECOND ARM NOT RUNNABLE** (§6 wording).
- **0.5 Census (margins only).** Per mapped
  Asset F member, the total occurrence count
  in the pinned primary corpus is computed —
  occurrence counts only, no follower quantity.
  Members below 30 total occurrences are
  recorded TOO THIN per member, with counts,
  and excluded from the §6 weighting. If **no**
  mapped member clears the floor, the
  execution closes as **TOO THIN** (§6 wording)
  with the full census as its finding — the
  token-weighted rate the verdict turns on
  does not exist.
- **0.6 Control set freeze.** The control set —
  non-fish animal signs, matched for frequency
  — is enumerated in the step-0 record before
  any follower quantity is computed for any
  sign: each control named with its published
  identification source and its primary-corpus
  total. A control below 30 occurrences is
  excluded with its count stated. The matching
  rule is the one fixed at the freeze
  (DD-048-13, OPEN-048-5): a control qualifies
  iff its published animal identification is
  citable from the program's records, its
  primary-corpus total is at least 30, and its
  total lies between half the smallest tested
  member's total and twice the largest tested
  member's total. The
  set, once recorded here, does not change
  after any result is seen.

## 4. Asset F — the consumed contract (Spec 044 §4, restated for the consumer)

This spec consumes Asset F exactly as Spec 044
froze it; this section restates the contract
only so the consumer's obligations are in one
place. Spec 044's text governs in any conflict.

- **Form.** One canonical JSON file,
  `asset-f-fish-family.json` (UTF-8, keys
  sorted, members sorted by `sign_key`),
  built once at Spec 044's step 0 solely from
  Parpola's published list (Parpola 1994,
  fig. 5.1).
- **Identity.** The SHA-256 of the canonical
  bytes, with the file's `digest` field
  excluded from the hashed bytes. That digest,
  as recorded in Spec 044's step-0 outcome
  record, is the asset's only authoritative
  identity. Under the pin-timing ruling
  (DD-048-9) this freeze quotes Spec 044's
  freeze digest as the contract anchor and
  fixes that step-0 record as the pin source;
  gate 0.1 asserts the byte-digest against it
  at execution step 0.
- **Members.** Nine required fields per member:
  `sign_key` (the member's identity — its
  identifier in Spec 044's pinned corpus layer
  of record); `mahadevan_number` and
  `parpola_number` (locators only, never
  membership criteria); `depiction_note`;
  `source_citation`; `source_locator` (no
  locator, no entry); `inclusion_basis`;
  `contested`; `notes`.
- **Join rule for this spec.** Because
  `sign_key` is keyed to Spec 044's layer, a
  member enters this spec's counting through
  its `mahadevan_number` locator and the §2
  crosswalk (gate 0.2) — for the primary arm
  directly, and for the Holdat arm through the
  per-sign crosswalk gate 0.4 states. The
  asset itself is not edited to make the join
  easier.
- **Direction of the contract.** The design
  packet's D-02 text says fish membership is
  "as frozen in D-04." That direction is
  **superseded** by the campaign (decision
  E-6, Part 3): D-02 builds Asset F, D-04
  consumes it. This draft follows the campaign
  and records the supersession in
  `adjudication.md` §6, defect 1, as Spec 044's
  adjudication (§6, defect 1) directs.

## 5. The test

**Primary arm (strict corpus, Mahadevan
numbering).** For every mapped Asset F member
with at least 30 occurrences in the pinned
primary corpus: compute the rate at which the
following sign is a text-ending sign — the
Phase-43 test T2.4 measure, **unchanged**,
under the definitions gate 0.3 reproduced the
reference points with. Report each member
separately (occurrences, followers counted,
ending-follower rate, PASS / does-not-pass)
and the token-weighted family rate over the
tested members.

**Member criterion.** A member **PASSES** at
an ending-follower rate of **20% or more** —
the level sign 72's recorded behaviour (25.9%)
establishes as the reading's signature, against
sign 267's 3.8%. The design fixes 20% and
directs that the exact bar be confirmed at
freeze against the T2.4 record before any new
counting. **Confirmed at the freeze
(DD-048-11, OPEN-048-3): the bar is 20%** —
it sits between sign 72's recorded 25.9%
(supported) and sign 267's recorded 3.8%
(not supported), exactly as the design fixed
it.

**Second arm (Holdat numbering).** The whole
test is repeated on the Holdat layer's
numbering, with the crosswalk stated per sign
at gate 0.4. Crosswalk-conflict pairs are
reported separately in both arms, never
silently dropped. The second arm's per-member
results are reported in full beside the
primary's.

**Sensitivity (reported alongside, never
verdict-changing beyond §6's stated rule).**
The family verdict recomputed using only signs
72, 64, 70 — the three the claim's own record
names — under the identical measure and
weighting, restricted to those members that
are Asset F members, mapped, and above the
floor. A sensitivity that contradicts the
primary is reported as contradicting it, in
the outcome record's first section.

**Control set.** The gate-0.6 controls run
through the identical measure. The control
comparison is the token-weighted share of
control occurrences carried by passing
controls, stated beside the family's figure.
If the controls pass at the same rate as the
family, the fish result is reported as a
positional fact, not as support for the
reading (§6's FAMILY SUPPORTED wording carries
both sentences; the one that applies is the
the one the control comparison selects, by the
rule fixed at the freeze (DD-048-13,
OPEN-048-5; DD-048-7's "at or above" reading
confirmed).

## 6. Criteria, outcome set, and pre-written verdict wordings

**Family rule (fixed in advance).** Over the
tested members (mapped, at or above the
30-occurrence floor), let the passing members'
share be the token-weighted share of the
family's tested occurrences they carry.

- **FAMILY SUPPORTED** — passing members carry
  at least **70%** of tested occurrences, and
  the two arms do not disagree under the
  inconclusive rule below.
- **FAMILY NOT SUPPORTED** — passing members
  carry **30% or less** of tested occurrences,
  and the two arms do not disagree under the
  inconclusive rule below.
- **INCONCLUSIVE** — the passing share is
  between 30% and 70%, **or** the two
  compilation arms disagree about the family's
  most frequent member (the most frequent
  tested member's PASS / does-not-pass status
  differs between arms).

The execution ends in exactly one headline
outcome. The outcome record's headline
paragraph uses one of these forms, with the
bracketed quantities filled from the run.
These wordings are written before any data is
touched; no other headline wording may be used.

- **FAMILY SUPPORTED:** "Tested sign by sign
  across the fish family fixed in advance by
  Asset F (digest [d]), members carrying [w]%
  of the family's tested occurrences pass the
  frozen ending-follower criterion (bar 20%):
  [per-member rates]. The family behaves, in
  its token-weighted majority, the way sign 72
  does and the way the 'meen' reading predicts.
  [Control sentence: either 'The frequency-matched
  non-fish animal controls pass at [c]% of their
  tested occurrences, below the family's rate'
  or 'The frequency-matched non-fish animal
  controls pass at the same rate ([c]%), so this
  result is reported as a positional fact, not
  as support for the reading.'] This does not
  establish that any fish sign was pronounced
  'meen': positional behaviour is a necessary
  shadow of the reading, not the reading."
- **FAMILY NOT SUPPORTED:** "Tested sign by
  sign across the fish family fixed in advance
  by Asset F (digest [d]), members carrying
  only [w]% of the family's tested occurrences
  pass the frozen ending-follower criterion
  (bar 20%): [per-member rates]. The family's
  token-weighted majority behaves like sign 267
  rather than sign 72. Sign 72's recorded pass
  stands as the exception it was recorded as,
  and the claim `parpola_2010_dravidian_solution_manual_002`
  is recorded as not supported as a family
  claim. This does not establish what any fish
  sign meant or was pronounced."
- **INCONCLUSIVE:** "Tested sign by sign across
  the fish family fixed in advance by Asset F
  (digest [d]), the result is inconclusive:
  [the passing members carry [w]% of tested
  occurrences, between the frozen 30% and 70%
  lines / the two compilation arms disagree
  about the family's most frequent member,
  [sign], which passes on [arm] and does not
  pass on [arm]]. [Per-member rates, both arms.]
  The claim stands exactly as recorded —
  partially supported, family split unresolved."
- **TOO THIN (step-0 closure, gate 0.5):**
  "Spec 048 closed at step 0, gate 0.5: no
  mapped Asset F member clears the
  30-occurrence floor in the pinned strict
  corpus ([census]). No ending-follower rate
  was computed. This closure is a statement
  about runnability, not about the claim; the
  claim stands exactly as recorded."
- **ASSET F DIGEST MISMATCH (step-0 closure,
  gate 0.1):** "Spec 048 closed at step 0,
  gate 0.1: Asset F as exhibited recomputes to
  digest [observed], which differs from the
  digest recorded in Spec 044's step-0 outcome
  record, [pinned]. No count was computed, and the
  asset was not rebuilt or substituted under
  this spec. This closure is a statement about
  the consumed asset's identity, not about the
  claim; the claim stands exactly as recorded,
  and any corrected asset is a new asset
  version usable only under a new freeze."
- **ASSET F NOT AVAILABLE (step-0 dependency
  closure, gate 0.1):** "Spec 048 closed at
  step 0, gate 0.1: Asset F does not yet exist
  as a frozen record — Spec 044's step 0 has
  not produced the canonical file and step-0
  record this spec's freeze fixed as its pin
  source (DD-048-9). No count was computed. This is a
  dependency closure, not a verdict; the claim
  stands exactly as recorded."
- **STRICT CORPUS NOT PINNABLE (step-0 closure,
  gate 0.3):** "Spec 048 closed at step 0,
  gate 0.3: the strict corpus layer of record
  could not be uniquely identified and pinned,
  or the pinned layer does not reproduce the
  Phase-43 T2.4 reference points ([reason]).
  No ending-follower rate was computed. This
  closure is a statement about runnability,
  not about the claim; the claim stands
  exactly as recorded."
- **SECOND ARM NOT RUNNABLE (step-0 closure,
  gate 0.4):** "Spec 048 closed at step 0,
  gate 0.4: the Holdat second arm could not be
  run as designed — [the layer could not be
  identified and pinned / the per-sign crosswalk
  could not be stated for [sign]]. No rate was
  computed in either arm. This closure is a
  statement about runnability, not about the
  claim; the claim stands exactly as recorded."
- **INVALID (integrity closure):** "Spec 048
  closed as INVALID: [the named §2 pin
  mismatched / the anchors assertion failed /
  the step-0 record does not precede the first
  count / a count was produced on an unmapped
  or unpinned basis]. No result is recorded
  under this spec."

## 7. Epistemic limits (binding on all outputs)

1. **The Roif hold.** This spec's records are
   internal. Nothing derived from this spec's
   results — no summary, article draft, status
   line, paper or website text, or public
   register wording — is published or surfaced
   under this campaign, in any form, until the
   owner clears the specific publication act
   under campaign R-7 / Part 8. Campaign
   reporting names this member only as
   "executed — held under the Roif gate,"
   without result content. (The verification
   that Roif's preprint is publicly posted and
   citable does not lift this hold; it is one
   of the gate's conditions, and the owner's
   cleared act is the other.)
2. **No pronunciation conclusion.** Even a
   FAMILY SUPPORTED outcome does not establish
   that any fish sign was pronounced 'meen',
   the fish/star wordplay, or the reading of
   any inscription. Positional behaviour is a
   necessary shadow of the reading, not the
   reading — the claim's own not-understood
   text states this limit, and every output
   carries it.
3. **No mechanism for sign 267.** A family
   verdict states how the members behave; it
   does not by itself explain *why* sign 267
   behaves differently. Any account of the
   difference is a separate, later act, named
   as such; no output of this spec presents a
   verdict as that account.
4. **Compilation-relativity.** Which drawn sign
   counts as "the fish sign" differs across
   compilations (Phase-125). The primary arm is
   a Mahadevan-numbering result; the Holdat arm
   is the design's control for exactly this,
   and the two arms' disagreement is a
   pre-written inconclusive outcome (§6), not
   a discrepancy to be averaged away. Phase-125
   found crosswalk-conflict pairs at 383 of
   762; conflicts are reported per sign.
5. **The strict-sign-set caution.** The strict
   sign set (94 `strict_sa_independent`
   readings) is a set of *readings*, and sign
   72 — this family's reference passer — is
   not one of them: its anchors entry (M072)
   carries validation status
   `pending_non_sa_validation`, not a strict
   reading (freeze correction, DD-048-18: the
   draft's "no entry in the anchors file" was
   imprecise — the entry exists; the strict
   status is what it lacks). No output may describe this
   test as restricted to the strict sign set:
   the freeze's OPEN-048-2 resolution
   (DD-048-10) confirms it is not.
6. Negative, inconclusive, thin, and
   step-0-closure outcomes publish (internally,
   under limit 1) with the same prominence as
   a supported finding.

## 8. Controls and named confounders

- **Position effects unrelated to sound
  values.** A sign could sit before endings for
  structural reasons. The gate-0.6 control set
  of non-fish animal signs, matched for
  frequency and run through the identical
  measure, is the design's control; its result
  travels with the family's in every wording
  (§5, §6).
- **Compilation disagreement.** The Holdat
  second arm, with the crosswalk stated per
  sign and conflict pairs reported separately,
  never silently dropped.
- **Family-definition discretion.** Removed
  from this spec entirely: membership is
  Asset F's, frozen by Spec 044 before any
  count in either spec's test existed, and
  pinned by digest at this spec's freeze. The
  72/64/70 sensitivity is pre-registered (§5),
  not a post-hoc redefinition.
- **Frequency.** The 30-occurrence floor per
  member, exact counts with every rate, and
  token weighting stated wherever a family
  figure is stated — one frequent member can
  neither carry nor sink the family silently,
  because its weight is printed.

## 9. Reporting obligations

Every product of an execution carries, in its
headline section:

1. Asset F's digest (the freeze pin, as
   asserted at gate 0.1) and member count, the
   mapped / UNMAPPED / TOO THIN disposition of
   every member, and the gate-0.2 cross-check
   against the claim record's trio and the
   Phase-43 six, with divergences named;
2. the corpus labels — the primary layer as
   pinned at gate 0.3 and the Holdat layer as
   pinned at gate 0.4, each with its digest;
3. per tested member, per arm: occurrences,
   followers counted, ending-follower rate,
   and the PASS / does-not-pass word; the
   token-weighted family rate and passing
   share per arm; the control set's figures;
   the 72/64/70 sensitivity;
4. the headline outcome word of §6, in §6's
   pre-written wording;
5. the Roif-hold sentence: "This record is
   internal under the campaign's Roif gate
   (R-7); it is not a publication."

Deliverables at execution: a results JSON
(step-0 record with all pins, the Asset F
digest assertion, the join and cross-check,
censuses, per-member tables for both arms,
controls, sensitivity), a report under these
headline rules, the experiment-graph node
(H15/H23, registered and verified before the
run), the outcome append in this directory,
and the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not. Anchors
asserted byte-identical before and after.

## 10. Stop conditions and outcome classes

Execution ends in exactly one of:

- **FAMILY SUPPORTED**, **FAMILY NOT
  SUPPORTED**, or **INCONCLUSIVE** — per §6,
  after all gates pass.
- **TOO THIN** — gate 0.5 (no mapped member
  clears the floor).
- **ASSET F DIGEST MISMATCH** — gate 0.1.
- **ASSET F NOT AVAILABLE** — gate 0.1
  (dependency closure).
- **STRICT CORPUS NOT PINNABLE** — gate 0.3.
- **SECOND ARM NOT RUNNABLE** — gate 0.4.
- **INVALID** — a §2 pin mismatches, the
  anchors assertion fails, or any count is
  shown to precede its gate or to rest on an
  unmapped or unpinned basis.

## 11. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — Asset F digest assertion;
   membership join and cross-check; strict
   corpus pin and T2.4 reproduction; Holdat
   pin and per-sign crosswalk; census; control
   set freeze.
3. **Primary arm** (§5) — per-member T2.4
   rates on the pinned strict corpus.
4. **Second arm and sensitivity** (§5) — the
   Holdat repeat; the 72/64/70 sensitivity;
   the control set.
5. **Outcome** (§9) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured; the claim's
   record gains its dated append (family
   verdict or closure) — under the Roif hold,
   as an internal record. Campaign order note:
  builders before dependents (campaign Part 4)
  — Spec 044's freeze precedes this freeze as
  the contract anchor (DD-048-9), and Spec
  044's step 0, which produces Asset F,
  precedes this spec's EXECUTION, not its
  freeze: the wave order forced the pinning
  moment to execution step 0 (gate 0.1).

## 12. What this spec is not

Not a build or re-derivation of Asset F (that
is Spec 044's step 0, and this spec consumes
the asset by digest only), not a re-run of
D-02's coastal test, not a test of what any
fish sign meant or was pronounced, not a new
corpus, not D-03's language comparison, and
not an authorisation to execute or to publish
anything. It is the family-level positional
test of one claim whose record currently
averages one pass and one failure, designed
so that its honest outcomes — including
closing at its own step 0 on the asset it
consumes — are written down before any sign
is counted.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
