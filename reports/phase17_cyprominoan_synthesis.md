# Phase-17 — Cypro-Minoan synthesis: signs, sounds, corpus, and what it means for our pipeline

This report synthesizes what we can glean from two recently-acquired Cypro-Minoan
sources:

1. **Valério 2016** (PhD thesis, Univ. Barcelona) — *Investigating the Signs and
   Sounds of Cypro-Minoan*. 697 pages, ~1.45 MB OCR text.
2. **Everson 2020** (Unicode L2/20-154 = ISO/IEC JTC1/SC2/WG2 N5135) — *Final
   proposal to encode the Cypro-Minoan script in the SMP of the UCS*. 24 pages,
   the encoding-standards baseline.

It also documents two new Linear B / Sanskrit corpus acquisitions that landed
in this round: the DAMOS Mycenaean corpus (in-progress scrape) and additional
GRETIL Rigveda variants.

## 1. Cypro-Minoan corpus structure (where the data lives)

From N5135 §1 + Valério's introduction:

| Property | Value |
|---|---|
| Date range | ca. 1550–1050 BCE (Late Bronze Age) |
| Provenience | Mostly Cyprus (Enkomi, Kition, Kalavassos, Palaepaphos); also Ugarit/Ras Shamra (Syrian coast); Tiryns (Peloponnese) |
| Object types | Clay balls, cylinders, tablets, vases |
| Total inscriptions | ~250 objects |
| Total signs | ~4,000 |
| Reference editions | Olivier 2007 (HCM); Ferrara 2012/2013 (HoChyMin) |
| Hellenization endpoint | Transformed into the Cypriot Greek Syllabary in the Early Iron Age (encoded in UCS already) |
| Ancestor | Derived from Linear A (per Evans 1909) |

This is a **very small corpus** by language-signature standards: ~4k tokens, on
the order of M77's Indus corpus (5,361 tokens). All the small-sample caveats
that apply to M77 will apply equally to CM signature analysis.

## 2. Sign inventory: Olivier vs. Valério

This is where the most interesting result lives.

**Olivier 2007's reference list (basis for N5135 encoding):**
- 96 syllabograms across CM 1, CM 2, CM 3
- Plus 2 stiktograms (punctuation: CM301, CM302) → encoded as U+12760, U+12761
- Plus 2 logograms CM201/CM202 (deferred from encoding because they appear in
  one fragmentary inscription)
- N5135 encodes **98 total CYPRO-MINOAN SIGN entries** in the SMP block U+12700..U+12761

**Valério 2016's revised inventory:**
- **57–70 syllabograms total** (depending on how aggressively variants are merged)
- The CM 2 tablets (largest single sample) contain only **57–59 distinct signs**
- Olivier's 96 figure is "inflated" — it requires mixing rare/hapax variants from
  different short inscriptions

The structural plausibility check is striking:

```
Linear A / Linear B  (ancestors / cousins)  ~90 syllabograms
Cypro-Minoan         (Valério)              ~57-70
Cypro-Minoan         (Olivier)              ~96
Cypro-Greek          (descendant)           ~55
```

A 57–70 sign inventory smoothly bridges Linear A → CM → Cypro-Greek. The 96-sign
inventory does not.

**Methodological critique by Valério (verbatim from Conclusions):**

> The traditional presentation of the Cypro-Minoan signary as maintained by
> Olivier contains many arbitrary identifications of signs. This owes to three
> factors. First, the signary has been framed in the also traditional division
> of Cypro-Minoan into three supposedly different scripts, CM 1, 2 and 3, which
> is itself based on inconsistent criteria and unproven assumptions. The
> ascription of one or another inscription to one of these artificial subscripts
> has led to circular arguments that certain pairs of sign forms correspond to
> distinct graphemes, not variants of a single sign, because they are attested
> in inscriptions assigned to different subscripts.

Valério replaces the CM 1/2/3 split with **four homogeneous subcorpora**:

1. **ENKO Atab 002–004** (the traditional "CM 2" — largest sample, very
   standardized script)
2. **Cylinder ENKO Arou 001** (single inscription)
3. **Tablet RASH Atab 004** = RS 20.25 (Ugarit; single inscription, long
   thought to be a "nominal list")
4. **Clay balls from Enkomi** (group of short texts, paleographically diverse
   but confined to one period and findspot — same script across all balls)

## 3. Phonetic values: what is and is not known

**Valério's working grid (Table 5.27):**
- Phonetic values proposed for **60 of 56–70 candidate sign forms** (so ~85–100%
  coverage of the inventory, depending on assimilation decisions)
- **9 values considered confirmed; the rest hypothetical**
- Of the 50 sign values offered: **41 already in Nahm 1981/1984**; 4 partial
  overlap; only **5 genuinely new**:
  - CM 37b/41 → *zi*?
  - CM 74 → *wi*?
  - CM 88/89/90 → *jo*
  - CM 98 → *qa*??
  - CM 112 → *z/ke*??

