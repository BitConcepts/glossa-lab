# Ratification + adoption record — Spec 092 (ratified 2026-11-06; adoption executed 2026-11-10)

**Scope:** tasks.md Stage 0 adoption runs (T003–T004), executed
on branch `adopt/092-r4` after the owner's block
ratification. This record covers the ratification act, the
AEE assessment at adoption, the program-map assignment, and
the claims-ledger intake (T004) with its settling-chain
refresh, the generated-layer regeneration, the index
completion, and the gate profiles over the refreshed tree.
No build stage (Stage 1 onward) is started by this motion:
no credential has been encrypted, no verified-write library
has been built, and no harness leg has run.

## The ratification act (T003)

**Owner block ratification: Tristen Pierson, 2026-11-06.**
The package (spec.md, claims.md with falsifiers, plan.md,
tasks.md, the grounding record) was presented in the
Glossa-Lab chat and the owner ratified it **AS A BLOCK** —
decisions D-092-1..4 all as drafted, each carrying the
recommendation text it was ratified with:

- **D-092-1 — Key custody: a dedicated key file with
  separate custody.** *Recommendation: (a) — a 32-byte key
  in a 0600 file outside `{data_dir}`; AES-256-GCM via the
  `cryptography` package, fresh nonce per value; losing
  the key file loses the stored credentials to re-entry,
  loudly, by named error, never silently.*
- **D-092-2 — Encryption scope: per-value.**
  *Recommendation: credential entries encrypted; hosts,
  ports, toggles and prefs stay readable in the same file,
  so a missing key degrades exactly the credential class
  under a named error.*
- **D-092-3 — Shape #1's registration: amend, never
  delete.** *Recommendation: when the tray flake is fixed
  and discharged, its run-defs entry is amended to record
  the mechanism and the fix, and a recurrence counts as a
  new unexplained junction.*
- **D-092-4 — The phase392 branch rule, chosen in
  advance.** *Recommendation: profile first — a fixable
  pathology gets fixed; an intrinsic cost gets a
  registered, environment-scoped deselection (CI
  authoritative); weakening the test's determinism
  assertion to buy a local pass is off the table either
  way.*

The spec's Status line is stamped RATIFIED with the date,
in spec.md on this branch.

## AEE at adoption (T003, assessment clause)

The bundle was re-verified mechanically against claims.md
at adoption: the same 14 ids (C092-1..14) in the same
order, every claim carrying at least one falsification
test, and every bundle text found in its claims.md block —
the bundle in the package is the claims.md bundle,
unaltered. Under the pinned AEE (glossa-ci venv), from the
package directory:

- `aee validate aee-claims.json` — `valid: 14 claim(s) in
  aee-claims.json`, exit 0.
- `aee assess --no-ledger --input aee-claims.json
  --output records/adoption-aee-assessment.json` — exit
  1, outcome **iterate**, recorded verbatim:
  "Assessed 14 claim(s); found 65 failure mode(s); 14
  claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 14 of 14
  claim(s); the same evidence set supports multiple claims
  (FR-2.8, reporting only, no outcome effect in this
  phase). Draft cap: 14 draft claim(s) capped at
  gather_evidence/iterate (FR-2.3). Stage cap: 14 claim(s)
  below stage 'explained'; the outcome cannot be 'pass'
  (Spec 004 R1.4). Not understood: 28 residual unknown(s)
  are recorded on this assessment (Spec 004 R5.2). Lane 1
  (machine verification): outcome iterate; 0 claim(s) at
  or above the 0.70 threshold, 14 below. Lane 2 (human
  acceptance): stages by effective stage: created 14.
  Lane-2 lag: 14 claim(s) below explained."

The summary is identical to the draft package's T002
assessment (65 failure modes) — the adoption changed no
claim. "Iterate" is the normal reading for a draft bundle
at adoption (Specs 090, 091 and 093 read the same way); it
is recorded, not chased. The assessment of record is
`records/adoption-aee-assessment.json` on this branch.

## The program-map assignment (T004a)

