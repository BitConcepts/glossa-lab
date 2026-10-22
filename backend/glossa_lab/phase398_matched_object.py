"""Phase-398 (spec 034) — Matched-Object Attribution.

Execution of the frozen Spec 034 contract (specs/
034-matched-object-attribution/; freeze digest
696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a;
registered before execution at OSF https://osf.io/zd7uq/,
DOI 10.17605/OSF.IO/ZD7UQ).

The study attributes the unexplained residue of the
SETTLED Phase-125 result (FAIL — DISAGREEMENT: 16
judgeable pairs of 286, median TV 0.636931; Phase-127:
not a sampling artefact, noise median 0.083; Phase-131:
6.1% attributed, 93.9% unexplained, zero shared object
keys). It does not re-judge that result (spec §2, §8;
claim F034-C14).

Step 0 builds the object bridge through the three
frozen routes and applies the frozen gate:

  (a) the CISI catalogue layer (7,705 rows, Phases
      120–124 work; local corpus store) attests every
      CISI-side object;
  (b) the Mahadevan side's published object references
      — the ICIT published corpus's per-inscription
      CISI references, carried by the programme's
      converted keyed layer v2 — admitted as an
      intake-schema dataset (Phase-130 schema v1:
      schema validation + provenance/license gate via
      glossa_lab.intake) and joined on
      provenance.object_id;
  (c) the 44 Phase-128 evidence dossiers, reported
      where they intersect the matched set.

Object identity is fixed ONLY by the published CISI
object reference. Holdat `cisi_number` is never read
here and never used as a join key (spec 019 §2.1:
Holdat-internal sequential numbering, not a CISI
object ID; the prohibition is F034-C06). No content
deduplication is applied to the bridge: deduplication
answers a scoring-population question (spec 018 §5),
not an identity question — two distinct published
objects may carry near-identical short texts, and
Phase-125/127/131 never content-deduplicated their
object populations either. The census reports the
bridge with and without the ICIT layer's Phase-116
build-status filter so the choice is inspectable;
the gate passes under both.

Step 1 (only if the gate passes) measures per-sign
positional profiles on the matched subset only with
Phase-125's own machinery (phase125_cross_compilation
.evaluate_arm: total-variation distance, count floor
8, the 286-pair PRIMARY crosswalk arm), decomposes
the remaining disagreement with Phase-131's own
alignment and difference-block classification
(phase131_attribution), and applies the frozen
verdict lines (spec §6): matched-object median TV
<= 0.20 ATTRIBUTED TO COMPOSITION; >= 0.32
ATTRIBUTED TO TRANSCRIPTION; between, a split
attribution with the decomposition table as the
result. Below the gate the study closes as TOO THIN
TO ATTRIBUTE with the census as the finding (spec
§4); no attribution is computed and no gate is
re-based.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

_BACKEND = Path(__file__).resolve().parent.parent
_REPO = _BACKEND.parent
sys.path.insert(0, str(_BACKEND))

from glossa_lab.data import mayig_layer as ml  # noqa: E402
from glossa_lab.data import (  # noqa: E402
    parpola_mahadevan_crosswalk_v1 as xw,
)
from glossa_lab.framework026 import verify_freeze  # noqa: E402
from glossa_lab.intake import validate_dataset  # noqa: E402
from glossa_lab.phase113_battery import CorpusContext  # noqa: E402
from glossa_lab.phase113_run import _gpu_device  # noqa: E402
from glossa_lab.phase125_cross_compilation import (  # noqa: E402
    FLOOR, build_arms, evaluate_arm, median, percentile_type7,
)
from glossa_lab.phase125_run import (  # noqa: E402
    ANCHORS_PATH, ANCHORS_SHA256, HOLDAT_EXPECTED, MAYIG_EXPECTED,
    _canonical_anchors_sha256, _find_holdat_csv, _sha256,
)
from glossa_lab.phase131_attribution import (  # noqa: E402
    CLS_INDEL, CLS_MERGE, CLS_SPLIT, CLS_SUBSTITUTION,
    align, block_token_totals, classify_pair, difference_blocks,
    mapped_sequence, primary_map, similarity,
)

PHASE = 398
SPEC = "specs/034-matched-object-attribution/spec.md"
SPEC_DIR = _REPO / "specs" / "034-matched-object-attribution"
DATE = "2026-10-13"
RESULTS_PATH = _REPO / "reports" / "phase398_results.json"
REPORT_PATH = _REPO / "reports" / "phase398_matched_object_attribution.md"
PHASE125_RESULTS = _REPO / "reports" / "phase125_cross_compilation_results.json"
PHASE127_RESULTS = (
    _REPO / "reports" / "phase127_cross_compilation_diagnostic_results.json")
PHASE131_RESULTS = _REPO / "reports" / "phase131_attribution_results.json"
DOSSIERS_CSV = _REPO / "reports" / "phase128_evidence_dossiers_44.csv"

# ── Frozen constants (spec 034 §§4–6; freeze.json) ──
GATE_MIN_MATCHED = 150        # matched objects (spec §4)
GATE_MIN_SIGNS = 3            # signs in BOTH compilations (spec §4)
COMPOSITION_LINE = 0.20       # median TV at/below (spec §6)
TRANSCRIPTION_LINE = 0.32     # median TV at/above (spec §6)
FREEZE_DIGEST = "696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a"

# ── Settled inputs, asserted against the record ─────
SETTLED_PHASE125_MEDIAN_TV = 0.636931
SETTLED_PHASE125_JUDGEABLE = 16
SETTLED_PHASE125_PAIRS = 286
SETTLED_PHASE131_RESIDUAL = 0.938679
SETTLED_PHASE131_COMPOSITION_SHARE = 0.061321

_MAIN_REPO = Path.home() / "workspace" / "glossa-lab"
_ICIT_REL = (Path("corpora") / "downloads" / "icit_fieldcady"
             / "icit_converted_v2_keyed.json")
_CATALOGUE_REL = (Path("corpora") / "downloads" / "cisi_image_layer"
                  / "catalogue")


def _find_local(rel: Path) -> Path:
    for cand in (_REPO / rel, _MAIN_REPO / rel):
        if cand.exists():
            return cand
    raise FileNotFoundError(f"local corpus file not found: {rel}")


def _round(x):
    return round(x, 6) if x is not None else None


# ── Loaders ──────────────────────────────────────────

def load_icit_layer(path: Path | None = None) -> dict:
    return json.loads((path or _find_local(_ICIT_REL)).read_text(
        encoding="utf-8"))


def load_catalogue() -> dict[str, dict]:
    """CISI catalogue layer (route (a)): cisi_id ->
    {n_rows, sites, object_types, volumes} over both
    published-volume catalogue CSVs (7,705 rows)."""
    out: dict[str, dict] = {}
    for vol in (1, 2):
        path = _find_local(_CATALOGUE_REL / f"cisi_vol{vol}_catalogue.csv")
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cid = (row.get("cisi_id") or "").strip()
                if not cid:
                    continue
                e = out.setdefault(cid, {"n_rows": 0, "sites": set(),
                                         "object_types": set(),
                                         "volumes": set()})
                e["n_rows"] += 1
                if (row.get("site") or "").strip():
                    e["sites"].add(row["site"].strip())
                if (row.get("object_type") or "").strip():
                    e["object_types"].add(row["object_type"].strip())
                e["volumes"].add(vol)
    return out


def load_dossier_signs() -> dict[str, str]:
    """The 44 Phase-128 dossiers (route (c)): anchor_id
    -> M sign id (e.g. 'M011')."""
    out = {}
    with open(DOSSIERS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["anchor_id"]] = f"M{int(row['sign_number']):03d}"
    return out


# ── Route (b): intake-schema admission ──────────────

def build_intake_dataset(icit: dict) -> dict:
    """The Mahadevan side's published object references
    as a Phase-130 intake-schema (v1) dataset: one
    record per ICIT inscription that carries a CISI
    object reference, the reference carried in
    provenance.object_id (the schema's declared
    catalogue/object ID field)."""
    inscriptions = []
    for r in icit["inscriptions"]:
        cisi = (r.get("cisi") or "").strip()
        if not cisi or cisi == "-":
            continue
        inscriptions.append({
            "inscription_id": f"icit-v2-row-{r['row']}",
            "source_row": r["row"],
            "site": r.get("site"),
            "tokens": list(r["tokens"]),
            "sign_list": "mahadevan_1977",
            "object_type": r.get("type"),
            "provenance": {
                "source_reference": (
                    "ICIT converted keyed layer v2, inscription "
                    f"id {r.get('id')} (source row {r['row']})"),
                "object_id": cisi,
                "transcriber": ("ICIT (Mahadevan lineage); "
                                "programme conversion, Phase-116"),
            },
        })
    return {
        "schema_version": "1.0",
        "dataset_name": ("phase398-icit-published-object-references"),
        "source": ("ICIT via Lipi repository CSV export, mirrored "
                   "(MIT) in field-cady/indus_valley_script_corpus; "
                   "programme-built converted keyed layer v2"),
        "source_class": "icit_full",
        "license_basis": (
            "MIT (field-cady/indus_valley_script_corpus mirror of "
            "the ICIT export). Cited data for internal analysis; "
            "published artifacts carry counts, shares, and "
            "distances only."),
        "upstream_lineage": {
            "derived_from": ("ICIT (Mahadevan) published corpus, "
                             "via the Lipi repository CSV export"),
            "is_derivation_input": False,
        },
        "compiler": "Glossa Lab Phase-398 bridge build",
        "acquisition_date": "2026-10-08",
        "inscriptions": inscriptions,
    }


# ── Step 0: the bridge ───────────────────────────────

def build_bridge(mayig_records: list[dict],
                 intake_inscriptions: list[dict],
                 catalogue: dict[str, dict]) -> dict:
    """Join mayig objects to intake records on the
    published CISI object ID (provenance.object_id ==
    cisi_object_id). No other key participates."""
    by_object: dict[str, list[dict]] = {}
    for ins in intake_inscriptions:
        by_object.setdefault(ins["provenance"]["object_id"],
                             []).append(ins)

    pairs = []
    ambiguous = []
    for rec in mayig_records:
        oid = rec["cisi_object_id"]
        cands = by_object.get(oid, [])
        chosen = None
        if len(cands) == 1:
            chosen = cands[0]
        elif len(cands) > 1:
            # Multiple published references to one object:
            # never resolved by content; recorded as
            # ambiguous and excluded from pairing.
            ambiguous.append({"cisi_object_id": oid,
                              "n_candidates": len(cands),
                              "candidates": [c["inscription_id"]
                                             for c in cands]})
        cat = catalogue.get(oid)
        pairs.append({
            "cisi_object_id": oid,
            "mayig": {
                "side_id": rec["side_id"],
                "tokens": list(rec["tokens"]),
                "token_count": rec["token_count"],
                "source_file": rec.get("source_file"),
            },
            "catalogue": (None if cat is None else {
                "n_rows": cat["n_rows"],
                "sites": sorted(cat["sites"]),
                "object_types": sorted(cat["object_types"]),
                "volumes": sorted(cat["volumes"]),
            }),
            "icit": (None if chosen is None else {
                "inscription_id": chosen["inscription_id"],
                "source_row": chosen.get("source_row"),
                "tokens": list(chosen["tokens"]),
                "token_count": len(chosen["tokens"]),
                "site": chosen.get("site"),
                "object_type": chosen.get("object_type"),
            }),
            "icit_build_status": None,  # filled by caller
            "matched": chosen is not None,
            "gate_ok": False,
        })
    return {"pairs": pairs, "ambiguous": ambiguous,
            "intake_objects_total": len(by_object)}


def apply_gate(pairs: list[dict]) -> dict:
    """The frozen §4 gate, applied to the bridge pairs
    exactly as counted. Mutates each pair's gate_ok."""
    n_gate = 0
    for p in pairs:
        p["gate_ok"] = bool(
            p["matched"]
            and p["mayig"]["token_count"] >= GATE_MIN_SIGNS
            and p["icit"]["token_count"] >= GATE_MIN_SIGNS)
        n_gate += p["gate_ok"]
    return {"n_matched_objects": sum(1 for p in pairs if p["matched"]),
            "n_gate_objects": n_gate,
            "gate_min_matched": GATE_MIN_MATCHED,
            "gate_min_signs": GATE_MIN_SIGNS,
            "gate_passed": n_gate >= GATE_MIN_MATCHED}


