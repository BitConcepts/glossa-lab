#!/usr/bin/env python3
"""Phase-137 (spec 024, FROZEN Stage 2(c)) — site repertoire
differentiation, family members F2 (Holdat layer) and F3
(ICIT-lineage layer), executed exactly as frozen in
``specs/024-evidence-integration/stage2c-freeze.md``.

Design (the freeze governs; summary only):

- Each layer is tested SEPARATELY, on its own native sign list,
  and is never pooled with the other.
- Unit: the inscription. Profile table: site x sign token counts
  over the layer's analysis population. Sign columns: signs whose
  layer-wide token count within the analysis population is >= 10;
  rarer signs pool into a single ``OTHER`` column. Placeholder /
  identity-less tokens are excluded from profiles entirely
  (ICIT-lineage codes ``000`` / ``999``; Holdat has none).
- Statistic: Pearson chi-square of the profile table, used as a
  divergence statistic only; all inference is by permutation.
- Composition control: site labels are shuffled at inscription
  level WITHIN composition strata only (Fisher-Yates via
  ``random.Random(20261009)``), B = 9,999,
  p = (1 + #{chi2_perm >= chi2_obs}) / (1 + B).
- Site inclusion (uniform): >= 30 inscriptions AND >= 100 tokens
  in the layer's parsed population.
- Estimability (freeze section 3, a stated substitution for the
  spec section 5.1 asymptotic default): a layer executes iff
  >= 2 eligible sites AND >= 2 sign columns after the collapse;
  the sparsity disclosure (share of cells with expected < 5,
  minimum expected count, per-site token counts) is mandatory.
- Effects (descriptive): Cramer's V; observed statistic vs the
  permutation median / 95th percentile; per-site total-variation
  distance to the pooled profile (all sites).

Text substrate (freeze section 0): the layers' sign sequences
are used only as the inscriptions themselves. Context variables
come from Class O fields only (``site`` in both layers; ``type``
in the ICIT-lineage layer). Class I interpretive fields enter
NOTHING: Holdat ``letter_label_encoded``, ``FormWithoutLemma``,
``MorphemeSeparated``, ``morpheme boundary``, ``noun``, ``verb``,
``prefix``, ``prefix_label_encoded``, ``vowel``, ``upos``,
``xpos``; ICIT-lineage ``class``, ``sanskrit``, ``translation``,
``notes``. This script reads only ``letters`` / ``position`` /
``seal_id`` / ``site`` (Holdat) and ``text`` / ``site`` /
``type`` (ICIT-lineage).

F2 Holdat: population all inscriptions (token rows grouped by
``seal_id``, ordered by int(``position``)); sign = ``letters``
M-code; values in the source file are single-quoted in the
compilation's exports as acquired by prior loaders, so values
are stripped of surrounding single quotes exactly as prior
Holdat loaders do (the file in hand carries no quotes; the
strip is a no-op there and is recorded as such in the flow).
Strata = length class {2-3, 4-5, 6-8} ONLY: the layer carries
no object-type field, so the type control degenerates (stated
in the freeze; not patched).

F3 ICIT-lineage: parse ``re.findall(r"\\d{3}", text)``;
placeholders ``000`` / ``999`` excluded from profiles. Strata =
type class x length class; type class = ``type`` prefix before
':' in {SEAL, TAB, POT, OTHER}, OTHER pooling {TAG, MISC,
BNGL, ROD, IMPL, BEAD, MDLN, Unknown}; length class {1, 2-3,
4-5, 6+} parsed tokens. The ICIT-lineage label is mandatory in
every headline for this layer.

Performance (H9/H11): per-inscription sign-count vectors are
precomputed sparsely over the frozen column set; permutations
accumulate a dense table from those vectors. The permutation
loop carries an explicit deadline and progress prints.

Inputs live in the local store (never committed). Outputs
(committed): ``reports/phase137_results.json``. Deterministic:
fixed seed, stable ordering everywhere, no wall-clock in the
output JSON.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
SWEEP = (Path.home() / "workspace" / "research_notes"
         / "indus-data-deep-sweep-20261008" / "downloads")

DEFAULT_HOLDAT = (MAIN_CHECKOUT / "corpora/downloads"
                  / "external_repos/holdatllc_indus"
                  / "indus_corpus 2.csv")
DEFAULT_HORUS = (SWEEP / "horus84-computational-linguistics"
                 / "data" / "inscriptions.csv")
DEFAULT_OUT = REPO_ROOT / "reports" / "phase137_results.json"
ANCHORS = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)

SEED = 20261009
B_PERMUTATIONS = 9999
MIN_SIGN_COUNT = 10
MIN_SITE_INSCRIPTIONS = 30
MIN_SITE_TOKENS = 100
PLACEHOLDERS = {"000", "999"}
OTHER = "OTHER"

AI_DISCLOSURE = (
    "Produced by an AI agent (Muse Spark, via Muse) at "
    "the direction of Tristen Pierson, per constitution "
    "section VI."
)


# ---------------------------------------------------------------------------
# Pure helpers (unit-tested)
# ---------------------------------------------------------------------------

def clean_value(value: str) -> str:
    """Strip whitespace and surrounding single quotes, as prior
    Holdat loaders do for this compilation's exports."""
    v = (value or "").strip()
    if len(v) >= 2 and v.startswith("'") and v.endswith("'"):
        v = v[1:-1].strip()
    return v


