#!/usr/bin/env python3
"""Spec 093 Stage 2 — T202 find-context successor
independent audit (freeze v2).

Recomputes the successor administration and control
battery from the pinned inputs under the freeze
(`specs/093-material-context-channel/records/t202-findcontext-freeze-v2.md`)
and compares the recomputed result blocks against the
run records filed in the store. This tool does not
import or execute
`tools/spec093/run_stage2_findcontext_v2.py`; the
freeze's constants are restated here on the auditor's
own face, and the implementation is a second one
(index-based classes, list confusion matrices,
precomputed per-class log-probability tables).

Usage:

    python3 tools/spec093/audit_stage2_findcontext_v2.py \
        --store <run-store-dir>

Prints one JSON document: per execution, the filed run
id, whether the filed result block equals the auditor's
recomputation (as parsed values), whether the header
pins verify against the files in the tree, and the
overall verdict (AGREE only if every filed successor
run recomputes exactly and its header pins verify).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from glossa_lab import run_records as rr  # noqa: E402

SPEC_DIR = "specs/093-material-context-channel"
SNAPSHOT_REL = "glossa-corpus/indus/exports/indus_research.jsonl"
SNAPSHOT_SHA256 = (
    "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e"
)
JOIN_REL = f"{SPEC_DIR}/records/t103-join-pairs-v1.jsonl"
JOIN_SHA256 = (
    "7107f738832a4e3b04cff91d81073212bc0f3a77afed6f0ccc3cee4fce621703"
)
FREEZE_REL = f"{SPEC_DIR}/records/t202-findcontext-freeze-v2.md"
SEED_BASE = 20261121
SEED_CONTROLS = 20261122
SMOOTHING = 1.0
FLOOR = 10
FOLDS = 5
REPEATS = 10
PERMUTATIONS = 200
P99_SLOT = 197
EMPTY = {"", "None", "-", "--"}
BK_FIELDS = ("source_system", "sign_id_scheme",
             "rights_status", "crosswalk_coverage")
WANT = {("administration", "find-context"),
        ("permutation-controls", "find-context")}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def blank(v) -> bool:
    if v is None or isinstance(v, (list, dict)) and not v:
        return True
    return isinstance(v, str) and v.strip() in EMPTY


def load_rows() -> list[dict]:
    snap = [json.loads(l) for l in
            (ROOT / SNAPSHOT_REL).open(encoding="utf-8") if l.strip()]
    by_id = {r["glossa_id"]: r for r in snap}
    out = []
    for line in (ROOT / JOIN_REL).open(encoding="utf-8"):
        if not line.strip():
            continue
        p = json.loads(line)
        if blank(p.get("area_section")):
            continue
        r = by_id[p["text_id"]]
        out.append({
            "rid": r["glossa_id"],
            "seq": [str(x) for x in r["canonical_grapheme_ids"]],
            "bk": tuple(str(r.get(k)) for k in BK_FIELDS),
            "y": str(p["area_section"]),
        })
    return out


def adjudged(rows_: list[dict]):
    tally: dict[str, int] = {}
    for r in rows_:
        tally[r["y"]] = tally.get(r["y"], 0) + 1
    kept = {c: n for c, n in sorted(tally.items()) if n >= FLOOR}
    dropped = {c: n for c, n in sorted(tally.items()) if n < FLOOR}
    return [r for r in rows_ if r["y"] in kept], kept, dropped


def feats(r: dict) -> list:
    seq = r["seq"]
    ev = [("tok", c) for c in seq]
    ev.append(("first", seq[0]))
    ev.append(("last", seq[-1]))
    ev.append(("len", str(len(seq))))
    ev.append(("distinct", str(len(set(seq)))))
    for k, v in zip(BK_FIELDS, r["bk"]):
        ev.append(("bk:" + k, v))
    return ev


def fold_assignment(rows_: list[dict], repeat: int) -> list[set]:
    """Freeze section 5 restated: fresh stream per
    repeat, classes ascending, ids ascending, shuffled
    with the continuing stream, fold f takes positions
    f, f+5, ... of each class's shuffled ids."""
    rng = random.Random(SEED_BASE + repeat)
    buckets: dict[str, list[str]] = {}
    for r in rows_:
        buckets.setdefault(r["y"], []).append(r["rid"])
    held = [set() for _ in range(FOLDS)]
    for label in sorted(buckets):
        ids = sorted(buckets[label])
        rng.shuffle(ids)
        for pos, rid in enumerate(ids):
            held[pos % FOLDS].add(rid)
    return held


