# Spec 078 — The Bridge Redesign: A Two-Axis Vocabulary for the Projected-Constraint Corpus Model (Method M13)

**Status: FROZEN at the freeze act of 2026-10-26** (see
`freeze.md` in this directory). This spec carries the
M13 design (method M13 of the advance-to-decipherment
plan; design draft of 2026-10-26, SHA-256 8bb02c07…)
into the programme's frozen-contract form. The design
text is carried as written except where this spec's
§0 records a freeze-fixed completion — a place the
design expressly left open for the freeze to close
(the counted population stated mechanically, the
blindness protocol stated in full, the pattern clause
operationalised, the pilot execution order). Every
such completion is stated in §0 and ruled in the
adjudication; none moves a bar, a threshold, a frame,
or a closure word of the design.

**Parentage.** This spec is the successor to **M12**,
frozen as **Spec 076** and closed by its pilot on
2026-10-26: **ASSUMPTION SET DOES NOT HOLD** (pilot
record: `2026-10-26-m12-pilot-record.md`, programme
goal record). It is a new spec, not an amendment: no
bar, frame, null, closure word, or filed record of
M12/076 is edited, re-run, or softened by anything
here. Where this spec inherits from M12, it says so
and cites the section; where it replaces M12
machinery, it names the replaced part.

**Governing rule (advance plan, iteration addendum,
2026-10-25), which this spec obeys:** no method whose
verdict rests on a score may proceed past drafting
until an instrument exists at its claimed scale and
has passed a wrong-decipherment null of its own at
that scale. This method's verdicts rest on
*deduction*, not scores — but the successor pilot
(§7) builds its control in anyway, in the form this
machinery can actually fail, and the one statistical
instrument it uses (functional coherence, §7.3) is a
pilot calibration device only: it files nothing, and
no register entry may ever cite it.

## 0. Freeze-fixed completions (ruled at adjudication DD-078-3)

- **FF-078-1 — Numbering.** This design is **Spec
  078, Phase 444**. Directory:
  `specs/078-projected-constraint-bridge-redesign`.
  Experiment id:
  `spec078-projected-constraint-bridge-redesign`.
  Claim family F078. (M7 is Spec 077, Phase 443; the
  numbering was verified against the adjacent
  freezes before this freeze was drafted.)
- **FF-078-2 — Counted population, mechanically.**
  The successor pilot's counted population is
  defined, not merely numbered: the
  **frame-attested strict signs** (the strict signs
  of the anchors file that are attested in the pilot
  frame, per the step-0 re-verified census) **minus
  the three worked examples** (M002, M342, M347,
  §5). Frame-absent strict signs are coded and
  reported on the NC-8 line (§5); worked examples
  are coded like all others and reported on their
  own worked-example line (§5). If the census
  re-verifies as in Spec 076 — 94 strict signs, 5
  frame-absent (039, 044, 046, 362, 374), 89
  frame-attested — the counted population is **86**.
  The definition is what is frozen; the number 86
  follows from it at the pilot's step 0, and a
  step-0 mismatch closes the pilot before any count
  is taken (§7.1).
- **FF-078-3 — Blindness protocol.** The step-3′
  coder receives only two things: the anchors
  file's `reading` + `basis` texts for the 94
  strict signs, and the NC-1…NC-8 rules of §5. The
  coder is blind to every census row, to the Spec
  076 pilot's per-sign rows, and to the design
  draft's §6 codings. The coding is produced before
  and independently of any comparison against the
  census, and the coder's file — every assertion
  seen, every ambiguity recorded verbatim — is
  preserved with the pilot record, as in 076.
- **FF-078-4 — Pattern clause operationalisation**
  (this completion does not change the bar). A
  **coding family** is (a) an (axis, NC rule) pair
  — for example (distributional, NC-1) or
  (functional, NC-2) — and, separately, (b) a
  **basis-provenance family**: the kind of basis
  text a coding came from, for example a
  grammar-slot inference, a distributional-study
  summary, or a glossarial note. A **pattern
  finding** is an adjudicated judgement, with its
  grounds recorded in the pilot record. It is
  triggered for consideration when **two or more
  failures share one family** under either
  definition. The bar's counts stand regardless of
  any pattern finding: the pattern clause can only
  close the pilot as BRIDGE DOES NOT HOLD (§7.4);
  it can never rescue a count that fails the bar.
- **FF-078-5 — Pilot execution order.** The pilot
  (§7) executes once, after this freeze is merged
  on genuine CI including the required C4 check, in
  this order: **step 0** re-verification of the
  inherited census → **step 3′** blind coding
  checks (the distributional line against the
  census rows; the functional line's anchor shares
  against the slot base rates computed from the
  re-verified census; the summary line reported,
  generating no failures) → **verdict** under the
  §7.4 bands. It runs **once, as frozen**. **Step 2
  (the shuffle null) is not re-run**: it is
  inherited as standing from Spec 076 under §7.2,
  and that standing is void automatically if step
  0 fails. No parameter of §7 may be altered after
  the freeze for any reason; a premise failure is
  a halt-and-report, recorded with the design's
  own closure words.

## 1. Purpose — the redesign target is the bridge, not the census

Spec 076's pilot split cleanly in two, and this spec
is built on the split:

- **What passed, and is inherited as foundation:**
  the census derivation is sound and reproducible
  (steps 0–1, exact against the pins), and the
  frame's constraint structure exceeds what its own
  marginals produce by chance (step 2: both
  pre-committed bars beaten by margins no shuffle
  in 999 approached — U2 finals residual 178
  against a null 5th percentile of 395.0; solo-only
  count 13 against a null 95th percentile of 5.0).
  The projected-constraint model's deductive core —
  *the attested corpus does force facts about any
  completion* — is a filed finding of the 076 pilot
  record, and this spec does not re-derive,
  re-test, or re-claim it.
- **What failed, and is the redesign target:** the
  **bridge** — the machinery that carries a human
  basis statement ("this sign is a case suffix";
  "this sign is initial") into a machine-checkable
  type-claim the census can judge. The pilot's
  step 3 coded the 94 strict signs' bases under
  rules CR-1…CR-7 into M12 §3.4's nine positional
  types, and the machinery excluded **36 of 89**
  frame-attested claimed types against a bar of 5.
  The pilot record's texture localises the failure
  precisely: 22 of the 36 were distributional
  *summaries* coded as exclusivity claims; all 8
  ONLY-FIN exclusions were *functional* terms
  ("terminal marker", "case suffix") coded as
  positional exclusivity; the ONLY-MED exclusions
  were summaries and a grammar-slot inference coded
  the same way. The presumption recorded at the
  closure — machinery first, strict core second —
  is this spec's starting point, inherited, not
  re-argued.

So: **the census stands; the vocabulary, the coding
rules, and A-FACE are redesigned.** Everything in
M12 that the pilot did not touch — the frame
discipline (M12 §5), the tier architecture (§3.3),
the honesty doctrine of §7.5 (attested occurrences
exclude; absences merely fail to exclude), the
feasibility boundary (§9), the relationship fences
(§10) — is inherited unchanged and cited, not
restated. This spec is deliberately narrow: it
rebuilds the one span that broke, at the same
standard the span that held was built to.

## 2. What exactly died in 076, named part by part

