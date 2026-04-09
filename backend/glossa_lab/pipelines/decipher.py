"""Substitution cipher decipherment engine.

Cracks a substitution cipher by matching the statistical fingerprint
of the ciphered text against a known target language model.

Approach (3-stage):
  1. SEED: Frequency-rank mapping — most frequent cipher sign →
     most frequent target phoneme, etc.
  2. REFINE: Bigram correlation — swap pairs in the mapping to
     maximise bigram log-likelihood against the target model.
  3. VALIDATE: Score the final mapping and report accuracy.

This implements the core insight behind historical decipherments:
if you know (or hypothesise) the language family, you can match
the statistical fingerprint of the unknown script against the
known language to propose sound values.

The Kandles system (Merkur patent) assists by providing a cross-
language phonetic similarity check: if the proposed decipherment
produces Kandles color patterns similar to the target language,
confidence increases.
"""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from itertools import cycle
from typing import Any

from glossa_lab.engine import register_pipeline

# ── Language model ────────────────────────────────────────────────────


class LanguageModel:
    """Unigram + bigram + trigram language model with positional stats."""

    def __init__(
        self,
        symbols: list[str],
        inscriptions: list[list[str]] | None = None,
    ) -> None:
        self.symbols = symbols
        total = len(symbols)
        self.alphabet = sorted(set(symbols))
        self.size = len(self.alphabet)

        # Unigram frequencies (normalized)
        counts = Counter(symbols)
        self.unigram_freq: dict[str, float] = {s: c / total for s, c in counts.items()}
        self.ranked = [s for s, _ in counts.most_common()]

        # Bigram frequencies (over the flat symbol stream — may cross word boundaries)
        bigram_counts: Counter[tuple[str, str]] = Counter()
        for i in range(len(symbols) - 1):
            bigram_counts[(symbols[i], symbols[i + 1])] += 1
        bigram_total = sum(bigram_counts.values()) or 1
        self.bigram_freq: dict[tuple[str, str], float] = {
            bg: c / bigram_total for bg, c in bigram_counts.items()
        }

        # Word-boundary bigrams — scored only within words, not across them.
        # Uses "<BOW>" and "<EOW>" pseudo-symbols so that word-initial and
        # word-final positions carry their own frequency statistics.
        # Snyder et al. (2010) use this representation for Semitic phonotactics.
        self.word_bigram_freq: dict[tuple[str, str], float] = {}
        self.word_initial_freq: dict[str, float] = {}
        self.word_final_freq:   dict[str, float] = {}
        self.ocp_rate: float = 0.0   # fraction of within-word bigrams that are repeats
        if inscriptions:
            wb_counts: Counter[tuple[str, str]] = Counter()
            wi_counts: Counter[str] = Counter()
            wf_counts: Counter[str] = Counter()
            total_within = 0
            repeat_count  = 0
            for word in inscriptions:
                if not word:
                    continue
                wi_counts[word[0]] += 1
                wf_counts[word[-1]] += 1
                # BOW → first sign
                wb_counts[("<BOW>", word[0])] += 1
                # within-word bigrams
                for i in range(len(word) - 1):
                    pair = (word[i], word[i + 1])
                    wb_counts[pair] += 1
                    total_within += 1
                    if word[i] == word[i + 1]:
                        repeat_count += 1
                # last sign → EOW
                wb_counts[(word[-1], "<EOW>")] += 1
            wb_total = sum(wb_counts.values()) or 1
            self.word_bigram_freq = {
                bg: c / wb_total for bg, c in wb_counts.items()
            }
            wi_total = sum(wi_counts.values()) or 1
            wf_total = sum(wf_counts.values()) or 1
            self.word_initial_freq = {s: c / wi_total for s, c in wi_counts.items()}
            self.word_final_freq   = {s: c / wf_total for s, c in wf_counts.items()}
            self.ocp_rate = repeat_count / total_within if total_within > 0 else 0.0

        # Word co-occurrence: fraction of words containing each unordered consonant pair.
        # Used by the root co-occurrence prior: in Semitic languages, the same two
        # consonants rarely appear in the same root (dissimilation), so a mapping
        # that produces many such co-occurrences in decoded words is penalised.
        # Conversely, common co-occurring pairs (e.g. m+l, b+r, y+d) reward
        # assignments that match the target language root structure.
        self.word_cooccur: dict[frozenset, float] = {}
        if inscriptions:
            pair_counts: Counter[frozenset] = Counter()
            n_words = 0
            for word in inscriptions:
                if len(word) < 2:
                    continue
                n_words += 1
                seen = set(word)  # unique consonants in this word
                for a in seen:
                    for b in seen:
                        if a < b:  # canonical unordered pair
                            pair_counts[frozenset([a, b])] += 1
            if n_words > 0:
                self.word_cooccur = {
                    pair: cnt / n_words for pair, cnt in pair_counts.items()
                }

        # Trigram frequencies
        trigram_counts: Counter[tuple[str, str, str]] = Counter()
        for i in range(len(symbols) - 2):
            trigram_counts[(symbols[i], symbols[i + 1], symbols[i + 2])] += 1
        trigram_total = sum(trigram_counts.values()) or 1
        self.trigram_freq: dict[tuple[str, str, str], float] = {
            tg: c / trigram_total for tg, c in trigram_counts.items()
        }

        # Positional profiles (if inscriptions provided)
        self.positional: dict[str, dict[str, float]] = {}
        if inscriptions:
            pos_counts: dict[str, dict[str, int]] = defaultdict(
                lambda: {"initial": 0, "medial": 0, "terminal": 0}
            )
            for insc in inscriptions:
                if len(insc) >= 2:
                    pos_counts[insc[0]]["initial"] += 1
                    pos_counts[insc[-1]]["terminal"] += 1
                    for s in insc[1:-1]:
                        pos_counts[s]["medial"] += 1
            for sign, pc in pos_counts.items():
                t = sum(pc.values()) or 1
                self.positional[sign] = {k: v / t for k, v in pc.items()}

    def score_text(
        self,
        text: list[str],
        use_word_bigrams: bool = False,
        inscriptions: list[list[str]] | None = None,
    ) -> float:
        """Combined bigram + trigram log-likelihood.

        Args:
            text:             flat decoded symbol sequence.
            use_word_bigrams: if True, score bigrams within words only (using
                              word_bigram_freq with <BOW>/<EOW> boundaries).
                              Requires ``inscriptions`` to be provided.
            inscriptions:     decoded word sequences (used when use_word_bigrams=True).

        Trigrams are only used when the corpus is large enough
        for meaningful trigram statistics (>1000 symbols).
        """
        smoothing = 1e-8
        ll = 0.0

        if use_word_bigrams and inscriptions and self.word_bigram_freq:
            # Score only within-word bigrams plus BOW/EOW transitions
            for word in inscriptions:
                if not word:
                    continue
                p = self.word_bigram_freq.get(("<BOW>", word[0]), smoothing)
                ll += math.log(p)
                for i in range(len(word) - 1):
                    p = self.word_bigram_freq.get((word[i], word[i + 1]), smoothing)
                    ll += math.log(p)
                p = self.word_bigram_freq.get((word[-1], "<EOW>"), smoothing)
                ll += math.log(p)
        else:
            # Flat bigram component (default, cross-boundary)
            for i in range(len(text) - 1):
                p = self.bigram_freq.get((text[i], text[i + 1]), smoothing)
                ll += math.log(p)
            # Trigram component (only if corpus is large enough)
            if len(self.symbols) >= 1000 and len(text) > 2:
                tri_ll = 0.0
                for i in range(len(text) - 2):
                    p = self.trigram_freq.get(
                        (text[i], text[i + 1], text[i + 2]),
                        smoothing,
                    )
                    tri_ll += math.log(p)
                # Light blend: 90% bigram + 10% trigram
                ll = 0.9 * ll + 0.1 * tri_ll

        return ll


