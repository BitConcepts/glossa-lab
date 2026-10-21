# Spec 039 — Outcome record (SKELETON — NOT EXECUTED)

> ## PRE-WRITTEN SKELETON — DRAFTED 2026-10-20 — NOTHING EXECUTED
>
> This skeleton is written at draft time so the
> execution append has its shape fixed before any
> run (the Spec 035/036 outcome pattern). Every
> slot below is **PENDING EXECUTION**. Execution
> is gated on this spec's freeze and on the
> bundle sequence in `plan.md` §2; neither has
> been reached at this draft. **No period label
> has been assigned to any site**;
> `program_period_assignment` on `main` stands
> null on all 36 gazetteer rows.

## 1. What was executed

_Pending execution._ To be completed at
execution with: the freeze digest this execution
ran under; the freeze record's DD-039 decisions;
the graph-first build record (experiment script,
graph module, graph registration); the run's own
record paths. Nothing else is executed under
this spec.

## 2. Input integrity

_Pending execution._ The gazetteer file
(`data/movement/gazetteer_rows.jsonl`) recomputed
against the spec §2 pin (SHA-256
`5ac76a30…`) — result: _pending_. Any drift stops
the execution here.

## 3. Assignments

_Pending execution._ To be completed with: the
per-site assignment table (site; assignment or
blank with reason code; label or label set; the
determinations relied on, each with citation and
locator; mapping rule applied; reviewer;
contested flag where set); the contested list
with the conflicting determinations carried
verbatim; the blank list with reason codes
(`NO_PUBLISHED_DETERMINATION`,
`UNMAPPED_SCHEME_VALUE`, `OUTSIDE_LABEL_SET`);
and the §6.3 completeness report by source.
Output A's path and SHA-256: _pending_ (expected
record: `data/movement/gazetteer_rows_assigned.jsonl`).

## 4. Margins verification step

_Pending execution._ To be completed with: the
period-eligibility re-computation under Spec
031's frozen rule (F031-C10) over the assigned
gazetteer — eligible-site count, reported both
ways over contested assignments — and the
standing statement of the margins step's
remaining floors: in-universe link mass 2
link-eligible sites and 1 linked pair against
floors of 8 eligible sites and 10 linked pairs.
The expected record, stated at draft: the step
closes at the link-mass floor, as a verification
result. **No Q7 verdict is issued by this step**,
and Spec 031's closures are not amended by
anything recorded here.

## 5. Dataset new version

_Pending execution._ To be completed with: the
new version of Zenodo record 23300361 (version
DOI, deposit date, file list), deposited through
the release gate; confirmation that the existing
version's files were not edited.

## 6. What this outcome does and does not establish

_Pending execution._ To be written under
F039-C01, C13, and C15: the assignments state
what named publications say about each site's
period, mapped under the frozen rule; they are
not dating evidence; no study verdict changed;
link mass is unchanged. Spec 030 Ask 2 remains
reserved and untouched by this outcome.

## 7. Claim consequences (governed register)

_Pending execution._ One line per governed
claim, F039-C01…C15: which claims the execution
checked, which fired, and which were not
reached — in the Spec 035/036 outcome pattern.

## 8. Records

_Pending execution._ To be completed with: the
results record path and hash; output A's path
and hash; the dataset new version's DOI; the
root LEDGER entry; the foundation check result
(H21); the suite and CI state at the merge.
Spec 027's, Spec 030's, and Spec 031's records
are not touched by any completion of this
skeleton.

---

## COMPLETION RECORD — executed 2026-10-20 (Phase-403)

This section completes the skeleton above by
append. Nothing in the skeleton is edited.

### 1. What was executed

The frozen Spec 039 contract, freeze digest
`ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742`
(freeze PR #226 merged at
`05f961fcb4233f3c54831fe2134f9509f1a75632`;
freeze record and DD-039-1…8 in
`aee-adjudication.md` and `freeze.md` of this
spec directory), executed as **Phase-403** under
owner decisions D1–D2 (the act authorised,
published determinations only) and DD-039-1…8.
Graph-first build: experiment script
`backend/scripts/phase403_gazetteer_assignment.py`;
graph module
`backend/glossa_lab/experiment_graph_phase403.py`
(node `IndusPhase403GazetteerAssignment`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran. The run's own
records: `reports/phase403_results.json` and
`reports/phase403_gazetteer_assignment_report.md`.
Contract registration filed at the freeze:
OSF <https://osf.io/w38ha/> (status at this
record: FILED — PENDING APPROVAL; see
`osf-spec-registration.md` in this directory).

### 2. Input integrity

