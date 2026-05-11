"""
V5 Phases 1-3: Data Corrections, Spectral Syllabic Grid, Longest-Text Analysis
================================================================================
Phase 1: Corpus unification + data corrections
Phase 2: Spectral clustering on co-substitution matrix
Phase 3: Longest-text decoding with anchors
"""
import csv
import json
import os
import sys
import numpy as np
from collections import defaultdict, Counter
from pathlib import Path

REPORT_DIR = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports")
REPORT_DIR.mkdir(exist_ok=True)

# ============================================================
# PHASE 1: Data Corrections + Unified Corpus
# ============================================================

def load_holdat_corpus():
    """Load Holdat LLC corpus (1,670 seals, Mahadevan sign numbering)."""
    path = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\external_repos\holdatllc_indus\indus_corpus 2.csv")
    seals = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            seals[r["cisi_number"]].append(r)
    return seals


def load_cisi_mayig_corpus():
    """Load CISI mayig corpus (Parpola sign numbering)."""
    path = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\glossa_lab\data\phase18_corpora\cisi_mayig_inscriptions.csv")
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def build_unified_corpus():
    """Build unified corpus from Holdat (primary) and supplement with CISI mayig."""
    holdat = load_holdat_corpus()
    cisi = load_cisi_mayig_corpus()

    # Convert Holdat to unified format
    unified = []
    for cisi_num, signs in holdat.items():
        seq = [s["letters"] for s in signs]
        unified.append({
            "id": cisi_num,
            "source": "holdat",
            "site": signs[0]["site"],
            "iconography": signs[0]["iconography"],
            "n_signs": len(seq),
            "signs": seq,
            "sign_system": "mahadevan"
        })

    # Add CISI mayig entries not already in Holdat (different sign system)
    unified_cisi = []
    for row in cisi:
        unified_cisi.append({
            "id": row["id"],
            "source": "cisi_mayig",
            "site": "Mohenjo-daro",  # All are M-series
            "iconography": row["description"],
            "n_signs": int(row["n_signs"]),
            "signs": row["signs_ws_joined"].split(),
            "sign_system": "parpola"
        })

    return unified, unified_cisi


def phase1_corrections():
    """Apply data corrections from deep-research-report.md."""
    corrections = {
        "dholavira_signboard": {
            "corrected_sign_count": 10,
            "note": "Dholavira signboard has 9-10 signs (scholarly debate on exact count due to fragmentary edge). "
                    "NOT 26 signs as sometimes erroneously claimed. The 26-sign count refers to the three-sided "
                    "amulet M-494/M-495, which has signs distributed across three faces.",
            "sources": ["Bisht 1991", "Coningham (mohenjodarorj)", "Farmer (safarmer.com)"]
        },
        "longest_single_face": {
            "inscription_id": "M-314",
            "mahadevan_number": "M-0314",
            "sign_count": 17,
            "description": "Longest inscription on a single flat surface. Contains 17 non-repeating symbols. "
                          "Seal from Mohenjo-daro with rhinoceros iconography.",
            "note_holdat": "Holdat corpus records only 4 signs for M-0314 (primary text line). "
                          "Full 17-sign reading spans 3 lines on same face per CISI.",
            "sources": ["Farmer (safarmer.com)", "Pandita Naomi (substack)", "CISI Vol. 1"]
        },
        "longest_multi_face": {
            "inscription_ids": ["M-494", "M-495"],
            "total_sign_count": 26,
            "faces": 3,
            "description": "Two examples of a mass-produced molded object with 26 signs across 3 faces "
                          "(5 long surfaces, 7 total including sides). Whether these form a continuous "
                          "'message' is debated. Farmer argues they are non-linguistic ritual symbols.",
            "note_holdat": "Holdat corpus records 6 signs each for M-0494 and M-0495 (one face only).",
            "sources": ["Farmer (safarmer.com)", "Marshall 1931", "CISI Vol. 1"]
        },
        "corpus_statistics": {
            "holdat_seals": 1670,
            "holdat_max_signs_per_seal": 8,
            "cisi_mayig_seals": 179,
            "cisi_mayig_max_signs": 13,
            "note": "Both open-access corpora cap at shorter than known max. Full CISI (unpublished digital) "
                    "contains ~4,000+ inscriptions. CISID project underway by Ameri, Jamison, Kenoyer, Uesugi."
        },
        "dholavira_in_corpus": {
            "count": 106,
            "note": "106 Dholavira inscriptions in Holdat corpus. Bisht 2015 draft may contain up to 150.",
            "max_length_in_corpus": 8
        }
    }
    return corrections


