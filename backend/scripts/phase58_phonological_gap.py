"""Phase-58: Phonological Gap Analysis. GPU: torch. Output: reports/phase58_phonological_gap.json"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
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
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
REPORTS = REPO / "reports"; REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase58_phonological_gap.json"

# Dravidian phonotactic constraints (from Krishnamurti 2003)
# Initial: V or CV (no initial consonant clusters; no initial retroflexes ṭ,ḍ,ṇ,ḷ,ṟ,ṉ)
# Final: C (nasal/lateral/vibrant) or V
# Forbidden initial consonants in Proto-Dravidian:
FORBIDDEN_INITIAL_CONSONANTS = set("ṭḍṇḷṟṉ")  # retroflexes don't occur initially
LONG_VOWEL_MARKER = "āīūēō"  # length markers

# Tamil syllable structure: (C*)(V)(C?)
VOWELS = set("aāiīuūeēoō")
CONSONANTS = set("bcdfghjklmnpqrstvwxyz" + "ṭḍṇḷṟṉṅñśṣ")

def is_valid_dravidian_initial(syllable: str) -> bool:
    """Check if syllable could validly appear initially in a Dravidian word."""
    if not syllable: return False
    s = syllable.lower().strip()
    # Remove diacritics for basic check
    s_norm = re.sub(r'[^a-zāīūēō]', '', s)
    if not s_norm: return True  # can't check
    first = s_norm[0]
    # Vowel initial is always valid
    if first in VOWELS: return True
    # Retroflex initial is INVALID in Proto-Dravidian
    if first in FORBIDDEN_INITIAL_CONSONANTS: return False
    return True

def analyze_phoneme_inventory(anchors: dict, freq: Counter) -> dict:
    """Analyze the phoneme inventory for gaps and issues."""
    by_initial: defaultdict = defaultdict(list)
    by_cv_shape: defaultdict = defaultdict(list)
    problematic = []
    collisions: defaultdict = defaultdict(list)  # same phoneme → multiple signs

    for sign, info in anchors.items():
        reading = info.get("reading", "")
        conf = info.get("confidence", "?")
        if not reading or conf in ("LOW", "?", "UNCERTAIN"): continue
        # Normalize reading to initial phoneme
        reading_clean = re.sub(r'[^a-zāīūēō]', '', reading.lower().split("/")[0].strip())
        if not reading_clean: continue
        initial = reading_clean[0]
        # Determine CV shape
        cv_shape = "V" if initial in VOWELS else "C"
        by_initial[initial].append((sign, reading, conf, freq.get(sign, 0)))
        by_cv_shape[cv_shape].append(sign)
        # Check phonotactic validity
        if not is_valid_dravidian_initial(reading_clean):
            problematic.append({
                "sign": sign, "reading": reading, "confidence": conf,
                "issue": f"Retroflex initial '{reading_clean[0]}' invalid in Proto-Dravidian",
            })
        # Track collisions (same reading → multiple signs)
        collisions[reading_clean[:3]].append(sign)

    # Find problematic collisions (>3 signs with same initial 3 chars)
    collision_issues = [
        {"reading_prefix": k, "signs": v, "n": len(v)}
        for k, v in collisions.items() if len(v) >= 4
    ]

    # Compute phoneme coverage
    n_distinct = len(by_initial)
    return {
        "by_initial_phoneme": {k: [(s, r, c, n) for s,r,c,n in v]
                                for k, v in sorted(by_initial.items())},
        "cv_shape_dist": dict(Counter(cv_shape for cv_shape in by_cv_shape for _ in by_cv_shape[cv_shape])),
        "n_distinct_initials": n_distinct,
        "phonotactic_violations": problematic,
        "sign_collisions": collision_issues,
        "initial_consonant_coverage": sorted(by_initial.keys()),
    }


def gpu_phoneme_distribution(anchors: dict, freq: Counter) -> dict:
    if torch is None: return {}
    # Build phoneme frequency-weighted distribution
    readings = []
    weights = []
    for sign, info in anchors.items():
        r = info.get("reading", "")
        if not r or info.get("confidence") not in ("HIGH", "MEDIUM"): continue
        r_clean = re.sub(r'[^a-zāīūēō]', '', r.lower()[:4])
        if r_clean:
            readings.append(r_clean[:1])  # initial phoneme
            weights.append(float(freq.get(sign, 1)))
    if not readings: return {}
    chars = sorted(set(readings))
    char_idx = {c: i for i, c in enumerate(chars)}
    n = len(chars)
    dist = torch.zeros(n, device=DEVICE)
    for r, w in zip(readings, weights):
        if r in char_idx: dist[char_idx[r]] += w
    dist_norm = (dist / dist.sum()).cpu().tolist()
    # Check if distribution is reasonable (not dominated by one phoneme)
    max_share = max(dist_norm) if dist_norm else 0
    print(f"[GPU:{DEVICE}] Phoneme distribution computed, max_share={max_share:.2f}")
    return {
        "phonemes": chars,
        "weighted_dist": [round(v, 4) for v in dist_norm],
        "max_single_phoneme_share": round(max_share, 3),
        "entropy_ok": max_share < 0.3,  # good diversity if no phoneme > 30%
    }


def main():
    print("Phase-58: Phonological Gap Analysis\n")
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data["anchors"]
    freq = Counter()
    with open(CORPUS, encoding="utf-8") as f:
        for r in csv.DictReader(f): freq[r["letters"]] += 1
    print(f"  Anchors: {len(anchors)}, Checking HIGH+MEDIUM only")
    analysis = analyze_phoneme_inventory(anchors, freq)
    gpu_dist = gpu_phoneme_distribution(anchors, freq)
    violations = analysis["phonotactic_violations"]
    collisions = analysis["sign_collisions"]
    n_valid_initials = analysis["n_distinct_initials"]
    print("\n=== Phase-58 Results ===")
    print(f"  Distinct initial phonemes: {n_valid_initials}")
    print(f"  Phonotactic violations: {len(violations)}")
    print(f"  Sign collisions (≥4 signs, same 3-char prefix): {len(collisions)}")
    if violations:
        for v in violations[:5]:
            print(f"  VIOLATION: {v['sign']} = {v['reading']!r} — {v['issue']}")
    print(f"  Initial phoneme coverage: {analysis['initial_consonant_coverage'][:20]}")
    if gpu_dist:
        print(f"  Max phoneme share: {gpu_dist.get('max_single_phoneme_share',0):.1%} (OK if <30%)")
    # Verdict
    verdict = "VALID" if len(violations) == 0 and n_valid_initials >= 10 else "ISSUES_FOUND"
    result = {
        "_citation": {"primary": ["A.1"], "krishnamurti": "Krishnamurti 2003"},
        "gpu_device": DEVICE,
        "n_anchors_checked": sum(1 for v in anchors.values() if v.get("confidence") in ("HIGH","MEDIUM")),
        "n_distinct_initials": n_valid_initials,
        "phonotactic_violations": violations,
        "sign_collisions": collisions,
        "phoneme_distribution": gpu_dist,
        "coverage": analysis["initial_consonant_coverage"],
        "verdict": verdict,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Verdict: {verdict}")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