The pre-act gazetteer recomputed to SHA-256
`5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6`,
matching the frozen §2 pin exactly: 36 rows,
30 distinct sites, `program_period_assignment`
null on all 36 rows. The phase script verifies
the pin fail-closed before any output is
written. The pre-act file was not modified at
any point (its hash is unchanged after the run).

### 3. Assignments

**11 of 30 sites assigned** (17 of 36 rows carry
an assignment); **1 contested**; **19 blank**.
Label incidences: Early Harappan 4, Mature
Harappan 8, Late Harappan 6. Reviewer of record
on every assignment: Muse Spark via Muse
(AI agent). Determinations were recorded only
where verified in the publication's own text or
in a published scholarly restatement quoting it
with pagination (the bar is stated in the
report's methods note).

| Site | Assignment |
|---|---|
| amri | Mature Harappan, Late Harappan |
| banawali | Early Harappan, Mature Harappan — **contested** |
| harappa | Early Harappan, Mature Harappan, Late Harappan |
| jhukar | Late Harappan |
| kalibangan | Early Harappan, Mature Harappan |
| khirsara | Mature Harappan |
| kunal | Early Harappan |
| lothal | Mature Harappan, Late Harappan |
| mohenjo daro | Mature Harappan, Late Harappan |
| rangpur | Mature Harappan |
| rojdi | Late Harappan |

**Contested list.** banawali: Bisht (1982), the
site report, maps to {Mature Harappan} (its
Period I is named "Pre-Harappan", which has no
mapping-table entry); the *Journal of
Archaeological Science* (2014) archaeobotany
review records Early Harappan levels at
Banawali, mapping to {Early Harappan, Mature
Harappan}. Both determinations are retained in
the assignment record and in Output A; neither
is suppressed, and the hierarchy did not
resolve the contest.

**Blank list.** `OUTSIDE_LABEL_SET` (9):
chagylly, mullali, yalangach (the rows' own
`PN`/`Neo.` values), piklihal, kanispur,
ojiyana, hiregudda, sannarachamma, sheri khan
tarakai. `UNMAPPED_SCHEME_VALUE` (2): shahr i
sokhta, ter kala dheri. `NO_PUBLISHED_DETERMINATION`
(8): desalpur, islam chowki, joenniemi, qasim
bagh, sheri khan tarakai 3, sheri khan tarakai
4, surkotada, tigrana. Per-site bases are in
the assignment report.

**Output A.**
`data/movement/gazetteer_rows_assigned.jsonl`,
SHA-256
`64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4`:
all 36 rows, byte-identical to the pre-act file
in every field except
`program_period_assignment` (verified by an
independent recount: parsed rows equal outside
the assignment field on all 36 rows; 17 rows
carry assignments across the 11 sites).

**Completeness by source (§6.3).** XRONOS: 21
rows, 21 sites, 4 assigned, 1 contested (a site
counted under each source that catalogues it).
CISI Vol. 1 catalogue layer: 11 rows, 11 sites,
9 assigned, 1 contested. CISI Vol. 2 catalogue
layer: 4 rows, 4 sites, 4 assigned, 0 contested.

### 4. Margins verification step

Recomputed over Output A under F031-C10:
**period-eligible sites 8 of 30 with contested
counted** (amri, banawali, harappa, kalibangan,
khirsara, lothal, mohenjo daro, rangpur);
**7 of 30 with contested excluded**. The step
closes at the link-mass floor, as frozen:
in-universe link mass **2 link-eligible sites
and 1 linked pair** against floors of **8
eligible sites and 10 linked pairs**. No
response, matrix, permutation, or Q7 verdict
was computed. **Q7 still fails its link-mass
floors; Q6 remains NOT-YET-TESTABLE; Spec 031's
closures are not amended.**

### 5. Dataset new version

A **new version** of Zenodo record 23300361 was
deposited 2026-10-20 through the release gate
(verdict PASS, 3/3: 2 MATCH, 1 EXTERNAL — the
derived releasable file):
**record 23523454, DOI
`10.5281/zenodo.23523454`**, version 2.0,
concept DOI `10.5281/zenodo.23300360`
unchanged. Files:
`gazetteer_rows_assigned_releasable.jsonl`
(the 21 verified-open rows of Output A;
SHA-256
`1d47eeb58c7cfea6c591f52f3215dac3c78b52ac7bdb058676acb81a33226ef7`;
4 of its 21 sites assigned),
`phase403_gazetteer_assignment_report.md`,
`source_register.json` (unchanged from v1).
The description is plain text (no Markdown),
per the owner's 2026-10-20 order. The existing
version's files were not edited (v1 remains as
deposited; an edit draft accidentally opened
during the deposit flow was discarded
unpublished and verified gone).

### 6. What this outcome does and does not establish

