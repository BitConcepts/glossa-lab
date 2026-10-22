# Correction proposals — GATE-PENDING (Material Audit 2026-10-22, spec 025)

The audit's stage records are advisory (verdict null by construction)
and change nothing by themselves. The items below need a program gate
or an owner decision that this audit commission does not carry, so
they are filed here as proposals with their evidence. Raw outputs are
in `raw/` in this directory. Evidence levels are marked on every item;
bounds are carried verbatim, per the abstract-bound rule.

## P1 — Farmer/Sproat/Witzel dossier: framing note (no status change proposed)

The four claims in `farmer_sproat_witzel_2004` stand as
"contradicted", with the Rao entropy results as the lead counter
evidence. The audit's challenge pass (W2) found the published
exchange does not support treating the matter as settled: Sproat
2014 (*Language* 90(2):457–481, DOI 10.1353/lan.2014.0031, FULL TEXT
— publisher PDF, indexed in `raw/W2_browser_sources.json`) shows the
published entropy measures do not discriminate real non-linguistic
systems and that the measures that do classify place Indus largely
via text length; Rao et al. 2010 (DOI 10.1162/coli_c_00030, FULL
TEXT) claims inductive evidence only; the exchange closed in
non-concession (Rao 2015 / Sproat 2015). Proposal: append a dated
note to the dossier recording that the literature position is
**contested and unresolved**, citing W2's filed evidence. The
dossiers' own `not_understood` fields already carry much of this
nuance. Any status change is for the program's adjudication gate,
not this audit. Supporting items: Parpola 2008 (FULL TEXT) and
Vidale 2007 (quoted in FULL TEXT) reject Farmer's *proof* claim;
Mukhopadhyay 2023 (DOI 10.1057/s41599-023-02320-7) partially
vindicates the functional core **at abstract level**; Nair 2026
(FULL TEXT) is mixed and expressly does not resolve the question.

## P2 — fuls2023 dossier metadata: detected_year

`fuls2023_catalog_of_indus_signs` carries detected_year 2008. The
document is Fuls, *Catalog of Indus Signs* (2023, self-published,
ISBN 979-8-398-42230-6); 2008 is the ICIT build year. Evidence: W4,
FULL TEXT. Proposal: correct the intake metadata field, or append a
dated note if the field is frozen by convention.

## P3 — Roif dossier: source description

The Roif document is a self-published manuscript — its own first
page states it was "Edited and Abbreviated using the assistance of
AI"; no venue, date, or DOI exists for it, and its intake
`detected_doi` (10.2307/595168) is a bibliography hyperlink
belonging to Sarton 1955 (Crossref-verified, W5). Proposal: describe
the source in the dossier as a self-published manuscript with no
identifier of its own. (Publication of any Roif-claim result stays
under the program's existing Roif gate regardless.)

## P4 — ancient_writing dossier: authorship and venue

The document `ancient_writing_and_modern_technologies` is not a Roif
paper: it is Andreas Fuls, "Ancient Writing and Modern Technologies
– Structural Analysis of Numerical Indus Inscriptions", in *Studies
on Indus Script* (Conference on Indus Script, Mohenjodaro 2020;
National Fund for Mohenjodaro, Government of Sindh), pp. 57–88 plus
sign-list appendix (FULL TEXT, W5 — the held PDF's own front
matter). Its intake `detected_doi` (10.13109/hisp.2015.128.1.42)
belongs to Fuls 2015, *Historical Linguistics* 128(1):42–58
(Crossref-verified). Proposal: correct the dossier's source fields
accordingly. Note: Spec 065's recovery act already resolved this
document's identity in the program's records; this proposal aligns
the extracted-claims dossier fields with it.

## P5 — DECIPHERMENT_DOSSIER_v1.md: Nair "4/4" line

The line "Nair (2026) scorecard: 4/4 linguistic-consistent metrics"
is not supported by Nair's full text (W6, FULL TEXT): the scorecard
has four metrics on which Indus discriminates from the *heraldic*
baseline, matches the *administrative* baseline on only two of four,
and is nowhere scored "4/4 linguistic-consistent". Proposal: correct
the line to Nair's own framing (intermediate position; discriminates
from heraldic baseline on 4/4, from administrative baseline on 2/4).

## P6 — Parpola dossiers: priority note

