"""Phases 363-370: Deep Experiments — Push Beyond Validation

Phase 363: Site-stratified translation — do readings work equally across all sites?
Phase 364: Compound word detection — find multi-sign words via PMI clustering
Phase 365: Title-suffix formula mining — extract [TITLE]-[SUFFIX] patterns
Phase 366: Seal-type function classification — do different seal types have different formulas?
Phase 367: Reading entropy profiling — which signs have the most/least predictable contexts?
Phase 368: Collocate-based LOW sign upgrade — use HIGH neighbors to propose readings
Phase 369: Gulf seal cross-check — do readings work on Failaka/Bahrain seals?
Phase 370: Full corpus decoded statistics — comprehensive coverage and translation report

Output: outputs/phase363_370_deep_experiments.json
"""
from __future__ import annotations
import csv, json, math, random
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"
OUT_PATH = REPO / "outputs" / "phase363_370_deep_experiments.json"

def _load_anchors():
    return json.loads(ANCHORS_PATH.read_text("utf-8")).get("anchors", {})
def _load_high_map():
    a = _load_anchors()
    return {s: i["reading"] for s, i in a.items() if i.get("confidence") == "HIGH" and i.get("reading")}
def _load_inscriptions():
    ins = []; cur = None; signs = []; motif = ""; site = ""
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["cisi_number"] != cur:
                if signs: ins.append({"id": cur, "signs": signs, "motif": motif, "site": site})
                cur = r["cisi_number"]; signs = []
                motif = (r.get("iconography") or "").strip().lower()
                site = (r.get("site") or "").strip()
            signs.append(r["letters"])
    if signs: ins.append({"id": cur, "signs": signs, "motif": motif, "site": site})
    return ins
def _clean(r): return r.split("/")[0].strip().lower() if r else ""

ROOTS = {_clean(r) for r in ["kol/koḷ","il/iḷ","ūr","pon","kal","nīr","kōṉ","kō","yānai","kaḷiṟu","erutu",
    "puli","nakaram","vēḷ","kāṇṭāmirukam","māṭu","āṉai","kōṭṭāṉ","mā","veL","nal","nēr","cem","tiru",
    "pū/puḷ","mutalai","vēṅkai","maṟi","kai","vī","kul"]}
SUFFIXES = {_clean(r) for r in ["an/aṇ","ay/ā","am/neuter","iN/in (genitive of)","iṉ/locative",
    "ōṭu/comitative","ā/āl","tu/tū","mu/muṉ","ka/kaṇ","oṉṟu/1"]}

# ═══════════════════════════════════════════════════════════════════════
def phase363_site_stratified():
    """Do readings produce coherent translations across ALL sites equally?"""
    print("\n[Phase 363] Site-stratified translation")
    hm = _load_high_map(); ins = _load_inscriptions()
    site_groups = defaultdict(list)
    for i in ins: site_groups[i["site"]].append(i)

    site_results = {}
    for site, group in sorted(site_groups.items(), key=lambda x: -len(x[1])):
        if len(group) < 10: continue
        n_readable = 0
        for i in group:
            readings = [_clean(hm.get(s, "")) for s in i["signs"]]
            coverage = sum(1 for r in readings if r) / max(1, len(readings))
            cats = []
            for r in readings:
                if r in ROOTS: cats.append("R")
                elif r in SUFFIXES: cats.append("S")
            has_rs = any(cats[j]=="R" and j+1<len(cats) and cats[j+1]=="S" for j in range(len(cats)-1))
            if coverage >= 0.5 and has_rs: n_readable += 1
        site_results[site] = {"n_seals": len(group), "n_readable": n_readable,
                              "readable_rate": round(n_readable/len(group), 3)}

    avg_rate = sum(v["readable_rate"] for v in site_results.values()) / max(1, len(site_results))
    return {"sites": site_results, "n_sites": len(site_results), "avg_readable_rate": round(avg_rate, 3),
            "verdict": f"Site-stratified: {len(site_results)} sites, avg {avg_rate:.0%} readable. "
                       + ("CONSISTENT" if avg_rate > 0.2 else "INCONSISTENT")}

