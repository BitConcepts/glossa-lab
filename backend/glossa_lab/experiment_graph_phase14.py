"""Phase-14 atomic node implementations.

This module is the response to the Phase-13 negative finding (the
HoldoutWordRecall + CTT pipeline is decorative on M77) and implements three
new orthogonal layers of analysis:

  Path 1 — Structural language signature
      BlockEntropyProfile, ConditionalEntropyProfile, ZipfMandelbrotFit,
      MutualInformationDecay, LanguageSignatureComparator,
      ReferenceCorpusLoader.

  Path 2 — External grounding from archaeological metadata
      ICITMetadataLoader, SignContextAssociation, DerivedAnchorSet.

  Epistatic engineering layer
      EpistaticInteractionDetector (2nd/3rd/4th-order MI surplus over
      independence + over the bigram baseline), EpistaticOrderProfile
      (Hierarchical Epistasis Decomposition), EpistaticAnchorRanker
      (rank candidate anchors by their epistatic-centrality score).

  Integrative
      LanguageDetectorVerdict — combine all signature tests into a single
      {is_language, confidence, evidence_for, evidence_against, verdict}
      output. This is the answer to "is the Indus script a real language?"

References
----------
- Rao, R. P. N. et al. (2009). "Entropic Evidence for Linguistic Structure
  in the Indus Script." Science 324:1165.
- Sproat, R. (2014). "A statistical comparison of written language and
  nonlinguistic symbol systems." Language 90(2):457-481.
- Manaris, B. et al. (2005). "Zipf's Law, Music Classification, and
  Aesthetics." (Zipf-Mandelbrot fitting as language fingerprint.)
- Lin, H. W. & Tegmark, M. (2017). "Critical Behavior in Physics and
  Probabilistic Formal Languages." Entropy 19(7). (Power-law MI decay
  as a language fingerprint.)
- Heaps, H. S. (1978). Heaps' law for type-token growth.
- Berg-Kirkpatrick, T. & Klein, D. (2011). "Simple effective decipherment
  via combinatorial optimization." (Berg-Kirkpatrick anchor framework.)
- Whitlock, M. C. et al. (1995). "Multiple fitness peaks and epistasis."
  Annual Review of Ecology and Systematics 26:601-629. (NK landscape
  framing of search problems.)
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

# ── Helpers ──────────────────────────────────────────────────────────────


def _ngram_counts(seqs: list[list[str]], n: int) -> Counter[tuple[str, ...]]:
    out: Counter[tuple[str, ...]] = Counter()
    for s in seqs:
        if len(s) < n:
            continue
        for i in range(len(s) - n + 1):
            out[tuple(s[i : i + n])] += 1
    return out


def _entropy_from_counter(c: Counter, total: int | None = None) -> float:
    """Plain MLE Shannon entropy in nats."""
    if total is None:
        total = sum(c.values())
    if total <= 0:
        return 0.0
    h = 0.0
    for v in c.values():
        if v <= 0:
            continue
        p = v / total
        h -= p * math.log(p)
    return h


def _flatten(seqs: list[list[str]]) -> list[str]:
    return [s for seq in seqs for s in seq]


# ── Path 1.1 — BlockEntropyProfile ───────────────────────────────────────


def _block_entropy_profile(inputs: dict, params: dict) -> dict:
    """Compute H(n) for n=1..max_n on the input sequences.

    Reuses the same plain-MLE estimator used by glossa_lab.pipelines.block_entropy
    so cross-corpus comparisons are calibrated. Output is a list of
    {n, H_nats, H_norm_by_lnL} dicts plus alphabet size + token count, plus a
    label for downstream comparison.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    max_n = max(1, int(params.get("max_n", 6)))
    label = str(params.get("label", "unknown"))

    flat = _flatten(sequences)
    if not flat:
        return {
            "label": label,
            "alphabet_size": 0,
            "n_tokens": 0,
            "block_entropies": [],
            "verdict": "Empty corpus.",
        }

    L = len(set(flat))
    ln_L = math.log(L) if L > 1 else 1.0
    entries: list[dict] = []
    for n in range(1, max_n + 1):
        ngrams = _ngram_counts(sequences, n)
        H = _entropy_from_counter(ngrams)
        entries.append({
            "n": n,
            "H_nats": round(H, 4),
            "H_norm": round(H / ln_L, 4) if ln_L > 0 else 0.0,
            "n_distinct": len(ngrams),
        })

    return {
        "label": label,
        "alphabet_size": L,
        "n_tokens": len(flat),
        "block_entropies": entries,
        "json": {
            "label": label,
            "alphabet_size": L,
            "n_tokens": len(flat),
            "block_entropies": entries,
        },
    }


# ── Path 1.2 — ConditionalEntropyProfile ─────────────────────────────────


def _conditional_entropy_profile(inputs: dict, params: dict) -> dict:
    """h(n) = H(n) - H(n-1).

    A natural language has a *plateau* in h(n) (the conditional entropy
    saturates at a finite value beyond a few orders). Pure unigram-random or
    uniform-random sequences have flat h(n). Highly repetitive (rote-formula)
    corpora have h(n) decaying rapidly to zero.

    Consumes the output of BlockEntropyProfile.
    """
    bep = inputs.get("block_entropies")
    label = ""
    if isinstance(bep, dict):
        label = bep.get("label", "")
        bep = bep.get("block_entropies")
    if not isinstance(bep, list) or not bep:
        return {"conditional_entropies": [], "verdict": "No block_entropies input."}

    by_n = {int(e["n"]): float(e["H_nats"]) for e in bep if "n" in e and "H_nats" in e}
    out: list[dict] = []
    prev: float | None = None
    for n in sorted(by_n.keys()):
        H = by_n[n]
        if prev is None:
            out.append({"n": n, "h_nats": round(H, 4), "delta_from_prev": None})
        else:
            out.append({"n": n, "h_nats": round(H - prev, 4),
                        "delta_from_prev": round((H - prev) - (out[-1]["h_nats"] if out else 0.0), 4)})
        prev = H

    # Plateau detection: check if h(n) decays to within 10% of h(max_n) by
    # n = max_n - 1.
    if len(out) >= 3:
        h_values = [e["h_nats"] for e in out[1:]]  # skip H(1) which is just unigram
        last = h_values[-1]
        plateau = "yes" if abs(h_values[-2] - last) <= 0.1 * max(1e-9, abs(last)) else "no"
    else:
        plateau = "unknown"

    verdict = (
        f"{label or 'unknown'}: conditional entropy plateau={plateau}; "
        f"h(2..{out[-1]['n']}) = "
        + ", ".join(f"{e['h_nats']:.3f}" for e in out[1:])
    )
    return {
        "label": label,
        "conditional_entropies": out,
        "plateau": plateau,
        "verdict": verdict,
        "json": {"label": label, "conditional_entropies": out, "plateau": plateau},
    }


