"""Closed-loop proposal engine — Propose → Build → Verify → Analyze.

Phase E: makes the research loop self-directing by replacing the old
pick_template + run_template pattern with a full pipeline:

  1. ProposalEngine.propose()  — rank experiment candidates for a gap
  2. build_experiment()        — instantiate a runnable experiment
  3. verify_before_run()       — pre-flight checks before execution
  4. analyze_result()          — post-run synthesis and trend analysis
"""
from __future__ import annotations

import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ExperimentProposal:
    experiment_id: str
    display_name: str
    rationale: str
    priority: float = 0.5
    estimated_value: float = 0.5
    novelty_score: float = 0.5


@dataclass
class ExperimentInstance:
    experiment_id: str
    display_name: str
    anchor_set_id: str | None
    corpus_ids: list[str]
    params: dict[str, Any] = field(default_factory=dict)
    proposal: ExperimentProposal | None = None


@dataclass
class VerificationResult:
    ok: bool
    issues: list[str] = field(default_factory=list)
    recommendation: str = "pass"  # pass | skip | abort


@dataclass
class AnalysisResult:
    summary: str
    metrics: dict[str, Any] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)
    suggested_next_steps: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Proposal engine
# ---------------------------------------------------------------------------

# Experiments most effective at reducing epistemic uncertainty —
# i.e. they target high-uncertainty signs or probe evidence diversity.
_EPISTEMIC_PRIORITY_EXPERIMENTS: frozenset[str] = frozenset({
    "blocker_sign_context",       # highest-uncertainty signs adjacent to HIGH anchors
    "rare_sign_neighbor_profile", # hapax-like signs with no assigned reading
    "reading_frequency_zipf",     # statistical consistency of assigned readings
    "decoded_text_repetition",    # text-type ratio reveals gaps in reading coverage
    "compound_semantic_coherence",# coherence loss flags implausible readings
})


