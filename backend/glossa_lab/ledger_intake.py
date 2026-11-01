"""Ledger intake and validation — Spec 086 Stage 1 (T102/T103).

The claims ledger (``glossa-indus/ledger/claims.jsonl``,
``ledger-schema v1``) is the sole entry point downstream
(Spec 086 Point 1). This module is the only code path that
writes to it:

- **Validation** — every entry is checked against the pinned
  schema, its proposition fingerprint is recomputed under the
  frozen ``spec029-phase-i-v1`` rules (D-B, via
  :mod:`glossa_lab.proposition_fingerprint`), duplicate
  fingerprints are refused naming both records, and
  field-provenance checks require every falsifier and
  does-not-establish line to trace to a source record named in
  the entry (C086-5) and explanation content to name a human
  author (C086-6 / OD-2). New (non-migration) claim entries
  must carry a falsifier (prospective rule, D-086-Q6).
- **Append** — a single verified write: temp file in the
  ledger's directory, fsync, atomic rename, then a read-back
  whose SHA-256 and byte-prefix are checked against what was
  written, so an append can never silently alter an existing
  line (C086-4).
- **Intake routes** (T103) — builders for the four doors:
  extraction intake, bundle import, research-check annotation
  intake, and discovery promotion. Nothing else in the code
  base appends to the ledger.

The migration that built the initial ledger lives in
``tools/ledger/migrate_ledger.py`` and uses the builders and
the bulk writer here.

**Canonical hashing (harmonization adoption, 2026-11-01 —
"Canonicalize before you hash," from the Spec-Kit AEE chat).**
Every hash this tooling records over a source file (ledger
entries' source hashes, migration provenance) is computed by
the ONE shared helper :func:`sha256_file`, which hashes the
file's canonical form — UTF-8 decoded, CRLF normalized to
LF — never its raw bytes. A raw-byte hash is platform-bound:
the same source checked out with CRLF endings would hash
differently and a regeneration gate would report drift on
one platform while passing on the other. Generated artifacts
(this ledger included) are written with pinned LF newlines
and compared byte-exactly. The repo's checkout is also
pinned (``.gitattributes``: ``* text=auto eol=lf``), and the
existing freeze regime's raw-byte pins are a separate,
historical regime — they verify under the attributes regime
and are NOT migrated to canonical hashing.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

from jsonschema import Draft202012Validator

from glossa_lab.proposition_fingerprint import (
    FINGERPRINT_RULES_VERSION,
    DuplicatePropositionError,
    proposition_fingerprint,
)

LEDGER_REL = "glossa-indus/ledger/claims.jsonl"
SCHEMA_REL = "glossa-indus/ledger/ledger-schema.json"
SCHEMA_VERSION = "ledger-schema v1"

#: Claim-entry fields whose text must trace to a source record.
_PROVENANCE_FALSIFIER_KEYS = ("falsification_tests", "falsification_condition")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_bytes(data: bytes) -> str:
    """Raw SHA-256 of in-memory bytes. NOT for source-file
    provenance — use :func:`sha256_file` for anything recorded
    over a file (see the module docstring's canonical-hash
    rule)."""
    return hashlib.sha256(data).hexdigest()


def canonicalize_bytes(data: bytes) -> bytes:
    """The canonical form a recorded hash is taken over:
    UTF-8 decoded, CRLF (and lone CR) normalized to LF,
    re-encoded as UTF-8."""
    text = data.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_sha256_bytes(data: bytes) -> str:
    return sha256_bytes(canonicalize_bytes(data))


def sha256_file(path: Path) -> str:
    """The ledger tooling's ONE shared canonical-hash helper:
    SHA-256 over the file's canonical form (see
    :func:`canonicalize_bytes`). Every hash recorded over a
    source file — ledger ``sources`` hashes, sidecar hashes,
    migration provenance — goes through here, so Stages 2–3
    cite the same hash for the same source."""
    return canonical_sha256_bytes(Path(path).read_bytes())


def load_schema(root: Path) -> dict[str, Any]:
    return json.loads((root / SCHEMA_REL).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Source-record provenance


class _SourceCache:
    """Loads source JSON files once and answers provenance queries."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._files: dict[str, Any] = {}

    def load(self, rel_path: str) -> Any:
        if rel_path not in self._files:
            p = self.root / rel_path
            self._files[rel_path] = (
                json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None
            )
        return self._files[rel_path]

    def claim_record(self, source: dict[str, Any]) -> Optional[dict[str, Any]]:
        """The claim record a ledger ``sources`` entry points at."""
        data = self.load(str(source.get("path", "")))
        claim_id = source.get("claim_id")
        if not isinstance(data, dict) or claim_id is None:
            return None
        for record in data.get("claims", []):
            if record.get("claim_id") == claim_id or record.get("id") == claim_id:
                return record
        return None

    def falsifier_texts(self, entry: dict[str, Any]) -> set[str]:
        texts: set[str] = set()
        for source in entry.get("sources", []):
            record = self.claim_record(source)
            if record is None:
                continue
            for key in _PROVENANCE_FALSIFIER_KEYS:
                value = record.get(key)
                if isinstance(value, list):
                    texts.update(str(v) for v in value)
                elif isinstance(value, str) and value:
                    texts.add(value)
        return texts

    def representative_dne_texts(self, entry: dict[str, Any]) -> set[str]:
        """Does-not-establish candidates from representative sources."""
        texts: set[str] = set()
        for source in entry.get("sources", []):
            if source.get("role") not in ("source_of_record", "bundle_aee"):
                continue
            record = self.claim_record(source)
            if record is None:
                continue
            for key in ("not_understood", "boundary"):
                value = record.get(key)
                if isinstance(value, str) and value:
                    texts.add(value)
                elif isinstance(value, list) and value:
                    texts.add(" ".join(str(v) for v in value))
        return texts


