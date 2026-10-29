"""Spec-study register API (Leg B hardening, 2026-10-29).

Mounted at ``/api/v1/spec-studies``.

Why this exists
---------------
The program record — every spec-kit study execution under ``specs/``
(Specs 001-081: frozen spec, outcome record, verdict) — had NO API
surface at all. The UI's "Studies" are canvas graphs (``/studies``);
no endpoint enumerated the spec register, so no UI surface could show
a study's verdict or status, and every spec outcome was invisible to
the frontend (Leg B reconciliation, 2026-10-29, delta D0).

Endpoints
---------
GET  /              Register: one entry per ``specs/NNN-slug/`` directory
GET  /{spec_id}     One register entry (spec_id = zero-padded number, e.g. "052")

Each entry carries: spec_id, slug, directory, title (spec.md H1),
has_spec, has_outcome, outcome_headline (the outcome record's own
headline line, verbatim-truncated — never a paraphrase), and
restricted (see below).

Restricted entries
------------------
Spec 072 is restricted: this module NEVER opens any file inside its
directory. Its entry is built from the directory name only (public
naming) and carries ``restricted: true`` with null title/headline.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/spec-studies", tags=["spec-studies"])

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SPECS_DIR = _REPO_ROOT / "specs"

# Spec numbers whose directory contents must never be read by this API.
RESTRICTED_SPEC_IDS = frozenset({"072"})

_DIR_RE = re.compile(r"^(\d{3})-(.+)$")
_HEADLINE_MAX = 300


def _specs_dir() -> Path:
    return _SPECS_DIR


def _title_from_spec_md(spec_dir: Path) -> str | None:
    spec_md = spec_dir / "spec.md"
    if not spec_md.exists():
        return None
    try:
        for line in spec_md.read_text("utf-8", errors="ignore").splitlines():
            if line.startswith("# "):
                return line[2:].strip() or None
            if line.strip():
                # H1 is expected at the top; do not scan the whole file.
                if line.startswith("#"):
                    continue
                break
    except OSError:
        return None
    return None


def _outcome_headline(spec_dir: Path) -> str | None:
    """The outcome record's own headline, verbatim.

    Outcome records open with an H1 title followed by a blockquote
    headline (``> ## EXECUTED — <date> — <verdict>``). Return the first
    blockquote line, stripped of markdown, truncated at _HEADLINE_MAX.
    Fall back to an explicit ``Outcome:`` / ``## Outcome`` line.
    Returns None when no headline shape is found — never invent one.
    """
    outcome_md = spec_dir / "outcome.md"
    if not outcome_md.exists():
        return None
    try:
        lines = outcome_md.read_text("utf-8", errors="ignore").splitlines()
    except OSError:
        return None
    def _clean(s: str) -> str:
        return s.lstrip(">").strip().strip("*").strip()

    # Pass 1: an explicit heading-style "Outcome: X" line near the top
    # (markdown heading or bold lead — never a prose sentence).
    for line in lines[:200]:
        raw = line.strip()
        if not (raw.startswith("#") or raw.startswith("**Outcome")):
            continue
        s = _clean(re.sub(r"^#+\s*", "", _clean(raw)))
        m = re.match(r"Outcome(?:\s+word)?[:\s]+(.+)", s, re.IGNORECASE)
        if m:
            return m.group(1).strip().strip("*").strip()[:_HEADLINE_MAX]
    # Pass 2: the outcome record's H1, which in most records carries the
    # execution + verdict summary in its own title.
    for line in lines[:10]:
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()[:_HEADLINE_MAX]
    # Pass 3: the opening blockquote headline, joining its wrapped lines.
    quote: list[str] = []
    for line in lines[:80]:
        s = line.strip()
        if s.startswith(">"):
            text = re.sub(r"^#+\s*", "", _clean(s)).strip()
            if text:
                quote.append(text)
            if len(quote) >= 8:
                break
        elif quote:
            break
    if quote:
        return " ".join(quote)[:_HEADLINE_MAX]
    return None


def _entry(spec_dir: Path) -> dict[str, Any] | None:
    m = _DIR_RE.match(spec_dir.name)
    if not m:
        return None
    spec_id, slug = m.group(1), m.group(2)
    if spec_id in RESTRICTED_SPEC_IDS:
        return {
            "spec_id": spec_id,
            "slug": slug,
            "directory": f"specs/{spec_dir.name}",
            "title": None,
            "has_spec": True,
            "has_outcome": None,
            "outcome_headline": None,
            "restricted": True,
        }
    return {
        "spec_id": spec_id,
        "slug": slug,
        "directory": f"specs/{spec_dir.name}",
        "title": _title_from_spec_md(spec_dir),
        "has_spec": (spec_dir / "spec.md").exists(),
        "has_outcome": (spec_dir / "outcome.md").exists(),
        "outcome_headline": _outcome_headline(spec_dir),
        "restricted": False,
    }


def list_spec_studies(specs_dir: Path | None = None) -> list[dict[str, Any]]:
    base = specs_dir if specs_dir is not None else _specs_dir()
    if not base.exists():
        return []
    entries = [
        e
        for d in sorted(base.iterdir())
        if d.is_dir() and (e := _entry(d)) is not None
    ]
    # Duplicate spec numbers exist (two 021s, two 025s, two 026s):
    # keep register order stable by (spec_id, slug).
    entries.sort(key=lambda e: (e["spec_id"], e["slug"]))
    return entries


@router.get("")
async def get_spec_studies() -> dict[str, Any]:
    entries = list_spec_studies()
    return {
        "studies": entries,
        "total": len(entries),
        "with_outcome": sum(1 for e in entries if e["has_outcome"]),
        "source": "specs/ register (repo tree of the serving backend)",
    }


@router.get("/{spec_id}")
async def get_spec_study(spec_id: str) -> dict[str, Any]:
    wanted = spec_id.zfill(3)
    matches = [e for e in list_spec_studies() if e["spec_id"] == wanted]
    if not matches:
        raise HTTPException(status_code=404, detail=f"no spec study {spec_id!r} in the register")
    if len(matches) == 1:
        return matches[0]
    # Ambiguous number (duplicate spec numbers in the register):
    # return all matches rather than silently picking one.
    return {"spec_id": wanted, "ambiguous": True, "matches": matches}