class ProposalEngine:
    """Generate ranked experiment proposals for a given research gap.

    Epistemic principle: every proposal is scored by expected information gain
    — how much will this experiment reduce our uncertainty about sign readings?
    Experiments that target high-uncertainty signs (LOW confidence, blocker
    signs, hapax logograms) receive an epistemic bonus over experiments that
    would revisit already-confident territory.

    Rule-based scorer that prefers:
    - Registered experiment templates
    - Templates with high historical success rate
    - Experiments covering unseen gaps
    - Experiments with high epistemic value (uncertainty reduction)

    Anti-patterns rejected:
    - Same experiment twice in a row
    - Superseded / legacy experiments
    - contact-zone before having enough anchors (min 50)
    """

    # Experiments that are superseded or legacy — never propose
    LEGACY_EXPERIMENTS: set[str] = set()

    # Experiments requiring minimum anchor counts
    MIN_ANCHOR_REQUIREMENTS: dict[str, int] = {
        "contact_zone_analysis": 50,
        "anchor_convergence_benchmark": 30,
    }

    def __init__(
        self,
        experiment_names: list[str],
        template_to_graph: dict[str, str],
        insight_to_experiments: dict[str, list[str]],
    ) -> None:
        self.experiment_names = experiment_names
        self.template_to_graph = template_to_graph
        self.insight_to_experiments = insight_to_experiments
        self.seen_experiments: set[str] = set()
        self.cooldown_map: dict[str, int] = {}  # experiment_id → last-run cycle

    def propose(
        self,
        gap: str,
        history: list[dict[str, Any]],
        anchor_count: int,
        cycle: int = 0,
        insights: list[dict[str, Any]] | None = None,
        epistemic_entropy: float = 0.5,
    ) -> list[ExperimentProposal]:
        """Return 2-3 ranked proposals for what experiment to run next.

        Args:
            epistemic_entropy: 0–1 normalised uncertainty across current anchor set.
                Higher = more unknown signs; triggers stronger epistemic-priority boost.
                Computed by study_loop.capture_state() and passed through per cycle.
        """
        insights = insights or []

        # Gather recent experiment IDs
        recent_5 = {h["experiment"] for h in history[-5:] if h.get("experiment")}
        last_exp = history[-1]["experiment"] if history else ""

        # Count historical success rate per experiment
        success_rate: dict[str, float] = {}
        exp_counts: Counter[str] = Counter()
        for h in history:
            eid = h.get("experiment", "")
            if not eid:
                continue
            exp_counts[eid] += 1
            if h.get("is_new_info"):
                success_rate[eid] = success_rate.get(eid, 0) + 1
        for eid in success_rate:
            success_rate[eid] /= max(exp_counts[eid], 1)

        # Determine which insight types dominate
        type_counts: Counter[str] = Counter(
            i.get("type", "") for i in insights
        )

        # Build candidate pool
        candidates: list[ExperimentProposal] = []
        for exp_id in self.experiment_names:
            # ── Anti-pattern filters ──
            if exp_id in self.LEGACY_EXPERIMENTS:
                continue
            if exp_id == last_exp:  # never same as last
                continue
            if exp_id in self.seen_experiments:
                last_cycle = self.cooldown_map.get(exp_id, 0)
                if cycle - last_cycle < 5:  # cooldown: 5 cycles
                    continue
            min_anch = self.MIN_ANCHOR_REQUIREMENTS.get(exp_id, 0)
            if min_anch > 0 and anchor_count < min_anch:
                continue

            # ── Scoring ──
            priority = 0.5
            novelty = 1.0 if exp_id not in self.seen_experiments else 0.3
            estimated_value = 0.5

            # Boost if experiment matches insight-driven selection
            for itype, _ in type_counts.most_common():
                exps_for_type = self.insight_to_experiments.get(itype, [])
                if exp_id in exps_for_type:
                    rank_in_type = exps_for_type.index(exp_id)
                    priority += 0.3 - rank_in_type * 0.05
                    break

            # Boost for historical success
            sr = success_rate.get(exp_id, 0.5)
            priority += sr * 0.2

            # Penalise if recently run (but past cooldown)
            if exp_id in recent_5:
                priority -= 0.2

            # Has a graph backing → slightly more reliable
            if exp_id in self.template_to_graph:
                priority += 0.05

            # ── Epistemic boost ──────────────────────────────────────────
            # Experiments targeting high-uncertainty signs get a boost
            # proportional to current epistemic entropy (0–1).  When
            # entropy is high (many unknown signs), reducing uncertainty
            # matters most, so we boost the experiments best positioned
            # to identify readings for the hardest signs.
            if exp_id in _EPISTEMIC_PRIORITY_EXPERIMENTS:
                epistemic_boost = epistemic_entropy * 0.35
                priority += epistemic_boost

            estimated_value = round(priority * novelty, 3)

            rationale = self._build_rationale(
                exp_id, gap, novelty, sr, type_counts,
                epistemic_entropy=epistemic_entropy,
            )

            candidates.append(ExperimentProposal(
                experiment_id=exp_id,
                display_name=exp_id.replace("_", " ").title(),
                rationale=rationale,
                priority=round(priority, 3),
                estimated_value=estimated_value,
                novelty_score=round(novelty, 3),
            ))

        # Sort by priority descending, take top 3
        candidates.sort(key=lambda p: -p.priority)
        return candidates[:3]

    def record_run(self, experiment_id: str, cycle: int) -> None:
        """Record that an experiment was run at a given cycle."""
        self.seen_experiments.add(experiment_id)
        self.cooldown_map[experiment_id] = cycle

    def _build_rationale(
        self,
        exp_id: str,
        gap: str,
        novelty: float,
        success_rate: float,
        type_counts: Counter,
        epistemic_entropy: float = 0.5,
    ) -> str:
        parts: list[str] = []
        if novelty >= 1.0:
            parts.append("never run before")
        if success_rate > 0.6:
            parts.append(f"high historical success ({success_rate:.0%})")
        top_type = type_counts.most_common(1)
        if top_type:
            parts.append(f"aligns with dominant insight type '{top_type[0][0]}'")
        if exp_id in _EPISTEMIC_PRIORITY_EXPERIMENTS and epistemic_entropy > 0.4:
            parts.append(
                f"epistemic priority: targets high-uncertainty signs "
                f"(system entropy {epistemic_entropy:.0%})"
            )
        parts.append(f"targets gap '{gap}'")
        return f"{exp_id.replace('_', ' ')}: " + "; ".join(parts) + "."


# ---------------------------------------------------------------------------
# Build experiment from proposal
# ---------------------------------------------------------------------------

def build_experiment(
    proposal: ExperimentProposal,
    anchor_set_id: str | None,
    corpus_ids: list[str],
    *,
    template_to_graph: dict[str, str] | None = None,
) -> ExperimentInstance:
    """Load template, inject anchor set and corpus IDs, return runnable instance."""
    template_to_graph = template_to_graph or {}
    graph_id = template_to_graph.get(proposal.experiment_id, "")

    params: dict[str, Any] = {}
    if anchor_set_id:
        params["anchor_set_id"] = anchor_set_id
    if corpus_ids:
        params["corpus_ids"] = corpus_ids
    if graph_id:
        params["graph_id"] = graph_id

    return ExperimentInstance(
        experiment_id=proposal.experiment_id,
        display_name=proposal.display_name,
        anchor_set_id=anchor_set_id,
        corpus_ids=corpus_ids,
        params=params,
        proposal=proposal,
    )


# ---------------------------------------------------------------------------
# Pre-run verification
# ---------------------------------------------------------------------------