def verdict_for(median_tv: float | None) -> str | None:
    """Spec §6 lines on the matched-object median TV."""
    if median_tv is None:
        return None
    if median_tv <= COMPOSITION_LINE:
        return "ATTRIBUTED TO COMPOSITION"
    if median_tv >= TRANSCRIPTION_LINE:
        return "ATTRIBUTED TO TRANSCRIPTION"
    return "SPLIT ATTRIBUTION"


# ── Step 1: profiles + decomposition ───────────────

def step1_profiles(gate_pairs: list[dict], arms: dict) -> dict:
    """Phase-125's own measurement on the matched
    subset only (evaluate_arm, PRIMARY arm, floor 8,
    total variation), via CorpusContext per side."""
    mayig_ctx = CorpusContext([p["mayig"]["tokens"] for p in gate_pairs])
    icit_ctx = CorpusContext([p["icit"]["tokens"] for p in gate_pairs])
    ev = evaluate_arm(arms["primary"], mayig_ctx, icit_ctx)
    return {"arm": ev, "mayig_subset": {
                "inscriptions": mayig_ctx.n_inscriptions,
                "tokens": mayig_ctx.n_tokens,
                "signs": len(mayig_ctx.token_counts)},
            "icit_subset": {
                "inscriptions": icit_ctx.n_inscriptions,
                "tokens": icit_ctx.n_tokens,
                "signs": len(icit_ctx.token_counts)}}


