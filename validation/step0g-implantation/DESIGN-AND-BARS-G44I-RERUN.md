# DESIGN AND BARS — G44-I VALIDATION, RERUN UNDER AMENDMENT 1 (execution record for the desktop package)

**Status: execution record for the rerun commissioned by the owner's word of 2026-10-27 ("Amend G44-I and rerun the validation"), routed to TRISTEN-DESKTOP through the Syncyard gatekeeper under the fleet compute-split directive (2026-10-27). This record is written and hashed BEFORE the run. The run executes only from the packaged script `g44i_rerun.py`; this record, the amendment, and the script's embedded constants must agree exactly.**

## Governing documents (hashes verified at package time)

- Draft: `2026-10-26-spec-draft-step0g-implantation-instrument.md`, SHA-256 `53b4ae9e3b00c13643057119b073a8fa14af8216101928608f66a6e2125389da` — unedited.
- Halt record: `2026-10-26-g44i-validation-record.md`, SHA-256 `b765a1fdebf8a9ae787da1abbfe87c0e8542509df7855fc54e2e8f8ea7bef0b8` — unedited.
- **Amendment 1**: `2026-10-27-spec-draft-step0g-implantation-amendment1.md`, SHA-256 `b1bdb05319e844eac02ca9a01d60230f35e9e8c32703148fd1dc36075008e670`. The amended design = draft + amendment; the amendment governs the parameter family.
- First run's design-and-bars record (SHA-256 `2a393f9f…`): all implementation pins carry over unless this record or the amendment states otherwise (selection semantics, evidence definition, leg-3 arm pins as adapted in §5 below, stream orders).

## 1. The amended parameter family (recap; the amendment is authoritative)

- ONLY: draw weight 0.04; **at most one** ONLY-planted sign (excess reassigned by the draft's deterministic rule); ONLY cell per compilation = min(round-half-up(a × quota), C_max), **C_max = floor(min(30, 25% of that compilation's solo slots))**; a_eff recorded; **spillover zero** for non-ONLY signs; feasibility precondition **C_max ≥ 10 in both compilations** when an ONLY-planted sign is in the ledger (violation = design-record halt at ledger construction).
- Quotas: uniform integer **[12, 18]** every sign, both compilations; budget scaling floor 12; the 20% budget rule and the per-source cap (§4.5) unchanged.
- Neighbor classes: uniform over the eligible set **{FIRST, MIDDLE, LAST}** (Amendment 1 census: P(FIRST) 706, P(MIDDLE) 2,900, P(LAST) 513, **P(ONLY) 0**); **at most 12 signs per neighbor class**, excess in label order reassigned to MIDDLE, recorded.
- Masses by final neighbor class: **FIRST/LAST uniform(0.50, 0.68); MIDDLE uniform(0.55, 0.80)**.
- Feasibility verification at ledger construction (halt before implantation on any failure): §4.3 margins; per-compilation aggregate and per-class demand vs per-source-cap capacity; the C_max precondition.
- Concentrations: uniform(0.55, 0.85) non-ONLY position classes; uniform(0.55, 0.70) ONLY — as drafted.
- **Bars, gate tolerances, certification rule, kill criteria, scorer, selection algorithm, order of operations: unchanged** (draft §§6, 7, 9; amendment §7).

## 2. Fresh seeds (drawn after the amendment was hashed)

Drawn 2026-10-27 from operating-system entropy (Python `secrets.randbelow`), uniform in [20280000, 20289999], checked disjoint from every spent seed (G44 20261026–31; G44-S 20261201–05; G44-S2 20270111–17; G44-I run 1: 20270321–24; Amendment-1 design seeds 20271001, 20271101–20271124):

| Stream | Seed |
|---|---|
| Model (ledger) | **20280865** |
| Split | **20281686** |
| Leg-2 null | **20281727** |
| Leg-3 null | **20284065** |

The split is fresh: within each inscription-length band, indices (ascending) are shuffled by Random(split seed) — one stream across bands in ascending band order — the bands concatenated in ascending length order, then dealt alternately (even positions fitting, odd scoring). This keeps the first run's length-stratified discipline with fresh membership driven by the split seed; the halted run's published split is not reused.

## 3. Pinned input

`population.json` beside the script — SHA-256 `f1d984c546c77bbd5459895e9ab31b877dd7a2af69a88ff4248049bf11e8811c`, 177,030 bytes. It is the population built at package time by the first run's stage-1 construction from the same pin-verified inputs (Mahadevan M77 text `ec802ad3…`; Fuls concordance JSON `b27ee60f…`; grades TSV `512b067d…`; signary registry `773f33a4…` — pins verified against live files on 2026-10-26 in the first run and recorded in its design-and-bars record; the population derives from the program's published working frame, not from restricted material). The script verifies the file's SHA-256, then asserts step 0 exactly: **3,045 inscriptions / 557 signs / 11,805 tokens / 550 signs in inscriptions of length ≥ 2**. Any mismatch exits before any draw (exit 2).

## 4. Execution order and halt rules (the script enforces these)

