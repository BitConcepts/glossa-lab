"""Phase-402 (Spec 037) — CISI 3.1 concordance spine:
execution of the frozen concordance contract, in the
frozen order — step 0 (gate and integrity, fail-closed),
the pilot census under the fixed ladder, the halt rule,
the spine build behind the halt rule, and the HARP
provenance annex (Workstream B, gated on step 0 only).

Freeze: specs/037-cisi31-concordance-spine/freeze.md
(digest 122c2ea4858094d2c6514d05225dfaad1f5266cccffd764949736a78d81aa4db;
owner's standing pipeline authorisation of 2026-10-20,
freeze order 038, then 037, then 039, then 040). The
frozen spec's own contract registration: OSF
https://osf.io/j6t9k/ (filed 2026-10-20 under
DD-037-7; not a step-0 condition).

Step 0, in the frozen order (spec section 7),
fail-closed — any failure stops the execution there,
as itself, before any join is computed:

  0.1  Gate record: the Phase-130 gate is on record
       (restricted-store PROVENANCE entry 22) and
       names this material restricted (local use,
       extraction, and publishable derived statistics
       permitted; redistribution of scans or row data
       prohibited; nothing derived enters git).
  0.2  Portion integrity: the portion PDF's SHA-256
       equals the intake pin 514338b1...; the local
       table parse-validates at 2,123 records x 26
       columns with its intake census (sections
       519 / 510 / 1,094; 2,101 distinct catalogue
       numbers).
  0.3  corpus_master pin: the SHA-256 of the exact
       corpus bytes this run consumes equals
       b19cfe95... (2,722 rows; every source_object_id
       unique).
  0.4  Repo cleanliness: no portion-derived file in
       the repository tree (checked by the caller
       against the tree listing at the execution
       commit and recorded in the step-0 record).

Pilot (spec section 4): the candidate set is
regenerated — every exact-string match between a
catalogue number in the local table and a
corpus_master object id (the Holdat cisi_number is
prohibited as a join key and is never read here).
Each candidate is graded under the fixed ladder
(spec section 4.3): site agreement mandatory (the
fixed section-to-site mapping); object-type
agreement mandatory where graded (the frozen class
rules below; a side that cannot be classed is
UNGRADED, never forced); corroborating keys (FC
number, excavation number, museum/registration)
graded only where both sides carry a value — the
corpus side carries none of these fields in
corpus_master, so corroboration is UNGRADED for
every candidate in this run and the per-field
graded bases are recorded as 0; a number whose own
portion records differ on join-relevant data
(section-to-site, heading class, FC, excavation,
museum, registration) is barred from VERIFIED
(NUMBER-AMBIGUOUS). Outcome classes: VERIFIED /
CONFLICT (with reason code) / UNRESOLVED.

Halt rule (spec section 4.7, DD-037-4): if the
CONFLICT share of all candidates exceeds 20
percent, no spine file is written and the outcome
is PILOT COMPLETE - SPINE HALTED. Otherwise the
spine — VERIFIED joins only — is written as
cisi31-concordance-spine.csv INTO THE PORTION
FOLDER of the restricted store (never into the
repository; the repository records it by filename
and row count only).

Hand-check stratum (spec section 4.6, DD-037-5):
a seeded random sample of 60 (30 VERIFIED / 15
CONFLICT / 15 UNRESOLVED, the whole class where a
class is smaller), drawn after grading with the
seed recorded here, in the committed script,
BEFORE sampling: SEED = 20261020. The stratum's
per-candidate cause attribution is a human step
over the local build record; only the cause class
counts enter the reported aggregates.

Annex (spec section 5, DD-037-6 — inside this
phase, gated on step 0 only): dig-year, lot, and
period-code inventories and distributions from the
1,094 HARP rows of the same local table, as
printed, with the period fill always carrying its
floor caveat (the scan's text layer loses split
period tokens, so the fill is a floor, not the
printed rate). The annex changes no Spec 031 (Q7)
finding and feeds no verdict.

Inputs and outputs are local paths, overridable by
environment: PORTION_DIR (the restricted portion
folder), CORPUS_MASTER_CSV (the corpus file whose
bytes are pinned at 0.3), RESULTS_OUT (the
aggregate results JSON the repository records).
With the restricted inputs absent the script exits
non-zero at step 0 by design, and the graph node
serves the committed results.
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

SEED = 20261020  # DD-037-5: recorded before sampling (committed source)

PORTION_DIR = Path(os.environ.get(
    "PORTION_DIR",
    "/home/hatch/workspace/research_notes/indus-data-deep-sweep-20261008"
    "/downloads/oakland-ill-cisi31-portion"))
PROVENANCE = Path(os.environ.get(
    "PROVENANCE_MD",
    "/home/hatch/workspace/research_notes/indus-data-deep-sweep-20261008"
    "/downloads/PROVENANCE.md"))
CORPUS_PATH = Path(os.environ.get(
    "CORPUS_MASTER_CSV",
    "/home/hatch/workspace/glossa-lab/data/normalized/corpus_master.csv"))
RESULTS_OUT = Path(os.environ.get(
    "RESULTS_OUT", "/home/hatch/workspace/glossa-run/spec037-work/phase402_results.json"))

PDF_NAME = "376929.pdf"
PDF_SHA256 = "514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a"
TABLE_NAME = "cisi31-basic-data.csv"
CORPUS_SHA256 = "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
SPINE_NAME = "cisi31-concordance-spine.csv"
GRADE_TABLE_NAME = "phase402-grade-table.csv"
BUILD_RECORD_NAME = "phase402-build-record.json"

SECTION_TO_SITE = {
    "Mohenjo-daro": "Mohenjo-daro",
    "Harappa (EH)": "Harappa",
    "Harappa (HARP)": "Harappa",
}
HALT_CAP = 0.20  # DD-037-4: conflict share of all candidates


class Step0Failure(Exception):
    def __init__(self, check: str, detail: str):
        super().__init__(f"step 0 closed at {check}: {detail}")
        self.check = check
        self.detail = detail


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---- frozen object-type rules (spec section 4.3) ----
# Portion side: the record's section heading, uppercased.
# (1) IMPRESSION or SEALING in the heading -> seal impression.
# (2) else the earliest text position among TABLET -> tablet,
#     GRAFFITI/GRAFFITO -> graffiti, IVORY STICK -> ivory stick,
#     SEAL -> seal, STONE -> stone object (listed order breaks
#     ties).
# (3) else a concrete object noun from the extraction's
#     HEADING_TYPE vocabulary -> other.
# (4) else (blank or ADDENDA-only heading) -> no class (UNGRADED).
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


def corpus_type_class(artifact_type: str) -> str | None:
    u = (artifact_type or "").upper()
    if not u.strip():
        return None
    if "IMPRESSION" in u:
        return "seal impression"
    if "TABLET" in u:
        return "tablet"
    if "GRAFFITI" in u or "GRAFFITO" in u:
        return "graffiti"
    if "IVORY" in u:
        return "ivory stick"
    if "SEAL" in u:
        return "seal"
    return "other"


def step0() -> dict:
    record = {}
    # 0.1 gate record
    prov = PROVENANCE.read_text(encoding="utf-8")
    idx = prov.find("## 22.")
    if idx < 0:
        raise Step0Failure("0.1", "PROVENANCE entry 22 heading not found")
    entry = prov[idx:prov.find("\n## ", idx + 1) if prov.find("\n## ", idx + 1) > 0 else len(prov)]
    for needle in ("oakland-ill-cisi31-portion", "Do not upload",
                   "Local analysis and extraction: permitted"):
        if needle not in entry:
            raise Step0Failure("0.1", f"gate entry lacks: {needle}")
    record["0.1_gate"] = "PASS (PROVENANCE entry 22 on record; material restricted)"

    # 0.2 portion integrity
    pdf = PORTION_DIR / PDF_NAME
    digest = sha256_file(pdf)
    if digest != PDF_SHA256:
        raise Step0Failure("0.2", f"portion PDF hash {digest} != pin")
    table_bytes = (PORTION_DIR / TABLE_NAME).read_bytes()
    table_sha = hashlib.sha256(table_bytes).hexdigest()
    rows = list(csv.DictReader(table_bytes.decode("utf-8").splitlines()))
    if len(rows) != 2123 or len(rows[0]) != 26:
        raise Step0Failure("0.2", f"table parse {len(rows)}x{len(rows[0])} != 2123x26")
    sections = Counter(r["section"] for r in rows)
    if sections != {"Mohenjo-daro": 519, "Harappa (EH)": 510, "Harappa (HARP)": 1094}:
        raise Step0Failure("0.2", f"section census {dict(sections)} != intake census")
    distinct_numbers = {r["cisi_number"] for r in rows}
    if len(distinct_numbers) != 2101:
        raise Step0Failure("0.2", f"distinct numbers {len(distinct_numbers)} != 2101")
    record["0.2_portion"] = (
        f"PASS (PDF sha256 {digest[:12]}...; table 2123x26, sha256 "
        f"{table_sha[:12]}... — the execution's own step-0 hash of the "
        "local table, the intake having recorded no table hash; census as intaken)")

    # 0.3 corpus pin over the exact bytes consumed
    corpus_bytes = CORPUS_PATH.read_bytes()
    cdigest = hashlib.sha256(corpus_bytes).hexdigest()
    if cdigest != CORPUS_SHA256:
        raise Step0Failure("0.3", f"corpus_master hash {cdigest} != pin")
    crows = list(csv.DictReader(corpus_bytes.decode("utf-8").splitlines()))
    if len(crows) != 2722:
        raise Step0Failure("0.3", f"corpus rows {len(crows)} != 2722")
    ids = [r["source_object_id"] for r in crows]
    if len(set(ids)) != 2722:
        raise Step0Failure("0.3", "corpus source_object_id values are not unique")
    record["0.3_corpus"] = f"PASS (sha256 {cdigest[:12]}...; 2722 rows; ids unique)"

    # 0.4 repo cleanliness is checked by the caller against the
    # execution tree listing and appended to the step-0 record there.
    return {"record": record, "rows": rows, "crows": crows, "table_sha": table_sha}


def grade_candidates(rows, crows):
    corpus = {r["source_object_id"]: r for r in crows}
    by_number: dict[str, list[dict]] = {}
    for r in rows:
        by_number.setdefault(r["cisi_number"], []).append(r)
    candidates = sorted(n for n in by_number if n in corpus)
    grades = []
    for n in candidates:
        recs = by_number[n]
        crow = corpus[n]
        sites = {SECTION_TO_SITE[r["section"]] for r in recs}
        classes = {portion_type_class(r["section_heading"]) for r in recs}
        graded_classes = {c for c in classes if c is not None}
        corpus_class = corpus_type_class(crow["artifact_type"])
        # join-relevant record comparison (NUMBER-AMBIGUOUS basis)
        def key(r):
            return (r["section"], portion_type_class(r["section_heading"]),
                    r["fc"].strip(), r["excavation"].strip(),
                    r["museum"].strip(), r["registration_no"].strip())
        ambiguous = len({key(r) for r in recs}) > 1
        outcome, reason = None, ""
        if len(sites) > 1:
            # the portion's own records conflict on section-to-site,
            # a join-relevant field: barred from VERIFIED as
            # NUMBER-AMBIGUOUS (the corpus site matching one of the
            # records does not cure the internal conflict)
            outcome, reason = "CONFLICT", "NUMBER-AMBIGUOUS"
        elif sites and next(iter(sites)) != crow["site"]:
            outcome, reason = "CONFLICT", "SITE"
        elif len(graded_classes) == 1 and corpus_class and graded_classes != {corpus_class}:
            outcome, reason = "CONFLICT", "TYPE"
        elif ambiguous:
            outcome, reason = "CONFLICT", "NUMBER-AMBIGUOUS"
        elif not graded_classes:
            outcome, reason = "UNRESOLVED", ""
        else:
            outcome, reason = "VERIFIED", ""
        sections = sorted({r["section"] for r in recs})
        grades.append({
            "cisi_number": n,
            "corpus_id": crow["source_object_id"],
            "corpus_source": crow["source_name"],
            "portion_records": len(recs),
            "portion_sections": ";".join(sections),
            "portion_site": ";".join(sorted(sites)),
            "corpus_site": crow["site"],
            "portion_type": ";".join(sorted(graded_classes)) if graded_classes else "",
            "corpus_type": corpus_class or "",
            "corroboration_graded": "none (corpus side carries no FC/excavation/museum values)",
            "outcome": outcome,
            "reason": reason,
        })
    return candidates, grades


def annex(rows):
    harp = [r for r in rows if r["section"] == "Harappa (HARP)"]
    years = Counter()
    for r in harp:
        m = re.search(r"H(\d{2})-", r["excavation"] or "")
        years[f"19{m.group(1)}" if m and int(m.group(1)) >= 50 else
              (f"20{m.group(1)}" if m else "no year token")] += 1
    period_fill = sum(1 for r in harp if (r["period"] or "").strip())
    periods = Counter((r["period"] or "").strip() for r in harp if (r["period"] or "").strip())
    bracketed = {k: v for k, v in periods.items() if "[" in k or "]" in k}
    plain = {k: v for k, v in periods.items() if k not in bracketed}
    return {
        "harp_rows": len(harp),
        "dig_year_distribution": dict(sorted(years.items())),
        "dig_year_rule": ("the two-digit year embedded in the excavation "
                          "number's H<YY>- prefix, read as 19YY for YY >= 50 "
                          "and 20YY below; values without the token counted "
                          "as 'no year token'"),
        "registration_no_fill": sum(1 for r in harp if (r["registration_no"] or "").strip()),
        "excavation_fill": sum(1 for r in harp if (r["excavation"] or "").strip()),
        "period_fill": period_fill,
        "period_fill_caveat": ("FLOOR: the scan's text layer loses split "
                               "period tokens, so this fill is a floor, not "
                               "the printed rate (spec section 5)"),
        "period_codes_plain": dict(sorted(plain.items())),
        "period_codes_bracketed": dict(sorted(bracketed.items())),
    }


def main() -> int:
    out = {"spec": "037", "phase": "Phase-402",
           "freeze_digest": "122c2ea4858094d2c6514d05225dfaad1f5266cccffd764949736a78d81aa4db"}
    try:
        s0 = step0()
    except Step0Failure as e:
        out["step0"] = {"closed_at": e.check, "detail": e.detail}
        out["outcome"] = f"CLOSED AT STEP 0 ({e.check})"
        RESULTS_OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(out, indent=1))
        return 1
    out["step0"] = s0["record"]
    out["step0"]["0.4_repo_cleanliness"] = (
        "checked by the caller against the execution tree listing; "
        "result recorded in the outcome record (specs/037 outcome.md section 2)")

    candidates, grades = grade_candidates(s0["rows"], s0["crows"])
    total = len(candidates)
    counts = Counter(g["outcome"] for g in grades)
    reasons = Counter(g["reason"] for g in grades if g["outcome"] == "CONFLICT")
    by_section = {}
    for sec in ("Mohenjo-daro", "Harappa (EH)", "Harappa (HARP)"):
        sub = [g for g in grades if sec in g["portion_sections"].split(";")]
        by_section[sec] = dict(Counter(g["outcome"] for g in sub))
    by_source = {}
    for src in sorted({g["corpus_source"] for g in grades}):
        sub = [g for g in grades if g["corpus_source"] == src]
        by_source[src] = dict(Counter(g["outcome"] for g in sub))
    conflict_share = counts["CONFLICT"] / total if total else 0.0
    out["pilot"] = {
        "candidates": total,
        "candidate_split_by_section": {
            "Mohenjo-daro": sum(1 for g in grades if g["portion_sections"] == "Mohenjo-daro"),
            "Harappa (EH)": sum(1 for g in grades if g["portion_sections"] == "Harappa (EH)"),
            "Harappa (HARP)": sum(1 for g in grades if g["portion_sections"] == "Harappa (HARP)"),
            "spanning_sections": sum(1 for g in grades if ";" in g["portion_sections"]),
        },
        "counts": dict(counts),
        "shares": {k: round(v / total, 4) for k, v in counts.items()} if total else {},
        "conflict_reasons": dict(reasons),
        "by_section": by_section,
        "by_corpus_source": by_source,
        "graded_bases": {"site": total, "type": sum(1 for g in grades if g["portion_type"]),
                         "fc": 0, "excavation": 0, "museum_registration": 0},
        "graded_bases_note": ("corroborating keys ungraded for every candidate: "
                                "corpus_master carries no FC, excavation, or "
                                "museum/registration values (spec section 4.3's "
                                "UNGRADED branch)"),
        "conflict_share": round(conflict_share, 4),
        "halt_threshold": HALT_CAP,
        "halted": conflict_share > HALT_CAP,
    }

    # local grade table (restricted store only)
    grade_path = PORTION_DIR / GRADE_TABLE_NAME
    with grade_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(grades[0].keys()))
        w.writeheader()
        w.writerows(grades)

    # stratum: seeded, seed recorded above before sampling
    rng = random.Random(SEED)
    def draw(cls, k):
        pool = sorted(g["cisi_number"] for g in grades if g["outcome"] == cls)
        return pool if len(pool) <= k else sorted(rng.sample(pool, k))
    stratum = {"VERIFIED": draw("VERIFIED", 30), "CONFLICT": draw("CONFLICT", 15),
               "UNRESOLVED": draw("UNRESOLVED", 15)}
    out["stratum"] = {"seed": SEED,
                      "sizes": {k: len(v) for k, v in stratum.items()},
                      "cause_counts": None}  # filled by the human attribution step

    # spine, behind the halt rule
    if conflict_share > HALT_CAP:
        out["spine"] = {"written": False,
                        "outcome_wording": "PILOT COMPLETE - SPINE HALTED"}
    else:
        spine_rows = [g for g in grades if g["outcome"] == "VERIFIED"]
        spine_path = PORTION_DIR / SPINE_NAME
        with spine_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["cisi_number", "corpus_object_id", "site",
                        "object_type", "corpus_source"])
            for g in spine_rows:
                w.writerow([g["cisi_number"], g["corpus_id"], g["corpus_site"],
                            g["portion_type"], g["corpus_source"]])
        verified_numbers = {g["cisi_number"] for g in spine_rows}
        cov = {}
        for sec in ("Mohenjo-daro", "Harappa (EH)", "Harappa (HARP)"):
            nums = {r["cisi_number"] for r in s0["rows"] if r["section"] == sec}
            cov[sec] = {"portion_numbers": len(nums),
                        "with_verified_join": len(nums & verified_numbers)}
        out["spine"] = {"written": True, "file": SPINE_NAME,
                        "rows": len(spine_rows),
                        "storage": "portion folder of the restricted store only",
                        "sha256": sha256_file(spine_path),
                        "coverage": cov}

    out["annex"] = annex(s0["rows"])
    out["local_products"] = {
        "grade_table": GRADE_TABLE_NAME,
        "build_record": BUILD_RECORD_NAME,
        "stratum_members": stratum,
    }
    RESULTS_OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    build = {"results": out,
             "table_sha256": s0["table_sha"],
             "stratum_members": stratum}
    (PORTION_DIR / BUILD_RECORD_NAME).write_text(
        json.dumps(build, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"step0": "PASS", "candidates": total,
                      "counts": dict(counts), "conflict_share": round(conflict_share, 4),
                      "halted": conflict_share > HALT_CAP}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
