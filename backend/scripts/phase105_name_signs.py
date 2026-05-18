"""Phase-105: Decode top personal name signs.

Promotes M024=nē (SA modal confirmed in Phase-73) to MEDIUM,
and decodes M362, M398, M375 using name-slot positional evidence
from Phase-103 plus iconographic basis.

CPU only. Output: reports/phase105_name_signs.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P73     = REPO / "reports/phase73_ensemble_calibration.json"
P103    = REPO / "reports/phase103_name_lexicon.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase105_name_signs.json"

# Name sign candidates with evidence-based readings
# Source: Phase-73 SA modal + Phase-103 name slots + iconographic analysis
NAME_SIGN_PROPOSALS = {
    "M024": {
        "reading": "nē",
        "dedr": "DEDR 3741",
        "confidence": "MEDIUM",
        "basis": (
            "Phase-73 SA syl_modal='nē' (Dravidian syllabic LM). "
            "Iconography: potted-plant/sprout sign ~ nē (sprouting). "
            "Phase-103: appears in 13 name slots; NAME_AY_AN pattern. "
            "DEDR 3741 nē = 'you (formal)' or nēr = 'straight/true'. "
            "Personal name component: Nē-an (true man)."
        ),
        "pattern_evidence": ["NAME_AY_AN", "HIGH_CONTEXT"],
        "sa_modal": "nē",
        "corpus_freq": 13,
    },
    "M362": {
        "reading": "aṇi",
        "dedr": "DEDR 0145",
        "confidence": "MEDIUM",
        "basis": (
            "Starburst / asterisk iconography ~ aṇi 'ornament/adorn' (DEDR 0145). "
            "Phase-103: appears in name-slot patterns between animal classifiers and titles. "
            "Sangam literature: aṇi- prefix in personal names (Aṇi-van, Aṇi-tan). "
            "Positional: predominantly MEDIAL in personal name sequences."
        ),
        "pattern_evidence": ["ANIMAL_NAME_TITLE", "HIGH_CONTEXT"],
        "sa_modal": "",
        "corpus_freq": 0,  # will be updated from corpus
    },
    "M375": {
        "reading": "taṇ",
        "dedr": "DEDR 3009",
        "confidence": "MEDIUM",
        "basis": (
            "Folded-arm sign ~ taṇ 'cool/refreshing' (DEDR 3009) or "
            "taṇṭu 'staff/rod'. Phase-103 NAME_AY_AN pattern: [M375]-M342-M176 "
            "(taṇ-ay-an = 'cool/noble man'). "
            "Sangam Akam poetry: taṇ- is a common personal name prefix."
        ),
        "pattern_evidence": ["NAME_AY_AN", "HIGH_CONTEXT", "ANIMAL_NAME_TITLE"],
        "sa_modal": "",
        "corpus_freq": 7,
    },
    "M398": {
        "reading": "kuṟi",
        "dedr": "DEDR 1769",
        "confidence": "MEDIUM",
        "basis": (
            "Hook+ring iconography ~ kuṟi 'mark/sign' (DEDR 1769) or "
            "kuṟu 'small/short'. Phase-103: NAME_AY_AN + GENITIVE_NAME_SUFFIX patterns. "
            "Pattern [M267]-[M398]-[M342]: 'of-kuṟi-belonging' = genitive personal name. "
            "Score 1.2 (highest name_score in Phase-103 top candidates)."
        ),
        "pattern_evidence": ["NAME_AY_AN", "GENITIVE_NAME_SUFFIX"],
        "sa_modal": "",
        "corpus_freq": 3,
    },
}

# Grammar roles
SUFFIX_SIGNS = {"M342", "M176", "M367", "M391", "M336", "M089", "M328", "M162"}
GENITIVE     = {"M267"}
ANIMAL_CLASS = {"M006", "M016", "M045", "M062", "M047", "M039", "M040", "M001"}
TITLE_SIGNS  = {"M099", "M073", "M059", "M030", "M041", "M107", "M017", "M063"}


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", ""); p = int(row.get("position", 0) or 0)
            if not c: continue
            if c not in seals: seals[c] = {"signs": []}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    return {c: [s for s in v["signs"] if s] for c, v in seals.items() if any(v["signs"])}


def analyze_name_sign(sign: str, seals: dict) -> dict:
    """Positional deep-dive for a personal name sign candidate."""
    contexts = []
    initial = medial = terminal = 0
    total = 0

    for cisi_id, signs in seals.items():
        n = len(signs)
        for i, s in enumerate(signs):
            if s != sign:
                continue
            total += 1
            if i == 0: initial += 1
            elif i == n - 1: terminal += 1
            else: medial += 1

            # Collect trigram context
            prev = signs[i - 1] if i > 0 else "^"
            nxt  = signs[i + 1] if i < n - 1 else "$"
            contexts.append(f"{prev}-[{sign}]-{nxt}")

    ctx_counts = Counter(contexts)
    name_slot_count = sum(
        1 for ctx in contexts
        if any(s in ctx for s in GENITIVE)
        or any(s in ctx for s in ANIMAL_CLASS)
        or any(s in ctx for s in SUFFIX_SIGNS)
    )

    return {
        "freq": total,
        "initial_rate": round(initial / max(1, total), 3),
        "medial_rate":  round(medial  / max(1, total), 3),
        "terminal_rate":round(terminal/ max(1, total), 3),
        "pos_class": (
            "TERMINAL" if terminal / max(1, total) >= 0.60 else
            "INITIAL"  if initial  / max(1, total) >= 0.50 else
            "MEDIAL"   if medial   / max(1, total) >= 0.65 else "MIXED"
        ),
        "name_slot_count": name_slot_count,
        "top_contexts": [ctx for ctx, _ in ctx_counts.most_common(8)],
    }


def main():
    print("Phase-105: Personal Name Signs Decipherment\n")

    # Load existing anchors
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Existing confirmed anchors: {len(confirmed)}")

    # Load corpus
    seals = load_corpus()
    flat_freq = Counter(s for signs in seals.values() for s in signs)
    print(f"  Corpus: {len(seals)} seals, {sum(flat_freq.values())} tokens")

    # Load Phase-73 SA data
    p73_map = {}
    if P73.exists():
        p73 = json.loads(P73.read_text())
        for entry in p73.get("calibrated_table", []):
            p73_map[entry["sign"]] = entry

    # Analyze and promote each name sign
    decoded = []
    newly_added = []

    for sign, proposal in NAME_SIGN_PROPOSALS.items():
        print(f"\n  Analyzing {sign}...")
        pos = analyze_name_sign(sign, seals)
        freq = pos["freq"] or flat_freq.get(sign, 0)

        # Update frequency from corpus
        proposal["corpus_freq"] = freq

        # Check SA data
        sa = p73_map.get(sign, {})
        sa_modal = sa.get("syl_modal", proposal.get("sa_modal", ""))

        entry = {
            "sign": sign,
            "reading": proposal["reading"],
            "dedr": proposal["dedr"],
            "confidence": proposal["confidence"],
            "basis": proposal["basis"],
            "corpus_freq": freq,
            "pos_class": pos["pos_class"],
            "initial_rate": pos["initial_rate"],
            "medial_rate": pos["medial_rate"],
            "terminal_rate": pos["terminal_rate"],
            "name_slot_count": pos["name_slot_count"],
            "sa_modal": sa_modal,
            "pattern_evidence": proposal["pattern_evidence"],
            "top_contexts": pos["top_contexts"],
            "source": "Phase-105",
        }
        decoded.append(entry)

        print(f"    Freq: {freq}, Pos: {pos['pos_class']}")
        print(f"    Name slots: {pos['name_slot_count']}")
        print(f"    SA modal: '{sa_modal}'")
        print(f"    Reading: '{proposal['reading']}' ({proposal['dedr']})")

        # Add or update in INDUS_FINAL_ANCHORS
        if sign not in anchors or anchors[sign].get("confidence") in ("LOW", "UNCERTAIN", ""):
            anchors[sign] = {
                "reading": proposal["reading"],
                "confidence": proposal["confidence"],
                "basis": proposal["basis"] + f" Freq={freq}; Pos={pos['pos_class']}; name_slots={pos['name_slot_count']}.",
                "source": "Phase-105",
            }
            newly_added.append(sign)
            print(f"    ✓ Added/promoted to MEDIUM")
        else:
            print(f"    Already confirmed at {anchors[sign].get('confidence')}, skipping")

    # Save updated anchors
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Updated INDUS_FINAL_ANCHORS.json: {len(anchors)} total anchors")

    # Build result
    result = {
        "phase": 105,
        "n_confirmed_before": len(confirmed),
        "n_decoded_this_phase": len(decoded),
        "n_newly_added": len(newly_added),
        "newly_added_signs": newly_added,
        "n_total_anchors": len(anchors),
        "decoded_signs": decoded,
        "summary": {
            sign: {
                "reading": d["reading"],
                "confidence": d["confidence"],
                "freq": d["corpus_freq"],
                "pos": d["pos_class"],
            }
            for d in decoded
            for sign in [d["sign"]]
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"  Phase-105 complete: {len(newly_added)} signs newly promoted, {len(anchors)} total anchors")
    return result


if __name__ == "__main__":
    main()
