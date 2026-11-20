# Meroitic Decipherment Campaign — Anchor Inventory Freeze v1 (Spec 097, Stage 4.1, T403)

**Date: 2026-11-20. Claim C097-8. Frozen against the completed
corpus of the Stage 4.1 completion record. An anchor is a form
whose reading is pinned by evidence independent of the corpus
statistics the campaign will test. Each anchor states: form,
proposed reading, evidence class, source, and the use the
class licenses. A candidate reading that depends on an anchor
not in this freeze is out of scope until a new freeze version
admits it. Transliteration follows the pinned corpus's mapping
(E = /o/ in the paper's convention, capitals for the dotted
letters) with normalized forms given in parentheses where the
literature differs.**

## Class A — name correspondences (pin phonology and onomastics; never common-word meanings)

| # | Form | Reading | Source / evidence |
|---|------|---------|-------------------|
| A1 | qes, qos | "Kush" (the country and people) | Egyptian transcription *kꜣš* of the endonym, attested from Middle Kingdom execration texts onward (Rilly 2016; Wikipedia, Meroitic language, with refs) |
| A2 | bedewe (bedewi) | "Meroe" (the city) | Egyptian renderings *bꜣ-rꜣ-wꜣ* and variants (Rilly 2016) |
| A3 | amana | the god Amun | Egyptian *Ỉmn* "Amun" in Meroitic rendering (Unicode proposal N3646, worked example) |
| A4 | ktke, kadke | "Kandake" — queen, queen mother | Greek Κανδάκη in classical authors for the Meroitic royal title (standard literature; Rilly & de Voogt 2012) |
| A5 | the royal-name set | the names of rulers also rendered in Egyptian hieroglyphic/Demotic inscriptions | The correspondence class through which Griffith fixed the sign values, 1907–1911 (Rilly 2016). The set is used as a class (name-slot behaviour), not as a word list |

## Class B — formula structure (pins slots; the filiation segmentation is carried as debated)

The funerary formula, in about half the published corpus,
known in outline since Griffith (1911):

| # | Slot | Form / structure | Reading of the slot |
|---|------|------------------|---------------------|
| B1 | invocation | wosi (wise) … asiri (soreyi) … | Isis and Osiris invoked; the suffix on the theonyms (vocative or conjunctive) is debated in the literature and is NOT frozen |
| B2 | presentation | "this is [deceased]" | the deceased's name occupies the name slot (the swap pool of the augmentation, 178 private names, is drawn from this slot) |
| B3 | filiation 1 | [mother's name] + teɖe-form (tedge) | "born of" — the mother relation; morpheme segmentation debated, relation not |
| B4 | filiation 2 | [father's name] + terike-form | "begotten of" — the father relation; same caveat |
| B5 | offering | clauses with ato "water" and food terms | the offering provision for the deceased (Griffith's contextual reading; Rilly 2007/2010 segmentation) |
| B6 | closing | short evaluative clause | "he/she was good" in the received reading; carried as received, flagged as the formula's least-pinned slot |

Sources: Griffith (1911) via Rilly (2016); the formula words
wosi, asiri/soreyi, terike, tedge are among the highest-frequency
forms of the held corpus, as the formula's prevalence predicts
(Glottometrics 15, 2007).

## Class C — numerals (pin quantity contexts; the administrative ostraca are the nearest-to-bilingual genre)

| # | Anchor | Content |
|---|--------|---------|
| C1 | the numeral sign inventory | units, tens, hundreds, thousands attested and valued; signs for 60, 90, 900 and for 4,000/6,000/7,000/8,000/9,000 unattested (Unicode proposal N3646, §5, after Rilly 2007) |
| C2 | the ostraca class | some 70 ostraca, predominantly short texts with numbers — administrative/commercial records whose arithmetic constrains readings (Rilly 2016) |
| C3 | licensed use | a candidate reading of a form in numeral company must predict quantities consistent with C1's values wherever the text's arithmetic is checkable; inconsistency falsifies the candidate for that text class |

## Class D — Egyptian loanwords and titles (pin a form only as far as the borrowing is demonstrated)

| # | Form | Reading | Evidence |
|---|------|---------|----------|
| D1 | peseto | "viceroy" (the king's son of Kush office) | Title of Egyptian derivation in the Napatan/Meroitic administration (standard literature; the translatable vocabulary is mostly titles, many borrowed from Egyptian — Rilly 2016) |
| D2 | the temple-title stratum | priestly and temple offices in the offering formulae | Egyptian religious vocabulary borrowed with the cults of Amun and Isis (Rilly 2016, as a class) |
| D3 | licensed use | a Class D proposal must name the Egyptian source form and the borrowing path; resemblance alone admits nothing | — |

## Class E — contextually pinned common words (scoring controls only; never sole support for a new reading)

| # | Form | Reading | Source |
|---|------|---------|--------|
| E1 | qor (qore) | "ruler, king" | Rilly & de Voogt (2012), via the standard summaries |
| E2 | kdi | "woman, lady" | same |
| E3 | ste | "mother" | same |
| E4 | mk | "god" | same |
| E5 | ato | "water" | same; also B5's offering context |
| E6 | the scale of the class | about 100 words translatable with some certainty in total scholarship; 39 lexemes with confirmed meaning (Rilly 2016; Rilly & de Voogt 2012) — Class E is small because the field's pinned vocabulary is small | — |

## The split (sealed held-out set, per the design §5)

Rule, hash-pinned here: a unit is **held out** iff
SHA-256(unit key) mod 10 == 0, where the unit key is the full
line for mero-corpus.txt lines and the inscription id
(e.g. "REM 0001") for acquired-corpus inscriptions. Computed
at this freeze on tower-compute: mero-corpus 18,090 lines →
1,825 held out, 16,265 development; acquired index 652
inscriptions → 77 held out, 575 development. The held-out
units are not used in candidate generation (Stages 4.2–4.3);
they are opened once, at Stage 4.4, against readings frozen
in writing before the opening. The seal is procedural — the
corpus is public, and the discipline is the program's own,
exactly as the design states.

## Freeze discipline

This freeze is v1. Changes require a v2 record naming what
changed and why, and any candidate scored under v1 keeps its
v1 basis on its record. The expert-verification stage (T406,
owner-gated) is the designed route for external challenge to
this inventory; until then, challenges enter only through the
program's own tests.
