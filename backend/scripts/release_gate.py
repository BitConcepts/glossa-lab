"""RELEASE GATE: hash-verify a staged deposit against its repo sources.

Owner-ordered after the release-integrity audit of Zenodo v4.2.0
(``reports/release_integrity_audit_v420.md``): the v4.2.0 deposit's
``INDUS_FINAL_ANCHORS.json`` (sha256 841e9067…) matched no committed
repo version — its parsed content was the 2026-05-27 anchors state
with CRLF line endings, deposited on 2026-10-07, more than a day
after the repo file had become sha256 eccea6d5… (Phase-110 Part B,
2026-10-06). This gate exists so that class of staging error fails
loudly *before* a deposit is made, not in an audit after it.

Usage::

    python backend/scripts/release_gate.py \
        --manifest path/to/release_manifest.json \
        --staging-dir path/to/staging_dir \
        [--repo-root path/to/repo] [--json-out gate_output.json]

Manifest (JSON; YAML also accepted when PyYAML is installed) — a list
form or a mapping form are both accepted::

    {"files": [
      {"deposit_name": "INDUS_FINAL_ANCHORS.json",
       "source": "backend/reports/INDUS_FINAL_ANCHORS.json"},
      {"deposit_name": "supplementary_note.md",
       "external_source": "Authored outside the repo; reviewed in PR #NN"}
    ]}

    {"INDUS_FINAL_ANCHORS.json": "backend/reports/INDUS_FINAL_ANCHORS.json",
     "supplementary_note.md": {"external_source": "Authored outside the repo"}}

Semantics per entry:

- ``source`` entry: the staged file and the named repo source are
  both sha256-hashed (raw bytes, no normalisation — line-ending
  drift is exactly what this gate must catch). Status MATCH or
  MISMATCH.
- ``external_source`` entry: no repo source exists by definition.
  The staged file must exist; its sha256 is printed for the release
  record and the status is EXTERNAL (not a failure). A *missing*
  staged external file is a failure.
- A missing staged file or a missing repo source is a failure in
  all cases.

Exit codes: 0 = every entry MATCH or EXTERNAL-present; 1 = at least
one MISMATCH / MISSING-STAGED / MISSING-SOURCE; 2 = manifest or
usage error. The tool is fully offline and stdlib-only (PyYAML is
used only if a YAML manifest is supplied and it is installed).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

CHUNK = 1024 * 1024  # bounded, chunked hashing (H11: no unbounded I/O)


def sha256_file(path: Path) -> str:
    """Return the sha256 hex digest of *path*'s raw bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_manifest(manifest_path: Path) -> list[dict]:
    """Load a manifest and normalise it to a list of entry dicts.

    Each returned entry has ``deposit_name`` plus exactly one of
    ``source`` / ``external_source``. Raises ``ValueError`` on any
    malformed input (the caller maps that to exit code 2).
    """
    text = manifest_path.read_text(encoding="utf-8")
    suffix = manifest_path.suffix.lower()
    if suffix in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ValueError(
                "YAML manifest supplied but PyYAML is not installed; "
                "use a JSON manifest instead"
            ) from exc
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    raw_entries: list[dict] = []
    if isinstance(data, dict) and "files" in data:
        raw_entries = data["files"]
    elif isinstance(data, dict):
        # Mapping form: {deposit_name: source | {source/external_source: ...}}
        for name, value in data.items():
            if isinstance(value, str):
                raw_entries.append({"deposit_name": name, "source": value})
            elif isinstance(value, dict):
                raw_entries.append({"deposit_name": name, **value})
            else:
                raise ValueError(f"manifest entry for {name!r} is not a string or object")
    elif isinstance(data, list):
        raw_entries = data
    else:
        raise ValueError("manifest must be an object with a 'files' list, "
                         "a name->source mapping, or a list of entries")

    entries: list[dict] = []
    for i, raw in enumerate(raw_entries):
        if not isinstance(raw, dict) or not raw.get("deposit_name"):
            raise ValueError(f"manifest entry #{i} lacks a 'deposit_name'")
        has_source = bool(raw.get("source"))
        has_external = bool(raw.get("external_source"))
        if has_source == has_external:
            raise ValueError(
                f"manifest entry {raw['deposit_name']!r} must set exactly one "
                "of 'source' or 'external_source'"
            )
        entries.append({
            "deposit_name": str(raw["deposit_name"]),
            "source": str(raw["source"]) if has_source else None,
            "external_source": str(raw["external_source"]) if has_external else None,
        })
    if not entries:
        raise ValueError("manifest contains no entries")
    return entries


