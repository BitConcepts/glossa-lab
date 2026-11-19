# Spec 093 Stage 2 — stage record (2026-11-19)

Stage 2 (Channel independence: T201, T202) executed
2026-11-19, commissioned the same day when the owner
lifted the Co-scientist gate that had held this stage
since Stage 1 merged (2026-11-09). Two tasks, one freeze,
four runs of record, one independent audit, one
mechanical adjudication. C093-1's standing is recorded
in §4 in spec.md §5's vocabulary, with the per-field
table on its face. No claim's status, stage, or score
was changed by this stage (C093-13); no ledger, matrix,
or map file is touched by this landing.

## T201 — Channel definition: DONE

Record: `records/t201-channel-definition-2026-11-19.md`
(SHA-256 `deaa5a71…`); grounding counts:
`records/t201-counts-2026-11-19.json`, recomputed from
the pinned files by `tools/spec093/stage2_counts.py`.
The material-context projection μ is defined against G1
§2.1's state as the per-object tuple (site, material
class, artifact type, holding/provenance, find context)
under Stage 1's vocabularies, over the named populations
P-seq (3,085 sequence-bearing records), P-site (966),
and P-join (the Stage 1 join's 179 pairs), with the
bookkeeping feature set bounded to source system,
sign-id scheme, rights status, and crosswalk coverage.
The definition names, on its face, the two bounds the
counts force: material reaches a sequence only as the
data list's recorded value on the joined population (the
T102 register does not cover the data list's values),
and find context is the data list's `area_section` (the
finer `excavation_idno`, 178 distinct values over 179
pairs, is an identifier, not a context class).

## T202 — Freeze, administration, and standing: DONE

Freeze: `records/t202-freeze-v1.md` (SHA-256
`075b5124…`), committed (6a32ed99) before any Stage 2
computation; the tools were committed after it
(226de09d). The freeze's floors decide three fields
before any computation, and the stage records them as
the freeze states them:

- **Material class — NOT ADMINISTERED.** One adjudged
  class (Steatite 176; Clay 1 and Faience 1 under the
  class floor of 10; 1 empty of 179).
- **Artifact type — NOT ADMINISTERED.** One distinct
  value ('seal') on all 3,085 sequence-bearing records;
  the join concurs ('SEAL:S', 179 of 179). No per-object
  recovery question exists.
- **Holding/provenance — NOT ADMINISTERED.** Sequence ∧
  holding copresence in the pinned snapshot is 0; the
  join pairs carry no holding on either side.

Two fields formed and were administered as Spec 089
runs on the study surface, store of record this
directory:

| execution | run id |
|---|---|
| site administration | `study-20261119T190159Z-e493a7` |
| site control battery | `study-20261119T190237Z-02e03b` |
| find-context administration | `study-20261119T190218Z-3b0101` |
| find-context control battery | `study-20261119T190257Z-cdc1e1` |

**Audit.** `tools/spec093/audit_stage2.py` — an
independent implementation that does not import the
runner — recomputed all four executions from the pinned
inputs under the freeze and compared result blocks:
**verdict AGREE** (`records/t202-audit-2026-11-19.json`:
every result block matches the recomputation exactly,
header pins verified against the files in the tree, no
unexpected Stage 2 runs). The mechanical adjudication
is `records/t202-adjudication-2026-11-19.json`
(`tools/spec093/check_stage2.py`, gated on the audit).

**Site — NOT RECOVERED.** Adjudged population 949
(Mohenjo-daro 839, Harappa 110); held out 284. The
frozen predictor scores accuracy 0.8768 — below the
majority rule's 0.8838, which is reported for scale —
balanced accuracy 0.5092, Cohen's κ 0.0297 (per-class
recall: Mohenjo-daro 0.988, Harappa 0.030; confusion
[[248, 3], [32, 1]] over (Mohenjo-daro, Harappa)). The
control battery behaves as registered (200 permutations:
κ max 0.0936, mean 0.0008, 99th percentile 0.0851 < the
0.10 validity ceiling), so the administration is valid,
and the field falls short of the freeze's bar
(κ ≥ 0.80 and balanced accuracy ≥ 0.85) by a wide
margin: site is not computable from the sequence table
plus bookkeeping at anything near recovery strength.

