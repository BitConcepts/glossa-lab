# Spec 027 — Movement, Culture, and Language in the Greater Indus World

> ## DRAFT — PROPOSAL FOR OWNER ADJUDICATION
>
> **This draft authorizes nothing.** It does not freeze a design,
> execute a stage, acquire or copy a dataset, publish a dataset,
> move an anchor, or score PRED-2026. Every stage below requires
> owner adjudication of §13 and its own later freeze before any
> execution.
>
> Directed by the owner (Tristen Pierson) on 2026-10-10: the
> Indus program must also study movement of people as it relates
> to culture and language before, during, and after the Harappan
> period, and that study must use the RCPH-derived framework
> installed by Spec 026 — spec-kit, the AEE extension, the
> evaluator contract, stable claim IDs, origin-group accounting,
> discriminating controls, practical margins, freeze/replay
> discipline, and the framework verdict taxonomy.

**Proposed stages:** Stage 0 (gazetteer + chronology spine),
Stage 1 (Q2 repertoire gate), Stage 2 (conditional Q7/Q6) ·
**Parent:** Spec 026 (framework) and Specs 024–025 (evidence
integration and controlled follow-ups) · **Date of proposal:**
2026-10-11.

**AI disclosure:** this draft is produced by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI. The movement research report used as a design
input was also AI-produced from web sources; its uncertainty and
verification labels are carried into this draft rather than
hardened into findings.

---

## 1. Why this spec exists

The completed Indus program has tested sign-internal structure,
cross-compilation agreement, evidence coverage, context
associations, and controlled site-repertoire questions. It has
not systematically built the independent geographic and
chronological infrastructure needed to ask whether those
patterns relate to mobility, exchange, cultural transmission, or
later language history.

The design input is the 2026-10-11 research report *Population
Movement and Human Mobility in Relation to Culture and Language
in the Greater Indus World*. The report's central separation is
adopted as this spec's founding rule:

- people, genes, goods, technologies, practices, words, and
  language communities do not move as one package;
- an object's provenance licenses a claim about the object, not
  automatically a claim about people;
- ancestry does not name a language;
- later language geography is an outcome to explain, never a
  premise for a Bronze Age reconstruction;
- most proposed inscription–mobility joins are ecological
  site-level associations, not evidence about the individuals
  who made, carried, or read an object.

The report also found a practical gap: no open, site-complete,
georeferenced Indus settlement gazetteer was verified as a
download. Stage 0 therefore treats the gazetteer as a
construction deliverable, not as an existing input.

## 2. Scope

### 2.1 In scope, if adjudicated

1. **Stage 0 — descriptive infrastructure only**
   - an Indus settlement gazetteer built row by row from named
     published sources, with `source_gazetteer` on every row;
   - a chronology spine assembled from XRONOS and traced
     c14bazAAR records, with a per-date context-association and
     material audit.
2. **Stage 1 — Q2 gate test**
   - whether regional sign-repertoire variation survives
     rarefaction, object-type stratification, and the other
     controls frozen before execution; a designed negative
     closure stops all downstream repertoire-geography work.
3. **Stage 2 — conditional, separately frozen questions**
   - Q7: provenanced-material networks versus geography as
     predictors of craft-style similarity, for objects and
     techniques only;
   - Q6: whether first-appearance timing for standardisation
     traits is simultaneous, wave-like, or polycentric, only if
     the Stage 0 chronology spine can support the estimand.
4. **Registered-but-blocked questions** Q1, Q3, Q4, Q5, Q8, and
   Q9, each retained with its exact blocker and unblocking
   condition in §9. Registration is not authorization to execute
   them by a weaker substitute design.

### 2.2 Out of scope

- Any decipherment claim, sign reading, anchor movement, or
  PRED-2026 scoring.
- Use of mobility, ancestry, isotope, provenance, settlement, or
  language-geography evidence as a feature, prior, label, tuning
  target, or validation source for sign readings.
- New excavation, sampling, destructive analysis, human-remains
  work, or generation of primary isotope/aDNA data.
- Bulk copying of a source whose licence or terms have not been
  verified as reusable.
- Treating AI coding as a substitute for the human etymologists
  required by Q8.
- Publication of the gazetteer or any other output. Publication
  posture is an owner decision in §13; execution, if approved,
  still requires the program's release gate at that later time.

## 3. Governing framework

Spec 027 is governed by Spec 026 as installed methodology, not
by analogy alone.

### 3.1 Lifecycle

The lifecycle for any approved stage is:

`constitution check → specify → clarify → plan → requirements
checklist → tasks → analyze → stage freeze → H15/H23 gate →
execution → AEE assess + gaps → closeout`.

This draft completes only the proposal side of that lifecycle.
No stage in this document is frozen. A later stage freeze must
be a separate commit or PR, following the Spec 024/025 pattern,
and must name its exact phase number from the repository's
then-current global phase registry. This draft reserves no
phase number.

### 3.2 Claim register

