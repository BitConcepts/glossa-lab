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
    """Load registered literature documents from glossa-indus/literature/documents/."""
    _LIT_DOCS.mkdir(parents=True, exist_ok=True)
    q          = str(params.get("query", "") or "").lower()
    max_papers = int(params.get("max_papers", 200) or 200)

    papers: list[dict[str, Any]] = []
    for f in sorted(_LIT_DOCS.glob("*.json")):
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if q:
            hay = ((d.get("detected_title") or "") + " " + " ".join(d.get("detected_authors") or [])).lower()
            if q not in hay:
                continue
        # Attach claim count
        claim_file = _CLAIMS_DIR / f"{d.get('document_id', f.stem)}.json"
        claim_count = 0
        if claim_file.exists():
            try:
                claim_count = json.loads(claim_file.read_text("utf-8")).get("total_claims", 0)
            except Exception:  # noqa: BLE001
                pass
        papers.append({
            "document_id": d.get("document_id", f.stem),
            "title":       d.get("detected_title", ""),
            "authors":     d.get("detected_authors", []),
            "year":        d.get("detected_year"),
            "doi":         d.get("detected_doi"),
            "claim_count": claim_count,
            "status":      d.get("processing_status", ""),
        })
        if len(papers) >= max_papers:
            break

    return {
        "papers":       papers,
        "total_papers": len(papers),
        "text":         f"Loaded {len(papers)} registered papers.",
    }