def score_matrix(matrix: list[list[int]], labels: list[str]):
    """Exact metrics from a square count matrix whose
    rows are actual classes and columns predicted."""
    k = len(labels)
    n = sum(sum(row) for row in matrix)
    hits = sum(matrix[i][i] for i in range(k))
    acc = Fraction(hits, n)
    recalls = []
    for i in range(k):
        row_total = sum(matrix[i])
        recalls.append(Fraction(matrix[i][i], row_total)
                       if row_total else Fraction(0))
    bal = sum(recalls) / k
    pe = Fraction(0)
    for j in range(k):
        col_total = sum(matrix[i][j] for i in range(k))
        pe += Fraction(sum(matrix[j]) * col_total, n * n)
    if pe >= 1:
        kap = Fraction(1) if acc >= 1 else Fraction(0)
    else:
        kap = (acc - pe) / (1 - pe)
    return acc, bal, kap, recalls


def run_cv(rows_: list[dict]):
    labels = sorted({r["y"] for r in rows_})
    idx = {c: i for i, c in enumerate(labels)}
    by_rid = {r["rid"]: r for r in rows_}
    repeats_out = []
    kap_sum = Fraction(0)
    bal_sum = Fraction(0)
    maj_kap_sum = Fraction(0)
    maj_bal_sum = Fraction(0)
    pooled = [[0] * len(labels) for _ in labels]
    for rep in range(REPEATS):
        held_sets = fold_assignment(rows_, rep)
        matrix = [[0] * len(labels) for _ in labels]
        maj_matrix = [[0] * len(labels) for _ in labels]
        vocab_sizes = []
        for f in range(FOLDS):
            train = [r for r in rows_ if r["rid"] not in held_sets[f]]
            test = [by_rid[i] for i in sorted(held_sets[f])]
            # Fit: per-class event tallies and a
            # precomputed log-probability table.
            counts: dict[str, dict] = {c: {} for c in labels}
            totals = {c: 0 for c in labels}
            members = {c: 0 for c in labels}
            vocab = set()
            for r in train:
                members[r["y"]] += 1
                for e in feats(r):
                    vocab.add(e)
                    d = counts[r["y"]]
                    d[e] = d.get(e, 0) + 1
                    totals[r["y"]] += 1
            vocab_sizes.append(len(vocab))
            logp: dict[str, dict] = {}
            for c in labels:
                denom = totals[c] + SMOOTHING * len(vocab)
                logp[c] = {e: math.log((counts[c].get(e, 0) + SMOOTHING)
                                       / denom) for e in vocab}
            majority = max(labels, key=lambda c: (members[c], c))
            for r in test:
                ev = [e for e in feats(r) if e in vocab]
                best, best_val = None, None
                for c in labels:
                    val = math.log(members[c] / len(train))
                    for e in ev:
                        val += logp[c][e]
                    if best_val is None or val > best_val:
                        best, best_val = c, val
                matrix[idx[r["y"]]][idx[best]] += 1
                maj_matrix[idx[r["y"]]][idx[majority]] += 1
        acc, bal, kap, recalls = score_matrix(matrix, labels)
        _ma, mbal, mkap, _mr = score_matrix(maj_matrix, labels)
        kap_sum += kap
        bal_sum += bal
        maj_kap_sum += mkap
        maj_bal_sum += mbal
        for i in range(len(labels)):
            for j in range(len(labels)):
                pooled[i][j] += matrix[i][j]
        conf = {a: {p: matrix[idx[a]][idx[p]] for p in labels}
                for a in labels}
        repeats_out.append({
            "repeat": rep,
            "kappa": float(kap),
            "balanced_accuracy": float(bal),
            "accuracy": float(acc),
            "per_class_recall": {c: float(recalls[idx[c]])
                                 for c in labels},
            "confusion": conf,
            "vocabulary_sizes_by_fold": vocab_sizes,
        })
    pooled_conf = {a: {p: pooled[idx[a]][idx[p]] for p in labels}
                   for a in labels}
    body = {
        "n_repeats": REPEATS,
        "n_folds": FOLDS,
        "per_repeat": repeats_out,
        "kappa_mean": float(kap_sum / REPEATS),
        "balanced_accuracy_mean": float(bal_sum / REPEATS),
        "pooled_confusion": pooled_conf,
        "majority_rule": {
            "kappa_mean": float(maj_kap_sum / REPEATS),
            "balanced_accuracy_mean": float(maj_bal_sum / REPEATS),
        },
    }
    return body, kap_sum / REPEATS