# ── Path 1.3 — ZipfMandelbrotFit ─────────────────────────────────────────


def _zipf_mandelbrot_fit(inputs: dict, params: dict) -> dict:
    """Fit f(r) = C / (r + beta)^alpha to the rank-frequency curve.

    Natural language: alpha ≈ 1.0–1.2, finite beta ≈ 1–10 (small offset).
    Random / uniform: alpha ≈ 0 (flat).
    Power-law without offset (alpha=1 strict Zipf): would give beta ≈ 0;
    deviation toward beta > 0 is a hallmark of finite vocabulary languages.

    We do a coarse 2D grid search over (alpha, beta) with MSE in log-log
    space. Cheap; gives the same diagnostic as scipy.optimize.curve_fit.
    """
    freq_map = inputs.get("freq_map")
    sequences = inputs.get("sequences") or []
    label = str(params.get("label", "unknown"))

    if isinstance(freq_map, dict) and freq_map:
        counts = sorted((float(v) for v in freq_map.values()), reverse=True)
    else:
        flat = _flatten(sequences)
        if not flat:
            return {"label": label, "alpha": 0.0, "beta": 0.0,
                    "verdict": "Empty corpus."}
        counts = sorted(Counter(flat).values(), reverse=True)

    n = len(counts)
    if n < 5:
        return {"label": label, "alpha": 0.0, "beta": 0.0, "n_ranks": n,
                "verdict": "Too few distinct symbols for a fit."}

    # Search a coarse grid then refine with parabolic minimisation.
    [math.log(r + 1) for r in range(n)]
    log_f = [math.log(c) if c > 0 else -1e9 for c in counts]
    mean_log_f = sum(log_f) / n

    def _mse(alpha: float, beta: float) -> float:
        # f_pred ∝ 1 / (r + beta)^alpha → log f_pred = const − alpha * log(r+beta+1).
        pred_unscaled = [-alpha * math.log(r + beta + 1) for r in range(n)]
        m = sum(pred_unscaled) / n
        c = mean_log_f - m  # least-squares C
        s = 0.0
        for i in range(n):
            d = log_f[i] - (pred_unscaled[i] + c)
            s += d * d
        return s / n

    best = (1.0, 1.0, _mse(1.0, 1.0))
    for a_int in range(1, 25):
        a = a_int * 0.1  # 0.1 .. 2.4
        for b_int in range(0, 16):
            b = b_int * 1.0  # 0 .. 15
            m = _mse(a, b)
            if m < best[2]:
                best = (a, b, m)

    alpha, beta, mse = best

    # R^2 for the fit
    pred = [-alpha * math.log(r + beta + 1) for r in range(n)]
    mean_pred = sum(pred) / n
    c = mean_log_f - mean_pred
    ss_res = sum((log_f[i] - (pred[i] + c)) ** 2 for i in range(n))
    ss_tot = sum((log_f[i] - mean_log_f) ** 2 for i in range(n))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    if 0.85 <= alpha <= 1.30 and r2 >= 0.85:
        verdict = (
            f"{label}: alpha={alpha:.2f}, beta={beta:.2f}, R^2={r2:.3f}. "
            "Consistent with a natural-language Zipf-Mandelbrot regime."
        )
    elif alpha < 0.50 or r2 < 0.5:
        verdict = (
            f"{label}: alpha={alpha:.2f}, R^2={r2:.3f}. Inconsistent with "
            "natural-language rank-frequency."
        )
    else:
        verdict = (
            f"{label}: alpha={alpha:.2f}, beta={beta:.2f}, R^2={r2:.3f}. "
            "Atypical Zipf shape; review."
        )
    return {
        "label": label,
        "alpha": round(alpha, 4),
        "beta": round(beta, 4),
        "r_squared": round(r2, 4),
        "mse_log_log": round(mse, 4),
        "n_ranks": n,
        "verdict": verdict,
        "json": {"label": label, "alpha": alpha, "beta": beta, "r2": r2, "n_ranks": n},
    }


# ── Path 1.4 — MutualInformationDecay ────────────────────────────────────


