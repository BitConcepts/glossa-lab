# Amendment — run-defs v2: departed-generation accounting (2026-11-05)

**Spec 089 lineage.** This record is the amendment act
for the run definitions: it registers **run-defs v2**,
propagated in this same landing to every registered copy
(run-defs §9): `glossa-indus/ledger/RUN-DEFINITIONS.md`,
the library's machine copy
(`backend/glossa_lab/run_records.py`), and the gate's
V11 copies (`backend/glossa_lab/ledger_gate.py`). The
builder repair lands in
`tools/ledger/build_legacy_index.py`. Nothing else in
the definitions changes: v2 carries v1 verbatim except
§7.1 (one act kind added, its fold rules added) and
§7.2 (the completion builder's population rule stated).
The comparability judgment row (§4) is untouched.

## The defect this amendment closes

Proven twice on 2026-11-05, on the first two claims-
ledger growths since the legacy index was completed
(Spec 084's C084-12 intake, PR #531's stage record; Spec
093's C093 intake, PR #530's ratification record
Appendix A — both intakes executed end-to-end and then
held, reverted, on this gap):

- A settling refresh re-derives the T405 pair; the
  superseded generations' records leave the store (the
  map builder's D-D rule cannot carry a stale-pinned
  evaluation record).
- The departed pair — `legacy:t405-incumbent-over-full-
  frame--d9f73e4c4e4e` and `legacy:t405-full-register-
  over-full-frame--f8c86443e924` — was entered
  **standing** by the Stage 5 completion builder, before
  any supersession accounting could exist for it. Its
  entry acts therefore carry no `superseded_by_commit` /
  `git_blob` / `blob_sha256`.
- Gate V11 leg (c) counts a departed record as accounted
  only when its **entry** carries those three fields.
  Run-defs §7.1 makes entry acts immutable, the fold
  refuses a second entry act for an id, and no act kind
  amends an entry — so no registered act could account
  the pair, and the gate over either refreshed tree read
  28 PASS / 1 FAIL / 1 NOT-RUN (31 / 1 / 0 under
  `--regen`), the failure being leg (c) alone.
- The completion builder could not repair it: it skips
  already-entered ids, and its history pass refused
  outright on a post-spec record standing in the store's
  history — verbatim, `LEGACY INDEX REFUSED: legacy
  recovery: record 'settling-20261105T022535Z-a7b4e5.json'
  carries no 'candidate' to recover` — appending nothing
  at all over the current store. Every future intake
  adds another post-spec record to that history, so the
  refusal would have blocked every future growth.

Every earlier generation was entered only after
departing, which is why the gap never fired before
2026-11-05.

## The registered change (run-defs v2, §7.1)

**A new index act kind, `departure`** — the departed-
generation accounting. Fields:

