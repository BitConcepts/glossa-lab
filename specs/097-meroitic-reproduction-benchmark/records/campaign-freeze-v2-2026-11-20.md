# Meroitic Decipherment Campaign — Freeze v2 (Spec 097, Stage 4)

**Date: 2026-11-20. Status: FROZEN before any Stage 4.2
computation. This freeze supersedes the split rule and the
affiliation-test registration of freeze v1 and of the
campaign design §§4–5 where they conflict, following the
whole-program red team of 2026-11-20 (findings F-08 and
F-09). Freeze v1's anchor inventory stands except as
re-sourced in §3 below. Venue: tower-compute; the Otten
corpus stays in held custody there and is never committed;
the acquired inscription corpus (CC BY 4.0) and the ASJP
lists (CC BY 4.0) are the only text bases this freeze
computes on, plus aggregate statistics of the held example
files. Companion: `records/freeze-v2-vocabulary-2026-11-20.json`
(the registered vocabulary, forms and glosses only, from the
CC BY / CC BY-SA sources named in §4; no Otten-derived text).**

## 1. The split, re-computed on distinct texts (F-08.1)

Freeze v1 split the name-augmented training file by line, so
copies of one underlying text, differing only in swapped
names, fell on both sides of the seal. That split is void.

**Registered basis:** the acquired inscription corpus
(Kovetsky build, pin `145af0836c071e7c9796d37d4b36add00d347c8a`,
CC BY 4.0 data) collapses to **368 distinct texts** (the
`text` field, deduplicated exactly). The augmented
mero-corpus.txt file is excluded from the split entirely:
its swap pool is not held as a list, so its twins cannot be
separated reliably; an independent 2026 account measured
662 distinct texts under name-masking in that file, and this
freeze does not rely on reproducing that count. The 932
distinct example phrases of the per-scholar files (Millet,
Rilly, Kalabsha) are development material only — they are
the generation source and are never sealed.

**Rule:** a distinct text is held out iff
SHA-256(text) mod 10 == 0, applied within the whole basis;
genre is the first-occurrence `kind` of the text, mapped to
the strata of §2. Result, computed at this freeze on
tower-compute: **335 development / 33 held out.**

## 2. Genre stratification (F-08.2)

Strata and counts (development / held out):

| Stratum | Dev | Held |
|---|---|---|
| funerary | 223 | 16 |
| royal / temple | 41 | 10 |
| document (ostracon, papyrus, wood, vessel) | 42 | 5 |
| graffito | 22 | 2 |
| other (oracular decree, not known) | 7 | 0 |
| **Total** | **335** | **33** |

Stage 4.4 reports held-out scores **per stratum**, and the
funerary stratum is scored and reported **separately** from
all other strata in every table: with 239 of 368 distinct
texts funerary, an unstratified score would mostly measure
the funerary formula. The "other" stratum has no held-out
texts and is reported as not administered.

## 3. Anchor re-sourcing (F-08.3)

Wikipedia and "standard summaries" are removed as
freeze-grade sources. Every Class A and Class E anchor is
re-sourced below to a primary or scholarly reference, taken
from the per-entry source apparatus of the acquired gold
lexicon (CC BY 4.0), which cites page numbers. An anchor
that cannot be re-sourced to that standard is marked
PROVISIONAL and is excluded from scoring controls.

