# Findings — Worker W5, part 2 (reconstruction by repair worker W7, 2026-10-22)

**What this file is.** `findings_W5.md` on disk ends mid-sentence
(5,606 bytes) inside "Nearest neighbor 1" of its prior-art section
(a). This part 2 reconstructs the missing remainder **only** from
W5's filed evidence: the 27 manual query outputs
`raw/W5_q01…q27_*.json` and the 8 RESEARCH-CHECK stage sidecars in
`glossa-indus/claims/research_checks/`. No new searches were run by
W7: every W5 query file proved readable (the federated files are
JSON objects; q04/q11/q17/q19/q20/q21/q22/q26 are concatenated
JSON-object strings, decoded object by object; q02/q06/q07/q09/
q10/q12/q16/q18 are recorded empty-string results, not corruption;
q25/q27 are recorded download-failure strings). Where W5's filed
evidence does not support a subsection, this file says so in the
prescribed form instead of inventing content.

**Scope correction, from W5's own filed evidence.** W5's scope is
8 claims from two dossiers, but they are not 8 Roif claims: 4 are
Roif's (`indus_valley_script_deciphered_from_myth_65ff0a26_manual_001…004`)
and 4 are Fuls's (`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001…0003`
and `…_statisti_0004`) — W5's landed text itself corrects the tasking
on the second dossier ("not Roif"). The sidecars are named
`indus_valley_script_deciphered_from_myth_65ff0a26__…` and
`ancient_writing_and_modern_technologies_51831ac9__…`; there are no
`roif_avishai_*` sidecar files. Section (d) below therefore covers
all 8 W5 claims, grouped by author.

**Evidence-level labels** (same as W5's landed text): **FULL TEXT**
= the source's full text was read (held source documents, or OA
full text via the client). **At abstract level** = metadata/
abstract only; such lines establish nothing about novelty or its
absence by themselves. **Metadata level** = a bibliographic record
only (title/author/venue/DOI, no abstract in the filed output).

---

## (a) Prior-art question (a), completed: the guild / economic-function neighbours

W5's landed text breaks off at: "Bahata A. Mukhopadhyay,
'Guild-Based Trading, Taxation, Tax Farming, Trade and Craft …".
Completed from W5's q23 (Crossref DOI lookup):

- **Nearest neighbor 1 — Mukhopadhyay's guild paper, metadata
  level.** Bahata A. Mukhopadhyay, "Guild-Based Trading, Taxation,
  Tax Farming, Trade and Craft Licensing, Access Control: Economic
  Practices of Indus Civilization Encoded in Indus Script"
  (metadata level, q23: Crossref record for DOI
  10.2139/ssrn.4052072, dated 2022-01-01, abstract field empty).
  The same record surfaced inside the stage sidecar for Roif
  manual_001 as its joint-top neighbour (Crossref, relevance
  0.308), where the stage explicitly filed it as **not read in
  full text** (sidecar gap list). Its full text was never reached
  by W5: the SSRN search timed out (q16, empty result), the SSRN
  PDF read timed out (q25), and the OA fallback chain failed —
  SSRN timeout plus Unpaywall reporting no OA URL (q27). So the
  closest guild-specific neighbour to Roif's guild-ledger claim is
  established **at metadata level only**; what its argument is
  beyond its title is an open gap (see (e)).
- **Nearest neighbor 1b — Mukhopadhyay's earlier programme, at
  abstract level.** "Interrogating Indus inscriptions to unravel
  their mechanisms of meaning conveyance", *Humanities and Social
  Sciences Communications* (2019), DOI 10.1057/s41599-019-0274-1,
  and its SSRN version (2018), DOI 10.2139/ssrn.3184583 (both in
  q17, abstracts filed in full). At abstract level: Indus seals
  and tablets are argued to be "formalized data-carriers" like
  proto-cuneiform administrative tablets, modern fiscal stamps
  and ration tokens; signs are classed as content- and
  functional-morphemes (logographic, not phonograms), with
  identified numerical and metrological sign classes quantifying
  specific lexemes. That is a published economic/administrative-
  function reading of the script, without guild sign-values and
  without any Akkadian-mnemonic mechanism — at abstract level.
