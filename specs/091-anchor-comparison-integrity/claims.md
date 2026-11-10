# Spec 091 — Claims

Every claim carries at least one falsifier (a concrete observation that
would show it false) and a "does not establish" line (the over-reading it
forbids), per the program's claims discipline. The same set, normalized
into `aee-claims.json` without substantive change, was validated under
the pinned AEE (1.5.3) before any build task starts (Stage 0, T002;
`records/t002-aee-assessment.json`). Grounding for every factual
statement below: `records/commission-and-grounding-2026-11-05.md`,
counted and read first-hand from the repo on 2026-11-05. The register
falsifiers of GR-088-01/02/03 are carried into the claims they govern —
verbatim where the claim is the register entry's own closure condition.

## W1 — The eligible set (GR-088-01)

**C091-1 — The locator pass is total over all 184 crosswalk entries.**
Every entry of the Mahadevan–Parpola crosswalk (v2.1, 184 entries)
carries, in the locator record this spec produces, an entry-level
primary-source locator for its reading fields (phonetic and semantic),
or a recorded locator-not-found outcome backed by a documented search
(sources consulted, in order, with dates). File-level citations of the
kind the staged crosswalk carries today do not satisfy this claim; the
locator names the entry's reading at its primary source. No entry is
left unexamined: the pass's census is 184 examined of 184.
*Falsifier:* an entry in the locator record with neither an entry-level
locator nor a documented not-found search; or a pass census below 184.
*Does not establish:* that any reading is correct, or that a located
reading is independent — location is provenance, not agreement; the
independence test is C091-2/C091-3.

**C091-2 — The independent coding is independent in fact.** The
readings used by the eligibility recomputation are coded from the
primary sources named by the locator record by a coder who did not
derive the project readings, under the blinding protocol filed before
coding starts (decision D-091-2: the coder sees the primary sources and
the sign list, never the project readings or the WP4 classifications,
until the coding is filed). The protocol, the coder's identity and
lineage exclusion, and any deviation are on record; a deviation voids
the coding it touches, which is then redone or the affected entries
fall back to their WP4 classes.
*Falsifier:* a coded reading whose coder is a member of the derivation
lineage; coding filed after recorded exposure to the project readings
or classifications; or an eligibility recomputation resting on coding
with no blinding protocol on record.
*Does not establish:* that the coder is right — only that their coding
is evidence independent of the project's derivation, which is the
property the eligibility class exists to certify.

**C091-3 — The eligible set is whatever the recomputation produces,
including zero.** Eligibility is recomputed mechanically from the
locator record and the independent coding under WP4's classification
rules (`crosswalk_provenance.py`'s rules, extended only by the new
versioned artifacts of D-091-3's pattern — never by editing the frozen
provenance file). The resulting count is reported as produced. Register
falsifier, carried verbatim: *the locator pass finds every entry's
reading traceable to the project's own derivation → the eligible count
stays 0 and the gap re-registers as structural (no independent Parpola
comparison exists to be had from this crosswalk), not as an unfinished
task.*
*Falsifier:* an eligibility count that differs from the mechanical
recomputation over the locator and coding records; or a structural
re-registration filed while at least one entry carries an independently
sourced reading under the recomputation.
*Does not establish:* that eligible entries' readings are correct —
eligibility certifies that a comparison *can* testify independently,
not what it testifies.

**C091-4 — Crosswalk agreement is citable only at its eligibility
class.** After W1's recomputation lands, no published layer of the
program (matrix, map, tracker, preprint prose) cites a "Parpola agrees"
relation as independent validation for an entry outside the eligible
set; every citation of crosswalk agreement carries the entry's
eligibility class. Before W1 lands, the standing class of every entry
is its WP4 class — under which no entry is eligible — and citations are
bound by that.
*Falsifier:* a published artifact, after the recomputation lands,
citing crosswalk agreement as independent support for an entry
classified project-derived, used-in-construction, unverified, or
ineligible; or a citation of crosswalk agreement carrying no class.
*Does not establish:* that eligible entries must be cited — only that
ineligible ones may not be cited as what they are not.

## W2 — Outside reproduction over the 46 (GR-088-02)