# ── Decipherment engine ──────────────────────────────────────────


def decipher(
    cipher_signs: list[str],
    target_model: LanguageModel,
    seed: int = 42,
    max_iterations: int = 12000,
    restarts: int = 10,
    cipher_inscriptions: list[list[str]] | None = None,
    kandles_profile: str | None = None,
    use_sa: bool = True,
    sa_temp_start: float = 1.0,
    sa_cooling: float = 0.9985,
    # ── Structural constraint flags ────────────────────────────────────
    use_word_bigrams: bool = False,
    ocp_weight: float = 0.0,
    positional_weight: float = 0.005,
    root_prior_weight: float = 0.0,
    anchors: dict[str, str] | None = None,
    surjective: bool = False,
) -> dict[str, Any]:
    """Crack a substitution cipher using simulated annealing.

    Args:
        cipher_signs:     the encrypted symbol sequence.
        target_model:     language model of the target (known) language.
        seed:             random seed.
        max_iterations:   max swaps per restart.
        restarts:         number of random restarts.
        cipher_inscriptions: optional inscription-level structure for
            positional constraint scoring.
        kandles_profile:  optional language-specific bias profile name.
        use_sa:           use simulated annealing (True) or pure hill climbing (False).
        sa_temp_start:    initial SA temperature.
        sa_cooling:       multiplicative cooling rate per iteration.
        use_word_bigrams: score bigrams within-word only (Semitic phonotactics).
                          Requires cipher_inscriptions and word_bigram_freq in LM.
        ocp_weight:       Obligatory Contour Principle penalty weight (0 = disabled).
                          Penalises mappings that produce many repeated consonants
                          within the same word (rare in Semitic roots).
        positional_weight: weight of word-initial/final positional bonus (default 0.005).
        root_prior_weight: weight of the root co-occurrence prior (0 = disabled).
                          Rewards mappings whose decoded words contain consonant
                          pairs that commonly co-occur in target-language roots.
        anchors:          optional dict of cipher_sign → target_sign for known
                          correspondences (e.g. pan-Semitic cognates r→r, m→m).
                          Anchored signs are locked and excluded from swaps.
        surjective:       if True, multiple cipher signs may map to the same
                          target sign (correct for cross-language where the cipher
                          alphabet is larger).  SA proposes re-assignments rather
                          than swaps.  Default False (bijection / same-alphabet).

    Returns:
        dict with proposed_mapping, deciphered_text, score, and stats.
    """
    rng = random.Random(seed)

    cipher_alphabet = sorted(set(cipher_signs))
    target_alphabet = target_model.ranked[: len(cipher_alphabet)]

    while len(target_alphabet) < len(cipher_alphabet):
        target_alphabet.append(f"?{len(target_alphabet)}")

    # Build cipher positional profiles (if inscriptions provided)
    cipher_positional: dict[str, dict[str, float]] = {}
    if cipher_inscriptions:
        pos_counts: dict[str, dict[str, int]] = defaultdict(
            lambda: {"initial": 0, "medial": 0, "terminal": 0}
        )
        for insc in cipher_inscriptions:
            if len(insc) >= 2:
                pos_counts[insc[0]]["initial"] += 1
                pos_counts[insc[-1]]["terminal"] += 1
                for s in insc[1:-1]:
                    pos_counts[s]["medial"] += 1
        for sign, pc in pos_counts.items():
            t = sum(pc.values()) or 1
            cipher_positional[sign] = {k: v / t for k, v in pc.items()}

    # Stage 1: SEED — frequency-rank mapping
    cipher_counts = Counter(cipher_signs)
    cipher_ranked = [s for s, _ in cipher_counts.most_common()]

    # Apply anchors: locked cipher→target pairs excluded from search
    locked: dict[str, str] = {}  # cipher_sign → target_sign (fixed)
    free_cipher: list[str] = []
    if surjective:
        # In surjective mode, target signs may be reused; no exclusion.
        # Use the real target alphabet only (no dummy padding).
        free_target: list[str] = list(target_alphabet)
        if anchors:
            for cs, ts in anchors.items():
                if cs in cipher_ranked and ts in (set(target_model.ranked) | set(free_target)):
                    locked[cs] = ts
        for cs in cipher_ranked:
            if cs not in locked:
                free_cipher.append(cs)
        free_target_ranked = list(target_model.ranked)  # all targets always available
    else:
        free_target = list(target_alphabet)
        if anchors:
            for cs, ts in anchors.items():
                if cs in cipher_ranked and ts in free_target:
                    locked[cs] = ts
                    free_target.remove(ts)
        for cs in cipher_ranked:
            if cs not in locked:
                free_cipher.append(cs)
        free_target_ranked = [t for t in target_model.ranked if t in free_target]
        for t in free_target:
            if t not in free_target_ranked:
                free_target_ranked.append(t)

    best_mapping: dict[str, str] = {}
    best_score = float("-inf")

    def _init_mapping(rng_: random.Random, shuffle: bool) -> dict[str, str]:
        """Build an initial cipher→target mapping for one restart.

        Surjective mode: free_cipher may be longer than free_target_ranked.
        We cycle over the targets so every cipher sign gets an assignment.
        Bijective mode: zip gives a 1-to-1 pairing.
        """
        m = dict(locked)
        if surjective:
            targets = list(free_target_ranked)
            if shuffle:
                rng_.shuffle(targets)
            # Cycle targets for the surplus cipher signs
            m.update({cs: t for cs, t in zip(free_cipher, cycle(targets))})
        else:
            targets = list(free_target_ranked)
            if shuffle:
                rng_.shuffle(targets)
            m.update(dict(zip(free_cipher, targets)))
        return m

    for restart in range(restarts):
        mapping = _init_mapping(rng, shuffle=(restart > 0))

        # Stage 2: REFINE — simulated annealing (falls back to hill climbing when T→0)
        current_score = _score_mapping(
            cipher_signs,
            mapping,
            target_model,
            cipher_positional,
            use_word_bigrams=use_word_bigrams,
            cipher_inscriptions=cipher_inscriptions,
            ocp_weight=ocp_weight,
            positional_weight=positional_weight,
            root_prior_weight=root_prior_weight,
        )

        temperature = sa_temp_start if use_sa else 0.0
        no_improve = 0
        for _iteration in range(max_iterations):
            if not free_cipher:
                break

            if surjective:
                # Surjective SA: re-assign one random cipher sign to a new target
                i = rng.randint(0, len(free_cipher) - 1)
                a = free_cipher[i]
                old_t = mapping[a]
                new_t = free_target_ranked[rng.randint(0, len(free_target_ranked) - 1)]
                if old_t == new_t:
                    continue
                mapping[a] = new_t
                new_score = _score_mapping(
                    cipher_signs, mapping, target_model, cipher_positional,
                    use_word_bigrams=use_word_bigrams,
                    cipher_inscriptions=cipher_inscriptions,
                    ocp_weight=ocp_weight,
                    positional_weight=positional_weight,
                    root_prior_weight=root_prior_weight,
                )
                delta = new_score - current_score
                if delta > 0 or (
                    temperature > 1e-4 and rng.random() < math.exp(delta / temperature)
                ):
                    current_score = new_score
                    no_improve = 0
                else:
                    mapping[a] = old_t
                    no_improve += 1
                if use_sa:
                    temperature *= sa_cooling
                thresh = 250 if temperature < 1e-4 else 800
                if no_improve > thresh:
                    break
                continue  # skip the bijective swap below

            # Bijective SA: swap two free cipher signs
            if len(free_cipher) < 2:
                break
            i = rng.randint(0, len(free_cipher) - 1)
            j = rng.randint(0, len(free_cipher) - 1)
            if i == j:
                continue

            a, b = free_cipher[i], free_cipher[j]
            mapping[a], mapping[b] = mapping[b], mapping[a]

            new_score = _score_mapping(
                cipher_signs,
                mapping,
                target_model,
                cipher_positional,
                use_word_bigrams=use_word_bigrams,
                cipher_inscriptions=cipher_inscriptions,
                ocp_weight=ocp_weight,
                positional_weight=positional_weight,
                root_prior_weight=root_prior_weight,
            )

            delta = new_score - current_score
            # Accept if better; or probabilistically if worse (SA escape from local optima)
            if delta > 0 or (
                temperature > 1e-4
                and rng.random() < math.exp(delta / temperature)
            ):
                current_score = new_score
                no_improve = 0
            else:
                mapping[a], mapping[b] = mapping[b], mapping[a]
                no_improve += 1

            # Cool temperature
            if use_sa:
                temperature *= sa_cooling

            # Early stop only when temperature is negligible (SA fully converged)
            converged_threshold = 250 if temperature < 1e-4 else 800
            if no_improve > converged_threshold:
                break

        if current_score > best_score:
            best_score = current_score
            best_mapping = dict(mapping)

    # Stage 3: VALIDATE — apply mapping + Kandles confidence
    deciphered = [best_mapping.get(s, "?") for s in cipher_signs]

    # Kandles validation (Merkur patent)
    kandles_confidence = _kandles_validate(
        deciphered,
        target_model.symbols,
        kandles_profile=kandles_profile,
    )

    return {
        "proposed_mapping": best_mapping,
        "deciphered_text": deciphered,
        "score": round(best_score, 4),
        "kandles_confidence": kandles_confidence,
        "cipher_alphabet_size": len(cipher_alphabet),
        "target_alphabet_size": target_model.size,
    }