# ---------------------------------------------------------------------------
# Validation


def validate_entry(
    entry: dict[str, Any],
    *,
    root: Path,
    cache: Optional[_SourceCache] = None,
) -> list[str]:
    """Schema + fingerprint + provenance checks for one entry."""
    errors: list[str] = []
    validator = Draft202012Validator(load_schema(root))
    for err in sorted(validator.iter_errors(entry), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"schema: {where}: {err.message}")
    if errors:
        return errors
    if entry.get("kind") != "claim":
        return errors
    cache = cache or _SourceCache(root)
    recomputed = proposition_fingerprint(entry.get("statement"))
    if recomputed != entry.get("proposition_fingerprint"):
        errors.append(
            "fingerprint: stored proposition_fingerprint does not "
            f"recompute under {FINGERPRINT_RULES_VERSION}"
        )
    falsifier = entry.get("falsifier")
    if falsifier:
        traced = cache.falsifier_texts(entry)
        has_promotion = any(
            s.get("role") == "promotion" for s in entry.get("sources", [])
        )
        if traced or has_promotion:
            for text in falsifier:
                if text not in traced and not has_promotion:
                    errors.append(
                        "provenance: falsifier text traces to no source "
                        f"record named in sources: {text[:80]!r}..."
                    )
    elif entry.get("migration") is None:
        errors.append(
            "provenance: new (non-migration) claim entry carries no "
            "falsifier (prospective rule, D-086-Q6)"
        )
    dne = entry.get("does_not_establish")
    if dne:
        candidates = cache.representative_dne_texts(entry)
        has_promotion = any(
            s.get("role") == "promotion" for s in entry.get("sources", [])
        )
        if candidates and dne not in candidates and not has_promotion:
            errors.append(
                "provenance: does_not_establish traces to no "
                "representative source record"
            )
    explanation = entry.get("explanation_record")
    if explanation:
        author = explanation.get("author") if isinstance(explanation, dict) else None
        kind = explanation.get("author_kind") if isinstance(explanation, dict) else None
        if not author or kind != "human":
            errors.append(
                "provenance: explanation_record without a named human "
                "author (OD-2 / C086-6)"
            )
        elif entry.get("author") != author or entry.get("author_kind") != "human":
            errors.append(
                "provenance: entry author fields do not match its "
                "explanation_record (OD-2 / C086-6)"
            )
    return errors


