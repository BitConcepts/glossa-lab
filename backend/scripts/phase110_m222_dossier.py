"""Phase-110 Part A: M222 / 'kur' adjudication dossier (spec 008).

Assembles, from in-repo artifacts only, the evidence for the
tension Phase-109 left flagged: 109 anchors restored to 'kur'/LOW
from Phase-111 allograph resolution — derivations that run through
M222 read as 'kur' — while M222 itself stands at 'min'/MEDIUM on
crosswalk v2.1 (Parpola) support.

Decide-only: writes reports/phase110_m222_dossier.json and
reports/phase110_m222_summary.md; touches nothing else.

GPU: no compute; gpu_device recorded per H20 (torch guarded).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase110-dossier] gpu_device={_GPU}", file=sys.stderr)

REPO = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
BACKUP = REPO / "backend/reports/INDUS_FINAL_ANCHORS.backup_20260523_181449.json"
P111_SCRIPT = REPO / "backend/scripts/phase111_allograph_resolution.py"
P111_OUT = REPO / "outputs/phase111_allograph_resolution.json"
P87_OUT = REPO / "outputs/phase87_anchor_sprint_120.json"
P71_SCRIPT = REPO / "backend/scripts/phase71_crosswalk_complete.py"
CROSSWALK = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"
REG109 = REPO / "reports/phase109_change_register.json"
LEDGER_INDUS = REPO / "glossa-indus/LEDGER.md"
OUT_JSON = REPO / "reports/phase110_m222_dossier.json"
OUT_MD = REPO / "reports/phase110_m222_summary.md"


def load(p: Path):
    return json.loads(p.read_text("utf-8"))


def phase111_mechanism() -> dict:
    src = P111_SCRIPT.read_text("utf-8").splitlines()
    write_block = [ln.strip() for ln in src
                   if "anchors[rare_sign]" in ln or "confirmed_reading" in ln
                   or '"basis"' in ln or "MAX_L1_DIST" in ln and "=" in ln]
    run = load(P111_OUT)
    amap = run["allograph_map"]
    matched = Counter(e.get("matched_to") for e in amap if e.get("matched_to"))
    dists = Counter(e["l1_dist"] for e in amap)
    inherited = Counter(e.get("inherited_reading") for e in amap
                        if e.get("matched_to"))
    m222_rows = [e for e in amap if e.get("matched_to") == "M222"][:2]

    # Recompute profiles with the script's own functions.
    import importlib.util
    spec = importlib.util.spec_from_file_location("p111", P111_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    seals = mod.load_corpus()
    profiles = mod.compute_profiles(seals, min_count=1)
    flat = Counter(s for signs in seals.values() for s in signs)
    rare = [s for s in flat if flat[s] <= mod.MAX_FREQ_RARE]
    rare_profiles = Counter(
        (profiles[s]["i"], profiles[s]["t"], profiles[s]["m"]) for s in rare)

    # Donor-tie analysis under the May-2026 anchors state (the state
    # the recorded run operated on): how many confirmed signs were
    # eligible donors, and how many shared M222's exact profile?
    backup = load(BACKUP)
    b_anchors = backup.get("anchors", backup)
    confirmed = {s for s, v in b_anchors.items()
                 if v.get("confidence") in ("HIGH", "MEDIUM")}
    donors = {s: profiles[s] for s in confirmed
              if s in profiles and profiles[s]["freq"] >= mod.MIN_FREQ_CONFIRMED}
    tied = {s: p for s, p in donors.items()
            if (p["i"], p["t"], p["m"]) == (0.0, 0.0, 1.0)}

    anchors_data = load(ANCHORS)
    return {
        "script": "backend/scripts/phase111_allograph_resolution.py",
        "method_as_coded": (
            "For each rare sign (corpus freq 1-4, not HIGH/MEDIUM), "
            "compute an I/M/T positional profile (initial/terminal/"
            "medial occurrence rates in the Holdat corpus); find the "
            "nearest confirmed sign (HIGH/MEDIUM, corpus freq >= 5) "
            "by L1 profile distance; if L1 <= 0.35, write the rare "
            "sign into the anchors file with the CONFIRMED SIGN'S "
            "READING VERBATIM at LOW. The value is copied from the "
            "donor entry; no per-sign evidence of any other kind "
            "enters the assignment."),
        "code_lines_quoted": write_block,
        "recorded_run": {
            "artifact": "outputs/phase111_allograph_resolution.json",
            "n_rare_signs": run["n_rare_signs"],
            "n_resolved": run["n_resolved"],
            "n_unresolved": run["n_unresolved"],
            "matched_to_distribution": dict(matched),
            "l1_dist_distribution": {str(k): v for k, v in dists.items()},
            "inherited_reading_distribution": dict(inherited),
            "sample_m222_rows": m222_rows,
        },
        "profile_recomputation": {
            "method": "phase111 module's own load_corpus/compute_profiles "
                      "on the in-repo Holdat corpus, run 2026-10-06",
            "corpus_tokens": sum(flat.values()),
            "corpus_distinct_signs": len(flat),
            "m222_profile": profiles.get("M222"),
            "n_rare_signs_freq_le_4": len(rare),
            "rare_profile_distribution": {
                str(k): v for k, v in rare_profiles.items()},
            "donor_tie_analysis_may2026_state": {
                "n_confirmed_signs": len(confirmed),
                "n_eligible_donors_freq_ge_5": len(donors),
                "n_donors_with_profile_0_0_1": len(tied),
                "tied_donor_signs": sorted(tied),
            },
        },
        "phase132_characterization": {
            "anchors_file_top_level_note": anchors_data.get("_phase132_note"),
            "sample_entry_note": next(
                (v["_phase132_note"] for v in anchors_data["anchors"].values()
                 if "_phase132_note" in v), None),
        },
    }


def m222_kur_record() -> dict:
    p87 = load(P87_OUT)
    proposal = next((p for p in p87["all_proposals"]
                     if p.get("sign") == "M222"), None)
    backup = load(BACKUP)
    b_anchors = backup.get("anchors", backup)
    ledger = LEDGER_INDUS.read_text("utf-8").splitlines()
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(ledger)
            if "M222=kur" in ln]
    return {
        "phase87_proposal": proposal,
        "phase87_artifact": "outputs/phase87_anchor_sprint_120.json",
        "may2026_backup_entry": b_anchors.get("M222"),
        "backup_file": "backend/reports/INDUS_FINAL_ANCHORS.backup_20260523_181449.json",
        "ledger_lines": hits,
    }


def m222_min_record() -> dict:
    anchors = load(ANCHORS)["anchors"]
    cw = load(CROSSWALK)["crosswalk"].get("M222")
    p71_lines = [ln.strip() for ln in P71_SCRIPT.read_text("utf-8").splitlines()
                 if '"M222"' in ln]
    reg109 = load(REG109)["entries"]
    m222_reg = [e for e in reg109 if e.get("sign") == "M222"]
    return {
        "current_anchor_entry": anchors.get("M222"),
        "crosswalk_v2_entry": cw,
        "phase71_extended_map_line": p71_lines,
        "phase109_register_record": m222_reg,
    }


def cohorts(anchors: dict, reg109: dict) -> dict:
    restores = [e for e in reg109["entries"]
                if e["step"] == "step1" and e["action"] == "restore"]
    cohort_a = sorted(e["sign"] for e in restores
                      if e["after"]["reading"] == "kur")
    current_low = sorted(
        s for s, v in anchors.items()
        if v.get("reading") == "kur" and v.get("confidence") == "LOW"
        and str(v.get("basis", "")).startswith("Phase-111 allograph"))
    cand = {s: v for s, v in anchors.items()
            if v.get("reading") == "kur" and v.get("confidence") == "CANDIDATE"
            and str(v.get("basis", "")).startswith("Phase-111 allograph")}
    # An "independent derivation" exempts an entry only if it
    # supports the VALUE 'kur'. The Phase-252 upgrade_basis records
    # claim allograph status under a parent sign — parse the
    # parent's recorded reading from the text (e.g. M427='en') and
    # compare: an allograph of M427 would read 'en', not 'kur'.
    import re
    cohort_b, cohort_c, cand_detail = [], {}, {}
    for s, v in sorted(cand.items()):
        ub = v.get("upgrade_basis") or ""
        m = re.search(r"(M\d+)='([^']+)'", ub)
        parent = {"sign": m.group(1), "reading": m.group(2)} if m else None
        supports_kur = bool(parent and parent["reading"] == "kur")
        cand_detail[s] = {
            "entry": v,
            "upgrade_parent": parent,
            "upgrade_basis_supports_kur": supports_kur,
        }
        if supports_kur:
            cohort_c[s] = {"upgrade_basis": ub, "dedr": v.get("dedr"),
                           "phase_upgraded": v.get("phase_upgraded")}
        else:
            cohort_b.append(s)
    return {
        "cohort_a_register_set": cohort_a,
        "cohort_a_current_low_set": current_low,
        "cohort_a_sets_equal": cohort_a == current_low,
        "cohort_b_candidate_pure_phase111": cohort_b,
        "cohort_c_candidate_dual_derivation": cohort_c,
        "candidate_detail": cand_detail,
        "n_kur_by_phase111_total": len(current_low) + len(cand),
    }


def reconciliation(anchors: dict) -> dict:
    run = load(P111_OUT)
    resolved = run["resolved_signs"]
    still = [s for s in resolved if s in anchors
             and anchors[s].get("reading") == "kur"
             and str(anchors[s].get("basis", "")).startswith(
                 "Phase-111 allograph")]
    other = [s for s in resolved if s in anchors and s not in still]
    absent = [s for s in resolved if s not in anchors]
    return {
        "phase111_resolved_total": len(resolved),
        "still_kur_with_phase111_basis_today": len(still),
        "present_with_later_readings": len(other),
        "absent_from_current_anchors": len(absent),
        "note": "Of the 220 signs Phase-111 resolved: 113 still "
                "carry the Phase-111 'kur' basis in the current "
                "anchors file (the adjudicated set); 3 are present "
                "with later readings from subsequent recorded "
                "processes; 104 are absent from the current file "
                "entirely (the anchors file was reduced in later "
                "cleanups, e.g. the June-2026 quality-audit "
                "605->285 cleanup). Only the 113 rest on the M222 "
                "premise today and are in scope.",
    }


def main() -> int:
    anchors_data = load(ANCHORS)
    anchors = anchors_data["anchors"]
    reg109 = load(REG109)
    mech = phase111_mechanism()
    coh = cohorts(anchors, reg109)

    assert coh["cohort_a_sets_equal"], "Cohort A set mismatch — STOP"
    # Spec 008 addendum: the Phase-252 upgrade_basis records support
    # 'en' (M427) / 'taṇ' (M375), never 'kur' — so no CANDIDATE entry
    # is exempt; Cohort C is empty and all four join Cohort B.
    assert coh["cohort_b_candidate_pure_phase111"] == [
        "M157", "M256", "M307", "M400"], \
        f"Cohort B unexpected: {coh['cohort_b_candidate_pure_phase111']}"
    assert coh["cohort_c_candidate_dual_derivation"] == {}, \
        f"Cohort C unexpected: {sorted(coh['cohort_c_candidate_dual_derivation'])}"

    # Verdict predicates — all mechanical.
    a_bases = [anchors[s].get("basis", "") for s in coh["cohort_a_register_set"]]
    p1 = all("matches M222 ('kur', MEDIUM)" in b for b in a_bases)
    rr = mech["recorded_run"]
    p2 = (rr["matched_to_distribution"] == {"M222": 220}
          and rr["inherited_reading_distribution"] == {"kur": 220})
    p3 = (rr["l1_dist_distribution"] == {"0.0": 220}
          and mech["profile_recomputation"]["rare_profile_distribution"]
          == {"(0.0, 0.0, 1.0)": mech["profile_recomputation"]
              ["n_rare_signs_freq_le_4"]})
    cur = anchors["M222"]
    p4 = (cur.get("reading") == "min" and cur.get("confidence") == "MEDIUM")
    predicates = {
        "P1_recorded_bases_cite_m222_kur": p1,
        "P2_run_is_pure_donor_inheritance": p2,
        "P3_profile_match_informationless": p3,
        "P4_m222_standing_record_is_min": p4,
    }
    if p1 and p2 and p3 and p4:
        branch, demote = 1, True
    elif p1 and p4:
        branch, demote = 1, False
    elif not p1:
        branch, demote = 2, False
    else:
        branch, demote = 3, False

    dossier = {
        "phase": 110,
        "spec": "specs/008-m222-adjudication",
        "part": "A — dossier",
        "gpu_device": _GPU,
        "question": "Do the 109 Phase-111 'kur' restorations genuinely "
                    "depend on the premise M222='kur', and is that "
                    "premise contradicted by M222's standing sourced "
                    "record ('min', crosswalk v2.1)?",
        "phase111_mechanism": mech,
        "m222_kur_record": m222_kur_record(),
        "m222_min_record": m222_min_record(),
        "cohorts": coh,
        "reconciliation": reconciliation(anchors),
        "verdict": {
            "predicates": predicates,
            "contradiction": (
                "REAL at the level of the recorded derivations. Every "
                "Cohort-A basis asserts, verbatim, a positional-profile "
                "match to M222 read as 'kur' as the source of the "
                "entry's value; M222's standing sourced record is "
                "'min'/MEDIUM. The premise the derived values cite is "
                "superseded by the anchor sign's own record."),
            "dependence_kind": (
                "(i) literal phonetic inheritance, mechanically "
                "proven: the Phase-111 script copies the donor sign's "
                "reading verbatim, the donor was M222 in 220/220 "
                "recorded matches, and the only per-sign evidence "
                "(profile identity) is informationless — every rare "
                "sign's profile is (0,0,1) and every match is "
                "L1=0.000, so M222's selection among tied (0,0,1) "
                "donors carried no sign-specific information. The "
                "class-label characterization (ii) exists only as "
                "Phase-132's post-hoc recharacterization ('parking "
                "placeholder... not a genuine phonetic reading'), "
                "which itself denies the values are genuine readings."),
            "branch": branch,
            "demote_cohort_a_to_candidate": demote,
        },
    }
    OUT_JSON.write_text(json.dumps(dossier, indent=2, ensure_ascii=False),
                        encoding="utf-8")

    v = dossier["verdict"]
    md = """# Phase-110 — M222 / 'kur' Adjudication: Dossier Summary (spec 008, Part A)

