"""GPU and parallel acceleration for Glossa Lab experiments.

This module provides three tiers of acceleration:

  TIER 1 — Multi-process parallelism (always available)
  --------------------------------------------------------
  Monte Carlo trials are embarrassingly parallel. ProcessPoolExecutor
  dispatches each trial to a separate CPU core.  This is the biggest
  single win: 30 trials → ~30× faster on a 32-core machine.

  TIER 2 — NumPy-vectorised scoring (requires numpy)
  -------------------------------------------------------
  The bigram log-likelihood inner loop is replaced by vectorised
  integer indexing into a pre-built frequency matrix.  Gives ~5-15×
  speedup over pure-Python dict lookups for large corpora.

  TIER 3 — GPU batched operations (requires torch or cupy with CUDA)
  -------------------------------------------------------------------
  Batch Kandles cosine-similarity and batch bigram-score matrices are
  pushed onto the GPU.  Useful when running hundreds of simultaneous
  hypothesis comparisons.  Falls back silently to Tier 2 / Tier 1 if
  no CUDA device is found.

USAGE:
    from glossa_lab.accelerate import (
        gpu_info,
        parallel_mc_trials,
        make_fast_scorer,
        kandles_batch_compare,
    )
"""

from __future__ import annotations

import concurrent.futures
import logging
import math
import multiprocessing
import os
import sys
from typing import Any, Callable, TypeVar

log = logging.getLogger(__name__)

T = TypeVar("T")

# ── Device detection ─────────────────────────────────────────

# ── GPU Platform Roadmap (TODO) ─────────────────────────────────────────────
# A) NVIDIA CUDA   — SUPPORTED via torch.cuda / cupy  (current)
# B) AMD ROCm 7.2  — TODO: Linux only. Use `torch` with ROCm wheel:
#      pip install torch --index-url https://download.pytorch.org/whl/rocm6.2
#      Then _TORCH_OK + torch.cuda.is_available() works identically.
# C) Apple M-series MPS — TODO: torch.backends.mps.is_available()
#      Move batch operations to device="mps" instead of "cuda".
#      BiggramScorer in decipher.py needs an MPS-aware path.
# D) Intel Arc (beta) — TODO: torch with Intel Extension for PyTorch (IPEX).
#      import intel_extension_for_pytorch as ipex
#      Very limited support; CPU fallback is acceptable.
# N) CPU — always available (numpy fast path, no GPU required).
# ───────────────────────────────────────────────────────────────────────────────

_NUMPY_OK = False
_TORCH_OK = False
_CUPY_OK = False
_CUDA_AVAILABLE = False
_MPS_AVAILABLE  = False   # Apple Silicon (future)
_ROCM_AVAILABLE = False   # AMD ROCm (future)

try:
    import numpy as _np  # type: ignore[import]

    _NUMPY_OK = True
except ImportError:
    _np = None  # type: ignore[assignment]

try:
    import torch as _torch  # type: ignore[import]

    _TORCH_OK = True
    _CUDA_AVAILABLE = _torch.cuda.is_available()
except ImportError:
    _torch = None  # type: ignore[assignment]

if not _CUDA_AVAILABLE:
    try:
        import cupy as _cp  # type: ignore[import]
        _CUPY_OK = True
        _CUDA_AVAILABLE = True
    except ImportError:
        _cp = None  # type: ignore[assignment]

# Apple MPS detection (no-op until MPS code paths are implemented)
if not _CUDA_AVAILABLE and _TORCH_OK:
    try:
        _MPS_AVAILABLE = _torch.backends.mps.is_available()  # type: ignore[union-attr]
    except Exception:  # noqa: BLE001
        _MPS_AVAILABLE = False


