"""GPU device detection with smart fallback behavior.

Detection rules
---------------
- ``torch`` not installed            → silent CPU fallback (no GPU ever configured)
- ``torch.cuda.is_available()`` False → silent CPU fallback (no CUDA hardware)
- CUDA available, free VRAM < limit   → **RuntimeWarning** + CPU fallback
- CUDA available, init raises error   → **logging.error** + CPU fallback
- Everything OK                       → returns ``"cuda"``

Usage
-----
    from glossa_lab.gpu_utils import detect_device
    DEVICE = detect_device()          # min_vram_gb=1.0 by default

    # In graph-module helpers (no print):
    def _get_device() -> str:
        from glossa_lab.gpu_utils import detect_device
        return detect_device()
"""
from __future__ import annotations

import logging
import warnings

_log = logging.getLogger(__name__)


def detect_device(min_vram_gb: float = 1.0) -> str:
    """Return the best available compute device string.

    Parameters
    ----------
    min_vram_gb:
        Minimum *free* GPU memory in GiB required to use CUDA.
        If the free memory is below this threshold the function emits a
        ``RuntimeWarning`` and returns ``"cpu"``.  Default: 1.0 GiB.

    Returns
    -------
    ``"cuda"`` if a working CUDA device is available with sufficient free
    VRAM, otherwise ``"cpu"``.
    """
    # ── 1. torch not installed → silent CPU ──────────────────────────────────
    try:
        import torch  # noqa: PLC0415
    except ImportError:
        return "cpu"

    # ── 2. No CUDA hardware → silent CPU ─────────────────────────────────────
    if not torch.cuda.is_available():
        return "cpu"

    # ── 3. CUDA present — check free VRAM ────────────────────────────────────
    try:
        free_bytes, total_bytes = torch.cuda.mem_get_info(0)
        free_gb  = free_bytes  / (1024 ** 3)
        total_gb = total_bytes / (1024 ** 3)
        if free_gb < min_vram_gb:
            warnings.warn(
                f"[GPU] CUDA device present ({total_gb:.1f} GiB total, "
                f"{free_gb:.2f} GiB free) but {min_vram_gb:.1f} GiB free is required. "
                f"Falling back to CPU.",
                RuntimeWarning,
                stacklevel=2,
            )
            return "cpu"
    except Exception as _vram_exc:  # noqa: BLE001
        # Cannot query VRAM — emit a warning and try to use GPU anyway.
        warnings.warn(
            f"[GPU] Could not query VRAM ({_vram_exc!s}); attempting CUDA anyway.",
            RuntimeWarning,
            stacklevel=2,
        )

    # ── 4. Verify CUDA initialises cleanly ───────────────────────────────────
    try:
        _probe = torch.zeros(1, device="cuda")
        del _probe
    except RuntimeError as exc:
        _log.error(
            "[GPU] CUDA device detected but failed to initialise: %s — falling back to CPU.",
            exc,
        )
        return "cpu"

    return "cuda"
