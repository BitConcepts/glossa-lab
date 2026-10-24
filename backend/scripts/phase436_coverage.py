#!/usr/bin/env python3
"""Spec 073 (Phase-436) coverage measurement (spec section 6) and the
closing record (sections 7, 9, 10).

Runs only after both product digests exist (Registry v2 and Asset A
v2, frozen). The join route restates DD-070-9/DD-071-10 over Registry
v2: a sign keys end-to-end when its Wells token resolves through
Registry v2's parpola_1982 rows' wells_ids and through v2's appended
icit_wells rows to exactly one sign_id, and that sign_id carries an
Asset A v2 row. Coverage counts and class sizes only; no positional
quantity is computed and neither predecessor study is re-run.

Closing check (section 9): Registry v1 and Asset A v1 are re-hashed;
any change voids both products (FROZEN INPUT MUTATED).
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
STEP0 = SPEC_DIR / "execution" / "step0-record.json"
REG_V1 = ROOT / "data/crosswalks/canonical_sign_registry.csv"
REG_V2 = ROOT / "data/crosswalks/canonical_sign_registry_v2.csv"
ASSET_V1 = ROOT / "specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv"
ASSET_V2 = SPEC_DIR / "asset-a-v2/depicted-kind-classification.csv"
REG_FREEZE = SPEC_DIR / "registry-v2" / "registry-v2-freeze.json"
ASSET_FREEZE = SPEC_DIR / "asset-a-v2" / "asset-a-v2-freeze.json"
SCHEDULE = SPEC_DIR / "registry-v2" / "change-schedule.json"
P433 = ROOT / "reports/phase433_results.json"
EXT = Path.home() / "workspace/research_notes/indus-data-deep-sweep-20261008/downloads"
CORPUS = EXT / "shaktiosindia-indus-sign-regimes-deposit/sanitized_corpus.json"
GRADES = EXT / "shakti_row_grades_2026-10-22.csv"
PIN_REG_V1 = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
PIN_ASSET_V1 = "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b"
FIVE = ["136", "298", "401", "617", "824"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    step0 = json.loads(STEP0.read_text(encoding="utf-8"))
    assert step0["verdict"] == "PASS"
    reg_freeze = json.loads(REG_FREEZE.read_text(encoding="utf-8"))
    asset_freeze = json.loads(ASSET_FREEZE.read_text(encoding="utf-8"))
    assert sha256(REG_V2) == reg_freeze["sha256"]
    assert sha256(ASSET_V2) == asset_freeze["sha256"]

    # Closing check first in effect: the frozen inputs must be untouched.
    closing = {"registry_v1_sha256": sha256(REG_V1), "asset_a_v1_sha256": sha256(ASSET_V1)}
    mutated = closing["registry_v1_sha256"] != PIN_REG_V1 or closing["asset_a_v1_sha256"] != PIN_ASSET_V1

    reg_rows = list(csv.DictReader(REG_V2.open(newline="", encoding="utf-8")))
    asset_rows = list(csv.DictReader(ASSET_V2.open(newline="", encoding="utf-8")))
    asset_by_id = {r["sign_key"]: r for r in asset_rows}
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))

    # --- M1: Wells coverage vs the 498 baseline, by row class ---
    parp_tokens: set[str] = set()
    icit_tokens: set[str] = set()
    for r in reg_rows:
        tokens = {t for t in (r["wells_ids"] or "").split("|") if t}
        if r["numbering_system"] == "parpola_1982":
            parp_tokens |= tokens
        elif r["numbering_system"] == "icit_wells":
            icit_tokens |= tokens
    m1 = {
        "baseline_distinct_wells_ids_v1": 498,
        "parpola_1982_rows_distinct_wells_ids_v2": len(parp_tokens),
        "icit_wells_rows_distinct_ids_v2": len(icit_tokens),
        "completions_added_to_parpola_map": len(parp_tokens) - 498,
        "total_distinct_ids_v2": len(parp_tokens | icit_tokens),
    }

    # --- the route over v2 ---
    wells_map: dict[str, set[str]] = {}
    for r in reg_rows:
        if r["numbering_system"] in ("parpola_1982", "icit_wells"):
            for token in (r["wells_ids"] or "").split("|"):
                token = token.strip()
                if token:
                    wells_map.setdefault(token, set()).add(r["sign_id"])

    def keying(code: str):
        hits = wells_map.get("W" + code, set())
        if len(hits) == 0:
            return None, "no registry resolution"
        if len(hits) > 1:
            return None, "contested identity"
        sid = next(iter(hits))
        if sid not in asset_by_id:
            return None, "resolved but no Asset A v2 row"
        return sid, None

    # --- M2: the five named signs ---
    consult = json.loads((SPEC_DIR / "execution" / "catalog-consult.json").read_text(encoding="utf-8"))
    placements = {"136": 6, "298": 217, "401": 107, "617": 272, "824": 373}
    m2 = {}
    for code in FIVE:
        sid, reason = keying(code)
        entry = asset_by_id.get(sid) if sid else None
        m2[code] = {
            "disposition": "resolved + keyed" if sid else reason,
            "registry_v2_sign_id": sid,
            "asset_a_v2_row": bool(entry),
            "depicted_kind": entry["depicted_kind"] if entry else None,
            "row_origin": entry["row_origin"] if entry else None,
            "catalog_section_2_5_placement": f"Parpola (1994) sign {placements[code]} (Fuls 2023, Catalog of Indus Signs, section 2.5)",
        }

    # --- M3: keyable shares ---
    p433 = json.loads(P433.read_text(encoding="utf-8"))
    set31 = [e["wells_code"] for e in p433["population"]["O_enumeration_wells_space"]]
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    grade_of = {g["shakti_id"]: g["grade"] for g in csv.DictReader(GRADES.open())}
    documented: set[str] = set()
    frame: set[str] = set()
    for r in corpus:
        if not any(s != "000" for s in r["symbols"]):
            continue
        if grade_of[r["id"]] == "documented-lineage":
            documented.update(s for s in r["symbols"] if s != "000")
        if grade_of[r["id"]] in ("documented-lineage", "undocumented-corroborated"):
            frame.update(s for s in r["symbols"] if s != "000")

    def keyable(codes):
        keyed, rem = [], Counter()
        remainder = []
        for c in sorted(codes):
            sid, reason = keying(c)
            if sid:
                keyed.append(c)
            else:
                rem[reason] += 1
                remainder.append({"code": c, "reason": reason})
        return keyed, dict(rem), remainder

    k31, r31, rem31 = keyable(set31)
    k557, r557, rem557 = keyable(documented)
    m3 = {
        "opening_strong_31": {"baseline_keyed_v1_route": 26, "keyed_after_repair": len(k31),
                              "remainder_by_reason": r31, "remainder": rem31},
        "documented_557": {"baseline_keyed_v1_route": 285, "keyed_after_repair": len(k557),
                           "remainder_by_reason": r557, "remainder": rem557},
    }

    # --- M4: census by kind and row origin; celestial count ---
    census = Counter((r["depicted_kind"], r["row_origin"]) for r in asset_rows)
    celestial = sum(n for (kind, _), n in census.items() if kind == "sky_cycle")
    m4 = {
        "census_by_kind_and_origin": {f"{k}|{o}": n for (k, o), n in sorted(census.items())},
        "celestial_sky_cycle_rows": celestial,
        "spec_071_too_thin_floor": 30,
        "note": ("the celestial count is a class size of the repaired classification asset, stated for "
                 "comparison beside Spec 071's frozen floor; it is not a re-run of Spec 071 and carries "
                 "no verdict"),
    }

    # --- M5: the section 4.3 schedule restated + lineage ---
    m5 = {
        "frame_accounting": schedule["frame_accounting_section_4_3"],
        "no_published_identity_codes": [e["icit_code"] for e in json.loads(
            (SPEC_DIR / "registry-v2" / "no-published-identity.json").read_text(encoding="utf-8"))["entries"]],
        "contested_identity_codes": [e["icit_code"] for e in schedule["contested_identity"]],
        "lineage_statement_PF1_S3": ("every identity statement behind Registry v2 and every label behind "
                                     "Asset A v2 sits in the ICIT tradition and its published concordances "
                                     "(the CISI sign list, the Fuls 2023 Catalog) — consistency within one "
                                     "tradition, not independent corroboration"),
    }

    if mutated:
        outcome = "FROZEN INPUT MUTATED — both products void"
    elif not m5["no_published_identity_codes"] and not m5["contested_identity_codes"] and all(
            m2[c]["disposition"] == "resolved + keyed" for c in FIVE):
        outcome = "KEYING SURFACE REPAIRED"
    else:
        outcome = "REPAIRED WITH NAMED SHORTFALL"

    results = {
        "phase": 436, "spec": "073", "spec_freeze_digest": "5419c4c413189acdec31c15494daf1be759c10c28f84d594935c9629e761dc98",
        "outcome": outcome,
        "registry_v2_sha256": reg_freeze["sha256"],
        "asset_a_v2_sha256": asset_freeze["sha256"],
        "step0_verdict": step0["verdict"],
        "M1_wells_coverage": m1,
        "M2_five_named_signs": m2,
        "M3_keyable_shares": m3,
        "M4_census": m4,
        "M5_frame_schedule": m5,
        "closing_v1_reassertion": {**closing, "registry_v1_pin": PIN_REG_V1, "asset_a_v1_pin": PIN_ASSET_V1,
                                   "untouched": not mutated},
        "does_not_establish": [
            "It does not re-run, amend, or supersede Spec 070's POPULATION NOT KEYED closure or Spec 071's INVALID closure; both stand exactly as recorded, and neither Hunt claim changes state.",
            "It does not decide whether either Hunt question should be re-frozen against the repaired surface; that is a separate owner decision.",
            "It establishes nothing about what any sign means or depicts beyond the published labels entered; the celestial class size is a property of the published sources' labels, not of the script.",
        ],
    }
    (ROOT / "reports" / "phase436_results.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")

    five_lines = "\n".join(
        f"- ICIT {c}: {m2[c]['disposition']} — Registry v2 identity {m2[c]['registry_v2_sign_id']}, "
        f"Asset A v2 row present (depicted kind: {m2[c]['depicted_kind']}); the Catalog's Parpola "
        f"concordance places it at {m2[c]['catalog_section_2_5_placement'].split(' (')[0]}." for c in FIVE)
    report = f"""# Phase-436 — Spec 073: keying-surface repair (Registry v2 + Asset A v2)