| Field | Content |
|---|---|
| `run_id` | The departed generation's id (an entered id) |
| `record` | The record's store-relative path — must equal the entry's `record` |
| `superseded_by_commit` | The first store-touching commit whose tree no longer carries the record (the same derivation the legacy entry uses) |
| `git_blob` | The record's final git blob id |
| `blob_sha256` | The SHA-256 of the blob's bytes |
| `ref` | The act that ordered the accounting (a stage record, PR, or the completion builder's invocation) |

The accounting is a **new act, never an edit**: the
entry act stands byte-untouched, append-only is
preserved, and the fold's state gains a `departed`
register (run id → its departure act).

**Fold rules (both registered copies, identically).** A
fold refuses a departure act that: names a run id with
no prior `entry` act; names a `record` differing from
the entry's `record`; is a second departure act for one
id (a generation's departure is accounted once); omits
a required field; carries a `superseded_by_commit` that
is not a 40-hex commit id, a `blob_sha256` that is not
a 64-hex SHA-256, an empty `git_blob`, or an empty
`ref`.

**Gate V11 leg (c) (the gate's copy).** A departed
record now counts as accounted when **either** its
entry carries the three accounting fields (the v1 form,
generations entered after departing) **or** a folded
departure act for its id carries them (the v2 form,
generations entered standing and departed later). An
entry whose record neither stands nor is accounted
under either form fails leg (c) with the same finding
as before. The leg's census evidence line counts the
departure-accounted generations separately.

## The builder's stated population rule (§7.2, as amended)

`build_legacy_index.py` completes an index over the
store's whole git history under these rules, in
enumeration order:

1. A record whose legacy id is **entered and still
   standing** is skipped (as in v1).
2. A record whose legacy id is **entered and has
   departed** gains a `departure` act carrying the
   accounting fields derived from its final blob and
   the superseding commit — unless a departure act
   already accounts it, in which case it is skipped.
   (This is the completion the v1 builder could not
   perform.)
3. A record **not entered** and carrying **no run
   header** is the pre-spec legacy population: entered
   as in v1 (standing from its bytes; departed with the
   accounting fields on its entry).
4. A record carrying a **run header** is a post-spec
   record, entered by its own writer under its own run
   id and never legacy-derived (the population rule
   `enumerate_legacy_entries` has always stated). In
   the history pass it is **skipped-with-record**: the
   builder names it on its output as skipped, and never
   refuses on it. This replaces the v1 behaviour, in
   which the first such record refused the whole build
   and nothing was appended.
5. A headerless record missing a recoverable key
   component (`semantics`, `candidate`, `pins`) remains
   a **named refusal**: it belongs to the legacy
   population and cannot be honestly half-entered. No
   such record stands in the store's history today (the
   census of the seeded proofs below is the evidence);
   the refusal names the record, as in v1.

Rules 2 and 4 are the repair: together they mean no
future ledger growth can strand a departed generation
unaccounted or block the completion build.

## Design choices recorded (judgments the prior records did not settle)

- **Act-kind name: `departure`.** The alternatives were
  amending the entry (forbidden by §7.1 immutability —
  not a real alternative) and builder authority to
  rewrite an entered-standing entry at departure (the
  same edit under another name). A new act kind is the
  only form consistent with the index's append-only
  discipline, and it mirrors the system's existing
  shape: relations a record cannot carry about itself
  live in the index as acts (D-089-3). The name says
  what the act records — a generation's departure from
  the store — and nothing stronger: a departure act is
  accounting, not supersession (a superseded generation
  whose record still stands gets no departure act; the
  act fires only when the record has left the store).
- **The act is not restricted to legacy ids.** Any
  entered generation whose record departs the store —
  a post-spec run removed under the same D-D rule, for
  instance — is accounted the same way; restricting the
  act to legacy ids would leave the identical hole open
  for post-spec generations. The gate's accounting test
  is symmetric.
- **The accounting fields live on the act, not
  re-derived by the gate.** The gate keeps its standing
  discipline: it shape-checks the three fields (commit
  form, blob id present, SHA-256 form) exactly as it
  shape-checks the entry-carried form; the values
  themselves are anchored in the store's git history,
  where a reviewer verifies them against the named
  commit and blob.
- **Version: v2, not an in-version note.** Run-defs §9
  admits definition changes only as a new version
  propagated to every copy in the same motion; §10's
  in-version registration amended no rule, table, or
  vocabulary, and this amendment changes all three (one
  act kind, its fold rules, the builder rule). The
  version constants in both machine copies move
  together; the gate's copies-agree test pins exactly
  that equality.

## Seeded proofs (executed at this landing; outputs are the evidence)

(a) **A held intake's growth passes V11 in both modes
with the fix.** Executed over the Spec 093 executed
intake state, preserved under the local tag
`held-intake-executed-2026-11-05` (commit `82b75048`;
ledger 957 lines, SHA-256 `e6525d04…`), with this
landing's machinery overlaid on a scratch copy (the
preserved state itself untouched). Controls first, on
the un-fixed machinery: the gate read **28 PASS / 1
FAIL / 1 NOT-RUN**, the failure being leg (c) alone,
and the builder refused verbatim (`record
'settling-20261105T022535Z-a7b4e5.json' carries no
'candidate' to recover`). With the fix, the builder
appended exactly 3 acts — the two departure acts for
the departed pair and the canonical event entry for
`re_derivations[4]` (the event the intake's refresh
added) — and skipped-with-record the four post-spec
records in the history (the a7b4e5 materialization
record, the refreshed pair, the new materialization
record). The departure acts' derived values match the
values Appendix A of the Spec 093 ratification record
preserved, computed independently here from git
history: superseding commit `82b750486c4b` for both;
incumbent blob SHA-256 `17d7dbae…`, git blob
`49d06bd3…`; full-register blob SHA-256 `176ca660…`,
git blob `f960d1b2…`. The index's first 20 lines are
byte-identical before and after — appends only. The
gate over the grown tree then read, verbatim: **29
PASS / 0 FAIL / 1 NOT-RUN** (default) and **32 PASS /
0 FAIL / 0 NOT-RUN** (`--regen`), all four V11 legs
PASS, leg (c)'s census line reading "folded census 19
entries = 4 standing record(s) + 8 superseded legacy
record(s) + 2 departed generation(s) accounted by
departure act + 5 canonical re-derivation event(s)".

(b) **A seeded unaccounted run still fails V11(c).**
The new teeth, all passing at this landing:
`test_teeth_v11c_dropped_legacy_generation_unaccounted_fails`
(a legacy entry whose record is dropped, with neither
entry-carried accounting nor a departure act, fails
leg (c) with the standing "neither stands in the
store" finding, every other leg green);
`test_teeth_v11c_departure_naming_an_unknown_run_fails`;
the fold teeth in `test_run_records.py` refusing
departure acts that name an unknown id, name a record
differing from the entry's, account one generation
twice, or carry a malformed commit id or blob hash;
and the builder teeth in `test_legacy_index.py`
seeding the full lifecycle (entered standing →
departed → accounted, third pass idempotent) and the
post-spec skip-with-record against tmp git repos, so
the enumeration is proven against git's own record.

(c) **The standing tree is unmoved.** With no intake
replayed, this landing's tree returns the standing
profile exactly: gate 29 PASS / 0 FAIL / 1 NOT-RUN
(default) and 32 PASS / 0 FAIL / 0 NOT-RUN (`--regen`);
the claims ledger byte-identical (943 lines, SHA-256
`15a5fbad24f400631ace1ebc88bfb7712c9bf6f68fae23e56fedbcac5fd5a794`);
settling canonicals 6/6; the settling store's index
byte-identical (the fix registers the accounting; the
first departure acts are appended by the intakes' own
replays, in their own PRs).

(d) **Full local enumeration.** [OUTPUT INSERTED AT
LANDING — the full backend enumeration on this
landing's tree, run from `backend/` with the phase392
determinism test deselected by its plain nodeid
(`tests/test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`);
clean except the phase133 environmental baseline and
the tray-teardown flake family. The run's summary line
is quoted in the landing PR's body.]

*This does not establish:* that either held intake is
now landed (each replays in its own PR, under its own
record, after this fix merges), or that the departed
pair's recorded results changed in any way (they did
not — the accounting names their departure; their blobs
stand in git history byte-identical), or anything about
what any settling result means.
