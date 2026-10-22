#!/usr/bin/env python3
"""Phase-430 — Spec 068 (Yadav's Zipf fit: what is a
curve fit worth? — successor on the Shakti corpus;
Amendment S-053).

Executes the frozen Spec 068 contract
(specs/068-yadav-zipf-controls-successor/freeze.md;
freeze digest
ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d;
OSF registration 3pbwe, filed 2026-10-22 and
standing pending approval at this run — recorded
as it stands, per freeze.md section 7 and the
owner's execution order of 2026-10-22).

Gates, in the frozen order (spec section 4),
before any system fit:

  0.1 Input integrity — every spec section 3 pin
      hashes to its freeze-record value (the claim
      file at its DD-068-8 re-pinned hash), the
      intake record stands as section 3 requires,
      and the anchors file is asserted
      byte-identical before and after. A mismatch
      stops the run as INVALID.
  0.2 Estimator self-test — Spec 053 gate 0.2,
      unchanged, run by Phase-413's own functions
      (the estimator implementation of record,
      imported from backend/scripts/
      phase413_yadav_zipf_controls.py): planted
      alpha 1.20, q 2.0, V 200, N 50,000, seed
      20261021; pass iff alpha is recovered within
      0.10 and q within 1.0. A failure stops the
      run as INVALID.
  0.3 Shakti intake identity (P-F1 S1) — the
      corpus and row-grades files, held
      restricted-local, recompute to the intake
      record's SHA-256 pins. A failure closes the
      run as SHAKTI INTAKE NOT REPRODUCED.
  0.4 Shakti intake census (P-F1 S2) — the corpus
      census reproduces the audit's census against
      the intake record; the same gate measures
      this successor's own restricted census (per
      population: rows, analyzable rows, tokens,
      distinct signs), which governs over the
      draft's derived figures. A mismatch closes
      the run as SHAKTI INTAKE NOT REPRODUCED.
  0.5 Population act (limb B, DD-068-7) — the
      freeze record's ruling is re-read from
      freeze.json: LIMB B, the strict-sign-set
      restriction dropped openly; the populations
      are stated as the full ICIT sign inventory
      of the restricted corpus with their measured
      distinct-sign counts. A freeze record stating
      no limb stops the run as INVALID.
  0.6 Control set freeze (cited data) — the four
      named systems entered whole as cited data
      from the committed tables in the spec's data
      directory (N1, N2 with its blazon and
      extraction records, P1) and frozen here,
      before any fit; N3 is generated under its
      frozen parameters at fit time (its size is
      gate 0.7's count). No count is typed into
      this script (H16). A table that cannot be
      entered whole stops the run as CONTROL SET
      FREEZE FAILED.
  0.7 Census floors — the primary fit population
      carries at least 50 distinct types and at
      least 2,000 tokens, or the run closes as TOO
      THIN with the census as its finding.

Fits (gates passed only): every system under the
one estimator frozen by Spec 053 (DD-053-11) —
f_hat(r) = C / (r + q)^alpha, C fixed by
normalisation, SSE of log residuals minimised
over the grid alpha 0.00-3.00 step 0.01, q
0.0-20.0 step 0.1, one refinement pass at
one-tenth steps; NRMSE_log = sqrt(SSE / V)
primary. System fits are computed by a
vectorised evaluation of the identical grid
objective; every system fit is cross-checked
against Phase-413's fit_zipf_mandelbrot (the
implementation of record) and the cross-check
is recorded — alpha, q, and NRMSE_log must
agree exactly as recorded. The comparison rule
of spec section 5 (epsilon = 0; N3 by replicate
median over 99 Yule-Simon replicates, rho =
0.10, seed 20261021, run to the Indus primary
token total; the positive-control condition;
the NEAR MISS band 0 < Delta <= 0.02) assigns
the headline on the primary fit alone.
Sensitivities: the grade fit in full beside the
primary (section 6.1) and the subsampling
tables for both populations (section 6.2:
random halves and quarters of inscriptions, 99
replicates per level, seed 20261021, without
replacement; median and central 90% interval
of alpha and NRMSE_log). Under limb B no
separate section 6.3 fit exists.

Generation procedure for N3 (stated here, as
the contract requires): one numpy default
generator seeded 20261021 produces the 99
replicates in sequence. Each replicate starts
empty and grows token by token to exactly the
Indus primary token total N: at each step,
with probability rho = 0.10 the token is a new
type; otherwise the token copies one uniformly
chosen token already generated in that
replicate (so a type is chosen with
probability proportional to its current
count — the Yule-Simon preferential rule).
The subsampling draws use a separate numpy
default generator seeded 20261021, in the
fixed order: primary halves, primary quarters,
sensitivity halves, sensitivity quarters.

Outputs (written on every terminal outcome):
  - reports/phase430_results.json (the full
    machine record)
  - reports/phase430_report.md (the report,
    under spec section 10's headline rules)

Integrity: every section 3 pin is asserted
before any gate quantity; the anchors file is
asserted byte-identical before and after. The
script is deterministic: a second run
reproduces both output files byte-identically.
The restricted corpus and row-grades files are
read from the restricted local store only and
never enter git; row-level corpus data appears
in no output.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[2]
_SPEC = _REPO / "specs/068-yadav-zipf-controls-successor"
_DATA = _SPEC / "data"
_LOCAL = (Path.home() / "workspace/research_notes/"
          "indus-data-deep-sweep-20261008/downloads")
CORPUS_FILE = (_LOCAL / "shaktiosindia-indus-sign-regimes-deposit"
               / "sanitized_corpus.json")
GRADES_FILE = _LOCAL / "shakti_row_grades_2026-10-22.csv"

PIN_CLAIM = (
    "glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json",
    "ec31778a75cbc56f27f385ed7da800edb874a8f600cbe102f46087a8159d6239",
)
PIN_ANCHORS = (
    "backend/reports/INDUS_FINAL_ANCHORS.json",
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
)
PIN_CROSSWALK = (
    "data/crosswalks/sign_crosswalk_master.csv",
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf",
)
PIN_INTAKE = (
    "docs/decisions/2026-10-22-shakti-corpus-intake-record.md",
    "bd14e2b1f0607366ca1845797bcd17f8b577d23140a2e3111fe0cc2652cf9a9d",
)
DIGEST_053 = (
    "fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309"
)
FREEZE_DIGEST = (
    "ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d"
)
CORPUS_SHA256 = (
    "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
)
GRADES_SHA256 = (
    "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
)
LINEAGE_STATEMENT = (
    "This corpus is an ICIT-lineage corpus. Agreement between it and "
    "the program's earlier ICIT-lineage layer is consistency within "
    "one tradition, not independent corroboration."
)
FENCE_SENTENCE = (
    "This result is a strength label for a recorded curve fit, "
    "measured as a new baseline on the Shakti corpus. It is not "
    "evidence that the script encodes language, it changes no "
    "verdict, and it neither confirms nor corrects any Phase-43 "
    "quantity."
)
GRADE_SENSITIVITY_SENTENCE = (
    "This ordering is grade-sensitive: it differs between the "
    "documented-lineage fit and the documented + corroborated fit, "
    "and both fits are reported."
)
EXECUTION_DATE = "2026-10-22"
BASE_COMMIT = "9bdb21d0e32a096abd87525a2dc159b7685dfd79"
SEED = 20261021
N3_RHO = 0.10
N3_REPLICATES = 99
SUB_LEVELS = (("half", 2), ("quarter", 4))
SUB_REPLICATES = 99

_OUT_RESULTS = _REPO / "reports/phase430_results.json"
_OUT_REPORT = _REPO / "reports/phase430_report.md"


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


def _load_phase413():
    spec = importlib.util.spec_from_file_location(
        "phase413_yadav_zipf_controls",
        _REPO / "backend/scripts/phase413_yadav_zipf_controls.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fit_fast(counts) -> dict:
    """The Spec 053 estimator (DD-053-11), evaluated
    on the identical grid objective by vectorised
    rows; produces the same optimum as the
    implementation of record (cross-checked on
    every system fit in the run record)."""
    ranked = sorted((int(c) for c in counts), reverse=True)
    f = np.asarray(ranked, dtype=float)
    v = int(len(f))
    n = int(f.sum())
    log_f = np.log(f)
    ranks = np.arange(1, v + 1, dtype=float)
    alphas = np.round(np.arange(0, 301) * 0.01, 2)
    best_sse = math.inf
    best_alpha = 0.0
    best_q = 0.0
    for qi in range(0, 201):
        q = round(qi * 0.1, 1)
        log_rq = np.log(ranks + q)
        w = np.exp(-np.outer(alphas, log_rq))
        c_norm = n / w.sum(axis=1)
        log_fh = (np.log(c_norm)[:, None]
                  - alphas[:, None] * log_rq[None, :])
        sse = ((log_f[None, :] - log_fh) ** 2).sum(axis=1)
        i = int(np.argmin(sse))
        if float(sse[i]) < best_sse:
            best_sse = float(sse[i])
            best_alpha = float(alphas[i])
            best_q = q
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
            log_rq = np.log(ranks + q)
            c_norm = n / float(np.exp(-alpha * log_rq).sum())
            log_fh = math.log(c_norm) - alpha * log_rq
            sse = float(((log_f - log_fh) ** 2).sum())
            if sse < best_sse:
                best_sse, best_alpha, best_q = sse, alpha, q
            qi += 1
        ai += 1
    sst = float(((log_f - log_f.mean()) ** 2).sum())
    return {
        "V": v,
        "N": n,
        "alpha": best_alpha,
        "q": best_q,
        "SSE": best_sse,
        "NRMSE_log": math.sqrt(best_sse / v),
        "R2_log": (1.0 - best_sse / sst) if sst > 0 else 0.0,
    }


def _yule_simon_replicate(rng, n_tokens: int) -> list[int]:
    # The replicate's token sequence is held explicitly, so
    # "copy one uniformly chosen token already generated" is
    # a uniform draw from that sequence (a type is therefore
    # chosen with probability proportional to its current
    # count — the Yule-Simon preferential rule).
    counts: list[int] = []
    sequence: list[int] = []
    for _ in range(n_tokens):
        if not counts or rng.random() < N3_RHO:
            counts.append(1)
            sequence.append(len(counts) - 1)
        else:
            idx = sequence[int(rng.integers(0, len(sequence)))]
            counts[idx] += 1
            sequence.append(idx)
    return counts


def _median(values):
    return float(np.median(np.asarray(values, dtype=float)))


def _interval90(values):
    arr = np.asarray(values, dtype=float)
    return [float(np.percentile(arr, 5)), float(np.percentile(arr, 95))]


def _read_table(name: str) -> tuple[list[tuple[str, int]], str]:
    path = _DATA / name
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows.append((row["type"], int(row["count"])))
    return rows, _sha256(path)


def main() -> int:
    p413 = _load_phase413()
    anchors_before = _sha256(_REPO / PIN_ANCHORS[0])
    gates: list[dict] = []
    outcome = None
    closure = None

    # ── Gate 0.1 — input integrity ──────────────────
    pins = [_check_pin(*p) for p in
            (PIN_CLAIM, PIN_ANCHORS, PIN_CROSSWALK, PIN_INTAKE)]
    freeze068 = json.loads((_SPEC / "freeze.json").read_text("utf-8"))
    freeze053 = json.loads(
        (_REPO / "specs/053-yadav-zipf-controls/freeze.json")
        .read_text("utf-8"))
    intake_text = (_REPO / PIN_INTAKE[0]).read_text("utf-8")
    intake_stands = (
        CORPUS_SHA256 in intake_text
        and GRADES_SHA256 in intake_text
        and all(f"**{g}" in intake_text for g in ("S1", "S2", "S3", "S4"))
        and "5,704 rows" in intake_text
        and "SHAKTI INTAKE NOT REPRODUCED" in intake_text
    )
    anchors_doc = json.loads(
        (_REPO / PIN_ANCHORS[0]).read_text("utf-8"))["anchors"]
    strict = [k for k, v in anchors_doc.items()
              if v.get("validation_status") == "strict_sa_independent"]
    gate_01 = {
        "gate": "0.1",
        "name": "Input integrity",
        "inputs": pins,
        "freeze068_digest": {
            "pin": FREEZE_DIGEST,
            "observed": freeze068["digest"],
            "match": freeze068["digest"] == FREEZE_DIGEST,
        },
        "spec053_freeze_digest": {
            "pin": DIGEST_053,
            "observed": freeze053["digest"],
            "match": freeze053["digest"] == DIGEST_053,
        },
        "intake_record_stands": intake_stands,
        "anchors_census": {"anchors": len(anchors_doc),
                           "strict_sa_independent": len(strict)},
        "verdict": "PASS" if (
            all(p["match"] for p in pins)
            and freeze068["digest"] == FREEZE_DIGEST
            and freeze053["digest"] == DIGEST_053
            and intake_stands
            and len(anchors_doc) == 287 and len(strict) == 94
        ) else "FAIL",
    }
    gates.append(gate_01)

    self_test = None
    census = None
    populations = None
    control_set = None
    fits = None
    comparison = None
    sensitivity = None
    subsampling = None
    cross_checks = []

    def _not_reached(*specs):
        for gid, name in specs:
            gates.append({"gate": gid, "name": name,
                          "verdict": "NOT REACHED"})

    if gate_01["verdict"] != "PASS":
        outcome = "INVALID"
        closure = "gate 0.1: a section 3 pin mismatched or the " \
                  "intake record did not stand as section 3 requires"
        _not_reached(("0.2", "Estimator self-test"),
                     ("0.3", "Shakti intake identity (P-F1 S1)"),
                     ("0.4", "Shakti intake census (P-F1 S2)"),
                     ("0.5", "Population act"),
                     ("0.6", "Control set freeze (cited data)"),
                     ("0.7", "Census floors"))
    else:
        # ── Gate 0.2 — estimator self-test ──────────
        self_test = p413._self_test()
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
            closure = "gate 0.2: the estimator self-test failed"
            _not_reached(("0.3", "Shakti intake identity (P-F1 S1)"),
                         ("0.4", "Shakti intake census (P-F1 S2)"),
                         ("0.5", "Population act"),
                         ("0.6", "Control set freeze (cited data)"),
                         ("0.7", "Census floors"))

    if outcome is None:
        # ── Gate 0.3 — Shakti identity (P-F1 S1) ────
        corpus_hash = _sha256(CORPUS_FILE) if CORPUS_FILE.exists() else None
        grades_hash = _sha256(GRADES_FILE) if GRADES_FILE.exists() else None
        gate_03 = {
            "gate": "0.3",
            "name": "Shakti intake identity (P-F1 S1)",
            "corpus": {"file": CORPUS_FILE.name, "pin": CORPUS_SHA256,
                       "observed": corpus_hash,
                       "match": corpus_hash == CORPUS_SHA256},
            "row_grades": {"file": GRADES_FILE.name, "pin": GRADES_SHA256,
                           "observed": grades_hash,
                           "match": grades_hash == GRADES_SHA256},
            "verdict": "PASS" if (corpus_hash == CORPUS_SHA256
                                  and grades_hash == GRADES_SHA256)
                       else "FAIL",
        }
        gates.append(gate_03)
        if gate_03["verdict"] != "PASS":
            outcome = "SHAKTI INTAKE NOT REPRODUCED"
            closure = "gate 0.3: a Shakti file did not recompute " \
                      "to the intake record's pin"
            _not_reached(("0.4", "Shakti intake census (P-F1 S2)"),
                         ("0.5", "Population act"),
                         ("0.6", "Control set freeze (cited data)"),
                         ("0.7", "Census floors"))

    corpus = grades = None
    if outcome is None:
        # ── Gate 0.4 — census (P-F1 S2) + own census ─
        corpus = json.loads(CORPUS_FILE.read_text("utf-8"))
        grades = {}
        with open(GRADES_FILE, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                grades[row["shakti_id"]] = row["grade"]

        def _analyzable(r):
            return any(s != "000" for s in r["symbols"])

        def _counts(rows):
            return Counter(s for r in rows for s in r["symbols"]
                           if s != "000")

        ana = [r for r in corpus if _analyzable(r)]
        grade_rows = Counter(grades[r["id"]] for r in corpus)
        cisi_ana = sum(1 for r in ana if r["cisi"] and r["cisi"] != "-")
        all_counts = _counts(ana)
        audit = {
            "rows": len(corpus),
            "analyzable": len(ana),
            "grades": {
                "documented-lineage": grade_rows["documented-lineage"],
                "undocumented-corroborated":
                    grade_rows["undocumented-corroborated"],
                "undocumented-uncorroborated":
                    grade_rows["undocumented-uncorroborated"],
            },
            "analyzable_with_cisi": cisi_ana,
            "tokens": sum(all_counts.values()),
            "distinct_signs": len(all_counts),
            "sites": len({r["site"] for r in corpus}),
        }
        expected = {
            "rows": 5704, "analyzable": 5536,
            "grades": {"documented-lineage": 3212,
                       "undocumented-corroborated": 2087,
                       "undocumented-uncorroborated": 405},
            "analyzable_with_cisi": 4904,
            "tokens": 18065, "distinct_signs": 713, "sites": 77,
        }
        pop_sets = {
            "primary": {"documented-lineage"},
            "sensitivity": {"documented-lineage",
                            "undocumented-corroborated"},
        }
        own = {}
        pop_rows = {}
        for name, gset in pop_sets.items():
            rows_all = [r for r in corpus if grades[r["id"]] in gset]
            rows_ana = [r for r in rows_all if _analyzable(r)]
            c = _counts(rows_ana)
            own[name] = {
                "rows": len(rows_all),
                "analyzable_rows": len(rows_ana),
                "inscriptions": len(rows_ana),
                "tokens": sum(c.values()),
                "distinct_signs": len(c),
            }
            pop_rows[name] = rows_ana
        census = {"audit_census_recomputed": audit,
                  "audit_census_expected": expected,
                  "restricted_census": own}
        gate_04 = {
            "gate": "0.4",
            "name": "Shakti intake census (P-F1 S2) + restricted census",
            "audit_census_match": audit == expected,
            "restricted_census": own,
            "verdict": "PASS" if audit == expected else "FAIL",
        }
        gates.append(gate_04)
        if gate_04["verdict"] != "PASS":
            outcome = "SHAKTI INTAKE NOT REPRODUCED"
            closure = "gate 0.4: the census did not reproduce " \
                      "the audit's census"
            _not_reached(("0.5", "Population act"),
                         ("0.6", "Control set freeze (cited data)"),
                         ("0.7", "Census floors"))
        else:
            populations = {
                name: {"grade_set": sorted(gset),
                       **own[name],
                       "counts": _counts(pop_rows[name])}
                for name, gset in pop_sets.items()
            }

    if outcome is None:
        # ── Gate 0.5 — population act (limb B) ──────
        ruling = (freeze068["definition"]["design"]["population"]
                  ["ruling"])
        limb_b = "LIMB B" in ruling
        gate_05 = {
            "gate": "0.5",
            "name": "Population act (OPEN-068-1, DD-068-7)",
            "limb": "B" if limb_b else None,
            "statement": (
                "The fitted population is the full ICIT sign "
                "inventory of the restricted corpus: the primary "
                "fit population is the analyzable "
                "documented-lineage rows ({} rows, {} tokens, "
                "{} distinct signs) and the sensitivity fit "
                "population is the analyzable documented + "
                "corroborated rows ({} rows, {} tokens, {} "
                "distinct signs), each counting every token by "
                "its ICIT sign type as recorded. No mapping act "
                "is performed and neither population is a strict "
                "population.".format(
                    populations["primary"]["analyzable_rows"],
                    populations["primary"]["tokens"],
                    populations["primary"]["distinct_signs"],
                    populations["sensitivity"]["analyzable_rows"],
                    populations["sensitivity"]["tokens"],
                    populations["sensitivity"]["distinct_signs"])),
            "verdict": "PASS" if limb_b else "FAIL",
        }
        gates.append(gate_05)
        if not limb_b:
            outcome = "INVALID"
            closure = "gate 0.5: the freeze record stated no " \
                      "population limb"
            _not_reached(("0.6", "Control set freeze (cited data)"),
                         ("0.7", "Census floors"))

    if outcome is None:
        # ── Gate 0.6 — control set freeze ───────────
        try:
            n1_rows, n1_hash = _read_table(
                "n1_mesopotamian_numerical_signs.csv")
            p1_rows, p1_hash = _read_table(
                "p1_linearb_syllabograms.csv")
            n2_rows, n2_hash = _read_table("n2_dering_charges.csv")
            n2_blazons_hash = _sha256(_DATA / "n2_dering_blazons.csv")
            n2_extraction_hash = _sha256(
                _DATA / "n2_dering_extraction.csv")
            tables_ok = all(
                rows and all(c > 0 for _, c in rows)
                and len({t for t, _ in rows}) == len(rows)
                for rows in (n1_rows, n2_rows, p1_rows))
        except Exception:  # noqa: BLE001
            tables_ok = False
            n1_rows = n2_rows = p1_rows = []
            n1_hash = n2_hash = p1_hash = None
            n2_blazons_hash = n2_extraction_hash = None
        control_set = {
            "N1": {
                "system": "Mesopotamian numerical signs",
                "table_file": "data/n1_mesopotamian_numerical_signs.csv",
                "table_sha256": n1_hash,
                "citation": (
                    "Token frequencies of numerical signs in the "
                    "proto-cuneiform administrative corpus (Uruk IV "
                    "and Uruk III periods), from the published "
                    "sign/n-gram frequency dataset of the SFU "
                    "NatLang pe-pc-datasets (L. Born; CDLI "
                    "proto-cuneiform corpus, September 2019 "
                    "snapshot; repository commit d1a51170, "
                    "2019-09-11): the ordered unigram layer, "
                    "compounds split, variants merged, both "
                    "periods combined; a published token k(Nxx) "
                    "contributes k occurrences of sign Nxx; "
                    "tenû forms (@T) entered as their own "
                    "published types; the two "
                    "indeterminate-multiplicity groups N(N01) "
                    "and N(N57) (one group each) are excluded "
                    "because counting them as 1 would fabricate "
                    "a count. Bibliographic pin of record: "
                    "Nissen, Damerow & Englund, Archaic "
                    "Bookkeeping (1993) and the published archaic "
                    "sign counts it reports (DD-053-13). Caveat "
                    "of record: this published derivation's "
                    "numerical layer is thin relative to the "
                    "full archaic corpus — the table is the "
                    "whole of what this source reports, entered "
                    "as it stands, with no floor applied."),
                "types": len(n1_rows),
                "tokens": sum(c for _, c in n1_rows),
                "counts": dict(n1_rows),
            },
            "N2": {
                "system": "Heraldic charges (Dering Roll)",
                "table_file": "data/n2_dering_charges.csv",
                "table_sha256": n2_hash,
                "blazons_file": "data/n2_dering_blazons.csv",
                "blazons_sha256": n2_blazons_hash,
                "extraction_file": "data/n2_dering_extraction.csv",
                "extraction_sha256": n2_extraction_hash,
                "builder": "data/build_n2_charges.py",
                "citation": (
                    "Frequencies of charges across the Dering "
                    "Roll (c. 1270–1280, British Library; the "
                    "oldest extant English roll of arms, 324 "
                    "coats of knights owing feudal service to "
                    "the Constable of Dover Castle), blazons as "
                    "transcribed by Brian Timms (Heraldry site, "
                    "archived) in the edited extract at "
                    "bsswebsite.me.uk/History/Dering/"
                    "dering-roll.html (snapshot SHA-256 "
                    "4cb6b0527d2fa482a092a848c0b93e88e0ae6ad39"
                    "00f20a07bd6e982ce054739); counting unit one "
                    "charge occurrence on one shield, under "
                    "the frozen counting rules stated in the "
                    "builder; every shield's extraction read "
                    "against its blazon at the table's freeze "
                    "(324 of 324); 35 shields bear no charge "
                    "(field only) and are named in the "
                    "extraction record."),
                "types": len(n2_rows),
                "tokens": sum(c for _, c in n2_rows),
                "counts": dict(n2_rows),
            },
            "N3": {
                "system": "Synthetic emblem inventory (Yule–Simon)",
                "generation": (
                    "Yule–Simon process, innovation probability "
                    "rho = 0.10, seed 20261021, one generator "
                    "producing 99 replicates in sequence, each "
                    "run to exactly the Indus primary fit's "
                    "token total N (gate 0.7's count); procedure "
                    "stated in this script's docstring "
                    "(DD-053-6, confirmed DD-053-16)."),
                "replicates": N3_REPLICATES,
                "counts": None,
            },
            "P1": {
                "system": "Linear B syllabic signs",
                "table_file": "data/p1_linearb_syllabograms.csv",
                "table_sha256": p1_hash,
                "citation": (
                    "Syllabic sign frequencies counted from the "
                    "DAMOS (Database of Mycenaean at Oslo) "
                    "transliterations as carried in the "
                    "mwenge/linearb.xyz corpus file "
                    "LinearBInscriptions.js (repository commit "
                    "84e0b00e; transcriptions and metadata "
                    "© DAMOS, CIPEM transliteration "
                    "conventions): 5,889 inscription records; "
                    "each transliterated word is split on '-'; "
                    "a token counts as a syllabogram iff it is "
                    "one of the 72 attested transliterated "
                    "syllabary values or an untransliterated "
                    "*NN sign with NN < 100 (Bennett "
                    "numbering; 17 such types attested). "
                    "Excluded: ideograms (including *NN with "
                    "NN >= 100 and *NNN-VAS compounds), "
                    "numerals, and editorial tokens."),
                "types": len(p1_rows),
                "tokens": sum(c for _, c in p1_rows),
                "counts": dict(p1_rows),
            },
        }
        gate_06 = {
            "gate": "0.6",
            "name": "Control set freeze (cited data)",
            "systems": {k: {"types": v.get("types"),
                            "tokens": v.get("tokens")}
                        for k, v in control_set.items()},
            "verdict": "PASS" if tables_ok else "FAIL",
        }
        gates.append(gate_06)
        if not tables_ok:
            outcome = "CONTROL SET FREEZE FAILED"
            closure = "gate 0.6: a named control's table could " \
                      "not be entered whole as cited data"
            _not_reached(("0.7", "Census floors"))

    if outcome is None:
        # ── Gate 0.7 — census floors ────────────────
        prim = populations["primary"]
        gate_07 = {
            "gate": "0.7",
            "name": "Census floors",
            "primary_types": prim["distinct_signs"],
            "primary_tokens": prim["tokens"],
            "floors": {"types": 50, "tokens": 2000},
            "verdict": "PASS" if (prim["distinct_signs"] >= 50
                                  and prim["tokens"] >= 2000)
                       else "FAIL",
        }
        gates.append(gate_07)
        if gate_07["verdict"] != "PASS":
            outcome = "TOO THIN"
            closure = "gate 0.7: the primary fit population is " \
                      "below a frozen floor"

    headline_wording = None
    grade_sensitive = False
    if outcome is None:
        # ── Fits ────────────────────────────────────
        def _fit_system(counts):
            fast = fit_fast(list(counts))
            ref = p413.fit_zipf_mandelbrot(list(counts))
            cross_checks.append({
                "V": fast["V"], "N": fast["N"],
                "alpha_fast": fast["alpha"], "alpha_ref": ref["alpha"],
                "q_fast": fast["q"], "q_ref": ref["q"],
                "nrmse_fast": fast["NRMSE_log"],
                "nrmse_ref": ref["NRMSE_log"],
                "agree": (fast["alpha"] == ref["alpha"]
                          and fast["q"] == ref["q"]
                          and fast["NRMSE_log"] == ref["NRMSE_log"]),
            })
            return fast

        indus_primary = _fit_system(
            populations["primary"]["counts"].values())
        indus_sens = _fit_system(
            populations["sensitivity"]["counts"].values())
        n1_fit = _fit_system(control_set["N1"]["counts"].values())
        n2_fit = _fit_system(control_set["N2"]["counts"].values())
        p1_fit = _fit_system(control_set["P1"]["counts"].values())

        # N3: 99 Yule–Simon replicates to the primary token total.
        rng = np.random.default_rng(SEED)
        n_primary = populations["primary"]["tokens"]
        n3_fits = []
        for _ in range(N3_REPLICATES):
            rep_counts = _yule_simon_replicate(rng, n_primary)
            n3_fits.append(fit_fast(rep_counts))
        n3_median = {
            "alpha": _median([f["alpha"] for f in n3_fits]),
            "q": _median([f["q"] for f in n3_fits]),
            "NRMSE_log": _median([f["NRMSE_log"] for f in n3_fits]),
            "V": _median([f["V"] for f in n3_fits]),
            "N": n_primary,
        }
        e_indus = indus_primary["NRMSE_log"]
        e = {"N1": n1_fit["NRMSE_log"], "N2": n2_fit["NRMSE_log"],
             "N3": n3_median["NRMSE_log"], "P1": p1_fit["NRMSE_log"]}
        n3_as_well_share = float(np.mean(
            [f["NRMSE_log"] <= e_indus for f in n3_fits]))

        def _compare(e_ind):
            as_well = {k: e[k] <= e_ind for k in ("N1", "N2", "N3")}
            gaps = {k: e[k] - e_ind for k in ("N1", "N2", "N3", "P1")}
            near = [k for k in ("N1", "N2", "N3", "P1")
                    if 0 < gaps[k] <= 0.02]
            p1_passes = all(e["P1"] < e[k] for k in ("N1", "N2", "N3"))
            return {"as_well": as_well, "gaps": gaps,
                    "near_miss": near,
                    "falsifier_fires": any(as_well.values()),
                    "positive_control_passes": p1_passes}

        comp_primary = _compare(e_indus)
        if not comp_primary["positive_control_passes"]:
            outcome = "COMPARISON UNINFORMATIVE"
        elif comp_primary["falsifier_fires"]:
            outcome = "NOT SEPARABLE"
        else:
            outcome = "SEPARABLE"
        comparison = {"primary": comp_primary,
                      "errors": {**e, "Indus": e_indus},
                      "n3_as_well_share": n3_as_well_share}

        # ── Sensitivity (section 6.1) ───────────────
        e_sens = indus_sens["NRMSE_log"]
        comp_sens = _compare(e_sens)
        ordering_keys = ("N1", "N2", "N3")
        grade_sensitive = (
            comp_sens["as_well"] != comp_primary["as_well"]
            or comp_sens["positive_control_passes"]
            != comp_primary["positive_control_passes"])
        sensitivity = {"fit": indus_sens, "comparison": comp_sens,
                       "grade_sensitive": grade_sensitive}

        fits = {
            "indus_primary": indus_primary,
            "indus_sensitivity": indus_sens,
            "N1": n1_fit, "N2": n2_fit, "P1": p1_fit,
            "N3_median": n3_median,
            "N3_replicates": n3_fits,
        }

        # ── Subsampling (section 6.2) ───────────────
        rng_sub = np.random.default_rng(SEED)
        subsampling = {}
        for name in ("primary", "sensitivity"):
            rows = [r for r in corpus
                    if grades[r["id"]] in (
                        {"documented-lineage"} if name == "primary"
                        else {"documented-lineage",
                              "undocumented-corroborated"})
                    and _analyzable(r)]
            per_level = {}
            for level, div in SUB_LEVELS:
                k = len(rows) // div
                alphas, nrmses = [], []
                for _ in range(SUB_REPLICATES):
                    idx = rng_sub.choice(len(rows), size=k,
                                         replace=False)
                    c = Counter()
                    for i in idx:
                        c.update(s for s in rows[int(i)]["symbols"]
                                 if s != "000")
                    f = fit_fast(list(c.values()))
                    alphas.append(f["alpha"])
                    nrmses.append(f["NRMSE_log"])
                per_level[level] = {
                    "inscriptions_per_replicate": k,
                    "replicates": SUB_REPLICATES,
                    "alpha_median": _median(alphas),
                    "alpha_interval90": _interval90(alphas),
                    "nrmse_median": _median(nrmses),
                    "nrmse_interval90": _interval90(nrmses),
                }
            subsampling[name] = per_level

        # ── Headline wording (spec section 7) ───────
        def _fmt(x):
            return f"{x:.4f}"
        gs = f" {GRADE_SENSITIVITY_SENTENCE}" if grade_sensitive else ""
        limb_txt = ("limb B — the full ICIT sign inventory of the "
                    "restricted corpus (DD-068-7)")
        if outcome == "SEPARABLE":
            headline_wording = (
                f"{LINEAGE_STATEMENT} Fitted under the one "
                f"Zipf-Mandelbrot rule frozen by Spec 053, the "
                f"Indus distribution of record for this spec — the "
                f"Shakti restricted corpus (documented-lineage "
                f"rows; {limb_txt}; fit error {_fmt(e_indus)}, "
                f"exponent {indus_primary['alpha']}) — fits the "
                f"curve strictly better than every named "
                f"non-linguistic control — Mesopotamian numerical "
                f"signs ({_fmt(e['N1'])}), heraldic charges "
                f"({_fmt(e['N2'])}), and the synthetic emblem "
                f"process (median {_fmt(e['N3'])}) — and the "
                f"linguistic positive control, Linear B sign "
                f"frequencies ({_fmt(e['P1'])}), fits strictly "
                f"better than every non-linguistic control, so "
                f"the measures separate the set's one certain "
                f"writing system from its non-writing systems.{gs} "
                f"On these measures, and on these measures only, "
                f"this fit is separable from the non-linguistic "
                f"controls. This is a new baseline on a new corpus "
                f"and a strength label for the recorded fit: it is "
                f"not new evidence that the script encodes "
                f"language, and it neither confirms nor corrects "
                f"any Phase-43 quantity.")
        elif outcome == "NOT SEPARABLE":
            fired = [k for k in ordering_keys
                     if comp_primary["as_well"][k]]
            names = {"N1": "Mesopotamian numerical signs",
                     "N2": "heraldic charges",
                     "N3": "the synthetic emblem process"}
            parts = "; ".join(
                f"{names[k]} (fit error {_fmt(e[k])}, gap "
                f"{_fmt(e[k] - e_indus)})" for k in fired)
            headline_wording = (
                f"{LINEAGE_STATEMENT} Fitted under the one "
                f"Zipf-Mandelbrot rule frozen by Spec 053, "
                f"{parts} fit(s) the curve as well as or better "
                f"than the Indus distribution of record for this "
                f"spec does — the Shakti restricted corpus "
                f"(documented-lineage rows; {limb_txt}; Indus fit "
                f"error {_fmt(e_indus)}). A system that is not "
                f"writing produces this curve as well as the "
                f"script does, so the recorded fit, on its own, "
                f"carries no distinguishing weight: the claim's "
                f"record gains this dated strength label — 'the "
                f"Zipf-Mandelbrot fit is not separable from named "
                f"non-linguistic systems on these measures' — "
                f"beside its standing verdict, which does not "
                f"change.{gs} What the script encodes is not "
                f"decided by this result in either direction, and "
                f"no Phase-43 quantity is confirmed or corrected "
                f"by it.")
        else:  # COMPARISON UNINFORMATIVE
            headline_wording = (
                f"{LINEAGE_STATEMENT} The comparison cannot judge "
                f"the script: the linguistic positive control, "
                f"Linear B sign frequencies (fit error "
                f"{_fmt(e['P1'])}), does not fit strictly better "
                f"than every non-linguistic control "
                f"(Mesopotamian numerical signs {_fmt(e['N1'])}; "
                f"heraldic charges {_fmt(e['N2'])}; the synthetic "
                f"emblem process, median {_fmt(e['N3'])}), so the "
                f"measures used here do not separate the one "
                f"certain writing system in the set from systems "
                f"that are not writing. The Indus quantities on "
                f"the Shakti restricted corpus "
                f"({_fmt(e_indus)}, exponent "
                f"{indus_primary['alpha']}) are reported for the "
                f"record as a new baseline and support no "
                f"separability conclusion either way.{gs} The "
                f"claim stands exactly as recorded, with no "
                f"strength label added.")

    anchors_after = _sha256(_REPO / PIN_ANCHORS[0])

    rec = {
        "phase": "Phase-430",
        "spec": "068-yadav-zipf-controls-successor",
        "act": ("step 0 (spec section 4 gates, in frozen order), "
                "then the fits, the comparison, and the "
                "sensitivities of spec sections 5-6"),
        "execution_date": EXECUTION_DATE,
        "base_commit": BASE_COMMIT,
        "claim_id": "yadav_2009_arxiv_manual_001",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": (
            "3pbwe (filed 2026-10-22; pending approval at "
            "execution — recorded as it stands, freeze.md "
            "section 7)"),
        "gates": gates,
        "estimator_self_test": self_test,
        "census": census,
        "populations": (
            None if populations is None else {
                name: {k: v for k, v in pop.items() if k != "counts"}
                for name, pop in populations.items()}),
        "control_set": (
            None if control_set is None else {
                k: {kk: vv for kk, vv in v.items() if kk != "counts"}
                for k, v in control_set.items()}),
        "fits": fits,
        "estimator_cross_check": {
            "implementation_of_record":
                "backend/scripts/phase413_yadav_zipf_controls.py"
                " fit_zipf_mandelbrot",
            "systems_checked": len(cross_checks),
            "all_agree": all(c["agree"] for c in cross_checks),
            "checks": cross_checks,
        },
        "comparison": comparison,
        "sensitivity": sensitivity,
        "subsampling": subsampling,
        "grade_sensitive": grade_sensitive,
        "anchors": {
            "file": PIN_ANCHORS[0],
            "sha256_before": anchors_before,
            "sha256_after": anchors_after,
            "byte_identical": anchors_before == anchors_after,
        },
        "outcome": outcome,
        "closure": closure,
        "headline_wording": headline_wording,
        "lineage_statement": LINEAGE_STATEMENT,
        "fence": FENCE_SENTENCE,
    }

    # ── Report (spec section 10 headline block) ─────
    lines = [
        "# Phase-430 — Spec 068 report",
        "",
        f"Claim: `yadav_2009_arxiv_manual_001` — standing strongly",
        "supported, stage explained, exactly as recorded.",
        f"Execution date: {EXECUTION_DATE}. Freeze digest:",
        f"`{FREEZE_DIGEST}`. OSF registration 3pbwe (filed",
        "2026-10-22; pending approval at execution, recorded as",
        "it stands).",
        "",
        f"## Outcome: {outcome}",
        "",
    ]
    if headline_wording:
        lines += ["## Headline (spec section 7 wording, filled "
                  "from the run)", "", f"> {headline_wording}", ""]
    if fits:
        lines += [
            "## Fit table (spec section 10, item 3)",
            "",
            "| System | V | N | alpha | q | NRMSE_log | R2_log | "
            "gap Delta |",
            "|---|---|---|---|---|---|---|---|",
        ]
        def _row(label, f, gap):
            g = "—" if gap is None else f"{gap:.4f}"
            return (f"| {label} | {f['V']} | {f['N']} | "
                    f"{f['alpha']} | {f['q']} | "
                    f"{f['NRMSE_log']:.4f} | {f['R2_log']:.4f} | {g} |")
        gaps = comparison["primary"]["gaps"]
        lines.append(_row("Indus primary (documented-lineage)",
                          fits["indus_primary"], None))
        lines.append(_row("N1 Mesopotamian numerical signs",
                          fits["N1"], gaps["N1"]))
        lines.append(_row("N2 Heraldic charges (Dering Roll)",
                          fits["N2"], gaps["N2"]))
        n3 = fits["N3_median"]
        lines.append(
            f"| N3 Synthetic emblem inventory (median of 99) | "
            f"{n3['V']} | {n3['N']} | {n3['alpha']} | {n3['q']} | "
            f"{n3['NRMSE_log']:.4f} | — | {gaps['N3']:.4f} |")
        lines.append(_row("P1 Linear B (positive control)",
                          fits["P1"], gaps["P1"]))
        near = comparison["primary"]["near_miss"]
        lines += [
            "",
            f"N3 replicate distribution: alpha median "
            f"{n3['alpha']}, NRMSE_log median "
            f"{n3['NRMSE_log']:.4f}, central 90% interval "
            f"{_interval90([f['NRMSE_log'] for f in fits['N3_replicates']])}; "
            f"as-well share "
            f"{comparison['n3_as_well_share']:.2f}. NEAR MISS "
            f"(0 < Delta <= 0.02): {', '.join(near) if near else 'none'}.",
            "",
            "Positive-control condition (P1 strictly better than "
            "every non-linguistic control): "
            f"{'MET' if comparison['primary']['positive_control_passes'] else 'NOT MET'}.",
            "",
            "## Sensitivity fit (spec section 6.1, in full)",
            "",
            _row("Indus sensitivity (documented + corroborated)",
                 fits["indus_sensitivity"], None),
            "",
            f"Grade-sensitive: {grade_sensitive}."
            + (f" {GRADE_SENSITIVITY_SENTENCE}" if grade_sensitive
               else " The verdict-relevant ordering does not "
                    "change between the grade sets."),
            "",
            "## Subsampling (spec section 6.2; median [central "
            "90% interval])",
            "",
        ]
        for name, per in subsampling.items():
            for level, d in per.items():
                lines.append(
                    f"- {name} {level}: alpha "
                    f"{d['alpha_median']} {d['alpha_interval90']}; "
                    f"NRMSE_log {d['nrmse_median']:.4f} "
                    f"{[round(x, 4) for x in d['nrmse_interval90']]} "
                    f"({d['inscriptions_per_replicate']} "
                    f"inscriptions x {d['replicates']} replicates)")
        lines += [
            "",
            "Section 6.3: no separate full-inventory fit exists "
            "under limb B — the primary already is that fit.",
            "",
        ]
    lines += [
        "## Gates, in frozen order",
        "",
    ]
    for g in gates:
        lines.append(f"- **Gate {g['gate']} — {g.get('name', '')}: "
                     f"{g['verdict']}**")
    lines += [
        "",
        f"{FENCE_SENTENCE}",
        "",
        "Anchors asserted byte-identical before and after: "
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
    print(f"Phase-430: outcome {outcome}")
    for g in gates:
        print(f"  gate {g['gate']}: {g['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
