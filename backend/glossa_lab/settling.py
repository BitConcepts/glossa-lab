"""Spec 086 Stage 4 — the settling engine (T403).

Implements Point 3 of the winning-combination adoption
under the semantics registered in
`glossa-indus/ledger/SETTLING-SEMANTICS.md`
(**glossa-settle-1**, T401 — registered before this module
existed; the canonical outputs were derived by hand in
`glossa-indus/ledger/settling-canonical.json`, T402, and
this engine's test — T404,
`backend/tests/test_settling_canonical.py` — requires
exact reproduction of every one of them).

Standing position: the Indus script is not deciphered.
Every output of this module is a computation over
ledgered relations under glossa-settle-1 semantics,
labeled as such (see SETTLING_LABEL); nothing here is a
decipherment claim, a reading, or evidence about the
script, and a run moves no ledger status, stage, score,
or weight (C086-16).

Structure (mirroring the matrix generator, and
harmonization adoption 3, item 5): the evaluators are
PURE builders — `evaluate_candidate` and `compare_runs`
compute run records in memory and write nothing;
`write_assignment_sets` and `write_run_record` are the
thin write wrappers used only by the command
(`tools/ledger/run_settling.py`). This module imports no
ledger intake/write entry point: it reads the ledger
through `ledger_intake`'s read path only, and the gate's
V9 audit (plus V8's reachability arm) verifies that.

The semantics' registered readings this module follows,
stated where a reader might expect otherwise:

- Sign identity is by (frame, number)
  (SETTLING-SEMANTICS.md §2): `mahadevan:64`,
  `mahadevan:064`, and the register key `M064` are the
  same sign. This deliberately differs from matrix-defs
  v1 R4's literal key construction; the divergence is
  registered in the semantics and stands.
- Contexts are the canonical anchors register's records,
  one per sign (§4); the database `anchor_sets` pair
  lists are not settling contexts in v1.
- Strictness is **recomputed** under the D-A rule the
  anchors file records (`strict_sa_independent_hm`),
  never trusted from the stored `strict_set` flags; a
  register whose stored flags disagree with the
  recomputation refuses (§1).
- S-R2 is the registered determinate v1 form (§5):
  bearings come only from governing stored outcome
  blocks mapped through the outcome table below (this
  module's registered copy of matrix-defs v1 §6), and
  tallies are **value-independent** in v1 — they depend
  on which signs are assigned, never on the values. A
  run record says so (§5's requirement), in its
  `s_r2_value_independence` field.
- S-R3 is registered but inert in v1: no positional-
  class table is registered (the table is UNMEASURED,
  §10), so every run reports the determinate zero.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from glossa_lab import ledger_intake as li

# ---------------------------------------------------------------------------
# Registered constants — this module's copies of
# glossa-settle-1 (SETTLING-SEMANTICS.md) and of the
# matrix-defs v1 outcome table its S-R2 reads.

SEMANTICS_VERSION = "glossa-settle-1"
SETTLING_LABEL = (
    "Computation over ledgered relations under "
    "glossa-settle-1 semantics. Establishes what the "
    "ledger implies under these rules, not what the "
    "script says."
)

ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
PROVENANCE_REGISTER_REL = "reports/phase108_provenance_register.json"
CORPUS_REL = "glossa-corpus/indus/exports/indus_research.jsonl"
CANONICAL_REL = "glossa-indus/ledger/settling-canonical.json"
ASSIGNMENT_SETS_REL = "glossa-indus/ledger/assignment-sets.json"
RUN_STORE_REL = "glossa-indus/ledger/runs"

# The strict-anchor rule (semantics §1; Spec 029 D-A):
# confidence in {HIGH, MEDIUM} AND the Phase-108 register
# category not in the SA-lineage set AND the register's
# sa_in_chain is false.
STRICT_RULE_ID = "strict_sa_independent_hm"
STRICT_CONFIDENCES = ("HIGH", "MEDIUM")
SA_LINEAGE_CATEGORIES = ("SA_DERIVED", "SA_CONFIRMED_ONLY")

# Frame → register key prefix (semantics §2). v1 settles
# the mahadevan frame only; the register's one H-prefixed
# key belongs to a frame the anchors file does not name
# (UNMEASURED, §10) and is out of scope.
FRAME_PREFIXES = {"mahadevan": "M"}
SETTLED_FRAME = "mahadevan"

# The outcome table (semantics §5, carrying matrix-defs
# v1 §6): no recorded outcome maps to supporting in v1;
# an unexecuted or null outcome bears neither way. The
# tally keys are the semantics' registered names —
# `supporting`, `opposing`, `constraining` — not the
# matrix's cell relation values.
BEARING_OUTCOMES = {
    "NOT SUPPORTED": "opposing",
    "INCONSISTENT": "opposing",
    "NOT NUMERAL-LIKE": "opposing",
}
TALLY_KEYS = ("supporting", "opposing", "constraining")

S_R2_VALUE_INDEPENDENCE = (
    "S-R2 in v1 is value-independent: a touched claim's "
    "tallies depend on which signs are assigned, never on "
    "the values assigned (SETTLING-SEMANTICS.md §5)."
)


class SettlingError(RuntimeError):
    """A run refuses: a defect in the record it was asked
    to settle over, named. Nothing is written."""


# ---------------------------------------------------------------------------
# Register access (hash-verified, through the ledger's
# pointers — the Stage 2 route)


def _records_of(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("claims"), list):
            return [r for r in data["claims"] if isinstance(r, dict)]
        return [r for r in data.values() if isinstance(r, dict)]
    return []


class _Registers:
    """The source records the ledger entries name, loaded
    only after canonical-hash verification."""

    def __init__(self, root: Path):
        self.root = root
        self._parsed: dict[str, Any] = {}
        self.mismatches: list[str] = []

    def verify(self, rel_path: str, recorded_sha256: str) -> None:
        if rel_path in self._parsed or rel_path in self.mismatches:
            return
        target = self.root / rel_path
        if not target.is_file():
            self.mismatches.append(f"{rel_path}: file not found")
            return
        actual = li.sha256_file(target)
        if actual != recorded_sha256:
            self.mismatches.append(
                f"{rel_path}: recorded sha256 {recorded_sha256} "
                f"does not match the file on disk ({actual})"
            )
            return
        try:
            self._parsed[rel_path] = json.loads(
                target.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            self.mismatches.append(f"{rel_path}: cannot parse: {exc}")

    def record(self, rel_path: str, claim_id: str) -> Optional[dict[str, Any]]:
        data = self._parsed.get(rel_path)
        if data is None:
            return None
        for record in _records_of(data):
            if record.get("claim_id") == claim_id or record.get("id") == claim_id:
                return record
        return None

    def raise_if_mismatched(self) -> None:
        if self.mismatches:
            named = "\n  ".join(sorted(set(self.mismatches)))
            raise SettlingError(
                "source verification failed — the records on "
                "disk are not the records the ledger mirrors:\n  "
                + named
            )


# ---------------------------------------------------------------------------
# Run state: the registers a run reads, each pinned
# (semantics §1)


@dataclass
class SettleState:
    root: Path
    entries: list[dict[str, Any]]
    claims: list[dict[str, Any]]
    anchors: dict[str, Any]
    strict: set[str]
    registers: _Registers
    pins: dict[str, Any]


def _recompute_strict(
    anchors: dict[str, Any], register_records: dict[str, Any]
) -> set[str]:
    """The D-A strict set, recomputed from the canonical
    anchors file and the Phase-108 provenance register
    (semantics §1) — never the stored flags."""
    strict: set[str] = set()
    for sign, record in anchors.items():
        if (record.get("confidence") or "").upper() not in STRICT_CONFIDENCES:
            continue
        reg = register_records.get(sign)
        if reg is None:
            continue
        if reg.get("category") in SA_LINEAGE_CATEGORIES:
            continue
        if reg.get("sa_in_chain"):
            continue
        strict.add(sign)
    return strict


def load_state(root: Path) -> SettleState:
    """Load and pin every register a settling run reads,
    refusing where the record is not in the state its own
    record claims (semantics §1)."""
    root = Path(root)

    ledger_path = root / li.LEDGER_REL
    if not ledger_path.is_file():
        raise SettlingError(f"ledger not found: {li.LEDGER_REL}")
    entries = li.read_ledger(ledger_path)
    claims = [e for e in entries if e.get("kind") == "claim"]

    anchors_path = root / ANCHORS_REL
    if not anchors_path.is_file():
        raise SettlingError(f"anchors register not found: {ANCHORS_REL}")
    anchors_bytes = anchors_path.read_bytes()
    anchors_data = json.loads(anchors_bytes.decode("utf-8"))
    anchors = anchors_data.get("anchors", {})

    annotation = (
        anchors_data.get("metadata", {}).get(
            "spec029_phase_h_annotation", {}
        )
    )
    recorded_rule = annotation.get("strict_set_rule", {})
    if recorded_rule.get("rule_id") != STRICT_RULE_ID:
        raise SettlingError(
            f"anchors file records strict rule "
            f"{recorded_rule.get('rule_id')!r}; glossa-settle-1 "
            f"is registered against {STRICT_RULE_ID!r} — the "
            "register is not in the state its record claims"
        )

    register_path = root / PROVENANCE_REGISTER_REL
    if not register_path.is_file():
        raise SettlingError(
            f"Phase-108 provenance register not found: "
            f"{PROVENANCE_REGISTER_REL}"
        )
    register_data = json.loads(register_path.read_text(encoding="utf-8"))
    register_records = register_data.get("records", register_data)
    if not isinstance(register_records, dict):
        register_records = {}

    strict = _recompute_strict(anchors, register_records)
    stored = {s for s, r in anchors.items() if r.get("strict_set")}
    if strict != stored:
        only_recomputed = sorted(strict - stored)
        only_stored = sorted(stored - strict)
        raise SettlingError(
            "strict-set recomputation disagrees with the "
            "stored strict_set flags — the register is not "
            f"in the state its record claims (recomputed-only "
            f"{only_recomputed[:8]}; stored-only "
            f"{only_stored[:8]})"
        )
    if recorded_rule.get("strict_count") is not None and (
        recorded_rule["strict_count"] != len(strict)
    ):
        raise SettlingError(
            f"anchors file records strict_count "
            f"{recorded_rule['strict_count']}, recomputed "
            f"{len(strict)} — the register is not in the "
            "state its record claims"
        )

    registers = _Registers(root)
    for entry in entries:
        for source in entry.get("sources", []):
            registers.verify(source["path"], source["sha256"])
    registers.raise_if_mismatched()

    corpus_path = root / CORPUS_REL
    if not corpus_path.is_file():
        raise SettlingError(f"corpus snapshot not found: {CORPUS_REL}")

    pins = {
        "ledger": {
            "path": li.LEDGER_REL,
            "sha256": li.canonical_sha256_bytes(ledger_path.read_bytes()),
            "lines": len(entries),
        },
        "anchors_register": {
            "path": ANCHORS_REL,
            "sha256_raw_bytes": hashlib.sha256(anchors_bytes).hexdigest(),
            "bytes": len(anchors_bytes),
            "records": len(anchors),
            "strict": len(strict),
            "strict_rule": STRICT_RULE_ID,
            "strict_rule_version": recorded_rule.get("rule_version"),
        },
        "phase108_register": {
            "path": PROVENANCE_REGISTER_REL,
            "sha256": li.sha256_file(register_path),
        },
        "corpus_snapshot": {
            "path": CORPUS_REL,
            "sha256": li.sha256_file(corpus_path),
        },
    }
    return SettleState(
        root=root,
        entries=entries,
        claims=claims,
        anchors=anchors,
        strict=strict,
        registers=registers,
        pins=pins,
    )


# ---------------------------------------------------------------------------
# Signs, candidates, contexts (semantics §2–§4)


def _sign_identity(ref: Any) -> Optional[tuple[str, int]]:
    """A frame-qualified sign ref → its (frame, number)
    identity, or None where the ref is not of that form."""
    frame, sep, value = str(ref).partition(":")
    if not sep or not frame:
        return None
    try:
        number = int(value)
    except ValueError:
        return None
    return (frame, number)


def _anchor_key(identity: tuple[str, int]) -> Optional[str]:
    """The register key for a sign identity, by (frame,
    number) — the register's keys are the frame's prefix
    plus the number zero-padded to three digits (§2)."""
    frame, number = identity
    prefix = FRAME_PREFIXES.get(frame)
    if prefix is None:
        return None
    return f"{prefix}{number:03d}"


def _validate_candidate(candidate: dict[str, Any]) -> dict[tuple[str, int], str]:
    """A candidate record → {sign identity: value},
    refusing the malformed shapes §3 names."""
    if not isinstance(candidate, dict) or not candidate.get("id"):
        raise SettlingError("candidate record carries no id")
    assignments: dict[tuple[str, int], str] = {}
    for item in candidate.get("assignments") or []:
        if not isinstance(item, dict) or "sign" not in item or "value" not in item:
            raise SettlingError(
                f"candidate {candidate['id']!r}: assignment "
                f"{item!r} is not a {{sign, value}} pair"
            )
        identity = _sign_identity(item["sign"])
        if identity is None:
            raise SettlingError(
                f"candidate {candidate['id']!r}: sign ref "
                f"{item['sign']!r} is not frame-qualified"
            )
        if identity in assignments:
            raise SettlingError(
                f"candidate {candidate['id']!r} assigns sign "
                f"{item['sign']!r} twice — a candidate that "
                "assigns one sign twice is malformed (§3)"
            )
        assignments[identity] = str(item["value"])
    return assignments


def _validate_scope(scope: list[Any]) -> list[tuple[str, tuple[str, int]]]:
    """A scope (a named list of frame-qualified signs) →
    [(the scope's string form, its identity)], refusing
    duplicates and unparseable refs."""
    seen: set[tuple[str, int]] = set()
    out: list[tuple[str, tuple[str, int]]] = []
    for ref in scope:
        identity = _sign_identity(ref)
        if identity is None:
            raise SettlingError(
                f"scope sign ref {ref!r} is not frame-qualified"
            )
        if identity in seen:
            raise SettlingError(
                f"scope names sign {ref!r} twice — a scope is "
                "a set of signs (§3)"
            )
        seen.add(identity)
        out.append((str(ref), identity))
    return out


def _outcome_blocks(
    state: SettleState, entry: dict[str, Any]
) -> dict[str, list[dict[str, Any]]]:
    """All stored outcome blocks of an entry's records of
    record, grouped by study — the scan matrix-defs v1 R3
    registers, read here for S-R2."""
    blocks_by_spec: dict[str, list[dict[str, Any]]] = {}
    for source in entry.get("sources", []):
        record = state.registers.record(source["path"], source["claim_id"])
        if record is None:
            continue
        for key, value in record.items():
            if (
                isinstance(value, dict)
                and "spec" in value
                and "outcome" in value
            ):
                spec = str(value["spec"])
                blocks_by_spec.setdefault(spec, []).append(
                    {
                        "spec": spec,
                        "outcome": str(value["outcome"]),
                        "date": value.get("date"),
                        "pointer": (
                            f"{source['path']}:{source['claim_id']}#{key}"
                        ),
                    }
                )
    return blocks_by_spec


def _governing(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    """The governing block of one study: latest dated
    governs; a block without a date sorts before dated
    blocks; ties break by pointer (matrix-defs v1 R3's
    total order)."""
    return sorted(blocks, key=lambda b: (str(b["date"] or ""), b["pointer"]))[-1]


def _falsifier_count(entry: dict[str, Any]) -> int:
    """The number of falsifier strings on a ledger entry
    (S-R2(ii)): the entry's falsifier field, stored as a
    list of strings, a single string, or null."""
    falsifier = entry.get("falsifier")
    if isinstance(falsifier, list):
        return sum(1 for f in falsifier if isinstance(f, str) and f)
    if isinstance(falsifier, str) and falsifier:
        return 1
    return 0


# ---------------------------------------------------------------------------
# The evaluator (pure): S-R1…S-R4 over one candidate and
# scope, producing the run record's result block in
# exactly the registered field set (semantics §5, S-R4)


def evaluate_candidate(
    state: SettleState,
    candidate: dict[str, Any],
    scope: list[Any],
) -> dict[str, Any]:
    assignments = _validate_candidate(candidate)
    scope_pairs = _validate_scope(scope)
    scope_ids = {identity for _, identity in scope_pairs}

    # The run's effective candidate (§3): assignments
    # whose sign is in the scope, in scope order;
    # assignments outside the scope enter no count and
    # are enumerated on the run record, not here.
    assigned: list[dict[str, Any]] = []
    for sign_str, identity in scope_pairs:
        if identity in assignments:
            assigned.append(
                {"sign": sign_str, "value": assignments[identity]}
            )
    assigned_ids = {identity for _, identity in scope_pairs} & set(assignments)

    # S-R1 — anchor-context check.
    contexts: list[dict[str, Any]] = []
    uncontexted: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    strict_contexts = 0
    consistent = 0
    non_strict_contexts = 0
    for item in assigned:
        identity = _sign_identity(item["sign"])
        assert identity is not None  # scope refs were validated
        key = _anchor_key(identity)
        record = state.anchors.get(key) if key else None
        if record is None:
            uncontexted.append(
                {"sign": item["sign"], "value": item["value"]}
            )
            continue
        is_strict = key in state.strict
        reading = record.get("reading")
        if is_strict:
            strict_contexts += 1
            if item["value"] == reading:
                result = "consistent"
                consistent += 1
            else:
                result = "conflict"
                conflicts.append(
                    {
                        "sign": item["sign"],
                        "anchor": key,
                        "assigned_value": item["value"],
                        "anchor_reading": reading,
                    }
                )
        else:
            result = "non_strict"
            non_strict_contexts += 1
        contexts.append(
            {
                "sign": item["sign"],
                "anchor": key,
                "assigned_value": item["value"],
                "anchor_reading": reading,
                "confidence": record.get("confidence"),
                "strict": is_strict,
                "result": result,
            }
        )

    # S-R2 — matrix-bearing check (v1 determinate form).
    claims_touched: list[dict[str, Any]] = []
    for entry in state.claims:
        sign_refs = entry.get("sign_refs") or []
        if not sign_refs:
            continue
        via = [
            ref
            for ref in sign_refs
            if _sign_identity(ref) in assigned_ids
        ]
        if not via:
            continue
        tallies = {key: 0 for key in TALLY_KEYS}
        for spec, blocks in _outcome_blocks(state, entry).items():
            relation = BEARING_OUTCOMES.get(_governing(blocks)["outcome"])
            if relation:
                tallies[relation] += 1
        claims_touched.append(
            {
                "claim": entry["id"],
                "via_signs": via,
                "tallies": tallies,
                "falsifiers_present": _falsifier_count(entry),
                # No falsifier's textual form is machine-
                # evaluable against anchor records in v1
                # (§5), so the evaluable count is the
                # determinate zero.
                "falsifiers_evaluable": 0,
            }
        )

    # S-R3 — positional check: registered but inert in v1
    # (no class table is registered; the table is
    # UNMEASURED, §10), so the determinate zero.
    s_r3 = {"class_table": None, "violations": []}

    # Forced readings (§5): scope signs left unassigned
    # whose strict records determine the value.
    forced: list[dict[str, Any]] = []
    for sign_str, identity in scope_pairs:
        if identity in assigned_ids:
            continue
        key = _anchor_key(identity)
        if key and key in state.strict and key in state.anchors:
            forced.append(
                {"sign": sign_str, "value": state.anchors[key].get("reading")}
            )

    scope_signs = len(scope_pairs)
    assigned_count = len(assigned)
    return {
        "scope": [sign_str for sign_str, _ in scope_pairs],
        "scope_signs": scope_signs,
        "assigned": assigned,
        "assigned_count": assigned_count,
        "assigned_share": (
            assigned_count / scope_signs if scope_signs else None
        ),
        "uncontexted_assignments": uncontexted,
        "contexts": contexts,
        "contexts_touched": len(contexts),
        "strict_contexts": strict_contexts,
        "consistent": consistent,
        "non_strict_contexts": non_strict_contexts,
        "conflicts": conflicts,
        "strict_agreement_share": (
            consistent / strict_contexts if strict_contexts else None
        ),
        "contexted_share": (
            len(contexts) / assigned_count if assigned_count else None
        ),
        "claims_touched": claims_touched,
        "claims_touched_count": len(claims_touched),
        "s_r3": s_r3,
        "forced": forced,
    }


def run_record(
    state: SettleState,
    candidate: dict[str, Any],
    scope: list[Any],
    *,
    scenario: Optional[str] = None,
) -> dict[str, Any]:
    """One settling run record (semantics §5, S-R4): the
    header (label, semantics, candidate, scope, input
    pins) over the evaluator's result block. Pure — the
    record is returned, not written."""
    assignments = _validate_candidate(candidate)
    scope_pairs = _validate_scope(scope)
    scope_ids = {identity for _, identity in scope_pairs}
    out_of_scope = [
        {"sign": item["sign"], "value": str(item["value"])}
        for item in candidate.get("assignments") or []
        if isinstance(item, dict)
        and _sign_identity(item.get("sign")) is not None
        and _sign_identity(item.get("sign")) not in scope_ids
    ]
    return {
        "artifact": "settling run record",
        "label": SETTLING_LABEL,
        "semantics": SEMANTICS_VERSION,
        "scenario": scenario,
        "candidate": candidate["id"],
        "candidate_provenance": candidate.get("provenance"),
        "pins": state.pins,
        "scope": [sign_str for sign_str, _ in scope_pairs],
        "out_of_scope_assignments": out_of_scope,
        "s_r2_value_independence": S_R2_VALUE_INDEPENDENCE,
        "result": evaluate_candidate(state, candidate, scope),
    }


# ---------------------------------------------------------------------------
# The dual run: a comparison over two run records
# (semantics §7)


def _side_key(candidate_id: str) -> str:
    """The comparison's side label for a candidate id:
    the id with hyphens as underscores (`incumbent`,
    `full_register`)."""
    return candidate_id.replace("-", "_")


def compare_runs(
    run_a: dict[str, Any],
    run_b: dict[str, Any],
    *,
    expectations: Optional[list[dict[str, Any]]] = None,
    expectations_note: Optional[str] = None,
) -> dict[str, Any]:
    """The dual-run comparison record (§7): both runs'
    S-R2 tallies over every claim either run touches,
    the divergences named claim by claim, the coverage
    deltas, and the signs assigned by one run only.

    A comparison is over two runs of ONE ledger build:
    the semantics version and the ledger and corpus pins
    of both run records must agree, or the comparison
    refuses (C086-15's registered falsifier — a comparison
    implemented as two single-run outputs pasted side by
    side, with no joint falsifier check, is named there
    as the defect this function exists to prevent).

    Pre-registered expectations are comparison INPUT data
    in v1 (§7 names them as expectations "the program's
    record carries"); no expectations register exists in
    v1's record, so the default input is empty and the
    comparison states the absence in so many words — a
    named absence, not an omission."""
    for key in ("semantics",):
        if run_a.get(key) != run_b.get(key):
            raise SettlingError(
                f"comparison refuses: the two runs carry "
                f"different {key} ({run_a.get(key)!r} vs "
                f"{run_b.get(key)!r})"
            )
    for pin in ("ledger", "corpus_snapshot"):
        hash_a = (run_a.get("pins", {}).get(pin) or {}).get("sha256")
        hash_b = (run_b.get("pins", {}).get(pin) or {}).get("sha256")
        if hash_a != hash_b:
            raise SettlingError(
                f"comparison refuses: the two runs were made "
                f"over different {pin} builds ({hash_a} vs "
                f"{hash_b}) — a comparison is one ledger "
                "build read two ways (§7)"
            )
    side_a = _side_key(run_a["candidate"])
    side_b = _side_key(run_b["candidate"])
    if side_a == side_b:
        raise SettlingError(
            "comparison refuses: both runs carry the same "
            f"candidate id ({run_a['candidate']!r}) — a dual "
            "run compares two candidates (§7)"
        )

    tallies_a = {
        t["claim"]: t["tallies"] for t in run_a["result"]["claims_touched"]
    }
    tallies_b = {
        t["claim"]: t["tallies"] for t in run_b["result"]["claims_touched"]
    }
    zero = {key: 0 for key in TALLY_KEYS}
    claims_compared: list[dict[str, Any]] = []
    divergences: list[dict[str, Any]] = []
    # Ledger order: run records carry claims in ledger
    # order; the union keeps that order.
    seen: list[str] = []
    for claim_id in list(tallies_a) + list(tallies_b):
        if claim_id not in seen:
            seen.append(claim_id)
    for claim_id in seen:
        ta = tallies_a.get(claim_id, dict(zero))
        tb = tallies_b.get(claim_id, dict(zero))
        divergent = ta != tb
        claims_compared.append(
            {
                "claim": claim_id,
                f"{side_a}_tallies": ta,
                f"{side_b}_tallies": tb,
                "divergent": divergent,
            }
        )
        if divergent:
            divergences.append(
                {
                    "claim": claim_id,
                    f"{side_a}_tallies": ta,
                    f"{side_b}_tallies": tb,
                }
            )

    def delta(field_a: Any, field_b: Any) -> dict[str, Any]:
        return {side_a: field_a, side_b: field_b}

    ra, rb = run_a["result"], run_b["result"]
    coverage_deltas = {
        "assigned_count": delta(ra["assigned_count"], rb["assigned_count"]),
        "contexts_touched": delta(
            ra["contexts_touched"], rb["contexts_touched"]
        ),
        "strict_contexts": delta(ra["strict_contexts"], rb["strict_contexts"]),
        "consistent": delta(ra["consistent"], rb["consistent"]),
        "conflicts": delta(len(ra["conflicts"]), len(rb["conflicts"])),
        "forced_count": delta(len(ra["forced"]), len(rb["forced"])),
    }

    assigned_a = [item["sign"] for item in ra["assigned"]]
    assigned_b = [item["sign"] for item in rb["assigned"]]
    ids_a = {_sign_identity(s) for s in assigned_a}
    ids_b = {_sign_identity(s) for s in assigned_b}
    only_a = [s for s in assigned_a if _sign_identity(s) not in ids_b]
    only_b = [s for s in assigned_b if _sign_identity(s) not in ids_a]
    signs_one_only = {
        f"{side_b}_only": only_b,
        f"{side_a}_only": only_a,
    }

    named_expectations: list[dict[str, Any]] = []
    for expectation in expectations or []:
        claim_id = expectation.get("claim")
        if claim_id not in seen:
            continue
        named_expectations.append(
            {
                "claim": claim_id,
                "source": expectation.get("source"),
                "expectation": expectation.get("expectation"),
                f"{side_a}_tallies": tallies_a.get(claim_id, dict(zero)),
                f"{side_b}_tallies": tallies_b.get(claim_id, dict(zero)),
            }
        )
    if expectations_note is None:
        if named_expectations:
            expectations_note = (
                f"{len(named_expectations)} pre-registered "
                "expectation(s) named and scored above."
            )
        elif len(seen) == 1:
            expectations_note = (
                "No pre-registered expectation exists in "
                "the program's record for the one touched "
                "claim."
            )
        elif seen:
            expectations_note = (
                "No pre-registered expectation exists in "
                f"the program's record for the {len(seen)} "
                "touched claims."
            )
        else:
            expectations_note = (
                "No pre-registered expectation exists in "
                "the program's record for a touched claim; "
                "neither run touches a claim."
            )

    return {
        "artifact": "settling comparison record",
        "label": SETTLING_LABEL,
        "semantics": SEMANTICS_VERSION,
        "runs": [run_a["candidate"], run_b["candidate"]],
        "pins": run_a["pins"],
        "result": {
            "claims_compared": claims_compared,
            "per_claim_divergences": divergences,
            "coverage_deltas": coverage_deltas,
            "signs_assigned_by_one_only": signs_one_only,
            "pre_registered_expectations": named_expectations,
            "pre_registered_expectations_note": expectations_note,
        },
    }


# ---------------------------------------------------------------------------
# The assignment sets of record (§3): the incumbent
# strict-94 set and the full-register set, materialized
# from the canonical anchors register as stored candidate
# records with provenance (C086-14, C086-16).


def build_assignment_sets(state: SettleState) -> dict[str, Any]:
    """The two assignment sets of record, as data. Pure:
    a function of the pinned register state only, so two
    builds over one register state are byte-identical."""
    provenance = {
        "author": (
            "Spec 086 Stage 4 (T403), materialized by "
            "backend/glossa_lab/settling.py"
        ),
        "source": (
            f"{ANCHORS_REL} (the canonical anchors "
            "register), read as assignments under "
            "SETTLING-SEMANTICS.md §3"
        ),
        "register_sha256_raw_bytes": state.pins["anchors_register"][
            "sha256_raw_bytes"
        ],
        "date": "2026-11-01",
    }

    def candidate_record(
        set_id: str, keys: list[str], description: str
    ) -> dict[str, Any]:
        assignments = []
        for key in keys:
            number = int(key[1:])
            assignments.append(
                {
                    "sign": f"{SETTLED_FRAME}:{number}",
                    "value": state.anchors[key].get("reading"),
                }
            )
        return {
            "id": set_id,
            "kind": "assignment_set_of_record",
            "provenance": {**provenance, "description": description},
            "frame": SETTLED_FRAME,
            "assignments": assignments,
        }

    mahadevan_keys = [
        key
        for key in state.anchors
        if key.startswith(FRAME_PREFIXES[SETTLED_FRAME])
    ]
    incumbent_keys = [key for key in mahadevan_keys if key in state.strict]
    out_of_frame = sorted(set(state.anchors) - set(mahadevan_keys))
    return {
        "artifact": "glossa-settle-1 assignment sets of record",
        "label": SETTLING_LABEL,
        "semantics": SEMANTICS_VERSION,
        "register": {
            "path": ANCHORS_REL,
            "sha256_raw_bytes": state.pins["anchors_register"][
                "sha256_raw_bytes"
            ],
            "records": len(state.anchors),
            "strict": len(state.strict),
        },
        "sets": [
            candidate_record(
                "incumbent",
                incumbent_keys,
                "The incumbent strict set read as assignments: "
                "each sign the recomputed strict set holds, "
                "assigned its recorded reading (§3).",
            ),
            candidate_record(
                "full-register",
                mahadevan_keys,
                "The full register read as assignments: every "
                "record of the settled frame, assigned its "
                "recorded reading (§3).",
            ),
        ],
        "out_of_frame_records": out_of_frame,
        "out_of_frame_note": (
            "Register records outside the settled frame "
            "(their frame is unnamed in the anchors file — "
            "UNMEASURED, SETTLING-SEMANTICS.md §2): counted "
            "here, assigned by no set of record in v1."
        ),
    }


def load_assignment_sets(root: Path) -> dict[str, dict[str, Any]]:
    target = Path(root) / ASSIGNMENT_SETS_REL
    if not target.is_file():
        raise SettlingError(
            f"assignment sets of record not found: "
            f"{ASSIGNMENT_SETS_REL} (materialize them with "
            "tools/ledger/run_settling.py materialize-sets)"
        )
    data = json.loads(target.read_text(encoding="utf-8"))
    return {record["id"]: record for record in data.get("sets", [])}


# ---------------------------------------------------------------------------
# Thin write wrappers (the only writers in this module).
# Run records land in the run store and nowhere else
# (C086-16); the assignment sets land at their one path.


def _dump(data: dict[str, Any]) -> bytes:
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    return text.encode("utf-8")


def _write_verified(path: Path, payload: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    if path.read_bytes() != payload:
        raise SettlingError(
            f"write verification failed for {path} — the "
            "bytes on disk differ from the bytes built"
        )
    return path


def write_assignment_sets(root: Path) -> Path:
    state = load_state(root)
    return _write_verified(
        Path(root) / ASSIGNMENT_SETS_REL, _dump(build_assignment_sets(state))
    )


def run_record_filename(record: dict[str, Any]) -> str:
    """The run store's file name for a run record:
    content-addressed from the record's candidate, scope,
    and pins, so a rerun of one scenario overwrites its
    own record and never another's."""
    basis = json.dumps(
        {
            "candidate": record["candidate"],
            "scope": record["scope"],
            "pins": record["pins"],
            "scenario": record.get("scenario"),
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    digest = hashlib.sha256(basis.encode("utf-8")).hexdigest()[:12]
    scenario = record.get("scenario")
    stem = scenario if scenario else record["candidate"]
    return f"{stem}--{digest}.json"


def write_run_record(root: Path, record: dict[str, Any]) -> Path:
    """Write one run record into the run store
    (`glossa-indus/ledger/runs/`) — the only write a
    settling run performs (T403's store discipline)."""
    target = Path(root) / RUN_STORE_REL / run_record_filename(record)
    return _write_verified(target, _dump(record))


__all__ = [
    "SEMANTICS_VERSION",
    "SETTLING_LABEL",
    "SettlingError",
    "SettleState",
    "load_state",
    "evaluate_candidate",
    "run_record",
    "compare_runs",
    "build_assignment_sets",
    "load_assignment_sets",
    "write_assignment_sets",
    "write_run_record",
    "run_record_filename",
]