- **Nearest neighbor 2 — Rao 2018, FULL TEXT.** Rajesh P. N. Rao,
  "The Indus Script and Economics. A Role for Indus Seals and
  Tablets in Rationing and Administration of Labor", in *Walking
  with the Unicorn* (Kenoyer Felicitation Volume), Archaeopress
  2018, pp. 518–525 — full text retrieved by W5 (q24) and also
  read by the stage for manual_001 (sidecar: 3,654 words read).
  FULL TEXT: the 16 Harappan miniature tablets are proposed as
  ration tokens for porters/labourers, by parallel with
  proto-Elamite and proto-cuneiform tablets; similar inscriptions
  on stamp seals then suggest seals generated tokens, tablets and
  sealings "for repetitive economic transactions such as rations
  and exchange of canonical amounts of goods, grains, animals,
  and labor in a barter-based economy"; patterned texts are
  segmented (following Wells and Bonta) as Prefix (institution/
  person) – Medial (number/quantity, typically involving numbers
  and 'fish' signs) – Core (commodity) – Terminal (function of
  the sealing). This is the strongest full-text prior art in W5's
  evidence for the *economic-function half* of Roif's package:
  seals/tablets as instruments of rationing, labour
  administration and exchange were published, with an explicit
  Near-Eastern bookkeeping parallel, before Roif. Rao proposes
  no guilds, no tribute ledger, and no Akkadian mnemonics
  (FULL TEXT).
- **Neighbour 3 — Kalyanaraman 2012, at abstract level.**
  Srinivasan Kalyanaraman, "Indus script corpora,
  archaeo-metallurgy and Meluhha (Mleccha)", arXiv (q01/q03). At
  abstract level: Indus hieroglyphs are read as rebus
  representations of archaeo-metallurgy lexemes in the artisans'
  lingua franca — an artisan/economic decipherment family, but
  with a Meluhha rebus mechanism, not Akkadian shorthand and not
  guild organisation.
- **Neighbour 4 — Manuel 2008, metadata level.** Mark James
  Manuel, "Hidden agendas: testing models of the social and
  political organisation of the Indus Valley tradition" (CORE
  record in q03; the filed abstract field is a truncated EThOS
  repository string, so metadata level only). A thesis-length
  test of social/political organisation models for the Indus —
  the neighbourhood for guild/cartel-style organisation claims,
  not itself a script decipherment in the filed record.
- **Context neighbours, at abstract level.** The federated guild
  queries (q01/q03) also returned Sinha et al. 2010 (network
  syntactic organisation) and Yadav et al. 2009/2010 (n-grams) —
  structural, not economic, neighbours (at abstract level in
  q01/q03; Yadav was additionally read in full by the stage for
  manual_001, FULL TEXT, per that sidecar).

**Completion of W5's (a) conclusion, as its evidence supports it:**
the *economic-function* reading of Indus seals/tablets — rationing,
labour administration, taxation/licensing, fiscal data-carriers —
is published prior art (Rao 2018, FULL TEXT; Mukhopadhyay 2018/
2019, at abstract level; Mukhopadhyay 2022 guild paper, metadata
level). Nothing in W5's retrieved evidence proposes Roif's
specific mechanism (Akkadian-influenced mnemonics giving
guild-controller sign values) — a statement about the sources
searched, bounded by the Semantic Scholar / OpenAlex 429 gaps
W5 recorded, not a proof of novelty.

---

## (b) Prior-art question (b): the fish sign vs Roif's fish claim

