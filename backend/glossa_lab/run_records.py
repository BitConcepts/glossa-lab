"""Spec 089 Stage 1 — the run-record library (T102).

The machine copy of **run-defs v1**
(`glossa-indus/ledger/RUN-DEFINITIONS.md`): execution-minted
run ids (D-089-1), the run-record header, run-key v1
comparability (D-089-4), the per-store run index (entry /
supersedes / quarantine / adjudication acts, appended and
folded — D-089-3), and legacy id derivation + recovery for
pre-spec records (D-089-5).

Structure: the builders and validators are PURE — they
compute and check in memory and write nothing.
`append_act` is the thin write entry point, used by the
surfaces' runners (settling adoption is Stage 2; the
junction tool is Stage 3). This module reads no store of
record and imports no ledger write path. Its write entry
point is named in run-defs v1 §9 as owed to the gate's
writer census when V11 lands (Stage 5's registration act);
it writes run stores and their indexes only, never a gated
generated artifact.

Standing position: the Indus script is not deciphered.
Nothing here is a decipherment claim; run hygiene governs
recorded executions, not what any result means (Spec 089
§Non-goals), and a run record certifies what an execution
recorded, never that a presentation of it was honest
(C089-20).
"""

from __future__ import annotations

import json
import re
import secrets
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

RUN_DEFS_VERSION = "run-defs v1"

#: The registered no-seed marker (run-defs v1 §4.2): a
#: surface with no seed records this string, never an
#: omitted component.
NO_SEED = "no-seed"

#: The legacy label, verbatim (run-defs v1 §7.2).
LEGACY_LABEL = "legacy — key partial"

#: The closed absence-kind list (run-defs v1 §3.2).
ABSENCE_KINDS = ("empty", "refused", "crashed")

#: The registered junction disposition vocabulary
#: (run-defs v1 §6).
DISPOSITIONS = (
    "explained-by-named-difference",
    "not-comparable",
    "identical-after-all",
    "unexplained",
)

#: The registered adjudication outcomes (run-defs v1 §7.1).
ADJUDICATION_STATES = ("quarantine-lifted", "quarantine-confirmed")

#: run-key v1's components, in registered order
#: (run-defs v1 §4).
KEY_COMPONENTS = (
    "surface",
    "command",
    "tool_version",
    "input_pins",
    "seed",
    "code_version",
    "environment_class",
)

#: The constitutive components (D-089-4): agreement on
#: exactly these makes two runs comparable. Code version and
#: environment class are recorded and diffed, never
#: constitutive.
CONSTITUTIVE_COMPONENTS = (
    "surface",
    "command",
    "tool_version",
    "input_pins",
    "seed",
)

#: The registered determinism classes.
DETERMINISM_CLASSES = ("deterministic", "named-nondeterministic")

#: The surface registry (run-defs v1 §1 + §5): the closed
#: list, each surface's determinism registration, and its
#: registered nondeterminism shape names. The `experiment`
#: surface's class is per-graph: the header must carry the
#: per-graph registered class explicitly.
SURFACES: dict[str, dict[str, Any]] = {
    "settling": {
        "determinism": "deterministic",
        "nondeterminism_shapes": (),
    },
    "experiment": {
        "determinism": "per-graph",
        "nondeterminism_shapes": (),
    },
    "study": {
        "determinism": "deterministic",
        "nondeterminism_shapes": (),
    },
    "suite": {
        "determinism": "named-nondeterministic",
        "nondeterminism_shapes": ("tray-teardown-flake",),
    },
}

_RUN_ID_RE = re.compile(
    r"^(?P<surface>[a-z]+)-(?P<stamp>\d{8}T\d{6}Z)-(?P<rand>[0-9a-f]{6})$"
)
_JUNCTION_ID_RE = re.compile(
    r"^junction-(?P<stamp>\d{8}T\d{6}Z)-(?P<rand>[0-9a-f]{6})$"
)
_STAMP_RE = re.compile(r"^\d{8}T\d{6}Z$")
_ISO_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

#: The registered components a settling legacy record does
#: not carry and cannot recover (run-defs v1 §7.2).
SETTLING_LEGACY_MISSING = (
    "command",
    "tool_version",
    "code_version",
    "seed",
    "environment_class",
    "started",
    "finished",
)


