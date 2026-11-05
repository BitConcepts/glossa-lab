"""Spec 086 Stage 5 — the layered-map generator (T502).

Implements Point 5 of the winning-combination adoption: the
map is **generated, never made**, from the layers the gate
verifies — ledger → matrix → map (spec.md Point 6: truth
flows one way). The sole entry point is the ledger; the map
derives from the **gated matrix artifact as published** and
from the settling records of record, under the definitions
registered in `glossa-indus/map/DEFINITIONS.md`
(`map-defs v1`), whose machine copy lives below.

Structure (the matrix pattern): `build_map` is a PURE
builder — it computes the artifact bytes in memory and
writes nothing. `write_map` is the thin write wrapper used
only by the generate command (`tools/ledger/generate_map.py`).
Publication is gated publication only
(`gated_publish.publish_map`): candidate → gate → replace
only on ALL PASS. The verification gate carries its own
registered copies of these definitions and recomputes the
artifact by its own route (gate check V5); a change made in
only one copy is exactly the divergence the gate exists to
catch.

Refusals: a source whose hash does not match the ledger's
record, a matrix artifact whose as-of stamp names a
different ledger build than the current ledger, or a
settling record pinned to a different ledger build each
refuse generation with a named error — a defect in the
record is repaired at the source, never generated around.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from glossa_lab import ledger_intake as li

# ---------------------------------------------------------------------------
# Registered definitions — machine copy of
# glossa-indus/map/DEFINITIONS.md (map-defs v1).
# A deliberate change is made in both copies in the same
# motion (DEFINITIONS.md §11); the gate carries a third.

MAP_DEFS_VERSION = "map-defs v1"
MAP_REL_DIR = "glossa-indus/map"
MAP_REL = "glossa-indus/map/map-data.json"
MATRIX_REL = "glossa-indus/matrix/matrix.json"
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
PROVENANCE_REGISTER_REL = "reports/phase108_provenance_register.json"
ASSIGNMENT_SETS_REL = "glossa-indus/ledger/assignment-sets.json"
RUNS_REL_DIR = "glossa-indus/ledger/runs"
COMPARISON_REL = (
    "specs/086-winning-combination-adoption/records/"
    "stage-4-dual-run-comparison.json"
)
SETTLING_CANONICAL_REL = "glossa-indus/ledger/settling-canonical.json"
SETTLE_SEMANTICS_VERSION = "glossa-settle-1"

RELATIONS = ("supports", "opposes", "constrains")
COLUMN_CLASSES = (
    "studies",
    "documents",
    "research_checks",
    "anchors",
    "corpus_texts",
)

# The matrix outcome table (matrix-defs v1 §6), copied:
# no outcome maps to supports in v1.
BEARING_OUTCOMES = {
    "NOT SUPPORTED": "opposes",
    "INCONSISTENT": "opposes",
    "NOT NUMERAL-LIKE": "opposes",
}

# The strict-anchor rule as recorded in the anchors file
# itself (the gate's V6 copies carry the same registration):
# confidence in {HIGH, MEDIUM} AND the Phase-108 register
# category not in the SA-lineage set AND sa_in_chain false.
STRICT_RULE_ID = "strict_sa_independent_hm"
STRICT_CONFIDENCES = ("HIGH", "MEDIUM")
SA_LINEAGE_CATEGORIES = ("SA_DERIVED", "SA_CONFIRMED_ONLY")
PENDING_VALIDATION_STATUS = "pending_non_sa_validation"
PENDING_VALIDATIONS_REASON = (
    "the anchors register records no review dates for the "
    "pending validations, so they appear as a count, not as "
    "dated items (decision Q4)"
)

# The settling layer's two key constructions (DEFINITIONS.md
# §7): the matrix's R4 key is the frame prefix + the number
# as written; glossa-settle-1 §2 zero-pads to three digits.
SETTLE_FRAME_PREFIXES = {"mahadevan": "M"}

# The run records' own label, verbatim (DEFINITIONS.md §8).
SETTLING_LABEL = (
    "Computation over ledgered relations under "
    "glossa-settle-1 semantics. Establishes what the ledger "
    "implies under these rules, not what the script says."
)

# The S-R3 reach statement (DEFINITIONS.md §8): the
# positional-class rule's status, as the run records
# carry it (class_table null in every stored run).
S_R3_NOTE = (
    "no positional-class table exists in the "
    "record; the rule is registered but inert "
    "and reports a determinate zero in every "
    "run record"
)

# The run-result fields the map carries per stored run
# (DEFINITIONS.md §8), in artifact order.
RUN_RESULT_FIELDS = (
    "scope_signs",
    "assigned_count",
    "assigned_share",
    "contexts_touched",
    "strict_contexts",
    "consistent",
    "non_strict_contexts",
    "conflicts",
    "strict_agreement_share",
    "claims_touched",
    "forced",
    "s_r3",
)


class MapBuildError(RuntimeError):
    """Generation refuses: a defect in the ledger, a
    register, or a record of record, named. Nothing is
    written."""


@dataclass
class MapBuild:
    json_bytes: bytes
    output: str
    stats: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Register access (hash-verified, through the ledger's pointers)


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
            raise MapBuildError(
                "source verification failed — the records on disk "
                "are not the records the ledger mirrors:\n  " + named
            )


def _outcome_blocks(
    registers: _Registers, entry: dict[str, Any]
) -> dict[str, list[dict[str, Any]]]:
    """All stored outcome blocks of an entry's records,
    grouped by spec — the matrix-defs §5 R3 scan."""
    blocks_by_spec: dict[str, list[dict[str, Any]]] = {}
    for source in entry.get("sources", []):
        record = registers.record(source["path"], source["claim_id"])
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
    """The governing block: latest dated governs; a block
    without a date sorts before dated blocks; ties break by
    pointer (matrix-defs §5 R3 total order)."""
    return sorted(blocks, key=lambda b: (str(b["date"] or ""), b["pointer"]))[-1]


def _strict_set(root: Path, anchors: dict[str, Any]) -> set[str]:
    """The strict set recomputed under the rule the anchors
    register records (DEFINITIONS.md §3)."""
    register_data = json.loads(
        (root / PROVENANCE_REGISTER_REL).read_text(encoding="utf-8")
    )
    records = register_data.get("records", register_data)
    if not isinstance(records, dict):
        records = {}
    recomputed: set[str] = set()
    for sign, record in anchors.items():
        if (record.get("confidence") or "").upper() not in STRICT_CONFIDENCES:
            continue
        reg = records.get(sign)
        if reg is None:
            continue
        if reg.get("category") in SA_LINEAGE_CATEGORIES:
            continue
        if reg.get("sa_in_chain"):
            continue
        recomputed.add(sign)
    return recomputed


def _falsifier_count(entry: dict[str, Any]) -> int:
    """glossa-settle-1's falsifier counting rule."""
    falsifier = entry.get("falsifier")
    if isinstance(falsifier, list):
        return sum(1 for f in falsifier if isinstance(f, str) and f)
    if isinstance(falsifier, str) and falsifier:
        return 1
    return 0