The fish = mīn rebus and the star reading are presented in the
dossiers through Parpola 2010. The priority record (W3, FULL TEXT
via Jyothibabu 2023, DOI 10.23993/store.85246, and the lecture text
itself): the fish rebus is Heras's (1930s); fish readings were
published by the Soviet (Gurov — who read fish as *kay*) and Finnish
teams in 1965–70, Mahadevan 1970, and Fairservis 1985/1992; Parpola
2010 is a synthesis. Mahadevan 2011 concluded the fish = star reading
"had run out of steam and needed reappraisal". Rival values for the
fish sign are on record (Gurov *kay*; Jyothibabu *kaḻ*; Mukhopadhyay
*maṇi* — the last **at abstract level**). Proposal: append a dated
priority/critique note to the Parpola dossiers. No decipherment is
adjudicated by this audit.

## P7 — Yadav dossiers: corpus-scope and priority notes

Both strongly_supported Yadav claims are verbatim-accurate in the
source papers (W1, FULL TEXT both) — no extraction correction.
Two framing notes are proposed: (i) the Zipf–Mandelbrot fit
(a = 15.39, b = 2.59, c = 44.47) is on the pruned EBUDS subset of
Mahadevan's M77 corpus, which the claim wording does not state, and
Yadav 2010 itself says a Zipf fit is "not sufficient to declare a
sequence as linguistic"; (ii) the beginner/ender positional result
is not a Yadav novelty — positional-statistical analysis of Indus
signs goes back to the Soviet (1965) and Finnish (1969) programmes,
Kondratov 1976 (metadata level — chapter paywalled), and Mahadevan
1977. Also recorded for the program: the dossier's "Phase-43 V3 Zipf
exponent ~1.35" is a different number from b = 2.59 and the two are
not interchangeable.

## P8 — Hunt dossier and positional line: three-part structure is prior art

A three-part positional grammar for Indus texts is published prior
art (W4, FULL TEXT): Wells 2015, ch. 3 (pp. 24–25) — "Patterned
texts consist of three fields (Initial, Medial and Terminal)" —
behind it Sinha et al. 2010 (arXiv:1005.4997, FULL TEXT), Yadav
2009, and Fuls's seven positional classes (explicitly syntactic, not
semantic), with roots in Mahadevan 1977 and Kondratov 1976. The Hunt
2025 document (a self-posted draft, September 2025; no indexed
record found) contributes the semantic slot labels and the
civic-ritual frame; the faunal-initial and celestial-terminal
characterizations have no published support in the texts read.
Proposal: append dated prior-art notes to the Hunt-tripartite and
related positional dossiers so the framing distinguishes the
program's semantic interpretation from the published structural
prior art. Any claim-status consequence is for the program's gates.
Related source identification (W4, FULL TEXT): the three
"Positional Analysis" stub dossiers are all Fuls — *Voprosi
Epigrafiki* 7(1):253–275 (2013), reprinted as Wells & Fuls 2015
Appendix II (DOI 10.2307/j.ctvr43jmf.16), and Fuls 2023 ch. 3.

## P9 — Preprint §8: in-text works with no bibliography entry

The body text relies on Mahadevan (1981) "Place Signs", Mahadevan
(1982) *Terminal Ideograms*, Mahadevan (1986) *Towards a Grammar*,
Mahadevan (1989), Mahadevan (2011), and aggregate counts ("10
Mahadevan papers 1972–2018"; "38 Mahadevan papers 1970–2018") —
none has a §8 entry (W6). None could be resolved to a verified
metadata record through this session's reachable sources, so no
entries were fabricated. Proposal: add verified entries when a
source with book/backfile coverage is reachable, or qualify the
in-text counts as internal text-mining outputs. Open gap.

## P10 — Preprint §8: Steinkeller 1982 entry unresolved as cited

The entry "Steinkeller, P. (1982). On the identity of the toponym
LÚ.SU(.A). *JAOS* 102(2), 299–309" could not be resolved in any
reachable source (W6). The only same-title record found is a
different item (JAOS 108(2):197, 1988, DOI 10.2307/603646). This
session's evidence cannot distinguish "entry fields wrong" from
"1982 article unindexed under this title". Proposal: verify against
a source with JAOS backfile coverage before citing further; do NOT
substitute the 1988 record. Open gap.
