"""Phase-113 (spec 011) — non-SA validation battery: pure machinery.

Ledger-sequence Phase-113 (2026-10-07). Implements the frozen
battery of specs/011-phase113-nonsa44-validation/spec.md:

  T1 cross-corpus consistency (ICIT converted layer vs Holdat),
  T2 positional-grammar fit against the strict SA-independent
     core (profile fit + reading-slot phonotactics),
  T3 compositional co-occurrence in fully-core-readable contexts,

plus the section-5 decision rule. The battery is pure counting
and set membership: no sampling, no RNG, no SA artifact of any
kind is read (governance H26 — SA agreement is not evidence for
sign values; the syllabic LM is deliberately NOT used).

Corpus contexts are built from inscription lists supplied by the
caller (phase113_run), so this module is testable on toy corpora.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

PASS = "PASS"
FAIL = "FAIL"
NOT_ATTESTED = "NOT_ATTESTED"
INDETERMINATE = "INDETERMINATE"

# ── Frozen thresholds (spec 011 section 3) ─────────────────────
T1_MIN_ICIT_TOKENS = 3
T1_TV_MAX = 0.40
T2_MIN_HOLDAT_TOKENS = 8
T2A_TV_MAX = 0.35
T2A_MODAL_SHARE_MIN = 0.45
T2B_MIN_CLASS_INITIALS = 5
T3_PARTNER_MIN_COOC = 2
T3_SUPPORT_PASS = 3
T3_SUPPORT_FAIL_MAX = 1
T3_MIN_CONTEXTS = 4
T3_LEGAL_FRACTION_MIN = 0.75

CLASSES = ("INITIAL", "MEDIAL", "TERMINAL")
_TIE_RANK = {"INITIAL": 0, "TERMINAL": 1, "MEDIAL": 2}

# ── Reading normalization (Phase-58 convention) ────────────────
_STRIP = re.compile(r"[^a-zāīūēōṅñṭṇṉṟḷḻ]")


def normalize_reading(reading: str) -> str:
    """First '/'-segment, lowercase, strip non-phoneme characters."""
    seg = (reading or "").split("/")[0].strip().lower()
    return _STRIP.sub("", seg)


# ── Syllable canon (spec 011 section 3) ────────────────────────
_VOWELS = set("aāiīuūeēoō")
_DIPHTHONGS = ("ai", "au")
_CONSONANTS = set("kṅcñṭṇtnpmyrlvḷḻṟṉ")


def _tokenize(s: str):
    """Split into ('C', ch) / ('N', nucleus) phonemes; None on
    any character outside the canon."""
    toks = []
    i = 0
    while i < len(s):
        two = s[i:i + 2]
        if two in _DIPHTHONGS:
            toks.append(("N", two))
            i += 2
            continue
        ch = s[i]
        if ch in _VOWELS:
            toks.append(("N", ch))
        elif ch in _CONSONANTS:
            toks.append(("C", ch))
        else:
            return None
        i += 1
    return toks


def syllabify(s: str):
    """Greedy maximal-onset syllabification, at most one onset
    consonant and one coda consonant per syllable. Returns the
    syllable list, or None if the string is not canon-legal
    (initial/final consonant cluster, 3+ consonants between
    nuclei, missing nucleus, unknown character)."""
    if not s:
        return None
    toks = _tokenize(s)
    if toks is None:
        return None
    syllables = []
    i, n = 0, len(toks)
    while i < n:
        syl = ""
        if toks[i][0] == "C":
            if i + 1 < n and toks[i + 1][0] == "C":
                return None  # consonant cluster at syllable onset
            syl += toks[i][1]
            i += 1
        if i >= n or toks[i][0] != "N":
            return None  # syllable without a nucleus
        syl += toks[i][1]
        i += 1
        if i < n and toks[i][0] == "C":
            nxt = toks[i + 1] if i + 1 < n else None
            if nxt is None or nxt[0] == "C":
                syl += toks[i][1]  # coda: final, or first of a CC split
                i += 1
            # else: the consonant onsets the next syllable; no coda
        syllables.append(syl)
    return syllables


def canon_legal(s: str) -> bool:
    return syllabify(s) is not None


# ── Positional profiles (Phase-69 / provenance-audit convention) ──

def positional_counts(inscriptions, sign: str) -> tuple[int, int, int]:
    """(INITIAL, MEDIAL, TERMINAL) counts: position 0 of a
    multi-sign inscription is INITIAL, last position TERMINAL,
    everything else (including sole tokens) MEDIAL."""
    counts = [0, 0, 0]
    for ins in inscriptions:
        n = len(ins)
        for pos, tok in enumerate(ins):
            if tok != sign:
                continue
            if pos == 0 and n > 1:
                counts[0] += 1
            elif pos == n - 1 and n > 1:
                counts[2] += 1
            else:
                counts[1] += 1
    return tuple(counts)


def profile_from_counts(counts) -> tuple[float, float, float] | None:
    total = sum(counts)
    if total == 0:
        return None
    return tuple(c / total for c in counts)


def modal_class(profile) -> str:
    """Largest share; ties break INITIAL > TERMINAL > MEDIAL."""
    shares = dict(zip(CLASSES, profile))
    return min(CLASSES, key=lambda k: (-shares[k], _TIE_RANK[k]))


def tv_distance(p, q) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


class CorpusContext:
    """Precomputed per-corpus statistics over inscription lists."""

    def __init__(self, inscriptions):
        self.inscriptions = [list(x) for x in inscriptions if x]
        self.token_counts: Counter = Counter()
        self._counts: dict[str, tuple[int, int, int]] = {}
        self.adjacency: dict[str, Counter] = defaultdict(Counter)
        raw: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
        for ins in self.inscriptions:
            n = len(ins)
            for pos, tok in enumerate(ins):
                self.token_counts[tok] += 1
                if pos == 0 and n > 1:
                    raw[tok][0] += 1
                elif pos == n - 1 and n > 1:
                    raw[tok][2] += 1
                else:
                    raw[tok][1] += 1
                if pos + 1 < n:
                    self.adjacency[tok][ins[pos + 1]] += 1
                    self.adjacency[ins[pos + 1]][tok] += 1
        self._counts = {s: tuple(c) for s, c in raw.items()}

    @property
    def n_inscriptions(self) -> int:
        return len(self.inscriptions)

    @property
    def n_tokens(self) -> int:
        return sum(self.token_counts.values())

    def profile(self, sign: str):
        return profile_from_counts(self._counts.get(sign, (0, 0, 0)))

    def token_count(self, sign: str) -> int:
        return self.token_counts.get(sign, 0)


class CoreGrammar:
    """The strict core's positional grammar + reading inventories,
    derived exclusively from core signs' corpus behavior."""

    def __init__(self, core_signs, readings_norm, holdat: CorpusContext):
        self.core = frozenset(core_signs)
        self.centroids: dict[str, tuple[float, float, float]] = {}
        self.class_initials: dict[str, set] = {}
        by_class: dict[str, list] = defaultdict(list)
        for s in self.core:
            prof = holdat.profile(s)
            if prof is None:
                continue
            by_class[modal_class(prof)].append((s, prof,
                                                holdat.token_count(s)))
        for k, members in by_class.items():
            wsum = sum(w for _, _, w in members) or 1
            self.centroids[k] = tuple(
                sum(p[i] * w for _, p, w in members) / wsum
                for i in range(3))
            self.class_initials[k] = {
                readings_norm[s][0] for s, _, _ in members
                if readings_norm.get(s)}
        self.class_sizes = {k: len(v) for k, v in by_class.items()}


