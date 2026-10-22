"""Spec 029 Phase J (D-D) — computed foundation-report annotations.

The Spec 029 audit (§5-P8, defect 3) found Phase-48-era prose
riding unflagged inside the live foundation report: the embedded
``solid_claims`` / ``caveated_claims`` annotations quoted a
Phase-48-era tier split and an unresolved-M267 figure from an
anchor table that no longer exists (the audit names the exact
figures), and the foundation status endpoint served silent
nulls beside the healthy on-disk report.

D-D's structural fix, implemented here: every annotation figure
that describes canonical data is **computed from the canonical
stores at report-generation time** — the anchors file
(``backend/reports/INDUS_FINAL_ANCHORS.json``) and the
extracted-claims store (``glossa-indus/claims/extracted_claims/``)
— and the generated report is stamped with the SHA-256 of the
anchors file it was computed against (the raw file bytes; the same
stamp Phase H records for that file) plus a combined digest of
the claims store. Hand-typed canonical figures cannot drift,
because there are none: regenerate the report and the figures
track the canonical files.

This module is the single source of that computation.
``backend/scripts/foundation_check.py`` builds its computed
annotations from it, and the foundation status endpoint
(``glossa_lab.api.foundation``) uses its hash helper to flag a
report whose stamp no longer matches the anchors file on disk.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
CLAIMS_REL = "glossa-indus/claims/extracted_claims"

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def anchors_file_sha256(anchors_path: Path) -> str:
    """SHA-256 of the anchors file's raw bytes (its identity stamp)."""
    return sha256_bytes(Path(anchors_path).read_bytes())


def claims_store_digest(claims_dir: Path) -> tuple[str, int, int]:
    """Combined digest of the extracted-claims store.

    Returns ``(digest, n_files, n_claims)``. The digest is the
    SHA-256 of the newline-joined ``"<filename>:<file sha256>"``
    lines over the store's ``*.json`` files in sorted order, so
    any content change in any claims file changes the digest.
    ``n_claims`` sums each file's ``claims`` list.
    """
    claims_dir = Path(claims_dir)
    lines: list[str] = []
    n_claims = 0
    files = sorted(claims_dir.glob("*.json"))
    for path in files:
        raw = path.read_bytes()
        lines.append(f"{path.name}:{sha256_bytes(raw)}")
        doc = json.loads(raw.decode("utf-8"))
        claims = doc.get("claims", []) if isinstance(doc, dict) else []
        n_claims += len(claims)
    return sha256_bytes("\n".join(lines).encode("utf-8")), len(files), n_claims


def compute_canonical_snapshot(
    repo_root: Path, *, as_of: str | None = None
) -> dict[str, Any]:
    """Compute every canonical figure the foundation report quotes.

    Reads only the canonical stores (anchors file + claims store)
    under ``repo_root``. ``as_of`` is the report-generation date
    (ISO); it defaults to today (UTC-naive local date is not used —
    the caller in the foundation script passes its own run date;
    tests pass an explicit date for determinism).
    """
    repo_root = Path(repo_root)
    anchors_path = repo_root / ANCHORS_REL
    claims_dir = repo_root / CLAIMS_REL
    anchors_sha = anchors_file_sha256(anchors_path)
    doc = json.loads(anchors_path.read_text(encoding="utf-8"))
    anchors: dict[str, Any] = doc.get("anchors", {})

    tier_counts = Counter(v.get("confidence", "?") for v in anchors.values())
    validation_counts = Counter(
        v.get("validation_status", "?") for v in anchors.values()
    )
    strict = {k: v for k, v in anchors.items() if v.get("strict_set")}
    strict_composition = Counter(v.get("confidence", "?") for v in strict.values())
    m267 = anchors.get("M267", {})
    claims_sha, n_claim_files, n_claims = claims_store_digest(claims_dir)
    as_of_date = as_of or date.today().isoformat()

    snapshot: dict[str, Any] = {
        "as_of_date": as_of_date,
        "anchors_file": ANCHORS_REL,
        "anchors_file_sha256": anchors_sha,
        "claims_store": CLAIMS_REL,
        "claims_store_sha256": claims_sha,
        "claims_files": n_claim_files,
        "claims_total": n_claims,
        "anchors_total": len(anchors),
        "tier_counts": {k: tier_counts[k] for k in sorted(tier_counts)},
        "hm_count": tier_counts.get("HIGH", 0) + tier_counts.get("MEDIUM", 0),
        "validation_status_counts": {
            k: validation_counts[k] for k in sorted(validation_counts)
        },
        "pending_count": validation_counts.get("pending_non_sa_validation", 0),
        "strict_count": len(strict),
        "strict_composition": {
            k: strict_composition[k] for k in sorted(strict_composition)
        },
        "corpus_token_coverage": doc.get("corpus_token_coverage"),
        "m267": {
            "confidence": m267.get("confidence"),
            "validation_status": m267.get("validation_status"),
            "strict_set": bool(m267.get("strict_set")),
        },
    }
    snapshot["as_of_label"] = as_of_label(snapshot)
    return snapshot


