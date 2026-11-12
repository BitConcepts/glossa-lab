#!/usr/bin/env python3
"""Spec 090 Stage G3 — T403 computation: the frozen
separator's administration over H1.

Computes the identity-structure profile P(T) for the six
frozen cases (A0, A1, A2, A3, C1, C2) over the held-out
set H1, exactly as frozen by
`specs/090-projected-constraints-generalization-study/records/stage-g3-freeze-record.md`
(T402, merged as PR #559; the owner's 2026-11-12 ruling
recorded in its §5 authorizes this administration).
Every constant below is the freeze's; the tool takes no
parameter that could move a result — the case and the
store are the only arguments.

Each case execution is a Spec 089 run on the `study`
surface (run-defs v2): the tool mints its run id at
execution start, and writes its run record into the
store through the registered library writer
(`backend/glossa_lab/run_records.py`), which appends
the index `entry` act. A refusal the freeze names (a
pin mismatch, a frozen count not reproducing, case
A2's floor unmet) writes an absence record
(kind `refused`) under the minted id and exits 1.

Usage (from anywhere; the repo root is derived from
this file's location):

    python3 tools/spec090/run_g3.py run-case \
        --case A0 --store <run-store-dir>

Deterministic: the study surface is registered
deterministic; comparable runs' result blocks agree
byte-for-byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from glossa_lab import run_records as rr  # noqa: E402

TOOL = "run_g3.py"
TOOL_VERSION = "1.0.0"
SPEC_DIR = "specs/090-projected-constraints-generalization-study"

# ---------------------------------------------------------------------------
# Frozen constants (stage-g3-freeze-record.md; package
# sections cited per constant). Nothing here is a choice
# this tool makes.

#: Freeze §1: the H1 source and its pin.
SNAPSHOT_REL = "glossa-corpus/indus/exports/indus_research.jsonl"
SNAPSHOT_SHA256 = (
    "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e"
)
#: Freeze §1: the §4 comparison population and its pin
#: (pinned and verified; no profile is computed over it).
FLAT_REL = "reports/mahadevan_corpus_flat.txt"
FLAT_SHA256 = (
    "878fd2231929f2105cb5c7fb37507ee7eceb7d83f355f1fa4d8e793926785c18"
)
FREEZE_REL = f"{SPEC_DIR}/records/stage-g3-freeze-record.md"

#: Freeze §2: the source-system filter.
SOURCE_SYSTEM = "indusscript-m77"
#: Freeze §3: the permitted counts the extraction must
#: reproduce exactly.
FROZEN_RECORD_COUNT = 2906
FROZEN_TOKEN_TOTAL = 12639

#: Freeze §8 (package §4): the C1 relabeling seed and
#: construction — distinct codes sorted ascending
#: (lexicographic), shuffled by random.Random(SEED)
#: under CPython 3, codes[i] mapped to shuffled[i].
SEED = 835303130428943522

#: Freeze §7 (package §4): A2's multiplicity floor.
A2_FLOOR = 10

CASES = ("A0", "A1", "A2", "A3", "C1", "C2")


class Refusal(Exception):
    """A refusal the freeze names: the execution
    declines, and the run record carries the absence
    (run-defs v2 §3.2, kind `refused`)."""


class CaseNotFormable(Refusal):
    """Freeze §7: a case that cannot be formed as
    frozen (A2's floor unmet) is an administration
    fact, not a defect to repair by moving the rule."""


# ---------------------------------------------------------------------------
# Frozen inputs


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pins() -> dict:
    """Hash both pinned source files and the freeze
    record; refuse if either source pin mismatches
    (the brief's stop condition and freeze §1)."""
    snap_sha = sha256_file(ROOT / SNAPSHOT_REL)
    if snap_sha != SNAPSHOT_SHA256:
        raise Refusal(
            f"snapshot pin mismatch: computed {snap_sha}, "
            f"frozen {SNAPSHOT_SHA256}"
        )
    flat_sha = sha256_file(ROOT / FLAT_REL)
    if flat_sha != FLAT_SHA256:
        raise Refusal(
            f"M77 flat-file pin mismatch: computed {flat_sha}, "
            f"frozen {FLAT_SHA256}"
        )
    return {
        "spec": "090",
        "stage": "G3",
        "freeze_record": FREEZE_REL,
        "freeze_record_sha256": sha256_file(ROOT / FREEZE_REL),
        "snapshot": {"path": SNAPSHOT_REL, "sha256": snap_sha},
        "m77_flat_file": {"path": FLAT_REL, "sha256": flat_sha},
    }


def extract_h1() -> list[list[str]]:
    """Freeze §2, exactly: records whose source_system
    is `indusscript-m77`; the sequence is the record's
    `canonical_grapheme_ids` list as recorded — no
    element dropped, rewritten, or re-ordered. The
    empty-list exclusion removes none (freeze §3), and
    the extracted counts must reproduce the freeze's
    permitted counts or the execution refuses."""
    sequences: list[list[str]] = []
    with (ROOT / SNAPSHOT_REL).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("source_system") != SOURCE_SYSTEM:
                continue
            seq = record.get("canonical_grapheme_ids")
            if not seq:
                continue
            sequences.append([str(code) for code in seq])
    token_total = sum(len(s) for s in sequences)
    if len(sequences) != FROZEN_RECORD_COUNT or token_total != FROZEN_TOKEN_TOTAL:
        raise Refusal(
            f"extraction does not reproduce the freeze's counts: "
            f"{len(sequences)} records / {token_total} tokens, frozen "
            f"{FROZEN_RECORD_COUNT} / {FROZEN_TOKEN_TOTAL}"
        )
    return sequences


# ---------------------------------------------------------------------------
# The separator (freeze §6; package §2)


def profile(type_sequences: list[list[str]]) -> dict:
    """P(T) = (|Sigma_O(T)|, M(T), L(T), X(T), B(T)),
    in the freeze's canonical representation:

    - inventory_size: the exercised inventory size.
    - M: per-type token multiplicities, sorted
      descending.
    - L: [length, count] pairs, sorted by length.
    - X: [initial, final, medial] triples per exercised
      type, as a multiset (sorted); a one-token
      sequence's token counts as both initial and
      final, never medial.
    - B: adjacent ordered-pair counts (zero counts
      excluded), as a multiset (sorted descending).
    """
    multiplicity: Counter[str] = Counter()
    lengths: Counter[int] = Counter()
    positional: dict[str, list[int]] = {}
    pairs: Counter[tuple[str, str]] = Counter()
    for seq in type_sequences:
        lengths[len(seq)] += 1
        last = len(seq) - 1
        for i, t in enumerate(seq):
            multiplicity[t] += 1
            triple = positional.setdefault(t, [0, 0, 0])
            if i == 0:
                triple[0] += 1
            if i == last:
                triple[1] += 1
            if 0 < i < last:
                triple[2] += 1
            if i < last:
                pairs[(t, seq[i + 1])] += 1
    return {
        "inventory_size": len(multiplicity),
        "M": sorted(multiplicity.values(), reverse=True),
        "L": [[length, lengths[length]] for length in sorted(lengths)],
        "X": sorted(triple for triple in positional.values()),
        "B": sorted(pairs.values(), reverse=True),
    }


# ---------------------------------------------------------------------------
# The frozen cases (freeze §7; package §4). Selections
# are over A0's recorded multiplicities, tie-broken as
# the freeze fixes: ascending recorded code string at
# equal multiplicity.


def _ranked_codes(multiplicity: Counter[str]) -> tuple[list[str], list[str]]:
    """(most-frequent-first, least-frequent-first) code
    orders under the freeze's tie-breaking."""
    desc = sorted(multiplicity, key=lambda c: (-multiplicity[c], c))
    asc = sorted(multiplicity, key=lambda c: (multiplicity[c], c))
    return desc, asc


def build_case(case: str, sequences: list[list[str]]):
    """Return (type_sequences, case_facts) for one
    frozen case over the recorded sequences."""
    multiplicity: Counter[str] = Counter()
    for seq in sequences:
        multiplicity.update(seq)
    desc, asc = _ranked_codes(multiplicity)

    if case == "A0":
        return [list(s) for s in sequences], {
            "rule": "the recorded coding (identity)",
        }

    if case == "C2":
        return [list(s) for s in sequences], {
            "rule": "the identity control: A0 against A0",
        }

    if case == "A1":
        head = desc[0]
        initial_label = f"{head}|split-initial"
        other_label = f"{head}|split-other"
        out = []
        initial_count = 0
        for seq in sequences:
            mapped = []
            for i, t in enumerate(seq):
                if t == head and i == 0:
                    mapped.append(initial_label)
                    initial_count += 1
                elif t == head:
                    mapped.append(other_label)
                else:
                    mapped.append(t)
            out.append(mapped)
        return out, {
            "split_code": head,
            "split_code_multiplicity": multiplicity[head],
            "initial_occurrences": initial_count,
            "other_occurrences": multiplicity[head] - initial_count,
        }

    if case == "A2":
        candidates = [c for c in asc if multiplicity[c] >= A2_FLOOR]
        if len(candidates) < 2:
            raise CaseNotFormable(
                f"A2 cannot be formed as frozen: only "
                f"{len(candidates)} code(s) have multiplicity "
                f">= {A2_FLOOR} (freeze section 7)"
            )
        a, b = candidates[0], candidates[1]
        label = f"merged|{a}+{b}"
        out = [
            [label if t in (a, b) else t for t in seq] for seq in sequences
        ]
        return out, {
            "merged_codes": [a, b],
            "multiplicities": [multiplicity[a], multiplicity[b]],
            "floor": A2_FLOOR,
        }

    if case == "A3":
        a, b = desc[0], desc[1]
        label = f"merged|{a}+{b}"
        out = [
            [label if t in (a, b) else t for t in seq] for seq in sequences
        ]
        return out, {
            "merged_codes": [a, b],
            "multiplicities": [multiplicity[a], multiplicity[b]],
        }

    if case == "C1":
        codes = sorted(multiplicity)
        shuffled = list(codes)
        random.Random(SEED).shuffle(shuffled)
        mapping = dict(zip(codes, shuffled))
        out = [[mapping[t] for t in seq] for seq in sequences]
        bijection_canonical = json.dumps(
            [[c, mapping[c]] for c in codes], ensure_ascii=False
        )
        return out, {
            "seed": SEED,
            "codes_permuted": len(codes),
            "bijection_sha256": hashlib.sha256(
                bijection_canonical.encode("utf-8")
            ).hexdigest(),
        }

    raise Refusal(f"unknown case {case!r}; the frozen list is {list(CASES)}")


# ---------------------------------------------------------------------------
# The run


def _git_head() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    sha = proc.stdout.strip()
    return sha if proc.returncode == 0 and sha else "unknown"


def run_case(case: str, store: Path) -> int:
    started = datetime.now(timezone.utc).replace(microsecond=0)
    run_id = rr.mint_run_id("study", now=started)
    command = f"run-case --case {case}"
    pins: dict = {}
    try:
        pins = verify_pins()
        sequences = extract_h1()
        type_sequences, facts = build_case(case, sequences)
        prof = profile(type_sequences)
        result = {
            "case": case,
            "spec": "090",
            "stage": "G3",
            "task": "T403",
            "object_count": len(type_sequences),
            "token_total": sum(len(s) for s in type_sequences),
            "profile": prof,
            "case_facts": facts,
        }
        finished = datetime.now(timezone.utc).replace(microsecond=0)
        header = rr.build_header(
            surface="study",
            tool=TOOL,
            tool_version=TOOL_VERSION,
            command=command,
            code_version=_git_head(),
            input_pins=pins,
            seed=SEED,
            environment_class="vm/linux",
            started=started,
            finished=finished,
            run_id=run_id,
        )
        record = rr.build_record(header, result=result)
        path = rr.write_run_record(store, record)
    except Refusal as exc:
        finished = datetime.now(timezone.utc).replace(microsecond=0)
        header = rr.build_header(
            surface="study",
            tool=TOOL,
            tool_version=TOOL_VERSION,
            command=command,
            code_version=_git_head(),
            input_pins=pins,
            seed=SEED,
            environment_class="vm/linux",
            started=started,
            finished=finished,
            run_id=run_id,
        )
        record = rr.build_record(
            header, absence={"kind": "refused", "detail": str(exc)}
        )
        path = rr.write_run_record(store, record)
        print(f"refused: {exc}", file=sys.stderr)
        print(f"absence run record: {path} ({run_id})")
        return 1
    print(f"run record: {path} ({run_id})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Spec 090 Stage G3 (T403): the frozen "
        "separator's administration over H1."
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)
    run = sub.add_parser("run-case", help="execute one frozen case")
    run.add_argument("--case", required=True, choices=list(CASES))
    run.add_argument(
        "--store",
        required=True,
        type=Path,
        help="the run store directory (the study surface's "
        "store of record for the administration; a "
        "verification re-execution names its own store)",
    )
    args = parser.parse_args(argv)
    if args.subcommand == "run-case":
        return run_case(args.case, args.store)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
