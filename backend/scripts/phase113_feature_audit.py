"""Phase-113 design-stage feature audit.

Permutation-sensitivity and statistical-power audit for the
Phase-113 new candidate families B and C, run on KNOWN panel
corpora ONLY (never Indus, never the synthetic controls) before
any spec freeze. For each known corpus: 20 original draws at
N = 11,000 (seed stream [20261020, corpus_index, draw], the same
stream as the Phase-112 audit so the draws coincide) and their
within-text permuted counterparts (seed stream
[20261021, corpus_index, draw]); plus 20 power draws at
N = 7,002 (seed stream [20261024, corpus_index, draw]).

Admission: a new candidate is admitted iff (i) the permutation
audit passes (median |Cohen d| >= 0.8 across the known corpora,
same-sign mean difference in >= 8 corpora, SD of original draws
> 0 in >= 5 corpora) AND (ii) the power audit passes (median
pairwise |Cohen d| between the 8 known-label classes at
N = 7,002 >= 0.5).

Output: reports/phase113_feature_audit.json, including the
LDA ladder power at N = 7,002 (ladder A alone, A + admitted B,
A + admitted B + admitted C) and the indeterminate-criterion
flags.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""
import itertools
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab import phase111_custodian as custodian  # noqa: E402
from glossa_lab.phase112_analyst import FAMILIES, NONLING, LDA  # noqa: E402
from glossa_lab.phase112_features import FEATURE_NAMES  # noqa: E402
from glossa_lab.phase112_features import extract_candidates as extract_candidates112  # noqa: E402
from glossa_lab.phase113_features import (  # noqa: E402
    LADDER_A,
    NEW_CANDIDATES,
    NEW_CANDIDATES_B,
    NEW_CANDIDATES_C,
    extract_new_candidates,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
# Phase-113 staged copies of the openly-licensed downloads
# (gitignored local store; identical files, identical licenses).
custodian.SOURCES = REPO_ROOT / "glossa-corpus" / "indus" / "sources" / "phase113"

N_DRAWS = 20
N_TOKENS = 11_000
N_POWER_TOKENS = 7_002
KNOWN_CODES = [code for _i, code, role in custodian.MEMBERS if role in ("known", "nonling")]
CORPUS_INDEX = {code: i for i, code, _r in custodian.MEMBERS}
CLASSES = sorted(set(custodian.KNOWN_LABELS.values()))

OUT_PATH = REPO_ROOT / "reports" / "phase113_feature_audit.json"


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


def _job(args: tuple[str, int, list[list[int]], str]) -> tuple[str, int, dict[str, float]]:
    code, draw_index, draw, kind = args
    if kind == "permuted":
        return code, draw_index, extract_new_candidates(draw, draw_index=draw_index)
    feats = extract_candidates112(draw, draw_index=draw_index)
    feats.update(extract_new_candidates(draw, draw_index=draw_index))
    return code, draw_index, feats


def _cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """112's exact formula: ddof=1 SDs, pooled = sqrt((sd_a^2 + sd_b^2) / 2)."""
    sd_a, sd_b = float(a.std(ddof=1)), float(b.std(ddof=1))
    pooled = np.sqrt((sd_a**2 + sd_b**2) / 2) if (sd_a + sd_b) > 0 else 0.0
    return float((a.mean() - b.mean()) / pooled) if pooled > 0 else 0.0


