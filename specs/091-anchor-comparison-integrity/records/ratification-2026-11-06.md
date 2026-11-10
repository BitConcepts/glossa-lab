# Ratification + adoption record — Spec 091 (ratified 2026-11-06; adoption executed 2026-11-10)

**Scope:** tasks.md Stage 0 adoption runs (T002–T004), executed
on branch `adopt/091-wave1` after the owner's block
ratification. This record covers the ratification act, the
AEE assessment at adoption, the program-map assignment, and
the claims-ledger intake (T004) with its settling-chain
refresh, the generated-layer regeneration, the index
completion, and the gate profiles over the refreshed tree.
No study stage (Stage 1 onward) is started by this motion.

## The ratification act (T003, first clause)

**Owner block ratification: Tristen Pierson, 2026-11-06.**
The package (spec.md, claims.md with falsifiers, plan.md,
tasks.md, the grounding censuses) was presented in the
Glossa-Lab chat and the owner ratified it **AS A BLOCK** —
decisions D-091-1..7 all as drafted, each carrying the
recommendation text it was ratified with:

- **D-091-1 — The independence legs' humans are an owner
  act; the in-house legs do not wait.** *Recommendation:
  (b) — the owner authorizes a shortlist (credentials,
  rates) prepared in Stage 1, contact only on his pick.*
- **D-091-2 — The blinding protocol is full blind, filed
  before coding starts.** *Recommendation: (a).*
- **D-091-3 — Dispositions land in a new versioned audit
  (audit v2), generated, with the WP5 audit frozen.**
  *Recommendation: (a).*
- **D-091-4 — The corrected Phase-48 battery is a new
  versioned battery; the original script is frozen.**
  *Recommendation: (a).*
- **D-091-5 — Honesty labels land per workstream, not at
  spec closeout.** *Recommendation: (a).* (Any preprint or
  site *text* change still goes through the owner's
  approval of the actual text, as always; this decision
  covers the labeling obligation and its timing, not any
  text.)
- **D-091-6 — Candidate 2's phonotactic arm is
  dependency-gated, not blocking.** *Recommendation:
  (a).*
- **D-091-7 — Eligible entries become citable at W1's
  close, with their class attached; no extra adjudication
  act.** *Recommendation: (a).*

The spec's Status line is stamped RATIFIED with the date,
in spec.md on this branch.

## AEE at adoption (T003, assessment clause)

The bundle was re-verified mechanically against claims.md
at adoption: the same 15 ids (C091-1..15) in the same
order, every claim carrying at least one falsification
test, and every bundle text opening with its claims.md
body — the bundle in the package is the claims.md bundle,
unaltered. Under the pinned AEE (glossa-ci venv), from the
package directory:

- `aee validate aee-claims.json` — `valid: 15 claim(s) in
  aee-claims.json`, exit 0.
- `aee assess --no-ledger --input aee-claims.json
  --output records/adoption-aee-assessment.json` — exit
  1, outcome **iterate**, recorded verbatim:
  "Assessed 15 claim(s); found 66 failure mode(s); 15
  claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 15 of 15
  claim(s); the same evidence set supports multiple claims
  (FR-2.8, reporting only, no outcome effect in this
  phase). Draft cap: 15 draft claim(s) capped at
  gather_evidence/iterate (FR-2.3). Stage cap: 15 claim(s)
  below stage 'explained'; the outcome cannot be 'pass'
  (Spec 004 R1.4)."

The summary is identical to the draft package's T002
assessment (66 failure modes) — the adoption changed no
claim. "Iterate" is the normal reading for a draft bundle
at adoption (Specs 090 and 093 read the same way); it is
recorded, not chased. The assessment of record is
`records/adoption-aee-assessment.json` on this branch.

## The program-map assignment (T004a)

`091-anchor-comparison-integrity` is assigned in
`glossa-indus/map/program-map-taxonomy.json` — domain
**Program infrastructure**, subdomain **Governance,
lifecycle & generated layers** (the 086–090 lineage
subdomain) — appended at the end of the studies list, as
Spec 090's and Spec 093's entries were appended at their
adoptions. The program map was regenerated through its
own generator: before the assignment the full gate read
**25 PASS / 4 FAIL / 1 NOT-RUN** (all four failures V10
naming the unassigned spec directory); with the
assignment the tree read the standing profile (below).
The pre-append regeneration read **927 claims · 93
studies · 29 unjudged studies**; the finds list recorded
this study as bundle-less (`bundle_less_study` 28 → 29)
— the truthful state until the intake landed.