**Scope note (required):** this section covers only what W5's own
filed evidence shows. The deeper fish-sign history — Heras,
Mahadevan, Gurov and the priority chain for fish = mīn — was
established separately by W3 in `findings_W3.md` §4a/§4d and is
**not** re-derived or relied on here.

**Roif's claim as filed.** Dossier claim manual_002: "The fish
sign encodes a coastal guild controller or maritime trader
identity (Lothal-linked)" (claim record). In Roif's held text the
fish is treated as one sign with one value — "Fish: Value marker,
controller mīn", with fish/jar seals at Lothal's pearl workshops
and a "coastal controller" reading (FULL TEXT, held Roif
document). It is this single-sign/single-office treatment that
the tasking calls the fish-sign-unity claim.

**What W5's queries showed:**

- The dedicated federated query (q05, "Parpola Indus fish sign
  min rebus Dravidian decipherment") returned, among its relevant
  hits, four Parpola items via Google Scholar — "The Indus
  script: A challenging puzzle" (1986), *A Dravidian solution to
  the Indus script problem* (2010), "Religion reflected in the
  iconic signs of the Indus script" (1988), and "'Hind Leg' +
  'Fish': Towards Further Understanding of the Indus Script"
  (2009) — each with only a short snippet in the filed output
  (at abstract level at best): the snippets show the fish
  pictogram worked through the rebus principle and the
  Proto-Dravidian mīn homophony (e.g. the compound 'black star'
  snippet in the 1986 item). No Parpola full text was retrieved
  by W5.
- Crossref (q19) returned the Parpola-school founding records —
  Parpola, Koskenniemi, Parpola & Aalto, "Decipherment of the
  Proto-Dravidian Inscriptions of the Indus Civilization. A
  First Announcement" (1969; journal record *Oriens* 1974, DOI
  10.2307/1580175) and its contemporary reviews — all metadata
  level (abstract fields empty in the filed output).
- The one fish-specific neighbour with a filed abstract is again
  Mukhopadhyay: "Can the semasiographic/logographic Indus script
  answer the Dravidian question? Insights from Indus script's
  gemstone related fish-signs, and Indus gemstone-word 'maṇi'"
  (OSF, DOI 10.31235/osf.io/ftdzc; SSRN version DOI
  10.2139/ssrn.4412558; sequel 2025, DOI 10.2139/ssrn.5079207,
  metadata level) — q19/q20, at abstract level. At abstract
  level, it treats the fish signs as a **plurality of distinct
  fish-like logograms** sitting in the 'core-informational'
  segment of formulaic inscriptions, encoding gemstone/lapidary
  meanings, taxed commodities and barter equivalencies, with
  fish-sign inscriptions concentrated in lapidary-workshop and
  jeweller contexts; it grounds the symbolism in the polysemic
  Proto-Dravidian fish-word *mīn* ('fish' / 'shining' /
  'gemstone'). So W5's evidence shows published fish-sign work
  that (i) assigns fish signs craft/commodity functions in a
  mercantile script — an economic neighbourhood for Roif's
  maritime-trader reading — but (ii) treats them as several
  distinct signs with lapidary/gemstone values, not as one
  unified sign naming a coastal guild office, and not tied to
  Lothal (at abstract level).
- CORE (q20) additionally returned, at abstract level, Parpola's
  "Tasks, Methods and Results in the Study of the Indus Script"
  (1975; general programme, no fish value stated in the filed
  abstract), Jyothibabu's critical review of Mahadevan's readings
  (2023; filed abstract describes Mahadevan's method in general
  terms), and Ganguly on Harappan–Brahmi sign variants (primary
  signs "seen to have many variants" — at abstract level, and
  about sign variants generally, not the fish sign).
- Rao 2018 (FULL TEXT, q24) is also a fish neighbour in W5's
  evidence: in patterned texts the Medial component "typically
  involves numbers and 'fish' signs", and the fish signs are
  reported (citing Bonta 2010) as linked to ancient weight
  measures 'minas' or 'maashas' — i.e. at full-text level the
  fish signs appear as quantity/weight elements inside economic
  transactions, not as office-holders.