def _median_abs(values: list[float]) -> float:
    abs_vals = sorted(abs(v) for v in values)
    n = len(abs_vals)
    if n % 2 == 1:
        return float(abs_vals[n // 2])
    return float((abs_vals[n // 2 - 1] + abs_vals[n // 2]) / 2)


def _balanced_accuracy(y_true: list[str], y_pred: list[str], classes: list[str]) -> float:
    recalls = []
    for cls in classes:
        mask = [t == cls for t in y_true]
        n = sum(mask)
        if n == 0:
            continue
        correct = sum(1 for t, p, m in zip(y_true, y_pred, mask) if m and p == cls)
        recalls.append(correct / n)
    return float(np.mean(recalls)) if recalls else 0.0


def main() -> None:
    per_corpus: dict[str, dict] = {}
    jobs: list[tuple[str, int, list[list[int]], str]] = []
    job_meta: list[tuple[str, int, str]] = []  # (code, draw, kind)
    for code in KNOWN_CODES:
        cidx = CORPUS_INDEX[code]
        kind, loader = custodian.LOADERS[code]
        payload, stats = loader()
        texts = custodian.chunk_stream(payload, cidx) if kind == "stream" else payload
        texts_int = _int_texts(texts)
        per_corpus[code] = {"corpus_index": cidx, "loader_stats": stats,
                            "texts_after_chunking": len(texts_int)}
        for draw_index in range(N_DRAWS):
            rng = np.random.default_rng(np.random.SeedSequence([20261020, cidx, draw_index]))
            draw = custodian.resample_draw(texts_int, N_TOKENS, rng)
            jobs.append((code, draw_index, draw, "original"))
            job_meta.append((code, draw_index, "original"))
            rng_p = np.random.default_rng(np.random.SeedSequence([20261021, cidx, draw_index]))
            perm = _permute_draw(draw, rng_p)
            jobs.append((code, draw_index, perm, "permuted"))
            job_meta.append((code, draw_index, "permuted"))
        for draw_index in range(N_DRAWS):
            rng = np.random.default_rng(np.random.SeedSequence([20261024, cidx, draw_index]))
            draw = custodian.resample_draw(texts_int, N_POWER_TOKENS, rng)
            jobs.append((code, draw_index, draw, "power"))
            job_meta.append((code, draw_index, "power"))
        print(f"loaded {code}: {len(texts_int)} texts", flush=True)

    with Pool(2) as pool:
        results = pool.map(_job, jobs)
    values: dict[tuple[str, int, str], dict[str, float]] = {}
    for (code, draw_index, feats), (_c, _d, kind) in zip(results, job_meta):
        values[(code, draw_index, kind)] = feats

    # ---- Permutation audit (original vs permuted at N = 11,000) ----
    permutation_audit: dict[str, dict] = {}
    for name in NEW_CANDIDATES:
        per_d: dict[str, float] = {}
        signs: dict[str, int] = {}
        nondeg = 0
        for code in KNOWN_CODES:
            orig = np.array([values[(code, d, "original")][name] for d in range(N_DRAWS)])
            perm = np.array([values[(code, d, "permuted")][name] for d in range(N_DRAWS)])
            per_d[code] = _cohens_d(orig, perm)
            signs[code] = int(np.sign(orig.mean() - perm.mean()))
            if float(orig.std(ddof=1)) > 0:
                nondeg += 1
        median_abs_d = _median_abs(list(per_d.values()))
        nonzero_signs = [s for s in signs.values() if s != 0]
        dominant_sign = max(set(nonzero_signs), key=nonzero_signs.count) if nonzero_signs else 0
        sign_consistency = int(sum(1 for s in signs.values() if s == dominant_sign))
        admitted = bool(median_abs_d >= 0.8 and sign_consistency >= 8 and nondeg >= 5)
        permutation_audit[name] = {
            "cohens_d_per_corpus": per_d,
            "median_abs_d": median_abs_d,
            "sign_consistency_corpora": sign_consistency,
            "nondegenerate_corpora": nondeg,
            "permutation_admitted": admitted,
        }
        print(f"perm {name:28s} median|d|={median_abs_d:8.3f} signs={sign_consistency} "
              f"nondeg={nondeg} admitted={admitted}", flush=True)

    # ---- Power analysis (pairwise class effect sizes) ----
    codes_by_class = {
        cls: [code for code in KNOWN_CODES if custodian.KNOWN_LABELS[code] == cls]
        for cls in CLASSES
    }
    power_analysis: dict[str, dict] = {}
    for name in NEW_CANDIDATES:
        entry: dict = {}
        for size_label, kind in (("7002", "power"), ("11000", "original")):
            pooled_by_class = {
                cls: np.array([values[(code, d, kind)][name]
                               for code in codes for d in range(N_DRAWS)])
                for cls, codes in codes_by_class.items()
            }
            pair_ds = [
                _cohens_d(pooled_by_class[a], pooled_by_class[b])
                for a, b in itertools.combinations(CLASSES, 2)
            ]
            entry[size_label] = {
                "median_pairwise_abs_d": _median_abs(pair_ds),
                "min_pairwise_abs_d": float(min(abs(v) for v in pair_ds)) if pair_ds else 0.0,
            }
        entry["power_admitted"] = bool(entry["7002"]["median_pairwise_abs_d"] >= 0.5)
        power_analysis[name] = entry
        print(f"power {name:28s} median|d|@7002={entry['7002']['median_pairwise_abs_d']:8.3f} "
              f"median|d|@11000={entry['11000']['median_pairwise_abs_d']:8.3f} "
              f"admitted={entry['power_admitted']}", flush=True)

    admitted_b = [n for n in NEW_CANDIDATES_B
                  if permutation_audit[n]["permutation_admitted"]
                  and power_analysis[n]["power_admitted"]]
    admitted_c = [n for n in NEW_CANDIDATES_C
                  if permutation_audit[n]["permutation_admitted"]
                  and power_analysis[n]["power_admitted"]]
    admitted_new_features = {"B": admitted_b, "C": admitted_c}

    # ---- Ladder power at N = 7,002 (train draws 0-9, test 10-19) ----
    feature_sets = {
        "A16": list(LADDER_A),
        "A16+B_admitted": list(LADDER_A) + admitted_b,
        "A16+B_admitted+C_admitted": list(LADDER_A) + admitted_b + admitted_c,
    }
    assert LADDER_A == FEATURE_NAMES
    ladder: dict[str, dict] = {}
    for set_name, feature_names in feature_sets.items():
        x_train, y_train, x_test, y_test = [], [], [], []
        for code in KNOWN_CODES:
            label = custodian.KNOWN_LABELS[code]
            for d in range(10):
                x_train.append([values[(code, d, "power")][f] for f in feature_names])
                y_train.append(label)
            for d in range(10, N_DRAWS):
                x_test.append([values[(code, d, "power")][f] for f in feature_names])
                y_test.append(label)
        x_train_arr = np.array(x_train, dtype=np.float64)
        x_test_arr = np.array(x_test, dtype=np.float64)
        classes = sorted(set(y_train))
        model = LDA().fit(x_train_arr, np.array(y_train), classes)
        pred_all = model.predict(x_test_arr)
        # Family BA over the 7 families (non_linguistic draws excluded, as G2).
        fam_true = [t for t in y_test if t in FAMILIES]
        fam_pred = [p for t, p in zip(y_test, pred_all) if t in FAMILIES]
        family_ba = _balanced_accuracy(fam_true, fam_pred, FAMILIES)
        # Binary linguistic BA (as G1): linguistic iff the summed family
        # posterior >= the non_linguistic posterior.
        post_test = model.posterior(x_test_arr)
        cls_index = {c: i for i, c in enumerate(model.classes_)}
        ling_cols = [cls_index[c] for c in FAMILIES if c in cls_index]
        nonling_col = cls_index[NONLING]
        ling_post = post_test[:, ling_cols].sum(axis=1)
        pred_binary = ["linguistic" if lp >= post_test[i, nonling_col] else "non_linguistic"
                       for i, lp in enumerate(ling_post)]
        true_binary = ["non_linguistic" if t == NONLING else "linguistic" for t in y_test]
        binary_ba = _balanced_accuracy(true_binary, pred_binary,
                                       ["linguistic", "non_linguistic"])
        ladder[set_name] = {
            "features": feature_names,
            "family_balanced_accuracy": family_ba,
            "binary_linguistic_balanced_accuracy": binary_ba,
        }
        print(f"ladder {set_name:32s} family BA={family_ba:.4f} binary BA={binary_ba:.4f}",
              flush=True)

    full_family_ba = ladder["A16+B_admitted+C_admitted"]["family_balanced_accuracy"]
    criterion_a = bool(len(admitted_b) + len(admitted_c) < 3)
    criterion_b = bool(full_family_ba < 0.70)
    indeterminate = {
        "criterion_a_total_admitted_new_lt_3": criterion_a,
        "criterion_b_full_ladder_family_ba_at_7002_lt_0.70": criterion_b,
        "fires": bool(criterion_a or criterion_b),
    }

    out = {
        "study": "Phase-113 design-stage feature audit (families B and C)",
        "date": "2026-10-07",
        "panel": "known corpora only (K1,K2,K3,K4,K5,K7,K8,K9,N1 as assembled under spec 009)",
        "draws_per_corpus": N_DRAWS,
        "tokens_per_draw": N_TOKENS,
        "power_tokens_per_draw": N_POWER_TOKENS,
        "draw_seed_stream": "[20261020, corpus_index, draw_index]",
        "permutation_seed_stream": "[20261021, corpus_index, draw_index]",
        "power_seed_stream": "[20261024, corpus_index, draw_index]",
        "permutation_admission_rule": (
            "median |Cohen d| >= 0.8 AND same-sign mean difference in >= 8 corpora "
            "AND SD(original) > 0 in >= 5 corpora"
        ),
        "power_admission_rule": "median pairwise |Cohen d| over the 28 class pairs at N=7002 >= 0.5",
        "corpora": per_corpus,
        "permutation_audit": permutation_audit,
        "power_analysis": power_analysis,
        "admitted_new_features": admitted_new_features,
        "ladder_power_at_7002": ladder,
        "indeterminate": indeterminate,
    }
    OUT_PATH.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT_PATH}")
    print("admitted B:", admitted_b)
    print("admitted C:", admitted_c)
    print("indeterminate:", indeterminate)


if __name__ == "__main__":
    main()