def _settle_identity(ref: Any) -> Optional[tuple[str, int]]:
    frame, sep, value = str(ref).partition(":")
    if not sep or not frame:
        return None
    try:
        return (frame, int(value))
    except ValueError:
        return None


def _matrix_key(ref: Any) -> Optional[str]:
    """matrix-defs v1 R4's key: the frame prefix + the
    number as written in the sign_ref (no zero-padding)."""
    frame, sep, value = str(ref).partition(":")
    if not sep or frame not in SETTLE_FRAME_PREFIXES:
        return None
    return f"{SETTLE_FRAME_PREFIXES[frame]}{value}"


def _settle_key(ref: Any) -> Optional[str]:
    """glossa-settle-1 §2's key: the frame prefix + the
    number zero-padded to three digits."""
    identity = _settle_identity(ref)
    if identity is None:
        return None
    prefix = SETTLE_FRAME_PREFIXES.get(identity[0])
    if prefix is None:
        return None
    return f"{prefix}{identity[1]:03d}"


def _anchor_summary(
    anchors: dict[str, Any], strict_set: set[str], key: Optional[str]
) -> Optional[dict[str, Any]]:
    if key is None:
        return None
    record = anchors.get(key)
    if record is None:
        return None
    return {
        "key": key,
        "reading": record.get("reading"),
        "confidence": record.get("confidence"),
        "validation_status": record.get("validation_status"),
        "strict": key in strict_set,
    }


