# Material Audit Report — Glossa Lab, 2026-10-22 (spec 025)

**Commission:** the owner's order of 2026-10-22 — check the program's
load-bearing literature claims and citations with the paper-search
MCP, under the protocol in `docs/paper-search-mcp.md`. Executed on
branch `spec/025-paper-search-research-check` (main merged in at
`a5a65f86`), in a fresh worktree; the main checkout was never touched.

**What was checked.** All 31 extracted claims in 10 dossiers
(`glossa-indus/claims/extracted_claims/`), every claim the preprint
and the anchor dossiers lean on, all 23 entries of the preprint's
reference list, the preprint's headline positioning (the 161 anchors,
the three-slot positional grammar, the Dravidian reading family), and
the sources the anchor dossiers rest on. Every claim got a
RESEARCH-CHECK stage record (in
`glossa-indus/claims/research_checks/`; advisory, verdict null by
construction) built from at least two concept phrasings across at
least two independent sources, plus worker-run challenge queries.
Nearest neighbours were read in full text wherever a lawful copy was
reachable. All raw outputs are filed in `raw/` in this directory;
worker findings are `raw/findings_W1.md`–`findings_W6.md`, plus
`findings_W5_part2.md` (see the method note).

**What this audit is not.** It does not adjudicate any decipherment,
change any claim status, anchor, or score, or contact any scholar.
Corrections it could land under the repo's own rules are in
`corrections_log.md`; the rest are filed as gate-pending proposals
in `correction_proposals.md` (P1–P10).

**Evidence levels — read this first.** Every finding below is marked
**FULL TEXT** (the work itself was read), **metadata level** (a
resolved Crossref/arXiv/OpenAIRE record was checked), or **at
abstract level** (only an abstract was available). Per the standing
abstract-bound rule, a finding that rests on an abstract or a partial
read keeps its bound wherever it is used, including in the
correction notes. "Not found" always means *not found in the sources
searched* — unreachable neighbours are open gaps, never proof of
absence.

## Headline outcomes

1. **The two strongly supported Yadav claims are accurate as
   extracted** — both are verbatim in the source papers (FULL TEXT).
   But the Zipf fit was run on a subset of Mahadevan's corpus, and
   the beginner/ender result is not a Yadav first: positional
   statistics on Indus signs goes back to the 1960s–70s Soviet and
   Finnish programmes and Mahadevan 1977.
2. **The "contradicted" framing of the Farmer–Sproat–Witzel thesis
   does not survive as a settled refutation.** The published exchange
   (Sproat 2014; Rao et al. 2010; both FULL TEXT) leaves the
   linguistic question contested and unresolved. The dossiers' own
   cautious fields already say much of this; a framing note is
   proposed (P1), with no status change.
3. **A three-part positional grammar is published prior art**
   (Wells 2015, ch. 3, FULL TEXT; behind it Sinha et al. 2010,
   Yadav 2009, and Fuls's positional classes). What the program's
   Hunt dossier adds is semantic labels on that structure, not the
   structure itself.
4. **The fish = mīn rebus is Heras's idea from the 1930s**, developed
   by the Soviet and Finnish teams and Mahadevan before Parpola;
   Parpola 2010 is a synthesis, and Mahadevan later said the
   fish = star reading had "run out of steam".
5. **The preprint's reference list had real defects, now corrected
   in v5:** a wrong year and a missing co-author (Wells & Fuls
   2015), a wrong year, volume, and author order (Parpola, Parpola
   & Brunswig 1977), a book cited as a journal article (Crawford
   2001), an entropy result credited to the wrong Rao paper (the
   *Science* paper was missing from the list), a Zipf exponent
   credited to Rao that no read text reports, an unverified journal
   attribution for Parpola 2010 (the located publication is the
   Coimbatore conference lecture), and Nair 2026 described as a
   "replication" of this program's tests when his full text says
   something narrower and deliberately hedged.
6. **The preprint's numbers all rest on one unreleased dataset**
   (Holdat LLC Indus Corpus v3). The preprint says so itself,
   plainly, in three places. The audit could verify none of those
   numbers and invented none.
7. **The Roif "deciphered" document is a self-published manuscript**
   (its first page says it was edited with AI assistance) with no
   venue, date, or identifier of its own. The Fuls chapter it was
   grouped with is a real 2020 conference-proceedings chapter.

## Method note — how the evidence was gathered, and its limits

- Six workers (W1–W6) plus one repair worker (W7: the two missing
  stage records, and the reconstruction below) ran the per-claim
  stages and manual queries. The coordinator re-derived the load-bearing items
  first-hand before any correction landed: the preprint's own
  sentences and reference entries (read verbatim from the `.tex`),
  the Crossref records for the Rao *Science* paper and the Meluhha
  article, Yadav 2010's filed full text (the fit parameters and the
  "not sufficient" sentence), and the two-worker Crossref absence
  pattern for Parpola 2010.
