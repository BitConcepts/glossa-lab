# Spec 037 / Phase-402 — Outcome record

> ## EXECUTED — 2026-10-20 — PILOT COMPLETE — SPINE HALTED
>
> Execution ran as Phase-402 under the contract frozen
> 2026-10-20 (freeze digest in `freeze.json`) and the
> owner's standing pipeline authorisation of 2026-10-20
> (freeze order 038, then 037, then 039, then 040).
> Step 0 passed in full; the pilot graded all 693
> candidates; the CONFLICT share (49.21%) exceeded the
> frozen 20% halt threshold, so **no spine file was
> written** and the outcome is recorded in the frozen
> wording: **PILOT COMPLETE — SPINE HALTED**. Every
> quantity recorded here is an aggregate statistic —
> no portion-derived row appears in this file, which
> lives in the repository (gate: F037-C08). Candidate-
> level records exist only in the local build record
> in the restricted store, named in §8.

## 1. What was executed

Phase-402 executed the frozen Spec 037 contract
(freeze digest
`122c2ea4858094d2c6514d05225dfaad1f5266cccffd764949736a78d81aa4db`,
framework026; freeze PR #225, merged 2026-10-20 as
`e9b5026cc33cb2c58208e2059af1379cc2525bcc`) under the
owner's standing pipeline authorisation of 2026-10-20.
Graph-first build (H15/H23): the phase script
(`backend/scripts/phase402_concordance.py`), the graph
node `IndusPhase402Concordance`
(`backend/glossa_lab/experiment_graph_phase402.py`),
and its registration were committed before any run
(build commit `889e13b1` on this record's branch; two
step-0 checker corrections followed, §2). Workstream
A (the pilot census and the halt rule) and Workstream
B (the HARP annex, DD-037-6: inside this phase, gated
on step 0 only) both ran. The freeze's decisions as
executed: DD-037-4 halt threshold 20% of all
candidates; DD-037-5 stratum 60 (30/15/15), seed
20261020 recorded in the committed build script
before sampling; DD-037-6 annex inside Phase-402;
DD-037-7 the spec's own OSF registration filed at
the freeze (`osf-spec-registration.md`); DD-037-8
phase allocation Phase-402. Nothing else was executed
under this spec. No PRED-register entry was created,
scored, advanced, or retired; no anchor changed.

## 2. Step 0, check by check

Step 0 ran in the frozen order, fail-closed. Two
earlier runs closed inside step 0 on defects in the
execution's own checker — not in the gated material
and not in the frozen contract — and are recorded
here in full because the closures happened:

- **First run — CLOSED AT STEP 0.1.** The checker's
  gate needles were phrased from a paraphrase of the
  gate, and one needle ("Do not upload") does not
  appear in PROVENANCE entry 22. The entry was then
  read in full: it records the classification
  (restricted research material), the permitted uses
  (local research use; OCR and table extraction;
  derived statistics publishable), and the
  prohibitions (no redistribution of scans or page
  images; no uploading to the repo, Zenodo, OSF, or
  any third-party service) in its own words. The
  checker was corrected to quote the entry's own
  recorded words and the correction committed
  (`4e564af4`) before any re-run. No candidate was
  graded by the closed run; it stopped inside
  step 0, before any join was computed.
- **Second run — CLOSED AT STEP 0.2.** The checker
  asserted the table's distinct catalogue-number
  count as 2,101 raw strings; the table carries
  2,106 distinct strings — 2,101 well-formed
  catalogue numbers plus 5 garbled low-confidence
  tokens (all Mohenjo-daro) that the intake's census
  resolves into the set and that match no corpus id.
  The frozen check is "census as intaken": the
  intake's census counts resolved numbers. The
  checker was corrected to the intake's own census
  semantics (2,101 well-formed + 5 garbled, both
  figures pinned) and the correction committed
  (`00f33f3d`) before the re-run. Again, no candidate
  was graded by the closed run.