def _score_mapping(
    cipher_signs: list[str],
    mapping: dict[str, str],
    target_model: LanguageModel,
    cipher_positional: dict[str, dict[str, float]] | None = None,
    use_word_bigrams: bool = False,
    cipher_inscriptions: list[list[str]] | None = None,
    ocp_weight: float = 0.0,
    positional_weight: float = 0.005,
    root_prior_weight: float = 0.0,
) -> float:
    """Score a mapping by n-gram log-likelihood + structural constraint bonuses.

    Structural constraints (all optional, all additive):
      use_word_bigrams:   score bigrams within words only (word_bigram_freq).
      ocp_weight:         penalise repeated consonants within words (OCP).
      positional_weight:  weight for word-initial/final profile matching bonus.
      root_prior_weight:  weight for root co-occurrence prior (word_cooccur).
    """
    decoded = [mapping.get(s, "?") for s in cipher_signs]

    if use_word_bigrams and cipher_inscriptions and target_model.word_bigram_freq:
        # Decode inscriptions word-by-word
        decoded_inscriptions = [
            [mapping.get(s, "?") for s in word] for word in cipher_inscriptions
        ]
        ll = target_model.score_text(
            decoded,
            use_word_bigrams=True,
            inscriptions=decoded_inscriptions,
        )
    else:
        ll = target_model.score_text(decoded)

    # Positional bonus: reward mappings where word-initial/final profiles match
    if positional_weight > 0 and cipher_positional and target_model.positional:
        pos_score = 0.0
        for cipher_sign, cipher_pos in cipher_positional.items():
            target_sign = mapping.get(cipher_sign)
            if target_sign and target_sign in target_model.positional:
                target_pos = target_model.positional[target_sign]
                for pos_key in ("initial", "medial", "terminal"):
                    pos_score += cipher_pos.get(pos_key, 0) * target_pos.get(pos_key, 0)
        ll += pos_score * abs(ll) * positional_weight

    # OCP penalty: in Semitic roots, consecutive identical consonants are rare.
    # Penalise mappings that produce many within-word repeated pairs.
    if ocp_weight > 0 and cipher_inscriptions:
        ocp_violations = 0
        total_pairs = 0
        for word in cipher_inscriptions:
            decoded_word = [mapping.get(s, "?") for s in word]
            for i in range(len(decoded_word) - 1):
                total_pairs += 1
                if decoded_word[i] == decoded_word[i + 1]:
                    ocp_violations += 1
        if total_pairs > 0:
            violation_rate = ocp_violations / total_pairs
            # Penalise excess violations above the expected LM baseline
            excess = max(0.0, violation_rate - target_model.ocp_rate)
            ll -= ocp_weight * excess * abs(ll)

    # Root co-occurrence prior: reward decoded words whose consonant pairs
    # commonly co-occur in target-language roots (word_cooccur).
    if root_prior_weight > 0 and cipher_inscriptions and target_model.word_cooccur:
        cooccur_score = 0.0
        n_scored = 0
        for word in cipher_inscriptions:
            decoded_word = [mapping.get(s, "?") for s in word]
            if len(decoded_word) < 2:
                continue
            seen = set(decoded_word) - {"?"}
            for a in seen:
                for b in seen:
                    if a < b:
                        pair = frozenset([a, b])
                        # Log of probability; 1e-4 as floor for unseen pairs
                        cooccur_score += math.log(
                            target_model.word_cooccur.get(pair, 1e-4)
                        )
                        n_scored += 1
        if n_scored > 0:
            # Normalise by number of pairs to keep scale consistent
            ll += root_prior_weight * cooccur_score / n_scored * abs(ll)

    return ll


