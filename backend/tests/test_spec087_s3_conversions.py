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

The one binary input, the two-page PDF read by the pdf cases, cannot
be committed as a file (`*.pdf` is gitignored), so its bytes are
committed base64-encoded in this module and materialized at run
time — see `_fixture_pdf`.

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


# The two-page fixture PDF for the pdf cases, committed as base64
# (a `*.pdf` file cannot be committed — it is gitignored). Produced
# with the exact recipe the pre-T701 run-time generation used:
# fitz.open(), one new_page() + insert_text((72, 72), line) per page
# text ("Glossa fixture page one" / "Glossa fixture page two").
# Verified at commit time: 1,203 bytes, 2 pages. The page count is
# pinned as data alongside, and `_fixture_pdf` asserts the real
# document agrees with it wherever PyMuPDF is present.
_FIXTURE_PDF_B64 = (
    "JVBERi0xLjcKJcK1wrYKJSBXcml0dGVuIGJ5IE11UERGIDEuMjguMgoKMSAwIG9iago8PC9UeXBlL0NhdGFsb2cvUGFnZXMgMiAw"
    "IFIvSW5mbzw8L1Byb2R1Y2VyKE11UERGIDEuMjguMik+Pj4+CmVuZG9iagoKMiAwIG9iago8PC9UeXBlL1BhZ2VzL0NvdW50IDIv"
    "S2lkc1s0IDAgUiA4IDAgUl0+PgplbmRvYmoKCjMgMCBvYmoKPDwvRm9udDw8L2hlbHYgNSAwIFI+Pj4+CmVuZG9iagoKNCAwIG9i"
    "ago8PC9UeXBlL1BhZ2UvTWVkaWFCb3hbMCAwIDU5NSA4NDJdL1JvdGF0ZSAwL1Jlc291cmNlcyAzIDAgUi9QYXJlbnQgMiAwIFIv"
    "Q29udGVudHNbNiAwIFJdPj4KZW5kb2JqCgo1IDAgb2JqCjw8L1R5cGUvRm9udC9TdWJ0eXBlL1R5cGUxL0Jhc2VGb250L0hlbHZl"
    "dGljYS9FbmNvZGluZy9XaW5BbnNpRW5jb2Rpbmc+PgplbmRvYmoKCjYgMCBvYmoKPDwvTGVuZ3RoIDk0Pj4Kc3RyZWFtCgpxCkJU"
    "CjEgMCAwIDEgNzIgNzcwIFRtCi9oZWx2IDExIFRmIFs8NDc2YzZmNzM3MzYxMjA2NjY5Nzg3NDc1NzI2NTIwNzA2MTY3NjUyMDZm"
    "NmU2NT5dVEoKRVQKUQoKZW5kc3RyZWFtCmVuZG9iagoKNyAwIG9iago8PC9Gb250PDwvaGVsdiA1IDAgUj4+Pj4KZW5kb2JqCgo4"
    "IDAgb2JqCjw8L1R5cGUvUGFnZS9NZWRpYUJveFswIDAgNTk1IDg0Ml0vUm90YXRlIDAvUmVzb3VyY2VzIDcgMCBSL1BhcmVudCAy"
    "IDAgUi9Db250ZW50c1s5IDAgUl0+PgplbmRvYmoKCjkgMCBvYmoKPDwvTGVuZ3RoIDkzL0ZpbHRlci9GbGF0ZURlY29kZT4+CnN0"
    "cmVhbQp42h3GMQqEQAwF0D6nyA1Mxpn/FWQLwcZOSCdW4rDFWth4fhd5zZNLxhBX+3NlUtI0Tmm+x+9Wd42q65CJHZUtW3gyAD07"
    "ZhYmlGQ0OPguk6ifLWaZQhZ5AM2uFL0KZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDEwCjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAw"
    "MDAwMDA0MiAwMDAwMCBuIAowMDAwMDAwMTIwIDAwMDAwIG4gCjAwMDAwMDAxNzggMDAwMDAgbiAKMDAwMDAwMDIxOSAwMDAwMCBu"
    "IAowMDAwMDAwMzI2IDAwMDAwIG4gCjAwMDAwMDA0MTUgMDAwMDAgbiAKMDAwMDAwMDU1OCAwMDAwMCBuIAowMDAwMDAwNTk5IDAw"
    "MDAwIG4gCjAwMDAwMDA3MDYgMDAwMDAgbiAKCnRyYWlsZXIKPDwvU2l6ZSAxMC9Sb290IDEgMCBSL0lEWzwwMkMzODRDMkJFMzVD"
    "MkE0MzY1REMyOTJDMzhFMzg3Qz48MTc4NTdDQjkyNkZEMUQ2MTRFMDE4RUY4QjdFREZGODI+XT4+CnN0YXJ0eHJlZgo4NjcKJSVF"
    "T0YK"
)
_FIXTURE_PDF_PAGES = 2


def _fixture_pdf(tmp_path: Path) -> Path:
    """The two-page fixture PDF for the pdf cases, materialized from
    the committed base64 bytes above into tmp_path.

    Where PyMuPDF is importable, the materialized document's real
    page count is asserted against the pinned `_FIXTURE_PDF_PAGES`,
    tying the fixture fields together. Without PyMuPDF the file
    still has to exist: the node checks existence before its import,
    so the path carries execution to the import whose failure is the
    node's pinned no-PyMuPDF behaviour.
    """
    import base64

    pdf_path = tmp_path / "tiny.pdf"
    pdf_path.write_bytes(base64.b64decode(_FIXTURE_PDF_B64))
    try:
        import fitz  # noqa: PLC0415
    except ImportError:
        return pdf_path
    doc = fitz.open(str(pdf_path))
    assert doc.page_count == _FIXTURE_PDF_PAGES
    doc.close()
    return pdf_path


def _run_case(case: dict, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    setup = case["setup"]
    kind = setup["kind"]
    tokens: dict[str, str] = {"__FIXTURE_PDF__": str(_fixture_pdf(tmp_path))}
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
            # This environment has no PyMuPDF. pymupdf is declared
            # under pyproject's `ocr` optional extra and CI installs
            # only `.[dev]`, so CI is exactly this environment; the
            # full extraction replay below runs only where fitz
            # exists. (An earlier text here claimed the opposite —
            # that CI installs it from pyproject; PR #499's first CI
            # run disproved that for the PR-F file, and the same
            # correction applies here.) The node's no-PyMuPDF error
            # dict is its designed behaviour without the optional
            # dependency, and it is the pinned expectation for
            # fitz-free environments, asserted exactly below. No
            # stand-in fitz is installed for these cases: the
            # extractor's whole function is fitz (page_count /
            # load_page().get_text()), so a stand-in would have to
            # fabricate the very extracted texts the fixtures pin —
            # the comparison would become circular. (PR-F's
            # stand-in is sound precisely because its pixmap bytes
            # feed a stubbed vision call that ignores them.) This
            # reasoned exception is recorded in the T701 closeout
            # record (records/stage-t701-closeout-record.md).
            probe_params = _substitute(
                case["params"], {"__FIXTURE_PDF__": str(_fixture_pdf(tmp_path))}
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
