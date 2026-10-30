"""Indus Evidence Graph API.

Mounted at ``/api/v1/indus-evidence``.

Spec 081 step 3 (T015; FR-018): the claim/library read surface also
lives at program-scoped paths — ``/api/v1/programs/{program_id}/…`` —
implemented at the bottom of this module. The ``/indus-evidence``
paths are the compatibility shim for one release: they serve the
Indus program's store exactly as the scoped paths do, and retire
with the shim's release. Write/intake/sweep paths are not scoped
this step.

Endpoints
---------
GET  /library                   List registered literature documents
GET  /claims                    List extracted claims (with filters)
GET  /claims/aee-scores         AEE-library scoring of all extracted claims
GET  /claims/{id}/trail         Per-claim inspectable trail (Spec 029 Phase C)
POST /priority-register         Priority-register intake (Spec 029 Phase C, OD-6)
GET  /priority-register         Public priority register (sealed-safe)
POST /priority-register/{id}/extend   Extend reveal date (once only)
POST /priority-register/{id}/unseal   Unseal by claimant publication
GET  /hypotheses                List hypothesis model summaries

POST /upload                    Upload a PDF → run intake
POST /import-url                Import a paper from a URL → run intake
POST /intake/run                Re-run claims extraction pipeline on all registered docs

GET  /sweep/config              Read project sweep.yaml
PUT  /sweep/config              Save project sweep.yaml
POST /sweep/run                 Run sweep using sweep.yaml → background job
GET  /sweep/candidates          Read latest sweep candidates file
POST /sweep/intake              Intake a single sweep candidate (by URL / doi / title)

All filesystem operations target the ``glossa-indus/`` directory which lives two
levels above this file's package root (alongside ``backend/``).
"""
from __future__ import annotations

import asyncio
import ipaddress
import json
import logging
import re
import socket
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile
from pydantic import BaseModel

_log = logging.getLogger("glossa_lab.api.indus_evidence")
router = APIRouter(prefix="/api/v1/indus-evidence", tags=["indus-evidence"])
scoped_router = APIRouter(prefix="/api/v1/programs", tags=["programs-evidence"])

# ── Path constants ────────────────────────────────────────────────────────────

_REPO_ROOT    = Path(__file__).resolve().parent.parent.parent.parent
_EVIDENCE_BASE = _REPO_ROOT / "glossa-indus"
_LIT_DOCS     = _EVIDENCE_BASE / "literature" / "documents"
_CLAIMS_DIR   = _EVIDENCE_BASE / "claims" / "extracted_claims"
_HYPO_MODELS  = _EVIDENCE_BASE / "hypotheses" / "models"
_SWEEP_CFG    = _EVIDENCE_BASE / "config" / "sweep.yaml"
_SWEEP_CANDS  = _EVIDENCE_BASE / "logs" / "sweep_candidates_latest.json"
_RAW_UPLOADS  = _EVIDENCE_BASE / "raw" / "user_uploads"
_SCRIPTS      = _EVIDENCE_BASE / "scripts"

# ── Intake hardening (Leg C red team, findings C-05 / C-06) ──────────────────
# Uploads and URL imports are the backend's untrusted-input boundary:
# filenames are never trusted as paths, bodies are size-capped and
# magic-checked, and outbound fetches refuse non-public destinations
# (SSRF guard). See legC-findings.md (hardening program, 2026-10-29).

_MAX_INTAKE_BYTES = 25 * 1024 * 1024  # 25 MiB cap for uploads and URL imports
_PDF_MAGIC = b"%PDF-"


def _safe_upload_name(filename: str) -> str:
    """Reduce an untrusted upload filename to a bare, sanitised basename.

    Directory components (including ``../`` traversal) are stripped, so
    the result can never escape the uploads directory it is joined to.
    """
    name = Path(filename or "").name
    name = re.sub(r"[^A-Za-z0-9._\-]", "_", name)[:120]
    return name


