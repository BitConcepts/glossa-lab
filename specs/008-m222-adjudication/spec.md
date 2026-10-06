# Spec 008 — Phase-110: M222 / 'kur' Adjudication + OSF Registry Link

**Status:** Proposed 2026-10-06 on `feat/phase110-m222-adjudication`
(from main 14a91a72). Owner-directed follow-through on the one item
Phase-109 (spec 007) left flagged rather than resolved, plus a
documentation link to the programme's new OSF provenance registry.

**Phase-numbering note:** ledger-sequence **Phase-110** (107 =
Phase-52 v2, spec 005; 108 = provenance audit, spec 006; 109 =
follow-through, spec 007). Legacy files from an earlier era carry
colliding numbers (`backend/scripts/phase110_targeted_sa_unknown.py`,
`experiment_graph_phase110_115.py`); they are append-only history,
NOT renamed or reused. New artifacts carry distinct names
(`phase110_m222_*`) and new graph node IDs, per the spec-005/006/007
precedent.

## Context — the flagged tension

Phase-109 Step 1(b) restored 112 pre-staging readings. 109 of them
restore the value `kur` at LOW, from **Phase-111 allograph
resolution**: each entry's basis states, verbatim, "Phase-111
allograph resolution: positional profile L1=0.000 matches M222
('kur', MEDIUM)" — i.e. the value was inherited from M222 at a time
when M222's own reading was `kur`. But M222 itself was in the
staging cohort, and Phase-109 Step 1(a) KEPT M222 at `min`/MEDIUM
on crosswalk v2.1 support (Phase-71 EXTENDED_MAP attribution to
Parpola 1994 App. B). The Phase-109 ledger entry flagged this
verbatim: "the restored basis states the derivation; the tension
is in the record itself." The owner directed that the tension be
adjudicated, not left flagged.

## Part A — Dossier (evidence assembly; touches nothing)

Artifact: `reports/phase110_m222_dossier.json` + short summary
`reports/phase110_m222_summary.md`. The dossier reconstructs, from
in-repo artifacts only, quoting them rather than paraphrasing:

1. **What Phase-111 claimed and how it worked mechanically** —
   `backend/scripts/phase111_allograph_resolution.py`, its recorded
   run `outputs/phase111_allograph_resolution.json`, and a
   recomputation of the positional profiles from the Holdat corpus
   using the script's own functions. Specifically: what reference
   set the profiles were matched against, what M222's role was, and
   whether the 109 `kur` values are (i) literal phonetic readings
   inherited from an M222=`kur` premise, (ii) a class label anchored
   on a cluster/profile rather than on M222's value, or (iii)
   something else the artifacts say. The Phase-132 validation note
   (anchors-file `_phase132_note` and per-entry notes) is part of
   this record and must be quoted.
2. **M222=`min` with equal rigor** — the current anchor entry, the
   crosswalk v2.1 entry and its `evidence` field
   (`backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json`),
   the Phase-71 EXTENDED_MAP source line
   (`backend/scripts/phase71_crosswalk_complete.py`), the Phase-87
   record of M222=`kur` (`outputs/phase87_anchor_sprint_120.json`;
   May-2026 backup anchors), and the Phase-109 Step 1(a) retention
   decision.
3. **Verdict** — whether a genuine contradiction exists between the
   109 entries' recorded bases and M222's standing sourced record,
   or whether the derivations are independent.

## Pre-registered decision rule (binding; fixed BEFORE any entry is touched)

> A sign's own directly-sourced reading outranks a class/profile
> inference anchored on that same sign; a derived value may not
> cite as its basis a premise that the anchor sign's own sourced
> record contradicts.

### Disposition branches (exactly one applies, per the dossier verdict)