class RunRecordError(ValueError):
    """A run id, header, record, or index act violates
    run-defs v1. Raised loudly: a malformed run artifact is
    a defect to repair at the source, never to write
    around."""


# ---------------------------------------------------------------------------
# Stamps


def _as_utc(now: datetime) -> datetime:
    if now.tzinfo is None:
        return now.replace(tzinfo=timezone.utc)
    return now.astimezone(timezone.utc)


def format_stamp(now: datetime) -> str:
    """The id stamp for an execution start:
    `yyyymmddThhmmssZ`, UTC."""
    return _as_utc(now).strftime("%Y%m%dT%H%M%SZ")


def iso_stamp(now: datetime) -> str:
    """An ISO 8601 UTC execution stamp at second
    resolution, e.g. `2026-11-04T07:39:00Z`."""
    return _as_utc(now).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso_utc(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str) or not _ISO_UTC_RE.match(value):
        raise RunRecordError(
            f"{field_name} must be an ISO 8601 UTC stamp "
            f"(YYYY-MM-DDThh:mm:ssZ), got {value!r}"
        )
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise RunRecordError(
            f"{field_name} is not a real date/time: {value!r}"
        ) from exc
    return parsed.replace(tzinfo=timezone.utc)


def _coerce_stamp(value: Any, field_name: str) -> tuple[str, datetime]:
    """Accept a datetime or an ISO string; return the
    normalized ISO string and the parsed instant."""
    if isinstance(value, datetime):
        moment = _as_utc(value)
        return iso_stamp(moment), moment
    parsed = _parse_iso_utc(value, field_name)
    return iso_stamp(parsed), parsed


# ---------------------------------------------------------------------------
# Minting (D-089-1)


def _default_rand_hex() -> str:
    return secrets.token_hex(3)


class _Minter:
    """Remembers the ids it has issued and redraws on
    collision, so one minter never issues the same id
    twice (run-defs v1 §2). The cross-process half of the
    uniqueness rule is the store write path's collision
    refusal (Stage 2), not the mint."""

    def __init__(self, rand_hex: Optional[Callable[[], str]] = None):
        self._rand_hex = rand_hex or _default_rand_hex
        self._issued: set[str] = set()
        self._lock = threading.Lock()

    def mint(self, prefix: str, now: Optional[datetime] = None) -> str:
        stamp = format_stamp(now or datetime.now(timezone.utc))
        with self._lock:
            while True:
                suffix = self._rand_hex()
                if not isinstance(suffix, str) or not re.fullmatch(
                    r"[0-9a-f]{6}", suffix
                ):
                    raise RunRecordError(
                        "random source produced a malformed id "
                        f"component: {suffix!r} (6 lowercase hex "
                        "required)"
                    )
                candidate = f"{prefix}-{stamp}-{suffix}"
                if candidate not in self._issued:
                    self._issued.add(candidate)
                    return candidate


_RUN_MINTER = _Minter()
_JUNCTION_MINTER = _Minter()


def mint_run_id(
    surface: str,
    *,
    now: Optional[datetime] = None,
    minter: Optional[_Minter] = None,
) -> str:
    """Mint a run id for `surface` at execution start
    (D-089-1). Ids name executions, never content."""
    if surface not in SURFACES:
        raise RunRecordError(
            f"unregistered surface {surface!r}; the closed "
            f"list is {sorted(SURFACES)}"
        )
    return (minter or _RUN_MINTER).mint(surface, now)


def mint_junction_id(*, now: Optional[datetime] = None) -> str:
    """Mint a junction id (run-defs v1 §7.1); the junction
    tool (Stage 3) is the minter of record."""
    return _JUNCTION_MINTER.mint("junction", now)


def parse_run_id(run_id: Any) -> dict[str, str]:
    """Validate a run id's format and return its parts.
    Refuses content-shaped or malformed ids — including
    legacy ids, which are index identities, not minted
    run ids."""
    if not isinstance(run_id, str):
        raise RunRecordError(f"run id must be a string, got {run_id!r}")
    match = _RUN_ID_RE.match(run_id)
    if not match:
        raise RunRecordError(
            f"malformed run id {run_id!r}; the format is "
            "<surface>-<yyyymmddThhmmssZ>-<6 lowercase hex>"
        )
    surface = match.group("surface")
    if surface not in SURFACES:
        raise RunRecordError(
            f"run id {run_id!r} names unregistered surface {surface!r}"
        )
    return {
        "surface": surface,
        "stamp": match.group("stamp"),
        "rand": match.group("rand"),
    }