A successor that says "the machinery failed" without
naming the parts invites a redesign that fixes the
wrong thing. The parts:

1. **The one-axis vocabulary (M12 §3.4).** Nine
   types, all of them claims about *where tokens
   occur*. The vocabulary had no way to state a
   claim about *what a sign's value does* — so
   every functional statement in a basis was forced
   onto the distributional axis, where it became an
   exclusivity claim it never made. §3.4 itself
   foresaw the failure mode abstractly ("a
   completion whose type-claims fall outside the
   vocabulary is handled by extending the
   vocabulary on the record") — the pilot simply
   produced the falsifier of D-M12-C03's sufficiency
   at scale: 36 claims the vocabulary could not
   hold.
2. **CR-2 (functional term → ONLY-\*).** The rule
   that converted "terminal marker, case suffix"
   into ONLY-FIN. Its warrant was A-FACE, and the
   conversion is where A-FACE's overreach became
   arithmetic: 349 medial occurrences of M342
   "contradicted" a claim that never mentioned
   inscriptions.
3. **CR-5 (strongest-single-type collapse).**
   Multi-part bases — the normal case in the
   anchors file, where a semantic identification, a
   distributional note, and a provenance trail share
   one text — were collapsed to their single
   strongest positional reading, discarding the
   rest. The collapse manufactured single claims
   out of compound evidence.
4. **CR-6 (ambiguity resolves toward the positional
   reading).** Written to keep the control able to
   fail, it instead made ambiguous text fail *as*
   positional text — coding summaries positionally
   wherever a positional reading was available. The
   control's ability to fail was bought by misreading
   the evidence it was calibrating against.
5. **A-FACE (M12 §3.2).** "A completion's value-type
   claims are taken at face value… if it calls a
   sign a suffix, it claims final-position behaviour
   for that sign." The demand that a type-claim
   carry its *full distributional content* treated
   every basis statement as if it were a claim in
   the register's own vocabulary. The bases are not
   written in that vocabulary; they are the anchors
   programme's working language, in which "INITIAL
   position (freq=16), distributional assignment"
   is a *report about a sample*, and "case suffix"
   is a *claim about a function*. A-FACE stands
   falsified as part of the closed 076 assumption
   set (F076-C08's falsifier fired). It is
   replaced, not revised: §4.

What did **not** die: A-FRAME, A-DIR, A-KEY
(inherited verbatim, §4.3); the distributional types
themselves *as distributional claims* (a sign whose
basis genuinely asserts positional exclusivity is
still judged by its row — §6 shows the teeth
remain); the tier discipline; and the pilot form
itself — a reproduction gate, a derivation, a null,
a blind positive control, verdict bands stated in
advance. The successor pilot (§7) keeps the form
and replaces the control's internals.

## 3. The two-axis vocabulary

### 3.1 The core distinction

A claim about a sign is henceforth a **pair**, whose
two components are independent and separately
judged:

- **The distributional component** — what the claim
  says about *where the sign's tokens occur*. This
  is M12 §3.4's axis, inherited without change:
  ONLY-INIT / ONLY-FIN / ONLY-MED / ONLY-SOLO,
  NEVER-INIT / NEVER-FIN / NEVER-MED / NEVER-SOLO,
  and the null component (no distributional claim
  made). Only this component can be contradicted by
  a census row, and contradiction is mechanical,
  exactly as §3.4 states.
- **The functional component** — what the claim
  says about *what the sign's value does* in the
  language: the role the value plays in the unit it
  belongs to. The functional types are:
  - **TERM-FUNC** — the value functions as a
    terminal element of its unit: an ending, a
    suffix, a case marker, a "terminal marker". The
    claim is about the value's role at the end of a
    *word or unit*, not about the slot distribution
    of the sign's tokens across inscriptions.
  - **INIT-FUNC** — the value functions as an
    opening element of its unit: a prefix, a
    proclitic, an "opening sign" in the role sense.
  - **MED-FUNC** — the value functions inside its
    unit, flanked by other material of the same
    unit: an infix, or a medial slot in a
    grammatical model of the unit.
  - **SOLO-FUNC** — the value by itself constitutes
    a complete unit or text.
  - and the null component (no functional claim
    made).

A pair is written e.g. (—, TERM-FUNC): no
distributional claim; a terminal-function claim.
M342's basis — "Terminal marker, Dravidian case
suffix" — is exactly this pair, stated in the
vocabulary for the first time without distortion
(§6.2).

### 3.2 What a functional claim does and does not commit to

The design's discipline is that a functional claim
is **not** an exclusivity claim wearing softer
clothes. Its commitments are exactly two, both
stated here so they cannot grow later:

1. **Anchor attestation.** Each functional type has
   an **anchor position**: TERM-FUNC → final;
   INIT-FUNC → initial; MED-FUNC → medial;
   SOLO-FUNC → solo. The claim commits to this:
   *the sign's value does its claimed work at its
   anchor* — which requires, in any frame that
   attests the sign at all, that the anchor position
   be attested for that sign somewhere in the
   programme's frames if the function is real and
   the frames sample the sign's life fairly. A
   functional claim whose anchor is attested
   **nowhere** — in no programme frame — is not
   contradicted (absence excludes nothing, §7.5's
   doctrine of M12, which binds this spec in full);
   it is **unsupported by attestation**, a named
   register status (§8.1) that a completion's author
   must cure with a frame that shows the anchor, or
   withdraw the claim. This is a real commitment
   with real teeth at the register level, and it is
   deliberately the *only* distributional commitment
   a functional type carries into the register.
2. **Pilot coherence.** For calibration purposes
   only (§7.3), the successor pilot checks a
   functional claim's **anchor share** — the
   fraction of the sign's tokens in the frame that
   sit at its anchor position — against the frame's
   base rate for that slot (an identity of the
   census: initial 2,655/11,507 ≈ 23.1%, final ≈
   23.1%, medial 5,972/11,507 ≈ 51.9%, solo
   225/11,507 ≈ 2.0%). A functional claim whose
   anchor share falls *below* the base rate is
   incoherent with the frame in a specific, weak
   sense: the sign is found at its claimed workplace
   *less* often than a token picked at random. This
   statistic calibrates the bridge in the pilot. It
   is a tendency instrument, it lives and dies in the
   pilot, and §8 states explicitly why it may not
   enter register entries.

A functional claim does **not** commit to:
exclusivity (any count in non-anchor positions is
compatible with it — other material follows a case
suffix inside a longer text; a word-medial sign
stands at inscription edges when its word does); a
rate (no share threshold is asserted by the claim
itself); or cross-frame behaviour (functional
claims, like everything in this design, are judged
frame by frame).

### 3.3 Why two axes, and not a longer list of types

The obvious alternative — keep one axis and add
types between ONLY-FIN and FREE ("mostly-final",
"final-leaning") — is rejected on the record, for
the reason §7.5 of M12 already gave: a graded
positional type is a tendency with a threshold, and
a threshold is a statistic wearing a type's clothes.
The 076 failure was not that the vocabulary lacked a
*grade*; it was that it lacked a *dimension*.
Function and distribution vary independently in the
bases themselves — a sign can be functionally
terminal and distributionally free (M342),
functionally medial and distributionally concentrated
(M347, §6.3), functionally silent and distributionally
exclusive (a genuine ONLY-\* basis). A vocabulary
that cannot represent the independence will keep
manufacturing the 076 failure one grade at a time.
The pair form can state all four combinations
without forcing any of them.

### 3.4 The distributional axis is unchanged — including its arithmetic

Possibility sets over the distributional axis keep
§3.4's exact semantics of M12: set membership, never
identity; the size arithmetic (0 zeros → 1 surviving
type, 1 → 2, 2 → 3, 3 → 5) unchanged; FREE of M12 is
the null component here. Nothing in the successor
re-opens a single distributional exclusion the 076
derivation produced: the Tier-C derivation of step 1
stands as computed (677 (sign, type) exclusions over
the 122 U2 signs; residual 178; solo-only 13), and
if a production register is ever licensed (§8), its
distributional half is that derivation, re-derived
under the successor's freeze from the same pins —
not re-invented.

## 4. A-FACE-2 — the successor assumption, filed as a claim

### 4.1 The claim

**A-FACE-2 (filed as claim F078-C06; design claim
D-M13-C01).** *A claim binds its maker at the
strength at which it is stated, and at no other
strength.* Strength is read from the statement's own
language, under the coding rules of §5:

- **Universal positional language** ("only",
  "never", "always", "exclusively" over positions)
  binds **universally**: it is a distributional
  type-claim, judged by the census without appeal
  to the sample it was drawn from. The author of
  such language has claimed a law, and laws are
  judged as laws in every frame.
- **Functional language** (a role: suffix, prefix,
  infix, terminal marker, slot in a unit) binds
  **functionally**: to its anchor-attestation
  commitment (§3.2) and to nothing distributional
  beyond it. The author has claimed a job the value
  does; they have not claimed where every token of
  the sign sits.
- **Summary language** (a positional report carrying
  sample markers — a frequency, a sample size, a
  "distributional assignment", a consistency note)
  binds **as a statement about the sample it
  names**: true or false of that sample, in the
  compilation it was drawn from, and *transferring
  to no other frame*. A summary is evidence about
  its own sample. It is not a claim about the sign,
  and neither the register nor a pilot may spend it
  as one.
- No claim may be **strengthened or weakened after
  the census is consulted**. Re-stating a claim at
  a different strength is a new claim, filed as
  such, and the old one stands or falls as stated.
  (This clause is A-FACE-2's anti-retreat provision:
  the failure mode it exists to prevent is the
  quiet re-reading of a falsified universal as
  "really" a summary, or of a summary as "really" a
  law when it happens to survive.)

### 4.2 A-FACE-2's falsifier

A-FACE-2 is a claim, and it can die two named
deaths:

1. **The residue case.** A basis statement in the
   strict core — or a claim in any future completion
   submitted to the register — whose
   positional/functional content demonstrably cannot
   be assigned a strength by §5's decision procedure
   without residue: language that is neither
   universal, nor functional, nor summary under the
   rules, produced from the record. One exhibited
   residue case falsifies A-FACE-2 as stated (the
   rules and the assumption are then redesigned
   together, in a new draft — never patched
   mid-pilot).
2. **The pattern-mode pilot failure.** If the
   successor pilot's positive control (§7) fails
   with its failures concentrated in one coding
   family (one axis, one rule — operationalised at
   FF-078-4), the concentration is evidence that the
   strength-reading itself — not individual claims —
   is mis-built, and A-FACE-2 falls with the pilot's
   closure word (§7.4).

What does **not** falsify A-FACE-2: individual coded
claims failing their checks. The assumption governs
how claims bind; a claim that binds correctly and is
false is a false claim, and the design's presumption
(§7.4) prices a small number of those in advance.

### 4.3 Inherited assumptions, unchanged

**A-FRAME, A-DIR, A-KEY** are inherited from M12
§3.2 verbatim, including A-KEY's ambiguity rule (the
13 duplicated Mahadevan ids are AMBIGUOUS for
derivation until resolved on the record) and Spec
076's FF-4 clarification of where that ambiguity
lives (the registry's cross-scheme join surface; the
pilot frame performs no such join, so no pilot-frame
row is excluded and attested members of the 13 carry
a join-ambiguity flag). They are filed in this
spec's register as F078-C04, F078-C05, F078-C07.
**A-FACE (076 form) is not inherited**: it stands
falsified inside the closed Spec 076 assumption set,
and this spec replaces it with A-FACE-2 as a new
claim (F078-C06). Nothing in the successor edits the
076 record of A-FACE's fall; the replacement is
prospective only.

## 5. The coding rules — NC-1…NC-8

The successor pilot's coder works from `reading` +
`basis` texts only, blind to every census row,
exactly as in 076 (FF-078-3 states the protocol in
full) — the blindness is inherited because it was
never the problem. What changes is the rules. Each
rule is stated with its decision test; §6 works them
on real text.

- **NC-1 — Universal positional language codes a
  distributional type-claim.** If the basis asserts a
  position with a universal quantifier — "only at
  the end", "never initial", "always final",
  "exclusively medial", "no initial occurrences", or
  the equivalent in the basis's own words — code the
  distributional type(s) it states (ONLY-\* or
  NEVER-\*, as stated; a basis may state more than
  one, and all are coded). This rule has no sample
  exception: quantifiers bind as written (A-FACE-2),
  even when a frequency stands next to them (NC-4).
- **NC-2 — Functional language codes a functional
  claim.** A role term — suffix, case suffix, prefix,
  infix, terminal marker, ending/opening sign *in
  the role sense*, a grammar-model slot label for a
  position *within a unit* ("slot=MEDIAL_BETWEEN",
  "between" patterns) — codes the corresponding
  functional type (TERM-FUNC / INIT-FUNC / MED-FUNC /
  SOLO-FUNC), with its anchor as §3.2 defines. A role
  term alone never codes a distributional type.
- **NC-3 — Sample-marked positional language codes a
  distributional summary.** Positional language
  accompanied by sample markers — "(freq=…)",
  "(n=…)", a count of contexts, "distributional
  assignment", "consistent X" (a sample-consistency
  note), a round/phase provenance identifying a
  distributional study — and carrying **no**
  universal quantifier, codes a **summary**: the
  basis reports where the sign's evidence
  concentrated *in a named or implied sample*. A
  summary is not a checkable claim in the pilot's
  control; it is counted and reported on the summary
  line (§7.3), with its named position and sample
  size recorded.
