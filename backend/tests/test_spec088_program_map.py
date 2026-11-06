"""Spec 088 Stage S1 — program-map builder teeth (T104).

Claims covered:
  C088-1  The map is generated, never hand-edited: the builder
          is the only route to the artifacts, and its outputs
          are a pure function of the defs' inputs.
  C088-2  Coverage is total and exact, and the builder fails
          closed: duplicates, omissions, unknown ids, and
          unassigned directories each fail with nothing written.
  C088-3  Claim standings derive mechanically under the
          registered table; an unregistered status fails.
  C088-4  Study standings are the registered roll-up;
          mixed studies are judgment calls, named in the finds.
  C088-5  A bundle-less study classes as unjudged and emits
          a find.
  C088-13 Determinism: identical inputs, byte-identical
          outputs; the stamp is input-derived only.
  C088-17 The taxonomy format carries no standings: a
          standing-shaped key anywhere is a build failure.
  C088-18 in_flight has no derivation rule; emitting one
          fails the build.
  C088-19 Restricted studies render name-only.

The fixtures are tiny synthetic roots (a ledger file, a
taxonomy file, empty spec directories — the builder reads
directory names only). The real-input census lives in
test_program_map_conformance.py.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab import program_map_generate as pmg

DOMAIN = "Dom"
SUB = "Sub"


def _claim(
    cid: str,
    population: str,
    status: str,
    *,
    spec: str | None = None,
    document: str | None = None,
    stage: str | None = "created",
    falsifier: object = ("a falsifier",),
    extra_sources: list | None = None,
) -> dict:
    source = {
        "role": "source_of_record",
        "path": "fixture",
        "sha256": "0" * 64,
        "spec": spec,
        "document_id": document,
        "claim_id": cid,
    }
    return {
        "id": cid,
        "kind": "claim",
        "date": "2026-11-01",
        "population": population,
        "statement": "a statement",
        "status": status,
        "stage": stage,
        "falsifier": list(falsifier) if falsifier else None,
        "sources": [source] + (extra_sources or []),
    }


def _write_root(
    tmp_path: Path,
    *,
    rows: list[dict],
    spec_dirs: list[str],
    studies: list[str] | None = None,
    documents: list[str] | None = None,
    restricted: list[str] | None = None,
    taxonomy_mutation=None,
) -> Path:
    root = tmp_path
    (root / "glossa-indus" / "ledger").mkdir(parents=True)
    (root / "glossa-indus" / "map").mkdir(parents=True)
    (root / "specs").mkdir()
    for name in spec_dirs:
        (root / "specs" / name).mkdir()
    (root / "glossa-indus" / "ledger" / "claims.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8"
    )
    tax = {
        "version": pmg.TAXONOMY_VERSION,
        "note": "fixture",
        "domains": [DOMAIN],
        "subdomains": {DOMAIN: [SUB]},
        "studies": [
            {"spec_dir": d, "domain": DOMAIN, "subdomain": SUB}
            for d in (studies if studies is not None else spec_dirs)
        ],
        "extracted_documents": [
            {"document": d, "domain": DOMAIN, "subdomain": SUB}
            for d in (documents or [])
        ],
        "restricted": restricted or [],
    }
    if taxonomy_mutation is not None:
        tax = taxonomy_mutation(tax)
    (root / "glossa-indus" / "map" / "program-map-taxonomy.json").write_text(
        json.dumps(tax), encoding="utf-8"
    )
    return root


def _build(root: Path) -> tuple[dict, dict]:
    artifacts = pmg.build_artifacts(root)
    return (
        json.loads(artifacts[pmg.MAP_REL]),
        json.loads(artifacts[pmg.FINDS_REL]),
    )


STUDY_DIRS = ["st-pos", "st-neg", "st-mixed", "st-closed", "st-open", "st-empty"]


def _base_rows() -> list[dict]:
    return [
        _claim("c-pos", "bundle", "strongly_supported", spec="st-pos"),
        _claim("c-neg", "bundle", "contradicted", spec="st-neg"),
        _claim("c-pf", "bundle", "partially_falsified", spec="st-neg"),
        _claim("c-mix-p", "bundle", "strongly_supported", spec="st-mixed"),
        _claim("c-mix-n", "bundle", "unsupported", spec="st-mixed"),
        _claim("c-closed", "bundle", "superseded", spec="st-closed"),
        _claim("c-open", "bundle", "draft", spec="st-open"),
        _claim(
            "c-ext",
            "extracted",
            "untested",
            document="doc-a",
            stage=None,
            falsifier=None,
        ),
        _claim("c-ext2", "extracted", "partially_supported", document="doc-a"),
    ]


def _base_root(tmp_path: Path) -> Path:
    return _write_root(
        tmp_path,
        rows=_base_rows(),
        spec_dirs=STUDY_DIRS,
        documents=["doc-a"],
    )


# ── Derivation table + roll-up (C088-3, C088-4, C088-5) ─────────────────────


@pytest.mark.parametrize(
    "status,expected",
    [
        ("strongly_supported", "positive"),
        ("contradicted", "negative"),
        ("unsupported", "negative"),
        ("partially_falsified", "negative"),
        ("superseded", "closed_other"),
        ("draft", "open"),
        ("untested", "open"),
        ("partially_supported", "open"),
    ],
)
def test_derivation_table_per_status(tmp_path, status, expected):
    root = _write_root(
        tmp_path,
        rows=[_claim("c1", "bundle", status, spec="st-open")],
        spec_dirs=["st-open"],
    )
    program_map, _ = _build(root)
    (node,) = program_map["nodes"]["claims"]
    assert node["class"] == expected
    assert node["status"] == status


def test_roll_up_precedence_and_finds(tmp_path):
    program_map, finds = _build(_base_root(tmp_path))
    studies = {n["id"]: n for n in program_map["nodes"]["studies"]}
    assert studies["st-pos"]["class"] == "positive"
    assert studies["st-neg"]["class"] == "negative"
    assert studies["st-closed"]["class"] == "closed_other"
    assert studies["st-open"]["class"] == "open"
    # Mixed positive+negative: judgment call, displayed open.
    assert studies["st-mixed"]["class"] == "open"
    assert studies["st-mixed"]["judgment_call"] is True
    # No members: unjudged, plus one find.
    assert studies["st-empty"]["class"] == "unjudged"
    find_kinds = {(f["kind"], f["subject"]) for f in finds["finds"]}
    assert ("bundle_less_study", "st-empty") in find_kinds
    assert ("judgment_call", "st-mixed") in find_kinds
    assert ("extracted_null_falsifier", "c-ext") in find_kinds
    judgment = next(f for f in finds["finds"] if f["kind"] == "judgment_call")
    assert judgment["positive"] == 1 and judgment["negative"] == 1
    coverage = program_map["coverage"]
    assert coverage["unjudged_studies"] == ["st-empty"]
    assert coverage["judgment_call_studies"] == ["st-mixed"]
    assert coverage["falsifier_coverage"]["present"] == 8
    assert coverage["falsifier_coverage"]["total"] == 9
    assert coverage["falsifier_coverage"]["null_extracted_claims"] == ["c-ext"]


def test_standing_text_template(tmp_path):
    program_map, _ = _build(_base_root(tmp_path))
    claims = {n["id"]: n for n in program_map["nodes"]["claims"]}
    assert claims["c-open"]["standing"] == (
        "Ledger standing: status draft · stage created · falsifier present"
    )
    assert claims["c-ext"]["standing"] == (
        "Ledger standing: status untested · stage none · falsifier absent"
    )
    assert claims["c-ext"]["study"] is None
    assert claims["c-ext"]["document"] == "doc-a"
    assert claims["c-open"]["study"] == "st-open"


def test_reclassification_governs(tmp_path):
    rows = [
        _claim("c1", "bundle", "draft", spec="st-open"),
        {
            "id": "r1",
            "kind": "reclassification",
            "date": "2026-11-02",
            "supersedes": "c1",
            "status": "contradicted",
        },
    ]
    root = _write_root(tmp_path, rows=rows, spec_dirs=["st-open"])
    program_map, _ = _build(root)
    (node,) = program_map["nodes"]["claims"]
    assert node["class"] == "negative"
    assert node["status"] == "contradicted"


def test_multi_spec_claim_is_listed_not_a_member_elsewhere(tmp_path):
    rows = [
        _claim(
            "c1",
            "bundle",
            "draft",
            spec="st-open",
            extra_sources=[
                {
                    "role": "evidence_instance",
                    "path": "fixture",
                    "sha256": "0" * 64,
                    "spec": "st-empty",
                    "document_id": None,
                    "claim_id": "c1",
                }
            ],
        )
    ]
    root = _write_root(tmp_path, rows=rows, spec_dirs=["st-open", "st-empty"])
    program_map, _ = _build(root)
    assert program_map["coverage"]["multi_spec_claims"] == ["c1"]
    studies = {n["id"]: n for n in program_map["nodes"]["studies"]}
    assert studies["st-empty"]["class"] == "unjudged"
    assert studies["st-open"]["member_counts"]["total"] == 1


# ── Restricted studies (C088-19) ─────────────────────────────────────────────


def test_restricted_study_renders_name_only(tmp_path, monkeypatch):
    monkeypatch.setitem(
        pmg.RESTRICTED_NAME_ONLY, "st-open", "executed — held under test"
    )
    root = _write_root(
        tmp_path,
        rows=[_claim("c1", "bundle", "draft", spec="st-open")],
        spec_dirs=["st-open"],
        restricted=["st-open"],
    )
    program_map, finds = _build(root)
    (node,) = program_map["nodes"]["studies"]
    assert node["restricted"] is True
    assert node["class"] is None
    assert node["standing"] == "executed — held under test"
    assert "member_counts" not in node
    assert ("restricted_node", "st-open") in {
        (f["kind"], f["subject"]) for f in finds["finds"]
    }
    # The restricted study's claims still receive their own nodes.
    assert program_map["nodes"]["claims"][0]["study"] == "st-open"


# ── The page (Stage S4, T401; C088-8, C088-14, C088-19) ─────────────────────

_MAP_MARKER = 'id="program-map-data">\n'
_FINDS_MARKER = 'id="program-map-finds">\n'
_REGISTERED_STATUSES = (
    "strongly_supported",
    "contradicted",
    "unsupported",
    "partially_falsified",
    "superseded",
    "draft",
    "untested",
    "partially_supported",
)


def _embedded(page: str, marker: str) -> str:
    return page.split(marker, 1)[1].split("</script>", 1)[0]


def test_page_embeds_the_artifacts_verbatim(tmp_path):
    artifacts = pmg.build_artifacts(_base_root(tmp_path))
    page = artifacts[pmg.PAGE_REL]
    # The embedded payloads are the artifacts themselves,
    # byte for byte — extraction reproduces them exactly.
    assert _embedded(page, _MAP_MARKER) == artifacts[pmg.MAP_REL]
    assert _embedded(page, _FINDS_MARKER) == artifacts[pmg.FINDS_REL]
    # And the page is template + verbatim data, nothing else:
    # the chrome around the payloads is the registered
    # template, so no number or standing can enter the page
    # from anywhere but the artifacts.
    assert page == (
        pmg._PAGE_HEAD
        + artifacts[pmg.MAP_REL]
        + pmg._PAGE_MID
        + artifacts[pmg.FINDS_REL]
        + pmg._PAGE_TAIL
    )
    # A single self-contained file: no external reference.
    assert "http://" not in page and "https://" not in page


def test_page_carries_the_build_census_and_no_foreign_data(tmp_path):
    artifacts = pmg.build_artifacts(_base_root(tmp_path))
    page = artifacts[pmg.PAGE_REL]
    program_map = json.loads(artifacts[pmg.MAP_REL])
    # The census the page displays is the coverage block's,
    # carried inside the embedded data: totals, per-domain
    # counts, and the stamp all appear.
    coverage = program_map["coverage"]
    assert f'"total": {coverage["claims"]["total"]}' in page
    for block in coverage["domains"].values():
        assert f'"claims": {block["claims"]}' in page
        assert f'"studies": {block["studies"]}' in page
    assert program_map["stamp"]["ledger_sha256"] in page
    # Nothing from the real ledger leaks into a fixture
    # build: the page is a function of its own inputs only.
    assert "913" not in page
    assert "yadav" not in page


def test_page_template_carries_no_derivation():
    """C088-8's source scan: the template (the only part of
    the page that is not embedded data) holds no standing
    logic — none of the registered ledger statuses, no
    derivation table, no standing template. The script
    filters and searches generated fields; the statuses it
    never sees cannot be re-derived by it."""
    template = pmg._PAGE_HEAD + pmg._PAGE_MID + pmg._PAGE_TAIL
    for status in _REGISTERED_STATUSES:
        assert status not in template
    assert "Ledger standing: status" not in template
    assert "STATUS_TO_CLASS" not in template
    # The class filter vocabulary is the registered one
    # (plan Stage 4): the page offers exactly these filters.
    for label in (
        "All",
        "Positive",
        "Negative",
        "Open",
        "In flight",
        "Closed",
        "Unjudged",
    ):
        assert label in pmg._PAGE_TAIL


def test_page_embedding_guard_refuses_a_script_close():
    with pytest.raises(pmg.ProgramMapBuildError, match="script-close"):
        pmg._render_page('{"x": "</script>"}', "{}")
    with pytest.raises(pmg.ProgramMapBuildError, match="script-close"):
        pmg._render_page("{}", '{"x": "</SCRIPT>"}')


# ── Determinism + stamp (C088-13) ────────────────────────────────────────────


def test_determinism_and_input_derived_stamp(tmp_path):
    root = _base_root(tmp_path)
    first = pmg.build_artifacts(root)
    second = pmg.build_artifacts(root)
    assert first == second
    program_map = json.loads(first[pmg.MAP_REL])
    stamp = program_map["stamp"]
    assert set(stamp) == {
        "ledger_latest_entry_date",
        "ledger_lines",
        "ledger_schema",
        "ledger_sha256",
        "program_map_defs",
        "program_map_taxonomy",
    }
    assert stamp["ledger_lines"] == 9
    assert stamp["ledger_latest_entry_date"] == "2026-11-01"
    from glossa_lab.ledger_intake import sha256_file

    assert stamp["ledger_sha256"] == sha256_file(
        root / "glossa-indus" / "ledger" / "claims.jsonl"
    )


# ── Fail-closed coverage (C088-2, C088-3, C088-17, C088-18) ──────────────────


def _assert_refused_and_nothing_written(root: Path, match: str):
    with pytest.raises(pmg.ProgramMapBuildError, match=match):
        pmg.write_outputs(root)
    assert not (root / pmg.MAP_REL).exists()
    assert not (root / pmg.FINDS_REL).exists()
    assert not (root / pmg.PAGE_REL).exists()


def test_unassigned_spec_directory_fails(tmp_path):
    root = _write_root(
        tmp_path,
        rows=_base_rows(),
        spec_dirs=STUDY_DIRS,
        studies=[d for d in STUDY_DIRS if d != "st-open"],
        documents=["doc-a"],
    )
    _assert_refused_and_nothing_written(root, "no assignment")


def test_assignment_naming_no_directory_fails(tmp_path):
    root = _write_root(
        tmp_path,
        rows=_base_rows(),
        spec_dirs=STUDY_DIRS,
        studies=STUDY_DIRS + ["st-ghost"],
        documents=["doc-a"],
    )
    _assert_refused_and_nothing_written(root, "naming no directory")


def test_duplicated_assignment_fails(tmp_path):
    def mutate(tax: dict) -> dict:
        tax["studies"] = tax["studies"] + [tax["studies"][0]]
        return tax

    root = _write_root(
        tmp_path,
        rows=_base_rows(),
        spec_dirs=STUDY_DIRS,
        documents=["doc-a"],
        taxonomy_mutation=mutate,
    )
    _assert_refused_and_nothing_written(root, "more than once")


def test_unknown_extracted_document_fails(tmp_path):
    rows = _base_rows() + [
        _claim("c-ghost", "extracted", "draft", document="doc-ghost")
    ]
    root = _write_root(
        tmp_path, rows=rows, spec_dirs=STUDY_DIRS, documents=["doc-a"]
    )
    _assert_refused_and_nothing_written(root, "doc-ghost")


def test_taxonomy_document_the_ledger_lacks_fails(tmp_path):
    root = _write_root(
        tmp_path,
        rows=_base_rows(),
        spec_dirs=STUDY_DIRS,
        documents=["doc-a", "doc-unused"],
    )
    _assert_refused_and_nothing_written(root, "doc-unused")


def test_unregistered_status_fails(tmp_path):
    rows = [_claim("c1", "bundle", "half_supported", spec="st-open")]
    root = _write_root(tmp_path, rows=rows, spec_dirs=["st-open"])
    _assert_refused_and_nothing_written(root, "unregistered status")


def test_in_flight_emission_fails(tmp_path, monkeypatch):
    monkeypatch.setitem(pmg.STATUS_TO_CLASS, "draft", "in_flight")
    root = _write_root(
        tmp_path,
        rows=[_claim("c1", "bundle", "draft", spec="st-open")],
        spec_dirs=["st-open"],
    )
    _assert_refused_and_nothing_written(root, "in_flight")


def test_duplicate_claim_id_fails(tmp_path):
    rows = [
        _claim("c1", "bundle", "draft", spec="st-open"),
        _claim("c1", "bundle", "draft", spec="st-open"),
    ]
    root = _write_root(tmp_path, rows=rows, spec_dirs=["st-open"])
    _assert_refused_and_nothing_written(root, "duplicate claim id")


def test_standing_shaped_taxonomy_key_fails(tmp_path):
    def mutate(tax: dict) -> dict:
        tax["studies"][0]["standing"] = "prose standing"
        return tax

    root = _write_root(
        tmp_path,
        rows=_base_rows(),
        spec_dirs=STUDY_DIRS,
        documents=["doc-a"],
        taxonomy_mutation=mutate,
    )
    _assert_refused_and_nothing_written(root, "forbidden")


def test_undeclared_subdomain_fails(tmp_path):
    def mutate(tax: dict) -> dict:
        tax["studies"][0]["subdomain"] = "Nowhere"
        return tax

    root = _write_root(
        tmp_path,
        rows=_base_rows(),
        spec_dirs=STUDY_DIRS,
        documents=["doc-a"],
        taxonomy_mutation=mutate,
    )
    _assert_refused_and_nothing_written(root, "not declared")


def test_restricted_without_registered_form_fails(tmp_path):
    root = _write_root(
        tmp_path,
        rows=[_claim("c1", "bundle", "draft", spec="st-open")],
        spec_dirs=["st-open"],
        restricted=["st-open"],
    )
    _assert_refused_and_nothing_written(root, "no registered")
