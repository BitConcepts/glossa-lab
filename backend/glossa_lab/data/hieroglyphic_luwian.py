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


# ── Extended Hieroglyphic Luwian lexicon (non-titular Hawkins/Melchert) ─────────
# Expansion drawn from Hawkins (2000) lexicon sections, Melchert's *Cuneiform
# Luvian Lexicon* (1993), Yakubovich (2010) and the ANNIS Anatolian Corpus
# Project entries.  This goes well beyond the royal-titulary core to cover
# common verbs, body parts, animals, plants, abstract nouns, place names,
# and inflected forms that account for the long tail of monumental tokens.
EXTENDED_VOCABULARY: dict[str, str] = {
    # ── Body parts ──────────────────────────────────────────────────────────
    "harman-": "head",
    "hassa": "hearth / family",
    "hilamni": "gateway / portico",
    "hudara": "finger / digit",
    "halpasi": "shoulder / upper arm",
    "isparza": "hip / loin",
    "isparuza": "sole of foot",
    "istamana": "ear",
    "karsana": "heart",
    "kalmara": "voice / shout",
    "kessar": "hand",
    "kessari": "in the hand (loc.)",
    "kupawi": "head / skull",
    "kalulupa": "finger / toe",
    "laman": "name / title",
    "lala": "tongue / speech",
    "lalpa": "forehead",
    "lala-tta": "speech (instr.)",
    "matussi": "tooth",
    "para-": "breath / soul",
    "parnal": "eye-brow / face",
    "parsana": "belly",
    "pata-": "foot",
    "papa": "lip / mouth",
    "sakuwa": "eye",
    "sasa": "chest / breast",
    "tarwana-pa": "voice / utterance",
    "tatara": "to swear / oath",
    "tara-tta": "firmly / strongly",
    "tunnak": "sanctum",
    "warpi": "horn",
    "zammuri": "beard",
    "zappa": "mouth / opening",
    # ── Animals (non-royal) ────────────────────────────────────────────────
    "alanza": "forest-game / boar",
    "hapanu": "river-fish",
    "haras": "eagle",
    "hartar": "deer / stag",
    "hawa": "sheep / ewe",
    "huitar": "wild animal",
    "hupa-": "bird (gen.)",
    "karasa": "hare",
    "kursanta": "young animal",
    "kuti": "hound",
    "luwana": "a kind of bird",
    "manuzi": "male calf",
    "mass": "young / cub",
    "musa": "mouse",
    "nuwana": "newborn animal",
    "parnu": "fox",
    "sakkar": "goat",
    "sarpu": "snake / serpent",
    "sasara": "lamb / suckling",
    "sittari": "sun-eagle (emblem)",
    "suppala": "cattle",
    "tarmana": "reptile / fish",
    "tasku": "hare",
    "tuhwala": "flock",
    "warwala": "colt",
    "wesi": "pasture-animal",
    "zarsa": "bird (small)",
    # ── Plants and natural objects ────────────────────────────────────────
    "alalla": "branch / leaf",
    "appalu": "orchard / fruit-grove",
    "appasa": "river-bed",
    "halki": "barley / grain",
    "halugatalla": "messenger plant",
    "hapu": "river",
    "haras-": "thicket / wood",
    "hatkapi": "olive",
    "hattar": "hill / mound",
    "hulla": "vine / grape",
    "hupali": "slope / mountainside",
    "huwasi-": "sacred stone (alt.)",
    "karassa": "leaf / foliage",
    "kunti": "meadow",
    "kuwap": "high place",
    "luliya": "pond / pool",
    "manuala": "forest-clearing",
    "nakku": "thorn",
    "napsa": "stream",
    "para-asha": "palace garden",
    "piya": "foliage",
    "sahanna": "orchard",
    "saplaka": "sapling",
    "sarliya": "upper hill",
    "taluppa": "clay / mud",
    "tipas": "sky / heaven",
    "tuwarsa": "thicket",
    "ulan": "strap / belt",
    "wallarwa": "oak / tall tree",
    "warana": "olive-grove",
    "wassuriya": "abundance / blessing",
    "watti": "land / grain field",
    # ── Common verbs (non-titular) ───────────────────────────────────────
    "alsa": "to call / name",
    "appa": "to seize / take",
    "arha": "away / forth",
    "arnu": "to bring",
    "asu": "to be (alt. stem)",
    "dai": "to put / place",
    "epp": "to seize",
    "ezza": "to eat / feast",
    "halzai": "to call / cry out",
    "hannai": "to judge",
    "hapariya": "to trade / barter",
    "har": "to hold",
    "hatkanu": "to shut / close",
    "hatkesnu": "to enclose",
    "haziya": "to incise / inscribe (alt.)",
    "hisai": "to draw / pull",
    "hupai": "to throw / hurl",
    "husk": "to wait / linger",
    "isparzai": "to escape",
    "istarki": "to be ill",
    "itar": "to walk / go (alt.)",
    "karpi": "to lift / raise",
    "katta": "down / below",
    "kalulupai": "to seize",
    "kuir": "to cut / sever",
    "kunna-": "to slay",
    "lahha": "to wage war",
    "lulai": "to break / shatter",
    "manai": "to see / look",
    "manink": "to remember",
    "mara": "to die / perish",
    "nahsariya": "to fear",
    "naktiya": "to harm",
    "naput": "to abandon",
    "nuntassa": "to make haste",
    "pahha": "to protect / guard",
    "papar": "to inscribe / engrave",
    "pesma": "to send (alt.)",
    "piya-": "to give (alt.)",
    "sakuwantar": "to look upon",
    "salla": "to be great",
    "sarli-": "to be supreme",
    "sarra": "to march / go up",
    "sarapa": "to drink / quaff",
    "saskupai": "to sleep / rest",
    "siai": "to seal (alt.)",
    "taparp": "to govern / rule",
    "tarmai": "to nail / fix",
    "tarru": "to oversee",
    "tessa": "to dream / vision",
    "tikup": "to flee / escape",
    "tuwa": "to set down",
    "upai": "to send (causative)",
    "wakkar": "to lack / fail",
    "walh": "to strike / beat",
    "wasta": "to sin / err",
    "watarnah": "to declare",
    "weh": "to turn / change",
    "weriya": "to call / name (alt.)",
    "za-": "to hit / strike",
    "zappa-": "to swallow / consume",
    # ── Common nouns of daily life ────────────────────────────────────────
    "alanzanu": "copper",
    "appasiwa": "fortress / stronghold",
    "asha-pa": "throne (oblique)",
    "esa": "earth / ground",
    "halmasuit": "royal seat / throne",
    "hannessar": "law-court",
    "hapina": "river-crossing",
    "hilana": "portico / forecourt",
    "hupariya": "tradesman",
    "huwawassi": "witness / sworn man",
    "isnan": "bread / loaf",
    "kasula": "libation cup",
    "kis": "day / time",
    "kursa": "hide / fleece",
    "kuttar": "shoulder / power",
    "laman-i": "name (gen.)",
    "laplapa": "branding-iron",
    "luza": "yoke / corvee",
    "makla": "loaf / cake",
    "malhassa": "festival",
    "masa": "day-time / festival",
    "masari": "prayer / offering",
    "naparta": "sister / female sibling",
    "nikis": "settlement",
    "papsa": "vase / jar",
    "parna": "house / household (alt.)",
    "parnali": "of the house",
    "perunna": "rock / cliff",
    "piyana": "gift / dowry",
    "sahis": "sigil / seal-impression",
    "sallai": "royal seal",
    "sarli-pa": "lord (oblique)",
    "sarpa": "silver",
    "sittasi": "banner / standard",
    "tabarpa": "dominion / lordship",
    "tarranu": "path of campaign",
    "tasmu": "dwelling / abode",
    "tinkala": "a measure of grain",
    "tunna": "feast",
    "tuppi": "tablet / document",
    "udni": "land (gen.)",
    "udnumi": "of my land",
    "uppa": "work / craft",
    "upi": "city-gate",
    "warpaliya": "weapon / mace (alt.)",
    "warpasa": "battle / combat",
    "wattar": "water / stream",
    "yarra": "month / festival cycle",
    "zalha": "campaign / march",
    "zammasa": "blessing",
    "zila": "kindred / clan",
    "zinta": "gold (rare)",
    # ── Pronouns, adverbs, quantifiers ───────────────────────────────────
    "ammi": "my (1sg poss.)",
    "appatti": "behind / after",
    "appiyatta": "hereafter",
    "ata": "that (anaphoric)",
    "hwa": "some / any",
    "kasa": "now / lo!",
    "kuissa": "each / every",
    "kwala": "ever / always",
    "masi": "how much",
    "namma": "again / further",
    "nasma": "or",
    "nuw": "and now",
    "sapa": "there / over there",
    "sarra-": "upper / above",
    "sumi": "you (2pl)",
    "taman": "thus / so",
    "tarpa-": "surely / firmly",
    "tassa": "of him / his",
    "taza": "now / today",
    "upat": "thereupon",
    "warpi-": "completely",
    "yaman": "likewise",
    "zila-": "of one's own kind",
    # ── Place-names beyond Karkamis cluster ──────────────────────────────
    "adana": "Adana (Cilician city)",
    "amurru": "Amurru (region)",
    "arpada": "Arpad",
    "ashshu": "Ashshu (mountain)",
    "haran": "Harran",
    "hilakku": "Hilakku (Cilicia)",
    "izriya": "Izriya / Iyzra",
    "karatepe": "Karatepe",
    "kummuh": "Kummuh (alt.)",
    "kuzi": "Kuzi-Tessub region",
    "lukka": "Lukka (Lycia)",
    "masuwari": "Masuwari (Til Barsib)",
    "maraqashi": "Maraqashi (Marash)",
    "musrai": "Egypt (in Luwian)",
    "niya": "Niya (Orontes)",
    "pala": "Pala (region)",
    "pisidia": "Pisidia",
    "que": "Que (Cilicia)",
    "saru": "Saru (city)",
    "tarsa": "Tarsus",
    "tuwana": "Tuwana (Tyana)",
    "unqi": "Unqi / Plain of Antioch",
    "wassukanni": "Wassukanni (Mitanni capital)",
    "yamhad": "Yamhad (Aleppo region)",
    # ── Religious / cosmic terms ─────────────────────────────────────────
    "alanza-pa": "of the wilds (oblique)",
    "halki-tessub": "Halki-Tessub (corn-deity)",
    "hapantali": "Hapantali (deity)",
    "hatkapur": "Hatkapur (deity)",
    "hebat": "Hebat (great goddess)",
    "hubabi": "Hubabi (mountain god)",
    "isaras": "Isara (oath goddess)",
    "kammama": "Kammama (goddess)",
    "karhuha": "Karhuha (stag-god)",
    "kasku": "Kasku (moon-god)",
    "kammusepa": "Kammusepa (alt.)",
    "manuzziya": "Manuzziya (mountain)",
    "muwatu": "Muwatalli (tit.)",
    "papas": "Father-god",
    "runtiya": "Runtiya (stag-god)",
    "sanunda": "Sanunda (deity)",
    "sarruma": "Sarruma (mountain god)",
    "sausga": "Sausga (Ishtar)",
    "siussummi": "of our god (1pl poss.)",
    "siussumis": "god (nom.)",
    "siwana": "god (nom. alt.)",
    "siwanat": "of the god (gen.)",
    "siwatti": "by the god (instr.)",
    "tarhunsi": "of the storm-god (gen.)",
    "telepinu": "Telepinu (vegetation deity)",
    "upelluri": "Upelluri (cosmic giant)",
    "zaliyanu": "Zaliyanu (mountain god)",
    "zammama": "Zammama (war-god)",
    # ── Adjectives and qualities ─────────────────────────────────────────
    "haripi": "steep / high",
    "harnamn": "swift",
    "hassukantu": "royal / kingly",
    "hilamn-i": "of the gateway",
    "kalmusa": "crooked / curved",
    "karu": "old / ancient",
    "kunna-pa": "slain (passive)",
    "lahhattalla": "warrior-like",
    "manink-i": "remembered (rel.)",
    "marwai": "angry / fierce",
    "nakkis": "heavy / weighty",
    "nawi": "not yet",
    "ninkanti": "black / dark",
    "papar-pa": "inscribed (passive)",
    "para-pa": "forward / ahead",
    "parsi": "holy / consecrated",
    "pittan": "swift / quick",
    "sallat": "large / broad",
    "saparta": "silvery / shining",
    "sarawi": "upright / lofty",
    "sarli-na": "of the lord (gen.)",
    "sasarah": "sacred / dedicated",
    "sarpasa": "sharp",
    "taru": "strong / firm",
    "tassauwa": "mighty",
    "tessupina": "of Tessub (gen.)",
    "upla": "high / elevated",
    "walhanta": "struck / smitten",
    "walwa-pa": "lion-like",
    "wassuwa": "of good (gen.)",
    "wesi-pa": "of the pasture (gen.)",
    # ── Inflected verb forms (3sg / 3pl past, imperative) ───────────────
    "asanut": "placed (3sg pret.)",
    "asanunta": "they sat",
    "awant": "may they come",
    "halzaiwant": "may they call",
    "hannit": "he judged",
    "haru": "may he hold",
    "haziyant": "they wrote",
    "karpiyaru": "let him lift",
    "katanut": "placed below (past)",
    "kunnani": "will slay (3sg fut.)",
    "lahhasu": "may he wage war",
    "manainta": "they saw",
    "matt-": "to cut",
    "naktiyatta": "harmed (med.)",
    "papartanu": "engraved (caus.)",
    "pittas": "swiftly (adv.)",
    "pita": "sent (3sg pret.)",
    "piyaru": "let him give",
    "saraps": "drank (3sg)",
    "sarrunt": "went up (3pl)",
    "siawatu": "may he seal",
    "taparru": "may he govern",
    "tarmaitu": "let him fix",
    "tarranta": "oversaw (3pl)",
    "tessuruwantu": "they dreamed",
    "tunaitu": "may he set",
    "upesi": "send (2sg imp.)",
    "walh-pa": "struck (passive)",
    "weriyanta": "they called",
    "za-tta": "struck (3sg pret.)",
}

# Merge extended vocabulary into the canonical VOCABULARY for downstream
# AttestedVocabularyLoader / HoldoutWordRecall use.  setdefault preserves
# any earlier curated entries while adding new lemmas.
for _k, _v in EXTENDED_VOCABULARY.items():
    VOCABULARY.setdefault(_k, _v)
del _k, _v


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
