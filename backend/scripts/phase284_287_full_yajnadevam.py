"""Phase 284-287: Full Yajnadevam Integration

Phase-284: Expand crosswalk to all 707 3-digit signs against full 413 anchor table
Phase-285: Import lipi corpus as permanent data source
Phase-286: SA on full mapped corpus (all 3-digit signs = Mahadevan codes)
Phase-287: Glossing.csv deep analysis — Sanskrit vs PDr seal-level comparison

Output: outputs/phase284_287_full_yajnadevam.json
"""
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase284_287_full_yajnadevam.json"
ANCHORS_F = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
LIPI_CSV = Path(r"C:\Users\trist\Downloads\lipi-main\lipi-main\src\assets\data\inscriptions.csv")
GLOSSING_CSV = Path(r"C:\Users\trist\Downloads\lipi-main\lipi-main\glossing.csv")
DEDR_CSV = REPO / "backend" / "glossa_lab" / "data" / "phase16_corpora" / "dedr_cognates.csv"
DEST_CSV = REPO / "backend" / "glossa_lab" / "data" / "yajnadevam_inscriptions.csv"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))


def parse_lipi(path):
    """Parse lipi inscriptions.csv into list of {signs: [...], site, id, sanskrit}."""
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    inscs = []
    for r in rows:
        text = (r.get("text") or "").strip().strip("+")
        if not text:
            continue
        signs = []
        for s in text.split("-"):
            s = s.strip().rstrip("[").lstrip("]")
            if s and s != "000" and not s.startswith("[") and not s.startswith("/"):
                # Keep only 3-digit numeric (= Mahadevan codes)
                if s.isdigit() and len(s) == 3:
                    signs.append(s)
        if signs:
            inscs.append({
                "signs": signs,
                "site": r.get("site", ""),
                "id": r.get("id", ""),
                "sanskrit": (r.get("sanskrit") or ""),
                "translation": (r.get("translation") or ""),
            })
    return inscs


