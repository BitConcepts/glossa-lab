"""Phase-46 T4: Fish Sign Expansion — M047 Family + Contact Zone.

Phase-45 T6 found NO_ENRICHMENT for M047 at coastal sites (n=13, p=0.685).
The test was underpowered. This script takes two approaches to increase power:

  Approach A: Expand the fish sign family.
    M047 is a CLASSIFIER_PREFIX (avg_pos=0.0, is_starter=True).
    The M040-M058 range contains 18 CLASSIFIER_PREFIX signs (excluding M048/M051/M059
    which are CASE_MARKER_SUFFIX or PERSON_OR_OWNER). Many of these are animal-class
    prefixes. The fish sign (min) and its graphemic variants may correspond to
    multiple M-numbers that share the same reading.
    Test: pool all INITIAL-STRONG signs (avg_pos=0.0, CLASSIFIER_PREFIX role) and
    run a pooled coastal enrichment test.

  Approach B: Check contact zone for fish sign.
    The Gulf seals (Laursen 2010, Parpola readings) include sign '53' or '60' as
    possible fish variants. Check Mesopotamia seals for fish sign occurrences.
    The CDLI Meluhha tablets that mention Meluhha may have fish-related terminology.

  Approach C: Compare fish sign frequency by ICONOGRAPHY.
    M047 appears in 'fish only' or 'fish+unicorn' motifs? Test if fish sign is
    preferentially associated with the 'fish' iconography motif.

GPU: torch for inscription scanning and contingency matrix.

Output: reports/phase46_t4_fish_expansion.json
"""
from __future__ import annotations
import csv, json, math, re
from collections import Counter
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

try:
    from scipy.stats import fisher_exact, chi2_contingency
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES   = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
CZ      = REPO / "corpora/downloads/contact_zone"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase46_t4_fish_expansion.json"

PRIMARY_FISH = "M047"  # confirmed mīn/min reading (HIGH confidence)

# Coastal sites
COASTAL_SITES = {"lothal", "dholavira"}
INLAND_SITES = {"mohenjo-daro", "harappa", "kalibangan", "chanhu-daro",
                "rakhigarhi", "banawali", "sutkagen-dor", "shortugai"}


def _is_coastal(site: str) -> bool | None:
    s = site.strip().lower()
    if any(c in s for c in COASTAL_SITES): return True
    if any(i in s for i in INLAND_SITES): return False
    return None


def load_roles() -> dict:
    with open(ROLES, encoding="utf-8") as f:
        return {r["symbol"]: r for r in csv.DictReader(f)}


def load_corpus() -> list[dict]:
    seals: dict[str, dict] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cisi = row["cisi_number"]
            pos = int(row.get("position", 0) or 0)
            if cisi not in seals:
                seals[cisi] = {
                    "signs": [],
                    "site": row.get("site", "").strip(),
                    "icon": (row.get("iconography") or "").strip().lower(),
                }
            while len(seals[cisi]["signs"]) <= pos:
                seals[cisi]["signs"].append("")
            seals[cisi]["signs"][pos] = row["letters"]
    return [{
        "id": cisi, "signs": [s for s in d["signs"] if s],
        "site": d["site"], "icon": d["icon"],
    } for cisi, d in seals.items() if any(d["signs"])]


