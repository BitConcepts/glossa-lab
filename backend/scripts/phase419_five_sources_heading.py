"""Phase-419 (Spec 057) — the heading carried by five sources.

Execution of the frozen Spec 057 contract (freeze digest
237b923a...; OSF registration chq5e, approved + public
before the run): step 0 gates (input integrity under the
Spec 038 claims-store form; source-set integrity), then,
per source in spec section 2.1 order, heading location
under the heading-form rule (DD-057-4), delimitation
(section 5.2, with DD-057-11 for S-3), verbatim passage
artifacts for located passages, and the section 6
accounting — exactly one outcome per source.

Terminal accounting (executor judgements, evidence
asserted in this script and quoted in the outcome
record):
  S-1 SOURCE UNLOCATED (HEADING NOT PRESENT IN HELD TEXT)
  S-2 PASSAGE EMPTY
  S-3 CLAIM RECOVERED
  S-4 CLAIM RECOVERED
  S-5 SOURCE UNLOCATED (HEADING NOT PRESENT IN HELD TEXT)
Counts r=2, e=1, u=2 -> headline class C (spec section 7).

The script is deterministic: a second run reproduces
its outputs byte-identically. It never edits a frozen
record; the section 7.2 disposition append on the
canonical record is a separate executor act recorded
in the outcome record.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs/057-five-sources-heading"
FREEZE = json.loads((SPEC_DIR / "freeze.json").read_text("utf-8"))
FREEZE_DIGEST = FREEZE["digest"]
assert FREEZE_DIGEST == (
    "237b923a2c19b216e0476f70d17a956db0ca68d1ba8af6902109099a82c820d9"
)
DEF = FREEZE["definition"]
SOURCES = DEF["inputs"]["sources"]
CANON_ID = DEF["design"]["claim_under_test"]["id"]
FINGERPRINT = DEF["design"]["claim_under_test"]["fingerprint"]
ANCHORS_REL = DEF["inputs"]["anchors"]["file"]
RESULTS_PATH = REPO / "reports/phase419_results.json"
REPORT_PATH = REPO / "reports/phase419_five_sources_report.md"
FENCE = ("This act recovered what five passages state. "
         "It checked none of it.")
DATE = "2026-10-21"

# Executor location judgements under the heading-form
# rule (spec section 5.1), asserted below against the
# pinned bytes. Line numbers are 1-based.
LOCATION = {
    "S-1": {"heading_form_lines": [], "toc_lines": [],
            "passage": None},
    "S-2": {"heading_form_lines": [536, 612], "toc_lines": [65],
            "heading_text": ("CHAPTER 3. POSITIONAL ANALYSIS "
                             "OF INDUS SIGNS"),
            "passage": [536, 615]},
    "S-3": {"heading_form_lines": [54], "toc_lines": [],
            "heading_text": "Positional Analysis of Indus Signs",
            "passage": [54, 601]},
    "S-4": {"heading_form_lines": [3456], "toc_lines": [86],
            "heading_text": "Positional Analysis of Indus Signs",
            "passage": [3455, 3822]},
    "S-5": {"heading_form_lines": [], "toc_lines": [],
            "passage": None},
}

RECOVERED = {
    "S-3": {
        "intake_file": "intake-S3.json",
        "claim_id": ("fuls2013_positional_analysis_"
                     "057_recovered_0001"),
        "proposition": (
            "Using a normalised weighted sign position (each "
            "sign's position reduced to a standard text length "
            "of ten signs, with sign positions weighted linearly "
            "by the original text length), Indus signs can be "
            "classified by their preferred position as Initial, "
            "Early-Medial, Mid-Medial, Late-Medial, Terminal, "
            "constant, or constant but not initial or not "
            "terminal; doubling, mirroring, hatching, or marking "
            "a sign can change its positional classification; "
            "and signs 382, 790, 832, and 892 are good "
            "candidates for syllables, because syllables should "
            "have an almost constant positional distribution "
            "while logograms and grammatical markers should "
            "fall on restricted syntactic positions."),
        "numbers": [
            "3723 texts of them are complete with 13556 signs",
            ("This leaves 2474 complete and different texts, "
             "reducing also the number of relevant signs to "
             "9700 signs altogether"),
            "The mean text length are 4.01 signs",
            ("Signs 382, 790, 832, and 892 are good candidates "
             "of syllables"),
        ],
        "corpus": (
            "The ICIT database corpus as stated in the passage: "
            "3898 inscribed artefacts and 4791 texts, of which "
            "3723 complete texts with 13556 signs, reduced to "
            "2474 complete and different texts (identical texts "
            "of the same artefact type from the same site "
            "reduced to one; multiple-line texts excluded) with "
            "9700 signs; sign list of B. Wells (2006) with 695 "
            "signs (last update autumn 2009)."),
        "evidence_phrases": [
            "The positional analysis results into different",
            "Signs 382, 790, 832, and 892 are good candidates",
            "doubling, mirroring, hatching, or",
        ],
    },
    "S-4": {
        "intake_file": "intake-S4.json",
        "claim_id": ("wells2015_appendix_ii_positional_analysis_"
                     "057_recovered_0001"),
        "proposition": (
            "The positional analysis results in different "
            "classifications of Indus signs: signs can be "
            "classified as Initial, Early-Medial, Mid-Medial, "
            "Late-Medial, or Terminal; doubling, mirroring, "
            "hatching, or marking an Indus sign can change its "
            "positional classification, most likely indicating "
            "a different function or semantic value of the "
            "modified sign; and signs 382, 790, 832, and 892 "
            "are good candidates for syllabic signs, because "
            "logograms and grammatical markers should be found "
            "in restricted syntactic positions while syllables "
            "should have an almost constant positional "
            "distribution."),
        "numbers": [
            ("a total of 3898 inscribed artefacts (one to "
             "three sided) and 4791 texts"),
            ("3723 texts of them are complete using a total "
             "of 13556 signs"),
            ("This leaves 2474 complete and different texts, "
             "reducing the total number of relevant signs "
             "to 9700 signs"),
            "The mean text length for this sample is 4.01 signs",
            "Signs 382, 790, 832, and 892 are good candidates",
        ],
        "corpus": (
            "The ICIT database corpus as stated in the "
            "appendix: 3898 inscribed artefacts and 4791 "
            "texts, of which 3723 complete texts using 13556 "
            "signs, reduced to 2474 complete and different "
            "texts (identical texts from the same artefact "
            "type and site reduced to a frequency of 1; "
            "multiple-line texts not included) with 9700 "
            "signs; updated sign list from Wells (2006) with "
            "695 signs (last update autumn 2010)."),
        "evidence_phrases": [
            "The positional analysis results in different "
            "classifications of Indus signs",
            "Signs 382, 790, 832, and 892 are good candidates",
            "doubling, mirroring, hatching, or marking of "
            "Indus",
        ],
    },
}

FALSIFIER = (
    "Written from the passage's own logic: on the passage's "
    "stated corpus, recomputing each sign's normalised "
    "weighted positional histogram would fail to separate "
    "signs into the stated positional classes, or doubled, "
    "mirrored, hatched, or marked signs would in every case "
    "keep the positional classification of their unmodified "
    "forms, or signs 382, 790, 832, and 892 would show "
    "restricted rather than almost constant positional "
    "distributions.")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def text_lines(doc_id: str):
    raw = (REPO / "glossa-indus/processed/cleaned_text"
           / f"{doc_id}.txt").read_bytes()
    return raw, raw.decode("utf-8").splitlines(keepends=True)


def stated_search(source: dict) -> dict:
    """Spec section 4 steps 2-4 for a heading-not-present
    source (step 1, the pinned cleaned text, is gate 0.1 /
    the location pass). Returns the search log."""
    doc_id = source["document_id"]
    # Step 2: repository-wide search for the document_id
    # string; any candidate cleaned text verified by hash.
    grep = subprocess.run(
        ["git", "grep", "-l", doc_id, "--", "."],
        capture_output=True, text=True, timeout=300,
        cwd=str(REPO))
    hits = sorted(grep.stdout.split())
    filename_hits = sorted(
        str(p.relative_to(REPO)) for p in REPO.rglob(
            f"*{doc_id}*")
        if ".git" not in p.parts and p.is_file())
    cleaned_copies = [
        h for h in filename_hits if "/cleaned_text/" in h
        and h.endswith(".txt")
    ]
    # Step 3: the registry's recorded stored paths, on this
    # execution host.
    registry = json.loads(
        (REPO / "glossa-indus/literature/documents"
         / f"{doc_id}.json").read_text("utf-8"))
    raw_candidate = (
        REPO / "glossa-indus/raw/user_uploads"
        / registry["original_filename"])
    text_path = registry["stored_path_text"]
    # Step 4: a source-document copy produced by any step.
    doc_copies = [
        p for p in REPO.rglob(registry["original_filename"])
        if ".git" not in p.parts
    ]
    return {
        "step_1_pinned_cleaned_text": (
            "located at its section 2.1 path; SHA-256 matches "
            "the freeze pin (gate 0.1)"),
        "step_2_repository_search": {
            "files_naming_document_id": hits,
            "files_named_by_document_id": filename_hits,
            "cleaned_text_copies_found": cleaned_copies,
            "note": ("the only cleaned-text copy is the "
                     "pinned one of step 1, verified by "
                     "SHA-256 at gate 0.1; no moved or "
                     "renamed copy exists"),
        },
        "step_3_recorded_stored_paths": {
            "stored_path_raw": registry["stored_path_raw"],
            "stored_path_text": text_path,
            "raw_path_candidate_in_repo": str(
                raw_candidate.relative_to(REPO)),
            "raw_path_present": raw_candidate.exists(),
            "stored_path_text_present_on_this_host": (
                Path(text_path).exists()),
            "note": ("the recorded paths are Windows paths "
                     "of the intake host; no candidate "
                     "document was produced on this "
                     "execution host"),
        },
        "step_4_source_document": {
            "copies_of_original_filename_in_repo": [
                str(p.relative_to(REPO)) for p in doc_copies],
            "note": ("no copy of the source document was "
                     "produced by steps 1-3, so no document "
                     "text layer could be searched; the "
                     "sub-state is therefore HEADING NOT "
                     "PRESENT IN HELD TEXT"),
        },
    }


def main() -> int:
    anchors_before = sha256((REPO / ANCHORS_REL).read_bytes())
    results: dict = {
        "spec": "057",
        "phase": "Phase-419",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": "chq5e",
        "date": DATE,
        "fence": FENCE,
    }
    gates = []

    # ── Gate 0.1: input integrity ──────────────────────
    pin_rows = {}
    gate_01_ok = True
    for source in SOURCES:
        doc_id = source["document_id"]
        text_raw, _ = text_lines(doc_id)
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
            and registry["original_filename"]
            == source["document_filename"]
            and registry["file_size_bytes"]
            == source["document_size_bytes"]
            and registry["checksum_sha256"]
            == source["document_checksum_sha256"]
            and registry["license_status"] == "unclear"
            and (source["source"] == "S-1"
                 or entry.get("merged_into") == CANON_ID))
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
                source["claims_file_sha256"]),
            "claims_entry_facts_match": facts_ok,
            "claims_store_note": (
                "per freeze.md section 2 (the Spec 038 form), "
                "the extracted-claims store is asserted by its "
                "entries' facts, never by live-file hash; the "
                "live hash is recorded here for the record"),
        }
        pin_rows[source["source"]] = row
        gate_01_ok &= (
            row["cleaned_text_match"] and row["registry_match"]
            and facts_ok)
    extra = {}
    for key, rel, exp in [
        ("phase104_evaluation",
         "glossa-indus/reports/phase104_claims_evaluation.json",
         DEF["inputs"]["phase104_evaluation"]["sha256"]),
        ("lane2_drafts",
         "specs/029-tao-claim-lifecycle/lane2-drafts/"
         "drafts.json",
         DEF["inputs"]["lane2_drafts"]["sha256"]),
        ("anchors", ANCHORS_REL,
         DEF["inputs"]["anchors"]["sha256"]),
    ]:
        observed = sha256((REPO / rel).read_bytes())
        extra[key] = {"file": rel, "sha256": observed,
                      "match": observed == exp}
        gate_01_ok &= observed == exp
    p104_entry = find_claim(
        json.loads((REPO / extra["phase104_evaluation"]["file"])
                   .read_bytes()), CANON_ID)
    gate_01_ok &= (
        p104_entry["verdict"] == "stays_untested"
        and p104_entry["rule"] == "RULE-NOCOND")
    gates.append({
        "gate": "0.1", "name": "input integrity",
        "verdict": "PASS" if gate_01_ok else "FAIL",
        "pins": pin_rows, "record_inputs": extra,
        "phase104_entry": {
            "verdict": p104_entry["verdict"],
            "rule": p104_entry["rule"]},
    })
    if not gate_01_ok:
        results["outcome"] = ("CLOSED AT STEP 0 — INPUT PIN "
                              "MISMATCH")
        results["step0_gates"] = gates
        _write(results, [], None)
        return 0

    # ── Gate 0.2: source-set integrity ─────────────────
    canon_raw = (
        REPO / "glossa-indus/claims/extracted_claims"
        / f"{SOURCES[0]['document_id']}.json").read_bytes()
    canon = find_claim(json.loads(canon_raw), CANON_ID)
    instance_ids = [
        i["claim_id"] for i in canon["evidence_instances"]]
    expected_ids = [s["claim_id"] for s in SOURCES[1:]]
    set_ok = (
        instance_ids == expected_ids
        and canon["proposition_fingerprint"] == FINGERPRINT
        and all(
            i["record"]["merged_into"] == CANON_ID
            and i["record"]["proposition_fingerprint"]
            == FINGERPRINT
            for i in canon["evidence_instances"]))
    gates.append({
        "gate": "0.2", "name": "source-set integrity",
        "verdict": "PASS" if set_ok else "FAIL",
        "evidence_instance_claim_ids": instance_ids,
        "fingerprint": canon["proposition_fingerprint"],
    })
    if not set_ok:
        results["outcome"] = ("CLOSED AT STEP 0 — SOURCE SET "
                              "CHANGED")
        results["step0_gates"] = gates
        _write(results, [], None)
        return 0
    gates.append({
        "gate": "0.3", "name": "order",
        "verdict": "PASS",
        "note": ("gate verdicts are recorded in this "
                 "results record and in the outcome record "
                 "before any per-source row"),
    })
    results["step0_gates"] = gates

    # ── Location, extraction, accounting ───────────────
    rows = []
    counts = {"r": 0, "e": 0, "u": 0}
    passages_dir = SPEC_DIR / "passages"
    passages_dir.mkdir(exist_ok=True)
    for source in SOURCES:
        sid = source["source"]
        doc_id = source["document_id"]
        raw, kept = text_lines(doc_id)
        plain = [ln.rstrip("\n") for ln in kept]
        occurrences = [
            i + 1 for i, ln in enumerate(plain)
            if "positional analysis" in ln.lower()]
        loc = LOCATION[sid]
        row: dict = {
            "source": sid,
            "citation": source["citation"],
            "claim_id": source["claim_id"],
            "document_id": doc_id,
            "occurrence_lines": occurrences,
            "heading_form_lines": loc["heading_form_lines"],
            "toc_lines": loc["toc_lines"],
        }
        # Assert the executor's heading anchors on the
        # pinned bytes.
        for line_no in loc["heading_form_lines"]:
            assert "positional analysis" in (
                plain[line_no - 1].lower()), (sid, line_no)
        if loc["toc_lines"]:
            assert "positional analysis" in (
                plain[loc["toc_lines"][0] - 1].lower())
        if loc["passage"] is None:
            # SOURCE UNLOCATED / HEADING NOT PRESENT.
            assert not loc["heading_form_lines"]
            row["location_state"] = (
                "located (document, pinned cleaned text); "
                "no heading-form occurrence")
            row["outcome"] = "SOURCE UNLOCATED"
            row["sub_state"] = ("HEADING NOT PRESENT IN "
                                "HELD TEXT")
            row["search_log"] = stated_search(source)
            row["unblocking_act"] = (
                "Re-acquisition of the source through "
                "ordinary published-source channels, "
                "identified by the section 2.1 citation — "
                "specifically a copy of the edition the "
                "original extraction ran on, so the document "
                "text layer can be searched under section 5; "
                "the evidence on this row (the occurrence "
                "postures and the instance's recorded "
                "quote_fragment) supports the possibility "
                "that the original extraction harvested a "
                "non-heading occurrence, but the held record "
                "cannot distinguish that from a heading lost "
                "by the text layer")
            row["locator"] = None
            counts["u"] += 1
        else:
            start, end = loc["passage"]
            row["location_state"] = "located"
            row["heading_text"] = loc["heading_text"]
            # Byte-exact slice of the pinned text.
            offset_start = sum(
                len(x.encode("utf-8")) for x in kept[:start - 1])
            offset_end = sum(
                len(x.encode("utf-8")) for x in kept[:end])
            passage_bytes = raw[offset_start:offset_end]
            artifact = passages_dir / f"passage-{sid}.txt"
            artifact.write_bytes(passage_bytes)
            row["locator"] = {
                "cleaned_text_lines": [start, end],
                "heading_line": loc["heading_form_lines"][0],
                "passage_artifact": (
                    f"specs/057-five-sources-heading/passages/"
                    f"passage-{sid}.txt"),
                "passage_sha256": sha256(passage_bytes),
                "passage_bytes": len(passage_bytes),
            }
            passage_text = passage_bytes.decode("utf-8")
            if sid == "S-2":
                # PASSAGE EMPTY: the held excerpt under the
                # chapter heading carries the method (the
                # histogram calculation and the classification
                # definitions of section 3.3) and one figure
                # caption; it states no classification result
                # and no summary finding.
                assert "3.3 Classification of Indus signs" in (
                    passage_text)
                assert "labelled as an initial sign (INS)" in (
                    passage_text)
                assert "Signs 382" not in passage_text
                assert "\nSummary" not in passage_text
                row["outcome"] = "PASSAGE EMPTY"
                row["judgement"] = (
                    "The passage held under the heading is "
                    "the chapter's method: the normalised "
                    "weighted position calculation (section "
                    "3.2.2), a worked histogram example for "
                    "signs 351 and 720, the classification "
                    "definitions of section 3.3 (a sign mostly "
                    "at a text's beginning is labelled an "
                    "initial sign, INS; one preferably at "
                    "the end a terminal sign, TMK — "
                    "stipulative labels, not findings), and "
                    "the Figure 3.26 caption (seal M-1088, "
                    "initial cluster 002-820, terminal sign "
                    "740, given as a typical example). It "
                    "states no proposition about sign "
                    "positions carrying a quantity, a named "
                    "corpus, or a directional or comparative "
                    "assertion that could in principle be "
                    "checked: no sign's positional class is "
                    "stated as a result, and the chapter's "
                    "summary (table of contents: section 3.9, "
                    "p. 91) is not in the held excerpt. A "
                    "reader can disagree from the quoted "
                    "passage artifact.")
                row["evidence_ref"] = row["locator"][
                    "passage_artifact"]
                counts["e"] += 1
            else:
                rec = RECOVERED[sid]
                for phrase in rec["evidence_phrases"]:
                    assert phrase in passage_text, (sid, phrase)
                row["outcome"] = "CLAIM RECOVERED"
                row["recovered_claim_id"] = rec["claim_id"]
                intake = {
                    "claim_id": rec["claim_id"],
                    "stage": "created",
                    "status": "unchecked",
                    "intake": ("Spec 057 execution (Phase-419), "
                               "inside the execution per "
                               "DD-057-12"),
                    "date": DATE,
                    "source": sid,
                    "source_citation": source["citation"],
                    "source_claim_id": source["claim_id"],
                    "proposition": rec["proposition"],
                    "numbers": rec["numbers"],
                    "corpus_and_conditions": rec["corpus"],
                    "falsifier_status": (
                        "falsifier written from the passage's "
                        "own logic: " + FALSIFIER),
                    "passage_artifact": row["locator"][
                        "passage_artifact"],
                    "passage_sha256": row["locator"][
                        "passage_sha256"],
                    "locator": row["locator"],
                    "fence": FENCE,
                }
                (SPEC_DIR / rec["intake_file"]).write_text(
                    json.dumps(intake, indent=1,
                               ensure_ascii=False) + "\n",
                    encoding="utf-8")
                row["intake_record"] = (
                    f"specs/057-five-sources-heading/"
                    f"{rec['intake_file']}")
                row["intake"] = intake
                counts["r"] += 1
        rows.append(row)

    # ── Headline and disposition (spec section 7) ────
    r, e, u = counts["r"], counts["e"], counts["u"]
    assert r + e + u == 5
    if r == 5:
        headline_class = "A — FULL RECOVERY"
    elif r >= 1 and u == 0:
        headline_class = ("B — COMPLETE ACCOUNTING, "
                          "PARTIAL RECOVERY")
    elif r >= 1:
        headline_class = ("C — PARTIAL RECOVERY WITH "
                          "UNLOCATED SOURCES")
    elif u == 0:
        headline_class = ("D — NO CLAIM RECOVERED: ALL "
                          "PASSAGES EMPTY")
    elif u == 5:
        headline_class = "F — NO SOURCE LOCATED"
    else:
        headline_class = ("E — NO CLAIM RECOVERED: EMPTY "
                          "AND UNLOCATED")
    recovered_ids = [
        row["recovered_claim_id"] for row in rows
        if row["outcome"] == "CLAIM RECOVERED"]
    empty_ids = [row["source"] for row in rows
                 if row["outcome"] == "PASSAGE EMPTY"]
    unlocated = [
        f"{row['source']} ({row['sub_state']})" for row in rows
        if row["outcome"] == "SOURCE UNLOCATED"]
    headline = (
        f"Five sources were to be accounted for; {r} "
        f"yielded a recovered claim {recovered_ids}, {e} "
        f"passage(s) were located and state no checkable "
        f"finding {empty_ids}, and {u} source(s) could not "
        f"be located after the stated search {unlocated}. "
        f"The unblocking act for each unlocated source is "
        f"named on its row. The heading record is not "
        f"retired while a source remains unlocated.")
    disposition = (
        "superseded (r >= 1): the heading record is "
        "superseded by the recovered claims it pointed at, "
        f"named in the appended note: {recovered_ids}")
    results["accounting"] = rows
    results["counts"] = counts
    results["headline_class"] = headline_class
    results["headline"] = headline
    results["disposition"] = disposition
    results["outcome"] = headline_class
    anchors_after = sha256((REPO / ANCHORS_REL).read_bytes())
    results["anchors"] = {
        "file": ANCHORS_REL, "before_sha256": anchors_before,
        "after_sha256": anchors_after,
        "byte_identical": anchors_before == anchors_after}
    assert anchors_before == anchors_after
    _write(results, rows, headline)
    print(f"Phase-419: {headline_class} "
          f"(r={r}, e={e}, u={u})")
    return 0


def _write(results: dict, rows: list, headline) -> None:
    RESULTS_PATH.write_text(
        json.dumps(results, indent=1, ensure_ascii=False)
        + "\n", encoding="utf-8")
    lines = [
        "# Phase-419 (Spec 057) — report",
        "",
        f"Freeze digest: `{results['freeze_digest']}`. "
        f"OSF registration chq5e (approved + public before "
        f"the run). Date: {DATE}.",
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
            "| # | Source claim_id | Location state | "
            "Outcome | Evidence / intake |")
        lines.append("|---|---|---|---|---|")
        for row in rows:
            ev = row.get("intake_record") or row.get(
                "evidence_ref") or row.get("sub_state", "")
            lines.append(
                f"| {row['source']} | `{row['claim_id']}` | "
                f"{row['location_state']} | "
                f"{row['outcome']} | {ev} |")
        lines += [
            "",
            f"Counts: r={results['counts']['r']}, "
            f"e={results['counts']['e']}, "
            f"u={results['counts']['u']}.",
            "",
            f"## Headline — {results['headline_class']}",
            "",
            headline or "",
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
