# Spec 014 — Phase-115: Non-SA Validation Battery v2 for the 44 SA-Lineage Anchors (pre-registration)

**Status:** FROZEN 2026-10-07 on `phase/nonsa44-validation-v2`
(from main `5d8f5d58`). Owner authorization: Tristen Pierson,
2026-10-07 ("continue fully", following his approval of the
Phase-113 outcome and its recorded successor paths). This spec is
committed alone, before any battery-v2 code is run against any
anchor and before any calibration or validation statistic exists
under it. Git order is the pre-registration proof.

**Phase-numbering note:** ledger-sequence **Phase-115**.
Phase-113 (spec 011) is the rejected battery this phase succeeds;
Phase-114 is reserved for the adversarial blind-affiliation study
(spec 012, separate worktree). Artifact names carry the phase
number (`phase115_battery`, `phase115_run`,
`phase115_build_layer_v2`, graph node
`IndusPhase115NonSaValidation`).

**AI disclosure:** this study is designed for execution by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.

## Context — why this phase exists, and what Phase-113 measured

Phase-113 (spec 011) froze a three-test non-SA battery (T1
cross-corpus consistency, T2 positional-grammar fit, T3
compositional co-occurrence) for the 44 anchors Phase-109 flagged
`pending_non_sa_validation`, and calibrated it before use. The
battery was **REJECTED at calibration**: the STRICT94 positive
control validated 3/94 (frozen gate ≥ 57) while the KUR113
negative control passed (0/113 ≤ 5). The 44 were never run; the
anchors file is untouched; all 44 remain flagged.

Phase-113's recorded diagnosis, which this spec is built on:

- **T2 is sound** (profile-fit component passes 91/94 strict
  signs). **T3's legality component never fires** on real
  compositions; its binding constraint is partner support.
- **T1 failed on data, not on anchors.** 61/94 strict signs were
  NOT_ATTESTED in the ICIT converted layer (45 with zero tokens)
  and 22 of the 33 attested failed agreement. The layer (Phase-107
  builder) held only 1,007 inscriptions / 2,238 tokens from 5,679
  source inscriptions, at 69.3% token-map coverage.
- Phase-113's summary and ledger record exactly two successor
  paths: **rebuild T1 on a fuller ICIT layer**, or **scale
  attestation floors to measured layer coverage** — by new spec,
  never by patching the rejected run. This phase does both, and
  nothing else: T2, T3, the calibration gates, and the decision
  rule are carried over from spec 011 unchanged.

Governance rule **H26** still frames the question: SA agreement
is not evidence for sign values, so the 44 stand or fall on
non-SA tests alone. This phase validates or demotes; it never
promotes (a VALIDATED_NON_SA outcome changes only
`validation_status`, with an H26 evidence reference; tiers are
unchanged by validation, and DEMOTE moves an anchor to
CANDIDATE).

## 1. Diagnosis of the v1 layer loss (measured pre-freeze; corpus-level only)

