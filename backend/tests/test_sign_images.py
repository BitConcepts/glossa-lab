"""Tests for the sign image processor pipeline.

Covers: manifest rebuild, triple-check verification, iconic fallback
generation, and new-source discovery.

Requires: opencv-python (cv2). The sign image processor uses OpenCV for
image processing. These tests are skipped automatically in CI environments
where cv2 is not installed. Install with: pip install opencv-python
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest import mock

import numpy as np
import pytest
from PIL import Image

# Skip the entire module if OpenCV is not installed.
# cv2 is an optional dependency used only for sign image processing.
pytest.importorskip("cv2", reason="cv2 (OpenCV) not installed — install opencv-python to run sign image tests")

# ── Helpers ────────────────────────────────────────────────────────────────


def _create_test_png(path: Path, *, fill: int = 255, ink_pct: float = 0.10) -> None:
    """Create a test PNG with controlled ink density."""
    size = 128
    img = np.full((size, size), fill, dtype=np.uint8)
    # Add some black pixels for ink
    n_black = int(size * size * ink_pct)
    if n_black > 0:
        rng = np.random.default_rng(42)
        coords = rng.choice(size * size, size=min(n_black, size * size), replace=False)
        for c in coords:
            img[c // size, c % size] = 0
    Image.fromarray(img, mode="L").save(str(path))


@pytest.fixture()
def signs_dir(tmp_path: Path):
    """Set up a temporary signs directory with test PNGs and a manifest."""
    signs = tmp_path / "static" / "signs"
    signs.mkdir(parents=True)
    (signs / "originals").mkdir()

    # Create 5 test sign PNGs with valid ink density
    for i in range(1, 6):
        sid = f"M{i:03d}"
        _create_test_png(signs / f"{sid}.png", ink_pct=0.08)

    # Create a manifest that's missing some entries
    manifest = {
        "M001": {
            "status": "ok",
            "source": "fallback_icon",
            "processed_path": "static\\signs\\M001.png",
            "original_path": None,
            "timestamp": "2026-06-08T09:05:49Z",
        },
        # M002-M005 intentionally missing from manifest
    }
    (signs / "manifest.json").write_text(json.dumps(manifest, indent=2))

    # Create an anchors file so the catalog is populated
    reports = tmp_path / "reports"
    reports.mkdir()
    anchors: dict[str, Any] = {"anchors": {}}
    for i in range(1, 6):
        sid = f"M{i:03d}"
        anchors["anchors"][sid] = {
            "reading": f"test_{i}",
            "confidence": "HIGH",
            "source": "test",
        }
    (reports / "INDUS_FINAL_ANCHORS.json").write_text(json.dumps(anchors))

    return tmp_path


# ── Tests ──────────────────────────────────────────────────────────────────


class TestRebuildManifest:
    """test_manifest_rebuilt: after rebuild_manifest(), all existing PNGs
    in static/signs/ have status='ok' in manifest."""

    def test_manifest_rebuilt(self, signs_dir: Path) -> None:
        from glossa_lab.tools import sign_image_processor as sip

        # Patch the module-level paths
        with (
            mock.patch.object(sip, "_BACKEND_DIR", signs_dir),
            mock.patch.object(sip, "_STATIC_SIGNS", signs_dir / "static" / "signs"),
            mock.patch.object(sip, "_ORIGINALS_DIR", signs_dir / "static" / "signs" / "originals"),
            mock.patch.object(sip, "_MANIFEST_PATH", signs_dir / "static" / "signs" / "manifest.json"),
        ):
            result = sip.rebuild_manifest()

        assert result["reconciled"] >= 4  # M002-M005 were missing
        assert result["already_ok"] >= 1  # M001 was already ok

        # Verify all 5 signs are now in the manifest with status=ok
        manifest = json.loads(
            (signs_dir / "static" / "signs" / "manifest.json").read_text()
        )
        for i in range(1, 6):
            sid = f"M{i:03d}"
            assert sid in manifest, f"{sid} missing from manifest"
            assert manifest[sid]["status"] == "ok", f"{sid} status is not ok"
            assert manifest[sid]["processed_path"] is not None


class TestTripleCheck:
    """test_triple_check_all_pass: after full pipeline, verify_sign_images()
    returns 0 failed."""

    def test_all_pass_when_valid(self, signs_dir: Path) -> None:
        from glossa_lab.tools import sign_image_processor as sip

        with (
            mock.patch.object(sip, "_BACKEND_DIR", signs_dir),
            mock.patch.object(sip, "_STATIC_SIGNS", signs_dir / "static" / "signs"),
            mock.patch.object(sip, "_ORIGINALS_DIR", signs_dir / "static" / "signs" / "originals"),
            mock.patch.object(sip, "_MANIFEST_PATH", signs_dir / "static" / "signs" / "manifest.json"),
            mock.patch.object(sip, "_ANCHORS_PATH", signs_dir / "reports" / "INDUS_FINAL_ANCHORS.json"),
            mock.patch.object(sip, "_CROSSWALK_PATH", signs_dir / "crosswalk.json"),
        ):
            # Rebuild first so manifest is correct
            sip.rebuild_manifest()
            # Now verify — force=True skips staleness check
            result = sip.verify_sign_images(force=True)

        assert result["failed"] == 0, f"Expected 0 failures, got: {result['failures']}"
        assert result["passed"] == 5

    def test_detects_missing_file(self, signs_dir: Path) -> None:
        from glossa_lab.tools import sign_image_processor as sip

        # Remove one PNG
        (signs_dir / "static" / "signs" / "M003.png").unlink()

        with (
            mock.patch.object(sip, "_BACKEND_DIR", signs_dir),
            mock.patch.object(sip, "_STATIC_SIGNS", signs_dir / "static" / "signs"),
            mock.patch.object(sip, "_ORIGINALS_DIR", signs_dir / "static" / "signs" / "originals"),
            mock.patch.object(sip, "_MANIFEST_PATH", signs_dir / "static" / "signs" / "manifest.json"),
            mock.patch.object(sip, "_ANCHORS_PATH", signs_dir / "reports" / "INDUS_FINAL_ANCHORS.json"),
            mock.patch.object(sip, "_CROSSWALK_PATH", signs_dir / "crosswalk.json"),
        ):
            sip.rebuild_manifest()
            result = sip.verify_sign_images(force=True)

        assert result["failed"] >= 1
        failed_ids = [f["sign_id"] for f in result["failures"]]
        assert "M003" in failed_ids


class TestIconicFallback:
    """test_iconic_fallback_always_produces_image: every sign_id produces
    a non-empty PNG via the iconic fallback path."""

    @pytest.mark.parametrize(
        "iconic",
        [
            "fish",
            "fish with roof",
            "zebu bull",
            "man",
            "elephant",
            "gharial",
            "jar",
            "cross",
            "circle",
            "dotted circle",
            "3 strokes",
            "unicorn",
            "",  # empty description → label fallback
            "unknown_thing_xyz",  # unknown → label fallback
        ],
    )
    def test_fallback_produces_valid_image(self, iconic: str) -> None:
        from glossa_lab.tools.sign_image_processor import generate_fallback_icon

        result = generate_fallback_icon("M999", iconic)

        assert isinstance(result, np.ndarray)
        assert result.shape == (128, 128)
        # Should have at least some black pixels (not all white)
        assert np.sum(result < 128) > 0, f"Fallback for '{iconic}' produced blank image"
        # Should not be all black
        assert np.sum(result >= 128) > 0, f"Fallback for '{iconic}' produced solid black"


class TestDiscovery:
    """test_new_sources_discovered: find_missing_signs() returns results."""

    def test_returns_dict(self) -> None:
        from glossa_lab.tools import sign_image_processor as sip

        # Mock network calls to avoid actual HTTP requests in tests
        with mock.patch.object(sip, "_wm_request", return_value=None):
            result = sip.find_missing_signs()

        assert isinstance(result, dict)

    def test_with_mock_wikimedia_category(self) -> None:
        from glossa_lab.tools import sign_image_processor as sip

        mock_response = json.dumps({
            "query": {
                "categorymembers": [
                    {"title": "File:Indus_script_sign_047.svg", "pageid": 123},
                    {"title": "File:Indus_sign_100.png", "pageid": 456},
                ]
            }
        }).encode()

        with mock.patch.object(sip, "_wm_request", return_value=mock_response):
            result = sip.find_missing_signs()

        # Should have found at least M047 and M100
        assert len(result) > 0
        # Check that sign IDs were extracted
        all_ids = list(result.keys())
        assert any("M047" in sid for sid in all_ids) or any("M100" in sid for sid in all_ids)


class TestValidatePng:
    """Tests for the PNG validation function."""

    def test_valid_png(self, tmp_path: Path) -> None:
        from glossa_lab.tools.sign_image_processor import validate_png

        p = tmp_path / "good.png"
        _create_test_png(p, ink_pct=0.10)
        assert validate_png(p) is True

    def test_blank_png(self, tmp_path: Path) -> None:
        from glossa_lab.tools.sign_image_processor import validate_png

        p = tmp_path / "blank.png"
        _create_test_png(p, ink_pct=0.0)
        assert validate_png(p) is False

    def test_missing_file(self, tmp_path: Path) -> None:
        from glossa_lab.tools.sign_image_processor import validate_png

        assert validate_png(tmp_path / "nope.png") is False

    def test_overfilled_png(self, tmp_path: Path) -> None:
        from glossa_lab.tools.sign_image_processor import validate_png

        p = tmp_path / "filled.png"
        _create_test_png(p, fill=0, ink_pct=0.0)  # all black
        assert validate_png(p) is False
