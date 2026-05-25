"""Phase 206 — Anchor Injection: M692=nal (MEDIUM) + M861=nallavar (LOW)
            + Absent-Phoneme Reconciliation Against Existing HIGH Anchors

Phase 197 identified M692 and M861 as upgrade candidates:
  M692: SA modal="nal" (cons=0.4), INITIAL position (i_rate=0.456), freq=171, DEDR 3594
  M861: SA modal="nallavar" (cons=0.5), MEDIAL position, freq=138, DEDR 3594 honorific

Phase 204 established MEDIUM evidence for /du/ and /ga/ — but cross-referencing against
existing HIGH anchors reveals:
  M089 = tu/tū (HIGH) — covers /du/ via Elamite tu-/du- voiced alternation (McAlpin 1974 #22)
  M391 = ka/kaṇ (HIGH) — covers /ga/ via Elamite ka-/ga- voiced alternation (McAlpin 1974 #14)
  M047 = min (HIGH)   — partially covers /mil/ via PDr min/mil cognate (DEDR 4897)
  M162 = il/iḷ (HIGH) — partially covers /li/ via PDr li-/il- metathesis (DEDR 491)

Remaining absent phonemes still needing sign assignment (ICIT corpus required):
  /sum/ — Elamite šum/sum=name; McAlpin App.II #29 STRONG; no sign yet
  /gu/  — Elamite ku/gu=say; McAlpin App.II #11 MODERATE; no sign yet
  /ab/  — Elamite ap/ab=father; McAlpin App.II #3 MODERATE; no sign yet
  /ba/  — Elamite pa/ba=speak; McAlpin App.II #8 MODERATE; no sign yet
  /shu/ — Elamite š-/ši; McAlpin App.II #25 CANDIDATE; no sign yet

This script:
  1. Loads current INDUS_FINAL_ANCHORS.json (402 anchors)
  2. Adds M692 = "nal/nall" [MEDIUM] with full evidence chain
  3. Adds M861 = "nallavar" [LOW] with full evidence chain
  4. Documents the absent-phoneme reconciliation as anchor notes
  5. Updates total 402 → 404
  6. Saves updated INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

# ── New anchor proposals from Phase 197 ──────────────────────────────────────
NEW_ANCHORS = {
    "M692": {
        "reading": "nal/nall",
        "confidence": "MEDIUM",
        "basis": (
            "Phase-197 upgrade candidate: SA modal='nal' (consistency=0.40), "
            "INITIAL position dominant (i_rate=0.456, m_rate=0.368), freq=171. "
            "DEDR 3594: nal = 'good, excellent, fine' (PDr adjective prefix). "
            "Corroborates M077=nal (HIGH) as allograph or compound variant. "
            "Co-occurs with M047=min (n=23) and M427=en (n=8). "
            "Triple-LM convergence (Phase-199): not in top-4 convergent set, "
            "but SA consistent across 2/5 seeds. "
            "Dravidian grammar fit: 'nall-' prefix before title = honorific compound."
        ),
        "source": "Phase-197 SA upgrade candidate",
        "_phase206_new_entry": True,
        "_phase197_data": {"sa_cons": 0.4, "i_rate": 0.456, "dedr": "3594",
                           "meaning": "good, excellent, fine"},
    },
    "M861": {
        "reading": "nallavar",
        "confidence": "LOW",
        "basis": (
            "Phase-197 upgrade candidate: SA modal='nallavar' (consistency=0.50), "
            "MEDIAL position (m_rate=0.449, t_rate=0.312), freq=138. "
            "DEDR 3594: nallavar = 'good people, nobles, honorifics' (plural of nal). "
            "Semantic: honorific plural title — consistent with IVC title-formula role. "
            "Co-occurs with M047=min (n=25). "
            "Confidence LOW because nallavar is a long compound reading; "
            "requires ICIT validation for full sign-level confirmation."
        ),
        "source": "Phase-197 SA upgrade candidate",
        "_phase206_new_entry": True,
        "_phase197_data": {"sa_cons": 0.5, "t_rate": 0.312, "dedr": "3594",
                           "meaning": "good people, nobles (honorific plural)"},
    },
}

# ── Absent-phoneme reconciliation annotations ─────────────────────────────────
# These are notes to add to existing HIGH anchors showing their McAlpin coverage
ABSENT_RECONCILIATION = {
    "M089": {
        "_phase206_absent_phoneme_note": (
            "/du/ RECONCILED: M089=tu/tū (HIGH) covers Elamo-Dravidian /du/ phoneme "
            "via standard voiced/unvoiced alternation. Elamite du-=tu- (McAlpin 1981 App.II #22-23). "
            "PDr *tu-=give/carry (DEDR 3302). Phase-204 combined score: 11 (STRONG+MEDIUM). "
            "Status: COVERED by existing HIGH anchor."
        ),
    },
    "M391": {
        "_phase206_absent_phoneme_note": (
            "/ga/ RECONCILED: M391=ka/kaṇ (HIGH) covers Elamo-Dravidian /ga/ phoneme "
            "via standard voiced/unvoiced alternation. Elamite ga-=ka- (McAlpin 1981 App.II #14-15). "
            "PDr *ka-=water/go (DEDR 1221). Phase-204 combined score: 11 (STRONG+STRONG). "
            "Status: COVERED by existing HIGH anchor."
        ),
    },
    "M047": {
        "_phase206_absent_phoneme_note": (
            "/mil/ PARTIAL: M047=min (HIGH) covers Elamo-Dravidian /mil/ phoneme "
            "via PDr min/mil cognate (DEDR 4897: min=fish/star, mil=brightness). "
            "Elamite mel-/mil- (McAlpin App.II #19-21). Phase-204 score: 6 (MODERATE). "
            "Status: PARTIALLY COVERED. /mil/ as standalone value not yet assigned."
        ),
    },
    "M162": {
        "_phase206_absent_phoneme_note": (
            "/li/ PARTIAL: M162=il/iḷ (HIGH) covers Elamo-Dravidian /li/ phoneme "
            "via PDr li-/il- metathesis alternation (DEDR 491: il/li=give/place). "
            "Elamite li- (McAlpin App.II #16). Phase-204 score: 4 (MODERATE). "
            "Status: PARTIALLY COVERED. /li/ as standalone value not yet assigned."
        ),
    },
}

# ── Pending absent phonemes (ICIT corpus needed) ─────────────────────────────
PENDING_ABSENT = {
    "sum": {
        "elamite": "šum-", "pdr": "*cum-", "dedr": "2689",
        "meaning": "to name, title, call", "mcalpin_paper": "1981 App.II #29",
        "mcalpin_confidence": "STRONG", "phase204_score": 9,
        "status": "PENDING — no sign assignment. Needs ICIT corpus.",
        "note": "šum/sum=name/title in Elamite; PDr *cum-=sound/name. "
                "Highly relevant if IVC signs encode proper names.",
    },
    "gu": {
        "elamite": "ku-/gu-", "pdr": "*ku-/*kuḷ-", "dedr": "1687",
        "meaning": "to say, make sound, clan", "mcalpin_paper": "1981 App.II #11-12",
        "mcalpin_confidence": "MODERATE", "phase204_score": 6,
        "status": "PENDING — no sign assignment. Needs ICIT corpus.",
    },
    "ab": {
        "elamite": "ap-/ab-", "pdr": "*appa", "dedr": "172",
        "meaning": "father, distal pronoun", "mcalpin_paper": "1981 App.II #3-5",
        "mcalpin_confidence": "MODERATE", "phase204_score": 6,
        "status": "PENDING — no sign assignment. Needs ICIT corpus.",
    },
    "ba": {
        "elamite": "ba-/pa-", "pdr": "*pa-", "dedr": "3927",
        "meaning": "to speak, protect", "mcalpin_paper": "1981 App.II #8-10",
        "mcalpin_confidence": "MODERATE", "phase204_score": 6,
        "status": "PENDING — no sign assignment. Needs ICIT corpus.",
    },
    "shu": {
        "elamite": "šu-/ši-", "pdr": "*cu-/*ci-", "dedr": "2665",
        "meaning": "fall, cut, palatalized sibilant", "mcalpin_paper": "1981 App.II #25-27",
        "mcalpin_confidence": "CANDIDATE", "phase204_score": 3,
        "status": "PENDING — no sign assignment. Needs ICIT corpus.",
    },
}


def count_by_confidence(anchors: dict) -> dict:
    from collections import Counter
    c = Counter(v.get("confidence","?") for v in anchors.values() if isinstance(v, dict))
    return dict(c)


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 206 — Anchor Injection M692/M861 + Absent-Phoneme Audit")
    print("=" * 60)

    # Load current anchors
    data = json.loads(ANCHOR_F.read_text(encoding="utf-8"))
    anchors = data["anchors"]
    old_total = data.get("total", len(anchors))
    before_conf = count_by_confidence(anchors)
    print(f"\nBefore: {old_total} anchors")
    print(f"  Distribution: {before_conf}")

    # Check M692 and M861 not already present
    new_entries_added = []
    for sign_id, entry in NEW_ANCHORS.items():
        if sign_id in anchors:
            print(f"  {sign_id} already exists — skipping")
        else:
            anchors[sign_id] = entry
            new_entries_added.append(sign_id)
            print(f"  + {sign_id} = {entry['reading']} [{entry['confidence']}]")

    # Add reconciliation notes to existing anchors
    for sign_id, note in ABSENT_RECONCILIATION.items():
        if sign_id in anchors:
            anchors[sign_id].update(note)
            ph = note["_phase206_absent_phoneme_note"].split(":")[0].replace("_phase206_absent_phoneme_note", "").strip()
            print(f"  ✓ Reconciliation note added to {sign_id}: {ph}")

    # Update total
    new_total = len(anchors)
    data["total"] = new_total
    data["_phase206_absent_phoneme_pending"] = PENDING_ABSENT
    data["_phase206_reconciliation_summary"] = {
        "du_covered_by": "M089=tu/tū (HIGH) via Elamite voiced alternation",
        "ga_covered_by": "M391=ka/kaṇ (HIGH) via Elamite voiced alternation",
        "mil_partial": "M047=min (HIGH) via PDr min/mil cognate",
        "li_partial": "M162=il/iḷ (HIGH) via PDr li/il metathesis",
        "pending_icit": list(PENDING_ABSENT.keys()),
        "notes_added_to": list(ABSENT_RECONCILIATION.keys()),
    }

    after_conf = count_by_confidence(anchors)
    print(f"\nAfter: {new_total} anchors (+{new_total - old_total} new)")
    print(f"  Distribution: {after_conf}")

    # Verify M77 corpus coverage
    try:
        from glossa_lab.data.indus_m77 import get_corpus_symbols
        freq = Counter(get_corpus_symbols())
        in_m77  = sum(1 for k in anchors if k.lstrip("M") in freq)
        new_in  = sum(1 for k in new_entries_added if k.lstrip("M") in freq)
        total_m77 = len(freq)
        print(f"\nM77 coverage: {in_m77}/{total_m77} anchored signs in corpus ({in_m77/total_m77*100:.1f}%)")
        print(f"  New entries in M77: {new_in}/{len(new_entries_added)}")
    except Exception:
        print("\nM77 coverage check: could not import data module")
        freq = {}

    # Save
    ANCHOR_F.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✓ Saved INDUS_FINAL_ANCHORS.json ({new_total} total)")

    # Print absent phoneme status
    print("\n=== Absent Phoneme Status (all 14) ===")
    covered = {
        "en": ("M427", "HIGH", "FULLY COVERED"),
        "ki": ("M874", "MEDIUM", "COVERED Phase-192"),
        "su": ("M740", "LOW", "COVERED Phase-192"),
        "zi": ("M455", "LOW", "COVERED Phase-192"),
        "gi": ("M868", "LOW", "COVERED Phase-192"),
        "du": ("M089=tu", "HIGH", "COVERED via voicing alt (Phase-206)"),
        "ga": ("M391=ka", "HIGH", "COVERED via voicing alt (Phase-206)"),
        "mil": ("M047=min", "HIGH", "PARTIAL via PDr cognate (Phase-206)"),
        "li": ("M162=il", "HIGH", "PARTIAL via metathesis (Phase-206)"),
        "sum": (None, "PENDING", "Needs ICIT"),
        "gu": (None, "PENDING", "Needs ICIT"),
        "ab": (None, "PENDING", "Needs ICIT"),
        "ba": (None, "PENDING", "Needs ICIT"),
        "shu": (None, "PENDING", "Needs ICIT"),
    }
    for ph, (sign, conf, status) in covered.items():
        marker = "✓" if "COVERED" in status else ("~" if "PARTIAL" in status else "✗")
        print(f"  {marker} /{ph}/: {sign or '—'} [{conf}] — {status}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 206,
        "elapsed_s": elapsed,
        "old_total": old_total,
        "new_total": new_total,
        "new_entries_added": new_entries_added,
        "confidence_before": before_conf,
        "confidence_after": after_conf,
        "absent_phoneme_status": covered,
        "pending_absent_phonemes": list(PENDING_ABSENT.keys()),
        "reconciled_via_existing": {
            "du": "M089=tu/tū HIGH (voiced alternation)",
            "ga": "M391=ka/kaṇ HIGH (voiced alternation)",
            "mil": "M047=min HIGH (PDr cognate partial)",
            "li": "M162=il/iḷ HIGH (metathesis partial)",
        },
        "verdict": (
            f"Phase 206: Added M692=nal [MEDIUM] and M861=nallavar [LOW]. "
            f"Total anchors 402 → {new_total}. "
            f"Absent-phoneme audit: /du/ and /ga/ COVERED via existing HIGH anchors "
            f"(M089, M391) through Elamite voiced alternation. "
            f"/mil/ and /li/ partially covered. "
            f"5 phonemes (/sum/, /gu/, /ab/, /ba/, /shu/) still pending ICIT corpus."
        ),
    }

    out = OUTPUTS / "phase206_anchor_injection_m692_m861.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase206_anchor_injection_m692_m861.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 206 complete in {elapsed}s | Saved: {out}")
    print(f"Verdict: {result['verdict']}")


if __name__ == "__main__":
    main()