- **The MCP download chain failed session-wide for Crossref DOIs:**
  no Unpaywall email is configured, so `download_with_fallback`
  failed for most journal papers (it also once returned an unrelated
  cotton-transcriptome PDF for the Yadav DOI — identity-checked by
  W1, deleted, and re-fetched correctly through Europe PMC). Where
  full texts were still read, the route is recorded per item (arXiv,
  Europe PMC, publisher or author PDFs via browser text fetch —
  indexed with URLs and read ranges in
  `raw/W2_browser_sources.json`). A tooling gap for the program:
  configure an Unpaywall email for the connector.
- **OpenAlex and Semantic Scholar returned 429 for most workers most
  of the session**, and CORE timed out for W6. Per protocol, a 429
  closed that source for the session — no retry loops. The
  semantic-index leg of the protocol is therefore incomplete for
  several claims; those are open gaps (§ Open gaps), not negative
  results.
- W5's findings file was truncated on disk mid-sentence (its tail
  never landed). Its evidence was fully filed, so the missing part
  was reconstructed from W5's own raw outputs as
  `findings_W5_part2.md`, marked as a reconstruction; anything the
  filed evidence could not support is written there as an open gap.
- Stage stdout logs are retained in this directory on disk; the
  repo's `*.log` ignore rule keeps them out of git. The committed
  record of each stage run is its sidecar JSON.

## Per-claim results, by dossier

### Yadav 2009 / Yadav et al. 2010 (4 claims, strongly_supported) — W1

Both headline claims are in the source papers word-for-word
(**FULL TEXT**: arXiv:0901.3017v1; PLoS ONE 5(3):e9506,
DOI 10.1371/journal.pone.0009506):

- The Zipf–Mandelbrot fit is real, with parameters a = 15.39,
  b = 2.59, c = 44.47 — but it was fit on the pruned EBUDS subset of
  Mahadevan's M77 corpus, a scope the claim wording does not state.
  Yadav 2010 also says, in the same paper, that a Zipf fit "is not
  sufficient to declare a sequence as linguistic". The dossier's own
  "Phase-43 V3 Zipf exponent ~1.35" is a different number from
  b = 2.59; the two must not be used interchangeably.
- The beginner/ender claim is real (82 beginner signs / 23 ender
  signs, roughly 80% of signs position-specialised — **FULL TEXT**),
  but it is not a Yadav first: positional-statistical analysis of
  Indus signs was published by the Soviet programme (1965),
  the Finnish programme (1969), Kondratov 1976 (chapter in the Knorozov
  volume, DOI 10.1515/9783110800258.39 — **metadata level**, the
  chapter itself is paywalled), and Mahadevan 1977.
- No earlier Indus Zipf fit was found in arXiv, Crossref, or Europe
  PMC. Kak 1988's frequency analysis was not examined — open gap,
  not a negative result.
- Framing notes proposed (P7). No extraction correction needed.

### Farmer, Sproat & Witzel 2004 (4 claims, contradicted) — W2

- The extraction of the 2004 thesis is faithful (**FULL TEXT**,
  author-hosted PDF, 39 pp.). The citation is verified, including a
  real DOI the dossier did not carry: 10.11588/ejvs.2004.2.620
  (Heidelberg; not Crossref-registered; EJVS 11(2):19–57).