def site_eligible(n_inscriptions: int, n_tokens: int) -> bool:
    """Freeze section 2 site inclusion rule (uniform)."""
    return (n_inscriptions >= MIN_SITE_INSCRIPTIONS
            and n_tokens >= MIN_SITE_TOKENS)


def holdat_length_class(n_tokens: int) -> str:
    if n_tokens <= 3:
        return "2-3"
    if n_tokens <= 5:
        return "4-5"
    return "6-8"


def horus_length_class(n_parsed_tokens: int) -> str:
    if n_parsed_tokens <= 1:
        return "1"
    if n_parsed_tokens <= 3:
        return "2-3"
    if n_parsed_tokens <= 5:
        return "4-5"
    return "6+"


def horus_type_class(type_value: str) -> str:
    prefix = (type_value or "").split(":")[0]
    if prefix in ("SEAL", "TAB", "POT"):
        return prefix
    return "OTHER"


def chi_square(table: list[list[float]]) -> float:
    """Pearson chi-square of a contingency table (divergence
    statistic only; no asymptotic inference anywhere)."""
    n_rows = len(table)
    n_cols = len(table[0]) if n_rows else 0
    row_totals = [sum(row) for row in table]
    col_totals = [sum(table[r][c] for r in range(n_rows))
                  for c in range(n_cols)]
    total = sum(row_totals)
    if total == 0:
        return 0.0
    stat = 0.0
    for r in range(n_rows):
        for c in range(n_cols):
            expected = row_totals[r] * col_totals[c] / total
            if expected > 0:
                diff = table[r][c] - expected
                stat += diff * diff / expected
    return stat


def cramers_v(table: list[list[float]], stat: float) -> float:
    n_rows = len(table)
    n_cols = len(table[0]) if n_rows else 0
    total = sum(sum(row) for row in table)
    k = min(n_rows - 1, n_cols - 1)
    if total == 0 or k <= 0:
        return 0.0
    return math.sqrt(stat / (total * k))


def tv_distances(table: list[list[float]]) -> list[float]:
    """Per-row total-variation distance to the pooled profile."""
    n_rows = len(table)
    n_cols = len(table[0]) if n_rows else 0
    col_totals = [sum(table[r][c] for r in range(n_rows))
                  for c in range(n_cols)]
    total = sum(col_totals)
    pooled = [ct / total if total else 0.0 for ct in col_totals]
    out = []
    for r in range(n_rows):
        row_total = sum(table[r])
        dist = 0.0
        for c in range(n_cols):
            p = table[r][c] / row_total if row_total else 0.0
            dist += abs(p - pooled[c])
        out.append(0.5 * dist)
    return out


def sparsity_disclosure(table: list[list[float]]) -> dict:
    n_rows = len(table)
    n_cols = len(table[0]) if n_rows else 0
    row_totals = [sum(row) for row in table]
    col_totals = [sum(table[r][c] for r in range(n_rows))
                  for c in range(n_cols)]
    total = sum(row_totals)
    cells = 0
    lt5 = 0
    min_expected = None
    for r in range(n_rows):
        for c in range(n_cols):
            if total == 0:
                continue
            expected = row_totals[r] * col_totals[c] / total
            cells += 1
            if expected < 5:
                lt5 += 1
            if min_expected is None or expected < min_expected:
                min_expected = expected
    return {
        "cells_total": cells,
        "cells_expected_lt5": lt5,
        "share_cells_expected_lt5": (lt5 / cells) if cells else 0.0,
        "min_expected_count": min_expected,
        "per_site_tokens": row_totals,
    }


