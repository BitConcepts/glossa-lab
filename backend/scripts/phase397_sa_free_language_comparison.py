#!/usr/bin/env python3
"""Phase-397 — Spec 033: the SA-free language comparison, executed
exactly as frozen.

WHAT THIS IS
------------
The frozen Spec 033 contract (specs/033-sa-free-language-comparison/,
framework026 digest
412b4805063bbffb3915a834354cb428cc9b10958f614a1680b859005a43b66d,
registered before execution at OSF https://osf.io/ephf7/, DOI
10.17605/OSF.IO/EPHF7) reruns the program's old Dravidian-versus-
Sanskrit sign-sequence comparison with the semantic-anchoring (SA)
machinery removed entirely. No SA method, no anchor promotion, and
no SA-derived quantity appears anywhere in this pipeline (house
rule H26; frozen claims F033-C03, F033-C07).

THE METHOD (spec section 5, frozen at freeze time)
-------------------------------------------------
- Scored unit: one inscription sequence over the strict sign set
  (the 94 anchors the Spec 029 Phase H record stamped
  strict_sa_independent). Sequences are the corpus inscriptions
  filtered to strict signs, order preserved, at least 2 signs.
- Families: Dravidian, Sanskrit, Munda, a no-language baseline
  (anchor signs carry no values), and 999 random assignments drawn
  from the same pool of published values (seed 20261013).
- Under a family's assignment, each anchor sign contributes the
  sound sequence its published value implies; every other strict
  sign contributes its own identity as a single value-free unit.
  Anchor assignments are the cited data frozen, before scoring, in
  specs/033-sa-free-language-comparison/anchors-phase397.json.
- Model: for each assignment, a counted conditional distribution
  of each unit given the preceding unit, estimated from the corpus
  itself under that assignment, with add-one (Laplace) smoothing.
  The first unit of a sequence is scored against a beginning-of-
  sequence context estimated the same way. A sequence's score is
  its total log probability divided by its number of signs; a
  family's score is the mean over all scored sequences. The
  computation is identical for every family and every control.
- Verdict (claims F033-C10/C11/C12/C15; plan section 4): the
  bounded claim is SUPPORTED only if Dravidian beats the best
  rival by at least 0.10 log units per sign AND stands above the
  99th percentile of the 999 random assignments, on the primary
  run. A rival at or above Dravidian, or Dravidian lying inside
  the random assignments' range, makes it NOT SUPPORTED. A
  first-place margin below 0.10, or a reversal when Harappa's
  inscriptions are removed (the pre-registered sensitivity), makes
  it INCONCLUSIVE. The robustness arm (a second anchor list per
  family) is reported beside the outcome and never decides it.

Inputs are checked against the frozen censuses before any score
is computed; a mismatch stops the run (fail-closed). Outputs:
reports/phase397_results.json.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs" / "033-sa-free-language-comparison"
ANCHOR_FREEZE = SPEC_DIR / "anchors-phase397.json"
ANCHORS_FILE = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
RESULTS_FILE = REPO / "reports" / "phase397_results.json"
DEFAULT_CORPUS = (REPO / "glossa-corpus" / "indus" / "exports"
                  / "indus_research.jsonl")

MARGIN = 0.10            # F033-C10 (frozen)
RANDOM_DRAWS = 999       # F033-C09 (frozen)
RANDOM_SEED = 20261013   # procedural constant, recorded in the anchor freeze
BOS = "<BOS>"

_FOLD = {
    "ā": "a", "ī": "i", "ū": "u", "ē": "e", "ō": "o",
    "ṭ": "t", "ḍ": "d", "ṇ": "n", "ṅ": "n", "ñ": "n",
    "ś": "s", "ṣ": "s", "ḷ": "l", "ṛ": "r", "ḥ": "h", "ṉ": "n",
    "T": "t", "N": "n", "L": "l", "X": "x",
}


def fold_value(value: str) -> list[str]:
    """A published value -> its sequence of sound units, by the
    mechanical rule frozen in anchors-phase397.json: first-listed
    alternant, trailing '-X' sign-form marker dropped, apostrophes
    dropped, marked letters folded to base letters, then one
    character per unit."""
    v = value.split("/")[0].strip()
    v = v.split("(")[0].strip()
    if v.endswith("-X"):
        v = v[:-2]
    v = v.replace("'", "").replace("'", "")
    out = []
    for ch in v:
        ch = _FOLD.get(ch, ch)
        for c in unicodedata.normalize("NFKD", ch):
            if unicodedata.combining(c):
                continue
            c = _FOLD.get(c, c)
            if c.isalpha():
                out.append(c.lower())
    return out


def load_strict_signs(path: Path = ANCHORS_FILE) -> tuple[set[str], dict]:
    data = json.loads(path.read_text("utf-8"))
    anchors = data["anchors"]
    strict = {str(int(k[1:])) for k, v in anchors.items()
              if v.get("validation_status") == "strict_sa_independent"}
    return strict, {"anchors_total": len(anchors), "strict": len(strict)}


def clean_tokens(tokens) -> list[str]:
    """The V3 loader's own cleaning rules (indus_corpus_v3): numeric
    Mahadevan ids only; '000'/'0' placeholders and '*'-prefixed
    supplementary tokens dropped."""
    out = []
    for t in tokens or []:
        if t is None:
            continue
        t = str(t)
        if t in ("000", "0") or t.startswith("*"):
            continue
        try:
            out.append(str(int(t)))
        except ValueError:
            continue
    return out


def build_sequences(records, strict: set[str]) -> list[list[str]]:
    """Filter each record's signs to the strict set, order preserved;
    keep sequences of at least 2 signs."""
    seqs = []
    for tokens in records:
        seq = [t for t in clean_tokens(tokens) if t in strict]
        if len(seq) >= 2:
            seqs.append(seq)
    return seqs


def _identity_unit(sign: str) -> str:
    return f"S{int(sign):03d}"


def map_sequence(seq: list[str], mapping: dict[str, list[str]]) -> list[str]:
    units: list[str] = []
    for sign in seq:
        if sign in mapping:
            units.extend(mapping[sign])
        else:
            units.append(_identity_unit(sign))
    return units


def score_sequences(sequences: list[list[str]],
                    mapping: dict[str, list[str]]) -> float:
    """The frozen estimator: counted conditional model with add-one
    smoothing, estimated from the mapped corpus itself; sequence
    score = total log probability / number of signs; family score =
    mean over sequences. Identical for every assignment."""
    mapped = [map_sequence(s, mapping) for s in sequences]
    vocab: set[str] = set()
    for units in mapped:
        vocab.update(units)
    v_size = len(vocab)
    trans: Counter = Counter()
    ctx: Counter = Counter()
    for units in mapped:
        prev = BOS
        for u in units:
            trans[(prev, u)] += 1
            ctx[prev] += 1
            prev = u
    total = 0.0
    for seq, units in zip(sequences, mapped):
        lp = 0.0
        prev = BOS
        for u in units:
            lp += math.log((trans[(prev, u)] + 1) / (ctx[prev] + v_size))
            prev = u
        total += lp / len(seq)
    return total / len(sequences)


def percentile_rank(sorted_scores: list[float], x: float) -> float:
    """Share of the distribution strictly below x, as a percentage."""
    below = sum(1 for s in sorted_scores if s < x)
    return 100.0 * below / len(sorted_scores)


def percentile_value(sorted_scores: list[float], p: float) -> float:
    """The p-th percentile, linear interpolation (numpy default)."""
    n = len(sorted_scores)
    if n == 1:
        return sorted_scores[0]
    rank = (p / 100.0) * (n - 1)
    lo = int(math.floor(rank))
    hi = min(lo + 1, n - 1)
    frac = rank - lo
    return sorted_scores[lo] * (1 - frac) + sorted_scores[hi] * frac


def decide_verdict(dravidian: float, best_rival: float,
                   random_max: float,
                   sensitivity_reversed: bool) -> tuple[str, str]:
    """The frozen verdict procedure (claims F033-C10/C11/C12/C15;
    plan section 4), in the frozen order."""
    margin = dravidian - best_rival
    if best_rival >= dravidian:
        return ("NOT SUPPORTED",
                "a rival assignment scores at or above Dravidian on "
                "the primary run (F033-C11)")
    if dravidian <= random_max:
        return ("NOT SUPPORTED",
                "the Dravidian score lies inside the random "
                "assignments' range (F033-C11)")
    if margin < MARGIN:
        return ("INCONCLUSIVE",
                "Dravidian finishes first but its margin over the "
                "best rival is below 0.10 log units per sign "
                "(F033-C12)")
    if sensitivity_reversed:
        return ("INCONCLUSIVE",
                "the pre-registered Harappa-removed sensitivity "
                "reverses the ranking (F033-C12)")
    return ("SUPPORTED",
            "margin at or above 0.10 log units per sign and the "
            "Dravidian score above the random maximum, hence above "
            "the 99th percentile (F033-C10, F033-C15)")


def _mapping(entries) -> dict[str, list[str]]:
    return {str(e["sign"]): [str(u) for u in e["units"]] for e in entries}


def _family_mapping(anchor_freeze: dict, family: str) -> dict[str, list[str]]:
    return {str(e["sign"]): [str(u) for u in e[family]["units"]]
            for e in anchor_freeze["primary_list"]}


def run(corpus_path: Path = DEFAULT_CORPUS) -> dict:
    anchor_freeze = json.loads(ANCHOR_FREEZE.read_text("utf-8"))
    strict, census = load_strict_signs()
    if (census["anchors_total"], census["strict"]) != (287, 94):
        raise SystemExit(
            f"strict-set census mismatch: {census} (frozen: 287/94)")

    records_all: list[list[str]] = []
    records_no_harappa: list[list[str]] = []
    site_counts: Counter = Counter()
    token_total = 0
    token_strict = 0
    with open(corpus_path, encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec.get("source_system") != "indusscript-m77":
                continue
            toks = clean_tokens(rec.get("canonical_grapheme_ids"))
            token_total += len(toks)
            token_strict += sum(1 for t in toks if t in strict)
            site = rec.get("site_name")
            site_counts[site if site else "site not recorded"] += 1
            records_all.append(rec.get("canonical_grapheme_ids"))
            if site != "Harappa":
                records_no_harappa.append(rec.get("canonical_grapheme_ids"))
    frozen_census = anchor_freeze["corpus"]["census_at_freeze"]
    observed = {"m77_records": len(records_all),
                "tokens_total": token_total, "tokens_strict": token_strict}
    for k, v in observed.items():
        if frozen_census[k] != v:
            raise SystemExit(
                f"corpus census mismatch on {k}: observed {v}, "
                f"frozen {frozen_census[k]} — inputs changed since "
                f"the anchor freeze; stopping (fail-closed)")

    sequences = build_sequences(records_all, strict)
    sequences_sens = build_sequences(records_no_harappa, strict)

    mappings = {
        "dravidian": _family_mapping(anchor_freeze, "dravidian"),
        "sanskrit": _family_mapping(anchor_freeze, "sanskrit"),
        "munda": _family_mapping(anchor_freeze, "munda"),
        "no_language_baseline": {},
    }
    primary = {name: score_sequences(sequences, m)
               for name, m in mappings.items()}
    sensitivity = {name: score_sequences(sequences_sens, m)
                   for name, m in mappings.items()}

    robustness = {}
    for family in ("dravidian", "sanskrit", "munda"):
        m = _mapping(anchor_freeze["robustness_lists"][family]["signs"])
        robustness[family] = score_sequences(sequences, m)

    signs_order = [str(e["sign"]) for e in anchor_freeze["primary_list"]]
    pool: list[list[str]] = []
    for fam in ("dravidian", "sanskrit", "munda"):
        for e in anchor_freeze["primary_list"]:
            pool.append([str(u) for u in e[fam]["units"]])
    rng = random.Random(RANDOM_SEED)
    random_scores: list[float] = []
    for _ in range(RANDOM_DRAWS):
        idx = rng.sample(range(len(pool)), len(signs_order))
        m = {signs_order[j]: pool[idx[j]] for j in range(len(signs_order))}
        random_scores.append(score_sequences(sequences, m))
    random_sorted = sorted(random_scores)

    d = primary["dravidian"]
    rivals = {k: primary[k]
              for k in ("sanskrit", "munda", "no_language_baseline")}
    best_rival_name = max(rivals, key=rivals.get)
    best_rival = rivals[best_rival_name]
    sens_rivals = max(sensitivity[k] for k in rivals)
    sens_reversed = sensitivity["dravidian"] <= sens_rivals
    verdict, rule = decide_verdict(d, best_rival, random_sorted[-1],
                                   sens_reversed)

    return {
        "phase": 397,
        "spec": "033-sa-free-language-comparison",
        "date": "2026-10-13",
        "frozen_contract": {
            "digest": "412b4805063bbffb3915a834354cb428cc9b10958"
                      "f614a1680b859005a43b66d",
            "osf_registration": "https://osf.io/ephf7/",
            "doi": "10.17605/OSF.IO/EPHF7",
        },
        "inputs": {
            "anchor_freeze_file": "specs/033-sa-free-language-comparison"
                                  "/anchors-phase397.json",
            "anchor_freeze_sha256": hashlib.sha256(
                ANCHOR_FREEZE.read_bytes()).hexdigest(),
            "anchors_file_sha256": hashlib.sha256(
                ANCHORS_FILE.read_bytes()).hexdigest(),
            "corpus_file": (str(corpus_path.relative_to(REPO))
                            if corpus_path.is_relative_to(REPO)
                            else str(corpus_path)),
            "corpus_file_sha256": hashlib.sha256(
                corpus_path.read_bytes()).hexdigest(),
        },
        "census": {
            "anchors_total": census["anchors_total"],
            "strict_signs": census["strict"],
            **observed,
            "records_by_site_as_held": dict(site_counts),
            "scored_sequences_primary": len(sequences),
            "scored_sequences_harappa_removed": len(sequences_sens),
        },
        "primary_run": {
            "scores_mean_log_prob_per_sign": primary,
            "best_rival": best_rival_name,
            "best_rival_score": best_rival,
            "margin_dravidian_minus_best_rival": d - best_rival,
            "frozen_margin_bar": MARGIN,
        },
        "sensitivity_harappa_removed": {
            "scores_mean_log_prob_per_sign": sensitivity,
            "dravidian_still_first": not sens_reversed,
            "note": "Removes the 110 records whose held site label is "
                    "Harappa; 1,940 records carry no site label in the "
                    "held corpus and are kept as held (limitation "
                    "recorded in the anchor freeze).",
        },
        "robustness_arm": {
            "scores_mean_log_prob_per_sign": robustness,
            "note": "Second anchor list per family (F033-C13), identical "
                    "pipeline, primary corpus. Reported beside the "
                    "outcome; never decides the verdict. The Munda "
                    "list has four signs — the published record offers "
                    "no fifth citable candidate (anchor freeze).",
        },
        "random_controls": {
            "draws": RANDOM_DRAWS,
            "seed": RANDOM_SEED,
            "min": random_sorted[0],
            "mean": sum(random_sorted) / len(random_sorted),
            "median": percentile_value(random_sorted, 50),
            "p99": percentile_value(random_sorted, 99),
            "max": random_sorted[-1],
            "percentile_of_each_family": {
                name: percentile_rank(random_sorted, s)
                for name, s in primary.items()},
            "scores": [round(s, 6) for s in random_scores],
        },
        "verdict": {
            "verdict": verdict,
            "rule_fired": rule,
            "bounded_claim": "Dravidian assignments fit the Indus "
                             "sign sequences better than the named "
                             "rival assignments (Sanskrit, Munda, "
                             "no-language) under this method, within "
                             "the Mahadevan lineage (F033-C01, C14).",
        },
        "does_not_establish": [
            "not the rebus method",
            "not any single sign reading",
            "not a decipherment of the Indus script",
            "a verdict here is a within-lineage statistical fit only: "
            "every corpus in the program descends from the Mahadevan "
            "compilation, so no independent-corpus replication exists",
        ],
    }


def main() -> int:
    corpus = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CORPUS
    results = run(corpus)
    RESULTS_FILE.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(json.dumps({
        "primary": results["primary_run"]["scores_mean_log_prob_per_sign"],
        "best_rival": results["primary_run"]["best_rival"],
        "margin": results["primary_run"]
                  ["margin_dravidian_minus_best_rival"],
        "random": {k: results["random_controls"][k]
                   for k in ("min", "mean", "median", "p99", "max")},
        "percentiles": results["random_controls"]
                       ["percentile_of_each_family"],
        "sensitivity": results["sensitivity_harappa_removed"]
                       ["scores_mean_log_prob_per_sign"],
        "robustness": results["robustness_arm"]
                      ["scores_mean_log_prob_per_sign"],
        "verdict": results["verdict"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