- Two of the four "claims" are title/subtitle fragments of the 2004
  paper rather than propositions — a classification note, not an
  error; the dossier reads their direction correctly.
- The challenge pass failed the "settled refutation" framing: Sproat
  2014 (**FULL TEXT**, publisher PDF) shows the published entropy
  measures do not discriminate real non-linguistic systems, and the
  two measures that do classify put Indus in the non-linguistic
  class largely through text length; Rao et al. 2010 (**FULL TEXT**)
  claims inductive evidence only and states that neither thesis can
  be proved without a decipherment; the exchange closed in
  non-concession (Rao 2015 / Sproat 2015). Parpola 2008 (**FULL
  TEXT**) and Vidale 2007 (quoted in full text) reject Farmer's
  *proof* claim. Mukhopadhyay 2023 (DOI 10.1057/s41599-023-02320-7)
  partially vindicates the functional core **at abstract level**.
  Nair 2026 (**FULL TEXT**) is mixed and expressly does not resolve
  the question. Accurate framing: **contested and unresolved**.
  Framing note proposed (P1); statuses untouched.

### Parpola 2010 + the Dravidian family (2 claims) — W3

- Both extracted claims are genuinely Parpola 2010's positions
  (**FULL TEXT** — the Coimbatore lecture text, 34 pp.; the
  dossiers' page references to pp. 13/16 check out).
- The publication is the Kalaignar Karunanidhi Classical Tamil
  Research Endowment Lecture, World Classical Tamil Conference,
  Coimbatore, 25 June 2010, published by the Central Institute of
  Classical Tamil, Chennai (2010). The preprint's "*World
  Archaeology*, 42(2), 178–193" attribution was not verified by
  seven Crossref searches across two workers, nor in CORE, Europe
  PMC, or OpenAIRE — recorded as an open gap bounded by the
  session's 429 outages, with the located publication corrected
  into the preprint (v5, item 4 of the corrections log).
- Priority: the fish = mīn rebus is Heras's (1930s). Fish readings
  were published by Gurov (who read fish as *kay*) and the Finnish
  team in 1965–70, Mahadevan 1970, and Fairservis 1985/1992.
  Parpola 2010 is a synthesis of that line, not its origin.
  Critiques read in **FULL TEXT** via Jyothibabu 2023 (DOI
  10.23993/store.85246): Mahadevan 2011 concluded the fish = star
  reading had run out of steam; rival fish values are on record
  (Gurov *kay*, Jyothibabu *kaḻ*; Mukhopadhyay *maṇi* **at abstract
  level**). Priority note proposed (P6).
- Parpola 1994 and McAlpin 1981 citations verified (metadata level;
  McAlpin: Trans. APS 71(3), DOI 10.2307/1006352).

### The positional-grammar line (10 claims: Hunt ×3, positional stubs ×3, Wells ×3, Fuls 2023 ×1) — W4

- **The three-field structure is prior art (FULL TEXT).** Wells
  2015, ch. 3, pp. 24–25: "Patterned texts consist of three fields
  (Initial, Medial and Terminal)". Behind it: Sinha et al. 2010
  (arXiv:1005.4997, **FULL TEXT**), Yadav 2009, and Fuls's seven
  positional classes — Initial / Early-Medial / Mid-Medial /
  Late-Medial / Terminal / Post-Terminal / constant — which are
  explicitly syntactic, not semantic. Roots in Mahadevan 1977 and
  Kondratov 1976.
- The Hunt 2025 document ("without kings or conquests…", a
  self-posted draft of September 2025 by Treasure A. Hunt; no
  indexed record found) contributes the semantic slot labels and
  the civic-ritual frame. Its faunal-initial and celestial-terminal
  characterisations have no published support in the texts read.
  Prior-art notes proposed (P8).
- All three "Positional Analysis" stub dossiers are the same
  author's work: Andreas Fuls — *Voprosi Epigrafiki* 7(1):253–275
  (2013), reprinted as Wells & Fuls 2015 Appendix II (DOI
  10.2307/j.ctvr43jmf.16), and Fuls 2023, *Catalog of Indus Signs*,
  ch. 3 (**FULL TEXT** all three identifications). The fuls2023
  dossier's detected_year 2008 is wrong (the book is 2023; 2008 is
  the ICIT build year) — proposal P2.