**Find context — NOT YET.** Adjudged population 125
(DKG. (S) 68, DKG. (N) 17, DK- 16, HRB 13, VSA 11); held
out 35. The administration's own numbers are recorded
(accuracy 0.4286 against the majority rule's 0.5714,
balanced accuracy 0.15, κ −0.1309), but the control
battery does not behave as registered: its 99th
percentile κ is 0.1322, at or above the freeze's 0.10
validity ceiling (max 0.1351, mean −0.0077). Under the
freeze's §7 the administration is therefore invalid and
the field takes no verdict from it — the machinery, not
the channel, is what failed, and the battery's values
are the obstruction, named here as C093-6's pattern
requires. No re-administration under this freeze repairs
it (C093-8); a successor attempt is a new freeze, and
none is commissioned by this record.

**The first execution, discarded and disclosed.** The
administration was first executed under the tools as
committed at 226de09d (run ids
`study-20261119T185558Z-bdf67b`,
`study-20261119T185617Z-39e26a`,
`study-20261119T185636Z-849ba1`,
`study-20261119T185656Z-2b5d46`). Its audit returned
DIVERGE on representation, not substance: every
confusion matrix, accuracy, and balanced accuracy
agreed exactly, and every verdict-bearing quantity read
identically under both implementations, but 20 of 200
control-battery κ values differed by at most 8.7e-16
(float summation order in κ's expected-agreement term),
and the auditor read the header pins at the wrong path.
The four records were uncommitted working-tree files;
they were discarded, the tools were repaired to exact
rational arithmetic (commit eacd6f60), and the
re-execution above is the administration of record.
Nothing in the episode moved a verdict: the site's
κ under the first execution was 0.029675907848497322
against the repaired 0.02967590784849668, both orders of
magnitude below the bar, and the find-context battery's
validity reading was identical.

## 4. C093-1's standing

Per-field outcomes: site **NOT RECOVERED**; find
context **NOT YET**; material class, artifact type, and
holding/provenance **NOT ADMINISTERED** at the forcing
counts stated. No field was recovered. Under the
freeze's §9 mapping to spec.md §5's vocabulary (no field
recovered; the unadministered and not-yet set
non-empty), C093-1's standing is:

**INDEPENDENT IN PART** — the material-context channel
stands independent for **site**, the one field the test
administered validly and failed to recover. Find
context, material class, artifact type, and
holding/provenance carry no standing either way from
this stage and may not be cited downstream as channel
data (FR-093-04). In particular, Stage 4's site pass
(T401) proceeds on a field whose independence stands;
Stage 4's material pass (T402) inherits a field with no
standing from this stage, and its own freeze must state
that bound rather than borrow strength this stage did
not establish.

## Verification on this tree

- Ledger gate (`tools/ledger/check_ledger_gate.py`,
  glossa-ci venv): default **29 PASS / 0 FAIL / 1
  NOT-RUN — RESULT: PASS**; `--regen` **32 PASS / 0
  FAIL / 0 NOT-RUN** — the standing profile; this
  landing moves no ledger, matrix, map, or pin.
- The audit and adjudication above are the stage's own
  acceptance machinery (T202's acceptance mode is
  human-as-oracle: the reviewer against the freeze, the
  runs, and the bar — the freeze, the four run records,
  the audit's AGREE verdict, and this record are the
  surface that review reads).

*This does not establish:* that the surviving fields say
anything about any reading — independence is about
projections, and §5's vocabulary is the whole of what
this task may conclude. (T202's line, carried verbatim.)
