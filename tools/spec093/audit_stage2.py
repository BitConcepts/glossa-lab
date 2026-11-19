#!/usr/bin/env python3
"""Spec 093 Stage 2 — T202 independent audit.

Recomputes the Stage 2 administrations and control
batteries from the pinned inputs under the freeze
(`specs/093-material-context-channel/records/t202-freeze-v1.md`)
and compares the recomputed result blocks against the
run records filed in the store. This tool does not
import or execute `tools/spec093/run_stage2.py`; the
freeze's constants are restated here on the auditor's
own face, and the implementation is a second one.

Usage:

    python3 tools/spec093/audit_stage2.py \
        --store <run-store-dir>

Prints one JSON document: per execution, the filed run
id, whether the filed result block equals the auditor's
recomputation byte-for-byte (as parsed values), and the
overall verdict (AGREE only if every filed Stage 2 run
recomputes exactly and its header pins verify against
the files in the tree).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from collections import Counter, defaultdict
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
SPLIT_SEED = 20261119
CONTROL_SEED = 20261120
ALPHA = 1.0
CLASS_FLOOR = 10
N_PERMUTATIONS = 200
P99_INDEX = 197
EMPTY = {"", "None", "-", "--"}
BK = ("source_system", "sign_id_scheme", "rights_status",
      "crosswalk_coverage")
EXPECTED = {
    ("administration", "site"),
    ("administration", "find-context"),
    ("permutation-controls", "site"),
    ("permutation-controls", "find-context"),
}


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


def rows(field: str) -> list[dict]:
    snap = [json.loads(l) for l in
            (ROOT / SNAPSHOT_REL).open(encoding="utf-8") if l.strip()]
    out = []
    if field == "site":
        for r in snap:
            if r.get("canonical_grapheme_ids") and not blank(r.get("site_name")):
                out.append({"id": r["glossa_id"],
                            "seq": [str(x) for x in r["canonical_grapheme_ids"]],
                            "bk": {k: str(r.get(k)) for k in BK},
                            "y": str(r["site_name"])})
    else:
        by_id = {r["glossa_id"]: r for r in snap}
        for line in (ROOT / JOIN_REL).open(encoding="utf-8"):
            if not line.strip():
                continue
            p = json.loads(line)
            if blank(p.get("area_section")):
                continue
            r = by_id[p["text_id"]]
            out.append({"id": r["glossa_id"],
                        "seq": [str(x) for x in r["canonical_grapheme_ids"]],
                        "bk": {k: str(r.get(k)) for k in BK},
                        "y": str(p["area_section"])})
    return out


def adjudged(rows_: list[dict]):
    counts = Counter(r["y"] for r in rows_)
    kept = {c: n for c, n in sorted(counts.items()) if n >= CLASS_FLOOR}
    excluded = {c: n for c, n in sorted(counts.items()) if n < CLASS_FLOOR}
    return [r for r in rows_ if r["y"] in kept], kept, excluded


def features(r: dict) -> list:
    seq = r["seq"]
    ev = [("t", c) for c in seq]
    ev += [("f", seq[0]), ("l", seq[-1]), ("n", str(len(seq))),
           ("d", str(len(set(seq))))]
    ev += [("b:" + k, r["bk"][k]) for k in BK]
    return ev


def partition(rows_: list[dict]):
    rng = random.Random(SPLIT_SEED)
    groups = defaultdict(list)
    for r in rows_:
        groups[r["y"]].append(r)
    train, test = [], []
    for label in sorted(groups):
        g = sorted(groups[label], key=lambda r: r["id"])
        ids = [r["id"] for r in g]
        rng.shuffle(ids)
        cut = max(1, (3 * len(ids)) // 10)
        held = set(ids[:cut])
        for r in g:
            (test if r["id"] in held else train).append(r)
    return train, test


def run_administration(rows_: list[dict]) -> dict:
    train, test = partition(rows_)
    labels = sorted({r["y"] for r in train})
    per_label = {c: Counter() for c in labels}
    totals = Counter()
    vocab = set()
    members = Counter()
    for r in train:
        ev = features(r)
        per_label[r["y"]].update(ev)
        totals[r["y"]] += len(ev)
        vocab.update(ev)
        members[r["y"]] += 1

    def classify(r: dict) -> str:
        ev = [e for e in features(r) if e in vocab]
        best, best_val = None, None
        for c in labels:
            denom = totals[c] + ALPHA * len(vocab)
            val = math.log(members[c] / len(train))
            for e in ev:
                val += math.log((per_label[c].get(e, 0) + ALPHA) / denom)
            if best_val is None or val > best_val:
                best, best_val = c, val
        return best

    def score(preds: list[str]):
        """Metrics in exact rational arithmetic, emitted
        as floats, so this recomputation and any other
        correct implementation agree bit-for-bit."""
        conf = {a: {p: 0 for p in labels} for a in labels}
        hits = 0
        for r, p in zip(test, preds):
            conf[r["y"]][p] += 1
            hits += (p == r["y"])
        n = len(test)
        acc = Fraction(hits, n)
        rec = {}
        for c in labels:
            row_total = sum(conf[c].values())
            rec[c] = Fraction(conf[c][c], row_total) if row_total else Fraction(0)
        bal = sum(rec[c] for c in labels) / len(labels)
        pe = sum(Fraction(sum(conf[c].values())
                          * sum(conf[a][c] for a in labels), n * n)
                 for c in labels)
        kap = (Fraction(1) if acc >= 1 else Fraction(0)) if pe >= 1 \
            else (acc - pe) / (1 - pe)
        return {"n_held_out": n, "accuracy": float(acc),
                "balanced_accuracy": float(bal),
                "kappa": float(kap),
                "per_class_recall": {c: float(rec[c]) for c in labels},
                "confusion": conf}, kap

    m, kap_exact = score([classify(r) for r in test])
    majority = max(labels, key=lambda c: (members[c], c))
    maj, _ = score([majority] * len(test))
    return {"train_size": len(train), "held_out_size": len(test),
            "vocabulary_size": len(vocab), "metrics": m,
            "majority_rule": {"class": majority,
                              "accuracy": maj["accuracy"],
                              "balanced_accuracy": maj["balanced_accuracy"],
                              "kappa": maj["kappa"]}}, kap_exact


def recompute(kind: str, field: str) -> dict:
    items = rows(field)
    adj, kept, excluded = adjudged(items)
    if kind == "administration":
        body, _kap = run_administration(adj)
        return {"spec": "093", "stage": "2", "task": "T202",
                "kind": "administration", "field": field,
                "population": len(items), "adjudged_classes": kept,
                "excluded_classes": excluded,
                "adjudged_total": len(adj), **body}
    ids = sorted(r["id"] for r in adj)
    by_id = {r["id"]: r for r in adj}
    base_labels = [by_id[i]["y"] for i in ids]
    rng = random.Random(CONTROL_SEED)
    kappas = []
    kappas_exact = []
    for _ in range(N_PERMUTATIONS):
        labs = list(base_labels)
        rng.shuffle(labs)
        relabeled = []
        for rid, lab in zip(ids, labs):
            clone = dict(by_id[rid])
            clone["y"] = lab
            relabeled.append(clone)
        body, kap = run_administration(relabeled)
        kappas.append(body["metrics"]["kappa"])
        kappas_exact.append(kap)
    ordered = sorted(kappas)
    return {"spec": "093", "stage": "2", "task": "T202",
            "kind": "permutation-controls", "field": field,
            "adjudged_classes": kept, "adjudged_total": len(adj),
            "n_permutations": N_PERMUTATIONS, "kappa_values": kappas,
            "kappa_max": ordered[-1],
            "kappa_mean": float(sum(kappas_exact) / len(kappas_exact)),
            "kappa_p99_index197": ordered[P99_INDEX],
            "validity_ceiling": 0.10,
            "controls_valid": ordered[P99_INDEX] < 0.10}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True, type=Path)
    args = parser.parse_args(argv)

    pins_ok = (
        digest(ROOT / SNAPSHOT_REL) == SNAPSHOT_SHA256
        and digest(ROOT / JOIN_REL) == JOIN_SHA256
    )
    filed: dict[tuple[str, str], dict] = {}
    for path in sorted(args.store.glob("study-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        result = record.get("result")
        if not isinstance(result, dict):
            continue
        if result.get("spec") != "093" or result.get("stage") != "2":
            continue
        filed[(result["kind"], result["field"])] = {
            "path": path, "record": record, "result": result,
        }

    audited = []
    all_match = pins_ok
    for kind, field in sorted(EXPECTED):
        entry = filed.get((kind, field))
        if entry is None:
            audited.append({"kind": kind, "field": field,
                            "filed": False, "match": False})
            all_match = False
            continue
        header_pins = entry["record"]["run"].get("key", {}).get("input_pins", {})
        header_pins_ok = (
            header_pins.get("snapshot", {}).get("sha256") == SNAPSHOT_SHA256
            and header_pins.get("join_pairs", {}).get("sha256") == JOIN_SHA256
        )
        mine = recompute(kind, field)
        match = (mine == entry["result"]) and header_pins_ok
        all_match = all_match and match
        audited.append({
            "kind": kind, "field": field, "filed": True,
            "run_id": entry["record"]["run"]["run_id"],
            "record_file": entry["path"].name,
            "header_pins_ok": header_pins_ok,
            "result_matches_recomputation": mine == entry["result"],
            "match": match,
        })
    extra = [f"{k[0]}:{k[1]}" for k in filed if k not in EXPECTED]
    if extra:
        all_match = False
    print(json.dumps({
        "spec": "093", "stage": "2", "task": "T202",
        "audit": "independent recomputation (audit_stage2.py)",
        "data_pins_verified_in_tree": pins_ok,
        "audited": audited,
        "unexpected_stage2_runs": extra,
        "verdict": "AGREE" if all_match else "DIVERGE",
    }, indent=1, sort_keys=True))
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
