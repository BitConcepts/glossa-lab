# Spec 013 — Tamil Nadu Graffiti Crosswalk: Independent Attestation Contexts for the CANDIDATE-Tier Sign Tail (feasibility + acquisition gate)

**Status:** FEASIBILITY COMPLETE 2026-10-07. The study is
**frozen at its acquisition gate (§5)**: no graffiti data has been
ingested, and none may be ingested until written permission from
RMRL / the Tamil Nadu State Department of Archaeology is on file.
The permission request is owner-sent only (Appendix A; governance
rule H14 — agents never send email). Owner authorization for this
feasibility work: Tristen Pierson, 2026-10-07 (roadmap item 3).

**AI disclosure:** this spec was prepared by an AI agent
(Muse Spark, via Muse) at the direction of Tristen Pierson,
per constitution §VI. All counts in §2 were recomputed from
`backend/reports/INDUS_FINAL_ANCHORS.json` at feasibility time;
all access findings in §4 are from live public pages read
2026-10-07 and the Phase-107 acquisition log.

## 1. Purpose

Can the Tamil Nadu graffiti corpus provide **independent
attestation contexts** for any of the 113 Indus signs currently
sitting at CANDIDATE tier — signs whose internal-corpus evidence
was exhausted by the Phase-110 adjudication? This spec first
audits access (§4), freezes a hard acquisition gate (§5), and
only then defines the crosswalk design (§6) that may run if the
gate opens.

"In independent attestation context" is used in a narrow,
pre-committed sense (§6.4): the sign's *form* is attested in a
second, independently compiled corpus with its own site/context
record. It is not a reading, not phonetic evidence, and not
evidence of descent.

## 2. The tail problem (verified state, 2026-10-07)

From `backend/reports/INDUS_FINAL_ANCHORS.json` (287 anchors;
Holdat corpus: 390 signs / 7,002 tokens):

| Tier | Count |
|---|---:|
| HIGH | 166 |
| MEDIUM | 5 |
| LOW | 3 |
| CANDIDATE | 113 |

All **113** CANDIDATE entries share the same profile:

- `validation_status` = `premise_superseded` (113/113);
- the recorded reading is the inherited label **`kur`** (113/113),
  retained as a historical label of record, not a supported
  reading (Phase-110, spec 008);
- the basis cites the legacy allograph-resolution run's verbatim
  inheritance from donor sign M222 (113/113), whose own sourced
  reading is `min` (MEDIUM) — the premise the entries relied on
  is contradicted by the donor's own record;
- Holdat token frequency **1–4** (43 signs at freq ≤ 2; all 113
  at freq ≤ 4), with the degenerate positional profile
  (I = 0.000, T = 0.000, M = 1.000) shared by every rare sign —
  the profile match that "assigned" their values carried no
  discriminating information (Phase-132's recorded verdict:
  positional parking spots, not genuine phonetic readings).

Internal evidence for these 113 signs is therefore exhausted by
construction: at freq 1–4 in a 7,002-token corpus, no positional,
distributional, or co-occurrence statistic can separate them.
The only evidence class that can move any of them is **external
attestation** — the same conclusion the Phase-111/112 nulls
reached for classification evidence generally (specs 009/010).

## 3. The external corpus

K. Rajan & R. Sivanantham, *Indus Signs and Graffiti Marks of
Tamil Nadu: A Morphological Study* (Tamil Nadu State Department
of Archaeology, Jan 2025; CITATIONS.md §E.5). The underlying
dataset was compiled by the TNSDA project *Documentation and
Digitization of Graffiti and Tamili (Tamil-Brahmi) Inscribed
Potsherds of Tamil Nadu*:

- **15,184** graffiti-bearing potsherds reported from **140
  sites**; ~**14,165** documented;
- **2,107** classified signs: **42 base signs, 544 variants,
  1,521 composite forms**;
- the authors report ~**60%** of the base signs find parallels
  in the Indus script (and a higher share of all marks, ~90%,
  claimed paralleled somewhere in Indus material);
- the authors' own framing is **morphological** (shape
  comparison), explicitly not a reading or a language claim.

Recorded counterweights (research sweep 2026-10-05; Harappa.com
review of the volume): a ≥1,000-year gap separates the Indus
cities from most sherds; many sherds are not securely dated;
simple geometric marks (crosses, V-shapes, double lines) are
reinvented independently across unrelated traditions, so
resemblance is not descent. A Sept-2025 report of an AMS date of
1692 BCE for a Kilnamandi sarcophagus deposit with
graffiti-bearing pots is an excavators' *indirect* inference
about the tradition's age, not a date for any individual mark.
The design in §6 is built around these counterweights, not
around the headline percentages.

## 4. Access audit (2026-10-07)