def gpu_info() -> dict[str, Any]:
    """Return a summary of available acceleration resources."""
    info: dict[str, Any] = {
        "numpy": _NUMPY_OK,
        "torch": _TORCH_OK,
        "cupy": _CUPY_OK,
        "cuda": _CUDA_AVAILABLE,
        "mps": _MPS_AVAILABLE,
        "cpu_cores": multiprocessing.cpu_count(),
        "tier": 1,
        "tier_name": "multi-process CPU",
        "platform": "CPU",
    }
    if _NUMPY_OK:
        info["tier"] = 2
        info["tier_name"] = "numpy-vectorised CPU"
        info["platform"] = "CPU (numpy)"
    if _MPS_AVAILABLE:
        info["tier"] = 3
        info["tier_name"] = "GPU (Apple MPS)"
        info["platform"] = "Apple MPS"
    if _CUDA_AVAILABLE:
        info["tier"] = 3
        info["tier_name"] = "GPU (CUDA)"

    if _TORCH_OK and _CUDA_AVAILABLE:
        info["gpu_name"] = _torch.cuda.get_device_name(0)
        info["gpu_mem_gb"] = round(_torch.cuda.get_device_properties(0).total_memory / 1e9, 2)
    elif _CUPY_OK and _CUDA_AVAILABLE:
        device = _cp.cuda.Device(0)
        info["gpu_name"] = f"CUDA device {device.id}"

    return info


# ── Tier 1: Multi-process MC trial parallelism ────────────────────────


def _n_workers() -> int:
    """Number of worker processes to use (leave 1 core for main thread)."""
    env = os.environ.get("GLOSSA_WORKERS")
    if env:
        return max(1, int(env))
    cores = multiprocessing.cpu_count()
    return max(1, cores - 1)


def parallel_mc_trials(
    trial_fn: Callable[..., T],
    seeds: list[int],
    *args: Any,
    n_workers: int | None = None,
    **kwargs: Any,
) -> list[T]:
    """Run trial_fn(seed, *args, **kwargs) in parallel for each seed.

    This is the primary speedup for Monte Carlo experiments. Each trial
    is independent and can run on a separate CPU core.

    Args:
        trial_fn:  A picklable function. First positional arg is seed (int).
        seeds:     List of integer seeds; one trial per seed.
        *args:     Additional positional arguments forwarded to trial_fn.
        n_workers: Override number of worker processes (default: cpu_count-1).
        **kwargs:  Keyword arguments forwarded to trial_fn.

    Returns:
        List of results in seed order (same order as input seeds).

    Example:
        results = parallel_mc_trials(my_trial, list(range(100)),
                                     corpus, mapping, "no_vocab", models)
    """
    workers = n_workers or _n_workers()

    if workers <= 1 or len(seeds) <= 1:
        # Serial fallback (avoids pickling overhead for tiny runs)
        return [trial_fn(s, *args, **kwargs) for s in seeds]

    futures_map: dict[concurrent.futures.Future, int] = {}  # future → order index
    results: list[T] = [None] * len(seeds)  # type: ignore[list-item]

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for idx, seed in enumerate(seeds):
            fut = executor.submit(trial_fn, seed, *args, **kwargs)
            futures_map[fut] = idx

        for fut in concurrent.futures.as_completed(futures_map):
            idx = futures_map[fut]
            try:
                results[idx] = fut.result()
            except Exception as exc:  # noqa: BLE001
                log.warning("Trial seed=%d failed: %s", seeds[idx], exc)
                results[idx] = None  # type: ignore[assignment]

    return results


# ── Tier 2: NumPy-vectorised language model scoring ───────────────────


class FastScorer:
    """NumPy-backed bigram log-likelihood scorer.

    Drop-in replacement for LanguageModel.score_text() that uses
    vectorised array indexing instead of Python dict loops.

    ~5-15× faster for corpora > 500 symbols.

    Build with make_fast_scorer(language_model) after importing numpy.
    """

    def __init__(
        self,
        bigram_matrix: Any,  # np.ndarray shape (V, V) float32
        symbol_to_idx: dict[str, int],
        smoothing: float = 1e-8,
    ) -> None:
        self._mat = bigram_matrix
        self._sym_to_idx = symbol_to_idx
        self._V = bigram_matrix.shape[0]
        self._log_smooth = math.log(smoothing)
        self._log_mat: Any = None  # lazy

    def _ensure_log_mat(self) -> None:
        if self._log_mat is None and _NUMPY_OK:
            import numpy as np

            mat = self._mat.copy()
            mat[mat == 0] = 1e-8
            self._log_mat = np.log(mat, dtype=np.float64)

    def score_text(self, text: list[str]) -> float:
        """Compute bigram log-likelihood for text."""
        if not _NUMPY_OK or len(text) < 2:
            return self._score_text_python(text)

        import numpy as np

        self._ensure_log_mat()

        V = self._V
        default_idx = V - 1  # last row/col is the OOV bucket
        indices = np.array(
            [self._sym_to_idx.get(s, default_idx) for s in text],
            dtype=np.int32,
        )
        rows = indices[:-1]
        cols = indices[1:]
        log_probs = self._log_mat[rows, cols]  # type: ignore[index]
        return float(log_probs.sum())

    def _score_text_python(self, text: list[str]) -> float:
        ll = 0.0
        for i in range(len(text) - 1):
            r = self._sym_to_idx.get(text[i], self._V - 1)
            c = self._sym_to_idx.get(text[i + 1], self._V - 1)
            v = float(self._mat[r, c]) if _NUMPY_OK else 0.0
            ll += math.log(v) if v > 0 else self._log_smooth
        return ll


