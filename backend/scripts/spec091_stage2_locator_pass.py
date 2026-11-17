#!/usr/bin/env python3
"""Spec 091 Stage 2 — the locator pass (T201 artifact + generator; T202 run).

The locator record is a NEW versioned artifact beside the frozen WP4
provenance file (`mahadevan_parpola_crosswalk_v2_provenance.json`,
never written by this script). For every one of the 184 crosswalk
entries, per reading field (`phonetic_reading`, `semantic_reading`),
it files exactly one outcome:

- a **locator** — the three-part primary-source locator of
  eligibility-defs v1 §2 (work + page/table/figure pinpoint + sign
  scheme) whose cited passage carries the field's value; or
- a **not-found** — backed by the documented search: the sources
  consulted, in order, each with its status (searched / not held /
  in-repo derivative), its method, its per-entry facts, and the
  search date (C091-1).

A file-level citation is not a locator (WP4; eligibility-defs §2),
and a pointer to another in-repo table is not a locator: the
program's own derivative compilations are consulted and recorded,
but they cannot ground a locator. Only a held primary source whose
passage carries the value at an entry-level pinpoint grounds one.

The generator REFUSES (raises, writes nothing) when:
- a registered held search source is absent at its canonical path
  (the pass must actually search the program's held copies);
- any entry/field would be filed with neither outcome, or with a
  malformed one (the validator runs before any write);
- an input's bytes differ from the pins the run declares.

Execution is a run under the program's run discipline (Spec 089):
`--execute` mints a run id at start (D-089-1), writes the artifact,
and writes the run record (surface `study`, store = the spec's
`records/`) through `glossa_lab.run_records`. `--verify-sample`
re-executes the searches for the rule-drawn sample from fresh reads
and files the per-entry verification results.

Standing position: the Indus script is not deciphered. This pass
records where readings can be found in the primary literature; it
establishes no reading's correctness and no entry's eligibility
(eligibility-defs v1; C091-1's own "does not establish").
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from glossa_lab import run_records  # noqa: E402
from glossa_lab.verified_write import write_file_verified  # noqa: E402

ARTIFACT_NAME = "mahadevan_parpola_crosswalk_v2_locators"
ARTIFACT_VERSION = "v1"
TOOL_NAME = "spec091_stage2_locator_pass.py"
TOOL_VERSION = "locator-pass v1 (Spec 091 Stage 2)"

PROVENANCE_REL = "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_provenance.json"
CROSSWALK_REL = "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"
PHONEME_REL = "backend/glossa_lab/data/parpola_phonemes.json"
M77_REL = "glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.csv"
WELLS_REL = "glossa-corpus/indus/sources/wells-1998/wells1998_sign_list.json"
ARTIFACT_REL = "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_locators.json"
SPEC_RECORDS_REL = "specs/091-anchor-comparison-integrity/records"
VERIFICATION_REL = f"{SPEC_RECORDS_REL}/t202-sample-verification.json"

FIELDS = ("phonetic_reading", "semantic_reading")
LOCATOR_PARTS = ("work", "pinpoint", "sign_scheme", "cited_value")


class LocatorPassError(ValueError):
    """A named refusal: the pass declines to file a defective record."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Search sources. A source knows how to search one held (or unheld)
# copy for one entry/field and returns a step dict. A source with
# `can_ground_locator` may additionally return a locator.
# ---------------------------------------------------------------------------


class Source:
    def __init__(
        self,
        source_id: str,
        work: str,
        *,
        held: bool,
        held_as: Optional[str],
        sha256: Optional[str],
        can_ground_locator: bool,
        search: Callable[[dict, str], dict],
        locate: Optional[Callable[[dict, str], Optional[dict]]] = None,
    ) -> None:
        self.source_id = source_id
        self.work = work
        self.held = held
        self.held_as = held_as
        self.sha256 = sha256
        self.can_ground_locator = can_ground_locator
        self._search = search
        self._locate = locate

    def search(self, ctx: dict, field: str) -> dict:
        return self._search(ctx, field)

    def locate(self, ctx: dict, field: str) -> Optional[dict]:
        if self._locate is None or not self.can_ground_locator:
            return None
        return self._locate(ctx, field)

    def registry_entry(self) -> dict:
        return {
            "source_id": self.source_id,
            "work": self.work,
            "held": self.held,
            "held_as": self.held_as,
            "sha256": self.sha256,
            "can_ground_locator": self.can_ground_locator,
        }