| Question | Finding |
|---|---|
| Host | The database ("Graffiti Marks of Tamil Nadu") is an online resource of the **Roja Muthiah Research Library (RMRL), Chennai — Indus Research Centre (IRC)**, built with the Tamil Nadu State Department of Archaeology. The IRC's web application is **indusscript.in** (launched 2021 on a TN Department of Archaeology grant), the same platform that hosts the Mahadevan IM77/IDF-80 concordance. |
| Interface | **Search-only web database** (per-object / per-sign lookup). No evidence of a researcher bulk interface. (Audit note: the application is JavaScript-rendered and could not be text-extracted in the audit session; this finding rests on the Phase-107 acquisition log, Harappa.com's description of the resource as searchable online, and the published literature — no contrary indication found in any of them.) |
| Terms of use | Recorded in the Phase-107 acquisition log as **"TN State Dept. of Archaeology / RMRL research use."** No public license (CC or equivalent), no published data-use policy, and no terms page offering research-scale reuse was located. |
| Official export | **None located.** |
| Public API | **None located or documented.** |
| Data deposit (Zenodo / figshare / institutional repository) | **None located.** The dataset exists as the live database and as the published print volume. |
| Precedent | The program's existing use of the same platform's concordance data is recorded in `glossa-indus/CORPUS_VERSIONS.md` under license **"user permission"** — i.e., this platform's data moves by permission, not by open license. No equivalent permission for the graffiti dataset is on file. |

**Verdict: no clearly licensed bulk route exists.** The only
legitimate research-scale route is written permission from
RMRL/TNSDA. Per the owner's standing directives (publish nothing
requiring permission we lack; no scraping against terms), the
acquisition gate in §5 therefore applies, and **no data was
ingested under this spec's feasibility stage**.

## 5. Acquisition gate (frozen rule)

1. **No ingestion, scraping, bulk querying, or systematic
   automated access** to the Graffiti Marks of Tamil Nadu
   database until written permission from RMRL / TNSDA is on
   file in the repo (permission letter or email thread,
   archived per the Phase-107 log format).
2. The request is sent by the **owner personally** (Appendix A
   is a draft for Tristen Pierson to send; H14 bars agent-sent
   email absolutely).
3. Human-scale manual lookups of publicly displayed pages for
   design purposes (e.g., confirming the published 42-base-sign
   classification is displayed) are permitted; anything
   resembling harvesting is not.
4. If permission is granted, ingestion goes **only** to the
   gitignored local sources store
   (`glossa-corpus/indus/sources/tn-graffiti/`), with a
   Phase-107-format acquisition-log entry (source, permission
   reference, date, counts: sherds / sites / base signs /
   variants / composites / tokens). Source data is **never
   committed**; committed artifacts are limited to the
   crosswalk register, statistics, and code, per the
   Phase-111/112 licensing precedent.
