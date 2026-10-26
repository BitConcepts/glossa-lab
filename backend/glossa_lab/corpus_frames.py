"""Gap-aware corpus representation (repair WP6, 2026-10-26).

This module sits ALONGSIDE the historical compressed frame. It does not
replace it and it does not change any frozen result.

The historical compressed frame (for example the Spec 076 pilot frame)
builds a token sequence by dropping tokens: placeholder tokens (``000``)
and marked tokens (``*``-prefixed) are removed, and positions are then
counted on what is left. That is simple and reproducible, but it loses
information:

* a dropped token at the edge of an inscription moves the "initial" and
  "final" positions onto different signs;
* a damaged or unreadable place in the inscription disappears, so the
  sequence looks shorter and cleaner than the object really is;
* two records that describe the same object (a repeat impression, a
  duplicate publication, a duplicate transcription) can be silently
  merged or double-counted, with no record of which happened.

This module keeps every place in the inscription. Each token carries an
explicit state, each inscription carries stable identifiers where they
are supplied, and every positional statistic must say which meaning of
"initial" it used.

Boundary semantics (the caller must choose; there is no default):

* ``ORIGINAL_BOUNDARY`` -- position in the full inscription, gaps
  included. If the first place is a gap, no legible sign is initial:
  the boundary place is occupied by the gap.
* ``FIRST_LEGIBLE`` -- the first retained legible token. This matches
  the historical compressed frame, where dropped tokens are removed
  before positions are counted.

Standard library only.
"""

from __future__ import annotations

import enum
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Optional, Sequence

__all__ = [
    "BoundarySemantics",
    "TokenState",
    "RecordKind",
    "SignToken",
    "legible",
    "damaged",
    "unknown_gap",
    "marked",
    "InscriptionRecord",
    "GapAwareFrame",
    "PositionalResult",
    "PositionalCounts",
    "classify_positions",
    "initial_token",
    "final_token",
    "BlockedJoin",
    "JoinResult",
    "join_on_mahadevan",
    "analyze_within_scheme",
]


class BoundarySemantics(enum.Enum):
    """Which meaning of a boundary position a statistic used."""

    ORIGINAL_BOUNDARY = "ORIGINAL_BOUNDARY"
    FIRST_LEGIBLE = "FIRST_LEGIBLE"


class TokenState(enum.Enum):
    """The state of one place in an inscription."""

    LEGIBLE = "legible"          # a sign that can be read
    DAMAGED = "damaged"          # a place is there; the sign is damaged
    UNKNOWN_GAP = "unknown_gap"  # a place is there; nothing can be read
    MARKED = "marked"            # a read sign carrying a mark (e.g. ``*``)


class RecordKind(enum.Enum):
    """What kind of record this is. These kinds are never merged silently."""

    ORIGINAL_ARTIFACT = "original_artifact"
    REPEAT_IMPRESSION = "repeat_impression"
    DUPLICATE_PUBLICATION = "duplicate_publication"
    DUPLICATE_TRANSCRIPTION = "duplicate_transcription"


@dataclass(frozen=True)
class SignToken:
    """One place in an inscription.

    ``sign_id`` is the sign identifier in the record's scheme, or None
    when no sign can be read at this place. ``raw`` keeps the source
    token exactly as supplied, when it is supplied.
    """

    state: TokenState
    sign_id: Optional[str] = None
    raw: Optional[str] = None

    def __post_init__(self) -> None:
        if self.state is TokenState.UNKNOWN_GAP and self.sign_id is not None:
            raise ValueError(
                "an unknown-gap token cannot carry a sign id; "
                "use DAMAGED if a damaged sign is partly readable"
            )
        if self.state is TokenState.LEGIBLE and not self.sign_id:
            raise ValueError("a legible token must carry a sign id")

    @property
    def is_legible(self) -> bool:
        return self.state is TokenState.LEGIBLE

    def to_dict(self) -> dict[str, Any]:
        return {"state": self.state.value, "sign_id": self.sign_id,
                "raw": self.raw}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SignToken":
        return cls(state=TokenState(data["state"]),
                   sign_id=data.get("sign_id"), raw=data.get("raw"))


def legible(sign_id: str, raw: Optional[str] = None) -> SignToken:
    return SignToken(TokenState.LEGIBLE, sign_id, raw)


def damaged(sign_id: Optional[str] = None,
            raw: Optional[str] = None) -> SignToken:
    return SignToken(TokenState.DAMAGED, sign_id, raw)


