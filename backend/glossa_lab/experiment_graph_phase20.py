"""Phase-20 atomic node implementations.

Phase-20 follow-ups to the four Phase-19 candidate experiments:

  Experiment 1 — Length-stratified spectral analysis
      LengthStratifier + BinSpectralFingerprint test whether M77's anomalous
      spectral gap (Phase-19 finding 1: ~50x smaller than every natural-
      language reference) is dominated by short pseudo-inscriptions, by
      computing the bigram-transition spectral gap per length bin.

  Experiment 2 — Archaeology of the 16-sign distributional cluster
      AllographDetector replicates the Daggumati-style clustering used in
      Phase-19. ClusterArchaeology then computes per-site distribution of
      that cluster (using site_code from reports/mahadevan_texts_decoded.json)
      and a chi-squared test for site-cluster independence.

  Experiment 3 — Ferrara 2006 OCR for empirical CM anchoring
      PDFTextExtractor uses PyMuPDF (fitz) to extract text per page from
      the 478MB Ferrara 2006 PhD PDF; CMCatalogParser scans the extracted
      text for sign-sequence patterns + frequency, producing best-effort
      empirical anchors for cypro_minoan_morphology.yaml.

  Experiment 4 — Fuls-style positional sign-function classifier
      FulsPositionalClassifier assigns each M77 sign to one of {INITIAL,
      MEDIAL, TERMINAL, NUMERICAL, MIXED} based on position rates +
      same-sign repetition rate (the numerical-strokes artifact identified
      in Phase-19 finding 4).

  Phase20Verdict combines the above into a yes/no/maybe per Phase-19
  prediction.

References
----------
- Daggumati, S. & Revesz, P. (2021). "Allograph detection methods..." -- the
  distributional clustering on bigram-context profile vectors used in
  Phase-19 + 20 sign clustering.
- Fuls, A. (2013). NWSP positional method (initial/medial/terminal rates
  + Z-scores; the basis for our 5-way logo-vs-syllabic classifier).
- Ferrara, S. (2006). "Cypro-Minoan: an Aegean writing system."
  PhD thesis, UCL.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# ── Helpers ────────────────────────────────────────────────────────────


def _flatten(seqs: list[list[str]]) -> list[str]:
    return [s for seq in seqs for s in seq]


def _resolve_repo_root() -> Path:
    # backend/glossa_lab/experiment_graph_phase20.py -> ../../../
    return Path(__file__).resolve().parents[2]


def _resolve_report(name: str) -> Path:
    return _resolve_repo_root() / "reports" / name


# ── Experiment 1: M77 inscription loader (with metadata) ────────────────


def _m77_inscription_loader(inputs: dict, params: dict) -> dict:
    """Load M77 inscriptions with per-inscription metadata.

    Primary source: reports/mahadevan_texts_decoded.json (the upstream
    Mahadevan OCR + rank-correlation glyph mapping), selected by the
    ``source`` parameter's default ("decoded"). The Holdat CSV corpus,
    which contains the same inscriptions with M-prefixed sign IDs and
    site metadata, is used only when it is selected explicitly
    (source="holdat"). There is no automatic substitution: when the
    selected source file is absent, the loader returns the
    absent-corpus error. (Until the Spec 087 S3 fallback retirement,
    owner-approved 2026-11-03, an absent decoded report silently fell
    back to the Holdat CSV — which corpus a consumer received depended
    on which files happened to exist.)

    Outputs both ``sequences`` (list[list[str]]) -- compatible with every
    other Phase-14/15 atomic node -- and ``inscriptions`` (list[dict])
    keeping the metadata for downstream archaeology / per-inscription
    statistics.

    Spec 087 S3 (family F1): the mechanism is the generic
    JsonCorpusLoader engine (glossa_lab.generic_loaders); this node is
    its M77 parameterisation — the source chain (the decoded report,
    plus the Holdat CSV with its column mapping as an explicit-only
    source), the field map, and the historical defaults live in the
    spec below, not in code.
    """
    from glossa_lab.generic_loaders import json_corpus_loader_execute  # noqa: PLC0415

    decoded_path = _resolve_report("mahadevan_texts_decoded.json")
    holdat_path = (
        _resolve_repo_root()
        / "corpora/downloads/external_repos/holdatllc_indus"
        / "indus_corpus 2.csv"
    )
    spec = {
        "sources": [
            {
                "kind": "json",
                "path": str(decoded_path),
                "site_coerce_str": True,
                "name": "decoded",
            },
            {
                "kind": "csv_grouped",
                "path": str(holdat_path),
                "group_key": "cisi_number",
                "order_key": "position",
                "value_key": "letters",
                "site_field": "site",
                "name": "holdat",
                "explicit_only": True,
            },
        ],
        "source_select_param": "source",
        "records_key": "inscriptions",
        "field_map": {
            "id": "id",
            "site": "site_code",
            "sequence": "sequence",
            "raw": "raw",
        },
        "projection": "sequence_corpus",
        "parse_error": "raise",
        "behavior_defaults": {
            "use_raw": False,
            "min_length": 1,
            "max_length": 0,
            "label": "indus_m77",
        },
        "absent_result": {
            "error": (
                "M77 corpus not available: neither {source_name} in reports/ "
                "nor Holdat CSV at {fallback_path} found. "
                "Run backend/scripts/decode_inscription_texts.py to regenerate."
            )
        },
    }
    merged = dict(params)
    merged["corpus_spec"] = spec
    return json_corpus_loader_execute(inputs, merged)


# ── Experiment 1: Length stratifier ─────────────────────────────────────


def _length_stratifier(inputs: dict, params: dict) -> dict:
    """Stratify sequences into length-defined bins.

    ``bins`` parameter is a list of [lo, hi] pairs (inclusive). Each
    sequence is assigned to the first bin whose [lo, hi] contains its
    length. Output ``stratifications`` is a dict bin_label -> sequences
    with bin_labels of the form ``"L{lo}-{hi}"``.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    bins = params.get("bins") or [[1, 2], [3, 4], [5, 6], [7, 9999]]
    if not isinstance(bins, list):
        return {"error": "bins must be a list of [lo, hi] pairs"}

    stratifications: dict[str, list[list[str]]] = {}
    summary: list[dict] = []
    for pair in bins:
        try:
            lo, hi = int(pair[0]), int(pair[1])
        except Exception:  # noqa: BLE001
            continue
        label = f"L{lo}-{hi}" if hi < 1000 else f"L{lo}+"
        stratifications[label] = []

    for seq in sequences:
        L = len(seq)
        for pair in bins:
            try:
                lo, hi = int(pair[0]), int(pair[1])
            except Exception:  # noqa: BLE001
                continue
            label = f"L{lo}-{hi}" if hi < 1000 else f"L{lo}+"
            if lo <= L <= hi:
                stratifications[label].append(seq)
                break

    for label, seqs in stratifications.items():
        flat = _flatten(seqs)
        summary.append({
            "bin": label,
            "n_seqs": len(seqs),
            "n_tokens": len(flat),
            "n_distinct_signs": len(set(flat)),
            "mean_length": (sum(len(s) for s in seqs) / max(1, len(seqs))) if seqs else 0.0,
        })

    return {
        "stratifications": stratifications,
        "summary": summary,
        "n_bins": len(stratifications),
        "total_sequences": sum(len(v) for v in stratifications.values()),
    }