def _mutual_information_decay(inputs: dict, params: dict) -> dict:
    """Compute I(X_t ; X_{t+k}) for k = 1..max_k from the input sequences.

    Power-law decay (I(k) ~ k^{-gamma} with gamma ~ 0.5..1) is the Lin-Tegmark
    fingerprint of natural language. Exponential decay is the fingerprint of
    Markov order-1. Flat / no decay is the fingerprint of unigram-random or
    completely independent emissions.

    We fit log I(k) vs log k and vs k separately, take whichever has the
    higher R^2, and report the regime.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    max_k = max(1, int(params.get("max_k", 8)))
    label = str(params.get("label", "unknown"))

    if not sequences:
        return {"label": label, "verdict": "Empty corpus.", "decay": []}

    # Single-sign distribution
    unigram = Counter(s for seq in sequences for s in seq)
    total_uni = sum(unigram.values()) or 1
    H1 = _entropy_from_counter(unigram, total_uni)

    decay: list[dict] = []
    for k in range(1, max_k + 1):
        joint: Counter[tuple[str, str]] = Counter()
        for seq in sequences:
            if len(seq) <= k:
                continue
            for i in range(len(seq) - k):
                joint[(seq[i], seq[i + k])] += 1
        total_j = sum(joint.values()) or 1
        if total_j < 10:
            decay.append({"k": k, "I_nats": 0.0, "n_pairs": total_j})
            continue
        H_joint = _entropy_from_counter(joint, total_j)
        # Marginals derived from joint to ensure they sum to 1 with the joint
        m_a: Counter[str] = Counter()
        m_b: Counter[str] = Counter()
        for (a, b), c in joint.items():
            m_a[a] += c
            m_b[b] += c
        H_a = _entropy_from_counter(m_a, total_j)
        H_b = _entropy_from_counter(m_b, total_j)
        I = max(0.0, H_a + H_b - H_joint)
        decay.append({"k": k, "I_nats": round(I, 6), "n_pairs": total_j})

    # Fit power-law and exponential decay; pick the better fit.
    pts = [(d["k"], d["I_nats"]) for d in decay if d["I_nats"] > 0]
    regime = "unknown"
    gamma = 0.0
    lam = 0.0
    r2_pow = 0.0
    r2_exp = 0.0
    if len(pts) >= 3:
        # Power-law: log I = -gamma * log k + c
        xs_p = [math.log(k) for k, _ in pts]
        ys_p = [math.log(I) for _, I in pts]
        n = len(pts)
        mx = sum(xs_p) / n
        my = sum(ys_p) / n
        num = sum((xs_p[i] - mx) * (ys_p[i] - my) for i in range(n))
        den = sum((x - mx) ** 2 for x in xs_p)
        slope_p = num / den if den else 0.0
        intercept_p = my - slope_p * mx
        ss_res_p = sum((ys_p[i] - (slope_p * xs_p[i] + intercept_p)) ** 2 for i in range(n))
        ss_tot_p = sum((y - my) ** 2 for y in ys_p)
        r2_pow = 1.0 - ss_res_p / ss_tot_p if ss_tot_p > 0 else 0.0
        gamma = -slope_p

        # Exponential: log I = -lam * k + c
        xs_e = [k for k, _ in pts]
        mx_e = sum(xs_e) / n
        num_e = sum((xs_e[i] - mx_e) * (ys_p[i] - my) for i in range(n))
        den_e = sum((x - mx_e) ** 2 for x in xs_e)
        slope_e = num_e / den_e if den_e else 0.0
        intercept_e = my - slope_e * mx_e
        ss_res_e = sum((ys_p[i] - (slope_e * xs_e[i] + intercept_e)) ** 2 for i in range(n))
        r2_exp = 1.0 - ss_res_e / ss_tot_p if ss_tot_p > 0 else 0.0
        lam = -slope_e

        if r2_pow > r2_exp + 0.05 and gamma > 0:
            regime = "power_law"  # natural-language fingerprint
        elif r2_exp > r2_pow + 0.05 and lam > 0:
            regime = "exponential"  # Markov-1 / non-language
        elif gamma <= 0.05 and lam <= 0.05:
            regime = "flat"  # unigram-random
        else:
            regime = "ambiguous"

    if regime == "power_law":
        verdict = (
            f"{label}: I(k) ~ k^-gamma with gamma={gamma:.2f}, R^2={r2_pow:.3f}. "
            "Power-law decay = natural-language fingerprint."
        )
    elif regime == "exponential":
        verdict = (
            f"{label}: I(k) ~ exp(-lam*k) with lam={lam:.3f}, R^2={r2_exp:.3f}. "
            "Exponential decay = Markov-1 / non-linguistic."
        )
    elif regime == "flat":
        verdict = (
            f"{label}: I(k) ~ flat. Consistent with unigram-random emissions."
        )
    else:
        verdict = (
            f"{label}: gamma={gamma:.2f} (R^2={r2_pow:.3f}), "
            f"lam={lam:.3f} (R^2={r2_exp:.3f}). Ambiguous decay regime."
        )

    return {
        "label": label,
        "decay": decay,
        "regime": regime,
        "gamma_powerlaw": round(gamma, 4),
        "lambda_exponential": round(lam, 4),
        "r2_powerlaw": round(r2_pow, 4),
        "r2_exponential": round(r2_exp, 4),
        "h1_nats": round(H1, 4),
        "verdict": verdict,
        "json": {
            "label": label, "decay": decay, "regime": regime,
            "gamma": gamma, "lambda": lam,
            "r2_pow": r2_pow, "r2_exp": r2_exp,
        },
    }


# ── Path 1.5 — ReferenceCorpusLoader ─────────────────────────────────────


def _reference_corpus_loader(inputs: dict, params: dict) -> dict:
    """Emit sequences (preferred) or [flat] for any of the supported reference
    languages. Matches BuiltinLM's languages but returns raw sequences instead
    of an LM object so the structural-signature nodes can profile them.
    """
    lang = str(params.get("language", "linear_b")).lower().strip()
    label = str(params.get("label", lang))

    seqs: list[list[str]] = []
    flat: list[str] | None = None
    try:
        if lang in ("hebrew", "old_hebrew"):
            from glossa_lab.data.old_hebrew import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            try:
                seqs = list(get_corpus_inscriptions())
            except Exception:  # noqa: BLE001
                flat = list(get_corpus_symbols())
        elif lang == "geez":
            from glossa_lab.data.geez import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            try:
                seqs = list(get_corpus_inscriptions())
            except Exception:  # noqa: BLE001
                flat = list(get_corpus_symbols())
        elif lang == "phoenician":
            from glossa_lab.data.phoenician import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            try:
                seqs = list(get_corpus_inscriptions())
            except Exception:  # noqa: BLE001
                flat = list(get_corpus_symbols())
        elif lang in ("hieroglyphic_luwian", "luwian"):
            from glossa_lab.data.hieroglyphic_luwian import (  # noqa: PLC0415
                get_corpus_inscriptions,
                get_corpus_symbols,
            )
            try:
                seqs = list(get_corpus_inscriptions())
            except Exception:  # noqa: BLE001
                flat = list(get_corpus_symbols())
        elif lang in ("linear_b", "mycenaean_greek", "mycenaean"):
            from glossa_lab.data.linear_b_language import get_corpus_symbols  # noqa: PLC0415
            flat = list(get_corpus_symbols())
        elif lang in ("sanskrit", "vedic_sanskrit", "vedic"):
            from glossa_lab.data.sanskrit import get_corpus_symbols  # noqa: PLC0415
            flat = list(get_corpus_symbols())
        elif lang in ("sumerian", "sumerian_ur3"):
            from glossa_lab.data.sumerian_ur3 import get_corpus_symbols  # noqa: PLC0415
            flat = list(get_corpus_symbols())
        elif lang in ("dravidian", "tamil", "old_tamil"):
            from glossa_lab.data.dravidian import get_word_symbols  # noqa: PLC0415
            flat = list(get_word_symbols())
        elif lang in ("pali", "middle_indo_aryan"):
            from glossa_lab.data.pali import get_corpus_symbols  # noqa: PLC0415
            flat = list(get_corpus_symbols())
        elif lang in ("indus_m77", "m77", "indus"):
            from glossa_lab.data.indus_m77 import get_corpus_inscriptions  # noqa: PLC0415
            seqs = list(get_corpus_inscriptions())
        elif lang in ("indus_cisi", "cisi"):
            from glossa_lab.data.indus_cisi import get_corpus_inscriptions  # noqa: PLC0415
            seqs = list(get_corpus_inscriptions())
        else:
            return {"sequences": [], "language": lang, "label": label,
                    "error": f"Unknown language: {lang}"}
    except Exception as exc:  # noqa: BLE001
        return {"sequences": [], "language": lang, "label": label,
                "error": str(exc)}

    if not seqs and flat is not None:
        # Wrap as a single sequence; many corpora are stored only as flat
        # symbol streams without word boundaries. The structural-signature
        # nodes still operate correctly because they compute n-gram statistics
        # on the flattened token stream.
        seqs = [list(flat)]
    n_tokens = sum(len(s) for s in seqs)
    return {
        "sequences": seqs,
        "language": lang,
        "label": label,
        "n_sequences": len(seqs),
        "n_tokens": n_tokens,
        "distinct_symbols": len({s for seq in seqs for s in seq}),
    }


# ── Path 1.6 — LanguageSignatureComparator ───────────────────────────────


def _language_signature_comparator(inputs: dict, params: dict) -> dict:
    """Take signature bundles (block-entropy + Zipf-M + MI-decay + epistatic
    profile, all from upstream profilers) for several corpora and rank them
    by similarity to the natural-language reference cluster.

    Inputs (a..f): each port carries one signature dict (the merged JSON
    from a profile chain). Param `target_label` names which bundle is the
    candidate (e.g. "indus_m77"); the others are reference points.

    Output: a ranked list with similarity scores, plus a verdict.

    Spec 087 S3 (family F9): the mechanism is the generic
    SignatureComparator engine (glossa_lab.generic_primitives);
    this node is its Phase-14 parameterisation — the candidate
    tag "indus", the candidate marker, the negative-tag set
    (permut / shuffle / random / uniform), the ±0.25 verdict
    margin, the feature keys, and the verdict texts are passed
    as comparator_spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        signature_comparator_execute,
    )

    merged = dict(params)
    spec = dict(merged.get("comparator_spec") or {})
    spec.setdefault("candidate_tag", "indus")
    spec.setdefault("candidate_marker", "candidate")
    spec.setdefault("negative_tags", ["permut", "shuffle", "random", "uniform"])
    spec.setdefault("verdict_margin", 0.25)
    spec.setdefault("feature_keys", ["alpha", "gamma_mi", "plateau_norm",
                                     "epistatic_2", "epistatic_3", "h_norm_n3"])
    spec.setdefault("verdict_templates", {
        "language": (
            "Target '{target}' is closer to the language template "
            "({d_lang:.2f}) than to the negative-control template "
            "({d_neg:.2f}). Provisional language-like signature."
        ),
        "negative": (
            "Target '{target}' is closer to the negative-control "
            "template ({d_neg:.2f}) than to the language template "
            "({d_lang:.2f}). Inconsistent with natural-language signature."
        ),
        "ambiguous": (
            "Target '{target}' lies between language and negative "
            "templates (delta={delta:+.2f}). Ambiguous."
        ),
        "no_target": "No target_label supplied; ranking-only output.",
    })
    merged["comparator_spec"] = spec
    return signature_comparator_execute(inputs, merged)


