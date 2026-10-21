# Spec 039 — Gazetteer Period Assignment: the Spec 027 §6.2 Act, Published Determinations Only

> ## FROZEN — 2026-10-20
>
> Drafted and frozen under the owner's decisions of
> 2026-10-20, recorded in `adjudication.md`: the
> gazetteer period-assignment act is **authorised**,
> bundled with the D-25 chronology test, and its
> evidence standard is **Option 1 — published period
> determinations only**. The AEE lifecycle gate ran
> over the recovered register (0.7-draft) before this
> freeze; the digest in `freeze.json` was computed
> exactly once over the frozen contract. Execution
> is **Phase-403**, run under this frozen contract
> after the freeze merged. At the freeze itself no
> period assignment has been made, no data file has
> changed, and the `program_period_assignment` field
> on `main` stands null on all 36 gazetteer rows
> exactly as Stage 0 left it.

## 1. Purpose

Spec 027's Stage 0 built the program's settlement
gazetteer as descriptive infrastructure: one row per
source assertion about a site, with two distinct
period fields — what the source itself published
(`period_label_as_published`), and the program's own
assignment (`program_period_assignment`), a field
§6.2 provides for but Stage 0 deliberately left
empty on every row, because filling it in is a
separate governed act.

That empty field has already decided a study. Spec
031 (Q7, provenance networks) froze a period rule
under which a site is period-eligible only if the
gazetteer itself labels it Mature Harappan — by
either field. No Indus site carries such a label, so
Phase-395 closed both of its arms at the margins
step, before any response was computed: the
bead/craft arm NOT-YET-TESTABLE, the ceramic arm
NOT ESTIMABLE. The Phase-395 outcome record named
the route forward in so many words: a Spec 027
gazetteer act — the program making period
assignments under its own written rules — is the
step that changes the period screen, and it is a
separate owner decision. The owner took that
decision on 2026-10-20. This spec is the act's
design.

**Epistemic fences (H13), stated before anything
else:**

- **The labels are finding aids, not dating
  evidence.** An assignment under this act states
  that a named publication assigns the site to the
  assigned period, mapped under a frozen rule. It
  is not a radiocarbon determination, not a
  stratigraphic finding, and not new chronological
  evidence of any kind. No chronology scenario,
  spine row, or timing computation consumes an
  assignment as a date.
- **The act changes no verdict by itself.** Spec
  031's closures stand exactly as recorded; Spec
  030's Q6 re-test stands exactly as recorded. The
  one re-computation this act performs is a
  verification step over its own output (§8), and
  it issues no Q7 verdict.
- **Link mass is unaffected, and is stated
  wherever the act's effect is described.** Inside
  the gazetteer's universe, the link side stands at
  2 link-eligible sites and 1 linked pair, against
  Spec 031's frozen viability floors of 8 eligible
  sites and 10 linked pairs. Period labels do not
  move that quantity at all. This act therefore
  cannot make Q7 testable, and no product of this
  act may suggest otherwise.
- **Published determinations only.** The owner's
  Option 1 excludes program-derived assignments:
  no label is inferred from chronology-spine dates,
  neighbouring sites, site size, or any other
  program reasoning. The reading-off-the-spine that
  Spec 031's freeze forbade for that study is not
  licensed here either.
- **A blank is an honest outcome.** A site the
  published record does not assign stays
  unassigned, with the reason recorded. Filling the
  column completely is not a goal of this act; the
  column's remaining blanks are coverage
  statements, not failures.

## 2. The gazetteer as it stands

Verified first-hand at this draft against `main`
(head `5e7f3cdb`), 2026-10-20:

- **Data product.** `data/movement/gazetteer_rows.jsonl`,
  SHA-256
  `5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6`
  — the same hash Phase-395 pinned as its input.
  36 rows, 30 distinct `program_site_id` values.
- **Row sources.** XRONOS 21 rows; CISI Vol. 1
  catalogue (Phase-124 layer) 11 rows; CISI Vol. 2
  catalogue (Phase-124 layer) 4 rows. Licence
  states (§5.1 of Spec 027): `verified_open` 21,
  `open_access_read_only` 15.
