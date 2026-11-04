"""Spec 088 Stages S1–S2 — program-map conformance against the real inputs.

The plan's S1 conformance: the builder run over the real
ledger, the filed taxonomy, and the live spec tree produces
the counted census — recomputed here independently from the
raw inputs and compared against the builder's coverage
block — deterministically, with an input-derived stamp and
no wall clock. The census pins below are the census of
record (stage record, 2026-11-04, post-adoption ledger):
a later intake that grows the ledger fails these pins
loudly and updates them in its own stage record, exactly
like the Spec 087 registry pins.

The committed artifacts landed in Stage S2 (T201), so
check semantics now run against the real root as well
(`test_committed_artifacts_match_fresh_build`); the tmp
copy still carries the drift case, which must never be
seeded in the real tree.
"""

from __future__ import annotations

import json
from pathlib import Path

from glossa_lab import program_map_generate as pmg
from glossa_lab.ledger_intake import sha256_file

_REPO = Path(__file__).resolve().parents[2]

# The census of record (2026-11-04, post-adoption ledger).
PIN_CLAIMS = 876
PIN_CLAIMS_BY_POPULATION = {"bundle": 853, "extracted": 23}
PIN_CLAIMS_BY_CLASS = {
    "closed_other": 1,
    "negative": 6,
    "open": 867,
    "positive": 2,
}
PIN_STUDIES = 89
PIN_UNJUDGED = 28
PIN_FALSIFIER_PRESENT = 867
PIN_NULL_FALSIFIER_EXTRACTED = 9
PIN_MULTI_SPEC = 44


def _raw_ledger() -> list[dict]:
    return [
        json.loads(line)
        for line in (_REPO / pmg.LEDGER_REL)
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]


def _spec_dirs() -> list[str]:
    return sorted(p.name for p in (_REPO / "specs").iterdir() if p.is_dir())


def _recompute() -> dict:
    rows = _raw_ledger()
    claims = [r for r in rows if r["kind"] == "claim"]
    homes: set[str] = set()
    documents: set[str] = set()
    null_extracted: list[str] = []
    multi_spec = 0
    for claim in claims:
        sor = next(
            s for s in claim["sources"] if s["role"] == "source_of_record"
        )
        if claim["population"] == "bundle":
            homes.add(sor["spec"])
            specs_named = {
                s.get("spec") for s in claim["sources"] if s.get("spec")
            }
            if len(specs_named) > 1:
                multi_spec += 1
        else:
            documents.add(sor["document_id"])
            if not claim.get("falsifier"):
                null_extracted.append(claim["id"])
    return {
        "claims": claims,
        "rows": rows,
        "unjudged": sorted(set(_spec_dirs()) - homes),
        "documents": sorted(documents),
        "null_extracted": sorted(null_extracted),
        "multi_spec": multi_spec,
    }


def test_real_build_census_matches_independent_recompute():
    program_map = json.loads(pmg.build_artifacts(_REPO)[pmg.MAP_REL])
    expected = _recompute()
    coverage = program_map["coverage"]
    assert coverage["claims"]["total"] == len(expected["claims"])
    assert coverage["claims"]["by_population"] == PIN_CLAIMS_BY_POPULATION
    assert coverage["claims"]["by_class"] == PIN_CLAIMS_BY_CLASS
    assert coverage["unjudged_studies"] == expected["unjudged"]
    assert coverage["multi_spec_claims"] == sorted(
        c["id"]
        for c in expected["claims"]
        if c["population"] == "bundle"
        and len({s.get("spec") for s in c["sources"] if s.get("spec")}) > 1
    )
    assert len(coverage["multi_spec_claims"]) == PIN_MULTI_SPEC
    assert (
        coverage["falsifier_coverage"]["null_extracted_claims"]
        == expected["null_extracted"]
    )
    assert coverage["falsifier_coverage"]["present"] == PIN_FALSIFIER_PRESENT
    assert (
        len(coverage["falsifier_coverage"]["null_extracted_claims"])
        == PIN_NULL_FALSIFIER_EXTRACTED
    )
    assert coverage["claims"]["total"] == PIN_CLAIMS
    assert coverage["studies"]["total"] == PIN_STUDIES == len(_spec_dirs())
    assert len(coverage["unjudged_studies"]) == PIN_UNJUDGED
    assert coverage["studies"]["restricted"] == 1
    assert coverage["judgment_call_studies"] == []
    assert len(program_map["nodes"]["claims"]) == PIN_CLAIMS
    assert len(program_map["nodes"]["studies"]) == PIN_STUDIES
    stamp = program_map["stamp"]
    assert stamp["ledger_sha256"] == sha256_file(_REPO / pmg.LEDGER_REL)
    assert stamp["ledger_lines"] == len(expected["rows"])
    assert stamp["ledger_latest_entry_date"] == max(
        r["date"] for r in expected["rows"]
    )


