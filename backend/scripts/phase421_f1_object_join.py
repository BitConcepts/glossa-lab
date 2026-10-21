#!/usr/bin/env python3
"""Phase-421 (spec 059, FROZEN) — the seal/tablet
difference on a better join: Spec 024 F1 rebuilt
through object identifiers (design D-22).

Executes the frozen Spec 059 contract (specs/
059-f1-object-join/freeze.md; freeze digest
bba1caca1885c2146515b437963619dff6737b4fc321a683f0dce9a56b5aed58;
OSF registration yfw7h, approved and public before
this run, DOI 10.17605/OSF.IO/YFW7H) in Wave 3
group 2 of the runnable-experiments campaign.

Step 0 runs first, in the frozen order (spec
section 3), and decides the execution before any
F1 quantity exists on the new join:

  0.1 Input integrity — every spec section 2
      input, and every object-identifier source
      named and pinned at freeze ruling DD-059-9,
      hashes to its freeze-record value; the
      Phase-130 schema validates the join dataset
      built at gate 0.3 (verdict pass, as Spec
      034's route (b) recorded for its dataset).
      A mismatch or a validation failure stops
      the run as INVALID.
  0.2 Original-join reproduction — the original
      concordance join is re-run on the pinned
      layer and catalogue under its frozen rule
      (exact string; a row joins iff its cisi
      value is a printed catalogue ID in exactly
      one volume) and must reproduce the recorded
      census exactly: 5,679 layer rows; 2,895
      matched; 2 ambiguous; 2,782 unmatched.
      A mismatch stops the run as INVALID.
  0.3 The object-identifier join census — the
      join is rebuilt through object identifiers
      only: each lineage row's published CISI
      object reference is carried as
      provenance.object_id under the Phase-130
      intake schema, exactly as the pinned Spec
      034 route-(b) construction (build_intake_
      dataset in backend/glossa_lab/
      phase398_matched_object.py) carried it, and
      resolves against the pinned catalogue
      layer's distinct objects (merged vols 1-2:
      an identifier resolving to exactly one
      distinct object joins; zero or more than
      one does not). String identity is never a
      join key (spec section 7.1; F059-C06): no
      name string, number string, cisi field
      string, or cisi_number string is matched as
      identity at any point — the identifiers
      enter only as cited provenance data in the
      schema's declared catalogue object ID
      field. The census unit is the layer row
      (DD-059-2).
  0.4 The gate comparison — freeze ruling
      DD-059-7 adopts the design's stated bar:
      joined share >= 61.0%, i.e. >= 3,465 of
      5,679 joined rows (0.61 x 5,679 = 3,464.19;
      3,464 rows = 60.997% and fails). The
      exact-points and relative readings are
      refused on the record and are not revived
      here. Below the bar the execution closes
      CLOSED AT STEP 0 — JOIN GATE NOT MET, in
      the spec section 3.5 wording, with the
      census published as the finding; no F1
      quantity is computed.

Only if gate 0.4 passes does section 4 run: the
frozen Phase-136 flow on the enlarged joined set,
unchanged in every particular (TERMINAL14; the
Cochran-Mantel-Haenszel statistic; the permutation
null with B = 9,999 and seed 20261009; the
Mantel-Haenszel common odds ratio with the
Robins-Breslow-Greenland interval), reusing the
pinned Phase-136 builder's own statistic
functions, with the single-test family correction
confirmed at DD-059-8 (adjusted q = raw p), the
section 5 verdict mapping with DD-059-3's
precedence confirmed at DD-059-12, the
leave-one-site-out rerun (descriptive; mints no
verdict), and both covariate comparisons.

Outputs (written on every terminal outcome):
  - reports/phase421_results.json (machine record)
  - reports/phase421_join_census.json (the
    per-row gate census: identifier provenance
    and resolution class for every layer row)
  - reports/phase421_report.md (the report)

Integrity: every pin is asserted before any join
quantity; the anchors file is asserted
byte-identical before and after. Deterministic:
no wall-clock values are written into the
outputs; a second run reproduces all three
output files byte-identically.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
HORUS84 = (Path.home() / "workspace" / "research_notes"
           / "indus-data-deep-sweep-20261008" / "downloads"
           / "horus84-computational-linguistics" / "data"
           / "inscriptions.csv")
KEYED_REL = (Path("corpora") / "downloads" / "icit_fieldcady"
             / "icit_converted_v2_keyed.json")
CATALOGUE_REL = (Path("corpora") / "downloads" / "cisi_image_layer"
                 / "catalogue")

FREEZE_DIGEST = "bba1caca1885c2146515b437963619dff6737b4fc321a683f0dce9a56b5aed58"
GATE_BAR_ROWS = 3465
GATE_BAR_SHARE = 0.61
LAYER_ROWS = 5679

# Committed pins (spec section 2 + DD-059-9):
# path -> (sha256, bytes)
COMMITTED_PINS = {
    "reports/phase136_results.json": (
        "11a0741317f50d9b8c2791fbfdd42ebec0f2a250d6f76809a2dec29fef857022",
        12992),
    "specs/024-evidence-integration/stage2a-freeze.md": (
        "c65a4b9ba7820f8dcf65fccfe64b8c271e488b036a754c76c45cd19f7cb4b94c",
        13150),
    "backend/scripts/phase136_terminal_type.py": (
        "d5ceec463bd271cd900fd2e5dbe2efb5b9e5f2b36444942b1d6cab12a6ee8871",
        22853),
    "reports/phase141_report.md": (
        "d442f8d2bcd1e7500c6df169f1dda0d8f48117c349e1710b34ff83011c7e4347",
        5453),
    "reports/phase136_137_138_stage2_report.md": (
        "6a4f5d2651ddc8316cf69d65ff6f4d29a7138ddc528c68310e6f07047eaed062",
        13823),
    "data/crosswalks/canonical_sign_registry.csv": (
        "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
        111583),
    "specs/034-matched-object-attribution/outcome.md": (
        "c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175",
        8142),
    "specs/037-cisi31-concordance-spine/outcome.md": (
        "28e444f20e698b3533559aac3a4bc3efcbc50440e79427ae58f656642886a02a",
        16077),
    "backend/reports/INDUS_FINAL_ANCHORS.json": (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
        570344),
    "data/intake/intake_dataset_schema_v1.json": (
        "b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b",
        6197),
    "backend/glossa_lab/phase398_matched_object.py": (
        "278f16b0ae8b02b77412cc925ac9e767110f5d5461729b73e8c122a9ff7673f0",
        40104),
    "backend/glossa_lab/intake.py": (
        "02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03",
        18867),
}

# Local-store pins (spec section 2 + DD-059-9):
# key -> (sha256, bytes)
LOCAL_PINS = {
    "horus84_inscriptions": (
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
        1190884),
    "cisi_vol1_catalogue": (
        "e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e",
        804665),
    "cisi_vol2_catalogue": (
        "e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9",
        1431631),
    "icit_converted_v2_keyed": (
        "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
        1586137),
}

RESULTS_OUT = REPO / "reports" / "phase421_results.json"
CENSUS_OUT = REPO / "reports" / "phase421_join_census.json"
REPORT_OUT = REPO / "reports" / "phase421_report.md"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_local(rel: Path) -> Path:
    for cand in (REPO / rel, MAIN_CHECKOUT / rel):
        if cand.exists():
            return cand
    raise FileNotFoundError(f"local corpus file not found: {rel}")


def catalogue_dir() -> Path:
    for cand in (REPO / CATALOGUE_REL, MAIN_CHECKOUT / CATALOGUE_REL):
        if (cand / "cisi_vol1_catalogue.csv").exists():
            return cand
    raise FileNotFoundError("cisi catalogue not found")


def check_pin(path: Path, pin: tuple[str, int]) -> dict:
    want_sha, want_bytes = pin
    got_sha = sha256_of(path) if path.exists() else None
    got_bytes = path.stat().st_size if path.exists() else None
    return {"path": str(path), "sha256": got_sha, "bytes": got_bytes,
            "pin_sha256": want_sha, "pin_bytes": want_bytes,
            "match": got_sha == want_sha and got_bytes == want_bytes}


# ---------------------------------------------------------------------------
# Step 0
# ---------------------------------------------------------------------------

def load_catalogue_rows() -> tuple[dict, dict, dict]:
    """Returns (per-volume printed-ID sets [gate 0.2, raw
    values exactly as Phase-136 read them], merged
    distinct-object view [gate 0.3, per the pinned
    Phase-398 load_catalogue keying: cisi_id stripped],
    per-volume row/distinct counts)."""
    cat_dir = catalogue_dir()
    vol_ids: dict[int, set] = {}
    merged: dict[str, dict] = {}
    counts: dict[str, dict] = {}
    for vol in (1, 2):
        path = cat_dir / f"cisi_vol{vol}_catalogue.csv"
        with path.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        vol_ids[vol] = {r["cisi_id"] for r in rows}
        counts[f"vol{vol}"] = {
            "rows": len(rows),
            "distinct_ids": len({(r["cisi_id"] or "").strip()
                                 for r in rows if (r["cisi_id"] or "").strip()}),
        }
        for r in rows:
            cid = (r.get("cisi_id") or "").strip()
            if not cid:
                continue
            obj = merged.setdefault(cid, {
                "n_rows": 0, "volumes": set(), "sites": set(),
                "object_types": set(), "site_first": "",
                "object_type_first": ""})
            obj["n_rows"] += 1
            obj["volumes"].add(vol)
            site = (r.get("site") or "").strip()
            otype = (r.get("object_type") or "").strip()
            if site:
                obj["sites"].add(site)
                if not obj["site_first"]:
                    obj["site_first"] = site
            if otype:
                obj["object_types"].add(otype)
                if not obj["object_type_first"]:
                    obj["object_type_first"] = otype
    return vol_ids, merged, counts


def load_horus_rows() -> list[dict]:
    with HORUS84.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build() -> tuple[dict, list[dict] | None]:
    result: dict = {
        "phase": "Phase-421",
        "spec": "059",
        "title": ("The seal/tablet difference on a better join — "
                  "Spec 024 F1 rebuilt through object identifiers "
                  "(design D-22)"),
        "lineage_label": "ICIT-lineage (horus84)",
        "lineage_sentence": ("results describe this lineage layer, "
                             "and (gate-passed) its object-ID-joined "
                             "subset, not the Indus corpus in general."),
        "claim_under_test": "STUDY-SPEC-024/F1",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": "https://osf.io/yfw7h/",
        "osf_doi": "10.17605/OSF.IO/YFW7H",
        "execution_date": "2026-10-21",
        "gate_bar": {"ruling": "DD-059-7",
                     "joined_share_min": GATE_BAR_SHARE,
                     "joined_rows_min": GATE_BAR_ROWS,
                     "arithmetic": ("0.61 x 5,679 = 3,464.19, so "
                                    ">= 61.0% is >= 3,465 rows; 3,464 "
                                    "rows = 60.997% and fails"),
                     "baseline": "2,895 / 5,679 = 50.977% (51.0%)"},
        "gates": {},
        "outcome": None,
        "ai_disclosure": ("Produced by an AI agent (Muse Spark, "
                          "via Muse) at the direction of Tristen "
                          "Pierson, per constitution section VI."),
    }
    census_rows: list[dict] | None = None

    anchors_before = sha256_of(
        REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")

    # ── Gate 0.1: input integrity (hashes) ─────────────────────────
    pin_checks: dict[str, dict] = {}
    for rel, pin in COMMITTED_PINS.items():
        pin_checks[rel] = check_pin(REPO / rel, pin)
    local_paths = {
        "horus84_inscriptions": HORUS84,
        "cisi_vol1_catalogue": catalogue_dir() / "cisi_vol1_catalogue.csv",
        "cisi_vol2_catalogue": catalogue_dir() / "cisi_vol2_catalogue.csv",
        "icit_converted_v2_keyed": find_local(KEYED_REL),
    }
    for key, pin in LOCAL_PINS.items():
        pin_checks[key] = check_pin(local_paths[key], pin)
    hashes_ok = all(c["match"] for c in pin_checks.values())
    result["inputs"] = pin_checks
    result["gates"]["0.1_input_integrity"] = {
        "status": "PASS" if hashes_ok else "FAIL",
        "detail": ("every spec section 2 pin and every DD-059-9 "
                   "object-identifier source pin recomputes to its "
                   "freeze-record value"
                   if hashes_ok else
                   "at least one pin mismatches; see inputs"),
        "schema_validation": "recorded at gate 0.3 (the dataset is "
                             "built there); a validation failure "
                             "closes the run INVALID under section 3.1",
    }
    if not hashes_ok:
        result["outcome"] = {
            "class": "INVALID",
            "wording": ("INVALID — gate 0.1 failed: an input pin "
                        "mismatches its freeze-record value. No "
                        "join was built and no F1 quantity was "
                        "computed."),
        }
        result["anchors_byte_identical"] = (
            sha256_of(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
            == anchors_before)
        return result, census_rows

    horus_rows = load_horus_rows()
    vol_ids, merged, cat_counts = load_catalogue_rows()

    # ── Gate 0.2: original-join reproduction (exact string) ──────
    matched = ambiguous = unmatched = 0
    original_joined_idx: set[int] = set()
    for i, r in enumerate(horus_rows):
        value = r["cisi"]
        in1, in2 = value in vol_ids[1], value in vol_ids[2]
        if in1 and in2:
            ambiguous += 1
        elif in1 or in2:
            matched += 1
            original_joined_idx.add(i)
        else:
            unmatched += 1
    reproduced = (len(horus_rows) == 5679 and matched == 2895
                  and ambiguous == 2 and unmatched == 2782)
    result["gates"]["0.2_original_join_reproduction"] = {
        "status": "PASS" if reproduced else "FAIL",
        "observed": {"layer_rows": len(horus_rows), "matched": matched,
                     "ambiguous": ambiguous, "unmatched": unmatched},
        "recorded": {"layer_rows": 5679, "matched": 2895,
                     "ambiguous": 2, "unmatched": 2782},
    }
    if not reproduced:
        result["outcome"] = {
            "class": "INVALID",
            "wording": ("INVALID — gate 0.2 failed: the original "
                        "concordance join does not reproduce the "
                        "recorded census exactly. The gate's "
                        "baseline is not established; no new join "
                        "was built and no F1 quantity was computed."),
        }
        result["anchors_byte_identical"] = (
            sha256_of(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
            == anchors_before)
        return result, census_rows

    # ── Gate 0.3: the object-identifier join census ──────────────
    # The join dataset is built by the PINNED route-(b)
    # construction itself (its hash was asserted at gate 0.1),
    # from the pinned converted keyed layer — the same source
    # in converted form (DD-059-9) — and validated under the
    # pinned Phase-130 schema by the pinned validator.
    from glossa_lab.intake import validate_dataset  # noqa: E402
    from glossa_lab.phase398_matched_object import (  # noqa: E402
        build_intake_dataset, load_icit_layer)

    icit = load_icit_layer(local_paths["icit_converted_v2_keyed"])
    dataset = build_intake_dataset(icit)
    validation = validate_dataset(dataset)
    result["gates"]["0.3_object_id_join_census"] = {
        "intake_dataset": {
            "name": dataset["dataset_name"],
            "records": len(dataset["inscriptions"]),
            "construction": ("backend/glossa_lab/"
                             "phase398_matched_object.py "
                             "build_intake_dataset (pinned, "
                             "DD-059-9)"),
            "validation_verdict": validation["verdict"],
            "validation_summary": validation["summary"],
        },
    }
    if validation["verdict"] != "pass":
        result["gates"]["0.3_object_id_join_census"]["status"] = "FAIL"
        result["outcome"] = {
            "class": "INVALID",
            "wording": ("INVALID — the Phase-130 schema validation "
                        "of the join dataset did not return pass "
                        "(spec section 3.1). No gate comparison "
                        "was made and no F1 quantity was computed."),
        }
        result["anchors_byte_identical"] = (
            sha256_of(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
            == anchors_before)
        return result, census_rows

    # Row alignment between the lineage layer and the converted
    # form is by layer-row order; inscription ids and sites are
    # asserted equal on every row before any census count.
    keyed = icit["inscriptions"]
    assert len(keyed) == len(horus_rows) == LAYER_ROWS
    for h, k in zip(horus_rows, keyed):
        assert (h["id"] or "").strip() == (k["id"] or "").strip(), (
            h["id"], k["id"])
        assert h["site"] == k["site"], (h["id"], h["site"], k["site"])

    by_row: dict[int, str] = {}
    for ins in dataset["inscriptions"]:
        by_row[ins["source_row"]] = ins["provenance"]["object_id"]

    # Per-row census, with the horus-direct route as an
    # independent cross-check of every row's resolution class:
    # the lineage layer's own cisi field, carried with the same
    # strip the route-(b) construction applies, must classify
    # every row identically.
    census_rows = []
    discrepancies = []
    for i, (h, k) in enumerate(zip(horus_rows, keyed)):
        oid = by_row.get(i)
        carried = oid is not None
        n_resolved = 0
        if carried:
            n_resolved = 1 if oid in merged else 0
        if n_resolved == 1:
            rclass = "exactly-one"
        elif carried:
            rclass = "zero"
        else:
            rclass = "zero"
        # Cross-check route (lineage layer directly).
        raw_h = h["cisi"] or ""
        stripped_h = raw_h.strip()
        h_oid = stripped_h if stripped_h and stripped_h != "-" else None
        h_resolved = (1 if h_oid in merged else 0) if h_oid else 0
        assert (h_resolved == 1) == (n_resolved == 1), (
            i, h["id"], raw_h, oid)
        # Identifier presence may differ between the two routes
        # on a row whose identifier resolves zero either way;
        # the joined classification — the census's quantity —
        # may not, and is asserted above.
        if raw_h != (k.get("cisi") or "") or (
                h["id"] or "") != (k["id"] or ""):
            discrepancies.append({
                "layer_row": i,
                "inscription_id": (h["id"] or "").strip(),
                "lineage_layer_id_raw": h["id"],
                "converted_form_id": k["id"],
                "lineage_layer_cisi_raw": raw_h,
                "converted_form_cisi": k.get("cisi"),
                "dataset_object_id": oid,
                "resolution_class": rclass,
                "joined": n_resolved == 1,
            })
        obj = merged.get(oid) if n_resolved == 1 else None
        census_rows.append({
            "layer_row": i,
            "inscription_id": (h["id"] or "").strip(),
            "site": h["site"],
            "identifier_carried": carried,
            "provenance_object_id": oid,
            "resolution_class": rclass,
            "joined": n_resolved == 1,
            "catalogue_object_id": oid if n_resolved == 1 else None,
            "catalogue_object_type": (
                obj["object_type_first"] if obj else None),
            "catalogue_volumes": (
                sorted(obj["volumes"]) if obj else None),
        })

    joined_rows = [c for c in census_rows if c["joined"]]
    unjoined_rows = [c for c in census_rows if not c["joined"]]
    ambiguous_rows = [c for c in census_rows
                      if c["resolution_class"] == "more-than-one"]
    joined_share = len(joined_rows) / LAYER_ROWS
    census = {
        "unit": "layer row (DD-059-2)",
        "layer_rows": LAYER_ROWS,
        "dataset_records_carrying_identifier": len(by_row),
        "rows_without_identifier": LAYER_ROWS - len(by_row),
        "joined_rows": len(joined_rows),
        "joined_share": joined_share,
        "joined_share_percent": round(joined_share * 100, 4),
        "unjoined_rows": len(unjoined_rows),
        "unjoined_with_identifier_resolving_zero": sum(
            1 for c in unjoined_rows if c["identifier_carried"]),
        "ambiguous_rows_more_than_one_object": len(ambiguous_rows),
        "distinct_catalogue_objects_joined_to": len(
            {c["catalogue_object_id"] for c in joined_rows}),
        "catalogue_layer": {
            "rows_total": sum(v["rows"] for v in cat_counts.values()),
            "per_volume": cat_counts,
            "distinct_objects_merged": len(merged),
            "ids_in_both_volumes": sorted(
                set(vol_ids[1]) & set(vol_ids[2])),
        },
        "joined_site_mix_lineage": dict(sorted(Counter(
            c["site"] for c in joined_rows).items())),
        "joined_object_type_mix": dict(sorted(Counter(
            c["catalogue_object_type"] or "(unfilled)"
            for c in joined_rows).items())),
        "by_site": [
            {"site": site,
             "layer_rows": sum(1 for c in census_rows
                               if c["site"] == site),
             "joined_rows": sum(1 for c in joined_rows
                                if c["site"] == site)}
            for site in sorted({c["site"] for c in census_rows})
        ],
        "added_rows_vs_original_join": [
            {"layer_row": c["layer_row"],
             "inscription_id": c["inscription_id"],
             "site": c["site"],
             "provenance_object_id": c["provenance_object_id"],
             "catalogue_object_type": c["catalogue_object_type"]}
            for c in joined_rows
            if c["layer_row"] not in original_joined_idx
        ],
        "original_joined_rows_lost": sum(
            1 for i in original_joined_idx
            if not census_rows[i]["joined"]),
        "raw_value_discrepancies_lineage_vs_converted": discrepancies,
        "cross_check": ("the census was derived twice: through "
                        "the pinned route-(b) intake dataset and "
                        "directly from the lineage layer's own "
                        "cisi field (same strip the construction "
                        "applies); every row's joined classification "
                        "agrees between the two routes"),
        "more_than_one_note": ("resolution is against distinct "
                               "catalogue objects in the merged "
                               "layer (DD-059-9): an identifier is "
                               "a distinct object's own ID, so the "
                               "more-than-one class is structurally "
                               "empty on this layer; it is counted "
                               "and reported as observed (0)"),
    }
    result["gates"]["0.3_object_id_join_census"]["status"] = "PASS"
    result["gates"]["0.3_object_id_join_census"]["census"] = census
    result["census"] = census

    # ── Gate 0.4: the gate comparison ─────────────────────────────
    gate_pass = len(joined_rows) >= GATE_BAR_ROWS
    result["gates"]["0.4_gate_comparison"] = {
        "status": "PASS" if gate_pass else "FAIL",
        "joined_rows": len(joined_rows),
        "joined_share_percent": round(joined_share * 100, 4),
        "bar_rows": GATE_BAR_ROWS, "bar_share_percent": 61.0,
        "shortfall_rows": max(0, GATE_BAR_ROWS - len(joined_rows)),
    }
    if not gate_pass:
        result["outcome"] = {
            "class": "CLOSED AT STEP 0 - JOIN GATE NOT MET",
            "wording": (
                "CLOSED AT STEP 0 — JOIN GATE NOT MET. The "
                "object-identifier join joined "
                f"{len(joined_rows)} of 5,679 lineage rows "
                f"({joined_share * 100:.2f}%), against the "
                "original concordance join's 51.0% and the gate "
                "fixed in advance at 61.0% or more. The enlarged "
                "joined set this design required does not exist "
                "on the available catalogue data, so no F1 "
                "quantity was computed and STUDY-SPEC-024/F1 "
                "stands exactly as recorded — SUPPORTED on its "
                "original joined subset, its 'on the joined "
                "subset' scope unchanged. The unjoined share is "
                "a measured property of the available catalogue "
                "data, not an oversight. The unblocking act is a "
                "more complete published object catalogue "
                "entering through Phase-130 intake."),
            "f1_quantity_computed": False,
        }
        result["anchors_byte_identical"] = (
            sha256_of(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
            == anchors_before)
        return result, census_rows

    # ── Section 4: the primary test (gate-passed only) ────────────
    result["primary_test"] = run_primary_test(
        horus_rows, census_rows, merged)
    result["outcome"] = result["primary_test"]["outcome"]
    result["anchors_byte_identical"] = (
        sha256_of(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
        == anchors_before)
    return result, census_rows


# ---------------------------------------------------------------------------
# Section 4 — the frozen Phase-136 flow on the enlarged set.
# Reached only when gate 0.4 passes. Statistic functions are the
# pinned Phase-136 builder's own, imported from its pinned file
# (hash asserted at gate 0.1 before this import happens).
# ---------------------------------------------------------------------------

def _phase136_module():
    path = REPO / "backend/scripts/phase136_terminal_type.py"
    spec = importlib.util.spec_from_file_location("phase136_builder", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_primary_test(horus_rows, census_rows, merged) -> dict:
    p136 = _phase136_module()
    from glossa_lab.pred_harness import SignMapper, build_sign_maps

    joined = [(horus_rows[c["layer_row"]],
               merged[c["catalogue_object_id"]])
              for c in census_rows if c["joined"]]
    typed = Counter()
    untyped = 0
    for _r, obj in joined:
        if obj["object_type_first"]:
            typed[obj["object_type_first"]] += 1
        else:
            untyped += 1
    restricted = [(r, o) for r, o in joined
                  if o["object_type_first"] in ("Seals", "Tablets")]

    mapper = SignMapper(build_sign_maps(
        REPO / "data/crosswalks/canonical_sign_registry.csv"))
    mapped = unk_terminal = no_codes = 0
    analysis: list[tuple[str, str, bool]] = []
    placeholders = {"000", "999"}
    for r, o in restricted:
        codes = re.findall(r"\d{3}", r["text"] or "")
        if not codes:
            no_codes += 1
            continue
        terminal_code = codes[-1]
        if terminal_code in placeholders:
            p_sign = "UNK"
        else:
            p_sign = mapper.map_w(terminal_code, Counter())
        if p_sign == "UNK":
            unk_terminal += 1
            continue
        mapped += 1
        analysis.append((r["site"], o["object_type_first"],
                         p_sign in p136.TERMINAL14))

    def strata_and_tables(rows):
        by_site: dict[str, list] = defaultdict(list)
        for site, otype, is_term in rows:
            by_site[site].append((otype, is_term))
        strata, eligible = [], []
        for site in sorted(by_site, key=lambda s: (-len(by_site[s]), s)):
            srows = by_site[site]
            n_seals = sum(1 for t, _ in srows if t == "Seals")
            n_tablets = len(srows) - n_seals
            a = sum(1 for t, out in srows if t == "Seals" and out)
            c_ = sum(1 for t, out in srows if t == "Tablets" and out)
            table = p136.table_from_counts(n_seals, n_tablets, a, c_)
            _or = p136.odds_ratio(table["a"], table["b"],
                                  table["c"], table["d"])
            strata.append({
                "site": site, "n": len(srows), "n_seals": n_seals,
                "n_tablets": n_tablets,
                "eligible": (len(srows) >= 20 and n_seals >= 5
                             and n_tablets >= 5),
                "table": table,
                "odds_ratio": (_or if _or is not None
                               and math.isfinite(_or) else None),
                "terminal14_share_seals": (
                    a / n_seals if n_seals else None),
                "terminal14_share_tablets": (
                    c_ / n_tablets if n_tablets else None),
            })
            if strata[-1]["eligible"]:
                outcomes = ([out for t, out in srows if t == "Seals"]
                            + [out for t, out in srows
                               if t == "Tablets"])
                eligible.append({"site": site, "n_seals": n_seals,
                                 "outcomes": outcomes, "table": table})
        return strata, eligible

    def estimability(eligible):
        tables = [e["table"] for e in eligible]
        if not tables:
            return {"n_eligible_strata": 0,
                    "fraction_expected_ge_5": 0.0, "estimable": False,
                    "pooled_table": {"a": 0, "b": 0, "c": 0, "d": 0},
                    "pooled_expected_counts": []}
        pooled = {k: sum(t[k] for t in tables) for k in "abcd"}
        n = sum(pooled.values())
        rt = [pooled["a"] + pooled["b"], pooled["c"] + pooled["d"]]
        ct = [pooled["a"] + pooled["c"], pooled["b"] + pooled["d"]]
        expected = [rt[0] * ct[0] / n, rt[0] * ct[1] / n,
                    rt[1] * ct[0] / n, rt[1] * ct[1] / n]
        frac = sum(1 for e in expected if e >= 5) / 4
        return {"n_eligible_strata": len(eligible),
                "fraction_expected_ge_5": frac,
                "estimable": len(eligible) >= 2 and frac >= 0.8,
                "pooled_table": pooled,
                "pooled_expected_counts": expected}

    strata, eligible = strata_and_tables(analysis)
    est = estimability(eligible)
    out: dict = {
        "flow": {"joined_rows": len(joined),
                 "typed_filled": sum(typed.values()),
                 "typed_by_type": dict(sorted(typed.items())),
                 "untyped": untyped,
                 "restricted_seals_tablets": len(restricted),
                 "terminal_mapped": mapped,
                 "terminal_unk": unk_terminal,
                 "terminal_no_codes": no_codes,
                 "analysis_population_all_strata": len(analysis),
                 "analysis_population_eligible_strata": sum(
                     e["table"]["a"] + e["table"]["b"]
                     + e["table"]["c"] + e["table"]["d"]
                     for e in eligible)},
        "strata": strata,
        "eligible_strata": [e["site"] for e in eligible],
        "estimability": est,
    }
    n_joined = sum(1 for c in census_rows if c["joined"])
    share_pct = round(n_joined / LAYER_ROWS * 100, 2)
    if not est["estimable"]:
        failed = ("(i) fewer than 2 eligible strata"
                  if est["n_eligible_strata"] < 2 else
                  "(ii) pooled expected counts >= 5 in fewer "
                  "than 80% of cells")
        out["outcome"] = {
            "class": "NOT ESTIMABLE",
            "wording": (
                f"The object-ID join passed its gate ({n_joined} "
                f"of 5,679 rows, {share_pct}%), but the enlarged "
                f"set fails the frozen estimability rule ({failed}; "
                "cell counts shown in the record). No p-value was "
                "computed and no verdict under this spec exists. "
                "STUDY-SPEC-024/F1 stands exactly as recorded."),
            "f1_quantity_computed": False,
        }
        out["loso"] = {"note": "not run: the enlarged set is not "
                               "estimable, so no dropped-site rerun "
                               "exists"}
        out["covariates"] = covariate_comparisons(
            horus_rows, census_rows, merged)
        return out

    tables = [e["table"] for e in eligible]
    mh = p136.mh_odds_ratio(tables)
    obs = p136.cmh_statistic(tables)
    perm = p136.permutation_test(eligible)
    assert abs(perm["statistic_observed"] - obs) < 1e-9
    raw_p = perm["p_value"]
    q = raw_p  # single-test family (DD-059-8): BH over one p-value
    ci = mh["ci95"]
    if q >= 0.05 or (ci and ci[0] <= 1.0 <= ci[1]):
        verdict = "NOT REPLICATED"
    elif ci and ci[0] > 1.5:
        verdict = "REPLICATED"
    else:
        verdict = "WEAKENED"
    out["test"] = {
        "statistic": "Cochran-Mantel-Haenszel chi-square",
        "statistic_observed": obs, "B": perm["b"], "seed": perm["seed"],
        "n_perm_ge_observed": perm["n_perm_ge_observed"],
        "raw_p": raw_p, "adjusted_q_single_test_family": q,
        "correction": "DD-059-8: single-test family; q = raw p",
    }
    out["effect_sizes"] = {
        "mh_common_odds_ratio": mh["common_odds_ratio"],
        "mh_ci95": ci,
        "crude_odds_ratio_uncontrolled": p136.crude_odds_ratio(tables),
    }

    # LOSO (descriptive; mints no verdict).
    loso = []
    for dropped in [e["site"] for e in eligible]:
        sub = [row for row in analysis if row[0] != dropped]
        _s, sub_eligible = strata_and_tables(sub)
        sub_est = estimability(sub_eligible)
        entry = {"dropped_site": dropped,
                 "estimable": sub_est["estimable"]}
        if sub_est["estimable"]:
            sub_mh = p136.mh_odds_ratio(
                [e["table"] for e in sub_eligible])
            entry["mh_common_odds_ratio"] = sub_mh["common_odds_ratio"]
            entry["mh_ci95"] = sub_mh["ci95"]
        loso.append(entry)
    load_bearing = [e["dropped_site"] for e in loso
                    if not e["estimable"]
                    or (e.get("mh_ci95") and e["mh_ci95"][0] <= 1.0)]
    loso_sentence = (
        "Leave-one-site-out: every dropped-site subset remained "
        "estimable with its interval excluding 1; no site is "
        "load-bearing."
        if not load_bearing else
        "Leave-one-site-out: dropping "
        + ", ".join(load_bearing)
        + " leaves a subset that is not estimable or whose "
          "interval includes 1; those sites are load-bearing.")
    out["loso"] = {"runs": loso, "sentence": loso_sentence,
                   "note": "descriptive only; mints no verdict"}

    r = mh["common_odds_ratio"]
    lo, hi = ci
    if verdict == "REPLICATED":
        wording = (
            f"On the enlarged object-ID-joined set ({n_joined} of "
            f"5,679 lineage rows, {share_pct}%, against the "
            "original join's 51.0%), the seal/tablet difference "
            "in TERMINAL14 endings replicates within sites: "
            f"Mantel–Haenszel odds ratio {r:.3f}, 95% CI "
            f"[{lo:.3f}–{hi:.3f}], entirely above 1.5, "
            f"family-adjusted q = {q}. The original F1 result "
            "was not an artefact of which rows the concordance "
            f"join could reach, at this test's resolution. "
            f"{loso_sentence} This is a statement about recorded "
            "use in this lineage layer, not about what the "
            "difference means.")
    elif verdict == "WEAKENED":
        wording = (
            f"On the enlarged object-ID-joined set ({n_joined} of "
            f"5,679 rows, {share_pct}%), the seal/tablet "
            "difference in TERMINAL14 endings remains detectable "
            f"within sites (family-adjusted q = {q}) but smaller "
            "than the original estimate: Mantel–Haenszel odds "
            f"ratio {r:.3f}, 95% CI [{lo:.3f}–{hi:.3f}], reaching "
            "below 1.5 (original: 2.384 [1.847–3.077] on 51.0% "
            "joined). Part of the original result's size was a "
            f"property of which rows could be joined. "
            f"{loso_sentence}")
    else:
        reason = (f"family-adjusted q = {q} at or above 0.05"
                  if q >= 0.05 else
                  f"the odds-ratio interval [{lo:.3f}–{hi:.3f}] "
                  "includes 1.0")
        wording = (
            f"On the enlarged object-ID-joined set ({n_joined} of "
            f"5,679 rows, {share_pct}%), the seal/tablet "
            "difference in TERMINAL14 endings does not replicate "
            f"within sites: {reason}, point estimate {r:.3f} "
            "(original: 2.384 [1.847–3.077] on 51.0% joined). "
            "The design's falsifier has fired: the original "
            "result was partly an artefact of which rows could "
            "be joined. The original verdict stands as recorded "
            "on its subset; this outcome is appended as its "
            f"replication record. {loso_sentence}")
    out["outcome"] = {"class": verdict, "wording": wording,
                      "f1_quantity_computed": True}
    out["covariates"] = covariate_comparisons(
        horus_rows, census_rows, merged)
    return out


def covariate_comparisons(horus_rows, census_rows, merged) -> dict:
    """Spec section 4.5: joined vs unjoined, and original joined
    set vs added rows, on every covariate the data carries."""
    def describe(idxs):
        rows = [horus_rows[i] for i in idxs]
        lengths = []
        for r in rows:
            codes = re.findall(r"\d{3}", r["text"] or "")
            lengths.append(len(codes))
        return {
            "n": len(rows),
            "site_mix": dict(sorted(Counter(
                r["site"] for r in rows).items())),
            "text_length_codes_mean": (
                round(sum(lengths) / len(lengths), 4) if lengths
                else None),
            "text_length_codes_median": (
                sorted(lengths)[len(lengths) // 2] if lengths
                else None),
            "preservation_mix": dict(sorted(Counter(
                (r.get("preservation") or "(unfilled)")
                for r in rows).items())),
            "material_mix": dict(sorted(Counter(
                (r.get("material") or "(unfilled)")
                for r in rows).items())),
        }

    joined_idx = [c["layer_row"] for c in census_rows if c["joined"]]
    unjoined_idx = [c["layer_row"] for c in census_rows
                    if not c["joined"]]
    census = {c["layer_row"]: c for c in census_rows}
    added_idx = []
    vol_ids, _m, _c = load_catalogue_rows()
    for i in joined_idx:
        value = horus_rows[i]["cisi"]
        if not ((value in vol_ids[1]) != (value in vol_ids[2])):
            added_idx.append(i)
    original_idx = [i for i in joined_idx if i not in set(added_idx)]
    joined_desc = describe(joined_idx)
    joined_desc["object_type_mix"] = dict(sorted(Counter(
        census[i]["catalogue_object_type"] or "(unfilled)"
        for i in joined_idx).items()))
    unjoined_desc = describe(unjoined_idx)
    unjoined_desc["object_type_mix"] = (
        "not carried: unjoined rows have no catalogue object, so "
        "the catalogue carries no object type for them")
    return {
        "joined_vs_unjoined": {"joined": joined_desc,
                               "unjoined": unjoined_desc},
        "original_vs_added": {"original_joined": describe(original_idx),
                              "added_by_object_id_join": describe(
                                  added_idx)},
        "not_carried": ("object type for unjoined rows (no "
                        "catalogue object); any covariate absent "
                        "from the lineage layer's fields"),
    }


# ---------------------------------------------------------------------------
# Rendering + main
# ---------------------------------------------------------------------------

def render_report(result: dict) -> str:
    g = result["gates"]
    outcome = result["outcome"]
    lines = [
        "# Phase-421 — Spec 059 execution report",
        "",
        "Claim: `STUDY-SPEC-024/F1` — standing SETTLED — SUPPORTED on "
        "its original joined subset (odds ratio 2.384, interval "
        "[1.847, 3.077], family q = 0.00015), exactly as recorded. "
        "Execution date: 2026-10-21. Freeze digest: "
        f"`{FREEZE_DIGEST}`. OSF registration yfw7h (approved and "
        "public; DOI 10.17605/OSF.IO/YFW7H). Lineage: ICIT-lineage "
        "(horus84) — results describe this lineage layer, and its "
        "object-ID-joined subset, not the Indus corpus in general.",
        "",
        f"## Outcome: {outcome['class']}",
        "",
        "> " + outcome["wording"],
        "",
        "## Step 0, gate by gate",
        "",
        f"- **Gate 0.1 — Input integrity: "
        f"{g['0.1_input_integrity']['status']}** — every spec "
        "section 2 pin and every DD-059-9 object-identifier source "
        "pin recomputes to its freeze-record value (hashes and "
        "byte counts in the machine record).",
    ]
    if "0.2_original_join_reproduction" in g:
        o = g["0.2_original_join_reproduction"]["observed"]
        lines.append(
            f"- **Gate 0.2 — Original-join reproduction: "
            f"{g['0.2_original_join_reproduction']['status']}** — "
            f"observed {o['layer_rows']} layer rows / {o['matched']} "
            f"matched / {o['ambiguous']} ambiguous / "
            f"{o['unmatched']} unmatched, against the recorded "
            "5,679 / 2,895 / 2 / 2,782.")
    if "0.3_object_id_join_census" in g:
        c3 = g["0.3_object_id_join_census"]
        lines.append(
            f"- **Gate 0.3 — Object-ID join census: "
            f"{c3.get('status', '—')}** — the join dataset built by "
            "the pinned route-(b) construction carries "
            f"{c3['intake_dataset']['records']} records; Phase-130 "
            "validation verdict: "
            f"{c3['intake_dataset']['validation_verdict']} "
            f"({c3['intake_dataset']['validation_summary']['errors']} "
            "errors, "
            f"{c3['intake_dataset']['validation_summary']['warnings']} "
            "warnings).")
    if "census" in result:
        c = result["census"]
        lines += [
            "",
            "## The gate census (the closure's finding)",
            "",
            f"- Layer rows: {c['layer_rows']}",
            f"- Joined rows: {c['joined_rows']} "
            f"({c['joined_share_percent']}%)",
            f"- Unjoined rows: {c['unjoined_rows']} "
            f"({c['rows_without_identifier']} carrying no "
            "identifier; "
            f"{c['unjoined_with_identifier_resolving_zero']} "
            "whose identifier resolves to zero catalogue objects)",
            "- Ambiguous rows (more than one distinct object): "
            f"{c['ambiguous_rows_more_than_one_object']}",
            "- Distinct catalogue objects joined to: "
            f"{c['distinct_catalogue_objects_joined_to']}",
            "- Catalogue layer: "
            f"{c['catalogue_layer']['rows_total']} rows, "
            f"{c['catalogue_layer']['distinct_objects_merged']} "
            "distinct objects across vols 1–2",
            "- Joined object-type mix: "
            + ", ".join(f"{k} {v}" for k, v in
                        c["joined_object_type_mix"].items()),
            "- Rows the object-ID join adds over the original "
            f"join: {len(c['added_rows_vs_original_join'])} "
            f"(original joined rows lost: "
            f"{c['original_joined_rows_lost']})",
            "",
            "The full per-row census — identifier provenance and "
            "resolution class for every one of the 5,679 layer "
            "rows — is `reports/phase421_join_census.json`.",
        ]
    if "0.4_gate_comparison" in g:
        c4 = g["0.4_gate_comparison"]
        lines += [
            "",
            f"- **Gate 0.4 — Gate comparison: {c4['status']}** — "
            f"joined {c4['joined_rows']} rows "
            f"({c4['joined_share_percent']}%) against the bar "
            f"fixed in advance at DD-059-7: >= {c4['bar_rows']} "
            f"rows (61.0%); shortfall {c4['shortfall_rows']} rows.",
        ]
    if "primary_test" in result:
        lines += ["", "## Primary test", "",
                  "See the machine record "
                  "(`reports/phase421_results.json`) for the full "
                  "flow, strata, test, effect sizes, "
                  "leave-one-site-out runs, and covariate "
                  "comparisons."]
    else:
        lines += [
            "",
            "## What was not done",
            "",
            "No F1 quantity was computed on the new join: no "
            "terminal mapping, no test statistic, no p-value, no "
            "odds ratio. The Phase-136 test machinery was not "
            "run. Spec 024's frozen records and SUPPORTED verdict "
            "stand unedited; this outcome appends beside them as "
            "a dated replication record that records a gate "
            "closure, not a verdict.",
        ]
    lines += [
        "",
        "Anchors asserted byte-identical before and after: "
        "`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` "
        f"at both readings (asserted: "
        f"{result.get('anchors_byte_identical')}).",
        "",
        "*AI disclosure: executed by an AI agent (Muse Spark, "
        "via Muse) at the direction of Tristen Pierson, per "
        "constitution section VI.*",
        "",
    ]
    return "\n".join(lines)


def main(argv=None) -> int:
    result, census_rows = build()
    RESULTS_OUT.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if census_rows is not None:
        census_doc = {
            "phase": "Phase-421", "spec": "059",
            "title": ("Spec 059 gate census — object-identifier "
                      "join, per layer row (DD-059-11: the census "
                      "is the join's audit)"),
            "unit": "layer row (DD-059-2)",
            "gate_bar": {"joined_rows_min": GATE_BAR_ROWS,
                         "joined_share_min_percent": 61.0,
                         "ruling": "DD-059-7"},
            "summary": result["census"],
            "rows": census_rows,
            "ai_disclosure": result["ai_disclosure"],
        }
        CENSUS_OUT.write_text(
            json.dumps(census_doc, indent=2) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(render_report(result), encoding="utf-8")
    print(f"[phase421] outcome: {result['outcome']['class']}")
    print(f"[phase421] wrote {RESULTS_OUT}")
    if census_rows is not None:
        print(f"[phase421] wrote {CENSUS_OUT}")
    print(f"[phase421] wrote {REPORT_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
