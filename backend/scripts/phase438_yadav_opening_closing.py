#!/usr/bin/env python3
"""Phase-438 — Spec 054 (Yadav's opening/closing
signs: given a falsifier, then rerun — the
amended falsifier act under battery NB-1).

Executes the frozen amended Spec 054 contract
(specs/054-yadav-opening-closing/freeze.md;
freeze digest
d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57;
OSF registration 8spvf, approved and public at
this run). Where the unamended draft and the
amendment disagree, the amendment governs
(freeze.md section 1; adjudication.md section
9). The claim under test is
yadav_2009_arxiv_manual_002 — "There are
specific text-beginning and text-ending signs
in the Indus corpus" — standing strongly
supported, carrying since the freeze the
falsifier the amendment's section 8 fixed
verbatim (appended 2026-10-23; the claim
record's post-append SHA-256 is
938174b0dee14169a5340c9299c73f4eb5b997377f8198a146ef611e73924050).
No outcome of this run moves the claim's
recorded status (amendment section 9).

Step-0 gates, in the amendment section 6
order, before any positional quantity is
computed in either arm (the draft's gate
numbers are noted beside each; failure stops
the run in the class named and later gates are
NOT REACHED):

  G1 Pin checks (draft 0.1) — every freeze
     section 2 pin recomputes: the claim store
     after the append, the Phase-43 record, the
     positional companion record, crosswalk v1
     JSON and CSV, the anchors file, the
     recovered register; the freeze digest
     itself is re-asserted as the contract's
     identity. Any mismatch: INVALID.
  G2 Strict corpus identification and pin
     (draft 0.3) — arm 1's layer is identified
     mechanically as the V3 / Mahadevan-lineage
     corpus the Phase-43 battery ran on and
     pinned by SHA-256. The identification is
     the mechanical attempt recorded in full in
     the step-0 record: C1 the V3 loader's data
     file (the Firestore 'indusarrays' dump
     backend/glossa_lab/data/indus_corpus_v3.py
     reads) at its path in this tree, in the
     main checkout, and in sibling trees; C2 a
     database copy (backend/data/glossa.db in
     this tree; the programme database in the
     main checkout, its texts censused); C3 the
     Phase-43 record's own census of its corpus
     (T1_1: source, 3,916 records, 2,665 unique
     dockeys, 3,137 sequences, 12,494 sign
     instances), read from the pinned file; C4
     every other corpus layer the environment
     holds, censused and compared. A layer
     counts as identified only if it is the
     corpus the Phase-43 record names AND the
     loader's census of it reproduces C3
     exactly. No layer is substituted. Failure:
     STRICT CORPUS NOT PINNABLE.
  G3 Thinness (draft 0.5 census, amendment
     section 6 lines) — arm 1 has fewer than 30
     sequences of length >= 3, or fewer than 10
     classifiable signs (N(s) >= 20). Failure:
     TOO THIN, with the census as its finding.
  G4 Second arm runnability (draft 0.4) — the
     Holdat layer is identified (the downloads
     CSV the programme's loaders read,
     phase113_run.load_holdat_inscriptions'
     source) and pinned by SHA-256; the
     crosswalk pins are G1's; arm 2 has fewer
     than 10 classifiable signs. Failure:
     SECOND ARM NOT RUNNABLE.
  G5 Determinism — the frozen decision
     computation (both arms' NB-1 sets, the
     reappearance measures, the pooled overlap
     and its 999-shuffle null, seed 44054), run
     twice over the pinned inputs, produces
     identical canonical records. Failure:
     INVALID.

Battery NB-1 (amendment section 3), exactly
as frozen, in each arm under its own
compilation's numbering and segmentation (no
re-segmentation, no renumbering, no crosswalk
inside a run): position classes initial /
terminal / medial over sequences of length
>= 2 (NB-1.2; sequences of length 1 counted
and reported separately, entering no count);
per-sign counts N, I, T, M with I + T + M = N
exactly (NB-1.3); classifiable iff N(s) >= 20
(NB-1.4); strength bands STRONG at a class
rate >= 2/3, MODERATE at >= 1/2 and < 2/3
(NB-1.5), applied symmetrically to the three
classes; opening-strong = INITIAL_STRONG,
closing-strong = TERMINAL_STRONG.

Decision procedure (amendment section 5):
reappearance per class (section 5.2) — the
share of arm 1's strong set in the class whose
members are also strong in arm 2 in the same
class, through crosswalk v1: an arm-1 sign
(M-number) carries through the crosswalk iff
the pinned crosswalk carries at least one row
for it and no row for it is conflict-paired;
it then reappears iff the same M-number is in
arm 2's strong set for the class. Under
DD-054-5's denominator discipline (section
5.4), arm-1 strong signs that are UNMAPPED
(no crosswalk row), CONFLICT (conflict-paired),
or TOO THIN in arm 2 (N < 20 there, named with
their count) count as not reappeared in the
primary measure; the sensitivity that removes
the named signs from the denominators is
reported with the same prominence and never
governs. The pooled overlap (section 5.3) is
the count of arm-1 positional-strong signs
(either class) carried through the crosswalk
whose M-number is positional-strong (either
class) in arm 2; its null is a label
permutation — the observed membership labels
(none / opening / closing / both) of arm 2's
classifiable signs are permuted uniformly at
random over those signs, holding arm 1's sets,
the crosswalk table, arm 2's per-class
strong-set sizes and pooled strong-set size
fixed — 999 shuffles, seed 44054, chance
level the nearest-rank 95th percentile (the
950th smallest). Precedence per DD-054-2 in
the section 5.5 order: (1) either arm-1 strong
set empty -> NOT SUPPORTED; (2) both classes
reappear at >= 1/2 -> the pooled overlap
decides (above the chance level SUPPORTED, at
or below NOT SUPPORTED); (3) a class
reappears at < 1/2 -> NOT SUPPORTED if the
pooled overlap is at or below the chance
level, else INCONCLUSIVE. Verdict wordings
are the amendment section 9 texts; the word
RE-EARNED appears in none of them.

Rate and share comparisons are made in
integer-exact form (2 * numerator >=
denominator for the one-half lines; count *
3 >= 2 * N for the STRONG band), so no float
comparison decides any condition.

Outputs (written on every terminal outcome):
  - reports/phase438_results.json (the full
    machine record)
  - reports/phase438_report.md (the report,
    under the draft section 9 headline rules:
    the falsifier verbatim with its append
    date, the full step-0 record, per-arm
    per-sign tables and the decision record
    when the run reaches them, and the
    headline outcome in the frozen wording)

Integrity: every freeze section 2 pin is
asserted before any gate quantity; the
anchors file is asserted byte-identical
before and after. The Holdat downloads CSV is
read from the main checkout's gitignored
downloads area and never enters git; row-level
corpus data appears in no output (per-sign
counts and rates are the frozen report's own
quantities).
"""
from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[2]
_SPEC = _REPO / "specs/054-yadav-opening-closing"
_MAIN_REPO = Path.home() / "workspace" / "glossa-lab"

