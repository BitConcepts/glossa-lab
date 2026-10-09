"""Tests for the Phase-132 (spec 023) pilot frame draw.

Synthetic-catalogue tests exercise the frozen rule deterministically;
the committed-frame tests validate the published pilot frame copy at
data/keyed_transcription/phase132_pilot_frame.json.
"""

import csv
import importlib.util
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "backend" / "scripts" / "phase132_frame.py"
COMMITTED_FRAME = REPO / "data" / "keyed_transcription" / \
    "phase132_pilot_frame.json"

spec = importlib.util.spec_from_file_location("phase132_frame", SCRIPT)
frame_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frame_mod)

HEADER = ["volume", "cisi_id", "photo_key", "side", "bis", "caption_raw",
          "caption_ocr_score", "pdf_page", "printed_page", "site",
          "object_type", "motif_chapter", "scale_pct", "collection_scope",
          "material", "material_basis", "dimensions", "dimensions_basis",
          "photo_box_xywh", "extraction_basis", "confidence", "notes"]


def _row(volume, cisi_id, page, site, otype, box="0;0;10;10"):
    return {"volume": str(volume), "cisi_id": cisi_id,
            "photo_key": f"{cisi_id} A", "side": "A", "bis": "",
            "caption_raw": "", "caption_ocr_score": "", "pdf_page": str(page),
            "printed_page": "", "site": site, "object_type": otype,
            "motif_chapter": "", "scale_pct": "", "collection_scope": "",
            "material": "", "material_basis": "", "dimensions": "",
            "dimensions_basis": "", "photo_box_xywh": box,
            "extraction_basis": "", "confidence": "", "notes": ""}


def _write_store(tmp_path, vol1_rows, vol2_rows):
    store = tmp_path / "store"
    (store / "catalogue").mkdir(parents=True)
    for vol, rows in ((1, vol1_rows), (2, vol2_rows)):
        with open(store / "catalogue" / f"cisi_vol{vol}_catalogue.csv",
                  "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=HEADER)
            w.writeheader()
            w.writerows(rows)
    return store


def _synthetic(tmp_path):
    """Pools comfortably above quota in every stratum."""
    v1, v2 = [], []
    # Mohenjo-Daro: M-1..M-60 (vol1); mayig overlap M-1..M-12
    for i in range(1, 61):
        v1.append(_row(1, f"M-{i}", 100 + i, "Mohenjo-Daro", "Seals"))
    # Harappa: H-1..H-40 (vol1)
    for i in range(1, 41):
        v1.append(_row(1, f"H-{i}", 300 + i, "Harappa", "Tablets"))
    # Lothal L-1..L-20, Kalibangan K-1..K-20 (vol1)
    for i in range(1, 21):
        v1.append(_row(1, f"L-{i}", 500 + i, "Lothal", "Seals"))
        v1.append(_row(1, f"K-{i}", 600 + i, "Kalibangan", "Tablets"))
    # Excluded rows: empty site, Addenda site, Graffiti type
    v1.append(_row(1, "M-900", 700, "", "Seals"))
    v1.append(_row(1, "M-901", 701, "Addenda", "Seals"))
    v1.append(_row(1, "M-902", 702, "Mohenjo-Daro", "Graffiti"))
    store = _write_store(tmp_path, v1, v2)
    layer = {"inscriptions": [
        {"cisi_object_id": f"M-{i}"} for i in range(1, 13)] + [
        {"cisi_object_id": "M-9999"},          # unresolved
        {"cisi_object_id": "M-900"},           # resolves, but excluded obj
    ]}
    layer_path = tmp_path / "layer.json"
    layer_path.write_text(json.dumps(layer))
    return store, layer_path


def test_determinism(tmp_path):
    store, layer_path = _synthetic(tmp_path)
    a = frame_mod.build_frame(store, layer_path)
    b = frame_mod.build_frame(store, layer_path)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_quotas_and_exclusions(tmp_path):
    store, layer_path = _synthetic(tmp_path)
    doc = frame_mod.build_frame(store, layer_path)
    frame = doc["frame"]
    assert len(frame) == 50
    sites = {}
    for o in frame:
        sites[o["site"]] = sites.get(o["site"], 0) + 1
    assert sites == {"Mohenjo-Daro": 25, "Harappa": 15,
                     "Lothal": 6, "Kalibangan": 4}
    keys = {o["cisi_id"] for o in frame}
    assert "M-900" not in keys and "M-901" not in keys
    assert "M-902" not in keys  # Graffiti excluded
    assert all(o["site"] not in ("", "Addenda") for o in frame)
    assert all(o["object_type"] != "Graffiti" for o in frame)


def test_mayig_subquota_and_resolution_report(tmp_path):
    store, layer_path = _synthetic(tmp_path)
    doc = frame_mod.build_frame(store, layer_path)
    # All synthetic overlap objects are Mohenjo-Daro, so only that
    # stratum can fill its mayig sub-quota (5); the others record a
    # shortfall drawn from their (empty) overlap pools.
    mayig = [o for o in doc["frame"] if o["mayig_overlap"]]
    assert len(mayig) == 5
    assert all(o["site"] == "Mohenjo-Daro" for o in mayig)
    rep = doc["frame_summary"]["mayig_resolution"]
    assert rep["n_layer_inscriptions"] == 14
    assert rep["n_unresolved"] == 1
    assert rep["unresolved_printed_ids"] == ["M-9999"]
    assert rep["n_ambiguous"] == 0


def test_key_format_gold_and_uniqueness(tmp_path):
    store, layer_path = _synthetic(tmp_path)
    doc = frame_mod.build_frame(store, layer_path)
    frame = doc["frame"]
    pat = re.compile(r"^cisi:v[12]:.+")
    assert all(pat.match(o["canonical_key"]) for o in frame)
    assert len({o["canonical_key"] for o in frame}) == len(frame)
    gold = [o for o in frame if o["gold"]]
    assert len(gold) == 10
    assert doc["frame_summary"]["gold_keys"] == \
        [o["canonical_key"] for o in frame if o["gold"]] or \
        set(doc["frame_summary"]["gold_keys"]) == \
        {o["canonical_key"] for o in gold}
    assert doc["frame_summary"]["seed"] == 20261009


def _walk(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)
    elif isinstance(obj, str):
        yield obj


def test_no_holdat_fields_anywhere(tmp_path):
    store, layer_path = _synthetic(tmp_path)
    doc = frame_mod.build_frame(store, layer_path)
    for token in _walk(doc):
        assert "holdat" not in str(token).lower()
    if COMMITTED_FRAME.exists():
        raw = COMMITTED_FRAME.read_text(encoding="utf-8")
        assert "holdat" not in raw.lower()


def test_committed_frame_shape():
    if not COMMITTED_FRAME.exists():
        return  # frame not yet drawn in this checkout
    doc = json.loads(COMMITTED_FRAME.read_text(encoding="utf-8"))
    frame = doc["frame"]
    assert len(frame) == 50
    assert len({o["canonical_key"] for o in frame}) == 50
    assert sum(1 for o in frame if o["gold"]) == 10
    sites = {}
    for o in frame:
        sites[o["site"]] = sites.get(o["site"], 0) + 1
    assert sites["Mohenjo-Daro"] == 25
    assert sites["Harappa"] == 15
    assert sites["Lothal"] + sites["Kalibangan"] == 10
    for o in frame:
        assert o["canonical_key"] == \
            f"cisi:v{o['volume']}:{o['cisi_id']}"
        for p in o["photos"]:
            assert set(p) == {"photo_key", "side", "bis", "pdf_page",
                              "printed_page", "photo_box_xywh"}
