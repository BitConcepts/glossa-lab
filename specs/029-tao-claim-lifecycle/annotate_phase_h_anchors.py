"""Spec 029 Phase H — anchor annotation and schema validation (D-A).

Run from the repo root with the Glossa venv:

    # dry run (writes nothing; emits the reconciliation report)
    python specs/029-tao-claim-lifecycle/annotate_phase_h_anchors.py --dry-run

    # live run (snapshots the anchors file first, then annotates)
    python specs/029-tao-claim-lifecycle/annotate_phase_h_anchors.py \
        --live --snapshot-dir /path/to/snapshots

    # post-run verification / CI validator core (read-only)
    python specs/029-tao-claim-lifecycle/annotate_phase_h_anchors.py --verify

D-A (ratified 2026-10-12) annotates the canonical anchors file
``backend/reports/INDUS_FINAL_ANCHORS.json`` in place, additively,
and pins its declared schema — it never demotes a tier and never
alters a pre-existing field:

- H1: ``validation_status`` is made total. A value already present
  is preserved verbatim; where the field is absent, the value the
  record's own provenance establishes is made explicit (see
  ``derive_validation_status`` and the vocabulary declared in
  ``anchors-schema.json``).
- H2: every record gains a boolean ``strict_set`` flag computed by
  the Phase-108 provenance register + Phase-109 rule join — the
  program's own ``strict_sa_independent_hm``, imported here, never
  re-implemented. The rule's identifier and version are recorded
  in the file metadata (``metadata.spec029_phase_h_annotation``).
  Both stored values are caches recomputable from the record's
  register evidence; the validator below recomputes them.
- H3/H4: the declared schema is ``anchors-schema.json`` in this
  directory; ``validate_anchors_doc`` is the validator core the
  backend test suite runs in CI — it fails on any record whose
  shape is undeclared under the schema, any missing or
  out-of-vocabulary ``validation_status``, any ``strict_set`` that
  disagrees with its recomputation, and any strict count other
  than 94 (90 HIGH + 4 MEDIUM), matching the audit exactly.

Additive only, asserted before writing: removing exactly the
Phase H annotation (``strict_set`` on every record, the
``validation_status`` values this pass assigns, and the metadata
annotation block) from the annotated document reproduces the
pre-run bytes (Phase-D-stamped SHA-256 ``18e6f4b2…``). The pass
is idempotent: a second run over the annotated file is a no-op
and says so; a partial or conflicting annotation stops the run
with a non-zero exit — nothing is smoothed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.pipelines.phase109_followthrough import (
    SA_LINEAGE_CATEGORIES,
    strict_sa_independent_hm,
)

SPEC_DIR = REPO / "specs" / "029-tao-claim-lifecycle"
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
REGISTER_PATH = REPO / "reports" / "phase108_provenance_register.json"
SCHEMA_PATH = SPEC_DIR / "anchors-schema.json"

ANNOTATION_DATE = "2026-10-12"
METADATA_KEY = "spec029_phase_h_annotation"
#: The anchors file's SHA-256 as Phase D left it (the pre-Phase-H
#: state this annotation starts from and must reproduce on strip).
PHASE_D_ANCHORS_SHA256 = (
    "18e6f4b2caa7bc9ae1f5cc92dd96f95ce191a77c56144b95820a368d75a316d6")

#: Values this pass assigns (the 130 records that carried no
#: ``validation_status``). Records already carrying a value keep it
#: verbatim (H1); those pre-existing values are disjoint from these.
NEW_VALUES = ("strict_sa_independent", "sa_in_provenance_chain",
              "no_validation_record")
PRE_EXISTING_VALUES = ("pending_non_sa_validation", "premise_superseded")
VOCABULARY = NEW_VALUES + PRE_EXISTING_VALUES

#: H2 reconciliation (audit §2/§3, tasks H2): strict count and
#: composition must match the audit exactly, or the phase stops.
EXPECTED_TOTAL = 287
EXPECTED_STRICT_COUNT = 94
EXPECTED_STRICT_COMPOSITION = {"HIGH": 90, "MEDIUM": 4}
EXPECTED_VALUE_COUNTS = {
    "strict_sa_independent": 94,
    "sa_in_provenance_chain": 33,
    "no_validation_record": 3,
    "pending_non_sa_validation": 44,
    "premise_superseded": 113,
}

STRICT_RULE = {
    "rule_id": "strict_sa_independent_hm",
    "rule_source": ("backend/glossa_lab/pipelines/"
                    "phase109_followthrough.py:strict_sa_independent_hm"),
    "rule_version": ("Phase-109 follow-through (spec 007, 2026-10-06) "
                     "applying the Phase-108 strict definition"),
    "register": "reports/phase108_provenance_register.json",
    "definition": ("confidence in {HIGH, MEDIUM} AND register category "
                   "not in {SA_DERIVED, SA_CONFIRMED_ONLY} AND register "
                   "sa_in_chain is false"),
}


class AnnotationError(RuntimeError):
    """The annotation stops; nothing is smoothed or partially written."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(data: Any) -> str:
    """The file's canonical serialization (indent=2, no trailing newline)."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def load_register() -> dict[str, dict]:
    return json.loads(REGISTER_PATH.read_text("utf-8"))["records"]


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text("utf-8"))


def load_anchors_doc() -> dict[str, Any]:
    return json.loads(ANCHORS_PATH.read_text("utf-8"))


def compute_strict_set(anchors: dict[str, dict],
                       records: dict[str, dict]) -> set[str]:
    """The H2 rule join: the Phase-109 strict rule itself, applied
    to the live anchors mapping over the Phase-108 register."""
    return strict_sa_independent_hm(anchors, records)


def derive_from_provenance(record: dict[str, Any],
                           register_record: dict[str, Any] | None,
                           in_strict_set: bool) -> str:
    """The validation value a record's own provenance establishes,
    ignoring any value the record already carries: the strict rule
    first, then the register's SA-in-chain fact, then the honest
    absence of any validation record."""
    if in_strict_set:
        return "strict_sa_independent"
    if register_record is not None and register_record.get("sa_in_chain"):
        return "sa_in_provenance_chain"
    return "no_validation_record"


def derive_validation_status(record: dict[str, Any],
                             register_record: dict[str, Any] | None,
                             in_strict_set: bool) -> str:
    """H1's rule: an existing value is preserved verbatim; an absent
    field is made explicit from the record's own provenance."""
    existing = record.get("validation_status")
    if existing is not None:
        return existing
    return derive_from_provenance(record, register_record, in_strict_set)


