# The Projected Constraints skeleton (generalization program, document 1)
Status: commissioned by the owner 2026-11-04 ("do both in
order," item 1). This document states the domain-independent
skeleton proposed in the generalization scoping note
(docs/GENERALIZATION-SCOPING-NOTE-2026-11-04.md in AXIOVEX/vexa)
formally enough that a second instantiation can be judged
against the G1 to G5 bar. It is a research document, not a
verdict: whether anything outside physics instantiates this
skeleton is exactly what the commissioned study tests.

## Definitions
D1. RECORD SYSTEM. A domain has a record system when its state
is known only through a set R of partial records: discrete,
inspectable items (observations, measurements, texts, reports,
assertions), each with a provenance. A record is not the system;
it is evidence about the system.
D2. PROJECTION. A projection is a stated rule pi that maps a
candidate system state to the records it would produce. Two
states are projection-equivalent when pi cannot distinguish
them. Everything the record system can ever know is a property
of the equivalence classes of pi, never of the states inside a
class.
D3. PRIMITIVE ABSOLUTE. A primitive absolute is a quantity the
framework takes as given in absolute terms (not relative to the
records). The skeleton permits AT MOST ONE, and requires it to
be named. If a domain needs two, it does not instantiate this
skeleton; it instantiates something else, and the study must
say so.
D4. NECESSARY CONDITION. A statement N is a necessary condition
for a record system when N holds of every state in every
projection-equivalence class consistent with the records. A
necessary condition is derived, not fitted: its proof or
derivation must proceed from D1 to D3 and the domain's stated
projection rule, and it must carry the observation that would
refute the derivation's application (a record the framework
declares impossible, observed).
D5. SEPARATOR. A separator is a computable quantity or test S
over records whose value partitions candidate states into
classes the records can distinguish: S differs across classes
it claims to separate, and is invariant inside a class. A
separator counting law, where one exists, states how the
number or capacity of independent separators grows with the
record system's size; a domain may have separators without a
counting law, and must say which it has.
D6. EXECUTABLE MATRIX. The records, the claims about them, and
their relations form a matrix that is (a) generated from the
domain's append-only ledger by script, (b) executable: an
engine computes its implications and settles claim statuses
mechanically, (c) gated: publication of any derived view is
blocked while a verification gate fails. This element is the
winning combination, stated as a definition; VEXA is its
maintained form.

## The skeleton, stated
A domain instantiates the Projected Constraints skeleton when
it exhibits all five, in its own terms:
S1. A record system (D1) with provenance on every record.
S2. A projection rule (D2) stated before results, including an
    explicit account of what the records cannot distinguish.
S3. At most one named primitive absolute (D3), or a proof that
    none is needed.
S4. The separator and necessary-condition machinery (D4, D5)
    defined over the domain's own records.
S5. An executable matrix (D6) carrying the domain's claims,
    verdicts, and corrections.
The physics instantiation (Appendix A) is the existence proof
for the skeleton's coherence, not evidence for any other
domain.

## Judging criteria (the bar, restated from the scoping note)
A claimed instantiation is judged by an independent reader
against G1 to G5 (scoping note). This document adds the judging
protocol: the reader receives ONLY this skeleton, the domain's
G1 document (its records, projection, absolute, stated before
results), and the domain's records; the reader does not receive
the domain team's conclusions. The verdicts available are
INSTANTIATES (all five S elements and G1 to G5 met), ANALOGY
(some S elements hold only metaphorically; the report must name
which), and NOT YET (a named S element or G item is unattempted
or unproven, with the missing work stated). ANALOGY and NOT YET
are publishable outcomes, recorded in the improvement registry
either way.

## Falsifier for this document
This skeleton document fails, and must be revised or withdrawn,
if either occurs: (a) a domain meets S1 to S5 and G1 to G5 and
independent practitioners of that domain judge the result to
have nothing to do with their field (the skeleton is then a
tautology that fits everything and means nothing); or (b) the
physics instantiation is shown not to meet S1 to S5 as stated
(the skeleton does not describe its own origin).

## Appendix A: the physics instantiation (summary, not the body)
Records: causal-set elements and counting data in sprinklings,
with provenance (the program's datasets and frozen runs).
Projection: order plus counting; the founding axiom is the
identifiability result that from order plus counting alone only
the dimensionless combination rho R^2 is identifiable.
Primitive absolute: exactly one dimensionful scale, irreducible
in principle. Necessary conditions and separators: the F0
theorems (invariance on rescaling orbits; no estimator from
causal-set data alone recovers absolute scale; one datum of
known nonzero weight fixes the orbit) and the separator
counting law (canonical home: projected-constraints-program,
papers/separator-counting-law). Executable matrix: the RCPH
program's ledger, matrix, and gated map. Largest named gap in
the instantiation: dynamics. Nothing in this appendix is
evidence for any other domain; it is the calibration case the
skeleton was abstracted from.

## Appendix B: what a domain team must produce (G1 checklist)
1. The record system's definition, with provenance rules.
2. The projection rule, written before results, including the
   cannot-distinguish account.
3. The named primitive absolute, or the none-needed proof.
4. One derived necessary condition with its falsifier (G2).
5. One computed separator, validated on held-out records (G3).
6. One instance of the domain's gate refusing or killing a
   claim (G4), from the domain's own records.
7. Reproduction materials sufficient for the G5 reader.
