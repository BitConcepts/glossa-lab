#!/usr/bin/env python3
"""Bundle import — Spec 086 intake route 2 (T103).

Imports one spec's claims bundle (``claims.json`` /
``aee-claims.json``) into the ledger, for use at freeze /
adjudication events. Propositions already canonical in the
ledger (from any spec) are reported, not duplicated (D-B:
merge, never delete); new propositions are appended through
the intake validator.

Usage (from the repo root):

    python3 tools/ledger/import_bundle.py --spec specs/<spec-dir>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.ledger_intake import (  # noqa: E402
    append_entry,
    build_bundle_entries,
)
from glossa_lab.proposition_fingerprint import (  # noqa: E402
    DuplicatePropositionError,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--date", required=True, help="intake date (YYYY-MM-DD)")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    root = args.root.resolve()
    spec_dir = (root / args.spec).resolve()
    groups = build_bundle_entries(root, [spec_dir], date=args.date)
    appended = already = 0
    for group in groups:
        try:
            append_entry(root, group.entry)
            appended += 1
            print(f"appended: {group.entry['id']}")
        except DuplicatePropositionError as exc:
            already += 1
            print(
                f"already canonical: {group.entry['id']} — proposition "
                f"already in the ledger as {exc.existing_claim_id!r} "
                "(D-B; source preserved in the bundle, not duplicated)"
            )
    print(
        f"bundle import for {args.spec}: {appended} appended, "
        f"{already} already canonical, {len(groups)} propositions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