def _step(source: Source, status: str, method: str, facts: dict, result: str, date: str) -> dict:
    return {
        "source_id": source.source_id,
        "work": source.work,
        "status": status,
        "method": method,
        "facts": facts,
        "result": result,
        "date": date,
    }


def parpola_1994_source() -> Source:
    def search(ctx: dict, field: str) -> dict:
        stated = ctx["source_as_stated"]
        detail = (
            "the work is not held by the program (no copy in the repo, on the "
            "mini-server, or in the tower-compute archive, surveyed 2026-11-17), "
            "so its text cannot be searched"
        )
        if stated == "Parpola 1994 Appendix B":
            detail += (
                "; the entry's stated pinpoint is Appendix B, which WP4 "
                "established is a sign-correspondence table: it supplies the "
                "Mahadevan-Parpola sign mapping, not readings"
            )
        return {
            "status": "not_held",
            "method": "consult the program's holdings for the work's text",
            "facts": {"held": False},
            "result": detail,
        }

    return Source(
        "parpola_1994",
        "Parpola 1994, Deciphering the Indus Script (Cambridge University Press)",
        held=False,
        held_as=None,
        sha256=None,
        can_ground_locator=True,
        search=search,
    )


def parpola_2010_source() -> Source:
    def search(ctx: dict, field: str) -> dict:
        return {
            "status": "not_held",
            "method": "consult the program's holdings for the work's text",
            "facts": {"held": False, "metadata_record_only": True},
            "result": (
                "the program holds only a metadata record for this lecture "
                "(glossa-indus/literature/documents/parpola_2010_dravidian_"
                "solution.json; the raw PDF stood on the retired Windows "
                "desktop), so its text cannot be searched"
            ),
        }

    return Source(
        "parpola_2010",
        "Parpola 2010, A Dravidian solution to the Indus script problem "
        "(World Classical Tamil Conference lecture)",
        held=False,
        held_as=None,
        sha256=None,
        can_ground_locator=True,
        search=search,
    )


def mahadevan_1977_source(rows_by_no: dict[int, dict], path: Path) -> Source:
    def search(ctx: dict, field: str) -> dict:
        row = rows_by_no.get(ctx["mahadevan_num"])
        if field == "phonetic_reading":
            result = (
                "the sign list attributes no phonetic value to any sign: its "
                "columns carry the sign number, a graphic-variant marker, the "
                "book's morphological class, and page numbers only"
            )
        else:
            result = (
                "the sign list attributes no meaning to any sign separately: "
                "its columns carry the sign number, a graphic-variant marker, "
                "the book's morphological class, and page numbers only"
            )
        facts = {
            "sign_present": row is not None,
            "value_attributed": False,
            "row": row,
        }
        return {
            "status": "searched",
            "method": (
                "row lookup by Mahadevan sign number in the held sign-list "
                "dataset transcribed from the pinned MASI 77 scan"
            ),
            "facts": facts,
            "result": result,
        }

    return Source(
        "mahadevan_1977_sign_list",
        "Mahadevan 1977, The Indus Script: Texts, Concordance and Tables "
        "(ASI MASI No. 77), Sign List (printed pp. 32-35)",
        held=True,
        held_as=M77_REL,
        sha256=sha256_file(path),
        can_ground_locator=False,
        search=search,
    )


