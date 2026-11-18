"""Spec 091 Stage 3, T303 — the 5's site-statistics arm, executed.

The site-statistics-arm revalidations of Stage 1's T105 split
(`records/t105-checker-arm-split.json`): M042, M046, M108 (rule
R5b, restored readings) and M176, M342 (rule R5c, Phase-48 cited
as support). T105 determined all five require the site-statistics
arm, none requires the phonotactic arm, and none is
undeterminable — so C091-11's GR-088-04 gating does not engage
for the five, and this leg produces no phonotactic verdict for
any anchor. The gated set is empty; it is recorded in the acts
in the same motion, with GR-088-04 (WP2: the phonotactic
certification leg) named as the dependency that would govern
any anchor that required the arm.

The measurement — the Phase-69 lineage, corrected. The table is
built exactly as the historical site-stratification script
(`backend/scripts/phase69_site_stratification.py`, guarded under
Spec 095 and pinned below as the lineage definition) builds it:
seals grouped by cisi_number, signs placed by position, the
seal's site taken from its first row; per site, the sign's
[initial, medial, terminal] counts under the lineage binning
(position 0 of a multi-sign inscription is initial, the last
position is terminal, everything else — including a single-sign
inscription — is medial); sites in sorted order; a site's row
enters the table iff the sign's total at that site is >= 3. The
table is computed by the repair brief's corrected checker,
`glossa_lab.site_stats_v2.chi_square_independence` (Pearson
chi-square, no Yates correction; module site-stats-v2.0.0).

What the correction changes, per the repair record: the p-value
is computed (the historical routine could only ever emit
p in {0.0, 0.5, 1.0}); insufficient data is an explicit
INSUFFICIENT_DATA status carrying no statistic and no p-value
(the historical routine dressed it with placeholder 0.0 / 1.0);
and there is NO invariance verdict — the checker detects
differences only, and equivalence is NOT_ASSESSED: no
prespecified equivalence margin or procedure is registered for
this arm, and the program's statistical standard (Spec 095,
STANDARDS.md Part II) bars deriving equivalence from a
non-significant difference test.

The T303 disposition rule, stated here before any run. Every
anchor whose arm executes moves from requires_revalidation to
insufficient_evidence; the act carries the outcome kind —
`difference_detected` (checker OK, p < 0.05: the corrected test
contradicts the distributional consistency the defective
validation claimed), `difference_not_detected` (checker OK,
p >= 0.05: no difference detected, which under the corrected
doctrine re-earns nothing — the support is not re-earned, and
no outcome of a difference-detection-only checker can restore
a supported class), or `insufficient_data` (checker
INSUFFICIENT_DATA: the data the lineage construction yields
cannot support the test the support rested on). The
authorities: GR-088-03 candidate 2's falsifier, carried into
C091-10 — *the v2 checkers judge the support insufficient →
the 5 move to insufficient evidence, not back to supported*
(candidate 3's contrasting falsifier, "stay
requires-revalidation", is the R5d four's, not the five's); and
C091-11's falsifier, which bars leaving one of the 5 at
requires_revalidation after the site-statistics arm ran
without the GR-088-04 dependency named where the phonotactic
arm was required — for the five it is not required, so no such
naming is available. A checker ERROR refuses the run: no
dispositions are filed on a defective execution. If the Holdat
corpus were not held, the arm would be not_run for all five
and no dispositions would be filed; `--execute` refuses with
that reason named. The corpus IS held for this run (staged
from the live origin into the clone's gitignored corpora/
tree; its SHA-256 is pinned in the run record and matches the
T302 run's pin).

Execution is one run under the registered run definitions
(run-defs v2 — tasks.md's T303 text says "run-defs v1"; the
registered definitions as they stand are v2, the naming
discrepancy carried from Stage 2 and T302), surface `study`,
store = this spec's records/, its id minted at execution start
(D-089-1), written through `glossa_lab.run_records`; the acts
are written through the verified-write library. `--execute`
refuses if the acts file already exists: a run's dispositions
are filed once.

Boundary (the task's own limit): these are checker-arm
outcomes only — no independent support is claimed for any
anchor by this leg, and no WP5 disposition outside the five is
touched. The frozen WP5 audit, the T105 record, the anchors
file, and the claims ledger are unmodified.

Standing position: the Indus script is not deciphered
(C091-15).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from glossa_lab import run_records  # noqa: E402
from glossa_lab.site_stats_v2 import MODULE_VERSION as CHECKER_VERSION  # noqa: E402
from glossa_lab.site_stats_v2 import chi_square_independence  # noqa: E402
from glossa_lab.verified_write import write_file_verified  # noqa: E402

TOOL_NAME = "spec091_stage3_site_stats.py"
TOOL_VERSION = "site-stats arm v1 (Spec 091 Stage 3, T303)"
CHECKER_ID = "site-stats-v2"

SPEC_REL = "specs/091-anchor-comparison-integrity"
SPEC_RECORDS_REL = f"{SPEC_REL}/records"
ACTS_REL = f"{SPEC_RECORDS_REL}/t303-reclassification-acts.json"
T105_REL = f"{SPEC_RECORDS_REL}/t105-checker-arm-split.json"
WP5_AUDIT_REL = "docs/repair-2026-10-26/anchor-support-audit.json"
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
CORPUS_REL = "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
PHASE69_REL = "backend/scripts/phase69_site_stratification.py"
SITE_STATS_REL = "backend/glossa_lab/site_stats_v2.py"

# The lineage's constants, from phase69_site_stratification.py:
# a site's row enters the table iff the sign's total there is
# >= 3, and p < 0.05 was its SITE_VARIANT threshold (the label
# is not reused; the threshold is the detection threshold).
MIN_SITE_TOTAL = 3
ALPHA = 0.05

EXPECTED_FIVE = ["M042", "M046", "M108", "M176", "M342"]
FROM_DISPOSITION = "requires_revalidation"
TO_DISPOSITION = "insufficient_evidence"

POSITION_BINS = ["initial", "medial", "terminal"]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# The population of record (T105's split, derived mechanically)


def derive_population(repo_root: Path):
    """The five, derived from the T105 determination record:
    the determinations requiring the site-statistics arm, in
    record order; the phonotactic-required and
    phonotactic-gated sets read alongside (both empty for the
    five — the same-motion recording in the acts rests on
    them)."""
    split = json.loads((repo_root / T105_REL).read_text("utf-8"))
    determinations = {d["sign"]: d for d in split["determinations"]}
    population = [
        d["sign"]
        for d in split["determinations"]
        if d["determination"]["site_statistics_arm_required"]
    ]
    phonotactic_required = [
        d["sign"]
        for d in split["determinations"]
        if d["determination"]["phonotactic_arm_required"]
    ]
    phonotactic_gated = [
        d["sign"]
        for d in split["determinations"]
        if d["determination"]["phonotactic_gated"]
    ]
    return population, phonotactic_required, phonotactic_gated, determinations


# ---------------------------------------------------------------------------
# The lineage table construction (phase69, verbatim semantics)


def parse_corpus(corpus_path: Path) -> dict[str, list]:
    """Seals grouped by cisi_number, signs placed by position,
    the seal's site from its first row — the historical
    script's parsing, unchanged. Returns {site: [inscription,
    ...]} with each inscription its non-empty signs in position
    order."""
    seals: dict[str, dict] = {}
    with open(corpus_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]
            p = int(row.get("position", 0) or 0)
            s = (row.get("letters") or "").strip()
            site = (row.get("site") or "UNKNOWN").strip()
            if c not in seals:
                seals[c] = {"signs": [], "site": site}
            while len(seals[c]["signs"]) <= p:
                seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    site_inscriptions: dict[str, list] = {}
    for seal_data in seals.values():
        signs = [s for s in seal_data["signs"] if s]
        if signs:
            site_inscriptions.setdefault(seal_data["site"], []).append(signs)
    return site_inscriptions


def sign_site_counts(site_inscriptions: dict, sign: str) -> dict[str, list]:
    """Per site (sorted), the sign's [initial, medial,
    terminal] counts under the lineage binning: position 0 of
    a multi-sign inscription is initial, the last position is
    terminal, everything else — including a single-sign
    inscription — is medial."""
    counts: dict[str, list] = {}
    for site in sorted(site_inscriptions):
        bins = [0, 0, 0]
        for ins in site_inscriptions[site]:
            n = len(ins)
            for pos, s in enumerate(ins):
                if s != sign:
                    continue
                if pos == 0 and n > 1:
                    bins[0] += 1
                elif pos == n - 1 and n > 1:
                    bins[2] += 1
                else:
                    bins[1] += 1
        counts[site] = bins
    return counts


def build_table(counts: dict[str, list]):
    """The lineage's site-inclusion rule: a site's row enters
    the table iff the sign's total at that site is >= 3.
    Returns (rows, included_sites, excluded_sites) with the
    excluded sites' counts carried for the record."""
    rows: list[list] = []
    included: list[str] = []
    excluded: list[dict] = []
    for site in sorted(counts):
        bins = counts[site]
        total = sum(bins)
        if total >= MIN_SITE_TOTAL:
            included.append(site)
            rows.append(list(bins))
        else:
            excluded.append(
                {"site": site, "counts": list(bins), "total": total}
            )
    return rows, included, excluded


