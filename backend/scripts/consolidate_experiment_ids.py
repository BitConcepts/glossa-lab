#!/usr/bin/env python3
"""Consolidate experiment IDs into canonical descriptive names.

Scans the experiment graph JSON files and the experiment_ledger.json
to build a mapping from canonical descriptive IDs to legacy phase-based IDs.
Writes backend/glossa_lab/experiment_id_aliases.json.

Usage:
    python backend/scripts/consolidate_experiment_ids.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

# Resolve paths relative to this script
BACKEND = Path(__file__).resolve().parent.parent
GLOSSA = BACKEND / "glossa_lab"
GRAPHS_DIR = GLOSSA / "experiments" / "graphs"
LEDGER_PATH = GLOSSA / "experiment_ledger.json"
OUTPUT_PATH = GLOSSA / "experiment_id_aliases.json"


def load_graph_ids() -> list[str]:
    """Return all experiment IDs from graph JSON files."""
    ids: list[str] = []
    if not GRAPHS_DIR.exists():
        return ids
    for p in sorted(GRAPHS_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text("utf-8"))
            ids.append(data.get("id", p.stem))
        except Exception:
            ids.append(p.stem)
    return ids


def load_ledger_categories() -> dict[str, str]:
    """Return file stem -> category from the experiment ledger."""
    cats: dict[str, str] = {}
    if not LEDGER_PATH.exists():
        return cats
    entries = json.loads(LEDGER_PATH.read_text("utf-8"))
    for entry in entries:
        fname = entry.get("file", "")
        stem = fname.replace(".py", "")
        cats[stem] = entry.get("category", "misc")
    return cats


# ── Canonical grouping rules ──────────────────────────────────────────────
# Each rule is (canonical_name, description, list of regex patterns that
# match graph experiment IDs).

CANONICAL_RULES: list[tuple[str, str, list[str]]] = [
    # --- Anchored SA Sanskrit (must come BEFORE Dravidian to grab *_sanskrit* IDs) ---
    (
        "indus_anchored_sa_sanskrit",
        "Anchored SA Sanskrit falsification tests",
        [
            r"^indus_phase32_t7_sanskrit",
            r"^indus_phase33_t7_sanskrit",
            r"^indus_cisi_dravidian_vs_sanskrit",
            r"^indus_dravidian_vs_sanskrit",
            r"^indus_south_dravidian_vs_sanskrit",
        ],
    ),
    # --- Entropy / Zipf / epistasis / structural signature ---
    (
        "indus_entropy_epistasis",
        "Entropy, Zipf, epistasis, structural language signature (phases 14-15, 20-21)",
        [
            r"^indus_phase1[45][a-z_]*",       # phase14*, phase15*
            r"^indus_phase20[a-z_]*",           # phase20*
            r"^indus_phase21[a-z_]*",           # phase21*
        ],
    ),
    # --- Contact zone / bilingual analysis ---
    (
        "indus_contact_zone_bilingual",
        "Mesopotamian contact zone, bilingual readout, seal analysis (phases 22-24)",
        [
            r"^indus_phase22[a-z_]*",
            r"^indus_phase23[a-z_]*",
            r"^indus_phase24[a-z_]*",
            r"^indus_contact_zone",
        ],
    ),
    # --- Anchored SA Dravidian (phonetic readout, Janabiyah, etc.) ---
    (
        "indus_anchored_sa_dravidian",
        "Anchored SA Dravidian: Janabiyah, Bayesian, phonetic readout (phases 25-30, 32-33, 48-73, 81-121, 128-165, 190-201, 206-229, 237-253, 257-294, 322-362)",
        [
            r"^indus_phase2[5-9][a-z_]*",       # phase25-29
            r"^indus_phase30[a-z_]*",            # phase30
            r"^indus_phase3[2-3][a-z_]*",        # phase32-33
            r"^indus_phase(4[89]|5[0-5])_?",     # phase48-55
            r"^indus_phase(5[6-9]|6[0-1])_?",    # phase56-61
            r"^indus_phase(6[2-6])_?",            # phase62-66
            r"^indus_phase(6[7-9]|7[0-3])_?",    # phase67-73
            r"^indus_phase(8[1-7])_?",            # phase81-87
            r"^indus_phase(9[1-9]|100)_?",        # phase91-100
            r"^indus_phase10[4-9]_?",             # phase104-109
            r"^indus_phase11[0-5]_?",             # phase110-115
            r"^indus_phase11[6-9]_?",             # phase116-119
            r"^indus_phase12[01]_?",              # phase120-121
            r"^indus_phase12[89]_?",              # phase128-129
            r"^indus_phase1[3-4][0-9]_?",         # phase130-149
            r"^indus_phase15[0-5]_?",             # phase150-155
            r"^indus_phase15[6-9]_?",             # phase156-159
            r"^indus_phase16[0-5]_?",             # phase160-165
            r"^indus_phase19[0-5]_?",             # phase190-195
            r"^indus_phase19[6-9]_?",             # phase196-199
            r"^indus_phase20[0-1]_?",             # phase200-201
            r"^indus_phase20[6-8]_?",             # phase206-208
            r"^indus_phase21[6-9]_?",             # phase216-219
            r"^indus_phase22[0-9]_?",             # phase220-229
            r"^indus_phase23[7-9]_?",             # phase237-239
            r"^indus_phase24[0-6]_?",             # phase240-246
            r"^indus_phase24[89]_?",              # phase248-249
            r"^indus_phase25[0-3]_?",             # phase250-253
            r"^indus_phase(25[7-9]|2[6-8][0-9]|29[0-4])_?",  # phase257-294
            r"^indus_phase(32[2-9]|3[3-5][0-9]|36[0-2])_?",  # phase322-362
            r"^indus_cisi_anchored",              # indus_cisi_anchored*
            r"^indus_cisi_sa",                    # indus_cisi_sa*
            r"^indus_anchor_estimation",
            r"^indus_anchor_sweep",
            r"^indus_v[35]_",                     # v3 / v5 graph experiments
        ],
    ),
    # --- Anchored SA Munda ---
    (
        "indus_anchored_sa_munda",
        "Anchored SA Munda comparison and substrate analysis (phases 298-308)",
        [
            r"^indus_phase(29[89]|30[0-8])_?",   # phase298-308
        ],
    ),
    # --- CTT ---
    (
        "indus_ctt_constrained",
        "Constraint Topology Theory variants (CTT)",
        [
            r"^indus_phase(9|1[0-3])_ctt",
            r"^indus_phase10_ctt",
            r"^indus_phase11_ctt",
            r"^indus_phase12_full",
            r"^indus_phase13_full",
        ],
    ),
    # --- Contact zone KL divergence ---
    (
        "indus_contact_zone_kl",
        "Contact zone KL divergence and indirect bilingual analysis (phases 230-234)",
        [
            r"^indus_phase23[0-4]_?",
            r"^kl_comparison$",
        ],
    ),
    # --- LM competing tests ---
    (
        "indus_lm_competing",
        "Competing language model tests (Dravidian vs Pali, scoring)",
        [
            r"^indus_cisi_dravidian_vs_pali",
            r"^indus_dravidian_vs_pali",
            r"^indus_phase(7[4-9]|80)_?",        # phase74-80
            r"^indus_phase16[6-8]_?",             # phase166-168
            r"^indus_phase169_?",                 # phase169
            r"^indus_phase170_?",                 # phase170
        ],
    ),
    # --- A/B language comparison ---
    (
        "indus_ab_dravidian_sanskrit",
        "A/B language comparison: Dravidian vs Sanskrit/Munda/Hebrew",
        [
            r"^indus_sign_function_dravidian",
        ],
    ),
    # --- Fuls NW Semitic benchmark ---
    (
        "fuls_nw_semitic",
        "Fuls NW Semitic decipherment benchmark",
        [
            r"^fuls_nw_semitic",
            r"^fuls_rtl_decipher",
        ],
    ),
    # --- Fuls validation suite ---
    (
        "fuls_validation",
        "Fuls validation suite: split sensitivity, independence, constraints",
        [
            r"^fuls_validation_suite",
            r"^fuls_split_sensitivity",
            r"^fuls_independence_suite",
            r"^fuls_constraint_space",
            r"^fuls_anchor_simulation",
            r"^fuls_sequence_information_test",
            r"^fuls_writing_system_comparison",
        ],
    ),
    # --- Fuls entropy ---
    (
        "fuls_entropy",
        "Fuls entropy and structural analysis",
        [
            # These are primarily captured by the validation suite above;
            # any fuls_* not already matched goes here
        ],
    ),
    # --- Cross-culture ---
    (
        "indus_cross_culture",
        "Cross-culture analysis: Elamite-Dravidian, McAlpin cognates, phylogenetics (phases 122-123, 185-189, 203-205, 235-236)",
        [
            r"^indus_phase12[23]_?",             # phase122-123
            r"^indus_phase18[5-9]_?",             # phase185-189
            r"^indus_phase20[3-5]_?",             # phase203-205
            r"^indus_phase23[56]_?",              # phase235-236
        ],
    ),
    # --- Archaeological / guild context ---
    (
        "indus_archaeological",
        "Archaeological context: OCR, iconography, name lexicon, aDNA, ICIT (phases 28-29, 101-103, 124-127, 181)",
        [
            r"^indus_phase10[1-3]_?",            # phase101-103
            r"^indus_phase12[4-7]_?",            # phase124-127
            r"^indus_phase181_?",                 # phase181
            r"^indus_cgsa",
            r"^indus_fish_sign",
            r"^indus_cisi_structural",
            r"^ocr_",
        ],
    ),
    # --- Literature mining ---
    (
        "indus_literature_mining",
        "Literature mining, evidence gathering, bulk mine runs (phases 88-90, 179-184, 295-297)",
        [
            r"^indus_phase(8[89]|90)_?",         # phase88-90
            r"^indus_phase17[9]_?",               # phase179
            r"^indus_phase18[0-4]_?",             # phase180-184
            r"^indus_phase29[5-7]_?",             # phase295-297
        ],
    ),
    # --- Legacy / infrastructure ---
    (
        "indus_legacy_infrastructure",
        "Legacy migration shims and infrastructure phases (16-19, misc_gaps)",
        [
            r"^indus_phase1[6-9]_",              # phase16-19 graph experiments
        ],
    ),
    # --- Non-Indus benchmarks (standalone) ---
    (
        "benchmark_non_indus",
        "Non-Indus script benchmarks: Ugaritic, Linear B, Meroitic, Proto-Sinaitic, etc.",
        [
            r"^ugaritic_",
            r"^ventris_",
            r"^phoenician_",
            r"^meroitic_",
            r"^proto_sinaitic_",
            r"^old_hebrew_",
            r"^linear_a_",
            r"^tier[35]_",
            r"^tier_diagnostics",
            r"^writing_system_progression",
            r"^beam_decipher_benchmark",
            r"^prior_ablation_benchmark",
            r"^semitic_constraints_benchmark",
            r"^sequence_eval_benchmark",
            r"^transparency_benchmark",
        ],
    ),
    # --- Geez benchmarks ---
    (
        "benchmark_geez",
        "Geez/Ethiopic decipherment benchmarks",
        [
            r"^geez_",
        ],
    ),
    # --- Generic structural tools ---
    (
        "tool_structural_analysis",
        "Generic structural analysis tools (positional profile, clustering, bigrams, KL, atlas)",
        [
            r"^positional_profile_analysis",
            r"^symbol_clustering",
            r"^bigram_analysis",
            r"^indus_structural_atlas",
            r"^kandles_bias",
            r"^luwian_kl_scoring",
        ],
    ),
    # --- Phase 9 cluster-anchored ---
    (
        "indus_cluster_anchored",
        "Cluster-anchored SA experiments (phase 9)",
        [
            r"^indus_phase9_",
        ],
    ),
]


def classify_ids(all_ids: list[str]) -> tuple[dict[str, list[str]], list[str]]:
    """Classify experiment IDs into canonical groups.

    Returns (canonical_map, unmatched_ids).
    """
    canonical_map: dict[str, list[str]] = {}
    matched: set[str] = set()

    for canonical_name, _desc, patterns in CANONICAL_RULES:
        group: list[str] = []
        for eid in all_ids:
            if eid in matched:
                continue
            for pat in patterns:
                if re.match(pat, eid):
                    group.append(eid)
                    matched.add(eid)
                    break
        if group:
            canonical_map[canonical_name] = sorted(group)

    unmatched = sorted(set(all_ids) - matched)
    return canonical_map, unmatched


def main() -> None:
    print("=" * 60)
    print("Experiment ID Consolidation")
    print("=" * 60)

    # Load all graph experiment IDs
    graph_ids = load_graph_ids()
    print(f"\nFound {len(graph_ids)} graph experiment IDs in {GRAPHS_DIR}")

    # Also load hardcoded experiments from _build_proper_graph_specs
    # These IDs are already in the graphs dir as JSON files, so graph_ids covers them

    # Classify
    canonical_map, unmatched = classify_ids(graph_ids)

    # Print summary
    print(f"\nCanonical groups: {len(canonical_map)}")
    print("-" * 60)
    total_mapped = 0
    for canonical, aliases in sorted(canonical_map.items()):
        total_mapped += len(aliases)
        print(f"\n  {canonical} ({len(aliases)} experiments)")
        for a in aliases:
            print(f"    - {a}")

    if unmatched:
        print(f"\n  [UNMATCHED] ({len(unmatched)} experiments)")
        for u in unmatched:
            print(f"    - {u}")

    print(f"\n{'=' * 60}")
    print(f"Total mapped:   {total_mapped}")
    print(f"Unmatched:      {len(unmatched)}")
    print(f"Total:          {len(graph_ids)}")

    # If there are unmatched IDs, add them to a catch-all group
    if unmatched:
        canonical_map["indus_uncategorized"] = unmatched

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(canonical_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {OUTPUT_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
