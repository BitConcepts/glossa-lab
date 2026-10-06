"""Phase-109 follow-through machinery (spec 007).

Executes the Phase-108 provenance audit's recommendations under
pre-registered mechanical rules (specs/007-phase109-follow-through):

- Step 1: staging-cohort re-review — (a) KEEP on recorded
  independent non-SA support, (b) RESTORE the prior sourced reading
  the June-2026 research-loop staging promotion overwrote,
  (c) DEMOTE one tier otherwise.
- Step 2: provenance flags on the 44 SA-lineage HIGH anchors.
- Step 3: tier caps for M293 / M362 / M398 from their dossiers.
- Step 5: headline re-base recomputation + anchors bookkeeping
  regeneration (spec 004 WS3 method).

Decision functions are pure over assembled evidence dicts so they
can be unit-tested on synthetic records. Apply functions mutate an
in-memory anchors-file dict and return change records for the
cumulative change register (reports/phase109_change_register.json).
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from glossa_lab.pipelines import provenance_audit as pa

REPO = Path(__file__).resolve().parents[3]
BACKEND = REPO / "backend"
REPORTS = REPO / "reports"
BKRPT = BACKEND / "reports"

ANCHORS_PATH = BKRPT / "INDUS_FINAL_ANCHORS.json"
BACKUP_NAMES = [
    "INDUS_FINAL_ANCHORS.backup_20260520_100230.json",
    "INDUS_FINAL_ANCHORS.backup_20260522_210001.json",
    "INDUS_FINAL_ANCHORS.backup_20260523_181449.json",
]
REGISTER_PATH = REPORTS / "phase108_provenance_register.json"
TRAILS_PATH = REPORTS / "phase108_anchor_trails.json"
STAGING_ARCHIVE_PATH = REPO / "outputs" / "anchor_staging_archive.json"
CHANGE_REGISTER_PATH = REPORTS / "phase109_change_register.json"

DATE = "2026-10-06"
TIERS = ["CANDIDATE", "LOW", "MEDIUM", "HIGH"]
DEMOTE = {"HIGH": "MEDIUM", "MEDIUM": "LOW", "LOW": "CANDIDATE",
          "CANDIDATE": "CANDIDATE"}
SA_LINEAGE_CATEGORIES = ("SA_DERIVED", "SA_CONFIRMED_ONLY")


# ── Loaders ──────────────────────────────────────────────────────────

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_anchors_file(path: Path | None = None) -> dict:
    return load_json(path or ANCHORS_PATH)


def load_backups() -> dict[str, dict]:
    """Backup snapshot files in chronological order (name -> data)."""
    out: dict[str, dict] = {}
    for name in BACKUP_NAMES:
        p = BKRPT / name
        if p.exists():
            out[name] = load_json(p)
    return out


def load_register() -> dict[str, dict]:
    return load_json(REGISTER_PATH)["records"]


def load_trails() -> dict[str, dict]:
    return load_json(TRAILS_PATH)["trails"]


def load_staging_archive() -> list[dict]:
    if STAGING_ARCHIVE_PATH.exists():
        return load_json(STAGING_ARCHIVE_PATH)
    return []


# ── Cohort definitions (registered in spec 007) ─────────────────────

def staging_cohort(records: dict[str, dict]) -> list[str]:
    """The 116: register records carrying a research_loop_heuristic
    component (Phase-108 Step-2 hand review)."""
    return sorted(
        s for s, r in records.items()
        if any(c.get("role") == "research_loop_heuristic"
               for c in r.get("components", [])))


def sa_lineage_anchors(records: dict[str, dict]) -> dict[str, str]:
    """The 44 SA load-bearing anchors: sign -> register category."""
    return {s: r["category"] for s, r in sorted(records.items())
            if r.get("category") in SA_LINEAGE_CATEGORIES}


def strict_sa_independent_hm(anchors: dict[str, dict],
                             records: dict[str, dict]) -> set[str]:
    """Phase-108 strict definition applied to a (post-change) anchors
    mapping: H+M signs whose register category is not SA_DERIVED /
    SA_CONFIRMED_ONLY and whose register record has sa_in_chain false."""
    out: set[str] = set()
    for sign, entry in anchors.items():
        if (entry.get("confidence") or "").upper() not in ("HIGH", "MEDIUM"):
            continue
        rec = records.get(sign)
        if rec is None:
            continue
        if rec.get("category") in SA_LINEAGE_CATEGORIES:
            continue
        if rec.get("sa_in_chain"):
            continue
        out.add(sign)
    return out


# ── Step 1: evidence assembly + decision ─────────────────────────────

_LEDGER_ASSIGN_RE = r"{sign}\s*=\s*([^\s,;(]+)"


def _ledger_assignments(sign: str, trail: dict) -> list[dict]:
    """`Mxxx = value` assignments found in the trail's ledger mentions."""
    pat = re.compile(_LEDGER_ASSIGN_RE.format(sign=re.escape(sign)))
    out = []
    for m in trail.get("ledger_mentions", []):
        for hit in pat.finditer(m.get("snippet", "")):
            out.append({"header": m.get("header", ""),
                        "line": m.get("line"),
                        "assigned_raw": hit.group(1),
                        "assigned_norm": pa.normalize_reading(hit.group(1)),
                        "snippet": m.get("snippet", "")[:200]})
    return out


