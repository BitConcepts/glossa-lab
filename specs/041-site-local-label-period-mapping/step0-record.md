# Spec 041 — Step-0 record (Phase-435 execution)

Execution act under the frozen spec (freeze digest
`fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7`;
OSF registration `w2vkn`, approved 2026-10-23; execution
ordered by the owner's waiting-decisions package approval
of 2026-10-23 20:25 EDT). Step 0 ran 2026-10-23 at the
execution venue (program VM, restricted-local data area).
**Verdict: STEP 0 PASSED — all six gates, in order,
fail-closed.** Construction proceeded.

The corpus layer is the **ICIT-lineage layer (horus84)**.
The sweep's local copy of the layer was absent from the
venue at execution time; the layer file was re-acquired
from its pinned source (`horus84/Computational_Linguistics`,
upstream HEAD `ac44f08c`) and asserted at the frozen pin
before any use. The pin, not the provenance path, is what
gate G0.1 governs, and it held exactly.

## Gates

- **G0.1 — layer pin: PASS.** SHA-256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`
  (1,190,884 bytes), 5,679 rows × 38 fields.
- **G0.2 — population reproduction: PASS.** Eligible sites
  (≥30 inscriptions and ≥100 parsed tokens): Chanhu-daro,
  Dholavira, Harappa, Kalibangan, Lothal, Mohenjo-daro,
  Nausharo. Population 5,410 rows (Chanhu-daro 74,
  Dholavira 238, Harappa 2,717, Kalibangan 212, Lothal 208,
  Mohenjo-daro 1,923, Nausharo 38) — the frozen table
  reproduced exactly.
- **G0.3 — census: PASS.** Headline margins reproduce the
  recorded tables exactly: period informative 2,266 /
  phase informative 2,638 / both 1,788 / union 3,116 /
  neither 2,294 (the 57.6% ceiling). The Phase-139
  covariates file (SHA-256 `a0f0d05a…`, 5,410 rows) agrees
  with the layer's `period`/`phase` values on **every**
  population row (0 mismatches) under the value convention
  below. Census: **78 cells** (one per attested
  (site, field, label) triple), committed with this record
  at `specs/041-site-local-label-period-mapping/step0-census.json`,
  SHA-256
  `b57fb6b1a0aa1e491ba38bf18978eec58c355f3bf833f58298c7516aabeca6be`.
  A secondary census of the full layer found 115 attested
  triples, of which 37 belong to non-population sites and
  are recorded for completeness only.
- **G0.4 — anchors pin: PASS.** SHA-256 `df0cf620…`
  (570,344 bytes) asserted before construction and again
  after; unchanged.
- **G0.5 — source admissibility: PASS.** The classification
  of every source consulted was fixed in the runner before
  extraction (determination sources vs locator aids, per
  spec §3) and is recorded in the runner's
  `SOURCE_CLASSIFICATION` and in the results file. No source
  may be reclassified after its evidence is seen; any
  classification judgment arising during extraction is
  recorded in the coverage report.
- **G0.6 — no-computation fence: PASS.** Step 0 computed
  margins and the census only — no cell value, no placement,
  and no G1 quantity of any kind.

## Value convention and the whitespace finding

The frozen margins and the Phase-139 covariates were both
produced under the Phase-139 loader's convention: `period`
and `phase` values are stripped of leading/trailing
whitespace, and a value is unrecorded iff the stripped form
is `""` or `"-"`. The census applies the same convention;
query marks and span marks internal to a value are carried
verbatim. Seven population rows carry whitespace variants
in the layer: Harappa `1085.1` phase `Stratum II␣`,
`1787.1`/`1787.2` phase `Stratum III␣`, Mohenjo-daro
`3085.1`/`3643.1` period `Late␣`, and Harappa
`1730.1`/`1730.2` phase `␣` (a single space — the two rows
the spec itself describes as "phase is also blank"). Under
a byte-verbatim reading the recorded margins would not
reproduce (phase informative would read 2,640, not the
frozen 2,638); the recorded convention is therefore the
one the frozen tables embody, and it is disclosed here so
no reader mistakes the census's labels for raw bytes.

## What step 0 does not establish

Passing step 0 establishes only that the frozen inputs are
present, pinned, and mutually consistent. It maps nothing;
every cell's value is decided in construction (E3–E5)
under spec §3, and counts under §8 are reported, never
adopted.
