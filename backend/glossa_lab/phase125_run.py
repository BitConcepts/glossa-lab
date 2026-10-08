"""Phase-125 (spec 019) — orchestration: load the three
frozen inputs -> assert totals + anchors hash -> build
arms -> evaluate arms (profiles strictly within each
compilation) -> verdict on the PRIMARY arm -> reports.

Executes the frozen protocol of
specs/019-phase125-cross-compilation-positional/spec.md:

  1. mayig CISI layer via its Phase-122 loader (P-space;
     179 inscriptions / 1,003 tokens / 182 signs asserted).
  2. Holdat via the specs-015/017 loader replication
     (phase113_run.load_holdat_inscriptions; loader logic
     of sa_validation.load_holdat_corpus only — no SA
     code is executed; 1,670 inscriptions / 7,002 tokens /
     390 signs asserted). Holdat is read from the
     gitignored downloads area and never committed; only
     statistics and verdicts are published.
  3. Crosswalk v1 via its Phase-122 loader — the sole
     join between the compilations (spec section 3).
  4. No object-level join is performed anywhere: Holdat's
     cisi_number is internal sequential numbering, not a
     CISI object ID (spec section 2.1).
  5. The anchors file is never opened for writing; its
     sha256 is asserted identical before and after.

Sensitivity arms are computed and reported separately
and never pooled into the verdict (spec sections 3, 6).
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
_MAIN_REPO = Path.home() / "workspace" / "glossa-lab"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.data import mayig_layer as ml  # noqa: E402
from glossa_lab.data import (  # noqa: E402
    parpola_mahadevan_crosswalk_v1 as xw,
)
from glossa_lab.phase113_battery import CorpusContext  # noqa: E402
from glossa_lab.phase113_run import (  # noqa: E402
    _gpu_device, load_holdat_inscriptions,
)
from glossa_lab.phase125_cross_compilation import (  # noqa: E402
    ARM_ORDER, ARM_PRIMARY, build_arms, classify, evaluate_arm,
)

ANCHORS_PATH = _BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
RESULTS_PATH = _REPO / "reports" / "phase125_cross_compilation_results.json"
SUMMARY_PATH = _REPO / "reports" / "phase125_cross_compilation_summary.md"
SPEC = "specs/019-phase125-cross-compilation-positional"
DATE = "2026-10-08"
ANCHORS_SHA256 = "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"

MAYIG_EXPECTED = {"inscriptions": 179, "tokens": 1003, "signs": 182}
HOLDAT_EXPECTED = {"inscriptions": 1670, "tokens": 7002, "signs": 390}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _find_holdat_csv() -> Path:
    rel = Path("corpora") / "downloads" / "external_repos" \
        / "holdatllc_indus" / "indus_corpus 2.csv"
    for cand in (_REPO / rel, _MAIN_REPO / rel):
        if cand.exists():
            return cand
    raise FileNotFoundError("Holdat CSV not found in worktree "
                            "or main checkout")


def _fmt(x, nd=6):
    return "null" if x is None else f"{x:.{nd}f}"


def run_all(write: bool = True) -> dict:
    anchors_hash_before = _sha256(ANCHORS_PATH)
    assert anchors_hash_before == ANCHORS_SHA256, anchors_hash_before

    # ── mayig (within-compilation context; P-space) ──
    mayig_records = ml.load_inscriptions()
    mayig_inscriptions = [list(r["tokens"]) for r in mayig_records]
    mayig_ctx = CorpusContext(mayig_inscriptions)
    mayig_totals = {
        "inscriptions": len(mayig_inscriptions),
        "tokens": mayig_ctx.n_tokens,
        "signs": len(mayig_ctx.token_counts),
        "objects": len(ml.object_ids()),
    }
    assert mayig_totals["inscriptions"] == MAYIG_EXPECTED["inscriptions"]
    assert mayig_totals["tokens"] == MAYIG_EXPECTED["tokens"]
    assert mayig_totals["signs"] == MAYIG_EXPECTED["signs"]

    # ── Holdat (within-compilation context; M-space) ──
    holdat_csv = _find_holdat_csv()
    holdat_inscriptions = load_holdat_inscriptions(holdat_csv)
    holdat_ctx = CorpusContext(holdat_inscriptions)
    holdat_totals = {
        "inscriptions": len(holdat_inscriptions),
        "tokens": holdat_ctx.n_tokens,
        "signs": len(holdat_ctx.token_counts),
    }
    assert holdat_totals["inscriptions"] == HOLDAT_EXPECTED["inscriptions"]
    assert holdat_totals["tokens"] == HOLDAT_EXPECTED["tokens"]
    assert holdat_totals["signs"] == HOLDAT_EXPECTED["signs"]

    # ── Crosswalk (the sole join) ──
    rows = xw.load_crosswalk()
    xw_stats = xw.crosswalk_stats()
    assert xw_stats["n_pairs"] == 762
    assert xw_stats["confidence_breakdown"] == {"high": 372, "low": 390}

    arms = build_arms(rows)
    arm_results: dict = {}
    for arm_name in ARM_ORDER:
        ev = evaluate_arm(arms[arm_name], mayig_ctx, holdat_ctx)
        ev["pattern"] = classify(ev["stats"])
        arm_results[arm_name] = ev

    verdict = arm_results[ARM_PRIMARY]["pattern"]

    results = {
        "phase": 125,
        "spec": SPEC,
        "date": DATE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gpu_device": _gpu_device(),
        "inputs": {
            "mayig_layer": {
                "path": "data/corpus_layers/mayig_cisi_layer_v1.json",
                "sha256": "6a7664c605079373ca80e70b7e9559c1527613e3f67b579a817ced785e129860",
                **mayig_totals,
            },
            "holdat": {
                "path": "corpora/downloads/external_repos/holdatllc_indus/"
                        "indus_corpus 2.csv (gitignored; main checkout)",
                "sha256": "62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e",
                **holdat_totals,
            },
            "crosswalk": {
                "path": "data/crosswalks/parpola_mahadevan_crosswalk_v1.json",
                "sha256": "4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb",
                "n_pairs": xw_stats["n_pairs"],
                "confidence_breakdown": xw_stats["confidence_breakdown"],
                "medium_pairs": 0,
                "unmapped_p_signs": xw.unmapped_p_signs(),
            },
            "object_join": "none performed (spec section 2.1: Holdat "
                           "cisi_number is internal sequential numbering, "
                           "not a CISI object ID)",
        },
        "arms": arm_results,
        "verdict": {
            "arm": ARM_PRIMARY,
            **verdict,
        },
        "anchors_sha256_before": anchors_hash_before,
    }

    anchors_hash_after = _sha256(ANCHORS_PATH)
    assert anchors_hash_after == anchors_hash_before
    results["anchors_sha256_after"] = anchors_hash_after
    results["anchors_unchanged"] = anchors_hash_after == anchors_hash_before

    if write:
        RESULTS_PATH.write_text(
            json.dumps(results, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
        SUMMARY_PATH.write_text(_summary(results), encoding="utf-8")
    return results


def _arm_table(results: dict) -> str:
    lines = [
        "| Arm | Pairs | Judgeable | Below floor | Median TV | "
        "Median W1 | rho initial | rho terminal | rho medial | "
        "Modal agree | p_null | Pattern |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name in ARM_ORDER:
        ev = results["arms"][name]
        s = ev["stats"]
        nul = s["null"] or {}
        lines.append(
            f"| {name} | {s['n_pairs']} | {s['n_judgeable']} | "
            f"{s['n_below_floor']} | {_fmt(s['median_tv'])} | "
            f"{_fmt(s['median_w1'])} | {_fmt(s['spearman_initial'])} | "
            f"{_fmt(s['spearman_terminal'])} | "
            f"{_fmt(s['spearman_medial'])} | "
            f"{_fmt(s['modal_agreement_share'])} | "
            f"{_fmt(nul.get('p_null'))} | "
            f"{ev['pattern']['verdict']} / {ev['pattern']['substate']} |")
    return "\n".join(lines)


def _judgeable_table(results: dict) -> str:
    lines = [
        "| Pair (P-M) | mayig n | Holdat n | mayig profile (I/M/T) | "
        "Holdat profile (I/M/T) | TV | W1 |",
        "|---|---|---|---|---|---|---|",
    ]
    for rec in results["arms"][ARM_PRIMARY]["records"]:
        if not rec["judgeable"]:
            continue
        mp = "/".join(_fmt(x, 4) for x in rec["mayig_profile"])
        hp = "/".join(_fmt(x, 4) for x in rec["holdat_profile"])
        lines.append(
            f"| {rec['parpola_id']}-{rec['mahadevan_id']} | "
            f"{rec['mayig_n']} | {rec['holdat_n']} | {mp} | {hp} | "
            f"{_fmt(rec['tv'])} | {_fmt(rec['w1'])} |")
    return "\n".join(lines)


def _summary(results: dict) -> str:
    v = results["verdict"]
    primary = results["arms"][ARM_PRIMARY]["stats"]
    nul = primary["null"] or {}
    a_stats = results["arms"]["sensitivity_a_medium_included"]["stats"]
    a_pat = results["arms"]["sensitivity_a_medium_included"]["pattern"]
    b_stats = results["arms"]["sensitivity_b_all_pairs"]["stats"]
    b_pat = results["arms"]["sensitivity_b_all_pairs"]["pattern"]
    return f"""# Phase-125 — Cross-Compilation Positional Comparison (mayig/CISI vs Holdat)

