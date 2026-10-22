# Spec 067 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication input is recorded in
> `adjudication.md` (the owner's approval of
> 2026-10-21, amendment package Item 7 §6).
> The execution tasks for Phase-429 run under
> the frozen contract; execution is
> additionally gated on the OSF registration's
> approval act and a separate execution order.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan,
      and claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the approved Item 7 §6 successor), H13
      (epistemic boundaries stated in spec §7,
      including the string-identity boundary of
      §7.1 and the restricted discipline of
      §7.3), H15/H23 (execution shape is
      graph-first, spec §10), H16 (data from the
      registered sources of record: the pinned
      lineage layer, the pinned merged catalogue
      layer v2, the Phase-130 schema, and the
      pinned Spec 024/059 records), H24 (no
      private correspondence in the repo; the
      restricted material itself never enters
      it).
- [x] **L2 — Claims-first register.**
      `claims.json` (F067-C01…C15) carried from
      Spec 059's recovered freeze register
      (0.8-draft) with the successor's changes
      (DD-067-7's bar adoption in F067-C04,
      DD-067-9's layer-v2 pins in F067-C05, the
      type-fill census in F067-C07/C12).
      Acceptance tests derived twice
      independently per claim; disagreements
      and resolutions recorded in
      `adjudication.md` §3.
- [x] **L3 — AEE lifecycle hooks (FREEZE
      GATE).** Run at the freeze act,
      2026-10-21, under aee 1.5.3:
      after_specify, after_plan, and
      after_tasks over the carried register.
      The gate is the DD-067-14 reading
      (adopting DD-038-10): zero correctness
      failure modes and no claim below the
      0.70 threshold at every hook; the
      residual records are the FR-2.3
      draft-cap records, disclosed in
      `aee/freeze-aee-note.md`.
- [x] **L4 — Freeze.** `freeze.md` finalised;
      `freeze.json` computed over the carried
      register and the finalised freeze texts
      by `build_freeze.py`; freeze tests pin
      the digest replay, the definition
      constants, the register integrity, the
      freeze-hook artifacts, and the cited
      records. DD-067-7 (the gate bar adopted
      openly, carried from DD-059-7), DD-067-8
      (single-test family confirmed),
      DD-067-9 (sources named and pinned,
      layer v2 as a definition constant),
      DD-067-10 (OSF under E-1), DD-067-11
      (the censuses suffice as the join audit),
      DD-067-12 (verdict precedence), DD-067-13
      (phase allocation Phase-429), and
      DD-067-14 (the gate reading) decided at
      the freeze (`adjudication.md` §8).
- [x] **L5 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).
      **Done 2026-10-21:** freeze PR #318 merged
      at `dcfa3af6` (CI run 39721764351, 7 of 7
      jobs success from the run's own
      conclusions); foundation check read-back
      on the merged tree 40 passed / 0 failed /
      8 warnings.
- [x] **L6 — OSF filing record completed**:
      `osf-spec-registration.md` filed at the
      freeze under DD-067-10; its follow-up
      record PR merged on genuine green.
      **Filed 2026-10-21:** registration
      https://osf.io/qsthg/ (draft
      `6ad9918010f1e20a2545f3de`, filed at
      2026-10-22T04:32:02Z), pending approval;
      the approval act is the parent's and no
      execution begins while it stands pending.

## Execution — gated on the freeze, the registration's approval, and a separate order

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
      **Done 2026-10-22:** script
      `backend/scripts/phase429_f1_enlarged_join.py`,
      graph module
      `backend/glossa_lab/experiment_graph_phase429.py`
      (node `IndusPhase429F1EnlargedJoin`),
      registration in
      `backend/glossa_lab/experiment_graph.py`
      verified by import (node present in
      `ATOMIC_NODES`) before the run.
- [x] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): input integrity against the
      freeze pins (layer v2 asserted on the
      local file first); original concordance
      join reproduced exactly (5,679 / 2,895 /
      2 / 2,782) against the vols. 1–2 layer.
      Any failure stops the run as INVALID
      (class named) before any new join is
      built. **Done 2026-10-22: both gates
      PASS; no INVALID class fired.**
- [x] **E3 — Step 0, part 2** (gates 0.3–0.5):
      the object-ID join built through the
      Phase-130 schema against layer v2
      (object identifiers only; string identity
      never a key — F067-C06), validated, and
      censused by resolution class; the
      type-fill census on the newly joined
      objects and the whole joined set, with
      the resulting eligible seal/tablet
      strata; the gate comparison against the
      DD-067-7 bar. A gate failure ends the
      execution here: the censuses and the
      §3.6 closure wording are its complete
      record, unscored. **Done 2026-10-22:
      gate 0.3 PASS (4,676 joined, 82.34%);
      gate 0.4 type-fill census taken; gate
      0.5 PASS against the ≥ 3,465 bar.**
- [x] **E4 — Primary** (spec §4, gate-passed
      only): the frozen Phase-136 flow on the
      enlarged set — eligibility and
      estimability applied mechanically (a
      failure is NOT ESTIMABLE, counts shown,
      no p-value), the CMH test under the
      frozen parameters, the LOSO rerun
      (descriptive), and both covariate
      comparisons (joined vs unjoined;
      original joined set vs added rows).
      **Done 2026-10-22: estimable; CMH
      67.3998, raw p = 0.0001, q = 0.0001, MH
      odds ratio 2.452 [1.965, 3.058]; LOSO
      reported, no site load-bearing; both
      covariate comparisons in the machine
      record.**
- [x] **E5 — Outcome:** the §5 record in the
      pre-written wording for the outcome
      class that fired — results JSON and
      report in Spec 059's form (lineage label,
      gate and type-fill censuses, flow,
      quantities, verdict word, LOSO table,
      covariate comparisons, the scope
      sentence), the appended outcome in this
      directory, the dated replication append
      to `STUDY-SPEC-024/F1`'s record
      (including the "on the joined subset"
      re-statement where §5 provides for it),
      and the LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured;
      row-level products of the merged layer
      restricted-local, named by filename and
      counts only. **Done 2026-10-22: outcome
      REPLICATED; `outcome.md` in this
      directory is the dated replication
      append and carries the §5 re-statement;
      LEDGER entry added; anchors asserted
      byte-identical (`df0cf620…` at both
      readings); foundation check as measured
      40 passed / 0 failed / 8 warnings; the
      per-row census `phase429_join_census.json`
      (5,679 rows) restricted-local, named by
      filename and count only.**

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
