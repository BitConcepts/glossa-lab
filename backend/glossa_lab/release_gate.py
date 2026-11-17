"""The composed release gate (Spec 095 Stage 4, T405; C095-14).

One gate of thirteen components of record:

    unit tests, integration tests, frontend tests, end-to-end
    tests, ledger validation, corpus identity verification,
    anchor regression, claim-stage validation, provenance
    completeness, security checks, accessibility checks,
    reproducibility smoke test, public-claims consistency.

Composition rules (C095-14):

- Every component's result is recorded per release candidate.
- A component either PASSes, FAILs, is NOT_RUN, or is EXCEPTED.
- Exceptions exist only as recorded owner-approved entries (see
  ``validate_exceptions`` for the required fields). An entry
  missing any required field is not an exception; it is ignored
  and the component keeps its own result.
- The candidate's verdict is PASS only when every component is
  PASS or EXCEPTED. Anything else is BLOCKED. The gate fails
  closed: an unrun component blocks exactly as a failed one does.

Executed vs evidence components. Six components are executed by
the gate itself against the candidate tree, deterministically:
ledger validation (the Spec 086 gate, --all), corpus identity
verification (the Stage 1 registry), anchor regression (the
anchors register against its pin and census), claim-stage
validation (``ledger_intake.validate_ledger``), provenance
completeness (the contamination class, Spec 095 T301), and
public-claims consistency (the stale-claim detector below). The
remaining seven (unit, integration, frontend, end-to-end,
security, accessibility, reproducibility smoke) are heavyweight
suites the gate does not re-run; they enter as recorded evidence
entries in an evidence manifest:

    {"unit_tests": {"verdict": "pass", "command": "...",
                    "exit_code": 0, "recorded_at": "...",
                    "record_ref": "..."}}

An evidence entry counts as PASS only with verdict "pass" and
exit_code 0; anything else is FAIL; a missing entry is NOT_RUN.

Public-claims consistency (the RT-03 detector). The component
scans the candidate's public surfaces for the stale-claim shape
of record (Stage 0 record, RT-03): superseded quantities
presented as current, with no supersession notice. A surface
fails when a stale marker is present AND no supersession banner
(a head-region statement of supersession naming the current
census) is present. Retired values below a banner, marked
historical, are the RT-03 acceptance shape and pass.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

# ---------------------------------------------------------------------------
# The thirteen components of record (C095-14), in order.

COMPONENTS: tuple[str, ...] = (
    "unit_tests",
    "integration_tests",
    "frontend_tests",
    "end_to_end_tests",
    "ledger_validation",
    "corpus_identity_verification",
    "anchor_regression",
    "claim_stage_validation",
    "provenance_completeness",
    "security_checks",
    "accessibility_checks",
    "reproducibility_smoke_test",
    "public_claims_consistency",
)

EVIDENCE_COMPONENTS: tuple[str, ...] = (
    "unit_tests",
    "integration_tests",
    "frontend_tests",
    "end_to_end_tests",
    "security_checks",
    "accessibility_checks",
    "reproducibility_smoke_test",
)

PASS = "PASS"
FAIL = "FAIL"
NOT_RUN = "NOT_RUN"
EXCEPTED = "EXCEPTED"

# ---------------------------------------------------------------------------
# Pins and expectations of record.

ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
ANCHORS_SHA256 = "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
ANCHORS_CENSUS = {"HIGH": 166, "MEDIUM": 5, "LOW": 3, "CANDIDATE": 113}
ANCHORS_TOTAL = 287

# Corpora whose absence from a checkout is by design (Stage 1
# record): the V3 strict file is placed read-only and never
# committed (gitignored subtree, licensing of record); the Holdat
# downloads layer is restricted-local. Any OTHER absent corpus
# fails the corpus-identity component.
EXPECTED_ABSENT_CORPORA = {
    "indus_v3_firestore_strict": "placed read-only at use time; never committed (identity record, licensing)",
    "holdat_downloads_layer": "restricted-local downloads layer; not held in checkouts (identity record, licensing)",
}

DEFAULT_SURFACES: tuple[str, ...] = (
    "research/indus/indus-anchor-model/README.md",
)

# The stale-claim markers of record (Stage 0 record, RT-03): the
# v2-era package presented as current.
STALE_MARKERS: tuple[tuple[str, str], ...] = (
    ("161-cohort-citation", r"161\s+Candidate\s+Proto-Dravidian\s+Anchors"),
    ("141/161-ratio", r"141/161"),
    ("161-bc-claim", r"161 H\+M signs have BC > 0"),
    ("stale-coverage", r"90\.96% H\+M"),
    ("preprint-v2-as-current", r"Preprint v2"),
)

# A supersession banner: within the head region, a statement of
# supersession that names the current anchor census.
_BANNER_LINES = 60
_BANNER_WORD = re.compile(r"supersed|supersession", re.IGNORECASE)
_BANNER_CENSUS = re.compile(r"\b287\b")


class ComponentResult:
    def __init__(self, status: str, detail: str):
        self.status = status
        self.detail = detail

    def as_dict(self) -> dict[str, str]:
        return {"status": self.status, "detail": self.detail}


# ---------------------------------------------------------------------------
# Executed components.


def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, timeout=3600
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def check_ledger_validation(root: Path) -> ComponentResult:
    code, out = _run(
        [sys.executable, "tools/ledger/check_ledger_gate.py", "--all", "--root", str(root)],
        cwd=root,
    )
    summary = next((ln.strip() for ln in out.splitlines() if "summary:" in ln), "")
    if code == 0 and "RESULT: PASS" in out:
        return ComponentResult(PASS, f"ledger gate --all: {summary}")
    return ComponentResult(FAIL, f"ledger gate --all exit {code}: {summary or out[-300:]}")


def check_corpus_identity(root: Path) -> ComponentResult:
    sys.path.insert(0, str(root / "backend"))
    from glossa_lab.data import corpus_identity as ci

    verified, absent, problems = [], [], []
    for key in ci.CORPUS_IDENTITIES:
        try:
            ci.verify_corpus_identity(key, root)
            verified.append(key)
        except ci.CorpusIdentityError as exc:
            if "corpus missing" in str(exc):
                absent.append(key)
            else:
                problems.append(f"{key}: {exc}")
        except Exception as exc:  # any other refusal is a mismatch class
            problems.append(f"{key}: {type(exc).__name__}: {exc}")
    unexpected_absent = [k for k in absent if k not in EXPECTED_ABSENT_CORPORA]
    for key in unexpected_absent:
        problems.append(f"{key}: absent from the candidate tree and not an expected absence")
    detail = f"{len(verified)} verified; absent-by-design: {sorted(absent)}"
    if problems:
        return ComponentResult(FAIL, detail + "; " + "; ".join(problems))
    return ComponentResult(PASS, detail)


def check_anchor_regression(root: Path) -> ComponentResult:
    path = root / ANCHORS_REL
    if not path.is_file():
        return ComponentResult(FAIL, f"anchors register missing: {ANCHORS_REL}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != ANCHORS_SHA256:
        return ComponentResult(FAIL, f"anchors register hash differs from pin: {digest}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("total") != ANCHORS_TOTAL or data.get("by_confidence") != ANCHORS_CENSUS:
        return ComponentResult(FAIL, f"anchors census differs: total={data.get('total')} by_confidence={data.get('by_confidence')}")
    return ComponentResult(PASS, f"anchors register at pin, census {ANCHORS_TOTAL} {ANCHORS_CENSUS}")


def check_claim_stage_validation(root: Path) -> ComponentResult:
    sys.path.insert(0, str(root / "backend"))
    from glossa_lab.ledger_intake import validate_ledger

    report = validate_ledger(root)
    if report.errors:
        return ComponentResult(FAIL, f"{len(report.errors)} intake error(s); first: {report.errors[0]}")
    return ComponentResult(PASS, f"ledger intake validation clean over {report.lines} lines")


def check_provenance_completeness(root: Path) -> ComponentResult:
    code, out = _run(
        [sys.executable, "tools/ledger/check_ledger_gate.py", "--contamination", "--root", str(root)],
        cwd=root,
    )
    line = next((ln.strip() for ln in out.splitlines() if "contamination class" in ln), "")
    if code == 0 and "CONTAMINATION: PASS" in out and "0 flag(s)" in out:
        return ComponentResult(PASS, f"contamination class: {line}")
    return ComponentResult(FAIL, f"contamination exit {code}: {line or out[-300:]}")


def has_supersession_banner(text: str) -> bool:
    head = "\n".join(text.splitlines()[:_BANNER_LINES])
    return bool(_BANNER_WORD.search(head) and _BANNER_CENSUS.search(head))


def scan_surface(text: str) -> list[str]:
    """Stale markers present in a surface, as marker names."""
    return [name for name, pattern in STALE_MARKERS if re.search(pattern, text)]


def check_public_claims(root: Path, surfaces: list[str] | None = None) -> ComponentResult:
    surfaces = surfaces if surfaces is not None else list(DEFAULT_SURFACES)
    failures, checked = [], []
    for rel in surfaces:
        path = root / rel
        if not path.is_file():
            failures.append(f"{rel}: surface missing")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        markers = scan_surface(text)
        checked.append(rel)
        if markers and not has_supersession_banner(text):
            failures.append(
                f"{rel}: stale claim presented as current (markers: {', '.join(markers)}); no supersession banner"
            )
    if failures:
        return ComponentResult(FAIL, "; ".join(failures))
    return ComponentResult(PASS, f"{len(checked)} public surface(s) free of unbannered stale claims")


EXECUTED_COMPONENTS: dict[str, Callable[..., ComponentResult]] = {
    "ledger_validation": check_ledger_validation,
    "corpus_identity_verification": check_corpus_identity,
    "anchor_regression": check_anchor_regression,
    "claim_stage_validation": check_claim_stage_validation,
    "provenance_completeness": check_provenance_completeness,
    "public_claims_consistency": check_public_claims,
}


# ---------------------------------------------------------------------------
# Evidence and exceptions.

REQUIRED_EXCEPTION_FIELDS = ("component", "scope", "approved_by", "owner_approval_ref", "date")


def validate_exceptions(entries: Any) -> tuple[dict[str, dict], list[str]]:
    """Return (valid exceptions by component, problems).

    An entry missing any required field is not an exception
    (C095-14: exceptions exist only as recorded owner-approved
    entries); it is reported as a problem and ignored.
    """
    valid: dict[str, dict] = {}
    problems: list[str] = []
    if entries is None:
        return valid, problems
    if not isinstance(entries, list):
        return valid, ["exceptions record is not a list"]
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            problems.append(f"exception #{i}: not an object")
            continue
        missing = [f for f in REQUIRED_EXCEPTION_FIELDS if not str(entry.get(f, "")).strip()]
        if missing:
            problems.append(f"exception #{i}: missing required field(s): {', '.join(missing)}")
            continue
        if entry["component"] not in COMPONENTS:
            problems.append(f"exception #{i}: unknown component {entry['component']!r}")
            continue
        valid[entry["component"]] = entry
    return valid, problems


def evidence_result(name: str, evidence: dict | None) -> ComponentResult:
    if not evidence or name not in evidence:
        return ComponentResult(NOT_RUN, "no evidence entry recorded for this component")
    entry = evidence[name]
    if entry.get("verdict") == "pass" and entry.get("exit_code") == 0:
        return ComponentResult(
            PASS,
            f"evidence: {entry.get('command', '?')} (recorded {entry.get('recorded_at', '?')}, ref {entry.get('record_ref', '?')})",
        )
    return ComponentResult(
        FAIL,
        f"evidence records verdict={entry.get('verdict')!r} exit_code={entry.get('exit_code')!r} (ref {entry.get('record_ref', '?')})",
    )


# ---------------------------------------------------------------------------
# The composed gate.


def run_release_gate(
    root: Path,
    *,
    evidence: dict | None = None,
    exceptions: list | None = None,
    surfaces: list[str] | None = None,
    executed: dict[str, Callable[..., ComponentResult]] | None = None,
) -> dict[str, Any]:
    """Run the composed gate over a candidate tree.

    Returns the per-candidate results record. ``executed`` may
    override executed-component runners (used by the gate's own
    tests to exercise composition without re-running the heavy
    in-place checks; production runs pass nothing).
    """
    runners = dict(EXECUTED_COMPONENTS)
    if executed:
        runners.update(executed)
    valid_exceptions, exception_problems = validate_exceptions(exceptions)

    results: dict[str, dict[str, str]] = {}
    for name in COMPONENTS:
        if name in EVIDENCE_COMPONENTS:
            result = evidence_result(name, evidence)
        elif name == "public_claims_consistency":
            result = runners[name](root, surfaces)
        else:
            result = runners[name](root)
        if result.status in (FAIL, NOT_RUN) and name in valid_exceptions:
            exc = valid_exceptions[name]
            result = ComponentResult(
                EXCEPTED,
                f"{result.status} covered by recorded owner-approved exception "
                f"(approved_by={exc['approved_by']}, ref={exc['owner_approval_ref']}, date={exc['date']}, scope={exc['scope']})",
            )
        results[name] = result.as_dict()

    blocked = [n for n, r in results.items() if r["status"] not in (PASS, EXCEPTED)]
    return {
        "candidate_root": str(root),
        "components": results,
        "exception_problems": exception_problems,
        "blocked_by": blocked,
        "verdict": PASS if not blocked else "BLOCKED",
    }


def format_summary(record: dict[str, Any]) -> str:
    lines = [f"RELEASE GATE: {record['verdict']}"]
    for name in COMPONENTS:
        r = record["components"][name]
        lines.append(f"  {name}: {r['status']} — {r['detail']}")
    if record["blocked_by"]:
        lines.append(f"  blocked by: {', '.join(record['blocked_by'])}")
    for problem in record["exception_problems"]:
        lines.append(f"  exception problem: {problem}")
    return "\n".join(lines)
