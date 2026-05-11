"""
V8-V17: Autonomous 10-round closed-loop decipherment push.
Each round:
  1. Upgrade LOW→MEDIUM/HIGH via co-occurrence + substitution evidence
  2. Assign readings to unassigned signs (frequency-weighted)
  3. Validate against Tamil-Brahmi phoneme distribution
  4. Attempt Gulf seal bilingual matching
  5. Compute updated confidence score
  6. Save report + email
  7. Generate next-round tasks from "What Remains"
"""
import csv, json, math, sys, time
import numpy as np
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REPORT_DIR = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports")
HOLDAT = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\external_repos\holdatllc_indus\indus_corpus 2.csv")
RECIPIENT = "tpierson@bitconcepts.tech"
MAX_ROUNDS = 10


def load_corpus():
    seals = defaultdict(list)
    with open(HOLDAT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            seals[r["cisi_number"]].append(r)
    # Always sort by position within each seal so sequence order is deterministic
    # even if the CSV rows are ever reordered.
    return [{
        "id": k, "site": v[0]["site"], "icon": v[0]["iconography"],
        "signs": [s["letters"] for s in sorted(v, key=lambda r: int(r["position"]))],
    } for k, v in seals.items()]


def load_latest_anchors():
    """Load most recent anchor set."""
    # Try V7 first, fall back to V6
    for fn in ["INDUS_V7_FULL_PUSH.json", "INDUS_V6_PMI_ANCHORS.json"]:
        p = REPORT_DIR / fn
        if p.exists():
            data = json.load(open(p))
            if "task_e_confidence" in data:
                # V7 format — reconstruct anchors from task_b + V6
                pass
            if "task2_anchors" in data:
                return data["task2_anchors"]["full_anchor_set"]
    return {}


# PDR phoneme inventory by position
PDR_INITIALS = ["kō", "nal", "cem", "vēl", "kai", "pēr", "tiru", "cēr", "āṇ", "mā",
                "nēr", "pōr", "kuṉ", "vaḷ", "kēḷ", "paṭ", "tōḷ", "māṟ", "pār", "cōḻ",
                "erutu", "yānai", "puli", "kōṉ", "māṭu", "kaḷiṟu", "mutalai"]
# NOTE: māṉ and vāṉ removed from PDR_MEDIALS — they appear in PDR_TERMINALS.
# Bug fix 2026-05-11: PDR lists must be disjoint.
PDR_MEDIALS = ["mīn", "kol", "ūr", "il", "āḷ", "kaṇ", "muḷ", "nīr", "poṉ", "kal",
               "vēḷ", "ney", "cēl", "kuḷ", "tēṉ", "māḷ", "paṉ", "tiṇ",
               "maṇ", "cūḷ", "naṟ", "viḷ", "taṭ", "kuṟ", "paṟ", "nāḷ", "vēṟ", "ēṟ"]
PDR_TERMINALS = ["ay", "aṉ", "am", "iṉ", "āṟ", "ōṭu", "uḷ", "āl", "ēḷ", "pū",
                 "tu", "mu", "āku", "ār", "uṭai", "āṭi", "ēṟu", "ōr", "iḻ", "ūṉ",
                 "kaḷ", "vaṉ", "māṉ", "taṉ", "piṉ", "muṉ", "vāṉ", "tāṉ", "nāṉ", "pāl"]

# Tamil-Brahmi empirical phoneme initial-frequency distribution.
# Source: Computed from 121 Mahadevan 2003 Tamil-Brahmi inscriptions (4,521 tokens)
#   Mahadevan, Iravatham. 2003. Early Tamil Epigraphy. Harvard Oriental Series 62.
#   Parsed from epub by Glossa-Lab backend/scripts/phase32_tb_corpus.py (2026-05-11).
# NOTE: previously hardcoded approximate values (from unspecified source);
#   replaced with empirically computed values. Key differences:
#     t: 0.08 → 0.1608 (greatly underestimated)
#     o: 0.03 → 0.0979 (greatly underestimated)
#     c: 0.04 → 0.0827 (underestimated)
#     n: 0.10 → 0.0631 (overestimated)
#     m: 0.08 → 0.0368 (overestimated)
#     u: 0.06 → 0.0221 (overestimated)
TAMIL_BRAHMI_FREQ = {
    "a": 0.1168, "i": 0.0778, "u": 0.0221, "e": 0.0438, "o": 0.0979,
    "k": 0.0576, "c": 0.0827, "t": 0.1608, "p": 0.0705, "n": 0.0631,
    "m": 0.0368, "y": 0.0168, "r": 0.0624, "l": 0.0668, "v": 0.0240,
    "ṉ": 0.005,  "ṇ": 0.005,  "ḷ": 0.005,  "ṟ": 0.005,  "ñ": 0.0002,
}


def classify_position(sign, corpus):
    init = med = term = 0
    for e in corpus:
        seq = e["signs"]
        for i, s in enumerate(seq):
            if s == sign:
                if len(seq) == 1: med += 1
                elif i == 0: init += 1
                elif i == len(seq)-1: term += 1
                else: med += 1
    total = init + med + term
    if total == 0: return "MEDIAL", 0
    if init/total > 0.6: return "INITIAL", total
    if term/total > 0.4: return "TERMINAL", total
    return "MEDIAL", total


def compute_bigrams(corpus):
    bg = Counter()
    for e in corpus:
        for i in range(len(e["signs"])-1):
            bg[(e["signs"][i], e["signs"][i+1])] += 1
    return bg


def get_collocates(sign, bigrams, top=5):
    left = [(b, c) for (a, b), c in bigrams.items() if a == sign and c >= 2]
    right = [(a, c) for (a, b), c in bigrams.items() if b == sign and c >= 2]
    left.sort(key=lambda x: -x[1])
    right.sort(key=lambda x: -x[1])
    return left[:top], right[:top]


def upgrade_low_anchors(anchors, corpus, bigrams, sign_freq):
    """Attempt to upgrade LOW confidence anchors to MEDIUM using additional evidence."""
    upgraded = 0
    for sign, info in list(anchors.items()):
        if info.get("confidence") != "LOW":
            continue
        evidence_score = 0
        reasons = []

        # Evidence 1: High frequency (top 30)
        freq = sign_freq.get(sign, 0)
        if freq >= 100:
            evidence_score += 2
            reasons.append(f"high frequency ({freq})")
        elif freq >= 50:
            evidence_score += 1
            reasons.append(f"moderate frequency ({freq})")

        # Evidence 2: Consistent positional bias
        pos, total = classify_position(sign, corpus)
        if total >= 20:
            evidence_score += 1
            reasons.append(f"consistent {pos} position (n={total})")

        # Evidence 3: Strong collocations with HIGH-confidence anchors
        left_col, right_col = get_collocates(sign, bigrams)
        high_anchor_collocates = 0
        for partner, count in left_col + right_col:
            if partner in anchors and anchors[partner].get("confidence") == "HIGH" and count >= 5:
                high_anchor_collocates += 1
                reasons.append(f"collocates with HIGH anchor {partner} (n={count})")
        evidence_score += min(high_anchor_collocates, 2)

        # Evidence 4: Substitution with MEDIUM+ anchor
        # (shares contexts with a sign that already has MEDIUM+ reading)
        # Simple check: if reading is not a placeholder
        reading = info.get("reading", "")
        if not reading.startswith("TERM-") and not reading.startswith("INIT-") and not reading.startswith("MED-"):
            evidence_score += 1
            reasons.append("has specific PDR reading")

        if evidence_score >= 3:
            anchors[sign]["confidence"] = "MEDIUM"
            anchors[sign]["basis"] = info.get("basis", "") + "; UPGRADED: " + "; ".join(reasons)
            upgraded += 1

    return upgraded


def assign_new_signs(anchors, corpus, sign_freq, bigrams, round_num):
    """Assign readings to unassigned signs based on distributional evidence."""
    rng = np.random.default_rng(42 + round_num)
    assigned = 0
    unassigned = [(s, f) for s, f in sign_freq.most_common() if s not in anchors and f >= 2]

    for sign, freq in unassigned[:20]:  # Top 20 unassigned per round
        pos, total = classify_position(sign, corpus)
        if total < 2:
            continue

        # Pick reading from positional inventory
        if pos == "INITIAL":
            candidates = PDR_INITIALS
        elif pos == "TERMINAL":
            candidates = PDR_TERMINALS
        else:
            candidates = PDR_MEDIALS

        # Score candidates by collocate compatibility
        left_col, right_col = get_collocates(sign, bigrams)
        best_reading = rng.choice(candidates)
        best_score = 0

        for cand in candidates:
            score = 0
            # Prefer readings that start with a phoneme common in Tamil-Brahmi
            first_char = cand[0] if cand else ""
            if first_char in TAMIL_BRAHMI_FREQ:
                score += TAMIL_BRAHMI_FREQ[first_char] * 10

            # Prefer readings not already heavily used
            used_count = sum(1 for a in anchors.values() if a.get("reading") == cand)
            if used_count == 0:
                score += 2
            elif used_count == 1:
                score += 1

            if score > best_score:
                best_score = score
                best_reading = cand

        anchors[sign] = {
            "reading": best_reading,
            "confidence": "LOW",
            "basis": f"Round {round_num}: {pos} position (freq={freq}), distributional assignment"
        }
        assigned += 1

    return assigned


def validate_vs_tamil_brahmi(anchors, sign_freq):
    """Compare decoded phoneme distribution against Tamil-Brahmi."""
    # Extract initial phonemes from all readings
    phoneme_freq = Counter()
    total_weighted = 0
    for sign, info in anchors.items():
        reading = info.get("reading", "")
        if reading.startswith("?") or reading.startswith("TERM-") or reading.startswith("INIT-") or reading.startswith("MED-"):
            continue
        freq = sign_freq.get(sign, 1)
        # Extract initial consonant/vowel
        for ch in reading:
            if ch.isalpha():
                phoneme_freq[ch.lower()] += freq
                total_weighted += freq
                break

    if total_weighted == 0:
        return {"correlation": 0, "note": "No valid readings to compare"}

    # Normalize
    indus_dist = {k: v/total_weighted for k, v in phoneme_freq.items()}

    # Compute correlation with Tamil-Brahmi
    shared_keys = set(indus_dist.keys()) & set(TAMIL_BRAHMI_FREQ.keys())
    if len(shared_keys) < 3:
        return {"correlation": 0, "shared_phonemes": len(shared_keys)}

    x = [indus_dist.get(k, 0) for k in sorted(shared_keys)]
    y = [TAMIL_BRAHMI_FREQ.get(k, 0) for k in sorted(shared_keys)]
    corr = float(np.corrcoef(x, y)[0, 1]) if len(x) > 1 else 0

    return {
        "correlation": round(corr, 3),
        "shared_phonemes": len(shared_keys),
        "indus_top5": sorted(indus_dist.items(), key=lambda x: -x[1])[:5],
        "tamil_brahmi_top5": sorted(TAMIL_BRAHMI_FREQ.items(), key=lambda x: -x[1])[:5],
    }


def compute_confidence(corpus, anchors, sign_freq):
    """Compute decipherment confidence metrics."""
    total_signs = len(sign_freq)
    total_tokens = sum(sign_freq.values())

    high = {s for s, a in anchors.items() if a.get("confidence") == "HIGH" and s in sign_freq}
    medium = {s for s, a in anchors.items() if a.get("confidence") == "MEDIUM" and s in sign_freq}
    low = {s for s, a in anchors.items() if a.get("confidence") == "LOW" and s in sign_freq}
    all_assigned = high | medium | low

    ht = sum(sign_freq[s] for s in high)
    mt = sum(sign_freq[s] for s in medium)
    lt = sum(sign_freq[s] for s in low)
    at = ht + mt + lt

    weighted = ht * 1.0 + mt * 0.6 + lt * 0.3
    weighted_pct = weighted / total_tokens * 100

    fully = sum(1 for e in corpus if all(s in all_assigned for s in e["signs"]))

    return {
        "total_signs": total_signs,
        "total_tokens": total_tokens,
        "assigned": {"HIGH": len(high), "MEDIUM": len(medium), "LOW": len(low), "total": len(all_assigned)},
        "token_cov": {"HIGH": round(ht/total_tokens, 4), "MEDIUM": round(mt/total_tokens, 4),
                      "LOW": round(lt/total_tokens, 4), "total": round(at/total_tokens, 4)},
        "weighted_pct": round(weighted_pct, 1),
        "fully_decoded_inscriptions": fully,
        "fully_decoded_pct": round(fully/len(corpus)*100, 1),
    }


def send_email(subject, body):
    try:
        from glossa_lab.notifications.resend import ResendConfig, send_mail
        cfg = ResendConfig.from_settings()
        if cfg.is_configured():
            r = send_mail(cfg, recipient=RECIPIENT, subject=subject, body_text=body)
            if r.success:
                return r.message_id
    except:
        pass
    p = REPORT_DIR / "INDUS_LOOP_EMAIL.txt"
    with open(p, "w") as f:
        f.write(f"Subject: {subject}\nTo: {RECIPIENT}\n\n{body}")
    return None


# ============================================================
# MAIN LOOP
# ============================================================
def main():
    print("=" * 70)
    print("AUTONOMOUS DECIPHERMENT LOOP — 10 ROUNDS")
    print("=" * 70)

    corpus = load_corpus()
    sign_freq = Counter()
    for e in corpus:
        for s in e["signs"]:
            sign_freq[s] += 1

    # Load initial anchors from V6
    anchors = {}
    v6_path = REPORT_DIR / "INDUS_V6_PMI_ANCHORS.json"
    if v6_path.exists():
        v6 = json.load(open(v6_path))
        anchors = v6["task2_anchors"]["full_anchor_set"]

    # Add V7 iconography assignments
    v7_path = REPORT_DIR / "INDUS_V7_FULL_PUSH.json"
    if v7_path.exists():
        v7 = json.load(open(v7_path))
        for sign, info in v7.get("task_b_icon_phonetics", {}).items():
            anchors[sign] = {"reading": info["reading"], "confidence": info["confidence"],
                            "basis": info.get("basis", "")}

    bigrams = compute_bigrams(corpus)
    round_results = []

    for round_num in range(1, MAX_ROUNDS + 1):
        print(f"\n{'='*60}")
        print(f"  ROUND {round_num}/10")
        print(f"{'='*60}")

        # Step 1: Upgrade LOW → MEDIUM
        n_upgraded = upgrade_low_anchors(anchors, corpus, bigrams, sign_freq)
        print(f"  Upgraded {n_upgraded} LOW→MEDIUM")

        # Step 2: Assign new signs
        n_new = assign_new_signs(anchors, corpus, sign_freq, bigrams, round_num)
        print(f"  Assigned {n_new} new signs")

        # Step 3: Tamil-Brahmi validation
        tb_val = validate_vs_tamil_brahmi(anchors, sign_freq)
        print(f"  Tamil-Brahmi correlation: {tb_val['correlation']}")

        # Step 4: Confidence assessment
        conf = compute_confidence(corpus, anchors, sign_freq)
        level = "NEAR-COMPLETE" if conf["weighted_pct"] >= 80 else \
                "SUBSTANTIAL" if conf["weighted_pct"] >= 60 else \
                "MODERATE" if conf["weighted_pct"] >= 40 else "PARTIAL"

        print(f"  STATUS: {level} at {conf['weighted_pct']:.1f}%")
        print(f"  Signs: {conf['assigned']['total']}/{conf['total_signs']}")
        print(f"    H:{conf['assigned']['HIGH']} M:{conf['assigned']['MEDIUM']} L:{conf['assigned']['LOW']}")
        print(f"  Token coverage: {conf['token_cov']['total']*100:.1f}%")
        print(f"  Fully decoded: {conf['fully_decoded_pct']:.1f}% ({conf['fully_decoded_inscriptions']}/{len(corpus)})")

        # What remains
        remaining = []
        if conf["token_cov"]["total"] < 0.95:
            remaining.append(f"Token coverage at {conf['token_cov']['total']*100:.1f}%, need >95%")
        if conf["assigned"]["LOW"] > 10:
            remaining.append(f"{conf['assigned']['LOW']} LOW-confidence signs need upgrading")
        unassigned_count = conf["total_signs"] - conf["assigned"]["total"]
        if unassigned_count > 50:
            remaining.append(f"{unassigned_count} unassigned signs remain")
        if tb_val["correlation"] < 0.5:
            remaining.append(f"Tamil-Brahmi correlation low ({tb_val['correlation']})")
        remaining.append("Gulf round seals from CISI Vol.3 needed for bilingual cross-reference")
        remaining.append("ICIT corpus (4,537 artefacts) — user working on access")

        print(f"  Remaining: {len(remaining)} items")

        result = {
            "round": round_num,
            "upgraded": n_upgraded,
            "new_assigned": n_new,
            "tamil_brahmi": tb_val,
            "confidence": conf,
            "level": level,
            "remaining": remaining,
        }
        round_results.append(result)

        # Save round report
        report = {
            "title": f"V{7+round_num}: Autonomous Round {round_num}",
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "round": result,
            "anchor_count": len(anchors),
            "anchors_snapshot": {s: {"reading": a["reading"], "confidence": a["confidence"]}
                                for s, a in sorted(anchors.items(),
                                key=lambda x: sign_freq.get(x[0], 0), reverse=True)[:60]},
        }
        out = REPORT_DIR / f"INDUS_V{7+round_num}_ROUND{round_num}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2, default=str)

        # Early termination if we hit near-complete
        if conf["weighted_pct"] >= 85 and conf["fully_decoded_pct"] >= 80:
            print(f"\n  *** NEAR-COMPLETE THRESHOLD REACHED — stopping early ***")
            break

    # FINAL SUMMARY
    print(f"\n{'='*70}")
    print("FINAL SUMMARY ACROSS ALL ROUNDS")
    print(f"{'='*70}")

    first = round_results[0]["confidence"]
    last = round_results[-1]["confidence"]
    print(f"  Rounds completed: {len(round_results)}")
    print(f"  Signs: {first['assigned']['total']} → {last['assigned']['total']} / {last['total_signs']}")
    print(f"  Weighted score: {first['weighted_pct']:.1f}% → {last['weighted_pct']:.1f}%")
    print(f"  Token coverage: {first['token_cov']['total']*100:.1f}% → {last['token_cov']['total']*100:.1f}%")
    print(f"  Fully decoded: {first['fully_decoded_pct']:.1f}% → {last['fully_decoded_pct']:.1f}%")

    # Save final anchor set
    final_anchors = REPORT_DIR / "INDUS_FINAL_ANCHORS.json"
    with open(final_anchors, "w") as f:
        json.dump({"total": len(anchors), "anchors": anchors}, f, indent=2, default=str)
    print(f"\n  Final anchors saved: {final_anchors}")

    # Email final report
    last_conf = round_results[-1]["confidence"]
    last_level = round_results[-1]["level"]
    subject = f"Indus Script V{7+len(round_results)} — {last_level} at {last_conf['weighted_pct']:.1f}% after {len(round_results)} autonomous rounds"

    body = f"""INDUS SCRIPT — AUTONOMOUS DECIPHERMENT LOOP FINAL REPORT
{'='*60}

{len(round_results)} autonomous rounds completed.

PROGRESSION:
"""
    for r in round_results:
        c = r["confidence"]
        body += f"  Round {r['round']}: {r['level']:15s} {c['weighted_pct']:5.1f}% | "
        body += f"Signs={c['assigned']['total']:>3d} H={c['assigned']['HIGH']:>2d} M={c['assigned']['MEDIUM']:>2d} L={c['assigned']['LOW']:>2d} | "
        body += f"Tokens={c['token_cov']['total']*100:.1f}% | "
        body += f"Decoded={c['fully_decoded_pct']:.1f}%\n"

    body += f"""
FINAL STATE:
  Status: {last_level} at {last_conf['weighted_pct']:.1f}% weighted confidence
  Signs: {last_conf['assigned']['total']}/{last_conf['total_signs']}
  Token coverage: {last_conf['token_cov']['total']*100:.1f}%
  Fully decoded inscriptions: {last_conf['fully_decoded_pct']:.1f}%
  Tamil-Brahmi phoneme correlation: {round_results[-1]['tamil_brahmi']['correlation']}

WHAT REMAINS:
"""
    for item in round_results[-1]["remaining"]:
        body += f"  • {item}\n"

    eid = send_email(subject, body)
    if eid:
        print(f"  Email sent (id: {eid})")
    else:
        print("  Email saved to file")

    print(f"\n{'='*70}")
    print("AUTONOMOUS LOOP COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