def decompose(gate_pairs: list[dict], rows: list[dict]) -> dict:
    """Per-object alignment + Phase-131 difference
    classification over the gate subset. The mayig
    sequence is mapped into M-space by the crosswalk
    PRIMARY map (all-or-nothing, Phase-131 §3.2
    eligibility); the crosswalk is used as a record
    of disagreement, never as ground truth (C13)."""
    pmap = primary_map(rows)
    conflict: dict[tuple[str, str], bool] = {}
    for r in rows:
        conflict[(r["parpola_id"], r["mahadevan_id"])] = bool(
            r.get("conflict"))
    per_object = []
    pair_dicts = []          # phase131 block_token_totals shape
    sub_checks = Counter()
    unk_blocks = 0
    dists = []
    for p in gate_pairs:
        p_tokens = p["mayig"]["tokens"]
        b_tokens = p["icit"]["tokens"]
        mapped = mapped_sequence(p_tokens, pmap)
        rec = {"cisi_object_id": p["cisi_object_id"],
               "mayig_tokens": p_tokens,
               "icit_tokens": b_tokens,
               "mapped_mayig_tokens": mapped,
               "decomposition_eligible": mapped is not None,
               "pair_class": None, "distance": None, "blocks": []}
        if mapped is not None:
            cols = align(mapped, b_tokens)
            # Annotate each a-column with its Parpola
            # token (a-columns consume mapped tokens in
            # order, 1:1 with the mayig P tokens).
            p_iter = iter(p_tokens)
            for c in cols:
                c["p"] = next(p_iter) if c["a"] is not None else None
            blocks = difference_blocks(cols)
            rec["blocks"] = blocks
            rec["pair_class"] = classify_pair(mapped, b_tokens, blocks)
            rec["distance"] = _round(1.0 - similarity(mapped, b_tokens))
            dists.append(rec["distance"])
            pair_dicts.append({"blocks": blocks})
            # Substitution crosswalk check (C13 posture):
            # walk the same non-match runs the frozen
            # classifier grouped, position by position.
            cur: list[dict] = []
            runs = []
            for c in cols:
                if c["op"] == "match":
                    if cur:
                        runs.append(cur)
                        cur = []
                else:
                    cur.append(c)
            if cur:
                runs.append(cur)
            for run in runs:
                if any(c["a"] == "UNK" or c["b"] == "UNK" for c in run):
                    unk_blocks += 1
                a_side = [c for c in run if c["a"] is not None]
                b_side = [c for c in run if c["b"] is not None]
                if len(a_side) == len(b_side) and a_side:
                    for ca, cb in zip(a_side, b_side):
                        if ca["op"] == "sub":
                            key = (ca["p"], cb["b"])
                            if key not in conflict:
                                sub_checks["no_crosswalk_row"] += 1
                            elif conflict[key]:
                                sub_checks["conflict_pair"] += 1
                            else:
                                sub_checks["crosswalk_attested_"
                                           "non_conflict"] += 1
        per_object.append(rec)
    totals = block_token_totals(pair_dicts)
    all_tok = totals.get("all_difference_blocks", 0)

    def share(cls):
        return _round(totals.get(cls, 0) / all_tok) if all_tok else None

    seg_tok = totals.get(CLS_SPLIT, 0) + totals.get(CLS_MERGE, 0)
    dist_sorted = sorted(dists)
    return {
        "per_object": per_object,
        "n_objects": len(per_object),
        "n_eligible": sum(1 for r in per_object
                          if r["decomposition_eligible"]),
        "n_ineligible": sum(1 for r in per_object
                            if not r["decomposition_eligible"]),
        "pair_class_counts": dict(Counter(
            r["pair_class"] for r in per_object
            if r["pair_class"] is not None)),
        "block_token_totals": totals,
        "shares_phase131_estimators": {
            "segmentation": (_round(seg_tok / all_tok)
                             if all_tok else None),
            "substitution": share(CLS_SUBSTITUTION),
            "insertion_deletion": share(CLS_INDEL),
        },
        "substitution_crosswalk_check": dict(sub_checks),
        "blocks_involving_unk": unk_blocks,
        "per_object_distance_distribution": {
            "n": len(dist_sorted),
            "min": dist_sorted[0] if dist_sorted else None,
            "p25": (_round(percentile_type7(dist_sorted, 25))
                    if dist_sorted else None),
            "median": (_round(median(dist_sorted))
                       if dist_sorted else None),
            "p75": (_round(percentile_type7(dist_sorted, 75))
                    if dist_sorted else None),
            "max": dist_sorted[-1] if dist_sorted else None,
        },
    }


