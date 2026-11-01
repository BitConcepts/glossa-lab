# Spec 078 — Adjudication (drafting record and freeze rulings)

This record carries the drafting decisions for Spec
078, the projected-constraint bridge redesign
(method M13), from its design draft (2026-10-26,
programme goal record, SHA-256
8bb02c07a8ad3245a899da660c48430b4cf1e16a53b1fb53a132215093e9a211)
to this freeze, under the owner's order of
2026-10-26 ("review, freeze, and run the M13
pilot"). The design is carried as written; the only
additions are the freeze-fixed completions of §3
below — places the design itself left open for the
freeze to close — each stated in spec §0 and ruled
here. No bar, threshold, frame, null, or closure
word of the design was moved.

## 1. Provenance

- The method is the successor design to M12 (Spec
  076), drafted 2026-10-26 as iteration 1 of the
  projected-constraint move's iteration loop (cap:
  three iterations, then the move re-ranks on
  evidence or closes PARKED), exploratory-labelled
  throughout. Its parent pilot closed the same day:
  ASSUMPTION SET DOES NOT HOLD (36 exclusions
  against a bar of 5), with the failure localised
  to the bridge — the one-axis vocabulary, coding
  rules CR-1…CR-7, and A-FACE — while steps 0–2
  passed exactly and by wide margins.
- The freeze order is the owner's, 2026-10-26:
  review, freeze, and run the M13 pilot. The pilot
  executes under FF-078-5 after this freeze merges.
- The S4 note at spec §13 answers the queued item
  F4 of the rerun-invalidation audit of 2026-10-26,
  which asked whoever prepared this freeze to state
  explicitly how the S4 structured-generator rule
  applies to M13 (ruled at DD-078-6 below).

## 2. Freeze-prep review (conducted before drafting; outcome: no amendments required)

The freeze worker reviewed the M13 design draft for
internal consistency before carrying it into frozen
form. Every check below was run against the draft
text and, where a figure is named, against a
first-hand re-derivation from the pinned inputs
(the three input digests recomputed from the local
copies of the repo files and equal to their pins;
the census re-derived by the model of Spec 076's
derivation and reproducing every pre-named figure
exactly — the C2 record carries the independent
recomputation from the pinned inputs only).

- **Bars.** The pilot bar appears in the draft's
  §7.3 and is restated in §7.4 and in draft claim
  D-M13-C02 (§10): total failures ≤ 3 over the
  counted population; neither line (distributional,
  functional) above 2; the pattern clause (§7.4:
  failures concentrated in one coding family close
  the pilot regardless of count); administrability
  ≥ 25 of 86 counted signs yielding at least one
  checkable claim. All four statements agree; no
  second, different bar appears anywhere in the
  draft.
- **Coding rules NC-1…NC-8.** All eight rules are
  present in §5, each with a decision test; the
  cross-references resolve (NC-4's precedence is
  used by NC-1 and NC-3; NC-6 abolishes CR-5 by
  name; NC-7 reverses CR-6 by name and owns the
  reversal; NC-8 inherits CR-7). The
  worked-example line (M002, M342, M347) is stated
  in §5 and administered consistently in §7.3.
- **A-FACE-2's falsifier.** Present at §4.2 in both
  named forms: the residue case and the
  pattern-mode pilot failure. §4.1's three strength
  classes (universal, functional, summary) and the
  anti-retreat clause are stated without exception
  clauses that would swallow them.
