"""Phase-17: measure language-signature DoFs on the DAMOS Mycenaean (Linear B)
corpus, completing the Aegean reference-language set.

Concatenates damos_signs.txt into one stream (Linear B sign tokens) and
computes the same 8 DoFs that the CAS-YAML morphology schemas use. Output is
appended to a Phase-17 measured DoFs JSON for downstream YAML grounding.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts" / "phase16"
sys.path.insert(0, str(SCRIPTS_DIR))
from measure_signature_dofs import measure_corpus  # type: ignore

DAMOS_SIGNS = ROOT / "backend" / "glossa_lab" / "data" / "phase17_corpora" / "damos_signs.txt"
OUT_JSON = ROOT / "backend" / "glossa_lab" / "data" / "phase17_corpora" / "phase17_measured_dofs.json"
OUT_CSV = ROOT / "backend" / "glossa_lab" / "data" / "phase17_corpora" / "phase17_measured_dofs.csv"


def main() -> int:
    if not DAMOS_SIGNS.exists():
        print(f"ERROR: not found {DAMOS_SIGNS}", file=sys.stderr)
        return 1
    seq: list[str] = []
    with DAMOS_SIGNS.open("r", encoding="utf-8") as fh:
        for line in fh:
            tokens = line.strip().split()
            seq.extend(tokens)
    print(f"DAMOS sign stream: {len(seq)} tokens", file=sys.stderr)

    r = measure_corpus("damos_linear_b", seq,
                       note="DAMOS Mycenaean Linear B; full corpus scrape, Phase-17.")
    print(f"  zipf_alpha={r['zipf_alpha']}  zipf_r2={r['zipf_r2']}", file=sys.stderr)
    print(f"  mi_gamma={r['mi_gamma']}  mi_r2_pow={r['mi_r2_pow']}", file=sys.stderr)
    print(f"  eps2={r['epistatic_2nd_norm']}  eps3={r['epistatic_3rd_norm']}", file=sys.stderr)
    print(f"  h1_norm={r['h1_norm']}  h1_nats={r['h1_nats']}", file=sys.stderr)
    print(f"  V={r['n_types']}", file=sys.stderr)

    out = {"phase": "phase17", "purpose": "Linear B DoF measurement",
           "results": [r]}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}", file=sys.stderr)
    import csv
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(r.keys()))
        w.writeheader()
        w.writerow(r)
    print(f"Wrote {OUT_CSV}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