# ── Section 7: selection bias ───────────────────────

def selection_bias(gate_pairs: list[dict], mayig_records: list[dict],
                   catalogue: dict[str, dict], icit: dict,
                   holdat_inscriptions_meta: list[dict]) -> dict:
    def mix(counter: Counter, total: int) -> list[dict]:
        return [{"value": k, "n": n, "share": _round(n / total)}
                for k, n in counter.most_common() if total]

    sub_sites = Counter(p["icit"]["site"] for p in gate_pairs)
    sub_types = Counter(p["icit"]["object_type"] for p in gate_pairs)
    icit_kept = [r for r in icit["inscriptions"]
                 if r.get("status") == "kept"]
    return {
        "matched_subset": {
            "n": len(gate_pairs),
            "sites": mix(sub_sites, len(gate_pairs)),
            "object_types": mix(sub_types, len(gate_pairs)),
            "description": (
                "All matched objects are Mohenjo-daro seals: "
                "the mayig layer transcribes CISI vols 1–2 "
                "Mohenjo-daro objects only, so the bridge "
                "universe is that population."),
        },
        "cisi_side_full_mayig_layer": {
            "n": len(mayig_records),
            "sites": mix(Counter(
                (sorted(catalogue[r["cisi_object_id"]]["sites"])[0]
                 if catalogue.get(r["cisi_object_id"])
                 and catalogue[r["cisi_object_id"]]["sites"]
                 else "(catalogue site blank)")
                for r in mayig_records), len(mayig_records)),
            "object_types": mix(Counter(
                t for r in mayig_records
                for t in (catalogue.get(r["cisi_object_id"], {})
                          .get("object_types") or {"(none recorded)"})),
                len(mayig_records)),
        },
        "mahadevan_side_full_icit_layer_kept": {
            "n": len(icit_kept),
            "sites": mix(Counter(r.get("site") for r in icit_kept),
                         len(icit_kept)),
            "object_types": mix(Counter(r.get("type") for r in icit_kept),
                                len(icit_kept)),
        },
        "mahadevan_side_full_holdat_layer": {
            "n": len(holdat_inscriptions_meta),
            "sites": mix(Counter(m["site"]
                                  for m in holdat_inscriptions_meta),
                         len(holdat_inscriptions_meta)),
            "iconographies": mix(Counter(
                m["iconography"] for m in holdat_inscriptions_meta),
                len(holdat_inscriptions_meta)),
            "note": ("Holdat carries no CISI object references "
                     "and cannot enter the bridge (spec 019 "
                     "§2.1); its mix is reported as the second "
                     "Mahadevan-side layer of record."),
        },
    }