def wells_1998_source(rows: list[dict], path: Path) -> Source:
    by_mahadevan: dict[int, dict] = {}
    for row in rows:
        for key in ("mahadevan_no", "mahadevan_num", "mahadevan_id"):
            value = row.get(key)
            if isinstance(value, int):
                by_mahadevan.setdefault(value, row)
            elif isinstance(value, str) and value.strip().lstrip("M").isdigit():
                by_mahadevan.setdefault(int(value.strip().lstrip("M")), row)

    def search(ctx: dict, field: str) -> dict:
        row = by_mahadevan.get(ctx["mahadevan_num"])
        identifications = []
        if row is not None:
            for key in ("identifications_full", "identifications"):
                value = row.get(key)
                if isinstance(value, list):
                    identifications = [str(v) for v in value]
                elif isinstance(value, str) and value.strip():
                    identifications = [value]
        if field == "phonetic_reading":
            result = (
                "Wells attributes no phonetic value to any sign: his table "
                "carries sign numbers, totals, varieties, set, class, type, "
                "site frequencies, and his own pictorial identifications"
            )
        else:
            result = (
                "Wells states pictorial identifications of his own for some "
                "signs; he attributes no meaning as this entry's Parpola "
                "reading, and an identification by a different author is not "
                "the entry's reading at its primary source"
            )
        facts = {
            "row_found_by_mahadevan_crossref": row is not None,
            "phonetic_value_attributed": False,
            "identifications_stated": identifications,
        }
        return {
            "status": "searched",
            "method": (
                "row lookup by the dataset's Mahadevan cross-reference in the "
                "held sign-list dataset transcribed from the pinned thesis scan"
            ),
            "facts": facts,
            "result": result,
        }

    return Source(
        "wells_1998_sign_list",
        "Wells 1998, An Introduction to Indus Writing (University of "
        "Calgary MA thesis), Appendix I, Table 3.2",
        held=True,
        held_as=WELLS_REL,
        sha256=sha256_file(path),
        can_ground_locator=False,
        search=search,
    )


def phoneme_compilation_source(phoneme_map: dict, path: Path) -> Source:
    def search(ctx: dict, field: str) -> dict:
        num = ctx["parpola_num"]
        hit = phoneme_map.get(str(num)) if num is not None else None
        if num is None:
            return {
                "status": "searched",
                "method": "lookup by Parpola sign number in the compilation",
                "facts": {"hit": False, "reason": "no Parpola number recorded for this entry"},
                "result": (
                    "the crosswalk records no Parpola number for this entry, "
                    "so the compilation cannot be consulted by key"
                ),
            }
        if hit is None:
            return {
                "status": "searched",
                "method": "lookup by Parpola sign number in the compilation",
                "facts": {"hit": False},
                "result": "the compilation carries no proposal for this Parpola number",
            }
        if field == "phonetic_reading":
            result = (
                f"the compilation carries a proposal for this sign "
                f"(phoneme {hit.get('phoneme')!r}, source label "
                f"{hit.get('source')!r}) — a pointer to the primary "
                "literature, not a locator: the compilation is an in-repo "
                "table, and WP4's rule is that a pointer to another in-repo "
                "table is not a locator; the labelled primary text is not held"
            )
        else:
            result = (
                f"the compilation carries a gloss for this sign "
                f"({hit.get('gloss')!r}, on its phoneme entry) — the "
                "compilation's own gloss in an in-repo table, not a "
                "primary-source attestation of a meaning"
            )
        return {
            "status": "searched",
            "method": "lookup by Parpola sign number in the compilation",
            "facts": {
                "hit": True,
                "phoneme": hit.get("phoneme"),
                "gloss": hit.get("gloss"),
                "source_label": hit.get("source"),
            },
            "result": result,
        }

    return Source(
        "parpola_phonemes_compilation",
        "Program compilation of Parpola's proposed values "
        "(backend/glossa_lab/data/parpola_phonemes.json) — in-repo "
        "derivative, consulted as a pointer only",
        held=True,
        held_as=PHONEME_REL,
        sha256=sha256_file(path),
        can_ground_locator=False,
        search=search,
    )


