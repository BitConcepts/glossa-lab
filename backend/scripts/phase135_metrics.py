"""Phase-135 (spec 024, Stage 1) — dataset assembly + metrics.

Reads ONLY the on-disk coding records in the gitignored local
store (pass_a / pass_b / pass_gold batch record dirs and the
adjudication record dir) plus the committed frame record. Computes
every quantity frozen in stage1-freeze.md §5, assembles the
publishable dataset (codes are this program's own work product;
images never leave the local store), and applies the §4.5 gates.

Per the Phase-132 §4(d) process finding, coder self-reports are
never used: a quantity exists only if it is computed here from
record files. The script fails loudly on any incomplete or
malformed record set rather than estimating around it.
"""

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
PILOT = MAIN_CHECKOUT / "corpora" / "downloads" / \
    "cisi_image_layer" / "phase135_pilot"
FRAME = REPO_ROOT / "data" / "evidence_integration" / \
    "phase135_pilot_frame.json"
DATASET_OUT = REPO_ROOT / "data" / "evidence_integration" / \
    "phase135_pilot_dataset.json"
META_OUT = REPO_ROOT / "data" / "evidence_integration" / \
    "phase135_pilot_dataset_meta.json"
METRICS_OUT = REPO_ROOT / "reports" / "phase135_pilot_metrics.json"

CATEGORIES = ["UNICORN", "ZEBU", "BUFFALO", "ELEPHANT",
              "RHINOCEROS", "GOAT_ANTELOPE", "TIGER", "COMPOSITE",
              "HUMAN_CULT", "GEOMETRIC", "SCRIPT_ONLY", "ILLEGIBLE"]

DISCLOSURE = ("All coding roles in this pilot (pass_a, pass_b, "
              "pass_gold, adjudicator) were executed by AI agents "
              "(Muse Spark, via Muse) in blinded "
              "role-isolated instances, at the direction of "
              "Tristen Pierson (constitution §VI; spec 024 "
              "§4.4). Agreement numbers are properties of this "
              "coding pipeline, never of human expert coding.")


def load_pass(batch_names):
    records, efforts = {}, {}
    for name in batch_names:
        recdir = PILOT / name / "records"
        files = sorted(
            (p for p in recdir.glob("*.json")
             if p.name != "_start.json"),
            key=lambda p: p.stat().st_mtime)
        start = recdir / "_start.json"
        start_mtime = start.stat().st_mtime if start.exists() \
            else None
        deltas = []
        prev = start_mtime
        for path in files:
            rec = json.loads(path.read_text())
            key = rec["canonical_key"]
            if key in records:
                raise SystemExit(f"duplicate record for {key}")
            if rec["primary_motif"] not in CATEGORIES:
                raise SystemExit(
                    f"{key}: primary_motif {rec['primary_motif']!r} "
                    "not in the frozen taxonomy")
            for sec in rec.get("secondary_motifs", []):
                if sec not in CATEGORIES:
                    raise SystemExit(
                        f"{key}: secondary {sec!r} not in taxonomy")
            records[key] = rec
            mtime = path.stat().st_mtime
            if prev is not None:
                deltas.append(mtime - prev)
            prev = mtime
        efforts[name] = {
            "n_records": len(files),
            "setup_seconds": (deltas[0] if deltas and
                              start_mtime is not None else None),
            "per_object_seconds": deltas[1:] if start_mtime
            is not None else deltas,
            "wall_seconds": (files[-1].stat().st_mtime - start_mtime
                             if files and start_mtime is not None
                             else None)}
    return records, efforts


def effort_summary(efforts):
    out = {}
    for name, e in efforts.items():
        secs = e["per_object_seconds"]
        out[name] = {
            "n_records": e["n_records"],
            "setup_seconds": e["setup_seconds"],
            "per_object_median_s":
                statistics.median(secs) if secs else None,
            "per_object_mean_s":
                statistics.mean(secs) if secs else None,
            "wall_seconds": e["wall_seconds"]}
    return out


def cohens_kappa(a_codes, b_codes):
    n = len(a_codes)
    matrix = Counter(zip(a_codes, b_codes))
    po = sum(v for (x, y), v in matrix.items() if x == y) / n
    a_marg = Counter(a_codes)
    b_marg = Counter(b_codes)
    pe = sum((a_marg[c] / n) * (b_marg[c] / n) for c in CATEGORIES)
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return kappa, po, pe, matrix


