"""Evidence Graph Atomic Nodes — Glossa-Lab Experiment Builder.

Registers a new palette category "Evidence Graph" containing 7 atomic
computation nodes that operate on the glossa-indus evidence graph data:

  IndusLiteratureLoader   Load registered papers from literature/documents/
  IndusClaimsLoader       Load extracted claims with type/status filters
  CrossHypothesisMatrix   Build agree/conflict/untested matrix across claims
  HiddenHypothesisGen     Derive compound testable hypotheses from intersections
  IndusClaimTester        Test positional claims against a corpus input
  IndusNullModelTest      Run a null-model check for sign-position hypotheses
  IndusIntakeRunner       Trigger the intake + claims pipeline on pending files

Port type added by this module:
  claims  #b45309 (amber) — list of claim records
  papers  #0891b2 (cyan)  — list of paper/document records
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from glossa_lab.experiment_graph import AtomicNodeDef

_REPO_ROOT     = Path(__file__).resolve().parent.parent.parent
_EVIDENCE_BASE = _REPO_ROOT / "glossa-indus"
_LIT_DOCS      = _EVIDENCE_BASE / "literature" / "documents"
_CLAIMS_DIR    = _EVIDENCE_BASE / "claims" / "extracted_claims"
_HYPO_MODELS   = _EVIDENCE_BASE / "hypotheses" / "models"
_SCRIPTS       = _EVIDENCE_BASE / "scripts"


# ── Node implementations ────────────────────────────────────────────────────

def _literature_loader(inputs: dict, params: dict) -> dict:
    """Load registered literature documents from glossa-indus/literature/documents/.

    Spec 087 S3 PR-F: delegates to the generic JsonRecordDirLoader
    (search mode); the evidence-base paths and field names are spec data
    resolved from this module's constants at call time.
    """
    from glossa_lab.generic_loaders import json_record_dir_loader_execute

    spec = {
        "mode": "search",
        "directory": str(_LIT_DOCS),
        "ensure_dir": True,
        "query_param": "query",
        "max_param": "max_papers",
        "max_default": 200,
        "search_title_field": "detected_title",
        "search_authors_field": "detected_authors",
        "projection": [
            {"out": "document_id", "from": "document_id", "default_stem": True},
            {"out": "title", "from": "detected_title", "default": ""},
            {"out": "authors", "from": "detected_authors", "default": []},
            {"out": "year", "from": "detected_year"},
            {"out": "doi", "from": "detected_doi"},
            {"out": "status", "from": "processing_status", "default": ""},
        ],
        "count_from": {
            "out": "claim_count",
            "directory": str(_CLAIMS_DIR),
            "key_field": "document_id",
            "value_field": "total_claims",
            "default": 0,
        },
        "items_key": "papers",
        "count_key": "total_papers",
        "text_template": "Loaded {n} registered papers.",
    }
    merged = dict(params)
    merged["loader_spec"] = spec
    return json_record_dir_loader_execute(inputs, merged)


def _claims_loader(inputs: dict, params: dict) -> dict:
    """Load extracted claims with optional type/status/sign filters.

    Spec 087 S3 PR-F: delegates to the generic JsonRecordDirLoader
    (records mode); the claims directory, the upstream-papers stem
    restriction, the three filters, the counts and the text shape are
    spec data. No schema defaults are applied — the historical loader
    passes claim records through unchanged (its "unknown" fallbacks
    live only in the counts, carried here as count defaults).
    """
    from glossa_lab.generic_loaders import json_record_dir_loader_execute

    spec = {
        "mode": "records",
        "directory": str(_CLAIMS_DIR),
        "ensure_dir": True,
        "items_key": "claims",
        "out_items_key": "claims",
        "count_key": "total_claims",
        "sources_key": "source_docs",
        "max_param": "max_claims",
        "max_default": 500,
        "restrict": {"input_key": "papers", "id_field": "document_id"},
        "schema_defaults": {},
        "filters": [
            {"param": "claim_type", "field": "claim_type", "kind": "equals"},
            {"param": "claim_status", "field": "claim_status", "kind": "equals"},
            {"param": "sign_filter", "kind": "substring_any",
             "fields": ["signs_involved", "normalized_claim"]},
        ],
        "counts": [
            {"out": "type_counts", "field": "claim_type", "default": "unknown"},
            {"out": "status_counts", "field": "claim_status", "default": "unknown"},
        ],
        "json_counts": ["type_counts"],
        "text_types": {"from_counts": "type_counts", "limit": 5},
        "text_template": "Loaded {n} claims from {n_sources} docs. Types: {types}",
    }
    merged = dict(params)
    merged["loader_spec"] = spec
    return json_record_dir_loader_execute(inputs, merged)


def _cross_hypothesis_matrix(inputs: dict, params: dict) -> dict:
    """Group claims by theme/sign and compute agree/conflict/untested matrix."""
    claims = inputs.get("claims") or []
    if not claims:
        return {"error": "No claims — connect IndusClaimsLoader.claims"}

    group_by = str(params.get("group_by", "sign") or "sign").lower()

    # Group claims by sign or by claim_type
    groups: dict[str, list[dict]] = {}
    for c in claims:
        if group_by == "sign":
            keys = c.get("signs_involved") or []
            if not keys:
                # Try to extract sign from normalized_claim
                nc = c.get("normalized_claim", "")
                m  = re.search(r"\b(fish|arrow|unicorn|jar|cattle|boat|buffalo)\b", nc, re.IGNORECASE)
                keys = [m.group(0).lower()] if m else ["unclassified"]
        else:
            keys = [c.get("claim_type", "unknown")]
        for k in keys:
            groups.setdefault(k, []).append(c)

    matrix: list[dict] = []
    for group_key, group_claims in sorted(groups.items(), key=lambda x: -len(x[1])):
        sources    = list({c.get("source_document_id", "") for c in group_claims if c.get("source_document_id")})
        statuses   = [c.get("claim_status", "untested") for c in group_claims]
        n_support  = sum(1 for s in statuses if s in ("strongly_supported", "partially_supported"))
        n_falsified = sum(1 for s in statuses if "falsified" in s or s == "contradicted")
        n_untested = sum(1 for s in statuses if s == "untested")
        verdict    = (
            "conflict"   if n_support > 0 and n_falsified > 0 else
            "supported"  if n_support > 0 else
            "falsified"  if n_falsified > 0 else
            "untested"
        )
        matrix.append({
            "group":       group_key,
            "n_claims":    len(group_claims),
            "n_sources":   len(sources),
            "sources":     sources,
            "n_supported": n_support,
            "n_falsified": n_falsified,
            "n_untested":  n_untested,
            "verdict":     verdict,
            "claims":      group_claims,
        })

    n_conflicts = sum(1 for r in matrix if r["verdict"] == "conflict")
    return {
        "matrix":      matrix,
        "n_groups":    len(matrix),
        "n_conflicts": n_conflicts,
        "json":        {"matrix": matrix, "n_conflicts": n_conflicts},
        "text": (
            f"Cross-hypothesis matrix: {len(matrix)} groups, "
            f"{n_conflicts} conflicts, grouped by {group_by}."
        ),
    }


def _hidden_hypothesis_gen(inputs: dict, params: dict) -> dict:
    """Derive compound testable hypotheses from cross-paper claim intersections.

    A hidden hypothesis is a prediction that follows logically from combining
    two or more claims from different papers, but that no single paper explicitly
    states.  Examples:
      - Parpola: fish=meen + Yadav: initial signs are titles → fish should be
        title-initial, testable via positional enrichment at Lothal
      - Hunt: faunal-prefix + Roif: fish=coastal → coastal fish-prefix
        hypothesis, testable via site-stratified positional analysis
    """
    claims = inputs.get("claims") or []
    inputs.get("matrix") or []  # from CrossHypothesisMatrix
    min_sources = int(params.get("min_sources_per_hypothesis", 2) or 2)

    if not claims:
        return {"error": "No claims — connect IndusClaimsLoader.claims (and optionally CrossHypothesisMatrix.matrix)"}

    # Index claims by type and by sign
    positional_claims: list[dict] = [c for c in claims if "position" in (c.get("claim_type") or "")]
    sign_value_claims: list[dict] = [c for c in claims if "sign_value" in (c.get("claim_type") or "") or "sign_function" in (c.get("claim_type") or "")]
    archaeological_claims: list[dict] = [c for c in claims if "archaeological" in (c.get("claim_type") or "")]
    language_claims: list[dict] = [c for c in claims if "language" in (c.get("claim_type") or "")]

    hypotheses: list[dict] = []

    # Pattern 1: sign_value × positional → compound site-enrichment hypothesis
    for sv in sign_value_claims[:20]:
        sv_signs = sv.get("signs_involved") or []
        sv_value = sv.get("proposed_value") or sv.get("normalized_claim", "")[:60]
        sv_src   = sv.get("source_document_id", "?")
        for pos in positional_claims[:20]:
            pos_src = pos.get("source_document_id", "?")
            if pos_src == sv_src:
                continue  # same paper — not a hidden cross-paper hypothesis
            pos_claim = pos.get("normalized_claim", "")
            pos_class = (
                "initial" if "initial" in pos_claim.lower() else
                "terminal" if "terminal" in pos_claim.lower() else None
            )
            if not pos_class:
                continue
            for sign in sv_signs:
                hyp_text = (
                    f"If '{sign}' encodes '{sv_value}' [{sv_src}] AND {pos_class} signs "
                    f"function as {('titles/determinatives' if pos_class == 'initial' else 'case suffixes')} [{pos_src}], "
                    f"then '{sign}' should be statistically enriched in {pos_class} position. "
                    f"Testable via chi-squared on V1 corpus positional profiles."
                )
                hypotheses.append({
                    "hypothesis_id":    f"hidden_{sign}_{pos_class}_{len(hypotheses):04d}",
                    "derived_from":     [sv_src, pos_src],
                    "n_sources":        2,
                    "hypothesis_text":  hyp_text,
                    "hypothesis_type":  "sign_position_compound",
                    "key_sign":         sign,
                    "predicted_position": pos_class,
                    "testability":      "directly_testable",
                    "test_method":      f"Chi-squared: {sign} {pos_class}_rate vs corpus average. Null model comparison.",
                    "status":           "unregistered",
                })
                if len(hypotheses) >= 50:
                    break
            if len(hypotheses) >= 50:
                break

    # Pattern 2: archaeological × language → site-language prediction
    for arch in archaeological_claims[:10]:
        arch_src = arch.get("source_document_id", "?")
        for lang in language_claims[:10]:
            lang_src = lang.get("source_document_id", "?")
            if lang_src == arch_src:
                continue
            hyp_text = (
                f"If {arch.get('normalized_claim','')[:100]} [{arch_src}] AND "
                f"{lang.get('normalized_claim','')[:80]} [{lang_src}], "
                f"then site-stratified sign distributions should reflect this prediction. "
                f"Testable via site-type metadata cross-tabulation."
            )
            hypotheses.append({
                "hypothesis_id":   f"hidden_arch_lang_{len(hypotheses):04d}",
                "derived_from":    [arch_src, lang_src],
                "n_sources":       2,
                "hypothesis_text": hyp_text,
                "hypothesis_type": "site_language_compound",
                "testability":     "indirectly_testable",
                "test_method":     "Site-type metadata cross-tabulation.",
                "status":          "unregistered",
            })
            if len(hypotheses) >= 80:
                break

    # Filter by min_sources
    hypotheses = [h for h in hypotheses if h.get("n_sources", 0) >= min_sources]

    return {
        "hypotheses":      hypotheses,
        "total_hypotheses": len(hypotheses),
        "json": {"hypotheses": hypotheses},
        "text": (
            f"Generated {len(hypotheses)} hidden compound hypotheses "
            f"from {len(set(src for h in hypotheses for src in h.get('derived_from', [])))} source papers."
        ),
    }


def _claim_tester(inputs: dict, params: dict) -> dict:
    """Test directly-testable positional claims against corpus sequences.

    Spec 087 S3 PR-F: delegates to the generic PositionalClaimTester;
    the testable type keywords, the position needles, the corpus-average
    support rule (observed >= average x 1.2 over signs with >= 3
    occurrences) and the error texts are spec data.
    """
    from glossa_lab.generic_primitives import positional_claim_tester_execute

    spec = {
        "type_keywords": ["position", "sign_value", "sign_function"],
        "positions": [["initial", "initial"], ["terminal", "terminal"]],
        "positional_min_length": 1,
        "min_count_for_avg": 3,
        "support_multiplier": 1.2,
        "sign_cap": 4,
        "source_truncate": 100,
        "no_sequences_error": "No sequences — connect BuiltinCorpus or CorpusReader.sequences to the 'sequences' port",
        "no_claims_error": "No claims — connect IndusClaimsLoader.claims",
        "text_template": "Tested {n_total} sign-position claims: {n_supp}/{n_total} supported ({pct}%).",
    }
    merged = dict(params)
    merged["tester_spec"] = spec
    return positional_claim_tester_execute(inputs, merged)


def _null_model_test(inputs: dict, params: dict) -> dict:
    """Run positional null model for sign-position or formula hypotheses.

    Tests whether the observed initial/terminal rate for a sign is explained
    by random shuffling alone (shuffle null) or frequency alone (freq null).

    Spec 087 S3 (family F9): the mechanism is the generic
    SignPositionNullTest engine (glossa_lab.generic_primitives);
    this node is its Indus-evidence parameterisation — the
    z-verdict bands (3 / 2 / 1.5) and the fallback verdict are
    passed as null_spec data. Per the triage's caution, the
    engine is a separate sequence-shaped primitive and does NOT
    reuse the score-shaped generic PermutationTest.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        sign_position_null_test_execute,
    )

    merged = dict(params)
    spec = dict(merged.get("null_spec") or {})
    spec.setdefault("verdict_bands", [
        [3, "STRONGLY_SIGNIFICANT"],
        [2, "SIGNIFICANT"],
        [1.5, "BORDERLINE"],
    ])
    spec.setdefault("verdict_fallback", "NOT_SIGNIFICANT")
    merged["null_spec"] = spec
    return sign_position_null_test_execute(inputs, merged)


