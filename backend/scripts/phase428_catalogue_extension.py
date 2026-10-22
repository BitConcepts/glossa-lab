"""Phase-428 (Spec 066) — Phase-130 catalogue extension.

Executes the frozen Spec 066 contract (freeze digest
recorded in specs/066-phase130-catalogue-extension/
freeze.json): grade every distinct well-formed
CISI Vol. 3.1 portion number (2,101 candidates:
1,341 referenced by Phase-421 census rows, 760
unreferenced) under the fixed ladder of spec
section 5.3, hand-check the frozen seeded stratum
(seed 20261021, DD-066-5), apply the halt rule of
spec section 5.5 (CONFLICT share of all graded
candidates above 20 percent, or any stratum
attribution to true non-identity), and - on pass
only - build the merged catalogue layer v2
LOCALLY, validate its extension dataset form with
the pinned Phase-130 validator, and write the
section 4 products (the extension index into the
repo tree; the aggregate census as the phase
machine record).

RESTRICTED MATERIAL (Phase-130 gate, PROVENANCE
entry 22): the portion PDF, the extraction table,
all page renders, the grade table, the build
record, the stratum record, the dataset form, and
the merged layer live in the restricted local
store only and are never written into the repo
tree beyond the section 4 line. This script reads
them locally; its committed outputs are the
extension index (number + site section + type
class + grade class) and aggregate JSON only.

Stages:
  census    step 0 + grading + stratum draw.
            Requires the low-confidence
            hand-verification file (written by the
            execution's render check) to cover
            every low-gated candidate; without it
            the stage writes an AWAITING record
            and exits 2 - grading does not
            complete on unverified low cells.
  finalise  reads the local stratum attribution
            file, applies the medium-coverage
            determination, evaluates the halt
            rule, and on pass builds + validates +
            pins. Writes the final aggregate
            record (reports/phase428_results.json).

The experiment graph node serves the committed
results JSON; the script's local inputs are
absent from CI, so the node serves committed
results there.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

SEED = 20261021  # DD-066-5: fixed at the freeze, recorded before sampling
FREEZE_DIGEST = (
    "0b81d8421c8fe66b486b2c729bb7e978faa6327c74b8f1bff7984128a31aa355"
)

REPO = Path(__file__).resolve().parents[2]
MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
PORTION_DIR = Path(os.environ.get(
    "PORTION_DIR",
    "/home/hatch/workspace/research_notes/indus-data-deep-sweep-20261008"
    "/downloads/oakland-ill-cisi31-portion"))
PROVENANCE = Path(os.environ.get(
    "PROVENANCE_MD",
    "/home/hatch/workspace/research_notes/indus-data-deep-sweep-20261008"
    "/downloads/PROVENANCE.md"))
SWEEP = Path(
    "/home/hatch/workspace/research_notes/indus-data-deep-sweep-20261008"
    "/downloads")
HORUS84 = SWEEP / "horus84-computational-linguistics" / "data" / "inscriptions.csv"
CATALOGUE_REL = Path("corpora") / "downloads" / "cisi_image_layer" / "catalogue"
RESULTS_OUT = Path(os.environ.get(
    "RESULTS_OUT", str(REPO / "reports" / "phase428_results.json")))
LOCAL_RESULTS = Path(os.environ.get(
    "LOCAL_RESULTS_OUT",
    "/home/hatch/workspace/glossa-run/spec066-work/phase428_results.json"))
INDEX_OUT = Path(os.environ.get(
    "INDEX_OUT", str(REPO / "data" / "intake" / "cisi31_extension_index.csv")))

PDF_NAME = "376929.pdf"
TABLE_NAME = "cisi31-basic-data.csv"
GRADE_TABLE_NAME = "phase428-grade-table.csv"
BUILD_RECORD_NAME = "phase428-build-record.json"
LOW_VERIF_NAME = "phase428-low-verification.json"
STRATUM_ATTR_NAME = "phase428-stratum-attribution.json"
DATASET_NAME = "phase428-extension-dataset.json"
MERGED_NAME = "cisi_catalogue_layer_v2.csv"

PINS = {
    "portion_pdf": (
        "514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a",
        8206446),
    "extraction_table": (
        "7179858d9b2bc18b480ba092a08ea2ee021ce569fcaceb5b992d22c541d333c8",
        None),
    "vol1": (
        "e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e",
        804665),
    "vol2": (
        "e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9",
        1431631),
    "horus84": (
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
        1190884),
    "phase421_census": (
        "952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8",
        None),
    "phase421_results": (
        "3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f",
        None),
    "intake_schema": (
        "b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b",
        6197),
    "intake_validator": (
        "02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03",
        18867),
}

SECTION_TO_SITE = {
    "Mohenjo-daro": "Mohenjo-daro",
    "Harappa (EH)": "Harappa",
    "Harappa (HARP)": "Harappa",
}
SECTION_LABEL = {
    "Mohenjo-daro": "Mohenjo-daro",
    "Harappa (EH)": "Harappa old",
    "Harappa (HARP)": "Harappa HARP",
}
HALT_CAP = 0.20  # DD-066-4: conflict share of all graded candidates
WELLFORMED = re.compile(r"^[A-Z]+-\d+$")

GATE_LICENSE_BASIS = (
    "Phase-130 intake gate, PROVENANCE entry 22 "
    "(recorded 2026-10-20, before any processing): "
    "Classification: restricted research material. "
    "ILL-supplied copies are made for the requesting "
    "patron's own study; they are not the program's "
    "to distribute, deposit, or publish. Permitted: "
    "local research use on this machine; OCR and "
    "table extraction for analysis; derived "
    "statistics, counts, and feature vectors "
    "(publishable, as with all restricted sources in "
    "this program); citation of facts (page counts, "
    "yields, field values) in program reports. Not "
    "permitted: redistributing scans or page images; "
    "uploading the material to the repo, Zenodo, "
    "OSF, or any third-party service; sharing copies "
    "with collaborators; bulk reproduction beyond "
    "the received portion. Any ambiguous use waits "
    "for an owner ruling. The delivery carried no "
    "stricter terms, so the plan's terms govern as "
    "written. The section 4 item-1 fact list of "
    "Spec 066 (number + site section + published "
    "type class + grade class) is a publishable "
    "derived fact list under the owner's approved "
    "reading of 2026-10-21; this dataset form itself "
    "stays in the restricted local store."
)


class Step0Failure(Exception):
    def __init__(self, check: str, detail: str):
        super().__init__(f"step 0 closed at {check}: {detail}")
        self.check = check
        self.detail = detail


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pin(name: str, path: Path) -> dict:
    pin, size = PINS[name]
    digest = sha256_file(path)
    if digest != pin:
        raise Step0Failure("0.2", f"{name} hash {digest} != pin")
    if size is not None and path.stat().st_size != size:
        raise Step0Failure("0.2", f"{name} bytes != pin")
    return {"sha256": digest, "bytes": path.stat().st_size}


def catalogue_dir() -> Path:
    for cand in (REPO / CATALOGUE_REL, MAIN_CHECKOUT / CATALOGUE_REL):
        if (cand / "cisi_vol1_catalogue.csv").exists():
            return cand
    raise Step0Failure("0.2", "vols. 1-2 catalogue dir not found locally")


# ---- frozen object-type rules (Spec 037 section 4.3, carried) ----
_HEADING_OTHER_NOUNS = (
    "POTTERY", "BANGLES", "BANGLE", "RINGS", "RING", "WEIGHTS",
    "WEIGHT", "TOOLS", "TOOL", "BEADS", "BEAD", "ORNAMENTS",
    "ORNAMENT", "FIGURINES", "FIGURINE", "VESSELS", "VESSEL",
    "INSCRIBED",
)


def portion_type_class(heading: str) -> str | None:
    u = (heading or "").upper()
    if not u.strip():
        return None
    if "IMPRESSION" in u or "SEALING" in u:
        return "seal impression"
    keys = []
    for token, cls in (("TABLET", "tablet"), ("GRAFFITI", "graffiti"),
                       ("GRAFFITO", "graffiti"), ("IVORY STICK", "ivory stick"),
                       ("SEAL", "seal"), ("STONE", "stone object")):
        pos = u.find(token)
        if pos >= 0:
            keys.append((pos, cls))
    if keys:
        keys.sort(key=lambda t: (t[0],))
        return keys[0][1]
    if any(n in u for n in _HEADING_OTHER_NOUNS):
        return "other"
    return None


def step0() -> dict:
    record = {}
    # 0.1 gate record, quoted in the outcome
    prov = PROVENANCE.read_text(encoding="utf-8")
    idx = prov.find("## 22.")
    if idx < 0:
        raise Step0Failure("0.1", "PROVENANCE entry 22 heading not found")
    nxt = prov.find("\n## ", idx + 1)
    entry = prov[idx:nxt if nxt > 0 else len(prov)]
    for needle in ("oakland-ill-cisi31-portion",
                   "Classification: restricted research material",
                   "derived statistics, counts, and feature vectors (publishable",
                   "Not permitted: redistributing scans or page images; "
                   "uploading the material to the repo"):
        if needle not in entry:
            raise Step0Failure("0.1", f"gate entry lacks: {needle}")
    record["0.1_gate"] = (
        "PASS (PROVENANCE entry 22 on record, recorded 2026-10-20 "
        "before any processing; material classified restricted "
        "research material; gate quoted in the outcome record)")

    # 0.2 pins (local recomputation; committed pins were also
    # verified by the second route - the contents API - in the
    # execution record)
    pins = {}
    pins["portion_pdf"] = check_pin("portion_pdf", PORTION_DIR / PDF_NAME)
    table_bytes = (PORTION_DIR / TABLE_NAME).read_bytes()
    tdigest = hashlib.sha256(table_bytes).hexdigest()
    if tdigest != PINS["extraction_table"][0]:
        raise Step0Failure("0.2", f"extraction table hash {tdigest} != pin")
    pins["extraction_table"] = {
        "sha256": tdigest, "bytes": len(table_bytes)}
    rows = list(csv.DictReader(table_bytes.decode("utf-8").splitlines()))
    if len(rows) != 2123 or len(rows[0]) != 26:
        raise Step0Failure(
            "0.2", f"table parse {len(rows)}x{len(rows[0])} != 2123x26")
    sections = Counter(r["section"] for r in rows)
    if sections != {"Mohenjo-daro": 519, "Harappa (EH)": 510,
                    "Harappa (HARP)": 1094}:
        raise Step0Failure("0.2", f"section census {dict(sections)}")
    confs = Counter(r["cisi_number_conf"] for r in rows)
    if confs != {"high": 1933, "medium": 183, "low": 7}:
        raise Step0Failure("0.2", f"confidence census {dict(confs)}")
    cat_dir = catalogue_dir()
    pins["vol1"] = check_pin("vol1", cat_dir / "cisi_vol1_catalogue.csv")
    pins["vol2"] = check_pin("vol2", cat_dir / "cisi_vol2_catalogue.csv")
    pins["horus84"] = check_pin("horus84", HORUS84)
    census_path = REPO / "reports" / "phase421_join_census.json"
    pins["phase421_census"] = check_pin("phase421_census", census_path)
    pins["phase421_results"] = check_pin(
        "phase421_results", REPO / "reports" / "phase421_results.json")
    pins["intake_schema"] = check_pin(
        "intake_schema", REPO / "data" / "intake"
        / "intake_dataset_schema_v1.json")
    pins["intake_validator"] = check_pin(
        "intake_validator", REPO / "backend" / "glossa_lab" / "intake.py")
    record["0.2_pins"] = (
        "PASS (every section 2 pin recomputed locally to its frozen "
        "value; committed pins additionally verified by the contents "
        "API route in the execution record)")
    record["pins"] = pins

    # 0.3 candidate sets re-derived
    census = json.loads(census_path.read_text(encoding="utf-8"))
    by_id: dict[str, list[dict]] = {}
    for r in census["rows"]:
        oid = r.get("provenance_object_id")
        if oid:
            by_id.setdefault(oid, []).append(r)
    portion_numbers = {
        r["cisi_number"] for r in rows if WELLFORMED.match(r["cisi_number"] or "")}
    garbled = {r["cisi_number"] for r in rows} - portion_numbers
    referenced = portion_numbers & set(by_id)
    zero = {n for n in referenced
            if any(r["resolution_class"] == "zero" for r in by_id[n])}
    joined = {n for n in referenced
              if any(r["joined"] for r in by_id[n])}
    unreferenced = portion_numbers - referenced
    zero_rows = sum(1 for r in census["rows"]
                    if r.get("provenance_object_id") in zero)
    sets = {"total": len(portion_numbers), "garbled": len(garbled),
            "referenced": len(referenced), "zero": len(zero),
            "joined": len(joined), "unreferenced": len(unreferenced),
            "zero_rows": zero_rows}
    if sets != {"total": 2101, "garbled": 5, "referenced": 1341,
                "zero": 1293, "joined": 48, "unreferenced": 760,
                "zero_rows": 1790}:
        raise Step0Failure("0.3", f"candidate sets {sets} != spec section 3")
    record["0.3_candidate_sets"] = (
        "PASS (2,101 well-formed + 5 garbled; referenced 1,341 = "
        "1,293 zero-resolution + 48 already-joined, disjoint; "
        "unreferenced 760; zero-resolution rows 1,790)")
    record["candidate_sets"] = sets

    # corroboration base fact (DD-066-7): the in-hand layers carry
    # no FC / excavation / museum fields
    vol1_header = next(csv.reader(
        (cat_dir / "cisi_vol1_catalogue.csv").open(encoding="utf-8")))
    vol2_header = next(csv.reader(
        (cat_dir / "cisi_vol2_catalogue.csv").open(encoding="utf-8")))
    corpus_header = next(csv.reader(
        (REPO / "data" / "normalized" / "corpus_master.csv").open(
            encoding="utf-8")))
    for hdr in (vol1_header, vol2_header, corpus_header):
        for bad in ("fc", "excavation", "museum", "registration_no"):
            if bad in [h.lower() for h in hdr]:
                raise Step0Failure(
                    "0.3", "corroboration base fact moved: a layer "
                    "carries a corroboration field")
    record["0.3_corroboration_base"] = (
        "PASS (neither the vols. 1-2 layer nor the mayig layer "
        "carries FC/excavation/museum values; rung 5 UNGRADED for "
        "every candidate, DD-066-7)")

    # 0.4 repo cleanliness is checked by the caller against the
    # execution tree listing and appended to the step-0 record there.
    return {"record": record, "rows": rows, "census": census,
            "by_id": by_id, "sets": sets, "cat_dir": cat_dir}


def grade_candidates(rows, by_id, low_verif: dict) -> tuple[list[dict], dict]:
    by_number: dict[str, list[dict]] = {}
    for r in rows:
        n = r["cisi_number"]
        if WELLFORMED.match(n or ""):
            by_number.setdefault(n, []).append(r)
    grades = []
    pending_low = []
    for n in sorted(by_number):
        recs = by_number[n]
        sites = {SECTION_TO_SITE[r["section"]] for r in recs}
        sections = sorted({r["section"] for r in recs})
        classes = {portion_type_class(r["section_heading"]) for r in recs}
        graded_classes = {c for c in classes if c is not None}
        confs = {r["cisi_number_conf"] for r in recs}
        ref_rows = by_id.get(n, [])
        ref_sites = {r["site"] for r in ref_rows}
        referenced = bool(ref_rows)

        def key(r):
            return (r["section"], portion_type_class(r["section_heading"]),
                    r["fc"].strip(), r["excavation"].strip(),
                    r["museum"].strip(), r["registration_no"].strip())
        ambiguous = len({key(r) for r in recs}) > 1

        outcome, reason = None, ""
        # rung 1 - site (single portion site vs referencing rows)
        if len(sites) == 1 and referenced and sites != ref_sites:
            outcome, reason = "CONFLICT", "SITE"
        # rung 2 - confidence gate (low)
        low_blocked = False
        if outcome is None and "low" in confs:
            v = low_verif.get(n)
            if v is None:
                pending_low.append(n)
                low_blocked = True
            elif not v.get("confirmed_as_printed"):
                low_blocked = True
        # rung 3 - ambiguity bar (incl. multi-site internal conflict)
        if outcome is None and ambiguous:
            outcome, reason = "CONFLICT", "NUMBER-AMBIGUOUS"
        if outcome is None:
            if low_blocked:
                outcome = "UNRESOLVED"
                reason = "CONFIDENCE-LOW-UNVERIFIED"
            else:
                outcome = "VERIFIED"
        grades.append({
            "cisi_number": n,
            "set": ("referenced" if referenced else "unreferenced"),
            "ref_class": (
                "zero" if any(r["resolution_class"] == "zero"
                               for r in ref_rows)
                else ("joined" if referenced else "")),
            "ref_rows": len(ref_rows),
            "portion_records": len(recs),
            "portion_sections": ";".join(sections),
            "site_section": ";".join(SECTION_LABEL[s] for s in sections),
            "portion_site": ";".join(sorted(sites)),
            "type_class": (
                next(iter(graded_classes)) if len(graded_classes) == 1
                else (";".join(sorted(graded_classes))
                      if graded_classes else "unfilled")),
            "confidence": (
                "low" if "low" in confs
                else ("medium" if "medium" in confs else "high")),
            "corroboration_graded": (
                "none (in-hand layers carry no FC/excavation/museum "
                "values)"),
            "outcome": outcome,
            "reason": reason,
        })
    return grades, {"pending_low": pending_low}


def census_block(grades: list[dict]) -> dict:
    total = len(grades)
    counts = Counter(g["outcome"] for g in grades)
    reasons = Counter(g["reason"] for g in grades
                      if g["outcome"] == "CONFLICT")
    def block(sub: list[dict]) -> dict:
        c = Counter(g["outcome"] for g in sub)
        keys = ("VERIFIED", "CONFLICT", "UNRESOLVED")
        return {
            "candidates": len(sub),
            "counts": {k: c.get(k, 0) for k in keys},
            "shares": ({k: round(c.get(k, 0) / len(sub), 4) for k in keys}
                       if sub else {k: 0.0 for k in keys}),
        }
    by_set = {s: block([g for g in grades if g["set"] == s])
              for s in ("referenced", "unreferenced")}
    by_ref_class = {s: block([g for g in grades if g["ref_class"] == s])
                    for s in ("zero", "joined")}
    by_section = {}
    for sec in ("Mohenjo-daro", "Harappa old", "Harappa HARP"):
        by_section[sec] = block(
            [g for g in grades if sec in g["site_section"].split(";")])
    conflict_share = counts.get("CONFLICT", 0) / total if total else 0.0
    return {
        "candidates": total,
        "counts": {k: counts.get(k, 0)
                   for k in ("VERIFIED", "CONFLICT", "UNRESOLVED")},
        "shares": {k: round(counts.get(k, 0) / total, 4)
                   for k in ("VERIFIED", "CONFLICT", "UNRESOLVED")},
        "conflict_reasons": dict(reasons),
        "by_set": by_set,
        "by_referenced_class": by_ref_class,
        "by_section": by_section,
        "graded_bases": {
            "site": sum(1 for g in grades if g["set"] == "referenced"),
            "confidence_gate": total,
            "ambiguity": total,
            "type_carriage": total,
            "corroboration": 0,
        },
        "graded_bases_note": (
            "corroborating keys ungraded for every candidate: "
            "neither in-hand layer carries FC, excavation, or "
            "museum/registration values (DD-066-7)"),
        "conflict_share": round(conflict_share, 4),
        "halt_threshold": HALT_CAP,
    }


def stage_census() -> int:
    out = {"spec": "066", "phase": "Phase-428",
           "freeze_digest": FREEZE_DIGEST}
    try:
        s0 = step0()
    except Step0Failure as e:
        out["step0"] = {"closed_at": e.check, "detail": e.detail}
        out["outcome"] = f"CLOSED AT STEP 0 ({e.check})"
        write_local(out)
        print(json.dumps(out, indent=1))
        return 1
    out["step0"] = s0["record"]
    out["step0"]["0.4_repo_cleanliness"] = (
        "checked by the caller against the execution tree listing; "
        "result recorded in the outcome record (specs/066 "
        "outcome.md)")

    low_path = PORTION_DIR / LOW_VERIF_NAME
    low_verif = {}
    if low_path.exists():
        low_verif = json.loads(low_path.read_text(encoding="utf-8"))
    grades, gate = grade_candidates(s0["rows"], s0["by_id"], low_verif)
    if gate["pending_low"]:
        out["outcome"] = "AWAITING LOW HAND-VERIFICATION"
        out["pending_low_count"] = len(gate["pending_low"])
        write_local(out)
        print(json.dumps({"step0": "PASS",
                          "outcome": out["outcome"],
                          "pending_low_count": len(gate["pending_low"])},
                         indent=1))
        return 2
    out["census"] = census_block(grades)
    low_conf = [g for g in grades if g["confidence"] == "low"]
    out["confidence_gate"] = {
        "low_candidates": len(low_conf),
        "low_hand_verified_confirmed": sum(
            1 for g in low_conf
            if (low_verif.get(g["cisi_number"]) or {}).get(
                "confirmed_as_printed")),
        "low_unresolved": sum(1 for g in low_conf
                              if g["outcome"] == "UNRESOLVED"),
        "medium_candidates": sum(1 for g in grades
                                 if g["confidence"] == "medium"),
        "medium_verified_provisional": sum(
            1 for g in grades if g["confidence"] == "medium"
            and g["outcome"] == "VERIFIED"),
    }

    # local grade table (restricted store only)
    grade_path = PORTION_DIR / GRADE_TABLE_NAME
    with grade_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(grades[0].keys()))
        w.writeheader()
        w.writerows(grades)

    # stratum: seeded, seed fixed at the freeze before sampling
    rng = random.Random(SEED)
    def draw(cls, k):
        pool = sorted(g["cisi_number"] for g in grades
                      if g["outcome"] == cls)
        return pool if len(pool) <= k else sorted(rng.sample(pool, k))
    stratum = {"VERIFIED": draw("VERIFIED", 30),
               "CONFLICT": draw("CONFLICT", 15),
               "UNRESOLVED": draw("UNRESOLVED", 15)}
    supplement = []
    by_num = {g["cisi_number"]: g for g in grades}
    if not any(by_num[n]["confidence"] == "medium"
               for n in stratum["VERIFIED"]):
        pool = sorted(g["cisi_number"] for g in grades
                      if g["outcome"] == "VERIFIED")
        shuffled = pool[:]
        random.Random(SEED).shuffle(shuffled)
        for n in shuffled:
            if by_num[n]["confidence"] == "medium":
                supplement.append(n)
                break
    out["stratum"] = {
        "seed": SEED,
        "sizes": {k: len(v) for k, v in stratum.items()},
        "medium_supplement": len(supplement),
        "cause_counts": None,  # filled by the attribution step
    }
    out["local_products"] = {
        "grade_table": GRADE_TABLE_NAME,
        "grade_table_rows": len(grades),
        "build_record": BUILD_RECORD_NAME,
    }
    build = {"results": out, "stratum_members": stratum,
             "stratum_supplement": supplement,
             "stratum_members_are_local_only": True}
    (PORTION_DIR / BUILD_RECORD_NAME).write_text(
        json.dumps(build, indent=1) + "\n", encoding="utf-8")
    write_local(out)
    print(json.dumps({"step0": "PASS", "candidates": len(grades),
                      "counts": out["census"]["counts"],
                      "conflict_share": out["census"]["conflict_share"],
                      "stratum_sizes": out["stratum"]["sizes"],
                      "medium_supplement": len(supplement)}, indent=1))
    return 0


def write_local(out: dict) -> None:
    LOCAL_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_RESULTS.write_text(json.dumps(out, indent=1) + "\n",
                             encoding="utf-8")


TYPE_LABEL = {
    "seal": "Seals", "tablet": "Tablets", "graffiti": "Graffiti",
    "seal impression": "Seal impressions",
    "ivory stick": "Objects", "stone object": "Objects",
    "other": "Objects", "unfilled": "",
}


def stage_finalise() -> int:
    build_path = PORTION_DIR / BUILD_RECORD_NAME
    build = json.loads(build_path.read_text(encoding="utf-8"))
    out = build["results"]
    attr_path = PORTION_DIR / STRATUM_ATTR_NAME
    if not attr_path.exists():
        print(json.dumps({"outcome": "AWAITING STRATUM ATTRIBUTION"}))
        return 2
    attr = json.loads(attr_path.read_text(encoding="utf-8"))
    out["stratum"]["cause_counts"] = attr["conflict_causes"]
    out["stratum"]["sampled_verified_sound"] = attr["verified_sound"]
    out["stratum"]["sampled_unresolved_attributed"] = attr[
        "unresolved_attributed"]

    # medium-coverage determination (DD-066-6)
    grades = list(csv.DictReader(
        (PORTION_DIR / GRADE_TABLE_NAME).open(encoding="utf-8")))
    medium_error = bool(attr.get("medium_misextracted_found"))
    demoted = 0
    if medium_error:
        for g in grades:
            if (g["confidence"] == "medium"
                    and g["outcome"] == "VERIFIED"):
                g["outcome"] = "UNRESOLVED"
                g["reason"] = "CONFIDENCE-MEDIUM-CLASS-NOT-COVERED"
                demoted += 1
        with (PORTION_DIR / GRADE_TABLE_NAME).open(
                "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(grades[0].keys()))
            w.writeheader()
            w.writerows(grades)
        out["census"] = census_block(grades)
    out["confidence_gate"]["medium_class_covered"] = not medium_error
    out["confidence_gate"]["medium_demoted"] = demoted

    # halt evaluation (spec section 5.5)
    share = out["census"]["conflict_share"]
    nonidentity = attr["conflict_causes"].get("true_non_identity", 0)
    halted = share > HALT_CAP or nonidentity > 0
    out["halt"] = {
        "conflict_share": share, "threshold": HALT_CAP,
        "share_halt": share > HALT_CAP,
        "stratum_true_non_identity": nonidentity,
        "tripwire_halt": nonidentity > 0,
        "halted": halted,
    }
    if halted:
        out["outcome"] = "INTAKE COMPLETE — CATALOGUE EXTENSION HALTED"
        write_local(out)
        RESULTS_OUT.parent.mkdir(parents=True, exist_ok=True)
        RESULTS_OUT.write_text(json.dumps(out, indent=1) + "\n",
                               encoding="utf-8")
        build["results"] = out
        build_path.write_text(json.dumps(build, indent=1) + "\n",
                              encoding="utf-8")
        print(json.dumps({"outcome": out["outcome"],
                          "conflict_share": share,
                          "true_non_identity": nonidentity}, indent=1))
        return 0

    # ---- on pass: merged layer, validator, index, projection ----
    s0 = step0()  # re-assert pins in the finalise run
    rows = s0["rows"]
    cat_dir = s0["cat_dir"]
    vol_rows: list[dict] = []
    vol_fields: list[str] = []
    for vol in (1, 2):
        with (cat_dir / f"cisi_vol{vol}_catalogue.csv").open(
                encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            vol_fields = list(rd.fieldnames or [])
            vol_rows.extend(rd)
    existing_ids = {r["cisi_id"] for r in vol_rows}
    by_number: dict[str, list[dict]] = {}
    for r in rows:
        if WELLFORMED.match(r["cisi_number"] or ""):
            by_number.setdefault(r["cisi_number"], []).append(r)
    by_grade = {g["cisi_number"]: g for g in grades}
    verified = [g for g in grades if g["outcome"] == "VERIFIED"]
    collisions = [g["cisi_number"] for g in verified
                  if g["cisi_number"] in existing_ids]
    new_objects = [g for g in verified
                   if g["cisi_number"] not in existing_ids]
    extra_fields = ["fc", "excavation", "museum_registration",
                    "printed_page", "portion_section", "grade"]
    fields = vol_fields + [f for f in extra_fields if f not in vol_fields]
    merged_path = cat_dir / MERGED_NAME
    with merged_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in vol_rows:
            w.writerow({f: r.get(f, "") for f in fields})
        for g in new_objects:
            rec = by_number[g["cisi_number"]][0]
            row = {f: "" for f in fields}
            row.update({
                "volume": "3.1-portion",
                "cisi_id": g["cisi_number"],
                "site": g["portion_site"],
                "object_type": TYPE_LABEL.get(
                    g["type_class"].split(";")[0], ""),
                "extraction_basis": (
                    "Phase-428 catalogue extension (Spec 066); "
                    "type class as published, carried not compared"),
                "fc": rec["fc"], "excavation": rec["excavation"],
                "museum_registration": (
                    (rec["museum"] + " " + rec["registration_no"]).strip()),
                "printed_page": rec["printed_page"],
                "portion_section": rec["section"],
                "grade": "VERIFIED",
            })
            w.writerow(row)
    merged_rows = len(vol_rows) + len(new_objects)
    merged_distinct = len(existing_ids | {g["cisi_number"]
                                          for g in new_objects})
    merged_pin = {"file": MERGED_NAME, "sha256": sha256_file(merged_path),
                  "bytes": merged_path.stat().st_size,
                  "rows": merged_rows,
                  "distinct_objects": merged_distinct,
                  "base_rows": len(vol_rows),
                  "base_distinct_objects": len(existing_ids),
                  "new_objects": len(new_objects),
                  "collisions_existing_object_stands": len(collisions)}
    out["merged_layer"] = merged_pin

    # extension dataset form (local only) + pinned validator
    sys.path.insert(0, str(REPO / "backend"))
    from glossa_lab.intake import validate_dataset  # noqa: E402
    inscriptions = []
    for g in verified:
        ins = {
            "inscription_id": f"phase428-{g['cisi_number']}",
            "site": g["portion_site"],
            "tokens": [],
            "sign_list": "other",
            "sign_list_detail": (
                "no sign transcription carried - CISI catalogue "
                "object record (Phase-130 extension)"),
            "provenance": {
                "source_reference": (
                    "CISI Vol. 3.1, Basic data for the objects "
                    "illustrated (printed pp. 413-443); portion "
                    "copy via Oakland ILL 2026-10-14; catalogue "
                    "number as printed"),
                "object_id": g["cisi_number"],
                "transcriber": (
                    "Glossa Lab Phase-428 intake (extraction of "
                    "2026-10-20, Spec 037 record)"),
            },
        }
        if g["type_class"] != "unfilled" and ";" not in g["type_class"]:
            ins["object_type"] = g["type_class"]
        inscriptions.append(ins)
    dataset = {
        "schema_version": "1.0",
        "dataset_name": "phase428-cisi31-catalogue-extension",
        "source": (
            "CISI Vol. 3.1 portion (Oakland ILL) via Phase-130 "
            "intake; Spec 066 catalogue extension"),
        "source_class": "future_concordance",
        "license_basis": GATE_LICENSE_BASIS,
        "upstream_lineage": {
            "derived_from": (
                "CISI Vol. 3.1 printed portion and the "
                "programme extraction table (restricted local "
                "store)"),
            "is_derivation_input": False,
        },
        "compiler": "Glossa Lab Phase-428 build",
        "acquisition_date": "2026-10-14",
        "inscriptions": inscriptions,
    }
    (PORTION_DIR / DATASET_NAME).write_text(
        json.dumps(dataset, indent=1) + "\n", encoding="utf-8")
    verdict = validate_dataset(dataset)
    out["validator"] = {
        "verdict": verdict["verdict"],
        "errors": len(verdict["errors"]),
        "warnings": len(verdict["warnings"]),
        "summary": verdict["summary"],
        "dataset_records": len(inscriptions),
        "dataset_form": DATASET_NAME + " (restricted local store only)",
        "license_basis": (
            "the entry-22 gate, quoted in the dataset form"),
    }
    if verdict["verdict"] == "reject":
        out["outcome"] = "INTAKE COMPLETE — CATALOGUE EXTENSION HALTED"
        out["halt"]["validator_reject"] = True
        out["halt"]["halted"] = True
        write_local(out)
        RESULTS_OUT.write_text(json.dumps(out, indent=1) + "\n",
                               encoding="utf-8")
        build["results"] = out
        build_path.write_text(json.dumps(build, indent=1) + "\n",
                              encoding="utf-8")
        print(json.dumps({"outcome": out["outcome"],
                          "validator": verdict["verdict"]}, indent=1))
        return 0

    # extension index (the section 4 item-1 fact list) into the tree
    INDEX_OUT.parent.mkdir(parents=True, exist_ok=True)
    with INDEX_OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["cisi_number", "site_section", "object_type_class",
                    "grade_class"])
        for g in sorted(grades, key=lambda x: x["cisi_number"]):
            w.writerow([g["cisi_number"], g["site_section"],
                        g["type_class"], g["outcome"]])
    out["extension_index"] = {
        "file": "data/intake/cisi31_extension_index.csv",
        "sha256": sha256_file(INDEX_OUT),
        "bytes": INDEX_OUT.stat().st_size,
        "rows": len(grades),
        "entered_objects_verified": len(verified),
    }

    # projection (spec section 5.7 - arithmetic, labelled)
    census = s0["census"]
    new_ids = {g["cisi_number"] for g in verified
               if g["ref_class"] == "zero"}
    projected_rows = sum(
        1 for r in census["rows"]
        if r.get("provenance_object_id") in new_ids)
    joined_now = census["summary"]["joined_rows"]
    out["projection"] = {
        "label": (
            "PROJECTION - no join has run; arithmetic over the "
            "committed Phase-421 census and this act's grades"),
        "already_joined_rows": joined_now,
        "newly_resolved_rows_projected": projected_rows,
        "projected_joined_rows": joined_now + projected_rows,
        "projected_share_percent": round(
            100.0 * (joined_now + projected_rows)
            / census["summary"]["layer_rows"], 2),
        "bar_rows": census["gate_bar"]["joined_rows_min"],
        "margin_rows": (joined_now + projected_rows
                        - census["gate_bar"]["joined_rows_min"]),
    }
    out["type_fill_entered"] = dict(Counter(
        g["type_class"] for g in verified))
    out["outcome"] = (
        "INTAKE COMPLETE — CATALOGUE EXTENSION PINNED")
    write_local(out)
    RESULTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_OUT.write_text(json.dumps(out, indent=1) + "\n",
                           encoding="utf-8")
    build["results"] = out
    build_path.write_text(json.dumps(build, indent=1) + "\n",
                          encoding="utf-8")
    print(json.dumps({"outcome": out["outcome"],
                      "merged": merged_pin,
                      "validator": out["validator"]["verdict"],
                      "projection": out["projection"]}, indent=1))
    return 0


def main() -> int:
    stage = sys.argv[1] if len(sys.argv) > 1 else "census"
    if stage == "census":
        return stage_census()
    if stage == "finalise":
        return stage_finalise()
    print(f"unknown stage {stage!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
