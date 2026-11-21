"""M222 public anchor table must carry the canonical register value.

Requirement (transcription correction, 2026-11-21): the program's
canonical register records sign M222's reading as "min" (MEDIUM;
source anchor_staging_archive:compound_semantic_coherence; retained
under the Phase-109 re-review on crosswalk v2.1 Parpola support; see
reports/phase110_m222_dossier.json, m222_min_record, and
specs/086-winning-combination-adoption/stage-4-record.md). The public
anchor tables previously listed the superseded Phase-87 value "kur"
for M222 itself. The derived Phase-111 rows of other signs are
historical records of that run and are out of scope here.

Test case: every public anchor table surface under research/indus
gives M222 the register value.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER_READING = "min"
REGISTER_CONFIDENCE = "MEDIUM"


def _csv_m222(path):
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["Sign"] == "M222":
                return row
    raise AssertionError(f"M222 row missing in {path}")


def test_anchor_table_csv_m222_matches_register():
    row = _csv_m222(ROOT / "research/indus/anchor_table.csv")
    assert row["Reading"] == REGISTER_READING
    assert row["Confidence"] == REGISTER_CONFIDENCE


def test_anchor_model_public_csv_m222_matches_register():
    row = _csv_m222(
        ROOT
        / "research/indus/indus-anchor-model/data/public/anchor_table_397.csv"
    )
    assert row["Reading"] == REGISTER_READING
    assert row["Confidence"] == REGISTER_CONFIDENCE


def test_anchor_table_json_m222_matches_register():
    data = json.loads(
        (ROOT / "research/indus/anchor_table.json").read_text(encoding="utf-8")
    )
    entry = data["anchors"]["M222"]
    assert entry["reading"] == REGISTER_READING
    assert entry["confidence"] == REGISTER_CONFIDENCE
