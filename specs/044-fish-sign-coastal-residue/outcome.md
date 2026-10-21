# Spec 044 — Step-0 outcome record (Phase-404)

> ## STEP 0 EXECUTED — 2026-10-21 — TOO THIN
>
> This record is the step-0 outcome record for
> Spec 044 (design D-02), executed as Phase-404
> under the runnable-experiments campaign
> approved by the owner AS WRITTEN on 2026-10-21
> (Wave 3, Group 1: step 0 only — the Asset F
> build). The frozen contract is
> `freeze.md` / `freeze.json` in this directory
> (freeze digest
> `6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f020fcf25691d9c8`);
> its OSF registration **6p9et** is APPROVED +
> PUBLIC, so the execution rule in the freeze
> record is satisfied. The §5 primary test, the
> sensitivities, and the remaining execution
> steps were NOT run — and, the execution having
> closed at gate 0.4, there is no per-sign test
> left to run under this contract (see §3).
>
> **This record is internal under the campaign's
> Roif gate (R-7); it is not a publication.**

## Headline (spec §6, pre-written wording)

**TOO THIN:** "The sign-by-sign residue test
cannot be run as designed: fewer than two fish
signs clear the 30-occurrence floor in the
pinned corpus layer (census: M047 13; M048 157;
M050 17; M052 22; M060 20; M145 3; M147 2). No
per-sign coastal test was computed. The
family-level verdict — partially falsified —
stands exactly as recorded, and the residue
remains open only in the sense this census
states: the surviving record is too thin to
test it sign by sign."

## 1. What was executed