# ═══════════════════════════════════════════════════════════════════════
def phase364_compound_words():
    """Detect compound words via high-PMI sign clusters."""
    print("\n[Phase 364] Compound word detection")
    hm = _load_high_map(); ins = _load_inscriptions()
    pair_freq = Counter(); sign_freq = Counter(); total = 0
    for i in ins:
        for s in i["signs"]: sign_freq[s] += 1
        for j in range(len(i["signs"])-1):
            pair_freq[(i["signs"][j], i["signs"][j+1])] += 1; total += 1
    tot_s = sum(sign_freq.values())
    compounds = []
    for (a,b), c in pair_freq.items():
        if sign_freq[a] >= 5 and sign_freq[b] >= 5:
            pmi = math.log2((c/total) / ((sign_freq[a]/tot_s) * (sign_freq[b]/tot_s) + 1e-10) + 1e-10)
            if pmi > 2.0:
                ra, rb = hm.get(a, "?"), hm.get(b, "?")
                compounds.append({"signs": f"{a}+{b}", "readings": f"{_clean(ra)}+{_clean(rb)}",
                                  "pmi": round(pmi, 2), "count": c})
    compounds.sort(key=lambda x: -x["pmi"])
    return {"n_compounds": len(compounds), "top_20": compounds[:20],
            "verdict": f"Compounds: {len(compounds)} high-PMI pairs (PMI>2.0). Top: {compounds[0]['readings'] if compounds else 'none'}."}

# ═══════════════════════════════════════════════════════════════════════
def phase365_title_suffix_formulas():
    """Extract [TITLE/QUALITY]-[ROOT]-[SUFFIX] formulas."""
    print("\n[Phase 365] Title-suffix formula mining")
    hm = _load_high_map(); ins = _load_inscriptions()
    TITLES = {"mā", "nal", "nēr", "tiru", "veL", "cem"}
    formulas = Counter()
    for i in ins:
        readings = [_clean(hm.get(s, "")) for s in i["signs"]]
        for j in range(len(readings)-2):
            if readings[j] in TITLES and readings[j+1] in ROOTS and readings[j+2] in SUFFIXES:
                formulas[f"{readings[j]}-{readings[j+1]}-{readings[j+2]}"] += 1
    top = formulas.most_common(20)
    return {"n_formulas": len(formulas), "total_occurrences": sum(formulas.values()),
            "top_20": [{"formula": f, "count": c} for f, c in top],
            "verdict": f"Title formulas: {len(formulas)} unique, {sum(formulas.values())} total occurrences."}

# ═══════════════════════════════════════════════════════════════════════
def phase366_seal_type_function():
    """Do different motif types have different reading distributions?"""
    print("\n[Phase 366] Seal-type function classification")
    hm = _load_high_map(); ins = _load_inscriptions()
    motif_readings = defaultdict(Counter)
    for i in ins:
        if not i["motif"]: continue
        for s in i["signs"]:
            r = _clean(hm.get(s, ""))
            if r: motif_readings[i["motif"]][r] += 1

    motif_profiles = {}
    for motif, rc in motif_readings.items():
        total = sum(rc.values())
        if total < 20: continue
        root_pct = sum(rc[r] for r in rc if r in ROOTS) / total
        suf_pct = sum(rc[r] for r in rc if r in SUFFIXES) / total
        top3 = rc.most_common(3)
        motif_profiles[motif] = {"n_tokens": total, "root_pct": round(root_pct, 2),
                                 "suffix_pct": round(suf_pct, 2),
                                 "top_3": [f"{r}({c})" for r, c in top3]}

    return {"n_motif_types": len(motif_profiles), "profiles": motif_profiles,
            "verdict": f"Seal types: {len(motif_profiles)} motif types profiled with reading distributions."}

# ═══════════════════════════════════════════════════════════════════════
def phase367_reading_entropy():
    """Which readings have the most/least predictable contexts?"""
    print("\n[Phase 367] Reading entropy profiling")
    hm = _load_high_map(); ins = _load_inscriptions()
    # For each reading, compute the entropy of its left/right context
    left_ctx = defaultdict(Counter); right_ctx = defaultdict(Counter)
    for i in ins:
        readings = [_clean(hm.get(s, "")) for s in i["signs"]]
        for j, r in enumerate(readings):
            if not r: continue
            if j > 0 and readings[j-1]: left_ctx[r][readings[j-1]] += 1
            if j < len(readings)-1 and readings[j+1]: right_ctx[r][readings[j+1]] += 1

    def _entropy(counter):
        total = sum(counter.values())
        if total < 2: return 0
        return -sum((c/total)*math.log2(c/total) for c in counter.values() if c > 0)

    profiles = []
    for r in set(list(left_ctx.keys()) + list(right_ctx.keys())):
        lh = _entropy(left_ctx[r]); rh = _entropy(right_ctx[r])
        total = sum(left_ctx[r].values()) + sum(right_ctx[r].values())
        if total >= 10:
            profiles.append({"reading": r, "left_entropy": round(lh, 2), "right_entropy": round(rh, 2),
                            "avg_entropy": round((lh+rh)/2, 2), "total_contexts": total})

    profiles.sort(key=lambda x: x["avg_entropy"])
    low_entropy = [p for p in profiles if p["avg_entropy"] < 1.5]  # Predictable
    high_entropy = [p for p in profiles if p["avg_entropy"] > 3.0]  # Unpredictable

    return {"n_profiled": len(profiles), "low_entropy": low_entropy[:10], "high_entropy": high_entropy[:10],
            "verdict": f"Entropy: {len(low_entropy)} predictable readings, {len(high_entropy)} unpredictable. "
                       f"Most predictable: {profiles[0]['reading'] if profiles else 'none'}."}

