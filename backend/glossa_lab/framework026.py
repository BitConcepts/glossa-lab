"""Spec 026 framework machinery: claim-register integrity + freeze/replay.

Implements the two mechanical checks the RCPH framework requires
that the installed ``aee`` package (1.0.4) does not provide:

1. **Forbidden-assumption inheritance** — a claim must not inherit,
   through its ``depends_on`` ancestry, an assumption it declares
   forbidden (its own ``metadata.forbidden_assumptions`` list).
   Dependency cycles and missing dependencies are delegated to
   :class:`glossa_lab.aee_core.ClaimGraph`, which already detects
   them; this module surfaces all three as one integrity report.

2. **Canonical freeze records** — a freeze is a digest over the
   canonical JSON of an experiment definition plus the sha256 of
   every named source file plus a small environment block.
   ``verify_freeze`` recomputes and reports any drift: a changed
   definition, a changed source, or a changed digest. A freeze is
   never regenerated over an old run; a changed gate is a new
   version and a new freeze (Spec 026 §4.7).

Assumption identifiers are plain strings (convention ``ASM-...``)
carried in ``Claim.assumptions``; forbidden identifiers live in
``Claim.metadata['forbidden_assumptions']``. Matching is exact
after whitespace normalization — renamed-equivalent assumptions
remain a human review obligation, as in the RCPH manual.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any, Iterable

from glossa_lab.aee_core import Claim, ClaimGraph


def _norm(value: str) -> str:
    return " ".join(str(value).split())


def _ancestors(graph: ClaimGraph, claim_id: str) -> set[str]:
    """All transitive depends_on ancestors of *claim_id* (excluding itself)."""
    seen: set[str] = set()
    stack = [c.id for c in graph.dependencies(claim_id)]
    while stack:
        cur = stack.pop()
        if cur in seen or cur == claim_id:
            continue
        seen.add(cur)
        stack.extend(c.id for c in graph.dependencies(cur))
    return seen


def check_dependency_integrity(claims: Iterable[Claim]) -> dict[str, Any]:
    """Return an integrity report for a claim register.

    Keys: ``cycles`` (list of cycles), ``missing_dependencies``
    (sorted list), ``forbidden_inheritance`` (list of
    ``{claim_id, forbidden, inherited_from}`` records), ``ok``
    (True only when all three are empty).
    """
    claim_list = list(claims)
    graph = ClaimGraph()
    for claim in claim_list:
        graph.add(claim)
    by_id = {c.id: c for c in claim_list}

    cycles = graph.cycles()
    missing = sorted(
        {dep for deps in graph.missing_dependencies().values() for dep in deps}
    )

    forbidden_hits: list[dict[str, str]] = []
    for claim in claim_list:
        forbidden = {
            _norm(x) for x in (claim.metadata or {}).get("forbidden_assumptions", [])
        }
        if not forbidden:
            continue
        for anc_id in sorted(_ancestors(graph, claim.id)):
            anc = by_id.get(anc_id)
            if anc is None:
                continue
            inherited = {_norm(a) for a in (anc.assumptions or [])}
            for hit in sorted(forbidden & inherited):
                forbidden_hits.append(
                    {
                        "claim_id": claim.id,
                        "forbidden": hit,
                        "inherited_from": anc_id,
                    }
                )

    return {
        "cycles": cycles,
        "missing_dependencies": missing,
        "forbidden_inheritance": forbidden_hits,
        "ok": not cycles and not missing and not forbidden_hits,
    }


def _canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def build_freeze(
    definition: dict[str, Any],
    root: str | Path,
    source_paths: Iterable[str],
) -> dict[str, Any]:
    """Build a canonical freeze record for *definition*.

    *source_paths* are explicit, unique paths relative to *root*;
    every one must exist inside *root*. The returned record's
    ``digest`` covers the canonical payload (definition + source
    hashes + environment), so changing any covered byte changes
    the digest.
    """
    base = Path(root).resolve()
    sources: dict[str, str] = {}
    for rel in source_paths:
        rel_str = str(rel)
        if rel_str in sources:
            raise ValueError(f"duplicate source path in freeze: {rel_str}")
        target = (base / rel_str).resolve()
        if base not in target.parents and target != base:
            raise ValueError(f"freeze source escapes root: {rel_str}")
        if not target.is_file():
            raise FileNotFoundError(f"freeze source not found: {rel_str}")
        sources[rel_str] = _sha256_file(target)

    try:
        import importlib.metadata

        aee_version = importlib.metadata.version("applied-epistemic-engineering")
    except Exception:  # pragma: no cover - metadata edge cases
        aee_version = "unknown"

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "definition": definition,
        "sources": sources,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.system(),
            "aee": aee_version,
        },
    }
    record = dict(payload)
    record["digest"] = _sha256_bytes(_canonical(payload))
    return record


def verify_freeze(record: dict[str, Any], root: str | Path) -> list[str]:
    """Verify a freeze record against the current tree.

    Returns a list of human-readable errors; empty means the
    freeze replays exactly (definition digest matches and every
    source file's current bytes match the frozen hash).
    """
    errors: list[str] = []
    payload = {k: v for k, v in record.items() if k != "digest"}
    expected = _sha256_bytes(_canonical(payload))
    if record.get("digest") != expected:
        errors.append("freeze digest mismatch: record payload was altered")

    base = Path(root).resolve()
    for rel, frozen_hash in sorted((record.get("sources") or {}).items()):
        target = (base / rel).resolve()
        if not target.is_file():
            errors.append(f"frozen source missing: {rel}")
            continue
        if _sha256_file(target) != frozen_hash:
            errors.append(f"frozen source changed: {rel}")
    return errors
