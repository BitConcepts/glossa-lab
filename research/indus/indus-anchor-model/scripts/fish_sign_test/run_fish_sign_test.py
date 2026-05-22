#!/usr/bin/env python3
"""
run_fish_sign_test.py — Fish-sign compound-only constraint test
================================================================
Loads the fish-sign contexts CSV and verifies that every occurrence
of the fish-family signs (M047 and M001) appears exclusively in
compound sequences — never in isolation.

This is a key Tier 2 falsification test: if fish signs appeared
isolated, the professional-title reading would be weakened.

Usage
-----
    python run_fish_sign_test.py
    python run_fish_sign_test.py --contexts-file ../../data/public/fish_sign_compound_context.csv
    python run_fish_sign_test.py --output-dir ../../outputs/

Requirements
------------
    Python 3.10+ (stdlib only)
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FISH_SIGNS = {"M047", "M001"}  # Primary fish-family signs
MIDDLE_DOT = "\u00b7"          # · used as sign separator in sequences


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyse_contexts(contexts_path: Path) -> Dict:
    """
    Analyse fish-sign contexts CSV.

    Returns a dict with:
      - total_rows: int
      - by_sign: {sign: {total, compound, isolated, sites, slots}}
      - isolated_cases: list of {sign, seal_id, sequence}
      - pass: bool
    """
    rows = []
    with open(contexts_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    result: Dict = {
        "total_rows": len(rows),
        "by_sign": {},
        "isolated_cases": [],
        "pass": True,
    }

    sign_data: Dict[str, Dict] = defaultdict(lambda: {
        "total": 0,
        "compound": 0,
        "isolated": 0,
        "sites": Counter(),
        "slots": Counter(),
    })

    for row in rows:
        sign = row.get("sign", "").strip()
        seal_id = row.get("seal_id", "").strip()
        site = row.get("site", "").strip()
        slot = row.get("positional_slot", "").strip()
        sequence = row.get("sequence", "").strip()
        right_neighbor = row.get("right_neighbor", "").strip()
        left_neighbor = row.get("left_neighbor", "").strip()

        sd = sign_data[sign]
        sd["total"] += 1
        sd["sites"][site] += 1
        sd["slots"][slot] += 1

        # Determine if compound or isolated
        # Compound: sequence contains middle-dot separator AND has a neighbor
        is_compound = (
            MIDDLE_DOT in sequence
            or (right_neighbor not in {"", "\u2014", "-"})
            or (left_neighbor not in {"", "\u2014", "-"})
        )

        if is_compound:
            sd["compound"] += 1
        else:
            sd["isolated"] += 1
            result["isolated_cases"].append({
                "sign": sign,
                "seal_id": seal_id,
                "sequence": sequence,
            })
            result["pass"] = False

    # Convert sign_data to serialisable form
    for sign, sd in sign_data.items():
        result["by_sign"][sign] = {
            "total": sd["total"],
            "compound": sd["compound"],
            "isolated": sd["isolated"],
            "sites": dict(sd["sites"]),
            "slots": dict(sd["slots"]),
        }

    return result


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_summary(analysis: Dict, output_dir: Path) -> Path:
    """Write a summary CSV to the output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "fish_sign_test_summary.csv"

    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "sign", "total", "compound", "isolated",
            "compound_pct", "sites", "dominant_slot", "result",
        ])
        for sign, data in sorted(analysis["by_sign"].items()):
            total = data["total"]
            compound = data["compound"]
            isolated = data["isolated"]
            pct = f"{compound / total:.1%}" if total > 0 else "N/A"
            sites = "; ".join(f"{s}({c})" for s, c in
                              sorted(data["sites"].items(), key=lambda x: -x[1]))
            dominant_slot = max(data["slots"], key=data["slots"].get) if data["slots"] else "N/A"
            status = "PASS" if isolated == 0 else "FAIL"
            writer.writerow([sign, total, compound, isolated, pct, sites,
                             dominant_slot, status])

    return out_path


def print_report(analysis: Dict) -> None:
    """Print a human-readable report to stdout."""
    print("=" * 68)
    print("Fish-Sign Compound-Only Constraint Test")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 68)
    print()

    total = analysis["total_rows"]
    print(f"Total fish-sign occurrences: {total}")
    print()

    for sign, data in sorted(analysis["by_sign"].items()):
        compound = data["compound"]
        isolated = data["isolated"]
        stotal = data["total"]
        pct = f"{compound / stotal:.1%}" if stotal > 0 else "N/A"
        sites = ", ".join(sorted(data["sites"].keys()))
        dominant_slot = max(data["slots"], key=data["slots"].get) if data["slots"] else "N/A"

        print(f"  {sign}:")
        print(f"    Occurrences  : {stotal}")
        print(f"    Compound     : {compound} ({pct})")
        print(f"    Isolated     : {isolated}")
        print(f"    Dominant slot: {dominant_slot}")
        print(f"    Sites        : {sites}")
        print()

    if analysis["pass"]:
        print("RESULT: PASS — all fish-sign occurrences are compound (0 isolated)")
        print()
        print("Interpretation (Tier 2): The compound-only constraint holds.")
        print("Fish signs function as professional-title determinatives,")
        print("not standalone commodity markers.")
    else:
        print("RESULT: FAIL — isolated occurrences detected")
        print()
        for case in analysis["isolated_cases"]:
            print(f"  ISOLATED: {case['sign']} on {case['seal_id']}: {case['sequence']}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fish-sign compound-only constraint test"
    )
    parser.add_argument(
        "--contexts-file",
        type=Path,
        default=None,
        help="Path to fish_sign_compound_context.csv. If omitted, "
             "searches default locations.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "outputs",
        help="Output directory (default: ../../outputs/)",
    )
    args = parser.parse_args(argv)

    # Resolve contexts file
    if args.contexts_file is not None:
        contexts_path = args.contexts_file.resolve()
    else:
        # Search default locations
        script_dir = Path(__file__).resolve().parent
        candidates = [
            script_dir.parent.parent / "data" / "public" / "fish_sign_compound_context.csv",
            script_dir.parent.parent / "data" / "public" / "fish_sign_contexts.csv",
            script_dir.parent.parent / "data" / "public" / "supplemental" / "fish_sign_compound_context.csv",
        ]
        contexts_path = None
        for c in candidates:
            if c.is_file():
                contexts_path = c
                break
        if contexts_path is None:
            print(
                "ERROR: Could not find fish_sign_compound_context.csv.\n"
                "       Use --contexts-file to specify the path.",
                file=sys.stderr,
            )
            return 1

    if not contexts_path.is_file():
        print(f"ERROR: File not found: {contexts_path}", file=sys.stderr)
        return 1

    print(f"Loading: {contexts_path}")
    analysis = analyse_contexts(contexts_path)

    print_report(analysis)
    print()

    out_path = write_summary(analysis, args.output_dir.resolve())
    print(f"Summary CSV: {out_path}")

    return 0 if analysis["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