def metadata_block() -> dict[str, Any]:
    """The file-level metadata H2 requires: the strict rule's
    identifier and version, the declared vocabulary, and the
    schema this annotation is governed by."""
    return {
        "spec": "specs/029-tao-claim-lifecycle (Phase H, D-A)",
        "date": ANNOTATION_DATE,
        "schema": "specs/029-tao-claim-lifecycle/anchors-schema.json",
        "annotation_script": ("specs/029-tao-claim-lifecycle/"
                              "annotate_phase_h_anchors.py"),
        "validation_status_vocabulary": sorted(VOCABULARY),
        "strict_set_rule": dict(STRICT_RULE, strict_count=EXPECTED_STRICT_COUNT),
    }


def annotate_record(record: dict[str, Any],
                    register_record: dict[str, Any] | None,
                    in_strict_set: bool) -> None:
    """Add the Phase H fields to one record, in place. Key order is
    append-only: a derived ``validation_status`` lands after the
    record's existing keys, then ``strict_set``."""
    if "validation_status" not in record:
        record["validation_status"] = derive_from_provenance(
            record, register_record, in_strict_set)
    record["strict_set"] = in_strict_set


def record_state(record: dict[str, Any],
                 register_record: dict[str, Any] | None,
                 in_strict_set: bool) -> str:
    """``annotated`` / ``unannotated`` / ``conflict`` for one record."""
    has_flag = "strict_set" in record
    value = record.get("validation_status")
    if not has_flag:
        if value is None or value in PRE_EXISTING_VALUES:
            return "unannotated"
        return "conflict"  # a Phase H value without its flag: partial
    expected_value = derive_validation_status(record, register_record,
                                              in_strict_set)
    if record["strict_set"] is in_strict_set and value == expected_value:
        return "annotated"
    return "conflict"