`092-platform-hardening-r4` is assigned in
`glossa-indus/map/program-map-taxonomy.json` — domain
**Program infrastructure**, subdomain **Governance,
lifecycle & generated layers** (the 086–091 lineage
subdomain) — appended at the end of the studies list, as
Spec 091's entry was appended at its adoption. The program
map was regenerated through its own generator: before the
assignment the full gate read **25 PASS / 4 FAIL / 1
NOT-RUN** (all four failures V10 naming the unassigned
spec directory); with the assignment the tree read the
standing profile (below). The pre-append regeneration read
**950 claims · 94 studies · 29 unjudged studies**; the
finds list recorded this study as bundle-less
(`bundle_less_study` 28 → 29) — the truthful state until
the intake landed.

## The claims intake (T004b)

`tools/ledger/import_bundle.py --spec
specs/092-platform-hardening-r4 --date 2026-11-06`
(the ratification date, per the C090/C091/C093 record-date
convention): **14 appended, 0 already canonical**
(092-platform-hardening-r4/C092-1..14). Ledger:
981 → **995 lines**; SHA-256
`85c3b4c7e52e154cdc94c1f882bd609a459994c19ea821d8b20bae3934fb387b`
→
`378f700dba87f0bde2cc6ddfa321e819e4fe204fffe015257698c58e63901d6f`;
the appended 14-line block's SHA-256 is
`014a13190a34b3426dc58d5f62ac7a6c340d730b021743f7cd208d199c942cdb`;
append-only verified byte-wise (the first 981 lines hash
to the pre-append file). `tools/ledger/validate_ledger.py`
over the grown ledger: **PASS** — **964 claim entries**
(bundle population 927 → 941, extracted 23); falsifier
coverage 955 of 964; does_not_establish coverage 755 of
964 (unchanged — the C092 claims carry their DNE folded
into the statement text under the bundle normalization, as
Specs 090/091 do).

**Intake shape note (the Spec 090 G3 machinery lesson,
checked and not triggered):** Spec 092's directory is new
to main and none of its claims were canonical, so the
package's own carrier — the spec's `aee-claims.json` — is
the intake source of record and no second bundle file was
needed. `aee-claims.json` landed byte-identical to the
ratified draft; the one-hash-per-path invariant holds in
the grown ledger.

## Settling chain refresh

