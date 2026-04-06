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

# Catalog only contains experiments NOT yet registered as ExperimentBase subclasses.
# All other experiments (structural atlas, Kandles bias, Ventris, etc.) are
# auto-discovered from backend/glossa_lab/experiments/ via ExperimentBase.
_EXPERIMENT_CATALOG: list[dict[str, Any]] = [
    {
        "id": "ocr_tables",
        "name": "OCR — Bigram & Frequency Tables",
        "category": "Data Extraction",
        "description": "Mistral OCR on Mahadevan (1977) table pages. Extracts bigram matrix.",
        "command": "python ocr_mahadevan.py --target tables",
        "results_file": "reports/mahadevan_bigrams.json",
        "requires_key": "mistral_api_key",
        "estimated_time": "~30 min",
    },
    {
        "id": "ocr_texts",
        "name": "OCR — Inscription Sequences (2906 texts)",
        "category": "Data Extraction",
        "description": "Mistral OCR on Mahadevan (1977) inscription pages. Extracts sign sequences",
        "command": "python ocr_mahadevan.py --target texts",
        "results_file": "reports/mahadevan_texts.json",
        "requires_key": "mistral_api_key",
        "estimated_time": "~2 hours",
    },
]

# Per-model descriptions tuned to Glossa Lab use cases.
# Each entry: (model_id, description, tags)
_MODEL_DESCRIPTIONS: dict[str, dict[str, str]] = {
    # OpenAI
    "gpt-5.4": {
        "description": "Best all-round reasoning model. Use for complex decipherment analysis, "
        "hypothesis generation, sign mapping disambiguation, and long-context "
        "synthesis tasks.",
        "use_for": "Hypothesis engine, complex analysis, agentic sessions",
    },
    "gpt-5.4-mini": {
        "description": "Faster, cheaper variant of gpt-5.4. Use for batch experiment runs, "
        "automated pipelines, and text classification tasks where "
        "full reasoning depth is not required.",
        "use_for": "Batch analysis, fast pipelines, classification",
    },
    "gpt-5.4-pro": {
        "description": "Most capable OpenAI model. Use for the most demanding tasks: "
        "full decipherment hypothesis synthesis, academic report writing, "
        "and multi-document corpus analysis.",
        "use_for": "Full decipherment synthesis, academic writing",
    },
    # Anthropic
    "claude-opus-4-6": {
        "description": "Anthropic's most capable model. Excellent at long-form academic "
        "text analysis, multi-step corpus comparison, and nuanced "
        "linguistic reasoning. Strong alternative to gpt-5.4-pro.",
        "use_for": "Deep linguistic analysis, academic synthesis",
    },
    "claude-sonnet-4-6": {
        "description": "Balanced capability and speed. Use for iterative experiment "
        "pipelines, script analysis, and generating experiment summaries. "
        "Good cost-performance for agentic sessions.",
        "use_for": "Pipelines, summaries, agentic sessions",
    },
    "claude-haiku-4-5": {
        "description": "Fastest and cheapest Claude. Use for high-volume tasks: "
        "classifying many sign sequences, filtering corpus data, "
        "or checking format validity.",
        "use_for": "High-volume classification, format checking",
    },
    # Google
    "gemini-3.1-pro-preview": {
        "description": "Google's most capable model. Strong multimodal reasoning. "
        "Use for cross-script visual comparison, sign image analysis, "
        "and complex reasoning tasks requiring long context.",
        "use_for": "Visual analysis, cross-script comparison",
    },
    "gemini-3-flash-preview": {
        "description": "Fast, efficient Gemini model. Use for quick structural analysis, "
        "batch sign classification, and experiment runs where "
        "latency matters.",
        "use_for": "Fast batch analysis, experiment runs",
    },
    "gemini-3.1-flash-lite-preview": {
        "description": "Lightest Gemini variant. Use for high-volume preprocessing, "
        "corpus filtering, and format conversion tasks.",
        "use_for": "Preprocessing, corpus filtering",
    },
    "gemini-2.5-pro": {
        "description": "Stable Gemini Pro. Reliable for mixed text+image tasks. "
        "Good choice when you need consistent results across "
        "long analysis sessions.",
        "use_for": "Stable mixed-modality analysis",
    },
    # Mistral
    "mistral-ocr-latest": {
        "description": "REQUIRED for Mahadevan OCR. Purpose-built document OCR model -- "
        "extracts text from scanned book pages significantly better than "
        "general vision models. No rate limits seen in practice for this "
        "project's page volumes.",
        "use_for": "Mahadevan OCR (primary), any scanned document extraction",
    },
    "mistral-ocr-2512": {
        "description": "Stable Mistral OCR model (Dec 2025). Same as mistral-ocr-latest. "
        "Use when you need version pinning for reproducibility.",
        "use_for": "OCR with version pinning",
    },
    "mistral-ocr-2505": {
        "description": "Earlier Mistral OCR build (May 2025). Fallback if later versions "
        "are unavailable.",
        "use_for": "OCR fallback",
    },
    "mistral-large-2512": {
        "description": "Mistral's large language model. Use for text analysis, "
        "sign sequence interpretation, and linguistic hypothesis scoring "
        "when you prefer Mistral's output style.",
        "use_for": "Text analysis, linguistic reasoning",
    },
    "devstral-2512": {
        "description": "Mistral coding model. Use for generating experiment code, "
        "writing parsing scripts, and automating pipeline logic. "
        "Strong at Python and JSON manipulation.",
        "use_for": "Experiment code generation, pipeline scripting",
    },
    "pixtral-large-latest": {
        "description": "Large Mistral vision model. Fallback if mistral-ocr is unavailable. "
        "Also useful for analysing sign drawings and comparing "
        "visual inscription layouts.",
        "use_for": "Vision fallback, sign drawing analysis",
    },
    "pixtral-large-2411": {
        "description": "Stable Pixtral Large (Nov 2024). Version-pinned alternative to "
        "pixtral-large-latest for reproducible vision tasks.",
        "use_for": "Version-pinned vision tasks",
    },
    "pixtral-12b-2409": {
        "description": "Earlier 12B Pixtral model. Superseded by mistral-ocr-latest for "
        "document OCR. Retained for backward compatibility.",
        "use_for": "Legacy OCR tasks only",
    },
}