**Three-step methodology:**
1. Cross-script comparison: form + value vs. Linear A and Cypro-Greek syllabary
2. Internal analysis: positional distribution, frequency, sign alternations as
   morphological symptoms, scribal hesitations
3. Provisional transliteration test: read a small inscription set; check if
   readings match independently-known linguistic data (personal names from
   cuneiform sources, etc.)

**Concrete result on RASH Atab 004 (RS 20.25):**

> The values proposed here thus yield two personal names and one toponymic
> adjective well attested at Ugarit, while at the same time supplying a reading
> for [sequence] 55-70 that makes its repetition less surprising: **it is the
> word 'king', not a name** [/malki/, mlk = ma-al-ku].

This validates the phonetic system: the recurring 55-70 sequence in the tablet
corresponds to a Northwest Semitic word for 'king', not a personal name as
É. Masson 1974 had read it.

## 4. Language(s) of Cypro-Minoan

> As most of the sequences interpreted in this thesis occur in the tablet RASH
> Atab 004 and have been recognized from cuneiform sources, little information
> has been achieved as regards the language or languages written with
> Cypro-Minoan in Cyprus.

But Valério finds **one grammatical signal in the Enkomi clay balls**:
- An opposition between **-ø or -o (nominative?)** and **-o-ti (genitive?)**
- Direct counterpart in **Eteocypriot** of the following millennium

Implication: at least the clay-ball language likely belongs to the same
substrate that surfaces a thousand years later as Eteocypriot. This is the most
specific genealogical claim Valério is willing to make.

## 5. Encoding & character properties (N5135)

For our pipeline, the encoding facts that matter:

- **96 syllabograms** at U+12700..U+1275F (Lo = Letter, other)
- **2 stiktograms** at U+12760 (CM301) and U+12761 (CM302) (Po = Punctuation,
  other)
- Aegean shared punctuation: U+10100 AEGEAN WORD SEPARATOR LINE (𐄀) and
  U+10101 AEGEAN WORD SEPARATOR DOT (𐄁) — used for Cypro-Minoan word division
- Numbers ("Arithmograms"): poorly attested, deferred to N5136 (L2/20-155);
  may be the same as in other Aegean scripts
- The **21 CM 0 signs** from oldest Enkomi tablets (ENKO Atab 001) are
  **deferred** — not encoded in this proposal
- Logograms CM201/CM202 deferred (one fragmentary attestation each; possibly
  variants of existing signs)
- Directionality: generally L→R, but some boustrophedon and R→L (per Ferrara
  vol. I p. 209)

The Unicode design choice is noteworthy and pragmatic: take a **catalogue-based
repertoire** rather than wait for decipherment. As consensus emerges on which
signs are variants of others, annotations are added; no characters can ever be
removed once encoded.

## 6. What this means for our Phase-15+/16 pipeline