# ============================================================
# PHASE 2: Spectral Syllabic Grid
# ============================================================

def build_co_substitution_matrix(corpus):
    """
    Build co-substitution matrix: signs that appear in the same positional context
    (same position, similar surrounding signs) are candidates for paradigmatic alternation.
    """
    # Use positional contexts: for each sign at position i in inscription,
    # context = (prev_sign or BOS, next_sign or EOS)
    # Two signs that share many contexts are co-substitutable
    sign_set = set()
    for entry in corpus:
        for s in entry["signs"]:
            sign_set.add(s)

    sign_list = sorted(sign_set)
    sign_idx = {s: i for i, s in enumerate(sign_list)}
    n = len(sign_list)

    # Context sharing matrix
    # For each context (prev, next), collect signs that appear there
    context_signs = defaultdict(set)
    sign_contexts = defaultdict(set)

    for entry in corpus:
        signs = entry["signs"]
        for i, s in enumerate(signs):
            prev_s = signs[i-1] if i > 0 else "BOS"
            next_s = signs[i+1] if i < len(signs) - 1 else "EOS"
            ctx = (prev_s, next_s)
            context_signs[ctx].add(s)
            sign_contexts[s].add(ctx)

    # Build co-sub matrix: C[i,j] = number of shared contexts
    C = np.zeros((n, n), dtype=np.float64)
    for ctx, signs_in_ctx in context_signs.items():
        if len(signs_in_ctx) < 2:
            continue
        slist = list(signs_in_ctx)
        for a in range(len(slist)):
            for b in range(a+1, len(slist)):
                i = sign_idx[slist[a]]
                j = sign_idx[slist[b]]
                C[i, j] += 1
                C[j, i] += 1

    return C, sign_list, sign_idx, context_signs, sign_contexts


def spectral_clustering(C, n_clusters=8):
    """
    Apply spectral clustering using normalized Laplacian.
    Returns cluster assignments.
    """
    # Degree matrix
    D = np.diag(C.sum(axis=1))
    # Handle zero-degree nodes
    d = C.sum(axis=1)
    d_inv_sqrt = np.zeros_like(d)
    nonzero = d > 0
    d_inv_sqrt[nonzero] = 1.0 / np.sqrt(d[nonzero])
    D_inv_sqrt = np.diag(d_inv_sqrt)

    # Normalized Laplacian: L_sym = I - D^{-1/2} C D^{-1/2}
    n = C.shape[0]
    I = np.eye(n)
    L_sym = I - D_inv_sqrt @ C @ D_inv_sqrt

    # Replace NaN with 0
    L_sym = np.nan_to_num(L_sym)

    # Eigen-decomposition (smallest eigenvalues)
    eigenvalues, eigenvectors = np.linalg.eigh(L_sym)

    # Use first n_clusters eigenvectors
    V = eigenvectors[:, :n_clusters]

    # Normalize rows
    row_norms = np.linalg.norm(V, axis=1, keepdims=True)
    row_norms[row_norms == 0] = 1
    V_norm = V / row_norms

    # K-means clustering
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=n_clusters, n_init=20, random_state=42)
    labels = km.fit_predict(V_norm)

    return labels, eigenvalues, eigenvectors


def analyze_spectral_grid(labels, sign_list, corpus, sign_contexts):
    """Analyze the spectral clusters for consonant/vowel structure."""
    clusters = defaultdict(list)
    for i, s in enumerate(sign_list):
        clusters[labels[i]].append(s)

    # Compute frequency for each sign
    sign_freq = Counter()
    for entry in corpus:
        for s in entry["signs"]:
            sign_freq[s] += 1

    # Compute positional bias for each cluster
    pos_bias = {}
    for cl_id, signs in clusters.items():
        initial = 0
        medial = 0
        terminal = 0
        total = 0
        for entry in corpus:
            seq = entry["signs"]
            for i, s in enumerate(seq):
                if s in signs:
                    total += 1
                    if i == 0:
                        initial += 1
                    elif i == len(seq) - 1:
                        terminal += 1
                    else:
                        medial += 1
        if total > 0:
            pos_bias[cl_id] = {
                "initial": initial / total,
                "medial": medial / total,
                "terminal": terminal / total,
                "total_tokens": total
            }
        else:
            pos_bias[cl_id] = {"initial": 0, "medial": 0, "terminal": 0, "total_tokens": 0}

    result = {}
    for cl_id in sorted(clusters.keys()):
        signs = clusters[cl_id]
        freqs = [(s, sign_freq[s]) for s in signs]
        freqs.sort(key=lambda x: -x[1])
        n_contexts = sum(len(sign_contexts.get(s, set())) for s in signs)
        result[int(cl_id)] = {
            "n_signs": len(signs),
            "total_freq": sum(f for _, f in freqs),
            "top_signs": freqs[:10],
            "positional_bias": pos_bias.get(cl_id, {}),
            "avg_contexts": n_contexts / max(len(signs), 1)
        }
    return result


