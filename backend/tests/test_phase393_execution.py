"""Spec 028 execution fences (Phase-393).

Pins: (1) the execution script asserts the frozen input
hashes; (2) the script's pipeline section is a verbatim
copy of the freeze-time pipeline module's pipeline section
(shared implementation between calibration and execution);
(3) the Phase-393 graph node is registered.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "backend/scripts/phase393_harappa_robustness.py"
PIPELINE = REPO / "specs/028-harappa-robustness/pipeline393.py"

FROZEN_INPUT_SHA256 = {
    "icit_converted_v2_keyed.json":
        "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
    "horus_inscriptions.csv":
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
}


def test_script_asserts_frozen_input_hashes():
    text = SCRIPT.read_text(encoding="utf-8")
    for name, digest in FROZEN_INPUT_SHA256.items():
        assert name in text and digest in text


def test_pipeline_section_is_verbatim():
    script = SCRIPT.read_text(encoding="utf-8")
    lines = PIPELINE.read_text(encoding="utf-8").split("\n")
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith("ALPHA = 0.05"))
    want = "\n".join(lines[start:]).strip()
    begin = script.index("# === FROZEN PIPELINE BEGIN")
    end = script.index("# === FROZEN PIPELINE END ===")
    section = script[script.index("\n", begin) + 1:end].strip()
    assert section == want


def test_phase393_node_registered():
    from glossa_lab.experiment_graph import ATOMIC_NODES

    assert "IndusPhase393HarappaRobustness" in ATOMIC_NODES