def check_entry(entry: dict, staging_dir: Path, repo_root: Path) -> dict:
    """Check one manifest entry; return a result dict (never raises
    for missing files — missing is a reported status, not a crash)."""
    staged = staging_dir / entry["deposit_name"]
    result: dict = {
        "deposit_name": entry["deposit_name"],
        "source": entry["source"],
        "external_source": entry["external_source"],
        "staged_sha256": None,
        "source_sha256": None,
        "status": "",
    }
    if not staged.is_file():
        result["status"] = "MISSING-STAGED"
        return result
    result["staged_sha256"] = sha256_file(staged)

    if entry["external_source"]:
        result["status"] = "EXTERNAL"
        return result

    source_path = Path(entry["source"])
    if not source_path.is_absolute():
        source_path = repo_root / source_path
    if not source_path.is_file():
        result["status"] = "MISSING-SOURCE"
        return result
    result["source_sha256"] = sha256_file(source_path)
    result["status"] = (
        "MATCH" if result["staged_sha256"] == result["source_sha256"] else "MISMATCH"
    )
    return result


def run_gate(manifest_path: Path, staging_dir: Path, repo_root: Path) -> tuple[list[dict], int]:
    """Run the gate; return (results, exit_code)."""
    entries = load_manifest(manifest_path)
    results = [check_entry(e, staging_dir, repo_root) for e in entries]
    failed = any(r["status"] in ("MISMATCH", "MISSING-STAGED", "MISSING-SOURCE")
                 for r in results)
    return results, (1 if failed else 0)


def format_table(results: list[dict]) -> str:
    """Render the per-file MATCH/MISMATCH table printed at release time."""
    lines = [
        f"{'FILE':<44} {'STATUS':<15} {'STAGED sha256':<16} {'SOURCE sha256'}",
        "-" * 110,
    ]
    for r in results:
        staged = (r["staged_sha256"] or "—")[:12] + "…" if r["staged_sha256"] else "—"
        if r["external_source"]:
            source = f"(external: {r['external_source']})"
        elif r["source_sha256"]:
            source = r["source_sha256"][:12] + "…"
        else:
            source = "—"
        lines.append(f"{r['deposit_name']:<44} {r['status']:<15} {staged:<16} {source}")
    n_fail = sum(1 for r in results
                 if r["status"] in ("MISMATCH", "MISSING-STAGED", "MISSING-SOURCE"))
    lines.append("-" * 110)
    lines.append(
        f"RELEASE GATE: {'FAIL' if n_fail else 'PASS'} — "
        f"{len(results) - n_fail}/{len(results)} entries OK, {n_fail} failed"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--staging-dir", required=True, type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(),
                        help="Base for relative manifest 'source' paths "
                             "(default: current working directory)")
    parser.add_argument("--json-out", type=Path, default=None,
                        help="Also write the full gate output (hashes + "
                             "statuses) as JSON, for the release record")
    args = parser.parse_args(argv)

    if not args.manifest.is_file():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        return 2
    if not args.staging_dir.is_dir():
        print(f"ERROR: staging directory not found: {args.staging_dir}", file=sys.stderr)
        return 2
    try:
        results, exit_code = run_gate(args.manifest, args.staging_dir, args.repo_root)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid manifest: {exc}", file=sys.stderr)
        return 2

    print(format_table(results))
    if args.json_out:
        payload = {
            "manifest": str(args.manifest),
            "staging_dir": str(args.staging_dir),
            "repo_root": str(args.repo_root),
            "verdict": "FAIL" if exit_code else "PASS",
            "results": results,
        }
        args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Gate output written to {args.json_out}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