- The stage sidecar for manual_002 itself found nothing usable:
  16 neighbours, all keyword false positives (coastal fish
  ecology, trader-identity finance), 0 read in full text
  (sidecar). The fish-specific Semantic Scholar (q06) and
  OpenAlex (q07) queries returned empty results — the 429 gap
  W5 recorded — so no semantic-index fish evidence exists in
  W5's file.

**Bounded conclusion for (b):** in W5's own evidence, prior art
gives the fish sign(s) Dravidian rebus values (Parpola school,
metadata/snippet level) and mercantile, gemstone/weight functions
(Mukhopadhyay at abstract level; Rao/Bonta FULL TEXT). No source
W5 retrieved states Roif's value — a coastal guild controller /
maritime trader identity centred on Lothal — and none states his
single-sign/single-value treatment; the retrieved fish literature
consistently works with a fish-sign *family*. Anything stronger
(e.g. who first read fish = mīn) is W3's record, not W5's.

---

## (c) Prior-art question (c): numerals and metrology — Sign 900 = six; Sign 700 and the unit of 40 / unit of 4

**The claims as filed.** Fuls dossier stubs: sign_val_0001
"Sign value: 900 / number six"; sign_val_0002 "Sign value: 700 /
a volumetric system with a unit of 40"; sign_val_0003 "Sign
value: 700 / a unit of 4". (The tasking's "900 = six units of
150" formulation appears nowhere in W5's filed query outputs
and nowhere in the held Fuls chapter text checked by W7; for
that sub-formulation: not reconstructable from filed outputs —
open gap.)

**What the held source itself says (FULL TEXT, Fuls 2020
chapter, the dossier's own document):**

- Sign 900 "represents number six"; Signs 904/914/908 are its
  repetitions giving 12/24/30; a tablet equation (ID 3786,
  counts of Sign 700 units vs Sign 840) yields candidate values
  4, 6, 8, 10 or 12 for Sign 900, and Fuls argues six, supported
  by the fish-sign argument (Sign 221, associated by Wells with
  1/3 of the basic fish Sign 220's weight, twice enclosed by
  Sign 900 read as the fraction 1/6: 2 × 1/6 = 1/3, ≈ 2.27 g)
  (FULL TEXT).
- The same chapter records the rival in print: "Wells (2011:128)
  argues that the value of Sign 900 should be five" (from the
  900 + Sign 2 replacing seven stacked strokes before Sign 585),
  and Fuls argues against that replacement reading (FULL TEXT).
  So "900 = six" is a contested value inside the source's own
  literature, not a settled one.
- Sign 700: "Wells (2018) demonstrates that Sign 700 represents
  a volumetric system with a unit of 40.4 litre for one long
  stroke. However, if a long stroke is 10 … then one volumetric
  unit equals 4.04 litre" (FULL TEXT). The two dossier stubs
  (unit of 40; unit of 4) are thus two scalings of one Wells
  proposal as reported — and re-scaled — by Fuls, not two
  independent findings.
- The chapter's own framing of the numeral prior art (FULL
  TEXT): stroke signs as numerals "as in other cultures
  (Parpola 1994, Korvink …)"; special numerical signs per Wells
  2015:73–76; Sign 415 as a special numerical sign (Bonta 1996;
  Wells …). W5 retrieved none of those works directly; they are
  known here only as cited inside the held chapter.

**What W5's external queries added:**

- Rao 2018 (FULL TEXT, q24) independently carries the unit-of-40
  prior art: "By estimating the approximate volume of one of
  these pots, Wells has proposed that [a] symbol is a volumetric
  measure with a value of approximately 40 liters (Wells
  2015)", with the fourfold count giving ≈ 160 litres, and the
  three strokes before each symbol read as the numeral three.
  Rao does not number the symbol 700 in the filed text (the
  glyphs are images lost in extraction), so the identification
  of Rao's vessel symbol with Fuls's Sign 700 rests on Fuls's
  own citation of Wells, FULL TEXT on the Fuls side and FULL
  TEXT on the Rao side, with the glyph-level match itself not
  verifiable from W5's extracted outputs — recorded as a
  limitation, not asserted.