def make_fast_scorer(language_model: Any) -> "FastScorer | None":
    """Build a FastScorer from a LanguageModel.

    Returns None if numpy is not available.
    """
    if not _NUMPY_OK:
        return None

    import numpy as np

    symbols = language_model.alphabet
    V = len(symbols) + 1  # +1 for OOV
    sym_to_idx = {s: i for i, s in enumerate(symbols)}

    mat = np.zeros((V, V), dtype=np.float32)
    for (a, b), freq in language_model.bigram_freq.items():
        ia = sym_to_idx.get(a, V - 1)
        ib = sym_to_idx.get(b, V - 1)
        mat[ia, ib] = freq

    return FastScorer(mat, sym_to_idx)


# ── Tier 3: GPU batch Kandles cosine similarity ───────────────────────


def kandles_batch_compare(
    distributions_a: list[list[float]],
    distributions_b: list[list[float]],
) -> list[float]:
    """Compute cosine similarity for N pairs of 8-dim Kandles distributions.

    Automatically uses GPU (torch/cupy) if available, otherwise numpy,
    otherwise pure Python.

    Args:
        distributions_a: List of N distributions (each is a list of 8 floats).
        distributions_b: List of N distributions (each is a list of 8 floats).

    Returns:
        List of N cosine similarity scores in [0, 1].
    """
    if not distributions_a:
        return []

    n = len(distributions_a)
    assert len(distributions_b) == n, "a/b lists must be same length"

    if _TORCH_OK and _CUDA_AVAILABLE:
        return _kandles_batch_torch(distributions_a, distributions_b)
    elif _CUPY_OK and _CUDA_AVAILABLE:
        return _kandles_batch_cupy(distributions_a, distributions_b)
    elif _NUMPY_OK:
        return _kandles_batch_numpy(distributions_a, distributions_b)
    else:
        return _kandles_batch_python(distributions_a, distributions_b)


def _kandles_batch_numpy(
    a: list[list[float]],
    b: list[list[float]],
) -> list[float]:
    import numpy as np

    A = np.array(a, dtype=np.float32)  # (N, 8)
    B = np.array(b, dtype=np.float32)  # (N, 8)
    dots = (A * B).sum(axis=1)
    mag_a = np.linalg.norm(A, axis=1)
    mag_b = np.linalg.norm(B, axis=1)
    denom = mag_a * mag_b
    sims = np.where(denom > 0, dots / denom, 0.0)
    return sims.tolist()


def _kandles_batch_torch(
    a: list[list[float]],
    b: list[list[float]],
) -> list[float]:
    import torch

    A = torch.tensor(a, dtype=torch.float32, device="cuda")  # (N, 8)
    B = torch.tensor(b, dtype=torch.float32, device="cuda")  # (N, 8)
    sims = torch.nn.functional.cosine_similarity(A, B, dim=1)
    return sims.cpu().tolist()


def _kandles_batch_cupy(
    a: list[list[float]],
    b: list[list[float]],
) -> list[float]:
    import cupy as cp

    A = cp.array(a, dtype=cp.float32)
    B = cp.array(b, dtype=cp.float32)
    dots = (A * B).sum(axis=1)
    mag_a = cp.linalg.norm(A, axis=1)
    mag_b = cp.linalg.norm(B, axis=1)
    denom = mag_a * mag_b
    sims = cp.where(denom > 0, dots / denom, 0.0)
    return cp.asnumpy(sims).tolist()