def is_legacy_id(run_id: Any) -> bool:
    return isinstance(run_id, str) and run_id.startswith("legacy:")


# ---------------------------------------------------------------------------
# The comparability key (run-key v1) and the header


def validate_key(key: Any, *, surface: str) -> dict[str, Any]:
    """Validate a run-key v1 key for `surface`: every
    registered component present and well-formed. Returns
    the key unchanged."""
    if not isinstance(key, dict):
        raise RunRecordError(f"comparability key must be an object, got {key!r}")
    for component in KEY_COMPONENTS:
        if component not in key:
            raise RunRecordError(
                f"comparability key for surface {surface!r} is "
                f"missing component {component!r} (run-key v1 "
                "carries every registered component)"
            )
    if key["surface"] != surface:
        raise RunRecordError(
            f"key surface {key['surface']!r} does not match the "
            f"record's surface {surface!r}"
        )
    for component in ("command", "tool_version", "code_version",
                      "environment_class"):
        if not isinstance(key[component], str) or not key[component]:
            raise RunRecordError(
                f"key component {component!r} must be a non-empty "
                f"string, got {key[component]!r}"
            )
    if not isinstance(key["input_pins"], dict):
        raise RunRecordError(
            "key component 'input_pins' must be an object (the "
            f"per-surface pin list), got {key['input_pins']!r}"
        )
    return key


def build_key(
    *,
    surface: str,
    command: str,
    tool_version: str,
    input_pins: dict[str, Any],
    seed: Any,
    code_version: str,
    environment_class: str,
) -> dict[str, Any]:
    """Build and validate a run-key v1 key. The seed is
    required: a surface with no seed passes the registered
    marker `NO_SEED`, never None."""
    if seed is None:
        raise RunRecordError(
            "seed component is required; a surface with no seed "
            f"records the registered marker {NO_SEED!r}"
        )
    key = {
        "surface": surface,
        "command": command,
        "tool_version": tool_version,
        "input_pins": input_pins,
        "seed": seed,
        "code_version": code_version,
        "environment_class": environment_class,
    }
    return validate_key(key, surface=surface)


def constitutive_diff(
    key_a: dict[str, Any], key_b: dict[str, Any]
) -> list[str]:
    """The constitutive components on which two keys
    differ (D-089-4). An empty list means the runs are
    comparable; a non-empty list means the pair is
    different experiments, with the differing components
    named (C089-10)."""
    return [
        component
        for component in CONSTITUTIVE_COMPONENTS
        if key_a.get(component) != key_b.get(component)
    ]


def keys_comparable(key_a: dict[str, Any], key_b: dict[str, Any]) -> bool:
    return not constitutive_diff(key_a, key_b)


def _resolve_determinism(surface: str, supplied: Optional[str]) -> str:
    registered = SURFACES[surface]["determinism"]
    if registered == "per-graph":
        if supplied is None:
            raise RunRecordError(
                f"surface {surface!r} registers its determinism "
                "class per graph; the header must carry the "
                "per-graph registered class explicitly"
            )
        if supplied not in DETERMINISM_CLASSES:
            raise RunRecordError(
                f"determinism class {supplied!r} is not registered; "
                f"the classes are {list(DETERMINISM_CLASSES)}"
            )
        return supplied
    if supplied is not None and supplied != registered:
        raise RunRecordError(
            f"surface {surface!r} is registered {registered!r}; "
            f"a header may not claim {supplied!r}"
        )
    return registered


