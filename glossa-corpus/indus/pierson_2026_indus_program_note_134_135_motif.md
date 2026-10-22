# Program note, Spec 024 Stages 1–1b: the motif-coding pilots — a middle-band pilot, a clarified codebook, and a fresh-sample re-pilot that answered the same way

**Tristen Pierson** (BitConcepts LLC) — ORCID 0009-0003-7269-956X

Program note, 2026-10-09. Prepared as an addendum to the
program's preprint record (Zenodo concept record DOI
10.5281/zenodo.20379070; previous published version v4.6.0,
DOI 10.5281/zenodo.23267995, record 23267995). Program
provenance registry: OSF [osf.io/ybd65](https://osf.io/ybd65/).
Code, frozen specs, and machine-readable results:
BitConcepts/glossa-lab (Spec 024; Phases 134–135; repository
main at commit 11e70c9889c52fe8640b89365dbecb2aa65fb48f,
merge of PR #112; the release-source commit for this note is
recorded in `RELEASE_VALIDATION.json`).

This note reports Spec 024's Stage 1 motif-coding pilot
(Phase-134) and its owner-directed continuation (Phase-135)
exactly as they stand in the merged reports
(`reports/phase134_pilot_report.md`,
`reports/phase135_pilot_report.md`), negatives included.
Neither phase changed any decipherment anchor: the anchors
file `backend/reports/INDUS_FINAL_ANCHORS.json` is
byte-identical throughout (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed).
The Phase-125 verdict — **FAIL — DISAGREEMENT** — is final
and unchanged; spec 020's adjudication outcome — **NO** —
stands untouched. **PRED-2026-001, PRED-2026-002, and
PRED-2026-003 remain PENDING.** No association statistic of
any kind was computed in either phase, and nothing in this
note is evidence that any particular reading of any Indus
sign is right or wrong.

## Abstract

Spec 024's Stage 1 asked a prior question before any motif
evidence could be used: can depictions on CISI Vol. 1–2
objects be coded reliably at all — measured, with frozen
gates, on bounded samples? Phase-134 coded a fresh
100-object stratified frame with two blinded passes, a gold
third coding, and full adjudication: exact agreement
**0.84**, Cohen's κ **0.7885** — the frozen proceed gate
(≥ 0.85 and κ ≥ 0.75) was **not met** by one object on the
agreement arm, the stop rule (< 0.70 or κ < 0.50) did not
fire, and the verdict was **MIDDLE BAND**. Its disagreement
concentrated on one nameable boundary — whether a worn
depiction is classifiable at all (10 of 16 disagreements
involving ILLEGIBLE). The owner directed a combined path:
clarify that boundary from the pilot's own adjudicated
record, re-pilot on a fresh sample under identical gates,
freeze a Stage 2(b) motif × sequence design only if the
proceed gate is met, and publish the combined record either
way. The clarification (five decision rules, B1–B5, frozen
before the re-pilot frame was drawn; taxonomy, precedence
rule, and every threshold unchanged) was executed as
Phase-135 on 100 entirely fresh objects (zero overlap with
the first frame, verified). Result: exact agreement
**0.78**, κ **0.7129** — **MIDDLE BAND for the second
time**, both gate arms short, stop rule again not fired.
No Stage 2(b) design follows on this record. The
clarification changed coder behavior in its intended
direction — ILLEGIBLE use halved — but reproducibility did
not follow: on a fresh sample under the clarified codebook,
this pipeline's measured reliability was lower, not higher.
Both pilot datasets (codes, notes, disagreement logs; no
images) are deposited with this release under **CC BY
4.0**, as the owner's combined-path approval directed.

## 1. Stage 1 as frozen (Phase-134)

Spec 024 Stage 1 (spec §4) tests whether the 12-code
motif taxonomy seeded from the published iconographic
categories (unicorn; zebu/bull; buffalo; elephant;
rhinoceros; goat/antelope; tiger; composite creatures;
human figures and cult/narrative scenes; geometric
designs; script only / no depiction; illegible / cannot
code) can be applied to CISI Vol. 1–2 object photographs
reproducibly. The stage freeze (`stage1-freeze.md`,
2026-10-09, on the owner's separate post-Stage-0 go) set
the frame (exactly 100 objects from the frozen §4.2
population of 3,245 — the shorthand "909 motif-chapter
objects" proved 98.9% unicorn-chapter and degenerate as a
frame; the correction is recorded in the freeze), the
codebook, the metric definitions, and the §4.5 gates:
**proceed** at exact agreement ≥ 0.85 **and** κ ≥ 0.75;
**stop** below 0.70 or κ < 0.50; middle band otherwise,
with the owner's decision framed and no silent middle
path. All coding roles were executed by AI agents
(Muse Spark) in blinded, role-isolated instances —
a disclosure carried in every artifact of both phases;
the agreement numbers are properties of this coding
pipeline, not of human expert coding.

## 2. Phase-134 — the first pilot (PR #111, merge c4a3ef4c)

Two blinded passes over the 100-object frame, a gold third
coding of a 20-object subset, adjudication of all 16
disagreements with the log preserved; every quantity
computed by script from the on-disk records. Exact
agreement **0.84** (84/100), Cohen's κ **0.7885**;
adjudication upheld pass A 10 times, pass B 6. Per-category
agreement was interpretable only in the four large
categories (SCRIPT_ONLY 0.833, UNICORN 0.793, GEOMETRIC
0.714, ILLEGIBLE 0.667). The confusion structure was the
finding: 10 of 16 disagreements involved ILLEGIBLE —
SCRIPT_ONLY×ILLEGIBLE 5, ILLEGIBLE×UNICORN 3, and one each
ILLEGIBLE×ELEPHANT and GEOMETRIC×ILLEGIBLE — against 6
identity/boundary calls among depictions. Gold drift
showed no outlier pass (A–B 0.80, A–G 0.85, B–G 0.75,
unanimous 0.70). One process deviation is recorded
(report §3, D1): a completion handoff raced its own final
writes, a verification snapshot read 23 of 25 records,
and a blinded top-up was commissioned for two objects
before the batch's own records landed; the metrics
script's fail-loud duplicate check caught the collision,
the original records governed, and the data impact was
none — a second live instance of the Phase-132 §4(d)
finding that batch self-reports are not data. Gate
application, exactly as frozen: proceed **NOT MET** (the
agreement arm, by one object), stop **NOT FIRED** →
**MIDDLE BAND**; the motif arm was not eligible for
Stage 2(b) on this pilot, and the report framed the
owner's options — accept the pilot, clarify the
ILLEGIBLE / SCRIPT_ONLY / GEOMETRIC boundary and
re-pilot, or let the arm rest.

## 3. The combined path and the clarification (freeze-2)

The owner (2026-10-09) chose the combined path:
"clarify the boundary, re-pilot fresh, freeze Stage 2(b)
only if the gates pass, publish the combined record."
The clarification amendment (`stage1-freeze-2.md`, freeze
commit `dee4e5c2`, committed before the re-pilot frame was
drawn and before any re-pilot image was viewed) defines
only the legibility boundary, distilled from the 16
adjudicated Phase-134 disagreements, whose rulings are
quoted as worked examples:

- **B1 — Classifiability threshold.** A depiction is
  classifiable only when a diagnostic feature of a
  specific code (horn number/shape, hump, trunk/ear,
  skin folds, body build) is discernible; a surviving
  fragment with none — a head/neck corner, a truncated
  body, hindquarters alone — is ILLEGIBLE.
- **B2 — Eroded or broken depiction field.** A reserved
  depiction field surviving only as blank erosion with
  faint traces, or a depiction fragment at a break, is
  ILLEGIBLE, not SCRIPT_ONLY.
- **B3 — No depiction is not an illegible depiction.**
  Erosion or wear with no outline, no fragment, and no
  reserved field means no depiction is present:
  SCRIPT_ONLY.
- **B4 — Script row vs geometric design.** Marks in a
  line as inscription characters are script, including
  signs with internal geometry; GEOMETRIC requires a
  deliberate design as the sole marking outside a script
  row; a single slit or stroke is a mark, not a design.
- **B5 — The positive side.** Damage does not defeat
  classification when a diagnostic feature remains
  discernible (the adjudicated unicorn/rhinoceros/
  composite rulings anchor this side).

Restated in the freeze so there is no ambiguity: the
12-code taxonomy, the precedence rule, the metric
definitions, the protocol, and **every gate threshold are
unchanged by any amount**. No rule loosens a code's
definition to manufacture agreement.

## 4. Phase-135 — the re-pilot (PR #112, merge 11e70c98)

Population: the same 3,245 eligible objects minus the
100 Phase-134 frame objects → 3,145; draw by the same
stratified rule with a new phase salt
(`phase135-20261009`), exactly 100 objects, gold subset
20. **Freshness: overlap with the Phase-134 frame = 0**,
asserted by the frame script at draw time and verified
independently against both committed frame records. All
100 objects yielded crops (210, zero failures); no
replacement was needed. Protocol identical in every
procedural respect, coders issued the clarified codebook
only — its worked examples were the sole Phase-134
material any coder saw. Record sets verified complete
before the metrics run (A 100, B 100, gold 20,
adjudication 22); the fail-loud checks passed on the
first run. **Deviations: none.**

Results as found. Exact agreement **0.78** (78/100);
Cohen's κ **0.7129** (chance agreement 0.2338 from the
marginals: SCRIPT_ONLY 36/34, UNICORN 29/29, ILLEGIBLE
14/12, GEOMETRIC 8/8, ELEPHANT 3/7, the remaining
categories ≤ 4 per pass, ZEBU and COMPOSITE unused).
Adjudication rate 0.22, upholding pass A 16 times and
pass B 6. Per-category agreement: GEOMETRIC 0.778,
UNICORN 0.758, SCRIPT_ONLY 0.750, ILLEGIBLE **0.368**,
TIGER and HUMAN_CULT 1.0 on two objects each, the small
animal categories 0–0.5 on 2–7 objects. Confusion: 12 of
22 disagreements still involved ILLEGIBLE
(SCRIPT_ONLY×ILLEGIBLE 8 by direction, ILLEGIBLE×UNICORN
2, and one each against ELEPHANT and GEOMETRIC), and 10
were depiction-identity calls (UNICORN×ELEPHANT 2,
UNICORN×BUFFALO 2, six singles) — roughly double
Phase-134's identity share. Gold drift: A–B 0.75,
A–G 0.90, B–G 0.75, unanimous 0.75; no outlier pass. The
adjudicated composition (descriptive only): SCRIPT_ONLY
38, UNICORN 30, ILLEGIBLE 10, GEOMETRIC 8, ELEPHANT 4,
all other codes ≤ 2, ZEBU and COMPOSITE 0 — identifiable
non-unicorn depictions remain thin in a proportional
draw, as Phase-134 found.

Gate application, identical numbers applied exactly:
proceed gate **NOT MET** (agreement 0.78 < 0.85 and
κ 0.7129 < 0.75 — both arms short this time); stop rule
**NOT FIRED** (0.78 and 0.7129 both clear). **Verdict:
MIDDLE BAND, for the second time.** Under the freeze's
branch obligations, no Stage 2(b) design is drafted, and
the re-pilot report (§8) frames the owner's decision
without a recommendation dressed as a verdict: accept a
pilot knowingly below the frozen gate as a new
adjudication; change the measurement basis itself (human
expert coders, or a materially different instrument) and
re-measure; or let the motif arm rest with both pilots
as its final record.

## 5. What the two pilots establish, and what they do not

Side by side (descriptive; the pilots differ in sample
and codebook, so this is not a controlled comparison):

| Quantity | Phase-134 | Phase-135 |
|---|---|---|
| Exact agreement | 0.84 | 0.78 |
| Cohen's κ | 0.7885 | 0.7129 |
| Disagreements | 16 | 22 |
| … involving ILLEGIBLE | 10/16 | 12/22 |
| ILLEGIBLE marginals (A/B) | 27 / 23 | 14 / 12 |
| ILLEGIBLE per-category agreement | 0.667 | 0.368 |
| Proceed gate | not met | not met |
| Stop rule | not fired | not fired |

The clarification did what it was written to do to
*coder behavior* — ILLEGIBLE calls halved, in the
direction Rules B3/B5 intend (commit where no depiction
is present, or where a feature is discernible) — and
reproducibility did not follow. The Phase-134 reading
that the disagreement was mostly one definitional
boundary is **not supported** by the re-pilot: the
boundary moved, and the disagreement moved with it, into
the residual legibility cases and into depiction
identity. What stands after both pilots: this pipeline
reproduces a primary motif code 78–84% of the time
(κ 0.71–0.79) across two fresh samples and two codebook
versions; the frozen gates have now answered twice, and
they do not answer "proceed." Motif evidence under this
spec therefore remains what Stage 0 graded it — the
richest field in hand (Holdat `iconography`) is Class C,
one compilation's unverifiable coding — and no
association test under §5.3 has been designed or run.
Nothing here touches any reading, anchor, or prediction;
associations, had any test run, would in any case have
described use, not meaning (spec §8).

## 6. What this release deposits, and the limits that govern it

Deposited with v4.7.0, under **CC BY 4.0**, per the
owner's combined-path approval: this note;
`phase134_pilot_dataset.json` + provenance meta and
`phase135_pilot_dataset.json` + provenance meta (both
passes, the gold coding, adjudicated codes, and the full
disagreement logs of both pilots — this program's own
work product); carried forward unchanged from v4.6.0:
the Stage 0 inventory dataset + meta, the prior program
notes, the addendum, `RELEASE_VALIDATION.json`,
`AUDIT_CORRECTIONS.json`, `INDUS_FINAL_ANCHORS.json`
(byte-identical; see the header), and the v3 preprint PDF
(external). **No images are deposited, ever** — crops and
photographs remain in the program's gitignored local
store. The mandatory release gate
(`backend/scripts/release_gate.py`, per
`docs/RELEASE_CHECKLIST.md`) was run against the staged
files from a clean checkout of the release-source commit
before deposit; its output, the deposit DOI, and the
post-deposit checksum confirmation are recorded in
`RELEASE_VALIDATION.json` (`release_v4_7_0`).
