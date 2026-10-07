"""Phase-112 custodian (spec 010 sections 5-6).

Builds the blinded panel exactly as spec 009 built Phase-111's —
same corpora, same frozen loaders / chunking / resampling / token
remap (reused by import from the frozen phase111_custodian; its
SOURCES global is redirected to the Phase-112 staged copies of the
identical downloads) — with three spec-010 differences:

  1. features come from phase112_features (the admitted
     order-carrying set frozen in spec 010 section 4);
  2. a fifth synthetic control, S5 (positional-bigram template
     generator, spec 010 section 5), joins S1-S4 as a blind member;
  3. all state lives under .glossa-state/phase112/ and the panel
     file is stamped spec 010.

The analyst module never imports this module.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from glossa_lab import phase111_custodian as c111
from glossa_lab.phase112_features import FEATURE_NAMES, extract_features

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES = REPO_ROOT / "glossa-corpus" / "indus" / "sources" / "phase112"
STATE_DIR = REPO_ROOT / ".glossa-state" / "phase112"

# The frozen spec-009 loaders read from their module-global SOURCES;
# redirect it to the Phase-112 staged copies (identical files,
# verified byte- or loader-equivalent against the Phase-111 build
# log; see reports/phase112_acquisition_log.json).
c111.SOURCES = SOURCES

MASTER_SEED = c111.MASTER_SEED
N_PRIMARY = c111.N_PRIMARY
N_DRAWS = c111.N_DRAWS
KNOWN_LABELS = c111.KNOWN_LABELS

# Panel members: spec 009's frozen list (identical order/indices)
# plus S5 at corpus_index 35.
MEMBERS: list[tuple[int, str, str]] = list(c111.MEMBERS) + [
    (35, "S5_positional_bigram_gen", "synthetic"),
]

LOADERS = c111.LOADERS


# --------------------------------------------------------------------------
# S5: positional-bigram template generator (spec 010 section 5)
# --------------------------------------------------------------------------

S5_BINS = 5
S5_BETA = 1.0  # interpolation weight toward the positional unigram


def _s5_bin(j: int, length: int) -> int:
    return (S5_BINS * j) // length


def s5_generator(r1_texts: list[list[str]]) -> tuple[list[list[str]], dict]:
    """Generate S5 texts from R1 statistics.

    Model (frozen, spec 010 section 5): relative-position bins
    b(j, L) = floor(5j / L). From R1: positional unigram counts
    U_b(x) per bin, and adjacent-pair counts C_{b,b'}(x -> y) per
    bin pair. A generated text of length L: x_0 ~ U_{b(0,L)};
    for j >= 1, with b = b(j-1, L), b' = b(j, L):
        P(y | x_{j-1}) = (C_{b,b'}(x_{j-1} -> y) + beta * U_{b'}(y))
                         / (C_{b,b'}(x_{j-1} -> .) + beta),
    beta = 1.0. Lengths from the frozen target distribution; texts
    generated until >= 5 x N_PRIMARY tokens. Seed stream
    [20261009, 5] (the spec-009 generator seed family). There is NO
    disclosed training instance of S5 and no gen class for it in the
    final model (spec 010 section 6).
    """
    pos_uni: dict[int, Counter] = defaultdict(Counter)
    pair_counts: dict[tuple[int, int], dict[str, Counter]] = defaultdict(
        lambda: defaultdict(Counter))
    for t in r1_texts:
        length = len(t)
        for j, tok in enumerate(t):
            pos_uni[_s5_bin(j, length)][tok] += 1
        for j in range(length - 1):
            pair_counts[(_s5_bin(j, length), _s5_bin(j + 1, length))][t[j]][t[j + 1]] += 1

    # Positional unigram distributions over sorted supports.
    uni_dist: dict[int, tuple[list[str], np.ndarray]] = {}
    for b, counter in pos_uni.items():
        vs = sorted(counter.keys())
        ws = np.array([counter[v] for v in vs], dtype=float)
        uni_dist[b] = (vs, ws / ws.sum())

    rng = np.random.default_rng(np.random.SeedSequence([20261009, 5]))
    need = 5 * N_PRIMARY
    lengths = c111._target_lengths(rng, need)

    # Cache successor distributions per (b, b', x).
    cache: dict[tuple[int, int, str], tuple[list[str], np.ndarray]] = {}

    def successor_dist(b: int, bp: int, x: str) -> tuple[list[str], np.ndarray]:
        key = (b, bp, x)
        if key in cache:
            return cache[key]
        support, base = uni_dist[bp]
        base_map = dict(zip(support, base))
        counts = pair_counts.get((b, bp), {}).get(x, Counter())
        total = sum(counts.values())
        vs = sorted(set(support) | set(counts.keys()))
        probs = np.array([
            (counts.get(y, 0) + S5_BETA * base_map.get(y, 0.0)) / (total + S5_BETA)
            for y in vs
        ])
        probs = probs / probs.sum()
        cache[key] = (vs, probs)
        return cache[key]

    texts: list[list[str]] = []
    for length in lengths:
        text: list[str] = []
        for j in range(length):
            if j == 0:
                vs, ws = uni_dist[_s5_bin(0, length)]
                text.append(str(rng.choice(vs, p=ws)))
            else:
                vs, ws = successor_dist(
                    _s5_bin(j - 1, length), _s5_bin(j, length), text[-1])
                text.append(str(rng.choice(vs, p=ws)))
        texts.append(text)

    # Unigram fidelity: total variation distance to R1's unigram
    # distribution (recorded in the build log per spec 010 section 5).
    r1_uni = Counter(tok for t in r1_texts for tok in t)
    s5_uni = Counter(tok for t in texts for tok in t)
    r1_total = sum(r1_uni.values())
    s5_total = sum(s5_uni.values())
    vocab = set(r1_uni) | set(s5_uni)
    tv = 0.5 * sum(
        abs(r1_uni.get(v, 0) / r1_total - s5_uni.get(v, 0) / s5_total) for v in vocab)
    stats = {"texts": len(texts), "tokens": s5_total,
             "unigram_tv_distance_to_R1": float(tv)}
    return texts, stats


# --------------------------------------------------------------------------
# Panel build (mirrors spec 009's build; spec 010 differences noted)
# --------------------------------------------------------------------------


def build_panel(workers: int = 2) -> dict:
    """Build the full anonymized panel + key + build log.

    Writes panel.json and key.json into STATE_DIR (.glossa-state/
    phase112/). Returns the build log for the acquisition record.
    """
    from multiprocessing import Pool

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    build_log: dict[str, dict] = {}

    texts_by_code: dict[str, list[list[str]]] = {}
    for corpus_index, code, _role in MEMBERS:
        if code in LOADERS:
            kind, loader = LOADERS[code]
            payload, stats = loader()
            texts = c111.chunk_stream(payload, corpus_index) if kind == "stream" else payload
            texts_by_code[code] = texts
            build_log[code] = {"kind": kind, **stats,
                               "texts_after_chunking": len(texts)}
    # Synthetics derive from R1 (S1-S4 frozen spec-009 algorithms;
    # S5 the spec-010 positional-bigram generator).
    gens = c111._generators(texts_by_code["R1_indus_holdat_m77"])
    for code, texts in gens.items():
        texts_by_code[code] = texts
        build_log[code] = {"kind": "generated", "texts": len(texts),
                           "tokens": sum(len(t) for t in texts)}
    s5_texts, s5_stats = s5_generator(texts_by_code["R1_indus_holdat_m77"])
    texts_by_code["S5_positional_bigram_gen"] = s5_texts
    build_log["S5_positional_bigram_gen"] = {"kind": "generated", **s5_stats}

    remapped: dict[str, list[list[int]]] = {}
    for corpus_index, code, _role in MEMBERS:
        remapped[code] = c111._remap(texts_by_code[code], corpus_index)

    id_order = [code for _, code, _ in MEMBERS]
    rng_ids = np.random.default_rng(np.random.SeedSequence([20261007]))
    shuffled = [id_order[i] for i in rng_ids.permutation(len(id_order))]
    cid_of = {code: f"C{i + 1:02d}" for i, code in enumerate(shuffled)}

    feature_jobs: list[tuple[str, str, int, list[list[int]]]] = []
    for corpus_index, code, role in MEMBERS:
        texts_int = remapped[code]
        sizes = [("primary", N_PRIMARY)]
        if role in ("known", "nonling", "target"):
            sizes += [("sens_5000", 5_000), ("sens_19600", 19_600)]
        for size_label, n_tok in sizes:
            for draw_index in range(N_DRAWS):
                rng = np.random.default_rng(
                    np.random.SeedSequence([MASTER_SEED, corpus_index, draw_index]))
                draw = c111.resample_draw(texts_int, n_tok, rng)
                feature_jobs.append((code, size_label, draw_index, draw))

    # Disclosed generator TRAINING instances for S3/S4 only (spec 009
    # addendum A route, inherited): S5 has NO training instance.
    gen_train_codes = {"S3_heraldic_gen": ("gen_heraldic", 901),
                       "S4_admin_gen": ("gen_administrative", 902)}
    gen_train_texts = c111._generators(
        texts_by_code["R1_indus_holdat_m77"], seed_extra=777)
    for src_code, (_cls, cidx) in gen_train_codes.items():
        rem = c111._remap(gen_train_texts[src_code], cidx)
        for draw_index in range(N_DRAWS):
            rng = np.random.default_rng(
                np.random.SeedSequence([MASTER_SEED, cidx, draw_index]))
            draw = c111.resample_draw(rem, N_PRIMARY, rng)
            feature_jobs.append((f"GENTRAIN:{src_code}", "primary", draw_index, draw))

    results: dict[tuple[str, str, int], dict[str, float]] = {}
    with Pool(workers) as pool:
        extracted = pool.starmap(
            _extract_job, [(job[3], job[2]) for job in feature_jobs])
    for (code, size_label, draw_index, _draw), feats in zip(feature_jobs, extracted):
        results[(code, size_label, draw_index)] = feats

    panel_members: dict[str, dict] = {}
    key: dict[str, dict] = {}
    for corpus_index, code, role in MEMBERS:
        cid = cid_of[code]
        entry: dict = {"label": KNOWN_LABELS.get(code) if role in ("known", "nonling") else None}
        for size_label in ("primary", "sens_5000", "sens_19600"):
            rows = []
            for draw_index in range(N_DRAWS):
                feats = results.get((code, size_label, draw_index))
                if feats is None:
                    continue
                rows.append([feats[name] for name in FEATURE_NAMES])
            if rows:
                entry[f"features_{size_label}"] = rows
        panel_members[cid] = entry
        key[cid] = {"code": code, "role": role,
                    "label": KNOWN_LABELS.get(code),
                    "corpus_index": corpus_index}

    generator_train: dict[str, list] = {}
    for src_code, (cls_name, _cidx) in gen_train_codes.items():
        rows = []
        for draw_index in range(N_DRAWS):
            feats = results[(f"GENTRAIN:{src_code}", "primary", draw_index)]
            rows.append([feats[name] for name in FEATURE_NAMES])
        generator_train[cls_name] = rows

    panel = {
        "spec": "010-phase112-blind-affiliation",
        "feature_names": FEATURE_NAMES,
        "n_primary": N_PRIMARY,
        "n_draws": N_DRAWS,
        "members": panel_members,
        "known_ids": [cid_of[c] for _, c, r in MEMBERS if r in ("known", "nonling")],
        "blind_ids": [cid_of[c] for _, c, r in MEMBERS if r in ("synthetic", "target")],
        "generator_train": generator_train,
    }
    (STATE_DIR / "panel.json").write_text(json.dumps(panel), encoding="utf-8")
    (STATE_DIR / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    (STATE_DIR / "build_log.json").write_text(json.dumps(build_log, indent=1), encoding="utf-8")
    return build_log


def _extract_job(draw: list[list[int]], draw_index: int) -> dict[str, float]:
    return extract_features(draw, draw_index=draw_index)