S0 input pins + step 0 → S1 split + ledger + feasibility battery (any failure: design-record halt, marker `G44I_HALT`, exit 3, no implantation) → S2 fitting implantation → final fitting profiles → in-run census printed (eligibility per §4.7 against the drawn ledger's classes; the amended draw plants no ONLY neighbor classes; if the in-run census found FIRST, MIDDLE, or LAST ineligible, the amended design has no rule and the run halts as a design-record event) → ledger finalized → S3 scoring implantation → S4 independent-recount gate (failure: verdict **INCOMPLETE — IMPLANTATION DEFECT**, no legs) → S5 legs 1, 1B, 2 → S6 leg 3 (calibration gate printed first; calibration failure: leg 3 does not run, verdict **INCOMPLETE** per draft §7.1) → S7 OD-1 quantities + K3 check + verdict.

The gate auditor is the independent recount implementation (Amendment 1 scratch `auditor.py`, embedded in the script): it shares no functions with the implantation code and runs with its own 5% R3 spot-check draw (Random(777)).

## 5. Leg-3 pins (carried from the first run's record, with the amended draw)

Fake background: the G44-S SIGIL-class generator, carried verbatim (tiers 4×500, 20×150, 80×40, 325×8, 128×7 = 11,696 tokens; 557 types; deal stride 4531; length counts {1:244, 2:521, 3:759, 4:600, 5:380, 6:230, 7:145, 8:85, 9:52, 10:29}; length stride 1124; the fake length-1 band 0.06–0.10 is a property of the carried construction and is NOT re-derived from the real frame). Fake split: alternate dealing of the generated order. Calibration (draft §7.4): the generator's five construction checks are printed before either arm runs and all must pass — inscriptions exactly 3,045; distinct types exactly 557; total tokens in 11,215–12,395; most-frequent-type share ≥ 0.04; length-1 share within the band [0.06, 0.10] pinned in the first run's record for this carried construction. If any check fails, neither arm runs and the run files INCOMPLETE with leg 3 outstanding; the generator is never tuned after the fact. The arms' batch signs are the 44 most frequent fake fitting types (count descending, then type id ascending). Arm 3A: batch = that baseline assignment; certification against a fresh Random(leg-3 seed) null. Arm 3B: a working ledger is drawn from a fresh Random(model seed) stream under the **amended** §4 draw (Amendment 1 changed the draw; the working ledger follows the governing record as amended), its k-th entry in label order paired with the k-th batch type in frequency order; the fake fitting compilation is implanted with it; the arm's planted pairs are then set to the designated types' own baseline pairs on the implanted fake fitting compilation; cells for the fake scoring implantation are recomputed toward the substituted position classes with the amended cell construction (quotas and concentrations from the working ledger); §4.7 eligibility is NOT applied to substituted pairs; the arm's null is a fresh Random(leg-3 seed) stream, separate from arm 3A's. Leg 3 passes only if both arms return NOT certified.

## 6. Checkpoints, resume, markers

The script writes one checkpoint per stage under `output/` beside itself, each carrying the configuration hash (SHA-256 over the seeds, the population hash, and the amendment hash). Re-running the script verifies and skips completed stages and continues from the last checkpoint; a configuration mismatch refuses to resume (exit 4). It is non-interactive, creates no windows, uses only the Python 3 standard library, and reads no path outside its own directory except its `output/` folder.

Marker lines (stdout and appended to `output/markers.txt`):

```
G44I_STAGE <S0..S7> DONE|SKIPPED sha256=<checkpoint hash>
G44I_HALT <reason>                       (design-record halt, exit 3)
G44I_GATE PASS|FAIL R1=<..> R2s_max=<..> R2s_fam=<..> R2f_max=<..> misses=<..> R3=<..> R4=<..>
G44I_LEG1 B=<..> recovered=<n>/44 mean_pos=<..> mean_nbr=<..> PASS|FAIL
G44I_LEG1B B_baseline=<..> margin=<..> PASS|FAIL
G44I_LEG2 p95=<..> share_ge=<..> PASS|FAIL
G44I_LEG3_CALIB insc=<..> types=<..> tokens=<..> top=<..> len1=<..> PASS|FAIL
G44I_LEG3 arm3A_certified=<0|1> arm3B_certified=<0|1> PASS|FAIL|NOTRUN
G44I_OD1 full=<n> pos_only=<n> nbr_only=<n> margin=<..>
G44I_K3 TRIGGERED|CLEAR
G44I_VERDICT <text>
G44I_DONE
```

## 7. Verdict vocabulary (draft §7.5, applied mechanically)

Gate failure → `INCOMPLETE — IMPLANTATION DEFECT`. Leg-3 calibration failure → `INCOMPLETE` (fake background could not be administered). Legs 1, 2, or 3 failing → `FAILED`. All legs passing → the certification call involving leg 1B is **held for OD-1** (the owner's open decision, draft §8): the script reports the leg-1B numbers and both readings (`VALIDATED` if leg 1B certifies as printed, with the K3 flag appended if K3 triggers; `FAILED` under the reading where a failed leg 1B decertifies). The final single-word verdict is entered in the rerun record after harvest, with the OD-1 status recorded — the script does not usurp the owner's decision.

**Expectation, on the record:** Amendment 1 §6 measures this design's gate to fail at R2 on typical draws (168 design draws, zero passes; the final-rules design draw failed on per-sign tails alone). This package is dispatched with that record in hand; the dispatch decision belongs to the owner/parent, and a gate failure here files the FIRST of KI-1's two strikes. Nothing in this record softens that expectation.

**Fences:** the real 44 anchors are never scored (the designated signs are synthetic G44I-01…44; leg 3's are fake types); the scorer is unchanged; restricted data is not in this package (the population derives from the published working frame); the protected local checkout is not used.
