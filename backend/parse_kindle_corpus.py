"""Parse the Kindle TXT exports of Fuls (2023) and reconstruct the ICIT corpus.

Inputs:
  A Catalog of Indus Signs.txt   — Chapter 5, statistical data per sign
  Corpus of Indus Inscriptions.txt — Chapter 3, inscription catalog

Output:
  reports/icit_extracted_corpus.json   — per-inscription sign sequences
  reports/icit_sign_stats.json         — per-sign stats with ICIT IDs
  reports/icit_corpus_summary.json     — summary statistics

Method:
  1. Parse Catalog: extract sign_id -> {total, terminal, medial, initial, solo,
     terminal_rate, initial_rate, icit_ids} for all 713 signs.
  2. Invert: icit_id -> [sign_ids that appear in it] (unordered set).
  3. Parse Corpus: icit_id -> {cisi, type, site, direction, n_lines, complete}
     (each row = one sign position, so n_rows per ICIT_ID = inscription length).
  4. Reconcile lengths: if Corpus says inscription N has k lines, keep only
     the k signs from the Catalog inversion.
  5. Order probabilistically using terminal_rate / initial_rate:
       - highest initial_rate  -> position 0
       - highest terminal_rate -> position -1
       - remainder sorted by terminal_rate ascending (medial)
  6. Write as JSON and as flat text corpus for Glossa Lab import.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

_CATALOG_PATH = Path(
    r"C:\Users\trist\OneDrive\Documents\My Kindle Content\A Catalog of Indus Signs.txt"
)
_CORPUS_PATH = Path(
    r"C:\Users\trist\OneDrive\Documents\My Kindle Content\Corpus of Indus Inscriptions.txt"
)
_OUT_DIR = Path(__file__).parent.parent / "reports"


# ── Step 1: Parse Catalog ─────────────────────────────────────────────


def parse_catalog(path: Path) -> dict[str, dict]:
    """Return dict: sign_id_str -> stats dict."""
    text = path.read_text(encoding="utf-8", errors="replace")
    sign_blocks = re.split(r"\nSign\s+(\d+)\s*\n", text)

    signs: dict[str, dict] = {}
    # sign_blocks: [preamble, sign_id_1, block_1, sign_id_2, block_2, ...]
    for i in range(1, len(sign_blocks) - 1, 2):
        sign_id = sign_blocks[i].strip()
        block = sign_blocks[i + 1]

        # Extract T/M/I/Solo from "Class Set Total Terminal Medial Initial Solo"
        tm_match = re.search(
            r"(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", block
        )
        total = terminal = medial = initial = solo = 0
        if tm_match:
            total = int(tm_match.group(3))
            terminal = int(tm_match.group(4))
            medial = int(tm_match.group(5))
            initial = int(tm_match.group(6))
            solo = int(tm_match.group(7))

        # Extract ICIT IDs — greedy match on digits/commas/whitespace only;
        # naturally stops at first non-digit (period, letter, etc.)
        icit_match = re.search(r"ICIT ID:\s*([\d,\n\r ]+)", block)
        icit_ids: list[int] = []
        if icit_match:
            raw = icit_match.group(1).replace("\n", " ").strip()
            icit_ids = [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]

        t_rate = terminal / total if total > 0 else 0.0
        i_rate = initial / total if total > 0 else 0.0
        s_rate = solo / total if total > 0 else 0.0

        signs[sign_id] = {
            "sign_id": sign_id,
            "total": total,
            "terminal": terminal,
            "medial": medial,
            "initial": initial,
            "solo": solo,
            "terminal_rate": round(t_rate, 4),
            "initial_rate": round(i_rate, 4),
            "solo_rate": round(s_rate, 4),
            "icit_ids": icit_ids,
        }

    return signs


# ── Step 2: Invert to ICIT_ID -> sign_set ─────────────────────────────


def build_icit_sign_map(signs: dict[str, dict]) -> dict[int, list[str]]:
    """Return dict: icit_id -> [sign_ids] (unordered)."""
    icit_to_signs: dict[int, list[str]] = defaultdict(list)
    for sign_id, data in signs.items():
        for icit_id in data["icit_ids"]:
            icit_to_signs[icit_id].append(sign_id)
    return dict(icit_to_signs)


# ── Step 3: Parse Corpus metadata ─────────────────────────────────────


def parse_corpus(path: Path) -> dict[int, dict]:
    """Return dict: icit_id -> {cisi, type, site, direction, n_positions, complete}."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    corpus: dict[int, dict] = {}
    site = "Unknown"

    # Detect site headings like "3.26. HARAPPA 137" (section header with page number)
    site_re = re.compile(
        r"^\d+\.\d+\.\s+([A-Z][A-Z\s\-]+?)\s*\d*\s*$"
    )
    # Each inscription row: "856 H-2219 R/L None"
    row_re = re.compile(r"^(\d+)\s+([\w\-]+|-)\s+(R/L|L/R|NR|-)\s+(\S+)\s*$")
    # Type row: "TAB:I Y None" or "SEAL:S N -"
    type_re = re.compile(r"^(SEAL:\w+|TAB:\w+|POT:\w+|MISC)\s*([YN?]?)\s*(\S*)\s*$")

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Update site
        sm = site_re.match(line)
        if sm:
            s = sm.group(1) or sm.group(2)
            if s:
                site = s.strip().title()
            i += 1
            continue

        # Inscription row
        rm = row_re.match(line)
        if rm:
            icit_id = int(rm.group(1))
            cisi = rm.group(2)
            direction = rm.group(3)

            if icit_id not in corpus:
                corpus[icit_id] = {
                    "icit_id": icit_id,
                    "cisi": cisi,
                    "direction": direction,
                    "site": site,
                    "type": "",
                    "complete": "",
                    "n_positions": 0,
                }
            corpus[icit_id]["n_positions"] += 1

            # Find the type on the next non-blank line
            if not corpus[icit_id]["type"]:
                for look in range(1, 4):
                    if i + look >= len(lines):
                        break
                    next_line = lines[i + look].strip()
                    if not next_line:
                        continue
                    tm = type_re.match(next_line)
                    if tm:
                        corpus[icit_id]["type"] = tm.group(1)
                        corpus[icit_id]["complete"] = tm.group(2)
                    break
            i += 1
            continue

        i += 1

    return corpus


