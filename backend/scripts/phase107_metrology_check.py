"""Phase-107 Step 5: numerals/metrology validation (spec 005).

Subsystem: the additive stroke-numeral family M086..M092 (1..7 vertical
strokes) identified in backend/glossa_lab/data/indus_sign_crosswalk.py
sign notes ("Single vertical stroke", "Two vertical strokes", ...;
"Additive stroke system; Mahadevan 1977").

Constraints (pre-registered in specs/005-phase52-v2/spec.md):
  C1 Distinctness — the seven stroke signs receive pairwise-distinct
     values under the strengthened SA consensus.
  C2 Order — IF the SA values are Dravidian numeral syllables, their
     numeric order must be monotone in stroke count; if they are not
     numeral syllables, C2 is NOT APPLICABLE (never pass/fail).
  C3 Positional/block structure — pattern statement, from the in-repo
     metrological artifacts: phase21d (outputs/phase21d_numerical_
     weights.json) analyses numerical signs as occurring in BLOCKS
     (runs); the additive system (Mahadevan 1977) groups strokes into
     counting blocks. Operationalisation (recorded here, per spec):
     in inscriptions containing >= 2 stroke-family tokens, the stroke
     tokens form a single contiguous block; PASS iff that holds for
     >= 80% of such inscriptions. C3 validates the metrological
     structure the SA subsystem inherits; it is a corpus fact, and the
     SA values for the block signs are reported alongside it.

GPU: torch guarded per H20 pattern. Output:
reports/phase107_step5_metrology.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

try:
    import torch

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only (WARNING: H20 CPU path)")

from glossa_lab.pipelines import sa_validation as sv  # noqa: E402

REPORTS = REPO / "reports"
OUT = REPORTS / "phase107_step5_metrology.json"
STROKES = {f"M{86 + i:03d}": i + 1 for i in range(7)}  # M086=1 .. M092=7 strokes
# NOTE (2026-10-05, continuation audit): the first execution of this
# script built the IDs as f"M{86+i}" (unpadded "M86".."M92"), which
# match nothing in the corpus/anchors/table — every lookup returned
# None and C3 found 0 stroke tokens. Zero-padding fixed before any
# result was committed; the null first run is recorded in the
# glossa-indus ledger Phase-107 Step-5 entry.
# Dravidian (Tamil) numeral first syllables, diacritic-stripped,
# as extractable by the harness gold procedure:
NUMERAL_SYLLABLES = {
    1: {"oru", "or", "on", "onr"},
    2: {"ira", "ir"},
    3: {"mun", "mu"},
    4: {"nan", "na"},
    5: {"ain", "ai"},
    6: {"aru", "ar"},
    7: {"elu", "el"},
}


def main() -> None:
    table = json.loads((REPORTS / "phase107_decipherment_table.json").read_text("utf-8"))
    by_sign = {t["sign"]: t for t in table}
    flat, insc = sv.load_holdat_corpus()
    anchors = sv.load_anchors()

    values = {}
    for sign, k in STROKES.items():
        t = by_sign.get(sign, {})
        values[sign] = {"strokes": k, "sa_reading": t.get("sa_reading"),
                        "consensus_frac": t.get("sa_consensus_frac"),
                        "tier": t.get("tier"),
                        "anchor_reading": anchors.get(sign, {}).get("reading", ""),
                        "anchor_confidence": anchors.get(sign, {}).get("confidence", "UNREAD"),
                        "n_corpus": t.get("n_corpus", 0)}

    # C1 distinctness
    sa_vals = [v["sa_reading"] for v in values.values()]
    c1 = {"pass": len(set(sa_vals)) == len(sa_vals),
          "values": sa_vals, "n_distinct": len(set(sa_vals))}

    # C2 order (only if values are numeral syllables)
    val_to_num: dict[str, int] = {}
    for num, syls in NUMERAL_SYLLABLES.items():
        for s in syls:
            val_to_num.setdefault(s, num)
    applicable = [(v["strokes"], val_to_num[v["sa_reading"]])
                    for v in values.values() if v["sa_reading"] in val_to_num]
    if len(applicable) >= 3:
        monotone = all(applicable[i][1] < applicable[i + 1][1]
                       for i in range(len(applicable) - 1))
        c2 = {"applicable": True, "pass": monotone,
              "pairs_strokes_to_numeral": applicable}
    else:
        c2 = {"applicable": False, "pass": None,
              "note": f"only {len(applicable)} of 7 SA values are Dravidian numeral "
                      "syllables (< 3 required); C2 NOT APPLICABLE by the pre-registered rule",
              "pairs_strokes_to_numeral": applicable}

    # C3 block contiguity
    stroke_set = set(STROKES)
    multi = [i for i in insc if sum(1 for s in i if s in stroke_set) >= 2]
    contiguous = 0
    for i in multi:
        pos = [j for j, s in enumerate(i) if s in stroke_set]
        if pos == list(range(pos[0], pos[0] + len(pos))):
            contiguous += 1
    n_stroke_tokens = sum(1 for s in flat if s in stroke_set)
    c3 = {"n_inscriptions_with_ge2_stroke_tokens": len(multi),
          "n_contiguous_block": contiguous,
          "rate": round(contiguous / len(multi), 4) if multi else None,
          "pass": (contiguous / len(multi) >= 0.80) if multi else None,
          "n_stroke_tokens_total": n_stroke_tokens}

    artifact = {
        "phase": 107, "step": 5, "spec": "specs/005-phase52-v2",
        "gpu_device": DEVICE,
        "subsystem": "additive stroke numerals M086-M092 (Mahadevan 1977 via indus_sign_crosswalk.py)",
        "sa_values": values,
        "C1_distinctness": c1,
        "C2_order": c2,
        "C3_block_contiguity": c3,
    }
    OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), "utf-8")
    print(f"Step 5 artifact: {OUT}")
    print(f"C1 pass={c1['pass']}  C2 applicable={c2['applicable']} pass={c2['pass']}  "
          f"C3 rate={c3['rate']} pass={c3['pass']}")


if __name__ == "__main__":
    main()