**C091-5 — Every one of the 46 internal-only strict anchors receives
its outside attempt.** The pass covers all 46 anchors named by the WP5
audit's `supported_internal_only` class, under a protocol recorded
before the pass starts: for each anchor, independent attestation or
blind re-derivation by readers who did not produce the original
derivations (decision D-091-1). Each anchor's outcome is recorded —
external line landed, external line attempted and not landed, or not
attempted with the reason — and the census is 46 accounted of 46.
*Falsifier:* one of the 46 with no recorded outcome; an attempt by a
reader inside the anchor's derivation lineage; or an outcome recorded
with no protocol on record.
*Does not establish:* that the 46 will move — the pass guarantees the
attempt and its record, not the result.

**C091-6 — An anchor leaves internal-only only when an external line
actually lands.** A per-anchor disposition changes from internal-only
to independently supported solely on a filed external support line (an
attestation, or a blind re-derivation that agrees, produced under
C091-5's protocol). Re-examination of same-lineage material, however
thorough, changes nothing. The program's independently supported count
is at all times exactly 6 (M044, M047, M124, M202, M329, M330) plus the
anchors with landed external lines. Register falsifier, carried in
substance: *an anchor whose only producible support after the pass
remains same-lineage stays internal-only and the count stands — the
find closes per-anchor only as external lines actually land.*
*Falsifier:* an anchor counted independently supported whose support
lines on record are all same-lineage; or a supported count that differs
from 6 + (anchors with filed external lines).
*Does not establish:* that an anchor with a landed external line is
correctly read — the line certifies independent support for the
standing, not the truth of the reading.

**C091-7 — Until external lines land, citations carry the internal-only
status.** From this spec's adoption onward, every published layer that
cites any of the 46 cites it as internal-only, and every statement of
the strict core's independently supported mass states the measured
number, not 94. This obligation binds from adoption, not from W2's
completion: the audit already established the classes, and the labels
only state them.
*Falsifier:* a published artifact, after adoption, citing any of the 46
as confirmed or independently supported, or stating the core's
independently supported mass as 94 (or as any number other than the
measured count of record).
*Does not establish:* that the 46 are wrong — internal-only is a
statement about where their support comes from, not about whether the
readings hold.

## W3 — Revalidation of the 37 (GR-088-03)

**C091-8 — The corrected Phase-48 battery contains no pass-by-default
path.** In the corrected battery (a new versioned battery, decision
D-091-4; the historical `phase48_medium_validation.py` is frozen),
every promotion credit is earned by an executed check over present
inputs. A missing input, an unexecuted check, or an inapplicable test
produces not-run or fail, never credit. The removed paths are
enumerated against the historical battery and the WP5 reconstruction
(the audit's credit census records, among the 30 promotions' credits,
two default-credit kinds: missing-model-character and too-short), and
each enumerated path has a fixture proving it now yields not-run/fail.
*Falsifier:* a corrected-battery run awarding credit for an absent
input, an unexecuted check, or a default branch — whether found in the
battery's code or in a run record; or an enumerated historical
pass-by-default path with no fixture proving its corrected behavior.
*Does not establish:* that the corrected battery's passes are correct
readings — only that its credits are earned by checks that ran.

**C091-9 — The 28 Phase-48 promotions follow the corrected run.** The
corrected battery is run over the 28 promotions standing at
requires-revalidation (the WP5 Phase-48 subset), as a run under
run-defs v1, cited by run id. Each promotion's disposition then follows
the run's recorded output: those the corrected battery promotes stand
promoted on the new evidence; the rest reclassify to the run's measured
disposition. The historical battery's output is retired as evidence for
all 28. Register falsifier, carried in substance: *the re-run promotes
a materially different set → the original promotions reclassify per the
new run, and the battery's historical output is retired as evidence.*
*Falsifier:* any of the 28 retaining a disposition sourced from the
historical battery after the corrected run is filed; a corrected-run
disposition not reflected in the anchor records; or a re-run executed
under the historical battery or an unversioned variant of it.
*Does not establish:* that the corrected run's promotions are
independently supported — battery promotion is an internal validation
event; the independence classes are W2's subject (and GR-088-02's
census is not changed by a battery outcome unless an external line also
lands).

**C091-10 — The 5 single-line anchors are revalidated on the corrected
checkers, and insufficiency moves them down, not back.** M042, M046,
M108 (rule R5b) and M176, M342 (rule R5c) are revalidated with the
repair brief's corrected checkers over every arm that can run without
GR-088-04's certification (the site-statistics lineage,
`site_stats_v2`). Each anchor's disposition follows its checker's
recorded output. Register falsifier, carried verbatim: *the v2 checkers
judge the support insufficient → the 5 move to insufficient evidence,
not back to supported.*
*Falsifier:* one of the 5 whose post-revalidation disposition is not
its corrected checker's recorded output; or one restored to a supported
class without a new support line on record.
*Does not establish:* a phonotactic verdict in either direction — the
phonotactic arm is C091-11's, and it does not run under uncertified
rules.