def assemble_staging_evidence(sign: str, anchors_data: dict,
                              records: dict[str, dict],
                              trails: dict[str, dict],
                              backups: dict[str, dict],
                              archive: list[dict]) -> dict:
    entry = anchors_data["anchors"][sign]
    rec = records[sign]
    trail = trails.get(sign, {})
    structured = trail.get("structured", {})
    snapshots = structured.get("anchor_snapshots", {}) or {}

    snap_list = []
    for name in BACKUP_NAMES:
        if name in snapshots:
            snap_list.append({"file": name,
                              "reading": snapshots[name].get("reading"),
                              "confidence": snapshots[name].get("confidence")})
    latest_snap_entry = None
    latest_snap_file = None
    if snap_list:
        latest_snap_file = snap_list[-1]["file"]
        b_entry = backups.get(latest_snap_file, {}).get("anchors", {}).get(sign)
        if b_entry is not None:
            latest_snap_entry = copy.deepcopy(b_entry)

    cw = structured.get("crosswalk_v2") or {}
    cur_norm = pa.normalize_reading(entry.get("reading", ""))
    assignments = _ledger_assignments(sign, trail)

    ev = {
        "sign": sign,
        "current": {"reading": entry.get("reading"),
                    "confidence": entry.get("confidence"),
                    "basis": entry.get("basis"),
                    "source": entry.get("source")},
        "register_category": rec.get("category"),
        "register_reasons": rec.get("reasons", []),
        "snapshots": snap_list,
        "latest_snapshot_entry": latest_snap_entry,
        "crosswalk": ({"parpola_id": cw.get("parpola_id"),
                       "reading": cw.get("reading"),
                       "source": cw.get("source")}
                      if cw.get("reading") else None),
        "ledger_assignments": assignments,
        "archive_entries": [c for c in archive
                            if (c.get("sign") or c.get("sign_id")) == sign],
    }
    # (A1) crosswalk literature support for the CURRENT value
    ev["a1_crosswalk_match"] = bool(
        ev["crosswalk"]
        and pa.normalize_reading(ev["crosswalk"]["reading"]) == cur_norm
        and cur_norm)
    # (A2) latest snapshot records the SAME reading
    ev["a2_snapshot_same"] = bool(
        snap_list
        and pa.normalize_reading(snap_list[-1]["reading"] or "") == cur_norm
        and cur_norm)
    # (A3) a ledger assignment of the CURRENT value via a non-loop method
    ev["a3_ledger_matches"] = [a for a in assignments
                               if a["assigned_norm"] == cur_norm and cur_norm]
    # Prior-reading facts for rule (b)
    ev["snapshots_agree"] = (
        len({s["reading"] for s in snap_list}) == 1 if snap_list else False)
    ev["prior_differs"] = bool(
        snap_list
        and pa.normalize_reading(snap_list[-1]["reading"] or "") != cur_norm)
    return ev