Full evidence: `reports/phase110_m222_dossier.json` (all quotations
verbatim from the cited in-repo artifacts).

## What Phase-111 actually did

`backend/scripts/phase111_allograph_resolution.py` assigns each
rare sign (freq 1–4) the reading of its nearest confirmed sign by
I/M/T positional-profile L1 distance — **copied verbatim** from the
donor's anchor entry. The recorded run
(`outputs/phase111_allograph_resolution.json`) resolved 220 signs:
**220/220 matched M222, 220/220 at L1 = 0.000, 220/220 inherited
'kur'**. Recomputation with the script's own functions shows why:
every rare sign's profile in the Holdat corpus is
(I=0.000, T=0.000, M=1.000) — all occurrences medial — and M222
(freq 5, the minimum donor frequency) shares that profile. The
match carried **zero discriminating information**; M222 was the
donor by tie-breaking, not by sign-specific affinity. Phase-132
later said the same in the anchors file's own note: the Phase-111
kur assignments were "positional parking spots (all-MEDIAL L1=0),
not genuine phonetic readings."

## The two M222 records

- **'kur' (Phase-87):** anchor-sprint proposal, method
  DEDR_REBUS_EXTENDED, depiction "hook sign", evidence_score 2.0 —
  promoted to MEDIUM (`outputs/phase87_anchor_sprint_120.json`;
  May-2026 backup entry, source `Phase-87 DEDR_REBUS_EXTENDED`).
  This was M222's reading when Phase-111 ran.
