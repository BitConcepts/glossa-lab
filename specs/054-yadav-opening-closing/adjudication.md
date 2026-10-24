# Spec 054 — Adjudication Record

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
>    Parts 1–4 read in full at this draft).
>    The campaign commissions this draft:
>    member 7 (design D-08), Wave 1, independent
>    members in parallel throughout. D-08
>    consumes no shared asset (Part 3:
>    "Everything else stands alone" — the
>    Phase-43 thresholds, the strict corpus,
>    the Holdat layer, and the crosswalk are
>    its only inputs). Campaign decisions
>    that touch this spec: E-5 (a step-0
>    failure closes this experiment, never
>    the pass) and R-6 (nothing from the pass
>    is published by the pass; claim
>    F054-C15).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-08 found **RIPE** — "Strict
>    corpus, Holdat layer, and crosswalk are
>    in hand; Phase-43 thresholds are on
>    record. The design's first product — a
>    falsifier written onto a record that
>    never had one — is available whatever
>    the rerun finds."
> 3. **Spec 045's draft (PR #244), DD-045-4.**
>    Spec 045 (design D-05) defines its
>    suffix/closing measure operationally in
>    its own §5.2 because D-08's measure was
>    not yet a frozen spec, and records that
>    at Spec 045's freeze the definition is
>    reconciled against D-08's frozen text if
>    one exists by then. The reconciliation
>    is therefore a two-sided touchpoint:
>    this draft records its side of it
>    (spec §5.2; OPEN-054-6 below).
>
> These inputs commission this **draft**.
> The freeze and the execution of Spec 054
> are separate later owner acts. The §4
> falsifier append is a freeze act: it is
> not performed by this draft.

## 1. The adopted basis (operative substance)

- **The design.** D-08 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
  §D-08): the Phase-43 positional battery
  rerun with its thresholds unchanged on the
  strict corpus (arm 1) and on the Holdat
  layer under its own numbering (arm 2),
  results mapped through the crosswalk with
  conflict pairs reported separately, overlap
  measured against a 999-shuffle label null,
  judged by the criteria fixed in the design
  (SUPPORTED (re-earned) / NOT SUPPORTED /
  INCONCLUSIVE), under the falsifier the
  design writes onto the claim's record at
  the freeze, in its own words.
- **The claim.**
  `yadav_2009_arxiv_manual_002` — "There are
  specific text-beginning and text-ending
  signs in the Indus corpus": strongly
  supported, stage explained, IN QUESTION in
  the packet's classification because its
  record carries no falsification condition
  (verified field by field at this draft,
  §2).
- **The falsifier.** The design's, verbatim
  (spec §1.2; claim F054-C04). This draft
  invents no falsifier of its own: the
  design writes it, and the spec's first
  drafting duty was to carry it exactly.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
via the GitHub API against `main` (head
`83b6a563…`) and against Spec 045's draft
branch; the local checkout was not used:

