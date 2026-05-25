"""Phase 209 -- Anchor injection M712=nallavar [LOW] + M817=nallavar [LOW]
              404 -> 406 anchors

Phase 207 top-unanchored signals:
  M712: modal=nallavar cons=0.400 freq=43  (MEDIAL dominant)
  M817: modal=nallavar cons=0.400 freq=107 (MEDIAL dominant)

Both signs converge on 'nallavar' (good people/nobles, DEDR 3594), matching
the already-anchored M861=nallavar [LOW]. These appear to be allographs or
compound variants of the nallavar honorific cluster (M077=nal HIGH, M692=nal/nall
MEDIUM, M861=nallavar LOW). Adding both at LOW confidence.

Also adding M700=aru [CANDIDATE] (freq=355, cons=0.400):
  Tamil aru = six (aaRu, DEDR 338) OR distal pronoun (av/ar, DEDR 255)
  Very high frequency (3rd most common in M77). MEDIAL dominant (0.834).
  Candidate status pending DEDR disambiguation.
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

NEW_ANCHORS = {
    "M712": {
        "reading": "nallavar",
        "confidence": "LOW",
        "basis": (
            "Phase-207 unanchored convergence: SA modal='nallavar' (cons=0.40 across 5 seeds). "
            "MEDIAL position dominant. freq=43. DEDR 3594: nallavar='good people/nobles'. "
            "Corroborates M861=nallavar [LOW] as allograph or inscriptional variant. "
            "Honorific plural consistent with title-formula grammar."
        ),
        "source": "Phase-207 SA unanchored convergence",
        "_phase209_new_entry": True,
    },
    "M817": {
        "reading": "nallavar",
        "confidence": "LOW",
        "basis": (
            "Phase-207 unanchored convergence: SA modal='nallavar' (cons=0.40 across 5 seeds). "
            "MEDIAL position dominant. freq=107. DEDR 3594: nallavar='good people/nobles'. "
            "High frequency (107) suggests core title-formula sign. Third nallavar cluster entry "
            "(alongside M861 [LOW] and M712 [LOW]), pointing to nallavar as productive "
            "title formula element in IVC epigraphy."
        ),
        "source": "Phase-207 SA unanchored convergence",
        "_phase209_new_entry": True,
    },
    "M700": {
        "reading": "aru/aRu",
        "confidence": "CANDIDATE",
        "basis": (
            "Phase-207 unanchored: SA modal='aru' (cons=0.40). MEDIAL dominant (m_rate=0.834). "
            "Very high frequency (freq=355, 3rd most common M77 sign). "
            "PDr candidates: (1) aaRu=six (DEDR 338, Tamil numeral) -- would pair with "
            "M059=7 numeral anchor; (2) av/ar=he/it distal pronoun (DEDR 255). "
            "CANDIDATE status pending DEDR disambiguation. Numeral interpretation preferred "
            "given M059=7 precedent and MEDIAL position (numerals appear in counting context)."
        ),
        "source": "Phase-207 SA unanchored convergence",
        "_phase209_new_entry": True,
    },
    "M527": {
        "reading": "katai",
        "confidence": "CANDIDATE",
        "basis": (
            "Phase-207 unanchored: SA modal='katai' (cons=0.40). freq=60. "
            "PDr katai = story, end, last (DEDR 1161) OR shop/bazaar (Tamil katai). "
            "CANDIDATE status: katai as terminal marker would fit TERMINAL position context. "
            "Semantic: 'end-of-inscription marker' or 'trade location' compatible with "
            "IVC commercial seal interpretation."
        ),
        "source": "Phase-207 SA unanchored convergence",
        "_phase209_new_entry": True,
    },
}


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 209 -- Anchor injection M712/M817/M700/M527")
    print("=" * 60)

    data = json.loads(ANCHOR_F.read_text(encoding="utf-8"))
    anchors = data["anchors"]
    old_total = data.get("total", len(anchors))

    from collections import Counter as C
    before = dict(C(v.get("confidence","?") for v in anchors.values() if isinstance(v, dict)))
    print(f"\nBefore: {old_total} anchors | {before}")

    added = []
    for sign_id, entry in NEW_ANCHORS.items():
        if sign_id in anchors:
            print(f"  {sign_id} already present -- skipping")
        else:
            anchors[sign_id] = entry
            added.append(sign_id)
            print(f"  + {sign_id} = {entry['reading']} [{entry['confidence']}]")

    new_total = len(anchors)
    data["total"] = new_total
    after = dict(C(v.get("confidence","?") for v in anchors.values() if isinstance(v, dict)))

    try:
        from glossa_lab.data.indus_m77 import get_corpus_symbols
        freq = Counter(get_corpus_symbols())
        in_m77 = sum(1 for k in anchors if k.lstrip("M") in freq)
        print(f"\nM77 coverage: {in_m77}/{len(freq)} signs anchored ({in_m77/len(freq)*100:.1f}%)")
    except Exception:
        pass

    ANCHOR_F.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nAfter: {new_total} anchors (+{new_total-old_total}) | {after}")

    elapsed = round(time.time()-t0, 1)
    result = {
        "phase": 209, "elapsed_s": elapsed,
        "old_total": old_total, "new_total": new_total,
        "new_entries_added": added,
        "confidence_after": after,
        "verdict": (
            f"Phase 209: Added {len(added)} entries. Total {old_total} -> {new_total}. "
            f"M712/M817=nallavar [LOW] (honorific cluster expansion). "
            f"M700=aru [CANDIDATE] (potential numeral 6 or distal pronoun). "
            f"M527=katai [CANDIDATE] (terminal marker or trade location)."
        ),
    }
    out = OUTPUTS / "phase209_anchor_injection_m712_m817.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase209_anchor_injection_m712_m817.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 209 complete in {elapsed}s | {result['verdict']}")


if __name__ == "__main__":
    main()