## The claims intake (T004b)

`tools/ledger/import_bundle.py --spec
specs/091-anchor-comparison-integrity --date 2026-11-06`
(the ratification date, per the C090/C093 record-date
convention): **15 appended, 0 already canonical**
(091-anchor-comparison-integrity/C091-1..15). Ledger:
958 → **973 lines**; SHA-256
`c55d57822bcd9b2e9a3401d807aea6e5e1ce872c5e239baadea4834310c8f4aa`
→
`6eada964c585a859db34e1a0e8c1da892baf0012db90e3742829bb318905a0b5`;
the appended 15-line block's SHA-256 is
`9f26496c577418bfbd86f5184673d42a975e0044f64292ee556c8fe7721fc2c7`;
append-only verified byte-wise (the first 958 lines hash
to the pre-append file). `tools/ledger/validate_ledger.py`
over the grown ledger: **PASS** — **942 claim entries**
(bundle population 904 → 919, extracted 23); falsifier
coverage 933 of 942; does_not_establish coverage 755 of
942 (unchanged — the C091 claims carry none, as drafted).

## Settling chain refresh

Executed in the standing precedent order.
`run_settling.py verify-canonicals` over the grown build,
before any pin moved: **6/6 registered canonicals
reproduce** (the C091 claims carry no sign_refs). Only
then: `glossa-indus/ledger/settling-canonical.json` pin
refreshed `c55d5782…`/958 → `6eada964…`/973 (provenance
and the comparison's inputs), with the re-derivation
recorded in the file itself as `re_derivations[6]`
(expectations unchanged; glossa-settle-1 unchanged). Both
T405 scenarios re-executed under run-defs v2 with the
standing pair's exact 286-sign full-frame scope and the
registered scenario ids: runs
**settling-20261110T140239Z-7b9862** (incumbent; record
SHA-256
`af5eb0e6d6d694b20cccfbdd15f0e75a18cb8ce41d62cc11b803e39a4a2fb1a0`)
and **settling-20261110T140240Z-b53030** (full-register;
record SHA-256
`8812547311bed0005be93cb43ac2fcafa7a58355d6edfe7ac826ab4aaeec595b`);
both result blocks **byte-equal** to the superseded
generation's; the run index gained their entry acts and
`supersedes` acts naming the 2026-11-06 pair. The Stage 4
dual-run comparison was re-filed from the new pair via
`run_settling.py compare`: identical to the previous
filing except the ledger pin; SHA-256
`b2f49c0c2bee35cad025ffb04b369225e20a9967c47c6f8e90cec6e83851eca0`.
Assignment sets re-materialized (`run_settling.py
materialize-sets`, run **settling-20261110T140246Z-d8affc**;
sets unchanged — incumbent 94, full-register 286, H003 out
of frame; the artifact's only differing line is the
producing-run line; artifact SHA-256
`f53e3dbdcaab37669b5744a919e9f310efa0b1cb4709d5ad4890007f02972988`).

One mechanics note, stated plainly: the first
re-execution of the pair omitted `--scenario`, so those
records carried `scenario: null` and were not map-carried
(the map carries scenario evaluation records only). They
were deleted before any commit, the run index restored to
its committed state, and the pair re-executed with the
registered scenario ids, as recorded above. No committed
state ever carried the scenario-less pair.

## Store departures and index completion

The superseded scenario generation (the 2026-11-06 pair,
`settling-20261106T085256Z-316590` and
`settling-20261106T085304Z-78bf5c`) departed the store
under the map builder's D-D rule — its records are pinned
to the old build and cannot be carried. Both records
stand preserved in git history: incumbent git blob
`5eef16f6d3ba4da7b9f36107e8c0cabe62d1859e` (blob SHA-256
`aecc66148765e4cd0628fcb8bf5556e6b0bd3dc4dda36d5123717e8c98cdd7fc`),
full-register git blob
`60015ca7bebdff70444985fdf29a0f0cc74e6f58` (blob SHA-256
`17a1650373fa1ad35ca8d2d28a0184472e77136c909a327153cb7e2398048242`).
`tools/ledger/build_legacy_index.py` on the committed
refresh appended the `re_derivations[6]` event entry. The
builder's own enumeration derives legacy ids and skips
post-spec records by name, so its departure branch does
not reach writer-entered generations; the pair's two
`departure` acts were therefore appended through
`run_records.departure_act` + `append_act` (run-defs v2
§7.1), with the fields derived from the store's git
history exactly as the completion builder derives them —
superseding commit `f75846488dc4518d07952d7af8b2fd5de46cf960`
(the refresh commit, the first store-touching commit
whose tree no longer carries the records), the git blobs
and blob SHA-256s above, and the builder's DEPARTURE_REF.
Folded census: **27 entries** (the settling store: 5
standing records, the departed generations accounted by
departure act, the canonical re-derivation events).

## Regeneration over the grown ledger

`tools/ledger/generate_matrix.py --gated` was refused
over the pre-regeneration tree (candidate gate 21 PASS /
8 FAIL / 1 NOT-RUN; all eight failures cross-layer
staleness against the not-yet-regenerated sibling layers,
and the published artifacts were byte-untouched, as the
gate is designed to leave them). The layers were
therefore regenerated with the plain generators in
dependency order, the Spec 093 Appendix A procedure:
matrix.json (785,277 bytes, SHA-256
`26ea487cca59f06aea33e618cef9e603683edbc77ed969af168367c9f4625f49`)
and matrix.md (SHA-256
`b2085ecc27c83cd61d9439208f9ad72133b71bd305d850b5a19f678d5e3d3b46`);
the Spec 086 map (map-data.json SHA-256
`6430cd9f2beef1c2ce2b553121c7365c8418681bbda5d846215480cc1b39d24d`;
settling runs carried: 2); the program map
(program-map.json SHA-256
`b753583faa62ce870a8107ddbfacd09bd3f0749fa75ed66f5fd3b4f89f1aebfc`:
**942 claims · 93 studies · 28 unjudged studies** — the
091 study is judged once its claims stand in the ledger;
finds 38, `bundle_less_study` back to 28).

## Gate on the shipped tree

`tools/ledger/check_ledger_gate.py`, run on this branch's
tree at landing (glossa-ci venv), verbatim summaries:

- default: **29 PASS / 0 FAIL / 1 NOT-RUN** — RESULT: PASS
- `--regen`: **32 PASS / 0 FAIL / 0 NOT-RUN** — RESULT: PASS

The standing profile, over the grown census (973 lines,
942 claims).

## Test maintenance — census re-pins

Every moved literal was re-set from the regenerated
artifacts' actuals; no check was weakened, skipped, or
deleted:

- `backend/tests/test_program_map_conformance.py`:
  `PIN_CLAIMS` 927 → 942; `PIN_CLAIMS_BY_POPULATION`
  bundle 904 → 919; `PIN_CLAIMS_BY_CLASS` open 918 → 933;
  `PIN_STUDIES` 92 → 93; `PIN_FALSIFIER_PRESENT` 918 →
  933; domain totals, "Program infrastructure" 19 → 20.
  (`PIN_UNJUDGED` 28, `PIN_NULL_FALSIFIER_EXTRACTED` 9,
  `PIN_MULTI_SPEC` 44 unchanged.)
- `backend/tests/test_spec086_map.py`: claims_total 927
  → 942 (three sites); draft 903 → 918; ledger_lines 958
  → 973; map elements 1571 → 1586; supports 1443 → 1458
  (two sites); loads 927 → 942; falsifier census 918/927
  → 933/942; AEE state census without_state/total 927 →
  942; claims untouched by any run 926 → 941.
- `backend/tests/test_spec086_ledger_gate.py`: "1450
  matrix cells" → "1465 matrix cells"; "927 claims
  counted across 8 statuses" → 942; "1450 map edges by
  relation" → 1465; "supports 1443" → "supports 1458";
  "927 claim nodes" → "942 claim nodes"; "92 study
  nodes" → "93 study nodes". ("bundle_less_study 28"
  unchanged.)
- `frontend/e2e/system-graph.spec.ts`: "927 claims in
  the ledger" → "942 claims in the ledger".

The four pin-bearing test files read **96 passed / 1
failed** locally (glossa-ci venv, basetemp on the
workspace disk); `test_spec086_ledger_migration.py::
test_p2_reconciliation` passes — the bundle population
fingerprint-matches the ledger again, as the intake
restores. The one failure is pre-existing on this VM and
not this landing's:
`test_spec086_map.py::test_builder_refuses_a_run_pinned_to_another_build`
fails on this VM even on pristine main (its fixture's
run-store glob meets a record the builder legitimately
skips, so the seeded corruption lands where no refusal
can fire; reproduced before this adoption, recorded in
Spec 093's adoption record). CI is authoritative for it.

*This does not establish:* anything beyond the intake's
landing — no study stage (Stage 1 onward) is started by
this motion, the named-human engagements of D-091-1
remain the owner's acts, and the ledger growth changes
no claim's status, stage, or score.
