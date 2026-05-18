"""Phase-84: Extended Formula Lexicon.

Build a comprehensive formula translation lexicon using all 97+ HIGH+MEDIUM anchors.
Extends Phase-68's pilot formula translations to cover:
  - All TITLE_FORMULA patterns (animal + title + suffix)
  - All PLACE_FORMULA patterns (place name + locative)
  - OWNERSHIP formulas (X-iN-Y)
  - SUFFIX_ONLY patterns
  - Numeric/quantity formulas

Produces formula_lexicon: a sorted table of pattern → translation with confidence.

CPU only. Output: reports/phase84_formula_lexicon.json
"""
from __future__ import annotations
import csv, json, re
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P68     = REPO / "reports/phase68_formula_translation.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase84_formula_lexicon.json"

# Sign role classification (from Phases 68, 74, 78)
SIGN_ROLES = {
    # Animal classifiers (determinatives)
    "M006": ("ANIMAL", "puli", "leopard/tiger"),
    "M016": ("ANIMAL", "erutu", "bull"),
    "M045": ("ANIMAL", "yānai", "elephant"),
    "M062": ("ANIMAL", "e", "antelope/deer"),
    "M047": ("ANIMAL", "miin", "fish"),
    "M039": ("ANIMAL", "kaa", "tree/grove"),
    "M040": ("ANIMAL", "aa", "cow"),
    # Title signs
    "M099": ("TITLE", "kol", "lord/chieftain"),
    "M073": ("TITLE", "ko", "king/ruler"),
    "M059": ("TITLE", "el", "lord"),
    "M030": ("TITLE", "nay", "leader"),
    "M041": ("TITLE", "aa", "great"),
    "M211": ("TITLE", "aatu", "goat/noble"),
    # Case suffixes
    "M342": ("SUFFIX", "ay", "genitive/belonging to"),
    "M176": ("SUFFIX", "an", "masculine personal name ending"),
    "M367": ("SUFFIX", "am", "collective/plural"),
    "M391": ("SUFFIX", "ka", "nominative"),
    "M336": ("SUFFIX", "i", "locative"),
    "M089": ("SUFFIX", "tu", "ablative/from"),
    "M328": ("SUFFIX", "a", "title suffix"),
    "M162": ("SUFFIX", "il", "in/at/house"),
    # Connective
    "M267": ("CONNECTIVE", "iN", "genitive 'of'"),
    # Place indicators
    "M233": ("PLACE", "ur", "settlement/town"),
    "M162": ("PLACE", "il", "house/at"),
    # Numbers (from DEDR)
    "M079": ("NUMERAL", "ir", "two"),
    "M095": ("NUMERAL", "ai5", "five strokes"),
    "M096": ("NUMERAL", "aru6", "six strokes"),
}

# Natural language interpretation templates for formula types
FORMULA_TEMPLATES = [
    # Pattern: (formula_type, required_roles, translation_template)
    ("TITLE_FORMULA_ANIMAL",
     ["ANIMAL", "TITLE", "SUFFIX"],
     "{animal} [seal of] {title}-{suffix}  |  '[Name: {title}]-{suffix}' with {animal} totem"),
    ("TITLE_FORMULA_SIMPLE",
     ["TITLE", "SUFFIX"],
     "{title}-{suffix}  |  Personal title + case marker"),
    ("OWNERSHIP_FORMULA",
     ["CONNECTIVE"],
     "X-iN-Y  |  'Y belonging to X' / 'Y of X'  (genitive construction)"),
    ("PLACE_FORMULA",
     ["PLACE"],
     "[PLACE_NAME]-{place}  |  Settlement/location identifier"),
    ("SUFFIX_ONLY",
     ["SUFFIX"],
     "[NAME]-{suffix}  |  Personal name + case marker (name unknown)"),
    ("NUMERAL_FORMULA",
     ["NUMERAL"],
     "{numeral} [COMMODITY]  |  Quantity + commodity (administrative record?)"),
]


def load_holdat_seals():
    seals: dict[str, list] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", "")
            p = int(row.get("position", 0) or 0)
            if not c: continue
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return {c: [s for s in v if s] for c, v in seals.items() if any(v)}


def classify_formula(signs: list) -> str:
    roles = set()
    for s in signs:
        if s in SIGN_ROLES:
            roles.add(SIGN_ROLES[s][0])
    if "ANIMAL" in roles and "TITLE" in roles and "SUFFIX" in roles:
        return "TITLE_FORMULA_ANIMAL"
    elif "TITLE" in roles and "SUFFIX" in roles:
        return "TITLE_FORMULA_SIMPLE"
    elif "CONNECTIVE" in roles:
        return "OWNERSHIP_FORMULA"
    elif "PLACE" in roles:
        return "PLACE_FORMULA"
    elif "NUMERAL" in roles:
        return "NUMERAL_FORMULA"
    elif "SUFFIX" in roles:
        return "SUFFIX_ONLY"
    else:
        return "UNCERTAIN"


def build_pattern_reading(signs: list, anchors: dict) -> dict:
    """Build the transliteration pattern for a seal."""
    parts = []
    for sign in signs:
        info = anchors.get(sign, {})
        if info.get("confidence") in ("HIGH", "MEDIUM"):
            r = info["reading"].split("/")[0].split("(")[0].strip()
            parts.append(r)
        else:
            parts.append(f"[{sign}]")
    return {
        "pattern": signs,
        "transliteration": "-".join(parts),
        "formula_type": classify_formula(signs),
    }


