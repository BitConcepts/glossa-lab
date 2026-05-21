"""Phase-53: Formula Corpus + Pilot Inscription Readings.

With confirmed readings for 7 HIGH + many MEDIUM signs, we can now
decode the most frequent inscription formulas partially or fully.

This script:
  1. Extracts the 50 most frequent inscription formula patterns
  2. For each formula, fills in confirmed readings slot by slot
  3. Produces human-readable candidate readings with confidence per slot
  4. Cross-references against Phase-52 SA decipherment table
  5. Outputs the first publicly defensible candidate translation set

Formula structure: each inscription = a sequence of sign M-numbers
  e.g. [M062, M267, M099, M176] = [erutu, ?, kol, aṇ]
                                 = "[bull] [particle] lord (masc)"

GPU: torch for formula pattern clustering.

Output: reports/phase53_formula_pilot.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None; DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
SA_TABLE = REPO / "reports/phase52_full_decipherment_table.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase53_formula_pilot.json"

# Confidence display
CONF_SYMBOL = {"HIGH": "✓✓", "MEDIUM": "✓", "LOW": "~", "UNREAD": "?", "UNCERTAIN": "??"}


def load_corpus_as_inscriptions() -> list[list[str]]:
    seals: dict[str, list] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return [[s for s in v if s] for v in seals.values() if any(v)]


def load_readings() -> dict[str, dict]:
    """Merge anchor readings with Phase-52 SA table."""
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    readings: dict[str, dict] = {}
    for sign, info in anchors.items():
        if info.get("reading"):
            readings[sign] = {
                "reading": info["reading"],
                "confidence": info.get("confidence", "UNKNOWN"),
                "gloss": info.get("gloss", ""),
            }
    # Add SA readings for signs without anchor readings
    if SA_TABLE.exists():
        table = json.loads(SA_TABLE.read_text("utf-8"))
        for entry in table:
            sign = entry["sign"]
            if sign not in readings and entry.get("sa_reading") and entry["sa_reading"] != "?":
                readings[sign] = {
                    "reading": entry["sa_reading"],
                    "confidence": "SA_CANDIDATE",
                    "gloss": "SA-derived candidate",
                }
    return readings


def render_inscription(signs: list[str], readings: dict) -> str:
    """Render an inscription as a reading string."""
    parts = []
    for s in signs:
        r = readings.get(s, {})
        reading = r.get("reading", "?")
        conf = r.get("confidence", "UNREAD")
        sym = CONF_SYMBOL.get(conf, "?")
        parts.append(f"{reading}[{sym}]")
    return " · ".join(parts)


def render_morphological(signs: list[str], readings: dict) -> str:
    """Attempt morphological parsing: CLASSIFIER + PARTICLE + TITLE + SUFFIX."""
    tokens = []
    for s in signs:
        r = readings.get(s, {})
        reading = r.get("reading", "?")
        conf = r.get("confidence", "UNREAD")
        tokens.append((s, reading, conf))

    # Parse structure
    parts = []
    for sign, reading, conf in tokens:
        if conf == "UNREAD":
            parts.append(f"[{sign}]")
        elif conf == "SA_CANDIDATE":
            parts.append(f"({reading})")
        else:
            parts.append(reading)
    return "-".join(parts)


def cluster_formulas_gpu(formulas: list[tuple], all_signs: list[str]) -> dict:
    """GPU: cluster formulas by sign overlap to find formula families."""
    if torch is None or not formulas:
        return {}
    sign_idx = {s: i for i, s in enumerate(all_signs)}
    n_signs = len(all_signs)
    n_forms = len(formulas)

    # Build binary occurrence matrix [formula × sign]
    mat = torch.zeros(n_forms, n_signs, device=DEVICE)
    for i, (pattern, count) in enumerate(formulas):
        for s in pattern:
            if s in sign_idx:
                mat[i, sign_idx[s]] = 1.0

    # Cosine similarity between formulas
    norms = mat.norm(dim=1, keepdim=True).clamp(min=1e-8)
    mat_n = mat / norms
    sim = (mat_n @ mat_n.T).cpu()

    # Group formulas by similarity ≥ 0.5
    clusters: dict[int, list[int]] = {}
    assigned = set()
    for i in range(n_forms):
        if i in assigned: continue
        cluster = [i]
        for j in range(i+1, n_forms):
            if j not in assigned and float(sim[i,j]) >= 0.5:
                cluster.append(j); assigned.add(j)
        clusters[i] = cluster
        assigned.add(i)

    print(f"[GPU:{DEVICE}] Formula clusters: {len(clusters)} groups from {n_forms} formulas")
    return {str(k): v for k, v in clusters.items()}


def main() -> None:
    print("Phase-53: Formula Corpus + Pilot Inscription Readings\n")

    inscriptions = load_corpus_as_inscriptions()
    readings = load_readings()
    print(f"  Inscriptions: {len(inscriptions)}")
    print(f"  Signs with readings: {len(readings)}")

    # Count formula frequencies
    formula_counter: Counter = Counter()
    for insc in inscriptions:
        formula_counter[tuple(insc)] += 1

    top_formulas = formula_counter.most_common(50)
    print(f"\n  Top 50 formula patterns (of {len(formula_counter)} unique)")

    # Decode each formula
    decoded_formulas = []
    for pattern, count in top_formulas:
        n_known = sum(1 for s in pattern if s in readings and readings[s]["confidence"] in ("HIGH","MEDIUM"))
        n_total = len(pattern)
        coverage = n_known / n_total if n_total else 0

        rendered = render_inscription(list(pattern), readings)
        morphological = render_morphological(list(pattern), readings)

        # Build per-sign annotation
        slot_annotations = []
        for s in pattern:
            r = readings.get(s, {})
            slot_annotations.append({
                "sign": s,
                "reading": r.get("reading", "?"),
                "confidence": r.get("confidence", "UNREAD"),
                "gloss": r.get("gloss", ""),
            })

        decoded_formulas.append({
            "pattern": list(pattern),
            "count": count,
            "length": n_total,
            "n_known_slots": n_known,
            "coverage_pct": round(coverage * 100, 1),
            "rendered": rendered,
            "morphological": morphological,
            "slots": slot_annotations,
        })

    # Print most complete readings
    best_decoded = sorted(decoded_formulas, key=lambda x: (-x["coverage_pct"], -x["count"]))
    print("\n=== Best-Decoded Formulas ===")
    for f in best_decoded[:20]:
        print(f"  [{f['count']:4d}×] ({f['n_known_slots']}/{f['length']}) {f['rendered']}")

    # GPU clustering
    all_signs = sorted(set(s for pattern, _ in top_formulas for s in pattern))
    clusters = cluster_formulas_gpu(top_formulas, all_signs)

    # Interesting pilot readings (fully or mostly decoded)
    fully_decoded = [f for f in decoded_formulas if f["coverage_pct"] >= 80]
    print(f"\n  Formulas ≥80% decoded: {len(fully_decoded)}")
    for f in fully_decoded[:10]:
        print(f"  [{f['count']:4d}×] {f['morphological']}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "n_inscriptions": len(inscriptions),
        "n_unique_formulas": len(formula_counter),
        "n_signs_with_readings": len(readings),
        "top_50_formulas": decoded_formulas,
        "fully_decoded": fully_decoded[:10],
        "formula_clusters": {k: v[:5] for k, v in list(clusters.items())[:10]},
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
