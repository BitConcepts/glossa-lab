"""Spec 089 Stage 1 — the run-record library teeth (T103)
and the legacy dry-run over the standing store (T104).

T103's acceptance: the formats and the fold of
`glossa_lab.run_records` (the machine copy of run-defs v2)
are proven against the registered rules — 10,000
same-second mints unique and format-conformant; header
validation refuses a missing key component per surface and
an absence block with an unregistered kind; the index fold
applies supersede / quarantine / adjudicate sequences in
act order and refuses an act naming an unknown run id;
legacy derivation is stable and collision-free over
generated store paths.

T104's acceptance: on a tmp copy of the standing settling
runs store, the fold enumerates exactly the records that
stand there, under legacy ids, with the recoverable key
components (semantics, candidate, pins) and the
`legacy — key partial` label. The enumeration is
recomputed from the store at test time — no count in this
file is asserted from the plan's numbers — and the real
store's bytes are verified unchanged by the dry run.

*This does not establish:* behaviour of any surface's
write path — adoption is Stages 2–4; this module proves
the formats, the fold, and the legacy derivation only.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from glossa_lab import run_records as rr

ROOT = Path(__file__).resolve().parents[2]
RUNS_STORE = ROOT / "glossa-indus" / "ledger" / "runs"

NOW = datetime(2026, 11, 4, 7, 39, 0, tzinfo=timezone.utc)
ID_RE = re.compile(r"^[a-z]+-\d{8}T\d{6}Z-[0-9a-f]{6}$")


def _key(surface: str = "settling", **overrides) -> dict:
    key = {
        "surface": surface,
        "command": "run_settling.py run --scenario t405-fixture",
        "tool_version": "1.0",
        "input_pins": {"ledger": {"sha256": "a" * 64, "lines": 1}},
        "seed": rr.NO_SEED,
        "code_version": "b" * 40,
        "environment_class": "ci/linux",
    }
    key.update(overrides)
    return key


def _header(surface: str = "settling", **overrides) -> dict:
    kwargs = {
        "surface": surface,
        "tool": "run_settling.py",
        "tool_version": "1.0",
        "command": "run_settling.py run --scenario t405-fixture",
        "code_version": "b" * 40,
        "input_pins": {"ledger": {"sha256": "a" * 64, "lines": 1}},
        "seed": rr.NO_SEED,
        "environment_class": "ci/linux",
        "started": NOW,
        "finished": NOW,
    }
    if surface == "experiment":
        kwargs["determinism_class"] = "named-nondeterministic"
    kwargs.update(overrides)
    return rr.build_header(**kwargs)


def _entry(run_id: str, surface: str = "settling") -> dict:
    return {
        "act": "entry",
        "run_id": run_id,
        "record": f"{run_id}.json",
        "key": _key(surface),
    }


def _minted_entry(surface: str = "settling") -> dict:
    return _entry(rr.mint_run_id(surface, now=NOW), surface)


# ---------------------------------------------------------------------------
# Minting (T103): format, uniqueness, redraw


def test_mint_format_for_every_surface():
    for surface in rr.SURFACES:
        run_id = rr.mint_run_id(surface, now=NOW)
        assert ID_RE.match(run_id)
        assert run_id.startswith(f"{surface}-20261104T073900Z-")
        assert rr.parse_run_id(run_id)["surface"] == surface


def test_mint_refuses_unregistered_surface():
    with pytest.raises(rr.RunRecordError):
        rr.mint_run_id("wizard", now=NOW)


def test_ten_thousand_same_second_mints_are_unique():
    ids = {rr.mint_run_id("settling", now=NOW) for _ in range(10_000)}
    assert len(ids) == 10_000
    assert all(ID_RE.match(run_id) for run_id in ids)


def test_minter_redraws_on_collision():
    draws = iter(["aaaaaa", "aaaaaa", "bbbbbb"])
    minter = rr._Minter(rand_hex=lambda: next(draws))
    first = rr.mint_run_id("settling", now=NOW, minter=minter)
    second = rr.mint_run_id("settling", now=NOW, minter=minter)
    assert first.endswith("-aaaaaa")
    assert second.endswith("-bbbbbb")


def test_minter_refuses_malformed_random():
    minter = rr._Minter(rand_hex=lambda: "ZZZZZZ")
    with pytest.raises(rr.RunRecordError):
        rr.mint_run_id("settling", now=NOW, minter=minter)


def test_parse_run_id_refusals():
    for bad in (
        "settling-20261104T073900Z-ABCDEF",  # uppercase hex
        "settling-20261104T073900-abcdef",  # stamp missing Z
        "settling--d9f73e4c4e4e",  # content-addressed shape
        "legacy:t405-incumbent",  # a legacy id is not a run id
        "wizard-20261104T073900Z-abcdef",  # unregistered surface
        42,
    ):
        with pytest.raises(rr.RunRecordError):
            rr.parse_run_id(bad)


# ---------------------------------------------------------------------------
# Header + key validation (T103)


@pytest.mark.parametrize("surface", sorted(rr.SURFACES))
@pytest.mark.parametrize("component", rr.KEY_COMPONENTS)
def test_header_validation_refuses_missing_key_component_per_surface(
    surface: str, component: str
):
    header = _header(surface)
    header["key"] = {
        name: value
        for name, value in header["key"].items()
        if name != component
    }
    with pytest.raises(rr.RunRecordError):
        rr.validate_header(header)


@pytest.mark.parametrize("kind", rr.ABSENCE_KINDS)
def test_absence_block_registered_kinds_build(kind: str):
    record = rr.build_record(
        _header(), absence={"kind": kind, "detail": "nothing produced"}
    )
    assert rr.validate_record(record) is record


def test_absence_block_unregistered_kind_refused():
    with pytest.raises(rr.RunRecordError):
        rr.build_record(
            _header(), absence={"kind": "vanished", "detail": "gone"}
        )
    with pytest.raises(rr.RunRecordError):
        rr.build_record(_header(), absence={"kind": "empty", "detail": ""})


def test_record_carries_exactly_one_outcome():
    header = _header()
    with pytest.raises(rr.RunRecordError):
        rr.build_record(
            header,
            result={"x": 1},
            absence={"kind": "empty", "detail": "none"},
        )
    with pytest.raises(rr.RunRecordError):
        rr.build_record(header)
    record = rr.build_record(header, result={"x": 1})
    assert rr.validate_record(record) is record


def test_header_stamp_rules():
    header = _header()
    # The minted id carries the execution start's stamp.
    assert header["run_id"].startswith("settling-20261104T073900Z-")
    assert header["started"] == "2026-11-04T07:39:00Z"
    with pytest.raises(rr.RunRecordError):
        _header(finished=datetime(2026, 11, 4, 7, 38, 0,
                                   tzinfo=timezone.utc))
    with pytest.raises(rr.RunRecordError):
        _header(started="04/11/2026 07:39")


def test_header_determinism_registration():
    # Fixed-class surfaces refuse a foreign class.
    with pytest.raises(rr.RunRecordError):
        _header("settling", determinism_class="named-nondeterministic")
    assert _header("suite")["determinism_class"] == "named-nondeterministic"
    assert _header("settling")["determinism_class"] == "deterministic"
    # The per-graph surface must state its class explicitly.
    kwargs = {
        "surface": "experiment",
        "tool": "backend",
        "tool_version": "1.0",
        "command": "create_job",
        "code_version": "b" * 40,
        "input_pins": {"graph": "g"},
        "seed": rr.NO_SEED,
        "environment_class": "desktop/windows",
        "started": NOW,
    }
    with pytest.raises(rr.RunRecordError):
        rr.build_header(**kwargs)
    header = rr.build_header(determinism_class="deterministic", **kwargs)
    assert header["determinism_class"] == "deterministic"


def test_seed_marker_rule():
    with pytest.raises(rr.RunRecordError):
        rr.build_key(
            surface="settling",
            command="run",
            tool_version="1.0",
            input_pins={},
            seed=None,
            code_version="b" * 40,
            environment_class="ci/linux",
        )
    assert _key()["seed"] == rr.NO_SEED


def test_comparability_is_decided_by_the_key():
    base = _key()
    assert rr.keys_comparable(base, _key(code_version="c" * 40))
    assert rr.keys_comparable(base, _key(environment_class="vm/linux"))
    pin_diff = _key(input_pins={"ledger": {"sha256": "d" * 64, "lines": 2}})
    assert not rr.keys_comparable(base, pin_diff)
    assert rr.constitutive_diff(base, pin_diff) == ["input_pins"]
    assert rr.constitutive_diff(base, _key(seed="42")) == ["seed"]


# ---------------------------------------------------------------------------
# The index fold (T103)


def test_fold_applies_supersede_quarantine_adjudicate_in_order():
    a, b, c = _minted_entry(), _minted_entry(), _minted_entry()
    junction = rr.mint_junction_id(now=NOW)
    acts = [
        a,
        b,
        c,
        {
            "act": "supersedes",
            "run_id": b["run_id"],
            "supersedes": a["run_id"],
            "ref": "stage record (fixture)",
        },
        {
            "act": "quarantine",
            "junction_id": junction,
            "run_ids": [b["run_id"], c["run_id"]],
        },
    ]
    state = rr.fold_acts(acts)
    assert state.census == 3
    assert state.superseded_by == {a["run_id"]: b["run_id"]}
    assert state.open_quarantine == {
        b["run_id"]: {junction},
        c["run_id"]: {junction},
    }
    lifted = rr.fold_acts(
        acts
        + [
            {
                "act": "adjudication",
                "junction_id": junction,
                "ruling": "explained by the named pin change",
                "actor": "stage reviewer (fixture)",
                "resulting_state": "quarantine-lifted",
            }
        ]
    )
    assert lifted.open_quarantine == {}


def test_fold_confirmed_quarantine_stays_open():
    a, b = _minted_entry(), _minted_entry()
    junction = rr.mint_junction_id(now=NOW)
    state = rr.fold_acts(
        [
            a,
            b,
            {
                "act": "quarantine",
                "junction_id": junction,
                "run_ids": [a["run_id"], b["run_id"]],
            },
            {
                "act": "adjudication",
                "junction_id": junction,
                "ruling": "divergence unexplained on re-examination",
                "actor": "stage reviewer (fixture)",
                "resulting_state": "quarantine-confirmed",
            },
        ]
    )
    assert state.open_quarantine == {
        a["run_id"]: {junction},
        b["run_id"]: {junction},
    }


def test_fold_refuses_acts_naming_unknown_ids():
    a = _minted_entry()
    unknown = rr.mint_run_id("settling", now=NOW)
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts(
            [
                a,
                {
                    "act": "supersedes",
                    "run_id": a["run_id"],
                    "supersedes": unknown,
                    "ref": "fixture",
                },
            ]
        )
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts(
            [
                a,
                {
                    "act": "quarantine",
                    "junction_id": rr.mint_junction_id(now=NOW),
                    "run_ids": [unknown],
                },
            ]
        )
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts(
            [
                a,
                {
                    "act": "adjudication",
                    "junction_id": rr.mint_junction_id(now=NOW),
                    "ruling": "no such junction",
                    "actor": "fixture",
                    "resulting_state": "quarantine-lifted",
                },
            ]
        )


def test_fold_refuses_duplicate_entry_and_double_supersession():
    a, b, c = _minted_entry(), _minted_entry(), _minted_entry()
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts([a, a])
    supersede = {
        "act": "supersedes",
        "run_id": b["run_id"],
        "supersedes": a["run_id"],
        "ref": "fixture",
    }
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts(
            [
                a,
                b,
                c,
                supersede,
                {
                    "act": "supersedes",
                    "run_id": c["run_id"],
                    "supersedes": a["run_id"],
                    "ref": "fixture",
                },
            ]
        )
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts([a, {"act": "explode", "run_id": a["run_id"]}])


def _departure(run_id: str, record: str, **overrides) -> dict:
    act = {
        "act": "departure",
        "run_id": run_id,
        "record": record,
        "superseded_by_commit": "c" * 40,
        "git_blob": "d" * 40,
        "blob_sha256": "e" * 64,
        "ref": "fixture (departed-generation accounting)",
    }
    act.update(overrides)
    return act


def test_fold_applies_a_departure_act_without_touching_the_entry():
    entry = _minted_entry()
    departure = _departure(entry["run_id"], entry["record"])
    state = rr.fold_acts([entry, departure])
    assert state.departed == {entry["run_id"]: departure}
    # The accounting is the appended act; the entry stands
    # byte-for-byte as entered (append-only preserved).
    assert state.entries[entry["run_id"]] == entry
    assert "superseded_by_commit" not in state.entries[entry["run_id"]]


def test_fold_accounts_a_legacy_generation_that_entered_standing():
    record = {
        "semantics": "glossa-settle-1",
        "candidate": "incumbent",
        "pins": {"ledger": {"sha256": "a" * 64}},
    }
    name = "t405-incumbent-over-full-frame--d9f73e4c4e4e.json"
    entry = rr.legacy_entry_for_record(name, record)
    assert "superseded_by_commit" not in entry
    departure = rr.departure_act(
        entry["run_id"],
        name,
        superseded_by_commit="c" * 40,
        git_blob="d" * 40,
        blob_sha256="e" * 64,
        ref="fixture",
    )
    state = rr.fold_acts([entry, departure])
    assert state.departed[entry["run_id"]]["blob_sha256"] == "e" * 64
    assert state.entries[entry["run_id"]] == entry


def test_fold_refuses_departure_acts_that_do_not_account():
    entry = _minted_entry()
    unknown = rr.mint_run_id("settling", now=NOW)
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts([entry, _departure(unknown, f"{unknown}.json")])
    with pytest.raises(rr.RunRecordError):
        # The named record must be the entry's own record.
        rr.fold_acts(
            [entry, _departure(entry["run_id"], "some-other.json")]
        )
    with pytest.raises(rr.RunRecordError):
        # A generation's departure is accounted once.
        rr.fold_acts(
            [
                entry,
                _departure(entry["run_id"], entry["record"]),
                _departure(entry["run_id"], entry["record"]),
            ]
        )
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts(
            [
                entry,
                _departure(
                    entry["run_id"],
                    entry["record"],
                    superseded_by_commit="not-a-commit",
                ),
            ]
        )
    with pytest.raises(rr.RunRecordError):
        rr.fold_acts(
            [
                entry,
                _departure(
                    entry["run_id"],
                    entry["record"],
                    blob_sha256="short",
                ),
            ]
        )
    with pytest.raises(rr.RunRecordError):
        missing = _departure(entry["run_id"], entry["record"])
        del missing["ref"]
        rr.fold_acts([entry, missing])


def test_append_act_validates_before_writing(tmp_path: Path):
    index = tmp_path / "run-index.jsonl"
    a, b = _minted_entry(), _minted_entry()
    state = rr.append_act(index, a)
    assert state.census == 1
    before = index.read_bytes()
    with pytest.raises(rr.RunRecordError):
        rr.append_act(
            index,
            {
                "act": "supersedes",
                "run_id": a["run_id"],
                "supersedes": rr.mint_run_id("settling", now=NOW),
                "ref": "fixture",
            },
        )
    # A refused act is never written.
    assert index.read_bytes() == before
    rr.append_act(index, b)
    rr.append_act(
        index,
        {
            "act": "supersedes",
            "run_id": b["run_id"],
            "supersedes": a["run_id"],
            "ref": "fixture",
        },
    )
    folded = rr.fold_index(index)
    assert folded.superseded_by == {a["run_id"]: b["run_id"]}


# ---------------------------------------------------------------------------
# Legacy derivation (T103) and the standing-store dry run (T104)


def test_legacy_derivation_is_stable():
    path = "t405-incumbent-over-full-frame--d9f73e4c4e4e.json"
    assert rr.legacy_run_id(path) == rr.legacy_run_id(path)
    assert (
        rr.legacy_run_id(path)
        == "legacy:t405-incumbent-over-full-frame--d9f73e4c4e4e"
    )
    assert rr.legacy_run_id("sub/dir/record.json") == "legacy:sub/dir/record"
    assert rr.legacy_run_id("sub\\dir\\record.json") == "legacy:sub/dir/record"


def test_legacy_derivation_collision_free_over_generated_paths():
    paths = [
        f"record-{i:04d}--{i:012x}.json" for i in range(200)
    ] + [f"gen{g}/record-{g}.json" for g in range(100)]
    ids = [rr.legacy_run_id(path) for path in paths]
    assert len(set(ids)) == len(ids) == 300


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_t104_dry_run_over_standing_store(tmp_path: Path):
    standing = sorted(RUNS_STORE.glob("*.json"))
    assert standing, "the standing runs store holds records"
    before = {path.name: _sha256(path) for path in standing}

    copy_dir = tmp_path / "runs"
    shutil.copytree(RUNS_STORE, copy_dir)
    copied = sorted(p.name for p in copy_dir.iterdir())
    acts = rr.enumerate_legacy_entries(copy_dir)
    state = rr.fold_acts(acts)

    # The legacy population is the store's pre-spec
    # records — the ones carrying no run header. Since
    # Stage 2 the store also holds post-spec records
    # under their own headers (the Stage 5 materializa-
    # tion record is the first), which their own writers
    # enter; the derivation enumerates exactly the
    # pre-spec subset (restated at Stage 5, when that
    # population first stood in the store).
    pre_spec = [
        path
        for path in standing
        if "run"
        not in json.loads(path.read_text(encoding="utf-8"))
    ]
    assert pre_spec, "the standing store holds pre-spec records"
    assert len(acts) == len(pre_spec)
    assert state.census == len(pre_spec)
    for act, source in zip(acts, pre_spec):
        record = json.loads(source.read_text(encoding="utf-8"))
        assert act["act"] == "entry"
        assert act["legacy"] is True
        assert act["key_partial"] is True
        assert act["label"] == rr.LEGACY_LABEL
        assert act["record"] == source.name
        assert act["run_id"] == rr.legacy_run_id(source.name)
        assert act["key"]["surface"] == "settling"
        assert act["key"]["semantics"] == record["semantics"]
        assert act["key"]["candidate"] == record["candidate"]
        assert act["key"]["input_pins"] == record["pins"]
        # No execution stamp or code version exists to recover.
        assert "code_version" in act["missing"]
        assert "started" in act["missing"]

    # The dry run never writes: the real store is byte-identical,
    # and the copy gained no file (no index is written by a
    # derivation). Since Spec 089 Stage 2 the store also carries
    # its run index; the invariant is that the copy's contents
    # are exactly what was copied — the derivation added none.
    after = {path.name: _sha256(path) for path in standing}
    assert before == after
    assert sorted(p.name for p in copy_dir.iterdir()) == copied


def test_legacy_entries_fold_with_minted_runs():
    """The S2 refresh shape, at format level: a minted run
    supersedes a legacy entry, and the fold resolves both."""
    copy_acts = rr.enumerate_legacy_entries(RUNS_STORE)
    assert copy_acts
    legacy_id = copy_acts[0]["run_id"]
    minted = _minted_entry()
    state = rr.fold_acts(
        copy_acts
        + [
            minted,
            {
                "act": "supersedes",
                "run_id": minted["run_id"],
                "supersedes": legacy_id,
                "ref": "fixture refresh act",
            },
        ]
    )
    assert state.superseded_by == {legacy_id: minted["run_id"]}
    assert rr.is_legacy_id(legacy_id)
