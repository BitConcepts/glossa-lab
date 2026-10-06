# Tasks 006 — Anchor Provenance Audit (Phase-108)

## Proposal
- [x] T001 Read AGENTS.md, constitution, governance rules, spec-005 shape
- [x] T002 Survey evidence landscape (anchors file, ledgers, SA artifacts, claims, corpus, crosswalk)
- [x] T003 Create branch `feat/anchor-provenance-audit` from main 6a46809e
- [x] T004 Write specs/006 (spec / plan / tasks) with pre-registered taxonomy + methods

## Step 1 — Evidence extraction
- [x] T010 Build `pipelines/provenance_audit.py` (loaders, trail assembly, SA-lineage tables)
- [x] T011 Unit tests `tests/test_provenance_audit.py`
- [x] T012 Write phase108 scripts + graph module + registration; verify ATOMIC_NODES (H23)
- [x] T013 Run extraction → `reports/phase108_anchor_trails.json`
- [x] T014 Spot-check trails (M267, M047 + 3 random) against raw sources

## Step 2 — Classification
- [x] T020 Pass 1 (programmatic) → draft register
- [x] T021 Hand-review all undecided trails → `reports/phase108_review_decisions.json`
- [x] T022 Finalize → register + summary MD; headline counts (overall / by tier / three-way)

## Step 3 — Subset recomputation
- [ ] T030 Coverage (a): full vs SA-independent H+M (+ sensitivity pair)
- [ ] T031 Phonotactics (b): Phase-58 machinery on the same sets
- [ ] T032 Parpola agreement (c): crosswalk v2.1 method + Phase-159 cross-check
- [ ] T033 Site invariance (d): Phase-69 machinery, full-set replication then subset
- [ ] T034 Aggregate → `reports/phase108_subset_recomputation.json`

## Step 4 — Circularity + downstream impact map
- [ ] T040 Circular chains (pin → agreement → promotion/claim), cited pairs
- [ ] T041 Claims map: 31 extracted claims vs SA-lineage anchors
- [ ] T042 Headline-number map: 161 / 90.96% / 59% source sets + SA-lineage share
- [ ] T043 Foundation-check map: every SA-citing claim text + post-107 status
- [ ] T044 Aggregate → `reports/phase108_impact_map.json` + summary

## Step 5 — Close-out
- [ ] T050 Recommendations section (authored, not executed)
- [ ] T051 Foundation check (0 failures; H21)
- [ ] T052 Full backend test suite (exact counts)
- [ ] T053 Ruff on changed Python files
- [ ] T054 Anchors file hash identical to main (audit-only guarantee)
- [ ] T055 glossa-indus LEDGER Phase-108 entries (per step, AI disclosure)
- [ ] T056 Root LEDGER.md summary entry (AI disclosure)
- [ ] T057 Push branch, open PR (do NOT merge)
