# Submission-ready package — Indus preprint v6 (one-page summary, 2026-10-22)

**What this is.** The corrected preprint package, assembled by the
spec-025 audit fix commission. It is **not** submitted, deposited, or
published anywhere. The owner gives the go on the actual text before
any of that happens.

## What changed from v5 to v6

1. **Five missing bibliography entries added** (audit proposal P9).
   The text relied on five Mahadevan works that had no §8 entry. All
   five are now entered, from records verified at published-
   bibliography level (Jyothibabu 2023's bibliography, with
   corroborations — the fix addendum carries the per-work record):
   1981 "Place Signs in the Indus Script" (Proc. Fifth Int.
   Conf.-Seminar of Tamil Studies 1(2):91–107); 1982 "Terminal
   Ideograms" (in Possehl (ed.), *Harappan Civilization*, 311–317);
   1986 "Towards a Grammar of the Indus Texts" (*Tamil Civilization*
   4(3&4):15–30); 1989 "What Do We Know about the Indus Script?"
   (*Journal of the Institute of Asian Studies* 7(1):1–38); 2011 "The
   Indus Fish Swam in the Great Bath" (*Bulletin of the Indus Research
   Centre* 2:1–73). One bound travels with the 2011 entry: identifying
   it as the work the text cites is *inferred* (it is the only 2011
   Mahadevan Indus work found), and that is stated wherever the entry
   is described.
2. **The paper counts are qualified in the text.** "10 Mahadevan
   papers" and "38 Mahadevan papers" could not be tied to any
   verifiable source, so §3.23 now says in place that the counts are
   the program's own text-mining corpus counts — internal outputs, not
   externally sourced figures.
3. **Version bumped to v6** (title block and closing line), and the
   **PDF was regenerated**: two clean XeLaTeX passes, zero errors, 18
   pages. The new entries, the qualifier, and both v6 stamps were
   spot-checked in the rendered PDF, not just the source. (Build:
   TinyTeX-1 provisioned under `~/workspace/tex-tools` — XeLaTeX was
   absent from the audit environment; tectonic's bundle route was
   blocked, so TinyTeX was used.)

## What did not change, deliberately

- **The Steinkeller 1982 entry stands as printed, flagged.** New
  evidence positively indicates the titled article is JAOS 108(2):
  197–202 (1988) — but the proposal's own rule was *do not substitute
  the 1988 record*, the real 1982 item's venue and pages are still
  unverified, and the contents of JAOS 102(2) were never directly
  inspected. The entry is flagged here and in the version record as
  unverified; resolving it needs one JAOS backfile check.
- **No claim, result, anchor, or number in the paper was altered.**
  v6 is bibliography completion + honest qualification, on top of
  v5's citation corrections.

## What the adversarial pass found

An independent reviewer (GPT-4-Turbo — a different engine; the
frontier routes were unavailable: OpenRouter returned no-credit, two
frontier ids were not enabled on the account's chat endpoint) attacked
the v6 manuscript on novelty, constants, overclaims, citations, and
consistency. Five findings, adjudicated against primary sources in
`adversarial_pass_2026-10-22.md`:

- **One sustained:** the Zipf exponent ~1.7 in §2.1 is the paper's own
  statistic on the unreleased corpus, printed without a derivation a
  reader can check. **Recommendation:** at submission, add the fit
  details or qualify the sentence in place. Not silently rewritten
  here — it is a results sentence, and the change is the owner's.
- **One caution, already carried:** the ">90% coverage" novelty
  sentence is knowledge-hedged and scoped; its real exposure
  (unreleased corpus) is disclosed by the paper itself in three
  places.
- **Three not sustained:** the Proto-Dravidian conclusion (conditional
  on its face), the Nair-reliance premise (does not match the
  corrected text), and an alleged arithmetic inconsistency (checked:
  75 + 86 = 161; 6,363/7,002 = 90.87% — exact).

**Recommended before any actual submission:** a deeper adversarial
pass with a frontier reasoning model, when a route with credit is
available — the pass on file is a genuine independent read but a
shallow one, and this summary does not round it up.

---

## Addendum — v7 and the Roif credit (2026-10-22, owner-directed)

The package is now **preprint v7**. The change from v6 is the Roif
credit only; no claim, result, anchor, or number was altered, and
the adversarial-pass record above (run on v6) is unaffected in
substance — v7 adds attribution, it changes no result sentence.
Full record: `roif_credit_addendum_2026-10-22.md` in this
directory.

### Roif credit

**Credited now (in v7): the fish-sign model.** §8 gains both
citations — Roif 2025a (*Deciphering the Indus Valley Script: A
Phonetic-Mnemonic Akkadian Shorthand Approach*, Academia.edu,
12 June 2025, academia.edu/129921039) and Roif 2025b (*Indus
Valley Script deciphered — From Mythology to History using the
Akkadian shorthand approach*, Academia.edu, 2 August 2025,
academia.edu/143222807); Academia.edu mints no DOIs, so the
stable URLs are the identifiers. §3.5 and §3.19 credit the model
to Avishai Roif in his terms — the fish sign read /mi/ (mīn) as a
value/divine marker and guild/title marker (2025a); the "coastal
controller" maritime-guild reading, with fish, boat, and jar
signs recurring at port sites including Lothal (2025b) — and
state the division of labour: his published model and
predictions; this program's measurements (the numbers are ours,
from our corpus work). §7 Acknowledgments names him as the
source of the fish-sign model the tests were built on. The
program's dossiers were also corrected so the prose names him as
the claims' author (literature record `detected_authors`; dated
credit notes on all six Roif-dossier claims).

**Prepared but held: §3.32 (betweenness centrality).** Not
restored into v7. A separate, clearly marked restoration draft is
filed with the package at
`glossa-corpus/indus/pierson_2026_indus_decipherment_section_3_32_restoration_draft_HELD.md`
— the Phase 172–177 full-graph analysis with Roif's methodology
as its origin, flagged **HELD PENDING ROIF'S REPLY**: the owner
is writing to Roif to ask his *Semiotica* status and whether he
wants the section restored as co-author. The agreed attribution
sentence, verbatim as Roif proposed it on 2026-05-22 and the
owner accepted, is:

> Betweenness centrality analysis in this section was conducted by A. Roif using network-theoretic methods developed independently; the full methodological framework will appear in Roif (forthcoming, Semiotica).

If the NCSI paper is now in press, that sentence updates to the
full *Semiotica* reference. The corrected version ships without
§3.32 unless and until Roif agrees.

**The submission hold stands in full.** Nothing about Roif — or
anything else in this package — has been submitted, posted, or
sent anywhere. The owner gives the go on the actual v7 text
before any deposit or submission.
