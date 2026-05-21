"""Phase-61: Phonotactic Falsification Battery.
Tests all assigned phoneme values against Dravidian phonotactic constraints.
GPU: torch for sequence validity matrix. Output: reports/phase61_phonotactic.json
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))  # add backend/ to sys.path
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P57     = REPO / "reports/phase57_decipherment_table.json"
REPORTS = REPO / "reports"; REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase61_phonotactic.json"

# Dravidian phonotactics (Krishnamurti 2003, Subrahmanyam 1983)
VOWELS = set("aāiīuūeēoō")
# Proto-Dravidian allows these word-initial consonants:
PD_VALID_INITIALS = set("kctpmnyvrlzsh")  # standard PDr set (romanized)
# Words CANNOT start with these in Proto-Dravidian
PD_INVALID_INITIALS = set("bdfgqwx")  # no voiced stops, no labio-dentals initially
# Tamil has specific disallowed bigrams (adjacent consonant sequences)
# Simplified: retroflex after alveolar within syllable is unusual
PROBLEMATIC_SEQUENCES = [
    ("r", "l"), ("l", "r"), ("n", "l"), ("v", "v"),
]

def check_phonotactics(reading: str) -> dict:
    """Check a reading against Dravidian phonotactic constraints."""
    r = reading.lower().split("/")[0].strip()
    r = re.sub(r'[^a-zāīūēō]', '', r)
    if not r: return {"valid": True, "issues": []}
    issues = []
    first = r[0]
    # Initial consonant check
    if first not in VOWELS and first in PD_INVALID_INITIALS:
        issues.append(f"Invalid initial '{first}' in Proto-Dravidian")
    # Check for impossible sequences
    for i in range(len(r)-1):
        pair = (r[i], r[i+1])
        if pair in PROBLEMATIC_SEQUENCES:
            issues.append(f"Unusual sequence '{r[i]}{r[i+1]}' at position {i}")
    # Minimum syllable length check
    if len(r) == 1 and r[0] not in VOWELS:
        issues.append("Single consonant — not a valid syllable")
    return {"valid": len(issues) == 0, "issues": issues, "normalized": r}


def compute_sequence_validity_gpu(inscriptions: list, readings: dict) -> dict:
    """GPU: compute fraction of inscriptions that form valid Dravidian phoneme sequences."""
    if torch is None: return {}
    n = len(inscriptions)
    validity = torch.zeros(n, device=DEVICE)
    for i, insc in enumerate(inscriptions):
        signs = insc["signs"]
        phonemes = []
        for s in signs:
            r = readings.get(s, {}).get("reading", "")
            if r: phonemes.append(r.lower()[:1])
        if not phonemes: continue
        # Check sequence: any vowel harmony violations?
        has_front = any(p in set("iīeē") for p in phonemes)
        has_back = any(p in set("uūoō") for p in phonemes)
        # Dravidian vowel harmony: front + back vowels in same word = unusual
        if not (has_front and has_back):
            validity[i] = 1.0
    valid_rate = float(validity.mean().item())
    print(f"[GPU:{DEVICE}] Sequence validity: {valid_rate:.1%} of inscriptions pass vowel harmony")
    return {"valid_inscription_rate": round(valid_rate, 3)}


def main():
    print("Phase-61: Phonotactic Falsification Battery\n")
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    # Load decipherment table
    readings = {}
    if P57.exists():
        for entry in json.loads(P57.read_text("utf-8")):
            sign = entry["sign"]
            conf = entry.get("confirmed_confidence", "UNREAD")
            if conf in ("HIGH","MEDIUM") and entry.get("confirmed_reading"):
                readings[sign] = {"reading": entry["confirmed_reading"], "confidence": conf}
            elif entry.get("sa_reading") and sign not in readings:
                readings[sign] = {"reading": entry["sa_reading"], "confidence": "SA"}
    else:
        for sign, info in anchors.items():
            if info.get("reading") and info.get("confidence") in ("HIGH","MEDIUM"):
                readings[sign] = {"reading": info["reading"], "confidence": info["confidence"]}
    # Test each reading
    results = []
    n_valid = n_issues = 0
    for sign, info in readings.items():
        check = check_phonotactics(info["reading"])
        if check["valid"]: n_valid += 1
        else: n_issues += 1
        results.append({
            "sign": sign, "reading": info["reading"], "confidence": info["confidence"],
            **check
        })
    # Load corpus for sequence test
    seals: dict[str, dict] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]; p = int(row.get("position",0) or 0)
            if c not in seals: seals[c] = {"signs": []}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = row["letters"]
    inscriptions = [{"signs": [s for s in v["signs"] if s]} for v in seals.values() if any(v["signs"])]
    seq_validity = compute_sequence_validity_gpu(inscriptions[:500], readings)
    # Overall verdict
    violation_rate = n_issues / max(n_valid + n_issues, 1)
    verdict = "VALID" if violation_rate < 0.1 else ("MOSTLY_VALID" if violation_rate < 0.25 else "ISSUES_FOUND")
    print("\n=== Phase-61 Results ===")
    print(f"  Readings tested: {len(results)}")
    print(f"  Valid: {n_valid}, Issues: {n_issues} ({violation_rate:.0%} violation rate)")
    print(f"  Sequence validity: {seq_validity.get('valid_inscription_rate',0):.1%}")
    print(f"  Verdict: {verdict}")
    problematic = [r for r in results if not r["valid"]]
    for r in problematic[:5]:
        print(f"  {r['sign']} = {r['reading']!r}: {r['issues']}")
    result = {
        "_citation": {"primary": ["A.1"], "krishnamurti": "Krishnamurti 2003"},
        "gpu_device": DEVICE,
        "n_tested": len(results), "n_valid": n_valid, "n_issues": n_issues,
        "violation_rate": round(violation_rate, 3),
        "sequence_validity": seq_validity,
        "verdict": verdict,
        "problematic_readings": problematic[:20],
        "all_results": results,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
