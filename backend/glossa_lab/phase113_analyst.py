"""Phase-113 analyst (spec 012 sections 8-11).

Reads ONLY the custodian's anonymized panel file. Imports nothing
from any custodian module. Contains: the frozen LDA classifier
(reused by import from phase112_analyst, whose implementation is
spec 010's, itself inherited), the per-round validation gate, the
ladder-aware final models, and the verdict logic (a pure function
of posteriors + the unblinded role map + the adversarial control
shares, called by the orchestrator at the unblinding step).

The gate and verdict bodies are spec 010's, copied from
phase112_analyst and generalized ONLY in (a) feature-subset
selection — every function takes the ladder step's feature_names
and slices panel columns by name — and (b) state paths / the
section 8.4 control set, which now runs over S1-S5 plus the three
adversarial round artifacts A1-A3. Every threshold, seed, and
formula is identical to Phase-112's.

Deterministic, numpy-only.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from glossa_lab.phase112_analyst import (
    FAMILIES,
    GEN_CLASSES,
    LDA,
    NONLING,
    _balanced_accuracy,
    benjamini_hochberg,
)

__all__ = [
    "FAMILIES",
    "GEN_CLASSES",
    "LDA",
    "NONLING",
    "RESULTS_PATH",
    "STATE_DIR",
    "benjamini_hochberg",
    "classify_blind",
    "compute_verdict",
    "control_share",
    "evaluate_gate_ladder",
    "exceedance_p_values",
    "final_training_rows",
    "known_posteriors",
    "train_final_model",
]

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / ".glossa-state" / "phase113"
RESULTS_PATH = REPO_ROOT / "reports" / "phase113_blind_affiliation_results.json"

CONTROL_SHARE_THRESHOLD = 0.95


# ---------------------------------------------------------------------------
# Feature slicing
# ---------------------------------------------------------------------------


def _slice_indices(panel: dict, feature_names: list[str]) -> list[int]:
    panel_names = panel["feature_names"]
    return [panel_names.index(name) for name in feature_names]


def _slice_rows(rows, panel: dict, feature_names: list[str]) -> np.ndarray:
    """Rows (lists in panel column order, or dicts keyed by name)
    sliced to feature_names, as a float array."""
    if rows is None or len(rows) == 0:
        return np.zeros((0, len(feature_names)), dtype=np.float64)
    if isinstance(rows[0], dict):
        return np.array([[float(row[name]) for name in feature_names]
                         for row in rows], dtype=np.float64)
    idx = _slice_indices(panel, feature_names)
    return np.array(rows, dtype=np.float64)[:, idx]


def _member_X(panel: dict, cid: str, feature_names: list[str],
              size_label: str = "primary") -> np.ndarray:
    return _slice_rows(panel["members"][cid][f"features_{size_label}"],
                       panel, feature_names)


# ---------------------------------------------------------------------------
# Validation gate (spec 012 section 9 = spec 009 section 7, per round)
# ---------------------------------------------------------------------------


def evaluate_gate_ladder(panel: dict, feature_names: list[str]) -> dict:
    """Gate for one ladder step. Train draws 0-49, test draws 50-99,
    known corpora only. Thresholds and seeds are Phase-112's."""
    known_ids = panel["known_ids"]
    labels = {cid: panel["members"][cid]["label"] for cid in known_ids}
    classes = sorted(set(labels.values()))

    X_train, y_train, X_test, y_test = [], [], [], []
    for cid in known_ids:
        X = _member_X(panel, cid, feature_names)
        X_train.append(X[:50])
        y_train += [labels[cid]] * 50
        X_test.append(X[50:])
        y_test += [labels[cid]] * 50
    X_train = np.vstack(X_train)
    X_test = np.vstack(X_test)
    y_train_arr = np.array(y_train)

    model = LDA().fit(X_train, y_train_arr, classes)
    post_test = model.posterior(X_test)
    cls_index = {c: i for i, c in enumerate(model.classes_)}

    # ---- G1: binary linguistic vs non-linguistic ----
    ling_cols = [cls_index[c] for c in FAMILIES if c in cls_index]
    nonling_col = cls_index[NONLING]
    ling_post = post_test[:, ling_cols].sum(axis=1)
    pred_binary = ["linguistic" if lp >= post_test[i, nonling_col] else "non_linguistic"
                   for i, lp in enumerate(ling_post)]
    true_binary = ["non_linguistic" if t == NONLING else "linguistic" for t in y_test]
    ba_g1 = _balanced_accuracy(true_binary, pred_binary, ["linguistic", "non_linguistic"])

    rng_boot = np.random.default_rng(np.random.SeedSequence([20261011]))
    idx_ling = np.array([i for i, t in enumerate(true_binary) if t == "linguistic"])
    idx_non = np.array([i for i, t in enumerate(true_binary) if t == "non_linguistic"])
    boot_bas = []
    for _ in range(2000):
        sample = np.concatenate([
            rng_boot.choice(idx_ling, size=len(idx_ling), replace=True),
            rng_boot.choice(idx_non, size=len(idx_non), replace=True),
        ])
        bt = [true_binary[i] for i in sample]
        bp = [pred_binary[i] for i in sample]
        boot_bas.append(_balanced_accuracy(bt, bp, ["linguistic", "non_linguistic"]))
    boot_bas = np.array(boot_bas)
    ci_low = float(np.percentile(boot_bas, 2.5))
    p_g1 = float((1 + int(np.sum(boot_bas <= 0.70))) / (1 + len(boot_bas)))
    g1_pass = bool(ba_g1 >= 0.85 and ci_low > 0.70)

    # ---- G2: family balanced accuracy + permutation test ----
    pred_all = model.predict(X_test)
    fam_true = [t for t in y_test if t in FAMILIES]
    fam_pred = [p for t, p in zip(y_test, pred_all) if t in FAMILIES]
    ba_g2 = _balanced_accuracy(fam_true, fam_pred, FAMILIES)

    rng_perm = np.random.default_rng(np.random.SeedSequence([20261010]))
    n_perm = 1000
    exceed = 0
    for _ in range(n_perm):
        y_perm = rng_perm.permutation(y_train_arr)
        m = LDA().fit(X_train, y_perm, classes)
        pp = m.predict(X_test)
        ba_p = _balanced_accuracy(
            fam_true, [p for t, p in zip(y_test, pp) if t in FAMILIES], FAMILIES)
        if ba_p >= ba_g2:
            exceed += 1
    p_g2 = (1 + exceed) / (1 + n_perm)
    g2_pass = bool(ba_g2 >= 0.70 and p_g2 < 0.001)

    return {
        "feature_names": list(feature_names),
        "g1_binary_balanced_accuracy": ba_g1,
        "g1_bootstrap_ci_low_95": ci_low,
        "g1_p_value": p_g1,
        "g1_pass": g1_pass,
        "g2_family_balanced_accuracy": ba_g2,
        "g2_permutation_p_value": p_g2,
        "g2_n_permutations": n_perm,
        "g2_pass": g2_pass,
        "gate_passed": bool(g1_pass and g2_pass),
        "per_family_recall": {
            fam: float(np.mean([p == fam for t, p in zip(fam_true, fam_pred) if t == fam]))
            if any(t == fam for t in fam_true) else None
            for fam in FAMILIES
        },
    }