# ---------------------------------------------------------------------------
# The outcome mapping (one pure function of the checker's result)


def outcome_kind_for(checker: dict) -> str:
    """The outcome kind of a recorded checker result. An ERROR
    result raises: no disposition is ever filed on a defective
    execution."""
    status = checker["status"]
    if status == "INSUFFICIENT_DATA":
        return "insufficient_data"
    if status == "OK":
        if checker["p_value"] is None:
            raise ValueError("checker status OK with no p_value recorded")
        return (
            "difference_detected"
            if checker["p_value"] < ALPHA
            else "difference_not_detected"
        )
    raise ValueError(
        f"checker status {status!r} produces no disposition: "
        "an ERROR execution is a defect, not an outcome"
    )


def disposition_for(checker: dict) -> str:
    """The T303 disposition rule, as stated in this module's
    docstring before any run: every executed arm moves its
    anchor to insufficient_evidence (the outcome kind is
    carried in the act, inseparable from the disposition)."""
    outcome_kind_for(checker)
    return TO_DISPOSITION


# ---------------------------------------------------------------------------
# Evaluation


def evaluate_sign(
    sign: str,
    reading: str,
    disposition_rule: str,
    site_inscriptions: dict,
) -> dict:
    counts = sign_site_counts(site_inscriptions, sign)
    rows, included, excluded = build_table(counts)
    checker = chi_square_independence(rows).to_dict()
    if checker["status"] == "ERROR":
        raise SystemExit(
            f"checker ERROR for {sign}: {checker['error']} — "
            "refusing to file dispositions on a defective execution"
        )
    return {
        "sign": sign,
        "reading": reading,
        "disposition_rule": disposition_rule,
        "n_corpus": sum(sum(c) for c in counts.values()),
        "table": {
            "position_bins": POSITION_BINS,
            "sites_included": included,
            "rows": rows,
            "sites_excluded": excluded,
            "all_site_counts": {site: counts[site] for site in sorted(counts)},
        },
        "checker": checker,
        "outcome_kind": outcome_kind_for(checker),
        "to_disposition": disposition_for(checker),
    }


