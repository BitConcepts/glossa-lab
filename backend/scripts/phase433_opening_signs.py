#!/usr/bin/env python3
"""Phase 433 — Spec 070 execution: are Shakti's opening-strong
signs the animal signs (re-scoped form)?

Runs the frozen Spec 070 contract (freeze digest
763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e):
the step-0 gates in order, then one counting run.

Gate order (spec section 5, fail-closed):
  0.1 Asset A asserted: Spec 069's asset-a-freeze.json present in
      the merged record; the canonical CSV's digest recomputes to
      the value the freeze quoted (95231935...); the freeze record's
      per-kind counts match the presented file's.
  0.2 Shakti intake (P-F1 S1/S2): both restricted-local files hash
      to their pins; the census reproduces (5,704 rows; 5,536
      analyzable; grades 3,212/2,087/405; 4,904 of 5,536 analyzable
      rows carrying a CISI identifier, cisi != '-').
  0.3 Input integrity: the section 3 inputs in the tree (canonical
      registry, crosswalk, anchors) hash to their freeze values.
  0.4 Population: the section 2 battery over the primary
      population (documented-lineage rows only); O (INITIAL_STRONG)
      enumerated in full in Wells space and its canonical
      enumeration hashed BEFORE any join (gate 0.6's proof);
      every O sign keyed under DD-070-9 (ICIT code = Wells number,
      resolved through the canonical registry's parpola_1982 rows'
      wells_ids to exactly one Asset A sign_key). An unkeyable O
      sign closes the execution as POPULATION NOT KEYED
      (DD-070-11).
  0.5 Census: U (total >= 30 under DD-070-10) enumerated with
      counts; the S-B unicorn naming scan over Asset A's verbatim
      labels; the full battery class counts published; every O and
      U sign shown to carry an Asset A row (else INVALID).
  0.6 Freeze-order proof: recorded in the results in order
      (freeze digest; asset digest; population hash; join after).

Battery (spec section 2): sequences are the population rows' sign
sequences with the gated ICIT-000 placeholder removed (it is not a
sign occurrence; the all-000 rows therefore contribute nothing,
as the spec states); a sequence of length >= 2 contributes one I
(first), one T (last) and M for positions between, in the corpus's
recorded order, no reversal. total = I+M+T; floor total >= 5;
cascade TERMINAL_STRONG t>=0.60, INITIAL_STRONG i>=0.55,
MEDIAL_STRONG m>=0.65, TERMINAL_MODERATE t>=0.40,
INITIAL_MODERATE i>=0.40, else MIXED (first match wins).
Threshold-only; no chance-baseline step exists in the battery or
in this script (G5 attestation).

Test (spec section 4): R1 = animal share of O / animal share of U
over classified members (contested and unidentified excluded from
both numerator and denominator, counted and listed); Fisher exact
on the disjoint 2x2 (O vs U minus O), one-sided p the criterion,
two-sided published. R2 = among U's animal signs the share in O
over the same share for U's non-animal signs, Fisher exact on the
corresponding table. Precedence (section 4.3): NOT SUPPORTED if
R1 <= 1.0 or p >= 0.05; SUPPORTED if R1 >= 1.5, p < 0.05 and
R2 > 1.0; otherwise INCONCLUSIVE. Sensitivities: S-A contested
included under CISI-governed labels; S-B unicorn removed (or not
applicable); S-C the documented + corroborated population with
classes re-derived, its verdict computed under the same
precedence and any change reported as grade-sensitive (P-F1 S4).

The corpus and grades files are restricted-local and never enter
the repository; only derived quantities are written, to
reports/phase433_results.json. Counts are over distinct signs
(the test's units are signs, per section 4).
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DOWNLOADS = Path(
    "/home/hatch/workspace/research_notes/"
    "indus-data-deep-sweep-20261008/downloads"
)
CORPUS_FILE = (
    DOWNLOADS / "shaktiosindia-indus-sign-regimes-deposit"
    / "sanitized_corpus.json"
)
GRADES_FILE = DOWNLOADS / "shakti_row_grades_2026-10-22.csv"

ASSET_DIR = REPO / "specs/069-hunt-asset-a/asset-a"
ASSET_FREEZE = ASSET_DIR / "asset-a-freeze.json"
ASSET_CSV = ASSET_DIR / "depicted-kind-classification.csv"
SPEC069_FREEZE = REPO / "specs/069-hunt-asset-a/freeze.json"
REGISTRY = REPO / "data/crosswalks/canonical_sign_registry.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
RESULTS = REPO / "reports/phase433_results.json"

ASSET_SHA256 = "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b"
SPEC069_FREEZE_DIGEST = "657b930c9200299c7d540baa8ed51b7a90176bdea9822577e9cb1f4d292f99aa"
SPEC070_FREEZE_DIGEST = "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e"
CORPUS_SHA256 = "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
GRADES_SHA256 = "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
REGISTRY_SHA256 = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
CROSSWALK_SHA256 = "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
ANCHORS_SHA256 = "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"

GRADE_DOCUMENTED = "documented-lineage"
GRADE_CORROBORATED = "undocumented-corroborated"
GRADE_UNCORROBORATED = "undocumented-uncorroborated"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon_sha(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


# ── Fisher exact test (exact integer hypergeometric) ──────────────

def _hypergeom_pmf(k, n_total, n_drawn, n_success):
    """P(X = k), X ~ Hypergeometric(N=n_total, K=n_success, n=n_drawn)."""
    if k < 0 or k > n_success or k > n_drawn or (n_drawn - k) > (n_total - n_success):
        return 0.0
    return (
        math.comb(n_success, k)
        * math.comb(n_total - n_success, n_drawn - k)
        / math.comb(n_total, n_drawn)
    )


def fisher_exact(table):
    """table [[a, b], [c, d]] -> (one-sided greater p, two-sided p)."""
    (a, b), (c, d) = table
    n = a + b + c + d
    row1 = a + b
    col1 = a + c
    lo = max(0, row1 - (n - col1))
    hi = min(row1, col1)
    p_obs = _hypergeom_pmf(a, n, row1, col1)
    p_greater = sum(
        _hypergeom_pmf(k, n, row1, col1) for k in range(a, hi + 1)
    )
    p_two = sum(
        p for k in range(lo, hi + 1)
        if (p := _hypergeom_pmf(k, n, row1, col1)) <= p_obs * (1 + 1e-9)
    )
    return p_greater, p_two


# ── Battery ───────────────────────────────────────────────────────

def derive_battery(rows):
    """rows: list of symbol lists. Returns per-sign counts/classes."""
    counts: dict[str, list[int]] = {}
    for symbols in rows:
        signs = [s for s in symbols if s != "000"]
        if len(signs) < 2:
            continue
        for pos, sign in enumerate(signs):
            slot = counts.setdefault(sign, [0, 0, 0])
            if pos == 0:
                slot[0] += 1
            elif pos == len(signs) - 1:
                slot[2] += 1
            else:
                slot[1] += 1
    derived = {}
    for sign, (i, m, t) in counts.items():
        total = i + m + t
        entry = {"I": i, "M": m, "T": t, "total": total, "class": None}
        if total >= 5:
            ir, mr, tr = i / total, m / total, t / total
            if tr >= 0.60:
                entry["class"] = "TERMINAL_STRONG"
            elif ir >= 0.55:
                entry["class"] = "INITIAL_STRONG"
            elif mr >= 0.65:
                entry["class"] = "MEDIAL_STRONG"
            elif tr >= 0.40:
                entry["class"] = "TERMINAL_MODERATE"
            elif ir >= 0.40:
                entry["class"] = "INITIAL_MODERATE"
            else:
                entry["class"] = "MIXED"
        derived[sign] = entry
    return derived


def keying_map() -> dict[str, set[str]]:
    wells: dict[str, set[str]] = {}
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["numbering_system"] != "parpola_1982":
                continue
            for token in (row["wells_ids"] or "").split("|"):
                token = token.strip()
                if token:
                    wells.setdefault(token, set()).add(row["sign_id"])
    return wells


def key_sign(code: str, wells: dict[str, set[str]]):
    """DD-070-9: ICIT code n -> Wells token W + n zero-padded."""
    token = "W" + code.zfill(3)
    hits = wells.get(token, set())
    if len(hits) == 1:
        return next(iter(hits)), None
    if len(hits) == 0:
        return None, f"no parpola_1982 registry row carries Wells id {token}"
    return None, f"Wells id {token} resolves to {len(hits)} distinct sign ids"


def arm_quantities(o_set, u_set, kinds, contested_labels):
    """Compute one arm's quantities over classified members.

    kinds: sign_key -> depicted_kind for keyed signs.
    Returns the full quantity block for the (O, U) pair.
    """
    def classify(sign_keys):
        animal = [s for s in sign_keys if kinds[s] == "animal"]
        non = [s for s in sign_keys
               if kinds[s] not in ("animal", "contested", "unidentified")]
        contested = [s for s in sign_keys if kinds[s] == "contested"]
        unidentified = [s for s in sign_keys if kinds[s] == "unidentified"]
        return animal, non, contested, unidentified

    o_keys = [k for k in o_set.values()]
    u_keys = [k for k in u_set.values()]
    o_animal, o_non, o_cont, o_unid = classify(o_keys)
    u_animal, u_non, u_cont, u_unid = classify(u_keys)
    o_classified = set(o_animal) | set(o_non)
    # R1 table: O vs U\O (classified members only)
    a = len(o_animal)
    b = len(o_non)
    c = len([s for s in u_animal if s not in o_classified])
    d = len([s for s in u_non if s not in o_classified])
    share_o = a / (a + b) if (a + b) else None
    share_u = (a + c) / (a + b + c + d) if (a + b + c + d) else None
    r1 = (share_o / share_u) if (share_o is not None and share_u) else None
    p1_one, p1_two = fisher_exact([[a, b], [c, d]]) if (a + b + c + d) else (None, None)
    # R2 table: within U, (animal vs non-animal) x (in O vs not in O)
    a2 = len([s for s in u_animal if s in o_classified])
    b2 = len(u_animal) - a2
    c2 = len([s for s in u_non if s in o_classified])
    d2 = len(u_non) - c2
    share_animal_in_o = a2 / (a2 + b2) if (a2 + b2) else None
    share_non_in_o = c2 / (c2 + d2) if (c2 + d2) else None
    r2 = (share_animal_in_o / share_non_in_o) if (
        share_animal_in_o is not None and share_non_in_o) else None
    p2_one, p2_two = fisher_exact([[a2, b2], [c2, d2]]) if (a2 + b2 + c2 + d2) else (None, None)
    # S-A: contested included under CISI-governed labels.
    def classify_sa(sign_keys):
        animal = [s for s in sign_keys
                    if kinds[s] == "animal"
                    or (kinds[s] == "contested"
                        and contested_labels.get(s) == "animal")]
        non = [s for s in sign_keys
               if s not in animal and kinds[s] != "unidentified"]
        return animal, non
    oa, on = classify_sa(o_keys)
    ua, un = classify_sa(u_keys)
    oc = set(oa) | set(on)
    sa = len(oa); sb = len(on)
    sc_ = len([s for s in ua if s not in oc]); sd = len([s for s in un if s not in oc])
    share_o_sa = sa / (sa + sb) if (sa + sb) else None
    share_u_sa = (sa + sc_) / (sa + sb + sc_ + sd) if (sa + sb + sc_ + sd) else None
    r1_sa = (share_o_sa / share_u_sa) if (share_o_sa is not None and share_u_sa) else None
    psa_one, psa_two = fisher_exact([[sa, sb], [sc_, sd]]) if (sa + sb + sc_ + sd) else (None, None)
    return {
        "O_size": len(o_keys), "U_size": len(u_keys),
        "O_animal": a, "O_non_animal": b,
        "O_contested": len(o_cont), "O_unidentified": len(o_unid),
        "U_animal_total": a + c, "U_non_animal_total": b + d,
        "U_contested": len(u_cont), "U_unidentified": len(u_unid),
        "table_R1": [[a, b], [c, d]],
        "animal_share_O": share_o, "animal_share_U": share_u,
        "R1": r1, "p_one_sided": p1_one, "p_two_sided": p1_two,
        "table_R2": [[a2, b2], [c2, d2]],
        "animal_in_O_share_of_U_animals": share_animal_in_o,
        "non_animal_in_O_share_of_U_non_animals": share_non_in_o,
        "R2": r2, "R2_p_one_sided": p2_one, "R2_p_two_sided": p2_two,
        "S_A": {
            "table_R1": [[sa, sb], [sc_, sd]],
            "animal_share_O": share_o_sa, "animal_share_U": share_u_sa,
            "R1": r1_sa, "p_one_sided": psa_one, "p_two_sided": psa_two,
        },
    }


def verdict_of(q):
    r1, p, r2 = q["R1"], q["p_one_sided"], q["R2"]
    if r1 is None or p is None:
        return "INCONCLUSIVE"
    if r1 <= 1.0 or p >= 0.05:
        return "NOT SUPPORTED"
    if r1 >= 1.5 and p < 0.05 and (r2 is not None and r2 > 1.0):
        return "SUPPORTED"
    return "INCONCLUSIVE"


def main() -> int:
    gates: list[dict] = []
    results: dict = {
        "phase": 433, "spec": "070",
        "spec_freeze_digest": SPEC070_FREEZE_DIGEST,
        "asset_a_sha256": ASSET_SHA256,
        "execution_order": [
            "freeze (Spec 070, digest quoted)",
            "gate 0.1 asset assertion",
            "gate 0.2 intake assertion (P-F1 S1/S2)",
            "gate 0.3 input integrity",
            "gate 0.4 population enumerated + published (hash) BEFORE any join",
            "gate 0.5 comparison census + coverage",
            "gate 0.6 freeze-order proof (this record's order)",
            "join + test (section 4)",
        ],
        "g5_attestation": (
            "The Phase-43 battery applied here is threshold-only: it "
            "contains no chance-baseline step - no permutation, shuffle, "
            "or expected-rate baseline - and none is restored or "
            "claimed. The inventory-share comparison of section 4 is "
            "this design's own test construction, not a Phase-43 element."
        ),
        "lineage_statement_PF1_S3": (
            "Lineage (P-F1 S3): the positional classes were measured on "
            "the Shakti corpus deposit (Zenodo) as graded by the "
            "programme's intake record - documented-lineage rows are "
            "CISI-verifiable; corroborated rows are supported by an "
            "independent sign list; uncorroborated rows enter no count. "
            "The Phase-43 counts (805/2,267; the 40/61/20 classes) are "
            "never a basis for any quantity here."
        ),
    }

    def close(outcome: str, **extra):
        results["outcome"] = outcome
        results["gates"] = gates
        results.update(extra)
        RESULTS.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
        print(outcome)
        return 0

    anchors_before = sha256(ANCHORS)

    # ── Gate 0.1: Asset A ────────────────────────────────────────
    if not ASSET_FREEZE.exists() or not SPEC069_FREEZE.exists():
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "asset-a-freeze.json or Spec 069 freeze.json absent"})
        return close("ASSET NOT FROZEN")
    spec069_freeze = json.loads(SPEC069_FREEZE.read_text(encoding="utf-8"))
    asset_freeze = json.loads(ASSET_FREEZE.read_text(encoding="utf-8"))
    if spec069_freeze.get("digest") != SPEC069_FREEZE_DIGEST:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "Spec 069 freeze record digest mismatch"})
        return close("ASSET NOT FROZEN")
    observed_asset_sha = sha256(ASSET_CSV)
    if observed_asset_sha != ASSET_SHA256 or asset_freeze.get("sha256") != ASSET_SHA256:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": f"asset digest {observed_asset_sha}"})
        return close("ASSET PIN MISMATCH", observed_asset_sha256=observed_asset_sha)
    with ASSET_CSV.open(newline="", encoding="utf-8") as handle:
        asset_rows = list(csv.DictReader(handle))
    kinds: dict[str, str] = {}
    labels: dict[str, str] = {}
    contested_labels: dict[str, str] = {}
    per_kind: dict[str, int] = {}
    for row in asset_rows:
        kinds[row["sign_key"]] = row["depicted_kind"]
        labels[row["sign_key"]] = row["depicted_label_verbatim"]
        per_kind[row["depicted_kind"]] = per_kind.get(row["depicted_kind"], 0) + 1
    presented_counts = {
        kind: per_kind.get(kind, 0)
        for kind in ("animal", "sky_cycle", "object_goods", "human",
                     "other", "unidentified")
    }
    presented_counts["contested"] = sum(
        1 for row in asset_rows if row["dispute_status"] == "contested"
    )
    if presented_counts != asset_freeze["per_kind_counts"]:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "per-kind counts differ from freeze record"})
        return close("ASSET PIN MISMATCH")
    gates.append({"gate": "0.1", "result": "PASS",
                  "detail": "Asset A frozen (Spec 069 digest 657b930c...); "
                            "canonical CSV recomputes to 95231935...; "
                            "per-kind counts match the freeze record"})

    # ── Gate 0.2: Shakti intake, P-F1 S1/S2 ─────────────────────
    if sha256(CORPUS_FILE) != CORPUS_SHA256 or sha256(GRADES_FILE) != GRADES_SHA256:
        gates.append({"gate": "0.2", "result": "FAIL", "detail": "S1 hash mismatch"})
        return close("SHAKTI INTAKE NOT REPRODUCED")
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    with GRADES_FILE.open(newline="", encoding="utf-8") as handle:
        grades_rows = list(csv.DictReader(handle))
    grade_of = {g["shakti_id"]: g["grade"] for g in grades_rows}
    grade_counts = {}
    for g in grade_of.values():
        grade_counts[g] = grade_counts.get(g, 0) + 1
    analyzable = [r for r in corpus if not all(s == "000" for s in r["symbols"])]
    cisi_carrying = sum(1 for r in analyzable if r["cisi"] != "-")
    census_ok = (
        len(corpus) == 5704 and len(analyzable) == 5536
        and grade_counts.get(GRADE_DOCUMENTED) == 3212
        and grade_counts.get(GRADE_CORROBORATED) == 2087
        and grade_counts.get(GRADE_UNCORROBORATED) == 405
        and cisi_carrying == 4904
        and all(r["id"] in grade_of for r in corpus)
    )
    if not census_ok:
        gates.append({"gate": "0.2", "result": "FAIL",
                      "detail": f"S2 census: rows={len(corpus)} analyzable={len(analyzable)} "
                                f"grades={grade_counts} cisi={cisi_carrying}"})
        return close("SHAKTI INTAKE NOT REPRODUCED")
    gates.append({"gate": "0.2", "result": "PASS",
                  "detail": "S1 hashes recompute; S2 census reproduces "
                            "(5,704 rows; 5,536 analyzable; 3,212/2,087/405; "
                            "4,904 CISI-carrying)"})

    # ── Gate 0.3: input integrity ────────────────────────────────
    if (sha256(REGISTRY) != REGISTRY_SHA256
            or sha256(CROSSWALK) != CROSSWALK_SHA256
            or anchors_before != ANCHORS_SHA256):
        gates.append({"gate": "0.3", "result": "FAIL",
                      "detail": "a section 3 input hash differs from its freeze value"})
        return close("INVALID")
    gates.append({"gate": "0.3", "result": "PASS",
                  "detail": "registry, crosswalk and anchors hash to their freeze values"})

    # ── Populations ──────────────────────────────────────────────
    primary_rows = [r["symbols"] for r in corpus
                    if grade_of[r["id"]] == GRADE_DOCUMENTED]
    sc_rows = [r["symbols"] for r in corpus
               if grade_of[r["id"]] in (GRADE_DOCUMENTED, GRADE_CORROBORATED)]
    results["population_rows"] = {
        "primary_documented": len(primary_rows),
        "sensitivity_sc_documented_plus_corroborated": len(sc_rows),
    }

    derived_primary = derive_battery(primary_rows)
    class_counts: dict[str, int] = {}
    for e in derived_primary.values():
        if e["class"]:
            class_counts[e["class"]] = class_counts.get(e["class"], 0) + 1
    o_codes = sorted(
        s for s, e in derived_primary.items() if e["class"] == "INITIAL_STRONG"
    )
    population_publication = {
        "population": "primary (documented-lineage rows only)",
        "O_enumeration_wells_space": [
            {"wells_code": code,
             "I": derived_primary[code]["I"], "M": derived_primary[code]["M"],
             "T": derived_primary[code]["T"], "total": derived_primary[code]["total"]}
            for code in o_codes
        ],
        "battery_class_counts_primary": class_counts,
    }
    # Gate 0.4: publish (hash) the population BEFORE any join.
    pop_sha = canon_sha(population_publication)
    results["gate_0_4_population_publication_sha256"] = pop_sha
    results["population"] = population_publication

    wells = keying_map()
    o_keyed: dict[str, str] = {}
    unkeyable = []
    for code in o_codes:
        sign_key, reason = key_sign(code, wells)
        if sign_key is None:
            unkeyable.append({"wells_code": code, "reason": reason})
        else:
            o_keyed[code] = sign_key
    if unkeyable:
        gates.append({"gate": "0.4", "result": "CLOSE",
                      "detail": f"{len(unkeyable)} unkeyable O sign(s); DD-070-11 closure"})
        return close("POPULATION NOT KEYED", unkeyable_O_signs=unkeyable,
                     O_size=len(o_codes))
    gates.append({"gate": "0.4", "result": "PASS",
                  "detail": f"O enumerated in Wells space ({len(o_codes)} signs), "
                            f"publication sha {pop_sha[:16]}..., every sign keyed "
                            "to exactly one Asset A row under DD-070-9"})

    # ── Gate 0.5: census + coverage ──────────────────────────────
    u_codes = sorted(
        s for s, e in derived_primary.items() if e["total"] >= 30
    )
    u_keyed: dict[str, str] = {}
    missing_rows = []
    for code in u_codes:
        sign_key, reason = key_sign(code, wells)
        if sign_key is None or sign_key not in kinds:
            missing_rows.append({"wells_code": code, "reason": reason or "no Asset A row"})
        else:
            u_keyed[code] = sign_key
    for code, sign_key in o_keyed.items():
        if sign_key not in kinds:
            missing_rows.append({"wells_code": code, "reason": "no Asset A row"})
    unicorn_signs = sorted(
        k for k, lab in labels.items() if "unicorn" in lab.lower()
    )
    results["gate_0_5"] = {
        "U_enumeration": [
            {"wells_code": code, "sign_key": u_keyed.get(code),
             "total": derived_primary[code]["total"]}
            for code in u_codes
        ],
        "unicorn_signs_named_from_asset_labels": unicorn_signs,
        "S_B": ("applicable" if unicorn_signs else
                "not applicable - no Asset A verbatim label identifies a unicorn"),
    }
    if missing_rows:
        gates.append({"gate": "0.5", "result": "FAIL",
                      "detail": f"{len(missing_rows)} population sign(s) without an Asset A row"})
        return close("INVALID", population_signs_without_asset_row=missing_rows)
    gates.append({"gate": "0.5", "result": "PASS",
                  "detail": f"U enumerated ({len(u_codes)} signs, total >= 30); "
                            "every O and U sign carries an Asset A row; "
                            f"S-B unicorn naming: {unicorn_signs or 'none - not applicable'}"})
    gates.append({"gate": "0.6", "result": "PASS",
                  "detail": "order recorded in this file: freeze quoted the asset "
                            "digest; the population was hashed at gate 0.4 before "
                            "the join below was computed"})

    # ── The join + test (only now) ───────────────────────────────
    o_map = {code: o_keyed[code] for code in o_codes}
    u_map = {code: u_keyed[code] for code in u_codes}
    primary_q = arm_quantities(o_map, u_map, kinds, contested_labels)
    outcome = verdict_of(primary_q)

    # S-B: remove unicorn-keyed signs (none on this asset).
    sb_q = None
    if unicorn_signs:
        o_sb = {c: k for c, k in o_map.items() if k not in unicorn_signs}
        u_sb = {c: k for c, k in u_map.items() if k not in unicorn_signs}
        sb_q = arm_quantities(o_sb, u_sb, kinds, contested_labels)

    # S-C: re-derive on documented + corroborated.
    derived_sc = derive_battery(sc_rows)
    o_sc_codes = sorted(
        s for s, e in derived_sc.items() if e["class"] == "INITIAL_STRONG"
    )
    u_sc_codes = sorted(
        s for s, e in derived_sc.items() if e["total"] >= 30
    )
    o_sc_map, u_sc_map, sc_unkeyable = {}, {}, []
    for code in o_sc_codes + [c for c in u_sc_codes if c not in o_sc_codes]:
        sign_key, reason = key_sign(code, wells)
        if sign_key is None or sign_key not in kinds:
            sc_unkeyable.append({"wells_code": code, "reason": reason})
        elif code in o_sc_codes:
            o_sc_map[code] = sign_key
        if sign_key is not None and sign_key in kinds and code in u_sc_codes:
            u_sc_map[code] = sign_key
    sc_q = arm_quantities(o_sc_map, u_sc_map, kinds, contested_labels)
    sc_verdict = verdict_of(sc_q)

    results["join_sha256"] = canon_sha(
        {"O": o_map, "U": u_map, "primary": primary_q}
    )
    results["primary"] = primary_q
    results["S_B_quantities"] = sb_q
    results["S_C"] = {
        "O_size": len(o_sc_codes), "U_size": len(u_sc_codes),
        "unkeyable_signs_named": sc_unkeyable,
        "quantities": sc_q,
        "verdict_under_same_precedence": sc_verdict,
        "grade_sensitive": sc_verdict != outcome,
    }
    results["anchors_sha256_after"] = sha256(ANCHORS)
    results["anchors_byte_identical"] = results["anchors_sha256_after"] == anchors_before
    return close(outcome)


if __name__ == "__main__":
    raise SystemExit(main())
