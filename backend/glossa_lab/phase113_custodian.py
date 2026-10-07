"""Phase-113 custodian (spec 012 sections 1-7).

Builds the blinded panel exactly as spec 010 built Phase-112's —
same corpora, same frozen loaders / chunking / resampling / token
remap (reused by import from the frozen phase111_custodian and
phase112_custodian; their SOURCES global is redirected to the
Phase-113 staged copies of the identical downloads, whose loader
statistics were verified against the Phase-111 build log before
this freeze; see reports/phase113_acquisition_log.json) — with the
spec-012 differences:

  1. features are the frozen 30-feature ladder L3 (spec section 4:
     L1 = the Phase-112 16, L2 = L1 + admitted family B, L3 = L2 +
     admitted family C), extracted per draw by
     phase113_features.extract_all113 and sliced to ladder order;
  2. the panel build is CHECKPOINTED per (member, size) under
     .glossa-state/phase113/checkpoints/ so a crashed build resumes
     member-by-member instead of recomputing everything;
  3. the adversarial generator family G(theta) (spec section 6)
     and the deterministic 200-evaluation optimizer (spec
     section 7) live here, custodian-side, so the search can never
     leak identities into the analyst path.

The analyst module never imports this module.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from glossa_lab import phase111_custodian as c111
from glossa_lab import phase112_custodian as c112
from glossa_lab.phase112_features import FEATURE_NAMES as FEATURE_NAMES112
from glossa_lab.phase113_features import NEW_CANDIDATES_B, NEW_CANDIDATES_C, extract_all113

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES = REPO_ROOT / "glossa-corpus" / "indus" / "sources" / "phase113"
STATE_DIR = REPO_ROOT / ".glossa-state" / "phase113"
CHECKPOINT_DIR = STATE_DIR / "checkpoints"

# The frozen spec-009 loaders read from their module-global SOURCES;
# redirect it to the Phase-113 staged copies. NOTE: importing
# phase112_custodian above already redirected c111.SOURCES to the
# Phase-112 staging, so this assignment must come after the imports.
c111.SOURCES = SOURCES

MASTER_SEED = c111.MASTER_SEED
N_PRIMARY = c111.N_PRIMARY
N_DRAWS = c111.N_DRAWS
KNOWN_LABELS = c112.KNOWN_LABELS
MEMBERS = c112.MEMBERS
LOADERS = c111.LOADERS

# ---------------------------------------------------------------------------
# Feature ladder (spec section 4, frozen)
# ---------------------------------------------------------------------------

LADDER_L1: list[str] = list(FEATURE_NAMES112)
ADMITTED_B: list[str] = [
    "blockH5",
    "blockH6",
    "mi_lag2",
    "mi_lag3",
    "rep_adj_4",
    "adj_clustering_lag2",
    "restore_acc_tri",
    "bigram_type_ratio_lag2",
]
ADMITTED_C: list[str] = [
    "dup_text_frac",
    "dup_token_coverage",
    "shared_bigram_type_frac",
    "cross_bigram_texts_mean",
    "longest_cross_repeat",
    "pair_bigram_overlap",
]
# Sanity at import time: the admitted sets are exactly the audit's,
# in the candidate modules' own order (the unit tests verify this
# against reports/phase113_feature_audit.json as well).
assert ADMITTED_B == [n for n in NEW_CANDIDATES_B if n in set(ADMITTED_B)]
assert ADMITTED_C == [n for n in NEW_CANDIDATES_C if n in set(ADMITTED_C)]
LADDER_L2: list[str] = LADDER_L1 + ADMITTED_B
LADDER_L3: list[str] = LADDER_L2 + ADMITTED_C
FEATURE_NAMES: list[str] = list(LADDER_L3)
LADDERS: list[list[str]] = [LADDER_L1, LADDER_L2, LADDER_L3]


def extract_ladder_features(texts_int: list[list[int]], draw_index: int) -> list[float]:
    """One draw's 30 ladder features, in frozen ladder order."""
    feats = extract_all113(texts_int, draw_index)
    return [float(feats[name]) for name in FEATURE_NAMES]


def _extract_job(draw: list[list[int]], draw_index: int) -> list[float]:
    return extract_ladder_features(draw, draw_index=draw_index)


# ---------------------------------------------------------------------------
# R1 access (the mapping the panel build uses)
# ---------------------------------------------------------------------------

