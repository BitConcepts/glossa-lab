# Spec 026 — Classification Criteria (FROZEN at S1 merge)

> These criteria were written and frozen BEFORE the impact
> register was built. They are keyed to method features only —
> never to whether an original result was welcome. Any later
> reclassification requires a dated amendment appended to this
> file with its reason; silent reclassification is a governance
> violation of this spec.

## Unit of classification

One row per spec (001–025; the duplicated 021 recorded as two
rows) and one row per numbered phase artifact (52–141) present
in the extraction inventory (`working/inventory.json`, 116
items). A phase with no recoverable record in the scoped
locations is classified from its inventory row, not omitted.

## The five classes

**RERUN-REQUIRED** — ALL of: (a) the item produced a verdict or
verdict-bearing estimate; (b) at least one named correction
(C1–C4 below) is specifiable from data already on disk, without
inventing new data, new coders, or a new instrument basis; (c)
applying the correction could materially change the estimate,
the verdict, or the evidentiary status.

- **C1 — margin/interval completion:** the verdict rested on a
  p-value (or an agreement point estimate) alone, and an effect
  estimate + interval are computable from the recorded data, so
  the §4.8 margin rule can adjudicate SUPPORTED vs INCONCLUSIVE.
- **C2 — origin-group collapse:** derivative layers were counted
  as independent corroboration, and a collapsed recomputation
  (each origin group counted once) is possible from recorded
  data.
- **C3 — discriminating-control construction:** a declared
  control was non-discriminating and a discriminating control is
  constructible from recorded data.
- **C4 — rescoring:** complete on-disk records exist from which
  scores/verdicts can be recomputed under the §4.6 taxonomy
  (coding pilots are C4 by definition: rescoring only, never
  re-coding).

**REPRODUCE-ONLY** — the computation is deterministic and its
inputs are on disk with recoverable definitions; replay
establishes what the run shows; no C1–C4 correction applies.

**REINTERPRET-ONLY** — a framework defect is present but no
rerun can cure it: the discriminating data were never collected,
the instrument/coder basis cannot be re-run on the original
footing, or the missing ingredient is independent data that does
not exist. The historical assessment (§8) carries the change.

**UNAFFECTED** — the item already satisfies the framework on
the evidence of its own record (declared discriminating
controls, frozen design, intervals/margins reported, origin
groups sound). The register row cites that evidence.

**NOT-RERUNNABLE** — the original experiment definition,
source, or data cannot be recovered from the record (e.g.
ledger-only summaries of experiments whose artifacts are not in
the repository's scoped locations). Preserve + label; the
assessment states the evidentiary ceiling this imposes.

## Tie-breaking and precedence

1. An item that is INVALID by its own record (control-validity
   failure) is REINTERPRET-ONLY unless a C3 correction is
   constructible from recorded data — INVALID is a property of
   the run, and re-running the same design cannot cure it.
2. SA-line items: H26 governs — no classification may produce a
   rerun whose output could serve as SA-sufficient promotion
   evidence. SA validation items whose design already included
   discriminating held-out controls are judged on their record.
3. PRED-2026 items: at most REPRODUCE-ONLY / REINTERPRET-ONLY /
   UNAFFECTED. No classification produces a scoring rerun.
4. Descriptive/data-layer items (catalogues, coverage audits,
   dossiers, intake packs) with no verdict: UNAFFECTED if their
   record is complete and provenance-sound; REPRODUCE-ONLY if
   their counts are verdict-bearing downstream.
5. Where two classes compete, the register row records both the
   chosen class and the rejected alternative with the reason.
