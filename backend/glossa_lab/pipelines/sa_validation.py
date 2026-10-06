"""Phase-107 (spec 005) — SA validation harness library.

Shared machinery for the Phase-52 v2 package: corpus/LM loaders, anchor
gold extraction (the Phase-52 pin procedure generalised to all H+M
anchors), k-fold construction, a pluggable-objective simulated-annealing
runner (full-rescoring path), constraint terms reusing the Phase-58/61/133
rule code, and an incremental (delta) scorer for the scaled run.

Nothing in this module modifies anchor data. SA output is evidence only.

GPU note (H20): torch is imported under guard; every artifact produced by
the phase107 scripts records ``gpu_device`` and the CPU path is announced,
never silent. BigramScorer is NumPy by design (see pipelines/decipher.py).
"""
from __future__ import annotations

import csv
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

try:
    import torch

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:  # torch absent on this VM — established Phase-52/106 pattern
    torch = None
    DEVICE = "cpu"

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

REPO = Path(__file__).resolve().parents[3]
HOLDAT_CSV = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
DATA = Path(__file__).resolve().parent.parent / "data"
DRAVIDIAN_LM = DATA / "dravidian_syllabic_lm.json"
SANSKRIT_LM = DATA / "sanskrit_syllable_lm.json"
GEEZ_TXT = DATA / "geez" / "Geez_Genesis_syllabic_nopunctuation.txt"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

MIN_SYLLABLE_FREQ = 3  # Phase-52's LM filter, replicated

# Phase-52's hardcoded HIGH syllabic pins (phase52_syllabic_sa.py,
# load_anchors_as_pins). Copied verbatim — the baseline's own values.
HIGH_SYLLABIC = {
    "M006": "pu",   # puli
    "M016": "ka",   # kaliru
    "M045": "ya",   # yanai
    "M062": "e",    # erutu
    "M099": "ko",   # kol
    "M176": "an",   # an
    "M342": "ay",   # ay
}

# Phase-61 phonotactics (phase61_phonotactic.py): Proto-Dravidian words
# cannot start with voiced stops / labio-dentals; romanised set.
PD_INVALID_INITIALS = set("bdfgqwx")
VOWEL_CHARS = set("aāiīuūeēoō")
FRONT_VOWELS = set("iīeē")   # Phase-61 / Phase-133e harmony classes
BACK_VOWELS = set("uūoō")


# ── Corpus ────────────────────────────────────────────────────────────────

