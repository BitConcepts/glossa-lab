# Spec 065 / Phase-427 — Outcome record (EXECUTED 2026-10-22 — Class B: S-5 RESOLVED, S-1 STILL BLOCKED)

> ## EXECUTED — 2026-10-22
>
> Executed under the frozen Spec 065 contract
> (freeze digest
> `f50a6e9c45d96fe15e737ee83a46b83c2c7e150e4a29421ccb5ec2be7a428c09`),
> as **Phase-427**, under the owner's
> 2026-10-21 approval of the amendment package
> as written, Item 6 (freeze + OSF + execution).
> The execution gate was satisfied before the
> run: OSF registration **34s9u** was approved
> and API-verified by the parent on 2026-10-22
> (public=true, pending=false, withdrawn=false,
> reviews_state=accepted). Outcome: **headline
> class B — S-5 RESOLVED, S-1 STILL BLOCKED**.
> S-5 resolves on the document itself as
> HEADING ABSENT FROM DOCUMENT; S-1 resolves
> under the frozen blocked arm as STILL
> UNLOCATED — ACQUISITION BLOCKED. No claim
> was recovered, so no intake record arises
> under this execution.

## Headline (spec §7.1 wording, class B form)

"One of Spec 057's two unlocated rows is
resolved on the document itself. S-5: HEADING
ABSENT FROM DOCUMENT (no sub-result; no claim
recovered — the row's evidence is the searched
file's hash and its single judged occurrence),
on the acquired file at SHA-256
77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665.
S-1 remains STILL UNLOCATED — ACQUISITION
BLOCKED: no document was handed over before
the run, no search was run for S-1, and
nothing about the chapter is found or implied.
The unblocking act remains the owner account
act named on S-1's row."

The two rows' outcomes, shown beside the
class as §7 requires: S-1 — STILL UNLOCATED —
ACQUISITION BLOCKED; S-5 — HEADING ABSENT FROM
DOCUMENT. Exactly one outcome per source (§6).

**Fence sentence (§8).** "This act searched
two documents for a heading. It checked
nothing either passage states."

## 1. What was executed

The frozen contract's execution shape (spec
§12), in order. Graph-first build (H15/H23):
experiment script
`backend/scripts/phase427_s1_s5_heading.py`;
graph module
`backend/glossa_lab/experiment_graph_phase427.py`
(node `IndusPhase427S1S5Heading`); registration
in `backend/glossa_lab/experiment_graph.py`;
the registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The run's base was
`main` at
`689a5499` (the merged freeze record's
successor state, including Spec 067's filing
record). The run's own records:
`reports/phase427_results.json` (SHA-256
`b485f75ee655c7e15acd7f95b3125859504481c680aa67fc882657cefa0cee63`)
and `reports/phase427_s1_s5_report.md`
(SHA-256
`bbe655312d78c2ec971d86fceb25200d8240f367c005ad187fa81174c6b50377`)
— both digests derived twice by independent
routes (the `sha256sum` tool and a Python
`hashlib` recomputation, identical), and the
script is deterministic: a second run
reproduced every output (results, report,
extraction artifact) byte-identically. No
external contact of any kind was made in this
run, and Andreas Fuls was not contacted in
any form (§9.6).

## 2. Step 0, gate by gate (all passed; recorded before any per-source row, gate 0.4)

- **0.1 Input integrity — PASS.** Every §2
  repository pin hashes to its freeze-record
  value on the live files: the two held
  cleaned texts (S-1 `1275b795…`, S-5
  `dd584975…`), the two literature registry
  files (S-1 `92e19e6d…`, S-5 `38122256…`),
  and the §2.3 record inputs — Spec 057's
  freeze record `3cc68c37…` (its digest
  recomputes as recorded, `237b923a…`), its
  outcome record `d3ae1325…`, its spec
  `0798d51a…`, its adjudication `04188070…`,
  and the anchors file `df0cf620…`. The two
  extracted-claims files are asserted in the
  freeze's own form (the Spec 038 form): their
  freeze-time hashes are definition constants
  and each entry's facts are asserted on the
  live files — each row's entry carries its
  claim_id, the fingerprint `a4874349…`,
  *untested* status, *created* stage, and its
  recorded `quote_fragment` (S-1 the lowercase
  "positional analysis"; S-5 "Positional
  analysis", sentence case, per the freeze
  correction), and the `merged_into` posture
  as Spec 057 left it: S-5's entry points at
  the canonical record, and the canonical
  record still carries exactly the four
  recorded evidence instances, each with the
  fingerprint and its `merged_into` pointer,
  including Spec 057's dated disposition
  append. Every registry record carries its
  source's original filename, size, and
  `checksum_sha256` as pinned.
