"""Vedic Sanskrit language data for Indus script decipherment.

Sources:
  - Monier-Williams Sanskrit Dictionary
  - Rigveda word frequency analysis
  - Mayrhofer: Etymologisches Worterbuch des Altindoarischen

This provides the competing hypothesis: if the Indus script
encodes an Indo-Aryan (Vedic) language, these are the roots
and patterns we'd expect to find.
"""

from __future__ import annotations

VOCABULARY: dict[str, str] = {
    # Gods / religion
    "deva": "god / divine",
    "agni": "fire / fire god",
    "indra": "Indra (storm god)",
    "soma": "soma (ritual drink / moon)",
    "varuna": "Varuna (sky/water god)",
    "mitra": "Mitra (contract/friend)",
    "surya": "sun / sun god",
    "usas": "dawn",
    "vayu": "wind",
    "dyaus": "sky / heaven",
    "prthivi": "earth",
    "rta": "cosmic order / truth",
    "yajna": "sacrifice / ritual",
    "veda": "knowledge / sacred text",
    "rsi": "seer / sage",
    "brahman": "prayer / sacred power",
    "hotr": "priest / invoker",
    # Animals
    "go": "cow / cattle",
    "asva": "horse",
    "vrsa": "bull",
    "aja": "goat",
    "avi": "sheep",
    "svan": "dog",
    "gaja": "elephant",
    "simha": "lion",
    "vyaghra": "tiger",
    "sarpa": "snake / serpent",
    "matsya": "fish",
    "paksin": "bird",
    "garuda": "eagle",
    "hansa": "goose / swan",
    # Nature
    "ap": "water",
    "agni": "fire",
    "vayu": "wind / air",
    "bhumi": "earth / ground",
    "akasa": "sky / space",
    "surya": "sun",
    "candra": "moon",
    "naksatra": "star",
    "megha": "cloud",
    "vrsti": "rain",
    "nadi": "river",
    "samudra": "ocean / sea",
    "giri": "mountain",
    "vana": "forest",
    "vrksa": "tree",
    "puspa": "flower",
    # Social
    "raja": "king",
    "pura": "city / fort",
    "grama": "village",
    "grha": "house",
    "pati": "lord / husband",
    "bharya": "wife",
    "putra": "son",
    "duhitr": "daughter",
    "pitr": "father",
    "matr": "mother",
    "jana": "person / people",
    "visa": "clan / settlement",
    "kula": "family / lineage",
    "dasa": "servant / slave",
    "arya": "noble / master",
    "vaisya": "commoner / trader",
    # Trade / materials
    "hiranya": "gold",
    "rajata": "silver",
    "ayas": "metal / copper / iron",
    "mani": "jewel / gem",
    "vastra": "cloth / garment",
    "anna": "food / grain",
    "yava": "barley",
    "dhanya": "grain / wealth",
    "ghee": "clarified butter",
    "madhu": "honey / mead",
    "lavana": "salt",
    "ratha": "chariot",
    # Numerals
    "eka": "one",
    "dvi": "two",
    "tri": "three",
    "catur": "four",
    "panca": "five",
    "sas": "six",
    "sapta": "seven",
    "asta": "eight",
    "nava": "nine",
    "dasa": "ten",
    "satam": "hundred",
    "sahasra": "thousand",
    # Body
    "siras": "head",
    "mukha": "face / mouth",
    "aksi": "eye",
    "karna": "ear",
    "nasa": "nose",
    "hasta": "hand",
    "pada": "foot",
    "hrdaya": "heart",
    "udara": "belly",
    # Basic verbs
    "as": "be / exist",
    "bhu": "become",
    "gam": "go",
    "i": "go / move",
    "da": "give",
    "dha": "place / put",
    "kr": "do / make",
    "vac": "speak / say",
    "vid": "know",
    "drs": "see",
    "sru": "hear",
    "ad": "eat",
    "pa": "drink",
    "stha": "stand",
    "sad": "sit",
    "si": "lie down",
    "jan": "be born",
    "mr": "die",
    "yuj": "yoke / join",
    "budh": "wake / know",
    # Adjectives
    "maha": "great / big",
    "laghu": "light / small",
    "dirgha": "long",
    "hrasva": "short",
    "nava": "new",
    "pura": "old / ancient",
    "sundara": "beautiful",
    "subha": "auspicious",
    "sat": "true / good",
    "asat": "untrue / bad",
    "bala": "strong",
    "durga": "difficult / fortress",
}

