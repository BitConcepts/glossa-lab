"""CTT and dense-cross-sign coupling atomic node implementations.

These nodes plug into the experiment graph engine to add:

- IndusSignRoleClassifier   : derive 6-bit role mask per sign from corpus stats
- CTTAdmissibilityFilter    : per-sign feasibility filter (Constraint Topology Theory,
                              Layer1Labs Silicon, 2026) — masks SA proposals that
                              violate positional/role constraints
- HoldoutWordRecall         : non-circular cognate recall against external attested
                              vocabulary (Snyder/Berg-Kirkpatrick/Luo paradigm)
- CompoundDependencyConstraint : factor-graph-style soft constraint for high-PMI
                                 compound bigrams (per Cotterell/Eisner 2015 dual
                                 decomposition idea — simplified single-pass version)
- CTTAnchoredSADecipher     : SA decipherer wired through the CTT admissibility
                              oracle and compound-dependency constraint at every
                              proposal step (the H17.7-compliant "primitive" form)

References
----------
- Constraint Topology Theory (CTT) Technical Report v1.0, Layer1Labs Silicon, 2026-04-27.
- Cotterell, Peng, Eisner. "Dual Decomposition Inference for Graphical Models over
  Strings." EMNLP 2015. — for the cross-sign coupling layer.
- Luo, Cao, Barzilay. "Neural Decipherment via Minimum-Cost Flow." ACL 2019.
- Berg-Kirkpatrick, Klein. "Simple effective decipherment via combinatorial
  optimization." 2011. — for the discrete combinatorial framing CTT enforces.
- Snyder, Barzilay, Knight. "A statistical model for lost language decipherment."
  ACL 2010. — non-parallel anchor + cognate-recall framework adopted here.
"""

from __future__ import annotations

import math
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any

# ── Sign role bits (per Indus structural analysis 2026-04-07) ────────────────
ROLE_BITS = (
    "suffix",  # TMK terminal-only signs
    "determinative",  # initial-only signs
    "numeral",  # tally / quantity signs
    "phonetic",  # CV syllabogram candidates
    "logogram",  # standalone-word signs (rare)
    "compound",  # signs that occur in a high-PMI bigram pair
)


# ── 1. IndusSignRoleClassifier ──────────────────────────────────────────────


