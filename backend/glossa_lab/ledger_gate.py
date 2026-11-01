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
regeneration (checked mode, `--regen`), V9 no write path.
V8 (settling canonicals) arrives with Stage 4 and is
enumerated as NOT-RUN until then.

**The gate never writes.** It calls only pure builders and
read paths; it imports no write entry point (V9 audits this
in the gate's own source). Publication lives in
`gated_publish.py`, which writes candidates, runs this gate
against them, and replaces the published artifacts only on
ALL PASS (C086-11).
"""

from __future__ import annotations

import ast
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

# The numeric arm's registered comparator vocabulary
# (harmonization adoption 3, item 2 — the Atlas's
# claim.measurement shape: value / comparator / bound).
NUMERIC_COMPARATORS = ("<=", ">=", "=", "in")

WRITE_ENTRY_POINTS = ("append_entry", "write_ledger", "write_matrix")
REGISTERED_WRITERS = {
    "backend/glossa_lab/matrix_generate.py",
    "backend/glossa_lab/gated_publish.py",
    "tools/ledger/generate_matrix.py",
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
                        [f"map header carries {carried_status}"],
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
                        or ["map header shares equal the recomputation"],
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
    report.checks.append(
        Check(
            "V8 settling canonicals",
            "NOT-RUN",
            ["arrives with Stage 4 (the settling engine)"],
        )
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
    if map_path.is_file():
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "FAIL",
                [
                    "a map artifact exists but no map builder "
                    "is registered until Stage 5; it cannot be "
                    "regenerated, so it cannot be verified "
                    "lossless"
                ],
            )
        )
    else:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "NOT-RUN",
                ["no map artifact exists (Stage 5)"],
            )
        )
    return checks