def build_header(
    *,
    surface: str,
    tool: str,
    tool_version: str,
    command: str,
    code_version: str,
    input_pins: dict[str, Any],
    seed: Any,
    environment_class: str,
    started: Any,
    finished: Any = None,
    run_id: Optional[str] = None,
    determinism_class: Optional[str] = None,
    minter: Optional[_Minter] = None,
) -> dict[str, Any]:
    """Build and validate a run-record header (run-defs v1
    §3.1). With no `run_id`, one is minted at the execution
    start the caller passes as `started` — the executing
    tool mints at start, before results exist (D-089-1);
    a pre-minted id is validated against the surface."""
    if surface not in SURFACES:
        raise RunRecordError(
            f"unregistered surface {surface!r}; the closed "
            f"list is {sorted(SURFACES)}"
        )
    if not isinstance(tool, str) or not tool:
        raise RunRecordError(f"tool must be a non-empty string, got {tool!r}")
    started_iso, started_dt = _coerce_stamp(started, "started")
    finished_iso: Optional[str] = None
    if finished is not None:
        finished_iso, finished_dt = _coerce_stamp(finished, "finished")
        if finished_dt < started_dt:
            raise RunRecordError(
                f"finished stamp {finished_iso} precedes started "
                f"stamp {started_iso}"
            )
    if run_id is None:
        run_id = mint_run_id(surface, now=started_dt, minter=minter)
    else:
        parts = parse_run_id(run_id)
        if parts["surface"] != surface:
            raise RunRecordError(
                f"run id {run_id!r} belongs to surface "
                f"{parts['surface']!r}, not {surface!r}"
            )
    header: dict[str, Any] = {
        "run_id": run_id,
        "surface": surface,
        "tool": tool,
        "tool_version": tool_version,
        "started": started_iso,
    }
    if finished_iso is not None:
        header["finished"] = finished_iso
    header["key"] = build_key(
        surface=surface,
        command=command,
        tool_version=tool_version,
        input_pins=input_pins,
        seed=seed,
        code_version=code_version,
        environment_class=environment_class,
    )
    header["determinism_class"] = _resolve_determinism(
        surface, determinism_class
    )
    return header


def validate_header(header: Any) -> dict[str, Any]:
    """Validate a run-record header against run-defs v1
    §3.1: identity, stamps, the full key, and the surface's
    registered determinism class."""
    if not isinstance(header, dict):
        raise RunRecordError(f"run header must be an object, got {header!r}")
    for field_name in ("run_id", "surface", "tool", "tool_version",
                       "started", "key", "determinism_class"):
        if field_name not in header:
            raise RunRecordError(f"run header is missing field {field_name!r}")
    surface = header["surface"]
    if surface not in SURFACES:
        raise RunRecordError(
            f"header names unregistered surface {surface!r}"
        )
    parts = parse_run_id(header["run_id"])
    if parts["surface"] != surface:
        raise RunRecordError(
            f"header run id {header['run_id']!r} belongs to "
            f"surface {parts['surface']!r}, not {surface!r}"
        )
    if not isinstance(header["tool"], str) or not header["tool"]:
        raise RunRecordError("header tool must be a non-empty string")
    if not isinstance(header["tool_version"], str) or not header["tool_version"]:
        raise RunRecordError("header tool_version must be a non-empty string")
    started_dt = _parse_iso_utc(header["started"], "started")
    if "finished" in header:
        finished_dt = _parse_iso_utc(header["finished"], "finished")
        if finished_dt < started_dt:
            raise RunRecordError(
                f"header finished stamp {header['finished']} precedes "
                f"started stamp {header['started']}"
            )
    validate_key(header["key"], surface=surface)
    expected = _resolve_determinism(surface, header["determinism_class"])
    if header["determinism_class"] != expected:
        raise RunRecordError(
            f"header determinism class {header['determinism_class']!r} "
            f"does not match the registration for surface {surface!r}"
        )
    return header


# ---------------------------------------------------------------------------
# The run record


def validate_absence(absence: Any) -> dict[str, Any]:
    if not isinstance(absence, dict):
        raise RunRecordError(
            f"absence block must be an object, got {absence!r}"
        )
    kind = absence.get("kind")
    if kind not in ABSENCE_KINDS:
        raise RunRecordError(
            f"absence kind {kind!r} is not registered; the closed "
            f"list is {list(ABSENCE_KINDS)}"
        )
    detail = absence.get("detail")
    if not isinstance(detail, str) or not detail:
        raise RunRecordError(
            "absence block must carry a non-empty 'detail' string"
        )
    return absence


_MISSING = object()