def _ip_is_public(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return not (
        ip.is_private or ip.is_loopback or ip.is_link_local
        or ip.is_reserved or ip.is_multicast or ip.is_unspecified
    )


def _assert_fetchable_url(url: str) -> None:
    """SSRF guard for caller-supplied fetch URLs (finding C-06).

    Allows only http/https URLs whose host is public: literal IPs must
    be public, ``localhost`` names are refused, and hostnames are
    refused when DNS resolution yields any non-public address. When
    DNS resolution itself fails, the fetch is left to fail naturally
    downstream (reported as a download failure, never silently
    allowed to a known-private target).
    """
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(
            status_code=400, detail="Only http/https URLs may be imported")
    host = (parsed.hostname or "").strip().lower()
    if not host or host == "localhost" or host.endswith(".localhost"):
        raise HTTPException(
            status_code=400, detail="URL host is not a public address")
    try:
        ips = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            infos = socket.getaddrinfo(host, None)
        except Exception:  # noqa: BLE001 — unresolved: download will fail as 502
            return
        ips = []
        for info in infos:
            try:
                ips.append(ipaddress.ip_address(info[4][0]))
            except ValueError:
                continue
    if any(not _ip_is_public(ip) for ip in ips):
        raise HTTPException(
            status_code=400, detail="URL host resolves to a non-public address")


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-run the SSRF guard on every redirect target."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ANN202
        try:
            _assert_fetchable_url(newurl)
        except HTTPException as exc:
            raise ValueError(f"Redirect blocked: {exc.detail}") from exc
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch_url_capped(url: str) -> bytes:
    """Fetch *url* under the SSRF guard with a hard size cap."""
    _assert_fetchable_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/1.0"})
    opener = urllib.request.build_opener(_GuardedRedirectHandler())
    with opener.open(req, timeout=30) as resp:  # noqa: S310 — guarded above
        content = resp.read(_MAX_INTAKE_BYTES + 1)
    if len(content) > _MAX_INTAKE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Remote file exceeds the {_MAX_INTAKE_BYTES} byte intake cap")
    return content


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── YAML helper (stdlib-only fallback, optional PyYAML) ───────────────────────

def _load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file. Falls back to a minimal line-parser if PyYAML is absent."""
    try:
        import yaml  # noqa: PLC0415
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Minimal fallback: parse only simple key: value lines
        data: dict = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and ":" in stripped:
                    k, _, v = stripped.partition(":")
                    data[k.strip()] = v.strip()
        return data


def _dump_yaml(data: dict[str, Any], path: Path) -> None:
    try:
        import yaml  # noqa: PLC0415
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    except ImportError:
        # Minimal fallback: write as JSON inside a YAML comment block
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# Auto-saved by Glossa-Lab (PyYAML not installed — JSON fallback)\n"
            + json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


# ── Library ───────────────────────────────────────────────────────────────────

@router.get("/library")
async def list_library(
    q: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List all registered literature documents."""
    _LIT_DOCS.mkdir(parents=True, exist_ok=True)
    docs: list[dict[str, Any]] = []
    for f in sorted(_LIT_DOCS.glob("*.json")):
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception:
            continue
        if q:
            haystack = (
                (d.get("detected_title") or "")
                + " "
                + " ".join(d.get("detected_authors") or [])
            ).lower()
            if q.lower() not in haystack:
                continue
        if status and d.get("processing_status") != status:
            continue

        # Attach claim count from extracted_claims if available
        claim_file = _CLAIMS_DIR / f"{d.get('document_id', f.stem)}.json"
        claim_count = 0
        if claim_file.exists():
            try:
                cd = json.loads(claim_file.read_text("utf-8"))
                claim_count = cd.get("total_claims", 0)
            except Exception:
                pass

        # Spec 083 (T023): evidence records carry the same attribution
        # label as claims (see list_claims) in cloud mode.
        from glossa_lab.cloud_scope import attribution_label  # noqa: PLC0415
        from glossa_lab.config import cloud_mode_enabled  # noqa: PLC0415

        docs.append({
            "document_id":        d.get("document_id", f.stem),
            **(
                {"attribution_label": attribution_label(d)}
                if cloud_mode_enabled() else {}
            ),
            "title":              d.get("detected_title", ""),
            "authors":            d.get("detected_authors", []),
            "year":               d.get("detected_year"),
            "doi":                d.get("detected_doi"),
            "file_size_bytes":    d.get("file_size_bytes", 0),
            "access_type":        d.get("access_type", ""),
            "license_status":     d.get("license_status", ""),
            "processing_status":  d.get("processing_status", ""),
            "ocr_required":       d.get("ocr_required", False),
            "intake_date":        d.get("intake_date", ""),
            "claim_count":        claim_count,
            "claim_extraction_status": d.get("claim_extraction_status", ""),
        })

    total = len(docs)
    return {"documents": docs[offset: offset + limit], "total": total, "limit": limit, "offset": offset}


# ── Claims ────────────────────────────────────────────────────────────────────

@router.get("/claims")
async def list_claims(
    q: str | None = None,
    claim_type: str | None = None,
    claim_status: str | None = None,
    doc_id: str | None = None,
    sign: str | None = None,
    limit: int = 200,
    offset: int = 0,
    aee: bool = False,
    verified_unexplained: bool | None = None,
) -> dict[str, Any]:
    """List all extracted claims across all registered documents.

    With ``?aee=true`` each returned claim gains an additive ``aee_score``
    field scored by the Applied Epistemic Engineering library
    (``glossa_lab.aee_core``); the default response shape is unchanged.

    Spec 029 (FR-029-01/03): every returned claim also carries its
    lane-2 lifecycle ``stage`` serialized as a distinct object (stage
    value, provenance, and history summary — ``stage: None`` until a
    record is stamped; a stage is never invented here) and the computed
    ``verified_unexplained`` risk flag, which the
    ``?verified_unexplained=true/false`` parameter can filter on.
    The lane-1 score, when requested, stays a separate object
    (``aee_score`` / ``lane1_score``) — never folded into ``stage``.

    Spec 029 Phase E2 (FR-029-05/09): each claim additionally carries
    ``not_understood`` (the record's own statement, or ``None`` when
    no human has authored one — the absence is serialized, never
    filled with generated text) with ``not_understood_recorded``, and
    ``bundle``: the Phase B bundle serialization for bundle parents
    (the contest travels with the parent), ``None`` for records that
    are not bundle parents.
    """
    from glossa_lab.claim_bundle import is_bundle, serialize_bundle  # noqa: PLC0415
    from glossa_lab.claim_stage import compute_verified_unexplained, serialize_stage  # noqa: PLC0415

    _CLAIMS_DIR.mkdir(parents=True, exist_ok=True)
    all_claims: list[dict[str, Any]] = []
    for f in sorted(_CLAIMS_DIR.glob("*.json")):
        if doc_id and f.stem != doc_id:
            continue
        try:
            record = json.loads(f.read_text("utf-8"))
        except Exception:
            continue
        for claim in record.get("claims", []):
            if claim_type and claim.get("claim_type") != claim_type:
                continue
            if claim_status and claim.get("claim_status") != claim_status:
                continue
            if q and q.lower() not in (claim.get("normalized_claim") or "").lower():
                continue
            if sign:
                signs_involved = " ".join(claim.get("signs_involved") or [])
                if sign.lower() not in signs_involved.lower():
                    continue
            entry = {
                **claim,
                "_source_file": f.stem,
            }
            # Spec 083 (T023): attribution at serialization. A claim
            # record with a cloud actor stamp renders that username;
            # every other record (the whole desktop/bundle-imported
            # register today) renders "via desktop import" — computed
            # here, never written back into the stored record.
            from glossa_lab.cloud_scope import attribution_label  # noqa: PLC0415
            from glossa_lab.config import cloud_mode_enabled  # noqa: PLC0415

            if cloud_mode_enabled():
                entry["attribution_label"] = attribution_label(claim)
            entry["stage"] = serialize_stage(claim)
            entry["verified_unexplained"] = compute_verified_unexplained(claim)
            # Phase E2: the not-understood statement travels with the
            # verdict display. Absence is serialized as None — it is a
            # stated gap in the record, never filled in here.
            _nu = claim.get("not_understood")
            entry["not_understood"] = _nu if isinstance(_nu, str) and _nu.strip() else None
            entry["not_understood_recorded"] = entry["not_understood"] is not None
            # Phase E2: a bundle parent's contest state renders on the
            # parent wherever the parent renders (FR-029-05).
            entry["bundle"] = None
            entry["bundle_serialization_error"] = None
            if is_bundle(claim):
                try:
                    entry["bundle"] = serialize_bundle(claim)
                except Exception as exc:  # noqa: BLE001 — a malformed bundle must not 500 the listing; the failure is serialized, not hidden
                    entry["bundle_serialization_error"] = str(exc)
            if verified_unexplained is not None and entry["verified_unexplained"] != verified_unexplained:
                continue
            all_claims.append(entry)

    total = len(all_claims)
    page = all_claims[offset: offset + limit]
    if aee and page:
        from glossa_lab.aee_core import score_claim_dicts  # noqa: PLC0415

        # Score the raw records, not the serialized entries: on an
        # entry, ``stage`` is the serialized stage object, while the
        # AEE adapter reads the record's flat stage fields.
        raw_page = []
        for claim in page:
            raw = dict(claim)
            stage_obj = claim.get("stage") or {}
            raw["stage"] = stage_obj.get("stage")
            raw["stage_source"] = stage_obj.get("stage_source")
            raw["stage_as_of"] = stage_obj.get("stage_as_of")
            raw["stage_history"] = stage_obj.get("stage_history") or []
            raw_page.append(raw)
        scores = score_claim_dicts(raw_page)
        for claim in page:
            score = scores.get(str(claim.get("claim_id") or ""))
            claim["aee_score"] = score
            claim["lane1_score"] = score
            # Recompute with the lane-1 score in hand: a high score
            # band can fire the flag where the status alone did not.
            # (claim["stage"] is the serialized stage object here, so
            # the flag computation reads the raw stage value from it.)
            claim["verified_unexplained"] = compute_verified_unexplained(
                {
                    "stage": claim["stage"].get("stage"),
                    "claim_status": claim.get("claim_status"),
                },
                score=score,
            )
    return {
        "claims": page,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/claims/aee-scores")
async def claims_aee_scores() -> dict[str, Any]:
    """AEE-backed scoring of every extracted claim (additive endpoint).

    Scores are computed by the Applied Epistemic Engineering library via
    ``glossa_lab.aee_core.assessment_summary`` — see that module for the
    Glossa→AEE mapping. Existing endpoints are unaffected.

    Spec 029 (FR-029-01/03): each per-claim entry serializes the lane-2
    ``stage`` object and the lane-1 score (``aee_score`` /
    ``lane1_score``) as distinct objects, plus the computed
    ``verified_unexplained`` risk flag.
    """
    from glossa_lab.aee_core import assessment_summary  # noqa: PLC0415

    return assessment_summary(_CLAIMS_DIR)


# ── Priority register (Spec 029 Phase C, FR-029-11 / OD-6) ───────────────────
#
# Runtime state only: the store and its seal key live under the
# gitignored ``.glossa-state/`` directory (plan §5/§V — register
# records live in the backend store; a claimant's contact is kept
# private there and never serialized).

_PRIORITY_STORE = _REPO_ROOT / ".glossa-state" / "priority_register.json"
_PRIORITY_KEY = _REPO_ROOT / ".glossa-state" / "priority_register.key"
_ANCHORS_FILE = _REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"


def _load_priority_register():
    from glossa_lab.priority_register import load_register  # noqa: PLC0415

    return load_register(_PRIORITY_STORE, _PRIORITY_KEY)


def _save_priority_register(register) -> None:
    from glossa_lab.priority_register import save_register  # noqa: PLC0415

    save_register(register, _PRIORITY_STORE)


def _priority_error_status(exc: Exception) -> int:
    return 404 if str(exc).startswith("no priority-register entry") else 400


class PriorityIntakeBody(BaseModel):
    claimant: str = ""
    claimant_contact: str = ""
    reading: str = ""
    evidence: list[str] = []
    claim_id: str | None = None
    reveal_date: str | None = None
    supersedes: str | None = None


@router.post("/priority-register")
async def priority_register_intake(body: PriorityIntakeBody) -> dict[str, Any]:
    """File a reading in the priority register (OD-6: public at intake).

    Issuance is on record completeness alone — no score, stage, or
    verdict is required, implied, or stored. The response carries
    the entry id and the public record (claimant + server
    timestamp + SHA-256 of the reading); the content stays sealed.
    """
    from glossa_lab.priority_register import (  # noqa: PLC0415
        PriorityRegisterError,
        public_record,
        serialize_entry,
    )

    register = _load_priority_register()
    try:
        entry = register.register(
            claimant=body.claimant,
            claimant_contact=body.claimant_contact,
            reading=body.reading,
            evidence=body.evidence,
            claim_id=body.claim_id,
            reveal_date=body.reveal_date,
            supersedes=body.supersedes,
        )
    except PriorityRegisterError as exc:
        raise HTTPException(status_code=_priority_error_status(exc), detail=str(exc)) from exc
    _save_priority_register(register)
    return {
        "entry_id": entry["entry_id"],
        "public_record": public_record(entry),
        "entry": serialize_entry(entry),
    }


@router.get("/priority-register")
async def priority_register_list() -> dict[str, Any]:
    """The public register: public records + sealed-safe entry views.

    Reading the register applies the reveal-date unseal trigger:
    any entry whose reveal date has been reached is unsealed (and
    the event recorded) before the listing is serialized. Sealed
    entries expose no content and no contact detail.
    """
    from glossa_lab.priority_register import (  # noqa: PLC0415
        public_record,
        serialize_entry,
    )

    register = _load_priority_register()
    if register.unseal_due():
        _save_priority_register(register)
    entries = [serialize_entry(e) for e in register.entries]
    return {
        "entries": entries,
        "public_records": [public_record(e) for e in register.entries],
        "total": len(entries),
    }


@router.get("/priority-register/{entry_id}")
async def priority_register_get(entry_id: str) -> dict[str, Any]:
    """One register entry, sealed-safe (content only once unsealed)."""
    from glossa_lab.priority_register import (  # noqa: PLC0415
        PriorityRegisterError,
        serialize_entry,
    )

    register = _load_priority_register()
    if register.unseal_due():
        _save_priority_register(register)
    try:
        entry = register.get(entry_id)
    except PriorityRegisterError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"entry": serialize_entry(entry)}


class PriorityExtendBody(BaseModel):
    new_reveal_date: str


@router.post("/priority-register/{entry_id}/extend")
async def priority_register_extend(entry_id: str, body: PriorityExtendBody) -> dict[str, Any]:
    """Extend an entry's reveal date — once only, as a dated record.

    A refused extension is recorded in the entry's history before
    the error is returned (the refusal is part of the register),
    so the store is saved on both paths.
    """
    from glossa_lab.priority_register import (  # noqa: PLC0415
        PriorityRegisterError,
        serialize_entry,
    )

    register = _load_priority_register()
    register.unseal_due()
    try:
        entry = register.extend_reveal_date(entry_id, body.new_reveal_date)
    except PriorityRegisterError as exc:
        _save_priority_register(register)
        raise HTTPException(status_code=_priority_error_status(exc), detail=str(exc)) from exc
    _save_priority_register(register)
    return {"entry": serialize_entry(entry)}


class PriorityUnsealBody(BaseModel):
    reading: str = ""
    evidence: list[str] = []


@router.post("/priority-register/{entry_id}/unseal")
async def priority_register_unseal(entry_id: str, body: PriorityUnsealBody) -> dict[str, Any]:
    """Unseal by claimant publication: present the content.

    The presented content unseals the entry only when its
    canonical SHA-256 matches the hash published at intake;
    a mismatched presentation is refused and recorded.
    """
    from glossa_lab.priority_register import (  # noqa: PLC0415
        PriorityRegisterError,
        serialize_entry,
    )

    register = _load_priority_register()
    try:
        entry = register.unseal_by_publication(
            entry_id, reading=body.reading, evidence=body.evidence,
        )
    except PriorityRegisterError as exc:
        _save_priority_register(register)
        raise HTTPException(status_code=_priority_error_status(exc), detail=str(exc)) from exc
    _save_priority_register(register)
    return {"entry": serialize_entry(entry)}


# ── Per-claim trail view (Spec 029 Phase C, FR-029-12) ────────────────────────

@router.get("/claims/{claim_id}/trail")
async def claim_trail(claim_id: str) -> dict[str, Any]:
    """The per-claim inspectable trail for one claim or anchor.

    Assembles (``glossa_lab.claim_trail``): stage + stage history
    with source pointers, evidence refs with origin groups, the
    falsifier state at decision time, actor and timestamp for
    verdicts and stage transitions alike, bundle decomposition
    and gate records when the claim is a bundle, the anchor
    annotation when present, evidence instances, and any
    priority-register entries filed against the claim (sealed
    content cannot leak through this view).
    """
    from glossa_lab.claim_trail import build_claim_trail  # noqa: PLC0415

    record: dict[str, Any] | None = None
    record_kind = "claim"
    strict_rule: dict[str, Any] | None = None
    _CLAIMS_DIR.mkdir(parents=True, exist_ok=True)
    for f in sorted(_CLAIMS_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text("utf-8"))
        except Exception:
            continue
        for claim in data.get("claims", []):
            if claim.get("claim_id") == claim_id:
                record = claim
                break
        if record is not None:
            break
    if record is None and _ANCHORS_FILE.exists():
        try:
            anchors_data = json.loads(_ANCHORS_FILE.read_text("utf-8"))
            anchor = (anchors_data.get("anchors") or {}).get(claim_id)
        except Exception:
            anchor = None
        if isinstance(anchor, dict):
            record = {**anchor, "claim_id": claim_id}
            record_kind = "anchor"
            annotation = (anchors_data.get("metadata") or {}).get(
                "spec029_phase_h_annotation") or {}
            strict_rule = annotation.get("strict_set_rule")
    if record is None:
        raise HTTPException(status_code=404, detail=f"no claim or anchor {claim_id!r}")

    priority_entries: list[dict[str, Any]] = []
    if _PRIORITY_STORE.exists():
        register = _load_priority_register()
        if register.unseal_due():
            _save_priority_register(register)
        priority_entries = register.entries_for_claim(claim_id)
    trail = build_claim_trail(
        record,
        record_kind=record_kind,
        claim_id=claim_id,
        priority_entries=priority_entries,
        strict_set_rule=strict_rule,
    )
    # Spec 083 (T023): the trail is the digestion/evidence surface —
    # label its actor the same way the claims list does.
    from glossa_lab.cloud_scope import attribution_label  # noqa: PLC0415
    from glossa_lab.config import cloud_mode_enabled  # noqa: PLC0415

    if cloud_mode_enabled() and isinstance(trail, dict):
        trail = {**trail, "attribution_label": attribution_label(record)}
    return trail


# ── Hypotheses ────────────────────────────────────────────────────────────────

@router.get("/hypotheses")
async def list_hypotheses() -> dict[str, Any]:
    """List hypothesis model summaries from YAML files."""
    _HYPO_MODELS.mkdir(parents=True, exist_ok=True)
    models: list[dict[str, Any]] = []
    for f in sorted(_HYPO_MODELS.glob("*.yaml")):
        try:
            d = _load_yaml(f)
        except Exception:
            d = {}
        models.append({
            "file": f.name,
            "model_id":   d.get("model_id", f.stem),
            "model_name": d.get("model_name", ""),
            "status":     d.get("status", ""),
            "model_type": d.get("model_type", ""),
            "n_claims":   len(d.get("core_claims") or []),
            "n_tests":    len(d.get("tests_planned") or []),
        })
    return {"models": models}


# ── Program-scoped equivalents (Spec 081 step 3, T015; FR-018) ───────────────
#
# The evidence store on disk (glossa-indus/) belongs to the default
# program this release. The scoped routes resolve a program id to one
# of two scopes:
#
#   "store" — the program that owns the on-disk store; its scoped
#             reads delegate to the handlers above, unchanged.
#   "empty" — any other existing program; it has no evidence store
#             yet, so its register, library and hypothesis list are
#             honestly empty (never the store program's data — one
#             program's claims are never served under another's name).
#
# An unknown program id 404s. The /indus-evidence paths above are the
# one-release compatibility shim for these routes.

_STORE_PROGRAM_ID = "indus_decipherment"


async def _program_scope(program_id: str) -> str:
    if program_id == _STORE_PROGRAM_ID:
        return "store"
    from glossa_lab.database import get_db  # noqa: PLC0415

    db = get_db()
    if db is not None and await db.get_project(program_id) is not None:
        return "empty"
    raise HTTPException(404, f"Program {program_id} not found")


@scoped_router.get("/{program_id}/claims")
async def list_program_claims(
    program_id: str,
    q: str | None = None,
    claim_type: str | None = None,
    claim_status: str | None = None,
    doc_id: str | None = None,
    sign: str | None = None,
    limit: int = 200,
    offset: int = 0,
    aee: bool = False,
    verified_unexplained: bool | None = None,
) -> dict[str, Any]:
    """Program-scoped claim register (the /indus-evidence/claims shim
    serves the store program's same register)."""
    if await _program_scope(program_id) == "empty":
        return {"claims": [], "total": 0, "limit": limit, "offset": offset}
    return await list_claims(
        q=q, claim_type=claim_type, claim_status=claim_status,
        doc_id=doc_id, sign=sign, limit=limit, offset=offset, aee=aee,
        verified_unexplained=verified_unexplained,
    )


@scoped_router.get("/{program_id}/claims/aee-scores")
async def program_claims_aee_scores(program_id: str) -> dict[str, Any]:
    """Program-scoped AEE scoring; an empty-scope program scores its
    (empty) register, yielding the summary's natural empty shape."""
    if await _program_scope(program_id) == "empty":
        import tempfile  # noqa: PLC0415

        from glossa_lab.aee_core import assessment_summary  # noqa: PLC0415

        with tempfile.TemporaryDirectory() as empty_dir:
            return assessment_summary(Path(empty_dir))
    return await claims_aee_scores()


@scoped_router.get("/{program_id}/claims/{claim_id}/trail")
async def program_claim_trail(program_id: str, claim_id: str) -> dict[str, Any]:
    """Program-scoped per-claim trail; a claim id is only resolvable
    inside the program whose register holds it."""
    if await _program_scope(program_id) == "empty":
        raise HTTPException(404, f"Claim {claim_id} not found in program {program_id}")
    return await claim_trail(claim_id)


@scoped_router.get("/{program_id}/library")
async def list_program_library(
    program_id: str,
    q: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """Program-scoped source library (the /indus-evidence/library shim
    serves the store program's same library)."""
    if await _program_scope(program_id) == "empty":
        return {"documents": [], "total": 0, "limit": limit, "offset": offset}
    return await list_library(q=q, status=status, limit=limit, offset=offset)


@scoped_router.get("/{program_id}/hypotheses")
async def list_program_hypotheses(program_id: str) -> dict[str, Any]:
    """Program-scoped hypothesis models; under the Q7 fold-in these
    read as the register's early-state claims on the claims surface —
    the endpoint remains for the record."""
    if await _program_scope(program_id) == "empty":
        return {"models": []}
    return await list_hypotheses()


# ── Upload PDF ────────────────────────────────────────────────────────────────

@router.post("/upload")
async def upload_paper(
    file: UploadFile,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Upload a PDF and queue it for intake."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    # C-05: never trust the client filename as a path — basename only.
    safe_name = _safe_upload_name(file.filename)
    if not safe_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    if len(content) > _MAX_INTAKE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Upload exceeds the {_MAX_INTAKE_BYTES} byte intake cap")
    if not content.startswith(_PDF_MAGIC):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported (content is not a PDF)")

    _RAW_UPLOADS.mkdir(parents=True, exist_ok=True)
    dest = _RAW_UPLOADS / safe_name
    dest.write_bytes(content)
    _log.info("uploaded: %s (%d bytes)", dest.name, len(content))

    background_tasks.add_task(_run_intake_on_file, str(dest))
    return {
        "status": "uploaded",
        "filename": safe_name,
        "size_bytes": len(content),
        "message": "Intake queued — document will be processed in the background.",
    }


def _run_intake_on_file(file_path: str) -> None:
    import subprocess  # noqa: PLC0415
    intake_script = _SCRIPTS / "indus_intake.py"
    try:
        subprocess.run(
            [sys.executable, str(intake_script), "--file", file_path],
            capture_output=True, text=True, timeout=120,
        )
    except Exception as exc:
        _log.warning("intake failed for %s: %s", file_path, exc)


# ── Import from URL ───────────────────────────────────────────────────────────

class ImportUrlBody(BaseModel):
    url: str
    title: str = ""
    doi: str = ""
    authors: list[str] = []
    year: int | None = None


@router.post("/import-url")
async def import_url(body: ImportUrlBody, background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Download a PDF from a URL and queue it for intake."""
    url = body.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="url is required")

    # Derive a safe filename from the URL
    parsed  = urllib.parse.urlparse(url)
    fname   = Path(parsed.path).name or "paper.pdf"
    if not fname.lower().endswith(".pdf"):
        fname += ".pdf"
    # Sanitize
    fname = re.sub(r"[^A-Za-z0-9._\-]", "_", fname)[:120]

    _RAW_UPLOADS.mkdir(parents=True, exist_ok=True)
    dest = _RAW_UPLOADS / fname

    # C-06: SSRF guard + size cap (raises 400/413 before any write).
    _assert_fetchable_url(url)
    try:
        content = _fetch_url_capped(url)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to download: {exc}") from exc
    dest.write_bytes(content)

    background_tasks.add_task(_run_intake_on_file, str(dest))
    return {
        "status": "downloaded",
        "filename": fname,
        "size_bytes": len(content),
        "source_url": url,
        "message": "Download complete — intake queued.",
    }


# ── Intake pipeline runner ────────────────────────────────────────────────────

@router.post("/intake/run")
async def run_intake_pipeline(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Re-run indus_intake.py (scan) + indus_claims.py on all registered docs."""
    background_tasks.add_task(_run_full_intake)
    return {"status": "queued", "message": "Full intake + claim extraction pipeline queued."}


def _run_full_intake() -> None:
    import subprocess  # noqa: PLC0415
    intake = _SCRIPTS / "indus_intake.py"
    claims = _SCRIPTS / "indus_claims.py"
    for script in (intake, claims):
        if not script.exists():
            continue
        try:
            args = [sys.executable, str(script)]
            if script.name == "indus_intake.py":
                args += ["--scan", str(_RAW_UPLOADS)]
            subprocess.run(args, capture_output=True, text=True, timeout=300)
        except Exception as exc:
            _log.warning("pipeline script %s failed: %s", script.name, exc)


# ── Sweep: read / write config ────────────────────────────────────────────────

@router.get("/sweep/config")
async def get_sweep_config() -> dict[str, Any]:
    """Read the project sweep.yaml configuration."""
    if not _SWEEP_CFG.exists():
        raise HTTPException(status_code=404, detail="sweep.yaml not found — create it via PUT /sweep/config")
    try:
        return _load_yaml(_SWEEP_CFG)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not parse sweep.yaml: {exc}") from exc


class SweepConfigBody(BaseModel):
    schema_version: str = "1.0"
    sweep: dict[str, Any] = {}


@router.put("/sweep/config")
async def save_sweep_config(body: SweepConfigBody) -> dict[str, Any]:
    """Save a new sweep.yaml configuration."""
    try:
        _dump_yaml(body.model_dump(), _SWEEP_CFG)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not write sweep.yaml: {exc}") from exc
    return {"status": "saved", "path": str(_SWEEP_CFG)}


# ── Sweep: run ────────────────────────────────────────────────────────────────

@router.post("/sweep/run")
async def run_sweep(background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Run the sweep in the background using sweep.yaml. Returns a job ack."""
    if not _SWEEP_CFG.exists():
        raise HTTPException(status_code=404, detail="sweep.yaml not found — configure it first")

    background_tasks.add_task(_bg_sweep)
    return {
        "status": "running",
        "message": "Sweep started in background. Poll GET /sweep/candidates for results.",
    }


async def _bg_sweep() -> None:
    """Background task: build a TopicProfile from sweep.yaml and run the fetchers."""
    try:
        cfg = _load_yaml(_SWEEP_CFG)
        sweep = cfg.get("sweep", {})

        from glossa_lab.discovery.fetchers import _build_fetchers, now_utc, to_iso  # noqa: PLC0415
        from glossa_lab.discovery.fetchers.base import TopicProfile  # noqa: PLC0415

        # Flatten keywords into one list for TopicProfile
        kw_block = sweep.get("keywords", {})
        all_kws: list[str] = (
            list(kw_block.get("primary", []))
            + list(kw_block.get("secondary", []))
        )
        # Only add expansions if total is still < 30
        if len(all_kws) < 30:
            all_kws += list(kw_block.get("expansions", []))

        source_overrides: dict[str, dict] = {}
        sources_cfg = sweep.get("sources", {})
        for src, opts in sources_cfg.items():
            if not isinstance(opts, dict) or not opts.get("enabled", True):
                continue
            ovr: dict = {}
            mr = opts.get("max_results")
            if mr:
                ovr["per_page"] = mr
                ovr["max_results"] = mr
                ovr["rows"] = mr
            cats = opts.get("categories")
            if cats:
                ovr["search_query_extra"] = " OR ".join(f"cat:{c}" for c in cats)
            if ovr:
                source_overrides[src] = ovr

        profile = TopicProfile(
            id="evidence_sweep",
            label=sweep.get("name", "Evidence Sweep"),
            description=sweep.get("description", ""),
            keywords=all_kws,
            exclusions=list(sweep.get("exclusions", [])),
            languages=list((sweep.get("filters") or {}).get("languages") or ["en"]),
            source_overrides=source_overrides,
        )

        # Only enabled sources
        enabled_sources = [
            src for src, opts in sources_cfg.items()
            if isinstance(opts, dict) and opts.get("enabled", True)
        ]

        fetchers = _build_fetchers(enabled_sources if enabled_sources else None)
        fetched_at = to_iso(now_utc())
        raw_items: list[dict[str, Any]] = []

        async def _one(f) -> None:
            try:
                items = list(await f.fetch(profile))
                for item in items:
                    # RawItem stores extra metadata in item.raw dict
                    # (doi, abstract/summary, authors, pdf_url, kind)
                    # — these fields are NOT direct attributes of RawItem
                    _raw = item.raw or {}
                    _doi = (_raw.get("doi") or "").strip()
                    _summary = (
                        _raw.get("abstract") or
                        _raw.get("summary") or
                        _raw.get("tldr") or ""
                    )
                    _authors = _raw.get("authors") or []
                    _pdf_url = _raw.get("pdf_url") or _raw.get("open_access_pdf") or ""
                    _kind = _raw.get("kind") or "study"
                    raw_items.append({
                        "source":        f.source,
                        "title":         item.title or "",
                        "url":           item.url or "",
                        "doi":           _doi,
                        "authors":       list(_authors),
                        "published_at":  item.published_at or "",
                        "summary":       str(_summary)[:400],
                        "pdf_url":       _pdf_url,
                        "open_access":   bool(_pdf_url),
                        "kind":          _kind,
                        "fetched_at":    fetched_at,
                    })
            except Exception as exc:  # noqa: BLE001
                _log.warning("sweep fetcher %s: %s", f.source, exc)

        # Split into parallel and sequential (rate-limited)
        parallel   = [f for f in fetchers if getattr(f, "rate_delay", 0) <= 0]
        sequential = [f for f in fetchers if getattr(f, "rate_delay", 0) > 0]
        await asyncio.gather(*[_one(f) for f in parallel])
        for f in sequential:
            await _one(f)

        # De-duplicate by normalized title + doi
        seen: set[str] = set()
        unique_items: list[dict] = []
        for it in raw_items:
            key = _normalize_title(it["title"]) or it["doi"] or it["url"]
            if key and key not in seen:
                seen.add(key)
                unique_items.append(it)

        # Filter against already-registered papers
        registered_keys = _registered_paper_keys()
        candidates = [
            it for it in unique_items
            if not _is_registered(it, registered_keys)
        ]

        # Apply max_candidates cap
        max_cands = int((sweep.get("output") or {}).get("max_candidates", 200))
        candidates = candidates[:max_cands]

        # Save to log
        _SWEEP_CANDS.parent.mkdir(parents=True, exist_ok=True)
        _SWEEP_CANDS.write_text(
            json.dumps({
                "sweep_date": _now_iso(),
                "total_fetched": len(raw_items),
                "total_unique": len(unique_items),
                "total_new":    len(candidates),
                "candidates":   candidates,
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        _log.info(
            "sweep complete: fetched=%d unique=%d new=%d",
            len(raw_items), len(unique_items), len(candidates),
        )
    except Exception as exc:  # noqa: BLE001
        _log.error("sweep background task failed: %s", exc)
        _SWEEP_CANDS.parent.mkdir(parents=True, exist_ok=True)
        _SWEEP_CANDS.write_text(
            json.dumps({"sweep_date": _now_iso(), "error": str(exc), "candidates": []}),
            encoding="utf-8",
        )


def _normalize_title(t: str) -> str:
    return re.sub(r"\W+", " ", (t or "").lower()).strip()[:120]


def _registered_paper_keys() -> set[str]:
    keys: set[str] = set()
    if not _LIT_DOCS.exists():
        return keys
    for f in _LIT_DOCS.glob("*.json"):
        try:
            d = json.loads(f.read_text("utf-8"))
            if d.get("detected_title"):
                keys.add(_normalize_title(d["detected_title"]))
            if d.get("detected_doi"):
                keys.add(str(d["detected_doi"]).lower().strip())
        except Exception:
            pass
    return keys


def _is_registered(item: dict[str, Any], registered_keys: set[str]) -> bool:
    title_key = _normalize_title(item.get("title", ""))
    doi_key   = str(item.get("doi", "") or "").lower().strip()
    return bool(
        (title_key and title_key in registered_keys)
        or (doi_key and doi_key in registered_keys)
    )


# ── Sweep: get candidates ─────────────────────────────────────────────────────

@router.get("/sweep/candidates")
async def get_sweep_candidates() -> dict[str, Any]:
    """Return the latest sweep candidate list."""
    if not _SWEEP_CANDS.exists():
        return {"candidates": [], "total_new": 0, "sweep_date": None}
    try:
        return json.loads(_SWEEP_CANDS.read_text("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not read candidates: {exc}") from exc


# ── Sweep: intake a candidate ─────────────────────────────────────────────────

class IntakeCandidateBody(BaseModel):
    url: str = ""
    pdf_url: str = ""
    title: str = ""
    doi: str = ""
    authors: list[str] = []
    year: int | None = None
    source: str = ""


@router.post("/sweep/intake")
async def intake_sweep_candidate(
    body: IntakeCandidateBody,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Download a sweep candidate and queue it for intake."""
    target_url = body.pdf_url or body.url
    if not target_url:
        raise HTTPException(status_code=400, detail="url or pdf_url required")

    # Generate filename from title or URL
    if body.title:
        fname = re.sub(r"[^A-Za-z0-9_\-]", "_", body.title[:60]) + ".pdf"
    else:
        parsed = urllib.parse.urlparse(target_url)
        fname  = Path(parsed.path).name or "paper.pdf"
        if not fname.lower().endswith(".pdf"):
            fname += ".pdf"
    fname = re.sub(r"_+", "_", fname).strip("_")

    _RAW_UPLOADS.mkdir(parents=True, exist_ok=True)
    dest = _RAW_UPLOADS / fname

    # If the target doesn't look like a direct PDF, just register the URL
    if not (target_url.endswith(".pdf") or "pdf" in target_url.lower()):
        # Write a placeholder JSON stub the user can replace with a manual upload
        stub = {
            "source_url": target_url,
            "title": body.title,
            "doi": body.doi,
            "authors": body.authors,
            "year": body.year,
            "note": "Non-PDF URL — please upload the PDF manually to raw/user_uploads/",
        }
        stub_path = _EVIDENCE_BASE / "logs" / "pending_imports.jsonl"
        stub_path.parent.mkdir(parents=True, exist_ok=True)
        with open(stub_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(stub, ensure_ascii=False) + "\n")
        return {
            "status": "pending_manual",
            "message": "URL is not a direct PDF. Logged to logs/pending_imports.jsonl — upload manually.",
            "url": target_url,
        }

    # C-06: same SSRF guard + size cap as /import-url.
    _assert_fetchable_url(target_url)
    try:
        content = _fetch_url_capped(target_url)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Download failed: {exc}") from exc
    dest.write_bytes(content)

    background_tasks.add_task(_run_intake_on_file, str(dest))
    return {
        "status": "downloaded",
        "filename": fname,
        "size_bytes": len(content),
        "message": "Downloaded and intake queued.",
    }
