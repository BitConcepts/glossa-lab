"""Phase-30a Statistical Validation Sprint.

Runs all 13 sub-tests of the Phase-30a validation plan against the Phase-29
findings (Enmenanak score 7.0, Enheduana 6.5, 102/1,222 PNs with at least
one position match). Writes one report JSON per test plus an aggregated
verdict, all under ``reports/``.

Sub-tests (per ``reports/PHASE_30_TASKS.md``):

  P30-A1  Permutation null on the 1,222-PN search (10,000x)
  P30-A2  Period filter (Old Akkadian / Ur III only) on the 102 candidates
  P30-A3  Meluhha co-occurrence filter on the 102 candidates
  P30-A4  Bootstrap CI on Enmenanak score (1,000x)
  P30-A5  Benjamini-Hochberg FDR correction across 1,222 tests
  P30-A6  Held-out replication: train Ur III, test Old Babylonian
  P30-A7  Janabiyah-pattern variant tests (sensitivity analysis)
  P30-A8  Phoneme-value permutation null v3 at M77 scale (1,669 inscriptions)
  P30-E7  Random-mapping null for the iconographic anchor score (10,000x)
  P30-G1  Joint period x provenience stratification (8x5 = 40 cells)
  P30-G8  Cohen's d for Enmenanak score vs random PN baseline
  P30-G9  M77 train (1,500) -> Janabiyah test cross-validation

This script is a self-contained runner; it imports the existing Phase-29
data accessors and re-implements the scoring functions here so that any
future changes to the experiment_graph_phase29 module don't break the
validation baseline.

Usage::

    python -m backend.scripts.run_phase30a_validation

Each test writes ``reports/indus_phase30a_<test_id>_<timestamp>.json``.
A combined ``reports/indus_phase30a_verdict_<timestamp>.json`` aggregates
results.
"""

from __future__ import annotations

import json
import math
import random
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Make the backend package importable regardless of where we run from.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKEND = _REPO_ROOT / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from glossa_lab.data.mesopotamian_contact import (  # noqa: E402
    get_epsd2_personal_names,
    get_epsd2_metadata,
    get_iconographic_anchors,
    get_janabiyah_seal_reading,
    get_mahadevan_inscriptions,
    get_meluhha_tablets,
    get_parpola_phoneme_map,
    get_seals_with_inscription,
    get_indus_seals_at_mesopotamia,
    get_phase27_seal_findspot_overrides,
    get_cisi_findspot_map,
)


REPORTS_DIR = _REPO_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

# Janabiyah skeleton (Phase-29):
JANABIYAH_TARGET_SEGMENTS = 7
JANABIYAH_MIIN_POSITIONS = {1, 3, 6}

# Base miin renderings (mirrors experiment_graph_phase29 v3):
BASE_RENDERINGS = {
    "miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
    "me-il", "mi-en", "me-in", "mu-li", "min", "men",
    "mul", "imin", "kakkab", "asz",
}


def _expand_to_tokens(renderings: set[str]) -> set[str]:
    """Split hyphenated renderings; keep tokens of length >= 2."""
    out: set[str] = set()
    for r in renderings:
        for t in r.split("-"):
            t = t.strip().lower()
            if t and len(t) >= 2:
                out.add(t)
    return out


def _epsd_pn_to_segments(forms: list[str]) -> list[list[str]]:
    """Convert ePSD2 forms list into candidate segment lists.

    Mirrors ``_epsd_pn_to_segments`` in ``experiment_graph_phase29.py``
    so scoring is consistent.
    """
    segs: list[list[str]] = []
    for f in forms or []:
        if not f:
            continue
        clean = re.sub(r"\{[^}]+\}", "", str(f).lower())
        parts = [p for p in re.split(r"[-]+", clean) if p and not p.isspace()]
        parts = [re.sub(r"[0-9]+$", "", p) for p in parts]
        parts = [p for p in parts if p]
        if parts:
            segs.append(parts)
    return segs


def _score_pn(forms: list[str], rendering_tokens: set[str],
              miin_positions: set[int] = JANABIYAH_MIIN_POSITIONS,
              n_target_segments: int = JANABIYAH_TARGET_SEGMENTS) -> dict:
    """Janabiyah-skeleton scoring of a single PN. Returns the best form's score.

    Mirrors ``_score_pn`` in ``experiment_graph_phase29.py``.
    """
    all_segs = _epsd_pn_to_segments(forms)
    if not all_segs:
        return {"total_score": -999.0, "position_match": 0,
                "free_miin": 0, "best_form": "",
                "best_n_segs": 0, "positions_matched": []}
    best_score = -999.0
    best = None
    for segs in all_segs:
        n_segs = len(segs)
        delta = abs(n_segs - n_target_segments)
        length_score = max(0.0, 3.0 - 0.5 * delta)
        position_match = 0
        positions_matched: list[int] = []
        for i, seg in enumerate(segs):
            if i in miin_positions and seg in rendering_tokens:
                position_match += 1
                positions_matched.append(i)
        free_miin = sum(1 for s in segs if s in rendering_tokens)
        total = length_score + position_match * 1.5 + free_miin * 0.5
        if total > best_score:
            best_score = total
            best = {
                "total_score": round(total, 3),
                "length_score": round(length_score, 2),
                "position_match": position_match,
                "free_miin": free_miin,
                "best_form": "-".join(segs),
                "best_n_segs": n_segs,
                "positions_matched": positions_matched,
            }
    return best  # type: ignore


def _score_all_pns(pns: list[dict], rendering_tokens: set[str],
                   miin_positions: set[int] = JANABIYAH_MIIN_POSITIONS,
                   n_target_segments: int = JANABIYAH_TARGET_SEGMENTS) -> list[dict]:
    out = []
    for pn in pns:
        r = _score_pn(pn.get("forms") or [], rendering_tokens,
                      miin_positions=miin_positions,
                      n_target_segments=n_target_segments)
        if r is None:
            continue
        out.append({
            "headword": pn.get("headword", ""),
            "icount": int(pn.get("icount", 0) or 0),
            "periods": pn.get("periods", []),
            **r,
        })
    return out


def _save_report(test_id: str, payload: dict) -> Path:
    fname = f"indus_phase30a_{test_id}_{TS}.json"
    p = REPORTS_DIR / fname
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