def annotate_doc(doc: dict[str, Any],
                 records: dict[str, dict]) -> list[dict[str, Any]]:
    """Annotate a whole anchors document in place; returns the
    per-record change list. Assumes the population state check
    (``plan``) has already passed."""
    anchors = doc["anchors"]
    strict = compute_strict_set(anchors, records)
    changes: list[dict[str, Any]] = []
    for sign in sorted(anchors):
        record = anchors[sign]
        before_value = record.get("validation_status")
        annotate_record(record, records.get(sign), sign in strict)
        changes.append({
            "sign": sign,
            "validation_status_before": before_value,
            "validation_status_after": record["validation_status"],
            "validation_status_assigned": before_value is None,
            "strict_set": record["strict_set"],
        })
    doc.setdefault("metadata", {})[METADATA_KEY] = metadata_block()
    return changes


def strip_phase_h(doc: dict[str, Any]) -> dict[str, Any]:
    """The Phase-D-stamped document: the Phase H annotation removed
    (``strict_set`` everywhere; the ``validation_status`` values
    this pass assigns — pre-existing values are untouched; the
    metadata annotation block). Canonical-comparison primitive."""
    stripped = copy.deepcopy(doc)
    for record in stripped.get("anchors", {}).values():
        record.pop("strict_set", None)
        if record.get("validation_status") in NEW_VALUES:
            record.pop("validation_status", None)
    stripped.get("metadata", {}).pop(METADATA_KEY, None)
    return stripped


def reconcile_counts(doc: dict[str, Any],
                     records: dict[str, dict]) -> dict[str, Any]:
    """The H1/H2 reconciliation against the audit's figures."""
    anchors = doc.get("anchors", {})
    strict_stored = {s for s, r in anchors.items() if r.get("strict_set")}
    strict_computed = compute_strict_set(anchors, records)
    value_counts = dict(Counter(r.get("validation_status")
                                for r in anchors.values()))
    composition = dict(Counter(anchors[s].get("confidence")
                                 for s in strict_stored))
    problems: list[str] = []
    if len(anchors) != EXPECTED_TOTAL:
        problems.append(f"anchor total {len(anchors)} != {EXPECTED_TOTAL}")
    if value_counts != EXPECTED_VALUE_COUNTS:
        problems.append(f"validation_status counts {value_counts} != "
                        f"{EXPECTED_VALUE_COUNTS}")
    if len(strict_stored) != EXPECTED_STRICT_COUNT:
        problems.append(f"strict_set count {len(strict_stored)} != "
                        f"{EXPECTED_STRICT_COUNT}")
    if composition != EXPECTED_STRICT_COMPOSITION:
        problems.append(f"strict composition {composition} != "
                        f"{EXPECTED_STRICT_COMPOSITION}")
    if strict_stored != strict_computed:
        diff = sorted(strict_stored ^ strict_computed)
        problems.append(f"stored strict_set != computed rule join for {diff}")
    return {"match": not problems, "problems": problems,
            "total": len(anchors), "value_counts": value_counts,
            "strict_count": len(strict_stored),
            "strict_composition": composition,
            "strict_computed_count": len(strict_computed)}