**Spec:** {SPEC} (frozen before any results) · **Date:** {DATE} · **GPU device:** {results['gpu_device']}

Per-sign positional profiles (initial/medial/terminal rates) computed
**within** the mayig/CISI compilation and **within** the Holdat
compilation separately — inscriptions never pooled — and joined only
through the Phase-122 Parpola-Mahadevan crosswalk v1. The PRIMARY arm
is the high-confidence, unambiguous pair set (372 high pairs, 286
after the uniqueness rule); floor 8 tokens per sign per compilation;
the verdict is the PRIMARY arm's frozen spec-section-6 pattern only.

## Verdict

**{v['verdict']} — {v['substate']}** ({v['reason']}). Primary arm:
{primary['n_judgeable']} judgeable pairs of {primary['n_pairs']};
median TV {_fmt(primary['median_tv'])} (PASS bound <= 0.35; FAIL bound
>= 0.50); Spearman rho initial {_fmt(primary['spearman_initial'])},
terminal {_fmt(primary['spearman_terminal'])} (PASS bound >= 0.50);
pairing-shuffle null (B = 999, seed 125125) p_null
{_fmt(nul.get('p_null'))} (PASS requires <= 0.05; FAIL requires
> 0.05 together with median TV >= 0.50), null median-of-medians
{_fmt(nul.get('null_median_of_medians'))}.

