"""Phase-111 custodian (spec 009 section 6).

Builds the blinded panel: loads every panel corpus, applies the
frozen unit/text rules, generates the synthetic controls, remaps
tokens to anonymous integers, resamples draws, extracts features
(via phase111_features), and writes:
  - the anonymized panel file (IDs C01.., labels only for KNOWN
    corpora, no names anywhere), and
  - the ID -> identity key, which lives ONLY in the gitignored
    runtime state dir (.glossa-state/phase111/) until unblinding.

The analyst module never imports this module.

Frozen constants (seeds, sizes, orders) are from spec 009 sections
1-5. Changing them after the spec freeze is a spec deviation
(spec section 11).

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

import csv
import json
import sqlite3
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from glossa_lab.phase111_features import FEATURE_NAMES, extract_features

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES = REPO_ROOT / "glossa-corpus" / "indus" / "sources" / "phase111"
DATA = REPO_ROOT / "backend" / "glossa_lab" / "data"
STATE_DIR = REPO_ROOT / ".glossa-state" / "phase111"

MASTER_SEED = 20261006
N_PRIMARY = 11_000
N_SENSITIVITY = (5_000, 19_600)
N_DRAWS = 100

# Frozen target length distribution: Holdat empirical (spec section 2).
TARGET_LEN_DIST: dict[int, int] = {2: 269, 3: 330, 4: 415, 5: 330, 6: 164, 7: 116, 8: 46}
_LEN_VALUES = np.array(sorted(TARGET_LEN_DIST.keys()))
_LEN_PROBS = np.array([TARGET_LEN_DIST[k] for k in sorted(TARGET_LEN_DIST.keys())], dtype=float)
_LEN_PROBS /= _LEN_PROBS.sum()

# Panel members in frozen order (spec section 1). corpus_index is the
# seed component burned into the spec's RNG scheme.
# (corpus_index, code, role) role: known / nonling / synthetic / target
MEMBERS: list[tuple[int, str, str]] = [
    (1, "K1_linear_b", "known"),
    (2, "K2_vedic_sanskrit", "known"),
    (3, "K3_classical_sanskrit", "known"),
    (4, "K4_old_tamil", "known"),
    (5, "K5_sumerian_ur3", "known"),
    (6, "K7_geez", "known"),  # K6 Akkadian = registered gap (spec 1e)
    (7, "K8_turkish", "known"),
    (8, "K9_indonesian", "known"),
    (9, "N1_khipu", "nonling"),
    (31, "S1_permutation", "synthetic"),
    (32, "S2_iid_zipf", "synthetic"),
    (33, "S3_heraldic_gen", "synthetic"),
    (34, "S4_admin_gen", "synthetic"),
    (21, "R1_indus_holdat_m77", "target"),
    (22, "R2_indus_icit_wells", "target"),
    (23, "R3_indus_mixed", "target"),
]

KNOWN_LABELS: dict[str, str] = {
    "K1_linear_b": "indo_european_other",
    "K2_vedic_sanskrit": "indo_aryan",
    "K3_classical_sanskrit": "indo_aryan",
    "K4_old_tamil": "dravidian",
    "K5_sumerian_ur3": "isolate_sumerian",
    "K7_geez": "semitic",
    "K8_turkish": "turkic",
    "K9_indonesian": "austronesian",
    "N1_khipu": "non_linguistic",
}


# --------------------------------------------------------------------------
# Syllable splitters (spec section 3)
# --------------------------------------------------------------------------

_SKT_VOWELS = ["ai", "au", "ā", "ī", "ū", "ṝ", "a", "i", "u", "ṛ", "ḷ", "e", "o"]
_SKT_VOWEL_SET = set("aāiīuūṛṝḷeo")


def syllabify_sanskrit(word: str) -> list[str]:
    """Deterministic IAST syllabifier (spec section 3).

    A syllable = onset cluster + one vowel nucleus + optional coda
    (anusvara/visarga attach to the preceding nucleus; when >= 2
    consonants precede a nucleus, the first becomes the previous
    syllable's coda). Unparseable residue is passed through whole.
    """
    # tokenise into units: digraph vowels are single nuclei
    units: list[tuple[str, bool]] = []  # (text, is_vowel)
    i = 0
    while i < len(word):
        two = word[i : i + 2]
        if two in ("ai", "au"):
            units.append((two, True))
            i += 2
        elif word[i] in _SKT_VOWEL_SET:
            units.append((word[i], True))
            i += 1
        else:
            units.append((word[i], False))
            i += 1
    vowel_pos = [j for j, (_, v) in enumerate(units) if v]
    if not vowel_pos:
        return [word]
    syllables: list[str] = []
    prev_end = 0  # unit index after previous nucleus (+ its attachs)
    for vi, vp in enumerate(vowel_pos):
        onset_units = units[prev_end:vp]
        nucleus = units[vp][0]
        end = vp + 1
        # anusvara / visarga attach to this nucleus
        while end < len(units) and units[end][0] in ("ṃ", "ḥ"):
            nucleus += units[end][0]
            end += 1
        onset = "".join(u for u, _ in onset_units)
        if vi > 0 and len(onset_units) >= 2:
            # first consonant of the cluster closes the previous syllable
            syllables[-1] += onset_units[0][0]
            onset = "".join(u for u, _ in onset_units[1:])
        if vi == len(vowel_pos) - 1:
            # trailing consonants close the final syllable
            onset_tail = "".join(u for u, _ in units[end:])
            syllables.append(onset + nucleus + onset_tail)
        else:
            syllables.append(onset + nucleus)
        prev_end = end
    return [s for s in syllables if s]


def syllabify_latin(word: str, vowels: set[str], diphthongs: set[str]) -> list[str]:
    """Vowel-nucleus syllabifier for shallow Latin orthographies."""
    w = word.lower()
    nuclei: list[tuple[int, int]] = []  # [start, end) spans of vowel nuclei
    i = 0
    while i < len(w):
        if w[i] in vowels:
            if i + 1 < len(w) and w[i : i + 2] in diphthongs:
                nuclei.append((i, i + 2))
                i += 2
            else:
                nuclei.append((i, i + 1))
                i += 1
        else:
            i += 1
    if not nuclei:
        return [w]
    syllables: list[str] = []
    prev_end = 0
    for ni, (ns, ne) in enumerate(nuclei):
        onset = w[prev_end:ns]
        if ni > 0 and len(onset) >= 2:
            syllables[-1] += onset[0]
            onset = onset[1:]
        if ni == len(nuclei) - 1:
            syllables.append(onset + w[ns:ne] + w[ne:])
        else:
            syllables.append(onset + w[ns:ne])
        prev_end = ne
    return [s for s in syllables if s]


_TR_VOWELS = set("aeıioöuü")
_ID_VOWELS = set("aeiou")
_ID_DIPHTHONGS = {"ai", "au", "oi"}


# --------------------------------------------------------------------------
# Corpus loaders. Each returns (texts_or_stream, stats) where
# texts_or_stream is ("texts", list[list[str]]) or ("stream", list[str]).
# --------------------------------------------------------------------------


def _holdat_texts() -> tuple[list[list[str]], dict]:
    path = SOURCES / "holdat_indus_corpus.csv"
    seals: dict[str, list[tuple[int, str]]] = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            seals[row["seal_id"]].append((int(row["position"]), row["letters"]))
    texts = [[tok for _, tok in sorted(v)] for v in seals.values()]
    stats = {
        "texts": len(texts),
        "tokens": sum(len(t) for t in texts),
        "vocab": len({t for s in texts for t in s}),
    }
    return texts, stats


def _icit_texts() -> tuple[list[list[str]], dict]:
    d = json.loads((SOURCES / "icit_extracted_corpus.json").read_text(encoding="utf-8"))
    texts = [[str(s) for s in ins["sequence"]] for ins in d["inscriptions"]]
    stats = {
        "texts": len(texts),
        "tokens": sum(len(t) for t in texts),
        "vocab": len({t for s in texts for t in s}),
    }
    return texts, stats


def _mixed_texts() -> tuple[list[list[str]], dict]:
    h, hs = _holdat_texts()
    w, ws = _icit_texts()
    texts = [["M:" + t for t in s] for s in h] + [["W:" + t for t in s] for s in w]
    stats = {"texts": len(texts), "tokens": hs["tokens"] + ws["tokens"],
             "vocab": len({t for s in texts for t in s})}
    return texts, stats


def _damos_stream() -> tuple[list[str], dict]:
    path = DATA / "phase17_corpora" / "damos_inscriptions.csv"
    stream: list[str] = []
    rows = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows += 1
            for tok in row["signs_ws_joined"].split():
                if tok in {".", "vac.", "vac", "..."}:
                    continue
                stream.append(tok)
    return stream, {"documents": rows, "tokens": len(stream),
                    "vocab": len(set(stream))}


def _rv_stream() -> tuple[list[str], dict]:
    path = DATA / "phase18_corpora" / "rv_padapatha_seqs.csv"
    stream: list[str] = []
    words = 0
    passthrough = 0
    rows = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows += 1
            for w in row["padapatha_words_ws_joined"].split():
                words += 1
                syl = syllabify_sanskrit(w)
                if syl == [w]:
                    passthrough += 1
                stream.extend(syl)
    return stream, {"documents": rows, "words": words, "tokens": len(stream),
                    "vocab": len(set(stream)), "splitter_passthrough_words": passthrough}


def _dcs_stream() -> tuple[list[str], dict]:
    stream: list[str] = []
    words = 0
    passthrough = 0
    files = sorted((SOURCES / "dcs_classical").glob("*.conllu"))
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or "\t" not in line:
                continue
            parts = line.split("\t")
            if "-" in parts[0] or "." in parts[0]:
                continue  # multiword token / empty node
            form = parts[1].strip()
            if not form or form == "_":
                continue
            words += 1
            syl = syllabify_sanskrit(form)
            if syl == [form]:
                passthrough += 1
            stream.extend(syl)
    return stream, {"documents": len(files), "words": words, "tokens": len(stream),
                    "vocab": len(set(stream)), "splitter_passthrough_words": passthrough}


def _tamil_stream() -> tuple[list[str], dict]:
    path = DATA / "phase16_corpora" / "kee2u_tamil_morpheme_seqs.csv"
    stream: list[str] = []
    rows = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows += 1
            stream.extend(row["morpheme_ids_ws_joined"].split())
    return stream, {"documents": rows, "tokens": len(stream),
                    "vocab": len(set(stream))}


def _conll_forms(path: Path) -> list[str]:
    forms: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line or line.startswith("#") or "\t" not in line:
            continue
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1].strip():
            forms.append(parts[1].strip())
    return forms


def _sumerian_stream() -> tuple[list[str], dict]:
    base = SOURCES / "sumerian_mtaac_ur3" / "ur3_corpus_data"
    index = json.loads((base / "corpus_20180410-215511.json").read_text(encoding="utf-8"))
    conll_dir = base / "conll"
    stream: list[str] = []
    files_read = 0
    word_tokens = 0
    MAX_FILES = 30_000  # frozen cap (spec acquisition note): CDLI-no order
    MAX_TOKENS = 2_000_000
    for entry in index["entries"]:
        if files_read >= MAX_FILES or len(stream) >= MAX_TOKENS:
            break
        pnum = entry.get("CDLI no.", "")
        path = conll_dir / f"{pnum}.conll"
        if not path.exists():
            continue
        files_read += 1
        for form in _conll_forms(path):
            word_tokens += 1
            cleaned = form.replace("{", "").replace("}", "")
            for sign in cleaned.split("-"):
                sign = sign.strip()
                if sign and sign != "...":
                    stream.append(sign)
    return stream, {"documents": files_read, "words": word_tokens,
                    "tokens": len(stream), "vocab": len(set(stream))}


def _geez_stream() -> tuple[list[str], dict]:
    path = DATA / "geez" / "Geez_Genesis_syllabic_nopunctuation.txt"
    words = path.read_text(encoding="utf-8").split()
    # The file's whitespace tokens are words written in the Ethiopic
    # syllabary; each character is one syllable sign. The frozen unit
    # (spec section 1) is the syllable, so the stream is the
    # character sequence.
    stream = [ch for w in words for ch in w]
    return stream, {"documents": 1, "words": len(words), "tokens": len(stream),
                    "vocab": len(set(stream))}


def _ud_stream(folder: str, vowels: set[str], diphthongs: set[str]) -> tuple[list[str], dict]:
    stream: list[str] = []
    words = 0
    passthrough = 0
    files = sorted((SOURCES / folder).glob("*.conllu"))
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or "\t" not in line:
                continue
            parts = line.split("\t")
            if "-" in parts[0] or "." in parts[0]:
                continue
            form = parts[1].strip()
            if not form or form == "_":
                continue
            if not any(ch.isalpha() for ch in form):
                continue
            words += 1
            syl = syllabify_latin(form, vowels, diphthongs)
            if syl == [form.lower()]:
                passthrough += 1
            stream.extend(syl)
    return stream, {"documents": len(files), "words": words, "tokens": len(stream),
                    "vocab": len(set(stream)), "splitter_passthrough_words": passthrough}


def _khipu_stream() -> tuple[list[str], dict]:
    db_path = SOURCES / "khipu_extract" / "open-khipu-repository-2.1.0" / "data" / "khipu.db"
    if not db_path.exists():
        zip_path = SOURCES / "open_khipu_repository.zip"
        with zipfile.ZipFile(zip_path) as z:
            z.extract("open-khipu-repository-2.1.0/data/khipu.db", SOURCES / "khipu_extract")
    db = sqlite3.connect(str(db_path))
    stream: list[str] = []
    khipu_ids = [r[0] for r in db.execute("SELECT KHIPU_ID FROM khipu_main ORDER BY KHIPU_ID")]
    n_cords = 0
    for kid in khipu_ids:
        cords = [r[0] for r in db.execute(
            "SELECT CORD_ID FROM cord WHERE KHIPU_ID = ? ORDER BY CORD_ID", (kid,))]
        n_cords += len(cords)
        for cid in cords:
            knots = [r[0] for r in db.execute(
                "SELECT TYPE_CODE FROM knot WHERE CORD_ID = ? "
                "ORDER BY CLUSTER_ORDINAL, KNOT_ORDINAL", (cid,))]
            stream.extend(str(k) for k in knots if k is not None)
    db.close()
    return stream, {"documents": len(khipu_ids), "cords": n_cords,
                    "tokens": len(stream), "vocab": len(set(stream))}


LOADERS = {
    "K1_linear_b": ("stream", _damos_stream),
    "K2_vedic_sanskrit": ("stream", _rv_stream),
    "K3_classical_sanskrit": ("stream", _dcs_stream),
    "K4_old_tamil": ("stream", _tamil_stream),
    "K5_sumerian_ur3": ("stream", _sumerian_stream),
    "K7_geez": ("stream", _geez_stream),
    "K8_turkish": ("stream", lambda: _ud_stream("turkish_ud", _TR_VOWELS, set())),
    "K9_indonesian": ("stream", lambda: _ud_stream("indonesian_ud", _ID_VOWELS, _ID_DIPHTHONGS)),
    "N1_khipu": ("stream", _khipu_stream),
    "R1_indus_holdat_m77": ("texts", _holdat_texts),
    "R2_indus_icit_wells": ("texts", _icit_texts),
    "R3_indus_mixed": ("texts", _mixed_texts),
}


# --------------------------------------------------------------------------
# Chunking, resampling, generators (spec sections 2 and 5)
# --------------------------------------------------------------------------


def chunk_stream(tokens: list[str], corpus_index: int) -> list[list[str]]:
    rng = np.random.default_rng(np.random.SeedSequence([MASTER_SEED, corpus_index]))
    chunks: list[list[str]] = []
    i = 0
    n = len(tokens)
    while i < n:
        length = int(rng.choice(_LEN_VALUES, p=_LEN_PROBS))
        if i + length > n:
            break  # final partial chunk dropped (spec section 2)
        chunks.append(tokens[i : i + length])
        i += length
    return chunks


def resample_draw(texts: list[list[int]], n_tokens: int, rng: np.random.Generator) -> list[list[int]]:
    out: list[list[int]] = []
    total = 0
    n_texts = len(texts)
    while total < n_tokens:
        t = texts[int(rng.integers(n_texts))]
        if total + len(t) <= n_tokens:
            out.append(list(t))
            total += len(t)
        else:
            need = n_tokens - total
            out.append(list(t[:need]))
            total += need
    return out


def _target_lengths(rng: np.random.Generator, total_needed: int) -> list[int]:
    lengths: list[int] = []
    total = 0
    while total < total_needed:
        length = int(rng.choice(_LEN_VALUES, p=_LEN_PROBS))
        lengths.append(length)
        total += length
    return lengths


def _generators(r1_texts: list[list[str]], seed_extra: int | None = None) -> dict[str, list[list[str]]]:
    """Synthetic controls S1-S4 (spec section 5), from R1 statistics.

    seed_extra=None gives the frozen blind instances (seeds
    [20261009, s]). seed_extra=777 gives the disclosed generator
    TRAINING instances used by the analyst's final model (spec 009
    addendum A); the algorithms are identical, only the seed stream
    differs.
    """
    def _seed(s: int) -> list[int]:
        return [20261009, s] if seed_extra is None else [20261009, s, seed_extra]

    unigram = Counter(tok for s in r1_texts for tok in s)
    vocab = list(unigram.keys())
    weights = np.array([unigram[v] for v in vocab], dtype=float)
    weights /= weights.sum()
    need = 5 * N_PRIMARY

    # S1: within-text permutation of R1
    rng1 = np.random.default_rng(np.random.SeedSequence(_seed(1)))
    s1: list[list[str]] = []
    for t in r1_texts:
        arr = list(t)
        rng1.shuffle(arr)
        s1.append(arr)

    # S2: iid Zipf (unigram) texts with target lengths
    rng2 = np.random.default_rng(np.random.SeedSequence(_seed(2)))
    s2: list[list[str]] = []
    for length in _target_lengths(rng2, need):
        s2.append(rng2.choice(vocab, size=length, p=weights).tolist())

    # S3: heraldic positional-template generator
    rng3 = np.random.default_rng(np.random.SeedSequence(_seed(3)))
    init_c = Counter(t[0] for t in r1_texts)
    final_c = Counter(t[-1] for t in r1_texts)
    medial_c = Counter(tok for t in r1_texts for tok in t[1:-1]) if any(len(t) > 2 for t in r1_texts) else unigram

    def _dist(counter: Counter) -> tuple[list[str], np.ndarray]:
        vs = list(counter.keys())
        ws = np.array([counter[v] for v in vs], dtype=float)
        return vs, ws / ws.sum()

    iv, iw = _dist(init_c)
    fv, fw = _dist(final_c)
    mv, mw = _dist(medial_c)
    s3: list[list[str]] = []
    for length in _target_lengths(rng3, need):
        text = []
        for pos in range(length):
            if pos == 0:
                text.append(str(rng3.choice(iv, p=iw)))
            elif pos == length - 1 and length > 1:
                text.append(str(rng3.choice(fv, p=fw)))
            else:
                text.append(str(rng3.choice(mv, p=mw)))
        s3.append(text)

    # S4: administrative generator (top-60 inventory + closure motif)
    rng4 = np.random.default_rng(np.random.SeedSequence(_seed(4)))
    top60 = [v for v, _ in unigram.most_common(60)]
    w60 = np.array([unigram[v] for v in top60], dtype=float)
    w60 /= w60.sum()
    s4: list[list[str]] = []
    for length in _target_lengths(rng4, need):
        text = rng4.choice(top60, size=length, p=w60).tolist()
        text = [str(x) for x in text]
        if length > 1 and rng4.random() < 0.3:
            text[-1] = text[0]
        s4.append(text)

    return {"S1_permutation": s1, "S2_iid_zipf": s2,
            "S3_heraldic_gen": s3, "S4_admin_gen": s4}


def _remap(texts: list[list[str]], corpus_index: int) -> list[list[int]]:
    vocab = sorted({tok for t in texts for tok in t})
    rng = np.random.default_rng(np.random.SeedSequence([20261008, corpus_index]))
    perm = rng.permutation(len(vocab))
    mapping = {tok: int(perm[i]) for i, tok in enumerate(vocab)}
    return [[mapping[tok] for tok in t] for t in texts]


# --------------------------------------------------------------------------
# Panel build
# --------------------------------------------------------------------------


def build_panel(workers: int = 2) -> dict:
    """Build the full anonymized panel + key + build log.

    Writes panel.json and key.json into STATE_DIR. Returns the build
    log (per-corpus counts) for the acquisition record.
    """
    from multiprocessing import Pool

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    build_log: dict[str, dict] = {}

    # Load all corpora into text lists.
    texts_by_code: dict[str, list[list[str]]] = {}
    for corpus_index, code, _role in MEMBERS:
        if code in LOADERS:
            kind, loader = LOADERS[code]
            payload, stats = loader()
            texts = chunk_stream(payload, corpus_index) if kind == "stream" else payload
            texts_by_code[code] = texts
            build_log[code] = {"kind": kind, **stats,
                               "texts_after_chunking": len(texts)}
    # Synthetics derive from R1.
    gens = _generators(texts_by_code["R1_indus_holdat_m77"])
    for code, texts in gens.items():
        texts_by_code[code] = texts
        build_log[code] = {"kind": "generated", "texts": len(texts),
                           "tokens": sum(len(t) for t in texts)}

    # Remap + draw + extract features.
    jobs = []  # (cid_order, code, corpus_index, size_label, n_tokens, draw_index, texts_int)
    remapped: dict[str, list[list[int]]] = {}
    for corpus_index, code, _role in MEMBERS:
        remapped[code] = _remap(texts_by_code[code], corpus_index)

    id_order = [code for _, code, _ in MEMBERS]
    rng_ids = np.random.default_rng(np.random.SeedSequence([20261007]))
    shuffled = [id_order[i] for i in rng_ids.permutation(len(id_order))]
    cid_of = {code: f"C{i + 1:02d}" for i, code in enumerate(shuffled)}

    feature_jobs: list[tuple[str, str, int, list[list[int]]]] = []
    for corpus_index, code, role in MEMBERS:
        texts_int = remapped[code]
        sizes = [("primary", N_PRIMARY)]
        if role in ("known", "nonling", "target"):
            sizes += [("sens_5000", 5_000), ("sens_19600", 19_600)]
        for size_label, n_tok in sizes:
            for draw_index in range(N_DRAWS):
                rng = np.random.default_rng(
                    np.random.SeedSequence([MASTER_SEED, corpus_index, draw_index]))
                draw = resample_draw(texts_int, n_tok, rng)
                feature_jobs.append((code, size_label, draw_index, draw))

    # Disclosed generator TRAINING instances (spec 009 addendum A):
    # same frozen algorithms, seed stream [20261009, s, 777]. These
    # give the analyst's final model its gen_heraldic / gen_
    # administrative classes; the blind S3/S4 members above remain
    # the frozen-seed instances used for control validity.
    gen_train_codes = {"S3_heraldic_gen": ("gen_heraldic", 901),
                       "S4_admin_gen": ("gen_administrative", 902)}
    gen_train_texts = _generators(texts_by_code["R1_indus_holdat_m77"], seed_extra=777)
    gen_train_remapped: dict[str, list[list[int]]] = {}
    for src_code, (_cls, cidx) in gen_train_codes.items():
        rem = _remap(gen_train_texts[src_code], cidx)
        gen_train_remapped[src_code] = rem
        for draw_index in range(N_DRAWS):
            rng = np.random.default_rng(
                np.random.SeedSequence([MASTER_SEED, cidx, draw_index]))
            draw = resample_draw(rem, N_PRIMARY, rng)
            feature_jobs.append((f"GENTRAIN:{src_code}", "primary", draw_index, draw))

    results: dict[tuple[str, str, int], dict[str, float]] = {}
    with Pool(workers) as pool:
        extracted = pool.starmap(
            _extract_job, [(job[3], job[2]) for job in feature_jobs])
    for (code, size_label, draw_index, _draw), feats in zip(feature_jobs, extracted):
        results[(code, size_label, draw_index)] = feats

    panel_members: dict[str, dict] = {}
    key: dict[str, dict] = {}
    for corpus_index, code, role in MEMBERS:
        cid = cid_of[code]
        entry: dict = {"label": KNOWN_LABELS.get(code) if role in ("known", "nonling") else None}
        for size_label in ("primary", "sens_5000", "sens_19600"):
            rows = []
            for draw_index in range(N_DRAWS):
                feats = results.get((code, size_label, draw_index))
                if feats is None:
                    continue
                rows.append([feats[name] for name in FEATURE_NAMES])
            if rows:
                entry[f"features_{size_label}"] = rows
        panel_members[cid] = entry
        key[cid] = {"code": code, "role": role,
                    "label": KNOWN_LABELS.get(code),
                    "corpus_index": corpus_index}

    generator_train: dict[str, list] = {}
    for src_code, (cls_name, _cidx) in gen_train_codes.items():
        rows = []
        for draw_index in range(N_DRAWS):
            feats = results[(f"GENTRAIN:{src_code}", "primary", draw_index)]
            rows.append([feats[name] for name in FEATURE_NAMES])
        generator_train[cls_name] = rows

    panel = {
        "spec": "009-phase111-blind-affiliation",
        "feature_names": FEATURE_NAMES,
        "n_primary": N_PRIMARY,
        "n_draws": N_DRAWS,
        "members": panel_members,
        "known_ids": [cid_of[c] for _, c, r in MEMBERS if r in ("known", "nonling")],
        "blind_ids": [cid_of[c] for _, c, r in MEMBERS if r in ("synthetic", "target")],
        "generator_train": generator_train,
    }
    (STATE_DIR / "panel.json").write_text(json.dumps(panel), encoding="utf-8")
    (STATE_DIR / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    (STATE_DIR / "build_log.json").write_text(json.dumps(build_log, indent=1), encoding="utf-8")
    return build_log


def _extract_job(draw: list[list[int]], draw_index: int) -> dict[str, float]:
    return extract_features(draw, draw_index=draw_index)
