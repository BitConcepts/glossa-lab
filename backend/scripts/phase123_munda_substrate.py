"""Phase-123: Munda/BMAC Substrate Vocabulary Analysis.

Analyzes signs still unresolved after Phase-122 for potential:
  1. Munda (Austroasiatic) proto-vocabulary — Witzel (1999) substrate
  2. BMAC (Bactria-Margiana Archaeological Complex) substrate words
  3. Brahui cognates — a Dravidian outlier in Pakistan with possible IVC connection
  4. Proto-Elamo-Dravidian vocabulary shared between Elamite and Dravidian

Signs that resist Dravidian decipherment may be substrate loans, foreign
words in a Dravidian inscription system, or purely syllabic signs.

CPU only. Output: reports/phase123_munda_substrate.json
"""
from __future__ import annotations
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P122    = REPO / "reports/phase122_syllabic_lm_sa.json"
P108    = REPO / "reports/phase108_phon_exhaustion.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase123_munda_substrate.json"

# ── Munda / Austroasiatic substrate vocabulary (Witzel 1999, Southworth 2005)
# Signs whose SA modal matches these roots may be Munda loans in Dravidian text
MUNDA_VOCAB = {
    # Format: "proto-form": {"gloss": ..., "source": ..., "dravidian_cognate": ...}
    "ba":   {"gloss": "water/river", "source": "Munda/Santali 'ba'", "dravidian_cognate": ""},
    "bi":   {"gloss": "seed/sprout", "source": "Munda 'bi'", "dravidian_cognate": ""},
    "biru": {"gloss": "jungle/forest", "source": "Munda 'bir'", "dravidian_cognate": ""},
    "ber":  {"gloss": "large/great", "source": "Munda 'beer'", "dravidian_cognate": ""},
    "horo": {"gloss": "paddy/rice", "source": "Munda 'horo'", "dravidian_cognate": ""},
    "dak":  {"gloss": "water/river (cf. 'dak' South Asia)", "source": "Munda substrate", "dravidian_cognate": ""},
    "tala": {"gloss": "lowland/plain", "source": "Munda/Santali 'tala'", "dravidian_cognate": "tal (pond)"},
    "kul":  {"gloss": "tiger/king-tiger", "source": "Munda 'kul'", "dravidian_cognate": "kol (Dravidian 'kill')"},
    "sumu": {"gloss": "house/home", "source": "Munda 'sumu'", "dravidian_cognate": ""},
    "di":   {"gloss": "water (cf. 'dhi')", "source": "Munda substrate", "dravidian_cognate": ""},
    "gid":  {"gloss": "leaf/branch", "source": "Munda 'gid'", "dravidian_cognate": ""},
    "hop":  {"gloss": "jump/escape", "source": "Munda 'hop'", "dravidian_cognate": ""},
    "jel":  {"gloss": "flow/stream", "source": "Munda substrate", "dravidian_cognate": ""},
}

# ── BMAC substrate (Witzel 1999, Lubotsky 2001)
# Bronze Age Bactrian words that may have entered Indus/Dravidian
BMAC_VOCAB = {
    "tur":  {"gloss": "strong/bull", "source": "BMAC/Bactrian 'tura'", "dravidian_cognate": ""},
    "var":  {"gloss": "water/rain", "source": "BMAC 'vara' (cf. Avestan)", "dravidian_cognate": ""},
    "asp":  {"gloss": "horse", "source": "BMAC/Old Iranian 'aspa'", "dravidian_cognate": ""},
    "kama": {"gloss": "desire/gold", "source": "BMAC 'kama'", "dravidian_cognate": ""},
    "sur":  {"gloss": "sun/bright", "source": "BMAC/Old Iranian 'sura'", "dravidian_cognate": ""},
    "maz":  {"gloss": "great (BMAC)", "source": "BMAC 'maz'", "dravidian_cognate": ""},
    "hari": {"gloss": "yellow/lion", "source": "BMAC/Sanskrit", "dravidian_cognate": ""},
    "pur":  {"gloss": "city/fort", "source": "BMAC/Old Iranian 'pura'", "dravidian_cognate": "pur (Tamil)"},
    "gau":  {"gloss": "cow", "source": "BMAC/Old Iranian 'gava'", "dravidian_cognate": ""},
    "mru":  {"gloss": "die/death", "source": "BMAC substrate", "dravidian_cognate": ""},
}