- **Counted-population arithmetic.** 94 strict
  signs − 5 frame-absent (039, 044, 046, 362, 374,
  per Spec 076's pilot record) − 3 worked examples
  (M002, M342, M347) = 86. The three worked
  examples are frame-attested (their §6 frame rows
  are non-empty), so the subtraction does not
  double-count the frame-absent five. The draft
  states the figure as conditional on step-0
  re-verification ("86, if the frame census
  re-verifies as in 076"); the freeze carries that
  conditionality into FF-078-2, which freezes the
  definition rather than the number.
- **Base rates against slot totals.** Initial
  2,655/11,507 = 0.2307 ≈ 23.1%; final the same;
  medial 5,972/11,507 = 0.5190 ≈ 51.9%; solo
  225/11,507 = 0.0196 ≈ 2.0%. The draft's §3.2 and
  §7.3 figures agree with the re-derived census to
  the precision the draft prints. The §6 anchor
  shares also reproduce: M342 fin/t = 876/1,274 =
  68.8%; M347 med/t = 83/101 = 82.2%.
- **Failure texture against the 076 pilot record.**
  The draft's §1/§2 counts (36 of 89; 22 ONLY-INIT
  summaries; 8 ONLY-FIN functional terms; 6
  ONLY-MED) agree with the pilot record's §4–§5
  (22 + 8 + 6 = 36; coded among the attested:
  ONLY-INIT 28, ONLY-FIN 8, ONLY-MED 7).

**Outcome: no genuine drafting defect was found,
and no amendment to the design draft was required
or made.** The draft's goal-files text stands
exactly as filed (SHA-256 8bb02c07… above). The
five freeze-fixed completions of §3 are the
freeze's own additions, stated in spec §0 in the
programme's standing form; none of them repairs a
defect in the draft, and none moves a bar.

## 3. Freeze rulings

- **DD-078-1 — Numbering and phase.** This freeze
  consumes **Spec 078** (the next free spec number
  after 077, consumed by the M7 freeze) and
  **Phase 444** (sequential after Spec 076's Phase
  442 and Spec 077's Phase 443). Directory:
  `specs/078-projected-constraint-bridge-redesign`.
  Experiment id:
  `spec078-projected-constraint-bridge-redesign`.
- **DD-078-2 — The claim set.** The register
  carries ten claims, F078-C01…F078-C10: the
  design's D-M13-C04 (inheritance soundness) as
  C01; D-M13-C02 (the bridge holds, pilot-gated)
  as C02; D-M13-C03 (pair-form sufficiency) as
  C03; the inherited assumptions A-FRAME / A-DIR /
  A-KEY as C04 / C05 / C07; the successor
  assumption A-FACE-2 (D-M13-C01) as C06; the
  successor pilot's calibration as C08; the
  design's output discipline and non-claims as
  C09 / C10. A-FACE in its 076 form is **not**
  carried: it stands falsified inside the closed
  Spec 076 assumption set, and carrying it forward
  would misstate the record. F078-C02 is
  pilot-gated: it is filed as a supported claim
  only on a pilot pass.
- **DD-078-3 — Freeze-fixed completions.**
  FF-078-1 (numbering: Spec 078, Phase 444),
  FF-078-2 (the counted population defined
  mechanically — frame-attested strict signs per
  the step-0 re-verified census, minus the three
  worked examples; expected 86; the definition,
  not the number, is frozen), FF-078-3 (the
  blindness protocol in full: the coder receives
  only the anchors reading+basis texts for the 94
  strict signs and the NC-1…NC-8 rules, blind to
  every census row, to the 076 pilot's per-sign
  rows, and to the design draft's §6 codings; the
  coding file preserved with the pilot record),
  FF-078-4 (the pattern clause operationalised: a
  coding family is an (axis, NC rule) pair, and
  separately a basis-provenance family; a pattern
  finding is an adjudicated judgement with grounds
  recorded, triggered for consideration when ≥ 2
  failures share one family; the bar's counts
  stand regardless, and the clause can only close
  the pilot as BRIDGE DOES NOT HOLD, never rescue
  it), and FF-078-5 (pilot execution order: after
  this freeze merges on genuine CI including the
  required C4 check — step 0 re-verification, then
  step 3′ blind coding checks, then the §7.4
  verdict; run once as frozen; step 2 not re-run,
  its standing inherited from Spec 076 and void
  automatically if step 0 fails) are adopted as
  spec §0 states them. Each closes a place the
  design left to the freeze or states mechanically
  what the design stated in prose; FF-078-4
  expressly does not change the bar.
- **DD-078-4 — AEE hook findings.** Ruled after the
  hooks run at this freeze; the findings and their
  answer from the spec's own structure are recorded
  in `aee/freeze-aee-note.md` and summarised in
  freeze.md §4. The register was not reworded to
  silence any challenge.
- **DD-078-5 — An OSF registration IS filed at
  this freeze.** Contrast Spec 076's DD-076-5,
  where the M12 design named no OSF registration
  and none was filed. Here the owner's express
  order for M13 directs the full freeze act
  including its filing, and this freeze therefore
  carries the registration as part of the act: the
  coordinator performs the OSF filing after merge
  via the proven ORCID/token-link route (OSF
  sign-in is ORCID only, per the programme's hard
  rule), and the registration's identifier is
  recorded with the pilot record when it lands.
  Nothing in the pilot depends on the registration;
  the repo freeze record governs the pilot either
  way. (This freeze package itself performs no OSF
  act.)
- **DD-078-6 — The S4 note.** The note queued by
  the rerun-invalidation audit's item F4 is written
  into the spec as its §13 and summarised in
  freeze.md §6. Its argument, in short: (a) M13's
  verdicts rest on deduction and a blind
  human-language coding control, not on scores or
  language-likeness diagnostics — the class S4
  governs; (b) its one statistic, anchor share vs
  slot base rate, is a pilot calibration device
  that files nothing and may never enter a register
  entry (spec §8.3), so no filed claim ever rests
  on a statistic a structured generator could
  spoof; (c) the inherited step-2 shuffle result
  already carries Spec 076's own S4 boundary note,
  and M13 does not re-run or extend it; (d) the
  structured-fake risk that does apply to a coding
  control — basis language that looks claim-shaped
  but is not — is what NC-7, the summary line, and
  A-FACE-2's residue falsifier exist to catch, with
  the pattern clause as tripwire; (e) therefore no
  SIGIL-class generator arm is added to this pilot,
  and the boundary is recorded so any future
  score-based use of the register takes S4 with it
  at that time. The freeze worker reviewed each
  part of that argument against the design and
  judges it sound as written; no part of it needed
  correction in the adjudication.
- **DD-078-7 — This freeze is a required-C4
  freeze.** The C4 records check is a required
  branch-protection check (owner act of 2026-10-25,
  after the 075 shadow freeze). The gate records
  under `gate-records/` are filed beside this
  record and must pass the C4 job in CI on the
  freeze PR.

## 4. What was not changed

The bars of §7.3 (total failures ≤ 3; neither line
> 2; administrability ≥ 25 of 86), the pattern
clause, the closure words of §7.4, the frame and its
pins, the two-axis vocabulary, NC-1…NC-8, A-FACE-2
and its falsifier, the inherited step-2 standing
and its step-0 conditionality, and the non-claims
of §11 stand exactly as the design wrote them. No
pilot quantity was computed at drafting or at the
freeze: the only computations performed are the
census reproductions the design itself prints and
the gate's C2 recomputation of the same figures.
In particular, no basis beyond the design's three
published worked examples was coded under
NC-1…NC-8 by the freeze worker, and the bar was
not checked against any such coding.

## 5. Establishes / does not establish (adjudication)

This adjudication establishes that the design was
carried into frozen form without moving any of its
bars, with its open places closed on the record,
its freeze-prep review conducted and recorded, and
its queued S4 note answered in the spec's own text.
It does not establish that the pilot will pass,
that the bridge holds, that A-FACE-2 is true, or
anything about what any sign means.
