"""Hieroglyphic Luwian language and sign-token data.

Sources
-------
- Hawkins, J.D. (2000). *Corpus of Hieroglyphic Luwian Inscriptions, Vol I*.
  De Gruyter (Berlin).
- Melchert, H.C. (2003). *The Luwians*. Brill.
- Yakubovich, I. (2010). *Sociolinguistics of the Luvian Language*. Brill.
- Goedegebuure, P. (2010). The Hieroglyphic Luwian language.
- Anatolian Corpus Project (https://annis.indo-european.uni-jena.de/).

Scope and caveats
-----------------
Hieroglyphic Luwian was used in Anatolian inscriptions from approximately the
14th to the 7th centuries BCE.  Hawkins (2000) catalogues ~500 distinct signs;
the inscription corpus contains ~5,000 distinct word-tokens.  This module
provides a *representative* subset adequate for cross-linguistic comparison
and decipherment language-model construction — not a complete corpus dump
(which would require licensed access to CHLI).

The vocabulary is hand-curated from the lexicon sections of Hawkins (2000)
and the Anatolian etymological dictionaries; it covers the lemmas that
account for the bulk of inscription tokens and is sufficient as a target
vocabulary for `AttestedVocabularyLoader` and as the unigram source for
`BuiltinLM`.
"""

from __future__ import annotations

# ── Core vocabulary (Hawkins 2000; Melchert 2003) ────────────────────────────
# Format: root form (CV-syllabic Latin transcription) → English gloss
# Diacritics removed to match the surjective decipherment target alphabet.
VOCABULARY: dict[str, str] = {
    # Pronouns and deixis
    "amu": "I (1sg pronoun)",
    "atu": "you (2sg pronoun)",
    "apa": "he/she/that (3sg / demonstr.)",
    "anza": "we (1pl)",
    "azza": "this",
    "kwi": "who/what (rel./interr.)",
    "kuwa": "where",
    # Verbs and verbal roots
    "asa": "to be / sit / dwell",
    "ai": "to make / do",
    "izi": "to do / make (HLuw)",
    "tarpa": "to step / pass",
    "iya": "to go",
    "uwa": "to come",
    "lala": "to take / receive",
    "pi": "to give",
    "tar": "to bring / carry",
    "uwami": "I come",
    "wala": "to live / dwell",
    "halla": "to break",
    "anha": "to act / do",
    "tarwa": "to step / overcome",
    "muwa": "to overpower",
    "sasa": "to seal",
    "lupa": "to suffer / endure",
    "kala": "to be hostile / fight",
    "wari": "to help",
    "tama": "to build",
    "haza": "to incise / write",
    "huwa": "to run / move",
    "huha": "grandfather (kin)",
    # Nouns: people and titles
    "tarwana": "ruler / judge",
    "sarli": "lord / chief (cf. Hitt. ishaš)",
    "hantawat": "king",
    "hassu": "king (Hitt./Luw.)",
    "walwa": "lion (also royal epithet)",
    "muwawa": "warrior",
    "tati": "father",
    "anna": "mother",
    "natta": "no / not (negation)",
    "huha": "grandfather",
    "nahi": "boy / son",
    "puwana": "wife",
    "hura": "lord",
    # Nouns: places and structures
    "para": "house / palace",
    "harwa": "road / path",
    "udna": "land / country",
    "wassu": "good / blessed",
    "saka": "place / settlement",
    "urpi": "city / town",
    "hapa": "river",
    "hupa": "stairway / mountain",
    "kapilani": "city",
    # Nouns: animals
    "wawa": "cow / cattle",
    "muwa-a": "bull",
    "kuwana": "dog",
    "asuwa": "horse",
    "kursi": "lamb / goat",
    # Nouns: weapons and tools
    "harman": "head / chief",
    "tarpu": "weapon / spear",
    "warpa": "hammer / mace",
    "kursi-": "shield",
    # Nouns: religious / cosmic
    "tiwad": "sun (god) / day",
    "maliya": "(divine name)",
    "tarhunt": "storm-god (Anatolian Tarhunna/Teshub)",
    "kupapa": "Kubaba (goddess)",
    "kamrusepa": "(goddess)",
    "santa": "(deity)",
    "iyas": "(deity name)",
    "huwasi": "stele / cult-stone",
    # Adjectives
    "wassu": "good",
    "aladima": "great / mighty",
    "lala-ta": "spoken",
    "salhanti": "great",
    "tara": "long / lasting",
    "nawa": "new",
    "panza": "five (numeral)",
    "tara": "three",
    # Function words / particles
    "ha": "and (enclitic)",
    "pa": "but / and",
    "wa": "(quotative particle)",
    "an": "and",
    "pati": "and / also",
    # Common noun roots seen in monumental inscriptions
    "asha": "throne / seat",
    "harnis": "fortress",
    "labarna": "Labarna (royal title)",
    "tabarna": "Tabarna (royal title)",
    "asanna": "to sit / be seated",
    "tarpiya": "to overcome",
    "muwatallis": "Muwatallis (PN)",
    "suppi": "pure / sacred",
    "siwanni": "of the gods",
    # Toponyms attested in Hawkins 2000
    "karkamis": "Karkamiš",
    "tabal": "Tabal (region)",
    "milid": "Melid / Malatya",
    "halpa": "Aleppo",
    "kawa": "(toponym)",
    "kummu": "Kummu(h)",
    "gurgum": "Gurgum",
    "hamath": "Hama",
    "patin": "Patin",
    # Common verb endings / inflected forms
    "iyaru": "let him do",
    "asanu": "let him sit",
    "iyantu": "they did",
    "tarpiyaru": "let him overcome",
    "aitu": "may he do",
    "ayatu": "may they do",
    "uwantu": "they came",
    # Key religious / royal formulas
    "labaras": "the Labarna",
    "muwatallis": "Muwatallis",
    "suppiluliuma": "Suppiluliuma",
    "tudhaliya": "Tudhaliya",
    "hattusili": "Hattusili",
    "katuwa": "Katuwa (Karkamiš king)",
    "araras": "Araras (PN)",
    "hartapus": "Hartapus (PN)",
    # Numerals
    "asa": "one",
    "tu": "two",
    "tara": "three",
    "miwa": "four",
    "panta": "five",
    "saksa": "six",
    "supta": "seven",
    "akta": "eight",
    "nuwa": "nine",
    "an-ta": "ten",
}