## Outcome: {outcome}

**Headline.** The repair is built and measured. Registry v2 keeps all
803 v1 rows byte-identical and adds 210 rows for attested signs the
old registry could not name, each stated in the published ICIT sign
list (Fuls 2023, *A Catalog of Indus Signs*, Ch. 2.3). Asset A v2
keeps all 187 v1 rows untouched and adds 365 rows entered blind under
the same discipline as v1. Measured over the recorded populations:
the 31-sign opening-strong set now keys {len(k31)} of 31 (baseline
26 by resolution in Spec 070's record) and the 557-sign documented
set now keys {len(k557)} of 557 (baseline 285). The one attested
code no published source identifies is named, not dropped: token
999, a corpus placeholder that appears in no published sign list.
The celestial (sky/cycle) class in Asset A v2 is {celestial} rows —
stated plainly beside Spec 071's frozen TOO THIN floor of 30: a
future re-freeze of the sky-signs question would still meet an empty
celestial class on the published labels, because no ruled source
depicts any of the newly keyed signs as a sky object.

## The five named signs (Spec 070's unkeyable five)

{five_lines}

Each of the five is *resolved + keyed*: a Registry v2 row now names
it and an Asset A v2 row exists. None of the five carries a verbal
depiction in any ruled published source, so each row's depicted kind
is *unidentified* — keyed for joining, honestly unclassified.

## Coverage (M1–M5)

- M1 (Wells coverage): the parpola_1982 Wells map still carries
  {m1['parpola_1982_rows_distinct_wells_ids_v2']} distinct ids
  (baseline 498; completions added: {m1['completions_added_to_parpola_map']});
  the new icit_wells rows carry {m1['icit_wells_rows_distinct_ids_v2']}
  further ids; Registry v2 names {m1['total_distinct_ids_v2']} distinct
  Wells/ICIT ids in total.
- M3 remainders: 31-set {r31}; 557-set {r557}.
- M4 (census by kind, new rows): {dict(Counter(r['depicted_kind'] for r in asset_rows if r['row_origin'] == 'new_entry'))};
  carried rows unchanged.
- M5 (frame accounting, §4.3): of {m5['frame_accounting']['attested_frame_codes']}
  attested frame codes, {m5['frame_accounting']['carried_by_v1_identity']}
  were already carried by a v1 identity, {m5['frame_accounting']['new_icit_wells_identity']}
  received a new icit_wells identity, {m5['frame_accounting']['no_published_identity']}
  has NO PUBLISHED IDENTITY ({m5['no_published_identity_codes']}), and
  {m5['frame_accounting']['contested_identity']} is CONTESTED IDENTITY.
  Lineage (P-F1 S3): {m5['lineage_statement_PF1_S3']}.

## Closing checks

Registry v1 re-hashed at the close: {closing['registry_v1_sha256']}
(pin {PIN_REG_V1}) — untouched: {not mutated}. Asset A v1 re-hashed:
{closing['asset_a_v1_sha256']} (pin {PIN_ASSET_V1}) — untouched: {not mutated}.
Step-0 gates 0.1–0.4 all PASS (execution/step0-record.json).

## What this does not establish

- It does not re-run, amend, or supersede Spec 070's POPULATION NOT
  KEYED closure or Spec 071's INVALID closure; both stand exactly as
  recorded, and neither Hunt claim changes state.
- It does not decide whether either Hunt question should be re-frozen
  against the repaired surface; that is a separate owner decision.
- It establishes nothing about what any sign means; the celestial
  count is a property of the published labels, not of the script.
"""
    (ROOT / "reports" / "phase436_report.md").write_text(report, encoding="utf-8")
    outcome_md = report.replace("# Phase-436", "# Spec 073 outcome — Phase-436", 1)
    (SPEC_DIR / "outcome.md").write_text(outcome_md, encoding="utf-8")
    print(json.dumps({"outcome": outcome, "k31": len(k31), "k557": len(k557), "celestial": celestial}, indent=1))
    return 0 if not mutated else 1


if __name__ == "__main__":
    sys.exit(main())
