"""Proposition fingerprints — Spec 029 Phase I (D-B), tasks I1/I4.

D-B (ratified 2026-10-12, ``specs/029-tao-claim-lifecycle/
adjudication.md`` addendum): extracted claims are deduplicated by
**proposition** — merge, never delete — and a proposition
fingerprint is checked at extraction intake so a duplicate
proposition can never silently enter the store again.

The fingerprint is a SHA-256 hash over the **normalised claim
text** (the record's ``normalized_claim`` field). The
normalisation rules are defined here and FROZEN by Phase I
(changing them changes every fingerprint; any change is a new
phase, not an edit):

1. Unicode NFKC normalisation, then case-folding.
2. Every character that is not a Unicode letter or digit is
   replaced by a single space. This one rule subsumes
   whitespace normalisation (runs of spaces, tabs, and the
   newlines some extraction snippets carry mid-phrase collapse
   identically) and punctuation normalisation
   (``Zipf-Mandelbrot`` and ``Zipf Mandelbrot`` are the same
   proposition text; ``Indus-Script`` and ``Indus script``
   likewise).
3. The result is split on whitespace and re-joined with single
   spaces (leading/trailing space removed).

The fingerprint of a claim is therefore a function of its
proposition text only — not of its source document, status,
stage, or evidence. Two records with the same fingerprint are,
under this phase's frozen definition, two records of one
proposition: the merge (Phase I tooling) keeps one canonical
record and preserves the others as evidence instances of it,
and the intake gate refuses any *new* record whose fingerprint
collides with an existing proposition.
"""

from __future__ import annotations

import hashlib
import unicodedata
from typing import Any

#: Version tag for the frozen normalisation rules above. Stored
#: alongside fingerprints in the phase record; a rules change
#: bumps this and re-fingerprints the store as a new phase.
FINGERPRINT_RULES_VERSION = "spec029-phase-i-v1"


def normalize_proposition_text(text: Any) -> str:
    """Normalise claim text per the frozen Phase I rules."""
    folded = unicodedata.normalize("NFKC", str(text or "")).casefold()
    chars = [ch if ch.isalnum() else " " for ch in folded]
    return " ".join("".join(chars).split())


def proposition_fingerprint(text: Any) -> str:
    """SHA-256 hex digest of the normalised proposition text."""
    normalized = normalize_proposition_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def claim_fingerprint(record: dict[str, Any]) -> str:
    """Fingerprint of one extracted-claim record (its proposition)."""
    return proposition_fingerprint(record.get("normalized_claim"))


class DuplicatePropositionError(RuntimeError):
    """Intake gate failure (tasks I4): a new claim's proposition
    fingerprint collides with an existing record's.

    The message names both records — the incoming claim and the
    existing canonical claim for that proposition — so the
    collision is loud and inspectable, never silent.
    """

    def __init__(self, *, incoming_claim_id: str, existing_claim_id: str,
                 fingerprint: str) -> None:
        self.incoming_claim_id = incoming_claim_id
        self.existing_claim_id = existing_claim_id
        self.fingerprint = fingerprint
        super().__init__(
            "duplicate proposition at extraction intake: incoming claim "
            f"{incoming_claim_id!r} has proposition fingerprint "
            f"{fingerprint} which already exists on claim "
            f"{existing_claim_id!r} (Spec 029 D-B: one canonical claim "
            "per proposition; merge, never delete — the new record was "
            "NOT written)"
        )


def fingerprint_groups(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group records by proposition fingerprint (insertion-ordered)."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        groups.setdefault(claim_fingerprint(record), []).append(record)
    return groups


def canonical_claim_id(record: dict[str, Any]) -> str:
    """The canonical claim id a record belongs to: itself, unless it
    is a merged evidence instance (``merged_into`` pointer)."""
    return str(record.get("merged_into") or record.get("claim_id") or "")