- **Design D-08** — read in full: the
  question, hypothesis, the falsifier stated
  verbatim (fewer than half of the original
  40/20 sets reappear on the strict corpus;
  cross-compilation overlap no more than the
  shuffle null; the effect disappears under
  the other compilation's segmentation),
  data (strict sign set and V3 corpus, arm 1;
  Holdat layer, arm 2; segmentation
  conventions per compilation as published),
  method (battery thresholds unchanged; 999
  shuffles), fixed criteria (SUPPORTED:
  both arms reproduce at least half and
  overlap exceeds the 95th percentile; NOT
  SUPPORTED: any falsifier condition fires;
  INCONCLUSIVE: one arm reproduces, the
  other does not), controls (segmentation as
  the named control; counts with rates; a
  minimum-occurrence floor identical in both
  arms), and the closing limit (no language
  conclusion, no meaning conclusion).
- **The claim record** — read on `main`:
  manual_002's normalised claim, status
  `strongly_supported`, stage `explained`,
  evidence line, not-understood text, and
  field set. File recomputed to SHA-256
  `90476623…` at this draft, and re-verified
  by a second, independent raw fetch with
  the same result. **The claim object
  carries no `falsification_condition` key**
  (checked by enumerating the object's
  fields); its companion manual_001 in the
  same file carries one ("If frequency
  distribution deviates from Zipf-Mandelbrot
  law"), so the absence is this claim's
  defect, not a file convention.
- **The Phase-43 record** — read on `main`:
  `outputs/phase43_all.json` recomputed to
  SHA-256 `78a6c219…` (the pin Specs 045 and
  048 also carry). §T1_1: V3 corpus, 3,916
  records, 3,137 sequences, 12,494 sign
  instances. §T2_2: terminal_strong_count 20,
  initial_strong_count 40, medial_strong_count
  61, total_signs_profiled 201 — and a
  `terminal_strong` list of **only 10
  entries** (signs 342, 176, 328, 211, 1,
  15, 254, 12, 60, 190; t_rates 0.683–0.892;
  totals 22–1,318), with **no
  initial-strong list at all**. The file
  states no threshold rule, no minimum
  count, and no classification definition
  for "strong" (§6, defect 1).
- **The companion positional record** —
  `hunt_tripartite_test.json` recomputed to
  `0e546962…` (Spec 045's pin): the same
  40/61/20 classes, mean initial rate 0.757,
  mean terminal rate 0.805, expected by
  chance 0.251, formula test 805 of 2,267
  inscriptions of length ≥ 3. Counts and
  summary rates only — again no membership
  lists and no threshold rule.
- **The crosswalk pin** —
  `data/crosswalks/parpola_mahadevan_crosswalk_v1.json`
  recomputed to `4e7559df…` and its `.csv`
  to `3d0b9ef1…`: Spec 019's frozen pins for
  the same files. The Phase-122 results
  record states 762 pairs, 383 conflict
  pairs, 209 conflict P-signs. (One fetch of
  that results file through the contents API
  returned inconsistent bytes at this draft;
  the file is therefore **not** pinned in
  spec §2 — its counts are cited through
  Spec 019's frozen record and the
  crosswalk files themselves, which were
  verified stable across repeated fetches.
  §6, defect 4.)
- **The strict sign set's census** — the
  anchors file recomputed to SHA-256
  `df0cf620…` (the fresh recompute Specs
  042, 045, and 048 also carry); 287
  anchors, 94 carrying
  `strict_sa_independent`.
- **Spec 033's data statement** — read on
  `main`: the strict sign set is the 94
  strict readings in the anchors file; the
  corpus is "the program's V3/Mahadevan-lineage
  corpus as held in the database." That is
  the statement D-08's "strict sign set and
  V3 corpus" refers to, and the ground for
  gate 0.3's identify-and-pin form
  (DD-054-3; the Spec 048 DD-048-3 precedent
  for the same phrase in design D-04).
- **Spec 045's §5.2 and DD-045-4** — read on
  branch `spec-045-hunt-depicted-kinds-draft`
  (PR #244): §5.2(a) defines suffix-like
  behaviour operationally as the
  distinct-predecessor rate in final
  position; DD-045-4 records that the
  freeze of Spec 045 reconciles that
  definition against D-08's frozen
  definition if one exists by then. This
  spec's closing-sign measure is different
  (terminal-strong set membership under the
  Phase-43 battery) — spec §5.2 states the
  difference and the touchpoint.
- **Neighbouring batteries are not
  Phase-43's** — read at this draft:
  `phase113_battery.py` (frozen constants
  T1_TV_MAX 0.40, T2A_TV_MAX 0.35, … — the
  non-SA validation battery of Specs
  011/015–017) and the generic positional
  pipeline (`exclusive` classification,
  floor ≥ 3). Neither is the Phase-43
  battery; neither's constants are borrowed
  anywhere in this draft (§6, defect 1).
- **Not done at draft, by design** — the
  original sets have **not** been exhibited
  (gate 0.2's act; the counts only were
  read), no corpus layer has been identified
  beyond Spec 033's statement, no census
  has been computed, no rate of any kind was
  calculated, no code was written or run,
  the falsifier has **not** been appended
  to the claim record (that is the freeze's
  act, §4 of the spec), the AEE hooks have
  not run, and nothing was filed with OSF.

## 3. Double derivation of acceptance tests (doctrine requirement)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived **twice,
independently, from the claim alone** —
Derivation A from the claim's operative
sentence, Derivation B from its falsifier /
outcome side — and disagreements were
resolved in the draft, here. Agreements are
recorded in one line; disagreements in full.

| Claim | Derivation A (from the claim) | Derivation B (from the falsifier/outcome side) | Result |
|---|---|---|---|
| C01 | Inspect outputs for any statement beyond the two-arm reappearance/overlap test | Inspect outputs for the excluded statements (language, meaning, other corpora) appearing anywhere | **Agree** — one inspection, both directions; the claim's falsification test is that inspection. |
| C02 | Recompute the claim file's hash and read manual_002's status and stage | Enumerate manual_002's field set for a falsification field | **Agree** — with a sharpening from B: a search for the string would miss a renamed field, so the draft's verification enumerated the object's fields; the claim's falsification test carries both the hash and the field reads. |
| C03 | Run §5; hypothesis supported iff both arms reproduce both sets at half or better and the overlap clears the 95th percentile | Run §5; hypothesis fails iff a falsifier condition fires (→ C04/C10) | **Disagreement, resolved.** A read the design's SUPPORTED criterion literally per arm ("both arms reproduce at least half the original sets" — sets pooled per arm, so an arm reproducing 35 of 60 pooled signs passes). B read the falsifier ("fewer than half of the original 40/20 sign sets reappear" — the two sets named separately) as per-set: each set must reach its own half, in each arm. **Resolution (DD-054-1):** B governs. The claim is about both sets; a pooled share lets the opening set's collapse hide behind the closing set's survival (or the reverse), and the falsifier — the text this design exists to write — names the sets separately. "Reproduces" in the spec is per-set (≥20 of 40 and ≥10 of 20), in both the SUPPORTED criterion and precedence step 1. |
| C04 | The freeze record exhibits the dated append beside the claim record | Any rerun outcome is checked for quoting the falsifier as appended | **Agree** — with the draft's completion that the comparison is character-for-character: the claim carries the design's text in quotation, copied at this draft from the design as read, so the freeze has an exact string to append and to be judged against. |
| C05 | Gate-0.2 record exhibits both sets with per-sign citations | A verdict measured against any other set is not a verdict under the falsifier (→ closure, not SUPPORTED/NOT SUPPORTED) | **Disagreement, resolved.** A initially treated the recorded counts (40/20) plus the ten exhibited terminal entries as enough to draft the gate around, assuming the full sets would be findable at execution in the Phase-43 file. B, reading the file in full, found neither full set in it: the terminal list is 10 of 20, and no initial list exists. **Resolution:** the gate is written as an exhibition act over *a pinned source on the record*, not over the Phase-43 file alone, and its failure is a pre-written closure (ORIGINAL SETS NOT EXHIBITABLE) rather than a drafting assumption. Whether a pinned source exhibiting the full sets exists is exactly what the gate tests; the draft asserts neither that it does nor that it does not (§6, defect 1). |
| C06 | Gate 0.3: reproduce the recorded reference points under the freeze-stated rule | A rerun under any rule that has not reproduced the reference points is a different battery, whatever its code is called | **Disagreement, resolved.** A assumed the Phase-43 file states the battery's thresholds (the triage's phrase "Phase-43 thresholds are on record" reads that way). B found counts and rates only — no threshold, no floor, no classification rule — and found two neighbouring batteries whose constants could be borrowed wrongly (Phase-113 family's; the generic pipeline's). **Resolution:** no threshold value or rule is asserted anywhere in this draft; the freeze states the rule from the record (OPEN-054-1), gate 0.3 proves it by reproduction, and the borrowed-constant routes are recorded as refused in claim C06. If the record cannot ground a rule, that is a freeze failure reported as such — not a drafting licence and not an execution improvisation. |
| C07 | Gate 0.3: identify, export, pin, reproduce on the pinned layer | A run counting on an unpinned or substituted layer is non-compliant on its face | **Agree** — but see DD-054-3: neither derivation could name the corpus as a repository file, because Spec 033 states it as held in the database (the Spec 048 derivation C07 reached the same point for the same phrase). The Yajnadevam file a sibling draft pins for a different test is named in the claim as a refused substitution. |
| C08 | Gate-0.4 record exhibits the layer digest and per-sign mapping table | Conflict or unmapped signs silently dropped shrink the mapped set until the arms agree (→ the disposition table is the check) | **Agree** — with one sub-point carried openly: the draft pins crosswalk v1 (Spec 019's frozen join) as the crosswalk of record, while the design says only "the crosswalk"; the governing-file confirmation is OPEN-054-4, and gate 0.4 fails closed if the stated per-sign mapping cannot be completed through the pinned file. |
| C09 | Gate verdicts precede quantities in the run record, in order | Any quantity preceding its gate falsifies compliance | **Agree.** |
| C10 | Headline derivable from both arms' reappearance counts and the overlap placement alone | Headline must match §6's pre-written wording for its class | **Disagreement, resolved.** The derivations diverged on the one-arm pattern. A read the falsifier's third condition ("the effect disappears when inscription segmentation follows the other compilation's conventions") as firing whenever arm 2 fails to reproduce — making the outcome NOT SUPPORTED. B read the design's criteria paragraph, which names exactly that pattern INCONCLUSIVE ("one arm reproduces and the other does not, with counts stated"), and noted that under A's reading the INCONCLUSIVE word is unreachable whenever the arms disagree — the design cannot have intended a verdict word its own falsifier deletes. **Resolution (DD-054-2):** B governs, with one carve-back both derivations accepted: if arm 2 reproduces *neither* set *and* the pooled overlap is at or below the null's 95th percentile, the falsifier's **second** condition has fired on its own terms (the sets overlap no more than shuffled labels), and the outcome is NOT SUPPORTED. The precedence is written into claim C10 and spec §6, and OPEN-054-7 puts its confirmation to the freeze before any counting. |
| C11 | Gate-0.5 census published before any positional quantity | A share computed past a floor failure, or with thin signs quietly excluded, falsifies compliance | **Disagreement, resolved.** A read the design's floor as a pure inclusion rule for the *rerun's* sets (below-floor signs simply form no part of the new sets, and reappearance is measured among the rest). B objected that this shrinks the *denominator* of reappearance: original signs that are thin in the rerun vanish from the fraction, so thinness itself raises the reappearance share — the falsifier gets easier to pass exactly where the data got weaker. **Resolution (DD-054-5):** the primary denominator is the full exhibited set; a below-floor original sign counts as not reappeared, is named TOO THIN with its count, and is removed from the denominator only in the pre-registered §5.1 sensitivity, reported with the same prominence. The floor's *value* is not in the design at all — OPEN-054-3 (§6, defect 3). |
| C12 | Observed overlap placed against the recorded 999-shuffle null | A null construction chosen after the observed overlap is known is a fitted test (→ construction and seed frozen first) | **Agree** — with the pooled-vs-per-class question resolved in the claim: the design states the overlap on "the two compilations' strong-sign sets" jointly, so the headline statistic is pooled, with per-class placements reported beside it (DD-054-6) so a pooled pass cannot hide a one-class collapse. |
| C13 | Gate-0.4 statement exhibits both conventions; outcome reports per-arm length distributions | A primary count on a re-segmented arm falsifies the run | **Agree.** |
| C14 | File inspection at close: prior content unchanged, appends dated and enumerated | A status restated in place, however convenient, falsifies compliance | **Agree.** |
| C15 | Inspect outputs for language/meaning/independent-corpus claims and for any campaign publication | An outcome presented as showing the script encodes language falsifies compliance | **Agree** — one inspection, both directions. B added the Spec 045 measure-conflation case (quoting 045's suffix result as this spec's closing result) to the claim's boundary, since both specs speak of "closing-sign behaviour" for different measures (§5.2 of the spec). |

## 4. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest
   in `freeze.md` / `freeze.json`), with
   every spec §2 pin re-asserted against the
   merged record — or decline, leaving
   `yadav_2009_arxiv_manual_002` with its
   strongly-supported, falsifier-less record
   exactly as it stands. **The freeze act
   performs the §4 falsifier append** in
   either case in which the freeze proceeds:
   the append is part of the freeze, not of
   any later execution.
2. **OPEN-054-1 (the battery's threshold
   rule).** State the Phase-43 battery's
   strong-sign threshold rule in checkable
   form, from the record, such that gate 0.3
   can prove it by reproducing the recorded
   reference points (201 profiled; 40/20/61;
   the ten exhibited terminal rates). No
   value is proposed at draft (§6, defect
   1). If the record cannot ground a rule,
   the freeze does not happen and the member
   is reported as a drafting/freeze failure
   under the campaign's rule — the rule is
   not invented at execution.
3. **OPEN-054-2 ("strict", operationally).**
   Confirm what the arm-1 restriction is:
   the draft's reading is the Phase-43 V3 /
   Mahadevan-lineage corpus as held,
   identified and pinned at gate 0.3, with
   counting restricted as the design states
   to the strict sign set (the 94
   `strict_sa_independent` readings of the
   anchors file), and the gate-0.3
   reproduction as the operative check. The
   freeze confirms this reading or states
   the restriction it intends, in terms gate
   0.3 can check, before any counting.
   (The Spec 048 OPEN-048-2 precedent for
   the same phrase is noted: there, a
   readings-restriction would have excluded
   that family's reference sign, which
   carried no anchor entry; the freeze here
   should check the exhibited original sets
   against the anchors file with the same
   care — if original signs carry no anchor
   entries, the restriction's meaning for
   them must be stated explicitly.)
4. **OPEN-054-3 (the occurrence floor).**
   Fix the minimum-occurrence floor's value
   — the design requires a floor identical
   in both arms and states none — before
   any counting, and confirm DD-054-5's
   denominator reading or swap the primary
   and sensitivity readings openly.
5. **OPEN-054-4 (the crosswalk of record,
   and the second arm's standing).** Confirm
   that the Phase-122 crosswalk v1 pinned in
   spec §2 governs arm 2's mapping (or name
   the file that does, and pin it), and
   confirm DD-054-4 (a gate-0.4 failure
   closes the whole execution as SECOND ARM
   NOT RUNNABLE, because the overlap and
   inconclusive rules need both arms) or
   rule openly that arm 1 may stand alone
   with the arm-missing case pre-written,
   before any counting.
6. **OPEN-054-5 (the shuffle null's
   construction).** State the label-shuffle
   procedure in checkable form — what is
   shuffled, what is held fixed (set sizes,
   per-class sizes, the mapping table) — and
   fix its seed, before any counting.
7. **OPEN-054-6 (the Spec 045 reconciliation
   touchpoint).** Reconcile this spec's
   closing-sign measure (Phase-43
   terminal-strong set membership) against
   Spec 045 §5.2(a)'s measure
   (distinct-predecessor rate in final
   position), against Spec 045's frozen text
   if one exists by then (DD-045-4 is the
   mirror item on that side): record whether
   the two are stated as one measure under
   two forms or as two distinct measures
   with distinct names, and which governs
   which spec's verdict. **The two specs'
   closing-sign measures must not silently
   diverge, and neither spec's output may
   quote the other's closing result as its
   own.** Whichever form the freeze adopts
   is a freeze decision; this draft adopts
   neither (spec §5.2).
8. **OPEN-054-7 (the precedence rule).**
   Confirm DD-054-2's precedence (claim C10;
   §3 derivation C10) or overturn it openly,
   before any counting. It may not be
   changed after.
9. **OPEN-054-8 (OSF).** Whether the frozen
   spec files its own OSF registration —
   under campaign decision E-1, every
   specification in the pass gets its own
   OSF contract registration at its freeze,
   so the proposal is **yes**, following
   Specs 036–039. Nothing is filed at draft.
10. **OPEN-054-9 (phase number).** Allocate
    the execution phase number at the freeze
    act, from the merged record as it then
    stands (DD-054-7).

## 5. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-054-1 — "Reproduces" is per-set.**
  Each original set must reach its own half
  (≥20 of 40 opening; ≥10 of 20 closing) in
  an arm for that arm to reproduce it (§3
  derivation C03; claim F054-C03).
- **DD-054-2 — The precedence rule.** The
  design's criteria and falsifier are
  applied in the order claim C10 / spec §6
  state; a one-arm shortfall is INCONCLUSIVE
  unless the overlap condition fires on its
  own terms (§3 derivation C10).
- **DD-054-3 — No invented corpus pin.**
  Spec §2 pins what was verified and says
  why the strict corpus and the Holdat layer
  carry no pin at draft; gates 0.3 and 0.4
  do the pinning as fail-closed acts (the
  Spec 048 DD-048-3 precedent).
- **DD-054-4 — The second arm is integral.**
  A gate-0.4 failure closes the execution,
  because §6's overlap and inconclusive
  rules compare the arms; an arm-1-only
  verdict could not state whether either
  fired. OPEN-054-4 puts this to the freeze.
- **DD-054-5 — Thin original signs count as
  not reappeared in the primary.** The
  floor-restricted denominator is the
  sensitivity, not the primary (§3
  derivation C11; claim F054-C11).
- **DD-054-6 — The overlap headline is
  pooled; per-class placements are
  reported.** (§3 derivation C12; claim
  F054-C12.)
- **DD-054-7 — No execution phase number at
  draft.** Allocated at the freeze act.
- **DD-054-8 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today
  (the Spec 042 DD-042-4 / Spec 048
  DD-048-8 precedent).

## 6. Design defects and ambiguities found at drafting

Recorded per the campaign rule that a defect
is reported, never repaired silently:

1. **The Phase-43 record does not carry
   what the design (and the triage) say it
   carries.** The design's method is "re-run
   the Phase-43 positional battery with its
   thresholds unchanged," and the triage
   records "Phase-43 thresholds are on
   record." The Phase-43 file of record
   states **counts and summary rates only**:
   no threshold value, no minimum-occurrence
   floor, no classification rule for
   "strong", a terminal-strong list of 10
   entries against a stated count of 20,
   and no initial-strong list at all. The
   companion positional record has the same
   shape (counts and mean rates, no lists,
   no rule). Two consequences are drafted
   openly rather than papered over:
   (a) gate 0.2 makes exhibition of the
   original sets a fail-closed act with a
   pre-written closure, because the
   falsifier's first condition is
   unmeasurable without them; (b) no
   threshold is asserted anywhere in this
   draft, and OPEN-054-1 makes stating the
   rule from the record a freeze act, with
   gate 0.3's reproduction as its proof.
   The neighbouring constants that could be
   borrowed by mistake (the Phase-113
   battery's frozen thresholds; the generic
   pipeline's `exclusive` rule and ≥3 floor)
   are recorded in §2 as read and refused:
   they belong to different batteries. This
   is the draft's principal finding, and if
   the freeze cannot ground the rule, the
   honest campaign outcome for this member
   is a reported freeze failure, not a
   quieter test.
2. **The design's criteria and its
   falsifier overlap on the one-arm
   pattern.** The criteria name that pattern
   INCONCLUSIVE; the falsifier's third
   condition ("the effect disappears when
   inscription segmentation follows the
   other compilation's conventions") can be
   read to fire on the same pattern, which
   would make NOT SUPPORTED and INCONCLUSIVE
   claim the same outcome. Resolved by the
   DD-054-2 precedence, recorded in full at
   §3 derivation C10, and put to the freeze
   as OPEN-054-7. Not resolved silently:
   either reading was available, and the
   draft shows its working.
3. **The design requires a floor it does
   not value.** "A minimum-occurrence floor
   identical in both arms" is a control in
   the design's own text; no number appears
   anywhere in it. The draft carries the
   requirement and the cross-arm identity
   verbatim, asserts no value, and puts the
   value to the freeze (OPEN-054-3) — the
   Spec 048 OPEN-048-3 pattern for a bar the
   design states and defers in the same
   breath.
4. **A fetch inconsistency in a cited
   record, recorded and routed around.** One
   contents-API fetch of
   `reports/phase122_crosswalk_mayig_results.json`
   returned bytes inconsistent with the
   file's metadata and with repeated raw
   fetches of the same path. The draft
   therefore does **not** pin that file; its
   counts (762 pairs, 383 conflicts) are
   cited through Spec 019's frozen record
   and the crosswalk files themselves,
   which verified stable across repeated
   fetches. No other pin in §2 was affected:
   every §2 pin was recomputed at least
   twice, by two fetch routes, with
   identical results.
5. **Spec 045's measure and this spec's
   measure share a name.** Spec 045 §5.2
   speaks of "closing-sign behaviour" for
   its distinct-predecessor measure; this
   spec's closing signs are the Phase-43
   battery's terminal-strong set. A reader
   moving between the two drafts could take
   them for one measure. Handled by spec
   §5.2 (the difference stated in both
   specs' terms) and OPEN-054-6 (the freeze
   reconciliation, mirroring Spec 045's
   DD-045-4). Not a defect in either design's
   substance: D-05's own text defines its
   measure independently, and D-08's is the
   battery's — the divergence risk is in
   the shared vocabulary, which is exactly
   what the freeze touchpoint exists to
   close.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 7. Freeze-stage adjudication — 2026-10-21: FREEZE FAILURE (OPEN-054-1 — BATTERY NOT PINNABLE; the original sets are not exhibitable from any record)

This section records a freeze attempt and its outcome. It is a
campaign bookkeeping act only: it is not a freeze, and it repairs
nothing.

- **Freeze attempt.** On 2026-10-21 the freeze for Spec 054
  (design D-08, draft PR #260, branch
  `spec-054-yadav-opening-closing-draft`, head `d5a5b127`)
  attempted the freeze question on the record of `main` at
  `e339996194e1dd3c5336d87da37be0d5b0765556`: either
  (a) freeze with the computation specified at the freeze and
  every Phase-43 identity reading honestly retired — available
  only if the design's falsifier (claim F054-C04, verbatim)
  can stand on the specified construction without pretending
  it is the original battery's — or (b) freeze failure.
- **Outcome: FREEZE FAILURE — option (b).** OPEN-054-1 cannot
  be resolved from the record, and the falsifier as written
  requires the original battery's sets, which do not exist as
  enumerable records. No threshold was invented, no set was
  reconstructed, and no constant was borrowed from a
  neighbouring battery (the draft expressly refused those
  routes, and this freeze honours that refusal). Under the
  draft's own terms (claim F054-C06's boundary; adjudication
  §6, defect 1), the spec therefore cannot freeze.
- **Phase allocation: Phase-417 was NOT allocated.**
  Allocation is a freeze act and no freeze occurred.
- **Actions NOT taken (by design, on failure):** no AEE
  hooks, no digest, no claims-register change, no OSF filing,
  no execution phase, no merge. PR #260 remains open and
  draft; the only change on its branch is this bookkeeping
  section, appended to this file.

### 7.1 Why option (a) is not available here (and was for Spec 053)

Spec 053 froze by option (a) (its DD-053-11) because its
falsifier never depended on a Phase-43 fit: it fires if a
named non-linguistic control fits as well as or better than
the Indus strict corpus under that spec's own estimator, so
specifying the estimator at the freeze and retiring the
"identical to Phase-43" reading changed nothing the
falsifier is about. Spec 054 is the opposite case, in its
own draft text:

1. **The falsifier's object is the original sets.**
   F054-C04, verbatim: the claim fails if "fewer than half
   of the original 40/20 sign sets reappear on the strict
   corpus". Reappearance is membership in the original
   opening-strong set (40 signs) and closing-strong set
   (20 signs). Those sets are the falsifier's measurable
   object (claims F054-C03, F054-C05; spec §3 gate 0.2,
   §5 "Reappearance").
2. **The battery identity is a claim, not a framing.**
   F054-C06: "The rerun's battery is the Phase-43 positional
   battery with its thresholds unchanged: the threshold rule
   is stated in checkable form in the freeze record, from
   the record". A freeze-specified new rule would not be a
   restatement of this claim; it would replace it.
3. **A specified construction cannot supply the sets
   honestly.** Any new threshold rule applied to a corpus
   would produce a new set, not the original one. Choosing
   a rule because it yields counts of 40 and 20 would be
   tuning to the recorded counts; the exhibited evidence
   does not fix a rule (see §7.2), and on the initial side
   it does not even bound one. Calling the constructed set
   "the original 40/20" would be exactly the pretence
   option (a) forbids, and reappearance measured against a
   set the rerun's own construction produced would be
   self-referential. Retiring the identity reading here
   does not leave a falsifier standing; it removes the
   falsifier's subject. That is a design amendment, not a
   freeze act, and it is outside this pass.

### 7.2 The search record

Searched on `main` at `e3399961…` (tree and contents
re-verified in the foreground by two routes — contents raw
and git blob — agreeing byte-for-byte on every draft file
and every §2 pin, including `outputs/phase43_all.json`
SHA-256 `78a6c219…` and the claim record SHA-256
`90476623…`):

- **Tree level.** The full recursive tree of `main`
  (5,908 entries, not truncated): exactly ONE path contains
  `phase43` — `outputs/phase43_all.json`. No Phase-43
  script, report, or experiment-graph module exists.
  The file's only commit in its path history is the
  2026-05-21 repository-restructure move.
- **The Phase-43 file, read in full.**
  §T2_2 carries the counts (initial-strong 40,
  terminal-strong 20, terminal-moderate 10, medial-strong
  61, total signs profiled 201) and a `terminal_strong`
  list of **10 entries only** (signs 342, 176, 328, 211,
  1, 15, 254, 12, 60, 190; terminal rates 0.683–0.892;
  totals 22–1,318). There is **no initial-strong list at
  all**, no medial list, no threshold, no floor, no
  minimum count, and no classification rule anywhere in
  the file; the word "threshold" occurs once, with no
  number (the §T2_4 fish note). §T2_1's rebus table labels
  positional roles for the 20 most frequent signs only
  (4 terminal-strong, 2 initial-strong — a subset of the
  exhibited ten on the terminal side, and 2 of 40 on the
  initial side, with no rates): partial labels, not a set.
- **The companion positional record**
  (`glossa-indus/analysis/positional/hunt_tripartite_test.json`,
  SHA-256 `0e546962…`): the same 40/20/61 counts and mean
  rates (0.757 / 0.805; chance 0.251). No lists, no rule.
- **Content level.** GitHub code search for
  `TERMINAL_STRONG`, `terminal_strong`, `INITIAL_STRONG`,
  `initial_strong`, `initial_strong_signs`,
  `terminal_strong_signs`, `total_signs_profiled`, and
  `medial_strong` (20 / 20 / 21 / 21 / 4 / 4 / 1 / 11
  hits). Every hit was examined. None exhibits the
  Phase-43 sets or states its rule:
  - `glossa-indus/reports/model_reports/batch5_analysis_report.json`
    — a same-corpus companion analysis (3,137 sequences,
    201 signs profiled): shuffle nulls and a contact-zone
    table carrying role labels for a handful of
    site-exclusive signs. No strong-sign lists.
  - `backend/scripts/phase45_t3_hunt_tripartite.py` and
    `outputs/phase45_t3_hunt_tripartite.json` — the
    Phase-45 battery on Holdat roles: its own rule
    (average position, count ≥ 8) and its own lists
    (75 initial-strong, 5 terminal-strong, M-numbered).
    A different battery; borrowing it is refused.
  - `scripts/structural_analysis.py` and
    `reports/latent_sign_class_report.md` — a different
    corpus (Mohenjo-daro only, P/Y sign space): 61
    terminal-strong and 45 initial-strong under a
    ≥ 0.55 rate / ≥ 4 frequency rule. Not Phase-43's
    counts, corpus, or sign space.
  - `outputs/phase33_positional_profiles.json` — 61 signs,
    classes INITIAL/MEDIAL/MIXED/TERMINAL, no STRONG
    classes, a different corpus.
  - `backend/scripts/phase54_falsification.py` and the
    Phase-219 arxiv update (`backend/scripts/phase219_arxiv_updated.py`,
    `outputs/phase219_arxiv_updated.txt`) — later phases
    that cite single signs as INITIAL_STRONG (e.g. M047,
    initial rate 0.806, frequency 356); no lists, no
    Phase-43 rule.
  - The claim records, the Hunt model YAML, the
    contact-zone file, and the LEDGER — all repeat the
    same counts and evidence strings and nothing more.
- **Rule-by-rule outcome (OPEN-054-1).** Threshold: not
  stated; the ten exhibited terminal rates bound any
  terminal threshold at ≤ 0.683 and nothing bounds an
  initial threshold (no initial rates are exhibited
  anywhere); the STRONG/MODERATE boundary cannot be
  located from either side, since no TERMINAL_MODERATE
  sign's rate is given. Floor: not stated; exhibited
  totals bound it at ≤ 22 only. Position rules: not
  stated for Phase-43 (the rates partition a sign's
  occurrences, but the rule producing the partition —
  including length-1/2 handling — appears in no Phase-43
  record). This is the same finding Spec 052's freeze
  recorded for the same battery (PR #249, adjudication
  §8: BATTERY NOT PINNABLE), reached again here from
  Spec 054's side with an independent search.
- **Set-by-set outcome (gate 0.2's object, at freeze).**
  Closing set: 10 of 20 exhibited (Phase-43 §T2_2).
  Opening set: 0 of 40 exhibited as a list; 2 members
  labelled in a frequency table. Neither full set is
  exhibitable from any pinned source on `main`.

### 7.3 The two freeze acts the draft mandated — disposition

- **OPEN-054-6 (the Spec 045 reconciliation).** Recorded
  here, as the mirror of Spec 045's frozen DD-045-19:
  Spec 054's closing-sign measure — **Phase-43
  terminal-strong set membership**, a set-membership state
  under the Phase-43 battery — and Spec 045's measure —
  the **closing distinct-predecessor rate** in final
  position — are **DIFFERENT measures, distinctly
  named**; neither spec adopts the other's form, and
  neither spec's output may quote the other's closing
  result as its own. Spec 045's freeze (DD-045-19)
  already records exactly this from its side; because
  Spec 054 does not freeze, no mirror freeze act is
  entered on this spec's side — the distinction stands
  on Spec 045's frozen record and on this draft's §5.2,
  and any future amendment or refreeze of this design
  must carry it.
- **The §4 falsifier append — NOT performed.** The append
  is a freeze act (spec §4; claim F054-C04's boundary:
  "if the freeze does not happen, no append happens
  under this spec"), and there is no freeze. The claim
  `yadav_2009_arxiv_manual_002` stands exactly as
  recorded. The durability question the freeze would
  have had to answer is nevertheless settled on the
  record, because it bears on any future attempt:
  - The record lives at
    `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`
    (SHA-256 `90476623…`, verified at this freeze
    attempt). Field enumeration at this attempt confirms
    manual_002 carries **no** `falsification_condition`
    field; its companion manual_001 in the same file
    carries one.
  - The store is regenerated by
    `glossa-indus/scripts/indus_claims.py`. Its
    hand-written manual_002 entry likewise carries no
    `falsification_condition`, and its Spec 029
    carry-over preserves, by claim identity, only:
    `stage`, `stage_source`, `stage_as_of`,
    `stage_history`, `verified_unexplained`,
    `proposition_fingerprint`, `merged_into`,
    `evidence_instances`, `not_understood`,
    `explanation_record` — plus, for records carrying a
    `status_correction`, `claim_status`,
    `contradicting_evidence`, and `status_correction`.
    **`falsification_condition` is not in the preserved
    set.** A falsifier appended to the extracted-claims
    store alone would therefore be silently dropped by
    the next regeneration. A durable append would have
    required amending the generator's manual entry (and
    regenerating), or another preserved-field home —
    a change to the claim-store machinery that a freeze
    of this spec does not by itself authorise, and that
    no freeze here performs.

### 7.4 The remaining OPEN items — disposition

OPEN-054-1 is antecedent and it fails, so the rest were
not decided: confirming them would be freeze acts, and
there is no freeze. OPEN-054-2 ("strict", operationally),
OPEN-054-3 (the floor's value and the denominator
reading), OPEN-054-4 (the crosswalk of record and
DD-054-4), OPEN-054-5 (the shuffle construction and
seed), and OPEN-054-7 (the DD-054-2 precedence
confirmation) remain as the draft states them, neither
confirmed nor overturned. OPEN-054-8 (OSF under E-1):
not filed — E-1 files at the freeze, and there is no
freeze. OPEN-054-9: no phase allocated (see above).

### 7.5 What record would unblock it

Any ONE of the following, as a record of record on
`main` (or an owner amendment that supersedes the
derivation requirement openly):

1. The original Phase-43 battery script (or a
   contemporaneous Phase-43 methods record) stating
   numerically the position rules, the count floor, and
   the STRONG/MODERATE thresholds, **and exhibiting the
   full original sets** (40 opening, 20 closing) — enough
   for gate 0.3 to reproduce the recorded reference
   points (201 profiled; 40/20/61; the ten exhibited
   terminal rates) and gate 0.2 to exhibit both sets.
2. Failing that, an amendment re-scoping Spec 054 to a
   NEW, explicitly defined battery with its own stated
   rules and a falsifier written against that battery's
   own sets, honestly labelled as a new test rather
   than as the Phase-43 rerun the design specifies —
   a design change, not a freeze act, and outside this
   pass.
3. For the falsifier append in any variant: a durable
   home for `falsification_condition` in the
   extracted-claims store — in practice, the generator
   amendment named in §7.3 — decided as its own act.

## 8. Bottom line for the wave report

FREEZE FAILURE — Spec 054 (PR #260, still draft).
OPEN-054-1 fails closed as BATTERY NOT PINNABLE, and
independently the falsifier's first condition has no
measurable object: of the original 40/20 sign sets the
design's falsifier (F054-C04) is written against, the
record exhibits 10 of 20 closing signs and no opening
list at all, and no threshold rule, floor, or position
rule for the Phase-43 battery is stated in any record
on `main`. Option (a) — specifying a new construction
at the freeze — was ruled out on the draft's own text:
claims F054-C04/C06 make the original sets and the
unchanged Phase-43 battery the falsifier's subject, so
a constructed successor cannot stand in for them
without the pretence option (a) forbids (contrast
Spec 053, whose falsifier never depended on Phase-43).
The falsifier append was not performed (it is a freeze
act; there is no freeze), and a direct append would in
any case not have survived regeneration of the
extracted-claims store. The defect queues as an
amendment per the campaign rule; nothing was rescued
in-pass.

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 8. Settled rulings — owner approval 2026-10-23 (Item 3)

§7 closed the 2026-10-21 freeze attempt: the battery
could not be pinned (OPEN-054-1), the original sets could
not be exhibited (OPEN-054-2), and no freeze could append
a falsifier the claim's record never carried, because the
append had no durable home (the §7.3 generator finding).
§7.5 reserved both design questions to the owner. The
owner decided both on 2026-10-23, approving Item 3 of
the waiting-decisions package as written. The rulings
are recorded here; the amendment they commission is
`amendment.md` in this directory, and it returns to the
owner as a mini-gate. This spec is not frozen by
anything in this section.

### 8.1 The falsifier design — §7.5(2) adopted

**Ruled:** the falsifier design of §7.5(2) is adopted.
The amended spec does not re-earn the original
Phase-43 sets (nothing can: OPEN-054-2's finding
stands — the sets cannot be exhibited, and no amended
text in this directory pretends otherwise). Instead the
amendment evaluates an amended statement under a new,
explicitly defined battery — **NB-1**, the same battery
Spec 052's amendment defines — which produces its own
opening-strong and closing-strong sets in both arms.
The design's three conditions are carried over and
re-aimed at the new battery's sets:

- reappearance **< ½**, read per class
  (DD-054-1's per-set reading);
- pooled overlap against the **999-shuffle null's 95th
  percentile** — the null's construction, left open at
  OPEN-054-5, is specified in the amendment (label
  permutation of arm 2's strong-set membership, set
  sizes and mapping held fixed, seed 44054);
- under **DD-054-2's precedence** and **DD-054-5's
  denominator discipline**, both carried into the
  amendment's decision procedure.

The verdict wordings are **rewritten**: the draft's
SUPPORTED (RE-EARNED) is struck — nothing is re-earned,
because the original sets remain unexhibitable — and
the amended SUPPORTED states what the new battery's own
sets establish, with its limits in the wording
(amendment §9). The new falsifier's exact text is fixed
in the amendment (§8) and is **appended at the amended
freeze**, not now: the append is a freeze act, and this
draft performs no freeze act.

Consequences for the draft's open items: OPEN-054-1 is
discharged by NB-1's definition (the battery no longer
needs pinning out of the Phase-43 record — the same
owner ruling as Spec 052's §9.1: nothing invented or
borrowed under the Phase-43 name). OPEN-054-2 is
discharged as a gate: the gate-0.2 ORIGINAL SETS NOT
EXHIBITABLE check retires, because the amended run
produces its own sets; the underlying fact stays in
this record and in the SUPPORTED wording's stated
limit. The draft's BATTERY NOT REPRODUCED closure
retires with it — NB-1 has no external original to
reproduce; the amendment substitutes a determinism
gate. OPEN-054-5 is answered by the amendment's null
construction.

### 8.2 The generator act — §7.5(3) decided, fix prepared

**Ruled:** the §7.5(3) act is decided together with the
design: the claim-store generator is amended so that an
appended `falsification_condition` survives
regeneration, giving the amended freeze's append a
durable home.

The fix is **prepared in this amendment's PR**, as a
separate commit touching only
`glossa-indus/scripts/indus_claims.py`: the
regeneration carry-over — the mechanism that already
preserves the stage fields, the merge state, and the
lane-2 authored fields by claim identity — gains
`falsification_condition`, with a dated comment in the
block's own style. It lands with this draft PR because
the act is machinery, decided on its own footing,
independent of the freeze it serves; it changes no
claim's content (no falsifier is appended by it — the
append remains the amended freeze's act).

Both halves of the proof were run on 2026-10-23 in a
scratch copy of the generator's tree, and are recorded
in full in `amendment.md` §7:

- **Failure mode (unmodified generator):** a marker
  `falsification_condition` appended to
  `yadav_2009_arxiv_manual_002`'s store record is
  absent from the record after regeneration — only
  `manual_001`'s generator-authored condition remains.
  §7.3's finding, reproduced on demand.
- **Fixed generator:** the same append survives
  regeneration verbatim; the only differences from the
  un-appended store are the appended field itself and
  the regeneration timestamps (the baseline noise,
  measured first on the unmodified tree).

### 8.3 What the amendment changes, and what it does not

- The **parent claim record is untouched**: no edit,
  no append, no status movement. The claim stands
  strongly supported with no falsification condition,
  exactly as §7.1 records, until the amended freeze
  performs the append.
- **§7.3's Spec 045 reconciliation carries unchanged:**
  Spec 045's "Holdat final-position concentration"
  (joint-sign rate > 0.5, object-frequency basis) and
  this spec's closing measure are different quantities,
  distinctly named in every outcome record
  (amendment §10).
- DD-054-1, DD-054-2, DD-054-5 and DD-054-6 carry into
  the amendment; DD-054-6's pooled-overlap headline is
  the overlap the amendment's §5 tests.
- The unamended draft's step-0 closures stand in the
  record as the 2026-10-21 attempt left them; the
  amendment's §6 states which survive, which retire,
  and what replaces them.

### 8.4 What returns to the owner

The amendment draft — this section, `amendment.md`,
claims F054-C16…C19, the amendment tasks, and the
generator-fix commit — is the mini-gate. The owner
approves it, amends it, or declines it. Only on
approval does the freeze path resume: AEE lifecycle
hooks over the recovered register (L4), the freeze act
— which appends the §8 falsifier text to the claim's
record and registers the claim-record hash **after**
the append — the OSF filing, and then a separate
execution order. Nothing in this section freezes,
files, appends, or executes anything.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 9. Mini-gate approval and the amended freeze — 2026-10-23

§8 recorded the settled rulings and returned the
amendment to the owner as a mini-gate. This section
records the owner's decision and the freeze act it
authorised. It is the freeze record's adjudication
half; `freeze.md` is its other half.

### 9.1 The mini-gate approval

On 2026-10-23 at 22:59 EDT the owner approved both
mini-gates as specified ("Approve both mini-gates as
specified") — for this spec, the four decisions of
`amendment.md` §11: (1) the amended statement (§2) and
battery NB-1 as specified (§3), floor 20 and bands
2/3 and 1/2 included; (2) the decision procedure (§5)
— per-class reappearance at ≥ 1/2 with DD-054-5
denominators, the pooled-overlap null as constructed
(label permutation, 999 shuffles, seed 44054,
nearest-rank 95th percentile), and DD-054-2's
precedence as ordered in §5.5; (3) the verdict
wordings (§9) and the falsifier text (§8) as the
exact words the amended freeze appends; (4) the
generator fix (§7) landing with the PR. `amendment.md`
and `spec.md` stand byte-untouched by this act, as
approved. Tasks A4 is complete.

### 9.2 L5 decided as amended

- **OPEN-054-1 — discharged.** NB-1's definition in
  the amendment replaces the unstatable Phase-43 rule
  (§8.1); nothing is pinned out of the Phase-43
  record and nothing is borrowed under its name.
- **OPEN-054-2 — discharged as a gate.** The amended
  run produces its own sets, so the gate-0.2
  exhibition check retires; the unexhibitability fact
  stands in §7.2 and in the amended SUPPORTED
  wording's stated limit. Arm 1's identify-and-pin
  act survives at step 0 as the STRICT CORPUS NOT
  PINNABLE closure (amendment §6).
- **OPEN-054-3 — decided.** The floor is fixed by
  NB-1.4 at N(s) ≥ 20, identical in both arms, and
  DD-054-5's denominator reading is confirmed as the
  primary (amendment §5.4): unmapped, conflict-paired,
  and below-floor-in-arm-2 signs count as not
  reappeared, named with their reasons; the
  sensitivity that removes named signs is reported
  with the same prominence and never governs.
- **OPEN-054-4 — confirmed.** The Phase-122 crosswalk
  v1 pinned in spec §2 is the crosswalk of record —
  re-asserted at this freeze against the files: JSON
  SHA-256 `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb`,
  CSV SHA-256 `3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823`;
  766 rows of which 762 are mapped pairs (4 unmapped)
  and 383 are conflict pairs. DD-054-4 is confirmed:
  a second-arm failure closes the execution as SECOND
  ARM NOT RUNNABLE (amendment §6); arm 1 does not
  stand alone.
- **OPEN-054-5 — answered.** The null is the
  amendment §5.3 construction: arm 2's strong-set
  membership labels permuted over its classifiable
  signs, marginals and mapping fixed; 999 shuffles;
  seed 44054; chance level the nearest-rank 95th
  percentile.
- **OPEN-054-6 — reconciled, as recorded.** The
  §7.3 reconciliation carries (amendment §10): Spec
  045's "Holdat final-position concentration"
  (joint-sign rate > 0.5, object-frequency basis) and
  this spec's closing measure — "closing-strong under
  NB-1", a per-sign terminal-rate band on an
  inscription-position basis — are different
  quantities, distinctly named in every outcome
  record of either spec.
- **OPEN-054-7 — confirmed.** DD-054-2's precedence
  stands in the amendment §5.5 form: empty arm-1 set
  first; then, both classes reappearing, the pooled
  overlap decides; then the residue (NOT SUPPORTED if
  the overlap is at or below the chance level,
  INCONCLUSIVE above it, with the rates stated).
- **OPEN-054-8 — yes.** This spec files its own OSF
  contract registration at this freeze, under
  campaign decision E-1 (record:
  `osf-spec-registration.md`, completed by append
  after filing).
- **OPEN-054-9 — Phase-437 allocated** (DD-054-10).
  Verified at this freeze act: the merged record's
  highest allocated execution phase is Phase-436
  (Spec 073; Spec 041 holds Phase-435), and Spec
  052's draft branch (PR #249) carries no freeze and
  no phase allocation. Phase-437 is therefore the
  next free number and is allocated to Spec 054's
  execution.
- **DD-054-1, DD-054-2, DD-054-5, DD-054-6** are
  carried into the amended design as the amendment
  states them; **DD-054-3 and DD-054-4** are
  confirmed as amended above; **DD-054-7** is
  discharged by the allocation; **DD-054-8** stands
  (the register's evidence carried `observed_at`
  from the draft, and carries `independent_of` from
  the freeze recovery).

### 9.3 Two freeze decisions recorded here

- **DD-054-9 — The AEE gate reading.** The
  DD-038-10 reading is adopted for this spec, as
  Specs 037, 041, and 053 adopted it before: the L4
  gate passes when every hook carries zero
  correctness failure modes (no irreducibility,
  negation-conflict, counterexample, or precision
  challenge) and no claim below the 0.70 threshold;
  FR-2.3 draft-cap records (one per claim) may
  remain, and the engine's "iterate" word from
  draft-cap alone is not a failure. Applied at this
  freeze: the hooks PASS (19 draft-cap records at
  every hook; minimum propagated 0.72;
  `aee/freeze-aee-note.md`).
- **DD-054-10 — Phase allocation.** The execution
  of Spec 054 under this frozen contract runs as
  **Phase-437** (OPEN-054-9, decided at §9.2).

### 9.4 The falsifier append — performed and proven

The freeze act of `amendment.md` §8, performed
2026-10-23 on the claim store of record:

- **Pre-append pin.** `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`
  recomputed to SHA-256
  `904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3`
  — the §7.1 pin, unchanged.
- **The append.** `yadav_2009_arxiv_manual_002`
  gained `falsification_condition` carrying the
  amendment §8 text **verbatim**, and the dated
  note field `spec054_falsifier_append_2026_10_23`
  (date 2026-10-23; kind
  `spec054-freeze-falsifier-append`) stating that
  the design's original falsifier was never
  appended because the 2026-10-21 freeze failed
  before any append (§7.2), and that this condition
  belongs to the amended statement (amendment §2).
  No other field of the claim changed; its recorded
  status (`strongly_supported`) and stage
  (`explained`) are untouched.
- **The proof (the amendment §7 standard).** Run
  first in a scratch copy of the generator's tree,
  then on the record itself: a baseline
  regeneration of the untouched store changes
  nothing but timestamps (the file's
  `extraction_date` and the two manual claims'
  `extracted_at`); with the append in place,
  regeneration through the fixed generator's
  `process_document("yadav_2009_arxiv")` was run
  and read back — the appended condition survives
  **verbatim**, `manual_001`'s authored condition
  ("If frequency distribution deviates from
  Zipf-Mandelbrot law.") is intact, and the final
  diff against the pre-append store (timestamps
  apart) is exactly the two added fields on
  `manual_002`.
- **The note's durability, stated openly.** The
  dated note field is **not** in the generator's
  carry-over list (the §8 condition is, by the
  §7.5(3) fix): a future regeneration keeps the
  condition and drops the note. The note was
  therefore re-entered on the regenerated record
  as part of this act, and the post-append hash
  below is the hash of the record carrying both.
  Extending the carry-over to note fields was not
  decided by any ruling and is not done here.
- **Post-append pin.** The claim record as
  committed by this freeze: SHA-256
  `dcbaf64a728bc4ff7a0a1f76f2c867f924734cbe7f9c8cab2554d131b22533d7`.
  This is the hash `freeze.md` and the freeze
  definition register (amendment §8's step,
  unchanged from §7.5(4)).

### 9.5 The execution gate

Not satisfied. This freeze orders no execution:
the amended run (Phase-437) starts only on a
separate owner execution order. At the freeze
itself no positional quantity was computed, no
arm was counted, and no verdict was reached on
the amended statement.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

### 9.6 Merge-resolution addendum — 2026-10-23 (same act, before merge)

Recorded openly, because it changes two values the
freeze registered. When PR #260 was marked ready,
GitHub reported it CONFLICTING with `main`, on one
file: the claim store. The draft branch's copy was
the §7.1-pinned record (SHA-256 `90476623…`), but on
`main` the store had moved after the draft's
verification: a regeneration of 2026-10-21
(`extraction_date` 2026-10-21T15:29:26Z) and, on
**both** manual claims, an `audit_note_2026_10_22`
field (the Spec 025 material audit's dated notes).
`main`'s store recomputes to SHA-256
`ec31778a75cbc56f27f385ed7da800edb874a8f600cbe102f46087a8159d6239`
(15,104 bytes), and its `manual_002` still carries
no `falsification_condition` — the append's object
is unchanged, and no other file in the PR
conflicts (the generator on `main` is byte-identical
to the branch's base; the fix applies cleanly).

**Resolution.** The append was re-based onto
`main`'s current store: the §8 condition and the
dated note were entered on that record identically,
**without** regenerating the committed file —
regeneration under the fixed generator preserves
the condition but drops dated note fields it does
not carry, and dropping the Spec 025 audit notes
(another act's dated record) is not this freeze's
to do. The §7 proof was re-run against the new base
in a scratch tree: the appended condition survives
regeneration **verbatim** on this base too, and
`manual_001`'s authored condition is intact. The
resolved store — `main`'s record plus exactly the
two appended fields — recomputes to SHA-256
`938174b0dee14169a5340c9299c73f4eb5b997377f8198a146ef611e73924050`
(17,276 bytes). **That hash supersedes
`dcbaf64a…`** (the append as first performed on the
branch's pinned copy, §9.4, which stands as the
record of the freeze act as performed) as the
post-append pin the freeze registers, in
`freeze.md` §2, in the freeze definition, and in
the freeze tests. Because `freeze.md`, this file,
`build_freeze.py`, and the test file are
digest-covered sources, the freeze digest
`60d2405770e3f87b…` — computed over the
pre-resolution texts — is superseded by the digest
recomputed over the corrected texts in this same
act, which stands in `freeze.json` and replays
clean under `verify_freeze`. Nothing else in §9
changes: the append's text, its proof standard,
and the claim's untouched status and stage are as
recorded.

### 9.7 CI interaction addendum — 2026-10-23 (same act, before merge)

The freeze PR's first full CI run (run 40061894770
on the merged tree) failed exactly one test of
1,139: Spec 029's Phase-104 blast-radius test
(`test_spec029_phase104_correction.py`). Two
interactions, both recorded here because this PR
carries both reconciliations:

- **The append's own score movement (expected,
  now pinned).** That test scores the whole
  extracted-claims store live and pins every
  claim's exact AEE score against its
  post-correction fixture. The §8 append gave
  `yadav_2009_arxiv_manual_002` its first
  falsification condition, so its falsifiability
  component moved 0.0 → 1.0 (direct/propagated
  0.70 → 0.85, band medium → high) — the append
  doing exactly what it was for. Following the
  test file's own supersession precedent (its
  2026-10-20 aee-1.5.0 fixture regeneration),
  the post-correction fixture was regenerated
  from the live store under aee 1.5.0: exactly
  one entry differs, manual_002's, in exactly
  those four values. The movement test now names
  the append as a second, separately caused
  governed movement beside the Phase-104
  correction's three, and pins it exactly; any
  further unexplained movement still fails it.
  The post-merge (pre-correction) fixture is
  unchanged.
- **A pre-existing key-set skew, exposed by the
  merge (not caused by this freeze).** The same
  file's corrected-records test pins the three
  Phase-104 records' exact key sets. On `main`,
  two of the three (critique_0001 / critique_0002)
  also carry `audit_note_2026_10_22` — the dated
  Roif-credit note appended 2026-10-22 — which
  the key pin predates; the merged tree is the
  first state in which pin and records stood
  together under a full CI run. The pin now
  admits the note field for those two records,
  with its provenance commented in the test, in
  the same form as the file's existing
  `evidence_instances` admission. No claim record
  was changed by this reconciliation.

Because this file is a digest-covered source,
the freeze digest is recomputed over the
corrected texts in this same act and stands in
`freeze.json` (the §9.6 digest is superseded in
the same manner §9.6 recorded). The freeze's
substance — the append, its proof, the pins,
the hooks, the decisions — is unchanged.
