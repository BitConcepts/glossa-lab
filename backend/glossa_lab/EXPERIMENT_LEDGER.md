# Experiment Ledger

Comprehensive catalog of all experiment graph phase files in the Glossa Lab research platform.

## Summary

| Phase File | Category | Status | Purpose | Recommendation |
|---|---|---|---|---|
| experiment_graph.py | structural_analysis | active | Core engine with ~50 built-in atomic nodes and graph execution runtime | keep |
| experiment_graph_ctt.py | ctt | active | CTT nodes: sign role classifier, admissibility filter, holdout recall, compound constraint, anchored SA | keep |
| experiment_graph_indus_evidence.py | misc | active | Evidence graph nodes for literature/claims management | keep |
| experiment_graph_phase14.py | structural_analysis | active | Block entropy, conditional entropy, Zipf-Mandelbrot, MI decay, epistatic detection, language verdict | keep |
| experiment_graph_phase15.py | structural_analysis | active | Long-tail validity, cipher self-test, multi-hypothesis ranker, deciphered mapping exporter | keep |
| experiment_graph_phase_legacy.py | misc | legacy | Migration shims for Phase 16-19 standalone scripts | keep |
| experiment_graph_phase20.py | structural_analysis | active | Length-stratified spectral, cluster archaeology, Ferrara OCR, Fuls classifier | keep |
| experiment_graph_phase21.py | structural_analysis | active | Repetition collapser, site stratifier, numerical-weight regression | keep |
| experiment_graph_phase22.py | contact_zone | active | CDLI Meluhha-mention corpus, Meluhhan persons, Indus seals at Mesopotamia | keep |
| experiment_graph_phase23.py | contact_zone | active | Refined seal audit, strict PN extraction, bilingual readout test | keep |
| experiment_graph_phase24.py | contact_zone | active | Laursen Table 1, seal sign upgrade, persons-v2, bipartite readout v2 | keep |
| experiment_graph_phase25.py | sa_variant | active | Janabiyah readout, held-out test, period-stratified replication, Tamil-Brahmi | keep |
| experiment_graph_phase26.py | sa_variant | active | Provenience-stratified SA, Bayesian decoder, expanded readout | keep |
| experiment_graph_phase27.py | sa_variant | active | Reverse Janabiyah, Bayesian v2, iconographic anchors | keep |
| experiment_graph_phase28.py | archaeological | active | CISI Vol 3 OCR, Mahadevan crosswalk, allograph-aware SA | keep |
| experiment_graph_phase29.py | archaeological | active | Corpus 10x expansion: M77, ePSD2, Fuls, ICIT loaders | keep |
| experiment_graph_phase30.py | sa_variant | active | Length-cohort reverse Janabiyah, permutation test, Dravidian syllable LM | keep |
| experiment_graph_phase_misc_gaps.py | misc | legacy | Phases 44-47, 202, 209-215, 254-256 wrapped as subprocess runners | keep |
| experiment_graph_phase48_55.py | sa_variant | active | Full Indus decipherment pipeline (GPU mandatory) | keep |
| experiment_graph_phase56_61.py | sa_variant | active | Expanded Parpola SA, phonotactic falsification (GPU mandatory) | keep |
| experiment_graph_phase62_66.py | sa_variant | active | Ensemble fix, phonotactic filter, morpheme boundary, Sanskrit SA | keep |
| experiment_graph_phase67_73.py | sa_variant | active | Sanskrit norm, formula translation, M267 validation, parser | keep |
| experiment_graph_phase74_80.py | lm_scoring | active | Grammar test, Levit, place formula, SA agreement, semantic cluster, DEDR | keep |
| experiment_graph_phase81_87.py | sa_variant | active | M293 deep-dive, seal translation, formula lexicon, phonology | keep |
| experiment_graph_phase88_90.py | misc | active | Literature mine, DEDR expansion to 120, scholarly translations | keep |
| experiment_graph_phase91_100.py | sa_variant | active | Anchor-120 SA, M293 SA, trigram, grammar, full-corpus runs | keep |
| experiment_graph_phase101_103.py | archaeological | active | M293 iconographic, PDF extraction, personal name lexicon | keep |
| experiment_graph_phase104_109.py | sa_variant | active | OCR, name signs, name SA, Tamil-Brahmi check, phoneme exhaustion | keep |
| experiment_graph_phase110_115.py | sa_variant | active | Targeted SA, allographs, grammar inference, seal translations | keep |
| experiment_graph_phase116_121.py | sa_variant | active | SA recalibration, grammar LOW, site semantics, arXiv | keep |
| experiment_graph_phase122_123.py | cross_language | active | Syllabic SA, Munda/BMAC substrate hypothesis | keep |
| experiment_graph_phase124_125.py | structural_analysis | active | Fish-sign polysemy, Arthasastra mining | keep |
| experiment_graph_phase126.py | archaeological | active | ICIT corpus integration and sign inventory alignment | keep |
| experiment_graph_phase127.py | contact_zone | active | Gulf corpus analysis, Roif mining, fish-sign polysemy | keep |
| experiment_graph_phase128_133.py | sa_variant | active | SA refinement and anchor injection cycles | keep |
| experiment_graph_phase134_141.py | structural_analysis | active | Falsification suite, advancement testing, master scorecard | keep |
| experiment_graph_phase142_145.py | sa_variant | active | SA anchor injection and refinement cycles | keep |
| experiment_graph_phase146_155.py | sa_variant | active | SA parameter exploration and convergence testing | keep |
| experiment_graph_phase156_165.py | sa_variant | active | Advanced SA with refined anchors | keep |
| experiment_graph_phase166_168.py | lm_scoring | active | Sibilant validation, Meluhhan expansion, blocker SA | keep |
| experiment_graph_phase169_170.py | structural_analysis | active | Master synthesis, grammar variance — computational frontier | keep |
| experiment_graph_phase171_178.py | structural_analysis | active | Network centrality, betweenness stratification, network deep-dive | keep |
| experiment_graph_phase179_180.py | misc | active | Literature mine, Mesopotamian contact mine | keep |
| experiment_graph_phase181.py | archaeological | active | aDNA archaeogenetics mine | keep |
| experiment_graph_phase182.py | misc | active | Deep evidence mine | keep |
| experiment_graph_phase183.py | misc | active | Bulk mine 5000 (superseded by phase184) | keep |
| experiment_graph_phase184.py | misc | active | Bulk mine 5000 second run, fresh clusters | keep |
| experiment_graph_phase185_189.py | cross_language | active | Fish-sign battery, Elamo-Dravidian gap, commodity semantic, north Dravidian LM | keep |
| experiment_graph_phase190_192.py | sa_variant | active | Elamite anchor injection, grammar validation | keep |
| experiment_graph_phase193_195.py | sa_variant | active | SA rerun, SSRN fetch, grammar revalidation | keep |
| experiment_graph_phase196_201.py | sa_variant | active | Mine3, top-8, DEDR lookup, triple-LM, inscription reading | keep |
| experiment_graph_phase203_205.py | cross_language | active | E28 falsification, McAlpin cognates, Bayesian phylogenetics | keep |
| experiment_graph_phase206_208.py | sa_variant | active | Anchor injection M692/M861, SA rerun 404, mine5 | keep |
| experiment_graph_phase216_220.py | sa_variant | active | SA recalibration, site semantic, arXiv, Parpola/CISI | keep |
| experiment_graph_phase221_225.py | sa_variant | active | P324/P122 investigation, CISI injection, slot mismatch | keep |
| experiment_graph_phase226_228.py | sa_variant | active | P122 phonetic, P324 formula, CISI tripartite | keep |
| experiment_graph_phase229.py | sa_variant | active | CISI anchor SA test, M122 upgrade | keep |
| experiment_graph_phase230_234.py | contact_zone | active | Cross-ref matrix, indirect bilingual, cultural/demographic | keep |
| experiment_graph_phase235_236.py | cross_language | active | Elamite–PDr bridge, Sanskrit loanword mapping | keep |
| experiment_graph_phase237_246.py | sa_variant | active | Blocker mine, batch upgrades, synthesis, SA crossing | keep |
| experiment_graph_phase248_253.py | sa_variant | active | Ceiling-breaker mine, allograph, semantic constraint | keep |
| experiment_graph_phase257_294.py | sa_variant | active | SA reruns, Yajnadevam, DEDR resolution, 605/605 decipherment | keep |
| experiment_graph_phase295_297.py | misc | active | Bulk mine May 2026, cross-reference, gap analysis | keep |
| experiment_graph_phase298_308.py | cross_language | active | Munda mine/SA, substrate, archaeology, DEDR, Elamite baseline | keep |
| experiment_graph_phase322_362.py | sa_variant | active | May 2026 decipherment advancement session | keep |
| experiment_graph_contact_zone.py | contact_zone | active | KL divergence, synthesis, A/B comparison for contact signals | keep |
| experiment_graph_ab_language.py | cross_language | active | A/B language SA: Dravidian vs Sanskrit/Munda/Hebrew, LM consistency | keep |
| experiment_graph_cross_culture.py | cross_language | active | Cultural contact matrix, script family classifier | keep |

## Category Legend

- **structural_analysis** — Entropy, positional, spectral, network analysis of sign/symbol systems
- **lm_scoring** — Language model scoring, grammar tests, validation
- **sa_variant** — Simulated annealing decipherment runs and variants
- **ctt** — Constraint Topology Theory framework
- **contact_zone** — Mesopotamian contact corpus, bilingual analysis, seals
- **cross_language** — Cross-language comparison, substrate hypothesis, phylogenetics
- **archaeological** — OCR, corpus expansion, archaeogenetics, iconography
- **misc** — Literature mining, evidence management, infrastructure, legacy shims