def plan(doc: dict[str, Any] | None = None,
         records: dict[str, dict] | None = None) -> dict[str, Any]:
    """Population state + the reconciliation the annotated document
    would carry. Writes nothing."""
    doc = load_anchors_doc() if doc is None else doc
    records = load_register() if records is None else records
    anchors = doc["anchors"]
    strict = compute_strict_set(anchors, records)
    states = Counter(record_state(r, records.get(s), s in strict)
                     for s, r in anchors.items())
    block_present = METADATA_KEY in doc.get("metadata", {})
    problems: list[str] = []
    if states.get("conflict"):
        problems.append(f"{states['conflict']} records in a conflicting "
                        "partial annotation state")
    if len(strict) != EXPECTED_STRICT_COUNT:
        problems.append(f"computed strict set is {len(strict)}, not "
                        f"{EXPECTED_STRICT_COUNT}: the rule does not "
                        "reproduce the audit's strict core — STOP")
    if states.get("annotated") and states.get("unannotated"):
        problems.append("population is partially annotated")
    if states.get("annotated") and not block_present:
        problems.append("records annotated but metadata block absent")
    if states.get("unannotated") and block_present:
        problems.append("metadata block present but records unannotated")
    annotated = copy.deepcopy(doc)
    if not states.get("annotated"):
        annotate_doc(annotated, records)
    recon = reconcile_counts(annotated, records)
    if not recon["match"]:
        problems.extend(recon["problems"])
    return {"state_counts": dict(states), "metadata_block_present": block_present,
            "would_be_reconciliation": recon, "problems": problems}


# ── The CI validator (H3/H4) ─────────────────────────────────────────────

def _type_ok(value: Any, declared: str) -> bool:
    if declared == "string":
        return isinstance(value, str)
    if declared == "boolean":
        return isinstance(value, bool)
    if declared == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if declared == "array":
        return isinstance(value, list)
    if declared == "object":
        return isinstance(value, dict)
    return False


def validate_anchors_doc(doc: dict[str, Any],
                         records: dict[str, dict],
                         schema: dict[str, Any]) -> list[str]:
    """Every way the document can fail the declared schema / the
    annotation rules, as a problems list (empty = valid). This is
    the H4 validator core: the backend suite runs it against the
    live file, and against mutated copies as must-fail controls."""
    problems: list[str] = []
    shape = schema["record_shape"]
    governed: dict[str, dict] = {}
    for section in ("required_core_fields", "phase_d_additive_fields",
                    "phase_h_additive_fields"):
        governed.update(shape[section])
    optional = shape["optional_fields"]
    declared = set(governed) | set(optional)
    vocab = set(schema["validation_status_vocabulary"])

    block = doc.get("metadata", {}).get(METADATA_KEY)
    if block is None:
        problems.append(f"metadata block {METADATA_KEY!r} absent")
    else:
        rule = block.get("strict_set_rule", {})
        declared_rule = schema["strict_set_rule"]
        for key in ("rule_id", "rule_source", "rule_version", "register"):
            if rule.get(key) != declared_rule.get(key):
                problems.append(f"metadata strict_set_rule {key} "
                                f"{rule.get(key)!r} != schema {declared_rule.get(key)!r}")
        if set(block.get("validation_status_vocabulary", [])) != vocab:
            problems.append("metadata vocabulary != declared vocabulary")

    anchors = doc.get("anchors", {})
    strict_computed = compute_strict_set(anchors, records)
    for sign, record in sorted(anchors.items()):
        reg = records.get(sign)
        if reg is None:
            problems.append(f"{sign}: no Phase-108 register record")
        for key in governed:
            if key not in record:
                problems.append(f"{sign}: required field {key!r} missing")
        for key in record:
            if key not in declared:
                problems.append(f"{sign}: field {key!r} is undeclared "
                                "under the schema")
        for key, decl in {**governed, **optional}.items():
            if key in record and not _type_ok(record[key], decl["type"]):
                problems.append(f"{sign}: field {key!r} is not of declared "
                                f"type {decl['type']}")
            if key in record and "enum" in decl \
                    and record[key] not in decl["enum"]:
                problems.append(f"{sign}: field {key!r} value "
                                f"{record[key]!r} outside its declared enum")
        value = record.get("validation_status")
        if value is not None and value not in vocab:
            problems.append(f"{sign}: validation_status {value!r} outside "
                            "the declared vocabulary")
        if value in NEW_VALUES:
            derived = derive_from_provenance(record, reg, sign in strict_computed)
            if value != derived:
                problems.append(f"{sign}: validation_status {value!r} != "
                                f"provenance derivation {derived!r}")
        elif value == "pending_non_sa_validation":
            if reg is None or reg.get("category") not in SA_LINEAGE_CATEGORIES:
                problems.append(f"{sign}: pending_non_sa_validation but "
                                "register category is not SA-lineage")
        elif value == "premise_superseded":
            if record.get("confidence") != "CANDIDATE" \
                    or record.get("reading") != "kur":
                problems.append(f"{sign}: premise_superseded but not the "
                                "CANDIDATE 'kur' cohort")
        flag = record.get("strict_set")
        if flag is not None:
            if flag is not (sign in strict_computed):
                problems.append(f"{sign}: strict_set {flag} != computed "
                                "rule join")
            if flag is not (value == "strict_sa_independent"):
                problems.append(f"{sign}: strict_set {flag} inconsistent "
                                f"with validation_status {value!r}")
    recon = reconcile_counts(doc, records)
    problems.extend(recon["problems"])
    return problems


