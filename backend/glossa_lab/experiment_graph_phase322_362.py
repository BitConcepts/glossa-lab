"""Experiment Graph atomic nodes for Phases 322–362.

Registers all experiments from the May 2026 decipherment advancement session:
  Phase 322: Mega mine 5000 (12 clusters, 6 APIs)
  Phase 323: Seal formula coherence (64%)
  Phase 324-325: First-char cross-entropy/prediction (flawed → superseded)
  Phase 326: Strict PD grammar (z=0.9, not significant)
  Phase 327: Label propagation community detection (collapsed)
  Phase 328: Missing phoneme resolution (0 truly missing)
  Phase 329: Inscription translation (19% coherence)
  Phase 330: Initial convergence (Level 1)
  Phase 331-335: Fixed experiments (full-reading level)
  Phase 336: PDr morpheme LM (z=14.0, circular note)
  Phase 337: Missing phoneme resolution (Krishnamurti analysis)
  Phase 338: Shu-ilishu quasi-bilingual (4/4 slots)
  Phase 339: Tight grammar (z=-2.3, fails)
  Phase 340: Anti-circularity suite (z=2.8 prior-only)
  Phase 341: Falsification re-run (F7=97%)
  Phase 342: Mine round 2
  Phase 343: Word-boundary detection (44% STEM→SUFFIX, STRONG)
  Phase 344-345: Motif validation (fixed) + convergence
  Phase 346: Motif-conditioned validation (z=17.9)
  Phase 347: Morpheme ordering (z=11.1)
  Phase 348-350: M77 replication + Sangam CE
  Phase 351: Advancement mine
  Phase 352-357: LOW upgrade, allograph, metrological, fish sign, translation, Mukhopadhyay
  Phase 358-362: Allograph consolidation (400→363), 66% coherent translations
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from glossa_lab.experiment_graph import AtomicNodeDef

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend" / "scripts"
_OUTPUTS = _REPO / "outputs"


def _load_output(json_name: str) -> dict[str, Any]:
    path = _OUTPUTS / json_name
    if not path.exists():
        return {"available": False, "error": f"Output not found: {json_name}"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _run_phase_script(script_name: str, timeout: int = 900) -> dict[str, Any]:
    script = _SCRIPTS / script_name
    if not script.exists():
        return {"error": f"Script not found: {script_name}"}
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=timeout, cwd=str(_REPO),
        )
        if result.returncode != 0:
            return {"error": f"Exit {result.returncode}", "stderr": result.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout after {timeout}s"}
    except Exception as exc:
        return {"error": str(exc)}
    return {"status": "ok", "stdout_tail": result.stdout[-500:]}


# ── Node implementations ────────────────────────────────────────────────────

def _phase322_mega_mine(inputs: dict, params: dict) -> dict[str, Any]:
    """Phase 322: Mega targeted mine 5000+ across 12 clusters."""
    data = _load_output("phase322_mega_mine_5000.json")
    return {
        "total_papers": data.get("total_unique", 0),
        "json": data,
        "number": float(data.get("total_unique", 0)),
        "text": data.get("verdict", "Phase 322 not run"),
    }

def _phase323_330_experiments(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 323-330: Initial 8 experiments (seal coherence, prediction, CE, etc.)."""
    data = _load_output("phase323_330_experiments.json")
    p323 = data.get("phase323", {})
    return {
        "seal_coherence": p323.get("coherence_rate", 0),
        "json": data,
        "number": float(p323.get("coherence_rate", 0)),
        "text": p323.get("verdict", "Phase 323 not run"),
    }

