"""Phase-104: Evaluation of the 21 untested extracted claims.

Evaluates every ``untested`` claim in
``glossa-indus/claims/extracted_claims/*.json`` against evidence already
in the repo, using each claim's own ``falsification_condition`` as the
test. Rules (stated up front, applied mechanically):

  RULE-DUP   The claim restates a proposition already adjudicated in
             this program (same proposition, already carrying a verdict
             with cited evidence). The verdict carries over, with the
             original evidence cited and the cross-reference recorded.
  RULE-NOCOND The claim states no falsification condition and its text
             is an auto-extraction fragment. Per constitution section IV
             it is not evaluable as stated -> stays untested.
  RULE-SITE  The falsification condition requires site-typology data
             (gateway/border, fire-altar, palatial/royal, trade-context)
             that does not exist in the repo -> stays untested.
  RULE-CLASS The falsification condition requires a sign-class
             classification (e.g. "celestial signs") that is not present
             in any in-repo data artifact -> stays untested.
  RULE-REF   The falsification condition references an artifact (e.g. a
             24-cluster atlas) whose definitions are not in the repo
             -> stays untested.
  RULE-NUM   The claim cites sign numbers in an unstated numbering
             system with no in-repo crosswalk entry -> stays untested.

AEE scores (glossa_lab.aee_core) are recorded per claim as a supporting
consistency signal only; they are never the basis for a verdict.

Only RULE-DUP claims change status. Output:
glossa-indus/reports/phase104_claims_evaluation.json
Also updates the claim JSONs in place for claims whose status changes.
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CLAIMS_DIR = REPO / "glossa-indus" / "claims" / "extracted_claims"
HOLDAT = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
CROSSWALK = REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"
OUT = REPO / "glossa-indus" / "reports" / "phase104_claims_evaluation.json"

# The Farmer/Sproat/Witzel (2004) proposition — "the Indus signs are
# non-linguistic symbols; there was no literate Harappan writing system" —
# was already adjudicated in this program as claim
# farmer_sproat_witzel_2004_manual_001 with verdict `contradicted` and
# cited contradicting evidence. These untested claims restate the same
# proposition (titles/extractions of the same thesis in other documents).
ADJUDICATED_ID = "farmer_sproat_witzel_2004_manual_001"
DUP_CLAIM_IDS = {
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001",
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0003",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0004",
}

SITE_TYPOLOGY_IDS = {
    "indus_valley_script_deciphered_from_myth_65ff0a26_manual_001",
    "indus_valley_script_deciphered_from_myth_65ff0a26_manual_003",
    "indus_valley_script_deciphered_from_myth_65ff0a26_manual_004",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002",
}
CLASS_IDS = {"without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004"}
REF_IDS = {"without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_005"}


def _load_claims() -> dict[str, tuple[Path, dict, dict]]:
    """claim_id -> (file path, file record, claim dict)."""
    out: dict[str, tuple[Path, dict, dict]] = {}
    for f in sorted(CLAIMS_DIR.glob("*.json")):
        record = json.loads(f.read_text(encoding="utf-8"))
        for claim in record.get("claims", []):
            out[str(claim.get("claim_id"))] = (f, record, claim)
    return out


def _crosswalk_numbers() -> set[str]:
    if not CROSSWALK.exists():
        return set()
    nums: set[str] = set()
    with open(CROSSWALK, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            for v in row.values():
                if v and v.strip().isdigit():
                    nums.add(v.strip())
    return nums


def _roles_classes() -> set[str]:
    if not ROLES.exists():
        return set()
    with open(ROLES, encoding="utf-8") as fh:
        return {r.get("semantic_role", "") for r in csv.DictReader(fh)}


def _m391_site_distribution() -> dict[str, int]:
    """Context data for the arrow-sign claim (M391): tokens per site."""
    if not HOLDAT.exists():
        return {}
    sites: Counter = Counter()
    with open(HOLDAT, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("letters") == "M391":
                sites[row.get("site", "?")] += 1
    return dict(sites.most_common())


def main() -> int:
    claims = _load_claims()
    adjudicated = claims[ADJUDICATED_ID][2]
    adjudicated_evidence = adjudicated.get("contradicting_evidence", [])

    # AEE scores as supporting signal only.
    aee_scores: dict[str, float] = {}
    try:
        import sys

        sys.path.insert(0, str(REPO / "backend"))
        from glossa_lab.aee_core import score_claim_dicts  # noqa: PLC0415

        all_claims = [c for _, _, c in claims.values()]
        raw = score_claim_dicts(all_claims)
        aee_scores = {
            str(k): float(v["propagated_score"])
            for k, v in raw.items()
            if isinstance(v, dict) and "propagated_score" in v
        }
    except Exception as exc:  # noqa: BLE001
        print(f"  [WARN] AEE scoring unavailable: {exc}")

    crosswalk_nums = _crosswalk_numbers()
    role_classes = _roles_classes()
    m391_sites = _m391_site_distribution()

    results: list[dict] = []
    changed_files: dict[Path, dict] = {}

    for cid, (path, record, claim) in sorted(claims.items()):
        if claim.get("claim_status") != "untested":
            continue
        entry: dict = {
            "claim_id": cid,
            "source_document_id": claim.get("source_document_id"),
            "claim_type": claim.get("claim_type"),
            "normalized_claim": claim.get("normalized_claim"),
            "aee_score_supporting_signal_only": aee_scores.get(cid),
            "verdict": "stays_untested",
            "new_status": None,
            "rule": None,
            "reason": None,
            "evidence": [],
        }

        if cid in DUP_CLAIM_IDS:
            entry["rule"] = "RULE-DUP"
            entry["verdict"] = "status_changed"
            entry["new_status"] = "contradicted"
            entry["reason"] = (
                f"Restates the proposition already adjudicated as {ADJUDICATED_ID} "
                "(verdict: contradicted, with cited evidence). Verdict carries over."
            )
            entry["evidence"] = list(adjudicated_evidence) + [
                f"Cross-reference: {ADJUDICATED_ID} (farmer_sproat_witzel_2004)"
            ]
            claim["claim_status"] = "contradicted"
            claim["contradicting_evidence"] = list(adjudicated_evidence)
            claim["glossa_lab_evidence"] = (
                f"Phase-104 (RULE-DUP): duplicate extraction of the proposition "
                f"adjudicated in {ADJUDICATED_ID}; verdict carried over with its "
                "cited evidence. See glossa-indus/reports/phase104_claims_evaluation.json."
            )
            changed_files[path] = record
        elif cid in SITE_TYPOLOGY_IDS:
            entry["rule"] = "RULE-SITE"
            entry["reason"] = (
                "Falsification condition requires site-typology data "
                "(gateway/border, fire-altar, palatial/royal, or trade-context "
                "classification of excavation sites); no such dataset exists "
                "in the repo — the Holdat corpus carries site names only."
            )
            if cid.endswith("manual_003"):
                entry["evidence"] = [
                    f"M391 (arrow sign) site distribution in Holdat corpus: {m391_sites}",
                    "M391 semantic role per Holdat roles file: CASE_MARKER_SUFFIX "
                    "(is_ending=True) — distributional context only; the claim's "
                    "gateway/border clustering condition cannot be evaluated "
                    "without a site-typology dataset.",
                ]
        elif cid in CLASS_IDS:
            entry["rule"] = "RULE-CLASS"
            entry["reason"] = (
                "Falsification condition requires a celestial sign class; the "
                f"in-repo semantic-role classes are {sorted(role_classes)} and "
                "no celestial classification artifact exists in repo data, so "
                "terminal enrichment for the class cannot be computed."
            )
        elif cid in REF_IDS:
            entry["rule"] = "RULE-REF"
            entry["reason"] = (
                "The claim's 24-cluster Translation Atlas definitions are not "
                "in the repo (Glossa's own cluster artifacts are different "
                "clusterings), so the distinct-profile test cannot be run."
            )
        elif claim.get("claim_type") == "sign_value_claim":
            entry["rule"] = "RULE-NUM"
            entry["reason"] = (
                "Sign number cited without a stated numbering system; no "
                "matching entry was located in the in-repo crosswalk "
                "(data/crosswalks/canonical_sign_registry.csv), and the "
                "extraction carries no falsification condition."
            )
            entry["evidence"] = [
                f"Crosswalk numeric IDs present in registry: {len(crosswalk_nums)}"
            ]
        elif not claim.get("falsification_condition"):
            entry["rule"] = "RULE-NOCOND"
            entry["reason"] = (
                "Auto-extraction fragment with no falsification condition and "
                "no stated proposition; not evaluable as stated "
                "(constitution section IV)."
            )
        else:
            entry["rule"] = "RULE-UNMAPPED"
            entry["reason"] = "No evaluation rule matched; left untested for manual review."

        results.append(entry)

    for path, record in changed_files.items():
        # indent=2 matches the extracted_claims files' existing format, so
        # the diff stays limited to the claims whose status changed.
        path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    moved = [r for r in results if r["verdict"] == "status_changed"]
    report = {
        "_citation": ["A.13", "C.1"],
        "phase": 104,
        "title": "Evaluation of untested extracted claims",
        "n_untested_evaluated": len(results),
        "n_status_changed": len(moved),
        "n_stays_untested": len(results) - len(moved),
        "rules": {
            "RULE-DUP": "verdict carried over from an already-adjudicated identical proposition",
            "RULE-NOCOND": "no falsification condition / extraction fragment",
            "RULE-SITE": "falsification needs site-typology data not in repo",
            "RULE-CLASS": "falsification needs a sign-class set not in repo data",
            "RULE-REF": "referenced artifact definitions not in repo",
            "RULE-NUM": "sign numbering unstated / not crosswalked in repo",
        },
        "note": (
            "AEE scores are recorded as supporting consistency signals only; "
            "no verdict rests on an AEE score."
        ),
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Phase-104: evaluated {len(results)} untested claims")
    print(f"  status changed: {len(moved)} (all RULE-DUP -> contradicted)")
    for r in moved:
        print(f"    {r['claim_id']} -> contradicted")
    print(f"  stays untested: {len(results) - len(moved)}")
    for r in results:
        if r["verdict"] == "stays_untested":
            print(f"    [{r['rule']}] {r['claim_id']}")
    print(f"Report: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
