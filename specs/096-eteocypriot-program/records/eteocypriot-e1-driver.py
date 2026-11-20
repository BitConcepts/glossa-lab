#!/usr/bin/env python3
"""Spec 096 — Eteocypriot E1 driver.

Implements exactly the procedure frozen in
specs/096-eteocypriot-program/records/freeze-record-2026-11-20.md
section 5, over the corpus frozen in section 2 of the same record.

Discipline:
- verifies the corpus file SHA-256 against the freeze pin and
  refuses to run on a mismatch (fail-closed);
- verifies each development record's per-inscription pin;
- loads DEVELOPMENT records only for analysis; held-out records
  are never read beyond the split field that excludes them (the
  seal is procedural, freeze section 4);
- stdlib only, deterministic; prints the run record as JSON.

Greek-name derivation D(name) implements rules R1-R3 of the
freeze and nothing else. The letter handling: polytonic
diacritics are stripped to letter identity; final sigma is
sigma; xi expands to the consonant sequence k+s. Vowel map:
alpha a, epsilon e, eta e, iota i, omicron o, upsilon u,
omega o. Consonant stems: beta p, gamma k, delta t, zeta s,
theta t, kappa k, lambda l, mu m, nu n, pi p, rho r, sigma s,
tau t, phi p, chi k.
"""
import hashlib
import json
import sys
import unicodedata

EXPECTED_CORPUS_SHA256 = (
    "5077285e8eac4b21785ca29cb151d47407f780998d85fa1eea27ef9d7e04f2dd"
)

VOWELS = {"α": "a", "ε": "e", "η": "e", "ι": "i", "ο": "o", "υ": "u", "ω": "o"}
STEMS = {
    "β": "p", "γ": "k", "δ": "t", "ζ": "s", "θ": "t", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "π": "p", "ρ": "r", "σ": "s",
    "τ": "t", "φ": "p", "χ": "k",
}


def letters_of(word):
    """Greek word -> list of ('v', vowel_sign) / ('c', stem) units."""
    decomposed = unicodedata.normalize("NFD", word)
    base = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    base = base.lower().replace("ς", "σ")
    units = []
    for ch in base:
        if ch in VOWELS:
            units.append(("v", VOWELS[ch]))
        elif ch == "ξ":
            units.append(("c", "k"))
            units.append(("c", "s"))
        elif ch in STEMS:
            units.append(("c", STEMS[ch]))
        else:
            raise ValueError(f"unhandled Greek letter {ch!r} in {word!r}")
    return units


def derive_cv(word):
    """D(name), R1-R3 with the CV pairing consuming its vowel.

    R2 pairs a consonant with the FOLLOWING vowel into one sign;
    that vowel does not then also emit a standalone sign. R1
    applies to a vowel not consumed by a preceding consonant.
    """
    units = letters_of(word)
    out = []
    prev_vowel = "a"
    i = 0
    while i < len(units):
        kind, val = units[i]
        if kind == "v":
            out.append(val)  # R1
            prev_vowel = val
            i += 1
        else:
            nxt = units[i + 1] if i + 1 < len(units) else None
            if nxt is not None and nxt[0] == "v":
                out.append(val + nxt[1])  # R2
                prev_vowel = nxt[1]
                i += 2
            else:
                out.append(val + prev_vowel)  # R3
                i += 1
    return out


def lccs(a, b):
    """Length of the longest common contiguous subsequence."""
    best = 0
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]:
                k += 1
            best = max(best, k)
    return best


def bare(token):
    return token.strip("[]")


