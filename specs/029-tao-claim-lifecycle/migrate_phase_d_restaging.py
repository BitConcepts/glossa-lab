"""Spec 029 Phase D — OD-1 re-staging migration (plan §2.2, tasks D2–D5).

Run from the repo root with the Glossa venv:

    # dry run (writes nothing; emits the reconciliation report)
    python specs/029-tao-claim-lifecycle/migrate_phase_d_restaging.py --dry-run

    # live run (snapshots every touched store first, then stamps)
    python specs/029-tao-claim-lifecycle/migrate_phase_d_restaging.py \
        --snapshot-dir /path/to/snapshots

    # post-run verification (read-only; reconciliation from live stores)
    python specs/029-tao-claim-lifecycle/migrate_phase_d_restaging.py --verify

The migration's ONLY input is the frozen
``specs/029-tao-claim-lifecycle/reclassification-ledger.json``
(345 entries; SHA-256 asserted against ``freeze.json``).
It is additive only: per record it adds ``stage``,
``stage_source``, ``stage_as_of``, ``stage_history`` and the
ledger-stamped ``verified_unexplained`` flag state, and it
asserts — canonically, before writing — that removing
exactly those keys reproduces the pre-run store bytes
(JSON stores) or that the pre-run bytes are a strict
prefix of the stamped bytes (hypothesis YAML stores,
which are appended to, never re-serialized). It is
idempotent: a second run over already-stamped records is
a no-op and says so. Any ledger/store mismatch, any
partial or conflicting stamp, and any reconciliation
that does not match the ledger's §3 table exactly stops
the run with a non-zero exit — nothing is smoothed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.claim_stage import validate_stage_value  # noqa: E402

SPEC_DIR = REPO / "specs" / "029-tao-claim-lifecycle"
LEDGER_PATH = SPEC_DIR / "reclassification-ledger.json"
FREEZE_PATH = SPEC_DIR / "freeze.json"
SIDECAR_PATH = SPEC_DIR / "phase-d-stamped-records.json"
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
CLAIMS_DIR = REPO / "glossa-indus" / "claims" / "extracted_claims"
HYPO_DIR = REPO / "glossa-indus" / "hypotheses" / "models"

MIGRATION_DATE = "2026-10-12"
ACTOR = "spec029-phase-d-restaging-migration"
LEDGER_REF = "specs/029-tao-claim-lifecycle/reclassification-ledger.json"
ADDITIVE_KEYS = ("stage", "stage_source", "stage_as_of", "stage_history",
                 "verified_unexplained")

#: Classes stamped in a file record store, and where.
FILE_STORE_CLASSES = ("anchor_reading", "extracted_claim", "hypothesis_model")
#: Classes with no live record store: stamped in the sidecar.
SIDECAR_CLASSES = ("registered_prediction", "study_headline_claim")
#: The live source each sidecar record names.
SIDECAR_LIVE_SOURCE = {
    "registered_prediction": "docs/PREDICTION_REGISTER.md",
    "study_headline_claim": "specs/ (per-spec outcome records; see live_source_detail)",
}
STUDY_LIVE_SOURCE_DETAIL = {
    "STUDY-SPEC-019/PHASE-125": "specs/019-phase125-cross-compilation-positional/",
    "STUDY-SPEC-023/PHASE-132+383": "specs/023-keyed-transcription-layer/",
    "STUDY-SPEC-024/F1": "specs/024-evidence-integration/",
    "STUDY-SPEC-024/F2-HOLDAT": "specs/024-evidence-integration/",
    "STUDY-SPEC-024/F3-ICIT": "specs/024-evidence-integration/",
    "STUDY-SPEC-025/G1": "specs/025-stage2-controlled-followup/",
    "STUDY-SPEC-027/STAGE1-PHASE-392": "specs/027-movement-culture-language/",
    "STUDY-SPEC-028/ARM-A": "specs/028-harappa-robustness/",
    "STUDY-SPEC-028/ARM-B": "specs/028-harappa-robustness/",
    "STUDY-SPECS-001-023+PHASES-TO-141": "specs/ (per-spec outcome records, Specs 001-023)",
}

#: The ledger §3 table (tasks D3) — the reconciliation must match exactly.
EXPECTED = {
    "anchor_reading": {"created": 193, "checked": 94},
    "extracted_claim": {"created": 21, "checked": 10},
    "registered_prediction": {"created": 3, "checked": 2},
    "hypothesis_model": {"created": 3},
    "study_headline_claim": {"checked": 10},
}
EXPECTED_TOTALS = {"created": 220, "checked": 116, "explained": 0,
                   "accepted": 0, "digested": 0}
EXPECTED_FLAGS = 105
EXPECTED_GROUPED = 9


class MigrationError(RuntimeError):
    """The migration stops; nothing is smoothed or partially written."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(data: Any) -> str:
    """The stores' canonical serialization (indent=2, no trailing newline)."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def stage_payload(entry: dict[str, Any]) -> dict[str, Any]:
    """The additive stamp for one ledger entry (Phase A record shape)."""
    item_id = entry["item_id"]
    stage = validate_stage_value(entry["honest_stage"])
    source = f"{LEDGER_REF}:{item_id}"
    history_entry = {
        "from_stage": None,
        "to_stage": stage,
        "actor": ACTOR,
        "timestamp": MIGRATION_DATE,
        "evidence_refs": [source],
        "reason": (
            f"OD-1 re-staging migration (Spec 029 Phase D, {MIGRATION_DATE}): "
            f"stage replayed from frozen reclassification ledger entry "
            f"{item_id}; no pre-existing field altered."
        ),
    }
    return {
        "stage": stage,
        "stage_source": source,
        "stage_as_of": MIGRATION_DATE,
        "stage_history": [history_entry],
        "verified_unexplained": "verified_unexplained" in (entry.get("flags") or []),
    }


def record_state(record: dict[str, Any], entry: dict[str, Any]) -> str:
    """'unstamped', 'stamped' (exactly the migration's stamp), or 'conflict'."""
    want = stage_payload(entry)
    present = [k for k in ADDITIVE_KEYS if k in record]
    if not present:
        return "unstamped"
    if all(record.get(k) == want[k] for k in ADDITIVE_KEYS) and len(present) == len(ADDITIVE_KEYS):
        return "stamped"
    return "conflict"


def stamp_record(record: dict[str, Any], entry: dict[str, Any]) -> None:
    want = stage_payload(entry)
    for key in ("stage", "stage_source", "stage_as_of", "stage_history",
                "verified_unexplained"):
        record[key] = want[key]


def strip_additive(record: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in record.items() if k not in ADDITIVE_KEYS}


# ── Store access ────────────────────────────────────────────────────────────

def load_ledger() -> dict[str, Any]:
    raw = LEDGER_PATH.read_bytes()
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    want = freeze["sources"][f"{LEDGER_REF}"]
    got = sha256_bytes(raw)
    if got != want:
        raise MigrationError(f"ledger hash mismatch: {got} != freeze-pinned {want}")
    ledger = json.loads(raw.decode("utf-8"))
    if len(ledger["entries"]) != 345:
        raise MigrationError(f"ledger has {len(ledger['entries'])} entries, expected 345")
    return ledger


def entries_by_class(ledger: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for e in ledger["entries"]:
        out.setdefault(e["class"], []).append(e)
    return out


def anchor_records(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return data["anchors"]


def claim_records() -> dict[Path, tuple[dict[str, Any], dict[str, dict[str, Any]]]]:
    """path -> (file data, {claim_id: claim record})."""
    out = {}
    for path in sorted(CLAIMS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out[path] = (data, {c["claim_id"]: c for c in data["claims"]})
    return out


def hypo_entry_for(entry: dict[str, Any]) -> tuple[Path, str]:
    model_id = entry["item_id"][len("HYP-"):]
    return HYPO_DIR / f"{model_id}.yaml", model_id


def yaml_stamp_block(entry: dict[str, Any]) -> str:
    """The appended top-level YAML block carrying one model's stamp."""
    want = stage_payload(entry)
    h = want["stage_history"][0]
    lines = [
        "",
        f"# Spec 029 Phase D (OD-1, {MIGRATION_DATE}): additive stage stamp —",
        "# appended by migrate_phase_d_restaging.py; no pre-existing line altered.",
        f"stage: {json.dumps(want['stage'])}",
        f"stage_source: {json.dumps(want['stage_source'])}",
        f"stage_as_of: {json.dumps(want['stage_as_of'])}",
        f"verified_unexplained: {json.dumps(want['verified_unexplained'])}",
        "stage_history:",
        f"  - from_stage: {json.dumps(h['from_stage'])}",
        f"    to_stage: {json.dumps(h['to_stage'])}",
        f"    actor: {json.dumps(h['actor'])}",
        f"    timestamp: {json.dumps(h['timestamp'])}",
        f"    evidence_refs: {json.dumps(h['evidence_refs'])}",
        f"    reason: {json.dumps(h['reason'])}",
        "",
    ]
    return "\n".join(lines)


def yaml_record_from_text(text: str) -> dict[str, Any]:
    """The stamped fields as read back from a YAML model file's text.

    The migration's block is the only top-level ``stage*`` content in
    these files, so top-level (column-0) scalar lines are the record.
    """
    rec: dict[str, Any] = {}
    for line in text.splitlines():
        if line.startswith(("stage: ", "stage_source: ", "stage_as_of: ",
                            "verified_unexplained: ")):
            key, _, scalar = line.partition(": ")
            try:
                rec[key] = json.loads(scalar)
            except json.JSONDecodeError:
                rec[key] = scalar
    return rec


def yaml_stamped_state(text: str, entry: dict[str, Any]) -> str:
    """State of a YAML model file: 'unstamped', 'stamped', or 'conflict'.

    Reads the appended top-level keys textually (one of the three
    files does not parse under PyYAML — a pre-existing defect —
    so parsing cannot be the state check for all three).
    """
    want = stage_payload(entry)
    if f'\nstage_source: {json.dumps(want["stage_source"])}' not in "\n" + text:
        if "\nstage:" in "\n" + text or "\nstage_source:" in "\n" + text:
            return "conflict"
        return "unstamped"
    block = yaml_stamp_block(entry)
    return "stamped" if text.endswith(block) else "conflict"


def sidecar_record(entry: dict[str, Any]) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "item_id": entry["item_id"],
        "class": entry["class"],
        "live_source": SIDECAR_LIVE_SOURCE[entry["class"]],
    }
    if entry["class"] == "study_headline_claim":
        rec["live_source_detail"] = STUDY_LIVE_SOURCE_DETAIL[entry["item_id"]]
    stamp_record(rec, entry)
    # Record-shape order: stage fields follow the identity fields.
    ordered = {k: rec[k] for k in
               ("item_id", "class", "live_source", *(
                   ("live_source_detail",) if "live_source_detail" in rec else ()),
                "stage", "stage_source", "stage_as_of", "stage_history",
                "verified_unexplained")}
    return ordered


def build_sidecar(ledger: dict[str, Any], by_class: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    records = []
    for cls in SIDECAR_CLASSES:
        for entry in by_class.get(cls, []):
            records.append(sidecar_record(entry))
    return {
        "record": ("Spec 029 Phase D — dated machine-readable stage stamps for the "
                   "reclassification-ledger classes with no live record store "
                   "(registered_prediction, study_headline_claim)"),
        "date": MIGRATION_DATE,
        "source_ledger": LEDGER_REF,
        "source_ledger_sha256": sha256_bytes(LEDGER_PATH.read_bytes()),
        "records": records,
    }


# ── Reconciliation ────────────────────────────────────────────────────────

def reconcile(counts: dict[str, dict[str, int]], flags: int, grouped: int) -> dict[str, Any]:
    totals: dict[str, int] = {s: 0 for s in EXPECTED_TOTALS}
    for cls_counts in counts.values():
        for stage, n in cls_counts.items():
            totals[stage] = totals.get(stage, 0) + n
    problems = []
    for cls, want in EXPECTED.items():
        got = counts.get(cls, {})
        if got != want:
            problems.append(f"class {cls}: got {got}, expected {want}")
    for cls in counts:
        if cls not in EXPECTED:
            problems.append(f"unexpected staged class {cls}: {counts[cls]}")
    if totals != EXPECTED_TOTALS:
        problems.append(f"totals: got {totals}, expected {EXPECTED_TOTALS}")
    if flags != EXPECTED_FLAGS:
        problems.append(f"verified_unexplained flags: got {flags}, expected {EXPECTED_FLAGS}")
    if grouped != EXPECTED_GROUPED:
        problems.append(f"grouped/non-record entries: got {grouped}, expected {EXPECTED_GROUPED}")
    return {"per_class": counts, "totals": totals,
            "verified_unexplained_flags": flags, "grouped_non_record_entries": grouped,
            "match": not problems, "problems": problems}


def count_stamped_records(stamped: list[tuple[str, dict[str, Any], dict[str, Any]]],
                          grouped: int) -> dict[str, Any]:
    """Count (class, ledger entry, stamped record) triples by stored stage."""
    counts: dict[str, dict[str, int]] = {}
    flags = 0
    for cls, entry, record in stamped:
        stage = record.get("stage")
        if record.get("stage_source") != stage_payload(entry)["stage_source"]:
            raise MigrationError(f"{entry['item_id']}: stage_source mismatch in live store")
        if record.get("stage_as_of") != MIGRATION_DATE:
            raise MigrationError(f"{entry['item_id']}: stage_as_of mismatch in live store")
        counts.setdefault(cls, {})
        counts[cls][stage] = counts[cls].get(stage, 0) + 1
        if record.get("verified_unexplained") is True:
            flags += 1
    return reconcile(counts, flags, grouped)


def collect_live_state(by_class: dict[str, list[dict[str, Any]]]) -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    """All stamped records as read back from the live stores."""
    out: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    anchors = anchor_records(json.loads(ANCHORS_PATH.read_text(encoding="utf-8")))
    for entry in by_class.get("anchor_reading", []):
        sign = entry["item_id"][len("ANCHOR-"):]
        if sign not in anchors:
            raise MigrationError(f"anchor {entry['item_id']} not in anchors file")
        out.append(("anchor_reading", entry, anchors[sign]))
    all_claims: dict[str, dict[str, Any]] = {}
    for _path, (_data, recs) in claim_records().items():
        all_claims.update(recs)
    for entry in by_class.get("extracted_claim", []):
        if entry["item_id"] not in all_claims:
            raise MigrationError(f"extracted claim {entry['item_id']} not in claims store")
        out.append(("extracted_claim", entry, all_claims[entry["item_id"]]))
    for entry in by_class.get("hypothesis_model", []):
        path, _mid = hypo_entry_for(entry)
        text = path.read_text(encoding="utf-8")
        if yaml_stamped_state(text, entry) != "stamped":
            raise MigrationError(f"hypothesis {entry['item_id']} not stamped in {path.name}")
        out.append(("hypothesis_model", entry, yaml_record_from_text(text)))
    if not SIDECAR_PATH.exists():
        raise MigrationError("sidecar phase-d-stamped-records.json missing")
    sidecar = json.loads(SIDECAR_PATH.read_text(encoding="utf-8"))
    by_id = {r["item_id"]: r for r in sidecar["records"]}
    for cls in SIDECAR_CLASSES:
        for entry in by_class.get(cls, []):
            if entry["item_id"] not in by_id:
                raise MigrationError(f"sidecar missing {entry['item_id']}")
            out.append((cls, entry, by_id[entry["item_id"]]))
    return out


def grouped_count(by_class: dict[str, list[dict[str, Any]]]) -> int:
    staged = set(FILE_STORE_CLASSES) | set(SIDECAR_CLASSES)
    return sum(len(v) for cls, v in by_class.items() if cls not in staged)


# ── Planning (shared by dry-run and live run) ──────────────────────────────

def plan() -> dict[str, Any]:
    ledger = load_ledger()
    by_class = entries_by_class(ledger)
    grouped = grouped_count(by_class)
    problems: list[str] = []
    actions: list[str] = []

    # Anchors
    anchors_data = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
    anchors = anchor_records(anchors_data)
    ledger_anchor_ids = {e["item_id"][len("ANCHOR-"):] for e in by_class.get("anchor_reading", [])}
    if set(anchors) != ledger_anchor_ids:
        problems.append(
            f"anchors store/ledger set mismatch: store-only {sorted(set(anchors) - ledger_anchor_ids)}, "
            f"ledger-only {sorted(ledger_anchor_ids - set(anchors))}")
    # Extracted claims
    claims_files = claim_records()
    all_claims: dict[str, dict[str, Any]] = {}
    for _p, (_d, recs) in claims_files.items():
        for cid, rec in recs.items():
            if cid in all_claims:
                problems.append(f"duplicate claim_id across files: {cid}")
            all_claims[cid] = rec
    ledger_claim_ids = {e["item_id"] for e in by_class.get("extracted_claim", [])}
    if set(all_claims) != ledger_claim_ids:
        problems.append(
            f"claims store/ledger set mismatch: store-only {sorted(set(all_claims) - ledger_claim_ids)}, "
            f"ledger-only {sorted(ledger_claim_ids - set(all_claims))}")
    # Hypotheses
    for entry in by_class.get("hypothesis_model", []):
        path, _mid = hypo_entry_for(entry)
        if not path.exists():
            problems.append(f"hypothesis file missing: {path}")
    hypo_files = {p.stem for p in HYPO_DIR.glob("*.yaml")}
    ledger_hypo = {e["item_id"][len("HYP-"):] for e in by_class.get("hypothesis_model", [])}
    if hypo_files != ledger_hypo:
        problems.append(f"hypothesis store/ledger set mismatch: {hypo_files} vs {ledger_hypo}")
    # Sidecar classes exist only in the ledger + their documents.
    for cls in SIDECAR_CLASSES:
        for entry in by_class.get(cls, []):
            if entry.get("honest_stage") is None:
                problems.append(f"{entry['item_id']}: sidecar class entry without a stage")

    # States
    states: dict[str, str] = {}
    def note(item_id: str, state: str) -> None:
        states[item_id] = state
        if state == "conflict":
            problems.append(f"{item_id}: existing stage fields conflict with the ledger stamp")
    for entry in by_class.get("anchor_reading", []):
        sign = entry["item_id"][len("ANCHOR-"):]
        if sign in anchors:
            note(entry["item_id"], record_state(anchors[sign], entry))
    for entry in by_class.get("extracted_claim", []):
        if entry["item_id"] in all_claims:
            note(entry["item_id"], record_state(all_claims[entry["item_id"]], entry))
    for entry in by_class.get("hypothesis_model", []):
        path, _mid = hypo_entry_for(entry)
        if path.exists():
            note(entry["item_id"], yaml_stamped_state(path.read_text(encoding="utf-8"), entry))
    if SIDECAR_PATH.exists():
        existing = json.loads(SIDECAR_PATH.read_text(encoding="utf-8"))
        want_sidecar = build_sidecar(ledger, by_class)
        if existing == want_sidecar:
            for entry in sum((by_class.get(c, []) for c in SIDECAR_CLASSES), []):
                note(entry["item_id"], "stamped")
        else:
            problems.append("sidecar exists but differs from the ledger-derived sidecar")
    else:
        for entry in sum((by_class.get(c, []) for c in SIDECAR_CLASSES), []):
            note(entry["item_id"], "unstamped")

    state_counts: dict[str, int] = {}
    for s in states.values():
        state_counts[s] = state_counts.get(s, 0) + 1
    if state_counts.get("stamped", 0) and state_counts.get("unstamped", 0):
        problems.append(f"partially stamped population: {state_counts} — refusing to smooth")

    # Would-be reconciliation: counts from the ledger entries that matched a store.
    would: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for cls in FILE_STORE_CLASSES + SIDECAR_CLASSES:
        for entry in by_class.get(cls, []):
            if states.get(entry["item_id"]) in ("unstamped", "stamped"):
                would.append((cls, entry, stage_payload(entry)))
    try:
        would_recon = count_stamped_records(would, grouped) if not problems else None
    except MigrationError as exc:
        problems.append(str(exc))
        would_recon = None
    return {"ledger": ledger, "by_class": by_class, "grouped": grouped,
            "states": states, "state_counts": state_counts, "problems": problems,
            "would_be_reconciliation": would_recon, "actions": actions}


# ── Live run ────────────────────────────────────────────────────────────────

def touched_paths() -> list[Path]:
    paths = [ANCHORS_PATH, *sorted(CLAIMS_DIR.glob("*.json")),
             *sorted(HYPO_DIR.glob("*.yaml"))]
    return paths


def snapshot(snapshot_dir: Path) -> list[dict[str, Any]]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snaps = []
    for path in touched_paths():
        dest = snapshot_dir / path.relative_to(REPO)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        snaps.append({"path": str(path.relative_to(REPO)),
                      "snapshot": str(dest),
                      "sha256_before": sha256_bytes(path.read_bytes())})
    snaps.append({"path": str(SIDECAR_PATH.relative_to(REPO)),
                  "snapshot": None,
                  "sha256_before": sha256_bytes(SIDECAR_PATH.read_bytes())
                  if SIDECAR_PATH.exists() else None,
                  "note": "did not exist before the run" if not SIDECAR_PATH.exists() else "existed"})
    return snaps


def additive_assert_json(before_text: str, after_data: dict[str, Any],
                         records_of: str) -> None:
    """Removing the additive keys from every target record in the
    post-run data must reproduce the pre-run canonical bytes exactly."""
    after = copy.deepcopy(after_data)
    if records_of == "anchors":
        for rec in after["anchors"].values():
            for k in ADDITIVE_KEYS:
                rec.pop(k, None)
    else:  # extracted-claims file
        for rec in after["claims"]:
            for k in ADDITIVE_KEYS:
                rec.pop(k, None)
    if canonical_json(after) != before_text.rstrip("\n") and canonical_json(after) != before_text:
        raise MigrationError(f"additive-only assertion FAILED for {records_of}")


def live_run(snapshot_dir: Path) -> dict[str, Any]:
    p = plan()
    if p["problems"]:
        raise MigrationError("plan problems: " + "; ".join(p["problems"]))
    if p["state_counts"].get("stamped", 0) and not p["state_counts"].get("unstamped", 0):
        return {"mode": "live", "noop": True,
                "message": "no-op: every record already carries this migration's stamp; nothing written",
                "state_counts": p["state_counts"],
                "reconciliation": p["would_be_reconciliation"]}
    by_class = p["by_class"]
    snaps = snapshot(snapshot_dir)
    hashes_before = {s["path"]: s["sha256_before"] for s in snaps}
    hashes_after: dict[str, str] = {}

    # Anchors (in place, canonical serialization preserved)
    before_text = ANCHORS_PATH.read_text(encoding="utf-8")
    data = json.loads(before_text)
    for entry in by_class["anchor_reading"]:
        stamp_record(data["anchors"][entry["item_id"][len("ANCHOR-"):]], entry)
    additive_assert_json(before_text, data, "anchors")
    ANCHORS_PATH.write_text(canonical_json(data), encoding="utf-8")
    hashes_after[str(ANCHORS_PATH.relative_to(REPO))] = sha256_bytes(ANCHORS_PATH.read_bytes())

    # Extracted claims (in place, per file)
    entries_by_id = {e["item_id"]: e for e in by_class["extracted_claim"]}
    for path in sorted(CLAIMS_DIR.glob("*.json")):
        before_text = path.read_text(encoding="utf-8")
        fdata = json.loads(before_text)
        changed = False
        for rec in fdata["claims"]:
            entry = entries_by_id.get(rec["claim_id"])
            if entry is not None:
                stamp_record(rec, entry)
                changed = True
        if changed:
            additive_assert_json(before_text, fdata, "claims")
            path.write_text(canonical_json(fdata), encoding="utf-8")
        hashes_after[str(path.relative_to(REPO))] = sha256_bytes(path.read_bytes())

    # Hypothesis models (append-only YAML block; prefix assertion)
    for entry in by_class["hypothesis_model"]:
        path, _mid = hypo_entry_for(entry)
        before = path.read_bytes()
        after = before + yaml_stamp_block(entry).encode("utf-8")
        if not after.startswith(before):
            raise MigrationError(f"additive-only (prefix) assertion FAILED for {path.name}")
        path.write_bytes(after)
        hashes_after[str(path.relative_to(REPO))] = sha256_bytes(path.read_bytes())

    # Sidecar (new file)
    sidecar = build_sidecar(p["ledger"], by_class)
    SIDECAR_PATH.write_text(canonical_json(sidecar) + "\n", encoding="utf-8")
    hashes_after[str(SIDECAR_PATH.relative_to(REPO))] = sha256_bytes(SIDECAR_PATH.read_bytes())

    # Re-read from the live stores and reconcile.
    live = collect_live_state(by_class)
    recon = count_stamped_records(live, p["grouped"])
    if not recon["match"]:
        raise MigrationError("post-run reconciliation mismatch: " + "; ".join(recon["problems"]))
    return {"mode": "live", "noop": False,
            "snapshots": snaps,
            "sha256_before": hashes_before, "sha256_after": hashes_after,
            "additive_only": "asserted per store (canonical comparison / byte prefix) before writing",
            "state_counts": p["state_counts"],
            "reconciliation": recon}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--verify", action="store_true")
    ap.add_argument("--snapshot-dir", type=Path, default=None,
                    help="required for --live: where pre-run snapshots are written")
    ap.add_argument("--report", type=Path, default=None,
                    help="also write the JSON report to this path")
    args = ap.parse_args()

    try:
        if args.verify:
            ledger = load_ledger()
            by_class = entries_by_class(ledger)
            live = collect_live_state(by_class)
            recon = count_stamped_records(live, grouped_count(by_class))
            report = {"mode": "verify", "reconciliation": recon}
            ok = recon["match"]
        elif args.dry_run:
            p = plan()
            report = {"mode": "dry-run", "state_counts": p["state_counts"],
                      "problems": p["problems"],
                      "reconciliation": p["would_be_reconciliation"],
                      "message": ("no-op: population already stamped"
                                  if p["state_counts"].get("stamped") and not p["state_counts"].get("unstamped")
                                  else "dry run: nothing written")}
            ok = not p["problems"] and bool(p["would_be_reconciliation"]) and p["would_be_reconciliation"]["match"]
        else:
            if args.snapshot_dir is None:
                ap.error("--live requires --snapshot-dir")
            report = live_run(args.snapshot_dir)
            ok = True
    except MigrationError as exc:
        report = {"mode": "error", "error": str(exc)}
        ok = False

    text = json.dumps(report, indent=2, ensure_ascii=False)
    print(text)
    if args.report:
        args.report.write_text(text + "\n", encoding="utf-8")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