def unknown_gap(raw: Optional[str] = None) -> SignToken:
    return SignToken(TokenState.UNKNOWN_GAP, None, raw)


def marked(sign_id: str, raw: Optional[str] = None) -> SignToken:
    return SignToken(TokenState.MARKED, sign_id, raw)


@dataclass(frozen=True)
class InscriptionRecord:
    """One inscription record, with stable identifiers where supplied.

    ``record_kind`` distinguishes an original artifact record from a
    repeat impression, a duplicate publication, and a duplicate
    transcription. Records of different kinds are kept as separate
    records; ``related_object_id`` may link a duplicate or repeat to
    the object it repeats, but nothing in this module merges them.

    ``direction`` records the reading direction when it is known;
    ``direction_uncertain=True`` keeps an uncertain direction visible
    instead of silently fixing one.
    """

    object_id: str
    tokens: tuple[SignToken, ...]
    face: Optional[str] = None
    catalog_id: Optional[str] = None
    source_lineage: Optional[str] = None
    scheme: Optional[str] = None
    record_kind: RecordKind = RecordKind.ORIGINAL_ARTIFACT
    related_object_id: Optional[str] = None
    direction: Optional[str] = None
    direction_uncertain: bool = False

    def __post_init__(self) -> None:
        if not self.object_id:
            raise ValueError("every record must carry a stable object id")
        object.__setattr__(self, "tokens", tuple(self.tokens))

    @property
    def legible_tokens(self) -> tuple[SignToken, ...]:
        return tuple(t for t in self.tokens if t.is_legible)

    def compressed_sign_ids(self) -> list[str]:
        """The historical compressed view of this record.

        Only legible tokens survive, in order. This is exactly the
        information loss the gap-aware view exists to make visible:
        gaps, damaged places, and marked signs are gone, and boundary
        positions move onto the surviving signs.
        """
        return [t.sign_id for t in self.tokens if t.is_legible]

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "face": self.face,
            "catalog_id": self.catalog_id,
            "source_lineage": self.source_lineage,
            "scheme": self.scheme,
            "record_kind": self.record_kind.value,
            "related_object_id": self.related_object_id,
            "direction": self.direction,
            "direction_uncertain": self.direction_uncertain,
            "tokens": [t.to_dict() for t in self.tokens],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "InscriptionRecord":
        return cls(
            object_id=data["object_id"],
            tokens=tuple(SignToken.from_dict(t) for t in data["tokens"]),
            face=data.get("face"),
            catalog_id=data.get("catalog_id"),
            source_lineage=data.get("source_lineage"),
            scheme=data.get("scheme"),
            record_kind=RecordKind(
                data.get("record_kind", RecordKind.ORIGINAL_ARTIFACT.value)),
            related_object_id=data.get("related_object_id"),
            direction=data.get("direction"),
            direction_uncertain=bool(data.get("direction_uncertain", False)),
        )


def _require_boundary(boundary: Optional[BoundarySemantics]) -> BoundarySemantics:
    if boundary is None or not isinstance(boundary, BoundarySemantics):
        raise ValueError(
            "boundary semantics must be chosen explicitly: pass "
            "boundary=BoundarySemantics.ORIGINAL_BOUNDARY (position in "
            "the full inscription, gaps included) or "
            "boundary=BoundarySemantics.FIRST_LEGIBLE (first retained "
            "legible token). There is no default, because the two "
            "meanings give different answers on inscriptions with "
            "leading or trailing gaps."
        )
    return boundary


@dataclass(frozen=True)
class PositionalResult:
    """One positional answer, naming the semantics it used."""

    sign_id: Optional[str]
    slot: str  # "initial" | "final" | "solo" | "medial" | "none"
    boundary_semantics: BoundarySemantics

    def describe(self) -> str:
        return (f"{self.slot} under {self.boundary_semantics.value}: "
                f"{self.sign_id!r}")


