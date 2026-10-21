"""Spec 044 freeze fences (fish-sign coastal residue).

Pins: (1) the freeze machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - the layer of record identified
and pinned at the freeze (OPEN-044-1: the Holdat
corpus file the Phase-45/46/54 scripts read, with
its population reproduction), Asset F's contract
and its consumer (Spec 048, design D-04 - the
draft's Spec 045 name corrected at the freeze),
the coastal-list rule with Lothal and Dholavira
by name, the test form (token primary, Fisher
one-sided, Bonferroni, ratio 1.5, floor 30), the
seven-class outcome set, the OSF decision under
campaign E-1, and Phase-404; (3) the governed
claim register is the frozen register (15 claims,
integrity-clean, recovered to 0.7-draft at the
freeze gate) and the three freeze-hook artifacts
record the pass on the DD-044-9 reading (zero
correctness failure modes; only FR-2.3 draft-cap
records; no claim below the 0.70 threshold);
(4) the cited records still carry the facts the
design rests on (the claim file and manual_002's
state, the gazetteer pin and census, the
crosswalk's Parpola citation and pin, the anchors
pin, the Phase-45 T6 line, the scripts' corpus
path, and the 179-inscription layer's inability
to carry a site test). These tests count no fish
sign, build no asset, and change no record.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/044-fish-sign-coastal-residue"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
CLAIM_FILE = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "indus_valley_script_deciphered_from_myth_"
    "65ff0a26.json"
)
GAZETTEER = REPO / "data/movement/gazetteer_rows.jsonl"
CROSSWALK = (
    REPO / "backend/glossa_lab/data/"
    "mahadevan_parpola_crosswalk.json"
)
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
PHASE45 = REPO / "backend/scripts/phase45_fish_coastal_test.py"
PHASE46 = REPO / "backend/scripts/phase46_t4_fish_expansion.py"
PHASE54 = REPO / "backend/scripts/phase54_falsification.py"
INDUS_CISI = REPO / "backend/glossa_lab/data/indus_cisi.py"
HOLDAT = (
    REPO / "corpora/downloads/external_repos/"
    "holdatllc_indus/indus_corpus 2.csv"
)

CLAIM_SHA256 = (
    "bc22d6f010f800d608d6e3f620fb430b3cf8d3ccd3ca"
    "adc6a989116fbfd125ed"
)
GAZETTEER_SHA256 = (
    "5ac76a3031121a61fa39f87b1d2760855374d171ddd0"
    "36988fee2820dca9b8b6"
)
CROSSWALK_SHA256 = (
    "9ebd7723472d888dc8a127ff840a108d4fbd546f7f8"
    "ed28ccc6e06444a2dc69b"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580"
    "088e6086592b32d34f569"
)
LAYER_SHA256 = (
    "62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3"
    "f5e85d1f7f40cbe28218e"
)

sys.path.insert(0, str(REPO / "backend"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == (
        "spec044-fish-sign-coastal-residue"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "1.5.0" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase-404"
    # The claim and its standing verdict.
    claim = design["claim"]
    assert claim["id"] == (
        "indus_valley_script_deciphered_from_myth_"
        "65ff0a26_manual_002"
    )
    assert "partially falsified" in claim["state"]
    assert "not re-opened" in claim["state"]
    # The layer of record, identified at the freeze.
    layer = design["layer_of_record"]
    assert layer["sha256"] == LAYER_SHA256
    assert layer["inscriptions"] == 1670
    assert layer["token_rows"] == 7002
    assert layer["key"] == "cisi_number"
    repro = layer["reproduction"]
    assert repro["m047_tokens"] == 13
    assert repro["m047_inscriptions"] == 13
    assert repro["fisher_p"] == 0.685
    assert repro["table"] == {
        "coastal_with": 2,
        "inland_with": 10,
        "coastal_without": 228,
        "inland_without": 1369,
    }
    # Asset F: source, membership rule, consumer.
    asset = design["asset_f"]
    assert "fig. 5.1" in asset["source"]
    assert "DD-044-5" in asset["membership"]
    assert "Spec 048 (design D-04)" in asset["consumer"]
    assert "corrected at the freeze" in asset["consumer"]
    # The coastal list: rule-built, named pair.
    coastal = design["coastal_list"]
    assert coastal["named_members"] == ["Lothal", "Dholavira"]
    assert "no site is classed by its fish counts" in (
        coastal["contested"]
    )
    # The test form, carried not softened.
    test = design["test"]
    assert "sign token" in test["unit"]
    assert "Fisher" in test["exact_test"]
    assert "one-sided" in test["exact_test"]
    assert "Bonferroni" in test["correction"]
    assert "at least 1.5" in test["criterion"]
    assert "below 0.05" in test["criterion"]
    assert test["floor"] == 30
    assert design["outcomes"] == [
        "ENRICHED MEMBER FOUND",
        "NO MEMBER ENRICHED",
        "TOO THIN",
        "ASSET F FREEZE FAILED",
        "LAYER NOT PINNABLE",
        "COASTAL LIST FAILED",
        "INVALID",
    ]
    # The fences and the execution gate.
    assert "Roif hold" in design["fences"]
    assert "awaits the verified approval" in (
        design["execution_gate"]
    )
    assert "no count was made at the freeze" in (
        design["execution_gate"]
    )
    # Inputs.
    inputs = definition["inputs"]
    assert inputs["claim_file"]["sha256"] == CLAIM_SHA256
    assert inputs["claim_file"]["claim_status"] == (
        "partially_falsified"
    )
    assert inputs["gazetteer"]["sha256"] == GAZETTEER_SHA256
    assert inputs["gazetteer"]["rows"] == 36
    assert inputs["gazetteer"]["program_sites"] == 30
    assert inputs["crosswalk"]["sha256"] == CROSSWALK_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.7-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F044-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_consumer_correction_on_the_record():
    spec = (SPEC / "spec.md").read_text(encoding="utf-8")
    adjudication = (SPEC / "adjudication.md").read_text(
        encoding="utf-8"
    )
    tasks = (SPEC / "tasks.md").read_text(encoding="utf-8")
    # Asset F's consumer is Spec 048 (design D-04).
    flat = " ".join(spec.split())
    assert "Spec 048 (design D-04) consumes it by digest" in flat
    assert "**Spec 048** (design D-04), not Spec 045" in flat
    # No live consumer reference names Spec 045; the
    # only Spec 045 mentions are the correction
    # record itself (adjudication section 7.1 and
    # the freeze header naming the error).
    assert "Spec 045 (design D-04) will consume" not in spec
    assert "Spec 045 (design D-04)\nconsumes" not in spec
    assert "Spec 048's (D-04)" in adjudication
    assert "Spec 048's" in tasks
    assert "7.1 Consumer-name correction" in adjudication


def test_cited_records_carry_the_design_facts():
    # The claim file: pin, entry, standing state.
    assert _sha(CLAIM_FILE) == CLAIM_SHA256
    claim_doc = json.loads(CLAIM_FILE.read_text(encoding="utf-8"))
    entries = [
        c for c in claim_doc["claims"]
        if c["claim_id"] == (
            "indus_valley_script_deciphered_from_myth_"
            "65ff0a26_manual_002"
        )
    ]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["claim_status"] == "partially_falsified"
    assert entry["stage"] == "explained"
    assert "fish family covers several distinct signs" in (
        entry["not_understood"]
    )
    # The gazetteer: pin and census.
    raw_bytes = GAZETTEER.read_bytes()
    assert hashlib.sha256(raw_bytes).hexdigest() == (
        GAZETTEER_SHA256
    )
    rows = [
        json.loads(line)
        for line in raw_bytes.decode("utf-8").splitlines()
        if line.strip()
    ]
    assert len(rows) == 36
    assert len({r["program_site_id"] for r in rows}) == 30
    # The crosswalk: pin and the Parpola citation.
    assert _sha(CROSSWALK) == CROSSWALK_SHA256
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    refs = " ".join(crosswalk["_citation"]["full_references"])
    assert "fig. 5.1, pp. 70-78" in refs
    # The anchors file: pin asserted at the freeze.
    assert _sha(ANCHORS) == ANCHORS_SHA256
    # The original test's record and shape.
    phase46 = PHASE46.read_text(encoding="utf-8")
    assert "NO_ENRICHMENT for M047" in phase46
    assert "n=13, p=0.685" in phase46
    for script in (PHASE45, PHASE46, PHASE54):
        text = script.read_text(encoding="utf-8")
        assert "holdatllc_indus" in text
        assert "indus_corpus 2.csv" in text
        assert "cisi_number" in text
    # The repo's other CISI layer cannot carry a
    # site test: 179 inscriptions, all Mohenjo-daro.
    cisi = INDUS_CISI.read_text(encoding="utf-8")
    assert "179 inscription sides (all Mohenjo-daro" in cisi


def test_held_layer_reproduces_the_original_population():
    # The layer of record is a held downloads-tree
    # file, not a repository file: where a checkout
    # holds it, its pin and the original population
    # must reproduce; where it does not (a fresh CI
    # checkout), the freeze record's constants are
    # the standing record and this check is inert.
    if not HOLDAT.exists():
        return
    assert _sha(HOLDAT) == LAYER_SHA256
    seals: dict[str, dict] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cisi = row["cisi_number"]
            if cisi not in seals:
                seals[cisi] = {
                    "site": row.get("site", "").strip(),
                    "signs": [],
                }
            seals[cisi]["signs"].append(row["letters"])
    assert len(seals) == 1670
    assert sum(len(v["signs"]) for v in seals.values()) == 7002
    assert sum(
        v["signs"].count("M047") for v in seals.values()
    ) == 13
    coastal = {"lothal", "dholavira"}
    inland = {
        "mohenjo-daro", "harappa", "kalibangan",
        "chanhu-daro", "rakhigarhi", "banawali",
        "sutkagen-dor", "shortugai",
    }

    def _class(site: str):
        s = site.lower()
        if any(c in s for c in coastal):
            return True
        if any(i in s for i in inland):
            return False
        return None

    a = b = c = d = 0
    for v in seals.values():
        label = _class(v["site"])
        if label is None:
            continue
        has = "M047" in v["signs"]
        if label and has:
            a += 1
        elif label:
            c += 1
        elif has:
            b += 1
        else:
            d += 1
    assert (a, b, c, d) == (2, 10, 228, 1369)
    # Fisher's exact test, two-sided, by direct
    # hypergeometric enumeration (the Phase-45
    # script's test on this table).
    n = a + b + c + d
    row1, col1 = a + b, a + c

    def _hyp(x: int) -> float:
        if not (0 <= x <= row1 and 0 <= col1 - x <= n - row1):
            return 0.0
        return (
            math.comb(row1, x)
            * math.comb(n - row1, col1 - x)
            / math.comb(n, col1)
        )

    p_obs = _hyp(a)
    lo = max(0, col1 - (n - row1))
    hi = min(row1, col1)
    p_val = sum(
        _hyp(x) for x in range(lo, hi + 1)
        if _hyp(x) <= p_obs + 1e-12
    )
    assert round(p_val, 3) == 0.685


FREEZE_STAMPS = [
    "20261021T095745Z",
    "20261021T095751Z",
    "20261021T095752Z",
]

CORRECTNESS_CATEGORIES = {
    "coverage_gap",
    "contradiction",
    "assumption_unvalidated",
    "ambiguous_requirement",
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