def recompute(kind: str) -> dict:
    rows_ = load_rows()
    adj, kept, dropped = adjudged(rows_)
    if kind == "administration":
        body, _ = run_cv(adj)
        return {"spec": "093", "stage": "2", "task": "T202-successor",
                "freeze": "v2", "kind": "administration",
                "field": "find-context", "population": len(rows_),
                "adjudged_classes": kept, "excluded_classes": dropped,
                "adjudged_total": len(adj), **body}
    ids = sorted(r["rid"] for r in adj)
    lookup = {r["rid"]: r for r in adj}
    base = [lookup[i]["y"] for i in ids]
    rng = random.Random(SEED_CONTROLS)
    vals: list[float] = []
    exact: list[Fraction] = []
    for _ in range(PERMUTATIONS):
        labs = list(base)
        rng.shuffle(labs)
        relabeled = []
        for rid, lab in zip(ids, labs):
            clone = dict(lookup[rid])
            clone["y"] = lab
            relabeled.append(clone)
        _body, mean_kap = run_cv(relabeled)
        vals.append(float(mean_kap))
        exact.append(mean_kap)
    ordered = sorted(vals)
    return {"spec": "093", "stage": "2", "task": "T202-successor",
            "freeze": "v2", "kind": "permutation-controls",
            "field": "find-context", "adjudged_classes": kept,
            "adjudged_total": len(adj), "n_permutations": PERMUTATIONS,
            "kappa_mean_values": vals,
            "kappa_mean_max": ordered[-1],
            "kappa_mean_mean": float(sum(exact) / len(exact)),
            "kappa_mean_p99_index197": ordered[P99_SLOT],
            "validity_ceiling": 0.10,
            "controls_valid": ordered[P99_SLOT] < 0.10}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True, type=Path)
    args = parser.parse_args(argv)

    freeze_sha = digest(ROOT / FREEZE_REL)
    pins_ok = (
        digest(ROOT / SNAPSHOT_REL) == SNAPSHOT_SHA256
        and digest(ROOT / JOIN_REL) == JOIN_SHA256
    )
    filed: dict[tuple[str, str], dict] = {}
    unexpected = []
    for path in sorted(args.store.glob("study-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        result = record.get("result")
        if not isinstance(result, dict):
            continue
        if result.get("task") != "T202-successor":
            continue
        key = (result.get("kind"), result.get("field"))
        if key in WANT and key not in filed:
            filed[key] = {"record": record, "path": path}
        else:
            unexpected.append(record["run"]["run_id"])

    audited = []
    all_match = pins_ok and not unexpected
    for kind, field in sorted(WANT):
        entry = {"kind": kind, "field": field}
        got = filed.get((kind, field))
        if got is None:
            entry.update({"filed": False, "match": False})
            all_match = False
        else:
            record, path = got["record"], got["path"]
            key_pins = record["run"]["key"]["input_pins"]
            header_ok = (
                key_pins.get("freeze_record") == FREEZE_REL
                and key_pins.get("freeze_record_sha256") == freeze_sha
                and key_pins.get("snapshot", {}).get("sha256")
                == SNAPSHOT_SHA256
                and key_pins.get("join_pairs", {}).get("sha256")
                == JOIN_SHA256
            )
            recomputed = recompute(kind)
            result_match = (record.get("result") == recomputed)
            entry.update({
                "filed": True,
                "run_id": record["run"]["run_id"],
                "record_file": path.name,
                "header_pins_ok": header_ok,
                "result_matches_recomputation": result_match,
                "match": bool(header_ok and result_match),
            })
            all_match = all_match and header_ok and result_match
        audited.append(entry)

    print(json.dumps({
        "audit": "independent recomputation "
                 "(audit_stage2_findcontext_v2.py)",
        "audited": audited,
        "data_pins_verified_in_tree": pins_ok,
        "spec": "093",
        "stage": "2",
        "task": "T202-successor",
        "unexpected_successor_runs": unexpected,
        "verdict": "AGREE" if all_match else "DIVERGE",
    }, indent=1, sort_keys=True))
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
