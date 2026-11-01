"""Safe replay wrapper for the frozen Spec 076 pilot (repair WP6).

The frozen pilot runner (``pilot_run.py``) and its results are read
only. This wrapper never writes into the frozen tree. The runner reads
``inputs/`` beside itself and writes ``pilot-results.json`` beside
itself, so running it in place would overwrite the archived result.
The wrapper therefore:

1. Checks the output directory first: it must be new (not already
   existing) and outside the frozen artifact tree.
2. Verifies the SHA-256 hash of every manifest artifact BEFORE any
   computation on their contents. A one-byte change fails here, even
   if it preserves every count.
3. Resolves each input from a documented local path, or stops with a
   precise access blocker naming the missing item and its documented
   acquisition route.
4. Runs census pre-checks (counts stated in the frozen spec) in
   addition to the hash checks.
5. Copies the runner byte-for-byte into a staging area inside the new
   output directory (the copy's hash is verified against the frozen
   original), stages verified copies of the inputs there, and runs
   the copy. The frozen original is never executed in place and never
   written to.
6. Compares the produced results against the manifest census
   (population counts and the archived outcome), and refuses -- a
   named census-mismatch failure -- if they differ.
7. Re-hashes the frozen tree afterwards and proves it is unchanged.

Hash provenance matters. A manifest must say, for each artifact,
whether its hash was a prospective frozen input hash (pinned before
the run, in ``freeze.json``) or a coding-artifact hash recorded after
coding, or another named timing. The wrapper refuses a manifest entry
with no hash-provenance field, because presenting all hashes as if
they were frozen at the same time would be false.

Historical environment values that are not recorded are stored as the
string ``"unknown"``. The replay environment (Python version,
platform, timestamp, wrapper version) is pinned separately in the
replay record, at run time.

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

WRAPPER_VERSION = "1.0.0"

HISTORICAL_ENV_KEYS = ("python", "platform", "runner", "aee", "specify", "os")


class ReplayError(Exception):
    """Base class for named replay refusals."""


class OutputDirError(ReplayError):
    """The output directory is not new, or is inside the frozen tree."""


class HashGateError(ReplayError):
    """A hash check failed before any computation."""


class AccessBlockerError(ReplayError):
    """A required input cannot be resolved from a documented path."""


class CensusMismatchError(ReplayError):
    """A census check does not match the frozen spec's stated counts."""


