"""Restore the jambu-dedr DEDR dataset at its recorded pin.

The DEDR dataset the program consumes was held as a bare gitlink at
``reports/jambu-dedr`` -- commit
``d5050e5a9671012df416e9c474c75aba41c07f8c`` of the upstream Jambu
data repository (``moli-mandala/data``: "a CLDF database for the
Jambu application", Aryaman Arora) -- with no ``.gitmodules`` in any
history, so the submodule could never be re-populated from the
record alone and the content was lost with the era's working
machine (recovery hunt, 2026-11-17: DEDR NOT RECOVERED).

The upstream repository is live again under its true identity and
the pinned commit is fetchable; Software Heritage holds the same
revision (directory ``ce6541aa7b96c31d0ea88e4a116e698e5fc187b9``)
and its recorded per-file content ids agree with the table below.
This script restores the consumed surface of that pinned tree --
``data/dedr/`` and ``cldf/``, plus the upstream README -- into
``reports/jambu-dedr/`` and verifies every placed file's git blob
SHA-1 against the pinned table before copying it.  The upstream
tree's other subtrees (CDIAL, Munda, other forms, model code) are
not DEDR dataset content and are not placed.

The dataset bytes are placed, never committed: the gitlink stays
the tree's only entry for ``reports/jambu-dedr``, exactly as the
program always held it.

Usage:
    python restore_jambu_dedr.py             # fetch, verify, place
    python restore_jambu_dedr.py --verify    # verify the placed tree
                                             # and print a JSON record

``--verify`` also exercises the program's own consumers over the
placed tree (the battery v2 DEDR loader and test, and the CLDF
loader summary) and reports their counts.  It mints no run record
and files no act: acceptance of the restored dataset is a separate
recorded act, and no study leg is re-run by this tooling.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET = REPO_ROOT / "reports" / "jambu-dedr"

UPSTREAM_URL = "https://github.com/moli-mandala/data"
PIN = "d5050e5a9671012df416e9c474c75aba41c07f8c"
SWH_DIRECTORY = "ce6541aa7b96c31d0ea88e4a116e698e5fc187b9"

# target-relative path -> (upstream-relative path, git blob sha1, size)
FILES: dict[str, tuple[str, str, int]] = {
    "README.md": ("README.md", "291ae6fff0d04e9bca8c0b9aa36baeb7dcd0f6df", 3527),
    "data/dedr/abbrevs.py": (
        "data/dedr/abbrevs.py", "efc508342a767c6a88ffd645165dd9a5318a8471", 8873),
    "data/dedr/dedr.csv": (
        "data/dedr/dedr.csv", "928c7338e148154a3cc30b10705b7810cf836dba", 5251799),
    "data/dedr/dedr.pickle": (
        "data/dedr/dedr.pickle", "d59272f0d975fd79b6deaafa58428b78d12a565b", 4266294),
    "data/dedr/dedr_new.csv": (
        "data/dedr/dedr_new.csv", "4f8411f19b9e3c2c0c235a24096d59d4afc558f1", 5478240),
    "data/dedr/dedr_new_entry_oct2013_edited.sql": (
        "data/dedr/dedr_new_entry_oct2013_edited.sql",
        "ac86809f942025318e9c97822ef27477441e198f", 8425279),
    "data/dedr/get_params.py": (
        "data/dedr/get_params.py", "75489e04d756cd072bb5f5f82336faa57ef2063a", 634),
    "data/dedr/params.csv": (
        "data/dedr/params.csv", "ae87dc8d393443fd55bc63992247094a0caddc54", 82802),
    "data/dedr/parse.py": (
        "data/dedr/parse.py", "9701706a870f5a507744ba7d77ad448152dc16e6", 9327),
    "data/dedr/pdr.csv": (
        "data/dedr/pdr.csv", "8cef0ec159a9d14ccea45c1431b61a5d65f81014", 67311),
    "cldf/Wordlist-metadata.json": (
        "cldf/Wordlist-metadata.json", "b6b2963bd1f903c15687dd72664d992b296d9005", 7355),
    "cldf/forms.csv": (
        "cldf/forms.csv", "1e914246cf927ac277b503f6178142b49a773332", 20702890),
    "cldf/languages.csv": (
        "cldf/languages.csv", "afb7a0b9e95e10665d12aa0712183461e59a6caa", 34099),
    "cldf/parameters.csv": (
        "cldf/parameters.csv", "490d4e9f9fca1dc6dc7ba715b8fc0a084a126621", 2972505),
    "cldf/sources.bib": (
        "cldf/sources.bib", "3da58d2c37f621e3e71fb2ed453babc793f9281c", 43778),
}

DEDR_NEW_SHA256 = "fbcc2b2d47c9be24338d846319de2b2c5a2ad4f45451274e3223bc63bc60cae0"


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def check_file(path: Path, want_sha1: str, want_size: int) -> dict:
    data = path.read_bytes()
    got = blob_sha1(data)
    return {
        "path": str(path.relative_to(TARGET)),
        "size": len(data),
        "size_ok": len(data) == want_size,
        "blob_sha1": got,
        "blob_sha1_ok": got == want_sha1,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def restore() -> list[dict]:
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "upstream"
        subprocess.run(
            ["git", "clone", "--quiet", UPSTREAM_URL, str(src)], check=True)
        subprocess.run(
            ["git", "-C", str(src), "checkout", "--quiet", PIN], check=True)
        head = subprocess.run(
            ["git", "-C", str(src), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True).stdout.strip()
        if head != PIN:
            raise SystemExit(f"upstream HEAD {head} != pin {PIN}")
        results = []
        for rel, (up_rel, want_sha1, want_size) in FILES.items():
            data = (src / up_rel).read_bytes()
            got = blob_sha1(data)
            if got != want_sha1 or len(data) != want_size:
                raise SystemExit(
                    f"hash mismatch for {up_rel}: got {got}/{len(data)}, "
                    f"want {want_sha1}/{want_size} -- refusing to place")
            dest = TARGET / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            results.append(check_file(dest, want_sha1, want_size))
        return results


def coverage() -> dict:
    path = TARGET / "data" / "dedr" / "dedr_new.csv"
    rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"))))
    params = {r[1] for r in rows}
    langs = {r[0] for r in rows}
    return {
        "dedr_new_rows": len(rows),
        "distinct_params": len(params),
        "distinct_language_tags": len(langs),
        "all_rows_9_columns": all(len(r) == 9 for r in rows),
    }


def consumer_checks() -> dict:
    sys.path.insert(0, str(REPO_ROOT / "backend"))
    sys.path.insert(0, str(REPO_ROOT / "backend" / "scripts"))
    import phase48_medium_validation_v2 as battery

    entries = battery.load_dedr(REPO_ROOT)
    out: dict = {"battery_v2_entries": None if entries is None else len(entries)}
    if entries is not None:
        probes = ["kalam", "nal", "kai", "tiru", "ko", "mutalai"]
        out["battery_v2_probes"] = {
            p: battery.test_dedr_v2(p, entries) for p in probes
        }
    from glossa_lab.data import cldf_loader

    out["cldf_summary"] = cldf_loader.get_cldf_summary(TARGET / "cldf")
    return out


def verify() -> dict:
    results = [
        check_file(TARGET / rel, want_sha1, want_size)
        for rel, (_up, want_sha1, want_size) in FILES.items()
        if (TARGET / rel).is_file()
    ]
    missing = [rel for rel in FILES if not (TARGET / rel).is_file()]
    record = {
        "pin": PIN,
        "upstream": UPSTREAM_URL,
        "swh_directory": SWH_DIRECTORY,
        "files_placed": len(results),
        "files_missing": missing,
        "all_hashes_ok": all(
            r["blob_sha1_ok"] and r["size_ok"] for r in results) and not missing,
        "dedr_new_sha256_ok": any(
            r["path"] == "data/dedr/dedr_new.csv"
            and r["sha256"] == DEDR_NEW_SHA256 for r in results),
        "files": results,
    }
    record.update(coverage())
    record.update(consumer_checks())
    return record


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="verify the placed tree and print a JSON record")
    args = ap.parse_args()
    if args.verify:
        print(json.dumps(verify(), indent=2, ensure_ascii=False))
        return
    results = restore()
    print(f"placed {len(results)} files at pin {PIN}; all hashes verified")


if __name__ == "__main__":
    main()