# ── Path 2.1 — ICITMetadataLoader ───────────────────────────────────────


def _icit_metadata_loader(inputs: dict, params: dict) -> dict:
    """Load reports/icit_extracted_corpus.json and emit sequences plus
    parallel metadata arrays.
    """
    repo_root = Path(__file__).resolve().parents[2]
    candidates = [
        repo_root / "reports" / "icit_extracted_corpus.json",
        repo_root / "reports" / "icit_corpus_flat.txt",
    ]
    seqs: list[list[str]] = []
    metadata: list[dict] = []
    used: str = ""
    for p in candidates:
        if not p.exists():
            continue
        if p.suffix == ".json":
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            inscs = d.get("inscriptions") or []
            for ins in inscs:
                seq = list(ins.get("sequence") or [])
                if not seq:
                    continue
                seqs.append(seq)
                metadata.append({
                    "icit_id": ins.get("icit_id"),
                    "site": ins.get("site") or "?",
                    "type": ins.get("type") or "?",
                    "complete": ins.get("complete") or "?",
                    "direction": ins.get("direction") or "?",
                    "length": len(seq),
                })
            used = str(p)
            break
    return {
        "sequences": seqs,
        "metadata": metadata,
        "n_sequences": len(seqs),
        "n_tokens": sum(len(s) for s in seqs),
        "source": used,
    }


# ── Path 2.2 — SignContextAssociation ───────────────────────────────────


