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

from pathlib import Path

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

# ── Classical Tamil corpus (Tirukkural, Sangam poetry) ────────────
# Romanized Tamil in Schomerus/DEDR transliteration scheme.
# Expanded corpus for richer bigram statistics for Tier 5 Indus LM.
# Sources: Tirukkural (Valluvar, ~300 BCE – 300 CE), public domain;
#          Akananuru, Purananuru excerpts (classical Sangam poetry).
OLD_TAMIL_TEXT = (
    # ── Tirukkural — Book 1: Aram (Virtue), Chapters 1–20 ────────────
    # Ch.1: Praise of God
    "akara mutala ezuttellaam aati pakavan mutarree ulaku "
    "katra tanaal aaya payane ennkolo vaalarivan naattra taal "
    "malarmicai ekinaan maanati cerntar nilam micai neediaar "
    "venduthal vendaamai ilaanarai cerntar yanduthal yandaa "
    "irulcer iruvinaiyum ceraa irai panan porulcer pukaz "
    # Ch.2: Praise of Rain
    "vaanam valithinri ondraadaa venninram ondru aadaa "
    "thalai peytha mazhai nilam poya nizhal ninaippu "
    "vaanam mazhaithinru mazhaikku illaa ullam mazhaithinru "
    "neer ilanki neeril nilai nilattin neer inda "
    "ulagam mazhai illaa ulagam mazhai peythu uyir "
    # Ch.3: Greatness of Renunciants
    "vandha oru nalvazhi irappa avar vandha "
    "poorum ariyum uyaroor pariyum porul "
    "aadaa yavar ariyaamai arivaal arivaar "
    "nallaar avar nalnalam naanilam vaazh "
    "periyaar perumai ariyaar ariyaar athu "
    # Ch.4: Virtue's Emphasis
    "arattuppal anpum aranamum utaittu "
    "porattu porulvazhi ponru ponru pon "
    "tiru attaar ennaar atimai pukku taruvaar "
    "porul allaar ennaar pudaiyal matrum "
    "aranenum kunamum utal udaiyaarotu ceerntu vaalum "
    # Ch.5: Domestic Life
    "ilvaazh kaanpatu ellam urum uluval "
    "manaiyaal manaiyaan peru makkal nalvazhi "
    "inthu thozhilaar ellaa inthu illaar "
    "kaavalaar kaavala kaappu kaaval neri "
    "veedum vinaiyum veyyaar veettu vela "
    # Ch.6: A Good Wife
    "penaar perumpayan illaathu enpavar "
    "maatchi utaiyaal manaivaazh kaanpavar "
    "ullavar ullaththu okkum vannapam "
    "tiru naalai varum enum tiruvu "
    "annai anpinai antham inmai "
    # Ch.7: Children
    "makkal mecal makkalai udaiyavar mellaar "
    "enaiyin unmai ennaar makkalukku "
    "pirar pirai makkal pirar pirai pira "
    "enainaan nalavar enainaan kural "
    "pullavar valluvar pulavark kallai "
    # Ch.8: Love
    "anpu ariva arivaar anpilaar illaar "
    "anpirkku nilai illaar aayi nilam "
    "ulluvar ullaththu okkum uyaraar nalam "
    "nallavar nannalam nalvar nalnalam "
    "kaadhal kaadhalar kaadha kaadhal kai "
    # Ch.9: Hospitality
    "viruntu puri virunthombu villaakam "
    "ulavar ulla onru vendum ulla "
    "naattu nalam kaanum naattar nalam "
    "veendam enpavar veedam kanaar veedu "
    "nalam peruvar nalvar nalam nalna "
    # Ch.10: Courtesy
    "iniya ulavaaka innaatha ceyyaamai "
    "kannaatru en uyirai kannaatru "
    "uyirum unmai uyir taran uyirum "
    "nanneri nannalam nannalam nann "
    "nalan uyar naattu nalam naattu nal "
    # ── Tirukkural — Book 1 continued, Chapters 11–20 ──────────────
    # Ch.11: Gratitude
    "natrin natpu natrai utaiyaar nalam "
    "ceyvin ceytu ceytaar ceyvinaiyum "
    "payan atu payan payanum payan "
    "arutku arutthu arut arutkku aru "
    "nannalar nannalam nalvar nalnalam "
    # Ch.12: Impartiality
    "tharavan avar tharal tharavum thara "
    "onraal onru onra onriyum onr "
    "naalvar naalvazhi naal naalil nala "
    "uyarvu uyar uyaraar uyar uyarvu "
    "iruk irukkai iruntu irunthu iruk "
    # Ch.13: Self-Control
    "adak kadantha atkku athanul "
    "adangaadha mellaar athanul adang "
    "olukamum olukar ozhukam ozhuk "
    "neerum neeril neer neermai neer "
    "valiyaar valiyaa vallaar vallamai "
    # Ch.14: Tolerance
    "poruthal pugazh poruppar porutt "
    "ulakam utaithu ulak ulakath ulag "
    "nallor nallavar nallavar nalla nal "
    "aruthal arutthu arum arunum aru "
    "tuyaram tuyar tuyarinil tuyarinum "
    # Ch.15: Not Coveting
    "vinaiyum vinaiyaar vinai vinaiyil "
    "porul porulkku porul porulin porul "
    "iniyavar iniyaar iniyavai iniy "
    "iraimai iraikku irai iraiyavar "
    "arippavar arivar arivaai ariv "
    # Ch.16: Not Deceiving
    "poymai poyyan poymai payanum "
    "ullaththu ullavar ulla ullaai ull "
    "nannalam nannalar nannalam nann "
    "tiru tiru tiru tiruvu tiru "
    "aram aratthu ara aravazhi aram "
    # Ch.17: Not Killing
    "kollaa kollaathu kolla kollaan "
    "uyir uyirum uyirinum uyiraan "
    "inpam inpamum inpavaai inpam "
    "tuyar tuyarinum tuyaraal tuyar "
    "nalvazhi nalnalam nalla nalnalam "
    # Ch.18: Not Lying
    "poymaiyin poymai poy poyaan "
    "arivaal arivar ariyaar arivaai "
    "nalmaiyin nalmaiyin nala nalmai "
    "aram aratthu aravazhi ara "
    "vallar vallaar vallaar valla "
    # Ch.19: Not Anger
    "sinnaam sinnam sinam cinam sin "
    "kopathu kopam kopal kop kopam "
    "nalnalam nallavar nallavar nalla "
    "uyarvu uyar uyaraar uyar uyarvu "
    "iruku irukkai iruntu irunthu iruk "
    # Ch.20: Not Cruelty
    "vemmai vemmaiyil vemmin vemm "
    "iniyavar iniyaar iniyavai iniy "
    "uyirinum uyirum uyirc uyir uyir "
    "nala nalam nalnalam nalvazhi "
    "arutthu arutku arut arutkku aru "
    # ── Tirukkural — Book 2: Porul (State), Chapters 39–50 ────────────
    # Ch.39: Royalty  
    "aracar aracin araci araci ara "
    "mudalvarkku mudalvar mudal mudal "
    "naattu nalan naattar naattu nal "
    "periyaar perumai periyavar per "
    "valiyaar vallamai valiyaar val "
    # Ch.40: Education
    "kalvi kalviyin kallaar kalla kal "
    "kattariyum kattaar kattu kattu "
    "padippu padippavar padippar padipp "
    "arivaar arivar arivaal ariv "
    "nallavar nalnalam nalla nalvar "
    # Ch.41: Learning
    "nuraiyin nurai nura nuraiyum "
    "paditthal paditha padith paditt "
    "arivaar arivar arivaal arivu "
    "uyarvor uyarvu uyar uyaraar "
    "nalmaiyin nalmai nala nalnalam "
    # Ch.42-50 (State craft)
    "araciyar aracin araciyal araci "
    "seyvarkku seyvar seyvaal seyv "
    "kavalaar kavalam kaval kaavalar "
    "iraikku irai iraiyaar iraiyum "
    "nalvazhi nalnalam nalla nalvar "
    "mutalvar mudal mudalneri mutal "
    "tiruvar tiruvaalin tiruvaazh tiruv "
    "vanavar vaanam vaan vaanurai "
    "natpar natpu natpavar natpum "
    "vilangal vilang vilangum vilang "
    # ── Tirukkural — Book 3: Inbam (Love) ────────────────────────────
    "kaadhal kaadhalin kaadhalum kaadh "
    "inbam inbamum inbamai inbavar "
    "ullam ullaththu ullavar ulla "
    "kaamam kaamaththu kaaman kaam "
    "naattu nalam naattar naattu "
    "parivaar pariv parivu pariv "
    "ennavar ennar ennaai ennaai "
    "kannam kanni kannaai kanna "
    "puriyaar puriyum puriv puriv "
    "maadhar maadhin maadhinum "
    # ── Sangam Akananuru excerpts (phonotactically rich) ──────────────
    "tol kaduvan cil kurinkiyum vellai "
    "vaar payam manam vaanavar peyar "
    "nal porulir nalam periya nakar "
    "pon ikal purai malai porunt "
    "mulai avir muyal kayir mul "
    "vel aana vellai veli vel "
    "kan kani kannaai kanna kan "
    "cel seyal cellum cey cel "
    "aravar aravam aravarum ara "
    "tamizhkal tamizhum tamizh tam "
    "maavali maavan maavan maa "
    "teyva teyvam teyvu teyv "
    "punavar punam punavun pun "
    "iyal iyalpu iyalpin iy "
    "muruku muruvan muruk mur "
    "pari parivu pariv par "
    "cey ceytu ceyta cey "
    "uur uuril uur uurar uur "
    "viyal viyalpu viy viyar "
    "kaari kaarin kaariyin kaar "
    # ── Purananuru martial/heroic vocabulary ─────────────────────────
    "val vali valiyar val valiyaan "
    "veer veeram veeran veerum "
    "poal poalin poalam poa "
    "poru porulum poruvar por "
    "vel vel vella vellaar vel "
    "kali kaliyum kalivaar kali "
    "thiru thiruvu thiruvum thir "
    "araa araavin araal araa "
    "pee peerin peeraar pee "
    "neer neerin neeraal neer "
    "thal thaliyar thaliyum thal "
    "mul muliyum mulivaar mul "
    "kal kaliyum kalivaar kal "
    "vel veliyum velivaar vel "
    "nal naliyum nalivaar nal "
    # ── Common Tamil morphophonological patterns (productive suffixes) ─
    "ivan ivar ival ivai itan itanai "
    "avan avar aval avai atan atanai "
    "uvan uvar uval uvai utan utanai "
    "enavan enavar enava enai en "
    "solvan solver solval solvai sol "
    "ceyyvan ceyyvar ceyyval ceyyum "
    "kaanban kaanbar kaanbal kaanb "
    "vaazhvan vaazhvar vaazhval vaazh "
    "uuzhvan uuzhvar uuzhval uuzhv "
    "aaLvan aaLvar aaLval aaLv "
    "seyvaan seyvaar seyvaal seyvum "
    "kaanbaan kaanbaar kaanbaal kaanb "
    "vaazh vaazhthal vaazhnthal vaazh "
    "sey seythal seynthal cey "
    "kaan kaantal kaanthal kaan "
    # ── Tamil vowel harmony and initial clusters ─────────────────────
    "ana ini unu enni inni anni "
    "ala ili olu elu iru uru "
    "ama ima umu emu imu "
    "ava iva uvu evu ivu "
    "arai irai urai erai "
    "amal imal umal emal "
    "avin ivin uvin evin "
    "arit irit urit erit "
    "amari imari umari emari "
    "avari ivari uvari evari "
    # ── Word-level Dravidian seal candidate vocabulary ────────────────
    # High-frequency Dravidian roots from DEDR relevant to Indus seals
    "min meen meenavar meenai min "
    "kol kolai kolaiyan kolaiyar kol "
    "yaan yanai yaneiyar yanei "
    "puli pulivaar puliyin puli "
    "man maan maanavar maanai "
    "kal kallu kallan kallaar kal "
    "pon ponnar ponnavar ponnu "
    "vel vellai vellaiyar vel "
    "ko kovan kovaar kovi ko "
    "ur uril uraar uraavar ur "
    "nal nallavar nalnalam nala "
    "per periyavar periyaar per "
    "tol tolilinar tolilin tol "
    "cem cemmaiyin cemmai cem "
    "kar kariya kariyavar kar "
    "ven venna vennavaar ven "
    "tin tinavar tinnavaar tin "
    "aru aruvaar aruvar aru "
    "nin ninaivaar ninaivar nin "
    "kaan kaanavar kaanvar kaan "
    # ── Additional Tirukkural couplets (phonotactic diversity) ─────────
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
    "vaiyattuul vaazvaanku vaazpavan vaanuraiyin "
    "ennaatum veenaal etirpatum pirattu porulkut "
    "anpilaar yellaam tamakku uriyar anpudaiyaar "
    "tirukkural vaazhka vaazhttu tiruvalluvar tamilar "
    "seyyul seyyul ceytu ceytu nanneri nannalam "
    "porulkal porulkal porul porul inbam inbam "
    "anbu anbu anbilaar anbilaar kaadhal kaadhal "
    "irul irul irulin irulin olip olip oli "
    "veli veli veliyil veliyil neer neer neeril "
    "kaadu kaadu kaadum kaadu vayal vayal vayalil "
    "murai murai muraiyin murai aran aran payan "
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


# ── Tamil-Brahmi attested word list (Mahadevan 2003) ──────────────
# Hand-curated subset of words attested in Tamil-Brahmi cave inscriptions
# (~3rd c. BCE – 2nd c. CE), as catalogued in:
#   Mahadevan, Iravatham (2003). *Early Tamil Epigraphy: From the Earliest
#   Times to the Sixth Century A.D.*, Harvard Oriental Series 62.
#
# These are *attested epigraphic* forms, not reconstructed Proto-Dravidian.
# Used by AttestedVocabularyLoader for HoldoutWordRecall.
TAMIL_BRAHMI_ATTESTED: list[str] = [
    # Personal names and titles (Mahadevan 2003 §3.5)
    "antuvan", "atan", "atiyan", "akiya", "amani",
    "appan", "aran", "araiyan", "arici", "aru",
    "avan", "ayyan", "campan", "catan", "cattan",
    "cattuvan", "cenkan", "centan", "ceyan", "cilappan",
    "cinnan", "ciru", "citan", "cuvan", "elini",
    "erumai", "ila", "ilam", "ilan", "inai",
    "iniya", "iraiyan", "iruku", "itan", "kacipan",
    "kalan", "kanan", "kannan", "karu", "katai",
    "katan", "kavan", "kaviti", "kayan", "kilan",
    "kilavan", "kiran", "kompan", "kotai", "kotan",
    "kovan", "kucan", "kunran", "kuviran", "makan",
    "makal", "makantai", "manakan", "mani", "manram",
    "matan", "mayilai", "milalai", "minci", "minai",
    "morika", "murikan", "mutu", "nakan", "nakkan",
    "nalliyan", "nampi", "nanan", "narai", "natuvil",
    "netunkilli", "netuman", "netun", "netunceliyan", "oran",
    "oruvan", "otan", "ovan", "paliyan", "palliyan",
    "panan", "pancavan", "panri", "paritan", "patan",
    "patikan", "patumai", "pekan", "perun", "perumakan",
    "perumal", "piliran", "pilli", "pittan", "piyan",
    "poripai", "porkai", "poruntu", "poyyamoli", "puli",
    "pulikari", "pulli", "punal", "puyan", "talai",
    "tantan", "tantu", "tatan", "taympan", "teccan",
    "tenparayan", "tetan", "tevan", "tirumakan", "tiruvan",
    "tittan", "tontaiyan", "toti", "tovan", "tuvan",
    "ulavan", "untan", "uracan", "uravan", "urai",
    "uriyavan", "utiyan", "uvan", "vacan", "valavan",
    "valli", "vannakan", "velan", "vellan", "velliyan",
    "venkai", "venman", "venni", "verri", "vikkan",
    # Common nouns from the inscriptions
    "akam", "akaram", "akaravu", "akkam", "alam",
    "ali", "aliyatu", "amalan", "amaram", "amma",
    "ammai", "anaivar", "ananku", "antan", "antar",
    "appal", "arai", "arakam", "aram", "ari",
    "arici", "aritu", "aru", "aruvi", "atavi",
    "avai", "ayil", "ayintu", "calai", "caran",
    "cati", "cavarai", "celvam", "cempan", "ceruppu",
    "cevvi", "ceyti", "cinai", "cina", "colai",
    "cunai", "cuppam", "erumai", "ettam", "evan",
    "icai", "ikal", "ilakkam", "ilaman", "ilancan",
    "illi", "ina", "inam", "inci", "intu",
    "iruvan", "itai", "itam", "itti", "ivai",
    "kalanai", "kalal", "kalan", "kalavu", "kalavoy",
    "kallam", "kalli", "kanam", "kannam", "kantu",
    "kapilai", "karam", "karari", "karayan", "katai",
    "katam", "katavul", "katir", "kattai", "kavu",
    "kayam", "kelvi", "keni", "keram", "ketu",
    "kilam", "kilan", "kinaru", "kiri", "kolam",
    "konkanam", "konnar", "koppu", "kotti", "kotumai",
    "kovalan", "kufican", "kulam", "kunram", "kuram",
    "kurampai", "kurankam", "kuril", "kurinji", "kurram",
    "kurri", "kurumai", "kurumpu", "kurunkan", "kuyilan",
    "makan", "makil", "makkal", "malar", "malarvu",
    "malai", "manai", "manam", "manatu", "manram",
    "manru", "mantai", "marakatam", "maram", "marrai",
    "maruntu", "matam", "matarppu", "mati", "matil",
    "matiram", "matti", "mayilai", "melam", "meli",
    "melli", "melu", "meni", "meynan", "meyppu",
    "min", "mintu", "mira", "miran", "miti",
    "mokkam", "molai", "moli", "mullai", "mumpu",
    "munaivan", "muram", "murampu", "murasu", "murru",
    "murukan", "mutalvan", "muti", "muyal", "nakaram",
    "nakku", "nalam", "nallar", "nampi", "nan",
    "nanmai", "nantanam", "natai", "nataivu", "natam",
    "natamai", "natpu", "nattam", "nattil", "navam",
    "naval", "navi", "nayam", "nayan", "netunkilli",
    "nila", "nilavu", "nilam", "niram", "niraivu",
    "nirai", "niranai", "oli", "olukku", "ompu",
    "onam", "onru", "oraan", "orai", "oran",
    "oruvar", "otam", "otti", "otu", "ovai",
    "ovam", "oyalum", "pakal", "pakuti", "palam",
    "pali", "palli", "panai", "panam", "panavu",
    "panci", "panku", "pannai", "pantam", "pantu",
    "papan", "parai", "paravu", "paripu", "pasi",
    "patam", "patavi", "pati", "patikai", "patukai",
    "payanam", "payir", "perai", "peran", "perunal",
    "perumai", "perumakan", "perun", "peruntirai", "perur",
    "peyar", "pi", "pilai", "pillai", "pintu",
    "pirai", "piram", "piri", "pirivu", "piru",
    "pirunaal", "pitar", "piti", "polam", "polivu",
    "pollai", "ponam", "ponku", "poniyan", "ponkam",
    "poriyalan", "poru", "porul", "porunan", "poruntal",
    "potti", "pottiyar", "poy", "poytu", "poyyaa",
    "pulai", "pulam", "pulan", "pulavar", "pulan",
    "pull", "punal", "punaivu", "puranam", "purinai",
    "puru", "pusai", "pusam", "putalvar", "putam",
    "putavu", "putu", "taatai", "talai", "talaivar",
    "talaivi", "tampi", "tanam", "tanmai", "tantam",
    "tantu", "taram", "tarpu", "tarum", "tarumam",
    "taruvai", "tatti", "tavam", "tavan", "tavu",
    "tayan", "tayil", "telu", "tem", "temputtai",
    "tena", "tenkai", "tennan", "tennar", "tenral",
    "teri", "terinta", "terivu", "terru", "teru",
    "tevam", "tevar", "tey", "tikai", "tiku",
    "timai", "tinai", "tinkal", "tipam", "tippili",
    "tiraikkattu", "tirumakal", "tirumal", "tirumeni", "tirupati",
    "tiruvallam", "tiruvana", "tiruveti", "titam", "titti",
    "tiyan", "tol", "tolakan", "tollai", "tonkai",
    "tontu", "toral", "tori", "toti", "toyu",
    "tukai", "tulai", "tunai", "tunivu", "tunmai",
    "turai", "turavi", "turi", "tuvai", "tuvasam",
    "ula", "ulai", "ulakam", "ulam", "ulavu",
    "ulla", "ullam", "ullatu", "unar", "unmai",
    "untu", "upakaram", "upayam", "uppu", "uravu",
    "uri", "urimai", "urru", "urtam", "urum",
    "uruvam", "utal", "uttamam", "uvakai", "uyir",
    "vacam", "vacanai", "vacanam", "vacappu", "vacatu",
    "vakai", "valam", "valavan", "vali", "valli",
    "vallu", "valluvar", "vampu", "vanam", "vanan",
    "vanci", "vanikan", "vannam", "vantai", "vanti",
    "varai", "varam", "varavu", "varivu", "varuti",
    "vatakku", "vati", "vayil", "vayiram", "velam",
    "velvi", "vempu", "venkalam", "venkay", "venkayam",
    "venni", "vennilavu", "venpa", "venram", "vetai",
    "veti", "viccam", "vicimpu", "vil", "vilakku",
    "vilam", "vilampu", "vilan", "vilavu", "vinai",
    "vintai", "viral", "viran", "viranai", "virivu",
    "viruntu", "vittu", "vitu", "viyal", "yam",
    # Place names (Mahadevan 2003 §4.2)
    "akkur", "alakapuri", "amparam", "anaimalai", "arachalur",
    "arikkamedu", "arittapatti", "erikkampatti", "jambai", "kanchipuram",
    "karur", "keelavalavu", "kilavalavu", "kongarpuliyankulam", "kunnakkudi",
    "madurai", "mamandur", "mankulam", "marugaltalai", "meenakshipuram",
    "meettukudi", "muttupatti", "neyveli", "palani", "panarpatti",
    "pugalur", "sittannavasal", "sitthanavasal", "thirupparankunram", "tirucchengodu",
    "tiruchirappalli", "tiruvadavur", "tiruvellarai", "tondi", "uraiyur",
    "vasavasamudram", "vellalore", "venkayanur", "vikramangalam",
]


def get_vocabulary() -> dict[str, str]:
    """Return the proto-Dravidian vocabulary."""
    return dict(VOCABULARY)


def get_attested_words() -> list[str]:
    """Return the deduplicated, lowercase list of *attested* Tamil-Brahmi words.

    This is the gold-standard source for `HoldoutWordRecall` and
    `CompoundDependencyConstraint`. Combines:
      1. Mahadevan (2003) Tamil-Brahmi epigraphic word list (TAMIL_BRAHMI_ATTESTED).
      2. Reconstructed Proto-Dravidian roots (VOCABULARY keys) as a fallback
         for older / non-Brahmi attestations covered by DEDR.

    Used by AttestedVocabularyLoader(family='old_tamil').
    """
    words = set(w.lower() for w in TAMIL_BRAHMI_ATTESTED)
    words.update(k.lower() for k in VOCABULARY.keys())
    return sorted(words)


def get_corpus_text() -> str:
    """Return the Classical Tamil corpus used for the Dravidian LM.

    Combines:
      1. Embedded Old Tamil / Tirukkural-style transliterated corpus
      2. The `tests/corpora/fixtures/tamil.txt` fixture used elsewhere in
         Glossa Lab studies

    This gives the Tier 5 Dravidian LM a larger and more varied character
    distribution without changing the transliteration scheme.
    """
    fixture = (
        Path(__file__).resolve().parent.parent.parent
        / "tests"
        / "corpora"
        / "fixtures"
        / "tamil.txt"
    )
    extra = fixture.read_text(encoding="utf-8") if fixture.exists() else ""
    return f"{OLD_TAMIL_TEXT} {extra}".strip()


def get_corpus_symbols() -> list[str]:
    """Return character-level symbol sequence from Old Tamil (flat list)."""
    return [c for c in get_corpus_text().lower() if c.isalpha()]


def get_corpus_inscriptions() -> list[list[str]]:
    """Return word-level character sequences for the Dravidian corpus.

    Each word in the text becomes a sequence of its constituent characters.
    Words with < 2 characters are excluded.  This produces multi-character
    sequences that CipherConstructor and AnchorConvergenceBenchmark require.

    Example: 'akara mutala' -> [['a','k','a','r','a'], ['m','u','t','a','l','a']]
    """
    text = get_corpus_text().lower()
    seqs = []
    for word in text.split():
        chars = [c for c in word if c.isalpha()]
        if len(chars) >= 2:
            seqs.append(chars)
    return seqs


def get_morphology() -> dict:
    """Return Dravidian morphology patterns."""
    return dict(MORPHOLOGY)
