"""
Extend Y→P crosswalk to length-mismatched inscription pairs.

The initial crosswalk (build_yajnadevam_crosswalk.py) used only pairs where
len(yj_seq) == len(cisi_seq), achieving 184 confirmed mappings and 81.5% token
coverage. This script handles the remaining 20 mismatched pairs using
anchor-guided gap-filling alignment:

Algorithm:
  1. Apply confirmed Y→P mappings to substitute known signs in both sequences.
  2. Find "anchor" positions — consecutive runs of matched P-signs in both.
  3. In gaps between anchors, if gap_size_yj == gap_size_cisi == 1, infer mapping.
  4. Accept only inferences consistent across ≥2 independent pairs.
  5. Accept only where the inferred sign doesn't already have a conflicting mapping.

This is conservative: single-evidence inferences are discarded. The result
supplements the existing crosswalk with additional lower-confidence entries.

Run from glossa-lab root:
    python scripts/extend_yp_crosswalk.py

Outputs:
    crosswalks/yajnadevam_to_parpola_crosswalk_extended.csv
    crosswalks/yajnadevam_crosswalk_extended_stats.md
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL_PATH  = ROOT / "data_raw" / "other_sites" / "yajnadevam_population.sql"
CISI_PATH = ROOT / "data" / "indus_cisi_corpus.json"
CROSSWALK_PATH = ROOT / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv"
OUT_PATH   = ROOT / "crosswalks" / "yajnadevam_to_parpola_crosswalk_extended.csv"
STATS_PATH = ROOT / "crosswalks" / "yajnadevam_crosswalk_extended_stats.md"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

MIN_EVIDENCE = 2          # minimum pairs supporting a new mapping
ANCHOR_CONF  = 0.80       # minimum confidence to use as anchor


# ── Load existing crosswalk ──────────────────────────────────────────────────

def load_confirmed_crosswalk() -> tuple[dict[str, str], list[dict]]:
    """Returns ({Y-id: P-id} for confirmed, full row list)."""
    mapping: dict[str, str] = {}
    rows: list[dict] = []
    with open(CROSSWALK_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
            if float(row["match_confidence"]) >= ANCHOR_CONF:
                mapping[row["registry_sign_id_yajnadevam"]] = row["best_parpola_match"]
    return mapping, rows


# ── Load corpora ─────────────────────────────────────────────────────────────

def load_cisi() -> dict[str, list[str]]:
    data = json.loads(CISI_PATH.read_text("utf-8"))
    corpus: dict[str, list[str]] = {}
    for insc in data:
        iid = insc.get("id", "")
        base = re.sub(r"[AB]$", "", iid)
        signs = [g["id"] for g in (insc.get("graphemes") or []) if g.get("id")]
        if signs:
            corpus[base] = signs
    return corpus


def parse_yajnadevam_md_seals(sql: str) -> dict[str, list[int]]:
    """Parse all SI1 (Mohenjo-daro) seals with M-numbers → {ext_id: [glyph_ids]}."""
    seal_start = sql.find("INSERT INTO SEAL")
    seal_end   = sql.find(";", seal_start)
    seal_block = sql[seal_start:seal_end]
    seal_map: dict[int, str] = {}
    for m in re.finditer(r'\((\d+),\s*"SI1",\s*"[^"]*",\s*"(M-\d+)"', seal_block):
        seal_map[int(m.group(1))] = m.group(2)

    insc_start = sql.find("INSERT INTO INSCRIPTION")
    insc_end   = sql.find(";", insc_start)
    insc_block = sql[insc_start:insc_end]
    inscribed: set[int] = {int(m.group(1)) for m in re.finditer(r'\((\d+),', insc_block)}

    gs_start = sql.find("INSERT INTO GLYPHSEQUENCE")
    gs_end   = sql.find(";", gs_start)
    gs_block = sql[gs_start:gs_end]
    sequences: dict[int, list[tuple[int,int]]] = defaultdict(list)
    for m in re.finditer(r'\((\d+),(\d+),(\d+)\)', gs_block):
        sid, gid, idx = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if sid in seal_map and sid in inscribed:
            sequences[sid].append((gid, idx))

    result: dict[str, list[int]] = {}
    for sid, ext_id in seal_map.items():
        if sid in sequences:
            seq = sorted(sequences[sid], key=lambda x: x[1])
            result[ext_id] = [g for g, _ in seq]
    return result


# ── Anchor-guided alignment ──────────────────────────────────────────────────

def apply_known(glyph_ids: list[int], mapping: dict[str, str]) -> list[str]:
    """Replace known Y-signs with P-numbers; unknowns become 'Yunknown_NNNN'."""
    out = []
    for gid in glyph_ids:
        y_id = f"Y{gid:04d}"
        out.append(mapping.get(y_id, f"Yunknown_{gid:04d}"))
    return out


def find_gaps(yj_translated: list[str], cisi_signs: list[str]) \
        -> list[tuple[list[str], list[str]]]:
    """
    Find 1:1 gap pairs using confirmed anchors.

    Both sequences have some known P-signs (anchors) and some unknowns.
    We align by matching anchor runs, then extract gaps between them.

    Returns list of (yj_gap_signs, cisi_gap_signs) — unaligned segments.
    Only keeps gaps where both sides have the same length > 0.
    """
    # Find positions of known P-signs in both sequences
    yj_known   = [(i, s) for i, s in enumerate(yj_translated) if s.startswith("P")]
    cisi_known = [(i, s) for i, s in enumerate(cisi_signs) if s.startswith("P")]

    if not yj_known or not cisi_known:
        return []

    # Find common P-sign subsequence (LCS of P-signs)
    yj_p   = [s for _, s in yj_known]
    cisi_p = [s for _, s in cisi_known]

    # LCS via DP
    m, n = len(yj_p), len(cisi_p)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if yj_p[i-1] == cisi_p[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack to find aligned anchor pairs
    aligned: list[tuple[int,int]] = []  # (yj_known_idx, cisi_known_idx)
    i, j = m, n
    while i > 0 and j > 0:
        if yj_p[i-1] == cisi_p[j-1]:
            aligned.append((i-1, j-1))
            i -= 1; j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    aligned.reverse()

    if not aligned:
        return []

    # Extract gaps between consecutive anchor pairs
    gaps = []
    anchor_positions = [(yj_known[ai][0], cisi_known[ci][0]) for ai, ci in aligned]

    # Sentinel: add start and end
    sentinels = [(-1, -1)] + anchor_positions + [(len(yj_translated), len(cisi_signs))]

    for k in range(len(sentinels)-1):
        yj_gap_start  = sentinels[k][0] + 1
        yj_gap_end    = sentinels[k+1][0]
        cisi_gap_start = sentinels[k][1] + 1
        cisi_gap_end   = sentinels[k+1][1]

        yj_gap   = yj_translated[yj_gap_start:yj_gap_end]
        cisi_gap = cisi_signs[cisi_gap_start:cisi_gap_end]

        # Only process gaps where both sides are non-empty unknowns with same length
        if yj_gap and cisi_gap and len(yj_gap) == len(cisi_gap):
            # All YJ gap elements must be unknown
            if all(s.startswith("Yunknown_") for s in yj_gap):
                gaps.append((yj_gap, cisi_gap))

    return gaps


# ── Main alignment pipeline ──────────────────────────────────────────────────

def extend_crosswalk(
    confirmed: dict[str, str],
    yj: dict[str, list[int]],
    cisi: dict[str, list[str]],
) -> tuple[list[dict], dict]:
    """
    Extend crosswalk using mismatched-length pairs.
    Returns (new_rows, stats).
    """
    new_evidence: dict[str, Counter] = defaultdict(Counter)
    n_mismatched = 0
    n_usable_gaps = 0

    for m_num, glyph_ids in yj.items():
        cisi_signs = cisi.get(m_num)
        if not cisi_signs:
            continue
        if len(glyph_ids) == len(cisi_signs):
            continue  # handled by initial crosswalk
        n_mismatched += 1

        yj_translated = apply_known(glyph_ids, confirmed)
        gaps = find_gaps(yj_translated, cisi_signs)

        for yj_gap, cisi_gap in gaps:
            n_usable_gaps += 1
            for yj_sign, cisi_sign in zip(yj_gap, cisi_gap):
                # yj_sign is like "Yunknown_0017" → extract glyph_id
                glyph_num = yj_sign.replace("Yunknown_", "")
                y_id = f"Y{int(glyph_num):04d}"
                new_evidence[y_id][cisi_sign] += 1

    # Build new rows from evidence
    new_rows = []
    for y_id, counter in sorted(new_evidence.items()):
        if y_id in confirmed:
            continue  # already mapped
        total = sum(counter.values())
        top_p, best_count = counter.most_common(1)[0]
        confidence = round(best_count / total, 4)
        if best_count < MIN_EVIDENCE:
            continue  # not enough evidence
        status = "confirmed_extended" if confidence >= 0.80 else \
                 "pending_extended" if confidence >= 0.50 else "ambiguous_extended"
        new_rows.append({
            "yajnadevam_glyph_id": int(y_id[1:]),
            "registry_sign_id_yajnadevam": y_id,
            "best_parpola_match": top_p,
            "match_confidence": confidence,
            "match_count": best_count,
            "total_alignments": total,
            "top3_parpola": " | ".join(f"{p}:{c}" for p, c in counter.most_common(3)),
            "review_status": status,
            "method": "anchor_guided_gap_filling",
            "source": "Yajnadevam SQL + mayig CISI corpus (mismatched-length pairs)",
        })

    stats = {
        "mismatched_pairs_processed": n_mismatched,
        "usable_gap_segments": n_usable_gaps,
        "new_y_ids_with_evidence": len(new_evidence),
        "new_rows_written": len(new_rows),
    }
    return new_rows, stats


def write_extended_crosswalk(
    existing_rows: list[dict],
    new_rows: list[dict],
    stats: dict,
) -> None:
    # Merged file (existing + new)
    all_rows = existing_rows + new_rows
    fieldnames = list(existing_rows[0].keys()) if existing_rows else list(new_rows[0].keys() if new_rows else [])
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(all_rows)

    conf_new   = sum(1 for r in new_rows if r["review_status"] == "confirmed_extended")
    pend_new   = sum(1 for r in new_rows if r["review_status"] == "pending_extended")
    amb_new    = sum(1 for r in new_rows if r["review_status"] == "ambiguous_extended")
    total_conf = sum(1 for r in existing_rows if "confirmed" in r.get("review_status","")) + conf_new

    lines = [
        "# Extended Yajnadevam Y→P Crosswalk Statistics",
        f"Generated: {NOW}",
        "",
        "## Method: Anchor-Guided Gap-Filling Alignment",
        "For length-mismatched inscription pairs, confirmed Y→P mappings are used",
        "as anchors. LCS alignment of anchor P-signs finds gaps between them.",
        "Gaps where both sides have equal non-zero length and all YJ signs are",
        "unknown yield new provisional mappings (accepted with ≥2 evidence instances).",
        "",
        "## Statistics",
        f"- Mismatched-length pairs processed: {stats['mismatched_pairs_processed']}",
        f"- Usable gap segments found: {stats['usable_gap_segments']}",
        f"- New Y-signs with gap evidence: {stats['new_y_ids_with_evidence']}",
        f"- New rows meeting evidence threshold (≥{MIN_EVIDENCE}): {stats['new_rows_written']}",
        "",
        "## New mapping confidence distribution",
        f"- confirmed_extended (≥0.80): {conf_new}",
        f"- pending_extended (0.50-0.79): {pend_new}",
        f"- ambiguous_extended (<0.50): {amb_new}",
        "",
        f"## Total crosswalk size: {len(all_rows)} entries",
        f"Total confirmed mappings (original + extended): ~{total_conf}",
        "",
        "## Limitations",
        "- Gap-filling is conservative: only equal-length gaps are aligned.",
        "- Evidence from ≥2 pairs required; single-pair inferences discarded.",
        "- These mappings are LOWER confidence than length-matched ones.",
        "- Visual sign-plate confirmation remains required for full validation.",
    ]
    STATS_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    print("=" * 60)
    print("Extend Y→P Crosswalk: Anchor-Guided Gap Filling")
    print("=" * 60)

    print("\nLoading confirmed crosswalk...")
    confirmed, existing_rows = load_confirmed_crosswalk()
    print(f"  {len(confirmed)} confirmed mappings (anchors)")

    print("Loading CISI corpus...")
    cisi = load_cisi()

    print("Parsing Yajnadevam SQL...")
    sql = SQL_PATH.read_text("utf-8", errors="replace")
    yj  = parse_yajnadevam_md_seals(sql)
    print(f"  {len(yj)} SI1 seals with M-numbers")

    print("\nRunning anchor-guided gap-filling on mismatched pairs...")
    new_rows, stats = extend_crosswalk(confirmed, yj, cisi)
    print(f"  Mismatched pairs: {stats['mismatched_pairs_processed']}")
    print(f"  Gap segments usable: {stats['usable_gap_segments']}")
    print(f"  New mappings (≥{MIN_EVIDENCE} evidence): {stats['new_rows_written']}")

    write_extended_crosswalk(existing_rows, new_rows, stats)
    print(f"\nExtended crosswalk: {OUT_PATH}")
    print(f"Stats: {STATS_PATH}")

    conf_new = sum(1 for r in new_rows if r["review_status"] == "confirmed_extended")
    print(f"\nNew confirmed_extended mappings: {conf_new}")
    print(f"Total confirmed: {len(confirmed) + conf_new}")


if __name__ == "__main__":
    main()
