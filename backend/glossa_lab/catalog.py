"""Shared backend catalog metadata for admin/dashboard surfaces."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from glossa_lab.engine import get_registered_pipeline_info

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_REPORTS_DIR = _REPO_ROOT / "reports"

_PIPELINE_METADATA: dict[str, dict[str, Any]] = {
    "block_entropy": {
        "label": "Block Entropy",
        "group": "Statistical (no LM)",
        "description": "Computes H_n and normalized entropy profiles across block sizes.",
        "inputs": "text_id, max_n",
        "outputs": "block_entropies[], normalized values, classification",
        "default_params": {"text_id": "", "max_n": 6},
        "needs_lm": False,
    },
    "char_freq": {
        "label": "Character Frequency",
        "group": "Statistical (no LM)",
        "description": "Builds sign frequency distributions and Zipf-style rank curves.",
        "inputs": "text_id",
        "outputs": "frequencies, rank_frequency[], zipf_exponent",
        "default_params": {"text_id": ""},
        "needs_lm": False,
    },
    "cooccurrence": {
        "label": "Co-occurrence Network",
        "group": "Statistical (no LM)",
        "description": "Constructs sign co-occurrence graphs and community structure.",
        "inputs": "text_id, window, min_freq, min_edge_weight",
        "outputs": "node_count, edge_count, community_count, communities[]",
        "default_params": {
            "text_id": "",
            "window": 2,
            "min_freq": 3,
            "min_edge_weight": 2,
        },
        "needs_lm": False,
    },
    "decipher": {
        "label": "Decipher (Substitution Cipher)",
        "group": "Language Model Required",
        "description": "Hill-climbing substitution solver against a target language model.",
        "inputs": "text_id, target_text_id, max_iterations, restarts",
        "outputs": "proposed_mapping{}, kandles_confidence, score",
        "default_params": {
            "text_id": "",
            "target_text_id": "",
            "max_iterations": 5000,
        },
        "needs_lm": True,
    },
    "distributional_decipherment": {
        "label": "Distributional Decipherment",
        "group": "Statistical (no LM)",
        "description": "Clusters signs by distributional behavior without language assumptions.",
        "inputs": "text_id, target_language",
        "outputs": "vowel_clusters[], consonant_clusters[], sign_classification{}",
        "default_params": {"text_id": "", "target_language": "generic"},
        "needs_lm": False,
    },
    "hypothesis": {
        "label": "Hypothesis Engine",
        "group": "Language Model Required",
        "description": "Iterative multi-hypothesis search across language families.",
        "inputs": "text_id, max_iterations",
        "outputs": "results[] with scores per hypothesis, suggested_next[]",
        "default_params": {"text_id": "", "max_iterations": 5000},
        "needs_lm": True,
    },
    "kandles": {
        "label": "Kandles Fingerprint",
        "group": "Language Model Required",
        "description": "Computes phonological colour fingerprints for comparison workflows.",
        "inputs": "text_id, mode, profile",
        "outputs": "color_distribution{}, similarity score",
        "default_params": {"text_id": "", "mode": "grid"},
        "needs_lm": True,
    },
    "logosyllabic": {
        "label": "Logosyllabic Analysis (Ventris)",
        "group": "Statistical (no LM)",
        "description": "Ventris-style sign classing, affinity clustering, and candidate readings.",
        "inputs": "text_id, target_language",
        "outputs": "sign_classification{}, affinity{}, proposed_readings{}",
        "default_params": {"text_id": "", "target_language": "generic"},
        "needs_lm": False,
    },
    "numerals": {
        "label": "Numeral Detection",
        "group": "Statistical (no LM)",
        "description": "Identifies likely numeral signs from positional and frequency patterns.",
        "inputs": "text_id",
        "outputs": "numeral_candidates[], numeral_patterns[]",
        "default_params": {"text_id": ""},
        "needs_lm": False,
    },
    "nwsp": {
        "label": "NWSP — Fuls Method",
        "group": "Statistical (no LM)",
        "description": "Implements Fuls' Normalized Weighted Sign Position analysis.",
        "inputs": "text_id, min_occurrences",
        "outputs": "signs[] with histogram, classification, ICIT code mapping",
        "default_params": {"text_id": "", "min_occurrences": 4},
        "needs_lm": False,
    },
    "paradigm": {
        "label": "Paradigm Detection",
        "group": "Statistical (no LM)",
        "description": "Finds paradigmatic alternations and recurring stem/variant structures.",
        "inputs": "text_id, min_stem_freq, min_variants",
        "outputs": "paradigm_count, paradigms[]",
        "default_params": {"text_id": "", "min_stem_freq": 2, "min_variants": 2},
        "needs_lm": False,
    },
    "positional": {
        "label": "Positional Analysis",
        "group": "Statistical (no LM)",
        "description": "Computes sign-level initial, medial, and terminal preferences.",
        "inputs": "text_id",
        "outputs": "profiles[] per sign with dominant_position",
        "default_params": {"text_id": ""},
        "needs_lm": False,
    },
    "sign_cluster": {
        "label": "Sign Clustering",
        "group": "Statistical (no LM)",
        "description": "Groups signs by similar contextual distributions.",
        "inputs": "text_id, min_freq, top_n",
        "outputs": "clusters[] with member signs",
        "default_params": {"text_id": "", "min_freq": 3, "top_n": 20},
        "needs_lm": False,
    },
    "sign_function_estimator": {
        "label": "Sign Function Estimator",
        "group": "Statistical (no LM)",
        "description": "Scores signs across numeral, logographic, phonetic, and boundary roles.",
        "inputs": "text_id, min_freq",
        "outputs": "signs[] with probabilities, system_summary, interpretation",
        "default_params": {"text_id": "", "min_freq": 3},
        "needs_lm": False,
    },
    "sign_polyvalence": {
        "label": "Sign Polyvalence",
        "group": "Statistical (no LM)",
        "description": "Detects bimodal positional behavior that suggests polyvalence.",
        "inputs": "text_id, min_freq",
        "outputs": "candidates[] sorted by bimodality_score",
        "default_params": {"text_id": "", "min_freq": 5},
        "needs_lm": False,
    },
    "structural_fingerprint": {
        "label": "Structural Fingerprint",
        "group": "Statistical (no LM)",
        "description": "Builds the multi-dimensional structural fingerprint used for comparison.",
        "inputs": "text_id, compare_to_db",
        "outputs": "vector[10], dimensions{}, nearest_scripts[], notes[]",
        "default_params": {"text_id": "", "compare_to_db": True},
        "needs_lm": False,
    },
    "word_structure_hypothesis": {
        "label": "Word-Structure Typology",
        "group": "Statistical (no LM)",
        "description": "Ranks language-family hypotheses from inscription length structure.",
        "inputs": "text_id",
        "outputs": "ranked_hypotheses[], winner, margin",
        "default_params": {"text_id": ""},
        "needs_lm": False,
    },
}

_EXPERIMENT_CATALOG: list[dict[str, Any]] = [
    {
        "id": "ocr_tables",
        "name": "OCR — Bigram & Frequency Tables",
        "category": "Data Extraction",
        "description": "OCR Mahadevan table pages and convert extracted signs to Fuls numbering.",
        "command": "python ocr_mahadevan.py --target tables",
        "results_file": "reports/mahadevan_bigrams.json",
        "requires_key": "mistral_api_key",
        "estimated_time": "~30 min",
    },
    {
        "id": "ocr_texts",
        "name": "OCR — Inscription Sequences",
        "category": "Data Extraction",
        "description": "OCR Mahadevan inscription pages to extract sequence-level corpora.",
        "command": "python ocr_mahadevan.py --target texts",
        "results_file": "reports/mahadevan_texts.json",
        "requires_key": "mistral_api_key",
        "estimated_time": "~2 hours",
    },
    {
        "id": "progression",
        "name": "Fuls Progression Benchmark",
        "category": "Validation",
        "description": "Runs the progression benchmark across the writing-system tiers.",
        "command": "python -m glossa_lab.experiments.progression_report",
        "results_file": "reports/progression.json",
        "estimated_time": "~1 min",
    },
    {
        "id": "indus_atlas",
        "name": "Indus Structural Atlas",
        "category": "Analysis",
        "description": "Generates the full structural atlas over Indus statistics and comparisons.",
        "command": "python -m glossa_lab.experiments.indus_structural_atlas",
        "results_file": "reports/indus_structural_atlas.json",
        "estimated_time": "~1 min",
    },
    {
        "id": "real_catalog",
        "name": "Real Catalog Analysis",
        "category": "Analysis",
        "description": "Analyzes real positional data extracted from the Fuls catalog.",
        "command": "python analyze_fuls_ebooks.py",
        "results_file": "reports/real_indus_catalog_analysis.json",
        "estimated_time": "~1 min",
    },
    {
        "id": "kandles_bias",
        "name": "Kandles Bias Comparison",
        "category": "Experiments",
        "description": "Compares Kandles scores with and without language-specific bias profiles.",
        "command": "python -m glossa_lab.experiments.run_kandles_biased_experiments --trials 30",
        "results_file": "reports/kandles_biased_results.json",
        "estimated_time": "~5 min",
    },
    {
        "id": "ventris_validation",
        "name": "Ventris Grid Validation (Linear B)",
        "category": "Validation",
        "description": "Validates the Ventris-style affinity workflow against Linear B.",
        "command": "python -m glossa_lab.experiments.ventris_validation",
        "estimated_time": "~10 sec",
    },
    {
        "id": "markov_model",
        "name": "Markov Model (Rao 2009 replication)",
        "category": "Analysis",
        "description": (
            "Builds the bigram Markov model once OCR-derived sequence data is available."
        ),
        "command": "python ocr_mahadevan.py --target texts",
        "requires_key": "mistral_api_key",
        "estimated_time": "After OCR",
    },
]

_PROVIDER_CATALOG: list[dict[str, Any]] = [
    {
        "id": "openai",
        "label": "OpenAI",
        "api_key_setting": "openai_api_key",
        "supports_live_model_discovery": True,
        "recommended_models": ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-pro"],
        "ocr_preferred_models": [],
    },
    {
        "id": "anthropic",
        "label": "Anthropic",
        "api_key_setting": "anthropic_api_key",
        "supports_live_model_discovery": True,
        "recommended_models": ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5"],
        "ocr_preferred_models": [],
    },
    {
        "id": "google",
        "label": "Google",
        "api_key_setting": "google_api_key",
        "supports_live_model_discovery": True,
        "recommended_models": [
            "gemini-3.1-pro-preview",
            "gemini-3-flash-preview",
            "gemini-3.1-flash-lite-preview",
            "gemini-2.5-pro",
        ],
        "ocr_preferred_models": [],
    },
    {
        "id": "mistral",
        "label": "Mistral",
        "api_key_setting": "mistral_api_key",
        "supports_live_model_discovery": True,
        "recommended_models": [
            "mistral-ocr-2512",
            "mistral-large-2512",
            "devstral-2512",
            "pixtral-12b-2409",
        ],
        "ocr_preferred_models": ["mistral-ocr-2512", "pixtral-12b-2409"],
    },
]


def list_pipeline_catalog() -> list[dict[str, Any]]:
    """Return pipeline metadata merged with the live registry."""
    entries: list[dict[str, Any]] = []
    for pipeline in get_registered_pipeline_info():
        metadata = _PIPELINE_METADATA.get(pipeline["name"], {})
        entries.append(
            {
                "id": pipeline["name"],
                "label": metadata.get("label", pipeline["name"].replace("_", " ").title()),
                "group": metadata.get("group", "Uncategorized"),
                "description": metadata.get("description", ""),
                "inputs": metadata.get("inputs", ""),
                "outputs": metadata.get("outputs", ""),
                "default_params": metadata.get("default_params", {}),
                "needs_lm": metadata.get("needs_lm", False),
                "registered": True,
                "module": pipeline["module"],
            }
        )
    return sorted(entries, key=lambda item: (item["group"], item["label"]))


def list_experiment_catalog() -> list[dict[str, Any]]:
    """Return curated experiment metadata."""
    return sorted(_EXPERIMENT_CATALOG, key=lambda item: (item["category"], item["name"]))


def list_provider_catalog() -> list[dict[str, Any]]:
    """Return curated provider and recommended-model metadata."""
    return list(_PROVIDER_CATALOG)


def list_report_catalog() -> list[dict[str, Any]]:
    """Return discovered report artifacts from the reports directory."""
    if not _REPORTS_DIR.exists():
        return []

    entries: list[dict[str, Any]] = []
    for path in sorted(_REPORTS_DIR.rglob("*")):
        if not path.is_file():
            continue
        stat = path.stat()
        suffix = path.suffix.lower()
        entries.append(
            {
                "id": path.stem,
                "name": path.name,
                "kind": _report_kind_for_suffix(suffix),
                "relative_path": path.relative_to(_REPO_ROOT).as_posix(),
                "size_bytes": stat.st_size,
                "updated_at": datetime.fromtimestamp(
                    stat.st_mtime,
                    tz=timezone.utc,
                ).isoformat(),
            }
        )
    return entries


def get_catalog_summary() -> dict[str, int]:
    """Return top-level catalog counts for dashboard status surfaces."""
    return {
        "pipelines": len(list_pipeline_catalog()),
        "experiments": len(list_experiment_catalog()),
        "reports": len(list_report_catalog()),
        "providers": len(list_provider_catalog()),
    }


def _report_kind_for_suffix(suffix: str) -> str:
    if suffix == ".json":
        return "json_report"
    if suffix == ".md":
        return "document"
    if suffix == ".csv":
        return "table"
    if suffix == ".pdf":
        return "pdf"
    return "artifact"
