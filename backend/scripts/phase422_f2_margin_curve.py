#!/usr/bin/env python3
"""Phase-422 — Spec 060 execution (the Holdat site effect:
margin curve and shared population; design D-23, a residue
study of Spec 024 F2).

Executes the FROZEN Spec 060 contract
(specs/060-f2-margin-curve/freeze.md; freeze digest
8c04b1a8bf742d80ea6da41021fe569686a854cdecd1cb22f4b12f1c385be1a3;
OSF registration 8ywxc, approved and public before this run)
in full: step 0, arm 1, and arm 2, in the frozen order.

Gates, in the frozen order (spec section 4):

  0.1 Input integrity — every spec section 3 input hashes
      to its stated value: the repository files to their
      recomputed pins, and the two held layer files (at the
      Phase-137 loaders' default paths, DD-060-15) to the
      values recorded in the Phase-137 results. A mismatch
      stops the run as INVALID.
  0.2 Population reproduction, both layers — the
      Phase-137 module's own loaders and frozen population
      rule (via the Phase-384 v2 module's own population
      builder) reproduce each layer's recorded profile
      table exactly, with the recorded counts, table
      dimensions, chi-square, and V. A mismatch stops the
      run as INVALID.
  0.3 Estimator regression — the Phase-384 v2 estimator,
      run unchanged on the two full-layer populations
      (one numpy default_rng(20261012) stream, F2 first
      then F3, exactly as the Phase-384 v2 script runs
      them), reproduces the recorded governing intervals
      exactly. A mismatch stops the run as INVALID.
  0.4 Shared-population census (arm 2's gate; margins and
      counts only) — the shared population of spec
      section 5.2 is constructed and censused: the site
      intersection re-derived from the pinned layers,
      per-layer and per-site counts. Fewer than 5 shared
      sites or fewer than 500 inscriptions in either
      layer closes arm 2 as TOO THIN, with the counts
      stated; arm 1 proceeds (DD-060-11).

Arm 1 (spec section 5.1) — the margin curve on the full
Holdat population: the governing interval recomputed at
gate 0.3 under the Phase-384 v2 estimator, reported as a
function of the margin on the fixed grid 0.05 / 0.075 /
0.10 / 0.125 / 0.15, each cell worded by the frozen family
rule, labelled sensitivity in every product. The recorded
verdict at 0.10 stands and no cell replaces it.

Arm 2 (spec section 5.2, if gate 0.4 passed) — the shared
population: from each layer's Phase-137 analysis
population, both layers restricted to the sites present
in both layers' analysis populations, and to the object
type present in both, SEAL (DD-060-12: the Holdat layer
carries no object-type field and its type is a constant,
so the Holdat side enters whole and the ICIT side is
restricted to its recorded SEAL type class). The
site-effect size is computed in each layer separately
with identical code — the Phase-384 v2 estimator's own
population builder, bootstrap, and interval functions,
imported unchanged — each layer in its own sign
numbering; signs are never pooled, mapped, or harmonised
(F060-C14). The estimator's frozen population rule is
applied to each restricted population by that identical
code (site eligibility and the >= 10 sign-column rule
re-derived within the restricted population, exactly as
the Phase-384 builder derives them for any population it
is given); the census counts and the estimator
populations are both reported. The arm-2 bootstrap pair
runs on a fresh numpy default_rng(20261012) stream,
Holdat first then ICIT, mirroring the Phase-384 v2
script's layer order. Period mix is stated per layer in
the frozen wording (DD-060-13): PERIOD MIX NOT DESCRIBED
FOR THIS LAYER - FIELD NOT CARRIED, for both layers; no
period assignment is imported from any other source.

Outcomes (spec sections 6, 11): INVALID on a gate
0.1-0.3 failure, with no arm quantity computed; otherwise
arm 1 always reports its curve and arm 2 reports exactly
one of COMPOSITION EXPLAINS THE GAP (the two governing
intervals on the shared population overlap), COMPOSITION
DOES NOT (they still exclude each other), or TOO THIN
(gate 0.4). No verdict moves under this spec: F2 stands
CONTRADICTED at the declared margin 0.10 and F3 stands
SUPPORTED at the declared margin 0.10, exactly as
recorded.

Outputs (written on every terminal outcome):
  - reports/phase422_results.json (the machine record)
  - reports/phase422_report.md (the report, under spec
    section 8's headline rules)

Integrity: every section 3 pin is asserted before any
arm quantity; the anchors file is asserted byte-identical
before and after. The script is deterministic: a second
run reproduces both output files byte-identically.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO / "backend" / "scripts"

FREEZE_DIGEST = (
    "8c04b1a8bf742d80ea6da41021fe569686a854cdecd1cb22f4b12f1c385be1a3"
)
OSF_REGISTRATION = "https://osf.io/8ywxc/"
EXECUTION_DATE = "2026-10-21"

# Spec section 3 pins (repository files, recomputed at the
# draft and re-asserted two-route at the freeze).
REPO_PINS = [
    ("reports/phase137_results.json",
     "18f86f45892526b947a4a7447201be9d69584ec96d33a1d18139309b9dc2a7a1"),
    ("backend/scripts/phase137_site_repertoire.py",
     "e00dacf4df8f52871b482e36ca0a37f66503c5f1b107ee835ac99fa21dfc8c86"),
    ("reports/phase384_results.json",
     "dda6092d9f4d368869a6e3a590948dfa97d02c5db50bf75868d6e055f0896aad"),
    ("backend/scripts/phase384_stage2_margins_v2.py",
     "3313394e6a716898cdfd440a46333ebd2b9136b77306413ed1514eab322a72a5"),
    ("specs/026-rcph-framework-transfer/reruns/phase384-contract-v2.md",
     "f0a67bd766ae28a33edc33553613bf9c50cc933df1bfbe2b5e1192d6571bbc75"),
    ("specs/026-rcph-framework-transfer/reruns/phase384-freeze-v2.json",
     "5749c6b89ac26be6333e0c20457bc320ca624c15f5ca65e689c107aa12b7b8e9"),
    ("specs/034-matched-object-attribution/outcome.md",
     "c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175"),
    ("specs/024-evidence-integration/spec.md",
     "a817f698fd5f2dd0a2d324d580d25cba41fc989762b20e0b77a4144a02d3ee25"),
    ("backend/reports/INDUS_FINAL_ANCHORS.json",
     "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"),
]
# The two held layers: pins are the values recorded in the
# Phase-137 results (F2 / F3 input.sha256), asserted against
# the copies at the Phase-137 loaders' default paths.
HOLDAT_LAYER_SHA256 = (
    "62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e"
)
ICIT_LAYER_SHA256 = (
    "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)

MARGIN_GRID = [0.05, 0.075, 0.10, 0.125, 0.15]
PERIOD_STATEMENT = (
    "PERIOD MIX NOT DESCRIBED FOR THIS LAYER - FIELD NOT CARRIED"
)
NO_VERDICT_MOVES = (
    "No verdict moves under this spec: F2 stands CONTRADICTED "
    "at the declared margin 0.10 and F3 stands SUPPORTED at "
    "the declared margin 0.10, exactly as recorded."
)

_OUT_RESULTS = _REPO / "reports" / "phase422_results.json"
_OUT_REPORT = _REPO / "reports" / "phase422_report.md"

AI_DISCLOSURE = (
    "Executed by an AI agent (Muse Spark, via Muse) at the "
    "direction of Tristen Pierson, per constitution sec.VI."
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


MARGIN_LABELS = {
    0.05: "0.05", 0.075: "0.075", 0.10: "0.10",
    0.125: "0.125", 0.15: "0.15",
}


def _cell_word(margin: float, lo: float, hi: float) -> str:
    label = MARGIN_LABELS[margin]
    if hi < margin:
        return f"CONTRADICTED AT {label}"
    if lo > margin:
        return f"SUPPORTED AT {label}"
    return f"STRADDLES {label}"


def _analysis_population(p137, inscriptions):
    """The Phase-137 frozen population rule, mirroring the
    Phase-384 v2 builder's first steps: eligible sites from
    the parsed population, then inscriptions at eligible
    sites with at least one parsed token."""
    per_site_insc: Counter = Counter()
    per_site_parsed: Counter = Counter()
    for insc in inscriptions:
        per_site_insc[insc["site"]] += 1
        per_site_parsed[insc["site"]] += insc["n_parsed_tokens"]
    eligible = sorted(
        s for s in per_site_insc
        if p137.site_eligible(per_site_insc[s], per_site_parsed[s])
    )
    analysis = [
        i for i in inscriptions
        if i["site"] in set(eligible) and i["n_parsed_tokens"] >= 1
    ]
    return eligible, analysis


def main() -> int:
    anchors_before = _sha256(_REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")

    p137 = _load_module(
        "phase137_site_repertoire",
        _SCRIPTS / "phase137_site_repertoire.py")
    p384 = _load_module(
        "phase384_stage2_margins_v2",
        _SCRIPTS / "phase384_stage2_margins_v2.py")

    recorded137 = json.loads(
        (_REPO / "reports/phase137_results.json").read_text("utf-8"))
    recorded384 = json.loads(
        (_REPO / "reports/phase384_results.json").read_text("utf-8"))

    gates: dict = {}
    terminal = None  # ("INVALID", gate) once a gate 0.1-0.3 fails

    # ── Gate 0.1 — input integrity ──────────────────────
    checks = []
    for rel, pin in REPO_PINS:
        path = _REPO / rel
        observed = _sha256(path) if path.exists() else None
        checks.append({
            "input": rel, "pin": pin, "observed": observed,
            "present": path.exists(), "match": observed == pin,
        })
    for label, path, pin in (
        ("holdat_layer (held, Phase-137 loader default path)",
         p137.DEFAULT_HOLDAT, HOLDAT_LAYER_SHA256),
        ("icit_layer (held, Phase-137 loader default path)",
         p137.DEFAULT_HORUS, ICIT_LAYER_SHA256),
    ):
        observed = _sha256(path) if path.exists() else None
        checks.append({
            "input": f"{label}: {path}", "pin": pin,
            "observed": observed, "present": path.exists(),
            "match": observed == pin,
        })
    gate01_pass = all(c["match"] for c in checks)
    gates["0.1"] = {
        "gate": "0.1", "name": "Input integrity",
        "inputs": checks,
        "verdict": "PASS" if gate01_pass else "FAIL",
    }
    if not gate01_pass:
        terminal = ("INVALID", "0.1")

    holdat_insc = horus_insc = None
    full = {}  # per-layer full-population estimator records
    if terminal is None:
        holdat_insc, _ = p137.load_holdat(p137.DEFAULT_HOLDAT)
        horus_insc, _ = p137.load_horus(p137.DEFAULT_HORUS)

        # ── Gate 0.2 — population reproduction, both layers ──
        layer_specs = [
            ("F2_holdat", "Holdat compilation layer", holdat_insc,
             1670, [9, 98]),
            ("F3_icit_lineage", "ICIT-lineage layer (horus84)",
             horus_insc, 5410, [7, 187]),
        ]
        repro = []
        gate02_pass = True
        for key, label, inscriptions, exp_n, exp_dims in layer_specs:
            table, by_site, n_analysis = p384.build_population(
                p137, inscriptions)
            recorded = recorded137["layers"][key]
            recorded_table = np.array(
                recorded["profile_table"]["counts"])
            table_exact = (
                table.shape == recorded_table.shape
                and bool((table == recorded_table).all()))
            chi2, v = p384._chi2_v(table)
            rec_chi2 = recorded["observed_chi_square"]
            rec_v = recorded["cramers_v_descriptive"]
            chi2_ok = abs(chi2 - rec_chi2) / rec_chi2 <= 1e-9
            v_ok = abs(v - rec_v) <= 1e-9
            ok = (table_exact and n_analysis == exp_n
                  and list(table.shape) == exp_dims
                  and chi2_ok and v_ok)
            gate02_pass = gate02_pass and ok
            repro.append({
                "layer": key, "label": label,
                "n_analysis_inscriptions": n_analysis,
                "expected_n": exp_n,
                "table_dimensions": list(table.shape),
                "expected_dimensions": exp_dims,
                "profile_table_exact": table_exact,
                "recomputed_chi2": chi2, "recorded_chi2": rec_chi2,
                "chi2_within_1e-9_relative": chi2_ok,
                "recomputed_v": v, "recorded_v": rec_v,
                "v_within_1e-9_absolute": v_ok,
                "verdict": "PASS" if ok else "FAIL",
            })
            full[key] = {
                "table": table, "by_site": by_site,
                "n": n_analysis, "chi2": chi2, "v": v,
            }
        gates["0.2"] = {
            "gate": "0.2",
            "name": "Population reproduction, both layers",
            "layers": repro,
            "verdict": "PASS" if gate02_pass else "FAIL",
        }
        if not gate02_pass:
            terminal = ("INVALID", "0.2")

    if terminal is None:
        # ── Gate 0.3 — estimator regression ─────────────
        # One fresh stream, F2 first then F3, exactly as the
        # Phase-384 v2 script runs them.
        rng = np.random.default_rng(p384.SEED)
        reg = []
        gate03_pass = True
        for key in ("F2_holdat", "F3_icit_lineage"):
            entry = full[key]
            boots = p384.bootstrap_within_site(
                entry["table"], entry["by_site"], rng)
            iv = p384.intervals(boots, entry["v"])
            rec = recorded384["members"][key]
            fields = {
                "basic_ci95": iv["basic_ci95"] == rec["basic_ci95"],
                "percentile_ci95":
                    iv["percentile_ci95"] == rec["percentile_ci95"],
                "bootstrap_median":
                    iv["bootstrap_median"] == rec["bootstrap_median"],
            }
            ok = all(fields.values())
            gate03_pass = gate03_pass and ok
            reg.append({
                "layer": key, "exact_match_fields": fields,
                "recomputed": iv,
                "recorded": {
                    "basic_ci95": rec["basic_ci95"],
                    "percentile_ci95": rec["percentile_ci95"],
                    "bootstrap_median": rec["bootstrap_median"],
                },
                "verdict": "PASS" if ok else "FAIL",
            })
            entry["intervals"] = iv
            entry["boots_median"] = iv["bootstrap_median"]
        gates["0.3"] = {
            "gate": "0.3", "name": "Estimator regression",
            "parameters": {
                "B_bootstrap": p384.B_BOOT, "seed": p384.SEED,
                "governing_interval": "basic bootstrap",
                "rng_stream": ("one numpy default_rng(20261012) "
                               "stream, F2 first then F3, as in "
                               "the Phase-384 v2 script"),
            },
            "layers": reg,
            "verdict": "PASS" if gate03_pass else "FAIL",
        }
        if not gate03_pass:
            terminal = ("INVALID", "0.3")

    census = None
    arm1 = None
    arm2 = None
    if terminal is None:
        # ── Gate 0.4 — shared-population census ─────────
        h_eligible, h_analysis = _analysis_population(p137, holdat_insc)
        i_eligible, i_analysis = _analysis_population(p137, horus_insc)
        shared_sites = sorted(set(h_eligible) & set(i_eligible))
        h_shared = [i for i in h_analysis if i["site"] in set(shared_sites)]
        i_shared = [
            i for i in i_analysis
            if i["site"] in set(shared_sites)
            and i["type_class"] == "SEAL"
        ]
        h_per_site = Counter(i["site"] for i in h_shared)
        i_per_site = Counter(i["site"] for i in i_shared)
        thin = (len(shared_sites) < 5 or len(h_shared) < 500
                or len(i_shared) < 500)
        census = {
            "shared_sites": shared_sites,
            "n_shared_sites": len(shared_sites),
            "holdat_inscriptions": len(h_shared),
            "icit_inscriptions_seal": len(i_shared),
            "per_site": {
                site: {
                    "holdat": h_per_site.get(site, 0),
                    "icit_seal": i_per_site.get(site, 0),
                } for site in shared_sites
            },
            "construction": (
                "each layer's Phase-137 analysis population, "
                "restricted to the sites present in both "
                "layers' analysis populations; object type "
                "SEAL (DD-060-12): Holdat enters whole (no "
                "object-type field; type a constant), ICIT "
                "restricted to its recorded SEAL type class"),
            "floors": {"min_sites": 5, "min_inscriptions_per_layer": 500},
            "verdict": "TOO THIN" if thin else "PASS",
        }
        gates["0.4"] = {
            "gate": "0.4",
            "name": "Shared-population census (arm 2's gate)",
            "census": census,
            "verdict": "TOO THIN (arm 2 only)" if thin else "PASS",
        }

        # ── Arm 1 — the margin curve (always reports) ───
        f2_iv = full["F2_holdat"]["intervals"]
        lo, hi = f2_iv["basic_ci95"]
        cells = [
            {"margin": m, "margin_label": MARGIN_LABELS[m],
             "cell_word": _cell_word(m, lo, hi)}
            for m in MARGIN_GRID
        ]
        arm1 = {
            "label": "sensitivity",
            "governing_basic_ci95": [lo, hi],
            "percentile_ci95": f2_iv["percentile_ci95"],
            "bootstrap_median": f2_iv["bootstrap_median"],
            "point_v": full["F2_holdat"]["v"],
            "n_analysis_inscriptions": full["F2_holdat"]["n"],
            "margin_grid": MARGIN_GRID,
            "cells": cells,
        }

        # ── Arm 2 — shared population (if its gate passed) ──
        if thin:
            arm2 = {
                "outcome": "TOO THIN",
                "census": census,
                "period_mix": {
                    "holdat": PERIOD_STATEMENT,
                    "icit_lineage": PERIOD_STATEMENT,
                },
            }
        else:
            rng2 = np.random.default_rng(p384.SEED)
            per_layer = {}
            for key, label, shared_insc in (
                ("holdat", "Holdat compilation layer", h_shared),
                ("icit_lineage", "ICIT-lineage layer (horus84)",
                 i_shared),
            ):
                table, by_site, n_est = p384.build_population(
                    p137, shared_insc)
                chi2, v = p384._chi2_v(table)
                boots = p384.bootstrap_within_site(table, by_site, rng2)
                iv = p384.intervals(boots, v)
                per_layer[key] = {
                    "label": label,
                    "n_census_inscriptions": len(shared_insc),
                    "n_estimator_inscriptions": n_est,
                    "table_dimensions": list(table.shape),
                    "table_sites": None,  # filled below
                    "chi2": chi2, "point_v": v,
                    "governing_basic_ci95": iv["basic_ci95"],
                    "percentile_ci95": iv["percentile_ci95"],
                    "bootstrap_median": iv["bootstrap_median"],
                }
            # Sites carried by each estimator population, in
            # the builder's eligible order (rows of the table).
            for key, shared_insc in (("holdat", h_shared),
                                     ("icit_lineage", i_shared)):
                elig, _ana = _analysis_population(p137, shared_insc)
                per_layer[key]["table_sites"] = elig
            h_lo, h_hi = per_layer["holdat"]["governing_basic_ci95"]
            i_lo, i_hi = per_layer["icit_lineage"]["governing_basic_ci95"]
            overlap = (h_lo <= i_hi) and (i_lo <= h_hi)
            arm2 = {
                "outcome": ("COMPOSITION EXPLAINS THE GAP" if overlap
                            else "COMPOSITION DOES NOT"),
                "intervals_overlap": overlap,
                "census": census,
                "per_layer": per_layer,
                "period_mix": {
                    "holdat": PERIOD_STATEMENT,
                    "icit_lineage": PERIOD_STATEMENT,
                },
                "rng_stream": ("fresh numpy default_rng(20261012) "
                               "stream for arm 2, Holdat first "
                               "then ICIT, mirroring the Phase-384 "
                               "v2 script's layer order"),
                "sign_treatment": (
                    "each layer computed inside its own sign "
                    "numbering; signs never pooled, mapped, or "
                    "harmonised (F060-C14); the only cross-layer "
                    "operation is the comparison of the two "
                    "governing intervals"),
            }

    anchors_after = _sha256(
        _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
    anchors_identical = anchors_before == anchors_after == ANCHORS_SHA256

    if terminal is not None:
        outcome_word = "INVALID"
        stopped_gate = terminal[1]
    elif arm2 is not None:
        outcome_word = arm2["outcome"]
        stopped_gate = None
    else:
        outcome_word = None
        stopped_gate = None

    results = {
        "phase": "Phase-422",
        "spec": "060",
        "design": "D-23",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": OSF_REGISTRATION,
        "claim_under_test": "STUDY-SPEC-024/F2-HOLDAT",
        "execution_date": EXECUTION_DATE,
        "parameters": {
            "B_bootstrap": 9999, "seed": 20261012,
            "governing_interval": "basic bootstrap",
            "margin_grid": MARGIN_GRID,
            "estimator": ("Phase-384 v2 estimator, unchanged, "
                          "imported from "
                          "backend/scripts/phase384_stage2_margins_v2.py"),
        },
        "corpus_labels": {
            "holdat": ("Holdat compilation layer (held file "
                       "indus_corpus 2.csv, holdatllc_indus export; "
                       "SHA-256 " + HOLDAT_LAYER_SHA256 + ")"),
            "icit_lineage": ("ICIT-lineage layer (horus84) (held "
                             "file inscriptions.csv; SHA-256 "
                             + ICIT_LAYER_SHA256 + ")"),
        },
        "gates": gates,
        "arm1_margin_curve": arm1,
        "arm2_shared_population": arm2,
        "terminal_outcome": outcome_word,
        "stopped_at_gate": stopped_gate,
        "period_mix": {
            "holdat": PERIOD_STATEMENT,
            "icit_lineage": PERIOD_STATEMENT,
        },
        "no_verdict_moves_sentence": NO_VERDICT_MOVES,
        "anchors_sha256_before": anchors_before,
        "anchors_sha256_after": anchors_after,
        "anchors_byte_identical": anchors_identical,
        "ai_disclosure": AI_DISCLOSURE,
    }
    _OUT_RESULTS.write_text(json.dumps(results, indent=1), "utf-8")

    # ── Report (spec section 8 headline rules) ──────────
    lines = []
    lines.append("# Phase-422 Report — Spec 060 (D-23): the Holdat "
                 "site effect, margin curve and shared population")
    lines.append("")
    lines.append(f"Execution date: {EXECUTION_DATE}. Frozen contract: "
                 f"specs/060-f2-margin-curve/freeze.md (digest "
                 f"{FREEZE_DIGEST}); OSF registration {OSF_REGISTRATION} "
                 "(approved and public).")
    lines.append("")
    lines.append("Corpus labels: the Holdat compilation layer "
                 f"(SHA-256 {HOLDAT_LAYER_SHA256}) and the ICIT-lineage "
                 f"layer (horus84) (SHA-256 {ICIT_LAYER_SHA256}).")
    lines.append("")
    lines.append("## Step 0 — the gates, in order")
    lines.append("")
    for gk in ("0.1", "0.2", "0.3", "0.4"):
        if gk in gates:
            g = gates[gk]
            lines.append(f"- Gate {gk} ({g['name']}): {g['verdict']}")
    lines.append("")
    if terminal is not None:
        lines.append("## Outcome — INVALID")
        lines.append("")
        lines.append(
            f"Execution stopped at step 0, gate {stopped_gate}: "
            "see the gate record in reports/phase422_results.json "
            "for the observed values. No arm quantity was "
            "computed. Spec 024's F2 and F3 records stand exactly "
            "as recorded.")
        lines.append("")
    else:
        lo, hi = arm1["governing_basic_ci95"]
        lines.append("## Arm 1 — the margin curve (sensitivity display)")
        lines.append("")
        cell_txt = " ".join(
            f"At margin {c['margin_label']}: {c['cell_word']}."
            for c in arm1["cells"])
        lines.append(
            "Margin curve for STUDY-SPEC-024/F2-HOLDAT "
            "(sensitivity display — the recorded verdict at the "
            "declared margin 0.10 stands, CONTRADICTED, and is "
            "not moved by this curve): governing basic-bootstrap "
            f"interval [{lo}, {hi}], point V {arm1['point_v']}, "
            "on the Holdat layer's 1,670-inscription analysis "
            "population, recomputed under the Phase-384 v2 "
            f"estimator. {cell_txt}")
        lines.append("")
        lines.append("## Arm 2 — the shared population")
        lines.append("")
        c = census
        sites_txt = ", ".join(c["shared_sites"])
        if arm2["outcome"] == "TOO THIN":
            lines.append(
                "The shared population cannot carry arm 2 as "
                f"designed: it retains {c['n_shared_sites']} sites "
                f"and {c['holdat_inscriptions']} Holdat / "
                f"{c['icit_inscriptions_seal']} ICIT inscriptions, "
                "against the frozen floors of 5 sites and 500 "
                "inscriptions in either layer. No shared-population "
                "quantity was computed. Arm 1's margin curve stands "
                "as this spec's product, and the settled F2 and F3 "
                "verdicts stand exactly as recorded.")
        else:
            ph = arm2["per_layer"]["holdat"]
            pi = arm2["per_layer"]["icit_lineage"]
            lines.append(
                f"Shared sites ({c['n_shared_sites']}): {sites_txt}. "
                f"Per-site counts (Holdat / ICIT SEAL): "
                + "; ".join(
                    f"{s} {v['holdat']} / {v['icit_seal']}"
                    for s, v in c["per_site"].items()) + ".")
            lines.append("")
            lines.append(
                f"Holdat governing interval {ph['governing_basic_ci95']}, "
                f"point V {ph['point_v']}, on {ph['n_estimator_inscriptions']} "
                "inscriptions. ICIT governing interval "
                f"{pi['governing_basic_ci95']}, point V {pi['point_v']}, "
                f"on {pi['n_estimator_inscriptions']} inscriptions.")
            lines.append("")
            lines.append(f"Outcome: {arm2['outcome']}.")
            lines.append("")
        lines.append(f"Period mix, Holdat layer: {PERIOD_STATEMENT}.")
        lines.append(f"Period mix, ICIT-lineage layer: {PERIOD_STATEMENT}.")
        lines.append("")
    lines.append(NO_VERDICT_MOVES)
    lines.append("")
    lines.append(f"Anchors asserted byte-identical before and after: "
                 f"{anchors_identical} ({anchors_after}).")
    lines.append("")
    lines.append(f"*AI disclosure: {AI_DISCLOSURE}*")
    lines.append("")
    _OUT_REPORT.write_text("\n".join(lines), "utf-8")

    print("gates:", {k: v["verdict"] for k, v in gates.items()})
    print("terminal outcome:", outcome_word)
    print("wrote", _OUT_RESULTS)
    print("wrote", _OUT_REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
