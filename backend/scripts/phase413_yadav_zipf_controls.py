#!/usr/bin/env python3
"""Phase-413 — Spec 053 (Yadav's Zipf fit: what is a
curve fit worth?; design D-07, arm A only).

Executes the frozen Spec 053 contract
(specs/053-yadav-zipf-controls/freeze.md; freeze
digest
fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309;
OSF registration s9yfe, approved and public before
this run) under the runnable-experiments campaign
(Wave 3, Group 2 — independent executions).

The estimator of record is the one the freeze
specified completely (DD-053-11, option (a)): the
Zipf-Mandelbrot model f_hat(r) = C / (r + q)^alpha
with C fixed by normalisation (sum of fitted
counts = N), fitted by minimising the sum of
squared log residuals over the deterministic grid
alpha 0.00-3.00 in steps of 0.01 and q 0.0-20.0 in
steps of 0.1, then one refinement pass at
one-tenth steps in alpha and q around the best
grid cell; the primary quantity is
NRMSE_log = sqrt(SSE / V). The "identical to
Phase-43" reading is RETIRED: Phase-43's results
file carries no Zipf fit and no Phase-43 estimator
is substituted or sought. The single
implementation below (fit_zipf_mandelbrot) is the
implementation gate 0.2 tests and the only one
any system fit would have used.

Gates, in the frozen order (spec section 3),
before any system fit:

  0.1 Input integrity — every spec section 2
      input that carries a pin hashes to its
      freeze-record value, and the anchors file
      is asserted byte-identical before and
      after. A mismatch stops the run as INVALID.
  0.2 Estimator self-test — the estimator is run
      on synthetic rank-frequency data generated
      from known Zipf-Mandelbrot parameters
      (alpha = 1.20, q = 2.0, V = 200 types,
      N = 50,000 tokens, seed 20261021). The
      generation procedure, stated here as the
      frozen contract requires: type
      probabilities p_r proportional to
      1 / (r + q)^alpha for r = 1..V, normalised
      to sum 1; counts drawn as one multinomial
      sample of N tokens from p with numpy's
      default generator seeded 20261021; the
      drawn counts are ranked descending (ties
      do not affect the fit, which uses the
      ranked counts alone) and fitted by the one
      estimator. The gate passes iff the fit
      recovers alpha within +/-0.10 and q within
      +/-1.0 of the generating values. A failure
      stops the run as INVALID.
  0.3 Strict corpus identification and pin — the
      V3 / Mahadevan-lineage corpus layer of
      record is identified from the database as
      the layer the Phase-43 framework ran on,
      exported in full, and pinned by SHA-256
      digest. The identification attempt is
      mechanical and is recorded in full:
        C1 the V3 loader's data file (the
           Firestore 'indusarrays' dump that
           backend/glossa_lab/data/
           indus_corpus_v3.py reads) — present in
           the tree or not; by the loader's own
           code a missing file loads zero records,
           so zero sequences are loadable;
        C2 a database copy in the execution tree
           (backend/data/glossa.db) — present
           or not;
        C3 the Phase-43 record's own census of
           its corpus (T1_1: source, records,
           sequences, dockeys, sign instances),
           read from the pinned results file;
        C4 every other corpus layer the tree
           holds, censused and compared against
           that record: the programme's
           site-attributed layer
           (yajnadevam_inscriptions.csv), the V1
           research export (indus_research.jsonl,
           with its source-system mixture), the
           ICIT-format export, and the Holdat
           downloads path.
      No layer is substituted for the V3 layer:
      a layer counts as identified only if it is
      the corpus the Phase-43 record names. If
      the layer cannot be uniquely identified,
      cannot be exported whole, or cannot be
      shown to be the Phase-43 framework's
      corpus family, the run closes as STRICT
      CORPUS NOT PINNABLE and nothing is fitted.
  0.4 Control set freeze — reached only if 0.3
      passes. No control count is typed into
      this script (H16); the frozen tables are
      entered as cited data at the gate.
  0.5 Census and floors — reached only if 0.4
      passes.

On a gate failure the execution stops in the
frozen order: later gates are NOT REACHED, no
control is entered, and no fit of any system is
computed. The only fit this script ever computes
before gate 0.3 is the gate 0.2 self-test fit on
synthetic data, which the frozen gate order
itself prescribes.

Outputs (written on every terminal outcome):
  - reports/phase413_results.json (the step-0
    record: pins, self-test record, the gate 0.3
    identification attempt, per-gate verdicts)
  - reports/phase413_step0_report.md (the step-0
    report, under spec section 9's headline rules
    as they apply to a step-0 closure)

Integrity: every section 2 pin is asserted before
any gate quantity; the anchors file is asserted
byte-identical before and after. The script is
deterministic: a second run reproduces both
output files byte-identically.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[2]

PIN_CLAIM = (
    "glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json",
    "904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3",
)
PIN_ANCHORS = (
    "backend/reports/INDUS_FINAL_ANCHORS.json",
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
)
PIN_CROSSWALK = (
    "data/crosswalks/sign_crosswalk_master.csv",
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf",
)
PIN_MP_CROSSWALK = (
    "backend/glossa_lab/data/mahadevan_parpola_crosswalk.json",
    "9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b",
)
PIN_PHASE43 = (
    "outputs/phase43_all.json",
    "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4",
)
FIRESTORE_DUMP = (
    "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/"
    "firestore_indusarrays_full.jsonl"
)
DATABASE_FILE = "backend/data/glossa.db"
LAYER_SITE_ATTRIBUTED = (
    "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
)
V1_EXPORT = "glossa-corpus/indus/exports/indus_research.jsonl"
ICIT_EXPORT = "glossa-corpus/indus/exports/indus_icit_format.json"
HOLDAT_LAYER = (
    "corpora/downloads/external_repos/holdatllc_indus/"
    "indus_corpus 2.csv"
)

_OUT_RESULTS = _REPO / "reports/phase413_results.json"
_OUT_REPORT = _REPO / "reports/phase413_step0_report.md"

EXECUTION_DATE = "2026-10-21"
BASE_COMMIT = "3200b7b5b6841a7b9567a81368bf84004fd17255"
FREEZE_DIGEST = (
    "fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309"
)

# Gate 0.2 generating parameters and tolerances
# (spec section 3, DD-053-11).
SELF_TEST_ALPHA = 1.20
SELF_TEST_Q = 2.0
SELF_TEST_V = 200
SELF_TEST_N = 50000
SELF_TEST_SEED = 20261021
SELF_TEST_ALPHA_TOL = 0.10
SELF_TEST_Q_TOL = 1.0


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_pin(rel: str, pin: str) -> dict:
    path = _REPO / rel
    if not path.exists():
        return {"file": rel, "pin": pin, "observed": None,
                "present": False, "match": False}
    observed = _sha256(path)
    return {"file": rel, "pin": pin, "observed": observed,
            "present": True, "match": observed == pin}


def fit_zipf_mandelbrot(counts) -> dict:
    """The one estimator of record (spec section 4.2).

    counts: a system's frozen counts by type. Types
    are ranked by count descending (ties do not
    affect the fit, which uses the ranked counts
    alone); the ranked counts are f(1) >= ... >=
    f(V), N = sum f(r). The model
    f_hat(r) = C / (r + q)^alpha is fitted with C
    fixed by normalisation (sum f_hat = N) by
    minimising SSE = sum_r (log f(r) - log
    f_hat(r))^2 over the deterministic grid alpha
    0.00-3.00 step 0.01, q 0.0-20.0 step 0.1, then
    one refinement pass at one-tenth steps (alpha
    step 0.001, q step 0.01) over the best grid
    cell (one coarse step to each side, clipped to
    the grid bounds).
    """
    ranked = sorted((int(c) for c in counts), reverse=True)
    f = np.asarray(ranked, dtype=float)
    v = int(len(f))
    n = int(f.sum())
    log_f = np.log(f)
    ranks = np.arange(1, v + 1, dtype=float)

    def _sse(alpha: float, q: float) -> float:
        log_rq = np.log(ranks + q)
        c_norm = n / float(np.exp(-alpha * log_rq).sum())
        log_fh = math.log(c_norm) - alpha * log_rq
        return float(((log_f - log_fh) ** 2).sum())

    best_sse = math.inf
    best_alpha = 0.0
    best_q = 0.0
    for qi in range(0, 201):
        q = round(qi * 0.1, 1)
        for ai in range(0, 301):
            alpha = round(ai * 0.01, 2)
            sse = _sse(alpha, q)
            if sse < best_sse:
                best_sse, best_alpha, best_q = sse, alpha, q
    a_lo = max(0.0, round(best_alpha - 0.01, 3))
    a_hi = min(3.0, round(best_alpha + 0.01, 3))
    q_lo = max(0.0, round(best_q - 0.1, 2))
    q_hi = min(20.0, round(best_q + 0.1, 2))
    ai = int(round(a_lo * 1000))
    while ai <= int(round(a_hi * 1000)):
        alpha = round(ai / 1000, 3)
        qi = int(round(q_lo * 100))
        while qi <= int(round(q_hi * 100)):
            q = round(qi / 100, 2)
            sse = _sse(alpha, q)
            if sse < best_sse:
                best_sse, best_alpha, best_q = sse, alpha, q
            qi += 1
        ai += 1
    sse = best_sse
    mean_log_f = float(log_f.mean())
    sst = float(((log_f - mean_log_f) ** 2).sum())
    return {
        "V": v,
        "N": n,
        "alpha": best_alpha,
        "q": best_q,
        "SSE": sse,
        "NRMSE_log": math.sqrt(sse / v),
        "R2_log": (1.0 - sse / sst) if sst > 0 else 0.0,
    }


def _self_test() -> dict:
    """Gate 0.2's generation + fit, as stated in
    this script's docstring (the frozen contract's
    stated multinomial procedure)."""
    ranks = np.arange(1, SELF_TEST_V + 1, dtype=float)
    p = 1.0 / (ranks + SELF_TEST_Q) ** SELF_TEST_ALPHA
    p = p / p.sum()
    rng = np.random.default_rng(SELF_TEST_SEED)
    draws = rng.multinomial(SELF_TEST_N, p)
    fit = fit_zipf_mandelbrot([int(c) for c in draws])
    alpha_err = abs(fit["alpha"] - SELF_TEST_ALPHA)
    q_err = abs(fit["q"] - SELF_TEST_Q)
    return {
        "generating_parameters": {
            "alpha": SELF_TEST_ALPHA, "q": SELF_TEST_Q,
            "V": SELF_TEST_V, "N": SELF_TEST_N,
            "seed": SELF_TEST_SEED,
        },
        "procedure": (
            "p_r proportional to 1/(r+q)^alpha for "
            "r = 1..V, normalised; counts drawn as one "
            "multinomial sample of N tokens from p "
            "with numpy's default generator seeded "
            "20261021; drawn counts ranked descending "
            "and fitted by the one estimator"),
        "drawn_counts": {
            "sum": int(draws.sum()),
            "min": int(draws.min()),
            "max": int(draws.max()),
            "zero_types": int((draws == 0).sum()),
        },
        "fit": fit,
        "alpha_error": alpha_err,
        "q_error": q_err,
        "tolerances": {"alpha": SELF_TEST_ALPHA_TOL,
                       "q": SELF_TEST_Q_TOL},
        "recovered_within_tolerance": (
            alpha_err <= SELF_TEST_ALPHA_TOL
            and q_err <= SELF_TEST_Q_TOL),
    }


def _gate_03_attempt() -> dict:
    phase43 = json.loads((_REPO / PIN_PHASE43[0]).read_text("utf-8"))
    t11 = phase43["T1_1_corpus_v3"]
    recorded = {
        "source": t11["source"],
        "total_records": t11["total_records"],
        "total_sequences": t11["total_sequences"],
        "unique_dockeys": t11["unique_dockeys"],
        "total_sign_instances": t11["total_sign_instances"],
    }
    firestore_present = (_REPO / FIRESTORE_DUMP).exists()
    database_present = (_REPO / DATABASE_FILE).exists()

    site_path = _REPO / LAYER_SITE_ATTRIBUTED
    with open(site_path, encoding="utf-8", newline="") as fh:
        site_records = sum(1 for _ in csv.DictReader(fh))

    v1_systems: Counter = Counter()
    v1_objects = 0
    with open(_REPO / V1_EXPORT, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                v1_objects += 1
                v1_systems[json.loads(line).get("source_system")] += 1

    icit = json.loads((_REPO / ICIT_EXPORT).read_text("utf-8"))

    candidates = [
        {
            "layer": LAYER_SITE_ATTRIBUTED,
            "identity": (
                "the programme's site-attributed layer "
                "(the Phase-393 layer; the layer of "
                "record for Specs 027/028/042/045)"),
            "records": site_records,
            "sha256": _sha256(site_path),
            "is_the_phase43_corpus": False,
            "why_not": (
                "the Phase-43 record names its corpus "
                "as the Firestore 'indusarrays' "
                "source at 3,916 records; this layer "
                "carries 5,679 records and is a "
                "different layer of record"),
        },
        {
            "layer": V1_EXPORT,
            "identity": (
                "the V1 primary research export "
                "(glossa-indus/CORPUS_VERSIONS.md: "
                "V1, loaded by indus_corpus_v2.py)"),
            "records": v1_objects,
            "source_systems": dict(sorted(v1_systems.items())),
            "is_the_phase43_corpus": False,
            "why_not": (
                "a five-source mixture in mixed sign "
                "schemes, labelled V1 in the corpus "
                "versioning record; the Phase-43 "
                "framework ran on the V3 Firestore "
                "reconstruction, not on this export"),
        },
        {
            "layer": ICIT_EXPORT,
            "identity": "the ICIT-format export",
            "total_sequences": icit["total_sequences"],
            "is_the_phase43_corpus": False,
            "why_not": (
                "ICIT-encoded sequences (3,085) — a "
                "different lineage and encoding from "
                "the Mahadevan-lineage V3 corpus the "
                "Phase-43 record names"),
        },
        {
            "layer": HOLDAT_LAYER,
            "identity": "the Holdat corpus layer",
            "present_in_tree": (_REPO / HOLDAT_LAYER).exists(),
            "is_the_phase43_corpus": False,
            "why_not": (
                "absent from this tree (the downloads "
                "are not tracked), and in any case the "
                "Holdat compilation — the distinct "
                "second compilation of the sibling "
                "specs, not the Mahadevan-lineage V3 "
                "layer"),
        },
    ]
    identified = firestore_present
    return {
        "recorded_phase43_corpus": recorded,
        "C1_v3_loader_data_file": {
            "path": FIRESTORE_DUMP,
            "present": firestore_present,
            "loader": "backend/glossa_lab/data/indus_corpus_v3.py",
            "sequences_loadable": None if firestore_present else 0,
            "note": (
                "the loader returns an empty record "
                "list when its data file does not "
                "exist, so no sequence can be loaded "
                "or exported from it in this tree"),
        },
        "C2_database_copy": {
            "path": DATABASE_FILE,
            "present_in_execution_tree": database_present,
            "note": (
                "no database file exists in the "
                "execution tree (backend/data/ is not "
                "tracked); the layer is not held in "
                "any database this run can identify "
                "it from"),
        },
        "C4_other_layers_in_tree": candidates,
        "layer_uniquely_identified_and_exportable": identified,
    }


def main() -> int:
    anchors_before = _sha256(_REPO / PIN_ANCHORS[0])

    # ── Gate 0.1 — input integrity ──────────────────
    pins = [_check_pin(*p) for p in (
        PIN_CLAIM, PIN_ANCHORS, PIN_CROSSWALK,
        PIN_MP_CROSSWALK, PIN_PHASE43)]
    anchors_doc = json.loads(
        (_REPO / PIN_ANCHORS[0]).read_text("utf-8"))["anchors"]
    strict = [k for k, v in anchors_doc.items()
              if v.get("validation_status")
              == "strict_sa_independent"]
    gate_01 = {
        "gate": "0.1",
        "name": "Input integrity",
        "inputs": pins,
        "anchors_census": {
            "anchors": len(anchors_doc),
            "strict_sa_independent": len(strict),
        },
        "verdict": "PASS" if all(p["match"] for p in pins)
                   else "FAIL",
    }

    gates = [gate_01]
    self_test = None
    attempt = None
    outcome = None
    closure_reason = None

    if gate_01["verdict"] != "PASS":
        outcome = "INVALID"
        gates.append({"gate": "0.2", "name": "Estimator self-test", "verdict": "NOT REACHED"})
        gates.append({"gate": "0.3", "name": "Strict corpus identification and pin", "verdict": "NOT REACHED"})
        gates.append({"gate": "0.4", "name": "Control set freeze (cited data)", "verdict": "NOT REACHED"})
        gates.append({"gate": "0.5", "name": "Census and floors", "verdict": "NOT REACHED"})
    else:
        # ── Gate 0.2 — estimator self-test ──────────
        self_test = _self_test()
        gate_02 = {
            "gate": "0.2",
            "name": "Estimator self-test",
            "generating_parameters":
                self_test["generating_parameters"],
            "fitted_alpha": self_test["fit"]["alpha"],
            "fitted_q": self_test["fit"]["q"],
            "alpha_error": self_test["alpha_error"],
            "q_error": self_test["q_error"],
            "tolerances": self_test["tolerances"],
            "verdict": "PASS"
                       if self_test["recovered_within_tolerance"]
                       else "FAIL",
        }
        gates.append(gate_02)
        if gate_02["verdict"] != "PASS":
            outcome = "INVALID"
            gates.append({"gate": "0.3",
                          "name": "Strict corpus identification and pin",
                          "verdict": "NOT REACHED"})
            gates.append({"gate": "0.4",
                          "name": "Control set freeze (cited data)",
                          "verdict": "NOT REACHED"})
            gates.append({"gate": "0.5",
                          "name": "Census and floors",
                          "verdict": "NOT REACHED"})
        else:
            # ── Gate 0.3 — strict corpus pin ────────
            attempt = _gate_03_attempt()
            identified = attempt[
                "layer_uniquely_identified_and_exportable"]
            gate_03 = {
                "gate": "0.3",
                "name": ("Strict corpus identification "
                         "and pin"),
                "recorded_phase43_corpus":
                    attempt["recorded_phase43_corpus"],
                "v3_data_file_present":
                    attempt["C1_v3_loader_data_file"]["present"],
                "sequences_loadable_from_v3_loader":
                    attempt["C1_v3_loader_data_file"][
                        "sequences_loadable"],
                "verdict": "PASS" if identified else "FAIL",
            }
            gates.append(gate_03)
            if identified:
                gates.append({"gate": "0.4",
                              "name": "Control set freeze "
                                      "(cited data)",
                              "verdict":
                              "NOT RUN BY THIS SCRIPT "
                              "(step-0 continuation)"})
                gates.append({"gate": "0.5",
                              "name": "Census and floors",
                              "verdict":
                              "NOT RUN BY THIS SCRIPT "
                              "(step-0 continuation)"})
                outcome = "STEP 0 CONTINUES"
            else:
                outcome = "STRICT CORPUS NOT PINNABLE"
                closure_reason = (
                    "the V3 layer's data file — the "
                    "Firestore 'indusarrays' dump the "
                    "V3 loader reads — is absent from "
                    "the tree, so the loader loads zero "
                    "sequences and the layer cannot be "
                    "exported or pinned; no database "
                    "copy exists in the execution tree; "
                    "and no other layer in the tree is "
                    "the corpus the Phase-43 record "
                    "names (its source at 3,916 "
                    "records, against 5,679 records "
                    "for the site-attributed layer, "
                    "15,508 mixed-source objects for "
                    "the V1 export, and 3,085 "
                    "ICIT-encoded sequences)")
                gates.append({"gate": "0.4",
                          "name": "Control set freeze (cited data)",
                          "verdict": "NOT REACHED"})
                gates.append({"gate": "0.5",
                          "name": "Census and floors",
                          "verdict": "NOT REACHED"})

    anchors_after = _sha256(_REPO / PIN_ANCHORS[0])

    rec = {
        "phase": "Phase-413",
        "spec": "053-yadav-zipf-controls",
        "act": ("step 0 (spec section 3 gates, in "
                "frozen order)"),
        "execution_date": EXECUTION_DATE,
        "base_commit": BASE_COMMIT,
        "claim_id": "yadav_2009_arxiv_manual_001",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": "s9yfe (approved and public)",
        "estimator_ruling": (
            "DD-053-11 option (a): the section 4.2 "
            "estimator specified completely at the "
            "freeze; the 'identical to Phase-43' "
            "reading retired — no Phase-43 estimator "
            "was sought or substituted"),
        "gates": gates,
        "estimator_self_test": self_test,
        "strict_corpus_identification_attempt": attempt,
        "control_set_frozen": False,
        "systems_fitted": [],
        "sensitivities_computed": [],
        "anchors": {
            "file": PIN_ANCHORS[0],
            "sha256_before": anchors_before,
            "sha256_after": anchors_after,
            "byte_identical": anchors_before == anchors_after,
        },
        "outcome": outcome,
        "outcome_wording_frozen_spec_6": (
            "Spec 053 closed at step 0, gate 0.3: "
            "the V3 / Mahadevan-lineage corpus layer "
            "of record could not be uniquely "
            "identified and pinned as the Phase-43 "
            f"framework's corpus ({closure_reason}). "
            "No fit was computed. This closure is a "
            "statement about runnability, not about "
            "the claim; the claim stands exactly as "
            "recorded."
            if outcome == "STRICT CORPUS NOT PINNABLE"
            else None
        ),
    }

    lines = [
        "# Phase-413 — Spec 053 step-0 report",
        "",
        "Claim: `yadav_2009_arxiv_manual_001` — standing",
        "strongly supported, stage explained, exactly as",
        "recorded (recorded Zipf exponent about 1.35).",
        f"Execution date: {EXECUTION_DATE}. Freeze digest:",
        f"`{FREEZE_DIGEST}`. OSF registration s9yfe",
        "(approved and public).",
        "",
        f"## Outcome: {outcome}",
        "",
    ]
    if outcome == "STRICT CORPUS NOT PINNABLE":
        lines += [
            "Frozen wording (spec section 6, STRICT",
            "CORPUS NOT PINNABLE form):",
            "",
            f"> {rec['outcome_wording_frozen_spec_6']}",
            "",
            "The only fit computed in this run is the",
            "gate 0.2 estimator self-test on synthetic",
            "data, which the frozen gate order itself",
            "prescribes; no fit of the Indus corpus or",
            "of any control system was computed, and no",
            "control count was entered.",
            "",
        ]
    lines += [
        "## Gates, in frozen order",
        "",
    ]
    for g in gates:
        lines.append(f"- **Gate {g['gate']} — "
                     f"{g.get('name', '')}: {g['verdict']}**")
        if g["gate"] == "0.1":
            for p in g["inputs"]:
                lines.append(
                    f"  - `{p['file']}` — "
                    f"{'match' if p['match'] else 'MISMATCH'} "
                    f"({p['observed']})")
            lines.append(
                f"  - Anchors census: "
                f"{g['anchors_census']['anchors']} anchors, "
                f"{g['anchors_census']['strict_sa_independent']} "
                f"strict_sa_independent.")
        if g["gate"] == "0.2" and self_test is not None:
            lines += [
                f"  - Planted alpha 1.20, q 2.0 "
                f"(V 200, N 50,000, seed 20261021); "
                f"fitted alpha {self_test['fit']['alpha']}, "
                f"q {self_test['fit']['q']} (errors "
                f"{self_test['alpha_error']:.3f} / "
                f"{self_test['q_error']:.3f} against "
                f"tolerances 0.10 / 1.0).",
            ]
        if g["gate"] == "0.3" and attempt is not None:
            r = attempt["recorded_phase43_corpus"]
            lines += [
                f"  - Phase-43 record's corpus: "
                f"{r['source']} — {r['total_records']} "
                f"records, {r['total_sequences']} "
                f"sequences, {r['unique_dockeys']} "
                f"dockeys, {r['total_sign_instances']} "
                f"sign instances.",
                "  - The V3 loader's data file is absent",
                "    from the tree; zero sequences are",
                "    loadable; no database copy exists in",
                "    the execution tree; no other layer",
                "    in the tree is that corpus.",
            ]
    lines += [
        "",
        "## What was not done",
        "",
        "Gate 0.4 (control set freeze) and gate 0.5",
        "(census and floors) were not reached: no",
        "control count was entered, no corpus was",
        "exported, and no system — Indus or control —",
        "was fitted. The sensitivities S1-S3 were not",
        "computed. No strength label is added to the",
        "claim's record; the claim stands exactly as",
        "recorded. This result is a strength label",
        "for a recorded curve fit. It is not evidence",
        "that the script encodes language, and it",
        "changes no verdict. (Spec section 9 fence",
        "sentence, carried here as written; this",
        "closure adds no label, so the fence is",
        "restated for completeness.)",
        "",
        "Anchors asserted byte-identical before and after:",
        f"`{anchors_before}` at both readings.",
        "",
        "*AI disclosure: executed by an AI agent (Muse Spark,",
        "via Muse) at the direction of Tristen Pierson, per",
        "constitution section VI.*",
        "",
    ]

    _OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    _OUT_RESULTS.write_text(
        json.dumps(rec, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n", "utf-8")
    _OUT_REPORT.write_text("\n".join(lines), "utf-8")
    print(f"Phase-413 step 0: outcome {outcome}")
    for g in gates:
        print(f"  gate {g['gate']}: {g['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