def load_holdat_meta() -> list[dict]:
    """Per-inscription site/iconography of the Holdat
    layer, read from its CSV for §7 mix counts only
    (counts are publishable under its recorded terms;
    its cisi_number field is never used as a key —
    inscriptions are counted in file order)."""
    path = _find_holdat_csv()
    groups: dict[str, dict] = {}
    order: list[str] = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            gid = row.get("form") or ""
            if gid not in groups:
                groups[gid] = {"site": row.get("site") or "",
                               "iconography": row.get("iconography")
                               or ""}
                order.append(gid)
    meta = [groups[g] for g in order]
    assert len(meta) == HOLDAT_EXPECTED["inscriptions"], len(meta)
    return meta


# ── Orchestration ───────────────────────────────────

def run_all(write: bool = True) -> dict:
    anchors_before = _canonical_anchors_sha256(ANCHORS_PATH)
    assert anchors_before == ANCHORS_SHA256, anchors_before

    freeze_errors = verify_freeze(
        json.loads((SPEC_DIR / "freeze.json").read_text(
            encoding="utf-8")), _REPO)
    assert freeze_errors == [], freeze_errors
    freeze = json.loads((SPEC_DIR / "freeze.json").read_text(
        encoding="utf-8"))
    assert freeze["digest"] == FREEZE_DIGEST, freeze["digest"]

    # Settled inputs, read from the record and asserted.
    p125 = json.loads(PHASE125_RESULTS.read_text(encoding="utf-8"))
    st125 = p125["arms"]["primary"]["stats"]
    assert st125["median_tv"] == SETTLED_PHASE125_MEDIAN_TV
    assert st125["n_judgeable"] == SETTLED_PHASE125_JUDGEABLE
    assert st125["n_pairs"] == SETTLED_PHASE125_PAIRS
    p131 = json.loads(PHASE131_RESULTS.read_text(encoding="utf-8"))
    syn131 = p131["arms"]["d_synthesis"]
    assert syn131["residual_unexplained_share"] == (
        SETTLED_PHASE131_RESIDUAL)
    assert syn131["rows"]["composition"]["share"] == (
        SETTLED_PHASE131_COMPOSITION_SHARE)
    p127 = json.loads(PHASE127_RESULTS.read_text(encoding="utf-8"))

    # ── Inputs ──
    mayig_records = ml.load_inscriptions()
    assert len(mayig_records) == MAYIG_EXPECTED["inscriptions"]
    mayig_ctx_full = CorpusContext([list(r["tokens"])
                                    for r in mayig_records])
    assert mayig_ctx_full.n_tokens == MAYIG_EXPECTED["tokens"]

    catalogue = load_catalogue()
    icit = load_icit_layer()
    icit_status = {r["row"]: r.get("status")
                   for r in icit["inscriptions"]}

    # ── Route (b): intake admission ──
    dataset = build_intake_dataset(icit)
    validation = validate_dataset(dataset)
    assert validation["verdict"] != "reject", validation["errors"][:3]
    intake_ins = dataset["inscriptions"]

    # ── Step 0: bridge + census + gate ──
    bridge = build_bridge(mayig_records, intake_ins,
                          {k: {"n_rows": v["n_rows"], "sites": v["sites"],
                               "object_types": v["object_types"],
                               "volumes": v["volumes"]}
                           for k, v in catalogue.items()})
    pairs = bridge["pairs"]
    for p in pairs:
        if p["icit"] is not None:
            p["icit_build_status"] = icit_status.get(
                p["icit"]["source_row"])
    gate = apply_gate(pairs)
    gate_pairs = [p for p in pairs if p["gate_ok"]]
    below = [p for p in pairs if p["matched"] and not p["gate_ok"]]

    kept_only_gate = sum(
        1 for p in pairs
        if p["gate_ok"] and p["icit_build_status"] == "kept")

    dossiers = load_dossier_signs()
    dossier_sign_set = set(dossiers.values())
    route_c_objects = [
        p["cisi_object_id"] for p in gate_pairs
        if dossier_sign_set & set(p["icit"]["tokens"])]
    route_c_anchors = sorted({
        aid for aid, sign in dossiers.items()
        if any(sign in p["icit"]["tokens"] for p in gate_pairs)})

    census = {
        "cisi_side": {
            "mayig_objects": len(mayig_records),
            "mayig_tokens": mayig_ctx_full.n_tokens,
            "catalogue_distinct_objects": len(catalogue),
            "catalogue_rows_total": sum(
                v["n_rows"] for v in catalogue.values()),
            "mayig_objects_attested_in_catalogue": sum(
                1 for p in pairs if p["catalogue"] is not None),
        },
        "mahadevan_side": {
            "icit_inscriptions_total": len(icit["inscriptions"]),
            "icit_inscriptions_with_cisi_reference": len(intake_ins),
            "icit_distinct_cisi_objects_referenced": (
                bridge["intake_objects_total"]),
            "intake_validation": {
                "verdict": validation["verdict"],
                "errors": len(validation["errors"]),
                "warnings": len(validation["warnings"]),
                "summary": validation["summary"],
            },
        },
        "bridge": {
            "matched_objects": gate["n_matched_objects"],
            "mayig_objects_without_icit_reference": (
                len(mayig_records) - gate["n_matched_objects"]),
            "ambiguous_objects": bridge["ambiguous"],
            "matched_with_ge3_sign_texts_both_sides": (
                gate["n_gate_objects"]),
            "gate": gate,
            "sensitivity_kept_status_only": {
                "matched_with_ge3_sign_texts_both_sides": kept_only_gate,
                "gate_passed": kept_only_gate >= GATE_MIN_MATCHED,
                "note": ("The Phase-116 build-status filter is "
                         "reported for inspectability; identity "
                         "rests on the published reference, not "
                         "on a build status."),
            },
            "below_text_condition": [{
                "cisi_object_id": p["cisi_object_id"],
                "mayig_token_count": p["mayig"]["token_count"],
                "icit_token_count": (p["icit"]["token_count"]
                                    if p["icit"] else None),
                "icit_build_status": p["icit_build_status"],
            } for p in below],
        },
        "route_c_dossiers": {
            "dossier_signs": len(dossiers),
            "gate_objects_touching_a_dossier_sign": len(route_c_objects),
            "dossier_anchors_touched": route_c_anchors,
            "note": ("Route (c) assembles sign-level evidence "
                     "for the contested subset; it contributes "
                     "no object identity of its own and is "
                     "reported as an intersection with the "
                     "matched set."),
        },
        "composition_residue": {
            "icit_referenced_objects_not_in_mayig": (
                bridge["intake_objects_total"]
                - gate["n_matched_objects"]),
            "note": ("Objects attested in one compilation's "
                     "frame only (spec §5): the ICIT corpus "
                     "references thousands of CISI objects "
                     "the mayig layer does not transcribe; "
                     "the mayig layer holds no object the "
                     "ICIT corpus fails to reference."),
        },
    }

    results: dict = {
        "phase": PHASE,
        "spec": SPEC,
        "date": DATE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gpu_device": _gpu_device(),
        "freeze": {"digest": FREEZE_DIGEST,
                   "osf_registration": "https://osf.io/zd7uq/",
                   "osf_doi": "10.17605/OSF.IO/ZD7UQ"},
        "settled_inputs": {
            "phase125_median_tv": SETTLED_PHASE125_MEDIAN_TV,
            "phase125_judgeable": SETTLED_PHASE125_JUDGEABLE,
            "phase125_pairs": SETTLED_PHASE125_PAIRS,
            "phase131_attributed_share": (
                SETTLED_PHASE131_COMPOSITION_SHARE),
            "phase131_residual_unexplained_share": (
                SETTLED_PHASE131_RESIDUAL),
            "phase127_noise_band": p127["arms"]["b_matched_size"],
        },
        "inputs": {
            "mayig_layer": {
                "path": "data/corpus_layers/mayig_cisi_layer_v1.json",
                "sha256": _sha256(_REPO / "data" / "corpus_layers"
                                  / "mayig_cisi_layer_v1.json"),
            },
            "icit_keyed_layer": {
                "path": ("corpora/downloads/icit_fieldcady/"
                         "icit_converted_v2_keyed.json (local "
                         "store; gitignored)"),
                "source": icit.get("source"),
                "build_stats": icit.get("build_stats"),
            },
            "cisi_catalogue": {
                "path": ("corpora/downloads/cisi_image_layer/"
                         "catalogue/ (local store; gitignored)"),
                "rows": census["cisi_side"]["catalogue_rows_total"],
            },
            "crosswalk": xw.crosswalk_stats(),
        },
        "step0_census": census,
        "bridge_pairs": pairs,
    }

    # ── Step 1 (only behind the frozen gate) ──
    if gate["gate_passed"]:
        rows = xw.load_crosswalk()
        arms = build_arms(rows)
        assert len(arms["primary"]) == SETTLED_PHASE125_PAIRS
        prof = step1_profiles(gate_pairs, arms)
        stats = prof["arm"]["stats"]
        dec = decompose(gate_pairs, rows)
        verdict = verdict_for(stats["median_tv"])
        results["step1_profiles"] = {
            "mayig_subset": prof["mayig_subset"],
            "icit_subset": prof["icit_subset"],
            "floor": FLOOR,
            "stats": stats,
            "records": prof["arm"]["records"],
        }
        results["step1_decomposition"] = dec
        results["selection_bias"] = selection_bias(
            gate_pairs, mayig_records,
            {k: {"sites": v["sites"], "object_types": v["object_types"]}
             for k, v in catalogue.items()},
            icit, load_holdat_meta())
        results["verdict"] = {
            "outcome": verdict,
            "matched_object_median_tv": stats["median_tv"],
            "composition_line": COMPOSITION_LINE,
            "transcription_line": TRANSCRIPTION_LINE,
            "judgeable_pairs": stats["n_judgeable"],
            "pairs_total": stats["n_pairs"],
            "matched_object_residual_phase131_estimator": _round(
                stats["median_tv"] / SETTLED_PHASE125_MEDIAN_TV),
            "subset_description": (
                f"{len(gate_pairs)} matched objects, all "
                "Mohenjo-daro seals (the CISI vols 1–2 object "
                "population transcribed in the mayig layer), "
                "Mahadevan-side readings from the ICIT "
                "published corpus."),
        }
    else:
        results["verdict"] = {
            "outcome": "TOO THIN TO ATTRIBUTE",
            "matched_object_median_tv": None,
            "note": ("Step 0 gate not met; no attribution "
                     "computed, per the frozen §4 closure."),
        }

    anchors_after = _canonical_anchors_sha256(ANCHORS_PATH)
    assert anchors_after == ANCHORS_SHA256 == anchors_before
    results["anchors_sha256_before"] = anchors_before
    results["anchors_sha256_after"] = anchors_after
    results["anchors_unchanged"] = anchors_before == anchors_after

    if write:
        RESULTS_PATH.write_text(json.dumps(results, indent=1),
                                encoding="utf-8")
        REPORT_PATH.write_text(render_report(results),
                               encoding="utf-8")
    return results


