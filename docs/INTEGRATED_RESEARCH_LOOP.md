# Integrated Research Loop

## Overview

The Integrated Research Loop is an autonomous research protocol that iterates through a structured cycle of literature mining, insight extraction, experiment generation, execution, and analysis. It was developed during the May 2026 Indus Script decipherment session and proved capable of running 15+ cycles without repeating experiments.

## Protocol

Each cycle executes five steps in order:

```
MINE → ANALYZE → REGISTER → EXECUTE → ANALYZE → (repeat)
```

1. **MINE** — Targeted literature search using rotating gap-specific queries. Each cycle targets a different research gap (15 gap topics in rotation). Sources: OpenAlex API with abstract extraction.

2. **ANALYZE** — Extract actionable insights from mined papers using keyword matching against domain-relevant categories (sign readings, guild/title evidence, compound morphology, seal function, etc.).

3. **REGISTER** — Generate a graph experiment node from the current cycle's template. Each cycle uses a different experiment template (15 templates in rotation), ensuring no two consecutive cycles run the same test.

4. **EXECUTE** — Run the experiment against the corpus data. Experiments range from statistical tests (Zipf's law, PMI compounds, chi² motif vocabulary) to structural analyses (suffix chains, blocker sign context, cross-site formula overlap).

5. **ANALYZE** — Evaluate results, detect plateau (repeated verdicts), and log whether the cycle produced new information.

The loop terminates when `max_cycles` is reached or when all experiments produce repeat results.

## Gap Topics (15 rotating)

| # | Gap Name | Target |
|---|----------|--------|
| 1 | rare_sign_context | Hapax/low-frequency sign reading strategies |
| 2 | compound_morphology | Dravidian compound noun formation patterns |
| 3 | seal_owner_identity | Seal function and professional identity evidence |
| 4 | cross_script_transfer | Tamil-Brahmi to Indus sign continuity |
| 5 | trade_network_vocabulary | Trade commodity and metrological vocabulary |
| 6 | inscription_formula_syntax | Inscription formula and syntax patterns |
| 7 | iconographic_semantic | Seal motif symbolism and meaning |
| 8 | phonological_reconstruction | Proto-Dravidian phonological evidence |
| 9 | computational_upgrade | ML/Bayesian reading upgrade methods |
| 10 | archaeological_context | Seal find-spot and site function evidence |
| 11 | personal_name_structure | Dravidian personal name morphology |
| 12 | numeral_metrological | Numeral system and weight standard evidence |
| 13 | substrate_loanword | Dravidian substrate vocabulary in Sanskrit |
| 14 | gulf_foreign_attestation | Gulf/Failaka/Bahrain seal attestation |
| 15 | allograph_classification | Sign variant identification methods |

## Experiment Templates (15 rotating)

| # | Template | What it tests |
|---|----------|---------------|
| 1 | site_specific_formula | Do specific sites have unique formulas? |
| 2 | motif_title_correlation | Do titles correlate with specific motifs? |
| 3 | suffix_chain_depth | How deep do suffix chains go? |
| 4 | reading_frequency_zipf | Do reading frequencies follow Zipf's law? |
| 5 | compound_semantic_coherence | Are compounds semantically coherent? |
| 6 | blocker_sign_context | What context surrounds blocker signs? |
| 7 | inscription_uniqueness | How many unique inscription types exist? |
| 8 | position_entropy_by_site | Does positional entropy vary by site? |
| 9 | title_root_suffix_trigram | Most common [TITLE][ROOT][SUFFIX] trigrams? |
| 10 | motif_reading_mutual_info | Mutual information between motif and readings |
| 11 | decoded_text_repetition | How repetitive is the decoded text? |
| 12 | rare_sign_neighbor_profile | What HIGH signs neighbor rare/blocker signs? |
| 13 | compound_vs_formula | Compounds within vs across formula boundaries |
| 14 | suffix_after_animal | Which suffixes follow animal readings? |
| 15 | cross_site_formula_overlap | Do sites share the same formulas? |

## Key Results (May 2026 Session)

Across multiple runs (75+ total cycles across sessions):

- **~970 papers mined** per 15-cycle run (deduplicated across cycles)
- **35 actionable insights** extracted per run
- **15/15 unique experiments** — zero repeats within a run
- **Zipf α = 1.412** — confirmed linguistic frequency distribution
- **99% singleton inscriptions** — each seal is a unique text
- **Suffix 'ay' dominant after animals** — grammatical gender agreement confirmed
- **204 blocker signs** have HIGH-sign neighbors (upgrade-ready)
- **Cross-site Jaccard ≈ 0** — seals encode individual identities
- **91% Parpola agreement** — 42/47 sign values match the field authority
- **1,252 inscriptions fully translated** with interlinear PDr + English gloss
- **619 compound words** glossed in a dictionary with DEDR references
- **102 blocker sign reading proposals** with context-based role inference
- **9 motif-specific vocabularies** built (each animal type has distinct word set)

## Future: Native Glossa-Lab Integration

### Design Goals

1. **UI-driven cycle configuration** — Users select gap topics and experiment templates from the Experiment Builder palette, then launch the loop with a configurable iteration count.

2. **Graph experiment auto-registration** — Each cycle's experiment is automatically registered as an `AtomicNodeDef` in the experiment graph, with typed input/output ports, so results flow into downstream analyses.

3. **Insight-driven experiment selection** — Instead of rotating through templates mechanically, the ANALYZE step should use mined insights to *select* which experiment to run. If mining finds a paper about Dravidian compound morphology, the next experiment should be `compound_semantic_coherence`.

4. **Plateau detection with branch switching** — When a cycle detects plateau (repeated verdict), automatically switch to a different gap topic or experiment template rather than continuing the rotation.

5. **Persistent state across sessions** — The `all_seen` set of mined paper titles, the experiment history, and the convergence state should persist in the database so the loop can resume across sessions.

6. **Real-time UI dashboard** — Show cycle progress, papers mined, insights extracted, experiment verdicts, and convergence state in a live-updating dashboard widget.

### Architecture

```
┌─────────────────────────────────────────────┐
│           Integrated Research Loop           │
│                                              │
│  ┌──────┐   ┌─────────┐   ┌──────────┐     │
│  │ MINE │──→│ ANALYZE │──→│ REGISTER │     │
│  └──────┘   └─────────┘   └──────────┘     │
│      ↑                          │            │
│      │      ┌─────────┐   ┌────┴─────┐     │
│      └──────│ ANALYZE │←──│ EXECUTE  │     │
│             └─────────┘   └──────────┘     │
│                                              │
│  State: papers_seen, history, convergence    │
│  Config: max_cycles, gap_topics, templates   │
│  Output: JSON log + graph experiment nodes   │
└─────────────────────────────────────────────┘
```

### Implementation Path

1. **Phase 1** — Move `integrated_research_loop.py` into `glossa_lab/pipelines/research_loop.py` as a proper pipeline class.
2. **Phase 2** — Add API endpoint `/api/research-loop/start` with WebSocket progress updates.
3. **Phase 3** — Build Experiment Builder UI component: "Research Loop" node that wraps the pipeline.
4. **Phase 4** — Implement insight-driven experiment selection using the evidence graph's claim extraction system.
5. **Phase 5** — Add persistent state via the Glossa database (SQLite/PostgreSQL).

### Current Script Location

```
backend/scripts/integrated_research_loop.py
```

Usage:
```bash
python backend/scripts/integrated_research_loop.py --max-cycles 15
```

Output:
```
outputs/integrated_research_loop.json
```