# ── Experiment 1: Per-bin spectral fingerprint ──────────────────────────


def _bigram_transition_matrix(seqs: list[list[str]]) -> tuple[list[str], list[list[float]]]:
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for s in seqs:
        for i in range(len(s) - 1):
            counts[s[i]][s[i + 1]] += 1
    signs = sorted(counts.keys() | {b for row in counts.values() for b in row})
    idx = {s: i for i, s in enumerate(signs)}
    n = len(signs)
    P = [[0.0] * n for _ in range(n)]
    for a, row in counts.items():
        total = sum(row.values())
        if total <= 0:
            continue
        i = idx[a]
        for b, c in row.items():
            P[i][idx[b]] = c / total
    return signs, P


def _spectral_gap(P: list[list[float]]) -> tuple[float, list[float]]:
    if not P:
        return 0.0, []
    try:
        import numpy as np  # noqa: PLC0415
    except Exception:  # noqa: BLE001
        return 0.0, []
    a = np.array(P, dtype=float)
    if a.size == 0:
        return 0.0, []
    try:
        eigvals = np.linalg.eigvals(a)
    except Exception:  # noqa: BLE001
        return 0.0, []
    mags = sorted([abs(complex(v)) for v in eigvals], reverse=True)
    gap = max(0.0, 1.0 - mags[1]) if len(mags) >= 2 else 0.0
    return float(round(gap, 6)), [float(round(m, 6)) for m in mags[:8]]