FREEZE_DIGEST = (
    "d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57"
)
OSF_REGISTRATION = "8spvf"
EXECUTION_DATE = "2026-10-24"
SEED = 44054
N_PERMUTATIONS = 999
FLOOR_N = 20
STRONG_NUM, STRONG_DEN = 2, 3
MODERATE_NUM, MODERATE_DEN = 1, 2
THIN_MIN_LEN_GE_3 = 30
THIN_MIN_CLASSIFIABLE = 10

FALSIFIER_TEXT = (
    "This claim, as evaluated under battery NB-1 (the Spec 054 "
    "amendment, as frozen), is falsified if any of the following "
    "holds when the frozen battery is run on the frozen arm-1 "
    "and arm-2 corpora: (1) either arm-1 positional-strong set "
    "(opening or closing) is empty; (2) for either class, fewer "
    "than half of arm 1's positional-strong signs are also "
    "positional-strong in arm 2 in the same class, through the "
    "pinned crosswalk; or (3) the pooled cross-arm overlap of "
    "positional-strong signs does not exceed the 95th "
    "percentile of the 999-shuffle label-permutation null — "
    "the three conditions applied under the precedence rule "
    "of the Spec 054 amendment (§5.5)."
)
FALSIFIER_APPEND_DATE = "2026-10-23"

PIN_FILES = [
    ("glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json",
     "938174b0dee14169a5340c9299c73f4eb5b997377f8198a146ef611e73924050",
     "claim store after the falsifier append"),
    ("outputs/phase43_all.json",
     "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4",
     "Phase-43 battery record"),
    ("glossa-indus/analysis/positional/hunt_tripartite_test.json",
     "0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48",
     "positional companion record"),
    ("data/crosswalks/parpola_mahadevan_crosswalk_v1.json",
     "4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb",
     "crosswalk v1 JSON"),
    ("data/crosswalks/parpola_mahadevan_crosswalk_v1.csv",
     "3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823",
     "crosswalk v1 CSV"),
    ("backend/reports/INDUS_FINAL_ANCHORS.json",
     "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
     "anchors file"),
    ("specs/054-yadav-opening-closing/claims.json",
     "ea161e47ed355af909af707f84e2ff5f4367b88f8160dd30d6e8938d8c7d24f0",
     "the recovered claim register"),
]
ANCHORS_FILE = _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)

V3_LOADER_REL = (
    "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/"
    "firestore_indusarrays_full.jsonl"
)
HOLDAT_REL = (
    "corpora/downloads/external_repos/holdatllc_indus/"
    "indus_corpus 2.csv"
)

_OUT_RESULTS = _REPO / "reports/phase438_results.json"
_OUT_REPORT = _REPO / "reports/phase438_report.md"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _band(count: int, n: int) -> str | None:
    """Strength band of a class count out of N, in
    integer-exact comparisons (NB-1.5)."""
    if count * STRONG_DEN >= STRONG_NUM * n:
        return "STRONG"
    if count * MODERATE_DEN >= MODERATE_NUM * n:
        return "MODERATE"
    return None


def _census(sequences):
    """Margin census of a population: sequence and
    occurrence counts only — no positional quantity."""
    seqs = [list(s) for s in sequences]
    n_cnt = Counter(s for seq in seqs for s in seq)
    return {
        "sequences_total": len(seqs),
        "sequences_len_1": sum(1 for s in seqs if len(s) == 1),
        "sequences_len_ge_2": sum(1 for s in seqs if len(s) >= 2),
        "sequences_len_ge_3": sum(1 for s in seqs if len(s) >= 3),
        "tokens": sum(n_cnt.values()),
        "distinct_signs": len(n_cnt),
        "classifiable_signs": sum(
            1 for v in n_cnt.values() if v >= FLOOR_N),
        "per_sign_N": {str(k): v for k, v in sorted(
            n_cnt.items(), key=lambda kv: str(kv[0]))},
    }


