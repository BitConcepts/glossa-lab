"""Phase-401 (Spec 038) — PRED-2026-007: step 0 of the
frozen full-population census contract, in the frozen
order, then — only behind a full step-0 pass — the
registered scoring (spec sections 5 and 6).

Freeze: specs/038-pred-2026-007-full-population/
freeze.md (digest
b54571d845a2be3429bc532fee4bb58c20723f77e2d40ffcd43b56e0caab6eef;
owner freeze-and-execute order of 2026-10-20: "Freeze
D-31 for execution"). The prediction's registration is
the PRED register entry itself (docs/
PREDICTION_REGISTER.md, PRED-2026-007, registered
2026-04-22; the prediction predates the programme's OSF
preregistration practice and has none of its own). The
frozen spec's own contract registration: OSF
https://osf.io/bkqeh/ (filed 2026-10-20 under DD-038-6;
not a step-0 condition — spec section 3 names the
register entry).

The build executes step 0 of Spec 038 section 3, in
the frozen order, fail-closed, before any scoring:

  0.1  Registration record and sources present and
       verified: the PRED-2026-007 entry located in
       the register file hashed to the freeze record's
       value, standing as registered (its Outcome
       field unaltered by this programme since
       registration); every source the census reads
       present, readable, and hashed to the values
       the freeze record cites; the coding-source
       readings standing in the cited form (primary:
       data.a[].icit_function across the file's 611
       per-sign records; cross-check: the registry's
       icit_function column); the conflict rule of
       spec section 2 in force (primary governs
       membership; cross-check published sign-by-sign;
       ambiguity or internal conflict within the
       primary closes the study here).
  0.2  Enumeration: the full ITM population read
       mechanically off the primary (every distinct
       sign whose icit_function value is exactly
       "ITM"); the record-count reconciliation (611
       records read against the count the frozen
       spec states); and the held-record verification
       read at the same pass — P385 and P378 must
       read ITM in the primary, P098 must not. The
       enumeration is written into the step-0 record,
       with its size, before any Phase 5 output is
       opened. An enumeration that cannot be
       produced, or any held record reading
       differently, closes the study here.
  0.3  Phase 5 output verification: the recorded
       clustering present and hashed as cited
       (best_k 40; 160 signs with assignments); the
       recorded characterisation present and hashed;
       and the sanity anchor reproduced exactly from
       the recorded clustering — P385 to Cluster 21,
       P378 to Cluster 39, P098 to Cluster 10. Any
       failure closes the study at this check.

The step-0 record is written and hashed before any
scoring begins. Only behind a full step-0 pass does
the scoring run (spec sections 5 and 6): each
enumerated sign takes its recorded cluster
(sign_to_cluster, exactly as recorded — no
re-clustering, ever) and that cluster's recorded
class from the characterisation (the class as
recorded — never a class derived from rates at
execution; DD-038-9). The cross-check value for every
sign is recorded and every disagreement published.
A sign with no recorded cluster, or whose cluster
has no recorded class, is unassigned. The share is
computed on the assigned population under the
frozen coverage rule (DD-038-4): coverage stated in
the verdict's first sentence; below 80 percent
coverage, if the unassigned signs could change the
outcome, the test is recorded as run at partial
scope. The verdict mapping is the registered one:
CONFIRMED at a share of at least 0.70 of the
assigned population TERMINAL or in TERMINAL
clusters, NOT CONFIRMED below. If the enumerated
population is exactly {P378, P385} — the ITM signs
the recorded partial test already covered — the
census branch applies: the design completes and
scores by the same rule.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REGISTER = REPO / "docs" / "PREDICTION_REGISTER.md"
PRIMARY = REPO / "reports" / "indus_cgsa_cluster_analysis.json"
CROSSCHECK = REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"
SIGN_CLUSTERS = REPO / "outputs" / "analysis" / "sign_clusters.json"
CHARACTERIZATION = REPO / "reports" / "cluster_characterization.md"
RESULTS_JSON = REPO / "reports" / "phase401_results.json"

FREEZE_DIGEST = "b54571d845a2be3429bc532fee4bb58c20723f77e2d40ffcd43b56e0caab6eef"
FREEZE_MERGE = "c363edefe4e2feb08e73a2a7e12934694b6dbb7d"
SPEC_REG_ID = "bkqeh"
CLOSURE = "CANNOT BE RUN AS WRITTEN"

PIN_REGISTER = "4f8aeb54fd5853d73766ed9cf0222ef93cccfa8d9a8c399a4631221fbbb4c1c2"
PIN_PRIMARY = "8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3"
PIN_CROSSCHECK = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
PIN_SIGN_CLUSTERS = "623a787dd9cc93c4d3d36377890c4753e3427f57cf7ad70adcd6e8256ba1394a"
PIN_CHARACTERIZATION = "54ebf660873fd853a64ce91c7e30d8c4cedc5bc3a0a1555db1f6281a52e3c476"

STATED_RECORD_COUNT = 611
EXPECTED_BEST_K = 40
EXPECTED_ASSIGNED_SIGNS = 160
# Held records (spec section 3, check 0.2): the signs
# whose primary-source codes were verified against
# the recorded partial test at design. P098's
# condition is that it must NOT read ITM.
HELD_MUST_READ_ITM = ["P385", "P378"]
HELD_MUST_NOT_READ_ITM = ["P098"]
# Sanity anchor (check 0.3), from the register's
# per-sign partial-test records.
ANCHOR = {"P385": 21, "P378": 39, "P098": 10}
PARTIAL_TEST_ITM = {"P378", "P385"}
CRITERION_SHARE = 0.70
COVERAGE_FLOOR = 0.80


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_json(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, indent=1).encode("utf-8")
    ).hexdigest()


def check_0_1() -> tuple[dict, dict]:
    """Registration record and sources. Returns
    (record, context) — context carries the parsed
    sources forward only on a pass."""
    rec: dict = {}
    ctx: dict = {}
    problems: list[str] = []

    reg_raw = REGISTER.read_bytes()
    reg_hash = sha256_bytes(reg_raw)
    rec["register_sha256"] = reg_hash
    rec["register_pin_match"] = reg_hash == PIN_REGISTER
    if reg_hash != PIN_REGISTER:
        problems.append("PRED register hash differs from the freeze record")
    text = reg_raw.decode("utf-8")
    start = text.index("PRED-2026-007")
    nxt = text.index("### PRED-", start + 10)
    entry = text[start:nxt]
    rec["entry_located"] = True
    rec["criterion_line_present"] = (
        "≥ 70% of ITM-coded signs are TERMINAL or cluster in TERMINAL clusters"
        in entry
    )
    rec["standing_outcome"] = (
        "PARTIALLY CONFIRMED" if "PARTIALLY CONFIRMED" in entry else None
    )
    rec["registered_date_present"] = "2026-04-22" in entry
    if not rec["criterion_line_present"] or rec["standing_outcome"] is None:
        problems.append("PRED-2026-007 entry does not stand as registered")

    hashes = {}
    for name, path, pin in (
        ("primary", PRIMARY, PIN_PRIMARY),
        ("crosscheck", CROSSCHECK, PIN_CROSSCHECK),
        ("sign_clusters", SIGN_CLUSTERS, PIN_SIGN_CLUSTERS),
        ("characterization", CHARACTERIZATION, PIN_CHARACTERIZATION),
    ):
        raw = path.read_bytes()
        h = sha256_bytes(raw)
        hashes[name] = {"sha256": h, "pin_match": h == pin}
        if h != pin:
            problems.append(f"{name} hash differs from the freeze citation")
        ctx[name + "_raw"] = raw
    rec["source_hashes"] = hashes

    # The coding-source readings in the cited form.
    cg = json.loads(ctx["primary_raw"])
    rows = cg["data"]["a"]
    rec["primary_field"] = "data.a[].icit_function"
    rec["primary_records"] = len(rows)
    rec["primary_form_ok"] = (
        isinstance(rows, list)
        and all("icit_function" in r and "sign_id" in r for r in rows)
    )
    if not rec["primary_form_ok"]:
        problems.append("primary field not present in the cited form")
    ctx["primary_rows"] = rows

    rdr = csv.DictReader(io.StringIO(ctx["crosscheck_raw"].decode("utf-8")))
    rec["crosscheck_field"] = "icit_function"
    rec["crosscheck_form_ok"] = (
        rdr.fieldnames is not None
        and "icit_function" in rdr.fieldnames
        and "sign_id" in rdr.fieldnames
    )
    if not rec["crosscheck_form_ok"]:
        problems.append("cross-check field not present in the cited form")
    ctx["crosscheck_rows"] = list(rdr)

    rec["conflict_rule_in_force"] = (
        "primary governs membership; cross-check values published "
        "sign-by-sign; disagreement moves no membership (spec s.2)"
    )
    rec["problems"] = problems
    rec["status"] = "PASS" if not problems else "FAIL"
    return rec, ctx


def check_0_2(ctx: dict) -> tuple[dict, dict | None]:
    """Enumeration, written before any Phase 5 lookup.
    Returns (record, enumeration) — enumeration None
    on closure."""
    rows = ctx["primary_rows"]
    by_sign: dict[str, list[str]] = {}
    for r in rows:
        by_sign.setdefault(r["sign_id"], []).append(r["icit_function"])
    conflicts = {s: v for s, v in by_sign.items() if len(set(v)) > 1}
    itm = sorted(s for s, v in by_sign.items() if set(v) == {"ITM"})
    enumeration = {
        "rule": "icit_function value in the primary source "
                "(data.a[].icit_function) equals exactly ITM (DD-038-5)",
        "source": "reports/indus_cgsa_cluster_analysis.json",
        "source_sha256": PIN_PRIMARY,
        "records_read": len(rows),
        "itm_signs": itm,
        "population_size": len(itm),
    }
    rec: dict = {
        "enumeration": enumeration,
        "enumeration_sha256": sha256_json(enumeration),
        "record_count_reconciliation": {
            "records_read": len(rows),
            "stated_count": STATED_RECORD_COUNT,
            "reconciled": len(rows) == STATED_RECORD_COUNT,
        },
        "internal_conflicts_within_primary": conflicts,
    }
    held = {}
    ok = True
    for sign in HELD_MUST_READ_ITM + HELD_MUST_NOT_READ_ITM:
        values = by_sign.get(sign)
        held[sign] = {
            "record_present": values is not None,
            "primary_code": values[0] if values else None,
        }
    for sign in HELD_MUST_READ_ITM:
        held[sign]["condition"] = "must read ITM in the primary"
        held[sign]["met"] = held[sign]["primary_code"] == "ITM"
        ok = ok and held[sign]["met"]
    for sign in HELD_MUST_NOT_READ_ITM:
        held[sign]["condition"] = "must not read ITM in the primary"
        held[sign]["met"] = held[sign]["primary_code"] != "ITM"
        ok = ok and held[sign]["met"]
    rec["held_records"] = held
    if conflicts:
        ok = False
        rec["closure_reason"] = (
            "internal conflict within the primary source over at "
            "least one sign (spec s.2 / check 0.1 in force at 0.2)"
        )
    if not rec["record_count_reconciliation"]["reconciled"]:
        ok = False
        rec["closure_reason"] = "record-count reconciliation failed"
    if not ok and "closure_reason" not in rec:
        bad = [s for s, h in held.items() if not h["met"]]
        rec["closure_reason"] = (
            "held record(s) " + ", ".join(bad) + " read differently "
            "in the primary than the recorded partial test states"
        )
    rec["status"] = "PASS" if ok else "FAIL"
    return rec, (enumeration if ok else None)


def check_0_3(ctx: dict) -> dict:
    """Phase 5 output verification and sanity anchor."""
    rec: dict = {}
    sc = json.loads(ctx["sign_clusters_raw"])
    rec["best_k"] = sc.get("best_k")
    s2c = sc.get("sign_to_cluster") or {}
    rec["assigned_signs"] = len(s2c)
    anchor = {}
    ok = (
        sc.get("best_k") == EXPECTED_BEST_K
        and len(s2c) == EXPECTED_ASSIGNED_SIGNS
    )
    for sign, cluster in ANCHOR.items():
        got = s2c.get(sign)
        anchor[sign] = {"expected_cluster": cluster,
                        "recorded_cluster": got, "match": got == cluster}
        ok = ok and got == cluster
    rec["sanity_anchor"] = anchor
    rec["status"] = "PASS" if ok else "FAIL"
    ctx["sign_to_cluster"] = s2c
    return rec


def parse_cluster_classes(md_text: str) -> dict[int, str]:
    """Per-cluster recorded classes from the
    characterisation's per-cluster headings
    ('### Cluster 21 — TERMINAL (1 signs, ...)').
    The class token(s) are taken exactly as recorded
    (a slash-joined pair stays a pair)."""
    classes: dict[int, str] = {}
    for m in re.finditer(
        r"^### Cluster (\d+) — ([A-Z/]+) \(", md_text, re.M
    ):
        classes[int(m.group(1))] = m.group(2)
    return classes


def score(ctx: dict, enumeration: dict) -> dict:
    s2c = ctx["sign_to_cluster"]
    classes = parse_cluster_classes(
        ctx["characterization_raw"].decode("utf-8"))
    cross = {}
    for row in ctx["crosscheck_rows"]:
        cross.setdefault(row["sign_id"], row["icit_function"])
    population = enumeration["itm_signs"]
    table = []
    disagreements = []
    assigned = 0
    numerator = 0
    unassigned = []
    for sign in population:
        cluster = s2c.get(sign)
        cclass = classes.get(cluster) if cluster is not None else None
        is_assigned = cluster is not None and cclass is not None
        counts = bool(is_assigned and "TERMINAL" in cclass.split("/"))
        cc_value = cross.get(sign)
        agree = cc_value == "ITM"
        if not agree:
            disagreements.append({
                "sign": sign, "primary": "ITM",
                "crosscheck": cc_value,
                "reading": "membership follows the primary (DD-038-5)",
            })
        if is_assigned:
            assigned += 1
            numerator += 1 if counts else 0
        else:
            unassigned.append(sign)
        table.append({
            "sign": sign,
            "primary_code": "ITM",
            "crosscheck_code": cc_value,
            "sources_agree": agree,
            "cluster": cluster,
            "cluster_class": cclass,
            "assigned": is_assigned,
            "counts_toward_criterion": counts if is_assigned else None,
        })
    coverage = (assigned / len(population)) if population else 0.0
    share = (numerator / assigned) if assigned else None
    # Coverage rule (DD-038-4): decisive iff the
    # unassigned signs cannot change the outcome.
    decisive = False
    if share is not None and population:
        worst = numerator / len(population)
        best = (numerator + len(unassigned)) / len(population)
        verdict_now = share >= CRITERION_SHARE
        decisive = (worst >= CRITERION_SHARE) == verdict_now and (
            best >= CRITERION_SHARE) == verdict_now
    partial_scope = bool(
        share is not None and coverage < COVERAGE_FLOOR and not decisive
    )
    verdict = None
    if share is not None:
        verdict = "CONFIRMED" if share >= CRITERION_SHARE else "NOT CONFIRMED"
    return {
        "population_size": len(population),
        "assigned": assigned,
        "unassigned": len(unassigned),
        "unassigned_signs": unassigned,
        "numerator_terminal_or_terminal_cluster": numerator,
        "denominator_assigned_population": assigned,
        "share": share,
        "coverage": coverage,
        "coverage_decisive": decisive,
        "run_at_partial_scope": partial_scope,
        "census_branch": set(population) == PARTIAL_TEST_ITM,
        "verdict": verdict,
        "crosscheck_disagreements": disagreements,
        "per_sign_table": table,
        "computation": "join of the step-0.2 enumeration (hashed "
                       "before lookup) to the recorded Phase 5 "
                       "sign_to_cluster assignments and the recorded "
                       "characterisation classes, exactly as recorded",
    }


def main() -> int:
    step0: dict = {}
    c1, ctx = check_0_1()
    step0["check_0_1"] = c1
    closure_check = None
    enumeration = None
    scoring = None
    if c1["status"] != "PASS":
        closure_check = "0.1"
    else:
        c2, enumeration = check_0_2(ctx)
        step0["check_0_2"] = c2
        if c2["status"] != "PASS":
            closure_check = "0.2"
        else:
            c3 = check_0_3(ctx)
            step0["check_0_3"] = c3
            if c3["status"] != "PASS":
                closure_check = "0.3"
    step0["phase5_output_opened"] = "check_0_3" in step0

    if closure_check is None:
        scoring = score(ctx, enumeration)
        outcome = {
            "type": "verdict",
            "verdict": scoring["verdict"],
            "prediction_state": scoring["verdict"],
            "scoring_run": True,
            "share": scoring["share"],
            "population_size": scoring["population_size"],
            "coverage": scoring["coverage"],
            "run_at_partial_scope": scoring["run_at_partial_scope"],
            "census_branch": scoring["census_branch"],
        }
    else:
        outcome = {
            "type": "step0_closure",
            "closure": CLOSURE,
            "failed_check": closure_check,
            "prediction_state": "UNSCORED - PARTIALLY CONFIRMED stands "
                                "as the pre-execution record",
            "scoring_run": False,
            "verdict": None,
        }

    results = {
        "experiment_id": "spec038-pred-2026-007-full-population",
        "spec": "038-pred-2026-007-full-population",
        "phase": 401,
        "freeze_digest": FREEZE_DIGEST,
        "freeze_merge": FREEZE_MERGE,
        "prediction": {
            "id": "PRED-2026-007",
            "registered": "2026-04-22",
            "criterion": {
                "quantity": "share of ITM-coded signs (the full "
                            "enumerated population, assigned) that "
                            "are TERMINAL or cluster in TERMINAL "
                            "clusters",
                "share_min": CRITERION_SHARE,
            },
        },
        "registration": {
            "prediction_registration": {
                "record": "docs/PREDICTION_REGISTER.md s.3, "
                          "PRED-2026-007 (registered 2026-04-22)",
                "osf": None,
                "note": "the prediction predates the programme's OSF "
                        "preregistration practice and has no OSF "
                        "preregistration of its own",
            },
            "spec_contract_registration": {
                "osf": f"https://osf.io/{SPEC_REG_ID}/",
                "state": "filed 2026-10-20 under DD-038-6; pending "
                         "approval at execution (not a step-0 "
                         "condition; spec s.3 names the register entry)",
            },
        },
        "step0_record": step0,
        "step0_record_sha256": sha256_json(step0),
        "scoring_record": scoring,
        "scoring_record_sha256": sha256_json(scoring) if scoring else None,
        "outcome": outcome,
    }
    RESULTS_JSON.write_text(
        json.dumps(results, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "step0": {k: v.get("status") for k, v in step0.items()
                  if isinstance(v, dict) and "status" in v},
        "outcome": outcome,
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
