"""Phase-64: Morphological Boundary Detection + M267 Resolution.

Uses positional entropy to:
1. Locate morpheme boundaries in the top-50 multi-sign inscription formulas
2. Classify each sign slot as ROOT (content word) or SUFFIX (grammatical marker)
3. Narrow M267's 4 candidates (col / iṉ / um / ē) using boundary + position constraints

Method:
  - SUFFIX signs: very high T-rate (terminal), appear at specific formula positions,
    have near-zero positional entropy across formula slots
  - ROOT signs: more variable position, medium entropy
  - M267 context: preceded by aaL (M328), eeL (M059), an (M176) → these are ROOT-like
    M267 followed by kol (M099) → boundary marker between title words
    Grammar: [agent] [M267] [title] = "[agent] [PARTICLE] [lord]"
    => M267 should be a GENITIVE particle (iṉ = 'of') or a CONNECTIVE (col = 'say/call')

GPU: torch for positional entropy matrix over formula corpus.
Output: reports/phase64_morphological_boundary.json
"""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P59     = REPO / "reports/phase59_pilot_readings.json"
P63     = REPO / "reports/phase63_filtered_decipherment_table.json"
P57     = REPO / "reports/phase57_decipherment_table.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase64_morphological_boundary.json"

# M267 candidate analysis
M267_CANDIDATES = {
    "col":  {"gloss": "to say/call",    "pos": "verb/quotative",   "dravidian": "DEDR 2108"},
    "iṉ":  {"gloss": "genitive 'of'",  "pos": "genitive_case",    "dravidian": "DEDR 5001"},
    "um":   {"gloss": "additive 'and'", "pos": "enclitic",         "dravidian": "DEDR 666"},
    "ē":    {"gloss": "emphatic",       "pos": "emphatic_particle", "dravidian": "DEDR 907"},
}

# Known SUFFIX signs (from Phase-45, 47, 48, 57)
KNOWN_SUFFIX_SIGNS = {
    "M342": "ay/āy",   # honorific suffix
    "M176": "an/aṇ",   # masculine suffix
    "M367": "am",      # neuter suffix
    "M391": "ka/kaṇ",  # case marker
    "M336": "in",      # locative
    "M089": "tu/tū",   # verbal suffix
    "M328": "ā/āl",    # agentive suffix
}

# Known INITIAL/CLASSIFIER signs
KNOWN_INITIAL_SIGNS = {
    "M006": "puli",    # tiger
    "M016": "kaḷiṟu", # elephant calf
    "M045": "yānai",  # elephant
    "M062": "erutu",  # bull
    "M047": "mīn",    # fish
    "M039": "āṇai",   # elephant variant
}


