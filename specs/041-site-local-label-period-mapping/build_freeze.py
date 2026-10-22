#!/usr/bin/env python3
"""Build the Spec 041 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-22 and run exactly once, in that act,
to compute the freeze digest over the recovered
register (0.8-draft) and the finalised freeze
texts (the Spec 035 ordering: the AEE lifecycle
hooks first, the digest after). Run with the
Glossa backend venv python from the repository
root:

    python specs/041-site-local-label-period-mapping/build_freeze.py

Writes specs/041-site-local-label-period-mapping/freeze.json
(framework026 build_freeze payload: definition +
source hashes + environment, digest = SHA-256 of
the canonical JSON serialisation) and prints the
digest.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.framework026 import build_freeze  # noqa: E402

SPEC_DIR = "specs/041-site-local-label-period-mapping"

DEFINITION = {
    "spec": "specs/041-site-local-label-period-mapping/spec.md",
    "freeze_doc": "specs/041-site-local-label-period-mapping/freeze.md",
    "experiment_id": "spec041-site-local-label-period-mapping",
    "register": {
        "path": "specs/041-site-local-label-period-mapping/claims.json",
        "register_version": "0.8-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-22 "
            "under aee 1.5.0: after_specify, "
            "after_plan, and after_tasks each carry "
            "15 failure modes, all FR-2.3 draft-cap "
            "records, with zero correctness failure "
            "modes and no claim below the 0.70 "
            "threshold (minimum propagated 0.72); "
            "the engine outcome word reads iterate "
            "solely from the draft-cap records (gate "
            "reading DD-041-15, adopting DD-038-10; "
            "record in "
            "specs/041-site-local-label-period-mapping/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/041-site-local-label-period-mapping/adjudication.md"
        ),
        "decisions": (
            "The draft was commissioned by the "
            "owner's order of 2026-10-21 (the act "
            "Spec 040's closure record section 3 "
            "named) and frozen on 2026-10-22 under "
            "the owner's instruction to resolve the "
            "program's open pull requests. Freeze "
            "decisions DD-041-10 to DD-041-15 are "
            "recorded in adjudication.md section 6: "
            "no single sensitivity label frozen (the "
            "determination set is the frozen "
            "sensitivity basis); source-acquisition "
            "scope (a); the spec's own OSF contract "
            "registration filed at the freeze; "
            "Phase-435 allocated; the DD-038-10 AEE "
            "gate reading adopted. DD-041-13's two "
            "reservations (the row-level derivation; "
            "the section 1 substitution) stand "
            "expressly undecided, for a future Spec "
            "040 freeze. Execution is not ordered by "
            "the freeze and has not started."
        ),
    },
    "design": {
        "phase": "Phase-435",
        "act": (
            "produce a frozen, machine-readable "
            "mapping keyed site x the layer's "
            "recorded local chronological label(s) "
            "to one coarse period (or UNASSIGNED), "
            "every mapping carrying its published "
            "citation and locator and contested "
            "flag, covering the seven G1 population "
            "sites, built to Spec 040 section 4's "
            "interface under published "
            "determinations only"
        ),
        "evidence_standard": {
            "source": (
                "the owner's 2026-10-20 decision "
                "(Spec 039, Option 1), carried: "
                "published period determinations "
                "only"
            ),
            "venue_locator_test": (
                "DD-039-3 carried verbatim in "
                "substance: a determination counts "
                "as published iff it appears, with a "
                "locator (page or table), in a "
                "peer-reviewed journal article, its "
                "published supplementary material, "
                "or a published excavation or survey "
                "report in a named series; doubtful "
                "venues default to not counting"
            ),
            "verification_bar": (
                "a determination is verified only "
                "when read in the publication's own "
                "text, or in a published restatement "
                "quoting it with pagination; "
                "anything else is a locator aid and "
                "never grounds a cell"
            ),
            "forbidden": [
                "radiocarbon-to-period conversion",
                "inheritance from the chronology spine's dated contexts",
                "borrowing a site-level label for a local label",
                "the Phase-139 chron_band or its citation register as a determination",
                "analyst reconciliation of sources",
            ],
        },
        "cell_schema": {
            "key": (
                "site (layer string, verbatim) x "
                "field (period | phase) x local_label "
                "(verbatim, query and span marks "
                "intact)"
            ),
            "values": ["EARLY", "MATURE", "LATE", "UNASSIGNED"],
            "statuses": ["MAPPED", "CONTESTED", "UNASSIGNED"],
            "unassigned_reasons": [
                "NO_PUBLISHED_DETERMINATION",
                "DETERMINATION_UNVERIFIED",
                "SPANS_COARSE_BOUNDARY",
                "NOT_IN_PUBLISHED_SCHEME",
                "LABEL_UNCERTAIN_IN_LAYER",
            ],
            "sensitivity_label": (
                "DD-041-10: no single label frozen; "
                "the field is reserved, nullable; "
                "the determination set is the frozen "
                "sensitivity basis"
            ),
            "completeness": (
                "every (site, field, local_label) "
                "triple attested on a population row "
                "appears exactly once; checked "
                "mechanically against the step-0 "
                "census"
            ),
        },
        "step0_gates": {
            "G0.1": "layer identity at the section 4 pin (fail-closed)",
            "G0.2": "population reproduction: seven sites, 5,410 rows",
            "G0.3": (
                "label census reproducing the "
                "recorded tables exactly (period "
                "2,266; phase 2,638; both 1,788; "
                "union 3,116) and the covariates "
                "copy asserted against the layer"
            ),
            "G0.4": "anchors at the refreshed pin, before and after",
            "G0.5": "source admissibility classified before extraction",
            "G0.6": "no-computation fence: margins and census only",
        },
        "construction": {
            "precedence": (
                "none: Phase-139's period-wins rule "
                "is not carried; every attested cell "
                "is resolved on its own evidence or "
                "is UNASSIGNED with its reason"
            ),
            "contested": (
                "two admissible determinations "
                "assigning different coarse periods "
                "make the cell CONTESTED, both "
                "retained verbatim, binding value "
                "UNASSIGNED; no preference rule "
                "applies"
            ),
            "dual_verification": (
                "every MAPPED or CONTESTED cell "
                "independently re-verified at its "
                "locator before the artifact is "
                "pinned; reclassifications recorded, "
                "never edited into agreement"
            ),
            "acquisition_scope": (
                "DD-041-11 (a): sources already held "
                "plus interlibrary access under the "
                "program's existing caps and gates; "
                "unreached cells land at "
                "DETERMINATION_UNVERIFIED and are "
                "counted"
            ),
        },
        "row_derivation": (
            "DD-041-13 RESERVED to a future Spec "
            "040 freeze: the coverage report "
            "publishes placement counts under "
            "derivations A1 / A2 / B / C and adopts "
            "none"
        ),
        "deliverables": [
            "the step-0 record and value-level census (committed)",
            "data/evidence_integration/site_period_mapping.jsonl + site_period_mapping_meta.json, SHA-256 pinned in the outcome record",
            "the coverage report (cell counts; A1/A2/B/C placement counts; the 57.6% ceiling; the dual-verification record)",
            "the outcome record in this directory; the experiment-graph node for Phase-435; the LEDGER entry",
        ],
        "execution_gate": (
            "NOT satisfied: no execution order "
            "exists for this contract; the freeze "
            "itself constructs no cell, computes no "
            "census, and produces no artifact"
        ),
    },
    "inputs": {
        "layer": {
            "file": "horus84 inscriptions.csv (ICIT-lineage layer)",
            "sha256": "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
            "rows": 5679,
            "fields": 38,
            "bytes": 1190884,
            "pin_state_at_freeze": (
                "not producible on the freeze "
                "machine (the loader's default-path "
                "copy is absent); the pin stands on "
                "the records of record (Spec 025 "
                "section 3; Phase-139/140 "
                "reproductions; held-copy "
                "verifications at the Spec 060 and "
                "Spec 067 freezes) and gate G0.1 "
                "re-asserts it fail-closed at "
                "execution"
            ),
        },
        "population": {
            "rule": (
                "Phase-137: sites eligible at >= 30 "
                "inscriptions AND >= 100 parsed "
                "tokens; rows with >= 1 parsed token"
            ),
            "rows": 5410,
            "eligible_sites": [
                "Chanhu-daro",
                "Dholavira",
                "Harappa",
                "Kalibangan",
                "Lothal",
                "Mohenjo-daro",
                "Nausharo",
            ],
            "label_coverage": {
                "period": 2266,
                "phase": 2638,
                "both": 1788,
                "either": 3116,
                "neither": 2294,
            },
        },
        "covariates": {
            "file": "data/evidence_integration/phase139_harmonized_covariates.json",
            "sha256": "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413",
            "bytes": 2665622,
            "role": (
                "convenience copy of period_raw / "
                "phase_raw per population "
                "inscription; the layer is the source "
                "of record and step 0 asserts the "
                "copy against it (G0.3)"
            ),
        },
        "citation_register": {
            "file": "data/evidence_integration/phase139_citation_register.json",
            "role": "locator aid only; never a determination source",
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "bytes": 570344,
            "rule": "asserted byte-identical before and after any execution",
        },
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": (
            "1.5.0 (adopted environment, PR #231; "
            "package pinned >=1.5.0,<1.6)"
        ),
        "specify": "1.0.10",
    },
}

SOURCES = [
    f"{SPEC_DIR}/freeze.md",
    f"{SPEC_DIR}/spec.md",
    f"{SPEC_DIR}/claims.json",
    f"{SPEC_DIR}/adjudication.md",
    f"{SPEC_DIR}/aee/freeze-aee-note.md",
    f"{SPEC_DIR}/build_freeze.py",
    "backend/tests/test_spec041_freeze.py",
]


def main() -> int:
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / SPEC_DIR / "freeze.json"
    out.write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8"
    )
    print(record["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