def _phase331_335_fixed(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 331-335: Fixed experiments with full-reading analysis."""
    data = _load_output("phase331_335_fixed_experiments.json")
    p333 = data.get("phase333", {})
    return {
        "community_purity": p333.get("purity_rate", 0),
        "json": data,
        "number": float(p333.get("purity_rate", 0)),
        "text": p333.get("verdict", "Phase 333 not run"),
    }

def _phase336_339_unlock(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 336-339: PDr morpheme LM, phoneme resolution, Shu-ilishu, grammar."""
    data = _load_output("phase336_339_unlock_decipherment.json")
    p336 = data.get("phase336", {})
    p338 = data.get("phase338", {})
    return {
        "morpheme_lm_z": p336.get("z_score", 0),
        "shu_ilishu_slots": p338.get("slots_covered", "0/4"),
        "json": data,
        "number": float(p336.get("z_score", 0)),
        "text": f"Phase 336 z={p336.get('z_score',0)}, Phase 338 {p338.get('slots_covered','?')}",
    }

def _phase340_345_validate(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 340-345: Anti-circularity, falsification, mine, word boundary, motif."""
    data = _load_output("phase340_345_validate_mine_experiment.json")
    p340 = data.get("phase340", {})
    p343 = data.get("phase343", {})
    return {
        "anti_circularity_z": p340.get("test1_prior_only", {}).get("z_score", 0),
        "word_boundary_ss": p343.get("stem_suffix_rate", 0),
        "json": data,
        "number": float(p340.get("test1_prior_only", {}).get("z_score", 0)),
        "text": data.get("phase345", {}).get("verdict", "Phase 345 not run"),
    }

def _phase346_348_level3(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 346-348: Motif validation (z=17.9), morpheme LM (z=11.1), M77."""
    data = _load_output("phase346_348_level3_push.json")
    p346 = data.get("phase346", {})
    p347 = data.get("phase347", {})
    return {
        "motif_z": p346.get("z_score", 0),
        "morpheme_z": p347.get("z_score", 0),
        "json": data,
        "number": float(p346.get("z_score", 0)),
        "text": p346.get("verdict", "Phase 346 not run"),
    }

def _phase352_357_advancement(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 352-357: LOW upgrade, allograph, metrological, fish, translation, Mukhopadhyay."""
    data = _load_output("phase352_357_advancement_experiments.json")
    p353 = data.get("phase353", {})
    p356 = data.get("phase356", {})
    return {
        "allograph_pairs": p353.get("total_allograph_pairs", 0),
        "translation_coherence": p356.get("average_coherence", 0),
        "json": data,
        "number": float(p356.get("average_coherence", 0)),
        "text": p356.get("verdict", "Phase 356 not run"),
    }

def _phase358_362_consolidate(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 358-362: Allograph consolidation, Mukhopadhyay cross-check, re-translation."""
    data = _load_output("phase358_362_consolidate_advance.json")
    p358 = data.get("phase358", {})
    p360 = data.get("phase360", {})
    return {
        "signs_merged": p358.get("signs_merged", 0),
        "canonical_signs": p358.get("unique_canonical_signs", 0),
        "consolidated_coherence": p360.get("average_coherence", 0),
        "json": data,
        "number": float(p360.get("average_coherence", 0)),
        "text": p360.get("verdict", "Phase 360 not run"),
    }

def _auto_decipher_loop(inputs: dict, params: dict) -> dict[str, Any]:
    """Auto-decipher loop: autonomous research protocol results."""
    data = _load_output("auto_decipher_loop.json")
    fc = data.get("final_convergence", {})
    return {
        "claim_level": fc.get("claim_level", 0),
        "n_strong": fc.get("n_strong", 0),
        "total_strength": fc.get("total_strength", 0),
        "json": data,
        "number": float(fc.get("claim_level", 0)),
        "text": f"Claim Level {fc.get('claim_level',0)}, {fc.get('n_strong',0)} strong, {fc.get('total_strength',0)}/18",
    }

def _phase363_370_deep(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 363-370: Deep experiments — site-stratified, compounds, formulas, corpus stats."""
    data = _load_output("phase363_370_deep_experiments.json")
    p370 = data.get("phase370", {})
    p363 = data.get("phase363", {})
    p364 = data.get("phase364", {})
    return {
        "fully_decoded_pct": p370.get("fully_decoded_inscriptions", 0) / max(1, p370.get("total_inscriptions", 1)),
        "high_coverage": p370.get("high_token_coverage", 0),
        "n_compounds": p364.get("n_compounds", 0),
        "n_sites": p363.get("n_sites", 0),
        "json": data,
        "number": float(p370.get("high_token_coverage", 0)),
        "text": p370.get("verdict", "Phase 370 not run"),
    }

def _phase371_376_exploit(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 371-376: Exploit findings — compounds, blockers, titles, chi2, prediction, length."""
    data = _load_output("phase371_376_exploit_findings.json")
    p372 = data.get("phase372", {})
    p373 = data.get("phase373", {})
    p374 = data.get("phase374", {})
    p376 = data.get("phase376", {})
    return {
        "guild_titles": p373.get("unique_names", 0),
        "blocked_by_one": p372.get("blocked_by_one_sign", 0),
        "motif_chi2_sig": p374.get("n_significant", 0),
        "json": data,
        "number": float(p373.get("unique_names", 0)),
        "text": f"Guild titles: {p373.get('unique_names',0)}, Blockers: {p372.get('blocked_by_one_sign',0)} one-sign, Chi2: {p374.get('n_significant',0)}/36 sig",
    }

def _mining_discovery_loop(inputs: dict, params: dict) -> dict[str, Any]:
    """Mining discovery loop: 5 rounds of targeted literature mining."""
    data = _load_output("mining_discovery_loop.json")
    return {
        "total_insights": data.get("total_insights", 0),
        "total_papers": data.get("total_new_papers", 0),
        "json": data,
        "number": float(data.get("total_insights", 0)),
        "text": data.get("verdict", "Mining discovery loop not run"),
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def phase322_362_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",   "type": "json"},
        {"name": "number", "type": "number"},
        {"name": "text",   "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="indus_phase322_mega_mine",
            name="Phase 322: Mega Mine 5000",
            category="Indus Decipherment (Phase 322–362)",
            description="Mega targeted literature mine across 12 clusters, 6 APIs",
            inputs=[], outputs=[{"name": "total_papers", "type": "number"}, *_STD],
            params_schema={}, fn=_phase322_mega_mine,
        ),
        AtomicNodeDef(
            id="indus_phase323_330_experiments",
            name="Phases 323–330: Initial Experiments",
            category="Indus Decipherment (Phase 322–362)",
            description="Seal coherence (64%), prediction, cross-entropy, grammar, community, phonemes, translation, convergence",
            inputs=[], outputs=[{"name": "seal_coherence", "type": "number"}, *_STD],
            params_schema={}, fn=_phase323_330_experiments,
        ),
        AtomicNodeDef(
            id="indus_phase331_335_fixed",
            name="Phases 331–335: Fixed Experiments",
            category="Indus Decipherment (Phase 322–362)",
            description="Full-reading cross-entropy, prediction, k-means community (86%), broad translation (62%)",
            inputs=[], outputs=[{"name": "community_purity", "type": "number"}, *_STD],
            params_schema={}, fn=_phase331_335_fixed,
        ),
        AtomicNodeDef(
            id="indus_phase336_339_unlock",
            name="Phases 336–339: Unlock Decipherment",
            category="Indus Decipherment (Phase 322–362)",
            description="PDr morpheme LM (z=14.0), missing phonemes (0 truly missing), Shu-ilishu (4/4), tight grammar",
            inputs=[], outputs=[{"name": "morpheme_lm_z", "type": "number"}, *_STD],
            params_schema={}, fn=_phase336_339_unlock,
        ),
        AtomicNodeDef(
            id="indus_phase340_345_validate",
            name="Phases 340–345: Validate & Mine",
            category="Indus Decipherment (Phase 322–362)",
            description="Anti-circularity (z=2.8), falsification (F7=97%), word boundary (44% STEM→SUFFIX)",
            inputs=[], outputs=[{"name": "anti_circularity_z", "type": "number"}, *_STD],
            params_schema={}, fn=_phase340_345_validate,
        ),
        AtomicNodeDef(
            id="indus_phase346_348_level3",
            name="Phases 346–348: Level 3 Push",
            category="Indus Decipherment (Phase 322–362)",
            description="Motif validation (z=17.9), morpheme ordering (z=11.1), M77 replication",
            inputs=[], outputs=[{"name": "motif_z", "type": "number"}, *_STD],
            params_schema={}, fn=_phase346_348_level3,
        ),
        AtomicNodeDef(
            id="indus_phase352_357_advancement",
            name="Phases 352–357: Advancement",
            category="Indus Decipherment (Phase 322–362)",
            description="LOW upgrade, allograph (84 pairs), metrological, fish sign, translation (56%), Mukhopadhyay",
            inputs=[], outputs=[{"name": "translation_coherence", "type": "number"}, *_STD],
            params_schema={}, fn=_phase352_357_advancement,
        ),
        AtomicNodeDef(
            id="indus_phase358_362_consolidate",
            name="Phases 358–362: Consolidate",
            category="Indus Decipherment (Phase 322–362)",
            description="Allograph consolidation (400→363), re-translation (66%), Mukhopadhyay cross-check (2/3)",
            inputs=[], outputs=[{"name": "consolidated_coherence", "type": "number"}, *_STD],
            params_schema={}, fn=_phase358_362_consolidate,
        ),
        AtomicNodeDef(
            id="indus_auto_decipher_loop",
            name="Auto-Decipher Loop",
            category="Indus Decipherment (Phase 322–376)",
            description="Autonomous research protocol: ASSESS→MINE→ANALYZE→DESIGN→EXECUTE→UPDATE (18/18 strong)",
            inputs=[], outputs=[{"name": "claim_level", "type": "number"}, *_STD],
            params_schema={"iterations": {"type": "integer", "default": 5}},
            fn=_auto_decipher_loop,
        ),
        AtomicNodeDef(
            id="indus_phase363_370_deep",
            name="Phases 363–370: Deep Experiments",
            category="Indus Decipherment (Phase 322–376)",
            description="Site-stratified (48%), compounds (619), title formulas (13), motif profiles (9), entropy, Gulf (67%/64%), corpus stats (75% decoded, 93% coverage)",
            inputs=[], outputs=[{"name": "fully_decoded_pct", "type": "number"}, *_STD],
            params_schema={}, fn=_phase363_370_deep,
        ),
        AtomicNodeDef(
            id="indus_phase371_376_exploit",
            name="Phases 371–376: Exploit Findings",
            category="Indus Decipherment (Phase 322–376)",
            description="Compound semantics (619), decode blockers (348 one-sign), guild titles (65), motif chi² (36/36 sig), entropy prediction (214), length-coherence",
            inputs=[], outputs=[{"name": "guild_titles", "type": "number"}, *_STD],
            params_schema={}, fn=_phase371_376_exploit,
        ),
        AtomicNodeDef(
            id="indus_mining_discovery_loop",
            name="Mining Discovery Loop",
            category="Indus Decipherment (Phase 322–376)",
            description="5-round targeted mining: hapax signs, Dravidian compounds, guild parallels, seal function, syntax (1331 papers, 217 insights)",
            inputs=[], outputs=[{"name": "total_insights", "type": "number"}, *_STD],
            params_schema={}, fn=_mining_discovery_loop,
        ),
    ]