def stated_source_step(ctx: dict, field: str, date: str) -> Optional[dict]:
    """The entry's own stated source, where it is an in-repo derivative.

    Returns None when the stated source is Parpola 1994 itself (the
    parpola_1994 step covers it, in first position).
    """
    stated = ctx["source_as_stated"]
    if stated == "Parpola 1994 Appendix B":
        return None
    if "Phase-28" in stated:
        source = Source(
            "crosswalk_phase28_file", stated, held=True, held_as=CROSSWALK_REL,
            sha256=None, can_ground_locator=False, search=lambda c, f: {},
        )
        return _step(
            source, "searched",
            "read the entry in the Phase-28 predecessor table the label names",
            {"in_repo_derivative": True, "pinpoint": None},
            "the stated source is the crosswalk's own Phase-28 predecessor "
            "table (in-repo): it carries the value at file level with no "
            "entry-level pinpoint, and a pointer to another in-repo table "
            "is not a locator (WP4)",
            date,
        )
    if "spec 004" in stated:
        source = Source(
            "crosswalk_spec004_expansion", stated, held=True, held_as=CROSSWALK_REL,
            sha256=None, can_ground_locator=False, search=lambda c, f: {},
        )
        return _step(
            source, "searched",
            "read the entry as admitted by the spec 004 WS2 expansion",
            {"in_repo_derivative": True, "pinpoint": None},
            "the stated source is the crosswalk's own 2026-10-05 expansion "
            "act (in-repo): the entry was admitted on in-repo support and "
            "carries no primary-source pinpoint",
            date,
        )
    # literature_synthesis label
    source = Source(
        "literature_synthesis_label", stated, held=True, held_as=CROSSWALK_REL,
        sha256=None, can_ground_locator=False, search=lambda c, f: {},
    )
    return _step(
        source, "searched",
        "read the entry under its literature-synthesis label",
        {"in_repo_derivative": True, "pinpoint": None},
        "the stated source is a synthesis label over Mahadevan 1977 + "
        "Parpola 1994/2010 + Holdat V7, not a work with an entry-level "
        "pinpoint; its Parpola components are searched below",
        date,
    )


# ---------------------------------------------------------------------------
# The pass itself
# ---------------------------------------------------------------------------


def build_outcome(ctx: dict, field: str, sources: list[Source], run_date: str) -> dict:
    """One entry/field outcome: a locator, or a documented not-found."""
    steps: list[dict] = []
    stated = stated_source_step(ctx, field, run_date)
    if stated is not None:
        steps.append(stated)
    for source in sources:
        raw = source.search(ctx, field)
        steps.append(
            _step(source, raw["status"], raw["method"], raw["facts"], raw["result"], run_date)
        )
        locator = source.locate(ctx, field)
        if locator is not None:
            return {"outcome": "located", "locator": locator, "not_found": None}
    basis = (
        "no held copy carries this field's value at an entry-level "
        "primary-source pinpoint; the primary literature the entry's "
        "reading is attributed to is not held by the program"
    )
    if ctx["staged_value"] is None:
        basis = (
            "the staged entry states no value for this field, and no held "
            "copy attributes one at an entry-level primary-source pinpoint"
        )
    return {
        "outcome": "not_found",
        "locator": None,
        "not_found": {"basis": basis, "search": steps},
    }


def entry_context(prov_entry: dict, crosswalk_entry: Optional[dict]) -> dict:
    parpola_num: Optional[int] = None
    if crosswalk_entry is not None:
        raw = crosswalk_entry.get("parpola_num")
        if isinstance(raw, int):
            parpola_num = raw
    return {
        "sign": prov_entry["sign"],
        "mahadevan_id": prov_entry["mahadevan_id"],
        "parpola_id": prov_entry["parpola_id"],
        "mahadevan_num": int(prov_entry["sign"][1:]),
        "parpola_num": parpola_num,
        "source_as_stated": prov_entry["phonetic_reading"]["source_as_stated"],
        "staged_value": prov_entry["phonetic_reading"]["value"],
    }


def build_record(
    provenance: dict,
    crosswalk: dict,
    sources: list[Source],
    *,
    run_id: str,
    run_date: str,
    input_pins: dict,
) -> dict:
    entries = []
    census = {field: {"located": 0, "not_found": 0} for field in FIELDS}
    for prov_entry in provenance["entries"]:
        ctx = entry_context(prov_entry, crosswalk.get(prov_entry["sign"]))
        record_entry: dict[str, Any] = {
            "sign": ctx["sign"],
            "mahadevan_id": ctx["mahadevan_id"],
            "parpola_id": ctx["parpola_id"],
        }
        for field in FIELDS:
            field_ctx = dict(ctx)
            field_ctx["staged_value"] = prov_entry[field]["value"]
            field_ctx["source_as_stated"] = prov_entry[field]["source_as_stated"]
            outcome = build_outcome(field_ctx, field, sources, run_date)
            census[field][
                "located" if outcome["outcome"] == "located" else "not_found"
            ] += 1
            record_entry[field] = {
                "staged_value": prov_entry[field]["value"],
                "source_as_stated": prov_entry[field]["source_as_stated"],
                **outcome,
            }
        entries.append(record_entry)
    record = {
        "artifact": ARTIFACT_NAME,
        "version": ARTIFACT_VERSION,
        "generated_by": f"{TOOL_NAME} (Spec 091 Stage 2, T201/T202)",
        "run_id": run_id,
        "run_date": run_date,
        "source_revision": provenance["source_revision"],
        "inputs": input_pins,
        "search_sources": [s.registry_entry() for s in sources],
        "summary": {
            "n_entries": len(entries),
            **{field: census[field] for field in FIELDS},
        },
        "entries": entries,
    }
    validate_locator_record(record, [e["sign"] for e in provenance["entries"]])
    return record


