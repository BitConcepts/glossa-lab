"""Default report template seeder.

Seeds six research-grade report templates into the database on startup.
All templates are idempotent — they only insert if the ID is absent,
so existing user edits are never overwritten.

Templates use data_key values that match the output keys produced by
standard experiment graph nodes (JSONExport, ConsistencyScorer, etc.)
so the ReportGenerator atomic node can auto-populate sections.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("glossa_lab.report_template_seeder")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Default template definitions ─────────────────────────────────────────────
# Each entry has a stable id so upserts are safe.
# `sections` follow the SectionDef schema:
#   title, data_source, data_key, chart_type, include_table, description

DEFAULT_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "tmpl-structural-analysis",
        "name": "Structural Analysis Report",
        "description": (
            "Summarises the structural fingerprint of any corpus: H1 entropy, "
            "Zipf exponent, positional profiles (I/M/T), symbol clustering, and "
            "WritingSystemClassifier tier. Works for any script."
        ),
        "category": "Structural Analysis",
        "sections": [
            {
                "title": "Writing System Classification",
                "data_source": "experiment",
                "data_key": "tier_classification",
                "chart_type": "text",
                "include_table": False,
                "description": (
                    "Tier label from WritingSystemClassifier: "
                    "Abjad / Syllabary / Logographic / Logosyllabic."
                ),
            },
            {
                "title": "Nearest Known Script",
                "data_source": "experiment",
                "data_key": "nearest_script",
                "chart_type": "text",
                "include_table": False,
                "description": "Closest match from the benchmark script database.",
            },
            {
                "title": "H1 Entropy",
                "data_source": "experiment",
                "data_key": "h1",
                "chart_type": "bar",
                "include_table": True,
                "description": "Shannon H1 entropy in bits/token.",
            },
            {
                "title": "Zipf Exponent",
                "data_source": "experiment",
                "data_key": "zipf_exponent",
                "chart_type": "text",
                "include_table": False,
                "description": "Slope of log-rank vs log-frequency. ~1.0 = ideal Zipf.",
            },
            {
                "title": "Positional Profiles (I/M/T)",
                "data_source": "experiment",
                "data_key": "profiles",
                "chart_type": "table",
                "include_table": True,
                "description": "Per-sign initial / medial / terminal rates and dominant position class.",
            },
            {
                "title": "Symbol Clusters",
                "data_source": "experiment",
                "data_key": "clusters",
                "chart_type": "table",
                "include_table": True,
                "description": "Positional cluster groups with member signs.",
            },
        ],
    },
    {
        "id": "tmpl-decipherment-benchmark",
        "name": "Decipherment Benchmark Report",
        "description": (
            "Standard benchmark report for SA or Beam decipherment experiments: "
            "consistency scores, accuracy (if answer key present), "
            "mean HCI ≥75% fraction, and proposed mapping top-N."
        ),
        "category": "Decipherment",
        "sections": [
            {
                "title": "Mean Consistency",
                "data_source": "experiment",
                "data_key": "mean_consistency",
                "chart_type": "text",
                "include_table": False,
                "description": "Fraction of SA seeds agreeing on modal assignment (0–1).",
            },
            {
                "title": "HCI ≥ 75% Signs",
                "data_source": "experiment",
                "data_key": "hci_count",
                "chart_type": "text",
                "include_table": False,
                "description": "Number of signs with consistency ≥ 75% across seeds.",
            },
            {
                "title": "Proposed Sign Mapping",
                "data_source": "experiment",
                "data_key": "proposed_mapping",
                "chart_type": "table",
                "include_table": True,
                "description": "Modal cipher→target mapping for all signs.",
            },
            {
                "title": "Per-Sign Consistency",
                "data_source": "experiment",
                "data_key": "consistency_per_sign",
                "chart_type": "table",
                "include_table": True,
                "description": "Consistency score, modal assignment and top-3 candidates per sign.",
            },
        ],
    },
    {
        "id": "tmpl-indus-complete",
        "name": "Indus Script Complete Analysis",
        "description": (
            "Full Tier 5 research report: structural fingerprint → phonogram filter → "
            "Dravidian vs Sumerian decipherment hypothesis test. "
            "Combines tier5_indus_readings and tier5_indus_decipherment results."
        ),
        "category": "Indus Script",
        "sections": [
            {
                "title": "Writing System Tier",
                "data_source": "tier5_indus_readings",
                "data_key": "b",
                "chart_type": "text",
                "include_table": False,
                "description": "Full-corpus tier classification (expected: Logographic / Logosyllabic).",
            },
            {
                "title": "Phonogram Tier (after hapax filter)",
                "data_source": "tier5_indus_decipherment",
                "data_key": "a",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier of the high-frequency phonogram subset (expected: Syllabary).",
            },
            {
                "title": "Dravidian Consistency",
                "data_source": "tier5_indus_decipherment",
                "data_key": "b",
                "chart_type": "text",
                "include_table": False,
                "description": "SA mean consistency vs Dravidian LM. Higher = stronger structural match.",
            },
            {
                "title": "Sumerian Consistency",
                "data_source": "tier5_indus_decipherment",
                "data_key": "c",
                "chart_type": "text",
                "include_table": False,
                "description": "SA mean consistency vs Sumerian LM (comparator).",
            },
            {
                "title": "Symbol Clusters (phonograms)",
                "data_source": "tier5_indus_readings",
                "data_key": "a",
                "chart_type": "table",
                "include_table": True,
                "description": "Positional clustering of high-frequency Indus signs.",
            },
        ],
    },
    {
        "id": "tmpl-nw-semitic",
        "name": "NW Semitic Study Report (Fuls Method)",
        "description": (
            "Decipherment benchmark following the Fuls (2013) / Snyder (2010) protocol: "
            "RTL-corrected NW Semitic corpus → SA vs Hebrew LM → consistency + accuracy. "
            "Primary validation suite for the Glossa Lab pipeline."
        ),
        "category": "NW Semitic",
        "sections": [
            {
                "title": "SA Consistency (5 seeds)",
                "data_source": "ugaritic_vs_hebrew",
                "data_key": "mean_consistency",
                "chart_type": "text",
                "include_table": False,
                "description": "Mean SA seed consistency for Ugaritic → Hebrew.",
            },
            {
                "title": "Proposed Sign Mapping",
                "data_source": "ugaritic_vs_hebrew",
                "data_key": "proposed_mapping",
                "chart_type": "table",
                "include_table": True,
                "description": "Modal Ugaritic→Hebrew mapping from SA decipherment.",
            },
            {
                "title": "Fuls Split Sensitivity",
                "data_source": "fuls_split_sensitivity",
                "data_key": "a",
                "chart_type": "text",
                "include_table": False,
                "description": "Consistency at 50/50 split vs 75/25 split — answers Fuls question.",
            },
        ],
    },
    {
        "id": "tmpl-writing-system-progression",
        "name": "Writing System Tier Progression Report",
        "description": (
            "Multi-tier benchmark: NW Semitic (abjad Tier 1), Meroitic (Tier 1/2), "
            "Ge'ez (syllabary Tier 4), Indus (logo-syllabic Tier 5). "
            "Quantifies the research challenge at each tier."
        ),
        "category": "Comparison",
        "sections": [
            {
                "title": "NW Semitic Classification",
                "data_source": "writing_system_progression",
                "data_key": "a",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for NW Semitic (abjad reference).",
            },
            {
                "title": "Meroitic Classification",
                "data_source": "writing_system_progression",
                "data_key": "b",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for Meroitic.",
            },
            {
                "title": "Ge'ez Classification",
                "data_source": "writing_system_progression",
                "data_key": "c",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for Ge'ez syllabary.",
            },
            {
                "title": "Indus Classification",
                "data_source": "writing_system_progression",
                "data_key": "d",
                "chart_type": "text",
                "include_table": False,
                "description": "Tier classification for the Indus Script.",
            },
        ],
    },
    {
        "id": "tmpl-geez-benchmark",
        "name": "Ge'ez Syllabic Anchor Convergence Report",
        "description": (
            "Anchor amplification benchmark on the Ge'ez syllabic corpus (Dr. Fuls 2026): "
            "sweep k = 0, 3, 10, 20 anchors and record StructAcc (free signs), "
            "consistency, and HCI ≥ 75%. Validates the anchor-amplification hypothesis."
        ),
        "category": "Geez / Ethiopic",
        "sections": [
            {
                "title": "Summary Table",
                "data_source": "geez_anchor_convergence_v2",
                "data_key": "summary_table",
                "chart_type": "table",
                "include_table": True,
                "description": (
                    "Columns: anchor_count, struct_acc_free, rand_acc_free, "
                    "struct_consistency, rand_consistency, struct_hci75."
                ),
            },
            {
                "title": "Conclusions",
                "data_source": "geez_anchor_convergence_v2",
                "data_key": "conclusions",
                "chart_type": "text",
                "include_table": False,
                "description": "Verdict: anchor-amplification VALIDATED / PARTIAL / FAILURE.",
            },
        ],
    },
    # ── Generic templates ──────────────────────────────────────────────────
    {
        "id": "tmpl-corpus-overview",
        "name": "Corpus Overview Report",
        "description": (
            "General-purpose overview of any uploaded corpus. "
            "Covers token count, alphabet size, Shannon entropy, conditional entropy, "
            "type-token ratio, Zipf exponent, and hapax count. "
            "Works for any script or language."
        ),
        "category": "General",
        "sections": [
            {
                "title": "Corpus Metrics Summary",
                "data_source": "experiment",
                "data_key": "token_count",
                "chart_type": "text",
                "include_table": True,
                "description": "Total token count for the corpus.",
            },
            {
                "title": "H1 Shannon Entropy",
                "data_source": "experiment",
                "data_key": "h1",
                "chart_type": "bar",
                "include_table": False,
                "description": "Unigram entropy H1 in bits/token. Natural language: 3–6 bits.",
            },
            {
                "title": "Conditional Entropy H(X|X−1)",
                "data_source": "experiment",
                "data_key": "conditional_h",
                "chart_type": "text",
                "include_table": False,
                "description": "Bigram predictability. Lower = more structured.",
            },
            {
                "title": "H2/H1 Ratio",
                "data_source": "experiment",
                "data_key": "h2_h1_ratio",
                "chart_type": "text",
                "include_table": False,
                "description": "~1.5 for natural language; <1 = strong sequential structure.",
            },
            {
                "title": "Type-Token Ratio (TTR)",
                "data_source": "experiment",
                "data_key": "type_token_ratio",
                "chart_type": "text",
                "include_table": False,
                "description": "Lexical diversity. High = rich vocabulary; low = formulaic/repetitive.",
            },
            {
                "title": "Zipf Exponent",
                "data_source": "experiment",
                "data_key": "zipf_exponent",
                "chart_type": "text",
                "include_table": False,
                "description": "Log-rank regression slope. −1.0 = ideal Zipf-Mandelbrot.",
            },
            {
                "title": "Token Frequency Distribution (top 30)",
                "data_source": "experiment",
                "data_key": "top_10",
                "chart_type": "bar",
                "include_table": True,
                "description": "Frequency rank of the most common tokens.",
            },
        ],
    },
    {
        "id": "tmpl-token-frequency",
        "name": "Token Frequency Report",
        "description": (
            "Detailed token frequency analysis for any corpus. "
            "Reports full frequency map, bigram counts, hapax legomena, "
            "and sign inventory size. Suitable for any sign-level corpus."
        ),
        "category": "General",
        "sections": [
            {
                "title": "Frequency Map",
                "data_source": "experiment",
                "data_key": "freq_map",
                "chart_type": "bar",
                "include_table": True,
                "description": "Frequency of each distinct token in the corpus.",
            },
            {
                "title": "Top 10 Tokens",
                "data_source": "experiment",
                "data_key": "top_10",
                "chart_type": "table",
                "include_table": True,
                "description": "Most frequent symbols with counts.",
            },
            {
                "title": "Distinct Symbol Count",
                "data_source": "experiment",
                "data_key": "distinct_symbols",
                "chart_type": "text",
                "include_table": False,
                "description": "Total unique symbols in the corpus.",
            },
            {
                "title": "Total Token Count",
                "data_source": "experiment",
                "data_key": "total_tokens",
                "chart_type": "text",
                "include_table": False,
                "description": "Total sign/token occurrences.",
            },
            {
                "title": "Bigram Frequencies",
                "data_source": "experiment",
                "data_key": "n_bigrams",
                "chart_type": "text",
                "include_table": False,
                "description": "Number of distinct bigram types found.",
            },
        ],
    },
    {
        "id": "tmpl-comparative-analysis",
        "name": "Comparative Corpus Analysis Report",
        "description": (
            "Side-by-side comparison of two corpora using KL and Jensen-Shannon divergence. "
            "Identifies structural differences in token distributions. "
            "Use after running a KL Divergence or KL Comparison experiment."
        ),
        "category": "Comparison",
        "sections": [
            {
                "title": "KL Divergence (P ∥ Q)",
                "data_source": "experiment",
                "data_key": "kl_divergence",
                "chart_type": "text",
                "include_table": False,
                "description": "KL(P∥Q) in nats. 0 = identical; higher = more different.",
            },
            {
                "title": "Jensen-Shannon Divergence",
                "data_source": "experiment",
                "data_key": "js_divergence",
                "chart_type": "text",
                "include_table": False,
                "description": "Symmetric JS divergence [0, 1]. 0 = identical; 1 = fully different.",
            },
            {
                "title": "Number of Shared Symbols",
                "data_source": "experiment",
                "data_key": "n_symbols",
                "chart_type": "text",
                "include_table": False,
                "description": "Symbols present in both corpora.",
            },
        ],
    },
    {
        "id": "tmpl-sign-classification",
        "name": "Sign / Symbol Classification Report",
        "description": (
            "Probabilistic classification of every sign in a corpus: "
            "P(numeral), P(determinative/logogram), P(phonetic), P(boundary marker). "
            "Generates a per-sign classification table. Use after running "
            "SignFunctionEstimator or PositionalProfiler."
        ),
        "category": "General",
        "sections": [
            {
                "title": "Positional Classes",
                "data_source": "experiment",
                "data_key": "class_summary",
                "chart_type": "table",
                "include_table": True,
                "description": "Count of INITIAL / MEDIAL / TERMINAL / MIXED signs.",
            },
            {
                "title": "Per-Sign Profiles",
                "data_source": "experiment",
                "data_key": "profiles",
                "chart_type": "table",
                "include_table": True,
                "description": "I/M/T rates and dominant position class per sign.",
            },
            {
                "title": "Symbol Clusters",
                "data_source": "experiment",
                "data_key": "clusters",
                "chart_type": "table",
                "include_table": True,
                "description": "Signs grouped by positional behaviour.",
            },
        ],
    },
    {
        "id": "tmpl-writing-system-fingerprint",
        "name": "Writing System Fingerprint Report",
        "description": (
            "10-dimensional structural fingerprint of any corpus, compared against "
            "a database of known writing systems. Returns nearest known script, "
            "distance score, and tier classification (abjad/syllabary/logosyllabic/logographic). "
            "Use after running WritingSystemClassifier or StructuralFingerprint."
        ),
        "category": "Structural Analysis",
        "sections": [
            {
                "title": "Tier Classification",
                "data_source": "experiment",
                "data_key": "tier_classification",
                "chart_type": "text",
                "include_table": False,
                "description": "Rule-based writing system tier (abjad/syllabary/logosyllabic/logographic).",
            },
            {
                "title": "Nearest Known Script",
                "data_source": "experiment",
                "data_key": "nearest_script",
                "chart_type": "text",
                "include_table": False,
                "description": "Closest match in the benchmark script database.",
            },
            {
                "title": "Distance Score",
                "data_source": "experiment",
                "data_key": "nearest_distance",
                "chart_type": "text",
                "include_table": False,
                "description": "Euclidean distance to nearest script. Lower = closer match.",
            },
            {
                "title": "Top 3 Nearest Scripts",
                "data_source": "experiment",
                "data_key": "top3_nearest",
                "chart_type": "table",
                "include_table": True,
                "description": "Ranked table of 3 closest known writing systems.",
            },
            {
                "title": "Classification Summary",
                "data_source": "experiment",
                "data_key": "text",
                "chart_type": "text",
                "include_table": False,
                "description": "Human-readable classification statement.",
            },
        ],
    },
    {
        "id": "tmpl-session-summary",
        "name": "Research Session Summary",
        "description": (
            "High-level summary of research progress for any session. "
            "Records key findings, next steps, and open questions. "
            "Designed for use with Glossa AI synthesis: select multiple data "
            "files in Compose mode then click AI Report to auto-generate."
        ),
        "category": "Research Summary",
        "sections": [
            {
                "title": "Key Findings",
                "data_source": "experiment",
                "data_key": "conclusions",
                "chart_type": "text",
                "include_table": False,
                "description": "Main conclusions from the experiment or session.",
            },
            {
                "title": "Quantitative Results",
                "data_source": "experiment",
                "data_key": "summary_table",
                "chart_type": "table",
                "include_table": True,
                "description": "Numerical results table.",
            },
            {
                "title": "Status / Verdict",
                "data_source": "experiment",
                "data_key": "verdict",
                "chart_type": "text",
                "include_table": False,
                "description": "Pass / Fail / Partial verdict for the experiment.",
            },
        ],
    },
]

async def seed_report_templates() -> int:
    """Seed default report templates (idempotent — skips existing IDs).

    Returns the number of templates inserted (0 if all already present).
    """
    from glossa_lab.database import get_db  # noqa: PLC0415

    db = get_db()
    if db is None:
        logger.warning("report_template_seeder: database not available")
        return 0

    assert db._conn  # noqa: SLF001
    inserted = 0
    for tmpl in DEFAULT_TEMPLATES:
        # Check if already present
        cursor = await db._conn.execute(  # noqa: SLF001
            "SELECT id FROM report_templates WHERE id = ?", (tmpl["id"],)
        )
        row = await cursor.fetchone()
        if row:
            continue  # already seeded — never overwrite user edits
        import json  # noqa: PLC0415
        await db._conn.execute(  # noqa: SLF001
            """INSERT INTO report_templates
               (id, name, description, category, sections, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                tmpl["id"],
                tmpl["name"],
                tmpl["description"],
                tmpl["category"],
                json.dumps(tmpl["sections"]),
                _now(),
                _now(),
            ),
        )
        inserted += 1

    if inserted:
        await db._conn.commit()  # noqa: SLF001
        logger.info("Report template seeder: inserted %d default templates", inserted)
    return inserted