- **NC-4 — Precedence: quantifier beats markers;
  components coexist.** Where universal language and
  sample markers appear together, the universal codes
  a type-claim under NC-1 and the marked material is
  recorded as its provenance (a law asserted from a
  sample is still a law as stated). Where functional
  and distributional language appear together,
  **both** components are coded as a pair; neither
  absorbs the other.
- **NC-5 — Pure semantic content codes no
  component.** A depicted object, a word gloss, a
  numeral value, an external corroboration (a DEDR
  entry, a cognate) with no positional or functional
  content codes (—, —) — the pair form of M12 CR-4's
  FREE, now honestly two-dimensional: such a basis
  makes no checkable claim of either kind.
- **NC-6 — Compound bases are coded whole, never
  collapsed.** Every assertion in the basis is coded
  under its own rule and recorded; there is no
  "strongest single type". (This abolishes CR-5. A
  basis that says three things makes up to three
  codings, each judged by its own standard; the 076
  collapse is named here as a defect, not reused as
  a convenience.)
- **NC-7 — Genuine ambiguity codes the weaker
  strength, and the ambiguity is recorded.** Where
  positional language is honestly ambiguous between a
  summary and a universal claim (no quantifier, no
  sample marker, provenance unclear), code the
  summary and record the ambiguity verbatim. **This
  reverses CR-6, and the reversal is owned:** CR-6
  resolved ambiguity toward the reading that could
  fail, which in practice manufactured exclusions
  from ambiguous text — the control failed, but
  partly on evidence its own rule had distorted,
  which is why the 36 could be *explained* after the
  fact instead of *adjudicated*. The successor keeps
  the control able to fail by other means (§7.3: the
  administrability floor and the pattern clause), and
  reads ambiguous claims at their weaker strength
  because that is what A-FACE-2 says a claim is: what
  it states, no more. A coder who must guess has not
  found a claim; they have found a summary-shaped
  text, and the rules now say so.
