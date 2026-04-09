"""Contact Zone Analysis — Indus Script.

Tests whether inscriptions from sites with known Mesopotamian trade contact
show statistically distinct sign usage patterns compared to inland sites,
supporting or challenging the 'contact hypothesis' for script dissemination.

Registered as an ExperimentBase so it appears in the Experiments tab.

References:
  Fuls (2023): site metadata with ICIT IDs
  Parpola (1994): Mesopotamian contact sites (Bahrain, Failaka, Lothal, Sutkagen-dor)
  Kenoyer (1998): Persian Gulf trade routes
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object  # type: ignore[assignment,misc]

_REPORTS = Path(__file__).resolve().parent.parent.parent.parent / "reports"

# ── Contact zone site classification ─────────────────────────────────────────
# Sources: Parpola 1994, Kenoyer 1998, Fuls 2023
# "contact" = sites with confirmed or probable Mesopotamian trade contact
# "inland"  = core Indus heartland sites (IVC urban centres)
# "peripheral" = Indus periphery sites with limited external contact

SITE_GROUPS: dict[str, str] = {
    # Contact zone / Persian Gulf trade
    "Lothal": "contact",           # Gujarat port, Persian Gulf trade
    "Sutkagen-Dor": "contact",     # Makran coast, westernmost major site
    "Sokhta Koh": "contact",       # Makran coast
    "Balakot": "contact",          # Makran coast
    "Desalpur": "contact",         # Gujarat, coastal
    "Kuntasi": "contact",          # Gujarat, coastal
    "Shortugai": "contact",        # Afghanistan, lapis lazuli route
    "Dholavira": "contact",        # Gujarat island, trade hub

    # Core heartland (major urban centres)
    "Harappa": "heartland",
    "Mohenjo-Daro": "heartland",
    "Chanhu-Daro": "heartland",
    "Rakhigarhi": "heartland",

    # Eastern periphery
    "Kalibangan": "peripheral",
    "Banawali": "peripheral",
    "Mitathal": "peripheral",
    "Hulas": "peripheral",
    "Alamgirpur": "peripheral",
}

# Normalise site names to match the OCR output format
_NORM: dict[str, str] = {s.lower(): g for s, g in SITE_GROUPS.items()}

# ── Utility functions ─────────────────────────────────────────────────────────


def _group(site: str) -> str:
    """Return site group label, defaulting to 'other'."""
    return _NORM.get(site.lower().strip(), "other")


def _h1(freq: Counter) -> float:
    """Shannon entropy H1 in nats."""
    n = sum(freq.values())
    if n == 0:
        return 0.0
    return -sum((c / n) * math.log(c / n) for c in freq.values() if c > 0)


def _kl(p: dict[str, float], q: dict[str, float], eps: float = 1e-6) -> float:
    """KL-divergence D(p || q)."""
    keys = set(p) | set(q)
    return sum(
        p.get(k, 0) * math.log(p.get(k, 0) / max(q.get(k, eps), eps))
        for k in keys
        if p.get(k, 0) > 0
    )


def _freq_dist(inscriptions: list[list[str]]) -> dict[str, float]:
    """Normalised unigram frequency distribution."""
    flat = [s for ins in inscriptions for s in ins]
    total = len(flat)
    if total == 0:
        return {}
    c = Counter(flat)
    return {s: n / total for s, n in c.items()}


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b) if (a | b) else 0.0


# ── Experiment ────────────────────────────────────────────────────────────────


def run_contact_zone_analysis(verbose: bool = True) -> dict[str, Any]:
    """
    Compare sign usage between contact-zone, heartland, and peripheral sites.

    Returns a results dict compatible with the ExperimentBase contract.
    """
    # Load corpus
    corpus_path = _REPORTS / "icit_extracted_corpus.json"
    if not corpus_path.exists():
        return {"error": "icit_extracted_corpus.json not found. Run OCR or TXT extraction first."}

    data = json.loads(corpus_path.read_text(encoding="utf-8"))
    inscriptions_raw = data.get("inscriptions", [])

    # Group inscriptions by site_group
    groups: dict[str, list[list[str]]] = {}
    site_counts: dict[str, int] = {}

    for ins in inscriptions_raw:
        site = ins.get("site", "Unknown")
        g = _group(site)
        groups.setdefault(g, []).append(ins.get("sequence", []))
        site_counts[site] = site_counts.get(site, 0) + 1

    group_counts = {g: len(inss) for g, inss in groups.items()}

    if verbose:
        print(f"  Corpus: {len(inscriptions_raw)} inscriptions")
        for g in ("contact", "heartland", "peripheral", "other"):
            print(f"    {g:<12}: {group_counts.get(g, 0):>5} inscriptions")

    # ── Per-group sign statistics ─────────────────────────────────────────────
    group_stats: dict[str, dict] = {}
    group_vocab: dict[str, set[str]] = {}

    for g, inss in groups.items():
        flat = [s for ins in inss for s in ins]
        freq = Counter(flat)
        n = len(flat)
        n_types = len(freq)
        h1 = _h1(freq)
        ln_v = math.log(n_types) if n_types > 1 else 1.0

        lengths = [len(ins) for ins in inss]
        mean_len = sum(lengths) / max(len(lengths), 1)

        # Top 10 signs
        top10 = freq.most_common(10)

        # TMK-like analysis: signs with terminal_rate >= 0.60
        terminal_c: Counter = Counter()
        initial_c: Counter = Counter()
        total_c: Counter = Counter()
        for ins in inss:
            if not ins:
                continue
            total_c.update(ins)
            if len(ins) == 1:
                pass
            else:
                initial_c[ins[0]] += 1
                terminal_c[ins[-1]] += 1

        tmk_signs = {
            s for s in total_c
            if total_c[s] >= 4 and terminal_c[s] / total_c[s] >= 0.60
        }
        initial_signs = {
            s for s in total_c
            if total_c[s] >= 4 and initial_c[s] / total_c[s] >= 0.55
        }

        group_vocab[g] = set(freq.keys())
        group_stats[g] = {
            "n_inscriptions": len(inss),
            "n_tokens": n,
            "n_sign_types": n_types,
            "mean_inscription_length": round(mean_len, 3),
            "h1_nats": round(h1, 4),
            "h1_normalized": round(h1 / ln_v, 4) if ln_v > 0 else 0,
            "n_tmk_signs": len(tmk_signs),
            "n_initial_signs": len(initial_signs),
            "top_10_signs": [{"sign": s, "count": c} for s, c in top10],
        }

    # ── Cross-group vocabulary overlap (Jaccard) ──────────────────────────────
    group_names = [g for g in ("contact", "heartland", "peripheral") if g in groups]
    jaccard_matrix: dict[str, dict[str, float]] = {}
    for g1 in group_names:
        jaccard_matrix[g1] = {}
        for g2 in group_names:
            jaccard_matrix[g1][g2] = round(_jaccard(group_vocab[g1], group_vocab[g2]), 4)

    # ── KL-divergence of sign frequency distributions ─────────────────────────
    group_dists = {g: _freq_dist(inss) for g, inss in groups.items()}
    kl_matrix: dict[str, dict[str, float]] = {}
    for g1 in group_names:
        kl_matrix[g1] = {}
        for g2 in group_names:
            if g1 == g2:
                kl_matrix[g1][g2] = 0.0
            else:
                kl_matrix[g1][g2] = round(_kl(group_dists[g1], group_dists[g2]), 4)

    # ── Exclusive signs: signs appearing ONLY in contact-zone sites ───────────
    contact_vocab = group_vocab.get("contact", set())
    heartland_vocab = group_vocab.get("heartland", set())
    peripheral_vocab = group_vocab.get("peripheral", set())

    contact_exclusive = contact_vocab - heartland_vocab - peripheral_vocab
    heartland_only = heartland_vocab - contact_vocab - peripheral_vocab

    # ── Site-level summary ────────────────────────────────────────────────────
    top_sites = sorted(site_counts.items(), key=lambda x: -x[1])[:20]

    # ── Contact-specific bigram patterns ─────────────────────────────────────
    contact_inss = groups.get("contact", [])
    heartland_inss = groups.get("heartland", [])

    def bigram_freq(inss: list[list[str]]) -> Counter:
        bg: Counter = Counter()
        for ins in inss:
            for j in range(len(ins) - 1):
                bg[(ins[j], ins[j + 1])] += 1
        return bg

    contact_bg = bigram_freq(contact_inss)
    heartland_bg = bigram_freq(heartland_inss)

    contact_top_bigrams = [
        {"bigram": list(bg), "count": c}
        for bg, c in contact_bg.most_common(10)
    ]
    heartland_top_bigrams = [
        {"bigram": list(bg), "count": c}
        for bg, c in heartland_bg.most_common(10)
    ]

    # ── Interpretation ────────────────────────────────────────────────────────
    # Low KL(contact || heartland) = similar distributions (no contact zone distinction)
    # High Jaccard = shared vocabulary (expected for same script)
    # Exclusive contact signs: signs only at trade ports → possible loanwords?

    kl_contact_heartland = kl_matrix.get("contact", {}).get("heartland", None)

    if kl_contact_heartland is not None and kl_contact_heartland < 0.5:
        interpretation = (
            f"Contact-zone sites show LOW KL-divergence from heartland "
            f"(KL={kl_contact_heartland:.3f}), suggesting a unified script with "
            "minimal geographic specialisation. "
            "Exclusive contact-zone signs may represent trade-specific logograms."
        )
    elif kl_contact_heartland is not None:
        interpretation = (
            f"Contact-zone sites show HIGH KL-divergence from heartland "
            f"(KL={kl_contact_heartland:.3f}), suggesting regional script variation "
            "at trade interface sites. "
            "This is consistent with script adaptation for external audiences."
        )
    else:
        interpretation = "Insufficient data for contact vs heartland comparison."

    if verbose:
        print("\n  Cross-group KL-divergences:")
        for g1 in group_names:
            for g2 in group_names:
                if g1 != g2:
                    print(f"    KL({g1} || {g2}) = {kl_matrix[g1][g2]:.4f}")
        print("\n  Vocabulary overlap (Jaccard):")
        for g1 in group_names:
            for g2 in group_names:
                if g1 < g2:
                    print(f"    {g1} ∩ {g2}: {jaccard_matrix[g1][g2]:.3f}")
        print(f"\n  Contact-exclusive signs: {len(contact_exclusive)}")
        print(f"  Heartland-only signs:    {len(heartland_only)}")
        print(f"\n  Interpretation: {interpretation}")

    return {
        "group_stats": group_stats,
        "jaccard_overlap": jaccard_matrix,
        "kl_divergences": kl_matrix,
        "contact_exclusive_signs": sorted(contact_exclusive),
        "heartland_only_signs": sorted(heartland_only),
        "top_sites": [{"site": s, "n_inscriptions": c} for s, c in top_sites],
        "contact_top_bigrams": contact_top_bigrams,
        "heartland_top_bigrams": heartland_top_bigrams,
        "interpretation": interpretation,
        "notes": {
            "contact_sites": sorted(s for s, g in SITE_GROUPS.items() if g == "contact"),
            "heartland_sites": sorted(s for s, g in SITE_GROUPS.items() if g == "heartland"),
            "data_source": "icit_extracted_corpus.json (PDF OCR)",
            "method": (
                "KL-divergence and Jaccard overlap of sign frequency "
                "distributions by site group"
            ),
        },
    }


class ContactZoneAnalysis(_EB):
    id = "contact_zone"
    name = "Contact Zone Analysis"
    category = "Research"
    description = (
        "Compares sign usage between Mesopotamian trade-contact sites "
        "(Lothal, Dholavira, Sutkagen-Dor) and heartland sites (Harappa, Mohenjo-daro). "
        "Tests for script specialisation at trade interfaces. "
        "Requires icit_extracted_corpus.json in reports/ (run OCR pipeline or TXT extraction first)."
    )
    estimated_time = "< 1 min"
    requires_key = None
    results_file = "reports/contact_zone_results.json"
    params_schema = {
        "type": "object",
        "properties": {
            "corpus_id": {
                "type": "string",
                "title": "Corpus ID",
                "description": (
                    "NOT USED — Contact Zone Analysis requires the ICIT corpus with "
                    "per-inscription site metadata (Lothal, Harappa, etc.). "
                    "It always loads icit_extracted_corpus.json from reports/. "
                    "Leave blank."
                ),
            },
        },
    }

    def run(self, **kwargs) -> dict:  # type: ignore[override]
        # corpus_id param is accepted for UI schema consistency but NOT used —
        # this experiment requires the ICIT corpus with site metadata that generic
        # corpora do not have.  It always loads icit_extracted_corpus.json.
        result = run_contact_zone_analysis(verbose=False)
        out = _REPORTS / "contact_zone_results.json"
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result


if __name__ == "__main__":
    result = run_contact_zone_analysis(verbose=True)
    out = _REPORTS / "contact_zone_results.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved to {out}")
