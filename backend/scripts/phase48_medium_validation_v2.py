"""Phase-48: MEDIUM Anchor Validation Suite — battery v2 (Spec 091 T301).

The corrected Phase-48 battery. Decision D-091-4: this is a NEW
versioned battery alongside the historical
``phase48_medium_validation.py``, which stays frozen and untouched.
The historical script's output is the evidence the WP5 audit
reconstructed; the instrument that produced it must stay inspectable
as it was.

What v2 removes — every path enumerated in Spec 091 Stage 1's T104
enumeration (``specs/091-anchor-comparison-integrity/records/
t104-pass-by-default-enumeration.json``) under which the historical
battery awarded a promotion credit without an executed check over
present inputs:

  P2  test_positional: a role with no expectation entry returned
      PASS ("no_expectation—pass_by_default"). v2: NOT_RUN.
  P3  test_dedr: a normalized reading shorter than 2 characters
      returned PASS ("too_short_pass") without the dictionary scan
      running. v2: NOT_RUN (the check cannot run on the input).
  P6  test_bigram_consistency: the reading's first character absent
      from the language model returned PASS
      ("char_not_in_lm—pass_by_default"). v2: NOT_RUN.
  P7  test_bigram_consistency: no qualifying anchor neighbour
      returned PASS ("no_anchor_neighbours—pass_by_default").
      v2: NOT_RUN.

And the non-credit input default the enumeration named (historical
test_positional, line 110): a missing avg_position was silently
defaulted to 0.5 before the expectation checks ran — and a recorded
0.0 was overwritten by the same ``or``. v2 never computes on a
defaulted input: a role record with no usable avg_position is
NOT_RUN for the positional check.

Every other check is the historical check, unchanged: the same
expectation table, the same DEDR exact/prefix rules, the same
bigram neighbour rule (the sign's top-5 following signs with
HIGH/MEDIUM anchor readings; match ratio >= 0.4). One determinism
correction inside P8 (the genuine bigram path): the historical
script's LM comparison set was backend-dependent (torch top-5
continuations with torch installed, ALL continuations without).
v2 computes the top-5 continuation characters deterministically
from the LM probabilities (probability descending, character
ascending on ties) and never imports torch, so the check is the
same test on every backend.

Outcomes are tri-state: "pass" / "fail" / "not_run". A missing
input, an unexecuted check, or an inapplicable test produces
not_run or fail, never credit (C091-8).

Aggregation (the historical rule, with the defaults removed): a
sign is promoted iff at least 2 of the 3 checks PASS. A not_run
never counts toward the threshold.

The T302 disposition rule, stated here before any run: over the
WP5 Phase-48 subset's 28 (the promotions standing at
requires_revalidation in the WP5 audit), a sign the corrected
battery promotes stands promoted on the new evidence — its
reclassification act moves it to supported_internal_only (a
battery promotion is an internal validation event, never
independent support; C091-9's "does not establish"). A sign the
corrected battery does not promote moves to
insufficient_evidence: the support its promotion rested on has
now been judged by the corrected instrument and found
insufficient. Every act carries the sign's full per-check outcome
vector, so a not_run inside a disposition is inseparable from the
disposition it fed.

Inputs (the same files the historical battery read):

  corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv
  corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv
  backend/reports/INDUS_FINAL_ANCHORS.json
  backend/glossa_lab/data/dravidian_tamil_lm.json
  reports/jambu-dedr/data/dedr/dedr_new.csv  (the DEDR dataset)

The DEDR dataset is NOT HELD in this tree: reports/jambu-dedr is
an unpopulated submodule whose content is absent from the repo,
from the live origin, and from this clone. With the dataset
absent, the DEDR check is NOT_RUN for every sign, with that
reason recorded per sign — the machinery's honest outcome for an
unheld input, never a silently empty scan (the historical loader
swallowed the absence and scored the empty scan as no-match
fails).

Execution (T302) is a run under run-defs v2 (surface `study`,
store = the citing spec's records/), its id minted at execution
start (D-089-1), written through ``glossa_lab.run_records``.
``--execute`` refuses if the acts file already exists: a run's
dispositions are filed once, and a second execution is a new run
under a new commission, not an overwrite.

Standing position: the Indus script is not deciphered. A battery
promotion is an internal validation event; nothing here is a
decipherment result (C091-15).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from glossa_lab import run_records  # noqa: E402
from glossa_lab.verified_write import write_file_verified  # noqa: E402

TOOL_NAME = "phase48_medium_validation_v2.py"
TOOL_VERSION = "battery v2 (Spec 091 Stage 3, T301/T302)"
BATTERY_ID = "phase48-battery-v2"

PASS = "pass"
FAIL = "fail"
NOT_RUN = "not_run"

SPEC_REL = "specs/091-anchor-comparison-integrity"
SPEC_RECORDS_REL = f"{SPEC_REL}/records"
ACTS_REL = f"{SPEC_RECORDS_REL}/t302-reclassification-acts.json"
WP5_AUDIT_REL = "docs/repair-2026-10-26/anchor-support-audit.json"
T104_REL = f"{SPEC_RECORDS_REL}/t104-pass-by-default-enumeration.json"
HISTORICAL_BATTERY_REL = "backend/scripts/phase48_medium_validation.py"

CORPUS_REL = "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES_REL = (
    "corpora/downloads/external_repos/holdatllc_indus/"
    "all_symbol_semantic_roles 2.csv"
)
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
DEDR_REL = "reports/jambu-dedr/data/dedr/dedr_new.csv"
LM_REL = "backend/glossa_lab/data/dravidian_tamil_lm.json"

# Positional expectations per Holdat role — the historical battery's
# table, verbatim (backend/scripts/phase48_medium_validation.py).
ROLE_POSITIONAL_EXPECT = {
    "CASE_MARKER_SUFFIX": {"avg_pos_min": 0.5, "is_ending": True, "is_starter": False},
    "CLASSIFIER_PREFIX": {"avg_pos_max": 0.2, "is_ending": False, "is_starter": True},
    "PERSON_OR_OWNER": {
        "avg_pos_min": 0.3,
        "avg_pos_max": 0.75,
        "is_ending": None,
        "is_starter": None,
    },
    "STRONG_PERSON_OR_OWNER": {"avg_pos_min": 0.3, "avg_pos_max": 0.75},
    "UNKNOWN": {},
}

PROMOTION_THRESHOLD = 2


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Loaders (the historical battery's, with the DEDR absence made explicit)


def load_all(repo_root: Path):
    anchors = json.loads((repo_root / ANCHORS_REL).read_text("utf-8"))
    roles = {}
    with open(repo_root / ROLES_REL, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            roles[r["symbol"]] = r
    with open(repo_root / CORPUS_REL, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    freq = Counter(r["letters"] for r in rows if r["letters"])
    inscriptions: dict[str, list] = {}
    for r in rows:
        cisi = r["cisi_number"]
        pos = int(r.get("position", 0) or 0)
        inscriptions.setdefault(cisi, [])
        while len(inscriptions[cisi]) <= pos:
            inscriptions[cisi].append("")
        inscriptions[cisi][pos] = r["letters"]
    seqs = [[s for s in v if s] for v in inscriptions.values() if any(v)]
    return anchors, roles, freq, seqs


def load_lm(repo_root: Path):
    raw = json.loads((repo_root / LM_REL).read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    total = sum(bigrams.values()) or 1
    return {tuple(k.split(",", 1)): v / total for k, v in bigrams.items() if "," in k}


def load_dedr(repo_root: Path):
    """The DEDR entries, or None when the dataset is not held.

    The historical loader caught every exception and returned an
    empty list, so an absent dataset was scored as an executed
    scan that found nothing. v2 makes the absence explicit: None
    means the check cannot run.
    """
    path = repo_root / DEDR_REL
    if not path.is_file():
        return None
    entries = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for row in csv.reader(f):
            if len(row) >= 5:
                word = row[2].strip() if len(row) > 2 else ""
                gloss = row[3].strip() if len(row) > 3 else ""
                if word and len(word) > 1:
                    entries.append((word.lower(), gloss.lower()))
    return entries


# ---------------------------------------------------------------------------
# The three checks, corrected (tri-state outcomes)


def test_positional_v2(sign: str, reading: str, role: dict) -> tuple[str, str]:
    """TEST 1: does avg_position match the Holdat role prediction?

    Corrections over the historical test: P2 (no expectation ->
    pass) returns not_run; a missing or unparseable avg_position
    returns not_run instead of being defaulted to 0.5 (the
    enumeration's named non-credit default, historical line 110);
    a role record absent entirely is not_run (absent input), where
    the historical test returned a fail for "no_role_data".
    """
    if not role:
        return NOT_RUN, "no_role_data—not_run"
    sem_role = role.get("semantic_role") or "UNKNOWN"
    expect = ROLE_POSITIONAL_EXPECT.get(sem_role)
    if expect is None or not expect:
        return NOT_RUN, "no_expectation—not_run"
    raw_pos = role.get("avg_position")
    if raw_pos is None or str(raw_pos).strip() == "":
        return NOT_RUN, "avg_position_absent—not_run"
    try:
        avg_pos = float(raw_pos)
    except (TypeError, ValueError):
        return NOT_RUN, "avg_position_unparseable—not_run"
    if expect.get("is_ending") is not None and role.get("is_ending") is None:
        return NOT_RUN, "is_ending_absent—not_run"
    if expect.get("is_starter") is not None and role.get("is_starter") is None:
        return NOT_RUN, "is_starter_absent—not_run"
    is_starter = role.get("is_starter", "") == "True"
    is_ending = role.get("is_ending", "") == "True"

    ok = True
    reason_parts = []
    if "avg_pos_min" in expect and avg_pos < expect["avg_pos_min"]:
        ok = False
        reason_parts.append(f"pos={avg_pos:.2f}<{expect['avg_pos_min']}")
    if "avg_pos_max" in expect and avg_pos > expect["avg_pos_max"]:
        ok = False
        reason_parts.append(f"pos={avg_pos:.2f}>{expect['avg_pos_max']}")
    if expect.get("is_ending") is not None and is_ending != expect["is_ending"]:
        ok = False
        reason_parts.append(f"ending={is_ending}!={expect['is_ending']}")
    if expect.get("is_starter") is not None and is_starter != expect["is_starter"]:
        ok = False
        reason_parts.append(f"starter={is_starter}!={expect['is_starter']}")

    return (PASS if ok else FAIL), ("PASS" if ok else f"FAIL: {'; '.join(reason_parts)}")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower())


def test_dedr_v2(reading: str, dedr_entries) -> tuple[str, str]:
    """TEST 2: is the reading attested in DEDR?

    Corrections over the historical test: P3 (normalized reading
    shorter than 2 characters -> pass without scanning) returns
    not_run; a dataset that is not held (dedr_entries is None)
    returns not_run instead of being scored as an empty scan.
    The exact/prefix rules are the historical rules, unchanged.
    """
    if dedr_entries is None:
        return NOT_RUN, "dedr_dataset_not_held—not_run"
    reading_clean = _norm(reading)
    if len(reading_clean) < 2:
        return NOT_RUN, "too_short—not_run"
    exact = sum(1 for w, g in dedr_entries if _norm(w) == reading_clean)
    prefix = sum(
        1
        for w, g in dedr_entries
        if _norm(w).startswith(reading_clean[:3])
        or reading_clean.startswith(_norm(w)[:3])
    )
    if exact > 0:
        return PASS, f"exact_match_{exact}"
    if prefix >= 2:
        return PASS, f"prefix_match_{prefix}"
    return FAIL, f"no_dedr_match (tried {reading_clean!r}, {prefix} prefix hits)"


def test_bigram_consistency_v2(
    sign: str, reading: str, seqs: list, bigram_prob: dict, anchors: dict
) -> tuple[str, str]:
    """TEST 3: do corpus neighbours align with Dravidian bigrams
    for this reading?

    Corrections over the historical test: P6 (reading's first
    character absent from the LM -> pass) returns not_run; P7 (no
    qualifying anchor neighbour -> pass) returns not_run. The LM
    comparison set is the top-5 continuation characters computed
    deterministically (probability descending, character ascending
    on ties) — the historical script's set was backend-dependent
    (torch top-5 vs all continuations); v2 never imports torch.
    The neighbour rule is unchanged: the sign's top-5 following
    signs, those with HIGH/MEDIUM anchor readings checked, match
    ratio >= 0.4 passes.
    """
    all_chars = sorted(set(t for pair in bigram_prob for t in pair))
    char_set = set(all_chars)
    reading_char = reading[0] if reading else "?"
    if reading_char not in char_set:
        return NOT_RUN, "char_not_in_lm—not_run"

    continuations = sorted(
        ((b, p) for (a, b), p in bigram_prob.items() if a == reading_char),
        key=lambda bp: (-bp[1], bp[0]),
    )
    top5_chars = {b for b, _ in continuations[:5]}

    post: Counter = Counter()
    for insc in seqs:
        for i, s in enumerate(insc):
            if s == sign and i < len(insc) - 1:
                post[insc[i + 1]] += 1

    matches = 0
    total_checked = 0
    for neighbor_sign, _cnt in post.most_common(5):
        a = anchors.get(neighbor_sign, {})
        if a.get("confidence") in ("HIGH", "MEDIUM") and a.get("reading"):
            neighbor_char = a["reading"][0]
            total_checked += 1
            if neighbor_char in top5_chars:
                matches += 1
    if total_checked == 0:
        return NOT_RUN, "no_anchor_neighbours—not_run"
    ratio = matches / total_checked
    return (PASS if ratio >= 0.4 else FAIL), (
        f"neighbour_match={matches}/{total_checked}={ratio:.1%}"
    )


# ---------------------------------------------------------------------------
# Evaluation + the disposition rule (one pure function of a result entry)


def evaluate_sign(
    sign: str,
    anchor: dict,
    role: dict,
    n_corpus: int,
    seqs: list,
    bigram_prob: dict,
    dedr_entries,
    anchors: dict,
) -> dict:
    reading = anchor.get("reading", "")
    t1_outcome, t1_detail = test_positional_v2(sign, reading, role)
    t2_outcome, t2_detail = test_dedr_v2(reading, dedr_entries)
    t3_outcome, t3_detail = test_bigram_consistency_v2(
        sign, reading, seqs, bigram_prob, anchors
    )
    tests = {
        "positional": {"outcome": t1_outcome, "detail": t1_detail},
        "dedr": {"outcome": t2_outcome, "detail": t2_detail},
        "bigram": {"outcome": t3_outcome, "detail": t3_detail},
    }
    n_pass = sum(1 for t in tests.values() if t["outcome"] == PASS)
    n_fail = sum(1 for t in tests.values() if t["outcome"] == FAIL)
    n_not_run = sum(1 for t in tests.values() if t["outcome"] == NOT_RUN)
    return {
        "sign": sign,
        "reading": reading,
        "n_corpus": n_corpus,
        "holdat_role": role.get("semantic_role", "?") if role else "?",
        "tests": tests,
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_not_run": n_not_run,
        "score": n_pass,
        "promote": n_pass >= PROMOTION_THRESHOLD,
    }


def disposition_for(result_entry: dict) -> str:
    """The T302 disposition rule, as stated in this module's
    docstring before any run: promoted -> supported_internal_only;
    not promoted -> insufficient_evidence."""
    return "supported_internal_only" if result_entry["promote"] else "insufficient_evidence"


# ---------------------------------------------------------------------------
# The WP5 Phase-48 subset (the population of record)


def derive_subset_28(repo_root: Path):
    """The 28, derived mechanically from the WP5 audit: the
    recorded Phase-48 promotions whose audit disposition stands at
    requires_revalidation. The remaining recorded promotions (the
    insufficient-evidence pair) are outside this spec (GR-088-27)
    and are returned separately so the record names them."""
    audit = json.loads((repo_root / WP5_AUDIT_REL).read_text("utf-8"))
    records = {r["sign"]: r for r in audit["records"]}
    promoted = audit["phase48_summary"]["promoted_signs_in_recorded_order"]
    subset = [
        s
        for s in promoted
        if records[s]["current_evidential_status"] == "requires_revalidation"
    ]
    excluded = [
        {
            "sign": s,
            "current_evidential_status": records[s]["current_evidential_status"],
            "disposition_rule": records[s].get("disposition_rule"),
            "note": "Recorded Phase-48 promotion outside the T302 population: "
            "not standing at requires_revalidation (GR-088-27's pair, "
            "outside Spec 091).",
        }
        for s in promoted
        if s not in subset
    ]
    return subset, excluded, audit


# ---------------------------------------------------------------------------
# Execution (T302): one run under run-defs v2, dispositions as acts


def execute(repo_root: Path) -> dict:
    acts_path = repo_root / ACTS_REL
    if acts_path.exists():
        raise SystemExit(
            f"refusing to execute: {ACTS_REL} already exists — a run's "
            "dispositions are filed once; a second execution is a new "
            "run under a new commission, not an overwrite"
        )
    started = datetime.now(timezone.utc)
    run_id = run_records.mint_run_id("study", now=started)

    subset, excluded, _audit = derive_subset_28(repo_root)
    if len(subset) != 28:
        raise SystemExit(
            f"population census failed: derived {len(subset)} of the 28 "
            "from the WP5 audit — refusing to run over a miscounted "
            "population"
        )

    anchors_data, roles, freq, seqs = load_all(repo_root)
    anchors = anchors_data["anchors"]
    lm = load_lm(repo_root)
    dedr_entries = load_dedr(repo_root)

    results = []
    for sign in subset:
        anchor = anchors.get(sign)
        if anchor is None:
            raise SystemExit(
                f"population census failed: {sign} is in the WP5 subset "
                "but absent from INDUS_FINAL_ANCHORS — refusing to file "
                "a disposition for an anchor the run did not test"
            )
        results.append(
            evaluate_sign(
                sign,
                anchor,
                roles.get(sign, {}),
                freq.get(sign, 0),
                seqs,
                lm,
                dedr_entries,
                anchors,
            )
        )

    n_promoted = sum(1 for r in results if r["promote"])
    census = {
        "n_tested": len(results),
        "n_promoted": n_promoted,
        "n_not_promoted": len(results) - n_promoted,
        "by_disposition": dict(
            Counter(disposition_for(r) for r in results)
        ),
        "n_checks_pass": sum(r["n_pass"] for r in results),
        "n_checks_fail": sum(r["n_fail"] for r in results),
        "n_checks_not_run": sum(r["n_not_run"] for r in results),
    }

    pins = {
        "spec": "091-anchor-comparison-integrity",
        "stage": "stage-3-battery-v2-rerun",
        "frozen_artifacts": {
            "historical_battery_sha256": sha256_file(
                repo_root / HISTORICAL_BATTERY_REL
            ),
            "wp5_audit_sha256": sha256_file(repo_root / WP5_AUDIT_REL),
            "anchors_sha256": sha256_file(repo_root / ANCHORS_REL),
            "corpus_sha256": sha256_file(repo_root / CORPUS_REL),
            "roles_sha256": sha256_file(repo_root / ROLES_REL),
            "lm_sha256": sha256_file(repo_root / LM_REL),
            "t104_enumeration_sha256": sha256_file(repo_root / T104_REL),
            "dedr_dataset": (
                "not held — reports/jambu-dedr submodule unpopulated; "
                "the DEDR check is not_run for every sign in this run"
            ),
        },
        "battery_v2_sha256": sha256_file(Path(__file__)),
    }

    acts = [
        {
            "sign": r["sign"],
            "act": "reclassification",
            "from_disposition": "requires_revalidation",
            "to_disposition": disposition_for(r),
            "basis": {
                "run_id": run_id,
                "battery": BATTERY_ID,
                "score": r["score"],
                "promotion_threshold": PROMOTION_THRESHOLD,
                "tests": r["tests"],
            },
            "prior_basis": (
                "WP5 anchor-support audit, rule R5a_phase48_promotion "
                "(the historical battery's output)"
            ),
        }
        for r in results
    ]
    acts_record = {
        "record_id": "spec091-t302-reclassification-acts",
        "spec": "091-anchor-comparison-integrity",
        "task": "T302",
        "claims": ["C091-9", "C091-13"],
        "generated_by": f"{TOOL_NAME} --execute (Spec 091 Stage 3, T302)",
        "run_id": run_id,
        "battery": {
            "id": BATTERY_ID,
            "tool": TOOL_NAME,
            "tool_version": TOOL_VERSION,
            "sha256": pins["battery_v2_sha256"],
        },
        "disposition_rule": (
            "promoted by the corrected battery (score >= 2 passes; "
            "not_run never counts) -> supported_internal_only; not "
            "promoted -> insufficient_evidence. Stated in the "
            "battery's docstring before the run."
        ),
        "acts": acts,
        "evidence_retirement": {
            "act": "evidence_retirement",
            "scope_signs": subset,
            "retired": (
                "The Phase-48 historical battery's output "
                "(phase48_medium_validation.py's recorded run, as "
                "reconstructed in the WP5 anchor-support audit's "
                "phase48_reconstruction fields) as evidence for the "
                "28 promotions' dispositions"
            ),
            "superseded_by_run": run_id,
            "claim": "C091-9",
            "note": (
                "The historical output remains of record in the WP5 "
                "audit and in git history; it is retired AS EVIDENCE "
                "for these dispositions, not deleted or edited."
            ),
        },
    }
    payload = json.dumps(acts_record, indent=1, ensure_ascii=False) + "\n"
    write_file_verified(acts_path, payload.encode("utf-8"))
    acts_sha = sha256_file(acts_path)

    code_version = "unknown"
    try:
        import subprocess

        code_version = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except Exception:
        pass
    finished = datetime.now(timezone.utc)
    header = run_records.build_header(
        surface="study",
        tool=f"{TOOL_NAME} --execute",
        tool_version=TOOL_VERSION,
        command=f"{TOOL_NAME} --execute",
        code_version=code_version,
        input_pins=pins,
        seed=run_records.NO_SEED,
        environment_class="mini-server/linux",
        started=started,
        finished=finished,
        run_id=run_id,
    )
    run_record = run_records.build_record(
        header,
        result={
            "population": subset,
            "excluded_from_subset": excluded,
            "results": results,
            "census": census,
            "acts": ACTS_REL,
            "acts_sha256": acts_sha,
        },
    )
    store = repo_root / SPEC_RECORDS_REL
    written = run_records.write_run_record(store, run_record)
    return {
        "run_id": run_id,
        "run_record": str(written.relative_to(repo_root)),
        "acts": ACTS_REL,
        "acts_sha256": acts_sha,
        "census": census,
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    if args.execute:
        outcome = execute(repo_root)
        print(json.dumps(outcome, indent=1, ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