R1_CODE = "R1_indus_holdat_m77"
R1_CORPUS_INDEX = next(idx for idx, code, _ in MEMBERS if code == R1_CODE)


def _r1_texts_str() -> list[list[str]]:
    """R1's texts in source tokens, via the frozen spec-009 loader."""
    _kind, loader = LOADERS[R1_CODE]
    payload, _stats = loader()
    return payload


def r1_texts_int() -> list[list[int]]:
    """R1's texts in the custodian int mapping the panel build used
    (c111._remap at R1's corpus_index over the sorted vocabulary)."""
    return c111._remap(_r1_texts_str(), R1_CORPUS_INDEX)


def _gen_train_texts() -> dict[str, list[list[str]]]:
    """Disclosed generator-training instances for S3/S4 (spec 009
    addendum A route, inherited): the frozen c111 generators with
    seed_extra=777, built from R1's source-token texts."""
    return c111._generators(_r1_texts_str(), seed_extra=777)


# ---------------------------------------------------------------------------
# Panel build (mirrors spec 010's build; checkpointed per member-size)
# ---------------------------------------------------------------------------


def _write_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload), encoding="utf-8")
    os.replace(tmp, path)


def _load_checkpoint(path: Path) -> list[list[float]] | None:
    """Checkpoint rows if the file exists with the right features."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if data.get("feature_names") != FEATURE_NAMES:
        return None
    rows = data.get("draws", data.get("rows"))
    return rows if isinstance(rows, list) else None


def build_panel(workers: int = 2) -> dict:
    """Build the full anonymized panel + key + build log.

    Writes panel.json and key.json into STATE_DIR (.glossa-state/
    phase113/). Each (member, size) group's 100 draws are
    checkpointed to checkpoints/<code>__<size_label>.json as soon as
    the group finishes; an existing checkpoint with the frozen L3
    feature names is loaded instead of recomputed. The disclosed
    generator-training rows are checkpointed the same way at
    checkpoints/gen_train.json. Returns the build log.
    """
    from multiprocessing import Pool

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
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
    # S5 the spec-010 positional-bigram generator, by import).
    gens = c111._generators(texts_by_code[R1_CODE])
    for code, texts in gens.items():
        texts_by_code[code] = texts
        build_log[code] = {"kind": "generated", "texts": len(texts),
                           "tokens": sum(len(t) for t in texts)}
    s5_texts, s5_stats = c112.s5_generator(texts_by_code[R1_CODE])
    texts_by_code["S5_positional_bigram_gen"] = s5_texts
    build_log["S5_positional_bigram_gen"] = {"kind": "generated", **s5_stats}

    remapped: dict[str, list[list[int]]] = {}
    for corpus_index, code, _role in MEMBERS:
        remapped[code] = c111._remap(texts_by_code[code], corpus_index)

    id_order = [code for _, code, _ in MEMBERS]
    rng_ids = np.random.default_rng(np.random.SeedSequence([20261007]))
    shuffled = [id_order[i] for i in rng_ids.permutation(len(id_order))]
    cid_of = {code: f"C{i + 1:02d}" for i, code in enumerate(shuffled)}

    # Per-(member, size) draw extraction, checkpointed group by group.
    draws_by_member_size: dict[tuple[str, str], list[list[float]]] = {}
    gen_train_by_class: dict[str, list[list[float]]] = {}
    with Pool(workers) as pool:
        for corpus_index, code, role in MEMBERS:
            texts_int = remapped[code]
            sizes = [("primary", N_PRIMARY)]
            if role in ("known", "nonling", "target"):
                sizes += [("sens_5000", 5_000), ("sens_19600", 19_600)]
            for size_label, n_tok in sizes:
                ckpt = CHECKPOINT_DIR / f"{code}__{size_label}.json"
                rows = _load_checkpoint(ckpt)
                if rows is None:
                    draws = []
                    for draw_index in range(N_DRAWS):
                        rng = np.random.default_rng(np.random.SeedSequence(
                            [MASTER_SEED, corpus_index, draw_index]))
                        draws.append(c111.resample_draw(texts_int, n_tok, rng))
                    rows = pool.starmap(
                        _extract_job, [(d, i) for i, d in enumerate(draws)])
                    rows = [[float(v) for v in row] for row in rows]
                    _write_json_atomic(ckpt, {"feature_names": FEATURE_NAMES,
                                              "draws": rows})
                draws_by_member_size[(code, size_label)] = rows

        # Disclosed generator TRAINING instances for S3/S4 only (spec
        # 009 addendum A route, inherited): S5 has NO training
        # instance and neither do the adversarial corpora.
        gen_train_codes = {"S3_heraldic_gen": ("gen_heraldic", 901),
                           "S4_admin_gen": ("gen_administrative", 902)}
        ckpt = CHECKPOINT_DIR / "gen_train.json"
        cached = _load_checkpoint(ckpt)
        cached_by_class = None
        if cached is not None and ckpt.exists():
            raw = json.loads(ckpt.read_text(encoding="utf-8"))
            if isinstance(raw.get("by_class"), dict):
                cached_by_class = raw["by_class"]
        if cached_by_class is not None:
            gen_train_by_class = cached_by_class
        else:
            gen_train_texts = _gen_train_texts()
            all_rows: list[list[float]] = []
            all_labels: list[str] = []
            for src_code, (cls_name, cidx) in gen_train_codes.items():
                rem = c111._remap(gen_train_texts[src_code], cidx)
                draws = []
                for draw_index in range(N_DRAWS):
                    rng = np.random.default_rng(np.random.SeedSequence(
                        [MASTER_SEED, cidx, draw_index]))
                    draws.append(c111.resample_draw(rem, N_PRIMARY, rng))
                rows = pool.starmap(
                    _extract_job, [(d, i) for i, d in enumerate(draws)])
                rows = [[float(v) for v in row] for row in rows]
                gen_train_by_class[cls_name] = rows
                all_rows.extend(rows)
                all_labels.extend([cls_name] * len(rows))
            _write_json_atomic(ckpt, {
                "feature_names": FEATURE_NAMES,
                "rows": [{name: row[i] for i, name in enumerate(FEATURE_NAMES)}
                         for row in all_rows],
                "labels": all_labels,
                "by_class": gen_train_by_class,
            })

    panel_members: dict[str, dict] = {}
    key: dict[str, dict] = {}
    for corpus_index, code, role in MEMBERS:
        cid = cid_of[code]
        entry: dict = {"label": KNOWN_LABELS.get(code) if role in ("known", "nonling") else None}
        for size_label in ("primary", "sens_5000", "sens_19600"):
            rows = draws_by_member_size.get((code, size_label))
            if rows:
                entry[f"features_{size_label}"] = rows
        panel_members[cid] = entry
        key[cid] = {"code": code, "role": role,
                    "label": KNOWN_LABELS.get(code),
                    "corpus_index": corpus_index}

    gen_train_rows: list[dict[str, float]] = []
    gen_train_labels: list[str] = []
    for cls_name in sorted(gen_train_by_class):
        for row in gen_train_by_class[cls_name]:
            gen_train_rows.append({name: row[i] for i, name in enumerate(FEATURE_NAMES)})
            gen_train_labels.append(cls_name)

    panel = {
        "spec": "012-phase113-blind-affiliation",
        "feature_names": FEATURE_NAMES,
        "n_primary": N_PRIMARY,
        "n_draws": N_DRAWS,
        "members": panel_members,
        "known_ids": [cid_of[c] for _, c, r in MEMBERS if r in ("known", "nonling")],
        "blind_ids": [cid_of[c] for _, c, r in MEMBERS if r in ("synthetic", "target")],
        "generator_train": gen_train_by_class,
        "gen_train": {"rows": gen_train_rows, "labels": gen_train_labels},
    }
    (STATE_DIR / "panel.json").write_text(json.dumps(panel), encoding="utf-8")
    (STATE_DIR / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    (STATE_DIR / "build_log.json").write_text(json.dumps(build_log, indent=1), encoding="utf-8")
    return build_log


# ---------------------------------------------------------------------------
# Adversarial generator family G(theta) (spec section 6)
# ---------------------------------------------------------------------------

ADV_BINS = 5
ADV_TARGET_TOKENS = 5 * N_PRIMARY

# theta_S5: pure positional-bigram mode at beta_P2 = 1.0 reproduces
# S5's construction (spec section 6 sanity anchor).
THETA_S5: tuple = (0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0)

THETA_NAMES: list[str] = [
    "w_P1", "w_P2", "w_P3", "w_G2", "w_G3",
    "beta_P2", "beta_P3", "beta_G2", "beta_G3", "p_burst", "p_copy",
]


def theta_to_dict(theta) -> dict[str, float]:
    """Named view of an 11-coordinate theta, for reporting."""
    return {name: float(v) for name, v in zip(THETA_NAMES, theta)}


def _adv_bin(j: int, length: int) -> int:
    return (ADV_BINS * j) // length


class AdvGen:
    """The parametric adversarial generator G(theta) of spec section 6.

    Built from R1's chunked texts in the custodian int mapping (the
    panel's R1 mapping). All component statistics are dense
    distributions over the token-id space, or Counters keyed by
    token id, precomputed once; per-context distributions are
    cached. Generation is deterministic given (theta, seed): the
    RNG consumption order is frozen — per text: length draw, then
    (if a previous text exists) copy draw and possibly copy-source
    draw; per token: burst draw, then mode draw, then value draw.
    """

    def __init__(self, r1_texts: list[list[int]]):
        texts = [list(t) for t in r1_texts if len(t) > 0]
        if not texts:
            raise ValueError("AdvGen needs a non-empty R1 corpus")
        self.texts = texts
        self.vocab: list[int] = sorted({tok for t in texts for tok in t})
        self.vocab_size: int = int(max(self.vocab)) + 1
        v = self.vocab_size

        uni_counts = np.zeros(v, dtype=np.float64)
        for t in texts:
            for tok in t:
                uni_counts[tok] += 1
        self.unigram: np.ndarray = uni_counts / uni_counts.sum()

        pos_counts = np.zeros((ADV_BINS, v), dtype=np.float64)
        for t in texts:
            length = len(t)
            for j, tok in enumerate(t):
                pos_counts[_adv_bin(j, length), tok] += 1
        self.pos_unigram: np.ndarray = np.zeros_like(pos_counts)
        for b in range(ADV_BINS):
            total = pos_counts[b].sum()
            self.pos_unigram[b] = pos_counts[b] / total if total > 0 else self.unigram

        self.pos_bigram: dict[tuple[int, int], dict[int, Counter]] = defaultdict(
            lambda: defaultdict(Counter))
        self.pos_trigram: dict[tuple[int, int, int], dict[tuple[int, int], Counter]] = (
            defaultdict(lambda: defaultdict(Counter)))
        self.glob_bigram: dict[int, Counter] = defaultdict(Counter)
        self.glob_trigram: dict[tuple[int, int], Counter] = defaultdict(Counter)
        for t in texts:
            length = len(t)
            for j in range(length - 1):
                b, bp = _adv_bin(j, length), _adv_bin(j + 1, length)
                self.pos_bigram[(b, bp)][t[j]][t[j + 1]] += 1
                self.glob_bigram[t[j]][t[j + 1]] += 1
            for j in range(length - 2):
                b = _adv_bin(j, length)
                bp = _adv_bin(j + 1, length)
                bpp = _adv_bin(j + 2, length)
                self.pos_trigram[(b, bp, bpp)][(t[j], t[j + 1])][t[j + 2]] += 1
                self.glob_trigram[(t[j], t[j + 1])][t[j + 2]] += 1

        length_counter = Counter(len(t) for t in texts)
        self.length_values: np.ndarray = np.array(
            sorted(length_counter), dtype=np.int64)
        self.length_cum: np.ndarray = np.cumsum(
            np.array([length_counter[int(length)] for length in self.length_values],
                     dtype=np.int64))
        self.length_total: int = int(self.length_cum[-1])

        self._cache_p1: dict = {}
        self._cache_p2: dict = {}
        self._cache_p3: dict = {}
        self._cache_g2: dict = {}
        self._cache_g3: dict = {}

    # -- component distributions (dense, normalized, cached) --------

    def _dense(self, counter: Counter | None) -> np.ndarray:
        vec = np.zeros(self.vocab_size, dtype=np.float64)
        if counter:
            for tok, count in counter.items():
                vec[tok] = count
        return vec

    def _dist_p1(self, b: int) -> np.ndarray:
        if b not in self._cache_p1:
            self._cache_p1[b] = np.array(self.pos_unigram[b], dtype=np.float64)
        return self._cache_p1[b]

    def _dist_p2(self, x: int, b: int, bp: int, beta2: float) -> np.ndarray:
        key = (x, b, bp, float(beta2))
        if key not in self._cache_p2:
            counts = self.pos_bigram.get((b, bp), {}).get(x, Counter())
            vec = self._dense(counts) + float(beta2) * self.pos_unigram[bp]
            total = vec.sum()
            self._cache_p2[key] = vec / total if total > 0 else np.array(
                self.pos_unigram[bp], dtype=np.float64)
        return self._cache_p2[key]

    def _dist_p3(self, x: int, y: int, b: int, bp: int, bpp: int,
                 beta3: float, beta2: float) -> np.ndarray:
        key = (x, y, b, bp, bpp, float(beta3), float(beta2))
        if key not in self._cache_p3:
            counts = self.pos_trigram.get((b, bp, bpp), {}).get((x, y), Counter())
            backoff = self._dist_p2(y, bp, bpp, beta2)
            vec = self._dense(counts) + float(beta3) * backoff
            total = vec.sum()
            self._cache_p3[key] = vec / total if total > 0 else backoff
        return self._cache_p3[key]

    def _dist_g2(self, x: int, beta_g2: float) -> np.ndarray:
        key = (x, float(beta_g2))
        if key not in self._cache_g2:
            vec = self._dense(self.glob_bigram.get(x, Counter())) + float(beta_g2) * self.unigram
            total = vec.sum()
            self._cache_g2[key] = vec / total if total > 0 else np.array(
                self.unigram, dtype=np.float64)
        return self._cache_g2[key]

    def _dist_g3(self, x: int, y: int, beta_g3: float, beta_g2: float) -> np.ndarray:
        key = (x, y, float(beta_g3), float(beta_g2))
        if key not in self._cache_g3:
            backoff = self._dist_g2(y, beta_g2)
            vec = self._dense(self.glob_trigram.get((x, y), Counter())) + float(beta_g3) * backoff
            total = vec.sum()
            self._cache_g3[key] = vec / total if total > 0 else backoff
        return self._cache_g3[key]

    # -- generation ---------------------------------------------------

    @staticmethod
    def _sample(dist: np.ndarray, rng: np.random.Generator) -> int:
        idx = int(np.searchsorted(np.cumsum(dist), rng.random()))
        return min(idx, len(dist) - 1)

    def generate(self, theta, seed_seq) -> list[list[int]]:
        """Generate texts under theta until >= 5 * N_PRIMARY tokens.

        theta is the 11-tuple (w_P1..w_G3, beta_P2, beta_P3, beta_G2,
        beta_G3, p_burst, p_copy) in spec section 6 coordinate order.
        """
        w = [float(v) for v in theta[:5]]
        beta_p2, beta_p3, beta_g2, beta_g3 = (float(v) for v in theta[5:9])
        p_burst, p_copy = float(theta[9]), float(theta[10])
        if isinstance(seed_seq, np.random.SeedSequence):
            seed = seed_seq
        else:
            seed = np.random.SeedSequence(seed_seq)
        rng = np.random.default_rng(seed)
        cumsum_w = np.cumsum(np.array(w, dtype=np.float64))

        texts: list[list[int]] = []
        total = 0
        while total < ADV_TARGET_TOKENS:
            # length draw (one rng.integers over the cumulative table)
            draw = int(rng.integers(0, self.length_total))
            li = int(np.searchsorted(self.length_cum, draw, side="right"))
            length = int(self.length_values[min(li, len(self.length_values) - 1)])
            # copy draw (+ source draw) — the first text is never a copy
            if texts and rng.random() < p_copy:
                src = int(rng.integers(0, len(texts)))
                copied = list(texts[src])
                texts.append(copied)
                total += len(copied)
                continue
            text: list[int] = []
            for j in range(length):
                if j == 0:
                    text.append(self._sample(self._dist_p1(_adv_bin(0, length)), rng))
                    continue
                # burst draw
                if rng.random() < p_burst:
                    text.append(text[-1])
                    continue
                # mode draw
                mode = min(int(np.searchsorted(cumsum_w, rng.random())), 4)
                if mode == 2 and j == 1:
                    mode = 1  # P3 falls back to P2 with one predecessor
                elif mode == 4 and j == 1:
                    mode = 3  # G3 falls back to G2 with one predecessor
                # value draw
                if mode == 0:
                    dist = self._dist_p1(_adv_bin(j, length))
                elif mode == 1:
                    dist = self._dist_p2(text[j - 1], _adv_bin(j - 1, length),
                                         _adv_bin(j, length), beta_p2)
                elif mode == 2:
                    dist = self._dist_p3(text[j - 2], text[j - 1],
                                         _adv_bin(j - 2, length), _adv_bin(j - 1, length),
                                         _adv_bin(j, length), beta_p3, beta_p2)
                elif mode == 3:
                    dist = self._dist_g2(text[j - 1], beta_g2)
                else:
                    dist = self._dist_g3(text[j - 2], text[j - 1], beta_g3, beta_g2)
                text.append(self._sample(dist, rng))
            texts.append(text)
            total += len(text)
        return texts


# ---------------------------------------------------------------------------
# Corpus distances (optimizer constraints / corpus statistics)
# ---------------------------------------------------------------------------


def unigram_tv(texts_a: list[list[int]], texts_b: list[list[int]]) -> float:
    """Total-variation distance between two corpora's unigram
    distributions, over the union support."""
    counts_a = Counter(tok for t in texts_a for tok in t)
    counts_b = Counter(tok for t in texts_b for tok in t)
    total_a = sum(counts_a.values())
    total_b = sum(counts_b.values())
    if total_a == 0 or total_b == 0:
        return 1.0
    vocab = set(counts_a) | set(counts_b)
    return float(0.5 * sum(
        abs(counts_a.get(v, 0) / total_a - counts_b.get(v, 0) / total_b)
        for v in vocab))


def positional_bigram_tv(texts_a: list[list[int]], texts_b: list[list[int]]) -> float:
    """Frequency-weighted mean positional-bigram TV between corpora.

    For every context (b, b', x) — relative-position bins of adjacent
    positions and the token at the first position — present in either
    corpus, the TV between the two corpora's empirical successor
    distributions for that context; contexts are weighted by their
    token count in texts_b.
    """
    def _contexts(texts):
        ctx: dict[tuple[int, int, int], Counter] = defaultdict(Counter)
        for t in texts:
            length = len(t)
            for j in range(length - 1):
                key = (_adv_bin(j, length), _adv_bin(j + 1, length), t[j])
                ctx[key][t[j + 1]] += 1
        return ctx

    ctx_a = _contexts(texts_a)
    ctx_b = _contexts(texts_b)
    weighted = 0.0
    weight_total = 0
    for key in set(ctx_a) | set(ctx_b):
        succ_a = ctx_a.get(key, Counter())
        succ_b = ctx_b.get(key, Counter())
        weight = sum(succ_b.values())
        if weight == 0:
            continue
        total_a = sum(succ_a.values())
        succ_vocab = set(succ_a) | set(succ_b)
        tv = 0.5 * sum(
            abs((succ_a.get(y, 0) / total_a if total_a else 0.0)
                - succ_b.get(y, 0) / weight)
            for y in succ_vocab)
        weighted += weight * tv
        weight_total += weight
    return float(weighted / weight_total) if weight_total else 0.0


# ---------------------------------------------------------------------------
# Optimizer (spec section 7)
# ---------------------------------------------------------------------------

BETA_GRID: tuple = (0.3, 1.0, 3.0)
N_EVALUATIONS = 200
N_RANDOM_CANDIDATES = 120


def rank_key(feasible: bool, n_violations: int, objective: float,
             eval_index: int) -> tuple:
    """Spec section 7 ranking; larger is better. Feasible outranks
    infeasible; among infeasible fewer violations wins, then higher
    objective; ties broken by lower eval_index."""
    return (1 if feasible else 0, -int(n_violations), float(objective),
            -int(eval_index))


def _random_theta(rng: np.random.Generator) -> tuple:
    w = rng.dirichlet([1.0, 1.0, 1.0, 1.0, 1.0])
    beta_p2 = BETA_GRID[int(rng.integers(0, 3))]
    beta_p3 = BETA_GRID[int(rng.integers(0, 3))]
    beta_g2 = BETA_GRID[int(rng.integers(0, 3))]
    beta_g3 = BETA_GRID[int(rng.integers(0, 3))]
    p_burst = float(rng.uniform(0, 0.25))
    p_copy = float(rng.uniform(0, 0.30))
    return (float(w[0]), float(w[1]), float(w[2]), float(w[3]), float(w[4]),
            float(beta_p2), float(beta_p3), float(beta_g2), float(beta_g3),
            p_burst, p_copy)


def _refine_theta(base: tuple, slot: int, rng: np.random.Generator) -> tuple:
    theta = list(base)
    k = slot % 11
    if k < 5:
        weights = [float(v) for v in theta[:5]]
        weights[k] *= math.exp(float(rng.normal(0, 0.35)))
        total = sum(weights)
        if total > 0:
            weights = [v / total for v in weights]
        theta[:5] = weights
    elif k <= 8:
        idx = min(range(len(BETA_GRID)),
                  key=lambda i: abs(BETA_GRID[i] - float(theta[k])))
        step = 1 if slot % 2 == 0 else -1
        theta[k] = BETA_GRID[min(max(idx + step, 0), len(BETA_GRID) - 1)]
    elif k == 9:
        theta[k] = min(max(float(theta[k]) + float(rng.uniform(-0.05, 0.05)), 0.0), 0.25)
    else:  # k == 10
        theta[k] = min(max(float(theta[k]) + float(rng.uniform(-0.05, 0.05)), 0.0), 0.30)
    return tuple(float(v) for v in theta)


def run_search(round_r: int, eval_fn, trace_path) -> tuple[tuple, list[dict]]:
    """The frozen 200-evaluation search of spec section 7.

    eval_fn(theta, eval_index) -> (objective, feasible, n_violations,
    detail dict). Every evaluation is appended as a JSON line to
    trace_path (flushed) before the next candidate is drawn; the
    file is truncated at the start, so re-running a round restarts
    its search deterministically from candidate 0. Returns
    (best_theta, trace records).
    """
    trace_path = Path(trace_path)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(np.random.SeedSequence([20261031, round_r]))
    trace: list[dict] = []
    best_theta: tuple | None = None
    best_key: tuple | None = None
    with open(trace_path, "w", encoding="utf-8") as handle:
        for eval_index in range(N_EVALUATIONS):
            if round_r == 1 and eval_index == 0:
                theta = tuple(float(v) for v in THETA_S5)
            elif eval_index < N_RANDOM_CANDIDATES or best_theta is None:
                theta = _random_theta(rng)
            else:
                theta = _refine_theta(best_theta, eval_index, rng)
            objective, feasible, n_violations, detail = eval_fn(theta, eval_index)
            record = {
                "eval_index": eval_index,
                "theta": [float(v) for v in theta],
                "objective": float(objective),
                "feasible": bool(feasible),
                "n_violations": int(n_violations),
                "detail": detail,
            }
            trace.append(record)
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            key = rank_key(bool(feasible), int(n_violations),
                           float(objective), eval_index)
            if best_key is None or key > best_key:
                best_key = key
                best_theta = theta
    if best_theta is None:  # unreachable: eval 0 always sets an incumbent
        raise RuntimeError("optimizer completed without an incumbent")
    return best_theta, trace


# ---------------------------------------------------------------------------
# Adversarial corpus plumbing (spec sections 2 and 7)
# ---------------------------------------------------------------------------


def generated_texts(theta, round_r: int, seed_extra: int,
                    advgen: AdvGen) -> list[list[int]]:
    """G(theta)'s raw output, in R1's own int-token space (seed
    stream [20261030, round_r, seed_extra])."""
    return advgen.generate(theta, [20261030, round_r, seed_extra])


def remap_texts(texts_int: list[list[int]], corpus_index: int) -> list[list[int]]:
    """The custodian token remap (frozen c111._remap)."""
    return c111._remap(texts_int, corpus_index)


def adversarial_texts(theta, round_r: int, seed_extra: int,
                      advgen: AdvGen) -> list[list[int]]:
    """The adversarial corpus for one evaluation / artifact: G(theta)
    generated with seed [20261030, round_r, seed_extra], then remapped
    at corpus_index 40 + round_r, as spec section 7 prescribes for
    draw construction."""
    return remap_texts(generated_texts(theta, round_r, seed_extra, advgen),
                       40 + round_r)


def primary_draws(texts_int: list[list[int]], corpus_index: int,
                  count: int) -> list[list[list[int]]]:
    """`count` primary-size (N=11,000) draws, seed stream
    [20261006, corpus_index, draw_index] (spec section 2)."""
    draws = []
    for draw_index in range(count):
        rng = np.random.default_rng(np.random.SeedSequence(
            [MASTER_SEED, corpus_index, draw_index]))
        draws.append(c111.resample_draw(texts_int, N_PRIMARY, rng))
    return draws


def draws_for(texts_int: list[list[int]], corpus_index: int,
              n_draws: int = 100) -> list[list[list[int]]]:
    """Alias for primary_draws with the round-artifact default."""
    return primary_draws(texts_int, corpus_index, n_draws)