def run_permutation(inscriptions, n_sites, n_cols, observed,
                    b=B_PERMUTATIONS, seed=SEED,
                    deadline_s=3300, label="layer"):
    """Permutation null: site labels shuffled at inscription
    level within composition strata only.

    ``inscriptions``: list of (site_idx, stratum_key,
    sparse_vector) where sparse_vector is a tuple of
    (col_idx, count) pairs over the frozen column set.
    Returns (sorted_stats, count_ge_observed).
    """
    rng = random.Random(seed)
    strata: dict[str, list[int]] = defaultdict(list)
    for idx, (_site, stratum, _vec) in enumerate(inscriptions):
        strata[stratum].append(idx)
    stratum_keys = sorted(strata)
    stratum_members = [strata[k] for k in stratum_keys]
    stratum_labels = [[inscriptions[i][0] for i in members]
                      for members in stratum_members]

    stats = []
    count_ge = 0
    start = time.monotonic()
    deadline = start + deadline_s
    for perm in range(1, b + 1):
        table = [[0] * n_cols for _ in range(n_sites)]
        for members, labels in zip(stratum_members, stratum_labels):
            shuffled = list(labels)
            rng.shuffle(shuffled)
            for idx, site_idx in zip(members, shuffled):
                for col_idx, count in inscriptions[idx][2]:
                    table[site_idx][col_idx] += count
        stat = chi_square(table)
        stats.append(stat)
        if stat >= observed:
            count_ge += 1
        if perm % 500 == 0:
            elapsed = time.monotonic() - start
            print(f"  [{label}] permutation {perm}/{b} "
                  f"({elapsed:.1f}s elapsed)", flush=True)
            if time.monotonic() > deadline:
                raise TimeoutError(
                    f"[{label}] permutation deadline "
                    f"({deadline_s}s) exceeded at permutation "
                    f"{perm}/{b}")
    stats.sort()
    return stats, count_ge


def permutation_summary(stats_sorted, count_ge, b=B_PERMUTATIONS):
    median = stats_sorted[b // 2]
    p95_idx = math.ceil(0.95 * b) - 1  # nearest-rank
    p95 = stats_sorted[p95_idx]
    p_value = (1 + count_ge) / (1 + b)
    return {
        "B": b,
        "seed": SEED,
        "p_formula": "(1 + #{chi2_perm >= chi2_obs}) / (1 + B)",
        "count_perm_ge_observed": count_ge,
        "permutation_median": median,
        "permutation_p95_nearest_rank": p95,
        "p_value_raw": p_value,
    }


# ---------------------------------------------------------------------------
# Layer loaders — each returns a list of inscription records:
# {site, stratum, tokens (profile tokens, placeholders removed)}
# plus a population-flow dict.
# ---------------------------------------------------------------------------

def load_holdat(path: Path):
    rows = []
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            rows.append({
                "letters": clean_value(raw["letters"]),
                "position": int(clean_value(raw["position"])),
                "seal_id": clean_value(raw["seal_id"]),
                "site": clean_value(raw["site"]),
            })
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["seal_id"]].append(row)
    inscriptions = []
    site_mismatch_seals = 0
    for seal_id in sorted(grouped, key=lambda s: int(s)):
        members = sorted(grouped[seal_id],
                         key=lambda r: r["position"])
        sites = {r["site"] for r in members}
        if len(sites) > 1:
            site_mismatch_seals += 1
        tokens = [r["letters"] for r in members]
        inscriptions.append({
            "site": members[0]["site"],
            "stratum": holdat_length_class(len(tokens)),
            "tokens": tokens,
            "n_parsed_tokens": len(tokens),
        })
    flow = {
        "token_rows_read": len(rows),
        "inscriptions_parsed": len(inscriptions),
        "placeholder_tokens_excluded": 0,
        "seals_with_multiple_sites": site_mismatch_seals,
        "distinct_signs_native_full_layer":
            len({r["letters"] for r in rows}),
        "inscription_length_min":
            min(len(i["tokens"]) for i in inscriptions),
        "inscription_length_max":
            max(len(i["tokens"]) for i in inscriptions),
    }
    return inscriptions, flow