def _bin_spectral_fingerprint(inputs: dict, params: dict) -> dict:
    """Compute spectral gap + top eigenvalues per length bin.

    Phase-19 found M77 has spectral_gap = 0.010 (mapped) / 0.0096 (raw),
    ~50x smaller than every natural-language reference (0.46-0.61). This
    node tests whether the gap rises with inscription length (i.e. the
    anomaly is dominated by short pseudo-inscriptions).
    """
    stratifications = inputs.get("stratifications") or {}
    if not isinstance(stratifications, dict) or not stratifications:
        return {"error": "stratifications input must be a non-empty dict"}

    per_bin: dict[str, dict] = {}
    for label, seqs in stratifications.items():
        flat = _flatten(seqs)
        if len(flat) < 2:
            per_bin[label] = {
                "n_seqs": len(seqs), "n_tokens": len(flat),
                "n_signs": len(set(flat)),
                "spectral_gap": None, "top_eigenvalues": [],
                "verdict": "insufficient data",
            }
            continue
        signs, P = _bigram_transition_matrix(seqs)
        gap, top = _spectral_gap(P)
        per_bin[label] = {
            "n_seqs": len(seqs), "n_tokens": len(flat),
            "n_signs": len(signs),
            "spectral_gap": gap,
            "top_eigenvalues": top,
            "verdict": (
                "natural-language regime" if gap >= 0.40
                else "intermediate" if gap >= 0.10
                else "highly deterministic / anomalous"
            ),
        }

    # Overall verdict
    nontrivial = [(b, d["spectral_gap"]) for b, d in per_bin.items()
                  if d.get("spectral_gap") is not None]
    if nontrivial:
        # Bin labels are produced by LengthStratifier as e.g. "L1-2", "L7+".
        # Sort by numeric prefix so we always quote the SHORTEST and LONGEST
        # bin (not just the gap-min/max ones, which collapse to a single label
        # when all gaps are tied at 0.0).
        def _bin_lo(label: str) -> int:
            try:
                core = label.lstrip("L")
                lo = core.split("-")[0].rstrip("+")
                return int(lo)
            except Exception:  # noqa: BLE001
                return 0
        ordered = sorted(nontrivial, key=lambda kv: _bin_lo(kv[0]))
        short_bin, short_gap = ordered[0]
        long_bin, long_gap = ordered[-1]
        max_gap = max(g for _, g in nontrivial)
        min_gap = min(g for _, g in nontrivial)
        rises = max_gap > 5 * max(1e-6, min_gap)
        verdict = (
            f"PREDICTION 1 {'CONFIRMED' if rises else 'NOT CONFIRMED'}: "
            f"spectral gap goes from {short_gap:.4f} ({short_bin}) to "
            f"{long_gap:.4f} ({long_bin}) across length bins "
            f"(min={min_gap:.4f}, max={max_gap:.4f}). "
            f"{'Long-tail bins are more language-like.' if rises else 'No length effect.'}"
        )
    else:
        verdict = "insufficient data across bins"

    return {
        "per_bin": per_bin,
        "verdict": verdict,
        "n_bins_with_data": len(nontrivial),
    }


# ── Experiment 2: Allograph detector (Daggumati-style) ──────────────────


