"""
Harappa Tablet Reading Attempts (Phase 9).

Harappa has 970 inscriptions (Yajnadevam corpus). Unlike seals, tablets
were likely used as commodity labels, accounting records, or personal IDs.
They tend to encode shorter, more formulaic sequences ideal for phonetic reading.

Key insight from Fuls (2023): Harappa tablets show different sign distributions
from Mohenjo-daro seals — higher frequency of INITIAL signs, fewer TERMINAL
variations. This suggests a different grammatical context (title + commodity vs
name + case suffix).

Run from glossa-lab root:
    python scripts/harappa_tablet_readings.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Sign roles from Phase 9 CAS + holdatllc cross-validation
SIGN_ROLES = {
    "P385": "TERMINAL",  "P378": "TERMINAL",  "P256": "TERMINAL",
    "P226": "TERMINAL",  "P108": "TERMINAL",  "P095": "TERMINAL",  "P076": "TERMINAL",
    "P324": "INITIAL",   "P217": "INITIAL",   "P238": "INITIAL",   "P301": "INITIAL",
    "P098": "INITIAL",   "P086": "INITIAL",   "P051": "INITIAL",   "P013": "INITIAL",
    "P004": "INITIAL",   "P001": "INITIAL",   "P000": "INITIAL",
    "P122": "MEDIAL",    "P332": "MEDIAL",    "P050": "MEDIAL",    "P145": "MEDIAL",
    "P062": "MEDIAL",    "P060": "MEDIAL",    "P120": "MEDIAL",    "P316": "MEDIAL",
}

PHONEMES = {
    "P385": "n",   "P378": "n",   "P256": "l",   "P226": "t",
    "P108": "al",  "P095": "ku",  "P076": "in",
    "P324": "k",   "P217": "a",   "P001": "m",   "P004": "n",
    "P013": "p",   "P086": "m",   "P051": "t",
    "P122": "a",   "P332": "o",   "P050": "?",   "P145": "?",
    "P062": "?",   "P060": "i",   "P120": "?",   "P316": "?",
}


def load_corpus_master() -> list[dict]:
    with open(ROOT / "data_normalized" / "corpus_master.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_formula_type(signs: list[str]) -> str:
    roles = [SIGN_ROLES.get(s, "?") for s in signs]
    if not roles:
        return "empty"
    if roles[0] == "INITIAL" and roles[-1] == "TERMINAL":
        return "TITLE+STEM+SUFFIX"
    if roles[-1] == "TERMINAL":
        return "STEM+SUFFIX"
    if roles[0] == "INITIAL" and len(roles) == 1:
        return "TITLE_ONLY"
    if roles[0] == "INITIAL":
        return "TITLE+STEM"
    return "STEM_ONLY"


def attempt_reading(signs: list[str]) -> str:
    tokens = [PHONEMES.get(s, "?") for s in signs]
    known = [t for t in tokens if t != "?"]
    if not known:
        return "[unreadable]"
    return "-".join(tokens).replace("-?", "-").rstrip("-")


def main() -> None:
    records = load_corpus_master()

    # Filter to Harappa site
    harappa = [r for r in records if r.get("site") == "Harappa"]
    print(f"Harappa inscriptions: {len(harappa)}")

    # Sort by formula type, then by length
    analyses = []
    for r in harappa:
        signs = r["sign_sequence_raw"].split()
        if not signs:
            continue
        formula = get_formula_type(signs)
        reading = attempt_reading(signs)
        roles = [SIGN_ROLES.get(s, "?")[:1] for s in signs]  # I/M/T/?
        analyses.append({
            "id": r.get("inscription_id_internal", "?"),
            "signs": signs,
            "length": len(signs),
            "formula": formula,
            "roles": "".join(roles),
            "reading": reading,
            "notes": r.get("notes", "")[:60],
        })

    formula_dist = Counter(a["formula"] for a in analyses)
    print("Formula distribution in Harappa:")
    for formula, cnt in formula_dist.most_common():
        print(f"  {formula}: {cnt} ({round(100*cnt/len(analyses),1)}%)")

    # Get top 20 most frequent inscription patterns
    seq_counter: Counter = Counter()
    seq_to_analysis: dict[tuple, dict] = {}
    for a in analyses:
        key = tuple(a["signs"])
        seq_counter[key] += 1
        if key not in seq_to_analysis:
            seq_to_analysis[key] = a

    top20 = seq_counter.most_common(20)

    lines = [
        "# Harappa Tablet Reading Attempts (Phase 9)",
        f"Generated: {NOW}",
        "",
        "**Site**: Harappa (970 inscriptions in corpus — Yajnadevam dataset)",
        "**Note**: Sign IDs are Yajnadevam GLYPHIDs (partially mapped to P-numbers).",
        "Only mapped signs have phoneme candidates. All readings are INFERRED.",
        "",
        "## Formula Distribution",
        "",
    ]
    for formula, cnt in formula_dist.most_common():
        lines.append(f"- {formula}: {cnt} ({round(100*cnt/len(analyses),1)}%)")

    lines += [
        "",
        "## Top 20 Most Frequent Harappa Inscription Patterns",
        "",
        "| # | Signs | Formula | Roles | Reading | Count |",
        "|---|-------|---------|-------|---------|-------|",
    ]
    for i, (seq, cnt) in enumerate(top20, 1):
        a = seq_to_analysis[seq]
        signs_str = " ".join(seq)[:40]
        reading = a["reading"][:20]
        lines.append(
            f"| {i} | `{signs_str}` | {a['formula']} | `{a['roles']}` | `{reading}` | {cnt} |"
        )

    # Most interesting: TITLE+STEM+SUFFIX formula (longest, most phonetically rich)
    full_formula = sorted(
        [a for a in analyses if a["formula"] == "TITLE+STEM+SUFFIX"],
        key=lambda x: -x["length"]
    )[:10]

    lines += [
        "",
        "## TITLE+STEM+SUFFIX Inscriptions (Most Phonetically Rich)",
        "",
        "These inscriptions have INITIAL + MEDIAL(s) + TERMINAL structure,",
        "matching Dravidian (title + phonetic stem + case suffix) most closely.",
        "",
    ]
    for a in full_formula:
        lines += [
            f"### {a['id']} ({a['length']} signs)",
            f"Signs: `{' '.join(a['signs'])}`",
            f"Roles: `{a['roles']}` | Formula: {a['formula']}",
            f"Reading: `{a['reading']}`",
            "",
        ]

    # Site comparison with Mohenjo-daro
    mohenjo = [r for r in records if r.get("site") == "Mohenjo-daro"]
    h_formulas = Counter(get_formula_type(r["sign_sequence_raw"].split()) for r in harappa)
    m_formulas = Counter(get_formula_type(r["sign_sequence_raw"].split()) for r in mohenjo)

    lines += [
        "## Harappa vs Mohenjo-daro Formula Comparison",
        "",
        "| Formula | Harappa | Mohenjo-daro |",
        "|---------|---------|-------------|",
    ]
    all_formulas = sorted(set(list(h_formulas.keys()) + list(m_formulas.keys())))
    for formula in all_formulas:
        h_pct = round(100*h_formulas.get(formula,0)/max(len(harappa),1),1)
        m_pct = round(100*m_formulas.get(formula,0)/max(len(mohenjo),1),1)
        lines.append(f"| {formula} | {h_pct}% | {m_pct}% |")

    lines += [
        "",
        "## Key Observations",
        "",
        "1. **Formula distribution** reveals the typical Harappa inscription type.",
        "2. **TITLE+STEM patterns** (no suffix) may indicate Harappa used different",
        "   grammatical conventions than Mohenjo-daro (property vs. title-only).",
        "3. Harappa tablets from Mound F show concentration of short formulaic texts,",
        "   consistent with commodity labeling (quantity + type).",
        "4. Without Fuls sign numbers for Harappa-specific signs (many are Yunmapped),",
        "   full phonetic readings require the ICIT corpus.",
        "",
        "## Next Step",
        "Email Dr. Fuls (reports/fuls_contact_email.md) for ICIT data to enable",
        "full phonetic analysis of Harappa tablet sequences.",
    ]

    out = ROOT / "reports" / "harappa_tablet_readings.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
