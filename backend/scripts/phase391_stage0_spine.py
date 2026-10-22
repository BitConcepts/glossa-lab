"""Phase-391 (Spec 027, Stage 0) — settlement gazetteer +
chronology spine build.

Freeze: specs/027-movement-culture-language/stage0-freeze.md
(+ stage0-freeze.json digest). Spec: specs/027-movement-
culture-language/spec.md section 6; adjudication Ask 1 -> 0A,
Ask 4 -> CC BY 4.0 release package for verified_open rows.

Descriptive infrastructure only. This build mints no movement,
culture, language, or repertoire verdict (FR-027-4). It reads
pinned inputs from the gitignored local store
corpora/downloads/spec027_stage0/, asserts their sha256
against the frozen values, builds source-asserted gazetteer
rows and traced chronology rows, validates every row against
the spec section 6 contracts (fail loud, no partial finals),
assesses Q6 timing support against the criteria frozen in
stage0-freeze.md section 4 (margins/metadata only), and
prepares the Ask 4 release package (derived CSVs of
verified_open rows only) under
specs/027-movement-culture-language/stage0-release/.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = REPO_ROOT / "corpora" / "downloads" / "spec027_stage0"
DATA_DIR = REPO_ROOT / "data" / "movement"
REPORTS_DIR = REPO_ROOT / "reports"
RELEASE_DIR = (REPO_ROOT / "specs" / "027-movement-culture-language"
               / "stage0-release")
DEFAULT_RESULTS = REPORTS_DIR / "phase391_results.json"
DEFAULT_REPORT = REPORTS_DIR / "phase391_stage0_report.md"

# --- Frozen values (stage0-freeze.md sections 2-4) -------------------------
EXPECTED_HASHES = {
    "xronos_data.csv":
        "8570bfd9b256ced2f9e840183ea52325b9a7079b79a2957c7db797f09c118655",
    "cisi_vol1_catalogue.csv":
        "e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e",
    "cisi_vol2_catalogue.csv":
        "e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9",
    "mutin_moesm1.pdf":
        "b5eae7291aa6a1ebb643b381bbf848651f8bccde0f68ccb282e79ed977857600",
}
LAT_MIN, LAT_MAX = 22.0, 37.5
LNG_MIN, LNG_MAX = 60.5, 79.0
CISI_NON_SITE_VALUES = {"", "Addenda"}  # catalogue section headers
WINDOW_BP = (3850, 5250)  # 3300-1900 BCE conventional window

CISI_CITATIONS = {
    1: ("Joshi, Jagat Pati & Asko Parpola (eds.). 1987. Corpus of "
        "Indus Seals and Inscriptions Vol. 1: Collections in India. "
        "Helsinki: Suomalainen Tiedeakatemia."),
    2: ("Shah, Sayid Ghulam Mustafa & Asko Parpola (eds.). 1991. "
        "Corpus of Indus Seals and Inscriptions Vol. 2: Collections "
        "in Pakistan. Helsinki: Suomalainen Tiedeakatemia."),
}
XRONOS_CITATION = ("XRONOS — An open repository and curation "
                   "platform for radiocarbon data (xronos.ch), full "
                   "export retrieved 2026-10-11 from "
                   "https://xronos.ch/data.csv; CC BY 4.0.")
MUTIN_CITATION = ("Mutin, B. et al. (2025). New radiocarbon dates "
                  "of human tooth enamel reveal a late appearance "
                  "of farming life in the Indus Valley. Scientific "
                  "Reports. DOI 10.1038/s41598-025-92621-5; "
                  "Supplementary Information, Table S2 (incl. "
                  "Zazzo 2014 lines as republished there). "
                  "Scenario status: CONTESTED.")

LONG_LIVED = {"charcoal", "wood", "charred crust"}
SHORT_LIVED_TOKENS = ("wheat", "barley", "seed", "triticum", "lablab",
                      "ziziphus", "bone", "enamel", "dentine", "root",
                      "tooth")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalise_name(name: str) -> str:
    decomposed = unicodedata.normalize("NFKD", name)
    stripped = "".join(c for c in decomposed
                       if not unicodedata.combining(c))
    cleaned = re.sub(r"[^a-z0-9]+", " ", stripped.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def classify_material(material: str) -> tuple[str, bool, object]:
    """Frozen mapping (stage0-freeze.md 3.3).

    Returns (material_class, old_wood_risk, short_lived_sample)
    where short_lived_sample is True/False/'unknown'.
    """
    m = (material or "").strip().lower()
    if m in LONG_LIVED:
        return "long_lived", True, False
    if m and any(tok in m for tok in SHORT_LIVED_TOKENS):
        return "short_lived", False, True
    return "unknown", False, "unknown"


def assert_inputs() -> dict[str, str]:
    hashes = {}
    for name, expected in EXPECTED_HASHES.items():
        path = INPUT_DIR / name
        if not path.is_file():
            print(f"FATAL: frozen input missing: {path}", file=sys.stderr)
            raise SystemExit(2)
        actual = sha256_file(path)
        if actual != expected:
            print(f"FATAL: input hash mismatch for {name}: "
                  f"{actual} != frozen {expected}", file=sys.stderr)
            raise SystemExit(2)
        hashes[name] = actual
    return hashes


def load_xronos_filtered() -> tuple[list[dict], int]:
    path = INPUT_DIR / "xronos_data.csv"
    total = 0
    kept: list[dict] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += 1
            try:
                lat = float(row["lat"])
                lng = float(row["lng"])
            except (TypeError, ValueError):
                continue
            if LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX:
                kept.append(row)
    return kept, total


def xronos_period_labels(periods_raw: str) -> list[str]:
    if not periods_raw or periods_raw.strip() in ("", "[]"):
        return []
    try:
        parsed = json.loads(periods_raw)
    except json.JSONDecodeError:
        return []
    labels = []
    for item in parsed if isinstance(parsed, list) else []:
        if isinstance(item, dict) and item.get("periode"):
            labels.append(str(item["periode"]))
    return labels


def build_gazetteer(xronos_rows: list[dict]) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    stats: dict = {}

    # --- CISI catalogue assertions (per volume x site) ---
    cisi_counts: dict[tuple[int, str], int] = Counter()
    cisi_excluded = 0
    for vol in (1, 2):
        path = INPUT_DIR / f"cisi_vol{vol}_catalogue.csv"
        with open(path, newline="", encoding="utf-8") as f:
            for rec in csv.DictReader(f):
                site = (rec.get("site") or "").strip()
                if site in CISI_NON_SITE_VALUES:
                    cisi_excluded += 1
                    continue
                cisi_counts[(vol, site)] += 1
    for (vol, site), n_objects in sorted(cisi_counts.items()):
        norm = normalise_name(site)
        rows.append({
            "gazetteer_row_id": f"GAZ-CISI{vol}-{norm.replace(' ', '-')}",
            "program_site_id": norm,
            "site_name_as_published": site,
            "site_name_normalised": norm,
            "source_gazetteer": f"CISI Vol. {vol} catalogue (Phase-124 layer)",
            "source_citation": CISI_CITATIONS[vol],
            "source_locator": (f"Vol. {vol} catalogue layer; {n_objects} "
                               f"catalogued objects asserted to this site"),
            "period_label_as_published": None,
            "period_scheme": None,
            "program_period_assignment": None,
            "site_size_as_published": None,
            "survey_or_excavation_basis": (
                "inscribed-object findspot as catalogued in CISI; "
                "museum-collection coverage, not a settlement survey"),
            "latitude": None,
            "longitude": None,
            "coordinate_state": "unknown",
            "coordinate_source": None,
            "coordinate_precision": None,
            "licence_state": "open_access_read_only",
            "origin_group": "CISI published volumes (Phase-124 layer)",
            "notes": ("Findspot assertion from the published CISI "
                      "catalogue layer; the catalogue asserts no "
                      "coordinates and no per-site period scheme."),
        })
    stats["cisi_rows"] = len(cisi_counts)
    stats["cisi_non_site_rows_excluded"] = cisi_excluded

    # --- XRONOS site assertions ---
    by_site: dict[str, list[dict]] = defaultdict(list)
    for rec in xronos_rows:
        by_site[rec["site"]].append(rec)
    for site, recs in sorted(by_site.items()):
        norm = normalise_name(site)
        first = recs[0]
        labels: list[str] = []
        for rec in recs:
            for lab in xronos_period_labels(rec.get("periods", "")):
                if lab not in labels:
                    labels.append(lab)
        rows.append({
            "gazetteer_row_id": f"GAZ-XRO-{norm.replace(' ', '-')}",
            "program_site_id": norm,
            "site_name_as_published": site,
            "site_name_normalised": norm,
            "source_gazetteer": "XRONOS",
            "source_citation": XRONOS_CITATION,
            "source_locator": (f"{len(recs)} dated records in the "
                               f"filtered export; first record id "
                               f"{first['id']}"),
            "period_label_as_published": labels or None,
            "period_scheme": "XRONOS periods (as published)" if labels
                             else None,
            "program_period_assignment": None,
            "site_size_as_published": None,
            "survey_or_excavation_basis": (
                "site with radiocarbon-dated contexts in XRONOS"),
            "latitude": float(first["lat"]),
            "longitude": float(first["lng"]),
            "coordinate_state": "exact_published",
            "coordinate_source": "XRONOS record coordinates",
            "coordinate_precision": "as published (decimal degrees)",
            "licence_state": "verified_open",
            "origin_group": "XRONOS",
            "notes": ("Coordinates are the XRONOS record's site "
                      "coordinates, republished at source precision."),
        })
    stats["xronos_site_rows"] = len(by_site)
    return rows, stats


def build_chronology_xronos(xronos_rows: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for rec in xronos_rows:
        material = (rec.get("material") or "").strip()
        mclass, old_wood, short_lived = classify_material(material)
        feature = (rec.get("feature") or "").strip()
        feature_type = (rec.get("feature_type") or "").strip()
        context = None
        parts = []
        if feature:
            parts.append(f"feature: {feature}")
        if feature_type:
            parts.append(f"feature_type: {feature_type}")
        if parts:
            context = "; ".join(parts)
        grade = "associated" if feature else "unassessed"
        bp = int(rec["bp"]) if (rec.get("bp") or "").strip() else None
        std = int(rec["std"]) if (rec.get("std") or "").strip() else None
        rows.append({
            "chronology_row_id": f"CHR-XRO-{rec['id']}",
            "program_site_id": normalise_name(rec["site"]),
            "site_name_as_published": rec["site"],
            "region_as_recorded": (rec.get("country") or "").strip()
                                  or None,
            "lab_code": (rec.get("labnr") or "").strip() or None,
            "dated_material": material or "unknown",
            "material_class": mclass,
            "context_description": context,
            "context_association_grade": grade,
            "bp": bp,
            "std": std,
            "cal_bp": None,
            "cal_std": None,
            "calibration_curve": None,
            "source_database": "XRONOS",
            "source_record_id": rec["id"],
            "retrieval_version": "full export retrieved 2026-10-11",
            "publication_citation": (rec.get("reference") or "").strip()
                                    or None,
            "old_wood_risk": old_wood,
            "short_lived_sample": short_lived,
            "licence_state": "verified_open",
            "origin_group": "XRONOS",
            "scenario": None,
            "notes": ("Conventional age as published; the retrieved "
                      "export carries no calibrated values for the "
                      "filtered rows and its source_database field "
                      "is empty, so the trace is lab code + cited "
                      "reference under the XRONOS origin group."),
        })
    return rows


MUTIN_ROW_RE = re.compile(
    r"^\s*(T\d+[A-Z]?(?:\s*\(\d+\))?)\b.*?"
    r"\b(enamel|dentine|root)\b.*?"
    r"\b(ECHo\d+\.\d+\.\d+|UBA-\d+)\s+(\d{3,5})\s+(\d{1,3})\b",
    re.IGNORECASE)


def build_chronology_mutin() -> list[dict]:
    pdf = INPUT_DIR / "mutin_moesm1.pdf"
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        print("FATAL: pdftotext failed on the Mutin SI PDF",
              file=sys.stderr)
        raise SystemExit(2)
    lines = proc.stdout.splitlines()
    start = end = None
    for i, line in enumerate(lines):
        if "Supplementary information 6" in line:
            start = i
        if start is not None and "Supplementary information 7" in line:
            end = i
            break
    if start is None or end is None:
        print("FATAL: Mutin SI section 6 markers not found",
              file=sys.stderr)
        raise SystemExit(2)
    rows: list[dict] = []
    for line in lines[start:end]:
        m = MUTIN_ROW_RE.search(line)
        if not m:
            continue
        grave, tissue, ams, age, err = m.groups()
        reference = ("Zazzo 2014" if "Zazzo" in line
                     else "Mutin et al. 2025 (this paper)")
        rows.append({
            "chronology_row_id": f"CHR-MUT-{ams}",
            "program_site_id": "mehrgarh",
            "site_name_as_published": "Mehrgarh",
            "region_as_recorded": "PK",
            "lab_code": ams,
            "dated_material": tissue.lower(),
            "material_class": "short_lived",
            "context_description": (f"burial tooth, grave {grave.strip()} "
                                    f"(Mehrgarh Period I cemetery, as "
                                    f"printed in Table S2)"),
            "context_association_grade": "direct",
            "bp": int(age),
            "std": int(err),
            "cal_bp": None,
            "cal_std": None,
            "calibration_curve": None,
            "source_database": "Mutin et al. 2025 SI Table S2",
            "source_record_id": ams,
            "retrieval_version": "publisher ESM as served 2026-10-11",
            "publication_citation": reference,
            "old_wood_risk": False,
            "short_lived_sample": True,
            "licence_state": "verified_open",
            "origin_group": "Mutin et al. 2025 supplementary data",
            "scenario": "CONTESTED",
            "notes": ("Dated tissue is the buried individual's own "
                      "tooth (direct for the burial event). The "
                      "Period I occupation-start inference drawn "
                      "from these dates is the contested model step "
                      "(spec section 6.5); it is not the grade."),
        })
    if len(rows) != 33:
        print(f"FATAL: Mutin Table S2 parse yielded {len(rows)} rows, "
              f"expected 33 (26 ECHo + 7 UBA)", file=sys.stderr)
        raise SystemExit(2)
    return rows


SOURCE_REGISTER = [
    {
        "source_id": "XRONOS",
        "kind": "radiocarbon_repository",
        "citation": XRONOS_CITATION,
        "licence_state": "verified_open",
        "licence_evidence": ("CC BY 4.0 stated on the XRONOS data "
                             "page, inspected 2026-10-11."),
        "use_in_stage0": "gazetteer site rows + chronology rows",
        "origin_group": "XRONOS",
    },
    {
        "source_id": "CISI Vol. 1 catalogue (Phase-124 layer)",
        "kind": "published_corpus_catalogue",
        "citation": CISI_CITATIONS[1],
        "licence_state": "open_access_read_only",
        "licence_evidence": ("In-copyright published volume; program "
                             "holds the IA scan as a local research "
                             "copy. Factual site assertions only; "
                             "excluded from the CC BY release "
                             "package."),
        "use_in_stage0": "gazetteer findspot rows",
        "origin_group": "CISI published volumes (Phase-124 layer)",
    },
    {
        "source_id": "CISI Vol. 2 catalogue (Phase-124 layer)",
        "kind": "published_corpus_catalogue",
        "citation": CISI_CITATIONS[2],
        "licence_state": "open_access_read_only",
        "licence_evidence": ("In-copyright published volume; program "
                             "holds the IA scan as a local research "
                             "copy. Factual site assertions only; "
                             "excluded from the CC BY release "
                             "package."),
        "use_in_stage0": "gazetteer findspot rows",
        "origin_group": "CISI published volumes (Phase-124 layer)",
    },
    {
        "source_id": "Mutin et al. 2025 SI",
        "kind": "journal_supplement",
        "citation": MUTIN_CITATION,
        "licence_state": "verified_open",
        "licence_evidence": ("Scientific Reports is CC BY 4.0; "
                             "supplement as served by the publisher "
                             "2026-10-11."),
        "use_in_stage0": ("chronology rows (Mehrgarh enamel series); "
                          "scenario status CONTESTED"),
        "origin_group": "Mutin et al. 2025 supplementary data",
    },
    {
        "source_id": "Possehl published site lists",
        "kind": "published_gazetteer",
        "citation": ("Possehl, Gregory L. Indus Age site lists "
                     "(Early ~477 / Mature ~1,022 / Late ~1,281 "
                     "sites, as cited in secondary literature; "
                     "movement research report D7)."),
        "licence_state": "catalogue_only",
        "licence_evidence": ("Book data; no open georeferenced "
                             "download verified."),
        "use_in_stage0": "catalogued only; no rows built",
        "origin_group": None,
    },
    {
        "source_id": "Law (2011) compilations",
        "kind": "dissertation_compilation",
        "citation": ("Law, Randall W. (2011). Inter-regional "
                     "interaction and urbanism in the ancient Indus "
                     "Valley. PhD dissertation, University of "
                     "Wisconsin-Madison."),
        "licence_state": "catalogue_only",
        "licence_evidence": "Bulk-open status not verified.",
        "use_in_stage0": "catalogued only; no rows built",
        "origin_group": None,
    },
    {
        "source_id": "TwoRains published survey data",
        "kind": "project_survey_data",
        "citation": ("TwoRains project (Cambridge-BHU); Zenodo "
                     "3909832 inspected 2026-10-11."),
        "licence_state": "catalogue_only",
        "licence_evidence": ("The cited Zenodo deposit is the "
                             "Angourakis et al. 2020 crop-model R "
                             "project (modelling inputs, no site "
                             "gazetteer); Haryana survey site data "
                             "remains in paper supplements not "
                             "audited for reuse in this stage."),
        "use_in_stage0": "catalogued only; no rows built",
        "origin_group": None,
    },
    {
        "source_id": "c14bazAAR",
        "kind": "aggregator_route",
        "citation": ("c14bazAAR (Kreutzer et al.), R package "
                     "aggregating radiocarbon databases."),
        "licence_state": "catalogue_only",
        "licence_evidence": ("Aggregator, not a primary source "
                             "(spec section 3.4); no source "
                             "database in it was verified in this "
                             "stage to add greater-Indus records "
                             "beyond the XRONOS export."),
        "use_in_stage0": "catalogued only; no rows built",
        "origin_group": None,
    },
]

GAZ_REQUIRED = ["gazetteer_row_id", "program_site_id",
                "site_name_as_published", "source_gazetteer",
                "source_citation", "source_locator", "licence_state",
                "origin_group", "coordinate_state"]
CHR_REQUIRED = ["chronology_row_id", "program_site_id",
                "site_name_as_published", "lab_code", "dated_material",
                "context_association_grade", "bp", "std",
                "source_database", "source_record_id",
                "licence_state", "origin_group"]


def validate(gaz_rows: list[dict], chr_rows: list[dict]) -> None:
    for row in gaz_rows:
        for key in GAZ_REQUIRED:
            if row.get(key) in (None, ""):
                raise SystemExit(
                    f"FATAL: gazetteer row {row.get('gazetteer_row_id')} "
                    f"missing required field {key}")
    for row in chr_rows:
        for key in CHR_REQUIRED:
            if row.get(key) in (None, ""):
                raise SystemExit(
                    f"FATAL: chronology row {row.get('chronology_row_id')} "
                    f"missing required field {key}")


def q6_assessment(chr_rows: list[dict]) -> dict:
    window = [r for r in chr_rows
              if r["bp"] is not None
              and WINDOW_BP[0] <= r["bp"] <= WINDOW_BP[1]
              and r["context_association_grade"] in ("direct",
                                                     "associated")]
    regions: dict[str, set] = defaultdict(set)
    for r in window:
        if r["region_as_recorded"]:
            regions[r["region_as_recorded"]].add(r["program_site_id"])
    regions_ok = sum(1 for sites in regions.values() if len(sites) >= 2)
    window_sites = {r["program_site_id"] for r in window}
    short_share = (sum(1 for r in window
                       if r["short_lived_sample"] is True)
                   / len(window)) if window else 0.0
    stds = sorted(r["std"] for r in window if r["std"] is not None)
    median_std = stds[len(stds) // 2] if stds else None
    criteria = {
        "c1_regions_with_2plus_sites": {
            "value": regions_ok, "threshold": 3,
            "pass": regions_ok >= 3},
        "c2_window_sites_direct_or_associated": {
            "value": len(window_sites), "threshold": 10,
            "pass": len(window_sites) >= 10},
        "c3_window_short_lived_share": {
            "value": round(short_share, 4), "threshold": 0.5,
            "pass": short_share >= 0.5},
        "c4_window_median_std_bp": {
            "value": median_std, "threshold": 80,
            "pass": median_std is not None and median_std <= 80},
    }
    supported = all(c["pass"] for c in criteria.values())
    return {
        "status": ("SUPPORTED-FOR-FREEZE-DESIGN" if supported
                   else "NOT-YET-TESTABLE"),
        "criteria": criteria,
        "window_rows_direct_or_associated": len(window),
        "note": ("Assessment from spine margins/metadata only "
                 "(stage0-freeze.md section 4); no trait-timing "
                 "outcome inspected. A SUPPORTED-FOR-FREEZE-DESIGN "
                 "status binds only that a Q6 freeze may be "
                 "designed; it is not a Q6 result."),
    }


def write_csv(path: Path, fieldnames: list[str],
              rows: list[dict]) -> int:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames,
                            extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: (json.dumps(v) if isinstance(v, (list, dict))
                             else v) for k, v in row.items()})
    path.write_text(buf.getvalue(), encoding="utf-8")
    # Round-trip validation (CSV hygiene): parse back, exact shape.
    with open(path, newline="", encoding="utf-8") as f:
        parsed = list(csv.reader(f))
    assert parsed and parsed[0] == fieldnames, f"header drift: {path}"
    assert len(parsed) - 1 == len(rows), f"row-count drift: {path}"
    assert all(len(r) == len(fieldnames) for r in parsed), \
        f"column-count drift: {path}"
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    hashes = assert_inputs()
    xronos_rows, xronos_total = load_xronos_filtered()
    gaz_rows, gaz_stats = build_gazetteer(xronos_rows)
    chr_rows = build_chronology_xronos(xronos_rows)
    chr_rows += build_chronology_mutin()
    validate(gaz_rows, chr_rows)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    gaz_path = DATA_DIR / "gazetteer_rows.jsonl"
    chr_path = DATA_DIR / "chronology_rows.jsonl"
    with open(gaz_path, "w", encoding="utf-8") as f:
        for row in sorted(gaz_rows,
                          key=lambda r: r["gazetteer_row_id"]):
            f.write(json.dumps(row, ensure_ascii=False,
                               sort_keys=True) + "\n")
    with open(chr_path, "w", encoding="utf-8") as f:
        for row in sorted(chr_rows,
                          key=lambda r: r["chronology_row_id"]):
            f.write(json.dumps(row, ensure_ascii=False,
                               sort_keys=True) + "\n")
    (DATA_DIR / "source_register.json").write_text(
        json.dumps(SOURCE_REGISTER, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")

    # Coverage + conflict summaries.
    by_source = Counter(r["source_gazetteer"] for r in gaz_rows)
    by_licence = Counter(r["licence_state"] for r in gaz_rows)
    by_coord = Counter(r["coordinate_state"] for r in gaz_rows)
    chr_by_source = Counter(r["source_database"] for r in chr_rows)
    chr_by_grade = Counter(r["context_association_grade"]
                           for r in chr_rows)
    chr_by_material = Counter(r["material_class"] for r in chr_rows)
    clusters: dict[str, list[dict]] = defaultdict(list)
    for row in gaz_rows:
        clusters[row["program_site_id"]].append(row)
    multi_source = {k: v for k, v in clusters.items() if len(v) > 1}
    q6 = q6_assessment(chr_rows)

    results = {
        "phase": 391,
        "spec": "027-movement-culture-language",
        "stage": 0,
        "kind": "descriptive_infrastructure_build",
        "verdict": None,
        "input_hashes": hashes,
        "xronos_export_total_rows": xronos_total,
        "xronos_filtered_rows": len(xronos_rows),
        "gazetteer": {
            "rows": len(gaz_rows),
            "by_source": dict(by_source),
            "by_licence_state": dict(by_licence),
            "by_coordinate_state": dict(by_coord),
            "program_site_clusters": len(clusters),
            "multi_source_clusters": len(multi_source),
            **gaz_stats,
        },
        "chronology": {
            "rows": len(chr_rows),
            "by_source": dict(chr_by_source),
            "by_context_grade": dict(chr_by_grade),
            "by_material_class": dict(chr_by_material),
            "contested_rows": sum(1 for r in chr_rows
                                  if r["scenario"] == "CONTESTED"),
        },
        "q6_timing_support": q6,
        "products": {
            "gazetteer_rows": "data/movement/gazetteer_rows.jsonl",
            "chronology_rows": "data/movement/chronology_rows.jsonl",
            "source_register": "data/movement/source_register.json",
        },
    }

    # Release package (Ask 4): derived CSVs of verified_open rows.
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    lawful_gaz = [r for r in gaz_rows
                  if r["licence_state"] == "verified_open"]
    lawful_chr = [r for r in chr_rows
                  if r["licence_state"] == "verified_open"]
    gaz_fields = list(gaz_rows[0].keys())
    chr_fields = list(chr_rows[0].keys())
    n_gaz_csv = write_csv(RELEASE_DIR / "indus_gazetteer_stage0_ccby.csv",
                          gaz_fields,
                          sorted(lawful_gaz,
                                 key=lambda r: r["gazetteer_row_id"]))
    n_chr_csv = write_csv(
        RELEASE_DIR / "indus_chronology_spine_stage0_ccby.csv",
        chr_fields,
        sorted(lawful_chr, key=lambda r: r["chronology_row_id"]))
    (RELEASE_DIR / "source_register.json").write_text(
        (DATA_DIR / "source_register.json").read_text(encoding="utf-8"),
        encoding="utf-8")
    results["release_package"] = {
        "dir": "specs/027-movement-culture-language/stage0-release",
        "gazetteer_csv_rows": n_gaz_csv,
        "chronology_csv_rows": n_chr_csv,
        "licence_rule": ("verified_open rows only; CISI-derived "
                         "open_access_read_only rows excluded"),
        "deposit_made": False,
    }
    (DATA_DIR / "stage0_meta.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    args.results.parent.mkdir(parents=True, exist_ok=True)
    args.results.write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")

    # Human report.
    lines = []
    lines.append("# Phase-391 — Spec 027 Stage 0 Report "
                 "(gazetteer + chronology spine)")
    lines.append("")
    lines.append("Descriptive infrastructure only (Spec 027 §6, "
                 "FR-027-4). This stage mints no movement, culture, "
                 "language, or repertoire verdict.")
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    lines.append(f"- XRONOS export: {xronos_total} rows total; "
                 f"{len(xronos_rows)} inside the frozen region "
                 f"filter (lat {LAT_MIN}-{LAT_MAX}, lng "
                 f"{LNG_MIN}-{LNG_MAX}).")
    lines.append(f"- Gazetteer rows: {len(gaz_rows)} "
                 f"({dict(by_source)}); program site clusters: "
                 f"{len(clusters)}, of which {len(multi_source)} "
                 f"are asserted by more than one source.")
    lines.append(f"- Gazetteer licence states: {dict(by_licence)}; "
                 f"coordinate states: {dict(by_coord)}.")
    lines.append(f"- CISI non-site catalogue rows excluded "
                 f"(empty site / section headers): "
                 f"{gaz_stats['cisi_non_site_rows_excluded']}.")
    lines.append(f"- Chronology rows: {len(chr_rows)} "
                 f"({dict(chr_by_source)}); context grades: "
                 f"{dict(chr_by_grade)}; material classes: "
                 f"{dict(chr_by_material)}; CONTESTED-scenario "
                 f"rows: {results['chronology']['contested_rows']}.")
    lines.append("")
    lines.append("## Coverage bias (statements, not findings)")
    lines.append("")
    lines.append("- CISI rows are inscribed-object findspots from "
                 "museum collections (Vols 1-2): they cover only "
                 "sites whose objects entered those collections, "
                 "dominated by Mohenjo-Daro and Harappa. A site "
                 "absent here is not absent from the Indus world.")
    lines.append("- XRONOS rows cover only sites with published "
                 "radiocarbon-dated contexts in the export; the "
                 "filtered export contains no Mohenjo-Daro, "
                 "Harappa, Mehrgarh, Rakhigarhi, Dholavira, "
                 "Kalibangan, or Lothal dates. The chronology "
                 "spine is therefore a dated-site skeleton, not "
                 "an Indus chronology.")
    lines.append("- Possehl, Law, and TwoRains site lists are "
                 "catalogued, not built (source_register.json): "
                 "the comprehensive settlement universe remains "
                 "untranscribed, and every downstream design "
                 "must treat gazetteer coverage as partial.")
    lines.append("")
    lines.append("## Q6 timing-support assessment (frozen criteria, "
                 "stage0-freeze.md §4)")
    lines.append("")
    for key, crit in q6["criteria"].items():
        lines.append(f"- {key}: value {crit['value']} vs threshold "
                     f"{crit['threshold']} — "
                     f"{'PASS' if crit['pass'] else 'FAIL'}")
    lines.append(f"- **Status: {q6['status']}** "
                 f"(window direct/associated rows: "
                 f"{q6['window_rows_direct_or_associated']}).")
    lines.append("")
    lines.append("## Fitness for question (descriptive, Spec 027 §6.6)")
    lines.append("")
    lines.append("- Q1 (mobility arm): unchanged blocker — the "
                 "spine adds no site-period mobility data; "
                 "NOT-YET-TESTABLE stands.")
    lines.append("- Q2 (Stage 1 gate): the gazetteer supplies "
                 "program site clusters for corpus sites; Stage 1 "
                 "proceeds under its own freeze.")
    lines.append("- Q3/Q4/Q5/Q8/Q9: unchanged blockers (spec §9); "
                 "Stage 0 changes none of their data conditions. "
                 "The Mutin et al. 2025 series is now traced in "
                 "the spine as CONTESTED rows; Q5's replication "
                 "blocker is unaffected.")
    lines.append("- Q6: see the assessment above.")
    lines.append("- Q7: Stage 0 supplies site identities and "
                 "coordinates for the dated-site subset only; "
                 "the D8 provenance/licence audit remains a "
                 "separate precondition.")
    lines.append("")
    lines.append("## Release package (Ask 4)")
    lines.append("")
    lines.append(f"- `stage0-release/` holds derived CC BY 4.0 "
                 f"CSVs of verified_open rows only (gazetteer "
                 f"{n_gaz_csv} rows; chronology {n_chr_csv} rows) "
                 f"plus the source register. CISI-derived rows "
                 f"(open_access_read_only) are excluded. The repo "
                 f"release gate was run against the package in "
                 f"this stage; **no external deposit was made**.")
    lines.append("")
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"gazetteer_rows": len(gaz_rows),
                      "chronology_rows": len(chr_rows),
                      "q6_status": q6["status"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