def load_horus(path: Path):
    rows = []
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            rows.append({
                "site": (raw["site"] or "").strip(),
                "type": (raw["type"] or "").strip(),
                "text": raw["text"] or "",
            })
    inscriptions = []
    n_parsed_tokens_total = 0
    n_placeholder_tokens_total = 0
    distinct_nonplaceholder = set()
    for row in rows:
        parsed = re.findall(r"\d{3}", row["text"])
        profile = [c for c in parsed if c not in PLACEHOLDERS]
        n_parsed_tokens_total += len(parsed)
        n_placeholder_tokens_total += len(parsed) - len(profile)
        distinct_nonplaceholder.update(profile)
        inscriptions.append({
            "site": row["site"],
            "stratum": (f"{horus_type_class(row['type'])}|"
                        f"{horus_length_class(len(parsed))}"),
            "tokens": profile,
            "n_parsed_tokens": len(parsed),
            "type_class": horus_type_class(row["type"]),
            "length_class": horus_length_class(len(parsed)),
        })
    flow = {
        "rows_read": len(rows),
        "rows_with_ge1_parsed_token":
            sum(1 for i in inscriptions if i["n_parsed_tokens"] >= 1),
        "parsed_tokens_full_layer": n_parsed_tokens_total,
        "placeholder_tokens_excluded_full_layer":
            n_placeholder_tokens_total,
        "nonplaceholder_tokens_full_layer":
            n_parsed_tokens_total - n_placeholder_tokens_total,
        "distinct_signs_nonplaceholder_full_layer":
            len(distinct_nonplaceholder),
    }
    return inscriptions, flow


# ---------------------------------------------------------------------------
# Layer analysis — the common frozen design
# ---------------------------------------------------------------------------

