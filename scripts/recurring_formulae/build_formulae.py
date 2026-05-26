"""Build recurring formula table from the 7,138-inscription translation corpus.

Scans for repeated multi-sign sequences (bigrams, trigrams, 4-grams),
computes site distribution and motif context, and flags failure/ambiguous cases.

Output:
  data/public/recurring_formulae.csv
  outputs/reports/recurring_formulae_failure_cases.md
"""
import csv
import json
import pathlib
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAX_NGRAM = 4
MIN_COUNT = 3  # minimum inscription count for a formula


def load_corpus():
    """Load translation corpus."""
    path = ROOT / "outputs" / "seal_translations.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["translations"]


def load_anchor_table():
    """Load anchor table for sign→reading lookup."""
    path = ROOT / "research" / "indus" / "anchor_table.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    lookup = {}
    anchors = data.get("anchors", {})
    if isinstance(anchors, dict):
        for sign, info in anchors.items():
            s = sign.replace("M", "").zfill(3)
            lookup[s] = {
                "reading": info.get("reading", ""),
                "dedr": info.get("dedr", info.get("DEDR", "")),
            }
    else:
        for a in anchors:
            sign = a.get("Sign", a.get("sign", ""))
            if sign:
                s = sign.replace("M", "").zfill(3)
                lookup[s] = {
                    "reading": a.get("Reading", a.get("reading", "")),
                    "dedr": a.get("DEDR", a.get("dedr", "")),
                }
    return lookup


def extract_ngrams(signs, n):
    """Extract all n-grams from a sign sequence."""
    return [tuple(signs[i : i + n]) for i in range(len(signs) - n + 1)]


def build_formulae():
    """Build recurring formula table."""
    corpus = load_corpus()
    anchors = load_anchor_table()

    # Collect n-gram occurrences with metadata
    ngram_data = defaultdict(lambda: {
        "inscriptions": [],
        "sites": Counter(),
        "corpora": Counter(),
        "grammar_patterns": Counter(),
    })

    for entry in corpus:
        signs = entry["signs"]
        if not signs or len(signs) < 2:
            continue
        site = entry.get("site", "unknown") or "unknown"
        corpus_name = entry.get("corpus", "unknown")
        grammar = entry.get("grammar_pattern", "")
        insc_id = entry.get("id", "")

        for n in range(2, min(MAX_NGRAM + 1, len(signs) + 1)):
            for ngram in extract_ngrams(signs, n):
                key = ngram
                d = ngram_data[key]
                d["inscriptions"].append(insc_id)
                d["sites"][site] += 1
                d["corpora"][corpus_name] += 1
                d["grammar_patterns"][grammar] += 1

    # Filter to formulae with MIN_COUNT inscriptions
    formulae = []
    failure_cases = []

    for ngram, data in sorted(
        ngram_data.items(), key=lambda x: len(x[1]["inscriptions"]), reverse=True
    ):
        count = len(data["inscriptions"])
        if count < MIN_COUNT:
            continue

        # Build reading sequence
        readings = []
        glosses = []
        for sign in ngram:
            info = anchors.get(sign, {})
            r = info.get("reading", f"?{sign}")
            readings.append(r)
            glosses.append(r)

        reading_seq = " + ".join(readings)
        sign_seq = " ".join(ngram)
        site_count = len(data["sites"])
        site_list = ", ".join(
            f"{s}({c})" for s, c in data["sites"].most_common(5)
        )

        # Determine positional pattern from grammar_patterns
        patterns = data["grammar_patterns"]
        dominant_pattern = patterns.most_common(1)[0][0] if patterns else ""

        # Evidence tier based on count and site distribution
        if count >= 20 and site_count >= 3:
            tier = "HIGH"
        elif count >= 10 or site_count >= 2:
            tier = "MEDIUM"
        else:
            tier = "LOW"

        # Detect failure/ambiguous cases
        is_failure = False
        caveats = []

        # Check if all readings are unknown
        unknowns = sum(1 for r in readings if r.startswith("?"))
        if unknowns > 0:
            caveats.append(f"{unknowns}/{len(readings)} signs lack anchor readings")
            if unknowns > len(readings) // 2:
                is_failure = True

        # Check for context weakness: only 1 site
        if site_count == 1 and count < 10:
            caveats.append("single-site formula, context may be local")

        # Check for inconsistent grammar patterns
        if len(patterns) > 1:
            top_pct = patterns.most_common(1)[0][1] / count
            if top_pct < 0.5:
                caveats.append(
                    f"inconsistent grammar patterns (top pattern only {top_pct:.0%})"
                )
                is_failure = True

        formula = {
            "formula_id": f"F{len(formulae) + 1:03d}",
            "sign_sequence": sign_seq,
            "n_gram_size": len(ngram),
            "proposed_reading": reading_seq,
            "inscription_count": count,
            "site_count": site_count,
            "site_distribution": site_list,
            "dominant_grammar_pattern": dominant_pattern,
            "evidence_tier": tier,
            "caveats": "; ".join(caveats) if caveats else "",
            "is_failure_case": is_failure,
        }
        formulae.append(formula)

        if is_failure:
            failure_cases.append(formula)

    return formulae, failure_cases


def write_csv(formulae):
    """Write recurring formulae CSV."""
    out = ROOT / "data" / "public" / "recurring_formulae.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "formula_id", "sign_sequence", "n_gram_size", "proposed_reading",
        "inscription_count", "site_count", "site_distribution",
        "dominant_grammar_pattern", "evidence_tier", "caveats",
        "is_failure_case",
    ]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(formulae)
    print(f"[CSV] {out} ({len(formulae)} formulae)")
    return out


def write_failure_report(failure_cases, all_count):
    """Write failure cases markdown report."""
    out = ROOT / "outputs" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "recurring_formulae_failure_cases.md"

    lines = [
        "# Recurring Formula Failure / Ambiguous Cases",
        "",
        f"Total formulae identified: {all_count}",
        f"Failure/ambiguous cases: {len(failure_cases)}",
        "",
        "These are sign sequences that recur across inscriptions but where",
        "the proposed readings are problematic, context is weak, or grammar",
        "patterns are inconsistent.",
        "",
    ]

    for fc in failure_cases[:20]:  # Cap at 20
        lines.extend([
            f"## {fc['formula_id']}: {fc['sign_sequence']}",
            f"- **Reading**: {fc['proposed_reading']}",
            f"- **Count**: {fc['inscription_count']} inscriptions, "
            f"{fc['site_count']} sites",
            f"- **Sites**: {fc['site_distribution']}",
            f"- **Tier**: {fc['evidence_tier']}",
            f"- **Issue**: {fc['caveats']}",
            "",
        ])

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[MD]  {path} ({len(failure_cases)} cases)")
    return path


if __name__ == "__main__":
    formulae, failures = build_formulae()
    # Limit to top 100 for CSV
    top_formulae = formulae[:100]
    write_csv(top_formulae)
    write_failure_report(failures, len(formulae))

    # Summary
    high = sum(1 for f in top_formulae if f["evidence_tier"] == "HIGH")
    med = sum(1 for f in top_formulae if f["evidence_tier"] == "MEDIUM")
    low = sum(1 for f in top_formulae if f["evidence_tier"] == "LOW")
    fails = sum(1 for f in top_formulae if f["is_failure_case"])
    print(f"\nSummary: {len(top_formulae)} formulae in CSV "
          f"(HIGH={high}, MEDIUM={med}, LOW={low}, failures={fails})")
