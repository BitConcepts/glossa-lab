#!/usr/bin/env python3
"""Phase-439 — Spec 040 (D-25: G1 with time held
fixed — the chronology-controlled rerun of the
Spec 025 / Phase-140 site-repertoire test).

Executes the frozen Spec 040 contract
(specs/040-d25-g1-chronology-controlled/freeze.md;
freeze digest
16aeeb7017f34f079742e56f13bfd88e3955ce75722693eae87fbbbaa9927515;
OSF registration 2rgtb, approved and public at
this run). Spec section 1's dependency gate was
judged satisfied at the freeze by the openly
recorded successor-artifact substitution:
Spec 039 executed and named, its artifact
recorded as NOT satisfying section 1, and
Spec 041's artifact accepted as the successor
dependency artifact at its pin. Derivation A1
governs (freeze section 2; DD-040 rulings:
DD-040-1 adopted, DD-040-5 confirmed —
NOT-YET-TESTABLE is the thinness word,
DD-040-6 retained — all three section 5 arms).

Execution shape (spec section 13; tasks E1–E7),
fail-closed, in order:

  Step 0 / E2 — dependency re-verification and
    input integrity: every freeze section 3 pin
    recomputes (Spec 041 artifact + meta + step-0
    census; Spec 039 artifact; the Phase-139
    covariates; the chronology spine; the
    anchors), the freeze record replays
    (framework026 verify_freeze), the recorded
    Spec 039 / Spec 041 freeze digests stand,
    and the ICIT-lineage layer (horus84
    inscriptions.csv) is asserted at its pin —
    from the held copy where one is present, or
    re-acquired from its pinned source
    (horus84/Computational_Linguistics at
    ac44f08c) and asserted before any use, the
    pattern of Spec 041's gate G0.1. The
    section 4.1 join then runs under A1 and
    must reproduce the freeze section 3
    verification exactly: exactly one assignment
    row for each of the 5,410 population
    inscription IDs, 1,457 placed (EARLY 32,
    MATURE 1,386, LATE 39), 3,953 unplaced
    (2,294 no informative label; 1,658 all
    labels UNASSIGNED; 1 disagreement), the
    covariate label margins (2,266 / 2,638 /
    1,788 / 3,116 / 2,294), the 78 census
    triples equal to the artifact's, and the
    covariates in agreement with the layer on
    every population row under the Phase-139
    value convention (values stripped; a value
    is unrecorded iff the stripped form is ""
    or "-"). Any failure stops the run INVALID
    before margins.
  Step 0 / determinism — the whole step-0 +
    margins record is computed twice from the
    pinned inputs; the two canonical records
    must be identical. Failure: INVALID.
  E3 — the section 5 margins gate, margins
    only: assigned / unassigned counts and
    shares overall, by site, and by coarse
    period; distinct sites with at least one
    assigned inscription in each coarse
    period; the contested-excluded count; and
    permutable inscriptions under the section 6
    primary strata (composition_stratum |
    preservation_class | period_stratum rows in
    strata containing at least 2 distinct
    sites). All three arms must hold:
    (1) each of EARLY, MATURE, LATE retains
    assigned inscriptions from at least 5
    distinct sites; (2) the unassigned share is
    at most 40% of the 5,410-row population;
    (3) permutable inscriptions number at
    least 1,000. Any arm failing closes the
    execution NOT-YET-TESTABLE (DD-040-5): no
    profile table outcome, no permutation, no
    interval is computed, and G1 stands
    unchanged with its rider.
  E4 — the section 7 comparability regression:
    reached only if the margins gate passes.
  E5 / E6 — the section 6 primary and the
    section 8 sensitivities: reached only after
    the regression reproduces exactly.

No outcome of this run moves any anchor, makes
no PRED contact, and edits no frozen record
(spec sections 10–11). The claim under test,
STUDY-SPEC-025/G1, stands exactly as Spec 025
and Phase-385 left it unless a section 6.4
outcome retires or restates it by append; a
NOT-YET-TESTABLE closure carries no
consequence for it.

Usage: phase439_g1_chronology_controlled.py run
(writes reports/phase439_results.json and
reports/phase439_report.md).
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs/040-d25-g1-chronology-controlled"
COVARIATES = (REPO / "data/evidence_integration"
              / "phase139_harmonized_covariates.json")
ARTIFACT = (REPO / "data/evidence_integration"
            / "site_period_mapping.jsonl")
ARTIFACT_META = (REPO / "data/evidence_integration"
                 / "site_period_mapping_meta.json")
SPEC041_CENSUS = (REPO / "specs/041-site-local-label-period-mapping"
                  / "step0-census.json")
SPEC039_ARTIFACT = (REPO / "data/movement"
                    / "gazetteer_rows_assigned.jsonl")
SPEC039_FREEZE = (REPO / "specs/039-gazetteer-period-assignment"
                  / "freeze.json")
SPEC041_FREEZE = (REPO / "specs/041-site-local-label-period-mapping"
                  / "freeze.json")
SPINE = REPO / "data/movement/chronology_rows_phase394.jsonl"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
FREEZE_JSON = SPEC_DIR / "freeze.json"
RESULTS = REPO / "reports/phase439_results.json"
REPORT = REPO / "reports/phase439_report.md"

FREEZE_DIGEST = "16aeeb7017f34f079742e56f13bfd88e3955ce75722693eae87fbbbaa9927515"
SPEC039_DIGEST = "ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742"
SPEC041_DIGEST = "fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7"
LAYER_SHA256 = "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
ARTIFACT_SHA256 = "1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67"
ARTIFACT_META_SHA256 = "bda1017dd88da0b14efaa3ffc5ff280b09818349bda4de1ed20f8c60d42864a9"
SPEC041_CENSUS_SHA256 = "b57fb6b1a0aa1e491ba38bf18978eec58c355f3bf833f58298c7516aabeca6be"
SPEC039_ARTIFACT_SHA256 = "64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4"
COVARIATES_SHA256 = "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413"
SPINE_SHA256 = "9dc2fba5019c34ecc57bb1bda3c341ac142876f8ee5c4f058807458faf7eae93"
ANCHORS_SHA256 = "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"

LAYER_URL = ("https://raw.githubusercontent.com/horus84/"
             "Computational_Linguistics/ac44f08c/data/inscriptions.csv")
LAYER_CANDIDATES = [
    Path.home() / "workspace" / "research_notes"
    / "indus-data-deep-sweep-20261008" / "downloads"
    / "horus84-computational-linguistics" / "data" / "inscriptions.csv",
    Path.home() / "workspace" / "glossa-run"
    / "spec040-phase439-layer" / "inscriptions.csv",
]
POPULATION_BY_SITE = {
    "Chanhu-daro": 74, "Dholavira": 238, "Harappa": 2717,
    "Kalibangan": 212, "Lothal": 208, "Mohenjo-daro": 1923,
    "Nausharo": 38,
}
EXPECTED_MARGINS = {"period": 2266, "phase": 2638, "both": 1788,
                    "union": 3116, "neither": 2294}
EXPECTED_PLACED = {"EARLY": 32, "MATURE": 1386, "LATE": 39}
EXPECTED_UNPLACED = {"no_informative_label": 2294,
                     "all_unassigned": 1658, "disagreement": 1}
EXPECTED_PLACED_BY_SITE = {"Dholavira": 133, "Harappa": 1021,
                           "Kalibangan": 157, "Lothal": 108,
                           "Nausharo": 38}
PERIODS = ("EARLY", "MATURE", "LATE")
AI_DISCLOSURE = ("Executed by an AI agent (Muse Spark, via Muse) "
                 "at the direction of Tristen Pierson, per "
                 "constitution section VI.")


class InvalidStop(Exception):
    """A frozen stop condition: the run closes INVALID."""


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _informative(value: str) -> bool:
    return value is not None and value.strip() not in ("", "-")


def _unrecorded(value: str) -> bool:
    return value is None or value.strip() in ("", "-")


def _acquire_layer() -> tuple[bytes, str]:
    """The layer, asserted at its pin before any use.

    Held copies first (Spec 041's venue path, then
    this run's venue cache); if none is present, the
    file is re-acquired from its pinned source and
    asserted — the pattern of Spec 041's gate G0.1.
    The pin, not the path, governs.
    """
    for cand in LAYER_CANDIDATES:
        if cand.exists():
            data = cand.read_bytes()
            if _sha_bytes(data) == LAYER_SHA256:
                return data, f"held copy at {cand}"
    cache = LAYER_CANDIDATES[-1]
    req = urllib.request.Request(
        LAYER_URL, headers={"User-Agent": "glossa-lab phase439"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = resp.read()
    if _sha_bytes(data) != LAYER_SHA256:
        raise InvalidStop(
            "re-acquired layer does not hash to the frozen pin")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(data)
    return data, (f"re-acquired from pinned source "
                  f"(horus84/Computational_Linguistics at ac44f08c) "
                  f"to {cache}")


def _gate_pins() -> dict:
    checks = {}

    def pin(name: str, path: Path, expected: str) -> None:
        got = _sha(path)
        checks[name] = {"file": str(path.relative_to(REPO)),
                        "expected": expected, "observed": got,
                        "match": got == expected}
        if got != expected:
            raise InvalidStop(f"pin mismatch: {name}")

    pin("spec041_artifact", ARTIFACT, ARTIFACT_SHA256)
    pin("spec041_artifact_meta", ARTIFACT_META, ARTIFACT_META_SHA256)
    pin("spec041_step0_census", SPEC041_CENSUS, SPEC041_CENSUS_SHA256)
    pin("spec039_artifact", SPEC039_ARTIFACT, SPEC039_ARTIFACT_SHA256)
    pin("covariates", COVARIATES, COVARIATES_SHA256)
    pin("spine", SPINE, SPINE_SHA256)
    pin("anchors", ANCHORS, ANCHORS_SHA256)
    rec039 = json.loads(SPEC039_FREEZE.read_text("utf-8"))
    rec041 = json.loads(SPEC041_FREEZE.read_text("utf-8"))
    checks["spec039_freeze_digest"] = {
        "expected": SPEC039_DIGEST, "observed": rec039["digest"],
        "match": rec039["digest"] == SPEC039_DIGEST}
    checks["spec041_freeze_digest"] = {
        "expected": SPEC041_DIGEST, "observed": rec041["digest"],
        "match": rec041["digest"] == SPEC041_DIGEST}
    for key in ("spec039_freeze_digest", "spec041_freeze_digest"):
        if not checks[key]["match"]:
            raise InvalidStop(f"recorded digest mismatch: {key}")
    sys.path.insert(0, str(REPO / "backend"))
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text("utf-8"))
    problems = verify_freeze(record, REPO)
    checks["spec040_freeze_replay"] = {
        "digest": record["digest"], "problems": problems,
        "match": record["digest"] == FREEZE_DIGEST and not problems}
    if not checks["spec040_freeze_replay"]["match"]:
        raise InvalidStop("Spec 040 freeze record does not replay")
    layer_data, layer_source = _acquire_layer()
    checks["layer"] = {"file": "horus84 inscriptions.csv",
                       "expected": LAYER_SHA256,
                       "observed": _sha_bytes(layer_data),
                       "match": True, "source": layer_source,
                       "bytes": len(layer_data)}
    return {"checks": checks, "layer_data": layer_data,
            "layer_source": layer_source}


def _population_and_join(layer_data: bytes) -> dict:
    covariates = json.loads(COVARIATES.read_text("utf-8"))
    if len(covariates) != 5410:
        raise InvalidStop("covariates do not carry 5,410 rows")
    population = [
        {"id": r["id"].strip(), "site": r["site"].strip(),
         "period": (r["period_raw"] or "").strip(),
         "phase": (r["phase_raw"] or "").strip(),
         "composition_stratum": r["composition_stratum"],
         "preservation_class": r["preservation_class"]}
        for r in covariates
    ]
    if len({r["id"] for r in population}) != 5410:
        raise InvalidStop("population IDs are not 5,410 unique")
    by_site = dict(Counter(r["site"] for r in population))
    if by_site != POPULATION_BY_SITE:
        raise InvalidStop(f"population by site differs: {by_site}")
    # The layer, indexed by stripped inscription id.
    layer_rows = {}
    layer_count = 0
    for row in csv.DictReader(io.StringIO(layer_data.decode("utf-8"))):
        layer_count += 1
        key = (row.get("id") or "").strip()
        if key in layer_rows:
            raise InvalidStop(f"duplicate layer id: {key}")
        layer_rows[key] = row
    # Covariate<->layer agreement on every population row,
    # under the Phase-139 value convention, plus duplicate /
    # missing coverage of the join key.
    mismatches = []
    for r in population:
        lr = layer_rows.get(r["id"])
        if lr is None:
            mismatches.append({"id": r["id"], "field": "presence"})
            continue
        if (lr.get("site") or "").strip() != r["site"]:
            mismatches.append({"id": r["id"], "field": "site"})
        for field, cov in (("period", r["period"]),
                           ("phase", r["phase"])):
            lv = lr.get(field)
            if _unrecorded(cov) and _unrecorded(lv):
                continue
            if _unrecorded(cov) != _unrecorded(lv) or (
                    not _unrecorded(cov) and lv.strip() != cov):
                mismatches.append({"id": r["id"], "field": field})
    if mismatches:
        raise InvalidStop(
            f"covariate/layer disagreement on {len(mismatches)} rows")
    # The label census and margins, from the covariates.
    margins = Counter()
    census = Counter()
    for row in population:
        p_inf = _informative(row["period"])
        f_inf = _informative(row["phase"])
        margins["period"] += p_inf
        margins["phase"] += f_inf
        margins["both"] += p_inf and f_inf
        margins["union"] += p_inf or f_inf
        margins["neither"] += (not p_inf) and (not f_inf)
        for field in ("period", "phase"):
            if _informative(row[field]):
                census[(row["site"], field, row[field])] += 1
    if dict(margins) != EXPECTED_MARGINS:
        raise InvalidStop(f"label margins differ: {dict(margins)}")
    # The accepted artifact: 78 cells, schema facts as frozen.
    cells = [json.loads(ln) for ln in
             ARTIFACT.read_text("utf-8").splitlines() if ln.strip()]
    if len(cells) != 78:
        raise InvalidStop("artifact does not carry 78 cells")
    cellmap = {(c["site"], c["field"], c["local_label"]): c
               for c in cells}
    if len(cellmap) != 78:
        raise InvalidStop("artifact cell keys are not 78 unique")
    if set(census) != set(cellmap):
        raise InvalidStop("census triples differ from the artifact's")
    for key, n in census.items():
        if cellmap[key]["attested_rows"] != n:
            raise InvalidStop(f"attested_rows differ at {key}")
    mapped_by_period = Counter(
        c["coarse_period"] for c in cells if c["status"] == "MAPPED")
    if dict(mapped_by_period) != {"EARLY": 4, "MATURE": 18, "LATE": 2}:
        raise InvalidStop("artifact MAPPED census differs")
    contested_cells = sum(1 for c in cells if c["contested"])
    # The section 4.1 join under derivation A1.
    placed = Counter()
    placed_by_site_period: dict[str, Counter] = defaultdict(Counter)
    unplaced = Counter()
    assignments: dict[str, str] = {}
    strata: dict[tuple, set] = defaultdict(set)
    strata_rows: Counter = Counter()
    for row in population:
        row_cells = [
            cellmap[(row["site"], field, row[field])]
            for field in ("period", "phase")
            if _informative(row[field])
        ]
        period = None
        if not row_cells:
            unplaced["no_informative_label"] += 1
        else:
            mapped = [c for c in row_cells if c["status"] == "MAPPED"]
            if mapped:
                values = {c["coarse_period"] for c in mapped}
                if len(values) == 1:
                    period = mapped[0]["coarse_period"]
                else:
                    unplaced["disagreement"] += 1
            elif any(c["contested"] for c in row_cells):
                unplaced["contested_only"] += 1
            else:
                unplaced["all_unassigned"] += 1
        assignments[row["id"]] = period or "UNASSIGNED"
        if period is not None:
            placed[period] += 1
            placed_by_site_period[row["site"]][period] += 1
            key = (row["composition_stratum"],
                   row["preservation_class"], period)
            strata[key].add(row["site"])
            strata_rows[key] += 1
    if len(assignments) != 5410:
        raise InvalidStop("join does not cover 5,410 rows exactly")
    if dict(placed) != EXPECTED_PLACED:
        raise InvalidStop(f"A1 placed counts differ: {dict(placed)}")
    if dict(unplaced) != EXPECTED_UNPLACED:
        raise InvalidStop(f"A1 unplaced counts differ: {dict(unplaced)}")
    placed_by_site = {s: sum(c.values())
                      for s, c in placed_by_site_period.items()}
    if placed_by_site != EXPECTED_PLACED_BY_SITE:
        raise InvalidStop(f"A1 placed-by-site differs: {placed_by_site}")
    return {
        "layer_rows_total": layer_count,
        "population_rows": 5410,
        "population_by_site": by_site,
        "label_margins": dict(margins),
        "census_triples": len(census),
        "covariate_layer_agreement": {
            "rows_checked": 5410, "mismatches": 0},
        "artifact_cells": {"total": 78,
                           "mapped_by_period": dict(mapped_by_period),
                           "unassigned": 54,
                           "contested": contested_cells},
        "placed": dict(placed),
        "unplaced": dict(unplaced),
        "placed_by_site": placed_by_site,
        "placed_by_site_period": {
            s: dict(c) for s, c in sorted(placed_by_site_period.items())},
        "assignments": assignments,
        "strata": strata,
        "strata_rows": strata_rows,
    }


def _margins(join: dict) -> dict:
    placed = join["placed"]
    unplaced_total = sum(join["unplaced"].values())
    assigned_total = sum(placed.values())
    sites_per_period = {}
    for p in PERIODS:
        sites_per_period[p] = sorted(
            s for s, c in join["placed_by_site_period"].items()
            if c.get(p, 0) >= 1)
    permutable = sum(n for key, n in join["strata_rows"].items()
                     if len(join["strata"][key]) >= 2)
    multi_strata = sum(1 for key in join["strata"]
                       if len(join["strata"][key]) >= 2)
    by_site = {}
    for site in sorted(POPULATION_BY_SITE):
        pop = POPULATION_BY_SITE[site]
        asg = join["placed_by_site"].get(site, 0)
        by_site[site] = {
            "population": pop, "assigned": asg,
            "unassigned": pop - asg,
            "unassigned_share": round((pop - asg) / pop, 6),
            "assigned_by_period": dict(
                join["placed_by_site_period"].get(site, {}))}
    arms = [
        {"arm": 1, "rule": "each of EARLY, MATURE, LATE retains "
                           "assigned inscriptions from at least 5 "
                           "distinct sites",
         "observed": {p: len(sites_per_period[p]) for p in PERIODS},
         "sites": sites_per_period,
         "verdict": "PASS" if all(
             len(sites_per_period[p]) >= 5 for p in PERIODS)
         else "FAIL"},
        {"arm": 2, "rule": "unassigned share at most 40% of the "
                           "5,410-row population",
         "observed": {"unassigned": unplaced_total,
                      "population": 5410,
                      "share": round(unplaced_total / 5410, 6)},
         "verdict": "PASS" if unplaced_total / 5410 <= 0.40
         else "FAIL"},
        {"arm": 3, "rule": "permutable inscriptions under the "
                           "primary strata at least 1,000 (DD-040-6, "
                           "retained)",
         "observed": {"permutable": permutable},
         "verdict": "PASS" if permutable >= 1000 else "FAIL"},
    ]
    return {
        "assigned_total": assigned_total,
        "unassigned_total": unplaced_total,
        "unassigned_share": round(unplaced_total / 5410, 6),
        "unplaced_reasons": join["unplaced"],
        "assigned_by_period": {p: placed[p] for p in PERIODS},
        "sites_per_period": {p: len(sites_per_period[p])
                             for p in PERIODS},
        "sites_per_period_named": sites_per_period,
        "contested_excluded": join["unplaced"].get("contested_only", 0),
        "by_site": by_site,
        "strata": {"strata_total": len(join["strata"]),
                   "strata_multi_site": multi_strata,
                   "permutable_inscriptions": permutable},
        "arms": arms,
        "gate_verdict": "PASS" if all(
            a["verdict"] == "PASS" for a in arms) else "FAIL",
    }


def _build_core() -> dict:
    pins = _gate_pins()
    join = _population_and_join(pins["layer_data"])
    margins = _margins(join)
    return {"pins": {k: v for k, v in pins["checks"].items()},
            "layer_source": pins["layer_source"],
            "join": {k: v for k, v in join.items()
                     if k not in ("assignments", "strata",
                                  "strata_rows")},
            "margins": margins}


def _headline(record: dict) -> str:
    m = record["margins"]
    spp = m["sites_per_period"]
    arms = {a["arm"]: a["verdict"] for a in m["arms"]}
    return (
        "On the ICIT-lineage layer (horus84), Spec 040 "
        "(Phase-439) closes NOT-YET-TESTABLE at the section 5 "
        "margins gate. Assignment census under derivation A1, "
        "consuming Spec 041's artifact "
        "data/evidence_integration/site_period_mapping.jsonl "
        f"(SHA-256 {ARTIFACT_SHA256}; Spec 039's artifact, named "
        "in the freeze record, did not satisfy section 1 and is "
        "not the consumed artifact): assigned "
        f"{m['assigned_total']} of 5,410 inscriptions "
        f"({100 * (1 - m['unassigned_share']):.1f}%), unassigned "
        f"{m['unassigned_total']} ({100 * m['unassigned_share']:.1f}%) "
        f"— no informative label "
        f"{m['unplaced_reasons']['no_informative_label']}; all "
        f"labels UNASSIGNED "
        f"{m['unplaced_reasons']['all_unassigned']}; "
        f"{m['unplaced_reasons']['disagreement']} disagreement "
        "left unplaced; contested-excluded "
        f"{m['contested_excluded']}. Margins gate: arm 1 "
        f"{arms[1]} (EARLY retains assigned inscriptions from "
        f"{spp['EARLY']} distinct site(s), MATURE from "
        f"{spp['MATURE']}, LATE from {spp['LATE']}, against the "
        f"5-site arm); arm 2 {arms[2]} (unassigned share "
        f"{100 * m['unassigned_share']:.1f}% against the 40% "
        f"arm); arm 3 {arms[3]} (permutable inscriptions "
        f"{m['strata']['permutable_inscriptions']} against the "
        "1,000 arm, DD-040-6 retained). No profile table, no "
        "permutation, and no interval was computed; the section "
        "7 regression and the section 6 primary were not "
        "reached. G1 stands unchanged: SUPPORTED under "
        "composition and preservation control, with the "
        "standing rider carried verbatim in this record.")


def _report_md(record: dict) -> str:
    m = record["margins"]
    g = {x["gate"]: x["verdict"] for x in record["gates"]}
    lines = [
        "# Phase-439 — Spec 040 (D-25): G1 with time held fixed",
        "",
        "Claim under test: `STUDY-SPEC-025/G1` — site-repertoire "
        "differentiation on the ICIT-lineage layer (horus84), "
        "SUPPORTED under composition and preservation control "
        "(Phase-140; governing basic interval [0.1838, 0.2102] "
        "against the V = 0.10 floor, Phase-385), with the standing "
        "rider: \"Chronology is NOT controlled in the primary "
        "test: period/phase (chronology) remain uncontrolled "
        "confounders; the S-chron sensitivity bound is reported "
        "alongside, never as the controlled verdict.\" Freeze "
        f"digest `{FREEZE_DIGEST}`; OSF registration 2rgtb "
        "(approved, public). Executed 2026-10-24 under the "
        "owner's execution order of 2026-10-24.",
        "",
        "## Step-0 gates (in order, fail-closed)",
        "",
        f"- **Gate 1 — pin verification (E2): {g['1']}**",
        f"- **Gate 2 — population reproduction and the section "
        f"4.1 join under A1 (E2): {g['2']}**",
        f"- **Gate 3 — determinism: {g['3']}**",
        "",
        "## Margins (spec section 5 — margins only)",
        "",
        f"- Assigned {m['assigned_total']} of 5,410 "
        f"({100 * (1 - m['unassigned_share']):.1f}%); unassigned "
        f"{m['unassigned_total']} "
        f"({100 * m['unassigned_share']:.1f}%): no informative "
        f"label {m['unplaced_reasons']['no_informative_label']}, "
        f"all labels UNASSIGNED "
        f"{m['unplaced_reasons']['all_unassigned']}, "
        f"{m['unplaced_reasons']['disagreement']} disagreement "
        f"unplaced, contested-excluded "
        f"{m['contested_excluded']}.",
        f"- Assigned by period: EARLY "
        f"{m['assigned_by_period']['EARLY']}, MATURE "
        f"{m['assigned_by_period']['MATURE']}, LATE "
        f"{m['assigned_by_period']['LATE']}.",
        f"- Distinct sites with assigned inscriptions: EARLY "
        f"{m['sites_per_period']['EARLY']} "
        f"({', '.join(m['sites_per_period_named']['EARLY'])}), "
        f"MATURE {m['sites_per_period']['MATURE']} "
        f"({', '.join(m['sites_per_period_named']['MATURE'])}), "
        f"LATE {m['sites_per_period']['LATE']} "
        f"({', '.join(m['sites_per_period_named']['LATE'])}).",
        f"- Permutable inscriptions under the primary strata: "
        f"{m['strata']['permutable_inscriptions']} "
        f"({m['strata']['strata_multi_site']} of "
        f"{m['strata']['strata_total']} strata hold at least 2 "
        "distinct sites).",
        "",
        "## The margins gate (all three arms must hold)",
        "",
    ]
    for a in m["arms"]:
        lines.append(f"- **Arm {a['arm']} — {a['verdict']}:** "
                     f"{a['rule']}.")
    lines += [
        "",
        "## Outcome",
        "",
        "**NOT-YET-TESTABLE** (DD-040-5)",
        "",
        record["headline_wording"],
        "",
        "## Limits",
        "",
        "- This closure is a statement about the assignment "
        "the published record supports, not a verdict on G1: "
        "no repertoire quantity was computed, and G1 stands "
        "exactly as Spec 025 and Phase-385 left it, rider "
        "intact (spec sections 5, 9, 11).",
        "- Every number describes the ICIT-lineage layer "
        "(horus84) — a derivative compilation, not an "
        "independent witness — never \"the Indus corpus\" in "
        "general (spec section 11.1).",
        "- Period assignment is constructed context: its "
        "published sources, mapping rules, coverage, and "
        "contested exclusions travel with every number that "
        "uses it; a result quoted without its assignment "
        "census is a misquote of this spec (spec section 11.6).",
        "- Assignment sparsity is structural: local "
        "chronological labels are recorded for a minority of "
        "layer rows and are missing by site (Mohenjo-daro "
        "places 0 of its 1,923 population rows under A1); the "
        "section 5 gate exists because this design may "
        "honestly close unrun (spec section 12).",
        "- Negative, weakened, and NOT-YET-TESTABLE outcomes "
        "publish with the same prominence as supported ones "
        "(spec section 11.7).",
        "",
        "---",
        "",
        f"*AI disclosure: {AI_DISCLOSURE}*",
        "",
    ]
    return "\n".join(lines)


def run() -> int:
    anchors_before = _sha(ANCHORS)
    if anchors_before != ANCHORS_SHA256:
        raise InvalidStop("anchors do not hash to their pin")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True,
        text=True, cwd=str(REPO)).stdout.strip()
    core1 = _build_core()
    core2 = _build_core()
    canon1 = json.dumps(core1, sort_keys=True)
    canon2 = json.dumps(core2, sort_keys=True)
    determinism = canon1 == canon2
    if not determinism:
        raise InvalidStop("the step-0 + margins computation is "
                          "not deterministic across two runs")
    margins = core1["margins"]
    gate_pass = margins["gate_verdict"] == "PASS"
    record = {
        "spec": "040",
        "phase": 439,
        "claim_under_test": "STUDY-SPEC-025/G1",
        "contract": {
            "freeze_digest": FREEZE_DIGEST,
            "osf_registration": "2rgtb",
            "derivation": "A1",
            "dependency": "Spec 041 artifact accepted at the "
                          "freeze by successor-artifact "
                          "substitution (Spec 039 executed and "
                          "named; its artifact recorded as NOT "
                          "satisfying section 1)",
            "rulings": ["DD-040-1 adopted",
                        "DD-040-5 confirmed (NOT-YET-TESTABLE)",
                        "DD-040-6 retained (all three section 5 "
                        "arms)"],
        },
        "execution": {
            "date": "2026-10-24",
            "order": "owner's execution order of 2026-10-24 "
                     "(19:04 EDT)",
            "executed_from_commit": head,
            "venue": "program VM; the fresh git worktree off "
                     "origin/main was reaped by the VM write "
                     "restriction mid-run, so the run executed "
                     "in a minimal tree assembled from "
                     "origin/main via the API with every input "
                     "hash-verified at step 0 (see "
                     "step0-record.md)",
        },
        "gates": [
            {"gate": "1", "name": "pin verification (E2)",
             "verdict": "PASS",
             "detail": "every freeze section 3 pin recomputed; "
                       "the freeze record replays; the layer "
                       "asserted at its pin before any use"},
            {"gate": "2", "name": "population reproduction and "
                                  "the section 4.1 join under A1 "
                                  "(E2)",
             "verdict": "PASS",
             "detail": "5,410 population rows reproduced; the "
                       "join yields exactly one assignment row "
                       "per inscription ID and reproduces the "
                       "freeze section 3 A1 counts exactly"},
            {"gate": "3", "name": "determinism",
             "verdict": "PASS",
             "detail": "the step-0 + margins record computed "
                       "twice from the pinned inputs; canonical "
                       "records identical"},
        ],
        "step0": {
            "pins": core1["pins"],
            "layer_source": core1["layer_source"],
            "join": core1["join"],
            "determinism": {"runs": 2, "canonical_identical": True},
        },
        "margins": margins,
        "margins_gate": {
            "verdict": margins["gate_verdict"],
            "closure": None if gate_pass else "NOT-YET-TESTABLE",
        },
        "regression": None if gate_pass else {
            "status": "NOT REACHED",
            "reason": "the section 5 margins gate failed; spec "
                      "section 13 places the regression after "
                      "the margins gate"},
        "primary": None if gate_pass else {
            "status": "NOT REACHED",
            "reason": "the section 5 margins gate failed; no "
                      "profile table outcome, no permutation, "
                      "no interval computed (spec section 5)"},
        "sensitivities": None if gate_pass else {
            "status": "NOT REACHED",
            "reason": "no primary outcome exists to bound "
                      "(spec section 8)"},
        "outcome": None if gate_pass else "NOT-YET-TESTABLE",
        "headline_wording": None,
        "anchors": {"file": "backend/reports/INDUS_FINAL_ANCHORS.json",
                    "pin": ANCHORS_SHA256,
                    "before": anchors_before,
                    "after": _sha(ANCHORS),
                    "byte_identical": anchors_before == _sha(ANCHORS)},
        "ai_disclosure": AI_DISCLOSURE,
    }
    if gate_pass:
        raise InvalidStop(
            "the margins gate PASSED at execution: this runner "
            "implements the frozen shape through the gate; the "
            "section 7 regression and section 6 primary require "
            "their own build before any outcome is recorded — "
            "no outcome is recorded by this run")
    record["headline_wording"] = _headline(record)
    RESULTS.write_text(json.dumps(record, indent=2) + "\n", "utf-8")
    REPORT.write_text(_report_md(record), "utf-8")
    print(record["headline_wording"])
    print(f"\nOutcome: {record['outcome']} — margins gate "
          f"{margins['gate_verdict']} "
          f"(arms: {[a['verdict'] for a in margins['arms']]})")
    return 0


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "run":
        print(__doc__)
        return 2
    try:
        return run()
    except InvalidStop as exc:
        print(f"INVALID — {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