- **Third run — step 0 PASSED in full:**
  - **0.1 Gate record** — PASS. PROVENANCE entry 22
    on record, naming this material restricted, in
    the terms summarised above.
  - **0.2 Portion integrity** — PASS. Portion PDF
    SHA-256 equals the intake pin `514338b1…`
    (8,206,446 bytes). The local table parse-validates
    at 2,123 records × 26 columns; section census as
    intaken (Mohenjo-daro 519, Harappa (EH) 510,
    Harappa (HARP) 1,094); 2,101 distinct well-formed
    catalogue numbers plus the 5 garbled tokens
    above. The table's SHA-256, recorded by this
    execution (the intake recorded no table hash):
    `7179858d9b2bc18b480ba092a08ea2ee021ce569fcaceb5b992d22c541d333c8`.
  - **0.3 corpus_master pin** — PASS. The SHA-256 of
    the exact corpus bytes consumed equals the pin
    `b19cfe95…`; the bytes were verified identical
    via the repository API (main at the freeze merge)
    and the working copy; 2,722 rows; every
    `source_object_id` unique.
  - **0.4 Repo cleanliness** — PASS. The execution
    tree listing was checked: no portion-derived file
    (no row data, no scan, no spine, no grade table)
    is in the tree; the matches a name search returns
    are this spec's own frozen contract documents and
    pre-existing unrelated files. Re-checked before
    the outcome commit (§8): PASS again.

## 3. Pilot (Workstream A)

The candidate set was regenerated from the pinned
inputs — every exact-string match between a
catalogue number in the local table and a
corpus_master object id (the Holdat `cisi_number`
was never read as a join key): **693 candidates**,
exactly the intake's count (Mohenjo-daro 289,
Harappa (EH) 102, Harappa (HARP) 302; no candidate
spans two sections). All 693 were graded under the
frozen ladder. Outcomes:

- **VERIFIED 269 (38.82%)**
- **CONFLICT 341 (49.21%)**
- **UNRESOLVED 83 (11.98%)**

By portion section (counts; shares of the section's
candidates): Mohenjo-daro — VERIFIED 224, CONFLICT
32, UNRESOLVED 33 (of 289: 77.5% / 11.1% / 11.4%).
Harappa (EH) — VERIFIED 23, CONFLICT 64, UNRESOLVED
15 (of 102: 22.5% / 62.7% / 14.7%). Harappa (HARP) —
VERIFIED 22, CONFLICT 245, UNRESOLVED 35 (of 302:
7.3% / 81.1% / 11.6%). By corpus source: all 693
candidates matched rows of the Yajnadevam corpus;
the mayig CISI digitisation contributed no candidate
(its object ids do not intersect the portion's
numbers).

Conflict breakdown by reason code: **TYPE 339**,
**NUMBER-AMBIGUOUS 2**, SITE 0, CORROB-FC 0,
CORROB-EXC 0, CORROB-MUS 0. The TYPE conflicts are
the ladder working as frozen: the portion's plate
headings class hundreds of the matched objects as
tablets (and a small number as graffiti, ivory
sticks, stone objects, or seal impressions), while
the corpus classes every matched object as a seal —
the two compilations' object-type vocabularies
disagree, and the mandatory type rung records that
as a conflict, candidate by candidate. The 2
NUMBER-AMBIGUOUS candidates are numbers whose own
portion records differ on join-relevant data; both
are barred from VERIFIED and named in the local
build record.

Per-field graded bases: site graded for all 693;
object type graded for 610 (for 83 candidates the
portion side carries no class — a blank heading or
an ADDENDA heading — so type is UNGRADED and those
candidates stand UNRESOLVED on the graded rungs);
**FC 0, excavation 0, museum/registration 0** —
corroboration is UNGRADED for every candidate,
because corpus_master carries no FC, excavation, or
museum/registration values at all (the ladder's
UNGRADED branch, spec §4.3): no corroborating key
could be graded on either a contradiction or an
agreement, and none was repaired, substituted, or
borrowed from any other source.

Independent recount: after the run, a separately
written tally re-aggregated the local grade table
and independently re-graded all 693 candidates from
the raw inputs; **0 mismatches** — the counts,
shares, reason breakdown, section split, and the
annex figures in §5 all reproduce exactly.