- Wells's book is Wells & Fuls, *The Archaeology and Epigraphy of
  Indus Writing*, Archaeopress 2015 (DOI 10.2307/j.ctvr43jmf) —
  the record behind preprint correction 1.
- Sign 821: Wells's wording is verbatim and hedged ("we really do
  not have a firm reading"), and it agrees with Fuls (821 = doubled
  820, broader positional profile) — **FULL TEXT** both sides.
  Sign 297 "horned tiger": Wells's hedged iconographic proposal
  only; no independent sign-list confirmation was found.
- **Numbering warning for the program:** 800-range sign numbers
  exist only in the Wells/Fuls lists (Mahadevan has 419 signs,
  Parpola 386). Any cross-list identity claim needs a graphic
  crosswalk, which this audit did not perform — open gap.

### Fuls, "Ancient Writing and Modern Technologies" (4 claims) — W5

- The document is Andreas Fuls's chapter in *Studies on Indus
  Script* (Conference on Indus Script, Mohenjodaro 2020; National
  Fund for Mohenjodaro, Government of Sindh), pp. 57–88 plus the
  702-sign ICIT sign-list appendix (**FULL TEXT** — the held PDF's
  own front matter, printed pp. III–IV). It is a
  conference-proceedings chapter, not a journal article, and no DOI
  for the chapter was found. Its intake `detected_doi` belongs to
  Fuls 2015, *Historical Linguistics* 128(1):42–58 (Crossref-
  verified, DOI 10.13109/hisp.2015.128.1.42). Dossier source-field
  corrections proposed (P4). This is the same document the
  program's Spec 065 recovery act resolved as source S-1.

### Roif, "The Indus Script Deciphered" (4 claims) — W5 + W7 reconstruction

Source status first: the document is a self-published manuscript —
its own first page states it was "Edited and Abbreviated using the
assistance of AI"; it has no venue, date, or DOI anywhere, and no
bibliographic record for it was found (Crossref and the federated
indexes searched; Semantic Scholar and OpenAlex were
429-unavailable). Its intake `detected_doi` is a bibliography
hyperlink belonging to Sarton 1955 (Crossref-verified). Dossiers
should describe it as a self-published manuscript — proposal P3.

- **Guild-ledger / Akkadian-mnemonic package (manual_001).** The
  economic-function half is published prior art: Rao 2018
  (**FULL TEXT**) proposes the Harappan miniature tablets as ration
  tokens and seals/tablets as instruments of rationing, labour
  administration, and exchange, with an explicit proto-Elamite /
  proto-cuneiform parallel; Mukhopadhyay's programme argues seals
  are fiscal data-carriers with taxation/licensing functions
  (**at abstract level**, 2019, DOI 10.1057/s41599-019-0274-1), and
  his guild-specific paper (SSRN, DOI 10.2139/ssrn.4052072) is the
  closest guild neighbour — **metadata level only**: its full text
  was never reached (SSRN timed out; no open-access copy), so what
  it argues beyond its title is an open gap. Nothing in the
  retrieved literature proposes Roif's specific mechanism
  (Akkadian-influenced mnemonics giving guild-controller sign
  values) — a statement about the sources searched, bounded by the
  429 gaps, not a proof of novelty.
- **Fish sign = coastal guild controller (manual_002).** The
  published fish literature in W5's evidence works with a *family*
  of fish signs: Dravidian rebus values from the Parpola school
  (metadata/snippet level in W5's file — the priority history is
  W3's record), gemstone and commodity functions (Mukhopadhyay
  **at abstract level**), and quantity/weight elements inside
  economic transactions (Rao 2018 / Bonta 2010, **FULL TEXT**). No
  retrieved source states a coastal-controller office, a
  Lothal-centred maritime identity, or Roif's single-sign /
  single-value treatment.
