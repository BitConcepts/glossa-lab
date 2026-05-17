"""Phase-49: Tamil Syllabic Language Model Construction.

The 944-bigram char LM (68 single-char tokens) cannot test multi-char
syllabic readings like ā/āl, ēḷ, il/iḷ, ūr, kōṉ, etc. This script
builds a SYLLABIC bigram LM over Tamil text where each token is a CV/CVC
syllable (the natural unit of a logo-syllabic script like Indus).

Sources:
  - TamilTB.v0.1.utf8.tt (435KB, 13k+ word tokens)
  - TamilTB.v0.1.utf8.conll (744KB, morphologically annotated)
  - DEDR phonological forms (*Proto-Dravidian reconstructions)
  - Existing MEDIUM anchor readings as seed syllables

Tamil syllabification:
  - Each syllable = onset consonant(s) + vowel nucleus (+ optional coda)
  - In romanized Tamil: CV = consonant + vowel; CVC = C+V+C
  - Vowel inventory: a ā i ī u ū e ē ai o ō au ṃ
  - Handle Tamil Unicode (U+0B80–U+0BFF) and romanized forms both

Output: backend/glossa_lab/data/dravidian_syllabic_lm.json
        reports/phase49_syllabic_lm.json (stats)
"""
from __future__ import annotations
import json, re, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None; DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

REPO     = Path(__file__).parents[2]
TB_TT    = REPO / "corpora/downloads/external_repos/Kee2u_Indus_Decipherment/TamilTB.v0.1/data/TamilTB.v0.1.utf8.tt"
TB_CONLL = REPO / "corpora/downloads/external_repos/Kee2u_Indus_Decipherment/TamilTB.v0.1/data/TamilTB.v0.1.utf8.conll"
DEDR     = REPO / "reports/jambu-dedr/data/dedr/dedr_new.csv"
ANCHORS  = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
DATA_OUT = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
REPORTS  = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT      = REPORTS / "phase49_syllabic_lm.json"

# ── Tamil vowels (romanized and Unicode) ────────────────────────────────────
VOWELS_ROM = set("aāiīuūeēoōai au".split() + list("aāiīuūeē oō"))
VOWELS_CHARS = set("aāiīuūeēoōai")  # romanized vowel chars
# Tamil Unicode vowels (independent vowels + matras)
TAMIL_VOWELS = set(
    "\u0B85\u0B86\u0B87\u0B88\u0B89\u0B8A\u0B8E\u0B8F\u0B90"
    "\u0B92\u0B93\u0B94"  # independent vowels
    "\u0BBE\u0BBF\u0BC0\u0BC1\u0BC2\u0BC6\u0BC7\u0BC8\u0BCA\u0BCB\u0BCC"  # matras
    "\u0BCD"  # virama (vowel killer)
)
TAMIL_CONSONANTS = set(
    "\u0B95\u0B99\u0B9A\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8\u0BAA\u0BAE"
    "\u0BAF\u0BB0\u0BB2\u0BB5\u0BB3\u0BB4\u0BB1\u0BA9\u0BA4\u0BAF"
)


def syllabify_roman(word: str) -> list[str]:
    """Segment a romanized Tamil/Dravidian word into CV syllables."""
    word = word.lower().strip()
    word = re.sub(r"[^a-zāīūēōḍṭṇṅñḷṟṉ]", "", word)
    if not word:
        return []
    syllables = []
    i = 0
    n = len(word)
    while i < n:
        # Try 2-char consonant cluster first (ṭh, ṅk, etc.) — simplified
        c_start = i
        # Consume consonants until we hit a vowel
        while i < n and word[i] not in VOWELS_CHARS:
            i += 1
        # Consume the vowel nucleus (possibly 2 chars for ā, ī, etc.)
        v_start = i
        if i < n:
            i += 1  # consume vowel char
            # Long vowels represented by ā, ī, ū etc. are single chars here
        # Consume optional coda consonant (before next vowel)
        if i < n and word[i] not in VOWELS_CHARS and i+1 < n and word[i+1] in VOWELS_CHARS:
            # If next-next char is a vowel, this consonant starts next syllable
            pass
        elif i < n and word[i] not in VOWELS_CHARS:
            # Coda: include in this syllable
            i += 1
        syl = word[c_start:i]
        if syl:
            syllables.append(syl)
    return [s for s in syllables if len(s) >= 1]


