"""Run assumption-free distributional and word-structure experiments.
Run: shell.cmd python backend/run_assumption_free_experiments.py
"""
import sys, os, json
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

import csv
from glossa_lab.pipelines.distributional_decipherment import analyse_distributional
from glossa_lab.pipelines.word_structure_hypothesis import rank_language_families, compute_corpus_profile
from tests.corpora.linear_a_real_corpus import (
    load_raw_tablet_corpus, load_real_linear_a_signs, _SKIP_SIGNS
)
from tests.corpora.indus_corpus import generate_indus_flat

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "backend" / "tests" / "corpora" / "fixtures" / "linear_a_real" / "phase1_corpus_manifest.csv"


def load_actual_inscriptions() -> list[list[str]]:
    """Parse corpus_manifest.csv into actual inscription-level sign sequences."""
    inscriptions = []
    if not MANIFEST.exists():
        flat, _ = load_raw_tablet_corpus()
        # Fallback: use prefix patterns as approximate inscriptions
        # Use variable-length chunks from 2-8 following a simple distribution
        import random; rng = random.Random(42)
        i = 0
        while i < len(flat):
            length = rng.choice([2, 2, 3, 3, 3, 4, 4, 5, 6])
            chunk = flat[i:i+length]
            if chunk: inscriptions.append(chunk)
            i += length
        return inscriptions

    with open(MANIFEST, encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            notes = row.get("notes", "").lower()
            if "logogram" in notes:
                continue
            seq = row.get("canonical_sequence", "").strip()
            tokens = []
            for tok in seq.split():
                t = tok.strip().lstrip("]")
                if t and t not in _SKIP_SIGNS and "[?" not in t and not t.startswith("[["):
                    tokens.append(t)
            if len(tokens) >= 2:
                inscriptions.append(tokens)
    return inscriptions


# ── 1. Linear A distributional decipherment (no LB assumptions) ──────
print("=== DISTRIBUTIONAL DECIPHERMENT: LINEAR A ===")
insc_la_chunked = load_actual_inscriptions()
print(f"  Loaded {len(insc_la_chunked)} inscription entries from manifest")

da_result = analyse_distributional(
    insc_la_chunked,
    min_sign_count=3,
    cluster_threshold=0.35,
    top_n=30,
)
print(f"  Corpus size:          {da_result.get('corpus_size')} tokens")
print(f"  Unique signs:         {da_result.get('unique_signs')}")
print(f"  Vowel clusters:       {da_result.get('n_vowel_clusters')}")
print(f"  Consonant clusters:   {da_result.get('n_consonant_clusters')}")
print(f"  Grid cells (filled):  {da_result.get('phonological_grid',{}).get('n_filled_cells',0)}")
ws = da_result.get('word_structure',{})
print(f"  Mean word length:     {ws.get('mean_word_length')}")
print(f"  TTR:                  {ws.get('type_token_ratio')}")
print(f"  Unique inscription %: {ws.get('unique_inscription_ratio')}")
if ws.get('likely_prefixes'):
    print(f"  Likely prefixes:      {ws['likely_prefixes'][:3]}")
if ws.get('likely_suffixes'):
    print(f"  Likely suffixes:      {ws['likely_suffixes'][:3]}")
vc = da_result.get('vowel_clusters', [])
print(f"  Top vowel cluster:    {vc[0] if vc else '(none)'}")
cc = da_result.get('consonant_clusters', [])
print(f"  Top consonant cluster:{cc[0] if cc else '(none)'}")

# ── 2. Linear A word-structure hypothesis (6 languages) ──────────────
print("\n=== WORD-STRUCTURE HYPOTHESIS: LINEAR A ===")
wsh_la = rank_language_families(insc_la_chunked)
cp = wsh_la['corpus_profile']
print(f"  Corpus word-length distribution: {dict(sorted(cp.get('word_length_dist',{}).items()))}")
print(f"  Mean word length:    {cp.get('mean_word_length')}")
print(f"  TTR:                 {cp.get('type_token_ratio')}")
print(f"  Prefix entropy:      {cp.get('prefix_entropy')}")
print(f"  Suffix entropy:      {cp.get('suffix_entropy')}")
print(f"\n  Rankings (compatibility score, higher=better):")
for r in wsh_la['ranked_hypotheses']:
    print(f"    {r['profile']:35} compat={r['compatibility']:.4f}  cost={r['cost']:.4f}  kl={r['word_length_kl']:.4f}")
print(f"\n  WINNER: {wsh_la['winner']} (margin={wsh_la['margin_vs_second']:.4f})")

# ── 3. Indus Script word-structure hypothesis ─────────────────────────
print("\n=== WORD-STRUCTURE HYPOTHESIS: INDUS SCRIPT ===")
indus = generate_indus_flat(seed=42)
# Segment into inscription-length groups based on Indus inscription structure
# Average Indus inscription length is ~5 signs
insc_indus = [indus[i:i+5] for i in range(0, len(indus), 5) if indus[i:i+5]]
wsh_indus = rank_language_families(insc_indus)
cp_i = wsh_indus['corpus_profile']
print(f"  Corpus size:         {cp_i.get('total_words')} inscriptions")
print(f"  Mean word length:    {cp_i.get('mean_word_length')}")
print(f"  TTR:                 {cp_i.get('type_token_ratio')}")
print(f"  Prefix entropy:      {cp_i.get('prefix_entropy')}")
print(f"  Suffix entropy:      {cp_i.get('suffix_entropy')}")
print(f"\n  Rankings:")
for r in wsh_indus['ranked_hypotheses']:
    print(f"    {r['profile']:35} compat={r['compatibility']:.4f}  kl={r['word_length_kl']:.4f}")
print(f"\n  WINNER: {wsh_indus['winner']} (margin={wsh_indus['margin_vs_second']:.4f})")

# ── 4. Cross-script alignment: Linear A vs Linear B ──────────────────
print("\n=== CROSS-SCRIPT ALIGNMENT: LINEAR A vs LINEAR B ===")
from glossa_lab.data.linear_b_language import get_corpus_symbols
lb_syms = get_corpus_symbols()
insc_lb = [lb_syms[i:i+4] for i in range(0, len(lb_syms), 4) if lb_syms[i:i+4]]
from glossa_lab.pipelines.distributional_decipherment import cross_script_align
align = cross_script_align(insc_la_chunked, insc_lb)
print(f"  Linear A mean inscription length: {align['corpus_a_mean_length']}")
print(f"  Linear B mean inscription length: {align['corpus_b_mean_length']}")
print(f"  Word-length KL divergence:        {align['word_length_kl_divergence']}")
print(f"  Top Linear A patterns:  {align['corpus_a_top_patterns'][:5]}")
print(f"  Top Linear B patterns:  {align['corpus_b_top_patterns'][:5]}")

# ── Save results ──────────────────────────────────────────────────────
results = {
    "linear_a_distributional": {k: v for k, v in da_result.items()
                                  if k not in ('vowel_clusters','consonant_clusters','top_signs')},
    "linear_a_word_structure": {k: v for k, v in wsh_la.items()
                                  if k != 'corpus_profile'},
    "indus_word_structure": {k: v for k, v in wsh_indus.items()
                               if k != 'corpus_profile'},
    "cross_script_align": align,
    "linear_a_corpus_profile": wsh_la.get('corpus_profile', {}),
    "indus_corpus_profile": wsh_indus.get('corpus_profile', {}),
}

out = REPO / "reports" / "assumption_free_results.json"
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\nResults saved: {out}")
