# Spec 048 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign plan,
>    approved by the owner AS WRITTEN on
>    2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
>    Parts 1–4 and 8 read in full at this draft).
>    The campaign commissions this draft:
>    member 3 (design D-04), Wave 1, dependents
>    second — drafted once the builder draft
>    (Spec 044, design D-02) had fixed Asset F's
>    contract; decision E-6 places Asset F's
>    build inside Spec 044 and its consumption
>    here; decision E-2 and requirement R-7
>    place this spec under the Roif gate.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-04 found **RIPE** — "The strict
>    corpus, the Phase-43 T2.4 measure, and the
>    Holdat second arm are all in hand. Nothing
>    in Specs 035–040 touched this claim."
> 3. **The Roif verification (post-plan,
>    2026-10-21).** Roif's preprint IS publicly
>    posted on Academia.edu and citable. This
>    satisfies at most one of the campaign
>    Part 8 gate's conditions; publication of
>    this spec's results remains a standing
>    GATE for the owner (claim F048-C14). The
>    verification is not a freeze order, not an
>    execution order, and not a publication
>    clearance.
>
> These inputs commission this **draft**. The
> freeze and the execution of Spec 048 are
> separate later owner acts, and — builders
> before dependents, campaign Part 4 — Spec
> 044's freeze and step 0 precede this spec's
> freeze, because this spec's freeze pin (Asset
> F's digest) is taken from Spec 044's step-0
> record.

## 1. The adopted basis (operative substance)

- **The design.** D-04 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
  §D-04): the fish family tested sign by sign
  under the Phase-43 T2.4 ending-follower
  measure on the strict corpus, repeated on
  the Holdat layer as a second arm — per-member
  PASS at 20% or more, family verdict by
  token-weighted passing share (70% / 30%
  lines), INCONCLUSIVE between or on a
  cross-arm disagreement about the most
  frequent member, 30-occurrence floor,
  frequency-matched non-fish animal controls,
  and the 72/64/70 sensitivity.
- **The claim.**
  `parpola_2010_dravidian_solution_manual_002`:
  IN QUESTION, partially supported — sign 72
  passed T2.4, sign 267 (the family's most
  frequent member) failed it; its
  not-understood text names this sign-by-sign
  run verbatim.
- **The asset.** Asset F, the fish-family list,
  built and frozen at Spec 044's step 0 from
  Parpola's published list (Spec 044 §4
  contract), consumed here by digest (campaign
  E-6, Part 3). This spec re-derives nothing
  about membership.
- **The measure.** Phase-43 T2.4, unchanged,
  reproduced against its recorded reference
  points at gate 0.3 before any member is
  judged.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
via the GitHub API against `main` (head
`83b6a563…`) and against Spec 044's draft
branch; the local checkout was not used:

- **Design D-04** — read in full: the question,
  hypothesis, falsifier (the token-weighted
  majority behaves like sign 267), data (strict
  corpus; Phase-43 framework; membership from
  Parpola's published list), method (T2.4 per
  member; Holdat second arm with per-sign
  crosswalk), fixed criteria (PASS at 20%;
  family lines 70% / 30%; floor 30; TOO THIN
  per member), controls (non-fish animal set;
  compilation second arm; frozen membership
  plus the 72/64/70 sensitivity), and the
  closing limit (no pronunciation conclusion).
- **Design D-02** — read in full, for the one
  line that touches this spec ("Fish family
  membership as frozen in D-04") — see §6,
  defect 1.
- **The claim record** — read on `main`:
  manual_002's normalized claim, status
  partially_supported, stage explained, its
  falsification condition, its sign_ids
  (Mahadevan 72, 64, 70), its T2.4 evidence
  line, its explanation (sign 72: 181
  occurrences, 25.9%; sign 267: 356, 3.8%; six
  fish candidates tried), and its
  not-understood text. File recomputed to
  SHA-256 `3202aeca…` at this draft.
- **The Phase-43 record** — read on `main`:
  `outputs/phase43_all.json` recomputed to
  SHA-256 `78a6c219…`; §T2_4_fish_rebus states
  fish_sign_candidates_tested [267, 72, 65, 59,
  60, 70], primary_fish_72 (total 181,
  terminal_frac 0.259, supported true),
  primary_fish_267 (total 356, terminal_frac
  0.038, supported false).
- **The strict sign set's census** — the
  anchors file recomputed to SHA-256
  `df0cf620…` (matching Spec 042's fresh
  recompute); 287 anchors, 94 carrying
  `strict_sa_independent`, 94 marked
  `strict_set`. Sign 72 carries **no anchor
  entry** — see §6, defect 3.
- **Spec 033's data statement** — read on
  `main`: the strict sign set is the 94
  strict readings in the anchors file; the
  corpus is "the program's V3/Mahadevan-lineage
  corpus as held in the database." That is the
  statement D-04's "strict corpus (the same
  strict sign set as D-03)" refers to, and the
  ground for gate 0.3's identify-and-pin form
  (DD-048-3).