- **Arrow sign = border enforcement (manual_003).** W5's evidence
  is effectively empty — one empty Semantic Scholar attempt and a
  stage record of keyword false positives. No prior art for or
  against was retrieved: **not reconstructable from filed outputs
  — open gap**.
- **Horned deity = fire-altar intermediary (manual_004).** The
  Kalibangan fire-altar *context* is published (snippet level in
  W5's file); no retrieved source assigns the horned-deity sign
  an intermediary office — in W5's evidence that sign value rests
  on Roif alone.

### The Fuls numeral claims inside the ancient-writing dossier — W5/W7

The three sign-value stubs are one passage of the Fuls chapter
read three ways (**FULL TEXT**, the held chapter): Sign 900 =
six is Fuls's own derivation (tablet equations plus a fish-weight
fraction argument), argued against Wells 2011's published value
five — a contested value inside the source's own literature. The
volumetric unit of ~40 (litres) for Sign 700 is Wells's proposal
(40.4 litres, Wells 2018 as reported by Fuls; Wells 2015's ≈40
litres also reported in Rao 2018, **FULL TEXT** both), and the
"unit of 4" stub is Fuls's re-scaling of the same proposal (4.04
litres if a long stroke is 10) — not a second independent finding.
General weights-and-measures scholarship (Iwata; Ascalone;
Kenoyer) was retrieved at metadata/abstract level and states none
of the specific values. One tasking formulation — "900 = six
units of 150" — appears nowhere in the filed evidence or the held
chapter: not reconstructable, open gap. Detail:
`raw/findings_W5_part2.md` §(c)–(d).

## The preprint's literature positioning

**The 161 anchors.** No external literature can check the anchor
set: every corpus number in the preprint (1,670 seals, 7,002 tokens,
390 signs, the positional z = 10.3, the 161-anchor set itself, the
fish-sign 0/113 contexts, the Zipf ~1.7) traces to the Holdat LLC
Indus Corpus v3, which is not publicly released and has no public
metadata record (W6 searched; none exists). The preprint discloses
this accurately in its abstract, its limitations (§4.4), and its
reproducibility statement (§6). The audit neither confirms nor
refutes any Holdat-derived number; the reliance map is in
`raw/findings_W6.md` §4.

**The three-slot positional grammar.** Published prior art for the
structure itself (W4 section above). The preprint's contribution is
the semantic interpretation of the slots and the readings hung on
them; the literature does not contain those readings, and nothing
read supports the faunal-initial / celestial-terminal
characterisations as published claims.

**The Dravidian reading family.** The preprint stands in the
Heras → Soviet/Finnish teams → Mahadevan → Parpola line (W3 section
above). Parpola 2010's own positions were extracted accurately; the
family's known internal critiques (Mahadevan 2011 on fish = star;
rival fish values) are now on the audit record and proposed as a
dossier note (P6).

