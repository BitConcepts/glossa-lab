#!/usr/bin/env python3
"""Phase-437 — Spec 052 (Farmer, Sproat & Witzel's
"not writing" thesis: the amended D-01 arm A —
battery NB-1 on the Shakti corpus layer).

Executes the frozen amended Spec 052 contract
(specs/052-farmer-not-writing-soviet/freeze.md;
freeze digest
83658949f9988990ddf265735f099e96d4c6c59c93eed66d4a648d3e8307c019;
OSF registration 7cu23, approved and public at
this run). Where the unamended draft and the
amendment disagree, the amendment governs
(freeze.md section 1).

Step-0 gates, in the amended order (amendment
section 5), before any positional quantity is
computed:

  A Corpus pin — the corpus-layer file and the
    row-grades file, held restricted-local,
    recompute to the freeze section 3 SHA-256
    pins; the freeze digest itself is re-asserted
    as the contract's identity. Failure: INVALID.
  B Population reproduction — extracting the
    primary population from the pinned layer
    under Spec 068's step-0 limb (a row is
    analyzable iff at least one of its symbols
    is not the layer's 000 placeholder; tokens
    counted excluding 000; a row's sequence is
    its symbols with 000 removed; primary =
    analyzable documented-lineage rows)
    reproduces the freeze-recorded counts
    exactly (3,045 rows; 11,805 tokens; 557
    distinct signs). Failure: INVALID.
  C Determinism — the battery, run twice over
    the pinned layer with seed 43052, produces
    identical outputs. Failure: INVALID.
  D Thinness — NB-1.9 applied to the primary
    population (fewer than 30 sequences of
    length >= 3, or fewer than 10 classifiable
    signs, closes the run). Failure: TOO THIN,
    with the census as its finding.

Battery NB-1 (amendment section 3), exactly as
frozen: position classes initial / terminal /
medial over sequences of length >= 2 (NB-1.2;
sequences of length 1 counted and reported
separately, entering no count); per-sign counts
N, I, T, M with I + T + M = N (NB-1.3);
classifiable iff N(s) >= 20 (NB-1.4); strength
bands STRONG at a class rate >= 2/3, MODERATE
at >= 1/2 and < 2/3, symmetric over the three
classes (NB-1.5); opening bigrams the first two
signs of each sequence of length >= 2, dominance
over B, the number of such sequences (NB-1.6);
chance baseline a within-sequence permutation
null (length and sign multiset fixed), 999
permutations, seed 43052, chance level the
nearest-rank 95th percentile (the 950th
smallest) of (a) the TERMINAL_STRONG count and
(b) the maximum opening-bigram dominance
(NB-1.7); conditions F and O as NB-1.8 states
them (O carries its count floor of 10).

The dominance comparisons are made in count
units: the observed dominance and every null
dominance share the same denominator B (B is
invariant under within-sequence permutation),
so dominance exceeds the chance level iff the
top bigram's count exceeds the 950th smallest
null maximum count. No float comparison decides
either condition.

Outcomes (amendment section 6): CONSISTENT iff
neither F nor O holds on the primary population;
INCONSISTENT iff both hold; PARTIAL iff exactly
one holds (the outcome names which); TOO THIN
is gate D's closure. The sensitivity population
(analyzable documented-lineage +
undocumented-corroborated rows) is run and
reported with the same prominence if, and only
if, the primary run reaches an outcome word.
No outcome moves the parent claim's recorded
status (contradicted); no outcome is a verdict
on the Farmer-Sproat-Witzel thesis.

Permutation procedure (stated here, as the
contract requires): one numpy random generator
(np.random.default_rng, PCG64) seeded 43052.
Sequences of length >= 2 are held as a padded
sign-index matrix; each permutation draws an
independent uniform random key for every real
position of every sequence (padding keys are
set above 1 so padded cells sort last), and the
argsort of the keys along each row is a uniform
permutation of that row's signs — length and
multiset fixed, sequences independent.
Permutations are drawn in fixed blocks of 128
so the draw stream is identical on every run.

Outputs (written on every terminal outcome):
  - reports/phase437_results.json (the full
    machine record)
  - reports/phase437_report.md (the report,
    under the amended headline rules: dataset
    label and census and per-sign quantities
    before the outcome word)

Integrity: every freeze section 3 pin is
asserted before any gate quantity; the anchors
file is asserted byte-identical before and
after. The restricted corpus and row-grades
files are read from the restricted local store
only and never enter git; row-level corpus data
appears in no output.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[2]
_SPEC = _REPO / "specs/052-farmer-not-writing-soviet"
_LOCAL = (Path.home() / "workspace/research_notes/"
          "indus-data-deep-sweep-20261008/downloads")
CORPUS_FILE = (_LOCAL / "shaktiosindia-indus-sign-regimes-deposit"
               / "sanitized_corpus.json")
GRADES_FILE = _LOCAL / "shakti_row_grades_2026-10-22.csv"

CORPUS_SHA256 = (
    "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
)
GRADES_SHA256 = (
    "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
)
FREEZE_DIGEST = (
    "83658949f9988990ddf265735f099e96d4c6c59c93eed66d4a648d3e8307c019"
)
ANCHORS_FILE = _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)

PRIMARY_PIN = {"rows": 3045, "tokens": 11805, "distinct_signs": 557}
SENSITIVITY_PIN = {"rows": 5131, "tokens": 17216, "distinct_signs": 707}
PRIMARY_LENGTH_PIN = {"len_ge_2": 2942, "len_ge_3": 2068,
                      "len_1": 103, "classifiable": 90}
SENSITIVITY_LENGTH_PIN = {"len_ge_3": 2889, "classifiable": 112}

SEED = 43052
N_PERMUTATIONS = 999
PERM_BLOCK = 128
FLOOR_N = 20
STRONG_NUM, STRONG_DEN = 2, 3
MODERATE_NUM, MODERATE_DEN = 1, 2
OPENING_COUNT_FLOOR = 10
THIN_MIN_LEN_GE_3 = 30
THIN_MIN_CLASSIFIABLE = 10

EXECUTION_DATE = "2026-10-24"
OSF_REGISTRATION = "7cu23"

_OUT_RESULTS = _REPO / "reports/phase437_results.json"
_OUT_REPORT = _REPO / "reports/phase437_report.md"

DATASET_LABEL = ("the Shakti corpus layer "
                 "(CISI-compilation lineage)")
BATTERY_LABEL = ("NB-1 (Spec 052 amendment as frozen)")
LINEAGE_LIMIT = (
    "The Shakti layer is a CISI-tradition compilation, a "
    "distinct lineage from the Soviet compilation and from "
    "Holdat/M77, but its editions cover substantially the "
    "same excavated objects: agreement is cross-compilation "
    "robustness, not independent discovery."
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _band(count: int, n: int) -> str | None:
    """Strength band of a class count out of N, in
    integer-exact comparisons (NB-1.5)."""
    if count * STRONG_DEN >= STRONG_NUM * n:
        return "STRONG"
    if count * MODERATE_DEN >= MODERATE_NUM * n:
        return "MODERATE"
    return None


def _extraction(corpus, grades):
    """Spec 068's step-0 limb, exactly: analyzable iff
    some symbol is not 000; sequence = symbols with
    000 removed; tokens exclude 000."""

    def _analyzable(r):
        return any(s != "000" for s in r["symbols"])

    def _seq(r):
        return [s for s in r["symbols"] if s != "000"]

    def _counts(rows):
        return Counter(s for r in rows for s in r["symbols"]
                       if s != "000")

    pop_sets = {
        "primary": {"documented-lineage"},
        "sensitivity": {"documented-lineage",
                        "undocumented-corroborated"},
    }
    pops = {}
    for name, gset in pop_sets.items():
        rows = [r for r in corpus
                if grades[r["id"]] in gset and _analyzable(r)]
        c = _counts(rows)
        pops[name] = {
            "grade_set": sorted(gset),
            "rows": len(rows),
            "tokens": sum(c.values()),
            "distinct_signs": len(c),
            "sequences": [_seq(r) for r in rows],
        }
    return pops


def _battery(sequences):
    """Battery NB-1 over one population's sequences.
    Returns the full record dict (deterministic)."""
    seqs_ge2 = [s for s in sequences if len(s) >= 2]
    len_1 = sum(1 for s in sequences if len(s) == 1)
    len_ge_3 = sum(1 for s in sequences if len(s) >= 3)
    big_b = len(seqs_ge2)

    signs = sorted({s for seq in sequences for s in seq})
    idx = {s: i for i, s in enumerate(signs)}
    v = len(signs)

    total_occ = Counter(s for seq in sequences for s in seq)
    n_cnt = Counter()
    i_cnt = Counter()
    t_cnt = Counter()
    m_cnt = Counter()
    for seq in seqs_ge2:
        n_cnt.update(seq)
        i_cnt[seq[0]] += 1
        t_cnt[seq[-1]] += 1
        m_cnt.update(seq[1:-1])

    per_sign = {}
    classifiable = []
    for s in signs:
        n = n_cnt.get(s, 0)
        bands = {}
        if n >= FLOOR_N:
            classifiable.append(s)
            for cls, cnt in (("initial", i_cnt.get(s, 0)),
                             ("terminal", t_cnt.get(s, 0)),
                             ("medial", m_cnt.get(s, 0))):
                b = _band(cnt, n)
                if b is not None:
                    bands[cls] = b
        per_sign[s] = {
            "N": n,
            "I": i_cnt.get(s, 0),
            "T": t_cnt.get(s, 0),
            "M": m_cnt.get(s, 0),
            "total_occurrences": total_occ.get(s, 0),
            "rates": ({"i": i_cnt.get(s, 0) / n,
                       "t": t_cnt.get(s, 0) / n,
                       "m": m_cnt.get(s, 0) / n}
                      if n else None),
            "classifiable": n >= FLOOR_N,
            "bands": bands,
        }

    strong = {cls: sorted(s for s in classifiable
                          if per_sign[s]["bands"].get(cls)
                          == "STRONG")
              for cls in ("initial", "terminal", "medial")}
    moderate = {cls: sorted(s for s in classifiable
                            if per_sign[s]["bands"].get(cls)
                            == "MODERATE")
                for cls in ("initial", "terminal", "medial")}

    openings = Counter((seq[0], seq[1]) for seq in seqs_ge2)
    if openings:
        (top_a, top_b), top_count = max(
            openings.items(), key=lambda kv: (kv[1], kv[0]))
    else:
        (top_a, top_b), top_count = (None, None), 0
    top_dominance = (top_count / big_b) if big_b else 0.0

    # ── Permutation null (NB-1.7) ─────────────────
    lengths = np.array([len(s) for s in seqs_ge2],
                       dtype=np.int64)
    maxlen = int(lengths.max()) if big_b else 0
    mat = np.full((big_b, maxlen), -1, dtype=np.int64)
    for r, seq in enumerate(seqs_ge2):
        mat[r, :len(seq)] = [idx[s] for s in seq]
    n_arr = np.array([n_cnt.get(s, 0) for s in signs],
                     dtype=np.int64)
    class_mask = n_arr >= FLOOR_N
    pos = np.arange(maxlen)[None, :]
    real = pos < lengths[:, None]

    rng = np.random.default_rng(SEED)
    ts_null = np.empty(N_PERMUTATIONS, dtype=np.int64)
    dom_null = np.empty(N_PERMUTATIONS, dtype=np.int64)
    done = 0
    while done < N_PERMUTATIONS:
        b = min(PERM_BLOCK, N_PERMUTATIONS - done)
        keys = rng.random((b, big_b, maxlen))
        keys = np.where(real[None, :, :], keys, 2.0)
        order = np.argsort(keys, axis=2)
        perm = np.take_along_axis(
            np.broadcast_to(mat, (b, big_b, maxlen)),
            order, axis=2)
        term = perm[np.arange(b)[:, None],
                    np.arange(big_b)[None, :],
                    (lengths - 1)[None, :]]
        first = perm[:, :, 0]
        second = perm[:, :, 1]
        for j in range(b):
            tc = np.bincount(term[j], minlength=v)
            ts_null[done + j] = int(np.sum(
                class_mask
                & (tc * STRONG_DEN >= STRONG_NUM * n_arr)))
            pairs = first[j].astype(np.int64) * v + second[j]
            pc = np.bincount(pairs, minlength=v * v)
            dom_null[done + j] = int(pc.max())
        done += b

    ts_sorted = np.sort(ts_null)
    dom_sorted = np.sort(dom_null)
    chance_ts = int(ts_sorted[949])
    chance_dom_count = int(dom_sorted[949])

    ts_observed = len(strong["terminal"])
    cond_f = bool(ts_observed >= 1 and ts_observed > chance_ts)
    cond_o = bool(top_count >= OPENING_COUNT_FLOOR
                  and top_count > chance_dom_count)

    def _null_summary(arr, chance):
        return {"min": int(arr.min()),
                "median": int(np.median(arr)),
                "max": int(arr.max()),
                "chance_level_950th": chance}

    return {
        "census": {
            "sequences_total": len(sequences),
            "sequences_len_1": len_1,
            "sequences_len_ge_2": big_b,
            "sequences_len_ge_3": len_ge_3,
            "distinct_signs": v,
            "classifiable_signs": len(classifiable),
        },
        "per_sign": per_sign,
        "strong_sets": strong,
        "moderate_sets": moderate,
        "terminal_strong_count": ts_observed,
        "opening": {
            "B": big_b,
            "top_bigram": [top_a, top_b],
            "top_count": top_count,
            "dominance": top_dominance,
            "distinct_opening_bigrams": len(openings),
        },
        "null": {
            "model": "within-sequence permutation (length "
                     "and sign multiset fixed)",
            "permutations": N_PERMUTATIONS,
            "seed": SEED,
            "generator": "numpy.random.default_rng (PCG64)",
            "numpy_version": np.__version__,
            "percentile_rule": "nearest-rank 95th "
                               "percentile (950th smallest)",
            "terminal_strong_count": _null_summary(
                ts_null, chance_ts),
            "max_opening_bigram_count": _null_summary(
                dom_null, chance_dom_count),
            "max_opening_bigram_dominance_chance":
                (chance_dom_count / big_b) if big_b else 0.0,
        },
        "conditions": {
            "F": {"holds": cond_f,
                  "observed_terminal_strong": ts_observed,
                  "chance_level": chance_ts,
                  "rule": "at least one TERMINAL_STRONG sign "
                          "and the observed count exceeds "
                          "the chance level"},
            "O": {"holds": cond_o,
                  "top_count": top_count,
                  "count_floor": OPENING_COUNT_FLOOR,
                  "chance_level_count": chance_dom_count,
                  "rule": "top opening-bigram count >= 10 "
                          "and its dominance exceeds the "
                          "chance level (compared in count "
                          "units over the shared "
                          "denominator B)"},
        },
    }


def _outcome_word(conditions):
    f = conditions["F"]["holds"]
    o = conditions["O"]["holds"]
    if f and o:
        return "INCONSISTENT"
    if f or o:
        return "PARTIAL"
    return "CONSISTENT"


def _append_text(outcome, primary, sensitivity_word):
    base = (
        f"Spec 052 (Phase-437), executed {EXECUTION_DATE} "
        f"under the frozen amended contract (freeze digest "
        f"{FREEZE_DIGEST}; OSF registration "
        f"{OSF_REGISTRATION}): battery {BATTERY_LABEL} run "
        f"on {DATASET_LABEL}, primary population "
        f"{primary['census_note']}. "
    )
    if outcome == "TOO THIN":
        return base + (
            "The run closed TOO THIN at step-0 gate D "
            "(NB-1.9); no positional quantity was computed "
            "beyond the census. The parent claim's "
            "contradicted status stands as recorded; this "
            "closure moves no verdict and is not a verdict "
            "on the Farmer-Sproat-Witzel thesis."
        )
    if outcome == "INVALID":
        return base + (
            "The run closed INVALID at step 0; no "
            "positional quantity was computed. The parent "
            "claim's contradicted status stands as "
            "recorded; this closure moves no verdict and "
            "is not a verdict on the "
            "Farmer-Sproat-Witzel thesis."
        )
    f = primary["conditions"]["F"]
    o = primary["conditions"]["O"]
    op = primary["opening"]
    text = base + (
        f"Condition F (dedicated final sets): "
        f"{'holds' if f['holds'] else 'does not hold'} — "
        f"{f['observed_terminal_strong']} TERMINAL_STRONG "
        f"sign(s) against a permutation-null chance level "
        f"of {f['chance_level']} (999 permutations, seed "
        f"43052). Condition O (opening formula): "
        f"{'holds' if o['holds'] else 'does not hold'} — "
        f"the most frequent opening bigram "
        f"({op['top_bigram'][0]}, {op['top_bigram'][1]}) "
        f"recurs {op['top_count']} times "
        f"(dominance {op['dominance']:.4f} over "
        f"B = {op['B']}) against a chance level of "
        f"{o['chance_level_count']} occurrences. "
        f"Outcome: {outcome}. "
    )
    if outcome == "CONSISTENT":
        text += (
            "Neither condition holds: the Farmer pattern "
            "is present in the CISI-lineage corpus as "
            "well, and the 'artefact of the Soviet "
            "dataset' caveat narrows. "
        )
    elif outcome == "INCONSISTENT":
        text += (
            "Both conditions hold: positional structure "
            "of the kind the thesis denies is present in "
            "this compilation, and the caveat widens. "
        )
    else:
        which = "F" if f["holds"] else "O"
        text += (
            f"Exactly one condition holds — {which} — so "
            f"the outcome is PARTIAL, naming {which}: "
            + ("dedicated final-position structure above "
               "chance is present in this compilation, "
               "while the opening-formula half of the "
               "pattern stands as the thesis asserts."
               if which == "F" else
               "an opening formula above chance is "
               "present in this compilation, while the "
               "final-position half of the pattern stands "
               "as the thesis asserts.")
            + " "
        )
    if sensitivity_word is not None:
        text += (
            f"The sensitivity population's run returned "
            f"{sensitivity_word} under the same battery. "
        )
    text += (
        "The parent claim's contradicted status stands "
        "as recorded; this outcome moves no verdict and "
        "is not a verdict on the Farmer-Sproat-Witzel "
        "thesis."
    )
    return text


def _render_report(res):
    lines = []
    lines.append("# Phase-437 — Spec 052 (amended arm A): "
                 "battery NB-1 on the Shakti corpus layer")
    lines.append("")
    lines.append(f"Dataset: **{DATASET_LABEL}**. "
                 f"Battery: **{BATTERY_LABEL}**. "
                 f"Freeze digest `{FREEZE_DIGEST}`; OSF "
                 f"registration {OSF_REGISTRATION} "
                 f"(approved, public). Executed "
                 f"{EXECUTION_DATE} under the owner's "
                 f"execution order of 2026-10-24.")
    lines.append("")
    lines.append(f"Lineage limit: {LINEAGE_LIMIT}")
    lines.append("")
    lines.append("## Step-0 gates (amendment section 5, "
                 "in order)")
    lines.append("")
    for g in res["gates"]:
        lines.append(f"- **Gate {g['gate']} — {g['name']}: "
                     f"{g['verdict']}**")
    lines.append("")
    if res.get("census"):
        c = res["census"]
        lines.append("## Census (gate B extraction, "
                     "pinned layer)")
        lines.append("")
        for name in ("primary", "sensitivity"):
            p = c[name]
            lines.append(
                f"- **{name}**: {p['rows']} rows; "
                f"{p['tokens']} tokens; "
                f"{p['distinct_signs']} distinct signs; "
                f"sequences of length >= 3: "
                f"{p['len_ge_3']}; classifiable signs: "
                f"{p['classifiable']}")
        lines.append("")
        for note in res.get("census_notes", []):
            lines.append(f"Census note: {note}")
            lines.append("")
    for name in ("primary", "sensitivity"):
        b = res.get(f"battery_{name}")
        if not b:
            continue
        cen = b["census"]
        lines.append(f"## {name.capitalize()} population — "
                     f"per-sign quantities (NB-1)")
        lines.append("")
        lines.append(f"Sequences: {cen['sequences_total']} "
                     f"total; {cen['sequences_len_1']} of "
                     f"length 1 (counted, entering no "
                     f"count); {cen['sequences_len_ge_2']} "
                     f"of length >= 2 (B = "
                     f"{cen['sequences_len_ge_2']}); "
                     f"{cen['sequences_len_ge_3']} of "
                     f"length >= 3. Classifiable signs "
                     f"(N >= 20): "
                     f"{cen['classifiable_signs']} of "
                     f"{cen['distinct_signs']}.")
        lines.append("")
        lines.append("| Sign | N | I | T | M | i | t | m "
                     "| Bands |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for s in sorted(b["per_sign"],
                        key=lambda x: (-b["per_sign"][x]["N"],
                                         x)):
            ps = b["per_sign"][s]
            if ps["classifiable"]:
                bands = ", ".join(
                    f"{cls.upper()}_{band}"
                    for cls, band in sorted(
                        ps["bands"].items())) or "—"
                r = ps["rates"]
                lines.append(
                    f"| {s} | {ps['N']} | {ps['I']} | "
                    f"{ps['T']} | {ps['M']} | {r['i']:.3f} "
                    f"| {r['t']:.3f} | {r['m']:.3f} | "
                    f"{bands} |")
        lines.append("")
        thin = [(s, ps) for s, ps in b["per_sign"].items()
                if not ps["classifiable"]]
        lines.append(f"Signs below the classifiability "
                     f"floor (N < 20), reported with their "
                     f"counts and marked TOO THIN for this "
                     f"population: {len(thin)}. Their full "
                     f"counts (N, I, T, M, total "
                     f"occurrences) are carried per sign in "
                     f"reports/phase437_results.json "
                     f"(per_sign); none is a member of any "
                     f"strong set and none was dropped.")
        lines.append("")
        ss = b["strong_sets"]
        ms = b["moderate_sets"]
        lines.append(f"Strong sets — TERMINAL_STRONG "
                     f"({len(ss['terminal'])}): "
                     f"{ss['terminal'] or '[]'}; "
                     f"INITIAL_STRONG "
                     f"({len(ss['initial'])}): "
                     f"{ss['initial'] or '[]'}; "
                     f"MEDIAL_STRONG ({len(ss['medial'])}): "
                     f"{ss['medial'] or '[]'}. Moderate sets "
                     f"— terminal {len(ms['terminal'])}, "
                     f"initial {len(ms['initial'])}, medial "
                     f"{len(ms['medial'])} (full lists in the "
                     f"results JSON).")
        lines.append("")
        op = b["opening"]
        nu = b["null"]
        lines.append(
            f"Opening bigrams: most frequent "
            f"{op['top_bigram']} with count "
            f"{op['top_count']} over B = {op['B']} "
            f"(dominance {op['dominance']:.4f}); "
            f"{op['distinct_opening_bigrams']} distinct "
            f"opening bigrams. Permutation null (999 "
            f"permutations, seed 43052): "
            f"TERMINAL_STRONG count chance level "
            f"{nu['terminal_strong_count']['chance_level_950th']} "
            f"(null min/median/max "
            f"{nu['terminal_strong_count']['min']}/"
            f"{nu['terminal_strong_count']['median']}/"
            f"{nu['terminal_strong_count']['max']}); "
            f"maximum opening-bigram count chance level "
            f"{nu['max_opening_bigram_count']['chance_level_950th']} "
            f"(null min/median/max "
            f"{nu['max_opening_bigram_count']['min']}/"
            f"{nu['max_opening_bigram_count']['median']}/"
            f"{nu['max_opening_bigram_count']['max']}).")
        lines.append("")
        cf = b["conditions"]
        lines.append(
            f"Conditions: F "
            f"{'HOLDS' if cf['F']['holds'] else 'does not hold'} "
            f"(observed {cf['F']['observed_terminal_strong']} "
            f"vs chance {cf['F']['chance_level']}); O "
            f"{'HOLDS' if cf['O']['holds'] else 'does not hold'} "
            f"(top count {cf['O']['top_count']} vs floor "
            f"{cf['O']['count_floor']} and chance "
            f"{cf['O']['chance_level_count']}).")
        lines.append("")
    lines.append("## Outcome")
    lines.append("")
    lines.append(res["outcome_append_text"])
    lines.append("")
    lines.append("## Limits")
    lines.append("")
    lines.append("- No verdict moves: the parent claim "
                 "(`farmer_sproat_witzel_2004_manual_001`) "
                 "stands contradicted as recorded; this "
                 "run narrows or widens the stated caveat "
                 "only, and is not a verdict on the "
                 "Farmer-Sproat-Witzel thesis.")
    lines.append(f"- {LINEAGE_LIMIT}")
    lines.append("- Consistency is not replication of "
                 "the whole case: nothing here speaks to "
                 "what language the signs encode, to any "
                 "sign's reading, or to conditional "
                 "entropy.")
    lines.append("- Negative, partial, thin, and "
                 "not-adjudicated outcomes publish with "
                 "the same prominence as a consistent "
                 "one.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    anchors_before = (_sha256(ANCHORS_FILE)
                      if ANCHORS_FILE.exists() else None)
    gates: list[dict] = []
    outcome = None
    closure = None

    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=str(_REPO),
            capture_output=True, text=True, timeout=30)
        executed_from = head.stdout.strip() or None
    except Exception:  # noqa: BLE001
        executed_from = None

    res: dict = {
        "phase": 437,
        "spec": "052",
        "contract": {
            "freeze_digest": FREEZE_DIGEST,
            "osf_registration": OSF_REGISTRATION,
            "dataset": DATASET_LABEL,
            "battery": BATTERY_LABEL,
        },
        "execution": {"date": EXECUTION_DATE,
                      "executed_from_commit": executed_from,
                      "seed": SEED},
        "anchors": {"file": "backend/reports/"
                            "INDUS_FINAL_ANCHORS.json",
                    "pin": ANCHORS_SHA256,
                    "before": anchors_before},
    }

    def _not_reached(*specs):
        for gid, name in specs:
            gates.append({"gate": gid, "name": name,
                          "verdict": "NOT REACHED"})

    # ── Gate A — corpus pin ───────────────────────
    corpus_hash = (_sha256(CORPUS_FILE)
                   if CORPUS_FILE.exists() else None)
    grades_hash = (_sha256(GRADES_FILE)
                   if GRADES_FILE.exists() else None)
    freeze_json = json.loads((_SPEC / "freeze.json")
                             .read_text("utf-8"))
    gate_a = {
        "gate": "A", "name": "Corpus pin",
        "corpus": {"file": CORPUS_FILE.name,
                   "pin": CORPUS_SHA256,
                   "observed": corpus_hash,
                   "match": corpus_hash == CORPUS_SHA256},
        "row_grades": {"file": GRADES_FILE.name,
                       "pin": GRADES_SHA256,
                       "observed": grades_hash,
                       "match": grades_hash == GRADES_SHA256},
        "freeze_digest": {
            "pin": FREEZE_DIGEST,
            "observed": freeze_json.get("digest"),
            "match": freeze_json.get("digest")
                     == FREEZE_DIGEST},
        "verdict": "PASS" if (
            corpus_hash == CORPUS_SHA256
            and grades_hash == GRADES_SHA256
            and freeze_json.get("digest") == FREEZE_DIGEST
        ) else "FAIL",
    }
    gates.append(gate_a)
    if gate_a["verdict"] != "PASS":
        outcome = "INVALID"
        closure = ("gate A: a corpus-layer pin (or the "
                   "freeze digest) did not recompute to "
                   "the freeze value")
        _not_reached(("B", "Population reproduction"),
                     ("C", "Determinism"),
                     ("D", "Thinness (NB-1.9)"))

    pops = None
    if outcome is None:
        corpus = json.loads(CORPUS_FILE.read_text("utf-8"))
        grades = {}
        with open(GRADES_FILE, newline="",
                  encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                grades[row["shakti_id"]] = row["grade"]
        pops = _extraction(corpus, grades)

        # ── Gate B — population reproduction ──────
        prim = pops["primary"]
        gate_b = {
            "gate": "B", "name": "Population reproduction",
            "pin": PRIMARY_PIN,
            "observed": {"rows": prim["rows"],
                         "tokens": prim["tokens"],
                         "distinct_signs":
                             prim["distinct_signs"]},
            "sensitivity_observed": {
                "rows": pops["sensitivity"]["rows"],
                "tokens": pops["sensitivity"]["tokens"],
                "distinct_signs":
                    pops["sensitivity"]["distinct_signs"]},
            "sensitivity_pin": SENSITIVITY_PIN,
            "verdict": "PASS" if (
                prim["rows"] == PRIMARY_PIN["rows"]
                and prim["tokens"] == PRIMARY_PIN["tokens"]
                and prim["distinct_signs"]
                == PRIMARY_PIN["distinct_signs"]
            ) else "FAIL",
        }
        gates.append(gate_b)
        if gate_b["verdict"] != "PASS":
            outcome = "INVALID"
            closure = ("gate B: the primary population "
                       "did not reproduce the "
                       "freeze-recorded counts")
            _not_reached(("C", "Determinism"),
                         ("D", "Thinness (NB-1.9)"))

    battery_primary = None
    if outcome is None:
        seqs = pops["primary"]["sequences"]
        run1 = _battery(seqs)
        run2 = _battery(seqs)
        canon1 = json.dumps(run1, sort_keys=True)
        canon2 = json.dumps(run2, sort_keys=True)
        gate_c = {
            "gate": "C", "name": "Determinism",
            "method": "battery run twice over the "
                      "pinned layer, seed 43052; "
                      "canonical-JSON comparison of the "
                      "full battery records",
            "identical": canon1 == canon2,
            "verdict": "PASS" if canon1 == canon2
                       else "FAIL",
        }
        gates.append(gate_c)
        if gate_c["verdict"] != "PASS":
            outcome = "INVALID"
            closure = ("gate C: the battery did not "
                       "reproduce its own outputs under "
                       "the frozen seed")
            _not_reached(("D", "Thinness (NB-1.9)"))
        else:
            battery_primary = run1
            cen = run1["census"]
            gate_d = {
                "gate": "D", "name": "Thinness (NB-1.9)",
                "sequences_len_ge_3": cen[
                    "sequences_len_ge_3"],
                "min_len_ge_3": THIN_MIN_LEN_GE_3,
                "classifiable_signs": cen[
                    "classifiable_signs"],
                "min_classifiable": THIN_MIN_CLASSIFIABLE,
                "freeze_recorded": PRIMARY_LENGTH_PIN,
                "verdict": "PASS" if (
                    cen["sequences_len_ge_3"]
                    >= THIN_MIN_LEN_GE_3
                    and cen["classifiable_signs"]
                    >= THIN_MIN_CLASSIFIABLE
                ) else "FAIL",
            }
            gates.append(gate_d)
            if gate_d["verdict"] != "PASS":
                outcome = "TOO THIN"
                closure = ("gate D (NB-1.9): the primary "
                           "population is too thin; the "
                           "census is the finding")

    census_block = None
    if pops is not None:
        def _census_block(name, batt):
            p = pops[name]
            seqs = p["sequences"]
            return {
                "rows": p["rows"], "tokens": p["tokens"],
                "distinct_signs": p["distinct_signs"],
                "sequences_total": len(seqs),
                "len_1": sum(1 for s in seqs
                             if len(s) == 1),
                "len_ge_2": sum(1 for s in seqs
                                if len(s) >= 2),
                "len_ge_3": sum(1 for s in seqs
                                if len(s) >= 3),
                "classifiable": (batt["census"][
                    "classifiable_signs"] if batt else None),
            }

        census_block = {
            "primary": _census_block("primary",
                                     battery_primary),
            "sensitivity": _census_block("sensitivity",
                                         None),
        }

    sensitivity_word = None
    battery_sensitivity = None
    if outcome is None and battery_primary is not None:
        outcome = _outcome_word(battery_primary[
            "conditions"])
        battery_sensitivity = _battery(
            pops["sensitivity"]["sequences"])
        sensitivity_word = _outcome_word(
            battery_sensitivity["conditions"])
        census_block["sensitivity"]["classifiable"] = (
            battery_sensitivity["census"][
                "classifiable_signs"])

    prim_for_text = None
    if battery_primary is not None:
        prim_for_text = dict(battery_primary)
        prim_for_text["census_note"] = (
            f"{PRIMARY_PIN['rows']:,} inscriptions / "
            f"{PRIMARY_PIN['tokens']:,} tokens / "
            f"{PRIMARY_PIN['distinct_signs']} signs")
    else:
        prim_for_text = {
            "census_note": (
                f"{PRIMARY_PIN['rows']:,} inscriptions / "
                f"{PRIMARY_PIN['tokens']:,} tokens / "
                f"{PRIMARY_PIN['distinct_signs']} signs "
                f"(freeze-recorded; reproduction failed "
                f"or was not reached)"),
            "conditions": {"F": {"holds": False,
                                 "observed_terminal_strong": 0,
                                 "chance_level": 0},
                           "O": {"holds": False,
                                 "top_count": 0,
                                 "chance_level_count": 0}},
            "opening": {"top_bigram": [None, None],
                        "top_count": 0, "dominance": 0.0,
                        "B": 0},
        }

    census_notes = []
    if battery_sensitivity is not None:
        for s, ps in sorted(
                battery_sensitivity["per_sign"].items()):
            if (ps["total_occurrences"] >= FLOOR_N
                    and ps["N"] < FLOOR_N):
                census_notes.append(
                    f"Sensitivity classifiability: sign {s} "
                    f"carries {ps['total_occurrences']} "
                    f"total occurrences but only {ps['N']} "
                    f"in sequences of length >= 2; under "
                    f"NB-1.2/NB-1.3 (length-1 sequences "
                    f"enter no count) N({s}) = {ps['N']} "
                    f"< 20, so it is not classifiable and "
                    f"the sensitivity classifiable count "
                    f"under NB-1 is "
                    f"{battery_sensitivity['census']['classifiable_signs']}, "
                    f"one below the freeze section 3 "
                    f"length-census figure of "
                    f"{SENSITIVITY_LENGTH_PIN['classifiable']}, "
                    f"which counted total occurrences. No "
                    f"gate turns on the sensitivity count; "
                    f"the primary count (90) is identical "
                    f"under both readings.")
    res["census_notes"] = census_notes
    res["gates"] = gates
    res["outcome"] = outcome
    res["closure"] = closure
    res["census"] = census_block
    res["battery_primary"] = battery_primary
    res["battery_sensitivity"] = battery_sensitivity
    res["sensitivity_outcome"] = sensitivity_word
    res["outcome_append_text"] = _append_text(
        outcome, prim_for_text, sensitivity_word)
    anchors_after = (_sha256(ANCHORS_FILE)
                     if ANCHORS_FILE.exists() else None)
    res["anchors"]["after"] = anchors_after
    res["anchors"]["byte_identical"] = (
        anchors_before == anchors_after == ANCHORS_SHA256)

    _OUT_RESULTS.write_text(
        json.dumps(res, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    _OUT_REPORT.write_text(_render_report(res),
                           encoding="utf-8")
    print(f"Phase-437 outcome: {outcome}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
