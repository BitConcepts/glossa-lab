"""Phase-383 (Spec 026) — C4 rescoring of the coding pilots.

Rerun contract: specs/026-rcph-framework-transfer/reruns/
phase383-contract.md (frozen at the S3 merge; freeze record
phase383-freeze.json). Rescoring ONLY — no re-coding. The script
recomputes the headline statistics of Phases 132/134/135 FROM
THE ON-DISK CODING RECORDS using the original metrics modules'
own loaders (imported, not reimplemented), asserts equality
with the committed metrics JSONs, and adds what the originals
lacked: bootstrap 95% CIs over objects (B = 9,999, seed
20261011), plus the coder origin-group audit the framework
requires (all passes in all three pilots share ONE origin
group — the same model family — so pass agreement is
intra-origin consistency, not independent corroboration).

Verdicts follow each pilot's own frozen gates, read under the
Spec 026 taxonomy (spec.md sec.8).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "backend" / "scripts"
MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
STORE_BASE = MAIN_CHECKOUT / "corpora" / "downloads" / "cisi_image_layer"
DEFAULT_OUT = REPO_ROOT / "reports" / "phase383_results.json"

SEED = 20261011
B_BOOT = 9999


def _load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _ci(values: np.ndarray) -> list[float]:
    lo, hi = np.percentile(values, [2.5, 97.5])
    return [float(lo), float(hi)]


# ---------------------------------------------------------------- Phase-132
def rescore_132(rng: np.random.Generator, verify_only: bool) -> dict:
    m = _load_module("phase132_metrics")
    store = STORE_BASE / "phase132_pilot"
    metrics = m.compute_metrics(store)
    committed = json.loads(
        (REPO_ROOT / "reports" / "phase132_pilot_metrics.json").read_text("utf-8")
    )
    exact_all = metrics["verdicts"]["stop_rule"][
        "exact_sequence_agreement_all_50_p"]
    committed_exact = committed["verdicts"]["stop_rule"][
        "exact_sequence_agreement_all_50_p"]
    if abs(float(exact_all) - float(committed_exact)) > 1e-9:
        raise SystemExit(
            f"132 recompute mismatch: {exact_all} != committed {committed_exact}"
        )

    # Per-object pairs in P space, rebuilt with the module's own pieces.
    crosswalk = json.loads(m.CROSSWALK_PATH.read_text("utf-8"))
    m_to_p = m.build_m_to_p(crosswalk["rows"])
    data = m.load_store(store)
    keys = data["keys"]

    def derived(records):
        return m.derive_sequence([t["m_id"] for t in records], m_to_p)

    pairs = [
        (
            m.p_values(derived(data["passes"]["pass_a"][k])),
            m.p_values(derived(data["passes"]["pass_b"][k])),
        )
        for k in keys
    ]
    exact_ind = np.array([1.0 if a == b else 0.0 for a, b in pairs])
    tok_match = np.array([float(m.alignment_matches(a, b)) for a, b in pairs])
    tok_denom = np.array([float(max(len(a), len(b))) for a, b in pairs])
    out: dict = {
        "pilot": "Phase-132",
        "n_objects": len(keys),
        "recomputed_exact_sequence_agreement_all50_p": float(exact_ind.mean()),
        "committed_exact_sequence_agreement_all50_p": float(committed_exact),
        "recomputed_per_token_agreement_p": float(tok_match.sum() / tok_denom.sum()),
    }
    if verify_only:
        return out
    idx = rng.integers(0, len(keys), size=(B_BOOT, len(keys)))
    boot_exact = exact_ind[idx].mean(axis=1)
    boot_tok = tok_match[idx].sum(axis=1) / tok_denom[idx].sum(axis=1)
    out["bootstrap_exact_seq_ci95"] = _ci(boot_exact)
    out["bootstrap_per_token_ci95"] = _ci(boot_tok)
    out["taxonomy_verdict"] = (
        "CONTRADICTED (bounded claim: this AI coding basis at this "
        "protocol can produce a publishable keyed transcription "
        "layer) — the frozen stop-rule fired at 0.20 vs the 0.80 "
        "floor, and the bootstrap CI sits far below the floor"
    )
    return out


# ------------------------------------------------------------- Phases 134/135
def _motif_pairs(mod) -> tuple[list[str], list[tuple[str, str]]]:
    frame_doc = json.loads(mod.FRAME.read_text("utf-8"))
    frame_keys = [o["canonical_key"] for o in frame_doc["frame"]]
    pass_a, _ = mod.load_pass([f"pass_a_batch{i}" for i in range(1, 5)])
    pass_b, _ = mod.load_pass([f"pass_b_batch{i}" for i in range(1, 5)])
    if set(pass_a) != set(frame_keys) or set(pass_b) != set(frame_keys):
        raise SystemExit("motif pilot: record set != frame set")
    pairs = [
        (pass_a[k]["primary_motif"], pass_b[k]["primary_motif"])
        for k in frame_keys
    ]
    return frame_keys, pairs


def _illegible_agreement(pairs: list[tuple[str, str]]) -> float | None:
    either = [(a, b) for a, b in pairs if a == "ILLEGIBLE" or b == "ILLEGIBLE"]
    if not either:
        return None
    return sum(1 for a, b in either if a == b) / len(either)


def rescore_motif(mod_name: str, phase: str, committed_path: str,
                  rng: np.random.Generator, verify_only: bool) -> dict:
    mod = _load_module(mod_name)
    _, pairs = _motif_pairs(mod)
    a_codes = [a for a, _ in pairs]
    b_codes = [b for _, b in pairs]
    kappa, po, _pe, _matrix = mod.cohens_kappa(a_codes, b_codes)
    committed = json.loads((REPO_ROOT / committed_path).read_text("utf-8"))
    c_agree = committed["exact_agreement"]
    c_kappa = committed["cohens_kappa"]
    if abs(po - float(c_agree)) > 1e-9 or abs(kappa - float(c_kappa)) > 1e-9:
        raise SystemExit(
            f"{phase} recompute mismatch: ({po}, {kappa}) != committed "
            f"({c_agree}, {c_kappa})"
        )
    out: dict = {
        "pilot": phase,
        "n_objects": len(pairs),
        "recomputed_exact_agreement": po,
        "recomputed_cohens_kappa": kappa,
        "committed_exact_agreement": float(c_agree),
        "committed_cohens_kappa": float(c_kappa),
        "recomputed_illegible_category_agreement": _illegible_agreement(pairs),
    }
    if verify_only:
        return out
    n = len(pairs)
    idx = rng.integers(0, n, size=(B_BOOT, n))
    boot_agree = np.empty(B_BOOT)
    boot_kappa = np.empty(B_BOOT)
    for r in range(B_BOOT):
        sel = idx[r]
        aa = [a_codes[i] for i in sel]
        bb = [b_codes[i] for i in sel]
        k_r, po_r, _pe_r, _m = mod.cohens_kappa(aa, bb)
        boot_agree[r] = po_r
        boot_kappa[r] = k_r
    agree_ci = _ci(boot_agree)
    out["bootstrap_agreement_ci95"] = agree_ci
    out["bootstrap_kappa_ci95"] = _ci(boot_kappa)
    out["near_miss_adjudication"] = (
        "CI upper bound < 0.85: the 'missed by one object' framing is "
        "not supported as a sampling statement"
        if agree_ci[1] < 0.85 else
        "CI reaches 0.85: the near-miss framing cannot be excluded "
        "on sampling grounds"
    )
    out["taxonomy_verdict"] = (
        "INCONCLUSIVE — the pilot's own frozen gates put the result "
        "in the middle band (proceed gate unmet, stop rule unfired); "
        "no confirmation test was completed on this basis"
    )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    rng = np.random.default_rng(SEED)
    p132 = rescore_132(rng, args.verify_only)
    print("Phase-132 recompute OK:", p132["recomputed_exact_sequence_agreement_all50_p"])
    p134 = rescore_motif("phase134_metrics", "Phase-134",
                         "reports/phase134_pilot_metrics.json", rng, args.verify_only)
    print("Phase-134 recompute OK:", p134["recomputed_exact_agreement"], p134["recomputed_cohens_kappa"])
    p135 = rescore_motif("phase135_metrics", "Phase-135",
                         "reports/phase135_pilot_metrics.json", rng, args.verify_only)
    print("Phase-135 recompute OK:", p135["recomputed_exact_agreement"], p135["recomputed_cohens_kappa"])
    if args.verify_only:
        return 0

    results = {
        "phase": "Phase-383",
        "spec": "026",
        "reruns": "Phases 132/134/135 — C4 rescoring from on-disk records",
        "contract": "specs/026-rcph-framework-transfer/reruns/phase383-contract.md",
        "parameters": {"B_bootstrap": B_BOOT, "seed": SEED},
        "origin_group_audit": (
            "All coding roles in all three pilots (pass_a, pass_b, "
            "pass_gold, adjudicator) were executed by AI agents of ONE "
            "model family (Muse Spark, via Muse), per the "
            "pilots' own disclosure. Effective independent coder "
            "origin groups = 1. Pass agreement is intra-origin "
            "consistency, not independent corroboration."
        ),
        "pilots": {"phase132": p132, "phase134": p134, "phase135": p135},
        "ai_disclosure": (
            "Executed by an AI agent (Muse Spark, via Muse) "
            "at the direction of Tristen Pierson, per constitution sec.VI."
        ),
    }
    args.out.write_text(json.dumps(results, indent=1), "utf-8")
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
