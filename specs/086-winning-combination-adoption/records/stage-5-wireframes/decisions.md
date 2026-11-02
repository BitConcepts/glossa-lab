# Spec 086, Stage 5 — decisions for the owner (T501)

Each question is decided by Tristen's approval act on this package. The
worker's recommendation is marked on each. Approving the package as
recommended adopts all eight as wired in the wireframes; any question can be
decided differently, and the wireframes then change before T502 starts —
the wireframes are the requirements, and a decision against a recommendation
is a wireframe change, not a build-time choice.

---

**Q1 — The system view carries no graph canvas in v1.**
Spec 085's system view was a node-link graph explorer. The intervening
stages changed what can honestly be drawn: the gated chain produces no
verified claim-graph edge set. The claim×claim dependency pairs (790) are
coverage data the generator carries, not cells; claim×anchor edges do not
exist (the three sign references resolve to no matrix cell); the one edge
set the chain does verify — the sign×sign co-occurrence block — is visible
on the system view as the block it is. A canvas drawn over anything else
would fabricate edges the gate never checked, and C086-17 makes the map
render generated data exactly.
**Recommendation: adopt the system view as wired — inventory, coverage, and
population, no canvas in v1.** A graph surface can return later as its own
spec, over an edge set the gate actually verifies.

**Q2 — Five screens, with the three levels as full views.**
Point 5's three levels (system → claim → evidence) are wired as three full
screens, plus the matrix view and the settling panel as first-class screens
under the same nav entry — five wireframes in all. The alternative (Spec
085's shape: levels as panels inside one explorer shell) compresses the
claim and evidence views into side panels, where the falsifier text, the
"this does not establish" line, and the register-record tables do not fit at
readable fidelity.
**Recommendation: adopt five screens.**

**Q3 — The header strip holds the spec's three items; falsifier coverage
lives on the system view.**
Point 5(b) names the header's contents exactly: claims by status,
validated-anchor share, nearest dated items. The falsifier-gap census
(831/840, printed by the gate on every run) is placed as a full-width line
on the system view rather than added to the strip, so the strip stays the
registered contract and the gate's V2/V6 header checks compare against
exactly three items.
**Recommendation: as wired.** Adding falsifier coverage to the strip is a
one-line design change if you want it there — but it should be decided
here, not at build time, because the gate checks the header against this
contract.

**Q4 — "Nearest dated items" are the dated study-outcome blocks; the 44
pending validations appear as a count.**
The ledger's own per-entry dates cannot serve: every claim entry is dated
2026-11-01 (the migration date), and only the 23 extracted claims carry an
as-of (October 2026). The genuinely dated things near the present are the
study-outcome blocks recorded in the source records and reached through the
matrix (Spec 054's governing append, 2026-10-25; Specs 074 and 052,
2026-10-24; and so on). The anchors register records no review dates for
the 44 pending validations, so they cannot be listed as dated items — the
strip shows them as a count with the reason.
**Recommendation: as wired.** If you want the pending validations dated,
that is a change to the anchors register's own record-keeping, separate
work from this spec.

**Q5 — Claim×sign is a row filter, not a matrix form.**
The task text for T501 names the matrix view's primary form as
claims×evidence with claim×sign as a column-class filter. The generated
matrix contains no claim×sign cells at all: identifier-based sign
references resolve to register records (evidence view), and prose sign
mentions are unresolved by design. What the wireframe implements is a
sign row-filter ("claims carrying sign_ref mahadevan:70" — today exactly 1
claim) plus the sign×sign block as a secondary form.
**Recommendation: as wired.** If a claim×sign grid is wanted as a form, it
would have to be a view over register records, not over matrix cells — say
so here and the wireframe changes.

**Q6 — The displayed-score slot is shown in its honest empty state.**
C086-16's displayed-score leg is carried into Stage 5 by the Stage 4
closeout: a displayed score must be an `aee/scoring.py` ScoringEngine
output over the ledger's relation set, labeled as such. Today's ledger
carries no AEE state on any of the 840 claims, so there is no score to
display. The claim view wires the block anyway, showing the empty state and
the labeling rule, rather than omitting the block until a score exists —
omitting it would hide both the gap and the rule.
**Recommendation: as wired.**

**Q7 — The settling panel opens on the stored T405 comparison.**
The panel's default state is the first stored interchangeability run pair —
incumbent vs full-register over the full frame — rather than empty run
controls. The comparison is the settling layer's headline result (0
conflicts under both candidates, 0 per-claim divergences, coverage deltas
stated), and opening on it makes the panel's labeling and divergence view
approvable on real content.
**Recommendation: as wired.**

**Q8 — The mahadevan:64/70/72 divergence is named on the evidence view
itself.**
Matrix-defs v1 and glossa-settle-1 resolve the same three sign references
differently (the matrix: to nothing; settling: to M064/M070/M072). The
evidence view names the divergence in a callout on the screen where a
reader meets it, rather than in a footnote or only in the stage record.
This question covers presentation only — the underlying definitions ruling
(matrix-defs v2, or a settle amendment) is already on your list separately
and is not decided by this package.
**Recommendation: named, as wired.**

---

## Decided upstream — not open questions

Recorded in `conformance.md` §4: Spec 085's Q1 (reports shown as graph
nodes) was reversed by the approved Spec 086 package (D-086-Q1: the layered
map is generated data, not an explorer over app entities); Spec 085's Q3
(constraint authorship in the UI) is superseded — the settling panel runs
registered scenarios and assignment sets and authors nothing; Spec 085's
four constraint kinds and its score-ceiling table belong to the
never-built projected-constraint engine and are superseded by
glossa-settle-1's rules and C086-16's score rule. None of these need an act
here; they are listed so the approval covers the whole surface knowingly.