Executed in the standing precedent order.
`run_settling.py verify-canonicals` over the grown build,
before any pin moved: **6/6 registered canonicals
reproduce** (the C092 claims carry no sign_refs). Only
then: `glossa-indus/ledger/settling-canonical.json` pin
refreshed `85c3b4c7…`/981 → `378f700d…`/995 (provenance
and the comparison's inputs), with the re-derivation
recorded in the file itself as `re_derivations[8]`
(expectations unchanged; glossa-settle-1 unchanged). Both
T405 scenarios re-executed under run-defs v2 with the
standing pair's exact 286-sign full-frame scope and the
registered scenario ids: runs
**settling-20261110T153530Z-bef382** (incumbent; record
SHA-256
`02495eba32170f0465b953ba833cc029f2ebd9c0bced9c62d9beb138fbb03874`)
and **settling-20261110T153537Z-fdc511** (full-register;
record SHA-256
`da877030e9d69c8f1a7323dbe2d215e05f9f38d3451b4a6578841eb273d643d4`);
both result blocks **byte-equal** to the superseded
generation's; the run index gained their entry acts and
`supersedes` acts naming the 2026-11-10 G3 pair. The
Stage 4 dual-run comparison was re-filed from the new
pair via `run_settling.py compare`: identical to the
previous filing except the ledger pin; SHA-256
`f911c73874c7451436835b34437af345fde5bcacd882e5a278c71225d2a8f3d4`.
Assignment sets re-materialized (`run_settling.py
materialize-sets`, run **settling-20261110T153556Z-3710e2**;
sets unchanged — incumbent 94, full-register 286, H003 out
of frame; the artifact's only differing line is the
producing-run line).

## Store departures and index completion

The superseded scenario generation (the 2026-11-10 G3
pair, `settling-20261110T145806Z-63c6de` and
`settling-20261110T145813Z-5f57c9`) departed the store
under the map builder's D-D rule — its records are pinned
to the old build and cannot be carried. Both records
stand preserved in git history: incumbent git blob
`ace71bcc168989c7a4d73b9812e2c714cafb2aa9` (blob SHA-256
`a160328e6de7cf9e480a529db7b04986907d2d264ec6e128c459f599d83b8c6d`),
full-register git blob
`f730eac0783a015a7152fa6e51ba5775c8230555` (blob SHA-256
`7d1e429932c9a7d4ddf8a38128d8250948b996e59fe0dfe5d760afc130df6c4d`).
`tools/ledger/build_legacy_index.py` on the committed
refresh appended the `re_derivations[8]` event entry. The
builder's own enumeration derives legacy ids and skips
post-spec records by name, so its departure branch does
not reach writer-entered generations; the pair's two
`departure` acts were therefore appended through
`run_records.departure_act` + `append_act` (run-defs v2
§7.1), with the fields derived from the store's git
history exactly as the completion builder derives them —
superseding commit `4b50326a84c701219cd7f89b1c1ab286b6d72ffc`
(the refresh commit, the first store-touching commit
whose tree no longer carries the records), the git blobs
and blob SHA-256s above, and the builder's DEPARTURE_REF.
Folded census: **35 entries** (the settling store: 8
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
matrix.json (793,634 bytes, SHA-256
`ff3e199127d34968e85c7150a6a6e2cceac3917caa2cbaa4e962fe153c5ee654`)
and matrix.md (SHA-256
`2537c12f74154b16d83c15ad78d86c74ca75207ba54f88d35fd129e0cf7ffa09`);
the Spec 086 map (map-data.json SHA-256
`af6d937ba55f9df9f662268ad0f5376312c92981891c7a31f4772d138c4b50fc`;
settling runs carried: 2); the program map
(program-map.json SHA-256
`6a448e154087b6c406d49b31d22a6de8143b14a65ab9ec3e6fb0a4579e77865e`:
**964 claims · 94 studies · 28 unjudged studies** — the
092 study is judged once its claims stand in the ledger;
finds 38, `bundle_less_study` back to 28).

## Gate on the shipped tree

`tools/ledger/check_ledger_gate.py`, run on this branch's
tree at landing (glossa-ci venv), verbatim summaries:

- default: **29 PASS / 0 FAIL / 1 NOT-RUN** — RESULT: PASS
- `--regen`: **32 PASS / 0 FAIL / 0 NOT-RUN** — RESULT: PASS

The standing profile, over the grown census (995 lines,
964 claims).

## Test maintenance — census re-pins

Every moved literal was re-set from the regenerated
artifacts' actuals; no check was weakened, skipped, or
deleted:

- `backend/tests/test_program_map_conformance.py`:
  `PIN_CLAIMS` 950 → 964; `PIN_CLAIMS_BY_POPULATION`
  bundle 927 → 941; `PIN_CLAIMS_BY_CLASS` open 941 → 955;
  `PIN_STUDIES` 93 → 94; `PIN_FALSIFIER_PRESENT` 941 →
  955; domain totals, "Program infrastructure" 20 → 21.
  (`PIN_UNJUDGED` 28, `PIN_NULL_FALSIFIER_EXTRACTED` 9,
  `PIN_MULTI_SPEC` 44 unchanged.)
- `backend/tests/test_spec086_map.py`: claims_total 950
  → 964 (three sites); draft 926 → 940; ledger_lines 981
  → 995; claim elements 950 → 964; elements total 1594 →
  1608; supports 1466 → 1480 (two sites); loads 950 →
  964; falsifier census 941/950 → 955/964; AEE state
  census without_state/total 950 → 964; claims untouched
  by any run 949 → 963. (`no_stage_recorded` 24 unchanged
  — the C092 claims record a stage.)
- `backend/tests/test_spec086_ledger_gate.py`: "1473
  matrix cells" → "1487 matrix cells"; "950 claims
  counted across 8 statuses" → 964; "1473 map edges by
  relation" → 1487; "supports 1466" → "supports 1480";
  "950 claim nodes" → "964 claim nodes"; "93 study nodes"
  → "94 study nodes".
- `frontend/e2e/system-graph.spec.ts`: "950 claims in
  the ledger" → "964 claims in the ledger".

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
landing — no build stage (Stage 1 onward) is started by
this motion, the ledger growth changes no claim's status,
stage, or score, and the Spec 082 token file, the edge's
secret custody, and every UI surface stand outside this
spec's diff exactly as C092-14's boundary states.