The Phase-107 builder (`backend/scripts/phase107_build_layers.py`)
converts the field-cady MIT mirror of the ICIT (Lipi) export,
`inscriptions.csv` (5,679 inscriptions; 19,942 sign codes, all
zero-padded 3-digit groups in the `text` field — delimiter-split
parsing and the builder's regex extraction agree on all 19,942).
Its losses, decomposed by a read-only diagnostic run before this
freeze (token counts over the full source):

| Cause | Tokens | Nature |
|---|---|---|
| Mapped as built (direct + chain) | 12,506 | — |
| **Leading-zero key mismatch** | **4,014** | The CSV writes Wells codes zero-padded (`002`, `032`); the canonical registry's Wells keys are integer-normalized (`2`, `32`). The v1 lookup used the raw padded code, so **every sub-100 Wells sign failed lookup** — disproportionately the *common* signs. Pure key-normalization defect. |
| Placeholder `000` (illegible) | 1,881 | Excluded by design in v1 — but v1 excluded the *whole inscription*, discarding its legible signs too. |
| Registry multi-M entries | 532 | Wells signs whose registry row lists several Mahadevan ids and whose Parpola chain does not resolve (Parpola id absent from crosswalk v2). No deterministic in-repo resolution. |
| Not in registry at all | 926 | 216 distinct Wells codes (incl. `999`, the source's blank/break marker, 17 tokens) with no canonical-registry row. No in-repo resolution. |
| Broken Parpola chain | 83 | Wells→Parpola known; Parpola id absent from crosswalk v2. |

Inscription-level consequence in v1: the all-or-nothing rule (one
unmapped code or one `000` discards the inscription) kept only
1,242 of 5,679 inscriptions fully convertible; Holdat/intra
dedupe left 1,007 inscriptions / 2,238 tokens.

Other in-repo crosswalks were examined for the residual codes
(`sign_crosswalk_master.csv`, `sign_registry_master.csv`,
`sign_inventory.csv`): they are Parpola-centric subsets of the
same registry and do not deterministically extend Wells
coverage. The canonical registry + crosswalk v2 remain the only
conversion sources (as in Phase-107).

## 2. The v2 converted layer (frozen build policy)

Builder: `backend/scripts/phase115_build_layer_v2.py`, a
deterministic extension of the Phase-107 builder. Inputs are the
same lawfully held local files (field-cady MIT mirror; canonical
registry; crosswalk v2; Holdat via the existing loader). Output:
`corpora/downloads/icit_fieldcady/icit_converted_v2.json` +
`corpora/downloads/layer_build_meta_v2.json` (both gitignored;
the v1 layer file is not modified). **Statistics only are
published; source texts are never committed** (publication
discipline).

Policy, in order:

1. **Parse:** all `\d{3}` groups of the `text` field, file order.
2. **Normalize:** lookup key = `str(int(code))` (repairs §1's
   mismatch). The registry side already uses this normalization
   (Phase-107 `wells_maps`).
3. **Placeholders:** codes `000` and `999` — the source's own
   non-sign encodings (illegible / blank, per the field-cady
   `xlits.csv` table) — become the sentinel token `UNK`, which
   occupies its position (preserving the positional geometry of
   neighbouring signs) and is never a tested sign.
4. **Map:** normalized key → registry Wells→M (single-valued
   entries only) → else registry Wells→Parpola (single-valued)
   → crosswalk v2 Parpola→M (highest-confidence entry; the
   Phase-107 rule). Unmapped non-placeholder codes also become
   `UNK` positions; **the inscription is retained** (this
   replaces v1's all-or-nothing rule).
5. **Drop** inscriptions with zero mapped tokens (counted).
6. **Dedupe** (file order, keep first; Phase-107's independence
   rule, extended):
   - *vs Holdat:* an inscription of length ≥ 3 with ≥ 2 mapped
     tokens is dropped if a Holdat inscription of the same
     length matches it at every mapped position. (Holdat
     sequences carry no sentinels; any completion of the
     candidate consistent with a Holdat inscription is a
     possible duplicate of an independently compiled
     transcription of the same artifact.) For sentinel-free
     candidates this is exactly v1's exact-match rule.
   - *intra-layer:* exact equality of the emitted sequence
     (sentinels included), length ≥ 3 (v1's rule). Wildcard
     matching is **not** used intra-layer: two distinct ICIT
     inscriptions may share every mapped position while
     differing at sentinel positions.
   - Inscriptions below these thresholds are kept (limitation
     registered in §8).

**Measured layer (prototype build of exactly this policy,
executed pre-freeze at corpus level; the shipped builder must
reproduce these numbers exactly, asserted at run time):**

| Measure | v1 (Phase-107) | v2 (this policy) |
|---|---|---|
| Source inscriptions / tokens | 5,679 / 19,942 | 5,679 / 19,942 |
| Token-map coverage excl. placeholders | 69.3% (12,506 / 18,061) | **91.554%** (16,520 / 18,044) |
| Kept inscriptions | 1,007 | **4,531** |
| Kept mapped tokens | 2,238 | **13,492** |
| Kept sentinel tokens | 0 | 2,388 |
| Distinct M-signs attested | not recorded | 284 (196 with ≥ 3 tokens) |

Build accounting (v2): placeholders 1,898 (1,881 `000` + 17
`999`); mapped direct 14,085 + chain 2,435; residual unmapped
1,524 tokens; dropped: 270 zero-mapped, 83 Holdat-wildcard
duplicates, 795 intra-layer exact duplicates. The prototype
output was discarded; the shipped builder rebuilds the layer
and its byte-identical reproducibility is verified by building
twice and comparing hashes (recorded in the PR).

**Pre-freeze measurement boundary:** every number above is a
corpus-level aggregate (layer size, coverage, build accounting).
No per-anchor or per-set attestation statistic was computed
before this freeze; the opportunity formula of §4 is defined
from first principles and the Phase-113 published aggregates,
not from any v2 calibration peek.

## 3. Sets (frozen definitions — identical to spec 011 §2, recomputed and asserted)

- **FLAGGED44** — `validation_status == "pending_non_sa_validation"`;
  asserted 44 (24 SA_DERIVED + 20 SA_CONFIRMED_ONLY; 43 HIGH +
  M293 MEDIUM).
- **STRICT94** — register category ∉ {SA_DERIVED,
  SA_CONFIRMED_ONLY} ∧ `sa_in_chain == false` ∧ tier ∈ {HIGH,
  MEDIUM}; asserted 94 (90 HIGH + 4 MEDIUM), disjoint from
  FLAGGED44, Holdat token coverage 0.7368 ± 0.001 (5,159/7,002).
- **KUR113** — `validation_status == "premise_superseded"`;
  asserted 113, all reading `kur`.

## 4. The battery v2 (frozen)

Conventions (profiles, modal class, tie order, TV, reading
normalization, syllable canon) are spec 011 §3 verbatim,
implemented by reusing `phase113_battery` machinery. Positional
profiles on the v2 ICIT layer are computed over the emitted
sequences **including sentinel positions**: a sentinel occupies
its slot, so a mapped sign's INITIAL/MEDIAL/TERMINAL class is
taken against the inscription's full length (the geometry the
sign actually sits in).

### T1 v2 — Cross-corpus consistency (v2 layer vs Holdat), opportunity-scaled floor

Let `M_I` = mapped (non-sentinel) tokens in the v2 layer
(13,492), `T_H` = Holdat tokens (7,002), and
**r = M_I / T_H** (recomputed at run time from the built layer;
expected ≈ 1.9269). For sign `s` with Holdat count `n_H(s)` and
v2-layer count `n_I(s)`:

- **Opportunity** `O(s) = r · n_H(s)` — the ICIT count `s` would
  carry if the layer sampled inscriptions in proportion to
  Holdat presence.
- **Attestation floor** `floor(s) = 1` if `O(s) < 3`; `2` if
  `3 ≤ O(s) < 9`; `3` if `O(s) ≥ 9`. (The floor never exceeds
  the Phase-113 absolute floor of 3, and never exceeds roughly
  a third of the sign's expected attestation: a sign is judged
  on the attestation it had a fair chance to produce, and no
  sign is failed for attestation it never had the chance to
  make.)
- If Holdat has no profile for `s` → **NOT_ATTESTED**
  (reason `sign_absent_holdat`; no comparison exists).
- If `n_I(s) < floor(s)` → **NOT_ATTESTED**.
- Else judge consistency exactly as spec 011: PASS iff modal
  class on the v2 layer == modal class on Holdat **and**
  TV(profile_v2(s), profile_Holdat(s)) ≤ **0.40**.
- **Stability guard:** if the judgment is disagreement but
  `n_I(s) < 3`, the state is **NOT_ATTESTED** (reason
  `below_stability_floor`), never FAIL — a profile of one or
  two tokens cannot carry a demotion. (Consequence, registered
  here: since T2 PASS requires `n_H(s) ≥ 8`, hence
  `O(s) ≥ 9`·(8·r/… ) — precisely, `O(s) ≥ 8r ≈ 15.4`, hence
  `floor(s) = 3` — the sub-3-token PASS path can never
  contribute to a VALIDATED_NON_SA outcome; it affects only
  the recorded T1 state of UNRESOLVED anchors. FAIL under T1
  v2 always rests on ≥ 3 tokens, exactly as in Phase-113.)

T1 v2 records per sign: `n_icit_tokens`, `opportunity`,
`floor`, `modal_holdat`, `modal_icit`, `tv`, and `reason` where
applicable.

### T2 — Positional-grammar fit: **spec 011 verbatim** (guard `n_H < 8`; T2a centroid TV ≤ 0.35, modal share ≥ 0.45; T2b phonotactics incl. Phase-58 initial check and canon legality).

### T3 — Compositional co-occurrence: **spec 011 verbatim** (partner co-occurrence ≥ 2; support FAIL ≤ 1 / PASS ≥ 3; contexts ≥ 4; legal fraction 0.75).

No test consults any SA artifact, any anchor's `basis` text, or
any prior phase's verdict about the tested sign (H26).

## 5. Calibration gates (frozen — identical to spec 011 §4)

- **Positive:** STRICT94, leave-one-out. Acceptance: VALIDATED
  (§6 rule) ≥ **57 of 94** (60%).
- **Negative:** KUR113 against STRICT94 as-is. Acceptance:
  VALIDATED ≤ **5 of 113**.

If either gate fails, the battery is **rejected**: the phase
stops, FLAGGED44 is never run, the anchors file is not modified,
and results/summary/ledgers record the rejection with the
calibration numbers. A rejected battery may not be re-tuned and
re-run under this spec.

## 6. Decision rule (frozen — spec 011 §5, mechanically applied to FLAGGED44)

- **VALIDATED_NON_SA** ⟺ T1 = PASS ∧ T2 = PASS ∧ T3 = PASS.
  Action: `validation_status` := `validated_non_sa`;
  `evidence_ref` appended (Phase-115, spec 014); tier unchanged;
  `phase115_annotation` records outcome + per-test states.
- **DEMOTE** ⟺ any test = FAIL. Action: `confidence` :=
  CANDIDATE; `validation_status` := `failed_non_sa_validation`;
  annotation records the failed test(s) and statistics.
- **UNRESOLVED** ⟺ otherwise. Action: no tier change; status
  stays `pending_non_sa_validation`; annotation records
  UNRESOLVED with per-test states.

Every action (and every UNRESOLVED non-action) is one change-
register record. No other anchor or field is modified.

## 7. Execution order (frozen)

1. This spec committed alone (pre-registration).
2. Layer builder `backend/scripts/phase115_build_layer_v2.py`;
   build executed; byte-identical rebuild verified; build meta
   asserted against §2's measured values.
3. Implementation: `backend/glossa_lab/phase115_battery.py`
   (T1 v2 + reuse of spec-011 machinery for T2/T3/decision),
   `backend/glossa_lab/phase115_run.py` (orchestration +
   reports), runner `backend/scripts/phase115_nonsa_battery_v2.py`;
   unit tests `backend/tests/test_phase115_battery.py`.
4. H23 gate, in order: script written → graph module
   `backend/glossa_lab/experiment_graph_phase115.py` (node
   `IndusPhase115NonSaValidation`) → registration in
   `experiment_graph.py` → registration asserted in
   `ATOMIC_NODES` → only then any run.
5. Calibration (§5). If rejected: write reports + ledgers, stop
   (no step 6).
6. Main run on FLAGGED44; apply §6; write reports + change
   register; update the anchors file (bookkeeping regenerated
   from entries, Phase-113 pattern; changed-entries ==
   change-register signs, asserted).
7. Full backend suite + foundation check (H21). Ruff clean
   before push.
8. Ledger entries (root `LEDGER.md` and `glossa-indus/LEDGER.md`,
   AI disclosure) and one PR. No merge without the owner's
   explicit say-so.

Determinism: builder and battery are pure counting and set
membership in file order — no sampling, no RNG. Re-running on
the same inputs reproduces the reports byte-identically except
timestamps; the layer file itself is byte-identical across
rebuilds (verified, step 2).

## 8. Limitations and epistemic boundaries (H13, registered at freeze)

- **What a PASS / FAIL means** — as spec 011 §8: distributional
  and compositional survival (or contradiction) under non-SA
  tests; not proof or disproof of a phonetic value. The KUR113
  gate, not rhetoric, decides whether the battery discriminates
  lineage rather than rewarding frequency.
- **Sentinel geometry assumption:** profiles on the v2 layer
  treat unmapped/placeholder positions as occupied slots. This
  matches the artifacts (a sign stood there) but the v1 layer
  instead measured only fully legible inscriptions; T1 v2 and
  T1 v1 therefore measure slightly different populations, and
  their numbers are not directly interchangeable.
- **Dedupe bounds:** inscriptions of length < 3, and partial
  inscriptions with < 2 mapped tokens, are not Holdat-deduped;
  a bounded number of cross-corpus duplicates may survive
  there. Intra-layer dedupe is exact-only (rationale in §2.6).
- **Floor bands are a frozen design choice**, set from the
  measured sampling ratio before any calibration statistic
  existed. No sensitivity analysis over alternative bands is
  permitted post-hoc under this spec; if the battery is
  rejected, the bands die with it.
- **Conversion residue:** 1,524 source tokens (216 distinct
  Wells codes) have no deterministic in-repo mapping and enter
  only as sentinel positions; 532 further tokens sit under
  registry multi-M entries resolvable only by a judgment call
  this phase refuses to make. Coverage claims are bounded
  accordingly (91.554% of non-placeholder tokens).
- **Corpus caveats (carried from spec 011):** Holdat and the
  ICIT layer are independent compilations of the same published
  catalogues, not independent archaeology. STRICT94 as the
  reference core rests on the Phase-108/109 provenance audit.
- **Assumptions declared:** reading order = corpus sequence
  order; the Phase-69 I/M/T convention; the §4 syllable canon
  (via spec 011) as the operative Proto-Dravidian syllable law;
  `999` is a non-sign blank (source repo's own encoding table).

## 9. Licensing / data handling

The field-cady corpus is MIT-licensed; the canonical registry
and crosswalk v2 are in-repo artifacts. Holdat and both ICIT
layers are used locally under their recorded terms
(Phase-107 acquisition log); no corpus file is committed or
redistributed by this phase. Published artifacts contain only
counts, shares, distances, floors, and verdicts.

## 10. Deliverables (frozen)

- `specs/014-phase115-nonsa44-validation-v2/{spec,plan,tasks}.md`
- `backend/scripts/phase115_build_layer_v2.py` (+ gitignored
  layer + meta under `corpora/downloads/`)
- `backend/glossa_lab/phase115_battery.py`,
  `backend/glossa_lab/phase115_run.py`,
  `backend/glossa_lab/experiment_graph_phase115.py`
  (+ registration)
- `backend/scripts/phase115_nonsa_battery_v2.py`
- `backend/tests/test_phase115_battery.py`
- `reports/phase115_nonsa44v2_results.json`
- `reports/phase115_nonsa44v2_change_register.json` (iff the
  main run executes)
- `reports/phase115_nonsa44v2_summary.md`
- Anchors-file changes per §6 (iff calibration passes)
- Ledger entries in `LEDGER.md` and `glossa-indus/LEDGER.md`
- One PR; suite + foundation results recorded in the summary
