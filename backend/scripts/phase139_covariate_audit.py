#!/usr/bin/env python3
"""Phase-139 (spec 025, FROZEN 2026-10-10, spec.md sec.11) —
covariate audit + harmonization for the Stage 2 controlled
follow-up. MARGINS ONLY.

This phase decides whether the Spec 025 test G1 is estimable
under control. It computes coverage, missingness structure,
harmonized covariate margins, and permutable-inscription
projections. It computes NO association statistic, NO
repertoire comparison, and NO G1 quantity of any kind: sign
tokens are read only to reproduce the Phase-137 F3 population
and its composition strata (the Phase-137 definitions, copied
below), never tabulated against any covariate.

Frozen design (specs/025-stage2-controlled-followup/spec.md,
adjudicated sec.11; plan.md Phase-139):

- Population: the Phase-137 F3 analysis population of the
  ICIT-lineage layer (horus84 ``inscriptions.csv``, sha256
  asserted): sites eligible under the Phase-137 rule
  (>= 30 inscriptions AND >= 100 parsed tokens in the layer's
  parsed population), rows with >= 1 parsed token
  (``re.findall(r"\\d{3}", text)``). Expected: 5,410 rows,
  7 sites.
- Candidate covariates (sec.4.1): the raw ``period`` /
  ``phase`` fields (provenance margins), the harmonized
  ``chron_band`` (Q2(a): published-stratigraphy harmonization,
  <= 3 bands early/middle/late + UNRECORDED, per-cell
  citations or UNRECORDED — see CHRON_MAPPING / CITATIONS),
  ``depth_band`` (Q3(a): within-site relative tertiles of
  parsed depth within (site x unit) groups), and
  ``preservation`` (collapsed: complete / fragment / damaged).
- Composition strata (for the permutable-N projection):
  Phase-137 F3 strata, type class x length class, crossed
  with the covariate under assessment; UNRECORDED is retained
  as its own stratum level (sec.4.2 step 3).
- Eligibility gate (sec.4.2 step 3, thresholds approved as
  drafted at adjudication Q5): a candidate covariate is a
  PRIMARY CONTROL iff (i) recorded coverage on the F3
  population >= 70%, (ii) >= 3 eligible sites contribute
  >= 30 recorded inscriptions each, and (iii) the permutable
  count under composition x covariate strata >= 1,000.
  Routing rule (adjudication amendment, sec.4.2): a
  gate-failing approved covariate routes to the sensitivity
  panel (EXPLORATORY); if exactly one covariate passes, the
  primary strata are composition x that covariate; if none
  passes, G1 is NOT ESTIMABLE (sec.4.3 F-c).

Inputs live in the local store (never committed). Outputs
(committed): ``reports/phase139_results.json``,
``data/evidence_integration/phase139_harmonized_covariates
.json`` (+ ``_meta.json``),
``data/evidence_integration/phase139_citation_register
.json``. Deterministic: no wall-clock in outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SWEEP = (Path.home() / "workspace" / "research_notes"
         / "indus-data-deep-sweep-20261008" / "downloads")
DEFAULT_HORUS = (SWEEP / "horus84-computational-linguistics"
                 / "data" / "inscriptions.csv")
DEFAULT_OUT = REPO_ROOT / "reports" / "phase139_results.json"
DEFAULT_DATASET = (REPO_ROOT / "data" / "evidence_integration"
                   / "phase139_harmonized_covariates.json")
DEFAULT_REGISTER = (REPO_ROOT / "data" / "evidence_integration"
                    / "phase139_citation_register.json")
ANCHORS = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)
LAYER_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
)

# Phase-137 site-inclusion rule (uniform), copied semantics.
MIN_SITE_INSCRIPTIONS = 30
MIN_SITE_TOKENS = 100

# Frozen eligibility gate (spec 025 sec.4.2 step 3; Q5).
GATE_MIN_COVERAGE = 0.70
GATE_MIN_SITES = 3
GATE_MIN_SITE_RECORDED = 30
GATE_MIN_PERMUTABLE = 1000

UNRECORDED = "UNRECORDED"
MISSING_SENTINELS = {"", "-"}

AI_DISCLOSURE = (
    "Produced by an AI agent (Muse Spark, via Muse) at "
    "the direction of Tristen Pierson, per constitution "
    "section VI."
)


# ---------------------------------------------------------------------------
# Composition strata — Phase-137 F3 definitions (identical semantics;
# copied from backend/scripts/phase137_site_repertoire.py)
# ---------------------------------------------------------------------------

def horus_length_class(n_parsed_tokens: int) -> str:
    if n_parsed_tokens <= 1:
        return "1"
    if n_parsed_tokens <= 3:
        return "2-3"
    if n_parsed_tokens <= 5:
        return "4-5"
    return "6+"


def horus_type_class(type_value: str) -> str:
    prefix = (type_value or "").split(":")[0]
    if prefix in ("SEAL", "TAB", "POT"):
        return prefix
    return "OTHER"


def composition_stratum(type_value: str, n_parsed_tokens: int) -> str:
    return (f"{horus_type_class(type_value)}|"
            f"{horus_length_class(n_parsed_tokens)}")


def site_eligible(n_inscriptions: int, n_tokens: int) -> bool:
    return (n_inscriptions >= MIN_SITE_INSCRIPTIONS
            and n_tokens >= MIN_SITE_TOKENS)


# ---------------------------------------------------------------------------
# Chronology harmonization (Q2(a)) — published stratigraphies only.
# Every mapped cell carries a citation key; every unmapped cell is
# UNRECORDED with the reason recorded. No invented mappings.
# ---------------------------------------------------------------------------

CITATIONS = {
    "KENOYER2008": (
        "Kenoyer, J.M. (2008), 'Indus Urbanism' (Sackler "
        "Colloquium); harappa.com Ch. 1 periodization (after "
        "Meadow & Kenoyer 2001): Harappa Period 1 Ravi and "
        "Period 2 Kot Diji = Early Harappan; Period 3A/3B/3C "
        "'Harappa Phase A/B/C' = Mature Harappan; Period 4 "
        "Transitional and Period 5 Cemetery H = Late "
        "Harappan era; concordance: Harappan 2 (Kot Diji) "
        "incl. Nausharo I, Harappan 3A incl. Nausharo II; "
        "Dholavira chronology after Bisht: Stages I-III "
        "Regionalisation era, IV-V Integration era, VI "
        "Localisation era (c.1900-1700 BCE), VII after 1700."),
    "BISHT_DHOLAVIRA": (
        "Bisht, R.S., Dholavira excavations (1989; 2000): "
        "seven-stage site sequence; stage-to-era assignment "
        "as summarized in Kenoyer 2008 (see KENOYER2008)."),
    "MARSHALL1931": (
        "Marshall, J. (1931), Mohenjo-daro and the Indus "
        "Civilization: the site's published Early / "
        "Intermediate / Late period terminology."),
    "MACKAY1938": (
        "Mackay, E.J.H. (1938), Further Excavations at "
        "Mohenjo-daro: 'Late period' and 'intermediate "
        "Period' in the excavator's own usage."),
    "LAL_THAPAR_KALIBANGAN": (
        "Lal, B.B. & Thapar, B.K., Kalibangan excavations "
        "1960-69 (ASI): Period I = Early Harappan "
        "(Soti-Siswal), Period II = Mature Harappan."),
    "RAO1979_LOTHAL": (
        "Rao, S.R. (1979), Lothal: A Harappan Port Town "
        "(1955-62), ASI: Period A = Mature Harappan, "
        "divided into phases I-IV; Period B = Late "
        "Harappan (= Phase V); Rao 1963 (as summarized in "
        "Lal 1997): Lothal Period V is the degeneration "
        "(Late) phase."),
    "JARRIGE1993_NAUSHARO": (
        "Jarrige, J.-F. (1993) and the published Nausharo "
        "chronology: Period I (IA-ID, c.2900-2550 BCE) "
        "pre-Mature (Period I corresponds to Mehrgarh VII); "
        "Period II (IIA-IIB, to c.1900 BCE) = Mature "
        "Harappan; Period III (c.1900-1800 BCE) = Late era. "
        "The scheme has no Period IV."),
}

# (site, field, raw value) -> (band, citation key).
# Prefix rules (Stratum/Layer) are handled in map_chron_cell.
CHRON_MAP = {
    # Mohenjo-daro — period field (site-published terminology)
    ("Mohenjo-daro", "period", "Early"): ("early", "MARSHALL1931"),
    ("Mohenjo-daro", "period", "Intermediate"): ("middle", "MACKAY1938"),
    ("Mohenjo-daro", "period", "Late"): ("late", "MACKAY1938"),
    # Harappa — period field (HARP periodization)
    ("Harappa", "period", "1"): ("early", "KENOYER2008"),
    ("Harappa", "period", "2"): ("early", "KENOYER2008"),
    ("Harappa", "period", "3"): ("middle", "KENOYER2008"),
    ("Harappa", "period", "4"): ("late", "KENOYER2008"),
    ("Harappa", "period", "5"): ("late", "KENOYER2008"),
    ("Harappa", "period", "4/5"): ("late", "KENOYER2008"),
    # Harappa — phase field (Period 3 subdivisions A/B/C)
    ("Harappa", "phase", "A"): ("middle", "KENOYER2008"),
    ("Harappa", "phase", "B"): ("middle", "KENOYER2008"),
    ("Harappa", "phase", "C"): ("middle", "KENOYER2008"),
    ("Harappa", "phase", "B/C"): ("middle", "KENOYER2008"),
    ("Harappa", "phase", "A-C"): ("middle", "KENOYER2008"),
    # Dholavira — period field carries Bisht stage numbers
    ("Dholavira", "period", "1"): ("early", "BISHT_DHOLAVIRA"),
    ("Dholavira", "period", "2"): ("early", "BISHT_DHOLAVIRA"),
    ("Dholavira", "period", "3"): ("early", "BISHT_DHOLAVIRA"),
    ("Dholavira", "period", "4"): ("middle", "BISHT_DHOLAVIRA"),
    ("Dholavira", "period", "5"): ("middle", "BISHT_DHOLAVIRA"),
    ("Dholavira", "period", "6"): ("late", "BISHT_DHOLAVIRA"),
    ("Dholavira", "period", "4/5"): ("middle", "BISHT_DHOLAVIRA"),
    # Kalibangan — period field
    ("Kalibangan", "period", "1"): ("early", "LAL_THAPAR_KALIBANGAN"),
    ("Kalibangan", "period", "2"): ("middle", "LAL_THAPAR_KALIBANGAN"),
    # Lothal — period 'A' and phase field (Rao)
    ("Lothal", "period", "A"): ("middle", "RAO1979_LOTHAL"),
    ("Lothal", "phase", "I"): ("middle", "RAO1979_LOTHAL"),
    ("Lothal", "phase", "II"): ("middle", "RAO1979_LOTHAL"),
    ("Lothal", "phase", "III"): ("middle", "RAO1979_LOTHAL"),
    ("Lothal", "phase", "IV"): ("middle", "RAO1979_LOTHAL"),
    ("Lothal", "phase", "II-III"): ("middle", "RAO1979_LOTHAL"),
    ("Lothal", "phase", "V"): ("late", "RAO1979_LOTHAL"),
    # Nausharo — period field (Jarrige)
    ("Nausharo", "period", "1"): ("early", "JARRIGE1993_NAUSHARO"),
    ("Nausharo", "period", "2"): ("middle", "JARRIGE1993_NAUSHARO"),
    ("Nausharo", "period", "3"): ("late", "JARRIGE1993_NAUSHARO"),
}

# Documented non-mappings: (site, field, matcher) -> reason.
CHRON_UNMAPPED_REASONS = [
    (("Harappa", "period", "2/3"),
     "Spans the Early/Mature boundary in the cited scheme; "
     "no single band is citable."),
    (("Harappa", "period", "3/4"),
     "Spans the Mature/Late boundary in the cited scheme; "
     "no single band is citable."),
    (("Harappa", "phase", "B?"),
     "Uncertain attribution in the layer itself (queried "
     "value); not citable to a band."),
    (("Dholavira", "period", "5/6"),
     "Spans the Integration/Localisation (Mature/Late) "
     "boundary in Bisht's scheme."),
    (("Dholavira", "period", "5?"),
     "Uncertain attribution in the layer itself (queried "
     "value); not citable to a band."),
    (("Nausharo", "period", "4"),
     "No Period IV exists in Jarrige's published Nausharo "
     "chronology (the sequence ends at Period III)."),
]


def map_chron_cell(site: str, field: str, raw: str):
    """Return (band, citation_key) or (None, reason)."""
    value = (raw or "").strip()
    if value in MISSING_SENTINELS:
        return None, "missing in layer"
    hit = CHRON_MAP.get((site, field, value))
    if hit:
        return hit[0], hit[1]
    for (s, f, v), reason in CHRON_UNMAPPED_REASONS:
        if (s, f, v) == (site, field, value):
            return None, reason
    if site == "Harappa" and field == "phase" \
            and value.startswith("Stratum"):
        return None, ("Vats-era stratum label; no correlation "
                      "to the HARP periodization was citable "
                      "from the published sources consulted.")
    if site == "Lothal" and field == "period" \
            and value.startswith("Layer"):
        return None, ("Excavation layer number; no published "
                      "layer-to-period correlation for Lothal "
                      "was citable from the sources consulted.")
    return None, ("No published-stratigraphy cell for this "
                  "(site, field, value) in the consulted "
                  "schemes.")


def harmonize_chron(site: str, period_raw: str, phase_raw: str):
    """Precedence: a mapped period cell wins; else a mapped
    phase cell; both mapped and disagreeing -> period band,
    conflict flagged. Returns (band, source_field,
    citation_key)."""
    p_band, p_cite = map_chron_cell(site, "period", period_raw)
    f_band, f_cite = map_chron_cell(site, "phase", phase_raw)
    if p_band and f_band:
        return p_band, "period", p_cite, p_band != f_band
    if p_band:
        return p_band, "period", p_cite, False
    if f_band:
        return f_band, "phase", f_cite, False
    return UNRECORDED, None, None, False


# ---------------------------------------------------------------------------
# Preservation collapse (sec.4.1: original spellings retained per row)
# ---------------------------------------------------------------------------

PRESERVATION_MAP = {
    "complete": "complete",
    "fragment": "fragment",
    "chipped": "damaged",
    "slightly chipped": "damaged",
    "partly damaged": "damaged",
}


def collapse_preservation(raw: str) -> str:
    value = (raw or "").strip()
    return PRESERVATION_MAP.get(value, UNRECORDED)


# ---------------------------------------------------------------------------
# Depth parsing (Q3(a)) — documented, deterministic.
#
# Categories: VALUE (single number with unit), RANGE (two numbers
# separated by '-', midpoint taken), DECIMAL_DOTDOT (the layer's
# 'X..Y' notation, read as the decimal X.Y — counted separately),
# COLON_FT_IN (the layer's single 'F:I ft' feet:inches notation,
# read as F + I/12 feet; n = 1 in the population), SURFACE (the
# word 'surface': depth 0.0 in the site's primary unit group),
# UNITLESS (a number with no unit token: its own unit group
# 'unspecified'), UNPARSED (anything else; counted, treated as
# missing), MISSING (sentinels).
# Tertiles are computed WITHIN (site x unit) groups only; groups
# with n < 9 parsed rows are not banded (rows -> UNRECORDED).
# Banding is by rank: row i (0-based, sorted by (value, id)) of
# n -> band floor(3i/n) in {shallow, middle, deep}. 'Shallow' is
# the smallest numeric value in the group; the bands are
# within-site RELATIVE by construction (sec.4.2 step 2).
# ---------------------------------------------------------------------------

DEPTH_MIN_GROUP = 9
_DEPTH_NUM = re.compile(r"\d+(?:\.\d+)?")
_DEPTH_UNIT = re.compile(r"\b(ft|cm|m|in)\b")
DEPTH_BANDS = ["shallow", "middle", "deep"]


def parse_depth(raw: str):
    """Return (category, value_or_None, unit_or_None)."""
    text = (raw or "").strip()
    if text in ("", "-", "- -"):
        return "MISSING", None, None
    low = text.lower()
    unit_m = _DEPTH_UNIT.search(low)
    unit = unit_m.group(1) if unit_m else None
    if "surface" in low:
        return "SURFACE", 0.0, unit
    sign = -1.0 if low.lstrip().startswith("-") else 1.0
    colon = re.fullmatch(
        r"[+-]?(\d+):(\d+)\s*(ft|m|cm|in)", low)
    if colon:
        value = sign * (int(colon.group(1))
                        + int(colon.group(2)) / 12.0)
        return "COLON_FT_IN", value, colon.group(3)
    if ".." in low:
        parts = _DEPTH_NUM.findall(low)
        if len(parts) == 2:
            value = sign * float(f"{parts[0]}.{parts[1]}")
            return "DECIMAL_DOTDOT", value, unit or "unspecified"
        return "UNPARSED", None, unit
    nums = _DEPTH_NUM.findall(low)
    if len(nums) == 2 and "-" in low:
        lo_v, hi_v = float(nums[0]), float(nums[1])
        return "RANGE", (lo_v + hi_v) / 2.0, unit or "unspecified"
    if len(nums) == 1:
        value = sign * float(nums[0])
        if unit:
            return "VALUE", value, unit
        return "UNITLESS", value, "unspecified"
    return "UNPARSED", None, unit


def assign_depth_bands(parsed_rows):
    """parsed_rows: population row dicts carrying depth_category,
    depth_value, depth_unit. Mutates: sets depth_band and
    depth_group_n (and depth_unit for SURFACE rows, which join
    the site's primary unit group — the modal unit among the
    site's VALUE/RANGE/DECIMAL_DOTDOT/UNITLESS rows — at 0.0).
    Returns margins dict."""
    by_site_unit: dict[tuple, list] = defaultdict(list)
    unit_counts: dict[str, Counter] = defaultdict(Counter)
    for row in parsed_rows:
        if row["depth_category"] in (
                "VALUE", "RANGE", "DECIMAL_DOTDOT",
                "COLON_FT_IN", "UNITLESS"):
            unit_counts[row["site"]][row["depth_unit"]] += 1
    primary_unit = {}
    for site, counts in unit_counts.items():
        primary_unit[site] = counts.most_common(1)[0][0]
    for row in parsed_rows:
        row["depth_band"] = UNRECORDED
        row["depth_group_n"] = 0
        if row["depth_value"] is None:
            continue
        unit = row["depth_unit"]
        if row["depth_category"] == "SURFACE":
            unit = primary_unit.get(row["site"])
            if unit is None:
                continue
            row["depth_unit"] = unit
        by_site_unit[(row["site"], unit)].append(row)
    boundary_tie_rows = 0
    group_margins = {}
    for (site, unit), members in sorted(by_site_unit.items()):
        n = len(members)
        group_margins[f"{site}|{unit}"] = n
        if n < DEPTH_MIN_GROUP:
            continue
        members.sort(key=lambda r: (r["depth_value"], str(r["id"])))
        band_of_value = {}
        for i, row in enumerate(members):
            band = DEPTH_BANDS[min(2, (3 * i) // n)]
            row["depth_band"] = band
            row["depth_group_n"] = n
            if row["depth_value"] in band_of_value \
                    and band_of_value[row["depth_value"]] != band:
                boundary_tie_rows += 1
            band_of_value.setdefault(row["depth_value"], band)
    return {
        "group_sizes": group_margins,
        "groups_banded": sum(1 for v in group_margins.values()
                             if v >= DEPTH_MIN_GROUP),
        "rows_in_small_groups_unbanded": sum(
            v for v in group_margins.values()
            if v < DEPTH_MIN_GROUP),
        "boundary_tie_rows": boundary_tie_rows,
        "min_group_size_for_banding": DEPTH_MIN_GROUP,
    }


# ---------------------------------------------------------------------------
# Gate (frozen) — pure; unit-tested
# ---------------------------------------------------------------------------

def apply_gate(recorded: int, population: int,
               sites_with_min_recorded: int,
               permutable: int) -> dict:
    coverage = (recorded / population) if population else 0.0
    arms = {
        "i_recorded_coverage_ge_0.70": coverage >= GATE_MIN_COVERAGE,
        "ii_sites_with_ge30_recorded_ge_3":
            sites_with_min_recorded >= GATE_MIN_SITES,
        "iii_permutable_ge_1000": permutable >= GATE_MIN_PERMUTABLE,
    }
    return {
        "recorded": recorded,
        "population": population,
        "recorded_coverage": coverage,
        "sites_with_ge30_recorded": sites_with_min_recorded,
        "permutable_inscriptions": permutable,
        "arms": arms,
        "passes": all(arms.values()),
    }


def permutable_count(rows, level_of):
    """rows: population rows; level_of(row) -> covariate level.
    Strata = composition x level (UNRECORDED is a level). A row
    is permutable iff its stratum contains >= 2 distinct sites.
    Returns (all_rows_permutable, recorded_only_permutable)."""
    strata_sites: dict[str, set] = defaultdict(set)
    for row in rows:
        strata_sites[row["_stratum_key"]].add(row["site"])
    total = 0
    recorded_total = 0
    for row in rows:
        if len(strata_sites[row["_stratum_key"]]) >= 2:
            total += 1
            if level_of(row) != UNRECORDED:
                recorded_total += 1
    return total, recorded_total


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def informative(raw: str) -> bool:
    return (raw or "").strip() not in MISSING_SENTINELS


def build(layer_path: Path) -> tuple[dict, list[dict], dict]:
    anchors_digest = sha256_of(ANCHORS)
    assert anchors_digest == ANCHORS_SHA256, (
        f"anchors changed: {anchors_digest} != {ANCHORS_SHA256}")
    layer_digest = sha256_of(layer_path)
    assert layer_digest == LAYER_SHA256, (
        f"layer file changed: {layer_digest} != {LAYER_SHA256}")

    with open(layer_path, encoding="utf-8", newline="") as fh:
        raw_rows = list(csv.DictReader(fh))
    assert len(raw_rows) == 5679, f"layer rows {len(raw_rows)} != 5679"
    ids = [r["id"] for r in raw_rows]
    assert len(set(ids)) == len(ids), "layer id column not unique"

    rows = []
    for r in raw_rows:
        text = r["text"] or ""
        n_parsed = len(re.findall(r"\d{3}", text))
        rows.append({
            "id": r["id"],
            "site": (r["site"] or "").strip(),
            "type": (r["type"] or "").strip(),
            "period_raw": (r["period"] or "").strip(),
            "phase_raw": (r["phase"] or "").strip(),
            "depth_raw": (r["depth"] or "").strip(),
            "preservation_raw": (r["preservation"] or "").strip(),
            "n_parsed_tokens": n_parsed,
        })

    # --- Phase-137 F3 population reproduction -------------------
    per_site_insc: Counter = Counter()
    per_site_tokens: Counter = Counter()
    for row in rows:
        per_site_insc[row["site"]] += 1
        per_site_tokens[row["site"]] += row["n_parsed_tokens"]
    eligible_sites = sorted(
        s for s in per_site_insc
        if site_eligible(per_site_insc[s], per_site_tokens[s]))
    pop = [r for r in rows
           if r["site"] in set(eligible_sites)
           and r["n_parsed_tokens"] >= 1]
    assert len(pop) == 5410, f"F3 population {len(pop)} != 5410"
    for row in pop:
        row["composition_stratum"] = composition_stratum(
            row["type"], row["n_parsed_tokens"])

    # --- Spec sec.3 reproduction (T1) ----------------------------
    def fill_table(subset):
        n = len(subset)
        per = sum(1 for r in subset if informative(r["period_raw"]))
        pha = sum(1 for r in subset if informative(r["phase_raw"]))
        both = sum(1 for r in subset
                   if informative(r["period_raw"])
                   and informative(r["phase_raw"]))
        dep = sum(1 for r in subset
                  if parse_depth(r["depth_raw"])[0]
                  not in ("MISSING", "UNPARSED"))
        pres = sum(1 for r in subset
                   if informative(r["preservation_raw"]))
        allt = sum(1 for r in subset
                   if informative(r["period_raw"])
                   and informative(r["phase_raw"])
                   and parse_depth(r["depth_raw"])[0]
                   not in ("MISSING", "UNPARSED"))
        return {
            "n": n,
            "period_informative": per,
            "phase_informative": pha,
            "period_and_phase": both,
            "chron_union": per + pha - both,
            "all_three": allt,
            "depth_parseable": dep,
            "preservation_informative": pres,
        }

    sec3_full = fill_table(rows)
    sec3_pop = fill_table(pop)
    spec_sec3 = {  # values printed in spec.md sec.3 (percent)
        "full_layer": {"period": 40.8, "phase": 46.7,
                       "depth": 48.1, "preservation": 99.8},
        "f3_population": {"period": 41.9, "phase": 48.8,
                          "period_and_phase": 33.0,
                          "chron_union": 57.7, "all_three": 16.8,
                          "depth": 49.9, "preservation": 99.9},
    }

    def pct(x, n):
        return round(100.0 * x / n, 1) if n else 0.0

    reproduction = {
        "full_layer": {
            **sec3_full,
            "period_pct": pct(sec3_full["period_informative"], 5679),
            "phase_pct": pct(sec3_full["phase_informative"], 5679),
            "depth_pct": pct(sec3_full["depth_parseable"], 5679),
            "preservation_pct": pct(
                sec3_full["preservation_informative"], 5679),
        },
        "f3_population": {
            **sec3_pop,
            "period_pct": pct(sec3_pop["period_informative"], 5410),
            "phase_pct": pct(sec3_pop["phase_informative"], 5410),
            "period_and_phase_pct": pct(
                sec3_pop["period_and_phase"], 5410),
            "chron_union_pct": pct(sec3_pop["chron_union"], 5410),
            "all_three_pct": pct(sec3_pop["all_three"], 5410),
            "depth_pct": pct(sec3_pop["depth_parseable"], 5410),
            "preservation_pct": pct(
                sec3_pop["preservation_informative"], 5410),
        },
    }
    # Count-based fields (period / phase / both / preservation)
    # reproduce the draft's sec.3 counts EXACTLY. Three printed
    # percentages carry documented deltas (see "deltas"); none
    # affects any sec.3 substantive claim or the gate.
    reproduction["count_fields_match_spec_sec3"] = (
        reproduction["full_layer"]["period_informative"] == 2318
        and reproduction["full_layer"]["phase_informative"] == 2652
        and reproduction["full_layer"]["preservation_informative"]
        == 5670
        and reproduction["f3_population"]["period_informative"]
        == 2266
        and reproduction["f3_population"]["phase_informative"]
        == 2638
        and reproduction["f3_population"]["period_and_phase"]
        == 1788
        and reproduction["f3_population"][
            "preservation_informative"] == 5404)
    reproduction["deltas"] = [
        ("chron_union_pct: draft prints 57.7%; the exact union "
         "count is 3,116 = 57.6%. The draft figure is the sum "
         "of rounded percentages (41.9 + 48.8 - 33.0 = 57.7). "
         "Counts agree exactly; no substantive delta."),
        ("depth_pct: draft prints 48.1% (full) / 49.9% (F3 "
         "population). This audit's documented parse "
         "(VALUE/RANGE/DECIMAL_DOTDOT/SURFACE/UNITLESS) gives "
         "49.5% / 51.2%; a digit+unit-only rule gives 48.2% / "
         "50.0%. The draft's exact rule was not recoverable; "
         "the bracket is [draft, this audit] and the depth "
         "gate classification (SENSITIVITY) is identical "
         "under every definition in the bracket."),
        ("all_three_pct: draft prints 16.8%; this audit "
         "computes 16.9% — a knock-on of the depth definition "
         "above."),
    ]
    reproduction["matches_spec_sec3"] = (
        reproduction["count_fields_match_spec_sec3"])

    # --- Harmonization -------------------------------------------
    conflicts = 0
    for row in pop:
        band, source, cite, conflict = harmonize_chron(
            row["site"], row["period_raw"], row["phase_raw"])
        row["chron_band"] = band
        row["chron_source_field"] = source
        row["chron_citation"] = cite
        if conflict:
            conflicts += 1
        row["preservation_class"] = collapse_preservation(
            row["preservation_raw"])
        category, value, unit = parse_depth(row["depth_raw"])
        row["depth_category"] = category
        row["depth_value"] = value
        row["depth_unit"] = unit
    depth_margins = assign_depth_bands(pop)
    for row in pop:
        if row["depth_band"] != UNRECORDED:
            row["depth_recorded"] = True
        else:
            row["depth_recorded"] = False

    # --- Margins --------------------------------------------------
    def margins_for(level_of, levels):
        per_site = {}
        for site in eligible_sites:
            sub = [r for r in pop if r["site"] == site]
            counts = Counter(level_of(r) for r in sub)
            per_site[site] = {
                "n": len(sub),
                "levels": {lv: counts.get(lv, 0) for lv in levels},
                "recorded": sum(counts.get(lv, 0) for lv in levels
                                if lv != UNRECORDED),
            }
        totals = Counter(level_of(r) for r in pop)
        return {
            "levels": {lv: totals.get(lv, 0) for lv in levels},
            "recorded_total": sum(totals.get(lv, 0)
                                  for lv in levels
                                  if lv != UNRECORDED),
            "per_site": per_site,
        }

    chron_margins = margins_for(
        lambda r: r["chron_band"],
        ["early", "middle", "late", UNRECORDED])
    depth_margins_out = margins_for(
        lambda r: r["depth_band"],
        ["shallow", "middle", "deep", UNRECORDED])
    preservation_margins = margins_for(
        lambda r: r["preservation_class"],
        ["complete", "fragment", "damaged", UNRECORDED])
    raw_period_margins = margins_for(
        lambda r: r["period_raw"] if informative(r["period_raw"])
        else UNRECORDED,
        sorted({r["period_raw"] for r in pop
                if informative(r["period_raw"])}) + [UNRECORDED])
    raw_phase_margins = margins_for(
        lambda r: r["phase_raw"] if informative(r["phase_raw"])
        else UNRECORDED,
        sorted({r["phase_raw"] for r in pop
                if informative(r["phase_raw"])}) + [UNRECORDED])
    depth_categories = Counter(r["depth_category"] for r in pop)
    depth_examples = {}
    for r in pop:
        depth_examples.setdefault(r["depth_category"],
                                  r["depth_raw"])

    # --- Gate application (T2) --------------------------------------
    def gate_for(level_of):
        recorded = sum(1 for r in pop if level_of(r) != UNRECORDED)
        sites_ge30 = sum(
            1 for site in eligible_sites
            if sum(1 for r in pop
                   if r["site"] == site
                   and level_of(r) != UNRECORDED)
            >= GATE_MIN_SITE_RECORDED)
        for r in pop:
            r["_stratum_key"] = (
                f"{r['composition_stratum']}|{level_of(r)}")
        perm_all, perm_rec = permutable_count(pop, level_of)
        gate = apply_gate(recorded, len(pop), sites_ge30, perm_all)
        gate["permutable_recorded_only"] = perm_rec
        return gate

    gates = {
        "chron_band": gate_for(lambda r: r["chron_band"]),
        "depth_band": gate_for(lambda r: r["depth_band"]),
        "preservation": gate_for(lambda r: r["preservation_class"]),
    }
    for row in pop:
        row.pop("_stratum_key", None)

    classifications = {}
    for name, gate in gates.items():
        classifications[name] = (
            "PRIMARY CONTROL" if gate["passes"] else "SENSITIVITY")
    passers = [n for n, g in gates.items() if g["passes"]]

    if len(passers) == 1:
        primary_covariates = passers
        primary_strata = (f"composition (Phase-137 type class x "
                          f"length class) x {passers[0]}")
        verdict_word = "ESTIMABLE"
        verdict = (
            "G1 is ESTIMABLE under the sec.4.2 routing rule: "
            f"exactly one covariate ({passers[0]}) passes the "
            "frozen eligibility gate, so the primary strata "
            f"are {primary_strata}, with UNRECORDED retained "
            "as a stratum level. Gate-failing approved "
            "covariates route to the sensitivity panel "
            "(EXPLORATORY, reported as bounds, never as the "
            "controlled verdict). Chronology is NOT controlled "
            "in the primary test and must be named as an "
            "uncontrolled confounder in every G1 headline.")
    elif len(passers) > 1:
        primary_covariates = passers
        primary_strata = ("composition (Phase-137 type class x "
                          "length class) x "
                          + " x ".join(passers))
        verdict_word = "ESTIMABLE"
        verdict = (
            "G1 is ESTIMABLE: the covariates "
            + ", ".join(passers)
            + " pass the frozen eligibility gate and form the "
            "primary strata with composition, UNRECORDED "
            "retained as a stratum level. Gate-failing "
            "approved covariates route to the sensitivity "
            "panel (EXPLORATORY).")
    else:
        primary_covariates = []
        primary_strata = None
        verdict_word = "NOT ESTIMABLE"
        verdict = (
            "G1 is NOT ESTIMABLE as designed (sec.4.3 F-c): no "
            "approved covariate passes the frozen eligibility "
            "gate, so no primary strata can be formed. The "
            "routed sensitivity analyses may be reported as "
            "exploratory bounds only. This is a designed, "
            "publishable outcome of Spec 025, recorded with "
            "the same prominence as an executed test.")

    # --- Dataset rows (derived fields only; no inscription text) --
    dataset_rows = []
    for row in sorted(pop, key=lambda r: str(r["id"])):
        dataset_rows.append({
            "id": row["id"],
            "site": row["site"],
            "type_class": horus_type_class(row["type"]),
            "length_class": horus_length_class(
                row["n_parsed_tokens"]),
            "n_parsed_tokens": row["n_parsed_tokens"],
            "composition_stratum": row["composition_stratum"],
            "period_raw": row["period_raw"],
            "phase_raw": row["phase_raw"],
            "chron_band": row["chron_band"],
            "chron_source_field": row["chron_source_field"],
            "chron_citation": row["chron_citation"],
            "depth_raw": row["depth_raw"],
            "depth_parse_category": row["depth_category"],
            "depth_value": row["depth_value"],
            "depth_unit": row["depth_unit"],
            "depth_band": row["depth_band"],
            "preservation_raw": row["preservation_raw"],
            "preservation_class": row["preservation_class"],
        })

    register = {
        "phase": "Phase-139",
        "spec": "025",
        "register": ("chron_band citation register: every "
                     "mapped (site, field, value) cell with "
                     "its band and citation; unmapped cells "
                     "stay UNRECORDED for the recorded "
                     "reasons. Constructed context, Class C "
                     "(spec sec.8.5); no decipherment claim "
                     "rests on it."),
        "citations": CITATIONS,
        "mapped_cells": [
            {"site": s, "field": f, "value": v, "band": b,
             "citation": c}
            for (s, f, v), (b, c) in sorted(CHRON_MAP.items())],
        "unmapped_cells_with_reasons": [
            {"site": s, "field": f, "value": v, "reason": reason}
            for (s, f, v), reason in CHRON_UNMAPPED_REASONS],
        "unmapped_classes": [
            {"site": "Harappa", "field": "phase",
             "values": "Stratum I-VII",
             "reason": ("Vats-era stratum label; no correlation "
                        "to the HARP periodization was citable "
                        "from the published sources consulted.")},
            {"site": "Lothal", "field": "period",
             "values": "Layer 2-15",
             "reason": ("Excavation layer number; no published "
                        "layer-to-period correlation for Lothal "
                        "was citable from the sources "
                        "consulted.")},
            {"site": "Mohenjo-daro", "field": "phase",
             "values": "I, II, III, IA, IB",
             "reason": ("The layer's phase labels at "
                        "Mohenjo-daro carry no citable "
                        "published band assignment in the "
                        "consulted schemes. (No F3-population "
                        "row depends on them: every "
                        "phase-informative Mohenjo-daro row "
                        "also carries a period value.)")},
            {"site": "Kalibangan", "field": "phase",
             "values": "Early, Middle, Late",
             "reason": ("Not used: every phase-informative "
                        "Kalibangan row also carries a period "
                        "value, and period precedence governs; "
                        "no phase cell was needed.")},
            {"site": "Nausharo", "field": "phase",
             "values": "B, C",
             "reason": ("No citable published band assignment "
                        "for these labels at Nausharo in the "
                        "consulted schemes.")},
            {"site": "Dholavira", "field": "phase",
             "values": "F",
             "reason": ("Single opaque label; no citable "
                        "published band assignment.")},
            {"site": "Chanhu-daro", "field": "period/phase",
             "values": "(none informative)",
             "reason": ("The layer records no informative "
                        "period or phase value for "
                        "Chanhu-daro; all rows UNRECORDED.")},
        ],
        "singleton_cells": [
            {"site": "Mohenjo-daro", "field": "phase",
             "values": "II/III (1 row), III? (1 row)",
             "reason": ("Phase cells on rows whose period "
                        "cell (Late) maps; never consulted "
                        "under precedence. Mohenjo-daro phase "
                        "is unmapped as a class.")},
            {"site": "Lothal", "field": "period",
             "values": "II (1 row)",
             "reason": ("Not a period label in Rao's A/B "
                        "scheme; no citable cell.")},
            {"site": "Harappa", "field": "phase",
             "values": "Ravi (1 row)",
             "reason": ("Phase cell on a row whose period "
                        "cell (1) maps to early; never "
                        "consulted under precedence.")},
        ],
        "precedence": ("A mapped period cell wins over a "
                       "mapped phase cell; disagreements are "
                       "counted as conflicts (margins) and "
                       "the period band is used."),
        "ai_disclosure": AI_DISCLOSURE,
    }

    results = {
        "phase": "Phase-139",
        "spec": "025",
        "test": ("Covariate audit + harmonization (FROZEN "
                 "2026-10-10, spec.md sec.11 adjudication). "
                 "Margins only: no association statistic, no "
                 "repertoire comparison, no G1 computation."),
        "input": {
            "path": str(layer_path),
            "sha256": layer_digest,
            "rows": 5679,
            "layer_label": "ICIT-lineage layer (horus84)",
        },
        "anchors_sha256": anchors_digest,
        "population": {
            "definition": ("Phase-137 F3: eligible sites "
                           "(>= 30 inscriptions AND >= 100 "
                           "parsed tokens), rows with >= 1 "
                           "parsed token."),
            "eligible_sites": eligible_sites,
            "per_site_inscriptions": {
                s: per_site_insc[s] for s in eligible_sites},
            "inscriptions": len(pop),
            "parsed_tokens": sum(r["n_parsed_tokens"] for r in pop),
        },
        "spec_sec3_reproduction": reproduction,
        "raw_field_margins": {
            "period": raw_period_margins,
            "phase": raw_phase_margins,
        },
        "chron_band": {
            "class": "C (constructed context, sec.8.5)",
            "margins": chron_margins,
            "period_phase_band_conflicts": conflicts,
            "mapping_cells": len(CHRON_MAP),
        },
        "depth_band": {
            "margins": depth_margins_out,
            "parse_categories": dict(sorted(
                depth_categories.items())),
            "parse_examples": depth_examples,
            "banding": depth_margins,
        },
        "preservation": {
            "margins": preservation_margins,
            "collapse_rule": ("complete -> complete; fragment "
                              "-> fragment; chipped / slightly "
                              "chipped / partly damaged -> "
                              "damaged; '-' or blank -> "
                              "UNRECORDED. Original spellings "
                              "retained per row in the dataset."),
        },
        "gate": {
            "thresholds": {
                "min_recorded_coverage": GATE_MIN_COVERAGE,
                "min_sites_with_recorded": GATE_MIN_SITES,
                "min_recorded_per_site": GATE_MIN_SITE_RECORDED,
                "min_permutable": GATE_MIN_PERMUTABLE,
            },
            "per_covariate": gates,
            "classifications": classifications,
        },
        "verdict": {
            "word": verdict_word,
            "statement": verdict,
            "primary_control_set": primary_covariates,
            "primary_strata": primary_strata,
            "sensitivity_panel": [
                n for n, c in classifications.items()
                if c == "SENSITIVITY"],
        },
        "fence": ("No chi-square, odds ratio, permutation, or "
                  "any other association quantity was computed "
                  "in this phase; sign tokens were used only "
                  "to reproduce the Phase-137 population and "
                  "composition strata."),
        "publication_note": ("Per adjudication Q6 and the "
                             "executing instruction, "
                             "publication rides with the Spec "
                             "025 outcome record (G1 executed, "
                             "or the NOT ESTIMABLE closeout); "
                             "Phase-139 alone triggers no "
                             "release."),
        "ai_disclosure": AI_DISCLOSURE,
    }
    return results, dataset_rows, register


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--layer", type=Path, default=DEFAULT_HORUS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--register", type=Path,
                    default=DEFAULT_REGISTER)
    args = ap.parse_args(argv)
    if not args.layer.exists():
        print(f"ERROR: input not found: {args.layer}")
        return 2
    results, dataset_rows, register = build(args.layer)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n",
        "utf-8")
    args.dataset.parent.mkdir(parents=True, exist_ok=True)
    args.dataset.write_text(
        json.dumps(dataset_rows, indent=1, ensure_ascii=False)
        + "\n", "utf-8")
    meta = {
        "dataset": args.dataset.name,
        "phase": "Phase-139",
        "spec": "025",
        "rows": len(dataset_rows),
        "fields": list(dataset_rows[0].keys()) if dataset_rows
        else [],
        "provenance": ("Derived fields computed by "
                       "backend/scripts/"
                       "phase139_covariate_audit.py from the "
                       "ICIT-lineage layer (horus84 "
                       "inscriptions.csv, sha256 "
                       f"{LAYER_SHA256}); inscription texts "
                       "are NOT included. Context fields are "
                       "Class O; chron_band is constructed "
                       "context, Class C (citation register: "
                       "phase139_citation_register.json)."),
        "ai_disclosure": AI_DISCLOSURE,
    }
    args.dataset.with_name(
        args.dataset.stem + "_meta.json").write_text(
        json.dumps(meta, indent=1, ensure_ascii=False) + "\n",
        "utf-8")
    args.register.write_text(
        json.dumps(register, indent=1, ensure_ascii=False) + "\n",
        "utf-8")
    print(f"population: {results['population']['inscriptions']} "
          f"inscriptions, sites "
          f"{results['population']['eligible_sites']}")
    repro_ok = results["spec_sec3_reproduction"][
        "matches_spec_sec3"]
    print(f"sec.3 reproduction matches spec: {repro_ok}")
    for name, gate in results["gate"]["per_covariate"].items():
        print(f"{name}: recorded {gate['recorded']} "
              f"({gate['recorded_coverage']:.1%}), sites>=30: "
              f"{gate['sites_with_ge30_recorded']}, permutable "
              f"{gate['permutable_inscriptions']} -> "
              f"{results['gate']['classifications'][name]}")
    print(f"VERDICT: {results['verdict']['word']} — "
          f"primary controls: "
          f"{results['verdict']['primary_control_set']}")
    print(f"Wrote {args.out}, {args.dataset}, {args.register}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