# ═══════════════════════════════════════════════════════════════════════
def phase368_collocate_upgrade():
    """Use HIGH-sign collocate patterns to propose readings for unread signs."""
    print("\n[Phase 368] Collocate-based reading proposal")
    hm = _load_high_map(); ins = _load_inscriptions(); anchors = _load_anchors()
    unread = {s for s, i in anchors.items() if not i.get("reading") or i.get("confidence") == "LOW"}

    sign_freq = Counter()
    left_hm = defaultdict(Counter); right_hm = defaultdict(Counter)
    for i in ins:
        for s in i["signs"]: sign_freq[s] += 1
        for j in range(len(i["signs"])):
            s = i["signs"][j]
            if s not in unread: continue
            if j > 0 and i["signs"][j-1] in hm: left_hm[s][hm[i["signs"][j-1]]] += 1
            if j < len(i["signs"])-1 and i["signs"][j+1] in hm: right_hm[s][hm[i["signs"][j+1]]] += 1

    proposals = []
    for s in sorted(unread):
        if sign_freq.get(s, 0) < 5: continue
        left_top = left_hm[s].most_common(3)
        right_top = right_hm[s].most_common(3)
        # If consistently preceded by STEM and followed by CASE → likely a SUFFIX
        left_cats = [("ROOT" if _clean(r) in ROOTS else "SUFFIX" if _clean(r) in SUFFIXES else "OTHER") for r, _ in left_top]
        right_cats = [("ROOT" if _clean(r) in ROOTS else "SUFFIX" if _clean(r) in SUFFIXES else "OTHER") for r, _ in right_top]

        predicted_role = "UNKNOWN"
        if left_cats and left_cats[0] == "ROOT": predicted_role = "SUFFIX_CANDIDATE"
        elif right_cats and right_cats[0] == "SUFFIX": predicted_role = "ROOT_CANDIDATE"
        elif left_cats and left_cats[0] == "SUFFIX": predicted_role = "ROOT_CANDIDATE"

        proposals.append({"sign": s, "freq": sign_freq[s], "predicted_role": predicted_role,
                         "left_context": [f"{r}({c})" for r, c in left_top],
                         "right_context": [f"{r}({c})" for r, c in right_top]})

    proposals.sort(key=lambda x: -x["freq"])
    n_suffix = sum(1 for p in proposals if p["predicted_role"] == "SUFFIX_CANDIDATE")
    n_root = sum(1 for p in proposals if p["predicted_role"] == "ROOT_CANDIDATE")

    return {"n_unread_scored": len(proposals), "n_suffix_candidates": n_suffix, "n_root_candidates": n_root,
            "top_20": proposals[:20],
            "verdict": f"Collocate upgrade: {n_suffix} suffix candidates, {n_root} root candidates from {len(proposals)} unread signs."}

