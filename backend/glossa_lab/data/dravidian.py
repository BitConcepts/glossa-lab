"""Proto-Dravidian language data for Indus script decipherment.

Sources:
  - DEDR: Dravidian Etymological Dictionary Revised (Burrow & Emeneau)
  - Parpola (1994, 2005): "Deciphering the Indus Script"
  - Krishnamurti (2003): "The Dravidian Languages"
  - Sangam Tamil literature (character frequencies)

The vocabulary is organized by semantic field, reflecting domains
likely represented on Indus seals (animals, trade, religion, numerals).
"""

from __future__ import annotations

# ── Proto-Dravidian reconstructed vocabulary (from DEDR) ──────────
# Format: root → English gloss
# Roots are in simplified transliteration (no diacritics)

VOCABULARY: dict[str, str] = {
    # Animals (appear as iconography on seals)
    "min": "fish (rebus: star, celestial)",
    "pal": "tooth / many / milk",
    "kol": "bull / male animal",
    "eri": "buffalo",
    "yane": "elephant",
    "puli": "tiger / leopard",
    "nay": "dog",
    "kil": "parrot",
    "kak": "crow",
    "amp": "tortoise",
    "pan": "pig / wild boar",
    "kat": "wild cow",
    "mar": "deer / antelope",
    "kur": "horse (borrowed?)",
    "pamp": "snake / serpent",
    "mul": "hare",
    "ant": "goose",
    # Nature / landscape
    "kal": "stone / rock",
    "nil": "stand / blue / indigo",
    "man": "earth / sand / soil",
    "ner": "water / wet",
    "tin": "fire / burning",
    "ven": "white / hot / sun",
    "kar": "black / dark / cloud",
    "cem": "red",
    "pac": "green / fresh",
    "mar": "tree / wood",
    "pul": "grass / low",
    "ten": "south / right",
    "vat": "north / left",
    "mel": "above / west",
    "kil": "below / east",
    "aru": "river / stream",
    "kat": "sea / ocean",
    "kun": "hill / mound",
    "pal": "valley / hollow",
    "pur": "outside / city",
    "ak": "inside",
    "nal": "good / auspicious",
    "tiy": "bad / evil",
    # Body parts
    "kan": "eye",
    "cevi": "ear",
    "muk": "face / nose",
    "vay": "mouth",
    "tal": "head",
    "kay": "hand / arm",
    "kal": "foot / leg",
    "ner": "chest / heart",
    "muti": "back",
    "viral": "finger",
    # Social / trade
    "ko": "king / chief",
    "vel": "priest / white / spear",
    "pan": "worker / make",
    "van": "smith / strong",
    "val": "ruler / power",
    "an": "male / man",
    "pen": "female / woman",
    "il": "house / home",
    "ur": "village / town",
    "pur": "city / fort",
    "kut": "clan / family",
    "pey": "spirit / demon",
    "kat": "protection / refuge",
    "tol": "ancient / old",
    "put": "new / fresh",
    "per": "big / great",
    "cir": "small / little",
    # Religion / ritual (relevant to seal content)
    "ven": "worship / white",
    "kol": "sacrifice / kill",
    "tat": "father / god",
    "amma": "mother / goddess",
    "mutu": "old / first / ancestor",
    "val": "strong / worship",
    "pal": "many / offering",
    "tin": "sacred fire",
    "ney": "ghee / oil (offering)",
    "koy": "temple / dig",
    # Numerals
    "onr": "one",
    "ir": "two",
    "mu": "three",
    "nal": "four",
    "aynt": "five",
    "aru": "six",
    "elu": "seven",
    "ettu": "eight",
    "onpatu": "nine",
    "pattu": "ten",
    "nuru": "hundred",
    "ayir": "thousand",
    # Basic verbs
    "va": "come",
    "po": "go",
    "tar": "give",
    "kol": "take / kill",
    "tin": "eat",
    "kut": "drink",
    "nil": "stand / stop",
    "iru": "sit / be / exist",
    "kit": "lie down",
    "cel": "go / proceed",
    "pal": "say / tell",
    "ket": "hear / ask",
    "kan": "see",
    "ar": "know",
    "cey": "do / make",
    "vey": "hunt / cook",
    "kal": "learn / steal",
    "pat": "sing / fall",
    "atu": "dance / play",
    "ney": "weave / spin",
    # Common grammatical suffixes (case markers)
    "am": "nominative / that",
    "ai": "accusative",
    "in": "genitive / of",
    "ku": "dative / to / for",
    "il": "locative / in / at",
    "otu": "instrumental / with",
    "atu": "ablative / from",
    # Adjectives / modifiers
    "nal": "good",
    "tiy": "bad",
    "per": "big",
    "cir": "small",
    "pul": "low / base",
    "uyar": "high / noble",
    "ton": "old / ancient",
    "put": "new",
    "val": "strong",
    "mel": "soft / gentle",
    "kur": "short",
    "net": "long / tall",
    # Materials / trade goods
    "pon": "gold",
    "vel": "silver (white metal)",
    "irump": "iron",
    "cem": "copper (red metal)",
    "man": "clay / pottery",
    "kal": "gem / stone",
    "mani": "bead / gem",
    "tuk": "cloth / garment",
    "nel": "rice / paddy",
    "tin": "grain / millet",
    "en": "sesame / oil seed",
    "up": "salt",
}