def classify_positions(
    record: InscriptionRecord,
    *,
    boundary: Optional[BoundarySemantics] = None,
) -> list[tuple[SignToken, str]]:
    """Classify every legible token's slot under the chosen semantics.

    Returns ``(token, slot)`` pairs for legible tokens only, where slot
    is one of ``initial``, ``final``, ``solo``, ``medial``.

    * FIRST_LEGIBLE: positions are counted on the legible tokens alone
      (the compressed view). A record with exactly one legible token
      gives that token the ``solo`` slot, even if gaps surround it --
      this is the singleton-after-filtering case, and it is a property
      of the filtering, not of the original inscription.
    * ORIGINAL_BOUNDARY: positions are counted on all places, gaps
      included. A legible token is ``initial`` only at place 0 and
      ``final`` only at the last place; a lone legible token between
      gaps is ``medial``, and a one-place inscription is ``solo``.
    """
    boundary = _require_boundary(boundary)
    leg = record.legible_tokens
    if not leg:
        return []
    if boundary is BoundarySemantics.FIRST_LEGIBLE:
        if len(leg) == 1:
            return [(leg[0], "solo")]
        out: list[tuple[SignToken, str]] = []
        for i, tok in enumerate(leg):
            slot = "initial" if i == 0 else "final" if i == len(leg) - 1 else "medial"
            out.append((tok, slot))
        return out
    # ORIGINAL_BOUNDARY
    n = len(record.tokens)
    if n == 1:
        return [(leg[0], "solo")]
    out = []
    for i, tok in enumerate(record.tokens):
        if not tok.is_legible:
            continue
        slot = "initial" if i == 0 else "final" if i == n - 1 else "medial"
        out.append((tok, slot))
    return out


def initial_token(
    record: InscriptionRecord,
    *,
    boundary: Optional[BoundarySemantics] = None,
) -> PositionalResult:
    """The initial sign under the chosen semantics (None if there is none).

    Under ORIGINAL_BOUNDARY, a leading gap means there is no initial
    legible sign. Under FIRST_LEGIBLE, the first legible sign is
    initial by construction. The returned result names the semantics.
    """
    boundary = _require_boundary(boundary)
    for tok, slot in classify_positions(record, boundary=boundary):
        if slot in ("initial", "solo"):
            return PositionalResult(tok.sign_id, slot, boundary)
    return PositionalResult(None, "none", boundary)


def final_token(
    record: InscriptionRecord,
    *,
    boundary: Optional[BoundarySemantics] = None,
) -> PositionalResult:
    """The final sign under the chosen semantics (see initial_token)."""
    boundary = _require_boundary(boundary)
    for tok, slot in classify_positions(record, boundary=boundary):
        if slot in ("final", "solo"):
            return PositionalResult(tok.sign_id, slot, boundary)
    return PositionalResult(None, "none", boundary)


@dataclass(frozen=True)
class PositionalCounts:
    """Slot counts over a frame, naming the semantics they used."""

    boundary_semantics: BoundarySemantics
    init: int
    fin: int
    solo: int
    med: int
    records_counted: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_semantics": self.boundary_semantics.value,
            "init": self.init, "fin": self.fin,
            "solo": self.solo, "med": self.med,
            "records_counted": self.records_counted,
        }


@dataclass
class GapAwareFrame:
    """A set of inscription records in the gap-aware representation."""

    records: list[InscriptionRecord] = field(default_factory=list)
    name: Optional[str] = None

    def add(self, record: InscriptionRecord) -> None:
        self.records.append(record)

    def positional_counts(
        self,
        *,
        boundary: Optional[BoundarySemantics] = None,
        record_kinds: Optional[Iterable[RecordKind]] = None,
    ) -> PositionalCounts:
        """Slot totals under the chosen semantics.

        By default every record kind is counted separately-visible:
        the caller may restrict ``record_kinds``; kinds are never
        merged or dropped silently -- the records counted are exactly
        the kinds named (or all kinds, when none are named).
        """
        boundary = _require_boundary(boundary)
        kinds = set(record_kinds) if record_kinds is not None else None
        counts: Counter[str] = Counter()
        n = 0
        for rec in self.records:
            if kinds is not None and rec.record_kind not in kinds:
                continue
            n += 1
            for _tok, slot in classify_positions(rec, boundary=boundary):
                counts[{"initial": "init", "final": "fin",
                        "medial": "med", "solo": "solo"}[slot]] += 1
        return PositionalCounts(
            boundary_semantics=boundary,
            init=counts["init"], fin=counts["fin"],
            solo=counts["solo"], med=counts["med"],
            records_counted=n,
        )

    def census(self) -> dict[str, Any]:
        """Plain counts of what this frame holds, by state and kind."""
        states: Counter[str] = Counter()
        kinds: Counter[str] = Counter()
        for rec in self.records:
            kinds[rec.record_kind.value] += 1
            for tok in rec.tokens:
                states[tok.state.value] += 1
        return {
            "records": len(self.records),
            "records_by_kind": dict(kinds),
            "tokens_total_places": sum(len(r.tokens) for r in self.records),
            "tokens_by_state": dict(states),
            "legible_tokens": states[TokenState.LEGIBLE.value],
        }