# ---------------------------------------------------------------------------
# Final (round) model
# ---------------------------------------------------------------------------


def final_training_rows(panel: dict, feature_names: list[str]):
    """(X, y) for a round's final model: all draws of every known
    corpus plus the disclosed S3/S4 generator-training rows, sliced
    to feature_names. Gen-train rows are read from
    panel["gen_train"] ({"rows": [dicts keyed by name], "labels"})
    when present, else from the Phase-112-style
    panel["generator_train"] ({class: rows}) mapping."""
    X_parts, y_parts = [], []
    for cid in panel["known_ids"]:
        X = _member_X(panel, cid, feature_names)
        X_parts.append(X)
        y_parts += [panel["members"][cid]["label"]] * len(X)
    gen_train = panel.get("gen_train")
    if isinstance(gen_train, dict) and "rows" in gen_train:
        rows = gen_train["rows"]
        labels = list(gen_train["labels"])
        if len(rows):
            X_parts.append(_slice_rows(rows, panel, feature_names))
            y_parts += labels
    elif panel.get("generator_train"):
        for cls_name in sorted(panel["generator_train"]):
            rows = panel["generator_train"][cls_name]
            X_parts.append(_slice_rows(rows, panel, feature_names))
            y_parts += [cls_name] * len(rows)
    X = np.vstack(X_parts) if X_parts else np.zeros((0, len(feature_names)))
    return X, np.array(y_parts)