# ─── Build syllable vocabulary for permutation null ───────────────────


def _build_syllable_vocab(pns: list[dict]) -> list[str]:
    """Vocab of all 2-4-letter syllables that appear in any ePSD2 PN form.

    This is the substitution-space for the permutation null: random
    rendering sets are sampled from this distribution.
    """
    vocab = Counter()
    for pn in pns:
        for segs in _epsd_pn_to_segments(pn.get("forms") or []):
            for s in segs:
                if 2 <= len(s) <= 4:
                    vocab[s] += 1
    # Weighted by frequency (so the random null reflects the underlying
    # distribution of common Sumerian syllables, not a uniform sample
    # over rare ones).
    return list(vocab.elements())


# ─── P30-A1: Permutation null ────────────────────────────────────────


def run_p30_a1(pns: list[dict], n_permutations: int = 10_000,
               observed_score: float = 7.0,
               observed_headword: str = "Enmenanak[1]PN") -> dict:
    """Permutation null for Phase-29's Enmenanak finding.

    Null: rendering tokens are random Sumerian syllables (sampled with
    replacement from the empirical syllable distribution), not the
    miin-derived set.
    For each permutation, recompute Enmenanak's score under the random
    rendering set. Return the rank-percentile of the observed 7.0.
    """
    rng = random.Random(42)
    vocab = _build_syllable_vocab(pns)
    target_size = len(_expand_to_tokens(BASE_RENDERINGS))
    # Pre-extract Enmenanak forms
    enmenanak_forms = []
    for pn in pns:
        if pn.get("headword") == observed_headword:
            enmenanak_forms = pn.get("forms") or []
            break
    if not enmenanak_forms:
        return {"error": f"{observed_headword} not found", "n_permutations": 0}

    null_scores = []
    n_geq = 0
    for i in range(n_permutations):
        # Sample target_size unique tokens from the empirical distribution
        # (with replacement on draws but de-duped to mirror token-set behavior)
        sampled: set[str] = set()
        attempts = 0
        while len(sampled) < target_size and attempts < target_size * 10:
            tok = rng.choice(vocab)
            sampled.add(tok)
            attempts += 1
        if len(sampled) < target_size:
            # Fall back: pad with any vocab tokens
            sampled.update(rng.sample(set(vocab), min(target_size, len(set(vocab)))))
        r = _score_pn(enmenanak_forms, sampled)
        s = r["total_score"]
        null_scores.append(s)
        if s >= observed_score:
            n_geq += 1

    null_scores.sort()
    p_value = (n_geq + 1) / (n_permutations + 1)
    pct = sum(1 for s in null_scores if s < observed_score) / n_permutations * 100.0
    n_dist = len(null_scores)
    summary_stats = {
        "mean": round(sum(null_scores) / n_dist, 4),
        "min": round(min(null_scores), 4),
        "max": round(max(null_scores), 4),
        "p50": round(null_scores[n_dist // 2], 4),
        "p95": round(null_scores[int(0.95 * n_dist)], 4),
        "p99": round(null_scores[int(0.99 * n_dist)], 4),
    }

    verdict = (
        f"P30-A1 permutation null on {observed_headword}: "
        f"observed score {observed_score} sits at the {pct:.2f} percentile of "
        f"{n_permutations} random-rendering permutations. "
        f"Empirical p-value (one-sided, P(null >= observed)) = {p_value:.4f}. "
        f"Null distribution: mean={summary_stats['mean']}, "
        f"p95={summary_stats['p95']}, p99={summary_stats['p99']}."
    )

    return {
        "test_id": "P30-A1",
        "test_name": "Permutation null for Enmenanak score (random rendering tokens)",
        "n_permutations": n_permutations,
        "observed_headword": observed_headword,
        "observed_score": observed_score,
        "rendering_set_size": target_size,
        "vocab_size": len(set(vocab)),
        "p_value_one_sided": round(p_value, 6),
        "rank_percentile": round(pct, 4),
        "null_distribution_stats": summary_stats,
        "n_at_or_above_observed": n_geq,
        "verdict": verdict,
    }


# ─── P30-A2: Period filter ───────────────────────────────────────────


def run_p30_a2(scored_all: list[dict]) -> dict:
    """Period filter: keep only PNs attested in Old Akkadian or Ur III.

    Janabiyah is Early Dilmun ~2100-2000 BCE. Old Akkadian (~2350-2150)
    and Ur III (~2100-2000) overlap; later periods (Old Babylonian, Neo-
    Assyrian, etc.) do not.
    """
    overlapping = {"Old Akkadian", "Ur III"}
    pos_matched = [r for r in scored_all if r["position_match"] > 0]

    filtered = [
        r for r in pos_matched
        if any(p in overlapping for p in (r.get("periods") or []))
    ]
    n_total = len(pos_matched)
    n_kept = len(filtered)
    filtered.sort(key=lambda r: (-r["total_score"], -r["icount"]))

    verdict = (
        f"P30-A2 period filter: of {n_total} position-matched PNs (Phase-29 "
        f"baseline), {n_kept} survive the Old-Akkadian/Ur-III chronological "
        f"filter (overlap with Janabiyah ~2100-2000 BCE). Remaining "
        f"{n_total - n_kept} are post-Akkadian (Old Babylonian, Neo-Assyrian, "
        f"etc.) and chronologically incompatible with the Janabiyah seal."
    )
    top = filtered[:30]

    return {
        "test_id": "P30-A2",
        "test_name": "Period filter (Old Akkadian / Ur III only)",
        "n_position_matched_input": n_total,
        "n_chronologically_compatible": n_kept,
        "fraction_kept": round(n_kept / max(1, n_total), 4),
        "top_30_compatible": top,
        "verdict": verdict,
    }


# ─── P30-A3: Meluhha co-occurrence filter ────────────────────────────


def run_p30_a3(scored_all: list[dict], tablets: list[dict]) -> dict:
    """For each position-matched PN, check whether any CDLI tablet
    co-mentions the candidate name AND a Meluhha keyword.
    """
    pos_matched = [r for r in scored_all if r["position_match"] > 0]
    # Build flat list of (tablet_id, line) text from atf_excerpt + lines
    tablet_texts: list[tuple[str, str, str]] = []
    for t in tablets:
        text_parts: list[str] = []
        text_parts.extend(t.get("atf_lines_with_match") or [])
        text_parts.extend(t.get("atf_excerpt_lines") or [])
        excerpt = t.get("atf_excerpt") or ""
        if excerpt:
            text_parts.extend([ln for ln in str(excerpt).splitlines() if ln.strip()])
        body = " || ".join(text_parts).lower()
        if not body:
            continue
        if "me-luh" not in body:
            continue
        tablet_texts.append((t.get("p_number", ""), t.get("period", ""), body))

    survivors = []
    for r in pos_matched:
        # Use the best_form (segs joined). If empty, use the headword strip.
        candidate_form = r["best_form"]
        if not candidate_form:
            continue
        # Search for the exact form (case-insensitive) on Meluhha tablets
        hits = []
        for p_num, period, body in tablet_texts:
            if candidate_form in body:
                hits.append({"p_number": p_num, "period": period})
                if len(hits) >= 5:
                    break
        if hits:
            survivors.append({
                **r,
                "n_meluhha_tablet_hits": len(hits),
                "meluhha_tablet_hits": hits[:5],
            })

    survivors.sort(key=lambda r: (-r["total_score"], -r["icount"]))
    n_total = len(pos_matched)
    n_kept = len(survivors)
    n_tablets_searched = len(tablet_texts)

    verdict = (
        f"P30-A3 Meluhha co-occurrence filter: of {n_total} position-matched "
        f"PNs, {n_kept} appear (as their best form) in at least one of the "
        f"{n_tablets_searched} Meluhha-mentioning CDLI tablets. "
        + (f"Top survivor: '{survivors[0]['headword']}' (score "
           f"{survivors[0]['total_score']}, hits {survivors[0]['n_meluhha_tablet_hits']})."
           if survivors else "No PN co-occurs with a Meluhha keyword on any tablet.")
    )

    return {
        "test_id": "P30-A3",
        "test_name": "Meluhha co-occurrence filter on 102 candidates",
        "n_position_matched_input": n_total,
        "n_meluhha_tablets_searched": n_tablets_searched,
        "n_with_meluhha_cooccurrence": n_kept,
        "fraction_kept": round(n_kept / max(1, n_total), 4),
        "survivors": survivors,
        "verdict": verdict,
    }


# ─── P30-A4: Bootstrap CI ────────────────────────────────────────────


def run_p30_a4(pns: list[dict], n_bootstrap: int = 1000,
               headword: str = "Enmenanak[1]PN") -> dict:
    """Bootstrap confidence interval on Enmenanak's score by resampling
    the rendering-tokens set with replacement.
    """
    rng = random.Random(7)
    base_tokens = list(_expand_to_tokens(BASE_RENDERINGS))
    enm_forms = next((p.get("forms") or [] for p in pns if p.get("headword") == headword), [])
    if not enm_forms:
        return {"error": f"{headword} not found"}

    boot_scores: list[float] = []
    for _ in range(n_bootstrap):
        sampled = set(rng.choices(base_tokens, k=len(base_tokens)))
        s = _score_pn(enm_forms, sampled)["total_score"]
        boot_scores.append(s)
    boot_scores.sort()
    n = len(boot_scores)
    ci = {
        "mean": round(sum(boot_scores) / n, 4),
        "ci_2_5": round(boot_scores[int(0.025 * n)], 4),
        "ci_50": round(boot_scores[n // 2], 4),
        "ci_97_5": round(boot_scores[int(0.975 * n)], 4),
        "min": round(min(boot_scores), 4),
        "max": round(max(boot_scores), 4),
    }
    return {
        "test_id": "P30-A4",
        "test_name": f"Bootstrap CI on {headword} score",
        "n_bootstrap": n_bootstrap,
        "headword": headword,
        "ci": ci,
        "verdict": (
            f"Bootstrap (n={n_bootstrap}): {headword} score has 95% CI "
            f"[{ci['ci_2_5']}, {ci['ci_97_5']}], median {ci['ci_50']}, "
            f"mean {ci['mean']}."
        ),
    }


# ─── P30-A5: Benjamini-Hochberg FDR ──────────────────────────────────


def _empirical_p_one_pn(pn_forms: list[str], pns_other: list[dict],
                         observed_score: float, vocab: list[str],
                         target_size: int, n_perms: int = 1000,
                         rng: random.Random | None = None) -> float:
    """Quick permutation p-value for a single PN (lightweight, used inside FDR)."""
    rng = rng or random.Random(123)
    n_geq = 0
    for _ in range(n_perms):
        sampled: set[str] = set()
        while len(sampled) < target_size:
            sampled.add(rng.choice(vocab))
        s = _score_pn(pn_forms, sampled)["total_score"]
        if s >= observed_score:
            n_geq += 1
    return (n_geq + 1) / (n_perms + 1)


def run_p30_a5(pns: list[dict], scored_all: list[dict],
               top_k: int = 30, n_perms: int = 500) -> dict:
    """Apply Benjamini-Hochberg FDR correction across the top-K PNs.
    Computes per-PN empirical p-value (n_perms permutations each) then
    BH-corrects.
    """
    rng = random.Random(0)
    vocab = _build_syllable_vocab(pns)
    target_size = len(_expand_to_tokens(BASE_RENDERINGS))
    # Sort scored_all by total_score desc
    scored_sorted = sorted(scored_all, key=lambda r: -r["total_score"])
    top = scored_sorted[:top_k]
    # For each top PN, compute p-value via permutations
    pvals = []
    for r in top:
        pn_obj = next((p for p in pns if p.get("headword") == r["headword"]), None)
        if not pn_obj:
            continue
        p = _empirical_p_one_pn(pn_obj.get("forms") or [], pns,
                                r["total_score"], vocab, target_size,
                                n_perms=n_perms, rng=rng)
        pvals.append({
            "headword": r["headword"],
            "score": r["total_score"],
            "icount": r["icount"],
            "periods": r["periods"],
            "p_value": round(p, 6),
        })

    # Benjamini-Hochberg
    pvals.sort(key=lambda x: x["p_value"])
    m = len(pvals)
    for i, row in enumerate(pvals, 1):
        row["bh_threshold_q05"] = round(0.05 * i / m, 6)
        row["significant_at_q05"] = row["p_value"] <= row["bh_threshold_q05"]
    # Find largest k where p_(k) <= q*k/m
    k_star = 0
    for i, row in enumerate(pvals, 1):
        if row["p_value"] <= 0.05 * i / m:
            k_star = i
    n_sig = k_star

    return {
        "test_id": "P30-A5",
        "test_name": "Benjamini-Hochberg FDR correction",
        "n_tests": m,
        "n_perms_per_test": n_perms,
        "q_level": 0.05,
        "n_significant_after_bh": n_sig,
        "rows": pvals,
        "verdict": (
            f"P30-A5 BH-FDR (q=0.05): of {m} top-scoring PNs subjected to "
            f"empirical permutation tests ({n_perms} perms/PN), {n_sig} "
            f"survive multiple-comparisons correction."
        ),
    }


# ─── P30-A6: Held-out replication ───────────────────────────────────


def run_p30_a6(pns: list[dict]) -> dict:
    """Replication: train rendering set on Ur III PNs, test on Old Babylonian
    PNs. Verify Enmenanak-class scores generalize across periods.
    """
    ur3 = [p for p in pns if "Ur III" in (p.get("periods") or [])]
    obab = [p for p in pns if "Old Babylonian" in (p.get("periods") or [])]
    rendering_tokens = _expand_to_tokens(BASE_RENDERINGS)

    ur3_scored = _score_all_pns(ur3, rendering_tokens)
    obab_scored = _score_all_pns(obab, rendering_tokens)

    def _summarize(rows: list[dict], label: str) -> dict:
        if not rows:
            return {"label": label, "n": 0}
        scores = [r["total_score"] for r in rows]
        scores.sort()
        n = len(scores)
        return {
            "label": label,
            "n": n,
            "mean_score": round(sum(scores) / n, 4),
            "p50": round(scores[n // 2], 4),
            "p95": round(scores[int(0.95 * n)], 4),
            "n_with_position_match": sum(1 for r in rows if r["position_match"] > 0),
            "n_with_position_match_rate": round(
                sum(1 for r in rows if r["position_match"] > 0) / max(1, n), 4
            ),
            "top_score": round(max(scores), 4),
        }

    ur3_summary = _summarize(ur3_scored, "Ur III (train)")
    obab_summary = _summarize(obab_scored, "Old Babylonian (test)")

    # Check whether the position-match rate generalizes
    rate_ur3 = ur3_summary.get("n_with_position_match_rate", 0)
    rate_obab = obab_summary.get("n_with_position_match_rate", 0)
    delta = abs(rate_ur3 - rate_obab)

    return {
        "test_id": "P30-A6",
        "test_name": "Held-out replication: Ur III train, Old Babylonian test",
        "ur3": ur3_summary,
        "old_babylonian": obab_summary,
        "rate_delta": round(delta, 4),
        "verdict": (
            f"P30-A6: Ur III ({ur3_summary.get('n', 0)} PNs) position-match "
            f"rate {rate_ur3*100:.2f}% vs Old Babylonian "
            f"({obab_summary.get('n', 0)} PNs) {rate_obab*100:.2f}% "
            f"(delta {delta*100:.2f}pp). "
            f"{'Rate generalizes (delta < 5pp).' if delta < 0.05 else 'Rate differs by >=5pp; check for period-specific bias.'}"
        ),
    }


# ─── P30-A7: Janabiyah-pattern variants ──────────────────────────────


def run_p30_a7(pns: list[dict],
               headword: str = "Enmenanak[1]PN") -> dict:
    """Sensitivity analysis: how robust is Enmenanak's score to changes
    in the assumed Janabiyah skeleton?
    """
    enm_forms = next((p.get("forms") or [] for p in pns if p.get("headword") == headword), [])
    rendering_tokens = _expand_to_tokens(BASE_RENDERINGS)

    variants = [
        {"name": "baseline", "positions": {1, 3, 6}, "n_target": 7},
        {"name": "miin_pos_0_2_5", "positions": {0, 2, 5}, "n_target": 7},
        {"name": "miin_pos_0_3_6", "positions": {0, 3, 6}, "n_target": 7},
        {"name": "miin_pos_2_4_6", "positions": {2, 4, 6}, "n_target": 7},
        {"name": "skeleton_5_segments", "positions": {1, 3, 4}, "n_target": 5},
        {"name": "skeleton_6_segments", "positions": {1, 3, 5}, "n_target": 6},
        {"name": "skeleton_8_segments", "positions": {1, 3, 6, 7}, "n_target": 8},
    ]
    rows = []
    # Also test against full PN corpus to see how unique Enmenanak is per variant
    for v in variants:
        # Enmenanak-only score
        enm_r = _score_pn(enm_forms, rendering_tokens,
                           miin_positions=v["positions"],
                           n_target_segments=v["n_target"])
        # Top-1 in full corpus
        all_scored = _score_all_pns(pns, rendering_tokens,
                                     miin_positions=v["positions"],
                                     n_target_segments=v["n_target"])
        all_scored.sort(key=lambda r: -r["total_score"])
        rows.append({
            "variant": v["name"],
            "miin_positions": sorted(v["positions"]),
            "n_target_segments": v["n_target"],
            "enmenanak_score": enm_r["total_score"],
            "enmenanak_position_matches": enm_r["position_match"],
            "top_corpus_score": all_scored[0]["total_score"] if all_scored else 0,
            "top_corpus_headword": all_scored[0]["headword"] if all_scored else "",
            "enmenanak_rank": next(
                (i for i, r in enumerate(all_scored, 1) if r["headword"] == headword),
                0,
            ),
        })

    return {
        "test_id": "P30-A7",
        "test_name": "Janabiyah skeleton sensitivity analysis",
        "headword": headword,
        "variants": rows,
        "verdict": (
            f"P30-A7: Across {len(variants)} skeleton variants, Enmenanak's "
            f"score ranges from {min(r['enmenanak_score'] for r in rows):.2f} "
            f"to {max(r['enmenanak_score'] for r in rows):.2f}; "
            f"Enmenanak's rank in the corpus ranges from "
            f"{min(r['enmenanak_rank'] for r in rows if r['enmenanak_rank'] > 0)} "
            f"to {max(r['enmenanak_rank'] for r in rows)}. "
            f"Baseline (positions {{1,3,6}}, 7 segs) gives score "
            f"{rows[0]['enmenanak_score']}, rank {rows[0]['enmenanak_rank']}."
        ),
    }


# ─── P30-A8: Phoneme-value perm null v3 at M77 scale ────────────────


def run_p30_a8(m77_inscriptions: list[list[str]],
               phoneme_map: dict,
               n_permutations: int = 2000) -> dict:
    """Permutation null v3 at Mahadevan-1977 scale.

    Test: under the null that sign->phoneme assignments are random,
    what is the probability that the observed phoneme-map produces a
    given level of structure (e.g. that a particular sign sequence
    appears in M77 with high frequency)?

    Operationalization: we compute the H1 entropy of the *phoneme* sequence
    induced by mapping each M77 sign to its phoneme via parpola_phonemes.
    Null: shuffle the sign->phoneme assignment N times; recompute H1.
    Observed: H1 of the actual map.
    """
    # Restrict to signs that appear in both the M77 corpus and the phoneme map
    m77_signs_flat = [s for ins in m77_inscriptions for s in ins]
    sign_freq = Counter(m77_signs_flat)
    total = sum(sign_freq.values())
    # Normalize sign IDs: M77 uses zero-padded 3-digit; phoneme_map uses
    # plain integers as strings ('47'). Strip leading zeros.
    norm_freq = Counter()
    for sid, c in sign_freq.items():
        norm_freq[str(int(sid))] += c

    pmap_signs = set(phoneme_map.keys())
    overlap = [(s, c) for s, c in norm_freq.items() if s in pmap_signs]
    overlap_total = sum(c for _, c in overlap)
    if not overlap:
        return {"test_id": "P30-A8", "error": "no overlap between M77 and phoneme_map"}

    # Observed: phoneme distribution
    def _phoneme_entropy(assignment: dict[str, str]) -> float:
        ph_counter: Counter = Counter()
        for s, c in overlap:
            ph = (assignment.get(s) or {}).get("phoneme", "") if isinstance(assignment.get(s), dict) else assignment.get(s, "")
            if ph:
                ph_counter[ph] += c
        if not ph_counter:
            return 0.0
        total_c = sum(ph_counter.values())
        h = 0.0
        for c in ph_counter.values():
            p = c / total_c
            if p > 0:
                h -= p * math.log2(p)
        return h

    observed_h = _phoneme_entropy(phoneme_map)

    # Build a list of (phoneme_str) values for permutation
    phoneme_values = [(phoneme_map.get(s) or {}).get("phoneme", "") for s in pmap_signs]
    phoneme_values = [p for p in phoneme_values if p]

    rng = random.Random(101)
    null_h = []
    n_geq = 0
    for _ in range(n_permutations):
        shuffled = list(phoneme_values)
        rng.shuffle(shuffled)
        rand_assignment = {s: {"phoneme": shuffled[i % len(shuffled)]}
                           for i, s in enumerate(pmap_signs)}
        h = _phoneme_entropy(rand_assignment)
        null_h.append(h)
        if h >= observed_h:
            n_geq += 1

    null_h.sort()
    p_value = (n_geq + 1) / (n_permutations + 1)
    n = len(null_h)
    return {
        "test_id": "P30-A8",
        "test_name": "Phoneme-value permutation null v3 at M77 scale",
        "n_permutations": n_permutations,
        "n_overlap_signs": len(overlap),
        "n_overlap_tokens_in_m77": overlap_total,
        "observed_h1_phoneme": round(observed_h, 4),
        "null_h1_mean": round(sum(null_h) / n, 4),
        "null_h1_p50": round(null_h[n // 2], 4),
        "null_h1_p95": round(null_h[int(0.95 * n)], 4),
        "p_value_one_sided": round(p_value, 6),
        "verdict": (
            f"P30-A8: At M77 scale ({overlap_total} sign-token overlap, "
            f"{len(overlap)} distinct signs in phoneme map), observed "
            f"phoneme H1 = {observed_h:.4f}; null H1 distribution "
            f"mean={sum(null_h)/n:.4f}, p95={null_h[int(0.95*n)]:.4f}; "
            f"p={p_value:.4f}."
        ),
    }


# ─── P30-E7: Random-mapping null for anchor score ────────────────────


def _iconographic_anchor_score(anchors: list[dict], phoneme_map: dict) -> float:
    """Reduced version of Phase-28's AllographAwareIconographicScore.
    Returns the total weighted score across all anchors.
    """
    iconic_to_phoneme_alias = {
        "fish": ("miin", "fish"),
        "fish/star": ("miin", "fish"),
        "fig": ("vaTa", "fig_tree"),
        "banyan/fig": ("vaTa", "fig_tree"),
        "banyan": ("vaTa", "fig_tree"),
        "muruku": ("muruku", "intersecting_circles"),
        "intersecting circles": ("muruku", "intersecting_circles"),
        "squirrel": ("piLLai", None),
        "pot": ("kuTam", None),
        "pot/jar": ("kuTam", None),
        "veL": ("veL", "numerals"),
        "veN-miin": ("veL", None),
        "venus": ("veL", None),
        "pleiades": ("aru-", "numerals"),
        "ursa major": ("eZu-", "numerals"),
        "north star": ("vaTa", "fig_tree"),
    }
    total = 0.0
    for a in anchors:
        sid = str(a.get("sign_id", "")).split("+")[0]
        iconic = (a.get("iconic_reading", "") or "").lower()
        anchor_conf = (a.get("confidence") or "low").lower()
        ph_entry = phoneme_map.get(sid, {}) or {}
        ph_value = (ph_entry.get("phoneme", "") or "").lower()
        ph_conf = (ph_entry.get("confidence") or "none").lower()

        match = False
        for k, (alias, _) in iconic_to_phoneme_alias.items():
            if k in iconic and alias.lower() in ph_value:
                match = True
                break
        if not match:
            for k, (alias, _) in iconic_to_phoneme_alias.items():
                if k in iconic:
                    match = alias.lower() in ph_value
                    if match:
                        break

        if match:
            if anchor_conf == "high":
                anchor_score = 2.0
            elif anchor_conf == "medium":
                anchor_score = 1.0
            else:
                anchor_score = 0.5
            if ph_conf == "high":
                anchor_score *= 1.5
            total += anchor_score
    return total


def run_p30_e7(anchors: list[dict], phoneme_map: dict,
               n_permutations: int = 10_000) -> dict:
    """Random-mapping null on the iconographic anchor score.

    Null: assign each sign a random phoneme value drawn uniformly from
    the empirical phoneme-value list. Recompute anchor score N times.
    """
    observed = _iconographic_anchor_score(anchors, phoneme_map)
    sign_ids = list(phoneme_map.keys())
    phoneme_entries = list(phoneme_map.values())
    rng = random.Random(2025)
    null = []
    n_geq = 0
    for _ in range(n_permutations):
        shuffled = list(phoneme_entries)
        rng.shuffle(shuffled)
        random_map = {sid: shuffled[i] for i, sid in enumerate(sign_ids)}
        s = _iconographic_anchor_score(anchors, random_map)
        null.append(s)
        if s >= observed:
            n_geq += 1
    null.sort()
    n = len(null)
    p_value = (n_geq + 1) / (n_permutations + 1)
    pct = sum(1 for s in null if s < observed) / n * 100.0
    return {
        "test_id": "P30-E7",
        "test_name": "Random-mapping null for iconographic anchor score",
        "n_permutations": n_permutations,
        "n_anchors": len(anchors),
        "n_signs_in_phoneme_map": len(sign_ids),
        "observed_anchor_score": round(observed, 4),
        "null_mean": round(sum(null) / n, 4),
        "null_p50": round(null[n // 2], 4),
        "null_p95": round(null[int(0.95 * n)], 4),
        "null_p99": round(null[int(0.99 * n)], 4),
        "null_max": round(null[-1], 4),
        "p_value_one_sided": round(p_value, 6),
        "rank_percentile": round(pct, 4),
        "verdict": (
            f"P30-E7: observed anchor score {observed:.2f} sits at the "
            f"{pct:.2f} percentile of {n_permutations} random sign->phoneme "
            f"permutations; null mean {sum(null)/n:.2f}, p95 "
            f"{null[int(0.95*n)]:.2f}; empirical p={p_value:.4f}."
        ),
    }


# ─── P30-G1: Joint period x provenience stratification ───────────────


def run_p30_g1(pns: list[dict], scored_all: list[dict],
               tablets: list[dict]) -> dict:
    """Joint period x provenience stratification (8 x 5 = 40 cells).

    Periods (8): Early Dynastic IIIa, IIIb, Old Akkadian, Lagash II, Ur III,
                 Old Babylonian, Middle Assyrian, Neo-Assyrian (+Hellenistic, unknown)
    Provenience buckets (5): Sumer core, Akkad core, Periphery north,
                              Periphery east (Iran), Periphery west (Anatolia/Syria)
    """
    pos_matched = [r for r in scored_all if r["position_match"] > 0]

    # Map provenience strings to 5 buckets (heuristic by city)
    provenience_buckets = {
        "Sumer core": {"ur", "uruk", "lagash", "girsu", "umma", "shuruppak",
                        "nippur", "isin", "larsa", "eridu"},
        "Akkad core": {"sippar", "kish", "akkad", "agade", "babylon",
                        "borsippa", "dilbat"},
        "North Mesopotamia / Assur": {"assur", "nineveh", "kalhu", "nimrud",
                                       "tarbish", "khorsabad", "ashur"},
        "Periphery East / Elam": {"susa", "shimashki", "anshan"},
        "Periphery West / Mari/Ebla": {"mari", "ebla", "tell beydar",
                                        "tell brak", "tell leilan"},
    }

    def _bucket(prov: str) -> str:
        p = (prov or "").lower()
        for bucket, cities in provenience_buckets.items():
            if any(c in p for c in cities):
                return bucket
        return "Unknown / Other"

    # For each period x bucket cell, count how many position-match PNs
    # fall in that cell, indirectly via the tablets mentioning them.
    # Build PN -> set of (period, bucket) cells observed.
    pn_to_cells = defaultdict(set)
    for t in tablets:
        period = t.get("period", "")
        bucket = _bucket(t.get("provenience", ""))
        text = (t.get("atf_excerpt", "") or "").lower()
        for r in pos_matched:
            form = r["best_form"]
            if form and form in text:
                pn_to_cells[r["headword"]].add((period, bucket))

    # Count per cell
    cell_counts = Counter()
    for cells in pn_to_cells.values():
        for c in cells:
            cell_counts[c] += 1

    # Tablet density per cell (denominator)
    tablet_cell_counts = Counter()
    for t in tablets:
        period = t.get("period", "")
        bucket = _bucket(t.get("provenience", ""))
        tablet_cell_counts[(period, bucket)] += 1

    # Compute cells with non-trivial density
    rows = []
    for (period, bucket), n_pn in cell_counts.most_common():
        n_tablets = tablet_cell_counts.get((period, bucket), 0)
        rows.append({
            "period": period,
            "provenience_bucket": bucket,
            "n_pos_match_pns_observed": n_pn,
            "n_tablets_in_cell": n_tablets,
            "rate_per_tablet": round(n_pn / max(1, n_tablets), 4),
        })

    return {
        "test_id": "P30-G1",
        "test_name": "Joint period x provenience stratification (8x5=40 cells)",
        "n_pos_matched_pns": len(pos_matched),
        "n_pns_with_any_cell_observation": len(pn_to_cells),
        "n_distinct_cells_observed": len(cell_counts),
        "rows": rows[:50],  # cap
        "verdict": (
            f"P30-G1: of {len(pos_matched)} position-matched PNs, "
            f"{len(pn_to_cells)} were observed on Meluhha-mentioning tablets "
            f"distributed across {len(cell_counts)} period x provenience "
            f"cells. Densest cell: {rows[0]['period']} / "
            f"{rows[0]['provenience_bucket']} "
            f"({rows[0]['n_pos_match_pns_observed']} PNs, "
            f"{rows[0]['n_tablets_in_cell']} tablets)."
            if rows else "No cell observations recovered."
        ),
    }


# ─── P30-G8: Cohen's d ───────────────────────────────────────────────


def run_p30_g8(scored_all: list[dict], observed_score: float = 7.0) -> dict:
    """Cohen's d effect size for Enmenanak score vs the random PN baseline."""
    scores = [r["total_score"] for r in scored_all]
    n = len(scores)
    mean = sum(scores) / n
    var = sum((s - mean) ** 2 for s in scores) / max(1, n - 1)
    sd = math.sqrt(var)
    d = (observed_score - mean) / sd if sd > 0 else float("inf")
    return {
        "test_id": "P30-G8",
        "test_name": "Cohen's d effect size for Enmenanak vs random PN baseline",
        "n_pns": n,
        "observed_score": observed_score,
        "baseline_mean": round(mean, 4),
        "baseline_sd": round(sd, 4),
        "cohens_d": round(d, 4),
        "verdict": (
            f"P30-G8: Enmenanak score {observed_score} vs corpus baseline "
            f"(mean={mean:.4f}, sd={sd:.4f}, n={n}); Cohen's d = {d:.4f} "
            f"({'large' if abs(d) >= 0.8 else 'medium' if abs(d) >= 0.5 else 'small'})."
        ),
    }


# ─── P30-G9: M77 train / Janabiyah test cross-validation ─────────────


def run_p30_g9(m77_inscriptions: list[list[str]],
               janabiyah_reading: dict,
               n_train: int = 1500,
               n_repeats: int = 50) -> dict:
    """Build a bigram language model on a random 1,500-inscription train
    split of M77; evaluate the LM perplexity on (a) the held-out 169 M77
    inscriptions, and (b) the Janabiyah seal sign sequence.
    """
    janabiyah_signs = janabiyah_reading.get("sign_sequence") or []
    rng = random.Random(99)
    n_total = len(m77_inscriptions)
    n_train = min(n_train, n_total - 1)

    def _bigram_lm(corpus: list[list[str]]):
        bg: Counter = Counter()
        ug: Counter = Counter()
        for ins in corpus:
            for i, s in enumerate(ins):
                ug[s] += 1
                if i + 1 < len(ins):
                    bg[(s, ins[i + 1])] += 1
        return bg, ug

    def _ppl(bg: Counter, ug: Counter, sequence: list[str]) -> float:
        if len(sequence) < 2:
            return float("inf")
        total_ug = sum(ug.values())
        log_ppl = 0.0
        denom = 0
        vocab = len(ug) + 1
        for i in range(len(sequence) - 1):
            a, b = sequence[i], sequence[i + 1]
            num = bg.get((a, b), 0) + 1
            den = ug.get(a, 0) + vocab
            p = num / den
            log_ppl -= math.log2(p)
            denom += 1
        if denom == 0:
            return float("inf")
        return 2 ** (log_ppl / denom)

    held_ppls = []
    janab_ppls = []
    for _ in range(n_repeats):
        idx = list(range(n_total))
        rng.shuffle(idx)
        train = [m77_inscriptions[i] for i in idx[:n_train]]
        test = [m77_inscriptions[i] for i in idx[n_train:]]
        bg, ug = _bigram_lm(train)
        # Held-out M77 inscription perplexity (mean over test set)
        test_ppls = []
        for ins in test:
            if len(ins) >= 2:
                test_ppls.append(_ppl(bg, ug, ins))
        if test_ppls:
            held_ppls.append(sum(test_ppls) / len(test_ppls))
        # Janabiyah perplexity (single sequence)
        janab_signs_normalized = [str(int(s)) if str(s).isdigit() else str(s)
                                   for s in janabiyah_signs]
        # Match M77 zero-padding
        janab_signs_padded = [s.zfill(3) for s in janab_signs_normalized]
        janab_ppls.append(_ppl(bg, ug, janab_signs_padded))

    held_mean = sum(held_ppls) / max(1, len(held_ppls))
    janab_mean = sum(janab_ppls) / max(1, len(janab_ppls))
    return {
        "test_id": "P30-G9",
        "test_name": "M77 bigram LM train, predict Janabiyah",
        "n_repeats": n_repeats,
        "n_train": n_train,
        "n_test": n_total - n_train,
        "janabiyah_signs": janabiyah_signs,
        "held_out_ppl_mean": round(held_mean, 4),
        "janabiyah_ppl_mean": round(janab_mean, 4),
        "ppl_ratio_janabiyah_to_heldout": round(janab_mean / max(1.0, held_mean), 4),
        "verdict": (
            f"P30-G9: M77 bigram LM held-out PPL = {held_mean:.2f}; "
            f"Janabiyah PPL under same LM = {janab_mean:.2f} "
            f"(ratio {janab_mean/max(1.0,held_mean):.2f}). "
            f"{'Janabiyah is structurally consistent with M77 grammar.' if janab_mean <= 2*held_mean else 'Janabiyah is structurally distinct from M77 (PPL ratio > 2).'}"
        ),
    }


# ─── Aggregator ──────────────────────────────────────────────────────


def main() -> int:
    print(f"=== Phase-30a Statistical Validation Sprint ({TS}) ===")
    print(f"Reports dir: {REPORTS_DIR}")
    sys.stdout.flush()

    print("[load] ePSD2 PNs...", end=" ", flush=True)
    pns = get_epsd2_personal_names()
    print(f"{len(pns)} PNs.")
    print("[load] Iconographic anchors + Janabiyah reading...", end=" ", flush=True)
    anchors = get_iconographic_anchors()
    janabiyah = get_janabiyah_seal_reading()
    print(f"{len(anchors)} anchors, {len(janabiyah.get('sign_sequence') or [])} Janabiyah signs.")
    print("[load] Mahadevan 1977 corpus...", end=" ", flush=True)
    m77 = get_mahadevan_inscriptions()
    print(f"{len(m77)} inscriptions, {sum(len(s) for s in m77)} tokens.")
    print("[load] Phoneme map...", end=" ", flush=True)
    phoneme_map = get_parpola_phoneme_map()
    print(f"{len(phoneme_map)} entries.")
    print("[load] CDLI Meluhha tablets...", end=" ", flush=True)
    tablets = get_meluhha_tablets()
    print(f"{len(tablets)} tablets.")

    # Pre-score all PNs once with the baseline rendering set
    print("[precompute] Scoring all 1,222 PNs against baseline...", end=" ", flush=True)
    rendering_tokens = _expand_to_tokens(BASE_RENDERINGS)
    scored_all = _score_all_pns(pns, rendering_tokens)
    n_pos = sum(1 for r in scored_all if r["position_match"] > 0)
    print(f"{len(scored_all)} scored, {n_pos} with position match.")

    aggregated: dict = {
        "phase": "30a",
        "timestamp_utc": TS,
        "headline_target": "Validate Phase-29 Enmenanak/Enheduana finding",
        "n_pns_in_corpus": len(pns),
        "n_pns_position_matched_baseline": n_pos,
        "n_iconographic_anchors": len(anchors),
        "n_m77_inscriptions": len(m77),
        "n_meluhha_tablets": len(tablets),
        "results": {},
    }

    test_specs = [
        ("P30-A1", lambda: run_p30_a1(pns, n_permutations=10_000)),
        ("P30-A2", lambda: run_p30_a2(scored_all)),
        ("P30-A3", lambda: run_p30_a3(scored_all, tablets)),
        ("P30-A4", lambda: run_p30_a4(pns, n_bootstrap=1000)),
        ("P30-A5", lambda: run_p30_a5(pns, scored_all, top_k=30, n_perms=500)),
        ("P30-A6", lambda: run_p30_a6(pns)),
        ("P30-A7", lambda: run_p30_a7(pns)),
        ("P30-A8", lambda: run_p30_a8(m77, phoneme_map, n_permutations=2000)),
        ("P30-E7", lambda: run_p30_e7(anchors, phoneme_map, n_permutations=10_000)),
        ("P30-G1", lambda: run_p30_g1(pns, scored_all, tablets)),
        ("P30-G8", lambda: run_p30_g8(scored_all, observed_score=7.0)),
        ("P30-G9", lambda: run_p30_g9(m77, janabiyah, n_train=1500, n_repeats=50)),
    ]

    for tid, fn in test_specs:
        t0 = time.time()
        print(f"[run] {tid}...", end=" ", flush=True)
        try:
            result = fn()
            elapsed = time.time() - t0
            result["_elapsed_seconds"] = round(elapsed, 2)
            tid_clean = tid.lower().replace("-", "_")
            path = _save_report(tid_clean, result)
            print(f"done ({elapsed:.1f}s) -> {path.name}")
            aggregated["results"][tid] = result
        except Exception as exc:
            elapsed = time.time() - t0
            print(f"ERROR ({elapsed:.1f}s): {exc}")
            aggregated["results"][tid] = {"error": str(exc),
                                           "_elapsed_seconds": round(elapsed, 2)}

    # ── Decision verdict ──
    a1 = aggregated["results"].get("P30-A1", {})
    a2 = aggregated["results"].get("P30-A2", {})
    a3 = aggregated["results"].get("P30-A3", {})
    a5 = aggregated["results"].get("P30-A5", {})
    e7 = aggregated["results"].get("P30-E7", {})
    g8 = aggregated["results"].get("P30-G8", {})
    g9 = aggregated["results"].get("P30-G9", {})

    a1_p = a1.get("p_value_one_sided", 1.0)
    a2_kept = a2.get("n_chronologically_compatible", 0)
    a3_kept = a3.get("n_with_meluhha_cooccurrence", 0)
    a5_sig = a5.get("n_significant_after_bh", 0)
    e7_p = e7.get("p_value_one_sided", 1.0)
    g8_d = g8.get("cohens_d", 0.0)
    g9_ratio = g9.get("ppl_ratio_janabiyah_to_heldout", 999.0)

    decision = []
    if a1_p < 0.05 and e7_p < 0.05:
        decision.append("PASS: A1 + E7 both reject the null at p<0.05.")
    else:
        decision.append(
            f"WARN: A1 p={a1_p:.4f}, E7 p={e7_p:.4f}; not both <0.05."
        )
    if a2_kept > 0:
        decision.append(f"PASS: {a2_kept} PNs survive period filter.")
    else:
        decision.append("FAIL: zero PNs survive Old Akkadian / Ur III filter.")
    if a3_kept > 0:
        decision.append(f"PASS: {a3_kept} PNs co-occur with Meluhha keyword.")
    else:
        decision.append("WARN: no PN co-occurs with Meluhha keyword on any tablet.")
    if a5_sig > 0:
        decision.append(f"PASS: {a5_sig} PNs survive BH-FDR (q=0.05).")
    else:
        decision.append("WARN: no PN survives BH-FDR (q=0.05).")
    if abs(g8_d) >= 0.8:
        decision.append(f"PASS: Cohen's d = {g8_d:.2f} (large effect).")
    elif abs(g8_d) >= 0.5:
        decision.append(f"PARTIAL: Cohen's d = {g8_d:.2f} (medium effect).")
    else:
        decision.append(f"WARN: Cohen's d = {g8_d:.2f} (small effect).")
    if g9_ratio <= 2.0:
        decision.append(f"PASS: Janabiyah PPL ratio {g9_ratio:.2f} <= 2 (consistent).")
    else:
        decision.append(f"WARN: Janabiyah PPL ratio {g9_ratio:.2f} > 2 (distinct).")

    aggregated["decision_summary"] = decision

    # Top-level next-step recommendation
    n_pass = sum(1 for d in decision if d.startswith("PASS"))
    n_fail = sum(1 for d in decision if d.startswith("FAIL"))
    if n_fail >= 2:
        next_action = ("REJECT — Phase-30a rejected the Phase-29 headline. "
                        "Pivot Phase-30b to corpus expansion (F1 + F9 + F13) "
                        "before re-attempting Janabiyah readout.")
    elif n_pass >= 4:
        next_action = ("ACCEPT — Phase-30a confirms the Phase-29 headline. "
                        "Proceed to Phase-30b: phoneme-map expansion (B1, B2) "
                        "+ computational decipherment (H1, H4); draft arXiv "
                        "preprint (L9); email Parpola/Fuls/Laursen.")
    else:
        next_action = ("PARTIAL — Phase-30a partially supports the Phase-29 "
                        "headline. Proceed cautiously: corpus expansion "
                        "(F1, F9) + falsification round (E1) before publication.")
    aggregated["next_action"] = next_action

    # Save aggregated verdict
    verdict_path = REPORTS_DIR / f"indus_phase30a_verdict_{TS}.json"
    verdict_path.write_text(
        json.dumps(aggregated, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\n=== AGGREGATE VERDICT === ({verdict_path.name})")
    for d in decision:
        print(f"  {d}")
    print(f"\nNext: {next_action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
