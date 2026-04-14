"""Shared parallel execution and compute-device utilities for Glossa Lab experiments.

ALL experiments that run multi-seed SA loops MUST use run_seeds_parallel()
from this module instead of a plain Python for-loop.

RULES (enforced by AGENTS.md H10 + H12):
  - GPU (CuPy) is used when available; falls back to NumPy automatically.
  - When GPU is unavailable, multi-core CPU parallelism is MANDATORY via ThreadPoolExecutor.
  - ThreadPoolExecutor is used (not ProcessPoolExecutor) because:
      1. LanguageModel objects are not picklable.
      2. NumPy/CuPy release the GIL for array operations, providing real
         concurrency across threads.

Usage in an experiment::

    from glossa_lab.experiments._parallel import run_seeds_parallel, compute_device

    def _one_seed(seed, cipher_tokens, lm, anchors):
        from glossa_lab.pipelines.decipher import decipher
        return decipher(cipher_signs=cipher_tokens, target_model=lm,
                        seed=seed, ...).get("proposed_mapping", {})

    mappings = run_seeds_parallel(_one_seed, seeds=[1,2,3,4,5],
                                  cipher_tokens=..., lm=..., anchors=...)
    device = compute_device()   # "gpu" | "cpu"
"""
from __future__ import annotations

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable

_log = logging.getLogger("glossa_lab.experiments")

# ── GPU detection ─────────────────────────────────────────────────────────────

_GPU_AVAILABLE: bool | None = None   # cached after first check


def _detect_gpu() -> bool:
    """Return True if a CUDA-capable GPU is available via CuPy."""
    try:
        import cupy as cp
        return bool(cp.cuda.is_available())
    except (ImportError, Exception):
        return False


def gpu_available() -> bool:
    """Cached GPU availability check."""
    global _GPU_AVAILABLE
    if _GPU_AVAILABLE is None:
        _GPU_AVAILABLE = _detect_gpu()
        if _GPU_AVAILABLE:
            _log.info("Compute device: GPU (CuPy CUDA)")
        else:
            _log.info("Compute device: CPU (NumPy — GPU unavailable)")
    return _GPU_AVAILABLE


def compute_device() -> str:
    """Return 'gpu' if GPU is available, else 'cpu'."""
    return "gpu" if gpu_available() else "cpu"


def compute_device_label() -> str:
    """Return a human-readable compute device label for job params and UI badges."""
    if gpu_available():
        try:
            import cupy as cp
            props = cp.cuda.Device(0).attributes
            return f"GPU (CUDA)"
        except Exception:
            return "GPU (CUDA)"
    else:
        try:
            import multiprocessing
            cores = multiprocessing.cpu_count()
            return f"CPU ({cores} cores)"
        except Exception:
            return "CPU"


# ── Parallel seed execution ───────────────────────────────────────────────────

def run_seeds_parallel(
    fn: Callable,
    seeds: list[int],
    *args: Any,
    max_workers: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    """Run fn(seed, *args, **kwargs) for each seed in parallel via ThreadPoolExecutor.

    Results are returned in the same order as seeds.
    Failed seeds are skipped (logged as warnings).

    Args:
        fn:          Function taking (seed, *args, **kwargs) → result.
        seeds:       List of integer seeds to run.
        *args:       Positional args forwarded to fn (after seed).
        max_workers: Max thread pool size; defaults to min(len(seeds), cpu_count).
        **kwargs:    Keyword args forwarded to fn.

    Returns:
        List of results in seed order (None for failed seeds, filtered out).
    """
    n = len(seeds)
    if n == 0:
        return []

    workers = max_workers or min(n, os.cpu_count() or 4)
    results: list[Any | None] = [None] * n

    if workers == 1 or n == 1:
        # Skip thread overhead for single seeds
        for i, seed in enumerate(seeds):
            try:
                results[i] = fn(seed, *args, **kwargs)
            except Exception as exc:
                _log.warning("Seed %d failed: %s", seed, exc)
        return [r for r in results if r is not None]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_idx = {
            executor.submit(fn, seed, *args, **kwargs): i
            for i, seed in enumerate(seeds)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as exc:
                _log.warning("Seed %d (idx %d) failed: %s", seeds[idx], idx, exc)

    return [r for r in results if r is not None]


def parallel_map(
    fn: Callable,
    args_list: list[tuple],
    max_workers: int | None = None,
) -> list[Any]:
    """Map fn over a list of argument tuples in parallel.

    Each element of args_list is a tuple of positional args for fn.
    Results preserve submission order. Failures return None (filtered).
    """
    n = len(args_list)
    if n == 0:
        return []

    workers = max_workers or min(n, os.cpu_count() or 4)
    results: list[Any | None] = [None] * n

    if workers == 1 or n == 1:
        for i, args in enumerate(args_list):
            try:
                results[i] = fn(*args)
            except Exception as exc:
                _log.warning("Task %d failed: %s", i, exc)
        return [r for r in results if r is not None]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_idx = {
            executor.submit(fn, *args): i
            for i, args in enumerate(args_list)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as exc:
                _log.warning("Task %d failed: %s", idx, exc)

    return [r for r in results if r is not None]
