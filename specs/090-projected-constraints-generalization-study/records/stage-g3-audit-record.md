# Stage G3 audit record (T404) — Spec 090 (2026-11-12)

**Scope:** tasks.md T404 — the independent audit of the
T403 administration (PR #560, merge commit `e4e32ee9`),
by a worker other than the computer. The auditor's
clone stands at main `e4e32ee9` (non-shallow, clean;
merge-base of HEAD and origin/main is HEAD itself),
assembled from a local bundle of an unrelated clean
clone plus a delta fetch — not from the executor's
working clone. The audit instrument is
`tools/spec090/audit_g3.py`, committed with this
record: it implements P(T) from the freeze record's
§6 alone, the extraction from its §2, the cases from
its §7, and the seed and bijection from its §8. It
does not import or execute `tools/spec090/run_g3.py`;
that tool was read only to learn the run records'
format and the bijection hash's canonical
serialization. Verdicts below come from the audit
script's output, from the committed records, and from
the GitHub API's PR #560 file list, each read directly.

**Overall audit verdict: CONFIRMED.** Every profile
the administration committed reproduces exactly under
independent recomputation from the frozen inputs; the
frozen bar, re-applied to the auditor's own profiles,
yields SEPARATED with the same component table the
outcome record states; and every number the outcome
record quotes that this audit sampled agrees with the
run records. No verdict-bearing number is wrong. Two
grades ride below the headline and are stated where
they belong: the §2(a) double-run claim is UNVERIFIED
as an in-repo claim (its evidence is not in the
repository; §4 below), corroborated in full by the
working evidence outside the repo; and the outcome
record's quoted hashes reproduce under a canonical
form the record does not name (§4 below) — an
observation about the record's completeness, not a
discrepancy in any value.

## 1. Input integrity

Both pinned source files were rehashed in the
auditor's clone:

- Snapshot `glossa-corpus/indus/exports/indus_research.jsonl`:
  SHA-256
  `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`
  — matches freeze §1 exactly.
- M77 flat file `reports/mahadevan_corpus_flat.txt`:
  SHA-256
  `878fd2231929f2105cb5c7fb37507ee7eceb7d83f355f1fa4d8e793926785c18`
  — matches freeze §1 exactly.

The extraction census also reproduces the freeze's §3
in full: 15,508 snapshot records (PennMuseum 7,515;
MetOpenAccess 4,904; `indusscript-m77` 2,906;
`mayig-cisi` 179; ClevelandArtOpenAccess 4); the
empty-list exclusion removes 0 records; every code
element in H1 is a string as recorded (0 non-string
elements, so no coercion question arises); H1 stands
at 2,906 records and 12,639 tokens, the freeze's
permitted counts.

## 2. Independent recomputation

All six tables were rebuilt from the frozen extraction
and case rules and profiled by the audit script's own
implementation. Per case, the recomputed profile is
**identical to the committed run record in all five
components** (inventory size, M, L, X, B):

| Case | Inventory (mine / record) | Components differing |
|---|---|---|
| A0 | 527 / 527 | none |
| A1 | 528 / 528 | none |
| A2 | 526 / 526 | none |
| A3 | 526 / 526 | none |
| C1 | 527 / 527 | none |
| C2 | 527 / 527 | none |

The case constructions reproduce with their facts:
A1 splits code `342` (multiplicity 1,274; exactly 1
initial occurrence, 1,273 other). A2 merges `*015` and
`*267`, each at multiplicity exactly 10 under the
frozen (multiplicity ascending, code ascending)
candidate order — the floor binds as the outcome
record states (375 of the 527 codes sit below the
floor). A3 merges `342` and `000` (1,274 and 680; the
merged type's multiplicity is 1,954 in the recomputed
A3 profile). C2 is the identity. For C1: the seed was
recomputed from the freeze §8 rule — SHA-256 of
`glossa-lab/spec090/g3/c1-relabeling-seed` is
`0b9797c580fd2ca2786c98bcd2fd484b706d178da7968c05de423bf696e501b4`
and its first 8 bytes as an unsigned big-endian
integer give 835303130428943522, both as frozen; the
bijection regenerated from that construction (527
codes sorted ascending, `random.Random(SEED).shuffle`,
codes[i] → shuffled[i]) has SHA-256
`cc4c4803984d60043cace35b473d167c7777c77e47e47d43f28111b0896bc61b`
over the record's canonical pair serialization —
matching the value the outcome record quotes and the
C1 run record carries. (The bijection fixes 2 of the
527 codes; a permutation may fix points, and the
profile is invariant regardless.)

## 3. Bar application

Applied to the auditor's recomputed profiles, the
frozen bar's three conditions read:

- **Distinctness.** (A0, A1) differ in inventory size,
  M, X. (A0, A2) differ in inventory size, M, X.
  (A0, A3) differ in inventory size, M, X, B. L
  differs for no pair. This is the outcome record's
  §4 table, component for component.
- **Invariance.** (A0, C1) and (A0, C2) are identical
  in every component.
- **No count separation.** All six recomputed tables
  stand at 2,906 objects and 12,639 tokens; there is
  no count difference for any component difference to
  run through.

All three conditions hold on the recomputation, so
**SEPARATED follows** — the outcome record's
application of the bar is confirmed, not merely
consistent with the records it cites.

## 4. Record fidelity

The stated sample: §1's run-id table, every headline
value in §3 per case, every number in §4's verdict
section, all twelve SHA-256 values §2(a) and §3
quote, and §2(c)'s identities. Findings:

- §1's six run ids match the six record files, the
  records' own `run.run_id` fields, and
  `run-index.jsonl`, which carries exactly the six
  `entry` acts — one per case, no absence records.
  Every index key pins the freeze record at SHA-256
  `ede853e5ca1036466348a5a5288ec53752dec986fab1d98d043b6702dc124d78`,
  which this audit recomputed from the merged freeze
  file in its clone: it matches, so the runs bind to
  the freeze text as merged, ruling and all.
- §3's values agree with the run records and with the
  recomputation: A0's M head (1274, 680, 615, 342,
  338, 317, 261, 255, 219, 209, 206, 192), 159 hapax
  codes, L in full (1×84, 2×387, 3×633, 4×597, 5×500,
  6×305, 7×205, 8×109, 9×37, 10×27, 11×17, 12×1,
  13×1, 14×3), 3,188 distinct adjacent pairs for A0
  and 3,071 for A3, and L identical across all six
  records.