# ── Step 4+5: Reconstruct ordered sequences ───────────────────────────


def reconstruct_sequences(
    icit_sign_map: dict[int, list[str]],
    corpus_meta: dict[int, dict],
    signs: dict[str, dict],
) -> list[dict]:
    """Build ordered inscription sequences using positional probabilities."""
    inscriptions = []

    all_icit = set(icit_sign_map.keys()) | set(corpus_meta.keys())

    for icit_id in sorted(all_icit):
        sign_set = icit_sign_map.get(icit_id, [])
        meta = corpus_meta.get(icit_id, {"site": "Unknown", "type": "", "n_positions": 0})

        if not sign_set:
            continue  # No sign data for this inscription

        # Deduplicate signs — each sign appears at most once per inscription
        seen: set[str] = set()
        unique_signs = []
        for s in sign_set:
            if s not in seen:
                seen.add(s)
                unique_signs.append(s)

        if len(unique_signs) == 1:
            ordered = unique_signs
        else:
            # Sort by initial_rate desc to build positional ordering
            # High initial_rate -> front; high terminal_rate -> back
            def _score(s: str) -> tuple[float, float]:
                d = signs.get(s, {})
                return (d.get("initial_rate", 0.0), -d.get("terminal_rate", 0.0))

            # Sort: most initial-dominant first
            sorted_by_initial = sorted(
                unique_signs, key=lambda s: signs.get(s, {}).get("initial_rate", 0), reverse=True
            )
            # Sort: most terminal-dominant last
            sorted_by_terminal = sorted(
                unique_signs, key=lambda s: signs.get(s, {}).get("terminal_rate", 0)
            )

            if len(unique_signs) == 2:
                # Simple: highest initial_rate first
                ordered = sorted_by_initial
            else:
                # Interleave: front = highest initial, back = highest terminal,
                # middle = remainder sorted by medial rate (lowest boundary bias)
                first = sorted_by_initial[0]
                last = sorted_by_terminal[-1]
                middle = [s for s in unique_signs if s != first and s != last]
                middle.sort(
                    key=lambda s: signs.get(s, {}).get("terminal_rate", 0) +
                    signs.get(s, {}).get("initial_rate", 0)
                )
                ordered = [first] + middle + [last]

        inscriptions.append({
            "icit_id": icit_id,
            "sequence": ordered,
            "length": len(ordered),
            "site": meta.get("site", "Unknown"),
            "type": meta.get("type", ""),
            "complete": meta.get("complete", ""),
            "direction": meta.get("direction", ""),
            "cisi": meta.get("cisi", ""),
        })

    return inscriptions


