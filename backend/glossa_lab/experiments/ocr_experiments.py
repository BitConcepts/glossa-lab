"""OCR experiment wrappers for Mahadevan (1977) extraction.

These are registered as ExperimentBase subclasses so they appear in the
Experiments tab. They require mistral_api_key and take significant time,
so run() raises NotImplementedError (use Stream mode or CLI command).
"""

from __future__ import annotations

try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object  # type: ignore[assignment,misc]


class OcrBigramTables(_EB):
    id = "ocr_tables"
    name = "OCR — Bigram & Frequency Tables"
    category = "Data Extraction"
    description = "Mistral OCR on Mahadevan (1977) table pages. Extracts bigram matrix."
    estimated_time = "~30 min"
    requires_key = "mistral_api_key"
    command = "python ocr_mahadevan.py --target tables"
    results_file = "reports/mahadevan_bigrams.json"

    def run(self, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            "OCR takes ~30 min. Use the CLI command or Stream button in the UI."
        )


class OcrInscriptionTexts(_EB):
    id = "ocr_texts"
    name = "OCR — Inscription Sequences (2906 texts)"
    category = "Data Extraction"
    description = "Mistral OCR on Mahadevan (1977) inscription pages. Extracts sign sequences."
    estimated_time = "~2 hours"
    requires_key = "mistral_api_key"
    command = "python ocr_mahadevan.py --target texts"
    results_file = "reports/mahadevan_texts.json"

    def run(self, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            "OCR takes ~2 hours. Use the CLI command or Stream button in the UI."
        )