5. If permission is refused or unanswered after a reasonable
   interval set by the owner, the study stays frozen. There is
   no workaround path. (§8 records one alternative that does
   not require the database at all; it needs its own owner
   authorization and is not part of this spec's execution.)

## 6. Crosswalk design (executes only after §5 opens)

### 6.1 Units

- Graffiti side: the **42 base signs** as the primary unit set;
  the 544 variants and 1,521 composites as a secondary,
  separately reported layer.
- Indus side: the **113 CANDIDATE signs** (§2) as targets; the
  **94 strict SA-independent HIGH+MEDIUM signs** (Phase-109
  re-based core) as a positive-control set; a complexity-matched
  random geometric-mark generator as the null set (§6.3).

### 6.2 Matching protocol (blinded, pre-registered rubric)

- Candidate pairs are presented **anonymized** (graffiti form vs
  M-sign form, no IDs, no readings, no frequency information) to
  the matcher — a frozen shape-similarity pipeline, or human
  raters if the owner prefers — which scores match / no-match
  with a confidence grade.
- The rubric is fixed before any pair is scored: stroke count,
  enclosure topology, appendage inventory, symmetry class,
  composite structure. **Complexity weighting is mandatory:**
  matches whose shared structure is a cross, V, double line, or
  comparably simple geometric form are recorded but carry
  **zero evidentiary weight** by rule — they are the forms the
  counter-literature shows are reinvented independently.

### 6.3 Null model

The cohort-level claim is tested against two nulls at a
threshold frozen in the execution addendum before unblinding:
(a) the match rate of the positive-control set under the same
protocol, and (b) the match rate of complexity-matched random
geometric marks. A per-sign attestation (§6.4) additionally
requires the individual match to be high-complexity under the
rubric; a cohort result that does not beat both nulls is
reported as a null result, in full, per program doctrine.

### 6.4 What counts as a result — and what it can never mean

A CANDIDATE sign gains an **independent attestation context**
iff: (i) a high-complexity graffiti match survives §6.2–6.3,
and (ii) at least one matched sherd carries a recorded site
context (dating recorded where the database provides it,
flagged as secure / insecure per §3's cautions). The attestation
register then records, per sign: matched graffiti base sign /
variant IDs, sherd count, site list, sequence contexts (does the
form occur in multi-mark sherd sequences, in which positions) —
contexts the 7,002-token internal corpus cannot supply at
freq 1–4.

An attestation is **not** a reading, not phonetic evidence, not
evidence of historical descent, and it does not by itself change
any anchor. Anchor changes flow only through the program's
normal adjudication path (new spec + owner review), with the
attestation register as one evidence input among others.

### 6.5 Deliverables (post-gate)

- `reports/phase113_graffiti_crosswalk_register.json` +
  summary `.md` (per-sign register, null-model results,
  complexity audit, limitations);
- acquisition-log entry (§5.4);
- ledger entries with AI disclosure.

(Phase number 113 is provisional, by ledger sequence at
execution time; the artifacts rename cleanly if the sequence
has moved.)

## 7. Feasibility verdict

**CONDITIONAL — well-posed and cheap if the data arrives;
blocked at the acquisition gate by design.** The expected value
is concentrated in the pictographic (high-complexity) minority
of the 113; the geometric majority is pre-committed to zero
evidentiary weight, which is exactly why the study is worth
registering: a positive result under §6 cannot be dismissed as
"simple marks recur," and a null result cleanly closes the
graffiti route for the tail. Enumeration of the
high-complexity subset happens at the post-permission design
freeze, when the graffiti base-sign chart and the M-sign forms
can legitimately be placed side by side at research scale.

## 8. Alternative recorded (not authorized here)

The 42-base-sign chart and the authors' parallels table are
**published** in the print volume (Rajan & Sivanantham 2025).
A manual crosswalk built from the published volume alone —
ordinary library scholarship, no database access — could
execute §6.1–6.4 at the base-sign level, without sherd-level
contexts. This route is recorded for completeness; it is
**not** authorized by this spec and would need its own owner
decision, because the boundary between "published table" and
"database substitute" must be the owner's call, not the
agent's.

## Appendix A — Draft permission request (OWNER SENDS; H14)

> To: Indus Research Centre, Roja Muthiah Research Library
> (admin@rmrl.in); cc: Tamil Nadu State Department of
> Archaeology
> From: Tristen Pierson, BitConcepts LLC — Glossa-Lab Indus
> decipherment research program
>
> Subject: Request for research access — Graffiti Marks of
> Tamil Nadu database (bulk export for a pre-registered
> comparative study)
>
> Dear colleagues,
>
> I direct a computational research program on the Indus
> script (preprint: DOI 10.5281/zenodo.23187630; public
> provenance registry: https://osf.io/ybd65/). We are preparing
> a pre-registered study comparing the sign forms of Rajan &
> Sivanantham's *Indus Signs and Graffiti Marks of Tamil Nadu*
> (2025) against a set of 113 rare Indus signs for which the
> internal corpus evidence is exhausted, to test whether any
> of them gain independent attestation contexts in the Tamil
> Nadu graffiti record. The study design, including its null
> models and the limits on what a match would be taken to mean,
> will be frozen in a public spec before any data is examined.
>
> I am writing to request permission for research-scale access
> to the Graffiti Marks of Tamil Nadu database — specifically a
> bulk export or equivalent of: (1) the classification (42 base
> signs, 544 variants, 1,521 composites); (2) per-sherd records
> (site, context/dating as recorded, marks per sherd in
> sequence, and image references where available).
>
> Terms we commit to: non-commercial scholarly use only; data
> held in a local, access-controlled research store and never
> redistributed or republished; published outputs limited to
> the match register, aggregate statistics, and analysis code,
> with credit to RMRL and the Tamil Nadu State Department of
> Archaeology in the form you specify; a copy of the resulting
> register shared with the Indus Research Centre on completion.
> If a data-use agreement or a different access mechanism
> (including on-site use) is your preference, we will gladly
> follow it.
>
> Thank you for building and maintaining this resource, and for
> considering the request.
>
> Tristen Pierson
> BitConcepts LLC

## Appendix B — Feasibility sources (read 2026-10-07)

- Harappa.com, "An Indus Concordance and Tamil Potsherds, Now
  Online" (blog) and "Indus Signs and Graffiti Marks of Tamil
  Nadu" (review) — database's existence, host institution,
  scale, classification counts, and the critical counterweights.
- Rajan & Sivanantham dataset figures as reported in secondary
  coverage of the volume (15,184 reported / ~14,165 documented
  sherds; 2,107 signs = 42 + 544 + 1,521).
- RMRL (rmrl.in) — institution and Indus Research Centre
  identity; IRC Bulletin (admin@rmrl.in).
- `reports/phase107_acquisition_log.json` — license recorded as
  "TN State Dept. of Archaeology / RMRL research use"; blocker
  recorded as "Search-only web database; no bulk download
  located."
- `glossa-indus/CORPUS_VERSIONS.md` — indusscript.in license
  recorded as "user permission."
- CITATIONS.md §E.5 — Rajan & Sivanantham 2025.