def syllabify_tamil_unicode(word: str) -> list[str]:
    """Segment a Tamil Unicode word into syllables."""
    syllables = []
    current = ""
    i = 0
    while i < len(word):
        ch = word[i]
        # Consonant
        if ch in TAMIL_CONSONANTS:
            if current:
                # Check if virama follows (consonant cluster)
                if i+1 < len(word) and word[i+1] == "\u0BCD":
                    current += ch + word[i+1]
                    i += 2
                    continue
                # Else: start new syllable
                syllables.append(current); current = ""
            current += ch
        elif ch in TAMIL_VOWELS:
            current += ch
        elif unicodedata.category(ch) in ("Lo", "Mn"):
            current += ch
        else:
            if current: syllables.append(current); current = ""
        i += 1
    if current: syllables.append(current)
    return [s for s in syllables if s]


def extract_syllables_from_word(word: str) -> list[str]:
    """Auto-detect Tamil Unicode vs romanized and syllabify."""
    if any(ord(c) > 0x0B7F for c in word):
        return syllabify_tamil_unicode(word)
    return syllabify_roman(word)


def parse_tamiltb_tt(path: Path) -> list[str]:
    words = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.strip().split("\t")
            if parts:
                w = parts[0].strip()
                if w and len(w) > 1 and not re.match(r"^[\d.,;:!?()\"\s]+$", w):
                    words.append(w)
    return words


def parse_tamiltb_conll(path: Path) -> list[str]:
    words = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = line.split("\t")
            if len(parts) >= 3:
                form = parts[1].strip()
                if form and len(form) > 1 and not re.match(r"^[\d.,;:!?()\"\s]+$", form):
                    words.append(form)
    return words


