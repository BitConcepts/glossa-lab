# Census evidence snapshot — Spec 087

A self-contained copy of the numbers Spec 087 stands on, so
the spec package can be read and gated without the audit
folder. Every table below is copied from the evidence of
record; nothing here is recomputed. Where the audit and the
census differ in framing, the census (the deeper instrument)
governs and the difference is noted.

**Provenance for the whole file.** System-coupling audit,
2026-11-02: `AUDIT.md` (findings F1–F10 and the S1–S6 plan)
and `CENSUS.md` (repo census, Appendix A classifying all 517
nodes), held in the goal workspace at
`hidden_files/system-coupling-2026-11-02/`, plus the live read
`live-atomic-census.json` from the same folder. Repo state:
`BitConcepts/glossa-lab` at `415a1576` (main, 2026-11-02).
Census method: static AST/regex extraction over
`backend/glossa_lab/experiment_graph*.py` plus a runtime
import of `ATOMIC_NODES` in the CI-faithful venv.

## Table 1 — The 517-node registry by class

| Class | Count | Meaning |
|---|---|---|
| Registered node types (`ATOMIC_NODES`) | **517** | Runtime count. 522 definition instances collapse to 517 dict entries (3 shadowed duplicates + 2 double-counted by one module's internal composition). |
| GENERIC | **90** | Mechanism is domain-free; domain content, if any, arrives via ports/params. |
| DOMAIN | **427** | Id, name, or category carries Indus / CISI / a named language, scholar, sign, or artefact (census §4.1 rule). |
| — of which WRAPPER | **359** | No input ports, empty params schema; the node's function runs one frozen phase script or reads one fixed report file. The node *is* the study. |
| — of which PARTIAL | **68** | Real ports and/or params exist, but the scholar/sign/language choice is fixed in code. The genericization candidates. |

Supporting counts (same sources):

- Core nodes defined in `experiment_graph.py` itself: **42**
  (41 inline + `ResearchLoopRunner`); of those, 39 GENERIC and
  3 DOMAIN (the CGSA loaders: `CanonicalSignLoader`,
  `ClusterMapper`, `StructuralTemplateAnalyzer`).
- Plugin modules: **144** `experiment_graph_*.py` files,
  hard-imported by name, contributing **475** distinct ids;
  every import sits in a try/except that logs only a warning
  on failure (the silent-shrink mechanism, finding F1).
- Categories: **66**; the largest, "Indus Decipherment",
  holds **319**.
- Parameter surface: **399** of 517 nodes have an empty
  `params_schema`; **382** have no input ports; **360** have
  neither.
- Palette: the Experiment Builder palette *is* the registry —
  `ExperimentBuilderView` fetches `GET /experiment-graphs/catalog`
  live, so palette-only and registry-only ids are both zero
  (census §2). The palette defects are the silent failure
  handler (F5), not drift.

## Table 2 — The live working set: 36 atomicIds across 27 graphs

All 27 experiments are registered as graphs (repo
`backend/glossa_lab/experiments/graphs/` and live), 189 node
instances, **zero dangling atomic references**. The
`_archive/` folder holds 130 further graph JSONs — archived,
out of this spec's scope.

*Provenance: `live-atomic-census.json` (live read, 2026-11-02);
graph-file verification in census §5.*

| atomicId | instances | atomicId | instances |
|---|---|---|---|
| JSONExport | 26 | DirectionNormalizer | 2 |
| Merger | 22 | CorpusSplitter | 2 |
| BuiltinCorpus | 19 | LMBuilder | 2 |
| SADecipher | 13 | TokenFilter | 2 |
| ConsistencyScorer | 13 | CipherConstructor | 1 |
| FreqCounter | 13 | AnchorConvergenceBenchmark | 1 |
| BuiltinLM | 11 | CanonicalSignLoader | 1 |
| EntropyCalc | 8 | ClusterMapper | 1 |
| PositionalProfiler | 7 | StructuralTemplateAnalyzer | 1 |
| ZipfFitter | 6 | StaticValue | 1 |
| SAMultiComparison | 6 | KalyanCrossValidation | 1 |
| NgramCounter | 5 | DravidianSyllableLM | 1 |
| ShuffleControl | 3 | IndusAnchorSetSyllable | 1 |
| SubExperiment | 3 | Clusterer | 1 |
| WritingSystemClassifier | 3 | PermutationTest | 1 |
| M77InscriptionLoader | 3 | MeluhhaCooccurrenceCheck | 1 |
| CorpusReader | 3 | PassResult | 1 |
| KLDivergence | 3 | BeamDecipher | 1 |

Notes carried from the audit (F4): 481 registered node types
are used by **no** live graph; none of the 359 wrappers is in
any live graph. The domain-flavoured ids in live use are
`M77InscriptionLoader`, `CanonicalSignLoader`,
`KalyanCrossValidation`, `DravidianSyllableLM`,
`IndusAnchorSetSyllable`, `MeluhhaCooccurrenceCheck`,
`WritingSystemClassifier` (the audit's list of seven); the
census's §4.1 rule additionally classes `ClusterMapper` and
`StructuralTemplateAnalyzer` as DOMAIN among the live 36 —
the difference is the classification rule's treatment of the
CGSA core loaders, and Stage S3's triage list is built from
the census rule so both lists are covered.

## Table 3 — The manuals' node reference vs the registry

*Provenance: census §7 (verified name-by-name against the 517
runtime ids), audit finding F7.*

`docs/user-manual.md` §"Node Reference" lists **21** node
names. **10 do not exist in the registry:**

1. CorpusLoader
2. EntropyAnalyzer
3. MappingInference
4. AnchorInjector
5. ConsistencyEvaluator
6. AnchorAccuracyEvaluator
7. RandomBaselineComparator
8. JSONReportWriter
9. MarkdownReportWriter
10. PDFReportWriter

The 11 names that do exist are **2.1%** of the 517-node
palette. HelpView's "Complete Node Reference" documents the
same stale set (the same 10 phantoms). `docs/USER_GUIDE.md`
lists **8** "active graph experiments" against **27** graph
files on disk, and describes the Study Builder's separate
node-type system where a reader would expect the Experiment
Builder palette (census §2.3 — the two systems are easily
confused in the docs). The user-manual's own example pipeline
is drawn with phantom nodes (CorpusLoader → MappingInference
→ ConsistencyEvaluator → JSONReportWriter).

## Table 4 — The 3 shadowed classes

*Provenance: census §1.3; audit finding F2.*

| Node id | Dead definition (shadowed) | Live definition (wins) |
|---|---|---|
| `IndusPhase254SemanticConstraint` | `experiment_graph_phase248_253.py:120` | `experiment_graph_phase_misc_gaps.py:158` |
| `IndusPhase255CommodityPhonemes` | `experiment_graph_phase248_253.py:137` | `experiment_graph_phase_misc_gaps.py:167` |
| `IndusPhase256LEExtension` | `experiment_graph_phase248_253.py:154` | `experiment_graph_phase_misc_gaps.py:176` |

Both modules are imported; insertion is dict assignment, so
the later import (misc_gaps) silently overwrites the earlier
(phase248_253). Whether the pairs are functionally equivalent
is **undetermined** (census open question 1) — Stage S1
determines it by diffing behaviour before deleting anything.

## Table 5 — Log-surface state

*Provenance: census §6; audit finding F6.*

| Surface | State |
|---|---|
| Backend application logging (`log_setup.py`, structured JSON, UTC, rotating `glossa.log` 10 MB × 5) | Working |
| `GET /terminal/log`, `GET /terminal/log/stream` (SSE), `POST /terminal/log/purge`, `POST /terminal/log/frontend` | Working endpoints |
| In-app log viewer | **Gone** — Spec 081 removed the bottom panel; the `api.ts` wrappers (`getLog`, `getLogStreamUrl`, `purgeLog`) are referenced by no component; the manuals still describe a Logs panel |
| DB records: `jobs` / `job_results`, `phase_actions`, `notification_log`, `research_loop_state` | Working; surfaced piecemeal (Jobs view) |
| Cloud append-only audit log (edge D1 `audit_log`) | Working; surfaced in the admin dashboard |
| Events bus (`api/events.py`) | In-memory only, **never persisted**; events with no live subscriber are lost (slow subscribers drop on `QueueFull`). Disposition is Spec 087 decision D2 |
| Manual-work data (live desktop DB) | Intact (F8): discovery triage 33 saved / 10 reviewed / 35 dismissed of 905; 104 anchor sets; 18 jobs, all completed; 1,230 reports; foundation PASS |

## Open questions the census carried (for the stage records)

1. Shadowed pairs' functional equivalence — Stage S1 answers.
2. Whether the desktop production install's registry also
   holds all 517 (registration failures are warnings only) —
   Stage S1's completeness test answers for CI; the desktop
   count becomes checkable the same way once the test exists.
3. Study Builder UI surface (no dedicated editor component in
   the tree) — noted, not in this spec's scope; the
   `node_registry.py` naming collision is in scope (decision
   D5 in spec.md).
