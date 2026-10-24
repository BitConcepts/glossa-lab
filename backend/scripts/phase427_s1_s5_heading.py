"""Phase-427 (Spec 065) — the two unlocated rows of
Spec 057: search the acquired documents' own text
layers for the heading (successor recovery act for
S-1 and S-5).

Execution of the frozen Spec 065 contract (freeze
digest f50a6e9c...; OSF registration 34s9u, approved
+ public before the run): step 0 gates in frozen
order (0.1 input integrity under the Spec 038
claims-store form; 0.2 the acquired S-5 file asserted
by size, SHA-256, and MD5 on the local file; 0.3 the
S-1 intake determination; 0.4 order), then the S-5
document-layer search (spec section 4.1) on the
pinned acquired file under Spec 057 section 5's
heading rule, carried verbatim in substance, and the
S-1 row under the frozen two-arm contract of section
4.2 (searched only on the intake-pinned search arm;
otherwise STILL UNLOCATED — ACQUISITION BLOCKED).

Terminal accounting (executor judgements, evidence
asserted in this script and quoted in the outcome
record):
  S-1 STILL UNLOCATED — ACQUISITION BLOCKED
      (no intake-S1.json before the run; the blocker
      record stands as the row's evidence)
  S-5 HEADING ABSENT FROM DOCUMENT
      (exactly one occurrence in the acquired file's
      text layer — extraction line 340, PDF page 9,
      sentence-initial inside a running paragraph of
      section 5.5 — not in heading form)
Headline class B — S-5 RESOLVED, S-1 STILL BLOCKED
(spec section 7). Disposition: the heading record
stands superseded-not-retired, by appended dated
note only (the append is a separate executor act
recorded in the outcome record, as in Spec 057).

The script is deterministic over its pinned inputs:
a second run on the same host reproduces its outputs
byte-identically. The acquired S-5 file lives in the
local research store only (spec section 2.2); on a
host without it the run closes at step 0, gate 0.2,
and never substitutes other bytes.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs/065-s1-s5-heading-successor"
FREEZE = json.loads((SPEC_DIR / "freeze.json").read_text("utf-8"))
FREEZE_DIGEST = FREEZE["digest"]
assert FREEZE_DIGEST == (
    "f50a6e9c45d96fe15e737ee83a46b83c2c7e150e4a29421ccb5ec2be7a428c09"
)
DEF = FREEZE["definition"]
DESIGN = DEF["design"]
ROWS = {r["source"]: r for r in DESIGN["rows"]}
CANON_ID = DESIGN["claim_under_test"]["id"]
FINGERPRINT = DESIGN["claim_under_test"]["fingerprint"]
ACQ = DESIGN["acquired_s5"]
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
RESULTS_PATH = REPO / "reports/phase427_results.json"
REPORT_PATH = REPO / "reports/phase427_s1_s5_report.md"
EXTRACTION_PATH = SPEC_DIR / "extraction-S5.txt"
INTAKE_S1 = SPEC_DIR / "intake-S1.json"
FENCE = ("This act searched two documents for a heading. "
         "It checked nothing either passage states.")
DATE = "2026-10-22"

# The acquired S-5 file, at its section 2.2 local path
# (local research store; never committed).
ACQUIRED_S5 = (
    Path.home() / "workspace" / "research_notes"
    / "indus-data-deep-sweep-20261008" / "downloads"
    / "hunt-without-kings-zenodo-2025" / ACQ["filename"])
PROVENANCE_MD = (
    Path.home() / "workspace" / "research_notes"
    / "indus-data-deep-sweep-20261008" / "downloads"
    / "PROVENANCE.md")
BLOCKED_MD = (
    Path.home() / "workspace" / "research_notes"
    / "indus-data-deep-sweep-20261008" / "downloads"
    / "fuls-studies-on-indus-script-2020" / "BLOCKED.md")

# Section 2.3 record-input pins (freeze.md section 2).
RECORD_PINS = {
    "spec057_freeze_record": (
        "specs/057-five-sources-heading/freeze.json",
        "3cc68c372790d6bd62d9ab1bb43b15ec2f43502dd614150d660d33b4c452d8af"),
    "spec057_outcome": (
        "specs/057-five-sources-heading/outcome.md",
        "d3ae1325bdba52295bd44990db024957c1d3aceeb462ddbf60af73b512834a58"),
    "spec057_spec": (
        "specs/057-five-sources-heading/spec.md",
        "0798d51aac680c981fe38bf45761358231957391b67cd24228b5cba675ec9e8d"),
    "spec057_adjudication": (
        "specs/057-five-sources-heading/adjudication.md",
        "041880706d9ebae2c1a30a5dae8cd2066d915317fb551d46af469dd2fd4ec017"),
    "anchors": (
        ANCHORS_REL,
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"),
}

# Executor judgement for the S-5 search (spec sections
# 4.1 / 5.1), asserted below against the extraction
# produced from the pinned bytes: exactly one
# occurrence, extraction line 340, PDF page 9, inside
# a running sentence of section 5.5 ("...waterworks.
# Positional analysis / shows a clear tripartite
# administrative grammar:") — a mention inside a
# running sentence, sentence-initial only because it
# follows a full stop; not standing alone, not a
# numbered heading, and no table-of-contents entry
# (the extraction carries no other occurrence).
S5_OCCURRENCE_LINES = [340]
S5_OCCURRENCE_PAGES = [9]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def find_claim(node, claim_id):
    if isinstance(node, dict):
        if node.get("claim_id") == claim_id:
            return node
        for value in node.values():
            found = find_claim(value, claim_id)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_claim(value, claim_id)
            if found is not None:
                return found
    return None


def extract_text_layer(pdf: Path) -> bytes:
    """The pinned file's own text layer, extracted in
    full with pdftotext -layout (the tool and settings
    of the Item 6 provenance extraction, which this
    extraction reproduces: 2,273 lines, 84,672 bytes).
    """
    out = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True, timeout=600, check=True)
    return out.stdout


def occurrence_list(text: str) -> list[dict]:
    """Every occurrence of 'positional analysis'
    (case-insensitive), with its page (PDF page, from
    the form-feed page breaks of the layout
    extraction) and its extraction line. No occurrence
    is pre-filtered (spec section 4.1 step 3)."""
    pages = text.split("\f")
    found = []
    line_no = 0
    for page_idx, page in enumerate(pages, start=1):
        for line in page.splitlines():
            line_no += 1
            if "positional analysis" in line.lower():
                found.append({
                    "extraction_line": line_no,
                    "page": page_idx,
                    "line_text": line,
                })
    return found


def main() -> int:
    anchors_before = sha256((REPO / ANCHORS_REL).read_bytes())
    results: dict = {
        "spec": "065",
        "phase": "Phase-427",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": "34s9u",
        "date": DATE,
        "fence": FENCE,
    }
    gates = []

    # ── Gate 0.1: input integrity ──────────────────────
    pin_rows = {}
    gate_01_ok = True
    for sid in ("S-1", "S-5"):
        source = ROWS[sid]
        doc_id = source["document_id"]
        text_raw = (REPO / "glossa-indus/processed/cleaned_text"
                    / f"{doc_id}.txt").read_bytes()
        reg_raw = (REPO / "glossa-indus/literature/documents"
                   / f"{doc_id}.json").read_bytes()
        claims_raw = (
            REPO / "glossa-indus/claims/extracted_claims"
            / f"{doc_id}.json").read_bytes()
        entry = find_claim(json.loads(claims_raw),
                           source["claim_id"])
        registry = json.loads(reg_raw)
        facts_ok = (
            entry is not None
            and entry["proposition_fingerprint"] == FINGERPRINT
            and entry["claim_status"] == "untested"
            and entry["stage"] == "created"
            and entry["quote_fragment"]
            == source["quote_fragment"]
            and registry["original_filename"]
            == source["document_filename"]
            and registry["file_size_bytes"]
            == source["document_size_bytes"]
            and registry["checksum_sha256"]
            == source["document_checksum_sha256"]
            and (sid == "S-1"
                 or entry.get("merged_into") == CANON_ID))
        if sid == "S-1":
            # The canonical record's merged_into posture
            # as Spec 057 left it: exactly the four
            # recorded evidence instances, each pointing
            # at the canonical record.
            instances = entry["evidence_instances"]
            facts_ok &= (
                [i["claim_id"] for i in instances] == [
                    "fuls2023_catalog_of_indussigns_searchins"
                    "_1dbdecdb_statisti_0001",
                    "positional_analysis_of_indus_signs"
                    "_a2bedc93_statisti_0001",
                    "the_archaeology_and_epigraphy_of_indus_w"
                    "_27f45a68_statisti_0003",
                    "without_kings_or_conquests_the_indus_scr"
                    "_ce9d98cc_statisti_0002",
                ]
                and all(
                    i["record"]["merged_into"] == CANON_ID
                    and i["record"]["proposition_fingerprint"]
                    == FINGERPRINT for i in instances))
        row = {
            "cleaned_text_sha256": sha256(text_raw),
            "cleaned_text_match": (
                sha256(text_raw)
                == source["cleaned_text_sha256"]),
            "registry_sha256": sha256(reg_raw),
            "registry_match": (
                sha256(reg_raw)
                == source["registry_file_sha256"]),
            "claims_file_live_sha256": sha256(claims_raw),
            "claims_file_freeze_constant": (
                source["claims_file_freeze_constant"]),
            "claims_entry_facts_match": facts_ok,
            "claims_store_note": (
                "per freeze.md section 2 (the Spec 038 form), "
                "the extracted-claims store is asserted by its "
                "entries' facts, never by live-file hash; the "
                "live hash is recorded here for the record"),
        }
        pin_rows[sid] = row
        gate_01_ok &= (
            row["cleaned_text_match"] and row["registry_match"]
            and facts_ok)
    record_rows = {}
    for key, (rel, exp) in RECORD_PINS.items():
        observed = sha256((REPO / rel).read_bytes())
        record_rows[key] = {"file": rel, "sha256": observed,
                            "match": observed == exp}
        gate_01_ok &= observed == exp
    # Spec 057's freeze digest recomputes as recorded.
    freeze057 = json.loads(
        (REPO / "specs/057-five-sources-heading/freeze.json")
        .read_text("utf-8"))
    gate_01_ok &= freeze057["digest"] == (
        "237b923a2c19b216e0476f70d17a956db0ca68d1ba8af6902109099a82c820d9")
    gates.append({
        "gate": "0.1", "name": "input integrity",
        "verdict": "PASS" if gate_01_ok else "FAIL",
        "pins": pin_rows, "record_inputs": record_rows,
        "spec057_freeze_digest_recomputed": freeze057["digest"],
    })
    if not gate_01_ok:
        results["outcome"] = ("CLOSED AT STEP 0 — INPUT PIN "
                              "MISMATCH")
        results["step0_gates"] = gates
        _write(results, [])
        return 0

    # ── Gate 0.2: acquired-file assertion (S-5) ────────
    acq_present = ACQUIRED_S5.is_file()
    acq_row = {"path": str(ACQUIRED_S5),
               "present": acq_present}
    gate_02_ok = False
    if acq_present:
        acq_bytes = ACQUIRED_S5.read_bytes()
        acq_row.update({
            "size_bytes": len(acq_bytes),
            "sha256": sha256(acq_bytes),
            "md5": md5(acq_bytes),
            "expected_size_bytes": ACQ["size_bytes"],
            "expected_sha256": ACQ["sha256"],
            "expected_md5": ACQ["md5"],
        })
        gate_02_ok = (
            len(acq_bytes) == ACQ["size_bytes"]
            and acq_row["sha256"] == ACQ["sha256"]
            and acq_row["md5"] == ACQ["md5"])
    gates.append({
        "gate": "0.2", "name": "acquired-file assertion (S-5)",
        "verdict": "PASS" if gate_02_ok else "FAIL",
        "acquired_file": acq_row,
        "note": ("the search is never run on substitute "
                 "bytes, and the held cleaned text is never "
                 "substituted for the acquired document"),
    })
    if not gate_02_ok:
        results["outcome"] = ("CLOSED AT STEP 0 — INPUT PIN "
                              "MISMATCH (the acquired input)")
        results["step0_gates"] = gates
        _write(results, [])
        return 0

    # ── Gate 0.3: S-1 intake determination ─────────────
    intake_exists = INTAKE_S1.is_file()
    determination = {
        "intake_record": ("specs/065-s1-s5-heading-successor/"
                          "intake-S1.json"),
        "intake_record_exists": intake_exists,
    }
    gate_03_ok = True
    if intake_exists:
        # Search arm: the pinned document must verify.
        intake = json.loads(INTAKE_S1.read_text("utf-8"))
        doc = Path(intake["local_path"])
        ok = (doc.is_file()
              and sha256(doc.read_bytes()) == intake["sha256"]
              and doc.stat().st_size == intake["size_bytes"])
        determination.update({
            "arm": "search arm",
            "intake": intake,
            "document_verifies": ok,
        })
        gate_03_ok = ok
    else:
        # Blocked arm: the determination's evidence,
        # re-read at step 0 on this host.
        provenance = PROVENANCE_MD.read_text("utf-8")
        s1_sections = provenance.split(
            "## S-1 acquisition attempt", 1)[1]
        folder_files = sorted(
            p.name for p in BLOCKED_MD.parent.iterdir()
            if p.is_file())
        determination.update({
            "arm": "blocked arm",
            "evidence": {
                "provenance_s1_sections_state": (
                    "no file acquired, no provenance entry "
                    "taken (acquisition-attempt section, "
                    "2026-10-21; follow-up section, "
                    "2026-10-22: ILL portion-copy request "
                    "placed and pending, still no file "
                    "acquired)"),
                "provenance_states_no_entry_taken": (
                    "no provenance entry taken" in s1_sections),
                "provenance_states_ill_pending": (
                    "ILL portion-copy request" in s1_sections
                    and "still no file acquired"
                    in s1_sections),
                "blocker_record": (
                    "downloads/fuls-studies-on-indus-script"
                    "-2020/BLOCKED.md (Academia.edu sign-in "
                    "wall; owner account act)"),
                "s1_download_folder_files": folder_files,
                "delivered_s1_file_in_downloads_tree": (
                    folder_files != ["BLOCKED.md"]),
                "note": ("no S-1 document has been handed "
                         "over and pinned by an append-only "
                         "intake record before the run; the "
                         "Oakland ILL portion-copy request "
                         "placed 2026-10-22 is pending and "
                         "nothing delivered under it has "
                         "been intake-pinned"),
            },
        })
        gate_03_ok = (
            determination["evidence"][
                "provenance_states_no_entry_taken"]
            and not determination["evidence"][
                "delivered_s1_file_in_downloads_tree"])
    gates.append({
        "gate": "0.3", "name": "S-1 intake determination",
        "verdict": "PASS" if gate_03_ok else "FAIL",
        "determination": determination,
    })
    if not gate_03_ok:
        results["outcome"] = ("CLOSED AT STEP 0 — INPUT PIN "
                              "MISMATCH (the S-1 intake record)")
        results["step0_gates"] = gates
        _write(results, [])
        return 0
    gates.append({
        "gate": "0.4", "name": "order",
        "verdict": "PASS",
        "note": ("gate verdicts are recorded in this "
                 "results record and in the outcome record "
                 "before the first per-source row; no text "
                 "layer was searched and no passage was "
                 "read for content before gates 0.1–0.3 "
                 "passed"),
    })
    results["step0_gates"] = gates

    # ── The searches and the accounting (sections 4–6) ─
    rows = []

    # S-1 row (section 2.1 order: S-1 first).
    s1 = ROWS["S-1"]
    s1_row: dict = {
        "source": "S-1",
        "citation": s1["citation"],
        "claim_id": s1["claim_id"],
        "document_id": s1["document_id"],
        "quote_fragment": s1["quote_fragment"],
    }
    if determination["arm"] == "blocked arm":
        s1_row.update({
            "document_searched": None,
            "blocker_ref": (
                "local research store: downloads/"
                "fuls-studies-on-indus-script-2020/"
                "BLOCKED.md; PROVENANCE.md S-1 sections "
                "after entry 23 (no provenance entry taken)"),
            "locator": None,
            "occurrence_list": None,
            "outcome": ("STILL UNLOCATED — ACQUISITION "
                        "BLOCKED"),
            "evidence_ref": (
                "the blocker record itself (gate 0.3 "
                "determination): no intake-S1.json before "
                "the run, no delivered S-1 file in the "
                "downloads tree, the ILL portion-copy "
                "request of 2026-10-22 pending with "
                "nothing intake-pinned"),
            "unblocking_act": (
                "The owner account act named in the "
                "blocker record: a copy of the chapter "
                "handed over by the owner (his own "
                "download, or a copy delivered through "
                "the fallback interlibrary-loan route) "
                "and pinned by the append-only intake "
                "record intake-S1.json before a later "
                "run. This successor contacts no one, "
                "creates no account, and sends no "
                "request (spec section 9.6)."),
        })
    else:
        # Search arm (not taken by this run): the
        # intake-pinned document's text layer is
        # searched exactly as S-5's is, under section
        # 5's rule, with every occurrence listed and
        # judged on the row.
        intake = determination["intake"]
        doc_bytes = Path(intake["local_path"]).read_bytes()
        text = extract_text_layer(
            Path(intake["local_path"])).decode(
                "utf-8", errors="replace")
        occ = occurrence_list(text)
        heading_form = [
            o for o in occ
            if o["line_text"].strip().lower()
            in ("positional analysis",
                "statistical finding: positional analysis")
            or o["line_text"].strip().lower().startswith(
                ("chapter", "appendix"))]
        s1_row.update({
            "document_searched": intake["sha256"],
            "locator": occ,
            "occurrence_list": occ,
            "outcome": ("HEADING FOUND" if heading_form
                        else "HEADING ABSENT FROM DOCUMENT"),
            "evidence_ref": intake["sha256"],
        })
    rows.append(s1_row)

    # S-5 row: search the acquired document's text
    # layer (section 4.1).
    s5 = ROWS["S-5"]
    extraction = extract_text_layer(ACQUIRED_S5)
    EXTRACTION_PATH.write_bytes(extraction)
    text = extraction.decode("utf-8", errors="replace")
    occ = occurrence_list(text)
    # Newline-delimited lines (the extraction's own line
    # numbering, as grep / wc report it): splitlines()
    # would also split on the extraction's form-feed
    # page breaks and shift every locator.
    plain_lines = text.split("\n")
    if plain_lines and plain_lines[-1].strip("\f \t") == "":
        # Trailing remainder after the last newline: the
        # final page's form feed only — not a text line.
        plain_lines.pop()
    # Assert the executor's judgement anchors on the
    # extraction produced from the pinned bytes.
    assert [o["extraction_line"] for o in occ] == (
        S5_OCCURRENCE_LINES), occ
    assert [o["page"] for o in occ] == S5_OCCURRENCE_PAGES
    occ_line = plain_lines[S5_OCCURRENCE_LINES[0] - 1]
    next_line = plain_lines[S5_OCCURRENCE_LINES[0]]
    assert "waterworks. Positional analysis" in occ_line
    assert next_line.strip().startswith(
        "shows a clear tripartite administrative grammar")
    # The occurrence's containing section is 5.5
    # "Governance and Civic Authority" (extraction
    # line 336), a numbered section heading that does
    # not contain the string; the occurrence stands
    # inside that section's "Findings." paragraph.
    assert "5.5 Governance and Civic Authority" in (
        plain_lines[335])
    judged = [{
        **o,
        "judgement": (
            "NOT the heading (spec section 5.1): a "
            "mention inside a running sentence — it "
            "begins mid-line, after '...fortified "
            "gates, and waterworks.', is capitalised "
            "only as a sentence start, and its sentence "
            "runs on to the next line ('shows a clear "
            "tripartite administrative grammar:'). It "
            "does not stand alone as a line or running "
            "head, carries no chapter/appendix "
            "numbering as a title, and is not a "
            "table-of-contents entry (the extraction "
            "carries no other occurrence of the "
            "string)."),
        "containing_section": (
            "5.5 Governance and Civic Authority "
            "(extraction line 336); the occurrence "
            "stands in that section's 'Findings.' "
            "running paragraph"),
        "heading_form": False,
    } for o in occ]
    s5_row: dict = {
        "source": "S-5",
        "citation": s5["citation"],
        "claim_id": s5["claim_id"],
        "document_id": s5["document_id"],
        "quote_fragment": s5["quote_fragment"],
        "document_searched": ACQ["sha256"],
        "extraction": {
            "tool": "pdftotext -layout (poppler), the "
                    "acquired file's own text layer "
                    "extracted in full from the pinned "
                    "bytes",
            "artifact": ("specs/065-s1-s5-heading-"
                         "successor/extraction-S5.txt"),
            "sha256": sha256(extraction),
            "bytes": len(extraction),
            "lines": len(plain_lines),
        },
        "occurrence_list": judged,
        "locator": {
            "occurrence_extraction_lines": (
                S5_OCCURRENCE_LINES),
            "occurrence_pages": S5_OCCURRENCE_PAGES,
            "note": ("locators are the extraction's "
                     "line numbers and the PDF page "
                     "numbers of the layout extraction"),
        },
        "outcome": "HEADING ABSENT FROM DOCUMENT",
        "evidence_ref": (
            "the searched file's SHA-256 "
            "77f10f3279454bede1ba60a04f3c099500667ca625"
            "74b07aaabb9fc69bf94665 (the acquired "
            "file, gate 0.2) and the extraction "
            "artifact at SHA-256 "
            + sha256(extraction)),
        "difference_from_held_text": (
            "None in posture: Spec 057 outcome section "
            "4.2 recorded one occurrence in the held "
            "cleaned text (line 267, sentence-initial "
            "inside a running paragraph of section "
            "5.5, not in heading form); the acquired "
            "document's text layer carries the same "
            "single occurrence, in the same sentence "
            "of the same section, likewise not in "
            "heading form. The successor's finding "
            "rests on the acquired file, not the held "
            "text (DD-065-3)."),
    }
    rows.append(s5_row)
    results["accounting"] = rows

    # ── Headline and disposition (section 7) ──────────
    s5_outcome = s5_row["outcome"]
    s1_outcome = s1_row["outcome"]
    resolved = ("HEADING FOUND", "HEADING ABSENT FROM DOCUMENT")
    if s1_outcome in resolved and s5_outcome in resolved:
        headline_class = "A — BOTH SOURCES RESOLVED"
        headline = (
            "Both of Spec 057's unlocated rows are "
            "resolved on the documents themselves. "
            f"S-1: [{s1_outcome}]. S-5: [{s5_outcome}, "
            "evidence the acquired file at SHA-256 "
            f"{ACQ['sha256']}]. Each resolution rests "
            "on the pinned document named on its row, "
            "searched under Spec 057 section 5's "
            "heading rule. No finding is attributed to "
            "either source beyond what its own row "
            "records.")
    else:
        headline_class = ("B — S-5 RESOLVED, S-1 STILL "
                          "BLOCKED")
        headline = (
            "One of Spec 057's two unlocated rows is "
            "resolved on the document itself. S-5: "
            "HEADING ABSENT FROM DOCUMENT (no "
            "sub-result; no claim recovered — the "
            "row's evidence is the searched file's "
            "hash and its single judged occurrence), "
            "on the acquired file at SHA-256 "
            f"{ACQ['sha256']}. S-1 remains STILL "
            "UNLOCATED — ACQUISITION BLOCKED: no "
            "document was handed over before the run, "
            "no search was run for S-1, and nothing "
            "about the chapter is found or implied. "
            "The unblocking act remains the owner "
            "account act named on S-1's row.")
    disposition = (
        "superseded-not-retired (class B): the heading "
        "record stands exactly as Spec 057 left it — "
        "superseded by Spec 057's two recovered claims, "
        "not retired. The appended, dated note records "
        "S-5's resolution (HEADING ABSENT FROM "
        "DOCUMENT, on the acquired file at SHA-256 "
        f"{ACQ['sha256']}) and S-1's blocked posture "
        "(STILL UNLOCATED — ACQUISITION BLOCKED), and "
        "states that retirement is not available while "
        "S-1 remains unlocated (spec section 7.2).")
    results["headline_class"] = headline_class
    results["headline"] = headline
    results["disposition"] = disposition
    results["outcome"] = headline_class
    results["hypothesis_F065_C14"] = (
        "Defeated over the one document actually "
        "searched (S-5: no heading-form occurrence in "
        "its text layer); unjudged as to S-1, which "
        "was never searched — S-5's row alone neither "
        "defeats nor confirms it for S-1 (spec section "
        "1.3).")
    anchors_after = sha256((REPO / ANCHORS_REL).read_bytes())
    results["anchors"] = {
        "file": ANCHORS_REL, "before_sha256": anchors_before,
        "after_sha256": anchors_after,
        "byte_identical": anchors_before == anchors_after}
    assert anchors_before == anchors_after
    _write(results, rows)
    print(f"Phase-427: {headline_class}")
    return 0


def _write(results: dict, rows: list) -> None:
    RESULTS_PATH.write_text(
        json.dumps(results, indent=1, ensure_ascii=False)
        + "\n", encoding="utf-8")
    lines = [
        "# Phase-427 (Spec 065) — report",
        "",
        f"Freeze digest: `{results['freeze_digest']}`. "
        f"OSF registration 34s9u (approved + public "
        f"before the run). Date: {DATE}.",
        "",
        "## Step 0 gates (recorded before any per-source row)",
        "",
    ]
    for gate in results["step0_gates"]:
        lines.append(
            f"- Gate {gate['gate']} ({gate['name']}): "
            f"**{gate['verdict']}**")
    lines += ["", "## Accounting", ""]
    if rows:
        lines.append(
            "| # | Source claim_id | Document searched "
            "or blocker ref | Outcome | Evidence |")
        lines.append("|---|---|---|---|---|")
        for row in rows:
            doc = row.get("document_searched") or row.get(
                "blocker_ref", "")
            lines.append(
                f"| {row['source']} | `{row['claim_id']}` "
                f"| {doc} | {row['outcome']} | "
                f"{row.get('evidence_ref', '')} |")
        lines += [
            "",
            f"## Headline — {results['headline_class']}",
            "",
            results["headline"],
            "",
            f"Disposition: {results['disposition']}",
            "",
        ]
    else:
        lines += [f"Outcome: **{results['outcome']}**", ""]
    lines += [FENCE, ""]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
