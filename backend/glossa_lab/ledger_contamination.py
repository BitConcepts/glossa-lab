"""Ledger contamination gate class — Spec 095 Stage 3 (T301, C095-7).

The six contamination shapes of claim C095-7, as a gate class over
intake presentations. The class lives beside the Spec 086 ledger
gate (``ledger_gate.py``, classes V1-V11) and is run through the
same tooling (``tools/ledger/check_ledger_gate.py --contamination``),
but it is reported under its own summary: the V1-V11 profile of
record (``--all`` 29 PASS / 0 FAIL / 1 NOT-RUN; ``--regen`` 32/0/0)
is a cross-stage record and does not move.

The six shapes, verbatim from C095-7:

* S1 — a source-derived value labelled independent;
* S2 — a self-labelling derivative presented as source data;
* S3 — a translation or reading column presented as corpus data;
* S4 — a derived result presented as independent confirmation;
* S5 — the same data under two source identities;
* S6 — a summary or delivery presented as the underlying record.

Presentation model
------------------
An *intake presentation* is the candidate entry together with the
provenance facts intake assembles for every source it cites: who
produced the source's content, what authority the presentation
attributes it to, what kind of thing it is (corpus, reading column,
translation, result, summary, dataset, record), what lineage root
it derives from, and how the presentation treats it (as corpus
data, as the underlying record, as independent corroboration, or
ordinarily). These are facts intake knows or can state at intake
time; the Phase-96 lesson (repair baseline sections 4.3/4.4) is
that the program *knew* its own code had written the crosswalk's
reading column under a "Parpola 1994" label — nothing checked the
presentation against the facts. This class is that check.

Derivation alone is never flagged: a derivative cited as a
derivative, under its own identity, with no independence asserted,
is ordinary program work. Every detector keys on the
*mislabelling* — the gap between what a source is and how the
presentation presents it.

Live-ledger contract
--------------------
``scan_ledger`` builds a minimal presentation from each ledger
entry (its ``sources`` with roles and content pins; provenance
facts the entry does not carry stay unset, and detectors whose
inputs are absent do not fire) and additionally runs the S5
content-pin check across the whole ledger. The class therefore
passes on the current ledger — whose entries carry no contaminated
presentation in the fields they do carry — and fires at intake,
where the full presentation exists, and on the acceptance fixtures
(Spec 095 Stage 3 records, ``t301-fixtures-2026-11-16.json``),
which reconstruct the six historical instances of record from the
GR-088-01 / GR-088-11 / GR-088-16 / GR-088-29 family.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

#: The six contamination shapes (C095-7), id -> statement of record.
SHAPES: tuple[tuple[str, str], ...] = (
    ("S1", "a source-derived value labelled independent"),
    ("S2", "a self-labelling derivative presented as source data"),
    ("S3", "a translation or reading column presented as corpus data"),
    ("S4", "a derived result presented as independent confirmation"),
    ("S5", "the same data under two source identities"),
    ("S6", "a summary or delivery presented as the underlying record"),
)

SHAPE_NAMES: dict[str, str] = dict(SHAPES)

#: Identities that name the program itself; attribution to one of
#: these is self-attribution, not an external authority claim.
_PROGRAM_IDENTITIES = frozenset({
    "program",
    "glossa-lab",
    "glossa lab",
    "this program",
    "the program",
})

_READING_KINDS = frozenset({"reading-column", "translation"})
_SUMMARY_KINDS = frozenset({"summary", "delivery"})


@dataclass(frozen=True)
class ContaminationFlag:
    """One flagged presentation: the shape, the source, the reason."""

    shape: str
    presentation_id: str
    source_path: str
    detail: str

    def render(self) -> str:
        return (
            f"FLAG {self.shape} ({SHAPE_NAMES[self.shape]}): "
            f"presentation {self.presentation_id!r}, source "
            f"{self.source_path!r} — {self.detail}"
        )


def _identity_of(source: dict[str, Any]) -> str:
    """The identity a source is presented under: its declared
    identity when the presentation declares one, else its path."""
    declared = source.get("declared_identity")
    if isinstance(declared, str) and declared.strip():
        return declared.strip()
    return str(source.get("path", ""))


def _asserts_independence(source: dict[str, Any]) -> bool:
    return bool(source.get("independence_asserted")) or (
        source.get("presented_as") == "independent-corroboration"
    )


def scan_presentation(presentation: dict[str, Any]) -> list[ContaminationFlag]:
    """Run the six detectors over one intake presentation."""
    pid = str(presentation.get("id", "<unnamed>"))
    subject_lineage = presentation.get("subject_lineage")
    sources = [
        s for s in (presentation.get("sources") or []) if isinstance(s, dict)
    ]
    flags: list[ContaminationFlag] = []

    for source in sources:
        path = str(source.get("path", ""))
        kind = source.get("kind")
        lineage = source.get("lineage")
        same_lineage = (
            lineage is not None
            and subject_lineage is not None
            and lineage == subject_lineage
        )
        independent = _asserts_independence(source)

        # S4 / S1 — independence asserted for material that derives
        # from the very lineage it is presented as supporting. A
        # derived *result* is S4; a derived *value* (data carried
        # in a corpus, reading column, dataset or record) is S1.
        if independent and same_lineage:
            if kind == "result":
                flags.append(ContaminationFlag(
                    "S4", pid, path,
                    "a derived result (lineage "
                    f"{lineage!r}, the subject's own) is presented "
                    "as independent confirmation",
                ))
            else:
                flags.append(ContaminationFlag(
                    "S1", pid, path,
                    "a value derived from lineage "
                    f"{lineage!r} (the subject's own) is labelled "
                    "independent",
                ))

        # S2 — content the program produced, attributed by the
        # presentation to an external authority: the derivative
        # labels itself as source data.
        attributed_to = source.get("attributed_to")
        if (
            source.get("produced_by") == "program"
            and isinstance(attributed_to, str)
            and attributed_to.strip()
            and attributed_to.strip().lower() not in _PROGRAM_IDENTITIES
        ):
            flags.append(ContaminationFlag(
                "S2", pid, path,
                "content produced by the program is attributed to "
                f"{attributed_to.strip()!r}: a self-labelling "
                "derivative presented as source data",
            ))

        # S3 — a reading/translation column treated as corpus data.
        if kind in _READING_KINDS and source.get("presented_as") == "corpus-data":
            flags.append(ContaminationFlag(
                "S3", pid, path,
                f"a {kind} is presented as corpus data",
            ))

        # S6 — a summary or delivery standing in for the record.
        if kind in _SUMMARY_KINDS and (
            source.get("role") == "source_of_record"
            or source.get("presented_as") == "underlying-record"
        ):
            flags.append(ContaminationFlag(
                "S6", pid, path,
                f"a {kind} is cited as the underlying record "
                "(role source_of_record / presented as the record)",
            ))

    # S5 — the same data under two source identities: either the
    # same content pin carried under two identities, or two
    # dataset sources sharing one lineage root (one accumulated
    # work product) under two dataset identities.
    for i, a in enumerate(sources):
        for b in sources[i + 1:]:
            id_a, id_b = _identity_of(a), _identity_of(b)
            if id_a == id_b:
                continue
            pin_a, pin_b = a.get("sha256"), b.get("sha256")
            if pin_a and pin_b and pin_a == pin_b:
                flags.append(ContaminationFlag(
                    "S5", pid, str(b.get("path", "")),
                    "the same content pin is carried under two "
                    f"source identities ({id_a!r} and {id_b!r})",
                ))
                continue
            if (
                a.get("kind") == "dataset"
                and b.get("kind") == "dataset"
                and a.get("lineage") is not None
                and a.get("lineage") == b.get("lineage")
            ):
                flags.append(ContaminationFlag(
                    "S5", pid, str(b.get("path", "")),
                    "two dataset identities "
                    f"({id_a!r} and {id_b!r}) name one lineage "
                    f"root ({a.get('lineage')!r}): the same data "
                    "under two source identities",
                ))
    return flags


def scan_presentations(
    presentations: Iterable[dict[str, Any]],
) -> list[ContaminationFlag]:
    flags: list[ContaminationFlag] = []
    for presentation in presentations:
        flags.extend(scan_presentation(presentation))
    return flags


def presentation_from_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """The minimal presentation a ledger entry itself carries.

    Only what the entry states: its sources' paths, roles and
    content pins. Provenance facts the entry does not carry stay
    unset, so detectors keyed on them do not fire — the live scan
    certifies the ledger as it stands, and the class's teeth are
    exercised at intake and on the fixtures.
    """
    sources = []
    for source in entry.get("sources") or []:
        if not isinstance(source, dict):
            continue
        sources.append({
            "path": source.get("path", ""),
            "role": source.get("role"),
            "sha256": source.get("sha256"),
            "declared_identity": source.get("path", ""),
        })
    return {"id": str(entry.get("id", "<unnamed>")), "sources": sources}


def scan_ledger(root: Path) -> tuple[int, list[ContaminationFlag]]:
    """Scan every ledger entry's own presentation, plus the S5
    content-pin check across the whole ledger (one pin carried
    under two distinct paths anywhere is S5, whatever entry cites
    it). Returns (entries scanned, flags)."""
    from glossa_lab import ledger_intake as li

    entries = li.read_ledger(root / "glossa-indus" / "ledger" / "claims.jsonl")
    flags = scan_presentations(presentation_from_entry(e) for e in entries)

    by_pin: dict[str, set[str]] = {}
    for entry in entries:
        for source in entry.get("sources") or []:
            if isinstance(source, dict) and source.get("sha256"):
                by_pin.setdefault(source["sha256"], set()).add(
                    str(source.get("path", ""))
                )
    for pin, paths in sorted(by_pin.items()):
        if len(paths) > 1:
            flags.append(ContaminationFlag(
                "S5", "<ledger-wide>",
                ", ".join(sorted(paths)),
                "one content pin is carried under two source "
                f"identities across the ledger (pin {pin[:12]}...)",
            ))
    return len(entries), flags


def render_scan(n_scanned: int, flags: list[ContaminationFlag]) -> str:
    """The class's own report block (never folded into the V1-V11
    summary, which is a cross-stage record)."""
    lines = [
        "contamination class (Spec 095 T301, C095-7): "
        f"{n_scanned} presentations scanned, {len(flags)} flag(s)",
    ]
    lines.extend(flag.render() for flag in flags)
    lines.append(
        "CONTAMINATION: PASS" if not flags else "CONTAMINATION: FLAGS RAISED"
    )
    return "\n".join(lines) + "\n"


__all__ = [
    "SHAPES",
    "SHAPE_NAMES",
    "ContaminationFlag",
    "scan_presentation",
    "scan_presentations",
    "presentation_from_entry",
    "scan_ledger",
    "render_scan",
]
