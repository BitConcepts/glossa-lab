"""Phase-62a: Fix Phase-55 Ensemble Token-Granularity Mismatch.

ROOT CAUSE (DO NOT CLAIM → VERIFIED fix):
  Phase-55 ran 4 LMs: Tamil_char, Tamil_syllabic, Proto_Dravidian, Sanskrit.
  Tamil_char LM uses single Tamil Unicode characters as tokens (ி, ா, ு, etc.).
  Tamil_syllabic, Proto_Dravidian, Sanskrit all use romanized syllables (ay, an, ko…).
  When comparing LM outputs, "ி" can never equal "ay" — the consensus always failed,
  yielding ENSEMBLE_HIGH=0, ENSEMBLE_MEDIUM=0, ENSEMBLE_LOW=390.

FIX:
  Use ONLY the 3 syllabic-level LMs for consensus:
    - Tamil_syllabic  (romanized syllables, DEDR + TamilTB)
    - Proto_Dravidian (romanized bigrams, DEDR reconstructions)
    - Sanskrit        (romanized syllables, adversarial)

  ENSEMBLE_HIGH  = Tamil_syllabic agrees with Proto_Dravidian AND Sanskrit DISAGREES
  ENSEMBLE_MEDIUM = Tamil_syllabic agrees with Proto_Dravidian (Sanskrit also agrees)
  ENSEMBLE_LOW   = Tamil_syllabic and Proto_Dravidian DISAGREE

GPU: torch for loading the phase55_final_decipherment.json tensor operations.
Output: reports/phase62_ensemble_fixed.json
"""
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
P55     = REPO / "reports/phase55_final_decipherment.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase62_ensemble_fixed.json"

# Proto-Dravidian initials that make a syllable plausibly Dravidian:
# (used as a secondary quality filter on ENSEMBLE_HIGH signs)
PD_VALID_INITIALS = set("kctpmnyvrlzsh")
PD_INVALID_INITIALS = set("bdfgqwx")


def is_pd_valid(reading: str) -> bool:
    """Return True if the reading has a plausible Proto-Dravidian initial."""
    r = reading.lower().strip()
    if not r:
        return False
    first = r[0]
    if first in "aāiīuūeēoō":  # vowel initial always valid
        return True
    return first not in PD_INVALID_INITIALS