Hand-check stratum (DD-037-5; seed 20261020,
recorded in the build script before sampling; 30
VERIFIED / 15 CONFLICT / 15 UNRESOLVED, drawn after
grading): the 15 sampled CONFLICT candidates were
attributed, one by one, to **genuine compilation
divergence in all 15 cases** — in each, the portion
classes the object as a tablet under its plate
heading while the corpus classes the same numbered
object as a seal, with site agreement throughout
and, where the heading names a material, the same
material the corpus records (faience, steatite,
terracotta/clay). Intake extraction error 0;
programme-side record error 0; true non-identity 0.
The 15 sampled UNRESOLVED candidates attribute to:
the heading not carried onto the record at
extraction (continuation rows — the volume prints
the heading once per page section) in 7 cases, the
records' own data fields intact; and the volume's
addenda arrangement (the object is classed at its
main entry, outside the portion) in 8 cases. The 30
sampled VERIFIED candidates were spot-checked: all
30 sound under the ladder (site and seal class in
agreement on both sides); no problem found.
Per-candidate attribution notes live in the local
build record only.

## 4. Spine build

**HALTED.** The CONFLICT share of all candidates is
341 / 693 = **49.21%**, which exceeds the frozen
halt threshold of 20% (DD-037-4). Under spec §4.7
the pilot completes and reports in full, **no spine
file was written** (verified: no
`cisi31-concordance-spine.csv` exists in the portion
folder), and the outcome is recorded in the frozen
wording: **PILOT COMPLETE — SPINE HALTED**. The 269
VERIFIED joins stand as graded candidates in the
local grade table; they were not written into a
spine, and no partial or smaller spine was built —
the halt rule admits neither.

## 5. Annex (Workstream B)

Descriptive only, from the 1,094 Harappa (HARP)
rows of the same local table, gated on step 0 only
(DD-037-6). Dig-year distribution (the two-digit
year in the excavation number's H<YY> prefix, read
as 19YY for YY ≥ 50 and 20YY below): 1986: 1;
1987: 1; 1988: 2; 1989: 4; 1990: 57; 1993: 19;
1994: 91; 1995: 207; 1996: 150; 1997: 89; 1998:
107; 1999: 48; 2000: 3; 2001: 3; **no year token:
312** — exactly the rows carrying no excavation
value (excavation fill 782 of 1,094). Lot/record
fill: registration numbers are carried for **754
of 1,094** HARP rows. Period fill: **656 of 1,094**
— **a floor, not the printed rate**: the scan's
text layer loses split period tokens, so the true
printed fill is at least this and the figure is
never stated without this caveat. Period-code
inventory (each code as printed, with its count;
mixed codes stand as their own classes): 3: 180;
3C: 94; 3B: 70; (3): 104; 2: 41; M(2): 31; S: 27;
3B/C: 21; 3 B/C: 14; 3(3): 14; 2(2): 8; 3 C: 6;
2/3(2): 6; (2): 5; 3 B: 5; 1/2(2): 4; 2/3: 4;
3 (3): 4; 1: 3; 1(1): 2; 3(2): 2; 3C(3): 2; S(3):
2; (4): 1; 2/3(3): 1; 4: 1; 4/5: 1; M (2): 1;
S(2): 1 — and one square-bracketed code as
printed, [4/5]: 1. The codes sum to the period
fill of 656. The annex's limits stand as frozen
(F037-C12, C13): these quantities are descriptive
only, and **the Spec 031 (Q7) finding is unchanged**
— in-universe link mass 2 sites / 1 pair,
bead/craft arm NOT-YET-TESTABLE, ceramic arm NOT
ESTIMABLE; no quantity here feeds a verdict.

## 6. What this outcome does and does not establish