def _kandles_batch_python(
    a: list[list[float]],
    b: list[list[float]],
) -> list[float]:
    results = []
    for va, vb in zip(a, b):
        dot = sum(x * y for x, y in zip(va, vb))
        mag_a = math.sqrt(sum(x * x for x in va))
        mag_b = math.sqrt(sum(y * y for y in vb))
        s = dot / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0.0
        results.append(s)
    return results


# ── Tier 3: Batch bigram scoring (GPU matrix multiply) ────────────────


def batch_hypothesis_score(
    phoneme_sequences: list[list[str]],
    language_model: Any,
) -> list[float]:
    """Score multiple phoneme sequences against one language model in batch.

    Uses GPU matrix operations if available. Each sequence is scored
    independently; results are returned in input order.

    This is useful when running many MC permutations against the same
    language model (e.g. null distribution experiments).

    Returns list of bigram log-likelihood scores.
    """
    if _TORCH_OK and _CUDA_AVAILABLE:
        return _batch_score_torch(phoneme_sequences, language_model)
    elif _NUMPY_OK:
        fs = make_fast_scorer(language_model)
        if fs:
            return [fs.score_text(seq) for seq in phoneme_sequences]
    # Fallback: use LanguageModel directly
    return [language_model.score_text(seq) for seq in phoneme_sequences]


def _batch_score_torch(
    sequences: list[list[str]],
    language_model: Any,
) -> list[float]:
    """Score sequences using a GPU bigram log-probability matrix."""
    import torch

    symbols = language_model.alphabet
    V = len(symbols) + 1
    sym_to_idx = {s: i for i, s in enumerate(symbols)}

    # Build bigram matrix on GPU
    import numpy as np

    mat = np.zeros((V, V), dtype=np.float32)
    for (a, b), freq in language_model.bigram_freq.items():
        ia = sym_to_idx.get(a, V - 1)
        ib = sym_to_idx.get(b, V - 1)
        mat[ia, ib] = freq
    mat[mat == 0] = 1e-8
    log_mat = torch.tensor(np.log(mat), dtype=torch.float32, device="cuda")

    scores = []
    for seq in sequences:
        if len(seq) < 2:
            scores.append(0.0)
            continue
        idxs = torch.tensor(
            [sym_to_idx.get(s, V - 1) for s in seq],
            dtype=torch.long,
            device="cuda",
        )
        log_probs = log_mat[idxs[:-1], idxs[1:]]
        scores.append(float(log_probs.sum().cpu().item()))

    return scores


# ── NumPy-accelerated Kandles grid comparison ─────────────────────────


def fast_kandles_validate(
    deciphered: list[str],
    target_symbols: list[str],
    kandles_profile: str | None = None,
) -> float:
    """Accelerated Kandles validation using numpy batch ops.

    Computes the cosine similarity of the 8-dim Kandles color
    distribution vectors. Falls back to the standard kandles module
    if numpy is not available.
    """
    try:
        from glossa_lab.pipelines.kandles import generate_grid

        grid_dec = generate_grid(deciphered[:200], profile=kandles_profile)
        grid_tgt = generate_grid(target_symbols[:200], profile=kandles_profile)

        # Extract raw distribution vectors instead of calling compare_grids
        def _dist_vec(grid: dict) -> list[float]:
            dist: dict[int, int] = {}
            for row in grid["grid"]:
                for cell in row:
                    g = cell.get("group", -1)
                    if g >= 0:
                        dist[g] = dist.get(g, 0) + 1
            total = sum(dist.values()) or 1
            return [dist.get(g, 0) / total for g in range(8)]

        va = _dist_vec(grid_dec)
        vb = _dist_vec(grid_tgt)

        sims = kandles_batch_compare([va], [vb])
        return round(sims[0], 4)
    except Exception:  # noqa: BLE001
        return 0.0


# ── GPU batch context-vector cosine similarity (Ventris / fingerprint) ───


