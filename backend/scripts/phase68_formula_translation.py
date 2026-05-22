"""Phase-68: Full Formula Translation Pilot with Linguistic Annotation.

For the 22 formulas decoded at >=80% in Phase-59, produces complete
Dravidian linguistic annotations:
  - Morphological role for each slot (ROOT/SUFFIX/CLASSIFIER/GENITIVE/PARTICLE)
  - DEDR entry citation where available
  - Semantic interpretation (title formula / ownership formula / trade formula)
  - Full gloss in English

No GPU required — pure linguistic analysis.
Output: reports/phase68_formula_translation.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
P59     = REPO / "reports/phase59_pilot_readings.json"
P64     = REPO / "reports/phase64_morphological_boundary.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase68_formula_translation.json"

# ── Morphological role database ───────────────────────────────────────────────
# For each M-number in the anchor set, assign a grammatical role and DEDR ref.
MORPH_ROLES: dict[str, dict] = {
    # CLASSIFIERS (INITIAL position, faunal/iconic, rebus principle)
    "M006": {"role": "CLASSIFIER", "dedr": "DEDR 4346", "gloss": "puli (tiger) -> title-class marker"},
    "M016": {"role": "CLASSIFIER", "dedr": "DEDR 1278", "gloss": "kaLiRu (elephant-calf) -> title-class marker"},
    "M045": {"role": "CLASSIFIER", "dedr": "DEDR 5149", "gloss": "yaanai (elephant) -> title-class marker"},
    "M062": {"role": "CLASSIFIER", "dedr": "DEDR 824",  "gloss": "erutu (zebu-bull) -> title-class marker"},
    "M047": {"role": "CLASSIFIER", "dedr": "DEDR 4839", "gloss": "miin (fish) -> title-class marker"},
    "M039": {"role": "CLASSIFIER", "dedr": "DEDR 327",  "gloss": "aaNai (elephant) -> title-class marker"},
    "M060": {"role": "ROOT",       "dedr": "DEDR 824",  "gloss": "eRu (bull/male)"},
    # ROOT signs (content words — titles, names, commodities)
    "M099": {"role": "TITLE",      "dedr": "DEDR 2159", "gloss": "kol/koL (lord/chieftain)"},
    "M059": {"role": "ROOT",       "dedr": "DEDR 907",  "gloss": "eeL/eL (person/owner/rule)"},
    "M211": {"role": "ROOT",       "dedr": "DEDR 2159", "gloss": "kol (unicorn-lord, title)"},
    "M073": {"role": "ROOT",       "dedr": "DEDR 2159", "gloss": "koon (king/chief)"},
    "M030": {"role": "ROOT",       "dedr": "DEDR 2159", "gloss": "koo (king/lord)"},
    "M233": {"role": "ROOT",       "dedr": "DEDR 5506", "gloss": "uur (settlement/town)"},
    "M013": {"role": "ROOT",       "dedr": "DEDR 3590", "gloss": "nakaram (town-place, na-)"},
    "M004": {"role": "ROOT",       "dedr": "DEDR 1967", "gloss": "keeL (hear/question)"},
    "M077": {"role": "ROOT",       "dedr": "DEDR 3599", "gloss": "nal (good)"},
    "M041": {"role": "ROOT",       "dedr": "DEDR 4375", "gloss": "peer (name/big)"},
    "M080": {"role": "ROOT",       "dedr": "DEDR 5500", "gloss": "veeNkai (kino-tree)"},
    "M249": {"role": "ROOT",       "dedr": "DEDR 3494", "gloss": "tii/tee (scorpion)"},
    "M261": {"role": "ROOT",       "dedr": "DEDR 4867", "gloss": "muruku (Murukan/young-man)"},
    # SUFFIXES (TERMINAL position, grammatical morphemes)
    "M342": {"role": "SUFFIX",     "dedr": "DEDR 5295", "gloss": "ay/aay (honorific suffix)"},
    "M176": {"role": "SUFFIX",     "dedr": "DEDR 134",  "gloss": "an/aN (masculine suffix)"},
    "M367": {"role": "SUFFIX",     "dedr": "DEDR 192",  "gloss": "am (neuter suffix)"},
    "M391": {"role": "CASE",       "dedr": "DEDR 1384", "gloss": "ka/kaN (case marker)"},
    "M336": {"role": "CASE",       "dedr": "DEDR 459",  "gloss": "iN/in (locative particle)"},
    "M089": {"role": "SUFFIX",     "dedr": "DEDR 3476", "gloss": "tu/tuu (verbal/nominal suffix)"},
    "M328": {"role": "SUFFIX",     "dedr": "DEDR 327",  "gloss": "aa/aaL (agentive suffix, feminine)"},
    "M162": {"role": "CASE",       "dedr": "DEDR 464",  "gloss": "il/iL (locative 'in/at')"},
    # PARTICLES
    "M267": {"role": "PARTICLE",   "dedr": "DEDR 460",  "gloss": "iN (genitive 'of') [UNCERTAIN]"},
    # Numbers
    "M086": {"role": "NUMBER",     "dedr": "DEDR 993",  "gloss": "oru (one)"},
    "M087": {"role": "NUMBER",     "dedr": "DEDR 5509", "gloss": "veL/iru (two/white)"},
    "M012": {"role": "NUMBER",     "dedr": "DEDR 3940", "gloss": "oNRu/oTTai (one)"},
    "M048": {"role": "ROOT",       "dedr": "DEDR 4927", "gloss": "mun (front/before)"},
    "M051": {"role": "ROOT",       "dedr": "DEDR 4277", "gloss": "puu (flower)"},
    "M305": {"role": "ROOT",       "dedr": "DEDR 473",  "gloss": "iru/ooTu (seated/comitative)"},
}

# Semantic formula type classification
FORMULA_TYPES = {
    "TITLE_FORMULA":     "Sign [Classifier]-[Root-title]-[Suffix] — identifies a person by title",
    "OWNERSHIP_FORMULA": "Sign [Owner-mark]-[Particle]-[Title] — '[owner's] [title]'",
    "PLACE_FORMULA":     "Sign [Root-place]-[Locative] — '[place] + locative'",
    "TRADE_FORMULA":     "Sign [Commodity]-[Number/Measure]-[Title]",
    "UNCERTAIN":         "Formula type unclear from current readings",
}


def classify_formula(slots: list[dict]) -> str:
    """Classify a formula by the roles of its decoded slots."""
    roles = [MORPH_ROLES.get(s["sign"], {}).get("role", "UNKNOWN") for s in slots]
    conf_roles = [roles[i] for i, s in enumerate(slots)
                  if s.get("confidence") in ("HIGH", "MEDIUM")]

    if not conf_roles:
        return "UNCERTAIN"

    # Title formula: CLASSIFIER + (ROOT/TITLE) + SUFFIX
    if "CLASSIFIER" in conf_roles and ("SUFFIX" in conf_roles or "TITLE" in conf_roles):
        return "TITLE_FORMULA"
    # Ownership: ROOT + PARTICLE + TITLE
    if "PARTICLE" in conf_roles and "TITLE" in conf_roles:
        return "OWNERSHIP_FORMULA"
    # Place formula
    if "CASE" in conf_roles:
        return "PLACE_FORMULA"
    # Multiple suffixes suggest a name formula
    if conf_roles.count("SUFFIX") >= 2:
        return "TITLE_FORMULA"
    return "UNCERTAIN"


def build_english_gloss(slots: list[dict], formula_type: str) -> str:
    """Produce a readable English gloss for the formula."""
    parts = []
    for slot in slots:
        sign = slot["sign"]
        reading = slot.get("reading", "?")
        conf = slot.get("confidence", "UNREAD")
        role_info = MORPH_ROLES.get(sign, {})
        role = role_info.get("role", "UNKNOWN")
        gloss = role_info.get("gloss", "")

        if conf in ("HIGH", "MEDIUM"):
            # Use the first readable element of the gloss
            gloss_short = gloss.split("(")[0].strip().split("/")[0]
            if role == "CLASSIFIER":
                parts.append(f"[{gloss_short}]")
            elif role in ("SUFFIX", "CASE"):
                parts.append(f"-{reading}")
            elif role == "PARTICLE":
                parts.append(f"{reading}")
            elif role == "TITLE":
                parts.append(gloss_short)
            else:
                parts.append(gloss_short if gloss_short else reading)
        elif conf == "SA_CANDIDATE":
            parts.append(f"({reading}?)")
        else:
            parts.append(f"[{sign}]")

    gloss = " ".join(parts)
    if formula_type == "TITLE_FORMULA":
        gloss = f"Title inscription: {gloss}"
    elif formula_type == "OWNERSHIP_FORMULA":
        gloss = f"Ownership formula: {gloss}"
    elif formula_type == "PLACE_FORMULA":
        gloss = f"Place reference: {gloss}"
    return gloss


def main():
    print("Phase-68: Full Formula Translation Pilot\n")

    if not P59.exists():
        print(f"ERROR: {P59} not found")
        return

    p59 = json.loads(P59.read_text("utf-8"))
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]

    # Build readings dict from anchors + SA candidates
    readings = {}
    for sign, info in anchors.items():
        if info.get("reading"):
            readings[sign] = {
                "reading": info["reading"],
                "confidence": info["confidence"],
                "gloss": info.get("gloss", ""),
            }

    formulas = p59.get("fully_decoded_gte_80pct", [])
    top_50   = p59.get("top_50_formulas", [])

    print(f"  Formulas >=80% decoded: {len(formulas)}")
    print(f"  Top-50 formulas: {len(top_50)}")

    translations = []
    formula_type_counts: Counter = Counter()

    for formula in formulas:
        pattern = formula.get("pattern", [])
        slots_raw = formula.get("slots", [])

        # Enrich slots with morphological roles
        slots_enriched = []
        for slot in slots_raw:
            sign = slot.get("sign", "")
            role_info = MORPH_ROLES.get(sign, {})
            enriched = {
                **slot,
                "morph_role": role_info.get("role", "UNKNOWN"),
                "dedr_ref":   role_info.get("dedr", ""),
                "morph_gloss":role_info.get("gloss", ""),
            }
            slots_enriched.append(enriched)

        formula_type = classify_formula(slots_raw)
        english_gloss = build_english_gloss(slots_raw, formula_type)
        formula_type_counts[formula_type] += 1

        # Build slot-level table
        slot_table = []
        for s in slots_enriched:
            sign = s["sign"]
            slot_table.append({
                "sign":        sign,
                "reading":     s.get("reading", "?"),
                "confidence":  s.get("confidence", "UNREAD"),
                "morph_role":  s["morph_role"],
                "dedr":        s["dedr_ref"],
                "gloss":       s["morph_gloss"][:60] if s["morph_gloss"] else "",
            })

        translation = {
            "pattern":       pattern,
            "count":         formula.get("count", 0),
            "morphological": formula.get("morphological", ""),
            "coverage_pct":  formula.get("coverage_pct", 0),
            "formula_type":  formula_type,
            "english_gloss": english_gloss,
            "slot_table":    slot_table,
        }
        translations.append(translation)

        print(f"  [{formula.get('count', 0):3d}x] {formula_type:20s} | {english_gloss[:60]}")

    # Sort by formula type then frequency
    translations.sort(key=lambda x: (x["formula_type"], -x["count"]))

    print("\n=== Phase-68 Results ===")
    print(f"  Formulas glossed:     {len(translations)}")
    print("  Formula type breakdown:")
    for ftype, count in formula_type_counts.most_common():
        print(f"    {ftype:25s}: {count}")
    print(f"\n  DEDR-cited morphemes: {sum(1 for t in translations for s in t['slot_table'] if s['dedr'])}")

    # Cross-reference with Phase-64 M267 resolution
    m267_formulas = [t for t in translations if any(s["sign"] == "M267" for s in t["slot_table"])]
    print(f"  Formulas with M267:   {len(m267_formulas)}")
    for f in m267_formulas[:3]:
        print(f"    {f['morphological'][:60]} -> {f['english_gloss'][:60]}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_glossed":        len(translations),
        "n_formula_types":  len(formula_type_counts),
        "formula_types":    dict(formula_type_counts),
        "translations":     translations,
        "morph_role_legend": MORPH_ROLES,
        "formula_type_legend": FORMULA_TYPES,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
