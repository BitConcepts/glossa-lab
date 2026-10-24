# Spec 069 / Phase 432 — Outcome record (EXECUTED 2026-10-22 — ASSET BUILT AND FROZEN)

> ## EXECUTED — 2026-10-22
>
> Executed under the frozen Spec 069 contract
> (freeze digest
> `657b930c9200299c7d540baa8ed51b7a90176bdea9822577e9cb1f4d292f99aa`;
> freeze PR #338 merged at `ba61d9cd`; OSF
> registration r3xqb filed at the freeze,
> pending the owner's approval act at the time
> of the run), as **Phase 432**, in the chain
> order of the owner act that commissioned the
> Hunt chain (freeze, merge, registration,
> execution). Outcome: **ASSET BUILT AND
> FROZEN** — gates A1–A6 all passed, in order,
> before any join. The build record is
> `build-record.md` in this directory; the
> machine record is
> `reports/phase432_results.json`.

## Headline (spec §5 ASSET BUILT AND FROZEN wording, filled from the run)

> "Asset A is built and frozen under Spec 045's
> §§2–3 contract as quoted and executed by Spec
> 069: 187 rows over the full pinned-crosswalk
> sign universe — animal 20, sky_cycle 0,
> object_goods 14, human 25, other 127,
> contested 0, unidentified 1 — entered blind
> from the held published sources, with
> disputes coded by rule and the D-18 input
> recorded as the terminal empty feed. Asset A,
> SHA-256
> `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`,
> is published as this spec's first product and
> is the asserted step-0 input of Spec 070 and
> Spec 071. This does not establish what any
> sign means: the asset records what the
> published lists say a sign depicts, with
> citations."

What this means, in plain words: the
classification the Hunt tests have always
needed now exists. Every one of the 187 signs
in the programme's pinned crosswalk has a row
saying what the published sign lists say it
depicts, where they say it, and how sure the
record is — including the honest gaps: one
sign no governing source identifies (M059),
four signs whose own published labels hedge
(borderline), and a sky class that is empty in
this sign universe under the published labels,
which Spec 071's design meets in its own
pre-registered terms. The asset was built
without looking at any inscription's sign
order, so nothing about where signs sit in
texts could shape what they are recorded as
depicting.

## 1. What was executed

The full frozen contract (spec §§2–3, quoted
from Spec 045), under the graph-first build
(H15/H23): experiment script
`backend/scripts/phase432_asset_a_build.py`;
graph module
`backend/glossa_lab/experiment_graph_phase432.py`
(node `IndusPhase432AssetABuild`); registration
in `backend/glossa_lab/experiment_graph.py`;
the registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). Gates A1–A6 as
recorded in the build record: sources named by
edition (with the digitization's restoration
from the public upstream at commit `ad2f1e2`
recorded, after the programme's downloads copy
was found missing during a concurrent
workspace sweep); the D-18 empty feed
re-asserted; blind double entry with
reconciliation (6 of 187 pass disagreements,
each adjudicated on the record); coverage,
citation, attestation, and freeze gates in
order. The product: `asset-a/` in this
directory — the canonical CSV, its
`asset-a-freeze.json`, and the entry log
`entry-decisions.json`. Anchors asserted
byte-identical before and after. Foundation
check reported in §2 as measured.

## 2. Foundation check (H21), as measured

Run on the execution tree after the phase,
with the two Holdat CSVs copied from the
existing local downloads into the worktree's
local store (the corpus CSV SHA-256
`62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
verified first): **40 checks passed, 0 failed,
8 warnings** — the standing figure. The check
is a standing programme measure; its result
changes no quantity in this record.

## 3. What the outcome does not establish

This build adjudicates no Hunt claim, reads no
corpus, and establishes no gloss or meaning for
any sign. Depiction here is the published
identification layer, not ground truth, and
Spec 037's caution (object-type labels
diverging between compilations in 49% of
matched cases) travels with the asset wherever
it is cited. Spec 045's INVALID closure stands
untouched. Whether the opening signs are the
animal signs, and whether the sky signs gather
at the ends of texts, are Spec 070's and Spec
071's questions, answered by their own frozen
contracts against this digest
(`952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`) —
including, for Spec 071, the open possibility
its design names: a celestial class too thin
to test.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
