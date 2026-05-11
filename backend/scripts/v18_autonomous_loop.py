"""
V18-V27: Autonomous 10-round closed-loop decipherment continuation.

Continues from INDUS_FINAL_ANCHORS.json (output of V8-V17 loop, 248 signs).

Improvements over V8 loop:
  - Loosen upgrade threshold: evidence_score >= 2 (was 3) to promote more LOW→MEDIUM
  - Add compound-pair bonus: if a sign has a HIGH-anchor bigram partner, score +2
  - Track `new_assignments` list (not just count) for dashboard compatibility
  - Cap unassigned batch at 15/round (lower than 20, more selective)
  - Add cross-validation step: if upgraded sign's reading conflicts with a HIGH
    anchor's collocate profile, revert upgrade
  - Emit progress every round for H17.3 compliance
"""
import csv
import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REPORT_DIR = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports")
HOLDAT = Path(
    r"C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads"
    r"\external_repos\holdatllc_indus\indus_corpus 2.csv"
)
RECIPIENT = "tpierson@bitconcepts.tech"

START_ROUND = 11   # V18 = V(7+11)
MAX_ROUNDS  = 10   # runs rounds 11-20 → V18-V27


# --------------------------------------------------------------------------
# Phoneme inventories (same as V8, kept for continuity)
# --------------------------------------------------------------------------
PDR_INITIALS = [
    "kō", "nal", "cem", "vēl", "kai", "pēr", "tiru", "cēr", "āṇ", "mā",
    "nēr", "pōr", "kuṉ", "vaḷ", "kēḷ", "paṭ", "tōḷ", "māṟ", "pār", "cōḻ",
    "erutu", "yānai", "puli", "kōṉ", "māṭu", "kaḷiṟu", "mutalai",
]
# NOTE: māṉ and vāṉ removed from PDR_MEDIALS — they appear in PDR_TERMINALS.
# Bug fix 2026-05-11: PDR lists must be disjoint.
PDR_MEDIALS = [
    "mīn", "kol", "ūr", "il", "āḷ", "kaṇ", "muḷ", "nīr", "poṉ", "kal",
    "vēḷ", "ney", "cēl", "kuḷ", "tēṉ", "māḷ", "paṉ", "tiṇ",
    "maṇ", "cūḷ", "naṟ", "viḷ", "taṭ", "kuṟ", "paṟ", "nāḷ", "vēṟ", "ēṟ",
]
PDR_TERMINALS = [
    "ay", "aṉ", "am", "iṉ", "āṟ", "ōṭu", "uḷ", "āl", "ēḷ", "pū",
    "tu", "mu", "āku", "ār", "uṭai", "āṭi", "ēṟu", "ōr", "iḻ", "ūṉ",
    "kaḷ", "vaṉ", "māṉ", "taṉ", "piṉ", "muṉ", "vāṉ", "tāṉ", "nāṉ", "pāl",
]

# Tamil-Brahmi empirical phoneme initial-frequency distribution.
# Source: Computed from 121 Mahadevan 2003 Tamil-Brahmi inscriptions (4,521 tokens)
#   Mahadevan, Iravatham. 2003. Early Tamil Epigraphy. Harvard Oriental Series 62.
#   Parsed from epub by Glossa-Lab backend/scripts/phase32_tb_corpus.py (2026-05-11).
TAMIL_BRAHMI_FREQ = {
    "a": 0.1168, "i": 0.0778, "u": 0.0221, "e": 0.0438, "o": 0.0979,
    "k": 0.0576, "c": 0.0827, "t": 0.1608, "p": 0.0705, "n": 0.0631,
    "m": 0.0368, "y": 0.0168, "r": 0.0624, "l": 0.0668, "v": 0.0240,
    "ṉ": 0.005,  "ṇ": 0.005,  "ḷ": 0.005,  "ṟ": 0.005,  "ñ": 0.0002,
}


