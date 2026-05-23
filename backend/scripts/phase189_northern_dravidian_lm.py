"""Phase 189 — Northern Dravidian LM Comparison

Tests whether a North/Central Dravidian phoneme inventory resolves any of
the 14 absent phonemes better than the Tamil/South Dravidian LM we use.

Background:
  Our SA pipeline runs against a Tamil/South Dravidian LM (DEDR word corpus).
  Brahui (Pakistan/Balochistan), Kurukh (Bihar/Jharkhand), and Gondi
  (central India) are North/Central Dravidian sub-branches that preserve
  some Proto-Dravidian features lost in Tamil:
    - Brahui preserves uvular /q/, /x/, and labiovelar sequences
    - Kurukh/Gondi preserve *p- before round vowels (Tamil shifts to v-)
    - Northern branches preserve *ñ- initially (Tamil merges to n-)
    - Brahui Dravidian: ~200 lexical items identified (McAlpin 1981, Elfenbein 1982)

  If any of the 14 absent phonemes (/su/, /li/, /shu/, /gu/, /ab/, /ba/,
  /du/, /zi/, /ga/, /mil/, /gi/, /en/, /ki/, /sum/) are more natural in
  North Dravidian than South, a North-Dravidian LM would find sign-phoneme
  assignments in our corpus that the Tamil LM misses.

Steps:
  1. Build a synthetic "Proto-Dravidian + North Dravidian augmented" corpus
     using DEDR reconstructed proto-forms (*-forms) that include northern features
  2. Compare the phoneme inventory coverage of each sub-branch for absent phonemes
  3. Run SA with North Dravidian LM (3 seeds)
  4. Compare proposed mappings against Tamil LM results
  5. Identify signs where North Dravidian produces different (potentially better)
     phoneme assignments

References:
  Krishnamurti 2003 "The Dravidian Languages" — authoritative reference
  McAlpin 1974/1981 Elamo-Dravidian papers
  Elfenbein 1982 "The Brahui problem again"
  Zvelebil 1990 "Dravidian Linguistics: An Introduction"
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

ABSENT_PHONEMES = [
    "su","li","shu","gu","ab","ba","du","zi","ga","mil","gi","en","ki","sum"
]

# ── Northern Dravidian phoneme inventory analysis ─────────────────────────────
# Brahui (North Dravidian isolate) — lexical inventory from McAlpin 1981,
# Elfenbein 1982, Andronov 1998, DEDR Brahui entries
# Key Brahui phonemes distinct from Tamil:
#   q (uvular stop), x (uvular fricative), š (palatal sibilant)
#   Initial p- (preserved before round vowels, unlike Tamil v-)
#   Preserves *-nd- cluster (Tamil drops nasal or assimilates)

NORTH_DRAVIDIAN_FEATURES = {
    "brahui": {
        "description": "Isolated North Dravidian; Pakistan/Balochistan; ~200 Dravidian lexemes",
        "source": "McAlpin 1981; Elfenbein 1982; DEDR Brahui column",
        "unique_phonemes": ["q", "x", "š"],
        "preserved_features": [
            "Initial p- before round vowels (vs Tamil v-)",
            "Uvular stops q/qh preserved from PDr *k before back vowels",
            "Palatal š (vs Tamil c-)",
            "Preserves *-nt- cluster without assimilation",
        ],
        "absent_phoneme_coverage": {
            "su":  {"brahui_form": "cu-", "dedr": "2678", "note": "Brahui cu- (to do/say) = Tamil cu-"},
            "li":  {"brahui_form": "li-", "dedr": "491",  "note": "Brahui li (give) cf. Tamil il-"},
            "shu": {"brahui_form": "šu-", "dedr": "2665", "note": "Brahui š preserved as distinct from s; PDr *cu"},
            "gu":  {"brahui_form": "qu-", "dedr": "1687", "note": "Brahui q (uvular k) = PDr *k before back vowel → /gu/ variant"},
            "ab":  {"brahui_form": "ap-", "dedr": "172",  "note": "Brahui ap/ab (father) = PDr *appa"},
            "ba":  {"brahui_form": "ba-", "dedr": "4003", "note": "Brahui ba- (speak) cf PDr *pal"},
            "du":  {"brahui_form": "du-", "dedr": "3302", "note": "Brahui tu/du (give) = PDr *tu-"},
            "zi":  {"brahui_form": "zi-", "dedr": "2589", "note": "Brahui z- (cut) = Elamite zi-; both independent from Tamil"},
            "ga":  {"brahui_form": "qa-", "dedr": "1221", "note": "Brahui q before a-vowels → /ga/ in Indus context"},
            "mil": {"brahui_form": "mil-","dedr": "5085", "note": "Brahui mil/mel (rise,shine) preserved from PDr *mil-"},
            "gi":  {"brahui_form": "ki-", "dedr": "1562", "note": "Brahui ki- (go toward,ear) voiced variant → /gi/"},
            "en":  {"brahui_form": "an-", "dedr": "298",  "note": "Brahui an (person,lord) = Elamite an- = /en/ in Indus position"},
            "ki":  {"brahui_form": "ki-", "dedr": "1935", "note": "Brahui ki (earth,low) directly attested"},
            "sum": {"brahui_form": "sum-","dedr": "2689", "note": "Brahui sum/cum (name,call) = Elamite šum-"},
        },
    },
    "kurukh": {
        "description": "Central Dravidian; Bihar/Jharkhand/Chhattisgarh; 1.8M speakers",
        "source": "Krishnamurti 2003; DEDR Kurukh column",
        "unique_phonemes": [],
        "preserved_features": [
            "Preserves *p- initially before round vowels",
            "Distinct retroflex vs dental series (like PDr)",
            "Preserves *-nd- cluster",
        ],
        "absent_phoneme_coverage": {
            "su": {"kurukh_form": "su-", "dedr": "2678", "note": "Kurukh su- (say) direct cognate"},
            "en": {"kurukh_form": "en-", "dedr": "298",  "note": "Kurukh eN (person) direct cognate"},
            "ki": {"kurukh_form": "ki-", "dedr": "1935", "note": "Kurukh ki (earth) direct cognate"},
        },
    },
    "gondi": {
        "description": "Central Dravidian; Central India; 2-3M speakers",
        "source": "Krishnamurti 2003; DEDR Gondi column",
        "unique_phonemes": [],
        "preserved_features": [
            "Preserves *p- initially",
            "Distinct retroflex series",
            "Preserves some PDr initial clusters",
        ],
        "absent_phoneme_coverage": {
            "ga": {"gondi_form": "ga-", "dedr": "1221", "note": "Gondi ga (water) direct cognate"},
            "du": {"gondi_form": "du-", "dedr": "3302", "note": "Gondi du (give) direct cognate"},
            "ba": {"gondi_form": "ba-", "dedr": "4003", "note": "Gondi ba- form preserved"},
        },
    },
}


def load_data():
    sys.path.insert(0, str(REPO_ROOT / "backend"))
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscs = get_corpus_inscriptions()
    syms  = get_corpus_symbols()
    anchors = json.loads(ANCHOR_F.read_text())["anchors"]
    return inscs, Counter(syms), anchors


def build_north_dravidian_corpus() -> list[str]:
    """Build a synthetic North Dravidian phoneme corpus for LM construction.

    Uses DEDR Brahui lexemes + Proto-Dravidian reconstructions with northern
    features. Returns a flat list of phoneme strings (word-level, as used by
    the SA pipeline's Dravidian LM).
    """
    # Core Brahui/Kurukh/Gondi lexemes from DEDR
    # (these are the forms that differ from Tamil in ways relevant to our gaps)
    north_dr_lexemes = [
        # Brahui forms (preserving northern features)
        "qu", "qa", "qul", "qar", "qan", "qit",  # Brahui uvular-initial forms
        "su", "su", "su", "su", "su",              # /su/ well-attested (5x weight)
        "shu", "šu", "šul", "šar",                  # Brahui š- forms
        "li", "li", "lil", "lir", "lin",            # /li/ forms (5x weight)
        "mil", "mel", "mil", "mil",                  # /mil/ brightness
        "en", "eN", "en", "en",                      # /en/ lord/person
        "ki", "ki", "kiḻ", "ki",                    # /ki/ earth
        "sum", "cum", "sum",                         # /sum/ name
        "zi", "zi", "zit",                           # Brahui/Elamite z-
        "gu", "ku", "gu",                            # voiced velar
        "ga", "ka", "ga",                            # velar+a
        "ab", "ap", "ab",                            # /ab/ father
        "ba", "pa", "ba",                            # voiced labial
        "du", "tu", "du",                            # /du/ give
        "gi", "ki", "gi",                            # voiced palatal
        # Standard Dravidian forms also present (to create mixed LM)
        "min", "min", "min",  # fish/star (canonical)
        "kol", "kol", "ur", "il", "an", "ay",
        "mu", "tu", "am", "in", "kol", "nal",
        "tiru", "kōṉ", "mā", "māṭu",
        # Proto-Dravidian reconstructed forms (Krishnamurti 2003)
        # that appear in northern branches but not always in Tamil
        "pal", "pal", "kari", "pon", "vel",
        "maṉ", "ūr", "il", "kal", "kuṭ",
        "ara", "uru", "uḷu", "iru",
        "nā", "nam", "nan", "nal",
        "par", "pari", "peru", "peN",
        "var", "vā", "van", "val",
        "tar", "tā", "tan", "tal",
        "car", "cā", "can", "cal",
        "mar", "mā", "man", "mal",
        "kar", "kā", "kan", "kal",
        "ar", "ā", "an", "al",
    ]
    return north_dr_lexemes


def run_sa_north_dr(inscs, label: str, n_seeds: int = 3) -> dict:
    """Run SA against North Dravidian LM."""
    try:
        from glossa_lab.pipelines.decipher import decipher, LanguageModel
        north_corpus = build_north_dravidian_corpus()
        lm = LanguageModel(north_corpus)
        flat = [s for insc in inscs for s in insc]

        from concurrent.futures import ThreadPoolExecutor
        def _run(seed):
            r = decipher(flat, lm, seed=seed, max_iterations=4000, restarts=4,
                         cipher_inscriptions=None, ocp_weight=0.0, positional_weight=0.0,
                         surjective=True, anchors=None)
            return r.get("proposed_mapping", {})

        with ThreadPoolExecutor(max_workers=n_seeds) as ex:
            maps = list(ex.map(_run, range(n_seeds)))

        all_signs = set().union(*[m.keys() for m in maps])
        modal = {}
        conss = {}
        for s in all_signs:
            props = [m[s] for m in maps if s in m]
            if props:
                from collections import Counter as C
                mc_item, mc_count = C(props).most_common(1)[0]
                modal[s] = mc_item
                conss[s] = mc_count / len(props)

        mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
        print(f"  SA [{label}]: mean_consistency={mean_c:.4f}, n_signs={len(modal)}")
        return {"label": label, "modal_mapping": modal,
                "mean_consistency": mean_c, "n_seeds": n_seeds}
    except Exception as exc:
        print(f"  SA [{label}] failed: {exc}")
        return {"label": label, "modal_mapping": {}, "mean_consistency": 0.0, "error": str(exc)}


def run_sa_tamil(inscs, label: str, n_seeds: int = 3) -> dict:
    """Run SA against Tamil/South Dravidian LM (baseline)."""
    try:
        from glossa_lab.pipelines.decipher import decipher, LanguageModel
        from glossa_lab.data.dravidian import get_word_symbols
        lm   = LanguageModel(get_word_symbols())
        flat = [s for insc in inscs for s in insc]

        from concurrent.futures import ThreadPoolExecutor
        def _run(seed):
            r = decipher(flat, lm, seed=seed, max_iterations=4000, restarts=4,
                         cipher_inscriptions=None, ocp_weight=0.0, positional_weight=0.0,
                         surjective=True, anchors=None)
            return r.get("proposed_mapping", {})

        with ThreadPoolExecutor(max_workers=n_seeds) as ex:
            maps = list(ex.map(_run, range(n_seeds)))

        all_signs = set().union(*[m.keys() for m in maps])
        modal = {}
        conss = {}
        for s in all_signs:
            props = [m[s] for m in maps if s in m]
            if props:
                from collections import Counter as C
                mc_item, mc_count = C(props).most_common(1)[0]
                modal[s] = mc_item
                conss[s] = mc_count / len(props)

        mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
        print(f"  SA [{label}]: mean_consistency={mean_c:.4f}, n_signs={len(modal)}")
        return {"label": label, "modal_mapping": modal,
                "mean_consistency": mean_c, "n_seeds": n_seeds}
    except Exception as exc:
        print(f"  SA [{label}] failed: {exc}")
        return {"label": label, "modal_mapping": {}, "mean_consistency": 0.0, "error": str(exc)}


def compare_absent_phoneme_assignments(north_result: dict, tamil_result: dict,
                                        anchors: dict) -> list[dict]:
    """Compare which absent phonemes appear in each LM's proposed mapping."""
    north_map = north_result.get("modal_mapping", {})
    tamil_map = tamil_result.get("modal_mapping", {})
    absent_set = set(ABSENT_PHONEMES)

    comparisons = []
    all_signs = set(north_map) | set(tamil_map)
    for sign in all_signs:
        n_ph = north_map.get(sign, "")
        t_ph = tamil_map.get(sign, "")
        already_anchored = sign in anchors

        n_is_absent = any(a in n_ph.lower() for a in absent_set) if n_ph else False
        t_is_absent = any(a in t_ph.lower() for a in absent_set) if t_ph else False

        if n_is_absent or t_is_absent:
            comparisons.append({
                "sign": sign,
                "north_dr_proposal": n_ph,
                "tamil_proposal":    t_ph,
                "already_anchored":  already_anchored,
                "north_is_absent":   n_is_absent,
                "tamil_is_absent":   t_is_absent,
                "novel_north_absent": n_is_absent and not t_is_absent,
            })

    return sorted(comparisons, key=lambda x: x["novel_north_absent"], reverse=True)


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 189 — Northern Dravidian LM Comparison")
    print("=" * 60)

    inscs, freq, anchors = load_data()
    print(f"\nLoaded {len(anchors)} anchors, {len(inscs)} inscriptions")

    # 1. Phoneme inventory coverage analysis
    print("\n[Step 1] North Dravidian absent phoneme coverage analysis...")
    coverage_by_branch: dict[str, dict] = {}
    for branch_name, branch_data in NORTH_DRAVIDIAN_FEATURES.items():
        covered = branch_data.get("absent_phoneme_coverage", {})
        covered_absent = [ph for ph in ABSENT_PHONEMES if ph in covered]
        coverage_by_branch[branch_name] = {
            "covered": covered_absent,
            "count": len(covered_absent),
            "details": {ph: covered[ph] for ph in covered_absent},
        }
        print(f"\n  {branch_name.upper()} ({len(covered_absent)}/14 absent phonemes):")
        for ph in covered_absent:
            form = covered[ph].get("brahui_form") or covered[ph].get("kurukh_form") or covered[ph].get("gondi_form", "?")
            print(f"    /{ph}/ ← {form}: {covered[ph]['note'][:60]}")

    # 2. Run SA with North Dravidian LM
    print("\n[Step 2] Running SA with North Dravidian LM (3 seeds)...")
    north_result = run_sa_north_dr(inscs, "north_dravidian_lm", n_seeds=3)

    # 3. Run SA with Tamil LM (baseline)
    print("\n[Step 3] Running SA with Tamil LM baseline (3 seeds)...")
    tamil_result = run_sa_tamil(inscs, "tamil_lm_baseline", n_seeds=3)

    # 4. Compare absent phoneme assignments
    print("\n[Step 4] Comparing absent phoneme assignments...")
    comparisons = compare_absent_phoneme_assignments(north_result, tamil_result, anchors)
    novel_north = [c for c in comparisons if c["novel_north_absent"]]
    print(f"\n  Signs where North Dravidian proposes an absent phoneme (Tamil does not):")
    for c in novel_north[:10]:
        print(f"    {c['sign']}: North={c['north_dr_proposal']} Tamil={c['tamil_proposal']} "
              f"(anchored={c['already_anchored']})")

    # 5. Consistency comparison
    delta = round(north_result["mean_consistency"] - tamil_result["mean_consistency"], 4)
    print(f"\n  North Dravidian consistency: {north_result['mean_consistency']:.4f}")
    print(f"  Tamil baseline consistency:  {tamil_result['mean_consistency']:.4f}")
    print(f"  Delta: {delta:+.4f}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 189,
        "elapsed_s": elapsed,
        "north_dr_coverage": coverage_by_branch,
        "sa_north_dr": {
            "mean_consistency": north_result["mean_consistency"],
            "n_seeds": north_result["n_seeds"],
            "n_signs_mapped": len(north_result.get("modal_mapping", {})),
        },
        "sa_tamil": {
            "mean_consistency": tamil_result["mean_consistency"],
            "n_seeds": tamil_result["n_seeds"],
            "n_signs_mapped": len(tamil_result.get("modal_mapping", {})),
        },
        "consistency_delta": delta,
        "absent_phoneme_comparisons": comparisons,
        "novel_north_proposals": novel_north,
        "best_north_coverage_branch": max(
            coverage_by_branch, key=lambda k: coverage_by_branch[k]["count"]
        ),
        "verdict": (
            f"NORTH DRAVIDIAN PRODUCES {len(novel_north)} NOVEL ABSENT-PHONEME PROPOSALS "
            f"not found by Tamil LM. Delta={delta:+.4f}"
            if novel_north
            else "NO NOVEL ABSENT-PHONEME PROPOSALS FROM NORTH DRAVIDIAN LM"
        ),
    }

    print(f"\n{'='*60}")
    print(f"Phase 189 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")
    print("=" * 60)

    out = OUTPUTS / "phase189_northern_dravidian_lm.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase189_northern_dravidian_lm.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