# ── The three tests ─────────────────────────────────────────────

def test_t1(sign, holdat: CorpusContext, icit: CorpusContext) -> dict:
    n_i = icit.token_count(sign)
    out = {"n_icit_tokens": n_i}
    if n_i < T1_MIN_ICIT_TOKENS:
        out["state"] = NOT_ATTESTED
        return out
    prof_h = holdat.profile(sign)
    prof_i = icit.profile(sign)
    out["modal_holdat"] = modal_class(prof_h)
    out["modal_icit"] = modal_class(prof_i)
    out["tv"] = round(tv_distance(prof_h, prof_i), 6)
    out["state"] = (PASS if out["modal_icit"] == out["modal_holdat"]
                    and out["tv"] <= T1_TV_MAX else FAIL)
    return out


def test_t2(sign, reading_norm, core: CoreGrammar,
            holdat: CorpusContext, is_valid_initial) -> dict:
    n_h = holdat.token_count(sign)
    out = {"n_holdat_tokens": n_h}
    prof = holdat.profile(sign)
    if prof is None:
        out.update({"state": INDETERMINATE, "reason": "sign absent"})
        return out
    k = modal_class(prof)
    modal_share = max(prof)
    out.update({"modal_class": k, "modal_share": round(modal_share, 6),
                "profile": [round(x, 6) for x in prof]})
    # T2a — profile fit against the core centroid of the same class
    centroid = core.centroids.get(k)
    if centroid is None:
        t2a, tv = INDETERMINATE, None
    else:
        tv = tv_distance(prof, centroid)
        t2a = (PASS if tv <= T2A_TV_MAX
               and modal_share >= T2A_MODAL_SHARE_MIN else FAIL)
    out["t2a"] = {"state": t2a,
                  "tv_to_centroid": None if tv is None else round(tv, 6)}
    # T2b — reading-slot phonotactics
    b_fail = []
    if not is_valid_initial(reading_norm):
        b_fail.append("invalid_dravidian_initial")
    initials = core.class_initials.get(k, set())
    if len(initials) >= T2B_MIN_CLASS_INITIALS:
        if not reading_norm or reading_norm[0] not in initials:
            b_fail.append("initial_not_in_class_inventory")
    if not canon_legal(reading_norm):
        b_fail.append("reading_not_canon_legal")
    out["t2b"] = {"state": FAIL if b_fail else PASS, "failures": b_fail}
    if t2a == FAIL or b_fail:
        out["state"] = FAIL
    elif n_h < T2_MIN_HOLDAT_TOKENS or t2a == INDETERMINATE:
        out["state"] = INDETERMINATE
    else:
        out["state"] = PASS
    return out


