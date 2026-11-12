"""Spec 084 — POLICY-SYNC conformance tests.

Every public policy or claims-bearing text served by the app has an
approved-text FIXTURE under specs/084-policy-sync-conformance/
fixtures/ (the single source of truth, headed by its approval
citation). These tests diff the surface sources against the
fixtures and run absence checks for removed/superseded text. A
failure means drift in one direction or the other:

- the surface no longer carries the approved text (the surface
  drifted — fix the surface), or
- the fixture no longer matches the surface (the fixture was
  edited — a fixture edit is legitimate ONLY with a recorded
  owner-approval act on the actual text, FR-084-08; without one it
  is itself a finding, never a reason to edit the surface to match).

HELD claims (C084-9…C084-11) deliberately have NO tests here:
their falsifiers cannot execute today (source outside this repo,
or no approval act exists to fixture). See
specs/084-policy-sync-conformance/spec.md §HELD. C084-8 was HELD
at the spec's landing and ACTIVATED 2026-11-05 under FR-084-09
(owner approval; its condition — frontend/src/cloud/ on main —
was met when feat/083-frontend landed in PR #476, 2026-11-01);
its tests are the C084-8 section below.

C084-12 (the privacy / data-handling statement, gap A4) entered
the regime on the owner's approval act of 2026-11-05 (T011) and
IS exercised here under FR-084-10: presence (the served copy
equals the fixture), wiring (the route is registered), and
absence (the superseded draft placeholder text stays out of
every served source, and the SPA carries no baked copy of the
statement).
"""

from __future__ import annotations

import html
import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_FIXTURES = _REPO / "specs" / "084-policy-sync-conformance" / "fixtures"


def _fixture_body(name: str) -> str:
    text = (_FIXTURES / name).read_text(encoding="utf-8")
    marker = "# ---\n"
    assert marker in text, f"fixture {name} lacks the '# ---' body marker"
    return text.split(marker, 1)[1]