def main():
    print("Phase-62a: Ensemble Fix (token granularity)\n")

    if not P55.exists():
        print(f"ERROR: {P55} not found — run phase55_ensemble.py first")
        return

    table = json.loads(P55.read_text("utf-8"))
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]

    print(f"  Signs in phase55 table: {len(table)}")
    print(f"  Fix: using Tamil_syllabic + Proto_Dravidian vs Sanskrit only")
    print()

    fixed_table = []
    n_high = 0
    n_medium = 0
    n_low = 0

    # Optionally use GPU to batch-process the consensus check
    if torch is not None and DEVICE == "cuda":
        # Build tensors: for each sign, encode agreement as binary
        # This is lightweight but demonstrates GPU path
        syl_readings  = []
        proto_readings = []
        skt_readings   = []
        for entry in table:
            per_lm = entry.get("per_lm", {})
            syl_readings.append(per_lm.get("Tamil_syllabic", ""))
            proto_readings.append(per_lm.get("Proto_Dravidian", ""))
            skt_readings.append(per_lm.get("Sanskrit", ""))
        n = len(table)
        # Encode agreement as 0/1 tensor
        syl_proto_agree = torch.zeros(n, dtype=torch.bool, device=DEVICE)
        syl_skt_differ  = torch.zeros(n, dtype=torch.bool, device=DEVICE)
        for i in range(n):
            syl_proto_agree[i] = syl_readings[i] != "" and syl_readings[i][:3] == proto_readings[i][:3]
            syl_skt_differ[i]  = syl_readings[i] != skt_readings[i]
        agree_cpu  = syl_proto_agree.cpu().tolist()
        differ_cpu = syl_skt_differ.cpu().tolist()
        print(f"[GPU:{DEVICE}] Computed {n}-sign consensus tensors")
    else:
        agree_cpu  = None
        differ_cpu = None

    for i, entry in enumerate(table):
        sign    = entry["sign"]
        per_lm  = entry.get("per_lm", {})
        n_corp  = entry.get("n_corpus", 0)
        confirmed_reading = entry.get("confirmed_reading", "")
        confirmed_conf    = entry.get("confirmed_confidence", "UNREAD")

        syl   = per_lm.get("Tamil_syllabic", "")
        proto = per_lm.get("Proto_Dravidian", "")
        skt   = per_lm.get("Sanskrit", "")

        # Agreement at first-3-char level (avoids tiny differences in transliteration)
        syl_proto_agree = (syl != "" and syl[:3] == proto[:3])
        syl_skt_differ  = (syl != skt)

        if agree_cpu is not None:
            syl_proto_agree = bool(agree_cpu[i])
            syl_skt_differ  = bool(differ_cpu[i])

        if syl_proto_agree and syl_skt_differ:
            ensemble_conf = "ENSEMBLE_HIGH"
            n_high += 1
        elif syl_proto_agree:
            ensemble_conf = "ENSEMBLE_MEDIUM"
            n_medium += 1
        else:
            ensemble_conf = "ENSEMBLE_LOW"
            n_low += 1

        # Phonotactic quality flag
        pd_valid = is_pd_valid(syl) if syl else False

        fixed_table.append({
            "sign":              sign,
            "n_corpus":          n_corp,
            "ensemble_reading":  syl if syl else proto,
            "ensemble_confidence": ensemble_conf,
            "Tamil_syllabic":    syl,
            "Proto_Dravidian":   proto,
            "Sanskrit":          skt,
            "syllabic_proto_agree": syl_proto_agree,
            "syllabic_skt_differ":  syl_skt_differ,
            "pd_phonotactic_valid":  pd_valid,
            "confirmed_reading": confirmed_reading,
            "confirmed_confidence": confirmed_conf,
        })

    # Sort by confidence tier then corpus frequency
    tier_order = {"ENSEMBLE_HIGH": 0, "ENSEMBLE_MEDIUM": 1, "ENSEMBLE_LOW": 2}
    fixed_table.sort(key=lambda x: (tier_order.get(x["ensemble_confidence"], 9),
                                    -x["n_corpus"]))

    print(f"=== Phase-62a Results ===")
    print(f"  ENSEMBLE_HIGH:   {n_high} signs")
    print(f"  ENSEMBLE_MEDIUM: {n_medium} signs")
    print(f"  ENSEMBLE_LOW:    {n_low} signs")
    print()

    # Show top ENSEMBLE_HIGH signs
    high_signs = [e for e in fixed_table if e["ensemble_confidence"] == "ENSEMBLE_HIGH"]
    print(f"  Top ENSEMBLE_HIGH signs (Dravidian consensus, Sanskrit diverges):")
    for e in high_signs[:15]:
        conf_marker = "✓✓" if e["confirmed_confidence"] in ("HIGH","MEDIUM") else "SA"
        agree_mark  = "✓" if e.get("confirmed_reading","")[:3] == e["Tamil_syllabic"][:3] else "?"
        print(f"  {e['sign']:6s} syl={e['Tamil_syllabic']:8s} proto={e['Proto_Dravidian']:8s} "
              f"skt={e['Sanskrit']:8s} [{conf_marker}] {agree_mark} confirmed={e['confirmed_reading']!r}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "fix_description": (
            "Phase-55 used Tamil_char LM (Unicode chars) + 3 syllabic LMs. "
            "Tamil_char tokens (ி,ா,etc.) can never match romanized syllabic tokens (ay,an,etc.) "
            "so ENSEMBLE_HIGH was always 0. Fix: use only Tamil_syllabic + Proto_Dravidian vs Sanskrit."
        ),
        "n_ensemble_high":   n_high,
        "n_ensemble_medium": n_medium,
        "n_ensemble_low":    n_low,
        "fixed_table": fixed_table[:50],   # top-50 for report
        "all_high_signs": [e["sign"] for e in high_signs],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