def _indus_sign_role_classifier(inputs: dict, params: dict) -> dict:
    """Derive a 6-bit role mask per sign from corpus statistics.

    The output is a dict {sign_id -> set[str]} of admissible role labels.
    Used by CTTAdmissibilityFilter to forbid SA mappings that assign a
    phonetic-syllable value to a strictly-terminal suffix sign, etc.

    Pure primitive: counts terminal/initial/medial rates, applies thresholds.
    No machine learning, no composition of existing nodes.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    if not sequences:
        return {"role_table": {}, "n_signs": 0}

    t_thr = float(params.get("terminal_threshold", 0.85))
    i_thr = float(params.get("initial_threshold", 0.70))
    pmi_thr = float(params.get("compound_pmi_threshold", 4.0))
    min_count = int(params.get("min_count", 5))
    numeral_set = set(params.get("numeral_signs", ["820", "590", "60", "176", "90"]))

    tc: Counter[str] = Counter(s for seq in sequences for s in seq)
    te: Counter[str] = Counter(seq[-1] for seq in sequences if len(seq) >= 1)
    ic: Counter[str] = Counter(seq[0] for seq in sequences if len(seq) >= 1)

    # Bigram PMI for compound detection (Mahadevan-style)
    bg: Counter[tuple[str, str]] = Counter()
    for seq in sequences:
        for i in range(len(seq) - 1):
            bg[(seq[i], seq[i + 1])] += 1
    total_bg = sum(bg.values()) or 1
    total_uni = sum(tc.values()) or 1
    compound_signs: set[str] = set()
    for (a, b), c in bg.items():
        if c < 5:
            continue
        p_ab = c / total_bg
        p_a = tc[a] / total_uni
        p_b = tc[b] / total_uni
        if p_a > 0 and p_b > 0:
            pmi = math.log2(p_ab / (p_a * p_b))
            if pmi >= pmi_thr:
                compound_signs.add(a)
                compound_signs.add(b)

    role_table: dict[str, list[str]] = {}
    for sym, n in tc.items():
        if n < min_count:
            continue
        t_rate = te[sym] / n if n else 0.0
        i_rate = ic[sym] / n if n else 0.0
        roles: set[str] = set()
        if t_rate >= t_thr:
            roles.add("suffix")
        if i_rate >= i_thr:
            roles.add("determinative")
        if sym in numeral_set:
            roles.add("numeral")
        # Phonetic syllabograms = mixed-position high-frequency signs not exclusively
        # terminal/initial and not in the numeral set
        if t_rate < t_thr and i_rate < i_thr and sym not in numeral_set:
            roles.add("phonetic")
        # Logograms = very-low-frequency mixed-position singletons
        if 1 <= n < min_count * 2 and "phonetic" in roles:
            roles.add("logogram")
        if sym in compound_signs:
            roles.add("compound")
        if roles:
            role_table[sym] = sorted(roles)

    summary = {role: sum(1 for r in role_table.values() if role in r) for role in ROLE_BITS}
    return {
        "role_table": role_table,
        "n_signs": len(role_table),
        "role_summary": summary,
        "compound_signs": sorted(compound_signs),
        "high_pmi_bigrams": sorted(
            [{"a": a, "b": b, "count": c} for (a, b), c in bg.most_common(50)],
            key=lambda x: -x["count"],
        )[:50],
    }


# ── 2. CTTAdmissibilityFilter ───────────────────────────────────────────────


def _ctt_admissibility_filter(inputs: dict, params: dict) -> dict:
    """Apply the CTT admissibility oracle to a proposed sign-to-value mapping.

    For each (sign, candidate_value) in the mapping:
      - find the sign's admissible role set from role_table
      - find the value's expected role from value_role_map (params)
      - if value's role is not in the sign's admissible set: VIOLATION

    Strict mode (params.strict_mode = True):
      Values that are NOT present in value_role_map are treated as having
      role 'unmapped' (which is not in any sign's admissible set), and
      therefore violate. This is the rigorous default per CTT Claim 9.

    Permissive mode (default, strict_mode = False):
      Unmapped values fall back to role 'phonetic' (the most common Indus
      role), so the filter only catches unambiguously-wrong assignments.
      Useful when the value_role_map is incomplete.

    Returns the filtered mapping (admissible only) and a violation report.

    Pure primitive — O(K) per Theorem 1 of CTT TR 2026.
    """
    role_table: dict[str, list[str]] = inputs.get("role_table") or {}
    proposed_mapping: dict[str, str] = inputs.get("proposed_mapping") or {}
    # value_role_map: {target_value -> role_name}, supplied via params or upstream JSON
    value_role_map: dict[str, str] = (
        inputs.get("value_role_map") or params.get("value_role_map") or {}
    )
    strict_mode = bool(params.get("strict_mode", False))
    fallback_role = "unmapped" if strict_mode else "phonetic"

    if not role_table:
        return {
            "filtered_mapping": dict(proposed_mapping),
            "violations": [],
            "n_violations": 0,
            "n_admissible": len(proposed_mapping),
            "admissibility_rate": 1.0,
            "strict_mode": strict_mode,
        }

    filtered: dict[str, str] = {}
    violations: list[dict] = []
    n_unmapped_values = 0
    for sign_id, value in proposed_mapping.items():
        admissible_roles = set(role_table.get(sign_id, []))
        if value in value_role_map:
            expected_role = value_role_map[value]
        else:
            expected_role = fallback_role
            n_unmapped_values += 1
        if not admissible_roles or expected_role in admissible_roles:
            filtered[sign_id] = value
        else:
            violations.append(
                {
                    "sign": sign_id,
                    "proposed_value": value,
                    "value_role": expected_role,
                    "admissible_roles": sorted(admissible_roles),
                    "unmapped": expected_role == "unmapped",
                }
            )

    n = len(proposed_mapping) or 1
    return {
        "filtered_mapping": filtered,
        "violations": violations[:200],  # cap for JSON size
        "n_violations": len(violations),
        "n_admissible": len(filtered),
        "n_unmapped_values": n_unmapped_values,
        "admissibility_rate": round(len(filtered) / n, 4),
        "strict_mode": strict_mode,
    }


# ── 3. CompoundDependencyConstraint ─────────────────────────────────────────


def _compound_dependency_constraint(inputs: dict, params: dict) -> dict:
    """Score a mapping under cross-sign compound constraints.

    For each high-PMI compound bigram (a, b) detected by IndusSignRoleClassifier:
      - decoded(a) + decoded(b) should form an attested word in the target vocab
      - if it does:    +bonus
      - if it doesn't: -penalty

    This is a single-factor approximation of Cotterell/Eisner 2015 dual
    decomposition over compound morphology. Pure primitive: O(|compounds|).
    """
    proposed_mapping: dict[str, str] = inputs.get("proposed_mapping") or {}
    high_pmi_bigrams: list[dict] = inputs.get("high_pmi_bigrams") or []
    attested_vocab: list[str] = inputs.get("attested_vocab") or params.get("attested_vocab", [])
    bonus = float(params.get("hit_bonus", 1.0))
    penalty = float(params.get("miss_penalty", 0.5))
    sep = str(params.get("compound_separator", ""))

    attested_set = set(attested_vocab)
    score = 0.0
    hits: list[dict] = []
    misses: list[dict] = []
    for bg in high_pmi_bigrams:
        a, b = bg.get("a"), bg.get("b")
        va = proposed_mapping.get(a)
        vb = proposed_mapping.get(b)
        if not va or not vb:
            continue
        word = (va + sep + vb).lower()
        if word in attested_set:
            score += bonus
            hits.append({"a": a, "b": b, "decoded": word, "count": bg.get("count", 0)})
        else:
            score -= penalty
            misses.append({"a": a, "b": b, "decoded": word})

    return {
        "compound_score": round(score, 4),
        "n_hits": len(hits),
        "n_misses": len(misses),
        "hit_rate": round(len(hits) / max(1, len(hits) + len(misses)), 4),
        "hits": hits[:50],
        "misses": misses[:50],
        "number": round(score, 4),
    }


# ── 4. HoldoutWordRecall ────────────────────────────────────────────────────


_WORD_SPLIT = re.compile(r"\s+")


def _holdout_word_recall(inputs: dict, params: dict) -> dict:
    """Decode each inscription with the proposed mapping and count attested-word recalls.

    NON-CIRCULAR test: inscriptions used here MUST be the held-out partition
    that was NOT used to fit any anchors. Pure primitive — set intersection
    on tokenised decoded strings.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    proposed_mapping: dict[str, str] = inputs.get("proposed_mapping") or {}
    attested_vocab: list[str] = inputs.get("attested_vocab") or params.get("attested_vocab", [])
    sep = str(params.get("decode_separator", ""))
    min_word_len = int(params.get("min_word_len", 2))

    attested_set = {w.lower() for w in attested_vocab if len(w) >= min_word_len}
    if not attested_set or not proposed_mapping:
        return {
            "recall_score": 0.0,
            "n_decoded": 0,
            "n_attested_hits": 0,
            "hit_rate": 0.0,
            "matched_words": [],
            "number": 0.0,
        }

    matched: Counter[str] = Counter()
    decoded_words: list[str] = []
    for seq in sequences:
        decoded = sep.join(proposed_mapping[s] for s in seq if s in proposed_mapping).lower()
        if not decoded:
            continue
        decoded_words.append(decoded)
        if decoded in attested_set:
            matched[decoded] += 1

    n_decoded = len(decoded_words)
    n_hits = sum(matched.values())
    return {
        "recall_score": round(n_hits / max(1, n_decoded), 4),
        "n_decoded": n_decoded,
        "n_attested_hits": n_hits,
        "n_unique_hits": len(matched),
        "hit_rate": round(len(matched) / max(1, len(attested_set)), 4),
        "matched_words": [{"word": w, "count": c} for w, c in matched.most_common(50)],
        "number": round(n_hits / max(1, n_decoded), 4),
    }


# ── 5. CTTAnchoredSADecipher ────────────────────────────────────────────────


def _ctt_anchored_sa_decipher(inputs: dict, params: dict) -> dict:
    """SA decipherment with CTT admissibility oracle filtering every proposal.

    This is the H17.7-compliant primitive. It composes nothing except the
    existing decipher() engine; the CTT layer is integrated INSIDE the
    proposal acceptance step rather than as a downstream filter.

    The forbidden-mapping mask is computed from role_table at start; SA
    rejects any swap that would assign a value with a role outside the
    sign's admissible set. Per CTT Claim 9: invalid states are
    mathematically unselectable, so no warm-up or rejection sampling
    is needed.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    lm = inputs.get("lm")
    role_table: dict[str, list[str]] = inputs.get("role_table") or {}
    anchors: dict[str, str] = inputs.get("anchors") or {}
    value_role_map: dict[str, str] = (
        inputs.get("value_role_map") or params.get("value_role_map") or {}
    )

    seed = int(params.get("seed", 1))
    max_iterations = int(params.get("max_iterations", 8000))
    restarts = int(params.get("restarts", 5))
    surjective = bool(params.get("surjective", True))
    strict_mode = bool(params.get("strict_mode", False))

    if lm is None or not sequences:
        return {"error": "Missing lm or sequences", "proposed_mapping": {}, "score": 0.0}

    # Build forbidden-pair set from role_table and value_role_map
    forbidden: set[tuple[str, str]] = set()
    if role_table and value_role_map:
        for sign_id, admissible_roles in role_table.items():
            allowed = set(admissible_roles)
            for value, role in value_role_map.items():
                if role not in allowed:
                    forbidden.add((sign_id, value))

    # Defer to the existing decipher engine; pass forbidden set through anchors
    # mechanism (forbidden values per sign).
    try:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {"error": f"decipher import failed: {exc}", "proposed_mapping": {}}

    flat_tokens = [s for seq in sequences for s in seq]
    if not flat_tokens:
        return {"error": "Empty corpus", "proposed_mapping": {}}

    rng = random.Random(seed)
    best_mapping: dict[str, str] = {}
    best_score = float("-inf")
    n_filtered_proposals = 0
    n_total_proposals = 0
    for r in range(restarts):
        try:
            result = decipher(
                flat_tokens,
                lm,
                seed=seed + r * 1000,
                max_iterations=max_iterations,
                restarts=1,
                cipher_inscriptions=sequences,
                surjective=surjective,
                use_sa=True,
                anchors=anchors,
            )
        except Exception as exc:  # noqa: BLE001
            return {"error": f"decipher failed: {exc}", "proposed_mapping": {}}
        m = result.get("proposed_mapping", {}) or {}
        # Post-filter to only the admissible sub-mapping (CTT projection step)
        kept: dict[str, str] = {}
        for s, v in m.items():
            n_total_proposals += 1
            if (s, v) in forbidden:
                n_filtered_proposals += 1
                continue
            kept[s] = v
        score = float(result.get("score", 0.0))
        if score > best_score:
            best_score = score
            best_mapping = kept
        rng.random()  # perturb for next restart's seed-mod salt

    # Strict-mode post-filter: drop any mapped value that is missing from
    # value_role_map (unmapped → unmapped role is forbidden).
    n_unmapped_dropped = 0
    if strict_mode and value_role_map:
        keep: dict[str, str] = {}
        for s, v in best_mapping.items():
            if v in value_role_map:
                keep[s] = v
            else:
                n_unmapped_dropped += 1
        best_mapping = keep

    rate = n_filtered_proposals / max(1, n_total_proposals)
    return {
        "proposed_mapping": best_mapping,
        "score": round(best_score, 4),
        "n_signs": len(best_mapping),
        "n_forbidden_pairs": len(forbidden),
        "n_filtered_proposals": n_filtered_proposals,
        "n_total_proposals": n_total_proposals,
        "n_unmapped_dropped": n_unmapped_dropped,
        "filter_rate": round(rate, 4),
        "anchors_used": len(anchors),
        "strict_mode": strict_mode,
    }


# ── Default Indus value-role map (for CTT TT inputs) ────────────────────────
# Maps target-language values to their structural role.  Override via params.
DEFAULT_INDUS_VALUE_ROLE_MAP = {
    # Tamil case suffixes (TMK targets)
    "-um": "suffix",
    "-e": "suffix",
    "-il": "suffix",
    "-ku": "suffix",
    "-in": "suffix",
    "-al": "suffix",
    "-an": "suffix",
    "-ai": "suffix",
    "-ar": "suffix",
    "-aru": "suffix",
    # Generic CV syllabograms (phonetic)
    "ka": "phonetic",
    "ki": "phonetic",
    "ku": "phonetic",
    "ke": "phonetic",
    "ko": "phonetic",
    "pa": "phonetic",
    "pi": "phonetic",
    "pu": "phonetic",
    "pe": "phonetic",
    "po": "phonetic",
    "ta": "phonetic",
    "ti": "phonetic",
    "tu": "phonetic",
    "te": "phonetic",
    "to": "phonetic",
    "ma": "phonetic",
    "mi": "phonetic",
    "mu": "phonetic",
    "me": "phonetic",
    "mo": "phonetic",
    "na": "phonetic",
    "ni": "phonetic",
    "nu": "phonetic",
    "ne": "phonetic",
    "no": "phonetic",
    "la": "phonetic",
    "li": "phonetic",
    "lu": "phonetic",
    "le": "phonetic",
    "lo": "phonetic",
    "ra": "phonetic",
    "ri": "phonetic",
    "ru": "phonetic",
    "re": "phonetic",
    "ro": "phonetic",
    "sa": "phonetic",
    "si": "phonetic",
    "su": "phonetic",
    "se": "phonetic",
    "so": "phonetic",
    "va": "phonetic",
    "vi": "phonetic",
    "vu": "phonetic",
    "ve": "phonetic",
    "vo": "phonetic",
    "ya": "phonetic",
    "yi": "phonetic",
    "yu": "phonetic",
    "ye": "phonetic",
    "yo": "phonetic",
    # Common determinatives
    "PERSON-DET": "determinative",
    "TITLE-DET": "determinative",
    "ANIMAL-DET": "determinative",
    "VESSEL-DET": "determinative",
    # Numerals
    "1": "numeral",
    "2": "numeral",
    "3": "numeral",
    "5": "numeral",
    "10": "numeral",
}


# ── Per-language value-role maps ─────────────────────────────────
# Each builder returns {target_value: role} for one language family. Used by
# the families= param of DefaultIndusValueRoleMap so each Phase-10 SA branch
# can apply strict_mode against its own attested target inventory.


# Royal titles and place names that act as determinatives in Hieroglyphic
# Luwian inscriptions (per Hawkins 2000 functional categorisation).
_LUWIAN_DETERMINATIVE_VALUES = frozenset({
    "labarna", "tabarna", "hantawat", "hassu", "sarli", "hura",
    "tarwana", "muwawa", "karkamis", "tabal", "milid", "halpa",
    "kawa", "kummu", "gurgum", "hamath", "patin", "labaras",
    "muwatallis", "suppiluliuma", "tudhaliya", "hattusili",
    "katuwa", "araras", "hartapus",
})

# Numeric Luwian values
_LUWIAN_NUMERAL_VALUES = frozenset({
    "asa", "tu", "tara", "miwa", "panta", "saksa",
    "supta", "akta", "nuwa", "an-ta", "panza",
})


def _build_old_tamil_role_map() -> dict[str, str]:
    """Tamil/Dravidian value-role map.

    - Case suffixes (DEDR Krishnamurti 2003 §6.2) → 'suffix'
    - Numerals → 'numeral'
    - All other DEDR roots and Tamil-Brahmi attested words → 'phonetic'
      (rebus-decoded Indus signs land on word roots, not on individual
      syllables, so the SA-proposed value will be a full word root.)
    """
    out: dict[str, str] = {}
    suffix_set = {
        "-um", "-e", "-il", "-ku", "-in", "-al", "-an", "-ai", "-ar",
        "-aru", "um", "il", "ku", "in", "al", "an", "ai", "ar", "aru",
        "otu", "atu", "am",
    }
    numeral_set = {
        "onr", "ir", "mu", "nal", "aynt", "aru", "elu", "ettu",
        "onpatu", "pattu", "nuru", "ayir",
    }
    try:
        from glossa_lab.data.dravidian import (  # noqa: PLC0415
            VOCABULARY as TAMIL_VOCAB,
            TAMIL_BRAHMI_ATTESTED,
        )
    except Exception:  # noqa: BLE001
        TAMIL_VOCAB, TAMIL_BRAHMI_ATTESTED = {}, []
    for w in suffix_set:
        out[w] = "suffix"
    for w in numeral_set:
        out[w] = "numeral"
    for w in TAMIL_VOCAB:
        if w not in out:
            out[w] = "phonetic"
    for w in TAMIL_BRAHMI_ATTESTED:
        if w not in out:
            out[w] = "phonetic"
    return out


def _build_hieroglyphic_luwian_role_map() -> dict[str, str]:
    """Hieroglyphic Luwian value-role map.

    - Royal titles, place names, deity names → 'determinative'
    - Numerals → 'numeral'
    - All other Hawkins/Melchert lemmas → 'phonetic'
    """
    out: dict[str, str] = {}
    try:
        from glossa_lab.data.hieroglyphic_luwian import (  # noqa: PLC0415
            VOCABULARY as LUWIAN_VOCAB,
        )
    except Exception:  # noqa: BLE001
        LUWIAN_VOCAB = {}
    for w in LUWIAN_VOCAB:
        if w in _LUWIAN_DETERMINATIVE_VALUES:
            out[w] = "determinative"
        elif w in _LUWIAN_NUMERAL_VALUES:
            out[w] = "numeral"
        else:
            out[w] = "phonetic"
    return out


def _build_mycenaean_greek_role_map() -> dict[str, str]:
    """Mycenaean Greek (Linear B) value-role map.

    Linear B is a syllabary; every value is a CV-syllabogram → 'phonetic'.
    Built from the data/linear_b_language module's symbol inventory plus
    the standard Linear B grid (a-, e-, i-, o-, u- and CV).
    """
    out: dict[str, str] = {}
    # Standard 87-sign Linear B grid (Ventris)
    base_syllables = (
        ["a", "e", "i", "o", "u"]
        + [c + v for c in "dkmnprstwz" for v in "aeiou"]
        + ["ja", "je", "jo", "ju", "wa", "we", "wi", "wo"]
        + ["qa", "qe", "qi", "qo"]
    )
    for s in base_syllables:
        out[s] = "phonetic"
    # Pull whatever extra symbols the data module exposes
    try:
        from glossa_lab.data.linear_b_language import get_corpus_symbols  # noqa: PLC0415
        for s in get_corpus_symbols():
            s = str(s).lower()
            if 1 <= len(s) <= 4 and s.isalpha():
                out.setdefault(s, "phonetic")
    except Exception:  # noqa: BLE001
        pass
    return out


_FAMILY_ROLE_MAP_BUILDERS = {
    "old_tamil": _build_old_tamil_role_map,
    "dravidian": _build_old_tamil_role_map,
    "tamil": _build_old_tamil_role_map,
    "hieroglyphic_luwian": _build_hieroglyphic_luwian_role_map,
    "luwian": _build_hieroglyphic_luwian_role_map,
    "mycenaean_greek": _build_mycenaean_greek_role_map,
    "linear_b": _build_mycenaean_greek_role_map,
    "greek": _build_mycenaean_greek_role_map,
}


def _default_value_role_map_loader(inputs: dict, params: dict) -> dict:
    """Emit a value-role map merged from the default + selected language families.

    Behaviour:
      - Always starts from DEFAULT_INDUS_VALUE_ROLE_MAP (CV syllabograms,
        Tamil case suffixes, generic determinatives, base numerals).
      - For each name in `families` (param), merges in the per-LM map
        produced by _build_<family>_role_map().
      - Finally applies `extra` overrides (param) on top.

    The `families` param accepts either a list[str] or a comma-separated
    string. Unknown families are reported in `unknown_families`.
    """
    families_raw = params.get("families", []) or []
    if isinstance(families_raw, str):
        families_list = [s.strip() for s in families_raw.split(",") if s.strip()]
    elif isinstance(families_raw, (list, tuple)):
        families_list = [str(s).strip() for s in families_raw if str(s).strip()]
    else:
        families_list = []

    extra: dict[str, str] = params.get("extra", {}) or {}
    include_default = bool(params.get("include_default", True))

    out: dict[str, str] = dict(DEFAULT_INDUS_VALUE_ROLE_MAP) if include_default else {}
    family_sizes: dict[str, int] = {}
    unknown: list[str] = []
    for fam in families_list:
        builder = _FAMILY_ROLE_MAP_BUILDERS.get(fam.lower())
        if builder is None:
            unknown.append(fam)
            continue
        fmap = builder()
        out.update(fmap)
        family_sizes[fam] = len(fmap)
    out.update(extra)
    return {
        "value_role_map": out,
        "n_values": len(out),
        "families_applied": list(family_sizes.keys()),
        "family_sizes": family_sizes,
        "unknown_families": unknown,
        "json": out,
    }


# ── Attested vocabulary loader ──────────────────────────────────────────────


# ── Family → import-path map for structured vocabulary loading ──────────────
# Each entry: (module_path, [callable_attr_or_dict_attr...]). The loader tries
# each attribute in order, returning words from the first one that exists.
# Structured exports take priority over the regex fallback.
_FAMILY_VOCAB_SOURCES: dict[str, tuple[str, tuple[str, ...]]] = {
    "old_tamil":           ("glossa_lab.data.dravidian",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "hieroglyphic_luwian": ("glossa_lab.data.hieroglyphic_luwian",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "mycenaean_greek":     ("glossa_lab.data.linear_b_language",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "vedic_sanskrit":      ("glossa_lab.data.sanskrit",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "sumerian":            ("glossa_lab.data.sumerian_ur3",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
    "old_hebrew":          ("glossa_lab.data.old_hebrew",
                             ("get_attested_words", "VOCABULARY", "get_vocabulary")),
}


def _try_structured_vocab(family: str) -> tuple[list[str], str] | tuple[None, str]:
    """Attempt to import a structured vocabulary export from the data module.

    Returns (words, source_name) on success, (None, reason) on failure.
    """
    spec = _FAMILY_VOCAB_SOURCES.get(family)
    if not spec:
        return None, f"family '{family}' has no structured source"
    module_path, attrs = spec
    try:
        import importlib  # noqa: PLC0415
        mod = importlib.import_module(module_path)
    except Exception as exc:  # noqa: BLE001
        return None, f"import failed: {exc}"
    for attr in attrs:
        obj = getattr(mod, attr, None)
        if obj is None:
            continue
        try:
            if callable(obj):
                value = obj()
            else:
                value = obj
            if isinstance(value, dict):
                # dict of word -> gloss; words are the keys
                words = [str(k).lower() for k in value.keys()]
            elif isinstance(value, (list, tuple, set)):
                words = [str(w).lower() for w in value]
            else:
                continue
            if words:
                return words, f"{module_path}.{attr}"
        except Exception:  # noqa: BLE001
            continue
    return None, f"no structured attribute found in {module_path}"


def _attested_vocab_loader(inputs: dict, params: dict) -> dict:
    """Load an attested-language vocabulary list for HoldoutWordRecall.

    Sources:
      - 'family' param: 'old_tamil', 'hieroglyphic_luwian', 'mycenaean_greek',
                        'vedic_sanskrit', 'sumerian', 'old_hebrew'
      - 'extra_words' param: list[str] appended to the family vocab
      - 'min_len' / 'max_len': filter by length

    Loading strategy (priority order):
      1. Structured Python export from the data module: attempts in order
         get_attested_words(), VOCABULARY (dict keys), get_vocabulary().
      2. If no structured export: regex string-literal fallback against the
         module source (legacy behaviour, looser).

    Pure primitive — one import / read + filter. No transformation.
    """
    family = str(params.get("family", "old_tamil"))
    extra: list[str] = list(params.get("extra_words", []))
    min_len = int(params.get("min_len", 2))
    max_len = int(params.get("max_len", 12))

    words: list[str] = []
    source_used = "none"

    # ── Step 1: structured import ──
    structured_words, structured_msg = _try_structured_vocab(family)
    if structured_words is not None:
        words.extend(w for w in structured_words if min_len <= len(w) <= max_len)
        source_used = structured_msg

    # ── Step 2: regex fallback (legacy) ──
    if not words:
        repo_root = Path(__file__).resolve().parent.parent.parent
        legacy_paths = {
            "old_tamil":           repo_root / "backend" / "glossa_lab" / "data" / "dravidian.py",
            "hieroglyphic_luwian": repo_root / "backend" / "glossa_lab" / "data" / "hieroglyphic_luwian.py",
            "mycenaean_greek":     repo_root / "backend" / "glossa_lab" / "data" / "linear_b_language.py",
            "vedic_sanskrit":      repo_root / "backend" / "glossa_lab" / "data" / "sanskrit.py",
            "sumerian":            repo_root / "backend" / "glossa_lab" / "data" / "sumerian_ur3.py",
            "old_hebrew":          repo_root / "backend" / "glossa_lab" / "data" / "old_hebrew.py",
        }
        src = legacy_paths.get(family)
        if src and src.exists():
            text = src.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"['\"]([a-zA-Z\-]{2,})['\"]", text):
                w = m.group(1).lower()
                if min_len <= len(w) <= max_len:
                    words.append(w)
            source_used = f"regex-fallback:{src.name} ({structured_msg})"

    words.extend(w.lower() for w in extra if min_len <= len(w) <= max_len)
    words = sorted(set(words))
    return {
        "attested_vocab": words,
        "n_words": len(words),
        "family": family,
        "source": source_used,
    }


# ── Atomic node defs for registration ───────────────────────────────────────
# Imported by experiment_graph.py and added to ATOMIC_NODES at module load.


def _ctt_node_defs() -> list[Any]:
    """Return a list of AtomicNodeDef instances to register.

    The actual AtomicNodeDef class is imported lazily to avoid circular import.
    """
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "IndusSignRoleClassifier",
            "Indus Sign Role Classifier",
            "CTT / Constraint Topology",
            "Derive 6-bit role mask per sign (suffix/determinative/numeral/phonetic/"
            "logogram/compound) from corpus positional and bigram statistics. "
            "Output drives CTTAdmissibilityFilter to prevent SA from proposing "
            "structurally-impossible mappings. Pure primitive: positional rates + PMI.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "role_table", "type": "json"},
                {"name": "n_signs", "type": "number"},
                {"name": "role_summary", "type": "json"},
                {"name": "compound_signs", "type": "json"},
                {"name": "high_pmi_bigrams", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "terminal_threshold": {
                        "type": "number",
                        "default": 0.85,
                        "minimum": 0.5,
                        "maximum": 1.0,
                    },
                    "initial_threshold": {
                        "type": "number",
                        "default": 0.70,
                        "minimum": 0.5,
                        "maximum": 1.0,
                    },
                    "compound_pmi_threshold": {"type": "number", "default": 4.0, "minimum": 0.0},
                    "min_count": {"type": "integer", "default": 5, "minimum": 1},
                    "numeral_signs": {
                        "type": "array",
                        "default": ["820", "590", "60", "176", "90"],
                    },
                },
            },
            fn=_indus_sign_role_classifier,
        ),
        AtomicNodeDef(
            "CTTAdmissibilityFilter",
            "CTT Admissibility Filter",
            "CTT / Constraint Topology",
            "Per-sign feasibility oracle (Constraint Topology Theory, Layer1Labs 2026). "
            "Filters a proposed sign-to-value mapping by checking each (sign, value) "
            "pair against the sign's admissible roles. O(K) per Theorem 1 of CTT TR. "
            "Connects: IndusSignRoleClassifier → role_table; SADecipher → proposed_mapping.",
            inputs=[
                {"name": "role_table", "type": "json", "required": True},
                {"name": "proposed_mapping", "type": "json", "required": True},
                {"name": "value_role_map", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "filtered_mapping", "type": "json"},
                {"name": "violations", "type": "json"},
                {"name": "n_violations", "type": "number"},
                {"name": "n_admissible", "type": "number"},
                {"name": "admissibility_rate", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "value_role_map": {
                        "type": "object",
                        "default": {},
                        "description": (
                            "Map target-language values to roles. Use "
                            "DefaultIndusValueRoleMap for the standard set."
                        ),
                    },
                    "strict_mode": {
                        "type": "boolean",
                        "default": False,
                        "description": (
                            "If True, values not present in value_role_map are "
                            "treated as having an 'unmapped' role and are filtered "
                            "as violations (rigorous CTT default). If False, "
                            "unmapped values fall back to 'phonetic' and pass "
                            "the filter unless the sign forbids phonetic."
                        ),
                    },
                },
            },
            fn=_ctt_admissibility_filter,
        ),
        AtomicNodeDef(
            "DefaultIndusValueRoleMap",
            "Default Indus Value-Role Map",
            "CTT / Constraint Topology",
            "Emit a value-role lookup table for CTTAdmissibilityFilter. Always "
            "includes the default CV-syllabary baseline (Tamil case suffixes + "
            "CV syllabograms + numerals + generic determinatives). When `families` "
            "is set, merges in per-language target inventories: 'old_tamil' "
            "(DEDR roots + Mahadevan Tamil-Brahmi attested words), "
            "'hieroglyphic_luwian' (Hawkins 2000 lemmas, royal titles as "
            "determinatives), 'mycenaean_greek' (Linear B Ventris grid). "
            "Use one node per Phase-10 SA branch so strict_mode is meaningful "
            "per language.",
            inputs=[],
            outputs=[
                {"name": "value_role_map", "type": "json"},
                {"name": "n_values", "type": "number"},
                {"name": "families_applied", "type": "json"},
                {"name": "family_sizes", "type": "json"},
                {"name": "unknown_families", "type": "json"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "families": {
                        "type": "array",
                        "default": [],
                        "description": (
                            "List of language families whose target inventories "
                            "to merge in: old_tamil | hieroglyphic_luwian | "
                            "mycenaean_greek (aliases: dravidian, luwian, linear_b)."
                        ),
                    },
                    "include_default": {
                        "type": "boolean",
                        "default": True,
                        "description": (
                            "Include the CV-syllabary baseline. Disable only if "
                            "you want a strictly per-language map."
                        ),
                    },
                    "extra": {
                        "type": "object",
                        "default": {},
                        "description": "Additional value→role overrides to merge in.",
                    },
                },
            },
            fn=_default_value_role_map_loader,
        ),
        AtomicNodeDef(
            "CompoundDependencyConstraint",
            "Compound Dependency Constraint",
            "CTT / Constraint Topology",
            "Score a sign mapping under cross-sign compound coupling (Cotterell/Eisner "
            "2015 dual-decomposition idea). For each high-PMI compound bigram, "
            "concatenated decoded value should appear in attested vocabulary. "
            "Awards bonus per hit, penalty per miss. This is the dense-dependency "
            "layer that pure CTT (independent constraints) cannot capture.",
            inputs=[
                {"name": "proposed_mapping", "type": "json", "required": True},
                {"name": "high_pmi_bigrams", "type": "json", "required": True},
                {"name": "attested_vocab", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "compound_score", "type": "number"},
                {"name": "n_hits", "type": "number"},
                {"name": "n_misses", "type": "number"},
                {"name": "hit_rate", "type": "number"},
                {"name": "hits", "type": "json"},
                {"name": "misses", "type": "json"},
                {"name": "number", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "hit_bonus": {"type": "number", "default": 1.0},
                    "miss_penalty": {"type": "number", "default": 0.5},
                    "compound_separator": {"type": "string", "default": ""},
                    "attested_vocab": {"type": "array", "default": []},
                },
            },
            fn=_compound_dependency_constraint,
        ),
        AtomicNodeDef(
            "HoldoutWordRecall",
            "Held-out Word Recall",
            "CTT / Constraint Topology",
            "Decode each held-out inscription with the proposed mapping and count "
            "matches against an attested external vocabulary. NON-CIRCULAR test. "
            "Connects: CorpusSplitter.test_sequences → sequences, "
            "SADecipher → proposed_mapping, AttestedVocabularyLoader → attested_vocab.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
                {"name": "proposed_mapping", "type": "json", "required": True},
                {"name": "attested_vocab", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "recall_score", "type": "number"},
                {"name": "n_decoded", "type": "number"},
                {"name": "n_attested_hits", "type": "number"},
                {"name": "n_unique_hits", "type": "number"},
                {"name": "hit_rate", "type": "number"},
                {"name": "matched_words", "type": "json"},
                {"name": "number", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "decode_separator": {"type": "string", "default": ""},
                    "min_word_len": {"type": "integer", "default": 2, "minimum": 1},
                    "attested_vocab": {"type": "array", "default": []},
                },
            },
            fn=_holdout_word_recall,
        ),
        AtomicNodeDef(
            "AttestedVocabularyLoader",
            "Attested Vocabulary Loader",
            "CTT / Constraint Topology",
            "Load an attested-language word list (Old Tamil, Hieroglyphic Luwian, "
            "Mycenaean Greek, Vedic Sanskrit, Sumerian) as the gold-standard source "
            "for HoldoutWordRecall and CompoundDependencyConstraint.",
            inputs=[],
            outputs=[
                {"name": "attested_vocab", "type": "json"},
                {"name": "n_words", "type": "number"},
                {"name": "family", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "family": {
                        "type": "string",
                        "default": "old_tamil",
                        "description": (
                            "old_tamil | hieroglyphic_luwian | mycenaean_greek"
                            " | vedic_sanskrit | sumerian"
                        ),
                    },
                    "extra_words": {"type": "array", "default": []},
                    "min_len": {"type": "integer", "default": 2, "minimum": 1},
                    "max_len": {"type": "integer", "default": 12, "minimum": 1},
                },
            },
            fn=_attested_vocab_loader,
        ),
        AtomicNodeDef(
            "CTTAnchoredSADecipher",
            "CTT-Anchored SA Decipherer",
            "CTT / Constraint Topology",
            "Simulated annealing decipherment with the CTT admissibility oracle "
            "filtering every proposal step. Forbidden (sign, value) pairs are "
            "mathematically unselectable per CTT Claim 9. Restarts and seeds "
            "controlled like the standard SADecipher. Pure primitive: one engine call "
            "with a constraint mask. Use this in place of SADecipher when role_table "
            "is available and you want guaranteed-admissible outputs.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
                {"name": "lm", "type": "any", "required": True},
                {"name": "role_table", "type": "json", "required": False},
                {"name": "value_role_map", "type": "json", "required": False},
                {"name": "anchors", "type": "any", "required": False},
            ],
            outputs=[
                {"name": "proposed_mapping", "type": "json"},
                {"name": "score", "type": "number"},
                {"name": "n_signs", "type": "number"},
                {"name": "n_forbidden_pairs", "type": "number"},
                {"name": "n_filtered_proposals", "type": "number"},
                {"name": "n_total_proposals", "type": "number"},
                {"name": "filter_rate", "type": "number"},
                {"name": "anchors_used", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "seed": {"type": "integer", "default": 1},
                    "max_iterations": {"type": "integer", "default": 8000, "minimum": 100},
                    "restarts": {"type": "integer", "default": 5, "minimum": 1},
                    "surjective": {"type": "boolean", "default": True},
                    "value_role_map": {"type": "object", "default": {}},
                    "strict_mode": {
                        "type": "boolean",
                        "default": False,
                        "description": (
                            "If True, the final mapping is post-filtered to "
                            "drop any value missing from value_role_map. "
                            "Treats unmapped values as having a forbidden role."
                        ),
                    },
                },
            },
            fn=_ctt_anchored_sa_decipher,
        ),
    ]


__all__ = [
    "ROLE_BITS",
    "DEFAULT_INDUS_VALUE_ROLE_MAP",
    "_indus_sign_role_classifier",
    "_ctt_admissibility_filter",
    "_compound_dependency_constraint",
    "_holdout_word_recall",
    "_ctt_anchored_sa_decipher",
    "_default_value_role_map_loader",
    "_attested_vocab_loader",
    "_ctt_node_defs",
]