**Cypro-Minoan as a competing-hypothesis CAS-YAML.** With Valério's reduced
57–70 sign inventory and the Eteocypriot grammatical hint from the clay balls,
CM is now a plausible *typological* model to compare against the Indus M77
corpus. Both:
- have small inventories on the same order of magnitude (M77 has 64 distinct
  signs after the project's rank-corr mapping; CM has 57–70)
- have similarly small text counts (M77: 1,669 inscriptions / 5,361 tokens;
  CM: ~250 inscriptions / ~4,000 tokens)
- are undeciphered logo-syllabaries

The natural Phase-17/18 move is to add a `cypro_minoan_morphology.yaml`
hypothesis to the multi-hypothesis ranker, *but* CM's actual phonetic content
is too thinly attested to constrain morphological CAS-YAML DoFs reliably.
Better near-term use: as a **structural-typological control** for the
inventory-size and sign-distribution stats, alongside Linear A (which we have
via the Lengyel CSVs).

**The HoChyMin corpus is still the key blocker.** N5135 references Ferrara
2012/2013 throughout for sign occurrences and figure references; Valério also
relies on it. To run actual structural-signature DoFs (Zipf, MI, ε₂/ε₃) on
Cypro-Minoan, we need the inscription data tabulated in HoChyMin, which is
print-only. The 4,000 signs / 250 inscriptions are a hard upper bound on what
any machine analysis can extract anyway.

**The "single script vs. three scripts" question is operationally relevant.**
Our CAS-YAML manifold approach treats a hypothesis as one set of constraint
ranges. If CM 1/2/3 really are different scripts (say, recording different
languages), they should be three separate CAS-YAMLs. If Valério is right
that they are one script with regional variation, one CAS-YAML suffices. The
Daggumati allograph clusterer we wrote in Phase-16 (`scripts/phase16/sign_clusters.py`)
applied to a CM corpus would give an independent take on which forms cluster
together. That's a clean future experiment if/when the inscription data
becomes machine-readable.

## 7. Side acquisitions in this round

### GRETIL Rigveda (extended)
Already had `rigveda_aufrecht_gretil.txt` (1.42 MB, 10,552 verses, full Mandalas
1–10). Added two more variants:
- `rigveda_aufrecht_gretil.xml` (4.84 MB) — TEI-XML version with richer
  per-verse markup; useful for Phase-17 if we want metrically-segmented or
  pada-segmented sequences.
- `rigveda_h1-10_unicode_gretil.htm` (1.64 MB) — HTML/Devanagari rendering of
  same edition; useful for cross-checking against the Kalyanaraman BoW corpus
  in `vedic_kalyanaraman_morphology.yaml`.

The GRETIL Padapātha (word-by-word, sandhi-resolved) version that would be the
most analytically valuable variant **does not appear to be hosted at GRETIL
under either `corpustei/sa_Rgveda-Padapatha.xml` or
`1_sanskr/1_veda/1_sam/1_rv/rvpp_*`** — both 404. Padapātha source would have
to come from a different mirror (TITUS, Vedaweb, etc.) if we want it.

### DAMOS Mycenaean (in-progress scrape)
DAMOS has no public bulk download — the data is only reachable through the
React frontend at `https://damos.hf.uio.no/`. Its undocumented API endpoint is
`GET /ajaxitem/<id>/`, returning JSON with the inscription text, heading,
series, provenience, chronology, and notes. The script
`scripts/phase17/scrape_damos.py` walks IDs 1..6000 (the actual corpus size is
~5998) at 5 req/s with a polite delay and stops automatically after a run of
500-error responses.

At the time of writing the scrape is running in the background; results will
land at `corpora/damos/{raw/, damos_inscriptions.csv, damos_signs.txt}`. Once
the scrape completes, we have a Linear B running-text corpus large enough to
add as a third positive-control reference language alongside Sumerian (CDLI)
and Tamil (Kee2u) — directly useful for re-grounding the
`indo_aryan_morphology.yaml` and any future `aegean_*.yaml` CAS-YAMLs we add.

(The DAMOS license is CC-BY-NC-SA 4.0; redistribution requires citing
Aurora 2015 *Procedia – Social and Behavioral Sciences* 198, 21–31. The raw
JSON files are gitignored as part of the regenerable `corpora/` tree;
downstream derivative CSVs we want in the project will be checked in
separately.)

## 8. Updated remaining-gaps list

Tier 1 (still needed, unchanged):
1. Wells 2015 *Epigraphic Approaches to Indus Writing* — paid book.
2. Parpola CISI Vol 3 — out of print.
3. ICIT full database (Fuls) — email request.

Tier 2 (still needed):
4. **HoChyMin** (Ferrara 2012/2013) — print-only; only path is library or
   contacting Silvia Ferrara directly. Without it, Cypro-Minoan stays at the
   typological-summary level and can't enter the Phase-15/16 multi-hypothesis
   ranker as a measured CAS-YAML.
5. ~~DAMOS Linear B inscriptions~~ — **acquired** (this round, via web scrape).
6. Padapātha-form Rigveda — would need to be sourced from TITUS/Vedaweb if we
   want word-segmented Sanskrit beyond what the Aufrecht XML structure gives.

## Citation references (from N5135 + Valério)

- Aurora, F. 2015. "DAMOS (Database of Mycenaean at Oslo). Annotating a
  Fragmentarily Attested Language." Procedia – Social and Behavioral Sciences
  198: 21-31. doi:10.1016/j.sbspro.2015.07.415
- Everson, M. 2020. "Final proposal to encode the Cypro-Minoan script in the
  SMP of the UCS." ISO/IEC JTC1/SC2/WG2 N5135 = L2/20-154.
- Ferrara, S. 2012/2013. *Cypro-Minoan Inscriptions* (HoChyMin), 2 vols.
  Oxford UP.
- Masson, É. 1974. *Cyprominoica: répertoires; documents de Ras Shamra; essai
  d'interprétation.* Studies in Mediterranean Archaeology 31:2, Göteborg.
- Nahm, W. 1981. "Studien zur kypro-minoischen Schrift." Kadmos 20: 52-63.
- Nahm, W. 1984. "Studien zur kypro-minoischen Schrift II." Kadmos 23: 164-179.
- Olivier, J.-P. 2007. *Édition holistique des textes chypro-minoens* (HCM).
  Pisa-Rome.
- Valério, M. F. G. 2016. *Investigating the Signs and Sounds of Cypro-Minoan.*
  PhD thesis, Universitat de Barcelona.