`claims.json` in this directory is the structured register for
the claims governed by this draft. Every governed claim carries:

- a stable ID (`F027-C…`);
- one bounded proposition;
- an epistemic layer: `O`, `I`, `M`, or `Interp.`;
- a boundary;
- assumptions and `depends_on` links;
- `forbidden_assumptions` in its metadata;
- a strongest rival in its metadata;
- at least one falsification test;
- evidence records with origin groups in their metadata;
- a verdict rule in its metadata.

The register must pass the Spec 026 machinery
(`backend/glossa_lab/framework026.py`): no dependency cycles, no
missing dependencies, and no forbidden-assumption inheritance.
Renamed-equivalent assumptions remain a human review obligation;
the mechanical check is exact-match after whitespace
normalisation, as in Spec 026.

### 3.3 Verdict taxonomy

Framework verdicts are exactly:

- **INVALID** — the run or instrument cannot discriminate the
  bounded claim (including a non-discriminating control);
- **INCONCLUSIVE** — a valid design ran or was assessed, but the
  evidence, completeness grid, interval, or practical margin
  does not adjudicate the bounded claim;
- **CONTRADICTED** — a valid, discriminating test defeats the
  bounded claim under its frozen rule;
- **SUPPORTED** — a valid, discriminating test supports the
  bounded claim under its frozen rule and declared margin.

`NOT-YET-TESTABLE` is a **registration status**, not a fifth
verdict. It means no currently available evidence or design can
discriminate the claim at the stated boundary. A later verdict
may be assigned only after the named unblocking condition is met
and a design is frozen.

### 3.4 Evidence origin groups

Evidence is counted by origin group, never by database mirror
or republication.

- **Poseidon and AADR are one origin group** for any sample they
  both carry. They are alternative access and packaging routes,
  not independent corroboration.
- XRONOS is an origin group for a radiocarbon record only when
  the underlying laboratory/context record is traced; c14bazAAR
  is an aggregator route to underlying databases, not an
  additional independent origin for the same date.
- The movement research report is one secondary research origin
  for design input. It is not primary evidence for the
  archaeological, genetic, or linguistic propositions it
  summarises.
- ICIT-lineage inscription layers remain one origin group, as
  established by Specs 024–026.
- Generated assertions, including AI summaries and this draft's
  prose, are neutral governance evidence only; they do not
  corroborate an empirical claim.

## 4. Research input and uncertainty posture

The movement report is web-derived research material. Its
claim register (§0.3), dataset inventory (§7, D1–D13),
questions (§8, Q1–Q9), limits (§9), and “Could not verify” list
are design inputs. The following labels are preserved:

- Mutin et al. (2025) on Mehrgarh is **CONTESTED** and
  unreplicated. It is never silently adopted as the chronology.
- The report's Dravidian, Para-Munda, Elamo-Dravidian, Brahui,
  multilingualism, and substrate propositions remain at the
  report's bounded status. None becomes a premise in this spec.
- Several report details came from indexes or secondary
  syntheses rather than full primary texts. Any future stage
  freeze that relies on such a detail must cite and inspect the
  primary source first.
- “Could not verify” items remain blockers, not rhetorical
  gaps: no verified open Indus-wide gazetteer download; no
  verified stable bulk-open download for Law (2011) provenance
  data or the Rice Archaeobotanical Database; variable exact
  Swat sub-period counts and I6113 SNP counts by version/filter;
  biodistance and substrate details partly obtained through
  secondary summaries.

## 5. Dataset inventory and licensing posture

The report's D1–D13 inventory is adopted as a catalogue of
candidate sources, not as permission to copy them.

| ID | Candidate source | Proposed role | Draft posture |
|---|---|---|---|
| D1 | Allen Ancient DNA Resource (AADR) | Future blocked-question context; sample metadata only in this spec | Version and DOI must be pinned in any later freeze; cultural labels stored as Interp.; **one origin group with D2** |
| D2 | Poseidon archives | Alternative archaeogenetic packaging/context route | Same origin group as D1; never counted twice |
| D3 | Valentine et al. and related published isotope supplements | Q1 blocker evidence; schema/context reference | Individual published supplements only; no Indus-wide isotope corpus is claimed to exist |
| D4 | XRONOS | Stage 0 chronology-spine source | Open infrastructure; every used date traced to lab record, material, and context |
| D5 | c14bazAAR | Scripted aggregator route for D4-related databases | Aggregator, not a primary source; origin database recorded per date |
| D6 | M77 concordance and CISI | Stage 1 corpus candidates and sign-list governance | No bulk use until source terms are verified; sign-list version is a data field |
| D7 | Possehl, Law, TwoRains and published survey lists | Stage 0 gazetteer sources | Build a sourced gazetteer; do not represent the published lists as an existing open download |
| D8 | Law (2011), Kenoyer/Vidale, Meluhha compilations | Q7 provenance-network source candidates | Catalogue and rights-clear before digitisation; bulk-open status not verified |
| D9 | Archaeobotany/faunal compilations and RAD | Q4 and contextual source candidates | Paper supplements as verified; RAD access/licence not promised |
| D10 | Glottolog CLDF | Later/attested language reference only | CC BY 4.0 as reported; no Bronze Age join without an explicit temporal model |
| D11 | D-PLACE | Method/null-model reference only | Never Harappan ethnography |
| D12 | DEDR, CDIAL, SARVA | Q8 source candidates | DEDR material is copyright-restricted as reported; catalogue only without permission |
| D13 | IE-CoR | Later Indo-European linguistic reference | Attested-language depth only; no reach-back to Harappan speakers |

