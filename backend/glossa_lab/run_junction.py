"""Spec 089 Stage 3 — the junction tool (T301, T303).

The comparator of **run-defs v1**
(`glossa-indus/ledger/RUN-DEFINITIONS.md`) §6: two run
records from one store, compared mechanically — the
component-by-component key diff (constitutive components
marked, D-089-4), the environment diff, the first
divergent output localized by recursive descent over the
outcome blocks, and exactly one disposition from the
registered vocabulary. The junction analysis is a
standalone tool (D-089-2): the gate (Stage 5) verifies
analyses, it never originates them, and this tool
originates no explanation beyond the registered
mechanical cases — the narrow shape case of run-defs §6
and the presentation case below. Every other explanation
is an adjudication act recorded in the run index by a
named actor.

Structure, following `run_records.py`: the comparator
(`compare_sides`) is PURE — it computes over two loaded
sides and writes nothing. The store layer beneath it
(`load_side`, `analyze_pair`, `scan_store`, `adjudicate`)
is the thin write surface: it reads the store's records,
writes junction reports into the junction store
(`glossa-indus/ledger/junctions/`, reports immutable),
and appends index acts through
`run_records.append_act` — so the fold's refusals bind
this tool exactly as they bind every writer (run-defs
v1 §7.1). The quarantine act is the only index write the
tool makes; adjudication acts are appended only by the
CLI's `adjudicate` command, on a named actor's ruling.

Dispositions, in the registered order (plan.md Stage 3):

1. a constitutive key difference (or a constitutive
   component either key cannot produce — a legacy,
   key-partial side) → `not-comparable`: the pair is
   different experiments, with the differing components
   named (C089-10). No report is written and no act is
   appended: the pair is refused as a junction.
2. outcome blocks equal → the pair is **identical**:
   listed as such, no report. The one exception: where a
   *presentation* of the pair asserted a divergence the
   records do not carry, and both stored records are
   byte-stable on re-read, the disposition is
   `identical-after-all` and a report IS written naming
   the presentation artifact (run-defs §6; the
   presentation-artifact check of plan.md Stage 3).
3. divergence wholly inside a registered nondeterminism
   shape for the pair's surface → `explained-by-named-
   difference`, citing the shape and the divergent
   lines, with the shape's evidence itemized. A shape
   whose evidence is absent does not explain: the
   matcher returns its reasons and the pair falls
   through to unexplained.
4. otherwise → `unexplained`: the report carries the
   red-team section (the six registered candidate
   causes, each pre-filled with the mechanical evidence
   that bears on it and the question the red team must
   answer; the sustained / not-sustained markings are
   completed by the red-team act, not by this tool),
   and both runs are quarantined by index act
   (C089-13, C089-14).

Standing position: the Indus script is not deciphered.
Nothing here is a decipherment claim; a junction
certifies what two executions recorded and how their
records differ, never that a presentation of either was
honest (C089-20) — junction machinery never ingests
deliveries (run-defs v1 §8).
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from glossa_lab import run_records as rr

#: The junction store, repo-relative (plan.md Stage 3).
JUNCTIONS_REL = "glossa-indus/ledger/junctions"

#: The default run store the CLI reads (the settling
#: store of record; other stores are named by --store).
RUNS_REL = "glossa-indus/ledger/runs"

#: The divergence cap, following `_first_divergences`'
#: precedent in `tools/ledger/run_settling.py`.
DIVERGENCE_LIMIT = 8

#: The registered candidate causes of the red-team
#: section (claims.md C089-14), in registered order.
RED_TEAM_CAUSES = (
    "input drift",
    "code drift",
    "environment drift",
    "nondeterminism",
    "record corruption",
    "presentation artifact",
)

_RED_TEAM_QUESTIONS = {
    "input drift": (
        "Did any input the comparability key does not pin "
        "change between the two executions?"
    ),
    "code drift": (
        "Does the code-version difference, where one "
        "exists, touch the code path that produced the "
        "divergent output?"
    ),
    "environment drift": (
        "Does the environment difference, where one "
        "exists, plausibly reach the divergent output "
        "(venue, runtime, dependency set)?"
    ),
    "nondeterminism": (
        "Is the divergence inside a nondeterminism shape "
        "nobody has registered — and if so, is registering "
        "it the right act, or is it a defect wearing a "
        "shape's clothes?"
    ),
    "record corruption": (
        "Is either stored record other than what its "
        "execution wrote (bytes unstable, content failing "
        "validation, provenance broken)?"
    ),
    "presentation artifact": (
        "Was the divergence ever in the records, or only "
        "in a presentation of them (a summary, a delivery, "
        "a dashboard)?"
    ),
}


def tool_version() -> str:
    """The junction tool's version, from the installed
    package metadata — pyproject.toml is the version's
    one home (governance H10). "unknown" where the
    metadata is unavailable; recorded, never invented."""
    try:
        return importlib.metadata.version("glossa-lab")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def junctions_path(root: Path) -> Path:
    """The junction store under a repo root."""
    return Path(root) / JUNCTIONS_REL


# ---------------------------------------------------------------------------
# Outcome equality and the divergence localizer (pure)


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False
    ).encode("utf-8")


def _outcomes_equal(side_a: dict[str, Any], side_b: dict[str, Any]) -> bool:
    return (
        side_a["outcome_kind"] == side_b["outcome_kind"]
        and _canonical(side_a["outcome"])
        == _canonical(side_b["outcome"])
    )


def _first_divergences(a: Any, b: Any, path: str, out: list[str],
                       limit: int = DIVERGENCE_LIMIT) -> None:
    """Localize the first divergences between two outcome
    blocks by recursive descent — the `_first_divergences`
    discipline of `run_settling.py` generalized from
    expectation-vs-run to run-vs-run: same path format
    (`path.key`, `path[i]`), same cap. Run A is the first
    record named, run B the second."""
    if isinstance(a, dict) and isinstance(b, dict):
        for key in a:
            if key not in b:
                out.append(f"{path}.{key}: missing in run B")
            else:
                _first_divergences(
                    a[key], b[key], f"{path}.{key}", out, limit
                )
            if len(out) >= limit:
                return
        for key in b:
            if key not in a:
                out.append(f"{path}.{key}: unexpected in run B")
            if len(out) >= limit:
                return
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(
                f"{path}: length {len(b)} in run B, "
                f"length {len(a)} in run A"
            )
        for i, (a_item, b_item) in enumerate(zip(a, b)):
            _first_divergences(
                a_item, b_item, f"{path}[{i}]", out, limit
            )
            if len(out) >= limit:
                return
    elif a != b:
        out.append(f"{path}: {b!r} in run B, {a!r} in run A")


def _first_present(value: Any, path: str) -> tuple[str, Any]:
    """The first result a non-empty side produced: the
    depth-first first scalar of its result block (dict
    keys in recorded order, list items in index order);
    an empty container is its own first present value."""
    if isinstance(value, dict):
        for key, item in value.items():
            return _first_present(item, f"{path}.{key}")
        return path, value
    if isinstance(value, list):
        for i, item in enumerate(value):
            return _first_present(item, f"{path}[{i}]")
        return path, value
    return path, value


def _outcome_divergences(side_a: dict[str, Any],
                         side_b: dict[str, Any]) -> list[str]:
    """The localized divergences between two outcome
    blocks, incl. the one-side-empty case (C089-11):
    where one side recorded an absence and the other a
    result, the first divergence is the first result the
    non-empty side produced."""
    if side_a["outcome_kind"] == side_b["outcome_kind"]:
        out: list[str] = []
        _first_divergences(
            side_a["outcome"], side_b["outcome"],
            side_a["outcome_kind"], out,
        )
        return out
    if side_a["outcome_kind"] == "result":
        result_side, absence_side = side_a, side_b
        result_label, absence_label = "A", "B"
    else:
        result_side, absence_side = side_b, side_a
        result_label, absence_label = "B", "A"
    absence = absence_side["outcome"]
    first_path, first_value = _first_present(
        result_side["outcome"], "result"
    )
    return [
        f"outcome: run {absence_label} recorded an absence "
        f"({absence['kind']}: {absence['detail']}); "
        f"run {result_label} recorded a result",
        f"{first_path}: {first_value!r} — the first result "
        f"present in run {result_label}, absent in run "
        f"{absence_label}",
    ]


# ---------------------------------------------------------------------------
# The key diff and the environment diff (pure)


def key_diff(key_a: dict[str, Any],
             key_b: dict[str, Any]) -> list[dict[str, Any]]:
    """The component-by-component key diff (C089-12):
    every registered run-key v1 component, constitutive
    components marked. A component absent from either
    key (a legacy, key-partial side) is `unrecoverable`
    — named, never silently agreed. `input_pins` is
    diffed by divergent sub-paths rather than dumped:
    the pins are the evidence, and the divergent lines
    are the diff."""
    out: list[dict[str, Any]] = []
    for component in rr.KEY_COMPONENTS:
        entry: dict[str, Any] = {
            "component": component,
            "constitutive": component in rr.CONSTITUTIVE_COMPONENTS,
        }
        if component not in key_a or component not in key_b:
            entry["status"] = "unrecoverable"
            entry["detail"] = (
                "absent from "
                + (
                    "both keys"
                    if component not in key_a
                    and component not in key_b
                    else "one key"
                )
                + " — a legacy (key-partial) side cannot "
                "produce it (run-defs v1 §7.2)"
            )
        elif key_a[component] == key_b[component]:
            entry["status"] = "agree"
            if component != "input_pins":
                entry["value"] = key_a[component]
        else:
            entry["status"] = "differ"
            if component == "input_pins":
                paths: list[str] = []
                _first_divergences(
                    key_a[component], key_b[component],
                    "input_pins", paths, limit=4,
                )
                entry["divergent_paths"] = paths
            else:
                entry["a"] = key_a[component]
                entry["b"] = key_b[component]
        out.append(entry)
    return out


def _differing_constitutive(diff: list[dict[str, Any]]) -> list[str]:
    return [
        entry["component"]
        for entry in diff
        if entry["constitutive"] and entry["status"] != "agree"
    ]


def environment_diff(key_a: dict[str, Any],
                     key_b: dict[str, Any]) -> dict[str, Any]:
    """The environment stamps, diffed (C089-12): code
    version and environment class — the recorded-and-
    diffed components (D-089-4). A junction explains
    *with* these; they never break comparability."""
    out: dict[str, Any] = {}
    for component in ("code_version", "environment_class"):
        a_val, b_val = key_a.get(component), key_b.get(component)
        out[component] = {
            "a": a_val,
            "b": b_val,
            "differ": a_val != b_val,
        }
    return out


# ---------------------------------------------------------------------------
# Registered nondeterminism shapes (pure matchers)

#: The sqlite closed-database family, as recorded in the
#: registered instance (run-defs v1 §5).
_SQLITE_CLOSED_DATABASE_MARKERS = ("closed database", "sqlite")


def _is_tray_test_id(test_id: Any) -> bool:
    """A tray test id (run-defs v1 §5): the test's module
    is a tray module — the registered instance is
    `test_tray_token_auth.py::...`. The machine reading
    of "tray test ids": the module filename (the part
    before `::`, basename) contains `tray`."""
    if not isinstance(test_id, str) or "::" not in test_id:
        return False
    module = test_id.split("::", 1)[0].replace("\\", "/")
    return "tray" in module.rsplit("/", 1)[-1]


def _error_entry_key(entry: Any) -> Any:
    if isinstance(entry, dict):
        return (
            entry.get("test_id"),
            entry.get("phase"),
            entry.get("error"),
        )
    return entry


def match_tray_teardown_flake(
    side_a: dict[str, Any], side_b: dict[str, Any],
    divergences: list[str],
) -> tuple[bool, list[str], list[str]]:
    """Suite shape #1 — the tray teardown flake (run-defs
    v1 §5), the registered mechanical explained case.
    Returns (matched, evidence, reasons): matched only
    when EVERY element of the registered shape is present
    in the records — the divergence confined to teardown
    ERROR entries of the sqlite closed-database family on
    tray test ids, with the runs' pass and fail counts
    otherwise equal. A missing element is a named reason,
    and the shape does not explain: an explained
    classification is never asserted without its
    evidence (the shape's evidence bar)."""
    evidence: list[str] = []
    reasons: list[str] = []
    shape_ref = (
        "run-defs v1 §5, suite nondeterminism shape #1 "
        "(tray-teardown-flake)"
    )
    if side_a["outcome_kind"] != "result" or (
        side_b["outcome_kind"] != "result"
    ):
        return False, evidence, [
            "one side recorded no result block; the shape "
            "is stated over suite result summaries"
        ]
    result_a, result_b = side_a["outcome"], side_b["outcome"]
    for label, result in (("run A", result_a), ("run B", result_b)):
        if not isinstance(result, dict) or not isinstance(
            result.get("summary"), dict
        ):
            return False, evidence, [
                f"{label}'s result block carries no summary "
                "object — the shape's counts cannot be read "
                "from the record"
            ]
        summary = result["summary"]
        for count in ("passed", "failed"):
            if not isinstance(summary.get(count), int):
                return False, evidence, [
                    f"{label}'s summary carries no integer "
                    f"{count!r} count — the shape's counts "
                    "cannot be read from the record"
                ]
        if not isinstance(result.get("errors", []), list) or not (
            isinstance(result.get("failures", []), list)
        ):
            return False, evidence, [
                f"{label}'s result block carries non-list "
                "failures/errors — the shape's confinement "
                "cannot be checked from the record"
            ]
    summary_a, summary_b = result_a["summary"], result_b["summary"]
    if summary_a.get("passed") != summary_b.get("passed"):
        reasons.append(
            f"pass counts differ ({summary_a.get('passed')} "
            f"in run A, {summary_b.get('passed')} in run B) "
            "— outside the shape, which requires them equal"
        )
    else:
        evidence.append(
            f"pass counts equal: {summary_a['passed']} in "
            "both runs"
        )
    if summary_a.get("failed") != summary_b.get("failed"):
        reasons.append(
            f"fail counts differ ({summary_a.get('failed')} "
            f"in run A, {summary_b.get('failed')} in run B) "
            "— outside the shape, which requires them equal"
        )
    else:
        evidence.append(
            f"fail counts equal: {summary_a['failed']} in "
            "both runs"
        )
    failures_a = sorted(result_a.get("failures", []))
    failures_b = sorted(result_b.get("failures", []))
    if failures_a != failures_b:
        reasons.append(
            "the failure lists differ — a divergence "
            "outside the teardown ERROR entries"
        )
    else:
        evidence.append(
            "failure lists identical "
            f"({len(failures_a)} failure(s) in both runs)"
        )
    for count in sorted(
        (set(summary_a) | set(summary_b)) - {"errors"}
    ):
        if count in ("passed", "failed"):
            continue
        if summary_a.get(count) != summary_b.get(count):
            reasons.append(
                f"summary count {count!r} differs "
                f"({summary_a.get(count)!r} in run A, "
                f"{summary_b.get(count)!r} in run B) — "
                "outside the shape's confinement"
            )
    errors_a = [_error_entry_key(e) for e in result_a.get("errors", [])]
    errors_b = [_error_entry_key(e) for e in result_b.get("errors", [])]
    only_a = [k for k in errors_a if k not in errors_b]
    only_b = [k for k in errors_b if k not in errors_a]
    differing = only_a + only_b
    if not differing:
        reasons.append(
            "the error entries do not differ — the "
            "divergence lies elsewhere in the result blocks"
        )
    for test_id, phase, error in differing:
        label = f"error entry {test_id!r}"
        if phase != "teardown":
            reasons.append(
                f"{label} is a {phase!r} error, not a "
                "teardown error — outside the shape"
            )
        if not _is_tray_test_id(test_id):
            reasons.append(
                f"{label} is not a tray test id — outside "
                "the shape"
            )
        if not isinstance(error, str) or not any(
            marker in error
            for marker in _SQLITE_CLOSED_DATABASE_MARKERS
        ):
            reasons.append(
                f"{label} carries no sqlite closed-database "
                f"error text (recorded: {error!r}) — the "
                "shape's family evidence is absent"
            )
        if (
            phase == "teardown"
            and _is_tray_test_id(test_id)
            and isinstance(error, str)
            and any(
                marker in error
                for marker in _SQLITE_CLOSED_DATABASE_MARKERS
            )
        ):
            evidence.append(
                f"{label}: teardown ERROR, sqlite "
                f"closed-database family, tray test id — "
                f"recorded error: {error}"
            )
    if summary_a.get("errors") is not None and (
        summary_b.get("errors") is not None
    ):
        delta = abs(summary_a["errors"] - summary_b["errors"])
        if delta != len(differing):
            reasons.append(
                f"the summary error counts differ by "
                f"{delta} but {len(differing)} error "
                "entries differ — the divergence is not "
                "confined to the differing entries"
            )
        else:
            evidence.append(
                f"summary error counts differ by exactly "
                f"the {len(differing)} differing entr"
                f"{'y' if len(differing) == 1 else 'ies'}"
            )
    if reasons:
        return False, evidence, reasons
    evidence.insert(
        0,
        f"shape consulted: {shape_ref} — every element "
        "of the registered shape is present in the "
        "records",
    )
    return True, evidence, reasons


#: The registered shape matchers, by shape name. A shape
#: with no matcher here is not mechanically explainable
#: by this tool (the adjudication path remains).
_SHAPE_MATCHERS = {
    "tray-teardown-flake": match_tray_teardown_flake,
}


def _consult_shapes(
    side_a: dict[str, Any], side_b: dict[str, Any],
    divergences: list[str],
) -> tuple[Optional[dict[str, Any]], list[str]]:
    """Consult the surface's registered nondeterminism
    shapes (run-defs v1 §5). Returns (shape_match,
    consultation lines): the match, when one shape's
    every element is present, else None plus the lines
    recording why each consulted shape did not explain —
    the red-team section's nondeterminism evidence."""
    surface = side_a["surface"]
    registered = rr.SURFACES.get(surface, {}).get(
        "nondeterminism_shapes", ()
    )
    lines: list[str] = []
    for shape in registered:
        matcher = _SHAPE_MATCHERS.get(shape)
        if matcher is None:
            lines.append(
                f"shape {shape!r}: registered for surface "
                f"{surface!r} but no mechanical matcher is "
                "registered in run-defs v1's machine copy "
                "— not mechanically explainable by this "
                "tool"
            )
            continue
        matched, evidence, reasons = matcher(
            side_a, side_b, divergences
        )
        if matched:
            return {
                "shape": shape,
                "shape_ref": (
                    "run-defs v1 §5 (suite shape #1)"
                    if shape == "tray-teardown-flake"
                    else "run-defs v1 §5"
                ),
                "evidence": evidence,
                "divergent_lines": list(divergences),
            }, lines
        lines.append(
            f"shape {shape!r} consulted: not matched — "
            + "; ".join(reasons)
        )
    return None, lines


# ---------------------------------------------------------------------------
# The red-team section (pure builder)


def _red_team_section(
    side_a: dict[str, Any], side_b: dict[str, Any],
    diff: list[dict[str, Any]],
    env: dict[str, Any],
    divergences: list[str],
    shape_lines: list[str],
    integrity: Optional[dict[str, Any]],
) -> dict[str, Any]:
    """The red-team section of an unexplained junction's
    report (C089-14): the six registered candidate
    causes, each pre-filled with the mechanical evidence
    that bears on it and the question the red team must
    answer. Every `marking` is None: the sustained /
    not-sustained markings are completed by the red-team
    act (an agent or human under the standing red-team
    practice), never by this tool (D-089-2)."""
    pins_entry = next(
        e for e in diff if e["component"] == "input_pins"
    )
    nondeterminism_evidence = [
        f"surface {side_a['surface']!r} is registered "
        f"{side_a['determinism_class']!r} (run-defs v1 §5)"
    ] + shape_lines
    if not shape_lines:
        nondeterminism_evidence.append(
            "no nondeterminism shape is registered for "
            "this surface — divergence on it is not "
            "explained by nondeterminism on any registered "
            "shape"
        )
    corruption: list[str] = []
    presentation: list[str] = []
    for label, side in (("A", side_a), ("B", side_b)):
        info = (integrity or {}).get(side["run_id"])
        if info is None:
            corruption.append(
                f"run {label} ({side['run_id']}): record "
                "supplied in memory; its stored bytes were "
                "not re-read by this analysis"
            )
        else:
            corruption.append(
                f"run {label} ({side['run_id']}): record "
                f"{info['record']}, sha256 "
                f"{info['sha256']}; byte-stable on re-read: "
                f"{info['byte_stable']}; parses and "
                "validates under run-defs v1 (the store "
                "layer refuses a record that does not)"
            )
    presentation.append(
        "the divergence is present in the stored records "
        f"themselves — first divergence: {divergences[0]} "
        "— so no presentation intervenes between the "
        "store and this analysis; a presentation-only "
        "divergence would have dispositioned "
        "identical-after-all"
    )
    evidence_by_cause = {
        "input drift": [
            "input pins agree on every component "
            f"(key diff for input_pins: {pins_entry['status']}) "
            "— the pair is comparable, so the pinned "
            "inputs are canonically identical; drift, if "
            "any, lives in an input the key does not pin"
        ],
        "code drift": [
            "code_version: "
            f"{env['code_version']['a']!r} (run A) vs "
            f"{env['code_version']['b']!r} (run B) — "
            + (
                "differs (recorded-and-diffed; a live "
                "candidate)"
                if env["code_version"]["differ"]
                else "identical"
            )
        ],
        "environment drift": [
            "environment_class: "
            f"{env['environment_class']['a']!r} (run A) vs "
            f"{env['environment_class']['b']!r} (run B) — "
            + (
                "differs (recorded-and-diffed; a live "
                "candidate)"
                if env["environment_class"]["differ"]
                else "identical"
            )
        ],
        "nondeterminism": nondeterminism_evidence,
        "record corruption": corruption,
        "presentation artifact": presentation,
    }
    return {
        "causes": [
            {
                "cause": cause,
                "question": _RED_TEAM_QUESTIONS[cause],
                "evidence": evidence_by_cause[cause],
                "marking": None,
            }
            for cause in RED_TEAM_CAUSES
        ],
        "note": (
            "The tool pre-fills the mechanical evidence "
            "only. Each cause's sustained / not-sustained "
            "marking is completed by the red-team act — a "
            "named agent or human working this junction "
            "under the standing red-team practice — and "
            "recorded as an adjudication act in the run "
            "index; this report is never edited (C089-14, "
            "D-089-2)."
        ),
    }


# ---------------------------------------------------------------------------
# The comparator (pure)


def compare_sides(
    side_a: dict[str, Any],
    side_b: dict[str, Any],
    *,
    presented_artifact: Optional[str] = None,
    integrity: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Compare two loaded run sides and return the
    junction analysis (pure: no writes, no junction id —
    the store layer mints and files). The analysis
    carries the disposition and every section a junction
    report is made of (C089-12). `presented_artifact`
    names a presentation of the pair that asserted a
    divergence; it is consulted only when the records
    themselves agree (the identical-after-all case).
    `integrity` is the store layer's per-run record
    integrity evidence, keyed by run id."""
    diff = key_diff(side_a["key"], side_b["key"])
    env = environment_diff(side_a["key"], side_b["key"])
    analysis: dict[str, Any] = {
        "runs": [
            {
                "run_id": side["run_id"],
                "record": side["record_name"],
                "record_sha256": side["record_sha256"],
                "key_partial": side["key_partial"],
            }
            for side in (side_a, side_b)
        ],
        "key_diff": diff,
        "environment_diff": env,
        "first_divergences": [],
    }
    differing = _differing_constitutive(diff)
    if differing:
        analysis["disposition"] = "not-comparable"
        analysis["differing_components"] = differing
        return analysis
    if _outcomes_equal(side_a, side_b):
        byte_stable = True
        if integrity is not None:
            byte_stable = all(
                info["byte_stable"]
                for info in integrity.values()
            )
        if presented_artifact is not None and byte_stable:
            analysis["disposition"] = "identical-after-all"
            analysis["presentation_artifact"] = presented_artifact
        else:
            analysis["disposition"] = "identical"
        return analysis
    divergences = _outcome_divergences(side_a, side_b)
    analysis["first_divergences"] = divergences
    shape_match, shape_lines = _consult_shapes(
        side_a, side_b, divergences
    )
    if shape_match is not None:
        analysis["disposition"] = "explained-by-named-difference"
        analysis["shape"] = shape_match
        return analysis
    analysis["disposition"] = "unexplained"
    analysis["red_team"] = _red_team_section(
        side_a, side_b, diff, env, divergences,
        shape_lines, integrity,
    )
    return analysis


# ---------------------------------------------------------------------------
# The store layer: sides, reports, acts (thin writes)


def _dump(data: dict[str, Any]) -> bytes:
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    return text.encode("utf-8")


def _write_verified(path: Path, payload: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    if path.read_bytes() != payload:
        raise rr.RunRecordError(
            f"junction report write failed verification: "
            f"{path} does not read back as written"
        )
    return path


def _side_from_record(
    run_id: str,
    entry: dict[str, Any],
    record: dict[str, Any],
    record_bytes: bytes,
) -> dict[str, Any]:
    """One loaded side of a junction: the record named by
    an index entry act, its key (the header's, or the
    entry's recoverable key for a legacy record), and its
    outcome block."""
    sha256 = hashlib.sha256(record_bytes).hexdigest()
    header = record.get("run")
    if isinstance(header, dict):
        rr.validate_record(record)
        key = header["key"]
        determinism = header["determinism_class"]
        key_partial = False
    elif entry.get("legacy"):
        key = entry["key"]
        determinism = rr.SURFACES[key["surface"]]["determinism"]
        key_partial = True
    else:
        raise rr.RunRecordError(
            f"record {entry['record']!r} for run {run_id!r} "
            "carries no run header and its index entry is "
            "not a legacy entry — not a junctionable record"
        )
    if "result" in record:
        outcome_kind, outcome = "result", record["result"]
    elif "absence" in record:
        outcome_kind, outcome = "absence", record["absence"]
    else:
        raise rr.RunRecordError(
            f"record {entry['record']!r} for run {run_id!r} "
            "carries neither a result block nor an absence "
            "block — not a junctionable record"
        )
    return {
        "run_id": run_id,
        "record_name": entry["record"],
        "record_sha256": sha256,
        "key": key,
        "key_partial": key_partial,
        "surface": key["surface"],
        "determinism_class": determinism,
        "outcome_kind": outcome_kind,
        "outcome": outcome,
    }


def load_side(store_dir: Path, state: rr.IndexState,
              run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load one run's side from a store, plus its record
    integrity evidence: the stored bytes' hash, and
    byte-stability on an immediate re-read (the
    presentation-artifact check of plan.md Stage 3 is
    made against the store itself). Refuses a run id
    with no entry act, and a record that fails run-defs
    validation — named, never worked around."""
    store = Path(store_dir)
    entry = state.entries.get(run_id)
    if entry is None:
        raise rr.RunRecordError(
            f"run id {run_id!r} has no entry act in the "
            f"index of store {store} — unknown to this "
            "store"
        )
    record_path = store / entry["record"]
    if not record_path.is_file():
        raise rr.RunRecordError(
            f"record {entry['record']!r} named by the "
            f"index entry for {run_id!r} is not in store "
            f"{store}"
        )
    payload = record_path.read_bytes()
    record = json.loads(payload.decode("utf-8"))
    side = _side_from_record(run_id, entry, record, payload)
    reread = record_path.read_bytes()
    integrity = {
        "record": entry["record"],
        "sha256": side["record_sha256"],
        "byte_stable": reread == payload,
    }
    return side, integrity


def write_report(junctions_dir: Path,
                 report: dict[str, Any]) -> Path:
    """Write one junction report into the junction
    store. Reports are immutable: a target that already
    exists refuses — a re-analysis is a new report under
    a new junction id naming the same pair, never an
    edit."""
    target = Path(junctions_dir) / f"{report['junction_id']}.json"
    if target.exists():
        raise rr.RunRecordError(
            f"junction report write refused: {target} "
            "already exists — reports are immutable, a "
            "re-analysis mints a new junction id"
        )
    return _write_verified(target, _dump(report))


def _build_report(analysis: dict[str, Any], junction_id: str,
                  now: datetime) -> dict[str, Any]:
    report: dict[str, Any] = {
        "junction_id": junction_id,
        "kind": "junction report",
        "run_defs": rr.RUN_DEFS_VERSION,
        "tool": "run_junction.py",
        "tool_version": tool_version(),
        "created": rr.iso_stamp(now),
        "runs": analysis["runs"],
        "key_diff": analysis["key_diff"],
        "environment_diff": analysis["environment_diff"],
        "first_divergences": analysis["first_divergences"],
        "disposition": analysis["disposition"],
    }
    for section in ("shape", "presentation_artifact"):
        if section in analysis:
            report[section] = analysis[section]
    if "red_team" in analysis:
        red_team = dict(analysis["red_team"])
        red_team["junction_id"] = junction_id
        report["red_team"] = red_team
    return report


def analyze_pair(
    store_dir: Path,
    junctions_dir: Path,
    run_id_a: str,
    run_id_b: str,
    *,
    presented_artifact: Optional[str] = None,
    now: Optional[datetime] = None,
) -> dict[str, Any]:
    """Analyze one pair in a store, with the tool's
    write consequences (plan.md Stage 3):

    - identical / not-comparable: nothing is written,
      no act is appended;
    - explained-by-named-difference / identical-after-
      all: the junction report is filed in the junction
      store;
    - unexplained: the report is filed AND a
      `quarantine` act naming both runs is appended to
      the store's index (through
      `run_records.append_act`, so the fold's refusals
      bind). While that quarantine stands open, neither
      run's results may be cited as verdict support
      (C089-13); lifting or confirming it is an
      adjudication act, never an edit.

    Returns the outcome: the analysis plus `junction_id`
    and `report_path` where a report was filed, and
    `quarantined` where the act was appended."""
    if run_id_a == run_id_b:
        raise rr.RunRecordError(
            f"a run is not a junction pair with itself: "
            f"{run_id_a!r}"
        )
    store = Path(store_dir)
    index_path = store / "run-index.jsonl"
    state = rr.fold_index(index_path)
    side_a, integrity_a = load_side(store, state, run_id_a)
    side_b, integrity_b = load_side(store, state, run_id_b)
    integrity = {run_id_a: integrity_a, run_id_b: integrity_b}
    analysis = compare_sides(
        side_a, side_b,
        presented_artifact=presented_artifact,
        integrity=integrity,
    )
    outcome: dict[str, Any] = dict(analysis)
    outcome["junction_id"] = None
    outcome["report_path"] = None
    outcome["quarantined"] = False
    if analysis["disposition"] in (
        "identical", "not-comparable",
    ):
        return outcome
    moment = now or datetime.now(timezone.utc)
    junction_id = rr.mint_junction_id(now=moment)
    report = _build_report(analysis, junction_id, moment)
    path = write_report(junctions_dir, report)
    outcome["junction_id"] = junction_id
    outcome["report_path"] = str(path)
    if analysis["disposition"] == "unexplained":
        rr.append_act(
            index_path,
            {
                "act": "quarantine",
                "junction_id": junction_id,
                "run_ids": [run_id_a, run_id_b],
            },
        )
        outcome["quarantined"] = True
    return outcome


def comparable_pairs(
    state: rr.IndexState,
    *,
    only_run_id: Optional[str] = None,
) -> tuple[list[tuple[str, str]], list[dict[str, Any]]]:
    """The store's comparable pairs from its folded
    index, and the pairs skipped with their reason.
    Comparability is decided by the keys alone (D-089-4,
    C089-10): complete keys, constitutive components in
    agreement. A legacy (key-partial) entry pairs with
    nothing — the components it cannot produce are
    constitutive, and a junction over unrecoverable
    components would rest on air (C089-17)."""
    pairs: list[tuple[str, str]] = []
    skipped: list[dict[str, Any]] = []
    all_ids = list(state.order)
    for i, run_id_a in enumerate(all_ids):
        for run_id_b in all_ids[i + 1:]:
            if only_run_id is not None and only_run_id not in (
                run_id_a, run_id_b,
            ):
                continue
            entry_a = state.entries[run_id_a]
            entry_b = state.entries[run_id_b]
            if entry_a.get("legacy") or entry_b.get("legacy"):
                skipped.append({
                    "runs": [run_id_a, run_id_b],
                    "reason": (
                        "a legacy (key-partial) side — its "
                        "unrecoverable components are "
                        "constitutive, so the pair's "
                        "comparability cannot be decided "
                        "from the keys"
                    ),
                })
                continue
            differing = _differing_constitutive(
                key_diff(entry_a["key"], entry_b["key"])
            )
            if differing:
                skipped.append({
                    "runs": [run_id_a, run_id_b],
                    "reason": (
                        "constitutive key components "
                        f"differ: {differing} — different "
                        "experiments (C089-10)"
                    ),
                })
                continue
            pairs.append((run_id_a, run_id_b))
    return pairs, skipped


def scan_store(
    store_dir: Path,
    junctions_dir: Path,
    *,
    only_run_id: Optional[str] = None,
    now: Optional[datetime] = None,
) -> dict[str, Any]:
    """Scan a store's index: every comparable pair is
    analyzed (identical pairs listed as such; triggering
    pairs reported + written, with quarantine acts on
    the unexplained). With `only_run_id`, only the pairs
    involving that run — the automatic trigger's form
    (T303): a scan of the new record against its
    comparable predecessors."""
    store = Path(store_dir)
    state = rr.fold_index(store / "run-index.jsonl")
    pairs, skipped = comparable_pairs(state, only_run_id=only_run_id)
    outcomes: list[dict[str, Any]] = []
    for run_id_a, run_id_b in pairs:
        outcomes.append(
            analyze_pair(
                store, junctions_dir, run_id_a, run_id_b,
                now=now,
            )
        )
    counts: dict[str, int] = {}
    for outcome in outcomes:
        counts[outcome["disposition"]] = (
            counts.get(outcome["disposition"], 0) + 1
        )
    return {
        "pairs": outcomes,
        "skipped": skipped,
        "counts": counts,
    }


def adjudicate(
    store_dir: Path,
    junction_id: str,
    *,
    ruling: str,
    actor: str,
    resulting_state: str,
) -> rr.IndexState:
    """Append the adjudication act for a junction
    (run-defs v1 §7.1): a named actor's ruling, lifting
    or confirming the junction's quarantine. The act is
    appended through `run_records.append_act`, so an
    adjudication naming a junction no quarantine act
    introduced refuses and the index is byte-unchanged
    by the refusal. The junction report and the run
    records are never edited."""
    if resulting_state not in rr.ADJUDICATION_STATES:
        raise rr.RunRecordError(
            f"resulting_state {resulting_state!r} is not "
            f"registered; the states are "
            f"{list(rr.ADJUDICATION_STATES)}"
        )
    for name, value in (("ruling", ruling), ("actor", actor)):
        if not isinstance(value, str) or not value:
            raise rr.RunRecordError(
                f"adjudication {name!r} must be a non-empty "
                "string — an adjudication is a named act "
                "by a named actor"
            )
    return rr.append_act(
        Path(store_dir) / "run-index.jsonl",
        {
            "act": "adjudication",
            "junction_id": junction_id,
            "ruling": ruling,
            "actor": actor,
            "resulting_state": resulting_state,
        },
    )


__all__ = [
    "DIVERGENCE_LIMIT",
    "JUNCTIONS_REL",
    "RED_TEAM_CAUSES",
    "RUNS_REL",
    "adjudicate",
    "analyze_pair",
    "comparable_pairs",
    "compare_sides",
    "environment_diff",
    "junctions_path",
    "key_diff",
    "load_side",
    "match_tray_teardown_flake",
    "scan_store",
    "tool_version",
    "write_report",
]
