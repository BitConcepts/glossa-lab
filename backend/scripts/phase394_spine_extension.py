"""Phase-394 (Spec 030) — Q6 chronology-spine extension build.

Freeze: specs/030-q6-chronology-spine-extension/freeze.md
(digest 3a61c63a...; adjudication.md — Asks 1, 3, 4, 5
adopted as proposed; Ask 2 expressly not decided).
Registered before execution: OSF https://osf.io/bge3k/,
DOI 10.17605/OSF.IO/BGE3K (adopted Ask 5 precondition).

The build extends the Stage 0 chronology spine (Phase-391,
data/movement/chronology_rows.jsonl — a Spec 027 record,
never modified here) through the five frozen routes in
stop-point order R5 -> R1 -> R2 -> R4 -> R3 (adopted
Ask 4), with a margins-only interim assessment after each
route. It then runs the re-test (spec section 6): the
stage0-freeze.md section 4 assessment VERBATIM — the
assessment, material mapping, name normalisation, and
window are imported from the Phase-391 build script, not
re-implemented — computed from spine margins and metadata
only. No trait list is built, no first-appearance outcome
is inspected, no timing model is fitted (F030-C05).

Integrity rules (spec section 5) as implemented:
  1. Trace or don't build — every added row carries
     origin source, source locator, lab code, licence
     state, origin group, region, scenario tag; a row
     missing any trace field fails the build loud.
  2. One measurement, one row — identity is the lab
     code (age/material as corroboration). Dedupe runs
     before the re-test and its counts are reported. A
     lab-code collision with a differing age is reported
     as a conflict and NOT merged.
  3. Grading by the frozen rule, on origin records —
     grade changes only from traced origin evidence
     (feature naming text recorded per row). No traced
     row is excluded from the pool to shape a criterion.
  4. Material by the frozen mapping, on the origin
     string — reclassifications are traced corrections
     (both strings kept, origin cited).
  5. CONTESTED never silent — the re-test reports every
     criterion twice: as frozen (all rows) and excluding
     CONTESTED-scenario rows. Ask 2 (whether the
     sensitivity binds a future Q6 freeze) is NOT
     decided here; the as-frozen computation is the
     assessment's verdict basis (adjudication.md).
  6. No calibration computed — conventional ages only.
  7. Coordinate-less dated records (adopted Ask 1) are
     admitted for gazetteer-established sites with the
     row's coordinate state recorded as
     inherited-from-cluster.

Route inputs live in the gitignored local store
corpora/downloads/spec030_phase394/ (never in git):
  r5_xronos_data.csv   R5 fresh XRONOS export
  r1_tracing.json      R1 traced origin evidence
  r2_candidates.json   R2 audited-database candidates
  r4_tworains.json     R4 TwoRains supplement audit
  r3_extraction.json   R3 targeted extraction
Each route file is a research product of its route audit;
a missing file fails the build loud (the route was not
run). Every input is sha256-pinned in the results.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = REPO_ROOT / "corpora" / "downloads" / "spec030_phase394"
DATA_DIR = REPO_ROOT / "data" / "movement"
REPORTS_DIR = REPO_ROOT / "reports"
DEFAULT_RESULTS = REPORTS_DIR / "phase394_results.json"
DEFAULT_REPORT = REPORTS_DIR / "phase394_extension_report.md"

# --- Verbatim Stage 0 machinery (imported, not copied) ---------------------
_spec = importlib.util.spec_from_file_location(
    "phase391_stage0_spine",
    Path(__file__).resolve().parent / "phase391_stage0_spine.py")
_p391 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_p391)

classify_material = _p391.classify_material
normalise_name = _p391.normalise_name
q6_assessment = _p391.q6_assessment
WINDOW_BP = _p391.WINDOW_BP
LAT_MIN, LAT_MAX = _p391.LAT_MIN, _p391.LAT_MAX
LNG_MIN, LNG_MAX = _p391.LNG_MIN, _p391.LNG_MAX

BASELINE_META = DATA_DIR / "stage0_meta.json"
# Stage 0 criteria as recorded in reports/phase391_results.json; the
# imported assessment applied to the untouched baseline must reproduce
# them exactly, or the re-test is not verbatim (fail loud).
BASELINE_CRITERIA = {
    "c1_regions_with_2plus_sites": {"value": 1, "threshold": 3,
                                    "pass": False},
    "c2_window_sites_direct_or_associated": {"value": 5, "threshold": 10,
                                             "pass": False},
    "c3_window_short_lived_share": {"value": 0.0, "threshold": 0.5,
                                    "pass": False},
    "c4_window_median_std_bp": {"value": 70, "threshold": 80,
                                "pass": True},
}

ROUTE_ORDER = ["R5", "R1", "R2", "R4", "R3"]
ROUTE_FILES = {
    "R5": "r5_xronos_data.csv",
    "R1": "r1_tracing.json",
    "R2": "r2_candidates.json",
    "R4": "r4_tworains.json",
    "R3": "r3_extraction.json",
}

NEW_ROW_REQUIRED = ["chronology_row_id", "program_site_id",
                    "site_name_as_published", "region_as_recorded",
                    "lab_code", "dated_material",
                    "context_association_grade", "bp", "std",
                    "source_database", "source_record_id",
                    "licence_state", "origin_group", "extension_route"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fatal(msg: str) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    raise SystemExit(2)


def lab_key(lab_code: object) -> str:
    """Dedupe identity (rule 2): the lab code, normalised."""
    if not lab_code:
        return ""
    return " ".join(str(lab_code).split()).upper()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in
            path.read_text(encoding="utf-8").splitlines() if line.strip()]


def assess(pool: list[dict]) -> dict:
    """The section 6 re-test computation: the frozen assessment
    as frozen (all rows) and excluding CONTESTED rows (rule 5)."""
    as_frozen = q6_assessment(pool)
    uncontested = [r for r in pool if r.get("scenario") != "CONTESTED"]
    sensitivity = q6_assessment(uncontested)
    return {"as_frozen": as_frozen,
            "excluding_contested": sensitivity}


def criteria_only(assessment: dict) -> dict:
    """Margins-only view for interim assessments (spec section 4):
    the four criterion values and the status, nothing else."""
    out = {}
    for label, a in assessment.items():
        out[label] = {
            "status": a["status"],
            "criteria": {k: {"value": v["value"], "pass": v["pass"]}
                         for k, v in a["criteria"].items()},
            "window_rows_direct_or_associated":
                a["window_rows_direct_or_associated"],
        }
    return out


class Pool:
    """The extended spine under construction. Baseline rows are
    deep copies; the committed Stage 0 files are never touched."""

    def __init__(self, baseline_rows: list[dict]):
        import copy
        self.rows: list[dict] = copy.deepcopy(baseline_rows)
        self.by_lab: dict[str, list[dict]] = defaultdict(list)
        for r in self.rows:
            k = lab_key(r.get("lab_code"))
            if k:
                self.by_lab[k].append(r)
        self.stats = {route: {"new_rows": 0, "citations_attached": 0,
                              "corrections": 0, "excluded": 0}
                      for route in ROUTE_ORDER}
        self.dedupe_report: dict = {
            "measurements_merged": 0, "rows_removed": [],
            "age_conflicts_not_merged": [],
            "site_assertion_conflicts": []}

    def touch(self, row: dict, route: str) -> dict:
        ext = row.setdefault("extension", {"citations": [],
                                           "corrections": [],
                                           "routes": []})
        if route not in ext["routes"]:
            ext["routes"].append(route)
        return ext

    def add_citation(self, row: dict, route: str, citation: dict) -> None:
        ext = self.touch(row, route)
        ext["citations"].append(citation)
        self.stats[route]["citations_attached"] += 1

    def apply_correction(self, row: dict, route: str, field: str,
                         new_value, origin_source: str, locator: str,
                         evidence_text: str) -> None:
        old = row.get(field)
        if old == new_value:
            return
        ext = self.touch(row, route)
        ext["corrections"].append({
            "field": field, "from": old, "to": new_value,
            "route": route, "origin_source": origin_source,
            "locator": locator, "evidence_text": evidence_text})
        row[field] = new_value
        if field == "dated_material":
            mclass, old_wood, short_lived = classify_material(
                str(new_value))
            row["material_class"] = mclass
            row["old_wood_risk"] = old_wood
            row["short_lived_sample"] = short_lived
        self.stats[route]["corrections"] += 1

    def add_row(self, row: dict, route: str) -> None:
        for key in NEW_ROW_REQUIRED:
            if row.get(key) in (None, ""):
                fatal(f"new row missing trace field {key}: "
                      f"{row.get('chronology_row_id')}")
        if row["extension_route"] != route:
            fatal(f"row {row['chronology_row_id']} route mismatch")
        mclass, old_wood, short_lived = classify_material(
            str(row["dated_material"]))
        # Frozen mapping on the origin string (rule 4): always
        # recomputed here, never trusted from the payload.
        row["material_class"] = mclass
        row["old_wood_risk"] = old_wood
        row["short_lived_sample"] = short_lived
        row.setdefault("scenario", None)
        row.setdefault("cal_bp", None)
        row.setdefault("cal_std", None)
        row.setdefault("calibration_curve", None)
        self.rows.append(row)
        k = lab_key(row.get("lab_code"))
        if k:
            self.by_lab[k].append(row)
        self.stats[route]["new_rows"] += 1

    def find_by_lab(self, lab_code: object) -> list[dict]:
        return self.by_lab.get(lab_key(lab_code), [])

    def dedupe(self) -> None:
        """Rule 2: one measurement, one row. Runs before the
        re-test; counts reported. Same lab code + differing age
        is a conflict, reported and NOT merged.

        The surviving row is the measurement's richest traced
        copy (a graded copy over an ungraded one, an
        informative material string over a placeholder), so the
        merged row carries the union of the traced evidence —
        e.g. the feature naming that one source record carried
        and its sibling copies dropped. Every other copy
        becomes a trace citation on the survivor; site, age,
        error, and material disagreements between copies are
        recorded, never silently resolved."""
        merged = 0
        removed_ids: list[str] = []
        conflicts: list[dict] = []
        site_conflicts: list[dict] = []
        drop: set[int] = set()

        def richness(r: dict) -> tuple:
            grade_rank = {"direct": 2, "associated": 1,
                          "unassessed": 0}.get(
                              r.get("context_association_grade"), 0)
            has_feature = 1 if (r.get("context_description") or "") \
                .startswith("feature:") else 0
            material_informative = 1 if r.get("material_class") in (
                "long_lived", "short_lived") else 0
            has_citation = 1 if r.get("publication_citation") else 0
            return (grade_rank, has_feature, material_informative,
                    has_citation)

        for key, group in list(self.by_lab.items()):
            if len(group) < 2:
                continue
            ages = {r.get("bp") for r in group}
            if len(ages) > 1:
                conflicts.append({
                    "lab_code": group[0].get("lab_code"),
                    "ages": sorted(a for a in ages if a is not None),
                    "row_ids": [r["chronology_row_id"] for r in group],
                    "disposition": "not merged (age conflict)"})
                continue
            canonical = sorted(
                group,
                key=lambda r: (tuple(-x for x in richness(r)),
                               r["chronology_row_id"]))[0]
            for other in group:
                if other is canonical:
                    continue
                sites = {canonical["program_site_id"],
                         other["program_site_id"]}
                if len(sites) > 1:
                    site_conflicts.append({
                        "lab_code": key,
                        "kept_site": canonical["program_site_id"],
                        "other_site_assertion": other["program_site_id"],
                        "merged_row_id": other["chronology_row_id"]})
                variants = {}
                for field in ("bp", "std", "dated_material",
                              "context_association_grade"):
                    if other.get(field) != canonical.get(field):
                        variants[field] = other.get(field)
                ext = canonical.setdefault(
                    "extension", {"citations": [], "corrections": [],
                                  "routes": []})
                ext["citations"].append({
                    "kind": "dedupe_merged_measurement",
                    "merged_row_id": other["chronology_row_id"],
                    "source_database": other.get("source_database"),
                    "source_record_id": other.get("source_record_id"),
                    "publication_citation":
                        other.get("publication_citation"),
                    "field_variants_vs_survivor": variants})
                if "dedupe" not in ext["routes"]:
                    ext["routes"].append("dedupe")
                drop.add(id(other))
                removed_ids.append(other["chronology_row_id"])
                merged += 1
        if drop:
            self.rows = [r for r in self.rows if id(r) not in drop]
            self.by_lab = defaultdict(list)
            for r in self.rows:
                k = lab_key(r.get("lab_code"))
                if k:
                    self.by_lab[k].append(r)
        # Accumulates across calls (dedupe runs after each route).
        acc = self.dedupe_report
        acc["measurements_merged"] += merged
        acc["rows_removed"] += removed_ids
        seen_conf = {c["lab_code"]
                     for c in acc["age_conflicts_not_merged"]}
        for c in conflicts:
            if c["lab_code"] not in seen_conf:
                acc["age_conflicts_not_merged"].append(c)
        acc["site_assertion_conflicts"] += site_conflicts


# --- R5: XRONOS re-retrieval ------------------------------------------------

def route_r5(pool: Pool, gazetteer_sites: set[str],
             retrieval_stamp: str) -> dict:
    path = INPUT_DIR / ROUTE_FILES["R5"]
    if not path.is_file():
        fatal(f"R5 input missing: {path}")
    baseline_ids = {r["source_record_id"] for r in pool.rows
                    if r.get("source_database") == "XRONOS"}
    baseline_by_id = {r["source_record_id"]: r for r in pool.rows
                      if r.get("source_database") == "XRONOS"}
    detail = {"export_rows_total": 0, "in_box_with_coords": 0,
              "new_records": 0, "field_corrections": 0,
              "coordless_admitted": 0, "coordless_unestablished": 0,
              "out_of_box_excluded": 0, "no_coords_no_site": 0,
              "age_diffs_observed_not_applied": []}
    with open(path, newline="", encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            detail["export_rows_total"] += 1
            try:
                lat = float(rec["lat"])
                lng = float(rec["lng"])
                has_coords = True
            except (TypeError, ValueError):
                has_coords = False
            if has_coords and LAT_MIN <= lat <= LAT_MAX \
                    and LNG_MIN <= lng <= LNG_MAX:
                detail["in_box_with_coords"] += 1
                rid = rec["id"]
                if rid in baseline_ids:
                    base = baseline_by_id[rid]
                    # Age diffs between export versions are observed
                    # and recorded, never applied: the frozen R5
                    # scope admits new records and the flat-field
                    # completions R1 exists for; it does not
                    # authorise re-dating a Stage 0 row.
                    try:
                        new_bp = int(rec["bp"])
                    except (TypeError, ValueError):
                        new_bp = None
                    if new_bp is not None and base.get("bp") is not None \
                            and new_bp != base["bp"] and \
                            len(detail["age_diffs_observed_not_applied"]) < 50:
                        detail["age_diffs_observed_not_applied"].append({
                            "source_record_id": rid,
                            "lab_code": base.get("lab_code"),
                            "stage0_bp": base["bp"],
                            "fresh_bp": new_bp})
                    # Export-version field diffs on existing records:
                    # traced corrections (the export is the source of
                    # both versions; locator = record id).
                    new_feature = (rec.get("feature") or "").strip()
                    base_feature = ""
                    if base.get("context_description"):
                        base_feature = base["context_description"]
                    new_mat = (rec.get("material") or "").strip()
                    if new_mat and new_mat != (base.get("dated_material")
                                               or ""):
                        pool.apply_correction(
                            base, "R5", "dated_material", new_mat,
                            "XRONOS (fresh export)",
                            f"XRONOS record id {rid}",
                            "material string differs between the "
                            "Stage 0 export (2026-10-11) and the "
                            "Phase-394 re-retrieval; the newer "
                            "export string governs (rule 4).")
                        detail["field_corrections"] += 1
                    if new_feature and "feature: " + new_feature \
                            not in (base_feature or ""):
                        if base.get("context_association_grade") \
                                == "unassessed":
                            pool.apply_correction(
                                base, "R5", "context_description",
                                f"feature: {new_feature}",
                                "XRONOS (fresh export)",
                                f"XRONOS record id {rid}",
                                "the fresh export names a feature "
                                "the Stage 0 export's flat fields "
                                "did not carry for this record.")
                            pool.apply_correction(
                                base, "R5", "context_association_grade",
                                "associated",
                                "XRONOS (fresh export)",
                                f"XRONOS record id {rid}",
                                f"feature named by the origin "
                                f"record: {new_feature!r} (rule 3).")
                            detail["field_corrections"] += 1
                    continue
                # Genuinely new in-box record: build exactly as
                # Stage 0 built XRONOS rows.
                built = _p391.build_chronology_xronos([rec])
                row = built[0]
                row["retrieval_version"] = retrieval_stamp
                row["extension_route"] = "R5"
                row["coordinate_state"] = "exact_published"
                detail["new_records"] += 1
                pool.add_row(row, "R5")
            elif has_coords:
                detail["out_of_box_excluded"] += 1
            else:
                site_norm = normalise_name(rec.get("site") or "")
                if site_norm and site_norm in gazetteer_sites:
                    # Adopted Ask 1 / rule 7: coordinate-less record
                    # for a gazetteer-established site.
                    built = _p391.build_chronology_xronos([rec])
                    row = built[0]
                    row["retrieval_version"] = retrieval_stamp
                    row["extension_route"] = "R5"
                    row["coordinate_state"] = "inherited-from-cluster"
                    row["notes"] = (
                        (row.get("notes") or "") +
                        " Coordinate-less in the export; admitted "
                        "under Spec 030 rule 7 for a "
                        "gazetteer-established site cluster, "
                        "coordinate state inherited-from-cluster.")
                    detail["coordless_admitted"] += 1
                    pool.add_row(row, "R5")
                elif site_norm:
                    detail["coordless_unestablished"] += 1
                else:
                    detail["no_coords_no_site"] += 1
    return detail


# --- R1/R2/R4/R3: record-driven routes ---------------------------------------

def apply_record_route(pool: Pool, route: str, payload: dict) -> dict:
    """Applies a route's research record: traced corrections,
    citations for existing measurements, and new rows. Records
    are authored by the route audit; this applier is
    deterministic and fails loud on untraced claims."""
    detail = {"corrections_applied": 0, "new_rows": 0,
              "citations_attached": 0}
    for entry in payload.get("corrections", []):
        targets = []
        if entry.get("chronology_row_id"):
            targets = [r for r in pool.rows
                       if r["chronology_row_id"]
                       == entry["chronology_row_id"]]
        elif entry.get("lab_code"):
            targets = pool.find_by_lab(entry["lab_code"])
        if len(targets) != 1:
            fatal(f"{route} correction targets {len(targets)} rows: "
                  f"{entry.get('chronology_row_id') or entry.get('lab_code')}")
        row = targets[0]
        field = entry["field"]
        if field == "context_association_grade":
            if not entry.get("evidence_text"):
                fatal(f"{route} grade correction without the "
                      f"feature naming text: {entry}")
        pool.apply_correction(row, route, field, entry["to"],
                              entry["origin_source"], entry["locator"],
                              entry["evidence_text"])
        detail["corrections_applied"] += 1
    for entry in payload.get("citations", []):
        targets = pool.find_by_lab(entry["lab_code"])
        if len(targets) != 1:
            fatal(f"{route} citation targets {len(targets)} rows: "
                  f"{entry['lab_code']}")
        pool.add_citation(targets[0], route, entry["citation"])
        detail["citations_attached"] += 1
    for row in payload.get("new_rows", []):
        existing = pool.find_by_lab(row.get("lab_code"))
        if existing:
            # One measurement, one row (rule 2): an already-pooled
            # measurement is a citation, never a second row.
            pool.add_citation(existing[0], route, {
                "kind": "same_measurement_via_route",
                "source_database": row.get("source_database"),
                "source_record_id": row.get("source_record_id"),
                "publication_citation":
                    row.get("publication_citation")})
            detail["citations_attached"] += 1
            continue
        pool.add_row(row, route)
        detail["new_rows"] += 1
    return detail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--retrieval-stamp", type=str,
                        default="full export re-retrieved 2026-10-12")
    args = parser.parse_args()

    baseline_path = DATA_DIR / "chronology_rows.jsonl"
    gazetteer_path = DATA_DIR / "gazetteer_rows.jsonl"
    baseline_rows = load_jsonl(baseline_path)
    gazetteer_rows = load_jsonl(gazetteer_path)
    gazetteer_sites = {r["program_site_id"] for r in gazetteer_rows}

    # Verbatim guarantee: the imported assessment on the untouched
    # baseline reproduces the recorded Stage 0 criteria exactly.
    base_assessment = q6_assessment(baseline_rows)
    if base_assessment["criteria"] != BASELINE_CRITERIA or \
            base_assessment["window_rows_direct_or_associated"] != 31:
        fatal("baseline reproduction mismatch — the imported "
              "assessment does not reproduce the Phase-391 record; "
              "the re-test would not be verbatim")

    input_hashes = {
        "data/movement/chronology_rows.jsonl": sha256_file(baseline_path),
        "data/movement/gazetteer_rows.jsonl": sha256_file(gazetteer_path),
        "backend/scripts/phase394_spine_extension.py":
            sha256_file(Path(__file__).resolve()),
    }
    for route, fname in ROUTE_FILES.items():
        p = INPUT_DIR / fname
        if not p.is_file():
            fatal(f"route input missing ({route} not run?): {p}")
        input_hashes[f"corpora/downloads/spec030_phase394/{fname}"] = \
            sha256_file(p)

    pool = Pool(baseline_rows)
    interim: dict[str, dict] = {}
    route_details: dict[str, dict] = {}
    stopped_early = None

    for route in ROUTE_ORDER:
        if route == "R5":
            route_details[route] = route_r5(pool, gazetteer_sites,
                                            args.retrieval_stamp)
        else:
            payload = json.loads(
                (INPUT_DIR / ROUTE_FILES[route]).read_text(
                    encoding="utf-8"))
            route_details[route] = apply_record_route(pool, route,
                                                      payload)
        pool.dedupe()
        interim[route] = criteria_only(assess(pool))
        # Section 3.5: the build is complete when the joint
        # targets are met on margins; later routes are not run
        # past a passing pool (their unrun status is recorded).
        if interim[route]["as_frozen"]["status"] == \
                "SUPPORTED-FOR-FREEZE-DESIGN":
            stopped_early = route
            break

    final = assess(pool)
    final_full = {
        label: {**a, "criteria": a["criteria"]}
        for label, a in final.items()}

    added = [r for r in pool.rows if r.get("extension_route")]
    results = {
        "phase": 394,
        "spec": "030-q6-chronology-spine-extension",
        "kind": "chronology_spine_extension_and_retest",
        "verdict": None,
        "registration": {
            "osf": "https://osf.io/bge3k/",
            "doi": "10.17605/OSF.IO/BGE3K",
            "freeze_digest":
                "3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3"
                "db00e9",
        },
        "input_hashes": input_hashes,
        "baseline": {
            "rows": len(baseline_rows),
            "q6_timing_support": {
                "status": "NOT-YET-TESTABLE",
                "criteria": BASELINE_CRITERIA,
                "window_rows_direct_or_associated": 31},
        },
        "routes": {
            route: {**route_details.get(route, {}),
                    "build_stats": pool.stats[route],
                    "interim_assessment": interim.get(route),
                    "ran": route in route_details}
            for route in ROUTE_ORDER},
        "stopped_early_at_route": stopped_early,
        "dedupe": pool.dedupe_report,
        "extended_spine": {
            "rows": len(pool.rows),
            "rows_added": len(added),
            "by_route": dict(Counter(r["extension_route"]
                                     for r in added)),
            "added_licence_distribution": dict(Counter(
                r["licence_state"] for r in added)),
            "added_by_region": dict(Counter(
                r["region_as_recorded"] for r in added)),
            "by_context_grade": dict(Counter(
                r["context_association_grade"] for r in pool.rows)),
            "by_material_class": dict(Counter(
                r["material_class"] for r in pool.rows)),
            "contested_rows": sum(1 for r in pool.rows
                                  if r.get("scenario") == "CONTESTED"),
        },
        "q6_retest": {
            "status_as_frozen": final["as_frozen"]["status"],
            "as_frozen": final["as_frozen"],
            "excluding_contested": final["excluding_contested"],
            "note": ("Re-test = stage0-freeze.md section 4 "
                     "assessment verbatim on the extended spine "
                     "(spec 030 section 6), margins/metadata only. "
                     "Both computations reported per integrity "
                     "rule 5; Ask 2 bindingness is not decided "
                     "(adjudication.md). SUPPORTED-FOR-FREEZE-"
                     "DESIGN binds only that a Q6 freeze may be "
                     "designed under Spec 027 section 8.2; it is "
                     "not a Q6 result."),
        },
        "products": {
            "chronology_rows":
                "data/movement/chronology_rows_phase394.jsonl",
            "gazetteer_rows":
                "data/movement/gazetteer_rows_phase394.jsonl",
            "extension_register":
                "data/movement/extension_register_phase394.json",
        },
    }

    # Extended gazetteer: baseline rows plus source-asserted rows
    # for genuinely new chronology sites (section 5.7 exception).
    import copy
    gaz_out = copy.deepcopy(gazetteer_rows)
    known_sites = {r["program_site_id"] for r in gaz_out}
    new_sites = sorted({r["program_site_id"] for r in pool.rows}
                       - known_sites)
    for site in new_sites:
        first = next(r for r in pool.rows
                     if r["program_site_id"] == site)
        gaz_out.append({
            "gazetteer_row_id": f"GAZ-P394-{site.replace(' ', '-')}",
            "program_site_id": site,
            "site_name_as_published": first["site_name_as_published"],
            "site_name_normalised": site,
            "source_gazetteer": first["source_database"],
            "source_citation": first.get("publication_citation"),
            "source_locator": (f"Phase-394 route "
                               f"{first.get('extension_route')}; "
                               f"first chronology row "
                               f"{first['chronology_row_id']}"),
            "period_label_as_published": None,
            "period_scheme": None,
            "program_period_assignment": None,
            "site_size_as_published": None,
            "survey_or_excavation_basis": (
                "site with radiocarbon-dated contexts admitted "
                "by the Phase-394 spine extension"),
            "latitude": first.get("latitude"),
            "longitude": first.get("longitude"),
            "coordinate_state": first.get("coordinate_state",
                                          "unknown"),
            "coordinate_source": None,
            "coordinate_precision": None,
            "licence_state": first["licence_state"],
            "origin_group": first["origin_group"],
            "notes": ("Gazetteer assertion added by Phase-394 "
                      "under Spec 030 section 5.7 (genuinely new "
                      "site under the frozen name normalisation)."),
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    chr_out = DATA_DIR / "chronology_rows_phase394.jsonl"
    with open(chr_out, "w", encoding="utf-8") as f:
        for row in sorted(pool.rows,
                          key=lambda r: r["chronology_row_id"]):
            f.write(json.dumps(row, ensure_ascii=False,
                               sort_keys=True) + "\n")
    gaz_path_out = DATA_DIR / "gazetteer_rows_phase394.jsonl"
    with open(gaz_path_out, "w", encoding="utf-8") as f:
        for row in sorted(gaz_out,
                          key=lambda r: r["gazetteer_row_id"]):
            f.write(json.dumps(row, ensure_ascii=False,
                               sort_keys=True) + "\n")
    register = {
        "phase": 394,
        "spec": "030-q6-chronology-spine-extension",
        "input_hashes": input_hashes,
        "routes": results["routes"],
        "stopped_early_at_route": stopped_early,
        "dedupe": pool.dedupe_report,
        "extended_spine": results["extended_spine"],
        "new_gazetteer_sites": new_sites,
    }
    (DATA_DIR / "extension_register_phase394.json").write_text(
        json.dumps(register, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    args.results.parent.mkdir(parents=True, exist_ok=True)
    args.results.write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")

    # Human report.
    lines = []
    lines.append("# Phase-394 — Spec 030 chronology-spine "
                 "extension + Q6 re-test")
    lines.append("")
    lines.append("Extension of the Phase-391 spine under the "
                 "Spec 030 freeze (OSF https://osf.io/bge3k/). "
                 "The Stage 0 products are inputs, unmodified; "
                 "the re-test is the stage0-freeze.md section 4 "
                 "assessment verbatim, margins only (F030-C05).")
    lines.append("")
    lines.append("## Routes (frozen order R5 -> R1 -> R2 -> R4 "
                 "-> R3)")
    lines.append("")
    for route in ROUTE_ORDER:
        st = pool.stats[route]
        ran = route in route_details
        lines.append(f"- {route}: ran={ran}; new rows "
                     f"{st['new_rows']}; citations attached "
                     f"{st['citations_attached']}; corrections "
                     f"{st['corrections']}.")
        if ran:
            crit = interim[route]["as_frozen"]["criteria"]
            lines.append(
                "  Interim (as frozen): " + "; ".join(
                    f"{k}={v['value']} "
                    f"({'PASS' if v['pass'] else 'FAIL'})"
                    for k, v in crit.items())
                + f" — status {interim[route]['as_frozen']['status']}")
    if stopped_early:
        lines.append(f"- Build complete at {stopped_early}: "
                     "joint targets met on margins (spec section "
                     "3.5); later routes not run.")
    lines.append("")
    lines.append("## Dedupe (rule 2)")
    lines.append("")
    lines.append(f"- Measurements merged: "
                 f"{pool.dedupe_report['measurements_merged']}; "
                 f"rows removed: "
                 f"{len(pool.dedupe_report['rows_removed'])}; "
                 f"age conflicts not merged: "
                 f"{len(pool.dedupe_report['age_conflicts_not_merged'])}; "
                 f"site-assertion conflicts: "
                 f"{len(pool.dedupe_report['site_assertion_conflicts'])}.")
    lines.append("")
    lines.append("## Q6 re-test (extended spine)")
    lines.append("")
    for label in ("as_frozen", "excluding_contested"):
        a = final[label]
        lines.append(f"### {label} — status: {a['status']}")
        for k, v in a["criteria"].items():
            lines.append(f"- {k}: value {v['value']} vs threshold "
                         f"{v['threshold']} — "
                         f"{'PASS' if v['pass'] else 'FAIL'}")
        lines.append(f"- Window direct/associated rows: "
                     f"{a['window_rows_direct_or_associated']}")
        lines.append("")
    lines.append("Ask 2 (whether the CONTESTED sensitivity binds "
                 "a future Q6 freeze) is not decided by this "
                 "build; both computations are reported above "
                 "(integrity rule 5). A SUPPORTED-FOR-FREEZE-"
                 "DESIGN outcome binds only that a Q6 freeze may "
                 "be designed under Spec 027 section 8.2.")
    lines.append("")
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "extended_rows": len(pool.rows),
        "rows_added": len(added),
        "q6_status_as_frozen": final["as_frozen"]["status"],
        "q6_status_excluding_contested":
            final["excluding_contested"]["status"],
        "stopped_early_at_route": stopped_early}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
