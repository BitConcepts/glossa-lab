# Spec 092 — Tasks

## Stage 0 — Package adoption

- [x] **T001 — Package lands.** spec.md, claims.md, aee-claims.json,
  plan.md, tasks.md, records/ (commission-and-grounding record, T002
  assessment + note) committed as `specs/092-platform-hardening-r4/`
  on `docs/092-r4-draft`. Claims: package-level. Acceptance: **test**
  (the package verification of record: aee-claims.json parses;
  claims.md and aee-claims.json carry the same 14 claim ids; every
  claim has a falsifier and a DNE line; the grounding record's
  mechanism statements are reproducible from the repo at the
  package's base commit).
  *This does not establish:* that the package is approved — only
  that it is complete and internally consistent.
- [x] **T002 — AEE verification of the claims.** The C092 bundle run
  through the pinned assessor (aee 1.5.3, CI-faithful venv):
  `aee validate` and `aee assess --no-ledger`, outcome recorded
  verbatim in `records/t002-note.md` with the assessment JSON at
  `records/t002-aee-assessment.json`. Acceptance: **test** (the
  assessor ran and its outcome is recorded verbatim).
  *This does not establish:* claim quality — a draft-stage outcome is
  the expected reading for a bundle on one asserted source; the
  owner's approval is the human act (T003).
- [x] **T003 — Owner block approval.** The owner ratifies the package
  as a block: spec, 14 claims, plan, and decisions D-092-1..4 —
  including the D-092-1 key-custody selection, which is part of this
  act, not a later one. Acceptance: **human-as-oracle** (the owner).
  *This does not establish:* approval of any later stage's output —
  each lands on its own evidence.
- [x] **T004 — Adoption intake + generated-layer regeneration.**
  After T003: (a) record the pre-append gate run; (b) append the C092
  bundle through `tools/ledger/import_bundle.py --spec
  specs/092-platform-hardening-r4 --date <adoption date>` — the only
  sanctioned path, never a hand-edit; (c) regenerate the generated
  layers over the grown ledger and republish through
  `tools/ledger/gated_publish.py`; (d) the bundle-reconciliation test
  passes and the gate's summaries on the final tree are recorded.
  Claims: package-level. Acceptance: **test** (gate summaries +
  reconciliation test in the adoption record).
  *This does not establish:* any C092 claim — the build stages
  discharge them.

## Stage 1 — Credential encryption at rest (PR: feat/092-s1-credential-encryption)

- [x] **T101 — Store format v2 + key loading.** The registered
  credential set; the v2 envelope for credential entries under the
  D-092-1 construction; the single key loader with its named failure
  modes; `_load_keys` decrypting inside the store functions;
  non-credential entries byte-identical to v1. Claims: C092-1,
  C092-2, C092-3 (construction side). Acceptance: **test** (the
  attack battery: byte sweep over a configured fixture store for
  every stored value; data-dir-only decryption attempt; key-absence
  sweep over the data dir and the repo tree).
  *This does not establish:* that a live store has migrated — that is
  T102's mechanism and T104's act.
- [x] **T102 — Legacy migration + verified save path.** First-load
  migration of v1 credential entries, re-save through the
  temp + fsync + rename + read-back construction implemented in the
  store module, post-migration re-read comparison, failure leaves
  the original byte-untouched and named; the database-init reader's
  skip-with-logged-reason tolerance. Claims: C092-4, C092-7 (store
  leg), C092-3 (migration-failure side). Acceptance: **test**
  (legacy fixtures value-identical before/after; denied-write and
  missing-key fixtures leave the original file's bytes unchanged).
  *This does not establish:* the library form of the write
  construction — Stage 2 lifts it and re-proves this leg.
- [x] **T103 — Contract preservation.** The consumer-facing battery
  run identically against v1 and v2 stores: masked GET shape, PUT
  semantics incl. the env side effect, `get_key` resolution order
  and placeholder filtering, the Graph save/disconnect path, the
  schedulers' toggles. No consumer module's diff. Claims: C092-5,
  C092-3 (surface side). Acceptance: **test**.
  *This does not establish:* consumer security — only that their
  contract did not move.
- [ ] **T104 — Live deployment + migration proof.** The stage deploys
  to the desktop install through the gatekeeper; the stage record
  carries the live store's key-name census (names and counts, never
  values) before and after migration and the post-restart backend
  health identity check. Claims: C092-4 (live leg), C092-1 (live
  leg). Acceptance: **gate** (the census proof in the stage record;
  the stage does not close on fixtures alone).
  *This does not establish:* anything about installs other than the
  one production store — there are none.

## Stage 2 — The verified-write library (PR: feat/092-s2-verified-write)

- [ ] **T201 — The library module.** The safe-write contract as a
  supported `backend/glossa_lab/` module: temp + fsync + atomic
  rename + directory fsync + read-back hash, the bounded retry
  ladder with fresh-subprocess attempts, empty-content refusal,
  parents never created, one typed error. Claims: C092-6, C092-7
  (library leg). Acceptance: **test** (round-trip and
  byte-preservation unit tests, incl. the rename-failure fixture).
  *This does not establish:* adoption anywhere — that is T203.
- [ ] **T202 — Fault-injection battery in CI.** The observed failure
  classes seeded by injection (denied open, 0-byte land, short
  write, missing parent, non-directory parent), each asserting the
  typed error with the target preserved, running inside the backend
  suite CI already runs. Claims: C092-8. Acceptance: **test** (the
  battery's CI job conclusions on the stage PR).
  *This does not establish:* that real waves equal the seeds — the
  claim covers the observed classes, named as such.
- [ ] **T203 — Store refactor + writer census.** The settings save
  path re-pointed at the library and Stage 1's in-module construction
  deleted; C092-7 re-proven on the library path with Stage 1's
  fixtures unchanged; the spec's store writers registered for the
  gate's V9 census, with the gate's full and --regen summaries
  recorded verbatim on the final tree. Claims: C092-7 (re-proof),
  C092-13. Acceptance: **test** (re-proof) + **gate** (the census
  output).
  *This does not establish:* adoption by writers outside this spec's
  surface — the census names this spec's writers; wider adoption is
  later work under the census's own discipline.

## Stage 3 — The test-harness remainder (PRs per leg: feat/092-s3-<leg>)

- [ ] **T301 — Tray teardown: reproduce, root-cause, fix.** The ERROR
  reproduced on demand; the mechanism stated in the stage record
  with the reproduction as evidence; the fix landed at the source
  (fixture/connection lifecycle). Claims: C092-9 (mechanism leg).
  Acceptance: **test** (the reproduction fails before the fix and
  cannot be produced after it, over the repetition battery the
  record states).
  *This does not establish:* discharge — the five named runs are
  T302.
- [ ] **T302 — Tray discharge + shape amendment.** Five consecutive
  full-suite runs, named by run id, with zero tray teardown ERRORs;
  on discharge, the run-defs §5 amendment act recording the
  mechanism and the fixing stage (D-092-3). Claims: C092-9
  (discharge leg). Acceptance: **gate** (the five named runs and the
  amendment landing through the definitions path).
  *This does not establish:* that no teardown flake of another family
  exists — only this family's closure, on the stated bar.
- [ ] **T303 — In-tree rewrites eliminated.** The rewriting tests
  censused from a full run's S4 manifest; each moved to isolated
  inputs or temp-tree asserted outputs; the repo-root `outputs/`
  writer dispositioned; the clean-tree guard removed; a full-suite
  light record whose manifest is empty and whose guard-skip count is
  zero. Claims: C092-10. Acceptance: **test** (post-run `git status`
  under the watched roots, from the run's own record).
  *This does not establish:* that the manifest machinery retires — it
  remains the detection instrument; what retires is the routine
  restore.
- [ ] **T304 — phase392 profile + registered outcome.** The stall
  profiled on the VM, the profile artifact filed with the stage
  record; D-092-4's branch applied: a pathology fixed and in-budget
  local completion proven, or the environment-scoped deselection
  registered and wired into the suite-runner configuration with CI
  named authoritative. Claims: C092-11. Acceptance: **test**
  (a local full-suite enumeration after the leg that neither stalls
  nor hand-deselects).
  *This does not establish:* that the test is fast — only that its
  cost is evidenced and its handling is machinery.
- [ ] **T305 — Notifications ERROR battery.** 50 standalone
  repetitions of the notifications module plus 3 full-suite-order
  runs, outcomes recorded; on reproduction, classification and (if a
  defect) a fix under T301's pattern; on no reproduction, the
  UNREPRODUCED closure record with its automatic-reopening term.
  Claims: C092-12. Acceptance: **test** (the battery's records).
  *This does not establish:* that the test is correct — only that
  its error state is no longer unclassified.

## Closeout

- [ ] **T401 — Closeout record.** Per-claim dispositions C092-1..14
  at stage-evidence strength with stage/PR pointers; the standing
  gate profile restated verbatim from the gate's own output on the
  final tree; C092-14 verified by diff census over the spec's stage
  branches; anything undischarged named with its reason. Claims:
  C092-13, C092-14 (final form). Acceptance: **gate** (the closeout
  PR's CI + checker, parent-run).
  *This does not establish:* the claims beyond their stage evidence —
  the record states each at exactly the strength its stage earned.