def _kandles_validate(
    deciphered: list[str],
    target_symbols: list[str],
    kandles_profile: str | None = None,
) -> float:
    """Kandles cross-validation: compare phonetic color distributions.

    Uses the Merkur patent Kandles system to compare the phonetic
    fingerprint of the deciphered text against the target text.
    Returns a confidence score in [0, 1].

    Args:
        deciphered:      Proposed decipherment as a list of phoneme strings.
        target_symbols:  Target language corpus symbols.
        kandles_profile: Language-specific bias profile name (e.g. 'luwian',
                         'hurrian'). None uses the default Greek mapping.
    """
    try:
        from glossa_lab.pipelines.kandles import compare_grids, generate_grid

        grid_dec = generate_grid(deciphered[:200], profile=kandles_profile)
        grid_tgt = generate_grid(target_symbols[:200], profile=kandles_profile)
        result = compare_grids(grid_dec, grid_tgt)
        return result["similarity"]
    except Exception:
        return 0.0


# ── Auto-dispatch: CPSC if available, hill climbing fallback ──────


def _cpsc_available() -> bool:
    """Check if the CPSC module is installed."""
    try:
        from glossa_lab.cpsc import CPSC_AVAILABLE

        return CPSC_AVAILABLE
    except ImportError:
        return False


