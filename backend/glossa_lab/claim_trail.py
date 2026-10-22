"""Per-claim inspectable trail — Spec 029 Phase C (FR-029-12; F029-C09).

Assessment finding P8: evidence trails were PARTIAL — falsifiers
and evidence strings were carried, but no claim-level record
serialized a complete trail. The frozen Phase C text
(``tasks.md`` C2, which governs) requires:

    "Per-claim API trail: evidence refs with origin groups,
    falsifier state at decision time, actor, timestamp, for
    verdicts and stage transitions alike."

This module assembles that one serialized view per claim from
what the earlier phases already built, without inventing any
of it:

* **stage + stage history** (Phases A/D) — the serialized stage
  object, and one trail event per ``stage_history`` entry, each
  carrying the record's ``stage_source`` as its **source
  pointer**, so every displayed stage is traceable to the
  evidence that produced it (the D-E invariant: a stage is
  always recomputable from the record's evidence — the stored
  value is a cache with provenance, never an assertion);
* **bundle decomposition + gate records** (Phase B, when the
  claim is a bundle) — the bundle serialization (sub-claims,
  the parent-stage computation, the contest travelling with
  the parent) plus any explanation / digestion / adverse-
  digestion records the claim carries;
* **anchor annotation** (Phase H, when the record carries it)
  — ``validation_status`` and the computed ``strict_set`` flag;
* **sources / evidence instances** (Phase I) — the claim's
  ``evidence_instances`` (merged duplicate propositions,
  preserved, never deleted), each counted by its origin group
  (its ``source_document_id``), and the AEE origin-group rule:
  a merged proposition's evidence counts its origin group
  **once** — the trail reports the distinct origin groups,
  not a raw instance count;
* **priority-register entries** (Phase C, when filed against
  this claim) — serialized by the register module, so a
  sealed entry's content cannot leak through the trail.

Every verdict record and every stage-transition event in the
trail serializes the FR-029-12 fields: evidence references
(each as ``{"ref", "origin_group"}``), the falsifier state at
decision time, the actor, and the timestamp. Where the record
does not carry a field — an extraction-era verdict names no
actor, for example — the trail says so explicitly
(``actor_recorded: False``, the field ``None``) instead of
inventing one, and the trail's own ``completeness`` block
reports which FR-029-12 fields are present and which are
missing, so an incomplete trail is visibly incomplete.

Origin groups: an evidence ref's origin group is the
independent source it came from. For an extracted claim that
is the ``source_document_id`` of the record (or, for an
evidence instance, that instance's own ``source_document_id``);
stage-history refs pointing into the reclassification ledger
belong to that ledger's origin group; a resolvable URI ref is
its own origin; Glossa's own test evidence belongs to the
program's evidence origin group.
"""

from __future__ import annotations

import copy
from typing import Any

from glossa_lab.claim_stage import serialize_stage

#: Where the canonical anchors file lives (the anchor trail's source).
ANCHORS_SOURCE = "backend/reports/INDUS_FINAL_ANCHORS.json"
#: Where extracted-claim records live (the claim trail's source).
CLAIMS_SOURCE = "glossa-indus/claims/extracted_claims"


def origin_group_for_ref(ref: Any, record: dict[str, Any]) -> str:
    """The origin group of one evidence reference (see module docstring)."""
    text = str(ref or "")
    if "reclassification-ledger" in text:
        return "spec029-reclassification-ledger"
    if text.startswith(("http://", "https://", "doi:")) or "://" in text:
        return text
    if record.get("source_document_id"):
        return str(record["source_document_id"])
    if record.get("claim_id"):
        return f"record:{record['claim_id']}"
    return "anchor-record"


def evidence_ref(ref: Any, record: dict[str, Any], *, kind: str) -> dict[str, Any]:
    """One serialized evidence reference, with its origin group."""
    return {"ref": str(ref), "origin_group": origin_group_for_ref(ref, record), "kind": kind}


