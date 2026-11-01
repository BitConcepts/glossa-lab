# Spec 078 — Pilot record (Phase 444)

**Executed 2026-10-26**, once, exactly as frozen
(spec §7, FF-078-5), after the freeze merged
(PR #418, merge commit e8376d74a29be79114b933391dde34c479a53dcc;
CI all checks passing including the required C4
freeze-gate records check, read from the runs' own
job conclusions). Freeze digest:
`d7ccfae47bcb771bca1c332bdb0f64eb7ef8de23de28d166aba9fb995961427b`.
OSF registration filed at the freeze (DD-078-5):
**49fgu** — https://osf.io/49fgu/ — registered
2026-10-26T16:00:51Z, 29 preregistration responses
completed from the frozen spec; at the time of
this record its admin approval is still pending
(the token-link approval requires the owner's
authenticated OSF session; the API approval route
returns HTTP 409, as on prior registrations — the
registration itself, the timestamped act, is
complete; see `osf-spec-registration.md`).

## Verdict

**PILOT CLOSES — CANNOT BE ADMINISTERED: THE CORE
MAKES TOO FEW CHECKABLE CLAIMS** (the design's
§7.4 closure word for administrability failure).
Step 0 passed exactly, so the inherited Spec 076
step-2 standing stands. The blind coding, checked
mechanically against the census, yields checkable
claims from **7 of the 86 counted signs** against
the frozen administrability floor of **25**. Under
the frozen text, claim **F078-C02 is not filed**,
and **no register is produced**. The pilot's
finding is the census of the strict core's basis
language itself, filed at §4 below: read at the
strength at which it is actually stated, the
core's language is overwhelmingly distributional
summaries and semantic identifications — reports
about samples and claims about referents — and
makes almost no claims of the kinds a census can
judge. The route returns to the advance plan's
iteration loop (this was iteration 1 of 3), which
re-ranks on this finding.

## 1. Step 0 — reproduction gate: PASS

Re-derived from the three pins, fetched from the
merged freeze on repository main and digest-verified
before the run (corpus export `08fc96c8…` — the
fetched file is byte-identical to the freeze pin
and to the Spec 076 freeze's local input; anchors
`df0cf620…`): 2,906 indusscript-m77 records; 680
placeholder + 452 marked tokens dropped; **11,507
tokens**; **5,883 strict tokens**; 2,880 non-empty
sequences; slot totals init 2,655 / med 5,972 /
fin 2,655 / solo 225; finals partition strict
1,707 / pending 250 / anchored-other 520 /
no-anchor **178**. Every figure equals the
expected value. The inherited step-2 standing
therefore **stands** (§7.2): the shuffle result
remains this design's foundation, cited, not
re-run.

## 2. The blind coding — production and reconciliation