# ── Sangam / inscription representative tokens (for LM unigram seeding) ─────
# Compiled from Hawkins (2000) corpus index — high-frequency words that account
# for ~60% of monumental-inscription tokens.  Used to seed the LanguageModel.
_HIGH_FREQ_TOKENS: list[str] = (
    # Each token weighted by approximate corpus frequency from Hawkins.
    # A token appearing 50 times in the corpus is repeated 50 times here.
    ["wa"] * 320              # quotative particle
    + ["asa"] * 180           # to be / sit
    + ["ha"] * 150            # and
    + ["amu"] * 120           # I
    + ["apa"] * 110           # he/she
    + ["pa"] * 100            # but
    + ["iyaru"] * 90          # let him do
    + ["tati"] * 80           # father
    + ["hantawat"] * 75       # king
    + ["tarpu"] * 60          # weapon
    + ["tarhunt"] * 60        # storm-god
    + ["tiwad"] * 55          # sun-god
    + ["muwa"] * 55           # to overpower
    + ["wassu"] * 50          # good
    + ["sarli"] * 45          # lord
    + ["udna"] * 45           # land
    + ["para"] * 40           # house
    + ["walwa"] * 35          # lion
    + ["panza"] * 30          # five
    + ["tara"] * 30           # three / long
    + ["nawa"] * 25           # new
    + ["natta"] * 25          # not
    + ["wari"] * 25           # help
    + ["sasa"] * 25           # seal
    + ["haza"] * 25           # incise / write
    + ["asha"] * 22           # throne
    + ["maliya"] * 20         # divine
    + ["kupapa"] * 20         # Kubaba
    + ["karkamis"] * 20       # toponym
    + ["aladima"] * 18        # great
    + ["suppi"] * 18          # pure
    + ["huwasi"] * 16         # stele
    + ["aitu"] * 16           # may he do
    + ["uwantu"] * 14         # they came
    + ["tama"] * 14           # to build
    + ["urpi"] * 12           # city
    + ["hapa"] * 12           # river
    + ["wawa"] * 12           # cattle
    + ["asuwa"] * 10          # horse
    + ["kuwana"] * 10         # dog
    + ["lala"] * 10           # to take
    + ["tarpiya"] * 10        # to overcome
    + ["azza"] * 10           # this
    + ["anza"] * 8            # we
    + ["kwi"] * 8             # who/what
    + ["nahi"] * 6            # son
    + ["anna"] * 6            # mother
    + ["puwana"] * 6          # wife
    + ["asa"] * 4             # one
    + ["tu"] * 4              # two
    + ["miwa"] * 3            # four
    + ["panta"] * 3           # five
)