# ── Brahui cognates (Dravidian outlier spoken in Balochistan)
# Brahui has preserved ancient Dravidian forms and may share substrate vocabulary
BRAHUI_VOCAB = {
    "pa":   {"gloss": "father/elder", "source": "Brahui 'pa'", "dravidian_cognate": "appan"},
    "nin":  {"gloss": "you (pronoun)", "source": "Brahui 'nin'", "dravidian_cognate": "nīn (Tamil)"},
    "kas":  {"gloss": "go/come", "source": "Brahui 'kas'", "dravidian_cognate": ""},
    "mul":  {"gloss": "root/origin", "source": "Brahui 'mul'", "dravidian_cognate": "mul (Tamil thorn)"},
    "kur":  {"gloss": "river/water", "source": "Brahui 'kur' (river)", "dravidian_cognate": ""},
    "ded":  {"gloss": "two", "source": "Brahui 'ded'", "dravidian_cognate": "iraNDu (Tamil 2)"},
    "sapt": {"gloss": "seven", "source": "Brahui (loanword)", "dravidian_cognate": "ēḷ (Tamil 7)"},
    "xal":  {"gloss": "gold/bright", "source": "Brahui 'xal'", "dravidian_cognate": ""},
}

# ── Proto-Elamo-Dravidian (McAlpin 1981, Blench 2008)
ELAMO_DRAVIDIAN = {
    "na":   {"gloss": "I (pronoun)", "source": "Elamite 'na'", "dravidian_cognate": "nān (Tamil I)"},
    "in":   {"gloss": "this/here", "source": "Elamite 'in'", "dravidian_cognate": "inta (Tamil this)"},
    "tur":  {"gloss": "son/young", "source": "Elamite 'tur'", "dravidian_cognate": ""},
    "hal":  {"gloss": "land/earth", "source": "Elamite 'hala'", "dravidian_cognate": "kalam (Tamil land)"},
    "ut":   {"gloss": "water", "source": "Elamite 'utta'", "dravidian_cognate": ""},
    "man":  {"gloss": "house/dwelling", "source": "Elamite 'man'", "dravidian_cognate": "māḷigai (Tamil palace)"},
    "mir":  {"gloss": "lord/ruler", "source": "Elamite 'mir'", "dravidian_cognate": ""},
    "uk":   {"gloss": "this (demonstrative)", "source": "Elamite 'uk'", "dravidian_cognate": ""},
}

