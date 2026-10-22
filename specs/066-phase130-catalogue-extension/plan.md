# Spec 066 — Plan

> ## PLAN — FROZEN 2026-10-21
>
> The intake act of amendment-queue Item 7
> (owner-approved 2026-10-21, §4's lawful line
> included), carried into frozen form in
> `spec.md`. Execution is Phase-428, run in the
> same run as the freeze, after the freeze
> merges, under the frozen contract and step
> 0's fail-closed order.

## Shape

1. **Freeze first.** Claims-first register
   (F066-C01…C15), AEE lifecycle hooks under
   the DD-066-10 gate reading (aee 1.5.3),
   freeze digest computed exactly once over the
   recovered register and the finalised freeze
   texts, freeze tests pinning the replay, the
   definition constants, the register integrity,
   the hook artifacts, and the cited records.
   Freeze PR merges only on genuine CI green
   (7 of 7 jobs, from the run's own
   conclusions). No OSF registration is filed
   (DD-066-8).
2. **Execution (Phase-428), graph-first**
   (H15/H23): experiment script
   (`backend/scripts/phase428_catalogue_extension.py`),
   graph module
   (`backend/glossa_lab/experiment_graph_phase428.py`),
   registration in the experiment graph,
   registration verification, then run.
3. **Step 0, fail-closed, in the frozen order**
   (spec §7): gate re-verified on the record
   and quoted; every pin recomputed (two routes
   where committed); candidate sets re-derived
   to the §3 counts; repo cleanliness (no
   portion-derived row-level file in tree or
   index). Any failure stops the execution as
   itself, before any grading.
4. **Grading.** The full census under the
   §5.3 ladder; low-confidence hand-verification
   against the page renders (renders local);
   the seeded stratum (seed 20261021) and its
   cause attribution; the medium-coverage
   determination; the §6 aggregates. All
   row-level working files in the restricted
   local store only.
5. **Halt evaluation** (§5.5): conflict share
   of all graded candidates against 20%, and
   the true-non-identity tripwire. On halt: the
   census reports in full; no index, no pin;
   outcome INTAKE COMPLETE — CATALOGUE
   EXTENSION HALTED.
6. **On pass:** build the merged catalogue
   layer v2 locally (collisions recorded, the
   existing object stands); run the pinned
   Phase-130 validator over the extension
   dataset form locally (license_basis = the
   entry-22 gate, quoted); commit only the §4
   products — extension index under
   `data/intake/`, the aggregate census record
   in `reports/`, the outcome record.
7. **Outcome:** `outcome.md`, the root LEDGER,
   and the phase machine record; local products
   named by filename and row count only, the
   merged layer pinned by hash as definition
   constants; repo cleanliness re-checked
   before the outcome commit; foundation check
   read-back after the outcome lands (40 / 0 /
   8 expected as the standing read-back; it is
   a read-back, not a gate — spec §7).

## Fences carried through every step

Restricted material never enters git or any
external service beyond the §4 line; scans,
renders, the extraction table, and every
extracted source-row field beyond (number +
site section + published type class + grade
class) stay in the restricted local store; the
merged layer file stays restricted-local,
hash-pinned only. No join is run; no F1
quantity is computed; Spec 059's and Spec
024's records are never edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
