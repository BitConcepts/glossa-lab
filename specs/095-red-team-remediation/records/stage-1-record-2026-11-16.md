# Spec 095 Stage 1 Record — Corpus Reproducibility (2026-11-16)

Stage 1 (T101–T105) executed 2026-11-16 on the mini-server, in a
fresh full clone of BitConcepts/glossa-lab at base `966f22ba`
(Spec 094 closeout merge), branch
`spec/095-s1-corpus-reproducibility`. Claims addressed: C095-2
(T101–T103), C095-3 (T104), C095-4 (T105).

## T101 — Locate and verify: LOCATED, PIN-VERIFIED

The artifact `firestore_indusarrays_full.jsonl` was located at
`/home/hatch/workspace/custody-search-2026-10-25/` on the programme
VM — the 2026-10-25 custody-search work directory, holding the
transfer parts, the gzip, and the reassembly from which custody
copy 2 was made.

| Candidate | Venue | SHA-256 | Verdict |
|---|---|---|---|
| `firestore_indusarrays_full.jsonl` (1,938,791 B, 3,916 lines) | VM `~/workspace/custody-search-2026-10-25/` | `073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578` | **MATCHES the PR #393 intake pin — the artifact** |
| `payload.gz` (187,609 B) in the same directory | VM custody-search dir | `9e483aeecda236723128c4da50a709f94141749377c6a8f28307b3e2cdedc8d2` | Matches the custody addendum's recorded gzip digest — the transfer form of the same artifact; decompresses to the pin-verified file above |
| `firestore_indusarrays_full.json` (3,282,806 B) | tower-compute archive, `glossa-custody-e8/copies-from-desktop/indusscript-probe-siblings/` | `0a3961ace8eb81dcfa1a29c5866724439c7721407827c4253a6f064a77c534d9` | Matches the intake table for the **sibling .json** — a different file, not the artifact |
| Sibling files `firestore_indusarray_extra.json`, `firestore_missing_texts.json`, `indusscript.har` | same custody siblings dir | (intake-hashed at custody; not the artifact's name or size) | Not candidates for the file of record |

Venues searched read-only, with negative results: whole-home name
(`*indusarrays*`) and exact-size (1,938,791 B) searches on the VM
(workspace and the rest of the home), the mini-server (whole home),
and tower-compute (whole home) — the exact-size search found
exactly one file on the VM (the artifact above) and none elsewhere;
the custody snapshot copies in the goal's
`hidden_files/spec080-migration/transfer/` (database snapshots only;
two frozen records — Spec 053 C2, Spec 054 C2 — already establish no
database copy of the layer exists, and identification rests on the
file); the repo-sweep evac archive, found at
`/home/tpierson/archive/repo-sweep-2026-11-06/repo-sweep-evac-2026-11-06-v3.zip`
on tower-compute (115,145 entries, zero `glossa-corpus` entries —
the sweep did not capture the raw subtree); the Spec 053 WSL evac
tar in the same archive directory (no match); the VM's surviving
Glossa trees (`glossa-corpus`, `glossa-run`, `glossa-lab-s054w`,
the goal workspace). Copy 2's recorded placement (the VM checkout
`~/workspace/glossa-lab/...`) no longer exists on this VM instance;
the custody-search directory preserved the verified copy. No venue
was modified, moved, or deleted.

## T102 — Place read-only and reproduce: COMPLETE

- Placed at the canonical path in this tree,
  `glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl`,
  permissions `0444` (read-only). Post-placement SHA-256 =
  `073a83aa…a578` (the pin). The path is gitignored
  (`glossa-corpus/.gitignore` `sources/`): the placement is a tree
  act recorded here, not a commit; the raw file remains
  restricted-local and uncommitted, as its licensing requires.
- Census through the repo's unmodified V3 loader
  (`indus_corpus_v3.corpus_stats`): **3,916 records / 2,665 unique
  dockeys / 3,137 sequences / 12,494 sign instances**, mean length
  3.98, dockey range [1001, 9905], numeric 12,868 / *NNN 504 —
  the Phase-43 census reproduced exactly.
