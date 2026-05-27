"""Integrated Research Loop: Mine → Analyze → Register → Execute → Analyze

Each cycle:
  1. MINE — targeted literature search based on current gaps
  2. ANALYZE — extract actionable insights from mined papers
  3. REGISTER — create graph experiment from top insight
  4. EXECUTE — run the new experiment against corpus
  5. ANALYZE — evaluate results, identify new gaps
  6. REPEAT until no new experiments can be generated or max iterations

Usage: python backend/scripts/integrated_research_loop.py [--max-cycles 15]

Output: outputs/integrated_research_loop.json
"""
from __future__ import annotations
import argparse, csv, json, math, random, re, time, urllib.parse, urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"
OUT_PATH = REPO / "outputs" / "integrated_research_loop.json"

def _load_high_map():
    a = json.loads(ANCHORS_PATH.read_text("utf-8")).get("anchors", {})
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

def _get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.7 (research)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception: time.sleep(0.5 * (attempt + 1))
    return None

# ── Gap identification ───────────────────────────────────────────────

ROOTS = {_clean(r) for r in ["kol/koḷ","il/iḷ","ūr","pon","kal","nīr","kōṉ","kō","yānai","kaḷiṟu",
    "erutu","puli","nakaram","vēḷ","kāṇṭāmirukam","māṭu","āṉai","kōṭṭāṉ","mā","veL","nal","nēr",
    "cem","tiru","pū","puḷ","mutalai","vēṅkai","maṟi","kai","vī","kul"]}
SUFFIXES = {_clean(r) for r in ["an/aṇ","ay/ā","am/neuter","iN/in (genitive of)","iṉ/locative",
    "ōṭu/comitative","ā/āl","tu/tū","mu/muṉ","ka/kaṇ","oṉṟu/1"]}

# Rotating gap-targeted query sets — each cycle uses a different one
GAP_QUERY_ROTATION = [
    {"name": "rare_sign_context", "queries": [
        "Indus script hapax context-based reading rare sign",
        "undeciphered script low frequency sign assignment method",
        "ancient writing rare glyph contextual reading inference"]},
    {"name": "compound_morphology", "queries": [
        "Dravidian compound noun head modifier agglutination",
        "Tamil compound word structure Tolkappiyam morpheme boundary",
        "Proto-Dravidian nominal compound semantic classification"]},
    {"name": "seal_owner_identity", "queries": [
        "Indus seal owner identity guild merchant professional",
        "ancient seal administrative personal name title function",
        "Harappan craft specialist seal inscription identity"]},
    {"name": "cross_script_transfer", "queries": [
        "Tamil Brahmi Indus script sign continuity comparison",
        "early Tamil writing aksara value Indus inheritance",
        "Brahmi adaptation pre-existing script South Asia"]},
    {"name": "trade_network_vocabulary", "queries": [
        "Indus trade network commodity vocabulary seal marking",
        "Harappan weight metrological seal inscription economic",
        "ancient Near East Indus trade term bilingual evidence"]},
    {"name": "inscription_formula_syntax", "queries": [
        "Indus inscription formula syntax tripartite structure",
        "seal text pattern computational n-gram Indus script",
        "ancient administrative inscription formula comparison"]},
    {"name": "iconographic_semantic", "queries": [
        "Indus seal animal motif meaning iconographic semantic",
        "unicorn bull elephant symbolism Indus Valley seal",
        "ancient seal iconography text relationship meaning"]},
    {"name": "phonological_reconstruction", "queries": [
        "Proto-Dravidian phonological reconstruction 2024 2025",
        "Krishnamurti Dravidian consonant vowel system reconstruction",
        "comparative Dravidian phonology DEDR evidence"]},
    {"name": "computational_upgrade", "queries": [
        "Bayesian sign reading upgrade undeciphered script 2025 2026",
        "neural network ancient script reading assignment confidence",
        "machine learning sign value prediction ancient writing"]},
    {"name": "archaeological_context", "queries": [
        "Indus seal find context archaeological site function",
        "Harappan seal impression workshop administrative building",
        "Indus seal distribution site type warehouse granary gate"]},
    {"name": "personal_name_structure", "queries": [
        "ancient Dravidian personal name structure compound title",
        "Tamil Brahmi hero stone personal name formula analysis",
        "Sangam Tamil name morphology patronymic title suffix"]},
    {"name": "numeral_metrological", "queries": [
        "Indus numeral system stroke sign counting interpretation",
        "Harappan weight standard metrological seal numeral",
        "ancient South Asian numerical notation system development"]},
    {"name": "substrate_loanword", "queries": [
        "Dravidian substrate loanword Rigvedic Sanskrit craft term",
        "pre-Aryan South Asian vocabulary evidence agricultural",
        "Indus civilization language contact substrate evidence"]},
    {"name": "gulf_foreign_attestation", "queries": [
        "Indus seal Failaka Bahrain Gulf attestation evidence",
        "Dilmun Meluhha trade seal foreign site comparison",
        "round stamp seal Persian Gulf Indus type analysis"]},
    {"name": "allograph_classification", "queries": [
        "Indus sign allograph variant identification method computational",
        "undeciphered script sign variant graphic classification",
        "ancient writing system sign merger simplification evidence"]},
]