- **0.2 Acquired-file assertion (S-5) —
  PASS.** The acquired S-5 file at its §2.2
  local path asserts, on the local file
  before any search: 657,863 bytes, SHA-256
  `77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665`,
  MD5 `36616e20a2c62be106ebf9c3d4093fd6` — the
  pinned values, the MD5 matching the Zenodo
  record's file MD5 exactly. No substitute
  bytes were searched, and the held cleaned
  text was not substituted for the acquired
  document.
- **0.3 S-1 intake determination — the
  blocked arm.** Recorded before any search,
  on evidence re-read first-hand at step 0:
  (a) no append-only intake record
  `intake-S1.json` exists in this spec's
  directory; (b) `PROVENANCE.md` in the
  downloads directory carries **no S-1
  provenance entry** — entry 23 is Hunt/S-5,
  and both S-1 sections state "no provenance
  entry taken" and "no file acquired" (the
  2026-10-21 acquisition-attempt section, and
  the 2026-10-22 follow-up section recording
  that an Oakland ILL portion-copy request
  for the Fuls chapter, pp. 57–90 of *Studies
  on Indus Script* (Karachi, 2020), was placed
  on 2026-10-22 and is pending — nothing
  delivered, nothing intake-pinned); (c) the
  S-1 downloads folder
  (`fuls-studies-on-indus-script-2020/`)
  contains only `BLOCKED.md` — no delivered
  S-1 file exists anywhere in the downloads
  tree. The determination is therefore the
  §4.2 blocked arm, and the S-1 row resolves
  exactly as frozen (§4.1 below). The
  determination is a gate verdict, not an
  outcome.
- **0.4 Order — PASS.** These gate verdicts
  stand before the first per-source row in
  this record and in the results record; no
  document text layer was searched, and no
  passage was read for content, before gates
  0.1–0.3 passed and were recorded.

## 3. The accounting table (§6.1 — exactly two rows, §2.1 order)

| # | Source (citation) | Source claim_id | Document searched (hash) or blocker ref | Locator / occurrence list ref | Outcome | Recovered claim id (intake) or evidence ref |
|---|---|---|---|---|---|---|
| S-1 | Fuls, Andreas. "Ancient Writing and Modern Technologies – Structural Analysis of Numerical Indus Inscriptions." In *Studies on Indus Script* (Mohenjodaro 2020), pp. 57–90. Karachi: National Fund for Mohenjodaro, 2020. | `ancient_writing_and_modern_technologies_51831ac9_statisti_0004` | blocker ref: local research store `downloads/fuls-studies-on-indus-script-2020/BLOCKED.md`; PROVENANCE.md S-1 sections after entry 23 (no provenance entry taken) | — (no search run) | STILL UNLOCATED — ACQUISITION BLOCKED | the blocker record itself (gate 0.3 determination, §2): no intake-S1.json before the run, no delivered S-1 file in the downloads tree, the ILL portion-copy request of 2026-10-22 pending with nothing intake-pinned |
| S-5 | Hunt, Treasure A. *Without Kings or Conquests: The Indus Script Deciphered and a Civilization Reconstructed.* Preprint, FelineMind Behavior Labs; draft posted September 2025. Zenodo, published 6 September 2025, version v1. DOI: 10.5281/zenodo.17066226. | `without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002` | acquired file SHA-256 `77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665` | extraction line 340, PDF page 9 — the single occurrence, listed and judged at §4.2; extraction artifact `extraction-S5.txt`, SHA-256 `74e42f8e3e4af6488c14540dd8c5b32e2cd5eed0cfdc03eaf82a7043dfcc155d` | HEADING ABSENT FROM DOCUMENT | the searched file's SHA-256 `77f10f32…` and the extraction artifact at SHA-256 `74e42f8e…` |

### 4.1 S-1 — STILL UNLOCATED — ACQUISITION BLOCKED (owner account act)