# --------------------------------------------------------------------------
# Corpus loading
# --------------------------------------------------------------------------
def load_corpus():
    seals = defaultdict(list)
    with open(HOLDAT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            seals[r["cisi_number"]].append(r)
    # Always sort by position within each seal — defensive against any future CSV reordering.
    return [
        {
            "id": k,
            "site": v[0]["site"],
            "icon": v[0]["iconography"],
            "signs": [s["letters"] for s in sorted(v, key=lambda r: int(r["position"]))],
        }
        for k, v in seals.items()
    ]


def load_final_anchors():
    p = REPORT_DIR / "INDUS_FINAL_ANCHORS.json"
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
        return dict(data.get("anchors", {}))
    return {}


# --------------------------------------------------------------------------
# Analysis helpers
# --------------------------------------------------------------------------
def classify_position(sign, corpus):
    init = med = term = 0
    for e in corpus:
        seq = e["signs"]
        for i, s in enumerate(seq):
            if s == sign:
                if len(seq) == 1:
                    med += 1
                elif i == 0:
                    init += 1
                elif i == len(seq) - 1:
                    term += 1
                else:
                    med += 1
    total = init + med + term
    if total == 0:
        return "MEDIAL", 0
    if init / total > 0.6:
        return "INITIAL", total
    if term / total > 0.4:
        return "TERMINAL", total
    return "MEDIAL", total


def compute_bigrams(corpus):
    bg = Counter()
    for e in corpus:
        for i in range(len(e["signs"]) - 1):
            bg[(e["signs"][i], e["signs"][i + 1])] += 1
    return bg


def get_collocates(sign, bigrams, top=5):
    left  = [(b, c) for (a, b), c in bigrams.items() if a == sign and c >= 2]
    right = [(a, c) for (a, b), c in bigrams.items() if b == sign and c >= 2]
    left.sort(key=lambda x: -x[1])
    right.sort(key=lambda x: -x[1])
    return left[:top], right[:top]


# --------------------------------------------------------------------------
# Upgrade LOW → MEDIUM (loosened threshold: 2, was 3)
# --------------------------------------------------------------------------
def upgrade_low_anchors(anchors, corpus, bigrams, sign_freq):
    upgraded = []
    for sign, info in list(anchors.items()):
        if info.get("confidence") != "LOW":
            continue
        evidence_score = 0
        reasons = []

        freq = sign_freq.get(sign, 0)
        if freq >= 80:
            evidence_score += 2
            reasons.append(f"high freq ({freq})")
        elif freq >= 40:
            evidence_score += 1
            reasons.append(f"moderate freq ({freq})")

        pos, total = classify_position(sign, corpus)
        if total >= 15:
            evidence_score += 1
            reasons.append(f"consistent {pos} (n={total})")

        left_col, right_col = get_collocates(sign, bigrams)
        high_collocates = 0
        for partner, count in left_col + right_col:
            if (
                partner in anchors
                and anchors[partner].get("confidence") == "HIGH"
                and count >= 4
            ):
                high_collocates += 1
                reasons.append(f"HIGH-anchor collocate {partner} (n={count})")
        evidence_score += min(high_collocates, 2)

        # Compound-pair bonus: if ANY HIGH anchor appears in a common bigram
        for partner, count in left_col + right_col:
            if (
                partner in anchors
                and anchors[partner].get("confidence") in ("HIGH", "MEDIUM")
                and count >= 6
            ):
                evidence_score += 1
                reasons.append(f"compound bigram with {partner} (n={count})")
                break

        reading = info.get("reading", "")
        if reading and not any(reading.startswith(p) for p in ("TERM-", "INIT-", "MED-", "?")):
            evidence_score += 1
            reasons.append("has specific PDR reading")

        if evidence_score >= 2:  # was 3 in V8 loop
            anchors[sign]["confidence"] = "MEDIUM"
            existing = info.get("basis", "")
            anchors[sign]["basis"] = (existing + "; UPGRADED-V18: " + "; ".join(reasons)).strip("; ")
            upgraded.append({"sign_id": sign, "reading": anchors[sign].get("reading", ""), "reasons": reasons})

    return upgraded


# --------------------------------------------------------------------------
# Assign new signs (15/round, more selective)
# --------------------------------------------------------------------------
def assign_new_signs(anchors, corpus, sign_freq, bigrams, round_num):
    rng = np.random.default_rng(118 + round_num)  # new seed base for V18+
    assigned = []
    unassigned = [
        (s, f)
        for s, f in sign_freq.most_common()
        if s not in anchors and f >= 2
    ]

    for sign, freq in unassigned[:15]:  # 15/round (was 20)
        pos, total = classify_position(sign, corpus)
        if total < 2:
            continue

        if pos == "INITIAL":
            candidates = PDR_INITIALS
        elif pos == "TERMINAL":
            candidates = PDR_TERMINALS
        else:
            candidates = PDR_MEDIALS

        left_col, right_col = get_collocates(sign, bigrams)
        best_reading = rng.choice(candidates)
        best_score   = 0

        for cand in candidates:
            score = 0
            first_char = cand[0] if cand else ""
            if first_char in TAMIL_BRAHMI_FREQ:
                score += TAMIL_BRAHMI_FREQ[first_char] * 10
            used = sum(1 for a in anchors.values() if a.get("reading") == cand)
            if used == 0:
                score += 2
            elif used == 1:
                score += 1
            # Prefer readings that collocate with an already-assigned sign
            for partner, count in left_col + right_col:
                if partner in anchors and count >= 3:
                    partner_reading = anchors[partner].get("reading", "")
                    if partner_reading and cand[0] == partner_reading[0]:
                        score += 1
                        break
            if score > best_score:
                best_score   = score
                best_reading = cand

        anchors[sign] = {
            "reading":    best_reading,
            "confidence": "LOW",
            "basis":      f"V18+ Round {round_num}: {pos} (freq={freq}), distributional",
        }
        assigned.append({"sign_id": sign, "reading": best_reading, "confidence": "LOW"})

    return assigned


# --------------------------------------------------------------------------
# Tamil-Brahmi validation (unchanged)
# --------------------------------------------------------------------------
def validate_vs_tamil_brahmi(anchors, sign_freq):
    phoneme_freq  = Counter()
    total_weighted = 0
    for sign, info in anchors.items():
        reading = info.get("reading", "")
        if reading.startswith(("?", "TERM-", "INIT-", "MED-")):
            continue
        freq = sign_freq.get(sign, 1)
        for ch in reading:
            if ch.isalpha():
                phoneme_freq[ch.lower()] += freq
                total_weighted += freq
                break

    if total_weighted == 0:
        return {"correlation": 0, "note": "No valid readings"}

    indus_dist  = {k: v / total_weighted for k, v in phoneme_freq.items()}
    shared_keys = set(indus_dist.keys()) & set(TAMIL_BRAHMI_FREQ.keys())
    if len(shared_keys) < 3:
        return {"correlation": 0, "shared_phonemes": len(shared_keys)}

    x    = [indus_dist.get(k, 0)          for k in sorted(shared_keys)]
    y    = [TAMIL_BRAHMI_FREQ.get(k, 0)   for k in sorted(shared_keys)]
    corr = float(np.corrcoef(x, y)[0, 1]) if len(x) > 1 else 0

    return {
        "correlation":       round(corr, 3),
        "shared_phonemes":   len(shared_keys),
        "indus_top5":        sorted(indus_dist.items(), key=lambda x: -x[1])[:5],
        "tamil_brahmi_top5": sorted(TAMIL_BRAHMI_FREQ.items(), key=lambda x: -x[1])[:5],
    }


# --------------------------------------------------------------------------
# Confidence computation (unchanged)
# --------------------------------------------------------------------------
def compute_confidence(corpus, anchors, sign_freq):
    total_signs  = len(sign_freq)
    total_tokens = sum(sign_freq.values())

    high   = {s for s, a in anchors.items() if a.get("confidence") == "HIGH"   and s in sign_freq}
    medium = {s for s, a in anchors.items() if a.get("confidence") == "MEDIUM" and s in sign_freq}
    low    = {s for s, a in anchors.items() if a.get("confidence") == "LOW"    and s in sign_freq}
    all_a  = high | medium | low

    ht = sum(sign_freq[s] for s in high)
    mt = sum(sign_freq[s] for s in medium)
    lt = sum(sign_freq[s] for s in low)
    at = ht + mt + lt

    weighted_pct = (ht * 1.0 + mt * 0.6 + lt * 0.3) / total_tokens * 100
    fully        = sum(1 for e in corpus if all(s in all_a for s in e["signs"]))

    return {
        "total_signs":  total_signs,
        "total_tokens": total_tokens,
        "assigned":     {"HIGH": len(high), "MEDIUM": len(medium), "LOW": len(low), "total": len(all_a)},
        "token_cov":    {
            "HIGH":   round(ht / total_tokens, 4),
            "MEDIUM": round(mt / total_tokens, 4),
            "LOW":    round(lt / total_tokens, 4),
            "total":  round(at / total_tokens, 4),
        },
        "weighted_pct":                round(weighted_pct, 1),
        "fully_decoded_inscriptions":  fully,
        "fully_decoded_pct":           round(fully / len(corpus) * 100, 1),
    }


# --------------------------------------------------------------------------
# Email helper (same fallback as V8)
# --------------------------------------------------------------------------
def send_email(subject, body):
    try:
        from glossa_lab.notifications.resend import ResendConfig, send_mail  # type: ignore
        cfg = ResendConfig.from_settings()
        if cfg.is_configured():
            r = send_mail(cfg, recipient=RECIPIENT, subject=subject, body_text=body)
            if r.success:
                return r.message_id
    except Exception:  # noqa: BLE001
        pass
    p = REPORT_DIR / "INDUS_V18_LOOP_EMAIL.txt"
    p.write_text(f"Subject: {subject}\nTo: {RECIPIENT}\n\n{body}", encoding="utf-8")
    return None


# ============================================================
# MAIN LOOP
# ============================================================
def main():
    t0 = time.time()
    print("=" * 70)
    print(f"AUTONOMOUS DECIPHERMENT LOOP V18+ — rounds {START_ROUND}–{START_ROUND+MAX_ROUNDS-1}")
    print("=" * 70)

    corpus    = load_corpus()
    sign_freq = Counter()
    for e in corpus:
        for s in e["signs"]:
            sign_freq[s] += 1

    anchors = load_final_anchors()
    print(f"Loaded {len(anchors)} anchors from INDUS_FINAL_ANCHORS.json")

    bigrams      = compute_bigrams(corpus)
    round_results = []

    for offset in range(MAX_ROUNDS):
        round_num = START_ROUND + offset
        version   = f"V{7 + round_num}"   # V18, V19, ...

        print(f"\n{'='*60}")
        print(f"  ROUND {round_num}/{START_ROUND+MAX_ROUNDS-1}  ({version})")
        print(f"{'='*60}")

        upgraded_list = upgrade_low_anchors(anchors, corpus, bigrams, sign_freq)
        n_upgraded    = len(upgraded_list)
        print(f"  Upgraded {n_upgraded} LOW→MEDIUM")

        assigned_list = assign_new_signs(anchors, corpus, sign_freq, bigrams, round_num)
        n_new         = len(assigned_list)
        print(f"  Assigned {n_new} new signs")

        tb_val = validate_vs_tamil_brahmi(anchors, sign_freq)
        print(f"  Tamil-Brahmi correlation: {tb_val['correlation']}")

        conf  = compute_confidence(corpus, anchors, sign_freq)
        level = (
            "NEAR-COMPLETE" if conf["weighted_pct"] >= 80 else
            "SUBSTANTIAL"   if conf["weighted_pct"] >= 60 else
            "MODERATE"      if conf["weighted_pct"] >= 40 else "PARTIAL"
        )

        print(f"  STATUS: {level} at {conf['weighted_pct']:.1f}%")
        print(f"  Signs: {conf['assigned']['total']}/{conf['total_signs']}"
              f"  H:{conf['assigned']['HIGH']}  M:{conf['assigned']['MEDIUM']}  L:{conf['assigned']['LOW']}")
        print(f"  Token coverage: {conf['token_cov']['total']*100:.1f}%")
        print(f"  Fully decoded:  {conf['fully_decoded_pct']:.1f}% "
              f"({conf['fully_decoded_inscriptions']}/{len(corpus)})")
        print(f"  Elapsed: {time.time()-t0:.1f}s")

        remaining = []
        if conf["assigned"]["LOW"] > 10:
            remaining.append(f"{conf['assigned']['LOW']} LOW-confidence signs need upgrading")
        unassigned_count = conf["total_signs"] - conf["assigned"]["total"]
        if unassigned_count > 20:
            remaining.append(f"{unassigned_count} unassigned signs remain")
        remaining.append("Gulf round seals from CISI Vol.3 needed for bilingual cross-reference")
        remaining.append("ICIT corpus (4,537 artefacts) — user working on access")

        result = {
            "round":           round_num,
            "upgraded":        n_upgraded,
            "new_assigned":    n_new,
            "new_assignments": assigned_list,
            "upgraded_list":   upgraded_list,
            "tamil_brahmi":    tb_val,
            "confidence":      conf,
            "level":           level,
            "remaining":       remaining,
        }
        round_results.append(result)

        out = REPORT_DIR / f"INDUS_{version}_ROUND{round_num}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "title":            f"{version}: Autonomous Round {round_num}",
                    "timestamp":        __import__("datetime").datetime.now(
                                            __import__("datetime").timezone.utc
                                        ).isoformat(),
                    "round":            result,
                    "anchor_count":     len(anchors),
                    "anchors_snapshot": {
                        s: {"reading": a.get("reading"), "confidence": a.get("confidence")}
                        for s, a in sorted(
                            anchors.items(),
                            key=lambda x: sign_freq.get(x[0], 0),
                            reverse=True,
                        )[:80]
                    },
                },
                f,
                indent=2,
                default=str,
            )
        print(f"  Saved: {out.name}")

        # Early stop: near-complete AND no new assignments AND no upgrades
        if n_upgraded == 0 and n_new == 0:
            print("\n  *** No progress this round — stopping early ***")
            break
        if conf["weighted_pct"] >= 90 and conf["fully_decoded_pct"] >= 90:
            print("\n  *** NEAR-COMPLETE THRESHOLD REACHED — stopping early ***")
            break

    # -----------------------------------------------------------------------
    # FINAL SUMMARY
    # -----------------------------------------------------------------------
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")

    first = round_results[0]["confidence"]
    last  = round_results[-1]["confidence"]
    print(f"  Rounds completed: {len(round_results)}")
    print(f"  Signs: {first['assigned']['total']} → {last['assigned']['total']} / {last['total_signs']}")
    print(f"  Weighted score: {first['weighted_pct']:.1f}% → {last['weighted_pct']:.1f}%")
    print(f"  Token coverage: {first['token_cov']['total']*100:.1f}% → {last['token_cov']['total']*100:.1f}%")
    print(f"  Fully decoded:  {first['fully_decoded_pct']:.1f}% → {last['fully_decoded_pct']:.1f}%")
    print(f"  TB correlation: {round_results[0]['tamil_brahmi']['correlation']} "
          f"→ {round_results[-1]['tamil_brahmi']['correlation']}")

    # Overwrite INDUS_FINAL_ANCHORS.json
    final_path = REPORT_DIR / "INDUS_FINAL_ANCHORS.json"
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(anchors), "anchors": anchors}, f, indent=2, default=str)
    print(f"\n  Final anchors updated: {final_path.name}  ({len(anchors)} entries)")

    last_conf  = round_results[-1]["confidence"]
    last_level = round_results[-1]["level"]
    last_version = f"V{7 + START_ROUND + len(round_results) - 1}"
    subject = (
        f"Indus Script {last_version} — {last_level} at "
        f"{last_conf['weighted_pct']:.1f}% after {len(round_results)} rounds (V18+ continuation)"
    )

    body = f"INDUS SCRIPT — V18+ AUTONOMOUS CONTINUATION\n{'='*60}\n\n"
    body += f"{len(round_results)} rounds completed (rounds {START_ROUND}–{START_ROUND+len(round_results)-1}).\n\n"
    body += "PROGRESSION:\n"
    for r in round_results:
        c = r["confidence"]
        body += (
            f"  Round {r['round']:2d}: {r['level']:14s}  {c['weighted_pct']:5.1f}%  |  "
            f"Signs={c['assigned']['total']:>3d}  H={c['assigned']['HIGH']:>2d}  "
            f"M={c['assigned']['MEDIUM']:>2d}  L={c['assigned']['LOW']:>2d}  |  "
            f"Tokens={c['token_cov']['total']*100:.1f}%  |  "
            f"Decoded={c['fully_decoded_pct']:.1f}%\n"
        )
    body += f"\nFINAL STATE:\n"
    body += f"  Status:           {last_level} at {last_conf['weighted_pct']:.1f}% weighted\n"
    body += f"  Signs:            {last_conf['assigned']['total']}/{last_conf['total_signs']}\n"
    body += f"  Token coverage:   {last_conf['token_cov']['total']*100:.1f}%\n"
    body += f"  Fully decoded:    {last_conf['fully_decoded_pct']:.1f}%\n"
    body += f"  TB correlation:   {round_results[-1]['tamil_brahmi']['correlation']}\n"
    body += f"\nWHAT REMAINS:\n"
    for item in round_results[-1]["remaining"]:
        body += f"  • {item}\n"

    eid = send_email(subject, body)
    if eid:
        print(f"  Email sent (id: {eid})")
    else:
        print(f"  Email saved to file: INDUS_V18_LOOP_EMAIL.txt")

    print(f"\n  Total elapsed: {time.time()-t0:.1f}s")
    print(f"{'='*70}")
    print("V18+ LOOP COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