def build_context_vectors(
    inscriptions: list[list[str]],
    signs: list[str],
    window: int = 2,
) -> tuple["Any", "Any"]:
    """Build left- and right-context frequency matrices for a set of signs.

    Returns two numpy arrays of shape (len(signs), len(signs)):
      left_matrix[i, j]  = frequency sign j appears within `window` positions
                           BEFORE sign i across all inscriptions.
      right_matrix[i, j] = frequency sign j appears within `window` positions
                           AFTER sign i.

    Falls back to pure-Python dicts if numpy is not available.
    """
    sign_to_idx = {s: i for i, s in enumerate(signs)}
    n = len(signs)

    if _NUMPY_OK:
        import numpy as np

        left = np.zeros((n, n), dtype=np.float32)
        right = np.zeros((n, n), dtype=np.float32)
        for insc in inscriptions:
            for pos, sign in enumerate(insc):
                if sign not in sign_to_idx:
                    continue
                si = sign_to_idx[sign]
                for d in range(1, window + 1):
                    if pos - d >= 0 and insc[pos - d] in sign_to_idx:
                        left[si, sign_to_idx[insc[pos - d]]] += 1
                    if pos + d < len(insc) and insc[pos + d] in sign_to_idx:
                        right[si, sign_to_idx[insc[pos + d]]] += 1
        return left, right

    # Pure-Python fallback
    from collections import defaultdict

    left_d: dict[int, dict[int, float]] = defaultdict(lambda: defaultdict(float))
    right_d: dict[int, dict[int, float]] = defaultdict(lambda: defaultdict(float))
    for insc in inscriptions:
        for pos, sign in enumerate(insc):
            if sign not in sign_to_idx:
                continue
            si = sign_to_idx[sign]
            for d in range(1, window + 1):
                if pos - d >= 0 and insc[pos - d] in sign_to_idx:
                    left_d[si][sign_to_idx[insc[pos - d]]] += 1
                if pos + d < len(insc) and insc[pos + d] in sign_to_idx:
                    right_d[si][sign_to_idx[insc[pos + d]]] += 1
    return left_d, right_d  # type: ignore[return-value]


def batch_cosine_similarity_matrix(
    vectors: "Any",
) -> "Any":
    """Compute an N×N cosine similarity matrix from an N×M feature matrix.

    Uses GPU (torch/cupy) when available, numpy otherwise.
    This is the core operation for the Ventris affinity grid:
      sim[i, j] = cosine_similarity(vectors[i], vectors[j])

    Args:
        vectors: N×M array (numpy, torch, or cupy).

    Returns:
        N×N cosine similarity matrix as numpy array.
    """
    if _TORCH_OK and _CUDA_AVAILABLE:
        import torch

        if not isinstance(vectors, torch.Tensor):
            import numpy as np

            V = torch.tensor(vectors, dtype=torch.float32, device="cuda")
        else:
            V = vectors.to("cuda").float()
        norms = V.norm(dim=1, keepdim=True).clamp(min=1e-8)
        V_norm = V / norms
        sim = (V_norm @ V_norm.T).cpu().numpy()
        return sim

    if _CUPY_OK and _CUDA_AVAILABLE:
        import cupy as cp

        V = cp.array(vectors, dtype=cp.float32)
        norms = cp.linalg.norm(V, axis=1, keepdims=True).clip(min=1e-8)
        V_norm = V / norms
        sim = cp.asnumpy(V_norm @ V_norm.T)
        return sim

    if _NUMPY_OK:
        import numpy as np

        V = np.asarray(vectors, dtype=np.float32)
        norms = np.linalg.norm(V, axis=1, keepdims=True).clip(min=1e-8)
        V_norm = V / norms
        return (V_norm @ V_norm.T).astype(np.float64)

    # Pure-Python O(N^3) fallback
    import math

    n = len(vectors)
    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            vi = list(vectors[i]) if not isinstance(vectors[i], list) else vectors[i]
            vj = list(vectors[j]) if not isinstance(vectors[j], list) else vectors[j]
            dot = sum(a * b for a, b in zip(vi, vj))
            mag_i = math.sqrt(sum(a * a for a in vi))
            mag_j = math.sqrt(sum(b * b for b in vj))
            s = dot / (mag_i * mag_j) if mag_i > 0 and mag_j > 0 else 0.0
            sim[i][j] = sim[j][i] = s
    return sim


