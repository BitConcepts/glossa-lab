"""Phase 443 - Spec 077 execution: three-witness sign-list
triangulation + the token 999 attack (Method M7).

Runs the frozen contract of specs/077-signary-triangulation
exactly once, as frozen:

  step 0  - verify every section-3 pin first-hand; verify the
            actual columns of every witness table counted from;
            reproduce Spec 075's population census (3,045 / 557 /
            550) and token 999's reference behavior (2 occurrences,
            0 text-final) under Spec 075's frozen construction
            over its pinned restricted-local inputs; file the
            13-duplicated-id resolution table (FF-4); verify the
            Table I input against FF-7's acceptance form. Any
            failure closes the execution CANNOT BE RUN AS WRITTEN
            and no counting runs.
  counting- C01's witness shares (raw, ancestry-adjusted per
            FF-5, per-witness breakdown), sensitivities S1/S2,
            the gap list (section 5 deliverable), and C02's
            token 999 attack under FF-6/FF-7 with its full
            candidate table.

Writes reports/phase443_results.json (the machine record).
The human records (step0-record.md, outcome.md) are authored
from it. Restricted-local inputs are read in place and cited
by hash only; nothing restricted is copied or written.

Environment overrides (defaults are the program's held paths):
  GLOSSA_STORE_DIR   canonical store sources dir
  SHAKTI_DEPOSIT_DIR the restricted-local Shakti deposit dir
  SHAKTI_GRADES_CSV  the restricted-local row-grades file
  TABLE1_RESIDUALS_JSON  optional JSON {residuals: [SOL, INI,
                     MED, FIN, TOT], unsettled_signs: [...],
                     landing_record: "..."} read from the Table I
                     dataset's landing record when the landed
                     file carries unsettled rows (FF-7 (ii)/(iii))
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOME = Path.home()
STORE = Path(os.environ.get(
    "GLOSSA_STORE_DIR",
    HOME / "workspace/glossa-lab/glossa-corpus/indus/sources"))
DEPOSIT = Path(os.environ.get(
    "SHAKTI_DEPOSIT_DIR",
    HOME / "workspace/research_notes/indus-data-deep-sweep-20261008"
           "/downloads/shaktiosindia-indus-sign-regimes-deposit"))
GRADES = Path(os.environ.get(
    "SHAKTI_GRADES_CSV",
    HOME / "workspace/research_notes/indus-data-deep-sweep-20261008"
           "/downloads/shakti_row_grades_2026-10-22.csv"))
THESIS = (HOME / "workspace/research_notes/indus-data-deep-sweep-20261008"
                "/downloads/wells-ma-thesis-1998"
                "/Wells1998_MA_AnIntroductionToIndusWriting_Calgary.pdf")

PINS = {
    "registry_v2": (
        REPO / "data/crosswalks/canonical_sign_registry_v2.csv",
        "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"),
    "phase441_record": (
        REPO / "reports/phase441_results.json",
        "f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29"),
    "m77_raw_text": (
        REPO / "data/mahadevan_m77_raw.txt",
        "11441e38286784a1f4215f73d91cbba8acd153b7e5b30daed9252f9f7b77304a"),
    "anchors": (
        REPO / "backend/reports/INDUS_FINAL_ANCHORS.json",
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"),
    "m77_dataset_v3": (
        STORE / "mahadevan-1977/m77_sign_list.csv",
        "9c619bfe2520e63e2968be0ab4ddc9cef1f9aff7dfa3f8eddbf58f21fb414f7e"),
    "wells1998_dataset": (
        STORE / "wells-1998/wells1998_sign_list.csv",
        "22bde128551adbd6d91cd76bb41b4f40199ab3e45af76d500a1008d27c5bea95"),
    "fig36_crossrefs": (
        STORE / "wells-1998/wells1998_fig36_crossrefs.csv",
        "b0ef40da7cd65cdcb6910fd2b1e6aeae4eac47cb31cbe2b2c6205f2ac5da270d"),
    "wells_thesis": (
        THESIS,
        "5720dc010acc68d6b50827fa89fb7bf3c4c0eb0aee67597e7662e5fd74508906"),
    "restricted_corpus": (
        DEPOSIT / "sanitized_corpus.json",
        "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"),
    "restricted_grades": (
        GRADES,
        "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"),
}

REGISTRY_COLUMNS = [
    "internal_id", "sign_id", "numbering_system", "description",
    "parpola_id", "wells_ids", "mahadevan_ids", "parpola_allographs",
    "icit_function", "corpus_freq", "start_rate", "end_rate",
    "internal_rate", "in_corpus", "n_feature_dims",
]
DUPLICATED_IDS = [
    "M002", "M050", "M064", "M076", "M099", "M103", "M161",
    "M167", "M168", "M199", "M216", "M264", "M409",
]
PRINTED_TOTALS = [190, 3010, 7196, 2976, 13372]
BAR_COUNT = 502
POPULATION = 557


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames, list(reader)


def parse_leading_int(text: str):
    digits = ""
    for ch in (text or "").strip():
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits) if digits else None


def parse_m_label(text: str):
    """A registry Mahadevan label ('M097') to its number (97).

    Distinct from parse_leading_int: the label's digits are
    trailing, after the 'M' prefix. (First-run defect record:
    the counting loop originally applied parse_leading_int to
    these labels, got None for every one, and produced an
    empty per-sign table - caught on inspection of the
    machine record before any record was filed; see the
    execution's step0-record.md.)"""
    body = (text or "").strip()
    if body.startswith("M"):
        body = body[1:]
    return int(body) if body.isdigit() else None


def main() -> int:
    record: dict = {
        "phase": 443,
        "spec": "077",
        "claim_family": "F077",
        "contract": {},
        "step0": {},
        "outcome": None,
    }
    failures: list[str] = []

    # ── step 0.1: pins ──────────────────────────────────────
    pin_results = {}
    for name, (path, want) in PINS.items():
        if not path.exists():
            pin_results[name] = {"ok": False, "error": "file missing"}
            failures.append(f"pin {name}: file missing ({path})")
            continue
        got = sha256(path)
        pin_results[name] = {"ok": got == want, "sha256": got}
        if got != want:
            failures.append(f"pin {name}: sha256 {got} != {want}")
    record["step0"]["pins"] = pin_results
    anchors_before = pin_results.get("anchors", {}).get("sha256")

    # ── step 0.2: witness tables' actual columns ────────────
    columns = {}
    _, registry_rows = read_csv(PINS["registry_v2"][0])
    columns["registry_v2"] = registry_rows and list(registry_rows[0].keys())
    reg_fields, _ = read_csv(PINS["registry_v2"][0])
    if reg_fields != REGISTRY_COLUMNS:
        failures.append(
            f"registry columns diverge: {reg_fields}")
    m77_fields, m77_rows = read_csv(PINS["m77_dataset_v3"][0])
    columns["m77_dataset_v3"] = m77_fields
    for needed in ("sign_no", "variant_marker", "status"):
        if needed not in (m77_fields or []):
            failures.append(f"m77 dataset lacks column {needed}")
    wells_fields, wells_rows = read_csv(PINS["wells1998_dataset"][0])
    columns["wells1998_dataset"] = wells_fields
    for needed in ("sign_no", "total", "mahadevan_xref_fig36", "status"):
        if needed not in (wells_fields or []):
            failures.append(f"wells dataset lacks column {needed}")
    fig_fields, fig_rows = read_csv(PINS["fig36_crossrefs"][0])
    columns["fig36_crossrefs"] = fig_fields
    for needed in ("mahadevan_1977", "wells_1997"):
        if needed not in (fig_fields or []):
            failures.append(f"fig36 file lacks column {needed}")
    record["step0"]["columns"] = columns

    # ── step 0.3: population reproduction + 999 references ──
    corpus = json.loads(PINS["restricted_corpus"][0].read_text(
        encoding="utf-8"))
    grade_of = {}
    with PINS["restricted_grades"][0].open(
            newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            grade_of[row["shakti_id"]] = row["grade"]
    primary = [r for r in corpus
               if grade_of.get(r["id"]) == "documented-lineage"]
    seqs = []
    for r in primary:
        seq = [s for s in r["symbols"] if s != "000"]
        if seq:
            seqs.append(seq)
    totals: dict[str, int] = {}
    finals: dict[str, int] = {}
    for seq in seqs:
        for s in seq:
            totals[s] = totals.get(s, 0) + 1
        finals[seq[-1]] = finals.get(seq[-1], 0) + 1
    census = {
        "analyzable_rows": len(seqs),
        "distinct_signs": len(totals),
        "signs_in_sequences_ge2": len(
            {x for s in seqs if len(s) >= 2 for x in s}),
        "token_999_occurrences": totals.get("999", 0),
        "token_999_finals": finals.get("999", 0),
    }
    record["step0"]["population_reproduction"] = census
    if census != {
        "analyzable_rows": 3045, "distinct_signs": 557,
        "signs_in_sequences_ge2": 550, "token_999_occurrences": 2,
        "token_999_finals": 0,
    }:
        failures.append(f"population reproduction diverges: {census}")

    # ── step 0.4: the 13-id resolution table (FF-4) ────────
    parpola = [r for r in registry_rows
               if r["numbering_system"] == "parpola_1982"]
    claims_by_id: dict[str, list[str]] = {}
    wells_of_row: dict[str, set[str]] = {}
    m_of_row: dict[str, set[str]] = {}
    for r in parpola:
        wells_of_row[r["sign_id"]] = {
            t for t in (r["wells_ids"] or "").split("|") if t}
        m_of_row[r["sign_id"]] = {
            t for t in (r["mahadevan_ids"] or "").split("|") if t}
        for m in m_of_row[r["sign_id"]]:
            claims_by_id.setdefault(m, []).append(r["sign_id"])
    resolution = {}
    for m in DUPLICATED_IDS:
        claimants = sorted(claims_by_id.get(m, []))
        if len(claimants) != 2:
            failures.append(
                f"duplicated id {m}: {len(claimants)} claiming rows, "
                "expected 2 - cannot state the resolution table")
        resolution[m] = {
            "claiming_rows": claimants,
            "wells_ids_by_row": {
                c: sorted(wells_of_row.get(c, set())) for c in claimants},
        }
    record["step0"]["duplicated_id_resolution"] = resolution

    # ── step 0.4b: the per-sign Mahadevan table, built twice ──
    # Method (a): through the step-0.4 maps. Method (b): a
    # direct row scan per sign. The two constructions must
    # agree exactly; the counting consumes method (b)'s table.
    # (This cross-check exists because the first invocation's
    # counting loop mis-parsed the 'M097'-form labels and
    # produced an empty table - see step0-record.md.)
    record441 = json.loads(PINS["phase441_record"][0].read_text(
        encoding="utf-8"))
    population_signs = [e["sign"] for e in record441["keyed_population"]]
    population_signs.append("999")
    m_by_sign_a: dict[str, set[int]] = {}
    m_by_sign_b: dict[str, set[int]] = {}
    for sign in population_signs:
        token = "W" + sign
        via_maps: set[int] = set()
        for r in parpola:
            if token in wells_of_row[r["sign_id"]]:
                for m in m_of_row[r["sign_id"]]:
                    n = parse_m_label(m)
                    if n is not None:
                        via_maps.add(n)
        m_by_sign_a[sign] = via_maps
        via_scan: set[int] = set()
        for r in parpola:
            if token in (r["wells_ids"] or "").split("|"):
                for m in (r["mahadevan_ids"] or "").split("|"):
                    if m:
                        n = parse_m_label(m)
                        if n is not None:
                            via_scan.add(n)
        m_by_sign_b[sign] = via_scan
    if m_by_sign_a != m_by_sign_b:
        failures.append(
            "per-sign Mahadevan table: the two step-0 constructions "
            "disagree - instrument failure, counting must not run")
    record["step0"]["signs_with_mahadevan_numbers"] = sum(
        1 for v in m_by_sign_b.values() if v)

    # ── step 0.5: Table I acceptance form (FF-7) ───────────
    table1_path = STORE / "mahadevan-1977/m77_table1_occurrences.csv"
    table1: dict[int, list[int] | None] = {}
    table1_info: dict = {"path": str(table1_path)}
    if not table1_path.exists():
        failures.append("Table I dataset missing from the canonical store")
    else:
        table1_info["sha256"] = sha256(table1_path)
        t_fields, t_rows = read_csv(table1_path)
        table1_info["columns"] = t_fields
        explicit = [c for c in ("sol", "ini", "med", "fin", "tot")
                    if c in (t_fields or [])]
        complete_sums = [0, 0, 0, 0, 0]
        unsettled: list[int] = []
        bad_rows: list[str] = []
        for r in t_rows:
            sign = parse_leading_int(r.get("sign_no", ""))
            if sign is None:
                bad_rows.append(f"unparsable sign_no {r.get('sign_no')!r}")
                continue
            cells: list[int | None] = [None] * 5
            if len(explicit) == 5:
                for i, c in enumerate(("sol", "ini", "med", "fin", "tot")):
                    v = (r.get(c) or "").strip()
                    cells[i] = int(v) if v.lstrip("-").isdigit() else None
            else:
                parts = (r.get("raw_ocr") or "").split("|")
                if len(parts) == 5:
                    for i, p in enumerate(parts):
                        p = p.strip()
                        cells[i] = int(p) if p.lstrip("-").isdigit() else None
                occ = (r.get("occurrences") or "").strip()
                if cells[4] is None and occ.lstrip("-").isdigit():
                    cells[4] = int(occ)
            if all(c is not None for c in cells):
                if cells[4] != cells[0] + cells[1] + cells[2] + cells[3]:
                    bad_rows.append(
                        f"sign {sign}: TOT != SOL+INI+MED+FIN {cells}")
                    table1[sign] = None
                    unsettled.append(sign)
                    continue
                table1[sign] = [int(c) for c in cells]
                for i in range(5):
                    complete_sums[i] += int(cells[i])
            else:
                table1[sign] = None
                unsettled.append(sign)
        table1_info["rows"] = len(t_rows)
        table1_info["complete_rows"] = sum(
            1 for v in table1.values() if v is not None)
        table1_info["unsettled_signs"] = sorted(unsettled)
        table1_info["bad_rows"] = bad_rows
        table1_info["complete_column_sums"] = complete_sums
        residuals = [PRINTED_TOTALS[i] - complete_sums[i] for i in range(5)]
        table1_info["residuals_vs_printed"] = residuals
        if bad_rows:
            failures.append(
                f"Table I row equations violated: {bad_rows[:5]}")
        residuals_env = os.environ.get("TABLE1_RESIDUALS_JSON")
        if not unsettled:
            if residuals != [0, 0, 0, 0, 0]:
                failures.append(
                    f"Table I column sums do not close on the printed "
                    f"totals row: residuals {residuals}")
            table1_info["reconciliation"] = "column sums equal printed totals"
        else:
            if not residuals_env:
                failures.append(
                    "Table I has not landed in the FF-7 form: "
                    f"{len(unsettled)} unsettled rows {sorted(unsettled)} "
                    "and no landing-record residuals supplied "
                    "(TABLE1_RESIDUALS_JSON) - input not verified")
            else:
                stated = json.loads(Path(residuals_env).read_text(
                    encoding="utf-8"))
                if stated.get("residuals") != residuals:
                    failures.append(
                        "Table I residuals computed from the file "
                        f"{residuals} != landing record's stated "
                        f"{stated.get('residuals')}")
                if sorted(stated.get("unsettled_signs", [])) != sorted(unsettled):
                    failures.append(
                        "Table I unsettled rows in the file "
                        f"{sorted(unsettled)} != landing record's named "
                        f"{sorted(stated.get('unsettled_signs', []))}")
                table1_info["reconciliation"] = (
                    "complete-row sums + landing record residuals "
                    f"({stated.get('landing_record')}) equal printed totals")
    record["step0"]["table1"] = table1_info

    record["step0"]["failures"] = failures
    out_path = REPO / "reports/phase443_results.json"

    if failures:
        record["outcome"] = "CANNOT BE RUN AS WRITTEN"
        record["step0"]["verdict"] = (
            "step 0 closes the execution; no counting ran")
        out_path.write_text(json.dumps(record, indent=1) + "\n",
                            encoding="utf-8")
        print("STEP 0 CLOSES THE EXECUTION - CANNOT BE RUN AS WRITTEN")
        for f in failures:
            print(" -", f)
        return 2

    # ── counting (FF-3 / FF-4) ──────────────────────────────
    m77_numbers = {int(r["sign_no"]) for r in m77_rows}
    fig36_targets: set[int] = set()
    wells_pairing: dict[int, int] = {}
    for r in wells_rows:
        if r["status"] == "NOT PRINTED":
            continue
        target = parse_leading_int(r.get("mahadevan_xref_fig36", ""))
        if target is not None:
            fig36_targets.add(target)
            wells_pairing[int(r["sign_no"])] = target

    # (record441 and population_signs were loaded at step 0.4b;
    # the counting consumes step 0.4b's verified table.)
    claimant_sets = {m: set(v) for m, v in claims_by_id.items()}

    def ff4_ok(sign_token: str, m: str) -> bool:
        claimants = claimant_sets.get(m, set())
        if len(claimants) <= 1:
            return True
        carrying = [c for c in claimants
                    if sign_token in wells_of_row.get(c, set())]
        return len(carrying) == 1

    per_sign = []
    for sign in population_signs:
        token = "W" + sign
        m_numbers = m_by_sign_b[sign]
        m_labels = {"M%03d" % n for n in m_numbers}
        w_m77 = False
        w_wells = False
        for n in m_numbers:
            label = "M%03d" % n
            if label not in m_labels:
                label = next((x for x in m_labels
                              if parse_m_label(x) == n), label)
            ok = ff4_ok(token, label)
            if not ok:
                continue
            if n in m77_numbers:
                w_m77 = True
            if n in fig36_targets:
                w_wells = True
        per_sign.append({
            "sign": sign,
            "mahadevan_numbers": sorted(m_numbers),
            "witnessed_m77": w_m77,
            "witnessed_wells1998": w_wells,
            "witnessed": w_m77 or w_wells,
        })

    n_m77 = sum(1 for s in per_sign if s["witnessed_m77"])
    n_wells = sum(1 for s in per_sign if s["witnessed_wells1998"])
    n_both = sum(1 for s in per_sign
                 if s["witnessed_m77"] and s["witnessed_wells1998"])
    n_witnessed = sum(1 for s in per_sign if s["witnessed"])
    gap = [s["sign"] for s in per_sign if not s["witnessed"]]
    record["counting"] = {
        "population": POPULATION,
        "witnessed_any": n_witnessed,
        "raw_share": n_witnessed / POPULATION,
        "witnessed_m77": n_m77,
        "ancestry_adjusted_share": n_m77 / POPULATION,
        "witnessed_wells1998": n_wells,
        "witnessed_both": n_both,
        "witnessed_only_wells1998": n_witnessed - n_m77,
        "sensitivities": {
            "S1_strictest_ancestry": n_m77 / POPULATION,
            "S2_registry_construction_exclusion": {
                "excluded_signs": 0,
                "share": n_witnessed / POPULATION,
            },
        },
        "gap_list": gap,
        "per_sign": per_sign,
    }
    if n_m77 >= BAR_COUNT:
        record["verdicts"] = {"F077-C01": "SUPPORTED"}
    else:
        record["verdicts"] = {
            "F077-C01": "NOT SUPPORTED",
            "closure_word": "SIGNARY NOT WITNESSED AT THE STATED LEVEL",
        }

    # ── token 999 attack (FF-6 / FF-7) ──────────────────────
    candidates_m77 = []
    for sign in sorted(table1):
        cells = table1[sign]
        if cells is None:
            candidates_m77.append({
                "m77_sign": sign, "tot": None, "fin": None,
                "condition_1": None, "condition_2": None,
                "meets_both": False,
                "note": "TOT/FIN unsettled in the landed Table I - "
                        "cannot be shown to meet the conditions (FF-7)",
            })
            continue
        tot, fin = cells[4], cells[3]
        if tot == 2:
            candidates_m77.append({
                "m77_sign": sign, "tot": tot, "fin": fin,
                "condition_1": True, "condition_2": fin == 0,
                "meets_both": fin == 0,
            })
    candidates_m77 = [c for c in candidates_m77
                      if c["condition_1"] or c["tot"] is None]
    candidates_wells = []
    for r in wells_rows:
        if r["status"] == "NOT PRINTED":
            continue
        tot_raw = (r["total"] or "").strip()
        if not tot_raw.lstrip("-").isdigit() or int(tot_raw) != 2:
            continue
        wsign = int(r["sign_no"])
        target = wells_pairing.get(wsign)
        entry = {
            "wells1998_sign": wsign, "total": 2,
            "fig36_mahadevan_pairing": target,
            "condition_1": True,
        }
        if target is None:
            entry.update({
                "condition_2": False, "meets_both": False,
                "note": "no Figure 3.6 pairing - no final-position "
                        "rate in its own list (FF-6)"})
        else:
            cells = table1.get(target)
            if cells is None:
                entry.update({
                    "condition_2": False, "meets_both": False,
                    "note": f"paired M77 sign {target} unsettled in "
                            "the landed Table I (FF-7)"})
            else:
                rate = cells[3] / cells[4] if cells[4] else 0.0
                entry.update({
                    "paired_final_rate": rate,
                    "condition_2": rate <= 0.10,
                    "meets_both": rate <= 0.10})
        candidates_wells.append(entry)
    identities = (
        [{"list": "mahadevan_1977", "sign": c["m77_sign"]}
         for c in candidates_m77 if c["meets_both"]]
        + [{"list": "wells_1998", "sign": c["wells1998_sign"]}
           for c in candidates_wells if c["meets_both"]])
    record["token_999_attack"] = {
        "reference": {"occurrences": 2, "finals": 0, "final_rate": 0.0},
        "candidates_m77_tot2": candidates_m77,
        "candidates_wells1998_total2": candidates_wells,
        "identities_meeting_both": identities,
    }
    record["verdicts"]["F077-C02"] = (
        {"identity": identities} if identities
        else "NO PUBLISHED IDENTITY")
    record["outcome"] = "EXECUTED"
    record["anchors_after"] = sha256(PINS["anchors"][0])
    record["anchors_byte_identical"] = (
        record["anchors_after"] == anchors_before)
    out_path.write_text(json.dumps(record, indent=1) + "\n",
                        encoding="utf-8")
    print(f"EXECUTED: witnessed {n_witnessed}/557 raw "
          f"({n_witnessed / 557:.4f}); M77 {n_m77}/557 adjusted "
          f"({n_m77 / 557:.4f}); gap {len(gap)}; "
          f"C01 {record['verdicts']['F077-C01']}; "
          f"C02 {record['verdicts']['F077-C02']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