- **Branch 1 — genuine dependence on a contradicted premise.** If
  the 109 `kur` values genuinely depend on the premise M222=`kur`
  (contradicted by M222's standing sourced record `min`): annotate
  each affected entry (dated Phase-110 annotation) restating its
  basis honestly — a Phase-111 class assignment whose M222 anchor
  premise is superseded by M222's sourced reading — and set
  `validation_status` to `premise_superseded`. Values/tiers change
  ONLY if the dossier shows the Phase-111 priors assigned `kur`
  **purely** as that premise's inheritance; in that case demote
  each affected entry to CANDIDATE with the annotation explaining
  why. Every change goes in the change register (below).
- **Branch 2 — no genuine dependence.** If the dossier shows the
  Phase-111 derivation is a class label independent of M222's own
  value: annotate M222 and the cohort entries documenting the two
  independent derivations and why both stand; no value/tier
  changes.
- **Branch 3 — indeterminate.** If the dossier is genuinely
  indeterminate from in-repo evidence: annotate the indeterminacy
  on M222 and the cohort; change nothing else. An honest
  non-decision beats a forced one.

### Cohorts (mechanical definitions; the dossier verifies each membership)

- **Cohort A (the 109):** the Phase-109 change register's Step-1
  `restore` entries whose restored reading is `kur`
  (`reports/phase109_change_register.json`). Verified mechanically
  to equal the set of current entries with reading `kur`, tier LOW,
  and a basis beginning "Phase-111 allograph resolution".
- **Cohort B:** current `kur` entries with a Phase-111 basis at
  CANDIDATE whose full record shows no derivation other than the
  Phase-111/120/132 lineage (expected: M256, M307). Same derivation
  as Cohort A and already at the Branch-1 destination tier: under
  Branch 1 they receive the same annotation + status, with no tier
  change. (Disclosed extension of the tasking's "the 109": the rule
  targets the derivation, and leaving two identically-derived
  entries unmarked would falsify the register.)
- **Cohort C:** current `kur` entries with a Phase-111 basis at
  CANDIDATE whose record ALSO carries an independent, non-Phase-111
  derivation (expected: M157, M400 — Phase-252 M427 allograph,
  Daggumati & Revesz 2021, with DEDR 1638). Under any branch they
  receive an annotation documenting which leg stands and which is
  superseded; no status, no tier change — their value does not rest
  solely on the M222 premise.

- **M222 itself:** gains a dated `phase110_annotation` recording
  the adjudication outcome and the dossier citation, under every
  branch. Its reading and tier are NOT re-tried in this package
  (see Assumptions).

## Addendum (2026-10-06, after dossier assembly, BEFORE apply)

The dossier's full-entry inspection of the four CANDIDATE
`kur` entries (M157, M256, M307, M400) found the Cohort-C
expectation above **wrong on the evidence**, and this addendum
revises the disposition before anything is applied:

- ALL FOUR entries carry a Phase-252 `upgrade_basis` — but none
  of them derives the value `kur`. M157/M307/M400 claim allograph
  status under **M427, whose recorded reading is 'en'** (r=0.953 /
  0.979 / 0.967); M256 claims allograph status under **M375,
  recorded reading 'taṇ'** (r=1.000). An allograph of M427 would
  read 'en', not 'kur': the Phase-252 legs are *competing,
  never-adopted* derivations of different values, not independent
  support for `kur`. (Phase-109's machinery summary had described
  M157/M400's Phase-252 record as an independent leg without
  noting that it supports a different value.)
- All four also carry the June-2026 quality-audit note verbatim:
  "Downgraded HIGH→CANDIDATE on 2026-06-07: reading 'kur' shared
  by 15 signs (bulk assignment)".
- **Revised disposition:** Cohort C is EMPTY. All four CANDIDATE
  entries rest, for the value `kur`, solely on the Phase-111
  M222 premise, and join Cohort B's disposition under Branch 1:
  dated annotation + `validation_status` =
  `premise_superseded`, no tier change (already CANDIDATE). Their
  annotations additionally record that the Phase-252
  `upgrade_basis` supports a different value ('en' / 'taṇ') and
  does not support `kur` — a further incoherence in these
  entries' records, flagged here rather than resolved (resolving
  it would mean re-trying values, which is out of scope).
### Annotation + change-register discipline

- Every changed entry gains a `phase110_annotation` field (dated
  2026-10-06) naming the action, the rule (spec 008 + branch), and
  the dossier citation. **No silent edits**; original `basis`
  strings are never rewritten — annotations are additive.
- Every change is recorded in `reports/phase110_change_register
  .json`, mirroring the Phase-109 format: sign, step, rule, action,
  before/after (reading, confidence, `validation_status`), citations.
- After any tier changes, the anchors file's summary/bookkeeping
  fields (`by_confidence`, `n_*`, `metadata.*_count`,
  `hm_confirmed_count`) are regenerated from the entries (spec 004
  WS3 method) and a `_phase110_note` is added; the regeneration is
  itself a register entry. Entries not named by the cohorts above
  are not modified in any way.

## Part C — OSF provenance registry link (documentation only)

The programme's provenance registry is live at
https://osf.io/ybd65/ (components: `zbh86` literature, `dfrhz`
corpora, `vwa7s` outputs). Add a short "Provenance & source
registry" pointer in `README.md` near the existing citations /
provenance material, and a header note in `CITATIONS.md` pointing
to the OSF registry as the public index (the repo remains
canonical). One or two lines each; no restructuring.

## Assumptions (H13 epistemic boundaries)

- **Standing record:** Phase-109's retention of M222=`min`/MEDIUM
  is the anchor sign's current sourced record. It was applied under
  pre-registered rules and merged by the owner (PR #62). This
  package adjudicates the *derived* entries against that record;
  it does not re-try M222's own value. If M222 is ever
  re-adjudicated, cohort dispositions here would need revisiting —
  that dependency is stated, not hidden.
- **Thinness acknowledged:** M222=`min`'s independent support is a
  single-source, CANDIDATE-confidence crosswalk attribution
  (Parpola 1994 App. B via Phase-71 EXTENDED_MAP) plus a staging-era
  DEDR gloss. The rule in this spec concerns what a derived value
  may *cite as its basis*, not which of `kur`/`min` is ultimately
  true of the hook sign.
- **Corpus:** positional profiles are computed on the Holdat corpus
  as encoded in-repo (`corpora/downloads/external_repos/holdatllc_
  indus/indus_corpus 2.csv`); profile findings are statements about
  that encoding.
- **Adversarial challenge:** a critic could argue the Phase-111
  `kur` strings were always intended as class labels (the Phase-132
  characterization), making Branch 2 correct. The dossier meets
  this head-on: the recorded bases assert phonetic inheritance
  from M222 specifically, and Phase-109 restored them *as readings*
  under that basis; the adjudication governs the record as it
  stands.
- No P1 belief artifact is relied on at LOW confidence; the
  load-bearing artifacts (Phase-111 script + run output, Phase-87
  output, crosswalk v2.1, Phase-109 register) are all in-repo and
  quoted verbatim in the dossier.

## Acceptance

- Dossier + summary artifacts exist and quote their sources.
- Exactly the cohort entries (plus M222's annotation) differ from
  main in the anchors file; every difference is in the change
  register (verified by an automated before/after diff in the apply
  step).
- Foundation check (H21): 0 failures after the anchor changes.
- Backend suite: no regressions against the 609 passed / 9 skipped
  baseline; ruff clean on changed Python.
- Ledger entries (root `LEDGER.md` + `glossa-indus/LEDGER.md`)
  with AI disclosure. PR opened, **NOT merged** — the owner reviews
  all scientific changes.