class FrozenTreeChangedError(ReplayError):
    """The frozen tree changed during the replay (must never happen)."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_tree(root: Path) -> dict[str, str]:
    """Relative path -> SHA-256 for every file under ``root``."""
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = sha256_file(p)
    return out


def normalize_historical_environment(env: Optional[dict]) -> dict[str, str]:
    """Fill unrecorded historical environment values with "unknown"."""
    env = env or {}
    return {k: (str(env[k]) if env.get(k) not in (None, "") else "unknown")
            for k in HISTORICAL_ENV_KEYS}


def replay_environment() -> dict[str, str]:
    """The replay environment, pinned at run time, kept separate from
    the historical environment."""
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "wrapper": f"replay076 {WRAPPER_VERSION}",
    }


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise AccessBlockerError(
            f"access blocker: manifest not found: {manifest_path}") from e
    except json.JSONDecodeError as e:
        raise ReplayError(f"manifest is not valid JSON: {manifest_path}: {e}") from e
    if manifest.get("schema_version") != "1.0":
        raise ReplayError(
            f"unsupported manifest schema_version: {manifest.get('schema_version')!r}")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ReplayError("manifest must list at least one artifact")
    for art in artifacts:
        if not art.get("sha256"):
            raise ReplayError(
                f"manifest artifact {art.get('name')!r} has no sha256")
        if not art.get("hash_provenance"):
            raise ReplayError(
                f"manifest artifact {art.get('name')!r} has no "
                "hash_provenance field; the manifest must distinguish a "
                "prospective frozen input hash from a coding-artifact "
                "hash recorded after coding, and must not imply all "
                "hashes were frozen at the same time")
    return manifest


def resolve_artifact(
    art: dict[str, Any],
    manifest_dir: Path,
    search_roots: Iterable[Path],
) -> Optional[Path]:
    """Resolve one artifact from its documented local paths.

    Candidates, in order: the artifact's ``path`` as written (if
    absolute), relative to the manifest directory, relative to each
    search root; then the artifact's ``repo_path`` relative to each
    search root and to the manifest directory.
    """
    candidates: list[Path] = []
    for key in ("path", "repo_path"):
        raw = art.get(key)
        if not raw:
            continue
        p = Path(raw)
        if p.is_absolute():
            candidates.append(p)
        else:
            candidates.append(manifest_dir / p)
            for root in search_roots:
                candidates.append(Path(root) / p)
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def _blocker_message(art: dict[str, Any]) -> str:
    route = art.get("acquisition") or "no acquisition route documented in the manifest"
    return (
        f"access blocker: required item {art.get('name')!r} is missing. "
        f"Documented local path: {art.get('path')!r}"
        + (f"; repository path: {art.get('repo_path')!r}" if art.get("repo_path") else "")
        + f". Lawful acquisition route as documented: {route}. "
        "The replay refuses to run without it; nothing was computed."
    )


def verify_hashes(
    manifest: dict[str, Any],
    manifest_dir: Path,
    search_roots: Iterable[Path],
) -> dict[str, Path]:
    """Verify every artifact hash before any computation.

    Returns name -> resolved path. Raises AccessBlockerError for a
    missing required item and HashGateError for any mismatch. This
    function reads bytes only to hash them; it parses nothing.
    """
    roots = list(search_roots)
    resolved: dict[str, Path] = {}
    for art in manifest["artifacts"]:
        found = resolve_artifact(art, manifest_dir, roots)
        if found is None:
            if art.get("required", True):
                raise AccessBlockerError(_blocker_message(art))
            continue
        actual = sha256_file(found)
        if actual != str(art["sha256"]).lower():
            raise HashGateError(
                f"hash gate: artifact {art.get('name')!r} at {found} has "
                f"SHA-256 {actual}, manifest expects {art['sha256']}. "
                "Refusing before any computation; a change of even one "
                "byte fails here, including a change that preserves "
                "every count.")
        resolved[art["name"]] = found
    return resolved


def census_prechecks(
    manifest: dict[str, Any],
    resolved: dict[str, Path],
) -> dict[str, Any]:
    """Count checks on the verified inputs, from the manifest census.

    Supported manifest ``census_expected`` keys (each optional, each
    checked only when present):
    ``coding_input_entries``, ``coding_output_entries`` (JSON list
    lengths), ``anchors_entries``, ``anchors_strict``,
    ``anchors_pending`` (from an anchors JSON artifact named by
    ``census_artifact_names``, defaulting to the conventional names).
    """
    expected = manifest.get("census_expected") or {}
    names = expected.get("census_artifact_names") or {}
    observed: dict[str, Any] = {}

    def _load(name_key: str, default: str) -> Optional[Any]:
        nm = names.get(name_key, default)
        path = resolved.get(nm)
        return json.loads(path.read_text(encoding="utf-8")) if path else None

    checks = {
        "coding_input_entries": ("coding_input", "strict-coding-input"),
        "coding_output_entries": ("coding_output", "strict-coding-output"),
    }
    for key, (name_key, default) in checks.items():
        if key in expected:
            data = _load(name_key, default)
            if data is None:
                raise CensusMismatchError(
                    f"census check {key}: artifact for this check is not "
                    "among the resolved manifest artifacts")
            observed[key] = len(data)
    if any(k in expected for k in
           ("anchors_entries", "anchors_strict", "anchors_pending")):
        data = _load("anchors", "anchors")
        if data is None:
            raise CensusMismatchError(
                "census check anchors_*: anchors artifact is not among "
                "the resolved manifest artifacts")
        anchors = data.get("anchors", data)
        observed["anchors_entries"] = len(anchors)
        observed["anchors_strict"] = sum(
            1 for v in anchors.values()
            if isinstance(v, dict)
            and v.get("validation_status") == "strict_sa_independent")
        observed["anchors_pending"] = sum(
            1 for v in anchors.values()
            if isinstance(v, dict)
            and v.get("validation_status") == "pending_non_sa_validation")
    for key, want in expected.items():
        if key == "census_artifact_names" or key not in observed:
            continue
        if observed[key] != want:
            raise CensusMismatchError(
                f"census mismatch on {key}: observed {observed[key]}, "
                f"frozen spec states {want}. Refusing to run.")
    return observed


def _subset_match(expected: Any, actual: Any, path: str = "") -> Optional[str]:
    """Return a description of the first mismatch, or None."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return f"{path or '.'}: expected an object"
        for k, v in expected.items():
            if k not in actual:
                return f"{path}.{k}: missing in produced results"
            r = _subset_match(v, actual[k], f"{path}.{k}")
            if r:
                return r
        return None
    if expected != actual:
        return f"{path}: expected {expected!r}, produced {actual!r}"
    return None


