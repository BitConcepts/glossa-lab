"""Researcher dashboard API — Spec 095 T403.

The read model behind the researcher dashboard (the Stage 4
wireframes, approved by the owner by name on 2026-11-18). Every
figure this module serves is read from a record of the program at
request time — the claims ledger, the generated program map, the
anchors register, the corpus identity registry, the canonical
corpus export, the run index, the hypothesis model files, the
identifiability application record, and the gap register. Nothing
here computes a new standing, promotes anything, or writes to the
ledger or the anchors register. The one write path is the
contribution endpoint, which appends a candidate to the research
loop's staging store through the verified-write library the
anchor path already uses, carrying the Spec 094 candidate gate
fields (falsifier, evidence_ref) on the candidate record itself.

Refusals enforced here, per the approved wireframes:

- A contribution without a falsifier is refused; the form's
  requirement is the pipeline's requirement, not a UI nicety.
- A contribution cannot carry an approver. Approval is a separate
  named-human act recorded later through the staging machinery;
  a submission that names its own approver is refused.
- An automated identity cannot submit a contribution.
- An evidence reference that does not resolve to a record (a
  ledger claim, an anchors-register sign, or a run of record) is
  refused, naming the reference.
- A corpus whose identity does not verify is listed unavailable
  with the reason, and is never served as explorable data.
- A re-run executes only after the canonical corpus verifies
  against its pin of record, evaluates against the current
  stores read-only, and writes its record only to a scratch
  directory. A reproduction outcome is never written into a
  standing.
- The hypothesis surface holds no translation of any inscription:
  the program holds none, and the response says so where a
  translation would go.
"""
from __future__ import annotations

import hashlib
import json
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import JSONResponse

_REPO = Path(__file__).resolve().parents[3]

_LEDGER = _REPO / "glossa-indus" / "ledger" / "claims.jsonl"
_MAP = _REPO / "glossa-indus" / "map" / "map-data.json"
_ANCHORS = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_CORPUS_EXPORT = _REPO / "glossa-corpus" / "indus" / "exports" / "indus_research.jsonl"
_CORPUS_OPEN = _REPO / "glossa-corpus" / "indus" / "exports" / "indus_open.jsonl"
_RUN_INDEX = _REPO / "glossa-indus" / "ledger" / "runs" / "run-index.jsonl"
_RUNS_DIR = _REPO / "glossa-indus" / "ledger" / "runs"
_IDENTIFIABILITY_RECORD = (
    _REPO / "specs" / "095-red-team-remediation" / "records"
    / "t303-identifiability-application-2026-11-16.md"
)
_GAP_REGISTER = _REPO / "glossa-indus" / "map" / "gap-register.md"
_HYPOTHESES_DIR = _REPO / "glossa-indus" / "hypotheses" / "models"
_SPECS_DIR = _REPO / "specs"
# The staging store path is the research loop's own derivation
# (_REPO / "outputs" / "anchor_staging.json" in api/research_loop.py);
# it is restated here so tests can point this module at a scratch
# store without touching the loop module's state.
_STAGING_PATH = _REPO / "outputs" / "anchor_staging.json"
_ARCHIVE_PATH = _REPO / "outputs" / "anchor_staging_archive.json"

CONTRIBUTION_ORIGIN = "researcher-dashboard"

router = APIRouter(prefix="/api/v1/researcher-dashboard", tags=["researcher-dashboard"])

# ── Cached record loaders (keyed by file mtime) ─────────────────────────────

_cache: dict[str, tuple[float, Any]] = {}


def _load_json(path: Path) -> Any:
    key = f"json:{path}"
    mtime = path.stat().st_mtime
    hit = _cache.get(key)
    if hit and hit[0] == mtime:
        return hit[1]
    data = json.loads(path.read_text(encoding="utf-8"))
    _cache[key] = (mtime, data)
    return data


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    key = f"jsonl:{path}"
    mtime = path.stat().st_mtime
    hit = _cache.get(key)
    if hit and hit[0] == mtime:
        return hit[1]
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    _cache[key] = (mtime, rows)
    return rows


def _missing(path: Path) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=f"a record this surface reads is absent: {path.relative_to(_REPO)}",
    )


def _ledger_rows() -> list[dict[str, Any]]:
    if not _LEDGER.exists():
        raise _missing(_LEDGER)
    return _load_jsonl(_LEDGER)


def _map_data() -> dict[str, Any]:
    if not _MAP.exists():
        raise _missing(_MAP)
    return _load_json(_MAP)


def _anchors() -> dict[str, Any]:
    if not _ANCHORS.exists():
        raise _missing(_ANCHORS)
    return _load_json(_ANCHORS)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _census() -> dict[str, Any]:
    rows = _ledger_rows()
    claims = [r for r in rows if r.get("kind") == "claim"]
    anchors = _anchors()
    by_conf = anchors.get("by_confidence") or {}
    studies = sorted(
        d.name for d in _SPECS_DIR.iterdir() if d.is_dir() and d.name[:3].isdigit()
    )
    return {
        "claims": len(claims),
        "ledger_lines": len(rows),
        "studies": len(studies),
        "study_ids": studies,
        "anchors_total": anchors.get("total"),
        "anchors_by_confidence": by_conf,
        "anchors_strict": sum(
            1 for a in (anchors.get("anchors") or {}).values()
            if a.get("validation_status") == "strict_sa_independent"
        ),
        "sources": {
            "claims": "glossa-indus/ledger/claims.jsonl (kind = claim rows)",
            "ledger_lines": "glossa-indus/ledger/claims.jsonl (all rows)",
            "studies": "specs/ study directories of the program",
            "anchors": "backend/reports/INDUS_FINAL_ANCHORS.json",
        },
    }


