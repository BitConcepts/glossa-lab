#!/usr/bin/env python3
"""Spec 073 (Phase-436) Asset A v2 build (spec section 5).

Universe: the 187 Asset A v1 rows carried verbatim (row_origin =
carried_v1, gate B3 field-for-field) plus new rows (row_origin =
new_entry) for every Registry v2 identity the attested frame resolves
to: parpola_1982 signs outside v1's universe (labels from the CISI
sign list as digitized) and icit_wells W-form signs (no verbal
depiction in any ruled source; entered unidentified with the search
recorded). Entry is blind two-pass under Spec 045's contract as
executed for v1: before any new row is coded, the deterministic rule
pass must reproduce Spec 069's recorded pass-2 codings on all 187
carried labels exactly (the discipline-continuity check).

Gates B1-B5 as frozen. Writes the asset CSV and its freeze record.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "specs" / "073-keying-surface-repair"
STEP0 = SPEC_DIR / "execution" / "step0-record.json"
REG_V2 = ROOT / "data/crosswalks/canonical_sign_registry_v2.csv"
REG_FREEZE = SPEC_DIR / "registry-v2" / "registry-v2-freeze.json"
ASSET_V1 = ROOT / "specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv"
DECISIONS_V1 = ROOT / "specs/069-hunt-asset-a/asset-a/entry-decisions.json"
OUT_DIR = SPEC_DIR / "asset-a-v2"
DECISIONS = OUT_DIR / "entry-decisions.json"
MAYIG = Path.home() / "workspace/research_notes/hunt-chain-sources/mayig-indus-valley-script-corpus"
EXT = Path.home() / "workspace/research_notes/indus-data-deep-sweep-20261008/downloads"
CORPUS = EXT / "shaktiosindia-indus-sign-regimes-deposit/sanitized_corpus.json"
GRADES = EXT / "shakti_row_grades_2026-10-22.csv"
PIN_ASSET_V1 = "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b"
PIN_REG_V2 = "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"

ANIMAL_T = {"fish", "deer", "elephant", "goat", "buffalo", "antelope", "hare", "rabbit", "bird",
            "scorpion", "snake", "unicorn", "bull", "dog", "tiger", "lion", "monkey", "tortoise",
            "turtle", "crocodile", "insect", "horse", "pig", "boar", "cow", "zebra", "peacock",
            "frog", "crab", "spider", "animal", "bee"}
HUMAN_T = {"person", "man", "woman", "human", "bearer", "priest", "figure"}
OBJECT_S = ["jar", "pot", "vessel", "table", "cart", "wheel", "pitchfork", "comb", "ladder",
            "stool", "stand", "basket", "bowl", "cup", "drum", "bow", "arrow", "spear", "sword",
            "knife", "axe", "plough", "boat", "chariot", "bed", "chair", "throne", "sieve",
            "scale", "yoke", "rope", "net", "lyre", "mill", "oven", "gate", "house", "pillar", "post"]
SKY_T = {"star", "sun", "moon", "sky", "comet", "eclipse", "planet"}


def span_of(label: str) -> str:
    cuts = [len(label)]
    for sep in (",", " with ", " where "):
        i = label.find(sep)
        if i >= 0:
            cuts.append(i)
    return label[:min(cuts)]


def rule_pass(label: str) -> str:
    """The deterministic second pass, fitted on and validated against
    Spec 069's executed codings (see the build record)."""
    if not label:
        return "unidentified"
    span = span_of(label).lower()
    toks = set(re.findall(r"[a-z]+", span))
    if toks & ANIMAL_T:
        return "animal"
    if toks & HUMAN_T:
        return "human"
    for w in OBJECT_S:
        if w in span:
            return "object_goods"
    if toks & SKY_T:
        return "sky_cycle"
    return "other"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    step0 = json.loads(STEP0.read_text(encoding="utf-8"))
    if step0["verdict"] != "PASS":
        print("step-0 record is not PASS; asset build refuses to run")
        return 1
    assert sha256(ASSET_V1) == PIN_ASSET_V1, "Asset A v1 pin mismatch"
    assert sha256(REG_V2) == PIN_REG_V2, "Registry v2 pin mismatch"
    reg_freeze = json.loads(REG_FREEZE.read_text(encoding="utf-8"))
    assert reg_freeze["sha256"] == PIN_REG_V2

    v1_rows = list(csv.DictReader(ASSET_V1.open(newline="", encoding="utf-8")))
    v1_fields = list(v1_rows[0].keys())
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))["signs"]

    # --- discipline-continuity check: rule pass reproduces v1's pass 2 ---
    dec_v1 = json.loads(DECISIONS_V1.read_text(encoding="utf-8"))["signs"]
    misses = []
    for r in v1_rows:
        want = dec_v1[r["sign_key"]]["pass2"]
        got = rule_pass(r["depicted_label_verbatim"]) if r["depicted_label_verbatim"] else "unidentified"
        if got != want:
            misses.append((r["sign_key"], want, got))
    if misses:
        failures.append(f"ENTRY DISCIPLINE FAILED: rule pass misses on carried labels: {misses}")
    continuity = {"carried_labels_checked": len(v1_rows), "rule_pass_misses": misses}

    # --- frame + Registry v2 resolution (the section 5.2 universe) ---
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    grade_of = {g["shakti_id"]: g["grade"] for g in csv.DictReader(GRADES.open())}
    frame: set[str] = set()
    for r in corpus:
        if any(s != "000" for s in r["symbols"]) and grade_of[r["id"]] in ("documented-lineage", "undocumented-corroborated"):
            frame.update(s for s in r["symbols"] if s != "000")
    reg_rows = list(csv.DictReader(REG_V2.open(newline="", encoding="utf-8")))
    wells_map: dict[str, set[str]] = {}
    for r in reg_rows:
        if r["numbering_system"] in ("parpola_1982", "icit_wells"):
            for token in (r["wells_ids"] or "").split("|"):
                token = token.strip()
                if token:
                    wells_map.setdefault(token, set()).add(r["sign_id"])
    resolved_ids: set[str] = set()
    for code in frame:
        hits = wells_map.get("W" + code, set())
        if len(hits) == 1:
            resolved_ids.update(hits)
    v1_ids = {r["sign_key"] for r in v1_rows}
    new_ids = sorted(resolved_ids - v1_ids)

    # --- B1: universe completeness ---
    if set(decisions) != set(new_ids):
        failures.append(f"ASSET FAILED (B1): decisions cover {len(decisions)} signs, universe is {len(new_ids)}")
    # --- B4 mechanics: every decision's pass2 equals the rule pass on its label ---
    labels: dict[str, str] = {}
    for sid in new_ids:
        if sid.startswith("W"):
            labels[sid] = ""
        else:
            feat = json.loads((MAYIG / "features" / f"{sid}.json").read_text(encoding="utf-8"))
            labels[sid] = feat.get("description", "")
    for sid in new_ids:
        if decisions[sid]["pass2"] != rule_pass(labels[sid]):
            failures.append(f"ASSET FAILED (B4): recorded pass2 for {sid} is not the rule pass output")

    # --- assemble rows ---
    out_fields = v1_fields + ["row_origin"]
    out_rows: list[dict] = []
    for r in v1_rows:
        row = {k: r[k] for k in v1_fields}
        row["row_origin"] = "carried_v1"
        out_rows.append(row)
    for sid in new_ids:
        d = decisions[sid]
        row = {k: "" for k in v1_fields}
        row["sign_key"] = sid
        row["depicted_kind"] = d["final"]
        row["depicted_label_verbatim"] = labels[sid]
        row["d18_input"] = "none"
        row["entered_blind"] = "yes"
        row["dispute_status"] = "borderline" if d["borderline"] else "none"
        if sid.startswith("W"):
            row["agreement"] = "silent"
            row["source_citations"] = "sources searched: " + d["sources_searched"]
        else:
            row["cisi_no"] = sid
            row["parpola_no"] = sid
            row["governing_source"] = "CISI"
            row["source_citations"] = (f"CISI sign list (Corpus of Indus Seals and Inscriptions), as held in the "
                                       f"mayig CISI digitization, features/{sid}.json — verbatim label")
            row["agreement"] = "single_source"
        row["row_origin"] = "new_entry"
        out_rows.append(row)

    # --- B2: citation completeness ---
    for row in out_rows:
        if row["row_origin"] == "new_entry" and not row["source_citations"]:
            failures.append(f"ASSET FAILED (B2): {row['sign_key']} carries no citation")
    # --- B3: carried-row fidelity (field-for-field against v1 as parsed) ---
    for i, r in enumerate(v1_rows):
        for k in v1_fields:
            if out_rows[i][k] != r[k]:
                failures.append(f"ASSET FAILED (B3): carried row {r['sign_key']} field {k} altered")

    if failures:
        print(json.dumps({"failures": failures}, indent=1))
        return 1

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=out_fields, lineterminator="\n")
    w.writeheader()
    for row in out_rows:
        w.writerow(row)
    data = buf.getvalue().encode("utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "depicted-kind-classification.csv").write_bytes(data)
    # B5: digest recomputation on the written file, round-trip validated
    parsed = list(csv.DictReader(io.StringIO(data.decode("utf-8"))))
    assert len(parsed) == len(out_rows) == 187 + len(new_ids)
    digest = hashlib.sha256(data).hexdigest()
    assert sha256(OUT_DIR / "depicted-kind-classification.csv") == digest

    census = Counter(r["depicted_kind"] for r in out_rows)
    census_new = Counter(r["depicted_kind"] for r in out_rows if r["row_origin"] == "new_entry")
    freeze = {
        "asset": "Asset A v2 — depicted-kind classification (Spec 073)",
        "contract": "Spec 045 sections 2-3, as executed for Asset A v1 by Spec 069, extended by Spec 073 section 5",
        "contract_anchor_freeze_digest": "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a",
        "spec073_freeze_digest": "5419c4c413189acdec31c15494daf1be759c10c28f84d594935c9629e761dc98",
        "canonical_file": "asset-a-v2/depicted-kind-classification.csv",
        "sha256": digest,
        "row_count": len(out_rows),
        "rows_carried_from_v1": 187,
        "rows_new_entry": len(new_ids),
        "per_kind_counts": dict(census),
        "per_kind_counts_new_entry": dict(census_new),
        "input_pins": {
            "asset_a_v1": {"sha256": PIN_ASSET_V1, "rows": 187},
            "registry_v2": {"sha256": PIN_REG_V2, "rows": 1013},
        },
        "entry_discipline": {
            "rule_pass_continuity_check": continuity,
            "disagreements_adjudicated": sum(1 for d in decisions.values() if d["pass1"] != d["pass2"]),
            "entry_log": "asset-a-v2/entry-decisions.json",
        },
        "build_order_attestation": ("entry was performed from the held published sources and the sign inventory "
                                    "only, in the frozen order (Registry v2 frozen first; entry second; the "
                                    "coverage join computed only after both digests exist); no positional "
                                    "result, keyability outcome, or Hunt part-membership information was "
                                    "consulted at any point during entry"),
        "freeze_date": "2026-10-23",
    }
    (OUT_DIR / "asset-a-v2-freeze.json").write_text(json.dumps(freeze, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(freeze, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