- Metrology searches proper (q21/q26 Crossref; q22 CORE):
  Shigeo Iwata, "Weights and Measures in the Indus Valley"
  (encyclopedia entries, 2008/2016, DOIs
  10.1007/978-1-4020-4425-0_8938 and
  10.1007/978-94-007-7747-7_8938) — metadata level (no abstract
  filed). Enrico Ascalone, *Bronze Age Weights from
  Mesopotamia, Iran & Greater Indus Valley* (2022, DOI
  10.23797/9783529035425) — at abstract level: 2,000+ weights
  from 20 sites including ~900 from Dholavira, with typology
  and metrology discussed; the filed abstract states no Indus
  sign values and no unit of 40 or 4. Kenoyer, "Trade and
  technology of the Indus Valley" (1997, DOI
  10.1080/00438243.1997.9980377) — metadata level. The CORE
  metrology query (q22) returned only keyword noise (hog
  slaughter weights, dimensional metrology).
- The numerals federated query (q08, "Indus script numeral
  signs stroke signs number system Mahadevan") returned no
  numeral-specific scholarship beyond the general Yadav et al.
  and Sinha et al. records (at abstract level) and a Crossref
  record for Mahadevan, "Agricultural Signs in the Indus
  Script" (2012, DOI 10.25003/ras.02.02.0001, metadata level).
  The metrology Semantic Scholar query (q09) returned empty.
- The stage sidecars for all three sign-value claims returned
  only keyword false positives (six-sigma, Hounsfield-unit and
  export-unit-value records; relevance driven by the stub
  phrasings), with 0 relevant neighbours and, for
  sign_val_0002/0003, 0 full-text reads (sidecars). The stage
  therefore contributes no numeral/metrology prior art; the
  load-bearing evidence for (c) is the held chapter (FULL TEXT)
  plus Rao 2018 (FULL TEXT).

**Bounded conclusion for (c):** the volumetric unit of ~40
(litres) is Wells's published proposal, reported in both the
held Fuls chapter and Rao 2018 (FULL TEXT both); Fuls's own
contribution in the filed text is the re-scaling to 4.04 litres
and the Sign 900 = six derivation, the latter against Wells
2011's published five (FULL TEXT). General Indus weights-and-
measures scholarship (Iwata; Ascalone; Kenoyer) exists in the
retrieved records at metadata/abstract level, but W5's evidence
contains no independent corroboration of the specific values
six, 40 or 4 from that scholarship.

---

## (d) Per-claim summaries — the 8 W5 claims

**Roif manual_001 — guild ledger with Akkadian mnemonics
(untested).** The stage (sidecar, checked 2026-10-22T14:31Z,
verdict null) surfaced Mukhopadhyay's guild paper as a top
neighbour (metadata level; not read by the stage) and read Rao
2018 and Yadav et al. in full (FULL TEXT); W5's manual queries
then established the economic-function family as prior art —
rationing/labour administration (Rao, FULL TEXT), fiscal
data-carriers and taxation/licensing (Mukhopadhyay, at abstract
level / metadata level) — while no retrieved source proposes
the Akkadian-mnemonic mechanism or guild-controller sign
values (bounded by the 429 gaps, (e)).

**Roif manual_002 — fish sign = coastal guild controller,
Lothal-linked (partially_falsified in the dossier).** The stage
found only keyword false positives (16 neighbours, 0 read,
sidecar); W5's manual fish queries (q05/q19/q20) showed the
published fish literature working with a family of fish signs
carrying Dravidian rebus values (Parpola school, metadata/
snippet level) and gemstone, commodity and weight functions
(Mukhopadhyay at abstract level; Rao/Bonta FULL TEXT) — no
retrieved source states a coastal-controller office or a
Lothal-centred maritime identity, and the dossier's own
falsification note (fish distribution vs coastal sites) is a
Glossa record, not something W5's literature queries tested.

**Roif manual_003 — arrow sign (tīr) = border enforcement /
guild authority (untested).** W5's evidence here is the
thinnest of the eight: there is no dedicated arrow query file
beyond the Semantic Scholar attempt (q12), which returned
empty, and the stage sidecar returned 20 neighbours that are
all keyword false positives (border-enforcement law, arrow-of-
time physics), its three full-text reads being arrow-of-time
papers (sidecar). The horned federated query (q13) touches the
arrow only inside Roif's own Google Scholar listing (snippet
level). No prior art for an Indus arrow sign read as tīr /
enforcement was retrieved by W5, and no refuting art either —
on W5's filed evidence this claim's literature position is:
not reconstructable from filed outputs — open gap (see (e)).