### 5.1 Licensing rule

For every source, Stage 0 records one of:

- `verified_open` — licence/terms inspected and reuse allowed;
- `open_access_read_only` — readable, but bulk reuse not
  verified;
- `permission_required` — not copied or redistributed without
  permission;
- `catalogue_only` — bibliographic/source metadata only;
- `unverified` — not used as data.

Anything not lawfully reusable is catalogued, not copied. A web
page being reachable is not a licence.

### 5.2 Coordinate rule

Every gazetteer row carries coordinate provenance and a
precision/restriction state:

- `exact_published` — coordinates as published for reuse;
- `approximate_published` — published at reduced precision;
- `derived_centroid` — derived from a named published extent or
  locality, with method recorded;
- `restricted` — a more precise location is known from a source
  but is not republished in the gazetteer;
- `unknown` — no defensible coordinate.

No restricted coordinate is made more precise by inference,
geocoding a modern namesake, or combining sources to defeat a
source's restriction.

## 6. Stage 0 — Gazetteer and chronology spine (descriptive only)

### 6.1 Purpose

Stage 0 builds the minimum independent infrastructure that any
later movement, culture, or repertoire-geography question needs:
which places are in the record, under which source's period
scheme, where they can defensibly be located, and which dated
contexts can support chronological reasoning.

Stage 0 produces **no movement finding, no culture finding, no
language finding, and no repertoire finding**. Its outputs are
descriptive infrastructure with provenance.

### 6.2 Gazetteer unit and required fields

The unit is one **source assertion about a site**, not a merged
claim that all sources agree. Rows may later be clustered under
a program `site_id`, but clustering never deletes the source
rows or their disagreements.

Required fields:

- `gazetteer_row_id` (stable, source-scoped);
- `program_site_id` (nullable until an adjudicated clustering
  rule is frozen);
- `site_name_as_published`;
- `site_name_normalised` (nullable; normalisation rule recorded);
- `source_gazetteer` (Possehl, Law, TwoRains, another named
  published source, or a later approved source);
- `source_citation` and `source_locator` (page/table/record);
- `period_label_as_published`;
- `period_scheme` (the source's scheme, not a silent universal
  chronology);
- `program_period_assignment` (nullable; mapping rule and
  reviewer recorded when present);
- `site_size_as_published` and unit, where present;
- `survey_or_excavation_basis`, where present;
- latitude/longitude or a null coordinate;
- `coordinate_state` (§5.2);
- `coordinate_source` and precision in metres or a qualitative
  published precision class;
- `licence_state` (§5.1);
- `notes` for ambiguity, duplicate names, and source conflicts.

Possehl's and Law's published lists are sources to be
transcribed or transformed only to the extent their terms
allow. If a list may be read but not lawfully redistributed,
Stage 0 catalogues its coverage and stores only the fields or
derived records the adjudicated posture permits.

### 6.3 Gazetteer completeness and conflicts

Stage 0 must report, by source:

- rows catalogued, rows lawfully reusable, rows excluded by
  licence, rows with usable coordinates, and rows by published
  period scheme;
- duplicate-name clusters and same-name/different-place risks;
- source disagreements on period, size, and location;
- geographic and survey-intensity bias. A blank region in the
  gazetteer is a coverage statement, not evidence that no sites
  existed there.

No majority vote silently resolves conflicting source rows.
The clustering rule, if any, is a governed claim with its own
falsifier: a demonstrated same-site split or different-site
merge defeats the affected cluster, not merely annotates it.

### 6.4 Chronology spine unit and required fields

The unit is one dated sample/context assertion. Required
fields:

- `chronology_row_id`;
- `program_site_id` and `site_name_as_published`;
- laboratory code, where available;
- dated material (`charcoal`, `bone`, `tooth_enamel`, seed or
  other short-lived sample, shell, sediment, other, unknown);
- context description and context-association grade:
  - `direct` — the dated material is the event/context claimed;
  - `associated` — stratigraphically associated, with the link
    stated;
  - `residual_or_intrusive_risk` — association is disputed or
    insecure;
  - `unassessed` — the source does not support grading yet;
- conventional radiocarbon age and error, or the source's
  reported age form;
- calibration curve/version and calibrated range, if computed;
- source database (`XRONOS`, or the underlying database reached
  through c14bazAAR), source record ID, and retrieval version;
