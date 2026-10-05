"""Phase-105: Positional/formula adjudication of personal-name candidates.

Adjudicates the Phase-103 top personal-name candidates (M362, M398,
M375, M024) against the Holdat corpus, in the style of the Phase-101
M293 adjudication: compute each sign's positional profile and name-slot
pattern membership from the corpus itself, compare against the animal
classifier class (Phase-101: classifiers are ~100% INITIAL), and let
the computed evidence decide the verdict.

This script REPLACES an earlier unrun draft of phase105_name_signs.py
that asserted pre-written readings and anchor promotions. No readings
are asserted here and no anchor is promoted or demoted by this script:
all four candidates already stand as HIGH anchors in
backend/reports/INDUS_FINAL_ANCHORS.json (their bases were folded in by
later phases), so the question adjudicated is whether the corpus
positional/formula evidence CORROBORATES the personal-name-component
role those anchors assert.

Verdict rules (stated up front, Phase-101 thresholds):
  CORROBORATED   freq >= 5 AND initial_rate < 0.50 (not classifier-like)
                 AND name_slot_count >= 2 across the Phase-103 patterns.
  INCONCLUSIVE   freq < 5 — token count too low for a positional verdict
                 (Phase-103 pattern counts are reported as context).
  CHALLENGED     freq >= 5 AND (initial_rate >= 0.50 OR
                 name_slot_count == 0) — profile fits a classifier or
                 shows no name-slot behaviour.

Name-slot patterns (Phase-103 definitions):
  ANIMAL_NAME_TITLE   [ANIMAL_CLASSIFIER]-[X]-[TITLE]
  GENITIVE_NAME       [M267]-[X]-... (genitive precedes the candidate)
  NAME_AY_AN          [X]-[M342]-[M176]

Corpus order follows the Holdat CSV (grouped by cisi_number, ascending
position), the same convention as Phase-101. CPU only.
Output: reports/phase105_name_signs.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOLDAT = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P103 = REPO / "outputs/phase103_name_lexicon.json"
OUT = REPO / "reports" / "phase105_name_signs.json"

CANDIDATES = ["M362", "M398", "M375", "M024"]

# Grammar role sets — identical to backend/scripts/phase103_name_lexicon.py
ANIMAL_CLASSIFIERS = {"M006", "M016", "M045", "M062", "M047", "M039", "M040", "M001", "M007"}
TITLE_SIGNS = {"M099", "M073", "M059", "M030", "M041", "M107", "M017", "M063"}
SUFFIX_SIGNS = {"M342", "M176", "M367", "M391", "M336", "M089", "M328", "M162"}
GENITIVE = "M267"
# Phase-101 adjudicated reference profile (M293, personal-name component)
M293_REFERENCE = {"initial": 0.069, "medial": 0.599, "terminal": 0.332}


def load_sequences() -> list[list[str]]:
    by_seal: dict[str, list[tuple[int, str]]] = defaultdict(list)
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row.get("cisi_number", "")
            p = int(row.get("position", 0) or 0)
            by_seal[c].append((p, row.get("letters", "")))
    return [[s for _, s in sorted(v)] for v in by_seal.values()]


def profile(sign: str, seqs: list[list[str]]) -> dict:
    n = n_init = n_med = n_term = 0
    after_genitive = before_suffix = name_slots = 0
    patterns: Counter = Counter()
    samples: list[str] = []
    for seq in seqs:
        for i, s in enumerate(seq):
            if s != sign:
                continue
            n += 1
            if i == 0:
                n_init += 1
            elif i == len(seq) - 1:
                n_term += 1
            else:
                n_med += 1
            prev = seq[i - 1] if i > 0 else None
            nxt = seq[i + 1] if i + 1 < len(seq) else None
            nxt2 = seq[i + 2] if i + 2 < len(seq) else None
            if prev == GENITIVE:
                after_genitive += 1
                patterns["GENITIVE_NAME"] += 1
                name_slots += 1
            if nxt in SUFFIX_SIGNS:
                before_suffix += 1
            if prev in ANIMAL_CLASSIFIERS and nxt in TITLE_SIGNS:
                patterns["ANIMAL_NAME_TITLE"] += 1
                name_slots += 1
            if nxt == "M342" and nxt2 == "M176":
                patterns["NAME_AY_AN"] += 1
                name_slots += 1
            if len(samples) < 4:
                ctx = seq[max(0, i - 1): i + 2]
                samples.append("-".join(ctx))
    return {
        "freq": n,
        "initial": n_init, "medial": n_med, "terminal": n_term,
        "initial_rate": round(n_init / n, 4) if n else 0.0,
        "medial_rate": round(n_med / n, 4) if n else 0.0,
        "terminal_rate": round(n_term / n, 4) if n else 0.0,
        "after_genitive_count": after_genitive,
        "before_case_suffix_count": before_suffix,
        "name_slot_count": name_slots,
        "patterns": dict(patterns),
        "sample_contexts": samples,
    }


def verdict(p: dict, role: str | None) -> tuple[str, str]:
    if p["freq"] < 5:
        return (
            "INCONCLUSIVE",
            f"Only {p['freq']} corpus tokens — too few for a positional verdict "
            "(Phase-101 adjudication rested on 100+ tokens). Phase-103 pattern "
            "counts stand as the only evidence and are not re-tested here.",
        )
    if p["initial_rate"] >= 0.50 or p["name_slot_count"] == 0:
        rationale = (
            "Positional profile is classifier-like (INITIAL >= 50%) or the sign "
            "never occupies a defined name slot; inconsistent with a "
            "personal-name-component role."
        )
        if role == "CLASSIFIER_PREFIX":
            rationale += (
                " The Holdat semantic-roles file independently classifies this "
                "sign as CLASSIFIER_PREFIX. NAME_AY_AN occurrences (the sign "
                "heading the [X]-M342-M176 formula) are the counter-consideration: "
                "the sign may head a name formula rather than sit medially in "
                "one, but under the Phase-101 adjudication standard its profile "
                "is a prefix/head profile, not a name-component profile. "
                "Flagged for future adjudication; the standing anchor is not "
                "changed by this phase."
            )
        return ("CHALLENGED", rationale)
    if p["name_slot_count"] >= 2:
        rationale = (
            "Non-initial positional profile plus repeated occupation of "
            "Phase-103 name slots; consistent with a personal-name component "
            "(compare M293 reference profile)."
        )
        if role == "PERSON_OR_OWNER":
            rationale += (
                " The Holdat semantic-roles file independently classifies this "
                "sign as PERSON_OR_OWNER, agreeing with the name-slot evidence."
            )
        return ("CORROBORATED", rationale)
    return (
        "INCONCLUSIVE",
        "Positional profile is not classifier-like, but name-slot evidence is "
        "thinner than the corroboration bar (>= 2 slots).",
    )


def main() -> int:
    seqs = load_sequences()
    print(f"Loaded {len(seqs)} inscriptions from Holdat corpus")

    roles: dict[str, str] = {}
    if ROLES.exists():
        with open(ROLES, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                roles[r["symbol"]] = r.get("semantic_role", "")

    p103: dict[str, dict] = {}
    if P103.exists():
        for c in json.loads(P103.read_text(encoding="utf-8")).get("name_candidates", []):
            p103[c.get("sign")] = c

    anchors = json.loads(ANCHORS.read_text(encoding="utf-8")).get("anchors", {})

    # Comparison class: aggregate animal-classifier profile (Phase-101 method)
    clf_profiles = {s: profile(s, seqs) for s in sorted(ANIMAL_CLASSIFIERS)}
    clf_freq = sum(p["freq"] for p in clf_profiles.values())
    clf_init_rate = (
        sum(p["initial"] for p in clf_profiles.values()) / clf_freq if clf_freq else 0.0
    )
    print(f"Animal classifiers: {clf_freq} tokens, aggregate INITIAL rate {clf_init_rate:.1%}")

    results = []
    for sign in CANDIDATES:
        p = profile(sign, seqs)
        v, rationale = verdict(p, roles.get(sign))
        anchor = anchors.get(sign, {})
        entry = {
            "sign": sign,
            "corpus_profile": p,
            "holdat_semantic_role": roles.get(sign),
            "phase103": {
                "name_score": p103.get(sign, {}).get("name_score"),
                "name_slot_count": p103.get(sign, {}).get("name_slot_count"),
                "sa_modal": p103.get(sign, {}).get("sa_modal"),
                "pattern_types": p103.get(sign, {}).get("pattern_types"),
            },
            "standing_anchor": {
                "reading": anchor.get("reading"),
                "confidence": anchor.get("confidence"),
            },
            "verdict": v,
            "rationale": rationale,
        }
        results.append(entry)
        print(
            f"  {sign}: freq={p['freq']} INIT={p['initial_rate']:.0%} "
            f"MED={p['medial_rate']:.0%} TERM={p['terminal_rate']:.0%} "
            f"name_slots={p['name_slot_count']} -> {v}"
        )

    try:
        from glossa_lab.gpu_utils import detect_device  # noqa: PLC0415

        gpu_device = str(detect_device())
    except Exception:  # noqa: BLE001
        gpu_device = "unavailable (torch not installed); CPU positional analysis only"

    report = {
        "_citation": ["A.13", "C.1", "C.2"],
        "phase": 105,
        "title": "Positional/formula adjudication of Phase-103 personal-name candidates",
        "method": (
            "Phase-101 style: per-sign positional profile + Phase-103 name-slot "
            "patterns computed from the Holdat corpus; classifier comparison "
            "class = Phase-103 ANIMAL_CLASSIFIERS set."
        ),
        "classifier_comparison": {
            "aggregate_freq": clf_freq,
            "aggregate_initial_rate": round(clf_init_rate, 4),
            "per_sign": {s: clf_profiles[s] for s in sorted(clf_profiles)},
        },
        "m293_reference_profile": M293_REFERENCE,
        "anchors_modified": False,
        "anchor_note": (
            "All four candidates already stand as HIGH anchors in "
            "INDUS_FINAL_ANCHORS.json; this phase adjudicates the "
            "personal-name-component role only and changes no anchor."
        ),
        "gpu_device": gpu_device,
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