The §4.2 blocked arm, on the gate 0.3
determination recorded at §2. No search was
run for S-1, and no finding about the chapter
is stated or implied by this row; the row's
evidence is the blocker record itself: the
Academia.edu download is gated by a sign-in
wall (`BLOCKED.md`), the owner foreclosed
the account routes on 2026-10-22 (he has no
Academia.edu account), and the fallback
Oakland ILL portion-copy request placed
2026-10-22 is pending with nothing delivered
and nothing intake-pinned. **Unblocking
act:** a copy of the chapter handed over by
the owner (his own download, or a copy
delivered through the fallback
interlibrary-loan route) and pinned by the
append-only intake record `intake-S1.json`
before a later run; an intake appended now
arms a later act, not this one. This
successor contacted no one, created no
account, used no credentials, and sent no
request (§9.6). This outcome is a complete
accounting of the row under the frozen
contract — not an interruption of the run
and not a failure of it (DD-065-6).

### 4.2 S-5 — HEADING ABSENT FROM DOCUMENT

The search Spec 057's §4 step 4 could not
run, run on the acquired file (gate 0.2).
The acquired file's own text layer was
extracted in full from the pinned bytes with
`pdftotext -layout` (the tool and settings of
the Item 6 provenance extraction, whose
figures this extraction reproduces: 2,273
lines, 84,672 bytes) and kept as the run
artifact `extraction-S5.txt` in this
directory (SHA-256 `74e42f8e…`). **Every**
occurrence of "positional analysis"
(case-insensitive) in that text layer —
exactly one, listed here in full, none
pre-filtered:

- **Extraction line 340, PDF page 9:**
  "citadels, administrative quarters,
  fortiﬁed gates, and waterworks. **Positional
  analysis**" — continuing on extraction
  line 341, "shows a clear tripartite
  administrative grammar:". **Judgement under
  §5.1: NOT the heading.** It is a mention
  inside a running sentence: it begins
  mid-line, after "…waterworks.", is
  capitalised only as a sentence start, and
  its sentence runs on to the next line. It
  does not stand alone as a line or running
  head, carries no chapter/appendix numbering
  as a title, and is not a table-of-contents
  entry (the extraction carries no other
  occurrence of the string). Its containing
  section is §5.5 "Governance and Civic
  Authority" (extraction line 336), whose
  "Findings." paragraph the occurrence stands
  in. No heading-form occurrence exists in
  the document, so no passage is delimited
  and no verbatim passage artifact arises.

The row therefore resolves **HEADING ABSENT
FROM DOCUMENT**: a document-level finding
that converts the row's Spec 057 sub-state
from HEADING NOT PRESENT IN HELD TEXT, with
the searched file's hash as its evidence.
**Difference from the held text's posture:**
none in substance — Spec 057 outcome §4.2
recorded one occurrence in the held cleaned
text (line 267, sentence-initial inside a
running paragraph of §5.5, not in heading
form); the acquired document's text layer
carries the same single occurrence, in the
same sentence of the same section, likewise
not in heading form. This successor's
finding rests on the acquired file, not the
held text (DD-065-3). The finding is
document-scoped (§9.7): it states nothing
about any other copy or edition, and nothing
about what the document's passages state.

## 5. Disposition of the heading record (§7.2)

Under class **B**, the record stands exactly
as Spec 057 left it — **superseded-not-retired**.
The disposition was made by appended, dated
note only: a `disposition_spec065` entry
appended to the canonical record
`ancient_writing_and_modern_technologies_51831ac9_statisti_0004`
in its extracted-claims file, recording
S-5's resolution and S-1's blocked posture
and stating that retirement is not available
while S-1 remains unlocated. Spec 057's own
`disposition` entry above it stands unedited,
and no pre-existing field of the record was
altered: removing the appended entry (and
restoring the comma after the Spec 057
disposition) reproduces the pre-act file
byte-identically (pre-act SHA-256
`224d6a2d…`, verified at the act). The
record's status (*untested*) and stage
(*created*) are unchanged. No claim was
recovered under this successor, so the note
names no new claim; Spec 057's two recovered
claims remain the claims the record is
superseded by.

## 6. What this outcome does and does not establish

It establishes the resolution of one of Spec
057's two unlocated rows on the document
itself: the acquired Hunt document — the same
September 2025 draft the original extraction
ran on, its edition relationship established
at the freeze — does not carry the heading
"Statistical finding: positional analysis" in
heading form anywhere in its text layer; its
single occurrence of the words is a running
sentence in §5.5. S-1's row is accounted
under the frozen blocked arm, with the
blocker and the pending ILL route on the
record. The hypothesis F065-C14 is defeated
over the one document actually searched
(S-5), and stands **unjudged as to S-1**,
which was never searched; no wording in this
record presents S-5's row as defeating or
confirming it for S-1. **This does not
establish** anything about what either
document's passages state, any positional
finding, or the truth of any claim in either
source — no passage was checked, no claim
was recovered to check, and no credit
transfers from the program's other positional
records to these rows (§9). It does not
establish that no other edition of the Hunt
preprint carries the heading, and it
establishes nothing at all about the Fuls
chapter, which remains unlocated.

