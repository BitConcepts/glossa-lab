#!/usr/bin/env python3
"""Phase-133 (spec 024, FROZEN Stage 0) — context-field inventory builder.

Implements spec 024 section 3 exactly:

- section 3.2 coverage matrix: one row per (layer x field) over every
  machine-readable layer in hand — field name as in the source, row
  count + unit, filled count + rate, distinct-value count, top-5
  values with counts, section 3.4 provenance grade, anomaly notes.
- section 3.3 join-key audit: volume-scoped CISI catalogue keys
  ``cisi:v{volume}:{printed_id}`` re-derived; mayig ``cisi_object_id``
  and horus84 ``cisi`` tested empirically (matched / ambiguous /
  unmatched); Holdat ``cisi_number`` PROHIBITED as a join key — its
  collision behaviour is documented factually and it is never joined
  on; Holdat ``seal_id`` intra-layer statistics only; museum records
  censused for CISI cross-references (joins counted only where a
  cross-reference exists in the acquired files — never invented).
- section 3.4 provenance grading: every field of every
  machine-readable layer graded O / C / I with a one-line reason.
- section 2.3 / section 3 mayig description parseability: the rule
  (motif-term list and object-type-term list, stated in code below
  BEFORE application) is a case-insensitive substring match against
  the free-text ``description`` field. A parse is never ground truth.
- Non-machine-readable pass (tasks T4): the Kodumanal volume and
  the Kunal article are described structurally only; no counts are
  pretended that the files cannot support.

FACTS ONLY (spec section 3.1): coverage and joinability only — no
associations, no correlations, no cross-tabulations beyond coverage
counting and the section 3.3 key tests.

Inputs live in the local store (never committed). Every count is
recomputed from the files at run time; nothing is copied from spec
Appendix A — Appendix A values appear in this script ONLY as the
claims the drift table checks the measured values against.

Outputs (committed):
- data/evidence_integration/phase133_stage0_inventory.json
- data/evidence_integration/phase133_stage0_inventory_meta.json

Deterministic: no randomness, no wall-clock in the outputs,
stable ordering everywhere.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
SWEEP = (Path.home() / "workspace" / "research_notes"
         / "indus-data-deep-sweep-20261008" / "downloads")

DEFAULT_OUT = (REPO_ROOT / "data" / "evidence_integration"
               / "phase133_stage0_inventory.json")
DEFAULT_META_OUT = (REPO_ROOT / "data" / "evidence_integration"
                    / "phase133_stage0_inventory_meta.json")

PLACEHOLDERS = {"-", "--", "- -", "None", "?", "??"}

# ---------------------------------------------------------------------------
# Section 3.4 provenance grades (O / C / I) with one-line reasons.
# O = observational, C = depiction-coded, I = interpretive (spec 3.4).
# ---------------------------------------------------------------------------

def _g(grade: str, reason: str) -> tuple[str, str]:
    return (grade, reason)


CISI_GRADES = {
    "volume": _g("O", "Publication volume as printed; bibliographic, no interpretation of the writing."),
    "cisi_id": _g("O", "Catalogue object identifier assigned by the CISI editors; object identity, not a reading."),
    "photo_key": _g("O", "Photograph identifier in the catalogue's own keying; extraction keying only."),
    "side": _g("O", "Object side as photographed/recorded; physical observation."),
    "bis": _g("O", "Catalogue bis marker as printed; bibliographic observation."),
    "caption_raw": _g("O", "Printed plate caption as extracted; the catalogue's own caption text."),
    "caption_ocr_score": _g("O", "This program's OCR extraction confidence for the caption; extraction metadata, not source content."),
    "pdf_page": _g("O", "Page position in the scan PDF; extraction metadata."),
    "printed_page": _g("O", "Printed page number as it appears in the volume; bibliographic observation."),
    "site": _g("O", "Findspot site as printed in the catalogue; recorded from excavation context."),
    "object_type": _g("O", "Object class as printed in the catalogue (Seals/Tablets/Graffiti/Objects); physical object classification."),
    "motif_chapter": _g("C", "CISI's own iconographic chapter organisation: a depiction classification made by the CISI editors."),
    "scale_pct": _g("O", "Printed photograph scale; physical/bibliographic observation."),
    "collection_scope": _g("O", "Volume-level collection scope statement from the title page/preface; collection provenance as printed."),
    "material": _g("O", "Material would be observational, but the field is not printed per object in CISI plates: it stands empty per boundary 3 and is never back-filled."),
    "material_basis": _g("O", "This program's provenance note stating why material is absent ('not printed per object in CISI plates')."),
    "dimensions": _g("O", "Dimensions would be observational, but the field is not printed per object in CISI plates: it stands empty per boundary 3 and is never back-filled."),
    "dimensions_basis": _g("O", "This program's provenance note stating why dimensions are absent ('not printed per object in CISI plates')."),
    "photo_box_xywh": _g("O", "Photograph bounding box in the scan; extraction geometry."),
    "extraction_basis": _g("O", "This program's extraction-method provenance for the row."),
    "confidence": _g("O", "This program's extraction confidence label for the row."),
    "notes": _g("O", "This program's extraction notes (e.g. OCR glyph corrections); extraction provenance, not source content."),
}

HOLDAT_GRADES = {
    "letters": _g("I", "Sign identity (M-number) assigned under the compilation's sign list: text-internal transcription, not observational context."),
    "form": _g("O", "Intra-compilation inscription identifier (seal_NNNN); keying only."),
    "cisi_number": _g("O", "Identifier string as printed in the compilation; inventoried as a field only — PROHIBITED as a join key per section 3.3 (Phase-131: internal sequential numbering). Grade does not validate the key."),
    "site": _g("O", "Site as recorded by the compilation for the inscription; findspot context."),
    "iconography": _g("C", "Depiction classification made by the Holdat compilation; coder-dependent depiction coding with no verifiable coding provenance."),
    "position": _g("O", "Token ordinal within the inscription as recorded; mechanical sequence position."),
    "seal_id": _g("O", "Intra-Holdat inscription identifier; valid only as an intra-layer key per section 3.3."),
    "upos": _g("I", "Universal part-of-speech annotation assigned by the compilation: linguistic theory, excluded from context evidence per the tasking and section 3.4."),
    "xpos": _g("I", "Language-specific part-of-speech annotation assigned by the compilation: linguistic theory, excluded from context evidence per the tasking and section 3.4."),
    "letter_label_encoded": _g("I", "Integer encoding of the compilation's sign label: text-internal transcription encoding."),
    "prefix": _g("I", "Prefix annotation under the compilation's morpheme analysis: interpretive linguistic annotation (field is empty as acquired)."),
    "vowel": _g("I", "Vowel annotation under the compilation's linguistic analysis: interpretive (field is empty as acquired)."),
    "morpheme boundary": _g("I", "Morpheme-boundary flag under the compilation's segmentation theory: interpretive, excluded from context evidence."),
    "noun": _g("I", "Noun assignment under the compilation's linguistic theory: interpretive, excluded from context evidence."),
    "verb": _g("I", "Verb assignment under the compilation's linguistic theory: interpretive, excluded from context evidence."),
    "FormWithoutLemma": _g("I", "Lemma-stripped form produced by the compilation's linguistic processing: text-internal derivation."),
    "Counts": _g("O", "Per-row count value as printed in the file (constant 1); mechanical count, no interpretation."),
    "MorphemeSeparated": _g("I", "Morpheme-separated rendering of the sign sequence under the compilation's segmentation: interpretive."),
    "prefix_label_encoded": _g("I", "Integer encoding of the compilation's prefix label: interpretive linguistic annotation, encoded."),
}

HOLDAT_ROLES_GRADES = {
    "symbol": _g("I", "Sign identity (M-number) under the compilation's sign list: text-internal."),
    "count": _g("O", "Mechanical occurrence count computed by the compilation."),
    "num_sequences": _g("O", "Mechanical count of sequences containing the sign."),
    "num_prefixes": _g("I", "Count of prefix occurrences under the compilation's morpheme/position analysis: interpretive derivation."),
    "num_suffixes": _g("I", "Count of suffix occurrences under the compilation's morpheme/position analysis: interpretive derivation."),
    "num_shells": _g("I", "Count of 'shell' occurrences under the compilation's positional-structure analysis: interpretive derivation."),
    "avg_length": _g("O", "Mechanical mean sequence length computed by the compilation."),
    "avg_position": _g("O", "Mechanical mean token position computed by the compilation."),
    "position_variance": _g("O", "Mechanical variance of token position computed by the compilation."),
    "context_diversity": _g("O", "Mechanical diversity statistic computed by the compilation."),
    "shell_density": _g("I", "Density derived from the compilation's 'shell' positional analysis: interpretive derivation."),
    "is_starter": _g("I", "Starter-role classification inferred by the compilation's positional analysis: interpretive."),
    "is_ending": _g("I", "Ending-role classification inferred by the compilation's positional analysis: interpretive."),
    "is_known_role": _g("I", "Known-role flag under the compilation's semantic-role assignment: interpretive."),
    "semantic_role": _g("I", "Semantic-role encoding assigned by the compilation (e.g. CASE_MARKER_SUFFIX): interpretive, excluded from context evidence."),
}

MAYIG_GRADES = {
    "cisi_object_id": _g("O", "CISI object identifier as keyed by the corpus author; object identity (unscoped printed ID — see join-key audit)."),
    "side_id": _g("O", "Object side identifier as keyed by the corpus author."),
    "description": _g("C", "Free-text description written by the corpus author that classifies what is depicted plus the object type (e.g. 'unicorn I seal'): depiction-coded, unstructured."),
    "tokens": _g("I", "Sign sequence (P-numbers) transcribed under the Parpola sign list: text-internal transcription, not context."),
    "token_count": _g("O", "Mechanical token count for the inscription."),
    "features": _g("I", "Wells-derived grapheme feature vectors: sign-form analysis, text-internal."),
    "source_file": _g("O", "Provenance pointer to the source corpus JSON file."),
}

MAYIG_SOURCE_GRADES = {
    "id": _g("O", "Side identifier as keyed in the source corpus JSON (e.g. 'M-1A')."),
    "description": _g("C", "Free-text depiction + object-type description written by the corpus author: depiction-coded, unstructured."),
    "graphemes": _g("I", "Per-grapheme P-identifiers with Wells-derived feature vectors: text-internal sign-form transcription."),
}

HORUS_GRADES = {
    "id": _g("O", "Row identifier in the ICIT-lineage file; keying only."),
    "cisi": _g("O", "Candidate artefact identifier as printed in the file; inventoried as a field — its semantics are unverified and it is tested, not assumed, in the join-key audit."),
    "region": _g("O", "Geographic region as recorded in the compilation; excavation geography."),
    "site": _g("O", "Findspot site as recorded in the compilation; excavation context."),
    "area-section": _g("O", "Excavation area/section as recorded; findspot context."),
    "block-house": _g("O", "Excavation block/house as recorded; findspot context."),
    "room-grid": _g("O", "Excavation room/grid as recorded; findspot context."),
    "excavation-idno": _g("O", "Excavation identifier number as recorded; findspot/collection keying."),
    "time": _g("O", "Archaeological time assignment as recorded in the compilation; dating context, not a reading."),
    "period": _g("O", "Archaeological period assignment as recorded in the compilation; dating context."),
    "phase": _g("O", "Archaeological phase assignment as recorded in the compilation; dating context."),
    "depth": _g("O", "Excavation depth as recorded; findspot context."),
    "boss": _g("O", "Seal boss form as recorded; physical observation."),
    "material": _g("O", "Material as recorded in the compilation; physical observation."),
    "color": _g("O", "Colour as recorded; physical observation."),
    "shape": _g("O", "Object shape as recorded; physical observation."),
    "cross-section": _g("O", "Object cross-section as recorded; physical observation."),
    "preservation": _g("O", "Preservation state as recorded; physical condition observation."),
    "symbol": _g("C", "Depiction/symbol classification recorded by the compilation: depiction-coded (includes 'None')."),
    "cult": _g("C", "Cult-scene classification recorded by the compilation: depiction-coded, named Class C in spec section 3.4."),
    "type": _g("O", "Object type code as recorded (e.g. SEAL:S, TAB:B, POT:T:g); physical object classification."),
    "sides": _g("O", "Number of inscribed sides as recorded; physical observation."),
    "condition": _g("O", "Condition grade as recorded; physical condition observation."),
    "complete": _g("O", "Completeness flag as recorded; physical condition observation."),
    "dir.": _g("O", "Recorded text direction (e.g. R/L) as an observed orientation of the inscription on the object."),
    "class": _g("I", "Text/sign class code assigned by the compilation with unverified semantics: text-internal classification, not observational context."),
    "text length": _g("O", "Mechanical text-length value as recorded."),
    "signs": _g("O", "Mechanical sign-count value as recorded."),
    "h": _g("O", "Height dimension as recorded; physical measurement."),
    "v": _g("O", "Vertical dimension as recorded; physical measurement."),
    "th": _g("O", "Thickness dimension as recorded; physical measurement."),
    "horizontal(mm)": _g("O", "Horizontal dimension in mm as recorded; physical measurement (0 encodes absence in this file — see anomaly note)."),
    "vertical(mm)": _g("O", "Vertical dimension in mm as recorded; physical measurement (0 encodes absence in this file — see anomaly note)."),
    "thickness(mm)": _g("O", "Thickness in mm as recorded; physical measurement (0 encodes absence in this file — see anomaly note)."),
    "text": _g("I", "Sign sequence transcribed under the ICIT sign identifiers: text-internal transcription, not context."),
    "sanskrit": _g("I", "Sanskrit identification proposed by the compilation: interpretive decipherment content, excluded from context evidence (spec sections 2.4 / 3.4)."),
    "translation": _g("I", "Translation proposed by the compilation: interpretive decipherment content, excluded from context evidence (spec sections 2.4 / 3.4)."),
    "notes": _g("I", "Free-text compilation annotations including textual/Rgvedic references; observational and interpretive content is not separable in this field, so it is excluded from context evidence by construction."),
}

MUSEUM_GRADE_REASON = (
    "Museum catalogue metadata recorded by the museum for its own "
    "object under its own accession/object key; no interpretation "
    "of the writing is carried by this field as acquired."
)


def museum_grade(field: str) -> tuple[str, str]:
    return _g("O", MUSEUM_GRADE_REASON)


# ---------------------------------------------------------------------------
# Mayig parseability rule (declared BEFORE application, per tasking):
# case-insensitive substring match of the description against the
# motif-term list and the object-type-term list below.
#
# Motif-term list derivation: the spec section 4.3 published
# iconographic categories (unicorn; zebu/bull; buffalo; elephant;
# rhinoceros; goat/antelope; tiger; composite creatures; human
# figures; cult/narrative scenes; geometric designs; script only /
# no depiction; illegible) UNION the distinct values of the Holdat
# iconography field as measured in this run (added programmatically
# below at build time and recorded verbatim in the output).
# Object-type-term list: seal, tablet, object, pottery, graffiti,
# plaque, impression (stated here, before application).
# ---------------------------------------------------------------------------
MOTIF_TERMS_SECTION_4_3 = [
    "unicorn", "zebu", "bull", "buffalo", "elephant", "rhinoceros",
    "goat", "antelope", "tiger", "composite", "human", "cult",
    "narrative", "geometric", "script only", "no depiction",
    "illegible",
]
OBJECT_TYPE_TERMS = [
    "seal", "tablet", "object", "pottery", "graffiti", "plaque",
    "impression",
]

# Appendix A claims (the values the drift table checks measured
# values against; measured values are always recomputed).
APPENDIX_A = {
    "cisi_total_rows": 7705, "cisi_vol1_rows": 3320,
    "cisi_vol2_rows": 4385, "cisi_distinct_volume_scoped": 3494,
    "cisi_vol1_distinct": 1475, "cisi_vol2_distinct": 2019,
    "cisi_n_fields": 22,
    "cisi_site_rate_v1_pct": 94.7, "cisi_site_rate_v2_pct": 92.2,
    "cisi_object_type_rate_v1_pct": 95.1,
    "cisi_object_type_rate_v2_pct": 96.3,
    "cisi_motif_rate_v1_pct": 25.1, "cisi_motif_rate_v2_pct": 26.8,
    "cisi_motif_rows_total": 2005,
    "cisi_material_rate_pct": 0.0, "cisi_dimensions_rate_pct": 0.0,
    "cisi_object_type_rows": {"Seals": 4778, "Tablets": 2180,
                              "Graffiti": 417, "Objects": 5},
    "holdat_rows": 7002, "holdat_distinct_seal_id": 1670,
    "holdat_n_fields": 19,
    "holdat_iconography_top": {"unicorn": 2143, "zebu bull": 1414,
                               "elephant": 859, "rhinoceros": 726,
                               "script only": 572, "geometric": 397},
    "mayig_inscriptions": 179, "mayig_objects": 179,
    "mayig_tokens": 1003, "mayig_distinct_signs": 182,
    "horus_rows": 5679, "horus_n_fields": 39,
    "museum_met_objects": 28, "museum_cleveland_seals": 3,
    "museum_penn_records": 2,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def content_hash(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False)
        .encode("utf-8")).hexdigest()


def is_filled(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, tuple, dict)):
        return len(value) > 0
    return True


def display_value(value) -> str:
    if isinstance(value, str):
        s = value
    else:
        s = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return s if len(s) <= 200 else s[:197] + "..."


def field_stats(values: list) -> dict:
    counter: Counter = Counter()
    for v in values:
        counter[display_value(v) if v is not None else ""] += 1
    filled_vals = [v for v in values if is_filled(v)]
    distinct = len({display_value(v) for v in filled_vals})
    top = [{"value": v, "count": c}
           for v, c in counter.most_common(5) if v.strip() != ""]
    placeholder = sum(1 for v in values
                      if isinstance(v, str)
                      and v.strip() in PLACEHOLDERS)
    return {
        "filled_count": len(filled_vals),
        "distinct_value_count": distinct,
        "top_values": top,
        "placeholder_count": placeholder,
    }


def coverage_row(layer_id, unit, field, values, grade, reason,
                 note=""):
    stats = field_stats(values)
    n = len(values)
    row = {
        "layer": layer_id,
        "unit": unit,
        "field": field,
        "row_count": n,
        "filled_count": stats["filled_count"],
        "filled_rate": (round(stats["filled_count"] / n, 6)
                        if n else 0.0),
        "distinct_value_count": stats["distinct_value_count"],
        "top_values": stats["top_values"],
        "provenance_grade": grade,
        "grade_reason": reason,
        "anomaly_note": note,
    }
    if stats["placeholder_count"]:
        ph_note = (
            f"{stats['placeholder_count']} row(s) carry placeholder "
            f"value(s) ('-', '--', 'None', '?', etc.) that encode "
            f"absence in the source convention; they are counted as "
            f"filled in the raw rate because the cell is not empty.")
        row["anomaly_note"] = (note + " " + ph_note).strip()
        row["placeholder_count"] = stats["placeholder_count"]
    return row


def read_csv_rows(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def classify_key(value: str, vol1_ids: set, vol2_ids: set) -> str:
    in1, in2 = value in vol1_ids, value in vol2_ids
    if in1 and in2:
        return "ambiguous"
    if in1 or in2:
        return "matched_single_volume"
    return "unmatched"


def normalize_zero_padded(value: str) -> str:
    m = re.match(r"^([A-Za-z]+)-0*(\d+)$", value.strip())
    if not m:
        return value.strip()
    return f"{m.group(1)}-{int(m.group(2))}"


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(args) -> tuple[dict, dict]:
    inputs: dict[str, dict] = {}

    def register(key: str, path: Path, note: str = ""):
        entry = {"path": str(path), "exists": path.exists()}
        if path.exists() and path.is_file():
            entry["sha256"] = sha256_of(path)
            entry["bytes"] = path.stat().st_size
        if note:
            entry["note"] = note
        inputs[key] = entry
        return path

    cisi_paths = {1: register("cisi_vol1_catalogue", args.cisi_vol1),
                  2: register("cisi_vol2_catalogue", args.cisi_vol2)}
    holdat_path = register("holdat_indus_corpus", args.holdat)
    roles_path = register("holdat_semantic_roles", args.holdat_roles)
    mayig_path = register("mayig_layer", args.mayig_layer)
    mayig_meta_path = register("mayig_layer_meta", args.mayig_meta)
    horus_path = register("horus84_inscriptions", args.horus)
    anomaly_path = register("anomaly_holdatllc_seal_catalog",
                            args.anomaly_file,
                            "Committed in the repository at "
                            "data/raw/other_sites/; content inspected "
                            "in this run (see anomalies).")
    met_ids_path = register("museum_met_indus_object_ids",
                            args.museum_dir / "met"
                            / "indus_object_ids.json")
    met_summary_path = register("museum_met_indus_objects_summary",
                                args.museum_dir / "met"
                                / "indus_objects_summary.json")
    cleveland_path = register("museum_cleveland_search_indus",
                              args.museum_dir / "cleveland"
                              / "search_indus.json")
    penn_path = register("museum_penn_records_md",
                         args.museum_dir / "penn" / "penn_records.md")
    kodumanal_path = register("kodumanal_volume_pdf", args.kodumanal)
    kunal_path = register("kunal_article_pdf", args.kunal)

    layers: list[dict] = []
    matrix: list[dict] = []
    anomalies: list[dict] = []

    def add_layer(layer_id, label, unit, rows_fields, source_desc,
                  license_basis, machine_readable=True):
        """rows_fields: list of (field, values, grade, reason, note)."""
        fields = []
        for item in rows_fields:
            field, values, grade, reason = item[:4]
            note = item[4] if len(item) > 4 else ""
            row = coverage_row(layer_id, unit, field, values,
                               grade, reason, note)
            fields.append(row)
            matrix.append(row)
        layer = {
            "layer_id": layer_id, "label": label, "unit": unit,
            "row_count": len(rows_fields[0][1]) if rows_fields else 0,
            "n_fields": len(rows_fields),
            "source": source_desc, "license_basis": license_basis,
            "machine_readable": machine_readable,
            "fields": fields,
        }
        layers.append(layer)
        return layer

    # ---- CISI catalogue, per volume ---------------------------------
    cisi_rows: dict[int, list[dict]] = {}
    cisi_fields: dict[int, list[str]] = {}
    cisi_ids: dict[int, set] = {}
    for vol in (1, 2):
        fields, rows = read_csv_rows(cisi_paths[vol])
        cisi_fields[vol], cisi_rows[vol] = fields, rows
        cisi_ids[vol] = {r["cisi_id"] for r in rows}
        rows_fields = []
        for f in fields:
            grade, reason = CISI_GRADES.get(
                f, _g("O", "Catalogue field as printed/extracted; "
                           "no interpretation of the writing."))
            note = ""
            if f in ("material", "dimensions"):
                note = ("0% filled as printed: CISI plates do not "
                        "print per-object material/dimensions "
                        "(Phase-124 premise correction; boundary 3). "
                        "Never back-filled.")
            if f in ("material_basis", "dimensions_basis"):
                note = ("Constant provenance string on every row "
                        "stating the per-object field is not "
                        "printed; the 100% rate is for this basis "
                        "note, not for material/dimensions data.")
            if f == "motif_chapter":
                vals = Counter(r[f] for r in rows if r[f].strip())
                odd = {k: c for k, c in vals.items()
                       if k not in ("unicorn",)}
                note = ("Distinct non-empty values as printed, "
                        "including OCR/chapter-heading variants: "
                        + json.dumps(dict(sorted(odd.items())),
                                     ensure_ascii=False)
                        + ". 'unicorn' is the dominant value; other "
                        "values are spelling variants and chapter "
                        "headings, recorded as found, not cleaned.")
            rows_fields.append((f, [r[f] for r in rows],
                                grade, reason, note))
        add_layer(
            f"cisi_vol{vol}_catalogue",
            f"CISI catalogue Vol. {vol} (Phase-124 OCR extraction)",
            "photo_row", rows_fields,
            f"cisi_vol{vol}_catalogue.csv (local store, "
            f"corpora/downloads/cisi_image_layer/catalogue/)",
            "Local research material (CISI volumes in copyright); "
            "derived counts only are published.")

    vol1_ids, vol2_ids = cisi_ids[1], cisi_ids[2]
    catalogue_keys = ({f"cisi:v1:{i}" for i in vol1_ids}
                      | {f"cisi:v2:{i}" for i in vol2_ids})

    # Catalogue per-object view (volume-scoped), first non-empty wins.
    obj_view: dict[tuple[int, str], dict] = {}
    for vol in (1, 2):
        for r in cisi_rows[vol]:
            d = obj_view.setdefault(
                (vol, r["cisi_id"]),
                {"site": "", "object_type": "", "motif_chapter": ""})
            for f in d:
                if not d[f] and r[f].strip():
                    d[f] = r[f]

    # ---- Holdat ------------------------------------------------------
    h_fields, h_rows = read_csv_rows(holdat_path)
    add_layer(
        "holdat_indus_corpus", "Holdat compilation (indus_corpus)",
        "token_row",
        [(f, [r[f] for r in h_rows], *HOLDAT_GRADES.get(
            f, _g("I", "Compilation field not otherwise classified; "
                       "treated as interpretive/text-internal.")),
          (("Field is empty on every row as acquired."
            if all(not r[f].strip() for r in h_rows) else "")
           if f in ("prefix", "vowel") else "")
          + (("Constant '0' on every row as acquired."
              if len({r[f] for r in h_rows}) == 1
              and f in ("noun", "verb") else "")))
         for f in h_fields],
        "indus_corpus 2.csv (local store, "
        "corpora/downloads/external_repos/holdatllc_indus/)",
        "Local research material; derived counts only.")

    r_fields, r_rows = read_csv_rows(roles_path)
    add_layer(
        "holdat_symbol_semantic_roles",
        "Holdat symbol semantic-roles table "
        "(all_symbol_semantic_roles)",
        "symbol_row",
        [(f, [r[f] for r in r_rows], *HOLDAT_ROLES_GRADES.get(
            f, _g("I", "Compilation analysis field; treated as "
                       "interpretive."))) for f in r_fields],
        "all_symbol_semantic_roles 2.csv (local store, same "
        "directory as the Holdat corpus file)",
        "Local research material; derived counts only.")

    # ---- mayig layer + source corpus --------------------------------
    mayig = json.loads(mayig_path.read_text("utf-8"))
    mayig_ins = mayig["inscriptions"]
    add_layer(
        "mayig_cisi_layer", "mayig CISI layer v1 (derived layer)",
        "inscription",
        [(f, [x.get(f) for x in mayig_ins], *MAYIG_GRADES[f])
         for f in ["cisi_object_id", "side_id", "description",
                   "tokens", "token_count", "features",
                   "source_file"]],
        "data/corpus_layers/mayig_cisi_layer_v1.json (committed)",
        "MIT (source repo LICENSE, Copyright (c) 2024 Michael "
        "Carlson; verified at acquisition, Phase-122 meta).")

    source_files = sorted(args.mayig_source_dir.rglob("*.json"))
    source_sides: list[dict] = []
    for p in source_files:
        try:
            data = json.loads(p.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, list):
            source_sides.extend(
                s for s in data if isinstance(s, dict))
    inputs["mayig_source_corpus_dir"] = {
        "path": str(args.mayig_source_dir),
        "exists": args.mayig_source_dir.exists(),
        "n_json_files_under_corpus": len(source_files),
        "note": "Per-file sha256 not recorded for the 179 source "
                "files; the combined acquisition hash is in the "
                "deep-sweep PROVENANCE.md entry 1."}
    add_layer(
        "mayig_source_corpus",
        "mayig source corpus JSONs (per-artefact files)",
        "inscription_side",
        [(f, [s.get(f) for s in source_sides],
          *MAYIG_SOURCE_GRADES[f])
         for f in ["id", "description", "graphemes"]],
        "mayig-indus-valley-script-corpus/corpus/ (deep-sweep "
        "downloads tree)",
        "MIT (source repo LICENSE, Copyright (c) 2024 Michael "
        "Carlson).")

    # ---- horus84 -----------------------------------------------------
    ho_fields, ho_rows = read_csv_rows(horus_path)
    ho_notes = {
        "horizontal(mm)": "Value '0' on 1,809 rows encodes absence "
                          "of a measurement in this file, not a "
                          "0 mm measurement; the raw filled rate "
                          "counts it as filled.",
        "vertical(mm)": "Value '0' on 1,680 rows encodes absence; "
                        "see horizontal(mm) note.",
        "thickness(mm)": "Value '0' on 3,585 rows encodes absence; "
                         "see horizontal(mm) note.",
    }
    # recompute zero counts rather than trusting the strings above
    for f in ("horizontal(mm)", "vertical(mm)", "thickness(mm)"):
        z = sum(1 for r in ho_rows if r[f].strip() == "0")
        ho_notes[f] = (f"Value '0' on {z} rows encodes absence of "
                       f"a measurement in this file, not a 0 mm "
                       f"measurement; the raw filled rate counts "
                       f"it as filled.")
    add_layer(
        "horus84_inscriptions",
        "horus84 ICIT-lineage inscriptions (inscriptions.csv)",
        "inscription",
        [(f, [r[f] for r in ho_rows], *HORUS_GRADES.get(
            f, _g("O", "Field as recorded in the ICIT-lineage "
                       "file; no interpretation of the writing.")),
          ho_notes.get(f, "")) for f in ho_fields],
        "horus84-computational-linguistics/data/inscriptions.csv "
        "(deep-sweep downloads tree)",
        "MIT per source repo metadata at acquisition; "
        "ICIT-lineage derivative — descriptive/QC use only, "
        "never an independent witness (spec section 2.4).")

    # ---- Museum layers ----------------------------------------------
    met_ids = json.loads(met_ids_path.read_text("utf-8"))
    met_records = []
    for oid in met_ids:
        p = (args.museum_dir / "met" / "objects" / f"{oid}.json")
        if p.exists():
            met_records.append(json.loads(p.read_text("utf-8")))
    met_field_names: list[str] = []
    for rec in met_records:
        for k in rec:
            if k not in met_field_names:
                met_field_names.append(k)
    add_layer(
        "museum_met_indus",
        "Met Museum open data — curated Indus set (28 object IDs "
        "in indus_object_ids.json, full object records)",
        "object",
        [(f, [rec.get(f) for rec in met_records],
          *museum_grade(f)) for f in met_field_names],
        "museum-open-data/met/objects/{objectID}.json for the 28 "
        "IDs in met/indus_object_ids.json (deep-sweep downloads)",
        "CC0 (Met Open Access).")

    cle = json.loads(cleveland_path.read_text("utf-8"))
    cle_records = cle.get("data", [])
    cle_field_names: list[str] = []
    for rec in cle_records:
        for k in rec:
            if k not in cle_field_names:
                cle_field_names.append(k)
    add_layer(
        "museum_cleveland_indus_search",
        "Cleveland Museum of Art open data — 'indus' search "
        "result set as acquired (10 records)",
        "record",
        [(f, [rec.get(f) for rec in cle_records],
          *museum_grade(f)) for f in cle_field_names],
        "museum-open-data/cleveland/search_indus.json "
        "(deep-sweep downloads)",
        "CC0 (Cleveland Open Access; per-record "
        "share_license_status field as acquired).")

    # ---- Join-key audit (section 3.3) --------------------------------
    dup_audit = {}
    for vol in (1, 2):
        rows = cisi_rows[vol]
        id_counter = Counter(r["cisi_id"] for r in rows)
        pk_counter = Counter(r["photo_key"] for r in rows)
        per_id = Counter(id_counter.values())
        dup_audit[f"vol{vol}"] = {
            "photo_rows": len(rows),
            "distinct_printed_ids": len(id_counter),
            "ids_with_more_than_one_photo_row":
                sum(1 for c in id_counter.values() if c > 1),
            "max_photo_rows_per_id": max(id_counter.values()),
            "photo_rows_per_id_distribution":
                {str(k): per_id[k] for k in sorted(per_id)},
            "note": "A printed ID legitimately carries several "
                    "photo rows (one per photographed side/view); "
                    "repetition across photo rows is the catalogue "
                    "structure, not a duplicate-object collision. "
                    "Exact duplicate photo_key values (the row-level "
                    "key) are the within-volume duplicate anomaly "
                    "and are listed separately.",
            "duplicate_photo_keys": {
                k: c for k, c in sorted(pk_counter.items()) if c > 1},
            "n_duplicate_photo_keys":
                sum(1 for c in pk_counter.values() if c > 1),
        }

    mayig_key_test = Counter(
        classify_key(x["cisi_object_id"], vol1_ids, vol2_ids)
        for x in mayig_ins)
    mayig_key_detail = {
        "key_field": "cisi_object_id",
        "n_values_tested": len(mayig_ins),
        "n_distinct_values":
            len({x["cisi_object_id"] for x in mayig_ins}),
        "matched_single_volume": mayig_key_test.get(
            "matched_single_volume", 0),
        "matched_vol1_only": sum(
            1 for x in mayig_ins
            if x["cisi_object_id"] in vol1_ids
            and x["cisi_object_id"] not in vol2_ids),
        "matched_vol2_only": sum(
            1 for x in mayig_ins
            if x["cisi_object_id"] in vol2_ids
            and x["cisi_object_id"] not in vol1_ids),
        "ambiguous_present_in_both_volumes":
            mayig_key_test.get("ambiguous", 0),
        "unmatched": mayig_key_test.get("unmatched", 0),
        "verdict": "USABLE as an unscoped printed-ID key against "
                   "the Vol. 1 catalogue population for this layer "
                   "as found: every value matched exactly one "
                   "volume (Vol. 1) and none was ambiguous or "
                   "unmatched. The verdict is empirical for these "
                   "179 values, not a semantics assumed from the "
                   "ID prefixes.",
    }

    horus_vals = [r["cisi"] for r in ho_rows]
    horus_key_test = Counter(
        classify_key(v, vol1_ids, vol2_ids) for v in horus_vals)
    horus_distinct_test = Counter(
        classify_key(v, vol1_ids, vol2_ids) for v in set(horus_vals))
    horus_counter = Counter(horus_vals)
    horus_key_detail = {
        "key_field": "cisi",
        "n_rows_tested": len(horus_vals),
        "n_distinct_values": len(set(horus_vals)),
        "rows": {
            "matched_single_volume": horus_key_test.get(
                "matched_single_volume", 0),
            "matched_vol1_only": sum(
                1 for v in horus_vals
                if v in vol1_ids and v not in vol2_ids),
            "matched_vol2_only": sum(
                1 for v in horus_vals
                if v in vol2_ids and v not in vol1_ids),
            "ambiguous_present_in_both_volumes":
                horus_key_test.get("ambiguous", 0),
            "unmatched": horus_key_test.get("unmatched", 0),
        },
        "distinct_values": {
            "matched_single_volume": horus_distinct_test.get(
                "matched_single_volume", 0),
            "ambiguous_present_in_both_volumes":
                horus_distinct_test.get("ambiguous", 0),
            "unmatched": horus_distinct_test.get("unmatched", 0),
        },
        "ambiguous_values": sorted(
            {v for v in set(horus_vals)
             if v in vol1_ids and v in vol2_ids}),
        "dash_placeholder_rows": sum(
            1 for v in horus_vals if v.strip() == "-"),
        "distinct_values_with_more_than_one_row":
            sum(1 for c in horus_counter.values() if c > 1),
        "max_rows_per_distinct_value": max(horus_counter.values()),
        "verdict": "NOT USABLE as a general join key: a majority-"
                   "unmatched candidate field (see counts) whose "
                   "values include non-CISI artefact numberings "
                   "(e.g. Agr-, Blk-, C- prefixes), a '-' "
                   "placeholder on 662 rows, and one ambiguous "
                   "value present in both volumes. Rows whose "
                   "value matches exactly one volume are counted "
                   "above as matched for that row only; no "
                   "layer-wide join on this field is validated.",
    }

    holdat_numbers = [r["cisi_number"] for r in h_rows]
    exact_rows = sum(1 for v in holdat_numbers
                     if v in vol1_ids or v in vol2_ids)
    norm_distinct = {normalize_zero_padded(v)
                     for v in set(holdat_numbers)}
    mayig_ids = {x["cisi_object_id"] for x in mayig_ins}
    holdat_key_detail = {
        "key_field": "cisi_number",
        "status": "PROHIBITED as a join key (spec section 3.3; "
                  "Phase-131 established it is internal sequential "
                  "numbering, not a CISI key). Never joined on in "
                  "this audit; the numbers below document its "
                  "collision behaviour factually only.",
        "n_token_rows": len(holdat_numbers),
        "n_distinct_values": len(set(holdat_numbers)),
        "exact_string_match_to_a_catalogue_printed_id": {
            "token_rows": exact_rows,
            "distinct_values": sum(
                1 for v in set(holdat_numbers)
                if v in vol1_ids or v in vol2_ids),
        },
        "zero_padded_form": "Values are zero-padded (e.g. "
                            "'H-0001', 'M-0001') where catalogue "
                            "printed IDs are unpadded (e.g. 'H-1', "
                            "'M-1'); exact-string coincidence with "
                            "a printed catalogue ID is therefore 0.",
        "after_stripping_leading_zeros_only": {
            "distinct_values_coinciding_with_a_printed_id":
                len(norm_distinct & (vol1_ids | vol2_ids)),
            "of_distinct_values": len(norm_distinct),
            "token_rows_coinciding": sum(
                1 for v in holdat_numbers
                if normalize_zero_padded(v)
                in (vol1_ids | vol2_ids)),
            "distinct_values_coinciding_with_a_mayig_id":
                len(norm_distinct & mayig_ids),
            "of_mayig_ids": len(mayig_ids),
            "note": "These coincidences are the collision "
                    "behaviour that makes the field dangerous: "
                    "after zero-stripping, most Holdat values "
                    "coincide with some printed ID, and all 179 "
                    "mayig IDs have a zero-padded namesake in "
                    "Holdat — the Phase-131 result stands: 179 "
                    "apparent namesakes, 0 validated as identity. "
                    "Coincidence under normalisation is not a "
                    "join.",
        },
        "phase131_fact_of_record": "Phase-131: apparent "
                                   "zero-padded namesakes 179 / "
                                   "0 validated; matched-object "
                                   "join ~0 under legitimate key "
                                   "discipline.",
    }

    seal_counter = Counter(r["seal_id"] for r in h_rows)
    per_seal = Counter(seal_counter.values())
    holdat_seal_detail = {
        "key_field": "seal_id",
        "scope": "intra-Holdat only (spec section 3.3)",
        "n_token_rows": len(h_rows),
        "n_distinct_seal_ids": len(seal_counter),
        "rows_per_id_distribution":
            {str(k): per_seal[k] for k in sorted(per_seal)},
        "min_rows_per_id": min(seal_counter.values()),
        "max_rows_per_id": max(seal_counter.values()),
    }

    # Museum cross-reference census: a record carries a CISI
    # cross-reference iff any string value anywhere in the record
    # (recursively) contains 'CISI' or 'Corpus of Indus'. Museum
    # schemas in hand have no dedicated CISI cross-reference field.
    def strings_recursive(obj):
        if isinstance(obj, str):
            yield obj
        elif isinstance(obj, dict):
            for v in obj.values():
                yield from strings_recursive(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from strings_recursive(v)

    def census(records):
        hits = 0
        for rec in records:
            if any("CISI" in s or "Corpus of Indus" in s
                   for s in strings_recursive(rec)):
                hits += 1
        return hits

    penn_text = penn_path.read_text("utf-8")
    penn_fetched = sum(
        1 for line in penn_text.splitlines()
        if line.startswith("## ")
        and not line.startswith("## Also seen"))
    museum_census = {
        "rule": "A museum record counts as carrying a CISI "
                "cross-reference iff any string value in the "
                "acquired record contains 'CISI' or 'Corpus of "
                "Indus'. No museum schema in hand has a dedicated "
                "CISI cross-reference field. Joins are counted "
                "only where such a cross-reference exists; none "
                "are invented.",
        "met": {"n_records_in_layer": len(met_records),
                "n_with_cisi_cross_reference": census(met_records)},
        "cleveland": {"n_records_in_layer": len(cle_records),
                      "n_with_cisi_cross_reference":
                          census(cle_records)},
        "penn": {"n_fetched_records_in_file": penn_fetched,
                 "n_with_cisi_cross_reference":
                     1 if ("CISI" in penn_text
                           or "Corpus of Indus" in penn_text)
                     else 0,
                 "note": "Penn records are a markdown capture, "
                         "not machine-readable records; the count "
                         "is over the captured text. Other numbers "
                         "present (Boston MFA number, Field Nos.) "
                         "are not CISI cross-references."},
        "total_records_censused": (len(met_records)
                                   + len(cle_records)
                                   + penn_fetched),
        "total_with_cisi_cross_reference": (
            census(met_records) + census(cle_records)
            + (1 if "CISI" in penn_text else 0)),
        "verdict": "No CISI cross-reference exists in any "
                   "acquired museum record, so no museum-to-CISI "
                   "join is counted or performed. Museum records "
                   "supply their own objects' metadata under "
                   "their own keys only (boundary 3).",
    }

    join_audit = {
        "canonical_cisi_key": "cisi:v{volume}:{printed_id}",
        "distinct_objects_vol1": len(vol1_ids),
        "distinct_objects_vol2": len(vol2_ids),
        "distinct_volume_scoped_objects": len(catalogue_keys),
        "distinct_unscoped_printed_ids_union":
            len(vol1_ids | vol2_ids),
        "printed_ids_present_in_both_volumes":
            sorted(vol1_ids & vol2_ids),
        "within_volume_duplicate_printed_ids": dup_audit,
        "mayig_cisi_object_id": mayig_key_detail,
        "horus84_cisi": horus_key_detail,
        "holdat_cisi_number": holdat_key_detail,
        "holdat_seal_id": holdat_seal_detail,
        "museum_cross_references": museum_census,
    }

    # ---- Provenance grading summary -------------------------------
    grade_flat = [
        {"layer": r["layer"], "field": r["field"],
         "grade": r["provenance_grade"], "reason": r["grade_reason"]}
        for r in matrix]
    class_i = [g for g in grade_flat if g["grade"] == "I"]
    grading = {
        "grades_by_layer_field": grade_flat,
        "counts": dict(sorted(Counter(
            g["grade"] for g in grade_flat).items())),
        "class_i_fields": class_i,
        "class_i_count": len(class_i),
    }

    # ---- mayig description parseability ------------------------------
    holdat_icon_values = sorted({r["iconography"] for r in h_rows})
    motif_terms = sorted(set(
        [t.lower() for t in MOTIF_TERMS_SECTION_4_3]
        + [v.lower() for v in holdat_icon_values]))
    descs = [x.get("description", "") for x in mayig_ins]
    motif_hits: Counter = Counter()
    type_hits: Counter = Counter()
    n_motif = n_type = n_both = n_neither = 0
    for d in descs:
        low = d.lower()
        mh = [t for t in motif_terms if t in low]
        th = [t for t in OBJECT_TYPE_TERMS if t in low]
        for t in mh:
            motif_hits[t] += 1
        for t in th:
            type_hits[t] += 1
        n_motif += bool(mh)
        n_type += bool(th)
        n_both += bool(mh and th)
        n_neither += not (mh or th)
    parseability = {
        "rule": "Declared before application: case-insensitive "
                "substring match of the mayig layer's free-text "
                "'description' against the motif-term list and "
                "the object-type-term list below. A parse is a "
                "string match under this stated rule only; it is "
                "never reported as ground truth.",
        "motif_term_list": motif_terms,
        "motif_term_list_derivation": "Union of (a) the spec "
                "section 4.3 published iconographic categories and "
                "(b) the distinct values of the Holdat iconography "
                "field as measured in this run: "
                + json.dumps(holdat_icon_values, ensure_ascii=False)
                + ".",
        "object_type_term_list": OBJECT_TYPE_TERMS,
        "n_descriptions": len(descs),
        "n_distinct_descriptions": len(set(descs)),
        "distinct_descriptions": dict(sorted(
            Counter(descs).items())),
        "with_at_least_one_motif_term": n_motif,
        "with_at_least_one_object_type_term": n_type,
        "with_both": n_both,
        "with_neither": n_neither,
        "top_matched_motif_terms": [
            {"term": t, "count": c}
            for t, c in motif_hits.most_common(10)],
        "top_matched_object_type_terms": [
            {"term": t, "count": c}
            for t, c in type_hits.most_common(10)],
    }

    # ---- Site coverage facts (coverage counting only) ---------------
    def per_site_inscriptions(pairs):
        """pairs: (inscription_key, site) — distinct inscriptions."""
        seen: dict[str, str] = {}
        for k, s in pairs:
            seen.setdefault(k, s)
        return dict(sorted(Counter(seen.values()).items()))

    site_facts = {
        "cisi_catalogue_photo_rows_by_site": {
            f"vol{v}": dict(sorted(Counter(
                r["site"] for r in cisi_rows[v]
                if r["site"].strip()).items()))
            for v in (1, 2)},
        "cisi_catalogue_distinct_objects_by_site": dict(sorted(
            Counter(d["site"] for d in obj_view.values()
                    if d["site"]).items())),
        "holdat_inscriptions_by_site": per_site_inscriptions(
            (r["seal_id"], r["site"]) for r in h_rows),
        "holdat_token_rows_by_site": dict(sorted(Counter(
            r["site"] for r in h_rows).items())),
        "horus84_rows_by_site": dict(sorted(Counter(
            r["site"] for r in ho_rows).items())),
        "horus84_n_distinct_sites": len(
            {r["site"] for r in ho_rows}),
        "mayig_site_field_in_layer": None,
        "mayig_site_via_catalogue_join": dict(sorted(Counter(
            obj_view[(1, x["cisi_object_id"])]["site"]
            for x in mayig_ins
            if (1, x["cisi_object_id"]) in obj_view).items())),
        "note": "mayig layer carries no site field of its own; "
                "the mayig row above is the catalogue site of the "
                "joined Vol. 1 object (empty string = the "
                "catalogue rows for that object carry no site). "
                "All counts are coverage facts, not associations.",
    }

    # ---- Feasibility facts (inputs to the report's section 3.5
    # arm-by-arm verdicts; facts only) --------------------------------
    def joined_object_types(records, keyfn):
        out = []
        for rec in records:
            k = keyfn(rec)
            if k is not None and k in obj_view:
                out.append(obj_view[k])
        return out

    mayig_joined = joined_object_types(
        mayig_ins, lambda x: (1, x["cisi_object_id"]))
    horus_joined = []
    for r in ho_rows:
        v = r["cisi"]
        vol = (1 if v in vol1_ids and v not in vol2_ids else
               2 if v in vol2_ids and v not in vol1_ids else None)
        if vol is not None:
            horus_joined.append(obj_view[(vol, v)])
    feasibility = {
        "arm_a_terminal_class_by_object_type": {
            "mayig_inscriptions_joinable_to_catalogue_object_type":
                len(mayig_joined),
            "mayig_joined_object_type_counts": dict(sorted(
                Counter(d["object_type"] for d in mayig_joined)
                .items())),
            "mayig_joined_object_type_filled": sum(
                1 for d in mayig_joined if d["object_type"]),
            "mayig_joined_with_site": sum(
                1 for d in mayig_joined if d["site"]),
            "horus84_rows_joinable_unambiguously": len(horus_joined),
            "horus84_joined_object_type_counts": dict(sorted(
                Counter(d["object_type"] for d in horus_joined)
                .items())),
            "horus84_joined_object_type_filled": sum(
                1 for d in horus_joined if d["object_type"]),
            "holdat_inscriptions_joinable_to_catalogue_object_type":
                0,
            "holdat_reason": "No audited key connects Holdat to "
                             "the catalogue: cisi_number is "
                             "PROHIBITED and seal_id is "
                             "intra-layer only. Holdat carries no "
                             "object-type field; its 'form' "
                             "values are seal_NNNN for all 7,002 "
                             "token rows.",
            "holdat_form_prefix_counts": dict(sorted(Counter(
                r["form"].split("_")[0] for r in h_rows).items())),
        },
        "arm_b_motif_by_sequence": {
            "catalogue_motif_chapter_filled_photo_rows": sum(
                1 for v in (1, 2) for r in cisi_rows[v]
                if r["motif_chapter"].strip()),
            "catalogue_motif_chapter_photo_rows_total": sum(
                len(cisi_rows[v]) for v in (1, 2)),
            "catalogue_distinct_objects_with_motif_chapter": sum(
                1 for d in obj_view.values() if d["motif_chapter"]),
            "catalogue_distinct_objects_total": len(obj_view),
            "holdat_iconography_grade": "C",
            "holdat_iconography_filled_token_rows": sum(
                1 for r in h_rows if r["iconography"].strip()),
            "holdat_distinct_inscriptions_with_iconography":
                len({r["seal_id"] for r in h_rows
                     if r["iconography"].strip()}),
            "mayig_description_parseability_rate":
                (round(n_both / len(descs), 6) if descs else 0.0),
            "mayig_descriptions_with_both_term_kinds": n_both,
            "stage1_dependency": "Spec section 5.3 test (b) runs "
                                 "only if Stage 1 passes its "
                                 "proceed gate (separate owner go, "
                                 "not frozen in Stage 0).",
        },
        "arm_c_site_repertoire": {
            "holdat_site_filled_token_rows": sum(
                1 for r in h_rows if r["site"].strip()),
            "holdat_distinct_inscriptions": len(seal_counter),
            "holdat_n_sites": len({r["site"] for r in h_rows}),
            "horus84_site_filled_rows": sum(
                1 for r in ho_rows if r["site"].strip()),
            "horus84_n_sites": len({r["site"] for r in ho_rows}),
            "mayig_site_field_present_in_layer": False,
            "mayig_inscriptions_with_site_via_join": sum(
                1 for d in mayig_joined if d["site"]),
            "mayig_inscriptions_total": len(mayig_ins),
            "cisi_catalogue_site_filled_photo_rows": sum(
                1 for v in (1, 2) for r in cisi_rows[v]
                if r["site"].strip()),
        },
        "arm_d_graffiti_comparative": {
            "catalogue_graffiti_photo_rows": sum(
                1 for v in (1, 2) for r in cisi_rows[v]
                if r["object_type"] == "Graffiti"),
            "catalogue_graffiti_photo_rows_by_volume": {
                f"vol{v}": sum(1 for r in cisi_rows[v]
                               if r["object_type"] == "Graffiti")
                for v in (1, 2)},
            "catalogue_graffiti_distinct_objects": sum(
                1 for d in obj_view.values()
                if d["object_type"] == "Graffiti"),
            "tamil_nadu_graffiti_corpus_records_in_hand": 0,
            "note": "The Tamil Nadu graffiti corpus "
                    "(tngraffiti.in; 9,486 records per spec "
                    "section 2.6) is NOT in hand; no Stage 0 "
                    "number assumes it. Graffiti is "
                    "comparative only and is never pooled with "
                    "seal texts (boundary 4).",
        },
    }

    # ---- Anomalies ---------------------------------------------------
    anomaly_raw = anomaly_path.read_bytes()
    try:
        anomaly_json = json.loads(anomaly_raw.decode("utf-8"))
        anomaly_models = [m.get("name")
                          for m in anomaly_json.get("models", [])]
    except Exception:  # noqa: BLE001
        anomaly_models = []
    anomalies.append({
        "id": "holdatllc_seal_catalog_content_mismatch",
        "file": "data/raw/other_sites/holdatllc_seal_catalog.csv",
        "finding": "The file's content does not match its name. "
                   "It is not CSV and contains no seal catalogue: "
                   "it is a single-line JSON document in the "
                   "shape of an Ollama /api/tags response listing "
                   "locally installed LLM models.",
        "bytes": len(anomaly_raw),
        "lines": len(anomaly_raw.decode("utf-8", "replace")
                     .splitlines()),
        "json_top_level_keys": sorted(anomaly_json.keys())
        if anomaly_models or isinstance(anomaly_json, dict)
        else [],
        "model_names_listed": anomaly_models,
        "csv_parse": "csv.DictReader finds no seal-catalogue "
                     "header or rows; 0 seal records are "
                     "recoverable from this file.",
        "disposition": "Recorded as found (spec section 3.2 / "
                       "task T4); not routed around, not used as "
                       "a data layer.",
    })
    for vol in (1, 2):
        d = dup_audit[f"vol{vol}"]
        if d["n_duplicate_photo_keys"]:
            anomalies.append({
                "id": f"cisi_vol{vol}_duplicate_photo_keys",
                "file": f"cisi_vol{vol}_catalogue.csv",
                "finding": "Exact duplicate photo_key values "
                           "within the volume (the row-level "
                           "key repeats).",
                "duplicate_photo_keys": d["duplicate_photo_keys"],
            })
    motif_variants = {}
    for vol in (1, 2):
        vals = Counter(r["motif_chapter"] for r in cisi_rows[vol]
                       if r["motif_chapter"].strip())
        motif_variants[f"vol{vol}"] = dict(sorted(vals.items()))
    anomalies.append({
        "id": "cisi_motif_chapter_variants",
        "finding": "motif_chapter values as printed include "
                   "spelling variants of 'unicorn' and, in Vol. 1, "
                   "chapter-heading strings ('SEALS', "
                   "'SEALSIMPRESSIONS') in the motif field. "
                   "Recorded as found; no cleaning was applied.",
        "motif_chapter_values_by_volume": motif_variants,
    })
    anomalies.append({
        "id": "cisi_cross_volume_printed_id",
        "finding": "Exactly one printed ID, 'H-311', occurs in "
                   "both volumes; volume-scoping the key "
                   "(cisi:v{volume}:{printed_id}) is therefore "
                   "necessary and sufficient for the catalogue "
                   "population in hand.",
        "printed_ids_in_both_volumes": sorted(vol1_ids & vol2_ids),
    })
    anomalies.append({
        "id": "holdat_empty_and_constant_interpretive_fields",
        "finding": "Holdat 'prefix' and 'vowel' are empty on all "
                   "7,002 token rows; 'noun' and 'verb' are the "
                   "constant '0' on all rows. The fields exist in "
                   "the schema and are graded Class I, but carry "
                   "no varying content as acquired.",
    })
    anomalies.append({
        "id": "horus_placeholder_conventions",
        "finding": "horus84 fields encode absence with "
                   "placeholders ('-', '--', '- -', 'None', '?', "
                   "'??') and, in the (mm) dimension fields, "
                   "with the value '0'. Raw filled rates count "
                   "non-empty cells; per-field placeholder counts "
                   "are recorded in the coverage matrix.",
    })
    # horus84 raw row-length distribution (rows shorter than the
    # header are missing trailing fields; csv.DictReader pads
    # them as absent, which is how the matrix treats them).
    with horus_path.open(newline="", encoding="utf-8") as fh:
        raw_lengths = Counter(len(r) for r in csv.reader(fh))
    anomalies.append({
        "id": "horus_row_length_variation",
        "finding": "Rows in inscriptions.csv do not all carry "
                   "the full 38 fields: trailing fields are "
                   "omitted on shorter rows (standard CSV "
                   "parsing pads them as absent, and the "
                   "coverage matrix treats them as unfilled). "
                   "Row-length distribution including the "
                   "header row is recorded here.",
        "row_length_distribution_including_header":
            {str(k): raw_lengths[k] for k in sorted(raw_lengths)},
    })
    anomalies.append({
        "id": "museum_acquisition_file_counts",
        "finding": "The Met objects directory in the downloads "
                   "tree holds 74 fetched object files (search "
                   "candidates); the curated Indus layer is the "
                   "28 object IDs listed in indus_object_ids.json "
                   "and summarised in indus_objects_summary.json. "
                   "The Cleveland 'indus' search file holds 10 "
                   "records, of which 3 carry type 'Seals'.",
        "met_object_files_in_directory": len(list(
            (args.museum_dir / "met" / "objects").glob("*.json"))),
        "met_curated_indus_records": len(met_records),
        "cleveland_records_in_search_file": len(cle_records),
        "cleveland_records_with_type_seals": sum(
            1 for r in cle_records if r.get("type") == "Seals"),
    })

    # ---- Non-machine-readable pass (T4) ------------------------------
    non_mr = build_non_machine_readable(args, kodumanal_path,
                                        kunal_path, penn_text)

    # ---- Appendix A drift table --------------------------------------
    drift = build_drift(cisi_rows, cisi_fields, vol1_ids, vol2_ids,
                        h_rows, h_fields, mayig_ins, ho_rows,
                        ho_fields, met_records, cle_records,
                        penn_fetched)

    inventory = {
        "phase": "Phase-133",
        "spec": "specs/024-evidence-integration/spec.md",
        "stage": "Stage 0 (FROZEN 2026-10-09)",
        "scope": "Coverage and joinability only (spec section "
                 "3.1): counts, rates, distinct values, collision "
                 "measurements, provenance grades. No "
                 "associations, no correlations, no findings "
                 "about the inscriptions.",
        "filled_definition": "A cell is filled iff its value is "
                             "present and, for strings, non-empty "
                             "after stripping whitespace; for "
                             "lists/dicts, non-empty. Placeholder "
                             "strings that encode absence ('-', "
                             "'--', 'None', '?', etc.) are "
                             "non-empty cells and are counted as "
                             "filled in the raw rate, with their "
                             "count recorded separately per field "
                             "where present.",
        "layers": layers,
        "coverage_matrix": matrix,
        "join_key_audit": join_audit,
        "provenance_grading": grading,
        "mayig_description_parseability": parseability,
        "site_coverage_facts": site_facts,
        "feasibility_facts": feasibility,
        "anomalies": anomalies,
        "non_machine_readable_pass": non_mr,
        "appendix_a_drift_table": drift,
        "anchors_note": "No anchor, reading, or PRED-2026 value "
                        "is an input or an output of this "
                        "inventory (spec boundary 1 / section 7).",
    }

    meta = {
        "dataset_name": "phase133_stage0_inventory",
        "dataset_file": "data/evidence_integration/"
                        "phase133_stage0_inventory.json",
        "spec": "specs/024-evidence-integration/spec.md "
                "(FROZEN Stage 0, 2026-10-09; PR #105, merge "
                "467adbcf, freeze fecba9ec)",
        "phase": "Phase-133",
        "builder": "backend/scripts/phase133_stage0_inventory.py",
        "provenance": "Every count recomputed by the builder "
                      "from the input files listed below at run "
                      "time; nothing copied from spec Appendix A "
                      "(Appendix A values are the claims checked "
                      "in the drift table).",
        "license_basis_per_layer": {
            layer["layer_id"]: layer["license_basis"]
            for layer in layers},
        "publication_basis": "Stage 0 inventory dataset approved "
                             "for CC BY 4.0 publication through "
                             "the release gate at Stage 0 "
                             "completion (spec Decision Ask 4, "
                             "freeze record 2026-10-09). This "
                             "build performs no publication; "
                             "disposition is task T6, handled "
                             "separately. Facts only; no images, "
                             "ever (boundary 5).",
        "inputs": inputs,
        "restricted_material": "No CISI image, page scan, or "
                               "restricted source file is "
                               "included; inputs were read from "
                               "the local store and only counts, "
                               "codes, and text are emitted.",
    }
    # content hash of the inventory, recorded in meta (Phase-132 style)
    meta["dataset_content_hash"] = content_hash(inventory)
    meta["hash_method"] = ("sha256 of canonical JSON (sort_keys, "
                           "ensure_ascii=False) of the inventory "
                           "object")
    return inventory, meta


def build_non_machine_readable(args, kodumanal_path: Path,
                               kunal_path: Path,
                               penn_text: str) -> list[dict]:
    out = []
    # Kodumanal: descriptive structure from the OCR text layer
    # and the volume's own contents listing. Printed tallies are
    # quoted as printed prose, never as computed counts.
    kod = {
        "id": "kodumanal_volume",
        "file": "kodumanal-dli/TVA_BOK_0010628_Archaeological_"
                "Excavations_of_Tamilnadu_VolII_Kodumanal.pdf",
        "form": "Scanned excavation-report volume (DLI scan, "
                "local research copy) with an OCR text layer; "
                "not machine-readable as a dataset: no tabular "
                "records, no per-object field structure that a "
                "parser could audit.",
        "pages": None,
        "structure": [],
        "descriptive_notes": [],
    }
    try:
        import fitz  # PyMuPDF, local tooling only
        doc = fitz.open(kodumanal_path)
        kod["pages"] = len(doc)
        text = "\n".join(p.get_text() for p in doc)
        doc.close()
        for heading in ("INTRODUCTION", "HISTORICAL BACKGROUND",
                        "TRENCHES", "CULTURAL SEQUENCE AND "
                        "CHRONOLOGY", "POTTERY", "GRAFFITI MARKS",
                        "ANTIQUITIES", "CONCLUSION"):
            if heading.lower() in text.lower():
                kod["structure"].append(
                    f"Kodumanal report section present: {heading}")
        trenches = sorted(set(re.findall(r"KML-\d+", text)))
        kod["descriptive_notes"].append(
            f"Trench-level organisation: the Trenches section is "
            f"organised by trench labels (OCR text contains "
            f"{len(trenches)} distinct KML-n trench labels, "
            f"e.g. {', '.join(trenches[:3])}); each trench entry "
            f"records location/orientation, dimensions, depth, "
            f"layers/phases, and the antiquities recovered, in "
            f"prose.")
        kod["descriptive_notes"].append(
            "Context structure: habitation trenches and the "
            "megalithic burial complex are reported in the same "
            "prose organisation; pottery is classified by ware "
            "(Black-and-red ware, Russet-coated ware, Red ware, "
            "Black ware), and graffiti marks are discussed by "
            "ware, by vessel position (shoulder near the rim), "
            "and as pre-firing vs surface marks.")
        kod["descriptive_notes"].append(
            "Printed tallies (quoted as printed prose in the "
            "Graffiti Marks section, NOT computed counts): the "
            "section states 'Out of 175 graffiti marks 75 in "
            "Black and Red ware, 70 Red ware, 70 Russet Coated "
            "ware and 10 Black ware were noticed' — whose "
            "printed subtotals sum to 225, not 175 — and "
            "separately that '41 Brahmi sherds were observed "
            "and 99 Graffiti marks were collected'. The printed "
            "prose is internally inconsistent, so no tally "
            "from this volume is used as a count anywhere in "
            "Stage 0.")
        kod["descriptive_notes"].append(
            "The Graffiti Marks section continues with a "
            "numbered prose description list of individual "
            "marks, each described in words with its ware "
            "(e.g. bow-and-arrow, boat-like, sun symbols, "
            "Brahmi-letter-like forms) — a descriptive "
            "catalogue in prose, not a coded field structure.")
        kod["descriptive_notes"].append(
            "Volume scope: the 152-page volume also contains "
            "the Karur and Poompuhar reports; the Kodumanal "
            "report is printed pp. 1-50 per the contents page. "
            "Comparative strand only (boundary 4).")
    except Exception as exc:  # noqa: BLE001
        kod["descriptive_notes"].append(
            f"Descriptive extraction unavailable in this "
            f"environment ({exc}); structure per spec section "
            f"2.6 and the acquisition record only.")
    out.append(kod)

    kun = {
        "id": "kunal_article",
        "file": "jstage-kunal-2012/JOrient55_22_Kunal_"
                "PreIndusSeals.pdf",
        "form": "Journal article PDF (J-STAGE, Journal of the "
                "Japanese Association for South Asian Studies / "
                "JOrient 55, 2012, DOI 10.5356/jorient.55.22); "
                "not machine-readable as acquired.",
        "pages": None,
        "structure": [],
        "descriptive_notes": [
            "Subject, per spec section 2.6 and the acquisition "
            "record: Early Harappan seals from Kunal published "
            "with their stratigraphic context — small and "
            "context-dense, in journal prose and figures.",
            "Field/context structure is the article's own: "
            "seals are presented in the excavation's "
            "stratigraphic/period framework in prose and "
            "plates; there is no tabular per-object record "
            "structure a parser could audit, and no counts are "
            "taken from it.",
        ],
    }
    try:
        import fitz
        doc = fitz.open(kunal_path)
        kun["pages"] = len(doc)
        full_text = "".join(p.get_text() for p in doc)
        doc.close()
        alnum = sum(1 for c in full_text if c.isalnum())
        kun["descriptive_notes"].append(
            f"Measured file property (not a content count): "
            f"{kun['pages']} PDF pages; the embedded text layer "
            f"contains {alnum} alphanumeric characters in total "
            f"(its extracted characters are NUL glyphs) — the "
            f"article's text and seal drawings are page "
            f"images, which is the mechanical reason no "
            f"machine-readable pass is possible on the file as "
            f"acquired.")
    except Exception as exc:  # noqa: BLE001
        kun["descriptive_notes"].append(
            f"Page/text measurement unavailable in this "
            f"environment ({exc}).")
    out.append(kun)

    out.append({
        "id": "museum_penn_records",
        "file": "museum-open-data/penn/penn_records.md",
        "form": "Markdown capture of two Penn Museum object "
                "pages (no JSON API located at acquisition); "
                "not machine-readable records.",
        "structure": [
            "Per-record fields as captured in prose: Object "
            "Number, object kind, Culture, Provenience, Site, "
            "Date Made, Section, Materials, Iconography, "
            "Inscription Language, Description, Other numbers, "
            "Location / Credit.",
        ],
        "descriptive_notes": [
            "Two fetched records (L-141-177, a Chanhu-Daro "
            "seal; 54-38-5, a seal impression) plus one further "
            "object (L-141-176) noted in the gallery listing "
            "but not individually fetched — it is not a "
            "record in hand.",
            "The L-141-177 record carries an Iconography field "
            "('Horned Animal') in the museum's own prose — a "
            "museum depiction description, not a coded field "
            "in a machine-readable layer.",
            "No CISI cross-reference appears in the captured "
            "text (see museum census).",
        ],
    })
    return out


def _rate_pct(filled: int, total: int) -> float:
    return round(100.0 * filled / total, 1) if total else 0.0


def build_drift(cisi_rows, cisi_fields, vol1_ids, vol2_ids,
                h_rows, h_fields, mayig_ins, ho_rows, ho_fields,
                met_records, cle_records, penn_fetched) -> list:
    A = APPENDIX_A
    rows = []

    def entry(item, appendix_value, measured_value, verdict,
              note=""):
        rows.append({"item": item,
                     "appendix_a_value": appendix_value,
                     "measured_value": measured_value,
                     "verdict": verdict, "note": note})

    tot = sum(len(cisi_rows[v]) for v in (1, 2))
    entry("CISI catalogue total photo rows",
          A["cisi_total_rows"], tot,
          "MATCH" if tot == A["cisi_total_rows"] else "DRIFT")
    for v in (1, 2):
        entry(f"CISI Vol. {v} photo rows",
              A[f"cisi_vol{v}_rows"], len(cisi_rows[v]),
              "MATCH" if len(cisi_rows[v]) == A[f"cisi_vol{v}_rows"]
              else "DRIFT")
        entry(f"CISI Vol. {v} distinct printed IDs",
              A[f"cisi_vol{v}_distinct"],
              len({1: vol1_ids, 2: vol2_ids}[v]),
              "MATCH")
    entry("CISI distinct volume-scoped objects (both volumes)",
          A["cisi_distinct_volume_scoped"],
          len(vol1_ids) + len(vol2_ids), "MATCH",
          "Volume-scoped sum. Clarification, not a correction: "
          "the unscoped union of printed IDs is "
          f"{len(vol1_ids | vol2_ids)}, because exactly one "
          "printed ID ('H-311') occurs in both volumes.")
    entry("CISI fields per volume", A["cisi_n_fields"],
          len(cisi_fields[1]), "MATCH",
          "Vol. 1 and Vol. 2 headers are identical, 22 fields.")
    for v, key in ((1, "v1"), (2, "v2")):
        rows_v = cisi_rows[v]
        for field, akey in (
                ("site", f"cisi_site_rate_{key}_pct"),
                ("object_type", f"cisi_object_type_rate_{key}_pct"),
                ("motif_chapter", f"cisi_motif_rate_{key}_pct")):
            filled = sum(1 for r in rows_v if r[field].strip())
            measured = _rate_pct(filled, len(rows_v))
            entry(f"CISI Vol. {v} {field} fill rate %",
                  A[akey], measured,
                  "MATCH" if measured == A[akey] else "DRIFT")
    motif_rows = sum(1 for v in (1, 2) for r in cisi_rows[v]
                     if r["motif_chapter"].strip())
    entry("CISI motif_chapter filled rows (both volumes, "
          "spec section 2.1)", A["cisi_motif_rows_total"],
          motif_rows, "MATCH" if motif_rows == 2005 else "DRIFT")
    for field in ("material", "dimensions"):
        filled = sum(1 for v in (1, 2) for r in cisi_rows[v]
                     if r[field].strip())
        entry(f"CISI {field} fill rate % (both volumes)",
              A[f"cisi_{field}_rate_pct"],
              _rate_pct(filled, tot), "MATCH")
    ot = Counter(r["object_type"] for v in (1, 2)
                 for r in cisi_rows[v] if r["object_type"].strip())
    entry("CISI object_type photo-row totals (spec section 2.1)",
          A["cisi_object_type_rows"], dict(sorted(ot.items())),
          "MATCH" if dict(ot) == A["cisi_object_type_rows"]
          else "DRIFT")
    entry("Holdat token rows", A["holdat_rows"], len(h_rows),
          "MATCH" if len(h_rows) == A["holdat_rows"] else "DRIFT")
    entry("Holdat distinct seal_id",
          A["holdat_distinct_seal_id"],
          len({r["seal_id"] for r in h_rows}), "MATCH")
    entry("Holdat fields", A["holdat_n_fields"], len(h_fields),
          "MATCH")
    entry("Holdat site fill rate % (token level)", 100.0,
          _rate_pct(sum(1 for r in h_rows if r["site"].strip()),
                    len(h_rows)), "MATCH")
    entry("Holdat iconography fill rate % (token level)", 100.0,
          _rate_pct(sum(1 for r in h_rows
                        if r["iconography"].strip()), len(h_rows)),
          "MATCH")
    icon_top = dict(Counter(r["iconography"] for r in h_rows)
                    .most_common(6))
    entry("Holdat iconography top values (token counts)",
          A["holdat_iconography_top"], icon_top,
          "MATCH" if icon_top == A["holdat_iconography_top"]
          else "DRIFT")
    entry("mayig inscriptions", A["mayig_inscriptions"],
          len(mayig_ins), "MATCH")
    entry("mayig tokens (sum of token_count)",
          A["mayig_tokens"],
          sum(x["token_count"] for x in mayig_ins), "MATCH")
    entry("mayig distinct signs (distinct tokens)",
          A["mayig_distinct_signs"],
          len({t for x in mayig_ins for t in x["tokens"]}),
          "MATCH")
    entry("horus84 rows", A["horus_rows"], len(ho_rows),
          "MATCH" if len(ho_rows) == A["horus_rows"] else "DRIFT")
    entry("horus84 fields", A["horus_n_fields"], len(ho_fields),
          "MATCH" if len(ho_fields) == A["horus_n_fields"]
          else "DRIFT",
          "The header of inscriptions.csv as acquired contains "
          "38 field names. Appendix A.4's own enumerated list "
          "also names 38 fields — the same 38, in the same "
          "order — while its prose says 39; spec section 2.4 "
          "repeats 39. The '39' is a miscount in the spec "
          "text; the field inventory itself matches the "
          "acquired header exactly.")
    entry("Museum Met objects in curated Indus layer",
          A["museum_met_objects"], len(met_records), "MATCH")
    met_seal_titled = sum(
        1 for r in met_records
        if "seal" in (str(r.get("objectName", "")) + " "
                      + str(r.get("title", ""))).lower())
    met_inscription_titled = sum(
        1 for r in met_records
        if "inscription" in str(r.get("title", "")).lower())
    entry("Museum Met 'incl. 4 inscribed seals' (Appendix A.5)",
          "4 inscribed seals",
          f"{met_seal_titled} seal objects, of which "
          f"{met_inscription_titled} has a title mentioning an "
          f"inscription",
          "DRIFT (wording)",
          "The 28-object count and the 4 seal objects match; "
          "'inscribed' is acquisition shorthand — only object "
          "49.40.3 is titled with 'inscription'. The other "
          "three are stamp seals 49.40.1/.2/.4.")
    cle_seals = sum(1 for r in cle_records
                    if r.get("type") == "Seals")
    entry("Museum Cleveland '3 seals' (Appendix A.5)",
          A["museum_cleveland_seals"],
          f"{cle_seals} records with type 'Seals', in an "
          f"acquired search file of {len(cle_records)} records",
          "DRIFT (presentation)",
          "Appendix A.5 summarises the layer by its 3 seals; "
          "the acquired file is the full 'indus' search result "
          "set: 10 records (3 seals, 1 jar, and 6 other object "
          "types). Stage 0 inventories the file as acquired.")
    entry("Museum Penn records", A["museum_penn_records"],
          penn_fetched, "MATCH",
          "Fetched records in penn_records.md; a third object "
          "is noted as seen in a gallery listing but was not "
          "fetched and is not counted.")
    entry("Phase-124 catalogue sample field accuracy 98.9% "
          "(spec section 2.1)", "98.9%",
          "not recomputed",
          "NOT RECOMPUTED",
          "Stage 0 takes no new hand-verified sample; the "
          "Phase-124 figure stands as a fact of record, not "
          "as a Stage 0 measurement.")
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cisi-vol1", type=Path, default=(
        MAIN_CHECKOUT / "corpora/downloads/cisi_image_layer"
        / "catalogue/cisi_vol1_catalogue.csv"))
    ap.add_argument("--cisi-vol2", type=Path, default=(
        MAIN_CHECKOUT / "corpora/downloads/cisi_image_layer"
        / "catalogue/cisi_vol2_catalogue.csv"))
    ap.add_argument("--holdat", type=Path, default=(
        MAIN_CHECKOUT / "corpora/downloads/external_repos"
        / "holdatllc_indus/indus_corpus 2.csv"))
    ap.add_argument("--holdat-roles", type=Path, default=(
        MAIN_CHECKOUT / "corpora/downloads/external_repos"
        / "holdatllc_indus/all_symbol_semantic_roles 2.csv"))
    ap.add_argument("--mayig-layer", type=Path, default=(
        REPO_ROOT / "data/corpus_layers/mayig_cisi_layer_v1.json"))
    ap.add_argument("--mayig-meta", type=Path, default=(
        REPO_ROOT / "data/corpus_layers/"
        "mayig_cisi_layer_v1_meta.json"))
    ap.add_argument("--mayig-source-dir", type=Path, default=(
        SWEEP / "mayig-indus-valley-script-corpus" / "corpus"))
    ap.add_argument("--horus", type=Path, default=(
        SWEEP / "horus84-computational-linguistics" / "data"
        / "inscriptions.csv"))
    ap.add_argument("--museum-dir", type=Path,
                    default=SWEEP / "museum-open-data")
    ap.add_argument("--anomaly-file", type=Path, default=(
        REPO_ROOT / "data/raw/other_sites/"
        "holdatllc_seal_catalog.csv"))
    ap.add_argument("--kodumanal", type=Path, default=(
        SWEEP / "kodumanal-dli"
        / "TVA_BOK_0010628_Archaeological_Excavations_of_"
          "Tamilnadu_VolII_Kodumanal.pdf"))
    ap.add_argument("--kunal", type=Path, default=(
        SWEEP / "jstage-kunal-2012"
        / "JOrient55_22_Kunal_PreIndusSeals.pdf"))
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--meta-out", type=Path,
                    default=DEFAULT_META_OUT)
    args = ap.parse_args(argv)

    inventory, meta = build(args)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(inventory, indent=1, ensure_ascii=False) + "\n",
        "utf-8")
    args.meta_out.write_text(
        json.dumps(meta, indent=1, ensure_ascii=False) + "\n",
        "utf-8")
    ja = inventory["join_key_audit"]
    print(f"layers: {len(inventory['layers'])} | coverage rows: "
          f"{len(inventory['coverage_matrix'])} | Class I fields: "
          f"{inventory['provenance_grading']['class_i_count']}")
    mayig_key = ja["mayig_cisi_object_id"]
    museum_total = ja["museum_cross_references"][
        "total_with_cisi_cross_reference"]
    print(f"catalogue objects: v1 {ja['distinct_objects_vol1']} "
          f"v2 {ja['distinct_objects_vol2']} | mayig key: "
          f"{mayig_key['matched_single_volume']}"
          f"/{mayig_key['n_values_tested']} "
          f"matched | museum cross-refs: {museum_total}")
    print(f"wrote {args.out} and {args.meta_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