def train_final_model(panel: dict, feature_names: list[str]) -> LDA:
    """A round's frozen final-model instance C_r (spec section 8.1):
    LDA on all known draws + the generator classes, L_r features."""
    X, y = final_training_rows(panel, feature_names)
    classes = sorted(set(y.tolist()))
    return LDA().fit(X, y, classes)


def classify_blind(panel: dict, model: LDA, feature_names: list[str],
                   size_label: str = "primary") -> dict[str, np.ndarray]:
    """Posteriors for every blind ID's draws at one size."""
    out: dict[str, np.ndarray] = {}
    for cid in panel["blind_ids"]:
        if f"features_{size_label}" in panel["members"][cid]:
            out[cid] = model.posterior(_member_X(panel, cid, feature_names, size_label))
    return out


def known_posteriors(panel: dict, model: LDA, feature_names: list[str],
                     size_label: str = "primary") -> dict[str, np.ndarray]:
    out: dict[str, np.ndarray] = {}
    for cid in panel["known_ids"]:
        if f"features_{size_label}" in panel["members"][cid]:
            out[cid] = model.posterior(_member_X(panel, cid, feature_names, size_label))
    return out


# ---------------------------------------------------------------------------
# Control validity (spec sections 8.2 / 8.4)
# ---------------------------------------------------------------------------


def control_share(post: np.ndarray, classes: list[str]) -> float:
    """Share of draws classified non-linguistic under the binary
    collapse: (non_linguistic + gen classes) posterior mass >= the
    summed family posterior mass."""
    post = np.asarray(post, dtype=np.float64)
    if post.size == 0:
        return 0.0
    col = {c: i for i, c in enumerate(classes)}
    fam_cols = [col[f] for f in FAMILIES if f in col]
    nonling_cols = [col[NONLING]] + [col[g] for g in GEN_CLASSES if g in col]
    nonling_mass = post[:, nonling_cols].sum(axis=1)
    fam_mass = post[:, fam_cols].sum(axis=1)
    return float(np.mean(nonling_mass >= fam_mass))


# ---------------------------------------------------------------------------
# Verdict logic (spec 012 section 10 = spec 009 section 9, with the
# section 8.4 control set extended to A1-A3). Pure function of
# posteriors and the unblinded role map. Called by the orchestrator
# AFTER unblinding.
# ---------------------------------------------------------------------------


def _median_odds(post: np.ndarray, col_a: int, col_b: int) -> float:
    odds = post[:, col_a] / np.maximum(post[:, col_b], 1e-300)
    return float(np.median(odds))


