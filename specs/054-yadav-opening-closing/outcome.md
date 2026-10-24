# Spec 054 / Phase-438 — Outcome record (EXECUTED 2026-10-24 — STRICT CORPUS NOT PINNABLE)

> ## EXECUTED — 2026-10-24
>
> Executed under the frozen amended Spec 054
> contract (freeze digest
> `d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57`,
> PR #260 merged at `b40dcfc1`), as
> **Phase-438**, under the owner's execution
> order of 2026-10-24 (08:07 EDT, "Do phase
> 438"), after OSF registration **8spvf** was
> approved and public. Outcome: **STRICT
> CORPUS NOT PINNABLE** — gate G2 (strict
> corpus identification and pin; draft gate
> 0.3) failed on observed values. Gate G1
> passed; gates G3–G5 were not reached. No
> positional quantity was computed in either
> arm, no strong set was produced, and no
> verdict on the amended statement exists.
> The claim `yadav_2009_arxiv_manual_002`
> stands exactly as recorded — strongly
> supported, stage explained, with the
> falsifier the freeze appended to its record
> on 2026-10-23.

## Headline (draft §6 wording, STRICT CORPUS NOT PINNABLE form)

"Spec 054 closed at step 0, gate 0.3: the
strict corpus layer of record could not be
uniquely identified and pinned from the
database as the V3 / Mahadevan-lineage corpus
the Phase-43 battery used (the V3 loader's
data file — the Firestore 'indusarrays' dump
the Phase-43 record names as its corpus's
source — is absent at its path in this tree,
in the main checkout, and in every sibling
tree scanned, so the loader loads zero
records and zero sequences and the layer
cannot be exported or pinned; no database
copy of the layer exists (the programme
database's only Indus text is the synthetic
prototype); and no other layer held is the
corpus the Phase-43 record names (the
site-attributed layer at 5,679 records, the
V1 research export, the mayig CISI layer, the
Holdat downloads layer, and the Shakti layer
are each a different corpus or lineage)). No
positional quantity was computed. This
closure is a statement about runnability, not
about the claim; the claim stands exactly as
recorded, with the falsifier appended at this
spec's freeze."

## What the result means, in plain words

The amended test needed the same corpus the
original Phase-43 counts were computed on —
the program's V3 layer, a reconstruction of
the indusscript.in database in Mahadevan's
sign numbering. That layer's data file is not
on this machine: not in the repository, not
in the program's database, not in any
neighbouring tree. Every other corpus the
program holds was checked and counted, and
each is a different corpus or a different
lineage, so none could be substituted without
changing the question. The honest outcome is
therefore the one the frozen contract wrote
in advance for exactly this case: the run
closes at its own step 0. The claim keeps the
thing this spec was built to give it — a
falsifier on its record that it did not have
before — and its strongly-supported status is
untouched, because no test ran.

## What was executed

Step 0 only (amendment §6 gates, in order),
under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase438_yadav_opening_closing.py`;
graph module
`backend/glossa_lab/experiment_graph_phase438.py`
(node `IndusPhase438YadavOpeningClosing`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`, 513 nodes total).
The script contains the full frozen instrument
— battery NB-1 in both arms, the reappearance
measures under DD-054-5's denominator
discipline, the pooled-overlap label-permutation
null (999 shuffles, seed 44054, nearest-rank
95th percentile), DD-054-2's precedence in the
§5.5 order, and the amendment §9 verdict
wordings — and the step-0 gate machinery; the
gates stopped it before any positional
quantity, as designed. The script was run
twice at the venue and produced byte-identical
records (results JSON SHA-256
`c776b247489562d69d9d95862cf315e723c1dd5aacb8ad4f1ff68e1d02a9acfc`).

Gate G1 passed in full: the claim store after
the append at the freeze's post-append pin
(`938174b0…`), the Phase-43 record, the
positional companion, both crosswalk v1
files, the anchors file, and the recovered
register all recomputed to their freeze §2
values, and the freeze digest re-asserted.
Gate G2's mechanical identification is
recorded in full in `step0-record.md` and in
`reports/phase438_results.json`: the
reference census from the pinned Phase-43
record (3,916 records / 2,665 dockeys / 3,137
sequences / 12,494 sign instances); the
loader file absent at all 9 candidate paths
and the loader loading zero; no database
copy; five other layers censused and each
shown to be a different corpus or lineage.

## The outcome append to the claim's record

As the draft's §9 deliverables prescribe, the
outcome was appended to the record of
`yadav_2009_arxiv_manual_002` as a dated entry
(key `spec054_outcome_append_2026_10_24`,
carrying the headline wording above). The
store's SHA-256 moved from the freeze's
post-append pin `938174b0…` to `21009b4a…` by
exactly that entry. Durability was proven in
a scratch tree at the amendment §7 standard:
regeneration through the fixed generator
preserves the appended entry verbatim (the
generator's carry-over covers
`specNNN_outcome_append_YYYY_MM_DD` keys), the
falsification condition survives verbatim,
and the claim's status (`strongly_supported`)
and stage (`explained`) are untouched.

## What does not exist under this spec

The §9 headline quantities a completed run
would carry — the pinned arm-1 and arm-2
layers and their digests, the four exhibited
strong sets, the per-sign positional tables,
the per-class reappearance counts and the
named TOO THIN / UNMAPPED / CONFLICT
dispositions, the pooled overlap and its null
record, the §5.4 sensitivity — do not exist,
because no arm was counted. This record says
so rather than supplying substitutes. The
amended statement stands untested, exactly as
a step-0 closure leaves it: its falsifier is
on the claim's record and any future run
under this freeze must still pass the same
gates in the same order.

## What this does not establish

- Nothing about Yadav et al. (2010)'s original
  statement, whose sets no surviving record
  exhibits (adjudication §7.2) — and nothing
  about the amended statement either: it was
  not tested.
- Nothing about whether the script encodes
  language, and nothing about any sign's
  meaning or reading (spec §7 limits).
- No movement of the parent claim's recorded
  status in either direction.
- The closure is a statement about the held
  record on this machine at this execution —
  the same observed facts on which Spec 053
  (Phase-413) closed at its gate 0.3 on
  2026-10-21. If the V3 layer is re-acquired
  and pinned, a future execution order under
  this freeze can run the battery; nothing in
  this record pre-judges that run.

## Records

- `reports/phase438_results.json` — the full
  machine record (gates, the identification
  attempt with all censuses, the headline
  wording, the anchors assertion).
- `reports/phase438_report.md` — the report
  under the draft §9 headline rules (the
  falsifier verbatim with its append date,
  the step-0 record, the outcome, the limits).
- `specs/054-yadav-opening-closing/step0-record.md`
  — the step-0 record.
- The dated outcome append on
  `yadav_2009_arxiv_manual_002`'s record
  (above).
- Anchors asserted byte-identical before and
  after (`df0cf620…` at both readings).

## Landing record

Appended at merge (append-only): PR number,
merge commit, CI conclusions, and the
foundation check as measured on the merged
tree.

**Landed 2026-10-24.** Execution PR **#364**,
merged as merge commit
`d8aa41a636900771738de8d7145fe3c515ca2025`.
CI on the PR head (`49f72953`), run
40095871845: **7/7 jobs successful**, read
from the run's own job conclusions — Backend
tests (pytest); Frontend tests (Playwright);
Evidence Graph script smoke tests; Indus
public validation checks; Shell wrappers
(ubuntu-latest, windows-latest, macos-latest).
Foundation check on the merged tree (merge
commit `d8aa41a6`, run 2026-10-24 with the
program's local corpora linked in read-only):
**40 checks passed, 0 failed, 8 warnings** —
the warnings are the standing caveats (site
coverage, sign-numbering crosswalks, the
superseded TB corpus, the Phase-29/30 notes,
torch absence); none touches this spec's
records. Read back from merged `main` by API
after the merge: the machine record (outcome
STRICT CORPUS NOT PINNABLE; G1 PASS, G2 FAIL,
G3–G5 NOT REACHED; battery and decision
null), this outcome record, and the claim
store at `21009b4a…` carrying the dated
outcome append with the claim's status
(strongly supported) and stage (explained)
unchanged and the falsifier verbatim.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