# ---------------------------------------------------------------------------
# The builder


def build_map(root: Path) -> MapBuild:
    """Pure builder: compute the map artifact in memory from
    the ledger through the gated matrix and the settling
    records of record. Writes nothing."""
    root = Path(root)
    entries = li.read_ledger(root / li.LEDGER_REL)
    claims = [e for e in entries if e.get("kind") == "claim"]
    annotations = [e for e in entries if e.get("kind") == "annotation"]
    ledger_bytes = (root / li.LEDGER_REL).read_bytes()
    ledger_sha = li.canonical_sha256_bytes(ledger_bytes)

    # -- the gated matrix, as published --------------------------------------
    matrix_path = root / MATRIX_REL
    if not matrix_path.is_file():
        raise MapBuildError(f"matrix artifact not found: {MATRIX_REL}")
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix_stamp = (matrix.get("as_of") or {}).get("ledger_sha256")
    if matrix_stamp != ledger_sha:
        raise MapBuildError(
            f"the published matrix was generated from ledger "
            f"{matrix_stamp}, but the current ledger is "
            f"{ledger_sha} — regenerate and re-publish the "
            "matrix through the gate before building the map "
            "(truth flows one way; the map never builds over "
            "a stale matrix)"
        )
    matrix_sha = li.sha256_file(matrix_path)
    cells = matrix.get("cells", [])
    coverage = matrix.get("coverage", {})

    # -- registers (hash-verified through the ledger's pointers) -------------
    registers = _Registers(root)
    for entry in entries:
        for source in entry.get("sources", []):
            registers.verify(source["path"], source["sha256"])
        if entry.get("kind") == "annotation":
            sidecar = entry.get("sidecar") or {}
            if sidecar.get("path") and sidecar.get("sha256"):
                registers.verify(sidecar["path"], sidecar["sha256"])
    registers.raise_if_mismatched()

    anchors_path = root / ANCHORS_REL
    if not anchors_path.is_file():
        raise MapBuildError(f"anchors register not found: {ANCHORS_REL}")
    anchors_raw = anchors_path.read_bytes()
    anchors = json.loads(anchors_raw.decode("utf-8")).get("anchors", {})
    anchors_raw_sha = hashlib.sha256(anchors_raw).hexdigest()
    strict_set = _strict_set(root, anchors)
    strict_share = (len(strict_set) / len(anchors)) if anchors else 0.0
    pending = sum(
        1
        for r in anchors.values()
        if r.get("validation_status") == PENDING_VALIDATION_STATUS
    )

    blocks_by_claim = {
        e["id"]: _outcome_blocks(registers, e) for e in claims
    }

    # -- header ----------------------------------------------------------------
    by_status = Counter(str(e.get("status")) for e in claims)
    bearing_groups: dict[tuple[str, str, str], dict[str, Any]] = {}
    for entry in claims:
        for spec, blocks in blocks_by_claim[entry["id"]].items():
            governing = _governing(blocks)
            relation = BEARING_OUTCOMES.get(governing["outcome"])
            if relation is None or governing["date"] is None:
                continue
            key = (str(governing["date"]), spec, governing["outcome"])
            group = bearing_groups.setdefault(
                key,
                {
                    "date": str(governing["date"]),
                    "study": spec,
                    "outcome": governing["outcome"],
                    "relation": relation,
                    "claims": [],
                },
            )
            group["claims"].append(entry["id"])
    nearest = sorted(
        bearing_groups.values(), key=lambda g: (g["study"], g["outcome"])
    )
    nearest = sorted(nearest, key=lambda g: g["date"], reverse=True)[:3]
    for group in nearest:
        group["claims"] = sorted(group["claims"])

    as_of = {
        "ledger_sha256": ledger_sha,
        "ledger_lines": len(entries),
        "ledger_date": max(
            (str(e.get("date")) for e in entries), default=None
        ),
        "ledger_schema": li.SCHEMA_VERSION,
        "matrix_defs": "matrix-defs v1",
        "map_defs": MAP_DEFS_VERSION,
        "settle_semantics": SETTLE_SEMANTICS_VERSION,
        "matrix_sha256": matrix_sha,
        "anchors_register_sha256_raw_bytes": anchors_raw_sha,
    }

    header = {
        "claims_total": len(claims),
        "claims_by_status": {k: by_status[k] for k in sorted(by_status)},
        "validated_anchor_share": strict_share,
        "strict_anchor_share": strict_share,
        "anchors_strict": len(strict_set),
        "anchors_total": len(anchors),
        "nearest_dated_items": nearest,
        "pending_validations": {
            "count": pending,
            "reason": PENDING_VALIDATIONS_REASON,
        },
        "as_of": as_of,
    }

    # -- elements + loads -------------------------------------------------------
    elements: list[dict[str, Any]] = [
        {
            "kind": "claim",
            "id": e["id"],
            "statement": e.get("statement"),
            "status": e.get("status"),
            "stage": e.get("stage"),
            "population": e.get("population"),
        }
        for e in claims
    ] + [
        {"kind": c["class"], "id": c["id"]} for c in matrix.get("columns", [])
    ]

    loads: dict[str, dict[str, int]] = {
        row["id"]: {rel: 0 for rel in RELATIONS}
        for row in matrix.get("rows", [])
    }
    cells_by_row: dict[str, list[dict[str, Any]]] = {}
    for cell in cells:
        if cell["row"] in loads:
            loads[cell["row"]][cell["relation"]] += 1
        cells_by_row.setdefault(cell["row"], []).append(cell)

    # -- edges (DEFINITIONS.md §5: citations that carry) -----------------------
    edges: list[dict[str, Any]] = []
    for cell in cells:
        citations = list(cell.get("citations") or [])
        if cell.get("rule") == "R3":
            blocks = blocks_by_claim.get(cell["row"], {}).get(
                cell["column"], []
            )
            governing = _governing(blocks) if blocks else None
            if governing is not None:
                citations = [
                    c
                    for c in citations
                    if c == cell["row"] or c == governing["pointer"]
                ]
        edges.append(
            {
                "from": cell["column"],
                "to": cell["row"],
                "rel": cell["relation"],
                "rule": cell.get("rule"),
                "column_class": cell["column_class"],
                "citations": citations,
            }
        )

    # -- the settling records of record -----------------------------------------
    sets_path = root / ASSIGNMENT_SETS_REL
    if not sets_path.is_file():
        raise MapBuildError(
            f"assignment sets of record not found: {ASSIGNMENT_SETS_REL}"
        )
    assignment_sets = json.loads(sets_path.read_text(encoding="utf-8"))
    as_of["assignment_sets_sha256"] = li.sha256_file(sets_path)

    runs: list[dict[str, Any]] = []
    runs_dir = root / RUNS_REL_DIR
    run_files = sorted(runs_dir.glob("*.json")) if runs_dir.is_dir() else []
    loaded_runs = []
    for run_path in run_files:
        record = json.loads(run_path.read_text(encoding="utf-8"))
        # The map carries scenario evaluation records. Since
        # Spec 089 the run store also holds the other record
        # kinds the run discipline writes there —
        # materialization records (no candidate/scenario) and
        # absence records (no result block) — store records
        # under run-defs v1, not settling evaluations, and
        # never map-carried (Spec 089 Stage 5, the two copies
        # of this enumeration — here and the gate's — filtered
        # in the same motion).
        if not (
            isinstance(record.get("candidate"), str)
            and isinstance(record.get("scenario"), str)
            and isinstance(record.get("result"), dict)
        ):
            continue
        loaded_runs.append((run_path, record))
    # Artifact order: the incumbent first, then the rest by
    # record id — the order the settling panel presents
    # (decision Q7: the panel opens on the stored pair,
    # incumbent vs challenger).
    loaded_runs.sort(
        key=lambda pair: (
            0 if pair[1].get("candidate") == "incumbent" else 1,
            pair[0].stem,
        )
    )
    touched_by_claim: dict[str, list[dict[str, Any]]] = {}
    for run_path, record in loaded_runs:
        pins = record.get("pins") or {}
        pin_sha = (pins.get("ledger") or {}).get("sha256")
        if pin_sha != ledger_sha:
            raise MapBuildError(
                f"run record {run_path.name} is pinned to ledger "
                f"{pin_sha}, but the current ledger is "
                f"{ledger_sha} — a run over a different build "
                "cannot be carried by the map (D-D); re-run "
                "the settling layer over this build first"
            )
        result = record.get("result") or {}
        run_summary = {
            "record": run_path.stem,
            "scenario": record.get("scenario"),
            "candidate": record.get("candidate"),
            "semantics": record.get("semantics"),
            "pins": pins,
        }
        for field_name in RUN_RESULT_FIELDS:
            run_summary[field_name] = result.get(field_name)
        runs.append(run_summary)
        for touched in result.get("claims_touched") or []:
            touched_by_claim.setdefault(touched["claim"], []).append(
                {
                    "candidate": record.get("candidate"),
                    "record": run_path.stem,
                    "via_signs": touched.get("via_signs"),
                    "tallies": touched.get("tallies"),
                    "falsifiers_present": touched.get("falsifiers_present"),
                    "falsifiers_evaluable": touched.get(
                        "falsifiers_evaluable"
                    ),
                }
            )

    comparison_path = root / COMPARISON_REL
    if not comparison_path.is_file():
        raise MapBuildError(f"comparison record not found: {COMPARISON_REL}")
    comparison_record = json.loads(
        comparison_path.read_text(encoding="utf-8")
    )
    comp_pin_sha = (
        (comparison_record.get("pins") or {}).get("ledger") or {}
    ).get("sha256")
    if comp_pin_sha != ledger_sha:
        raise MapBuildError(
            f"the filed comparison record is pinned to ledger "
            f"{comp_pin_sha}, but the current ledger is "
            f"{ledger_sha} — it cannot be carried by the map (D-D)"
        )
    comparison = {
        "record": COMPARISON_REL,
        "sha256": li.sha256_file(comparison_path),
        "result": comparison_record.get("result"),
    }
    as_of["comparison_sha256"] = comparison["sha256"]
    divergent_by_claim = {
        row["claim"]: row.get("divergent")
        for row in (comparison_record.get("result") or {}).get(
            "claims_compared", []
        )
    }

    canonical_path = root / SETTLING_CANONICAL_REL
    if not canonical_path.is_file():
        raise MapBuildError(
            f"settling canonicals not found: {SETTLING_CANONICAL_REL}"
        )
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    canonicals = {
        "record": SETTLING_CANONICAL_REL,
        "sha256": li.sha256_file(canonical_path),
        "scenarios": [
            {
                "id": s.get("id"),
                "title": s.get("title"),
                "expected": s.get("expected"),
            }
            for s in canonical.get("scenarios", [])
        ],
    }
    as_of["settling_canonical_sha256"] = canonicals["sha256"]

    # -- system view --------------------------------------------------------------
    sets_summary = [
        {
            "id": s.get("id"),
            "frame": s.get("frame"),
            "assignments": len(s.get("assignments") or []),
            "provenance": s.get("provenance"),
        }
        for s in assignment_sets.get("sets", [])
    ]
    out_of_frame = list(assignment_sets.get("out_of_frame_records") or [])
    frame = sets_summary[0]["frame"] if sets_summary else None
    in_frame = len(anchors) - len(out_of_frame)
    for item in sets_summary:
        item["frame_scope"] = in_frame
        item["share"] = (
            item["assignments"] / in_frame if in_frame else None
        )
    hotspots = [
        {
            "row": c["row"],
            "column": c["column"],
            "column_class": c["column_class"],
            "rule": c.get("rule"),
            "relation": c["relation"],
        }
        for c in cells
        if c["relation"] == "opposes"
    ]
    by_stage = Counter(
        str(e.get("stage")) for e in claims if e.get("stage")
    )
    by_population = Counter(str(e.get("population")) for e in claims)
    falsifier_gaps = [e["id"] for e in claims if not e.get("falsifier")]
    falsifier_by_population = coverage.get("falsifier_coverage", {})
    system = {
        "sign_inventory": {
            "frame": frame,
            "register_records": len(anchors),
            "out_of_frame_records": out_of_frame,
            "out_of_frame_note": assignment_sets.get("out_of_frame_note"),
            "frame_scope": in_frame,
            "assignment_sets": sets_summary,
            "register": {
                "path": ANCHORS_REL,
                "sha256_raw_bytes": anchors_raw_sha,
            },
        },
        "matrix_coverage": {
            "rows_total": coverage.get("rows_total"),
            "rows_with_cells": coverage.get("rows_with_cells"),
            "empty_rows": coverage.get("empty_rows"),
            "columns_by_class": coverage.get("columns_by_class"),
            "unused_columns": coverage.get("unused_columns"),
            "cells_total": coverage.get("cells_total"),
            "cells_by_relation": coverage.get("cells_by_relation"),
            "cells_by_class": coverage.get("cells_by_class"),
            "conflict_hotspots": hotspots,
            "study_columns_without_cells": (
                (coverage.get("unused_columns") or {}).get("studies", [])
            ),
            "dependency_pairs_not_cells": len(
                coverage.get("dependency_pairs_not_cells") or []
            ),
        },
        "claim_population": {
            "by_status": {k: by_status[k] for k in sorted(by_status)},
            "by_stage": {k: by_stage[k] for k in sorted(by_stage)},
            "no_stage_recorded": sum(
                1 for e in claims if not e.get("stage")
            ),
            "by_population": {
                k: by_population[k] for k in sorted(by_population)
            },
        },
        "falsifier_census": {
            "covered": falsifier_by_population.get("covered"),
            "total": falsifier_by_population.get("total"),
            "by_population": falsifier_by_population.get("by_population"),
            "gap_claims": falsifier_gaps,
        },
        "aee_state_census": {
            "with_state": sum(
                1 for e in claims if e.get("aee_state") is not None
            ),
            "without_state": sum(
                1 for e in claims if e.get("aee_state") is None
            ),
            "total": len(claims),
        },
        "unresolved": {
            "sign_mentions": coverage.get("unresolved_sign_mentions"),
            "sign_refs_without_anchor_record": coverage.get(
                "sign_refs_without_anchor_record"
            ),
        },
        "sign_sign_block_summary": {
            "node_count": (matrix.get("sign_sign_block") or {}).get(
                "node_count"
            ),
            "edge_count": (matrix.get("sign_sign_block") or {}).get(
                "edge_count"
            ),
            "edges_emitted": (matrix.get("sign_sign_block") or {}).get(
                "edges_emitted"
            ),
            "community_count": (
                matrix.get("sign_sign_block") or {}
            ).get("community_count"),
            "corpus_sha256": (
                (matrix.get("sign_sign_block") or {}).get("source") or {}
            ).get("corpus_sha256"),
        },
    }

    # -- per-claim records ---------------------------------------------------------
    annotations_by_target: dict[str, list[dict[str, Any]]] = {}
    for annotation in annotations:
        target = annotation.get("target_claim_id")
        if target:
            annotations_by_target.setdefault(target, []).append(
                {
                    "id": annotation.get("id"),
                    "canonical_claim_id": annotation.get(
                        "canonical_claim_id"
                    ),
                    "sidecar": annotation.get("sidecar"),
                    "bearing": annotation.get("bearing"),
                }
            )

    columns_by_class = coverage.get("columns_by_class") or {}
    claim_records: dict[str, Any] = {}
    for entry in claims:
        eid = entry["id"]
        row_cells = cells_by_row.get(eid, [])
        touched = touched_by_claim.get(eid)
        bearing = None
        if touched:
            bearing = {
                "runs": touched,
                "divergent": divergent_by_claim.get(eid),
            }
        evaluable = (
            touched[0].get("falsifiers_evaluable") if touched else None
        )
        sign_records = []
        for ref in entry.get("sign_refs") or []:
            m_key = _matrix_key(ref)
            s_key = _settle_key(ref)
            matrix_record = _anchor_summary(anchors, strict_set, m_key)
            settle_record = _anchor_summary(anchors, strict_set, s_key)
            sign_records.append(
                {
                    "sign_ref": ref,
                    "matrix_key": m_key,
                    "matrix_record": matrix_record,
                    "settle_key": s_key,
                    "settle_record": settle_record,
                    "divergence": (matrix_record is None)
                    != (settle_record is None)
                    or (
                        matrix_record is not None
                        and settle_record is not None
                        and m_key != s_key
                    ),
                }
            )
        sor = next(
            (
                s
                for s in entry.get("sources", [])
                if s.get("role") == "source_of_record"
            ),
            None,
        )
        claim_records[eid] = {
            "id": eid,
            "statement": entry.get("statement"),
            "status": entry.get("status"),
            "stage": entry.get("stage"),
            "population": entry.get("population"),
            "author": entry.get("author"),
            "author_kind": entry.get("author_kind"),
            "as_of": entry.get("as_of"),
            "date": entry.get("date"),
            "falsifier": entry.get("falsifier"),
            "falsifier_counts": {
                "present": _falsifier_count(entry),
                "evaluable": evaluable,
            },
            "does_not_establish": entry.get("does_not_establish"),
            "aee_state": entry.get("aee_state"),
            "displayed_score": (
                {"state": "recorded", "aee_state": entry.get("aee_state")}
                if entry.get("aee_state") is not None
                else {"state": "empty"}
            ),
            "sign_refs": entry.get("sign_refs") or [],
            "sources": entry.get("sources") or [],
            "matrix_row": {
                "cells": row_cells,
                "empty": not row_cells,
            },
            "settling_bearing": bearing,
            "annotations": annotations_by_target.get(eid, []),
            "evidence": {
                "column_summary": {
                    cls: {
                        "columns": columns_by_class.get(cls, 0),
                        "cells": sum(
                            1
                            for c in row_cells
                            if c["column_class"] == cls
                        ),
                    }
                    for cls in COLUMN_CLASSES
                },
                "source_document": sor,
                "sign_records": sign_records,
            },
        }

    settling = {
        "label": SETTLING_LABEL,
        "semantics": SETTLE_SEMANTICS_VERSION,
        "assignment_sets": {
            "record": ASSIGNMENT_SETS_REL,
            "sha256": as_of["assignment_sets_sha256"],
            "register": assignment_sets.get("register"),
            "sets": sets_summary,
            "out_of_frame_records": out_of_frame,
            "out_of_frame_note": assignment_sets.get("out_of_frame_note"),
        },
        "runs": runs,
        "comparison": comparison,
        "canonicals": canonicals,
        "reach": {
            "claims_with_sign_refs": sum(
                1 for e in claims if e.get("sign_refs")
            ),
            "claims_total": len(claims),
            "claims_untouched_by_any_run": len(claims)
            - len(touched_by_claim),
            "s_r3": {
                "status": "UNMEASURED",
                "class_table": None,
                "note": S_R3_NOTE,
            },
        },
    }

    map_data = {
        "artifact": "glossa-indus layered map data",
        "generated_from": (
            f"{li.LEDGER_REL} through {MATRIX_REL} and the "
            "settling records of record"
        ),
        "generated_by": (
            "tools/ledger/generate_map.py "
            "(backend/glossa_lab/map_generate.py)"
        ),
        "header": header,
        "elements": elements,
        "edges": edges,
        "loads": loads,
        "matrix": {
            "rows": matrix.get("rows"),
            "columns": matrix.get("columns"),
            "cells": cells,
            "coverage": coverage,
            "sign_sign_block": matrix.get("sign_sign_block"),
        },
        "system": system,
        "claims": claim_records,
        "settling": settling,
    }
    json_bytes = (
        json.dumps(map_data, ensure_ascii=False, indent=1).encode("utf-8")
        + b"\n"
    )

    output = _render_output(map_data, as_of)
    stats = {
        "elements": len(elements),
        "edges": len(edges),
        "claims": len(claims),
        "ledger_sha256": ledger_sha,
    }
    return MapBuild(json_bytes=json_bytes, output=output, stats=stats)