# ── Old Tamil character bigram frequencies ────────────────────────
# Approximate frequencies from Sangam literature analysis
# Used for building the character-level language model
OLD_TAMIL_TEXT = (
    "akara mutala ezuttellaam aati pakavan mutarre ulaku "
    "karra tanaal aaya payane ennkolo vaalarivan naattra taal "
    "malarmicai ekinaan maanati cerntar nilam micai neediaar "
    "venduthal vendaamai ilaanarai cerntar yanduthal yandaa "
    "irulcer iruvinaiyum ceraa irai panan porulcer pukaz "
    "porai utaiyaar pukaz utaiyaar matrai ellam niraiyutaimai "
    "niraiyenum nannootai neenta punal maraiya maanath "
    "anivalakum aaviar vaalkkai nunaivalakum nuulal pala "
    "enainaanal vaazhi ulliyum pirai enainaan nannattaatkku "
    "kol eruntaatu maatci irappini niraintanku kuruntar "
    "oppuravu ozhukam ulakattar kanneriyaam karperaam kuuti "
    "pirappokkum ella uyirkkum cirappovvaa ceyyolukam "
    "aravazhi yattraruul aavi anait tiralum piravaa neri "
    "anputaimai aana kuzaviyin munnarival tontrum "
    "utaimai itaiyuurantu vaalaapin mutumai "
    "uravottaar enpathu orotalai poriyil tanaiyaatci "
    "aamaiyin ontra punarci urpavar saalpar enpa mattra "
    "inpam virumpi aravil centraar inpamuutrar varuntuvaar "
    "arattan varuvaat inpamum untaaka pirattal ati ennaar "
    "anpum aranum utaittu aayen kuzavi munnankondra "
    "aaram tazuviya nenjamum enpotu irantum illaiyaal "
    "ceytannam allatu kolvaana tilla iruntannam allatu "
    "onraamal oruvanukku veru onru nalla kutimaiyum "
    "aranenum kunamum utal udaiyaarotu ceerntu vaalum "
    "vaiyattuul vaazvaanku vaazpavan vaanuraiyin "
    "ennaatum veenaal etirpatum pirattu porulkut "
    "anpilaar yellaam tamakku uriyar anpudaiyaar "
    "tiru attaar ennaar atimai pukku taruvaar "
    "porul allaar ennaar pudaiyal matrum "
    "irulum etirpatu onrilla iraikku "
)

# ── Dravidian morphology patterns ─────────────────────────────────
MORPHOLOGY = {
    "type": "agglutinative",
    "word_order": "SOV",
    "case_suffixes": {
        "nominative": ["am", "an", "al", "ar", "a"],
        "accusative": ["ai", "in"],
        "genitive": ["in", "atu", "utaiya"],
        "dative": ["ku", "ukku"],
        "locative": ["il", "itattu"],
        "instrumental": ["al", "otu", "kontu"],
        "ablative": ["iliruntu", "inru"],
    },
    "verb_suffixes": {
        "present": ["kinr", "kir"],
        "past": ["t", "nt", "in"],
        "future": ["v", "p"],
        "imperative": ["", "min", "ka"],
        "negative": ["a", "aat"],
    },
    "person_markers": {
        "1sg": "en",
        "2sg": "ay",
        "3sg_m": "an",
        "3sg_f": "al",
        "1pl": "om",
        "2pl": "ir",
        "3pl": "ar",
    },
}


def get_vocabulary() -> dict[str, str]:
    """Return the proto-Dravidian vocabulary."""
    return dict(VOCABULARY)


def get_corpus_text() -> str:
    """Return Old Tamil text for language model building."""
    return OLD_TAMIL_TEXT


def get_corpus_symbols() -> list[str]:
    """Return character-level symbol sequence from Old Tamil."""
    return [c for c in OLD_TAMIL_TEXT.lower() if c.isalpha()]


def get_morphology() -> dict:
    """Return Dravidian morphology patterns."""
    return dict(MORPHOLOGY)
