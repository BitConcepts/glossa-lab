"""Phase-109 Step 3: individual re-reviews — M293, M362, M398 (spec 007).

Assembles full evidence dossiers from in-repo sources and applies
the pre-registered caps:

- M293: tier = highest tier its NON-SA evidence supports. The
  Phase-101 positional adjudication (2026-05-18) recorded PROMOTED
  TO MEDIUM; the MEDIUM->HIGH move was the Phase-116 SA
  recalibration gate (SA-cons=1.00 the firing disjunct, source not
  whitelisted). Absent a completed non-SA validation at HIGH
  level, the tier is MEDIUM.
- M362 / M398: the latest adjudication (Phase-105) is INCONCLUSIVE
  (freq 3, below the positional-verdict floor) and was never
  superseded; a recalibration gate is not an adjudication. Tier is
  capped at MEDIUM unless the dossier's search finds a later
  superseding adjudication.

Modes: `decide` (default; writes reports/phase109_dossier_<sign>
.json) and `apply` (tier changes + change register).

GPU: no compute; gpu_device recorded per H20 (torch guarded).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase109-step3] gpu_device={_GPU}", file=sys.stderr)

from glossa_lab.pipelines import phase109_followthrough as p109  # noqa: E402

REPO = Path(__file__).parents[2]
GLOSSA_LEDGER = REPO / "glossa-indus" / "LEDGER.md"
ROOT_LEDGER = REPO / "LEDGER.md"
VERDICT_WORDS = ("INCONCLUSIVE", "CORROBORATED", "CHALLENGED",
                 "CONFIRMED", "REJECTED", "verdict")


def _ledger_section(path: Path, start_marker: str, max_lines: int = 40) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines):
        if start_marker in ln:
            return "\n".join(lines[i:i + max_lines])
    return ""


def _adjudication_search(sign: str) -> list[dict]:
    """Post-Phase-105 adjudication search for `sign`: ledger sections
    and phase artifacts (>=106) carrying a verdict for the sign."""
    hits: list[dict] = []
    for path in (GLOSSA_LEDGER, ROOT_LEDGER):
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(re.escape(sign), text):
            span = text[max(0, m.start() - 300):m.start() + 300]
            if any(w in span for w in VERDICT_WORDS):
                hits.append({"source": str(path.relative_to(REPO)),
                             "context": span.replace("\n", " ")[-400:]})
    for base in (REPO / "reports", REPO / "outputs",
                 REPO / "backend" / "reports"):
        for f in sorted(base.glob("phase1*.json")):
            m = re.match(r"phase(\d+)", f.name)
            if not m or int(m.group(1)) < 106 or "phase109" in f.name:
                continue
            try:
                txt = f.read_text(encoding="utf-8")
            except Exception:  # noqa: BLE001
                continue
            if sign in txt and "verdict" in txt:
                hits.append({"source": str(f.relative_to(REPO)),
                             "context": "artifact mentions sign + 'verdict'"})
    return hits


def dossier_m293(anchors_data: dict, records: dict, trails: dict,
                 backups: dict) -> dict:
    sign = "M293"
    entry = anchors_data["anchors"][sign]
    p116 = p109.load_json(REPO / "outputs" / "phase116_sa_recalibration.json")
    eval_rec = next((e for e in p116.get("eval_log", [])
                     if isinstance(e, dict) and e.get("sign") == sign), None)
    section = _ledger_section(GLOSSA_LEDGER,
                              "### Phase-101: M293 DEFINITIVE RESOLUTION")
    trail = trails.get(sign, {})
    return {
        "phase": 109, "step": 3, "spec": "specs/007-phase109-follow-through",
        "gpu_device": _GPU, "sign": sign,
        "current": {"reading": entry.get("reading"),
                    "confidence": entry.get("confidence"),
                    "basis": entry.get("basis"),
                    "source": entry.get("source")},
        "register": {"category": records[sign].get("category"),
                     "sa_in_chain": records[sign].get("sa_in_chain"),
                     "reasons": records[sign].get("reasons", [])},
        "evidence_for_high": [
            "Phase-116 recalibration upgraded M293 MEDIUM->HIGH "
            "(outputs/phase116_sa_recalibration.json: sign in "
            "upgraded_signs) — but the gate's firing disjunct was "
            "SA-cons=1.00 (eval_log: source 'Phase-101 positional "
            "adjudication' not whitelisted; has_dedr=true; new SA "
            "modal was 'nal', not 'ta'). SA evidence is void after "
            "Phase-107, so this line cannot support HIGH under the "
            "no-SA-sufficient rule (H26).",
        ],
        "evidence_non_sa": [
            "Phase-101 positional adjudication (glossa-indus/LEDGER"
            ".md, 2026-05-18): M293 6.9% INITIAL vs 100% INITIAL for "
            "animal classifiers; 59.9% MEDIAL / 33.2% TERMINAL; 11x "
            "after genitive M267, 48x before case suffixes -> "
            "'ta' (DEDR 3003, body/self), a personal-name component. "
            "Its own recorded outcome: PROMOTED TO MEDIUM.",
            "Section text: " + section[:1200],
            "May-2026 backup snapshots already record 'ta' (HIGH in "
            "the file by then — the tier Phase-116 later re-asserted "
            "via the SA gate).",
            "Phase-105 used M293's profile as the known name-"
            "component reference (m293_reference_profile) — a use "
            "of the reading, not a HIGH-level validation of it.",
        ],
        "later_non_sa_high_validation_search": {
            "method": "trail ledger_mentions + artifact_mentions "
                      "reviewed; no completed non-SA validation at "
                      "HIGH level found in the recorded chain "
                      "(Phase-108 register concurs: SA_CONFIRMED_ONLY "
                      "under the load-bearing test)",
            "ledger_mentions": trail.get("ledger_mentions", [])[:10],
        },
        "determination": {
            "rule": "spec 007 Step 3 (M293): highest tier supported "
                    "by NON-SA evidence; Phase-101's adjudicated "
                    "outcome (MEDIUM) is that tier",
            "new_confidence": "MEDIUM",
            "reading_changed": False,
        },
    }


def dossier_name_sign(sign: str, anchors_data: dict, records: dict,
                      trails: dict, backups: dict) -> dict:
    entry = anchors_data["anchors"][sign]
    p105 = p109.load_json(REPO / "reports" / "phase105_name_signs.json")
    result = next((r for r in p105.get("results", [])
                   if r.get("sign") == sign), {})
    snap = (trails.get(sign, {}).get("structured", {})
            .get("anchor_snapshots", {}))
    search = _adjudication_search(sign)
    # A superseding adjudication must be a verdict-bearing record
    # that post-dates / supersedes Phase-105 and upgrades the sign.
    # The search surfaces candidates; Phase-106/107/108 contain no
    # name-sign adjudication (106 = SA re-run, 107 = SA validation,
    # 108 = provenance audit, whose own note restates INCONCLUSIVE).
    return {
        "phase": 109, "step": 3, "spec": "specs/007-phase109-follow-through",
        "gpu_device": _GPU, "sign": sign,
        "current": {"reading": entry.get("reading"),
                    "confidence": entry.get("confidence"),
                    "basis": entry.get("basis"),
                    "source": entry.get("source")},
        "register": {"category": records[sign].get("category"),
                     "sa_in_chain": records[sign].get("sa_in_chain"),
                     "reasons": records[sign].get("reasons", [])},
        "phase105_adjudication": {
            "verdict": result.get("verdict"),
            "rationale": result.get("rationale"),
            "corpus_profile": result.get("corpus_profile"),
            "phase103": result.get("phase103"),
            "anchors_modified_by_phase105": p105.get("anchors_modified"),
            "citation": "reports/phase105_name_signs.json",
        },
        "pre_gate_tier": snap,
        "promotion_record": (
            "Anchor basis bracket: [Phase-216: SA-cons=0.17 DEDR✓ "
            "source=Phase-105] — a recalibration/promotion gate, not "
            "an adjudication (Phase-108 register note concurs)."),
        "superseding_adjudication_search": {
            "method": "both ledgers scanned for verdict-bearing "
                      "mentions; reports/ + outputs/ + backend/"
                      "reports phase>=106 artifacts scanned for the "
                      "sign + 'verdict'",
            "hits": search,
            "conclusion": "no later superseding adjudication found; "
                          "Phase-105 INCONCLUSIVE stands as the "
                          "latest adjudication (restated 2026-10-05 "
                          "and by the Phase-108 register)",
        },
        "determination": {
            "rule": "spec 007 Step 3 (M362/M398): tier may not "
                    "exceed what the latest adjudication supports; "
                    "INCONCLUSIVE supports at most MEDIUM",
            "new_confidence": "MEDIUM",
            "reading_changed": False,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="decide",
                    choices=("decide", "apply"))
    args = ap.parse_args()
    anchors_data = p109.load_anchors_file()
    records = p109.load_register()
    trails = p109.load_trails()
    backups = p109.load_backups()
    dossiers = {
        "M293": dossier_m293(anchors_data, records, trails, backups),
        "M362": dossier_name_sign(sign="M362", anchors_data=anchors_data,
                                   records=records, trails=trails,
                                   backups=backups),
        "M398": dossier_name_sign(sign="M398", anchors_data=anchors_data,
                                   records=records, trails=trails,
                                   backups=backups),
    }
    for sign, dos in dossiers.items():
        out = REPO / "reports" / f"phase109_dossier_{sign}.json"
        out.write_text(json.dumps(dos, indent=2, ensure_ascii=False),
                       encoding="utf-8")
        print(f"[phase109-step3] dossier {sign}: "
              f"{dos['determination']['new_confidence']} -> {out.name}")
    if args.mode == "apply":
        reg = p109.load_change_register()
        ann = {
            "M293": ("individual re-review under spec 007 Step 3: "
                     "HIGH rested on the Phase-116 SA-only "
                     "recalibration gate (SA-cons=1.00 the firing "
                     "disjunct); under the no-SA-sufficient rule the "
                     "highest tier its non-SA evidence supports is "
                     "MEDIUM — the Phase-101 positional "
                     "adjudication's own recorded outcome "
                     "(2026-05-18). Reading unchanged. Dossier: "
                     "reports/phase109_dossier_M293.json."),
            "M362": ("individual re-review under spec 007 Step 3: "
                     "tier capped at MEDIUM — the latest "
                     "adjudication (Phase-105) is INCONCLUSIVE "
                     "(freq 3, below the positional-verdict floor) "
                     "and was never superseded; the HIGH came from "
                     "the Phase-216 recalibration gate, a promotion "
                     "gate, not an adjudication. Reading unchanged. "
                     "Dossier: reports/phase109_dossier_M362.json."),
            "M398": ("individual re-review under spec 007 Step 3: "
                     "tier capped at MEDIUM — the latest "
                     "adjudication (Phase-105) is INCONCLUSIVE "
                     "(freq 3, below the positional-verdict floor) "
                     "and was never superseded; the HIGH came from "
                     "the Phase-216 recalibration gate, a promotion "
                     "gate, not an adjudication. Reading unchanged. "
                     "Dossier: reports/phase109_dossier_M398.json."),
        }
        changes = []
        for sign, dos in dossiers.items():
            new_conf = dos["determination"]["new_confidence"]
            if anchors_data["anchors"][sign]["confidence"] != new_conf:
                changes.append(p109.apply_tier_change(
                    anchors_data, sign, new_conf, ann[sign],
                    rule="step3",
                    citations=[f"reports/phase109_dossier_{sign}.json"]))
        p109.append_changes(reg, "step3", changes)
        p109.save_change_register(reg)
        p109.write_anchors_file(anchors_data)
        print(f"[phase109-step3] applied {len(changes)} tier changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
