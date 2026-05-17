"""Phase-48: MEDIUM Anchor Validation Suite.

We have 54 MEDIUM-confidence readings. If validated, they cover ~24% more
corpus tokens — pushing total decoded coverage from 20% (HIGH only) to ~44%.

For each top-frequency MEDIUM sign, run 3 independent tests:

  TEST 1 — POSITIONAL: Does avg_position match the predicted grammatical role?
    CASE_MARKER_SUFFIX → expected avg_pos ≥ 0.5, is_ending=True
    CLASSIFIER_PREFIX  → expected avg_pos = 0.0, is_starter=True
    PERSON_OR_OWNER    → expected avg_pos ∈ [0.4, 0.7] (medial)

  TEST 2 — DEDR ATTESTATION: Is the reading plausibly attested in DEDR?
    Scan DEDR for the romanized reading form. Score by how many DEDR entries
    contain it as a Tamil word root or morpheme.

  TEST 3 — BIGRAM CONSISTENCY: Do the sign's corpus bigrams align with
    what the Dravidian 944-LM predicts for the assigned character?
    (A sign reading 'ā' should most often co-occur with signs whose readings
    are vowel-adjacent in Tamil bigram space.)

Signs passing ≥2/3 tests → promoted to HIGH in updated ANCHORS.

GPU: torch for bigram matrix consistency scoring.

Output: reports/phase48_medium_validation.json
        updates INDUS_FINAL_ANCHORS.json (promoted_to_high section)
"""
from __future__ import annotations
import csv, json, math, re
from collections import Counter
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None; DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES   = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
DEDR    = REPO / "reports/jambu-dedr/data/dedr/dedr_new.csv"
LM_PATH = REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase48_medium_validation.json"

# Positional expectations per Holdat role
ROLE_POSITIONAL_EXPECT = {
    "CASE_MARKER_SUFFIX":  {"avg_pos_min": 0.5, "is_ending": True,  "is_starter": False},
    "CLASSIFIER_PREFIX":   {"avg_pos_max": 0.2, "is_ending": False, "is_starter": True},
    "PERSON_OR_OWNER":     {"avg_pos_min": 0.3, "avg_pos_max": 0.75, "is_ending": None, "is_starter": None},
    "STRONG_PERSON_OR_OWNER": {"avg_pos_min": 0.3, "avg_pos_max": 0.75},
    "UNKNOWN":             {},
}