def load_dedr_words(path: Path) -> list[str]:
    words = []
    try:
        import csv
        with open(path, encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                if len(row) > 2:
                    w = row[2].strip()
                    if w and len(w) > 1 and not re.match(r"^[\d.,;:!?()\"\s]+$", w):
                        words.append(w)
    except Exception:
        pass
    return words


def load_anchor_readings(path: Path) -> list[str]:
    """Use existing anchor readings as seed syllables."""
    try:
        anchors = json.loads(path.read_text("utf-8"))["anchors"]
        words = []
        for v in anchors.values():
            r = v.get("reading", "")
            if r: words.append(r)
        return words
    except Exception:
        return []


def build_syllabic_lm(all_words: list[str]) -> tuple[dict, dict]:
    """Build bigram LM over syllables extracted from words."""
    bigram_counts: Counter = Counter()
    syllable_counts: Counter = Counter()
    n_words = 0

    for word in all_words:
        sylls = extract_syllables_from_word(word)
        if len(sylls) < 2: continue
        n_words += 1
        for s in sylls:
            syllable_counts[s] += 1
        for i in range(len(sylls) - 1):
            bigram_counts[(sylls[i], sylls[i+1])] += 1

    # Keep only syllables with count >= 2
    valid_sylls = {s for s, c in syllable_counts.items() if c >= 2}
    filtered_bigrams: Counter = Counter()
    for (a, b), c in bigram_counts.items():
        if a in valid_sylls and b in valid_sylls:
            filtered_bigrams[(a, b)] += c

    total = sum(filtered_bigrams.values()) or 1
    prob = {f"{a},{b}": c/total for (a,b),c in filtered_bigrams.items()}

    return prob, dict(syllable_counts)


def main() -> None:
    print("Phase-49: Tamil Syllabic LM Construction\n")

    # Load all word sources
    print("Loading TamilTB .tt…")
    tt_words = parse_tamiltb_tt(TB_TT)
    print(f"  {len(tt_words)} word tokens from TamilTB .tt")

    print("Loading TamilTB CoNLL…")
    conll_words = parse_tamiltb_conll(TB_CONLL)
    print(f"  {len(conll_words)} word tokens from CoNLL")

    print("Loading DEDR words…")
    dedr_words = load_dedr_words(DEDR)
    print(f"  {len(dedr_words)} word tokens from DEDR")

    print("Loading anchor readings…")
    anchor_words = load_anchor_readings(ANCHORS)
    print(f"  {len(anchor_words)} readings from anchors")

    all_words = tt_words + conll_words + dedr_words + anchor_words
    all_words = list(dict.fromkeys(all_words))  # deduplicate
    print(f"\nTotal unique words for syllabification: {len(all_words)}")

    # Build syllabic LM
    print("Building syllabic bigram LM…")
    bigram_prob, syllable_freq = build_syllabic_lm(all_words)

    n_syllables = len(syllable_freq)
    n_bigrams   = len(bigram_prob)
    print(f"  Unique syllables: {n_syllables}")
    print(f"  Bigrams:          {n_bigrams}")

    # GPU: build probability tensor for analysis
    if torch is not None:
        sylls = sorted(syllable_freq.keys())
        sidx  = {s: i for i, s in enumerate(sylls)}
        n = len(sylls)
        mat = torch.zeros(n, n, device=DEVICE)
        for key, p in bigram_prob.items():
            a, b = key.split(",", 1)
            if a in sidx and b in sidx:
                mat[sidx[a], sidx[b]] = float(p)
        # Top bigrams
        flat = mat.view(-1)
        top_idx = flat.topk(10).indices.cpu().tolist()
        top_bigrams = []
        for idx in top_idx:
            i, j = idx // n, idx % n
            top_bigrams.append((sylls[i], sylls[j], float(flat[idx])))
        print(f"[GPU:{DEVICE}] LM matrix {n}×{n} built")
        print(f"  Top bigrams: {top_bigrams[:5]}")
    else:
        top_bigrams = sorted(bigram_prob.items(), key=lambda x: -x[1])[:5]
        top_bigrams = [(k.split(",",1)[0], k.split(",",1)[1], v) for k,v in top_bigrams]

    # Sample syllable inventory (first 50)
    top_sylls = sorted(syllable_freq.items(), key=lambda x: -x[1])[:50]
    print(f"\n  Top syllables: {[s for s,_ in top_sylls[:20]]}")

    # Save LM
    lm_data = {
        "description": "Tamil syllabic bigram LM — CV/CVC syllables from TamilTB + DEDR",
        "sources": ["TamilTB.v0.1 (.tt + CoNLL)", "DEDR new.csv", "INDUS_FINAL_ANCHORS readings"],
        "n_words": len(all_words),
        "n_syllables": n_syllables,
        "n_bigrams": n_bigrams,
        "bigrams": bigram_prob,
        "syllable_freq": {s: c for s, c in sorted(syllable_freq.items(), key=lambda x: -x[1])[:500]},
        "top_bigrams": top_bigrams[:20],
    }
    DATA_OUT.write_text(json.dumps(lm_data, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nLM saved: {DATA_OUT}")

    result = {
        "_citation": {"primary": ["A.1"], "tamiltb": "TamilTB.v0.1", "dedr": "DEDR Burrow & Emeneau"},
        "gpu_device": DEVICE,
        "n_source_words": len(all_words),
        "n_syllables": n_syllables,
        "n_bigrams": n_bigrams,
        "top_syllables": [s for s,_ in top_sylls[:30]],
        "top_bigrams": top_bigrams[:10],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