| Anchor | Form | Re-sourced reference |
|---|---|---|
| A1 | qes, qos "Kush" | **PROVISIONAL** — the only source apparatus held for this entry cites Wikipedia (citing Rilly 2007/2011 without pages). Excluded from scoring controls until re-sourced by page. |
| A2 | bedewe "Meroe" | Rilly 2016, "Meroitic", UCLA Encyclopedia of Egyptology, p. 6 |
| A3 | amni (v1: amana) "Amun" | Rilly 2016, p. 4. The gold form is *amni*; v1's *amana* is carried as a spelling variant, not a separate anchor (see §7). |
| A4 | ktke "Kandake" | Rilly 2016, pp. 8–9 |
| A5 | the royal-name set | Carried as a class (name-slot behaviour), per Rilly & de Voogt 2012, *The Meroitic Language and Writing System*, CUP — used as a class only, never as a word list, as in v1 |
| B1 | wos "Isis", sorey "Osiris" | Rilly & de Voogt 2012, p. 10 (gold apparatus) |
| B3 | tedḫe "born of" | Rilly & de Voogt 2012, p. 14 (Filiation) |
| B4 | terike "begotten of" | Rilly & de Voogt 2012, p. 14 (Filiation) |
| D1 | peseto "viceroy" | Kuckertz 2021, pp. 18, 20 (gold apparatus) |
| D2 | ant "priest, prophet" (temple-title stratum representative) | Rilly 2016, pp. 7–9 |
| E1 | qore "ruler, king" | Rilly 2016, p. 9 |
| E2 | kdi "woman, lady" | Rilly 2016, pp. 7, 9 |
| E3 | ste "mother" | Rilly 2016, p. 9 |
| E4 | mk "god" | Rilly 2016, p. 7 |
| E5 | ato "water" | Rilly 2016, pp. 6, 9 |

Class B's remaining slots (B2 presentation, B5 offering,
B6 closing) and Class C (numerals) stand as in v1, sourced
to Griffith (1911) via Rilly (2016) and to the Unicode
proposal N3646 §5 after Rilly (2007) respectively; neither
is used as a scoring control for a new reading, per their
class licences. Class E's scale note (E6) stands: about 100
words translatable with some certainty; 39 lexemes with
confirmed meaning (Rilly 2016; Rilly & de Voogt 2012).

## 4. The affiliation freeze — registered numerically (F-09)

**Vocabulary.** The frozen vocabulary is the **182 forms**
in the companion JSON: every form (including spelling
variants as separate forms, §7) of the 81 gold-lexicon
entries rated *certain* or *probable* (47 certain, 34
probable), plus Meroitic Wiktionary lemmas with common-noun
glosses not already present (proper names excluded).
Sources: the acquired gold lexicon (data CC BY 4.0, per-entry
scholarly apparatus) and Wiktionary (CC BY-SA 4.0). No
Otten-derived form is in the vocabulary.

**Concepts.** Glosses are mapped to ASJP concept IDs by the
registered map in the pipeline code. **12 concepts** are
covered by the vocabulary and by both comparator sets: 12
two, 15 small, 16 woman, 17 man, 21 dog, 46 foot, 55 eat,
62 kill, 70 give, 72 sun, 75 water, 97 good.

**Comparators (attested forms only for the R1 test).**
ASJP CLDF (Wichmann et al., CC BY 4.0), pinned at
lexibank/asjp commit `cf4bf0d13c95256b1b48f440d07c5c098500a770`;
file SHA-256: forms.csv
`4ee30b771a2cba59e7e904587f7f60dc3d823824a7b9aae9dd6f73a960139321`,
languages.csv
`647174df2eb812eff370355b02b6843d76bfb2b082147bc263e5ccd4cc628be5`,
parameters.csv
`2ed306c24552ea61e48ad6dc067859d8b70029abfc1d36668246214a5a1183ec`.
R1 set (attested Nubian and Nara only; reconstructions are
excluded by construction — PROTO_NILE_NUBIAN is not in the
set): OLD_NUBIAN, NOBIIN, DONGOLESE_NUBIAN, KUNUZ_NUBIAN,
MEIDOB_NUBIAN, NARA. R2 set (Afroasiatic): COPTIC,
LATE_EGYPTIAN, MIDDLE_EGYPTIAN, AKKADIAN, BIBLICAL_HEBREW,
AMHARIC, HAUSA (one list per language).

**Correspondence scoring rule.** For a Meroitic form and a
comparator form of the same concept: take consonant
skeletons (vowels a, e, i, o, u removed; ASJPcode mapped by
the registered table in the pipeline code; Meroitic forms
folded only by the diacritic fold of §7). A pair **matches**
iff the first skeleton consonants are equal AND (either
skeleton has length 1 OR the second skeleton consonants are
equal). The test statistic **S** is the number of the 12
concepts for which at least one Meroitic form matches at
least one comparator form of that concept.