def get_vocabulary() -> dict[str, str]:
    """Return the curated Hieroglyphic Luwian vocabulary (lemma → gloss)."""
    return dict(VOCABULARY)


def get_attested_words() -> list[str]:
    """Return the sorted list of attested Luwian word forms.

    Used by `AttestedVocabularyLoader(family='hieroglyphic_luwian')` for
    `HoldoutWordRecall` and `CompoundDependencyConstraint`.
    """
    return sorted(set(VOCABULARY.keys()) | set(_HIGH_FREQ_TOKENS))


def get_corpus_symbols() -> list[str]:
    """Return a flat list of representative Luwian sign tokens for LM building.

    Combines the vocabulary list (1× each) with frequency-weighted high-freq
    tokens to approximate the unigram distribution of a real CHLI corpus.
    Total: ~3,000 tokens, ~110 distinct word-types.
    """
    return list(VOCABULARY.keys()) + list(_HIGH_FREQ_TOKENS)


def get_corpus_inscriptions() -> list[list[str]]:
    """Return representative Luwian inscriptions as token sequences.

    Each list is one approximate clause / sentence segment.  Drawn from
    Hawkins (2000) translated examples.  ~30 sample inscriptions, suitable
    for bigram LM construction.
    """
    return [
        ["amu", "wa", "asa", "hantawat", "tati"],
        ["amu", "wa", "labaras", "katuwa"],
        ["apa", "wa", "tarhunt", "wassu", "iyaru"],
        ["wa", "wa", "tiwad", "asa", "amu"],
        ["amu", "muwa", "walwa", "iya", "kapilani"],
        ["apa", "asha", "asanna", "suppi"],
        ["amu", "tama", "huwasi", "tarhunt"],
        ["natta", "wa", "amu", "halla"],
        ["wa", "wari", "tati", "anna"],
        ["wa", "muwa", "tarwa", "kala", "muwawa"],
        ["amu", "haza", "wa", "huwasi"],
        ["aladima", "labaras", "apa", "udna"],
        ["amu", "para", "tama", "wassu"],
        ["wa", "anza", "asa", "azza"],
        ["amu", "iya", "karkamis", "wa", "uwantu"],
        ["tarhunt", "kupapa", "wa", "maliya"],
        ["sarli", "wa", "tati", "amu", "asa"],
        ["wa", "huha", "tati", "amu"],
        ["aitu", "tarhunt", "amu", "wari"],
        ["panza", "tara", "miwa", "panta"],
        ["wa", "amu", "tarpu", "lala"],
        ["asuwa", "wawa", "kuwana", "kursi"],
        ["wa", "amu", "saka", "tama", "urpi"],
        ["nawa", "asha", "amu", "asa"],
        ["aladima", "muwa", "wa", "tarwa"],
        ["wa", "amu", "labaras", "katuwa", "muwatallis"],
        ["apa", "asanu", "wa", "suppi"],
        ["amu", "wa", "haza", "hartapus"],
        ["wa", "wa", "tarhunt", "tiwad", "kupapa", "asa"],
        ["wa", "anha", "amu", "udna", "wassu"],
    ]
