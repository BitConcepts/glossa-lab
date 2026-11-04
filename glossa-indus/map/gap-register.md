# Gap register v1 — the full picture's missing pieces

Consolidated 2026-11-04 (Spec 088, Stage S6) from the
three Stage S5 cluster scans, executed the same day on
the generated program map (ledger 907 lines, canonical
SHA-256 `9f8144c3…`; program-map coverage: 876 claims,
89 studies):

- Cluster A — corpus + anchors:
  `specs/088-full-picture-map-gap-register/records/scan-corpus-anchors.md`
- Cluster B — claim families + contact zone:
  `specs/088-full-picture-map-gap-register/records/scan-families-contact.md`
- Cluster C — infrastructure + bookkeeping:
  `specs/088-full-picture-map-gap-register/records/scan-infra-bookkeeping.md`

Each entry names a missing NODE or a missing EDGE (or,
for the bookkeeping kinds, the record whose absence
leaves the picture stale), why its absence blocks
convergence, and the candidate that would fill it, with
its falsifier and its honesty-rule type (C088-12:
in-house re-derivation and independent confirmation
are different types, and neither is recorded as the
other; a candidate that only re-derives in-house never
closes an outside-reproduction gap). Scan-local ids
(A-NN / B-NN / C-NN) are cited on every entry so each
traces to its evidence. One entry (GR-088-26) is
sourced not from a scan but from the Spec 086 Stage 5
record, added at consolidation because the T602
completeness check maps it from C088-11's named
source lists; its provenance is stated on its face.

This register proposes; nothing here is commissioned
until ratified (T603). Verdicts and standings are the
ledger's, not this document's. No claim's status,
stage, or score was changed by this register or by
the scans behind it.

Status words (the plan's vocabulary): UNSTATED (the
missing record does not exist), UNMEASURED (the study
or check that would settle it has not run), UNJUDGED
(work exists but no verdict can be taken, or the
verdict is pending), UNCONNECTED (both sides exist;
the relation between them was never built or tested),
DATA-BLOCKED (the input dataset does not exist in
program hands), TIME-SENSITIVE (a window closes).
Applied to the gap's own state, in that plain sense.
No entry in v1 is TIME-SENSITIVE. GR-088-37 carries
no status word: it is a find carried under a standing
owner restriction, not a gap.

Kinds (the four registered kinds of C088-10, counted
in the census at the close of this document): missing
node, missing edge, thin evidence, stale bookkeeping.

## The headline list (consolidation ranking across domains)

Ranking is the consolidation's judgment; it settles
only at the owner's ratification (T603).

1. GR-088-01 WP4: of 184 Parpola comparisons, zero are
   eligible as independent validation — the program's
   flagship outside-reproduction hole.
2. GR-088-02 46 of the 94 strict anchors rest on
   internal-only support; the independently supported
   mass of the strict core is 6, not 94.
3. GR-088-03 37 strict anchors require revalidation,
   including 28 of the 30 Phase-48 promotions.
4. GR-088-04 WP2: the phonotactic certification leg
   (a linguist-reviewed rule set) was never supplied,
   so no corrected violation count exists.
5. GR-088-05 GAP-C07: the claim lifecycle machine is
   not storage-enforced, and the cross-cutting spec
   it calls for was never written.
6. GR-088-06 The 44 pending readings have no
   adjudication route; the instrument line is closed
   by the owner's own OD-1.
7. GR-088-07 No claim bears a recorded relation to
   any anchor: 287 anchor columns, zero anchor cells.
8. GR-088-08 The Holdat positional corpus exists as
   profiles, not as a keyed, citable dataset
   (DATA-BLOCKED; it also gates GR-088-09).
9. GR-088-09 WP3: the corrected site-statistics
   re-evaluation was never run.
10. GR-088-10 The contact-zone sequence study is
    gated on a CISI Vol. 3 transcription that does
    not exist (DATA-BLOCKED, owner-gated).

Entries 11–36 follow in the register body in ranked
order. GR-088-37 is unranked by design (carried find,
owner restriction).

## Register entries

GR-088-01. WP4: NO ELIGIBLE INDEPENDENT PARPOLA
COMPARISON (Claim families). UNCONNECTED.
Kind: missing edge. Scan source: B-01
(`records/scan-families-contact.md`).
**Missing piece:** a single comparison, of the 184 in
the Mahadevan–Parpola crosswalk, whose reading is
independently sourced. The provenance classification
is total: 0 eligible; 116 entries carry the project's
own readings copied under a "Parpola 1994" source
label (the Phase-96 mechanism); per-entry
primary-source locators have never been recorded.
**Why its absence blocks convergence:** every
"Parpola agrees" relation in the lineage is circular
— it shares the derivation it would confirm — so the
edge from the anchor claims to the field's standard
comparator carries no weight. This is the honesty
rule's standing instance (C088-12).
**Candidate:** build the eligible set — entry-level
primary-source locators for all 184 entries, and
independent coding of the readings from those primary
sources by a coder who did not derive the project
readings.
**Falsifier:** the locator pass finds every entry's
reading traceable to the project's own derivation →
the eligible count stays 0 and the gap re-registers
as structural (no independent Parpola comparison
exists to be had from this crosswalk), not as an
unfinished task.
**Type:** independent confirmation.
**Owner gates:** the locator pass is in-house work,
but its product counts as independent only if the
coding is independent — an outside coder is an owner
act. The register must not mistake the pass for the
confirmation.

GR-088-02. 46 STRICT ANCHORS REST ON INTERNAL-ONLY
SUPPORT (Anchors & readings). UNMEASURED.
Kind: thin evidence. Scan source: A-05
(`records/scan-corpus-anchors.md`).
**Missing piece:** for 46 strict anchors, any support
line originating outside the program's own derivation
lineage (audit derivation categories for the 46:
GRAMMAR 20 / DEDR 17 / ICONOGRAPHIC 4 / MIXED 2 /
CROSSWALK_CORPUS 2 / LITERATURE 1 — every line
produced inside this program).
**Why its absence blocks convergence:** under the
honesty rule these standings cannot be cited as
confirmed. The strict core's independently supported
mass is 6 (M044, M047, M124, M202, M329, M330), not
94, and every downstream claim inheriting anchor
support inherits the thinness.
**Candidate:** an outside-reproduction pass over the
46 — independent attestation, or blind re-derivation
by readers who did not produce the original
derivations.
**Falsifier:** an anchor whose only producible
support after the pass remains same-lineage stays
internal-only and the count stands — the find closes
per-anchor only as external lines actually land.
**Type:** independent confirmation.
**Owner gates:** external readers are an owner act
(named humans; the program's contact rules apply).

GR-088-03. 37 STRICT ANCHORS REQUIRE REVALIDATION
(Anchors & readings). UNMEASURED.
Kind: thin evidence. Scan source: A-06
(`records/scan-corpus-anchors.md`).
**Missing piece:** a validation that survives the
repair brief's findings, for 37 anchors, routed from
the audit's own fields: 28 Phase-48 promotions (the
promoting battery carried four pass-by-default paths
and promoted 30 of 30 tested); 5 resting on a single
line (M042, M046, M108 under rule R5b; M176, M342
under R5c); 4 resting solely on a crosswalk/literature
import (R5d: M087, M165, M264, M311).
**Why its absence blocks convergence:** 37 of the 94
strict anchors — including 28 of the 30 Phase-48
promotions (the remaining 2 are GR-088-27's pair;
none of the 30 is supported in any class) — hold a
status the program's own audit says it cannot
currently defend. Until they are revalidated or fall,
the strict core's size is nominal.
**Candidate 1 (the 28):** corrected Phase-48 battery
re-run over the 28, with the pass-by-default paths
removed.
**Falsifier:** the re-run promotes a materially
different set → the original promotions reclassify
per the new run, and the battery's historical output
is retired as evidence.
**Type:** in-house re-derivation.
**Owner gates:** none.
**Candidate 2 (the 5):** corrected-checker
revalidation of the 5 single-line anchors
(phonotactics_v2 / site_stats_v2 lineage).
**Falsifier:** the v2 checkers judge the support
insufficient → the 5 move to insufficient evidence,
not back to supported.
**Type:** in-house re-derivation.
**Owner gates:** gated on GR-088-04's linguist leg
for the phonotactic arm.
**Candidate 3 (the 4):** an independent support line
for the 4 R5d anchors, sourced outside the crosswalk
lineage.
**Falsifier:** no source outside the crosswalk
lineage attests the readings → the 4 stay
requires-revalidation permanently, recorded as
structural rather than pending.
**Type:** independent confirmation.
**Owner gates:** external sourcing is an owner act.