def main() -> int:
    frame_doc = json.loads(FRAME.read_text())
    frame = frame_doc["frame"]
    frame_keys = [o["canonical_key"] for o in frame]
    gold_keys = frame_doc["gold_keys"]

    pass_a, eff_a = load_pass(
        [f"pass_a_batch{i}" for i in range(1, 5)])
    pass_b, eff_b = load_pass([f"pass_b_batch{i}" for i in range(1, 5)])
    pass_g, eff_g = load_pass(["pass_gold_batch1"])

    for name, recs, expect in (
            ("pass_a", pass_a, set(frame_keys)),
            ("pass_b", pass_b, set(frame_keys)),
            ("pass_gold", pass_g, set(gold_keys))):
        if set(recs) != expect:
            missing = sorted(expect - set(recs))
            extra = sorted(set(recs) - expect)
            raise SystemExit(
                f"{name}: record set mismatch; missing={missing} "
                f"extra={extra}")

    adj_dir = PILOT / "adjudication" / "records"
    adjudications = {}
    for path in adj_dir.glob("*.json"):
        if path.name == "_start.json":
            continue
        rec = json.loads(path.read_text())
        if rec["adjudicated_primary"] not in CATEGORIES:
            raise SystemExit(
                f"adjudication {path.name}: code not in taxonomy")
        adjudications[rec["canonical_key"]] = rec

    disagreements = [k for k in frame_keys
                     if pass_a[k]["primary_motif"]
                     != pass_b[k]["primary_motif"]]
    if set(adjudications) != set(disagreements):
        raise SystemExit(
            "adjudication set != disagreement set: "
            f"missing={sorted(set(disagreements) - set(adjudications))} "
            f"extra={sorted(set(adjudications) - set(disagreements))}")

    a_codes = [pass_a[k]["primary_motif"] for k in frame_keys]
    b_codes = [pass_b[k]["primary_motif"] for k in frame_keys]
    kappa, po, pe, matrix = cohens_kappa(a_codes, b_codes)
    exact = po

    per_category = {}
    for c in CATEGORIES:
        union = [k for k in frame_keys
                 if pass_a[k]["primary_motif"] == c
                 or pass_b[k]["primary_motif"] == c]
        agree = [k for k in union
                 if pass_a[k]["primary_motif"]
                 == pass_b[k]["primary_motif"] == c]
        per_category[c] = {
            "pass_a_count": a_codes.count(c),
            "pass_b_count": b_codes.count(c),
            "union": len(union), "agreements": len(agree),
            "agreement_rate": (len(agree) / len(union)
                               if union else None)}

    confusion = [{"pass_a": x, "pass_b": y, "count": v}
                 for (x, y), v in sorted(
                     matrix.items(), key=lambda kv: -kv[1])
                 if x != y]

    gold = {}
    for k in gold_keys:
        trio = (pass_a[k]["primary_motif"],
                pass_b[k]["primary_motif"],
                pass_g[k]["primary_motif"])
        gold[k] = trio
    gold_pairs = {
        pair: sum(1 for t in gold.values() if t[i] == t[j]) / 20
        for pair, (i, j) in {"A-B": (0, 1), "A-G": (0, 2),
                            "B-G": (1, 2)}.items()}
    gold_unanimous = sum(1 for t in gold.values()
                         if t[0] == t[1] == t[2]) / 20

    dataset, disagreement_log = [], []
    for obj in frame:
        k = obj["canonical_key"]
        row = {
            "canonical_key": k, "volume": obj["volume"],
            "cisi_id": obj["cisi_id"], "site": obj["site"],
            "site_group": obj["site_group"],
            "object_type": obj["object_type"], "gold": obj["gold"],
            "motif_chapter_family": obj["motif_chapter_family"],
            "pass_a_primary": pass_a[k]["primary_motif"],
            "pass_a_secondary": pass_a[k].get("secondary_motifs", []),
            "pass_a_note": pass_a[k].get("note", ""),
            "pass_b_primary": pass_b[k]["primary_motif"],
            "pass_b_secondary": pass_b[k].get("secondary_motifs", []),
            "pass_b_note": pass_b[k].get("note", ""),
            "pass_gold_primary": (pass_g[k]["primary_motif"]
                                  if k in pass_g else None),
            "agreement": pass_a[k]["primary_motif"]
            == pass_b[k]["primary_motif"]}
        if k in adjudications:
            row["adjudicated_primary"] = \
                adjudications[k]["adjudicated_primary"]
            row["ruling_note"] = adjudications[k].get(
                "ruling_note", "")
            disagreement_log.append({
                "canonical_key": k,
                "pass_a_primary": row["pass_a_primary"],
                "pass_a_note": row["pass_a_note"],
                "pass_b_primary": row["pass_b_primary"],
                "pass_b_note": row["pass_b_note"],
                "pass_gold_primary": row["pass_gold_primary"],
                "adjudicated_primary": row["adjudicated_primary"],
                "ruling_note": row["ruling_note"]})
        else:
            row["adjudicated_primary"] = row["pass_a_primary"]
            row["ruling_note"] = None
        dataset.append(row)

    conc_objects = [r for r in dataset
                    if r["motif_chapter_family"] == "UNICORN"]
    concordance = {
        "n_sampled_with_unicorn_chapter": len(conc_objects),
        "adjudicated_unicorn": sum(
            1 for r in conc_objects
            if r["adjudicated_primary"] == "UNICORN"),
        "adjudicated_other": sum(
            1 for r in conc_objects
            if r["adjudicated_primary"] != "UNICORN"),
        "note": "Descriptive concordance only (stage1-freeze "
                "§6): the catalogue chapter is a comparison, "
                "never ground truth; NONMAPPABLE families are "
                "excluded by the frozen rule."}

    proceed = exact >= 0.85 and kappa >= 0.75
    stop = exact < 0.70 or kappa < 0.50
    verdict = ("PROCEED_GATE_MET" if proceed else
               "STOP_RULE_FIRED" if stop else "MIDDLE_BAND")

    metrics = {
        "phase": 135, "spec": "024", "stage": 1,
        "n_sample": len(frame_keys),
        "exact_agreement": exact,
        "agreements": sum(1 for x, y in zip(a_codes, b_codes)
                          if x == y),
        "cohens_kappa": kappa, "expected_agreement_pe": pe,
        "marginals": {"pass_a": dict(Counter(a_codes)),
                      "pass_b": dict(Counter(b_codes))},
        "per_category": per_category,
        "confusion_pairs": confusion,
        "adjudication_rate": len(disagreements) / len(frame_keys),
        "n_disagreements": len(disagreements),
        "gold_drift": {"pairwise_agreement": gold_pairs,
                       "unanimous_rate": gold_unanimous,
                       "n_gold": len(gold_keys)},
        "effort": {"pass_a": effort_summary(eff_a),
                   "pass_b": effort_summary(eff_b),
                   "pass_gold": effort_summary(eff_g),
                   "method": "record-file mtimes within each "
                             "batch (setup = _start marker to "
                             "first record; per-object = "
                             "successive record deltas). "
                             "AI-agent wall times under this "
                             "pipeline."},
        "concordance_motif_chapter": concordance,
        "gates": {"proceed_gate": {"exact_min": 0.85,
                                   "kappa_min": 0.75,
                                   "met": proceed},
                  "stop_rule": {"exact_below": 0.70,
                                "kappa_below": 0.50,
                                "fired": stop},
                  "verdict": verdict},
        "ai_disclosure": DISCLOSURE}

    dataset_doc = {
        "phase": 135, "spec": "024", "stage": 1,
        "frame_seed": frame_doc["seed"],
        "categories": CATEGORIES,
        "records": dataset,
        "disagreement_log": disagreement_log,
        "ai_disclosure": DISCLOSURE}
    DATASET_OUT.write_text(
        json.dumps(dataset_doc, indent=2, ensure_ascii=False) + "\n")

    meta = {
        "dataset": "phase135_pilot_dataset.json",
        "provenance": "Motif codes produced by this program's "
                      "Stage 1 re-pilot (Phase-135; blinded double coding + "
                      "adjudication) over CISI Vols. 1-2 "
                      "photographs in the local store; object "
                      "metadata (site, object type) from the "
                      "Phase-124 CISI catalogue (local research "
                      "material). Images are NOT included and "
                      "never leave the local store.",
        "license": "Codes, counts, and metadata in this dataset "
                   "are this program's own work product, "
                   "published CC BY 4.0 with the combined "
                   "motif-arm record (Zenodo v4.7.0) under the "
                   "owner's combined-path approval of "
                   "2026-10-09 (stage1-freeze-2.md).",
        "recorder_provenance": "pass_a / pass_b / pass_gold / "
                               "adjudicator — AI agents, blinded "
                               "role-isolated instances (see "
                               "ai_disclosure in the dataset).",
        "ai_disclosure": DISCLOSURE}
    META_OUT.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    METRICS_OUT.parent.mkdir(parents=True, exist_ok=True)
    METRICS_OUT.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "n": len(frame_keys), "exact_agreement": exact,
        "kappa": kappa, "verdict": verdict,
        "n_disagreements": len(disagreements),
        "gold": gold_pairs, "gold_unanimous": gold_unanimous},
        indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