- publication citation;
- `old_wood_risk` for charcoal and other long-lived material;
- `short_lived_sample` boolean or `unknown`;
- `licence_state` and origin-group ID.

An aggregate site date with no sample/context trace is not a
chronology-spine row. It may be catalogued as a published period
assertion in the gazetteer, but it cannot support Q6 timing.

### 6.5 Chronology scenarios and contested dates

The spine preserves competing chronology assertions. It does
not choose a single chronology by deleting a rival.

For Mehrgarh, at minimum:

- the older charcoal-based Period I chronology remains a source
  assertion with its old-wood/context risks stated;
- Mutin et al. (2025) remains a **CONTESTED** source assertion,
  based in the research report on enamel dates and an
  unreplicated revision;
- any analysis that needs one chronology must name the scenario
  it uses and report the rival scenario as a sensitivity or
  declare the question not-yet-testable under disagreement.

### 6.6 Stage 0 exit criteria

Stage 0 can close only when:

1. every gazetteer and chronology row has source, licence, and
   origin-group fields;
2. every chronology row has a context-association grade or is
   explicitly `unassessed`;
3. coordinate precision/restriction is recorded for every
   gazetteer row;
4. source-conflict and coverage-bias reports are complete;
5. the claim-register integrity check passes;
6. a descriptive report states what the infrastructure can and
   cannot support, question by question (Q1–Q9).

Failure of a source's licence or traceability does not fail
Stage 0 if the source is honestly catalogued and excluded.
Inventing coverage to avoid that outcome would make the stage
INVALID.

## 7. Stage 1 — Q2, the repertoire gate

### 7.1 Bounded question

**Q2:** After rarefaction to a common sample size and
stratification by object type, does site explain more
sign-repertoire variation than expected under permuted site
labels, net of the frozen preservation, medium/context, period,
and corpus-size rules?

The bounded claim is about **recorded sign repertoires in a
named corpus under a named sign list**. It is not a claim about
spoken dialects, ethnic groups, political units, workshops as
peoples, or the language of the Indus script.

### 7.2 Why Q2 comes before every downstream repertoire question

Specs 024–026 establish that site-repertoire associations can
be computed on an ICIT-lineage layer, but also that composition,
preservation, chronology, and corpus construction can carry the
apparent pattern. Q2 is therefore the gate, not a preliminary
version of Q1:

- if Q2's null is not rejected under a valid frozen design, all
  Q1-style repertoire-geography work under this spec stops;
- that negative closure is a successful outcome;
- no network, mobility, material, or language interpretation
  may be attached to a Q2 failure;
- a Q2 pass licenses only a **separate proposal and freeze**
  for downstream work. It does not itself authorize Q1.

### 7.3 Unit, variables, and estimand

- **Unit:** site, with site-period used only where both the
  corpus and Stage 0 chronology support the same period scheme
  without silent harmonisation.
- **Response:** sign-repertoire composition under the governing
  sign list selected in §13.
- **Primary grouping:** site.
- **Strata/controls:** object type; medium and context type
  where recorded; preservation/legibility; period scheme where
  eligible; inscription length class where the frozen design
  states it.
- **Effect:** a frozen repertoire-divergence estimand and a
  practical margin declared before outcome data are examined.
  The Spec 026 convention of reporting an effect and interval
  beside any permutation result applies. A p-value alone cannot
  produce SUPPORTED.
- **Rarefaction:** repeated rarefaction to the frozen common
  sample size within eligible strata, with the seed, number of
  draws, handling of strata below the common size, and pooling
  rule fixed in the Stage 1 freeze.
- **Permutation null:** site labels permuted only within strata
  in which labels are exchangeable under the frozen design.
  Rows in non-permutable strata are reported and excluded from
  the effective N, never silently retained.
- **Jackknife:** leave-one-site-out over every eligible site,
  with corpus-dominant sites named in the report. An effect
  whose direction or margin status depends on one site is not
  reported as a general regional pattern.

### 7.4 Corpus rules that must be pinned before execution

The Stage 1 freeze must state all of the following. Section 13
asks the owner to select the governing choices; the freeze may
not change them silently.

1. **Governing sign list.** Exactly one of M77, Parpola/CISI, or
   the Wells/ICIT-native numbering governs the primary test.
   `sign_list_version` is a field on every record. M77, Parpola,
   and Wells sign numbers are **not interchangeable**.
2. **Crosswalks.** A crosswalk may define a separately labelled
   sensitivity only where the mapping is recorded sign by sign.
   An ambiguous or many-to-many mapping is not resolved by a
   silent pick.
3. **Object inclusion.** Provenance/site eligibility, object
   types included, and whether pottery graffiti are pooled or
   held as their own stratum. The draft's proposed default is
   **not pooled** with seals/tablets in the primary test.
4. **Damage and legibility.** Damaged objects and multi-line
   texts are included or excluded by an explicit rule, with
   flags retained. The draft's proposed default is to include a
   damaged/multi-line object only when its recorded sequence
   meets the frozen minimum legible-token rule, and to run the
   opposite inclusion state as a labelled sensitivity if the
   freeze so declares.