# ============================================================
# PHASE 3: Longest-Text Analysis with Anchors
# ============================================================

def get_known_anchors():
    """Return established HIGH-confidence sign-phoneme anchors from prior work."""
    # Based on V2-V4 anchor refinement (Parpola readings + statistical validation)
    anchors = {
        "M342": {"reading": "ay/ā", "confidence": "HIGH", "basis": "Terminal marker, Dravidian case suffix"},
        "M176": {"reading": "an/aṇ", "confidence": "HIGH", "basis": "Masculine suffix, freq terminal"},
        "M267": {"reading": "min/mīn", "confidence": "HIGH", "basis": "Fish sign = star/planet (Parpola)"},
        "M099": {"reading": "kol/koḷ", "confidence": "HIGH", "basis": "Jar/vessel sign"},
        "M233": {"reading": "ūr", "confidence": "MEDIUM", "basis": "Settlement/place name marker"},
        "M391": {"reading": "ka/kaṇ", "confidence": "MEDIUM", "basis": "Numeral/stroke sign"},
        "M162": {"reading": "il/iḷ", "confidence": "MEDIUM", "basis": "House/dwelling sign"},
        "M328": {"reading": "ā/āl", "confidence": "MEDIUM", "basis": "Man/person sign"},
        "M059": {"reading": "ēḷ/eḷ", "confidence": "MEDIUM", "basis": "Numeral 7"},
        "M051": {"reading": "pū/puḷ", "confidence": "MEDIUM", "basis": "Comb/flower sign"},
        "M089": {"reading": "tu/tū", "confidence": "LOW", "basis": "Positional analysis"},
        "M048": {"reading": "mu/muṉ", "confidence": "LOW", "basis": "Positional analysis"},
    }
    return anchors


def decode_inscription(signs, anchors):
    """Attempt to decode an inscription using known anchors."""
    decoded = []
    for s in signs:
        if s in anchors:
            a = anchors[s]
            decoded.append({
                "sign": s,
                "reading": a["reading"],
                "confidence": a["confidence"]
            })
        else:
            decoded.append({
                "sign": s,
                "reading": "???",
                "confidence": "NONE"
            })
    return decoded


def longest_text_analysis(corpus, anchors):
    """Analyze the longest texts with our anchor set."""
    # Sort by length
    by_len = sorted(corpus, key=lambda x: x["n_signs"], reverse=True)

    results = []
    for entry in by_len[:50]:  # Top 50 longest
        decoded = decode_inscription(entry["signs"], anchors)
        n_decoded = sum(1 for d in decoded if d["confidence"] != "NONE")
        pct = n_decoded / max(len(decoded), 1)
        results.append({
            "id": entry["id"],
            "site": entry["site"],
            "iconography": entry["iconography"],
            "n_signs": entry["n_signs"],
            "signs": entry["signs"],
            "decoded": decoded,
            "n_decoded": n_decoded,
            "pct_decoded": round(pct, 3),
            "reading": " ".join(d["reading"] for d in decoded)
        })

    return results