- Canonical export pin, computed by the phase438 construction
  (sort-keys JSON of source label + sequences-by-dockey, SHA-256)
  two independent ways (the loader module's
  `load_corpus_by_dockey()` and the Route 2 mirror; the two
  sequence mappings are identical): **`e90fd7ce41121529887b51dda11640741c23db94a224e946588628802503c659`** —
  matching the recorded prefix `e90fd7ce41121529`. The full digest
  is recorded here for the first time; prior records carried only
  the prefix.
- Independent corroboration: the Route 2 census tool
  (`tools/route2/route2_verify_census.py`) against the placed file
  — gates V1–V4 ALL PASS (exit 0).
- Counting-basis note: the V3 loader's module docstring carries
  "2,906 unique dockeys"; per the Route 2 recovery record that
  figure is the V1 export's dockey count, and 2,665 (the loader's
  own reconstruction count, above) governs. The docstring was not
  edited in this stage.

## T103 — Spec 053 step 0 re-execution: EXECUTED — INVALID AT GATE 0.1

Executed under the filed execution order
(`t103-execution-order-2026-11-16.md`), instrument
`backend/scripts/phase413_yadav_zipf_controls.py` unmodified,
gates byte-unchanged, step 0 only. Full outputs filed as
`t103-phase413-results-2026-11-16.json` and
`t103-phase413-step0-report-2026-11-16.md`. The frozen outputs in
`reports/` were restored byte-identical after capture (SHA-256
`98ccd10a…` / `e0edac40…`, their pre-run values). No frozen text
was moved.

**Outcome: INVALID at gate 0.1 (input integrity); gates 0.2–0.5
NOT REACHED, in the frozen order.** Pin table from the run:

| §2 input | Pin | Observed at `966f22ba` | Match |
|---|---|---|---|
| `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json` | `904766238d…` | `9dd672d107c98082e12ffaeec11d710bc307322f21b7ea354e7e454ae2599804` | **NO** |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620…` | `df0cf620…` (byte-identical before/after; census 287 anchors / 94 strict) | yes |
| `data/crosswalks/sign_crosswalk_master.csv` | `4ace1a61…` | `4ace1a61…` | yes |
| `backend/glossa_lab/data/mahadevan_parpola_crosswalk.json` | `9ebd7723…` | `9ebd7723…` | yes |
| `outputs/phase43_all.json` | `78a6c219…` | `78a6c219…` | yes |

The claim file's digest moved after the freeze through sanctioned
post-freeze amendments to the same claim file (its history includes
the Spec 054 freeze merge-resolution, both Spec 054 execution
records, and PR #477's dispositions). The frozen pin was NOT
updated — updating it would amend the freeze. Consequences, stated
plainly: the frozen step 0 cannot pass gate 0.1 on current main, so
the instrument never reached gate 0.3 in this re-execution; the
strict corpus's identification and pins stand on T102's
reproduction (loader + Route 2 tool + export pin), not on a
re-executed gate 0.3. Whether a future re-execution proceeds under
an amended freeze is a governance question outside this stage.
The instrument's outputs carry its own frozen constants
(execution_date 2026-10-21, base_commit `3200b7b5…`) because the
instrument is unmodified; the actual execution context is this
record and the execution order.

## T104 — The corpus identity standard: COMPLETE

- Prose standard: `glossa-indus/CORPUS_IDENTITY_STANDARD.md`.
- Machine-readable registry + verification + enforcement + audit:
  `backend/glossa_lab/data/corpus_identity.py` — eight registered
  corpora (strict V3, V1 research export, ICIT export, CISI
  compilation, mayig CISI layer, M77 flat text, site-attributed
  CSV, Holdat downloads layer), each with version, SHA-256 pin,
  source, licensing, census under a named basis, and normalization
  rules. Pins of record: strict corpus = PR #393 intake pin;
  Holdat = Spec 054 arm-2 pin (`62d14d2b…`); the rest were
  established by this stage's measurement of the in-tree files at
  registration and are stated as such in the module.
- Covered loaders fail closed: `indus_corpus_v3`,
  `indus_corpus_firestore`, `indus_corpus_v2`, `indus_cisi`,
  `indus_m77`, `mayig_layer` each enforce the identity pin on
  every load (present-but-different raises `CorpusIdentityError`;
  the V1 loader does not fall back over a failed identity), and
  the V3/V1 loaders expose `load_corpus_verified` entry points
  that also refuse absence and empty results.
- Design reading, stated per the commission: C095-3's falsifier
  turns on a loader executing against a corpus that DIFFERS from
  its identity record; C095-4's absence case takes its behaviour
  from its case definition. The standard therefore makes
  present-but-different a hard load-path refusal, and absence a
  refusal on every verified path while the legacy load paths keep
  their documented absence behaviour (absence is flagged and
  detectable through verification at any time, and is never a
  substitution). In this tree, seven of eight registered corpora
  verify; the Holdat layer correctly refuses as missing (its file
  is held in downloads trees, not in this repo).

## T105 — The twelve-case battery: COMPLETE

`backend/tests/test_spec095_corpus_battery.py` — the twelve cases
of C095-4 as a named suite (`TestTwelveCases.test_01` …
`test_12`), each case's refusal or flag as defined in the suite's
docstring table: (1) missing corpus, (2) wrong content hash,
(3) same-name-different-corpus, (4) empty loader result,
(5) duplicate identifiers, (6) contradictory mappings,
(7) unknown signs, (8) damaged spans, (9) reversed reading order,
(10) partial availability, (11) unauthorized access,
(12) synthetic-presented-as-real; plus the V1 no-fallback refusal,
the registry-completeness tests, and a real-tree leg (runs where
the corpora are placed, skips where they are not) asserting the
T102 census and the full export pin. The suite is CI-shaped: it
needs no corpus files except in the skipping leg.

## Test actuals

- Battery (targeted): `17 passed` (backend, CI venv, this tree).
- Full backend suite (CI invocation from backend/: GPU test files ignored, the phase392 deterministic test (tests/test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed) deselected locally by its plain nodeid, single run, this tree): **2866 passed, 108 skipped, 1 deselected, 0 failed** in 1296s. Local only — CI is authoritative.
- Ruff on all changed files: **All checks passed**.
- Ledger gate (both modes run sequentially on the quiet tree): --all gives 29 PASS / 0 FAIL / 1 NOT-RUN, RESULT: PASS; --regen gives 32 PASS / 0 FAIL / 0 NOT-RUN, RESULT: PASS. The standing profile holds exactly; the regen run produced no in-tree changes.

## Claims discharged

- **C095-2** — locate-first, fail-closed pinnability: T101 (pin
  decides; the one non-matching named candidate was the sibling
  .json and stopped nothing because the pin-matching artifact was
  located), T102 (read-only placement, census + full export pin
  reproduced), T103 (re-execution under a new execution order,
  gates unchanged, outcome filed as its own record — INVALID at
  gate 0.1 for a post-freeze claim-file amendment; no frozen text
  moved).
- **C095-3** — identity of record for every claim-bearing corpus,
  stated in the standard and registry; covered loaders verify and
  fail closed (battery cases 1–4, 10–12 exercise the refusals).
- **C095-4** — the twelve cases as a named CI suite over the
  covered loaders, each case's refusal or flag as defined
  (battery, 17 passed including the twelve).

## Deviations and notes

- The commission's evac-archive path (a VM path) was stale: the
  evac archive lives on tower-compute under `~/archive/`; it was
  searched there, read-only, with a negative result.
- The stage heading in tasks.md still reads "(not commissioned)";
  the five task boxes are ticked. Heading/closeout conventions are
  the parent's, as with Spec 094's stages.
- No venue was modified during the search; the live origin tree on
  the mini-server was never touched; the backend was never
  restarted; the research loop was never run.
