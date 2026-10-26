"""Tests for the safe Spec 076 replay wrapper (repair WP6).

Covers: the hash gate tripping on a one-byte count-preserving change,
a missing-dependency refusal naming the item and its acquisition
route, refusal of an in-tree or already-existing output directory,
and archived files staying byte-unchanged after a failed replay.
A synthetic frozen runner stands in for the real one; the real frozen
runner is exercised by the acceptance run, not by unit tests.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from glossa_lab import replay076
from glossa_lab.replay076 import (
    AccessBlockerError,
    HashGateError,
    OutputDirError,
)

RUNNER = '''\
import json, pathlib
here = pathlib.Path(__file__).resolve().parent
data = json.loads((here / "inputs" / "data.json").read_text())
coding = json.loads((here / "strict-coding-output.json").read_text())
res = {"step0": {"records": data["records"], "tokens": data["tokens"]},
       "coding_entries": len(coding), "verdict": "TEST VERDICT"}
(here / "pilot-results.json").write_text(json.dumps(res))
print("synthetic runner ran")
'''

DATA = b'{"records": 3, "tokens": 5}'
CODING = b'[{"sign": "A", "coded_type": "FREE"}]'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build(tmp: Path):
    """A synthetic frozen tree + checkout + manifest. Returns paths."""
    frozen = tmp / "frozen"
    (frozen / "pilot").mkdir(parents=True)
    runner = frozen / "pilot" / "pilot_run.py"
    runner.write_text(RUNNER)
    archived = frozen / "pilot" / "pilot-results.json"
    archived.write_text('{"verdict": "ARCHIVED"}\n')
    checkout = tmp / "checkout"
    (checkout / "inputs").mkdir(parents=True)
    (checkout / "inputs" / "data.json").write_bytes(DATA)
    (checkout / "strict-coding-output.json").write_bytes(CODING)
    manifest = {
        "schema_version": "1.0",
        "wrapper_version": replay076.WRAPPER_VERSION,
        "frozen": {"tree_root": "frozen"},
        "historical_environment": {"python": "3.12.3"},
        "artifacts": [
            {"name": "pilot-runner", "role": "code",
             "path": "frozen/pilot/pilot_run.py",
             "sha256": sha(RUNNER.encode()),
             "hash_provenance": "code_hash_recorded_at_freeze",
             "acquisition": "frozen tree in this test"},
            {"name": "corpus-data", "role": "input",
             "path": "checkout/inputs/data.json",
             "sha256": sha(DATA),
             "hash_provenance": "prospective_frozen_input_hash",
             "staging_name": "inputs/data.json",
             "acquisition": "test checkout"},
            {"name": "strict-coding-output", "role": "coding_output",
             "path": "checkout/strict-coding-output.json",
             "sha256": sha(CODING),
             "hash_provenance": "coding_artifact_hash_recorded_after_coding",
             "staging_name": "strict-coding-output.json",
             "acquisition": "test checkout"},
        ],
        "census_expected": {
            "coding_output_entries": 1,
            "census_artifact_names": {"coding_output": "strict-coding-output"},
            "pilot_results": {"step0": {"records": 3, "tokens": 5},
                              "verdict": "TEST VERDICT"},
        },
    }
    mpath = tmp / "manifest.json"
    mpath.write_text(json.dumps(manifest, indent=1))
    return mpath, frozen, checkout


def tree_hashes(root: Path):
    return {str(p.relative_to(root)): sha(p.read_bytes())
            for p in sorted(root.rglob("*")) if p.is_file()}


# --- a clean synthetic replay works, and leaves the frozen tree alone --------

def test_synthetic_replay_reproduces_and_preserves(tmp_path):
    mpath, frozen, _ = build(tmp_path)
    before = tree_hashes(frozen)
    out = tmp_path / "out-new"
    record = replay076.replay(mpath, out)
    assert record["verdict"] == "TEST VERDICT"
    assert record["frozen_tree_unchanged"] is True
    assert tree_hashes(frozen) == before
    assert (out / "staging" / "pilot-results.json").is_file()
    # Historical environment: unrecorded fields are "unknown", the
    # replay environment is pinned separately.
    assert record["historical_environment"]["python"] == "3.12.3"
    assert record["historical_environment"]["platform"] == "unknown"
    assert record["replay_environment"]["python"]
    assert record["replay_environment"]["wrapper"]


# --- hash gate: a one-byte, count-preserving change fails ---------------------

def test_hash_gate_trips_on_one_byte_count_preserving_change(tmp_path):
    mpath, frozen, checkout = build(tmp_path)
    before = tree_hashes(frozen)
    target = checkout / "strict-coding-output.json"
    changed = CODING.replace(b'"A"', b'"B"')  # same length, same counts
    assert len(changed) == len(CODING) and changed != CODING
    assert len(json.loads(changed)) == len(json.loads(CODING))
    target.write_bytes(changed)
    with pytest.raises(HashGateError) as exc:
        replay076.replay(mpath, tmp_path / "out-new")
    assert "hash gate" in str(exc.value)
    assert "strict-coding-output" in str(exc.value)
    # Nothing ran: no output directory was created.
    assert not (tmp_path / "out-new").exists()
    assert tree_hashes(frozen) == before


# --- missing dependency: the refusal names the item and the route --------------

def test_missing_dependency_refusal_names_item_and_route(tmp_path):
    mpath, frozen, checkout = build(tmp_path)
    (checkout / "inputs" / "data.json").unlink()
    with pytest.raises(AccessBlockerError) as exc:
        replay076.replay(mpath, tmp_path / "out-new")
    msg = str(exc.value)
    assert "corpus-data" in msg
    assert "checkout/inputs/data.json" in msg
    assert "test checkout" in msg  # the documented acquisition route


# --- output directory gates -----------------------------------------------------

def test_existing_output_dir_refused(tmp_path):
    mpath, _, _ = build(tmp_path)
    out = tmp_path / "already-there"
    out.mkdir()
    with pytest.raises(OutputDirError):
        replay076.replay(mpath, out)


def test_in_tree_output_dir_refused(tmp_path):
    mpath, frozen, _ = build(tmp_path)
    with pytest.raises(OutputDirError) as exc:
        replay076.replay(mpath, frozen / "new-output")
    assert "inside the frozen artifact tree" in str(exc.value)
    assert not (frozen / "new-output").exists()


# --- a failed replay leaves every archived file byte-unchanged ------------------

def test_failed_replay_leaves_archived_files_unchanged(tmp_path):
    mpath, frozen, checkout = build(tmp_path)
    before = tree_hashes(frozen)
    # Fail at the hash gate.
    (checkout / "inputs" / "data.json").write_bytes(b'{"records": 3, "tokens": 6}')
    with pytest.raises(HashGateError):
        replay076.replay(mpath, tmp_path / "out-1")
    # Fail at the access gate.
    (checkout / "inputs" / "data.json").unlink()
    with pytest.raises(AccessBlockerError):
        replay076.replay(mpath, tmp_path / "out-2")
    assert tree_hashes(frozen) == before


# --- manifest without hash provenance is refused ---------------------------------

def test_manifest_must_distinguish_hash_provenance(tmp_path):
    mpath, _, _ = build(tmp_path)
    manifest = json.loads(mpath.read_text())
    del manifest["artifacts"][1]["hash_provenance"]
    mpath.write_text(json.dumps(manifest))
    with pytest.raises(replay076.ReplayError) as exc:
        replay076.replay(mpath, tmp_path / "out-new")
    assert "hash_provenance" in str(exc.value)
