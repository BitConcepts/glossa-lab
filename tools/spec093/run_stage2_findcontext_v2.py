#!/usr/bin/env python3
"""Spec 093 Stage 2 — T202 find-context successor
administration (freeze v2).

Administers, for the find-context field only, exactly
what `specs/093-material-context-channel/records/t202-findcontext-freeze-v2.md`
freezes: the field's recorded value is predicted from
the object's sequence table plus the T201 section 4
bookkeeping by a multinomial Naive Bayes predictor,
adjudged by repeated stratified 5-fold cross-validation
(10 repeats, every adjudged record predicted out-of-fold
in every repeat), against a 200-permutation control
battery whose statistic is the same repeat-mean kappa.
Every constant below is the freeze's; the tool takes no
parameter that could move a result — the store is the
only argument besides the subcommand.

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

    python3 tools/spec093/run_stage2_findcontext_v2.py \
        run-field --store <run-store-dir>
    python3 tools/spec093/run_stage2_findcontext_v2.py \
        run-controls --store <run-store-dir>

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
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from glossa_lab import run_records as rr  # noqa: E402

TOOL = "run_stage2_findcontext_v2.py"
TOOL_VERSION = "1.0.0"
SPEC_DIR = "specs/093-material-context-channel"
FIELD = "find-context"

# ---------------------------------------------------------------------------
# Frozen constants (t202-findcontext-freeze-v2.md).
# Nothing here is a choice this tool makes.

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
FREEZE_REL = f"{SPEC_DIR}/records/t202-findcontext-freeze-v2.md"
V1_FREEZE_REL = f"{SPEC_DIR}/records/t202-freeze-v1.md"
STAGE2_RECORD_REL = f"{SPEC_DIR}/records/stage2-record-2026-11-19.md"

#: Freeze section 2: the floors.
CLASS_FLOOR = 10
MIN_ADJUDGED_CLASSES = 2
MIN_ADJUDGED_RECORDS = 50

#: Freeze section 2: the frozen expectations the
#: extraction must reproduce exactly.
POPULATION_TOTAL = 175
ADJUDGED_CLASSES = {"DK-": 16, "DKG. (N)": 17, "DKG. (S)": 68,
                    "HRB": 13, "VSA": 11}
ADJUDGED_TOTAL = 125

#: Freeze section 4: the predictor's smoothing constant.
ALPHA = 1.0

#: Freeze sections 5-6: the evaluation design and the
#: controls.
SPLIT_SEED_BASE = 20261121
CONTROL_SEED = 20261122
N_FOLDS = 5
N_REPEATS = 10
N_PERMUTATIONS = 200
CONTROL_P99_INDEX = 197
CONTROL_VALIDITY_CEILING = 0.10

#: Freeze section 7: the bar.
BAR_KAPPA = 0.80
BAR_BALANCED_ACCURACY = 0.85

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
        "freeze": "v2",
        "freeze_record": FREEZE_REL,
        "freeze_record_sha256": sha256_file(ROOT / FREEZE_REL),
        "superseded_freeze_record": V1_FREEZE_REL,
        "superseded_freeze_record_sha256": sha256_file(ROOT / V1_FREEZE_REL),
        "stage2_record": STAGE2_RECORD_REL,
        "stage2_record_sha256": sha256_file(ROOT / STAGE2_RECORD_REL),
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


def population() -> list[dict]:
    """The field's administration population (freeze
    section 2): dicts with id, sequence (recorded codes),
    bookkeeping values, and the field's label. Raises
    Refusal if the frozen counts do not reproduce."""
    snap = load_snapshot()
    by_id = {r["glossa_id"]: r for r in snap}
    items: list[dict] = []
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
    if len(items) != POPULATION_TOTAL:
        raise Refusal(
            f"find-context: administration population is {len(items)}, "
            f"frozen {POPULATION_TOTAL}"
        )
    return items


def adjudged(items: list[dict]):
    """Apply freeze section 2's floors; return
    (adjudged items, adjudged class counts, excluded
    class counts). Refuses if the frozen expectations do
    not reproduce."""
    counts = Counter(it["label"] for it in items)
    kept = {c: n for c, n in counts.items() if n >= CLASS_FLOOR}
    excluded = {c: n for c, n in counts.items() if n < CLASS_FLOOR}
    if kept != ADJUDGED_CLASSES:
        raise Refusal(
            f"find-context: adjudged classes {dict(sorted(kept.items()))} "
            f"do not reproduce the freeze's {ADJUDGED_CLASSES}"
        )
    if len(kept) < MIN_ADJUDGED_CLASSES or sum(kept.values()) < MIN_ADJUDGED_RECORDS:
        raise Refusal(
            "find-context: the formation floor fires under the "
            f"freeze's own numbers (adjudged classes {len(kept)}, "
            f"records {sum(kept.values())})"
        )
    adjudged_items = [it for it in items if it["label"] in kept]
    if len(adjudged_items) != ADJUDGED_TOTAL:
        raise Refusal(
            f"find-context: adjudged total is {len(adjudged_items)}, "
            f"frozen {ADJUDGED_TOTAL}"
        )
    return adjudged_items, dict(sorted(kept.items())), dict(sorted(excluded.items()))


# ---------------------------------------------------------------------------
# Features, predictor, folds, metrics (freeze sections
# 3-5, 7)


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


def folds(items: list[dict], repeat: int) -> list[set]:
    """Freeze section 5: one Random(SPLIT_SEED_BASE +
    repeat) stream, classes in ascending label order, ids
    ascending, shuffled with the continuing stream; fold
    f takes positions f, f+5, f+10, ... of each class's
    shuffled list. Returns the N_FOLDS held-out id sets."""
    rng = random.Random(SPLIT_SEED_BASE + repeat)
    by_class: dict[str, list[dict]] = {}
    for it in items:
        by_class.setdefault(it["label"], []).append(it)
    held: list[set] = [set() for _ in range(N_FOLDS)]
    for label in sorted(by_class):
        group = sorted(by_class[label], key=lambda it: it["id"])
        ids = [it["id"] for it in group]
        rng.shuffle(ids)
        for f in range(N_FOLDS):
            held[f].update(ids[f::N_FOLDS])
    return held


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


def metrics_from_confusion(confusion: dict, classes: list[str]):
    """Metrics from a confusion matrix (freeze section
    7), computed in exact rational arithmetic and emitted
    as floats: two independent implementations of the
    same mathematics must agree on the emitted values
    bit-for-bit. Returns (metrics dict, exact kappa,
    exact balanced accuracy)."""
    n = sum(sum(row.values()) for row in confusion.values())
    correct = sum(confusion[c][c] for c in classes)
    accuracy = Fraction(correct, n)
    recalls = {}
    for c in classes:
        actual = sum(confusion[c].values())
        recalls[c] = Fraction(confusion[c][c], actual) if actual else Fraction(0)
    balanced = sum(recalls[c] for c in classes) / len(classes)
    pe = sum(
        Fraction(sum(confusion[c].values())
                 * sum(confusion[a][c] for a in classes), n * n)
        for c in classes
    )
    if pe >= 1:
        kappa = Fraction(1) if accuracy >= 1 else Fraction(0)
    else:
        kappa = (accuracy - pe) / (1 - pe)
    return {
        "n": n,
        "accuracy": float(accuracy),
        "balanced_accuracy": float(balanced),
        "kappa": float(kappa),
        "per_class_recall": {c: float(recalls[c]) for c in classes},
        "confusion": confusion,
    }, kappa, balanced


def empty_confusion(classes: list[str]) -> dict:
    return {a: {p: 0 for p in classes} for a in classes}


def administer(items: list[dict]):
    """One full administration under freeze section 5:
    N_REPEATS repeats of stratified N_FOLDS-fold
    cross-validation. Returns (result body dict, exact
    mean kappa Fraction, exact mean balanced-accuracy
    Fraction)."""
    classes = sorted({it["label"] for it in items})
    by_id = {it["id"]: it for it in items}
    per_repeat = []
    pooled = empty_confusion(classes)
    kappas_exact: list[Fraction] = []
    balanced_exact: list[Fraction] = []
    maj_kappas_exact: list[Fraction] = []
    maj_balanced_exact: list[Fraction] = []
    for r in range(N_REPEATS):
        held_sets = folds(items, r)
        confusion = empty_confusion(classes)
        maj_confusion = empty_confusion(classes)
        vocab_sizes = []
        for f in range(N_FOLDS):
            test = [by_id[i] for i in sorted(held_sets[f])]
            train = [it for it in items if it["id"] not in held_sets[f]]
            model = fit(train)
            vocab_sizes.append(model["vocab_size"])
            majority = max(model["classes"],
                           key=lambda c: (model["class_counts"][c], c))
            for it in test:
                confusion[it["label"]][predict(model, it)] += 1
                maj_confusion[it["label"]][majority] += 1
        m, kap, bal = metrics_from_confusion(confusion, classes)
        maj_m, maj_kap, maj_bal = metrics_from_confusion(maj_confusion, classes)
        kappas_exact.append(kap)
        balanced_exact.append(bal)
        maj_kappas_exact.append(maj_kap)
        maj_balanced_exact.append(maj_bal)
        for a in classes:
            for p in classes:
                pooled[a][p] += confusion[a][p]
        per_repeat.append({
            "repeat": r,
            "kappa": m["kappa"],
            "balanced_accuracy": m["balanced_accuracy"],
            "accuracy": m["accuracy"],
            "per_class_recall": m["per_class_recall"],
            "confusion": confusion,
            "vocabulary_sizes_by_fold": vocab_sizes,
        })
    kappa_mean = sum(kappas_exact) / len(kappas_exact)
    balanced_mean = sum(balanced_exact) / len(balanced_exact)
    body = {
        "n_repeats": N_REPEATS,
        "n_folds": N_FOLDS,
        "per_repeat": per_repeat,
        "kappa_mean": float(kappa_mean),
        "balanced_accuracy_mean": float(balanced_mean),
        "pooled_confusion": pooled,
        "majority_rule": {
            "kappa_mean": float(sum(maj_kappas_exact) / len(maj_kappas_exact)),
            "balanced_accuracy_mean": float(
                sum(maj_balanced_exact) / len(maj_balanced_exact)),
        },
    }
    return body, kappa_mean, balanced_mean


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


def run_field(store: Path) -> int:
    started = datetime.now(timezone.utc).replace(microsecond=0)
    command = "run-field --field find-context"

    def make(pins: dict):
        pins.update(verify_pins())
        items = population()
        adj, kept, excluded = adjudged(items)
        body, _kap, _bal = administer(adj)
        return {
            "spec": "093", "stage": "2", "task": "T202-successor",
            "freeze": "v2",
            "kind": "administration", "field": FIELD,
            "population": len(items),
            "adjudged_classes": kept,
            "excluded_classes": excluded,
            "adjudged_total": len(adj),
            **body,
        }

    return _write(store, command, SPLIT_SEED_BASE, started, make)


def run_controls(store: Path) -> int:
    started = datetime.now(timezone.utc).replace(microsecond=0)
    command = "run-controls --field find-context"

    def make(pins: dict):
        pins.update(verify_pins())
        items = population()
        adj, kept, _excluded = adjudged(items)
        ids_sorted = sorted(it["id"] for it in adj)
        by_id = {it["id"]: it for it in adj}
        labels_in_id_order = [by_id[i]["label"] for i in ids_sorted]
        rng = random.Random(CONTROL_SEED)
        kappas: list[float] = []
        kappas_exact: list[Fraction] = []
        for _ in range(N_PERMUTATIONS):
            permuted = list(labels_in_id_order)
            rng.shuffle(permuted)
            relabeled = []
            for rid, lab in zip(ids_sorted, permuted):
                clone = dict(by_id[rid])
                clone["label"] = lab
                relabeled.append(clone)
            _body, kappa_mean_exact, _bal = administer(relabeled)
            kappas.append(float(kappa_mean_exact))
            kappas_exact.append(kappa_mean_exact)
        ordered = sorted(kappas)
        return {
            "spec": "093", "stage": "2", "task": "T202-successor",
            "freeze": "v2",
            "kind": "permutation-controls", "field": FIELD,
            "adjudged_classes": kept,
            "adjudged_total": len(adj),
            "n_permutations": N_PERMUTATIONS,
            "kappa_mean_values": kappas,
            "kappa_mean_max": ordered[-1],
            "kappa_mean_mean": float(sum(kappas_exact) / len(kappas_exact)),
            "kappa_mean_p99_index197": ordered[CONTROL_P99_INDEX],
            "validity_ceiling": CONTROL_VALIDITY_CEILING,
            "controls_valid": ordered[CONTROL_P99_INDEX] < CONTROL_VALIDITY_CEILING,
        }

    return _write(store, command, CONTROL_SEED, started, make)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Spec 093 Stage 2 (T202 successor, freeze "
        "v2): the find-context channel-independence "
        "administration.")
    sub = parser.add_subparsers(dest="subcommand", required=True)
    for name in ("run-field", "run-controls"):
        p = sub.add_parser(name)
        p.add_argument("--store", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.subcommand == "run-field":
        return run_field(args.store)
    return run_controls(args.store)


if __name__ == "__main__":
    raise SystemExit(main())