def _allograph_detector(inputs: dict, params: dict) -> dict:
    """Distributional clustering of signs.

    For each sign with frequency >= min_count, build a bigram-context
    feature vector (count of right-context partners). Compute pairwise
    cosine similarity; greedy-merge signs whose similarity >= cos_threshold
    AND whose position-distribution L1 distance <= pos_threshold.

    Outputs the cluster list (sets of sign tokens) and a sign->cluster
    map. Returns the largest cluster's members as ``biggest_cluster``.
    Reproduces the Phase-19 16-sign finding when run on M77-mapped.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    min_count = int(params.get("min_count", 5))
    cos_threshold = float(params.get("cos_threshold", 0.55))
    pos_threshold = float(params.get("pos_threshold", 0.50))

    freq: Counter[str] = Counter()
    pos_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"I": 0, "M": 0, "T": 0}
    )
    bi_right: dict[str, Counter[str]] = defaultdict(Counter)
    for seq in sequences:
        n = len(seq)
        for i, s in enumerate(seq):
            freq[s] += 1
            if n == 1:
                pos_counts[s]["I"] += 1
                pos_counts[s]["T"] += 1
            elif i == 0:
                pos_counts[s]["I"] += 1
            elif i == n - 1:
                pos_counts[s]["T"] += 1
            else:
                pos_counts[s]["M"] += 1
            if i + 1 < n:
                bi_right[s][seq[i + 1]] += 1

    eligible = [s for s, c in freq.items() if c >= min_count]
    eligible.sort()
    n_eligible = len(eligible)

    # Build feature vectors as dict[partner -> share]
    vecs: dict[str, dict[str, float]] = {}
    pos_vecs: dict[str, tuple[float, float, float]] = {}
    for s in eligible:
        total = sum(bi_right[s].values())
        vecs[s] = {p: c / total for p, c in bi_right[s].items()} if total else {}
        pc = pos_counts[s]
        ptot = pc["I"] + pc["M"] + pc["T"]
        if ptot > 0:
            pos_vecs[s] = (pc["I"] / ptot, pc["M"] / ptot, pc["T"] / ptot)
        else:
            pos_vecs[s] = (0.0, 0.0, 0.0)

    def _cos(a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        dot = sum(a[k] * b[k] for k in common)
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na > 0 and nb > 0 else 0.0

    def _pos_l1(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

    # Greedy clustering
    parent: dict[str, str] = {s: s for s in eligible}

    def _find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def _union(x: str, y: str) -> None:
        rx, ry = _find(x), _find(y)
        if rx != ry:
            parent[rx] = ry

    for i, a in enumerate(eligible):
        for b in eligible[i + 1:]:
            if _cos(vecs[a], vecs[b]) >= cos_threshold and _pos_l1(pos_vecs[a], pos_vecs[b]) <= pos_threshold:
                _union(a, b)

    grouping: dict[str, list[str]] = defaultdict(list)
    for s in eligible:
        grouping[_find(s)].append(s)
    multi = sorted(
        (sorted(members) for members in grouping.values() if len(members) >= 2),
        key=len, reverse=True,
    )
    sign_to_cluster: dict[str, int] = {}
    for ci, members in enumerate(multi):
        for s in members:
            sign_to_cluster[s] = ci

    biggest = multi[0] if multi else []
    return {
        "n_signs_total": len(freq),
        "n_signs_eligible": n_eligible,
        "n_clusters": len(multi),
        "n_signs_in_multi_clusters": sum(len(c) for c in multi),
        "clusters": [{"members": m, "size": len(m)} for m in multi],
        "biggest_cluster": {"members": biggest, "size": len(biggest)},
        "sign_to_cluster": sign_to_cluster,
        "params": {
            "min_count": min_count,
            "cos_threshold": cos_threshold,
            "pos_threshold": pos_threshold,
        },
    }


# ── Experiment 2: Cluster archaeology ───────────────────────────────────


def _cluster_archaeology(inputs: dict, params: dict) -> dict:
    """Per-cluster archaeological signature.

    Inputs:
      inscriptions      list[dict]  -- M77InscriptionLoader output
      sign_to_cluster   dict[sign->cluster_id]
      target_cluster    int (default 0 = biggest)

    Output: per-cluster site distribution, length distribution, chi-squared
    test of site-vs-cluster independence on the cluster's hosting
    inscriptions, plus a verdict on whether the cluster's archaeological
    distribution differs from the corpus baseline.

    Spec 087 S3 (family F3): the mechanism is the generic
    ClusterContingencyProfile engine (glossa_lab.generic_primitives);
    this node is its Phase-20 parameterisation — the site strata
    rule (site_code, 2-character prefix + "0000"), the significance
    rule (chi2 > 3.84 * dof, ~p<0.05), the 25-row site table, and
    the PREDICTION 2 verdict text live in the params below, not
    in code.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        cluster_contingency_profile_execute,
    )

    merged = dict(params)
    merged.setdefault("strata_field", "site_code")
    merged.setdefault("prefix_len", 2)
    merged.setdefault("prefix_suffix", "0000")
    merged.setdefault("critical_per_dof", 3.84)
    merged.setdefault("site_limit", 25)
    merged.setdefault(
        "verdict_template",
        "PREDICTION 2 {outcome}: chi2={chi2:.2f} dof={dof}; per-site rate range "
        "{min_rate:.3f}-{max_rate:.3f} (corpus baseline {baseline:.3f}).",
    )
    return cluster_contingency_profile_execute(inputs, merged)


# ── Experiment 3: PDF text extractor ────────────────────────────────────


def _pdf_text_extractor(inputs: dict, params: dict) -> dict:
    """Extract text per page from a PDF using PyMuPDF (fitz)."""
    file_path = (inputs.get("file_path") or
                 inputs.get("text") or inputs.get("value") or
                 params.get("file_path") or "")
    file_path = str(file_path).strip()
    if not file_path:
        return {"error": "no file_path provided"}
    p = Path(file_path)
    if not p.exists():
        return {"error": f"PDF not found: {p}"}

    max_pages = int(params.get("max_pages", 100))
    start_page = int(params.get("start_page", 0))
    try:
        import fitz  # type: ignore  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {"error": f"PyMuPDF not available: {exc}"}

    pages: list[dict] = []
    n_total_pages = 0
    try:
        doc = fitz.open(str(p))
        n_total_pages = doc.page_count
        end_page = min(n_total_pages, start_page + max_pages)
        for i in range(start_page, end_page):
            try:
                txt = doc.load_page(i).get_text("text")
            except Exception as exc:  # noqa: BLE001
                txt = ""
                pages.append({"page_num": i, "text": "", "error": str(exc)})
                continue
            pages.append({"page_num": i, "text": txt})
        doc.close()
    except Exception as exc:  # noqa: BLE001
        return {"error": f"failed to open / read PDF: {exc}"}

    total_chars = sum(len(p_["text"]) for p_ in pages)
    return {
        "file_path": str(p),
        "n_total_pages": n_total_pages,
        "n_pages_extracted": len(pages),
        "start_page": start_page,
        "end_page": start_page + len(pages),
        "total_characters": total_chars,
        "pages": pages,
    }