- **NC-8 — Frame-absent signs are coded and reported
  on their own line** (CR-7, inherited unchanged): a
  sign attested nowhere in the pilot frame is coded
  as its basis states and enters neither the
  control's numerator nor its denominator.

**The worked-example line.** Three signs' bases are
worked in §6 of this spec, from the preserved 076
pilot record, as published rule illustrations:
**M002, M342, M347**. In the successor pilot these
three are coded by the blind coder like all others
but are **excluded from the control's count** and
reported on their own worked-example line — the
designer's published codings must not be allowed to
leak into the calibration they illustrate (§7.3).
Their exclusion shrinks the counted population and
is therefore conservative for the control, not
generous: M342 in particular is a claim any honest
bridge should pass, and the count does not get to
spend it.

## 6. Worked re-codings — the pilot's three texture cases, under the new rules

Each case quotes the basis **verbatim** from the
preserved 076 pilot input (`strict-coding-input.json`,
preserved with the 076 pilot record), gives the
frame row from the same pilot's output, applies
NC-1…NC-8 step by step, and then states — as the
no-softening discipline requires — **what basis text
the new rules would still exclude**. Nothing here is
a re-run: no count over the 94 is computed or
implied, and these three codings are the designer's,
published in advance, on the worked-example line
(§5) precisely so they cannot contaminate the
successor pilot's blind count.

### 6.1 The ONLY-INIT summary case — M002 ("kuṉ")

**Basis, verbatim:** "Round 2: INITIAL position
(freq=16), distributional assignment; UPGRADED-V18:
consistent INITIAL (n=16); has specific PDR reading;
Phase-272: DEDR 1694 injected + existing evidence →
HIGH"

**Frame row (076 pilot):** t = 18 — init 7, med 10,
fin 0, solo 1. Possibility set {NEVER-FIN, FREE}:
ONLY-INIT is contradicted (med + solo = 11 > 0),
which is why the 076 coding excluded it.

**076 coding:** ONLY-INIT (CR-1/CR-6 at face value)
→ **excluded**, 1 of the 22 ONLY-INIT exclusions.

**Successor coding, rule by rule:**

- "INITIAL position (freq=16), distributional
  assignment" — positional language carrying two
  sample markers at once (a frequency; the words
  "distributional assignment" naming the method that
  produced it) and **no universal quantifier**. →
  NC-3: **summary**, named position INITIAL, sample
  16.
- "consistent INITIAL (n=16)" — a sample-consistency
  note with its size stated. → NC-3: the same
  summary, restated.
- "has specific PDR reading; DEDR 1694…" —
  semantic/corroborative content. → NC-5: no
  component.
- No universal quantifier anywhere in the text; no
  role term. → No NC-1 coding, no NC-2 coding.
- **Pair: (—, —), plus one summary (INITIAL, n =
  16).** There is no checkable claim for the control
  to exclude. M002 leaves the exclusion line — not
  because its row changed (it did not: med 10 still
  contradicts ONLY-INIT, and §3.4 still says so),
  but because its basis *never made that claim*.
  What the basis made was a report about 16
  occurrences in the compilation the anchors
  programme was working from — and the pilot frame
  is a different sample, in which the same sign's 18
  tokens split 7 initial / 10 medial / 1 solo. The
  summary does not even *transfer* as a tendency: in
  this frame the sign's modal position is medial,
  not initial. That non-transfer is recorded where
  it belongs — on the summary line, as one more
  instance of the M1 lesson (a distributional
  summary is a property of its sample) — and it is
  worth stating plainly that the new rules do not
  rescue the summary. They refuse to let it
  impersonate a claim; they do not certify it as
  anything else.

**What the new rules would still exclude here.** Had
the same basis read "INITIAL **only** (freq=16)" or
"**never** medial", NC-1 would code ONLY-INIT (resp.
NEVER-MED) as a type-claim under NC-4 — provenance
markers notwithstanding — and this frame's row would
exclude it mechanically (med 10 > 0; solo 1 > 0).
The quantifier is the whole difference, and it is a
difference in what the basis *says*, not in how the
machinery feels about it.

### 6.2 The flagship — M342 ("ay/ā")

**Basis, verbatim:** "Terminal marker, Dravidian
case suffix"

**Frame row (076 pilot):** t = 1,274 — init 26, med
349, fin 876, solo 23. Possibility set {FREE}: every
positional type except FREE is contradicted by
attested occurrences — the widest row in the strict
core.

**076 coding:** ONLY-FIN (CR-2: functional term →
positional exclusivity) → **excluded** (fin-only
contradicted by init 26 + med 349 + solo 23). The
pilot record's own commentary named the absurdity:
"a case suffix that other material can follow is a
terminal *function* claim, not an inscription-final
*exclusivity* claim; §3.4's vocabulary has no type
between ONLY-FIN and FREE in which to state it."

**Successor coding, rule by rule:**

- "Terminal marker" — a role term: the value marks
  a termination. → NC-2: **TERM-FUNC** (anchor:
  final).
- "Dravidian case suffix" — a role term: a suffix
  is by definition an element bound at the end of
  its unit; "case suffix" names its grammatical job.
  → NC-2: **TERM-FUNC**, the same component, doubly
  sourced.
- No positional statement of any kind — no
  quantifier, no frequency, no position word applied
  to inscriptions (the "terminal" in "terminal
  marker" modifies the *unit's* end, which is the
  role). → No NC-1 coding; no NC-3 summary.
- **Pair: (—, TERM-FUNC).** The claim, stated in the
  new vocabulary for the first time without
  distortion: *the value of M342 does terminal,
  case-marking work at the end of its unit.* Judged
  by its own standard in the pilot's coherence check
  (§7.3): anchor share = fin/t = 876/1,274 ≈
  **68.8%**, against the frame's final-slot base rate
  ≈ 23.1% — coherent, and not marginally: the sign
  is found at its claimed workplace at three times
  the base rate, while also occurring medially 349
  times, exactly as a case suffix inside longer
  texts should. Under the old vocabulary this row was
  the control's most embarrassing exclusion; under
  the pair form it is the control's clearest
  *positive* — the same row, the same basis, a
  vocabulary that can finally say what the basis
  always said.

