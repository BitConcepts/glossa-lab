"""Phase-111 analyst (spec 009 sections 6-10).

Reads ONLY the custodian's anonymized panel file. Imports nothing
from the custodian. Contains: the frozen LDA classifier, the
validation gate, final-model classification of the blind IDs, and
the verdict logic (a pure function of posteriors + the unblinded
role map, called by the orchestrator at the unblinding step).

Deterministic, numpy-only. All thresholds are spec 009's frozen
values; changing them post-freeze is a spec deviation (section 11).

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

import numpy as np

FAMILIES = [
    "dravidian",
    "indo_aryan",
    "semitic",
    "indo_european_other",
    "isolate_sumerian",
    "turkic",
    "austronesian",
]
NONLING = "non_linguistic"
GEN_CLASSES = ["gen_heraldic", "gen_administrative"]
SHRINKAGE = 0.1  # frozen (spec section 6)
_JITTER = 1e-9


class LDA:
    """Linear discriminant analysis, shared shrunk covariance,
    equal priors. Deterministic closed-form fit."""

    def __init__(self, shrinkage: float = SHRINKAGE):
        self.shrinkage = shrinkage

    def fit(self, X: np.ndarray, y: np.ndarray, classes: list[str]) -> "LDA":
        self.classes_ = list(classes)
        self.x_mean_ = X.mean(axis=0)
        self.x_std_ = X.std(axis=0)
        self.x_std_[self.x_std_ == 0] = 1.0
        Z = (X - self.x_mean_) / self.x_std_
        n, d = Z.shape
        c = len(self.classes_)
        means = np.zeros((c, d))
        scatter = np.zeros((d, d))
        for ci, cls in enumerate(self.classes_):
            Zc = Z[y == cls]
            means[ci] = Zc.mean(axis=0)
            centred = Zc - means[ci]
            scatter += centred.T @ centred
        cov = scatter / max(n - c, 1)
        cov = (1 - self.shrinkage) * cov + self.shrinkage * np.diag(np.diag(cov))
        cov += _JITTER * np.eye(d)
        self.cov_inv_ = np.linalg.inv(cov)
        self.means_ = means
        # discriminant coefficients: delta_c(x) = x @ w_c + b_c
        self.w_ = (self.cov_inv_ @ means.T).T  # (c, d)
        self.b_ = -0.5 * np.sum(means @ self.cov_inv_ * means, axis=1)
        return self

    def posterior(self, X: np.ndarray) -> np.ndarray:
        Z = (X - self.x_mean_) / self.x_std_
        logits = Z @ self.w_.T + self.b_
        logits = logits - logits.max(axis=1, keepdims=True)
        exp = np.exp(logits)
        return exp / exp.sum(axis=1, keepdims=True)

    def predict(self, X: np.ndarray) -> list[str]:
        post = self.posterior(X)
        idx = post.argmax(axis=1)
        return [self.classes_[i] for i in idx]


def _member_X(panel: dict, cid: str, size_label: str = "primary") -> np.ndarray:
    return np.array(panel["members"][cid][f"features_{size_label}"], dtype=np.float64)


def _balanced_accuracy(y_true: list[str], y_pred: list[str], classes: list[str]) -> float:
    recalls = []
    for cls in classes:
        mask = [t == cls for t in y_true]
        n = sum(mask)
        if n == 0:
            continue
        correct = sum(1 for t, p, m in zip(y_true, y_pred, mask) if m and p == cls)
        recalls.append(correct / n)
    return float(np.mean(recalls)) if recalls else 0.0


def evaluate_gate(panel: dict) -> dict:
    """Spec section 7. Train draws 0-49, test draws 50-99, known only."""
    known_ids = panel["known_ids"]
    labels = {cid: panel["members"][cid]["label"] for cid in known_ids}
    classes = sorted(set(labels.values()))

    X_train, y_train, X_test, y_test = [], [], [], []
    for cid in known_ids:
        X = _member_X(panel, cid)
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


def train_final_model(panel: dict) -> tuple[LDA, list[str]]:
    """Final model: all draws of known corpora + generator classes."""
    X_parts, y_parts = [], []
    for cid in panel["known_ids"]:
        X_parts.append(_member_X(panel, cid))
        y_parts += [panel["members"][cid]["label"]] * len(X_parts[-1])
    for cls_name, rows in panel["generator_train"].items():
        X_parts.append(np.array(rows, dtype=np.float64))
        y_parts += [cls_name] * len(rows)
    X = np.vstack(X_parts)
    y = np.array(y_parts)
    classes = sorted(set(y.tolist()))
    model = LDA().fit(X, y, classes)
    return model, classes


def classify_blind(panel: dict, model: LDA) -> dict[str, np.ndarray]:
    """Posteriors for every blind ID's primary draws."""
    out: dict[str, np.ndarray] = {}
    for cid in panel["blind_ids"]:
        out[cid] = model.posterior(_member_X(panel, cid))
    return out


