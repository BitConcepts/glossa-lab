"""Spec 027 Stage 1 — margins-only corpus audit (freeze input).

Computes population flow, strata margins, sign coverage, and
permutability projections for the Stage 1 (Phase-392) freeze.
NO repertoire outcome is computed: no site-by-sign association,
no divergence, no permutation statistic appears in the output.
A test pins the absence of outcome fields (the Phase-139
no-peeking fence pattern).

Inputs (hashes asserted):
  icit_converted_v2_keyed.json  (M77-keyed layer, Phase-115/116
      build; the program dedup artifact's output: status field)
  inscriptions.csv              (horus84 / ICIT-lineage layer,
      sha256 c368f290... as frozen in Spec 025)
  parpola_mahadevan_crosswalk_v1.csv (repo-tracked; M<->P pairs)
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import os
if os.environ.get("SPEC027_STAGE1_STORE"):
    HERE = Path(os.environ["SPEC027_STAGE1_STORE"])
else:
    HERE = (Path(__file__).resolve().parents[3]
            / "corpora" / "downloads" / "spec027_stage1")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def type_class(type_value: str) -> str:
    prefix = (type_value or "").split(":")[0]
    return prefix if prefix in ("SEAL", "TAB", "POT") else "OTHER"


def main() -> int:
    keyed_path = HERE / "icit_converted_v2_keyed.json"
    horus_path = HERE / "horus_inscriptions.csv"
    crosswalk_path = HERE / "parpola_mahadevan_crosswalk_v1.csv"
    if not crosswalk_path.is_file():
        crosswalk_path = (Path(__file__).resolve().parents[3]
                          / "data" / "crosswalks"
                          / "parpola_mahadevan_crosswalk_v1.csv")
    hashes = {p.name: sha256_file(p)
              for p in (keyed_path, horus_path, crosswalk_path)}
    assert hashes["horus_inscriptions.csv"].startswith("c368f290"), \
        hashes["horus_inscriptions.csv"]

    keyed = json.loads(keyed_path.read_text(encoding="utf-8"))
    records = keyed["inscriptions"]
    horus = {}
    with open(horus_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            horus[row["id"]] = row

    # Join integrity (margins).
    joined = 0
    site_agree = 0
    for rec in records:
        h = horus.get(rec["id"])
        if h is None:
            continue
        joined += 1
        if (h["site"] or "").strip() == rec["site"]:
            site_agree += 1

    # Population flow under the adjudicated Ask 3 rules.
    flow = Counter()
    eligible = []
    for rec in records:
        flow["layer_records"] += 1
        if rec["status"] != "kept":
            flow[f"excluded_status_{rec['status']}"] += 1
            continue
        flow["after_dedup_kept"] += 1
        if not (rec["site"] or "").strip():
            flow["excluded_no_site"] += 1
            continue
        if (rec["site"] or "").strip() == "Unknown":
            flow["excluded_site_unknown"] += 1
            continue
        flow["provenanced"] += 1
        h = horus.get(rec["id"]) or {}
        if not h:
            flow["unjoined_in_horus"] += 1
        tc = type_class(rec["type"])
        is_graffiti = rec["type"] == "POT:T:g"
        if is_graffiti:
            flow["excluded_graffiti_pottg"] += 1
        if tc not in ("SEAL", "TAB"):
            flow[f"excluded_type_{tc}"] += 1
            continue
        flow["seal_tab"] += 1
        kinds = rec["kinds"]
        n_legible = sum(1 for k in kinds
                        if k in ("direct", "chain", "unmapped"))
        n_placeholder = sum(1 for k in kinds if k == "placeholder")
        if n_legible < 2:
            flow["excluded_legible_lt2"] += 1
            continue
        flow["eligible_primary"] += 1
        eligible.append({
            "id": rec["id"], "site": rec["site"],
            "type_class": tc, "type": rec["type"],
            "tokens": rec["tokens"], "kinds": kinds,
            "n_legible": n_legible, "n_placeholder": n_placeholder,
            "complete": (h.get("complete") or "").strip(),
            "preservation": (h.get("preservation") or "").strip(),
            "period": (h.get("period") or "").strip(),
            "program_site_id": None,  # filled by caller if needed
        })

    # Per-site margins over the eligible population.
    per_site = {}
    site_insc = Counter(e["site"] for e in eligible)
    site_tokens = Counter()
    for e in eligible:
        site_tokens[e["site"]] += e["n_legible"]
    total_eligible = len(eligible)
    for site in sorted(site_insc):
        per_site[site] = {
            "inscriptions": site_insc[site],
            "legible_tokens": site_tokens[site],
            "share_of_eligible": round(
                site_insc[site] / total_eligible, 4),
        }
    dominant = sorted(per_site.items(),
                      key=lambda kv: -kv[1]["inscriptions"])[:5]

    # Strata grid (site x type_class) + permutability projections.
    grid = defaultdict(Counter)
    for e in eligible:
        grid[e["site"]][e["type_class"]] += 1
    projections = {}
    for min_site, min_cell in ((10, 5), (20, 5), (20, 10), (30, 10),
                               (50, 10)):
        sites_ok = []
        permutable = 0
        for site, cells in grid.items():
            n = sum(cells.values())
            if n < min_site:
                continue
            ok_cells = {t: c for t, c in cells.items() if c >= min_cell}
            if len(ok_cells) >= 2 or (len(cells) == 1 and ok_cells):
                # a site permutes within a type stratum when >=2
                # sites share that stratum cell; cell-level count
                # is refined below by stratum totals.
                sites_ok.append(site)
                permutable += sum(ok_cells.values())
        projections[f"min_site_{min_site}_min_cell_{min_cell}"] = {
            "sites_passing": len(sites_ok),
            "inscriptions_in_passing_cells": permutable,
        }
    # Stratum-level exchangeability: for each type_class, sites
    # with >= min_cell inscriptions can exchange labels.
    stratum_exchange = {}
    for tc in ("SEAL", "TAB"):
        counts = {s: grid[s][tc] for s in grid if grid[s][tc] > 0}
        stratum_exchange[tc] = {
            "sites_with_any": len(counts),
            "sites_ge5": sum(1 for v in counts.values() if v >= 5),
            "sites_ge10": sum(1 for v in counts.values() if v >= 10),
            "inscriptions": sum(counts.values()),
        }

    # Sign coverage margins.
    kind_counts = Counter()
    sign_counts = Counter()
    for e in eligible:
        for tok, kind in zip(e["tokens"], e["kinds"]):
            kind_counts[kind] += 1
            if kind in ("direct", "chain"):
                sign_counts[tok] += 1
    total_tokens = sum(kind_counts.values())

    # Crosswalk sensitivity feasibility (coverage margin only):
    # share of mapped tokens whose M sign has a high-confidence
    # P partner in crosswalk v1 — (a) any high-confidence pair;
    # (b) unambiguous: exactly one high-confidence P partner
    # and no conflict flag on the pair.
    m_to_p_high: dict[str, set] = defaultdict(set)
    m_conflict: set = set()
    with open(crosswalk_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            conf = (row.get("confidence") or "").strip().lower()
            if conf.startswith("high"):
                m_to_p_high[row["mahadevan_id"]].add(row["parpola_id"])
                if (row.get("conflict") or "").strip().lower() == "true":
                    m_conflict.add(row["mahadevan_id"])
    covered = sum(c for s, c in sign_counts.items()
                  if s in m_to_p_high)
    covered_unambig = sum(
        c for s, c in sign_counts.items()
        if len(m_to_p_high.get(s, ())) == 1 and s not in m_conflict)
    mapped_tokens = sum(sign_counts.values())

    out = {
        "audit": "spec027-stage1-margins-only",
        "outcome_fields_present": False,
        "input_hashes": hashes,
        "join": {"keyed_records": len(records), "joined": joined,
                 "site_agree": site_agree},
        "population_flow": dict(flow),
        "eligible_sites": len(per_site),
        "per_site": per_site,
        "dominant_sites": [
            {"site": s, **v} for s, v in dominant],
        "stratum_exchangeability": stratum_exchange,
        "permutability_projections": projections,
        "token_kinds_eligible": dict(kind_counts),
        "total_tokens_eligible": total_tokens,
        "distinct_m_signs_mapped": len(sign_counts),
        "signs_ge10_tokens": sum(1 for c in sign_counts.values()
                                 if c >= 10),
        "unmapped_share_of_tokens": round(
            kind_counts.get("unmapped", 0) / total_tokens, 4),
        "placeholder_share_of_tokens": round(
            kind_counts.get("placeholder", 0) / total_tokens, 4),
        "crosswalk_sensitivity_token_coverage": {
            "mapped_tokens": mapped_tokens,
            "covered_by_any_high_confidence_m_to_p": covered,
            "share_any": round(covered / mapped_tokens, 4)
            if mapped_tokens else None,
            "covered_by_unambiguous_high_confidence_m_to_p":
                covered_unambig,
            "share_unambiguous": round(covered_unambig / mapped_tokens, 4)
            if mapped_tokens else None,
        },
    }
    text = json.dumps(out, indent=1)
    print(text)
    out_path = os.environ.get("SPEC027_AUDIT_OUT")
    if out_path:
        Path(out_path).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