# ---------------------------------------------------------------------------
# Execution (T303): one run under run-defs v2, dispositions as acts


def execute(repo_root: Path) -> dict:
    acts_path = repo_root / ACTS_REL
    if acts_path.exists():
        raise SystemExit(
            f"refusing to execute: {ACTS_REL} already exists — a run's "
            "dispositions are filed once; a second execution is a new "
            "run under a new commission, not an overwrite"
        )
    corpus_path = repo_root / CORPUS_REL
    if not corpus_path.is_file():
        raise SystemExit(
            f"corpus not held: {CORPUS_REL} is absent — the "
            "site-statistics arm is not_run for all five and no "
            "dispositions are filed (an unheld input is a named "
            "outcome, never a silently empty scan)"
        )
    started = datetime.now(timezone.utc)
    run_id = run_records.mint_run_id("study", now=started)

    population, phonotactic_required, phonotactic_gated, determinations = (
        derive_population(repo_root)
    )
    if (
        population != EXPECTED_FIVE
        or phonotactic_required != []
        or phonotactic_gated != []
    ):
        raise SystemExit(
            "population census failed: the T105 split derives "
            f"site-statistics {population}, phonotactic-required "
            f"{phonotactic_required}, phonotactic-gated "
            f"{phonotactic_gated} — refusing to run over a "
            "population other than the five of record with an "
            "empty phonotactic subset"
        )

    audit = json.loads((repo_root / WP5_AUDIT_REL).read_text("utf-8"))
    audit_records = {r["sign"]: r for r in audit["records"]}
    anchors = json.loads((repo_root / ANCHORS_REL).read_text("utf-8"))["anchors"]
    for sign in population:
        record = audit_records[sign]
        if record["current_evidential_status"] != FROM_DISPOSITION:
            raise SystemExit(
                f"population census failed: {sign} stands at "
                f"{record['current_evidential_status']!r} in the WP5 "
                f"audit, not {FROM_DISPOSITION!r} — refusing to file "
                "a reclassification from a state the record does "
                "not show"
            )
        if determinations[sign]["reading_as_recorded"] != anchors[sign]["reading"]:
            raise SystemExit(
                f"population census failed: {sign}'s reading as "
                "recorded in the T105 split "
                f"({determinations[sign]['reading_as_recorded']!r}) "
                "differs from the anchors file "
                f"({anchors[sign]['reading']!r}) — refusing to run "
                "over a mismatched identity"
            )

    site_inscriptions = parse_corpus(corpus_path)
    results = [
        evaluate_sign(
            sign,
            determinations[sign]["reading_as_recorded"],
            determinations[sign]["disposition_rule"],
            site_inscriptions,
        )
        for sign in population
    ]

    census = {
        "n_tested": len(results),
        "by_disposition": dict(Counter(r["to_disposition"] for r in results)),
        "by_outcome_kind": dict(Counter(r["outcome_kind"] for r in results)),
        "n_checker_ok": sum(
            1 for r in results if r["checker"]["status"] == "OK"
        ),
        "n_checker_insufficient_data": sum(
            1 for r in results if r["checker"]["status"] == "INSUFFICIENT_DATA"
        ),
    }

    pins = {
        "spec": "091-anchor-comparison-integrity",
        "stage": "stage-3-single-line",
        "frozen_artifacts": {
            "wp5_audit_sha256": sha256_file(repo_root / WP5_AUDIT_REL),
            "t105_split_sha256": sha256_file(repo_root / T105_REL),
            "anchors_sha256": sha256_file(repo_root / ANCHORS_REL),
            "corpus_sha256": sha256_file(corpus_path),
            "phase69_lineage_sha256": sha256_file(repo_root / PHASE69_REL),
            "site_stats_v2_sha256": sha256_file(repo_root / SITE_STATS_REL),
        },
        "runner_sha256": sha256_file(Path(__file__)),
    }

    acts = [
        {
            "sign": r["sign"],
            "act": "reclassification",
            "from_disposition": FROM_DISPOSITION,
            "to_disposition": r["to_disposition"],
            "basis": {
                "run_id": run_id,
                "checker": CHECKER_ID,
                "checker_module_version": CHECKER_VERSION,
                "outcome_kind": r["outcome_kind"],
                "checker_status": r["checker"]["status"],
                "statistic": r["checker"]["statistic"],
                "df": r["checker"]["df"],
                "p_value": r["checker"]["p_value"],
                "table": r["table"],
            },
            "prior_basis": {
                "disposition_rule": r["disposition_rule"],
                "support_lines": audit_records[r["sign"]][
                    "evidence_independence"
                ]["independent_lines"],
            },
        }
        for r in results
    ]
    acts_record = {
        "record_id": "spec091-t303-reclassification-acts",
        "spec": "091-anchor-comparison-integrity",
        "task": "T303",
        "claims": ["C091-10", "C091-11", "C091-13"],
        "generated_by": f"{TOOL_NAME} --execute (Spec 091 Stage 3, T303)",
        "run_id": run_id,
        "checker": {
            "id": CHECKER_ID,
            "module": "glossa_lab/site_stats_v2.py",
            "module_version": CHECKER_VERSION,
            "sha256": pins["frozen_artifacts"]["site_stats_v2_sha256"],
        },
        "disposition_rule": (
            "every anchor whose site-statistics arm executes moves "
            "requires_revalidation -> insufficient_evidence; the act "
            "carries the outcome kind (difference_detected / "
            "difference_not_detected / insufficient_data). Stated in "
            "the runner's docstring before the run, on GR-088-03 "
            "candidate 2's falsifier (C091-10) and C091-11's "
            "falsifier; the corrected checker detects differences "
            "only and produces no outcome that re-earns a support."
        ),
        "acts": acts,
        "phonotactic_arm": {
            "required_for": phonotactic_required,
            "gated_dispositions": [
                {
                    "sign": s,
                    "recorded_at": FROM_DISPOSITION,
                    "dependency": "GR-088-04",
                }
                for s in phonotactic_gated
            ],
            "dependency": (
                "GR-088-04 — WP2: the phonotactic certification leg "
                "(the linguist-certified rule set for phonotactics_v2)"
            ),
            "basis": (
                "Spec 091 Stage 1 T105 determination "
                "(records/t105-checker-arm-split.json): the "
                "phonotactic arm is required for none of the five "
                "and none is undeterminable, so the gated set is "
                "empty, no anchor is recorded at "
                "requires_revalidation on this dependency by this "
                "leg, and no phonotactic verdict is produced for "
                "any anchor (C091-11)."
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
            "population": population,
            "results": results,
            "census": census,
            "phonotactic_arm": acts_record["phonotactic_arm"],
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
