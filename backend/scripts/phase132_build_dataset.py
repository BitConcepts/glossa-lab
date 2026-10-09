#!/usr/bin/env python3
"""Phase-132 (spec 023, FROZEN) — pilot dataset assembly.

Assembles the Stage P pilot dataset (intake schema v1,
dataset class image_transcription) from the adjudication
records in the local store
(corpora/downloads/cisi_image_layer/phase132_pilot/), then
runs the Phase-130 intake pipeline on it: validate_dataset
(must produce no errors; warnings captured), assign_evaluability,
and run_intake with the Phase-130 sign-classes map
(glossa_lab.pred_harness.load_sign_classes over
data/crosswalks/sign_inventory.csv — the calling pattern of
backend/tests/test_phase130_intake_pack.py), which applies
the shared spec-018 dedup module and the harness DRY-RUN
path only.

Record rules (spec 023 sections 4-6 + the Phase-132 tasking):
- One record per CISI object (volume-scoped printed ID);
  the canonical key is the inscription_id.
- The token sequence is the object's final adjudicated
  sequence: the three-pass adjudicated sequence (s3_tokens)
  for gold objects, else the two-pass adjudicated sequence
  (s2_tokens). Tokens are P-space primary values derived via
  crosswalk v1 (phase132_metrics.derive_token): the primary
  P counterpart, the literal "UNK", or the placeholder
  "UNMAPPED:<M_ID>" for a token whose M has no crosswalk row
  (its p_id is null in tokens_detail; no P ID is invented).
- Ambiguity-log objects (adjudication record ambiguity_log
  true) are excluded from the dataset and counted. The pilot
  frame contains none, but the rule is implemented.
- object_type is the frame value verbatim; the field is
  omitted when the frame value is the empty string (schema:
  object_type is optional).

Outputs (committed; the pass/adjudication JSONs themselves
stay in the local store):
- data/keyed_transcription/phase132_pilot_dataset_v1.json
- data/keyed_transcription/phase132_pilot_dataset_v1_meta.json
  (content hash, crosswalk hash, validation verdict +
  warnings, evaluability assignment, dedup counts, intake
  outcome — counts and verdicts only, no pass content).

Deterministic: no randomness, no wall-clock in the outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import phase132_metrics as pm  # noqa: E402
from glossa_lab.intake import (  # noqa: E402
    _content_hash, assign_evaluability, run_intake, validate_dataset,
)
from glossa_lab.pred_harness import load_sign_classes  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE = pm.DEFAULT_STORE
DATASET_OUT = REPO_ROOT / "data" / "keyed_transcription" / \
    "phase132_pilot_dataset_v1.json"
META_OUT = REPO_ROOT / "data" / "keyed_transcription" / \
    "phase132_pilot_dataset_v1_meta.json"
INVENTORY = REPO_ROOT / "data" / "crosswalks" / "sign_inventory.csv"

DATASET_NAME = "phase132_keyed_transcription_pilot_v1"
SIGN_LIST_DETAIL = (
    "Tokens transcribed by glyph match against Mahadevan 1977 "
    "sign-list drawings (backend/static/signs, source m77_pdf); "
    "P IDs derived via crosswalk v1 primary map (freeze block "
    "§5.6); crosswalk content sha256 recorded in dataset meta.")


def build_dataset(store: Path) -> tuple[dict, dict]:
    """Returns (dataset, build_info)."""
    crosswalk_bytes = pm.CROSSWALK_PATH.read_bytes()
    crosswalk = json.loads(crosswalk_bytes)
    crosswalk_sha = hashlib.sha256(crosswalk_bytes).hexdigest()
    m_to_p = pm.build_m_to_p(crosswalk["rows"])
    data = pm.load_store(store)
    frame_by_key = {e["canonical_key"]: e for e in data["frame"]}

    inscriptions = []
    excluded_ambiguity = []
    n_gold_final_from_s3 = 0
    for key in data["keys"]:
        adj = data["adjudication"][key]
        if adj.get("ambiguity_log"):
            excluded_ambiguity.append(
                {"key": key, "reason": adj.get("ambiguity_reason")})
            continue
        frame = frame_by_key[key]
        volume = frame["volume"]
        if "s3_tokens" in adj:
            source_field = "s3_tokens"
            n_gold_final_from_s3 += 1
        else:
            source_field = "s2_tokens"
        token_records = sorted(adj[source_field],
                               key=lambda t: t["position"])
        tokens, tokens_detail = [], []
        for t in token_records:
            d = pm.derive_token(t["m_id"], m_to_p)
            tokens.append(d["p_value"])
            tokens_detail.append({
                "position": t["position"],
                "photo_key": t["photo_key"],
                "m_id": t["m_id"],
                "p_id": d["p_id"],
                "legibility": t["legibility"],
                "crosswalk_conflict": d["crosswalk_conflict"],
                "crosswalk_unmapped": d["crosswalk_unmapped"],
                "crosswalk_candidates": d["candidates"],
            })
        # Provenance source reference from the frame photo rows
        # for the photos actually transcribed (adjudication
        # record), in transcription order.
        photo_rows = {p["photo_key"]: p for p in frame["photos"]}
        printed_pages, pdf_pages = [], []
        for pk in adj["photos_transcribed"]:
            row = photo_rows[pk]
            pp = row["printed_page"] or "n/a"
            if pp not in printed_pages:
                printed_pages.append(pp)
            if row["pdf_page"] not in pdf_pages:
                pdf_pages.append(row["pdf_page"])
        source_reference = (
            f"CISI v{volume} printed p. {', '.join(printed_pages)} / "
            f"PDF p. {', '.join(str(p) for p in pdf_pages)} / "
            f"photos {', '.join(adj['photos_transcribed'])}")
        ins = {
            "inscription_id": key,
            "site": frame["site"],
            "sign_list": "parpola_1982",
            "sign_list_detail": SIGN_LIST_DETAIL,
            "tokens": tokens,
            "tokens_detail": tokens_detail,
            "partial": adj["partial"],
            "damage_notes": adj["damage_notes"],
            "orientation_basis": adj["orientation_basis"],
            "provenance": {
                "source_reference": source_reference,
                "object_id": frame["cisi_id"],
                "image_ref": "local-store:corpora/downloads/"
                             "cisi_image_layer/phase132_pilot/"
                             f"objects/{key}",
                "transcriber": "pass_a+pass_b+adjudicator (AI agents, "
                               "role-isolated blinded instances; "
                               "spec 023 §5.5)",
                "transcription_date": "2026-10-09",
            },
        }
        if frame["object_type"]:
            ins["object_type"] = frame["object_type"]
        inscriptions.append(ins)

    dataset = {
        "schema_version": "1.0",
        "dataset_name": DATASET_NAME,
        "source": "CISI Vols. 1–2 plate photographs, local research "
                  "copies (corpora/downloads/cisi_image_layer)",
        "source_class": "image_transcription",
        "license_basis": "Transcription facts (sign sequences + "
                         "printed metadata) produced by this program "
                         "from in-copyright local research copies of "
                         "CISI Vol. 1 (Joshi & Parpola 1987) and "
                         "Vol. 2 (Shah & Parpola 1991); dataset "
                         "published CC BY 4.0 per owner adjudication "
                         "2026-10-09 (spec 023 §11 ask 4); plate "
                         "images are never published.",
        "acquisition_date": "2026-10-09",
        "compiler": "Glossa Lab Phase-132 (spec 023)",
        "text_rule": "Impression-primary orientation (spec 023 §5.1, "
                     "owner value at freeze); seal-face sequence is "
                     "the derived reversal.",
        "unit_rule": "One record per CISI object (volume-scoped "
                     "printed ID); multi-face objects concatenate "
                     "inscribed faces in A-then-B order with "
                     "per-token photo attribution.",
        "upstream_lineage": {
            "derived_from": "Original transcription from CISI plate "
                            "photographs",
            "is_derivation_input": False,
            "notes": "Not derived from Holdat, ICIT, or the mayig "
                     "layer; passes were blinded (spec 023 §5.5). "
                     "Sign identifications use the published "
                     "Mahadevan/Parpola lists (spec 023 §8 limits "
                     "apply).",
        },
        "crosswalk": {
            "version": "v1",
            "path": "data/crosswalks/parpola_mahadevan_crosswalk_v1.json",
            "sha256": crosswalk_sha,
        },
        "inscriptions": inscriptions,
    }
    build_info = {"excluded_ambiguity_log": excluded_ambiguity,
                  "n_gold_records_from_s3": n_gold_final_from_s3,
                  "crosswalk_sha256": crosswalk_sha}
    return dataset, build_info


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--store", type=Path, default=DEFAULT_STORE)
    ap.add_argument("--dataset-out", type=Path, default=DATASET_OUT)
    ap.add_argument("--meta-out", type=Path, default=META_OUT)
    args = ap.parse_args(argv)

    dataset, build_info = build_dataset(args.store)
    validation = validate_dataset(dataset)
    assert not validation["errors"], \
        f"validator errors: {validation['errors']}"
    evaluability = assign_evaluability(dataset)
    classes = load_sign_classes(INVENTORY)
    intake_report = run_intake(dataset, classes)
    assert intake_report["outcome"] == "intake-complete-dry-run-only", \
        intake_report["outcome"]
    content_hash = _content_hash(dataset)
    assert intake_report["dataset_content_hash"] == content_hash

    args.dataset_out.parent.mkdir(parents=True, exist_ok=True)
    args.dataset_out.write_text(
        json.dumps(dataset, indent=2, ensure_ascii=False) + "\n", "utf-8")
    meta = {
        "dataset_name": DATASET_NAME,
        "dataset_file": "data/keyed_transcription/"
                        "phase132_pilot_dataset_v1.json",
        "dataset_content_hash": content_hash,
        "hash_method": "glossa_lab.intake._content_hash: sha256 of "
                       "canonical JSON (sort_keys, ensure_ascii=False)",
        "crosswalk": {
            "path": "data/crosswalks/parpola_mahadevan_crosswalk_v1.json",
            "sha256": build_info["crosswalk_sha256"],
        },
        "source_class_registration": {DATASET_NAME: "image_transcription"},
        "token_sequence_rule": "final adjudicated sequence per object "
                               "(s3_tokens for gold objects, else "
                               "s2_tokens), P-space primary values via "
                               "crosswalk v1; UNK literal; "
                               "crosswalk-unmapped tokens carried as "
                               "UNMAPPED:<M_ID> with p_id null in "
                               "tokens_detail",
        "n_inscriptions": len(dataset["inscriptions"]),
        "n_tokens": sum(len(i["tokens"]) for i in dataset["inscriptions"]),
        "n_gold_records_from_s3": build_info["n_gold_records_from_s3"],
        "excluded_ambiguity_log": build_info["excluded_ambiguity_log"],
        "validation": validation,
        "evaluability": evaluability,
        "dedup": intake_report["stages"]["dedup"],
        "intake": {
            "outcome": intake_report["outcome"],
            "license_gate": intake_report["stages"]["license_gate"],
            "label": intake_report.get("label"),
            "harness_dry_run_dedup":
                intake_report["stages"]["harness_dry_run"].get("dedup"),
        },
    }
    args.meta_out.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"Phase-132 pilot dataset -> {args.dataset_out}")
    print(f"  inscriptions: {meta['n_inscriptions']}  tokens: "
          f"{meta['n_tokens']}  excluded (ambiguity log): "
          f"{len(build_info['excluded_ambiguity_log'])}")
    print(f"  validation: {validation['verdict']} "
          f"(errors={len(validation['errors'])}, "
          f"warnings={len(validation['warnings'])})")
    print(f"  dedup: {meta['dedup']}")
    print(f"  intake outcome: {meta['intake']['outcome']}  "
          f"license gate: {meta['intake']['license_gate']}")
    print(f"  content hash: {content_hash}")
    print(f"  meta -> {args.meta_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
