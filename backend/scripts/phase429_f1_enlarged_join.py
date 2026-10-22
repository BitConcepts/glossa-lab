#!/usr/bin/env python3
"""Phase-429 (spec 067, FROZEN) — the seal/tablet
difference on the enlarged join: Spec 059's
question re-run against the Spec 066 merged
catalogue layer v2 (design D-22, carried).

Executes the frozen Spec 067 contract (specs/
067-f1-enlarged-join/freeze.md; freeze digest
73463ab949f65ecf620a9f4544b9a84fe18f72056a86c48ce9d5d0164f3d41db;
OSF registration qsthg, approved and public
before this run, verified by the parent by API
read-back 2026-10-22: public true, pending
false, withdrawn false, reviews_state accepted).

Step 0 runs first, in the frozen order (spec
section 3), and decides the execution before any
F1 quantity exists on the new join:

  0.1 Input integrity — every spec section 2
      input, and every source named and pinned
      at freeze ruling DD-067-9, hashes to its
      freeze-record value; the merged catalogue
      layer v2 is asserted on the local file
      first (SHA-256, byte count, 9,741 rows,
      5,529 distinct objects); the Phase-130
      schema validates the join dataset built at
      gate 0.3 (verdict pass). A pin mismatch
      stops the run as INVALID — PIN FAILURE; a
      validation failure as INVALID — CENSUS
      FAILURE.
  0.2 Original-join reproduction — the original
      concordance join is re-run on the pinned
      layer and the pinned vols. 1-2 catalogue
      under its frozen rule (exact string; a row
      joins iff its cisi value is a printed
      catalogue ID in exactly one volume) and
      must reproduce the recorded census exactly:
      5,679 layer rows; 2,895 matched; 2
      ambiguous; 2,782 unmatched. A mismatch
      stops the run as INVALID — CENSUS FAILURE.
      This reproduction contributes no row to
      the enlarged set.
  0.3 The object-identifier join census — the
      join is rebuilt through object identifiers
      only, exactly as in Spec 059: each lineage
      row's published CISI object reference is
      carried as provenance.object_id under the
      Phase-130 intake schema, exactly as the
      pinned Spec 034 route-(b) construction
      (build_intake_dataset in backend/glossa_lab/
      phase398_matched_object.py) carried it, and
      resolves against the pinned MERGED
      catalogue layer v2 (an identifier resolving
      to exactly one distinct object joins; zero
      or more than one does not). String identity
      is never a join key (spec section 7.1;
      F067-C06). The census unit is the layer
      row (DD-067-2).
  0.4 The type-fill census (mandatory, Item 7
      section 6) — before any F1 quantity: type
      fill on the newly joined objects (the
      joined rows the Phase-421 census recorded
      as unjoined, identifier resolving to zero
      objects in the vols. 1-2 layer) and on the
      whole joined set, with the resulting
      eligible seal/tablet strata under the
      frozen Phase-136 eligibility mapping
      applied as a census (restriction to
      {Seals, Tablets}, then N >= 20 with >= 5
      Seals and >= 5 Tablets per site; no
      terminal mapping, no statistic).
  0.5 The gate comparison — freeze ruling
      DD-067-7 adopts Spec 059's bar carried
      unchanged: joined share >= 61.0%, i.e.
      >= 3,465 of 5,679 joined rows (0.61 x
      5,679 = 3,464.19; 3,464 rows = 60.997% and
      fails). No bar is derived from Spec 066's
      projection, which has no standing. Below
      the bar the execution closes CLOSED AT
      STEP 0 — JOIN GATE NOT MET, in the spec
      section 3.6 wording, with the gate and
      type-fill censuses published as the
      finding; no F1 quantity is computed.

Only if gate 0.5 passes does section 4 run: the
frozen Phase-136 flow on the enlarged joined set,
unchanged in every particular (TERMINAL14; the
Cochran-Mantel-Haenszel statistic; the permutation
null with B = 9,999 and seed 20261009; the
Mantel-Haenszel common odds ratio with the
Robins-Breslow-Greenland interval), reusing the
pinned Phase-136 builder's own statistic
functions, with the single-test family correction
confirmed at DD-067-8 (adjusted q = raw p), the
section 5 verdict mapping with DD-067-3's
precedence confirmed at DD-067-12, the
leave-one-site-out rerun (descriptive; mints no
verdict), and both covariate comparisons.

Outputs (written on every terminal outcome):
  - reports/phase429_results.json (machine
    record; aggregates only)
  - reports/phase429_report.md (the report)
  - the per-row gate census against layer v2 is
    a row-level product of the merged layer and
    stays RESTRICTED-LOCAL under spec section
    7.3 (written beside the layer in the main
    checkout's local catalogue store as
    phase429_join_census.json; named in the
    committed records by filename and counts
    only, never committed)

Integrity: every pin is asserted before any join
quantity; the anchors file is asserted
byte-identical before and after. Deterministic:
no wall-clock values are written into the
outputs; a second run reproduces all output
files byte-identically.
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

FREEZE_DIGEST = "73463ab949f65ecf620a9f4544b9a84fe18f72056a86c48ce9d5d0164f3d41db"
SPEC066_FREEZE_DIGEST = "0b81d8421c8fe66b486b2c729bb7e978faa6327c74b8f1bff7984128a31aa355"
GATE_BAR_ROWS = 3465
GATE_BAR_SHARE = 0.61
LAYER_ROWS = 5679

# Committed pins (spec section 2 + DD-067-9):
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
    "reports/phase421_join_census.json": (
        "952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8",
        1981510),
    "reports/phase421_results.json": (
        "3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f",
        36170),
    "data/intake/cisi31_extension_index.csv": (
        "be20439a094d4196352bd8c31fd8eeee3f92cd81d8443786a1c520d8355f2540",
        78531),
}

# Local-store pins (spec section 2 + DD-067-9):
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
    "merged_catalogue_layer_v2": (
        "cd0c2ba8823678be9f7573616528ae0b6be2fe579dc7e34c93add421c80886ad",
        2655958),
}
MERGED_LAYER_ROWS = 9741
MERGED_LAYER_DISTINCT = 5529

RESULTS_OUT = REPO / "reports" / "phase429_results.json"
REPORT_OUT = REPO / "reports" / "phase429_report.md"
# Restricted-local per-row census (spec section 7.3): written
# beside the merged layer in the main checkout's local
# catalogue store; NEVER into the repo tree.
CENSUS_OUT = (MAIN_CHECKOUT / CATALOGUE_REL
              / "phase429_join_census.json")


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

def _object_view(rows: list[dict]) -> dict:
    """Distinct-object view keyed by stripped cisi_id (the
    pinned Phase-398 load_catalogue keying): first non-empty
    site / object_type wins, as in Phase-136/421."""
    merged: dict[str, dict] = {}
    for r in rows:
        cid = (r.get("cisi_id") or "").strip()
        if not cid:
            continue
        obj = merged.setdefault(cid, {
            "n_rows": 0, "volumes": set(), "sites": set(),
            "object_types": set(), "site_first": "",
            "object_type_first": ""})
        obj["n_rows"] += 1
        vol = r.get("volume")
        if vol:
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
    return merged


def load_catalogue_rows() -> tuple[dict, dict, dict]:
    """Vols. 1-2 layer (gate 0.2 ONLY). Returns (per-volume
    printed-ID sets [raw values exactly as Phase-136 read
    them], merged distinct-object view, per-volume counts)."""
    cat_dir = catalogue_dir()
    vol_ids: dict[int, set] = {}
    all_rows: list[dict] = []
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
        all_rows.extend(rows)
    return vol_ids, _object_view(all_rows), counts


def load_layer_v2() -> tuple[dict, dict]:
    """The pinned merged catalogue layer v2 (gate 0.3
    resolution). Returns (distinct-object view, shape)."""
    path = catalogue_dir() / "cisi_catalogue_layer_v2.csv"
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    merged = _object_view(rows)
    shape = {
        "rows": len(rows),
        "distinct_objects": len(merged),
        "rows_by_volume": dict(sorted(Counter(
            (r.get("volume") or "") for r in rows).items())),
        "object_type_mix_all_rows": dict(sorted(Counter(
            (r.get("object_type") or "(unfilled)")
            for r in rows).items())),
    }
    return merged, shape


def load_horus_rows() -> list[dict]:
    with HORUS84.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build() -> tuple[dict, list[dict] | None]:
    result: dict = {
        "phase": "Phase-429",
        "spec": "067",
        "title": ("The seal/tablet difference on the enlarged "
                  "join — Spec 059's question re-run against "
                  "the Spec 066 merged catalogue layer v2 "
                  "(design D-22, carried)"),
        "lineage_label": "ICIT-lineage (horus84)",
        "lineage_sentence": ("results describe this lineage layer, "
                             "and (gate-passed) its object-ID-joined "
                             "subset, not the Indus corpus in general."),
        "claim_under_test": "STUDY-SPEC-024/F1",
        "freeze_digest": FREEZE_DIGEST,
        "spec066_freeze_digest": SPEC066_FREEZE_DIGEST,
        "osf_registration": "https://osf.io/qsthg/",
        "osf_registration_state": (
            "approved and public before this run; verified by "
            "the parent by API read-back 2026-10-22 (public "
            "true, pending false, withdrawn false, "
            "reviews_state accepted)"),
        "execution_date": "2026-10-22",
        "gate_bar": {"ruling": "DD-067-7 (carrying DD-059-7)",
                     "joined_share_min": GATE_BAR_SHARE,
                     "joined_rows_min": GATE_BAR_ROWS,
                     "arithmetic": ("0.61 x 5,679 = 3,464.19, so "
                                    ">= 61.0% is >= 3,465 rows; 3,464 "
                                    "rows = 60.997% and fails"),
                     "baseline": "2,895 / 5,679 = 50.977% (51.0%)"},
        "restricted_local_products": {
            "note": ("row-level products of the merged layer "
                     "stay restricted-local (spec section 7.3) "
                     "and are named here by filename and counts "
                     "only"),
            "per_row_join_census": {
                "filename": "phase429_join_census.json",
                "location": ("restricted local store, beside "
                             "the merged catalogue layer v2 "
                             "(main checkout corpora/downloads/"
                             "cisi_image_layer/catalogue/)"),
                "rows": None},
        },
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
        "merged_catalogue_layer_v2": (
            catalogue_dir() / "cisi_catalogue_layer_v2.csv"),
    }
    for key, pin in LOCAL_PINS.items():
        pin_checks[key] = check_pin(local_paths[key], pin)
    # The Spec 066 freeze digest is asserted from its record.
    spec066_freeze = json.loads(
        (REPO / "specs/066-phase130-catalogue-extension/freeze.json"
         ).read_text(encoding="utf-8"))
    pin_checks["spec066_freeze_digest"] = {
        "path": "specs/066-phase130-catalogue-extension/freeze.json",
        "digest": spec066_freeze.get("digest"),
        "pin_digest": SPEC066_FREEZE_DIGEST,
        "match": spec066_freeze.get("digest") == SPEC066_FREEZE_DIGEST}
    hashes_ok = all(c["match"] for c in pin_checks.values())
    # The merged layer v2 is asserted on the local file BEFORE
    # any join work: SHA-256 and bytes (above), plus its rows
    # and distinct objects counted from the file.
    merged_v2, layer_v2_shape = load_layer_v2()
    layer_shape_ok = (
        layer_v2_shape["rows"] == MERGED_LAYER_ROWS
        and layer_v2_shape["distinct_objects"] == MERGED_LAYER_DISTINCT)
    result["inputs"] = pin_checks
    result["merged_layer_v2_shape"] = layer_v2_shape
    result["gates"]["0.1_input_integrity"] = {
        "status": "PASS" if (hashes_ok and layer_shape_ok) else "FAIL",
        "detail": ("every spec section 2 pin and every DD-067-9 "
                   "source pin recomputes to its freeze-record "
                   "value, and the merged catalogue layer v2 "
                   "asserted on the local file first (9,741 "
                   "rows, 5,529 distinct objects)"
                   if (hashes_ok and layer_shape_ok) else
                   "at least one pin or the layer v2 shape "
                   "mismatches; see inputs"),
        "failure_class": "PIN FAILURE",
        "schema_validation": "recorded at gate 0.3 (the dataset is "
                             "built there); a validation failure "
                             "closes the run INVALID — CENSUS "
                             "FAILURE under section 3.1",
    }
    if not (hashes_ok and layer_shape_ok):
        result["outcome"] = {
            "class": "INVALID — PIN FAILURE",
            "wording": ("INVALID — PIN FAILURE — gate 0.1 failed: "
                        "an input pin (or the merged layer v2 "
                        "shape) mismatches its freeze-record "
                        "value. No join was built and no F1 "
                        "quantity was computed."),
        }
        result["anchors_byte_identical"] = (
            sha256_of(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
            == anchors_before)
        return result, census_rows

    horus_rows = load_horus_rows()
    vol_ids, merged_vols, cat_counts = load_catalogue_rows()
    merged = merged_v2

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
            "class": "INVALID — CENSUS FAILURE",
            "wording": ("INVALID — CENSUS FAILURE — gate 0.2 "
                        "failed: the original concordance join "
                        "does not reproduce the recorded census "
                        "exactly. The gate's baseline is not "
                        "established; no new join was built and "
                        "no F1 quantity was computed."),
        }
        result["anchors_byte_identical"] = (
            sha256_of(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
            == anchors_before)
        return result, census_rows

    # ── Gate 0.3: the object-identifier join census ──────────────
    # Resolution is against the pinned merged catalogue layer
    # v2 (merged = merged_v2, loaded and shape-asserted at
    # gate 0.1). The join dataset is built by the PINNED
    # route-(b) construction itself (its hash was asserted at
    # gate 0.1), from the pinned converted keyed layer — the
    # same source in converted form (DD-067-9) — and validated
    # under the pinned Phase-130 schema by the pinned validator.
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
                             "DD-067-9)"),
            "validation_verdict": validation["verdict"],
            "validation_summary": validation["summary"],
        },
    }
    if validation["verdict"] != "pass":
        result["gates"]["0.3_object_id_join_census"]["status"] = "FAIL"
        result["outcome"] = {
            "class": "INVALID — CENSUS FAILURE",
            "wording": ("INVALID — CENSUS FAILURE — the Phase-130 "
                        "schema validation of the join dataset "
                        "did not return pass (spec section 3.1). "
                        "No gate comparison was made and no F1 "
                        "quantity was computed."),
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
    added_vs_original = [
        c for c in joined_rows
        if c["layer_row"] not in original_joined_idx]
    census = {
        "unit": "layer row (DD-067-2)",
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
            "name": "merged catalogue layer v2 (Spec 066)",
            "rows_total": layer_v2_shape["rows"],
            "distinct_objects": layer_v2_shape["distinct_objects"],
            "rows_by_volume": layer_v2_shape["rows_by_volume"],
            "vols_1_2_reference": {
                "rows_total": sum(v["rows"] for v in cat_counts.values()),
                "per_volume": cat_counts,
                "distinct_objects_merged": len(merged_vols),
                "ids_in_both_volumes": sorted(
                    set(vol_ids[1]) & set(vol_ids[2])),
            },
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
        "added_rows_vs_original_join_count": len(added_vs_original),
        "added_rows_vs_original_join": (
            "row-level list held in the restricted-local "
            "per-row census (spec section 7.3); count only here"),
        "original_joined_rows_lost": sum(
            1 for i in original_joined_idx
            if not census_rows[i]["joined"]),
        "raw_value_discrepancies_lineage_vs_converted_count": len(
            discrepancies),
        "raw_value_discrepancies_lineage_vs_converted": (
            "per-row detail held in the restricted-local "
            "per-row census; count only here"),
        "cross_check": ("the census was derived twice: through "
                        "the pinned route-(b) intake dataset and "
                        "directly from the lineage layer's own "
                        "cisi field (same strip the construction "
                        "applies); every row's joined classification "
                        "agrees between the two routes"),
        "more_than_one_note": ("resolution is against distinct "
                               "catalogue objects in the merged "
                               "catalogue layer v2 (DD-067-9): an "
                               "identifier is a distinct object's "
                               "own ID, so the more-than-one class "
                               "is structurally empty on this "
                               "layer; it is counted and reported "
                               "as observed"),
    }
    result["gates"]["0.3_object_id_join_census"]["status"] = "PASS"
    result["gates"]["0.3_object_id_join_census"]["census"] = census
    result["census"] = census
    result["restricted_local_products"][
        "per_row_join_census"]["rows"] = len(census_rows)
    # Restricted-local detail carried out of the committed
    # record by main(): the per-row discrepancies list.
    result["_restricted_discrepancies"] = discrepancies
    result["_restricted_added_rows"] = [
        {"layer_row": c["layer_row"],
         "inscription_id": c["inscription_id"],
         "site": c["site"],
         "provenance_object_id": c["provenance_object_id"],
         "catalogue_object_type": c["catalogue_object_type"]}
        for c in added_vs_original]

    # ── Gate 0.4: the type-fill census (mandatory) ────────────────
    # Before any F1 quantity exists: no terminal mapping, no
    # statistic — type fill and the census-form eligible strata
    # only (spec section 3.4).
    p421 = json.loads((REPO / "reports/phase421_join_census.json"
                       ).read_text(encoding="utf-8"))
    p421_by_row = {r["layer_row"]: r for r in p421["rows"]}
    newly_joined = [
        c for c in joined_rows
        if not p421_by_row[c["layer_row"]]["joined"]
        and p421_by_row[c["layer_row"]]["resolution_class"] == "zero"]

    def _fill(rows_list):
        objs = {}
        for c in rows_list:
            obj = merged[c["catalogue_object_id"]]
            objs[c["catalogue_object_id"]] = obj["object_type_first"]
        return {
            "joined_rows": len(rows_list),
            "rows_type_filled": sum(
                1 for c in rows_list if c["catalogue_object_type"]),
            "rows_type_unfilled": sum(
                1 for c in rows_list
                if not c["catalogue_object_type"]),
            "distinct_objects": len(objs),
            "distinct_objects_type_filled": sum(
                1 for v in objs.values() if v),
            "distinct_objects_type_unfilled": sum(
                1 for v in objs.values() if not v),
            "type_mix_rows": dict(sorted(Counter(
                c["catalogue_object_type"] or "(unfilled)"
                for c in rows_list).items())),
            "type_mix_distinct_objects": dict(sorted(Counter(
                v or "(unfilled)" for v in objs.values()).items())),
        }

    restricted_rows = [
        c for c in joined_rows
        if c["catalogue_object_type"] in ("Seals", "Tablets")]
    census_strata = []
    for site in sorted({c["site"] for c in restricted_rows}):
        srows = [c for c in restricted_rows if c["site"] == site]
        n_seals = sum(1 for c in srows
                      if c["catalogue_object_type"] == "Seals")
        n_tablets = len(srows) - n_seals
        census_strata.append({
            "site": site, "n_restricted_rows": len(srows),
            "n_seals": n_seals, "n_tablets": n_tablets,
            "eligible_census_form": (
                len(srows) >= 20 and n_seals >= 5 and n_tablets >= 5),
            "note": ("census form: restriction to {Seals, "
                     "Tablets} then the stratum rule, before "
                     "any terminal mapping (spec section 3.4); "
                     "the primary's eligibility is computed on "
                     "the analysis population in section 4")})
    type_fill = {
        "newly_joined_objects": _fill(newly_joined),
        "newly_joined_definition": (
            "joined rows the Phase-421 census recorded as "
            "unjoined with resolution class zero (identifier "
            "resolving to zero objects in the vols. 1-2 layer)"),
        "whole_joined_set": _fill(joined_rows),
        "restricted_seals_tablets_rows": len(restricted_rows),
        "eligible_seal_tablet_strata_census_form": census_strata,
        "eligible_sites_census_form": [
            s["site"] for s in census_strata
            if s["eligible_census_form"]],
    }
    result["type_fill_census"] = type_fill
    result["gates"]["0.4_type_fill_census"] = {
        "status": "PASS",
        "detail": ("type fill censused on the newly joined "
                   "objects and on the whole joined set, with "
                   "the resulting eligible seal/tablet strata "
                   "in census form, before any F1 quantity"),
        "type_fill": type_fill,
    }

    # ── Gate 0.5: the gate comparison ─────────────────────────────
    gate_pass = len(joined_rows) >= GATE_BAR_ROWS
    result["gates"]["0.5_gate_comparison"] = {
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
                "object-identifier join against the merged "
                "catalogue layer v2 joined "
                f"{len(joined_rows)} of 5,679 lineage rows "
                f"({joined_share * 100:.2f}%), against the "
                "original concordance join's 51.0% and the gate "
                "fixed in advance at 61.0% or more (≥ 3,465 "
                "rows, carried from Spec 059 at DD-067-7). The "
                "enlarged joined set this design required does "
                "not exist on the enlarged catalogue data "
                "either, so no F1 quantity was computed and "
                "STUDY-SPEC-024/F1 stands exactly as recorded "
                "— SUPPORTED on its original joined subset, "
                "its 'on the joined subset' scope unchanged. "
                "The unjoined share is a measured property of "
                "the enlarged catalogue data, not an oversight."),
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
# Reached only when gate 0.5 passes. Statistic functions are the
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
                "The object-ID join against layer v2 passed "
                f"its gate ({n_joined} of 5,679 rows, "
                f"{share_pct}%), but the enlarged set fails the "
                f"frozen estimability rule ({failed}; cell "
                "counts shown in the record; the step-0 "
                "type-fill census is part of that record). No "
                "p-value was computed and no verdict under "
                "this spec exists. STUDY-SPEC-024/F1 stands "
                "exactly as recorded."),
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
    q = raw_p  # single-test family (DD-067-8): BH over one p-value
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
        "correction": "DD-067-8: single-test family; q = raw p",
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
    p421 = json.loads((REPO / "reports/phase421_join_census.json"
                       ).read_text(encoding="utf-8"))
    p421_joined = {r["layer_row"] for r in p421["rows"] if r["joined"]}
    newly_idx = [i for i in joined_idx if i not in p421_joined]
    prior_idx = [i for i in joined_idx if i in p421_joined]
    return {
        "joined_vs_unjoined": {"joined": joined_desc,
                               "unjoined": unjoined_desc},
        "original_vs_added": {"original_joined": describe(original_idx),
                              "added_by_object_id_join": describe(
                                  added_idx)},
        "phase421_joined_vs_newly_joined": {
            "phase421_joined_set": describe(prior_idx),
            "newly_joined_by_layer_v2": describe(newly_idx)},
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
        "# Phase-429 — Spec 067 execution report",
        "",
        "Claim: `STUDY-SPEC-024/F1` — standing SETTLED — SUPPORTED on "
        "its original joined subset (odds ratio 2.384, interval "
        "[1.847, 3.077], family q = 0.00015), exactly as recorded. "
        "Execution date: 2026-10-22. Freeze digest: "
        f"`{FREEZE_DIGEST}`. OSF registration qsthg (approved and "
        "public before this run; verified by API read-back "
        "2026-10-22). Lineage: ICIT-lineage "
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
        "section 2 pin and every DD-067-9 source pin recomputes "
        "to its freeze-record value, and the merged catalogue "
        "layer v2 was asserted on the local file first (SHA-256, "
        "2,655,958 bytes, 9,741 rows, 5,529 distinct objects; "
        "hashes and byte counts in the machine record).",
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
            "## The gate census",
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
            "- Catalogue layer: merged catalogue layer v2, "
            f"{c['catalogue_layer']['rows_total']} rows, "
            f"{c['catalogue_layer']['distinct_objects']} "
            "distinct objects",
            "- Joined object-type mix: "
            + ", ".join(f"{k} {v}" for k, v in
                        c["joined_object_type_mix"].items()),
            "- Rows the object-ID join against layer v2 adds "
            "over the original concordance join: "
            f"{c['added_rows_vs_original_join_count']} "
            f"(original joined rows lost: "
            f"{c['original_joined_rows_lost']})",
            "",
            "The full per-row census — identifier provenance and "
            "resolution class for every one of the 5,679 layer "
            "rows — is the restricted-local product "
            "`phase429_join_census.json` (5,679 rows), held "
            "beside the merged layer in the restricted local "
            "store under spec section 7.3 and named here by "
            "filename and count only; it is not committed.",
        ]
    if "type_fill_census" in result:
        tf = result["type_fill_census"]
        nw = tf["newly_joined_objects"]
        wh = tf["whole_joined_set"]
        lines += [
            "",
            "## The type-fill census (gate 0.4)",
            "",
            f"- **Gate 0.4 — Type-fill census: "
            f"{g['0.4_type_fill_census']['status']}** — taken "
            "before any F1 quantity existed.",
            "- Newly joined objects (rows the Phase-421 census "
            "recorded as unjoined, identifier resolving to zero "
            "in vols. 1–2): "
            f"{nw['joined_rows']} rows / {nw['distinct_objects']} "
            f"distinct objects — type filled "
            f"{nw['distinct_objects_type_filled']} objects "
            f"({nw['rows_type_filled']} rows), type unfilled "
            f"{nw['distinct_objects_type_unfilled']} objects "
            f"({nw['rows_type_unfilled']} rows).",
            "- Whole joined set: "
            f"{wh['joined_rows']} rows / {wh['distinct_objects']} "
            f"distinct objects — type filled "
            f"{wh['distinct_objects_type_filled']} objects "
            f"({wh['rows_type_filled']} rows), type unfilled "
            f"{wh['distinct_objects_type_unfilled']} objects "
            f"({wh['rows_type_unfilled']} rows).",
            "- Whole joined set type mix (rows): "
            + ", ".join(f"{k} {v}" for k, v in
                        wh["type_mix_rows"].items()),
            "- Restricted to {Seals, Tablets}: "
            f"{tf['restricted_seals_tablets_rows']} rows.",
            "- Eligible seal/tablet strata (census form, "
            "before terminal mapping): "
            + (", ".join(tf["eligible_sites_census_form"])
               or "none")
            + ". Per-site census strata are in the machine "
              "record.",
        ]
    if "0.5_gate_comparison" in g:
        c5 = g["0.5_gate_comparison"]
        lines += [
            "",
            f"- **Gate 0.5 — Gate comparison: {c5['status']}** — "
            f"joined {c5['joined_rows']} rows "
            f"({c5['joined_share_percent']}%) against the bar "
            f"fixed in advance at DD-067-7: >= {c5['bar_rows']} "
            f"rows (61.0%); shortfall {c5['shortfall_rows']} rows.",
        ]
    if "primary_test" in result:
        pt = result["primary_test"]
        lines += ["", "## Primary test (frozen Phase-136 flow)", ""]
        fl = pt["flow"]
        lines += [
            f"- Flow: joined {fl['joined_rows']} → typed "
            f"{fl['typed_filled']} (untyped {fl['untyped']}) → "
            f"restricted to seals/tablets "
            f"{fl['restricted_seals_tablets']} → terminal "
            f"mapped {fl['terminal_mapped']} (UNK "
            f"{fl['terminal_unk']}, no codes "
            f"{fl['terminal_no_codes']}) → analysis population "
            f"in eligible strata "
            f"{fl['analysis_population_eligible_strata']}.",
            "- Eligible strata: "
            + (", ".join(pt["eligible_strata"]) or "none") + ".",
            f"- Estimability: "
            f"{pt['estimability']['estimable']} "
            f"({pt['estimability']['n_eligible_strata']} eligible "
            "strata; pooled expected counts >= 5 in "
            f"{pt['estimability']['fraction_expected_ge_5']} of "
            "cells).",
        ]
        if "test" in pt:
            t = pt["test"]
            es = pt["effect_sizes"]
            ci = es["mh_ci95"]
            lines += [
                f"- CMH chi-square: {t['statistic_observed']}; "
                f"permutation raw p = {t['raw_p']} (B = {t['B']}, "
                f"seed {t['seed']}); family-adjusted q = "
                f"{t['adjusted_q_single_test_family']} "
                "(single-test family, DD-067-8).",
                f"- Mantel–Haenszel common odds ratio: "
                f"{es['mh_common_odds_ratio']}, 95% CI "
                f"[{ci[0]}–{ci[1]}]; crude odds ratio "
                f"(uncontrolled): "
                f"{es['crude_odds_ratio_uncontrolled']['odds_ratio']}.",
                "",
                "## Leave-one-site-out (descriptive)",
                "",
                pt["loso"]["sentence"],
                "",
                "| Dropped site | Estimable | MH odds ratio | 95% CI |",
                "|---|---|---|---|",
            ]
            for run in pt["loso"]["runs"]:
                lines.append(
                    f"| {run['dropped_site']} | "
                    f"{run['estimable']} | "
                    f"{run.get('mh_common_odds_ratio')} | "
                    f"{run.get('mh_ci95')} |")
            lines += [
                "",
                "## Covariate comparisons",
                "",
                "Joined versus unjoined rows, the original "
                "joined set versus the rows the layer-v2 join "
                "adds, and the Phase-421 joined set versus the "
                "newly joined rows — on site, object type (for "
                "rows the catalogue types), text length, and "
                "preservation as recorded — are in the machine "
                "record (`reports/phase429_results.json`). "
                "Object type for unjoined rows is not carried: "
                "unjoined rows have no catalogue object.",
            ]
        else:
            lines += [
                "",
                "No p-value was computed: the enlarged set is "
                "NOT ESTIMABLE under the frozen rule (above). "
                "The covariate comparisons are in the machine "
                "record.",
            ]
    else:
        lines += [
            "",
            "## What was not done",
            "",
            "No F1 quantity was computed on the new join: no "
            "terminal mapping, no test statistic, no p-value, no "
            "odds ratio. The Phase-136 test machinery was not "
            "run. Spec 024's and Spec 059's frozen records and "
            "verdicts stand unedited; this outcome appends "
            "beside them as a dated replication record that "
            "records a gate closure, not a verdict.",
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
    discrepancies = result.pop("_restricted_discrepancies", [])
    added_rows = result.pop("_restricted_added_rows", [])
    RESULTS_OUT.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if census_rows is not None:
        census_doc = {
            "phase": "Phase-429", "spec": "067",
            "title": ("Spec 067 gate census — object-identifier "
                      "join against the merged catalogue layer "
                      "v2, per layer row (DD-067-11: the census "
                      "is the join's audit). RESTRICTED-LOCAL "
                      "under spec section 7.3: a row-level "
                      "product of the merged layer; never "
                      "committed."),
            "unit": "layer row (DD-067-2)",
            "gate_bar": {"joined_rows_min": GATE_BAR_ROWS,
                         "joined_share_min_percent": 61.0,
                         "ruling": "DD-067-7"},
            "summary": result["census"],
            "type_fill_census": result.get("type_fill_census"),
            "added_rows_vs_original_join": added_rows,
            "raw_value_discrepancies_lineage_vs_converted":
                discrepancies,
            "rows": census_rows,
            "ai_disclosure": result["ai_disclosure"],
        }
        CENSUS_OUT.parent.mkdir(parents=True, exist_ok=True)
        CENSUS_OUT.write_text(
            json.dumps(census_doc, indent=2) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(render_report(result), encoding="utf-8")
    print(f"[phase429] outcome: {result['outcome']['class']}")
    print(f"[phase429] wrote {RESULTS_OUT}")
    if census_rows is not None:
        print(f"[phase429] wrote restricted-local {CENSUS_OUT}")
    print(f"[phase429] wrote {REPORT_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