The step-3′ coding was produced by a coder working
from the 94 strict signs' `reading` + `basis`
texts and the NC-1…NC-8 rules only — blind to
every census row, to the Spec 076 pilot's per-sign
rows and coding output, and to the design draft's
§6 codings. One sequencing fact is recorded
plainly, because the record is the record: the
coding was commissioned in parallel with the
freeze build and was completed and hash-sealed at
2026-10-26T14:37Z (SHA-256
`d63eb914ec62d9faa8e664828f1ef57973a2797400ccf46dc46811b6a851370b`)
— before the freeze digest existed and before
the freeze merged. The freeze worker never opened
it (its existence is flagged in the freeze
package's own report); the bars it would be judged
against are the design draft's, frozen in the
repository without reference to it; and the
mechanical checks of §3 were run exactly once,
after the merge, on the sealed file, whose digest
was re-verified against the seal immediately
before the run. The blindness the design requires
— independence of the coding from the census and
from the designer's worked examples — holds in
full; the timing is disclosed here rather than
smoothed over.

Coder's totals over all 94 signs: **0
distributional type-claims**; **12 functional
claims** (TERM-FUNC 6, MED-FUNC 4, INIT-FUNC 2,
SOLO-FUNC 0); **38 summaries**; 50 codings in all
across 44 signs; **50 signs with no codable
content of any kind** under the rules (semantic
identifications, glosses, corroborations —
NC-5). The zero on the distributional line was
verified independently by the pilot worker: the
words "never", "always" and "only" occur in none
of the 94 bases, and every "exclusive" phrase in
the corpus of bases (13 signs) asserts exclusivity
over seal **motifs** ("Exclusive to tiger seals"),
not over positions. Under NC-1, honestly applied,
the strict core states no positional universal at
all.

## 3. Step 3′ — the checks

Population lines, mechanical against the step-0
rows: frame-absent **5** (039, 044, 046, 362, 374
— coded, counted neither way, NC-8; M362 carries
2 coded functional claims and M374 1, reported
here for completeness and spent nowhere);
worked-example **3** (M002, M342, M347); counted
**86**, as the frozen definition gives.

**Administrability (assessed first, as frozen):**
counted signs yielding at least one checkable
claim: **7** (M176, M267, M305, M336, M351,
M367, M375 — each carrying exactly one functional
claim; distributional claims: none). Floor: 25.
**7 < 25 → the pilot closes at this door.** The
failure count is therefore not the verdict's
basis; it is recorded below as observation, as
the frozen run produced it.

**The checks as run (recorded observations):**
- Distributional line: 0 claims, 0 failures.
- Functional line (counted): 7 claims, **5
  incoherent** — anchor share below the slot base
  rate computed from the step-0 census: M267
  TERM-FUNC 0.0266 vs 0.2307; M305 TERM-FUNC
  0.0000 (the sign has no final occurrence in
  this frame at all); M336 TERM-FUNC 0.0388;
  M351 MED-FUNC 0.0000 (no medial occurrence in
  this frame); M367 TERM-FUNC 0.1667. Coherent:
  M176 TERM-FUNC and M375 INIT-FUNC.
- Worked-example line (excluded from the count,
  reported as designed): M342 TERM-FUNC coherent
  (anchor share 0.6876 vs 0.2307) and M347
  MED-FUNC coherent (0.8218 vs 0.5190) — the
  blind coder, who never saw §6, coded both
  flagship bases exactly as the design's worked
  examples did, and both pass their own kind's
  standard. M002's summary (INITIAL, n = 16) does
  **not** transfer to this frame: the sign's
  plurality here is medial — recorded on the
  summary line as the tendency it is.
- Summary census (counted line): 36 summaries;
  the named position holds the sign's plurality
  in this frame in 15, and does not in 21. No
  failures attach to summaries (§7.3); the
  transfer record is the M1 lesson at scale — a
  distributional summary is a property of its
  sample — and it is filed here as a tendency
  observation, nothing more.

## 4. The finding — what the core's language is

The design priced this outcome in advance
(§7.3): if honest coding finds that fewer than
about 29% of the strict core's bases make any
checkable claim at all, then the register's
calibration premise — that the field's basis
language contains enough stated claims to test
a bridge against — is false, and the successor
route closes on that finding rather than passing
a control that tested almost nothing. That is
what happened, and at greater strength than the
floor contemplated: the figure is 7 of 86
(8%). The remaining 79 counted bases divide
into summaries (36 counted) — the anchors
program's real distributional knowledge, stated
as reports about the samples it was drawn from —
and semantic identifications that make no
positional or functional claim of any kind.

Two further observations are filed for the
iteration loop's re-rank, as observations, not
verdicts. First: even the few functional claims
the core does state mostly fail their own
kind's coherence standard in this frame (5 of
7 counted), two of them with an anchor share of
exactly zero — the frame attests the claimed
workplace nowhere. Whatever the re-rank
concludes about the bridge, the core's
functional vocabulary and the frame's evidence
are far apart, and any future register work
must reckon with that directly. Second: the
blind coding surfaced a genuine gap in the
rules, recorded by the coder and confirmed
here — NC-1…NC-8 say nothing about assertions
that a basis itself retracts or supersedes
inside its own text (three signs carry such
passages: M047, M063, M267). The coder coded
the retracted material as no current claim and
recorded the passages verbatim. That reading is
adopted for this record; a rule for it is
iteration 2's to write, in a new draft, never
patched into this one.

## 5. A-FACE-2 — adjudication of the residue candidates

The coder filed two residue candidates against
A-FACE-2's falsifier (§4.2, first death). Each
is adjudicated here, with grounds:

