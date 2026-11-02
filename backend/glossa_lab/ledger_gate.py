"""Spec 086 Stage 3 — the verification gate over the
ledger → matrix → map chain (spec.md Point 4).

The gate recomputes every downstream layer from the ledger
by an **independent route**: the matrix definitions below are
the gate's own registered copies of `matrix-defs v1`
(`glossa-indus/matrix/DEFINITIONS.md`), deliberately not
imported from the generator (`matrix_generate.py`). A
deliberate definitions change is made in all copies in the
same motion (DEFINITIONS.md §12); a change made in only one
copy is exactly the divergence this gate exists to catch.

Check classes (spec.md Point 4(c)): V1 ledger validity
(including the recorded-source-hash arm: every `sources[]`
and annotation-sidecar hash recorded in the ledger verifies
against the canonical hash of the named file — the Stage 1
gap this stage closes), V2 count equivalence, V3 matrix
recomputation, V4 relation-carrying citations (tie rules
T1–T4 plus the numeric arm of harmonization adoption 3,
item 2), V5 map recomputation, V6 anchor shares, V7 lossless
regeneration (checked mode, `--regen`), V8 settling
canonicals (Stage 4: the canonical scenarios and comparison
registered in `glossa-indus/ledger/settling-canonical.json`
reproduced under the gate's own glossa-settle-1 route — the
settle definitions below are the gate's registered copies,
not imported from the engine — plus the settling layer's
scenario/verdict separation check), V9 no write path.

**The gate never writes.** It calls only pure builders and
read paths; it imports no write entry point (V9 audits this
in the gate's own source). Publication lives in
`gated_publish.py`, which writes candidates, runs this gate
against them, and replaces the published artifacts only on
ALL PASS (C086-11).
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from glossa_lab import ledger_intake as li

# ---------------------------------------------------------------------------
# Registered definitions — the gate's own copies of
# matrix-defs v1 (glossa-indus/matrix/DEFINITIONS.md).
# NOT imported from the generator: this is the independent
# recomputation route (spec.md Point 4, V3).

GATE_MATRIX_DEFS_VERSION = "matrix-defs v1"
MATRIX_REL_DIR = "glossa-indus/matrix"
MAP_REL = "glossa-indus/map/map-data.json"
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
PROVENANCE_REGISTER_REL = "reports/phase108_provenance_register.json"
CORPUS_REL = "glossa-corpus/indus/exports/indus_research.jsonl"

RELATIONS = ("supports", "opposes", "constrains")
COLUMN_CLASSES = (
    "studies",
    "documents",
    "research_checks",
    "anchors",
    "corpus_texts",
)
RULES = {
    "R1": "evidence instance (documents, supports)",
    "R2": "bundle evidence direction (documents, per stored direction)",
    "R3": "study outcome (studies, per the outcome table)",
    "R4": "anchor assignment (anchors, constrains)",
    "R5": "research-check verdict (research checks; verdict table empty in v1)",
    "R6": "settling instrument (constrains; instrument register empty in v1)",
}
DIRECTION_RELATIONS = {
    "supports": "supports",
    "opposes": "opposes",
    "constrains": "constrains",
}
# The outcome table (DEFINITIONS.md §6): no outcome maps to
# supports in v1; an unexecuted or null outcome carries
# neither relation.
BEARING_OUTCOMES = {
    "NOT SUPPORTED": "opposes",
    "INCONSISTENT": "opposes",
    "NOT NUMERAL-LIKE": "opposes",
}
VERDICT_RELATIONS: dict[str, str] = {}
COOCCURRENCE_PARAMS = {"window": 2, "min_freq": 3, "min_edge_weight": 2}
COOCCURRENCE_PIPELINE = "glossa_lab.pipelines.cooccurrence.build_cooccurrence_network"

# The strict-anchor rule as recorded in the anchors file
# itself (metadata.spec029_phase_h_annotation.strict_set_rule,
# Spec 029 Phase H / D-A): confidence in {HIGH, MEDIUM} AND
# the Phase-108 register category not in the SA-lineage set
# AND the register's sa_in_chain is false.
STRICT_RULE_ID = "strict_sa_independent_hm"
STRICT_CONFIDENCES = ("HIGH", "MEDIUM")
SA_LINEAGE_CATEGORIES = ("SA_DERIVED", "SA_CONFIRMED_ONLY")

# ---------------------------------------------------------------------------
# Registered definitions — the gate's own copies of
# glossa-settle-1 (`glossa-indus/ledger/SETTLING-SEMANTICS.md`),
# for V8. NOT imported from the engine (`settling.py`):
# the same independent-route discipline as the matrix
# definitions above. A deliberate semantics change is made
# in all copies in the same motion (a new semantics
# version); a change in only one copy is the divergence
# V8 exists to catch.

SETTLE_SEMANTICS_VERSION = "glossa-settle-1"
SETTLING_CANONICAL_REL = "glossa-indus/ledger/settling-canonical.json"
# Sign identity is by (frame, number) under glossa-settle-1
# §2 — the register key is the frame's prefix plus the
# number zero-padded to three digits. This is the settling
# identity rule, deliberately NOT matrix-defs v1 R4's
# literal key construction (the divergence is registered
# in the semantics and stands).
SETTLE_FRAME_PREFIXES = {"mahadevan": "M"}
# The outcome table (SETTLING-SEMANTICS.md §5, carrying
# matrix-defs v1 §6): tallies are keyed supporting /
# opposing / constraining; no recorded outcome maps to
# supporting in v1.
SETTLE_BEARING_OUTCOMES = {
    "NOT SUPPORTED": "opposing",
    "INCONSISTENT": "opposing",
    "NOT NUMERAL-LIKE": "opposing",
}
SETTLE_TALLY_KEYS = ("supporting", "opposing", "constraining")

# The numeric arm's registered comparator vocabulary
# (harmonization adoption 3, item 2 — the Atlas's
# claim.measurement shape: value / comparator / bound).
NUMERIC_COMPARATORS = ("<=", ">=", "=", "in")

# ---------------------------------------------------------------------------
# Registered definitions — the gate's own copies of
# map-defs v1 (glossa-indus/map/DEFINITIONS.md), for V5's
# map recomputation (Stage 5). NOT imported from the
# builder (map_generate.py): the same independent-route
# discipline as the matrix and settling definitions above.
# A deliberate definitions change is made in all copies in
# the same motion (DEFINITIONS.md §11).

GATE_MAP_DEFS_VERSION = "map-defs v1"
ASSIGNMENT_SETS_REL = "glossa-indus/ledger/assignment-sets.json"
RUNS_REL_DIR = "glossa-indus/ledger/runs"
COMPARISON_REL = (
    "specs/086-winning-combination-adoption/records/"
    "stage-4-dual-run-comparison.json"
)
PENDING_VALIDATION_STATUS = "pending_non_sa_validation"
PENDING_VALIDATIONS_REASON = (
    "the anchors register records no review dates for the "
    "pending validations, so they appear as a count, not as "
    "dated items (decision Q4)"
)
SETTLING_LABEL = (
    "Computation over ledgered relations under "
    "glossa-settle-1 semantics. Establishes what the ledger "
    "implies under these rules, not what the script says."
)
MAP_RUN_RESULT_FIELDS = (
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
MAP_S_R3_NOTE = (
    "no positional-class table exists in the "
    "record; the rule is registered but inert "
    "and reports a determinate zero in every "
    "run record"
)

WRITE_ENTRY_POINTS = ("append_entry", "write_ledger", "write_matrix")
REGISTERED_WRITERS = {
    "backend/glossa_lab/matrix_generate.py",
    "backend/glossa_lab/map_generate.py",
    "backend/glossa_lab/gated_publish.py",
    "tools/ledger/generate_matrix.py",
    "tools/ledger/generate_map.py",
}
ARTIFACT_PATH_PATTERNS = (
    re.compile(r"glossa-indus/matrix"),
    re.compile(r"glossa-indus/map"),
    re.compile(r"(?<![\w.-])matrix\.json(?![\w-])"),
    re.compile(r"(?<![\w.-])matrix\.md(?![\w-])"),
    re.compile(r"(?<![\w.-])map-data\.json(?![\w-])"),
)


# ---------------------------------------------------------------------------
# Result model


@dataclass
class Check:
    name: str
    status: str  # "PASS" | "FAIL" | "NOT-RUN"
    evidence: list[str] = field(default_factory=list)


@dataclass
class GateReport:
    root: Path
    mode: str
    checks: list[Check] = field(default_factory=list)
    header: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.status != "FAIL" for c in self.checks)

    def counts(self) -> dict[str, int]:
        out = {"PASS": 0, "FAIL": 0, "NOT-RUN": 0}
        for c in self.checks:
            out[c.status] = out.get(c.status, 0) + 1
        return out

    def render(self) -> str:
        lines = list(self.header)
        lines.append("checks:")
        for c in self.checks:
            lines.append(f"{c.status} {c.name}")
            for ev in c.evidence:
                lines.append(f"  {ev}")
        n = self.counts()
        lines.append(
            f"summary: {n['PASS']} PASS / {n['FAIL']} FAIL / "
            f"{n['NOT-RUN']} NOT-RUN"
        )
        lines.append("RESULT: " + ("PASS" if self.ok else "FAIL"))
        return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Register access for the gate's own derivation (hash-verified
# through the ledger's pointers, like the generator's route
# but independently coded here).


def _records_of(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("claims"), list):
            return [r for r in data["claims"] if isinstance(r, dict)]
        return [r for r in data.values() if isinstance(r, dict)]
    return []


class _GateRegisters:
    """Source records named by ledger entries, parsed only
    after their canonical hash verifies. Mismatches are
    collected, not raised, so the gate can name them under
    the check classes they belong to."""

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

    def records(self, rel_path: str) -> list[dict[str, Any]]:
        data = self._parsed.get(rel_path)
        return _records_of(data) if data is not None else []


def _load_registers(root: Path, entries: list[dict[str, Any]]) -> _GateRegisters:
    registers = _GateRegisters(root)
    for entry in entries:
        for source in entry.get("sources", []):
            registers.verify(source["path"], source["sha256"])
        if entry.get("kind") == "annotation":
            sidecar = entry.get("sidecar") or {}
            if sidecar.get("path") and sidecar.get("sha256"):
                registers.verify(sidecar["path"], sidecar["sha256"])
    return registers


def _source_record(
    registers: _GateRegisters, entry: dict[str, Any], role: str
) -> Optional[dict[str, Any]]:
    for source in entry.get("sources", []):
        if source.get("role") == role:
            return registers.record(source["path"], source["claim_id"])
    return None


def _outcome_blocks(
    registers: _GateRegisters, entry: dict[str, Any]
) -> dict[str, list[dict[str, Any]]]:
    """All stored outcome blocks of an entry's records,
    grouped by spec: {spec: [{outcome, date, pointer}]} —
    the gate's own scan, per DEFINITIONS.md §5 R3."""
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
    pointer (DEFINITIONS.md §5 R3 total order)."""
    return sorted(blocks, key=lambda b: (str(b["date"] or ""), b["pointer"]))[-1]


# ---------------------------------------------------------------------------
# The gate's independent matrix recomputation (V3's route,
# and the derivation V4's tie rules read from).


@dataclass
class _Derivation:
    rows: list[dict[str, Any]]
    columns: list[dict[str, Any]]
    cells: list[dict[str, Any]]
    coverage: dict[str, Any]
    as_of: dict[str, Any]
    sign_block: Optional[dict[str, Any]]
    registers: _GateRegisters
    blocks: dict[str, dict[str, list[dict[str, Any]]]]  # entry id -> spec -> blocks


def _derive(
    root: Path,
    entries: list[dict[str, Any]],
    *,
    with_sign_block: bool,
) -> _Derivation:
    claims = [e for e in entries if e.get("kind") == "claim"]
    annotations = [e for e in entries if e.get("kind") == "annotation"]
    claim_ids = {e["id"] for e in claims}
    registers = _load_registers(root, entries)

    anchors_path = root / ANCHORS_REL
    anchors: dict[str, Any] = {}
    if anchors_path.is_file():
        anchors = json.loads(
            anchors_path.read_text(encoding="utf-8")
        ).get("anchors", {})

    cells: dict[tuple[str, str, str], dict[str, Any]] = {}
    study_columns: set[str] = set()
    document_columns: set[str] = set()
    non_bearing: list[dict[str, Any]] = []
    unresolved_anchor_refs: list[dict[str, Any]] = []
    blocks_by_entry: dict[str, dict[str, list[dict[str, Any]]]] = {}
    derivation_conflicts: list[str] = []

    def put(cell: dict[str, Any]) -> None:
        key = (cell["row"], cell["column_class"], cell["column"])
        existing = cells.get(key)
        if existing is None:
            cells[key] = cell
            return
        if (
            existing["relation"] != cell["relation"]
            or existing["rule"] != cell["rule"]
        ):
            derivation_conflicts.append(
                f"conflicting derivations for ({cell['row']} x "
                f"{cell['column']}): {existing['rule']}/"
                f"{existing['relation']} vs {cell['rule']}/"
                f"{cell['relation']}"
            )
            return
        for citation in cell["citations"]:
            if citation not in existing["citations"]:
                existing["citations"].append(citation)

    for entry in claims:
        eid = entry["id"]
        sor = _source_record(registers, entry, "source_of_record")

        # R1 — evidence instances (extracted population).
        if entry.get("population") == "extracted" and sor is not None:
            for instance in sor.get("evidence_instances") or []:
                if not isinstance(instance, dict):
                    continue
                doc = instance.get("source_document_id")
                inst_id = instance.get("claim_id")
                if not doc:
                    continue
                document_columns.add(str(doc))
                put(
                    {
                        "row": eid,
                        "column": str(doc),
                        "column_class": "documents",
                        "relation": "supports",
                        "rule": "R1",
                        "citations": [eid, str(inst_id)] if inst_id else [eid],
                    }
                )

        # R2 — bundle evidence direction (bundle population).
        if entry.get("population") == "bundle" and sor is not None:
            by_ref: dict[str, dict[str, Any]] = {}
            for item in sor.get("evidence") or []:
                if not isinstance(item, dict) or not item.get("ref"):
                    continue
                ref = str(item["ref"])
                relation = DIRECTION_RELATIONS.get(str(item.get("direction")))
                if relation is None:
                    derivation_conflicts.append(
                        f"{eid}: evidence item {ref} carries "
                        f"unregistered direction {item.get('direction')!r}"
                    )
                    continue
                document_columns.add(ref)
                cell = by_ref.get(ref)
                if cell is None:
                    by_ref[ref] = {
                        "row": eid,
                        "column": ref,
                        "column_class": "documents",
                        "relation": relation,
                        "rule": "R2",
                        "citations": [eid, ref],
                    }
                elif cell["relation"] != relation:
                    derivation_conflicts.append(
                        f"{eid}: conflicting stored directions for "
                        f"evidence ref {ref}"
                    )
            for cell in by_ref.values():
                put(cell)

        # R3 — study outcomes (any population).
        blocks_by_spec = _outcome_blocks(registers, entry)
        blocks_by_entry[eid] = blocks_by_spec
        for spec in sorted(blocks_by_spec):
            study_columns.add(spec)
            blocks = blocks_by_spec[spec]
            ordered = sorted(
                blocks, key=lambda b: (str(b["date"] or ""), b["pointer"])
            )
            governing = ordered[-1]
            relation = BEARING_OUTCOMES.get(governing["outcome"])
            if relation is not None:
                put(
                    {
                        "row": eid,
                        "column": spec,
                        "column_class": "studies",
                        "relation": relation,
                        "rule": "R3",
                        "citations": [eid] + [b["pointer"] for b in ordered],
                    }
                )
                for block in ordered[:-1]:
                    non_bearing.append(
                        {
                            "row": eid,
                            "study": spec,
                            "outcome": block["outcome"],
                            "date": block["date"],
                            "pointer": block["pointer"],
                            "reason": (
                                "superseded by a later outcome block "
                                "from the same study"
                            ),
                        }
                    )
            else:
                for block in ordered:
                    non_bearing.append(
                        {
                            "row": eid,
                            "study": spec,
                            "outcome": block["outcome"],
                            "date": block["date"],
                            "pointer": block["pointer"],
                            "reason": (
                                "governing outcome is non-bearing"
                                if block is governing
                                else "superseded by a later outcome "
                                "block from the same study"
                            ),
                        }
                    )

        # R4 — anchor assignment (constrains).
        for sign_ref in entry.get("sign_refs") or []:
            frame, _, value = str(sign_ref).partition(":")
            anchor_key = f"M{value}" if frame == "mahadevan" else None
            anchor = anchors.get(anchor_key) if anchor_key else None
            if anchor is not None and anchor.get("reading"):
                put(
                    {
                        "row": eid,
                        "column": anchor_key,
                        "column_class": "anchors",
                        "relation": "constrains",
                        "rule": "R4",
                        "citations": [eid, anchor_key],
                    }
                )
            else:
                if frame != "mahadevan":
                    reason = (
                        f"frame {frame!r} has no anchor-register "
                        "mapping in matrix-defs v1"
                    )
                elif anchor is None:
                    reason = "no anchor record under this key"
                else:
                    reason = "anchor record carries no recorded reading"
                unresolved_anchor_refs.append(
                    {"row": eid, "sign_ref": str(sign_ref), "reason": reason}
                )

    # R5 — research-check verdicts (verdict table empty in v1).
    research_check_columns: set[str] = set()
    for annotation in annotations:
        sidecar = (annotation.get("sidecar") or {}).get("path")
        if not sidecar:
            continue
        research_check_columns.add(str(sidecar))
        verdict = (annotation.get("bearing") or {}).get("verdict")
        relation = VERDICT_RELATIONS.get(verdict) if verdict else None
        target = annotation.get("canonical_claim_id")
        if relation is not None and target in claim_ids:
            put(
                {
                    "row": str(target),
                    "column": str(sidecar),
                    "column_class": "research_checks",
                    "relation": relation,
                    "rule": "R5",
                    "citations": [str(target), annotation["id"]],
                }
            )

    # R6 — settling instruments: register empty in v1.

    cell_list = sorted(
        cells.values(), key=lambda c: (c["row"], c["column_class"], c["column"])
    )
    rows_with_cells = {c["row"] for c in cell_list}
    columns_by_class: dict[str, list[str]] = {
        "studies": sorted(study_columns),
        "documents": sorted(document_columns),
        "research_checks": sorted(research_check_columns),
        "anchors": sorted(anchors.keys()),
        "corpus_texts": [],
    }
    borne = {(c["column_class"], c["column"]) for c in cell_list}
    unused_columns = {
        cls: [c for c in cols if (cls, c) not in borne]
        for cls, cols in columns_by_class.items()
    }
    falsifier_by_population: dict[str, dict[str, int]] = {}
    for entry in claims:
        bucket = falsifier_by_population.setdefault(
            str(entry.get("population")), {"covered": 0, "total": 0}
        )
        bucket["total"] += 1
        if entry.get("falsifier"):
            bucket["covered"] += 1
    falsifier_coverage = {
        "covered": sum(b["covered"] for b in falsifier_by_population.values()),
        "total": len(claims),
        "by_population": falsifier_by_population,
    }
    unresolved_mentions: list[dict[str, Any]] = []
    seen_store_records: set[tuple[str, str]] = set()
    for entry in claims:
        if entry.get("population") != "extracted":
            continue
        for source in entry.get("sources", []):
            for record in registers.records(source["path"]):
                marker = (source["path"], str(record.get("claim_id")))
                if marker in seen_store_records:
                    continue
                seen_store_records.add(marker)
                for mention in record.get("signs_involved") or []:
                    unresolved_mentions.append(
                        {
                            "record": str(record.get("claim_id")),
                            "source": source["path"],
                            "mention": str(mention),
                        }
                    )
    unresolved_mentions.sort(key=lambda m: (m["record"], m["mention"]))
    dependency_pairs: list[dict[str, str]] = []
    for entry in claims:
        spec_prefix = (
            entry["id"].rsplit("/", 1)[0] if "/" in entry["id"] else None
        )
        for ref in entry.get("evidence_refs") or []:
            target = None
            if ref in claim_ids:
                target = ref
            elif spec_prefix and f"{spec_prefix}/{ref}" in claim_ids:
                target = f"{spec_prefix}/{ref}"
            if target and target != entry["id"]:
                dependency_pairs.append({"from": entry["id"], "to": target})
    dependency_pairs.sort(key=lambda p: (p["from"], p["to"]))
    non_bearing.sort(
        key=lambda b: (b["row"], b["study"], str(b["date"] or ""), b["pointer"])
    )
    unresolved_anchor_refs.sort(key=lambda u: (u["row"], u["sign_ref"]))

    coverage = {
        "rows_total": len(claims),
        "rows_with_cells": len(rows_with_cells),
        "empty_rows": [e["id"] for e in claims if e["id"] not in rows_with_cells],
        "columns_by_class": {
            cls: len(cols) for cls, cols in columns_by_class.items()
        },
        "unused_columns": unused_columns,
        "cells_total": len(cell_list),
        "cells_by_relation": {
            rel: sum(1 for c in cell_list if c["relation"] == rel)
            for rel in RELATIONS
        },
        "cells_by_class": {
            cls: sum(1 for c in cell_list if c["column_class"] == cls)
            for cls in COLUMN_CLASSES
        },
        "falsifier_coverage": falsifier_coverage,
        "unresolved_sign_mentions": unresolved_mentions,
        "sign_refs_without_anchor_record": unresolved_anchor_refs,
        "study_outcome_blocks_not_bearing": non_bearing,
        "dependency_pairs_not_cells": dependency_pairs,
    }
    if derivation_conflicts:
        coverage["derivation_conflicts"] = sorted(set(derivation_conflicts))

    sign_block = _sign_sign_block(root) if with_sign_block else None

    ledger_bytes = (root / li.LEDGER_REL).read_bytes()
    as_of = {
        "ledger_sha256": li.canonical_sha256_bytes(ledger_bytes),
        "ledger_lines": len(entries),
        "ledger_date": max((str(e.get("date")) for e in entries), default=None),
        "ledger_schema": li.SCHEMA_VERSION,
        "matrix_defs": GATE_MATRIX_DEFS_VERSION,
    }
    return _Derivation(
        rows=[
            {
                "id": e["id"],
                "population": e.get("population"),
                "status": e.get("status"),
                "stage": e.get("stage"),
            }
            for e in claims
        ],
        columns=[
            {"id": column, "class": cls}
            for cls in COLUMN_CLASSES
            for column in columns_by_class[cls]
        ],
        cells=cell_list,
        coverage=coverage,
        as_of=as_of,
        sign_block=sign_block,
        registers=registers,
        blocks=blocks_by_entry,
    )


def _sign_sign_block(root: Path) -> dict[str, Any]:
    """The gate's own run of the registered co-occurrence
    pipeline over the corpus snapshot, with the gate's
    registered parameters (DEFINITIONS.md §8)."""
    corpus_path = root / CORPUS_REL
    corpus_hash = li.sha256_file(corpus_path)

    from glossa_lab.data import indus_corpus_v2
    from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network

    status = indus_corpus_v2.corpus_status()
    tier = str(status.get("tier", ""))
    if not tier.startswith("real-corpus"):
        raise RuntimeError(
            f"corpus loader tier is {tier!r}, not the real corpus"
        )
    sequences = indus_corpus_v2.load_corpus()
    symbols = [f"sign-int:{n}" for seq in sequences for n in seq]
    network = build_cooccurrence_network(symbols, **COOCCURRENCE_PARAMS)
    return {
        "source": {
            "pipeline": COOCCURRENCE_PIPELINE,
            "parameters": dict(COOCCURRENCE_PARAMS),
            "parameter_note": (
                "window/min_freq/min_edge_weight as at the "
                "analyze_script.py §6 call site; remaining "
                "parameters at the pipeline's defaults, "
                "including its node selection and edge "
                "emission caps — the block is the pipeline "
                "output as emitted"
            ),
            "corpus": CORPUS_REL,
            "corpus_sha256": corpus_hash,
            "corpus_tier": tier,
            "sequences": len(sequences),
            "sign_tokens": len(symbols),
            "sign_id_form": (
                "sign-int:<n> — the corpus loader's integer sign "
                "ids, not relabeled with a frame name (the loader "
                "converts to Mahadevan integers where its "
                "crosswalk maps and otherwise preserves "
                "source-frame integers)"
            ),
        },
        "node_count": network["node_count"],
        "edge_count": network["edge_count"],
        "edges_emitted": len(network["edges"]),
        "community_count": network["community_count"],
        "nodes": network["nodes"],
        "edges": network["edges"],
        "communities": network["communities"],
    }


# ---------------------------------------------------------------------------
# V4 — relation-carrying citations (tie rules T1–T4 + the
# numeric arm)


def numeric_arm_check(
    relation: str, value: float, comparator: str, bound: Any
) -> Optional[str]:
    """The numeric arm (adoption 3, item 2): where a cited
    evidence entry carries a measurement and the citing claim
    carries a machine-readable bound, a supports citation
    whose value violates the bound is refused, and the
    symmetric opposes case. Returns a failure reason, or
    None when the citation carries its relation."""
    if comparator == "<=":
        satisfies = value <= bound
    elif comparator == ">=":
        satisfies = value >= bound
    elif comparator == "=":
        satisfies = value == bound
    elif comparator == "in":
        lo, hi = bound
        satisfies = lo <= value <= hi
    else:
        return f"unregistered numeric comparator {comparator!r}"
    if relation == "supports" and not satisfies:
        return (
            f"measurement value {value} violates the claim's bound "
            f"{comparator} {bound} — a supports citation the number "
            "does not carry"
        )
    if relation == "opposes" and satisfies:
        return (
            f"measurement value {value} satisfies the claim's bound "
            f"{comparator} {bound} — an opposes citation the number "
            "does not carry"
        )
    return None


def _measurement_shape(record: Any) -> Optional[dict[str, Any]]:
    """A record's machine-readable measurement value, in
    the registered shape {value, comparator, bound} — the
    cited evidence entry carries the value (and may carry
    the whole shape)."""
    if not isinstance(record, dict):
        return None
    m = record.get("measurement")
    if isinstance(m, dict) and "value" in m:
        return m
    return None


def _bound_shape(record: Any) -> Optional[dict[str, Any]]:
    """A record's machine-readable bound {comparator,
    bound} — the citing claim carries the bound; no value
    is required on this half of the shape."""
    if not isinstance(record, dict):
        return None
    m = record.get("measurement")
    if isinstance(m, dict) and "comparator" in m and "bound" in m:
        return m
    return None


_POINTER_RE = re.compile(r"^(?P<path>.+):(?P<claim>[^:#]+)#(?P<field>[^#]+)$")


class _TieContext:
    """Everything V4 reads: the ledger entries, the verified
    source registers, the anchors register, and each claim's
    stored outcome blocks."""

    def __init__(self, root: Path, entries: list[dict[str, Any]]):
        self.root = root
        self.entries = {e["id"]: e for e in entries}
        self.claims = {
            e["id"]: e for e in entries if e.get("kind") == "claim"
        }
        self.registers = _load_registers(root, entries)
        anchors_path = root / ANCHORS_REL
        self.anchors: dict[str, Any] = {}
        if anchors_path.is_file():
            self.anchors = json.loads(
                anchors_path.read_text(encoding="utf-8")
            ).get("anchors", {})
        self.blocks = {
            e["id"]: _outcome_blocks(self.registers, e)
            for e in entries
            if e.get("kind") == "claim"
        }
        self.numeric_exercised = 0

    def source_record(self, entry: dict[str, Any]) -> Optional[dict[str, Any]]:
        return _source_record(self.registers, entry, "source_of_record")

    def resolve_pointer(self, pointer: str) -> Optional[dict[str, Any]]:
        m = _POINTER_RE.match(pointer)
        if not m:
            return None
        record = self.registers.record(m.group("path"), m.group("claim"))
        if record is None:
            return None
        block = record.get(m.group("field"))
        if isinstance(block, dict) and "spec" in block and "outcome" in block:
            return {
                "spec": str(block["spec"]),
                "outcome": str(block["outcome"]),
                "date": block.get("date"),
                "pointer": pointer,
            }
        return None


def _tie_failures_for_cell(
    ctx: _TieContext, cell: dict[str, Any]
) -> list[str]:
    """V4 over one matrix cell. Every citation after the
    entry id must carry the cell's relation under a
    registered tie; the entry id itself is T1 (the claim
    itself)."""
    row = cell["row"]
    relation = cell["relation"]
    rule = cell.get("rule")
    column = cell["column"]
    entry = ctx.claims.get(row)
    if entry is None:
        return [f"row {row!r} is not a ledger claim entry"]
    citations = cell.get("citations") or []
    if not citations or citations[0] != row:
        return [
            f"citation list does not open with the ledger entry id "
            f"{row!r} (got {citations[:1]})"
        ]
    sor = ctx.source_record(entry)
    failures: list[str] = []
    extras = citations[1:]

    if rule == "R1":
        instances = (sor or {}).get("evidence_instances") or []
        for citation in extras:
            tied = any(
                isinstance(inst, dict)
                and inst.get("source_document_id") == column
                and inst.get("claim_id") == citation
                for inst in instances
            )
            if not tied:
                failures.append(
                    f"citation {citation!r} is not an evidence "
                    f"instance of the claim naming document "
                    f"{column!r} (T1: no stored membership)"
                )
        if not extras:
            tied = any(
                isinstance(inst, dict)
                and inst.get("source_document_id") == column
                and not inst.get("claim_id")
                for inst in instances
            )
            if not tied:
                failures.append(
                    "R1 cell cites no instance and no stored "
                    "instance without a claim id names the column (T1)"
                )
    elif rule == "R2":
        items = (sor or {}).get("evidence") or []
        for citation in extras:
            tied = any(
                isinstance(item, dict)
                and str(item.get("ref")) == citation
                and DIRECTION_RELATIONS.get(str(item.get("direction")))
                == relation
                for item in items
            )
            if not tied:
                failures.append(
                    f"citation {citation!r}: no stored evidence "
                    f"item with this ref carries direction "
                    f"{relation!r} (T1: stored direction governs)"
                )
    elif rule == "R3":
        failures.extend(_tie_failures_study(ctx, row, column, relation, extras))
    elif rule == "R4":
        for citation in extras:
            anchor = ctx.anchors.get(citation)
            sign_ref = (
                f"mahadevan:{citation[1:]}"
                if citation.startswith("M")
                else None
            )
            tied = (
                anchor is not None
                and bool(anchor.get("reading"))
                and sign_ref in (entry.get("sign_refs") or [])
                and citation == column
            )
            if not tied:
                failures.append(
                    f"citation {citation!r}: no registered anchor "
                    "record whose frame-qualified sign intersects "
                    "the claim's sign_refs with a recorded reading "
                    "(T3)"
                )
    elif rule == "R5":
        failures.append(
            "R5 cell exists but the v1 verdict table is empty — "
            "no research-check verdict can carry a relation in v1"
        )
    elif rule == "R6":
        failures.append(
            "R6 cell exists but the settling-instrument register "
            "is empty in matrix-defs v1 (T4: no registered "
            "instrument record)"
        )
    else:
        failures.append(f"unregistered derivation rule {rule!r}")

    failures.extend(_numeric_arm_failures(ctx, entry, relation, extras))
    return failures


def _tie_failures_study(
    ctx: _TieContext,
    row: str,
    study: str,
    relation: str,
    pointers: list[str],
) -> list[str]:
    """T2, the dated-test tie — the Atlas failure mode's
    home. A study citation ties only if the study's
    governing stored outcome block for the claim is among
    the cited pointers and its recorded outcome maps to the
    asserted relation under the outcome table. An unexecuted
    or null outcome carries neither relation."""
    failures: list[str] = []
    stored = ctx.blocks.get(row, {}).get(study, [])
    if not stored:
        return [
            f"no stored outcome record names study {study!r} for "
            "this claim (T2: the study did not test the claim "
            "in the record)"
        ]
    governing = _governing(stored)
    cited_blocks = []
    for pointer in pointers:
        block = ctx.resolve_pointer(pointer)
        if block is None or block["spec"] != study:
            failures.append(
                f"citation {pointer!r} does not resolve to a "
                f"stored outcome block of study {study!r} for "
                "this claim (T2)"
            )
        else:
            cited_blocks.append(block)
    if failures:
        return failures
    if governing["pointer"] not in pointers:
        cited_desc = "; ".join(
            f"{b['outcome']} ({b['date']})" for b in cited_blocks
        )
        failures.append(
            f"the cited outcome block(s) [{cited_desc}] do not "
            f"include the study's governing block "
            f"({governing['outcome']}, {governing['date']}) — a "
            "superseded or non-bearing outcome carries no "
            "relation (T2). This is the named Atlas failure "
            "mode: a citation can exist, be relevant, and still "
            "not carry the relation"
        )
        return failures
    mapped = BEARING_OUTCOMES.get(governing["outcome"])
    if mapped != relation:
        failures.append(
            f"governing outcome {governing['outcome']!r} "
            f"({governing['date']}) maps to "
            f"{mapped or 'no relation (non-bearing)'} under the "
            f"outcome table, not {relation!r} (T2)"
        )
    return failures


def _numeric_arm_failures(
    ctx: _TieContext,
    entry: dict[str, Any],
    relation: str,
    citations: list[str],
) -> list[str]:
    """The numeric arm over a citation set: fires only where
    a cited record carries a measurement value and a
    machine-readable bound is carried on the cited record or
    the citing claim (registered shape {value, comparator,
    bound}). Counts exercises so the gate can state whether
    the live population exercised the arm."""
    failures: list[str] = []
    claim_shape = _bound_shape(entry) or _measurement_shape(entry)
    for citation in citations:
        cited_record: Any = None
        if citation in ctx.entries:
            cited_record = ctx.entries[citation]
        else:
            m = _POINTER_RE.match(citation)
            if m:
                cited_record = ctx.registers.record(
                    m.group("path"), m.group("claim")
                )
        cited_shape = _measurement_shape(cited_record)
        value = None
        comparator = None
        bound = None
        if cited_shape is not None:
            value = cited_shape.get("value")
            comparator = cited_shape.get("comparator")
            bound = cited_shape.get("bound")
        if value is None and isinstance(cited_record, dict) \
                and cited_record.get("kind") == "measurement":
            value = cited_record.get("value")
        if comparator is None and claim_shape is not None:
            comparator = claim_shape.get("comparator")
            bound = claim_shape.get("bound")
        if value is None or comparator is None or bound is None:
            continue
        ctx.numeric_exercised += 1
        reason = numeric_arm_check(relation, value, comparator, bound)
        if reason:
            failures.append(f"numeric arm: {reason}")
    return failures


def _tie_failures_for_edge(
    ctx: _TieContext, edge: dict[str, Any]
) -> list[str]:
    """V4 over one candidate-map edge {from, to, rel,
    citations}: the same tie rules as for matrix cells,
    resolved by citation kind (the map's edges are authored
    downstream, so no derivation rule vouches for them —
    each citation must tie on its own)."""
    claim_id = edge.get("to")
    relation = edge.get("rel")
    entry = ctx.claims.get(claim_id)
    label = f"edge {edge.get('from')!r} -> {claim_id!r} ({relation})"
    if entry is None:
        return [f"{label}: target is not a ledger claim entry"]
    if relation not in RELATIONS:
        return [f"{label}: unregistered relation {relation!r}"]
    citations = edge.get("citations") or []
    body = [c for c in citations if c != claim_id]
    failures: list[str] = []
    sor = ctx.source_record(entry)
    for citation in body:
        tied = False
        reasons: list[str] = []
        # T2 — a stored outcome-block pointer.
        block = ctx.resolve_pointer(citation)
        if block is not None:
            sub = _tie_failures_study(
                ctx, claim_id, block["spec"], relation, [citation]
            )
            if not sub:
                tied = True
            else:
                reasons.extend(sub)
        # T1 — an evidence instance claim id (supports).
        if not tied and sor is not None:
            instances = sor.get("evidence_instances") or []
            if any(
                isinstance(inst, dict)
                and inst.get("claim_id") == citation
                for inst in instances
            ):
                if relation == "supports":
                    tied = True
                else:
                    reasons.append(
                        "an evidence instance stands behind the "
                        "claim; it carries supports, not "
                        f"{relation!r} (T1)"
                    )
            # T1 — a bundle evidence ref with stored direction.
            items = sor.get("evidence") or []
            if any(
                isinstance(item, dict)
                and str(item.get("ref")) == citation
                and DIRECTION_RELATIONS.get(str(item.get("direction")))
                == relation
                for item in items
            ):
                tied = True
        # T3 — a registered anchor key.
        if not tied and citation in ctx.anchors:
            anchor = ctx.anchors[citation]
            sign_ref = (
                f"mahadevan:{citation[1:]}"
                if citation.startswith("M")
                else None
            )
            if (
                anchor.get("reading")
                and sign_ref in (entry.get("sign_refs") or [])
                and relation == "constrains"
            ):
                tied = True
            else:
                reasons.append(
                    "anchor record does not tie: the sign does "
                    "not intersect the claim's sign_refs, or "
                    "carries no reading, or the relation is not "
                    "constrains (T3)"
                )
        if not tied:
            detail = "; ".join(reasons) if reasons else (
                "the cited record is not named in the claim's "
                "stored relation fields, is not a governing "
                "study outcome, and is not a registered anchor "
                "or instrument (T1–T4). Existence and topical "
                "relevance are not ties"
            )
            failures.append(
                f"{label}: citation {citation!r} carries no "
                f"tie: {detail}"
            )
    failures.extend(
        f"{label}: {f}"
        for f in _numeric_arm_failures(ctx, entry, relation, body)
    )
    return failures


# ---------------------------------------------------------------------------
# V6 — anchor shares


def _anchor_shares(root: Path) -> dict[str, Any]:
    """Recompute the strict set and shares from the
    canonical anchors file under the rule version recorded
    in the file itself, with the Phase-108 provenance
    register the rule reads."""
    anchors_data = json.loads((root / ANCHORS_REL).read_text(encoding="utf-8"))
    anchors = anchors_data.get("anchors", {})
    annotation = (
        anchors_data.get("metadata", {}).get(
            "spec029_phase_h_annotation", {}
        )
    )
    rule = annotation.get("strict_set_rule", {})
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
    stored = {s for s, r in anchors.items() if r.get("strict_set")}
    total = len(anchors)
    return {
        "total": total,
        "recomputed_strict": recomputed,
        "stored_strict": stored,
        "recorded_rule_id": rule.get("rule_id"),
        "recorded_rule_version": rule.get("rule_version"),
        "recorded_strict_count": rule.get("strict_count"),
        "vocabulary": annotation.get("validation_status_vocabulary", []),
        "validation_statuses": {
            r.get("validation_status") for r in anchors.values()
        },
        "strict_share": (len(recomputed) / total) if total else 0.0,
    }


# ---------------------------------------------------------------------------
# V8 — settling canonicals under the gate's own
# glossa-settle-1 route, and the settling layer's
# scenario/verdict separation check.


def _settle_identity(ref: Any) -> Optional[tuple[str, int]]:
    frame, sep, value = str(ref).partition(":")
    if not sep or not frame:
        return None
    try:
        return (frame, int(value))
    except ValueError:
        return None


def _settle_anchor_key(identity: tuple[str, int]) -> Optional[str]:
    prefix = SETTLE_FRAME_PREFIXES.get(identity[0])
    if prefix is None:
        return None
    return f"{prefix}{identity[1]:03d}"


def _settle_falsifier_count(entry: dict[str, Any]) -> int:
    falsifier = entry.get("falsifier")
    if isinstance(falsifier, list):
        return sum(1 for f in falsifier if isinstance(f, str) and f)
    if isinstance(falsifier, str) and falsifier:
        return 1
    return 0


def _gate_settle(
    claims: list[dict[str, Any]],
    registers: _GateRegisters,
    anchors: dict[str, Any],
    strict_set: set[str],
    candidate: dict[str, Any],
    scope: list[Any],
) -> dict[str, Any]:
    """The gate's own S-R1…S-R4 evaluation of one candidate
    over one scope (glossa-settle-1, the gate's registered
    copies above). Independent of the engine's route: the
    same registered rules, separately implemented."""
    by_identity: dict[tuple[str, int], str] = {}
    for item in candidate.get("assignments") or []:
        identity = _settle_identity(item.get("sign"))
        if identity is not None:
            by_identity[identity] = str(item.get("value"))
    scope_pairs: list[tuple[str, tuple[str, int]]] = []
    for ref in scope:
        identity = _settle_identity(ref)
        if identity is not None:
            scope_pairs.append((str(ref), identity))

    assigned = [
        {"sign": sign_str, "value": by_identity[identity]}
        for sign_str, identity in scope_pairs
        if identity in by_identity
    ]
    assigned_ids = set(by_identity) & {
        identity for _, identity in scope_pairs
    }

    contexts: list[dict[str, Any]] = []
    uncontexted: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    n_strict = 0
    n_consistent = 0
    n_non_strict = 0
    for item in assigned:
        identity = _settle_identity(item["sign"])
        key = _settle_anchor_key(identity) if identity else None
        record = anchors.get(key) if key else None
        if record is None:
            uncontexted.append(
                {"sign": item["sign"], "value": item["value"]}
            )
            continue
        is_strict = key in strict_set
        reading = record.get("reading")
        if is_strict:
            n_strict += 1
            if item["value"] == reading:
                outcome = "consistent"
                n_consistent += 1
            else:
                outcome = "conflict"
                conflicts.append(
                    {
                        "sign": item["sign"],
                        "anchor": key,
                        "assigned_value": item["value"],
                        "anchor_reading": reading,
                    }
                )
        else:
            outcome = "non_strict"
            n_non_strict += 1
        contexts.append(
            {
                "sign": item["sign"],
                "anchor": key,
                "assigned_value": item["value"],
                "anchor_reading": reading,
                "confidence": record.get("confidence"),
                "strict": is_strict,
                "result": outcome,
            }
        )

    touched: list[dict[str, Any]] = []
    for entry in claims:
        refs = entry.get("sign_refs") or []
        via = [r for r in refs if _settle_identity(r) in assigned_ids]
        if not via:
            continue
        tallies = {key: 0 for key in SETTLE_TALLY_KEYS}
        for blocks in _outcome_blocks(registers, entry).values():
            relation = SETTLE_BEARING_OUTCOMES.get(
                _governing(blocks)["outcome"]
            )
            if relation:
                tallies[relation] += 1
        touched.append(
            {
                "claim": entry["id"],
                "via_signs": via,
                "tallies": tallies,
                "falsifiers_present": _settle_falsifier_count(entry),
                "falsifiers_evaluable": 0,
            }
        )

    forced: list[dict[str, Any]] = []
    for sign_str, identity in scope_pairs:
        if identity in assigned_ids:
            continue
        key = _settle_anchor_key(identity)
        if key and key in strict_set and key in anchors:
            forced.append(
                {"sign": sign_str, "value": anchors[key].get("reading")}
            )

    return {
        "scope": [sign_str for sign_str, _ in scope_pairs],
        "scope_signs": len(scope_pairs),
        "assigned": assigned,
        "assigned_count": len(assigned),
        "assigned_share": (
            len(assigned) / len(scope_pairs) if scope_pairs else None
        ),
        "uncontexted_assignments": uncontexted,
        "contexts": contexts,
        "contexts_touched": len(contexts),
        "strict_contexts": n_strict,
        "consistent": n_consistent,
        "non_strict_contexts": n_non_strict,
        "conflicts": conflicts,
        "strict_agreement_share": (
            n_consistent / n_strict if n_strict else None
        ),
        "contexted_share": (
            len(contexts) / len(assigned) if assigned else None
        ),
        "claims_touched": touched,
        "claims_touched_count": len(touched),
        "s_r3": {"class_table": None, "violations": []},
        "forced": forced,
    }


def _gate_compare(
    candidate_a: str,
    result_a: dict[str, Any],
    candidate_b: str,
    result_b: dict[str, Any],
) -> dict[str, Any]:
    """The gate's own dual-run comparison over two settled
    result blocks (semantics §7): tallies over every claim
    either run touches, divergences named, coverage deltas,
    signs assigned by one only, and the expectations
    absence statement in its mechanically derivable form."""
    side_a = candidate_a.replace("-", "_")
    side_b = candidate_b.replace("-", "_")
    tallies_a = {t["claim"]: t["tallies"] for t in result_a["claims_touched"]}
    tallies_b = {t["claim"]: t["tallies"] for t in result_b["claims_touched"]}
    zero = {key: 0 for key in SETTLE_TALLY_KEYS}
    order: list[str] = []
    for claim_id in list(tallies_a) + list(tallies_b):
        if claim_id not in order:
            order.append(claim_id)
    compared: list[dict[str, Any]] = []
    divergences: list[dict[str, Any]] = []
    for claim_id in order:
        ta = tallies_a.get(claim_id, dict(zero))
        tb = tallies_b.get(claim_id, dict(zero))
        compared.append(
            {
                "claim": claim_id,
                f"{side_a}_tallies": ta,
                f"{side_b}_tallies": tb,
                "divergent": ta != tb,
            }
        )
        if ta != tb:
            divergences.append(
                {
                    "claim": claim_id,
                    f"{side_a}_tallies": ta,
                    f"{side_b}_tallies": tb,
                }
            )

    def delta(value_a: Any, value_b: Any) -> dict[str, Any]:
        return {side_a: value_a, side_b: value_b}

    assigned_a = [item["sign"] for item in result_a["assigned"]]
    assigned_b = [item["sign"] for item in result_b["assigned"]]
    ids_a = {_settle_identity(s) for s in assigned_a}
    ids_b = {_settle_identity(s) for s in assigned_b}
    if len(order) == 1:
        note = (
            "No pre-registered expectation exists in the "
            "program's record for the one touched claim."
        )
    elif order:
        note = (
            "No pre-registered expectation exists in the "
            f"program's record for the {len(order)} touched "
            "claims."
        )
    else:
        note = (
            "No pre-registered expectation exists in the "
            "program's record for a touched claim; neither "
            "run touches a claim."
        )
    return {
        "claims_compared": compared,
        "per_claim_divergences": divergences,
        "coverage_deltas": {
            "assigned_count": delta(
                result_a["assigned_count"], result_b["assigned_count"]
            ),
            "contexts_touched": delta(
                result_a["contexts_touched"], result_b["contexts_touched"]
            ),
            "strict_contexts": delta(
                result_a["strict_contexts"], result_b["strict_contexts"]
            ),
            "consistent": delta(
                result_a["consistent"], result_b["consistent"]
            ),
            "conflicts": delta(
                len(result_a["conflicts"]), len(result_b["conflicts"])
            ),
            "forced_count": delta(
                len(result_a["forced"]), len(result_b["forced"])
            ),
        },
        "signs_assigned_by_one_only": {
            f"{side_b}_only": [
                s for s in assigned_b if _settle_identity(s) not in ids_a
            ],
            f"{side_a}_only": [
                s for s in assigned_a if _settle_identity(s) not in ids_b
            ],
        },
        "pre_registered_expectations": [],
        "pre_registered_expectations_note": note,
    }


def _map_matrix_key(ref: Any) -> Optional[str]:
    """matrix-defs v1 R4's key construction (map-defs v1
    §7): the frame prefix + the number as written in the
    sign_ref — no zero-padding."""
    frame, sep, value = str(ref).partition(":")
    if not sep or frame not in SETTLE_FRAME_PREFIXES:
        return None
    return f"{SETTLE_FRAME_PREFIXES[frame]}{value}"


def _map_anchor_summary(
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


def _map_census_lines(expected_map: dict[str, Any]) -> list[str]:
    """The census rule (map-defs v1 §10): every map check
    class states the live instance count behind it; a class
    or named sub-population with zero live instances is
    reported UNPROVEN on the live population, never silently
    counted as passing."""
    elements = expected_map.get("elements", [])
    by_kind = Counter(e.get("kind") for e in elements)
    edges = expected_map.get("edges", [])
    by_rel = Counter(e.get("rel") for e in edges)
    lines = [
        f"census: {by_kind.get('claim', 0)} claim elements; "
        "column elements by class: "
        + ", ".join(
            f"{cls} {by_kind.get(cls, 0)}" for cls in COLUMN_CLASSES
        ),
        f"census: {len(edges)} map edges by relation: "
        + ", ".join(f"{rel} {by_rel.get(rel, 0)}" for rel in RELATIONS)
        + f"; {len(expected_map.get('claims', {}))} per-claim "
        "records; "
        f"{len((expected_map.get('settling') or {}).get('runs', []))} "
        "stored settling runs recomputed",
    ]
    for cls in COLUMN_CLASSES:
        if not by_kind.get(cls):
            lines.append(
                f"UNPROVEN on the live population: {cls} "
                "elements — 0 live instances (the class exists "
                "in the definitions and carries no columns "
                "in v1; its teeth are fixtures in the battery)"
            )
    if not by_rel.get("constrains"):
        lines.append(
            "UNPROVEN on the live population: constrains "
            "edges — 0 live instances (the relation class is "
            "empty in the generated matrix and the artifact "
            "says so; its teeth are fixtures in the battery)"
        )
    return lines


def _derive_map(
    root: Path,
    entries: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    deriv: _Derivation,
    shares: dict[str, Any],
    ledger_sha: str,
) -> tuple[dict[str, Any], list[str]]:
    """The gate's own map recomputation (V5's full leg):
    the expected map artifact, built from the ledger by
    the gate's routes — its matrix derivation, its anchor
    shares, its settling route — under its registered
    map-defs v1 copies. Returns (expected, failures):
    failures names defects in the records of record
    themselves (a stored run record the gate's route does
    not reproduce, a pin that names another build), which
    fail V5 however faithfully the map copied them."""
    failures: list[str] = []
    coverage = deriv.coverage
    anchors_path = root / ANCHORS_REL
    anchors_raw = anchors_path.read_bytes()
    anchors = json.loads(anchors_raw.decode("utf-8")).get("anchors", {})
    anchors_raw_sha = hashlib.sha256(anchors_raw).hexdigest()
    strict_set = shares["recomputed_strict"]

    # -- header ---------------------------------------------------------------
    by_status = Counter(str(e.get("status")) for e in claims)
    bearing_groups: dict[tuple[str, str, str], dict[str, Any]] = {}
    for entry in claims:
        for spec, blocks in deriv.blocks.get(entry["id"], {}).items():
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
    pending = sum(
        1
        for r in anchors.values()
        if r.get("validation_status") == PENDING_VALIDATION_STATUS
    )

    matrix_path = root / MATRIX_REL_DIR / "matrix.json"
    as_of = {
        "ledger_sha256": ledger_sha,
        "ledger_lines": len(entries),
        "ledger_date": max(
            (str(e.get("date")) for e in entries), default=None
        ),
        "ledger_schema": li.SCHEMA_VERSION,
        "matrix_defs": GATE_MATRIX_DEFS_VERSION,
        "map_defs": GATE_MAP_DEFS_VERSION,
        "settle_semantics": SETTLE_SEMANTICS_VERSION,
        "matrix_sha256": li.sha256_file(matrix_path),
        "anchors_register_sha256_raw_bytes": anchors_raw_sha,
    }
    header = {
        "claims_total": len(claims),
        "claims_by_status": {k: by_status[k] for k in sorted(by_status)},
        "validated_anchor_share": shares["strict_share"],
        "strict_anchor_share": shares["strict_share"],
        "anchors_strict": len(strict_set),
        "anchors_total": shares["total"],
        "nearest_dated_items": nearest,
        "pending_validations": {
            "count": pending,
            "reason": PENDING_VALIDATIONS_REASON,
        },
        "as_of": as_of,
    }

    # -- elements + loads ------------------------------------------------------
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
        {"kind": c["class"], "id": c["id"]} for c in deriv.columns
    ]
    loads: dict[str, dict[str, int]] = {
        row["id"]: {rel: 0 for rel in RELATIONS} for row in deriv.rows
    }
    cells_by_row: dict[str, list[dict[str, Any]]] = {}
    for cell in deriv.cells:
        if cell["row"] in loads:
            loads[cell["row"]][cell["relation"]] += 1
        cells_by_row.setdefault(cell["row"], []).append(cell)

    # -- edges (map-defs §5: citations that carry) -----------------------------
    edges: list[dict[str, Any]] = []
    for cell in deriv.cells:
        citations = list(cell.get("citations") or [])
        if cell.get("rule") == "R3":
            blocks = deriv.blocks.get(cell["row"], {}).get(
                cell["column"], []
            )
            if blocks:
                governing = _governing(blocks)
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

    # -- the settling records, re-derived by the gate's own route ---------------
    sets_path = root / ASSIGNMENT_SETS_REL
    if not sets_path.is_file():
        raise FileNotFoundError(
            f"assignment sets of record not found: {ASSIGNMENT_SETS_REL}"
        )
    assignment_sets = json.loads(sets_path.read_text(encoding="utf-8"))
    as_of["assignment_sets_sha256"] = li.sha256_file(sets_path)
    register_pin = (assignment_sets.get("register") or {}).get(
        "sha256_raw_bytes"
    )
    if register_pin != anchors_raw_sha:
        failures.append(
            f"the assignment-sets record pins anchors register "
            f"{register_pin}, but the register on disk hashes "
            f"{anchors_raw_sha}"
        )
    sets_by_id = {
        s.get("id"): s for s in assignment_sets.get("sets", [])
    }
    out_of_frame = list(assignment_sets.get("out_of_frame_records") or [])
    in_frame = len(anchors) - len(out_of_frame)
    sets_summary = []
    for s in assignment_sets.get("sets", []):
        item = {
            "id": s.get("id"),
            "frame": s.get("frame"),
            "assignments": len(s.get("assignments") or []),
            "provenance": s.get("provenance"),
        }
        item["frame_scope"] = in_frame
        item["share"] = (
            item["assignments"] / in_frame if in_frame else None
        )
        sets_summary.append(item)

    runs_dir = root / RUNS_REL_DIR
    run_files = sorted(runs_dir.glob("*.json")) if runs_dir.is_dir() else []
    loaded_runs = []
    for run_path in run_files:
        record = json.loads(run_path.read_text(encoding="utf-8"))
        loaded_runs.append((run_path, record))
    loaded_runs.sort(
        key=lambda pair: (
            0 if pair[1].get("candidate") == "incumbent" else 1,
            pair[0].stem,
        )
    )
    runs: list[dict[str, Any]] = []
    settled_results: list[tuple[str, dict[str, Any]]] = []
    touched_by_claim: dict[str, list[dict[str, Any]]] = {}
    for run_path, record in loaded_runs:
        pins = record.get("pins") or {}
        pin_sha = (pins.get("ledger") or {}).get("sha256")
        if pin_sha != ledger_sha:
            failures.append(
                f"run record {run_path.stem} is pinned to ledger "
                f"{pin_sha}, but the current ledger is "
                f"{ledger_sha} — it cannot be carried by the map"
            )
        candidate_id = record.get("candidate")
        candidate_set = sets_by_id.get(candidate_id)
        if candidate_set is None:
            failures.append(
                f"run record {run_path.stem} names candidate "
                f"{candidate_id!r}, which is not a set of record"
            )
            continue
        result = _gate_settle(
            claims,
            deriv.registers,
            anchors,
            strict_set,
            {"assignments": candidate_set.get("assignments") or []},
            record.get("scope") or [],
        )
        stored_result = record.get("result") or {}
        record_divs: list[str] = []
        _first_divergences(
            result, stored_result, f"run record {run_path.stem}",
            record_divs, limit=6,
        )
        failures.extend(
            f"the gate's settling route does not reproduce {d}"
            for d in record_divs
        )
        settled_results.append((str(candidate_id), result))
        run_summary = {
            "record": run_path.stem,
            "scenario": record.get("scenario"),
            "candidate": candidate_id,
            "semantics": record.get("semantics"),
            "pins": pins,
        }
        for field_name in MAP_RUN_RESULT_FIELDS:
            run_summary[field_name] = result.get(field_name)
        runs.append(run_summary)
        for touched in result.get("claims_touched") or []:
            touched_by_claim.setdefault(touched["claim"], []).append(
                {
                    "candidate": candidate_id,
                    "record": run_path.stem,
                    "via_signs": touched.get("via_signs"),
                    "tallies": touched.get("tallies"),
                    "falsifiers_present": touched.get(
                        "falsifiers_present"
                    ),
                    "falsifiers_evaluable": touched.get(
                        "falsifiers_evaluable"
                    ),
                }
            )

    comparison_path = root / COMPARISON_REL
    if not comparison_path.is_file():
        raise FileNotFoundError(
            f"comparison record not found: {COMPARISON_REL}"
        )
    comparison_record = json.loads(
        comparison_path.read_text(encoding="utf-8")
    )
    comp_pin_sha = (
        (comparison_record.get("pins") or {}).get("ledger") or {}
    ).get("sha256")
    if comp_pin_sha != ledger_sha:
        failures.append(
            f"the filed comparison record is pinned to ledger "
            f"{comp_pin_sha}, but the current ledger is {ledger_sha}"
        )
    if len(settled_results) == 2:
        computed_comparison = _gate_compare(
            settled_results[0][0],
            settled_results[0][1],
            settled_results[1][0],
            settled_results[1][1],
        )
    else:
        failures.append(
            f"the run store carries {len(settled_results)} "
            "reproducible runs, not the stored pair the "
            "comparison names"
        )
        computed_comparison = comparison_record.get("result")
    comparison = {
        "record": COMPARISON_REL,
        "sha256": li.sha256_file(comparison_path),
        "result": computed_comparison,
    }
    as_of["comparison_sha256"] = comparison["sha256"]
    divergent_by_claim = {
        row["claim"]: row.get("divergent")
        for row in (computed_comparison or {}).get(
            "claims_compared", []
        )
    }

    canonical_path = root / SETTLING_CANONICAL_REL
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
    frame = sets_summary[0]["frame"] if sets_summary else None
    hotspots = [
        {
            "row": c["row"],
            "column": c["column"],
            "column_class": c["column_class"],
            "rule": c.get("rule"),
            "relation": c["relation"],
        }
        for c in deriv.cells
        if c["relation"] == "opposes"
    ]
    by_stage = Counter(
        str(e.get("stage")) for e in claims if e.get("stage")
    )
    by_population = Counter(str(e.get("population")) for e in claims)
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
            "covered": (coverage.get("falsifier_coverage") or {}).get(
                "covered"
            ),
            "total": (coverage.get("falsifier_coverage") or {}).get(
                "total"
            ),
            "by_population": (
                coverage.get("falsifier_coverage") or {}
            ).get("by_population"),
            "gap_claims": [
                e["id"] for e in claims if not e.get("falsifier")
            ],
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
            "node_count": (deriv.sign_block or {}).get("node_count"),
            "edge_count": (deriv.sign_block or {}).get("edge_count"),
            "edges_emitted": (deriv.sign_block or {}).get(
                "edges_emitted"
            ),
            "community_count": (deriv.sign_block or {}).get(
                "community_count"
            ),
            "corpus_sha256": (
                (deriv.sign_block or {}).get("source") or {}
            ).get("corpus_sha256"),
        },
    }

    # -- per-claim records ---------------------------------------------------------
    annotations = [e for e in entries if e.get("kind") == "annotation"]
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
            m_key = _map_matrix_key(ref)
            identity = _settle_identity(ref)
            s_key = _settle_anchor_key(identity) if identity else None
            matrix_record = _map_anchor_summary(
                anchors, strict_set, m_key
            )
            settle_record = _map_anchor_summary(
                anchors, strict_set, s_key
            )
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
                "present": _settle_falsifier_count(entry),
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
                "note": MAP_S_R3_NOTE,
            },
        },
    }

    expected = {
        "artifact": "glossa-indus layered map data",
        "generated_from": (
            f"{li.LEDGER_REL} through "
            f"{MATRIX_REL_DIR}/matrix.json and the "
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
            "rows": deriv.rows,
            "columns": deriv.columns,
            "cells": deriv.cells,
            "coverage": coverage,
            "sign_sign_block": deriv.sign_block,
        },
        "system": system,
        "claims": claim_records,
        "settling": settling,
    }
    return expected, failures


def _v8_checks(
    root: Path,
    entries: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[Check]:
    names = (
        "V8 settling canonicals — scenarios reproduce under "
        "the gate's own glossa-settle-1 route",
        "V8 settling canonicals — the registered comparison "
        "reproduces",
        "V8 scenario/verdict separation — the settling layer "
        "carries no reachable ledger write path",
    )
    canonical_path = root / SETTLING_CANONICAL_REL
    anchors_path = root / ANCHORS_REL
    register_path = root / PROVENANCE_REGISTER_REL
    corpus_path = root / CORPUS_REL
    absent = [
        rel
        for rel, path in (
            (SETTLING_CANONICAL_REL, canonical_path),
            (ANCHORS_REL, anchors_path),
            (PROVENANCE_REGISTER_REL, register_path),
            (CORPUS_REL, corpus_path),
        )
        if not path.is_file()
    ]
    if absent:
        return [
            Check(
                name,
                "NOT-RUN",
                [
                    "the settling layer is not present in this "
                    f"tree (absent: {', '.join(absent)}) — V8 "
                    "runs where the settling layer is present"
                ],
            )
            for name in names
        ]
    try:
        canonical = json.loads(
            canonical_path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        return [
            Check(
                names[0],
                "FAIL",
                [f"cannot parse {SETTLING_CANONICAL_REL}: {exc}"],
            ),
            Check(names[1], "NOT-RUN", ["the canonical artifact does not parse"]),
            Check(names[2], "NOT-RUN", ["the canonical artifact does not parse"]),
        ]

    # The provenance pins first: the canonicals govern one
    # pinned build; a tree they do not describe fails here,
    # naming the pin, before any scenario is settled.
    pin_failures: list[str] = []
    prov = canonical.get("provenance", {})
    ledger_pin = prov.get("ledger", {})
    ledger_path = root / li.LEDGER_REL
    actual_ledger_sha = (
        li.canonical_sha256_bytes(ledger_path.read_bytes())
        if ledger_path.is_file()
        else "MISSING"
    )
    if ledger_pin.get("sha256_canonical") != actual_ledger_sha:
        pin_failures.append(
            f"ledger pin: the canonicals were derived over "
            f"ledger sha256 {ledger_pin.get('sha256_canonical')}, "
            f"this tree's ledger hashes {actual_ledger_sha}"
        )
    if ledger_pin.get("lines") != len(entries):
        pin_failures.append(
            f"ledger pin: the canonicals record "
            f"{ledger_pin.get('lines')} ledger lines, this "
            f"tree carries {len(entries)}"
        )
    anchors_bytes = anchors_path.read_bytes()
    anchors_raw_sha = hashlib.sha256(anchors_bytes).hexdigest()
    anchors_pin = prov.get("anchors_register", {})
    if anchors_pin.get("sha256_raw_bytes") != anchors_raw_sha:
        pin_failures.append(
            "anchors register pin: the canonicals were "
            f"derived over register raw sha256 "
            f"{anchors_pin.get('sha256_raw_bytes')}, this "
            f"tree's register hashes {anchors_raw_sha}"
        )
    corpus_pin = prov.get("corpus_snapshot", {})
    if corpus_pin.get("sha256_canonical") != li.sha256_file(corpus_path):
        pin_failures.append(
            "corpus pin: the canonicals were derived over "
            f"corpus sha256 {corpus_pin.get('sha256_canonical')}, "
            f"this tree's corpus hashes "
            f"{li.sha256_file(corpus_path)}"
        )
    shares = _anchor_shares(root)
    if shares["recorded_rule_id"] != STRICT_RULE_ID:
        pin_failures.append(
            f"strict rule pin: the anchors file records rule "
            f"{shares['recorded_rule_id']!r}; glossa-settle-1 "
            f"is registered against {STRICT_RULE_ID!r}"
        )
    if shares["recomputed_strict"] != shares["stored_strict"]:
        pin_failures.append(
            "strict set: the recomputation disagrees with "
            "the stored strict_set flags — a settling run "
            "refuses over this register (semantics §1)"
        )
    if anchors_pin.get("strict") != len(shares["recomputed_strict"]):
        pin_failures.append(
            f"strict count pin: the canonicals record "
            f"{anchors_pin.get('strict')} strict anchors, "
            f"recomputed {len(shares['recomputed_strict'])}"
        )
    registers = _load_registers(root, entries)
    if registers.mismatches:
        pin_failures.append(
            "source records do not verify against the "
            "ledger's recorded hashes (the settling route "
            "reads outcome blocks from verified records "
            f"only): {registers.mismatches[:3]}"
        )
    if pin_failures:
        return [
            Check(names[0], "FAIL", pin_failures),
            Check(
                names[1],
                "NOT-RUN",
                ["the canonicals' pins do not hold over this tree"],
            ),
            *_v8_separation_checks(root, names[2]),
        ]

    anchors = json.loads(anchors_bytes.decode("utf-8")).get("anchors", {})
    strict_set = shares["recomputed_strict"]

    # (a) The scenarios, settled by the gate's own route.
    divergences: list[str] = []
    settled: dict[str, dict[str, Any]] = {}
    candidates: dict[str, str] = {}
    for scenario in canonical.get("scenarios", []):
        result = _gate_settle(
            claims,
            registers,
            anchors,
            strict_set,
            scenario["inputs"]["candidate"],
            scenario["inputs"]["scope"],
        )
        settled[scenario["id"]] = result
        candidates[scenario["id"]] = scenario["inputs"]["candidate"].get(
            "id", scenario["id"]
        )
        _first_divergences(
            result,
            scenario["expected"],
            f"scenario {scenario['id']}",
            divergences,
            limit=12,
        )
    scenario_check = Check(
        names[0],
        "FAIL" if divergences else "PASS",
        divergences
        or [
            f"{len(settled)} registered canonical scenarios "
            "reproduced exactly under the gate's own "
            "glossa-settle-1 route (S-R4 result blocks, "
            "field-for-field), over provenance pins that "
            "verify against this tree"
        ],
    )

    # (b) The registered comparison, compared by the gate's
    # own comparison. The expectations note is checked on
    # its mechanically derivable part (FINDING-S4-1).
    comparison_checks: list[Check] = []
    for comparison in canonical.get("comparisons", []):
        run_ids = comparison["inputs"]["runs"]
        if len(run_ids) != 2 or any(r not in settled for r in run_ids):
            comparison_checks.append(
                Check(
                    names[1],
                    "FAIL",
                    [
                        f"comparison {comparison['id']} names "
                        f"runs {run_ids}, which are not both "
                        "registered scenarios"
                    ],
                )
            )
            continue
        computed = _gate_compare(
            candidates[run_ids[0]],
            settled[run_ids[0]],
            candidates[run_ids[1]],
            settled[run_ids[1]],
        )
        expected = dict(comparison["expected"])
        registered_note = expected.pop(
            "pre_registered_expectations_note", None
        )
        gate_note = computed.pop("pre_registered_expectations_note")
        comp_divergences: list[str] = []
        _first_divergences(
            computed, expected, f"comparison {comparison['id']}",
            comp_divergences, limit=12,
        )
        note_ok = (
            registered_note is not None
            and gate_note == registered_note.split(";")[0] + "."
        )
        if comp_divergences or not note_ok:
            evidence = list(comp_divergences)
            if not note_ok:
                evidence.append(
                    "pre_registered_expectations_note: the "
                    "gate's absence clause does not match the "
                    "registered note's first clause"
                )
            comparison_checks.append(Check(names[1], "FAIL", evidence))
        else:
            comparison_checks.append(
                Check(
                    names[1],
                    "PASS",
                    [
                        f"comparison {comparison['id']} "
                        "reproduced exactly (claims compared, "
                        "per-claim divergences, coverage "
                        "deltas, signs assigned by one only, "
                        "expectations named); the expectations "
                        "note is checked on its mechanically "
                        "derivable part — the absence clause "
                        "matches verbatim; the registered "
                        "note's remainder is brief-specific "
                        "prose (FINDING-S4-1, stage record)"
                    ],
                )
            )
    if not comparison_checks:
        comparison_checks.append(
            Check(
                names[1],
                "FAIL",
                ["the canonical artifact registers no comparison"],
            )
        )

    return [scenario_check, *comparison_checks, *_v8_separation_checks(root, names[2])]


def _v8_separation_checks(root: Path, name: str) -> list[Check]:
    """The settling layer's separation arm: no settling or
    scenario module may import **or reach** a ledger write
    entry point. V9.2 audits imports; this arm extends the
    audit to reachability — an attribute use such as
    `li.append_entry(...)` or a bare name reference is a
    reachable write path even where the import itself names
    only the module (harmonization adoption 3, item 3: the
    computed layer and the verdict layer stay distinct by
    construction, not by import style)."""
    pkg_dir = root / "backend" / "glossa_lab"
    modules: list[Path] = []
    if pkg_dir.is_dir():
        modules = sorted(
            p
            for p in pkg_dir.rglob("*.py")
            if re.search(r"settling|scenario", p.name)
        )
    if not modules:
        return [
            Check(
                name,
                "FAIL",
                [
                    "the canonical artifact is present but no "
                    "settling/scenario module exists under "
                    "backend/glossa_lab — the layer the "
                    "canonicals govern is missing"
                ],
            )
        ]
    failures: list[str] = []
    for path in modules:
        rel = str(path.relative_to(root))
        tree = ast.parse(path.read_text(encoding="utf-8"))
        bad_imports = _imported_names(tree) & set(WRITE_ENTRY_POINTS)
        if bad_imports:
            failures.append(
                f"{rel} imports ledger write entry points "
                f"{sorted(bad_imports)}"
            )
        reached: set[str] = set()
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr in WRITE_ENTRY_POINTS
            ):
                reached.add(node.attr)
            elif (
                isinstance(node, ast.Name)
                and node.id in WRITE_ENTRY_POINTS
            ):
                reached.add(node.id)
        if reached:
            failures.append(
                f"{rel} reaches ledger write entry points "
                f"{sorted(reached)} (attribute or name use — "
                "a reachable write path, not only an import)"
            )
    return [
        Check(
            name,
            "FAIL" if failures else "PASS",
            failures
            or [
                f"{len(modules)} settling/scenario module(s) "
                "scanned; none imports or reaches a ledger "
                f"write path ({', '.join(WRITE_ENTRY_POINTS)}) "
                "— the settling layer's outputs are computed "
                "records, never ledger verdicts"
            ],
        )
    ]


# ---------------------------------------------------------------------------
# V9 — no write path


def _imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.name)
                if alias.asname:
                    names.add(alias.asname)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
    return names


def _has_write_call(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in (
                "write_bytes",
                "write_text",
            ):
                return True
            if isinstance(func, ast.Name) and func.id == "open" and any(
                isinstance(a, ast.Constant)
                and isinstance(a.value, str)
                and ("w" in a.value or "a" in a.value)
                for a in node.args[1:]
            ):
                return True
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "replace"
                and isinstance(func.value, ast.Name)
                and func.value.id == "os"
            ):
                return True
    return False


def _v9_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    # V9.1 — the gate's own import hygiene.
    gate_files = [
        Path(__file__),
        root / "tools" / "ledger" / "check_ledger_gate.py",
    ]
    hygiene_failures: list[str] = []
    for path in gate_files:
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        bad = _imported_names(tree) & set(WRITE_ENTRY_POINTS)
        if bad:
            hygiene_failures.append(
                f"{path.name} imports write entry points {sorted(bad)}"
            )
        if path == Path(__file__) and _has_write_call(tree):
            hygiene_failures.append(
                "ledger_gate.py contains a write call — the gate "
                "must never write"
            )
    checks.append(
        Check(
            "V9 no write path — gate import hygiene",
            "FAIL" if hygiene_failures else "PASS",
            hygiene_failures
            or [
                "the gate modules import no write entry point "
                f"({', '.join(WRITE_ENTRY_POINTS)}) and contain "
                "no write call"
            ],
        )
    )

    # V9.2 — settling/scenario package audit.
    pkg_dir = root / "backend" / "glossa_lab"
    settling_modules = []
    if pkg_dir.is_dir():
        settling_modules = sorted(
            p
            for p in pkg_dir.rglob("*.py")
            if re.search(r"settling|scenario", p.name)
        )
    audit_failures: list[str] = []
    for path in settling_modules:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        bad = _imported_names(tree) & set(WRITE_ENTRY_POINTS)
        if bad:
            audit_failures.append(
                f"{path.relative_to(root)} imports write entry "
                f"points {sorted(bad)}"
            )
    if settling_modules:
        evidence = audit_failures or [
            f"{len(settling_modules)} settling/scenario module(s) "
            "audited; none imports a ledger write path"
        ]
    else:
        evidence = [
            "no settling/scenario package exists yet (Stage 4); "
            "the audit is armed and scans for one on every run"
        ]
    checks.append(
        Check(
            "V9 no write path — settling/scenario import audit",
            "FAIL" if audit_failures else "PASS",
            evidence,
        )
    )

    # V9.3 — writer census over the repo's production python
    # sources (backend/glossa_lab, backend/scripts, tools).
    # Test code is out of the census: it writes fixtures
    # under tmp dirs by design and is not a publication path.
    writers_found: set[str] = set()
    readers: set[str] = set()
    for base in (
        root / "backend" / "glossa_lab",
        root / "backend" / "scripts",
        root / "tools",
    ):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.py")):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if not any(p.search(text) for p in ARTIFACT_PATH_PATTERNS):
                continue
            rel = str(path.relative_to(root))
            if _has_write_call(ast.parse(text)):
                writers_found.add(rel)
            else:
                readers.add(rel)
    unregistered = writers_found - REGISTERED_WRITERS
    checks.append(
        Check(
            "V9 no write path — matrix/map writer census",
            "FAIL" if unregistered else "PASS",
            [
                f"writers of the gated artifacts: "
                f"{sorted(writers_found) or 'none found'}",
                f"readers (no write call): {len(readers)} module(s)",
                "census scope: backend/glossa_lab, "
                "backend/scripts, tools (test code writes "
                "fixtures under tmp dirs by design and is not "
                "a publication path)",
            ]
            + (
                [
                    f"UNREGISTERED WRITER: {w} — the generator "
                    "and the gated-publication path are the only "
                    "writers (V9)"
                    for w in sorted(unregistered)
                ]
                if unregistered
                else []
            ),
        )
    )
    return checks


# ---------------------------------------------------------------------------
# The gate run


def _first_divergences(expected: Any, actual: Any, path: str, out: list[str],
                       limit: int = 8) -> None:
    """Enumerate the first divergences between two JSON
    structures, with paths — enough to repair from, never a
    silent 'differs'."""
    if len(out) >= limit:
        return
    if type(expected) is not type(actual):
        out.append(
            f"{path}: expected {type(expected).__name__} "
            f"{str(expected)[:80]!r}, found {type(actual).__name__} "
            f"{str(actual)[:80]!r}"
        )
        return
    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(actual), key=str):
            if len(out) >= limit:
                return
            if key not in actual:
                out.append(f"{path}.{key}: missing from the artifact")
            elif key not in expected:
                out.append(f"{path}.{key}: present in the artifact, not recomputed")
            else:
                _first_divergences(expected[key], actual[key], f"{path}.{key}", out, limit)
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            out.append(
                f"{path}: recomputed {len(expected)} items, "
                f"artifact carries {len(actual)}"
            )
        for i, (e, a) in enumerate(zip(expected, actual)):
            if len(out) >= limit:
                return
            label = f"{path}[{i}]"
            if isinstance(e, dict) and "row" in e and "column" in e:
                label = f"{path}[{e['row']} × {e['column']}]"
            elif isinstance(e, dict) and "id" in e:
                label = f"{path}[{e['id']}]"
            _first_divergences(e, a, label, out, limit)
    elif expected != actual:
        out.append(f"{path}: recomputed {expected!r}, artifact carries {actual!r}")


def run_gate(
    root: Path,
    *,
    mode: str = "full",
    scope: Optional[set[str]] = None,
    candidate_matrix: Optional[Path] = None,
    candidate_map: Optional[Path] = None,
    regen: bool = False,
    intended_change: Optional[str] = None,
) -> GateReport:
    """Run the gate over the tree at ``root``. ``scope`` is
    the set of check classes to run (None = all); classes
    out of scope are enumerated NOT-RUN. Never writes."""
    root = Path(root)
    report = GateReport(root=root, mode=mode)

    def in_scope(cls: str) -> bool:
        return scope is None or cls in scope

    ledger_path = root / li.LEDGER_REL
    entries: list[dict[str, Any]] = []
    if ledger_path.is_file():
        entries = li.read_ledger(ledger_path)
    claims = [e for e in entries if e.get("kind") == "claim"]

    # -- header -------------------------------------------------------------
    validator = li.validate_ledger(root)
    ledger_sha = (
        li.canonical_sha256_bytes(ledger_path.read_bytes())
        if ledger_path.is_file()
        else "MISSING"
    )
    report.header = [
        "Ledger gate — glossa-indus chain (Spec 086, Point 4)",
        f"mode: {mode}",
        f"root: {root}",
        f"ledger: {li.LEDGER_REL} — {len(entries)} lines, "
        f"canonical sha256 {ledger_sha}",
        f"definitions: {GATE_MATRIX_DEFS_VERSION} (the gate's "
        "registered copies); ledger schema: "
        f"{li.SCHEMA_VERSION}",
        f"map definitions: {GATE_MAP_DEFS_VERSION} (the gate's "
        "registered copies)",
        f"settling semantics: {SETTLE_SEMANTICS_VERSION} (the "
        f"gate's registered copies); canonicals: "
        f"{SETTLING_CANONICAL_REL}",
        "falsifier coverage: "
        f"{validator.falsifier_covered} of {validator.falsifier_total} "
        "claim entries carry a falsifier (published on every "
        "gate run, C086-5)"
        + (
            " — by population: "
            + ", ".join(
                f"{k} {c}/{t}"
                for k, (c, t) in sorted(
                    validator.falsifier_by_population.items()
                )
            )
            if validator.falsifier_by_population
            else ""
        ),
    ]

    # -- the matrix under check ----------------------------------------------
    matrix_path = candidate_matrix or (root / MATRIX_REL_DIR / "matrix.json")
    matrix: Optional[dict[str, Any]] = None
    matrix_error: Optional[str] = None
    if matrix_path.is_file():
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            matrix_error = f"cannot parse {matrix_path}: {exc}"
    else:
        matrix_error = f"matrix artifact not found: {matrix_path}"
    if candidate_matrix is not None:
        report.header.append(
            f"candidate matrix under check: {matrix_path} "
            "(the published artifact is not read)"
        )

    map_data: Optional[dict[str, Any]] = None
    map_error: Optional[str] = None
    committed_map = root / MAP_REL
    if candidate_map is not None:
        if candidate_map.is_file():
            try:
                map_data = json.loads(
                    candidate_map.read_text(encoding="utf-8")
                )
            except (OSError, json.JSONDecodeError) as exc:
                map_error = f"cannot parse {candidate_map}: {exc}"
        else:
            map_error = f"candidate map not found: {candidate_map}"
    elif committed_map.is_file():
        try:
            map_data = json.loads(committed_map.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            map_error = f"cannot parse {committed_map}: {exc}"

    # -- derivations (lazy: the expensive routes run once) --------------------
    _derivation: dict[str, Optional[_Derivation]] = {}

    def derivation(with_sign_block: bool) -> Optional[_Derivation]:
        key = "full" if with_sign_block else "plain"
        if key not in _derivation:
            try:
                _derivation[key] = _derive(
                    root, entries, with_sign_block=with_sign_block
                )
            except Exception as exc:  # derivation refusal = a named failure
                _derivation[key] = None
                _derivation[f"{key}_error"] = exc  # type: ignore[assignment]
        return _derivation[key]

    # -- V1 -------------------------------------------------------------------
    if in_scope("V1"):
        errors = list(validator.errors)
        report.checks.append(
            Check(
                "V1 ledger validity — pinned schema, fingerprints "
                "(spec029-phase-i-v1), D-B uniqueness, field "
                "provenance, pointers (Stage 1 validator)",
                "FAIL" if errors else "PASS",
                [f"validator error: {e}" for e in errors]
                or [
                    f"{validator.lines} lines validate against "
                    f"{li.SCHEMA_VERSION}; every fingerprint "
                    "recomputes; no duplicates"
                ],
            )
        )
        # The recorded-source-hash arm (spec.md V1's last
        # clause, extended to every entry: the Stage 1 gap).
        hash_failures: list[str] = []
        checked = 0
        for entry in entries:
            for source in entry.get("sources", []):
                checked += 1
                target = root / source["path"]
                if not target.is_file():
                    hash_failures.append(
                        f"{entry['id']}: source {source['path']} "
                        "not found"
                    )
                elif li.sha256_file(target) != source["sha256"]:
                    hash_failures.append(
                        f"{entry['id']}: recorded sha256 for "
                        f"{source['path']} does not match the "
                        "file on disk under the canonical hash"
                    )
            if entry.get("kind") == "annotation":
                sidecar = entry.get("sidecar") or {}
                if sidecar.get("path") and sidecar.get("sha256"):
                    checked += 1
                    target = root / sidecar["path"]
                    if not target.is_file():
                        hash_failures.append(
                            f"{entry['id']}: sidecar "
                            f"{sidecar['path']} not found"
                        )
                    elif li.sha256_file(target) != sidecar["sha256"]:
                        hash_failures.append(
                            f"{entry['id']}: recorded sidecar "
                            f"sha256 for {sidecar['path']} does "
                            "not match the file on disk"
                        )
        report.checks.append(
            Check(
                "V1 recorded source hashes — every sources[] and "
                "sidecar hash verifies (canonical hash)",
                "FAIL" if hash_failures else "PASS",
                hash_failures
                or [
                    f"{checked} recorded hashes verified against "
                    "the files on disk via "
                    "ledger_intake.sha256_file"
                ],
            )
        )
    else:
        report.checks.append(
            Check("V1 ledger validity", "NOT-RUN",
                  ["out of scope for this run"])
        )
        report.checks.append(
            Check("V1 recorded source hashes", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V2 -------------------------------------------------------------------
    if in_scope("V2"):
        if matrix is None:
            report.checks.append(
                Check("V2 count equivalence", "FAIL",
                      [matrix_error or "matrix unavailable"])
            )
        else:
            rows = matrix.get("rows", [])
            for label, field_name in (
                ("by status", "status"),
                ("by stage", "stage"),
                ("by population", "population"),
            ):
                recomputed = Counter(
                    str(e.get(field_name)) for e in claims
                )
                carried = Counter(str(r.get(field_name)) for r in rows)
                report.checks.append(
                    Check(
                        f"V2 count equivalence — claims {label}: "
                        "ledger == matrix",
                        "PASS" if recomputed == carried else "FAIL",
                        [
                            f"{sum(recomputed.values())} claims; "
                            + (
                                "counts equal"
                                if recomputed == carried
                                else f"ledger {dict(recomputed)} != "
                                f"matrix {dict(carried)}"
                            )
                        ],
                    )
                )
            deriv = derivation(False)
            fc_carried = (matrix.get("coverage") or {}).get(
                "falsifier_coverage"
            )
            fc_recomputed = (
                deriv.coverage["falsifier_coverage"] if deriv else None
            )
            report.checks.append(
                Check(
                    "V2 count equivalence — falsifier coverage "
                    "block: ledger == matrix",
                    "PASS"
                    if fc_recomputed is not None
                    and fc_carried == fc_recomputed
                    else "FAIL",
                    [
                        f"matrix carries {fc_carried}; recomputed "
                        f"{fc_recomputed}"
                    ],
                )
            )
            if map_data is not None:
                header = map_data.get("header", {})
                by_status = Counter(str(e.get("status")) for e in claims)
                carried_status = header.get("claims_by_status")
                report.checks.append(
                    Check(
                        "V2 count equivalence — claims by status: "
                        "ledger == map header",
                        "PASS"
                        if carried_status
                        == {k: v for k, v in by_status.items()}
                        else "FAIL",
                        [
                            f"map header carries {carried_status}",
                            f"census: {len(claims)} claims "
                            f"counted across {len(by_status)} "
                            "statuses in the map header",
                        ],
                    )
                )
            else:
                report.checks.append(
                    Check(
                        "V2 count equivalence — map header leg",
                        "NOT-RUN",
                        [
                            "no map artifact (the map is Stage "
                            "5) and no --candidate-map supplied"
                        ]
                        + ([map_error] if map_error else []),
                    )
                )
    else:
        report.checks.append(
            Check("V2 count equivalence", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V3 -------------------------------------------------------------------
    if in_scope("V3"):
        if matrix is None:
            report.checks.append(
                Check("V3 matrix recomputation", "FAIL",
                      [matrix_error or "matrix unavailable"])
            )
        else:
            deriv = derivation(True)
            if deriv is None:
                exc = _derivation.get("full_error")
                report.checks.append(
                    Check(
                        "V3 matrix recomputation — independent route",
                        "FAIL",
                        [f"the gate's recomputation refused: {exc}"],
                    )
                )
            else:
                reg_failures = list(deriv.registers.mismatches)
                cell_divs: list[str] = []
                _first_divergences(
                    deriv.cells, matrix.get("cells", []), "cells", cell_divs
                )
                report.checks.append(
                    Check(
                        "V3 matrix recomputation — cells "
                        "cell-for-cell (relation, citation ids, "
                        "derivation rule id)",
                        "FAIL" if (cell_divs or reg_failures) else "PASS",
                        [f"register mismatch: {m}" for m in reg_failures]
                        + cell_divs
                        or [
                            f"{len(deriv.cells)} cells recomputed "
                            "from the ledger by the gate's own "
                            "route; every cell equal"
                        ],
                    )
                )
                struct_divs: list[str] = []
                for key, expected in (
                    ("rows", deriv.rows),
                    ("columns", deriv.columns),
                    ("coverage", deriv.coverage),
                    ("as_of", deriv.as_of),
                    ("sign_sign_block", deriv.sign_block),
                ):
                    _first_divergences(
                        expected, matrix.get(key), key, struct_divs
                    )
                report.checks.append(
                    Check(
                        "V3 matrix recomputation — rows, columns, "
                        "coverage, as-of stamp, sign×sign block",
                        "FAIL" if struct_divs else "PASS",
                        struct_divs
                        or [
                            "rows, columns, coverage, the as-of "
                            "stamp and the sign×sign block all "
                            "equal the gate's recomputation"
                        ],
                    )
                )
    else:
        report.checks.append(
            Check("V3 matrix recomputation", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V4 -------------------------------------------------------------------
    if in_scope("V4"):
        ctx = _TieContext(root, entries)
        v4_failures: list[str] = []
        cells_checked = 0
        citations_checked = 0
        if matrix is None:
            v4_failures.append(matrix_error or "matrix unavailable")
        else:
            for cell in matrix.get("cells", []):
                cells_checked += 1
                citations_checked += max(
                    0, len(cell.get("citations") or []) - 1
                )
                for failure in _tie_failures_for_cell(ctx, cell):
                    v4_failures.append(
                        f"cell ({cell['row']} × {cell['column']}, "
                        f"{cell['relation']}, {cell.get('rule')}): "
                        f"{failure}"
                    )
        edges_checked = 0
        if map_data is not None:
            for edge in map_data.get("edges", []):
                edges_checked += 1
                citations_checked += len(edge.get("citations") or [])
                v4_failures.extend(_tie_failures_for_edge(ctx, edge))
        evidence = [
            f"{cells_checked} matrix cells and {edges_checked} "
            f"map edges checked; {citations_checked} citations "
            "required to carry their relation under T1–T4"
        ]
        if ctx.numeric_exercised:
            evidence.append(
                f"numeric arm exercised on {ctx.numeric_exercised} "
                "citation(s) carrying a measurement and a bound"
            )
        else:
            evidence.append(
                "numeric arm: 0 citations in the live population "
                "carry a measurement with a machine-readable "
                "bound (the arm is exercised on fixtures in the "
                "teeth battery)"
            )
        if map_data is not None:
            edge_rels = Counter(
                e.get("rel") for e in map_data.get("edges", [])
            )
            evidence.append(
                "map edge census: "
                + ", ".join(
                    f"{rel} {edge_rels.get(rel, 0)}"
                    for rel in RELATIONS
                )
            )
            if not edge_rels.get("constrains"):
                evidence.append(
                    "UNPROVEN on the live population: "
                    "constrains map edges — 0 live instances "
                    "(the class is empty in the artifact and "
                    "says so; its teeth are fixtures in the "
                    "battery)"
                )
        if ctx.registers.mismatches:
            v4_failures.extend(
                f"register mismatch: {m}"
                for m in ctx.registers.mismatches
            )
        report.checks.append(
            Check(
                "V4 relation-carrying citations — every citation "
                "ties under T1–T4 (incl. the numeric arm)",
                "FAIL" if v4_failures else "PASS",
                v4_failures[:40] + evidence,
            )
        )
    else:
        report.checks.append(
            Check("V4 relation-carrying citations", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V5 -------------------------------------------------------------------
    if in_scope("V5"):
        if map_data is None:
            report.checks.append(
                Check(
                    "V5 map recomputation",
                    "NOT-RUN",
                    [
                        "no map artifact (the map is Stage 5) "
                        "and no --candidate-map supplied"
                    ]
                    + ([map_error] if map_error else []),
                )
            )
        else:
            v5_failures: list[str] = []
            by_id = {e["id"]: e for e in claims}
            column_ids = {
                (c["class"], c["id"])
                for c in (matrix or {}).get("columns", [])
            }
            anchor_keys = set()
            anchors_path = root / ANCHORS_REL
            if anchors_path.is_file():
                anchor_keys = set(
                    json.loads(
                        anchors_path.read_text(encoding="utf-8")
                    ).get("anchors", {})
                )
            for element in map_data.get("elements", []):
                eid = element.get("id")
                kind = element.get("kind")
                if kind == "claim":
                    entry = by_id.get(eid)
                    if entry is None:
                        v5_failures.append(
                            f"element {eid!r}: not a ledger claim"
                        )
                        continue
                    for field_name in (
                        "statement",
                        "status",
                        "stage",
                        "population",
                    ):
                        if field_name in element and element[
                            field_name
                        ] != entry.get(field_name):
                            v5_failures.append(
                                f"element {eid!r}: embedded "
                                f"{field_name} {element[field_name]!r} "
                                f"!= ledger {entry.get(field_name)!r}"
                            )
                elif kind in COLUMN_CLASSES:
                    if (kind, eid) not in column_ids and eid not in anchor_keys:
                        v5_failures.append(
                            f"element {eid!r} ({kind}): traces to "
                            "no matrix column or anchor record"
                        )
                else:
                    v5_failures.append(
                        f"element {eid!r}: unregistered element "
                        f"kind {kind!r}"
                    )
            # The loads block deep-equals the matrix's.
            expected_loads: dict[str, dict[str, int]] = {}
            for row in (matrix or {}).get("rows", []):
                expected_loads[row["id"]] = {
                    rel: 0 for rel in RELATIONS
                }
            for cell in (matrix or {}).get("cells", []):
                if cell["row"] in expected_loads:
                    expected_loads[cell["row"]][cell["relation"]] += 1
            carried_loads = map_data.get("loads")
            if carried_loads != expected_loads:
                divs: list[str] = []
                _first_divergences(
                    expected_loads, carried_loads, "loads", divs
                )
                v5_failures.extend(divs or ["loads block differs"])
            header = map_data.get("header", {})
            stamp = (header.get("as_of") or {}).get("ledger_sha256")
            if stamp != ledger_sha:
                v5_failures.append(
                    f"map header as-of stamp names ledger "
                    f"{stamp}, current ledger is {ledger_sha} "
                    "(stale artifact, D-D)"
                )
            report.checks.append(
                Check(
                    "V5 map recomputation — elements trace, "
                    "embedded fields equal, loads block "
                    "deep-equals the matrix's",
                    "FAIL" if v5_failures else "PASS",
                    v5_failures[:40]
                    or [
                        f"{len(map_data.get('elements', []))} "
                        "elements trace to ledger ids; loads "
                        "block equal"
                    ],
                )
            )
            # The full leg (Stage 5): the whole artifact
            # recomputed by the gate's own route under its
            # registered map-defs v1 copies, section by
            # section — the V3 idiom applied to the map.
            deriv = derivation(True)
            if deriv is None:
                exc = _derivation.get("full_error")
                report.checks.append(
                    Check(
                        "V5 map recomputation — full artifact, "
                        "the gate's own route (map-defs v1 "
                        "copies)",
                        "FAIL",
                        [f"the gate's recomputation refused: {exc}"],
                    )
                )
            else:
                try:
                    shares_for_map = _anchor_shares(root)
                    expected_map, map_failures = _derive_map(
                        root, entries, claims, deriv,
                        shares_for_map, ledger_sha,
                    )
                except (OSError, json.JSONDecodeError,
                        FileNotFoundError) as exc:
                    expected_map, map_failures = None, [str(exc)]
                if expected_map is None:
                    report.checks.append(
                        Check(
                            "V5 map recomputation — full "
                            "artifact, the gate's own route "
                            "(map-defs v1 copies)",
                            "FAIL",
                            [
                                "the gate's map recomputation "
                                f"could not run: {map_failures[0]}"
                            ],
                        )
                    )
                else:
                    divs: list[str] = list(map_failures)
                    for section in (
                        "artifact", "generated_from",
                        "generated_by", "header", "elements",
                        "edges", "loads", "matrix", "system",
                        "claims", "settling",
                    ):
                        _first_divergences(
                            expected_map.get(section),
                            map_data.get(section),
                            section,
                            divs,
                            limit=6,
                        )
                    census = _map_census_lines(expected_map)
                    report.checks.append(
                        Check(
                            "V5 map recomputation — full "
                            "artifact, the gate's own route "
                            "(map-defs v1 copies)",
                            "FAIL" if divs else "PASS",
                            divs[:40] + census
                            if divs
                            else [
                                "every section of the map "
                                "artifact equals the gate's "
                                "recomputation from the ledger "
                                "(header, elements, edges, "
                                "loads, matrix, system, claims, "
                                "settling)"
                            ]
                            + census,
                        )
                    )
    else:
        report.checks.append(
            Check("V5 map recomputation", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V6 -------------------------------------------------------------------
    if in_scope("V6"):
        try:
            shares = _anchor_shares(root)
        except (OSError, json.JSONDecodeError) as exc:
            shares = None
            report.checks.append(
                Check("V6 anchor shares", "FAIL",
                      [f"cannot recompute anchor shares: {exc}"])
            )
        if shares is not None:
            v6_failures: list[str] = []
            if shares["recorded_rule_id"] != STRICT_RULE_ID:
                v6_failures.append(
                    f"anchors file records strict rule "
                    f"{shares['recorded_rule_id']!r}, the gate's "
                    f"registered copy is {STRICT_RULE_ID!r}"
                )
            if shares["recomputed_strict"] != shares["stored_strict"]:
                only_recomputed = sorted(
                    shares["recomputed_strict"] - shares["stored_strict"]
                )
                only_stored = sorted(
                    shares["stored_strict"] - shares["recomputed_strict"]
                )
                v6_failures.append(
                    f"strict set recomputation disagrees with "
                    f"the stored strict_set flags: recomputed-"
                    f"only {only_recomputed[:8]}; stored-only "
                    f"{only_stored[:8]}"
                )
            if shares["recorded_strict_count"] is not None and (
                shares["recorded_strict_count"]
                != len(shares["recomputed_strict"])
            ):
                v6_failures.append(
                    f"recorded strict_count "
                    f"{shares['recorded_strict_count']} != "
                    f"recomputed {len(shares['recomputed_strict'])}"
                )
            out_of_vocab = (
                shares["validation_statuses"] - set(shares["vocabulary"])
                - {None}
            )
            if out_of_vocab:
                v6_failures.append(
                    f"validation_status values outside the "
                    f"recorded vocabulary: {sorted(out_of_vocab)}"
                )
            share = shares["strict_share"]
            report.checks.append(
                Check(
                    "V6 anchor shares — strict set recomputes "
                    "under the recorded D-A rule "
                    f"({STRICT_RULE_ID})",
                    "FAIL" if v6_failures else "PASS",
                    v6_failures
                    or [
                        f"strict anchors: "
                        f"{len(shares['recomputed_strict'])} of "
                        f"{shares['total']}; strict share "
                        f"{share:.4f}; validated-anchor share "
                        f"(the strict share, spec.md Point 5) "
                        f"{share:.4f}; rule version as recorded: "
                        f"{shares['recorded_rule_version']}"
                    ],
                )
            )
            if map_data is not None:
                header = map_data.get("header", {})
                header_failures: list[str] = []
                for field_name in (
                    "validated_anchor_share",
                    "strict_anchor_share",
                ):
                    carried = header.get(field_name)
                    if carried is None or abs(carried - share) > 1e-6:
                        header_failures.append(
                            f"map header {field_name} = "
                            f"{carried}, recomputed {share:.6f}"
                        )
                report.checks.append(
                    Check(
                        "V6 anchor shares — map header leg",
                        "FAIL" if header_failures else "PASS",
                        header_failures
                        or [
                            "map header shares equal the "
                            "recomputation",
                            f"census: the share is computed "
                            f"over {shares['total']} register "
                            f"records, {len(shares['recomputed_strict'])} "
                            "of them strict",
                        ],
                    )
                )
            else:
                report.checks.append(
                    Check(
                        "V6 anchor shares — map header leg",
                        "NOT-RUN",
                        ["no map artifact (Stage 5) and no "
                         "--candidate-map supplied"],
                    )
                )
    else:
        report.checks.append(
            Check("V6 anchor shares", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V7 -------------------------------------------------------------------
    if regen:
        report.checks.extend(
            _regen_checks(
                root, entries, intended_change=intended_change
            )
        )
    elif in_scope("V7"):
        report.checks.append(
            Check(
                "V7 lossless regeneration",
                "NOT-RUN",
                ["runs under --regen (the push CI job runs it)"],
            )
        )
    else:
        report.checks.append(
            Check("V7 lossless regeneration", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V8 -------------------------------------------------------------------
    if in_scope("V8"):
        report.checks.extend(_v8_checks(root, entries, claims))
    else:
        report.checks.append(
            Check("V8 settling canonicals", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V9 -------------------------------------------------------------------
    if in_scope("V9"):
        report.checks.extend(_v9_checks(root))
    else:
        report.checks.append(
            Check("V9 no write path", "NOT-RUN",
                  ["out of scope for this run"])
        )

    return report


def _regen_checks(
    root: Path,
    entries: list[dict[str, Any]],
    *,
    intended_change: Optional[str],
) -> list[Check]:
    """V7 — hash, regenerate with the pure builders only,
    byte-compare, classify. The regeneration route is the
    generator's pure builder (that is what regeneration
    means); V3 above is the independent route."""
    from glossa_lab import matrix_generate as mg

    checks: list[Check] = []
    try:
        build = mg.build_matrix(root)
    except Exception as exc:
        return [
            Check(
                "V7 lossless regeneration — matrix",
                "FAIL",
                [f"regeneration refused: {exc}"],
            )
        ]
    fresh = {"matrix.json": build.json_bytes, "matrix.md": build.md_bytes}
    for name, data in fresh.items():
        target = root / MATRIX_REL_DIR / name
        if not target.is_file():
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "FAIL",
                    [f"published artifact missing: {target}"],
                )
            )
            continue
        before = target.read_bytes()
        before_sha = li.canonical_sha256_bytes(before)
        after_sha = li.canonical_sha256_bytes(data)
        if before == data:
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "PASS",
                    [
                        f"byte-identical after regeneration "
                        f"(sha256 {before_sha})"
                    ],
                )
            )
        elif intended_change:
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "PASS",
                    [
                        f"diff classified: intended-change-named "
                        f"({intended_change}); published sha256 "
                        f"{before_sha}, regenerated {after_sha} "
                        "— republish through the gated path"
                    ],
                )
            )
        else:
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "FAIL",
                    [
                        f"diff classified: downstream-defect — "
                        f"the published artifact is not what the "
                        f"ledger generates (published sha256 "
                        f"{before_sha}, regenerated {after_sha}); "
                        "fixed by regeneration through the gated "
                        "path, never by editing the artifact"
                    ],
                )
            )
    map_path = root / MAP_REL
    if not map_path.is_file():
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "FAIL",
                [f"published artifact missing: {map_path}"],
            )
        )
        return checks
    from glossa_lab import map_generate as mp

    try:
        map_build = mp.build_map(root)
    except Exception as exc:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "FAIL",
                [f"regeneration refused: {exc}"],
            )
        )
        return checks
    before = map_path.read_bytes()
    before_sha = li.canonical_sha256_bytes(before)
    after_sha = li.canonical_sha256_bytes(map_build.json_bytes)
    if before == map_build.json_bytes:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "PASS",
                [
                    f"byte-identical after regeneration "
                    f"(sha256 {before_sha})"
                ],
            )
        )
    elif intended_change:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "PASS",
                [
                    f"diff classified: intended-change-named "
                    f"({intended_change}); published sha256 "
                    f"{before_sha}, regenerated {after_sha} "
                    "— republish through the gated path"
                ],
            )
        )
    else:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "FAIL",
                [
                    f"diff classified: downstream-defect — "
                    f"the published artifact is not what the "
                    f"ledger generates (published sha256 "
                    f"{before_sha}, regenerated {after_sha}); "
                    "fixed by regeneration through the gated "
                    "path, never by editing the artifact"
                ],
            )
        )
    return checks