**Nair 2026.** Citation and all three quoted statistics are exact
(**FULL TEXT**, arXiv:2604.17828). The preprint's framing
overstated the paper — "independent replication", "entirely
separate dataset", "strong converging evidence" — where Nair's own
conclusion is an intermediate position that "does not settle the
linguistic question", on a separate digitisation of the same
published assemblage, with a different test statistic that bears
on none of the preprint's grammar, anchors, or readings. Corrected
in v5 (corrections log item 7). An internal dossier line ("Nair
scorecard: 4/4 linguistic-consistent") is likewise unsupported by
the full text — proposal P5.

**Rao 2009.** The PNAS citation is exact on every field (Crossref
DOI record 10.1073/pnas.0906237106 — metadata level). The preprint
misattributed the *Science* entropy result to it and carried no
*Science* entry; both fixed in v5 (items 5–6). The Rao PNAS and
*Science* full texts were not read this session (connector chain
failure; both are obtainable — PNAS is open access as PMC2721819),
so the content checks on those two papers stand **at abstract
level**.

## Reference-list verification (all 23 entries) — W6

Verified field-by-field against resolved metadata records
(Crossref/OpenAIRE/arXiv); the full table is `raw/findings_W6.md` §1.

- **MATCH on all fields (9):** Burrow & Emeneau 1984; Farmer,
  Sproat & Witzel 2004; Mahadevan 1977; McAlpin 1981; Parpola 1994;
  Rao et al. 2009 (PNAS); Krishnamurti 2003; Nair 2026; Reade 2001.
- **MATCH with notes (4):** Southworth 2005 (Crossref's e-book
  record is dated 2004; the print year as cited is 2005); Laursen
  2010 (title shortened in the preprint; issue (2) confirmed by the
  record, DOI 10.1111/j.1600-0471.2010.00329.x); Witzel 1999 (pages
  1–67 not present in the resolved record); Kjaerum 1983 (series
  record resolved; the seals volume itself not individually
  resolved).
- **MISMATCH — corrected in v5 (4):** Wells 2011 → Wells & Fuls
  2015; Parpola/Parpola/Brunswig 1975 → 1977, vol. 20, author
  order; Crawford 2001 journal article → monograph; Parpola 2010
  *World Archaeology* → CICT conference lecture.
- **Partially corroborated (2):** Lubotsky 2001 (container volume
  resolved, DOI 10.33341/sus.1242; chapter not individually
  resolved); Potts 1994 (proceedings volume corroborated; chapter
  not individually resolved).
- **NOT RESOLVED — open gaps, entries left as printed (3):**
  Højlund & Abu-Laban 2012; Mitchell 1986; Steinkeller 1982 as
  cited (a different same-title 1988 record exists and was NOT
  substituted — proposal P10).
- **Unverifiable by design (1):** Miller 2025 (Holdat corpus) —
  honestly labelled in the preprint itself.
- **Also found:** body text relies on at least five Mahadevan works
  (1981, 1982, 1986, 1989, 2011) and two aggregate paper counts that
  have no §8 entry at all — proposal P9. None could be resolved to
  a verified record this session, so none was fabricated.

## What the anchor dossiers rest on — W6

`reports/phase128_evidence_dossiers_44.json` cites internal
artifacts, which rest on: the Wells segmentation witness — Wells's
1998 Calgary MA thesis (DOI 10.11575/PRISM/23641; the DOI was not
resolvable via Crossref this session and rests on the program's own
file — open gap) and 2006 Harvard PhD thesis, cross-matched against
the Wells 2015 form of the Wells/ICIT list (the 2015 Wells & Fuls
book, verified); and the Parpola–Mahadevan crosswalk — the canonical
sign registry from the mayig CISI digitisation, Mahadevan 1977
(verified), and Parpola's CISI numbering (CISI vol. 1, eds. Joshi &
Parpola, 1987, corroborated at metadata level by review records).
DECIPHERMENT_DOSSIER_v1.md additionally rests on Rao 2009
(verified), Parpola 1994 (verified), Nair 2026 (verified, but see
the "4/4" line, P5), the Yajnadevam corpus (no independent
publication record resolved), and Holdat (unverifiable).

## Corrections and proposals

- **Landed:** preprint v5 citation corrections (7 items,
  `corrections_log.md` Batch 1), the audit records themselves
  (Batch 2), and two ledger entries. The audit landed via PR #331
  (commits 5d436362 + 0abf27f3), merged to main as 814a5dc2 with
  all seven CI checks green on the final head (backend pytest,
  frontend Playwright, evidence-graph smoke, Indus public
  validation, shell wrappers on three OSes — the shell-wrappers
  job first caught a lint error in the spec's own stage code,
  fixed in 0abf27f3). The merge record is the ledger addendum of
  2026-10-22 filed with this report's final version.
- **Gate-pending proposals P1–P10** (`correction_proposals.md`):
  Farmer framing note; fuls2023 year; Roif source description;
  ancient_writing source fields; the DECIPHERMENT_DOSSIER "4/4"
  line; Parpola priority note; Yadav scope/priority notes; Hunt
  prior-art notes; preprint §8 entries for the in-text Mahadevan
  works; Steinkeller verification. None changes a claim status,
  anchor, or score — those remain with the program's gates.
- **Version flag:** preprint v5 is a corrected *source*; its PDF
  has not been regenerated (no xelatex in the audit environment)
  and **an adversarial pass is required before submission** of any
  new version.

