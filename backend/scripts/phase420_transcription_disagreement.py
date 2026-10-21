#!/usr/bin/env python3
"""Phase-420 — Spec 058 execution (what drove the Spec 023
transcription disagreement; design D-21, arm A only).

Executes the frozen Spec 058 contract
(specs/058-transcription-disagreement-mechanism/freeze.md;
freeze digest
8bdd4764380bf9e6cb442b1cc75a3b57f4507284676bcb65603e481a49435713;
OSF registration 86dgh, approved and public before this
run) as Phase-420, in Wave 3 group 2 of the
runnable-experiments campaign (plan approved AS WRITTEN
on 2026-10-21). Arm A only: a re-analysis of the recorded
Phase-132 pilot passes. Arm B (the human-coder
calibration arm) is blocked and out of scope (claim
F058-C06); this script designs and runs no part of it
and no AI substitution for human coders. No record is
re-coded, no image is consulted, and no substitute
source is admitted.

Step 0 runs first, in the frozen order (spec section
3), before any localisation quantity:

  0.1 Committed-record integrity — every spec
      section 2.1 input hashes to its freeze-record
      value. Mismatch stops the run as INVALID.
  0.2 Pilot-pass record production — the Phase-132
      store record set is produced at the execution
      venue (the machine holding the program's main
      checkout; ruling DD-058-15) and inventoried
      against the pilot report's section 9 inventory:
      frame.json, 50 Pass A records, 50 Pass B
      records, 10 gold-pass records, 50 adjudication
      records, effort_log.csv with 320 events, keyed
      by the committed frame's canonical keys. A
      per-file SHA-256 manifest of the produced set
      is computed and recorded. A shortfall closes
      the execution as PILOT-PASS RECORDS NOT
      PRODUCIBLE, unscored. Production is a records
      act only: no record is edited, completed, or
      re-created.
  0.3 Frame identity — the produced store's frame
      list equals the committed pilot frame exactly.
      Mismatch stops the run as INVALID.
  0.4 Reproduction of the committed metrics — the
      pinned Phase-132 metrics module, imported
      unchanged, computes the metrics from the
      produced store; the computed record must equal
      the committed metrics file in full. Mismatch
      stops the run as INVALID.
  0.5 Adjudication-taxonomy cross-check — the
      disagreement taxonomy recomputed from the
      produced adjudication records equals the pilot
      report's section 4(c) counts exactly (identity
      93, legibility 45, count 11, key 10, orientation
      2, order 1; total 162). Mismatch stops the run
      as INVALID.
  0.6 Analysis census — the mismatched population
      (objects whose Pass A and Pass B P-sequences
      differ; 40 on the committed record) is
      published as the population every share is
      taken over.

Tabulations (spec section 4) run on the gate-proven
record set only, with the frozen machinery imported
unchanged from the pinned phase132_metrics.py (the
store loader, the P-space derivation, the minimum-edit
alignment): mismatch events typed SUBSTITUTION /
INDEL over the frozen alignment; T1 by sign
(involvement counts; top-10 share over summed
involvement; frequency shares over the 381 tokens of
both passes' full sequences), T2 by recorded object
type, T3 by divergence type (the INDEL share is the
registered segmentation proxy, spec section 8(4));
the first-divergence table; the section 4.4
UNK-excluded descriptive secondary; and the M-space
sensitivity (descriptive only). Locus rules and the
headline mapping are spec section 5's, mechanically
applied (combination class LOCALISED TO MULTIPLE
LOCI, DD-058-9).

Outputs (written on every terminal outcome):
  - reports/phase420_results.json (the machine record)
  - reports/phase420_report.md (the report, under
    spec section 6's reporting obligations)

Integrity: the anchors file is asserted byte-identical
before and after. The script is deterministic: a
second run over the same record set reproduces both
output files byte-identically.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO / "backend" / "scripts"

FREEZE_DIGEST = (
    "8bdd4764380bf9e6cb442b1cc75a3b57f4507284676bcb65603e481a49435713"
)
CLAIM_ID = "STUDY-SPEC-023/PHASE-132+383"
EXECUTION_DATE = "2026-10-21"
BASE_COMMIT = "3200b7b5b6841a7b9567a81368bf84004fd17255"

# The execution venue is the machine holding the
# program's main checkout (ruling DD-058-15); the
# Phase-132 store lives there, gitignored, exactly as
# the Phase-383 rescoring read it.
DEFAULT_STORE = (
    Path.home() / "workspace" / "glossa-lab" / "corpora"
    / "downloads" / "cisi_image_layer" / "phase132_pilot"
)

PINS = [
    ("specs/023-keyed-transcription-layer/spec.md",
     "c2e5d1668b270266d5a20e30b1ec87cd4c1d5d2ffe786a45331a9a5ade1275d2"),
    ("reports/phase132_pilot_metrics.json",
     "e864fca57ecd1dc403c8e52ab9df6414372478d5781457f0aaca5e9084914554"),
    ("reports/phase132_pilot_report.md",
     "e1df32da86f7d3fd276d0ad546b3c351b58fd88b73f4468461f61075f6460e00"),
    ("data/keyed_transcription/phase132_pilot_frame.json",
     "a967144be0531c9d8396615d1ca07161dca0bc7347ca8c2c0d6a3c21a037a2ea"),
    ("data/keyed_transcription/phase132_pilot_dataset_v1.json",
     "adb596a1745470835e46c5148c1848d8408c45a030687d96427f00dbb6f74400"),
    ("data/keyed_transcription/phase132_pilot_dataset_v1_meta.json",
     "b2c607fae5f2602bb7b9634ff103f01df1de3885a1f1bbeeb6da3fc489cdefd4"),
    ("reports/phase383_results.json",
     "4e52942dc6be25fed4ab2004823a1d9353c9abfe6f5428e1050ee8d0d9a98334"),
    ("reports/phase383_report.md",
     "9f35f722611f6acd57e1ee05c9de0c8e95267ccf7f93b27eacb31bdff9cd08ca"),
    ("backend/scripts/phase132_metrics.py",
     "238dfafa3bac17dc0ad610ff4b7e6cf4fa577462d04cd31a3c612537cbe21984"),
    ("backend/scripts/phase383_pilot_rescoring.py",
     "b64b60de35d59bd99177e8ac3f68a80ffd2b0d31f8c75ea87312f69f927729ec"),
    ("data/crosswalks/parpola_mahadevan_crosswalk_v1.json",
     "4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb"),
    ("backend/reports/INDUS_FINAL_ANCHORS.json",
     "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"),
]
PIN_FRAME = PINS[3][1]
PIN_ANCHORS = PINS[11][1]
FRAME_REL = PINS[3][0]
METRICS_REL = PINS[1][0]

EXPECTED_TAXONOMY = {
    "identity": 93, "legibility": 45, "count": 11,
    "key": 10, "orientation": 2, "order": 1,
}
EXPECTED_EFFORT_EVENTS = 320

FENCE_SENTENCE = (
    "This account is about why two recorded AI pilot "
    "passes disagreed. It is not evidence about human "
    "transcription, and it changes no verdict."
)

_OUT_RESULTS = _REPO / "reports" / "phase420_results.json"
_OUT_REPORT = _REPO / "reports" / "phase420_report.md"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _round(x):
    return round(x, 6) if x is not None else None


def _pct(share: float) -> str:
    return f"{share * 100:.1f}%"


def _load_metrics_module():
    """Import the pinned Phase-132 metrics module
    unchanged (the Phase-383 precedent)."""
    spec = importlib.util.spec_from_file_location(
        "phase132_metrics", _SCRIPTS / "phase132_metrics.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["phase132_metrics"] = mod
    spec.loader.exec_module(mod)
    return mod


def _check_pin(rel: str, pin: str) -> dict:
    path = _REPO / rel
    if not path.exists():
        return {"file": rel, "pin": pin, "observed": None,
                "present": False, "match": False}
    observed = _sha256(path)
    return {"file": rel, "pin": pin, "observed": observed,
            "present": True, "match": observed == pin}


# ── Step 0 ──────────────────────────────────────────────

def _gate_01() -> tuple[dict, bool]:
    checks = [_check_pin(rel, pin) for rel, pin in PINS]
    ok = all(c["match"] for c in checks)
    return ({"gate": "0.1", "name": "Committed-record integrity",
             "verdict": "PASS" if ok else "FAIL",
             "inputs": checks}, ok)


def _expected_store_files(frame_entries):
    keys = [e["canonical_key"] for e in frame_entries]
    gold = [e["canonical_key"] for e in frame_entries if e.get("gold")]
    rels = ["frame.json", "effort_log.csv"]
    rels += [f"pass_a/{k}.json" for k in keys]
    rels += [f"pass_b/{k}.json" for k in keys]
    rels += [f"pass_gold/{k}.json" for k in gold]
    rels += [f"adjudication/{k}.json" for k in keys]
    return rels, keys, gold


def _gate_02(store: Path, frame_entries) -> tuple[dict, bool]:
    rels, keys, gold = _expected_store_files(frame_entries)
    missing = [r for r in rels if not (store / r).is_file()]
    effort_events = None
    effort_path = store / "effort_log.csv"
    if effort_path.is_file():
        with open(effort_path, newline="", encoding="utf-8") as fh:
            effort_events = sum(1 for _ in csv.DictReader(fh))
    inventory = {
        "frame_json": (store / "frame.json").is_file(),
        "pass_a_records": sum(
            1 for k in keys if (store / f"pass_a/{k}.json").is_file()),
        "pass_b_records": sum(
            1 for k in keys if (store / f"pass_b/{k}.json").is_file()),
        "pass_gold_records": sum(
            1 for k in gold if (store / f"pass_gold/{k}.json").is_file()),
        "adjudication_records": sum(
            1 for k in keys
            if (store / f"adjudication/{k}.json").is_file()),
        "effort_log_events": effort_events,
    }
    expected = {
        "frame_json": True, "pass_a_records": 50,
        "pass_b_records": 50, "pass_gold_records": 10,
        "adjudication_records": 50,
        "effort_log_events": EXPECTED_EFFORT_EVENTS,
    }
    ok = (not missing) and inventory == expected
    manifest = {}
    if ok:
        for rel in rels:
            manifest[rel] = _sha256(store / rel)
    gate = {"gate": "0.2", "name": "Pilot-pass record production",
            "verdict": "PASS" if ok else "FAIL",
            "store": str(store),
            "inventory": inventory,
            "expected_inventory": expected,
            "missing_files": missing,
            "manifest_files": len(manifest),
            "manifest": manifest}
    return gate, ok


def _taxonomy(store: Path, keys) -> dict:
    counts: Counter = Counter()
    for k in keys:
        rec = json.loads(
            (store / f"adjudication/{k}.json").read_text("utf-8"))
        for d in rec["disagreements"]:
            counts[d["type"]] += 1
    return dict(sorted(counts.items()))


# ── Tabulations (spec section 4) ────────────────────────

def _events_for(mod, seq_a, seq_b):
    """Frozen alignment -> typed mismatch events."""
    cols = mod.align(seq_a, seq_b)
    events = []
    for idx, (x, y) in enumerate(cols, start=1):
        if x is not None and x == y:
            continue
        if x is not None and y is not None:
            events.append({"position": idx, "type": "SUBSTITUTION",
                           "a_value": x, "b_value": y})
        else:
            events.append({"position": idx, "type": "INDEL",
                           "a_value": x, "b_value": y})
    return events


def _tabulate(events_by_key, frame_by_key, token_counts):
    """T1/T2/T3 + locus verdicts over a given event set.

    events_by_key: key -> event list (already filtered
    by the caller for the descriptive secondary).
    token_counts: Counter over both passes' full token
    streams (the frequency basis; 381 tokens on the
    committed record)."""
    all_events = [e for k in sorted(events_by_key)
                  for e in events_by_key[k]]
    total_e = len(all_events)

    involvement: Counter = Counter()
    for e in all_events:
        if e["type"] == "SUBSTITUTION":
            involvement[e["a_value"]] += 1
            involvement[e["b_value"]] += 1
        else:
            present = e["a_value"] if e["a_value"] is not None \
                else e["b_value"]
            involvement[present] += 1
    total_involvement = sum(involvement.values())
    ranked = sorted(involvement.items(), key=lambda kv: (-kv[1], kv[0]))
    total_tokens = sum(token_counts.values())
    t1_rows = [
        {"value": v, "involvement": c,
         "involvement_share": _round(c / total_involvement)
         if total_involvement else None,
         "frequency": token_counts.get(v, 0),
         "frequency_share": _round(token_counts.get(v, 0) / total_tokens)
         if total_tokens else None}
        for v, c in ranked
    ]
    top10 = t1_rows[:10]
    top10_involvement = sum(r["involvement"] for r in top10)
    top10_share = (top10_involvement / total_involvement
                   if total_involvement else 0.0)
    top10_freq = sum(r["frequency"] for r in top10)
    top10_freq_share = top10_freq / total_tokens if total_tokens else 0.0
    if top10_share >= 0.5:
        sign_state = "CONCENTRATED"
    elif abs(top10_share - top10_freq_share) <= 0.10:
        sign_state = "UNIFORM"
    else:
        sign_state = "BETWEEN"
    signs_fire = top10_share >= 0.5
    unk_in_top10 = any(r["value"] == "UNK" for r in top10)
    unk_row = next((r for r in t1_rows if r["value"] == "UNK"), None)

    def _category(entry):
        return entry.get("object_type") or "Unrecorded"

    cats = ["Seals", "Tablets", "Unrecorded"]
    t2_rows = []
    for cat in cats:
        cat_keys = [k for k, e in frame_by_key.items()
                    if _category(e) == cat]
        cat_mismatched = [k for k in cat_keys if k in events_by_key]
        cat_events = sum(len(events_by_key[k]) for k in cat_mismatched)
        t2_rows.append({
            "object_type_recorded": cat,
            "events": cat_events,
            "event_share": _round(cat_events / total_e) if total_e
            else None,
            "objects": len(cat_keys),
            "object_share": _round(len(cat_keys) / len(frame_by_key)),
            "mismatched_objects": len(cat_mismatched),
        })
    types_fire = None
    for row in t2_rows:
        if row["object_type_recorded"] == "Unrecorded":
            continue
        if total_e and row["events"] / total_e >= 0.5 and (
                row["events"] / total_e
                - row["objects"] / len(frame_by_key) >= 0.10):
            types_fire = row["object_type_recorded"]

    n_sub = sum(1 for e in all_events if e["type"] == "SUBSTITUTION")
    n_indel = total_e - n_sub
    indel_share = n_indel / total_e if total_e else 0.0
    t3 = {"substitution": n_sub,
          "substitution_share": _round(n_sub / total_e) if total_e
          else None,
          "indel": n_indel,
          "indel_share": _round(indel_share) if total_e else None}
    seg_fire = indel_share >= 0.5

    loci = {
        "signs": {"fires": signs_fire,
                  "top10_involvement": top10_involvement,
                  "total_involvement": total_involvement,
                  "top10_share": _round(top10_share),
                  "top10_values": [r["value"] for r in top10],
                  "top10_frequency": top10_freq,
                  "total_tokens": total_tokens,
                  "top10_frequency_share": _round(top10_freq_share),
                  "sign_state": sign_state,
                  "unk_in_top10": unk_in_top10,
                  "unk_involvement_share":
                      _round(unk_row["involvement"] / total_involvement)
                      if unk_row and total_involvement else None},
        "object_types": {"fires": types_fire is not None,
                         "firing_type": types_fire},
        "segmentation": {"fires": seg_fire,
                         "indel_share": _round(indel_share)},
    }
    return {"event_total_E": total_e,
            "total_involvement": total_involvement,
            "t1_by_sign": t1_rows,
            "t2_by_object_type": t2_rows,
            "t3_by_divergence_type": t3,
            "loci": loci}


def _headline(primary):
    """The section 5.2 headline: word + pre-written
    paragraph, filled mechanically."""
    loci = primary["loci"]
    firing = []
    if loci["signs"]["fires"]:
        firing.append("SIGNS")
    if loci["object_types"]["fires"]:
        firing.append("OBJECT TYPES")
    if loci["segmentation"]["fires"]:
        firing.append("SEGMENTATION")
    s = loci["signs"]
    t2 = primary["t2_by_object_type"]
    by_type = {r["object_type_recorded"]: r for r in t2}
    largest_type_share = max(
        (r["event_share"] or 0.0) for r in t2)
    unk_sentence = ""
    if s["fires"] and s["unk_in_top10"]:
        unk_sentence = (
            " UNK — the passes' 'no identification' value — is "
            "itself among the most-involved values ("
            + _pct(s["unk_involvement_share"])
            + " of involvement); the localisation is in part a "
            "localisation to illegibility, stated as such.")
    if len(firing) >= 2:
        names = {"SIGNS": "signs", "OBJECT TYPES": "object types",
                 "SEGMENTATION": "segmentation choices"}
        shares = []
        if "SIGNS" in firing:
            shares.append(
                "the 10 most-involved signs account for "
                + _pct(s["top10_share"]) + " of all mismatch "
                "involvement")
        if "OBJECT TYPES" in firing:
            ft = loci["object_types"]["firing_type"]
            shares.append(
                f"objects recorded as {ft} carry "
                + _pct(by_type[ft]["event_share"])
                + " of all mismatch events")
        if "SEGMENTATION" in firing:
            shares.append(
                _pct(primary["t3_by_divergence_type"]["indel_share"])
                + " of mismatch events are insertion/deletion "
                "events")
        para = (
            "Re-analysed under Spec 058, the disagreement between "
            "the two recorded Phase-132 pilot passes is localised "
            "to " + ", ".join(names[f] for f in firing) + ": "
            + "; ".join(shares) + ". No single locus accounts for "
            "the disagreement on its own. The pilot's failure "
            "stands exactly as recorded; this account says "
            "nothing about human coders.")
        return "LOCALISED TO MULTIPLE LOCI", para + unk_sentence
    if firing == ["SIGNS"]:
        para = (
            "Re-analysed under Spec 058, the disagreement between "
            "the two recorded Phase-132 pilot passes is localised "
            "to signs: the 10 most-involved signs account for "
            + _pct(s["top10_share"]) + " of all mismatch "
            "involvement, led by "
            + ", ".join(s["top10_values"]) + ". The pilot's "
            "failure stands exactly as recorded; this account "
            "names where its disagreement sits, in this pilot's "
            "passes, and says nothing about human coders.")
        return "LOCALISED TO SIGNS", para + unk_sentence
    if firing == ["OBJECT TYPES"]:
        ft = loci["object_types"]["firing_type"]
        row = by_type[ft]
        census_sentence = (
            f"The mismatched census is {sum(r['mismatched_objects'] for r in t2)} "
            f"objects: Seals {by_type['Seals']['mismatched_objects']}, "
            f"Tablets {by_type['Tablets']['mismatched_objects']}, "
            f"Unrecorded {by_type['Unrecorded']['mismatched_objects']}; "
            f"{ft} carry {row['events']} of "
            f"{primary['event_total_E']} mismatch events.")
        para = (
            "Re-analysed under Spec 058, the disagreement between "
            "the two recorded Phase-132 pilot passes is localised "
            f"to object types: objects recorded as {ft} carry "
            + _pct(row["event_share"]) + " of all mismatch events "
            f"on {row['objects']} of 50 frame objects. "
            + census_sentence + " The pilot's failure stands "
            "exactly as recorded; this account says nothing about "
            "human coders.")
        return "LOCALISED TO OBJECT TYPES", para
    if firing == ["SEGMENTATION"]:
        para = (
            "Re-analysed under Spec 058, the disagreement between "
            "the two recorded Phase-132 pilot passes is localised "
            "to segmentation choices, as registered in Spec 058 "
            "§4.3: "
            + _pct(primary["t3_by_divergence_type"]["indel_share"])
            + " of mismatch events are insertion/deletion "
            "events — the passes differ more in how they cut "
            "sequences than in which signs they name. The pilot's "
            "failure stands exactly as recorded; this account "
            "says nothing about human coders.")
        return "LOCALISED TO SEGMENTATION", para
    para = (
        "Re-analysed under Spec 058, the disagreement between the "
        "two recorded Phase-132 pilot passes does not localise: "
        "no sign set, object type, or segmentation proxy meets "
        "the frozen criteria (top-10 sign share "
        + _pct(s["top10_share"]) + " against a frequency share "
        "of " + _pct(s["top10_frequency_share"]) + " — "
        + s["sign_state"] + "; largest object-type event share "
        + _pct(largest_type_share)
        + "; indel share "
        + _pct(primary["t3_by_divergence_type"]["indel_share"])
        + "). The disagreement is distributed across the "
        "passes' readings in proportion too close to their "
        "frequencies to name a locus. The pilot's failure "
        "stands exactly as recorded.")
    return "NOT LOCALISED", para


def _first_divergence(events_by_key):
    rows = []
    for k in sorted(events_by_key):
        evs = events_by_key[k]
        if not evs:
            continue
        first = evs[0]
        rows.append({"key": k, "position": first["position"],
                     "type": first["type"],
                     "a_value": first["a_value"],
                     "b_value": first["b_value"]})
    by_position = Counter(r["position"] for r in rows)
    by_type = Counter(r["type"] for r in rows)
    by_value: Counter = Counter()
    for r in rows:
        if r["type"] == "SUBSTITUTION":
            by_value[r["a_value"]] += 1
            by_value[r["b_value"]] += 1
        else:
            present = r["a_value"] if r["a_value"] is not None \
                else r["b_value"]
            by_value[present] += 1
    summary = {
        "by_position": {str(p): by_position[p]
                        for p in sorted(by_position)},
        "by_type": dict(sorted(by_type.items())),
        "by_value": [{"value": v, "count": c} for v, c in
                     sorted(by_value.items(),
                            key=lambda kv: (-kv[1], kv[0]))],
    }
    return rows, summary


def _analyse(mod, data, frame_by_key, census_keys, space):
    """Full section 4 tabulation set for one space."""
    val = mod.p_values if space == "p" else mod.m_values

    # build_m_to_p is deterministic; build it once.
    m_to_p = mod.build_m_to_p(json.loads(
        mod.CROSSWALK_PATH.read_text("utf-8"))["rows"])

    def seqs(pass_name):
        return {k: val(mod.derive_sequence(
            [t["m_id"] for t in data["passes"][pass_name][k]],
            m_to_p)) for k in data["keys"]}

    seq_a, seq_b = seqs("pass_a"), seqs("pass_b")
    token_counts: Counter = Counter()
    for k in data["keys"]:
        token_counts.update(seq_a[k])
        token_counts.update(seq_b[k])
    events_by_key = {}
    per_object = {}
    for k in census_keys:
        evs = _events_for(mod, seq_a[k], seq_b[k])
        events_by_key[k] = evs
        per_object[k] = evs
    primary = _tabulate(events_by_key, frame_by_key, token_counts)
    # Section 4.4 descriptive secondary: exclude every
    # event involving an UNK value on either side.
    filtered = {
        k: [e for e in evs
            if e["a_value"] != "UNK" and e["b_value"] != "UNK"]
        for k, evs in events_by_key.items()
    }
    secondary = _tabulate(filtered, frame_by_key, token_counts)
    fd_rows, fd_summary = _first_divergence(per_object)
    return {"primary": primary,
            "secondary_unk_excluded": secondary,
            "per_object_events": {
                k: per_object[k] for k in sorted(per_object)},
            "first_divergence": fd_rows,
            "first_divergence_summary": fd_summary,
            "token_total_both_passes": sum(token_counts.values())}


# ── Report (spec section 6) ─────────────────────────────

def _fmt_share(x):
    return "—" if x is None else _pct(x)


def _report_lines(rec):
    lines = [
        "# Phase-420 — Spec 058 report (transcription-disagreement mechanism)",
        "",
        f"Claim: `{CLAIM_ID}` — SETTLED — CONTRADICTED, exactly as",
        "recorded; this execution appends a mechanism account and",
        "changes no verdict. Execution date: 2026-10-21. Freeze digest:",
        f"`{FREEZE_DIGEST}`. OSF registration 86dgh (approved and",
        "public). Phase-420, Wave 3 group 2 of the runnable-experiments",
        "campaign. Arm A only; arm B is blocked and out of scope.",
        "",
        f"## Outcome: {rec['outcome']}",
        "",
        "Headline paragraph (spec §5.2 wording, quantities filled):",
        "",
        f"> {rec['headline_paragraph']}",
        "",
        f"Fence sentence: {FENCE_SENTENCE}",
        "",
        "## Step 0, gate by gate",
        "",
    ]
    for g in rec["step0"]:
        lines.append(f"- **Gate {g['gate']} — {g.get('name', '')}: "
                     f"{g['verdict']}**")
        if g["gate"] == "0.1":
            for p in g["inputs"]:
                lines.append(
                    f"  - `{p['file']}` — "
                    f"{'match' if p['match'] else 'MISMATCH'} "
                    f"({p['observed']})")
        if g["gate"] == "0.2" and "inventory" in g:
            inv = g["inventory"]
            lines.append(
                f"  - Inventory: frame.json "
                f"{'present' if inv['frame_json'] else 'MISSING'}; "
                f"Pass A {inv['pass_a_records']}/50; "
                f"Pass B {inv['pass_b_records']}/50; "
                f"gold {inv['pass_gold_records']}/10; "
                f"adjudication {inv['adjudication_records']}/50; "
                f"effort log {inv['effort_log_events']} events. "
                f"Manifest: {g['manifest_files']} files "
                f"(per-file SHA-256 in the results JSON).")
            if g["missing_files"]:
                lines.append(
                    f"  - Missing: {', '.join(g['missing_files'])}")
        if g["gate"] == "0.4" and "reproduction" in g:
            r = g["reproduction"]
            lines.append(
                f"  - Full-record equality with the committed metrics "
                f"file: {r['full_record_equal']}; exact-sequence "
                f"{r['exact_sequence_agreement_all_50_p']} (P and M), "
                f"per-token {r['per_token_agreement_all_50']} all-50 / "
                f"{r['per_token_agreement_gold']} gold, gold estimator "
                f"{r['gold_error_estimator_p']}, token totals "
                f"{r['total_tokens_pass_a']}/"
                f"{r['total_tokens_pass_b']}/"
                f"{r['total_tokens_pass_gold']}/"
                f"{r['total_tokens_adjudicated_final']}.")
        if g["gate"] == "0.5" and "taxonomy" in g:
            lines.append(f"  - Taxonomy recomputed: {g['taxonomy']}")
        if g["gate"] == "0.6" and "census" in g:
            lines.append(
                f"  - Census: {len(g['census'])} mismatched objects "
                f"(full census in the results JSON and the outcome "
                f"record).")
    analysis = rec.get("analysis")
    if analysis:
        p = analysis["primary"]
        lines += [
            "",
            "## Tabulations (P space, primary)",
            "",
            f"Event total E = {p['event_total_E']} over the "
            f"{len(rec['census'])} mismatched objects; summed "
            f"involvement = {p['total_involvement']}.",
            "",
            "### T1 — by sign (full ranked table in the results JSON)",
            "",
            "| value | involvement | involvement share | frequency | frequency share |",
            "|---|---|---|---|---|",
        ]
        for r in p["t1_by_sign"]:
            lines.append(
                f"| {r['value']} | {r['involvement']} | "
                f"{_fmt_share(r['involvement_share'])} | "
                f"{r['frequency']} | "
                f"{_fmt_share(r['frequency_share'])} |")
        s = p["loci"]["signs"]
        lines += [
            "",
            f"Top-10 share {_fmt_share(s['top10_share'])} over summed "
            f"involvement; frequency share of the same 10 values "
            f"{_fmt_share(s['top10_frequency_share'])}; state "
            f"{s['sign_state']}; sign locus "
            f"{'FIRES' if s['fires'] else 'does not fire'}.",
            "",
            "### T2 — by object type",
            "",
            "| recorded type | events | event share | objects | object share | mismatched objects |",
            "|---|---|---|---|---|---|",
        ]
        for r in p["t2_by_object_type"]:
            lines.append(
                f"| {r['object_type_recorded']} | {r['events']} | "
                f"{_fmt_share(r['event_share'])} | {r['objects']} | "
                f"{_fmt_share(r['object_share'])} | "
                f"{r['mismatched_objects']} |")
        t3 = p["t3_by_divergence_type"]
        lines += [
            "",
            "### T3 — by divergence type",
            "",
            f"SUBSTITUTION {t3['substitution']} "
            f"({_fmt_share(t3['substitution_share'])}); INDEL "
            f"{t3['indel']} ({_fmt_share(t3['indel_share'])}). The "
            f"INDEL share is the registered segmentation proxy "
            f"(spec §8(4): an indel cannot be separated into a "
            f"different cut of the same glyphs versus a sign one "
            f"pass recorded and the other omitted). Segmentation "
            f"locus {'FIRES' if p['loci']['segmentation']['fires'] else 'does not fire'}; "
            f"object-type locus "
            f"{'FIRES (' + str(p['loci']['object_types']['firing_type']) + ')' if p['loci']['object_types']['fires'] else 'does not fire'}.",
            "",
            "## Descriptive secondary (UNK-excluded) and M-space sensitivity",
            "",
        ]
        sec = analysis["secondary_unk_excluded"]
        lines.append(
            f"Secondary (events involving UNK excluded): E = "
            f"{sec['event_total_E']}; top-10 sign share "
            f"{_fmt_share(sec['loci']['signs']['top10_share'])} "
            f"(state {sec['loci']['signs']['sign_state']}); indel "
            f"share {_fmt_share(sec['t3_by_divergence_type']['indel_share'])}. "
            f"The secondary is descriptive only and carries no "
            f"headline. Full secondary tables are in the results "
            f"JSON.")
        if rec.get("m_space_sensitivity"):
            mp = rec["m_space_sensitivity"]["primary"]
            lines.append(
                f"M-space sensitivity (descriptive only): E = "
                f"{mp['event_total_E']}; top-10 sign share "
                f"{_fmt_share(mp['loci']['signs']['top10_share'])} "
                f"(state {mp['loci']['signs']['sign_state']}); indel "
                f"share {_fmt_share(mp['t3_by_divergence_type']['indel_share'])}. "
                f"Full M-space tables are in the results JSON; they "
                f"move no headline (DD-058-4).")
        fd = analysis["first_divergence_summary"]
        lines += [
            "",
            "## First divergence",
            "",
            f"Per-object first-divergence table is in the results "
            f"JSON. Distribution by position: {fd['by_position']}; "
            f"by type: {fd['by_type']}.",
            "",
            "## Produced-set manifest",
            "",
            "Per-file SHA-256 of the 162-file produced set (gate "
            "0.2):",
            "",
        ]
        manifest = rec["step0"][1].get("manifest", {})
        for rel in sorted(manifest):
            lines.append(f"- `{rel}` — `{manifest[rel]}`")
    lines += [
        "",
        f"Anchors asserted byte-identical before and after: "
        f"`{rec['anchors_before']}` at both readings.",
        "",
        "*AI disclosure: executed by an AI agent (Muse Spark,",
        "via Muse) at the direction of Tristen Pierson, per",
        "constitution section VI.*",
        "",
    ]
    return lines


# ── Main ────────────────────────────────────────────────

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--store", type=Path, default=DEFAULT_STORE)
    args = ap.parse_args(argv)
    store: Path = args.store

    anchors_before = _sha256(_REPO / "backend/reports/"
                               "INDUS_FINAL_ANCHORS.json")

    gates: list[dict] = []
    outcome = None
    headline_paragraph = None
    census = None
    analysis = None
    m_sensitivity = None

    committed_frame = json.loads((_REPO / FRAME_REL).read_text("utf-8"))
    frame_entries = committed_frame["frame"]
    frame_by_key = {e["canonical_key"]: e for e in frame_entries}

    # Gate 0.1 — committed-record integrity.
    g01, ok01 = _gate_01()
    gates.append(g01)
    if not ok01:
        bad = [c["file"] for c in g01["inputs"] if not c["match"]]
        outcome = "INVALID"
        headline_paragraph = (
            "Spec 058 stops as INVALID at gate 0.1: committed-record "
            f"integrity failed for {', '.join(bad)} (observed hashes "
            "in the step-0 record). No localisation quantity was "
            "computed. The Spec 023 pilot record stands exactly as "
            "recorded; the failure is in this spec's inputs, not in "
            "the pilot.")
    else:
        # Gate 0.2 — record-set production.
        g02, ok02 = _gate_02(store, frame_entries)
        gates.append(g02)
        if not ok02:
            inv = g02["inventory"]
            shortfall = (
                f"frame.json {'present' if inv['frame_json'] else 'missing'}; "
                f"Pass A {inv['pass_a_records']}/50; "
                f"Pass B {inv['pass_b_records']}/50; "
                f"gold {inv['pass_gold_records']}/10; "
                f"adjudication {inv['adjudication_records']}/50; "
                f"effort log {inv['effort_log_events']} events")
            if g02["missing_files"]:
                shortfall += ("; missing files: "
                              + ", ".join(g02["missing_files"]))
            outcome = "PILOT-PASS RECORDS NOT PRODUCIBLE"
            headline_paragraph = (
                "Spec 058 closes at step 0: the recorded Phase-132 "
                f"pilot passes could not be produced as a complete "
                f"record set ({shortfall}). The committed repository "
                "record carries the pilot's metrics, frame, and "
                "adjudicated dataset, but not the per-pass codings "
                "arm A exists to re-analyse. No localisation quantity "
                "was computed, and no substitute source was used. "
                "Design D-21 arm A remains unrun; its unblocking act "
                "is the preservation of the pilot-pass record set as "
                "a committed, hashed record.")
        else:
            mod = _load_metrics_module()
            # Gate 0.3 — frame identity.
            store_frame = json.loads(
                (store / "frame.json").read_text("utf-8"))
            frame_equal = store_frame["frame"] == frame_entries
            gates.append({
                "gate": "0.3", "name": "Frame identity",
                "verdict": "PASS" if frame_equal else "FAIL",
                "frame_list_equal": frame_equal})
            if not frame_equal:
                outcome = "INVALID"
                headline_paragraph = (
                    "Spec 058 stops as INVALID at gate 0.3: the "
                    "produced store's frame list differs from the "
                    "committed pilot frame. No localisation quantity "
                    "was computed. The Spec 023 pilot record stands "
                    "exactly as recorded; the failure is in this "
                    "spec's inputs, not in the pilot.")
            else:
                # Gate 0.4 — reproduction of the committed metrics.
                committed_metrics = json.loads(
                    (_REPO / METRICS_REL).read_text("utf-8"))
                repro_error = None
                try:
                    computed = mod.compute_metrics(store)
                except Exception as exc:  # noqa: BLE001
                    computed, repro_error = None, str(exc)
                full_equal = computed == committed_metrics
                repro = {
                    "full_record_equal": full_equal,
                    "error": repro_error,
                }
                if computed is not None:
                    repro.update({
                        "exact_sequence_agreement_all_50_p":
                            computed["exact_sequence_agreement"]
                            ["all_50"]["p"]["rate"],
                        "per_token_agreement_all_50":
                            computed["per_token_agreement"]
                            ["all_50"]["p"]["rate"],
                        "per_token_agreement_gold":
                            computed["per_token_agreement"]
                            ["gold_sample"]["p"]["rate"],
                        "gold_error_estimator_p":
                            computed["gold_error_estimator"]["p"]["rate"],
                        "total_tokens_pass_a":
                            computed["counts"]["total_tokens_pass_a"],
                        "total_tokens_pass_b":
                            computed["counts"]["total_tokens_pass_b"],
                        "total_tokens_pass_gold":
                            computed["counts"]["total_tokens_pass_gold"],
                        "total_tokens_adjudicated_final":
                            computed["counts"]
                            ["total_tokens_adjudicated_final"],
                    })
                gates.append({
                    "gate": "0.4",
                    "name": "Reproduction of the committed metrics",
                    "verdict": "PASS" if full_equal else "FAIL",
                    "reproduction": repro})
                if not full_equal:
                    outcome = "INVALID"
                    headline_paragraph = (
                        "Spec 058 stops as INVALID at gate 0.4: the "
                        "metrics computed from the produced store by "
                        "the frozen metrics module do not equal the "
                        "committed metrics file exactly"
                        + (f" (computation error: {repro_error})"
                           if repro_error else "")
                        + ". No localisation quantity was computed. "
                        "The Spec 023 pilot record stands exactly as "
                        "recorded; the failure is in this spec's "
                        "inputs, not in the pilot.")
                else:
                    # Gate 0.5 — taxonomy cross-check.
                    keys = [e["canonical_key"] for e in frame_entries]
                    taxonomy = _taxonomy(store, keys)
                    tax_ok = taxonomy == EXPECTED_TAXONOMY
                    gates.append({
                        "gate": "0.5",
                        "name": "Adjudication-taxonomy cross-check",
                        "verdict": "PASS" if tax_ok else "FAIL",
                        "taxonomy": taxonomy,
                        "taxonomy_total": sum(taxonomy.values()),
                        "expected": EXPECTED_TAXONOMY})
                    if not tax_ok:
                        outcome = "INVALID"
                        headline_paragraph = (
                            "Spec 058 stops as INVALID at gate 0.5: "
                            "the adjudication taxonomy recomputed "
                            f"from the produced records is {taxonomy}, "
                            "not the pilot report's section 4(c) "
                            "counts (identity 93, legibility 45, "
                            "count 11, key 10, orientation 2, order 1; "
                            "total 162). No localisation quantity was "
                            "computed. The Spec 023 pilot record "
                            "stands exactly as recorded; the failure "
                            "is in this spec's inputs, not in the "
                            "pilot.")
                    else:
                        # Gate 0.6 — analysis census.
                        per_object = {
                            r["key"]: r
                            for r in computed["per_object"]}
                        census = []
                        for e in frame_entries:
                            k = e["canonical_key"]
                            row = per_object[k]
                            if not row["exact_p"]:
                                census.append({
                                    "key": k,
                                    "site": e["site"],
                                    "object_type_recorded":
                                        e.get("object_type") or "",
                                    "gold": bool(e.get("gold")),
                                    "len_pass_a": row["len_pass_a"],
                                    "len_pass_b": row["len_pass_b"],
                                })
                        gates.append({
                            "gate": "0.6", "name": "Analysis census",
                            "verdict": "PASS",
                            "mismatched_objects": len(census),
                            "census": census})
                        census_keys = [c["key"] for c in census]
                        data = mod.load_store(store)
                        p_space = _analyse(
                            mod, data, frame_by_key, census_keys, "p")
                        m_space = _analyse(
                            mod, data, frame_by_key, census_keys, "m")
                        analysis = p_space
                        m_sensitivity = m_space
                        outcome, headline_paragraph = _headline(
                            p_space["primary"])

    anchors_after = _sha256(_REPO / "backend/reports/"
                            "INDUS_FINAL_ANCHORS.json")
    assert anchors_after == anchors_before == PIN_ANCHORS, \
        "anchors file changed during the run"

    if census is None and gates and gates[-1]["gate"] == "0.6":
        census = gates[-1]["census"]
    rec = {
        "phase": "Phase-420",
        "spec": "058-transcription-disagreement-mechanism",
        "design": "D-21 arm A",
        "claim_id": CLAIM_ID,
        "claim_status": "SETTLED — CONTRADICTED (unchanged)",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": "86dgh",
        "execution_date": EXECUTION_DATE,
        "base_commit": BASE_COMMIT,
        "outcome": outcome,
        "headline_paragraph": headline_paragraph,
        "fence_sentence": FENCE_SENTENCE,
        "step0": gates,
        "census": census,
        "analysis": analysis,
        "m_space_sensitivity": m_sensitivity,
        "anchors_before": anchors_before,
        "anchors_after": anchors_after,
        "anchors_byte_identical": anchors_before == anchors_after,
        "ai_disclosure": (
            "Executed by an AI agent (Muse Spark, via Muse) "
            "at the direction of Tristen Pierson, per constitution "
            "sec.VI."),
    }
    _OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    _OUT_RESULTS.write_text(
        json.dumps(rec, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n", "utf-8")
    _OUT_REPORT.write_text("\n".join(_report_lines(rec)), "utf-8")
    print(f"Phase-420: outcome {outcome}")
    for g in gates:
        print(f"  gate {g['gate']}: {g['verdict']}")
    if analysis:
        p = analysis["primary"]
        print(f"  E = {p['event_total_E']}; loci: "
              f"signs={p['loci']['signs']['fires']} "
              f"types={p['loci']['object_types']['fires']} "
              f"segmentation={p['loci']['segmentation']['fires']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