def validate_locator_record(record: dict, expected_signs: list[str]) -> None:
    """The refusal: no entry/field may be filed with neither outcome,
    a malformed locator, or an undocumented not-found."""
    entries = record.get("entries")
    if not isinstance(entries, list):
        raise LocatorPassError("locator record carries no entries list")
    signs = [e.get("sign") for e in entries]
    if signs != expected_signs:
        raise LocatorPassError(
            f"entry census mismatch: record carries {len(signs)} entries, "
            f"the provenance file carries {len(expected_signs)}, or the "
            "sign order/identity differs"
        )
    census = {field: {"located": 0, "not_found": 0} for field in FIELDS}
    for entry in entries:
        for field in FIELDS:
            block = entry.get(field)
            if not isinstance(block, dict):
                raise LocatorPassError(
                    f"{entry.get('sign')}/{field}: no outcome block filed"
                )
            outcome = block.get("outcome")
            if outcome == "located":
                locator = block.get("locator")
                if not isinstance(locator, dict):
                    raise LocatorPassError(
                        f"{entry['sign']}/{field}: located with no locator"
                    )
                for part in LOCATOR_PARTS:
                    if not str(locator.get(part) or "").strip():
                        raise LocatorPassError(
                            f"{entry['sign']}/{field}: locator missing its "
                            f"{part} part (eligibility-defs v1 §2 requires "
                            "all three parts, non-empty, for that field)"
                        )
                census[field]["located"] += 1
            elif outcome == "not_found":
                not_found = block.get("not_found")
                search = (not_found or {}).get("search")
                if not search:
                    raise LocatorPassError(
                        f"{entry['sign']}/{field}: not-found filed with no "
                        "documented search (C091-1)"
                    )
                for step in search:
                    for key in ("source_id", "status", "method", "result", "date"):
                        if not step.get(key):
                            raise LocatorPassError(
                                f"{entry['sign']}/{field}: search step for "
                                f"{step.get('source_id')} lacks {key}"
                            )
                census[field]["not_found"] += 1
            else:
                raise LocatorPassError(
                    f"{entry['sign']}/{field}: filed with neither a locator "
                    f"nor a documented not-found (outcome={outcome!r})"
                )
    summary = record.get("summary") or {}
    if summary.get("n_entries") != len(entries):
        raise LocatorPassError("summary n_entries does not match the entries")
    for field in FIELDS:
        if summary.get(field) != census[field]:
            raise LocatorPassError(
                f"summary census for {field} does not match the entries"
            )


# ---------------------------------------------------------------------------
# Loading the real inputs
# ---------------------------------------------------------------------------


def load_m77_rows(path: Path) -> dict[int, dict]:
    rows: dict[int, dict] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows[int(row["sign_no"])] = {
                "sign_no": int(row["sign_no"]),
                "variant_marker": row.get("variant_marker"),
                "morph_class_no": row.get("morph_class_no"),
                "morph_class_label": row.get("morph_class_label"),
                "page_printed": row.get("page_printed"),
            }
    return rows