# ── Modes ────────────────────────────────────────────────────────────────

def verify() -> dict[str, Any]:
    doc = load_anchors_doc()
    records = load_register()
    schema = load_schema()
    problems = validate_anchors_doc(doc, records, schema)
    return {"valid": not problems, "problems": problems,
            "reconciliation": reconcile_counts(doc, records)}


def snapshot(snapshot_dir: Path) -> Path:
    dest = snapshot_dir / "backend" / "reports" / ANCHORS_PATH.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ANCHORS_PATH, dest)
    return dest


def live_run(snapshot_dir: Path) -> dict[str, Any]:
    before_text = ANCHORS_PATH.read_text("utf-8")
    before_sha = sha256_bytes(before_text.encode("utf-8"))
    doc = json.loads(before_text)
    records = load_register()
    p = plan(doc, records)
    if p["problems"]:
        raise AnnotationError(f"plan problems: {p['problems']}")
    if p["state_counts"].get("annotated") == EXPECTED_TOTAL:
        return {"noop": True, "sha256": before_sha,
                "note": "every record already carries this annotation; "
                        "nothing written"}
    if before_sha != PHASE_D_ANCHORS_SHA256:
        raise AnnotationError(
            f"pre-run anchors SHA-256 {before_sha} != Phase-D-stamped "
            f"{PHASE_D_ANCHORS_SHA256}: unexpected starting state — STOP")
    snap = snapshot(snapshot_dir)
    changes = annotate_doc(doc, records)
    # Additive-only assertion, before writing: stripping exactly the
    # Phase H annotation must reproduce the pre-run bytes.
    if canonical_json(strip_phase_h(doc)) != before_text:
        raise AnnotationError("additive-only assertion failed: stripped "
                              "annotation does not reproduce pre-run bytes")
    problems = validate_anchors_doc(doc, records, load_schema())
    if problems:
        raise AnnotationError(f"annotated document fails validation: {problems}")
    ANCHORS_PATH.write_text(canonical_json(doc), encoding="utf-8")
    after_sha = sha256_bytes(ANCHORS_PATH.read_bytes())
    check = verify()
    if not check["valid"]:
        raise AnnotationError(f"post-write verification failed: "
                              f"{check['problems']}")
    return {"noop": False, "before_sha256": before_sha,
            "after_sha256": after_sha, "snapshot": str(snap),
            "changes": changes, "reconciliation": check["reconciliation"]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--verify", action="store_true")
    ap.add_argument("--snapshot-dir", type=Path, default=None,
                    help="required with --live")
    ap.add_argument("--report", type=Path, default=None,
                    help="also save the JSON report to this path")
    args = ap.parse_args()

    report: dict[str, Any]
    if args.dry_run:
        report = {"mode": "dry-run", **plan()}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        ok = not report["problems"]
    elif args.verify:
        report = {"mode": "verify", **verify()}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        ok = report["valid"]
    else:
        if args.snapshot_dir is None:
            ap.error("--live requires --snapshot-dir")
        try:
            report = {"mode": "live", **live_run(args.snapshot_dir)}
        except AnnotationError as exc:
            print(f"STOP: {exc}", file=sys.stderr)
            return 1
        summary = {k: v for k, v in report.items() if k != "changes"}
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        ok = True
    if args.report is not None:
        args.report.write_text(json.dumps(report, indent=2,
                                          ensure_ascii=False),
                               encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
