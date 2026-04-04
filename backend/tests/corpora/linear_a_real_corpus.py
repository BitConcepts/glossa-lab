"""Real Linear A corpus loader.

Builds a sign sequence from actual tablet bigram statistics downloaded from:
  tylerlengyel.com/linearA/research/output/latest/ (CC-compatible, academic)

Data derived from John G. Younger's Linear A transliterations, covering
~9 tablets from Haghia Triada (HT) and Zakros (ZA), processed through
a structural analysis pipeline.

Signs appear in mixed notation:
  - Phonetic values for signs with Linear B correspondences:
    KU, DA, PA, RE, TA, RA, RA2, MA, NA, SA, KI, MI, KA, SI, TE,
    RO, TI, TU, I, U, A, DU, JA, DI, RI, SE, ME, ZA, NI, NU, SU,
    PI, PU, QA, DE, ZU, NE, WA, WI, JU, QE, ...
  - GORILA codes for signs without consensus values:
    AB81, AB08, AB59, AB01, AB67, AB06, AB28, AB77, AB02, AB27, AB60,
    AB57, AB03, AB41, AB80, AB31, AB07, AB73, AB51, AB37, AB26, AB53,
    AB04, AB69, AB79, AB56, AB78, AB09, AB30, AB39, AB58, AB45, AB46,
    AB16, AB86, AB55, AB65, AB17, AB19, AB40, AB47, ...

Known Linear A words (Younger 2000, Packard 1974):
  ku-ro      = "total" (administrative term, most common formula)
  sa-ra2     = "flax" (extremely frequent at Haghia Triada)
  ki-re-ta2  = "barley" (from Greek loan krithe)
  mi-ja      = unknown (personal name or title?)
  a-du       = unknown (possibly "product" or "contribution")
  ku-ro      appears ~25 times in the real corpus

Sources:
  tylerlengyel.com/linearA (2025) — structural analysis of Younger's data
  Younger, J.G. (2024). Linear A Texts in Phonetic Transcription.
    academia.edu/117949876
  Packard, D.W. (1974). Minoan Linear A.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "fixtures" / "linear_a_real"

# ── GORILA-code → tentative phonetic value ────────────────────────────
# Based on Linear B homomorphic sign correspondences (Ventris / Younger 2000).
# Only signs with reasonable consensus are listed; uncertain mappings omitted.
GORILA_TO_PHONEME: dict[str, str] = {
    "AB01": "da",
    "AB02": "ro",
    "AB03": "pa",
    "AB04": "te",
    "AB06": "na",
    "AB07": "di",
    "AB08": "a",
    "AB09": "se",
    "AB10": "u",
    "AB13": "me",
    "AB16": "qa",
    "AB17": "za",
    "AB22": "mi2",
    "AB23": "mu",
    "AB24": "ne",
    "AB25": "a2",
    "AB26": "ru2",
    "AB27": "re",
    "AB28": "i",
    "AB29": "pu2",
    "AB30": "ni",
    "AB31": "sa",
    "AB34": "a3",
    "AB37": "ti",
    "AB38": "e",
    "AB40": "wi",
    "AB41": "si",
    "AB45": "de",
    "AB46": "je",
    "AB47": "twe",
    "AB48": "nwa",
    "AB49": "du2",
    "AB50": "pu",
    "AB51": "du",
    "AB53": "ri",
    "AB54": "wa",
    "AB55": "nu",
    "AB56": "pa3",
    "AB57": "ja",
    "AB58": "su",
    "AB59": "ta2",
    "AB60": "ra",
    "AB61": "o",
    "AB65": "ju",
    "AB66": "ta2v",
    "AB67": "ki",
    "AB68": "ro2",
    "AB70": "ko",
    "AB73": "mi3",
    "AB77": "ka",
    "AB78": "qe",
    "AB79": "zu",
    "AB80": "ma",
    "AB81": "?81",
    "AB86": "a2v",
}

# Signs already written as phonetic values — normalise to lowercase
_ALREADY_PHONETIC = {
    "KU",
    "DA",
    "PA",
    "RE",
    "TA",
    "RA",
    "RA2",
    "MA",
    "NA",
    "SA",
    "KI",
    "MI",
    "KA",
    "SI",
    "TE",
    "RO",
    "TI",
    "TU",
    "I",
    "U",
    "A",
    "DU",
    "JA",
    "DI",
    "RI",
    "SE",
    "ME",
    "ZA",
    "NI",
    "NU",
    "SU",
    "PI",
    "PU",
    "QA",
    "DE",
    "ZU",
    "NE",
    "WA",
    "WI",
    "JU",
    "QE",
    "MU",
    "KO",
    "PO",
    "TO",
    "JE",
    "TA2",
    "PA3",
    "RA2",
    "PU2",
    "NWA",
    "ZE",
    "KE",
    "NO",
    "SO",
    "DO",
    "GO",
    "WO",
}

# Signs to discard (logograms, numerals, damage markers, editorial notes)
_SKIP_SIGNS = {
    "[?]",
    "GRA",
    "OLE",
    "OLIV",
    "FIC",
    "VIR",
    "VINA",
    "VINB",
    "VINC",
    "VIN",
    "FIC",
    "OVIS",
    "OVISF",
    "OVISM",
    "BOSM",
    "BOS",
    "SUS",
    "TELA",
    "CAPM",
    "VAS",
    "BOSM",
    "DESUNT",
    "B",
    "F",
    "D",
    "K",
    "L2",
    "L3L3",
    "CF",
    "IB",
    "HT",
    "ZB",
    "[NAME",
    "IMPRESSION",
    "*411VASB",
    "*401VAS",
    "*164D",
    "*164A",
    "*164B",
    "*164C",
    "UNIT",
    "EACH",
    "IMMEDIATELY",
    "AFTER",
    "BEFORE",
    "SAME",
    "AS",
    "IF",
    "ARE",
    "THEY",
    "BE",
    "MIGHT",
    "PEOPLE",
    "CHILDREN?",
    "NOT",
    "PRESERVED",
    "DISC",
    "PAPYRUS",
    "MOTIF",
    "VESTIGIA",
    "GRAFFITO",
    "NEW",
    "WINE",
    "FIGS",
    "RATIO",
    "IS",
    "TIMES",
    "WHERE",
    "THIS",
    "AMOUNT",
    "3RD",
    "10TH",
    "20TH",
    "ASARA2",
    "MAIMI",
    "TARA",
    "OFIMPRESSIONS",
}

# ── Corpus building ───────────────────────────────────────────────────


def _load_sign_frequencies() -> dict[str, float]:
    """Load sign unigram frequencies from CSV."""
    freqs: dict[str, float] = {}
    f = _DATA_DIR / "phase1_sign_frequency.csv"
    if not f.exists():
        return {}
    with open(f, encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            sign = row["sign"].strip()
            if (
                sign
                and sign not in _SKIP_SIGNS
                and not sign.startswith("]")
                and not sign.startswith("[[")
            ):
                try:
                    freqs[sign] = float(row["relative_frequency"])
                except (ValueError, KeyError):
                    pass
    return freqs


def _load_bigrams() -> list[tuple[str, str, float]]:
    """Load bigram frequencies. Returns (sign1, sign2, count)."""
    bigrams: list[tuple[str, str, float]] = []
    f = _DATA_DIR / "phase1_bigram_frequency.csv"
    if not f.exists():
        return []
    with open(f, encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            bigram = row["bigram"].strip()
            parts = bigram.split(" ", 1)
            if len(parts) == 2:
                s1, s2 = parts
                s1, s2 = s1.strip(), s2.strip()
                # Skip if either sign is a logogram / noise
                if (
                    s1 in _SKIP_SIGNS
                    or s2 in _SKIP_SIGNS
                    or s1.startswith("]")
                    or s2.startswith("]")
                    or s1.startswith("[[")
                    or s2.startswith("[[")
                ):
                    continue
                if "[?" in s1 or "[?" in s2:
                    continue
                try:
                    cnt = float(row["count"])
                    bigrams.append((s1, s2, cnt))
                except (ValueError, KeyError):
                    pass
    return bigrams


def _translate_sign(sign: str) -> str:
    """Translate a sign to its phonetic value (lowercase) or keep as code."""
    s = sign.strip()
    if s in _ALREADY_PHONETIC:
        return s.lower()
    if s in GORILA_TO_PHONEME:
        return GORILA_TO_PHONEME[s]
    # Keep unknown signs as-is (they remain as opaque codes)
    return s


def generate_real_linear_a_sequence(
    seed: int = 42,
    n_tokens: int = 6000,
) -> list[str]:
    """Generate a sign sequence using the real bigram distribution.

    Uses a first-order Markov chain sampled from the actual bigram
    frequencies observed across the HT, KH, and ZA tablet corpora.

    Args:
        seed: Random seed.
        n_tokens: Approximate number of sign tokens to generate.

    Returns:
        List of sign tokens (mix of phonetic values and GORILA codes).
    """
    rng = random.Random(seed)
    freqs = _load_sign_frequencies()
    bigrams = _load_bigrams()

    if not bigrams:
        # Fallback: use unigram sampling if bigrams not available
        signs = list(freqs.keys())
        weights = [freqs[s] for s in signs]
        total = sum(weights)
        norm = [w / total for w in weights]
        result = []
        while len(result) < n_tokens:
            r = rng.random()
            cum = 0.0
            for sign, w in zip(signs, norm):
                cum += w
                if r <= cum:
                    result.append(sign)
                    break
        return result

    # Build bigram transition table: {sign: [(next_sign, weight), ...]}
    transitions: dict[str, list[tuple[str, float]]] = {}
    for s1, s2, cnt in bigrams:
        transitions.setdefault(s1, []).append((s2, cnt))

    # Normalise weights per origin
    trans_norm: dict[str, tuple[list[str], list[float]]] = {}
    for s1, nexts in transitions.items():
        signs_list = [s2 for s2, _ in nexts]
        raw = [cnt for _, cnt in nexts]
        total = sum(raw)
        trans_norm[s1] = (signs_list, [w / total for w in raw])

    # Unigram fallback for cold starts
    all_signs = list(freqs.keys())
    all_weights = [freqs[s] for s in all_signs]
    total_ug = sum(all_weights)
    unigram_norm = [w / total_ug for w in all_weights]

    def sample_from(signs_l: list[str], weights_l: list[float]) -> str:
        r = rng.random()
        cum = 0.0
        for s, w in zip(signs_l, weights_l):
            cum += w
            if r <= cum:
                return s
        return signs_l[-1]

    result: list[str] = []
    current = sample_from(all_signs, unigram_norm)

    while len(result) < n_tokens:
        result.append(current)
        if current in trans_norm:
            nxt_signs, nxt_weights = trans_norm[current]
            current = sample_from(nxt_signs, nxt_weights)
        else:
            # No outgoing bigrams — restart from unigram
            current = sample_from(all_signs, unigram_norm)

    return result[:n_tokens]


def translate_sequence_to_phonemes(sequence: list[str]) -> list[str]:
    """Translate a sign sequence to phonetic values where known.

    Signs without consensus readings are kept as their GORILA codes.
    """
    return [_translate_sign(s) for s in sequence]


def extract_phoneme_only_words(
    sequence: list[str],
    min_word_len: int = 2,
    max_word_len: int = 6,
) -> list[str]:
    """Extract word-group strings where all signs have known phonetic values.

    A word group is a run of signs all of which have consensus phonetic
    readings. Words with any unknown (AB-code) signs are excluded.

    Returns list of phoneme strings (syllables concatenated, e.g. 'kuro').
    """
    words = []
    run: list[str] = []

    for sign in sequence:
        phoneme = _translate_sign(sign)
        # Check if sign was translated (phoneme differs from sign code)
        is_known = sign in _ALREADY_PHONETIC or sign in GORILA_TO_PHONEME
        if is_known and not phoneme.startswith("?"):
            run.append(phoneme)
            if len(run) >= max_word_len:
                if len(run) >= min_word_len:
                    words.append("".join(run))
                run = []
        else:
            if len(run) >= min_word_len:
                words.append("".join(run))
            run = []

    if len(run) >= min_word_len:
        words.append("".join(run))

    return words


# ── Known Linear A vocabulary ─────────────────────────────────────────

# Words identified or strongly hypothesised by scholars.
# Source: Younger (2000, 2024), Packard (1974), Hooker (1980)
KNOWN_LINEAR_A_WORDS: dict[str, str] = {
    "kuro": "total (administrative formula; cf. ku-ro ~25× in corpus)",
    "kirota": "barley? (cf. Greek krithe; Younger 2000)",
    "kireta": "barley / grain allocation (tentative reading of ki-re-ta2)",
    "sara": "flax? (sa-ra2 very frequent at HT; Younger 2000)",
    "sara2": "flax (most frequent content word at Haghia Triada)",
    "saro": "flax (variant reading)",
    "adu": "product? contribution? (uncertain)",
    "adaro": "unknown (common pattern)",
    "mija": "unknown (personal name or occupational title?)",
    "mijaruma": "unknown (recurring 3-syllable form)",
    "dame": "community? (cf. Linear B damo)",
    "damesi": "of the community? (tentative)",
    "damesina": "conjunction? (da-me-si-na, possibly 'and')",
    "tana": "unknown (frequent pattern)",
    "tanati": "unknown (recurring)",
    "qaqaru": "unknown (qa-qa-ru, appears in accounts)",
    "pata": "unknown (pa-ta, short formula)",
    "paja": "unknown (pa-ja)",
    "ruma": "unknown",
    "ruta": "unknown",
    "nipa": "unknown (ni-pa, possibly a product name)",
    "pajare": "unknown (pa-ja-re)",
    "kunisu": "emmer wheat? (ku-ni-su; Younger 2000)",
    "didero": "einkorn wheat? (di-de-ro; Younger 2000)",
}

# ── Raw tablet corpus from corpus_manifest.csv ───────────────────────

#: Site prefix map for partitioning.
#: HT = Haghia Triada, KH = Khania, ZA = Zakros, PH = Pyrgos/Phaistos,
#: ARKH = Arkhanes, KN = Knossos, MA = Malia, ZE = Zernos, TY = Tylissos
SITE_PREFIXES: dict[str, str] = {
    "HT": "Haghia Triada",
    "KH": "Khania",
    "ZA": "Zakros",
    "PH": "Pyrgos/Phaistos",
    "ARKH": "Arkhanes",
    "KN": "Knossos",
    "MA": "Malia",
    "TY": "Tylissos",
    "GO": "Gournies",
    "PE": "Petras",
    "PK": "Palaikastro",
    "PS": "Pseira",
    "SY": "Sklavokampos",
}


def load_raw_tablet_corpus(
    sites: list[str] | None = None,
    exclude_logograms: bool = True,
) -> tuple[list[str], dict[str, list[str]]]:
    """Load actual tablet sign sequences from corpus_manifest.csv.

    Parses the canonical_sequence column (actual transcription order per
    inscription entry) grouped by artifact_id, then concatenated.

    Args:
        sites: List of site prefixes to include (e.g. ['HT', 'KH']).
               If None, include all sites.
        exclude_logograms: If True, skip rows tagged as logograms
                           (younger_table_logogram or similar).

    Returns:
        (flat_sequence, site_dict) where:
          flat_sequence: all signs concatenated in tablet order
          site_dict:     {site_prefix: [signs]} for separate analysis
    """
    manifest = _DATA_DIR / "phase1_corpus_manifest.csv"
    if not manifest.exists():
        # Fallback: use Markov chain if manifest not available
        return generate_real_linear_a_sequence(), {}

    site_signs: dict[str, list[str]] = {}
    all_signs: list[str] = []

    with open(manifest, encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            artifact = row.get("artifact_id", "").strip()
            sequence = row.get("canonical_sequence", "").strip()
            notes = row.get("notes", "").lower()

            # Skip if this entry is a logogram row
            if exclude_logograms and "logogram" in notes:
                continue

            # Determine site prefix
            site = None
            for prefix in SITE_PREFIXES:
                if artifact.startswith(prefix):
                    site = prefix
                    break
            if site is None:
                site = artifact.split()[0] if artifact else "OTHER"

            # Filter by requested sites
            if sites and site not in sites:
                continue

            # Parse sign tokens from sequence
            tokens = []
            for tok in sequence.split():
                t = tok.strip()
                if not t:
                    continue
                # Skip leading ] damage markers and [[..]] restoration brackets
                t_clean = t.lstrip("]")
                if t_clean.startswith("[[") or t_clean.endswith("]]"):
                    continue
                if t_clean in _SKIP_SIGNS:
                    continue
                if t_clean.startswith("[") and t_clean != t_clean.rstrip("]"):
                    continue  # skip [?] etc.
                if "[?" in t_clean:
                    continue
                if t_clean:
                    tokens.append(t_clean)

            if tokens:
                all_signs.extend(tokens)
                site_signs.setdefault(site, []).extend(tokens)

    return all_signs, site_signs


# ── Loaders for real.py ───────────────────────────────────────────────


def load_real_linear_a_signs(seed: int = 42) -> list[str]:
    """Load a sign sequence from the real bigram-based corpus."""
    return generate_real_linear_a_sequence(seed=seed)


def load_real_linear_a_phonemes(seed: int = 42) -> list[str]:
    """Load phonemically decoded Linear A tokens.

    Known signs translated to tentative phoneme values;
    unknown signs kept as GORILA codes.
    """
    seq = generate_real_linear_a_sequence(seed=seed)
    return translate_sequence_to_phonemes(seq)