5. **Duplicates.** Duplicate texts and duplicate records are
   distinguished. The program's existing deduplication rule is
   named by artifact/version; a duplicate text is not assumed
   to be a duplicate object.
6. **Unmapped signs.** Signs absent from the governing list are
   retained as `UNMAPPED`, pooled only under a frozen rule, or
   excluded — one rule, stated in advance.
7. **Minimum cell support.** Minimum inscriptions/tokens per
   site and stratum, treatment of signs below a frequency
   threshold, and the completeness grid are declared before
   execution. Missing cells are INCONCLUSIVE for the affected
   estimand, never pooled away after the fact.
8. **Corpus lineage.** The corpus origin group is named in every
   headline. A second compilation is a sensitivity or witness,
   not independent corroboration, unless its origin independence
   is separately established.

### 7.5 Discriminating controls

Stage 1 is INVALID if its controls cannot discriminate:

- **Negative control:** a label-shuffled or synthetic
  homogeneous repertoire with the same stratum sizes must not
  produce the claimed site effect at the frozen rule.
- **Positive control:** a synthetic planted site effect of the
  declared practical size, passed through the same rarefaction
  and stratification pipeline, must be detectable at the frozen
  rule.
- **Composition control:** the primary result must be reported
  within at least one single-object-type stratum if the
  completeness grid supports it; otherwise that limitation is
  part of the verdict, not a footnote after a pooled claim.

A control failure is not a caveat on a result. It makes the run
INVALID under Spec 026.

### 7.6 Stage 1 verdict rules

- **SUPPORTED:** the frozen primary estimand is estimable, the
  controls discriminate, the permutation rule rejects the null,
  and the effect interval lies on the support side of the
  declared practical margin under the frozen interval rule.
- **CONTRADICTED:** the frozen primary estimand is estimable,
  the controls discriminate, and the frozen null is not
  rejected, or the interval lies on the null side of the
  declared margin under the frozen rule. The bounded repertoire
  claim is defeated and §7.2's negative closure applies.
- **INCONCLUSIVE:** the design is valid but the completeness
  grid, interval, jackknife, or sensitivity pattern does not
  adjudicate the bounded claim at the declared margin.
- **INVALID:** a control cannot discriminate, corpus lineage or
  sign-list identity is compromised, a frozen rule is changed
  after outcome inspection, or the pipeline cannot reproduce
  its own population from the frozen corpus definition.

No Stage 1 outcome identifies a dialect or a language.

## 8. Stage 2 — Conditional questions

Stage 2 is not a package. Q7 and Q6 have different evidence,
different estimands, and different failure modes. Each requires
its own freeze, its own claim subset, and its own completion or
negative closure.

### 8.1 Q7 — Provenanced-material networks and craft style

**Bounded question:** Do site pairs that share provenanced
material sources show greater ceramic or bead/craft-technique
similarity than expected from geographic and river-network
distance alone?

- **Unit:** site pair.
- **Predictor:** shared geological/provenance source, with the
  provenance method recorded per link (visual, petrography,
  INAA, LA-ICP-MS, Pb isotopes, or another named method).
- **Responses:** separately modelled ceramic similarity and
  bead/craft-technique similarity. They are not pooled into a
  single “culture” score.
- **Controls:** geographic distance, river-network distance,
  period eligibility, site sample size, and publication/
  excavation intensity where measurable.
- **Null:** geography and river distance explain all shared
  variance; source-sharing adds no predictive power.
- **Falsifier:** source-sharing adds no predictive power, or
  its effect is not robust to the frozen site jackknife.
- **Licensed conclusion:** a statement about objects,
  materials, and techniques only. Neither outcome licenses a
  claim that people migrated, that a workshop population moved,
  or that a language spread.

Q7 may be frozen only after Stage 0 and after the D8 source/
licence audit establishes which provenance links are lawfully
and traceably usable.

### 8.2 Q6 — Timing of standardisation

**Bounded question:** Are first-appearance dates for frozen
standardisation traits simultaneous within dating uncertainty,
distance-decayed in a wave-like pattern, or region-first in a
polycentric pattern?

Candidate traits are limited to traits whose first appearance
can be tied to a Stage 0 chronology row: standard weights,
brick ratio, seal/sign use, and planned drainage/layout where
the context evidence supports a date. A trait with only a broad
period label is not a timing observation.

Stage 0 supports Q6 only if its future freeze can show, before
outcomes are examined:

- enough independent sites in at least the frozen minimum
  number of regions;
- dates with direct or associated context grades adequate for
  the timing model;
- uncertainty intervals narrow enough that simultaneous and
  wave-like rivals predict materially different patterns;
- a declared Bayesian or equivalent timing model, its priors,
  and a posterior/predictive threshold for each rival.