def analyse_layer(inscriptions, *, family_member, headline_label,
                  layer_name, strata_definition, deadline_s,
                  progress_label):
    # Per-site population counts in the parsed population.
    per_site_insc: Counter = Counter()
    per_site_parsed: Counter = Counter()
    per_site_profile: Counter = Counter()
    for insc in inscriptions:
        per_site_insc[insc["site"]] += 1
        per_site_parsed[insc["site"]] += insc["n_parsed_tokens"]
        per_site_profile[insc["site"]] += len(insc["tokens"])

    sites_all = []
    eligible_sites = []
    excluded_sites = []
    for site in sorted(per_site_insc):
        eligible = site_eligible(per_site_insc[site],
                                 per_site_parsed[site])
        record = {
            "site": site,
            "inscriptions": per_site_insc[site],
            "parsed_tokens": per_site_parsed[site],
            "profile_tokens_nonplaceholder": per_site_profile[site],
            "eligible": eligible,
        }
        sites_all.append(record)
        if eligible:
            eligible_sites.append(site)
        else:
            excluded_sites.append(record)

    analysis = [i for i in inscriptions
                if i["site"] in set(eligible_sites)
                and i["n_parsed_tokens"] >= 1]
    analysis_tokens = sum(len(i["tokens"]) for i in analysis)

    # Frozen column set: layer-wide count >= 10 within the
    # analysis population; rarer signs pool into OTHER.
    sign_counts: Counter = Counter()
    for insc in analysis:
        sign_counts.update(insc["tokens"])
    kept_signs = sorted(s for s, c in sign_counts.items()
                        if c >= MIN_SIGN_COUNT)
    other_tokens = sum(c for s, c in sign_counts.items()
                       if c < MIN_SIGN_COUNT)
    columns = kept_signs + ([OTHER] if other_tokens else [])
    col_index = {s: j for j, s in enumerate(kept_signs)}
    other_idx = len(kept_signs) if other_tokens else None

    site_index = {s: j for j, s in enumerate(eligible_sites)}
    table = [[0] * len(columns) for _ in eligible_sites]
    sparse_inscriptions = []
    for insc in analysis:
        vec: Counter = Counter()
        for tok in insc["tokens"]:
            if tok in col_index:
                vec[col_index[tok]] += 1
            else:
                vec[other_idx] += 1
        for col_idx, count in vec.items():
            table[site_index[insc["site"]]][col_idx] += count
        sparse_inscriptions.append((
            site_index[insc["site"]], insc["stratum"],
            tuple(sorted(vec.items()))))

    strata_counts = dict(sorted(
        Counter(i["stratum"] for i in analysis).items()))

    result = {
        "family_member": family_member,
        "headline_label": headline_label,
        "layer": layer_name,
        "sites_all": sites_all,
        "eligible_sites": eligible_sites,
        "excluded_sites": excluded_sites,
        "analysis_population": {
            "inscriptions": len(analysis),
            "profile_tokens": analysis_tokens,
            "parsed_tokens": sum(i["n_parsed_tokens"]
                                 for i in analysis),
        },
        "strata_definition": strata_definition,
        "strata_counts": strata_counts,
        "sign_space": {
            "distinct_signs_in_analysis_population":
                len(sign_counts),
            "min_sign_count_for_column": MIN_SIGN_COUNT,
            "n_sign_columns_kept": len(kept_signs),
            "other_column_present": other_tokens > 0,
            "other_tokens": other_tokens,
            "other_share_of_profile_tokens":
                (other_tokens / analysis_tokens)
                if analysis_tokens else 0.0,
            "columns": columns,
        },
        "profile_table": {
            "sites": eligible_sites,
            "columns": columns,
            "counts": table,
            "row_totals": [sum(r) for r in table],
            "column_totals": [sum(table[r][c]
                                  for r in range(len(table)))
                              for c in range(len(columns))],
            "grand_total": sum(sum(r) for r in table),
        },
        "table_dimensions": [len(eligible_sites), len(columns)],
    }

    estimable = (len(eligible_sites) >= 2 and len(columns) >= 2)
    result["estimable"] = estimable
    if not estimable:
        result["estimability_outcome"] = (
            "NOT ESTIMABLE (freeze section 3): fewer than 2 "
            "eligible sites or fewer than 2 sign columns; "
            "counts shown, no p-value.")
        result["observed_chi_square"] = None
        result["permutation"] = None
        result["p_value_raw"] = None
        return result

    observed = chi_square(table)
    result["observed_chi_square"] = observed
    result["cramers_v_descriptive"] = cramers_v(table, observed)
    result["per_site_tv_distance_descriptive"] = {
        site: dist for site, dist
        in zip(eligible_sites, tv_distances(table))}
    result["sparsity_disclosure"] = sparsity_disclosure(table)
    result["estimability_outcome"] = (
        "ESTIMABLE AND EXECUTED (freeze section 3): >= 2 "
        "eligible sites and >= 2 sign columns; sparsity "
        "disclosed below as mandated.")

    print(f"[{progress_label}] observed chi-square = "
          f"{observed:.4f}; running {B_PERMUTATIONS} "
          f"permutations (seed {SEED}) ...", flush=True)
    stats_sorted, count_ge = run_permutation(
        sparse_inscriptions, len(eligible_sites), len(columns),
        observed, deadline_s=deadline_s, label=progress_label)
    result["permutation"] = permutation_summary(
        stats_sorted, count_ge)
    result["p_value_raw"] = result["permutation"]["p_value_raw"]
    return result


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(holdat_path: Path, horus_path: Path,
          deadline_s: int) -> dict:
    anchors_digest = sha256_of(ANCHORS)
    assert anchors_digest == ANCHORS_SHA256, (
        f"anchors changed: {anchors_digest} != {ANCHORS_SHA256}")

    print("Loading Holdat layer (F2) ...", flush=True)
    holdat_inscriptions, holdat_flow = load_holdat(holdat_path)
    print("Loading ICIT-lineage layer (F3) ...", flush=True)
    horus_inscriptions, horus_flow = load_horus(horus_path)

    f2 = analyse_layer(
        holdat_inscriptions,
        family_member="F2",
        headline_label="Holdat compilation layer",
        layer_name="holdat_indus_corpus",
        strata_definition=(
            "inscription length class only: {2-3, 4-5, 6-8} "
            "tokens. Object-type control degenerates: the "
            "layer carries no object-type field and its "
            "inscriptions are seal texts, so the type mix is "
            "a constant (freeze section 4) — stated, not "
            "patched."),
        deadline_s=deadline_s,
        progress_label="F2 Holdat")
    f2["population_flow"] = holdat_flow
    f2["input"] = {
        "path": str(holdat_path), "sha256": sha256_of(holdat_path)}

    f3 = analyse_layer(
        horus_inscriptions,
        family_member="F3",
        headline_label="ICIT-lineage layer (horus84)",
        layer_name="horus84_inscriptions",
        strata_definition=(
            "object-type class x length class. Type class = "
            "type prefix before ':' in {SEAL, TAB, POT, "
            "OTHER}, OTHER pooling {TAG, MISC, BNGL, ROD, "
            "IMPL, BEAD, MDLN, Unknown}; length class {1, "
            "2-3, 4-5, 6+} parsed tokens (freeze section 5)."),
        deadline_s=deadline_s,
        progress_label="F3 ICIT-lineage")
    f3["population_flow"] = horus_flow
    f3["input"] = {
        "path": str(horus_path), "sha256": sha256_of(horus_path)}

    return {
        "phase": "Phase-137",
        "spec": "024",
        "test": ("Stage 2(c) — site repertoire "
                 "differentiation (freeze: "
                 "specs/024-evidence-integration/"
                 "stage2c-freeze.md)"),
        "family": {
            "F2": "Site repertoire differentiation — "
                  "Holdat compilation layer",
            "F3": "Site repertoire differentiation — "
                  "ICIT-lineage layer (horus84)",
            "correction": (
                "Benjamini-Hochberg at q = 0.05 across the "
                "family, applied once in the combined Stage "
                "2 report; raw p-values only here, verdict "
                "words deferred to that report."),
        },
        "parameters": {
            "B_permutations": B_PERMUTATIONS,
            "seed": SEED,
            "rng": "random.Random(20261009), Fisher-Yates "
                   "shuffles of site labels within strata",
            "min_sign_count_for_column": MIN_SIGN_COUNT,
            "site_inclusion": {
                "min_inscriptions": MIN_SITE_INSCRIPTIONS,
                "min_tokens": MIN_SITE_TOKENS},
            "statistic": "Pearson chi-square of the site x "
                         "sign profile table (divergence "
                         "statistic only; permutation "
                         "inference only)",
        },
        "fields_used": {
            "holdat": ["letters", "position", "seal_id",
                       "site"],
            "horus84": ["text", "site", "type"],
            "class_i_fields_entering_nothing": {
                "holdat": ["letter_label_encoded",
                           "FormWithoutLemma",
                           "MorphemeSeparated",
                           "morpheme boundary", "noun", "verb",
                           "prefix", "prefix_label_encoded",
                           "vowel", "upos", "xpos"],
                "horus84": ["class", "sanskrit",
                            "translation", "notes"]},
        },
        "uncontrolled_confounders_statement": (
            "Composition strata as frozen capture the "
            "confounders spec section 5.1 names (type mix, "
            "length mix); other confounders (period, "
            "preservation, excavation history) are not "
            "available in these layers and are NOT "
            "controlled (freeze section 6, B2)."),
        "anchors_sha256": anchors_digest,
        "ai_disclosure": AI_DISCLOSURE,
        "layers": {"F2_holdat": f2, "F3_icit_lineage": f3},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--holdat", type=Path,
                    default=DEFAULT_HOLDAT)
    ap.add_argument("--horus", type=Path, default=DEFAULT_HORUS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--deadline-s", type=int, default=3300,
                    help="per-layer permutation deadline "
                         "(H9/H11)")
    args = ap.parse_args(argv)

    for p in (args.holdat, args.horus):
        if not p.exists():
            print(f"ERROR: input not found: {p}",
                  file=sys.stderr)
            return 2

    results = build(args.holdat, args.horus, args.deadline_s)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(results, indent=1, ensure_ascii=False)
        + "\n", "utf-8")
    for key, layer in results["layers"].items():
        perm = layer.get("permutation") or {}
        print(f"{key}: sites={len(layer['eligible_sites'])} "
              f"table={layer['table_dimensions']} "
              f"chi2={layer['observed_chi_square']} "
              f"p_raw={layer['p_value_raw']} "
              f"perm_median={perm.get('permutation_median')} "
              f"perm_p95="
              f"{perm.get('permutation_p95_nearest_rank')}")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
