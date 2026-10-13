"""Spec 029 Phase G — the CI gate layer (FR-029-12; claim F029-C09;
plan §0, §2.4; tasks G1–G2).

Phases A–J and E each shipped their own tests. This module is the
*gate layer* over the whole live data and the whole record
population: the machinery the Phase G tests
(``backend/tests/test_spec029_phase_g.py``) run in CI so the
discipline cannot silently regress. It invents no stage, no
falsifier, no actor, and no evidence: where a live record lacks a
field, the gate reports the gap (the Phase G test file carries the
explicit, recorded baseline of the gaps that legitimately exist
at this head, and the phase record names them — a gap not in that
baseline fails CI, and a *new* record carrying any gap fails CI).

Two gates live here:

* **G1 — trail completeness.** For every live record, the
  Phase C trail (:func:`glossa_lab.claim_trail.build_claim_trail`)
  must assemble, and every verdict event and stage-transition
  event it serializes must carry the FR-029-12 fields: evidence
  references (each resolvable — see :func:`evidence_ref_resolves`),
  the origin group of each reference, the falsifier state at
  decision time (serialized as ``stated`` or ``absent`` — the
  state is always present; its *content* gaps are the baseline's
  business, below), the actor, and the timestamp. A stamped stage
  event must carry its source pointer (plan §0). Where a record's
  stage is above ``checked``, the Phase B gate records that stage
  requires must be present and valid.

* **G2 — stage-cache recompute integrity (the plan §0 / D-E
  invariant).** A stored stage is a cache with provenance, never
  an assertion. :func:`recompute_stage` recomputes a record's
  stage from its own evidence, by the rule its ``stage_source``
  names:

  - a **ledger source** (``…/reclassification-ledger.json:<id>``)
    replays the frozen reclassification ledger — the audit's
    rule application, and Phase D's single source of truth: the
    recomputed stage is the ledger entry's ``honest_stage`` for
    that item, and the record's history tail must agree;
  - a **bundle source** recomputes the Phase B parent-stage
    computation (minimum of sub-claim stages, then the OD-3
    contested-attribution cap and the OD-5 adverse-digestion
    cap);
  - a **transition-service source** recomputes from the
    append-only history the source indexes: the indexed entry's
    ``to_stage``, with ``stage_as_of`` equal to its timestamp;
  - an **unstamped** record (``stage is None``) recomputes to
    ``None`` and must be honestly unstamped (no half-stamp:
    no ``stage_source`` / ``stage_as_of`` without a stage).

  Any other source is unrecomputable, and an unrecomputable
  stored stage is a defect. The full migrated population is
  recomputed on every CI run (336 ledger-stamped records plus
  their preserved evidence instances — cheap and deterministic),
  which exceeds the frozen text's sampled minimum; the sampled
  form remains available via :func:`audit_stage_cache` on any
  subset a caller chooses.

Resolvability of an evidence reference, mechanically: a ledger /
file pointer (``<path>:<fragment>`` or a bare repo-relative path)
resolves when the file exists and the fragment is found in it;
a URI or DOI resolves when it has resolvable form
(:func:`glossa_lab.claim_bundle.is_resolvable_ref`); a source
document reference resolves when the document is one of the live
extracted-claims documents; any other non-empty reference is
evidence carried on the record itself (a basis line, a quote
fragment) and resolves to its record of origin — the origin group
the trail attributes to it. An empty reference never resolves.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from glossa_lab.claim_bundle import (
    PARENT_STAGE_SOURCE,
    is_bundle,
    is_resolvable_ref,
    validate_attribution_subclaim,
    validate_digestion_record,
    validate_explanation_record,
    validate_subclaim,
    BundleValidationError,
    get_subclaim,
    ATTRIBUTION_KIND,
)
from glossa_lab.claim_stage import STAGE_ORDER, is_named_human, validate_stage_value
from glossa_lab.claim_trail import build_claim_trail

REPO_ROOT = Path(__file__).resolve().parents[2]

LEDGER_REL = "specs/029-tao-claim-lifecycle/reclassification-ledger.json"
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
CLAIMS_DIR_REL = "glossa-indus/claims/extracted_claims"
SIDECAR_REL = "specs/029-tao-claim-lifecycle/phase-d-stamped-records.json"
HYPOTHESES_DIR_REL = "glossa-indus/hypotheses/models"

_CHECKED = STAGE_ORDER["checked"]
_ACCEPTED = STAGE_ORDER["accepted"]
_DIGESTED = STAGE_ORDER["digested"]

#: Actors a stage-history entry may carry when its target stage is
#: above ``checked`` without being a named human: the Phase B
#: bundle-minimum computation (its entries record a computation,
#: not a human act — the sub-claim transitions beneath it are the
#: human-gated ones, and they are checked on their own records).
_COMPUTATION_ACTORS = frozenset({"bundle-minimum-computation"})


@dataclass
class GateContext:
    """Everything a gate needs to resolve references against the
    live stores, loaded once from the repository tree."""

    root: Path
    ledger_entries: dict[str, dict[str, Any]] = field(default_factory=dict)
    document_ids: set[str] = field(default_factory=set)
    anchor_signs: set[str] = field(default_factory=set)


@dataclass
class LiveRecord:
    record_id: str
    kind: str  # anchor | extracted_claim | document_record | hypothesis_model | evidence_instance
    record: dict[str, Any]


def load_context(root: Path = REPO_ROOT) -> GateContext:
    ctx = GateContext(root=root)
    ledger_path = root / LEDGER_REL
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text("utf-8"))
        ctx.ledger_entries = {e["item_id"]: e for e in ledger.get("entries", [])}
    claims_dir = root / CLAIMS_DIR_REL
    if claims_dir.exists():
        for path in sorted(claims_dir.glob("*.json")):
            data = json.loads(path.read_text("utf-8"))
            if data.get("document_id"):
                ctx.document_ids.add(str(data["document_id"]))
            for claim in data.get("claims", []):
                if claim.get("source_document_id"):
                    ctx.document_ids.add(str(claim["source_document_id"]))
    anchors_path = root / ANCHORS_REL
    if anchors_path.exists():
        doc = json.loads(anchors_path.read_text("utf-8"))
        ctx.anchor_signs = set((doc.get("anchors") or {}).keys())
    return ctx


# ── Live population ───────────────────────────────────────────────────────

_YAML_SCALAR = re.compile(r'^(stage|stage_source|stage_as_of|verified_unexplained):\s*(.+)$')
_YAML_HIST_KEY = re.compile(r"^\s+(?:-\s+)?(from_stage|to_stage|actor|timestamp|evidence_refs|reason):\s*(.*)$")


def _yaml_scalar(text: str) -> Any:
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return text.strip().strip('"').strip("'") or None


def hypothesis_record_from_text(text: str) -> dict[str, Any]:
    """The Phase D stage stamp of one hypothesis-model YAML file.

    The stamp is the migration's appended top-level block (the
    Phase D migration's own read-back rule); one of the three
    files does not parse under PyYAML (a pre-existing defect
    recorded by Phase D), so the stamp is read textually for all
    three, uniformly: the top-level stage scalars plus the
    appended ``stage_history`` entries.
    """
    record: dict[str, Any] = {"stage_history": []}
    in_history = False
    current: dict[str, Any] | None = None
    for line in text.splitlines():
        if line.startswith("stage_history:"):
            in_history = True
            continue
        if in_history:
            if line and not line.startswith((" ", "\t")):
                in_history = False
                current = None
                continue
            stripped = line.strip()
            if stripped.startswith("- "):
                current = {}
                record["stage_history"].append(current)
                stripped = stripped[2:]
            m = _YAML_HIST_KEY.match("  " + stripped) if stripped else None
            if m and current is not None:
                key, raw = m.group(1), m.group(2).strip()
                if key == "evidence_refs":
                    current[key] = [r.strip().strip('"') for r in raw.strip("[]").split(",") if r.strip()]
                elif key in ("from_stage", "to_stage"):
                    current[key] = None if raw in ("null", "~", "") else _yaml_scalar(raw)
                else:
                    current[key] = _yaml_scalar(raw) if key in ("actor", "timestamp") else raw
            continue
        m = _YAML_SCALAR.match(line)
        if m:
            value = _yaml_scalar(m.group(2).strip())
            record[m.group(1)] = value if m.group(1) != "verified_unexplained" else (m.group(2).strip() == "true")
    return record


def iter_live_records(root: Path = REPO_ROOT, ctx: GateContext | None = None) -> list[LiveRecord]:
    """Every live record the gates run over, from the real stores.

    The population is the Phase D migrated population — 287
    anchors, the extracted claims, the 15 document-class records
    of the Phase D stamped-records sidecar (5 registered
    predictions + 10 study headlines), and the 3 hypothesis
    models — plus every preserved evidence instance a merged
    claim carries (Phase I: each instance retains its own
    stamped stage and history, so each is gated too).
    """
    ctx = ctx or load_context(root)
    records: list[LiveRecord] = []

    anchors_path = root / ANCHORS_REL
    if anchors_path.exists():
        doc = json.loads(anchors_path.read_text("utf-8"))
        for sign, rec in sorted((doc.get("anchors") or {}).items()):
            records.append(LiveRecord(f"ANCHOR-{sign}", "anchor", rec))

    claims_dir = root / CLAIMS_DIR_REL
    if claims_dir.exists():
        for path in sorted(claims_dir.glob("*.json")):
            data = json.loads(path.read_text("utf-8"))
            for claim in data.get("claims", []):
                records.append(LiveRecord(str(claim.get("claim_id")), "extracted_claim", claim))
                for inst in claim.get("evidence_instances") or []:
                    inner = inst.get("record") if isinstance(inst, dict) else None
                    if isinstance(inner, dict):
                        records.append(LiveRecord(
                            str(inst.get("claim_id") or inner.get("claim_id")),
                            "evidence_instance", inner))

    sidecar_path = root / SIDECAR_REL
    if sidecar_path.exists():
        sidecar = json.loads(sidecar_path.read_text("utf-8"))
        for rec in sidecar.get("records", []):
            records.append(LiveRecord(str(rec.get("item_id")), "document_record", rec))

    hypo_dir = root / HYPOTHESES_DIR_REL
    if hypo_dir.exists():
        for entry_id, entry in sorted(ctx.ledger_entries.items()):
            if entry.get("class") != "hypothesis_model":
                continue
            name = entry_id[len("HYP-"):] if entry_id.startswith("HYP-") else entry_id
            path = hypo_dir / f"{name}.yaml"
            if path.exists():
                records.append(LiveRecord(
                    entry_id, "hypothesis_model",
                    hypothesis_record_from_text(path.read_text("utf-8"))))
    return records


# ── Reference resolution ──────────────────────────────────────────────────

def evidence_ref_resolves(ref: Any, record: dict[str, Any], ctx: GateContext) -> bool:
    """True when one evidence reference resolves (module docstring)."""
    text = str(ref or "").strip()
    if not text:
        return False
    if "://" in text or text.lower().startswith("doi:") or is_resolvable_ref(text):
        return True
    # A repo-file pointer: "<path>:<fragment>" or a bare repo path.
    path_part, _, fragment = text.partition(":")
    candidate = path_part.strip()
    if "/" in candidate and (candidate.endswith((".json", ".md", ".yaml", ".yml", ".py", ".txt"))):
        target = ctx.root / candidate
        if not target.exists():
            return False
        if fragment:
            frag = fragment.strip()
            if candidate == LEDGER_REL:
                return frag in ctx.ledger_entries
            return frag in target.read_text("utf-8", errors="ignore")
        return True
    if text in ctx.document_ids or text in ctx.anchor_signs:
        return True
    # Evidence carried on the record itself (basis line, quote
    # fragment, a named corpus): resolves to its record of origin.
    return True


# ── G1: trail completeness ────────────────────────────────────────────────

def trail_gap_profile(record: dict[str, Any], *, record_kind: str = "claim") -> frozenset[str]:
    """The record trail's own gap profile: the Phase C trail's
    ``completeness.missing`` list, as a set. An incomplete trail is
    visibly incomplete there; the gate compares this profile
    against the recorded baseline (tests) so no gap can grow
    silently and no new record can carry one."""
    trail = build_claim_trail(record, record_kind=record_kind)
    return frozenset(trail["completeness"]["missing"])


def _gate_record_violations(record: dict[str, Any]) -> list[str]:
    """Phase B gate records required by the record's own stage."""
    violations: list[str] = []
    stage = record.get("stage")
    if stage is None or stage not in STAGE_ORDER:
        return violations
    rank = STAGE_ORDER[stage]
    if rank <= _CHECKED:
        return violations
    if is_bundle(record):
        attribution = get_subclaim(record, ATTRIBUTION_KIND)
        if attribution is not None and attribution.get("contest_state", "unexamined") != "unexamined":
            try:
                validate_attribution_subclaim(attribution)
            except BundleValidationError as exc:
                violations.append(f"attribution template invalid for a stage above 'checked': {exc}")
        return violations
    if rank >= _ACCEPTED:
        try:
            validate_explanation_record(record.get("explanation_record"))
        except BundleValidationError as exc:
            violations.append(f"stage {stage!r} requires a valid explanation record (FR-029-06): {exc}")
    if rank >= _DIGESTED:
        try:
            validate_digestion_record(
                record.get("digestion_record"),
                claim_authors=record.get("claim_authors") or (),
                program_staff=record.get("program_staff") or ())
        except BundleValidationError as exc:
            violations.append(f"stage 'digested' requires a valid digestion record (FR-029-07): {exc}")
    return violations