# ---------------------------------------------------------------------------
# Cross-scheme join on a Mahadevan identifier
# ---------------------------------------------------------------------------

def _mahadevan_id(entry: Any) -> Optional[str]:
    if isinstance(entry, Mapping):
        for key in ("mahadevan_id", "mahadevan", "m_id", "id"):
            if entry.get(key):
                return str(entry[key])
        return None
    return getattr(entry, "mahadevan_id", None)


@dataclass(frozen=True)
class BlockedJoin:
    """A sign whose cross-scheme join is blocked, and why."""

    mahadevan_id: Optional[str]
    left_count: int
    right_count: int
    reason: str


@dataclass(frozen=True)
class JoinResult:
    """Result of a cross-scheme join.

    ``joined`` holds only unambiguous one-to-one pairs. ``blocked``
    holds every affected sign that could not be joined safely.
    ``unmatched`` holds identifiers present on one side only.
    """

    joined: tuple[tuple[Any, Any], ...]
    blocked: tuple[BlockedJoin, ...]
    unmatched_left: tuple[str, ...]
    unmatched_right: tuple[str, ...]

    @property
    def blocked_ids(self) -> list[Optional[str]]:
        return [b.mahadevan_id for b in self.blocked]


def join_on_mahadevan(left: Sequence[Any], right: Sequence[Any]) -> JoinResult:
    """Join two entry sets on their Mahadevan identifier.

    If an identifier is REPEATED in either input, every join for that
    sign is blocked and returned in ``blocked``. The first match is
    never taken silently: a repeated identifier means the join does
    not say which entry on the repeated side is meant (this is the
    Spec 076 FF-4 / A-KEY situation: 13 Mahadevan identifiers claimed
    by two Parpola-keyed registry rows each).

    Analysis wholly within one scheme does not use this function and
    is unaffected by repeats; see ``analyze_within_scheme``.
    """
    left_by: dict[Optional[str], list[Any]] = {}
    for e in left:
        left_by.setdefault(_mahadevan_id(e), []).append(e)
    right_by: dict[Optional[str], list[Any]] = {}
    for e in right:
        right_by.setdefault(_mahadevan_id(e), []).append(e)

    joined: list[tuple[Any, Any]] = []
    blocked: list[BlockedJoin] = []
    unmatched_left: list[str] = []
    unmatched_right: list[str] = []
    for mid in sorted(set(left_by) | set(right_by), key=lambda x: (x is None, x)):
        lc, rc = len(left_by.get(mid, [])), len(right_by.get(mid, []))
        if mid is None:
            blocked.append(BlockedJoin(
                None, lc, rc,
                "entries without a Mahadevan identifier cannot be joined"))
            continue
        if lc > 1 or rc > 1:
            blocked.append(BlockedJoin(
                mid, lc, rc,
                f"Mahadevan identifier {mid} is repeated "
                f"(left x{lc}, right x{rc}); the join is ambiguous and "
                "no first match is taken"))
            continue
        if lc == 1 and rc == 1:
            joined.append((left_by[mid][0], right_by[mid][0]))
        elif lc == 1:
            unmatched_left.append(mid)
        else:
            unmatched_right.append(mid)
    return JoinResult(tuple(joined), tuple(blocked),
                      tuple(unmatched_left), tuple(unmatched_right))


def analyze_within_scheme(
    records: Sequence[InscriptionRecord],
    scheme: str,
) -> dict[str, Any]:
    """Counts wholly inside one scheme. No cross-scheme join is used,
    so repeated identifiers on a join surface elsewhere do not affect
    this analysis."""
    chosen = [r for r in records if r.scheme == scheme]
    signs: Counter[str] = Counter()
    for rec in chosen:
        for tok in rec.legible_tokens:
            signs[tok.sign_id] += 1
    return {
        "scheme": scheme,
        "records": len(chosen),
        "legible_tokens": sum(signs.values()),
        "distinct_signs": len(signs),
        "sign_counts": dict(sorted(signs.items())),
        "join_used": False,
    }