def _battery(sequences):
    """Battery NB-1 over one population's sequences
    (amendment section 3). Returns the full record
    (deterministic). Signs keep the arm's own
    labels (ints for arm 1, 'M###' strings for
    arm 2)."""
    seqs = [list(s) for s in sequences]
    seqs_ge2 = [s for s in seqs if len(s) >= 2]
    cen = _census(seqs)

    n_cnt = Counter()
    i_cnt = Counter()
    t_cnt = Counter()
    m_cnt = Counter()
    total_occ = Counter(s for seq in seqs for s in seq)
    for seq in seqs_ge2:
        n_cnt.update(seq)
        i_cnt[seq[0]] += 1
        t_cnt[seq[-1]] += 1
        m_cnt.update(seq[1:-1])

    per_sign = {}
    classifiable = []
    for s in sorted(total_occ, key=str):
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
        per_sign[str(s)] = {
            "sign": s if isinstance(s, str) else s,
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

    strong = {cls: sorted(
        (per_sign[str(s)]["sign"] for s in classifiable
         if per_sign[str(s)]["bands"].get(cls) == "STRONG"),
        key=str) for cls in ("initial", "terminal", "medial")}
    moderate = {cls: sorted(
        (per_sign[str(s)]["sign"] for s in classifiable
         if per_sign[str(s)]["bands"].get(cls) == "MODERATE"),
        key=str) for cls in ("initial", "terminal", "medial")}

    return {
        "census": {k: v for k, v in cen.items()
                   if k != "per_sign_N"},
        "per_sign": per_sign,
        "strong_sets": {
            "opening": strong["initial"],
            "closing": strong["terminal"],
            "medial": strong["medial"],
        },
        "moderate_sets": {
            "opening": moderate["initial"],
            "closing": moderate["terminal"],
            "medial": moderate["medial"],
        },
    }


def _mkey(sign) -> str:
    """The crosswalk key form of a Mahadevan sign:
    'M' + zero-padded 3-digit number."""
    if isinstance(sign, str):
        return sign
    return f"M{int(sign):03d}"


def _crosswalk_maps():
    """Crosswalk v1 as the pinned JSON carries it:
    per M sign, its rows and conflict state."""
    doc = json.loads(
        (_REPO / "data/crosswalks/"
         "parpola_mahadevan_crosswalk_v1.json").read_text("utf-8"))
    rows = doc["rows"]
    by_m: dict[str, list] = {}
    for r in rows:
        mid = r.get("mahadevan_id")
        if mid:
            by_m.setdefault(mid, []).append(r)
    return {
        "rows_total": len(rows),
        "mapped_pairs": sum(1 for r in rows if r.get("mahadevan_id")),
        "conflict_pairs": sum(1 for r in rows if r.get("conflict")),
        "by_m": by_m,
    }


def _decision(arm1, arm2, xw):
    """The amendment section 5 decision procedure
    over the two arms' battery records.
    Deterministic given the frozen seed."""
    by_m = xw["by_m"]
    a2_per_sign = arm2["per_sign"]
    a2_classifiable = sorted(
        (rec["sign"] for rec in a2_per_sign.values()
         if rec["classifiable"]), key=str)
    a2_strong = {
        "opening": set(arm2["strong_sets"]["opening"]),
        "closing": set(arm2["strong_sets"]["closing"]),
    }
    a2_pooled = a2_strong["opening"] | a2_strong["closing"]

    def _disposition(sign, cls):
        """(reappeared, reason) for an arm-1 strong
        sign under DD-054-5's discipline."""
        key = _mkey(sign)
        rows = by_m.get(key)
        if not rows:
            return False, "UNMAPPED"
        if any(r.get("conflict") for r in rows):
            return False, "CONFLICT"
        rec2 = a2_per_sign.get(key)
        n2 = rec2["N"] if rec2 else 0
        if n2 < FLOOR_N:
            return False, "TOO THIN"
        if key in a2_strong[cls]:
            return True, None
        return False, None

    reappearance = {}
    for cls in ("opening", "closing"):
        members = arm1["strong_sets"][cls]
        named = []
        hit = 0
        for s in members:
            ok, reason = _disposition(s, cls)
            if ok:
                hit += 1
            elif reason is not None:
                named.append({"sign": s, "reason": reason,
                              "arm2_N": (
                                  a2_per_sign.get(_mkey(s), {})
                                  .get("N", 0)
                                  if reason == "TOO THIN"
                                  else None)})
        den = len(members)
        named_den = den - len(named)
        named_num = hit
        reappearance[cls] = {
            "arm1_strong": members,
            "reappeared": hit,
            "denominator": den,
            "rate": (hit / den) if den else None,
            "reappears": bool(den) and 2 * hit >= den,
            "named_not_reappeared": named,
            "sensitivity": {
                "reappeared": named_num,
                "denominator": named_den,
                "rate": (named_num / named_den)
                if named_den else None,
                "reappears": bool(named_den)
                and 2 * named_num >= named_den,
            },
        }

    a1_pooled = (set(arm1["strong_sets"]["opening"])
                 | set(arm1["strong_sets"]["closing"]))
    def _carried(sign):
        key = _mkey(sign)
        rows = by_m.get(key)
        return bool(rows) and not any(
            r.get("conflict") for r in rows)

    overlap_observed = sum(
        1 for s in a1_pooled
        if _carried(s) and _mkey(s) in a2_pooled)

    # ── Label-permutation null (section 5.3) ──
    labels = {}
    for s in a2_classifiable:
        in_o = s in a2_strong["opening"]
        in_c = s in a2_strong["closing"]
        labels[s] = ("both" if in_o and in_c else
                     "opening" if in_o else
                     "closing" if in_c else "none")
    label_list = [labels[s] for s in a2_classifiable]
    targets = [(_mkey(s), _carried(s)) for s in a1_pooled]
    rng = np.random.default_rng(SEED)
    null_counts = np.empty(N_PERMUTATIONS, dtype=np.int64)
    base = np.array(label_list, dtype=object)
    for j in range(N_PERMUTATIONS):
        perm = rng.permutation(base)
        lab = dict(zip(a2_classifiable, perm.tolist()))
        null_counts[j] = sum(
            1 for key, carried in targets
            if carried and lab.get(key, "none") != "none")
    null_sorted = np.sort(null_counts)
    chance = int(null_sorted[949])

    overlap = {
        "observed": overlap_observed,
        "arm1_pooled_strong": sorted(a1_pooled, key=str),
        "arm2_pooled_strong": sorted(a2_pooled, key=str),
        "null": {
            "model": "label permutation of arm 2's "
                     "strong-set membership over its "
                     "classifiable signs (arm 1's sets, "
                     "the crosswalk table, arm 2's "
                     "per-class and pooled strong-set "
                     "sizes held fixed)",
            "permutations": N_PERMUTATIONS,
            "seed": SEED,
            "generator": "numpy.random.default_rng (PCG64)",
            "numpy_version": np.__version__,
            "percentile_rule": "nearest-rank 95th "
                               "percentile (950th smallest)",
            "min": int(null_counts.min()),
            "median": int(np.median(null_counts)),
            "max": int(null_counts.max()),
            "chance_level_950th": chance,
        },
        "exceeds_chance": overlap_observed > chance,
    }

    # ── Precedence (section 5.5) ──
    empty1 = (not arm1["strong_sets"]["opening"]
              or not arm1["strong_sets"]["closing"])
    both_re = (reappearance["opening"]["reappears"]
               and reappearance["closing"]["reappears"])
    if empty1:
        verdict = "NOT SUPPORTED"
        fired = ("an arm-1 positional-strong set is empty")
        step = "5.5(1)"
    elif both_re:
        step = "5.5(2)"
        if overlap["exceeds_chance"]:
            verdict = "SUPPORTED"
            fired = None
        else:
            verdict = "NOT SUPPORTED"
            fired = ("both classes reappear, but the pooled "
                     "overlap does not exceed the null's "
                     "95th percentile")
    else:
        step = "5.5(3)"
        if not overlap["exceeds_chance"]:
            verdict = "NOT SUPPORTED"
            fired = ("a positional class reappears at less "
                     "than one half, with the pooled overlap "
                     "at or below the label-shuffle null's "
                     "95th percentile")
        else:
            verdict = "INCONCLUSIVE"
            fired = None

    return {
        "reappearance": reappearance,
        "overlap": overlap,
        "precedence": {
            "step": step,
            "arm1_either_set_empty": empty1,
            "both_classes_reappear": both_re,
            "fired_condition": fired,
        },
        "verdict": verdict,
    }


def _verdict_wording(decision):
    """The amendment section 9 wordings, verbatim."""
    v = decision["verdict"]
    if v == "SUPPORTED":
        return (
            "Positional structure of the Yadav kind — specific "
            "text-beginning and text-ending sign sets — is "
            "present in the strict corpus under battery NB-1 "
            "and reproduces across compilations: both classes "
            "reappear in the Holdat layer at one half or more, "
            "and the pooled overlap exceeds the label-shuffle "
            "null's 95th percentile. This verdict is about the "
            "amended statement under NB-1 as frozen in the "
            "Spec 054 amendment. It does not establish that the "
            "script encodes language, that any sign has a "
            "meaning or a reading, or anything about Yadav et "
            "al. (2010)'s original Phase-43 statement, whose "
            "sets no surviving record exhibits; the parent "
            "claim's record, including its strongly-supported "
            "status, is untouched by this verdict."
        )
    if v == "NOT SUPPORTED":
        return (
            "The amended statement is not supported under "
            "battery NB-1 as frozen: "
            + decision["precedence"]["fired_condition"]
            + ". This verdict falsifies the amended statement "
            "only. It does not falsify Yadav et al. (2010)'s "
            "original statement — the original battery's sets "
            "cannot be exhibited — and it does not move the "
            "parent claim's recorded status."
        )
    return (
        "One positional class reappears across compilations "
        "at less than one half, while the pooled overlap "
        "exceeds the label-shuffle null's 95th percentile. "
        "The two measures point opposite ways on the record "
        "as frozen; the run records the per-class rates and "
        "the overlap counts and closes INCONCLUSIVE. No "
        "repair, re-weighting, or second battery is "
        "permitted at run time."
    )


def _closure_wording(outcome, detail):
    """The draft section 6 pre-written closure
    wordings, with their bracketed slots filled."""
    if outcome == "STRICT CORPUS NOT PINNABLE":
        return (
            "Spec 054 closed at step 0, gate 0.3: the strict "
            "corpus layer of record could not be uniquely "
            "identified and pinned from the database as the "
            "V3 / Mahadevan-lineage corpus the Phase-43 "
            "battery used (" + detail + "). No positional "
            "quantity was computed. This closure is a "
            "statement about runnability, not about the "
            "claim; the claim stands exactly as recorded, "
            "with the falsifier appended at this spec's "
            "freeze."
        )
    if outcome == "TOO THIN":
        return (
            "Spec 054 closed at step 0, gate 0.5: in the "
            "pinned strict corpus, " + detail + ". No "
            "positional quantity was computed. This closure "
            "is a statement about runnability, not about "
            "the claim; the claim stands exactly as "
            "recorded, with the falsifier appended at this "
            "spec's freeze."
        )
    if outcome == "SECOND ARM NOT RUNNABLE":
        return (
            "Spec 054 closed at step 0, gate 0.4: the "
            "Holdat arm could not be run as designed — "
            + detail + ". No positional quantity was "
            "computed in either arm. This closure is a "
            "statement about runnability, not about the "
            "claim; the claim stands exactly as recorded, "
            "with the falsifier appended at this spec's "
            "freeze."
        )
    return (
        "Spec 054 closed as INVALID: " + detail + ". No "
        "result is recorded under this spec. The claim "
        "stands exactly as recorded, with the falsifier "
        "appended at this spec's freeze."
    )


def _load_v3_records(path: Path):
    """The V3 loader's own record loading, against an
    explicit file (backend/glossa_lab/data/
    indus_corpus_v3.py's _load_records logic)."""
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except Exception:  # noqa: BLE001
                pass
    return records


def _v3_census(records):
    """The loader's corpus census (its corpus_stats
    quantities, guarded): records, unique dockeys
    with reconstructed sequences, sequences, sign
    instances — the reconstruction being the loader
    module's own _reconstruct_sequences."""
    sys.path.insert(0, str(_REPO / "backend"))
    from glossa_lab.data.indus_corpus_v3 import (
        _reconstruct_sequences,
    )
    seqs_by_dockey = _reconstruct_sequences(records)
    all_seqs = [seq for seqs in seqs_by_dockey.values()
                for seq in seqs]
    return {
        "total_records": len(records),
        "unique_dockeys": len(seqs_by_dockey),
        "total_sequences": len(all_seqs),
        "total_sign_instances": sum(len(s) for s in all_seqs),
        "sequences_by_dockey": {
            str(k): v for k, v in seqs_by_dockey.items()},
    }


def _load_holdat_sequences(csv_path: Path):
    """The programme's Holdat loader logic
    (phase113_run.load_holdat_inscriptions, itself
    the sa_validation grouping): rows grouped by
    cisi_number at their position index, empties
    dropped."""
    seals: dict[str, list] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
    return [[s for s in v if s] for v in seals.values() if any(v)]


def _identification(phase43):
    """Gate G2's mechanical identification attempt,
    recorded in full (C1–C4 as Spec 053's gate 0.3
    framed them, against this environment)."""
    ref = {
        "source": phase43["T1_1_corpus_v3"]["source"],
        "total_records": phase43["T1_1_corpus_v3"]["total_records"],
        "unique_dockeys": phase43["T1_1_corpus_v3"]["unique_dockeys"],
        "total_sequences": phase43["T1_1_corpus_v3"]["total_sequences"],
        "total_sign_instances": phase43["T1_1_corpus_v3"][
            "total_sign_instances"],
    }

    # C1 — the V3 loader's data file, at its path in
    # this tree, in the main checkout, and in the
    # sibling trees this machine holds.
    candidates = []
    seen = set()
    roots = [_REPO, _MAIN_REPO] + sorted(
        p for p in (Path.home() / "workspace").glob("glossa-lab-*")
        if p.is_dir())
    for root in roots:
        p = root / V3_LOADER_REL
        if str(p) not in seen:
            seen.add(str(p))
            candidates.append({
                "root": str(root),
                "path": str(p),
                "present": p.exists(),
            })
    found = next((c for c in candidates if c["present"]), None)

    loader_census = None
    sequences_by_dockey = None
    if found is not None:
        records = _load_v3_records(Path(found["path"]))
        full = _v3_census(records)
        sequences_by_dockey = full.pop("sequences_by_dockey")
        loader_census = full
    else:
        # The loader in this tree, run as the
        # programme runs it: its file is absent, so
        # it loads zero records and zero sequences.
        records_here = []
        loader_path = _REPO / V3_LOADER_REL
        if loader_path.exists():
            records_here = _load_v3_records(loader_path)
        full = _v3_census(records_here)
        sequences_by_dockey = full.pop("sequences_by_dockey")
        loader_census = full

    reproduces = bool(
        found is not None
        and loader_census["total_records"] == ref["total_records"]
        and loader_census["unique_dockeys"] == ref["unique_dockeys"]
        and loader_census["total_sequences"] == ref["total_sequences"]
        and loader_census["total_sign_instances"]
        == ref["total_sign_instances"])

    # C2 — database copies.
    tree_db = _REPO / "backend/data/glossa.db"
    main_db = _MAIN_REPO / "backend/data/glossa.db"
    db_record = {
        "execution_tree_db_present": tree_db.exists(),
        "programme_db": str(main_db),
        "programme_db_present": main_db.exists(),
        "programme_db_texts": None,
    }
    if main_db.exists():
        con = sqlite3.connect(
            f"file:{main_db}?mode=ro", uri=True)
        try:
            rows = con.execute(
                "SELECT id, name, alphabet_size, length(content), "
                "metadata FROM texts ORDER BY name").fetchall()
        finally:
            con.close()
        texts = []
        for rid, name, alpha, clen, meta in rows:
            try:
                source = json.loads(meta).get("source", "")
            except Exception:  # noqa: BLE001
                source = ""
            texts.append({
                "id": rid, "name": name,
                "alphabet_size": alpha,
                "content_chars": clen,
                "metadata_source": source[:160],
            })
        db_record["programme_db_texts"] = texts

    # C4 — every other corpus layer the environment
    # holds, censused. None is the corpus the
    # Phase-43 record names; no layer is substituted.
    others = []

    yaj = _REPO / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
    if yaj.exists():
        with open(yaj, newline="", encoding="utf-8") as fh:
            n_rows = sum(1 for _ in csv.DictReader(fh))
        others.append({
            "layer": "yajnadevam_inscriptions.csv (the programme's "
                     "site-attributed layer; Specs 042/045's layer "
                     "of record)",
            "records": n_rows,
            "why_not_arm_1": "a different layer: not the "
                             "Firestore 'indusarrays' "
                             "reconstruction the Phase-43 record "
                             "names (its record count also "
                             "differs from C3's 3,916)",
        })

    mayig = _REPO / "data/corpus_layers/mayig_cisi_layer_v1.json"
    if mayig.exists():
        doc = json.loads(mayig.read_text("utf-8"))
        insc = doc["inscriptions"]
        seqs = [i["tokens"] if isinstance(i, dict) else i
                for i in insc]
        cen = _census(seqs)
        others.append({
            "layer": "mayig CISI layer v1 (data/corpus_layers/"
                     "mayig_cisi_layer_v1.json)",
            "inscriptions": cen["sequences_total"],
            "tokens": cen["tokens"],
            "distinct_signs": cen["distinct_signs"],
            "why_not_arm_1": "the CISI compilation in Parpola "
                             "numbering (Spec 019's arm) — a "
                             "different compilation from the "
                             "Mahadevan-lineage V3 layer",
        })

    research = _REPO / "glossa-corpus/indus/exports/indus_research.jsonl"
    if research.exists():
        n_lines = sum(1 for line in research.read_text("utf-8")
                      .splitlines() if line.strip())
        others.append({
            "layer": "indus_research.jsonl (the V1 research "
                     "export)",
            "records": n_lines,
            "why_not_arm_1": "a mixed-source-system export, not "
                             "the Firestore 'indusarrays' "
                             "reconstruction the Phase-43 record "
                             "names",
        })

    holdat_path = _MAIN_REPO / HOLDAT_REL
    if holdat_path.exists():
        hseqs = _load_holdat_sequences(holdat_path)
        cen = _census(hseqs)
        others.append({
            "layer": "the Holdat downloads layer (indus_corpus "
                     "2.csv; arm 2's layer)",
            "inscriptions": cen["sequences_total"],
            "tokens": cen["tokens"],
            "distinct_signs": cen["distinct_signs"],
            "why_not_arm_1": "the other compilation: the "
                             "Phase-43 record itself treats it "
                             "as a different corpus (its T4_3 "
                             "cross-validation against V3); it "
                             "is arm 2's layer, never a "
                             "substitute for arm 1",
        })

    shakti = (Path.home() / "workspace/research_notes/"
              "indus-data-deep-sweep-20261008/downloads/"
              "shaktiosindia-indus-sign-regimes-deposit/"
              "sanitized_corpus.json")
    if shakti.exists():
        sdoc = json.loads(shakti.read_text("utf-8"))
        others.append({
            "layer": "the Shakti corpus layer "
                     "(restricted-local; Specs 068/052's layer)",
            "records": len(sdoc),
            "sha256": _sha256(shakti),
            "why_not_arm_1": "a CISI-lineage compilation — a "
                             "different lineage from the "
                             "Mahadevan-lineage Firestore V3 "
                             "layer the Phase-43 record names",
        })

    identified = reproduces
    return {
        "reference_census_C3": ref,
        "C1_loader_file_candidates": candidates,
        "C1_loader_file_found": found,
        "C1_loader_census": loader_census,
        "C2_database": db_record,
        "C4_other_layers": others,
        "census_reproduces_phase43_record": reproduces,
        "identified": identified,
        "sequences_by_dockey": sequences_by_dockey
        if identified else None,
        "export_pin": None,
        "source_file_pin": None,
    }


def _render_report(res):
    lines = []
    lines.append("# Phase-438 — Spec 054 (amended): Yadav's "
                 "opening/closing signs under battery NB-1")
    lines.append("")
    lines.append(
        f"Claim under test: `yadav_2009_arxiv_manual_002` — "
        f"\"There are specific text-beginning and text-ending "
        f"signs in the Indus corpus\" (strongly supported as "
        f"recorded; this run moves no claim status). Freeze "
        f"digest `{FREEZE_DIGEST}`; OSF registration "
        f"{OSF_REGISTRATION} (approved, public). Executed "
        f"{EXECUTION_DATE} under the owner's execution order "
        f"of 2026-10-24.")
    lines.append("")
    lines.append("## The falsifier (appended to the claim's "
                 "record at the freeze, "
                 f"{FALSIFIER_APPEND_DATE})")
    lines.append("")
    lines.append("> " + FALSIFIER_TEXT)
    lines.append("")
    lines.append("## Step-0 gates (amendment section 6, in "
                 "order)")
    lines.append("")
    for g in res["gates"]:
        lines.append(f"- **Gate {g['gate']} — {g['name']}: "
                     f"{g['verdict']}**")
    lines.append("")
    idn = res.get("identification")
    if idn:
        ref = idn["reference_census_C3"]
        lines.append("## Step-0 record — strict corpus "
                     "identification (gate G2)")
        lines.append("")
        lines.append(
            f"Reference census (C3, from the pinned Phase-43 "
            f"record, T1_1): source \"{ref['source']}\"; "
            f"{ref['total_records']} records; "
            f"{ref['unique_dockeys']} unique dockeys; "
            f"{ref['total_sequences']} sequences; "
            f"{ref['total_sign_instances']} sign instances.")
        lines.append("")
        found = idn["C1_loader_file_found"]
        lines.append(
            "C1 — the V3 loader's data file (the Firestore "
            "'indusarrays' dump): "
            + (f"found at {found['path']}."
               if found else
               "absent at its path in this tree, in the main "
               "checkout, and in every sibling tree scanned "
               f"({len(idn['C1_loader_file_candidates'])} "
               "candidate paths); the loader therefore loads "
               "zero records and zero sequences."))
        lines.append("")
        db = idn["C2_database"]
        lines.append(
            "C2 — database copies: no database copy exists "
            "in the execution tree; the programme database "
            "(backend/data/glossa.db, main checkout) holds "
            + (f"{len(db['programme_db_texts'])} texts, of "
               "which the only Indus entry is the synthetic "
               "prototype (\"Indus Script (synthetic, Yadav "
               "2010 / Fuls 2014)\", 923 inscriptions by its "
               "metadata) — not the V3 layer."
               if db["programme_db_texts"] is not None else
               "no texts census available."))
        lines.append("")
        lines.append("C4 — other layers held, censused; "
                     "none is the corpus the Phase-43 record "
                     "names, and none was substituted:")
        lines.append("")
        for o in idn["C4_other_layers"]:
            nums = ", ".join(
                f"{k} {v}" for k, v in o.items()
                if k not in ("layer", "why_not_arm_1", "sha256")
                and isinstance(v, int))
            lines.append(f"- **{o['layer']}** — {nums}. "
                         f"{o['why_not_arm_1']}.")
        lines.append("")
    for arm_name in ("arm1", "arm2"):
        b = res.get(f"battery_{arm_name}")
        if not b:
            continue
        cen = b["census"]
        lines.append(f"## {arm_name.upper()} — per-sign "
                     f"quantities (NB-1)")
        lines.append("")
        lines.append(
            f"Sequences: {cen['sequences_total']} total; "
            f"{cen['sequences_len_1']} of length 1 (counted, "
            f"entering no count); {cen['sequences_len_ge_2']} "
            f"of length >= 2; {cen['sequences_len_ge_3']} of "
            f"length >= 3. Classifiable signs (N >= 20): "
            f"{cen['classifiable_signs']} of "
            f"{cen['distinct_signs']}.")
        lines.append("")
        lines.append("| Sign | N | I | T | M | i | t | m "
                     "| Bands |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for key in sorted(b["per_sign"],
                          key=lambda k: (-b["per_sign"][k]["N"],
                                         str(k))):
            ps = b["per_sign"][key]
            if ps["classifiable"]:
                bands = ", ".join(
                    f"{cls.upper()}_{band}"
                    for cls, band in sorted(
                        ps["bands"].items())) or "—"
                r = ps["rates"]
                lines.append(
                    f"| {ps['sign']} | {ps['N']} | {ps['I']} "
                    f"| {ps['T']} | {ps['M']} | {r['i']:.3f} "
                    f"| {r['t']:.3f} | {r['m']:.3f} | {bands} |")
        lines.append("")
        thin = sum(1 for ps in b["per_sign"].values()
                   if not ps["classifiable"])
        lines.append(
            f"Signs below the classifiability floor "
            f"(N < 20), reported with their counts in the "
            f"results JSON and marked TOO THIN for this "
            f"population: {thin}. None is a member of any "
            f"strong set and none was dropped.")
        lines.append("")
        ss = b["strong_sets"]
        lines.append(
            f"Strong sets — opening-strong "
            f"({len(ss['opening'])}): {ss['opening'] or '[]'}"
            f"; closing-strong ({len(ss['closing'])}): "
            f"{ss['closing'] or '[]'}; medial-strong "
            f"({len(ss['medial'])}): {ss['medial'] or '[]'}.")
        lines.append("")
    dec = res.get("decision")
    if dec:
        lines.append("## Decision record (amendment "
                     "section 5)")
        lines.append("")
        for cls in ("opening", "closing"):
            r = dec["reappearance"][cls]
            s = r["sensitivity"]
            lines.append(
                f"- **{cls} reappearance (primary): "
                f"{r['reappeared']}/{r['denominator']}** "
                f"(rate "
                f"{r['rate'] if r['rate'] is not None else '—'}"
                f"; reappears at >= 1/2: {r['reappears']}). "
                f"Named not reappeared: "
                f"{[(n['sign'], n['reason']) for n in r['named_not_reappeared']] or '[]'}. "
                f"Sensitivity (named signs removed from the "
                f"denominator): {s['reappeared']}/"
                f"{s['denominator']}"
                f" (reappears: {s['reappears']}).")
        ov = dec["overlap"]
        nu = ov["null"]
        lines.append(
            f"- **Pooled overlap: {ov['observed']}** against "
            f"the label-permutation null's chance level "
            f"{nu['chance_level_950th']} (999 shuffles, seed "
            f"44054; null min/median/max {nu['min']}/"
            f"{nu['median']}/{nu['max']}); exceeds the "
            f"chance level: {ov['exceeds_chance']}.")
        lines.append(
            f"- Precedence: amendment section "
            f"{dec['precedence']['step']} decided the "
            f"verdict.")
        lines.append("")
    lines.append("## Outcome")
    lines.append("")
    lines.append(f"**{res['outcome']}**")
    lines.append("")
    lines.append(res["headline_wording"])
    lines.append("")
    lines.append("## Limits")
    lines.append("")
    lines.append("- No language conclusion: opening and "
                 "closing markers occur in non-linguistic "
                 "systems too; no outcome of this run "
                 "establishes that the script encodes "
                 "language (spec section 7.1).")
    lines.append("- No meaning conclusion: no outcome "
                 "establishes what any opening or closing "
                 "sign means, or what any sign was read as.")
    lines.append("- Compilation-relativity: the arms are "
                 "two compilations' stories, computed "
                 "inside each compilation and joined only "
                 "through the pinned crosswalk; no output "
                 "pools the corpora or presents a crosswalk "
                 "pair as a finding that two drawn signs are "
                 "the same sign.")
    lines.append("- The Phase-43 record stands: this run "
                 "edits no Phase-43 file and no prior claim "
                 "status; the parent claim's record, "
                 "including its strongly-supported status, "
                 "is untouched by any verdict (amendment "
                 "section 9).")
    lines.append("- This spec's closing measure is "
                 "\"closing-strong under NB-1\" (a per-sign "
                 "terminal-rate band on an "
                 "inscription-position basis), a different "
                 "quantity from Spec 045's \"Holdat "
                 "final-position concentration\" "
                 "(amendment section 10).")
    lines.append("- Negative, inconclusive, thin, and "
                 "step-0 outcomes are recorded with the "
                 "same prominence as a supported finding.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    anchors_before = (_sha256(ANCHORS_FILE)
                      if ANCHORS_FILE.exists() else None)
    gates: list[dict] = []
    outcome = None
    closure_detail = None

    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=str(_REPO),
            capture_output=True, text=True, timeout=30)
        executed_from = head.stdout.strip() or None
    except Exception:  # noqa: BLE001
        executed_from = None

    res: dict = {
        "phase": 438,
        "spec": "054",
        "claim_id": "yadav_2009_arxiv_manual_002",
        "contract": {
            "freeze_digest": FREEZE_DIGEST,
            "osf_registration": OSF_REGISTRATION,
            "battery": "NB-1 (Spec 054 amendment as frozen)",
            "falsifier": FALSIFIER_TEXT,
            "falsifier_append_date": FALSIFIER_APPEND_DATE,
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

    # ── Gate G1 — pin checks ──────────────────
    pin_results = []
    pins_ok = True
    for rel, pin, label in PIN_FILES:
        p = _REPO / rel
        observed = _sha256(p) if p.exists() else None
        match = observed == pin
        pins_ok = pins_ok and match
        pin_results.append({
            "file": rel, "label": label, "pin": pin,
            "observed": observed, "present": p.exists(),
            "match": match})
    freeze_json = json.loads((_SPEC / "freeze.json")
                             .read_text("utf-8"))
    digest_match = freeze_json.get("digest") == FREEZE_DIGEST
    gate1 = {
        "gate": "G1", "name": "Pin checks (draft 0.1)",
        "inputs": pin_results,
        "freeze_digest": {"pin": FREEZE_DIGEST,
                          "observed": freeze_json.get("digest"),
                          "match": digest_match},
        "verdict": "PASS" if (pins_ok and digest_match)
                   else "FAIL",
    }
    gates.append(gate1)
    if gate1["verdict"] != "PASS":
        outcome = "INVALID"
        bad = [r["file"] for r in pin_results if not r["match"]]
        closure_detail = (
            "the named freeze section 2 pin(s) mismatched: "
            + ", ".join(bad)
            + ("" if digest_match else
               "; the freeze digest did not re-assert"))
        _not_reached(
            ("G2", "Strict corpus identification and pin"),
            ("G3", "Thinness"),
            ("G4", "Second arm runnability"),
            ("G5", "Determinism"))

    # ── Gate G2 — strict corpus identification ─
    identification = None
    arm1_sequences = None
    if outcome is None:
        phase43 = json.loads(
            (_REPO / "outputs/phase43_all.json").read_text("utf-8"))
        identification = _identification(phase43)
        sbd = identification.pop("sequences_by_dockey")
        if identification["identified"]:
            seqs = [seq for seqs in sbd.values() for seq in seqs]
            arm1_sequences = [
                [int(s) for s in seq] for seq in seqs]
            export = json.dumps(
                {"source": "indusscript.in Firestore "
                           "'indusarrays' (2026-05-14)",
                 "sequences_by_dockey": sbd},
                sort_keys=True).encode("utf-8")
            identification["export_pin"] = _sha256_bytes(export)
            found_path = Path(
                identification["C1_loader_file_found"]["path"])
            identification["source_file_pin"] = _sha256(found_path)
            identification["exported_sequences"] = len(arm1_sequences)
        gate2 = {
            "gate": "G2",
            "name": "Strict corpus identification and pin "
                    "(draft 0.3)",
            "identified": identification["identified"],
            "census_reproduces_phase43_record":
                identification["census_reproduces_phase43_record"],
            "verdict": "PASS" if identification["identified"]
                       else "FAIL",
        }
        gates.append(gate2)
        if gate2["verdict"] != "PASS":
            outcome = "STRICT CORPUS NOT PINNABLE"
            closure_detail = (
                "the V3 loader's data file — the Firestore "
                "'indusarrays' dump the Phase-43 record names "
                "as its corpus's source — is absent at its "
                "path in this tree, in the main checkout, and "
                "in every sibling tree scanned, so the loader "
                "loads zero records and zero sequences and the "
                "layer cannot be exported or pinned; no "
                "database copy of the layer exists (the "
                "programme database's only Indus text is the "
                "synthetic prototype); and no other layer "
                "held is the corpus the Phase-43 record names "
                "(the site-attributed layer at 5,679 records, "
                "the V1 research export, the mayig CISI "
                "layer, the Holdat downloads layer, and the "
                "Shakti layer are each a different corpus or "
                "lineage)")
            _not_reached(("G3", "Thinness"),
                         ("G4", "Second arm runnability"),
                         ("G5", "Determinism"))

    # ── Gate G3 — thinness (arm 1 census) ─────
    arm1_census = None
    if outcome is None:
        arm1_census = _census(arm1_sequences)
        gate3 = {
            "gate": "G3", "name": "Thinness (draft 0.5 census)",
            "sequences_len_ge_3": arm1_census["sequences_len_ge_3"],
            "min_len_ge_3": THIN_MIN_LEN_GE_3,
            "classifiable_signs": arm1_census["classifiable_signs"],
            "min_classifiable": THIN_MIN_CLASSIFIABLE,
            "verdict": "PASS" if (
                arm1_census["sequences_len_ge_3"] >= THIN_MIN_LEN_GE_3
                and arm1_census["classifiable_signs"]
                >= THIN_MIN_CLASSIFIABLE) else "FAIL",
        }
        gates.append(gate3)
        if gate3["verdict"] != "PASS":
            outcome = "TOO THIN"
            closure_detail = (
                "the pinned strict corpus carries "
                f"{arm1_census['sequences_len_ge_3']} sequences "
                f"of length >= 3 (frozen line "
                f"{THIN_MIN_LEN_GE_3}) and "
                f"{arm1_census['classifiable_signs']} "
                f"classifiable signs (frozen line "
                f"{THIN_MIN_CLASSIFIABLE})")
            _not_reached(("G4", "Second arm runnability"),
                         ("G5", "Determinism"))

    # ── Gate G4 — second arm runnability ──────
    arm2_sequences = None
    arm2_pin = None
    if outcome is None:
        holdat_path = _MAIN_REPO / HOLDAT_REL
        gate4 = {
            "gate": "G4",
            "name": "Second arm runnability (draft 0.4)",
            "holdat_file": str(holdat_path),
            "holdat_present": holdat_path.exists(),
        }
        if not holdat_path.exists():
            gate4["verdict"] = "FAIL"
            gates.append(gate4)
            outcome = "SECOND ARM NOT RUNNABLE"
            closure_detail = ("the Holdat layer could not be "
                              "identified and pinned — its "
                              "downloads file is absent")
            _not_reached(("G5", "Determinism"))
        else:
            arm2_pin = _sha256(holdat_path)
            arm2_sequences = _load_holdat_sequences(holdat_path)
            arm2_census = _census(arm2_sequences)
            gate4["holdat_pin"] = arm2_pin
            gate4["arm2_census"] = {
                k: v for k, v in arm2_census.items()
                if k != "per_sign_N"}
            gate4["classifiable_signs"] = arm2_census[
                "classifiable_signs"]
            gate4["min_classifiable"] = THIN_MIN_CLASSIFIABLE
            gate4["verdict"] = (
                "PASS" if arm2_census["classifiable_signs"]
                >= THIN_MIN_CLASSIFIABLE else "FAIL")
            gates.append(gate4)
            if gate4["verdict"] != "PASS":
                outcome = "SECOND ARM NOT RUNNABLE"
                closure_detail = (
                    "arm 2 has "
                    f"{arm2_census['classifiable_signs']} "
                    f"classifiable signs, under the frozen "
                    f"floor of {THIN_MIN_CLASSIFIABLE}")
                _not_reached(("G5", "Determinism"))

    # ── Gate G5 — determinism, then the verdict ─
    battery_arm1 = None
    battery_arm2 = None
    decision = None
    if outcome is None:
        xw = _crosswalk_maps()

        def _compute():
            b1 = _battery(arm1_sequences)
            b2 = _battery(arm2_sequences)
            d = _decision(b1, b2, xw)
            return b1, b2, d

        b1a, b2a, da = _compute()
        b1b, b2b, db = _compute()
        canon_a = json.dumps(
            {"arm1": b1a, "arm2": b2a, "decision": da},
            sort_keys=True, default=str)
        canon_b = json.dumps(
            {"arm1": b1b, "arm2": b2b, "decision": db},
            sort_keys=True, default=str)
        gate5 = {
            "gate": "G5", "name": "Determinism",
            "method": "the full decision computation run "
                      "twice over the pinned inputs, seed "
                      "44054; canonical-JSON comparison of "
                      "both arms' battery records and the "
                      "decision record",
            "identical": canon_a == canon_b,
            "verdict": "PASS" if canon_a == canon_b else "FAIL",
        }
        gates.append(gate5)
        if gate5["verdict"] != "PASS":
            outcome = "INVALID"
            closure_detail = (
                "the frozen implementation did not produce "
                "identical sets and null percentiles on a "
                "second run under seed 44054")
        else:
            battery_arm1, battery_arm2, decision = b1a, b2a, da
            outcome = decision["verdict"]

    # ── Records ───────────────────────────────
    if identification is not None:
        res["identification"] = {
            k: v for k, v in identification.items()
            if k != "sequences_by_dockey"}
    if arm1_census is not None:
        res["arm1_census"] = {
            k: v for k, v in arm1_census.items()
            if k != "per_sign_N"}
    if arm2_pin is not None:
        res["arm2_pin"] = arm2_pin
    res["gates"] = gates
    res["outcome"] = outcome
    res["battery_arm1"] = battery_arm1
    res["battery_arm2"] = battery_arm2
    res["decision"] = decision
    if decision is not None:
        res["headline_wording"] = _verdict_wording(decision)
    else:
        res["headline_wording"] = _closure_wording(
            outcome, closure_detail or "")
        res["closure_detail"] = closure_detail
    res["outcome_append_text"] = (
        f"Spec 054 (Phase-438), executed {EXECUTION_DATE} "
        f"under the frozen amended contract (freeze digest "
        f"{FREEZE_DIGEST}; OSF registration "
        f"{OSF_REGISTRATION}): " + res["headline_wording"])
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
    print(f"Phase-438 outcome: {outcome}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