def decipher_auto(
    cipher_signs: list[str],
    target_model: LanguageModel,
    seed: int = 42,
    max_iterations: int = 10000,
    restarts: int = 5,
    cipher_inscriptions: list[list[str]] | None = None,
    engine: str = "auto",
    kandles_profile: str | None = None,
) -> dict[str, Any]:
    """Decipher with automatic engine selection.

    engine:
      "auto" — use CPSC if available, hill climbing otherwise
      "cpsc" — force CPSC (raises if not available)
      "hillclimb" — force hill climbing
    """
    use_cpsc = False
    if engine == "auto":
        use_cpsc = _cpsc_available()
    elif engine == "cpsc":
        if not _cpsc_available():
            raise RuntimeError(
                "CPSC module not available. Install glossa_lab.cpsc or use engine='hillclimb'."
            )
        use_cpsc = True

    if use_cpsc:
        from glossa_lab.cpsc.projection import cpsc_project

        return cpsc_project(
            cipher_signs,
            target_model,
            seed=seed,
            max_epochs=max_iterations,
            restarts=restarts,
        )

    # Fallback: hill climbing
    return decipher(
        cipher_signs,
        target_model,
        seed=seed,
        max_iterations=max_iterations,
        restarts=restarts,
        cipher_inscriptions=cipher_inscriptions,
        kandles_profile=kandles_profile,
    )