def decide_staging(ev: dict) -> dict:
    """Spec 007 Step 1 rules, applied in order (a) -> (b) -> (c).

    Pure function over the assembled evidence dict."""
    sign = ev["sign"]
    support: list[str] = []
    if ev["a1_crosswalk_match"]:
        support.append(
            "A1 crosswalk v2.1 Parpola reading "
            f"'{ev['crosswalk']['reading']}' ({ev['crosswalk']['source']}) "
            "equals the current reading under Phase-108 normalisation")
    if ev["a2_snapshot_same"]:
        support.append(
            "A2 latest pre-promotion backup snapshot "
            f"({ev['snapshots'][-1]['file']}) records the same reading — "
            "the value predates the research loop")
    for a in ev["a3_ledger_matches"]:
        support.append(
            f"A3 ledger assignment {sign}={a['assigned_raw']} "
            f"({a['header']}, glossa-indus/LEDGER.md:{a['line']})")
    if support:
        return {"sign": sign, "rule": "a", "action": "keep",
                "support": support,
                "needs_handcheck": bool(ev["a3_ledger_matches"]),
                "prior": None}
    if ev["snapshots"] and ev["prior_differs"] and ev["snapshots_agree"] \
            and ev["latest_snapshot_entry"] is not None:
        prior = ev["latest_snapshot_entry"]
        return {"sign": sign, "rule": "b", "action": "restore",
                "support": [
                    "prior sourced reading in "
                    f"{ev['snapshots'][-1]['file']} (all "
                    f"{len(ev['snapshots'])} backup snapshots agree), "
                    "overwritten by the June-2026 staging promotion"],
                "needs_handcheck": prior.get("confidence") in ("HIGH", "MEDIUM"),
                "prior": {"file": ev["snapshots"][-1]["file"],
                          "reading": prior.get("reading"),
                          "confidence": prior.get("confidence"),
                          "entry": prior}}
    return {"sign": sign, "rule": "c", "action": "demote",
            "support": ["no independent non-SA support recorded for the "
                        "staging value; no restorable prior sourced "
                        "reading in the backup snapshots"],
            "needs_handcheck": True,
            "prior": None}


def _annotation(text: str) -> str:
    return f"Phase-109 ({DATE}): {text}"


def staging_annotation(decision: dict, ev: dict) -> str:
    rule = decision["rule"]
    if rule == "a":
        return _annotation(
            "staging-cohort re-review — value RETAINED under spec 007 "
            "Step 1(a): independent non-SA support recorded ("
            + "; ".join(decision["support"])
            + "). Phase-108 register: reports/phase108_provenance_"
            "register.json.")
    if rule == "b":
        p = decision["prior"]
        return _annotation(
            "staging-cohort re-review — pre-staging reading RESTORED "
            "under spec 007 Step 1(b): the June-2026 research-loop "
            "staging promotion (fixed heuristic tables; /staging/"
            "verify-sa performs no SA test) overwrote the sourced "
            f"reading '{p['reading']}' ({p['confidence']}); prior "
            f"source: backend/reports/{p['file']}. Staging value was "
            f"'{ev['current']['reading']}' ({ev['current']['confidence']}).")
    return _annotation(
        "staging-cohort re-review — DEMOTED one tier under spec 007 "
        "Step 1(c): staging-heuristic origin, unvalidated "
        "(Phase-109). No independent non-SA support recorded and no "
        "restorable prior sourced reading.")


# ── Change application + register ────────────────────────────────────

def load_change_register() -> dict:
    if CHANGE_REGISTER_PATH.exists():
        return load_json(CHANGE_REGISTER_PATH)
    return {"phase": 109, "spec": "specs/007-phase109-follow-through",
            "date": DATE, "entries": []}


