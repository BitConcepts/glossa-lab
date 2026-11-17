# T304 — Reading Direction as Data: Registry Extension and Positional Re-issue (2026-11-16)

Spec 095 Stage 3, claim C095-10.

## The carrier, and the choice

Orientation basis is carried in the corpus identity registry
(backend/glossa_lab/data/corpus_identity.py, Spec 095 Stage 1):
every registered corpus identity now carries an
`orientation_basis` field beside its pin, census and
normalization, and the Corpus Identity Standard states the rule
at glossa-indus/CORPUS_IDENTITY_STANDARD.md section 5. The
registry was chosen over a free-standing document because it is
already the identity of record for the claim-bearing corpora —
the place a loader, and a reader, already goes to learn what a
corpus is — and because the standard's section 4 discipline (an
identity changes only by a recorded act in the same change) then
governs orientation changes too.

As registered, none of the eight covered corpora records a
reading-direction basis. Each entry says so in its own words and
names the standing assumption positional use makes instead:
stored order taken as reading order. Registering the assumption
does not promote it to a corpus fact; it makes it visible, which
is the defect RT-27 names (no corpus carried an orientation
basis, and positional statistics silently inherited one).

Anchor-level direction notes exist in the record — some
Phase-108 anchor trail entries carry a `reading_direction` field
("rtl") — and section 5 of the standard states why they do not
discharge the corpus requirement: they record an assumption made
about individual anchor entries, not a basis of any corpus.

## The re-issue list

Scope, per the stage plan: the positional results this stage
touches — the Phase-125 cross-compilation comparison (the
GR-088-16 family line, touched by T301's third fixture and by
the T303 applications' distributional evidence) and the
positional material inside the six anchors' records (touched by
T303). Nothing else was re-issued; no study was re-run.

### R1 — Phase-125 cross-compilation positional comparison (spec 019): re-issued, both orientations

Assumption named: profiles as stored in
reports/phase125_cross_compilation_results.json — stored order
taken as reading order on both sides (the mayig layer and the
Holdat layer, per their new registry basis entries). The
reversed variant reads every stored profile in the opposite
direction (initial and terminal rates exchanged, medial
unchanged) on both sides, and recomputes the arm statistics from
the recorded per-pair profiles. This is a re-issue on the
recorded data, not a re-run: the pairing, the floors and the
verdict pattern are the study's own.

Verification of the instrument: in the as-recorded orientation
the recomputation reproduces every filed statistic to the six
decimals the study reports (primary arm: median TV 0.636931,
median W1 0.658181, Spearman initial -0.424758, terminal
0.316034, modal agreement 0.187500; arm B: median TV 0.636931,
median W1 0.726396, initial -0.245008, terminal 0.291861, modal
0.250000; arm A coincides with the primary arm, as the study
itself registers).

Reversed variant, all three arms: per-pair TV is identical
under the joint reversal (maximum absolute difference 0.0 in the
primary and A arms; per-pair W1 differs by at most 1.11e-16,
and by at most 4.0e-06 in arm B, an artifact of the profiles
being stored rounded to six decimals). Median TV and median W1
are therefore unchanged (0.636931 and 0.658181 primary; 0.636931
and 0.726396 arm B). Spearman initial and terminal exchange
values (primary: initial becomes 0.316034, terminal becomes
-0.424758; arm B: 0.291861 and -0.245008). Modal agreement is
unchanged (0.187500 primary; 0.250000 arm B). The pairing-shuffle
null is a statement about pairings, not orientations, and is
unchanged (p_null 0.824, primary).

What the re-issue shows: the study's FAIL — DISAGREEMENT verdict
is orientation-invariant, because the comparison applies one
orientation assumption to both compilations; reversing both
sides cannot manufacture or remove the disagreement. What is
*not* invariant is any statement that names an end: which
profile is "initial-heavy" flips with the assumption. The
original report makes no such end-naming claim in its verdict;
downstream uses that do are the ones this re-issue governs.

### R2 — Phase-127 diagnostic, arms (a) and (b) (spec 021): invariance derived, not recomputed

The split-half noise floor and the matched-size null compare
halves and subsets of the single Holdat compilation under one
orientation; a reversal acts identically on both sides of each
comparison, so the figures are orientation-invariant by the same
reflection argument as R1. Stated as a derivation: the
diagnostic's per-replicate draws are not filed in the tree, so
no recomputation from record is possible, and none is claimed.

### U1 — The six anchors' Phase-48 positional-test outcomes: reversal undefined on the record as filed

The positional test consumed per-sign profiles computed at
runtime from the Holdat layer. That layer is not in the tree
(the registry verifies it by pin and by absence), and the filed
record of the outcomes (the WP5 audit) carries outcomes without
the profiles they were computed from. A reversed variant
therefore cannot be computed from the record as filed, and none
is asserted. This is itself an instance of the defect RT-27
names; the registry and standard changes above are the
prospective fix — a future positional run must file its profiles
and name its basis.

### U2 — Token frequency counts: reversal not defined

The counts the T303 applications cite (Phase-107 table: M044
n = 19, M047 n = 13, M124 n = 3, M202 n = 4, M329 n = 5, M330
n = 3) do not depend on sequence orientation. A reversed variant
of a count is not a different number; reversal is undefined for
them, and they are re-issued unchanged under either orientation.

### U3 — Position-independent anchor flags: reversal not defined

The anchor trails' `mahadevan_position_independent` flags are
defined without reference to orientation. Reversal is undefined
for the flag itself; no variant exists to file.

## What this discharges

C095-10's falsifier is a positional or sequential result in a
claim-bearing record with no named orientation assumption, or no
reversed variant and no undefined-reversal statement. The
results this stage touches are re-issued above, each with its
assumption named and its reversed variant computed or its
undefined-reversal statement filed; the corpora those results
rest on now carry their orientation basis (or its recorded
absence) in the registry; and the standard makes the requirement
prospective for every positional result from adoption.
