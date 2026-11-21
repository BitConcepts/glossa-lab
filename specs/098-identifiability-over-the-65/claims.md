# Spec 098 — Claims

Every claim carries at least one falsifier (a concrete
observation that would show it false) and a "does not
establish" line (the over-reading it forbids), per the
program's claims discipline. The same set, normalized into
`aee-claims.json` without substantive change, is the claims
bundle of record for this package, intaken into the
canonical ledger at adoption (D-098-3). The design every claim binds was frozen before any
test inscription was revealed to any scoring path
(`records/freeze-v1-2026-11-21.md`).

## The freeze

**C098-1 — Nothing is scored before the freeze and the seal.**
No held-out inscription is revealed to the scoring path, and
no scoring-path code runs on development data for this study,
before the freeze record is committed and the Stage 1 seal
record (held-out count and SHA-256 only) is committed; the
held-out list is released to the scoring path exactly once,
at scoring, and that release is recorded.
*Falsifier:* a scoring output, run-index entry, or development
export dated before the seal record; a second release of the
held-out list; or a seal hash at scoring time that does not
recompute from the released list (which voids the run as
SEAL FAILURE).
*Does not establish:* that the held-out material is pristine
against the candidates' historical derivation — that is
C098-6's separate, capped question.

**C098-2 — The population and its values are the frozen
annex's, exactly.** The study tests the 65 I candidates and,
as its secondary arm, the six E readings, with sign
identities, allograph handling, candidate values, reading
variants, and grammatical assumptions exactly as the
population annex and the crosswalk of record state them at
the pinned commit; no value is resolved, split, respelled,
or re-glossed after the freeze.
*Falsifier:* a scored sign absent from the annex; a scored
value differing from the annex's recorded value for that
sign; or a grapheme-to-sign mapping in the scoring inputs
that the frozen crosswalk does not carry.
*Does not establish:* that the annex's values are correct —
the annex freezes what is tested, not what is true.

## The comparison

**C098-3 — Every scored sign faces the full frozen rival set
under matched conditions.** Each sign's candidate is compared
against rivals R-A (matched wrong Dravidian value), R-B
(unrelated-family value), R-C (logogram), R-D (structural-
only), and the model-level permutation R-E, constructed on
development data only under WP8 fairness conditions (matched
tuning budget, matched available evidence); Arm E signs
additionally face the cross-sign and comparandum-as-value
rivals named in the spec.
*Falsifier:* a scored sign whose outcome record lacks any of
the five rival scores; a rival constructed using held-out
data; or a tuning-budget asymmetry between candidate and
rivals in the run record.
*Does not establish:* that the rival set is exhaustive of all
conceivable alternatives — it is the frozen, named set the
audit's "serious alternatives" requires, and its limits are
stated, not hidden.

**C098-4 — Success must be value-relevant.** A sign can reach
a pass outcome only on an accepted prediction sheet whose
differing observables are value-relevant (neighbour identity
or class, referent-distinguishing context, or a collocation
on which phonetic and logogram rivals differ); success on
language-neutral position or frequency alone — including
beating the structural-only rival R-D — never suffices, and
a sign with no accepted sheet is NOT IDENTIFIABLE by
construction.
*Falsifier:* a pass outcome whose prediction sheet's only
differing observable is position or frequency; or a scored
sign with no prediction sheet in the pre-unsealing record.
*Does not establish:* that a borne-out value-relevant
prediction proves the value — it is the frozen bar for
discrimination, not a decipherment criterion.

**C098-5 — The decision rules are applied as frozen.** Each
sign's outcome is the frozen vocabulary's, under the frozen
precedence (UNDECIDABLE AT THIS POWER before NOT
IDENTIFIABLE before the pass outcomes), the frozen bars
(minimum 5 held-out tokens; penalized margin at least 10
nats; above the permutation null's 99th percentile,
B = 999, seed 9801), and the frozen flexibility penalty of
2 nats per free choice, charged to candidates and rivals
alike.
*Falsifier:* an outcome record whose per-sign outcome does
not follow from its own margins, counts, and null under the
stated rules; a bar, seed, or penalty in the outcome record
absent from the freeze; or a family-level summary that is
not counts of per-sign outcomes.
*Does not establish:* that the bars are the uniquely right
ones — they are the frozen ones, stated in advance so the
study cannot be tuned to its results.

## The bounds

**C098-6 — The contamination ceiling is honoured.** Because
the candidates were historically derived on the program's
full corpus, the in-corpus held-out arm is pseudo-held-out:
its pass outcome is DISCRIMINATED ON PSEUDO-HELD-OUT and
supports no identification claim beyond the corpus; only a
pass on the Stage 1 genuine-holdout subset (material
documented as absent from every candidate-generation input)
can be reported IDENTIFIABLE ON HELD-OUT; if no such subset
exists, that absence is itself recorded.
*Falsifier:* an IDENTIFIABLE ON HELD-OUT outcome scored on
in-corpus material; or a Stage 1 record that omits the
provenance audit's result.
*Does not establish:* that a pseudo-held-out discrimination
is worthless — it is real evidence about predictive fit,
capped at what its provenance can carry.

**C098-7 — No outcome of this study moves any other program
record.** No per-sign outcome, margin, or family count
produced under this spec changes any reading's standing,
anchor, or class (including the audit's E/I relabels, which
are separate acts); identifiability outcomes and support
dispositions are kept in their separate vocabularies per
Standards Part III rule 5.
*Falsifier:* a standing, anchor, or register entry changed
citing this study as its basis without a separate act of
record; or a record that converts an outcome here into a
support disposition.
*Does not establish:* that standings should never change on
this evidence — only that this study does not change them.

**C098-8 — Execution discipline: venue, index, payload
verdicts.** All execution runs on tower-compute in a fresh
clone; every scoring attempt, including failures, appears in
the run index; and every reported run verdict is the run's
own payload verdict record, never a wrapper or transport
state.
*Falsifier:* a run executed on the coordination VM or the
mini-server; a run index with a gap against the frozen
settings; or a reported verdict that is a wrapper state
rather than the payload's own record.
*Does not establish:* that a complete index proves the runs
were correct — it proves they are all on the record, which
is what makes their correctness checkable.
