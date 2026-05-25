"""Phase 281-283: Yajnadevam Corpus Integration + SA + Sanskrit Falsification

Phase-281: Build Yajnadevam→Mahadevan crosswalk and load lipi inscriptions.csv
           (5,679 inscriptions, 77 sites, 18,735 tokens, 1,118 signs)
Phase-282: Run SA on expanded corpus with expanded DEDR LM + HIGH anchors
Phase-283: Compare Yajnadevam Sanskrit readings vs our PDr readings

Output: outputs/phase281_283_yajnadevam.json
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase281_283_yajnadevam.json"
ANCHORS_F = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
LIPI_CSV = Path(r"C:\Users\trist\Downloads\lipi-main\lipi-main\src\assets\data\inscriptions.csv")
GLOSSING_CSV = Path(r"C:\Users\trist\Downloads\lipi-main\lipi-main\glossing.csv")
DEDR_CSV = REPO / "backend" / "glossa_lab" / "data" / "phase16_corpora" / "dedr_cognates.csv"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))


def load_lipi_corpus():
    """Load and parse the Yajnadevam lipi inscriptions.csv."""
    rows = list(csv.DictReader(open(LIPI_CSV, encoding="utf-8")))
    inscriptions = []
    for r in rows:
        text = r.get("text", "").strip().strip("+")
        if not text:
            continue
        # Signs separated by - ; filter out brackets and 000 (unreadable)
        signs = []
        for s in text.split("-"):
            s = s.strip().rstrip("[").lstrip("]")
            if s and s != "000" and not s.startswith("[") and not s.startswith("/"):
                signs.append(s)
        if signs:
            inscriptions.append({
                "signs": signs,
                "site": r.get("site", ""),
                "id": r.get("id", ""),
                "sanskrit": r.get("sanskrit", ""),
                "translation": r.get("translation", ""),
            })
    return inscriptions


def build_crosswalk(lipi_signs, m77_signs):
    """Build crosswalk: Yajnadevam sign IDs that overlap with M77 numeric codes."""
    # Yajnadevam uses 3-digit codes similar to Mahadevan. Many are identical.
    # M77 signs are 3-digit zero-padded (e.g. "047", "342")
    crosswalk = {}
    for ys in lipi_signs:
        # Direct numeric match
        if ys in m77_signs:
            crosswalk[ys] = f"M{ys}"
    return crosswalk


def extract_dedr_words(max_unique=5000):
    """Extract Tamil words from DEDR for expanded LM."""
    raw = []
    with open(DEDR_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            text = row.get("raw_text", "")
            for m in re.finditer(r"\b([a-z]{2,12})\b", text):
                raw.append(m.group(1).lower())
    freq = Counter(raw)
    top = {w for w, _ in freq.most_common(max_unique)}
    return [w for w in raw if w in top]


def main():
    t0 = time.time()
    print("=" * 70)
    print("PHASE 281-283: YAJNADEVAM CORPUS + SA + SANSKRIT FALSIFICATION")
    print("=" * 70)

    # ── Phase 281: Load corpus + build crosswalk ────────────────────────────
    print("\n=== PHASE-281: LOAD YAJNADEVAM CORPUS ===")

    inscs = load_lipi_corpus()
    print(f"  Inscriptions loaded: {len(inscs)}")

    all_signs = [s for i in inscs for s in i["signs"]]
    sign_freq = Counter(all_signs)
    print(f"  Total tokens: {len(all_signs)}")
    print(f"  Distinct signs: {len(sign_freq)}")

    sites = Counter(i["site"] for i in inscs)
    print(f"  Sites: {len(sites)}")
    print(f"  Top 5: {sites.most_common(5)}")

    # Load our M77 sign list
    from glossa_lab.data.indus_m77 import get_corpus_symbols
    m77_syms = get_corpus_symbols()
    m77_signs = set(m77_syms)
    print(f"  M77 distinct signs: {len(m77_signs)}")

    # Build crosswalk
    lipi_sign_set = set(sign_freq.keys())
    crosswalk = build_crosswalk(lipi_sign_set, m77_signs)
    print(f"  Direct crosswalk matches: {len(crosswalk)}")
    print(f"  Crosswalk coverage: {sum(sign_freq[s] for s in crosswalk) / len(all_signs):.1%} of tokens")

    # Map inscriptions to M77 codes where possible
    mapped_inscs = []
    for insc in inscs:
        mapped = [crosswalk.get(s) for s in insc["signs"] if s in crosswalk]
        if len(mapped) >= 2:  # Need at least 2 mapped signs for SA
            mapped_inscs.append([m.lstrip("M") for m in mapped])  # M77 uses bare numbers

    print(f"  Inscriptions with 2+ mapped signs: {len(mapped_inscs)}")
    mapped_flat = [s for seq in mapped_inscs for s in seq]
    print(f"  Mapped tokens: {len(mapped_flat)}")

    # ── Phase 282: SA on expanded corpus ────────────────────────────────────
    print("\n=== PHASE-282: SA ON EXPANDED CORPUS ===")

    from glossa_lab.data.dravidian import get_word_symbols
    from glossa_lab.pipelines.decipher import LanguageModel, decipher

    base_words = get_word_symbols()
    dedr_words = extract_dedr_words()
    lm = LanguageModel(base_words + dedr_words)
    print(f"  LM vocab: {lm.size}")

    # Build anchor dict from HIGH signs that appear in mapped corpus
    anchors_raw = json.loads(ANCHORS_F.read_text("utf-8"))["anchors"]
    mapped_freq = Counter(mapped_flat)
    anch = {}
    for aid, rec in anchors_raw.items():
        if rec.get("confidence") != "HIGH":
            continue
        m77 = aid.lstrip("M")
        reading = rec.get("reading", "").split("/")[0].strip()
        if m77 in mapped_freq and reading:
            anch[m77] = reading
    print(f"  HIGH anchors in expanded corpus: {len(anch)}")

    if len(mapped_flat) >= 100 and len(anch) >= 5:
        N_SEEDS = 8
        MAX_ITER = 10_000
        RESTARTS = 5

        def _one(seed):
            r = decipher(
                mapped_flat, lm, seed=seed, max_iterations=MAX_ITER,
                restarts=RESTARTS, cipher_inscriptions=None,
                ocp_weight=0.0, positional_weight=0.0,
                surjective=True, anchors=anch or None,
            )
            return r.get("proposed_mapping", {})

        print(f"  Running SA: {MAX_ITER} iter × {RESTARTS} restarts × {N_SEEDS} seeds...")
        with ThreadPoolExecutor(max_workers=min(N_SEEDS, 8)) as ex:
            maps = list(ex.map(_one, range(N_SEEDS)))

        all_sa_signs = set().union(*[m.keys() for m in maps])
        modal, conss = {}, {}
        for s in all_sa_signs:
            props = [m[s] for m in maps if s in m]
            if props:
                c = Counter(props)
                val, cnt = c.most_common(1)[0]
                modal[s] = val
                conss[s] = cnt / len(props)

        mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
        hci = sum(1 for v in conss.values() if v >= 0.75)
        print(f"  SA mean consistency: {mean_c:.4f} ({mean_c * 100:.1f}%)")
        print(f"  HCI (≥0.75): {hci}")
        print(f"  Signs with cons≥0.40: {sum(1 for v in conss.values() if v >= 0.40)}")
    else:
        print(f"  Insufficient mapped data for SA ({len(mapped_flat)} tokens, {len(anch)} anchors)")
        mean_c = 0
        hci = 0
        conss = {}
        modal = {}

    # ── Phase 283: Sanskrit vs Dravidian falsification ──────────────────────
    print("\n=== PHASE-283: SANSKRIT VS DRAVIDIAN FALSIFICATION ===")

    # Load Yajnadevam's Sanskrit readings from inscriptions.csv
    sanskrit_readings = {}
    for insc in inscs:
        skt = (insc.get("sanskrit") or "").strip()
        if skt and not skt.startswith("ref:"):
            for sign in insc["signs"]:
                if sign in crosswalk:
                    m_key = crosswalk[sign]
                    if m_key not in sanskrit_readings:
                        sanskrit_readings[m_key] = skt

    print(f"  Sanskrit readings available: {len(sanskrit_readings)}")

    # Compare against our PDr readings
    agreements = 0
    conflicts = 0
    comparison = []
    for m_key, skt_reading in sorted(sanskrit_readings.items()):
        our_reading = anchors_raw.get(m_key, {}).get("reading", "")
        if not our_reading:
            continue
        # Check if readings are compatible (any overlap in first 3 chars)
        our_low = our_reading.lower().split("/")[0][:4]
        skt_low = skt_reading.lower()[:4]
        agrees = our_low in skt_low or skt_low in our_low
        if agrees:
            agreements += 1
        else:
            conflicts += 1
        comparison.append({
            "sign": m_key,
            "our_pdr": our_reading,
            "yajnadevam_skt": skt_reading,
            "agrees": agrees,
        })

    total_compared = agreements + conflicts
    print(f"  Compared: {total_compared} signs")
    print(f"  Agreements: {agreements} ({agreements / max(total_compared, 1):.0%})")
    print(f"  Conflicts: {conflicts} ({conflicts / max(total_compared, 1):.0%})")

    if comparison:
        print("\n  Sample comparisons:")
        for c in comparison[:10]:
            tag = "✓" if c["agrees"] else "✗"
            print(f"    {tag} {c['sign']}: PDr='{c['our_pdr']}' vs Skt='{c['yajnadevam_skt']}'")

    # Also load glossing.csv if available
    glossing_data = []
    if GLOSSING_CSV.exists():
        glossing_data = list(csv.DictReader(open(GLOSSING_CSV, encoding="utf-8")))
        print(f"\n  Glossing.csv entries: {len(glossing_data)}")
        if glossing_data:
            cols = list(glossing_data[0].keys())
            print(f"  Columns: {cols[:8]}")

    elapsed = round(time.time() - t0, 1)

    # ── Save ────────────────────────────────────────────────────────────────
    by_conf = Counter(v.get("confidence", "?") for v in anchors_raw.values())

    result = {
        "phase": "281_283",
        "elapsed_s": elapsed,
        "phase281": {
            "inscriptions": len(inscs),
            "tokens": len(all_signs),
            "distinct_signs": len(sign_freq),
            "sites": len(sites),
            "crosswalk_matches": len(crosswalk),
            "crosswalk_token_coverage": round(
                sum(sign_freq[s] for s in crosswalk) / max(len(all_signs), 1), 4
            ),
            "mapped_inscriptions": len(mapped_inscs),
            "mapped_tokens": len(mapped_flat),
        },
        "phase282": {
            "sa_mean_consistency": mean_c,
            "sa_hci_75": hci,
            "sa_signs_040": sum(1 for v in conss.values() if v >= 0.40),
            "n_anchors_mapped": len(anch),
        },
        "phase283": {
            "sanskrit_readings_found": len(sanskrit_readings),
            "compared": total_compared,
            "agreements": agreements,
            "conflicts": conflicts,
            "agreement_rate": round(agreements / max(total_compared, 1), 4),
            "sample_comparisons": comparison[:20],
            "glossing_entries": len(glossing_data),
        },
        "final_state": {
            "HIGH": by_conf.get("HIGH", 0),
            "MEDIUM": by_conf.get("MEDIUM", 0),
            "total": len(anchors_raw),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Output: {OUT}")
    print(f"  Elapsed: {elapsed}s")
    print(f"\n{'=' * 70}")
    print(f"PHASE 281-283 COMPLETE | SA: {mean_c:.1%} | Skt agree: {agreements}/{total_compared}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
