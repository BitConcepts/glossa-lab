"""Versioned phonotactic initial checker (repair WP2, successor to Phase 58).

What this module is
-------------------
This module replaces the initial-sound check in the old Phase 58 script
(``phase58_phonological_gap.py``). The old script had defects that made
its headline result meaningless:

* Its cleanup step kept only the characters in ``[^a-zāīūēō]``. That
  deleted every retroflex consonant (ṭ ḍ ṇ ḷ ṟ ṉ) before the check ran,
  so a reading such as "ṭa" became "a" and passed as vowel-initial. The
  prohibited-initial rule could never fire.
* Input it could not check at all (nothing left after cleanup) returned
  ``True``, i.e. PASS.
* Slash alternatives were collapsed to the first segment only.
* A separate matching helper in ``provenance_audit.py``
  (``normalize_reading``) stripped all diacritics, so ṭ and t, ḍ and d,
  ś/ṣ and s collapsed to the same string for matching.

This module fixes those defects by design:

* No character is ever deleted to make a reading checkable. A character
  outside the recognized inventory makes the affected alternative
  UNCHECKABLE, with the character named in the reason.
* Uncheckable input is reported as UNCHECKABLE, never as PASS, and it
  stays in the denominator in every aggregate this module produces.
* Slash alternatives are parsed and checked individually. Each
  alternative gets its own outcome.
* Parenthetical annotations (glosses) are recorded on the result, not
  silently dropped. The text inside the parentheses is not treated as
  part of the reading.

Unicode handling
----------------
Input is normalized to Unicode NFC before any check, then lowercased.
NFC means a composed character (for example ṭ, U+1E6D) and the same
character written as a base letter plus a combining mark (t + U+0323)
behave identically. Diacritics are never stripped: ṭ and t remain
different characters, as do ḍ/d, ṇ/n, ś/s and ṣ/s. Characters are never
removed, folded to plain ASCII, or replaced.

Recognized transliteration inventory
------------------------------------
The recognized characters are exactly:

* plain lower-case Latin letters ``a``-``z`` (upper-case input is
  lowercased before checking, so A-Z are accepted by that step), and
* the Latin Extended letters with the Dravidian diacritic set
  ṭ ḍ ṇ ḷ ṟ ṉ ṅ ñ ś ṣ ṁ ḥ, and
* the long vowels ā ī ū ē ō.

Any other character -- digits, punctuation other than the slash
separator and annotation parentheses, symbols such as ``*`` or ``?``,
letters outside the list above such as č or ṛ, and internal
whitespace -- is unrecognized and makes its alternative UNCHECKABLE.

Scope -- read this before using any result
------------------------------------------
Every result carries ``scope = "INITIALS-ONLY"``. This module checks
only the first character of each alternative against the declared
rules below. That is not a complete phonotactic assessment: it says
nothing about the rest of the reading, about syllable shape, about
final sounds, or about whether the reading is a real word in any
language. A PASS means only "this initial does not break a declared
rule that was enabled for this check". Reports must carry the scope
with the result and must never present an initials-only PASS or a
zero-violation count from this module as a full phonotactic verdict.

Declared rules only -- human dependency
---------------------------------------
The rule set is data (see ``RULES``): each rule has an id, a plain
description, and an enabled flag. This module demonstrates compliance
with the declared rules only. It cannot certify historical accuracy.
Which restrictions belong to the proposed historical language, and
which concern only later Tamil, is a question for a linguist's review
of the sources (the old script cites Krishnamurti 2003 for the
declared rule). That review is a named human dependency of the repair
program. Until it is done, no result from this module validates a
corpus claim.

Pure standard library only.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum

__all__ = [
    "PARSER_VERSION",
    "SCOPE",
    "SCOPE_NOTE",
    "RECOGNIZED_CHARACTERS",
    "FORBIDDEN_INITIALS",
    "Outcome",
    "CheckOutcome",
    "Rule",
    "RULES",
    "DEFAULT_RULES",
    "AlternativeResult",
    "ReadingResult",
    "AggregateResult",
    "check_reading",
    "assess_reading",
    "check_readings",
    "assess_readings",
    "summarize_results",
]

PARSER_VERSION = "phonotactics-v2.0.0"

SCOPE = "INITIALS-ONLY"
SCOPE_NOTE = (
    "Initials-only assessment: only the first character of each "
    "alternative was checked against the declared rules. This is not "
    "a complete phonotactic assessment."
)

# Recognized transliteration inventory. See the module docstring.
_DIACRITIC_LETTERS = "ṭḍṇḷṟṉṅñśṣṁḥ"
_LONG_VOWELS = "āīūēō"
RECOGNIZED_CHARACTERS = frozenset(
    "abcdefghijklmnopqrstuvwxyz" + _DIACRITIC_LETTERS + _LONG_VOWELS
)

# The declared prohibited initials, exactly as Phase 58 declared them:
# no word-initial retroflex consonants ṭ ḍ ṇ ḷ ṟ ṉ.
FORBIDDEN_INITIALS = frozenset("ṭḍṇḷṟṉ")

VOWELS = frozenset("aāiīuūeēoō")


class Outcome(str, Enum):
    """Outcome of one check. UNCHECKABLE is a real outcome, not a pass."""

    PASS = "PASS"
    VIOLATION = "VIOLATION"
    UNCHECKABLE = "UNCHECKABLE"


# Alias with a more explicit name for callers that prefer it.
CheckOutcome = Outcome


@dataclass(frozen=True)
class Rule:
    """One declared rule, as data.

    ``forbidden_initials`` is the set of first characters that break
    this rule. An empty set means the rule prohibits no initial (it is
    kept for declaration completeness and can never be violated).
    """

    id: str
    description: str
    enabled: bool = True
    forbidden_initials: tuple[str, ...] = ()


RULES: tuple[Rule, ...] = (
    Rule(
        id="prohibited-initial-retroflex",
        description=(
            "A reading may not begin with a retroflex consonant "
            "(ṭ, ḍ, ṇ, ḷ, ṟ, ṉ), as declared in Phase 58 after "
            "Krishnamurti 2003."
        ),
        enabled=True,
        forbidden_initials=tuple(sorted(FORBIDDEN_INITIALS)),
    ),
)
DEFAULT_RULES = RULES


@dataclass
class AlternativeResult:
    """The outcome for one slash alternative of one reading."""

    alternative: str
    normalized: str = ""
    outcome: Outcome = Outcome.UNCHECKABLE
    reasons: tuple[str, ...] = ()
    rules_checked: tuple[str, ...] = ()
    rules_violated: tuple[str, ...] = ()
    initial: str | None = None
    annotations: tuple[str, ...] = ()
    scope: str = SCOPE
    scope_note: str = SCOPE_NOTE
    parser_version: str = PARSER_VERSION

    def to_dict(self) -> dict:
        return {
            "alternative": self.alternative,
            "normalized": self.normalized,
            "outcome": self.outcome.value,
            "reasons": list(self.reasons),
            "rules_checked": list(self.rules_checked),
            "rules_violated": list(self.rules_violated),
            "initial": self.initial,
            "annotations": list(self.annotations),
            "scope": self.scope,
            "scope_note": self.scope_note,
            "parser_version": self.parser_version,
        }


@dataclass
class ReadingResult:
    """The outcome for one full input reading (all its alternatives)."""

    original: object
    alternatives: list[AlternativeResult] = field(default_factory=list)
    annotations: tuple[str, ...] = ()
    scope: str = SCOPE
    scope_note: str = SCOPE_NOTE
    parser_version: str = PARSER_VERSION

    @property
    def outcome(self) -> Outcome:
        if any(a.outcome is Outcome.VIOLATION for a in self.alternatives):
            return Outcome.VIOLATION
        if any(a.outcome is Outcome.UNCHECKABLE for a in self.alternatives):
            return Outcome.UNCHECKABLE
        if self.alternatives and all(
            a.outcome is Outcome.PASS for a in self.alternatives
        ):
            return Outcome.PASS
        return Outcome.UNCHECKABLE

    def to_dict(self) -> dict:
        return {
            "original": self.original if isinstance(self.original, str) else repr(self.original),
            "outcome": self.outcome.value,
            "alternatives": [a.to_dict() for a in self.alternatives],
            "annotations": list(self.annotations),
            "scope": self.scope,
            "scope_note": self.scope_note,
            "parser_version": self.parser_version,
        }


@dataclass
class AggregateResult:
    """Denominator-preserving totals over a set of readings.

    Counts are per alternative, because alternatives are checked
    individually. ``checked`` is PASS + VIOLATION only; UNCHECKABLE
    items are counted separately and are never folded into PASS.
    """

    n_readings: int = 0
    total: int = 0
    checked: int = 0
    passed: int = 0
    violations: int = 0
    uncheckable: int = 0
    results: list[ReadingResult] = field(default_factory=list)
    scope: str = SCOPE
    scope_note: str = SCOPE_NOTE
    parser_version: str = PARSER_VERSION

    def to_dict(self) -> dict:
        return {
            "n_readings": self.n_readings,
            "total": self.total,
            "checked": self.checked,
            "passed": self.passed,
            "violations": self.violations,
            "uncheckable": self.uncheckable,
            "scope": self.scope,
            "scope_note": self.scope_note,
            "parser_version": self.parser_version,
            "results": [r.to_dict() for r in self.results],
        }


_ANNOTATION_RE = re.compile(r"\(([^()]*)\)")


def _extract_annotations(text: str) -> tuple[str, tuple[str, ...], str | None]:
    """Remove parenthetical annotations, recording their contents.

    Returns (remaining_text, annotations, malformed_reason_or_None).
    """
    annotations: list[str] = []

    def _record(match: re.Match) -> str:
        annotations.append(match.group(1).strip())
        return " "

    remaining = _ANNOTATION_RE.sub(_record, text)
    if "(" in remaining or ")" in remaining:
        return remaining, tuple(annotations), (
            "malformed annotation: parentheses are not balanced"
        )
    if any(a == "" for a in annotations):
        return remaining, tuple(annotations), (
            "malformed annotation: empty parenthetical annotation"
        )
    return remaining, tuple(annotations), None


def _check_alternative(
    segment: str,
    annotations: tuple[str, ...],
    rules: tuple[Rule, ...],
) -> AlternativeResult:
    original_segment = segment
    segment = segment.strip()
    if not segment:
        return AlternativeResult(
            alternative=original_segment,
            normalized="",
            outcome=Outcome.UNCHECKABLE,
            reasons=("empty alternative (malformed slash separation or empty input)",),
            annotations=annotations,
        )

    normalized = segment.lower()
    unrecognized: list[str] = []
    for ch in normalized:
        if ch not in RECOGNIZED_CHARACTERS and ch not in unrecognized:
            unrecognized.append(ch)
    if unrecognized:
        named = ", ".join(repr(c) for c in unrecognized)
        return AlternativeResult(
            alternative=original_segment,
            normalized=normalized,
            outcome=Outcome.UNCHECKABLE,
            reasons=(
                f"unrecognized character(s): {named}; no character is "
                "deleted or substituted, so this alternative cannot be checked",
            ),
            annotations=annotations,
        )

    initial = normalized[0]
    enabled_rules = tuple(r for r in rules if r.enabled)
    violated = tuple(
        r.id for r in enabled_rules if initial in r.forbidden_initials
    )
    checked_ids = tuple(r.id for r in enabled_rules)
    if violated:
        return AlternativeResult(
            alternative=original_segment,
            normalized=normalized,
            outcome=Outcome.VIOLATION,
            reasons=(
                f"initial {initial!r} is prohibited by declared rule(s): "
                + ", ".join(violated),
            ),
            rules_checked=checked_ids,
            rules_violated=violated,
            initial=initial,
            annotations=annotations,
        )
    return AlternativeResult(
        alternative=original_segment,
        normalized=normalized,
        outcome=Outcome.PASS,
        reasons=(
            f"initial {initial!r} is not prohibited by the declared "
            "rule(s) checked; this passes only the specified rule(s), "
            "within the initials-only scope",
        ),
        rules_checked=checked_ids,
        rules_violated=(),
        initial=initial,
        annotations=annotations,
    )


def check_reading(
    reading: object,
    rules: tuple[Rule, ...] | None = None,
) -> ReadingResult:
    """Check one reading against the declared rules.

    Slash alternatives are checked individually. The result is never a
    bare boolean: every alternative carries PASS, VIOLATION, or
    UNCHECKABLE with reasons, plus the initials-only scope.
    """
    active_rules = RULES if rules is None else tuple(rules)

    if not isinstance(reading, str):
        alt = AlternativeResult(
            alternative="",
            normalized="",
            outcome=Outcome.UNCHECKABLE,
            reasons=(f"input is not text (got {type(reading).__name__})",),
        )
        return ReadingResult(original=reading, alternatives=[alt])

    # NFC first, so composed and decomposed forms behave identically.
    nfc_text = unicodedata.normalize("NFC", reading)
    remaining, annotations, malformed = _extract_annotations(nfc_text)
    if malformed is not None:
        alt = AlternativeResult(
            alternative=reading,
            normalized=unicodedata.normalize("NFC", remaining).strip().lower(),
            outcome=Outcome.UNCHECKABLE,
            reasons=(malformed,),
            annotations=annotations,
        )
        return ReadingResult(
            original=reading, alternatives=[alt], annotations=annotations
        )

    if not remaining.strip():
        reason = (
            "annotation-only input: no checkable reading remains after "
            "the recorded annotation(s) are removed"
            if annotations
            else "empty input: no checkable reading"
        )
        alt = AlternativeResult(
            alternative=reading,
            normalized="",
            outcome=Outcome.UNCHECKABLE,
            reasons=(reason,),
            annotations=annotations,
        )
        return ReadingResult(
            original=reading, alternatives=[alt], annotations=annotations
        )

    alternatives = [
        _check_alternative(segment, annotations, active_rules)
        for segment in remaining.split("/")
    ]
    return ReadingResult(
        original=reading, alternatives=alternatives, annotations=annotations
    )


assess_reading = check_reading


def check_readings(
    readings,
    rules: tuple[Rule, ...] | None = None,
) -> AggregateResult:
    """Check many readings and report every part of the denominator."""
    results = [check_reading(r, rules=rules) for r in readings]
    total = passed = violations = uncheckable = 0
    for result in results:
        for alt in result.alternatives:
            total += 1
            if alt.outcome is Outcome.PASS:
                passed += 1
            elif alt.outcome is Outcome.VIOLATION:
                violations += 1
            else:
                uncheckable += 1
    return AggregateResult(
        n_readings=len(results),
        total=total,
        checked=passed + violations,
        passed=passed,
        violations=violations,
        uncheckable=uncheckable,
        results=results,
    )


assess_readings = check_readings
summarize_results = check_readings