## 7. Claim consequences (governed register)

Executed under register 0.6-draft (frozen);
one line per claim, F065-C01…C15.

- **F065-C01** (an outcome states only the
  resolution of the two rows): HELD — every
  statement in this record is tied to the
  searched document's extraction, the gate
  records, or the blocker record; no
  positional finding is asserted by the
  execution itself.
- **F065-C02** (the record under resolution
  is Spec 057's two SOURCE UNLOCATED rows):
  CHECKED — read and pin-verified at gate
  0.1; the two rows' postures, fingerprint
  `a4874349…`, and sub-states are as frozen.
- **F065-C03** (the source set is fixed by
  Spec 057's record): HELD — exactly S-1 and
  S-5 were accounted; no source was added,
  dropped, or substituted, and identity was
  by claim_id and document_id throughout.
- **F065-C04** (each input is pinned at §2
  by SHA-256): HELD — every live-file pin
  matches at gate 0.1; the extracted-claims
  entries are asserted by their facts under
  the freeze's Spec 038 form, with live
  hashes recorded in the results record.
- **F065-C05** (execution stops before any
  text layer is searched on a step-0 gate
  failure): HELD — gates 0.1–0.4 ran in
  frozen order, before any per-source
  material, and passed; no step-0 closure
  arose.
- **F065-C06** (for each source with a
  document in hand, the document's own text
  layer is searched under §5's rule): HELD —
  S-5's acquired file was searched in full,
  its single occurrence listed with its
  locator and judged; S-1 had no document in
  hand under §4.2, and no held text was
  substituted for either document.
- **F065-C07** (an occurrence anchors a
  passage only in heading form): HELD — the
  single S-5 occurrence is a running-sentence
  mention and anchored nothing; no
  heading-form occurrence was judged a
  non-heading.
- **F065-C08** (each passage found is
  recorded verbatim in a per-source passage
  artifact): HELD, vacuously — no passage was
  found on either row, so no passage artifact
  arises; the extraction artifact stands on
  S-5's row with its SHA-256, re-judgeable
  from the record.
- **F065-C09** (each source receives exactly
  one outcome): HELD — two rows, one outcome
  each from the frozen set (§3).
- **F065-C10** (a passage stating a checkable
  finding is recorded HEADING FOUND with the
  claim recovered): NOT TRIGGERED — no
  heading was found, so neither the recovered
  nor the recorded-empty sub-result arose on
  either row.
- **F065-C11** (each recovered claim enters
  through intake at the created stage): NOT
  TRIGGERED — no claim was recovered under
  this execution; no intake record was
  created, and the claim set is unchanged by
  recovery (the disposition append of §5 is
  the record's only claims-store change).
- **F065-C12** (the headline is exactly one
  §7 class): HELD — class B derived
  mechanically from the two rows' outcomes
  (S-5 resolved, S-1 still blocked), under
  the pre-written §7.1 wording, with the
  outcomes shown beside it.
- **F065-C13** (the heading record retires
  only when both sources resolve): HELD —
  under class B the record stands
  superseded-not-retired exactly as Spec 057
  left it, by appended dated note only (§5).
- **F065-C14** (at least one of the two
  documents carries the heading in heading
  form): DEFEATED over S-5, the one document
  actually searched; UNJUDGED as to S-1,
  which was never searched (§6).
- **F065-C15** (no outcome establishes any
  positional finding): HELD — no positional
  conclusion is drawn, no credit transfers, no
  frozen record was edited (Spec 057's
  directory is untouched), the S-1 fence was
  observed absolutely (no contact, no
  account, no credentials, no request), and
  the absence finding is scoped to the
  searched document at its pinned hash.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 8. Records

- Results: `reports/phase427_results.json`
  (`b485f75e…`); report:
  `reports/phase427_s1_s5_report.md`
  (`bbe65531…`).
- Extraction artifact:
  `specs/065-s1-s5-heading-successor/extraction-S5.txt`
  (`74e42f8e…`) — the acquired file's full
  text layer as extracted from the pinned
  bytes; internal program record.
- Passage artifacts: none — no heading was
  found on either row.
- Intake records: none — no claim was
  recovered (F065-C11 not triggered). There
  is likewise no `intake-S1.json`: its absence
  is the gate 0.3 determination's central fact.
- Disposition append: `disposition_spec065`
  entry on the canonical record in
  `glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json`
  (§5).
- Graph node: `IndusPhase427S1S5Heading`
  (registered and verified by import before
  the run). The node recomputes via the phase
  script only when the acquired file is
  present at its pinned local path; on hosts
  without it (CI) the script would close at
  step 0, so the node serves the committed
  results there rather than re-running on
  substitute bytes.
- Root LEDGER entry: "Spec 065 (Phase-427)"
  entry added with this record.
- Tasks: E2–E5 stand ticked in `tasks.md`
  with this record.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` of this spec
  were **not** edited: they are digest-covered
  sources of the freeze
  (`test_spec065_freeze.py` enforces the
  pins), and the executed-spec form records
  execution here, in `outcome.md`. Spec 057's
  directory and records are untouched.
- Foundation check (H21), run in the
  execution worktree with the two Holdat CSVs
  supplied from the main checkout's gitignored
  downloads (never committed): **40 checks
  passed, 0 failed, 8 warnings** — the
  standing figure, as measured. The committed
  report `reports/foundation_check_report.json`
  is regenerated with this record; its only
  changes are the generation date and the
  extracted-claims store's combined hash,
  which moved because of this execution's own
  disposition append.
- Execution tests:
  `backend/tests/test_spec065_execution.py`
  (4 tests) pass in the run environment, and
  the Spec 065 freeze tests pass except the
  one local-environment failure disclosed
  next.
- Local-environment disclosure: in this VM's
  `glossa-lab` venv, the freeze tests'
  `test_register_integrity` errors with a
  TypeError from that venv's AEE loader
  version (the conftest shim's `strict`
  keyword) — the same pre-existing failure
  Spec 057's outcome record disclosed, on the
  same class of venv mismatch; the frozen
  files are byte-identical to `main`. The
  PR's CI run is the figure of record.
- CI and the landing record: appended below
  after the record PR merges, in the Spec 057
  completion pattern — this section is
  completed by append, not edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 8.1 Landing record (appended 2026-10-22, after merge)

- Record PR: #320 (branch spec-065-execution),
  merged as commit
  d1726cb267651e48cc61ff8e51bef3b433ece0a6.
- CI of record: run 39742670484 on the PR head
  20b9da35 — all seven jobs success by job
  conclusion (Backend tests (pytest), Evidence
  Graph script smoke tests, Indus public
  validation checks, Frontend tests
  (Playwright), Shell wrappers ubuntu-latest /
  macos-latest / windows-latest). Main had not
  advanced beyond the run's base during the
  PR's life, so no merge-in was needed.
- Run digests re-verified on main at the merge
  commit by two routes (git blobs at
  d1726cb2… and the GitHub git-blob API;
  the results record also by the contents raw
  read): reports/phase427_results.json
  b485f75ee655c7e15acd7f95b3125859504481c680aa67fc882657cefa0cee63;
  reports/phase427_s1_s5_report.md
  bbe655312d78c2ec971d86fceb25200d8240f367c005ad187fa81174c6b50377;
  extraction artifact 74e42f8e… (S-5). The §5
  disposition_spec065 entry is present on main
  (form superseded-not-retired; Spec 057's
  disposition entry intact above it; the
  record's claim_status/stage still
  untested/created), and the root LEDGER entry
  is present.
- Foundation check (H21) at the merge commit:
  re-run on the landing checkout at
  d1726cb267651e48cc61ff8e51bef3b433ece0a6
  with the two Holdat CSVs supplied from the
  main checkout's gitignored downloads (never
  committed). Result: 40 checks passed, 0
  failed, 8 warnings — the standing figure,
  as measured at execution and again at the
  merge commit.
- Terminal outcome, restated in the frozen
  §7.1 class B wording: One of Spec 057's two
  unlocated rows is resolved on the document
  itself. S-5: HEADING ABSENT FROM DOCUMENT
  (no sub-result; no claim recovered — the
  row's evidence is the searched file's hash
  and its single judged occurrence), on the
  acquired file at SHA-256
  77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665.
  S-1 remains STILL UNLOCATED — ACQUISITION
  BLOCKED: no document was handed over before
  the run, no search was run for S-1, and
  nothing about the chapter is found or
  implied. The unblocking act remains the
  owner account act named on S-1's row. —
  disposition: superseded-not-retired. This
  act searched two documents for a heading.
  It checked nothing either passage states.
