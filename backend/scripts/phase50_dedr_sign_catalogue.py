"""Phase-50: DEDR Sign Depiction Catalogue.

For each IVC sign whose depiction is known (animal, tool, plant, object),
scan DEDR for the Proto-Dravidian word for that object. The initial syllable
of that word = the rebus phoneme value for that sign.

This extends Phase-47 T1 (which did 7 HIGH anchors) to ALL identifiable signs.

Sign depictions come from:
  1. The phase28b phoneme_map (Parpola/Laursen readings already in JSON)
  2. The allograph_families.json (Holdat sign descriptions)
  3. The MEDIUM anchor readings (already have Dravidian word assignments)

IVC sign depiction inventory (from Parpola 1994 sign catalogue):
  Animals: unicorn, zebu, elephant, rhinoceros, tiger, buffalo, fish, gharial,
           hare, bird, snake, scorpion, squirrel, antelope, bison, ram, bull
  Tools:   hammer/kol, comb, jar/pot, bow, arrow, yoke, plough, sickle, net
  Plants:  pipal/fig, branch, grass, trough/manger, root
  Geometry: chevron, cross, circle, grid, dot, stroke (numerical)
  Humans:  human figure, seated figure, deity (horned)

GPU: torch for cosine similarity matrix over DEDR word embeddings (TF-IDF approx).

Output: reports/phase50_dedr_sign_catalogue.json
"""
from __future__ import annotations
import csv, json, math, re
from collections import Counter
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None; DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

REPO     = Path(__file__).parents[2]
DEDR     = REPO / "reports/jambu-dedr/data/dedr/dedr_new.csv"
ANCHORS  = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
CW       = REPO / "reports/phase28b_mahadevan_crosswalk.json"
ALLOGRAPH = REPO / "reports/allograph_families.json"
REPORTS  = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT      = REPORTS / "phase50_dedr_sign_catalogue.json"

# Known sign depictions → search terms for DEDR
# Format: {M_number: [depiction_terms, ...]}  OR {parpola_num: [...]}
SIGN_DEPICTIONS = {
    # Confirmed HIGH anchors (for reference)
    "M006": ["tiger", "puli", "leopard"],
    "M016": ["calf", "kaliru", "young elephant"],
    "M045": ["elephant", "yanai"],
    "M062": ["bull", "zebu", "eru", "ox"],
    "M099": ["hammer", "kol", "chisel", "forge"],
    "M176": ["male", "man", "an", "masculine"],
    "M342": ["pronoun", "suffix", "ay"],
    # MEDIUM anchors — verify Dravidian attestation
    "M047": ["fish", "min", "meen"],
    "M073": ["king", "kon", "chief"],
    "M013": ["town", "ur", "settlement"],
    "M060": ["rhinoceros", "erumai", "buffalo"],
    # Key unread signs — attempt DEDR match
    "M211": ["unicorn", "kol", "one-horn"],    # the most common motif
    "M293": ["comb", "vil", "teeth"],           # comb-like sign
    "M065": ["jar", "pot", "kuTam"],
    "M125": ["bow", "vil", "arrow"],
    "M087": ["pipal", "fig", "tree", "arasu"],
    "M249": ["scorpion", "tee", "teel"],
    "M220": ["bison", "erumai", "buffalo"],
    "M305": ["seated figure", "iru", "sit"],
    "M367": ["squirrel", "pilLai", "rat"],
    "M233": ["dot", "oru", "one", "point"],
    # Parpola sign mappings (from phoneme_map)
    "P001": ["man", "person", "aal"],
    "P099": ["bow", "vil"],
    "P086": ["one", "oru", "single"],
    "P087": ["two", "iru", "white"],
    "P091": ["six", "aru"],
    "P092": ["seven", "elu"],
    "P124": ["pot", "kuTam"],
    "P175": ["spindle", "katir"],
    "P261": ["circle", "muruku"],
    "P264": ["female", "pen"],
    "P281": ["squirrel", "piLLai"],
    "P311": ["fig star", "vaTa miin", "north"],
}

# DEDR search — normalize and search
def norm(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower())


