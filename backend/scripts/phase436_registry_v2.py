#!/usr/bin/env python3
"""Spec 073 (Phase-436) Registry v2 build (spec section 4).

Emits data/crosswalks/canonical_sign_registry_v2.csv (the 803 v1 rows
byte-identical, in order; completions applied only where a ruled
published sign list states the identity; icit_wells rows appended for
frame codes no v1 row carries), the per-addition change schedule, the
no-published-identity schedule, and the registry freeze record.

Runs only on a PASS step-0 record. Restricted inputs (the Shakti
corpus and its row grades) are read from the owner's local
research-notes tree and never copied into the repository.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "specs" / "073-keying-surface-repair"
STEP0 = SPEC_DIR / "execution" / "step0-record.json"
CONSULT = SPEC_DIR / "execution" / "catalog-consult.json"
REG_V1 = ROOT / "data/crosswalks/canonical_sign_registry.csv"
REG_V2 = ROOT / "data/crosswalks/canonical_sign_registry_v2.csv"
OUT_DIR = SPEC_DIR / "registry-v2"
EXT = Path.home() / "workspace/research_notes/indus-data-deep-sweep-20261008/downloads"
MAYIG = Path.home() / "workspace/research_notes/hunt-chain-sources/mayig-indus-valley-script-corpus"
CORPUS = EXT / "shaktiosindia-indus-sign-regimes-deposit/sanitized_corpus.json"
GRADES = EXT / "shakti_row_grades_2026-10-22.csv"
PIN_V1 = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    step0 = json.loads(STEP0.read_text(encoding="utf-8"))
    if step0["verdict"] != "PASS":
        print("step-0 record is not PASS; registry build refuses to run")
        return 1
    consult = json.loads(CONSULT.read_text(encoding="utf-8"))
    v1_bytes = REG_V1.read_bytes()
    assert sha256_bytes(v1_bytes) == PIN_V1, "registry v1 pin mismatch"
    v1_rows = list(csv.DictReader(io.StringIO(v1_bytes.decode("utf-8"))))
    fieldnames = list(v1_rows[0].keys())
    assert len(v1_rows) == 803

    # --- attested frame (documented + corroborated strata), step-0 machinery ---
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    grade_of = {g["shakti_id"]: g["grade"] for g in csv.DictReader(GRADES.open())}

    def codes_where(pred):
        out: set[str] = set()
        for r in corpus:
            if any(s != "000" for s in r["symbols"]) and pred(grade_of[r["id"]]):
                out.update(s for s in r["symbols"] if s != "000")
        return out

    documented = codes_where(lambda g: g == "documented-lineage")
    frame = codes_where(lambda g: g in ("documented-lineage", "undocumented-corroborated"))

    def strata(code: str) -> list[str]:
        s = []
        if code in documented:
            s.append("documented")
        if code in frame - documented:
            s.append("corroborated")
        return s

    # --- v1 Wells map ---
    wells_map: dict[str, set[str]] = {}
    for r in v1_rows:
        if r["numbering_system"] != "parpola_1982":
            continue
        for token in (r["wells_ids"] or "").split("|"):
            token = token.strip()
            if token:
                wells_map.setdefault(token, set()).add(r["sign_id"])
    resolved = {c for c in frame if "W" + c in wells_map}

    # --- (a) completions: identities a ruled published sign list states ---
    # The CISI sign list as entered (mayig digitization) is the stating
    # instrument for the parpola_1982 rows; a token it states for a sign
    # that the row does not carry is a completion. The Fuls Catalog
    # section 2.5 concordance states Parpola (1994) numbers, which are
    # not this registry's numbering (see the consult record), so it
    # grounds no completion here.
    completions: list[dict] = []
    by_sign = {r["sign_id"]: r for r in v1_rows if r["numbering_system"] == "parpola_1982"}
    for feat_path in sorted((MAYIG / "features").glob("P*.json")):
        feat = json.loads(feat_path.read_text(encoding="utf-8"))
        row = by_sign.get(feat["id"])
        if row is None:
            continue
        carried = {t for t in (row["wells_ids"] or "").split("|") if t}
        for token in feat.get("wells_graphemes", []):
            if token not in carried:
                completions.append({
                    "sign_id": feat["id"], "added_wells_id": token,
                    "form": "wells_map_completion",
                    "source": "CISI sign list as digitized (mayig CISI digitization, upstream commit ad2f1e218a34b8c33c57de0d6cb8d99272765bbb)",
                    "statement": f"feature {feat['id']} states wells_graphemes including {token}",
                })
                carried.add(token)
                row["wells_ids"] = "|".join(sorted(carried))

    # --- (b) icit_wells rows + the section 4.3 accounting ---
    listed_page = {}
    for page, codes in consult["sign_list_codes_by_printed_page"].items():
        for c in codes:
            listed_page[str(c).zfill(3)] = int(page)
    additions: list[dict] = []
    new_rows: list[dict] = []
    no_identity: list[dict] = []
    contested: list[dict] = []
    for code in sorted(frame - resolved):
        token = "W" + code
        if code in listed_page:
            new_row = {k: "" for k in fieldnames}
            new_row["internal_id"] = str(uuid.uuid5(
                uuid.UUID("3f7a1c2e-9b4d-5e6a-8c0f-1d2e3a4b5c6d"), f"spec073-icit-wells-{token}"))
            new_row["sign_id"] = token
            new_row["numbering_system"] = "icit_wells"
            new_row["wells_ids"] = token
            new_row["description"] = ""
            new_rows.append(new_row)
            additions.append({
                "sign_id": token, "icit_code": code, "form": "icit_wells_row",
                "source": "Fuls 2023, A Catalog of Indus Signs, Chapter 2.3 sign list",
                "printed_page": listed_page[code],
                "statement": f"the sign list presents a sign under ICIT number {int(code)} (printed p. {listed_page[code]})",
                "attestation_strata": strata(code),
            })
        else:
            no_identity.append({
                "icit_code": code, "attestation_strata": strata(code),
                "disposition": "NO PUBLISHED IDENTITY",
                "sources_searched": consult["sources_searched_for_identity"],
                "note": ("attested in the corpus frame but stated in no ruled published sign list in hand; "
                         "the token is a corpus placeholder in the ICIT tradition (compare token 000, "
                         "gated out of sign analysis at intake) and is named here rather than dropped"),
            })

    # --- write v2: v1 bytes verbatim (with any completions applied) + appended rows ---
    if completions:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        for r in v1_rows:
            w.writerow(r)
        prefix = buf.getvalue().encode("utf-8")
    else:
        prefix = v1_bytes
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    for r in new_rows:
        w.writerow(r)
    v2_bytes = prefix + buf.getvalue().encode("utf-8")
    REG_V2.write_bytes(v2_bytes)

    # round-trip validation (section 8 hygiene): parse back; v1 rows
    # field-for-field equal; counts exact.
    parsed = list(csv.DictReader(io.StringIO(v2_bytes.decode("utf-8"))))
    assert len(parsed) == 803 + len(new_rows), "v2 row count"
    v1_orig = list(csv.DictReader(io.StringIO(v1_bytes.decode("utf-8"))))
    for i, r in enumerate(v1_orig):
        got = {k: parsed[i][k] for k in fieldnames}
        want = {k: r[k] for k in fieldnames}
        if completions:
            want["wells_ids"] = by_sign[r["sign_id"]]["wells_ids"] if r["sign_id"] in by_sign else want["wells_ids"]
        assert got == want, f"v1 row {i} altered beyond a recorded completion"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    schedule = {
        "spec": "073", "phase": 436, "product": "Registry v2 change schedule",
        "base": {"file": "data/crosswalks/canonical_sign_registry.csv", "sha256": PIN_V1, "rows": 803},
        "completions": completions,
        "icit_wells_additions": additions,
        "contested_identity": contested,
        "frame_accounting_section_4_3": {
            "attested_frame_codes": len(frame),
            "carried_by_v1_identity": len(resolved),
            "new_icit_wells_identity": len(additions),
            "no_published_identity": len(no_identity),
            "contested_identity": len(contested),
            "check": len(resolved) + len(additions) + len(no_identity) + len(contested) == len(frame),
        },
    }
    (OUT_DIR / "change-schedule.json").write_text(json.dumps(schedule, indent=1) + "\n", encoding="utf-8")
    (OUT_DIR / "no-published-identity.json").write_text(
        json.dumps({"spec": "073", "phase": 436, "entries": no_identity}, indent=1) + "\n", encoding="utf-8")
    freeze = {
        "product": "Registry v2 — canonical sign registry (Spec 073)",
        "canonical_file": "data/crosswalks/canonical_sign_registry_v2.csv",
        "sha256": sha256_bytes(v2_bytes),
        "rows_total": len(parsed),
        "rows_carried_from_v1": 803,
        "completions_applied": len(completions),
        "icit_wells_rows_appended": len(new_rows),
        "base_v1_sha256": PIN_V1,
        "consult_record": "specs/073-keying-surface-repair/execution/catalog-consult.json",
        "freeze_date": "2026-10-23",
    }
    (OUT_DIR / "registry-v2-freeze.json").write_text(json.dumps(freeze, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(freeze, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