def _sign_context_association(inputs: dict, params: dict) -> dict:
    """Compute PMI between signs and a chosen metadata field, with a
    permutation null.

    Score per (sign, context_value) is:
        pmi = log( P(sign, ctx) / (P(sign) * P(ctx)) )

    A permutation null is built by shuffling the metadata-context array
    n_perm times and recomputing each (sign, ctx) PMI. We report observed
    PMI minus the mean of the null and a z-score.

    Spec 087 S3 (family F9): the mechanism is the generic
    TokenContextAssociation engine (glossa_lab.generic_primitives);
    this node is its Phase-14 parameterisation — the z >= 2.0
    significance cut, the >= 5 strong-verdict minimum, the
    length_bin bucketing (short <= 2 / medium <= 5 / long, from
    the length field), and the verdict texts are passed as
    association_spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        token_context_association_execute,
    )

    merged = dict(params)
    spec = dict(merged.get("association_spec") or {})
    spec.setdefault("significance_cut", 2.0)
    spec.setdefault("strong_min", 5)
    spec.setdefault("binned_field", "length_bin")
    spec.setdefault("bin_source_field", "length")
    spec.setdefault("bins", [[2, "short"], [5, "medium"]])
    spec.setdefault("default_bin", "long")
    spec.setdefault("verdict_templates", {
        "strong": (
            "Field '{field}': {n} (sign, ctx) pairs at z >= {cut:g}σ above "
            "permutation null. External grounding present."
        ),
        "weak": (
            "Field '{field}': only {n} pair(s) at z >= {cut:g}σ. Weak grounding."
        ),
        "none": (
            "Field '{field}': zero (sign, ctx) pairs survive a permutation null "
            "at z >= {cut:g}σ. No external grounding signal detected."
        ),
    })
    merged["association_spec"] = spec
    return token_context_association_execute(inputs, merged)


# ── Path 2.3 — DerivedAnchorSet ─────────────────────────────────────────


def _derived_anchor_set(inputs: dict, params: dict) -> dict:
    """Take the top-K significant sign-context associations and emit a
    sign->value anchor dict whose values are the context labels.

    This is the empirically-grounded replacement for
    IconographicAnchorPin's hardcoded defaults. Each anchor is a sign whose
    distribution is significantly skewed toward a single archaeological
    context (e.g. site, artifact type) above a permutation baseline.

    Spec 087 S3 (family F8): the mechanism is the generic
    AssociationAnchorDeriver engine (glossa_lab.generic_primitives);
    this node is its Phase-14 parameterisation — the "ctx:" anchor-id
    convention is passed as the anchor_prefix param. (The context
    label is treated as the "value" the anchor binds the sign to;
    downstream it is just a string the SA initial mapping is seeded
    with — what matters is that it came from real data.)
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        association_anchor_deriver_execute,
    )

    merged = dict(params)
    merged.setdefault("anchor_prefix", "ctx:")
    return association_anchor_deriver_execute(inputs, merged)


# ── Epistatic 1 — EpistaticInteractionDetector ──────────────────────────


def _epistatic_interaction_detector(inputs: dict, params: dict) -> dict:
    """Detect higher-order sign-pair / triple interactions beyond what
    independence (or the bigram baseline) predicts.

    For each frequent bigram (a, b):
      pmi_2 = log P(a,b) / (P(a) P(b))
      surplus_2 = pmi_2 (already by construction surplus over independence)

    For each frequent trigram (a, b, c):
      surplus_3 = log P(a,b,c) - log[ P(a,b) * P(c) ]   (3rd-order chain rule)
      i.e. interaction information beyond pairwise.

    Surplus is reported as nats. Sorted top-K bigrams and trigrams.

    Spec 087 S3 (family F9): the mechanism is the generic
    InteractionSurplusProfile engine (glossa_lab.generic_primitives);
    this node is its Phase-14 parameterisation — the 2.0-nat
    PMI-surplus significance cut is passed as profile_spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        interaction_surplus_profile_execute,
    )

    merged = dict(params)
    spec = dict(merged.get("profile_spec") or {})
    spec.setdefault("significance_cut", 2.0)
    merged["profile_spec"] = spec
    return interaction_surplus_profile_execute(inputs, merged)


# ── Epistatic 2 — EpistaticOrderProfile (HED) ───────────────────────────


def _epistatic_order_profile(inputs: dict, params: dict) -> dict:
    """Hierarchical Epistasis Decomposition of corpus information content.

    Decomposes total per-symbol information into successive orders:

        I_1 = H_max - H(1)              # 1st-order (unigram skew)
        I_2 = H(1) + H(1) - H(2)        # = mutual info at lag-1
        I_3 = additional info at order 3 over the bigram-Markov baseline
        I_k = additional info at order k

    where H(n) is the per-symbol n-block entropy. Reports the fraction of
    total structure captured at each order (the language-vs-non-language
    fingerprint).

    Spec 087 S3 (family F9): the mechanism is the generic
    OrderInformationProfile engine (glossa_lab.generic_primitives);
    this node is its Phase-14 parameterisation — the regime rule
    table (f2/f1 >= 0.10 and f3/f2 >= 0.05 -> language_like;
    f2/f1 < 0.05 -> non_linguistic; otherwise ambiguous) is
    passed as profile_spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        order_information_profile_execute,
    )

    merged = dict(params)
    spec = dict(merged.get("profile_spec") or {})
    spec.setdefault("regime_rules", [
        {"regime": "language_like",
         "conditions": [["f2_over_f1", ">=", 0.10], ["f3_over_f2", ">=", 0.05]]},
        {"regime": "non_linguistic",
         "conditions": [["f2_over_f1", "<", 0.05]]},
    ])
    spec.setdefault("fallback_regime", "ambiguous")
    merged["profile_spec"] = spec
    return order_information_profile_execute(inputs, merged)


# ── Epistatic 3 — EpistaticAnchorRanker ─────────────────────────────────