def _enrich_model(model_id: str) -> dict[str, str]:
    meta = _MODEL_DESCRIPTIONS.get(model_id, {})
    return {
        "id": model_id,
        "description": meta.get("description", ""),
        "use_for": meta.get("use_for", ""),
    }


_PROVIDER_CATALOG: list[dict[str, Any]] = [
    {
        "id": "openai",
        "label": "OpenAI",
        "api_key_setting": "openai_api_key",
        "supports_live_model_discovery": True,
        "recommended_models": ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-pro"],
        "model_details": [_enrich_model(m) for m in ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-pro"]],
        "ocr_preferred_models": [],
    },
    {
        "id": "anthropic",
        "label": "Anthropic",
        "api_key_setting": "anthropic_api_key",
        "supports_live_model_discovery": True,
        "recommended_models": ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5"],
        "model_details": [
            _enrich_model(m) for m in ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5"]
        ],
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
        "model_details": [
            _enrich_model(m)
            for m in [
                "gemini-3.1-pro-preview",
                "gemini-3-flash-preview",
                "gemini-3.1-flash-lite-preview",
                "gemini-2.5-pro",
            ]
        ],
        "ocr_preferred_models": [],
    },
    {
        "id": "mistral",
        "label": "Mistral",
        "api_key_setting": "mistral_api_key",
        "supports_live_model_discovery": True,
        "recommended_models": [
            "mistral-ocr-latest",
            "mistral-ocr-2512",
            "mistral-large-2512",
            "devstral-2512",
            "pixtral-large-latest",
            "pixtral-12b-2409",
        ],
        "model_details": [
            _enrich_model(m)
            for m in [
                "mistral-ocr-latest",
                "mistral-ocr-2512",
                "mistral-large-2512",
                "devstral-2512",
                "pixtral-large-latest",
                "pixtral-12b-2409",
            ]
        ],
        "ocr_preferred_models": ["mistral-ocr-latest", "mistral-ocr-2512"],
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
