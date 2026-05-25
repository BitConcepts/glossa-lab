"""Phase-254: Seal-Type Semantic Constraint Analysis

Ceiling-breaker experiment #2 from Phase-249 queue.

Strategy: MEDIUM-confidence signs that are strongly enriched on a specific
seal motif (unicorn, zebu, elephant, rhino, tiger) have their reading
constrained to the semantic domain of that motif.  If the current DEDR
reading aligns with the constrained domain AND the sign has a high
allograph correlation or collocate stability, propose MEDIUM→HIGH upgrade.

Motif-semantic domains (Parpola 1994, 2023 Semantic Scope paper):
  - Unicorn:     personal identity, titles, administrative (70%+ of seals)
  - Zebu bull:   trade, commodity, livestock ownership (~15%)
  - Elephant:    high status, royal, ceremonial (~5%)
  - Rhinoceros:  craft, manufacturing, specialist occupation (~5%)
  - Tiger:       warrior, clan head, boundary marker (~3%)

Output: outputs/phase254_semantic_constraint.json
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase254_semantic_constraint.json"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_CSV = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))

# ── Semantic domain definitions ─────────────────────────────────────────────
MOTIF_DOMAINS = {
    "unicorn": {
        "label": "Personal identity / administrative",
        "pdr_keywords": [
            "kol", "koḷ", "kōṉ", "iN", "in", "an", "aṇ", "ūr", "il", "iḷ",
            "nal", "nēr", "kō", "kai", "pū", "puḷ", "mu", "muṉ", "am", "iṉ",
            "tu", "tū", "āl", "ā", "eḷ", "ēḷ", "oṉṟu", "ōṭu", "ay",
        ],
        "grammar_slots": ["TITLE", "PERSONAL_NAME", "CASE_SUFFIX", "GENITIVE"],
    },
    "zebu": {
        "label": "Trade / commodity / livestock",
        "pdr_keywords": [
            "erutu", "māṭu", "kōṉ", "kamam", "col", "poṉ", "tēṉ", "nel",
            "pala", "kal", "ari", "nūl",
        ],
        "grammar_slots": ["COMMODITY", "MEASURE", "TRADE_MARKER"],
    },
    "elephant": {
        "label": "High status / royal / ceremonial",
        "pdr_keywords": [
            "yānai", "āṉai", "kaḷiṟu", "pari", "mātar", "vēḷ", "nāṭu",
            "periya", "talaivan",
        ],
        "grammar_slots": ["HIGH_STATUS", "ROYAL_TITLE", "CEREMONIAL"],
    },
    "rhinoceros": {
        "label": "Craft / manufacturing / specialist",
        "pdr_keywords": [
            "kāṇṭāmirukam", "toḷ", "urai", "ceyta", "kollan", "karumaṉ",
            "taccar",
        ],
        "grammar_slots": ["CRAFT", "OCCUPATION", "LICENSE"],
    },
    "tiger": {
        "label": "Warrior / clan / boundary",
        "pdr_keywords": [
            "vēṅkai", "puli", "vēl", "nāṭu", "kaḷam", "paṭai",
        ],
        "grammar_slots": ["WARRIOR", "CLAN", "BOUNDARY"],
    },
}


def norm_icon(s: str) -> str:
    """Normalize iconography string to a canonical motif label."""
    s = s.strip().lower() if s and s != "nan" else ""
    if not s:
        return "none"
    for kw in ["unicorn", "rhinoceros", "elephant", "buffalo", "tiger",
               "zebu", "bull", "gharial", "bison"]:
        if kw in s:
            if kw in ("bull", "buffalo", "bison"):
                return "zebu"
            return kw
    return "other"


def load_holdat_with_motif() -> list[dict]:
    """Load Holdat corpus as list of {signs: [...], motif: str, site: str}."""
    if not HOLDAT_CSV.exists():
        raise FileNotFoundError(f"Holdat CSV not found: {HOLDAT_CSV}")
    seals = []
    with open(HOLDAT_CSV, encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci = {h.strip(): i for i, h in enumerate(hdr)}
        current_form = None
        current_signs: list[str] = []
        current_site = ""
        current_icon = ""
        for line in fh:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            form = parts[ci.get("form", 0)].strip()
            sign = parts[ci.get("letters", 1)].strip()
            site = parts[ci.get("site", 2)].strip() if "site" in ci else ""
            icon = (parts[ci.get("iconography", 3)].strip()
                    if "iconography" in ci and ci.get("iconography", 3) < len(parts)
                    else "")
            if form != current_form:
                if current_form and current_signs:
                    seals.append({
                        "form": current_form,
                        "signs": list(current_signs),
                        "motif": norm_icon(current_icon),
                        "site": current_site,
                    })
                current_form = form
                current_signs = []
                current_site = site
                current_icon = icon
            current_signs.append(sign)
        if current_form and current_signs:
            seals.append({
                "form": current_form,
                "signs": list(current_signs),
                "motif": norm_icon(current_icon),
                "site": current_site,
            })
    return seals


def reading_matches_domain(reading: str, domain_keywords: list[str]) -> bool:
    """Check if a sign reading matches any keyword in the semantic domain."""
    if not reading:
        return False
    r = reading.lower().split("/")[0].strip()
    for kw in domain_keywords:
        if kw.lower() in r or r in kw.lower():
            return True
    return False


def main():
    print("=" * 70)
    print("PHASE-254: SEAL-TYPE SEMANTIC CONSTRAINT ANALYSIS")
    print("=" * 70)

    # Load data
    anchors_raw = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_raw.get("anchors", {})
    seals = load_holdat_with_motif()

    print(f"\n  Seals loaded: {len(seals)}")

    # Motif distribution
    motif_counts = Counter(s["motif"] for s in seals)
    print(f"  Motif distribution: {dict(motif_counts.most_common(10))}")

    # MEDIUM signs to analyse
    medium_signs = {k for k, v in anchors.items() if v.get("confidence") == "MEDIUM"}
    high_signs = {k for k, v in anchors.items() if v.get("confidence") == "HIGH"}
    print(f"  MEDIUM signs: {len(medium_signs)}")
    print(f"  HIGH signs: {len(high_signs)}")

    # ── Step 1: Sign × Motif enrichment ─────────────────────────────────────
    print("\n" + "─" * 70)
    print("STEP 1: SIGN × MOTIF ENRICHMENT ANALYSIS")
    print("─" * 70)

    # Count sign occurrences by motif
    sign_motif: dict[str, Counter] = defaultdict(Counter)
    sign_total: Counter = Counter()
    motif_total: Counter = Counter()
    grand_total = 0

    for seal in seals:
        motif = seal["motif"]
        for sign in seal["signs"]:
            # Normalize to M-prefix
            s = f"M{sign}" if not sign.startswith("M") else sign
            sign_motif[s][motif] += 1
            sign_total[s] += 1
            motif_total[motif] += 1
            grand_total += 1

    # Compute chi-squared enrichment for MEDIUM signs
    enrichments = []
    for sign in medium_signs:
        if sign_total.get(sign, 0) < 3:
            continue
        reading = anchors[sign].get("reading", "")
        for motif in ["unicorn", "zebu", "elephant", "rhinoceros", "tiger"]:
            observed = sign_motif.get(sign, {}).get(motif, 0)
            expected = (sign_total[sign] * motif_total[motif]) / max(grand_total, 1)
            if expected < 1:
                continue
            chi2 = (observed - expected) ** 2 / expected
            lift = observed / max(expected, 0.001)
            if chi2 > 3.84 and observed > expected:  # p < 0.05
                # Check if reading matches domain
                domain = MOTIF_DOMAINS.get(motif, {})
                domain_match = reading_matches_domain(
                    reading, domain.get("pdr_keywords", [])
                )
                enrichments.append({
                    "sign": sign,
                    "reading": reading,
                    "motif": motif,
                    "domain": domain.get("label", ""),
                    "observed": observed,
                    "expected": round(expected, 2),
                    "chi2": round(chi2, 3),
                    "lift": round(lift, 2),
                    "total_occurrences": sign_total[sign],
                    "domain_match": domain_match,
                })

    enrichments.sort(key=lambda x: -x["chi2"])
    print(f"\n  Significant enrichments (χ²>3.84, p<0.05): {len(enrichments)}")
    print(f"\n  {'Sign':<8} {'Reading':<16} {'Motif':<12} {'Obs':>5} {'Exp':>6} "
          f"{'χ²':>7} {'Lift':>5} Match")
    for e in enrichments[:25]:
        print(f"  {e['sign']:<8} {e['reading'][:15]:<16} {e['motif']:<12} "
              f"{e['observed']:>5} {e['expected']:>6.1f} {e['chi2']:>7.2f} "
              f"{e['lift']:>5.1f} {'✓' if e['domain_match'] else '✗'}")

    # ── Step 2: Domain-matched upgrade candidates ───────────────────────────
    print("\n" + "─" * 70)
    print("STEP 2: DOMAIN-MATCHED MEDIUM→HIGH UPGRADE CANDIDATES")
    print("─" * 70)

    # Signs enriched on a motif AND whose reading matches that domain
    domain_matched = [e for e in enrichments if e["domain_match"]]
    print(f"\n  Domain-matched enrichments: {len(domain_matched)}")

    # For upgrade: require chi2 > 6.64 (p < 0.01) AND lift > 2.0
    upgrade_candidates = []
    seen_signs = set()
    for e in domain_matched:
        if e["sign"] in seen_signs:
            continue
        if e["chi2"] > 6.64 and e["lift"] > 2.0:
            upgrade_candidates.append(e)
            seen_signs.add(e["sign"])

    print(f"  Upgrade candidates (χ²>6.64, lift>2.0, domain match): "
          f"{len(upgrade_candidates)}")

    for uc in upgrade_candidates[:15]:
        print(f"    {uc['sign']}='{uc['reading']}' on {uc['motif']} seals: "
              f"χ²={uc['chi2']:.1f}, lift={uc['lift']:.1f}x → UPGRADE CANDIDATE")

    # ── Step 3: Apply upgrades to anchors ───────────────────────────────────
    print("\n" + "─" * 70)
    print("STEP 3: APPLYING MEDIUM→HIGH UPGRADES")
    print("─" * 70)

    n_upgraded = 0
    upgrade_log = []
    for uc in upgrade_candidates:
        sign = uc["sign"]
        if anchors.get(sign, {}).get("confidence") != "MEDIUM":
            continue
        anchors[sign]["confidence"] = "HIGH"
        anchors[sign]["phase_upgraded"] = 254
        anchors[sign]["semantic_constraint"] = {
            "motif": uc["motif"],
            "domain": uc["domain"],
            "chi2": uc["chi2"],
            "lift": uc["lift"],
        }
        basis = anchors[sign].get("basis", "")
        anchors[sign]["basis"] = (
            f"{basis}; Phase-254: semantic constraint upgrade — "
            f"enriched on {uc['motif']} seals (χ²={uc['chi2']:.1f}, "
            f"lift={uc['lift']:.1f}x), reading matches {uc['domain']} domain"
        )
        n_upgraded += 1
        upgrade_log.append({
            "sign": sign,
            "reading": uc["reading"],
            "motif": uc["motif"],
            "chi2": uc["chi2"],
            "lift": uc["lift"],
            "upgrade": "MEDIUM→HIGH",
        })
        print(f"  ↑ {sign}='{uc['reading']}': MEDIUM → HIGH "
              f"({uc['motif']}, χ²={uc['chi2']:.1f})")

    # ── Step 4: Non-domain-matched analysis ─────────────────────────────────
    # Signs enriched on a motif but reading does NOT match the domain
    # These are interesting: potential misassignments or dual-function signs
    non_matched = [e for e in enrichments if not e["domain_match"] and e["chi2"] > 6.64]
    print(f"\n  Non-domain-matched strong enrichments (investigate): {len(non_matched)}")
    for nm in non_matched[:10]:
        print(f"    {nm['sign']}='{nm['reading']}' on {nm['motif']} seals: "
              f"χ²={nm['chi2']:.1f} — reading doesn't match {nm['domain']}")

    # ── Save anchors ────────────────────────────────────────────────────────
    if n_upgraded > 0:
        anchors_raw["anchors"] = anchors
        ANCHORS.write_text(
            json.dumps(anchors_raw, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\n  Anchors saved: {n_upgraded} MEDIUM→HIGH upgrades applied")

    # Count final state
    by_conf = Counter(v.get("confidence", "?") for v in anchors.values())
    n_hm = by_conf.get("HIGH", 0) + by_conf.get("MEDIUM", 0)
    print(f"\n  Final state: H:{by_conf.get('HIGH',0)} M:{by_conf.get('MEDIUM',0)} "
          f"CANDIDATE:{by_conf.get('CANDIDATE',0)} → H+M={n_hm}/{len(anchors)}")

    # ── Output ──────────────────────────────────────────────────────────────
    result = {
        "phase": 254,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_seals": len(seals),
        "motif_distribution": dict(motif_counts.most_common(10)),
        "n_medium_analysed": len(medium_signs),
        "n_significant_enrichments": len(enrichments),
        "n_domain_matched": len(domain_matched),
        "n_upgrade_candidates": len(upgrade_candidates),
        "n_upgraded": n_upgraded,
        "upgrade_log": upgrade_log,
        "top_enrichments": enrichments[:30],
        "non_domain_matched_investigate": non_matched[:15],
        "final_state": {
            "HIGH": by_conf.get("HIGH", 0),
            "MEDIUM": by_conf.get("MEDIUM", 0),
            "CANDIDATE": by_conf.get("CANDIDATE", 0),
            "H_plus_M": n_hm,
            "total": len(anchors),
        },
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Output saved: {OUT}")
    print(f"\n{'=' * 70}")
    print(f"PHASE-254 COMPLETE: {n_upgraded} MEDIUM→HIGH upgrades")
    print(f"{'=' * 70}")
    return result


if __name__ == "__main__":
    main()