def known_posteriors(panel: dict, model: LDA) -> dict[str, np.ndarray]:
    out: dict[str, np.ndarray] = {}
    for cid in panel["known_ids"]:
        out[cid] = model.posterior(_member_X(panel, cid))
    return out


# --------------------------------------------------------------------------
# Verdict logic (spec section 9). Pure function of posteriors and the
# unblinded role map. Called by the orchestrator AFTER unblinding.
# --------------------------------------------------------------------------


def _median_odds(post: np.ndarray, col_a: int, col_b: int) -> float:
    odds = post[:, col_a] / np.maximum(post[:, col_b], 1e-300)
    return float(np.median(odds))


def compute_verdict(
    posteriors: dict[str, np.ndarray],
    classes: list[str],
    roles: dict[str, str],          # cid -> target code or synthetic code
    known_post: dict[str, np.ndarray],
    known_labels: dict[str, str],   # cid -> class label (known corpora)
) -> dict:
    """roles maps blind cids to R1/R2/R3/S1/S2/S3/S4 codes."""
    col = {c: i for i, c in enumerate(classes)}
    fam_cols = [col[f] for f in FAMILIES if f in col]
    rep = {code: posteriors[cid] for cid, code in roles.items()
           if code.startswith("R")}
    synth = {code: posteriors[cid] for cid, code in roles.items()
             if code.startswith("S")}

    # ---- Control validity (section 8) ----
    nonling_mass_cols = [col[NONLING]] + [col[g] for g in GEN_CLASSES if g in col]
    control: dict[str, float] = {}
    control_ok = True
    for code, post in synth.items():
        nonling_mass = post[:, nonling_mass_cols].sum(axis=1)
        fam_mass = post[:, fam_cols].sum(axis=1)
        share = float(np.mean(nonling_mass >= fam_mass))
        control[code] = share
        if share < 0.95:
            control_ok = False
    if not control_ok:
        return {"verdict": "INVALID RUN — CONTROL VALIDITY FAILED",
                "control_validity_shares": control}

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
                "control_validity_shares": control, "replicates": summaries}

    # ---- V2 linguistic BF per replicate ----
    v2: dict[str, dict] = {}
    v2_all = True
    for code, post in rep.items():
        # BF for linguistic over a comparator class = median over draws
        # of P(linguistic)/P(comparator) (spec section 9 operationalization)
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
                "replicates": summaries, "v2_linguistic_bf": v2}

    # ---- Family level ----
    winners = {s["winner_family"] for s in summaries.values()}
    if len(winners) != 1:
        return {"verdict": "UNSTABLE / INCONCLUSIVE",
                "control_validity_shares": control, "replicates": summaries,
                "v2_linguistic_bf": v2}
    winner = summaries["R1_indus_holdat_m77"]["winner_family"]

    # Runner-up: second-highest pooled median posterior
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
                "control_validity_shares": control, "replicates": summaries,
                "v2_linguistic_bf": v2, "family": family_detail}

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
                    "control_validity_shares": control, "replicates": summaries,
                    "v2_linguistic_bf": v2, "family": family_detail}

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
        # Winner is decisive vs runner-up (BF >= 3, not equivalent) but
        # the full support bar is not met: the frozen vocabulary has
        # no partial-support label; the outcome is reported as
        # NO FAMILY DISCRIMINATION only via V4. If V4 did not trigger,
        # the accurate frozen-vocabulary outcome is that support is
        # not established at family level.
        verdict = "NO FAMILY DISCRIMINATION"
        family_detail["note"] = (
            "V3 support bar not fully met although V4 equivalence did "
            "not trigger; reported under the frozen verdict vocabulary "
            "as no established family discrimination. See v3_checks.")
    return {"verdict": verdict, "control_validity_shares": control,
            "replicates": summaries, "v2_linguistic_bf": v2,
            "family": family_detail}


def exceedance_p_values(
    posteriors: dict[str, np.ndarray],
    classes: list[str],
    roles: dict[str, str],
    gate: dict,
) -> dict:
    """T3/T4/T5 draw-exceedance p-values (spec section 10). T1/T2 come
    from the gate. Returns raw p-values for tests that were reached."""
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


def benjamini_hochberg(pvals: dict[str, float], q: float = 0.05) -> dict[str, dict]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    adjusted: dict[str, float] = {}
    running = 1.0
    for i in range(m - 1, -1, -1):
        name, p = items[i]
        running = min(running, p * m / (i + 1))
        adjusted[name] = float(min(running, 1.0))
    return {name: {"raw_p": p, "bh_adjusted_p": adjusted[name],
                   "significant_at_q": bool(adjusted[name] <= q)}
            for name, p in pvals.items()}
