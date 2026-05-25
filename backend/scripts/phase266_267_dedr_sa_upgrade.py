"""Phase 266-267: Expanded DEDR LM SA + Batch MEDIUM→HIGH Upgrades

Phase-264 showed the expanded DEDR LM (55K vocab) boosts SA from 56%→74%.
This phase runs a full SA with that LM + 139 HIGH anchors pinned, then
applies consistency-based upgrades to MEDIUM signs.

Upgrade criteria (conservative):
  - Expanded-LM SA consistency >= 0.40
  - Sign has DEDR entry
  - SA modal reading matches current anchor reading (or is phonotactically compatible)

Output: outputs/phase266_267_dedr_sa_upgrade.json
"""
from __future__ import annotations

import csv, json, os, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase266_267_dedr_sa_upgrade.json"
ANCHORS_F = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
DEDR_CSV = REPO / "backend" / "glossa_lab" / "data" / "phase16_corpora" / "dedr_cognates.csv"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))

N_SEEDS = 8
MAX_ITER = 10_000
RESTARTS = 5


def extract_dedr_words(max_unique: int = 5000) -> list[str]:
    """Extract Tamil words from DEDR, capped to prevent BigramScorer OOM."""
    raw: list[str] = []
    with open(DEDR_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            text = row.get("raw_text", "")
            for m in re.finditer(r'\b([a-z]{2,12})\b', text):
                raw.append(m.group(1).lower())
    # Keep only the most frequent words to cap LM size
    freq = Counter(raw)
    top = {w for w, _ in freq.most_common(max_unique)}
    return [w for w in raw if w in top]


def build_anchor_dict(anchors_raw, freq, min_conf="HIGH"):
    tier = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "CANDIDATE": 0}
    thr = tier.get(min_conf, 0)
    out = {}
    for aid, rec in anchors_raw.items():
        if not isinstance(rec, dict): continue
        if tier.get(rec.get("confidence", ""), 0) < thr: continue
        m77 = aid.lstrip("M")
        reading = rec.get("reading", "").split("/")[0].strip()
        if m77 in freq and reading:
            out[m77] = reading
    return out


