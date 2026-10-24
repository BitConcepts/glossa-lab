"""Spec 047 freeze fences (Roif ledger distribution test).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the distribution-component
fence, the Asset B contract (the six-class
vocabulary, the pooled and contrast groupings, the
two-source agreement rule, the dispute statuses
with no tiebreak, the build gates B1-B4, the
unsound-asset rule), the step-0 gates, the
pre-registered measures and verdict partition
(9,999 shuffles, seed 20261021, the 12-site
classification gate), the freeze rulings
DD-047-8 to DD-047-16 (the second corpus layer
unused; D-10 proceeds against a thin asset; the
spine-only population confirmed; the all-UNMAPPED
partition; the Roif publication hold), and
Phase-406; (3) the governed claim register is the
frozen register (19 claims, integrity-clean,
recovered to 0.7-draft at the freeze gate) and the
three freeze-hook artifacts record the pass on the
DD-047-16 reading (zero correctness failure modes;
only FR-2.3 draft-cap records; no claim below the
0.70 threshold); (4) the cited records still carry
the facts the design rests on (every spec section
2 pin, verified at the freeze by two independent
routes; the gazetteer census; the corpus census;
the Phase-104 UNTESTED / RULE-SITE entry; the
citation record's Roif key; the hypothesis-model
file's recorded defect; Spec 027's gazetteer
discipline). These tests classify no site,
extract no ledger-sign list, and count no
inscription by site class.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/047-roif-ledger-distribution"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
GAZETTEER = REPO / "data/movement/gazetteer_rows.jsonl"
CORPUS = REPO / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
CROSSWALK = REPO / "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv"
PHASE104 = REPO / "glossa-indus/reports/phase104_claims_evaluation.json"
SEED_CITATIONS = REPO / "backend/scripts/seed_citations.py"
MODEL_YAML = (
    REPO / "glossa-indus/hypotheses/models/roif_guild_ledger.yaml"
)
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
SPEC027 = REPO / "specs/027-movement-culture-language/spec.md"

GAZETTEER_SHA256 = (
    "5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6"
)
CORPUS_SHA256 = (
    "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
)
CROSSWALK_SHA256 = (
    "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
)
PHASE104_SHA256 = (
    "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d"
)
CITATION_SHA256 = (
    "39d28112e21151ccba0f5a370801c78d87575c6ff61695bb8fafc5c14c08b8f9"
)
MODEL_SHA256 = (
    "c5f08461cc1a37b91cb5a17981e2e4d7c02958312e1e7b6b9a49618a154c9586"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
SPEC027_SHA256 = (
    "7fff5d5a90b0af5697afa17a631e6901702b521f7e61c3c2bb444f08e369f9b0"
)
CLAIM_ID = "indus_valley_script_deciphered_from_myth_65ff0a26_manual_001"

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == (
        "spec047-roif-ledger-distribution"
    )
    assert definition["register"]["claims"] == 19
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-406"
    # The claim and its component fence, carried not softened.
    claim = design["claim_under_test"]
    assert claim["id"] == CLAIM_ID
    assert claim["component_tested"] == (
        "the distribution component only"
    )
    assert claim["components_not_tested"] == [
        "guild authority",
        "Akkadian influence",
    ]
    assert "RULE-SITE" in claim["record"]
    # Asset B: the frozen contract.
    asset = design["asset_b"]
    assert asset["classes"] == [
        "gateway/border",
        "administrative",
        "port/trade",
        "domestic",
        "ritual",
        "mixed/unknown",
    ]
    assert asset["pooled_class"]["name"] == "ADMIN-TRADE-GATEWAY"
    assert asset["pooled_class"]["members"] == [
        "gateway/border",
        "administrative",
        "port/trade",
    ]
    assert asset["contrast_class"] == ["domestic", "ritual"]
    assert set(asset["build_gates"]) == {"B1", "B2", "B3", "B4"}
    assert "exactly 30 rows" in asset["build_gates"]["B1"]
    assert "unsound" in asset["unsound_rule"]
    assert "no majority rule" in asset["no_tiebreak"]
    assert "DD-047-1" in asset["thinness"]
    assert asset["dispute_statuses"] == [
        "DISAGREED",
        "SINGLE-SOURCE",
        "NO-SOURCE",
        "AGREED at mixed/unknown",
    ]
    # The ledger-sign list and its freeze ruling.
    ledger = design["ledger_sign_list"]
    assert "Academia.edu postings" in ledger["source"]
    assert "DD-047-13" in ledger["all_unmapped"]
    # Step 0 stays fail-closed.
    gates = design["step0_gates"]
    assert "INVALID" in gates["input_integrity"]
    assert "36 rows" in gates["spine_reproduction"]
    assert "exactly one" in gates["join_census"]
    # The test: measures, permutation, gate, partition.
    test = design["test"]
    perm = test["permutation"]
    assert perm["shuffles"] == 9999
    assert perm["level"] == 0.05
    assert perm["seed"] == 20261021
    gate = test["classification_gate"]
    assert gate["min_testable_sites"] == 12
    assert "DD-047-2" in gate["empty_side"]
    assert "no distribution quantity" in gate["outcome"]
    crit = test["criteria"]
    assert crit["supported"] == (
        "R >= 1.5 and p < 0.05 and R_ledger > 1.0"
    )
    assert "R <= 1.0" in crit["not_supported"]
    assert "does not reject" in crit["not_supported"]
    assert "DD-047-13" in test["all_unmapped_partition"]
    assert "R_ledger is not computed" in test["all_unmapped_partition"]
    assert "DD-047-9" in test["second_corpus_layer"]
    assert "unused" in test["second_corpus_layer"]
    assert "DD-047-11" in test["d10_against_thin_asset"]
    assert "DD-047-14" in test["classification_audit"]
    # The Roif hold stands in the frozen definition.
    assert "held under the Roif gate" in design["roif_gate"]
    assert "R-7" in design["roif_gate"]
    # The execution gate is not satisfied by the freeze itself.
    assert "Not satisfied at the freeze" in design["execution_gate"]
    assert "approval click" in design["execution_gate"]
    assert "no site was classified" in design["execution_gate"]
    # Inputs: every section 2 pin, as verified two-route at the freeze.
    inputs = definition["inputs"]
    assert inputs["gazetteer"]["sha256"] == GAZETTEER_SHA256
    assert inputs["gazetteer"]["rows"] == 36
    assert inputs["gazetteer"]["program_sites"] == 30
    assert inputs["primary_corpus_layer"]["sha256"] == CORPUS_SHA256
    assert inputs["primary_corpus_layer"]["records"] == 5679
    assert inputs["sign_crosswalk"]["sha256"] == CROSSWALK_SHA256
    p104 = inputs["phase104_evaluation"]
    assert p104["sha256"] == PHASE104_SHA256
    assert p104["claim_id"] == CLAIM_ID
    assert p104["verdict"] == "stays_untested"
    assert p104["rule"] == "RULE-SITE"
    assert inputs["citation_record"]["sha256"] == CITATION_SHA256
    assert inputs["citation_record"]["key"] == "roif_indus_ledger"
    assert inputs["hypothesis_model_file"]["sha256"] == MODEL_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert inputs["spec027_spec"]["sha256"] == SPEC027_SHA256
    assert "two independent routes" in inputs["pin_verification"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F047-C{i:02d}" for i in range(1, 20)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def _find_claim(node, claim_id):
    if isinstance(node, dict):
        if node.get("claim_id") == claim_id:
            return node
        for value in node.values():
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_claim(value, claim_id)
            if found is not None:
                return found
    return None


def test_cited_records_carry_the_design_facts():
    # The gazetteer spine: pin, census, cluster count.
    raw_bytes = GAZETTEER.read_bytes()
    assert hashlib.sha256(raw_bytes).hexdigest() == GAZETTEER_SHA256
    rows = [
        json.loads(line)
        for line in raw_bytes.decode("utf-8").splitlines()
        if line.strip()
    ]
    assert len(rows) == 36
    assert len({r["program_site_id"] for r in rows}) == 30
    # The primary corpus layer: pin, census, site column.
    corpus_bytes = CORPUS.read_bytes()
    assert hashlib.sha256(corpus_bytes).hexdigest() == CORPUS_SHA256
    corpus_lines = corpus_bytes.decode("utf-8").splitlines()
    header = corpus_lines[0].split(",")
    assert "site" in header
    assert "text" in header
    assert len([l for l in corpus_lines[1:] if l.strip()]) == 5679
    # The crosswalk and the anchors file: pins only.
    assert (
        hashlib.sha256(CROSSWALK.read_bytes()).hexdigest()
        == CROSSWALK_SHA256
    )
    assert (
        hashlib.sha256(ANCHORS.read_bytes()).hexdigest()
        == ANCHORS_SHA256
    )
    # The Phase-104 record: the claim stands UNTESTED under RULE-SITE.
    p104_bytes = PHASE104.read_bytes()
    assert hashlib.sha256(p104_bytes).hexdigest() == PHASE104_SHA256
    entry = _find_claim(json.loads(p104_bytes), CLAIM_ID)
    assert entry is not None
    assert entry["verdict"] == "stays_untested"
    assert entry["rule"] == "RULE-SITE"
    assert "site-typology" in entry["reason"]
    assert "site names only" in entry["reason"]
    # The citation record: the Roif key as described in spec section 2.
    cit_bytes = SEED_CITATIONS.read_bytes()
    assert hashlib.sha256(cit_bytes).hexdigest() == CITATION_SHA256
    cit = cit_bytes.decode("utf-8")
    i = cit.index("roif_indus_ledger")
    block = cit[i:i + 700]
    assert '"authors": "Roif, A."' in block
    assert '"venue": "Academia.edu"' in block
    assert '"year": ""' in block
    assert '"doi": ""' in block
    assert '"url": "https://www.academia.edu/"' in block
    # The hypothesis-model file: pin and the recorded defect.
    model_bytes = MODEL_YAML.read_bytes()
    assert hashlib.sha256(model_bytes).hexdigest() == MODEL_SHA256
    model = model_bytes.decode("utf-8")
    assert 'document_id: indus_valley_script_deci.pdf"' in model
    assert 'doi: "10.2307/595168"' in model
    # Spec 027's gazetteer discipline.
    spec027_bytes = SPEC027.read_bytes()
    assert hashlib.sha256(spec027_bytes).hexdigest() == SPEC027_SHA256
    spec027 = " ".join(spec027_bytes.decode("utf-8").split())
    assert "program_site_id" in spec027
    assert "No majority vote" in spec027


FREEZE_STAMPS = [
    "20261021T095753Z",
    "20261021T095802Z",
    "20261021T095804Z",
]

CORRECTNESS_CATEGORIES = {
    "coverage_gap",
    "contradiction",
    "assumption_unvalidated",
    "ambiguous_requirement",
    "independence_unmodeled",
}


def test_freeze_hook_artifacts_record_the_pass():
    aee_dir = SPEC / "aee"
    for phase, stamp in zip(
        ("after_specify", "after_plan", "after_tasks"),
        FREEZE_STAMPS,
    ):
        record = json.loads(
            (aee_dir / f"aee-{phase}-{stamp}.json").read_text(
                encoding="utf-8")
        )
        failures = [
            f for c in record["claims"] for f in c["failures"]
        ]
        assert failures, phase
        assert {f["category"] for f in failures} <= {"draft_cap"}, phase
        assert not [
            f for f in failures
            if f["category"] in CORRECTNESS_CATEGORIES
        ], phase
        confidences = [c["confidence"] for c in record["claims"]]
        assert min(confidences) >= 0.70, phase
