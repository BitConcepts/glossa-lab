"""Preamble sign value assignment — authored by Glossa AI via glossa_chat.py.

For each preamble sign (321, 850, 61, 235, 240), computes L1 distance to
known M77 profile entries and proposes Dravidian phonetic values via rebus.

Tooling addition by Oz: M77 descriptions dict + print formatting for the
propose_dravidian_value stub (analysis logic is Glossa AI's).
"""
from __future__ import annotations

import json
from pathlib import Path

# ── M77 reference profiles (Mahadevan 1977, from run_sign_expansion.py) ───────
# Each entry: (t_rate, i_rate, m_rate, description, dravidian_rebus)
M77_FULL: dict[str, tuple[float, float, float, str, str]] = {
    "M028": (0.044, 0.923, 0.033, "Arrow (strong initial)",          "a-  (arrow=vil? or initial vowel)"),
    "M200": (0.038, 0.811, 0.151, "Bull head (initial)",             "a-  (bull=erumai, but phonetic a-)"),
    "M029": (0.030, 0.101, 0.869, "Comb/rake (medial)",              "ma?/pa? (rake=poral/muzha)"),
    "M005": (0.000, 0.019, 0.981, "Six strokes (pure medial)",       "ā? (six=āru in Tamil)"),
    "M059": (0.047, 0.094, 0.812, "Fish (medial)",                   "meen (fish=meen in Tamil)"),
    "M012": (0.863, 0.013, 0.125, "Small circle (TMK)",              "-um (enclitic)"),
    "M282": (0.730, 0.016, 0.254, "Bracket terminal",                "suffix slot"),
    "M342": (0.138, 0.241, 0.517, "Short stroke medial",             "ka/na?"),
    "M086": (0.060, 0.360, 0.540, "Standing figure",                 "aal (person)"),
    "M088": (0.056, 0.333, 0.611, "Figure+staff",                    "admin official"),
    "M500": (0.125, 0.250, 0.625, "Plant/tree",                      "maa (great) or maram (tree)"),
    "M002": (0.333, 0.333, 0.333, "Two strokes",                     "iru? (two)"),
    "M013": (0.730, 0.008, 0.262, "Large circle (TMK)",              "suffix/terminal"),
    "M083": (0.059, 0.588, 0.353, "Kneeling figure (initial)",       "initial person/name marker"),
}

# ── Confirmed preamble sign profiles ─────────────────────────────────────────
sign_profiles: dict[str, tuple[float, float, float]] = {
    "321": (0.000, 0.000, 1.000),   # pure medial connector
    "850": (0.018, 0.818, 0.073),   # pure initial
    "61":  (0.064, 0.287, 0.606),   # mixed bridge
    "235": (0.156, 0.112, 0.708),   # medial preamble
    "240": (0.240, 0.045, 0.689),   # medial preamble
}

sign_formula_role: dict[str, str] = {
    "321": "CONNECTOR — always in [235][321][407], never initial or terminal",
    "850": "INITIAL opener of seal type B: [850][61][407][806][845][900]",
    "61":  "BRIDGE from initial 850 to title sign 407",
    "235": "PRIMARY preamble element; precedes both 240 and 321",
    "240": "SECONDARY preamble element; follows 235 in many inscriptions",
}


def l1(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def find_best_matches(sign: str) -> list[tuple[str, float, str, str]]:
    """Return top-5 M77 matches as (code, dist, desc, rebus)."""
    sp = sign_profiles[sign]
    ranked = sorted(
        [(code, l1(sp, (t, i, m)), desc, rebus)
         for code, (t, i, m, desc, rebus) in M77_FULL.items()],
        key=lambda x: x[1],
    )
    return ranked[:5]


# ── Run analysis ───────────────────────────────────────────────────────────────

print("=" * 78)
print("PREAMBLE SIGN M77 MATCHING + PHONETIC VALUE PROPOSALS")
print("=" * 78)

results = {}
for sign, profile in sign_profiles.items():
    matches = find_best_matches(sign)
    best = matches[0]
    role = sign_formula_role[sign]

    print(f"\nSign {sign}  (T={profile[0]:.3f}  I={profile[1]:.3f}  M={profile[2]:.3f})")
    print(f"  Formula role: {role}")
    print("  Top M77 matches:")
    for code, dist, desc, rebus in matches:
        marker = " ← BEST" if dist == best[1] else ""
        print(f"    {code}  dist={dist:.3f}  {desc:<30}  {rebus}{marker}")
    print(f"  Proposed phonetic value: {best[3]}  (from {best[0]} {best[2]}, dist={best[1]:.3f})")

    results[sign] = {
        "profile": {"t": profile[0], "i": profile[1], "m": profile[2]},
        "formula_role": role,
        "top5_m77": [
            {"code": c, "dist": round(d, 3), "desc": dc, "rebus": rb}
            for c, d, dc, rb in matches
        ],
        "best_m77": best[0],
        "best_dist": round(best[1], 3),
        "proposed_value": best[3],
    }

out = Path(__file__).parent.parent / "reports" / "preamble_value_assignment.json"
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), "utf-8")
print(f"\nSaved → {out}")