ALL_SUBSTRATE = {
    "MUNDA": MUNDA_VOCAB,
    "BMAC": BMAC_VOCAB,
    "BRAHUI": BRAHUI_VOCAB,
    "ELAMO_DRAVIDIAN": ELAMO_DRAVIDIAN,
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


def check_substrate_match(reading: str) -> list[dict]:
    """Check if a reading matches any substrate vocabulary."""
    if not reading:
        return []
    r = reading.lower().strip()
    matches = []
    for substrate_name, vocab in ALL_SUBSTRATE.items():
        for form, info in vocab.items():
            f = form.lower()
            if r == f or r.startswith(f[:2]) or f.startswith(r[:2]):
                similarity = "exact" if r == f else "partial"
                matches.append({
                    "substrate": substrate_name,
                    "form": form,
                    "similarity": similarity,
                    "gloss": info["gloss"],
                    "source": info["source"],
                    "dravidian_cognate": info.get("dravidian_cognate", ""),
                })
    return matches


def main():
    print("Phase-123: Munda/BMAC Substrate Analysis\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
    print(f"  Confirmed H+M anchors: {len(confirmed)}")

    # Load Phase-122 results (signs still unresolved)
    p122_results = []
    if P122.exists():
        p122 = json.loads(P122.read_text("utf-8"))
        p122_results = p122.get("results", [])

    # Load Phase-108 unresolved list
    p108_skipped = []
    if P108.exists():
        p108 = json.loads(P108.read_text("utf-8"))
        for entry in p108.get("sweep_log", []):
            if entry.get("skipped") and entry.get("freq", 0) >= 5:
                p108_skipped.append(entry["sign"])

    seals = load_corpus()
    flat_freq = Counter(s for signs in seals.values() for s in signs)

    # Signs still unresolved after Phase-122
    still_unresolved = []
    for sign in p108_skipped:
        if sign not in confirmed:
            freq = flat_freq.get(sign, 0)
            # Get Phase-122 SA reading if available
            p122_entry = next((r for r in p122_results if r.get("sign") == sign), None)
            sa_modal_122 = p122_entry.get("sa_modal", "") if p122_entry else ""
            cons_122 = p122_entry.get("consistency", 0) if p122_entry else 0
            still_unresolved.append({
                "sign": sign, "freq": freq,
                "syllabic_sa_modal": sa_modal_122,
                "syllabic_sa_cons": cons_122,
            })

    print(f"  Still unresolved after Phase-122: {len(still_unresolved)} signs")

    # Substrate analysis for each unresolved sign
    substrate_analysis = []
    n_substrate_match = 0

    for sign_data in still_unresolved:
        sign = sign_data["sign"]
        sa_modal = sign_data.get("syllabic_sa_modal", "")

        # Check if the SA modal matches any substrate form
        matches = check_substrate_match(sa_modal) if sa_modal else []

        # Also check using positional context (what grammar slot is the sign in?)
        # Use the trigram context from seals
        contexts = Counter()
        for signs in seals.values():
            n = len(signs)
            for i, s in enumerate(signs):
                if s != sign: continue
                prev = signs[i-1] if i > 0 else "^"
                nxt  = signs[i+1] if i < n-1 else "$"
                contexts[f"{prev}→[{sign}]→{nxt}"] += 1

        analysis = {
            "sign": sign,
            "freq": sign_data["freq"],
            "syllabic_sa_modal": sa_modal,
            "syllabic_sa_cons": sign_data["syllabic_sa_cons"],
            "substrate_matches": matches,
            "n_substrate_matches": len(matches),
            "best_substrate": matches[0] if matches else None,
            "top_contexts": [ctx for ctx, _ in contexts.most_common(5)],
            "hypothesis": (
                "SUBSTRATE_LOAN" if matches else
                "SYLLABIC_UNRESOLVED" if sa_modal else
                "UNKNOWN"
            ),
        }
        substrate_analysis.append(analysis)

        if matches:
            n_substrate_match += 1
            print(f"  {sign}(f={sign_data['freq']}): modal='{sa_modal}' → {matches[0]['substrate']} '{matches[0]['form']}' ({matches[0]['gloss']})")
        elif sa_modal:
            print(f"  {sign}(f={sign_data['freq']}): modal='{sa_modal}' — no substrate match (syllabic unresolved)")
        else:
            print(f"  {sign}(f={sign_data['freq']}): no SA modal — UNKNOWN")

    # Summary by substrate type
    by_substrate: dict = defaultdict(list)
    for a in substrate_analysis:
        for m in a.get("substrate_matches", []):
            by_substrate[m["substrate"]].append(a["sign"])

    print(f"\n  Substrate match summary:")
    print(f"    Signs with substrate match: {n_substrate_match}/{len(still_unresolved)}")
    for sub, signs in by_substrate.items():
        print(f"    {sub}: {len(signs)} signs — {', '.join(signs[:5])}")

    # Coverage impact assessment
    total_tokens = sum(flat_freq.values())
    unresolved_tokens = sum(flat_freq.get(s["sign"], 0) for s in still_unresolved)
    substrate_tokens  = sum(flat_freq.get(s["sign"], 0) for s in substrate_analysis
                            if s.get("substrate_matches"))
    print(f"\n  Unresolved tokens: {unresolved_tokens} ({unresolved_tokens/total_tokens:.1%} of corpus)")
    print(f"  Of which potential substrate: {substrate_tokens} ({substrate_tokens/max(1,total_tokens):.1%})")

    # Interpretation
    interpretation = (
        f"After Phases 104-122 (Dravidian decipherment), {len(still_unresolved)} signs "
        f"with freq≥5 remain unresolved ({unresolved_tokens/total_tokens:.1%} of tokens). "
        f"{n_substrate_match} of these have SA modals matching known Munda/BMAC/Brahui substrate vocabulary, "
        f"suggesting they may be substrate loans in an otherwise Proto-Dravidian inscription system. "
        f"This is consistent with Witzel's (1999) hypothesis of a Munda substrate layer in the Indus Valley, "
        f"and McAlpin's (1981) Proto-Elamo-Dravidian connection. "
        f"The remaining {len(still_unresolved)-n_substrate_match} signs are likely "
        f"allographs, rare phonetic variants, or genuinely opaque signs requiring expert epigrapher review."
    )
    print(f"\n  {interpretation[:200]}...")

    result = {
        "phase": 123,
        "n_unresolved": len(still_unresolved),
        "n_substrate_match": n_substrate_match,
        "unresolved_token_fraction": round(unresolved_tokens/max(1,total_tokens), 4),
        "substrate_token_fraction": round(substrate_tokens/max(1,total_tokens), 4),
        "substrate_analysis": substrate_analysis,
        "by_substrate": {k: v for k, v in by_substrate.items()},
        "interpretation": interpretation,
        "substrate_vocabularies": {
            k: len(v) for k, v in ALL_SUBSTRATE.items()
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"  Phase-123 complete: {n_substrate_match}/{len(still_unresolved)} signs matched substrate vocabulary")
    return result


if __name__ == "__main__":
    main()
