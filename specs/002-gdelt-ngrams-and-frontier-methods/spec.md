# Spec 002 — GDELT Web Ngrams switch + frontier methods

**Status:** (i) implemented; (ii) and (iii) recorded as future work /
design notes — NOT implemented.
**Date:** 2026-10-05
**Context:** Guidance from Kalev Leetaru (GDELT Project) on how
researchers should work with GDELT during its infrastructure migration,
and two GDELT-published methods worth adopting as Glossa's corpus grows.
Private correspondence is not reproduced here (constitution §V);
only the public guidance and published methods are recorded.

## (i) GDELT source switch — IMPLEMENTED

GDELT's legacy search/API infrastructure is strained during its
Spanner migration; researchers were asked to switch to the temporary
**Web Ngrams dataset** instead of the DOC API:

- Every minute, two gzipped files are published for the minute ~2
  minutes ago under
  `https://data.gdeltproject.org/gdeltv5/weblegacy/ngrams/`:
  `<YYYYMMDDHHMM00>.ngrams.txt.gz` (tab-delimited DOCID, QUADGRAM,
  COUNT — no full text) and `<YYYYMMDDHHMM00>.toc.json.gz` (DOCID →
  url, title, date, language, image).
- Consumers should request the file from ~5 minutes ago and must
  accommodate GDELT's 15-minute heartbeat — files may exist only at
  15-minute marks, with gaps between.
- Quadgrams can be reduced to uni/bi/trigrams for phrase matching.

Implementation: `backend/glossa_lab/discovery/fetchers/gdelt_ngrams.py`
(source id `gdelt_ngrams`), registered as the **default** GDELT source.
It walks back over candidate marks (exact minute at now−5 min, then
15-minute heartbeat marks, bounded at 24 marks ≈ 6 h), downloads and
gunzips the pair, matches topic keywords (1–4-word keywords as
contiguous subsequences of a quadgram; >4-word keywords via constituent
4-gram windows plus reduced trigram/bigram windows), applies topic
exclusions, and cross-references matched DOCIDs through the TOC into
`RawItem`s for the discovery store. A watermark in
`.glossa-state/gdelt_ngrams.json` prevents rescanning processed
minutes. The DOC-API fetcher (`gdelt.py`) remains in the tree but is
**opt-in only** (explicit source request or a topic
`source_overrides.gdelt.enabled: true`), with a docstring noting it is
paused per GDELT's request during the migration.

Acceptance evidence: `backend/tests/test_gdelt_ngrams.py` (synthetic
.gz fixtures, no network) covers quadgram matching, TOC cross-reference,
exclusions, >4-word keyword handling, and heartbeat-gap walk-back with
watermark suppression. A live smoke test against the real dataset is
run at migration time and reported in the migration PR.

## (ii) FUTURE — fully-cited daily briefing over the discovery corpus

GDELT's "Today's Trends" briefings pair a reasoning model (Gemini)
with a day's coverage to produce a daily briefing in which **every
insight is linked to its source**. That shape maps directly onto
Glossa's Evidence Graph discipline (constitution §I): a "Glossa Daily
Briefing" over the discovery corpus — the day's new items clustered
into themes, each claimed insight carrying citations to the underlying
discovery items and, where relevant, to extracted claims scored by the
AEE core (spec 001 / `aee_core.py`).

**Status: proposed future work only. Not implemented in this spec.**
Open design questions for when it is scheduled: briefing cadence and
retention, which model/provider runs the reasoning pass, the citation
format (must resolve to Evidence Graph nodes), and the review gate
before any briefing leaves the lab (foundation-check rule, §III).

## (iii) DESIGN NOTES — manuscript-method lessons for future vision work

From GDELT's "Gemini for Museums" work — using Gemini Deep Research to
identify and contextualize a set of 800-year-old manuscript leaves, the
model matched human experts and even caught a provenance mark (a
"MLC 455" Colker-collection mark) that experts had missed — two method
lessons are recorded here for Glossa's future vision work on seals and
tablets:

1. **Supply physical metadata up front.** Giving the model each leaf's
   physical dimensions in the prompt corrected a vision-model scale
   bias. For Indus seals/tablets: pass dimensions, material, and find
   context in the prompt/context block before any reading attempt —
   never let the model infer scale from the image alone.
2. **Split analysis into discrete focused passes.** Separating the work
   into focused passes (identification; dating/provenance; reading)
   outperformed one mega-prompt. For Glossa: pass 1 identification
   (object class, material, context), pass 2 dating/provenance, pass 3
   sign reading — each pass's output entering the Evidence Graph as its
   own claim set, scored via the AEE core, rather than a single
   undifferentiated "analyze this seal" call.

**Status: design notes recorded. No vision feature is implemented or
scheduled by this spec.**

## Epistemic boundaries (per repo governance H13)

- (i) is an infrastructure substitution: ngrams provide phrase-level
  presence signals, NOT article full text; a quadgram match is weaker
  evidence than a DOC-API article record and is labeled as such in
  `RawItem.raw` (matched quadgrams + counts are preserved).
- (ii)/(iii) are learnings recorded from GDELT's published posts; they
  assert nothing about Glossa results and ship no functionality.