def audit_trail_record(record: dict[str, Any], ctx: GateContext, *, record_kind: str = "claim") -> list[str]:
    """G1 hard checks for one record. Returns violation strings
    (empty = the record's trail events are complete). The trail's
    softer gap profile (a missing falsifier text, an extraction-era
    verdict actor) is *not* judged here — it is compared against
    the recorded baseline by :func:`trail_gap_profile`'s caller,
    so legacy gaps stay visible without making the gate red on
    day one, and any growth still fails."""
    violations: list[str] = []
    trail = build_claim_trail(record, record_kind=record_kind)

    stage = record.get("stage")
    if stage is not None:
        try:
            validate_stage_value(stage)
        except ValueError as exc:
            violations.append(str(exc))
        if not str(record.get("stage_source") or "").strip():
            violations.append("stamped stage lacks stage_source (plan §0)")
        if not str(record.get("stage_as_of") or "").strip():
            violations.append("stamped stage lacks stage_as_of (plan §0)")
    else:
        # Honestly unstamped: a half-stamp is a defect.
        if record.get("stage_source") or record.get("stage_as_of"):
            violations.append("unstamped stage carries stage_source/stage_as_of (a half-stamp)")

    for event in trail["stage_transitions"]:
        label = f"stage transition -> {event.get('to_stage')!r}"
        if not event.get("actor"):
            violations.append(f"{label}: missing actor")
        if not event.get("timestamp"):
            violations.append(f"{label}: missing timestamp")
        if not event.get("evidence_refs"):
            violations.append(f"{label}: missing evidence refs")
        for ref in event.get("evidence_refs") or []:
            if not ref.get("origin_group"):
                violations.append(f"{label}: evidence ref {ref.get('ref')!r} has no origin group")
            if not str(ref.get("ref") or "").strip():
                violations.append(f"{label}: evidence ref is whitespace-only (carries no content)")
            elif not evidence_ref_resolves(ref.get("ref"), record, ctx):
                violations.append(f"{label}: evidence ref {ref.get('ref')!r} does not resolve")
        if event.get("falsifier_state_at_decision") not in ("stated", "absent"):
            violations.append(f"{label}: falsifier state at decision time not serialized")
        if stage is not None and not event.get("source_pointer"):
            violations.append(f"{label}: stamped stage event lacks a source pointer")
        target = event.get("to_stage")
        if target in STAGE_ORDER and STAGE_ORDER[target] > _CHECKED:
            actor = str(event.get("actor") or "")
            if actor not in _COMPUTATION_ACTORS and not is_named_human(actor):
                violations.append(
                    f"{label}: a transition above 'checked' was written by "
                    f"{actor!r}, not a named human (FR-029-02)")

    for event in trail["verdicts"]:
        label = f"verdict {event.get('verdict')!r}"
        if not event.get("timestamp"):
            violations.append(f"{label}: missing timestamp")
        if not event.get("evidence_refs"):
            violations.append(f"{label}: missing evidence refs")
        for ref in event.get("evidence_refs") or []:
            if not ref.get("origin_group"):
                violations.append(f"{label}: evidence ref {ref.get('ref')!r} has no origin group")
            if not str(ref.get("ref") or "").strip():
                violations.append(f"{label}: evidence ref is whitespace-only (carries no content)")
            elif not evidence_ref_resolves(ref.get("ref"), record, ctx):
                violations.append(f"{label}: evidence ref {ref.get('ref')!r} does not resolve")
        if event.get("falsifier_state_at_decision") not in ("stated", "absent"):
            violations.append(f"{label}: falsifier state at decision time not serialized")
        if not event.get("source_pointer"):
            violations.append(f"{label}: verdict lacks a source pointer")

    violations.extend(_gate_record_violations(record))

    if is_bundle(record):
        for sub in record.get("sub_claims") or []:
            if not isinstance(sub, dict):
                violations.append("bundle sub-claim is not a record")
                continue
            try:
                validate_subclaim(sub)
            except BundleValidationError as exc:
                violations.append(f"sub-claim {sub.get('claim_id')!r}: {exc}")
            if sub.get("stage") is not None and (
                    not sub.get("stage_source") or not sub.get("stage_as_of")):
                violations.append(
                    f"sub-claim {sub.get('claim_id')!r}: stamped stage lacks "
                    "stage_source/stage_as_of (plan §0)")
    return violations