def _intake_runner(inputs: dict, params: dict) -> dict:
    """Trigger the glossa-indus intake + claims extraction pipeline."""
    import subprocess  # noqa: PLC0415
    import sys  # noqa: PLC0415

    intake = _SCRIPTS / "indus_intake.py"
    claims = _SCRIPTS / "indus_claims.py"

    results: list[dict] = []
    for script, extra_args in [(intake, ["--scan", str(_EVIDENCE_BASE / "raw" / "user_uploads")]), (claims, [])]:
        if not script.exists():
            results.append({"script": script.name, "status": "not_found"})
            continue
        try:
            r = subprocess.run(
                [sys.executable, str(script)] + extra_args,
                capture_output=True, text=True, timeout=300,
            )
            results.append({
                "script":      script.name,
                "status":      "ok" if r.returncode == 0 else "error",
                "returncode":  r.returncode,
                "stdout_tail": r.stdout[-400:] if r.stdout else "",
                "stderr_tail": r.stderr[-200:] if r.stderr else "",
            })
        except Exception as exc:  # noqa: BLE001
            results.append({"script": script.name, "status": "exception", "error": str(exc)})

    ok = all(r.get("status") == "ok" for r in results)
    return {
        "pipeline_results": results,
        "all_ok":           ok,
        "json":             {"pipeline_results": results},
        "text": (
            "Intake + claims pipeline: ALL OK" if ok
            else "Intake + claims pipeline: ERRORS — see pipeline_results for details"
        ),
    }