def verify_before_run(
    instance: ExperimentInstance,
    anchor_count: int,
    corpus_available: bool,
    corpus_seq_count: int = 0,
) -> VerificationResult:
    """Pre-flight checks before running an experiment.

    Returns:
        VerificationResult with ok, issues, and recommendation (pass|skip|abort).
    """
    issues: list[str] = []

    # Anchor checks
    min_anchors = ProposalEngine.MIN_ANCHOR_REQUIREMENTS.get(
        instance.experiment_id, 0
    )
    if min_anchors > 0 and anchor_count < min_anchors:
        issues.append(
            f"Experiment requires ≥{min_anchors} anchors, "
            f"only {anchor_count} available"
        )

    # Corpus availability
    if not corpus_available:
        issues.append("No corpus data available for this experiment")

    if corpus_seq_count < 10 and corpus_available:
        issues.append(f"Very small corpus ({corpus_seq_count} sequences)")

    # SA-style experiments need enough anchors
    if instance.experiment_id in (
        "anchor_convergence_benchmark",
        "constraint_sweep",
    ) and anchor_count < 30:
        issues.append(
            f"Anchored SA needs ≥30 anchors; only {anchor_count} available"
        )

    if not issues:
        return VerificationResult(ok=True, recommendation="pass")

    # Determine severity
    critical = any("No corpus" in i for i in issues)
    if critical:
        return VerificationResult(ok=False, issues=issues, recommendation="abort")

    return VerificationResult(ok=False, issues=issues, recommendation="skip")


# ---------------------------------------------------------------------------
# Post-run analysis
# ---------------------------------------------------------------------------

def analyze_result(
    result: dict[str, Any],
    proposal: ExperimentProposal,
    prior_results: list[dict[str, Any]],
    verdict: str = "",
) -> AnalysisResult:
    """Post-run synthesis: extract metrics, detect trends, flag changes.

    Extracts key metrics from the result (z-scores, consistency rates,
    entropy values), compares to prior runs, and flags significant changes.
    """
    metrics: dict[str, Any] = {}
    flags: list[str] = []
    next_steps: list[str] = []

    # Extract common metrics
    for key in (
        "zipf_alpha", "ttr", "mutual_info", "avg_jaccard", "avg_depth",
        "n_unique", "n_singletons", "n_blockers", "valid_pct",
        "n_rare", "avg_sigma", "n_trigrams", "n_sites", "n_motifs",
        "n_start", "n_mid", "n_shared",
    ):
        if key in result:
            metrics[key] = result[key]

    # Detect new anchor candidates from the result
    n_cands = result.get("n_candidates", 0)
    if isinstance(n_cands, int) and n_cands > 0:
        flags.append("new_anchor_candidate")
        metrics["n_candidates"] = n_cands

    # Detect whether the needle moved vs prior runs of same experiment
    same_type_priors = [
        p for p in prior_results
        if p.get("experiment") == proposal.experiment_id
    ]

    if same_type_priors and metrics:
        prev_metrics = same_type_priors[-1].get("analysis_metrics", {})
        # Snapshot keys to avoid 'dictionary changed size during iteration'
        # when we add _delta keys below
        deltas: dict[str, float] = {}
        for key, val in list(metrics.items()):
            if key in prev_metrics and isinstance(val, (int, float)):
                prev_val = prev_metrics[key]
                if isinstance(prev_val, (int, float)) and prev_val != 0:
                    pct_change = (val - prev_val) / abs(prev_val)
                    if pct_change > 0.1:
                        flags.append("needle_moved")
                        deltas[f"{key}_delta"] = round(pct_change, 3)
                    elif pct_change < -0.1:
                        flags.append("regression_detected")
                        deltas[f"{key}_delta"] = round(pct_change, 3)
        metrics.update(deltas)

    # Generate summary
    metric_strs = [f"{k}={v}" for k, v in list(metrics.items())[:5]
                   if not k.endswith("_delta")]
    summary_parts = [
        f"{proposal.display_name}: {verdict}" if verdict else proposal.display_name
    ]
    if metric_strs:
        summary_parts.append("; ".join(metric_strs))
    if "needle_moved" in flags:
        summary_parts.append("📈 Needle moved")
    if "regression_detected" in flags:
        summary_parts.append("📉 Regression detected")
    if "new_anchor_candidate" in flags:
        summary_parts.append(f"🎯 {n_cands} new candidate(s)")

    summary = " · ".join(summary_parts)

    # Suggest next steps
    if "needle_moved" in flags:
        next_steps.append(
            f"Run {proposal.experiment_id} again with more data to confirm trend"
        )
    if "new_anchor_candidate" in flags:
        next_steps.append("Review staged anchor candidates")
    if not flags:
        next_steps.append("Try a different experiment type to explore new angles")

    return AnalysisResult(
        summary=summary,
        metrics=metrics,
        flags=flags,
        suggested_next_steps=next_steps,
    )