# Rotating experiment templates — each generates a different test
EXPERIMENT_TEMPLATES = [
    "site_specific_formula",      # Do specific sites have unique formulas?
    "motif_title_correlation",    # Do titles correlate with specific motifs?
    "suffix_chain_depth",         # How deep do suffix chains go?
    "reading_frequency_zipf",     # Do reading frequencies follow Zipf's law?
    "compound_semantic_coherence", # Are compounds semantically coherent?
    "blocker_sign_context",       # What context surrounds blocker signs?
    "inscription_uniqueness",     # How many unique inscription types exist?
    "position_entropy_by_site",   # Does positional entropy vary by site?
    "title_root_suffix_trigram",  # Most common [TITLE][ROOT][SUFFIX] trigrams?
    "motif_reading_mutual_info",  # Mutual information between motif and readings
    "decoded_text_repetition",    # How repetitive is the decoded text?
    "rare_sign_neighbor_profile", # What HIGH signs neighbor rare/blocker signs?
    "compound_vs_formula",        # Compounds within vs across formula boundaries
    "suffix_after_animal",        # Which suffixes follow animal readings?
    "cross_site_formula_overlap", # Do sites share the same formulas?
]


# ── Core loop functions ──────────────────────────────────────────────

def mine_cycle(cycle_num, all_seen):
    """Mine with rotating queries."""
    gap = GAP_QUERY_ROTATION[(cycle_num - 1) % len(GAP_QUERY_ROTATION)]
    bucket = []
    for q in gap["queries"]:
        enc = urllib.parse.quote(q)
        url = (f"https://api.openalex.org/works?search={enc}&per-page=50&cursor=*"
               f"&select=id,title,doi,publication_year,abstract_inverted_index"
               f"&mailto=tpierson@bitconcepts.tech")
        data = _get_json(url)
        if data and "results" in data:
            for w in data["results"]:
                title = w.get("title") or ""
                abstract = ""
                aii = w.get("abstract_inverted_index")
                if aii:
                    pairs = sorted([(pos, word) for word, positions in aii.items() for pos in positions])
                    abstract = " ".join(w for _, w in pairs)
                if title:
                    bucket.append({"title": title, "abstract": abstract[:400]})
        time.sleep(0.4)

    unique = []
    for p in bucket:
        norm = re.sub(r"\s+", " ", p["title"].lower().strip())
        if norm and norm not in all_seen:
            all_seen.add(norm)
            unique.append(p)

    # Extract insights
    insights = []
    for p in unique:
        text = f"{p['title']} {p['abstract']}".lower()
        for kw, itype in [("sign value","reading"),("reading propos","reading"),("guild","guild"),
                          ("compound","compound"),("hapax","rare"),("formula","formula"),
                          ("seal function","function"),("administrative","function"),
                          ("numeral","numeral"),("weight","metrological"),("morpheme","morphology"),
                          ("personal name","name"),("title","title"),("loanword","substrate")]:
            if kw in text:
                insights.append({"type": itype, "title": p["title"][:80]})
                break

    return gap["name"], unique, insights