**What the new rules would still exclude here.** (i)
Any completion — or basis — that claims ONLY-FIN for
M342 distributionally: excluded by the row in one
step (med 349), under §3.4 unchanged. The functional
code is not a shelter for distributional over-claims;
it is a refusal to invent them. (ii) TERM-FUNC
itself, if its anchor failed: had M342's frame row
shown fin = 0 across its frames, the register would
record TERM-FUNC as unsupported-by-attestation
(§8.1); had its anchor share fallen below the base
rate in the pilot, the claim would count as a
coherence failure on the functional line. The
functional axis has its own ways to fail; they are
simply *its own*, not borrowed from an axis the
claim never addressed.

### 6.3 The ONLY-MED case — M347 ("ka")

**Basis, verbatim:** "Phase-117 grammar inference:
slot=MEDIAL_BETWEEN_CONF, n_contexts=7,
patterns=['M342-[M347]-M293', 'M028-[M347]-M367',
'M211-[M347]-M099']. Inferred from Dravidian grammar
slot model (Phases 74-112). [Phase-120: grammar
n_ctx=7≥4 → MEDIUM] [Phase-216: SA-cons=0.17 DEDR✓
source=Phase-117]"

**Frame row (076 pilot):** t = 101 — init 9, med 83,
fin 9, solo 0. Possibility set {NEVER-SOLO, FREE}:
ONLY-MED is contradicted (init + fin = 18 > 0),
which is why the 076 coding excluded it.