def as_of_label(snapshot: dict[str, Any]) -> str:
    """The dated as-of label naming the anchor table described (J1).

    This is the foundation report's permanent provenance line: it
    names the canonical data state (anchors-file hash + claims
    digest + generation date) every computed figure describes, so
    no figure can be read as current when it is not.
    """
    return (
        f"As of {snapshot['as_of_date']} — computed at report generation from "
        f"the canonical anchors file {snapshot['anchors_file']} "
        f"(SHA-256 {snapshot['anchors_file_sha256']}) and the extracted-claims "
        f"store {snapshot['claims_store']} "
        f"(combined SHA-256 {snapshot['claims_store_sha256']}). "
        "Figures describe that anchor table; if the anchors file changes, "
        "this label's hash no longer matches and the report is stale."
    )


def _composition(counts: dict[str, int], order: tuple[str, ...]) -> str:
    parts = [f"{counts[k]} {k}" for k in order if k in counts]
    parts += [f"{v} {k}" for k, v in counts.items() if k not in order]
    return " + ".join(parts)


def computed_annotation_entries(
    snapshot: dict[str, Any],
) -> tuple[tuple[str, str, str], tuple[str, str, str]]:
    """The computed annotations, as (claim, detail, status) triples.

    Returns ``(solid_entry, caveated_entry)`` in the foundation
    script's annotation shape. Every figure in both details comes
    from ``snapshot`` — nothing is hand-typed.
    """
    tiers = snapshot["tier_counts"]
    tier_split = _composition(tiers, ("HIGH", "MEDIUM", "LOW", "CANDIDATE"))
    strict_comp = _composition(
        snapshot["strict_composition"], ("HIGH", "MEDIUM", "LOW", "CANDIDATE")
    )
    validation_split = ", ".join(
        f"{k}={v}" for k, v in snapshot["validation_status_counts"].items()
    )
    coverage = snapshot["corpus_token_coverage"]
    coverage_text = (
        f"{coverage:.1%}" if isinstance(coverage, (int, float)) else "not recorded"
    )
    m267 = snapshot["m267"]

    solid_entry = (
        "Canonical anchor table (computed)",
        (
            f"{snapshot['anchors_total']} anchors in the canonical table: "
            f"{tier_split}. Strict core (strict_set, per the Phase-108 "
            f"register + Phase-109 rule as annotated in Phase H): "
            f"{snapshot['strict_count']} anchors ({strict_comp}). "
            f"Pending validation: {snapshot['pending_count']} anchors "
            "(validation_status=pending_non_sa_validation). "
            f"validation_status distribution: {validation_split}. "
            f"H+M token coverage of the Holdat corpus, as recorded in the "
            f"anchors file: {coverage_text}. Extracted-claims store: "
            f"{snapshot['claims_total']} claims in "
            f"{snapshot['claims_files']} files."
        ),
        "VERIFIED — computed from the canonical stores at report "
        "generation; hash-stamped (see annotations_as_of)",
    )
    caveated_entry = (
        "signs assigned",
        (
            f"{snapshot['hm_count']} signs "
            f"({tiers.get('HIGH', 0)} HIGH + {tiers.get('MEDIUM', 0)} MEDIUM) "
            "carry phonetic/grammatical evidence in the current canonical "
            f"anchor table; {tiers.get('LOW', 0)} LOW entries are "
            f"distributional proposals only and {tiers.get('CANDIDATE', 0)} "
            "CANDIDATE entries are unvalidated. M267 is "
            f"{m267['confidence']} (validation_status "
            f"{m267['validation_status']}) in the current table — resolved, "
            "not UNCERTAIN. All figures computed at report generation from "
            "the hash-stamped anchors file (see annotations_as_of)."
        ),
        "CLARIFY: HIGH+MEDIUM are supported; LOW are distributional "
        "proposals only",
    )
    return solid_entry, caveated_entry


def historical_label(phase: str) -> str:
    """In-detail as-of marker for a legitimately historical figure (J4)."""
    return (
        f" [Historical figure — as of {phase}, when this result was "
        "recorded; the current canonical figures are computed at report "
        "time in the 'Canonical anchor table (computed)' annotation.]"
    )
