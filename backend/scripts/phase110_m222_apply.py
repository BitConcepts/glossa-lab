"""Phase-110 Part B: M222 / 'kur' disposition apply (spec 008).

Reads the verdict from reports/phase110_m222_dossier.json and
applies the pre-registered spec-008 disposition:

- Cohort A (the 109 Phase-109 restores to 'kur'): dated
  phase110_annotation restating the basis honestly +
  validation_status='premise_superseded'; under Branch 1 with the
  dossier's pure-inheritance finding, demoted LOW -> CANDIDATE.
- Cohort B (M256, M307 — same lineage, already CANDIDATE):
  annotation + status, no tier change.
- Cohort C (M157, M400 — dual derivation via Phase-252 M427):
  annotation documenting which leg stands; no status/tier change.
- M222: dated annotation recording the adjudication outcome.

Writes reports/phase110_change_register.json (Phase-109 format),
regenerates the anchors file's bookkeeping fields from the
entries, and self-verifies that the set of changed entries equals
the register's sign set.

GPU: no compute; gpu_device recorded per H20 (torch guarded).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase110-apply] gpu_device={_GPU}", file=sys.stderr)

REPO = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
DOSSIER = REPO / "reports/phase110_m222_dossier.json"
REG109 = REPO / "reports/phase109_change_register.json"
OUT_REG = REPO / "reports/phase110_change_register.json"
DATE = "2026-10-06"

ANN_A = (
    "Phase-110 (2026-10-06): M222/'kur' adjudication (spec 008, "
    "Branch 1) — PREMISE SUPERSEDED. This entry's 'kur' value was "
    "assigned by Phase-111 allograph resolution purely by "
    "inheritance from M222, whose reading at run time was 'kur' "
    "(Phase-87, DEDR_REBUS_EXTENDED); the recorded basis cites "
    "that premise verbatim (\"matches M222 ('kur', MEDIUM)\"). "
    "M222's standing sourced record is 'min'/MEDIUM (retained "
    "Phase-109 Step 1(a) on crosswalk v2.1, Parpola 1994 App. B "
    "attribution). The Phase-111 profile match carried no "
    "discriminating information: every rare-sign profile in the "
    "Holdat corpus is (I=0.000, T=0.000, M=1.000) and every "
    "recorded match is L1=0.000 (cf. Phase-132: 'parking "
    "placeholder... not a genuine phonetic reading'). Under the "
    "spec-008 rule — a derived value may not cite as its basis a "
    "premise that the anchor sign's own sourced record "
    "contradicts — the basis is restated as: Phase-111 "
    "medial-only class assignment whose M222 anchor premise is "
    "superseded by M222's sourced reading. "
    "validation_status='premise_superseded'; confidence demoted "
    "LOW -> CANDIDATE. The value 'kur' is retained as the "
    "historical label of record, not as a supported reading. "
    "Dossier: reports/phase110_m222_dossier.json."
)
ANN_B = (
    "Phase-110 (2026-10-06): M222/'kur' adjudication (spec 008, "
    "Branch 1; addendum) — PREMISE SUPERSEDED. Same Phase-111 "
    "derivation as Cohort A: 'kur' inherited from M222 ('kur' at "
    "run time, Phase-87), a premise superseded by M222's "
    "standing sourced record 'min'/MEDIUM (Phase-109 Step 1(a); "
    "crosswalk v2.1, Parpola 1994 App. B attribution). The "
    "Phase-111 profile match carried no discriminating "
    "information (all rare-sign profiles (0,0,1); L1=0.000; "
    "Phase-132: 'parking placeholder... not a genuine phonetic "
    "reading'). This entry's Phase-252 upgrade_basis, where "
    "recorded, claims allograph status under a parent sign with "
    "a DIFFERENT recorded reading ('en' via M427 / 'tan' via "
    "M375) and does not support 'kur'. "
    "validation_status='premise_superseded'. Already at "
    "CANDIDATE — no tier change. Dossier: "
    "reports/phase110_m222_dossier.json."
)
ANN_C = (  # spec 008 Cohort C — empty per the dossier/addendum;
    # retained so the apply path follows the spec text verbatim.
    "Phase-110 (2026-10-06): M222/'kur' adjudication (spec 008) "
    "— DUAL DERIVATION NOTED. The Phase-111 leg of this entry's "
    "basis (inheritance from M222='kur') is superseded: M222's "
    "standing sourced record is 'min'/MEDIUM (Phase-109 Step "
    "1(a); crosswalk v2.1). This entry ALSO carries an "
    "independent derivation supporting 'kur' itself, recorded "
    "in upgrade_basis, which stands. No validation_status "
    "imposed and no tier change. The Phase-111 leg should not "
    "be cited as support. Dossier: "
    "reports/phase110_m222_dossier.json."
)
ANN_M222 = (
    "Phase-110 (2026-10-06): M222/'kur' adjudication (spec 008) "
    "— this sign's standing reading 'min'/MEDIUM (retained "
    "Phase-109 Step 1(a) on crosswalk v2.1 Parpola attribution) "
    "is the sourced record against which the Phase-111-derived "
    "'kur' cohort was adjudicated. Verdict (Branch 1): the "
    "cohort's recorded bases cite this sign's superseded Phase-87 "
    "reading 'kur' as their premise; that premise is superseded "
    "by this record. Cohort A (109 entries) demoted LOW -> "
    "CANDIDATE with validation_status='premise_superseded'; "
    "Cohorts B/C annotated per the change register. This sign's "
    "own reading and tier were NOT re-tried in Phase-110 (spec "
    "008 Assumptions). Change register: "
    "reports/phase110_change_register.json. Dossier: "
    "reports/phase110_m222_dossier.json."
)

CITES = [
    "reports/phase110_m222_dossier.json",
    "outputs/phase111_allograph_resolution.json",
    "backend/scripts/phase111_allograph_resolution.py",
    "backend/reports/INDUS_FINAL_ANCHORS.json:_phase132_note",
    "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json:M222",
    "reports/phase109_change_register.json",
]


def load(p: Path):
    return json.loads(p.read_text("utf-8"))


def derive_cohorts(anchors: dict, reg109: dict) -> dict:
    import re
    restores = [e for e in reg109["entries"]
                if e["step"] == "step1" and e["action"] == "restore"]
    a = sorted(e["sign"] for e in restores if e["after"]["reading"] == "kur")
    cand = {s: v for s, v in anchors.items()
            if v.get("reading") == "kur" and v.get("confidence") == "CANDIDATE"
            and str(v.get("basis", "")).startswith("Phase-111 allograph")}
    b, c = [], []
    for s, v in sorted(cand.items()):
        m = re.search(r"(M\d+)='([^']+)'", v.get("upgrade_basis") or "")
        if m and m.group(2) == "kur":
            c.append(s)
        else:
            b.append(s)
    return {"A": a, "B": b, "C": c}


def snap(entry: dict) -> dict:
    return {"reading": entry.get("reading"),
            "confidence": entry.get("confidence"),
            "validation_status": entry.get("validation_status")}


def main() -> int:
    dossier = load(DOSSIER)
    verdict = dossier["verdict"]
    branch = verdict["branch"]
    demote = verdict["demote_cohort_a_to_candidate"]
    assert branch == 1, f"Apply script implements Branch 1; dossier says {branch}"

    data = load(ANCHORS)
    anchors = data["anchors"]
    before = {s: dict(v) for s, v in anchors.items()}
    coh = derive_cohorts(anchors, load(REG109))
    assert coh["A"] == dossier["cohorts"]["cohort_a_register_set"], \
        "Cohort A mismatch vs dossier"
    assert coh["B"] == dossier["cohorts"]["cohort_b_candidate_pure_phase111"]
    assert coh["C"] == sorted(
        dossier["cohorts"]["cohort_c_candidate_dual_derivation"])
    hm_before = {s for s, v in anchors.items()
                 if v.get("confidence") in ("HIGH", "MEDIUM")}

    register: list[dict] = []

    def record(step, sign, rule, action, citations=None):
        register.append({
            "step": step, "sign": sign, "rule": rule, "action": action,
            "before": snap(before[sign]), "after": snap(anchors[sign]),
            "citations": citations or CITES,
        })

    for s in coh["A"]:
        e = anchors[s]
        assert e.get("confidence") == "LOW" and "phase110_annotation" not in e
        e["validation_status"] = "premise_superseded"
        e["phase110_annotation"] = ANN_A
        if demote:
            e["confidence"] = "CANDIDATE"
        record("stepB", s, "spec008-branch1-cohortA",
               "demote+annotate+status" if demote else "annotate+status")
    for s in coh["B"]:
        e = anchors[s]
        assert "phase110_annotation" not in e
        e["validation_status"] = "premise_superseded"
        e["phase110_annotation"] = ANN_B
        record("stepB", s, "spec008-branch1-cohortB", "annotate+status")
    for s in coh["C"]:
        e = anchors[s]
        assert "phase110_annotation" not in e
        e["phase110_annotation"] = ANN_C
        record("stepB", s, "spec008-cohortC-dual-derivation", "annotate")
    anchors["M222"]["phase110_annotation"] = ANN_M222
    record("stepB", "M222", "spec008-m222-record", "annotate")

    # Bookkeeping regeneration from the entries (spec 004 WS3 method).
    counts = Counter(v.get("confidence") for v in anchors.values())
    hm_after = {s for s, v in anchors.items()
                if v.get("confidence") in ("HIGH", "MEDIUM")}
    assert hm_before == hm_after, "H+M set changed — unexpected"
    data["total"] = len(anchors)
    data["total_all_entries"] = len(anchors)
    data["by_confidence"] = {k: counts.get(k, 0)
                             for k in ("HIGH", "MEDIUM", "LOW", "CANDIDATE")}
    data["n_high"] = counts.get("HIGH", 0)
    data["n_medium"] = counts.get("MEDIUM", 0)
    data["n_low"] = counts.get("LOW", 0)
    data["n_candidate"] = counts.get("CANDIDATE", 0)
    md = data.setdefault("metadata", {})
    md["total_count"] = len(anchors)
    md["high_count"] = counts.get("HIGH", 0)
    md["medium_count"] = counts.get("MEDIUM", 0)
    md["low_count"] = counts.get("LOW", 0)
    md["candidate_count"] = counts.get("CANDIDATE", 0)
    md["hm_confirmed_count"] = counts.get("HIGH", 0) + counts.get("MEDIUM", 0)
    data["_phase110_note"] = (
        "Phase-110 (2026-10-06, spec 008): M222/'kur' adjudication "
        "applied — Cohort A (109 Phase-111 'kur' entries) demoted "
        "LOW -> CANDIDATE with validation_status='premise_superseded'; "
        "Cohorts B/C and M222 annotated; summary fields regenerated "
        "from the entries; full change record in "
        "reports/phase110_change_register.json.")
    register.append({
        "step": "bookkeeping", "sign": "*", "rule": "spec008-bookkeeping",
        "action": "regenerate-summary-fields",
        "before": {"by_confidence": {"HIGH": 166, "MEDIUM": 5,
                                     "LOW": 112, "CANDIDATE": 4}},
        "after": {"by_confidence": data["by_confidence"]},
        "citations": ["reports/phase110_m222_dossier.json"],
    })

    # Self-verification: changed entries == register signs.
    changed = {s for s in anchors if anchors[s] != before[s]}
    reg_signs = {r["sign"] for r in register if r["sign"] != "*"}
    assert changed == reg_signs, (
        f"diff/register mismatch: diff-only={sorted(changed - reg_signs)} "
        f"register-only={sorted(reg_signs - changed)}")

    ANCHORS.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                       encoding="utf-8")
    out = {"phase": 110, "spec": "specs/008-m222-adjudication",
           "date": DATE, "gpu_device": _GPU,
           "branch": branch, "entries": register}
    OUT_REG.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                       encoding="utf-8")
    print(f"[phase110-apply] changed entries: {len(changed)} "
          f"(A={len(coh['A'])}, B={len(coh['B'])}, C={len(coh['C'])}, +M222)")
    print(f"[phase110-apply] tiers after: {dict(counts)}")
    print(f"[phase110-apply] wrote {OUT_REG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