**Roif manual_004 — horned deity sign = fire-altar intermediary,
Kalibangan (untested).** The dedicated query (q13, "Kalibangan
fire altars horned deity Indus seals ritual interpretation")
returned no horned-deity sign study: its relevant hits are
Roif's own listing (Google Scholar snippet, at abstract level:
the horned deity "as a ritual marker, perhaps tied to
Kalibangan's fire-altars"), general Kalibangan fire-altar /
Harappan religion items (Paddayya 1988; Paudel; R. Rao on a
Kalibangan seal and fire-altar ritual — all Google Scholar
snippet level), a Crossref "FIRE ALTARS" encyclopedia record
(metadata level), and Manuel on terracotta cakes as counting
tokens at Kalibangan fire altars (snippet level). The stage
sidecar likewise returned only noise plus Kalibangan burial/
geology records (sidecar). W5's evidence thus shows the
fire-altar *context* is published, but no retrieved source
assigns the horned-deity sign an intermediary office — the
sign-value half rests, in W5's file, on Roif alone.

**Fuls sign_val_0001 — Sign 900 = number six (untested).**
A stub for Fuls's derivation, which the held chapter states in
full (FULL TEXT, §(c) above): value six argued from the
two-sided tablet equations and the fish-weight fraction
argument, against Wells 2011's published value five (FULL
TEXT). The stage returned 34 neighbours, all keyword false
positives (six-sigma / sign-pattern mathematics), and read
three unrelated mathematics papers (sidecar); W5's external
queries added no independent numeral scholarship (q08, at
abstract level / metadata level). Literature position on W5's
evidence: an intra-literature dispute (Fuls six vs Wells
five), both sides known at FULL TEXT only via the held
chapter's own reporting.

**Fuls sign_val_0002 — Sign 700 = volumetric system, unit of
40 (untested).** The held chapter attributes the 40.4-litre
unit to Wells (2018) (FULL TEXT), and Rao 2018 reports Wells
2015's ≈40-litre volumetric proposal in full (FULL TEXT, q24)
— so the unit-of-40 is prior Wells work as reported by two
full texts, with the glyph-to-sign-number match not verifiable
from the extracted outputs (§(c)). The stage returned 21
keyword false positives and read nothing (sidecar); the
Crossref/CORE metrology queries (q21/q22/q26) produced only
general weights-and-measures records (Iwata metadata level;
Ascalone at abstract level) stating no such unit.

**Fuls sign_val_0003 — Sign 700 = a unit of 4 (untested).**
This stub is the same held passage as sign_val_0002 read at
the other scaling: "if a long stroke is 10 … then one
volumetric unit equals 4.04 litre" (FULL TEXT). It is Fuls's
re-scaling of Wells's 40.4, conditional on his long-stroke
base-10 result; it is not a second, independent value in the
source. The stage returned 25 false-positive neighbours, 0
read (sidecar), and W5's queries contain no other unit-of-4
source.