The assignments state what named publications
say about each site's period, mapped under the
frozen rule. **They are finding aids, not
dating evidence** (F039-C15). No study verdict
changed: Q7 still fails its link-mass floors
and in-universe link mass is unchanged at 2
sites / 1 pair (F039-C13); Q6 remains
NOT-YET-TESTABLE. The TwoRains determinations
were used not at all (no TwoRains period
determination meeting DD-039-3 presented in
this act's assembly; the gazetteer's rows cite
Law 2011 for coordinates, which carry no period
determinations), and the Masudpur determinations
remain preserved and unadmitted (DD-039-4).
**Spec 030 Ask 2 remains RESERVED and is
untouched by this outcome.**

### 7. Claim consequences (governed register)

Executed under register 0.7-draft (frozen);
one line per claim, F039-C01…C15.

- **F039-C01** (eligibility gate pass, both
  ways stated): CHECKED at execution — the
  re-computation ran over Output A; counts
  8 (contested counted) / 7 (contested
  excluded) recorded in §4 above. The claim's
  link-mass-floor closure is what the record
  carries; no Q7 verdict issued.
- **F039-C02** (a determination counts only as
  published with a locator): HELD — every
  recorded determination carries a citation
  and locator; unverifiable candidates were
  excluded and their sites left blank.
- **F039-C03** (program-derived assignments =
  0): HELD — no derived assignment exists in
  Output A; every assignment's evidence is a
  published determination.
- **F039-C04** (one record per site, carried
  onto all its rows): HELD — assignments are
  per `program_site_id`, identical on all 17
  carried rows.
- **F039-C05** (coarse labels only, closed
  set): HELD — every recorded label is one of
  Early / Mature / Late Harappan; the script
  fails closed on any other value.
- **F039-C06** (the row is the unit; sources'
  own assertions untouched): HELD — Output A
  is byte-identical to the pre-act file
  outside the assignment field (independent
  recount).
- **F039-C07** (mapping-rule/reviewer pair on
  every assignment): HELD — all 11 assignments
  carry their applied rule ids and the
  reviewer of record.
- **F039-C08** (citation/locator pair per
  determination): HELD — all 27 recorded
  determinations carry citation and locator.
- **F039-C09** (contested determinations
  retained; no suppression, no vote, no
  hierarchy resolution): HELD — banawali
  records both determinations and the
  `contested` flag; the union is recorded,
  not a resolution.
- **F039-C10** (undetermined sites stay null):
  HELD — 19 sites are null in Output A, each
  with a reason code in the report.
- **F039-C11** (the act is confined to the 30
  existing sites): HELD — no site was added;
  the Masudpur determinations were not used.
- **F039-C12** (only releasable rows are
  released): HELD — the Zenodo package holds
  the 21 `verified_open` rows only, staged
  through the release gate (PASS, 3/3).
- **F039-C13** (in-universe link mass
  unchanged): HELD — 2 sites / 1 pair before
  and after; the act moved no link.
- **F039-C14** (restricted determinations
  appear only as citations in any release):
  HELD — the released package contains only
  the 21 verified-open rows; no CISI-derived
  (read-only) row is released, and every
  assignment in the package carries its
  evidence as citations, never as reproduced
  restricted content.
- **F039-C15** (labels are finding aids, not
  dating evidence; no outcome changes): HELD —
  stated on the report, the results record,
  the graph node, and the dataset description;
  Q7 and Q6 stand exactly as before.

### 8. Records

- Results record: `reports/phase403_results.json`;
  report: `reports/phase403_gazetteer_assignment_report.md`.
- Output A: `data/movement/gazetteer_rows_assigned.jsonl`
  (SHA-256 in §3); pre-act pin in §2.
- Dataset new version: Zenodo record 23523454,
  DOI `10.5281/zenodo.23523454` (§5).
- Root LEDGER entry: "Spec 039 (Phase-403)"
  entry added with this record.
- Foundation check (H21) and CI state at the
  record merge: CI at the record merge commit
  (`14d15411`, PR #234) is genuinely 7/7 from
  the run's own job conclusions; the backend
  job log reads 1,484 passed / 20 skipped /
  0 failed. The foundation check was measured
  standalone at that same commit (2026-10-20):
  **40 passed / 0 failed / 8 warnings**,
  unchanged — `reports/foundation_check_report.json`
  regenerated at the commit and committed with
  the completion note that carries this
  correction (the sentence in the pre-merge
  draft of this bullet said the foundation
  figures would be read from the backend job
  log; that log carries the suite counts only,
  so the standalone measurement at the merge
  commit is the figure of record). At the
  freeze merge commit (`05f961fc`) the backend
  job log likewise reads 1,484 passed / 20
  skipped / 0 failed, CI genuinely 7/7.
- Spec 027's, Spec 030's, and Spec 031's
  records are not touched by this completion.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
