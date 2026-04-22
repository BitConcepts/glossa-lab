"""Inscription reading attempt: apply anchor mapping to CISI, find candidate Dravidian words.

Run via: shell.cmd python backend/scripts/attempt_readings.py

Loads the 10-anchor proposed mapping from reports/indus_cisi_anchored_10.json,
applies it to each CISI inscription, and identifies:
  1. Fully-readable inscriptions (all signs in anchor set)
  2. Partially-readable inscriptions (>= 50% anchored)
  3. Candidate Dravidian word matches for readable sequences
"""
import sys, json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent))

REPORTS = Path(__file__).parent.parent.parent / "reports"

# ── Known Dravidian words (Proto-Dravidian roots, DEDR) ──────────────────────
# Format: phoneme_string -> [gloss, ...]
DRAVIDIAN_WORDS = {
    # 3-char words (most likely to appear in ~5-sign inscriptions)
    "kan": ["eye (Tamil: kan)", "black (Tamil: kar/kan)"],
    "kal": ["stone, rock (Tamil: kal)", "to learn (Tamil: kal)"],
    "val": ["strong, power (Tamil: val)"],
    "pal": ["tooth, many, milk (Tamil: pal)"],
    "mul": ["thorn, point (Tamil: mul)"],
    "kul": ["family, pond, clan (Tamil: kul/kulam)"],
    "pul": ["grass, low (Tamil: pul)"],
    "nar": ["good, noble (Tamil: nar)"],
    "man": ["earth, sand (Tamil: man/mannu)"],
    "van": ["strong, sky (Tamil: van)"],
    "par": ["to see, rock (Tamil: par)"],
    "var": ["to come (Tamil: var)"],
    "mar": ["tree, change (Tamil: mar/maram)"],
    "kar": ["black, cloud (Tamil: kar)"],
    "nar": ["noble, good (Tamil: nal/nar)"],
    "pan": ["work, make, pig (Tamil: pan)"],
    "min": ["fish, star (Tamil: min/meen)"],
    "vil": ["bow, price (Tamil: vil)"],
    "kil": ["below, east, parrot (Tamil: kil)"],
    "nir": ["water (Tamil: nir/neer)"],
    "pur": ["city, outside (Tamil: pur)"],
    "kur": ["short, horse (Tamil: kur)"],
    "vel": ["spear, white, victory (Tamil: vel)"],
    "nel": ["rice paddy (Tamil: nel)"],
    "pol": ["like, gold (Tamil: pol/pon)"],
    "kol": ["kill, take, bull (Tamil: kol)"],
    "tal": ["head, self (Tamil: tal/talai)"],
    "nul": ["thread, book (Tamil: nul)"],
    "ver": ["root, victory (Tamil: ver)"],
    # 4-char words
    "kani": ["fruit, ripe (Tamil: kani)"],
    "mani": ["bead, gem, bell (Tamil: mani)"],
    "mali": ["full, abundant (Tamil: mali)"],
    "vali": ["strong, path (Tamil: vali)"],
    "kari": ["elephant, black (Tamil: kari/yane)"],
    "puli": ["tiger, leopard (Tamil: puli)"],
    "kali": ["joy, liquor (Tamil: kali)"],
    "nali": ["vessel (Tamil: nali)"],
    "vari": ["line, tax (Tamil: vari)"],
    "para": ["rock, fly (Tamil: para)"],
    "kara": ["hand, shore (Tamil: kara)"],
    "mara": ["tree (Tamil: mara/maram)"],
    "paru": ["large (Tamil: paru)"],
    "kanu": ["to see, eye (Tamil: kanu)"],
    "minu": ["lightning (Tamil: minu)"],
    "kalu": ["heel, time (Tamil: kalu)"],
    "vanu": ["sky (Tamil: vanu/vanam)"],
    "kari": ["black, charcoal (Tamil: kari)"],
    "vari": ["stripe, spread (Tamil: vari)"],
    "niru": ["standing (Tamil: niru)"],
    # 5-char words
    "kallu": ["stone (emphatic Tamil: kal+lu)"],
    "kannu": ["eye (emphatic Tamil: kan+nu)"],
    "mannu": ["earth, permanent (Tamil: mannu)"],
    "vannu": ["came (Tamil: vannu)"],
    "pallu": ["tooth (emphatic: pal+lu)"],
    "mullu": ["thorn (emphatic: mul+lu)"],
    "vallu": ["arrow (Tamil: vallu)"],
    "pullu": ["grass (emphatic: pul+lu)"],
    "karpu": ["chastity (Tamil: karpu)"],
    "marpu": ["chest (Tamil: marpu)"],
    "nalpu": ["goodness (Tamil: nalpu)"],
}

def apply_mapping(seq, mapping):
    """Apply sign-to-phoneme mapping to a sequence. Returns (phonemes, coverage%)."""
    phonemes = []
    anchored = 0
    for sign in seq:
        p = mapping.get(sign)
        if p:
            phonemes.append(p)
            anchored += 1
        else:
            phonemes.append("?")
    coverage = anchored / len(seq) if seq else 0
    return phonemes, coverage