def main():
    t0 = time.time()
    print("=" * 70)
    print("PHASE 266-267: EXPANDED DEDR LM SA + MEDIUM→HIGH BATCH UPGRADE")
    print("=" * 70)

    from glossa_lab.data.dravidian import get_word_symbols
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    from glossa_lab.pipelines.decipher import LanguageModel, decipher

    # Build expanded LM
    base_words = get_word_symbols()
    dedr_words = extract_dedr_words()
    expanded = base_words + dedr_words
    lm = LanguageModel(expanded)
    print(f"\n  Expanded LM: {lm.size} unique symbols")

    # Load corpus + anchors
    syms = get_corpus_symbols()
    inscs = get_corpus_inscriptions()
    freq = Counter(syms)
    flat = [s for seq in inscs for s in seq]

    anchors_raw = json.loads(ANCHORS_F.read_text("utf-8"))["anchors"]
    anch_high = build_anchor_dict(anchors_raw, freq, "HIGH")
    print(f"  M77: {len(freq)} distinct, {len(flat)} tokens")
    print(f"  HIGH anchors pinned: {len(anch_high)}")
    print(f"  SA: {MAX_ITER} iter × {RESTARTS} restarts × {N_SEEDS} seeds")

    # ── Phase 266: Run SA ───────────────────────────────────────────────────
    print("\n=== PHASE-266: SA RUN (EXPANDED DEDR LM) ===")

    def _one(seed):
        r = decipher(flat, lm, seed=seed, max_iterations=MAX_ITER, restarts=RESTARTS,
                     cipher_inscriptions=None, ocp_weight=0.0,
                     positional_weight=0.0, surjective=True,
                     anchors=anch_high or None)
        return r.get("proposed_mapping", {})

    with ThreadPoolExecutor(max_workers=min(N_SEEDS, 10)) as ex:
        maps = list(ex.map(_one, range(N_SEEDS)))

    all_signs = set().union(*[m.keys() for m in maps])
    modal, conss = {}, {}
    for s in all_signs:
        props = [m[s] for m in maps if s in m]
        if props:
            c = Counter(props); val, cnt = c.most_common(1)[0]
            modal[s] = val; conss[s] = cnt / len(props)

    mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
    hci = sum(1 for v in conss.values() if v >= 0.75)
    hci40 = sum(1 for v in conss.values() if v >= 0.40)
    print(f"  Mean consistency: {mean_c:.4f} ({mean_c*100:.1f}%)")
    print(f"  HCI (cons>=0.75): {hci}")
    print(f"  Signs with cons>=0.40: {hci40}")

    # ── Phase 267: Apply upgrades ───────────────────────────────────────────
    print("\n=== PHASE-267: MEDIUM→HIGH UPGRADES ===")

    medium_signs = {k: v for k, v in anchors_raw.items() if v.get("confidence") == "MEDIUM"}
    n_upgraded = 0
    upgrade_log = []

    for sign, info in medium_signs.items():
        m77 = sign.lstrip("M")
        cons = conss.get(m77, 0)
        sa_modal = modal.get(m77, "")
        current_reading = info.get("reading", "").split("/")[0].strip()
        has_dedr = bool(info.get("dedr", ""))

        if cons < 0.40:
            continue
        if not has_dedr:
            continue

        # Check reading agreement (exact or prefix match)
        agrees = False
        if sa_modal and current_reading:
            agrees = (sa_modal.lower() == current_reading.lower() or
                      sa_modal.lower().startswith(current_reading.lower()[:3]) or
                      current_reading.lower().startswith(sa_modal.lower()[:3]))

        if not agrees:
            continue  # Require reading agreement for safety

        anchors_raw[sign]["confidence"] = "HIGH"
        anchors_raw[sign]["phase_upgraded"] = 267
        basis = anchors_raw[sign].get("basis", "")
        anchors_raw[sign]["basis"] = (
            f"{basis}; Phase-267: expanded DEDR LM SA upgrade — "
            f"cons={cons:.2f}, modal='{sa_modal}', agrees with anchor reading"
        )
        n_upgraded += 1
        upgrade_log.append({
            "sign": sign, "reading": current_reading, "sa_modal": sa_modal,
            "sa_cons": round(cons, 3), "freq": freq.get(m77, 0),
        })

    print(f"  Upgraded: {n_upgraded} MEDIUM→HIGH")
    for ul in upgrade_log[:15]:
        print(f"    {ul['sign']}='{ul['reading']}' cons={ul['sa_cons']:.2f} sa='{ul['sa_modal']}'")

    if n_upgraded > 0:
        data = json.loads(ANCHORS_F.read_text("utf-8"))
        data["anchors"] = anchors_raw
        ANCHORS_F.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    by_conf = Counter(v.get("confidence", "?") for v in anchors_raw.values())
    elapsed = round(time.time() - t0, 1)

    print(f"\n  Final: H:{by_conf.get('HIGH',0)} M:{by_conf.get('MEDIUM',0)} → "
          f"H+M={by_conf.get('HIGH',0)+by_conf.get('MEDIUM',0)}/413")
    print(f"  Elapsed: {elapsed}s")

    result = {
        "phase": "266_267", "elapsed_s": elapsed,
        "sa_params": {"max_iter": MAX_ITER, "restarts": RESTARTS, "n_seeds": N_SEEDS},
        "lm_vocab": lm.size, "n_high_pinned": len(anch_high),
        "mean_consistency": mean_c, "hci_75": hci, "hci_40": hci40,
        "n_upgraded": n_upgraded, "upgrade_log": upgrade_log[:50],
        "final_state": {"HIGH": by_conf.get("HIGH", 0), "MEDIUM": by_conf.get("MEDIUM", 0),
                        "total": len(anchors_raw)},
    }
    OUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\n{'='*70}")
    print(f"PHASE 266-267 COMPLETE: {n_upgraded} upgrades | SA {mean_c:.1%} | H:{by_conf.get('HIGH',0)}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