def test_t3(sign, reading_norm, core_signs, readings_norm,
            holdat: CorpusContext) -> dict:
    n_h = holdat.token_count(sign)
    out = {"n_holdat_tokens": n_h}
    partners = {p for p, c in holdat.adjacency.get(sign, {}).items()
                if c >= T3_PARTNER_MIN_COOC and p in core_signs}
    out["support"] = len(partners)
    contexts = [ins for ins in holdat.inscriptions
                if len(ins) >= 2 and sign in ins
                and all(t == sign or t in core_signs for t in ins)]
    out["n_contexts"] = len(contexts)
    legal = 0
    for ins in contexts:
        composed = "".join(
            reading_norm if t == sign else readings_norm.get(t, "")
            for t in ins)
        if composed and canon_legal(composed):
            legal += 1
    out["legal_contexts"] = legal
    out["legal_fraction"] = (round(legal / len(contexts), 6)
                             if contexts else None)
    if n_h < T2_MIN_HOLDAT_TOKENS:
        out["state"] = INDETERMINATE
    elif out["support"] <= T3_SUPPORT_FAIL_MAX or (
            out["n_contexts"] >= T3_MIN_CONTEXTS
            and out["legal_fraction"] < T3_LEGAL_FRACTION_MIN):
        out["state"] = FAIL
    elif (out["support"] >= T3_SUPPORT_PASS
          and out["n_contexts"] >= T3_MIN_CONTEXTS
          and out["legal_fraction"] >= T3_LEGAL_FRACTION_MIN):
        out["state"] = PASS
    else:
        out["state"] = INDETERMINATE
    return out


def evaluate_anchor(sign, reading_raw, core: CoreGrammar,
                    readings_norm, holdat: CorpusContext,
                    icit: CorpusContext, is_valid_initial) -> dict:
    """Full battery for one anchor against a fixed core grammar.
    `readings_norm` maps core signs to normalized readings (for T3
    composition); the tested sign's own reading is normalized here."""
    reading_norm = normalize_reading(reading_raw)
    t1 = test_t1(sign, holdat, icit)
    t2 = test_t2(sign, reading_norm, core, holdat, is_valid_initial)
    t3 = test_t3(sign, reading_norm, core.core, readings_norm, holdat)
    states = {"t1": t1["state"], "t2": t2["state"], "t3": t3["state"]}
    return {"sign": sign, "reading": reading_raw,
            "reading_normalized": reading_norm,
            "t1": t1, "t2": t2, "t3": t3,
            "outcome": decide(states)}


def decide(states) -> str:
    """Spec 011 section 5 decision rule."""
    vals = [states["t1"], states["t2"], states["t3"]]
    if all(v == PASS for v in vals):
        return "VALIDATED_NON_SA"
    if any(v == FAIL for v in vals):
        return "DEMOTE"
    return "UNRESOLVED"