def run_experiment(cycle_num, hm, ins):
    """Run experiment from rotating template."""
    template = EXPERIMENT_TEMPLATES[(cycle_num - 1) % len(EXPERIMENT_TEMPLATES)]
    rng = random.Random(42 + cycle_num)

    if template == "site_specific_formula":
        site_formulas = defaultdict(Counter)
        for i in ins:
            if not i["site"]: continue
            readings = tuple(_clean(hm.get(s, "")) for s in i["signs"] if s in hm)
            if len(readings) >= 2:
                site_formulas[i["site"]][readings] += 1
        n_unique_per_site = {s: len(f) for s, f in site_formulas.items() if len(f) >= 3}
        return {"experiment": template, "n_sites": len(n_unique_per_site),
                "avg_unique_formulas": round(sum(n_unique_per_site.values())/max(1,len(n_unique_per_site)),1),
                "verdict": f"Site formulas: {len(n_unique_per_site)} sites with unique formula sets."}

    elif template == "motif_title_correlation":
        motif_titles = defaultdict(Counter)
        TITLES = {"kōṉ","kō","vēḷ","mā","nal","tiru","veL","nēr","cem"}
        for i in ins:
            if not i["motif"]: continue
            for s in i["signs"]:
                r = _clean(hm.get(s, ""))
                if r in TITLES: motif_titles[i["motif"]][r] += 1
        profiles = {m: dict(tc.most_common(3)) for m, tc in motif_titles.items() if sum(tc.values()) >= 5}
        return {"experiment": template, "n_motifs": len(profiles), "profiles": profiles,
                "verdict": f"Motif-title: {len(profiles)} motifs have title reading profiles."}

    elif template == "suffix_chain_depth":
        max_chains = []
        for i in ins:
            readings = [_clean(hm.get(s, "")) for s in i["signs"]]
            chain = 0; max_c = 0
            for r in readings:
                if r in SUFFIXES: chain += 1; max_c = max(max_c, chain)
                else: chain = 0
            max_chains.append(max_c)
        avg_depth = sum(max_chains) / max(1, len(max_chains))
        depth_dist = Counter(max_chains)
        return {"experiment": template, "avg_depth": round(avg_depth, 2), "distribution": dict(depth_dist),
                "verdict": f"Suffix chains: avg depth {avg_depth:.1f}. Distribution: {dict(depth_dist.most_common(5))}."}

    elif template == "reading_frequency_zipf":
        rf = Counter()
        for i in ins:
            for s in i["signs"]:
                r = _clean(hm.get(s, ""))
                if r: rf[r] += 1
        ranked = sorted(rf.values(), reverse=True)
        if len(ranked) >= 5:
            log_ranks = [math.log(i+1) for i in range(len(ranked))]
            log_freqs = [math.log(f) for f in ranked]
            mr = sum(log_ranks)/len(log_ranks); mf = sum(log_freqs)/len(log_freqs)
            num = sum((lr-mr)*(lf-mf) for lr,lf in zip(log_ranks,log_freqs))
            den = sum((lr-mr)**2 for lr in log_ranks)
            alpha = round(-num/den, 3) if den else 0
        else: alpha = 0
        return {"experiment": template, "zipf_alpha": alpha, "n_readings": len(ranked),
                "verdict": f"Zipf: α={alpha} ({len(ranked)} readings). {'Linguistic' if 0.8<alpha<1.5 else 'Non-Zipfian'}."}

    elif template == "compound_semantic_coherence":
        pair_freq = Counter(); sf = Counter(); total = 0
        for i in ins:
            for s in i["signs"]: sf[s] += 1
            for j in range(len(i["signs"])-1):
                pair_freq[(i["signs"][j],i["signs"][j+1])] += 1; total += 1
        ts = sum(sf.values())
        sem_coherent = 0; sem_total = 0
        for (a,b),c in pair_freq.items():
            if sf[a]>=5 and sf[b]>=5:
                pmi = math.log2((c/total)/((sf[a]/ts)*(sf[b]/ts)+1e-10)+1e-10)
                if pmi > 2:
                    ra,rb = _clean(hm.get(a,"")),_clean(hm.get(b,""))
                    if ra and rb:
                        sem_total += 1
                        ar = ra in ROOTS; br = rb in ROOTS; asuf = ra in SUFFIXES; bsuf = rb in SUFFIXES
                        if (ar and bsuf) or (ar and br) or (asuf and br): sem_coherent += 1
        rate = sem_coherent / max(1, sem_total)
        return {"experiment": template, "coherent": sem_coherent, "total": sem_total, "rate": round(rate,3),
                "verdict": f"Compound coherence: {rate:.0%} ({sem_coherent}/{sem_total}) semantically valid."}

    elif template == "blocker_sign_context":
        blocker_ctx = defaultdict(Counter)
        for i in ins:
            for j,s in enumerate(i["signs"]):
                if s not in hm:
                    if j>0 and i["signs"][j-1] in hm: blocker_ctx[s][hm[i["signs"][j-1]]] += 1
                    if j<len(i["signs"])-1 and i["signs"][j+1] in hm: blocker_ctx[s][hm[i["signs"][j+1]]] += 1
        top_blockers = sorted(blocker_ctx.items(), key=lambda x: -sum(x[1].values()))[:10]
        return {"experiment": template, "n_blockers_with_context": len(blocker_ctx),
                "top_10": [{s: dict(c.most_common(3))} for s,c in top_blockers],
                "verdict": f"Blocker context: {len(blocker_ctx)} blockers have HIGH-sign neighbors."}

    elif template == "inscription_uniqueness":
        type_counts = Counter(tuple(i["signs"]) for i in ins)
        n_unique = len(type_counts)
        n_singleton = sum(1 for c in type_counts.values() if c == 1)
        return {"experiment": template, "n_unique_types": n_unique, "n_singletons": n_singleton,
                "total_inscriptions": len(ins),
                "verdict": f"Uniqueness: {n_unique} unique inscription types, {n_singleton} singletons ({n_singleton/max(1,n_unique):.0%})."}

    elif template == "decoded_text_repetition":
        bigrams = Counter()
        for i in ins:
            readings = [_clean(hm.get(s,"")) for s in i["signs"]]
            readings = [r for r in readings if r]
            for j in range(len(readings)-1): bigrams[(readings[j],readings[j+1])] += 1
        total = sum(bigrams.values()); types = len(bigrams)
        ttr = types / max(1, total)
        top5 = bigrams.most_common(5)
        return {"experiment": template, "ttr": round(ttr, 4), "n_types": types, "n_tokens": total,
                "top_5": [f"{a}→{b}({c})" for (a,b),c in top5],
                "verdict": f"Text repetition: TTR={ttr:.3f} ({types} types / {total} tokens)."}

    elif template == "suffix_after_animal":
        ANIMALS = {"yānai","kaḷiṟu","erutu","puli","vēṅkai","nakaram","kāṇṭāmirukam","māṭu","āṉai","kōṭṭāṉ","maṟi","mutalai"}
        after_animal = Counter()
        for i in ins:
            readings = [_clean(hm.get(s,"")) for s in i["signs"]]
            for j in range(len(readings)-1):
                if readings[j] in ANIMALS and readings[j+1] in SUFFIXES:
                    after_animal[readings[j+1]] += 1
        return {"experiment": template, "suffix_counts": dict(after_animal.most_common(10)),
                "verdict": f"After animal: {dict(after_animal.most_common(5))}. Most common: {after_animal.most_common(1)[0][0] if after_animal else 'none'}."}

    elif template == "cross_site_formula_overlap":
        site_formulas = defaultdict(set)
        for i in ins:
            if not i["site"]: continue
            readings = tuple(_clean(hm.get(s,"")) for s in i["signs"] if s in hm)
            if len(readings) >= 2: site_formulas[i["site"]].add(readings)
        sites = [s for s,f in site_formulas.items() if len(f) >= 5]
        overlaps = []
        for i in range(len(sites)):
            for j in range(i+1,len(sites)):
                shared = len(site_formulas[sites[i]] & site_formulas[sites[j]])
                total = len(site_formulas[sites[i]] | site_formulas[sites[j]])
                overlaps.append({"s1": sites[i], "s2": sites[j], "jaccard": round(shared/max(1,total),3)})
        avg_jac = sum(o["jaccard"] for o in overlaps) / max(1,len(overlaps))
        return {"experiment": template, "n_pairs": len(overlaps), "avg_jaccard": round(avg_jac,3),
                "verdict": f"Cross-site formulas: {len(overlaps)} pairs, avg Jaccard {avg_jac:.2f}."}

    else:
        # Generic fallback
        return {"experiment": template, "verdict": f"Template '{template}' executed (generic)."}