# ── Experiment 3: CM catalog parser ─────────────────────────────────────


def _cm_catalog_parser(inputs: dict, params: dict) -> dict:
    """Best-effort sign-sequence + inscription extraction from Ferrara 2006.

    Heuristics:
      * Inscription IDs match patterns like ``RASH Avv ###``, ``ENKO Atab ###``,
        ``CM ##.###``, or numbered catalog entries ``#0001``, ``#0002`` etc.
      * Sign-sequence lines: contiguous Cypro-Minoan codepoints
        (Unicode block U+12F90..U+12FFF) OR Ferrara's transliteration
        notation ``001-002-003``. We extract both.
      * Per-page sign frequency tallied from any 3-digit sign codes ``\\d{3}``
        on lines that look like sign sequences (digits-and-dashes only).
    """
    pages = inputs.get("pages") or []
    inscription_id_re = re.compile(
        r"\b("
        r"(?:RASH|ENKO|HAZO|UGAR|MARO|TEKE|MILO|HALA|KALA|KOUR)"
        r"\s*[A-Za-z]+\s*\d{1,5}"
        r"|CM\s*\d{1,3}\.\d{1,4}"
        r"|##?\d{2,5}"
        r")",
        re.IGNORECASE,
    )
    sign_seq_re = re.compile(r"\b\d{2,3}(?:-\d{2,3}){1,}\b")
    cm_unicode_re = re.compile(r"[\U00012F90-\U00012FFF]+")

    inscriptions: list[dict] = []
    sign_freq: Counter[str] = Counter()
    cm_unicode_freq: Counter[str] = Counter()
    n_pages_with_signs = 0

    for entry in pages:
        text = entry.get("text") or ""
        if not text:
            continue
        page_signs_found = False

        for m in inscription_id_re.finditer(text):
            inscriptions.append({"page": entry.get("page_num"), "id": m.group(1).strip()})
        for m in sign_seq_re.finditer(text):
            seq = m.group(0).split("-")
            if len(seq) < 2:
                continue
            inscriptions.append({
                "page": entry.get("page_num"), "id": None,
                "sequence_codes": seq, "raw": m.group(0),
            })
            for s in seq:
                sign_freq[s] += 1
            page_signs_found = True
        for m in cm_unicode_re.finditer(text):
            for ch in m.group(0):
                cm_unicode_freq[ch] += 1
            page_signs_found = True

        if page_signs_found:
            n_pages_with_signs += 1

    # Deduplicate exact id-only inscription duplicates per page
    seen_ids: set[tuple[Any, str]] = set()
    deduped: list[dict] = []
    for ins in inscriptions:
        key = (ins.get("page"), ins.get("id") or ins.get("raw"))
        if key in seen_ids:
            continue
        seen_ids.add(key)
        deduped.append(ins)

    n_with_seq = sum(1 for i in deduped if i.get("sequence_codes"))
    cm_unicode_total = sum(cm_unicode_freq.values())
    verdict = (
        f"PREDICTION 3 {'PARTIALLY CONFIRMED' if n_with_seq >= 30 or cm_unicode_total >= 100 else 'NOT CONFIRMED'}: "
        f"recovered {n_with_seq} sign-sequence lines + {cm_unicode_total} CM-block "
        f"unicode glyphs across {n_pages_with_signs} pages with parseable signs. "
    )
    if cm_unicode_total < 50 and n_with_seq < 20:
        verdict += (
            "OCR text is too noisy / un-tagged for direct catalog harvest; "
            "image-based catalog plates would need a separate vision pipeline."
        )
    else:
        verdict += "Sufficient material for an empirical CM YAML refinement."

    return {
        "n_pages_processed": len(pages),
        "n_pages_with_signs": n_pages_with_signs,
        "n_inscriptions_recovered": len(deduped),
        "n_with_sequence": n_with_seq,
        "top_sign_codes": sign_freq.most_common(40),
        "n_cm_unicode_glyphs": cm_unicode_total,
        "top_cm_unicode": cm_unicode_freq.most_common(40),
        "inscriptions_sample": deduped[:80],
        "verdict": verdict,
    }


