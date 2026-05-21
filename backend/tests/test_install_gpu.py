"""Tests for GPU installer logic (TEST-GPU-001..010).

TEST-GPU-001  _cupy_package_for_cuda returns correct package for CUDA 11.
TEST-GPU-002  _cupy_package_for_cuda returns correct package for CUDA 12.
TEST-GPU-003  _cupy_package_for_cuda returns correct package for CUDA 13.
TEST-GPU-004  _cupy_package_for_cuda fallback chain for unknown CUDA version.
TEST-GPU-005  _cupy_package_for_cuda future CUDA 14+ tries cupy-cuda13x first.
TEST-GPU-006  detect_nvidia returns None when nvidia-smi not available.
TEST-GPU-007  detect_amd returns None on non-AMD systems without rocm-smi.
TEST-GPU-008  _parallel compute_device_label returns non-empty string.
TEST-GPU-009  _parallel gpu_available returns bool (True if CuPy + CUDA).
TEST-GPU-010  _parallel run_seeds_parallel runs N seeds in parallel.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow importing from backend/scripts/
_BACKEND = Path(__file__).resolve().parent.parent
_SCRIPTS = _BACKEND / "scripts"
sys.path.insert(0, str(_SCRIPTS))


# ── Package selection logic ───────────────────────────────────────────────────

def test_cupy_package_cuda11():
    """TEST-GPU-001: CUDA 11 maps to cupy-cuda11x first."""
    from install_gpu import _cupy_package_for_cuda
    pkgs = _cupy_package_for_cuda(11)
    assert pkgs[0] == "cupy-cuda11x"


def test_cupy_package_cuda12():
    """TEST-GPU-002: CUDA 12 maps to cupy-cuda12x first."""
    from install_gpu import _cupy_package_for_cuda
    pkgs = _cupy_package_for_cuda(12)
    assert pkgs[0] == "cupy-cuda12x"


def test_cupy_package_cuda13():
    """TEST-GPU-003: CUDA 13 maps to cupy-cuda13x first."""
    from install_gpu import _cupy_package_for_cuda
    pkgs = _cupy_package_for_cuda(13)
    assert pkgs[0] == "cupy-cuda13x"


def test_cupy_package_unknown_cuda():
    """TEST-GPU-004: Unknown CUDA version (0) returns a non-empty list."""
    from install_gpu import _cupy_package_for_cuda
    pkgs = _cupy_package_for_cuda(0)
    assert len(pkgs) >= 2
    assert all("cupy" in p for p in pkgs)


def test_cupy_package_future_cuda():
    """TEST-GPU-005: Future CUDA 14+ tries cupy-cuda13x first (newest known)."""
    from install_gpu import _cupy_package_for_cuda
    pkgs = _cupy_package_for_cuda(14)
    assert pkgs[0] == "cupy-cuda13x"


def test_detect_nvidia_returns_none_or_dict():
    """TEST-GPU-006: detect_nvidia returns None or a dict with the right keys."""
    from install_gpu import detect_nvidia
    result = detect_nvidia()
    if result is not None:
        assert "name" in result
        assert "cuda_major" in result
        assert "vram_mb" in result
        assert isinstance(result["cuda_major"], int)


def test_detect_amd_returns_none_or_dict():
    """TEST-GPU-007: detect_amd returns None or a dict with vendor='AMD'."""
    from install_gpu import detect_amd
    result = detect_amd()
    if result is not None:
        assert result.get("vendor") == "AMD"


# ── _parallel utilities ───────────────────────────────────────────────────────

def test_compute_device_label_non_empty():
    """TEST-GPU-008: compute_device_label returns a non-empty string."""
    from glossa_lab.experiments._parallel import compute_device_label
    label = compute_device_label()
    assert isinstance(label, str)
    assert len(label) > 0
    # Should contain either GPU or CPU
    assert "GPU" in label or "CPU" in label


def test_gpu_available_returns_bool():
    """TEST-GPU-009: gpu_available returns a bool."""
    from glossa_lab.experiments._parallel import gpu_available
    result = gpu_available()
    assert isinstance(result, bool)


def test_run_seeds_parallel_produces_n_results():
    """TEST-GPU-010: run_seeds_parallel runs exactly N seeds and returns results."""
    from glossa_lab.experiments._parallel import run_seeds_parallel

    def _echo(seed: int) -> int:
        return seed * 2

    seeds  = [1, 2, 3, 4, 5]
    results = run_seeds_parallel(_echo, seeds)
    assert len(results) == 5
    assert sorted(results) == [2, 4, 6, 8, 10]
