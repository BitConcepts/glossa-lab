"""Extract a compact subset of ePSD2 names for glossa-lab Phase-29.

Source: oracc.museum.upenn.edu/json/epsd2-names.zip (gloss-qpn.json, 37 MB)
Output: backend/glossa_lab/data/epsd2_names_subset.json (~ 1 MB)

We keep:
  - headword (e.g. "A.KU[1]DN")
  - id (Oracc ID, e.g. "x000024750")
  - pos (PN/DN/SN/GN/RN/MN/TN/WN — Personal/Divine/Settlement/Geographic/...)
  - icount (instance count)
  - dc_title (full glossary path)
  - cf (citation form)
  - sigs (CDLI-compatible sign-cuneiform-form, where available)
  - forms (alternate writings)
  - periods (when the name is attested)

We drop instances (the ~50k individual occurrences) and morphological details — these
can be re-fetched live from Oracc if needed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "corpora" / "downloads" / "indus_corpus_expansion" / "epsd2_names_extracted" / "epsd2" / "names" / "gloss-qpn.json"
OUT = REPO / "backend" / "glossa_lab" / "data" / "epsd2_names_subset.json"


def main() -> None:
    if not SOURCE.exists():
        print(f"ERROR: {SOURCE} not found. Download epsd2-names.zip from "
              "oracc.museum.upenn.edu/json/ first.", file=sys.stderr)
        sys.exit(1)
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    entries = data.get("entries") or []
    print(f"Read {len(entries)} entries from {SOURCE.name}")

    by_pos: dict[str, list[dict]] = {}
    compact: list[dict] = []
    for e in entries:
        pos = e.get("pos", "?")
        forms = e.get("forms") or []
        form_list: list[str] = []
        for f in forms:
            n = f.get("n") or f.get("form") or ""
            if n and n not in form_list:
                form_list.append(n)
        periods: list[str] = []
        for p in (e.get("periods") or []):
            pn = p.get("p") or p.get("period") or ""
            if pn and pn not in periods:
                periods.append(pn)

        rec = {
            "headword": e.get("headword", ""),
            "id": e.get("id", ""),
            "pos": pos,
            "icount": int(e.get("icount", 0) or 0),
            "cf": e.get("cf", ""),
            "forms": form_list[:10],   # cap at 10 alternate writings
            "periods": periods[:8],
        }
        compact.append(rec)
        by_pos.setdefault(pos, []).append(rec)

    summary = {p: len(by_pos[p]) for p in sorted(by_pos)}
    print("Counts by POS:")
    for p, c in sorted(summary.items(), key=lambda x: -x[1]):
        print(f"  {p:>4s} : {c}")

    out = {
        "_doc": ("ePSD2 names subset — Sumerian/Akkadian PNs/DNs/etc. for the "
                  "glossa-lab Indus decipherment Phase-29. Source: "
                  "oracc.museum.upenn.edu, ePSD2/names project (CC BY-SA)."),
        "_source": "https://oracc.museum.upenn.edu/json/epsd2-names.zip",
        "_license": "CC BY-SA",
        "_n_total_entries": len(compact),
        "_pos_counts": summary,
        "_pos_legend": {
            "PN": "Personal Name",
            "DN": "Divine Name",
            "SN": "Settlement Name",
            "GN": "Geographic Name",
            "RN": "Royal Name",
            "MN": "Month Name",
            "TN": "Temple Name",
            "WN": "Watercourse Name",
            "CN": "Constellation Name",
        },
        "entries": compact,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