# ── G2: stage-cache recompute ─────────────────────────────────────────────

class UnrecomputableStage(ValueError):
    """The stored stage's provenance names no recomputation rule."""


def recompute_stage(record: dict[str, Any], ctx: GateContext) -> tuple[str | None, str]:
    """Recompute a record's stage from its evidence.

    Returns ``(stage, method)`` where *method* names the rule the
    record's ``stage_source`` invoked. Raises
    :class:`UnrecomputableStage` when the stored stage cannot be
    recomputed — itself a defect under plan §0.
    """
    stage = record.get("stage")
    source = str(record.get("stage_source") or "")

    if is_bundle(record):
        from glossa_lab.claim_bundle import compute_parent_stage  # noqa: PLC0415
        return compute_parent_stage(record), "bundle-minimum-computation"

    if stage is None:
        if source:
            raise UnrecomputableStage(
                f"unstamped record carries stage_source {source!r} (a half-stamp)")
        return None, "honestly-unstamped"

    if source.startswith(LEDGER_REL + ":"):
        item_id = source[len(LEDGER_REL) + 1:]
        entry = ctx.ledger_entries.get(item_id)
        if entry is None:
            raise UnrecomputableStage(
                f"stage_source names ledger entry {item_id!r}, which is not in the frozen ledger")
        return entry.get("honest_stage"), "reclassification-ledger-replay"

    if source == PARENT_STAGE_SOURCE:
        # The bundle computation's provenance on a record that no
        # longer carries sub-claims cannot be recomputed.
        raise UnrecomputableStage(
            "stage_source names the bundle-minimum computation but the record "
            "carries no sub_claims to recompute from")

    if source.startswith("transition-service:"):
        m = re.search(r"stage_history\[(\d+)\]\s*$", source)
        history = record.get("stage_history") or []
        if not m or not history:
            raise UnrecomputableStage(
                f"stage_source {source!r} does not index a stage_history entry")
        idx = int(m.group(1))
        if idx != len(history) - 1 or idx >= len(history):
            raise UnrecomputableStage(
                f"stage_source indexes stage_history[{idx}] but the history "
                f"tail is stage_history[{len(history) - 1}]")
        return history[idx].get("to_stage"), "transition-service-history-tail"

    raise UnrecomputableStage(f"stage_source {source!r} names no recomputation rule")