def compute_verdict(
    posteriors: dict[str, np.ndarray],
    classes: list[str],
    roles: dict[str, str],          # cid -> target code or synthetic code
    known_post: dict[str, np.ndarray] | None = None,
    known_labels: dict[str, str] | None = None,   # cid -> class label (known)
    control_shares_extra: dict[str, float] | None = None,
) -> dict:
    """roles maps blind cids to R1/R2/R3/S1..S5 codes (full custodian
    codes, as in Phase-112). control_shares_extra carries the A1-A3
    shares (section 8.4), computed by the orchestrator from the
    stored adversarial L3 matrices under C_3."""
    col = {c: i for i, c in enumerate(classes)}
    fam_cols = [col[f] for f in FAMILIES if f in col]
    rep = {code: posteriors[cid] for cid, code in roles.items()
           if code.startswith("R")}
    synth = {code: posteriors[cid] for cid, code in roles.items()
             if code.startswith("S")}

    # ---- Control validity (section 8.4: S1-S5 + A1-A3) ----
    control: dict[str, float] = {}
    for code, post in synth.items():
        control[code] = control_share(post, classes)
    for name, share in (control_shares_extra or {}).items():
        control[name] = float(share)
    failing = [code for code, share in control.items()
               if share < CONTROL_SHARE_THRESHOLD]
    if failing:
        return {"verdict": "INVALID RUN — CONTROL VALIDITY FAILED",
                "control_validity_shares": control,
                "failing_controls": failing}

    # ---- Per-replicate summaries ----
    summaries: dict[str, dict] = {}
    for code, post in rep.items():
        ling = post[:, fam_cols].sum(axis=1)
        med_fam = {f: float(np.median(post[:, col[f]])) for f in FAMILIES}
        winner = max(med_fam, key=med_fam.get)
        summaries[code] = {
            "median_linguistic_posterior": float(np.median(ling)),
            "binary_linguistic": bool(np.median(ling) >= 0.5),
            "winner_family": winner,
            "median_family_posteriors": med_fam,
            "winner_draw_argmax_share": float(
                np.mean(post.argmax(axis=1) == col[winner])),
        }

    # ---- V1 replicate consistency (binary level) ----
    binaries = {s["binary_linguistic"] for s in summaries.values()}
    if len(binaries) != 1:
        return {"verdict": "UNSTABLE / INCONCLUSIVE",
                "control_validity_shares": control, "failing_controls": [],
                "replicates": summaries}

    # ---- V2 linguistic BF per replicate ----
    v2: dict[str, dict] = {}
    v2_all = True
    for code, post in rep.items():
        ling_mass = post[:, fam_cols].sum(axis=1)
        bf_heraldic = float(np.median(ling_mass / np.maximum(post[:, col["gen_heraldic"]], 1e-300)))
        bf_admin = float(np.median(ling_mass / np.maximum(post[:, col["gen_administrative"]], 1e-300)))
        bf_attested = float(np.median(ling_mass / np.maximum(post[:, col[NONLING]], 1e-300)))
        ok = bf_heraldic >= 10 and bf_admin >= 10 and bf_attested >= 10
        v2[code] = {"bf_vs_heraldic_gen": bf_heraldic, "bf_vs_admin_gen": bf_admin,
                    "bf_vs_attested_nonling": bf_attested, "pass": bool(ok)}
        v2_all = v2_all and ok
    if not v2_all:
        return {"verdict": "NOT ESTABLISHED", "control_validity_shares": control,
                "failing_controls": [], "replicates": summaries,
                "v2_linguistic_bf": v2}

    # ---- Family level ----
    winners = {s["winner_family"] for s in summaries.values()}
    if len(winners) != 1:
        return {"verdict": "UNSTABLE / INCONCLUSIVE",
                "control_validity_shares": control, "failing_controls": [],
                "replicates": summaries, "v2_linguistic_bf": v2}
    winner = summaries["R1_indus_holdat_m77"]["winner_family"]

    pooled = np.vstack([rep[c] for c in rep])
    med_fam_pooled = {f: float(np.median(pooled[:, col[f]])) for f in FAMILIES}
    ranked = sorted(med_fam_pooled.items(), key=lambda kv: -kv[1])
    runner_up = ranked[1][0]

    bf_vs_runner = _median_odds(pooled, col[winner], col[runner_up])
    bf_vs_heraldic = float(np.median(
        pooled[:, col[winner]] / np.maximum(pooled[:, col["gen_heraldic"]], 1e-300)))
    bf_vs_admin = float(np.median(
        pooled[:, col[winner]] / np.maximum(pooled[:, col["gen_administrative"]], 1e-300)))

    # TOST on winner - runner-up posterior difference (bootstrap over draws)
    diffs = pooled[:, col[winner]] - pooled[:, col[runner_up]]
    rng = np.random.default_rng(np.random.SeedSequence([20261016]))
    boots = []
    for _ in range(2000):
        sample = rng.choice(diffs, size=len(diffs), replace=True)
        boots.append(float(np.median(sample)))
    ci_lo, ci_hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
    tost_equiv = (ci_lo >= -0.05) and (ci_hi <= 0.05)

    family_detail = {
        "winner": winner, "runner_up": runner_up,
        "pooled_median_family_posteriors": med_fam_pooled,
        "bf_vs_runner_up": bf_vs_runner,
        "bf_vs_heraldic_gen": bf_vs_heraldic,
        "bf_vs_admin_gen": bf_vs_admin,
        "tost_ci_95": [ci_lo, ci_hi], "tost_equivalent": bool(tost_equiv),
    }

    # ---- V4 refutation / no discrimination ----
    if bf_vs_runner < 3 or tost_equiv:
        return {"verdict": "NO FAMILY DISCRIMINATION",
                "control_validity_shares": control, "failing_controls": [],
                "replicates": summaries, "v2_linguistic_bf": v2,
                "family": family_detail}

    # ---- V5 suffixing confound ----
    if winner == "dravidian":
        bf_vs_sum = _median_odds(pooled, col[winner], col["isolate_sumerian"])
        dsum = pooled[:, col[winner]] - pooled[:, col["isolate_sumerian"]]
        boots = []
        for _ in range(2000):
            sample = rng.choice(dsum, size=len(dsum), replace=True)
            boots.append(float(np.median(sample)))
        lo, hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
        family_detail["bf_vs_isolate_sumerian"] = bf_vs_sum
        family_detail["tost_ci_vs_sumerian"] = [lo, hi]
        if bf_vs_sum < 3 or (lo >= -0.05 and hi <= 0.05):
            return {"verdict": "NO FAMILY DISCRIMINATION (suffixing confound not excluded)",
                    "control_validity_shares": control, "failing_controls": [],
                    "replicates": summaries, "v2_linguistic_bf": v2,
                    "family": family_detail}

    # ---- V3 support ----
    v3_checks = {
        "median_posterior_ge_0.90_each_replicate": all(
            summaries[c]["median_family_posteriors"][winner] >= 0.90 for c in rep),
        "bf_vs_runner_up_ge_10": bf_vs_runner >= 10,
        "bf_vs_heraldic_ge_10": bf_vs_heraldic >= 10,
        "bf_vs_admin_ge_10": bf_vs_admin >= 10,
        "same_winner_both_sign_lists": (
            summaries["R1_indus_holdat_m77"]["winner_family"] == winner
            and summaries["R2_indus_icit_wells"]["winner_family"] == winner),
        "argmax_share_ge_0.90_R1_R2": (
            summaries["R1_indus_holdat_m77"]["winner_draw_argmax_share"] >= 0.90
            and summaries["R2_indus_icit_wells"]["winner_draw_argmax_share"] >= 0.90),
    }
    family_detail["v3_checks"] = v3_checks
    if all(v3_checks.values()):
        verdict = f"SUPPORTED: {winner}"
    else:
        verdict = "NO FAMILY DISCRIMINATION"
        family_detail["note"] = (
            "V3 support bar not fully met although V4 equivalence did "
            "not trigger; reported under the frozen verdict vocabulary "
            "as no established family discrimination. See v3_checks.")
    return {"verdict": verdict, "control_validity_shares": control,
            "failing_controls": [], "replicates": summaries,
            "v2_linguistic_bf": v2, "family": family_detail}


