"""
Fact-check fix: correct two erroneous HIGH-confidence assignments in INDUS_FINAL_ANCHORS.json.

FINDING A (M267): M267 has freq=400 and appears across ALL motif types (unicorn 127,
zebu bull 72, elephant 37, etc.) — it is NOT an iconographic fish sign.
The Mahadevan-Parpola crosswalk identifies M047 (freq=13) as P47 = "fish (plain)".
M267 was incorrectly assigned 'min/mīn' with HIGH confidence in V6.
Correcting to UNCERTAIN with an explanatory basis.

FINDING B (M063): M063 was assigned 'mutalai' (crocodile) with HIGH confidence based
on a claimed 'lift > 5.0 on gharial seals'. True gharial lift = 4.35 (< 5.0 threshold).
M063 appears across many motifs (unicorn 4, zebu bull 3, gharial 3, tiger 2, ...).
Correcting to MEDIUM confidence.

TB CORRELATION IMPACT:
- Removing M267 changes correlation 0.9138 → 0.9065 (modest effect: M267 is freq=400/7002=5.7%)
- These corrections do not invalidate the overall finding; correlation ~0.91 is still well above
  the random baseline of 0.47.
"""
import json
from pathlib import Path

FINAL = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports\INDUS_FINAL_ANCHORS.json")

data = json.loads(FINAL.read_text(encoding="utf-8"))
anchors = data["anchors"]

# ── Fix M267 ──────────────────────────────────────────────────────────────────
old_m267 = dict(anchors.get("M267", {}))
anchors["M267"] = {
    "reading":    "?/uncertain",
    "confidence": "UNCERTAIN",
    "basis": (
        "FACT-CHECK CORRECTION 2026-05-11: Original V6 assignment 'min/mīn' (HIGH) was wrong. "
        "M267 has freq=400 in the Holdat corpus and appears across ALL motif types "
        "(unicorn 127, zebu bull 72, elephant 37, rhinoceros 25, etc.) — it is NOT an "
        "iconographic fish sign. The actual Mahadevan fish sign is M047 (freq=13, P47 in "
        "Parpola's system, as documented in mahadevan_parpola_crosswalk.json). "
        "M267 is most likely a high-frequency functional/suffixal sign. Downgraded from HIGH. "
        f"Previous: {old_m267}"
    ),
}
print(f"M267: {old_m267['confidence']} → UNCERTAIN  (was: {old_m267['reading']})")

# ── Fix M063 ──────────────────────────────────────────────────────────────────
old_m063 = dict(anchors.get("M063", {}))
anchors["M063"] = {
    "reading":    "mutalai",
    "confidence": "MEDIUM",
    "basis": (
        "FACT-CHECK CORRECTION 2026-05-11: Original V7 assignment was HIGH based on claimed "
        "'lift > 5.0 on gharial seals'. Actual measured gharial lift = 4.35 (below threshold). "
        "M063 appears on 3/18 seals with gharial motif (vs. 4 unicorn, 3 zebu bull). "
        "Reading 'mutalai' (Tamil: crocodile/gharial, DEDR 4954) is plausible given gharial "
        "association, but not exclusive enough for HIGH confidence. Downgraded HIGH → MEDIUM. "
        f"Previous: {old_m063}"
    ),
}
print(f"M063: {old_m063['confidence']} → MEDIUM  (reading preserved: mutalai)")

# ── Note M047 as the actual fish sign candidate ──────────────────────────────
if "M047" not in anchors:
    anchors["M047"] = {
        "reading":    "mīn",
        "confidence": "MEDIUM",
        "basis": (
            "FACT-CHECK ADDITION 2026-05-11: M047 is documented as P47 = 'fish (plain)' "
            "in mahadevan_parpola_crosswalk.json (Parpola 1994a + Mahadevan 1977 crosswalk). "
            "Freq=13 in Holdat corpus (rare, consistent with a specific iconic sign). "
            "Reading 'mīn' (Tamil: fish/star, DEDR 4897) is the Parpola canonical anchor "
            "from Parpola 2010 iconographic anchor set (see iconographic_anchors.json sign '47'). "
            "MEDIUM confidence: crosswalk-backed but small corpus sample."
        ),
    }
    print("M047: NEW entry added — mīn (MEDIUM) — the actual Mahadevan fish sign")
else:
    print(f"M047: already exists — {anchors['M047']}")

# ── Save ──────────────────────────────────────────────────────────────────────
data["total"] = len(anchors)
FINAL.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved: {FINAL.name}  ({data['total']} entries)")

# ── Report new HIGH/MEDIUM/LOW counts ────────────────────────────────────────
from collections import Counter
conf_counts = Counter(v.get("confidence","?") for v in anchors.values())
print(f"\nUpdated confidence breakdown:")
for conf, count in sorted(conf_counts.items()):
    print(f"  {conf}: {count}")
