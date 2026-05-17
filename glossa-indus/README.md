# Glossa-Lab Indus Evidence Graph

**Indus Corpus + Literature Graph + Claim Registry + Hypothesis Engine + Testbed**

## Purpose

This system builds a comprehensive, evidence-grounded research environment for the
Indus script.  It does **not** declare the script deciphered.  It makes every
decipherment claim **visible, structured, comparable, testable, falsifiable, and
traceable to evidence**.

## Core Philosophy

- Do not force a single theory — preserve all competing interpretations.
- Treat all decipherments as hypotheses, not settled truth.
- Prioritize falsifiability over elegance.
- Separate evidence from interpretation at every layer.
- Keep everything reversible — never overwrite raw data.

## System Components

| Layer | Purpose |
|---|---|
| `corpus/` | Inscriptions, artifacts, images, sign sequences, metadata |
| `literature/` | Papers, books, excavation reports, catalogues, PDFs |
| `claims/` | Extracted and normalized scholarly claims |
| `hypotheses/` | Registered decipherment models and predictions |
| `analysis/` | Statistical, positional, GIS, and contextual tests |
| `reports/` | Synthesis reports, model comparisons, ingestion reports |
| `raw/` | Unmodified source files — never edited |
| `processed/` | OCR, cleaned text, tables, images extracted from raw |
| `quarantine/` | Unclear license, failed downloads, duplicates |

## Decipherment Pipeline (in order)

```
1. Build corpus
2. Normalize signs
3. Ingest literature
4. Extract claims
5. Register hypotheses
6. Run structural tests
7. Run archaeological context tests
8. Run null models
9. Compare hypotheses
10. Produce cautious synthesis
11. Generate candidate readings only after evidence scoring
```

Do NOT jump from paper ingestion to translation.

## Currently Registered Hypotheses

See `hypotheses/models/` for full schemas.

| Model ID | Type | Status |
|---|---|---|
| `mahadevan_concordance_baseline` | corpus/sign_concordance | registered |
| `parpola_proto_dravidian` | proto_dravidian_rebus | registered — Phase-41/43 SA evidence |
| `farmer_sproat_witzel_nonlinguistic` | critique/non_linguistic | registered |
| `wells_structural_sign_list` | sign_system | registered |
| `roif_guild_ledger` | phonetic_mnemonic_economic | stub — awaiting upload |
| `hunt_civic_ritual` | symbolic_operational | stub — awaiting upload |
| `null_random_shuffle` | null_model | registered |
| `null_frequency_preserved` | null_model | registered |

## Claim Status Vocabulary

```
untested | testable | partially_supported | strongly_supported
contradicted | unfalsifiable | requires_more_data
```

## How to Upload a Paper

Place the PDF in `raw/user_uploads/` and run:

```bash
python glossa-indus/scripts/indus_intake.py --file raw/user_uploads/<file.pdf>
```

The intake script will:
1. Compute checksum and check for duplicates
2. Extract text (embedded or OCR)
3. Register in `literature/documents/`
4. Add to claim extraction queue

## Key Scripts

| Script | Purpose |
|---|---|
| `scripts/indus_intake.py` | Document intake, dedup, registration |
| `scripts/indus_claims.py` | Claim extraction and normalization |
| `scripts/indus_hypothesis.py` | Hypothesis registry and scoring |
| `scripts/indus_analyze.py` | Run positional, cooccurrence, null-model tests |
| `scripts/indus_dedupe.py` | Deduplicate documents, inscriptions, claims |

## Operating Modes

- **acquisition_mode**: Download and register sources
- **upload_processing_mode**: Process user-uploaded files
- **dedupe_mode**: Detect duplicate documents, inscriptions, claims
- **extraction_mode**: Extract text, claims, signs, tables
- **corpus_mode**: Build inscription and artifact database
- **hypothesis_mode**: Register models and predictions
- **analysis_mode**: Run statistical and contextual tests
- **synthesis_mode**: Generate reports and conclusions

## Agent Instruction Plan

The full agentic instruction plan for this system is stored at:
`glossa-indus/config/INSTRUCTION_PLAN.md`

This plan governs how the agent builds, maintains, and extends this system
across all sessions.
