"""PRED-2026-010 — registration pins (2026-10-13).

The successor registration (docs/PREDICTION_REGISTER.md,
section 3) freezes, by hash, the training pool, the
filtered-pool manifest, the withheld file, and the
crosswalk, and enumerates the trained INITIAL set derived
at registration. These tests pin those values so any
drift in an input, in the derivation, or in the register
entry itself fails loudly instead of quietly changing
what the prediction is. The derivation they exercise
tokenises only the CISI Mohenjo-daro pool; the withheld
file is byte-hashed only, here as at registration.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

CORPUS_SHA256 = "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
POOL_MANIFEST_SHA256 = "ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a"
CROSSWALK_SHA256 = "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
WITHHELD_SHA256 = "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
REGISTERED_INITIAL = ["P000", "P217", "P324"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_derivation():
    spec = importlib.util.spec_from_file_location(
        "pred010_register_derivation",
        REPO / "backend" / "scripts" / "pred010_register_derivation.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_registered_input_hashes_unchanged():
    assert _sha256(REPO / "data" / "normalized" / "corpus_master.csv") == CORPUS_SHA256
    assert (
        _sha256(REPO / "data" / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv")
        == CROSSWALK_SHA256
    )
    assert (
        _sha256(REPO / "backend" / "glossa_lab" / "data" / "yajnadevam_inscriptions.csv")
        == WITHHELD_SHA256
    )


def test_derivation_reproduces_the_registered_set():
    record = _load_derivation().derive()
    pool = record["training_pool"]
    assert pool["pool_rows"] == 179
    assert pool["pool_sites"] == {"Mohenjo-daro": 179}
    assert pool["yajnadevam_rows_in_pool"] == 0
    assert pool["file_sha256"] == CORPUS_SHA256
    assert pool["pool_manifest_sha256"] == POOL_MANIFEST_SHA256
    result = record["result"]
    assert result["classifiable_signs"] == 28
    assert result["trained_initial_set"] == REGISTERED_INITIAL
    committed = json.loads(
        (REPO / "reports" / "pred010_derivation_record.json").read_text("utf-8")
    )
    assert committed["result"]["trained_initial_set"] == REGISTERED_INITIAL
    assert committed["training_pool"]["pool_manifest_sha256"] == POOL_MANIFEST_SHA256


def test_register_carries_the_pred010_entry():
    text = (REPO / "docs" / "PREDICTION_REGISTER.md").read_text("utf-8")
    assert "### PRED-2026-010" in text
    assert "P000, P217, P324" in text
    assert "https://osf.io/wjebq/" in text
    assert POOL_MANIFEST_SHA256 in text