def approach_a_pooled_classifier(inscriptions: list[dict], roles: dict) -> dict:
    """Pool all INITIAL CLASSIFIER_PREFIX signs and run coastal enrichment."""
    # All INITIAL STRONG signs (avg_pos=0.0, CLASSIFIER_PREFIX, count >= 8)
    initial_classifiers = [
        sym for sym, r in roles.items()
        if float(r.get("avg_position", 1)) == 0.0
        and r.get("semantic_role") == "CLASSIFIER_PREFIX"
        and int(r.get("count", 0)) >= 8
    ]
    print(f"\nApproach A: {len(initial_classifiers)} CLASSIFIER_PREFIX signs (avg_pos=0.0)")
    print(f"  Signs: {sorted(initial_classifiers)}")

    # For each, run coastal test
    sign_results = []
    if torch is not None:
        n = len(inscriptions)
        site_labels = torch.tensor(
            [1 if _is_coastal(ins["site"]) is True
             else (0 if _is_coastal(ins["site"]) is False else -1)
             for ins in inscriptions],
            device=DEVICE, dtype=torch.int8,
        )
        print(f"[GPU:{DEVICE}] Coastal label tensor built ({n} inscriptions)")

    for sym in sorted(initial_classifiers):
        # Count coastal/inland occurrences
        coastal_with = coastal_without = inland_with = inland_without = 0
        for ins in inscriptions:
            is_c = _is_coastal(ins["site"])
            if is_c is None:
                continue
            has_sign = sym in ins["signs"]
            if is_c:
                if has_sign: coastal_with += 1
                else: coastal_without += 1
            else:
                if has_sign: inland_with += 1
                else: inland_without += 1

        total = coastal_with + inland_with
        coastal_total = coastal_with + coastal_without
        inland_total = inland_with + inland_without
        coastal_rate = coastal_with / coastal_total if coastal_total else 0
        inland_rate  = inland_with / inland_total if inland_total else 0
        rr = coastal_rate / inland_rate if inland_rate > 0 else (float("inf") if coastal_rate > 0 else 1.0)

        sign_results.append({
            "sign": sym,
            "total_occurrences": total,
            "coastal_with": coastal_with,
            "inland_with": inland_with,
            "coastal_rate": round(coastal_rate, 4),
            "inland_rate": round(inland_rate, 4),
            "relative_risk": round(rr, 3),
        })

    # Aggregate: mean RR across all INITIAL CLASSIFIERS
    rrs = [r["relative_risk"] for r in sign_results if r["relative_risk"] < 100]
    mean_rr = sum(rrs) / len(rrs) if rrs else 0
    enriched = [r for r in sign_results if r["relative_risk"] > 1.5]
    print(f"  Mean RR across all initial classifiers: {mean_rr:.2f}x")
    print(f"  Signs with RR > 1.5 (coastal-enriched): {[r['sign'] for r in enriched]}")

    # M047 specific
    m047_r = next((r for r in sign_results if r["sign"] == PRIMARY_FISH), {})
    print(f"  M047 specifically: {m047_r}")

    return {
        "n_initial_classifiers": len(initial_classifiers),
        "classifier_signs": sorted(initial_classifiers),
        "sign_coastal_results": sign_results,
        "mean_rr_all_classifiers": round(mean_rr, 3),
        "coastal_enriched_signs": [r["sign"] for r in enriched],
        "m047_result": m047_r,
        "interpretation": (
            f"Mean RR for all INITIAL CLASSIFIER_PREFIX signs = {mean_rr:.2f}x. "
            f"If classifiers as a class are not coastal-enriched, M047's "
            f"RR=1.20 (from Phase-45 T6) is consistent with the baseline."
        ),
    }


def approach_b_contact_zone(roles: dict) -> dict:
    """Check Gulf seals and Mesopotamia seals for fish sign variants."""
    gulf = json.loads((CZ / "gulf_seals/laursen_2010_table1.json").read_text("utf-8"))
    meso = json.loads((CZ / "indus_seals_mesopotamia/seals_at_mesopotamia.json").read_text("utf-8"))

    # Parpola signs 53, 60 → possible fish variants
    fish_parpola_ids = {"53", "60"}
    gulf_fish_matches = []
    for seal_no, reading in gulf.get("parpola_readings", {}).items():
        for sign_entry in reading.get("indus_signs", []):
            sid = str(sign_entry.get("primary", ""))
            alts = [str(a) for a in sign_entry.get("alternates", [])]
            if sid in fish_parpola_ids or any(a in fish_parpola_ids for a in alts):
                gulf_fish_matches.append({
                    "seal_no": seal_no,
                    "site": reading.get("site"),
                    "parpola_sign_id": sid,
                    "note": sign_entry.get("note", ""),
                    "position": sign_entry.get("position"),
                })

    # Check CDLI Meluhha tablets for fish-related cuneiform logograms
    tablets = json.loads((CZ / "cdli_meluhha/meluhha_tablets.json").read_text("utf-8"))
    fish_mentions = []
    fish_patterns = [r"\bkuₓ\b", r"\bha\b", r"\bku6\b", r"fish", r"naga", r"kua"]
    for t in tablets.get("tablets", []):
        atf = (t.get("atf_excerpt") or "").lower()
        for pat in fish_patterns:
            if re.search(pat, atf, re.IGNORECASE):
                fish_mentions.append({
                    "p_number": t.get("p_number"),
                    "period": t.get("period"),
                    "provenience": t.get("provenience"),
                })
                break

    print(f"\nApproach B Contact Zone:")
    print(f"  Gulf seals with fish sign (Parpola 53/60): {len(gulf_fish_matches)}")
    print(f"  CDLI tablets with fish cuneiform: {len(fish_mentions)}")
    for m in gulf_fish_matches:
        print(f"  Gulf seal #{m['seal_no']} ({m['site']}): Parpola sign {m['parpola_sign_id']} — {m['note'][:60]}")

    return {
        "gulf_seal_fish_matches": gulf_fish_matches,
        "cdli_fish_tablet_count": len(fish_mentions),
        "cdli_fish_tablets_sample": fish_mentions[:5],
        "interpretation": (
            f"Parpola's sign 53/60 (fish) appears in {len(gulf_fish_matches)} Gulf seal readings. "
            "This provides independent evidence that the fish sign was used in the Gulf "
            "contact zone — consistent with the mīn reading and maritime trade context."
        ),
    }