# ── Node definitions ────────────────────────────────────────────────────────

def _evidence_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            id="IndusLiteratureLoader",
            name="Literature Loader",
            category="Evidence Graph",
            description="Load registered papers from the glossa-indus evidence graph library.",
            inputs=[],
            outputs=[
                {"name": "papers",       "type": "papers"},
                {"name": "total_papers", "type": "number"},
                {"name": "text",         "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "query":      {"type": "string",  "title": "Search Query",  "default": "",  "description": "Filter by title / author (optional)."},
                    "max_papers": {"type": "integer", "title": "Max Papers",    "default": 200, "description": "Maximum papers to load."},
                },
            },
            fn=_literature_loader,
        ),
        AtomicNodeDef(
            id="IndusClaimsLoader",
            name="Claims Loader",
            category="Evidence Graph",
            description="Load extracted claims with optional type, status, and sign filters.",
            inputs=[
                {"name": "papers", "type": "papers", "required": False},
            ],
            outputs=[
                {"name": "claims",        "type": "claims"},
                {"name": "total_claims",  "type": "number"},
                {"name": "type_counts",   "type": "json"},
                {"name": "status_counts", "type": "json"},
                {"name": "text",          "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "claim_type":   {"type": "string", "title": "Claim Type Filter",   "default": "", "description": "e.g. sign_value_claim, language_claim, sign_position_claim"},
                    "claim_status": {"type": "string", "title": "Claim Status Filter", "default": "", "description": "e.g. untested, partially_supported, partially_falsified"},
                    "sign_filter":  {"type": "string", "title": "Sign Filter",         "default": "", "description": "Keep only claims mentioning this sign."},
                    "max_claims":   {"type": "integer","title": "Max Claims",           "default": 500},
                },
            },
            fn=_claims_loader,
        ),
        AtomicNodeDef(
            id="CrossHypothesisMatrix",
            name="Cross-Hypothesis Matrix",
            category="Evidence Graph",
            description="Group claims by sign or type and compute agree/conflict/untested verdicts.",
            inputs=[
                {"name": "claims", "type": "claims", "required": True},
            ],
            outputs=[
                {"name": "matrix",       "type": "json"},
                {"name": "n_conflicts",  "type": "number"},
                {"name": "json",         "type": "json"},
                {"name": "text",         "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "group_by": {"type": "string", "title": "Group By", "default": "sign",
                                 "description": "'sign' groups by signs_involved; 'claim_type' groups by claim type."},
                },
            },
            fn=_cross_hypothesis_matrix,
        ),
        AtomicNodeDef(
            id="HiddenHypothesisGen",
            name="Hidden Hypothesis Generator",
            category="Evidence Graph",
            description="Derive compound testable hypotheses from cross-paper claim intersections.",
            inputs=[
                {"name": "claims", "type": "claims",  "required": True},
                {"name": "matrix", "type": "json",    "required": False},
            ],
            outputs=[
                {"name": "hypotheses",       "type": "json"},
                {"name": "total_hypotheses", "type": "number"},
                {"name": "json",             "type": "json"},
                {"name": "text",             "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_sources_per_hypothesis": {
                        "type": "integer", "title": "Min Source Papers", "default": 2,
                        "description": "Minimum number of distinct papers a hypothesis must draw from.",
                    },
                },
            },
            fn=_hidden_hypothesis_gen,
        ),
        AtomicNodeDef(
            id="IndusClaimTester",
            name="Claim Tester",
            category="Evidence Graph",
            description="Test directly-testable positional claims against a corpus. Outputs per-sign verdicts.",
            inputs=[
                {"name": "claims",    "type": "claims",    "required": True},
                {"name": "sequences", "type": "sequences", "required": True},
            ],
            outputs=[
                {"name": "test_results",  "type": "json"},
                {"name": "n_tested",      "type": "number"},
                {"name": "support_rate",  "type": "number"},
                {"name": "json",          "type": "json"},
                {"name": "text",          "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {},
            },
            fn=_claim_tester,
        ),
        AtomicNodeDef(
            id="IndusNullModelTest",
            name="Null Model Test",
            category="Evidence Graph",
            description="Run a shuffle null model for a single sign's positional enrichment.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
            ],
            outputs=[
                {"name": "z_score",    "type": "number"},
                {"name": "p_approx",   "type": "number"},
                {"name": "verdict",    "type": "text"},
                {"name": "json",       "type": "json"},
                {"name": "text",       "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "target_sign":  {"type": "string",  "title": "Target Sign",   "default": "",     "description": "Sign code to test, e.g. 'M77/72'"},
                    "test_type":    {"type": "string",  "title": "Position Type", "default": "initial", "description": "'initial' or 'terminal'"},
                    "n_null_runs":  {"type": "integer", "title": "Null Runs",     "default": 1000,   "description": "Number of shuffle runs for null distribution."},
                    "random_seed":  {"type": "integer", "title": "Random Seed",   "default": 42},
                },
            },
            fn=_null_model_test,
        ),
        AtomicNodeDef(
            id="IndusIntakeRunner",
            name="Intake Runner",
            category="Evidence Graph",
            description="Trigger the intake + claims extraction pipeline on all pending uploads.",
            inputs=[],
            outputs=[
                {"name": "pipeline_results", "type": "json"},
                {"name": "all_ok",           "type": "number"},
                {"name": "text",             "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {},
            },
            fn=_intake_runner,
        ),
    ]
