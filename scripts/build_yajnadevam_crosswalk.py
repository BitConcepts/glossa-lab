"""
Build Yajnadevam GLYPHID ↔ Parpola P-number crosswalk.

Method: sequence alignment on shared inscriptions.
Both the Yajnadevam corpus and the mayig CISI corpus cover many of the same
Mohenjo-daro inscriptions. Where they reference the same artefact (same M-number),
we can compare sign sequences to build a GLYPHID → P-number alignment.

Limitations:
  - Works only where sequences have equal length (direct 1:1 alignment)
  - Different sign-splitting decisions produce different sequence lengths
  - Result is partial and requires visual confirmation

Run from glossa-lab root:
    python scripts/build_yajnadevam_crosswalk.py

Outputs:
    crosswalks/yajnadevam_to_parpola_crosswalk.csv
    crosswalks/yajnadevam_crosswalk_stats.md
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL_PATH = ROOT / "data_raw" / "other_sites" / "yajnadevam_population.sql"
CISI_PATH = ROOT / "data" / "indus_cisi_corpus.json"
CROSSWALKS = ROOT / "crosswalks"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_cisi() -> dict[str, list[str]]:
    """Load CISI corpus → {M-number: [P-signs]}. Strips trailing 'A'/'B' from ID."""
    data = json.loads(CISI_PATH.read_text("utf-8"))
    corpus: dict[str, list[str]] = {}
    for insc in data:
        iid = insc.get("id", "")
        # M-165A → M-165, M-3B → M-3
        base = re.sub(r"[AB]$", "", iid)
        signs = [g["id"] for g in (insc.get("graphemes") or []) if g.get("id")]
        if signs:
            corpus[base] = signs
    return corpus


def parse_seal_glyphseq(sql: str) -> dict[str, tuple[str, list[int]]]:
    """
    Parse SQL → {external_id: (site_id, [glyph_ids])}
    Only for SI1 (Mohenjo-daro) seals with external M-numbers.
    """
    # Parse SEAL table
    seal_start = sql.find("INSERT INTO SEAL")
    seal_end = sql.find(";", seal_start)
    seal_block = sql[seal_start:seal_end]

    # Map seal_id → (site_id, external_id) for Mohenjo-daro seals
    seal_map: dict[int, tuple[str, str]] = {}
    for m in re.finditer(r'\((\d+),\s*"(SI\d+)",\s*"[^"]*",\s*"([^"]+)"', seal_block):
        seal_id = int(m.group(1))
        site_id = m.group(2)
        ext_id = m.group(3)
        if site_id == "SI1" and re.match(r"M-\d+$", ext_id):
            seal_map[seal_id] = (site_id, ext_id)

    # Parse INSCRIPTION table to get is_complete
    insc_start = sql.find("INSERT INTO INSCRIPTION")
    insc_end = sql.find(";", insc_start)
    insc_block = sql[insc_start:insc_end]
    inscribed: set[int] = set()
    for m in re.finditer(r'\((\d+),', insc_block):
        inscribed.add(int(m.group(1)))

    # Parse GLYPHSEQUENCE
    gs_start = sql.find("INSERT INTO GLYPHSEQUENCE")
    gs_end = sql.find(";", gs_start)
    gs_block = sql[gs_start:gs_end]
    sequences: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for m in re.finditer(r'\((\d+),(\d+),(\d+)\)', gs_block):
        seal_id, glyph_id, idx = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if seal_id in seal_map and seal_id in inscribed:
            sequences[seal_id].append((glyph_id, idx))

    # Build final dict: ext_id → glyph_id_list (sorted by idx)
    result: dict[str, tuple[str, list[int]]] = {}
    for seal_id, (site_id, ext_id) in seal_map.items():
        if seal_id in sequences:
            seq = sorted(sequences[seal_id], key=lambda x: x[1])
            result[ext_id] = (site_id, [g for g, _ in seq])

    return result


def build_crosswalk(
    cisi: dict[str, list[str]],
    yj: dict[str, tuple[str, list[int]]],
) -> list[dict]:
    """
    Align sequences for matching M-numbers and build G→P mappings.
    Alignment: only direct 1:1 when sequence lengths match exactly.
    """
    # Maps GLYPHID → {P-number: count}
    glyph_to_parpola: dict[int, Counter] = defaultdict(Counter)
    matched_inscriptions = 0
    length_matched = 0
    alignment_pairs: list[dict] = []

    for m_num, (site_id, yj_signs) in yj.items():
        cisi_signs = cisi.get(m_num)
        if not cisi_signs:
            continue
        matched_inscriptions += 1

        if len(yj_signs) == len(cisi_signs):
            length_matched += 1
            # Direct 1:1 alignment
            for glyph_id, p_sign in zip(yj_signs, cisi_signs):
                glyph_to_parpola[glyph_id][p_sign] += 1

    # Build crosswalk rows
    rows: list[dict] = []
    for glyph_id, counter in sorted(glyph_to_parpola.items()):
        total = sum(counter.values())
        top_p = counter.most_common(3)
        best_p, best_count = top_p[0]
        confidence = round(best_count / total, 4) if total else 0
        status = "confirmed" if confidence >= 0.8 else "pending_confirmation" if confidence >= 0.5 else "ambiguous"
        rows.append({
            "yajnadevam_glyph_id": glyph_id,
            "registry_sign_id_yajnadevam": f"Y{glyph_id:04d}",
            "best_parpola_match": best_p,
            "match_confidence": confidence,
            "match_count": best_count,
            "total_alignments": total,
            "top3_parpola": " | ".join(f"{p}:{c}" for p, c in top_p),
            "review_status": status,
            "method": "sequence_alignment_length_match",
            "source": "Yajnadevam indus-website + mayig CISI corpus alignment",
        })

    stats = {
        "matching_m_numbers": matched_inscriptions,
        "length_matched_pairs": length_matched,
        "glyph_ids_mapped": len(glyph_to_parpola),
        "alignment_pairs": alignment_pairs,
    }
    return rows, stats


def write_crosswalk(rows: list[dict]) -> Path:
    out = CROSSWALKS / "yajnadevam_to_parpola_crosswalk.csv"
    if not rows:
        print("No crosswalk rows to write")
        return out
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return out


def write_crosswalk_stats(rows: list[dict], stats: dict) -> Path:
    out = CROSSWALKS / "yajnadevam_crosswalk_stats.md"
    confirmed = sum(1 for r in rows if r["review_status"] == "confirmed")
    pending = sum(1 for r in rows if r["review_status"] == "pending_confirmation")
    ambiguous = sum(1 for r in rows if r["review_status"] == "ambiguous")

    lines = [
        "# Yajnadevam GLYPHID ↔ Parpola P-number Crosswalk — Statistics",
        f"Generated: {NOW}",
        "",
        "## Method",
        "Sequence alignment on shared Mohenjo-daro inscriptions.",
        "Both corpora reference the same physical artefacts by M-number.",
        "Where sequence lengths match exactly, signs are aligned 1:1.",
        "Where lengths differ, no alignment is attempted (length mismatch = different sign-splitting).",
        "",
        "## Coverage",
        f"- Matching M-numbers found: {stats['matching_m_numbers']}",
        f"- Pairs with matching sequence length (usable): {stats['length_matched_pairs']}",
        f"- Yajnadevam GLYPHIDs mapped to Parpola: {stats['glyph_ids_mapped']}",
        "",
        "## Confidence distribution",
        f"- Confirmed (confidence ≥ 0.80): {confirmed}",
        f"- Pending confirmation (0.50–0.79): {pending}",
        f"- Ambiguous (< 0.50): {ambiguous}",
        "",
        "## Top confirmed mappings",
        "",
    ]
    confirmed_rows = sorted(
        [r for r in rows if r["review_status"] == "confirmed"],
        key=lambda x: -x["match_confidence"]
    )[:30]
    for r in confirmed_rows:
        lines.append(
            f"  - Y{r['yajnadevam_glyph_id']:04d} → {r['best_parpola_match']} "
            f"(conf={r['match_confidence']}, n={r['match_count']}/{r['total_alignments']})"
        )

    lines += [
        "",
        "## Limitations",
        "- Only length-matched pairs are aligned; ~50% of overlapping inscriptions",
        "  have mismatched lengths (Yajnadevam collapses more variants than Parpola).",
        "- Visual confirmation against sign plates is required before treating any",
        "  mapping as definitive.",
        "- Ambiguous mappings (one Y-sign maps to multiple P-signs) indicate",
        "  a many-to-one or splitting difference between the two sign systems.",
        "",
        "## Next Step",
        "Use confirmed mappings to re-label Yajnadevam Y-numbers with P-numbers",
        "in the combined corpus_master.csv, enabling unified cross-site analysis.",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> None:
    print("=" * 60)
    print("Task 1: Yajnadevam Y↔P Crosswalk Builder")
    print("=" * 60)

    print("\nLoading CISI corpus (Parpola P-numbers)...")
    cisi = load_cisi()
    print(f"  {len(cisi)} inscriptions with P-numbers")

    print("Parsing Yajnadevam SQL (GLYPHIDs for Mohenjo-daro M-numbered seals)...")
    sql = SQL_PATH.read_text("utf-8", errors="replace")
    yj = parse_seal_glyphseq(sql)
    print(f"  {len(yj)} Mohenjo-daro inscriptions with M-number external IDs")

    print("Building crosswalk via sequence alignment...")
    rows, stats = build_crosswalk(cisi, yj)
    print(f"  Matching M-numbers: {stats['matching_m_numbers']}")
    print(f"  Length-matched pairs: {stats['length_matched_pairs']}")
    print(f"  GLYPH IDs mapped: {stats['glyph_ids_mapped']}")

    out = write_crosswalk(rows)
    stats_out = write_crosswalk_stats(rows, stats)

    print(f"\nOutputs:")
    print(f"  {out}")
    print(f"  {stats_out}")

    confirmed = sum(1 for r in rows if r["review_status"] == "confirmed")
    print(f"\nConfirmed mappings (confidence ≥ 0.80): {confirmed}")
    print("NOTE: All mappings require visual confirmation against sign plates.")


if __name__ == "__main__":
    main()
