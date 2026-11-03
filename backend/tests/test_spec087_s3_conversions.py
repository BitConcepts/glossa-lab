"""Spec 087 Stage S3 conversion PR-A — fixture output-equivalence (F14 + F1).

The S3 conversion contract (records/stage-s3-conversions.md):

  * A converted node's implementation becomes generic machinery driven
    by parameters; the domain node delegates to the generic primitive
    with today's domain specifics as parameter defaults.
  * Fixture output-equivalence: outputs captured from the CURRENT
    (pre-conversion) implementation are committed as fixtures; after
    conversion the same inputs must produce byte-identical outputs.

The fixtures in tests/fixtures/spec087_s3_conv_a/expected.json were
captured from the pre-conversion implementations on this branch BEFORE
any implementation changed (commit "Spec 087 S3: pre-change equivalence
fixtures"). Full-mode cases pin the whole result dict (canonical-JSON
equality); hash-mode cases pin the canonical-JSON SHA-256 plus the key
set and verbatim scalar fields, for payloads too large to commit whole.

Also pinned here: the F14 relabels (generic category, no legacy flag,
implementation module unchanged), the two new generic primitives'
registration, and the six converted ids' legacy flags.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from glossa_lab import experiment_graph as eg
from glossa_lab import experiment_graph_phase20 as phase20
from glossa_lab import experiment_graph_phase_legacy as phase_legacy
from glossa_lab.data import mesopotamian_contact as mc

FIXTURES = Path(__file__).parent / "fixtures" / "spec087_s3_conv_a"
_BUNDLE = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
CASES = _BUNDLE["cases"]

CONVERTED_IDS = [
    "M77InscriptionLoader",
    "ContactCorpusLoader",
    "MahadevanInscriptionLoader",
    "EPSD2NamesLoader",
    "ICITCorpusLoader",
    "MathematicaEpigraphicaLoader",
]

CONVERTED_MODULES = {
    "M77InscriptionLoader": "glossa_lab.experiment_graph_phase20",
    "ContactCorpusLoader": "glossa_lab.experiment_graph_phase22",
    "MahadevanInscriptionLoader": "glossa_lab.experiment_graph_phase29",
    "EPSD2NamesLoader": "glossa_lab.experiment_graph_phase29",
    "ICITCorpusLoader": "glossa_lab.experiment_graph_phase29",
    "MathematicaEpigraphicaLoader": "glossa_lab.experiment_graph_phase29",
}


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def _substitute(obj: Any, tokens: dict[str, str]) -> Any:
    """Replace the capture-time path tokens with this run's real paths."""
    if isinstance(obj, str):
        for token, value in tokens.items():
            obj = obj.replace(token, value)
        return obj
    if isinstance(obj, list):
        return [_substitute(item, tokens) for item in obj]
    if isinstance(obj, dict):
        return {key: _substitute(value, tokens) for key, value in obj.items()}
    return obj


def _clear_contact_caches() -> None:
    for name in dir(mc):
        member = getattr(mc, name)
        if hasattr(member, "cache_clear"):
            member.cache_clear()