def _epistatic_anchor_ranker(inputs: dict, params: dict) -> dict:
    """Rank candidate anchor signs by their *epistatic centrality*.

    For each sign s we compute:
        centrality(s) = sum over partners p of |PMI(s, p)| weighted by count.

    This is the information-theoretic version of "which sign's value, when
    fixed, most-constrains the values of the most-other signs?" — exactly
    the criterion that should drive Berg-Kirkpatrick / SA anchor placement.

    Replaces the frequency-based AnchorGenerator default.

    Spec 087 S3 (family F8): the mechanism is the generic
    PMICentralityRanker engine (glossa_lab.generic_primitives) —
    the triage found no domain constants in this node at all;
    this wrapper is the delegation point that keeps the
    registered id and its parameter surface.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        pmi_centrality_ranker_execute,
    )

    return pmi_centrality_ranker_execute(inputs, params)


# ── Constraint projection — removed, with pointer ────
# The CASHypothesisProjector node left the palette with the
# CPSC engine in May 2026; its stub function is removed here
# under Spec 086 T406 (Spec 085 C085-15, carried in). The
# capability's successor is the glossa-settle-1 settling
# engine — backend/glossa_lab/settling.py, operated via
# tools/ledger/run_settling.py — which settles sign-value
# assignment sets against the anchor register and the
# ledger. No Experiment Builder node projects constraints
# in v1; LanguageDetectorVerdict's optional cas_projection
# input has no in-tree producer and is inert unconnected.


# ── Integrative — LanguageDetectorVerdict ───────────────────────────────


def _language_detector_verdict(inputs: dict, params: dict) -> dict:
    """Combine the structural-signature, epistatic-order, and (optionally)
    CPSC-projection outputs into a single verdict on whether the corpus is
    a real natural-language writing system.

    Evidence-for buckets (each contributes +1 to the score):
      - Zipf-Mandelbrot R^2 >= 0.85 and 0.85 <= alpha <= 1.30
      - Block-entropy plateau detected (h(n) flattens at n>=3)
      - MI decay regime == "power_law"
      - HED regime == "language_like"
      - HED 2nd-order fraction >= 0.10
      - HED 3rd-order fraction >= 0.05
      - Permutation null distinguishes corpus from shuffled (delta >= 0.5)
      - CAS projection success == True OR max_violation <= small threshold

    Evidence-against (each contributes -1):
      - Zipf alpha < 0.5 OR R^2 < 0.5
      - MI decay regime == "flat"
      - HED regime == "non_linguistic"
      - HED 2nd-order fraction < 0.05
      - CAS projection max_violation > large threshold

    Output: {is_language: bool, confidence: 0..1, score, evidence_for,
             evidence_against, verdict_text}.

    Spec 087 S3 (family F9): the mechanism is the generic
    EvidenceRuleAggregator engine (glossa_lab.generic_primitives);
    this node is its Phase-14 parameterisation — the evidence
    rule table (the Zipf range pair, the plateau and MI/HED
    regime equalities, the HED fraction checks at 0.10 / 0.05,
    and the CAS success-threshold rule over the cas_violation
    params), the is_language score threshold of 2, and the
    verdict texts are passed as aggregator_spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        evidence_rule_aggregator_execute,
    )

    merged = dict(params)
    spec = dict(merged.get("aggregator_spec") or {})
    spec.setdefault("rules", [
        {"kind": "range_pair", "input": "zipf",
         "field_a": "alpha", "field_b": "r_squared",
         "field_b_fallback": "r2_zipf",
         "a_range": [0.85, 1.30], "b_min": 0.85,
         "a_floor": 0.50, "b_floor": 0.50,
         "for_template": "Zipf alpha={alpha:.2f} R^2={r_squared:.3f} in language range",
         "against_template": "Zipf alpha={alpha:.2f} R^2={r_squared:.3f} outside language range"},
        {"kind": "field_equals", "input": "conditional_entropy",
         "field": "plateau", "default": "no", "equals": "yes", "side": "for",
         "template": "Conditional-entropy plateau at n>=3 (h(n) saturates)"},
        {"kind": "field_equals", "input": "mi_decay",
         "field": "regime", "default": "unknown", "equals": "power_law",
         "side": "for",
         "template": "MI decay = power-law (gamma={gamma_powerlaw:.2f})"},
        {"kind": "field_equals", "input": "mi_decay",
         "field": "regime", "default": "unknown", "equals": "flat",
         "side": "against",
         "template": "MI decay = flat (consistent with unigram-random)"},
        {"kind": "field_equals", "input": "mi_decay",
         "field": "regime", "default": "unknown", "equals": "exponential",
         "side": "against",
         "template": "MI decay = exponential (Markov-1, non-linguistic)"},
        {"kind": "field_equals", "input": "hed",
         "field": "regime", "default": "unknown", "equals": "language_like",
         "side": "for",
         "template": "HED regime = language-like (2nd/1st={f2:.2f}, 3rd/2nd={f3:.2f})",
         "values": {"f2": "f2_over_f1", "f3": "f3_over_f2"}},
        {"kind": "field_equals", "input": "hed",
         "field": "regime", "default": "unknown", "equals": "non_linguistic",
         "side": "against",
         "template": "HED regime = non-linguistic (2nd/1st={f2:.2f})",
         "values": {"f2": "f2_over_f1"}},
        {"kind": "list_fraction_checks", "input": "hed",
         "list_field": "orders", "value_field": "fraction_of_total",
         "skip_if_input_empty": True,
         "checks": [
             {"index": 1, "op": ">=", "threshold": 0.10, "side": "for",
              "template": "HED 2nd-order fraction = {value:.2f}"},
             {"index": 2, "op": ">=", "threshold": 0.05, "side": "for",
              "template": "HED 3rd-order fraction = {value:.2f}"},
             {"index": 1, "op": "<", "threshold": 0.05, "side": "against",
              "template": "HED 2nd-order fraction = {value:.2f} (<0.05)"},
         ]},
        {"kind": "success_threshold", "input": "cas_projection",
         "skip_if_input_empty": True,
         "success_field": "success", "value_field": "max_violation",
         "value_default": 1e9,
         "low_param": "cas_violation_low", "low_default": 0.1,
         "high_param": "cas_violation_high", "high_default": 1.0,
         "for_template": "CAS projection succeeded (max_violation={value:.3f})",
         "against_template": "CAS projection failed (max_violation={value:.3f})"},
    ])
    spec.setdefault("language_min_score", 2)
    spec.setdefault("confidence_threshold", 0.5)
    spec.setdefault("verdict_templates", {
        "likely_for": (
            "LIKELY LANGUAGE: {n_for} positive signals vs "
            "{n_against} negative; confidence={confidence:.2f}."
        ),
        "likely_against": (
            "LIKELY NOT LANGUAGE: {n_against} negative signals "
            "vs {n_for} positive; confidence={confidence:.2f}."
        ),
        "ambiguous": (
            "AMBIGUOUS: {n_for} positive and "
            "{n_against} negative signals; "
            "confidence={confidence:.2f}. Need richer corpus or stronger "
            "diagnostic to discriminate."
        ),
    })
    merged["aggregator_spec"] = spec
    return evidence_rule_aggregator_execute(inputs, merged)


# ── Helper — DoFExtractor (corpus -> CAS DoF dict) ──────────────────────


