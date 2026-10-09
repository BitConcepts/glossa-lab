"""Phase-130 (spec 021) — independent-data intake pack.

Validates an incoming inscription dataset against the intake
schema v1 (`data/intake/intake_dataset_schema_v1.json`),
assigns its spec 018 (Phase-119) §4 evaluability class, runs
the shared §5 dedup (`glossa_lab.dedup`), and — as its final
stage — hands the dataset to the Phase-119 harness's DRY-RUN
path only.

STRUCTURAL RULE (spec 021 §5): this module imports
`dry_run` from `glossa_lab.pred_harness` and deliberately
does NOT import `evaluate` or any scoring function. Intake
output can only ever reach the harness's dry-run path;
evaluation of any prediction requires its own future spec
and separate owner authorization. Tests assert the
separation (no scoring names bound in this module, and a
dry-run report carrying the §8 label and no verdict keys).

Schema-implementation choice (spec 021 §2): the canonical
contract is the versioned JSON Schema document; the enforcing
validator here is stdlib-only Python (no new dependency —
core `glossa_lab` modules are stdlib-only and `jsonschema` is
not a project dependency; pydantic in this repo is confined
to the API layer). Tests assert the validator's required
fields, enums and version match the JSON Schema file.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path

from glossa_lab.dedup import dedup
from glossa_lab.pred_harness import (
    DRY_RUN_LABEL,
    EVALUABILITY,
    SOURCE_CLASSES,
    IngestedDataset,
    dry_run,
)

SCHEMA_VERSION = "1.0"
SCHEMA_PATH = (Path(__file__).resolve().parents[2]
               / "data" / "intake" / "intake_dataset_schema_v1.json")

SIGN_LISTS = ("parpola_1982", "mahadevan_1977", "wells",
              "marshall", "other")

# Consumed by spec 018 (§§4-7) -> REQUIRED (schema v1).
DATASET_REQUIRED = ("schema_version", "dataset_name", "source",
                    "source_class", "license_basis",
                    "upstream_lineage", "inscriptions")
INSCRIPTION_REQUIRED = ("inscription_id", "site", "tokens",
                        "sign_list", "provenance")
LINEAGE_REQUIRED = ("derived_from", "is_derivation_input")
PROVENANCE_REQUIRED = ("source_reference",)
# Optional-but-declared; absence warns.
DATASET_RECOMMENDED = ("compiler", "acquisition_date")
INSCRIPTION_RECOMMENDED = ("object_type",)

_TOKEN_PATTERNS = {
    "parpola_1982": re.compile(r"^P\d{3}$"),
    "mahadevan_1977": re.compile(r"^M\d{3,4}$"),
    "wells": re.compile(r"^\d{1,4}$"),
    "marshall": re.compile(r"^[A-Z]?\d{1,4}$"),
}


def _issue(code, path, message):
    return {"code": code, "path": path, "message": message}


def _is_nonempty_str(v):
    return isinstance(v, str) and bool(v.strip())


def _check_date(value, path, errors, warnings, required=False):
    if value is None:
        return
    try:
        date.fromisoformat(str(value))
    except ValueError:
        errors.append(_issue("INVALID_DATE", path,
                             f"{path} is not an ISO date: {value!r}"))


def validate_dataset(dataset) -> dict:
    """Validate a candidate dataset (parsed JSON dict) against
    intake schema v1. Returns a structured verdict:
    {"verdict": "pass"|"pass-with-warnings"|"reject",
     "errors": [{code, path, message}],   # rejects, named
     "warnings": [{code, path, message}],
     "summary": {...counts...}}.
    A missing/empty license basis is an error (reject), never
    a warning (spec 021 §3 license gate)."""
    errors: list[dict] = []
    warnings: list[dict] = []
    if not isinstance(dataset, dict):
        return {"verdict": "reject",
                "errors": [_issue("TYPE_ERROR", "$",
                                  "dataset must be a JSON object")],
                "warnings": [], "summary": {}}
    for f in DATASET_REQUIRED:
        if f not in dataset or dataset[f] is None:
            code = ("LICENSE_BASIS_MISSING" if f == "license_basis"
                    else "REQUIRED_FIELD_MISSING")
            errors.append(_issue(code, f, f"required field missing: {f}"))
    if ("schema_version" in dataset
            and dataset["schema_version"] != SCHEMA_VERSION):
        errors.append(_issue(
            "SCHEMA_VERSION_UNSUPPORTED", "schema_version",
            f"unsupported schema_version {dataset['schema_version']!r}; "
            f"this validator implements {SCHEMA_VERSION}"))
    for f in ("dataset_name", "source"):
        if f in dataset and not _is_nonempty_str(dataset[f]):
            errors.append(_issue("TYPE_ERROR", f,
                                 f"{f} must be a non-empty string"))
    # License gate: presence of a declared lawful basis.
    if "license_basis" in dataset and not _is_nonempty_str(dataset["license_basis"]):
        errors.append(_issue(
            "LICENSE_BASIS_MISSING", "license_basis",
            "license_basis is empty: a dataset with no declared "
            "lawful basis is rejected, not warned through"))
    if ("source_class" in dataset
            and dataset["source_class"] not in SOURCE_CLASSES):
        errors.append(_issue(
            "SOURCE_CLASS_INVALID", "source_class",
            f"source_class {dataset['source_class']!r} is not one of "
            f"spec 018 section 4's classes {list(SOURCE_CLASSES)}"))
    for f in DATASET_RECOMMENDED:
        if f not in dataset or dataset[f] is None:
            warnings.append(_issue(
                "RECOMMENDED_FIELD_MISSING", f,
                f"optional-but-declared field absent: {f}"))
    _check_date(dataset.get("acquisition_date"), "acquisition_date",
                errors, warnings)
    lineage = dataset.get("upstream_lineage")
    if lineage is not None:
        if not isinstance(lineage, dict):
            errors.append(_issue("TYPE_ERROR", "upstream_lineage",
                                 "upstream_lineage must be an object"))
        else:
            for f in LINEAGE_REQUIRED:
                if f not in lineage or lineage[f] is None:
                    errors.append(_issue(
                        "REQUIRED_FIELD_MISSING", f"upstream_lineage.{f}",
                        f"lineage declaration incomplete: {f} missing"))
            if ("is_derivation_input" in lineage
                    and not isinstance(lineage["is_derivation_input"], bool)):
                errors.append(_issue(
                    "TYPE_ERROR", "upstream_lineage.is_derivation_input",
                    "is_derivation_input must be a boolean"))
    inscriptions = dataset.get("inscriptions")
    n_tokens = 0
    sign_lists_seen: set[str] = set()
    if inscriptions is not None:
        if not isinstance(inscriptions, list) or not inscriptions:
            errors.append(_issue(
                "EMPTY_DATASET", "inscriptions",
                "inscriptions must be a non-empty list"))
            inscriptions = []
        seen_ids: dict[str, int] = {}
        for i, ins in enumerate(inscriptions):
            base = f"inscriptions[{i}]"
            if not isinstance(ins, dict):
                errors.append(_issue("TYPE_ERROR", base,
                                     "inscription must be an object"))
                continue
            for f in INSCRIPTION_REQUIRED:
                if f not in ins or ins[f] is None and f != "site":
                    code = ("SIGN_LIST_UNDECLARED" if f == "sign_list"
                            else "REQUIRED_FIELD_MISSING")
                    errors.append(_issue(code, f"{base}.{f}",
                                         f"required field missing: {f}"))
            iid = ins.get("inscription_id")
            if _is_nonempty_str(iid):
                if iid in seen_ids:
                    errors.append(_issue(
                        "DUPLICATE_INSCRIPTION_ID",
                        f"{base}.inscription_id",
                        f"inscription_id {iid!r} duplicates "
                        f"inscriptions[{seen_ids[iid]}]"))
                else:
                    seen_ids[iid] = i
            elif "inscription_id" in ins:
                errors.append(_issue(
                    "TYPE_ERROR", f"{base}.inscription_id",
                    "inscription_id must be a non-empty string"))
            if "site" in ins and ins["site"] is None:
                warnings.append(_issue(
                    "SITE_MISSING", f"{base}.site",
                    "site is null: PRED-2026-003 evaluability "
                    "(spec 018 section 6.1.5) needs site values"))
            sl = ins.get("sign_list")
            if sl is not None:
                if sl not in SIGN_LISTS:
                    errors.append(_issue(
                        "SIGN_LIST_UNDECLARED", f"{base}.sign_list",
                        f"sign_list {sl!r} is not a declared sign list "
                        f"{list(SIGN_LISTS)}"))
                else:
                    sign_lists_seen.add(sl)
                    if sl == "other" and not _is_nonempty_str(
                            ins.get("sign_list_detail")):
                        warnings.append(_issue(
                            "SIGN_LIST_DETAIL_MISSING",
                            f"{base}.sign_list_detail",
                            "sign_list 'other' without a detail "
                            "declaration"))
            toks = ins.get("tokens")
            if toks is not None:
                if (not isinstance(toks, list)
                        or any(not _is_nonempty_str(t) for t in toks)):
                    errors.append(_issue(
                        "TYPE_ERROR", f"{base}.tokens",
                        "tokens must be a list of non-empty strings"))
                else:
                    n_tokens += len(toks)
                    if not toks:
                        warnings.append(_issue(
                            "EMPTY_TOKEN_SEQUENCE", f"{base}.tokens",
                            "empty sign sequence"))
                    pat = _TOKEN_PATTERNS.get(sl or "")
                    if pat is not None:
                        bad = [t for t in toks
                               if t != "UNK" and not pat.match(t)]
                        if bad:
                            warnings.append(_issue(
                                "TOKEN_FORMAT_MISMATCH", f"{base}.tokens",
                                f"{len(bad)} token(s) do not match the "
                                f"declared {sl} format, e.g. {bad[0]!r}"))
            prov = ins.get("provenance")
            if prov is not None:
                if not isinstance(prov, dict):
                    errors.append(_issue("TYPE_ERROR", f"{base}.provenance",
                                         "provenance must be an object"))
                else:
                    for f in PROVENANCE_REQUIRED:
                        if not _is_nonempty_str(prov.get(f)):
                            errors.append(_issue(
                                "REQUIRED_FIELD_MISSING",
                                f"{base}.provenance.{f}",
                                f"per-inscription provenance incomplete: "
                                f"{f} missing/empty"))
                    if ("artifact_hash" in ins
                            and not re.fullmatch(
                                r"[0-9a-f]{64}", str(ins["artifact_hash"]))):
                        warnings.append(_issue(
                            "ARTIFACT_HASH_FORMAT", f"{base}.artifact_hash",
                            "artifact_hash is not a sha256 hex digest"))
                    _check_date(prov.get("transcription_date"),
                                f"{base}.provenance.transcription_date",
                                errors, warnings)
            for f in INSCRIPTION_RECOMMENDED:
                if f not in ins or ins[f] is None:
                    warnings.append(_issue(
                        "RECOMMENDED_FIELD_MISSING", f"{base}.{f}",
                        f"optional-but-declared field absent: {f}"))
    verdict = ("reject" if errors else
               "pass-with-warnings" if warnings else "pass")
    return {"verdict": verdict, "errors": errors, "warnings": warnings,
            "summary": {"inscriptions": len(inscriptions or []),
                        "tokens": n_tokens,
                        "sign_lists": sorted(sign_lists_seen),
                        "errors": len(errors), "warnings": len(warnings)}}


def assign_evaluability(dataset: dict) -> dict:
    """Spec 018 §4 evaluability-class assignment for a validated
    dataset: per-prediction QUALIFIES/NO from the frozen matrix
    (pred_harness.EVALUABILITY), the C1 caveat flag for
    icit_full, the multi-site input for PRED-2026-003, and a
    lineage consistency check (a dataset declaring
    is_derivation_input=True cannot be an independent class)."""
    source_class = dataset.get("source_class")
    per_prediction = {}
    for pid, qualifying in EVALUABILITY.items():
        per_prediction[pid] = ("QUALIFIES" if source_class in qualifying
                               else "NO")
    sites = {ins.get("site") for ins in dataset.get("inscriptions", [])
             if isinstance(ins, dict) and ins.get("site")}
    lineage = dataset.get("upstream_lineage") or {}
    independent = source_class in ("rmrl_concordance",
                                   "image_transcription",
                                   "future_concordance")
    consistency = []
    if independent and lineage.get("is_derivation_input") is True:
        consistency.append(
            "declared independent class but upstream_lineage."
            "is_derivation_input is true: class assignment must be "
            "re-adjudicated before any dry run is treated as "
            "independent-lineage")
    return {"source_class": source_class,
            "per_prediction": per_prediction,
            "qualifies_any": any(v == "QUALIFIES"
                                  for v in per_prediction.values()),
            "caveat_c1_required": source_class == "icit_full",
            "distinct_sites": len(sites),
            "multi_site": len(sites) >= 2,
            "pred2026_003_site_input": len(sites) >= 2,
            "lineage_consistency_notes": consistency}


def _content_hash(dataset: dict) -> str:
    canon = json.dumps(dataset, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def to_ingested_dataset(dataset: dict) -> IngestedDataset:
    """Convert a validated intake dataset to the harness record
    shape for the DRY-RUN path. Only parpola_1982-declared
    records pass through token-for-token (already P-space);
    any other declared sign list raises — mapping it to P-space
    is a spec 018 §7 adapter's job, not intake's."""
    records = []
    for ins in dataset["inscriptions"]:
        if ins["sign_list"] != "parpola_1982":
            raise ValueError(
                "intake dry-run pass-through requires every record "
                "declared parpola_1982; sign_list "
                f"{ins['sign_list']!r} needs a spec 018 section 7 "
                "adapter before the harness dry-run path")
        records.append({"inscription_id": ins["inscription_id"],
                        "site": ins.get("site"),
                        "tokens": list(ins["tokens"])})
    raw = json.dumps(dataset, sort_keys=True, ensure_ascii=False)
    provenance = {
        "date": dataset.get("acquisition_date"),
        "name": dataset["dataset_name"],
        "source": dataset["source"],
        "license": dataset["license_basis"],
        "status": "ingested",
        "input_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "text_rule": dataset.get(
            "text_rule",
            "intake schema v1: tokens taken verbatim, in source "
            "transcription order"),
        "unit_rule": dataset.get(
            "unit_rule", "one intake record = one inscription"),
        "source_class": dataset["source_class"],
        "compiler": dataset.get("compiler"),
        "upstream_lineage": dataset["upstream_lineage"],
    }
    tokens = sum(len(r["tokens"]) for r in records)
    ds = IngestedDataset(
        name=dataset["dataset_name"],
        source_class=dataset["source_class"],
        records=records, provenance=provenance,
        stats={"inscriptions": len(records), "tokens": tokens,
               "tokens_unmapped": 0, "tokens_ambiguous": 0,
               "distinct_signs": len({t for r in records
                                       for t in r["tokens"]
                                       if t != "UNK"})})
    return ds


def intake_dry_run(dataset: dict, classes: dict[str, str]) -> dict:
    """Final intake stage: the harness DRY-RUN path (§8) and
    nothing else. `classes` is the frozen §3 class map
    (pred_harness.load_sign_classes)."""
    return dry_run(to_ingested_dataset(dataset), classes)


def run_intake(dataset, classes: dict[str, str]) -> dict:
    """The runbook pipeline (docs/INTAKE_RUNBOOK.md), end to end:
    provenance/license gate -> schema validation -> dedup
    (shared module, raw declared-space token lists — a
    pre-adapter pre-check; the harness dry run re-applies the
    same module post-adapter) -> evaluability-class assignment
    -> harness dry-run. A rejected dataset stops at the gate:
    no dedup, no dry run. The report carries the §8 dry-run
    label whenever a dry run ran, and never a verdict, rate,
    or conformance statistic (spec 021 §5)."""
    report: dict = {"schema_version": SCHEMA_VERSION,
                    "dataset_content_hash": _content_hash(dataset)
                    if isinstance(dataset, dict) else None,
                    "stages": {}}
    verdict = validate_dataset(dataset)
    report["stages"]["validation"] = verdict
    # License gate is part of validation but reported separately
    # (runbook stage order: provenance -> license -> schema).
    report["stages"]["license_gate"] = (
        "pass" if not any(e["code"] == "LICENSE_BASIS_MISSING"
                          for e in verdict["errors"]) else "reject")
    if verdict["verdict"] == "reject":
        report["outcome"] = "rejected"
        return report
    records = [{"inscription_id": ins["inscription_id"],
                "site": ins.get("site"), "tokens": list(ins["tokens"])}
               for ins in dataset["inscriptions"]]
    _kept, dedup_counts = dedup(records)
    report["stages"]["dedup"] = dedup_counts
    report["stages"]["evaluability"] = assign_evaluability(dataset)
    try:
        dr = intake_dry_run(dataset, classes)
        report["stages"]["harness_dry_run"] = dr
        report["label"] = dr["label"]
        assert dr["label"] == DRY_RUN_LABEL
    except ValueError as exc:
        report["stages"]["harness_dry_run"] = {
            "status": "skipped", "reason": str(exc)}
    report["outcome"] = "intake-complete-dry-run-only"
    return report