def audit_stage_cache(record: dict[str, Any], ctx: GateContext) -> list[str]:
    """G2 for one record: the stored stage must equal its
    recomputation, and its provenance must be complete."""
    violations: list[str] = []
    stage = record.get("stage")
    if stage is not None:
        try:
            validate_stage_value(stage)
        except ValueError as exc:
            return [str(exc)]
        if not str(record.get("stage_source") or "").strip():
            violations.append("stored stage lacks stage_source (plan §0)")
        if not str(record.get("stage_as_of") or "").strip():
            violations.append("stored stage lacks stage_as_of (plan §0)")
    try:
        expected, method = recompute_stage(record, ctx)
    except (UnrecomputableStage, BundleValidationError) as exc:
        return violations + [f"stage is unrecomputable: {exc}"]
    if expected != stage:
        violations.append(
            f"stored stage {stage!r} disagrees with its recomputation "
            f"{expected!r} (method: {method})")
    # History-tail agreement for the two history-backed methods:
    # the append-only history is part of the evidence the cache
    # claims to derive from.
    history = record.get("stage_history") or []
    if method in ("reclassification-ledger-replay", "transition-service-history-tail"):
        if not history:
            violations.append(f"no stage_history backs the {method} stage")
        else:
            tail = history[-1]
            if tail.get("to_stage") != stage:
                violations.append(
                    f"stage_history tail lands on {tail.get('to_stage')!r}, "
                    f"not the stored stage {stage!r}")
            if str(record.get("stage_as_of") or "") != str(tail.get("timestamp") or ""):
                violations.append(
                    "stage_as_of does not equal the timestamp of the history "
                    "entry the stage derives from")
    if method == "bundle-minimum-computation":
        detail_stage = (record.get("stage_computation") or {}).get("stage")
        if detail_stage is not None and detail_stage != stage:
            violations.append(
                f"stored stage_computation cache says {detail_stage!r}, "
                f"stored stage is {stage!r}")
    return violations
