# GPU Setup Guide — Glossa Lab

GPU acceleration is **automatically detected and installed** when you run `shell.cmd setup`.
This guide explains what happens, how to verify it, and how to handle edge cases.

---

## Why GPU matters

Glossa Lab's core performance bottleneck is the Simulated Annealing (SA) decipherment engine.
Each SA run scores a candidate sign mapping against a bigram language model:

| Mode | Per-iteration speed | Typical full run |
|---|---|---|
| CPU (NumPy) | ~0.1 ms / iteration | ~10 s / seed |
| GPU (CuPy, RTX 4070+) | ~0.005 ms / iteration | ~0.5 s / seed |

With 10 parallel seeds × 8 restarts × 10,000 iterations, GPU is **~20× faster overall**.

The `BigramScorer` class in `decipher.py` automatically uses CuPy when available — no code
change required.

---

## Auto-install (recommended)

```bat
shell.cmd setup
```

This runs `backend/scripts/install_gpu.py` which:
1. Detects your GPU vendor (NVIDIA/AMD/Intel) using `nvidia-smi` / `nvcc` / `rocm-smi`
2. Determines your CUDA/ROCm version
3. Installs the matching CuPy package
4. Falls back gracefully to NumPy (CPU) if anything fails

---

## NVIDIA (CuPy + CUDA)

### Requirements
- NVIDIA GPU (any generation supported by CUDA 11, 12, or 13)
- NVIDIA driver ≥ 450.x (CUDA 11) / 525.x (CUDA 12) / 570.x (CUDA 13)
- CUDA Toolkit installed from [developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)

### Which package to install

| CUDA Toolkit version | Package | Notes |
|---|---|---|
| CUDA 11.x | `cupy-cuda11x` | RTX 30xx, Tesla V100, A100 |
| CUDA 12.x | `cupy-cuda12x` | RTX 40xx (most common) |
| CUDA 13.x | `cupy-cuda13x` | RTX 40xx with latest toolkit |

### Manual install

```bat
REM Check your CUDA version:
nvcc --version

REM Install matching CuPy (replace 12x with your version):
shell.cmd python -m pip install cupy-cuda12x

REM Or use the pyproject.toml extra:
shell.cmd python -m pip install -e backend[gpu-cuda13]
```

### Check CUDA version from driver only (no toolkit)

```bat
nvidia-smi
REM Look for "CUDA Version: X.Y" in the top-right of the output.
REM This is the MAXIMUM version your driver supports.
REM Install the CUDA Toolkit matching this version or lower.
```

---

## AMD (ROCm / HIP)

AMD GPU support via CuPy is available but requires manual steps.

### Requirements
- AMD GPU with ROCm support (Radeon RX 6000+, Instinct MI series)
- ROCm 5.x or 6.x installed from [rocm.docs.amd.com](https://rocm.docs.amd.com)
- Linux only (ROCm on Windows is limited)

### Install

```bash
# ROCm 5.x
pip install cupy-rocm-5-0

# ROCm 6.x
pip install cupy-rocm-6-0
```

Check ROCm version:
```bash
rocm-smi --version
```

### Windows + AMD

ROCm on Windows is experimental. Consider using WSL2 with a Linux ROCm installation,
or use CPU mode (NumPy, which is already installed).

---

## Intel (Arc / Xe)

Intel discrete GPU support is experimental via Intel Extension for PyTorch (IPEX).
CuPy does not currently support Intel GPUs.

Glossa Lab will fall back to NumPy (CPU) on Intel GPU systems. The SA engine will
still run but without GPU acceleration.

For Intel CPU optimization (not GPU), NumPy with Intel MKL is automatically used
when installed via conda or Intel's Python distribution.

---

## CPU-only mode (no GPU)

No action needed. NumPy is installed as a core dependency and the SA engine uses
it automatically when CuPy is not available.

Parallelism is still active: all seed loops use `ThreadPoolExecutor` across all
available CPU cores, which typically gives 4–32× speedup over sequential execution.

Check your parallel configuration:
```bat
shell.cmd python -c "from glossa_lab.experiments._parallel import compute_device_label; print(compute_device_label())"
```

---

## Verify GPU is working

```bat
shell.cmd python -c "
from glossa_lab.experiments._parallel import gpu_available, compute_device_label
print('GPU:', gpu_available())
print('Device:', compute_device_label())

from glossa_lab.pipelines.decipher import _HAS_CUPY, _HAS_NUMPY
print('BigramScorer: cupy=%s numpy=%s' % (_HAS_CUPY, _HAS_NUMPY))
"
```

Expected output on a machine with CUDA 13 + CuPy:
```
GPU: True
Device: GPU (CUDA)
BigramScorer: cupy=True numpy=True
```

Expected output on CPU-only:
```
GPU: False
Device: CPU (32 cores)
BigramScorer: cupy=False numpy=True
```

---

## The Jobs panel GPU/CPU badge

When experiments run via `run_cli()` or from the UI, the Jobs panel shows a badge:

- ⚡ GPU (CUDA) — blue badge, CuPy active
- ⚙️ CPU (N cores) — gray badge, NumPy only

This is updated live as each job starts.

---

## Troubleshooting

### "CuPy installed but GPU not accessible"

1. Ensure the CUDA Toolkit version matches the CuPy package:
   ```bat
   nvcc --version     # shows toolkit version
   pip show cupy-cuda12x  # shows installed package
   ```

2. Try reinstalling:
   ```bat
   pip uninstall cupy-cuda12x cupy-cuda13x cupy-cuda11x
   pip install cupy-cuda12x   # or your version
   ```

3. Check the CUDA path is set:
   ```bat
   echo %CUDA_PATH%
   REM Should point to e.g. C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x
   ```

### "nvidia-smi found but nvcc not found"

CUDA Toolkit is not installed (only the driver). Install the toolkit from NVIDIA's site.
Without the toolkit, `cupy-cuda12x` will still work if the driver version is compatible.

### Multiple CUDA versions

If you have multiple CUDA versions (e.g., 12.x and 13.x), set `CUDA_PATH` to the version
you want CuPy to use, then reinstall CuPy.

### GPU detected by Glossa Lab UI (Settings → Hardware) but not by CuPy

The Settings → Hardware panel uses `nvidia-smi` (reads the driver) while CuPy needs
the CUDA Toolkit. Install the CUDA Toolkit and the matching CuPy package.

---

## For contributors / new machines

When setting up a new development machine:

```bat
# 1. Install NVIDIA CUDA Toolkit (see developer.nvidia.com/cuda-downloads)
# 2. Clone the repo
git clone https://github.com/your-org/glossa-lab

# 3. Run setup — GPU is auto-detected and CuPy installed
shell.cmd setup

# 4. Verify
shell.cmd python backend/scripts/install_gpu.py --check
```

The `--check` flag shows what would be installed without actually installing.