def load_holdat_corpus() -> tuple[list[str], list[list[str]]]:
    """Holdat corpus, replicating phase52_syllabic_sa.load_corpus exactly."""
    seals: dict[str, list] = {}
    with open(HOLDAT_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
    inscriptions = [[s for s in v if s] for v in seals.values() if any(v)]
    flat = [s for insc in inscriptions for s in insc]
    return flat, inscriptions


# ── Language models ───────────────────────────────────────────────────────

def load_dravidian_lm() -> tuple[dict, list[str]]:
    """Dravidian syllabic LM, replicating phase52.load_syllabic_lm exactly."""
    raw = json.loads(DRAVIDIAN_LM.read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    syl_freq = raw.get("syllable_freq", {})
    valid = {s for s, c in syl_freq.items() if c >= MIN_SYLLABLE_FREQ}
    total = sum(v for k, v in bigrams.items()
                if k.split(",", 1)[0] in valid and k.split(",", 1)[1] in valid) or 1
    prob = {
        tuple(k.split(",", 1)): v / total
        for k, v in bigrams.items()
        if "," in k
        and k.split(",", 1)[0] in valid
        and k.split(",", 1)[1] in valid
    }
    return prob, sorted(valid)


def load_sanskrit_lm() -> tuple[dict, list[str]]:
    """Sanskrit syllabic LM (control i). File format: vocab list +
    'a|b'-keyed bigram counts (sanskrit_syllable_lm.json)."""
    raw = json.loads(SANSKRIT_LM.read_text("utf-8"))
    vocab = list(raw.get("vocab", []))
    vset = set(vocab)
    bigrams = raw.get("bigrams", {})
    items = []
    for k, v in bigrams.items():
        if "|" not in k:
            continue
        a, b = k.split("|", 1)
        if a in vset and b in vset:
            items.append(((a, b), float(v)))
    total = sum(v for _, v in items) or 1
    return {k: v / total for k, v in items}, sorted(vocab)


def build_geez_lm() -> tuple[dict, list[str]]:
    """Ge'ez syllabic LM (control ii) built from the in-repo Fuls Ge'ez
    Genesis syllabic corpus: whitespace-separated words, one Ethiopic
    character = one syllable; bigrams within words only."""
    text = GEEZ_TXT.read_text("utf-8")
    words = [w for w in re.split(r"\s+", text) if w]
    freq: Counter = Counter()
    big: Counter = Counter()
    for w in words:
        syl = list(w)
        for s in syl:
            freq[s] += 1
        for a, b in zip(syl, syl[1:]):
            big[(a, b)] += 1
    valid = {s for s, c in freq.items() if c >= MIN_SYLLABLE_FREQ}
    items = [((a, b), c) for (a, b), c in big.items() if a in valid and b in valid]
    total = sum(c for _, c in items) or 1
    return {k: c / total for k, c in items}, sorted(valid)


def scramble_lm(prob: dict, vocab: list[str], seed: int = 107) -> tuple[dict, list[str]]:
    """Scrambled control (iii): bijectively permute the syllable labels of
    the Dravidian LM. Bigram probability multiset is preserved exactly;
    the lexicon-phonotactic correspondence is destroyed."""
    rng = random.Random(seed)
    permuted = list(vocab)
    rng.shuffle(permuted)
    ren = dict(zip(vocab, permuted))
    return {(ren[a], ren[b]): p for (a, b), p in prob.items()}, sorted(vocab)


LM_LOADERS = {
    "dravidian": load_dravidian_lm,
    "sanskrit": load_sanskrit_lm,
    "geez": build_geez_lm,
}


# ── Anchor gold values ────────────────────────────────────────────────────

def _normalise_first_syllable(reading: str) -> str:
    """Phase-52's MEDIUM extraction: first segment, lowercase, strip
    non-[a-z], max 4 chars."""
    syl = reading.rstrip("/").split("/")[0].strip().lower()
    return re.sub(r"[^a-z]", "", syl)[:4]


def _map_into_vocab(syl_norm: str, vocab: list[str], vocab_set: set[str]) -> str | None:
    """Phase-52's vocab mapping: exact match, else first vocab entry with
    the same 2-char prefix, else None."""
    if not syl_norm:
        return None
    if syl_norm in vocab_set:
        return syl_norm
    return next((s for s in vocab if s.startswith(syl_norm[:2])), None)


def extract_gold(anchors: dict, vocab: list[str]) -> dict[str, str | None]:
    """Gold syllabic value for every H+M anchor sign: HIGH_SYLLABIC takes
    precedence (Phase-52's own pins), else the Phase-52 MEDIUM procedure
    applied to the reading. None when no value maps into the vocab."""
    vocab_set = set(vocab)
    gold: dict[str, str | None] = {}
    for sign, info in anchors.items():
        if info.get("confidence") not in ("HIGH", "MEDIUM"):
            continue
        reading = info.get("reading") or ""
        if sign in HIGH_SYLLABIC:
            gold[sign] = _map_into_vocab(HIGH_SYLLABIC[sign], vocab, vocab_set)
        elif reading:
            gold[sign] = _map_into_vocab(_normalise_first_syllable(reading), vocab, vocab_set)
        else:
            gold[sign] = None
    return gold


def phase52_pins(vocab: list[str]) -> dict[str, str]:
    """The Phase-52 pin set, produced by the baseline script's own code
    (imported, not re-implemented) for baseline fidelity."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "phase52_baseline", REPO / "backend/scripts/phase52_syllabic_sa.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_anchors_as_pins(vocab)


def load_anchors() -> dict:
    return json.loads(ANCHORS.read_text("utf-8"))["anchors"]


# ── Folds ─────────────────────────────────────────────────────────────────

def make_folds(pins: dict[str, str], anchors: dict, k: int = 5,
               seed: int = 107) -> list[list[str]]:
    """Stratified (by confidence) deterministic k-folds over the pinnable
    anchor signs. Returns k held-out sign lists; folds are disjoint and
    cover the pinnable set."""
    by_conf: dict[str, list[str]] = defaultdict(list)
    for sign in sorted(pins):
        by_conf[anchors.get(sign, {}).get("confidence", "?")].append(sign)
    rng = random.Random(seed)
    folds: list[list[str]] = [[] for _ in range(k)]
    for conf in sorted(by_conf):
        signs = list(by_conf[conf])
        rng.shuffle(signs)
        for i, s in enumerate(signs):
            folds[i % k].append(s)
    return [sorted(f) for f in folds]


def select_pin_budget(available: dict[str, str], budget: int,
                      flat: list[str]) -> dict[str, str]:
    """Top-`budget` pins by the pre-registered priority: HIGH_SYLLABIC
    pins first, then by descending corpus frequency of the sign."""
    if budget >= len(available):
        return dict(available)
    freq = Counter(flat)
    ordered = sorted(
        available,
        key=lambda s: (0 if s in HIGH_SYLLABIC else 1, -freq.get(s, 0), s))
    return {s: available[s] for s in ordered[:budget]}


# ── Objective terms ───────────────────────────────────────────────────────

def syllable_initial_invalid(syl: str) -> bool:
    """Phase-61 check_phonotactics applied to a single syllabic value:
    invalid Proto-Dravidian initial consonant, or a lone consonant.
    (Phase-61's problematic-sequence rule operates across a reading's
    phoneme stream and cannot fire on one syllable; Phase-58's retroflex
    rule is vacuous on this diacritic-stripped representation.)"""
    if not syl:
        return False
    first = syl[0]
    if first not in VOWEL_CHARS and first in PD_INVALID_INITIALS:
        return True
    if len(syl) == 1 and first not in VOWEL_CHARS:
        return True
    return False


def syllable_vowel_class(syl: str) -> str:
    """'F' / 'B' / 'N' by the syllable's first vowel (Phase-61/133e classes)."""
    for ch in syl:
        if ch in FRONT_VOWELS:
            return "F"
        if ch in BACK_VOWELS:
            return "B"
        if ch in VOWEL_CHARS:
            return "N"
    return "N"


class Objective:
    """Pluggable SA objective: LM bigram score + optional constraint terms.

    Terms (weights pre-registered in specs/005): phonotactic λ=3.0 per
    inscription with an invalid initial syllable; harmony λ=3.0 per
    inscription mixing front/back vowel classes; positional +1.0 ×
    Σ_tokens log P(value | position class) with a caller-supplied
    log-profile table (built per fold from training anchors only).
    """

    def __init__(self, bigram_prob: dict, flat: list[str],
                 inscriptions: list[list[str]],
                 terms: tuple[str, ...] = (),
                 positional_logp: dict | None = None,
                 lambda_phono: float = 3.0, lambda_harmony: float = 3.0):
        from glossa_lab.pipelines.decipher import BigramScorer

        tc: Counter = Counter()
        for (a, b) in bigram_prob:
            tc[a] += 1
            tc[b] += 1
        ranked = [t for t, _ in tc.most_common()]
        self.scorer = BigramScorer(
            SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)
        self.terms = tuple(terms)
        self.lambda_phono = lambda_phono
        self.lambda_harmony = lambda_harmony
        self.positional_logp = positional_logp  # {value: [logp_I, logp_M, logp_T]}
        # Precomputed structures (mapping-independent)
        self.init_counts = Counter(insc[0] for insc in inscriptions if insc)
        self.insc_signs = [list(insc) for insc in inscriptions]
        # token position classes per cipher sign: counts n[sign][class]
        self.pos_counts: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
        for insc in inscriptions:
            n = len(insc)
            for i, s in enumerate(insc):
                cls = 0 if i == 0 else (2 if i == n - 1 else 1)
                self.pos_counts[s][cls] += 1
        self._invalid_cache: dict[str, bool] = {}
        self._vclass_cache: dict[str, str] = {}
        # Vectorised term structures (identical values to the dict path)
        sc = self.scorer
        self._flat_idx = np.array([sc.cipher_idx[s] for s in flat], dtype=np.int32)
        self._init_count_arr = np.zeros(sc.C, dtype=np.float64)
        for sign, cnt in self.init_counts.items():
            if sign in sc.cipher_idx:
                self._init_count_arr[sc.cipher_idx[sign]] = cnt
        self._invalid_arr = np.array(
            [syllable_initial_invalid(t) for t in sc.target_vocab], dtype=bool)
        self._vclass_arr = np.array(
            [{"N": 0, "F": 1, "B": 2}[syllable_vowel_class(t)]
             for t in sc.target_vocab], dtype=np.int32)
        self._pos_counts_arr = np.zeros((sc.C, 3), dtype=np.float64)
        for sign, counts in self.pos_counts.items():
            if sign in sc.cipher_idx:
                self._pos_counts_arr[sc.cipher_idx[sign]] = counts
        # inscription segments in the flat stream (contiguous by construction)
        self._seg_starts = []
        off = 0
        for insc in inscriptions:
            self._seg_starts.append(off)
            off += len(insc)
        self._seg_starts = np.array(self._seg_starts, dtype=np.int64)
        self._logp_arr = None
        if positional_logp:
            self._logp_arr = np.zeros((len(sc.target_vocab), 3), dtype=np.float64)
            for t, lp in positional_logp.items():
                if t in sc.target_idx:
                    self._logp_arr[sc.target_idx[t]] = lp

    def _m_array(self, mapping: dict[str, str]):
        sc = self.scorer
        m = np.zeros(sc.C, dtype=np.int32)
        for cs, ts in mapping.items():
            ci = sc.cipher_idx.get(cs, -1)
            ti = sc.target_idx.get(ts, -1)
            if ci >= 0 and ti >= 0:
                m[ci] = ti
        return m

    # term components (mapping: sign -> syllable)
    def lm_score(self, mapping: dict[str, str]) -> float:
        return self.scorer.score_full(mapping)

    def phono_penalty(self, mapping: dict[str, str]) -> float:
        m = self._m_array(mapping)
        return float((self._init_count_arr * self._invalid_arr[m]).sum())

    def harmony_penalty(self, mapping: dict[str, str]) -> float:
        m = self._m_array(mapping)
        cls = self._vclass_arr[m[self._flat_idx]]
        is_f = (cls == 1).astype(np.int32)
        is_b = (cls == 2).astype(np.int32)
        has_f = np.maximum.reduceat(is_f, self._seg_starts)
        has_b = np.maximum.reduceat(is_b, self._seg_starts)
        return float(((has_f > 0) & (has_b > 0)).sum())

    def positional_score(self, mapping: dict[str, str]) -> float:
        if self._logp_arr is None:
            return 0.0
        m = self._m_array(mapping)
        return float((self._pos_counts_arr * self._logp_arr[m]).sum())

    def score(self, mapping: dict[str, str]) -> float:
        total = self.lm_score(mapping)
        if "phono" in self.terms:
            total -= self.lambda_phono * self.phono_penalty(mapping)
        if "harmony" in self.terms:
            total -= self.lambda_harmony * self.harmony_penalty(mapping)
        if "positional" in self.terms:
            total += self.positional_score(mapping)
        return total


def build_positional_logp(train_gold: dict[str, str | None],
                          flat: list[str], inscriptions: list[list[str]],
                          vocab: list[str]) -> dict[str, list[float]]:
    """Per-fold positional profile: log P(value | position class) from
    TRAINING anchors' gold values over their corpus token occurrences
    (Phase-133b position classes; add-1 smoothing over the vocab)."""
    counts: dict[str, list[int]] = {v: [0, 0, 0] for v in vocab}
    train = {s: g for s, g in train_gold.items() if g}
    for insc in inscriptions:
        n = len(insc)
        for i, s in enumerate(insc):
            g = train.get(s)
            if g is None:
                continue
            cls = 0 if i == 0 else (2 if i == n - 1 else 1)
            counts[g][cls] += 1
    logp: dict[str, list[float]] = {}
    totals = [sum(counts[v][k] for v in vocab) for k in range(3)]
    V = len(vocab)
    for v in vocab:
        logp[v] = [math.log((counts[v][k] + 1) / (totals[k] + V)) for k in range(3)]
    return logp


# ── SA runner (full-rescoring path, Phase-52 loop discipline) ─────────────

def target_tokens_for(bigram_prob: dict, n_cipher: int) -> list[str]:
    toks = sorted(set(t for pair in bigram_prob for t in pair))
    while len(toks) < n_cipher:
        toks.append(f"?{len(toks)}")
    return toks


def run_sa(objective: Objective, flat: list[str], bigram_prob: dict,
           pinned: dict[str, str], seeds=(0, 1, 2), n_restarts: int = 5,
           max_iter: int = 10_000, temp: float = 1.0,
           cool: float = 0.9997) -> dict:
    """Phase-52's SA loop (same init, swap proposal, Metropolis rule and
    cooling), parameterised. Returns per-seed bests + consensus."""
    cipher_alpha = sorted(set(flat))
    target_tokens = target_tokens_for(bigram_prob, len(cipher_alpha))
    free_cipher = [c for c in cipher_alpha if c not in pinned]
    seed_results = []
    for seed in seeds:
        rng = random.Random(seed)
        best_score = float("-inf")
        best_mapping: dict[str, str] = {}
        for restart in range(n_restarts):
            mapping = dict(pinned)
            used = set(mapping.values())
            pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used]
            if restart > 0:
                rng.shuffle(pool)
            for c, t in zip(free_cipher, pool):
                mapping[c] = t
            score = objective.score(mapping)
            t = temp
            for _ in range(max_iter):
                if len(free_cipher) < 2:
                    break
                i, j = rng.sample(range(len(free_cipher)), 2)
                ca, cb = free_cipher[i], free_cipher[j]
                mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
                ns = objective.score(mapping)
                delta = ns - score
                if delta > 0 or (t > 0 and rng.random() < math.exp(min(delta / t, 0))):
                    score = ns
                else:
                    mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
                t *= cool
            if score > best_score:
                best_score = score
                best_mapping = dict(mapping)
        seed_results.append({"seed": seed, "score": best_score, "mapping": best_mapping})
    consensus, consensus_frac = consensus_of([r["mapping"] for r in seed_results])
    return {"seeds": seed_results, "consensus": consensus,
            "consensus_frac": consensus_frac}


def consensus_of(mappings: list[dict[str, str]]) -> tuple[dict[str, str], dict[str, float]]:
    """Phase-52-style majority vote across seed-best mappings."""
    votes: dict[str, Counter] = defaultdict(Counter)
    for m in mappings:
        for sign, val in m.items():
            votes[sign][val] += 1
    consensus, frac = {}, {}
    for sign, c in votes.items():
        val, n = c.most_common(1)[0]
        consensus[sign] = val
        frac[sign] = n / sum(c.values())
    return consensus, frac


def estimate_null(objective: Objective, flat: list[str], bigram_prob: dict,
                  n: int = 30, seed: int = 42) -> tuple[float, float]:
    """Phase-52's null: random full mappings scored with the SAME
    objective; returns (mean, std)."""
    cipher_alpha = sorted(set(flat))
    target_tokens = target_tokens_for(bigram_prob, len(cipher_alpha))
    rng = random.Random(seed)
    scores = []
    for _ in range(n):
        tgt = list(target_tokens[:len(cipher_alpha)])
        rng.shuffle(tgt)
        scores.append(objective.score(dict(zip(cipher_alpha, tgt))))
    mu = sum(scores) / len(scores)
    std = math.sqrt(sum((s - mu) ** 2 for s in scores) / len(scores)) or 1.0
    return mu, std


# ── Agreement metrics ─────────────────────────────────────────────────────

def agreement(consensus: dict[str, str], gold: dict[str, str | None],
              signs) -> dict:
    """Exact-match agreement on the given signs (gold None = not evaluable)."""
    n_eval = n_agree = 0
    detail = {}
    for s in signs:
        g = gold.get(s)
        if g is None or s not in consensus:
            continue
        n_eval += 1
        ok = consensus[s] == g
        n_agree += int(ok)
        detail[s] = {"gold": g, "sa": consensus[s], "agree": ok}
    return {"n_eval": n_eval, "n_agree": n_agree,
            "rate": (n_agree / n_eval) if n_eval else None, "detail": detail}


# ── Delta (incremental) scorer — Step 3 ───────────────────────────────────

class DeltaObjective:
    """Incremental equivalent of Objective: mapping held as an int array
    (cipher idx -> target idx); swap deltas touch only affected bigrams,
    inscriptions and profile rows. Accumulates in float64; mirrors
    Objective.score's value up to float32-vs-64 summation noise in
    BigramScorer (the equivalence criteria in specs/005 allow for it)."""

    def __init__(self, objective: Objective, inscriptions: list[list[str]]):
        if np is None:
            raise RuntimeError("numpy required for DeltaObjective")
        sc = objective.scorer
        self.obj = objective
        self.cipher_idx = sc.cipher_idx
        self.target_idx = sc.target_idx
        self.target_vocab = sc.target_vocab
        self.mat = sc.bigram_mat.astype(np.float64)
        self.pair_a = sc.pair_a
        self.pair_b = sc.pair_b
        self.C = sc.C
        # pair positions per cipher sign
        self.pos_of_sign = []
        for c in range(self.C):
            self.pos_of_sign.append(
                np.where((self.pair_a == c) | (self.pair_b == c))[0])
        # term structures by cipher idx
        self.init_count_arr = np.zeros(self.C, dtype=np.float64)
        for sign, cnt in objective.init_counts.items():
            if sign in self.cipher_idx:
                self.init_count_arr[self.cipher_idx[sign]] = cnt
        self.invalid_arr = np.array(
            [syllable_initial_invalid(t) for t in self.target_vocab], dtype=bool)
        self.vclass_arr = np.array(
            [{"N": 0, "F": 1, "B": 2}[syllable_vowel_class(t)]
             for t in self.target_vocab], dtype=np.int32)
        self.insc_idx = [[self.cipher_idx[s] for s in insc if s in self.cipher_idx]
                         for insc in inscriptions]
        self.insc_of_sign: list[list[int]] = [[] for _ in range(self.C)]
        for ii, signs in enumerate(self.insc_idx):
            for c in set(signs):
                self.insc_of_sign[c].append(ii)
        self.pos_counts_arr = np.zeros((self.C, 3), dtype=np.float64)
        for sign, counts in objective.pos_counts.items():
            if sign in self.cipher_idx:
                self.pos_counts_arr[self.cipher_idx[sign]] = counts
        if objective.positional_logp:
            self.logp_arr = np.zeros((len(self.target_vocab), 3), dtype=np.float64)
            for t, lp in objective.positional_logp.items():
                if t in self.target_idx:
                    self.logp_arr[self.target_idx[t]] = lp
        else:
            self.logp_arr = None
        self.m = np.zeros(self.C, dtype=np.int32)

    # -- state -------------------------------------------------------------
    def set_mapping(self, mapping: dict[str, str]) -> None:
        self.m[:] = 0
        for cs, ts in mapping.items():
            ci = self.cipher_idx.get(cs, -1)
            ti = self.target_idx.get(ts, -1)
            if ci >= 0 and ti >= 0:
                self.m[ci] = ti

    def mapping_dict(self) -> dict[str, str]:
        inv = {i: s for s, i in self.cipher_idx.items()}
        return {inv[c]: self.target_vocab[int(self.m[c])] for c in range(self.C)}

    # -- full recompute (verification path) --------------------------------
    def total(self) -> float:
        total = float(self.mat[self.m[self.pair_a], self.m[self.pair_b]].sum())
        if "phono" in self.obj.terms:
            bad = float((self.init_count_arr * self.invalid_arr[self.m]).sum())
            total -= self.obj.lambda_phono * bad
        if "harmony" in self.obj.terms:
            bad = 0
            for signs in self.insc_idx:
                if not signs:
                    continue
                cls = self.vclass_arr[self.m[signs]]
                if (cls == 1).any() and (cls == 2).any():
                    bad += 1
            total -= self.obj.lambda_harmony * bad
        if "positional" in self.obj.terms and self.logp_arr is not None:
            total += float((self.pos_counts_arr * self.logp_arr[self.m]).sum())
        return total

    # -- delta --------------------------------------------------------------
    def _insc_violates(self, signs: list[int], m) -> bool:
        if not signs:
            return False
        cls = self.vclass_arr[m[signs]]
        return bool((cls == 1).any() and (cls == 2).any())

    def delta_swap(self, ci: int, cj: int) -> float:
        if ci == cj:
            return 0.0
        m = self.m
        ti, tj = int(m[ci]), int(m[cj])
        if ti == tj:
            return 0.0
        d = 0.0
        # LM term: affected pair positions
        pos = np.union1d(self.pos_of_sign[ci], self.pos_of_sign[cj])
        if len(pos):
            pa, pb = self.pair_a[pos], self.pair_b[pos]
            old = float(self.mat[m[pa], m[pb]].sum())
            m2 = m.copy()
            m2[ci], m2[cj] = tj, ti
            new = float(self.mat[m2[pa], m2[pb]].sum())
            d += new - old
        else:
            m2 = m
        if "phono" in self.obj.terms:
            d -= self.obj.lambda_phono * (
                self.init_count_arr[ci] * (float(self.invalid_arr[tj]) - float(self.invalid_arr[ti]))
                + self.init_count_arr[cj] * (float(self.invalid_arr[ti]) - float(self.invalid_arr[tj])))
        if "harmony" in self.obj.terms:
            affected = set(self.insc_of_sign[ci]) | set(self.insc_of_sign[cj])
            if affected:
                old_v = sum(1 for ii in affected if self._insc_violates(self.insc_idx[ii], m))
                new_v = sum(1 for ii in affected if self._insc_violates(self.insc_idx[ii], m2))
                d -= self.obj.lambda_harmony * (new_v - old_v)
        if "positional" in self.obj.terms and self.logp_arr is not None:
            d += float((self.pos_counts_arr[ci] * (self.logp_arr[tj] - self.logp_arr[ti])).sum()
                       + (self.pos_counts_arr[cj] * (self.logp_arr[ti] - self.logp_arr[tj])).sum())
        return d

    def apply_swap(self, ci: int, cj: int) -> None:
        self.m[ci], self.m[cj] = self.m[cj], self.m[ci]


def run_sa_delta(delta: DeltaObjective, flat: list[str], bigram_prob: dict,
                 pinned: dict[str, str], seeds=(0, 1, 2), n_restarts: int = 5,
                 max_iter: int = 10_000, temp: float = 1.0,
                 cool: float = 0.9997) -> dict:
    """Delta-scoring twin of run_sa: identical init and RNG discipline
    (shuffle on restart>0, rng.sample pair choice, rng.random drawn only
    on the non-improving branch), so streams are comparable."""
    cipher_alpha = sorted(set(flat))
    target_tokens = target_tokens_for(bigram_prob, len(cipher_alpha))
    free_cipher = [c for c in cipher_alpha if c not in pinned]
    free_idx = [delta.cipher_idx[c] for c in free_cipher]
    seed_results = []
    for seed in seeds:
        rng = random.Random(seed)
        best_score = float("-inf")
        best_mapping: dict[str, str] = {}
        for restart in range(n_restarts):
            mapping = dict(pinned)
            used = set(mapping.values())
            pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used]
            if restart > 0:
                rng.shuffle(pool)
            for c, t in zip(free_cipher, pool):
                mapping[c] = t
            delta.set_mapping(mapping)
            score = delta.total()
            t = temp
            for _ in range(max_iter):
                if len(free_idx) < 2:
                    break
                i, j = rng.sample(range(len(free_idx)), 2)
                ci, cj = free_idx[i], free_idx[j]
                d = delta.delta_swap(ci, cj)
                if d > 0 or (t > 0 and rng.random() < math.exp(min(d / t, 0))):
                    delta.apply_swap(ci, cj)
                    score += d
                t *= cool
            if score > best_score:
                best_score = score
                best_mapping = delta.mapping_dict()
        seed_results.append({"seed": seed, "score": best_score, "mapping": best_mapping})
    consensus, consensus_frac = consensus_of([r["mapping"] for r in seed_results])
    return {"seeds": seed_results, "consensus": consensus,
            "consensus_frac": consensus_frac}