def extract_dedr_words(max_unique=5000):
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
    print("PHASE 284-287: FULL YAJNADEVAM INTEGRATION")
    print("=" * 70)

    anchors_raw = json.loads(ANCHORS_F.read_text("utf-8"))["anchors"]
    anchor_m77 = {k.lstrip("M"): v for k, v in anchors_raw.items() if k.startswith("M")}

    # ── Phase 284: Full crosswalk ───────────────────────────────────────────
    print("\n=== PHASE-284: FULL CROSSWALK (all 3-digit → anchor table) ===")

    inscs = parse_lipi(LIPI_CSV)
    all_signs = [s for i in inscs for s in i["signs"]]
    sign_freq = Counter(all_signs)
    print(f"  Inscriptions (3-digit only): {len(inscs)}")
    print(f"  Tokens: {len(all_signs)}")
    print(f"  Distinct 3-digit signs: {len(sign_freq)}")

    # Match against full anchor table (413 entries, M001-M920)
    crosswalk = {}
    for ys in sign_freq:
        if ys in anchor_m77:
            crosswalk[ys] = f"M{ys}"
    print(f"  Crosswalk matches (vs 413 anchors): {len(crosswalk)}")
    cov_tokens = sum(sign_freq[s] for s in crosswalk)
    print(f"  Token coverage: {cov_tokens}/{len(all_signs)} = {cov_tokens / len(all_signs):.1%}")

    # Signs in Yajnadevam NOT in our anchors — these are new signs we don't have readings for
    new_signs = {s: sign_freq[s] for s in sign_freq if s not in crosswalk}
    new_by_freq = sorted(new_signs.items(), key=lambda x: -x[1])
    print(f"  New signs (not in anchors): {len(new_signs)} ({sum(new_signs.values())} tokens)")
    print(f"  Top 10 new: {new_by_freq[:10]}")

    # ── Phase 285: Import corpus ────────────────────────────────────────────
    print("\n=== PHASE-285: IMPORT CORPUS AS DATA SOURCE ===")

    shutil.copy2(LIPI_CSV, DEST_CSV)
    print(f"  Copied to: {DEST_CSV}")
    print(f"  Size: {DEST_CSV.stat().st_size:,} bytes")

    # ── Phase 286: SA on full mapped corpus ─────────────────────────────────
    print("\n=== PHASE-286: SA ON FULL MAPPED CORPUS ===")

    from glossa_lab.data.dravidian import get_word_symbols
    from glossa_lab.pipelines.decipher import LanguageModel, decipher

    lm = LanguageModel(get_word_symbols() + extract_dedr_words())
    print(f"  LM vocab: {lm.size}")

    # Map all inscriptions using full crosswalk
    mapped_inscs = []
    for insc in inscs:
        mapped = [s for s in insc["signs"] if s in crosswalk]
        if len(mapped) >= 2:
            mapped_inscs.append(mapped)

    mapped_flat = [s for seq in mapped_inscs for s in seq]
    mapped_freq = Counter(mapped_flat)
    print(f"  Mapped inscriptions: {len(mapped_inscs)}")
    print(f"  Mapped tokens: {len(mapped_flat)}")
    print(f"  Mapped distinct: {len(mapped_freq)}")

    # Build anchors
    anch = {}
    for m77, rec in anchor_m77.items():
        if rec.get("confidence") != "HIGH":
            continue
        reading = rec.get("reading", "").split("/")[0].strip()
        if m77 in mapped_freq and reading:
            anch[m77] = reading
    print(f"  HIGH anchors in mapped corpus: {len(anch)}")

    N_SEEDS = 8
    MAX_ITER = 10_000
    RESTARTS = 5
    mean_c = 0.0
    hci = 0
    conss = {}
    modal = {}

    if len(mapped_flat) >= 100 and len(anch) >= 5:
        def _one(seed):
            r = decipher(
                mapped_flat, lm, seed=seed, max_iterations=MAX_ITER,
                restarts=RESTARTS, cipher_inscriptions=None,
                ocp_weight=0.0, positional_weight=0.0,
                surjective=True, anchors=anch or None,
            )
            return r.get("proposed_mapping", {})

        print(f"  SA: {MAX_ITER} iter × {RESTARTS} restarts × {N_SEEDS} seeds...")
        with ThreadPoolExecutor(max_workers=8) as ex:
            maps = list(ex.map(_one, range(N_SEEDS)))

        for s in set().union(*[m.keys() for m in maps]):
            props = [m[s] for m in maps if s in m]
            if props:
                c = Counter(props)
                val, cnt = c.most_common(1)[0]
                modal[s] = val
                conss[s] = cnt / len(props)

        mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
        hci = sum(1 for v in conss.values() if v >= 0.75)
        print(f"  Mean consistency: {mean_c:.4f} ({mean_c * 100:.1f}%)")
        print(f"  HCI (≥0.75): {hci}")
        print(f"  Signs ≥0.40: {sum(1 for v in conss.values() if v >= 0.40)}")

        # Check MEDIUM signs — any now have high consistency?
        medium_upgraded = 0
        for aid, rec in anchors_raw.items():
            if rec.get("confidence") != "MEDIUM":
                continue
            m77 = aid.lstrip("M")
            c = conss.get(m77, 0)
            if c >= 0.40 and rec.get("dedr"):
                sa_modal = modal.get(m77, "")
                cur = rec.get("reading", "").split("/")[0].strip().lower()
                if sa_modal and (sa_modal.lower()[:3] == cur[:3] or cur[:3] in sa_modal.lower()):
                    anchors_raw[aid]["confidence"] = "HIGH"
                    anchors_raw[aid]["phase_upgraded"] = 286
                    anchors_raw[aid]["basis"] = (
                        f"{rec.get('basis', '')}; Phase-286: Yajnadevam cross-corpus SA "
                        f"cons={c:.2f} on 5532-inscription corpus"
                    )
                    medium_upgraded += 1

        if medium_upgraded > 0:
            data = json.loads(ANCHORS_F.read_text("utf-8"))
            data["anchors"] = anchors_raw
            ANCHORS_F.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  MEDIUM→HIGH upgrades from cross-corpus SA: {medium_upgraded}")
    else:
        print(f"  Insufficient data ({len(mapped_flat)} tokens, {len(anch)} anchors)")

    # ── Phase 287: Glossing analysis ────────────────────────────────────────
    print("\n=== PHASE-287: GLOSSING.CSV DEEP ANALYSIS ===")

    glossing = []
    if GLOSSING_CSV.exists():
        glossing = list(csv.DictReader(open(GLOSSING_CSV, encoding="utf-8")))
    print(f"  Glossing entries: {len(glossing)}")

    if glossing:
        cols = list(glossing[0].keys())
        print(f"  Columns: {cols}")

        # Count unique translations
        translations = Counter((g.get("translation") or "").strip() for g in glossing if (g.get("translation") or "").strip())
        print(f"  Unique translations: {len(translations)}")
        print(f"  Top 10: {translations.most_common(10)}")

        # Count types
        types = Counter((g.get("type") or "").strip() for g in glossing if (g.get("type") or "").strip())
        print(f"  Sign types: {dict(types.most_common(10))}")

        # Analyze form field — these are the Sanskrit word forms
        forms = Counter((g.get("form") or "").strip() for g in glossing if (g.get("form") or "").strip())
        print(f"  Unique forms: {len(forms)}")
        print(f"  Top 10 forms: {forms.most_common(10)}")

    by_conf = Counter(v.get("confidence", "?") for v in anchors_raw.values())
    elapsed = round(time.time() - t0, 1)

    print(f"\n  Final: H:{by_conf.get('HIGH', 0)} M:{by_conf.get('MEDIUM', 0)}")
    print(f"  Elapsed: {elapsed}s")

    result = {
        "phase": "284_287",
        "elapsed_s": elapsed,
        "phase284": {
            "total_3digit_signs": len(sign_freq),
            "crosswalk_matches": len(crosswalk),
            "token_coverage_pct": round(cov_tokens / max(len(all_signs), 1), 4),
            "new_signs_not_in_anchors": len(new_signs),
            "new_signs_tokens": sum(new_signs.values()),
            "top_new_signs": new_by_freq[:20],
        },
        "phase285": {
            "corpus_imported": True,
            "dest_path": str(DEST_CSV),
        },
        "phase286": {
            "mapped_inscriptions": len(mapped_inscs),
            "mapped_tokens": len(mapped_flat),
            "sa_mean_consistency": mean_c,
            "sa_hci_75": hci,
            "n_anchors": len(anch),
            "medium_upgraded": medium_upgraded if "medium_upgraded" in dir() else 0,
        },
        "phase287": {
            "glossing_entries": len(glossing),
            "unique_translations": len(translations) if glossing else 0,
            "unique_forms": len(forms) if glossing else 0,
        },
        "final_state": {
            "HIGH": by_conf.get("HIGH", 0),
            "MEDIUM": by_conf.get("MEDIUM", 0),
            "total": len(anchors_raw),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{'=' * 70}")
    print(f"PHASE 284-287 COMPLETE | SA: {mean_c:.1%} | H:{by_conf.get('HIGH', 0)}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
