#!/usr/bin/env python3
"""Spec 083 (T008) — cloud image smoke test: assessor identity.

Run INSIDE the built image (CI job ``cloud-image-smoke``), or locally
in a venv as the equivalent proof:

    python backend/scripts/cloud_image_smoke.py

Checks (any failure exits non-zero and fails the image build's CI):

1. ``applied-epistemic-engineering`` resolves within the repo pin
   ``>=1.5.0,<1.6`` (backend/pyproject.toml).
2. The GAP-ENV 23-claim regression set scores exactly as expected,
   including the 0.1625 sign_val expectations.

Regression-set source — decided from repo evidence (2026-10-30):

* GAP-ENV (docs/governance/legc-gaps-2026-10-29.md) records that a
  runtime venv carrying AEE 1.0.4 — below the declared pin — can
  assess with the wrong engine; the Spec 083 route study adds that
  under AEE 1.0.4 vs 1.5.x, 16 of the 23 regression claims scored
  differently (0.0 vs 0.1625). The set itself is the Spec 029
  Phase I canonical set: the extracted records in
  ``glossa-indus/claims/extracted_claims`` deduplicate (Phase I,
  D-B) to exactly 23 canonical claims, which is what
  ``glossa_lab.aee_core.load_claims_from_dir`` loads (merged
  instances skipped) — pinned by
  ``backend/tests/test_spec029_phase_i.py``
  ("the scored set is the 23 canonical claims").
* Expectations live in
  ``backend/tests/fixtures/spec029_post_phase104_correction_aee150_scores.json``
  — NOT in the older ``spec029_post_merge_aee_scores.json``. The
  post-merge fixture is a preserved historical target, superseded
  twice: by the Phase-104 carry-over correction fixture, then by the
  AEE 1.5.0 adoption fixture (2026-10-20; methodology-2.0 semantics:
  FR-8.7 substance credit, FR-8.13 unrounded scores, widened dict
  shape). The live regression test
  (``test_spec029_phase_a.py::test_score_propagation_byte_identical_to_pre_change``)
  asserts byte-identical equality against the aee150 fixture under
  the pinned engine. Verified while writing this smoke: under AEE
  1.5.3 the live scores match the aee150 fixture 23/23 and mismatch
  the post-merge fixture 23/23 — using the post-merge fixture here
  would fail a conforming image.
* The spec's "0.1625 sign_val expectations" are the five
  ``*_sign_val_*`` claims' ``evidence`` score component: exactly
  0.1625 in the pre-1.5 fixtures; 0.16249999999999998 in the
  unrounded 1.5 shape. The smoke asserts the component within 1e-9
  of 0.1625 for every sign_val claim, on top of the full-fixture
  byte-equality check.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
_DEFAULT_FIXTURE = (
    _REPO_ROOT
    / "backend"
    / "tests"
    / "fixtures"
    / "spec029_post_phase104_correction_aee150_scores.json"
)
PIN_LOW = (1, 5, 0)
PIN_HIGH = (1, 6, 0)
SIGN_VAL_EVIDENCE = 0.1625


def _parse_version(text: str) -> tuple[int, ...]:
    parts = []
    for chunk in text.strip().split("."):
        digits = ""
        for ch in chunk:
            if ch.isdigit():
                digits += ch
            else:
                break
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--claims-dir", default=str(_DEFAULT_CLAIMS_DIR))
    parser.add_argument("--fixture", default=str(_DEFAULT_FIXTURE))
    args = parser.parse_args(argv)

    failures: list[str] = []

    # 1 — the assessor resolves inside the pin.
    try:
        version_text = importlib.metadata.version(
            "applied-epistemic-engineering"
        )
    except importlib.metadata.PackageNotFoundError:
        print("FAIL: applied-epistemic-engineering is not installed")
        return 1
    version = _parse_version(version_text)
    padded = (version + (0, 0, 0))[:3]
    if not (PIN_LOW <= padded < PIN_HIGH):
        failures.append(
            f"applied-epistemic-engineering {version_text} is outside "
            "the pin >=1.5.0,<1.6"
        )
    else:
        print(f"OK: applied-epistemic-engineering {version_text} within >=1.5.0,<1.6")

    # 2 — the GAP-ENV 23-claim regression set scores as expected.
    sys.path.insert(0, str(_REPO_ROOT / "backend"))
    from glossa_lab.aee_core import assessment_summary  # noqa: PLC0415

    expected = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    summary = assessment_summary(Path(args.claims_dir))
    if summary["total_claims"] != 23:
        failures.append(
            f"regression set holds {summary['total_claims']} claims, expected 23"
        )
    if summary["total_claims"] != len(expected):
        failures.append(
            f"claim count {summary['total_claims']} != fixture {len(expected)}"
        )

    sign_val_checked = 0
    for entry in summary["claims"]:
        claim_id = entry["claim_id"]
        want = expected.get(claim_id)
        if want is None:
            failures.append(f"{claim_id}: not in the expectation fixture")
            continue
        got = entry["aee_score"]
        if got != want or json.dumps(got, sort_keys=True) != json.dumps(
            want, sort_keys=True
        ):
            failures.append(f"{claim_id}: score diverges from the aee150 fixture")
        if "sign_val" in claim_id:
            sign_val_checked += 1
            evidence = (got or {}).get("components", {}).get("evidence")
            if evidence is None or abs(evidence - SIGN_VAL_EVIDENCE) > 1e-9:
                failures.append(
                    f"{claim_id}: evidence component {evidence!r} != 0.1625"
                )
    if sign_val_checked == 0:
        failures.append("no sign_val claims were checked for the 0.1625 expectation")
    else:
        print(
            f"OK: {sign_val_checked} sign_val claims carry the 0.1625 "
            "evidence-component expectation"
        )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(
        f"PASS: GAP-ENV regression set — {summary['total_claims']} claims "
        "byte-identical to the aee150 expectation fixture"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