**Permutation design.** 10,000 permutations, seed 20261120:
comparator forms are shuffled across concepts (preserving
per-concept form counts) and S recomputed;
p = (1 + #{S_perm ≥ S_obs}) / 10,001.

**Pass bars.** R1 vocabulary test passes iff **p < 0.01 AND
S ≥ 5**. R2 vocabulary test: the same rule against the R2
set. R1 formative leg (supporting, not sufficient alone):
passes iff at least **3** formatives in the gold morphology
(26 entries) carry a published NES comparandum in their
source apparatus AND each is attested at least **20** tokens
in the development texts. R2 phonotactic leg: Rowan's
restriction is measured as the rate of same-place consonant
pairs (place classes: labial {p, b, m}, velar {k, q, g, x},
coronal {t, d, s, z, n, l, r}, other) among word-internal
consonant pairs separated by exactly one vowel, over the
development texts and example phrases; it passes iff the
observed rate is below the within-word consonant-shuffle
null at **p < 0.01** (10,000 shuffles, same seed) AND the
Meroitic rate is below the same statistic computed on the
R1 (NES) reference lists.

**Power statement.** At n = 12 concepts, the S ≥ 5 bar with
a chance match rate of 0.10 per concept gives α ≈ 0.0043.
Power is **0.81** if the true per-concept correspondence
rate is 0.50, and **0.42** if it is 0.35. The tests can
therefore detect only a strong correspondence signal; a
moderate signal is not detectable at this power, and a
failure of both vocabulary tests under this power statement
is adjudicated under §5, not as a positive classification.

**Corpus basis for 4.2.** All Stage 4.2 computation uses the
development partition (§1) and the example phrases only.
The held-out partition is not touched until Stage 4.4.

## 5. Adjudication vocabulary — amended

The outcome set for Stage 4.2 is: **R1 SUPPORTED / R2
SUPPORTED / UNDECIDABLE AT THIS POWER / each rival NOT
SUPPORTED at its registered bar**. R3 (isolate / null) may
be recorded only as **"not displaced"** — never as
"supported" — and a double failure of R1 and R2 under the
§4 power statement is recorded as UNDECIDABLE AT THIS POWER
with R3 not displaced. This amends claim C097-9's and the
design §4's R3 wording for all Stage 4 adjudications from
this freeze onward; the amendment and its cause (F-09) are
recorded here, before computation.

## 6. The seal, stated plainly

The held-out seal is **unverifiable by construction**: the
corpus is public, the split is a hash rule anyone can
recompute, and no mechanism could detect a breach. The
discipline is procedural and the program's own. Consequence,
registered as a cap: a Stage 4.4 held-out pass is one leg of
a SUPPORTED score, never the whole of it — SUPPORTED still
requires the identifiability protocol passed before the
opening (design §5), and every SUPPORTED citation from this
campaign carries the sentence "the held-out seal is
procedural and unverifiable by construction" with it.

## 7. Normalization and the varietas caution

Per Rilly's caution (ICNS 2026 keynote, reported in the
program's 2026-11-20 news check) that Meroitic spelling
variation is deliberate *varietas*, **no spelling
normalization is applied anywhere in Stages 4.2–4.4**:
spelling variants are data, kept as distinct forms in the
vocabulary and distinct types in every count. The only folds
permitted are (i) case-folding, and (ii) folding the gold
lexicon's diacritic letters (ḥ, ḫ, ṭ, ṯ, š) to the corpus's
ASCII classes for skeleton computation, both registered in
the pipeline code. A result that changes under a different
fold must be reported under both folds.

## 8. What this freeze does not do

It computes no Stage 4.2 test, moves no claim standing, and
touches no other program's record. The pipeline code that
implements §§1–4 is the program's own, held in the campaign
scratch on tower-compute and named in the Stage 4.2 outcome
record; only code and aggregate statistics are published.
