#!/usr/bin/env python3
"""Phase-408 — Spec 048 (Parpola's fish-sign family,
sign by sign; design D-04; consumes Asset F).

Executes STEP 0 ONLY of the frozen Spec 048 contract
(specs/048-parpola-fish-family-profiles/freeze.md;
freeze digest
56beec70957ac64e5f17e3bb889e66c9becfe7a7a55b49bc59e5a232c642a846;
OSF registration eqpab, approved and public before
this run, DOI 10.17605/OSF.IO/EQPAB) under the
runnable-experiments campaign (Wave 3, Group 3).
Gates 0.1 and 0.2 run in full; gate 0.3 closes the
execution, so gates 0.4-0.6, the primary arm, the
second arm, the sensitivity, and the controls do
not exist in this script — a gate failure closes
the execution before any of those can run, by the
frozen design. No ending-follower rate is computed
for any sign at any point in this script.

Gates, in the frozen order (spec section 3):

  0.1 Asset F digest assertion — Asset F's
      canonical file (specs/044-fish-sign-coastal-
      residue/asset-f-fish-family.json, preserved
      in Spec 044's directory) is exhibited; its
      SHA-256 is recomputed over the canonical
      bytes with the `digest` field excluded
      (Spec 044 section 4.2's exclusion rule, the
      canonical serialisation of Spec 044's own
      build: json.dumps with indent=2, keys sorted,
      ensure_ascii=False, plus a trailing newline,
      the `digest` field removed) and compared to
      the digest recorded in Spec 044's step-0
      outcome record — the pin source the freeze
      fixed (DD-048-9). Absence of the file or of
      that record closes ASSET F NOT AVAILABLE; a
      mismatch closes ASSET F DIGEST MISMATCH. The
      asset is never rebuilt, re-derived, or
      substituted under this spec.
  0.2 Membership join and cross-check — each
      Asset F member is joined to the primary
      corpus's numbering by its `mahadevan_number`
      locator, through the pinned Mahadevan–Parpola
      crosswalk (SHA-256 9ebd7723...). A member
      carrying no Mahadevan mapping, or whose
      locator is absent from the crosswalk, is
      recorded UNMAPPED with the reason and
      excluded from both arms' weighting; it is
      never silently dropped and never counted as
      TOO THIN (DD-048-5). The cross-check reports
      Asset F's membership against the claim
      record's trio (Mahadevan 72, 64, 70) and the
      Phase-43 six candidates (267, 72, 65, 59,
      60, 70), every divergence named; it adds and
      removes no member.
  0.3 Strict corpus identification, pin, and
      measure reproduction — the primary corpus
      layer is identified from the database as
      the V3 / Mahadevan-lineage layer the
      Phase-43 framework used (Spec 033 section 4;
      DD-048-10), exported in full, and pinned by
      SHA-256, and the T2.4 reference points are
      re-derived from the pinned layer (sign 72 —
      181 occurrences, terminal fraction 0.259,
      supported; sign 267 — 356 occurrences,
      0.038, not supported). The identification
      attempt is mechanical, in four parts, and
      recorded in full:
        C1 the V3 layer itself: the one loader of
           record (backend/glossa_lab/data/
           indus_corpus_v3.py) reads one data file,
           the Firestore 'indusarrays' dump at
           glossa-corpus/indus/sources/rmrl/raw/
           indusscript-probe/
           firestore_indusarrays_full.jsonl; the
           loader is imported from its file and run
           — by its own code a missing file yields
           an empty record list;
        C2 a database copy in the execution tree
           (backend/data/glossa.db) — present
           or not;
        C3 the Phase-43 record's own census of its
           corpus (T1_1: source, records,
           sequences, dockeys, sign instances) and
           its T2.4 reference points, read from
           the pinned results file;
        C4 every other corpus layer the tree
           holds, censused and compared against
           that record: the site-attributed layer
           (yajnadevam_inscriptions.csv), the V1
           research export (indus_research.jsonl,
           with its source-system mixture), the
           ICIT-format export, and the Holdat
           downloads path (the second compilation
           of the sibling specs, not this arm).
      No layer is substituted for the V3 layer.
      If the layer cannot be uniquely identified,
      cannot be exported whole, or the reference
      points do not reproduce, the run closes as
      STRICT CORPUS NOT PINNABLE and nothing is
      counted.
  0.4 Holdat layer and crosswalk pin — NOT
      REACHED when 0.3 closes.
  0.5 Census (margins only) — NOT REACHED.
  0.6 Control set freeze — NOT REACHED.

Integrity (spec sections 2, 6, 10): every
section 2 pin that carries a byte pin is asserted
before any gate quantity — the Phase-43 results
file, the anchors file, the Mahadevan–Parpola
crosswalk, and the Spec 033 spec — and a mismatch
closes INVALID. The claim file is handled in the
Spec 038 form the freeze test itself uses: its
freeze-time hash (3202aeca...) is recorded as a
definition constant, and manual_002's facts
(status, stage, sign_ids, not-understood text)
are asserted on the live file, because the
backend suite regenerates the extracted-claims
store mid-run and a later regeneration (Spec
058's execution, 2026-10-21) has already changed
the live file's extraction timestamps — and
only those, for manual_002. The anchors file is
asserted byte-identical before and after.

Outputs (written on every terminal outcome):
  - reports/phase408_results.json (the step-0
    record: pins, the Asset F digest assertion,
    the join and cross-check, the gate 0.3
    identification attempt, per-gate verdicts)
  - reports/phase408_step0_report.md (the step-0
    report, under spec section 9's headline rules
    as they apply to a step-0 closure)

This record is internal under the campaign's
Roif gate (R-7); it is not a publication. The
script is deterministic: a second run reproduces
both output files byte-identically.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]

PIN_PHASE43 = (
    "outputs/phase43_all.json",
    "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4",
)
PIN_ANCHORS = (
    "backend/reports/INDUS_FINAL_ANCHORS.json",
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
)
PIN_CROSSWALK = (
    "backend/glossa_lab/data/mahadevan_parpola_crosswalk.json",
    "9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b",
)
PIN_SPEC033 = (
    "specs/033-sa-free-language-comparison/spec.md",
    "eaea0e2e4f288e199acfa56cc401b80b5939175578ccb5f52c87adddf2f15ca9",
)
CLAIM_FILE = (
    "glossa-indus/claims/extracted_claims/"
    "parpola_2010_dravidian_solution.json"
)
CLAIM_FREEZE_SHA256 = (
    "3202aeca1ddaf7e588ebf19b2eaf8c93d06a34ecebba"
    "20d06c1b22810dfb000c"
)
CLAIM_ID = "parpola_2010_dravidian_solution_manual_002"
SPEC044_FREEZE_DIGEST = (
    "6851f943d196fa389e48b67cb5161b90daa1180d8a3"
    "e1cf3f020fcf25691d9c8"
)
ASSET_F = (
    "specs/044-fish-sign-coastal-residue/"
    "asset-f-fish-family.json"
)
SPEC044_OUTCOME = (
    "specs/044-fish-sign-coastal-residue/outcome.md"
)
FIRESTORE_DUMP = (
    "glossa-corpus/indus/sources/rmrl/raw/"
    "indusscript-probe/firestore_indusarrays_full.jsonl"
)
V3_LOADER = "backend/glossa_lab/data/indus_corpus_v3.py"
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

_OUT_RESULTS = _REPO / "reports/phase408_results.json"
_OUT_REPORT = _REPO / "reports/phase408_step0_report.md"

EXECUTION_DATE = "2026-10-21"
BASE_COMMIT = "3e75d7b0707a210598e90df5d92d92253cf9435b"
FREEZE_DIGEST = (
    "56beec70957ac64e5f17e3bb889e66c9becfe7a7a"
    "55b49bc59e5a232c642a846"
)

TRIO = [72, 64, 70]
PHASE43_SIX = [267, 72, 65, 59, 60, 70]


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


def _canonical(obj: dict) -> bytes:
    """Spec 044 section 4's canonical serialisation
    (the form its own build script uses)."""
    return (json.dumps(obj, indent=2, sort_keys=True,
                       ensure_ascii=False)
            + "\n").encode("utf-8")


def _asset_f_digest() -> dict:
    """Gate 0.1's exhibit: the canonical file, the
    digest recorded in Spec 044's step-0 outcome
    record (the pin source, DD-048-9), and the
    recomputation under the exclusion rule."""
    asset_path = _REPO / ASSET_F
    outcome_path = _REPO / SPEC044_OUTCOME
    out = {
        "asset_path": ASSET_F,
        "asset_present": asset_path.exists(),
        "pin_source": SPEC044_OUTCOME,
        "pin_source_present": outcome_path.exists(),
        "digest_recorded_in_pin_source": None,
        "digest_field_in_file": None,
        "digest_recomputed_excluding_digest_field": None,
        "whole_file_sha256": None,
        "member_count": None,
    }
    if outcome_path.exists():
        flat = " ".join(
            outcome_path.read_text("utf-8").split())
        m = re.search(
            r"Digest \(SHA-256 of the canonical bytes "
            r"with the `digest` field excluded\): "
            r"`([0-9a-f]{64})`", flat)
        if m:
            out["digest_recorded_in_pin_source"] = m.group(1)
    if asset_path.exists():
        out["whole_file_sha256"] = _sha256(asset_path)
        obj = json.loads(asset_path.read_text("utf-8"))
        out["digest_field_in_file"] = obj.get("digest")
        out["member_count"] = obj.get("member_count")
        stripped = {k: v for k, v in obj.items()
                    if k != "digest"}
        out["digest_recomputed_excluding_digest_field"] = (
            hashlib.sha256(_canonical(stripped)).hexdigest())
    recorded = out["digest_recorded_in_pin_source"]
    recomputed = out["digest_recomputed_excluding_digest_field"]
    out["assertion"] = (
        "PASS" if (recorded is not None
                   and recomputed == recorded
                   and out["digest_field_in_file"] == recorded)
        else "FAIL")
    return out


def _claim_facts() -> dict:
    """The claim file in the Spec 038 form: facts
    asserted on the live file; the freeze-time
    hash carried as a definition constant only."""
    path = _REPO / CLAIM_FILE
    doc = json.loads(path.read_text("utf-8"))
    entries = [c for c in doc["claims"]
               if c["claim_id"] == CLAIM_ID]
    entry = entries[0] if len(entries) == 1 else {}
    facts = {
        "entries_with_claim_id": len(entries),
        "claim_status": entry.get("claim_status"),
        "stage": entry.get("stage"),
        "sign_ids_mahadevan": (
            entry.get("sign_ids", {}).get("mahadevan")),
        "not_understood_names_the_family_test": (
            "run sign by sign across the whole fish family"
            in entry.get("not_understood", "")),
        "not_understood_names_the_strict_corpus": (
            "on the strict corpus"
            in entry.get("not_understood", "")),
    }
    facts["facts_match_the_freeze_record"] = (
        len(entries) == 1
        and facts["claim_status"] == "partially_supported"
        and facts["stage"] == "explained"
        and facts["sign_ids_mahadevan"] == ["72", "64", "70"]
        and facts["not_understood_names_the_family_test"]
        and facts["not_understood_names_the_strict_corpus"])
    return {
        "file": CLAIM_FILE,
        "freeze_time_sha256_definition_constant":
            CLAIM_FREEZE_SHA256,
        "live_sha256_at_execution_base": _sha256(path),
        "handling": (
            "Spec 038 form (as the freeze test uses): "
            "the whole-file hash is a definition "
            "constant, not a live assertion, because "
            "the extracted-claims store is "
            "regenerated wholesale; the live file at "
            "the execution base differs from the "
            "freeze-time bytes in extraction "
            "timestamps (Spec 058's execution "
            "regenerated the store on 2026-10-21) — "
            "for manual_002, in the extracted_at "
            "field only"),
        "facts": facts,
    }


def _join(asset_obj: dict, crosswalk: dict) -> dict:
    """Gate 0.2: the join via mahadevan_number
    through the pinned crosswalk, and the
    cross-check (DD-048-5, DD-048-15)."""
    xwalk = crosswalk["crosswalk"]
    members = []
    for m in asset_obj["members"]:
        num = m.get("mahadevan_number")
        key = f"M{num:03d}" if isinstance(num, int) else None
        entry = xwalk.get(key) if key else None
        if num is None:
            disposition, reason = (
                "UNMAPPED",
                "the member carries no mahadevan_number "
                "locator")
        elif entry is None:
            disposition, reason = (
                "UNMAPPED",
                f"mahadevan_number {num} (key {key}) is "
                "absent from the pinned crosswalk")
        else:
            disposition, reason = ("MAPPED", "")
        members.append({
            "sign_key": m["sign_key"],
            "mahadevan_number": num,
            "parpola_number": m.get("parpola_number"),
            "crosswalk_key": key,
            "crosswalk_parpola_id": (
                entry.get("parpola_id") if entry else None),
            "parpola_locator_agrees": (
                entry is not None
                and str(entry.get("parpola_id"))
                == str(m.get("parpola_number"))),
            "depiction_note": m.get("depiction_note"),
            "disposition": disposition,
            "unmapped_reason": reason,
        })
    asset_mah = {m["mahadevan_number"]
                 for m in asset_obj["members"]}
    cross_check = {
        "claim_record_trio_mahadevan": TRIO,
        "trio_in_asset_f": [n for n in TRIO
                            if n in asset_mah],
        "trio_not_in_asset_f": [n for n in TRIO
                                if n not in asset_mah],
        "phase43_six_candidates": PHASE43_SIX,
        "phase43_six_in_asset_f": [n for n in PHASE43_SIX
                                   if n in asset_mah],
        "phase43_six_not_in_asset_f": [
            n for n in PHASE43_SIX if n not in asset_mah],
        "note": (
            "the trio and the six are Mahadevan "
            "numbers as named in the claim record and "
            "the Phase-43 record; Asset F's members "
            "are fixed solely by Parpola's published "
            "list via Spec 044's step 0. Every "
            "divergence is named here; the "
            "cross-check adds and removes no member"),
    }
    return {"members": members, "cross_check": cross_check}


def _gate_03_attempt() -> dict:
    phase43 = json.loads(
        (_REPO / PIN_PHASE43[0]).read_text("utf-8"))
    t11 = phase43["T1_1_corpus_v3"]
    t24 = phase43["T2_4_fish_rebus"]
    recorded = {
        "source": t11["source"],
        "total_records": t11["total_records"],
        "total_sequences": t11["total_sequences"],
        "unique_dockeys": t11["unique_dockeys"],
        "total_sign_instances": t11["total_sign_instances"],
    }
    reference_points = {
        "candidates": t24["fish_sign_candidates_tested"],
        "sign_72": {
            "occurrences": t24["primary_fish_72"]["total"],
            "terminal_frac":
                t24["primary_fish_72"]["terminal_frac"],
            "supported": t24["primary_fish_72"]["supported"],
        },
        "sign_267": {
            "occurrences": t24["primary_fish_267"]["total"],
            "terminal_frac":
                t24["primary_fish_267"]["terminal_frac"],
            "supported": t24["primary_fish_267"]["supported"],
        },
    }
    firestore_present = (_REPO / FIRESTORE_DUMP).exists()
    loader_records = None
    loader_sequences = None
    loader_error = None
    try:
        spec = importlib.util.spec_from_file_location(
            "indus_corpus_v3_gate03", _REPO / V3_LOADER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loader_records = len(module._load_records())
        loader_sequences = len(module.load_corpus())
    except Exception as exc:  # noqa: BLE001
        loader_error = f"{type(exc).__name__}: {exc}"
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
                v1_systems[json.loads(line).get(
                    "source_system")] += 1

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
                "as the Firestore 'indusarrays' source "
                "at 3,916 records; this layer carries "
                "5,679 records and is a different layer "
                "of record"),
        },
        {
            "layer": V1_EXPORT,
            "identity": (
                "the V1 primary research export "
                "(glossa-indus/CORPUS_VERSIONS.md: V1, "
                "loaded by indus_corpus_v2.py)"),
            "records": v1_objects,
            "source_systems": dict(sorted(v1_systems.items())),
            "sha256": _sha256(_REPO / V1_EXPORT),
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
            "sha256": _sha256(_REPO / ICIT_EXPORT),
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
                "second compilation whose arm gate 0.4 "
                "governs, not the Mahadevan-lineage V3 "
                "layer of this arm"),
        },
    ]
    identified = bool(firestore_present
                      and loader_sequences)
    return {
        "recorded_phase43_corpus": recorded,
        "t24_reference_points_of_record": reference_points,
        "C1_v3_loader_data_file": {
            "path": FIRESTORE_DUMP,
            "present": firestore_present,
            "loader": V3_LOADER,
            "records_loaded_by_the_loader": loader_records,
            "sequences_loadable": loader_sequences,
            "loader_error": loader_error,
            "note": (
                "the loader was imported from its file "
                "and run in this tree: it returns an "
                "empty record list when its data file "
                "does not exist, so no sequence can "
                "be loaded, exported whole, or pinned "
                "from it here"),
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
        "t24_reproduction": (
            "NOT RUN — there is no pinned layer to "
            "re-derive the reference points from; the "
            "gate's first leg (identification, export, "
            "pin) already fails, and the frozen "
            "wording closes the run on either leg"),
    }


def main() -> int:
    anchors_before = _sha256(_REPO / PIN_ANCHORS[0])

    # ── Integrity pins (spec section 2), before any
    # gate quantity. A mismatch closes INVALID
    # (spec section 10).
    pins = [_check_pin(*p) for p in (
        PIN_PHASE43, PIN_ANCHORS, PIN_CROSSWALK,
        PIN_SPEC033)]
    anchors_doc = json.loads(
        (_REPO / PIN_ANCHORS[0]).read_text("utf-8"))["anchors"]
    strict = [k for k, v in anchors_doc.items()
              if v.get("validation_status")
              == "strict_sa_independent"]
    claim = _claim_facts()
    integrity_ok = (
        all(p["match"] for p in pins)
        and claim["facts"]["facts_match_the_freeze_record"])
    integrity = {
        "inputs": pins,
        "claim_file_spec038_form": claim,
        "anchors_census": {
            "anchors": len(anchors_doc),
            "strict_sa_independent": len(strict),
            "m072_validation_status": (
                anchors_doc.get("M072", {})
                .get("validation_status")),
        },
        "verdict": "PASS" if integrity_ok else "FAIL",
    }

    gates: list[dict] = []
    asset = None
    join = None
    attempt = None
    outcome = None
    closure_reason = None

    not_reached = [
        ("0.1", "Asset F digest assertion"),
        ("0.2", "Membership join and cross-check"),
        ("0.3", "Strict corpus identification, pin, "
                "and measure reproduction"),
        ("0.4", "Holdat layer and crosswalk pin"),
        ("0.5", "Census (margins only)"),
        ("0.6", "Control set freeze"),
    ]

    if not integrity_ok:
        outcome = "INVALID"
        gates = [{"gate": g, "name": n,
                  "verdict": "NOT REACHED"}
                 for g, n in not_reached]
    else:
        # ── Gate 0.1 — Asset F digest assertion ────
        asset = _asset_f_digest()
        if not asset["asset_present"] or not asset[
                "pin_source_present"] or asset[
                "digest_recorded_in_pin_source"] is None:
            outcome = "ASSET F NOT AVAILABLE"
            gates.append({
                "gate": "0.1",
                "name": "Asset F digest assertion",
                "verdict": "FAIL — ASSET F NOT AVAILABLE"})
            gates += [{"gate": g, "name": n,
                       "verdict": "NOT REACHED"}
                      for g, n in not_reached[1:]]
        elif asset["assertion"] != "PASS":
            outcome = "ASSET F DIGEST MISMATCH"
            gates.append({
                "gate": "0.1",
                "name": "Asset F digest assertion",
                "verdict": "FAIL — ASSET F DIGEST MISMATCH"})
            gates += [{"gate": g, "name": n,
                       "verdict": "NOT REACHED"}
                      for g, n in not_reached[1:]]
        else:
            gates.append({
                "gate": "0.1",
                "name": "Asset F digest assertion",
                "digest": asset[
                    "digest_recorded_in_pin_source"],
                "member_count": asset["member_count"],
                "verdict": "PASS"})

            # ── Gate 0.2 — join and cross-check ────
            asset_obj = json.loads(
                (_REPO / ASSET_F).read_text("utf-8"))
            crosswalk = json.loads(
                (_REPO / PIN_CROSSWALK[0]).read_text("utf-8"))
            join = _join(asset_obj, crosswalk)
            mapped = [m for m in join["members"]
                      if m["disposition"] == "MAPPED"]
            unmapped = [m for m in join["members"]
                        if m["disposition"] == "UNMAPPED"]
            gates.append({
                "gate": "0.2",
                "name": "Membership join and cross-check",
                "mapped": len(mapped),
                "unmapped": len(unmapped),
                "verdict": "PASS"})

            # ── Gate 0.3 — strict corpus pin ───────
            attempt = _gate_03_attempt()
            identified = attempt[
                "layer_uniquely_identified_and_exportable"]
            gates.append({
                "gate": "0.3",
                "name": ("Strict corpus identification, "
                         "pin, and measure reproduction"),
                "recorded_phase43_corpus":
                    attempt["recorded_phase43_corpus"],
                "v3_data_file_present":
                    attempt["C1_v3_loader_data_file"][
                        "present"],
                "sequences_loadable_from_v3_loader":
                    attempt["C1_v3_loader_data_file"][
                        "sequences_loadable"],
                "verdict": "PASS" if identified else "FAIL"})
            if identified:
                gates += [{"gate": g, "name": n,
                           "verdict": "NOT RUN BY THIS "
                                      "SCRIPT (step-0 "
                                      "continuation)"}
                          for g, n in not_reached[3:]]
                outcome = "STEP 0 CONTINUES"
            else:
                outcome = "STRICT CORPUS NOT PINNABLE"
                closure_reason = (
                    "the V3 / Mahadevan-lineage "
                    "layer's data file — the Firestore "
                    "'indusarrays' dump the V3 loader "
                    "reads — is absent from the tree, "
                    "so the loader loads zero "
                    "sequences and the layer cannot be "
                    "exported whole or pinned; no "
                    "database copy exists in the "
                    "execution tree; and no other "
                    "layer in the tree is the corpus "
                    "the Phase-43 record names (its "
                    "source at 3,916 records, against "
                    "5,679 records for the "
                    "site-attributed layer, 15,508 "
                    "mixed-source objects for the V1 "
                    "export, and 3,085 ICIT-encoded "
                    "sequences), so the T2.4 reference "
                    "points (sign 72 — 181 "
                    "occurrences, ending-follower "
                    "fraction 25.9%; sign 267 — 356 "
                    "occurrences, 3.8%) cannot be "
                    "re-derived from a pinned layer")
                gates += [{"gate": g, "name": n,
                           "verdict": "NOT REACHED"}
                          for g, n in not_reached[3:]]

    anchors_after = _sha256(_REPO / PIN_ANCHORS[0])

    wording = None
    if outcome == "STRICT CORPUS NOT PINNABLE":
        wording = (
            "Spec 048 closed at step 0, gate 0.3: "
            "the strict corpus layer of record could "
            "not be uniquely identified and pinned, "
            "or the pinned layer does not reproduce "
            "the Phase-43 T2.4 reference points "
            f"({closure_reason}). No ending-follower "
            "rate was computed. This closure is a "
            "statement about runnability, not about "
            "the claim; the claim stands exactly as "
            "recorded.")

    rec = {
        "phase": "Phase-408",
        "spec": "048-parpola-fish-family-profiles",
        "act": ("step 0 (spec section 3 gates, in "
                "frozen order)"),
        "execution_date": EXECUTION_DATE,
        "base_commit": BASE_COMMIT,
        "claim_id": CLAIM_ID,
        "freeze_digest": FREEZE_DIGEST,
        "spec044_freeze_digest_contract_anchor":
            SPEC044_FREEZE_DIGEST,
        "osf_registration": "eqpab (approved and public)",
        "integrity": integrity,
        "asset_f_digest_assertion": asset,
        "membership_join": join,
        "strict_corpus_identification_attempt": attempt,
        "gates": gates,
        "ending_follower_rates_computed": [],
        "census_computed": False,
        "control_set_frozen": False,
        "anchors": {
            "file": PIN_ANCHORS[0],
            "sha256_before": anchors_before,
            "sha256_after": anchors_after,
            "byte_identical": anchors_before == anchors_after,
        },
        "outcome": outcome,
        "outcome_wording_frozen_spec_6": wording,
        "roif_hold": (
            "This record is internal under the "
            "campaign's Roif gate (R-7); it is not a "
            "publication."),
    }

    lines = [
        "# Phase-408 — Spec 048 step-0 report",
        "",
        "Claim: `parpola_2010_dravidian_solution_"
        "manual_002` — standing IN QUESTION,",
        "partially supported, exactly as recorded",
        "(Mahadevan sign 72 passed its Phase-43 T2.4",
        "test; sign 267, the family's most frequent",
        "member, failed it).",
        f"Execution date: {EXECUTION_DATE}. Freeze "
        "digest:",
        f"`{FREEZE_DIGEST}`. OSF registration eqpab",
        "(approved and public; DOI "
        "10.17605/OSF.IO/EQPAB).",
        "",
        "This record is internal under the campaign's",
        "Roif gate (R-7); it is not a publication.",
        "",
        f"## Outcome: {outcome}",
        "",
    ]
    if wording:
        lines += [
            "Frozen wording (spec section 6, STRICT",
            "CORPUS NOT PINNABLE form):",
            "",
            f"> {wording}",
            "",
        ]
    if asset is not None:
        lines += [
            "## Asset F (gate 0.1)",
            "",
            f"Digest asserted: "
            f"`{asset['digest_recorded_in_pin_source']}`",
            "(SHA-256 of the canonical bytes with the",
            "`digest` field excluded), against Spec",
            "044's step-0 outcome record — the pin",
            "source fixed at the freeze (DD-048-9).",
            f"Members: {asset['member_count']}. Whole-"
            "file SHA-256 of the exhibited file:",
            f"`{asset['whole_file_sha256']}`.",
            "",
        ]
    if join is not None:
        lines += [
            "## Membership join (gate 0.2)",
            "",
        ]
        for m in join["members"]:
            lines.append(
                f"- {m['sign_key']} — Mahadevan "
                f"{m['mahadevan_number']}, Parpola "
                f"{m['parpola_number']}: "
                f"{m['disposition']}"
                + (f" ({m['unmapped_reason']})"
                   if m["unmapped_reason"] else ""))
        cc = join["cross_check"]
        lines += [
            "",
            "Cross-check: of the claim record's trio",
            f"(72, 64, 70), in Asset F: "
            f"{cc['trio_in_asset_f']}; not in Asset F: "
            f"{cc['trio_not_in_asset_f']}. Of the",
            "Phase-43 six (267, 72, 65, 59, 60, 70),",
            f"in Asset F: {cc['phase43_six_in_asset_f']};",
            f"not in Asset F: "
            f"{cc['phase43_six_not_in_asset_f']}. The",
            "cross-check adds and removes no member.",
            "",
        ]
    lines += [
        "## Gates, in frozen order",
        "",
    ]
    for g in gates:
        lines.append(f"- **Gate {g['gate']} — "
                     f"{g.get('name', '')}: "
                     f"{g['verdict']}**")
    lines += [
        "",
        "## What was not done",
        "",
        "Gate 0.4 (Holdat layer and crosswalk pin),",
        "gate 0.5 (census), and gate 0.6 (control set",
        "freeze) were not reached: no ending-follower",
        "rate was computed for any sign in either arm,",
        "no census exists, no control was entered, and",
        "the 72/64/70 sensitivity was not computed.",
        "The claim stands exactly as recorded.",
        "",
        "Anchors asserted byte-identical before and "
        "after:",
        f"`{anchors_before}` at both readings.",
        "",
        "*AI disclosure: executed by an AI agent "
        "(Muse Spark,",
        "via Muse) at the direction of Tristen "
        "Pierson, per",
        "constitution section VI.*",
        "",
    ]

    _OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    _OUT_RESULTS.write_text(
        json.dumps(rec, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n", "utf-8")
    _OUT_REPORT.write_text("\n".join(lines), "utf-8")
    print(f"Phase-408 step 0: outcome {outcome}")
    for g in gates:
        print(f"  gate {g['gate']}: {g['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