def build_record(
    header: dict[str, Any],
    *,
    result: Any = _MISSING,
    absence: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Compose a run record from a validated header and
    exactly one outcome: a result block, or an absence
    block (run-defs v1 §3)."""
    validate_header(header)
    if (result is _MISSING) == (absence is None):
        raise RunRecordError(
            "a run record carries exactly one outcome: a result "
            "block or an absence block"
        )
    record: dict[str, Any] = {"run": header}
    if absence is not None:
        record["absence"] = validate_absence(absence)
    else:
        record["result"] = result
    return record


def validate_record(record: Any) -> dict[str, Any]:
    """Validate a run record: a valid header under `run`,
    and exactly one of `result` / `absence` at top level
    (the settling record shape — header additive over the
    surface's own fields — satisfies this by construction
    from Stage 2)."""
    if not isinstance(record, dict):
        raise RunRecordError(f"run record must be an object, got {record!r}")
    if "run" not in record:
        raise RunRecordError("run record carries no 'run' header")
    validate_header(record["run"])
    has_result = "result" in record
    has_absence = "absence" in record
    if has_result == has_absence:
        raise RunRecordError(
            "run record must carry exactly one of 'result' / "
            "'absence'"
        )
    if has_absence:
        validate_absence(record["absence"])
    return record


# ---------------------------------------------------------------------------
# The run index (D-089-3): acts, fold, append


@dataclass
class IndexState:
    """The folded state of one store's run index."""

    entries: dict[str, dict[str, Any]] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)
    supersedes: dict[str, list[str]] = field(default_factory=dict)
    superseded_by: dict[str, str] = field(default_factory=dict)
    junctions: dict[str, dict[str, Any]] = field(default_factory=dict)

    @property
    def open_quarantine(self) -> dict[str, set[str]]:
        """run id -> the junction ids under which it stands
        quarantined (a junction lifts only by adjudication;
        the latest adjudication state governs)."""
        out: dict[str, set[str]] = {}
        for junction_id, junction in self.junctions.items():
            if junction["lifted"]:
                continue
            for run_id in junction["run_ids"]:
                out.setdefault(run_id, set()).add(junction_id)
        return out

    @property
    def census(self) -> int:
        return len(self.entries)


def _require_fields(act: dict[str, Any], fields: Iterable[str]) -> None:
    for name in fields:
        if name not in act:
            raise RunRecordError(
                f"index act {act.get('act')!r} is missing field {name!r}"
            )


def _apply_entry(state: IndexState, act: dict[str, Any]) -> None:
    _require_fields(act, ("run_id", "record", "key"))
    run_id = act["run_id"]
    if not isinstance(run_id, str) or not run_id:
        raise RunRecordError(f"entry act run_id must be a string, got {run_id!r}")
    if not is_legacy_id(run_id):
        parse_run_id(run_id)
    if not isinstance(act["record"], str) or not act["record"]:
        raise RunRecordError("entry act 'record' must be a non-empty path string")
    if not isinstance(act["key"], dict):
        raise RunRecordError("entry act 'key' must be an object")
    if run_id in state.entries:
        raise RunRecordError(
            f"duplicate entry act for run id {run_id!r}: an id is "
            "one execution, entered once"
        )
    if act.get("legacy"):
        if not is_legacy_id(run_id):
            raise RunRecordError(
                f"legacy entry act carries non-legacy run id {run_id!r}"
            )
        if act.get("label") != LEGACY_LABEL or not act.get("key_partial"):
            raise RunRecordError(
                f"legacy entry {run_id!r} must carry the label "
                f"{LEGACY_LABEL!r} and key_partial: true"
            )
        if not act.get("missing"):
            raise RunRecordError(
                f"legacy entry {run_id!r} must name the components "
                "that do not exist to recover ('missing')"
            )
    else:
        if is_legacy_id(run_id):
            raise RunRecordError(
                f"entry act for legacy id {run_id!r} must be marked "
                "legacy (legacy ids exist only under the partial "
                "label)"
            )
        validate_key(act["key"], surface=act["key"].get("surface"))
    state.entries[run_id] = act
    state.order.append(run_id)