def score_accuracy(
    proposed: dict[str, str],
    answer_key: dict[str, str],
) -> dict[str, Any]:
    """Score a proposed mapping against the answer key.

    answer_key: cipher_sign → true_phoneme
    proposed: cipher_sign → proposed_phoneme
    """
    correct = 0
    total = 0
    details = []
    for sign, true_val in answer_key.items():
        proposed_val = proposed.get(sign, "?")
        match = proposed_val == true_val
        if match:
            correct += 1
        total += 1
        details.append(
            {
                "sign": sign,
                "true": true_val,
                "proposed": proposed_val,
                "correct": match,
            }
        )

    return {
        "correct": correct,
        "total": total,
        "accuracy": round(correct / total, 3) if total > 0 else 0,
        "details": details,
    }


@register_pipeline("decipher")
async def run_decipher(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id: cipher text corpus
        target_text_id: target language corpus (for building model)
        max_iterations: hill climbing iterations (default 5000)
        restarts: number of random restarts (default 3)
    """
    from glossa_lab.database import get_db

    text_id = params.get("text_id")
    target_text_id = params.get("target_text_id")
    if not text_id or not target_text_id:
        raise ValueError("Requires text_id and target_text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    cipher_text = await db.get_text(text_id)
    target_text = await db.get_text(target_text_id)
    if cipher_text is None or target_text is None:
        raise ValueError("Text not found")

    target_model = LanguageModel(target_text["content"])
    result = decipher(
        cipher_text["content"],
        target_model,
        max_iterations=params.get("max_iterations", 5000),
        restarts=params.get("restarts", 3),
    )
    result["cipher_text_id"] = text_id
    result["target_text_id"] = target_text_id
    return result