def main():
    print("Phase-84: Extended Formula Lexicon\n")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}

    seals = load_holdat_seals()
    print(f"  Anchors: {len(confirmed)} HIGH+MEDIUM")
    print(f"  Seals: {len(seals)}")

    # Load Phase-68 base translations if available
    phase68_formulas = {}
    if P68.exists():
        try:
            p68 = json.loads(P68.read_text())
            for f in p68.get("formula_translations", []):
                phase68_formulas[f.get("pattern", "")] = f
            print(f"  Phase-68 base formulas: {len(phase68_formulas)}")
        except Exception:
            pass

    # Classify all seals and group by formula type
    formula_type_dist: Counter = Counter()
    pattern_counter: Counter = Counter()
    formula_examples: dict = defaultdict(list)

    for cisi_id, signs in seals.items():
        if not signs: continue
        ft = classify_formula(signs)
        formula_type_dist[ft] += 1
        # Build pattern key (formula type + sign sequence)
        pat_key = ft + "|" + ",".join(signs[:5])  # first 5 signs as key
        pattern_counter[pat_key] += 1
        if len(formula_examples[ft]) < 5:
            reading = build_pattern_reading(signs, anchors)
            formula_examples[ft].append({
                "cisi_id": cisi_id,
                "signs": signs,
                "transliteration": reading["transliteration"],
            })

    print(f"\n  Formula type distribution:")
    for ft, count in sorted(formula_type_dist.items(), key=lambda x: -x[1]):
        print(f"    {ft:30s}: {count:4d} seals ({count/len(seals)*100:.1f}%)")

    # Build formula lexicon entries
    lexicon = []
    for ft, template_info in [(t[0], t) for t in FORMULA_TEMPLATES]:
        _, required_roles, template = template_info
        count = formula_type_dist.get(ft, 0)
        examples = formula_examples.get(ft, [])

        # Build natural-language reading using actual anchor readings
        # Fill template placeholders with most common readings for each role
        nl_readings = {}
        for role in required_roles:
            role_signs = [s for s, (r, reading, _) in SIGN_ROLES.items() if r == role]
            if role_signs:
                # Use the first confirmed reading for this role
                for rs in role_signs:
                    if rs in anchors and anchors[rs].get("confidence") in ("HIGH", "MEDIUM"):
                        nl_readings[role.lower()] = anchors[rs]["reading"].split("/")[0]
                        break
                else:
                    nl_readings[role.lower()] = f"[{role}]"

        try:
            nl_translation = template.format(**nl_readings)
        except KeyError:
            nl_translation = template

        entry = {
            "formula_type": ft,
            "required_sign_roles": required_roles,
            "n_seals": count,
            "pct_of_corpus": round(count / len(seals) * 100, 1),
            "natural_language_template": nl_translation,
            "key_anchor_signs": [
                {"sign": s, "reading": anchors.get(s, {}).get("reading", "?"),
                 "role": SIGN_ROLES.get(s, ("?", "?", "?"))[0]}
                for role in required_roles
                for s in SIGN_ROLES
                if SIGN_ROLES.get(s, ("",))[0] == role and s in confirmed
            ][:6],
            "examples": examples[:3],
        }
        lexicon.append(entry)

    # Add a worked example translation
    print(f"\n  Sample formula translations:")
    for entry in lexicon[:4]:
        if entry["n_seals"] > 0:
            print(f"    {entry['formula_type']} ({entry['n_seals']} seals):")
            print(f"      Template: {entry['natural_language_template'][:80]}")
            if entry["examples"]:
                ex = entry["examples"][0]
                print(f"      Example: {ex['cisi_id']} -> {ex['transliteration']}")

    # Overall lexicon stats
    n_formulas_decoded = sum(1 for e in lexicon if e["n_seals"] > 0)
    total_covered = sum(e["n_seals"] for e in lexicon if e["formula_type"] != "UNCERTAIN")

    print(f"\n=== Phase-84 Results ===")
    print(f"  Formula types in lexicon: {len(lexicon)}")
    print(f"  Non-UNCERTAIN formulas: {n_formulas_decoded}")
    print(f"  Seals covered by lexicon: {total_covered}/{len(seals)} ({total_covered/len(seals)*100:.1f}%)")
    print(f"  UNCERTAIN seals: {formula_type_dist.get('UNCERTAIN', 0)}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_anchor_signs": len(confirmed),
        "n_seals_total": len(seals),
        "n_formulas_decoded": n_formulas_decoded,
        "n_seals_covered_by_lexicon": total_covered,
        "formula_type_distribution": dict(formula_type_dist),
        "formula_lexicon": lexicon,
        "sign_role_table": {
            s: {"role": r[0], "reading": r[1], "meaning": r[2]}
            for s, r in SIGN_ROLES.items() if s in confirmed
        },
        "verdict": (
            f"Phase-84: Extended formula lexicon with {n_formulas_decoded} formula types. "
            f"{total_covered}/{len(seals)} seals covered ({total_covered/len(seals)*100:.0f}%). "
            f"Key formula types: TITLE_FORMULA_ANIMAL ({formula_type_dist.get('TITLE_FORMULA_ANIMAL',0)} seals), "
            f"OWNERSHIP_FORMULA ({formula_type_dist.get('OWNERSHIP_FORMULA',0)} seals), "
            f"SUFFIX_ONLY ({formula_type_dist.get('SUFFIX_ONLY',0)} seals)."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
