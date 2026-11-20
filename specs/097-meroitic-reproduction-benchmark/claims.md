# Spec 097 — Claims

Every claim carries at least one falsifier (a concrete observation
that would show it false) and a "does not establish" line (the
over-reading it forbids), per the program's claims discipline. The
same set, normalized into `aee-claims.json` without substantive
change, is validated under the pinned AEE at adoption (Stage 0;
`records/adoption-aee-assessment.json`). The criteria every claim
below binds were fixed before execution in the founding scoping
(`specs/095-red-team-remediation/second-targets/meroitic-benchmark-scoping-2026-11-17.md`),
which is this program's provenance of record.

## Step 0

**C097-1 — Nothing computes before the corpus is pinned and its
licensing is on the record.** No benchmark computation runs before
the paper's corpus repository is pinned by exact commit, its
license (or its absence) is recorded, and a C095-3-style identity
record for the pinned corpus is filed under this spec; the corpus
is held in custody and is never committed to this repository or
redistributed, and only the program's own code and derived
aggregate statistics are published.
*Falsifier:* a benchmark result dated before the step-0 identity
record; a corpus file, authors' embedding, or authors' code file
found in this repository's tree or history; or an identity record
whose pin does not resolve to the commit the computations used.
*Does not establish:* that the corpus is the one the paper's
authors used for every count — only that the benchmark's inputs
are exactly the pinned ones, named.

## The legs

**C097-2 — Leg A reproduces the published census or names each
divergence's cause.** Each of the ten published counts (Table 1:
193, 897, 302, 708; section 5.3: 871, 1,729, 99,338, 1,868,
17,257, 782,761) and each Table 2 dictionary size (26, 18, 15, 14,
9, 6, 3) is either reproduced exactly from the pinned corpus under
a counting basis stated before the count was taken, or reported
as diverged with the traced cause (counting basis, repository
state, or material never published) named on the record.
*Falsifier:* a published count for which the outcome record shows
neither an exact reproduction nor a named, traced cause; or a
counting basis in the outcome record that is absent from the
execution freeze.
*Does not establish:* that a reproduced count validates the
paper's downstream claims — a census match is a statement about
the corpus and the counting, not about decipherment.

**C097-3 — Leg B tests the fixture's sign inventory against the
published corpus.** The corpus's attested sign set is compared
against the fixture's 19 signs after explicit reconciliation of
the paper's E-for-/o/ convention (and a dotted-variant fold stated
in the freeze); computed frequency ranks are compared against the
fixture's ME rank order at the fixed Spearman rho 0.90 bar; and
positional (initial/medial/final) distributions are computed and
archived either way.
*Falsifier:* the outcome record reports criterion (i) met while an
attested sign outside the reconciled 19 goes unnamed; reports the
rho without its computation basis; or lacks the archived
positional distributions.
*Does not establish:* that a mismatch impeaches the fixture's use
as an inventory for other purposes — the leg measures the
fixture's stated frequency-rank convention against this corpus,
and a divergence is a finding about that convention's fit to the
2025 corpus, not about Meroitic sign values, which are not in
question.

**C097-4 — Leg C reproduces the alignment headlines in their
fixed bands, with attempts accounted.** Under the paper's
hyperparameters and the freeze's two arms, unseen-dictionary
precision at 10 equals 0 percent, training-dictionary accuracy
sits in the at-most-25 percent band, and the numerals dictionary
is best or tied at 100 dimensions; every alignment attempt,
including failures, appears in the run index.
*Falsifier:* a headline reported outside its band without the leg
being reported as not reproduced; a run index with a gap against
the frozen settings grid; or a seeded (training) dictionary scored
as unseen.
*Does not establish:* anything about whether Meroitic can be
deciphered by alignment — the leg tests whether the paper's
published headlines reproduce, and the paper's own reading of its
0 percent unseen result (that the signal is lexical memorization,
not transfer) stands as the paper's, not this program's.

## The verdict and the bound

**C097-5 — The falsifier is applied as fixed, not as convenient.**
The outcome record applies the scoping's falsifier verbatim: if
Leg A fails on a majority of its counts with divergences tracing
to the published corpus or the paper's stated methods, the
premise is falsified and the outcome is NOT REPRODUCED; a step-0
failure gives NOT EXECUTABLE AS SCOPED; otherwise each leg carries
its own verdict exactly as its criteria read.
*Falsifier:* an outcome record whose verdict does not follow from
its own per-count table under the stated rule; or a verdict of
NOT REPRODUCED (or REPRODUCED) that the per-leg verdicts do not
support.
*Does not establish:* a judgment on the paper's scholarship beyond
reproducibility — a NOT REPRODUCED outcome under this falsifier is
a statement about the published record's completeness for
reproduction, stated as such.

**C097-6 — No outcome of this benchmark moves any other program
record.** No verdict, count, or statistic produced under this spec
changes any Indus claim, anchor, standing, or fixture of record;
the deciphered Meroitic sign values validate no Indus method; and
any transfer claim to another script is a separate claim, in that
script's own package, with its own falsifier.
*Falsifier:* an Indus record whose text, standing, or count
changes citing this benchmark as its basis; or a transfer claim
filed under this spec's claim ids.
*Does not establish:* that transfer is impossible — only that this
benchmark does not perform it.