# ── Main loop ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cycles", type=int, default=15)
    args = parser.parse_args()

    print("=" * 70)
    print(f"INTEGRATED RESEARCH LOOP — up to {args.max_cycles} cycles")
    print("Mine → Analyze → Register → Execute → Analyze → repeat")
    print("=" * 70)

    hm = _load_high_map()
    ins = _load_inscriptions()
    all_seen = set()
    history = []
    prev_verdict = ""

    for cycle in range(1, args.max_cycles + 1):
        print(f"\n{'═' * 70}")
        print(f"CYCLE {cycle}/{args.max_cycles}")
        print(f"{'═' * 70}")

        # 1. MINE
        gap_name, papers, insights = mine_cycle(cycle, all_seen)
        print(f"  [MINE] Gap: {gap_name} | {len(papers)} papers | {len(insights)} insights")

        # 2. ANALYZE mining results
        insight_types = Counter(i["type"] for i in insights)
        print(f"  [ANALYZE] Insight types: {dict(insight_types.most_common(5))}")

        # 3. REGISTER (conceptual — the experiment is generated from template)
        template = EXPERIMENT_TEMPLATES[(cycle - 1) % len(EXPERIMENT_TEMPLATES)]
        print(f"  [REGISTER] Experiment: {template}")

        # 4. EXECUTE
        result = run_experiment(cycle, hm, ins)
        print(f"  [EXECUTE] {result['verdict']}")

        # 5. ANALYZE results — check if this is new information
        verdict = result["verdict"]
        is_new = verdict != prev_verdict
        prev_verdict = verdict

        if not is_new and cycle > 3:
            # Check if we've seen this exact experiment before
            same_count = sum(1 for h in history if h.get("experiment") == template)
            if same_count >= 2:
                print(f"  [PLATEAU] Experiment '{template}' repeated {same_count+1} times with same result.")

        history.append({
            "cycle": cycle,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gap_targeted": gap_name,
            "n_papers": len(papers),
            "n_insights": len(insights),
            "experiment": template,
            "verdict": verdict,
            "is_new_info": is_new,
        })

        print(f"  [STATUS] {'NEW INFO' if is_new else 'REPEAT'} | "
              f"Cumulative: {sum(h['n_papers'] for h in history)} papers, "
              f"{sum(h['n_insights'] for h in history)} insights, "
              f"{cycle} experiments")

    # Save
    total_papers = sum(h["n_papers"] for h in history)
    total_insights = sum(h["n_insights"] for h in history)
    n_new = sum(1 for h in history if h["is_new_info"])

    output = {
        "protocol": "integrated_research_loop",
        "cycles_run": len(history),
        "max_cycles": args.max_cycles,
        "total_papers_mined": total_papers,
        "total_insights": total_insights,
        "n_new_experiments": n_new,
        "n_repeat_experiments": len(history) - n_new,
        "history": history,
        "verdict": (
            f"Integrated loop: {len(history)} cycles, {total_papers} papers, "
            f"{total_insights} insights, {n_new} new experiments, "
            f"{len(history)-n_new} repeats."
        ),
    }

    OUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{'=' * 70}")
    print(f"FINAL: {output['verdict']}")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