def _dof_extractor(inputs: dict, params: dict) -> dict:
    """Read multiple profiler outputs and emit a flat dict of DoF values
    keyed by the names that the language_signature CAS model expects.

    Collects measured corpus metrics. Fields read:
      - block_entropies (BlockEntropyProfile)
      - zipf (ZipfMandelbrotFit)
      - mi_decay (MutualInformationDecay)
      - hed (EpistaticOrderProfile)

    Spec 087 S3 (family F9): the mechanism is the generic
    MetricFieldExtractor engine (glossa_lab.generic_primitives);
    this node is its Phase-14 parameterisation — the fixed CAS
    field-renaming table is passed as the field_map parameter,
    which is the parameter surface this node gains in the
    conversion.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        metric_field_extractor_execute,
    )

    merged = dict(params)
    merged.setdefault("field_map", [
        {"out": "h1_norm", "kind": "list_row_at_n_field",
         "input": "block_entropies", "list_key": "block_entropies",
         "n": 3, "field": "H_norm", "default": 0.0, "coerce": "float"},
        {"out": "h1_nats", "kind": "list_first_field",
         "input": "block_entropies", "list_key": "block_entropies",
         "field": "H_nats", "default": 0.0, "coerce": "float"},
        {"out": "zipf_alpha", "kind": "field",
         "input": "zipf", "field": "alpha", "default": 0.0, "coerce": "float"},
        {"out": "zipf_r2", "kind": "field",
         "input": "zipf", "field": "r_squared", "default": 0.0, "coerce": "float"},
        {"out": "mi_gamma", "kind": "field",
         "input": "mi_decay", "field": "gamma_powerlaw",
         "default": 0.0, "coerce": "float"},
        {"out": "mi_r2_pow", "kind": "field",
         "input": "mi_decay", "field": "r2_powerlaw",
         "default": 0.0, "coerce": "float"},
        {"out": "epistatic_2nd_norm", "kind": "list_index_field",
         "input": "hed", "list_key": "orders",
         "index": 1, "field": "fraction_of_total",
         "default": 0.0, "coerce": "float"},
        {"out": "epistatic_3rd_norm", "kind": "list_index_field",
         "input": "hed", "list_key": "orders",
         "index": 2, "field": "fraction_of_total",
         "default": 0.0, "coerce": "float"},
    ])
    return metric_field_extractor_execute(inputs, merged)


# ── Atomic node defs for registration ───────────────────────────────────


def _phase14_node_defs() -> list[Any]:
    """Return AtomicNodeDef instances for Phase-14."""
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "BlockEntropyProfile", "Block Entropy Profile (Phase-14)",
            "Phase-14 / Structural",
            "Compute H(n) for n=1..max_n on the input sequences. Plain MLE "
            "estimator. Output is the language-vs-non-language fingerprint "
            "(Rao 2009).",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "alphabet_size", "type": "number"},
                {"name": "n_tokens", "type": "number"},
                {"name": "block_entropies", "type": "json"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "max_n": {"type": "integer", "default": 6, "minimum": 2},
                    "label": {"type": "string", "default": "unknown"},
                },
            },
            fn=_block_entropy_profile,
        ),
        AtomicNodeDef(
            "ConditionalEntropyProfile", "Conditional Entropy Profile (Phase-14)",
            "Phase-14 / Structural",
            "h(n) = H(n) - H(n-1). A natural language plateaus at finite n; "
            "non-language is flat or rapidly decaying.",
            inputs=[{"name": "block_entropies", "type": "json", "required": True}],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "conditional_entropies", "type": "json"},
                {"name": "plateau", "type": "text"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_conditional_entropy_profile,
        ),
        AtomicNodeDef(
            "ZipfMandelbrotFit", "Zipf-Mandelbrot Fit (Phase-14)",
            "Phase-14 / Structural",
            "Fit f(r) = C / (r + beta)^alpha via 2D grid search. Natural "
            "language: alpha approx 1, finite beta. Random: alpha approx 0.",
            inputs=[
                {"name": "freq_map", "type": "freq_map", "required": False},
                {"name": "sequences", "type": "sequences", "required": False},
            ],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "alpha", "type": "number"},
                {"name": "beta", "type": "number"},
                {"name": "r_squared", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "label": {"type": "string", "default": "unknown"},
                },
            },
            fn=_zipf_mandelbrot_fit,
        ),
        AtomicNodeDef(
            "MutualInformationDecay", "Mutual Information Decay (Phase-14)",
            "Phase-14 / Structural",
            "I(X_t; X_{t+k}) for k=1..max_k. Power-law decay = natural "
            "language; exponential decay = Markov-1; flat = unigram-random.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "decay", "type": "json"},
                {"name": "regime", "type": "text"},
                {"name": "gamma_powerlaw", "type": "number"},
                {"name": "lambda_exponential", "type": "number"},
                {"name": "r2_powerlaw", "type": "number"},
                {"name": "r2_exponential", "type": "number"},
                {"name": "h1_nats", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "max_k": {"type": "integer", "default": 8, "minimum": 2},
                    "label": {"type": "string", "default": "unknown"},
                },
            },
            fn=_mutual_information_decay,
        ),
        AtomicNodeDef(
            "ReferenceCorpusLoader", "Reference Corpus Loader (Phase-14)",
            "Phase-14 / Structural",
            "Emit raw sequences for any supported reference language. Mirrors "
            "BuiltinLM's language list. Used for Path-1 cross-corpus comparison.",
            inputs=[],
            outputs=[
                {"name": "sequences", "type": "sequences"},
                {"name": "language", "type": "text"},
                {"name": "label", "type": "text"},
                {"name": "n_sequences", "type": "number"},
                {"name": "n_tokens", "type": "number"},
                {"name": "distinct_symbols", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "language": {"type": "string", "default": "linear_b"},
                    "label": {"type": "string", "default": "linear_b"},
                },
            },
            fn=_reference_corpus_loader,
        ),
        AtomicNodeDef(
            "LanguageSignatureComparator", "Language Signature Comparator (Phase-14)",
            "Phase-14 / Structural",
            "Compare 4-6 corpora's structural signatures and rank a target "
            "by similarity to the natural-language reference cluster vs the "
            "negative-control template.",
            inputs=[
                {"name": "a", "type": "json", "required": False},
                {"name": "b", "type": "json", "required": False},
                {"name": "c", "type": "json", "required": False},
                {"name": "d", "type": "json", "required": False},
                {"name": "e", "type": "json", "required": False},
                {"name": "f", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "ranked", "type": "json"},
                {"name": "language_template", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "target_label": {"type": "string", "default": ""},
                },
            },
            fn=_language_signature_comparator,
        ),
        AtomicNodeDef(
            "ICITMetadataLoader", "ICIT Metadata Loader (Phase-14)",
            "Phase-14 / Grounding",
            "Load reports/icit_extracted_corpus.json with per-inscription "
            "site / type / direction / completeness metadata.",
            inputs=[],
            outputs=[
                {"name": "sequences", "type": "sequences"},
                {"name": "metadata", "type": "json"},
                {"name": "n_sequences", "type": "number"},
                {"name": "n_tokens", "type": "number"},
                {"name": "source", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_icit_metadata_loader,
        ),
        AtomicNodeDef(
            "SignContextAssociation", "Sign-Context Association (Phase-14)",
            "Phase-14 / Grounding",
            "PMI between sign and metadata field (site, type, direction, "
            "length_bin) with permutation null. Reports z-score per pair.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
                {"name": "metadata", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "associations", "type": "json"},
                {"name": "n_significant", "type": "number"},
                {"name": "n_total_pairs", "type": "number"},
                {"name": "field", "type": "text"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "field": {"type": "string", "default": "type",
                              "description": "metadata field: site|type|direction|length_bin"},
                    "n_perm": {"type": "integer", "default": 8, "minimum": 2},
                    "seed": {"type": "integer", "default": 11},
                    "min_count": {"type": "integer", "default": 5, "minimum": 1},
                    "top_k": {"type": "integer", "default": 30, "minimum": 1},
                },
            },
            fn=_sign_context_association,
        ),
        AtomicNodeDef(
            "DerivedAnchorSet", "Derived Anchor Set (Phase-14)",
            "Phase-14 / Grounding",
            "Empirically-grounded sign->context anchor dict from "
            "SignContextAssociation. Replacement for hardcoded "
            "IconographicAnchorPin defaults.",
            inputs=[{"name": "associations", "type": "json", "required": True}],
            outputs=[
                {"name": "anchors", "type": "json"},
                {"name": "n_anchors", "type": "number"},
                {"name": "anchor_table", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_z": {"type": "number", "default": 2.0},
                    "max_anchors": {"type": "integer", "default": 25, "minimum": 1},
                },
            },
            fn=_derived_anchor_set,
        ),
        AtomicNodeDef(
            "EpistaticInteractionDetector", "Epistatic Interaction Detector (Phase-14)",
            "Phase-14 / Epistatic",
            "Detect 2nd- and 3rd-order interactions beyond independence. "
            "Reports top-K bigrams (PMI) and trigrams (interaction information).",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "bigrams", "type": "json"},
                {"name": "trigrams", "type": "json"},
                {"name": "n_significant_bigrams", "type": "number"},
                {"name": "n_significant_trigrams", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_count_2": {"type": "integer", "default": 5, "minimum": 2},
                    "min_count_3": {"type": "integer", "default": 3, "minimum": 2},
                    "top_k": {"type": "integer", "default": 25, "minimum": 5},
                    "label": {"type": "string", "default": "unknown"},
                },
            },
            fn=_epistatic_interaction_detector,
        ),
        AtomicNodeDef(
            "EpistaticOrderProfile", "Epistatic Order Profile (HED) (Phase-14)",
            "Phase-14 / Epistatic",
            "Hierarchical Epistasis Decomposition. Reports the fraction of "
            "corpus information at each interaction order. Language has a "
            "characteristic order-by-order signature.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "orders", "type": "json"},
                {"name": "regime", "type": "text"},
                {"name": "f2_over_f1", "type": "number"},
                {"name": "f3_over_f2", "type": "number"},
                {"name": "per_symbol_entropy", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "max_order": {"type": "integer", "default": 4, "minimum": 2},
                    "label": {"type": "string", "default": "unknown"},
                },
            },
            fn=_epistatic_order_profile,
        ),
        AtomicNodeDef(
            "EpistaticAnchorRanker", "Epistatic Anchor Ranker (Phase-14)",
            "Phase-14 / Epistatic",
            "Rank candidate anchor signs by epistatic centrality "
            "(sum |PMI| weighted by count over all bigram partners). "
            "Information-theoretic replacement for frequency-based anchor "
            "selection.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "ranking", "type": "json"},
                {"name": "n_signs_ranked", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "top_k": {"type": "integer", "default": 10, "minimum": 1},
                    "min_count": {"type": "integer", "default": 5, "minimum": 1},
                },
            },
            fn=_epistatic_anchor_ranker,
        ),
        AtomicNodeDef(
            "DoFExtractor", "DoF Extractor (Phase-14)",
            "Phase-14 / Structural",
            "Reads BlockEntropyProfile / Zipf / MI / HED outputs and emits "
            "a flat measurement dict.",
            inputs=[
                {"name": "block_entropies", "type": "json", "required": False},
                {"name": "zipf", "type": "json", "required": False},
                {"name": "mi_decay", "type": "json", "required": False},
                {"name": "hed", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "dof_values", "type": "json"},
                {"name": "n_dofs", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_dof_extractor,
        ),
        AtomicNodeDef(
            "LanguageDetectorVerdict", "Language Detector Verdict (Phase-14)",
            "Phase-14 / Integrative",
            "Combine block-entropy plateau, Zipf-Mandelbrot, MI decay, HED "
            "into a single yes/no/maybe verdict on whether the corpus is a real "
            "natural-language writing system. Answers: 'is this corpus a language?'",
            inputs=[
                {"name": "zipf", "type": "json", "required": False},
                {"name": "conditional_entropy", "type": "json", "required": False},
                {"name": "mi_decay", "type": "json", "required": False},
                {"name": "hed", "type": "json", "required": False},
                {"name": "cas_projection", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "is_language", "type": "any"},
                {"name": "confidence", "type": "number"},
                {"name": "score", "type": "number"},
                {"name": "evidence_for", "type": "json"},
                {"name": "evidence_against", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "cas_violation_low": {"type": "number", "default": 0.1},
                    "cas_violation_high": {"type": "number", "default": 1.0},
                },
            },
            fn=_language_detector_verdict,
        ),
    ]


__all__ = [
    "_block_entropy_profile",
    "_conditional_entropy_profile",
    "_zipf_mandelbrot_fit",
    "_mutual_information_decay",
    "_reference_corpus_loader",
    "_language_signature_comparator",
    "_icit_metadata_loader",
    "_sign_context_association",
    "_derived_anchor_set",
    "_epistatic_interaction_detector",
    "_epistatic_order_profile",
    "_epistatic_anchor_ranker",
    "_dof_extractor",
    "_language_detector_verdict",
    "_phase14_node_defs",
]