def save_change_register(reg: dict) -> None:
    CHANGE_REGISTER_PATH.write_text(
        json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def append_changes(reg: dict, step: str, changes: list[dict]) -> None:
    for ch in changes:
        reg["entries"].append({"step": step, **ch})


def apply_staging_decisions(anchors_data: dict,
                            decisions: list[dict],
                            evidence: dict[str, dict]) -> list[dict]:
    anchors = anchors_data["anchors"]
    changes: list[dict] = []
    for d in decisions:
        sign = d["sign"]
        ev = evidence[sign]
        before = copy.deepcopy(anchors[sign])
        ann = staging_annotation(d, ev)
        if d["rule"] == "a":
            anchors[sign]["phase109_annotation"] = ann
            action = "keep+annotate"
        elif d["rule"] == "b":
            prior_entry = copy.deepcopy(d["prior"]["entry"])
            prior_entry["phase109_annotation"] = ann
            anchors[sign] = prior_entry
            action = "restore"
        else:
            anchors[sign]["confidence"] = DEMOTE[before["confidence"]]
            anchors[sign]["phase109_annotation"] = ann
            action = "demote"
        changes.append({
            "sign": sign, "rule": f"step1({d['rule']})", "action": action,
            "before": {"reading": before.get("reading"),
                       "confidence": before.get("confidence"),
                       "basis": before.get("basis"),
                       "source": before.get("source")},
            "after": {"reading": anchors[sign].get("reading"),
                      "confidence": anchors[sign].get("confidence"),
                      "basis": anchors[sign].get("basis"),
                      "source": anchors[sign].get("source")},
            "citations": d["support"]})
    return changes


def apply_sa_flags(anchors_data: dict,
                   lineage: dict[str, str]) -> list[dict]:
    """Step 2: provenance flags only — reading/confidence untouched."""
    anchors = anchors_data["anchors"]
    changes: list[dict] = []
    for sign, category in lineage.items():
        before = copy.deepcopy(anchors[sign])
        anchors[sign]["validation_status"] = "pending_non_sa_validation"
        anchors[sign]["provenance_class"] = category
        anchors[sign]["phase109_annotation"] = _annotation(
            "SA-lineage HIGH anchor flagged under spec 007 Step 2: "
            f"provenance_class={category} (Phase-108 register); value "
            "and tier unchanged in this step; presented as a candidate "
            "pending non-SA validation (Phase-107 falsified SA as "
            "evidence for sign values).")
        assert anchors[sign]["reading"] == before["reading"]
        assert anchors[sign]["confidence"] == before["confidence"]
        changes.append({
            "sign": sign, "rule": "step2", "action": "flag",
            "before": {"reading": before.get("reading"),
                       "confidence": before.get("confidence")},
            "after": {"reading": anchors[sign].get("reading"),
                      "confidence": anchors[sign].get("confidence"),
                      "validation_status": "pending_non_sa_validation",
                      "provenance_class": category},
            "citations": ["reports/phase108_provenance_register.json "
                          f"({category})"]})
    return changes


def apply_tier_change(anchors_data: dict, sign: str, new_confidence: str,
                      annotation: str, rule: str,
                      citations: list[str]) -> dict:
    anchors = anchors_data["anchors"]
    before = copy.deepcopy(anchors[sign])
    anchors[sign]["confidence"] = new_confidence
    anchors[sign]["phase109_annotation"] = _annotation(annotation)
    return {"sign": sign, "rule": rule, "action": "tier_change",
            "before": {"reading": before.get("reading"),
                       "confidence": before.get("confidence")},
            "after": {"reading": anchors[sign].get("reading"),
                      "confidence": new_confidence},
            "citations": citations}


# ── Step 5: bookkeeping regeneration (spec 004 WS3 method) ──────────

def regenerate_bookkeeping(anchors_data: dict,
                           corpus_coverage: float) -> dict:
    """Regenerate every summary field from the entries themselves.
    Returns {field: [old, new]} for fields that changed."""
    anchors = anchors_data["anchors"]
    counts = {t: 0 for t in TIERS}
    for e in anchors.values():
        counts[(e.get("confidence") or "").upper()] += 1
    total = len(anchors)
    hm = counts["HIGH"] + counts["MEDIUM"]
    changed: dict[str, list] = {}

    def _set(container: dict, key: str, value) -> None:
        if container.get(key) != value:
            changed[key] = [container.get(key), value]
            container[key] = value

    _set(anchors_data, "total", total)
    _set(anchors_data, "total_all_entries", total)
    _set(anchors_data, "by_confidence", dict(counts))
    _set(anchors_data, "n_high", counts["HIGH"])
    _set(anchors_data, "n_medium", counts["MEDIUM"])
    _set(anchors_data, "n_low", counts["LOW"])
    _set(anchors_data, "n_candidate", counts["CANDIDATE"])
    _set(anchors_data, "corpus_token_coverage", corpus_coverage)
    md = anchors_data.setdefault("metadata", {})
    _set(md, "total_count", total)
    _set(md, "high_count", counts["HIGH"])
    _set(md, "medium_count", counts["MEDIUM"])
    _set(md, "low_count", counts["LOW"])
    _set(md, "candidate_count", counts["CANDIDATE"])
    _set(md, "hm_confirmed_count", hm)
    return {"counts": counts, "total": total, "hm": hm,
            "changed_fields": changed}


def write_anchors_file(anchors_data: dict, path: Path | None = None) -> None:
    (path or ANCHORS_PATH).write_text(
        json.dumps(anchors_data, indent=2, ensure_ascii=False),
        encoding="utf-8")