@dataclass
class LedgerReport:
    path: str
    lines: int = 0
    kind_counts: dict[str, int] = field(default_factory=dict)
    population_counts: dict[str, int] = field(default_factory=dict)
    falsifier_covered: int = 0
    falsifier_total: int = 0
    falsifier_by_population: dict[str, tuple[int, int]] = field(default_factory=dict)
    dne_covered: int = 0
    aee_present: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def render(self) -> str:
        out = [
            f"Ledger validation — {self.path}",
            f"schema: {SCHEMA_VERSION} ({SCHEMA_REL})",
            f"fingerprint rules: {FINGERPRINT_RULES_VERSION}",
            f"lines: {self.lines}",
            "entries by kind: "
            + ", ".join(
                f"{k} {v}" for k, v in sorted(self.kind_counts.items())
            ),
            "claims by population: "
            + ", ".join(
                f"{k} {v}" for k, v in sorted(self.population_counts.items())
            ),
            f"falsifier coverage: {self.falsifier_covered} of "
            f"{self.falsifier_total} claim entries carry a falsifier",
            "falsifier coverage by population: "
            + ", ".join(
                f"{k} {c}/{t}"
                for k, (c, t) in sorted(self.falsifier_by_population.items())
            ),
            f"does_not_establish coverage: {self.dne_covered} of "
            f"{self.falsifier_total} claim entries",
            f"aee_state present: {self.aee_present} of "
            f"{self.falsifier_total} claim entries",
        ]
        if self.errors:
            out.append(f"errors: {len(self.errors)}")
            out.extend(f"ERROR: {e}" for e in self.errors)
            out.append("RESULT: FAIL")
        else:
            out.append("errors: none")
            out.append("RESULT: PASS")
        return "\n".join(out) + "\n"