**Fuls statisti_0004 — "Statistical finding: positional
analysis" (untested).** A section-title stub, in this dossier
standing for the Fuls chapter's structural analysis of
numerical inscriptions (held chapter, FULL TEXT). Within W5's
own evidence, the external record is bibliographic: Crossref
(q11/q17) verifies Fuls's Appendices I–III in Wells 2015
(DOIs 10.2307/j.ctvr43jmf.15/.16/.17, metadata level), and
Mukhopadhyay's abstract notes "strong positional preferences
demonstrated by some signs" (at abstract level, q17). The
stage returned 30 false-positive neighbours (positional
tolerancing, fMRI statistics) and read three unrelated
statistics papers (sidecar). The substantive positional-
analysis prior-art treatment in this audit is W4's line, not
W5's; on W5's filed evidence alone, nothing more specific
about this stub is reconstructable.

---

## (e) W5's gaps (as filed, plus gaps the reconstruction exposes)

1. **Semantic Scholar** returned 429 during the stage runs and
   on manual query q02, and empty results on its later single
   attempts (q06 fish, q09 metrology, q12 arrow) — no
   semantic-index evidence for the fish, metrology or arrow
   claims (W5 landed header; query files). **OpenAlex**
   returned 429 from q07 onward (q07 fish, q10 Fuls: empty) —
   the same gap for those lines.
2. **Mukhopadhyay's guild paper (SSRN 4052072), the closest
   guild neighbour, was never read**: SSRN search timed out
   (q16), SSRN PDF read timed out (q25), OA fallback failed
   with no Unpaywall URL (q27). It stands at metadata level.
3. **BASE not searched** (expected empty per protocol doc) and
   **Zenodo errored** inside every federated search
   (`'str' object has no attribute 'isoformat'`, q01/q03/q05/
   q08/q13) (W5 landed header; query files).
4. **No Parpola fish full text in W5's file**: the fish rebus
   literature is present only as Google Scholar snippets,
   Crossref metadata and one CORE abstract-level review item
   (q05/q19/q20). The Heras/Mahadevan/Gurov history is W3's
   record, deliberately not duplicated in (b).
5. **Wells 2011 / Wells 2015 / Wells 2018 on Signs 700/900**
   were not themselves retrieved by W5: they are known through
   the held Fuls chapter's reporting (FULL TEXT as cited there)
   and, for the ≈40-litre proposal, Rao 2018 (FULL TEXT). The
   glyph-level identity of Rao's vessel symbol with Sign 700
   is not verifiable from the extracted outputs (glyphs are
   images).
6. **The arrow sign (manual_003) has effectively no W5
   literature evidence** — one empty Semantic Scholar attempt
   (q12) and a false-positive stage record. Its prior-art
   section is not reconstructable from filed outputs — open
   gap.
7. **The tasking's "900 = six units of 150" formulation** has
   no counterpart in W5's filed outputs or in the held Fuls
   chapter: not reconstructable from filed outputs — open gap.
8. **Stage neighbour quality**: for 7 of W5's 8 claims the
   stage's automated neighbours were keyword false positives
   (only manual_001's record read true neighbours in full);
   the audit weight for W5's claims therefore rests on the
   manual queries and held texts, and every novelty-shaped
   statement in this part 2 is bounded accordingly.
9. **Roif's venue status**: Crossref holds no Roif Indus
   record (q04 returned only an unrelated Indonesian author
   named Roif); two Roif titles do appear as Google Scholar
   listings inside the federated guild query (q01, metadata
   level) — consistent with W5's landed conclusion (self-
   published / unpublished manuscript), with the Scholar
   listings themselves unverified beyond that listing.

*End of W7 reconstruction of W5. `findings_W5.md` was not
modified; this file is append-only companion material.*