def scrambled_control(corpus, anchors, n_trials=100):
    """Run scrambled control: randomly pick DIFFERENT signs as anchors and measure decode rate."""
    rng = np.random.default_rng(42)
    by_len = sorted(corpus, key=lambda x: x["n_signs"], reverse=True)[:50]

    # Collect all signs in these inscriptions
    all_signs_in_long = set()
    for entry in by_len:
        for s in entry["signs"]:
            all_signs_in_long.add(s)
    all_signs_list = sorted(all_signs_in_long)

    # Real decode rate
    real_rates = []
    for entry in by_len:
        decoded = decode_inscription(entry["signs"], anchors)
        n_decoded = sum(1 for d in decoded if d["confidence"] != "NONE")
        real_rates.append(n_decoded / max(len(decoded), 1))
    real_mean = np.mean(real_rates)

    # Scrambled trials: pick random signs as fake anchors
    n_anchors = len(anchors)
    anchor_readings = list(set(a["reading"] for a in anchors.values()))
    scrambled_means = []
    for _ in range(n_trials):
        # Pick n_anchors random signs from the sign pool
        fake_signs = rng.choice(all_signs_list, size=min(n_anchors, len(all_signs_list)), replace=False)
        fake_anchors = {}
        for i, s in enumerate(fake_signs):
            fake_anchors[s] = {
                "reading": anchor_readings[i % len(anchor_readings)],
                "confidence": "FAKE"
            }
        rates = []
        for entry in by_len:
            n_decoded = sum(1 for s in entry["signs"] if s in fake_anchors)
            rates.append(n_decoded / max(len(entry["signs"]), 1))
        scrambled_means.append(np.mean(rates))

    scrambled_mean = np.mean(scrambled_means)
    scrambled_std = np.std(scrambled_means)
    snr = (real_mean - scrambled_mean) / max(scrambled_std, 1e-9)

    return {
        "real_decode_rate": round(float(real_mean), 4),
        "scrambled_decode_rate": round(float(scrambled_mean), 4),
        "scrambled_std": round(float(scrambled_std), 4),
        "snr": round(float(snr), 3),
        "n_trials": n_trials,
        "n_inscriptions": len(by_len)
    }


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("=" * 70)
    print("V5 PHASES 1-3: INDUS SCRIPT DECIPHERMENT")
    print("=" * 70)

    # ---- PHASE 1 ----
    print("\n--- PHASE 1: Data Corrections + Unified Corpus ---")
    corrections = phase1_corrections()
    print(f"  Corrections documented: {len(corrections)} items")

    holdat_unified, cisi_unified = build_unified_corpus()
    print(f"  Holdat corpus: {len(holdat_unified)} seals")
    print(f"  CISI mayig corpus: {len(cisi_unified)} inscriptions")

    # Use Holdat as primary (larger, multi-site)
    corpus = holdat_unified

    # Statistics
    sites = Counter(e["site"] for e in corpus)
    lengths = [e["n_signs"] for e in corpus]
    print(f"  Sites: {dict(sites)}")
    print(f"  Mean length: {np.mean(lengths):.2f}, Max: {max(lengths)}, Median: {np.median(lengths):.0f}")

    # Sign inventory
    all_signs = Counter()
    for e in corpus:
        for s in e["signs"]:
            all_signs[s] += 1
    print(f"  Distinct signs: {len(all_signs)}")
    print(f"  Total tokens: {sum(all_signs.values())}")
    print(f"  Top 10 signs: {all_signs.most_common(10)}")

    # ---- PHASE 2 ----
    print("\n--- PHASE 2: Spectral Syllabic Grid ---")
    print("  Building co-substitution matrix...")
    C, sign_list, sign_idx, ctx_signs, sign_ctx = build_co_substitution_matrix(corpus)
    print(f"  Matrix size: {C.shape[0]}x{C.shape[1]}")
    print(f"  Non-zero entries: {np.count_nonzero(C)}")
    print(f"  Total shared contexts: {C.sum():.0f}")

    # Filter to frequent signs (freq >= 5) for meaningful clustering
    freq_threshold = 5
    freq_signs = [s for s in sign_list if all_signs.get(s, 0) >= freq_threshold]
    freq_idx = [sign_idx[s] for s in freq_signs]
    C_filtered = C[np.ix_(freq_idx, freq_idx)]
    print(f"  Signs with freq >= {freq_threshold}: {len(freq_signs)}")

    # Try multiple cluster counts
    best_k = 6
    best_result = None
    eigenvalue_gaps = {}

    for k in [4, 5, 6, 7, 8, 10]:
        try:
            labels, eigenvalues, eigvecs = spectral_clustering(C_filtered, n_clusters=k)
            # Compute eigengap
            gaps = np.diff(eigenvalues[:k+2])
            max_gap_idx = np.argmax(gaps[1:k+1]) + 1  # skip first trivial eigenvalue
            eigenvalue_gaps[k] = {
                "eigenvalues": eigenvalues[:k+2].tolist(),
                "max_gap": float(gaps[max_gap_idx]) if max_gap_idx < len(gaps) else 0,
                "gap_position": int(max_gap_idx)
            }
            # Map labels back to sign names
            grid = analyze_spectral_grid(labels, freq_signs, corpus, sign_ctx)
            cluster_sizes = [grid[cl]["n_signs"] for cl in grid]
            size_var = np.std(cluster_sizes) / max(np.mean(cluster_sizes), 1)
            print(f"  k={k}: cluster sizes={cluster_sizes}, size_cv={size_var:.2f}")

            if best_result is None or size_var < best_result["size_cv"]:
                best_k = k
                best_result = {
                    "k": k,
                    "grid": grid,
                    "labels": labels.tolist(),
                    "size_cv": float(size_var),
                    "eigenvalue_gaps": eigenvalue_gaps[k]
                }
        except Exception as e:
            print(f"  k={k}: FAILED - {e}")

    print(f"\n  Best k={best_k} (lowest CV of cluster sizes)")
    if best_result:
        for cl_id, info in best_result["grid"].items():
            top3 = info["top_signs"][:3]
            pos = info["positional_bias"]
            print(f"    Cluster {cl_id}: n={info['n_signs']} freq={info['total_freq']} "
                  f"top={[t[0] for t in top3]} "
                  f"pos=I:{pos.get('initial',0):.2f}/M:{pos.get('medial',0):.2f}/T:{pos.get('terminal',0):.2f}")

    # ---- PHASE 3 ----
    print("\n--- PHASE 3: Longest-Text Analysis ---")
    anchors = get_known_anchors()
    print(f"  Anchor set: {len(anchors)} signs")

    lt_results = longest_text_analysis(corpus, anchors)
    print(f"  Analyzed {len(lt_results)} longest inscriptions")
    for r in lt_results[:10]:
        print(f"    {r['id']}: n={r['n_signs']} decoded={r['n_decoded']}/{r['n_signs']} "
              f"({r['pct_decoded']*100:.0f}%) -> {r['reading']}")

    # Scrambled control
    print("\n  Running scrambled control (100 trials)...")
    control = scrambled_control(corpus, anchors)
    print(f"    Real decode rate: {control['real_decode_rate']}")
    print(f"    Scrambled rate: {control['scrambled_decode_rate']} ± {control['scrambled_std']}")
    print(f"    SNR: {control['snr']}")

    # ---- SAVE REPORT ----
    report = {
        "title": "V5 Phases 1-3: Data Corrections, Spectral Grid, Longest-Text Analysis",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "phase1_corrections": corrections,
        "phase1_corpus_stats": {
            "holdat_seals": len(holdat_unified),
            "cisi_mayig_inscriptions": len(cisi_unified),
            "distinct_signs_holdat": len(all_signs),
            "total_tokens": sum(all_signs.values()),
            "mean_length": round(float(np.mean(lengths)), 2),
            "max_length": int(max(lengths)),
            "sites": dict(sites),
            "top_20_signs": all_signs.most_common(20)
        },
        "phase2_spectral_grid": {
            "n_signs_analyzed": len(freq_signs),
            "freq_threshold": freq_threshold,
            "best_k": best_k,
            "eigenvalue_gaps": eigenvalue_gaps,
            "clusters": best_result["grid"] if best_result else {},
            "size_cv": best_result["size_cv"] if best_result else None
        },
        "phase3_longest_texts": {
            "n_analyzed": len(lt_results),
            "top_10": lt_results[:10],
            "scrambled_control": control
        }
    }

    out_path = REPORT_DIR / "INDUS_V5_PHASES_1_3.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n  Report saved: {out_path}")

    # Also save the spectral grid details for Phase 4
    grid_path = REPORT_DIR / "INDUS_V5_SPECTRAL_GRID.json"
    grid_data = {
        "sign_list": freq_signs,
        "labels": best_result["labels"] if best_result else [],
        "clusters": best_result["grid"] if best_result else {},
        "eigenvalue_gaps": eigenvalue_gaps
    }
    with open(grid_path, "w", encoding="utf-8") as f:
        json.dump(grid_data, f, indent=2, default=str)
    print(f"  Grid data saved: {grid_path}")

    print("\n" + "=" * 70)
    print("PHASES 1-3 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