- **Spec 044's Asset F contract** — read on
  branch `spec-044-fish-sign-coastal-residue-draft`
  (PR #243): spec §4 (canonical file
  `asset-f-fish-family.json`; nine required
  fields; `sign_key` is identity in Spec 044's
  pinned layer; Mahadevan and Parpola numbers
  are locators only; no locator, no entry;
  digest = SHA-256 of the canonical bytes with
  the `digest` field excluded) and §4.4
  (consumer states the digest in its own
  freeze, asserts it at its own step 0, and a
  mismatch is the consumer's step-0 closure);
  adjudication §3 (derivations C05/C06) and §6
  (defect 1, directing this draft not to cite
  the packet's direction as its basis).
- **The crosswalk pin** —
  `backend/glossa_lab/data/mahadevan_parpola_crosswalk.json`
  recomputed to `9ebd7723…`, matching Spec
  044's carried pin; its citation names
  Parpola 1994b, sign list (= Parpola 1994a
  fig. 5.1, pp. 70–78).
- **Not done at draft, by design** — Asset F
  has **not** been built (that is Spec 044's
  step 0; no member is named anywhere in this
  draft beyond the record's own reference
  signs), no digest exists to pin, no corpus
  layer has been identified beyond Spec 033's
  statement, no census has been computed, no
  rate of any kind was calculated, no code was
  written or run, the AEE hooks have not run,
  and nothing was filed with OSF.

## 3. Double derivation of acceptance tests (doctrine requirement)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived **twice,
independently, from the claim alone** —
Derivation A from the claim's operative
sentence, Derivation B from its falsifier /
outcome side — and disagreements were resolved
in the draft, here. Agreements are recorded in
one line; disagreements in full.

| Claim | Derivation A (from the claim) | Derivation B (from the falsifier/outcome side) | Result |
|---|---|---|---|
| C01 | Inspect outputs for any statement beyond per-member T2.4 behaviour in the two pinned arms | Inspect outputs for the excluded statements (pronunciation, meaning, coastal distribution, other corpora) appearing anywhere | **Agree** — one inspection, both directions; the claim's falsification test is that inspection. |
| C02 | Recompute the claim file's hash and read manual_002's status | Recompute the Phase-43 file's hash and read §T2_4_fish_rebus | **Agree** — both pins are required; the claim carries both. |
| C03 | Run §5; hypothesis supported iff the passing share is at least 70% with no cross-arm disagreement | Run §5; hypothesis fails iff the passing share is at most 30% (→ C04) | **Agree** — complementary by construction; the band between, and any cross-arm disagreement, is routed to INCONCLUSIVE under C10, not silently to either side. |
| C04 | Outcome record carries FAMILY NOT SUPPORTED wording when the condition holds | If passing members carry more than 30%, C04's condition does not arise (→ C10's other words) | **Agree.** |
| C05 | Gate-0.2 record exhibits the tested population as Asset F's members under the join | A member tested on a non-Asset-F basis, or an Asset F member silently omitted, breaks the population (→ INVALID) | **Disagreement, resolved.** A initially read D-04's own text — membership "fixed in advance from Parpola's published list (the record names Mahadevan signs 72, 64, 70, and the Phase-43 test's six fish candidates)", frozen "in the design's freeze step" — as this spec freezing its own list. B read campaign Part 3 / E-6 and Spec 044 §4 — "Frozen by D-02 at its own step 0, from Parpola's published list. Consumed by D-04… D-04 does not re-derive the list" — as the governing direction. **Resolution (DD-048-1):** the campaign plan, approved later and AS WRITTEN, governs; Spec 044 builds, this spec consumes by digest. The 72/64/70 trio and the Phase-43 six survive only as the gate-0.2 cross-check and the §5 sensitivity, exactly as Spec 044 §3's C05 resolution carries them on its side. The supersession is recorded again at §6, defect 1. |
| C06 | Step-0 record exhibits the exhibited file's recomputed digest beside the freeze pin, before any count | Any consumption of a different asset shows as digest drift against the freeze pin | **Agree** — ordering check + drift check are the same record read two ways. One sub-point carried from Spec 044 §3 C06: the digest excludes the `digest` field itself, since a self-referential hash has no fixed point; this spec recomputes under that same exclusion rule (§4) or its assertion would fail against a correctly built asset. A second sub-point is this spec's own: at draft there is no digest to state — the pin is taken at the freeze (OPEN-048-1), and gate 0.1 distinguishes a mismatched asset (DIGEST MISMATCH) from a not-yet-built one (NOT AVAILABLE), because the two closures say different things and must not be conflated. |
| C07 | Gate 0.3: identify, export, pin, reproduce the T2.4 reference points | A run counting on an unpinned or non-reproducing corpus is non-compliant on its face | **Agree** — but see DD-048-3: neither derivation could name the corpus as a repository file, because Spec 033 states it as held in the database. The draft states that plainly instead of pinning a plausible-looking wrong file. What "strict" restricts operationally divided the derivations — see §6, defect 3, and OPEN-048-2. |
| C08 | Member verdicts follow mechanically from the per-member rates and the 20% bar | Gate 0.3's reproduction: a measure that misses the reference points is not T2.4, whatever its code says | **Agree** — with the design's own caveat carried as OPEN-048-3: the 20% bar is "confirmed at freeze against the T2.4 record before any new counting"; the draft carries 20% verbatim and invents no other value. |
| C09 | Gate verdicts precede quantities in the run record, in order | Any quantity preceding its gate falsifies compliance | **Agree.** |
| C10 | Headline derivable from both arms' per-member tables alone | Headline must match §6's pre-written wording for its class | **Agree** — with one draft completion recorded: the design names three family outcomes; the step-0 closure classes (TOO THIN as a headline, DIGEST MISMATCH, NOT AVAILABLE, NOT PINNABLE, SECOND ARM NOT RUNNABLE, INVALID) are this draft's fail-closed completion (DD-048-2), following Spec 044's DD-044-1 precedent. |
| C11 | Gate-0.5 census published before any follower quantity | A rate computed over a below-floor member, or past a no-member census, falsifies compliance | **Disagreement, resolved.** A read the design's floor as purely per-member: below-floor members are excluded, and if all are excluded the family figure is simply empty. B read the verdict rule: with no tested member the token-weighted share does not exist, so an empty figure cannot be adjudicated as any of the three family words. **Resolution (DD-048-2):** B governs — no mapped member clearing the floor closes the execution as TOO THIN with the census as its finding (Spec 044's gate-0.4 pattern). The freeze may overturn this openly (OPEN-048-6 is not needed; the item rides L5's confirmation of DD-048-2). |
| C12 | All members' dispositions and figures, both arms, controls, and sensitivity present at close | A headline following the sensitivity instead of the primary falsifies the boundary | **Agree.** |
| C13 | Control set frozen at gate 0.6, run identically, figures beside the family's | A FAMILY SUPPORTED record claiming reading-support while the controls match falsifies compliance | **Disagreement, resolved.** A read "pass at the same rate" as the controls' passing share equalling the family's within rounding. B read it as the controls matching or exceeding the family — anything weaker leaves a gap a reader could drive a support claim through. **Resolution (DD-048-7):** B's reading is carried in claim F048-C13 ("at or above"), stated as the draft's reading, and OPEN-048-5 puts both the comparison rule and the frequency-matching rule to the freeze before any counting. Either may be changed at freeze; neither may be changed after. |
| C14 | Campaign public-surface audit finds nothing from this spec | Campaign reporting uses only the held-under-gate naming, no result content | **Agree.** |
| C15 | Inspect outputs for pronunciation/meaning/wordplay/mechanism claims | An outcome presented as explaining sign 267 falsifies compliance | **Agree** — one inspection, both directions. |

## 4. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   spec §2 pin re-asserted against the merged
   record — or decline, leaving the claim with
   its split record exactly as it stands:
   partially supported, family untested as a
   family.
2. **OPEN-048-1 (the Asset F pin itself).**
   Take Asset F's digest from Spec 044's
   step-0 record and state it in this spec's
   freeze record. This is not a discretionary
   item: the freeze cannot complete without
   it, because gate 0.1 asserts against it.
   The freeze also confirms the exhibited
   file's canonical form and the digest-field
   exclusion rule were applied as Spec 044 §4
   states.
3. **OPEN-048-2 ("strict", operationally).**
   Confirm what the primary corpus restriction
   is: the draft's reading is the Phase-43
   V3 / Mahadevan-lineage corpus as held,
   identified and pinned at gate 0.3, with the
   T2.4 reproduction as the operative check —
   and **not** a restriction of counted signs
   to the 94 strict readings, which would
   exclude sign 72 itself (§6, defect 3). The
   freeze confirms this reading or states the
   restriction it intends, in terms gate 0.3
   can check, before any counting.
4. **OPEN-048-3 (the PASS bar).** Confirm the
   member bar at 20% against the T2.4 record,
   as the design directs, before any new
   counting. The bar may be changed at freeze;
   it may not be changed after.
5. **OPEN-048-4 (second-arm closure form).**
   Confirm DD-048-4 (a Holdat layer or
   crosswalk failure closes the whole
   execution as SECOND ARM NOT RUNNABLE,
   because the INCONCLUSIVE rule needs both
   arms) or rule openly that the primary may
   stand alone with the arm-missing case
   pre-written, before any counting.
6. **OPEN-048-5 (control set rules).** Fix the
   frequency-matching rule for selecting the
   non-fish animal controls and confirm
   DD-048-7's "same rate" comparison (controls'
   token-weighted passing share at or above
   the family's), before any counting.
7. **OPEN-048-6 (OSF).** Whether the frozen
   spec files its own OSF registration — under
   campaign decision E-1, every specification
   in the pass gets its own OSF contract
   registration at its freeze, so the proposal
   is **yes**, following Specs 036–039. Nothing
   is filed at draft. Note: the OSF registration
   registers the frozen contract; it does not
   publish results, and the Roif hold
   (F048-C14) is unaffected.
8. **OPEN-048-7 (unmapped members).** Confirm
   DD-048-5 (a member with no Mahadevan mapping
   is UNMAPPED, listed, excluded from both
   arms' weighting, never counted as TOO THIN)
   or state the freeze's rule for such a
   member, before any counting.
9. **OPEN-048-8 (phase number).** Allocate the
   execution phase number at the freeze act,
   from the merged record as it then stands
   (DD-048-6).

## 5. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-048-1 — The campaign's direction
  governs membership.** Spec 044 builds Asset
  F; this spec consumes it by digest (§3
  derivation C05; §6, defect 1).
- **DD-048-2 — Step-0 closures complete the
  outcome set, and an empty census closes
  TOO THIN.** Design D-04 names three family
  outcomes; the frozen-spec form requires a
  pre-written wording for every way an
  execution can end. The draft adds TOO THIN
  (gate 0.5), ASSET F DIGEST MISMATCH and
  ASSET F NOT AVAILABLE (gate 0.1), STRICT
  CORPUS NOT PINNABLE (gate 0.3), SECOND ARM
  NOT RUNNABLE (gate 0.4), and INVALID, each
  with §6 wordings (claims C09–C11) — the
  Spec 044 DD-044-1 precedent.
- **DD-048-3 — No invented corpus pin.** Spec
  §2 pins what was verified and says why the
  strict corpus and the Holdat layer carry no
  pin at draft; gates 0.3 and 0.4 do the
  pinning as fail-closed acts.
- **DD-048-4 — The second arm is integral.**
  A Holdat failure closes the execution,
  because §6's inconclusive rule compares the
  arms on the most frequent member; a
  primary-only verdict could not state whether
  that clause fired. OPEN-048-4 puts this to
  the freeze.
- **DD-048-5 — UNMAPPED is its own
  disposition.** A member whose `sign_key` is
  keyed to Spec 044's layer and which carries
  no Mahadevan locator cannot be counted in
  either of this spec's numberings; it is
  listed and excluded, never silently dropped
  and never misreported as thin.
- **DD-048-6 — No execution phase number at
  draft.** Allocated at the freeze act.
- **DD-048-7 — "Same rate" for the controls
  means at or above the family's passing
  share** (§3 derivation C13; OPEN-048-5).
- **DD-048-8 — Evidence carries `observed_at`
  from the draft.** The cited facts were
  verified first-hand today (the Spec 042
  DD-042-4 / Spec 044 DD-044-8 precedent).

## 6. Design defects and ambiguities found at drafting

Recorded per the campaign rule that a defect
is reported, never repaired silently:

1. **The packet reverses the Asset F direction
   — twice.** Design D-02's data note says
   fish membership is "as frozen in D-04," and
   design D-04's own data note says membership
   is frozen "in the design's freeze step."
   The campaign (E-6, Part 3) and the triage
   supersede both: D-02 (Spec 044) builds
   Asset F at its step 0; D-04 (this spec)
   consumes it by digest and re-derives
   nothing. This draft follows the campaign,
   as Spec 044's adjudication (§6, defect 1)
   directs, and records the packet lines as
   superseded. (This is the same defect Spec
   044 recorded from its side; it is recorded
   here too because D-04's own text is one of
   the reversed statements.)
2. **Spec 044's draft names this consumer
   "Spec 045."** Spec 044 §4 and its header
   were written when D-04 was expected to be
   Spec 045; that number was taken by design
   D-05's draft (PR #244), and this spec is
   Spec 048 under the campaign's drafting
   order. No substance turns on it — the
   contract is by digest, not by number — but
   a reader following Spec 044's cross-reference
   should land here, and this note is the
   landing record. Spec 044's frozen text, if
   it carries the number, is not edited by
   this spec.
3. **"Strict corpus" cannot mean a
   strict-sign-set restriction as written.**
   D-04's data note says "the strict corpus
   (the same strict sign set as D-03)," and the
   claim's not-understood text says the test
   runs "on the strict corpus." But the strict
   sign set of D-03 is a set of *readings* (the
   94 `strict_sa_independent` anchors), and
   sign 72 — the family's reference passer,
   whose 20% bar and reproduction values this
   test is built around — carries no entry in
   the anchors file at all (verified at this
   draft). A corpus restricted to the strict
   set would exclude the very sign the measure
   must reproduce. The draft therefore reads
   "strict corpus" as the V3 / Mahadevan-lineage
   corpus of Spec 033 §4, identified and pinned
   at gate 0.3 with the T2.4 reproduction as
   the operative check, and puts the question
   to the freeze as OPEN-048-2 rather than
   resolving it silently.
4. **Phase-43's own fish-candidate set is
   internally uneven.** T2.4's tested list is
   [267, 72, 65, 59, 60, 70], but the same
   record's T2.1 table describes sign 59 as
   "Jar + handle," not a fish form, while sign
   89 ("Double fish") was not among the six
   tested. This is one more reason the claim
   record's lists cannot govern membership —
   and it is exactly the discretion Asset F's
   published-list freeze exists to remove.
   This spec takes no position on any
   individual sign; the gate-0.2 cross-check
   reports whatever divergence Asset F shows
   against both lists.
5. **The design's PASS bar is stated and
   deferred in the same sentence** ("20% or
   more… the exact bar is confirmed at freeze
   against the T2.4 record"). Carried verbatim
   at 20%, with the confirmation made an
   explicit freeze item (OPEN-048-3); nothing
   in this draft treats the bar as settled
   beyond the design's own words.
6. **Asset F's `sign_key` is keyed to a
   different corpus than either of this spec's
   arms.** Spec 044 §4.2 keys membership
   identity to "the pinned corpus layer of
   record" of Spec 044's coastal test. This
   spec counts in Mahadevan numbering
   (primary) and Holdat numbering (second
   arm). The join therefore runs through the
   `mahadevan_number` locator (gate 0.2), and
   a member without one is UNMAPPABLE to this
   spec's arms (DD-048-5; OPEN-048-7). The
   asset contract is not defective — locators
   are its stated mechanism — but a consumer
   draft that assumed `sign_key` was a
   Mahadevan number would have built its
   counting on the wrong key, so the join is
   written as an explicit, gated act here.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
