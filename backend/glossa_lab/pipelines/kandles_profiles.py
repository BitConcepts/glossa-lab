"""Language-specific Kandles phoneme-colour profiles.

The default Kandles system ([REDACTED-PATENT-PUB]) uses a single
Greek/English-calibrated phoneme→colour mapping for all comparisons.
This is appropriate when both corpora are transcribed in the same
phonological system, but introduces a systematic bias when comparing
deciphered texts from different language families.

Each profile redefines the 8 Kandles colour groups using the phonological
categories natural to that language family. The 8 groups remain fixed
(they are the Kandles patent categories), but which phonemes fall into
which group changes according to the target language's phonology.

BIAS CORRECTION PRINCIPLE:
  When testing hypothesis X (e.g. Luwian), the Kandles similarity score
  should compare the deciphered Linear A corpus against the Luwian target
  corpus using LUWIAN phonological categories, not Greek ones.
  This makes the fingerprint comparison linguistically fair.

USAGE:
    from glossa_lab.pipelines.kandles_profiles import get_profile, PROFILE_NAMES
    profile = get_profile("luwian")
    # profile.letter_to_group: dict[str, int] (uppercase letter → group 0-7)
    # profile.digraph_to_group: dict[str, int] (uppercase digraph → group 0-7)
    # profile.name: str
    # profile.description: str

PHONOLOGICAL SOURCES:
  Greek/Default: Extended Soundex (Merkur patent baseline)
  Luwian:        Melchert (1994) Anatolian Historical Phonology; Yakubovich (2010)
  Hurrian:       Wilhelm (1989) The Hurrians; Wegner (2007) Hurritisch
  Semitic:       Huehnergard (2005) Proto-Semitic; Fox (2003)
  Dravidian:     Krishnamurti (2003) The Dravidian Languages
  Sumerian:      Jagersma (2010) Descriptive Grammar of Sumerian
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class KandlesProfile:
    """A language-specific Kandles phoneme→colour mapping.

    The 8 colour groups retain their Kandles semantics (Yellow=Sun, Grey=Moon,
    etc.) but the phoneme assignments differ per language family.
    """

    name: str
    description: str
    groups: dict[int, dict[str, Any]]  # group_num → {letters, digraphs, ...}
    letter_to_group: dict[str, int] = field(default_factory=dict)
    digraph_to_group: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.letter_to_group = {}
        self.digraph_to_group = {}
        for gnum, ginfo in self.groups.items():
            for letter in ginfo.get("letters", set()):
                self.letter_to_group[letter.upper()] = gnum
            for digraph in ginfo.get("digraphs", set()):
                self.digraph_to_group[digraph.upper()] = gnum


# ── Profile 0: Default / Mycenaean Greek ─────────────────────────────
# The original Kandles mapping from [REDACTED-PATENT-PUB].
# Calibrated for Greek/English phonological categories.
_DEFAULT_GROUPS: dict[int, dict[str, Any]] = {
    0: {"letters": set("AEIOU"), "color": "White",
        "nature": "Vowel", "description": "All vowels"},
    1: {"letters": {"K", "G", "J", "C", "Q"}, "color": "Yellow",
        "nature": "Sun", "digraphs": {"CH"},
        "description": "Velars and palatals"},
    2: {"letters": {"M", "N"}, "color": "Grey",
        "nature": "Moon", "digraphs": set(),
        "description": "Nasals"},
    3: {"letters": {"T", "D"}, "color": "Red",
        "nature": "Fire", "digraphs": {"TH"},
        "description": "Dentals"},
    4: {"letters": {"R", "L"}, "color": "Blue",
        "nature": "Water", "digraphs": set(),
        "description": "Liquids"},
    5: {"letters": {"Y", "W", "H"}, "color": "Green",
        "nature": "Tree", "digraphs": {"KH"},
        "description": "Semivowels and laryngeals"},
    6: {"letters": {"P", "B", "F", "V"}, "color": "Purple",
        "nature": "Flower", "digraphs": set(),
        "description": "Labials"},
    7: {"letters": {"S", "Z", "X"}, "color": "Brown",
        "nature": "Soil", "digraphs": {"SH"},
        "description": "Sibilants"},
}

PROFILE_DEFAULT = KandlesProfile(
    name="default",
    description=(
        "Greek/English baseline (Merkur patent [REDACTED-PATENT-PUB]). "
        "Calibrated for Mycenaean Greek syllabary comparison."
    ),
    groups=_DEFAULT_GROUPS,
)


# ── Profile 1: Luwian / Anatolian ────────────────────────────────────
# Luwian (and other Anatolian IE languages: Hittite, Palaic, Lycian) have:
#   - Distinctive laryngeals inherited from proto-IE: h₂ (ḫ) is uvular
#   - Labialized velars (kw-, gw-, hw-) are a key phonological class
#   - W functions as a semivowel/consonant pair (not grouped with H)
#   - The sibilant system is simpler (mainly s, less z)
#   - Gemination is phonological (pp, tt, kk distinct from p, t, k)
#
# Key changes from default:
#   Gr5 (Green/Tree): H → separate laryngeal group; W stays Green
#   Gr1 (Yellow/Sun): KW (labiovelar) added explicitly
#   Gr5 (Green/Tree): laryngeals and their reflexes (H, HH/KH)

_LUWIAN_GROUPS: dict[int, dict[str, Any]] = {
    0: {"letters": set("AEIOU"), "color": "White",
        "nature": "Vowel", "description": "Vowels"},
    1: {"letters": {"K", "G", "Q"}, "color": "Yellow",
        "nature": "Sun", "digraphs": {"KW", "GW"},
        "description": "Velars + labialized velars (kw/gw) — key Anatolian class"},
    2: {"letters": {"M", "N"}, "color": "Grey",
        "nature": "Moon", "digraphs": {"NN"},
        "description": "Nasals (including geminate NN common in Luwian)"},
    3: {"letters": {"T", "D"}, "color": "Red",
        "nature": "Fire", "digraphs": {"TT", "DD", "TS"},
        "description": "Dentals (geminates TT/DD common in Luwian)"},
    4: {"letters": {"R", "L"}, "color": "Blue",
        "nature": "Water", "digraphs": {"LL", "RR"},
        "description": "Liquids (geminates LL/RR also occur)"},
    5: {"letters": {"H", "Y"}, "color": "Green",
        "nature": "Tree", "digraphs": {"HH", "KH", "HW"},
        "description": "Laryngeals h₁/h₂/h₃ reflexes — major Anatolian category"},
    6: {"letters": {"P", "B", "V", "W"}, "color": "Purple",
        "nature": "Flower", "digraphs": {"PP"},
        "description": "Labials + W (labiodental class in Anatolian)"},
    7: {"letters": {"S", "Z"}, "color": "Brown",
        "nature": "Soil", "digraphs": {"SS", "SH", "ZZ"},
        "description": "Sibilants (Luwian has s/z contrast, geminates)"},
}

PROFILE_LUWIAN = KandlesProfile(
    name="luwian",
    description=(
        "Luwian/Anatolian phonological categories. "
        "Emphasises laryngeals (h₁/h₂/h₃) and labialized velars (kw/gw) "
        "as major distinctive classes. Source: Melchert (1994), Yakubovich (2010)."
    ),
    groups=_LUWIAN_GROUPS,
)


# ── Profile 2: Hurrian ───────────────────────────────────────────────
# Hurrian (non-IE, ergative, spoken c. 2300–1200 BCE in Mesopotamia/Syria) has:
#   - Uvular stop q (different from velar k/g)
#   - Fricative h (not clearly laryngeal, may be pharyngeal)
#   - Agglutinative morphology with rich suffix system
#   - No labial fricatives (no f/v)
#   - Geminate consonants phonological
#   - Emphatic/ejective consonants disputed but possible
#
# Key changes from default:
#   Gr1: Q (uvular stop) separated from K/G into their own group (uvular = Gr5)
#   Gr5: H (pharyngeal fricative) gets its own group with Y

_HURRIAN_GROUPS: dict[int, dict[str, Any]] = {
    0: {"letters": set("AEIOUEI"), "color": "White",
        "nature": "Vowel", "description": "Vowels (a/e/i/o/u)"},
    1: {"letters": {"K", "G"}, "color": "Yellow",
        "nature": "Sun", "digraphs": {"KK"},
        "description": "Velars k/g (uvular Q is separate)"},
    2: {"letters": {"M", "N"}, "color": "Grey",
        "nature": "Moon", "digraphs": {"NN"},
        "description": "Nasals"},
    3: {"letters": {"T", "D"}, "color": "Red",
        "nature": "Fire", "digraphs": {"TT", "TS"},
        "description": "Dentals and affricates"},
    4: {"letters": {"R", "L"}, "color": "Blue",
        "nature": "Water", "digraphs": {"LL"},
        "description": "Liquids"},
    5: {"letters": {"H", "Q", "X"}, "color": "Green",
        "nature": "Tree", "digraphs": {"KH"},
        "description": "Uvular q + pharyngeal h — major Hurrian phonological category"},
    6: {"letters": {"P", "B", "W"}, "color": "Purple",
        "nature": "Flower", "digraphs": {"PP"},
        "description": "Labials (no f/v in Hurrian; W is labial semivowel)"},
    7: {"letters": {"S", "Z", "SH", "ZH", "J"}, "color": "Brown",
        "nature": "Soil", "digraphs": {"SH", "ZZ", "SS"},
        "description": "Sibilants and affricates (rich in Hurrian)"},
}

PROFILE_HURRIAN = KandlesProfile(
    name="hurrian",
    description=(
        "Hurrian phonological categories. "
        "Separates uvular Q from velar K/G; treats pharyngeal H as uvular-class. "
        "Source: Wilhelm (1989), Wegner (2007)."
    ),
    groups=_HURRIAN_GROUPS,
)


# ── Profile 3: Proto-Semitic ─────────────────────────────────────────
# Proto-Semitic and daughter languages (Phoenician, Akkadian, Arabic, Hebrew) have:
#   - Pharyngeal consonants: ʿ (ayin) and ħ (he/het) — MAJOR class
#   - Emphatic stops: ṭ, ḍ, ṣ (glottalised or pharyngealised)
#   - Uvular stop q (qoph) — distinct from k
#   - Laryngeal ʾ (aleph, glottal stop) — consonantal
#   - Triconsonantal root system makes consonant classes critical
#   - Rich sibilant system: s, š, ṣ, z
#
# Key changes from default:
#   Gr5 (Green): PHARYNGEALS get own group (ʿ/ayin, ħ/ḥet)
#   Gr1 (Yellow): Q (uvular) joins velars K/G
#   New "emphatic" class grouped with dentals in Red

_SEMITIC_GROUPS: dict[int, dict[str, Any]] = {
    0: {"letters": set("AEIOU"), "color": "White",
        "nature": "Vowel", "description": "Vowels"},
    1: {"letters": {"K", "G", "Q", "C"}, "color": "Yellow",
        "nature": "Sun", "digraphs": {"KH"},
        "description": "Velars + uvular Q (qoph) — all dorsal stops"},
    2: {"letters": {"M", "N"}, "color": "Grey",
        "nature": "Moon",
        "description": "Nasals"},
    3: {"letters": {"T", "D"}, "color": "Red",
        "nature": "Fire", "digraphs": {"TH", "DH", "TS"},
        "description": "Dentals + dental emphatics (ṭ, ḍ grouped here)"},
    4: {"letters": {"R", "L"}, "color": "Blue",
        "nature": "Water",
        "description": "Liquids"},
    5: {"letters": {"H", "Y", "W"}, "color": "Green",
        "nature": "Tree", "digraphs": {"GH", "KH"},
        "description": "PHARYNGEALS + laryngeals — critical Semitic category "
                       "(ʿ/ayin, ħ/ḥet, ʾ/aleph all map here)"},
    6: {"letters": {"P", "B", "F", "V"}, "color": "Purple",
        "nature": "Flower",
        "description": "Labials"},
    7: {"letters": {"S", "Z", "X", "J"}, "color": "Brown",
        "nature": "Soil", "digraphs": {"SH", "TS"},
        "description": "Sibilants + emphatic sibilant ṣ — rich Semitic sibilant system"},
}

PROFILE_SEMITIC = KandlesProfile(
    name="semitic",
    description=(
        "Proto-Semitic phonological categories. "
        "Groups uvular Q with velars; highlights pharyngeal class (ʿ/ħ). "
        "Source: Huehnergard (2005), Fox (2003)."
    ),
    groups=_SEMITIC_GROUPS,
)


# ── Profile 4: Proto-Dravidian ───────────────────────────────────────
# Proto-Dravidian and daughter languages (Tamil, Kannada, Telugu, Malayalam) have:
#   - RETROFLEX consonants: ṭ, ḍ, ṇ, ṛ, ḷ — the most important class
#   - Three-way place distinction: dental vs alveolar vs retroflex
#   - Two types of R: alveolar r, retroflex ṟ
#   - Three types of N: dental n, alveolar ṉ, retroflex ṇ
#   - Dravidian has no aspirates (ph, bh not native)
#   - The retroflex class is what most distinguishes Dravidian from IE languages
#
# Key changes from default:
#   Gr4 (Blue): Retroflex class gets Blue — R (dental), ṟ (retroflex R), ḷ (retroflex L)
#   Gr3 (Red): Dental T/D gets Red; retroflex ṭ/ḍ also Red (both retroflex and dental dentals)
#   Gr1 (Yellow): K group includes K/G only (no uvular Q which is not native)

_DRAVIDIAN_GROUPS: dict[int, dict[str, Any]] = {
    0: {"letters": set("AEIOU"), "color": "White",
        "nature": "Vowel", "description": "Vowels (Tamil: a, ā, i, ī, u, ū, e, ē, o, ō)"},
    1: {"letters": {"K", "G", "C"}, "color": "Yellow",
        "nature": "Sun", "digraphs": {"CH"},
        "description": "Velars and palatal K/G — dorsal stops"},
    2: {"letters": {"M", "N"}, "color": "Grey",
        "nature": "Moon", "digraphs": {"NN", "NY"},
        "description": "Nasals (dental n + palatal ny/ñ in Dravidian)"},
    3: {"letters": {"T", "D"}, "color": "Red",
        "nature": "Fire", "digraphs": {"TT", "DD"},
        "description": "DENTAL and RETROFLEX stops — critical Dravidian class "
                       "(dental ṯ vs retroflex ṭ vs alveolar t all grouped here)"},
    4: {"letters": {"R", "L", "V"}, "color": "Blue",
        "nature": "Water", "digraphs": {"RR", "LL", "ZH"},
        "description": "RETROFLEX liquids — critical Dravidian class: "
                       "r, ṟ (alveolar trill), ṛ (retroflex), l, ḷ (retroflex), "
                       "ḻ (approximant zha in Tamil)"},
    5: {"letters": {"Y", "W", "H"}, "color": "Green",
        "nature": "Tree",
        "description": "Semivowels and fricative H (rare in native Dravidian words)"},
    6: {"letters": {"P", "B", "F"}, "color": "Purple",
        "nature": "Flower",
        "description": "Labials (no native aspirates ph/bh in Proto-Dravidian)"},
    7: {"letters": {"S", "Z", "J", "X"}, "color": "Brown",
        "nature": "Soil", "digraphs": {"SH"},
        "description": "Sibilants + affricates (c/ch in Tamil)"},
}

PROFILE_DRAVIDIAN = KandlesProfile(
    name="dravidian",
    description=(
        "Proto-Dravidian phonological categories. "
        "Highlights retroflex class (ṭ/ḍ/ṇ/ṛ/ḷ) as major distinctive category. "
        "Source: Krishnamurti (2003) The Dravidian Languages."
    ),
    groups=_DRAVIDIAN_GROUPS,
)


# ── Profile 5: Sumerian ──────────────────────────────────────────────
# Sumerian (non-IE, non-Semitic, spoken c. 3500–2000 BCE in Mesopotamia):
#   - Reconstructed phonology is partially uncertain
#   - Has a consonant g₁ (= /ŋ/ velar nasal, distinct from g)
#   - Possible pharyngeal /ʕ/ (written as subscript digit 2)
#   - Agglutinative with complex verb-prefix system
#   - Prefix morphology makes initial consonant class critical
#   - Key classes: stops, nasals, sibilants, liquids, laryngeals
#   - No labiodentals (f/v) in original Sumerian
#
# Key changes from default:
#   Gr2 (Grey/Moon): Velar nasal ŋ (written G₂/NG) joins nasals M/N
#   Gr5 (Green/Tree): H/laryngeal + possible ʕ
#   Gr1 (Yellow/Sun): K/G (velars without ŋ)

_SUMERIAN_GROUPS: dict[int, dict[str, Any]] = {
    0: {"letters": set("AEIOU"), "color": "White",
        "nature": "Vowel", "description": "Vowels (a, e, i, u in Sumerian)"},
    1: {"letters": {"K", "G", "Q"}, "color": "Yellow",
        "nature": "Sun", "digraphs": {"KK"},
        "description": "Velars k/g (not including velar nasal ŋ)"},
    2: {"letters": {"M", "N"}, "color": "Grey",
        "nature": "Moon", "digraphs": {"NG", "NN"},
        "description": "Nasals including VELAR NASAL ŋ (NG/G₂) — important Sumerian class"},
    3: {"letters": {"T", "D"}, "color": "Red",
        "nature": "Fire", "digraphs": {"TT"},
        "description": "Dentals t/d"},
    4: {"letters": {"R", "L"}, "color": "Blue",
        "nature": "Water", "digraphs": {"LL"},
        "description": "Liquids r/l"},
    5: {"letters": {"H", "Y", "W"}, "color": "Green",
        "nature": "Tree", "digraphs": {"KH"},
        "description": "Laryngeals and semivowels (H possibly pharyngeal in Sumerian)"},
    6: {"letters": {"P", "B"}, "color": "Purple",
        "nature": "Flower", "digraphs": {"PP"},
        "description": "Labials p/b (no f/v in native Sumerian)"},
    7: {"letters": {"S", "Z", "J", "X"}, "color": "Brown",
        "nature": "Soil", "digraphs": {"SH", "ZZ"},
        "description": "Sibilants s/z/sh"},
}

PROFILE_SUMERIAN = KandlesProfile(
    name="sumerian",
    description=(
        "Sumerian phonological categories. "
        "Adds velar nasal ŋ (NG) to the nasal class; treats H as possible pharyngeal. "
        "Source: Jagersma (2010) Descriptive Grammar of Sumerian."
    ),
    groups=_SUMERIAN_GROUPS,
)


# ── Profile registry ──────────────────────────────────────────────────

ALL_PROFILES: dict[str, KandlesProfile] = {
    "default":   PROFILE_DEFAULT,
    "greek":     PROFILE_DEFAULT,   # alias
    "mycenaean": PROFILE_DEFAULT,   # alias
    "luwian":    PROFILE_LUWIAN,
    "anatolian": PROFILE_LUWIAN,    # alias
    "hurrian":   PROFILE_HURRIAN,
    "semitic":   PROFILE_SEMITIC,
    "dravidian": PROFILE_DRAVIDIAN,
    "sumerian":  PROFILE_SUMERIAN,
}

PROFILE_NAMES = list(ALL_PROFILES.keys())

# Auto-mapping from hypothesis language IDs to profiles
LANGUAGE_TO_PROFILE: dict[str, str] = {
    # exact hypothesis IDs
    "greek":           "default",
    "mycenaean-greek": "default",
    "mycenaean":       "default",
    "luwian":          "luwian",
    "luwian-anatolian":"luwian",
    "anatolian":       "luwian",
    "hurrian":         "hurrian",
    "semitic":         "semitic",
    "proto-semitic":   "semitic",
    "dravidian":       "dravidian",
    "proto-dravidian": "dravidian",
    "sumerian":        "sumerian",
    # fallback
    "default":         "default",
}


def get_profile(name: str) -> KandlesProfile:
    """Retrieve a Kandles profile by name or language ID.

    Args:
        name: Profile name (e.g. 'luwian', 'semitic') or language ID
              (e.g. 'proto-dravidian', 'mycenaean-greek').

    Returns:
        KandlesProfile for the requested language.

    Raises:
        ValueError: If the profile name is not recognised.
    """
    key = name.lower().strip()

    # Direct lookup
    if key in ALL_PROFILES:
        return ALL_PROFILES[key]

    # Language ID lookup
    if key in LANGUAGE_TO_PROFILE:
        return ALL_PROFILES[LANGUAGE_TO_PROFILE[key]]

    raise ValueError(
        f"Unknown Kandles profile: {name!r}. "
        f"Available: {sorted(ALL_PROFILES)}"
    )


def describe_profiles() -> list[dict[str, str]]:
    """Return a description of all available profiles for reporting."""
    seen: set[str] = set()
    result = []
    for name, profile in ALL_PROFILES.items():
        if profile.name not in seen:
            seen.add(profile.name)
            result.append({
                "name": profile.name,
                "description": profile.description,
                "aliases": [k for k, p in ALL_PROFILES.items() if p.name == profile.name],
            })
    return result


def profile_diff(
    profile_a: KandlesProfile,
    profile_b: KandlesProfile,
) -> list[dict[str, str]]:
    """Return phonemes that are assigned to different groups in the two profiles.

    Useful for understanding exactly what changes between e.g. Greek and Luwian.
    """
    diffs = []
    all_letters = set(profile_a.letter_to_group) | set(profile_b.letter_to_group)
    for letter in sorted(all_letters):
        ga = profile_a.letter_to_group.get(letter, -1)
        gb = profile_b.letter_to_group.get(letter, -1)
        if ga != gb:
            color_a = profile_a.groups.get(ga, {}).get("color", "Unassigned")
            color_b = profile_b.groups.get(gb, {}).get("color", "Unassigned")
            diffs.append({
                "phoneme":       letter,
                f"{profile_a.name}_group": str(ga),
                f"{profile_a.name}_color": color_a,
                f"{profile_b.name}_group": str(gb),
                f"{profile_b.name}_color": color_b,
            })
    return diffs