**076 coding:** ONLY-MED (CR-6: the slot label and
between-patterns read positionally, ambiguity
resolved toward the positional reading per the
coder's own preserved note) → **excluded**, 1 of the
6 ONLY-MED exclusions.

**Successor coding, rule by rule:**

- "slot=MEDIAL_BETWEEN_CONF", patterns of the form
  "X-[M347]-Y" — a claim about the sign's position
  **within a grammatical unit**: flanked by other
  material of the same unit, in a slot of a
  Dravidian grammar model. This is functional
  language about a unit-internal role. → NC-2:
  **MED-FUNC** (anchor: medial). It is not
  inscription-position language: a sign medial *in
  its word* stands at an inscription's edge whenever
  its word does, and the basis's own patterns are
  word-patterns, not inscription-patterns.
- "n_contexts=7", "grammar n_ctx=7≥4 → MEDIUM" —
  sample markers, attached to the *inference's
  evidence*, recording that the slot assignment
  rests on 7 contexts. Under NC-3's logic this
  provenance is recorded with the coding (it is the
  claim's evidence base, and its thinness is a fact
  the register's consumers should see), but it does
  not convert the functional claim into a summary:
  the basis does not report a positional
  *distribution* from those 7 contexts; it reports a
  *slot assignment inferred* from them. The
  distinction is in the text: a summary says "the
  occurrences were medial"; this basis says "the
  slot is medial". → Recorded as provenance on the
  MED-FUNC coding.
- No universal quantifier over inscription
  positions. → No NC-1 coding. (Contrast the form
  the pilot record's §5 describes for other ONLY-MED
  bases — "internal position (never
  inscription-initial/final)": that form carries
  inscription-level universals, and under NC-1 it
  codes NEVER-INIT ∧ NEVER-FIN as type-claims. Where
  a frame shows such a sign at an edge, the
  successor machinery excludes it exactly as 076
  did. The rules spare the slot claim; they do not
  spare universal language, from any source.)
- **Pair: (—, MED-FUNC)**, provenance: grammar-slot
  inference, 7 contexts. Pilot coherence (§7.3):
  anchor share = med/t = 83/101 ≈ **82.2%**, against
  the medial base rate ≈ 51.9% — coherent. The
  inscription-edge occurrences (init 9, fin 9)
  contradict nothing the basis claims: they are the
  word-edge cases the slot model predicts will
  exist.

**What the new rules would still exclude here.** (i)
A distributional ONLY-MED or NEVER-INIT/NEVER-FIN
claim for M347, from any basis that states one:
excluded by init 9 / fin 9. (ii) MED-FUNC with a
failed anchor: a slot claim for a sign whose medial
count were 0 in every frame would file as
unsupported-by-attestation; in the pilot, a medial
anchor share below the 51.9% base rate would count
on the functional failure line. (iii) The evidence
thinness is not laundered: 7 contexts is recorded on
the face of the coding, and §8.1 states that a
register entry carries its claims' evidence
provenance — a completion leaning on M347's slot
claim leans on 7 contexts, and the register says so.

### 6.4 What the three cases jointly show — and what they do not

The three exclusions that the pilot record itself
chose as the texture of its failure all dissolve
under the pair form — and in each case the
dissolution is a *reading* result, not a *leniency*
result: in none of the three does the basis contain
the universal language whose absence the new coding
honors, and in each case §6 names the one-word change
("only", "never") that would restore the exclusion
in full. That is the sense in which the re-codings
hold **without softening**: the machinery's teeth
are untouched; what changed is that summaries and
functions are no longer fed to them. What the three
cases do **not** show is that the successor control
will pass: the remaining 91 bases are uncoded under
NC-1…NC-8 at design time, deliberately (§7.3), and
the strict core's other functional and universal
claims may fail their own standards in numbers this
spec does not predict and must not pre-count.

## 7. Successor pilot design — the bridge, tested on its own standards

The pilot's question is narrower than 076's, because
076 already answered the wider one: **does the
redesigned bridge — two-axis vocabulary, NC-1…NC-8,
A-FACE-2 — carry the strict core's basis language
into checkable claims without manufacturing
contradictions?** Everything else the 076 pilot
tested is inherited, per §7.1–7.2. The pilot is
designed to be able to die at each of its doors,
with the closure words stated now.

### 7.1 Step 0 — reproduction gate: RE-VERIFIED, as in 076

Re-derive the inherited frame census from the
inherited pins (M12 §5/§7.1: the Spec 033 corpus
export `08fc96c8…`; the anchors file `df0cf620…`;
Registry v2 `42ab09fb…`): 2,906 records → 11,507
tokens; 5,883 strict tokens; the §7.2 identities of
M12 exact; the §7.3 partition summing to 2,655;
headline derivation numbers 677 / 178 / 13
reproduced. Any mismatch closes the pilot **CANNOT
BE RUN AS WRITTEN** — and, per §7.2, drags the
inherited step-2 standing down with it, since the
shuffle result is a property of this census.

The pins, stated in full: the corpus export
(`glossa-corpus/indus/exports/indus_research.jsonl`,
SHA-256
`08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`;
2,906 indusscript-m77 records; token construction:
the records' stored grapheme ids, dropping 680
placeholder tokens (`000`) and 452 marked tokens
(`*`-prefixed) → **11,507 tokens**; **5,883** strict
tokens; 2,880 non-empty sequences; distinct signs
attested 393); the anchors file
(`backend/reports/INDUS_FINAL_ANCHORS.json`, SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`;
287 entries, 94 `strict_sa_independent`, 44
`pending_non_sa_validation`); Registry v2
(`data/crosswalks/canonical_sign_registry_v2.csv`,
SHA-256
`42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`,
1,013 rows). Slot totals: init 2,655 / fin 2,655 /
solo 225 / med 5,972 (sum 11,507). Finals partition:
strict 1,707 / pending 250 / anchored-other 520 /
no-anchor 178, summing to 2,655. Slot base rates,
computed from these totals: init 0.2307 / fin 0.2307
/ med 0.5190 / solo 0.0196.

### 7.2 Step 2 — the shuffle leg: STANDS, not re-run (decision, with reasons)

**Decision: the successor pilot does not re-run the
shuffle null. Spec 076's step-2 result stands as this
design's inherited foundation**, cited from the pilot
record (both bars passed; empirical fraction 0.000 on
both statistics; seed 20261026; B = 999). Reasons,
stated so they can be disagreed with on the record:

1. **The shuffle leg tests a property of the frame
   and the derivation — neither of which the
   successor changes.** The redesign is entirely on
   the claim side of the bridge (vocabulary, coding
   rules, A-FACE-2). The frame pins, the token
   construction, the census, and the tested
   statistics are byte-identical to 076's. Re-running
   an identical computation on identical inputs under
   an identical seed would reproduce 076's numbers
   exactly and test nothing that is in dispute; it
   would be ceremony in the costume of rigor, and
   this programme's records distinguish the two.
2. **The one new statistic the successor uses —
   anchor share vs slot base rate (§7.3) — does not
   depend on the shuffle.** Its denominators are the
   census's slot totals, which are *identities* (M12
   §7.2: true in every scramble by construction), not
   shuffle outputs. No part of the new control
   inherits uncertainty from the decision to let
   step 2 stand.
3. **The pilot's scarce resource is blind-coder
   independence, and it is spent where the open
   question is.** A second blind coding under new
   rules is the pilot's real cost (§12); spending the
   run re-proving a settled leg would leave the
   bridge — the only thing 076 left open — tested
   with whatever independence remained.
4. **The standing is conditional, not comfortable.**
   It holds exactly as long as step 0 (§7.1)
   re-verifies the census it rests on. A step-0
   failure voids the inheritance automatically: the
   pilot closes at the gate and the shuffle leg's
   standing is recorded as fallen with the census,
   in the same record.

The label-permutation trap (M12 §8) is restated for
the successor's avoidance: nothing in this pilot
permutes labels, and no statistic in it is invariant
under the operation it tests.

### 7.3 Step 3′ — the positive control under the new rules

**Population.** The 94 strict signs, coded from
`reading` + `basis` only, by a coder blind to every
census row and to this spec's §6 codings (the
blindness protocol of FF-078-3). Lines:

- **Frame-absent line:** the 5 strict signs attested
  nowhere in the frame (039, 044, 046, 362, 374 in
  076) — coded, reported, counted neither way
  (NC-8).
- **Worked-example line:** M002, M342, M347 — coded
  by the blind coder like all others, but excluded
  from the count and reported separately, because
  the designer has published codings of them in §6
  and the calibration must not spend its own
  illustrations.
- **Counted population:** the remaining
  frame-attested strict signs — **86**, if the frame
  census re-verifies as in 076 (89 frame-attested −
  3 worked), under the frozen definition of
  FF-078-2.

**Coding.** Under NC-1…NC-8 (§5). Each counted sign
yields: zero or more distributional type-claims,
zero or more functional claims, zero or more
summaries, or no checkable claim at all. The coder's
file, with every assertion seen and every ambiguity
recorded verbatim, is preserved with the pilot
record, as in 076.

**Checks — each claim judged by its own kind's
standard:**

- **Distributional line.** Each coded type-claim is
  run against the sign's census row under §3.4's
  mechanical contradiction rules (inherited
  unchanged). A contradicted type-claim counts **one
  distributional failure**.
- **Functional line.** Each coded functional claim
  is checked for **anchor coherence**: the sign's
  anchor share in the frame (anchor tokens / total
  tokens) must be **at least the frame's base rate
  for that slot** (initial ≈ 23.1%, final ≈ 23.1%,
  medial ≈ 51.9%, solo ≈ 2.0% — computed from the
  re-verified census, not quoted from this spec).
  Below the base rate counts **one functional
  failure**. (The check is deliberately weak, and the
  spec says why: it is a calibration of the bridge's
  anchor assignments — a functional vocabulary whose
  anchors routinely point at positions the sign
  visits *less than chance* is mis-built — not a
  judgement of any claim's truth. A claim can be
  coherent and false; it cannot be incoherent and
  well-bridged.)
- **Summary line.** Summaries are counted and
  reported with named positions and sample sizes;
  their transfer behaviour in this frame (does the
  named position hold the sign's plurality here?) is
  recorded as a tendency observation. Summaries
  generate **no failures**: they make no checkable
  claim, and inventing a failure mode for them would
  rebuild CR-6's error under a new name.

**The bar — pre-committed here, derived from the
design's logic:**

> **The control passes iff (a) total failures
> (distributional + functional) ≤ 3 among the
> counted population, with neither line exceeding 2;
> and (b) administrability: at least 25 of the 86
> counted signs yield at least one checkable claim
> (distributional or functional).**

**Why this bar is not fitted to 076's 36.** Three
independent reasons, any one of which would suffice:

1. **It cannot have been computed from a recount,
   because no recount exists.** At design time,
   exactly three bases have been coded under
   NC-1…NC-8 — the §6 worked examples, which are
   *excluded from the count*. The other 91 bases (86
   counted + 5 frame-absent) are uncoded under the
   new rules; the designer has not coded them, in
   this spec or anywhere, and the bar was fixed
   without their codings. A bar fitted to a result
   requires the result; there is none.
2. **Its derivation is an attribution argument, not
   a percentile.** The tolerance exists for exactly
   one named cause: individual strict-core claims
   that are simply false. The core is a human
   artifact — the anchors file itself carries weaker
   and superseded standings alongside the strict 94
   — and a correct bridge will faithfully carry a
   false claim to its contradiction. Such failures
   are idiosyncratic: claim by claim, patternless.
   The bar's shape encodes that: a small absolute
   tolerance (≤ 3), a per-line cap (≤ 2) so no single
   coding family can spend the whole tolerance, and
   the **pattern clause** (§7.4): failures
   concentrated in one family falsify the machinery
   regardless of count. Three patternless failures
   among ≥ 25 checkable claims is the largest outcome
   still consistent with "the bridge is right and the
   core contains a few false claims"; a fourth, or
   any pattern, breaks the attribution — there is no
   count at which the bar was reverse-engineered from
   36, because 36 was produced by different rules
   coding different claim-kinds, and the number does
   not survive translation into the successor's
   units.
3. **It is stricter than 076's bar on a smaller
   denominator.** 076 allowed 5 failures among 89
   with every basis forced into a checkable type.
   The successor allows 3 among 86 while *removing*
   the forced codings — the designs' tolerances are
   not commensurable, and the successor's is the
   tighter instrument on the claims that remain
   genuinely checkable.

The administrability floor (≥ 25 of 86) is itself a
design commitment with its own failure word (§7.4):
if honest coding finds that fewer than ~29% of the
strict core's bases make any checkable claim at all,
then the register's calibration premise — that the
field's basis language contains enough stated claims
to test a bridge against — is false, and the
successor route closes on that finding rather than
passing a control that tested almost nothing.

### 7.4 Verdict bands and closure words

- **Step 0 mismatch** → **CANNOT BE RUN AS
  WRITTEN**; the inherited step-2 standing falls
  with the census (§7.2).
- **Administrability failure** (checkable claims <
  25) → **CANNOT BE ADMINISTERED — THE CORE MAKES
  TOO FEW CHECKABLE CLAIMS**; the summary/functional
  census of the bases is filed as the pilot's
  finding, and the route re-ranks on it.
- **Bar failure**, or **pattern failure** (failures
  concentrated in one coding family under FF-078-4,
  at any count the adjudication judges patterned,
  with the judgement and its grounds recorded) →
  **BRIDGE DOES NOT HOLD**: A-FACE-2 falls (§4.2),
  F078-C02 is not filed, no register is produced,
  and the closure word is appended to this spec with
  the pilot record, exploratory-labelled, in the
  advance plan's iteration loop. Iteration 2 of 3
  would remain.
- **PILOT PASSES** (step 0 exact; administrability
  met; failures ≤ 3 with neither line > 2 and no
  pattern) → F078-C02 is filed, and §8's licence
  opens: a freeze for the production register **may
  be drafted** (the freeze itself remains the
  owner's word through the hardened gate, as
  everywhere in this programme). The pilot files no
  production claim either way, and a pass is reported
  as the counts it rests on, never rounded to an
  adjective.

## 8. What a pass would license — the register under the new vocabulary

### 8.1 The entry form, precisely

Under M12, a register entry was a possibility set
over the distributional axis. Under the successor,
an entry for sign *x* in frame *F* is a **triple**:

1. **poss_D(x)** — the distributional possibility
   set, exactly as M12 §3.4/§6.2 define: the
   distributional types *not contradicted by
   attested occurrences* in F. Meaning, unchanged
   and restated because everything depends on it:
   membership records **non-exclusion** ("the data
   has not ruled this type out"), never identity
   ("x is this type"). Tier C, assumption set
   A-FRAME + A-DIR + A-KEY (+ A-FACE-2 for any entry
   whose derivation passes through a coded claim).
2. **fposs(x)** — the functional possibility set:
   the functional types **whose anchor position is
   attested for x in F** (anchor count > 0), each
   printed with its anchor count and the frame's
   name. Meaning, with the same asymmetry as the
   distributional axis and stated just as plainly:
   presence in fposs records **attested support**
   ("this function has a workplace in the data for
   this sign") — never that the sign *has* that
   function. Absence from fposs records **no
   attestation**, never that the sign lacks the
   function (M12 §7.5's doctrine, applied to the new
   axis without dilution: attestation admits;
   absence merely fails to admit; admission is not
   identification).
3. **The claims ledger for x** — every coded claim
   about x from any source (a pending reading's
   asserted pair, a completion submitted for
   judgement), each with its basis verbatim, its NC
   coding, its provenance (including evidence
   thinness, e.g. M347's 7 contexts), and its
   standing under the checks of §7.3's kinds: a
   distributional claim contradicted by the row is
   **EXCLUDED** (Tier C, the register's strongest
   word, and still its only exclusion word); a
   functional claim whose anchor is attested in no
   programme frame is **UNSUPPORTED-BY-ATTESTATION**
   (a named status, weaker than EXCLUDED and stronger
   than silence: the claim may be true of the
   language and false of every sample we hold, and
   the register says exactly that); a summary is
   filed as a summary, with its sample named, and
   carries no standing beyond it.

### 8.2 What an entry then means — and what it still does not

A register entry under the successor says, for one
sign in one frame: *these distributional types
remain uncontradicted; these functions have attested
workplaces; these stated claims stand excluded,
unsupported, or as filed.* A completion is judged
against entries component-wise: it falls where its
distributional claims meet EXCLUDED entries; it is
flagged where its functional claims meet unsupported
ones; it is never "scored" by the register, and the
register's functional half never excludes a
completion by itself — that asymmetry is the price
of the functional axis's honesty, paid openly: **the
register can kill a completion for claiming a
distribution the corpus contradicts; over function
it can only demand the anchor.** The §6.3
resolution-value ranking of M12 extends by one term
(freedom counted over both axes' set sizes) and keeps
its feeds exactly as M12 §10 fixed them — to M4 as
*ordering only*, to M7 as *bounds only* (the entries
for token 999), neither gate touched, neither feed
upgraded by the new axis.

### 8.3 What a pass does not license

No production derivation runs on the pilot's
authority: the primary-population register (M12
§5.2) still needs its own freeze. No pending reading
is promoted, demoted, or scored (§10 of M12 is
inherited whole: M4's gate is not this method's to
lift). No functional entry may be quoted without its
frame and its anchor count. And the pilot's
coherence statistic (§7.3) **does not enter the
register**: anchor share is printed in entries as a
count ratio from the census (data), while the
base-rate comparison — the statistic — remains a
pilot instrument, filed with the pilot record and
nowhere else. A register that filed coherence
verdicts would be filing tendencies as findings,
which is the confusion the tier architecture exists
to prevent.

## 9. Relationship map — inheritance and fences

- **To M12 / Spec 076.** Parent and foundation.
  Inherited: the frame discipline and pins (M12 §5),
  the tier architecture (§3.3), the distributional
  axis and its derivation (§3.4 semantics, §7), the
  shuffle finding (via §7.2's standing), the
  feasibility boundary (§9), the empty-set honesty
  (§7.6), and the closure discipline itself.
  Replaced: A-FACE (by A-FACE-2, a new claim),
  CR-1…CR-7 (by NC-1…NC-8), the one-axis vocabulary
  (by the pair form). 076's records are not edited;
  its pilot is not re-run; its closure word stands.
- **To M4.** Unchanged from M12 §10, and restated
  because the new axis makes the temptation
  concrete: the register may now file EXCLUDED
  against a pending reading's *distributional*
  claims and UNSUPPORTED-BY-ATTESTATION against its
  *functional* ones — both are deductions or named
  statuses about the claim *as stated*, delivered in
  the fitting frame. Neither is a score, neither
  lifts M4's gate, and the ranking feed remains
  ordering only.
- **To M7.** Unchanged: register entries for token
  999 are bounds the two-condition attack must
  respect; the attack remains M7's; unmapped
  witnesses constrain nothing (§4/S6 of M12
  inherited).
- **To the trigger census.** Unchanged from M12
  §10: neither run nor pre-judged by this design;
  the formal act remains the owner's call.
- **To the owner's projected-constraints framework.**
  As M12 §10 stated, and not enlarged by succession:
  what is borrowed is the discipline — necessities
  conditional on stated assumptions, exclusions over
  identifications, the residual made explicit — and
  the successor inherits that paragraph's fences
  verbatim (no cross-programme evidence transfers;
  no entry may cite the framework as support; M13's
  §3–§5 definitions govern where usages differ).

## 10. Claims of this spec

- **F078-C01 — the inheritance is sound** (design
  D-M13-C04). Spec 076's steps 0–2 results are
  properties of the inherited pins and derivation,
  and stand as this design's foundation.
  *Falsifier:* a step-0 re-verification mismatch in
  the successor pilot (§7.1), which closes that
  pilot at its gate and voids the standing in the
  same record.
- **F078-C02 — the bridge holds at the pre-committed
  bar (pilot-gated)** (design D-M13-C02). Coded blind
  under NC-1…NC-8, the strict core's checkable claims
  fail their own kinds' standards at most 3 times
  among the counted population (neither line above
  2, no pattern), with at least 25 of 86 counted
  signs yielding a checkable claim. *Falsifier:* the
  §7.4 closure words, each as stated. **Filed only
  if the successor pilot passes**; the pilot record
  is appended to this spec either way.
- **F078-C03 — the pair form suffices to state the
  register** (design D-M13-C03). Every register entry
  and every coded claim the successor machinery
  produces is expressible as a §8.1 triple without
  residue. *Falsifier:* a derived constraint or a
  basis assertion the pair form cannot state,
  produced on the record — whereupon the vocabulary
  is extended as a new claim and prior entries are
  re-derived, never translated by hand (M12
  D-M12-C03's discipline, inherited).
- **F078-C04…C05, C07 — the inherited assumption
  claims** A-FRAME, A-DIR, A-KEY (§4.3), each with
  the falsifier its statement carries.
- **F078-C06 — A-FACE-2** (design D-M13-C01) (§4.1):
  a claim binds its maker at the strength at which
  it is stated — universal language universally,
  functional language functionally, summary language
  as a statement about its named sample — and no
  claim may be re-strengthened or weakened after the
  census is consulted. *Falsifier:* §4.2's residue
  case, or the successor pilot's pattern-mode
  failure.
- **F078-C08 — the pilot calibration claim.**
  The step-3′ control's bar and administrability
  floor, as §7.3 states them, judged on the blind
  coding under FF-078-3.
- **F078-C09 — output discipline.** The register is
  triples; membership and attested support, never
  identity; the coherence statistic never enters the
  register; the ranking feeds M4 as ordering only
  and M7 as bounds only.
- **F078-C10 — the non-claims.** This spec claims no
  reading, value, or identification for any sign;
  not that any completion exists; nothing about
  signs in frames not derived; and not decipherment,
  in any wording: the standing position of the
  programme — **the script is not deciphered** — is
  unchanged by anything in this spec.

## 11. What this spec does not establish

No reading, value, or identification for any sign —
the successor changes how claims are *carried*, and
a better bridge to a census is still not a
decipherment. Not that the successor pilot will
pass: the 91 bases beyond §6's three are uncoded
under the new rules at design time, and the strict
core's universal and functional claims may fail in
numbers this spec neither predicts nor pre-counts.
Not that A-FACE-2 is true: it is a claim with a
stated falsifier, standing exactly as exposed as
A-FACE stood before the pilot killed it. Not that
the summaries the new rules decline to spend were
worthless — several are the anchors programme's real
distributional knowledge, filed here as what they
are (statements about their samples) rather than
what 076 forced them to impersonate. Not that the
functional axis exhausts what bases say: F078-C03
carries the residue falsifier precisely because a
third kind of content may be waiting in the texts,
and if it is, this spec wants to die on it in the
open, as its parent did. And not decipherment, in
any wording: the standing position of the programme
— **the script is not deciphered** — is unchanged by
anything in this spec.

## 12. Cost and dependencies

Successor pilot: days, not weeks — every input is in
hand and pinned (the inherited pins of §7.1; the
preserved 076 pilot files for the worked-example
line). The real cost is the blind re-coding of 94
bases under NC-1…NC-8 with its verbatim ambiguity
record, and the record-keeping the gate demands; the
computation is seconds. No dependency on ICIT
access, on the Laursen lawful copy, on M7's freeze,
or on any other in-flight stream. A production
register remains gated on the successor pilot
passing *and* a freeze, with its depiction arm
additionally gated on the owed C-1 split sensitivity
(M12 §4, S5), exactly as in the parent design.

## 13. The S4 note (queued at the rerun audit of 2026-10-26, F4)

The rerun-invalidation audit of 2026-10-26 queued a
note for whoever prepared this freeze (its item F4):
when M13 is prepared for freeze, its positive
control and null design should state explicitly how
the S4 structured-generator rule applies to it — or
why its structure already covers the concern. S4 is
the governing-rule extension adopted from the
2026-10-26 indirect-methods scan: because a
deterministic generator of seal-like inscriptions
for a fictional non-language passes published
statistical language diagnostics, permutation nulls
are necessary but not sufficient **for score-based
methods** — their pilots must also face a calibrated
structured generator where one exists for their
statistic. This section states how S4 applies to
M13, in five parts.

**(a) M13's verdicts do not rest on the class S4
governs.** S4 governs methods whose verdict rests
on a score or a language-likeness diagnostic — a
number that says how language-like a text or a
reading looks. M13's verdicts rest on two things
that are not scores: deduction (the distributional
line is mechanical contradiction of a stated
universal claim by attested occurrences — a count of
contradictions of claims, not a likeness measure)
and a blind human-language coding control (the
step-3′ coder reads basis texts under NC-1…NC-8 and
the claims are judged by their own kinds'
standards). No language-likeness diagnostic appears
anywhere in the pilot, and no verdict is a threshold
crossing of a likeness score.

**(b) The pilot's one statistic files nothing and can
never enter a register entry.** The anchor-share
comparison (§7.3) is a calibration device for the
bridge: it asks whether the functional vocabulary's
anchors point at positions the signs visit at least
at the frame's base rate. It is deliberately weak,
it judges no claim true or false, and §8.3 bars it
from the register outright — anchor share enters an
entry only as a count ratio from the census (data),
while the base-rate comparison itself stays in the
pilot record. So no filed claim ever rests on a
statistic a structured generator could spoof: a
generator that manufactured seal-like texts could in
principle move a base rate, but it cannot move a
filed claim, because no filed claim cites the
comparison.

**(c) The inherited shuffle leg already carries its
own S4 boundary, and M13 does not extend it.** Step
2 is not re-run (§7.2); it stands as Spec 076's
result, and 076's own S4 note (its spec §14, recorded
at its freeze) states the boundary for that leg: its
two statistics are census-concentration measures
tested against a marginals-preserving shuffle, its
calibration is an independent blind positive
control, and S4 therefore added no generator arm to
that pilot. M13 inherits the result with the note
attached; it does not re-run, re-word, or extend the
leg, and it claims no new standing for it.

**(d) The structured-fake risk that does apply to a
coding control is named, and the design already
carries its counters.** A coding control's analogue
of a structured fake is basis language that *looks*
claim-shaped but is not — text whose surface form
invites a stronger coding than its statement
supports. That is precisely the failure 076 measured
(summaries and functional terms wearing type-claims'
clothes), and the successor's counters are built for
it: NC-7 codes genuine ambiguity at the weaker
strength with the ambiguity recorded verbatim, so
claim-shaped text cannot be silently spent as a
claim; the summary line reports summaries as
summaries, so their volume is visible rather than
converted; A-FACE-2's residue falsifier (§4.2) kills
the assumption outright if a basis statement's
content cannot be assigned a strength without
residue; and the pattern clause (FF-078-4, §7.4) is
the tripwire — failures concentrated in one coding
family close the pilot as BRIDGE DOES NOT HOLD at
any count, which is the coding control's version of
discovering that the instrument, not the material,
produced the result.

**(e) Conclusion, and the boundary going forward.**
For these reasons **no SIGIL-class structured
generator arm is added to this pilot**: there is no
score for a generator to spoof, no filed claim rests
on the pilot's one statistic, and the fake-risk that
does apply to the control is the one the control was
redesigned to catch. The boundary is recorded here
so it travels with the method: **any future
score-based use of the register — any use that leans
on a statistic of language-likeness — takes S4 with
it at that time**, including a calibrated structured
generator arm where one exists for that statistic.