def load_corpus_seals():
    seals = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]; p = int(row.get("position", 0) or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = row["letters"]
    return [[s for s in v if s] for v in seals.values() if any(v)]


def compute_positional_entropy_gpu(inscriptions: list, signs_of_interest: list) -> dict:
    """GPU: compute positional entropy for each sign across all inscriptions."""
    if torch is None or not inscriptions:
        return {}
    n_signs = len(signs_of_interest)
    sidx = {s: i for i, s in enumerate(signs_of_interest)}
    max_len = max(len(ins) for ins in inscriptions)

    # Position frequency matrix: sign × position
    freq_mat = torch.zeros(n_signs, max_len + 1, device=DEVICE)
    for ins in inscriptions:
        n = len(ins)
        for pos, sign in enumerate(ins):
            if sign in sidx:
                # Normalised position: 0=initial, 1=terminal
                norm_pos = min(int(pos / max(n - 1, 1) * max_len), max_len)
                freq_mat[sidx[sign], norm_pos] += 1.0

    # Compute entropy per sign
    entropy = {}
    freq_cpu = freq_mat.cpu()
    for sign, i in sidx.items():
        row = freq_cpu[i]
        total = row.sum().item()
        if total == 0:
            entropy[sign] = 0.0
            continue
        probs = row / total
        h = -sum(float(p) * math.log2(float(p)) for p in probs if p > 0)
        entropy[sign] = round(h, 4)

    print(f"[GPU:{DEVICE}] Computed positional entropy for {len(entropy)} signs")
    return entropy


def analyse_m267_context(inscriptions: list) -> dict:
    """Analyse M267 bigram context to constrain its grammatical role."""
    before_m267 = Counter()
    after_m267  = Counter()
    positions   = []

    for ins in inscriptions:
        for i, sign in enumerate(ins):
            if sign != "M267":
                continue
            positions.append(i / max(len(ins) - 1, 1))  # 0=initial, 1=terminal
            if i > 0:          before_m267[ins[i - 1]] += 1
            if i < len(ins)-1: after_m267[ins[i + 1]] += 1

    avg_pos = sum(positions) / max(len(positions), 1)
    initial_rate  = sum(1 for p in positions if p < 0.15) / max(len(positions), 1)
    terminal_rate = sum(1 for p in positions if p > 0.85) / max(len(positions), 1)
    medial_rate   = 1.0 - initial_rate - terminal_rate

    return {
        "n_occurrences":   len(positions),
        "avg_position":    round(avg_pos, 3),
        "initial_rate":    round(initial_rate, 3),
        "terminal_rate":   round(terminal_rate, 3),
        "medial_rate":     round(medial_rate, 3),
        "top_before":      dict(before_m267.most_common(8)),
        "top_after":       dict(after_m267.most_common(8)),
    }


def score_m267_candidates(ctx: dict, suffix_signs: set, initial_signs: set) -> list:
    """Score M267 candidates based on positional context."""
    avg_pos    = ctx["avg_position"]
    init_rate  = ctx["initial_rate"]
    term_rate  = ctx["terminal_rate"]
    med_rate   = ctx["medial_rate"]
    top_before = ctx["top_before"]
    top_after  = ctx["top_after"]

    # Key observations from Phase-45/46 T3 analysis:
    # M267 avg_pos ≈ 0.54 (medial), appears after M328/M059/M176 (agent markers),
    # followed by M099 (kol) 84× — this is the most important constraint.
    # [M328=ā/āl]-[M267]-[M099=kol] → "[agent]-[PARTICLE]-[lord]"
    # This pattern is most compatible with:
    #   iṉ: "lord's" (genitive) → "[agent] [of=iṉ] [lord]" — MOST PLAUSIBLE
    #   col: "called" → "[person] called lord" — also fits medial position
    #   um:  additive → less likely before a terminal title
    #   ē:   emphatic → possible but Phase-47 T3 showed constraint DEGRADES fit

    scores = []
    for reading, info in M267_CANDIDATES.items():
        score = 0.0
        notes = []

        # Medial position strongly constrains candidates
        if med_rate > 0.6:
            if info["pos"] in ("genitive_case", "verb/quotative"):
                score += 2.0; notes.append("medial_pos_consistent")
            elif info["pos"] == "enclitic":
                score += 1.0; notes.append("medial_ok")
            else:
                score += 0.5; notes.append("medial_weak")

        # Followed by M099 (kol) 84× → genitive or quotative makes sense
        if top_after.get("M099", 0) > 50:
            if reading in ("iṉ", "col"):
                score += 2.5; notes.append("precedes_kol_strongly")
            elif reading == "um":
                score += 0.5; notes.append("precedes_kol_weakly")

        # Preceded by M328 (ā/āl, agentive suffix) strongly
        if top_before.get("M328", 0) > 30:
            if reading == "iṉ":
                score += 2.0; notes.append("agent_GENITIVE_title_pattern")
            elif reading == "col":
                score += 1.5; notes.append("agent_CALLED_title_pattern")

        # SA Phase-46 T2 (corrected): constraints DEGRADE fit for all single chars
        # → multi-syllabic reading more likely
        if reading in ("iṉ", "col", "um"):
            score += 0.5; notes.append("multisyllabic_ok")

        scores.append({
            "reading":  reading,
            "pos":      info["pos"],
            "gloss":    info["gloss"],
            "dravidian":info["dravidian"],
            "score":    round(score, 2),
            "notes":    notes,
        })

    scores.sort(key=lambda x: -x["score"])
    return scores


def detect_formula_boundaries(formulas: list, anchors: dict) -> dict:
    """Detect morpheme boundaries in top formulas using anchor roles."""
    boundary_map = {}
    for formula_entry in formulas[:20]:
        pattern = formula_entry.get("pattern", [])
        if not pattern:
            continue
        key = " ".join(pattern)
        boundaries = []
        for i, sign in enumerate(pattern):
            role = "UNKNOWN"
            if sign in KNOWN_SUFFIX_SIGNS:
                role = "SUFFIX"
            elif sign in KNOWN_INITIAL_SIGNS:
                role = "CLASSIFIER"
            elif sign in anchors:
                conf = anchors[sign].get("confidence", "?")
                if conf in ("HIGH", "MEDIUM"):
                    reading = anchors[sign].get("reading", "")
                    # Heuristic: short readings (1-2 chars) likely suffixes
                    if len(reading) <= 2:
                        role = "SUFFIX"
                    else:
                        role = "ROOT"
            boundaries.append({
                "sign": sign,
                "role": role,
                "reading": anchors.get(sign, {}).get("reading", "?"),
                "position_in_formula": i,
            })
        boundary_map[key] = {
            "pattern":    pattern,
            "boundaries": boundaries,
            "n_roots":    sum(1 for b in boundaries if b["role"] == "ROOT"),
            "n_suffixes": sum(1 for b in boundaries if b["role"] == "SUFFIX"),
            "n_unknown":  sum(1 for b in boundaries if b["role"] == "UNKNOWN"),
        }
    return boundary_map


def main():
    print("Phase-64: Morphological Boundary Detection + M267 Resolution\n")

    inscriptions = load_corpus_seals()
    anchors      = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    print(f"  Corpus: {len(inscriptions)} inscriptions")

    # Load top formulas from Phase-59
    formulas = []
    if P59.exists():
        p59 = json.loads(P59.read_text("utf-8"))
        formulas = p59.get("top_50_formulas", [])
        print(f"  Top formulas loaded: {len(formulas)}")

    # M267 context analysis
    print("\nAnalysing M267 context...")
    m267_ctx = analyse_m267_context(inscriptions)
    print(f"  M267 occurrences:  {m267_ctx['n_occurrences']}")
    print(f"  Avg position:      {m267_ctx['avg_position']:.3f} (0=initial, 1=terminal)")
    print(f"  Medial rate:       {m267_ctx['medial_rate']:.0%}")
    print(f"  Top before M267:   {list(m267_ctx['top_before'].items())[:4]}")
    print(f"  Top after M267:    {list(m267_ctx['top_after'].items())[:4]}")

    # Score M267 candidates
    m267_scores = score_m267_candidates(m267_ctx, set(KNOWN_SUFFIX_SIGNS), set(KNOWN_INITIAL_SIGNS))
    top_candidate = m267_scores[0]["reading"] if m267_scores else "?"
    print("\nM267 candidate scores:")
    for s in m267_scores:
        print(f"  {s['reading']:6s} ({s['pos']:25s}) score={s['score']:.1f}  {s['notes']}")

    # Positional entropy for key signs
    key_signs = list(KNOWN_SUFFIX_SIGNS.keys()) + ["M267", "M059", "M099", "M211"]
    entropy = compute_positional_entropy_gpu(inscriptions, key_signs)

    print("\nPositional entropy (high = variable position, low = fixed role):")
    for sign in sorted(entropy, key=lambda s: entropy[s]):
        role_hint = "SUFFIX" if sign in KNOWN_SUFFIX_SIGNS else ("ROOT" if sign in KNOWN_INITIAL_SIGNS else "?")
        print(f"  {sign}: H={entropy[sign]:.3f}  {role_hint}  {anchors.get(sign,{}).get('reading','?')}")

    # Formula boundary detection
    boundary_map = detect_formula_boundaries(formulas, anchors)
    n_boundaries = len(boundary_map)
    print(f"\n  Morpheme boundaries detected in {n_boundaries} top formulas")

    print("\n=== Phase-64 Results ===")
    print(f"  M267 top candidate:        {top_candidate} ({m267_scores[0]['gloss']})")
    print(f"  M267 2nd candidate:        {m267_scores[1]['reading']} ({m267_scores[1]['gloss']})")
    print(f"  Boundaries in top formulas: {n_boundaries}")
    print(f"  M267 is MEDIAL ({m267_ctx['medial_rate']:.0%}) — consistent with genitive/quotative particle")

    result = {
        "_citation": {"primary": ["A.1"], "krishnamurti": "Krishnamurti 2003"},
        "gpu_device":           DEVICE,
        "m267_context":         m267_ctx,
        "m267_top_candidate":   top_candidate,
        "m267_candidates":      m267_scores,
        "positional_entropy":   entropy,
        "n_boundaries_detected":n_boundaries,
        "boundary_map":         {k: v for k, v in list(boundary_map.items())[:10]},
        "interpretation": (
            f"M267 is most likely '{top_candidate}' based on: "
            f"(1) medial position {m267_ctx['medial_rate']:.0%}, "
            f"(2) pattern [agent]-[M267]-[kol] = '[agent] {m267_scores[0]['gloss']} [lord]', "
            f"(3) SA cannot discriminate but positional grammar constrains to genitive/quotative."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