def load_dedr_entries() -> list[dict]:
    entries = []
    try:
        with open(DEDR, encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                if len(row) >= 4:
                    lang = row[0].strip()
                    word = row[2].strip()
                    gloss = row[3].strip()
                    if word and gloss:
                        entries.append({
                            "lang": lang, "word": word.lower(),
                            "gloss": gloss.lower(),
                            "word_norm": norm(word),
                        })
    except Exception as e:
        print(f"  DEDR load warning: {e}")
    return entries


def search_dedr(terms: list[str], dedr_entries: list[dict], top_k: int = 5) -> list[dict]:
    """Find DEDR entries matching any of the search terms."""
    results = []
    seen = set()
    for term in terms:
        t = norm(term)
        for entry in dedr_entries:
            w = entry["word_norm"]
            g = norm(entry["gloss"])
            if (t in w or t in g or w[:3] == t[:3]) and w not in seen:
                seen.add(w)
                results.append({**entry, "search_term": term})
                if len(results) >= top_k * len(terms):
                    break
    # Score by relevance: exact gloss match first
    results.sort(key=lambda x: (
        -sum(1 for t in terms if norm(t) in norm(x["gloss"])),
        len(x["word"]),
    ))
    return results[:top_k]


def extract_rebus_phoneme(word: str) -> str:
    """Extract initial syllable (rebus phoneme) from a Tamil/Dravidian word."""
    word = word.lower().strip()
    word = re.sub(r"[^a-zāīūēōḍṭṇṅñḷṟṉ]", "", word)
    if not word:
        return "?"
    vowels = set("aāiīuūeēoōai")
    # Find first vowel
    for i, c in enumerate(word):
        if c in vowels:
            # Return consonants before vowel + vowel + optional coda
            end = i + 1
            if end < len(word) and word[end] not in vowels and (end+1 >= len(word) or word[end+1] in vowels):
                end += 1  # include coda consonant
            return word[:end]
    return word[:2]  # fallback


def compute_gpu_similarity(sign_ids: list[str], phonemes: list[str]) -> list[tuple]:
    """GPU: compute pairwise phoneme distance matrix to identify sign clusters."""
    if torch is None or not phonemes:
        return []
    # Build char frequency vectors
    chars = sorted(set(c for p in phonemes for c in p))
    char_idx = {c: i for i, c in enumerate(chars)}
    n = len(phonemes)
    d = len(chars)
    mat = torch.zeros(n, d, device=DEVICE)
    for i, p in enumerate(phonemes):
        for c in p:
            if c in char_idx:
                mat[i, char_idx[c]] += 1.0
    # Cosine similarity
    norms = mat.norm(dim=1, keepdim=True).clamp(min=1e-8)
    mat_n = mat / norms
    sim = (mat_n @ mat_n.T).cpu()
    # Find most similar pairs
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            pairs.append((sign_ids[i], phonemes[i], sign_ids[j], phonemes[j], float(sim[i,j])))
    pairs.sort(key=lambda x: -x[4])
    return pairs[:10]


def main() -> None:
    print("Phase-50: DEDR Sign Depiction Catalogue\n")

    dedr_entries = load_dedr_entries()
    print(f"  DEDR entries: {len(dedr_entries)}")

    phoneme_map = json.loads(CW.read_text("utf-8")).get("phoneme_map", {})
    anchors_all = json.loads(ANCHORS.read_text("utf-8"))["anchors"]

    catalogue = []
    for sign_id, terms in SIGN_DEPICTIONS.items():
        matches = search_dedr(terms, dedr_entries, top_k=3)
        best_word = matches[0]["word"] if matches else "?"
        best_gloss = matches[0]["gloss"] if matches else "?"
        rebus = extract_rebus_phoneme(best_word) if best_word != "?" else "?"

        # Check if already in anchors
        existing = anchors_all.get(sign_id, {})
        conf = existing.get("confidence", "UNREAD") if existing else "UNREAD"
        existing_reading = existing.get("reading", "") if existing else ""

        # Cross-check with phoneme_map (Parpola)
        p_num = sign_id.replace("P","").replace("M","")
        parpola_entry = phoneme_map.get(p_num, {})
        parpola_phoneme = parpola_entry.get("phoneme", "")

        agree = (rebus[:2] == existing_reading[:2]) if existing_reading and rebus != "?" else None

        print(f"  {sign_id:6s} terms={terms[0]:15s} best_match={best_word!r:15s} "
              f"rebus={rebus!r:8s} existing={existing_reading!r:10s} "
              f"parpola={parpola_phoneme!r:10s} agree={agree}")

        catalogue.append({
            "sign_id": sign_id,
            "depiction_terms": terms,
            "best_dedr_word": best_word,
            "best_dedr_gloss": best_gloss,
            "rebus_phoneme": rebus,
            "existing_reading": existing_reading,
            "existing_confidence": conf,
            "parpola_phoneme": parpola_phoneme,
            "dedr_matches": matches[:3],
            "rebus_agrees_with_existing": agree,
        })

    # GPU: similarity matrix over rebus phonemes
    sign_ids = [c["sign_id"] for c in catalogue if c["rebus_phoneme"] != "?"]
    phonemes = [c["rebus_phoneme"] for c in catalogue if c["rebus_phoneme"] != "?"]
    similar_pairs = compute_gpu_similarity(sign_ids, phonemes)
    if similar_pairs:
        print(f"\n[GPU:{DEVICE}] Top phoneme-similar sign pairs:")
        for s1, p1, s2, p2, sim in similar_pairs[:5]:
            print(f"  {s1}({p1!r}) ~ {s2}({p2!r}) = {sim:.3f}")

    # New candidate readings (unread signs with good DEDR match)
    new_candidates = [c for c in catalogue
                      if c["existing_confidence"] in ("UNREAD", "LOW")
                      and c["rebus_phoneme"] != "?"
                      and c["best_dedr_word"] != "?"]
    print(f"\nNew candidate readings for unread/LOW signs: {len(new_candidates)}")
    for c in new_candidates:
        print(f"  {c['sign_id']}: {c['best_dedr_word']!r} → rebus={c['rebus_phoneme']!r}")

    result = {
        "_citation": {"primary": ["A.1", "A.13"], "dedr": "DEDR Burrow & Emeneau",
                      "parpola": "Parpola 1994"},
        "gpu_device": DEVICE,
        "n_signs_catalogued": len(catalogue),
        "n_new_candidates": len(new_candidates),
        "catalogue": catalogue,
        "new_rebus_candidates": new_candidates,
        "similar_sign_pairs": [{"s1": s1, "p1": p1, "s2": s2, "p2": p2, "sim": sim}
                               for s1, p1, s2, p2, sim in similar_pairs[:10]],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