Step 0 only (spec §3, gates 0.1–0.5 in order;
tasks E1–E3), under the graph-first build
(H15/H23): experiment script
`backend/scripts/phase404_fish_coastal_step0.py`;
graph module
`backend/glossa_lab/experiment_graph_phase404.py`
(node `IndusPhase404FishCoastalStep0`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (node present
in `ATOMIC_NODES`). The run's own records:
`reports/phase404_results.json` (the step-0
record) and `reports/phase404_step0_report.md`.
Every spec §2 pin was asserted before any
counting and matched: claim file
`bc22d6f010f800d608d6e3f620fb430b3cf8d3ccd3caadc6a989116fbfd125ed`;
gazetteer
`5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6`;
crosswalk
`9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b`;
anchors
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`,
asserted byte-identical before and after the
run.

## 2. The gates, in order, with observed values

- **Gate 0.1 — PASS.** The layer of record (the
  Holdat corpus file the Phase-45/46/54 scripts
  of record read,
  `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`)
  re-asserted: 593,253 bytes, SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`,
  matching the freeze pin. Population
  reproduction exact: 7,002 sign-token rows;
  1,670 inscriptions over 9 sites (Mohenjo-daro
  606, Harappa 492, Lothal 124, Kalibangan 110,
  Dholavira 106, Chanhu-daro 78, Surkotada 61,
  Banawali 60, Rakhigarhi 33); M047 at 13 tokens
  in 13 inscriptions; the Phase-45 T6 table
  reproduces (coastal-with 2, inland-with 10,
  coastal-without 228, inland-without 1,369;
  Surkotada unclassed in the original script, as
  there) with Fisher's exact two-sided
  p = 0.685272…, the recorded 0.685. Every
  figure was verified by two independent routes
  (Python csv/hashlib and sha256sum/awk counts),
  agreeing exactly.
- **Gate 0.2 — PASS. Asset F built and frozen.**
  Built solely from Parpola's published list
  (Parpola 1994, *Deciphering the Indus Script*,
  sign list fig. 5.1, pp. 70–78) as held by the
  programme in the pinned Mahadevan–Parpola
  crosswalk: 7 members — M047 (Parpola 47, fish
  (plain), `parpola-list-fish`), M048 (48,
  fish-with-roof), M050 (50, fish-with-fins),
  M052 (52, fish-with-trefoil), M060 (60, fish
  (variant; 'badly drawn')), M145 (145, fish
  with two horizontal lines), M147 (147, fish
  (sign-list variant)) — the six non-plain
  members on the `parpola-list-fish-variant`
  basis, each carrying its per-sign locator
  (fig. 5.1 entry, pp. 70–78). Canonical file:
  `asset-f-fish-family.json` in this directory
  (UTF-8, keys sorted, members sorted by
  `sign_key`). **Digest (SHA-256 of the
  canonical bytes with the `digest` field
  excluded):
  `ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`.**
  The digest was verified by two independent
  routes (an independent staging build from the
  pinned crosswalk, byte-identical to the run's
  file; and the consumer-rule recompute over
  the landed file), agreeing exactly. This
  record is the pin source Spec 048's freeze
  fixed for its gate 0.1 (DD-048-9).
  Cross-check (DD-044-5), reported and never a
  membership source: of the claim record's
  named trio (Mahadevan 72, 64, 70), none is an
  Asset F member; of the Phase-43 six
  candidates (267, 72, 65, 59, 60, 70), only 60
  is. The trio and the six are Mahadevan
  numbers in the Phase-43 record's corpus
  numbering, which is not the pinned layer's;
  the divergence is named here and adds and
  removes no member.
- **Gate 0.3 — PASS. Coastal list frozen.**
  Coastal/maritime: **Lothal** and **Dholavira**
  (both members by name, spec §3; Lothal the
  Gulf of Khambhat port town, Dholavira on
  Khadir island in the Rann of Kutch). Inland:
  Banawali, Chanhu-daro, Harappa, Kalibangan,
  Mohenjo-daro, Rakhigarhi, and Surkotada.
  **Contested: Surkotada** — classed inland
  (a fortified town of the Kutch interior, not
  a port) and listed as contested, its
  coastal-zone status being disputed in the
  literature and the original Phase-45 script
  having left it unclassed. Per-site bases are
  in the step-0 record. No site was classed by
  its fish counts. Three layer sites
  (Chanhu-daro, Dholavira, Rakhigarhi) have no
  rows in the pinned gazetteer and were classed
  from published site geography, as gate 0.3
  provides.
- **Gate 0.4 — TOO THIN (the execution closes
  here).** Census (margins only; total
  occurrences in the pinned layer, no site
  split): M047 13, M048 157, M050 17, M052 22,
  M060 20, M145 3, M147 2. One member (M048)
  clears the 30-occurrence floor; six are TOO
  THIN per member. Fewer than two members
  clear the floor, so the execution closes as
  **TOO THIN** under §3 gate 0.4 / §6, with
  the full census as its finding.
- **Gate 0.5 — NOT REACHED.** The execution
  ended at gate 0.4; no baseline was stated
  and no per-sign test was computed. No
  coastal split of any sign was counted at
  any point in this execution.

## 3. What this outcome does and does not establish

The census establishes exactly one thing: in
the pinned layer, the fish family as Parpola's
list fixes it is too thin, member by member,
for the frozen sign-by-sign test — only M048
occurs often enough to test, and the criterion
needs at least two testable members. **This
does not establish** anything about coastal
enrichment of any member (no coastal count
exists), anything about what any fish sign
meant, or any change to the family-level
verdict, which stands exactly as recorded
(partially falsified). The residue remains
open only in the sense the census states.
Because the closure is at gate 0.4, the §5
test and sensitivities (tasks E4–E5) have no
run under this contract; any future test of
this residue is a new act under a new freeze
or an amendment, not a continuation of this
execution. Asset F stands frozen for its
consumer (Spec 048) by the digest above,
independent of this closure.

## 4. Claim consequences (governed register)

One line per governed claim, F044-C01…C15.

- **F044-C01** (an outcome states only the
  per-sign distribution in the pinned layer):
  HELD in scope — this record states the
  census and the closure only; no distribution
  conclusion is stated, because none was
  computed.
- **F044-C02** (manual_002 stands SETTLED,
  partially falsified): HELD — the claim's
  record is untouched; its family-level
  verdict stands exactly as recorded. No
  append was made to the extracted-claims
  file: its bytes are a frozen §2 pin, and
  the dated residue append for this closure
  is this outcome record and the root LEDGER
  entry.
- **F044-C03** (at least one tested member
  ENRICHED): NOT REACHED — no member was
  tested; the TOO THIN closure routes here
  per the register's own derivation record.
- **F044-C04** (zero ENRICHED members records
  NO MEMBER ENRICHED): NOT REACHED — that
  outcome requires a run test; none ran.
- **F044-C05** (Asset F is a single canonical
  list built solely from Parpola's published
  list): CHECKED at gate 0.2 — held, §2 above.
- **F044-C06** (the frozen Asset F carries its
  digest as its identity; no in-place edits):
  HELD — digest recorded before the census
  existed; the asset has not been edited
  since.
- **F044-C07** (the test runs on the layer
  pinned at gate 0.1): HELD in form — the
  layer was pinned and reproduced at gate
  0.1; no test ran on any other layer.
- **F044-C08** (the coastal list is frozen at
  step 0 under the design's rule): CHECKED at
  gate 0.3 — held, §2 above.
- **F044-C09** (execution stops before any
  per-sign coastal test on any step-0 gate
  failure): FIRED as written — gate 0.4's
  TOO THIN closure stopped the execution
  before any per-sign coastal test.
- **F044-C10** (the ENRICHED criterion): NOT
  REACHED — no member was evaluated against
  it.
- **F044-C11** (the headline is exactly one
  member of the §6 outcome set): HELD — the
  headline is TOO THIN, in §6's pre-written
  wording with the census filled in.
- **F044-C12** (every tested member's full
  counts reported): HELD in the form the
  closure allows — no member was tested, and
  every member's census count is reported in
  full above and in the step-0 record.
- **F044-C13** (no outcome establishes what a
  fish sign meant): HELD — no meaning
  statement appears in any product of this
  execution.
- **F044-C14** (records are internal under
  the Roif gate): HELD — this record and its
  companions are internal; nothing was
  published or surfaced, and campaign
  reporting names this member only as
  executed — held under the Roif gate.
- **F044-C15** (sign identities are
  compilation-relative): HELD — the census
  and the asset are stated for the pinned
  layer only, and the cross-check divergence
  (§2, gate 0.2) is reported, not smoothed
  over.

## 5. Records

- Step-0 record: `reports/phase404_results.json`;
  report: `reports/phase404_step0_report.md`.
- Asset F: `asset-f-fish-family.json` in this
  directory; digest
  `ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`
  (digest field excluded), 7 members.
- Graph node: `IndusPhase404FishCoastalStep0`
  (registered and verified by import before
  the run).
- Root LEDGER entry: "Spec 044 step 0
  (Phase-404)" entry added with this record.
- `adjudication.md` carries no execution
  append: it is a digest-covered source of
  the freeze, and the executed-spec form
  (Specs 035–039) records execution in the
  outcome record, not in the frozen
  adjudication. This file is that record.
- Foundation check (H21): run at the run tree
  before this record landed — **40 passed /
  0 failed / 8 warnings**, the standing
  figure; `reports/foundation_check_report.json`
  regenerated at the run (its only change is
  the generation timestamp).
- Anchors: asserted byte-identical before and
  after (`df0cf620…`, §1).
- CI and suite state at the record merge:
  recorded in the completion note appended
  below at the merge.
- Local-environment disclosure: in this VM's
  existing glossa-lab venv, the freeze test
  `test_register_integrity` fails with a
  TypeError from the venv's AEE loader version
  (the conftest's `strict` keyword) — the
  register file is byte-identical to main and
  untouched by this execution; the same class
  of local-only failure was disclosed on
  Spec 059's freeze record. The PR's CI run
  is the figure of record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