def _apply_supersedes(state: IndexState, act: dict[str, Any]) -> None:
    _require_fields(act, ("run_id", "supersedes", "ref"))
    new_id, old_id = act["run_id"], act["supersedes"]
    for named in (new_id, old_id):
        if named not in state.entries:
            raise RunRecordError(
                f"supersedes act names unknown run id {named!r}"
            )
    if new_id == old_id:
        raise RunRecordError("a run may not supersede itself")
    if not isinstance(act["ref"], str) or not act["ref"]:
        raise RunRecordError(
            "supersedes act must carry the act reference ('ref') "
            "that ordered the supersession"
        )
    if old_id in state.superseded_by:
        raise RunRecordError(
            f"run {old_id!r} is already superseded by "
            f"{state.superseded_by[old_id]!r}; a record's "
            "successor is single"
        )
    state.superseded_by[old_id] = new_id
    state.supersedes.setdefault(new_id, []).append(old_id)


def _apply_quarantine(state: IndexState, act: dict[str, Any]) -> None:
    _require_fields(act, ("junction_id", "run_ids"))
    junction_id = act["junction_id"]
    if not isinstance(junction_id, str) or not _JUNCTION_ID_RE.match(
        junction_id
    ):
        raise RunRecordError(
            f"quarantine act junction id {junction_id!r} is "
            "malformed; the format is junction-<yyyymmddThhmmssZ>"
            "-<6 lowercase hex>"
        )
    run_ids = act["run_ids"]
    if not isinstance(run_ids, list) or not run_ids:
        raise RunRecordError("quarantine act 'run_ids' must be a non-empty list")
    for run_id in run_ids:
        if run_id not in state.entries:
            raise RunRecordError(
                f"quarantine act names unknown run id {run_id!r}"
            )
    junction = state.junctions.setdefault(
        junction_id, {"run_ids": [], "lifted": False, "adjudications": []}
    )
    for run_id in run_ids:
        if run_id not in junction["run_ids"]:
            junction["run_ids"].append(run_id)


def _apply_adjudication(state: IndexState, act: dict[str, Any]) -> None:
    _require_fields(act, ("junction_id", "ruling", "actor", "resulting_state"))
    junction_id = act["junction_id"]
    if junction_id not in state.junctions:
        raise RunRecordError(
            f"adjudication act names unknown junction id "
            f"{junction_id!r} (no quarantine act introduced it)"
        )
    if act["resulting_state"] not in ADJUDICATION_STATES:
        raise RunRecordError(
            f"adjudication resulting_state {act['resulting_state']!r} "
            f"is not registered; the states are "
            f"{list(ADJUDICATION_STATES)}"
        )
    for name in ("ruling", "actor"):
        if not isinstance(act[name], str) or not act[name]:
            raise RunRecordError(
                f"adjudication act {name!r} must be a non-empty string"
            )
    junction = state.junctions[junction_id]
    junction["adjudications"].append(act)
    junction["lifted"] = act["resulting_state"] == "quarantine-lifted"


_ACT_APPLIERS = {
    "entry": _apply_entry,
    "supersedes": _apply_supersedes,
    "quarantine": _apply_quarantine,
    "adjudication": _apply_adjudication,
}


def apply_act(state: IndexState, act: Any) -> IndexState:
    """Apply one index act to a folded state, with every
    registered refusal (run-defs v1 §7.1). Mutates and
    returns `state`."""
    if not isinstance(act, dict):
        raise RunRecordError(f"index act must be an object, got {act!r}")
    kind = act.get("act")
    applier = _ACT_APPLIERS.get(kind) if isinstance(kind, str) else None
    if applier is None:
        raise RunRecordError(
            f"unknown index act kind {kind!r}; the acts are "
            f"{sorted(_ACT_APPLIERS)}"
        )
    applier(state, act)
    return state


def fold_acts(acts: Iterable[dict[str, Any]]) -> IndexState:
    """Fold index acts in order to the store's current
    state."""
    state = IndexState()
    for act in acts:
        apply_act(state, act)
    return state


def read_index(index_path: Path) -> list[dict[str, Any]]:
    """Read a store's run index acts. A store with no index
    yet reads as empty."""
    path = Path(index_path)
    if not path.is_file():
        return []
    acts: list[dict[str, Any]] = []
    for line_no, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            acts.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise RunRecordError(
                f"{path}:{line_no}: malformed index line: {exc}"
            ) from exc
    return acts