If those conditions fail, Q6 remains NOT-YET-TESTABLE. A
period-label co-occurrence table is not a substitute timing
test.

### 8.3 Stage 2 separation from Q1

A Q7 network result is not the mobility/exchange arm of Q1.
A Q6 timing result is not evidence that administrators,
migrants, or speakers carried a trait. Either result may inform
a later proposal, but neither upgrades Q1 from its blocked
state and neither enters a sign-reading model.

## 9. Registered-but-blocked questions

Registration preserves the question and the reason it cannot
currently be answered. It does not authorize an easier question
under the same number.

| Question | Exact blocker | Data condition that would unblock it | Strongest honest status now |
|---|---|---|---|
| **Q1 — Mobility arm:** does sign-repertoire variation track independently measured mobility, net of geography, chronology, object type, sampling, and reporting? | Published individual-level isotope/aDNA coverage is available for **≤3 relevant sites** in the design input, while the inscription corpus spans many more; inscribed objects and sampled individuals are almost never the same people/objects. The mobility arm therefore has too few independent site-period observations and a direct ecological-fallacy exposure. | A lawful, traceable site-period mobility dataset covering the frozen minimum number of independent inscription-bearing sites, with local isotope baselines and period linkage; plus a frozen ecological-estimand design that does not upgrade site association to individual carriage. The exchange-only part may be redesigned separately, but it may not be relabelled the mobility arm. | **NOT-YET-TESTABLE as designed** |
| **Q3 — Cemetery H / early PGW incoming people?** | The decisive design needs paired isotope and, where recoverable, aDNA observations on the same Cemetery H / earliest PGW-associated remains, compared with same-catchment Mature Harappan baselines and local fauna/water baselines. Those paired primary data are not in hand and this program cannot generate them. | New or newly released primary paired data meeting a future frozen sample-size/power rule, with context, preservation, and catchment baselines documented. Cremation-related preservation failure below the frozen threshold leaves the question not-yet-testable; it does not prove continuity. | **NOT-YET-TESTABLE** |
| **Q4 — Late Harappan eastward shift: movement or in-place crop adaptation?** | The full design needs linked archaeobotanical spectra, direct crop dates, settlement foundation/abandonment timing, and human dietary isotopes across at least three independent site clusters. Bone preservation in parts of the relevant region is poor, and the linked dataset is not assembled. | Either the full linked dataset, or a separately frozen fallback using faunal isotopes plus settlement chronometry. The fallback has a **weaker verdict ceiling**: it may support or contradict a bounded settlement/subsistence pattern, but it cannot by itself identify population movement. | **REGISTERED-BLOCKED; fallback requires its own freeze and weaker ceiling** |
| **Q5 — Mehrgarh farming diffusion and chronology replication** | The question turns on primary chronology from sealed Neolithic contexts — replicated enamel/short-lived-sample dates, context records, and preferably a west→east first-appearance transect. This program has no such primary dataset. Mutin et al. (2025) is a single, unreplicated revision in the design input. | Independent replication or refutation from sealed contexts using short-lived/enamel samples, with full context publication; for the demic-versus-diffusion form, discriminating Neolithic genomic or equally direct evidence would also be required. | **NOT-YET-TESTABLE by this program; Mutin et al. CONTESTED** |
| **Q8 — Substrate stratigraphy** | Etymology coding is judgement-laden and the discriminating instrument is blind coding by **at least two qualified human etymologists**, with a pre-registered agreement threshold. AI coding is not a substitute — a single model family or correlated AI coders would be one origin group and cannot supply the independent human judgement the design tests. The program has no such coder panel. | A recruited panel of at least two qualified human etymologists, coding independently and blind to the hypothesis allocation, under a frozen word list, donor taxonomy, agreement statistic, and adjudication rule. If agreement is below the frozen threshold, the valid result is that substrate stratigraphy is not currently a discriminating instrument. | **NOT-YET-TESTABLE** |
| **Q9 — Brahui discriminator** | The proposed discriminator depends on loanword stratigraphy, shared North Dravidian innovations, dated attestations, and Baluchistan toponymy. There are no pre-modern Brahui texts in the design input (earliest literature c. 18th century), and no currently stated observation may discriminate relic survival from later arrival at the required standard. Genetics cannot substitute: Brahui speakers' admixture history is not their language's arrival date. | A future linguistic design that names, before coding, an observation or combination of observations whose expected pattern differs materially under relic versus later-arrival models and survives independent expert review. Until then, no weaker proxy is promoted to a discriminator. | **MAY BE NOT-YET-TESTABLE; that possibility is declared in advance** |

No blocked question may be “unblocked” by lowering its unit,
substituting modern geography, using AI in place of the named
human evidence, pooling unlike evidence, or changing its claim
after seeing a convenient result. Unblocking is a new freeze
with the changed data condition evidenced.

## 10. Hard limits

The following are stop conditions, not discussion points.

1. **No gene→language identification.** No ancestry component,
   haplogroup, admixture date, isotope profile, or burial group
   names a language or language family.
