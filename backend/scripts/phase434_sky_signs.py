#!/usr/bin/env python3
"""Phase 434 — Spec 071 execution: do the sky signs gather at
the ends of texts (re-scoped form)?

Runs the frozen Spec 071 contract (freeze digest
c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478):
the step-0 gates in order, then — only if every gate passes —
one counting run under Spec 050's criteria carried unchanged.

Gate order (spec section 5, fail-closed, before any
final-position quantity):
  0.1 Asset A asserted against the pin source the freeze
      fixed: Spec 069's asset-a-freeze.json in its merged
      executed record; the canonical CSV recomputes to
      95231935...; per-kind counts match.
  0.2 Shakti intake (P-F1 S1/S2), as in Spec 070's gate 0.2.
  0.3 Input integrity and coverage: every section 3 input
      hashes to its freeze value; every sign occurring in
      the primary population carries exactly one Asset A
      row under the keying route of DD-071-10 (zero or
      multiple resolutions, or a resolved key with no Asset
      A row, is a coverage failure); every sky_cycle row's
      sign_key resolves in the pinned crosswalk. A failure
      stops the run as INVALID — an absent row is never
      treated as non-celestial by default, because that
      default would silently define the comparison class
      (the gate's own words).
  0.4 Population enumeration, keying and class census
      (totals only): the section 2 battery over the primary
      population; Shakti's terminal-strong set enumerated
      in full in Wells space and published (hashed) before
      any test; every enumerated sign keyed (an unkeyable
      sign closes POPULATION NOT KEYED, DD-071-11); the
      celestial census (member signs with labels, each
      member's total, the class total) and the section 4.2
      comparison census published; celestial or comparison
      total occurrences below 30 close TOO THIN.
  0.5 Freeze-order proof: recorded in this record's order
      (Spec 069 froze Asset A; this spec froze quoting its
      digest, following Spec 070's freeze; the population
      was published; no join precedes any of these).

Battery and counting conventions are Spec 070's, shared by
DD-071-3's one battery statement: sequences are the
population rows' sign sequences with the gated ICIT-000
placeholder removed; length >= 2; I/M/T in recorded order;
floor total >= 5; the cascade of section 2. Threshold-only;
no chance-baseline step (G5).

Test (spec section 4, Spec 050's criteria): pooled
final-position rates for the celestial class and the
frequency-matched comparison class (non-celestial,
non-contested signs whose primary-population total lies
within the celestial members' min-max band, inclusive);
enrichment ratio R_sky / R_cmp >= 1.5; Fisher exact
two-sided at 5 percent on the pooled counts; the
half-of-occurrences condition against the corpus-wide
final-position rate. NOT SUPPORTED if the ratio is at or
below 1.0; INCONCLUSIVE otherwise (TOO THIN its thin
form). Sensitivities S1 (borderline removed), S2
(contested under CISI-governed sky labels), S3
(corroborated population, classes re-derived).
Reconciliation failure closes NOT ADJUDICATED.

The corpus and grades files are restricted-local and
never enter the repository; only derived quantities are
written, to reports/phase434_results.json.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DOWNLOADS = Path(
    "/home/hatch/workspace/research_notes/"
    "indus-data-deep-sweep-20261008/downloads"
)
CORPUS_FILE = (
    DOWNLOADS / "shaktiosindia-indus-sign-regimes-deposit"
    / "sanitized_corpus.json"
)
GRADES_FILE = DOWNLOADS / "shakti_row_grades_2026-10-22.csv"

ASSET_DIR = REPO / "specs/069-hunt-asset-a/asset-a"
ASSET_FREEZE = ASSET_DIR / "asset-a-freeze.json"
ASSET_CSV = ASSET_DIR / "depicted-kind-classification.csv"
SPEC069_FREEZE = REPO / "specs/069-hunt-asset-a/freeze.json"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
RESULTS = REPO / "reports/phase434_results.json"

ASSET_SHA256 = "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b"
SPEC069_FREEZE_DIGEST = "657b930c9200299c7d540baa8ed51b7a90176bdea9822577e9cb1f4d292f99aa"
SPEC070_FREEZE_DIGEST = "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e"
SPEC071_FREEZE_DIGEST = "c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478"
CORPUS_SHA256 = "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
GRADES_SHA256 = "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
REGISTRY_SHA256 = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
CROSSWALK_SHA256 = "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
ANCHORS_SHA256 = "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"

GRADE_DOCUMENTED = "documented-lineage"
GRADE_CORROBORATED = "undocumented-corroborated"
GRADE_UNCORROBORATED = "undocumented-uncorroborated"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon_sha(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _hypergeom_pmf(k, n_total, n_drawn, n_success):
    if k < 0 or k > n_success or k > n_drawn or (n_drawn - k) > (n_total - n_success):
        return 0.0
    return (
        math.comb(n_success, k)
        * math.comb(n_total - n_success, n_drawn - k)
        / math.comb(n_total, n_drawn)
    )


def fisher_two_sided(table):
    (a, b), (c, d) = table
    n = a + b + c + d
    row1 = a + b
    col1 = a + c
    lo = max(0, row1 - (n - col1))
    hi = min(row1, col1)
    p_obs = _hypergeom_pmf(a, n, row1, col1)
    return sum(
        p for k in range(lo, hi + 1)
        if (p := _hypergeom_pmf(k, n, row1, col1)) <= p_obs * (1 + 1e-9)
    )


def derive_battery(rows):
    counts: dict[str, list[int]] = {}
    for symbols in rows:
        signs = [s for s in symbols if s != "000"]
        if len(signs) < 2:
            continue
        for pos, sign in enumerate(signs):
            slot = counts.setdefault(sign, [0, 0, 0])
            if pos == 0:
                slot[0] += 1
            elif pos == len(signs) - 1:
                slot[2] += 1
            else:
                slot[1] += 1
    derived = {}
    for sign, (i, m, t) in counts.items():
        total = i + m + t
        entry = {"I": i, "M": m, "T": t, "total": total, "class": None}
        if total >= 5:
            ir, mr, tr = i / total, m / total, t / total
            if tr >= 0.60:
                entry["class"] = "TERMINAL_STRONG"
            elif ir >= 0.55:
                entry["class"] = "INITIAL_STRONG"
            elif mr >= 0.65:
                entry["class"] = "MEDIAL_STRONG"
            elif tr >= 0.40:
                entry["class"] = "TERMINAL_MODERATE"
            elif ir >= 0.40:
                entry["class"] = "INITIAL_MODERATE"
            else:
                entry["class"] = "MIXED"
        derived[sign] = entry
    return derived


def keying_map() -> dict[str, set[str]]:
    wells: dict[str, set[str]] = {}
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["numbering_system"] != "parpola_1982":
                continue
            for token in (row["wells_ids"] or "").split("|"):
                token = token.strip()
                if token:
                    wells.setdefault(token, set()).add(row["sign_id"])
    return wells


def key_sign(code: str, wells: dict[str, set[str]]):
    token = "W" + code.zfill(3)
    hits = wells.get(token, set())
    if len(hits) == 1:
        return next(iter(hits)), None
    if len(hits) == 0:
        return None, f"no parpola_1982 registry row carries Wells id {token}"
    return None, f"Wells id {token} resolves to {len(hits)} distinct sign ids"


def main() -> int:
    gates: list[dict] = []
    results: dict = {
        "phase": 434, "spec": "071",
        "spec_freeze_digest": SPEC071_FREEZE_DIGEST,
        "asset_a_sha256": ASSET_SHA256,
        "execution_order": [
            "Spec 069 froze Asset A (2026-10-22, executed record merged)",
            "Spec 070 froze (freeze digest 763108f8...)",
            "Spec 071 froze quoting Asset A's digest (this spec, c06a7a86...)",
            "gate 0.1 asset assertion (pin source: Spec 069 asset-a-freeze.json)",
            "gate 0.2 intake assertion (P-F1 S1/S2)",
            "gate 0.3 input integrity + coverage",
            "gate 0.4 frame enumerated + published (hash) BEFORE any test; class censuses; TOO THIN floor",
            "gate 0.5 freeze-order proof (this record's order)",
            "counting run (section 4)",
        ],
        "g5_attestation": (
            "The Phase-43 battery applied here is threshold-only: it "
            "contains no chance-baseline step - no permutation, shuffle, "
            "or expected-rate baseline - and none is restored or "
            "claimed. The frequency-matched comparison of section 4 is "
            "this design's own test construction (carried from Spec "
            "050), not a Phase-43 element."
        ),
        "lineage_statement_PF1_S3": (
            "Lineage (P-F1 S3): the positional classes were measured on "
            "the Shakti corpus deposit (Zenodo) as graded by the "
            "programme's intake record - documented-lineage rows are "
            "CISI-verifiable; corroborated rows are supported by an "
            "independent sign list; uncorroborated rows enter no count. "
            "The Phase-43 counts (805/2,267; the 40/61/20 classes) are "
            "never a basis for any quantity here."
        ),
    }

    def close(outcome: str, **extra):
        results["outcome"] = outcome
        results["gates"] = gates
        results.update(extra)
        RESULTS.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
        print(outcome)
        return 0

    anchors_before = sha256(ANCHORS)

    # ── Gate 0.1: Asset A (pin source fixed by the freeze) ──────
    if not ASSET_FREEZE.exists() or not SPEC069_FREEZE.exists():
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "asset-a-freeze.json or Spec 069 freeze.json absent"})
        return close("CLOSED AT STEP 0 - ASSET NOT FROZEN")
    spec069_freeze = json.loads(SPEC069_FREEZE.read_text(encoding="utf-8"))
    asset_freeze = json.loads(ASSET_FREEZE.read_text(encoding="utf-8"))
    if spec069_freeze.get("digest") != SPEC069_FREEZE_DIGEST:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "Spec 069 freeze record digest mismatch"})
        return close("CLOSED AT STEP 0 - ASSET NOT FROZEN")
    observed_asset_sha = sha256(ASSET_CSV)
    if observed_asset_sha != ASSET_SHA256 or asset_freeze.get("sha256") != ASSET_SHA256:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": f"asset digest {observed_asset_sha}"})
        return close("CLOSED AT STEP 0 - ASSET PIN MISMATCH",
                     observed_asset_sha256=observed_asset_sha)
    with ASSET_CSV.open(newline="", encoding="utf-8") as handle:
        asset_rows = list(csv.DictReader(handle))
    kinds: dict[str, str] = {}
    asset_by_key: dict[str, dict] = {}
    per_kind: dict[str, int] = {}
    for row in asset_rows:
        kinds[row["sign_key"]] = row["depicted_kind"]
        asset_by_key[row["sign_key"]] = row
        per_kind[row["depicted_kind"]] = per_kind.get(row["depicted_kind"], 0) + 1
    presented_counts = {
        kind: per_kind.get(kind, 0)
        for kind in ("animal", "sky_cycle", "object_goods", "human",
                     "other", "unidentified")
    }
    presented_counts["contested"] = sum(
        1 for row in asset_rows if row["dispute_status"] == "contested"
    )
    if presented_counts != asset_freeze["per_kind_counts"]:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "per-kind counts differ from the pin source"})
        return close("CLOSED AT STEP 0 - ASSET PIN MISMATCH")
    gates.append({"gate": "0.1", "result": "PASS",
                  "detail": "Asset A frozen (pin source Spec 069's "
                            "asset-a-freeze.json); canonical CSV "
                            "recomputes to 95231935...; counts match"})

    # ── Gate 0.2: Shakti intake, P-F1 S1/S2 ─────────────────────
    if sha256(CORPUS_FILE) != CORPUS_SHA256 or sha256(GRADES_FILE) != GRADES_SHA256:
        gates.append({"gate": "0.2", "result": "FAIL", "detail": "S1 hash mismatch"})
        return close("SHAKTI INTAKE NOT REPRODUCED")
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    with GRADES_FILE.open(newline="", encoding="utf-8") as handle:
        grades_rows = list(csv.DictReader(handle))
    grade_of = {g["shakti_id"]: g["grade"] for g in grades_rows}
    grade_counts = {}
    for g in grade_of.values():
        grade_counts[g] = grade_counts.get(g, 0) + 1
    analyzable = [r for r in corpus if not all(s == "000" for s in r["symbols"])]
    cisi_carrying = sum(1 for r in analyzable if r["cisi"] != "-")
    census_ok = (
        len(corpus) == 5704 and len(analyzable) == 5536
        and grade_counts.get(GRADE_DOCUMENTED) == 3212
        and grade_counts.get(GRADE_CORROBORATED) == 2087
        and grade_counts.get(GRADE_UNCORROBORATED) == 405
        and cisi_carrying == 4904
        and all(r["id"] in grade_of for r in corpus)
    )
    if not census_ok:
        gates.append({"gate": "0.2", "result": "FAIL",
                      "detail": f"S2 census: rows={len(corpus)} analyzable={len(analyzable)} "
                                f"grades={grade_counts} cisi={cisi_carrying}"})
        return close("SHAKTI INTAKE NOT REPRODUCED")
    gates.append({"gate": "0.2", "result": "PASS",
                  "detail": "S1 hashes recompute; S2 census reproduces "
                            "(5,704 rows; 5,536 analyzable; 3,212/2,087/405; "
                            "4,904 CISI-carrying)"})

    # ── Gate 0.3: input integrity + coverage ────────────────────
    if (sha256(REGISTRY) != REGISTRY_SHA256
            or sha256(CROSSWALK) != CROSSWALK_SHA256
            or anchors_before != ANCHORS_SHA256):
        gates.append({"gate": "0.3", "result": "FAIL",
                      "detail": "a section 3 input hash differs from its freeze value"})
        return close("INVALID")
    primary_rows = [r["symbols"] for r in corpus
                    if grade_of[r["id"]] == GRADE_DOCUMENTED]
    results["population_rows"] = {"primary_documented": len(primary_rows)}
    # Totals only at this gate (occurrence counts are census
    # quantities, not positional quantities).
    totals: dict[str, int] = {}
    for symbols in primary_rows:
        for s in symbols:
            if s != "000":
                totals[s] = totals.get(s, 0) + 1
    wells = keying_map()
    occurring = sorted(totals)
    covered: dict[str, str] = {}
    uncovered: list[dict] = []
    for code in occurring:
        sign_key, reason = key_sign(code, wells)
        if sign_key is None:
            uncovered.append({"wells_code": code, "total": totals[code],
                              "reason": reason})
        elif sign_key not in kinds:
            uncovered.append({"wells_code": code, "total": totals[code],
                              "reason": f"keys to {sign_key}, which carries no Asset A row"})
        else:
            covered[code] = sign_key
    # Every sky_cycle row's sign_key resolves in the pinned crosswalk.
    with CROSSWALK.open(newline="", encoding="utf-8") as handle:
        crosswalk_keys = {r["registry_sign_id"] for r in csv.DictReader(handle)}
    sky_keys = [k for k, v in kinds.items() if v == "sky_cycle"]
    sky_unresolved = [k for k in sky_keys if k not in crosswalk_keys]
    results["gate_0_3_coverage"] = {
        "signs_occurring_in_primary_population": len(occurring),
        "signs_carrying_an_asset_row": len(covered),
        "signs_without_an_asset_row": len(uncovered),
        "uncovered_signs": uncovered,
        "sky_cycle_rows_in_asset": len(sky_keys),
        "sky_cycle_keys_unresolved_in_crosswalk": sky_unresolved,
    }
    if uncovered or sky_unresolved:
        gates.append({"gate": "0.3", "result": "FAIL",
                      "detail": f"coverage: {len(uncovered)} of {len(occurring)} signs "
                                "occurring in the primary population carry no Asset A "
                                "row under the keying route; an absent row is never "
                                "treated as non-celestial by default"})
        return close("INVALID")
    gates.append({"gate": "0.3", "result": "PASS",
                  "detail": f"every one of the {len(occurring)} occurring signs "
                            "carries exactly one Asset A row; every sky_cycle "
                            "key resolves in the pinned crosswalk"})

    # ── Gate 0.4: enumeration, keying, censuses, TOO THIN ───────
    derived = derive_battery(primary_rows)
    class_counts: dict[str, int] = {}
    for e in derived.values():
        if e["class"]:
            class_counts[e["class"]] = class_counts.get(e["class"], 0) + 1
    frame_codes = sorted(
        s for s, e in derived.items() if e["class"] == "TERMINAL_STRONG"
    )
    frame_publication = {
        "frame": "terminal-strong set, primary population",
        "enumeration_wells_space": [
            {"wells_code": c, "I": derived[c]["I"], "M": derived[c]["M"],
             "T": derived[c]["T"], "total": derived[c]["total"]}
            for c in frame_codes
        ],
        "battery_class_counts_primary": class_counts,
    }
    frame_sha = canon_sha(frame_publication)
    results["gate_0_4_frame_publication_sha256"] = frame_sha
    results["frame"] = frame_publication
    frame_keyed: dict[str, str] = {}
    frame_unkeyable = []
    for code in frame_codes:
        sign_key, reason = key_sign(code, wells)
        if sign_key is None or sign_key not in kinds:
            frame_unkeyable.append({"wells_code": code,
                                    "reason": reason or "no Asset A row"})
        else:
            frame_keyed[code] = sign_key
    if frame_unkeyable:
        gates.append({"gate": "0.4", "result": "CLOSE",
                      "detail": f"{len(frame_unkeyable)} unkeyable frame sign(s); DD-071-11 closure"})
        return close("POPULATION NOT KEYED", unkeyable_frame_signs=frame_unkeyable,
                     frame_size=len(frame_codes))
    # Celestial census (totals only).
    celestial_keys = set(sky_keys)
    celestial_members = []
    celestial_total = 0
    for code in occurring:
        sign_key = covered[code]
        if sign_key in celestial_keys:
            row = asset_by_key[sign_key]
            celestial_members.append({
                "wells_code": code, "sign_key": sign_key,
                "verbatim_label": row["depicted_label_verbatim"],
                "agreement": row["agreement"],
                "dispute_status": row["dispute_status"],
                "total_in_primary": totals[code],
            })
            celestial_total += totals[code]
    # Comparison census: band from celestial members' totals.
    if celestial_members:
        band_lo = min(m["total_in_primary"] for m in celestial_members)
        band_hi = max(m["total_in_primary"] for m in celestial_members)
    else:
        band_lo = band_hi = None
    comparison_members = []
    comparison_total = 0
    if band_lo is not None:
        for code in occurring:
            sign_key = covered[code]
            row = asset_by_key[sign_key]
            if sign_key in celestial_keys:
                continue
            if row["dispute_status"] == "contested":
                continue
            if band_lo <= totals[code] <= band_hi:
                comparison_members.append(code)
                comparison_total += totals[code]
    results["gate_0_4_censuses"] = {
        "celestial_members": celestial_members,
        "celestial_total_occurrences": celestial_total,
        "comparison_band": [band_lo, band_hi],
        "comparison_members": comparison_members,
        "comparison_total_occurrences": comparison_total,
    }
    if celestial_total < 30 or comparison_total < 30:
        gates.append({"gate": "0.4", "result": "CLOSE",
                      "detail": f"TOO THIN floor: celestial total {celestial_total}, "
                                f"comparison total {comparison_total} (floor 30)"})
        return close("TOO THIN")
    gates.append({"gate": "0.4", "result": "PASS",
                  "detail": f"frame enumerated ({len(frame_codes)} signs), publication "
                            f"sha {frame_sha[:16]}...; censuses published; both class "
                            "totals clear the TOO THIN floor"})
    gates.append({"gate": "0.5", "result": "PASS",
                  "detail": "order recorded in this file: Spec 069 froze Asset A; "
                            "Spec 071 froze quoting its digest after Spec 070's "
                            "freeze; the frame was hashed at gate 0.4 before the "
                            "counting run below"})

    # ── Counting run (section 4) ────────────────────────────────
    # Reached only if every gate passed. Pooled rates over the
    # primary population; per-sign table over frame + celestial.
    def pooled(codes):
        tot = sum(derived[c]["total"] for c in codes if c in derived)
        fin = sum(derived[c]["T"] for c in codes if c in derived)
        return fin, tot
    celestial_codes = [m["wells_code"] for m in celestial_members]
    sky_fin, sky_tot = pooled(celestial_codes)
    cmp_fin, cmp_tot = pooled(comparison_members)
    r_sky = sky_fin / sky_tot if sky_tot else None
    r_cmp = cmp_fin / cmp_tot if cmp_tot else None
    ratio = (r_sky / r_cmp) if (r_sky is not None and r_cmp) else None
    p_two = fisher_two_sided([[sky_fin, sky_tot - sky_fin],
                              [cmp_fin, cmp_tot - cmp_fin]])
    all_fin = sum(e["T"] for e in derived.values())
    all_tot = sum(e["total"] for e in derived.values())
    corpus_rate = all_fin / all_tot if all_tot else None
    above = sum(
        derived[m["wells_code"]]["total"] for m in celestial_members
        if m["wells_code"] in derived and corpus_rate is not None
        and derived[m["wells_code"]]["total"] > 0
        and (derived[m["wells_code"]]["T"] / derived[m["wells_code"]]["total"]) > corpus_rate
    )
    half_ok = (above / sky_tot) >= 0.5 if sky_tot else False
    reconciles = (sky_tot == celestial_total and cmp_tot == comparison_total)
    results["primary"] = {
        "celestial": {"final": sky_fin, "total": sky_tot, "rate": r_sky},
        "comparison": {"final": cmp_fin, "total": cmp_tot, "rate": r_cmp},
        "ratio": ratio, "fisher_two_sided_p": p_two,
        "corpus_wide_final_rate": corpus_rate,
        "half_condition": {"occurrences_from_above_rate_members": above,
                             "share": (above / sky_tot) if sky_tot else None,
                             "passes": half_ok},
        "reconciles_with_censuses": reconciles,
    }
    if not reconciles:
        return close("NOT ADJUDICATED")
    if ratio is not None and ratio <= 1.0:
        outcome = "NOT SUPPORTED"
    elif (ratio is not None and ratio >= 1.5 and p_two < 0.05 and half_ok):
        outcome = "SUPPORTED"
    else:
        outcome = "INCONCLUSIVE"
    results["anchors_sha256_after"] = sha256(ANCHORS)
    results["anchors_byte_identical"] = results["anchors_sha256_after"] == anchors_before
    return close(outcome)


if __name__ == "__main__":
    raise SystemExit(main())