It establishes, for the CISI 3.1 portion's ranges
only (F037-C01, C15): that of the intake's 693
string matches, 269 verify as same-object joins
under the frozen ladder, 341 conflict (almost all
on object type), and 83 cannot be resolved from the
portion as extracted — and that the conflict share
is far above the level at which the programme was
willing to build a concordance spine, so none was
built. It does not establish anything about any
reading, sign, or sequence on any object (F037-C06:
the concordance is a finding aid, and in the event
not even the aid was built). No prediction was
scored, advanced, or retired (F037-C07). The Q7
record is unchanged (F037-C13). Museum and owner
values were used only as printed in 2010, a dated
snapshot (F037-C14). A step-0 stop would have been
recorded as itself; the two checker closures in §2
are recorded as what they were — defects in the
execution's own checker, corrected openly, with the
gate and the census themselves passing as frozen on
the run that counted.

## 7. Claim consequences (governed register)

- **F037-C01** — checked; the outcome concerns join
  verification and descriptive provenance structure
  for the portion's ranges only, as bounded.
- **F037-C02** — governed the regeneration: 693
  exact-string matches treated as candidates,
  never as joins.
- **F037-C03** — the ladder was applied to all 693
  candidates exactly as frozen; VERIFIED was
  reached only through it (269).
- **F037-C04** — 341 conflicts recorded with reason
  codes and never repaired; no data on either side
  was edited; the 2 internally inconsistent numbers
  were barred from VERIFIED.
- **F037-C05** — **fired**: the CONFLICT share
  (49.21%) exceeds 20%; the spine build halted;
  the outcome is PILOT COMPLETE — SPINE HALTED.
- **F037-C06** — held: no join, verified or
  otherwise, is stated as evidence about any
  reading; no spine exists to be misread as one.
- **F037-C07** — held: the PRED register is
  untouched by this execution (byte-identical; no
  entry scored, advanced, or retired).
- **F037-C08** — held: every row-level product
  (grade table, build record, stratum notes) lives
  only in the restricted portion folder; the repo
  carries aggregates only.
- **F037-C09** — executed as frozen: step 0 ran
  fail-closed in the fixed order before any join
  was computed; the two checker closures and their
  corrections are recorded in §2.
- **F037-C10** — the census was graded in full (not
  sampled); the stratum was drawn at the frozen
  size with the seed recorded before sampling.
- **F037-C11** — the reported quantities are
  exactly the pre-registered aggregates of spec
  §4.4; UNRESOLVED is reported as its own class
  throughout.
- **F037-C12** — the annex is descriptive only,
  with the period-fill floor caveat attached in
  the same paragraph (§5).
- **F037-C13** — the Spec 031 (Q7) finding is
  unchanged; no annex quantity fed any verdict.
- **F037-C14** — museum and owner values stood as
  printed in 2010 throughout; none is stated as a
  current location anywhere in this record.
- **F037-C15** — coverage is the portion's ranges
  only; nothing here claims coverage of Vol. 3.1
  as a whole.

## 8. Records

- **Step-0 record:** §2 above; the machine record
  is the local build record (below).
- **Local products** (restricted portion folder
  only; named here by filename and row count,
  contents never in the repo): `phase402-grade-table.csv`
  (693 candidate rows), `phase402-build-record.json`
  (the run's full record, the step-0 table hash,
  and the stratum membership),
  `phase402-stratum-attribution.json` (the
  hand-check attribution record). **No spine file
  exists** (halt rule, §4).
- **Committed results:** `reports/phase402_results.json`
  carries the aggregate record this outcome reports;
  the graph node `IndusPhase402Concordance` serves it.
- **Root LEDGER:** the freeze-plus-execution entry
  appended with this record.
- **Repo cleanliness:** re-checked against this
  record branch's tree before the outcome commit —
  no portion-derived file present: PASS.
- **Suite and CI:** at the freeze merge (PR #225,
  merge commit `e9b5026c…`, tree identical to the
  CI-tested head), the full suite ran green on a
  genuine run verified from its own conclusions —
  7 of 7 jobs successful; backend 1,479 passed /
  20 skipped. This record merges only on the same
  terms (a genuine 7/7 run on the record head); its
  merge figures are recorded in the programme's
  next LEDGER entry and in the execution report.
- The PRED register and the anchors are untouched
  by this execution.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