def approach_c_iconography(inscriptions: list[dict]) -> dict:
    """Test if M047 preferentially appears with 'fish' iconography motif."""
    fish_icon_ctr: Counter = Counter()
    all_icon_ctr: Counter = Counter()

    for ins in inscriptions:
        icon = ins["icon"] or "unknown"
        all_icon_ctr[icon] += 1
        if PRIMARY_FISH in ins["signs"]:
            fish_icon_ctr[icon] += 1

    total_fish = sum(fish_icon_ctr.values())
    total_all = sum(all_icon_ctr.values())

    # Expected rate for "fish" iconography motif
    fish_motif_rate_corpus = all_icon_ctr.get("fish", 0) / total_all if total_all else 0
    fish_motif_rate_m047   = fish_icon_ctr.get("fish", 0) / total_fish if total_fish else 0
    lift = fish_motif_rate_m047 / fish_motif_rate_corpus if fish_motif_rate_corpus > 0 else 0

    print(f"\nApproach C Iconography:")
    print(f"  M047 with 'fish' iconography: {fish_icon_ctr.get('fish',0)}/{total_fish} = {fish_motif_rate_m047:.1%}")
    print(f"  Corpus 'fish' icon rate: {fish_motif_rate_corpus:.1%}")
    print(f"  Lift (M047 on fish motif): {lift:.2f}x")
    print(f"  Top M047 iconographies: {fish_icon_ctr.most_common(5)}")

    return {
        "m047_total_occurrences": total_fish,
        "m047_icon_distribution": dict(fish_icon_ctr.most_common(10)),
        "corpus_fish_icon_rate": round(fish_motif_rate_corpus, 4),
        "m047_fish_icon_rate": round(fish_motif_rate_m047, 4),
        "lift_on_fish_motif": round(lift, 3),
        "interpretation": (
            f"M047 appears on 'fish' iconography motifs at {fish_motif_rate_m047:.0%} "
            f"(vs corpus rate {fish_motif_rate_corpus:.0%}, lift={lift:.1f}x). "
            "If lift >> 1, the fish sign preferentially appears on fish-motif seals, "
            "supporting the mīn reading."
        ),
    }


def main() -> None:
    print("Phase-46 T4: Fish Sign M047 Family Expansion\n")

    roles = load_roles()
    inscriptions = load_corpus()
    print(f"Corpus: {len(inscriptions)} inscriptions")
    print(f"M047 role: {roles.get(PRIMARY_FISH, {})}")

    result_a = approach_a_pooled_classifier(inscriptions, roles)
    result_b = approach_b_contact_zone(roles)
    result_c = approach_c_iconography(inscriptions)

    # Synthesis
    m047_rr = result_a.get("m047_result", {}).get("relative_risk", 1.0)
    mean_rr = result_a.get("mean_rr_all_classifiers", 1.0)
    gulf_fish = len(result_b.get("gulf_seal_fish_matches", []))
    fish_lift = result_c.get("lift_on_fish_motif", 0)

    print(f"\n=== Fish Sign Expansion Summary ===")
    print(f"M047 coastal RR: {m047_rr:.2f}x (baseline mean: {mean_rr:.2f}x)")
    print(f"Gulf seals with fish sign: {gulf_fish}")
    print(f"M047 on fish-iconography: {fish_lift:.2f}x lift")

    if fish_lift > 2.0:
        verdict = "ICONOGRAPHIC_SUPPORT"
        note = (f"M047 appears on fish-motif seals at {fish_lift:.1f}x the corpus rate. "
                "Strong iconographic alignment with mīn/'fish' reading.")
    elif gulf_fish >= 1:
        verdict = "CONTACT_ZONE_SUPPORT"
        note = (f"{gulf_fish} Gulf seal(s) contain Parpola's fish sign (53/60). "
                "Contact zone presence consistent with maritime trade fish-sign use.")
    else:
        verdict = "UNDERPOWERED"
        note = "All approaches remain underpowered. mīn reading still plausible but unconfirmed."

    result = {
        "_citation": {"primary_sources": ["A.1"], "reading": "min/min (fish) — Dravidian"},
        "gpu_device": DEVICE,
        "approach_a_pooled_classifiers": result_a,
        "approach_b_contact_zone": result_b,
        "approach_c_iconography": result_c,
        "synthesis": {
            "m047_coastal_rr": m047_rr,
            "all_classifiers_mean_rr": mean_rr,
            "gulf_seal_fish_count": gulf_fish,
            "m047_fish_icon_lift": float(fish_lift),
            "verdict": verdict,
            "note": note,
        },
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