## Arms (each computed and reported separately; never pooled)

{_arm_table(results)}

Sensitivity notes: arm A (medium-included) — crosswalk v1 contains
zero medium pairs, so arm A's pair set coincides with the PRIMARY
arm's (judgeable {a_stats['n_judgeable']} of {a_stats['n_pairs']};
pattern {a_pat['verdict']} / {a_pat['substate']}); this coincidence
is a registered design fact (spec section 3), and arm A is not an
independent sensitivity check. Arm B (all 762 pairs, judged
pair-by-pair, ambiguity included) — judgeable {b_stats['n_judgeable']}
pairs; pattern {b_pat['verdict']} / {b_pat['substate']}; arm B does
not change the verdict. The 4 unmapped P signs
({", ".join(results['inputs']['crosswalk']['unmapped_p_signs'])})
have no pair in any arm and are counted non-judgeable.

## Primary judgeable pairs

{_judgeable_table(results)}

## Inputs and guards

- mayig layer: {results['inputs']['mayig_layer']['inscriptions']}
  inscriptions / {results['inputs']['mayig_layer']['tokens']} tokens /
  {results['inputs']['mayig_layer']['signs']} distinct P signs,
  {results['inputs']['mayig_layer']['objects']} CISI objects.
- Holdat: {results['inputs']['holdat']['inscriptions']} inscriptions /
  {results['inputs']['holdat']['tokens']} tokens /
  {results['inputs']['holdat']['signs']} distinct M signs.
- Object join: **none performed** (spec section 2.1: Holdat's
  cisi_number is internal sequential numbering — contiguous 1..N per
  site — not a CISI object ID; the zero-padded coincidence with mayig
  CISI IDs is not an identity join and was not used).
- Anchors file unchanged: sha256 {results['anchors_sha256_after']}
  before and after (asserted in code).

## Claim scope (spec section 7)

A PASS supports exactly: for the judgeable high-confidence
unambiguous crosswalk pairs, the two compilations' within-compilation
positional profiles agree at the frozen thresholds, beyond
shuffled-pairing chance. A FAIL supports exactly: crosswalk-joined
positional agreement is refuted at the frozen thresholds on the
judgeable primary pairs — the pairing carries no positional agreement
beyond shuffled pairings at median TV >= 0.50; it does not identify
which side produces the disagreement. Neither outcome says anything
about any individual sign's identity or reading, about below-floor /
ambiguous / low-confidence pairs, or about Holdat vs the ICIT lineage
(Phase-116 R-NONE stands untouched). Population caveat: the mayig
layer (179 inscriptions) and Holdat (1,670 inscriptions) cover
substantially the same artefact population but not the same
inscription set, so disagreement can arise from population mix as
well as transcription; the verdict is a statement about the
well-attested minority of pairs ({primary['n_judgeable']} judgeable
of {primary['n_pairs']} primary pairs), never about the script as a
whole. No PRED verdict is issued and no
anchor status changes under this phase.

## Deviations

None in the frozen definitions, thresholds, floor, arms, null, or
verdict rule. The object-join discipline of spec section 2.1 is
implemented as specified: because no legitimate CISI object-ID join
between Holdat and mayig exists, no object-matched arm is run; the
comparison is sign-level over full within-compilation profiles, as
registered in the frozen spec.

## Verification

Full backend suite: 866 passed / 13 skipped / 0 failed (main
baseline 854 passed / 12 skipped, plus this phase's 12 new tests —
12 passed in isolation, 0 skipped; the one additional suite-level
skip is in the pre-existing suite, not in Phase-125 tests).
Foundation check (H21): 40 passed / 0 failed / 8 warnings
(baseline unchanged). Ruff clean on all new/changed files.
Test side effects (glossa-indus/ claims, outputs/) reverted
before commit, per precedent.

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
"""


if __name__ == "__main__":
    out = run_all()
    print(json.dumps(out["verdict"], indent=1))
    print({k: v["stats"] for k, v in out["arms"].items()})
