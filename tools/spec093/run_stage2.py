#!/usr/bin/env python3
"""Spec 093 Stage 2 — T202 administration: the frozen
channel-independence prediction test.

Administers, per field, exactly what
`specs/093-material-context-channel/records/t202-freeze-v1.md`
freezes: the field's recorded value is predicted from
the object's sequence table plus the T201 section 4
bookkeeping by a multinomial Naive Bayes predictor,
fitted on a seeded stratified training split and adjudged
on held-out objects, against a 200-permutation control
battery. Every constant below is the freeze's; the tool
takes no parameter that could move a result — the field
and the store are the only arguments.

Each execution is a Spec 089 run on the `study` surface
(run-defs v2): the tool mints its run id at execution
start and writes its run record into the store through
the registered library writer
(`backend/glossa_lab/run_records.py`), which appends the
index `entry` act. A refusal the freeze names (a pin
mismatch, a frozen count not reproducing) writes an
absence record (kind `refused`) under the minted id and
exits 1.

Usage (from anywhere; the repo root is derived from
this file's location):

    python3 tools/spec093/run_stage2.py run-field \
        --field site --store <run-store-dir>
    python3 tools/spec093/run_stage2.py run-controls \
        --field site --store <run-store-dir>

Deterministic: the study surface is registered
deterministic; comparable runs' result blocks agree
byte-for-byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from glossa_lab import run_records as rr  # noqa: E402

TOOL = "run_stage2.py"
TOOL_VERSION = "1.0.0"
SPEC_DIR = "specs/093-material-context-channel"

# ---------------------------------------------------------------------------
# Frozen constants (t202-freeze-v1.md). Nothing here is a
# choice this tool makes.

#: Freeze section 1: the pinned inputs.
SNAPSHOT_REL = "glossa-corpus/indus/exports/indus_research.jsonl"
SNAPSHOT_SHA256 = (
    "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e"
)
JOIN_REL = f"{SPEC_DIR}/records/t103-join-pairs-v1.jsonl"
JOIN_SHA256 = (
    "7107f738832a4e3b04cff91d81073212bc0f3a77afed6f0ccc3cee4fce621703"
)
DEFINITION_REL = f"{SPEC_DIR}/records/t201-channel-definition-2026-11-19.md"
COUNTS_REL = f"{SPEC_DIR}/records/t201-counts-2026-11-19.json"
FREEZE_REL = f"{SPEC_DIR}/records/t202-freeze-v1.md"

#: Freeze sections 3: the floors.
CLASS_FLOOR = 10
MIN_ADJUDGED_CLASSES = 2
MIN_ADJUDGED_RECORDS = 50

#: Freeze section 5: the predictor's smoothing constant.
ALPHA = 1.0

#: Freeze sections 6-7: the split and the controls.
SPLIT_SEED = 20261119
CONTROL_SEED = 20261120
TEST_FRACTION_NUM = 3  # floor(0.3 * n), as (3 * n) // 10 in exact integer arithmetic
N_PERMUTATIONS = 200
CONTROL_P99_INDEX = 197
CONTROL_VALIDITY_CEILING = 0.10

#: Freeze section 8: the bar.
BAR_KAPPA = 0.80
BAR_BALANCED_ACCURACY = 0.85

#: Freeze sections 2-3: the frozen expectations the
#: extraction must reproduce exactly, per administered
#: field (population size, adjudged classes and counts,
#: adjudged total, held-out total).
FIELDS = {
    "site": {
        "population": 966,
        "adjudged": {"Harappa": 110, "Mohenjo-daro": 839},
        "adjudged_total": 949,
        "held_out_total": 284,
    },
    "find-context": {
        "population": 175,
        "adjudged": {"DK-": 16, "DKG. (N)": 17, "DKG. (S)": 68,
                     "HRB": 13, "VSA": 11},
        "adjudged_total": 125,
        "held_out_total": 35,
    },
}

SENTINELS = {"", "None", "-", "--"}
BOOKKEEPING = ("source_system", "sign_id_scheme",
               "rights_status", "crosswalk_coverage")


class Refusal(Exception):
    """A refusal the freeze names: the execution
    declines, and the run record carries the absence
    (run-defs v2 section 3.2, kind `refused`)."""


# ---------------------------------------------------------------------------
# Frozen inputs


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_empty(v) -> bool:
    if v is None:
        return True
    if isinstance(v, (list, dict)):
        return len(v) == 0
    if isinstance(v, str):
        return v.strip() in SENTINELS
    return False


def verify_pins() -> dict:
    snap_sha = sha256_file(ROOT / SNAPSHOT_REL)
    if snap_sha != SNAPSHOT_SHA256:
        raise Refusal(
            f"snapshot pin mismatch: computed {snap_sha}, "
            f"frozen {SNAPSHOT_SHA256}"
        )
    join_sha = sha256_file(ROOT / JOIN_REL)
    if join_sha != JOIN_SHA256:
        raise Refusal(
            f"join pin mismatch: computed {join_sha}, "
            f"frozen {JOIN_SHA256}"
        )
    return {
        "spec": "093",
        "stage": "2",
        "freeze_record": FREEZE_REL,
        "freeze_record_sha256": sha256_file(ROOT / FREEZE_REL),
        "definition_record": DEFINITION_REL,
        "definition_record_sha256": sha256_file(ROOT / DEFINITION_REL),
        "counts_record": COUNTS_REL,
        "counts_record_sha256": sha256_file(ROOT / COUNTS_REL),
        "snapshot": {"path": SNAPSHOT_REL, "sha256": snap_sha},
        "join_pairs": {"path": JOIN_REL, "sha256": join_sha},
    }


def load_snapshot() -> list[dict]:
    records = []
    with (ROOT / SNAPSHOT_REL).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def population(field: str) -> list[dict]:
    """The field's administration population (freeze
    section 2): dicts with id, sequence (recorded codes),
    bookkeeping values, and the field's label. Raises
    Refusal if the frozen counts do not reproduce."""
    snap = load_snapshot()
    items: list[dict] = []
    if field == "site":
        for rec in snap:
            seq = rec.get("canonical_grapheme_ids")
            if not seq or is_empty(rec.get("site_name")):
                continue
            items.append({
                "id": rec["glossa_id"],
                "sequence": [str(c) for c in seq],
                "bookkeeping": {k: str(rec.get(k)) for k in BOOKKEEPING},
                "label": str(rec["site_name"]),
            })
    elif field == "find-context":
        by_id = {r["glossa_id"]: r for r in snap}
        with (ROOT / JOIN_REL).open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                pair = json.loads(line)
                if is_empty(pair.get("area_section")):
                    continue
                rec = by_id[pair["text_id"]]
                seq = rec.get("canonical_grapheme_ids")
                items.append({
                    "id": rec["glossa_id"],
                    "sequence": [str(c) for c in seq],
                    "bookkeeping": {k: str(rec.get(k)) for k in BOOKKEEPING},
                    "label": str(pair["area_section"]),
                })
    else:  # pragma: no cover - argparse restricts the field
        raise Refusal(f"unknown field {field!r}")
    expected = FIELDS[field]
    if len(items) != expected["population"]:
        raise Refusal(
            f"{field}: administration population is {len(items)}, "
            f"frozen {expected['population']}"
        )
    return items


def adjudged(items: list[dict], field: str):
    """Apply freeze section 3's floors; return
    (adjudged items, adjudged class counts, excluded
    class counts). Refuses if the frozen expectations do
    not reproduce."""
    counts = Counter(it["label"] for it in items)
    kept = {c: n for c, n in counts.items() if n >= CLASS_FLOOR}
    excluded = {c: n for c, n in counts.items() if n < CLASS_FLOOR}
    expected = FIELDS[field]
    if kept != expected["adjudged"]:
        raise Refusal(
            f"{field}: adjudged classes {dict(sorted(kept.items()))} do "
            f"not reproduce the freeze's {expected['adjudged']}"
        )
    if len(kept) < MIN_ADJUDGED_CLASSES or sum(kept.values()) < MIN_ADJUDGED_RECORDS:
        raise Refusal(
            f"{field}: the formation floor fires under the freeze's "
            f"own numbers (adjudged classes {len(kept)}, records "
            f"{sum(kept.values())})"
        )
    adjudged_items = [it for it in items if it["label"] in kept]
    if len(adjudged_items) != expected["adjudged_total"]:
        raise Refusal(
            f"{field}: adjudged total is {len(adjudged_items)}, "
            f"frozen {expected['adjudged_total']}"
        )
    return adjudged_items, dict(sorted(kept.items())), dict(sorted(excluded.items()))


# ---------------------------------------------------------------------------
# Features, predictor, split, metrics (freeze sections
# 4-6, 8)


def events(item: dict) -> list[tuple[str, str]]:
    seq = item["sequence"]
    ev: list[tuple[str, str]] = [("tok", code) for code in seq]
    ev.append(("first", seq[0]))
    ev.append(("last", seq[-1]))
    ev.append(("len", str(len(seq))))
    ev.append(("distinct", str(len(set(seq)))))
    for key in BOOKKEEPING:
        ev.append((f"bk:{key}", item["bookkeeping"][key]))
    return ev


def split(items: list[dict]):
    """Freeze section 6: one Random(SPLIT_SEED) stream,
    classes in ascending label order, ids ascending,
    first max(1, (3*n)//10) shuffled ids held out."""
    rng = random.Random(SPLIT_SEED)
    by_class: dict[str, list[dict]] = {}
    for it in items:
        by_class.setdefault(it["label"], []).append(it)
    train, test = [], []
    for label in sorted(by_class):
        group = sorted(by_class[label], key=lambda it: it["id"])
        ids = [it["id"] for it in group]
        rng.shuffle(ids)
        n_test = max(1, (TEST_FRACTION_NUM * len(ids)) // 10)
        test_ids = set(ids[:n_test])
        for it in group:
            (test if it["id"] in test_ids else train).append(it)
    return train, test


def fit(train: list[dict]):
    classes = sorted({it["label"] for it in train})
    class_counts = Counter(it["label"] for it in train)
    event_counts: dict[str, Counter] = {c: Counter() for c in classes}
    totals: Counter = Counter()
    vocab: set[tuple[str, str]] = set()
    for it in train:
        ev = events(it)
        event_counts[it["label"]].update(ev)
        totals[it["label"]] += len(ev)
        vocab.update(ev)
    return {
        "classes": classes,
        "class_counts": dict(sorted(class_counts.items())),
        "event_counts": event_counts,
        "totals": dict(totals),
        "vocab_size": len(vocab),
        "vocab": vocab,
        "n_train": len(train),
    }


def predict(model: dict, item: dict) -> str:
    ev = [e for e in events(item) if e in model["vocab"]]
    best_label, best_score = None, None
    for c in model["classes"]:
        denom = model["totals"][c] + ALPHA * model["vocab_size"]
        score = math.log(model["class_counts"][c] / model["n_train"])
        counts = model["event_counts"][c]
        for e in ev:
            score += math.log((counts.get(e, 0) + ALPHA) / denom)
        if best_score is None or score > best_score:
            best_label, best_score = c, score
    return best_label


def metrics(test: list[dict], predictions: list[str], classes: list[str]) -> dict:
    confusion: dict[str, dict[str, int]] = {
        a: {p: 0 for p in classes} for a in classes
    }
    correct = 0
    for it, pred in zip(test, predictions):
        confusion[it["label"]][pred] += 1
        if pred == it["label"]:
            correct += 1
    n = len(test)
    accuracy = correct / n
    recalls = {}
    for c in classes:
        actual = sum(confusion[c].values())
        recalls[c] = confusion[c][c] / actual if actual else 0.0
    balanced = sum(recalls[c] for c in classes) / len(classes)
    pe = 0.0
    for c in classes:
        actual_total = sum(confusion[c].values())
        pred_total = sum(confusion[a][c] for a in classes)
        pe += (actual_total * pred_total) / (n * n)
    if pe >= 1.0:
        kappa = 1.0 if accuracy >= 1.0 else 0.0
    else:
        kappa = (accuracy - pe) / (1.0 - pe)
    return {
        "n_held_out": n,
        "accuracy": accuracy,
        "balanced_accuracy": balanced,
        "kappa": kappa,
        "per_class_recall": {c: recalls[c] for c in classes},
        "confusion": confusion,
    }


def administer(items: list[dict]) -> dict:
    """One full administration (freeze sections 4-6, 8)
    over adjudged items: split, fit, predict, metrics,
    plus the majority-rule scale metrics."""
    train, test = split(items)
    model = fit(train)
    predictions = [predict(model, it) for it in test]
    m = metrics(test, predictions, model["classes"])
    majority = max(model["classes"],
                   key=lambda c: (model["class_counts"][c], c))
    maj = metrics(test, [majority] * len(test), model["classes"])
    return {
        "train_size": len(train),
        "held_out_size": len(test),
        "vocabulary_size": model["vocab_size"],
        "metrics": m,
        "majority_rule": {
            "class": majority,
            "accuracy": maj["accuracy"],
            "balanced_accuracy": maj["balanced_accuracy"],
            "kappa": maj["kappa"],
        },
    }


# ---------------------------------------------------------------------------
# The runs


def _git_head() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=30, check=False,
    )
    sha = proc.stdout.strip()
    return sha if proc.returncode == 0 and sha else "unknown"


def _write(store: Path, command: str, seed: int,
           started: datetime, make_result) -> int:
    run_id = rr.mint_run_id("study", now=started)
    pins: dict = {}
    try:
        result = make_result(pins)
    except Refusal as exc:
        finished = datetime.now(timezone.utc).replace(microsecond=0)
        header = rr.build_header(
            surface="study", tool=TOOL, tool_version=TOOL_VERSION,
            command=command, code_version=_git_head(), input_pins=pins,
            seed=seed, environment_class="mini-server/linux",
            started=started, finished=finished, run_id=run_id,
        )
        record = rr.build_record(
            header, absence={"kind": "refused", "detail": str(exc)})
        path = rr.write_run_record(store, record)
        print(f"refused: {exc}", file=sys.stderr)
        print(f"absence run record: {path} ({run_id})")
        return 1
    finished = datetime.now(timezone.utc).replace(microsecond=0)
    header = rr.build_header(
        surface="study", tool=TOOL, tool_version=TOOL_VERSION,
        command=command, code_version=_git_head(), input_pins=pins,
        seed=seed, environment_class="mini-server/linux",
        started=started, finished=finished, run_id=run_id,
    )
    record = rr.build_record(header, result=result)
    path = rr.write_run_record(store, record)
    print(f"run record: {path} ({run_id})")
    return 0


def run_field(field: str, store: Path) -> int:
    started = datetime.now(timezone.utc).replace(microsecond=0)
    command = f"run-field --field {field}"

    def make(pins: dict):
        pins.update(verify_pins())
        items = population(field)
        adj, kept, excluded = adjudged(items, field)
        outcome = administer(adj)
        if outcome["held_out_size"] != FIELDS[field]["held_out_total"]:
            raise Refusal(
                f"{field}: held-out total is {outcome['held_out_size']}, "
                f"frozen {FIELDS[field]['held_out_total']}"
            )
        return {
            "spec": "093", "stage": "2", "task": "T202",
            "kind": "administration", "field": field,
            "population": len(items),
            "adjudged_classes": kept,
            "excluded_classes": excluded,
            "adjudged_total": len(adj),
            **outcome,
        }

    return _write(store, command, SPLIT_SEED, started, make)


def run_controls(field: str, store: Path) -> int:
    started = datetime.now(timezone.utc).replace(microsecond=0)
    command = f"run-controls --field {field}"

    def make(pins: dict):
        pins.update(verify_pins())
        items = population(field)
        adj, kept, _excluded = adjudged(items, field)
        ids_sorted = sorted(it["id"] for it in adj)
        by_id = {it["id"]: it for it in adj}
        labels_in_id_order = [by_id[i]["label"] for i in ids_sorted]
        rng = random.Random(CONTROL_SEED)
        kappas: list[float] = []
        for _ in range(N_PERMUTATIONS):
            permuted = list(labels_in_id_order)
            rng.shuffle(permuted)
            relabeled = []
            for rid, lab in zip(ids_sorted, permuted):
                clone = dict(by_id[rid])
                clone["label"] = lab
                relabeled.append(clone)
            outcome = administer(relabeled)
            kappas.append(outcome["metrics"]["kappa"])
        ordered = sorted(kappas)
        return {
            "spec": "093", "stage": "2", "task": "T202",
            "kind": "permutation-controls", "field": field,
            "adjudged_classes": kept,
            "adjudged_total": len(adj),
            "n_permutations": N_PERMUTATIONS,
            "kappa_values": kappas,
            "kappa_max": ordered[-1],
            "kappa_mean": sum(kappas) / len(kappas),
            "kappa_p99_index197": ordered[CONTROL_P99_INDEX],
            "validity_ceiling": CONTROL_VALIDITY_CEILING,
            "controls_valid": ordered[CONTROL_P99_INDEX] < CONTROL_VALIDITY_CEILING,
        }

    return _write(store, command, CONTROL_SEED, started, make)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Spec 093 Stage 2 (T202): the frozen "
        "channel-independence administration.")
    sub = parser.add_subparsers(dest="subcommand", required=True)
    for name in ("run-field", "run-controls"):
        p = sub.add_parser(name)
        p.add_argument("--field", required=True, choices=sorted(FIELDS))
        p.add_argument("--store", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.subcommand == "run-field":
        return run_field(args.field, args.store)
    return run_controls(args.field, args.store)


if __name__ == "__main__":
    raise SystemExit(main())