## Open gaps (consolidated)

1. Kak 1988 frequency analysis — unexamined (W1).
2. Mahadevan 1977 — no open-access full text; content checks at
   metadata level. The preprint's "397 signs in the Mahadevan
   catalogue" figure was not independently verifiable.
3. Kondratov 1976 — paywalled chapter; priority finding at metadata
   level. Korvink 2011 (*A Positional-Statistical Approach*) —
   bibliographic record only.
4. Rao *Science* 2009 and PNAS 2009 full texts via this connector
   (chain failure, not availability) — content checks at abstract
   level.
5. Vidale 2007 full text; Sproat's 2023/2024 books; no dedicated
   2020s review article on the linguistic question was reached.
6. Parpola 2010 — a DOI could neither be confirmed nor ruled out;
   OpenAlex/Semantic Scholar were down. The *World Archaeology*
   attribution stands as "not verified in the sources searched".
7. Unresolved reference entries: Højlund & Abu-Laban 2012;
   Mitchell 1986; Steinkeller 1982 as cited; chapter-level records
   for Lubotsky 2001, Kjaerum 1983, Potts 1994; Wells's 1998/2006
   theses' metadata; the five in-text Mahadevan works (P9).
8. Wells 2015's "161 pages" figure and the Phase-157/158/160 mining
   counts (284 / 96 / 403) — internal outputs, not externally
   checkable; the book has no reachable open-access full text.
9. The Wells/Fuls 800-range ↔ Mahadevan/Parpola sign-identity
   crosswalk was not performed; cross-list sign claims need it.
10. Fuls 2023's per-sign entries were only partially present in the
    held text W4 read.
11. Semantic-index coverage: OpenAlex and Semantic Scholar were
    429-unavailable for most of the session, so the protocol's
    semantic leg is incomplete for several claims (W4, W5, W6
    records show the per-source errors in their sidecars).
12. Roif-claim detail that W5's filed outputs could not support is
    listed as not reconstructable in `findings_W5_part2.md`, not
    filled in.

## Coordinator's verification statement

Before any correction landed, the coordinator independently
re-read: the preprint's §1.2, §2.1, §3.10, acknowledgment, and §8
passages from the `.tex` itself; the Crossref records for DOI
10.1126/science.1170391 (Rao *Science*) and 10.2307/3631775
(Meluhha) from the filed raw outputs; Yadav 2010's fit parameters
and self-limiting sentence in the filed full text; and the
Crossref-absence pattern for Parpola 2010 across both workers'
filed searches. Worker findings that rest on sources the
coordinator did not re-read are attributed to their worker and
carry their evidence level above. One worker-evidence caveat is
recorded in the method note: W2's full texts were read via browser
text fetch of publisher/author PDFs (the MCP download chain had
failed), indexed with URLs and read ranges in
`raw/W2_browser_sources.json` — re-performable, but the fetched
texts are not themselves filed.

## Erratum (2026-10-22)

The Roif section of this report is headed "(4 claims)": those are
the four manual claims (manual_001–004), which carry the substance
and are the claims its paragraphs cover — but the Roif dossier in
fact holds six claims, because the audit's stage also ran
critique_0001 and critique_0002 (sidecars filed in
`glossa-indus/claims/research_checks/`, verdicts null), and
neither the surviving worker text nor the reconstruction gives
either of them a per-claim paragraph. The critique_0001 sidecar's
evidence also holds exactly one neighbour item that appears
nowhere in this report: Mukhopadhyay, "Semantic scope of Indus
inscriptions comprising taxation, trade and craft licensing…"
(2023; DOIs 10.31235/osf.io/7dtqz and 10.2139/ssrn.4316270), at
abstract level — the same guild/taxation neighbour family the
report already covers, so no finding changes. Two status notes
complete the record: the reconstruction the Roif section rests on
was independently verified — W8 checked W7's reconstruction line
by line against the filed evidence and found it sound — and this
report's open gaps stand verbatim, in particular the arrow claim
(manual_003) and the "900 = six units of 150" formulation, neither
of which is reconstructable from the filed outputs.