# Rigveda opening hymns (character-level text for model building)
RIGVEDA_TEXT = (
    "agnim ile purohitam yajnasya devam ritvijam hotaram ratnadhaatamam "
    "agnih purvebhir rishibhir idyo nutanair uta sa devaan eha vakshati "
    "agninaa rayim ashnavat posham eva dive dive yashasam viravattamam "
    "agne yam yajnam adhvaram vishvatah paribhuurasi sa id deveshu gacchati "
    "agnir hota kavikratuh satyash chitrasravastamah devo devebhir aa gamat "
    "yad angha daashushe tvam agne bhadram karishyasi tavet tat satyam angirah "
    "upa tvaa agne dive dive doshaavastur dhiyaa vayam namo bharanta emasi "
    "raajantam adhvaraanaam gopaam ritasya diidivim vardhamaanam sve dame "
    "sa nah piteva suunave agne suupaayano bhava sachasvaa nah svastaye "
    "vaayav aa yaahi darshateme somaa aranakritaah teshaam paahi shrudhi havam "
    "vaayo tava praprinchantii dheno girbhis tvam acchhaa jigaati "
    "indravaayu ime sutaa upa prayobhir aa gatam indavo vaam ushastishah "
    "vaayav indash cha chetthah sutaanaam vaajiniivasuu taavaa yaatam "
    "indram agne sominah iishe tvaam indrasya karmabhih iishe tvaam "
    "iishe yajnasya raadhaso vivikvaaan aapriyeshaam iishe hi pitvo atitheh "
    "indram ange hotaarim sat sajoshaa devam deveshu yajniye na agnim "
    "raayantu praachii sarasvati mahaa dakshaa mahaa dhiyaa devii devavitaye "
    "indra mitra varuna agni aahur atha divyo sa suparno garutmaan "
    "ekam sat vipra bahudhaa vadanti agnim yamam maatarishvaanam aahuh "
    "somo raajaa varuna mahaa indra vishnu vaayur rudra shiva "
    "aham brahmaasmi tat tvam asi sarvam khalv idam brahma "
    "satyam jnaanam anantam brahma aanando brahma "
    "om tat sat om shanti shanti shanti "
    "vishvam daivam vasu saantam shivam advaita caturtham "
    "prajnanam brahma ayam aatmaa brahma aham brahmaasmi "
    "neti neti iti brahmanam adhigacchati "
    "brahmaiva idam vishvam aatmaa karma jnaana bhakti "
    "sarva dharman parityajya maam ekam sharanam vraja "
    "aham sarvasya prabhavo mattah sarvam pravartate "
    "maanasa vaaca karmana samskaara dharma artha kama moksha "
    "sukha dukha janma mrityu samsaara nirvana "
    "guru deva mata pita vishnu brahma maheshvara "
    "satya ahimsa brahmacharya asteya aparigraha "
    "samaadhi dhyaana dharana pratyaahara pranayama "
    "asana niyama yama ashta anga yoga sutra "
    "mantra stotra vedanta upanishad aranyaka brahmana "
    "rishi muni tapas vrata yagna homa puja "
    "graha nakshatra rashi jyotisha veda vastu "
    "shiva shakti brahma vishnu ganesha skanda "
    "sarasvati lakshmi parvati durga kali "
    "rama krishna arjuna yudhishthira bhima "
    "dharma adharma satya asatya viveka vairagya "
    "mukti moksha nirvana kaivalya liberation "
    "karma jnaana bhakti maarga path yoga "
    "shraddha shanti sattva rajas tamas guna "
    "praana apana vyana udaana samana "
    "nadi chakra kundalini sushumna ida pingala "
    "ajna vishuddha anahata manipura svadhisthana muladhara "
    "vishva taijasa prajna turiya consciousness "
    "sthula sukshma karana sharira body three "
    "jagrat svapna sushupti turiya state awareness "
    "maaya avidya ignorance knowledge liberation "
    "samskaara vasana prarabdha agami sanchita karma "
    "vivartavada ajativada brahman nirguna saguna "
    "adhyatma adhidaiva adhibhuta three aspects "
    "atman paramatman jivatman supreme individual "
    "shad darshana nyaya vaisheshika sankhya yoga "
    "mimamsa vedanta six systems philosophy "
    "agama tantra mantra yantra puja ritual "
    "shri rama jaya rama jaya jaya rama "
    "hare krishna hare rama mahamantra "
    "om namah shivaya panchakshara mantra "
    "gayatri savitri mantra surya sun verse "
    "namo narayanaya vishnu thousand names "
    "brahman vishnu mahesha trimurti creation "
    "shristi sthiti laya creation maintenance dissolution "
    "prakriti purusha samkhya duality non duality "
    "satcitananda being consciousness bliss brahman "
    "vedic aryan tradition culture civilization "
    "soma yagna fire sacrifice ritual ancient "
    "surya moon stars planets cosmic order "
    "rta dharma moral cosmic order truth "
    "ahimsa satya compassion truth virtue "
    "shanti peace harmony happiness moksha "
    "bhakti devotion jnana wisdom karma action "
    "yoga union meditation practice path "
    "advaita non duality brahman atman same "
    "brahmananda joy bliss supreme consciousness "
    "satyam shivam sundaram truth auspicious beauty "
)

MORPHOLOGY = {
    "type": "fusional",
    "word_order": "SOV (flexible)",
    "case_suffixes": {
        "nominative": ["s", "m", "h"],
        "accusative": ["m", "am"],
        "instrumental": ["aa", "ena", "bhis"],
        "dative": ["e", "aaya", "bhyas"],
        "ablative": ["at", "bhyas"],
        "genitive": ["sya", "aam"],
        "locative": ["i", "su"],
        "vocative": ["", "s"],
    },
    "verb_suffixes": {
        "present_1sg": "mi",
        "present_2sg": "si",
        "present_3sg": "ti",
        "present_1pl": "mas",
        "present_3pl": "nti",
        "past_3sg": "t",
        "imperative_2sg": "",
    },
}


def get_vocabulary() -> dict[str, str]:
    return dict(VOCABULARY)


def get_corpus_text() -> str:
    return RIGVEDA_TEXT


def get_corpus_symbols() -> list[str]:
    return [c for c in RIGVEDA_TEXT.lower() if c.isalpha()]


def get_morphology() -> dict:
    return dict(MORPHOLOGY)