- All twelve quoted hashes reproduce — the six
  profile SHA-256 values (§3) and the six result-block
  SHA-256 values (§2(a)) — under the canonical JSON
  form `json.dumps(payload, sort_keys=True,
  ensure_ascii=False)` with default separators, over
  the run records' profile and result blocks
  respectively. Observation: the outcome record says
  "canonical serialization" without naming the form,
  and the repository's registered
  `canonical_payload_sha256` (compact separators) does
  **not** reproduce them; the default-separator form
  reproduces all twelve exactly. The values are right;
  the form is now named here so a future reader does
  not have to rediscover it.
- §2(c)'s eight arithmetic identities hold on all
  six committed profiles (checked against each
  record's own object and token totals).
- **§2(a)'s double-run claim, graded.** The six
  verification run records the outcome cites
  (`study-20261112T152017Z-3414a6` …
  `study-20261112T152020Z-d845ea`) are **not in the
  repository**: their ids occur in the repo only
  inside the outcome record's own text. As a claim
  resting on the repository record, §2(a) is therefore
  **UNVERIFIED** — not false: the outcome record
  itself discloses that "the verification store is
  working evidence, not the store of record". The
  working evidence exists and corroborates the claim
  in full: the executor's verification store on disk
  (`~/workspace/glossa-run/g3-run-verification/store`,
  outside the repo) holds exactly those six records,
  each result block hashes to the §2(a) value under
  the canonical form above, and each result block
  deep-equals the corresponding administration
  record's. The verdict of this audit does not rest
  on that leg in any case: §2's independent
  recomputation establishes the profiles directly.

## 5. Discipline checks

- **Claims ledger untouched (C090-23).** PR #560's
  file list, read from the GitHub API, is 11 files —
  the outcome record, the six run records, the run
  index, the two tools, and the root LEDGER entry —
  and contains no claims-ledger file. In the stronger
  form: `glossa-indus/ledger/claims.jsonl` is
  byte-identical between PR #560's base (`96894f9c`)
  and its merge (`e4e32ee9`), SHA-256
  `378f700dba87f0bde2cc6ddfa321e819e4fe204fffe015257698c58e63901d6f`
  at both, 995 lines. The landing's claims-ledger
  diff is empty, as C090-23 requires.
- **The §3.1 overlap item.** The outcome record §5
  carries it exactly as frozen — "not measurable by
  the specified route", the two populations side by
  side (2,906 H1 records; 1,669 flat-file
  inscriptions), no number. No substituted method
  appears anywhere in the outcome record, and
  `run_g3.py` computes nothing over the flat file (it
  hash-verifies the pin and stops there; the file
  contains no overlap code at all).
- **The §5 disclosure and the capped C090-19.**
  Outcome §5 restates the Spec 076 adjacency in
  substance (its length profile and positional
  aggregates, its dropping construction, the
  enumerated verification, the owner's 2026-11-12
  ruling) and carries the capped sentence: the
  profiles "are the first computed under Spec 090's
  separator over a set held out from Spec 090's own
  design process under the enumerated criterion, with
  one adjacent length profile under a different token
  construction pre-existing in the frozen records" —
  not a first-profile-by-anyone claim at full
  strength, as the ruling requires.
- **The hand-check.** `tools/spec090/check_g3.py`
  was run in the auditor's clone: exit 0, 16 PASS
  lines, "all hand-checks passed" — the outcome
  record's §2(b) statement. This audit also
  re-derived the docstring's A0 toy profile in full
  and the A1 and A3 pair spectra by hand from the
  freeze's definitions; they agree with the stated
  hand values.

## 6. Ledger gate on this audit's final tree

Run with the CI-faithful venv interpreter from the
repo root, full mode first, the tree restored between
modes per the standing run-order caveat:

- Full: `summary: 29 PASS / 0 FAIL / 1 NOT-RUN / RESULT: PASS`
- `--regen`: `summary: 32 PASS / 0 FAIL / 0 NOT-RUN / RESULT: PASS`

The standing profile, unchanged by this landing;
`run_settling.py verify-canonicals` was not re-run by
this audit (no settling surface is touched).

*T404's "does not establish" line:* this audit
establishes that the T403 administration was executed
and recorded as the freeze specifies and that its
outcome follows from its profiles. It does not
re-adjudge the package's design judgment (the ANALOGY
pressure the outcome record names stands as the
reader's to weigh), and it establishes nothing about
the Indus script, which remains undeciphered.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
