#!/usr/bin/env python3
"""Phase 435 — Spec 041 execution: the site x local-label
period mapping Spec 040's closure requires.

Runs the frozen Spec 041 contract (freeze digest
fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7;
OSF contract registration https://osf.io/w2vkn/; execution
ordered by the owner's approval of 2026-10-23 of the
waiting-decisions package, Item 1).

Stages, in frozen order (spec sections 6-9):

  step0  Gates G0.1-G0.6, fail-closed, margins and census
         only. G0.1 layer identity (pin c368f290...; the
         layer is an acquired input, consumed read-only,
         never committed). G0.2 population reproduction
         (the Phase-137 F3 rule: sites at >= 30
         inscriptions AND >= 100 parsed tokens; rows with
         >= 1 parsed token; parse re.findall(r"\\d{3}",
         text)) — the seven sites, 5,410 rows. G0.3 the
         value-level label census (headline period 2,266 /
         phase 2,638 / both 1,788 / union 3,116) and the
         Phase-139 covariates copy asserted against the
         layer on every population row. G0.4 anchors at the
         refreshed pin df0cf620.... G0.5 source
         admissibility classified before extraction.
         G0.6 the no-computation fence: step 0 computes
         margins and census counts only — no repertoire
         quantity, no association statistic, no G1
         quantity of any kind.
  build  Construction (spec section 7) from the committed
         determinations record: one cell per census
         triple, exactly once (section 5.5 completeness
         asserted against the census); contested cells
         retain every admissible determination with
         binding value UNASSIGNED and no sensitivity
         label frozen (DD-041-10); unassigned cells carry
         exactly one enumerated reason (section 5.4);
         then the section 8 placement counts under
         derivations A1 / A2 / B / C (none adopted, none
         preferred) and the artifact + meta written to
         the section 5.6 paths and pinned.
  verify Dual verification support (section 7.4): re-reads
         the artifact against the determinations record
         and the census; asserts every MAPPED / CONTESTED
         cell's determination set, locator and assignment
         read exactly as recorded; lists the cells for
         the independent second-pass read.

The layer file is restricted-local (an acquired input held
on the owner's machines); it is never written to the
repository. Only derived artifacts are written: the census,
the mapping artifact and its meta, and
reports/phase435_results.json.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs" / "041-site-local-label-period-mapping"

LAYER_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef")
LAYER_ROWS = 5679
LAYER_FIELDS = 38
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569")
COVARIATES_SHA256 = (
    "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413")
FREEZE_DIGEST = (
    "fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7")

POPULATION_SITES = {
    "Chanhu-daro": 74,
    "Dholavira": 238,
    "Harappa": 2717,
    "Kalibangan": 212,
    "Lothal": 208,
    "Mohenjo-daro": 1923,
    "Nausharo": 38,
}
POPULATION_ROWS = 5410
# Spec section 2.2 / section 6 recorded headline margins.
MARGIN_PERIOD = 2266
MARGIN_PHASE = 2638
MARGIN_BOTH = 1788
MARGIN_UNION = 3116
MARGIN_NEITHER = 2294

COARSE = ("EARLY", "MATURE", "LATE", "UNASSIGNED")
REASONS = (
    "NO_PUBLISHED_DETERMINATION",
    "DETERMINATION_UNVERIFIED",
    "SPANS_COARSE_BOUNDARY",
    "NOT_IN_PUBLISHED_SCHEME",
    "LABEL_UNCERTAIN_IN_LAYER",
)
VERIFICATION_MODES = ("OWN_TEXT", "PAGINATED_RESTATEMENT")

DEFAULT_LAYER = (Path.home() / "workspace" / "research_notes"
                 / "indus-data-deep-sweep-20261008" / "downloads"
                 / "horus84-computational-linguistics" / "data"
                 / "inscriptions.csv")

AI_DISCLOSURE = (
    "Executed by an AI agent (Muse Spark, via Muse) "
    "at the direction of Tristen Pierson, per constitution "
    "section VI.")

# G0.5 — source admissibility, classified before extraction
# (spec section 3.2 venue-and-locator test; section 3.3
# verification bar). Determination sources are admissible
# only as each use passes the venue test with a locator;
# locator aids may point and never ground a cell.
SOURCE_CLASSIFICATION = [
    {"source": "Marshall, J. (1931), Mohenjo-daro and the "
               "Indus Civilization (ASI excavation report)",
     "class": "DETERMINATION_SOURCE",
     "scope": "Mohenjo-daro local scheme"},
    {"source": "Mackay, E.J.H. (1938), Further Excavations "
               "at Mohenjo-daro (ASI excavation report)",
     "class": "DETERMINATION_SOURCE",
     "scope": "Mohenjo-daro local scheme"},
    {"source": "Vats, M.S. (1940), Excavations at Harappa "
               "(ASI excavation report)",
     "class": "DETERMINATION_SOURCE",
     "scope": "Harappa Vats-era strata (as the report's own "
              "text states)"},
    {"source": "Rao, S.R. (1979), Lothal: A Harappan Port "
               "Town (1955-62) (ASI Memoir 78)",
     "class": "DETERMINATION_SOURCE",
     "scope": "Lothal Period A/B and phases I-V"},
    {"source": "Lal, B.B. & Thapar, B.K., Kalibangan "
               "excavation reports (ASI; Indian Archaeology "
               "- A Review season reports; Ancient India)",
     "class": "DETERMINATION_SOURCE",
     "scope": "Kalibangan Periods I-II"},
    {"source": "Bisht, R.S., Dholavira excavation reports "
               "(ASI; Indian Archaeology - A Review; the "
               "Dholavira monograph literature)",
     "class": "DETERMINATION_SOURCE",
     "scope": "Dholavira stages I-VII"},
    {"source": "Jarrige, J.-F. (1993) and the published "
               "Nausharo excavation reports",
     "class": "DETERMINATION_SOURCE",
     "scope": "Nausharo Periods I-III"},
    {"source": "Meadow & Kenoyer, the HARP periodization "
               "as published (peer-reviewed / published "
               "report venues, with locators)",
     "class": "DETERMINATION_SOURCE",
     "scope": "Harappa Periods 1-5 and phases"},
    {"source": "Published restatements quoting a site "
               "determination with pagination (journal "
               "articles, published monographs and handbook "
               "chapters in named series)",
     "class": "DETERMINATION_SOURCE",
     "scope": "verification mode PAGINATED_RESTATEMENT "
              "only; the restatement is named per cell"},
    {"source": "Phase-139 citation register "
               "(data/evidence_integration/"
               "phase139_citation_register.json)",
     "class": "LOCATOR_AID", "scope": "points; never grounds"},
    {"source": "Phase-139 harmonized covariates and "
               "chron_band",
     "class": "LOCATOR_AID", "scope": "points; never grounds"},
    {"source": "Phase-139 / Phase-140 reports and results",
     "class": "LOCATOR_AID", "scope": "points; never grounds"},
    {"source": "Phase-394 chronology spine",
     "class": "LOCATOR_AID", "scope": "points; never grounds"},
    {"source": "Spec 039 gazetteer artifact and records",
     "class": "LOCATOR_AID", "scope": "points; never grounds"},
    {"source": "Spec 025 / Phase-137 records",
     "class": "LOCATOR_AID", "scope": "points; never grounds"},
    {"source": "harappa.com and other web compilations "
               "without the section 3.2 venue",
     "class": "LOCATOR_AID", "scope": "points; never grounds"},
    {"source": "CISI 3.1 (catalogue volumes)",
     "class": "LOCATOR_AID",
     "scope": "not a period-determination source for "
              "these labels"},
    {"source": "Fuls print corpus / catalog (held)",
     "class": "LOCATOR_AID",
     "scope": "not a stratigraphic authority for these "
              "labels"},
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def informative(value: str) -> bool:
    """A label is informative iff, after the Phase-139
    loader's whitespace strip, it is not a missing
    sentinel ("", "-") — the convention behind the
    recorded margins and the covariates (phase139
    MISSING_SENTINELS). Query and span marks internal
    to a value are never touched."""
    return value is not None and value != "" and value != "-"


def load_population(layer_path: Path):
    """Apply the Phase-137 F3 rule exactly (load_horus +
    analyse_layer): tokens = re.findall(r"\\d{3}", text);
    site eligible at >= 30 inscriptions AND >= 100 parsed
    tokens over all its rows; population = rows at eligible
    sites with >= 1 parsed token."""
    with open(layer_path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames
        raw_rows = list(reader)
    per_site_insc: Counter = Counter()
    per_site_tokens: Counter = Counter()
    parsed_counts = []
    for raw in raw_rows:
        site = (raw["site"] or "").strip()
        n_tokens = len(re.findall(r"\d{3}", raw["text"] or ""))
        per_site_insc[site] += 1
        per_site_tokens[site] += n_tokens
        parsed_counts.append(n_tokens)
    eligible = sorted(
        s for s in per_site_insc
        if per_site_insc[s] >= 30 and per_site_tokens[s] >= 100)
    population = []
    whitespace_findings = []
    for raw, n_tokens in zip(raw_rows, parsed_counts):
        site = (raw["site"] or "").strip()
        if site in eligible and n_tokens >= 1:
            row = {
                "id": (raw["id"] or "").strip(),
                "site": site,
                "period": (raw["period"] or "").strip(),
                "phase": (raw["phase"] or "").strip(),
                "n_parsed_tokens": n_tokens,
            }
            for field in ("period", "phase"):
                if (raw[field] or "") != row[field]:
                    whitespace_findings.append({
                        "id": row["id"], "site": site,
                        "field": field,
                        "layer_raw": raw[field],
                        "stripped": row[field]})
            population.append(row)
    return (raw_rows, fieldnames, eligible, population,
            whitespace_findings)


def census_of(population):
    """The G0.3 value-level census over population rows."""
    cells: dict[tuple, int] = {}
    margins = Counter()
    for row in population:
        p_inf = informative(row["period"])
        f_inf = informative(row["phase"])
        margins["period"] += p_inf
        margins["phase"] += f_inf
        margins["both"] += p_inf and f_inf
        margins["union"] += p_inf or f_inf
        margins["neither"] += (not p_inf) and (not f_inf)
        for field in ("period", "phase"):
            if informative(row[field]):
                key = (row["site"], field, row[field])
                cells[key] = cells.get(key, 0) + 1
    return cells, margins


def full_layer_census(raw_rows):
    """Secondary census: triples attested anywhere in the
    full layer (section 5.5 / deliverable 3)."""
    cells: dict[tuple, int] = {}
    for raw in raw_rows:
        site = (raw["site"] or "").strip()
        for field in ("period", "phase"):
            value = (raw[field] or "").strip()
            if informative(value):
                key = (site, field, value)
                cells[key] = cells.get(key, 0) + 1
    return cells


def run_step0(args) -> dict:
    gates = []

    def gate(gid, name, verdict, detail):
        gates.append({"gate": gid, "name": name,
                      "verdict": verdict, "detail": detail})
        return verdict == "PASS"

    layer = Path(args.layer)
    covariates_path = Path(args.covariates)
    anchors_path = Path(args.anchors)

    # G0.1 — layer identity.
    digest = sha256_of(layer) if layer.exists() else None
    n_rows = n_fields = None
    if layer.exists():
        with open(layer, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            n_fields = len(reader.fieldnames or [])
            n_rows = sum(1 for _ in reader)
    ok = (digest == LAYER_SHA256 and n_rows == LAYER_ROWS
          and n_fields == LAYER_FIELDS)
    gate("G0.1", "Layer identity", "PASS" if ok else "FAIL",
         {"path": str(layer), "sha256": digest,
          "expected_sha256": LAYER_SHA256, "rows": n_rows,
          "fields": n_fields})
    if not ok:
        return _step0_close(gates)

    (raw_rows, _fields, eligible, population,
     whitespace_findings) = load_population(layer)

    # G0.2 — population reproduction.
    per_site = Counter(r["site"] for r in population)
    ok = (eligible == sorted(POPULATION_SITES)
          and dict(per_site) == POPULATION_SITES
          and len(population) == POPULATION_ROWS)
    gate("G0.2", "Population reproduction",
         "PASS" if ok else "FAIL",
         {"eligible_sites": eligible,
          "per_site": dict(sorted(per_site.items())),
          "expected_per_site": POPULATION_SITES,
          "rows": len(population)})
    if not ok:
        return _step0_close(gates)

    # G0.3 — label census + covariates assertion.
    cells, margins = census_of(population)
    headline_ok = (
        margins["period"] == MARGIN_PERIOD
        and margins["phase"] == MARGIN_PHASE
        and margins["both"] == MARGIN_BOTH
        and margins["union"] == MARGIN_UNION
        and margins["neither"] == MARGIN_NEITHER)
    covariates = json.loads(covariates_path.read_text("utf-8"))
    cov_by_id = {(r["id"] or "").strip(): r for r in covariates}
    mismatches = []
    sentinel_only = 0
    for row in population:
        cov = cov_by_id.get(row["id"])
        if cov is None:
            mismatches.append({"id": row["id"],
                               "cause": "no covariate row"})
            continue
        for field, raw_key in (("period", "period_raw"),
                               ("phase", "phase_raw")):
            layer_v = row[field] if row[field] != "" else "-"
            cov_v = cov.get(raw_key)
            cov_v = "-" if cov_v in (None, "") else cov_v
            if layer_v != cov_v:
                if not informative(layer_v) and not informative(cov_v):
                    sentinel_only += 1
                else:
                    mismatches.append(
                        {"id": row["id"], "field": field,
                         "layer": row[field], "covariates": cov_v})
    cov_digest = sha256_of(covariates_path)
    ok = (headline_ok and not mismatches
          and cov_digest == COVARIATES_SHA256
          and len(covariates) == POPULATION_ROWS)
    gate("G0.3", "Label census + covariates assertion",
         "PASS" if ok else "FAIL",
         {"margins": dict(margins),
          "expected_margins": {
              "period": MARGIN_PERIOD, "phase": MARGIN_PHASE,
              "both": MARGIN_BOTH, "union": MARGIN_UNION,
              "neither": MARGIN_NEITHER},
          "census_cells": len(cells),
          "covariates_sha256": cov_digest,
          "covariates_rows": len(covariates),
          "covariate_mismatches": mismatches[:20],
          "covariate_mismatch_count": len(mismatches),
          "sentinel_representation_differences": sentinel_only,
          "value_convention": "period/phase values stripped "
              "of leading/trailing whitespace, the Phase-139 "
              "loader convention (MISSING_SENTINELS after "
              "strip); internal query/span marks untouched",
          "whitespace_findings_population_rows":
              whitespace_findings})
    if not ok:
        return _step0_close(gates)

    # G0.4 — anchors at the refreshed pin (before).
    anchors_digest = sha256_of(anchors_path)
    ok = anchors_digest == ANCHORS_SHA256
    gate("G0.4", "Anchors pin (before)", "PASS" if ok else "FAIL",
         {"path": str(anchors_path), "sha256": anchors_digest,
          "expected_sha256": ANCHORS_SHA256})
    if not ok:
        return _step0_close(gates)

    # G0.5 — source admissibility classified before extraction.
    gate("G0.5", "Source admissibility classified",
         "PASS", {"classification": SOURCE_CLASSIFICATION})

    # G0.6 — no-computation fence.
    gate("G0.6", "No-computation fence", "PASS",
         {"computed_in_step0": [
             "layer margins", "value-level census counts"],
          "not_computed": [
              "any repertoire quantity", "any association "
              "statistic", "any G1 quantity",
              "any inscription-level join"]})

    census_doc = {
        "phase": "Phase-435", "spec": "041", "stage": "step0",
        "layer_sha256": digest,
        "value_convention": "period/phase values stripped of "
            "leading/trailing whitespace (Phase-139 loader "
            "convention); internal query/span marks verbatim",
        "whitespace_findings_population_rows": len(
            whitespace_findings),
        "population_rows": len(population),
        "margins": dict(margins),
        "cells": [
            {"site": s, "field": f, "local_label": v, "rows": n}
            for (s, f, v), n in sorted(cells.items())],
        "ai_disclosure": AI_DISCLOSURE,
    }
    census_path = Path(args.out_census)
    census_path.parent.mkdir(parents=True, exist_ok=True)
    census_path.write_text(
        json.dumps(census_doc, indent=1, sort_keys=False) + "\n",
        encoding="utf-8")

    full = full_layer_census(raw_rows)
    return {
        "stage": "step0", "verdict": "STEP 0 PASSED",
        "gates": gates,
        "census": census_doc,
        "census_sha256": sha256_of(census_path),
        "full_layer_triples": [
            {"site": s, "field": f, "local_label": v, "rows": n,
             "population_cell": (s, f, v) in cells}
            for (s, f, v), n in sorted(full.items())],
        "population_rows_detail": population,
        "anchors_sha256_before": anchors_digest,
    }


def _step0_close(gates) -> dict:
    return {"stage": "step0",
            "verdict": "CLOSED AT STEP 0 — NO ARTIFACT",
            "gates": gates}


# ------------------------------------------------------------------
# Construction (spec section 7) and reporting (spec section 8)
# ------------------------------------------------------------------

def validate_determinations(det_doc, census_cells):
    """Assert the determinations record covers the census
    exactly and obeys the schema discipline of section 5.
    Returns the cell objects in artifact key order."""
    by_key = {}
    for cell in det_doc["cells"]:
        key = (cell["site"], cell["field"], cell["local_label"])
        if key in by_key:
            raise ValueError(f"duplicate cell {key}")
        by_key[key] = cell
    census_keys = set(census_cells)
    if set(by_key) != census_keys:
        missing = sorted(census_keys - set(by_key))
        extra = sorted(set(by_key) - census_keys)
        raise ValueError(
            f"cell set != census set; missing={missing} extra={extra}")
    out = []
    for key in sorted(by_key):
        cell = by_key[key]
        status = cell["status"]
        dets = cell.get("determinations", [])
        if status == "MAPPED":
            assert len(dets) == 1, f"{key}: MAPPED needs 1 det"
            d = dets[0]
            assert d["coarse_assigned"] == cell["coarse_period"]
            assert cell["coarse_period"] in COARSE[:3]
            assert not cell.get("contested")
            assert cell.get("unassigned_reason") is None
        elif status == "CONTESTED":
            assert len(dets) >= 2, f"{key}: CONTESTED needs >=2"
            assigned = {d["coarse_assigned"] for d in dets}
            assert len(assigned) >= 2, f"{key}: not contested"
            assert cell["coarse_period"] == "UNASSIGNED"
            assert cell.get("contested") is True
            assert cell.get("unassigned_reason") is None
        elif status == "UNASSIGNED":
            assert cell["coarse_period"] == "UNASSIGNED"
            assert cell.get("unassigned_reason") in REASONS, key
            assert not cell.get("contested")
        else:
            raise ValueError(f"{key}: bad status {status}")
        for d in dets:
            assert d["citation"] and d["locator"], key
            assert d["mapping_rule"], key
            assert d["verification"] in VERIFICATION_MODES, key
            assert d["coarse_assigned"] in COARSE[:3], key
        assert cell.get("sensitivity_label") is None, (
            f"{key}: DD-041-10 — no sensitivity label is frozen")
        out.append({
            "site": cell["site"], "field": cell["field"],
            "local_label": cell["local_label"],
            "coarse_period": cell["coarse_period"],
            "status": status,
            "determinations": [
                {"citation": d["citation"],
                 "locator": d["locator"],
                 "mapping_rule": d["mapping_rule"],
                 "verification": d["verification"]}
                for d in dets],
            "contested": bool(cell.get("contested")),
            "sensitivity_label": None,
            "unassigned_reason": cell.get("unassigned_reason"),
            "attested_rows": census_cells[key],
        })
    return out


def _row_cells(row, cellmap):
    cells = []
    for field in ("period", "phase"):
        if informative(row[field]):
            cells.append(cellmap[(row["site"], field, row[field])])
    return cells


def derive(row, cellmap, which):
    """Section 8 derivations. Returns (placed_period|None,
    cause|None). Causes use the section 8 taxonomy; A2's
    veto is reported in its own two causes, stated in the
    coverage report."""
    p_inf = informative(row["period"])
    f_inf = informative(row["phase"])
    p_cell = (cellmap[(row["site"], "period", row["period"])]
              if p_inf else None)
    f_cell = (cellmap[(row["site"], "phase", row["phase"])]
              if f_inf else None)
    cells = [c for c in (p_cell, f_cell) if c is not None]
    if not cells:
        return None, "no_informative_label"
    mapped = [c for c in cells if c["status"] == "MAPPED"]
    if which == "B":
        gov = p_cell if p_inf else f_cell
        if gov["status"] == "MAPPED":
            return gov["coarse_period"], None
        if gov["status"] == "CONTESTED":
            return None, "contested_only"
        return None, "all_unassigned"
    if which == "A2":
        if len(mapped) != len(cells):
            if any(c["status"] == "UNASSIGNED" for c in cells):
                return None, "vetoed_by_unassigned_cell"
            return None, "vetoed_by_contested_cell"
        values = {c["coarse_period"] for c in mapped}
        if len(values) == 1:
            return mapped[0]["coarse_period"], None
        return None, "disagreement"
    # A1 and C share mechanics here: at least one MAPPED
    # label and every MAPPED label agrees (A1's literal
    # reading; C's either-field union with disagreement
    # unplaced). A1's contested-only rule is the
    # no-mapped-with-contested branch below.
    if mapped:
        values = {c["coarse_period"] for c in mapped}
        if len(values) == 1:
            return mapped[0]["coarse_period"], None
        return None, "disagreement"
    if any(c["status"] == "CONTESTED" for c in cells):
        return None, "contested_only"
    return None, "all_unassigned"


def derivation_counts(population, cellmap, which):
    placed = Counter()
    placed_by_site = defaultdict(Counter)
    unplaced = Counter()
    unplaced_by_site = defaultdict(Counter)
    for row in population:
        period, cause = derive(row, cellmap, which)
        if period is not None:
            placed[period] += 1
            placed_by_site[row["site"]][period] += 1
        else:
            unplaced[cause] += 1
            unplaced_by_site[row["site"]][cause] += 1
    return {
        "placed_total": sum(placed.values()),
        "placed_by_period": dict(sorted(placed.items())),
        "placed_by_site": {
            s: dict(sorted(c.items()))
            for s, c in sorted(placed_by_site.items())},
        "unplaced_total": sum(unplaced.values()),
        "unplaced_by_cause": dict(sorted(unplaced.items())),
        "unplaced_by_site": {
            s: dict(sorted(c.items()))
            for s, c in sorted(unplaced_by_site.items())},
    }


def run_build(args, step0_result):
    census_cells = {
        (c["site"], c["field"], c["local_label"]): c["rows"]
        for c in step0_result["census"]["cells"]}
    det_doc = json.loads(
        Path(args.determinations).read_text("utf-8"))
    cells = validate_determinations(det_doc, census_cells)
    cellmap = {(c["site"], c["field"], c["local_label"]): c
               for c in cells}
    population = step0_result["population_rows_detail"]

    derivations = {
        w: derivation_counts(population, cellmap, w)
        for w in ("A1", "A2", "B", "C")}

    status_counts = Counter(c["status"] for c in cells)
    by_site_field_status = defaultdict(Counter)
    for c in cells:
        by_site_field_status[(c["site"], c["field"])][c["status"]] += 1

    artifact_path = Path(args.out_artifact)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    with open(artifact_path, "w", encoding="utf-8") as fh:
        for cell in cells:
            fh.write(json.dumps(cell, ensure_ascii=False) + "\n")
    artifact_sha = sha256_of(artifact_path)

    meta = {
        "artifact": "site_period_mapping.jsonl",
        "phase": "Phase-435", "spec": "041",
        "lineage": "ICIT-lineage layer (horus84)",
        "layer_sha256": LAYER_SHA256,
        "covariates_sha256": COVARIATES_SHA256,
        "anchors_sha256": ANCHORS_SHA256,
        "census_sha256": step0_result["census_sha256"],
        "freeze_digest": FREEZE_DIGEST,
        "standard": "Spec 041 section 3 (DD-039-3 carried): "
                    "published determinations only; venue-and-"
                    "locator test; verification OWN_TEXT or "
                    "PAGINATED_RESTATEMENT",
        "key_order": "site, field, local_label (lexicographic)",
        "cells_total": len(cells),
        "cells_by_status": dict(sorted(status_counts.items())),
        "sensitivity_labels_frozen": "none (DD-041-10): the "
            "determination set is the frozen sensitivity basis",
        "ceiling": "At most 3,116 of 5,410 population rows "
                   "(57.6%) carry any recorded label; no "
                   "derivation places more than that share.",
        "ai_disclosure": AI_DISCLOSURE,
    }
    meta_path = Path(args.out_meta)
    meta_path.write_text(
        json.dumps(meta, indent=1) + "\n", encoding="utf-8")

    verification = {"status": "PENDING"}
    if args.verification:
        verification = json.loads(
            Path(args.verification).read_text("utf-8"))

    anchors_after = sha256_of(Path(args.anchors))
    results = {
        "phase": "Phase-435", "spec": "041",
        "outcome": "EXECUTED",
        "lineage": "ICIT-lineage layer (horus84)",
        "g1_quantity_computed": False,
        "step0_verdict": step0_result["verdict"],
        "population_rows": step0_result["census"][
            "population_rows"],
        "gates": step0_result["gates"],
        "census_headline": step0_result["census"]["margins"],
        "census_cells": len(census_cells),
        "census_sha256": step0_result["census_sha256"],
        "artifact": {
            "path": "data/evidence_integration/"
                    "site_period_mapping.jsonl",
            "sha256": artifact_sha,
            "meta_path": "data/evidence_integration/"
                         "site_period_mapping_meta.json",
            "meta_sha256": sha256_of(meta_path),
            "cells_total": len(cells),
            "cells_by_status": dict(sorted(status_counts.items())),
            "cells_by_site_field_status": {
                f"{s}|{f}": dict(sorted(c.items()))
                for (s, f), c in sorted(
                    by_site_field_status.items())},
        },
        "derivations": derivations,
        "ceiling": meta["ceiling"],
        "full_layer_secondary_census": {
            "triples": len(step0_result["full_layer_triples"]),
            "population_cells": sum(
                1 for t in step0_result["full_layer_triples"]
                if t["population_cell"]),
            "non_population_triples": sum(
                1 for t in step0_result["full_layer_triples"]
                if not t["population_cell"]),
        },
        "dual_verification": verification,
        "anchors_sha256_before": step0_result[
            "anchors_sha256_before"],
        "anchors_sha256_after": anchors_after,
        "anchors_unchanged": anchors_after == ANCHORS_SHA256,
        "ai_disclosure": AI_DISCLOSURE,
    }
    results_path = Path(args.out_results)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(
        json.dumps(results, indent=1) + "\n", encoding="utf-8")
    return results


def run_verify(args):
    """Section 7.4 support: structural re-read of the
    artifact against the determinations record and the
    census (the independent locator re-read itself is a
    separate pass; its record is embedded at build)."""
    det_doc = json.loads(
        Path(args.determinations).read_text("utf-8"))
    census = json.loads(Path(args.census).read_text("utf-8"))
    census_cells = {
        (c["site"], c["field"], c["local_label"]): c["rows"]
        for c in census["cells"]}
    cells = validate_determinations(det_doc, census_cells)
    grounded = [c for c in cells
                if c["status"] in ("MAPPED", "CONTESTED")]
    return {
        "cells_total": len(cells),
        "grounded_cells_for_second_pass": len(grounded),
        "grounded": [
            {"site": c["site"], "field": c["field"],
             "local_label": c["local_label"],
             "status": c["status"],
             "determinations": c["determinations"]}
            for c in grounded],
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("stage",
                    choices=("step0", "build", "verify", "run"))
    ap.add_argument("--layer", default=str(DEFAULT_LAYER))
    ap.add_argument("--covariates", default=str(
        REPO / "data/evidence_integration/"
               "phase139_harmonized_covariates.json"))
    ap.add_argument("--anchors", default=str(
        REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"))
    ap.add_argument("--out-census", default=str(
        SPEC_DIR / "step0-census.json"))
    ap.add_argument("--out-step0", default=str(
        REPO / "reports/phase435_step0.json"))
    ap.add_argument("--determinations", default=str(
        SPEC_DIR / "determinations.json"))
    ap.add_argument("--census", default=str(
        SPEC_DIR / "step0-census.json"))
    ap.add_argument("--out-artifact", default=str(
        REPO / "data/evidence_integration/"
               "site_period_mapping.jsonl"))
    ap.add_argument("--out-meta", default=str(
        REPO / "data/evidence_integration/"
               "site_period_mapping_meta.json"))
    ap.add_argument("--out-results", default=str(
        REPO / "reports/phase435_results.json"))
    ap.add_argument("--verification", default=None)
    args = ap.parse_args(argv)

    if args.stage == "verify":
        out = run_verify(args)
        print(json.dumps(out, indent=1))
        return 0

    step0 = run_step0(args)
    step0_public = {k: v for k, v in step0.items()
                    if k != "population_rows_detail"}
    Path(args.out_step0).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_step0).write_text(
        json.dumps(step0_public, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"stage": "step0",
                      "verdict": step0["verdict"],
                      "gates": [(g["gate"], g["verdict"])
                                for g in step0["gates"]]},
                     indent=1))
    if step0["verdict"] != "STEP 0 PASSED":
        return 2
    if args.stage == "step0":
        return 0
    results = run_build(args, step0)
    print(json.dumps({
        "stage": "build", "cells": results["artifact"][
            "cells_total"],
        "by_status": results["artifact"]["cells_by_status"],
        "artifact_sha256": results["artifact"]["sha256"]},
        indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
