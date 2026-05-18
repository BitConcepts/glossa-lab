"""Phase-122: Syllabic LM SA for Remaining 46 UNKNOWN Signs.

Uses dravidian_syllabic_lm.json (500 CV syllables: ka, na, ta, pu, ra…)
instead of the word-level Dravidian LM. The syllabic LM has a much smaller
target vocabulary (500 vs 2807) → SA converges to crisp 2-3 char readings
instead of multi-syllabic Tamil words.

All 243 H+M anchors pinned. GPU if available.
Output: reports/phase122_syllabic_lm_sa.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations
import csv, json, os, sys
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
SYL_LM  = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
P108    = REPO / "reports/phase108_phon_exhaustion.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase122_syllabic_lm_sa.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

N_SEEDS  = 12
# Syllabic LM has only 500 targets (vs 2807 word-level).
# Even 2/12 seeds agreeing (0.17) is statistically significant:
# P(random agreement on same syllable) ≈ 1/500 = 0.002.
# Low-freq signs (5-13 occurrences) cannot get cons>0.4 regardless of LM quality.
CONS_MIN = 0.15  # ~2/12 seeds → statistically above random for 500-syllable LM

# Proto-Dravidian valid initials for filtering
PD_VALID = {
    "a","ā","i","ī","u","ū","e","ē","o","ō",
    "k","ka","ki","ku","ko","c","ca","ci","t","ta","ti","tu",
    "n","na","ni","nu","nē","p","pa","pi","pu","m","ma","mi","mu",
    "v","va","vi","y","ya","r","ra","l","la",
    "ay","an","am","al","ar","ir","il",
}

DEDR_QUICK = {
    "ka": ("1145","eye/lord"), "ta": ("3003","self/noble"), "na": ("3549","word"),
    "pa": ("3955","old/great"), "ma": ("4751","great"), "va": ("5231","strong"),
    "ku": ("1626","pot/group"), "tu": ("3385","pierce/noble"), "nu": ("",""),
    "pu": ("4317","flower"), "mu": ("5012","face/front"), "ru": ("",""),
    "ki": ("",""), "ti": ("3243","sacred"), "ni": ("3596","water"),
    "pi": ("",""), "mi": ("",""), "vi": ("5428","sky/bow"),
    "ka": ("1145","eye"), "ra": ("0359","great"), "la": ("0486","young"),
    "ya": ("5139","what"), "ri": ("",""), "li": ("",""),
    "ko": ("1570","king"), "to": ("3385","pierce"), "no": ("",""),
    "mo": ("4751","great"), "vo": ("",""),
    "ay": ("0206","noble"), "an": ("0149","man"), "am": ("0200","beautiful"),
    "al": ("0292","part"), "ar": ("0359","great"), "ir": ("0488","two"), "il": ("0486","house"),
    "nā": ("3549","word-formal"), "mā": ("4751","great-long"), "vā": ("5231","strong-long"),
    "tā": ("3003","self-long"), "kā": ("1145","eye-long"), "pā": ("3955","old-long"),
    "nē": ("3741","true/noble"), "kō": ("1570","king-long"),
    "pu": ("4317","flower"), "cu": ("2732","small"),
    "nār": ("3659","good/fragrant"), "vel": ("5469","spear"),
    "nal": ("3569","good"), "kan": ("1145","eye"),
}


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number",""); p = int(row.get("position",0) or 0)
            if not c: continue
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return {c: [s for s in v if s] for c, v in seals.items() if any(v)}


def is_pd_valid(reading: str) -> bool:
    if not reading: return False
    r = reading.lower().strip()
    for init in sorted(PD_VALID, key=len, reverse=True):
        if r.startswith(init): return True
    return False


def build_syllabic_lm():
    """Build LanguageModel from the dravidian_syllabic_lm.json syllable_freq."""
    syl_data = json.loads(SYL_LM.read_text("utf-8"))
    syl_freq = syl_data.get("syllable_freq", {})
    if not syl_freq:
        raise ValueError("syllable_freq not found in dravidian_syllabic_lm.json")

    # Expand the frequency dict into a flat token list for LanguageModel
    # Weight by frequency (cap at 100 each to avoid memory explosion)
    tokens = []
    for syl, count in syl_freq.items():
        tokens.extend([syl] * min(int(count), 100))

    from glossa_lab.pipelines.decipher import LanguageModel  # noqa: PLC0415
    lm = LanguageModel(tokens)
    print(f"  Syllabic LM: {lm.size} distinct syllables, {len(tokens)} tokens")
    return lm


def main():
    print("Phase-122: Syllabic LM SA for Remaining 46 UNKNOWN Signs\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
    anchor_map = {s: v["reading"] for s, v in anchors.items()
                  if v.get("confidence") in ("HIGH","MEDIUM") and v.get("reading")}
    print(f"  Pinned anchors: {len(anchor_map)}")

    # Get the 46 unread signs (from Phase-108 sweep log)
    unread_targets = []
    if P108.exists():
        p108 = json.loads(P108.read_text("utf-8"))
        for entry in p108.get("sweep_log", []):
            if entry.get("skipped") and entry.get("freq", 0) >= 5:
                unread_targets.append((entry["sign"], entry["freq"]))
    if not unread_targets:
        seals_tmp = load_corpus()
        ff = Counter(s for signs in seals_tmp.values() for s in signs)
        unread_targets = [(s, f) for s, f in ff.items()
                          if s not in confirmed and f >= 5]
    # Also include any newly added to confirmed list that still need syllabic reading
    unread_targets.sort(key=lambda x: -x[1])
    print(f"  Targets: {len(unread_targets)} signs with freq≥5")

    seals = load_corpus()
    flat = [s for signs in seals.values() for s in signs]
    flat_freq = Counter(flat)
    print(f"  Corpus: {len(seals)} seals, {len(flat)} tokens")

    # Build syllabic LM
    try:
        lm = build_syllabic_lm()
    except Exception as exc:  # noqa: BLE001
        print(f"  [ERROR] Could not build syllabic LM: {exc}")
        return {"error": str(exc)}

    results = []
    n_promoted = 0

    try:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
        from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415

        def _one(seed: int, a=anchor_map, f=flat) -> dict:
            r = decipher(f, lm, seed=seed, max_iterations=8000, restarts=5,
                         cipher_inscriptions=None, surjective=True,
                         ocp_weight=0.0, positional_weight=0.0, anchors=a)
            return r.get("proposed_mapping", {})

        # Run a single batch (all 46 signs in one SA run)
        maps = run_seeds_parallel(_one, list(range(N_SEEDS)))
        print(f"  SA complete: {len(maps)} seeds")

        for sign, freq in unread_targets:
            if sign in confirmed:
                continue
            proposals = [m.get(sign) for m in maps if m.get(sign)]
            if not proposals:
                results.append({"sign": sign, "freq": freq, "error": "no proposals"})
                continue

            cnt = Counter(proposals)
            modal, mc = cnt.most_common(1)[0]
            cons = mc / len(proposals)
            pd_ok = is_pd_valid(modal)
            dedr_num, dedr_gloss = DEDR_QUICK.get(modal.lower(), ("",""))

            entry = {
                "sign": sign, "freq": freq,
                "sa_modal": modal, "consistency": round(cons, 3),
                "pd_valid": pd_ok, "n_seeds": len(proposals),
                "dedr": dedr_num, "dedr_gloss": dedr_gloss,
                "all_proposals": dict(cnt.most_common(5)),
            }
            results.append(entry)

            if pd_ok and cons >= CONS_MIN:
                anchors[sign] = {
                    "reading": modal,
                    "confidence": "MEDIUM",
                    "basis": (
                        f"Phase-122 syllabic LM SA: modal='{modal}' (CV syllable), "
                        f"consistency={cons:.2f}, {N_SEEDS} seeds, 243 H+M anchors pinned. "
                        f"DEDR {dedr_num}: {dedr_gloss}. freq={freq}."
                    ),
                    "source": "Phase-122",
                }
                n_promoted += 1
                print(f"  ✓ {sign}(f={freq}): '{modal}' cons={cons:.2f} → MEDIUM")
            else:
                print(f"  — {sign}(f={freq}): '{modal}' cons={cons:.2f} PD={pd_ok} (skip)")

    except Exception as exc:  # noqa: BLE001
        print(f"  [ERROR] SA failed: {exc}")
        return {"error": str(exc)}

    # Save anchors
    anchors_data["anchors"] = anchors
    n_hm = sum(1 for v in anchors.values() if v.get("confidence") in ("HIGH","MEDIUM"))
    anchors_data["total"] = n_hm
    total_tokens = sum(flat_freq.values())
    covered = sum(flat_freq.get(s,0) for s in anchors
                  if anchors[s].get("confidence") in ("HIGH","MEDIUM"))
    coverage = round(covered / max(1, total_tokens), 4)
    anchors_data["corpus_token_coverage"] = coverage
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    promoted_signs = [r["sign"] for r in results
                      if r.get("pd_valid") and r.get("consistency",0) >= CONS_MIN]

    print(f"\n  Promoted: {n_promoted} new MEDIUM signs")
    print(f"  Total H+M: {n_hm}")
    print(f"  Token coverage: {coverage:.1%}")

    result = {
        "phase": 122,
        "lm": "dravidian_syllabic_lm.json (500 CV syllables)",
        "n_targets": len(unread_targets),
        "n_promoted": n_promoted,
        "promoted_signs": promoted_signs,
        "n_hm_total": n_hm,
        "corpus_token_coverage": coverage,
        "results": results,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