# ── Main ──────────────────────────────────────────────────────────────


def main() -> None:
    print("[1/5] Parsing Catalog of Indus Signs...")
    if not _CATALOG_PATH.exists():
        print(f"ERROR: Catalog not found at {_CATALOG_PATH}")
        sys.exit(1)
    signs = parse_catalog(_CATALOG_PATH)
    print(f"      {len(signs)} signs parsed")

    print("[2/5] Building ICIT ID → sign set mapping...")
    icit_sign_map = build_icit_sign_map(signs)
    print(f"      {len(icit_sign_map)} inscription IDs found in Catalog")

    corpus_meta: dict[int, dict] = {}
    if _CORPUS_PATH.exists():
        print("[3/5] Parsing Corpus of Indus Inscriptions...")
        corpus_meta = parse_corpus(_CORPUS_PATH)
        print(f"      {len(corpus_meta)} inscription records parsed")
    else:
        print("[3/5] Corpus file not found — skipping metadata")

    print("[4/5] Reconstructing ordered sequences...")
    inscriptions = reconstruct_sequences(icit_sign_map, corpus_meta, signs)
    print(f"      {len(inscriptions)} inscriptions reconstructed")

    # Summary stats
    lengths = [ins["length"] for ins in inscriptions]
    total_tokens = sum(lengths)
    sites = {}
    for ins in inscriptions:
        sites[ins["site"]] = sites.get(ins["site"], 0) + 1
    types = {}
    for ins in inscriptions:
        t = ins["type"]
        types[t] = types.get(t, 0) + 1

    summary = {
        "n_inscriptions": len(inscriptions),
        "total_sign_tokens": total_tokens,
        "n_signs": len(signs),
        "mean_inscription_length": round(total_tokens / max(len(inscriptions), 1), 2),
        "max_inscription_length": max(lengths) if lengths else 0,
        "sites": dict(sorted(sites.items(), key=lambda x: -x[1])[:20]),
        "object_types": dict(sorted(types.items(), key=lambda x: -x[1])[:10]),
        "method": (
            "Sequences reconstructed from Catalog ICIT_ID lists. "
            "Sign ordering is probabilistic (initial_rate -> first, terminal_rate -> last). "
            "True ordering requires the full Corpus text layer (PDF recommended)."
        ),
    }

    print("[5/5] Saving results...")
    _OUT_DIR.mkdir(exist_ok=True)

    (_OUT_DIR / "icit_sign_stats.json").write_text(
        json.dumps(signs, indent=2), encoding="utf-8"
    )
    (_OUT_DIR / "icit_extracted_corpus.json").write_text(
        json.dumps({"summary": summary, "inscriptions": inscriptions}, indent=2),
        encoding="utf-8",
    )
    (_OUT_DIR / "icit_corpus_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    # Flat text corpus for Glossa Lab: one inscription per line, signs space-separated
    flat_lines = [" ".join(ins["sequence"]) for ins in inscriptions if ins["sequence"]]
    (_OUT_DIR / "icit_corpus_flat.txt").write_text(
        "\n".join(flat_lines), encoding="utf-8"
    )

    print()
    print("=== ICIT Corpus Reconstruction Results ===")
    print(f"  Inscriptions:    {summary['n_inscriptions']:,}")
    print(f"  Sign tokens:     {summary['total_sign_tokens']:,}")
    print(f"  Mean length:     {summary['mean_inscription_length']}")
    print(f"  Unique signs:    {summary['n_signs']}")
    print()
    print("  Top sites:")
    for site, count in list(summary["sites"].items())[:8]:
        print(f"    {site:<30} {count:>5}")
    print()
    print("  Object types:")
    for otype, count in list(summary["object_types"].items())[:6]:
        print(f"    {otype:<20} {count:>5}")
    print()
    print(f"  Saved to: {_OUT_DIR}")
    print()
    print("  NOTE: Sign ordering is probabilistic, not ground-truth.")
    print("  Re-run with PDF corpus to get true sign sequences.")


if __name__ == "__main__":
    main()
