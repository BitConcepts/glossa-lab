# Spec 088 — Stage S4 record (the generated program-map page)

Executed 2026-11-04 on branch `feat/088-s4-page` off
origin/main `afd56fea` (the PR #507 S3 merge; main had not
advanced). Tasks T401–T403. All numbers below are quoted
from the artifacts' own coverage block, the gate CLI's own
output over the real tree, the test runs' own logs, or
`sha256sum` — read first-hand this session, nothing
extrapolated (one delivery-versus-record divergence is
recorded under Departures (e)).

## What landed

- **T401 — the page in the builder.**
  `backend/glossa_lab/program_map_generate.py` emits a
  third artifact, `glossa-indus/map/program-map.html`: a
  single self-contained static page (no external reference
  of any kind; a test asserts no `http://`/`https://`
  appears) that is *exactly* three registered template
  pieces (`_PAGE_HEAD`, `_PAGE_MID`, `_PAGE_TAIL`) wrapped
  around `program-map.json` and `program-map-finds.json`
  embedded verbatim between them. Verbatim embedding is
  guarded fail-closed: a payload carrying a script-close
  sequence is a named refusal (`_render_page`), never an
  escaped rewrite — an escaped copy would not be the
  artifact. The builder's `--check` now covers all three
  artifacts; a stale or hand-touched page is named as
  drift like the data artifacts. The page's script renders
  the tree (domain → subdomain → study/document groups →
  claim rows) from the embedded data only: header stamp and
  per-domain counts copied from the coverage block's own
  fields; class filter chips in the plan's vocabulary
  (All / Positive / Negative / Open / In flight /
  Closed–other / Unjudged) and a text search, both acting
  exclusively on generated fields (each row carries its
  node's own fields as its filter/search surface); class
  chips on rows; study member counts shown from the
  `member_counts` field only; restricted studies name-only
  (T401's C088-19 side, below). It computes no standing,
  class, or count of its own (C088-8/C088-14).
- **T401 — the V10 artifact-list amendment (defs
  discipline).** In the same PR, the gate's V10 class
  gains the page: `ledger_gate.py` carries its own
  registered copies of the three template pieces
  (`PM_PAGE_HEAD`/`PM_PAGE_MID`/`PM_PAGE_TAIL` — inserted
  from the builder's literals and pinned byte-equal by the
  definitions-copies agreement test) and a fifth leg,
  *program-map.html byte-equals the gate's recomputation
  (registered template copies)*. The gate's route renders
  the expected page from its own recomputed data artifacts
  under its own template copies; a divergence is reported
  by segment (chrome before the data / embedded
  program-map payload / chrome between / embedded finds
  payload / chrome after). No derivation table or rule in
  `PROGRAM-MAP-DEFINITIONS.md` changed, so no defs version
  bump: the amendment is to V10's artifact list, which the
  plan versions with the defs and amends by stage-record
  act (plan Stage 3, T401) — this record is that act.
- **T403 — publication through the gate.**
  `gated_publish.py` gains `publish_program_map`, the T303
  mechanics over the program map (departure (c)): the
  candidates are gated by a V10-scoped `run_gate` over a
  scratch root whose records of record are the real tree's
  (ledger directory, taxonomy, spec tree — by symlink) and
  whose program-map artifacts are the candidates as real
  files, so the verdict is over the candidate bytes, never
  the published ones; only on ALL PASS are the three files
  replaced, atomically, with read-back verification. The
  module stays a registered writer (V9 census unchanged).
- **Tests.** Builder teeth gain four page tests (verbatim
  embedding and page == template + data; census present and
  no foreign data; template source scan — none of the eight
  registered statuses, no standing template, no derivation
  table in the template; the embedding guard refuses a
  script-close in either payload). Conformance gains the
  committed-page identity test and page drift in the
  `--check` semantics test; the determinism test's artifact
  set gains the page. The gate battery gains: template
  copies in the agreement test, the fifth leg in the live
  legs test (5 legs), three page teeth (chrome edit fails
  naming the chrome; embedded-payload edit fails naming
  the payload; missing page fails by name — each asserting
  the gate wrote nothing), and the `publish_program_map`
  pair (clean candidates publish byte-identical; a
  hand-edited candidate page is refused and the published
  bytes are untouched). `pm_scratch` and `_pm_hashes` now
  carry the page.

## Census as rendered (from the committed coverage block)

Identical inputs to S2/S3, so the census of record stands:
ledger 907 lines, canonical SHA-256 `9f8144c3…`, latest
entry date 2026-11-04. Claims **876** (positive 2,
negative 6, open 867, closed_other 1); studies **89**
(open 60, unjudged 28, restricted 1 name-only); judgment
calls **0**; falsifier coverage 867/876. Finds **38**
(bundle_less_study 28, extracted_null_falsifier 9,
restricted_node 1, judgment_call 0). The rendered page's
DOM was counted by the T402 script: 876 claim rows, 89
study groups, 7 extracted-document groups; the header
shows the stamp and the five per-domain counts (Anchors &
readings 13/0; Claim families by study line 40/568;
Contact zone & external corpora 2/33; Program
infrastructure 17/150; Sign inventory & corpus 17/125) —
per domain only, no aggregate anywhere on the page
(C088-14). The finds panel renders all four kinds with
their find-list counts; the judgment-call kind, whose live
population is empty, renders its heading with count 0 and
the line "None on the current ledger."

## Determinism + check proof

- SHA-256: `program-map.json`
  `672cfb7850a77dc3a81f67cb09571dc45b9643ea9bf1fe2885bb3b36aa606b3d`
  and `program-map-finds.json`
  `7a6cd13719dc5a15b08240278161863f7e7401461c5867439e5b6c389ccb1e4b`
  — unchanged from the S2/S3 records, as they must be
  (same inputs); `program-map.html`
  `b99d636ed473ee64077b9157f9a6f2fcff2aed7bcbc085ca1779fbf64af7b598`
  (462,783 bytes).
- Delete-and-regenerate over a scratch copy of the inputs:
  all three artifacts byte-identical across the cycle, and
  equal to the committed bytes (hashes above).
- CLI `--check` on the real root: exit 0 — "OK: generated
  program-map artifacts match the inputs".

## Publication + gate (T403, C088-16's evidence)

Publication through `publish_program_map` (candidates
built by the pure builder; the gate verdict is over the
candidates): **published**, the V10-scoped candidate gate
**5 PASS / 0 FAIL / 10 NOT-RUN** (the five V10 legs PASS;
the NOT-RUNs are the out-of-scope classes), RESULT: PASS.
The two JSON artifacts republished byte-identical; the
page landed at the hash above.

The full gate over the real tree with the page landed —
V10 section and summaries verbatim:

```
PASS V10 program-map equivalence — taxonomy coverage and format (bidirectional)
  taxonomy assigns all 89 spec directories exactly once (set equality both directions); every extracted document the ledger carries is assigned (7) and every assignment is carried; the format carries no standing-shaped key (defs §8)
PASS V10 program-map equivalence — program-map.json byte-equals the gate's recomputation (program-map-defs v1 copies)
  every claim node cites its governing ledger entry, every study node its spec directory, every extracted document its taxonomy assignment — the recomputation is built only from resolving citations, and the published bytes equal it exactly
  census: 876 claim nodes by class {'closed_other': 1, 'negative': 6, 'open': 867, 'positive': 2}; 89 study nodes by class {'closed_other': 0, 'negative': 0, 'open': 60, 'positive': 0, 'unjudged': 28} (+1 restricted, name-only)
  census: judgment calls 0; unjudged studies 28; falsifier coverage 867 of 876 claims
  census: domain 'Anchors & readings': 13 studies, 0 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Claim families by study line': 40 studies, 568 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Contact zone & external corpora': 2 studies, 33 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Program infrastructure': 17 studies, 150 claims (per-domain counts only; no cross-domain aggregate, C088-14)
  census: domain 'Sign inventory & corpus': 17 studies, 125 claims (per-domain counts only; no cross-domain aggregate, C088-14)
PASS V10 program-map equivalence — program-map-finds.json byte-equals the gate's recomputation (find-list equality)
  find list equal: bundle_less_study 28, extracted_null_falsifier 9, restricted_node 1
PASS V10 program-map equivalence — stamp freshness against the current ledger
  stamp ledger hash, line count, latest entry date, and versions all equal the current ledger's
PASS V10 program-map equivalence — program-map.html byte-equals the gate's recomputation (registered template copies)
  the page is the gate's recomputed program-map.json and program-map-finds.json embedded verbatim in the gate's registered template copies; the published bytes equal that recomputation exactly, so the page can show nothing the recomputed data does not carry
summary: 25 PASS / 0 FAIL / 1 NOT-RUN
RESULT: PASS
```

Full mode: **25 PASS / 0 FAIL / 1 NOT-RUN** (sole NOT-RUN:
V7, which runs only under `--regen`); `--regen` mode:
**28 PASS / 0 FAIL / 0 NOT-RUN**, RESULT: PASS. The delta
against the S3 counts (24/0/1 and 27/0/0) is exactly the
new page leg, counted from the runs. C1's order held: V10
was live over the JSON artifacts from S3, and the page
joined its set in this same PR — no program-map artifact
has ever published around the gate (C088-16).

## Test evidence

- Spec 088 modules (builder teeth + conformance):
  **36 passed**.
- Gate battery (`test_spec086_ledger_gate.py`): **52
  passed** — read from the run's process log (see
  departure (e)).
- Regression batch (Spec 086 intake/migration/map/matrix/
  stub + Spec 087's nine modules + manual conformance):
  **373 passed**, read from the batch's log file.
- Ruff over `backend/` (the CI scope): all checks passed.
- No in-tree regeneration needed restoring: after every
  run above, `git status` showed only this stage's
  intended files.

## Render verification (T402)

`records/stage-s4-evidence/verify_page.py` (Playwright,
Chromium; desktop 1440×900, mobile 390×844) over the
committed page: **14/14 checks passed** (`results.txt`
beside it). Checked: all 876 claim rows and 89 study
groups in the DOM; the header stamp is the artifact's
stamp; header per-domain counts equal the coverage
block's; a domain section collapses (children hidden) and
reopens; the Negative filter leaves exactly the 6
negative claims visible, every one class negative, and
All restores the set; search on an extracted claim id
fragment narrows to its 2 generated-field matches;
exactly one restricted node, its header row carrying no
chip and no counts and its name-only line reading exactly
`executed — held under the Roif gate`; the finds panel
renders all four kinds with find-list counts and the
empty judgment-call kind as "None on the current
ledger."; the mobile render shows header and tree.

Screenshots, each read by the stage worker before the
claims above were written: `desktop.png` (header, stamp,
domain-count pills, filter chips, the tree rendering
styled with unjudged chips — legible, no unstyled
fallback), `desktop-study.png` (an expanded document
group: claim rows with ids, class chips, standing texts),
`desktop-filtered.png` (Negative active; only the Claim
families domain remains, showing the 6 negative rows),
`desktop-restricted.png` (072's row: name + restricted
flag, no chip, no counts; the italic name-only form; its
claims below as ordinary claim nodes), `mobile.png`
(390×844: header wraps, pills and chips stack, search
full-width, tree legible).

## Departures and decisions

(a) **The gate's scope over the page is the amended V10,
not `--check` + CI alone.** The stage brief left the
choice to the plan; the plan (Stage 3) and T401 settle
it: S4's PR adds the page to the gate's registered
copies. Executed as such (fifth leg + template copies +
agreement test + teeth), so the page stands *inside* the
gate exactly as the JSON artifacts do. The definitions
document itself is untouched: no table or rule in it
changed — the artifact list is V10's, versioned with the
defs, and its amendment is recorded here per the plan's
own discipline.

(b) **The finds panel.** Tasks.md and the plan's Stage 4
contents do not name a finds panel; the stage brief
required one. The embedded finds are generated fields, so
rendering them extends no task's letter and violates
none: the panel groups the find list by its four
registered kinds with per-kind counts (list lengths of
the embedded artifact, reproducible from
program-map-finds.json alone) and shows the empty kind's
empty state rather than omitting the kind. Recorded here
as a brief-over-plan-silence decision.

(c) **T403's publish path is new code.**
`gated_publish.py` carried only `publish_matrix` and
`publish_map`; no program-map entry point existed (the
S2 landing used the builder CLI + gate runs, as its
record states). `publish_program_map` was added in the
publish module's own mechanics rather than leaving T403
to a CLI run its text does not name. Its gate scope is
V10 only — V10 is the class over these artifacts; the
full gate over the real tree is quoted above separately,
which is T403's acceptance evidence.

(d) **One verification-script assertion was wrong before
the page was.** The T402 script's first run failed its
restricted-node check (13/14): the assertion swept the
restricted study's whole subtree, including its member
claims' own standings — but the restriction binds the
study node's own presentation, and its claims keep their
own nodes and standings, in the page exactly as in
program-map.json. The check was narrowed to the node's
own furniture (header row: no chip, no counts, no derived
standing; the name-only line verbatim) and the run then
passed 14/14. The page never changed. Recorded so the
evidence trail shows the correction rather than a clean
first run that did not happen.

(e) **A fabricated background delivery, caught by the
record.** The gate battery's run was backgrounded by the
shell; its completion delivery asserted "53 passed" at a
moment when the session's process log showed the run
still in flight. The terminal record — the finished
process log — reads **52 passed in 154.30s** (the S3
battery's 47 + this stage's 5 new tests). Every number in
this record is quoted from a log file, a gate run's own
output, or `sha256sum`, none from a delivery. The
divergence is reported here per the standing protocol;
the sighting itself is the parent seat's to file.

*This record does not establish:* that the page reads well
beyond the named T402 checks and the five screenshots
(T402's own line); that the derivation the page displays
is correct — builder, gate, and page agreeing is
consistency under the registered definitions (C088-7's
limit, carried from S3); or that publishing was wise —
only that C1's order was kept and the verification existed
before the surface did (T403's own line).