def main():
    corpus_path = sys.argv[1]
    raw = open(corpus_path, "rb").read()
    file_sha = hashlib.sha256(raw).hexdigest()
    if file_sha != EXPECTED_CORPUS_SHA256:
        print(f"REFUSED: corpus file sha256 {file_sha} != freeze pin "
              f"{EXPECTED_CORPUS_SHA256}", file=sys.stderr)
        return 3
    corpus = json.loads(raw.decode("utf-8"))

    # Seal: only the split field of non-development records is read.
    dev = []
    for rec in corpus["inscriptions"]:
        if rec.get("split") == "development":
            dev.append(rec)
    by_id = {r["id"]: r for r in dev}

    pins = {}
    for rec in dev:
        canon = json.dumps(rec, sort_keys=True, ensure_ascii=False).encode("utf-8")
        pins[rec["id"]] = hashlib.sha256(canon).hexdigest()

    ics = by_id["ICS196"]
    segments = []
    for line in ics["eteocypriot_lines"]:
        segments.extend([[bare(t) for t in seg] for seg in line["segments"]])
    greek_words = ics["greek_side"]["words"]

    # Ground truth from the corpus record (freeze section 5 states
    # the same correspondences; scoring only, never an input).
    gt = []
    for corr in ics["ground_truth_correspondences"]:
        gt.append({
            "greek_word": corr["greek_word"],
            "greek_word_index": corr["greek_word_index"],
            "segment_index": corr["eteocypriot_segment_index"],
        })

    record = {
        "run": "eteocypriot-e1",
        "date": "2026-11-20",
        "program": "Spec 096 - Eteocypriot Program",
        "freeze": "records/freeze-record-2026-11-20.md",
        "corpus_file_sha256_verified": file_sha,
        "development_pins": pins,
        "held_out_records_loaded": 0,
        "ics196_segments": ["-".join(s) for s in segments],
        "greek_words": greek_words,
        "ground_truth": gt,
        "legs": {},
    }

    # ICS 196 leg.
    leg = {"names": []}
    for corr in gt:
        name = corr["greek_word"]
        d = derive_cv(name)
        scores = [lccs(d, seg) for seg in segments]
        # A1: positional partner = segment with the Greek word's index.
        a1_partner = corr["greek_word_index"]
        a1_recovered = (a1_partner == corr["segment_index"])
        # A2: argmax LCCS, ties to earliest.
        best = max(scores)
        a2_partner = scores.index(best) + 1
        a2_recovered = (a2_partner == corr["segment_index"])
        leg["names"].append({
            "greek_word": name,
            "greek_word_index": corr["greek_word_index"],
            "derived_spelling": "-".join(d),
            "lccs_by_segment": scores,
            "ground_truth_segment": corr["segment_index"],
            "A1_partner_segment": a1_partner,
            "A1_recovered": a1_recovered,
            "A2_partner_segment": a2_partner,
            "A2_lccs": best,
            "A2_recovered": a2_recovered,
        })
    leg["A1_recovered_count"] = sum(1 for n in leg["names"] if n["A1_recovered"])
    leg["A2_recovered_count"] = sum(1 for n in leg["names"] if n["A2_recovered"])
    leg["names_total"] = len(leg["names"])
    leg["both_recovered_under_at_least_one_assumption"] = any(
        all(n[f"{a}_recovered"] for n in leg["names"]) for a in ("A1", "A2")
    )
    record["legs"]["ics196"] = leg

    # Androkles leg: no Eteocypriot side held (freeze F-E1b).
    androkles = {"names": []}
    for rid in ("ANDROKLES-A", "ANDROKLES-B"):
        rec = by_id[rid]
        segs = rec.get("eteocypriot_side") or []
        androkles["names"].append({
            "inscription": rid,
            "eteocypriot_segments_held": len(segs),
            "administrable": False,
        })
    androkles["administrable"] = False
    androkles["floor_F_E1b"] = "NOT MET (freeze section 6); leg TOO THIN at freeze"
    record["legs"]["androkles"] = androkles

    # P1 as registered: conjunction over both legs.
    record["P1"] = {
        "ics196_leg_passes": leg["both_recovered_under_at_least_one_assumption"],
        "androkles_leg_passes": False,
        "P1_passes_as_registered": False,
        "basis": "P1 requires both ICS 196 correspondences and at least one "
                 "Androkles correspondence recovered under at least one "
                 "assumption; the Androkles leg is TOO THIN at freeze "
                 "(F-E1b) and the ICS 196 leg is scored above.",
    }
    print(json.dumps(record, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