def find_dravidian_matches(phoneme_str):
    """Find Dravidian words that match or contain the phoneme string."""
    matches = []
    # Exact match
    if phoneme_str in DRAVIDIAN_WORDS:
        matches.append({"word": phoneme_str, "glosses": DRAVIDIAN_WORDS[phoneme_str], "type": "exact"})
    # Substring match (word is contained in the phoneme string)
    for word, glosses in DRAVIDIAN_WORDS.items():
        if len(word) >= 3 and word in phoneme_str and word != phoneme_str:
            matches.append({"word": word, "glosses": glosses, "type": "substring"})
    # Check if phoneme string is a prefix of any Dravidian word
    for word, glosses in DRAVIDIAN_WORDS.items():
        if len(phoneme_str) >= 2 and word.startswith(phoneme_str) and word != phoneme_str:
            matches.append({"word": word, "phoneme_prefix": phoneme_str, "glosses": glosses, "type": "prefix"})
    return matches


def main():
    # Load 10-anchor mapping
    result_file = REPORTS / "indus_cisi_anchored_10.json"
    if not result_file.exists():
        print("ERROR: reports/indus_cisi_anchored_10.json not found.")
        print("Run: shell.cmd python -m glossa_lab.experiments indus_cisi_anchored_10")
        sys.exit(1)

    result = json.loads(result_file.read_text())
    data = result.get("data", result)

    # Extract proposed mapping — keys are "c__P***"
    mapping = {}
    for k, v in data.items():
        if k.startswith("c__") and isinstance(v, str):
            sign = k[3:]   # "P324"
            mapping[sign] = v

    if not mapping:
        print("No mapping found in result. Keys:", list(data.keys())[:20])
        sys.exit(1)

    print(f"Loaded mapping: {len(mapping)} signs mapped")
    # Show anchored signs
    anchored = {s: p for s,p in mapping.items() if p != "a"}
    print(f"Non-'a' mappings ({len(anchored)}): {dict(list(sorted(anchored.items()))[:30])}")

    # Load CISI corpus
    corpus_file = Path(__file__).parent.parent.parent / "data" / "indus_cisi_corpus.json"
    if not corpus_file.exists():
        print("ERROR: data/indus_cisi_corpus.json not found. Run scripts/download_indus_cisi.py")
        sys.exit(1)

    corpus = json.loads(corpus_file.read_text())
    print(f"CISI corpus: {len(corpus)} inscriptions")

    # Apply mapping to each inscription
    full_reads = []
    partial_reads = []
    all_phoneme_seqs = []

    for insc in corpus:
        insc_id = insc.get("id", "?")
        signs = [g["id"] for g in insc.get("graphemes", []) if g.get("id")]
        if len(signs) < 2:
            continue

        phonemes, coverage = apply_mapping(signs, mapping)
        phoneme_str = "".join(p for p in phonemes if p != "?")
        full_str = "".join(phonemes)  # includes ?

        entry = {
            "id": insc_id,
            "signs": signs,
            "phonemes": phonemes,
            "phoneme_string": phoneme_str,
            "full_string": full_str,
            "coverage": round(coverage, 2),
            "n_signs": len(signs),
        }

        matches = find_dravidian_matches(phoneme_str) if phoneme_str else []
        if matches:
            entry["dravidian_matches"] = matches

        if coverage >= 1.0:
            full_reads.append(entry)
        elif coverage >= 0.5:
            partial_reads.append(entry)

        all_phoneme_seqs.append(entry)

    print(f"\nFully readable inscriptions (all signs anchored): {len(full_reads)}")
    for r in full_reads:
        print(f"  {r['id']:8s}  {r['signs']}  ->  '{r['phoneme_string']}'", end="")
        if r.get("dravidian_matches"):
            print(f"  [{', '.join(m['word']+':'+m['glosses'][0] for m in r['dravidian_matches'][:2])}]")
        else:
            print()

    print(f"\nPartially readable inscriptions (>=50% anchored): {len(partial_reads)}")
    for r in sorted(partial_reads, key=lambda x: -x["coverage"])[:20]:
        print(f"  {r['id']:8s}  {r['full_string']:20s}  ({r['coverage']*100:.0f}% cov)", end="")
        if r.get("dravidian_matches"):
            print(f"  [{r['dravidian_matches'][0]['word']}: {r['dravidian_matches'][0]['glosses'][0]}]")
        else:
            print()

    # Statistics on phoneme sequences
    phoneme_bigrams = Counter()
    for r in all_phoneme_seqs:
        s = r["phoneme_string"]
        for i in range(len(s) - 1):
            if s[i] != "?" and s[i+1] != "?":
                phoneme_bigrams[(s[i], s[i+1])] += 1

    print(f"\nTop 15 phoneme bigrams from anchored signs:")
    for (a, b), n in phoneme_bigrams.most_common(15):
        print(f"  {a}->{b}  n={n}")

    # Save results
    out = REPORTS / "indus_reading_attempt.json"
    out.write_text(json.dumps({
        "n_inscriptions": len(all_phoneme_seqs),
        "n_fully_readable": len(full_reads),
        "n_partially_readable": len(partial_reads),
        "mapping_size": len(mapping),
        "n_non_a_mappings": len(anchored),
        "non_a_mapping": anchored,
        "fully_readable": full_reads,
        "top_partial": sorted(partial_reads, key=lambda x: -x["coverage"])[:30],
        "top_phoneme_bigrams": [(f"{a}->{b}", n) for (a,b),n in phoneme_bigrams.most_common(20)],
    }, indent=2, default=str))
    print(f"\nSaved -> reports/indus_reading_attempt.json")


if __name__ == "__main__":
    main()