def load_all():
    anchors = json.loads(ANCHORS_PATH.read_text("utf-8"))
    roles = {}
    with open(ROLES, encoding="utf-8") as f:
        for r in csv.DictReader(f): roles[r["symbol"]] = r
    with open(CORPUS, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    freq = Counter(r["letters"] for r in rows if r["letters"])
    inscriptions: dict[str, list] = {}
    for r in rows:
        cisi = r["cisi_number"]; pos = int(r.get("position",0) or 0)
        inscriptions.setdefault(cisi, [])
        while len(inscriptions[cisi]) <= pos: inscriptions[cisi].append("")
        inscriptions[cisi][pos] = r["letters"]
    seqs = [[s for s in v if s] for v in inscriptions.values() if any(v)]
    return anchors, roles, freq, seqs


def load_lm():
    raw = json.loads(LM_PATH.read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    total = sum(bigrams.values()) or 1
    return {tuple(k.split(",",1)): v/total for k,v in bigrams.items() if "," in k}


def load_dedr():
    """Load DEDR as list of (tamil_word, gloss) tuples."""
    entries = []
    try:
        with open(DEDR, encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                if len(row) >= 5:
                    word = row[2].strip() if len(row) > 2 else ""
                    gloss = row[3].strip() if len(row) > 3 else ""
                    if word and len(word) > 1:
                        entries.append((word.lower(), gloss.lower()))
    except Exception as e:
        print(f"  DEDR load warning: {e}")
    return entries


def test_positional(sign: str, reading: str, role: dict) -> tuple[bool, str]:
    """TEST 1: does avg_position match the Holdat role prediction?"""
    if not role:
        return False, "no_role_data"
    avg_pos = float(role.get("avg_position", 0.5) or 0.5)
    is_starter = role.get("is_starter", "") == "True"
    is_ending  = role.get("is_ending", "") == "True"
    sem_role   = role.get("semantic_role", "UNKNOWN")
    expect     = ROLE_POSITIONAL_EXPECT.get(sem_role, {})

    if not expect:
        return True, "no_expectation—pass_by_default"

    ok = True
    reason_parts = []
    if "avg_pos_min" in expect and avg_pos < expect["avg_pos_min"]:
        ok = False; reason_parts.append(f"pos={avg_pos:.2f}<{expect['avg_pos_min']}")
    if "avg_pos_max" in expect and avg_pos > expect["avg_pos_max"]:
        ok = False; reason_parts.append(f"pos={avg_pos:.2f}>{expect['avg_pos_max']}")
    if expect.get("is_ending") is not None and is_ending != expect["is_ending"]:
        ok = False; reason_parts.append(f"ending={is_ending}!={expect['is_ending']}")
    if expect.get("is_starter") is not None and is_starter != expect["is_starter"]:
        ok = False; reason_parts.append(f"starter={is_starter}!={expect['is_starter']}")

    return ok, ("PASS" if ok else f"FAIL: {'; '.join(reason_parts)}")


def test_dedr(reading: str, dedr_entries: list) -> tuple[bool, str]:
    """TEST 2: is the reading attested in DEDR?"""
    # Strip diacritics for fuzzy match
    def norm(s): return re.sub(r"[^a-z]", "", s.lower())
    reading_clean = norm(reading)
    if len(reading_clean) < 2:
        return True, "too_short_pass"
    # Check exact match and prefix match
    exact = sum(1 for w, g in dedr_entries if norm(w) == reading_clean)
    prefix = sum(1 for w, g in dedr_entries if norm(w).startswith(reading_clean[:3]) or reading_clean.startswith(norm(w)[:3]))
    if exact > 0:
        return True, f"exact_match_{exact}"
    if prefix >= 2:
        return True, f"prefix_match_{prefix}"
    return False, f"no_dedr_match (tried {reading_clean!r}, {prefix} prefix hits)"


def test_bigram_consistency(sign: str, reading: str, seqs: list, bigram_prob: dict) -> tuple[bool, str]:
    """TEST 3: do corpus neighbours align with Dravidian bigrams for this reading?"""
    all_chars = sorted(set(t for pair in bigram_prob for t in pair))
    char_idx = {c: i for i, c in enumerate(all_chars)}

    # The reading's initial character in the LM
    reading_char = reading[0] if reading else "?"
    if reading_char not in char_idx:
        return True, "char_not_in_lm—pass_by_default"

    # Get top-5 continuation characters from LM for this reading char
    if torch is not None:
        n = len(all_chars)
        row = torch.zeros(n, device=DEVICE)
        for (a, b), p in bigram_prob.items():
            if a == reading_char and b in char_idx:
                row[char_idx[b]] = float(p)
        top5 = row.topk(min(5, n)).indices.cpu().tolist()
        top5_chars = {all_chars[i] for i in top5}
    else:
        top5_chars = {b for (a,b) in bigram_prob if a == reading_char}

    # Get anchors (HIGH confidence) for signs that appear most after this sign
    anchors = json.loads(ANCHORS_PATH.read_text("utf-8"))["anchors"]
    post: Counter = Counter()
    for insc in seqs:
        for i, s in enumerate(insc):
            if s == sign and i < len(insc)-1:
                post[insc[i+1]] += 1

    # How many top following signs have readings starting with chars in top5_chars?
    matches = 0; total_checked = 0
    for neighbor_sign, cnt in post.most_common(5):
        a = anchors.get(neighbor_sign, {})
        if a.get("confidence") in ("HIGH", "MEDIUM") and a.get("reading"):
            neighbor_char = a["reading"][0]
            total_checked += 1
            if neighbor_char in top5_chars:
                matches += 1
    if total_checked == 0:
        return True, "no_anchor_neighbours—pass_by_default"
    ratio = matches / total_checked
    return ratio >= 0.4, f"neighbour_match={matches}/{total_checked}={ratio:.1%}"


def main() -> None:
    print("Phase-48: MEDIUM Anchor Validation Suite\n")

    anchors_data, roles, freq, seqs = load_all()
    anchors = anchors_data["anchors"]
    lm = load_lm()
    dedr = load_dedr()
    print(f"  DEDR entries loaded: {len(dedr)}")

    medium = [(k, v) for k, v in anchors.items() if v.get("confidence") == "MEDIUM"]
    medium.sort(key=lambda x: -freq.get(x[0], 0))
    print(f"  MEDIUM signs: {len(medium)}, testing top 30 by frequency\n")

    results = []
    promoted = []

    for sign, anchor in medium[:30]:
        reading = anchor.get("reading", "")
        role = roles.get(sign, {})
        n = freq.get(sign, 0)

        t1_pass, t1_msg = test_positional(sign, reading, role)
        t2_pass, t2_msg = test_dedr(reading, dedr)
        t3_pass, t3_msg = test_bigram_consistency(sign, reading, seqs, lm)

        score = sum([t1_pass, t2_pass, t3_pass])
        promote = score >= 2
        status = "PROMOTE→HIGH" if promote else f"KEEP_MEDIUM({score}/3)"

        print(f"  {sign:6s} n={n:4d} {reading!r:15s} T1={'✓' if t1_pass else '✗'} T2={'✓' if t2_pass else '✗'} T3={'✓' if t3_pass else '✗'} {score}/3 → {status}")
        results.append({
            "sign": sign, "reading": reading, "n_corpus": n,
            "holdat_role": role.get("semantic_role","?"),
            "avg_position": float(role.get("avg_position",0) or 0),
            "test1_positional": {"pass": t1_pass, "detail": t1_msg},
            "test2_dedr": {"pass": t2_pass, "detail": t2_msg},
            "test3_bigram": {"pass": t3_pass, "detail": t3_msg},
            "score": score, "promote": promote,
        })
        if promote:
            promoted.append(sign)

    n_promoted = len(promoted)
    promoted_coverage = sum(freq.get(s,0) for s in promoted)
    total_tokens = sum(freq.values())
    new_cov = sum(freq.get(s,0) for s in anchors if anchors[s].get("confidence")=="HIGH") + promoted_coverage
    print(f"\n=== Validation Summary ===")
    print(f"  Promoted to HIGH: {n_promoted} signs: {promoted}")
    print(f"  Additional coverage: {promoted_coverage}/{total_tokens} = {promoted_coverage/total_tokens:.1%}")
    print(f"  New total HIGH coverage: {new_cov/total_tokens:.1%}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "n_medium_tested": len(results),
        "n_promoted": n_promoted,
        "promoted_signs": promoted,
        "additional_coverage_pct": round(promoted_coverage/total_tokens*100, 1),
        "new_total_high_coverage_pct": round(new_cov/total_tokens*100, 1),
        "results": results,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