def falsifier_state(record: dict[str, Any]) -> dict[str, Any]:
    """The record's falsifier state, as serialized at decision time.

    ``stated`` when the record carries a falsification condition,
    ``absent`` when it does not (an honest gap — no falsifier is
    ever invented here; cf. the Phase I finding that some
    records carry none). Bundle sub-claims each carry their own.
    """
    condition = record.get("falsification_condition")
    stated = isinstance(condition, str) and bool(condition.strip())
    sub: dict[str, Any] = {}
    for entry in record.get("sub_claims") or []:
        if isinstance(entry, dict):
            fc = entry.get("falsification_condition")
            sub[str(entry.get("kind"))] = {
                "state": "stated" if isinstance(fc, str) and fc.strip() else "absent",
                "falsification_condition": fc if isinstance(fc, str) and fc.strip() else None,
            }
    return {
        "state": "stated" if stated else "absent",
        "falsification_condition": condition if stated else None,
        "sub_claims": sub,
    }


def _record_evidence(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Evidence refs carried directly on the record, with origin groups."""
    refs: list[dict[str, Any]] = []
    source_doc = record.get("source_document_id")
    if source_doc:
        refs.append({
            "ref": str(source_doc), "origin_group": str(source_doc),
            "kind": "source_document",
        })
    if record.get("quote_fragment"):
        refs.append(evidence_ref(record["quote_fragment"], record, kind="quote_fragment"))
    for item in record.get("glossa_lab_evidence") or []:
        refs.append({
            "ref": str(item), "origin_group": "glossa_lab_evidence", "kind": "glossa_lab_evidence",
        })
    if isinstance(record.get("glossa_lab_evidence"), str) and record["glossa_lab_evidence"].strip():
        refs.append({
            "ref": record["glossa_lab_evidence"],
            "origin_group": "glossa_lab_evidence", "kind": "glossa_lab_evidence",
        })
    for item in record.get("contradicting_evidence") or []:
        refs.append(evidence_ref(item, record, kind="contradicting_evidence"))
    if record.get("basis"):
        refs.append(evidence_ref(record["basis"], record, kind="basis"))
    for sub in record.get("sub_claims") or []:
        if isinstance(sub, dict):
            for item in sub.get("evidence") or []:
                refs.append({
                    "ref": str(item),
                    "origin_group": origin_group_for_ref(item, record),
                    "kind": f"subclaim_evidence:{sub.get('kind')}",
                })
    return refs


def build_claim_trail(
    record: dict[str, Any],
    *,
    record_kind: str = "claim",
    claim_id: str | None = None,
    source_pointer: str | None = None,
    priority_entries: list[dict[str, Any]] | None = None,
    strict_set_rule: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble the per-claim inspectable trail for one record.

    *priority_entries* are raw register entries filed against
    this claim (serialized here through the register module, so
    the seal holds in this view too). *strict_set_rule* is the
    anchors file's rule metadata, when the caller read it from
    that file — it is the recomputation pointer for the
    ``strict_set`` flag, and is never invented here.
    """
    from glossa_lab.priority_register import serialize_entry  # noqa: PLC0415

    cid = claim_id or record.get("claim_id") or record.get("sign_id")
    pointer = source_pointer or (ANCHORS_SOURCE if record_kind == "anchor" else CLAIMS_SOURCE)
    falsifier = falsifier_state(record)

    # ── Evidence + origin groups (Phases I / 026 discipline) ──────────────
    evidence = _record_evidence(record)
    instances: list[dict[str, Any]] = []
    instance_groups: list[str] = []
    for inst in record.get("evidence_instances") or []:
        if not isinstance(inst, dict):
            continue
        group = str(inst.get("source_document_id") or origin_group_for_ref("", record))
        if group not in instance_groups:
            instance_groups.append(group)
        inst_record = inst.get("record") if isinstance(inst.get("record"), dict) else {}
        instances.append({
            "claim_id": inst.get("claim_id"),
            "origin_group": group,
            "source_document_id": inst.get("source_document_id"),
            "stage": serialize_stage(inst_record) if inst_record else None,
        })
        for ref in _record_evidence(inst_record):
            evidence.append({**ref, "kind": f"evidence_instance:{ref['kind']}"})
    origin_groups = sorted({r["origin_group"] for r in evidence} | set(instance_groups))

    # ── Stage transitions (Phases A/D), each with its source pointer ──────
    transitions: list[dict[str, Any]] = []
    for entry in record.get("stage_history") or []:
        if not isinstance(entry, dict):
            continue
        transitions.append({
            "event_type": "stage_transition",
            "from_stage": entry.get("from_stage"),
            "to_stage": entry.get("to_stage"),
            "actor": entry.get("actor"),
            "actor_recorded": bool(entry.get("actor")),
            "timestamp": entry.get("timestamp"),
            "evidence_refs": [
                evidence_ref(r, record, kind="stage_history")
                for r in (entry.get("evidence_refs") or [])
            ],
            "falsifier_state_at_decision": falsifier["state"],
            "reason": entry.get("reason"),
            # D-E invariant: the displayed stage is traceable to
            # its evidence through this pointer (plan §0).
            "source_pointer": record.get("stage_source") or pointer,
        })

    # ── Verdict(s): lane-1 records, serialized FR-029-12-style ────────────
    verdicts: list[dict[str, Any]] = []
    status = record.get("claim_status") or record.get("verdict")
    if status:
        actor = record.get("verdict_actor") or record.get("actor")
        verdicts.append({
            "event_type": "verdict",
            "verdict": status,
            "actor": actor,
            "actor_recorded": bool(actor),
            "timestamp": record.get("extracted_at") or record.get("stage_as_of"),
            "evidence_refs": evidence,
            "falsifier_state_at_decision": falsifier["state"],
            "not_understood": record.get("not_understood"),
            "not_understood_recorded": bool(record.get("not_understood")),
            "source_pointer": pointer,
        })

    # ── Bundle decomposition + gate records (Phase B) ─────────────────────
    bundle = None
    if isinstance(record.get("sub_claims"), list) and record["sub_claims"]:
        from glossa_lab.claim_bundle import serialize_bundle  # noqa: PLC0415

        bundle = serialize_bundle(record)
    gate_records = {
        "explanation_record": copy.deepcopy(record.get("explanation_record")),
        "digestion_record": copy.deepcopy(record.get("digestion_record")),
        "adverse_digestion": copy.deepcopy(record.get("adverse_digestion")),
    }

    # ── Anchor annotation (Phase H) ───────────────────────────────────────
    anchor_annotation = None
    if "validation_status" in record or "strict_set" in record:
        anchor_annotation = {
            "validation_status": record.get("validation_status"),
            "strict_set": record.get("strict_set"),
            "source_pointer": pointer,
            "strict_set_rule": strict_set_rule,
        }

    # ── Priority-register entries filed against this claim (Phase C) ──────
    priority = [serialize_entry(e) for e in (priority_entries or [])]

    # ── Completeness: the trail reports its own gaps (FR-029-12) ──────────
    events = transitions + verdicts
    missing: list[str] = []
    if not evidence:
        missing.append("evidence_refs")
    if not origin_groups:
        missing.append("origin_groups")
    if falsifier["state"] != "stated":
        missing.append("falsifier_state")
    if events and not all(e["actor_recorded"] for e in events):
        missing.append("actor")
    if events and not all(e.get("timestamp") for e in events):
        missing.append("timestamp")
    if not events:
        missing.append("events")

    return {
        "claim_id": cid,
        "record_kind": record_kind,
        "source_pointer": pointer,
        "stage": serialize_stage(record),
        "verified_unexplained": record.get("verified_unexplained"),
        "evidence": evidence,
        "origin_groups": origin_groups,
        "origin_group_count": len(origin_groups),
        "evidence_instances": instances,
        "merged_into": record.get("merged_into"),
        "falsifier": falsifier,
        "stage_transitions": transitions,
        "verdicts": verdicts,
        "bundle": bundle,
        "gate_records": gate_records,
        "anchor_annotation": anchor_annotation,
        "priority_entries": priority,
        "completeness": {
            "complete": not missing,
            "missing": missing,
            "fields": {
                "evidence_refs": bool(evidence),
                "origin_groups": bool(origin_groups),
                "falsifier_state": falsifier["state"] == "stated",
                "actor": bool(events) and all(e["actor_recorded"] for e in events),
                "timestamp": bool(events) and all(bool(e.get("timestamp")) for e in events),
            },
        },
    }
