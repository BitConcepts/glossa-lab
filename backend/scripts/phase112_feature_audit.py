"""Phase-112 design-stage feature audit (spec 010 section 4).

Permutation-sensitivity audit for the candidate order-carrying
features, run on KNOWN panel corpora ONLY (never Indus, never the
synthetic controls) BEFORE the spec 010 freeze. For each candidate
feature and each known corpus: 20 draws at N = 11,000 (audit seed
stream [20261020, corpus_index, draw]) and their within-text
permuted counterparts (seed stream [20261021, corpus_index, draw]);
Cohen's d of (original - permuted) per corpus.

Admission rule (frozen in spec 010 section 4): a candidate is
admitted iff (i) median |d| across the 9 known corpora >= 0.8,
(ii) the sign of the mean difference is the same in >= 8 of 9
corpora, and (iii) the feature is non-degenerate (SD of original
draws > 0 in >= 5 corpora). Everything else is dropped and the drop
is recorded in spec 010 and in the output JSON.

Output: reports/phase112_feature_audit.json.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab import phase111_custodian as custodian  # noqa: E402
from glossa_lab.phase112_features import (  # noqa: E402
    CANDIDATE_FEATURES,
    extract_candidates,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
# Phase-112 staged copies of the Phase-111 openly-licensed downloads
# (gitignored local store; identical files, identical licenses).
custodian.SOURCES = REPO_ROOT / "glossa-corpus" / "indus" / "sources" / "phase112"

N_AUDIT_DRAWS = 20
N_TOKENS = 11_000
KNOWN_CODES = [code for _i, code, role in custodian.MEMBERS if role in ("known", "nonling")]
CORPUS_INDEX = {code: i for i, code, _r in custodian.MEMBERS}

OUT_PATH = REPO_ROOT / "reports" / "phase112_feature_audit.json"


def _int_texts(texts: list[list[str]]) -> list[list[int]]:
    vocab = sorted({tok for t in texts for tok in t})
    mapping = {tok: i for i, tok in enumerate(vocab)}
    return [[mapping[tok] for tok in t] for t in texts]


def _permute_draw(draw: list[list[int]], rng: np.random.Generator) -> list[list[int]]:
    out = []
    for t in draw:
        arr = list(t)
        rng.shuffle(arr)
        out.append(arr)
    return out


def _job(args: tuple[str, int, list[list[int]], bool]) -> tuple[str, int, dict[str, float]]:
    code, draw_index, draw, _perm = args
    return code, draw_index, extract_candidates(draw, draw_index=draw_index)


def main() -> None:
    per_corpus: dict[str, dict] = {}
    jobs: list[tuple[str, int, list[list[int]], bool]] = []
    job_meta: list[tuple[str, int, str]] = []  # (code, draw, kind)
    for code in KNOWN_CODES:
        cidx = CORPUS_INDEX[code]
        kind, loader = custodian.LOADERS[code]
        payload, stats = loader()
        texts = custodian.chunk_stream(payload, cidx) if kind == "stream" else payload
        texts_int = _int_texts(texts)
        per_corpus[code] = {"corpus_index": cidx, "loader_stats": stats,
                            "texts_after_chunking": len(texts_int)}
        for draw_index in range(N_AUDIT_DRAWS):
            rng = np.random.default_rng(np.random.SeedSequence([20261020, cidx, draw_index]))
            draw = custodian.resample_draw(texts_int, N_TOKENS, rng)
            jobs.append((code, draw_index, draw, False))
            job_meta.append((code, draw_index, "original"))
            rng_p = np.random.default_rng(np.random.SeedSequence([20261021, cidx, draw_index]))
            perm = _permute_draw(draw, rng_p)
            jobs.append((code, draw_index, perm, True))
            job_meta.append((code, draw_index, "permuted"))
        print(f"loaded {code}: {len(texts_int)} texts", flush=True)

    with Pool(4) as pool:
        results = pool.map(_job, jobs)
    values: dict[tuple[str, int, str], dict[str, float]] = {}
    for (code, draw_index, feats), (_c, _d, kind) in zip(results, job_meta):
        values[(code, draw_index, kind)] = feats

    features_out: dict[str, dict] = {}
    for name in CANDIDATE_FEATURES:
        per_d: dict[str, float] = {}
        signs: dict[str, int] = {}
        nondeg = 0
        for code in KNOWN_CODES:
            orig = np.array([values[(code, d, "original")][name] for d in range(N_AUDIT_DRAWS)])
            perm = np.array([values[(code, d, "permuted")][name] for d in range(N_AUDIT_DRAWS)])
            sd_o, sd_p = float(orig.std(ddof=1)), float(perm.std(ddof=1))
            pooled = np.sqrt((sd_o**2 + sd_p**2) / 2) if (sd_o + sd_p) > 0 else 0.0
            d_eff = float((orig.mean() - perm.mean()) / pooled) if pooled > 0 else 0.0
            per_d[code] = d_eff
            signs[code] = int(np.sign(orig.mean() - perm.mean()))
            if sd_o > 0:
                nondeg += 1
        abs_ds = sorted(abs(v) for v in per_d.values())
        median_abs_d = float(abs_ds[len(abs_ds) // 2]) if len(abs_ds) % 2 == 1 else float(
            (abs_ds[len(abs_ds) // 2 - 1] + abs_ds[len(abs_ds) // 2]) / 2)
        nonzero_signs = [s for s in signs.values() if s != 0]
        dominant_sign = max(set(nonzero_signs), key=nonzero_signs.count) if nonzero_signs else 0
        sign_consistency = int(sum(1 for s in signs.values() if s == dominant_sign))
        admitted = bool(median_abs_d >= 0.8 and sign_consistency >= 8 and nondeg >= 5)
        features_out[name] = {
            "cohens_d_per_corpus": per_d,
            "median_abs_d": median_abs_d,
            "sign_consistency_corpora": sign_consistency,
            "nondegenerate_corpora": nondeg,
            "admitted": admitted,
        }
        print(f"{name:20s} median|d|={median_abs_d:8.3f} signs={sign_consistency}/9 "
              f"nondeg={nondeg}/9 admitted={admitted}", flush=True)

    out = {
        "study": "Phase-112 design-stage permutation-sensitivity audit (spec 010 section 4)",
        "date": "2026-10-07",
        "panel": "known corpora only (K1,K2,K3,K4,K5,K7,K8,K9,N1 as assembled under spec 009)",
        "draws_per_corpus": N_AUDIT_DRAWS,
        "tokens_per_draw": N_TOKENS,
        "draw_seed_stream": "[20261020, corpus_index, draw_index]",
        "permutation_seed_stream": "[20261021, corpus_index, draw_index]",
        "admission_rule": "median |Cohen d| >= 0.8 AND same-sign mean difference in >= 8/9 corpora AND SD(original) > 0 in >= 5 corpora",
        "corpora": per_corpus,
        "features": features_out,
        "admitted_features": [n for n in CANDIDATE_FEATURES if features_out[n]["admitted"]],
        "dropped_features": [n for n in CANDIDATE_FEATURES if not features_out[n]["admitted"]],
    }
    OUT_PATH.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT_PATH}")
    print("admitted:", out["admitted_features"])
    print("dropped:", out["dropped_features"])


if __name__ == "__main__":
    main()