def read_ledger(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not path.is_file():
        return entries
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def validate_ledger(
    root: Path, ledger_path: Optional[Path] = None
) -> LedgerReport:
    ledger_path = ledger_path or (root / LEDGER_REL)
    report = LedgerReport(path=str(ledger_path))
    if not ledger_path.is_file():
        # A gate that passes on an absent artifact certifies
        # nothing. Missing (or empty, below) is RED, never a
        # vacuous PASS. (Defect found 2026-11-01: the first
        # version read a missing file as zero lines and passed.)
        report.errors.append(
            f"ledger file does not exist: {ledger_path}"
        )
        return report
    raw_lines = ledger_path.read_text(encoding="utf-8").splitlines()
    if not any(line.strip() for line in raw_lines):
        report.errors.append(
            f"ledger file contains no entries: {ledger_path}"
        )
        return report
    entries: list[dict[str, Any]] = []
    cache = _SourceCache(root)
    seen_ids: dict[str, int] = {}
    seen_fps: dict[str, str] = {}
    for lineno, line in enumerate(raw_lines, start=1):
        if not line.strip():
            continue
        report.lines += 1
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            report.errors.append(f"line {lineno}: invalid JSON: {exc}")
            continue
        entries.append(entry)
        report.kind_counts[entry.get("kind", "?")] = (
            report.kind_counts.get(entry.get("kind", "?"), 0) + 1
        )
        for err in validate_entry(entry, root=root, cache=cache):
            report.errors.append(f"line {lineno} ({entry.get('id')}): {err}")
        eid = entry.get("id")
        if eid in seen_ids:
            report.errors.append(
                f"line {lineno}: duplicate entry id {eid!r} "
                f"(first at line {seen_ids[eid]})"
            )
        seen_ids[eid] = lineno
        if entry.get("kind") == "claim":
            pop = entry.get("population", "?")
            report.population_counts[pop] = report.population_counts.get(pop, 0) + 1
            report.falsifier_total += 1
            cov, tot = report.falsifier_by_population.get(pop, (0, 0))
            tot += 1
            if entry.get("falsifier"):
                cov += 1
                report.falsifier_covered += 1
            report.falsifier_by_population[pop] = (cov, tot)
            if entry.get("does_not_establish"):
                report.dne_covered += 1
            if entry.get("aee_state"):
                report.aee_present += 1
            fp = entry.get("proposition_fingerprint")
            if fp in seen_fps:
                report.errors.append(
                    f"line {lineno}: fingerprint shared with entry "
                    f"{seen_fps[fp]!r} (D-B: one canonical entry per "
                    "proposition)"
                )
            else:
                seen_fps[fp] = eid
    claim_ids = {
        e.get("id") for e in entries if e.get("kind") == "claim"
    }
    for entry in entries:
        if entry.get("kind") == "annotation":
            target = entry.get("canonical_claim_id") or entry.get("target_claim_id")
            if target not in claim_ids:
                report.errors.append(
                    f"annotation {entry.get('id')}: target claim "
                    f"{target!r} is not a ledger claim entry"
                )
        if entry.get("kind") == "reclassification":
            if entry.get("supersedes") not in {e.get("id") for e in entries}:
                report.errors.append(
                    f"reclassification {entry.get('id')}: supersedes "
                    f"{entry.get('supersedes')!r} names no ledger entry"
                )
    return report


# ---------------------------------------------------------------------------
# Verified write / append


def _verified_replace(path: Path, new_bytes: bytes, *, old_bytes: bytes) -> None:
    """Replace ``path`` with ``new_bytes`` (which must extend
    ``old_bytes``), then read back and verify byte-for-byte."""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".ledger-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(new_bytes)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    read_back = path.read_bytes()
    if read_back != new_bytes or not read_back.startswith(old_bytes):
        raise RuntimeError(
            f"verified write failed for {path}: read-back does not "
            "match the written bytes (append-only invariant broken)"
        )


def dump_entry(entry: dict[str, Any]) -> str:
    return json.dumps(entry, sort_keys=True, ensure_ascii=False)


def append_entry(
    root: Path,
    entry: dict[str, Any],
    ledger_path: Optional[Path] = None,
) -> None:
    """Validate and append one entry. Writes nothing on refusal."""
    ledger_path = ledger_path or (root / LEDGER_REL)
    errors = validate_entry(entry, root=root)
    if errors:
        raise ValueError("ledger intake refused: " + "; ".join(errors))
    existing = read_ledger(ledger_path)
    if entry.get("kind") == "claim":
        fp = entry["proposition_fingerprint"]
        for other in existing:
            if other.get("kind") == "claim" and other.get(
                "proposition_fingerprint"
            ) == fp:
                raise DuplicatePropositionError(
                    incoming_claim_id=str(entry.get("id")),
                    existing_claim_id=str(other.get("id")),
                    fingerprint=fp,
                )
    if any(e.get("id") == entry.get("id") for e in existing):
        raise ValueError(
            f"ledger intake refused: entry id {entry.get('id')!r} "
            "already exists in the ledger"
        )
    old_bytes = ledger_path.read_bytes() if ledger_path.is_file() else b""
    new_bytes = old_bytes + (dump_entry(entry) + "\n").encode("utf-8")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    _verified_replace(ledger_path, new_bytes, old_bytes=old_bytes)


def write_ledger(
    root: Path,
    entries: list[dict[str, Any]],
    ledger_path: Optional[Path] = None,
) -> None:
    """Bulk verified write used by the one-time D-E migration.

    Refuses to replace a non-empty ledger: after migration the
    only write path is :func:`append_entry`.
    """
    ledger_path = ledger_path or (root / LEDGER_REL)
    if ledger_path.is_file() and ledger_path.read_bytes().strip():
        raise RuntimeError(
            "write_ledger refuses to replace a non-empty ledger; "
            "post-migration writes go through append_entry"
        )
    cache = _SourceCache(root)
    for entry in entries:
        errors = validate_entry(entry, root=root, cache=cache)
        if errors:
            raise ValueError(
                f"migration entry {entry.get('id')!r} invalid: "
                + "; ".join(errors)
            )
    fps = [e["proposition_fingerprint"] for e in entries if e.get("kind") == "claim"]
    if len(fps) != len(set(fps)):
        raise ValueError("migration set contains duplicate fingerprints (D-B)")
    body = "".join(dump_entry(e) + "\n" for e in entries).encode("utf-8")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    _verified_replace(ledger_path, body, old_bytes=b"")


# ---------------------------------------------------------------------------
# Intake route builders (T103)


_CONFIDENCE_KEYS = ("confidence_in_source", "confidence")


def _confidence_fields(record: dict[str, Any]) -> dict[str, Any]:
    """Verbatim confidence carriage (harmonization adoption
    #3, item 6 — BINDING): narrative confidence is not a
    number. A numeric source confidence is carried verbatim
    into ``confidence_in_source``; a qualitative (string)
    confidence is carried VERBATIM into ``confidence_text``
    and is NEVER normalized into a numeric value; any other
    non-null shape is carried as its canonical JSON text in
    ``confidence_text``. Absent/null -> both null."""
    fields: dict[str, Any] = {
        "confidence_in_source": None,
        "confidence_text": None,
    }
    for key in _CONFIDENCE_KEYS:
        value = record.get(key)
        if value is None:
            continue
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            fields["confidence_in_source"] = value
        elif isinstance(value, str):
            fields["confidence_text"] = value
        else:
            fields["confidence_text"] = json.dumps(value, sort_keys=True)
        return fields
    return fields


def _sign_refs(record: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    sign_ids = record.get("sign_ids")
    if isinstance(sign_ids, dict):
        for system, values in sorted(sign_ids.items()):
            if system == "glossa_note" or not isinstance(values, list):
                continue
            for value in values:
                refs.append(f"{system}:{value}")
    return refs


def entry_from_extracted_record(
    record: dict[str, Any],
    *,
    source_path: str,
    source_sha256: str,
    date: str,
    migration: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Route 1 (extraction intake) / P1 migration: one extracted
    claim record -> one ledger claim entry."""
    explanation = record.get("explanation_record") or None
    evidence_refs = set()
    if record.get("source_document_id"):
        evidence_refs.add(str(record["source_document_id"]))
    for instance in record.get("evidence_instances") or []:
        if isinstance(instance, dict) and instance.get("claim_id"):
            evidence_refs.add(str(instance["claim_id"]))
    falsifier: list[str] = []
    for key in _PROVENANCE_FALSIFIER_KEYS:
        value = record.get(key)
        if isinstance(value, list):
            falsifier.extend(str(v) for v in value)
        elif isinstance(value, str) and value:
            falsifier.append(value)
    return {
        "id": str(record["claim_id"]),
        "kind": "claim",
        "population": "extracted",
        "statement": str(record["normalized_claim"]),
        "proposition_fingerprint": proposition_fingerprint(
            record["normalized_claim"]
        ),
        "sources": [
            {
                "path": source_path,
                "sha256": source_sha256,
                "role": "source_of_record",
                "spec": None,
                "claim_id": str(record["claim_id"]),
                "document_id": record.get("source_document_id"),
            }
        ],
        "date": date,
        "as_of": record.get("stage_as_of"),
        "status": str(record.get("claim_status")),
        "stage": record.get("stage"),
        "stage_source": record.get("stage_source"),
        "aee_state": None,
        **_confidence_fields(record),
        "falsifier": falsifier or None,
        "does_not_establish": record.get("not_understood"),
        "evidence_refs": sorted(evidence_refs),
        "sign_refs": _sign_refs(record),
        "author": explanation.get("author") if explanation else None,
        "author_kind": explanation.get("author_kind") if explanation else None,
        "explanation_record": explanation,
        "migration": migration,
    }


def annotation_from_sidecar(
    root: Path,
    sidecar_path: Path,
    *,
    date: str,
    canonical_map: dict[str, str],
    migration: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Route 3 (research-check intake): one advisory sidecar ->
    one annotation entry. The sidecar is never modified and the
    annotation changes no claim field."""
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    rel = str(sidecar_path.relative_to(root))
    stem = sidecar_path.name.replace(".research_check.json", "").replace(
        ".json", ""
    )
    target = str(sidecar["claim_id"])
    return {
        "id": f"annotation/{stem}",
        "kind": "annotation",
        "date": date,
        "target_claim_id": target,
        "canonical_claim_id": canonical_map.get(target, target),
        "sidecar": {"path": rel, "sha256": sha256_file(sidecar_path)},
        "bearing": {
            "advisory": True,
            "stage": str(sidecar.get("stage")),
            "verdict": sidecar.get("verdict"),
            "checked_at": sidecar.get("checked_at"),
            "protocol": sidecar.get("protocol"),
            "sources_requested": list(sidecar.get("sources_requested") or []),
            "neighbors_surfaced": len(sidecar.get("neighbors") or []),
            "gaps": len(sidecar.get("gaps") or []),
        },
        "migration": migration,
    }


def discovery_candidate(
    item: dict[str, Any],
    *,
    promoted_by: str,
    falsifier: list[str],
    date: str,
) -> dict[str, Any]:
    """Route 4 (discovery promotion): a named human promotes a
    discovery item to a candidate ledger entry. A falsifier is
    required at promotion; candidates carry no weight until
    adjudicated."""
    if not promoted_by:
        raise ValueError("discovery promotion requires a named human")
    if not falsifier:
        raise ValueError("discovery promotion requires a falsifier")
    statement = str(item.get("statement") or item.get("text") or "")
    if not statement:
        raise ValueError("discovery item carries no statement text")
    item_bytes = canonicalize_bytes(
        json.dumps(item, sort_keys=True).encode("utf-8")
    )
    return {
        "id": f"discovery/{item.get('id')}",
        "kind": "claim",
        "population": "discovery",
        "statement": statement,
        "proposition_fingerprint": proposition_fingerprint(statement),
        "sources": [
            {
                "path": "discovery_items",
                "sha256": sha256_bytes(item_bytes),
                "role": "promotion",
                "spec": None,
                "claim_id": str(item.get("id")),
                "document_id": None,
            }
        ],
        "date": date,
        "as_of": None,
        "status": "candidate",
        "stage": "created",
        "stage_source": f"discovery promotion by {promoted_by} on {date}",
        "aee_state": None,
        **_confidence_fields(item),
        "falsifier": list(falsifier),
        "does_not_establish": item.get("does_not_establish"),
        "evidence_refs": [],
        "sign_refs": [],
        "author": promoted_by,
        "author_kind": "human",
        "explanation_record": None,
        "migration": None,
    }


def extracted_canonical_map(root: Path) -> dict[str, str]:
    """claim_id -> canonical claim_id for the P1 store, resolved
    through its own ``merged_into`` pointers (Spec 029 Phase I)."""
    claims_dir = root / "glossa-indus" / "claims" / "extracted_claims"
    mapping: dict[str, str] = {}
    for path in sorted(claims_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("claims", []):
            mapping[str(record["claim_id"])] = str(
                record.get("merged_into") or record["claim_id"]
            )
    return mapping


# ---------------------------------------------------------------------------
# Bundle (P2) grouping — D-B applied to the spec governance bundles


@dataclass
class BundleGroup:
    fingerprint: str
    entry: dict[str, Any]
    # (spec, claim_id, format, path) for every source record of
    # this proposition, representative first.
    members: list[tuple[str, str, str, str]]
    representative: tuple[str, str]


def _boundary_text(record: dict[str, Any]) -> Optional[str]:
    value = record.get("boundary")
    if isinstance(value, str) and value:
        return value
    if isinstance(value, list) and value:
        return " ".join(str(v) for v in value)
    return None


def build_bundle_entries(
    root: Path,
    spec_dirs: Iterable[Path],
    *,
    date: str,
    migration: Optional[dict[str, Any]] = None,
) -> list[BundleGroup]:
    """Group bundle claim records by proposition fingerprint
    (D-B: one canonical entry per proposition) and build one
    ledger entry per group. The representative record is the
    group's first (spec, claim id) in sorted order; every other
    record of the proposition is preserved as an evidence
    instance in the entry's ``sources``. Falsifiers are the
    ordered union over the group's records — each string traces
    to a named source record."""
    records: list[tuple[str, str, str, Path, dict[str, Any]]] = []
    file_hashes: dict[Path, str] = {}
    for spec_dir in sorted(spec_dirs):
        spec = spec_dir.name
        for fmt, name in (("claims", "claims.json"), ("aee", "aee-claims.json")):
            path = spec_dir / name
            if not path.is_file():
                continue
            file_hashes[path] = sha256_file(path)
            data = json.loads(path.read_text(encoding="utf-8"))
            for record in data.get("claims", []):
                records.append((spec, str(record["id"]), fmt, path, record))
    groups: dict[str, list[tuple[str, str, str, Path, dict[str, Any]]]] = {}
    for rec in records:
        groups.setdefault(proposition_fingerprint(rec[4].get("text")), []).append(rec)
    out: list[BundleGroup] = []
    for fp in sorted(groups):
        members = sorted(groups[fp], key=lambda r: (r[0], r[1], r[2]))
        rep_spec, rep_id = members[0][0], members[0][1]
        rep_records = [r for r in members if (r[0], r[1]) == (rep_spec, rep_id)]
        rep = next(
            (r for r in rep_records if r[2] == "claims"), rep_records[0]
        )
        rep_record = rep[4]
        sources: list[dict[str, Any]] = []
        falsifier: list[str] = []
        for spec, claim_id, fmt, path, record in members:
            if (spec, claim_id) == (rep_spec, rep_id):
                # The representative record's own serialization is
                # the source of record; the pair's other
                # serialization (when both exist) is bundle_aee.
                role = "source_of_record" if fmt == rep[2] else "bundle_aee"
            else:
                role = "evidence_instance"
            sources.append(
                {
                    "path": str(path.relative_to(root)),
                    "sha256": file_hashes[path],
                    "role": role,
                    "spec": spec,
                    "claim_id": claim_id,
                    "document_id": None,
                }
            )
            for text in record.get("falsification_tests") or []:
                if str(text) not in falsifier:
                    falsifier.append(str(text))
        stage = None
        stage_source = None
        for spec, claim_id, fmt, path, record in rep_records:
            if fmt == "aee" and record.get("stage"):
                stage = record["stage"]
                stage_source = str(path.relative_to(root))
        evidence_refs = set()
        for item in rep_record.get("evidence") or []:
            if isinstance(item, dict) and item.get("ref"):
                evidence_refs.add(str(item["ref"]))
        for dep in rep_record.get("depends_on") or []:
            evidence_refs.add(str(dep))
        entry = {
            "id": f"{rep_spec}/{rep_id}",
            "kind": "claim",
            "population": "bundle",
            "statement": str(rep_record.get("text")),
            "proposition_fingerprint": fp,
            "sources": sources,
            "date": date,
            "as_of": None,
            "status": str(rep_record.get("status")),
            "stage": stage,
            "stage_source": stage_source,
            "aee_state": None,
            **_confidence_fields(rep_record),
            "falsifier": falsifier or None,
            "does_not_establish": _boundary_text(rep_record),
            "evidence_refs": sorted(evidence_refs),
            "sign_refs": [],
            "author": None,
            "author_kind": None,
            "explanation_record": None,
            "migration": migration,
        }
        out.append(
            BundleGroup(
                fingerprint=fp,
                entry=entry,
                members=[
                    (s, c, f, str(p.relative_to(root))) for s, c, f, p, _ in members
                ],
                representative=(rep_spec, rep_id),
            )
        )
    return out
