#!/usr/bin/env python3
"""Complete a run store's legacy index (Spec 089 Stage 5,
T501; D-089-5 index-only reach-back; the completion
rules as amended by run-defs v2 §7.2, 2026-11-05).

Enumerates every run record that has ever stood in the
settling store from the store's git history (the commits
on HEAD's line that touch the store), and appends the
acts the index still lacks, under the population rule
run-defs v2 §7.2 states:

- a record still standing in the store and not yet
  entered is entered from its standing bytes;
- a record no longer in the store and not yet entered
  is entered from its final blob, and its entry names
  the superseding commit (the first store-touching
  commit whose tree no longer carries it), the record's
  git blob id, and the SHA-256 of the blob's bytes;
- a generation that was entered standing and has since
  departed the store gains a `departure` act (run-defs
  v2 §7.1) carrying that same accounting — the entry
  act is immutable, so the accounting is appended,
  never edited in — unless a departure act or the
  entry's own fields already account it;
- a record carrying a run header is a post-spec record,
  entered by its own writer under its own run id and
  never legacy-derived: the history pass skips it and
  names the skip on its output (skip-with-record), and
  never refuses on it;
- each `re_derivations` entry in
  `glossa-indus/ledger/settling-canonical.json` is
  entered as a legacy run event pointing at that file.

A headerless record missing a recoverable key component
remains a named refusal: it belongs to the legacy
population and is not half-entered.

Legacy entries are index acts only: no record's bytes
are read for anything but key recovery, and no record is
ever written (C089-17). Appends go through
`run_records.append_act`, so the fold's refusals bind
this tool as they bind every writer; a second run over a
completed index appends nothing (idempotent — entered
ids are skipped by name, departed generations already
accounted are skipped likewise).

Usage (from the repo root):

    python3 tools/ledger/build_legacy_index.py [--root PATH]
        [--dry-run]

Exit code 0 on success; a refusal (not a git checkout,
an unrecoverable record, a fold refusal) exits 1 with
the refusal named on stderr.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Any, Optional  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab import run_records as rr  # noqa: E402

STORE_REL = "glossa-indus/ledger/runs"
CANONICAL_REL = "glossa-indus/ledger/settling-canonical.json"
INDEX_NAME = "run-index.jsonl"

#: The `ref` a builder-appended departure act carries:
#: the act that ordered the accounting is this
#: completion pass itself, under the run-defs v2
#: amendment of record.
DEPARTURE_REF = (
    "tools/ledger/build_legacy_index.py completion pass "
    "(run-defs v2 departed-generation accounting, "
    "amendment record 2026-11-05)"
)


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise rr.RunRecordError(
            f"git {' '.join(args)} failed: {proc.stderr.strip()}"
        )
    return proc.stdout


def store_history(root: Path) -> list[dict[str, Any]]:
    """Every record file that has ever stood in the
    settling store on HEAD's history, in first-appearance
    order. Each item: `name` (store-relative filename),
    `present` (stands in the store at HEAD), `git_blob`
    and `blob` (the record's final blob: at HEAD when
    present, else at the last commit carrying it),
    `superseded_by_commit` (None when present)."""
    commits = [
        line
        for line in _git(
            root, "rev-list", "--reverse", "HEAD", "--", STORE_REL
        ).splitlines()
        if line.strip()
    ]
    if not commits:
        raise rr.RunRecordError(
            f"no git history touches {STORE_REL} under {root} — "
            "the legacy enumeration has nothing to stand on"
        )
    trees: list[tuple[str, dict[str, str]]] = []
    for commit in commits:
        listing = _git(
            root, "ls-tree", commit, "--", STORE_REL + "/"
        )
        names: dict[str, str] = {}
        for line in listing.splitlines():
            meta, _, rel = line.partition("\t")
            name = rel.rsplit("/", 1)[-1]
            if name.endswith(".json") and name != INDEX_NAME:
                names[name] = meta.split()[2]
        trees.append((commit, names))
    order: list[str] = []
    for _, names in trees:
        for name in names:
            if name not in order:
                order.append(name)
    history: list[dict[str, Any]] = []
    for name in order:
        last_with: Optional[int] = None
        for idx, (_, names) in enumerate(trees):
            if name in names:
                last_with = idx
        assert last_with is not None
        commit, names = trees[last_with]
        blob_id = names[name]
        blob = subprocess.run(
            ["git", "cat-file", "blob", blob_id],
            cwd=root,
            capture_output=True,
        )
        if blob.returncode != 0:
            raise rr.RunRecordError(
                f"git cat-file blob {blob_id} failed: "
                f"{blob.stderr.decode('utf-8', 'replace').strip()}"
            )
        present = last_with == len(trees) - 1
        history.append(
            {
                "name": name,
                "present": present,
                "git_blob": blob_id,
                "blob": blob.stdout,
                "superseded_by_commit": (
                    None if present else trees[last_with + 1][0]
                ),
            }
        )
    return history


def canonical_event_act(index: int, event: dict[str, Any]) -> dict[str, Any]:
    """The legacy `entry` act for one `re_derivations`
    event in settling-canonical.json: a legacy run event
    pointing at that file, its key the components the
    event itself records (its date and its act)."""
    return {
        "act": "entry",
        "run_id": f"legacy:settling-canonical/re_derivations[{index}]",
        "record": "settling-canonical.json",
        "event": f"re_derivations[{index}]",
        "key": {
            "surface": "settling",
            "semantics": "glossa-settle-1",
            "date": event.get("date"),
            "act": event.get("act"),
        },
        "legacy": True,
        "key_partial": True,
        "label": rr.LEGACY_LABEL,
        "missing": list(rr.SETTLING_LEGACY_MISSING),
    }


def build_legacy_acts(
    root: Path,
) -> tuple[list[dict[str, Any]], list[str]]:
    """The acts the settling store's index still lacks,
    in enumeration order: store generations first
    (first-appearance order), then the canonical
    re-derivation events — plus the names of the
    post-spec records the history pass skipped-with-
    record. Entered ids are skipped by name, so both
    lists are empty over a completed index.

    The population rule is run-defs v2 §7.2's: an
    entered generation that has departed gains a
    `departure` act (unless already accounted, on its
    entry or by a departure act); an unentered
    headerless record is legacy population and is
    entered; an unentered record carrying a run header
    is a post-spec record, skipped-with-record and
    never refused on."""
    store = root / STORE_REL
    index_path = store / INDEX_NAME
    folded = (
        rr.fold_index(index_path)
        if index_path.is_file()
        else rr.IndexState()
    )
    entered = set(folded.entries)
    accounted = set(folded.departed)
    acts: list[dict[str, Any]] = []
    skipped: list[str] = []
    for item in store_history(root):
        run_id = rr.legacy_run_id(item["name"])
        if run_id in entered:
            if item["present"] or run_id in accounted:
                continue
            if folded.entries[run_id].get("superseded_by_commit"):
                # Entered after departing: the entry
                # itself carries the accounting.
                continue
            acts.append(
                rr.departure_act(
                    run_id,
                    item["name"],
                    superseded_by_commit=item[
                        "superseded_by_commit"
                    ],
                    git_blob=item["git_blob"],
                    blob_sha256=hashlib.sha256(
                        item["blob"]
                    ).hexdigest(),
                    ref=DEPARTURE_REF,
                )
            )
            accounted.add(run_id)
            continue
        try:
            record = json.loads(item["blob"].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise rr.RunRecordError(
                f"legacy recovery: historical record "
                f"{item['name']!r} is not readable JSON: {exc}"
            ) from exc
        if isinstance(record, dict) and "run" in record:
            # A post-spec record: entered by its writer
            # under its own run id, never legacy-derived.
            skipped.append(item["name"])
            continue
        act = rr.legacy_entry_for_record(item["name"], record)
        if not item["present"]:
            act["superseded_by_commit"] = item["superseded_by_commit"]
            act["git_blob"] = item["git_blob"]
            act["blob_sha256"] = hashlib.sha256(item["blob"]).hexdigest()
        acts.append(act)
    canonical_path = root / CANONICAL_REL
    if canonical_path.is_file():
        canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
        for idx, event in enumerate(canonical.get("re_derivations") or []):
            act = canonical_event_act(idx, event)
            if act["run_id"] not in entered:
                acts.append(act)
    return acts, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repo root (default: this repo)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="enumerate and print the acts without appending",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    index_path = root / STORE_REL / INDEX_NAME
    try:
        acts, skipped = build_legacy_acts(root)
        if not args.dry_run:
            for act in acts:
                rr.append_act(index_path, act)
    except rr.RunRecordError as exc:
        print(f"LEGACY INDEX REFUSED: {exc}", file=sys.stderr)
        return 1
    state = rr.fold_index(index_path)
    for act in acts:
        if act["act"] == "departure":
            print(
                f"departure {act['run_id']} — record "
                "(departed, accounted)"
            )
            continue
        kind = (
            "record (standing)"
            if act["run_id"].startswith("legacy:")
            and "event" not in act
            and "superseded_by_commit" not in act
            else (
                "canonical re-derivation event"
                if "event" in act
                else "record (superseded)"
            )
        )
        print(f"entry {act['run_id']} — {kind}")
    for name in skipped:
        print(
            f"skip {name} — post-spec record (run header "
            "present); entered by its writer, never "
            "legacy-derived"
        )
    print(
        f"legacy index: {len(acts)} act(s) "
        f"{'enumerated (dry run)' if args.dry_run else 'appended'}; "
        f"folded census {state.census} entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
