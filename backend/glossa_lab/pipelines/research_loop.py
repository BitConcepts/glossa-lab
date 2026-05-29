"""Integrated Research Loop pipeline.

Exposes the Mine→Analyze→Register→Execute→Analyze cycle as a proper
pipeline class with API-friendly methods. Used by the research-loop
API router and can also be imported by the Experiment Builder.

Phase 6: Insight-driven experiment selection (May 2026).
Phase 7: Database persistence via glossa_lab.database (May 2026).
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator

logger = logging.getLogger(__name__)

_REPO = Path(__file__).resolve().parents[3]

# ── Gap topics (15 rotating) ────────────────────────────────────────

GAP_TOPICS = [
    {"name": "rare_sign_context", "queries": [
        "Indus script hapax context-based reading rare sign",
        "undeciphered script low frequency sign assignment method",
        "ancient writing rare glyph contextual reading inference"]},
    {"name": "compound_morphology", "queries": [
        "Dravidian compound noun head modifier agglutination",
        "Tamil compound word structure Tolkappiyam morpheme boundary",
        "Proto-Dravidian nominal compound semantic classification"]},
    {"name": "seal_owner_identity", "queries": [
        "Indus seal owner identity guild merchant professional",
        "ancient seal administrative personal name title function",
        "Harappan craft specialist seal inscription identity"]},
    {"name": "cross_script_transfer", "queries": [
        "Tamil Brahmi Indus script sign continuity comparison",
        "early Tamil writing aksara value Indus inheritance",
        "Brahmi adaptation pre-existing script South Asia"]},
    {"name": "trade_network_vocabulary", "queries": [
        "Indus trade network commodity vocabulary seal marking",
        "Harappan weight metrological seal inscription economic",
        "ancient Near East Indus trade term bilingual evidence"]},
    {"name": "inscription_formula_syntax", "queries": [
        "Indus inscription formula syntax tripartite structure",
        "seal text pattern computational n-gram Indus script",
        "ancient administrative inscription formula comparison"]},
    {"name": "iconographic_semantic", "queries": [
        "Indus seal animal motif meaning iconographic semantic",
        "unicorn bull elephant symbolism Indus Valley seal",
        "ancient seal iconography text relationship meaning"]},
    {"name": "phonological_reconstruction", "queries": [
        "Proto-Dravidian phonological reconstruction 2024 2025",
        "Krishnamurti Dravidian consonant vowel system reconstruction",
        "comparative Dravidian phonology DEDR evidence"]},
    {"name": "computational_upgrade", "queries": [
        "Bayesian sign reading upgrade undeciphered script 2025 2026",
        "neural network ancient script reading assignment confidence",
        "machine learning sign value prediction ancient writing"]},
    {"name": "archaeological_context", "queries": [
        "Indus seal find context archaeological site function",
        "Harappan seal impression workshop administrative building",
        "Indus seal distribution site type warehouse granary gate"]},
    {"name": "personal_name_structure", "queries": [
        "ancient Dravidian personal name structure compound title",
        "Tamil Brahmi hero stone personal name formula analysis",
        "Sangam Tamil name morphology patronymic title suffix"]},
    {"name": "numeral_metrological", "queries": [
        "Indus numeral system stroke sign counting interpretation",
        "Harappan weight standard metrological seal numeral",
        "ancient South Asian numerical notation system development"]},
    {"name": "substrate_loanword", "queries": [
        "Dravidian substrate loanword Rigvedic Sanskrit craft term",
        "pre-Aryan South Asian vocabulary evidence agricultural",
        "Indus civilization language contact substrate evidence"]},
    {"name": "gulf_foreign_attestation", "queries": [
        "Indus seal Failaka Bahrain Gulf attestation evidence",
        "Dilmun Meluhha trade seal foreign site comparison",
        "round stamp seal Persian Gulf Indus type analysis"]},
    {"name": "allograph_classification", "queries": [
        "Indus sign allograph variant identification method computational",
        "undeciphered script sign variant graphic classification",
        "ancient writing system sign merger simplification evidence"]},
]

EXPERIMENT_NAMES = [
    "site_specific_formula", "motif_title_correlation", "suffix_chain_depth",
    "reading_frequency_zipf", "compound_semantic_coherence", "blocker_sign_context",
    "inscription_uniqueness", "position_entropy_by_site", "title_root_suffix_trigram",
    "motif_reading_mutual_info", "decoded_text_repetition", "rare_sign_neighbor_profile",
    "compound_vs_formula", "suffix_after_animal", "cross_site_formula_overlap",
]

# ── Template → graph experiment mapping ────────────────────────────
# Maps each abstract template name to a real graph experiment ID or
# atomic node ID that can be executed via execute_graph() or .fn().
# If the target doesn't exist at runtime, _execute falls back to a
# lightweight built-in analysis.
TEMPLATE_TO_GRAPH: dict[str, str] = {
    "site_specific_formula":      "indus_structural_atlas",
    "motif_title_correlation":    "positional_profile_analysis",
    "suffix_chain_depth":         "bigram_analysis",
    "reading_frequency_zipf":     "indus_structural_atlas",
    "compound_semantic_coherence": "kl_comparison",
    "blocker_sign_context":       "bigram_analysis",
    "inscription_uniqueness":     "indus_structural_atlas",
    "position_entropy_by_site":   "positional_profile_analysis",
    "title_root_suffix_trigram":  "bigram_analysis",
    "motif_reading_mutual_info":  "kl_comparison",
    "decoded_text_repetition":    "bigram_analysis",
    "rare_sign_neighbor_profile": "positional_profile_analysis",
    "compound_vs_formula":        "kl_comparison",
    "suffix_after_animal":        "positional_profile_analysis",
    "cross_site_formula_overlap": "bigram_analysis",
}
# ── Insight keyword extraction ──────────────────────────────────────
# (keyword_in_title, insight_type) — checked in order, first match wins.
# Broad coverage across all Indus/Dravidian research domains.
_INSIGHT_KEYWORDS: list[tuple[str, str]] = [
    # reading / sign value
    ("sign value", "reading"), ("sign reading", "reading"),
    ("decipherment", "reading"), ("decipher", "reading"),
    ("phonetic", "reading"), ("phonemic", "reading"),
    ("syllabary", "reading"), ("syllabic", "reading"),
    ("logographic", "reading"), ("logosyllabic", "reading"),
    ("aksara", "reading"), ("akshara", "reading"),
    ("script reading", "reading"), ("sign identification", "reading"),
    ("undeciphered", "reading"),
    # guild / trade / economy
    ("guild", "guild"), ("merchant", "guild"), ("trader", "guild"),
    ("craft specialist", "guild"), ("artisan", "guild"),
    ("trade network", "guild"), ("exchange network", "guild"),
    ("commodity", "guild"), ("commercial", "guild"),
    ("economic", "guild"), ("metrolog", "guild"),
    ("weight system", "guild"), ("weight standard", "guild"),
    # compound / morphology
    ("compound", "compound"), ("agglutina", "compound"),
    ("morpheme", "morphology"), ("morpholog", "morphology"),
    ("suffix", "morphology"), ("prefix", "morphology"),
    ("inflection", "morphology"), ("declension", "morphology"),
    ("genitive", "morphology"), ("dative", "morphology"),
    ("case marker", "morphology"), ("case ending", "morphology"),
    # formula / syntax / structure
    ("formula", "formula"), ("syntax", "formula"),
    ("inscription pattern", "formula"), ("sign sequence", "formula"),
    ("bigram", "formula"), ("trigram", "formula"), ("n-gram", "formula"),
    ("word order", "formula"), ("tripartite", "formula"),
    ("positional", "formula"), ("structural pattern", "formula"),
    # function / iconography / context
    ("seal function", "function"), ("seal type", "function"),
    ("iconograph", "function"), ("motif", "function"),
    ("unicorn", "function"), ("animal symbol", "function"),
    ("seal impression", "function"), ("sealing", "function"),
    ("administrative", "function"), ("bureaucra", "function"),
    # Dravidian / linguistic
    ("dravidian", "reading"), ("proto-dravidian", "reading"),
    ("tamil", "reading"), ("tamil-brahmi", "reading"),
    ("sangam", "reading"), ("tolkappiyam", "reading"),
    ("dedr", "reading"), ("kannada", "reading"),
    ("telugu", "reading"), ("malayalam", "reading"),
    ("brahui", "reading"), ("kurux", "reading"),
    # archaeology / sites
    ("harappa", "function"), ("mohenjo", "function"),
    ("indus valley", "function"), ("indus civiliz", "function"),
    ("mature harappan", "function"), ("dholavira", "function"),
    ("rakhigarhi", "function"), ("lothal", "function"),
    ("kalibangan", "function"),
    # computational / statistical
    ("entropy", "formula"), ("zipf", "formula"),
    ("frequency", "formula"), ("statistic", "formula"),
    ("computational", "formula"), ("machine learning", "formula"),
    ("neural network", "formula"), ("bayesian", "formula"),
    ("cluster", "formula"), ("classif", "formula"),
    # epigraphy / writing systems
    ("epigraph", "reading"), ("inscription", "formula"),
    ("writing system", "reading"), ("script", "reading"),
    ("glyph", "reading"), ("sign list", "reading"),
    ("cuneiform", "reading"), ("hieroglyph", "reading"),
    ("linear a", "reading"), ("linear b", "reading"),
]

# ── Phase 6: Insight type → best experiment mapping ─────────────────
# Each insight type (extracted from paper titles during mining) maps to
# the experiments most likely to exploit that kind of evidence.
INSIGHT_TO_EXPERIMENTS: dict[str, list[str]] = {
    "reading":    ["reading_frequency_zipf", "rare_sign_neighbor_profile",
                   "blocker_sign_context", "decoded_text_repetition"],
    "guild":      ["motif_title_correlation", "title_root_suffix_trigram",
                   "site_specific_formula", "suffix_after_animal"],
    "compound":   ["compound_semantic_coherence", "compound_vs_formula",
                   "suffix_chain_depth", "title_root_suffix_trigram"],
    "formula":    ["site_specific_formula", "inscription_uniqueness",
                   "cross_site_formula_overlap", "compound_vs_formula"],
    "function":   ["motif_title_correlation", "motif_reading_mutual_info",
                   "position_entropy_by_site", "suffix_after_animal"],
    "morphology": ["suffix_chain_depth", "title_root_suffix_trigram",
                   "compound_semantic_coherence", "decoded_text_repetition"],
}


class ResearchLoop:
    """Stateful research loop that yields cycle results.

    Phase 7: When *db* is provided, ``all_seen`` and ``history`` are
    loaded from the database on construction and persisted after every
    cycle so state survives across server restarts.
    """

    def __init__(self, max_cycles: int = 15, *, db: Any | None = None):
        self.max_cycles = max_cycles
        self.all_seen: set[str] = set()
        self.history: list[dict[str, Any]] = []
        self.running = False
        self.should_stop = False
        self._db = db
        self._used_experiments: set[str] = set()  # Phase 6: track used this session

        # Phase 7: try to restore persisted state
        if db is not None:
            self._load_persisted_state()

    # ── Phase 7 helpers ─────────────────────────────────────────────

    def _load_persisted_state(self) -> None:
        """Load all_seen + history from DB (sync wrapper)."""
        if self._db is None:
            return
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're inside an async context — schedule as a task
                # (called from __init__ before run(), so this is fine)
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    state = pool.submit(self._load_sync).result(timeout=5)
            else:
                state = loop.run_until_complete(self._db.load_research_loop_state())
        except Exception:
            state = None

        if state:
            self.all_seen = set(state.get("all_seen") or [])
            self.history = list(state.get("history") or [])
            self._used_experiments = {
                h["experiment"] for h in self.history if h.get("experiment")
            }
            logger.info(
                "Restored research loop state: %d seen papers, %d history entries",
                len(self.all_seen), len(self.history),
            )

    def _load_sync(self) -> dict | None:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self._db.load_research_loop_state())
        finally:
            loop.close()

    def _persist_state(self) -> None:
        """Save all_seen + history to DB (sync wrapper, best-effort)."""
        if self._db is None:
            return
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    pool.submit(self._save_sync).result(timeout=5)
            else:
                loop.run_until_complete(self._db.save_research_loop_state(
                    all_seen=list(self.all_seen),
                    history=self.history,
                ))
        except Exception as exc:
            logger.warning("Failed to persist research loop state: %s", exc)

    def _save_sync(self) -> None:
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self._db.save_research_loop_state(
                all_seen=list(self.all_seen),
                history=self.history,
            ))
        finally:
            loop.close()

    # ── Phase 6: insight-driven experiment selection ─────────────────

    def _select_experiment(self, insights: list[dict], cycle: int) -> str:
        """Pick the best experiment based on mined insights.

        Strategy:
        1. Tally insight types from this cycle's mining results.
        2. For the most common insight type, pick the highest-priority
           experiment from INSIGHT_TO_EXPERIMENTS that hasn't been used
           recently (within the last ``len(EXPERIMENT_NAMES)`` cycles).
        3. Fall back to round-robin rotation if no insights or all
           candidates are exhausted.
        """
        # Build insight type histogram
        type_counts: Counter[str] = Counter(i.get("type", "") for i in insights)

        # Recently-used set (last N cycles)
        recent_window = max(5, len(EXPERIMENT_NAMES))
        recent_exps = {
            h["experiment"] for h in self.history[-recent_window:]
            if h.get("experiment")
        }

        # Try each insight type in descending frequency
        for itype, _count in type_counts.most_common():
            candidates = INSIGHT_TO_EXPERIMENTS.get(itype, [])
            for exp in candidates:
                if exp not in recent_exps:
                    return exp

        # Fallback: round-robin, skipping recent
        idx = (len(self.history) + cycle - 1) % len(EXPERIMENT_NAMES)
        for offset in range(len(EXPERIMENT_NAMES)):
            candidate = EXPERIMENT_NAMES[(idx + offset) % len(EXPERIMENT_NAMES)]
            if candidate not in recent_exps:
                return candidate

        # All exhausted — just rotate
        return EXPERIMENT_NAMES[cycle % len(EXPERIMENT_NAMES)]

    def stop(self) -> None:
        self.should_stop = True

    def run(self) -> Generator[dict[str, Any], None, None]:
        """Yield one dict per completed cycle.

        Persistence is NOT done here — this generator runs in a worker
        thread (via asyncio.to_thread) and cannot safely access the
        async DB connection. The API layer persists after each cycle.
        """
        self.running = True
        self.should_stop = False

        for cycle in range(1, self.max_cycles + 1):
            if self.should_stop:
                break

            gap = GAP_TOPICS[(cycle - 1) % len(GAP_TOPICS)]

            # 1. MINE
            papers, insights = self._mine(gap)

            # 2. Phase 6: select experiment based on insights
            template = self._select_experiment(insights, cycle)

            # 3. REGISTER + EXECUTE
            verdict = self._execute(template)

            # 4. ANALYZE
            is_new = verdict != (self.history[-1]["verdict"] if self.history else "")

            entry = {
                "cycle": cycle,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "gap_targeted": gap["name"],
                "n_papers": len(papers),
                "n_insights": len(insights),
                "insight_types": dict(Counter(i.get("type", "") for i in insights)),
                "experiment": template,
                "selection_method": "insight" if insights else "rotation",
                "verdict": verdict,
                "is_new_info": is_new,
            }
            self.history.append(entry)
            yield entry

        self.running = False

    def get_status(self) -> dict[str, Any]:
        return {
            "running": self.running,
            "cycles_completed": len(self.history),
            "max_cycles": self.max_cycles,
            "total_papers": sum(h["n_papers"] for h in self.history),
            "total_insights": sum(h["n_insights"] for h in self.history),
            "history": self.history[-5:],  # Last 5 for brevity
        }

    def get_full_results(self) -> dict[str, Any]:
        return {
            "protocol": "integrated_research_loop",
            "cycles_run": len(self.history),
            "max_cycles": self.max_cycles,
            "total_papers_mined": sum(h["n_papers"] for h in self.history),
            "total_insights": sum(h["n_insights"] for h in self.history),
            "n_new_experiments": sum(1 for h in self.history if h["is_new_info"]),
            "history": self.history,
        }

    def _mine(self, gap: dict) -> tuple[list[dict], list[dict]]:
        bucket: list[dict] = []
        for q in gap["queries"]:
            enc = urllib.parse.quote(q)
            url = (f"https://api.openalex.org/works?search={enc}&per-page=50&cursor=*"
                   f"&select=id,title,doi,publication_year,abstract_inverted_index"
                   f"&mailto=tpierson@bitconcepts.tech")
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.8"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read().decode("utf-8", errors="replace"))
                for w in data.get("results", []):
                    title = w.get("title") or ""
                    if title:
                        bucket.append({"title": title})
            except Exception:
                pass
            time.sleep(0.4)

        unique = []
        for p in bucket:
            norm = re.sub(r"\s+", " ", p["title"].lower().strip())
            if norm and norm not in self.all_seen:
                self.all_seen.add(norm)
                unique.append(p)

        insights = []
        for p in unique:
            text = p["title"].lower()
            for kw, itype in _INSIGHT_KEYWORDS:
                if kw in text:
                    insights.append({"type": itype, "title": p["title"][:80]})
                    break

        return unique, insights

    def _execute(self, template: str) -> str:
        """Run a real graph experiment mapped from the template name.

        Strategy:
        1. Look up the template in TEMPLATE_TO_GRAPH.
        2. Try to run it via execute_graph() (the full graph engine).
        3. If the graph doesn't exist, try running the atomic node directly.
        4. Summarize key metrics from the result.
        """
        graph_id = TEMPLATE_TO_GRAPH.get(template)
        if not graph_id:
            return f"Template '{template}': no graph mapping."

        try:
            from glossa_lab.experiment_graph import (
                execute_graph,
                get_graph_experiment,
            )

            graph_def = get_graph_experiment(graph_id)
            if graph_def:
                result = execute_graph(graph_def)
                return self._summarize_result(template, graph_id, result)
        except Exception as exc:
            logger.warning("Graph execution failed for %s (%s): %s", template, graph_id, exc)

        # Fallback: try running as an atomic node directly
        try:
            from glossa_lab.experiment_graph import ATOMIC_NODES

            node = ATOMIC_NODES.get(graph_id)
            if node:
                result = node.fn({}, {})
                return self._summarize_result(template, graph_id, result)
        except Exception as exc:
            logger.warning("Atomic node execution failed for %s: %s", graph_id, exc)

        return f"Template '{template}' ({graph_id}): execution failed."

    @staticmethod
    def _summarize_result(template: str, graph_id: str, result: dict) -> str:
        """Extract a concise verdict string from experiment results."""
        if not result or "error" in result:
            return f"{template} ({graph_id}): {result.get('error', 'no output')}"

        # Extract key metrics from common output shapes
        parts = [f"{template} ({graph_id})"]

        for key in ["h1", "h1_normalized", "zipf_exponent", "mean_consistency",
                    "accuracy", "n_signs", "total_tokens", "distinct_symbols",
                    "tier_classification", "n_templates", "n_clusters",
                    "kl_divergence", "js_divergence"]:
            if key in result:
                val = result[key]
                if isinstance(val, float):
                    parts.append(f"{key}={val:.4f}")
                else:
                    parts.append(f"{key}={val}")

        if len(parts) == 1:
            # No recognized metrics — show top-level keys
            keys = [k for k in result if not k.startswith("_")][:5]
            parts.append(f"keys={keys}")

        return "; ".join(parts)
