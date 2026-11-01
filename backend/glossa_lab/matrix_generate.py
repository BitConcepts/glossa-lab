"""Spec 086 Stage 2 — the claims×evidence matrix generator.

Implements Point 2 of the winning-combination adoption: the
matrix is **generated, never made**. The sole entry point is
the ledger (`glossa-indus/ledger/claims.jsonl`); every cell
traces to a ledger entry and arises from exactly one
registered derivation rule in `glossa-indus/matrix/
DEFINITIONS.md` (`matrix-defs v1`), whose machine copy is
registered below. The generator reads only the registers
DEFINITIONS.md §1 names: the ledger, the source records the
entries name in `sources[]` (read only after their canonical
hash verifies against the hash the entry records), the
canonical anchors file, the research-check sidecars named by
annotation entries, and the corpus snapshot (for the
sign×sign block, imported from the existing co-occurrence
pipeline — no new co-occurrence code).

Structure (harmonization adoption 3, item 5 — binding):
`build_matrix` is a PURE builder: it computes the artifact
bytes in memory and writes nothing. `write_matrix` is the
thin write wrapper used only by the generate command
(`tools/ledger/generate_matrix.py`). Gates and regen checks
(Stage 3) call only the pure builder and compare against
committed bytes.

Refusals: a source file whose hash does not match the
ledger's record, an evidence item whose direction is not
registered, or two stored directions for one (claim, ref)
that conflict, each refuse generation with a named error —
a defect in the record is repaired at the source, never
generated around.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from glossa_lab import ledger_intake as li

# ---------------------------------------------------------------------------
# Registered definitions — machine copy of
# glossa-indus/matrix/DEFINITIONS.md (matrix-defs v1).
# A deliberate change is made in both copies in the same
# motion (DEFINITIONS.md §12).

MATRIX_DEFS_VERSION = "matrix-defs v1"
MATRIX_REL_DIR = "glossa-indus/matrix"
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
CORPUS_REL = "glossa-corpus/indus/exports/indus_research.jsonl"

RELATIONS = ("supports", "opposes", "constrains")

# Column classes in registered order (DEFINITIONS.md §3).
COLUMN_CLASSES = (
    "studies",
    "documents",
    "research_checks",
    "anchors",
    "corpus_texts",
)

# Derivation rules (DEFINITIONS.md §5).
RULES = {
    "R1": "evidence instance (documents, supports)",
    "R2": "bundle evidence direction (documents, per stored direction)",
    "R3": "study outcome (studies, per the outcome table)",
    "R4": "anchor assignment (anchors, constrains)",
    "R5": "research-check verdict (research checks; verdict table empty in v1)",
    "R6": "settling instrument (constrains; instrument register empty in v1)",
}

# R2 direction table (DEFINITIONS.md §5, R2): the stored
# direction string maps to the relation of the same name.
DIRECTION_RELATIONS = {
    "supports": "supports",
    "opposes": "opposes",
    "constrains": "constrains",
}

# R3 outcome table (DEFINITIONS.md §6): an exact recorded
# outcome string in this table bears on the claim with the
# mapped relation. Every other outcome string is
# non-bearing. There is no supports entry in v1.
BEARING_OUTCOMES = {
    "NOT SUPPORTED": "opposes",
    "INCONSISTENT": "opposes",
    "NOT NUMERAL-LIKE": "opposes",
}

# R5 verdict table (DEFINITIONS.md §5, R5): empty in v1 —
# no verdict vocabulary is registered, because the sidecar
# population states no verdicts (all bearings carry
# verdict: null) and a research check is advisory.
VERDICT_RELATIONS: dict[str, str] = {}

# Sign×sign block: the existing pipeline with the
# analyze_script.py §6 call site's parameters
# (DEFINITIONS.md §8); remaining parameters at the
# pipeline's defaults.
COOCCURRENCE_PARAMS = {"window": 2, "min_freq": 3, "min_edge_weight": 2}
COOCCURRENCE_PIPELINE = "glossa_lab.pipelines.cooccurrence.build_cooccurrence_network"


class MatrixBuildError(RuntimeError):
    """Generation refuses: a defect in the ledger or a
    register, named. Nothing is written."""


@dataclass
class MatrixBuild:
    json_bytes: bytes
    md_bytes: bytes
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

    def records(self, rel_path: str) -> list[dict[str, Any]]:
        data = self._parsed.get(rel_path)
        return _records_of(data) if data is not None else []

    def raise_if_mismatched(self) -> None:
        if self.mismatches:
            named = "\n  ".join(sorted(set(self.mismatches)))
            raise MatrixBuildError(
                "source verification failed — the records on disk "
                "are not the records the ledger mirrors:\n  " + named
            )


# ---------------------------------------------------------------------------
# Cell derivation


@dataclass
class _Cell:
    row: str
    column: str
    column_class: str
    relation: str
    rule: str
    citations: list[str] = field(default_factory=list)

    def add_citation(self, citation: str) -> None:
        if citation not in self.citations:
            self.citations.append(citation)

    def as_dict(self) -> dict[str, Any]:
        return {
            "row": self.row,
            "column": self.column,
            "column_class": self.column_class,
            "relation": self.relation,
            "rule": self.rule,
            "citations": self.citations,
        }


def _source_record(
    registers: _Registers, entry: dict[str, Any], role: str
) -> Optional[dict[str, Any]]:
    for source in entry.get("sources", []):
        if source.get("role") == role:
            return registers.record(source["path"], source["claim_id"])
    return None


def build_matrix(root: Path) -> MatrixBuild:
    """Pure builder: compute the matrix artifacts in memory
    from the ledger and its registers. Writes nothing."""
    root = Path(root)
    entries = li.read_ledger(root / li.LEDGER_REL)
    claims = [e for e in entries if e.get("kind") == "claim"]
    annotations = [e for e in entries if e.get("kind") == "annotation"]
    claim_ids = {e["id"] for e in claims}

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
        raise MatrixBuildError(f"anchors register not found: {ANCHORS_REL}")
    anchors = json.loads(anchors_path.read_text(encoding="utf-8")).get(
        "anchors", {}
    )

    cells: dict[tuple[str, str, str], _Cell] = {}
    study_columns: set[str] = set()
    document_columns: set[str] = set()
    non_bearing_blocks: list[dict[str, Any]] = []
    unresolved_anchor_refs: list[dict[str, Any]] = []

    def put(cell: _Cell) -> _Cell:
        key = (cell.row, cell.column_class, cell.column)
        existing = cells.get(key)
        if existing is None:
            cells[key] = cell
            return cell
        if existing.relation != cell.relation or existing.rule != cell.rule:
            raise MatrixBuildError(
                f"conflicting derivations for ({cell.row} x "
                f"{cell.column}): {existing.rule}/{existing.relation} "
                f"vs {cell.rule}/{cell.relation} — a contradiction "
                "in the record, repaired at the source"
            )
        for citation in cell.citations:
            existing.add_citation(citation)
        return existing

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
                if inst_id and inst_id not in entry.get("evidence_refs", []):
                    raise MatrixBuildError(
                        f"{eid}: evidence instance {inst_id} is not "
                        "carried in the ledger entry's evidence_refs — "
                        "the ledger does not mirror its source record"
                    )
                document_columns.add(str(doc))
                put(
                    _Cell(
                        eid,
                        str(doc),
                        "documents",
                        "supports",
                        "R1",
                        [eid, str(inst_id)] if inst_id else [eid],
                    )
                )

        # R2 — bundle evidence direction (bundle population).
        if entry.get("population") == "bundle" and sor is not None:
            by_ref: dict[str, _Cell] = {}
            for item in sor.get("evidence") or []:
                if not isinstance(item, dict) or not item.get("ref"):
                    continue
                ref = str(item["ref"])
                if ref not in entry.get("evidence_refs", []):
                    raise MatrixBuildError(
                        f"{eid}: evidence ref {ref} is not carried in "
                        "the ledger entry's evidence_refs — the ledger "
                        "does not mirror its source record"
                    )
                direction = item.get("direction")
                if direction not in DIRECTION_RELATIONS:
                    raise MatrixBuildError(
                        f"{eid}: evidence item {ref} carries "
                        f"unregistered direction {direction!r} — "
                        "register it in matrix-defs before generating"
                    )
                document_columns.add(ref)
                cell = by_ref.get(ref)
                if cell is None:
                    cell = _Cell(
                        eid,
                        ref,
                        "documents",
                        DIRECTION_RELATIONS[str(direction)],
                        "R2",
                        [eid, ref],
                    )
                    by_ref[ref] = cell
                elif cell.relation != DIRECTION_RELATIONS[str(direction)]:
                    raise MatrixBuildError(
                        f"{eid}: conflicting stored directions for "
                        f"evidence ref {ref} — a contradiction in "
                        "the record, repaired at the source"
                    )
            for cell in by_ref.values():
                put(cell)

        # R3 — study outcomes (any population; the stored
        # blocks live on extracted claims' records today).
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
                    study_columns.add(spec)
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
        for spec in sorted(blocks_by_spec):
            blocks = blocks_by_spec[spec]
            ordered = sorted(
                blocks, key=lambda b: (str(b["date"] or ""), b["pointer"])
            )
            governing = ordered[-1]
            relation = BEARING_OUTCOMES.get(governing["outcome"])
            if relation is not None:
                put(
                    _Cell(
                        eid,
                        spec,
                        "studies",
                        relation,
                        "R3",
                        [eid] + [b["pointer"] for b in ordered],
                    )
                )
                for block in ordered[:-1]:
                    non_bearing_blocks.append(
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
                    reason = (
                        "governing outcome is non-bearing"
                        if block is governing
                        else "superseded by a later outcome block "
                        "from the same study"
                    )
                    non_bearing_blocks.append(
                        {
                            "row": eid,
                            "study": spec,
                            "outcome": block["outcome"],
                            "date": block["date"],
                            "pointer": block["pointer"],
                            "reason": reason,
                        }
                    )

        # R4 — anchor assignment (constrains).
        for sign_ref in entry.get("sign_refs") or []:
            frame, _, value = str(sign_ref).partition(":")
            anchor_key = f"M{value}" if frame == "mahadevan" else None
            anchor = anchors.get(anchor_key) if anchor_key else None
            if anchor is not None and anchor.get("reading"):
                put(
                    _Cell(
                        eid,
                        anchor_key,
                        "anchors",
                        "constrains",
                        "R4",
                        [eid, anchor_key],
                    )
                )
            else:
                if frame != "mahadevan":
                    reason = f"frame {frame!r} has no anchor-register mapping in matrix-defs v1"
                elif anchor is None:
                    reason = "no anchor record under this key"
                else:
                    reason = "anchor record carries no recorded reading"
                unresolved_anchor_refs.append(
                    {"row": eid, "sign_ref": str(sign_ref), "reason": reason}
                )

    # R5 — research-check verdicts (research checks).
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
                _Cell(
                    str(target),
                    str(sidecar),
                    "research_checks",
                    relation,
                    "R5",
                    [str(target), annotation["id"]],
                )
            )

    # R6 — settling instruments: the register is empty in
    # matrix-defs v1 (no glossa-settle-1 records exist until
    # Stage 4); the rule is registered and yields nothing.

    # ------------------------------------------------------------------
    # Coverage inputs (DEFINITIONS.md §7)

    cell_list = sorted(
        cells.values(), key=lambda c: (c.row, c.column_class, c.column)
    )
    rows_with_cells = {c.row for c in cell_list}
    empty_rows = [e["id"] for e in claims if e["id"] not in rows_with_cells]

    columns_by_class: dict[str, list[str]] = {
        "studies": sorted(study_columns),
        "documents": sorted(document_columns),
        "research_checks": sorted(research_check_columns),
        "anchors": sorted(anchors.keys()),
        "corpus_texts": [],
    }
    borne_columns = {(c.column_class, c.column) for c in cell_list}
    unused_columns = {
        cls: [c for c in cols if (cls, c) not in borne_columns]
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

    # Unresolved sign mentions: free-text signs_involved on
    # every extracted-claims record the ledger names.
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

    # Dependency pairs carried in evidence_refs (not cells
    # under matrix-defs v1; recorded, not dropped).
    dependency_pairs: list[dict[str, str]] = []
    for entry in claims:
        spec_prefix = entry["id"].rsplit("/", 1)[0] if "/" in entry["id"] else None
        for ref in entry.get("evidence_refs") or []:
            target = None
            if ref in claim_ids:
                target = ref
            elif spec_prefix and f"{spec_prefix}/{ref}" in claim_ids:
                target = f"{spec_prefix}/{ref}"
            if target and target != entry["id"]:
                dependency_pairs.append({"from": entry["id"], "to": target})
    dependency_pairs.sort(key=lambda p: (p["from"], p["to"]))

    non_bearing_blocks.sort(
        key=lambda b: (b["row"], b["study"], str(b["date"] or ""), b["pointer"])
    )
    unresolved_anchor_refs.sort(key=lambda u: (u["row"], u["sign_ref"]))

    coverage = {
        "rows_total": len(claims),
        "rows_with_cells": len(rows_with_cells),
        "empty_rows": empty_rows,
        "columns_by_class": {
            cls: len(cols) for cls, cols in columns_by_class.items()
        },
        "unused_columns": unused_columns,
        "cells_total": len(cell_list),
        "cells_by_relation": {
            rel: sum(1 for c in cell_list if c.relation == rel)
            for rel in RELATIONS
        },
        "cells_by_class": {
            cls: sum(1 for c in cell_list if c.column_class == cls)
            for cls in COLUMN_CLASSES
        },
        "falsifier_coverage": falsifier_coverage,
        "unresolved_sign_mentions": unresolved_mentions,
        "sign_refs_without_anchor_record": unresolved_anchor_refs,
        "study_outcome_blocks_not_bearing": non_bearing_blocks,
        "dependency_pairs_not_cells": dependency_pairs,
    }

    sign_block = _sign_sign_block(root)

    ledger_bytes = (root / li.LEDGER_REL).read_bytes()
    as_of = {
        "ledger_sha256": li.canonical_sha256_bytes(ledger_bytes),
        "ledger_lines": len(entries),
        "ledger_date": max((str(e.get("date")) for e in entries), default=None),
        "ledger_schema": li.SCHEMA_VERSION,
        "matrix_defs": MATRIX_DEFS_VERSION,
    }

    matrix = {
        "artifact": "glossa-indus claims×evidence matrix",
        "generated_from": li.LEDGER_REL,
        "generated_by": "tools/ledger/generate_matrix.py "
        "(backend/glossa_lab/matrix_generate.py)",
        "as_of": as_of,
        "rows": [
            {
                "id": e["id"],
                "population": e.get("population"),
                "status": e.get("status"),
                "stage": e.get("stage"),
            }
            for e in claims
        ],
        "columns": [
            {"id": column, "class": cls}
            for cls in COLUMN_CLASSES
            for column in columns_by_class[cls]
        ],
        "cells": [c.as_dict() for c in cell_list],
        "coverage": coverage,
        "sign_sign_block": sign_block,
    }
    json_bytes = (
        json.dumps(matrix, ensure_ascii=False, indent=1).encode("utf-8") + b"\n"
    )

    output = _render_output(as_of, coverage, sign_block)
    md_bytes = (
        _render_md(matrix, output).encode("utf-8")
    )
    stats = {
        "cells": len(cell_list),
        "rows": len(claims),
        "columns": sum(len(c) for c in columns_by_class.values()),
        "ledger_sha256": as_of["ledger_sha256"],
    }
    return MatrixBuild(
        json_bytes=json_bytes, md_bytes=md_bytes, output=output, stats=stats
    )


# ---------------------------------------------------------------------------
# The sign×sign block (imported from the existing pipeline)


def _sign_sign_block(root: Path) -> dict[str, Any]:
    corpus_path = root / CORPUS_REL
    if not corpus_path.is_file():
        raise MatrixBuildError(f"corpus snapshot not found: {CORPUS_REL}")
    corpus_hash = li.sha256_file(corpus_path)

    from glossa_lab.data import indus_corpus_v2
    from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network

    status = indus_corpus_v2.corpus_status()
    tier = str(status.get("tier", ""))
    if not tier.startswith("real-corpus"):
        raise MatrixBuildError(
            f"corpus loader tier is {tier!r}, not the real corpus — "
            "refusing to import a co-occurrence block computed over "
            "a fallback or synthetic corpus"
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
# Rendering (the printed output and matrix.md share the coverage text)


def _render_output(
    as_of: dict[str, Any],
    coverage: dict[str, Any],
    sign_block: dict[str, Any],
) -> str:
    fc = coverage["falsifier_coverage"]
    lines = [
        "Matrix generation — glossa-indus/matrix/ "
        f"({as_of['matrix_defs']}; {as_of['ledger_schema']})",
        f"generated from: {li.LEDGER_REL}",
        f"ledger sha256: {as_of['ledger_sha256']}",
        f"ledger lines: {as_of['ledger_lines']}; "
        f"ledger date: {as_of['ledger_date']}",
        f"rows: {coverage['rows_total']} claims "
        f"({coverage['rows_with_cells']} with at least one cell; "
        f"{len(coverage['empty_rows'])} empty)",
        "columns: "
        + ", ".join(
            f"{cls} {n}" for cls, n in coverage["columns_by_class"].items()
        ),
        f"cells: {coverage['cells_total']} "
        + "("
        + ", ".join(
            f"{rel} {n}" for rel, n in coverage["cells_by_relation"].items()
        )
        + ")",
        "cells by class: "
        + ", ".join(
            f"{cls} {n}" for cls, n in coverage["cells_by_class"].items()
        ),
        f"falsifier coverage: {fc['covered']} of {fc['total']} "
        "claim entries carry a falsifier",
        "falsifier coverage by population: "
        + ", ".join(
            f"{pop} {b['covered']}/{b['total']}"
            for pop, b in sorted(fc["by_population"].items())
        ),
        "Coverage",
        f"empty rows: {len(coverage['empty_rows'])}",
    ]
    if coverage["empty_rows"]:
        lines.append("  " + ", ".join(coverage["empty_rows"]))
    for cls in COLUMN_CLASSES:
        unused = coverage["unused_columns"][cls]
        total = coverage["columns_by_class"][cls]
        lines.append(f"unused columns ({cls}): {len(unused)} of {total}")
        if unused:
            lines.append("  " + ", ".join(unused))
    lines.append(
        "unresolved sign mentions: "
        f"{len(coverage['unresolved_sign_mentions'])}"
    )
    for mention in coverage["unresolved_sign_mentions"]:
        lines.append(
            f"  {mention['record']}: {mention['mention']} "
            f"({mention['source']})"
        )
    lines.append(
        "sign refs without an anchor record: "
        f"{len(coverage['sign_refs_without_anchor_record'])}"
    )
    for item in coverage["sign_refs_without_anchor_record"]:
        lines.append(
            f"  {item['row']}: {item['sign_ref']} — {item['reason']}"
        )
    lines.append(
        "study outcome blocks not bearing: "
        f"{len(coverage['study_outcome_blocks_not_bearing'])}"
    )
    for block in coverage["study_outcome_blocks_not_bearing"]:
        lines.append(
            f"  {block['row']} x study {block['study']}: "
            f"{block['outcome']} ({block['date']}) — {block['reason']} "
            f"[{block['pointer']}]"
        )
    lines.append(
        "dependency pairs carried in evidence_refs "
        "(not matrix cells under matrix-defs v1): "
        f"{len(coverage['dependency_pairs_not_cells'])}"
    )
    src = sign_block["source"]
    lines += [
        "Sign×sign block (imported from the existing pipeline)",
        f"pipeline: {src['pipeline']} {src['parameters']}",
        f"corpus: {src['corpus']} sha256 {src['corpus_sha256']}",
        f"sequences: {src['sequences']}; sign tokens: {src['sign_tokens']}",
        f"nodes: {sign_block['node_count']}; "
        f"edges: {sign_block['edge_count']} reported by the pipeline "
        f"({sign_block['edges_emitted']} edge records emitted); "
        f"communities: {sign_block['community_count']}",
        "RESULT: GENERATED",
    ]
    return "\n".join(lines) + "\n"


def _render_md(matrix: dict[str, Any], output: str) -> str:
    as_of = matrix["as_of"]
    coverage = matrix["coverage"]
    sign_block = matrix["sign_sign_block"]
    lines = [
        "# Glossa Indus — claims×evidence matrix",
        "",
        "Generated from `glossa-indus/ledger/claims.jsonl` by "
        "`tools/ledger/generate_matrix.py`. Do not hand-edit; "
        "regenerate.",
        "",
        f"Definitions: {as_of['matrix_defs']} "
        "(`glossa-indus/matrix/DEFINITIONS.md`). "
        f"Ledger schema: {as_of['ledger_schema']}.",
        f"As-of: ledger sha256 `{as_of['ledger_sha256']}`; "
        f"{as_of['ledger_lines']} ledger lines; "
        f"ledger date {as_of['ledger_date']}.",
        "",
        f"Rows: {coverage['rows_total']} claims. "
        f"Cells: {coverage['cells_total']} ("
        + ", ".join(
            f"{rel} {n}" for rel, n in coverage["cells_by_relation"].items()
        )
        + ").",
        "",
        "## Cells by column class",
        "",
        "| Class | Columns | Borne | Cells | Supports | Opposes | Constrains |",
        "|---|---|---|---|---|---|---|",
    ]
    cell_list = matrix["cells"]
    for cls in COLUMN_CLASSES:
        cls_cells = [c for c in cell_list if c["column_class"] == cls]
        borne = len({c["column"] for c in cls_cells})
        counts = {
            rel: sum(1 for c in cls_cells if c["relation"] == rel)
            for rel in RELATIONS
        }
        lines.append(
            f"| {cls} | {coverage['columns_by_class'][cls]} | {borne} | "
            f"{len(cls_cells)} | {counts['supports']} | "
            f"{counts['opposes']} | {counts['constrains']} |"
        )
    lines += ["", "## Borne columns", ""]
    for cls in COLUMN_CLASSES:
        borne_cols = sorted({c["column"] for c in cell_list if c["column_class"] == cls})
        if not borne_cols:
            continue
        lines.append(f"### {cls}")
        lines.append("")
        lines.append("| Column | Cells | Supports | Opposes | Constrains |")
        lines.append("|---|---|---|---|---|")
        for column in borne_cols:
            col_cells = [
                c
                for c in cell_list
                if c["column_class"] == cls and c["column"] == column
            ]
            counts = {
                rel: sum(1 for c in col_cells if c["relation"] == rel)
                for rel in RELATIONS
            }
            lines.append(
                f"| {column} | {len(col_cells)} | {counts['supports']} | "
                f"{counts['opposes']} | {counts['constrains']} |"
            )
        lines.append("")
    lines += [
        "## Generator output (verbatim, including the coverage block)",
        "",
        "```text",
        output.rstrip("\n"),
        "```",
        "",
        "## Sign×sign block",
        "",
        f"Imported from `{sign_block['source']['pipeline']}` over "
        f"`{sign_block['source']['corpus']}` (sha256 "
        f"`{sign_block['source']['corpus_sha256']}`): "
        f"{sign_block['node_count']} nodes, "
        f"{sign_block['edge_count']} edges, "
        f"{sign_block['community_count']} communities. "
        "The full block (nodes, edges, communities, provenance) "
        "is in `matrix.json`.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Write wrapper (the only write path; used by the generate command)


def write_matrix(
    root: Path, out_dir: Optional[Path] = None
) -> dict[str, Any]:
    """Thin wrapper over the pure builder: build, write the
    two artifacts with pinned LF bytes, read back and verify."""
    root = Path(root)
    build = build_matrix(root)
    out = Path(out_dir) if out_dir else (root / MATRIX_REL_DIR)
    out.mkdir(parents=True, exist_ok=True)
    written = {}
    for name, data in (
        ("matrix.json", build.json_bytes),
        ("matrix.md", build.md_bytes),
    ):
        target = out / name
        target.write_bytes(data)
        read_back = target.read_bytes()
        if read_back != data:
            raise MatrixBuildError(
                f"write verification failed for {target}: read-back "
                "bytes differ from the built bytes"
            )
        written[name] = {
            "path": str(target),
            "sha256": li.canonical_sha256_bytes(read_back),
            "bytes": len(read_back),
        }
    return {"build": build, "written": written}