def _claims_loader(inputs: dict, params: dict) -> dict:
    """Load extracted claims with optional type/status/sign filters."""
    _CLAIMS_DIR.mkdir(parents=True, exist_ok=True)
    claim_type   = str(params.get("claim_type", "") or "").strip()
    claim_status = str(params.get("claim_status", "") or "").strip()
    sign_filter  = str(params.get("sign_filter", "") or "").lower().strip()
    max_claims   = int(params.get("max_claims", 500) or 500)

    all_claims: list[dict] = []
    source_files = []

    # If papers from upstream, restrict to those doc_ids
    upstream_papers = inputs.get("papers") or []
    allowed_ids = {p.get("document_id", "") for p in upstream_papers} if upstream_papers else None

    for f in sorted(_CLAIMS_DIR.glob("*.json")):
        if allowed_ids is not None and f.stem not in allowed_ids:
            continue
        try:
            record = json.loads(f.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        source_files.append(f.stem)
        for claim in record.get("claims", []):
            if claim_type and claim.get("claim_type") != claim_type:
                continue
            if claim_status and claim.get("claim_status") != claim_status:
                continue
            if sign_filter:
                signs = " ".join(claim.get("signs_involved") or [])
                if sign_filter not in signs.lower() and sign_filter not in (claim.get("normalized_claim") or "").lower():
                    continue
            all_claims.append(claim)
            if len(all_claims) >= max_claims:
                break
        if len(all_claims) >= max_claims:
            break

    type_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for c in all_claims:
        type_counts[c.get("claim_type", "unknown")] = type_counts.get(c.get("claim_type", "unknown"), 0) + 1
        status_counts[c.get("claim_status", "unknown")] = status_counts.get(c.get("claim_status", "unknown"), 0) + 1

    return {
        "claims":        all_claims,
        "total_claims":  len(all_claims),
        "source_docs":   len(source_files),
        "type_counts":   type_counts,
        "status_counts": status_counts,
        "json":          {"claims": all_claims, "type_counts": type_counts},
        "text": (
            f"Loaded {len(all_claims)} claims from {len(source_files)} docs. "
            f"Types: {', '.join(f'{k}={v}' for k, v in sorted(type_counts.items())[:5])}"
        ),
    }


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
    matrix = inputs.get("matrix") or []  # from CrossHypothesisMatrix
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
    """Test directly-testable positional claims against corpus sequences."""
    claims    = inputs.get("claims") or []
    sequences = inputs.get("sequences") or []

    if not sequences:
        return {"error": "No sequences — connect BuiltinCorpus or CorpusReader.sequences to the 'sequences' port"}
    if not claims:
        return {"error": "No claims — connect IndusClaimsLoader.claims"}

    from collections import Counter  # noqa: PLC0415

    # Build positional profile from sequences
    tc  = Counter(s for seq in sequences for s in seq)
    ic  = Counter(seq[0]  for seq in sequences if len(seq) > 1)
    te  = Counter(seq[-1] for seq in sequences if len(seq) > 1)
    total = len(sequences)

    results: list[dict] = []
    for claim in claims:
        ct = claim.get("claim_type", "")
        if "position" not in ct and "sign_value" not in ct and "sign_function" not in ct:
            continue
        signs   = claim.get("signs_involved") or []
        nc      = claim.get("normalized_claim", "")
        pred_pos = (
            "initial"  if "initial" in nc.lower() else
            "terminal" if "terminal" in nc.lower() else
            None
        )
        if not signs or not pred_pos:
            continue

        for sign in signs[:4]:
            n       = tc.get(sign, 0)
            if n == 0:
                continue
            obs_rate = (ic[sign] if pred_pos == "initial" else te[sign]) / n
            avg_rate = (
                sum(ic[s] / max(tc[s], 1) for s in tc if tc[s] >= 3) / max(len([s for s in tc if tc[s] >= 3]), 1)
                if pred_pos == "initial" else
                sum(te[s] / max(tc[s], 1) for s in tc if tc[s] >= 3) / max(len([s for s in tc if tc[s] >= 3]), 1)
            )
            supported = obs_rate >= avg_rate * 1.2
            results.append({
                "claim_id":         claim.get("claim_id", ""),
                "sign":             sign,
                "predicted_pos":    pred_pos,
                "observed_rate":    round(obs_rate, 4),
                "corpus_avg_rate":  round(avg_rate, 4),
                "lift":             round(obs_rate / max(avg_rate, 0.001), 3),
                "n_occurrences":    n,
                "test_verdict":     "supported" if supported else "not_supported",
                "source_claim":     nc[:100],
            })

    n_supp  = sum(1 for r in results if r["test_verdict"] == "supported")
    n_total = len(results)
    return {
        "test_results": results,
        "n_tested":     n_total,
        "n_supported":  n_supp,
        "support_rate": round(n_supp / max(n_total, 1), 4),
        "json": {"test_results": results},
        "number": round(n_supp / max(n_total, 1), 4),
        "text":  f"Tested {n_total} sign-position claims: {n_supp}/{n_total} supported ({round(100*n_supp/max(n_total,1))}%).",
    }


def _null_model_test(inputs: dict, params: dict) -> dict:
    """Run positional null model for sign-position or formula hypotheses.

    Tests whether the observed initial/terminal rate for a sign is explained
    by random shuffling alone (shuffle null) or frequency alone (freq null).
    """
    import math    # noqa: PLC0415
    import random  # noqa: PLC0415
    from collections import Counter  # noqa: PLC0415

    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"error": "No sequences — connect BuiltinCorpus or CorpusReader.sequences"}

    target_sign  = str(params.get("target_sign", "") or "").strip()
    n_null       = int(params.get("n_null_runs", 1000) or 1000)
    test_type    = str(params.get("test_type", "initial") or "initial").lower()  # "initial" | "terminal"
    random.seed(int(params.get("random_seed", 42) or 42))

    if not target_sign:
        return {"error": "Set target_sign parameter to the sign to test (e.g. 'M77/72')"}

    flat = [s for seq in sequences for s in seq]
    tc   = Counter(flat)
    n    = tc.get(target_sign, 0)
    if n == 0:
        return {"error": f"Sign '{target_sign}' not found in corpus"}

    def _obs_rate(seqs: list) -> float:
        if test_type == "initial":
            return sum(1 for seq in seqs if seq and seq[0] == target_sign) / max(len(seqs), 1)
        return sum(1 for seq in seqs if seq and seq[-1] == target_sign) / max(len(seqs), 1)

    observed = _obs_rate(sequences)

    # Shuffle null: randomly permute each inscription
    null_rates_shuffle: list[float] = []
    for _ in range(n_null):
        shuffled = [random.sample(seq, len(seq)) for seq in sequences]  # noqa: S311
        null_rates_shuffle.append(_obs_rate(shuffled))

    null_mean = sum(null_rates_shuffle) / len(null_rates_shuffle)
    null_std  = math.sqrt(sum((r - null_mean) ** 2 for r in null_rates_shuffle) / max(len(null_rates_shuffle), 1))
    z_score   = (observed - null_mean) / max(null_std, 1e-9)
    p_approx  = max(sum(1 for r in null_rates_shuffle if r >= observed) / n_null, 1 / n_null)

    verdict = (
        "STRONGLY_SIGNIFICANT"   if abs(z_score) >= 3 else
        "SIGNIFICANT"            if abs(z_score) >= 2 else
        "BORDERLINE"             if abs(z_score) >= 1.5 else
        "NOT_SIGNIFICANT"
    )

    return {
        "sign":          target_sign,
        "test_type":     test_type,
        "observed_rate": round(observed, 5),
        "null_mean":     round(null_mean, 5),
        "null_std":      round(null_std, 6),
        "z_score":       round(z_score, 3),
        "p_approx":      round(p_approx, 4),
        "n_null_runs":   n_null,
        "verdict":       verdict,
        "number":        round(z_score, 3),
        "json":          {"sign": target_sign, "z_score": z_score, "verdict": verdict},
        "text":          f"Null model ({test_type}): {target_sign} z={z_score:.2f} p≈{p_approx:.3f} → {verdict}.",
    }


def _intake_runner(inputs: dict, params: dict) -> dict:
    """Trigger the glossa-indus intake + claims extraction pipeline."""
    import subprocess  # noqa: PLC0415
    import sys          # noqa: PLC0415

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