def check_output_census(
    manifest: dict[str, Any],
    produced: dict[str, Any],
) -> None:
    """Compare produced pilot results with the manifest census.

    ``census_expected.pilot_results`` is a nested subset (for example
    step0 counts, step1 slot totals, the exclusion count, and the
    verdict) that the produced results must match exactly.
    """
    expected = (manifest.get("census_expected") or {}).get("pilot_results")
    if not expected:
        return
    problem = _subset_match(expected, produced)
    if problem:
        raise CensusMismatchError(
            f"census mismatch in produced results at {problem}. "
            "The replay does not reproduce the archived census/outcome.")


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def replay(
    manifest_path: Path,
    output_dir: Path,
    search_roots: Iterable[Path] = (),
    timeout: int = 3600,
) -> dict[str, Any]:
    """Run a safe replay. Returns the replay record.

    Raises a ReplayError subclass (a named gate) on any refusal. On a
    gate failure before staging, the output directory is not created.
    """
    manifest_path = Path(manifest_path)
    output_dir = Path(output_dir)
    manifest = load_manifest(manifest_path)
    manifest_dir = manifest_path.resolve().parent

    frozen_spec = manifest.get("frozen") or {}
    frozen_tree_raw = frozen_spec.get("tree_root")
    frozen_tree = (manifest_dir / frozen_tree_raw).resolve() \
        if frozen_tree_raw else None

    # (d) Output directory gate -- first, before anything is written.
    if output_dir.exists():
        raise OutputDirError(
            f"output directory refusal: {output_dir} already exists. "
            "A replay requires a new output directory, so that no "
            "earlier result can be overwritten or confused with this run.")
    if frozen_tree is not None and _is_within(output_dir, frozen_tree):
        raise OutputDirError(
            f"output directory refusal: {output_dir} is inside the "
            f"frozen artifact tree {frozen_tree}. Replay output must "
            "live outside the frozen tree.")

    # Frozen-tree snapshot, before.
    before = hash_tree(frozen_tree) if frozen_tree and frozen_tree.is_dir() else {}

    # (b) Hash gate -- before any computation.
    resolved = verify_hashes(manifest, manifest_dir, search_roots)

    # (e) Census pre-checks, in addition to hash checks.
    precheck = census_prechecks(manifest, resolved)

    # Stage into the new output directory.
    output_dir.mkdir(parents=True)
    staging = output_dir / "staging"
    staging.mkdir()
    runner_art = next(
        (a for a in manifest["artifacts"] if a.get("role") == "code"),
        None)
    if runner_art is None:
        raise ReplayError("manifest lists no artifact with role 'code' "
                          "(the frozen runner)")
    runner_src = resolved[runner_art["name"]]
    staged_runner = staging / Path(runner_src.name)
    shutil.copyfile(runner_src, staged_runner)
    if sha256_file(staged_runner) != sha256_file(runner_src):
        raise ReplayError("staged runner copy does not match the frozen "
                          "runner's hash; refusing to run an unverified copy")
    for art in manifest["artifacts"]:
        staging_name = art.get("staging_name")
        if not staging_name or art["name"] not in resolved:
            continue
        dest = staging / staging_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(resolved[art["name"]], dest)
        if sha256_file(dest) != str(art["sha256"]).lower():
            raise ReplayError(
                f"staged copy of {art['name']!r} does not match its "
                "manifest hash; refusing to run")

    # Run the staged copy. The frozen runner is never run in place.
    proc = subprocess.run(
        [sys.executable, str(staged_runner)],
        cwd=str(staging), capture_output=True, text=True, timeout=timeout)
    produced_path = staging / "pilot-results.json"
    produced = None
    if produced_path.is_file():
        produced = json.loads(produced_path.read_text(encoding="utf-8"))

    record: dict[str, Any] = {
        "wrapper_version": WRAPPER_VERSION,
        "manifest": str(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "historical_environment": normalize_historical_environment(
            manifest.get("historical_environment")),
        "replay_environment": replay_environment(),
        "census_prechecks": precheck,
        "runner_exit_code": proc.returncode,
        "runner_stdout_tail": proc.stdout[-2000:],
        "runner_stderr_tail": proc.stderr[-2000:],
        "produced_results": str(produced_path) if produced else None,
        "verdict": None,
    }
    if produced is not None:
        record["verdict"] = produced.get("verdict")
        # (e) Post-run census: refuse (named failure) on mismatch.
        check_output_census(manifest, produced)
    elif proc.returncode != 0:
        raise ReplayError(
            f"runner failed with exit code {proc.returncode} and "
            f"produced no results. stderr tail: {proc.stderr[-500:]}")

    # (f) Prove the frozen tree is unchanged.
    after = hash_tree(frozen_tree) if frozen_tree and frozen_tree.is_dir() else {}
    record["frozen_tree_files"] = len(before)
    record["frozen_tree_unchanged"] = (before == after)
    if before != after:
        raise FrozenTreeChangedError(
            "the frozen tree changed during the replay; this is an "
            "integrity failure and the replay record must not be trusted")
    (output_dir / "replay-record.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Safe replay of the frozen Spec 076 pilot.")
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--search-root", action="append", type=Path, default=[],
                    help="extra root for resolving documented local paths "
                         "(may be repeated)")
    args = ap.parse_args(argv)
    try:
        record = replay(args.manifest, args.output_dir, args.search_root)
    except AccessBlockerError as e:
        print(f"REFUSED (access blocker): {e}", file=sys.stderr)
        return 3
    except HashGateError as e:
        print(f"REFUSED (hash gate): {e}", file=sys.stderr)
        return 2
    except OutputDirError as e:
        print(f"REFUSED (output directory): {e}", file=sys.stderr)
        return 4
    except CensusMismatchError as e:
        print(f"REFUSED (census mismatch): {e}", file=sys.stderr)
        return 5
    except ReplayError as e:
        print(f"REFUSED (replay): {e}", file=sys.stderr)
        return 6
    print(json.dumps(record, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