def _render_output(map_data: dict[str, Any], as_of: dict[str, Any]) -> str:
    header = map_data["header"]
    system = map_data["system"]
    lines = [
        "Map generation — glossa-indus layered map (Spec 086, T502)",
        f"definitions: {MAP_DEFS_VERSION}; ledger schema: "
        f"{as_of['ledger_schema']}; settling semantics: "
        f"{as_of['settle_semantics']}",
        f"ledger sha256: {as_of['ledger_sha256']}",
        f"ledger lines: {as_of['ledger_lines']}; "
        f"ledger date: {as_of['ledger_date']}",
        f"claims: {header['claims_total']}; elements: "
        f"{len(map_data['elements'])}; edges: "
        f"{len(map_data['edges'])} (one per matrix cell)",
        f"validated-anchor share: {header['anchors_strict']} of "
        f"{header['anchors_total']} strict = "
        f"{header['validated_anchor_share']:.4f}",
        "nearest dated items: "
        + "; ".join(
            f"{g['date']} study {g['study']} ({g['outcome']}) — "
            f"{len(g['claims'])} claim(s)"
            for g in header["nearest_dated_items"]
        ),
        f"falsifier census: {system['falsifier_census']['covered']} "
        f"of {system['falsifier_census']['total']} claims carry a "
        f"falsifier; {len(system['falsifier_census']['gap_claims'])} "
        "gaps named",
        f"settling runs carried: {len(map_data['settling']['runs'])}; "
        f"claims carrying sign_refs: "
        f"{map_data['settling']['reach']['claims_with_sign_refs']}",
    ]
    return "\n".join(lines) + "\n"


def write_map(
    root: Path, out_dir: Optional[Path] = None
) -> dict[str, Any]:
    """Thin wrapper over the pure builder: build, write the
    artifact with pinned LF bytes, read back and verify.
    (Direct write for local use; publication to the tree is
    gated publication — `gated_publish.publish_map`.)"""
    root = Path(root)
    build = build_map(root)
    out = Path(out_dir) if out_dir else (root / MAP_REL_DIR)
    out.mkdir(parents=True, exist_ok=True)
    target = out / "map-data.json"
    target.write_bytes(build.json_bytes)
    read_back = target.read_bytes()
    if read_back != build.json_bytes:
        raise MapBuildError(
            f"write verification failed for {target}: read-back "
            "bytes differ from the built bytes"
        )
    return {
        "build": build,
        "written": {
            "map-data.json": {
                "path": str(target),
                "sha256": li.canonical_sha256_bytes(read_back),
                "bytes": len(read_back),
            }
        },
    }