# ═══════════════════════════════════════════════════════════════════════
def phase369_gulf_seals():
    """Check if readings work on seals from Gulf sites (Failaka-like contexts)."""
    print("\n[Phase 369] Gulf seal cross-check")
    hm = _load_high_map(); ins = _load_inscriptions()
    gulf_keywords = {"failaka", "bahrain", "dilmun", "oman", "gulf", "lothal", "surkotada", "dholavira"}
    coastal = [i for i in ins if any(k in i["site"].lower() for k in gulf_keywords)]
    inland = [i for i in ins if i not in coastal and i["site"]]

    def _coherence(group):
        coh_vals = []
        for i in group:
            readings = [_clean(hm.get(s, "")) for s in i["signs"]]
            cats = []
            for r in readings:
                if r in ROOTS: cats.append("R")
                elif r in SUFFIXES: cats.append("S")
            if len(cats) >= 2:
                nv = sum(1 for j in range(len(cats)-1) if (cats[j]=="R" and cats[j+1]=="S") or
                         (cats[j]=="S" and cats[j+1]=="R") or (cats[j]=="R" and cats[j+1]=="R"))
                coh_vals.append(nv / (len(cats)-1))
        return sum(coh_vals) / max(1, len(coh_vals))

    coastal_coh = _coherence(coastal); inland_coh = _coherence(inland)
    return {"coastal_seals": len(coastal), "inland_seals": len(inland),
            "coastal_coherence": round(coastal_coh, 3), "inland_coherence": round(inland_coh, 3),
            "difference": round(abs(coastal_coh - inland_coh), 3),
            "verdict": f"Gulf: coastal {coastal_coh:.0%} vs inland {inland_coh:.0%} coherence. "
                       f"{'CONSISTENT' if abs(coastal_coh-inland_coh) < 0.1 else 'DIVERGENT'} across regions."}

# ═══════════════════════════════════════════════════════════════════════
def phase370_corpus_stats():
    """Comprehensive corpus-wide decoded statistics."""
    print("\n[Phase 370] Full corpus decoded statistics")
    hm = _load_high_map(); all_map = {s: i["reading"] for s, i in _load_anchors().items() if i.get("reading")}
    ins = _load_inscriptions()

    total_ins = len(ins)
    total_tokens = sum(len(i["signs"]) for i in ins)
    total_types = len(set(s for i in ins for s in i["signs"]))

    high_tokens = sum(1 for i in ins for s in i["signs"] if s in hm)
    any_tokens = sum(1 for i in ins for s in i["signs"] if s in all_map)

    fully_decoded = sum(1 for i in ins if all(s in hm for s in i["signs"]))
    partially_decoded = sum(1 for i in ins if any(s in hm for s in i["signs"]) and not all(s in hm for s in i["signs"]))
    no_reading = total_ins - fully_decoded - partially_decoded

    lengths = [len(i["signs"]) for i in ins]
    avg_len = sum(lengths) / max(1, len(lengths))

    reading_freq = Counter()
    for i in ins:
        for s in i["signs"]:
            r = _clean(hm.get(s, ""))
            if r: reading_freq[r] += 1

    return {
        "total_inscriptions": total_ins, "total_tokens": total_tokens, "total_sign_types": total_types,
        "high_token_coverage": round(high_tokens / max(1, total_tokens), 4),
        "any_token_coverage": round(any_tokens / max(1, total_tokens), 4),
        "fully_decoded_inscriptions": fully_decoded, "partially_decoded": partially_decoded,
        "no_reading": no_reading, "avg_inscription_length": round(avg_len, 1),
        "n_distinct_readings": len(reading_freq),
        "top_20_readings": [{"reading": r, "count": c} for r, c in reading_freq.most_common(20)],
        "verdict": (f"Corpus: {total_ins} inscriptions, {total_tokens} tokens. "
                    f"HIGH coverage: {high_tokens/max(1,total_tokens):.0%}. "
                    f"Fully decoded: {fully_decoded} ({fully_decoded/max(1,total_ins):.0%}). "
                    f"{len(reading_freq)} distinct readings used."),
    }

# ═══════════════════════════════════════════════════════════════════════
def main():
    print("=" * 70); print("PHASES 363-370: DEEP EXPERIMENTS"); print("=" * 70)
    results = {}
    for name, fn in [("phase363", phase363_site_stratified), ("phase364", phase364_compound_words),
                     ("phase365", phase365_title_suffix_formulas), ("phase366", phase366_seal_type_function),
                     ("phase367", phase367_reading_entropy), ("phase368", phase368_collocate_upgrade),
                     ("phase369", phase369_gulf_seals), ("phase370", phase370_corpus_stats)]:
        try:
            results[name] = fn(); print(f"  → {results[name]['verdict']}")
        except Exception as e:
            results[name] = {"error": str(e)}; print(f"  → {name} ERROR: {e}")
            import traceback; traceback.print_exc()
    OUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved to {OUT_PATH}")
    print("\n" + "=" * 70 + "\nSUMMARY\n" + "=" * 70)
    for k in sorted(results):
        v = results[k].get("verdict", results[k].get("error", ""))
        print(f"  {k}: {v[:130]}")

if __name__ == "__main__": main()