- **M222** — basis: "Promoted from anchor
  staging archive (2026-06-07…); evidence_
  type=compound_slot_coherence; score=1.00;
  status=verified; DEDR: shine / lightning
  (verb)". **Not a residue case.** The phrase
  the coder flagged is an evidence-type label
  from the anchors program's staging machinery:
  it describes how the anchor was evidenced,
  not anything about where the sign occurs or
  what its value does in a unit. The basis
  carries no positional or functional content
  whose strength would need assigning; its one
  content-bearing element is a semantic gloss,
  which NC-5 codes (—, —), and the remainder
  is provenance, recorded as such. A residue
  case under §4.2 requires content that
  demonstrably cannot be assigned a strength;
  a text with no such content is NC-5's home
  ground, not a counterexample to it.
- **M233** — basis: "Settlement/place marker".
  **Not a residue case.** This is a semantic
  identification — a claim about what the sign
  denotes, of the same kind as a depicted-object
  gloss. "Marker" here names no unit and no
  anchor: NC-2's role terms are positions
  within a unit (suffix, prefix, infix,
  terminal marker of a unit, unit-internal
  slot), and a place marker asserts a
  referent, not a unit-internal role. NC-5
  codes it (—, —) without residue. The
  boundary is recorded precisely so it binds
  future coders: had the basis read "marks the
  end of a place-name" — a role inside a unit —
  NC-2 would have coded TERM-FUNC.

The coder's flags were the correct procedure —
both texts sit near a rule boundary, and the
falsifier watch is supposed to surface them.
**No exhibited residue case stands**, so
A-FACE-2's residue falsifier does not fire.
Its pattern-mode falsifier does not fire
either: the pilot did not fail by the bar — it
closed one door earlier, at administrability,
on a finding about the core's language, not
about the bridge. **A-FACE-2 therefore stands
neither confirmed nor falsified**: a claim
whose test could not be administered, carried
forward as a draft claim into the iteration
loop, exactly as exposed as it was filed.

## 6. Filings and non-filings

- **F078-C02: NOT FILED** (its condition — a
  pilot pass — did not occur). It remains draft
  in the frozen register, permanently
  unadvanced by this pilot.
- **No register is produced**, in any form. The
  §8 licence does not open.
- The remaining register claims stand as frozen:
  C01 (inheritance soundness) is **confirmed in
  its step-0 part** — the census re-derived
  exactly — and its step-2 part stands
  inherited, unvoided. C03 (pair-form
  sufficiency) is untested by this pilot: the
  pair form stated every coding the run
  produced, and no claim the machinery produced
  needed a form outside it; that is consistency,
  not a verdict, and it is recorded as such.
- The pilot artifacts are preserved under
  `pilot/`: `pilot_run.py` (the single frozen
  run), `pilot-results.json` (the full output,
  every line and every check), `strict-coding-
  input.json` (the coder's only input),
  `strict-coding-output-nc.json` (the sealed
  blind coding), `coder-note.md`.

## 7. What this pilot establishes / does not establish

**Establishes:** the inherited census reproduces
exactly a fourth independent time, and the Spec
076 step-2 standing survives its conditional
test; the redesigned bridge can be administered
honestly — its rules, applied blind, produce a
complete and auditable coding of the strict
core; and the strict core's basis language,
read at the strength at which it is stated,
contains checkable claims for only 7 of 86
counted signs — the calibration premise of the
register route, as designed against this core,
is false. That last finding is a result, bought
by a control designed to be able to deliver it:
it redirects the program from calibrating
bridges against this basis language toward the
questions the finding itself raises (what the
summaries, as sample-reports, can jointly
support; whether a register should be built
against claims the field has actually stated
in claim form, or not built against this core
at all).

**Does not establish:** that the bridge is wrong
— it was barely exercised, and A-FACE-2 stands
unfalsified (§5); that the strict core's
readings are wrong — summaries and glosses are
not false for being uncheckable, and nothing
here re-judges any reading; that the necessity
program is empty — the step-2 finding stands,
and its Tier-C derivation exists as a
computation exactly as it did after 076; or
anything about any sign's meaning. Not
decipherment: the standing position is
unchanged — **the script is not deciphered**.

## 8. Route status

Spec 078's pilot is **closed: CANNOT BE
ADMINISTERED — THE CORE MAKES TOO FEW CHECKABLE
CLAIMS**. The move returns to the advance plan's
iteration loop, exploratory-labelled: iteration
1 of 3 consumed (076 was the parent's single
run; this draft was the successor's iteration
1). No re-run of this pilot, under any
parameters, is authorized by this record;
iteration 2, if the loop takes it up, is a new
draft judged as this one was — and it starts
from §4's finding, not from this pilot's
machinery.