def fold_index(index_path: Path) -> IndexState:
    return fold_acts(read_index(index_path))


def append_act(index_path: Path, act: dict[str, Any]) -> IndexState:
    """Append one act to a store's run index. The act is
    validated against the folded current state first: a
    refused act is never written, and the index file is
    byte-unchanged by the refusal. Returns the new folded
    state."""
    path = Path(index_path)
    state = fold_index(path)
    apply_act(state, act)
    line = json.dumps(act, sort_keys=True, ensure_ascii=False)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    return state


# ---------------------------------------------------------------------------
# Legacy derivation and recovery (D-089-5)


def legacy_run_id(store_rel_path: str) -> str:
    """Derive a legacy id from a record's store-relative
    path: `legacy:` + the path with its final suffix
    removed (run-defs v1 §7.2). A pure function of the
    path — stable across calls."""
    normalized = store_rel_path.replace("\\", "/")
    path = Path(normalized)
    stem = path.name
    if "." in stem:
        stem = stem.rsplit(".", 1)[0]
    parent = path.parent.as_posix()
    rel_stem = stem if parent in ("", ".") else f"{parent}/{stem}"
    return f"legacy:{rel_stem}"


def legacy_entry_for_record(
    record_rel_path: str, record: dict[str, Any]
) -> dict[str, Any]:
    """The legacy `entry` act for one pre-spec settling run
    record: the recoverable key components (semantics,
    candidate, the pins block verbatim) under the partial
    label. A record missing a recoverable component
    refuses, naming the record — it is not half-entered.
    The record itself is never modified."""
    for component in ("semantics", "candidate", "pins"):
        if component not in record:
            raise RunRecordError(
                f"legacy recovery: record {record_rel_path!r} "
                f"carries no {component!r} to recover"
            )
    key = {
        "surface": "settling",
        "semantics": record["semantics"],
        "candidate": record["candidate"],
        "input_pins": record["pins"],
    }
    return {
        "act": "entry",
        "run_id": legacy_run_id(record_rel_path),
        "record": record_rel_path,
        "key": key,
        "legacy": True,
        "key_partial": True,
        "label": LEGACY_LABEL,
        "missing": list(SETTLING_LEGACY_MISSING),
    }


def enumerate_legacy_entries(
    store_dir: Path, *, surface: str = "settling"
) -> list[dict[str, Any]]:
    """Enumerate legacy entry acts over a run store's
    standing records (sorted by filename). Read-only: the
    records are opened, never written. In run-defs v1 the
    settling store is the only store with a registered
    recovery; other surfaces refuse until their adoption
    stages register one."""
    if surface != "settling":
        raise RunRecordError(
            f"no legacy recovery is registered for surface "
            f"{surface!r} in run-defs v1"
        )
    store = Path(store_dir)
    acts: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record_path in sorted(store.glob("*.json")):
        record = json.loads(record_path.read_text(encoding="utf-8"))
        act = legacy_entry_for_record(record_path.name, record)
        if act["run_id"] in seen:
            raise RunRecordError(
                f"legacy derivation collision: {act['run_id']!r} "
                "derives from more than one record in the store "
                "— a store defect, reported, not worked around"
            )
        seen.add(act["run_id"])
        acts.append(act)
    return acts


__all__ = [
    "ABSENCE_KINDS",
    "ADJUDICATION_STATES",
    "CONSTITUTIVE_COMPONENTS",
    "DISPOSITIONS",
    "IndexState",
    "KEY_COMPONENTS",
    "LEGACY_LABEL",
    "NO_SEED",
    "RUN_DEFS_VERSION",
    "RunRecordError",
    "SETTLING_LEGACY_MISSING",
    "SURFACES",
    "append_act",
    "apply_act",
    "build_header",
    "build_key",
    "build_record",
    "constitutive_diff",
    "enumerate_legacy_entries",
    "fold_acts",
    "fold_index",
    "format_stamp",
    "is_legacy_id",
    "iso_stamp",
    "keys_comparable",
    "legacy_entry_for_record",
    "legacy_run_id",
    "mint_junction_id",
    "mint_run_id",
    "parse_run_id",
    "read_index",
    "validate_absence",
    "validate_header",
    "validate_key",
    "validate_record",
]