def _fixture_lines(name: str) -> list[str]:
    return [line for line in _fixture_body(name).splitlines() if line.strip()]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _source(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


def _iter_source_files(root: Path, suffixes: tuple[str, ...]):
    for path in sorted(root.rglob("*")):
        if "node_modules" in path.parts:
            continue
        if path.is_file() and path.suffix in suffixes:
            yield path


# ── C084-1: the standing position (FR-084-01) ────────────────────────────────


def test_standing_position_matches_fixture():
    from glossa_lab.project_seeder import _DEFAULT_PROJECT

    approved = _fixture_body("standing-position.txt").strip()
    assert _DEFAULT_PROJECT["standing_position"] == approved


# ── C084-2: the stage-count framing (FR-084-02) ──────────────────────────────


def test_stage_count_framing_matches_fixture():
    approved = _norm(_fixture_body("stage-count-framing.txt"))
    surface = _norm(_source("frontend/src/components/ProgramHome.tsx"))
    assert approved in surface


# ── C084-3: the cloud edge perimeter texts (FR-084-03) ───────────────────────


def test_edge_robots_body_matches_fixture():
    src = _source("cloud/edge/src/worker.ts")
    match = re.search(r'ROBOTS_TXT = "((?:[^"\\]|\\.)*)"', src)
    assert match, "ROBOTS_TXT constant not found in cloud/edge/src/worker.ts"
    served = match.group(1).encode("utf-8").decode("unicode_escape")
    approved = "\n".join(_fixture_lines("edge-robots.txt")) + "\n"
    assert served == approved


def test_edge_noindex_value_matches_fixture():
    src = _source("cloud/edge/src/headers.ts")
    match = re.search(r'NOINDEX_VALUE = "([^"]*)"', src)
    assert match, "NOINDEX_VALUE constant not found in cloud/edge/src/headers.ts"
    assert match.group(1) == _fixture_body("edge-noindex.txt").strip()


# ── C084-4: the API-token gate copy (FR-084-04) ──────────────────────────────


def test_token_gate_copy_matches_fixture():
    surface = _norm(_source("frontend/src/components/ApiToken.tsx"))
    for line in _fixture_lines("token-gate-copy.txt"):
        assert _norm(line) in surface, f"approved token-gate copy missing: {line!r}"


# ── C084-5: the tray status copy (FR-084-05) ─────────────────────────────────


def test_tray_status_copy_matches_fixture():
    surface = _norm(_source("tray/glossa_tray/main.py"))
    for line in _fixture_lines("tray-status-copy.txt"):
        assert _norm(line) in surface, f"approved tray copy missing: {line!r}"


# ── C084-12: the privacy / data-handling statement (FR-084-10, T011) ────────


def test_privacy_statement_matches_fixture():
    from glossa_lab.privacy_statement import PRIVACY_STATEMENT

    approved = _fixture_body("privacy-data-handling.txt").strip()
    assert PRIVACY_STATEMENT == approved


def test_privacy_route_is_registered():
    main_src = _source("backend/glossa_lab/main.py")
    assert "from glossa_lab.api.privacy import router as privacy_router" in main_src
    assert 'include_router(privacy_router, prefix="/api/v1")' in main_src
    api_src = _source("backend/glossa_lab/api/privacy.py")
    assert '@router.get("/privacy")' in api_src


def test_no_unverified_placeholder_text():
    roots = [
        _REPO / "frontend" / "src",
        _REPO / "cloud" / "edge" / "src",
        _REPO / "backend" / "glossa_lab",
    ]
    offenders = []
    for root in roots:
        for path in _iter_source_files(root, (".ts", ".tsx", ".js", ".jsx", ".py")):
            if "[UNVERIFIED" in path.read_text(encoding="utf-8", errors="ignore"):
                offenders.append(str(path.relative_to(_REPO)))
    assert not offenders, f"superseded draft placeholder text found in: {offenders}"


def test_spa_carries_no_baked_privacy_copy():
    # The SPA must render the served statement, never a second
    # copy baked into the frontend (a second copy is a second
    # source of truth — the drift this spec exists to prevent).
    distinctive = _norm(
        "The cloud edition does not move the program. The research data"
    )
    offenders = []
    for path in _iter_source_files(_REPO / "frontend" / "src", (".ts", ".tsx")):
        if distinctive in _norm(path.read_text(encoding="utf-8", errors="ignore")):
            offenders.append(str(path.relative_to(_REPO)))
    assert not offenders, f"baked copy of the privacy statement found in: {offenders}"


# ── C084-8: the cloud anonymous-surface copy (FR-084-09) ────────────────────


def test_cloud_anonymous_surface_copy_matches_fixture():
    # The TSX source spells one apostrophe as an HTML entity
    # (&rsquo;); the fixture carries the approved text as rendered,
    # so the surface is entity-decoded before the comparison — the
    # same literal-decode treatment as the edge robots body above.
    # The surface's copy lives in two sources since PR #556: the
    # SPA's static text (pages.tsx) and the edge's structured
    # refusal messages (cloud/edge/src/identity.ts), which the SPA
    # renders verbatim. Both are the surface the visitor reads, so
    # both are searched; the assertion itself is unchanged.
    surface = _norm(
        html.unescape(_source("frontend/src/cloud/pages.tsx"))
        + "\n"
        + html.unescape(_source("cloud/edge/src/identity.ts"))
    )
    for line in _fixture_lines("cloud-anonymous-surface-copy.txt"):
        assert _norm(line) in surface, f"approved cloud copy missing: {line!r}"


def test_superseded_reset_link_promise_absent():
    # Wireframe 01's login sentence promised a reset link ("Forgot
    # your password? An admin can issue you a reset link from the
    # user dashboard."). The 2026-10-31 parent decision on the
    # Phase 3 flags superseded it: admin disable + re-invite is
    # the designed recovery. The superseded promise must not
    # return on any served frontend surface.
    needle = "issue you a reset link"
    front = _REPO / "frontend" / "src"
    offenders = []
    for path in _iter_source_files(front, (".ts", ".tsx", ".js", ".jsx")):
        if needle in _norm(path.read_text(encoding="utf-8", errors="ignore")).lower():
            offenders.append(str(path.relative_to(_REPO)))
    assert not offenders, f"superseded reset-link promise found in: {offenders}"


# ── C084-6: absence — the superseded "161" headline framing (FR-084-06) ─────


def test_no_superseded_161_headline_framing():
    pattern = re.compile(r"\b161\s+(candidate|readings|anchors)\b", re.IGNORECASE)
    roots = [
        _REPO / "frontend" / "src",
        _REPO / "cloud" / "edge" / "src",
        _REPO / "backend" / "glossa_lab",
    ]
    offenders = []
    for root in roots:
        for path in _iter_source_files(root, (".ts", ".tsx", ".js", ".jsx", ".py")):
            if pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
                offenders.append(str(path.relative_to(_REPO)))
    assert not offenders, f"superseded 161 headline framing found in: {offenders}"


# ── C084-7: absence — the Spec 081 D4-removed surfaces (FR-084-07) ──────────

_REMOVED_COMPONENTS = [
    "DeciphermentPanel",
    "StudiesView",
    "AG2Panel",
    "AIChatView",
    "CollaborationPanel",
    "ExperimentRegistry",
    "PhaseAdvancerPanel",
    "SignDictionary",
    "PresetsView",
    "ExperimentsView",
    "StudyBuilderView",
    "DashboardView",
]


def test_d4_removed_surfaces_stay_removed():
    front = _REPO / "frontend" / "src"
    files = list(_iter_source_files(front, (".ts", ".tsx", ".js", ".jsx")))
    for name in _REMOVED_COMPONENTS:
        assert not list(front.rglob(f"{name}.tsx")), f"{name}.tsx has returned"
        assert not list(front.rglob(f"{name}.ts")), f"{name}.ts has returned"
        import_pattern = re.compile(
            rf"(from\s+['\"][^'\"]*/{name}['\"]|\bimport\s+{name}\b)"
        )
        for path in files:
            assert not import_pattern.search(
                path.read_text(encoding="utf-8", errors="ignore")
            ), f"{name} is imported again in {path.relative_to(_REPO)}"
    for path in files:
        assert "REAL_CATALOG_SUMMARY" not in path.read_text(
            encoding="utf-8", errors="ignore"
        ), f"REAL_CATALOG_SUMMARY fallback data has returned in {path.relative_to(_REPO)}"
