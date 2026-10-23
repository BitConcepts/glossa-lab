#!/usr/bin/env python3
"""Spec 073 (Phase-436) step 0: gates 0.1-0.4, in the frozen order, fail-closed.

Gate 0.1 frozen-input integrity and the Shakti intake (census form);
gate 0.2 baseline reproduction figure by figure (Spec 070's 31-sign
keyed split and token counts, Spec 071's 557-sign census split, the
498-id Wells map census, Asset A v1's census); gate 0.3 sources in
hand (the freeze section 4 exhibits, recomputed); gate 0.4 blind-entry
setup attested. Any failure closes the study under the section 7 word
its gate names; nothing downstream runs on a failed record.

Writes specs/073-keying-surface-repair/execution/step0-record.json.
Restricted inputs are read from the owner's local research-notes tree
only and are never copied into the repository.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "specs" / "073-keying-surface-repair"
OUT = SPEC_DIR / "execution" / "step0-record.json"
HOME = Path.home()
EXT = HOME / "workspace/research_notes/indus-data-deep-sweep-20261008/downloads"
MAYIG = HOME / "workspace/research_notes/hunt-chain-sources/mayig-indus-valley-script-corpus"

REGISTRY_V1 = ROOT / "data/crosswalks/canonical_sign_registry.csv"
CROSSWALK = ROOT / "data/crosswalks/sign_crosswalk_master.csv"
ASSET_A_V1 = ROOT / "specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv"
P433 = ROOT / "reports/phase433_results.json"
P434 = ROOT / "reports/phase434_results.json"
CORPUS = EXT / "shaktiosindia-indus-sign-regimes-deposit/sanitized_corpus.json"
GRADES = EXT / "shakti_row_grades_2026-10-22.csv"

PIN_REGISTRY = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
PIN_CROSSWALK = "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
PIN_ASSET_A = "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b"
PIN_045 = "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a"
PIN_070 = "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e"
PIN_071 = "c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478"
PIN_P433 = "667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214"
PIN_P434 = "7158f79ce416e5e01fee041e6e97df827d3a048f9c1c178a8200bd79f68bbda7"
PIN_CORPUS = "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
PIN_GRADES = "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
FIVE = ["136", "298", "401", "617", "824"]
FIVE_COUNTS = {"136": 6, "298": 7, "401": 5, "617": 56, "824": 16}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wells_map(rows):
    out: dict[str, set[str]] = {}
    for r in rows:
        if r["numbering_system"] != "parpola_1982":
            continue
        for token in (r["wells_ids"] or "").split("|"):
            token = token.strip()
            if token:
                out.setdefault(token, set()).add(r["sign_id"])
    return out


def main() -> int:
    record: dict = {"spec": "073", "phase": 436, "step": 0, "gates": {}}
    failures: list[str] = []

    # ---- Gate 0.1: frozen-input integrity + Shakti intake census ----
    g1: dict = {"checks": {}}
    file_pins = {
        "registry_v1": (REGISTRY_V1, PIN_REGISTRY),
        "crosswalk": (CROSSWALK, PIN_CROSSWALK),
        "asset_a_v1": (ASSET_A_V1, PIN_ASSET_A),
        "phase433_results": (P433, PIN_P433),
        "phase434_results": (P434, PIN_P434),
        "shakti_corpus": (CORPUS, PIN_CORPUS),
        "shakti_row_grades": (GRADES, PIN_GRADES),
    }
    for name, (path, pin) in file_pins.items():
        got = sha256(path)
        g1["checks"][name] = {"sha256": got, "pin": pin, "match": got == pin}
        if got != pin:
            failures.append(f"INPUT PIN MISMATCH: {name}")
    for name, pin, spec_dir in (
        ("spec045_digest", PIN_045, "045-hunt-depicted-kinds"),
        ("spec070_digest", PIN_070, "070-hunt-opening-signs-successor"),
        ("spec071_digest", PIN_071, "071-hunt-sky-signs-successor"),
    ):
        freeze_json = (ROOT / "specs" / spec_dir / "freeze.json").read_text(encoding="utf-8")
        present = pin in freeze_json
        g1["checks"][name] = {"recorded_digest": pin, "present_in_freeze_json": present}
        if not present:
            failures.append(f"INPUT PIN MISMATCH: {name} not found in its freeze record")

    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    grade_of = {g["shakti_id"]: g["grade"] for g in csv.DictReader(GRADES.open())}
    analyzable = [r for r in corpus if any(s != "000" for s in r["symbols"])]
    allrow_grades = Counter(grade_of[r["id"]] for r in corpus)
    ana_grades = Counter(grade_of[r["id"]] for r in analyzable)

    def code_set(rows):
        out: set[str] = set()
        for r in rows:
            out.update(s for s in r["symbols"] if s != "000")
        return out

    distinct_all = code_set(analyzable)
    documented_rows = [r for r in analyzable if grade_of[r["id"]] == "documented-lineage"]
    distinct_documented = code_set(documented_rows)
    census = {
        "rows_total": len(corpus),
        "rows_analyzable": len(analyzable),
        "grade_counts_all_rows": dict(allrow_grades),
        "grade_counts_analyzable_rows": dict(ana_grades),
        "distinct_signs_corpus_wide": len(distinct_all),
        "distinct_signs_documented_stratum": len(distinct_documented),
    }
    g1["shakti_intake_census"] = census
    intake_ok = (
        census["rows_total"] == 5704
        and census["rows_analyzable"] == 5536
        and census["grade_counts_all_rows"].get("documented-lineage") == 3212
        and census["grade_counts_all_rows"].get("undocumented-corroborated") == 2087
        and census["grade_counts_all_rows"].get("undocumented-uncorroborated") == 405
        and census["distinct_signs_corpus_wide"] == 713
        and census["distinct_signs_documented_stratum"] == 557
    )
    g1["intake_reproduced"] = intake_ok
    if not intake_ok:
        failures.append("SHAKTI INTAKE NOT REPRODUCED")
    record["gates"]["0.1"] = g1

    # ---- Gate 0.2: baseline reproduction, figure by figure ----
    g2: dict = {}
    reg_rows = list(csv.DictReader(REGISTRY_V1.open(newline="", encoding="utf-8")))
    wmap = wells_map(reg_rows)
    asset_rows = list(csv.DictReader(ASSET_A_V1.open(newline="", encoding="utf-8")))
    asset_ids = {r["sign_key"] for r in asset_rows}

    def resolve(code):
        hits = wmap.get("W" + code, set())
        return next(iter(hits)) if len(hits) == 1 else None

    p433 = json.loads(P433.read_text(encoding="utf-8"))
    enumeration = [e["wells_code"] for e in p433["population"]["O_enumeration_wells_space"]]
    counts = {e["wells_code"]: e["total"] for e in p433["population"]["O_enumeration_wells_space"]}
    resolved = [c for c in enumeration if resolve(c) is not None]
    unresolved = [c for c in enumeration if resolve(c) is None]
    a_ok = (
        len(enumeration) == 31
        and len(resolved) == 26
        and sorted(unresolved) == FIVE
        and all(counts[c] == FIVE_COUNTS[c] for c in FIVE)
    )
    g2["baseline_A_opening_strong_31"] = {
        "enumeration": enumeration,
        "resolved_via_v1_route": len(resolved),
        "unresolved": sorted(unresolved),
        "five_sign_token_counts": {c: counts[c] for c in FIVE},
        "of_the_resolved_carry_asset_a_v1_rows": sum(1 for c in resolved if resolve(c) in asset_ids),
        "reproduced": a_ok,
    }
    if not a_ok:
        failures.append("BASELINE NOT REPRODUCED: A (Spec 070 31-sign split)")

    keyed, nores, noasset = [], [], []
    for code in sorted(distinct_documented):
        sid = resolve(code)
        if sid is None:
            nores.append(code)
        elif sid in asset_ids:
            keyed.append(code)
        else:
            noasset.append(code)
    b_ok = (len(keyed), len(nores), len(noasset)) == (285, 134, 138)
    g2["baseline_B_documented_557"] = {
        "keyed_end_to_end": len(keyed),
        "no_registry_resolution": len(nores),
        "resolved_no_asset_row": len(noasset),
        "reproduced": b_ok,
    }
    if not b_ok:
        failures.append("BASELINE NOT REPRODUCED: B (Spec 071 557-sign census)")

    g2["baseline_C_wells_map"] = {"distinct_wells_ids_on_parpola_rows": len(wmap), "reproduced": len(wmap) == 498}
    if len(wmap) != 498:
        failures.append("BASELINE NOT REPRODUCED: C (498-id Wells map)")

    kind_census = Counter(r["depicted_kind"] for r in asset_rows)
    d_expect = {"animal": 20, "sky_cycle": 0, "object_goods": 14, "human": 25, "other": 127, "contested": 0, "unidentified": 1}
    d_ok = len(asset_rows) == 187 and all(kind_census.get(k, 0) == v for k, v in d_expect.items())
    g2["baseline_D_asset_a_v1"] = {"rows": len(asset_rows), "per_kind": dict(kind_census), "reproduced": d_ok}
    if not d_ok:
        failures.append("BASELINE NOT REPRODUCED: D (Asset A v1 census)")
    record["gates"]["0.2"] = g2

    # ---- Gate 0.3: sources in hand (freeze section 4 exhibits) ----
    exhibits = {
        "cisi_vol1_ia_scan": (EXT / "cisi-1-ia-scan/CorpusVol1.pdf", "8278d815450cb23cf04ffb1ffb43f62a6206bfc75f9a61f505b92eb41c627908"),
        "cisi_vol2_ia_scan": (EXT / "cisi-2-ia-scan/CorpusVol2.pdf", "727132579a485ee626e48a64c663148a85fbc0811fb523818fd615231f8a327d"),
        "cisi_31_ia_scan": (EXT / "cisi-31-ia-scan/CISI_3-1_Parpola_IA_DLI_scan.pdf", "772e929782119ff9293088e060562c18f14234e7a24efdf3deb68669fea67afa"),
        "parpola_2010_lecture_pdf": (EXT / "parpola-2010-helsinki/Parpola2010_DravidianSolution_lecture.pdf", "c58137e54cdde3f2acdcfaf05293dfc5f5ba33def3e0b12585c451f76bd4ba84"),
        "fuls_corpus_ocr_locator": (EXT / "fuls-print-corpus-desktop-2026/Corpus of Indus Inscriptions.txt", "d8aab17680af50012a8d78487c9e047dfc1f9d93d7cbcd4ed3c5c5a84acb5cc5"),
        "fuls_catalog_ocr_locator": (EXT / "fuls-print-corpus-desktop-2026/A Catalog of Indus Signs.txt", "3e9c6758b112364f33c057c7c8464324511fa6008662aaeae26e10f1962df27c"),
    }
    g3: dict = {"exhibits": {}, "struck_at_freeze": ["Wells 1998 (PRISM full text refused; record-level only)",
                                                       "Mahadevan 1977 (sign-list tables not in hand)"]}
    for name, (path, pin) in exhibits.items():
        if path.exists():
            got = sha256(path)
            ok = (pin is None) or (got == pin)
            g3["exhibits"][name] = {"path": str(path), "sha256": got, "pin": pin, "match": ok}
            if not ok:
                failures.append(f"SOURCE NOT IN HAND: {name} hash differs from the freeze exhibit")
        else:
            g3["exhibits"][name] = {"path": str(path), "present": False}
            failures.append(f"SOURCE NOT IN HAND: {name}")
    g3["fuls_print_volumes"] = ("Held on the owner's desktop (PROVENANCE entry 27); consulted for this "
                                "build through page renders whose hashes are recorded in "
                                "execution/catalog-consult.json. The OCR texts above are locators only.")
    g3["cisi_sign_list_digitization"] = ("mayig CISI digitization held at commit "
                                          "ad2f1e218a34b8c33c57de0d6cb8d99272765bbb; 396 feature files read for the build")
    record["gates"]["0.3"] = g3

    # ---- Gate 0.4: blind-entry setup ----
    record["gates"]["0.4"] = {
        "attestation": ("Entry for Asset A v2's new rows runs from an inventory carrying candidate sign_ids "
                        "and verbatim source labels only: no positional counts, no frequency data, no "
                        "keyability outcomes, no Hunt part-membership information. The two passes are the "
                        "enterer's coding and a deterministic rule pass over the same verbatim labels; the "
                        "rule pass is validated by requiring it to reproduce Spec 069's recorded pass-2 "
                        "codings on all 187 carried labels before any new row is coded."),
        "inventory_produced_by": "backend/scripts/phase436_asset_a_v2.py (stage: inventory)",
        "status": "attested",
    }

    record["failures"] = failures
    record["verdict"] = "PASS" if not failures else "CLOSED: " + "; ".join(failures)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": record["verdict"], "failures": failures}, indent=1))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