2. **No ethnic labels projected backward.** “Aryan”,
   “Dravidian” as a people/race, “Harappan ethnicity”, caste, or
   any modern ethnonym may not be attached to genomes,
   skeletons, pots, seals, sites, or sign repertoires. Language
   family names may be used only for languages, with dates.
3. **No object→mass-migration inference.** A provenanced object
   licenses a claim about that object and, with an appropriate
   assemblage, about exchange or production. It does not by
   itself license population movement and never, alone, mass
   migration.
4. **No later text as a Harappan transcript.** Later Vedic,
   Avestan, Sangam, Mesopotamian, or other texts are evidence
   for their own worlds and contacts. They are not transcripts
   of what Harappans said, believed, or called themselves.
5. **Absolute PRED/decipherment fence.** Mobility, ancestry,
   isotope, provenance, settlement, chronology, or later
   language evidence may never enter sign-reading features,
   priors, labels, tuning, validation, anchor decisions, or
   PRED-2026 scoring.
6. **No package deals.** Crops, animals, metals, burial rites,
   genes, words, technologies, and practices each require their
   own claim, date, evidence, rival, and falsifier.
7. **No teleology joins.** Modern or later language geography
   is an outcome to explain, never a premise. Any join between a
   later language distribution and Bronze Age sites requires an
   explicit temporal model plus language shift and language loss
   as live rivals.
8. **No silent model-shopping.** Every model variant tried is
   reported, including source populations, corpus exclusions,
   sign-list version, gazetteer version, chronology scenario,
   rejected specifications, and negative controls.
9. **No absence upgrades.** Missing genomes, missing sites,
   missing inscriptions, or a missing destruction horizon prove
   only the bounded absence in the sampled record, not a
   universal historical negative.
10. **No AI substitution for named human evidence.** This is
    absolute for Q8 and applies wherever a future freeze names
    independent human coding as the instrument.
11. **No licence laundering.** A dataset does not become open
    because it was scraped, mirrored, summarised by another
    project, or included in an aggregator.
12. **No anchor contact.** Nothing in this spec moves, promotes,
    demotes, or revalidates an anchor. Any unexpected bearing on
    an anchor is reported to the owner as a separate assessment;
    it is never actioned inside this spec.

## 11. Requirements

- **FR-027-1 — Claim governance.** Every governed claim is in
  `claims.json` with the §3.2 fields and passes the Spec 026
  integrity check before a stage freeze.
- **FR-027-2 — Gazetteer.** Stage 0 produces a source-asserted
  settlement gazetteer satisfying §6.2–§6.3, with licensing and
  coordinate states on every row.
- **FR-027-3 — Chronology spine.** Stage 0 produces a traced
  dated-sample/context spine satisfying §6.4–§6.5; aggregate
  period labels are not promoted to timing observations.
- **FR-027-4 — Stage 0 neutrality.** Stage 0 reports coverage,
  conflicts, and fitness-for-question only. It mints no movement,
  culture, language, or repertoire verdict.
- **FR-027-5 — Q2 gate.** Stage 1 tests Q2 under a frozen corpus
  and design satisfying §7.3–§7.6. A valid non-rejection applies
  the negative closure automatically.
- **FR-027-6 — Sign-list integrity.** Every Stage 1 record
  carries its sign-list version. No primary analysis mixes sign
  lists or silently resolves crosswalk ambiguity.
- **FR-027-7 — Discriminating controls.** Every confirmatory
  stage names positive and negative controls in its freeze. A
  non-discriminating control makes the run INVALID.
- **FR-027-8 — Q7 separation.** Q7, if frozen, models material
  and technique outcomes separately and licenses no people or
  language claim.
- **FR-027-9 — Q6 estimability.** Q6 may freeze only after the
  §8.2 support conditions are evidenced from Stage 0 margins
  and metadata, without inspecting trait-timing outcomes.
- **FR-027-10 — Blocked-question fidelity.** Q1, Q3, Q4, Q5,
  Q8, and Q9 remain registered with §9's blockers. No substitute
  design inherits their numbers or claims.
- **FR-027-11 — Origin-group accounting.** Poseidon/AADR count
  once for shared samples; aggregators do not create new origin
  groups; derivative inscription layers are labelled by lineage.
- **FR-027-12 — Freeze and replay.** Each stage freeze records
  the canonical definition, input hashes, versions, seeds,
  environment, practical margins, and completeness grid before
  outcome data are examined. A changed gate is a new version and
  a new freeze.
- **FR-027-13 — Graph-first execution.** Any future numbered
  research phase follows H15/H23 in order: script, graph module,
  registration, registration verification, then run. No phase
  script runs before its graph node exists.
- **FR-027-14 — AEE lifecycle evidence.** AEE assess and the
  evaluator-contract result are saved after specify, plan, and
  tasks for this draft, and after every later stage's
  corresponding lifecycle steps. Any outcome stricter than
  `warn` is a drafting or stage-closure blocker until the named
  recovery work is recorded.