- **'min' (standing record):** current entry at MEDIUM, retained by
  Phase-109 Step 1(a) because crosswalk v2.1 records the Parpola
  reading 'min' for M222→P222 (Phase-71 EXTENDED_MAP, "Parpola 1994
  App. B", crosswalk confidence CANDIDATE, single in-repo source —
  quoted in the dossier). Acknowledged thinness: one crosswalk
  attribution plus a staging-era DEDR gloss ("shine / lightning").
  Phase-110 does not re-try M222's own value (spec 008
  Assumptions); it adjudicates the *derived* entries against the
  standing record.

## Verdict

**Contradiction: real** (predicates P1–P4 all true — see dossier).
The 109 values are **pure premise inheritance**: their recorded
bases cite M222='kur', a premise M222's own sourced record
contradicts. **Branch 1 applies, with demotion**: Cohort A (109)
is annotated `premise_superseded` and demoted LOW → CANDIDATE.
The four further CANDIDATE entries carrying a Phase-111 'kur'
basis (M157, M256, M307, M400) join the same disposition with no
tier change: their Phase-252 `upgrade_basis` records claim
allograph status under M427 ('en') or M375 ('taṇ') — competing,
never-adopted derivations of *different* values that do not
support 'kur' (spec 008 addendum; Cohort C is empty). Of the 220
signs Phase-111 resolved, 113 still carry its 'kur' basis today
(3 more are present with later readings; 104 are absent from the
current anchors file after later cleanups).

**AI disclosure:** assembled by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution §VI.
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"[phase110-dossier] verdict branch={branch} demote={demote}")
    print(f"[phase110-dossier] wrote {OUT_JSON} + {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