GR-088-04. WP2: THE PHONOTACTIC CERTIFICATION LEG
WAS NEVER SUPPLIED (Claim families). UNMEASURED.
Kind: thin evidence. Scan source: B-02
(`records/scan-families-contact.md`).
**Missing piece:** the linguist-reviewed rule set,
and with it the corrected re-run. The corrected
checker exists (`phonotactics_v2`); what does not
exist is (a) the linguist's establishment of which
restrictions belong to the proposed historical
language vs later Tamil, and (b) any certified run of
the corrected checker over the dependent population.
The "zero violations" quantity was withdrawn, not
replaced; the overlay holds the dependent claims at
`invalid_method`.
**Why its absence blocks convergence:** every claim
whose support passes through the Phase-58 checker
lineage — including GR-088-03's candidate 2 — stands
on an uncertified arm. The program cannot state a
phonotactic violation count in either direction.
**Candidate:** linguist certification of the rule
set, then the v2 re-run over the strict core and the
dependent claims.
**Falsifier:** under certified rules the v2 checker
returns violations > 0 for the strict core → the
dependent claims reclassify downward and the
thinness converts to measured contradiction for the
affected family; a zero count under certified rules
is what closes it.
**Type:** in-house re-derivation (the closing study
is the program's own re-run; its gating input is
external — typed by the study, not the input).
**Owner gates:** the linguist engagement is an owner
act (a named human; DATA-BLOCKED in the repair
brief's terms until supplied).

GR-088-05. GAP-C07: THE LIFECYCLE STATE MACHINE IS
NOT STORAGE-ENFORCED (Program infrastructure).
UNSTATED.
Kind: missing node. Scan source: C-01
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** the cross-cutting spec the gap
record itself calls for. The gated transitions are
sound, but no API endpoint or file writer is forced
through them: claim/anchor records are plain JSON and
other writers set `stage` / `review_status` /
`confidence` directly. Closing it "needs its own spec
so each writer's legitimate transitions are enumerated
rather than guessed" — that spec does not exist.
**Why its absence blocks convergence:** the ledger's
lifecycle guarantees hold only where writers
cooperate. Every generated surface downstream —
matrix, maps, this program's standings — derives from
fields no storage layer protects, so the whole chain's
integrity rests on writer discipline rather than
enforcement.
**Candidate:** the GAP-C07 spec — a writer census,
then routing every writer through the gated
transitions or adding storage-layer validation.
**Falsifier:** the writer census shows every current
writer already routes through the gated transitions →
the gap closes as already-enforced and only the census
record is new.
**Type:** in-house re-derivation.
**Owner gates:** the spec is a cross-cutting act
(block approval like any spec); the gap record names
the backend maintainer as its owner.

GR-088-06. THE 44 PENDING READINGS HAVE NO
ADJUDICATION ROUTE (Anchors & readings). UNJUDGED.
Kind: missing node. Scan source: A-11
(`records/scan-corpus-anchors.md`).
**Missing piece:** any validated route — instrument
or panel — that may score the 44 pending anchor
readings. The Step 0-G instrument line closed by
owner decision OD-1 (2026-10-28) after its final run
("M4 remains GATED — DRAFT ONLY, permanently under
its current gate. The 44 pending readings remain
pending indefinitely, carrying no weight"). Phase-120
gave them a descriptive triage (Bhaskar 2024), not an
adjudication.
**Why its absence blocks convergence:** 44 candidate
readings — against 287 recorded anchors and a strict
core of 94 — sit outside every verdict. The core can
neither grow from them nor formally exclude them, and
"pending" has no exit condition on any current record.
**Candidate:** an expert adjudication panel for the
44 on the M222 pattern (GR-088-14) — the instrument
route is closed by the owner's own decision, so the
panel is the route that does not require reopening it.
**Falsifier:** the panel's agreement on a
planted-control subset falls below the registered bar
→ the panel route closes too, and the 44 stay pending
by a second, independent failure.
**Type:** independent confirmation.
**Owner gates:** OWNER — OD-1 was his decision; any
route (panel, or a new instrument design) opens only
on his act.

GR-088-07. NO CLAIM BEARS A RECORDED RELATION TO ANY
ANCHOR (Anchors & readings). UNCONNECTED.
Kind: missing edge. Scan source: A-04
(`records/scan-corpus-anchors.md`).
**Missing piece:** claim→anchor edges. The matrix
carries 287 anchor columns and zero anchor cells
(counted from the current `matrix.json`); under
matrix-defs v1 anchors contribute no cells, so the
relation was never built. On the claim side, 14 sign
mentions in claim text resolve to no sign identity,
so those mentions cannot become edges either.
**Why its absence blocks convergence:** which claims
stand on which anchors is the most decision-relevant
relation in a decipherment program — it is the blast
radius of every anchor verdict in GR-088-02 and
GR-088-03 — and it is absent from the evidence graph.
**Candidate:** an edge-construction study under a
matrix-defs amendment, building anchor cells from
structured sign references and the WP5 trails.
**Falsifier:** the construction pass finds structured
sign references on too few claims to populate the
relation (today exactly 1 claim carries sign_refs) →
the find converts to a missing-node find (structured
sign-mention extraction, GR-088-11's candidate)
rather than closing.
**Type:** in-house re-derivation.
**Owner gates:** a matrix-defs amendment is a program
act under Spec 086's amendment discipline.

GR-088-08. THE HOLDAT POSITIONAL CORPUS IS NOT A
KEYED DATASET (Sign inventory & corpus). DATA-BLOCKED.
Kind: missing node. Scan source: A-12
(`records/scan-corpus-anchors.md`).
**Missing piece:** the Holdat dataset itself in
keyed, pinned, citable form — a corpus node. The
adoption record names "WP3 Holdat CSV + GPU
environment" as blocked legs; Specs 015/019 studied
the Holdat–ICIT disagreement from positional profiles,
and the cross-compilation line has only ever
adjudicated profiles. (The scan cited the block on
the adoption record's authority and did not
independently establish which artifact is absent;
this entry carries that provenance on its face.)
**Why its absence blocks convergence:** two legs wait
on it — GR-088-09's re-evaluation and any ground-truth
check of the profile disagreement (GR-088-16). A
disagreement between profiles of a corpus nobody can
cite cannot be settled at the level of the corpus.
**Candidate:** acquisition and keying of the Holdat
corpus with a pin, under the program's corpus
discipline.
**Falsifier:** keyed and pinned, the corpus reproduces
the 015/019 profile disagreement identically → the
disagreement lives in profile construction, not the
data; this find closes as not-the-blocker and
GR-088-09's block stands on the GPU environment alone.
**Type:** in-house re-derivation.
**Owner gates:** lawful access to the dataset, if it
is not already in program hands, is an owner matter.

GR-088-09. WP3: THE CORRECTED SITE-STATISTICS
RE-EVALUATION WAS NEVER RUN (Claim families).
UNMEASURED.
Kind: thin evidence. Scan source: B-03
(`records/scan-families-contact.md`).
**Missing piece:** the re-evaluation of the
site-statistics population under the corrected
implementation. The Phase-69 routine could emit only
p ∈ {0.0, 0.5, 1.0}; `site_stats_v2` exists with a real
p-value and reference values on record. No equivalence
design exists (no prespecified margin), the invariance
language was contained rather than established, and
current displays hide the insufficient-data remainder
— 29 of 94 strict, 81 of 171 full — outside the tested
denominator.
**Why its absence blocks convergence:** the site-effect
family of standings (the "no site effect" line that
Specs 028/040/060 work in) rests on outputs the staged
routine cannot reproduce. Nobody can say which
historical site verdicts survive correction, so the
family can neither be relied on nor retired.
**Candidate:** the corrected re-evaluation over the
full population — remainder inside the denominator —
with the equivalence margin prespecified before
outcomes are seen.
**Falsifier:** v2 disagrees with the historical outputs
beyond the declared tolerance on the reference tables →
the historical site verdicts reclassify wholesale, and
the find converts from thin evidence to contradicted
for the affected family.
**Type:** in-house re-derivation.
**Owner gates:** the full-population arm waits on
GR-088-08's Holdat leg and a GPU environment (program
infrastructure; the Syncyard/desktop route is the
program's own act).

GR-088-10. THE CONTACT-ZONE SEQUENCE STUDY IS GATED
ON A TRANSCRIPTION THAT DOES NOT EXIST (Contact zone
& external corpora). DATA-BLOCKED.
Kind: missing node. Scan source: B-09
(`records/scan-families-contact.md`).
**Missing piece:** a transcription of the CISI
Vol. 3 inscription material — the sign sequences of
the Gulf inscribed material, with per-sequence
provenance — lawfully accessible under the program's
restricted-material custody. The WP9 preparation names
it "the precise missing dependency," records the stop
rule ("no further sequence-leg work until the CISI
Vol. 3 transcription exists and is lawfully
accessible"), and carries the design condition that
any future freeze must name the wider Dilmun corpus
(approximately 800 seals) as its held-out arm or state
why its design does not need one.
**Why its absence blocks convergence:** the sequence
leg is the contact zone's only discriminating test —
sequence-level comparison of the Gulf INDUS material
against the Indus corpus. Until the transcription
exists the study cannot be frozen, let alone run, and
Domain 4's thinness cannot change.
**Candidate:** produce the transcription under the
custody arrangement the program already uses for
restricted material, pinned as the study's input.
**Falsifier:** the transcription is produced and
pinned → the gate lifts and the find closes at the
study's freeze; if lawful access is refused on the
record, the leg dispositions as abandoned-by-access
and the find closes as a recorded dead end instead.
**Type:** in-house re-derivation (the work product is
the program's own transcription of an external corpus).
**Owner gates:** OWNER-GATED — CISI material is
restricted (statistics publishable; scans never
redistributed; custody on the owner's machines). The
access route is the owner's; no agent route exists.

GR-088-11. THE TWO-GRAPH-WORLDS JOIN HAS POPULATION
ONE (Program infrastructure). UNCONNECTED.
Kind: missing edge. Scan source: C-05
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** identifier linkage between claim
text and the sign register at population scale.
Exactly one claim of 876 carries sign_refs that
resolve (one `sign_refs` occurrence in the current
matrix artifact; the population did not grow with the
ledger). The friction surface, from the same coverage
block: 14 unresolved sign mentions and 3 sign_refs
with no anchor record under the matrix key
(GR-088-28).
**Why its absence blocks convergence:** claims and
signs are the program's two graph worlds; joined at
one claim, every cross-world question (which claims
does this sign's verdict touch — GR-088-07 from the
other side) is unanswerable from the generated layers.
**Candidate:** a sign-mention extraction pass minting
structured sign_refs from claim text under a
registered rule.
**Falsifier:** the pass over all 876 claims finds
structured mentions on only the same single claim →
the join is population-one because the claims
genuinely do not name signs in extractable form, and
the find re-registers as a property of the claim
corpus, not a missing build.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-12. NO STRICT ANCHOR RECORD STATES A FALSIFIER
(Anchors & readings). UNSTATED.
Kind: thin evidence. Scan source: A-09
(`records/scan-corpus-anchors.md`).
**Missing piece:** per-anchor falsifiers. Counted from
the audit's records by the scan: all 94 strict records
carry `falsifier: "no falsifier recorded"` and
`distinguishing_observation: "not recorded"` (94/94,
both fields). The ledger's claims are
falsifier-complete for the bundle population (853/853)
— the absence is at the anchor-record level, a
different instrument (WP5 element 5.5, unexecuted at
this completeness).
**Why its absence blocks convergence:** an anchor whose
record states no observation that would distinguish its
reading from the runner-up alternative cannot be
falsified as held; GR-088-02's and GR-088-03's
revalidations have no per-anchor test to run against.
**Candidate:** falsifier backfill per anchor from its
derivation trail (the distinguishing observation the
trail's own tests imply), executed as WP5 element 5.5
at record level.
**Falsifier:** an anchor whose trail contains no
distinguishing observation even in prose is recorded as
unfalsifiable-as-held and routed to GR-088-14's and
GR-088-27's dispositions — the backfill claim fails for
it on its own record.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-13. DOMAIN 2'S THIRTEEN STUDIES CARRY NO LEDGER
CLAIMS (Anchors & readings). UNJUDGED.
Kind: stale bookkeeping. Scan source: A-01
(`records/scan-corpus-anchors.md`).
**Missing piece:** claims bundles for the anchor
provenance and validation era:
`004-indus-executable-package`, `005-phase52-v2`,
`006-anchor-provenance-audit`,
`007-phase109-follow-through`, `008-m222-adjudication`,
`009-phase111-blind-affiliation`,
`010-phase112-blind-affiliation`,
`011-phase113-nonsa44-validation`,
`012-phase113-blind-affiliation`,
`014-phase115-nonsa44-validation-v2`,
`016-phase117-within-compilation-validation`,
`017-phase118-within-compilation-validation-v2`,
`018-phase119-pred2026-readiness` — all class unjudged;
their standings exist only in phase records and prose.
Consumes 13 `bundle_less_study` finds.
**Why its absence blocks convergence:** the anchor layer
is the program's core evidence, and its entire
validation era (Phases 111–119, the batteries the
SA-lineage anchors were tested by) is invisible to the
ledger → matrix → map chain. No generated surface can
weigh it; WP5 had to audit the anchors from trails
outside the ledger (GR-088-19).
**Candidate:** bundle backfill — extract claims bundles
for the 13 studies from their phase records through the
sanctioned ledger intake.
**Falsifier:** a study whose phase record contains no
falsifiable claim-shaped statements (pure battery run
logs) dispositions as pre-ledger history instead of
receiving a bundle — the backfill claim fails for that
study on its own record.
**Type:** in-house re-derivation.
**Owner gates:** none for the intake (the program's own
act); per-study dispositions settle at this register's
ratification (T603).

GR-088-14. THREE STRICT ANCHORS AWAIT EXPERT
ADJUDICATION — M222, M362, M398 (Anchors & readings).
UNJUDGED.
Kind: thin evidence. Scan source: A-07
(`records/scan-corpus-anchors.md`).
**Missing piece:** expert adjudication verdicts for
M222, M362, M398. M222's adjudication study exists
(`008-m222-adjudication`) but is itself bundle-less
(GR-088-13), so even its partial record is outside the
ledger.
**Why its absence blocks convergence:** the audit's
acceptance rule marks expert adjudication pending where
required — never forced complete. Three anchors sit in
that pending state with no verdict and no schedule.
**Candidate:** complete the expert adjudications on the
M222 pattern (named expert, registered protocol).
**Falsifier:** an expert returns "cannot adjudicate on
this evidence" → the anchor moves to insufficient
evidence, closing the pending state honestly rather than
by default.
**Type:** independent confirmation.
**Owner gates:** owner act (named experts; contact
rules).

GR-088-15. THE DESKTOP HOST RUNS A 2026-10-31 CHECKOUT,
118 COMMITS BEHIND MAIN (Program infrastructure).
UNMEASURED.
Kind: stale bookkeeping. Scan source: C-08
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** the Spec 083-sequence sync of the
desktop checkout to main, with its post-sync battery.
The repo's own record: the desktop checkout was settled
from `124a1ac3` to `309ea63c` on 2026-10-31 (T020
acceptance) and no later settle is recorded. Precision
the scan adds, and this entry carries in corrected form:
`309ea63c` is PR #472's merge commit and **is** in main's
history — the GitHub compare read by the scan shows main
118 commits ahead of it, 0 behind. It is the desktop
**checkout** that stands still, so every Spec 087/088-era
backend change is absent from the served host. (The
count is as of the S4 merge `893a426a`; it grows with
every later merge until the sync runs.)
**Why its absence blocks convergence:** the production
Glossa backend — the one the MCP tools and the cloud
edition are being built on — serves an October 31
snapshot while the ledger's home repo has moved through
two specs. Any behavior verified in the repo is not
thereby behavior of the served system.
**Candidate:** execute the sync through the Syncyard
gatekeeper (windowless, owner's profile) with the host
battery re-run, as the Spec 083 sequence prescribes.
**Falsifier:** a gatekeeper read shows the desktop
checkout already at a descendant of current main with
the battery green → the find is closed and only this
record was stale.
**Type:** in-house re-derivation.
**Owner gates:** the sync belongs to the Spec 083
sequence (adoption record §4); desktop execution runs
through the gatekeeper only.

GR-088-16. THE CROSS-COMPILATION ATTRIBUTION LINE'S
EARLY LEGS ARE UNLEDGERED (Sign inventory & corpus).
UNCONNECTED.
Kind: missing edge. Scan source: A-03
(`records/scan-corpus-anchors.md`).
**Missing piece:** the claim-level edge from the
Phase-125/127 disagreement result to its attribution
successors. Studies `019-phase125-cross-compilation-positional`,
`021-phase127-cross-compilation-diagnostic`, and
`022-phase131-attribution` (the diagnostic legs) carry
no claims (GR-088-20), while `034-matched-object-attribution`
and `058-transcription-disagreement-mechanism` carry the
attribution forward with bundles. The successor relation
exists in titles and prose only; at claim level there is
nothing for an edge to attach to.
**Why its absence blocks convergence:** the program's
central corpus disagreement — why the Holdat and ICIT
positional profiles disagree — has its evidentiary root
outside the generated graph. A reader of the map cannot
trace what the attributions attribute.
**Candidate:** the GR-088-20 backfill for `019`,
`021-phase127`, `022`, sequenced first — it creates the
nodes this edge needs, in the disagreement result's own
terms.
**Falsifier:** extraction shows the phase records' stated
result contradicts the premise `034` attributes (a different
disagreement mechanism) → the edge is recorded as contested,
not supportive, and the attribution line re-opens.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-17. THE COMPLETED LAURSEN CATALOG LEG HAS NO
LEDGER CLAIMS (Contact zone & external corpora).
UNSTATED.
Kind: missing node. Scan source: B-10
(`records/scan-families-contact.md`).
**Missing piece:** an extraction bundle carrying the
catalog leg's claims. The leg is complete and verified
on its record: the Laursen 2010 Table 1 catalog in
program hands is 121 seals = 92 Gulf Type + 28 Gulf
INDUS + 1 Gulf Linear-Elamite, across 29 named sites.
But the scan's count over `claims.jsonl` finds zero
entries mentioning laursen, gulf, dilmun, janabiyah, or
arabia — the program's one completed contact-zone
measurement exists only in preparation and goal-workspace
records.
**Why its absence blocks convergence:** the catalog leg is
the contact zone's strongest completed result (its negative
bearing on contact-mechanism claims is the line's current
standing). Unledgered, it cannot be cited by the matrix,
weighed by the map, or inherited by any successor study.
**Candidate:** extraction of the catalog leg into the
ledger through the sanctioned intake, from the completed
rebuild record.
**Falsifier:** the extracted claims fail the research-check
reproduction of the catalog counts (121 = 92 + 28 + 1 across
29 sites) → the bundle is rejected and the catalog leg's
standing re-opens instead of entering.
**Type:** in-house re-derivation.
**Owner gates:** none (the intake is the program's own act;
the underlying catalog is published literature).

GR-088-18. CLAIM×CLAIM DEPENDENCY PAIRS ARE COVERAGE
DATA, NOT EDGES (Program infrastructure). UNCONNECTED.
Kind: missing edge. Scan source: C-04
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** typed claim→claim edges. The current
matrix coverage counts `dependency_pairs_not_cells: 793`
(790 at Spec 086 Stage 5; +3 from the C088 intake's own
pairs) — pairs carried in evidence_refs and expressly not
cells under matrix-defs v1; and extracted claims carry no
`depends_on` / `conflicts_with` fields for the AEE graph
at all.
**Why its absence blocks convergence:** the map cannot show
that one claim's fall takes others with it. Digestion order
and blast radius — the two things a claims program most
needs from its graph — are invisible in the layer built to
show them.
**Candidate:** a dependency-edge promotion study — promote
the recorded pairs to typed edges under a matrix-defs
amendment, or record why they must stay coverage data.
**Falsifier:** the promotion analysis shows the pairs
duplicate existing claim→evidence edges claim-for-claim →
not-a-gap disposition, with the analysis as the record.
**Type:** in-house re-derivation.
**Owner gates:** a matrix-defs amendment is a program act
under Spec 086's discipline.

GR-088-19. 52 OF 94 STRICT-ANCHOR TRAILS NEVER CITE THE
LEDGER (Anchors & readings). UNCONNECTED.
Kind: missing edge. Scan source: A-10
(`records/scan-corpus-anchors.md`).
**Missing piece:** trail→ledger citation edges. The audit's
summary counts `records_with_no_ledger_passage_in_trail: 52`
— for over half the strict core, the provenance trail records
no ledger passage the standing rests on.
**Why its absence blocks convergence:** the anchor layer's
provenance and the claim layer's record do not meet. A reader
cannot walk from an anchor's standing to the ledger entry that
carries it, which is why GR-088-13's era had to be audited
from trails at all.
**Candidate:** a trail completion pass over the Phase-108
register trails, adding the ledger passage citation where the
passage exists.
**Falsifier:** a trail whose underlying passage does not exist
in the ledger corpus → that anchor's standing is recorded as
resting on an uncitable passage (a worse, named state), not
silently passed over.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-20. DOMAIN 1'S SEVEN BUNDLE-LESS STUDIES (Sign
inventory & corpus). UNJUDGED.
Kind: stale bookkeeping. Scan source: A-02
(`records/scan-corpus-anchors.md`).
**Missing piece:** claims bundles for
`015-phase116-corpus-harmonization`,
`019-phase125-cross-compilation-positional`,
`020-soviet-pred-adjudication`,
`021-phase127-cross-compilation-diagnostic`,
`021-phase130-intake-pack`, `022-phase131-attribution`,
`023-keyed-transcription-layer` — all unjudged, all
concentrated in the cross-compilation line and the keyed
transcription build. Consumes 7 `bundle_less_study` finds.
**Why its absence blocks convergence:** Domain 1's other ten
studies carry 125 claims; the seven without bundles include
the corpus-harmonization study and the transcription layer
the later corpus work stands on, so the corpus's own
foundations are the part of the domain the picture cannot
weigh.
**Candidate:** bundle backfill from the phase records, as
GR-088-13.
**Falsifier:** as GR-088-13 — a record with no claim-shaped
statements dispositions as pre-ledger history, not backfill.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-21. NINE EXTRACTED CLAIMS CARRY NO FALSIFIER (Claim
families). UNSTATED.
Kind: thin evidence. Scan source: B-05
(`records/scan-families-contact.md`).
**Missing piece:** a falsifier — or a recorded disposition —
for each of the 9 claims enumerated in the find list:
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`,
`…_sign_val_0002`, `…_sign_val_0003`,
`ancient_writing_and_modern_technologies_51831ac9_statisti_0004`,
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001`,
`…_critique_0002`,
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001`,
`…_sign_val_0002`,
`without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001`.
Falsifier coverage stands at 867/876 with the extracted
population at 14/23; the bundle population is complete
(853/853). Per the scan plan this is a disposition item, not
a measurement item. Consumes all 9 `extracted_null_falsifier`
finds.
**Why its absence blocks convergence:** a claim with no
falsifier cannot move by evidence in either direction; nine of
the program's 23 literature claims are structurally stuck at
their extraction standings.
**Candidate:** falsifier backfill by re-derivation from each
claim's source document, claim by claim.
**Falsifier:** a claim whose source text states no observation
that would count against it → backfill is impossible for that
claim; it remains a counted null by disposition, and the find
closes only when all 9 are filled or dispositioned.
**Type:** in-house re-derivation.
**Owner gates:** the accept-and-record disposition, where
backfill fails, is an owner act at ratification (T603).

GR-088-22. GAP-C13: BUNDLE-LESS DIRECTORIES AND THE
UNDISTINGUISHED FALSIFIER CASES (Program infrastructure).
UNSTATED.
Kind: stale bookkeeping. Scan source: C-03
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** a one-line disposition per listed spec
(no-claims / claims-elsewhere / falsifier-required). Two
instruments, recorded separately because they measure
different things: (i) today's tree — 28 bundle-less
directories in the find list, of which Domain 5's six are this
entry's own cluster (`001-glossa-lab-baseline`,
`002-gdelt-ngrams-and-frontier-methods`,
`003-mcp-and-test-gaps`, `025-paper-search-research-check`,
`025-stage2-controlled-followup`, `026-core-research-source`;
the other 22 are carried by GR-088-13, GR-088-20, GR-088-31,
GR-088-33); (ii) the audit-era instrument — at the 2026-10-29
scan of specs 001–081, 31 specs had no `claims.json` at all and
27 specs' `spec.md` never mentions a falsifier, with the
register unable to distinguish "no governed claims" from
"governed claims with no falsifier."
**Why its absence blocks convergence:** the program cannot
tell, for a third of its historical spec range, whether silence
means "nothing governed here" or "governed claims nobody gave a
falsifier to." Every completeness claim this register makes
inherits that ambiguity until the sweep runs.
**Candidate:** the disposition sweep over the audit list,
reconciled against today's bundle census — one line per spec,
recorded against it.
**Falsifier:** a listed spec is found holding governed claims
that lack falsifiers → it exits the sweep as a falsifier-backfill
find, and the "bookkeeping only" framing fails for it.
**Type:** in-house re-derivation.
**Owner gates:** spec authors for their specs; the program owner
for the sweep and any constitution-level rule it proposes (per
the gap record).

GR-088-23. THREE EXTRACTED DOCUMENTS HAVE NO TESTING LINE
(Claim families). UNSTATED.
Kind: missing node. Scan source: B-04
(`records/scan-families-contact.md`).
**Missing piece:** a study line that takes up the claims of
`ancient_writing_and_modern_technologies` (4 claims),
`the_archaeology_and_epigraphy_of_indus_writing` (2), and
`indus_valley_script_deciphered_from_myth` (6). The taxonomy
assigns all three to the Extracted literature claims subdomain
expressly because no testing line exists. Of the 12 claims, 9 sit
at status untested; 3 (all in the myth document) carry negative
standings from their extraction records that no study has ever
re-tested.
**Why its absence blocks convergence:** extracted claims are the
program's picture of what the literature asserts. Twelve of the 23
were never connected to the testing machinery at all, so the picture
holds assertions the program has neither confirmed nor refuted with
its own instruments.
**Candidate:** one testing-line study per document (or a single
study with three arms), taking each claim to a registered corpus
test where a test exists.
**Falsifier:** the claim-by-claim pass finds claims admitting no
corpus test (purely historiographical assertions) → those claims
disposition as not-testable and the node shrinks to the testable
subset; the falsifier is expected to fire for at least the myth
document's framing claims.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-24. D-DESIGN OUTCOMES ARE UNCONSUMED; SUCCESSOR STRUCTURE
UNRECORDED AT CLAIM LEVEL (Claim families). UNCONNECTED.
Kind: missing edge. Scan source: B-06
(`records/scan-families-contact.md`).
**Missing piece:** the consumption/residue record for the D-design
line. Two faces, both from the generated layer: (a) of the matrix's
10 study columns, 6 are unused (046, 047, 051, 056, 063, 064), 7
study outcome blocks are recorded as not bearing, and study-class
cells total 7 — study outcomes exist that no claim cell consumes
under matrix-defs v1; (b) the taxonomy's title record carries
successor edges for 045→069, 046→064, 050→071, 053→068, 056→063,
057→065, 070→074, but D-designs 044 (D-02), 047 (D-09), 051 (D-10),
052 (D-01), 054 (D-08), 055 (D-15) carry no successor edge, and
whether each closed cleanly or left an open residue is recorded
nowhere at claim level.
**Why its absence blocks convergence:** a closed design's residue
can drop out of the program silently. The map shows the D-design
studies as open bundles of draft claims; it cannot show that a
question was finished, abandoned, or inherited — the successor
structure is the program's memory of its own source-thesis tests.
**Candidate:** a D-design residue census over the six no-successor
designs' outcome records and the seven non-bearing outcome blocks,
recorded as claim-level edges or explicit terminal dispositions.
**Falsifier:** every one of the six records states a terminal
verdict with no named residue → the find downgrades to a bookkeeping
note and closes.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-25. FOURTEEN EXTRACTED CLAIMS ARE ISOLATED ROWS IN THE
EVIDENCE MATRIX (Claim families). UNCONNECTED.
Kind: missing edge. Scan source: B-07
(`records/scan-families-contact.md`).
**Missing piece:** any edge at all for 14 extracted claims — rows
with zero cells (rows with cells 862 of 876): the
`ancient_writing…` sign_val_0002/0003 pair, the
`indus_valley_script_deciphered_from_myth…` manual_001–004 set, the
`parpola_2010_dravidian_solution…` manual_001/002 pair, the
`the_archaeology_and_epigraphy…` sign_val_0001/0002 pair, and
`without_kings…` manual_001/002/004/005. They have program-map nodes
but no recorded relation to any document, study, or anchor column —
including the Parpola document's own two claims, the subject of
GR-088-01.
**Why its absence blocks convergence:** the matrix layer cannot weigh
what it cannot reach. Fourteen literature claims — over half the
extracted population — are invisible to the program's evidence
machinery while remaining visible on the map.
**Candidate:** a cell-construction pass deciding, per claim under the
defs, whether its isolation is a registered defs consequence
(non-bearing outcomes, the R-rules) or a construction gap.
**Falsifier:** the pass shows every empty row's isolation follows from
a registered matrix-defs rule → the find downgrades to a defs note for
the register, not a gap.
**Type:** in-house re-derivation.
**Owner gates:** a matrix-defs amendment, if the pass recommends one,
is a program act.

GR-088-26. SPEC 086 RESIDUAL: THE S-R3 POSITIONAL-CLASS TABLE IS
UNMEASURED (Program infrastructure). UNMEASURED.
Kind: missing node. Source: Spec 086 Stage 5 record, §T505 item 5 —
**not an S5 scan find.** This entry was added at consolidation (S6)
because the T602 completeness check maps it from C088-11's named
source lists (the Spec 086 residuals); the scans produced no find for
it, and leaving it unmapped would have failed the completeness claim
this register is presented under. Its provenance is stated here so
the owner can strike it at ratification if he judges otherwise.
**Missing piece:** the measured positional-class table S-R3 needs.
The settling rule S-R3 is registered in glossa-settle-1 but inert:
its positional-class table is UNMEASURED, so the rule cannot fire on
any claim (Spec 086 Stage 4 record; T505 item 5 re-scores the
projected-constraint engine "partially closed" on exactly this leg).
**Why its absence blocks convergence:** one of the settling layer's
registered rules is decorative until the table exists — any verdict
path that should pass through positional class silently does not.
**Candidate:** the positional-class measurement study the Stage 4
record prescribes, producing the table as a registered input, after
which S-R3 fires or is retired on the measurement's own result.
**Falsifier:** the measurement shows positional class carries no
settling signal over the registered population → S-R3 retires as
measured-null rather than activating, and the residual closes as a
verdict, not a table.
**Type:** in-house re-derivation.
**Owner gates:** none (the table, once measured, enters by the
settling layer's own registration discipline).

GR-088-27. TWO STRICT ANCHORS ARE RECORDED AS INSUFFICIENT EVIDENCE
— M367, M048 (Anchors & readings). UNJUDGED.
Kind: thin evidence. Scan source: A-08
(`records/scan-corpus-anchors.md`).
**Missing piece:** evidence itself. Both are Phase-48 promotions
(the promotion subset's 2 insufficient of 30); the audit's verdict
is that the trails do not carry enough to judge them either way.
**Why its absence blocks convergence:** two members of the strict
core are known-empty: they count in the 94 and support nothing.
Unlike GR-088-03, no method repair changes this — the record is the
gap.
**Candidate:** targeted evidence assembly over the widest trails
(Phase-108 register, crosswalk, corpus frames) with a stop rule.
**Falsifier:** assembly over the full trails still yields no second
line → the pair is recorded as permanently insufficient and exits the
strict core's working mass by disposition.
**Type:** in-house re-derivation (assembly of existing records; only
external evidence could change the outcome if it fails — noted, not
claimed).
**Owner gates:** none.

GR-088-28. T201: TWO REGISTERED ROUTES DERIVE MAHADEVAN:64/70/72
DIFFERENTLY (Program infrastructure). UNJUDGED.
Kind: stale bookkeeping. Scan source: C-06
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** the owner's oracle ruling, and the losing route's
amendment. Matrix-defs v1's literal key resolves `mahadevan:64`,
`mahadevan:70`, `mahadevan:72` to no anchor record (the current matrix
coverage still lists exactly these 3 as sign_refs_without_anchor_record,
all on `parpola_2010_dravidian_solution_manual_002`), while
glossa-settle-1 resolves the same references by number to
M064/M070/M072. The divergence was flagged for the owner's oracle read
beside T201 at Spec 086 Stage 2; no ruling is on record and matrix-defs
is unamended.
**Why its absence blocks convergence:** one claim's anchor relations
are simultaneously "no record" and "M064/M070/M072" depending on which
registered surface a reader opens. The program's two generated layers
disagree about the same fact, by name, in print.
**Candidate:** the owner's oracle ruling, then the amendment of the
route that loses (a matrix-defs v2 key rule, or a settle-key
registration change).
**Falsifier:** a third registered route is found resolving the refs a
third way → the divergence is wider than two routes and the entry must
be re-scoped before any ruling.
**Type:** in-house re-derivation (a reconciliation of the program's own
records).
**Owner gates:** OWNER — the ruling is his oracle act; T201's acceptance
was human-as-oracle from the start.

GR-088-29. THE DATA-LINEAGE QUESTION: TWO PRODUCTION DATASETS, NO
ADJUDICATION (Program infrastructure). UNJUDGED.
Kind: stale bookkeeping. Scan source: C-09
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** the adjudication of which dataset is canonical
where they differ, and a diff census bounding where they differ. Both
are preserved: the VM-era dataset and desktop snapshot 1 (2026-10-28,
taken at the Spec 080 cutover). Scope note: the VM production DB holds
no claim state — claims of record live in the repo checkout — so the
open question concerns the application's dataset, not the ledger.
**Why its absence blocks convergence:** any app-level record (jobs,
experiments, reports) can exist in two versions with no rule for which
one a future surface should show. The ambiguity is bounded but
unbounded-in-time: it survives every migration that copies either
dataset forward.
**Candidate:** the lineage adjudication — a byte-level diff census
first, then the owner's ruling on the census.
**Falsifier:** the census shows the two datasets identical in every
claim-adjacent respect → the question is moot and closes as not-a-gap,
with the census as the record.
**Type:** in-house re-derivation.
**Owner gates:** OWNER — the adjudication is his ruling.

GR-088-30. GAP-C12 REMNANT: A LEGACY CHI-SQUARED RULE IS STILL
REGISTERED, ITS LIVE REACH UNTRACED (Program infrastructure).
UNMEASURED.
Kind: missing node. Scan source: C-02
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** the live-caller trace and the disposition.
`backend/glossa_lab/experiment_graph_phase20.py` still declares
significance by `chi2 > 3.84 * max(1, dof)` — a statistically wrong
threshold scaling (verified in the current tree by the scan: the rule
at line 462, `critical_per_dof` 3.84 at line 474) — and the gap record
states "whether any live verdict flows through it is untested." The v2
checkers can fail correctly; the legacy module was neither retired nor
repaired.
**Why its absence blocks convergence:** an unknown number of verdicts
(possibly zero) rest on a rule the program has already judged wrong.
Until the trace runs, no verdict inventory can certify that none of
them are live.
**Candidate:** run the caller trace, then the disposition it dictates
(retire the module, or replace the rule with proper per-dof critical
values).
**Falsifier:** the trace finds zero live callers and zero
verdict-bearing artifacts → the module retires and the find closes as
bookkeeping; a trace finding live verdicts converts it to a
thin-evidence find over those verdicts.
**Type:** in-house re-derivation.
**Owner gates:** the disposition is the experiment-graph maintainer's
(per the gap record).

GR-088-31. SPEC 024, ROOT OF THE F1/F2 LINEAGE, IS BUNDLE-LESS (Claim
families). UNJUDGED.
Kind: stale bookkeeping. Scan source: B-08
(`records/scan-families-contact.md`).
**Missing piece:** `024-evidence-integration`'s claims bundle — or a
recorded disposition that it is pre-ledger history. Its successors
carry bundles: `059` is "Spec 024 F1 Rebuilt", `060` is "Residue of
Spec 024 F2", `067` re-runs `059`. The lineage's root is the one member
the ledger cannot weigh. Consumes 1 `bundle_less_study` find.
**Why its absence blocks convergence:** the F1/F2 object-join line is
one of Domain 3's live lines; its origin study's findings enter the
successors' premises without ever having been ledgered themselves.
**Candidate:** bundle backfill from 024's record.
**Falsifier:** 024's record contains no claim-shaped statements beyond
what 059/060 already ledger → disposition as history, with the lineage
root marked superseded-by-successors.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-32. THE MULTI-SPEC MEMBERSHIP FORK (44 CLAIMS) IS UNRULED
(Program infrastructure). UNJUDGED.
Kind: stale bookkeeping. Scan source: C-11
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** the ruling on the fork — or a recorded decision that
the registered reading stands permanently. The taxonomy draft's premise
("none multi-spec today") is falsified by the ledger: 44 bundle claims
name more than one spec directory across their `sources[]`, in
non-representative roles (`bundle_aee`, `evidence_instance`,
`promotion`); the ids are enumerated in every build's coverage block
(`multi_spec_claims`, 44). Program-map-defs v1 registered membership =
the source-of-record spec only (Stage S1 record, departure (a)), so
citing studies' roll-ups do not count claims they cite. The other reading
(any-source membership) would be a defs v2 amendment; it has not been
ruled on.
**Why its absence blocks convergence:** two defensible readings of "a
study's claims" diverge on exactly these 44 claims. Any future surface
that counts membership the other way disagrees with the program map by a
known, enumerated set — a standing invitation to a future "the two
records disagree" find with no ruling to point at.
**Candidate:** the owner rules the fork at this register's ratification;
if any-source membership wins, defs v2 and the builder amendment follow
as their own act.
**Falsifier:** a recomputation under the any-source rule changes no
study's class on today's ledger → the fork is presentational today and
downgrades to a note, with the recomputation as its record.
**Type:** in-house re-derivation.
**Owner gates:** OWNER — the defs' semantics were his at T003/T101;
changing or confirming them is his.

GR-088-33. SPEC 013, DOMAIN 4'S ATTESTATION STUDY, IS BUNDLE-LESS
(Contact zone & external corpora). UNJUDGED.
Kind: stale bookkeeping. Scan source: B-12
(`records/scan-families-contact.md`).
**Missing piece:** `013-tn-graffiti-crosswalk`'s claims bundle, or its
pre-ledger-history disposition. It is Domain 4's only
independent-attestation study (the CANDIDATE-tier sign tail's external
context) and one of the 28 bundle-less directories; its standing lives
in prose. Consumes 1 `bundle_less_study` find.
**Why its absence blocks convergence:** Domain 4's thinness rests partly
on this: the domain's one study whose evidence originates outside the
Indus corpus proper is the one the ledger cannot weigh.
**Candidate:** bundle backfill from 013's record.
**Falsifier:** as GR-088-31 — no claim-shaped statements beyond what
later records already ledger → disposition as pre-ledger history.
**Type:** in-house re-derivation.
**Owner gates:** none.

GR-088-34. THE TRACKER'S LLMS.TXT NAMES THE SUPERSEDED V8 PREPRINT AS
LATEST (Program infrastructure). UNSTATED.
Kind: stale bookkeeping. Scan source: C-07
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** the corrected latest-release line on the served
`bitconcepts.tech/llms.txt`, which still names the superseded v8 preprint
as the latest release (verified live 2026-10-31) while v9 is the current
deposit. The correction is held as C084-10 because its text is bundled
with the prepared v10 corrections package awaiting the owner's approval
of the exact text, and the source lives outside this repo.
**Why its absence blocks convergence:** llms.txt is the machine-facing
summary of the program's public record; it currently directs readers to a
superseded version as the latest — the one public surface that misstates
the program's own headline artifact.
**Candidate:** the v10-gated correction, published through the tracker
publish path with its served-identity check.
**Falsifier:** a fresh fetch of the served llms.txt already names v9 (or
v10) → the find is already closed and is removed, with the fetch as the
record.
**Type:** in-house re-derivation.
**Owner gates:** OWNER — the correction text is bundled with his v10
approval act.

GR-088-35. THE TAXONOMY'S DOMAIN-4 NOTE DESCRIBES CLAIM NODES THE MAP
DOES NOT CONTAIN (Contact zone & external corpora). UNSTATED.
Kind: stale bookkeeping. Scan source: B-11
(`records/scan-families-contact.md`).
**Missing piece:** a taxonomy note that matches the generated picture.
The v0 draft's Domain-4 note asserts the Gulf/Laursen line "enter[s] the
map as claim nodes under their testing studies in Domain 3 and as
extracted claims" — but its §4 table assigns no Gulf/Laursen document,
and the map, derived only from the ledger, contains no such nodes
(GR-088-17's count). The prose expectation and the generated picture
disagree; under C2 the map governs, and the prose is the find.
**Why its absence blocks convergence:** the taxonomy is a builder input;
a note in it that misdescribes the population teaches every future reader
(and every future taxonomy amendment) a wrong starting picture of the
program's thinnest domain.
**Candidate:** correct the note at the next taxonomy version, recording
which of GR-088-10 / GR-088-17 changed the picture by then.
**Falsifier:** a Gulf/Laursen claim is located in the ledger under a
naming the scan's search missed → the find closes as a scan error,
recorded as such in the register.
**Type:** in-house re-derivation.
**Owner gates:** a taxonomy amendment is a stage-record act (C088-9).

GR-088-36. SPEC NUMBERS 049 AND 085 HAVE NO DIRECTORY (Program
infrastructure). UNSTATED.
Kind: stale bookkeeping. Scan source: C-10
(`records/scan-infra-bookkeeping.md`).
**Missing piece:** a recorded disposition per number. Verified against
the scan-day tree (89 directories; no `049-*`, no `085-*`): 049 is named
as a predecessor in Spec 070's own title ("Successor to Spec 049, D-06")
— a number the lineage cites that the tree cannot produce; 085's package
(the graph-matrix audit) exists only in the goal workspace, unadopted —
its six gaps were re-scored by Spec 086 Stage 5 without the spec ever
landing.
**Why its absence blocks convergence:** the count of the program's studies
is citable two ways (89 directories; numbers running to 088 with two
holes), and a successor's title cites a predecessor no reader can open.
Small, but exactly the class of discrepancy that compounds in a program
whose defense is its records.
**Candidate:** for 049, a register disposition (lineage reference, not a
study — no directory ever existed in this tree); for 085, adoption or
formal non-adoption of the package. This entry itself is the 049
disposition unless ratification rules otherwise.
**Falsifier:** a 049 bundle or directory surfaces in any clone or archive
→ 049 converts to a bundle-less-study find (the GR-088-13 pattern) and
this disposition is wrong on the record.
**Type:** in-house re-derivation.
**Owner gates:** 085's adoption is the owner's act.

GR-088-37. SPEC 072 — CARRIED FIND, OWNER RESTRICTION BY DESIGN (Claim
families). NO STATUS WORD.
Kind: none — this entry is the find list's `restricted_node` item,
carried to S6 by T504's explicit disposition. It is not one of the four
gap kinds and not a gap.
**The restriction, stated in the registered form:** the study
`072-fish-family-profiles-redesign` renders name-only on every program
surface — "executed — held under the Roif gate" — under a standing owner
restriction. This entry records the restriction and nothing else: no
standing, no member counts, no content of the study appears here or in
any entry above.
**Why it is in the register:** the completeness claim (C088-11) covers
every find-list item; the find list's 38th item is this one, and its
disposition is the carry, recorded rather than scanned. The restriction
is by design, not a defect; nothing about it blocks convergence, and no
candidate is proposed.
**Owner gates:** OWNER — the restriction stands until the owner lifts it
by name. No agent route exists, and none is sought by this register.

## Census of this register

Entries: **37** (GR-088-01 … GR-088-37), consolidating the S5 scans'
35 finds and 37 candidates, the 1 carried find-list item (GR-088-37),
and 1 entry added at consolidation from its source record (GR-088-26).
Candidates carried: **38** (GR-088-03 carries three; GR-088-37 carries
none; every other entry carries one). Every candidate carries a
falsifier and an honesty-rule type, mechanically counted at Stage S6
(the count is in `records/stage-s6-record.md`).

By kind: missing node 8 (GR-088-05, 06, 08, 10, 17, 23, 26, 30) ·
missing edge 8 (GR-088-01, 07, 11, 16, 18, 19, 24, 25) · thin evidence
8 (GR-088-02, 03, 04, 09, 12, 14, 21, 27) · stale bookkeeping 12
(GR-088-13, 15, 20, 22, 28, 29, 31, 32, 33, 34, 35, 36) · carried,
not a gap kind 1 (GR-088-37).

By domain: Sign inventory & corpus 3 (GR-088-08, 16, 20) · Anchors &
readings 9 (GR-088-02, 03, 06, 07, 12, 13, 14, 19, 27) · Claim
families 9 (GR-088-01, 04, 09, 21, 23, 24, 25, 31, 37) · Contact zone
& external corpora 4 (GR-088-10, 17, 33, 35) · Program infrastructure
12 (GR-088-05, 11, 15, 18, 22, 26, 28, 29, 30, 32, 34, 36).

By status word: UNSTATED 9 · UNMEASURED 7 · UNJUDGED 10 · UNCONNECTED 8 ·
DATA-BLOCKED 2 · TIME-SENSITIVE 0 · no status word (carried) 1.

Deduplication at consolidation: **no two scan finds were merged.** The
consolidation checked the near-duplicate families — the bundle-backfill
finds (GR-088-13, 20, 31, 33, with GR-088-22 carrying the same
population's audit-era instrument), the falsifier finds (GR-088-12
anchor-record level, GR-088-21 extracted-claim level, GR-088-22
spec-document level — three different instruments), and the edge finds
(GR-088-07, 11, 18, 19 — four different relations) — and kept each find
as its own entry because each names a different missing piece with a
different falsifier; merging any pair would have hidden a falsifier.
Cross-references are recorded on the entries themselves.

Completeness: the T602 source-coverage annex (every C088-11 source-list
item mapped to entry ids or a recorded not-a-gap disposition, with the
mechanical legs' output) is
`specs/088-full-picture-map-gap-register/records/stage-s6-record.md`,
§ "Source-coverage annex (T602)".

## Owner decisions this register surfaces

Each item names the entry, the decision, and what it unblocks. These
are the owner's acts; the register does not pre-decide any of them.

1. **GR-088-06 — open an adjudication route for the 44 pending
   readings** (a panel on the M222 pattern, or a new instrument
   design), or rule that they stay pending permanently. OD-1 closed
   the instrument route; only the owner reopens the question.
2. **GR-088-10 — the CISI access route.** The sequence study's
   transcription exists only if the restricted material's lawful
   access route, which is the owner's, produces it.
3. **GR-088-28 — the T201 oracle ruling** on mahadevan:64/70/72
   (matrix literal key vs settle by-number), after which the losing
   route is amended.
4. **GR-088-32 — rule the multi-spec membership fork** (confirm
   source-of-record membership as permanent, or direct the defs v2
   any-source amendment), at this register's ratification.
5. **GR-088-29 — adjudicate the data-lineage question** on the diff
   census the candidate produces (VM-era dataset vs desktop
   snapshot 1).
6. **GR-088-34 — the v10 approval act**, with which the llms.txt
   correction (C084-10) is bundled.
7. **GR-088-04 — engage the linguist** for the WP2 rule-set
   certification (a named human; the leg is DATA-BLOCKED until
   supplied). Also gates GR-088-03's candidate 2.
8. **Expert and external-reader engagements** — GR-088-14 (named
   experts for M222/M362/M398), GR-088-02 (external readers for the
   46), GR-088-03 candidate 3 (external sourcing for the 4), and
   GR-088-01 (an outside coder, without whom the locator pass does
   not count as independent confirmation).
9. **GR-088-21 — accept-and-record dispositions**, at ratification,
   for any of the 9 null-falsifier claims whose backfill fails on
   their own source texts.
10. **GR-088-36 — adopt or formally not-adopt the Spec 085 package**
    (the 049 half of the entry is dispositioned by the entry itself).
11. **GR-088-08 — lawful access to the Holdat dataset**, if it is
    not already in program hands.
12. **GR-088-37 — no decision sought.** The Spec 072 restriction
    stands until lifted by name; the register records it and asks
    nothing.

Program acts the register also names (not owner-personal): matrix-defs
amendments (GR-088-07, GR-088-18, and GR-088-25 if its pass recommends
one); the GAP-C07 cross-cutting spec's block approval (GR-088-05); the
Spec 083 sequence's ownership of the desktop sync (GR-088-15); the
taxonomy amendment act (GR-088-35); spec authors' dispositions inside
GR-088-22's sweep.

## Ratification block

**Register v1 — presented for block ratification (T603).**

Ratified as a block (entries, ranking, dispositions, and the
owner-decisions section above), or amended on the record, by the
owner's act:

- Owner: Tristen Pierson
- Act: PENDING — not yet ratified. Until this block is completed by
  the owner's act, this register proposes and commissions nothing;
  first waves are commissioned separately, from the ratified
  register, by a later owner act.
- Date: —
- Record of the act: —

*This register does not establish:* that these are all the gaps there
are — only that every find the S5 scans recorded in the registered
shape is consolidated here, and that the register is complete against
the program's own named source lists (C088-11), which is the claim
the T602 annex checks. Nor does the ranking establish priority in
nature — ranking is judgment, and the owner's ratification (T603) is
where it settles. (T601's lines.)