- **Period fields.** `period_label_as_published`
  is null on 33 of 36 rows; the three non-null
  values are `["PN", "Neo.?"]` (2 rows) and
  `["PN", "Neo."]` (1 row) — pre-Neolithic /
  Neolithic labels on Central Asian rows, nothing
  that marks any site as belonging to any Harappan
  period. `program_period_assignment` is null on
  all 36 rows.
- **The field contract (§6.2).** The gazetteer unit
  is one source assertion about a site; clustering
  under a `program_site_id` never deletes source
  rows or their disagreements.
  `program_period_assignment` is nullable, and when
  present it records the mapping rule and the
  reviewer. §6.3 forbids resolving conflicting
  source rows by majority vote. §6.5 preserves
  competing assertions side by side and requires
  any analysis to name the scenario it uses and
  report the rival as a sensitivity.
- **The published dataset.** The Stage 0 release
  package (the `verified_open` rows only: 21-row
  gazetteer CSV, spine CSV, README, source
  register) is deposited on Zenodo as record
  23300361, DOI 10.5281/zenodo.23300361, verified at
  this draft. That deposit is a published record:
  this act supersedes it only by a new version of
  the same record (§6), never by editing it.

## 3. The evidence standard (decided: Option 1)

The owner decided the evidence standard on
2026-10-20 (`adjudication.md`): **published period
determinations only.** Operatively:

- **Admissible.** A period determination for a
  named site, stated in a publication, cited with
  its locator (page, table, or record). The
  determination is the publication's own: an
  excavation report's statement of a site's
  occupational periods, a published survey's or
  catalogue's per-site period assignment, a
  published compilation's site list entry. Which
  published bases count, and in what citation
  order, is the source hierarchy of DD-039-2.
- **Inadmissible.** Chronology-spine dates and any
  inference from them; neighbouring-site analogy;
  site-size or survey-intensity reasoning;
  unpublished data in any form; the program's own
  prior prose; and any determination that cannot
  be cited to a publication and a locator.
- **Restricted sources enter as citations only.**
  Possehl's published site lists and Law (2011)'s
  compilations stand `catalogue_only` in the Stage
  0 record, and the CISI catalogue layers stand
  `open_access_read_only`. Under §5.1 of Spec 027
  and the Stage 0 posture, an assignment resting on
  such a source records the citation, the locator,
  and the determination as published — the source's
  contents are not copied or redistributed in bulk,
  exactly as Stage 0 already handles them.
- **"Published" at the edges.** The ordinary cases
  are clear (journal articles, their published
  supplements, published report and monograph
  series). One body of material sits at the edge —
  the TwoRains project's determinations — and its
  treatment is stated precisely as DD-039-3, with a
  conservative recommended default, because the
  Masudpur question (§10) turns on it.

## 4. The label set and the mapping rule

