"""Phase-44 infrastructure fixes.

1. Fix INDUS_FINAL_ANCHORS: remove V8-V24 nīr placeholder noise
2. Rebuild indus_cisi_corpus.json from mayig_cisi_json repo
3. Build Gulf seal corpus from laursen_2010_table1.json + contact_zone data
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

BKRPT = REPO / "backend" / "reports"
DATA = REPO / "backend" / "glossa_lab" / "data"
CISI_SRC = REPO / "corpora" / "downloads" / "external_repos" / "mayig_cisi_json" / "corpus"
CONTACT_ZONE = REPO / "corpora" / "downloads" / "contact_zone"
REPORTS = REPO / "reports"

# ── 1. Fix INDUS_FINAL_ANCHORS ────────────────────────────────────────────────

def fix_anchors() -> dict:
    """Remove LOW-confidence nīr placeholder entries from INDUS_FINAL_ANCHORS.json."""
    path = BKRPT / "INDUS_FINAL_ANCHORS.json"
    if not path.exists():
        return {"status": "skipped", "reason": "INDUS_FINAL_ANCHORS.json not found"}

    data = json.loads(path.read_text(encoding="utf-8"))
    anchors_in = data.get("anchors", {})

    kept: dict = {}
    removed: list = []
    for sign, info in anchors_in.items():
        conf = (info.get("confidence") or "").upper()
        reading = (info.get("reading") or "").strip()
        # Remove placeholders: LOW confidence AND reading is nīr (water) placeholder
        # Also remove INIT-* and TERM-* placeholders that have no real phonetic value
        is_nir_placeholder = conf == "LOW" and reading in ("nīr", "nir")
        is_init_placeholder = conf in ("LOW", "MEDIUM") and reading.startswith("INIT-")
        is_term_placeholder = conf in ("LOW", "MEDIUM") and reading.startswith("TERM-")
        is_med_placeholder = conf in ("LOW", "MEDIUM") and reading.startswith("MED-")

        if is_nir_placeholder:
            removed.append(f"{sign}(nīr/LOW)")
        elif is_init_placeholder:
            removed.append(f"{sign}({reading}/{conf})")
        elif is_term_placeholder:
            removed.append(f"{sign}({reading}/{conf})")
        elif is_med_placeholder:
            removed.append(f"{sign}({reading}/{conf})")
        else:
            kept[sign] = info

    # Update total and confidence breakdown
    by_conf: dict = {}
    for info in kept.values():
        c = (info.get("confidence") or "LOW").upper()
        by_conf[c] = by_conf.get(c, 0) + 1

    data["anchors"] = kept
    data["total"] = len(kept)
    data["by_confidence"] = by_conf
    data["_cleanup_note"] = (
        f"2026-05-17: Removed {len(removed)} nīr/INIT/TERM/MED placeholder entries "
        f"from V8-V24 autonomous loops. Retained {len(kept)} real anchors."
    )

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    result = {
        "status": "done",
        "original_count": len(anchors_in),
        "kept_count": len(kept),
        "removed_count": len(removed),
        "by_confidence": by_conf,
        "sample_removed": removed[:10],
        "kept_high": [f"{s}={info['reading']}" for s, info in kept.items()
                      if info.get("confidence") == "HIGH"],
    }
    print(f"\n✓ Anchor set fixed: {len(anchors_in)} → {len(kept)} "
          f"(removed {len(removed)} placeholders)")
    print(f"  By confidence: {by_conf}")
    print(f"  HIGH: {result['kept_high']}")
    return result


# ── 2. Rebuild CISI corpus JSON ───────────────────────────────────────────────

def rebuild_cisi_corpus() -> dict:
    """Build indus_cisi_corpus.json from the mayig_cisi_json corpus folders."""
    if not CISI_SRC.exists():
        return {"status": "skipped", "reason": f"CISI source not found: {CISI_SRC}"}

    inscriptions: list[dict] = []
    n_signs = 0
    sign_freq: dict = defaultdict(int)

    # Process both m001_m099 and m100_m199 subfolders
    for subfolder in ["m001_m099", "m100_m199"]:
        folder = CISI_SRC / subfolder
        if not folder.exists():
            print(f"  WARNING: {subfolder} not found, skipping")
            continue
        for jf in sorted(folder.glob("*.json")):
            try:
                entries = json.loads(jf.read_text(encoding="utf-8"))
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    raw_id = entry.get("id", "")
                    desc = entry.get("description", "")
                    graphemes = entry.get("graphemes", [])
                    if not graphemes:
                        continue
                    signs = []
                    for g in graphemes:
                        gid = g.get("id", "")
                        if gid:
                            signs.append(gid)
                            sign_freq[gid] += 1
                    if not signs:
                        continue
                    # Derive site from ID prefix
                    site = raw_id[0] if raw_id else "?"
                    inscriptions.append({
                        "id": raw_id,
                        "site": site,
                        "description": desc,
                        "signs": signs,
                        "n_signs": len(signs),
                    })
                    n_signs += len(signs)
            except Exception as e:
                print(f"  WARNING: failed to parse {jf.name}: {e}")

    if not inscriptions:
        return {"status": "failed", "reason": "No inscription data found in mayig corpus"}

    corpus = {
        "_citation": {
            "primary_sources": ["A.1", "A.2"],
            "derivation": (
                "Derived from mayig/indus-valley-script-corpus (GitHub, MIT License). "
                "Digitization of Parpola et al. CISI Vols 1-3. Sign IDs are Parpola P-numbers."
            ),
            "authors": "mcskware (digitization); Parpola, A. et al. 1987-2010 (original corpus)",
            "date": "2026-05-17",
        },
        "n_inscriptions": len(inscriptions),
        "n_sign_tokens": n_signs,
        "n_distinct_signs": len(sign_freq),
        "sign_numbering": "Parpola (allograph numbers, e.g. P121, P324)",
        "sites": sorted(set(i["site"] for i in inscriptions)),
        "inscriptions": inscriptions,
    }

    out = DATA / "indus_cisi_corpus.json"
    out.write_text(json.dumps(corpus, indent=2, ensure_ascii=False), encoding="utf-8")

    # Also write to the legacy path that download_indus_cisi.py would have put it
    legacy_path = REPO / "data" / "indus_cisi_corpus.json"
    legacy_path.parent.mkdir(exist_ok=True)
    legacy_path.write_text(json.dumps(corpus, indent=2, ensure_ascii=False), encoding="utf-8")

    result = {
        "status": "done",
        "n_inscriptions": len(inscriptions),
        "n_sign_tokens": n_signs,
        "n_distinct_signs": len(sign_freq),
        "sites": sorted(set(i["site"] for i in inscriptions)),
        "top_5_signs": sorted(sign_freq.items(), key=lambda x: -x[1])[:5],
        "mean_length": round(n_signs / max(len(inscriptions), 1), 2),
    }
    print(f"\n✓ CISI corpus rebuilt: {len(inscriptions)} inscriptions, "
          f"{n_signs} tokens, {len(sign_freq)} distinct signs")
    print(f"  Sites: {result['sites']}, Mean length: {result['mean_length']}")
    print(f"  Top 5 signs: {result['top_5_signs']}")
    return result


# ── 3. Build Gulf seal corpus ─────────────────────────────────────────────────

def build_gulf_seal_corpus() -> dict:
    """Build gulf_seal_corpus.json from Laursen 2010 Table 1 and contact_zone data."""
    gulf_path = CONTACT_ZONE / "gulf_seals"
    meluhha_path = CONTACT_ZONE / "meluhha_tablets.json"
    laursen_path = CONTACT_ZONE / "laursen_2010_table1.json"

    sources_found = []
    all_items: list[dict] = []

    # Load Laursen Table 1
    if laursen_path.exists():
        try:
            raw = json.loads(laursen_path.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                for item in raw:
                    all_items.append({
                        "id": item.get("id", f"Laursen_{len(all_items)}"),
                        "site": item.get("site", "Gulf"),
                        "site_region": item.get("region", "Bahrain/Oman"),
                        "signs": item.get("signs", item.get("inscription", [])),
                        "source": "Laursen 2010 Table 1",
                        "catalog": "Laursen",
                        "description": item.get("description", ""),
                    })
                sources_found.append(f"laursen_2010_table1.json ({len(raw)} entries)")
            elif isinstance(raw, dict):
                # Might be a dict with nested structure
                items = raw.get("seals", raw.get("items", raw.get("data", [])))
                for item in items:
                    all_items.append({
                        "id": item.get("id", f"Laursen_{len(all_items)}"),
                        "site": item.get("site", "Gulf"),
                        "site_region": "Bahrain/Oman",
                        "signs": item.get("signs", item.get("inscription", [])),
                        "source": "Laursen 2010 Table 1",
                        "catalog": "Laursen",
                        "description": item.get("description", ""),
                    })
                sources_found.append(f"laursen_2010_table1.json ({len(items)} entries)")
        except Exception as e:
            print(f"  WARNING: laursen_2010_table1.json parse failed: {e}")

    # Load Meluhha tablets
    if meluhha_path.exists():
        try:
            meluhha = json.loads(meluhha_path.read_text(encoding="utf-8"))
            if isinstance(meluhha, list):
                for item in meluhha:
                    signs_raw = item.get("signs", item.get("inscription", item.get("text", [])))
                    all_items.append({
                        "id": item.get("id", f"Meluhha_{len(all_items)}"),
                        "site": item.get("site", "Mesopotamia"),
                        "site_region": "Mesopotamia/Gulf",
                        "signs": signs_raw if isinstance(signs_raw, list) else [],
                        "source": "Meluhha tablets corpus",
                        "catalog": "Meluhha",
                        "description": item.get("description", item.get("title", "")),
                    })
                sources_found.append(f"meluhha_tablets.json ({len(meluhha)} entries)")
        except Exception as e:
            print(f"  WARNING: meluhha_tablets.json parse failed: {e}")

    # Check gulf_seals subfolder
    if gulf_path.exists():
        for jf in gulf_path.glob("*.json"):
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                items = data if isinstance(data, list) else data.get("seals", [])
                for item in items:
                    all_items.append({
                        "id": item.get("id", f"{jf.stem}_{len(all_items)}"),
                        "site": item.get("site", "Gulf"),
                        "site_region": "Gulf region",
                        "signs": item.get("signs", item.get("inscription", [])),
                        "source": f"gulf_seals/{jf.name}",
                        "catalog": jf.stem,
                        "description": item.get("description", ""),
                    })
                sources_found.append(f"gulf_seals/{jf.name} ({len(items)} entries)")
            except Exception as e:
                print(f"  WARNING: {jf.name} parse failed: {e}")

    if not all_items:
        return {
            "status": "partial",
            "reason": "No inscription data found in Gulf seal sources",
            "sources_checked": [str(gulf_path), str(meluhha_path), str(laursen_path)],
        }

    # Only keep entries that have actual sign sequences
    with_signs = [item for item in all_items if item.get("signs")]
    without_signs = [item for item in all_items if not item.get("signs")]

    corpus = {
        "_citation": {
            "primary_sources": ["A.5", "C.3"],
            "derivation": (
                "Gulf-type seal and Meluhha tablet corpus from Laursen 2010 Table 1 "
                "(Bahrain/Oman Gulf-type seals) and Meluhha tablet dataset. "
                "Cross-site contact zone analysis."
            ),
            "authors": "Laursen, S.T. 2010 (Gulf seals); various (Meluhha tablets)",
            "date": "2026-05-17",
        },
        "n_total": len(all_items),
        "n_with_signs": len(with_signs),
        "n_metadata_only": len(without_signs),
        "sources": sources_found,
        "seals": all_items,
    }

    out = DATA / "gulf_seal_corpus.json"
    out.write_text(json.dumps(corpus, indent=2, ensure_ascii=False), encoding="utf-8")

    result = {
        "status": "done",
        "n_total": len(all_items),
        "n_with_signs": len(with_signs),
        "sources": sources_found,
    }
    print(f"\n✓ Gulf seal corpus built: {len(all_items)} entries "
          f"({len(with_signs)} with sign sequences)")
    print(f"  Sources: {sources_found}")
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Phase-44 Infrastructure Fixes")
    print("=" * 60)

    results = {}
    results["anchor_fix"] = fix_anchors()
    results["cisi_rebuild"] = rebuild_cisi_corpus()
    results["gulf_corpus"] = build_gulf_seal_corpus()

    out = REPORTS / "phase44_infrastructure.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✓ Results saved to {out.name}")
    print("\nSummary:")
    for task, r in results.items():
        print(f"  {task}: {r.get('status', '?')}")