def _map_stale() -> dict[str, Any]:
    """The map artifact's freshness against the ledger it was generated from."""
    data = _map_data()
    gen = data.get("generated_from") or {}
    ledger_pin = None
    if isinstance(gen, dict):
        ledger_pin = (gen.get("ledger") or {}).get("sha256") or gen.get("ledger_sha256")
    current = _sha256(_LEDGER) if _LEDGER.exists() else None
    return {
        "map_as_of": (data.get("header") or {}).get("as_of"),
        "map_generated_from": gen,
        "ledger_sha256_now": current,
        "stale": bool(ledger_pin and current and ledger_pin != current),
    }


# ── Identifiability application (Spec 095 T303 record) ──────────────────────

_HEADING = re.compile(
    r"^## (M\d+) — reading (.+?) \((HIGH|MEDIUM|LOW); n = (\d+)[^)]*\)\s*$", re.M
)


def _identifiability() -> list[dict[str, Any]]:
    if not _IDENTIFIABILITY_RECORD.exists():
        raise _missing(_IDENTIFIABILITY_RECORD)
    text = _IDENTIFIABILITY_RECORD.read_text(encoding="utf-8")
    out: list[dict[str, Any]] = []
    matches = list(_HEADING.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[m.start():end]
        outcome = ""
        om = re.search(r"^Outcome:\s*(.+?)(?:\n\s*\n|\Z)", section, re.M | re.S)
        if om:
            outcome = re.sub(r"\s+", " ", om.group(1)).strip()
        out.append({
            "sign": m.group(1),
            "reading": m.group(2),
            "confidence": m.group(3),
            "n": int(m.group(4)) if m.group(4) else None,
            "identifiable": "NOT IDENTIFIABLE" not in outcome,
            "outcome": outcome,
            "record": str(_IDENTIFIABILITY_RECORD.relative_to(_REPO)),
        })
    return out


# ── Gap register headline list ───────────────────────────────────────────────

def _gap_headlines() -> list[dict[str, Any]]:
    if not _GAP_REGISTER.exists():
        raise _missing(_GAP_REGISTER)
    text = _GAP_REGISTER.read_text(encoding="utf-8")
    start = text.find("## The headline list")
    if start < 0:
        return []
    rest = text[start:]
    nxt = rest.find("\n## ", 10)
    section = rest if nxt < 0 else rest[:nxt]
    items: list[dict[str, Any]] = []
    current: list[str] = []
    for line in section.splitlines()[1:]:
        if re.match(r"^\d+\.\s", line):
            if current:
                items.append(current)
            current = [line]
        elif current and (line.startswith("   ") or line.startswith("\t")):
            current.append(line)
    if current:
        items.append(current)
    out = []
    for lines in items:
        joined = re.sub(r"\s+", " ", " ".join(lines)).strip()
        joined = re.sub(r"^\d+\.\s*", "", joined)
        gid = re.search(r"GR-088-\d+", joined)
        out.append({
            "id": gid.group(0) if gid else None,
            "text": joined,
            "owner": None,
            "owner_note": "the register names no owner for this item",
        })
    return out


# ── Home ─────────────────────────────────────────────────────────────────────

@router.get("/home")
async def dashboard_home() -> dict[str, Any]:
    data = _map_data()
    header = data.get("header") or {}
    census = _census()
    falsifier_census = ((data.get("system") or {}).get("falsifier_census")) or {}
    return {
        "as_of": header.get("as_of"),
        "census": census,
        "claims_by_status": header.get("claims_by_status") or {},
        "falsifier_census": falsifier_census,
        "pending_validations": header.get("pending_validations"),
        "identifiability": _identifiability(),
        "identifiability_record": str(_IDENTIFIABILITY_RECORD.relative_to(_REPO)),
        "does_not_claim": [
            "The Indus script is not deciphered, and nothing on this "
            "dashboard says or implies that it is.",
            "No reading is shown stronger than its recorded standing; "
            "the strongest readings in the record are stated with "
            "their identifiability outcome, not above it.",
            "Every count here is the gate-verified census of record, "
            "read from the ledger, the anchors register, and the "
            "generated program map. No other numbers are shown.",
        ],
        "recent_adjudications": (header.get("nearest_dated_items") or [])[:6],
        "recent_adjudications_basis": (
            "dated study outcomes recorded against claims in the "
            "generated program map (header.nearest_dated_items) — "
            "acts and outcomes, not summaries"
        ),
        "freshness": _map_stale(),
    }


# ── Program status ───────────────────────────────────────────────────────────

@router.get("/program-status")
async def dashboard_program_status() -> dict[str, Any]:
    census = _census()
    data = _map_data()
    header = data.get("header") or {}
    records: list[dict[str, Any]] = []
    for spec_dir in sorted(_SPECS_DIR.iterdir()):
        rec_dir = spec_dir / "records"
        if not rec_dir.is_dir():
            continue
        for f in rec_dir.iterdir():
            if f.suffix not in (".md", ".json"):
                continue
            dm = re.search(r"(20\d{2}-\d{2}-\d{2})", f.name)
            records.append({
                "spec": spec_dir.name,
                "file": f.name,
                "path": str(f.relative_to(_REPO)),
                "date": dm.group(1) if dm else None,
            })
    records.sort(key=lambda r: (r["date"] or "", r["path"]), reverse=True)
    return {
        "census": census,
        "claims_by_status": header.get("claims_by_status") or {},
        "freshness": _map_stale(),
        "blocked_items": _gap_headlines(),
        "blocked_items_source": str(_GAP_REGISTER.relative_to(_REPO)),
        "recent_landing_records": records[:10],
        "recent_landing_records_basis": (
            "the landing records themselves, newest first; each "
            "record carries its own wrapper and payload verdicts — "
            "this surface lists the records, it does not restate "
            "their verdicts as its own"
        ),
    }


# ── Corpora + inscription explorer ───────────────────────────────────────────

_corpus_verify_cache: dict[str, dict[str, Any]] = {}


def _corpus_entries() -> list[dict[str, Any]]:
    from glossa_lab.data.corpus_identity import (
        CISI_KEY,
        HOLDAT_KEY,
        ICIT_KEY,
        M77_KEY,
        MAYIG_KEY,
        SITE_KEY,
        V1_KEY,
        V3_KEY,
        CorpusIdentityError,
        get_identity,
        verify_corpus_identity,
    )

    keys = [V3_KEY, V1_KEY, ICIT_KEY, CISI_KEY, MAYIG_KEY, M77_KEY, SITE_KEY, HOLDAT_KEY]
    entries: list[dict[str, Any]] = []
    for key in keys:
        if key in _corpus_verify_cache:
            entries.append(_corpus_verify_cache[key])
            continue
        ident = get_identity(key)
        entry: dict[str, Any] = {
            "key": key,
            "name": ident.name,
            "version": ident.version,
            "source": ident.source,
            "licensing": ident.licensing,
            "orientation_basis": ident.orientation_basis,
            "identity_paths": list(ident.paths),
            "explorable": False,
        }
        try:
            rec = verify_corpus_identity(key, _REPO)
            entry["identity_status"] = "verified"
            entry["verified_path"] = rec["path"]
            entry["verified_sha256"] = rec["sha256"]
            entry["census"] = rec["census"]
            entry["unavailable_reason"] = None
        except CorpusIdentityError as exc:
            entry["identity_status"] = "unavailable"
            entry["verified_path"] = None
            entry["verified_sha256"] = None
            entry["census"] = None
            entry["unavailable_reason"] = str(exc)
        _corpus_verify_cache[key] = entry
        entries.append(entry)
    # The explorable corpus: the canonical export, verified against
    # the pin the settling runs of record carry for it.
    pin = None
    for run in (_map_data().get("settling") or {}).get("runs") or []:
        pin = ((run.get("pins") or {}).get("corpus_snapshot") or {}).get("sha256")
        if pin:
            break
    canonical: dict[str, Any] = {
        "key": "indus_canonical_export",
        "name": "Canonical Indus export (objectized from the CISI compilation)",
        "version": "canonical export of record",
        "source": "glossa-corpus/indus/exports/indus_research.jsonl",
        "licensing": "per-record rights_status, shown on each record",
        "orientation_basis": (
            "the mayig-cisi layer's orientation basis of record "
            "applies to the objectized export"
        ),
        "identity_paths": ["glossa-corpus/indus/exports/indus_research.jsonl"],
        "explorable": False,
    }
    if _CORPUS_EXPORT.exists() and pin:
        observed = _sha256(_CORPUS_EXPORT)
        canonical["verified_sha256"] = observed
        canonical["pin_of_record"] = pin
        if observed == pin:
            canonical["identity_status"] = "verified"
            canonical["unavailable_reason"] = None
            canonical["explorable"] = True
        else:
            canonical["identity_status"] = "unavailable"
            canonical["unavailable_reason"] = (
                f"the canonical export hashes to {observed}, which "
                f"differs from its pin of record {pin}"
            )
    else:
        canonical["identity_status"] = "unavailable"
        canonical["unavailable_reason"] = (
            "the canonical export or its pin of record is absent"
        )
    return [canonical, *entries]


@router.get("/corpora")
async def dashboard_corpora() -> dict[str, Any]:
    return {"corpora": _corpus_entries()}


def _corpus_records() -> list[dict[str, Any]]:
    if not _CORPUS_EXPORT.exists():
        raise _missing(_CORPUS_EXPORT)
    return _load_jsonl(_CORPUS_EXPORT)


def _open_export_index() -> dict[str, dict[str, Any]]:
    if not _CORPUS_OPEN.exists():
        return {}
    key = f"openidx:{_CORPUS_OPEN}"
    mtime = _CORPUS_OPEN.stat().st_mtime
    hit = _cache.get(key)
    if hit and hit[0] == mtime:
        return hit[1]
    idx = {r["glossa_id"]: r for r in _load_jsonl(_CORPUS_OPEN) if r.get("glossa_id")}
    _cache[key] = (mtime, idx)
    return idx


def _sign_ref_forms(sign: str) -> set[str]:
    """The forms under which one sign appears across the records.

    The anchors register and the corpus grapheme identities name a
    sign M072; ledger sign_refs name the same sign mahadevan:72.
    A lookup by either form must find the other, or the one
    claim-to-sign linkage the program holds would be invisible.
    """
    forms = {sign}
    m = re.fullmatch(r"M0*(\d+)", sign)
    if m:
        forms.add(f"mahadevan:{int(m.group(1))}")
    m = re.fullmatch(r"mahadevan:0*(\d+)", sign)
    if m:
        forms.add(f"M{int(m.group(1)):03d}")
    return forms


def _tokens(record: dict[str, Any]) -> list[str]:
    code = record.get("text_code_diplomatic") or ""
    inner = code.strip().strip("+")
    return [t for t in inner.split("-") if t] if inner else []


def _inscription_summary(r: dict[str, Any]) -> dict[str, Any]:
    return {
        "glossa_id": r.get("glossa_id"),
        "artifact_type": r.get("artifact_type"),
        "site_name": r.get("site_name"),
        "sign_instance_count": r.get("sign_instance_count"),
        "text_code_diplomatic": r.get("text_code_diplomatic"),
        "rights_status": r.get("rights_status"),
        "source_system": r.get("source_system"),
    }


@router.get("/inscriptions")
async def dashboard_inscriptions(
    corpus: str = Query("indus_canonical_export"),
    site: str | None = Query(None),
    object_class: str | None = Query(None),
    sign: str | None = Query(None),
    length_min: int | None = Query(None),
    length_max: int | None = Query(None),
    q: str | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> dict[str, Any]:
    entries = {e["key"]: e for e in _corpus_entries()}
    entry = entries.get(corpus)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"unknown corpus: {corpus}")
    if not entry["explorable"]:
        return {
            "corpus": corpus,
            "total": 0,
            "items": [],
            "facets": {"sites": {}, "object_classes": {}},
            "unavailable_reason": entry["unavailable_reason"]
            or "this corpus carries no inscription-level export in the record",
        }
    records = _corpus_records()
    sites: dict[str, int] = {}
    classes: dict[str, int] = {}
    for r in records:
        if r.get("site_name"):
            sites[r["site_name"]] = sites.get(r["site_name"], 0) + 1
        if r.get("artifact_type"):
            classes[r["artifact_type"]] = classes.get(r["artifact_type"], 0) + 1
    out = []
    for r in records:
        if site and r.get("site_name") != site:
            continue
        if object_class and r.get("artifact_type") != object_class:
            continue
        if sign and sign not in _tokens(r):
            continue
        n = r.get("sign_instance_count") or 0
        if length_min is not None and n < length_min:
            continue
        if length_max is not None and n > length_max:
            continue
        if q and q.lower() not in (r.get("glossa_id") or "").lower():
            continue
        out.append(r)
    return {
        "corpus": corpus,
        "total": len(out),
        "items": [_inscription_summary(r) for r in out[offset:offset + limit]],
        "facets": {"sites": sites, "object_classes": classes},
        "unavailable_reason": None,
    }


@router.get("/inscriptions/{glossa_id}")
async def dashboard_inscription(glossa_id: str) -> dict[str, Any]:
    records = {r.get("glossa_id"): r for r in _corpus_records()}
    r = records.get(glossa_id)
    if r is None:
        raise HTTPException(status_code=404, detail=f"no inscription of record: {glossa_id}")
    anchors = (_anchors().get("anchors") or {})
    tokens = _tokens(r)
    graphemes = r.get("canonical_grapheme_ids") or []
    positions = []
    for i, token in enumerate(tokens):
        grapheme = graphemes[i] if i < len(graphemes) else None
        anchor = anchors.get(grapheme) if grapheme else None
        positions.append({
            "position": i,
            "token": token,
            "grapheme": grapheme,
            "anchor_reading": (
                {
                    "sign": grapheme,
                    "reading": anchor.get("reading"),
                    "confidence": anchor.get("confidence"),
                    "validation_status": anchor.get("validation_status"),
                }
                if anchor else None
            ),
        })
    sign_ids = [p["grapheme"] for p in positions if p["grapheme"]]
    ref_forms: set[str] = set()
    for s in sign_ids:
        ref_forms |= _sign_ref_forms(s)
    claims = [
        row for row in _ledger_rows()
        if row.get("kind") == "claim"
        and any(ref in (row.get("sign_refs") or []) for ref in ref_forms)
    ]
    open_rec = _open_export_index().get(glossa_id)
    return {
        "glossa_id": glossa_id,
        "layers": {
            "observation": {
                "glossa_id": r.get("glossa_id"),
                "artifact_type": r.get("artifact_type"),
                "site_name": r.get("site_name"),
                "current_holding": r.get("current_holding"),
                "material": r.get("material"),
                "accession_number": r.get("accession_number"),
                "image_master_uri": r.get("image_master_uri"),
                "rights_status": r.get("rights_status"),
                "source_system": r.get("source_system"),
                "citation": r.get("_citation"),
                "note": (
                    "catalogue identity and context exactly as "
                    "recorded; a field the record leaves empty is "
                    "shown empty, never filled in"
                ),
            },
            "transcription": {
                "sign_id_scheme": r.get("sign_id_scheme"),
                "diplomatic": r.get("text_code_diplomatic"),
                "normalized": r.get("text_code_diplomatic_normalized"),
                "open_export": (
                    {
                        "diplomatic": open_rec.get("text_code_diplomatic"),
                        "source_system": open_rec.get("source_system"),
                    }
                    if open_rec else None
                ),
                "positions": positions,
                "crosswalk_coverage": r.get("crosswalk_coverage"),
                "note": (
                    "transcriptions as recorded in each export, "
                    "labelled by their source; no normalization, "
                    "completion, or reordering is applied here"
                ),
            },
            "hypothesis": {
                "readings_for_signs": [
                    p["anchor_reading"] for p in positions if p["anchor_reading"]
                ],
                "absent_reason": (
                    None if any(p["anchor_reading"] for p in positions) else
                    "no sign of this inscription carries a reading in "
                    "the anchors register under a resolved grapheme "
                    "identity on this record"
                ),
                "note": (
                    "sign-level readings from the anchors register, "
                    "shown only where the record's own grapheme "
                    "identity resolves; they are readings of signs, "
                    "not a reading of this inscription"
                ),
            },
            "claim": {
                "claims": [
                    {
                        "id": c.get("id"),
                        "statement": c.get("statement"),
                        "status": c.get("status"),
                        "sign_refs": c.get("sign_refs"),
                    }
                    for c in claims
                ],
                "absent_reason": (
                    None if claims else
                    "no ledger claim records a relation to the signs "
                    "of this inscription (claim-to-sign linkage is a "
                    "named gap of the program)"
                ),
            },
        },
    }


# ── Hypothesis comparison ────────────────────────────────────────────────────

@router.get("/hypotheses")
async def dashboard_hypotheses() -> dict[str, Any]:
    import yaml  # noqa: PLC0415 — the codebase's lazy-yaml pattern

    models: list[dict[str, Any]] = []
    if _HYPOTHESES_DIR.is_dir():
        for f in sorted(_HYPOTHESES_DIR.glob("*.yaml")):
            try:
                d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            except Exception:  # noqa: BLE001
                d = {}
            if isinstance(d, dict):
                models.append(d)
    rows = _ledger_rows()
    nonlinguistic = next(
        (r for r in rows if r.get("id") == "farmer_sproat_witzel_2004_manual_001"),
        None,
    )
    anchors = _anchors()
    ident = {i["sign"]: i for i in _identifiability()}
    readings = []
    for sign, a in sorted((anchors.get("anchors") or {}).items()):
        readings.append({
            "sign": sign,
            "reading": a.get("reading"),
            "confidence": a.get("confidence"),
            "validation_status": a.get("validation_status"),
            "stage": a.get("stage"),
            "identifiability": ident.get(sign),
        })
    return {
        "models": models,
        "nonlinguistic_position": (
            {
                "claim_id": nonlinguistic.get("id"),
                "statement": nonlinguistic.get("statement"),
                "status": nonlinguistic.get("status"),
                "falsifier": nonlinguistic.get("falsifier"),
                "does_not_establish": nonlinguistic.get("does_not_establish"),
                "basis": (
                    "the position is carried in the claims ledger "
                    "in the same form as every other claim"
                ),
            }
            if nonlinguistic else None
        ),
        "translations": {
            "held": 0,
            "statement": (
                "The program holds no translation of any "
                "inscription. Where a translation would go, this "
                "is what stands: no translation exists in the "
                "record, and none is presented."
            ),
        },
        "readings": readings,
        "readings_basis": (
            "the anchors register, with the identifiability "
            "outcomes of the T303 application joined for the six "
            "signs it examined; a reading is never displayed above "
            "the weakest standing it rests on"
        ),
    }


# ── Evidence inspection ──────────────────────────────────────────────────────

def _map_claims() -> dict[str, dict[str, Any]]:
    return _map_data().get("claims") or {}


@router.get("/claims")
async def dashboard_claims(
    standing: str | None = Query(None),
    study: str | None = Query(None),
    sign: str | None = Query(None),
    falsifier: str | None = Query(None),  # "present" | "absent"
    q: str | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> dict[str, Any]:
    claims = _map_claims()
    out = []
    for cid, c in claims.items():
        if standing and c.get("status") != standing:
            continue
        if falsifier == "present" and not c.get("falsifier"):
            continue
        if falsifier == "absent" and c.get("falsifier"):
            continue
        if sign and not (_sign_ref_forms(sign) & set(c.get("sign_refs") or [])):
            continue
        if study:
            cells = ((c.get("matrix_row") or {}).get("cells")) or []
            if not any(
                cell.get("column") == study and cell.get("column_class") == "studies"
                for cell in cells
            ):
                continue
        if q and q.lower() not in (c.get("statement") or "").lower() \
                and q.lower() not in cid.lower():
            continue
        out.append({
            "id": cid,
            "statement": c.get("statement"),
            "status": c.get("status"),
            "stage": c.get("stage"),
            "population": c.get("population"),
            "date": c.get("date"),
            "falsifier_present": bool(c.get("falsifier")),
            "sign_refs": c.get("sign_refs") or [],
        })
    out.sort(key=lambda c: c["id"])
    census = ((_map_data().get("system") or {}).get("falsifier_census")) or {}
    return {
        "total": len(out),
        "items": out[offset:offset + limit],
        "falsifier_census": census,
        "falsifier_gap_note": (
            "claims carrying no falsifier are findable as a class "
            "(falsifier = absent); the gap is shown, not worked "
            "around"
        ),
    }


@router.get("/claims/{claim_id}")
async def dashboard_claim(claim_id: str) -> dict[str, Any]:
    claims = _map_claims()
    map_claim = claims.get(claim_id)
    rows = {r.get("id"): r for r in _ledger_rows() if r.get("kind") == "claim"}
    ledger_row = rows.get(claim_id)
    if map_claim is None and ledger_row is None:
        raise HTTPException(status_code=404, detail=f"no claim of record: {claim_id}")
    from glossa_lab.api.indus_evidence import claim_trail  # noqa: PLC0415

    trail = await claim_trail(claim_id)
    supersedes = (ledger_row or {}).get("supersedes")
    superseded_by = [
        r.get("id") for r in rows.values() if r.get("supersedes") == claim_id
    ]
    return {
        "claim_id": claim_id,
        "statement": (map_claim or ledger_row or {}).get("statement"),
        "falsifier": (map_claim or ledger_row or {}).get("falsifier"),
        "does_not_establish": (map_claim or ledger_row or {}).get("does_not_establish"),
        "status": (map_claim or ledger_row or {}).get("status"),
        "stage": (map_claim or ledger_row or {}).get("stage"),
        "population": (map_claim or ledger_row or {}).get("population"),
        "author": (map_claim or ledger_row or {}).get("author"),
        "sign_refs": (map_claim or ledger_row or {}).get("sign_refs") or [],
        "supersession": {"supersedes": supersedes, "superseded_by": superseded_by},
        "lineage": {
            "source_document": ((map_claim or {}).get("evidence") or {}).get("source_document"),
            "sources": (map_claim or ledger_row or {}).get("sources") or [],
            "evidence_refs": (ledger_row or {}).get("evidence_refs") or [],
            "evidence_column_summary": ((map_claim or {}).get("evidence") or {}).get("column_summary"),
            "sign_records": ((map_claim or {}).get("evidence") or {}).get("sign_records") or [],
            "note": (
                "every evidence item is shown with the lineage the "
                "record carries for it; an item with no lineage is "
                "never displayed as evidence"
            ),
        },
        "matrix_cells": ((map_claim or {}).get("matrix_row") or {}).get("cells") or [],
        "trail": trail,
        "ledger_row": ledger_row,
        "map_claim": map_claim,
    }


@router.get("/claims/{claim_id}/export")
async def dashboard_claim_export(claim_id: str) -> JSONResponse:
    detail = await dashboard_claim(claim_id)
    payload = {
        "claim_id": claim_id,
        "export_kind": "audit trail — the records themselves, not a summary",
        "ledger_row": detail["ledger_row"],
        "map_claim": detail["map_claim"],
        "trail": detail["trail"],
        "lineage": detail["lineage"],
        "matrix_cells": detail["matrix_cells"],
        "supersession": detail["supersession"],
    }
    return JSONResponse(
        content=payload,
        headers={
            "Content-Disposition": f'attachment; filename="claim-audit-trail-{claim_id}.json"'
        },
    )


@router.get("/matrix")
async def dashboard_matrix() -> dict[str, Any]:
    matrix = _map_data().get("matrix") or {}
    coverage = matrix.get("coverage") or {}
    by_class: dict[str, int] = {}
    studies: list[str] = []
    for col in matrix.get("columns") or []:
        cls = col.get("class") or "unknown"
        by_class[cls] = by_class.get(cls, 0) + 1
        if cls == "studies":
            studies.append(col.get("id"))
    return {
        "rows_total": coverage.get("rows_total"),
        "rows_with_cells": coverage.get("rows_with_cells"),
        "empty_rows": len(coverage.get("empty_rows") or []),
        "columns_total": len(matrix.get("columns") or []),
        "columns_by_class": by_class,
        "cells_total": len(matrix.get("cells") or []),
        "study_columns": sorted(s for s in studies if s),
        "drill_down": (
            "pick a claim in the evidence section: its matrix row "
            "and every cell on it are shown on the claim itself"
        ),
    }


# ── Experiment reproduction ──────────────────────────────────────────────────

def _run_entries() -> list[dict[str, Any]]:
    if not _RUN_INDEX.exists():
        raise _missing(_RUN_INDEX)
    return _load_jsonl(_RUN_INDEX)


def _run_summary(e: dict[str, Any]) -> dict[str, Any]:
    key = e.get("key") or {}
    missing = e.get("missing") or []
    return {
        "run_id": e.get("run_id"),
        "record": e.get("record"),
        "act": e.get("act"),
        "candidate": key.get("candidate"),
        "semantics": key.get("semantics"),
        "legacy": bool(e.get("legacy")),
        "missing": missing,
        "reproducible": not missing,
        "not_reproducible_reason": (
            "the execution record is incomplete; the missing "
            "pieces are named, and the result is listed as not "
            "reproducible rather than silently passed over"
            if missing else None
        ),
        "input_pins": key.get("input_pins") or {},
    }


@router.get("/results")
async def dashboard_results() -> dict[str, Any]:
    entries = _run_entries()
    settling = _map_data().get("settling") or {}
    settling_runs = []
    for run in settling.get("runs") or []:
        settling_runs.append({
            "record": run.get("record"),
            "scenario": run.get("scenario"),
            "candidate": run.get("candidate"),
            "semantics": run.get("semantics"),
            "assigned_count": run.get("assigned_count"),
            "assigned_share": run.get("assigned_share"),
            "consistent": run.get("consistent"),
            "conflicts": len(run.get("conflicts") or []),
            "pins": run.get("pins") or {},
        })
    return {
        "label": settling.get("label"),
        "semantics_note": (
            "a settling run establishes what the ledger implies "
            "under its semantics, not what the script says; a "
            "reproduction outcome is compared per quantity and is "
            "never written into a standing"
        ),
        "runs": [_run_summary(e) for e in entries],
        "settling_runs": settling_runs,
    }


@router.get("/results/{run_id:path}")
async def dashboard_result(run_id: str) -> dict[str, Any]:
    entries = _run_entries()
    entry = next(
        (e for e in entries if e.get("run_id") == run_id or e.get("record") == run_id),
        None,
    )
    if entry is None:
        raise HTTPException(status_code=404, detail=f"no run of record: {run_id}")
    record_file = None
    record_name = entry.get("record")
    if record_name:
        path = _RUNS_DIR / record_name
        if path.exists():
            record_file = _load_json(path)
    return {"entry": entry, "summary": _run_summary(entry), "record_file": record_file}


@router.post("/results/{run_id:path}/rerun")
async def dashboard_result_rerun(run_id: str) -> dict[str, Any]:
    """Re-run one settling result of record against scratch only.

    The corpus identity is verified before anything runs (the
    wireframe refusal); the evaluation reads the current stores
    and writes its record only into a scratch directory; the
    comparison is per-quantity via the settling semantics' own
    compare function, never pooled, and the outcome is written
    into no standing.
    """
    from glossa_lab.settling import (  # noqa: PLC0415
        SettlingError,
        compare_runs,
        load_assignment_sets,
        load_state,
        run_record,
    )

    detail = await dashboard_result(run_id)
    entry = detail["entry"]
    original = detail["record_file"]
    if entry.get("missing"):
        raise HTTPException(
            status_code=422,
            detail="the execution record is incomplete (missing: "
                   + ", ".join(entry["missing"])
                   + "); the result is not reproducible and no "
                     "re-run is offered for it",
        )
    if original is None:
        raise HTTPException(
            status_code=422,
            detail="this result has no run record file in the run "
                   "store; there is nothing of record to re-run",
        )
    # Corpus identity before anything runs.
    canonical = next(
        (e for e in _corpus_entries() if e["key"] == "indus_canonical_export"), None
    )
    if not canonical or canonical.get("identity_status") != "verified":
        raise HTTPException(
            status_code=422,
            detail="the canonical corpus does not verify against "
                   "its pin of record; refusing to run against an "
                   "unverified corpus",
        )
    candidate_id = original.get("candidate")
    scope = original.get("scope")
    if not candidate_id or not scope:
        raise HTTPException(
            status_code=422,
            detail="the run record names no candidate or scope; "
                   "there is nothing of record to re-run",
        )
    try:
        sets = load_assignment_sets(_REPO)
        candidate = sets[candidate_id]
        state = load_state(_REPO)
        fresh = run_record(state, candidate, scope, scenario=original.get("scenario"))
    except (SettlingError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=f"the re-run refused: {exc}") from exc
    # Scratch only: the fresh record is written to a scratch
    # directory and nowhere else; the run store is not touched.
    # The write goes through the verified-write library — this
    # module holds no direct write call (the ledger gate's V9
    # writer census classifies it as what it is: a reader of the
    # gated artifacts).
    from glossa_lab.verified_write import write_file_verified  # noqa: PLC0415

    scratch = Path(tempfile.mkdtemp(prefix="glossa-rerun-"))
    write_file_verified(
        scratch / "rerun-record.json",
        json.dumps(fresh, indent=2, ensure_ascii=False),
    )
    comparison: dict[str, Any]
    try:
        comparison = {"status": "compared", "record": compare_runs(fresh, original)}
    except (SettlingError, ValueError) as exc:
        comparison = {
            "status": "comparison refused",
            "reason": str(exc),
            "note": (
                "the settling semantics refuse a comparison whose "
                "pins do not agree; the refusal is the result, and "
                "no pooled or partial comparison is substituted"
            ),
        }
    quantities = {}
    for name, rec in (("recorded", original), ("rerun", fresh)):
        res = rec.get("result") or {}
        quantities[name] = {
            k: res.get(k)
            for k in (
                "assigned_count", "assigned_share", "consistent",
                "conflicts", "scope_signs", "contexts_touched",
                "strict_contexts",
            )
            if k in res
        }
    return {
        "run_id": run_id,
        "corpus_identity": canonical["identity_status"],
        "scratch_record": str(scratch / "rerun-record.json"),
        "quantities": quantities,
        "comparison": comparison,
        "standing_effect": (
            "none — a reproduction outcome is never written into "
            "a standing directly"
        ),
    }


# ── Researcher contribution ──────────────────────────────────────────────────

def _read_staging() -> tuple[list[dict[str, Any]], bool]:
    """Return (records, was_dict_shaped) for the staging store."""
    if not _STAGING_PATH.exists():
        return [], False
    data = json.loads(_STAGING_PATH.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return list(data.get("candidates") or []), True
    return list(data), False


def _contribution_view(rec: dict[str, Any]) -> dict[str, Any]:
    # The view is the candidate record itself (a copy), with the
    # subject sign normalized to one field name. This module never
    # assigns a lifecycle field: creation happens in the pipeline
    # module and transitions in the transition service (Spec 094).
    view = dict(rec)
    view["subject_sign"] = rec.get("subject_sign") or rec.get("sign")
    return view


@router.get("/contributions")
async def dashboard_contributions() -> dict[str, Any]:
    records, _ = _read_staging()
    mine = [r for r in records if r.get("origin") == CONTRIBUTION_ORIGIN]
    archive: list[dict[str, Any]] = []
    if _ARCHIVE_PATH.exists():
        raw = json.loads(_ARCHIVE_PATH.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            archive = [r for r in raw if r.get("origin") == CONTRIBUTION_ORIGIN]
    return {
        "contributions": [_contribution_view(r) for r in [*mine, *archive]],
        "boundaries": {
            "research_assistant": (
                "the Research Assistant is advisory only; nothing "
                "it produces enters the record on its own"
            ),
            "approval": (
                "approval is a named human act, recorded on the "
                "candidate record through the staging machinery; "
                "no approval is automatic and none is implied by "
                "submission"
            ),
            "promotion": (
                "there is no automatic promotion anywhere in this "
                "system, and no submitter can certify their own "
                "candidate"
            ),
        },
    }


@router.post("/contributions")
async def dashboard_contribution_submit(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    from glossa_lab.claim_stage import is_automated_actor  # noqa: PLC0415
    from glossa_lab.verified_write import write_file_verified  # noqa: PLC0415

    if "approver" in payload:
        raise HTTPException(
            status_code=422,
            detail="a submission cannot carry an approver: approval "
                   "is a separate named-human act, recorded on the "
                   "candidate record later through the staging "
                   "machinery (Spec 094)",
        )
    statement = payload.get("statement")
    if not isinstance(statement, str) or not statement.strip():
        raise HTTPException(status_code=422, detail="a candidate requires a statement")
    falsifier = payload.get("falsifier")
    if not isinstance(falsifier, str) or not falsifier.strip():
        raise HTTPException(
            status_code=422,
            detail="the form cannot submit without a falsifier: a "
                   "candidate the record cannot prove wrong is not "
                   "a candidate",
        )
    submitted_by = payload.get("submitted_by")
    if not isinstance(submitted_by, str) or not submitted_by.strip():
        raise HTTPException(
            status_code=422, detail="a candidate requires a named submitter"
        )
    if is_automated_actor(submitted_by):
        raise HTTPException(
            status_code=422,
            detail="an automated identity cannot submit a candidate "
                   "for adjudication",
        )
    refs = payload.get("evidence_refs")
    if not isinstance(refs, list) or not refs or not all(
        isinstance(x, str) and x.strip() for x in refs
    ):
        raise HTTPException(
            status_code=422,
            detail="a candidate requires at least one evidence "
                   "reference picked from the record",
        )
    claim_ids = {r.get("id") for r in _ledger_rows() if r.get("kind") == "claim"}
    anchor_ids = set((_anchors().get("anchors") or {}).keys())
    run_ids = {e.get("run_id") for e in _run_entries()}
    for ref in refs:
        if ref not in claim_ids and ref not in anchor_ids and ref not in run_ids:
            raise HTTPException(
                status_code=422,
                detail=f"evidence reference does not resolve to a "
                       f"record: {ref}",
            )
    subject = payload.get("subject_sign")
    if subject is not None and subject not in anchor_ids:
        raise HTTPException(
            status_code=422,
            detail=f"subject sign is not in the anchors register: {subject}",
        )
    does_not_establish = payload.get("does_not_establish")
    if does_not_establish is not None and not isinstance(does_not_establish, str):
        raise HTTPException(
            status_code=422, detail="does_not_establish must be a statement or absent"
        )
    records, was_dict = _read_staging()
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_existing = sum(1 for r in records if r.get("origin") == CONTRIBUTION_ORIGIN)
    contribution_id = f"RDC-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}-{n_existing + 1:03d}"
    # Candidate CREATION is the pipeline module's act (Spec 094's
    # census pins it there): the record is born at the creation
    # state that module assigns, never transitioned into existence
    # by this surface, and it carries no approver — approval is a
    # later, separate, named-human act on the record.
    from glossa_lab.pipelines.research_loop import (  # noqa: PLC0415
        create_staged_candidate,
    )

    record = create_staged_candidate({
        "contribution_id": contribution_id,
        "origin": CONTRIBUTION_ORIGIN,
        "statement": statement.strip(),
        "falsifier": falsifier.strip(),
        "evidence_ref": refs[0],
        "evidence_refs": refs,
        "does_not_establish": does_not_establish,
        "subject_sign": subject,
        "sign": subject,
        "proposed_reading": None,
        "submitted_by": submitted_by.strip(),
        "submitted_at": now,
        "stage": None,
        "stage_source": "researcher dashboard submission (Spec 095 T403)",
        "stage_as_of": now,
        "stage_history": [
            {
                "from_stage": None,
                "to_stage": "staged",
                "actor": submitted_by.strip(),
                "timestamp": now,
                "reason": (
                    "submitted through the researcher dashboard; "
                    "submission implies no approval, verification, "
                    "or promotion"
                ),
            }
        ],
    })
    records.append(record)
    payload_out: Any = {"candidates": records} if was_dict else records
    write_file_verified(
        _STAGING_PATH, json.dumps(payload_out, indent=2, ensure_ascii=False)
    )
    return _contribution_view(record)