**Label set (DD-039-1, decided at freeze).** The coarse
three-period set the downstream designs actually
consume: **Early Harappan**, **Mature Harappan**,
**Late Harappan**. The vocabulary is aligned to
Spec 031's frozen period rule (adopted 4A;
F031-C10): a site is period-eligible iff its
gazetteer `period_label_as_published` **or program
period assignment** "indicates Mature Harappan
occupation as published", and that design attempts
"no finer temporal slicing" anywhere. A finer set
would be more work per site, more disagreement to
adjudicate, and is needed by nothing currently
frozen. Under this set, a published determination
outside the Harappan sequence (for example the
gazetteer's own `PN`/`Neo.` labels) grounds no
assignment.

**Mapping rule.** Each source's period scheme is
mapped to the label set by the scheme-aware table
frozen immediately below, before any assignment is
made. The rules of the table:

1. A value with a table entry maps as the entry
   states; a value with no entry maps to nothing —
   the site stays unassigned on that evidence, with
   reason code `UNMAPPED_SCHEME_VALUE`. No mapping
   is improvised at assignment time.
2. A source that assigns a site to more than one
   period (a multi-period occupation statement)
   grounds a multi-label record, stated as such —
   not silently collapsed to one label. (How the
   eligibility reading treats a multi-label record
   that includes Mature Harappan is determined by
   Spec 031's frozen wording — "indicates Mature
   Harappan occupation" — and is not re-decided
   here.)
3. The mapping entry applied is recorded on every
   assignment (§6), so any label can be traced from
   the published value through the named rule to
   the assigned label.

**Frozen mapping table (Phase-403).** The reviewer
string on every assignment is `Muse Spark
via Muse (AI agent)`. An entry applies only
when the cited publication's own period scheme is
the scheme named in the entry; a value in a
different scheme is not carried across schemes.

| Entry | Published scheme / value | Assigned label(s) |
|---|---|---|
| MAP-EXPLICIT-EARLY | Explicit three-period scheme: `Early Harappan`, or `EH` where the publication itself expands EH as Early Harappan | Early Harappan |
| MAP-EXPLICIT-MATURE | Explicit three-period scheme: `Mature Harappan`, or `MH` where the publication itself expands MH as Mature Harappan | Mature Harappan |
| MAP-EXPLICIT-LATE | Explicit three-period scheme: `Late Harappan`, or `LH` where the publication itself expands LH as Late Harappan | Late Harappan |
| MAP-EXPLICIT-MULTI | Explicit three-period scheme: a value naming two or three of the labels above | Each named label, as a multi-label record |
| MAP-RANGE-EARLY-MATURE | Explicit three-period scheme: `Early-Mature Harappan` or the equivalent range wording | Early Harappan; Mature Harappan |
| MAP-RANGE-MATURE-LATE | Explicit three-period scheme: `Mature-Late Harappan` or the equivalent range wording | Mature Harappan; Late Harappan |
| MAP-RANGE-EARLY-LATE | Explicit three-period scheme: `Early-Late Harappan` or the equivalent all-period range wording | Early Harappan; Mature Harappan; Late Harappan |
| MAP-HARP-RAVI | HARP/Harappa period scheme: `Ravi Phase` or `Period 1` where the same publication equates Period 1 with the Ravi Phase | Early Harappan |
| MAP-HARP-KOTDIJI | HARP/Harappa period scheme: `Kot Diji Phase` or `Period 2` where the same publication equates Period 2 with the Kot Diji Phase | Early Harappan |
| MAP-HARP-HARAPPAN | HARP/Harappa period scheme: `Harappa Phase` or `Period 3` where the same publication equates Period 3 with the Harappa Phase | Mature Harappan |
| MAP-HARP-CEMETERY-H | HARP/Harappa period scheme: `Cemetery H Phase` or `Period 5` where the same publication equates Period 5 with the Cemetery H Phase | Late Harappan |
| MAP-JHUKAR | A published scheme that names the site's occupation as the `Jhukar Phase` | Late Harappan |
| MAP-CEMETERY-H | A published scheme that names the site's occupation as the `Cemetery H Phase` (outside the HARP scheme) | Late Harappan |

No other published value has a mapping entry.
In particular, an unqualified `Harappan`, `Indus`,
`Pre-Harappan`, `Post-Harappan`, `Bronze Age`, an
ordinal period in an unnamed scheme, or a named
phase not listed above maps to nothing and yields
`UNMAPPED_SCHEME_VALUE` if it is the only evidence
for the site. A value affirmatively outside the
Harappan sequence (for example `PN` or `Neo.`)
yields `OUTSIDE_LABEL_SET` where the report records
that value as the reason for a blank. These entries
are the whole table; execution adds none.

## 5. Disagreement handling

Disagreements are carried, never voted away (§6.3):

- Where admissible determinations for one site map
  to more than one label, the assignment is flagged
  **contested**, and every conflicting determination
  stays on the record verbatim, with its citation.
- No majority vote, no hierarchy suppression, and
  no silent preference resolves a contested
  assignment. The source hierarchy (DD-039-2) is a
  citation and presentation order only.
- Any later study consuming the labels reports its
  period checkpoint **both ways** — contested
  assignments counted, and contested assignments
  excluded — in the §6.5 posture Spec 030 used for
  contested chronology.
- **Spec 030 Ask 2 stays RESERVED.** Whether the
  contested-excluded computation must bind a future
  Q6 freeze was expressly not decided by Spec 030's
  adjudication and is not decided by this act. Ask
  2 governs chronology scenarios for the Q6 timing
  question; this act governs gazetteer period
  labels. They are different fields in different
  records, and nothing in this spec depends on Ask
  2 or prejudges it.

## 6. The assignment record and the act's outputs

**Unit.** Assignments are made per `program_site_id`
(30 sites) and carried onto every gazetteer row for
that site. The assignment field is the program's
own (§6.2): a row keeps its source's assertion
untouched in every other field, whatever the
program's assignment says.

**Assignment shape.** When present,
`program_period_assignment` is a record carrying:
the `label` (or label set, §4 rule 2); the
`mapping_rule` applied; the `reviewer` of record;
the `evidence` — every determination the assignment
rests on, each with its source, citation, locator,
published period value, and period scheme; and,
where §5 applies, `contested: true` with the
conflicting determinations listed. When no
admissible determination exists, the field stays
null and the assignment report records the blank's
reason code (`NO_PUBLISHED_DETERMINATION`,
`UNMAPPED_SCHEME_VALUE`, or `OUTSIDE_LABEL_SET`).

**Outputs.**

- **A — the assigned gazetteer.**
  `data/movement/gazetteer_rows_assigned.jsonl`:
  all 36 rows carried over, byte-identical to the
  pre-act file in every field except
  `program_period_assignment`. The pre-act file is
  not modified; its SHA-256 (above) is pinned in
  the outcome record, and its original bytes —
  including every empty period field — remain in
  git history and in that pin. The assignment is
  an append to the record, not an edit of it.
- **B — the assignment report.** A results record
  and report (`reports/phaseNNN_results.json`,
  `reports/phaseNNN_gazetteer_assignment_report.md`,
  phase number fixed at freeze): the per-site
  assignment table with its evidence, the contested
  list, the blank list with reason codes, and the
  §6.3 completeness report by source (rows
  catalogued, assignments grounded per evidence
  base, disagreements carried).
- **C — the dataset's new version.** A new version
  of the Zenodo Stage 0 record (23300361),
  deposited as part of execution, carrying the
  assigned gazetteer for the releasable rows under
  the same licence posture as v1 (assignments
  resting on restricted sources appear as citations,
  per §3). The existing deposit is never edited.

## 7. Execution shape (frozen)

For the Phase-403 execution under this frozen
contract, the shape is:

1. **Graph-first build** (H15/H23): script → graph
   module → registration → registration
   verification → run. No phase script runs before
   its graph node exists.
2. **Input integrity:** the gazetteer file hashes
   to the §2 pin; any drift stops the execution.
3. **Evidence assembly:** per site, the admissible
   determinations with locators, under the §3
   standard and the frozen source hierarchy.
4. **Mapping and assignment:** the frozen mapping
   table applied; contested flags set under §5;
   blanks recorded with reason codes.
5. **Outputs A and B** written and hashed.
6. **Margins verification step** (§8).
7. **Output C:** the Zenodo new-version deposit,
   gated through the release gate, recorded by DOI.
8. **Outcome record:** this directory's
   `outcome.md` completed by append; the root
   LEDGER entry; the foundation check (H21) after
   the record lands.

## 8. The margins verification step

The act's execution enables one re-computation, and
this spec proposes it as **this act's own
verification step** (DD-039-5, recommended): re-run
the first gate of the Phase-395 margins step over
the assigned gazetteer — and nothing beyond that
gate.

- **What is recomputed.** Period eligibility under
  Spec 031's frozen rule (F031-C10), read over
  Output A: which gazetteer sites now indicate
  Mature Harappan occupation by a program period
  assignment (the `period_label_as_published` side
  of the rule is unchanged by this act), and the
  eligible-site count that follows — reported both
  ways over contested assignments (§5).
- **What the record then states, in writing.** The
  margins step's remaining frozen floors and where
  the record stands against them: the in-universe
  link mass is 2 link-eligible sites and 1 linked
  pair, against floors of 8 eligible sites and 10
  linked pairs. On the standing record, the
  verification step therefore closes at the
  link-mass floor — a different reason from
  Phase-395's period-floor closure, the same
  outcome class, recorded as a verification result
  and not as a Q7 verdict.
- **What is never re-opened.** No response is
  computed; no matrix, permutation, or verdict
  machinery of Spec 031 runs; Spec 031's closures
  (bead/craft NOT-YET-TESTABLE, ceramic NOT
  ESTIMABLE) are not amended, superseded, or
  restated as anything else. A future Q7 re-run is
  a future spec's business, gated on new site-pair
  data, not on this act.

## 9. The D-25 bundle

The owner's decision bundles this act with **D-25**
(the experiment-design portfolio, PR #195): the
chronology-controlled re-test of Spec 025's G1
result — the program's strongest positive site
effect, which stands SUPPORTED under control with
its named weakness intact: **chronology is not
controlled**. D-25 is already runnable on the
205-row extended spine; the bundled act gives its
period strata firmer footing — assignments made
under a frozen mapping rule with citations on every
row, instead of period readings taken off spine
rows case by case — and makes its own thinness
checks (enough sites per period stratum, few
enough unassignable rows) more likely to pass
honestly.

Sequencing inside the bundle: one adjudication
cycle covers both acts; this act executes first;
D-25's spec is its own document (its design stands
in the portfolio) and consumes Output A as an input
pinned by hash. This spec does not design D-25's
test, freeze it, or prejudge its outcome.

## 10. What this spec does not do

- It assigns nothing at draft or at freeze; the
  assignments are execution work, under the frozen
  rules.
- It changes no verdict, no claim stage, and no
  frozen record: Specs 027, 030, and 031 stand as
  written, and the Stage 0 deposit stands as
  published until a new version supersedes it.
- It makes no chronology-spine change. In
  particular it does **not** admit the 28 preserved
  TwoRains / Masudpur determinations: Phase-394
  extracted them in full and did not admit them,
  because Masudpur VII and Masudpur I are not
  gazetteer-established sites and no publication
  reached states their coordinates (Phase-394's
  rule 7 admits coordinate-less rows only for
  gazetteer-established sites). Whether this act
  also establishes those sites is DD-039-4, with
  the conservative recommended default that it does
  not — the act is confined to the existing 30
  sites, and the establishment route stays recorded
  for a future act that takes the coordinate
  question (§5.2) as its own subject.
- It adds no new sites to the gazetteer (subject
  only to DD-039-4, default no), removes none, and
  re-clusters none.
- It decides nothing about Spec 030 Ask 2 (§5).

## 11. Epistemic boundaries (H13)

This act's products say, at most: for each of 30
sites, whether a named publication assigns that
site to a period, and what this program recorded
under its frozen mapping rule. They do not say when
any site was occupied; they do not date anything;
they do not strengthen or weaken any movement,
culture, or language claim; and they do not bring
any registered question closer to a verdict except
by removing one named infrastructure gap, whose
removal §8 records with its limits attached.

## 12. Governed claims (summary)

The claim register (`claims.json`, F039-C01…C15)
governs this design. In summary: C01 the scope of
an assignment statement; C02 the published-
determination basis; C03 the exclusion of
spine-derived labels; C04 the blank rule; C05 the
label set; C06 the site-level unit and row
carriage; C07 the mapping-rule and reviewer
record; C08 the citation and locator record; C09
the contested flag; C10 the no-majority-vote rule;
C11 the append-only preservation of pre-act rows;
C12 the deposit supersession rule; C13 the
no-verdict-change fence; C14 the margins
verification step's scope; C15 the unchanged
link-mass statement.

## 13. Design decisions

The freeze decisions are logged in
`adjudication.md` as DD-039-1…DD-039-8:
DD-039-1…DD-039-6 adopt the draft recommendations,
DD-039-7 allocates Phase-403, and DD-039-8 records
the AEE gate reading. The two
substantive owner decisions of 2026-10-20
(authorisation and bundle; Option 1) are recorded
there as **decided**, not as proposals.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