def ventris_affinity_gpu(
    inscriptions: list[list[str]],
    signs: list[str],
    window: int = 2,
) -> tuple["Any", "Any"]:
    """Compute Ventris vowel+consonant affinity matrices using GPU.

    Returns:
        (vowel_sim, consonant_sim): two N×N cosine similarity matrices.
        vowel_sim[i,j]     = similarity of RIGHT context → consonant affinity
        consonant_sim[i,j] = similarity of LEFT context  → vowel affinity

    NOTE on semantics (Ventris 1953):
      - Signs sharing the same VOWEL appear after similar consonants
        → similar LEFT context → left_matrix cosine → 'vowel affinity' (rows)
      - Signs sharing the same CONSONANT appear before similar vowels
        → similar RIGHT context → right_matrix cosine → 'consonant affinity' (cols)
    """
    left_mat, right_mat = build_context_vectors(inscriptions, signs, window)

    if _NUMPY_OK:
        import numpy as np

        if not hasattr(left_mat, "shape"):
            # Convert dicts to array
            n = len(signs)
            left_arr = np.zeros((n, n), dtype=np.float32)
            right_arr = np.zeros((n, n), dtype=np.float32)
            for i, row in left_mat.items():  # type: ignore[union-attr]
                for j, v in row.items():
                    left_arr[i, j] = v
            for i, row in right_mat.items():  # type: ignore[union-attr]
                for j, v in row.items():
                    right_arr[i, j] = v
            left_mat = left_arr
            right_mat = right_arr

    vowel_sim = batch_cosine_similarity_matrix(left_mat)
    consonant_sim = batch_cosine_similarity_matrix(right_mat)
    return vowel_sim, consonant_sim


def gpu_fingerprint_compare(
    target_vector: list[float],
    database_vectors: list[list[float]],
    weights: list[float] | None = None,
) -> list[float]:
    """Compute weighted Euclidean distances from target to all database vectors.

    Uses GPU batch subtraction + reduction when available.

    Args:
        target_vector:    Single fingerprint vector (length D).
        database_vectors: K fingerprint vectors (K × D).
        weights:          Optional D-length weight vector.

    Returns:
        K distances in same order as database_vectors.
    """
    if not database_vectors:
        return []

    D = len(target_vector)
    W = weights or [1.0] * D

    if _TORCH_OK and _CUDA_AVAILABLE:
        import torch

        t = torch.tensor(target_vector, dtype=torch.float32, device="cuda")
        db = torch.tensor(database_vectors, dtype=torch.float32, device="cuda")
        w = torch.tensor(W, dtype=torch.float32, device="cuda")
        diff = db - t.unsqueeze(0)  # K × D
        dist = torch.sqrt((diff**2 * w).sum(dim=1))  # K
        return dist.cpu().tolist()

    if _CUPY_OK and _CUDA_AVAILABLE:
        import cupy as cp

        t = cp.array(target_vector, dtype=cp.float32)
        db = cp.array(database_vectors, dtype=cp.float32)
        w = cp.array(W, dtype=cp.float32)
        diff = db - t[None, :]
        dist = cp.sqrt((diff**2 * w).sum(axis=1))
        return cp.asnumpy(dist).tolist()

    if _NUMPY_OK:
        import numpy as np

        t = np.array(target_vector, dtype=np.float64)
        db = np.array(database_vectors, dtype=np.float64)
        w = np.array(W, dtype=np.float64)
        diff = db - t[None, :]
        dist = np.sqrt((diff**2 * w).sum(axis=1))
        return dist.tolist()

    # Pure-Python fallback
    import math

    return [
        math.sqrt(sum(W[d] * (db_v[d] - target_vector[d]) ** 2 for d in range(D)))
        for db_v in database_vectors
    ]


# ── Progress reporter for long experiments ────────────────────────────


class ProgressCounter:
    """Thread-safe progress counter for parallel experiment runs."""

    def __init__(self, total: int, desc: str = "trials") -> None:
        self.total = total
        self.desc = desc
        self._count = multiprocessing.Value("i", 0)

    def increment(self) -> None:
        with self._count.get_lock():
            self._count.value += 1
            n = self._count.value
        pct = n / self.total * 100
        bar = "#" * int(pct // 5)
        sys.stdout.write(f"\r  [{bar:<20}] {n}/{self.total} {self.desc} ({pct:.0f}%)")
        sys.stdout.flush()
        if n >= self.total:
            sys.stdout.write("\n")
            sys.stdout.flush()