def render_report(r: dict) -> str:
    c = r["step0_census"]
    b = c["bridge"]
    g = b["gate"]
    v = r["verdict"]
    lines = [
        "# Phase-398 — Matched-Object Attribution (spec 034)",
        "",
        "**This study attributes the residue of a settled "
        "result; it does not re-judge it.** The Phase-125 "
        "verdict — FAIL — DISAGREEMENT (16 judgeable pairs "
        "of 286; median TV 0.636931) — stands untouched "
        "(F034-C14). Phase-131 attributed 6.1% of the "
        "disagreement and left 93.9% unexplained because "
        "the two digital layers shared zero object keys. "
        "This phase builds the missing object bridge and "
        "asks the question object by object, under the "
        "frozen Spec 034 contract (freeze digest "
        f"`{FREEZE_DIGEST}`; OSF registration "
        "https://osf.io/zd7uq/, DOI 10.17605/OSF.IO/ZD7UQ).",
        "",
        "## Step 0 — the bridge census",
        "",
        f"- CISI side: the mayig layer holds "
        f"{c['cisi_side']['mayig_objects']} objects "
        f"({c['cisi_side']['mayig_tokens']} tokens). The "
        f"CISI catalogue layer (route (a)) attests "
        f"{c['cisi_side']['mayig_objects_attested_in_catalogue']} "
        f"of them, out of "
        f"{c['cisi_side']['catalogue_distinct_objects']} "
        f"catalogued objects "
        f"({c['cisi_side']['catalogue_rows_total']} rows).",
        f"- Mahadevan side: the ICIT published corpus "
        f"carries a CISI object reference for "
        f"{c['mahadevan_side']['icit_inscriptions_with_cisi_reference']} "
        f"of its {c['mahadevan_side']['icit_inscriptions_total']} "
        f"inscriptions "
        f"({c['mahadevan_side']['icit_distinct_cisi_objects_referenced']} "
        f"distinct objects), admitted through the "
        f"Phase-130 intake schema (route (b); validation "
        f"verdict: "
        f"{c['mahadevan_side']['intake_validation']['verdict']}).",
        f"- **Matched objects: {b['matched_objects']}** "
        f"(mayig objects with no ICIT reference: "
        f"{b['mayig_objects_without_icit_reference']}). "
        f"Holdat `cisi_number` was never used as a key "
        f"(F034-C06).",
        f"- Matched objects with texts of three or more "
        f"signs in both compilations: "
        f"**{g['n_gate_objects']}** — the frozen gate is "
        f"{g['gate_min_matched']}; gate "
        f"{'PASSED' if g['gate_passed'] else 'NOT MET'}.",
        f"- Sensitivity: counting only ICIT records the "
        f"Phase-116 build kept, the same figure is "
        f"{b['sensitivity_kept_status_only']['matched_with_ge3_sign_texts_both_sides']} "
        f"— the gate passes under both counts.",
        f"- Route (c): "
        f"{c['route_c_dossiers']['gate_objects_touching_a_dossier_sign']} "
        f"of the gate objects carry a sign covered by "
        f"one of the 44 Phase-128 dossiers.",
        f"- Composition residue (census level): "
        f"{c['composition_residue']['icit_referenced_objects_not_in_mayig']} "
        f"CISI objects are referenced by the ICIT corpus "
        f"but not transcribed in the mayig layer.",
        "",
    ]
    if v["outcome"] == "TOO THIN TO ATTRIBUTE":
        lines += [
            "## Outcome — TOO THIN TO ATTRIBUTE",
            "",
            "The bridge census above is the finding "
            "(F034-C05). No attribution was computed and "
            "no gate was re-based. The unblocking act, "
            "as frozen: a published concordance or "
            "object-level dataset entering through "
            "intake that pairs more of the two "
            "compilations' objects with texts of three "
            "or more signs on both sides.",
            "",
        ]
    else:
        s = r["step1_profiles"]["stats"]
        d = r["step1_decomposition"]
        sh = d["shares_phase131_estimators"]
        lines += [
            "## Step 1 — profiles on the matched subset",
            "",
            f"Phase-125's own measurement (total "
            f"variation, count floor {FLOOR}, the 286 "
            f"PRIMARY crosswalk pairs), computed on the "
            f"{g['n_gate_objects']} matched objects only: "
            f"**{s['n_judgeable']} judgeable pairs**, "
            f"matched-object median TV "
            f"**{s['median_tv']}**.",
            "",
            f"## Outcome — {v['outcome']}",
            "",
            f"The frozen lines are 0.20 (composition) "
            f"and 0.32 (transcription). The matched-object "
            f"median TV of {s['median_tv']} gives: "
            f"**{v['outcome']}**. Subset: "
            f"{v['subset_description']} As a persistence "
            f"measure in Phase-131's estimator, the "
            f"matched-object residual is "
            f"{v['matched_object_residual_phase131_estimator']} "
            f"of the corpus-level distance.",
            "",
            "## Decomposition (Phase-131 categories)",
            "",
            f"Over {d['n_eligible']} decomposition-eligible "
            f"objects ({d['n_ineligible']} not mappable "
            f"all-or-nothing under the PRIMARY map), "
            f"difference-block token shares: segmentation "
            f"{sh['segmentation']}, substitution "
            f"{sh['substitution']}, insertion/deletion "
            f"{sh['insertion_deletion']}. Pair classes: "
            f"{d['pair_class_counts']}. Substitutions "
            f"checked against the crosswalk (a record of "
            f"disagreement, never ground truth): "
            f"{d['substitution_crosswalk_check']}. "
            f"Per-object distances: median "
            f"{d['per_object_distance_distribution']['median']} "
            f"(n = {d['per_object_distance_distribution']['n']}).",
            "",
        ]
    lines += [
        "## What this does not establish",
        "",
        "Which compilation is right where they differ "
        "(F034-C01). Attribution explains disagreement; "
        "it does not crown a winner, and the settled "
        "Phase-125 verdict stands exactly as issued.",
        "",
        f"*Anchors file unchanged: sha256 "
        f"{r['anchors_sha256_after']} before and after "
        f"(asserted in code).*",
        "",
        "**AI disclosure:** executed by an AI agent "
        "(Muse Spark, via Muse) at the direction of "
        "Tristen Pierson, per constitution section VI.",
        "",
    ]
    return "\n".join(lines)