def _run_case(case: dict, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    setup = case["setup"]
    kind = setup["kind"]
    tokens: dict[str, str] = {"__FIXTURE_PDF__": str(FIXTURES / "tiny.pdf")}
    if kind == "m77":
        root = tmp_path / "repo"
        (root / "reports").mkdir(parents=True)
        if setup.get("decoded"):
            shutil.copy(
                FIXTURES / setup["decoded"],
                root / "reports" / "mahadevan_texts_decoded.json",
            )
        if setup.get("csv"):
            csv_dir = (
                root
                / "corpora/downloads/external_repos/holdatllc_indus"
            )
            csv_dir.mkdir(parents=True)
            shutil.copy(FIXTURES / setup["csv"], csv_dir / "indus_corpus 2.csv")
        monkeypatch.setattr(phase20, "_resolve_repo_root", lambda: root)
        tokens["__REPO_ROOT__"] = str(root)
        tokens["__CASE_TMP__"] = str(root)
    elif kind == "tmp_files":
        for dest, src in setup["files"].items():
            target = tmp_path / dest
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(FIXTURES / src, target)
        tokens["__CASE_TMP__"] = str(tmp_path)
    elif kind == "contact":
        monkeypatch.setattr(mc, "_CDLI_MELUHHA", FIXTURES / "contact_tablets.json")
        monkeypatch.setattr(mc, "_INDUS_SEALS_MES", FIXTURES / "contact_seals.json")
        _clear_contact_caches()
    elif kind == "script_runner":
        root = tmp_path / "repo"
        (root / "scripts").mkdir(parents=True)
        shutil.copy(FIXTURES / "tiny_script.py", root / "scripts" / "tiny.py")
        monkeypatch.setattr(phase_legacy, "_resolve_repo_root", lambda: root)
        tokens["__REPO_ROOT__"] = str(root)
        tokens["__CASE_TMP__"] = str(root)
    elif kind in ("plain", "pdf"):
        # Plain cases run against the real tree; the capture tokenised
        # the resolved repo root as __REPO_ROOT__ (e.g. the
        # script-not-found error path).
        tokens["__REPO_ROOT__"] = str(phase_legacy._resolve_repo_root())
    else:  # pragma: no cover - guards the fixture bundle itself
        raise AssertionError(f"unknown setup kind {kind!r}")

    params = _substitute(case["params"], tokens)
    node_fn = eg.ATOMIC_NODES[case["node"]].fn
    result = node_fn({}, params)
    if kind == "contact":
        _clear_contact_caches()
    return result, tokens


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_conversion_output_equivalence(case, tmp_path, monkeypatch):
    """Post-conversion outputs are byte-identical to the captured
    pre-conversion outputs, per case."""
    if case["setup"]["kind"] == "pdf":
        try:
            import fitz  # noqa: F401, PLC0415
        except ImportError:
            # This environment has no PyMuPDF (the CI venv installs it
            # from pyproject; the local glossa-ci venv does not). The
            # node's no-PyMuPDF error is its behaviour here; the
            # extraction fixtures pin behaviour where fitz exists (CI).
            probe_params = _substitute(
                case["params"], {"__FIXTURE_PDF__": str(FIXTURES / "tiny.pdf")}
            )
            result = eg.ATOMIC_NODES[case["node"]].fn({}, probe_params)
            assert set(result) == {"error"}
            assert result["error"].startswith("PyMuPDF not available:")
            return
    result, tokens = _run_case(case, tmp_path, monkeypatch)
    if case["mode"] == "full":
        expected = _substitute(case["expected"], tokens)
        assert _canonical(result) == _canonical(expected)
    else:
        digest = hashlib.sha256(_canonical(result).encode("utf-8")).hexdigest()
        assert digest == case["expected_sha256"]
        assert sorted(result.keys()) == case["expected_keys"]
        for field, value in case["expected_fields"].items():
            # JSON round-trip: the fixture stores tuples as arrays.
            assert json.loads(_canonical(result[field])) == value


# ── F14: relabelled, generic, unflagged, implementation untouched ────────────


def test_f14_nodes_relabelled_generic():
    script_runner = eg.ATOMIC_NODES["LegacyPhaseScriptRunner"]
    assert script_runner.category == "Experiments"
    assert script_runner.legacy is False
    assert script_runner.fn.__module__ == "glossa_lab.experiment_graph_phase_legacy"

    pdf = eg.ATOMIC_NODES["PDFTextExtractor"]
    assert pdf.category == "Sources"
    assert pdf.legacy is False
    assert pdf.fn.__module__ == "glossa_lab.experiment_graph_phase20"


# ── The two new generic primitives ───────────────────────────────────────────


def test_generic_primitives_registered_in_the_palette(client):
    for node_id in ("JsonCorpusLoader", "DatasetRecordLoader"):
        node_def = eg.ATOMIC_NODES[node_id]
        assert node_def.category == "Sources"
        assert node_def.legacy is False
    resp = client.get("/api/v1/experiment-graphs/catalog")
    assert resp.status_code == 200
    palette_ids = {entry["id"] for entry in resp.json()}
    assert {"JsonCorpusLoader", "DatasetRecordLoader"} <= palette_ids


# ── The six converted ids: flagged, resolvable, provenance unchanged ────────


def test_converted_ids_flagged_legacy_but_registered(client):
    for node_id in CONVERTED_IDS:
        node_def = eg.ATOMIC_NODES[node_id]
        assert node_def.legacy is True
        assert node_def.fn.__module__ == CONVERTED_MODULES[node_id]
    resp = client.get("/api/v1/experiment-graphs/catalog")
    palette_ids = {entry["id"] for entry in resp.json()}
    assert not (set(CONVERTED_IDS) & palette_ids)
    resp = client.get("/api/v1/experiment-graphs/catalog?include_legacy=true")
    full_ids = {entry["id"] for entry in resp.json()}
    assert set(CONVERTED_IDS) <= full_ids