def exceedance_p_values(
    posteriors: dict[str, np.ndarray],
    classes: list[str],
    roles: dict[str, str],
    gate: dict,
) -> dict:
    """T3/T4 draw-exceedance p-values (spec section 11). T1/T2 come
    from the gate dict passed in (the round-1 gate instances are the
    primary ones, per spec section 11). T5 is added by the run
    module, as in Phase-112."""
    col = {c: i for i, c in enumerate(classes)}
    fam_cols = [col[f] for f in FAMILIES if f in col]
    rep = {code: posteriors[cid] for cid, code in roles.items() if code.startswith("R")}
    synth = {code: posteriors[cid] for cid, code in roles.items() if code.startswith("S")}
    pooled = np.vstack([rep[c] for c in rep])
    indus_ling_med = float(np.median(pooled[:, fam_cols].sum(axis=1)))
    out: dict[str, float] = {}
    out["T1_gate_linguistic"] = gate["g1_p_value"]
    out["T2_gate_family"] = gate["g2_permutation_p_value"]
    for tname, scode in (("T3_vs_heraldic_gen", "S3_heraldic_gen"),
                         ("T4_vs_admin_gen", "S4_admin_gen")):
        if scode in synth:
            ling = synth[scode][:, fam_cols].sum(axis=1)
            out[tname] = float((1 + int(np.sum(ling >= indus_ling_med))) / (1 + len(ling)))
    return out