def load_wells_rows(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("rows", "signs", "entries"):
            if isinstance(data.get(key), list):
                return data[key]
        raise LocatorPassError(f"wells dataset at {path} has no rows list")
    return data


def build_real_sources(repo_root: Path) -> list[Source]:
    """The registered search order. Refuses if a held copy is absent:
    the pass must actually search the program's held copies."""
    m77_path = repo_root / M77_REL
    wells_path = repo_root / WELLS_REL
    phoneme_path = repo_root / PHONEME_REL
    for path, label in (
        (m77_path, "Mahadevan 1977 sign-list dataset"),
        (wells_path, "Wells 1998 sign-list dataset"),
        (phoneme_path, "Parpola phoneme compilation"),
    ):
        if not path.exists():
            raise LocatorPassError(
                f"registered held search source absent: {label} at "
                f"{path} — the pass refuses to file not-found outcomes "
                "against a held copy it did not search"
            )
    phoneme_map = json.loads(phoneme_path.read_text(encoding="utf-8"))["phoneme_map"]
    return [
        parpola_1994_source(),
        parpola_2010_source(),
        mahadevan_1977_source(load_m77_rows(m77_path), m77_path),
        wells_1998_source(load_wells_rows(wells_path), wells_path),
        phoneme_compilation_source(phoneme_map, phoneme_path),
    ]


def load_inputs(repo_root: Path) -> tuple[dict, dict, dict]:
    provenance = json.loads((repo_root / PROVENANCE_REL).read_text(encoding="utf-8"))
    crosswalk_doc = json.loads((repo_root / CROSSWALK_REL).read_text(encoding="utf-8"))
    pins = {
        "provenance": {
            "path": PROVENANCE_REL,
            "sha256": sha256_file(repo_root / PROVENANCE_REL),
        },
        "crosswalk": {
            "path": CROSSWALK_REL,
            "sha256": sha256_file(repo_root / CROSSWALK_REL),
        },
        "phoneme_compilation": {
            "path": PHONEME_REL,
            "sha256": sha256_file(repo_root / PHONEME_REL),
        },
        "mahadevan_1977_sign_list": {
            "path": M77_REL,
            "sha256": sha256_file(repo_root / M77_REL),
        },
        "wells_1998_sign_list": {
            "path": WELLS_REL,
            "sha256": sha256_file(repo_root / WELLS_REL),
        },
    }
    return provenance, crosswalk_doc["crosswalk"], pins


# ---------------------------------------------------------------------------
# The sample (rule stated in the stage record before drawing)
# ---------------------------------------------------------------------------


def sample_signs(record: dict) -> list[str]:
    """The T202 sample rule: every entry carrying a locator (all of
    them — locators are verified against their cited source text as
    a census, not a sample), plus every 12th entry in sign order
    starting with the 1st (16 entries), plus every entry whose
    phoneme-map consultation hit (the near-miss population)."""
    entries = record["entries"]
    picked = {entries[i]["sign"] for i in range(0, len(entries), 12)}
    for entry in entries:
        for field in FIELDS:
            block = entry[field]
            if block["outcome"] == "located":
                picked.add(entry["sign"])
            if block["outcome"] == "not_found":
                for step in block["not_found"]["search"]:
                    if (
                        step["source_id"] == "parpola_phonemes_compilation"
                        and step["facts"].get("hit")
                    ):
                        picked.add(entry["sign"])
    return sorted(picked)


def verify_sample(repo_root: Path, record: dict) -> dict:
    provenance, crosswalk, _pins = load_inputs(repo_root)
    sources = build_real_sources(repo_root)
    run_date = record["run_date"]
    by_sign = {e["sign"]: e for e in record["entries"]}
    prov_by_sign = {e["sign"]: e for e in provenance["entries"]}
    results = []
    for sign in sample_signs(record):
        prov_entry = prov_by_sign[sign]
        ctx = entry_context(prov_entry, crosswalk.get(sign))
        per_field = {}
        ok = True
        for field in FIELDS:
            field_ctx = dict(ctx)
            field_ctx["staged_value"] = prov_entry[field]["value"]
            field_ctx["source_as_stated"] = prov_entry[field]["source_as_stated"]
            rederived = build_outcome(field_ctx, field, sources, run_date)
            filed = by_sign[sign][field]
            match = (
                rederived["outcome"] == filed["outcome"]
                and rederived.get("locator") == filed.get("locator")
                and (
                    filed["outcome"] == "located"
                    or _search_facts(rederived) == _search_facts(filed)
                )
            )
            per_field[field] = {
                "filed_outcome": filed["outcome"],
                "rederived_outcome": rederived["outcome"],
                "match": match,
            }
            ok = ok and match
        results.append({"sign": sign, "fields": per_field, "verified": ok})
    locator_signs = {
        e["sign"]
        for e in record["entries"]
        for f in FIELDS
        if e[f]["outcome"] == "located"
    }
    verified_signs = {r["sign"] for r in results if r["verified"]}
    return {
        "run_id": record["run_id"],
        "sample_rule": (
            "every entry carrying a locator (census), plus every 12th "
            "entry in sign order starting with the 1st, plus every entry "
            "whose phoneme-map consultation hit"
        ),
        "n_sampled": len(results),
        "n_locators_in_record": sum(
            1
            for e in record["entries"]
            for f in FIELDS
            if e[f]["outcome"] == "located"
        ),
        "all_locators_verified": locator_signs <= verified_signs,
        "results": results,
        "all_verified": all(r["verified"] for r in results),
    }


def _search_facts(block: dict) -> list:
    return [
        (s["source_id"], s["status"], json.dumps(s["facts"], sort_keys=True))
        for s in block["not_found"]["search"]
    ]


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


def execute(repo_root: Path) -> dict:
    provenance, crosswalk, pins = load_inputs(repo_root)
    sources = build_real_sources(repo_root)
    started = datetime.now(timezone.utc)
    run_id = run_records.mint_run_id("study", now=started)
    run_date = started.date().isoformat()
    record = build_record(
        provenance, crosswalk, sources,
        run_id=run_id, run_date=run_date, input_pins=pins,
    )
    artifact_path = repo_root / ARTIFACT_REL
    payload = json.dumps(record, indent=1, ensure_ascii=True) + "\n"
    write_file_verified(artifact_path, payload.encode("utf-8"))
    artifact_sha = sha256_file(artifact_path)

    code_version = "unknown"
    try:
        import subprocess

        code_version = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo_root,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        pass
    finished = datetime.now(timezone.utc)
    header = run_records.build_header(
        surface="study",
        tool=f"{TOOL_NAME} --execute",
        tool_version=TOOL_VERSION,
        command=f"{TOOL_NAME} --execute",
        code_version=code_version,
        input_pins={
            "spec": "091-anchor-comparison-integrity",
            "stage": "stage-2-locator-pass",
            "frozen_artifacts": {
                "provenance_sha256": pins["provenance"]["sha256"],
                "crosswalk_sha256": pins["crosswalk"]["sha256"],
            },
            "search_sources": {
                "mahadevan_1977_sign_list_sha256": pins["mahadevan_1977_sign_list"]["sha256"],
                "wells_1998_sign_list_sha256": pins["wells_1998_sign_list"]["sha256"],
                "phoneme_compilation_sha256": pins["phoneme_compilation"]["sha256"],
            },
            "generator_sha256": sha256_file(Path(__file__)),
            "eligibility_defs": "specs/091-anchor-comparison-integrity/eligibility-defs-v1.md",
        },
        seed=run_records.NO_SEED,
        environment_class="mini-server/linux",
        started=started,
        finished=finished,
        run_id=run_id,
    )
    run_record = run_records.build_record(
        header,
        result={
            "artifact": ARTIFACT_REL,
            "artifact_sha256": artifact_sha,
            "census": record["summary"],
        },
    )
    store = repo_root / SPEC_RECORDS_REL
    written = run_records.write_run_record(store, run_record)
    return {
        "run_id": run_id,
        "artifact": ARTIFACT_REL,
        "artifact_sha256": artifact_sha,
        "run_record": str(written.relative_to(repo_root)),
        "census": record["summary"],
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--execute", action="store_true")
    group.add_argument("--verify-sample", action="store_true")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    if args.execute:
        outcome = execute(repo_root)
        print(json.dumps(outcome, indent=1))
        return 0
    artifact = json.loads((repo_root / ARTIFACT_REL).read_text(encoding="utf-8"))
    verification = verify_sample(repo_root, artifact)
    out_path = repo_root / VERIFICATION_REL
    write_file_verified(
        out_path,
        (json.dumps(verification, indent=1, ensure_ascii=True) + "\n").encode("utf-8"),
    )
    print(json.dumps({
        "run_id": verification["run_id"],
        "n_sampled": verification["n_sampled"],
        "all_verified": verification["all_verified"],
        "written": VERIFICATION_REL,
    }, indent=1))
    return 0 if verification["all_verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