# ── Experiment 4: Fuls-style positional sign-function classifier ────────


def _fuls_positional_classifier(inputs: dict, params: dict) -> dict:
    """Per-sign 5-way functional classification.

    Position rates (I/M/T) follow Fuls 2013. Same-sign-repetition rate
    (RR) flags Phase-19 numerical-stroke signs (e.g. M77 sign 527 with
    `527 527 527`). The 5 classes:

      * NUMERICAL  -- RR >= numerical_rr (>= 0.20 by default)
      * INITIAL    -- I_rate >= dom_threshold and others < secondary
      * MEDIAL     -- M_rate >= dom_threshold
      * TERMINAL   -- T_rate >= dom_threshold
      * MIXED      -- otherwise

    Spec 087 S3 (family F9): the mechanism is the generic
    PositionalClassClassifier engine (glossa_lab.generic_primitives);
    this node is its Phase-20 parameterisation — the 5-class
    label set, the ordered dominant-position rules (INITIAL,
    then TERMINAL, then MEDIAL), and the PREDICTION 4 verdict
    text are passed as classifier_spec data. Every threshold
    was already a parameter here, so this is the cheapest
    conversion in the stage.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        positional_class_classifier_execute,
    )

    merged = dict(params)
    spec = dict(merged.get("classifier_spec") or {})
    spec.setdefault("class_labels", {
        "numerical": "NUMERICAL", "initial": "INITIAL",
        "medial": "MEDIAL", "terminal": "TERMINAL", "mixed": "MIXED",
    })
    spec.setdefault("position_classes", [
        {"label_key": "initial", "dominant": "I"},
        {"label_key": "terminal", "dominant": "T"},
        {"label_key": "medial", "dominant": "M"},
    ])
    spec.setdefault("verdict_template", (
        "PREDICTION 4: classified {n} signs. Class fractions: {fractions}. "
        "Logographic-like ({INITIAL}+{TERMINAL}) = {n_logo}; "
        "syllabic-like ({MEDIAL}+{MIXED}) = {n_syll}; "
        "{NUMERICAL} = {n_numerical} "
        "(confirms Phase-19 numerical-strokes finding if > 5)."
    ))
    merged["classifier_spec"] = spec
    return positional_class_classifier_execute(inputs, merged)


def _phase20_verdict(inputs: dict, params: dict) -> dict:
    """Combine the four sub-experiment outputs into a single yes/no/maybe
    verdict on each Phase-19 prediction.

    Inputs (any subset; missing inputs map to UNKNOWN for that prediction):
      length_strata        -- BinSpectralFingerprint output (dict OR verdict string)
      cluster_archaeology  -- ClusterArchaeology output (dict OR verdict string)
      ferrara_cm           -- CMCatalogParser output (dict OR verdict string)
      fuls_positional      -- FulsPositionalClassifier output (dict OR verdict string)
      fuls_positional_counts -- optional: counts_by_class dict for the NUMERICAL test.
    """

    def _verdict_text(v: Any) -> str:
        if isinstance(v, dict):
            return str(v.get("verdict") or "")
        if isinstance(v, str):
            return v
        return ""

    a_t = _verdict_text(inputs.get("length_strata"))
    b_t = _verdict_text(inputs.get("cluster_archaeology"))
    c_t = _verdict_text(inputs.get("ferrara_cm"))
    d_t = _verdict_text(inputs.get("fuls_positional"))

    p1 = ("CONFIRMED" if "CONFIRMED" in a_t and "NOT CONFIRMED" not in a_t
          else "NOT CONFIRMED" if "NOT CONFIRMED" in a_t else "UNKNOWN")
    p2 = ("CONFIRMED" if "CONFIRMED" in b_t and "NOT CONFIRMED" not in b_t
          else "NOT CONFIRMED" if "NOT CONFIRMED" in b_t else "UNKNOWN")
    p3 = ("PARTIALLY CONFIRMED" if "PARTIALLY CONFIRMED" in c_t
          else "NOT CONFIRMED" if "NOT CONFIRMED" in c_t else "UNKNOWN")

    counts = inputs.get("fuls_positional_counts")
    if not isinstance(counts, dict):
        if isinstance(inputs.get("fuls_positional"), dict):
            counts = inputs["fuls_positional"].get("counts_by_class") or {}
        else:
            counts = {}
    n_numerical = int(counts.get("NUMERICAL", 0)) if isinstance(counts, dict) else 0
    p4 = ("OBSERVED" if n_numerical > 5 else ("NOT OBSERVED" if d_t or counts else "UNKNOWN"))

    return {
        "prediction_1_length_dominates_spectral_gap": p1,
        "prediction_2_cluster_archaeology_nonrandom": p2,
        "prediction_3_ferrara_cm_extractable": p3,
        "prediction_4_numerical_strokes_confirmed": p4,
        "evidence": {
            "length_strata_verdict": a_t,
            "cluster_archaeology_verdict": b_t,
            "ferrara_cm_verdict": c_t,
            "fuls_positional_verdict": d_t,
            "fuls_numerical_count": n_numerical,
        },
        "summary": (
            f"Phase-20: P1={p1} | P2={p2} | P3={p3} | P4={p4}"
        ),
    }


# ── Atomic node defs for registration ───────────────────────────────────


def _phase20_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "M77InscriptionLoader", "M77 Inscription Loader (Phase-20)",
            "Phase-20 / Sources",
            "Load Mahadevan 1977 inscriptions from "
            "reports/mahadevan_texts_decoded.json with id / site_code / "
            "length / sequence per inscription. The Holdat CSV corpus "
            "is loaded only when source='holdat' is set explicitly; "
            "there is no automatic fallback.",
            inputs=[],
            outputs=[
                {"name": "sequences", "type": "sequences"},
                {"name": "inscriptions", "type": "json"},
                {"name": "n_inscriptions", "type": "number"},
                {"name": "n_tokens", "type": "number"},
                {"name": "n_distinct_signs", "type": "number"},
                {"name": "label", "type": "text"},
                {"name": "source", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "default": "decoded",
                               "enum": ["decoded", "holdat"],
                               "description": "Corpus source: 'decoded' = reports/mahadevan_texts_decoded.json (default); 'holdat' = the Holdat CSV corpus, used only when selected explicitly. An absent selected source is an error, never a silent substitution."},
                    "use_raw": {"type": "boolean", "default": False,
                                "description": "If true, use raw OCR glyph chars (V=337) instead of mapped 3-digit codes."},
                    "min_length": {"type": "integer", "default": 1, "minimum": 1},
                    "max_length": {"type": "integer", "default": 0,
                                    "description": "0 = no upper bound."},
                    "label": {"type": "string", "default": "indus_m77"},
                },
            },
            fn=_m77_inscription_loader,
        ),
        AtomicNodeDef(
            "LengthStratifier", "Length Stratifier (Phase-20)",
            "Phase-20 / Transforms",
            "Bin sequences into length-based strata. Output a "
            "`stratifications` dict bin_label -> sequences for "
            "downstream per-bin analysis.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "stratifications", "type": "json"},
                {"name": "summary", "type": "json"},
                {"name": "n_bins", "type": "number"},
                {"name": "total_sequences", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "bins": {"type": "array", "default": [[1, 2], [3, 4], [5, 6], [7, 9999]]},
                },
            },
            fn=_length_stratifier,
        ),
        AtomicNodeDef(
            "BinSpectralFingerprint", "Bin Spectral Fingerprint (Phase-20)",
            "Phase-20 / Spectral",
            "Compute the bigram-transition spectral gap and top "
            "eigenvalues per length-stratification bin. Tests Phase-19 "
            "prediction 1 (M77's anomalously small spectral gap is "
            "dominated by short inscriptions).",
            inputs=[{"name": "stratifications", "type": "json", "required": True}],
            outputs=[
                {"name": "per_bin", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "n_bins_with_data", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_bin_spectral_fingerprint,
        ),
        AtomicNodeDef(
            "AllographDetector", "Allograph Detector (Phase-20)",
            "Phase-20 / Sign clustering",
            "Daggumati-style distributional clustering of signs by "
            "bigram-context cosine + position-distribution L1 distance.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "clusters", "type": "json"},
                {"name": "biggest_cluster", "type": "json"},
                {"name": "sign_to_cluster", "type": "json"},
                {"name": "n_signs_total", "type": "number"},
                {"name": "n_signs_eligible", "type": "number"},
                {"name": "n_clusters", "type": "number"},
                {"name": "n_signs_in_multi_clusters", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_count": {"type": "integer", "default": 5, "minimum": 2},
                    "cos_threshold": {"type": "number", "default": 0.55},
                    "pos_threshold": {"type": "number", "default": 0.50},
                },
            },
            fn=_allograph_detector,
        ),
        AtomicNodeDef(
            "ClusterArchaeology", "Cluster Archaeology (Phase-20)",
            "Phase-20 / Archaeology",
            "Per-cluster site-distribution + length-distribution + "
            "chi-squared test of site-vs-cluster independence.",
            inputs=[
                {"name": "inscriptions", "type": "json", "required": True},
                {"name": "sign_to_cluster", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "site_table", "type": "json"},
                {"name": "length_table", "type": "json"},
                {"name": "chi_squared", "type": "number"},
                {"name": "dof", "type": "number"},
                {"name": "significant_p05", "type": "any"},
                {"name": "verdict", "type": "text"},
                {"name": "target_cluster_signs", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "target_cluster": {"type": "integer", "default": 0,
                                        "description": "0 = biggest cluster from AllographDetector"},
                    "fixed_members": {"type": "array", "default": [],
                                       "description": "If provided, override sign_to_cluster and use this list as target."},
                },
            },
            fn=_cluster_archaeology,
        ),
        AtomicNodeDef(
            "PDFTextExtractor", "PDF Text Extractor (Phase-20)",
            "Sources",
            "Extract text per page from a PDF using PyMuPDF.",
            inputs=[{"name": "file_path", "type": "any", "required": False}],
            outputs=[
                {"name": "pages", "type": "json"},
                {"name": "n_total_pages", "type": "number"},
                {"name": "n_pages_extracted", "type": "number"},
                {"name": "total_characters", "type": "number"},
                {"name": "file_path", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "default": ""},
                    "max_pages": {"type": "integer", "default": 100, "minimum": 1},
                    "start_page": {"type": "integer", "default": 0, "minimum": 0},
                },
            },
            fn=_pdf_text_extractor,
        ),
        AtomicNodeDef(
            "CMCatalogParser", "CM Catalog Parser (Phase-20)",
            "Phase-20 / Sources",
            "Heuristic Cypro-Minoan catalog extractor (Ferrara 2006 "
            "OCR text). Recovers inscription IDs, sign sequences, and "
            "per-sign frequency where parseable.",
            inputs=[{"name": "pages", "type": "json", "required": True}],
            outputs=[
                {"name": "inscriptions_sample", "type": "json"},
                {"name": "n_inscriptions_recovered", "type": "number"},
                {"name": "n_with_sequence", "type": "number"},
                {"name": "top_sign_codes", "type": "json"},
                {"name": "top_cm_unicode", "type": "json"},
                {"name": "n_cm_unicode_glyphs", "type": "number"},
                {"name": "n_pages_with_signs", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_cm_catalog_parser,
        ),
        AtomicNodeDef(
            "FulsPositionalClassifier", "Fuls Positional Classifier (Phase-20)",
            "Phase-20 / Sign function",
            "Fuls 2013-style 5-way per-sign classification: INITIAL / "
            "MEDIAL / TERMINAL / NUMERICAL / MIXED based on I/M/T rates "
            "and same-sign repetition rate.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "table", "type": "json"},
                {"name": "counts_by_class", "type": "json"},
                {"name": "fractions_by_class", "type": "json"},
                {"name": "n_signs_classified", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_count": {"type": "integer", "default": 5, "minimum": 2},
                    "dom_threshold": {"type": "number", "default": 0.55},
                    "secondary_threshold": {"type": "number", "default": 0.30},
                    "numerical_rr": {"type": "number", "default": 0.20},
                },
            },
            fn=_fuls_positional_classifier,
        ),
        AtomicNodeDef(
            "Phase20Verdict", "Phase-20 Verdict Aggregator",
            "Phase-20 / Synthesis",
            "Combine the four Phase-20 sub-experiment outputs into a "
            "yes/no/partially-confirmed verdict per Phase-19 prediction.",
            inputs=[
                {"name": "length_strata", "type": "json", "required": False},
                {"name": "cluster_archaeology", "type": "json", "required": False},
                {"name": "ferrara_cm", "type": "json", "required": False},
                {"name": "fuls_positional", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "prediction_1_length_dominates_spectral_gap", "type": "text"},
                {"name": "prediction_2_cluster_archaeology_nonrandom", "type": "text"},
                {"name": "prediction_3_ferrara_cm_extractable", "type": "text"},
                {"name": "prediction_4_numerical_strokes_confirmed", "type": "text"},
                {"name": "evidence", "type": "json"},
                {"name": "summary", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase20_verdict,
        ),
    ]


__all__ = [
    "_m77_inscription_loader",
    "_length_stratifier",
    "_bin_spectral_fingerprint",
    "_allograph_detector",
    "_cluster_archaeology",
    "_pdf_text_extractor",
    "_cm_catalog_parser",
    "_fuls_positional_classifier",
    "_phase20_verdict",
    "_phase20_node_defs",
]