**C091-11 — The phonotactic arm is dependency-gated, never silently
dropped and never run uncertified.** For any of the 5 whose
revalidation requires the phonotactic checker (`phonotactics_v2`), that
arm waits for GR-088-04's linguist-certified rule set. Until it lands,
the affected anchors remain at requires-revalidation with the
GR-088-04 dependency named on their records; no phonotactic violation
count, in either direction, is produced for any anchor under the
uncertified rule set. GR-088-04 is a separate register entry: this spec
notes the dependency and does not absorb the linguist leg.
*Falsifier:* a phonotactic violation count stated for any anchor under
the uncertified rule set; or one of the 5 reclassified on a phonotactic
basis before certification; or one of the 5 left at
requires-revalidation after the site-statistics arm ran, without the
GR-088-04 dependency named where the phonotactic arm was required.
*Does not establish:* that the dependency will be supplied — if the
linguist leg never lands, the arm stays open and the register entry
says so (Stage 6 closeout names it).

**C091-12 — The 4 R5d anchors get an outside line or a structural
record.** M087, M165, M264, M311 — each resting solely on a crosswalk
or literature import — receive a documented sourcing attempt for an
independent support line outside the crosswalk lineage (an owner act
for the external engagement, D-091-1). Where an outside line lands,
the disposition follows it. Register falsifier, carried verbatim: *no
source outside the crosswalk lineage attests the readings → the 4 stay
requires-revalidation permanently, recorded as structural rather than
pending.*
*Falsifier:* one of the 4 reclassified as supported on crosswalk-lineage
material; or one left recorded as merely pending after a documented
sourcing attempt found no outside attestation.
*Does not establish:* that an outside attestation, where found, settles
the reading — it settles the support class, per the same rule as
C091-6.

## Cross-cutting — disposition discipline and boundaries

**C091-13 — Every disposition change is an append-only act in audit
v2; frozen records are never edited.** All status changes this spec
produces (W1's eligibility classes, W2's support classes, W3's
revalidation dispositions) land as recorded reclassification acts and
in a new versioned anchor-support audit (audit v2, decision D-091-3)
whose generator and inputs are named. The WP5 audit JSON, the WP4
provenance JSON, the historical Phase-48 battery and its output, and
the original crosswalk file are never edited by any stage.
*Falsifier:* a byte change in any frozen record attributable to this
spec; or a disposition change in audit v2 with no corresponding
recorded act and named generator inputs.
*Does not establish:* that audit v2's dispositions are right — only
that every one of them is traceable to an act and an execution, and the
record it supersedes survives intact.

**C091-14 — The register entries close only on their falsifiers'
terms.** At each workstream's end, its register entry (GR-088-01,
GR-088-02, GR-088-03) is amended — append-only, per the register's own
discipline — to its measured end state: closed (its candidate executed
and its closure condition met on the records), re-registered structural
(its falsifier's structural outcome produced), or still open with the
blocking fact named (a dependency ungated, an owner act outstanding).
This spec's completion alone closes no entry.
*Falsifier:* a register entry marked closed whose workstream's closure
condition is unmet on the records; or a workstream at its end with its
register entry unamended.
*Does not establish:* that a closed entry's subject is settled forever
— closure states that the named gap was answered as specified, under
the records as they stand.

**C091-15 — Nothing in this spec is a decipherment result.** No stage
changes any anchor's proposed reading, any claim's verdict in the
ledger, or the program's standing position that the Indus script is not
deciphered. The only quantities that move are support classes,
eligibility classes, and validation statuses. A stage artifact that
altered a reading or a verdict would be a scope violation, not a
result, and is withdrawn on discovery.
*Falsifier:* a stage artifact of this spec that alters a proposed
reading or a ledger claim verdict, or prose in a record of record
presenting a support-class or eligibility change as a reading
confirmation.
*Does not establish:* anything about the readings themselves — this
spec is evidence-chain repair, and its strongest possible outcome is
that the program's support statements become exactly as strong as
their evidence, no stronger.