def test_real_build_is_byte_deterministic():
    first = pmg.build_artifacts(_REPO)
    second = pmg.build_artifacts(_REPO)
    assert first == second
    assert set(first) == {pmg.MAP_REL, pmg.FINDS_REL}


def test_real_build_has_no_in_flight_and_restricted_is_name_only():
    program_map = json.loads(pmg.build_artifacts(_REPO)[pmg.MAP_REL])
    for node in (
        program_map["nodes"]["claims"] + program_map["nodes"]["studies"]
    ):
        assert node["class"] != "in_flight"
    (restricted_node,) = [
        n for n in program_map["nodes"]["studies"] if n["restricted"]
    ]
    assert restricted_node["id"] == "072-fish-family-profiles-redesign"
    assert restricted_node["class"] is None
    assert (
        restricted_node["standing"]
        == pmg.RESTRICTED_NAME_ONLY["072-fish-family-profiles-redesign"]
    )
    assert "member_counts" not in restricted_node


def test_taxonomy_hygiene_against_live_inputs():
    tax = json.loads((_REPO / pmg.TAXONOMY_REL).read_text(encoding="utf-8"))
    for key_path in pmg._walk_keys(tax):
        key = key_path.rsplit(".", 1)[-1].split("[")[0]
        assert key not in pmg.FORBIDDEN_TAXONOMY_KEYS
    assert tax["version"] == pmg.TAXONOMY_VERSION
    assert {s["spec_dir"] for s in tax["studies"]} == set(_spec_dirs())
    assert {e["document"] for e in tax["extracted_documents"]} == set(
        _recompute()["documents"]
    )
    assert tax["restricted"] == ["072-fish-family-profiles-redesign"]
    domain_totals = {
        domain: sum(1 for s in tax["studies"] if s["domain"] == domain)
        for domain in tax["domains"]
    }
    assert domain_totals == {
        "Anchors & readings": 13,
        "Claim families by study line": 40,
        "Contact zone & external corpora": 2,
        "Program infrastructure": 17,
        "Sign inventory & corpus": 17,
    }
    program_map = json.loads(pmg.build_artifacts(_REPO)[pmg.MAP_REL])
    for domain, block in program_map["coverage"]["domains"].items():
        assert block["studies"] == domain_totals[domain]
    assert set(program_map["coverage"]["domains"]) == set(tax["domains"])


def test_committed_artifacts_match_fresh_build():
    # Stage S2 (T201): --check against the real root — the
    # committed program-map.json + program-map-finds.json
    # are byte-identical to a fresh build over the live
    # inputs, or this names the drifted artifact.
    assert pmg.check_outputs(_REPO) == []


def test_check_semantics_on_tmp_copy(tmp_path):
    ledger = (_REPO / pmg.LEDGER_REL).read_bytes()
    (tmp_path / "glossa-indus" / "ledger").mkdir(parents=True)
    (tmp_path / "glossa-indus" / "map").mkdir(parents=True)
    (tmp_path / "glossa-indus" / "ledger" / "claims.jsonl").write_bytes(ledger)
    (tmp_path / "glossa-indus" / "map" / "program-map-taxonomy.json").write_bytes(
        (_REPO / pmg.TAXONOMY_REL).read_bytes()
    )
    (tmp_path / "specs").mkdir()
    for name in _spec_dirs():
        (tmp_path / "specs" / name).mkdir()
    pmg.write_outputs(tmp_path)
    assert pmg.check_outputs(tmp_path) == []
    map_path = tmp_path / pmg.MAP_REL
    map_path.write_bytes(map_path.read_bytes() + b" ")
    assert pmg.check_outputs(tmp_path) == [pmg.MAP_REL]
