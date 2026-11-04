# Taxonomy v0 draft — Spec 088 (for ratification as program-map-taxonomy v1)

Drafted 2026-11-04 from first-hand counts: the spec tree of the clone
(`specs/`, 88 directories, every one with a `spec.md`; titles below are
each spec's own first line) and the ledger
(`glossa-indus/ledger/claims.jsonl`, 857 claim entries). Ratifying this
draft is part of the owner's package approval (T003); on adoption it is
filed, with any owner amendments, as `program-map-taxonomy v1`
(plan.md, T102).

## 1. The file shape (mirrors RCPH's taxonomy.json, minus `curated`)

```json
{
  "version": "program-map-taxonomy v1",
  "note": "Curated study/claim assignments for the generated program map. Grouping only: this file carries no standings (C2). Changes are amendment acts (new version, recorded in the stage record).",
  "domains": ["Sign inventory & corpus", "Anchors & readings",
              "Claim families by study line",
              "Contact zone & external corpora", "Program infrastructure"],
  "subdomains": { "<domain>": ["<subdomain>", "..."] },
  "studies": [
    { "spec_dir": "054-yadav-opening-closing",
      "domain": "Claim families by study line",
      "subdomain": "Source-thesis tests (D-designs)" }
  ],
  "extracted_documents": [
    { "document": "farmer_sproat_witzel_2004",
      "domain": "Claim families by study line",
      "subdomain": "Source-thesis tests (D-designs)" }
  ],
  "restricted": ["072-fish-family-profiles-redesign"]
}
```

Deliberate divergences from RCPH's file, both from the adoption
constraints: **there is no `curated` object and no standing/status field
anywhere in the format** (C2 — RCPH's curated standings are not adopted);
and assignments are stated per study directory rather than per grouped
node, because Glossa's nodes are individual (D-088-1).

## 2. Assignment rules

- **Studies.** Every spec directory is assigned to exactly one domain and
  one subdomain of that domain (the table in §3). The builder fails on a
  directory with no assignment, an assignment naming no directory, or a
  subdomain not declared under its domain (C088-2, C088-9).
- **Bundle claims.** A claim inherits the domain/subdomain of its study:
  the spec directory named in its ledger `sources[]` (membership rule,
  program-map-defs v1). A bundle claim whose sources name more than one
  spec directory — none exist today — would be a build-time judgment call
  for the build record, not a silent pick; the defs register the primary
  source (first `sources[]` entry carrying a `spec`) as the default.
- **Extracted claims (23).** Extracted claims belong to no study. Each is
  assigned by its source document (§4) to the subdomain of the study line
  that tests that document's claims, where one exists.
- **Restricted.** A directory in `restricted` renders name-only in every
  generated surface (C088-19). V1 population: exactly
  `072-fish-family-profiles-redesign` ("executed — held under the Roif
  gate").
- **Amendments.** Changing any assignment, adding a domain/subdomain, or
  adding a restricted entry is a new taxonomy version, recorded in the
  stage record in the same motion (C088-9).

## 3. Study assignments — all 88 spec directories

Counted 2026-11-04. Domain totals: Sign inventory & corpus 17 ·
Anchors & readings 13 · Claim families by study line 40 · Contact zone &
external corpora 2 · Program infrastructure 16. **Total: 88.**

### Domain 1 — Sign inventory & corpus (17)

*Corpus, catalogue & transcription builds (4)*

| Spec dir | Title |
|---|---|
| 023-keyed-transcription-layer | Keyed Transcription Layer over CISI Vols. 1–2 |
| 037-cisi31-concordance-spine | CISI 3.1 Concordance Spine and HARP Provenance Annex |
| 066-phase130-catalogue-extension | Phase-130 Catalogue Extension: CISI Vol. 3.1 Portion Objects into the Pinned Catalogue Layer |
| 073-keying-surface-repair | Repairing the Keying Surface: Registry Wells Coverage and a Second Depicted-Kind Classification |

*Cross-compilation comparisons (8)*

| Spec dir | Title |
|---|---|
| 015-phase116-corpus-harmonization | Phase-116: Corpus-Harmonization Study — Why Holdat and ICIT Positional Profiles Disagree |
| 019-phase125-cross-compilation-positional | Phase-125: Cross-Compilation Positional Comparison — mayig/CISI Layer vs Holdat Compilation |
| 020-soviet-pred-adjudication | Adjudication: Does the Soviet Positional Dataset (Kondratov 1965) Qualify as an Evaluation Source for PRED-2026-001/002? |
| 021-phase127-cross-compilation-diagnostic | Phase-127: Cross-Compilation Disagreement Diagnostic |
| 021-phase130-intake-pack | Phase-130: Independent-Data Intake Pack |
| 022-phase131-attribution | Phase-131: Source-of-Disagreement Attribution for the Phase-125/127 Result |
| 034-matched-object-attribution | Why the Two Compilations Disagree: A Matched-Object Attribution |
| 058-transcription-disagreement-mechanism | What Drove the Spec 023 Transcription Disagreement (Design D-21) |

*Signary & corpus models (3)*

| Spec dir | Title |
|---|---|
| 076-projected-constraint-corpus-model | The Projected-Constraint Corpus Model |
| 077-signary-triangulation | Three-Witness Sign-List Triangulation + Token 999 (Method M7) |
| 078-projected-constraint-bridge-redesign | The Bridge Redesign: A Two-Axis Vocabulary for the Corpus Model (Method M13) |

*Site & chronology data (2)*

| Spec dir | Title |
|---|---|
| 030-q6-chronology-spine-extension | Q6 Chronology-Spine Extension |
| 039-gazetteer-period-assignment | Gazetteer Period Assignment: the Spec 027 §6.2 Act |

### Domain 2 — Anchors & readings (13)

*Anchor provenance, Phases 52–110 (4)*

| Spec dir | Title |
|---|---|
| 004-indus-executable-package | Indus Executable Package (Phase-52 SA run, crosswalk expansion, anchors reconciliation) |
| 005-phase52-v2 | Phase-52 v2: Held-Out Validation, Blind Controls, Constraint Ablation |
| 006-anchor-provenance-audit | Anchor Provenance Audit: What the 287 Anchors Rest On after Phase-107 |
| 007-phase109-follow-through | Phase-109 Follow-Through: Executing the Phase-108 Audit's Recommendations |

*Validation batteries for the SA-lineage anchors, Phases 111–119 (8)*

| Spec dir | Title |
|---|---|
| 009-phase111-blind-affiliation | Phase-111: Blind Language-Affiliation Study |
| 010-phase112-blind-affiliation | Phase-112: Blind Language-Affiliation Study, Order-Carrying Features |
| 011-phase113-nonsa44-validation | Phase-113: Non-SA Validation Battery for the 44 SA-Lineage Anchors |
| 012-phase113-blind-affiliation | Phase-113: Blind Language-Affiliation Study, Adversarial Protocol |
| 014-phase115-nonsa44-validation-v2 | Phase-115: Non-SA Validation Battery v2 for the 44 SA-Lineage Anchors |
| 016-phase117-within-compilation-validation | Phase-117: Within-Compilation Validation Battery for the 44 Flagged Anchors |
| 017-phase118-within-compilation-validation-v2 | Phase-118: Within-Compilation Validation Battery v2 (W1-Primary, Cross-Fit W3) |
| 018-phase119-pred2026-readiness | Phase-119: PRED-2026 Readiness — the Pre-Registered Prediction Evaluation Harness |

*Single-anchor adjudications (1)*

| Spec dir | Title |
|---|---|
| 008-m222-adjudication | Phase-110: M222 / 'kur' Adjudication + OSF Registry Link |

### Domain 3 — Claim families by study line (40)

*Source-thesis tests, the D-designs (23)*

| Spec dir | Title |
|---|---|
| 044-fish-sign-coastal-residue | The Fish Sign and the Ports, Tested Sign by Sign (D-02) |
| 045-hunt-depicted-kinds | Hunt's Three Parts: Pattern, or Meanings? (D-05) |
| 046-horned-tiger-concordance | "Sign 297 Is the Horned Tiger": an Identification Concordance (D-18) |
| 047-roif-ledger-distribution | Roif's Ledger Thesis: the Distribution Test (D-09) |
| 048-parpola-fish-family-profiles | Parpola's Fish-Sign Family, Sign by Sign (D-04) |
| 050-hunt-sky-signs-endings | Hunt: Sky Signs at the Ends of Texts (D-13) |
| 051-roif-arrow-sign | Roif: the Arrow Sign — Border Marker, or City Sign? (D-10) |
| 052-farmer-not-writing-soviet | Farmer's "Not Writing at All" Thesis: the Soviet-Compilation Consistency Check (D-01) |
| 053-yadav-zipf-controls | Yadav's Zipf Fit: What Is a Curve Fit Worth? (D-07) |
| 054-yadav-opening-closing | Yadav's Opening/Closing Signs: Given a Falsifier, Then Rerun (D-08) |
| 055-sign900-numeral | "Sign 900 Means Six": Identify the Sign, Then Test It as a Numeral (D-15) |
| 056-sign821-recovery | "Sign 821, Used in a Variety of Contexts": Recover the Argument, or Retire the Fragment (D-17) |
| 057-five-sources-heading | The Heading Carried by Five Sources (D-19) |
| 063-sign821-identification-successor | Sign 821, Identification Successor to Spec 056 |
| 064-sign297-concordance-successor | "Sign 297 Is the Horned Tiger": Concordance, Successor to Spec 046 |
| 065-s1-s5-heading-successor | The Two Unlocated Rows of Spec 057 (Successor Recovery Act) |
| 068-yadav-zipf-controls-successor | Yadav's Zipf Fit — Successor on the Shakti Corpus (Amendment S-053) |
| 069-hunt-asset-a | Hunt Depicted-Kind Classification: The Asset A Build (Contract of Spec 045) |
| 070-hunt-opening-signs-successor | Hunt Opening Signs Successor, on the Shakti Corpus (Successor to Spec 049, D-06) |
| 071-hunt-sky-signs-successor | Hunt Sky-Signs Endings Successor, on the Shakti Corpus (D-13) |
| 072-fish-family-profiles-redesign | Parpola's Fish-Sign Family in ICIT Numbering on the Shakti Corpus — **restricted: name-only** ("executed — held under the Roif gate") |
| 074-hunt-opening-signs-repaired-surface | Hunt Opening Signs on the Repaired Keying Surface (Successor to Spec 070, D-06) |
| 075-depicted-kind-endings-atlas | Depicted-Kind Endings Atlas, on the Shakti Corpus (Phase 441) |

*Site, object & repertoire tests (12)*

| Spec dir | Title |
|---|---|
| 024-evidence-integration | Evidence Integration: Tying the Inscriptions to Non-Textual Evidence |
| 028-harappa-robustness | Harappa Robustness: Is the Repertoire Site Effect Independent of Its Largest Site? |
| 031-stage2-q7-provenance-networks | Spec 027 Stage 2 / Q7: Provenanced-Material Networks and Craft Style |
| 033-sa-free-language-comparison | The Language Comparison Rerun Without the Falsified Method (D-03) |
| 040-d25-g1-chronology-controlled | D-25: G1 With Time Held Fixed (Chronology-Controlled Site-Repertoire Test) |
| 041-site-local-label-period-mapping | Site × Local-Label Period Mapping |
| 042-arm-b-object-type-split | Arm B Split by Object Type (Registered Variant of Spec 028 Arm B) |
| 059-f1-object-join | The Seal/Tablet Difference on a Better Join (Spec 024 F1 Rebuilt) |
| 060-f2-margin-curve | The Holdat Site Effect: Margin Curve and Shared Population (Residue of Spec 024 F2) |
| 061-arm-a-precision | Spec 028 Arm A: the Precision Computation (D-27) |
| 062-arm-a-precision-calibration-repair | Spec 028 Arm A: Precision Computation, Calibration Repair (Successor to Spec 061) |
| 067-f1-enlarged-join | The Seal/Tablet Difference on the Enlarged Join (Spec 059's Question Re-Run) |

*Registered predictions, PRED-2026 (5)*

| Spec dir | Title |
|---|---|
| 032-pred-2026-006-harappa-breakdown | PRED-2026-006: The Harappa Breakdown, Computed Exactly as Registered |
| 035-pred-2026-010-scoring | PRED-2026-010: Scoring the Clean-Withholding Successor |
| 036-pred-2026-011-scoring | PRED-2026-011: Scoring the Screened Clean-Withholding Successor |
| 038-pred-2026-007-full-population | PRED-2026-007 at Full Population |
| 043-pred-2026-007-registry-frame | PRED-2026-012 at Full Population, Corrected Frame (Successor to Spec 038) |

### Domain 4 — Contact zone & external corpora (2)

*Independent attestation contexts (1)*

| Spec dir | Title |
|---|---|
| 013-tn-graffiti-crosswalk | Tamil Nadu Graffiti Crosswalk: Independent Attestation Contexts for the CANDIDATE-Tier Sign Tail |

*Regional movement & culture (1)*

| Spec dir | Title |
|---|---|
| 027-movement-culture-language | Movement, Culture, and Language in the Greater Indus World |

Note on the domain's size: in v0 this domain is deliberately small at the
study level — its population is claim-led. The literature lines that work
the contact zone (e.g. the Gulf/Laursen line) enter the map as claim nodes
under their testing studies in Domain 3 and as extracted claims (§4), and
the scans (S5, Cluster B) treat the domain's thinness as a find to
classify, not a drafting error to pad over.

### Domain 5 — Program infrastructure (16)

*Platform & tooling (8)*

| Spec dir | Title |
|---|---|
| 001-glossa-lab-baseline | Glossa Lab Baseline (as-built) |
| 002-gdelt-ngrams-and-frontier-methods | GDELT Web Ngrams Switch + Frontier Methods |
| 003-mcp-and-test-gaps | MCP Update, Requirements/Test Traceability, Indus Continuation |
| 079-supervised-backend-tray | Supervised Backend + Tray Installation |
| 080-desktop-host-migration | Desktop Host Migration — Glossa Lab on TRISTEN-DESKTOP |
| 081-ui-redesign-generic-tool | UI Redesign — Glossa Lab as a Generic Program Tool |
| 082-api-token-auth | Per-Install API Token Authentication |
| 083-cloud-edition | Cloud Edition — Accounts, Invites, Admin, Hosted Tool |

*Evidence & research-check tooling (3)*

| Spec dir | Title |
|---|---|
| 025-paper-search-research-check | Paper-Search MCP Client + RESEARCH-CHECK Stage |
| 025-stage2-controlled-followup | Spec 025 Stage 2 Controlled Follow-Up |
| 026-core-research-source | CORE as a Keyed Source for the RESEARCH-CHECK Stage |

*Governance, lifecycle & generated layers (5)*

| Spec dir | Title |
|---|---|
| 026-rcph-framework-transfer | RCPH Framework Transfer, Impact Audit, and Reruns |
| 029-tao-claim-lifecycle | Tao Claim Lifecycle: Staging, Decomposition, Digestion, Lane Discipline |
| 084-policy-sync-conformance | POLICY-SYNC Conformance — Approved-Text Fixtures for Web Surfaces |
| 086-winning-combination-adoption | Winning-Combination Adoption: Ledger, Generated Matrix, Executable Settling, Layered Map |
| 087-node-system-tightening | Node-System Tightening — One Registry, a Primitive Palette, a Generated Manual |

(088's own directory joins Domain 5 / Governance on adoption — it is the
89th directory when it lands, and the taxonomy amendment that adds it is
part of the adoption motion, recorded here in advance so the count is
honest: v1 as filed covers the 88 directories that exist today; the
adoption amendment adds `088-program-map-gap-register` under Governance,
lifecycle & generated layers, making the filed v1 cover 89.)

## 4. Extracted-claim document assignments (23 claims, 7 documents)

Counted from the ledger 2026-11-04 (population = extracted; falsifier
present on 14 of 23 — the 9 nulls are a scan/register item, enumerated by
the builder's find list, not here).

| Source document | Claims | Assignment |
|---|---|---|
| farmer_sproat_witzel_2004 | 1 | Domain 3 — Source-thesis tests (tested by Spec 052) |
| yadav_2009_arxiv | 2 | Domain 3 — Source-thesis tests (Specs 053/054/068) |
| parpola_2010_dravidian_solution | 2 | Domain 3 — Source-thesis tests (Specs 048/072) |
| without_kings_or_conquests (Hunt) | 6 | Domain 3 — Source-thesis tests (Specs 045/050/069–071/074/075) |
| ancient_writing_and_modern_technologies | 4 | Domain 3 — Extracted literature claims (no testing line) |
| the_archaeology_and_epigraphy_of_indus_writing | 2 | Domain 3 — Extracted literature claims (no testing line) |
| indus_valley_script_deciphered_from_myth | 6 | Domain 3 — Extracted literature claims (no testing line) |

The three "no testing line" documents take the additional subdomain
**Extracted literature claims** under Domain 3, declared here so the
taxonomy's subdomain list is complete: Domain 3 has four subdomains, not
three. That these documents' claims were extracted but never taken up by
a study is itself a scan input (Cluster B), stated here so the assignment
is not mistaken for coverage.

## 5. Coverage notes (counted, 2026-11-04)

- **88 directories, 85 distinct numbers.** Numbers 021, 025, and 026 each
  have two directories (distinct studies, listed separately above).
- **Numbers 049 and 085 have no directory.** Spec 049 is named as a
  predecessor by Spec 070's own title ("Re-scoped Successor to Spec
  049"); Spec 085's package exists only in the goal workspace,
  unadopted. Neither can receive a study node — there is no directory to
  cite (C088-6) — so both are recorded here and carried to the scans as
  stale-bookkeeping candidates (Cluster C), not silently dropped from
  the count.
- **Bundle-less directories: 28.** The ledger carries bundle claims for
  60 of the 88 directories (bundle files on disk also count 60). The 28
  without — the 001–025 directories (27, counting both 021s and both
  025s) plus `026-core-research-source` — receive unjudged nodes and
  per-study finds under C088-5. They are concentrated in Domains 2 and 5
  and the early Domain 1, which the scans read as the map's largest
  single hole.