- **FR-027-15 — No-contact boundary.** Execution under this
  spec, if later authorized, changes no anchor and performs no
  PRED-2026 scoring.

## 12. Epistemic boundaries (H13)

**Assumptions declared:**

- The movement research report is a faithful enough design
  input when its hedges are preserved; it is not treated as a
  primary source.
- Published gazetteer and chronology sources can be catalogued
  with enough provenance to distinguish lawful reuse from
  catalogue-only access. Where they cannot, the row is excluded.
- A site-period join is ecological unless the same object or
  individual supplies both sides of the join.
- Practical margins are conventions declared before outcomes,
  not discoveries from the data.
- AEE outcomes are governance signals, not probabilities that a
  historical proposition is true.

**Adversarial challenges that could break the program:**

- A gazetteer that merges source assertions so aggressively
  that it manufactures a false site universe.
- A chronology spine that treats charcoal association as direct
  dating, or silently adopts the contested Mehrgarh revision.
- A sign corpus whose sign-list or exclusion rules recreate the
  regional pattern being tested.
- A network analysis that converts shared materials into a
  people-movement claim through language drift in the report.
- A later linguistic distribution used, explicitly or through
  feature construction, as the answer to a Bronze Age question.
- Correlated databases or AI coders counted as independent
  evidence.

**Belief artifacts relied on:** Spec 026's framework records;
Specs 024–025's lineage and covariate records; the program's
existing corpus/deduplication artifacts as named in a future
freeze; and the movement report as a secondary design input.
No P1 belief artifact below MEDIUM confidence is load-bearing
for a verdict in this draft, because this draft issues no
verdict.

## 13. Decision asks for owner adjudication

The owner is asked to answer the following. Until then, this
spec remains a draft and no stage is authorized.

### Ask 1 — Stage order and Stage 0 scope

Approve the order **Stage 0 → Stage 1 gate → conditional
Stage 2**, and choose Stage 0's scope:

- **0A (draft recommendation):** gazetteer and chronology spine
  in one Stage 0, because Q6 and any defensible site-period work
  need both; or
- **0B:** gazetteer first, chronology spine as a separate later
  stage; or
- **0C:** do not proceed with Stage 0.

### Ask 2 — Q2 governing sign list

Choose exactly one governing sign list for the Stage 1 primary
test:

- **M77** (Mahadevan numbering);
- **Parpola/CISI** numbering; or
- **Wells/ICIT-native** numbering.

A second list may be named only as a separately labelled
sensitivity with a sign-by-sign crosswalk rule.

### Ask 3 — Q2 corpus inclusion rules

Approve or amend the draft's proposed primary rules:

- provenanced records only;
- pottery graffiti **not pooled** with seals/tablets in the
  primary test;
- damaged and multi-line objects included only when the frozen
  minimum legible-token rule is met, with their flags retained;
- duplicate records removed under the named program
  deduplication artifact, while duplicate texts on distinct
  objects are retained as distinct objects;
- unmapped signs retained as `UNMAPPED` under one frozen pooling
  rule;
- site/stratum minimum-support and frequency rules fixed in
  the Stage 1 freeze before outcomes are examined.

### Ask 4 — Gazetteer licensing and publication posture

Choose the posture for any completed Stage 0 gazetteer:

- **CC BY 4.0 publication through the program release gate**,
  limited to lawfully reusable rows and with restricted
  coordinates never published more precisely than their source
  state allows; or
- **repo-local / repository-only retention**, with no external
  publication, even for lawfully reusable rows.

Catalogue-only and permission-required sources are excluded
from publication under either choice.

### Ask 5 — Stage 1 execution timing

After owner adjudication and completion of Stage 0, choose:

- **Stage 1 executes on the adjudicated design** once its own
  freeze is committed and merged; or
- **Stage 1 returns for a separate owner go** after the Stage 0
  report, even if this spec is otherwise adjudicated.

## 14. Lifecycle record for this draft

- Constitution check: performed against constitution §§I–VIII
  and governance H2, H6, H13, and H15. The draft is a proposal
  only (H2), states its boundaries (H13), expands no execution
  scope (H6), and defers all experiment execution to future
  graph-first freezes (H15/H23).
- Clarify: the unresolved choices are not hidden assumptions;
  they are the explicit owner asks in §13.
- AEE/evaluator lifecycle outputs: saved under `aee/` for
  after-specify, after-plan, and after-tasks. Final outcomes
  are **pass** at all three phases (33 claims, 0 failure modes,
  0 claims below the 0.70 threshold); the specify-stage rounds
  and recovery are recorded in `aee/recovery-specify.md`, and
  the composed strict evaluator outcome after tasks is `pass`.
  These outcomes govern whether this draft is ready for owner
  adjudication; they do not adjudicate it.
- Analyze: `plan.md`, `tasks.md`, and
  `checklists/requirements.md` are cross-checked against
  FR-027-1…15 before the draft PR is opened.
