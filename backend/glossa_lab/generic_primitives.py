"""Generic graph-node machinery (Spec 087 S3, families F3 + F8,
F4 + F5, F7 + F6, and F9).

Twenty-six spec/parameter-driven engines back the generic
primitives registered in experiment_graph.py: RegistryTableLoader,
LabelMapApplier, TemplateMiner, ClusterContingencyProfile,
SignRoleClassifier, ValueRoleMapSource, AnchorSyllabifier,
AssociationAnchorDeriver, and PMICentralityRanker (PR-B), plus
IconographicAnchorScorer, PhonemeMapCoverage,
PhonemeMapPermutationTest, LengthMatchScorer,
LengthMatchPermutationTest, and StratifiedPermutationTest
(PR-C), plus SkeletonTabletSearch, ReverseSkeletonSearch, and
PersonsAggregator (PR-D), plus InteractionSurplusProfile,
OrderInformationProfile, TokenContextAssociation,
MetricFieldExtractor, SignatureComparator,
EvidenceRuleAggregator, PositionalClassClassifier, and
SignPositionNullTest (PR-E). The domain nodes converted in Spec
087 S3 PR-B (CanonicalSignLoader, ClusterMapper,
StructuralTemplateAnalyzer, ClusterArchaeology,
IndusSignRoleClassifier, DefaultIndusValueRoleMap,
IndusAnchorSetSyllable, DerivedAnchorSet, EpistaticAnchorRanker),
PR-C (IconographicAnchorScore, AllographAwareIconographicScore,
BlindHeldOutTest, BayesianDecoder, BayesianDecoderV2,
EnhancedNameMatcher, EnhancedNameMatcherV2, MeluhhaNameMatcher,
BilingualReadoutTest, BilingualReadoutTestV2,
PeriodStratifiedReadout, PeriodStratifiedReadout6Bucket,
ProvenienceStratifiedReadout), PR-D
(JanabiyahPhoneticReadout, JanabiyahPhoneticReadoutV2,
ReverseJanabiyahSearch, ReverseJanabiyahSearchV2,
M77ReverseJanabiyahSearchV3, LengthCohortReverseJanabiyahSearch,
MeluhhanPersonsExtractor, RefinedMeluhhanPersonsExtractor,
RefinedMeluhhanPersonsExtractorV2, Persons_v3_Extractor), and
PR-E (EpistaticInteractionDetector, EpistaticOrderProfile,
SignContextAssociation, DoFExtractor,
LanguageSignatureComparator, LanguageDetectorVerdict,
FulsPositionalClassifier, IndusNullModelTest) keep
their registered ids and parameter schemas; their
implementations delegate here with the domain content — table
names, file paths, numeral sets, value-role tables, diacritic
tables, alias tables, strata rules, rendering sets, verdict
text — carried as parameters instead of code. That is the
conversion contract: generic mechanism in this module, domain
content in parameters.

Like generic_loaders.py, this module is stdlib-only and imports
nothing from glossa_lab, so core and phase modules can both use
it without a cycle. The one data access it needs — synchronous
SQLite reads of the backend DB — is its own copy of the
_sync_db_all semantics (same path, same JSON-string coercion).

Engine parameter surfaces:

  RegistryTableLoader (params["registry_spec"], or flat params)
    table, filters (clause builders driven by params: mode
    "truthy" adds the clause when the named param is truthy,
    mode "arg" adds it with the param value as its argument
    when non-empty), id_field / uuid_field, count_filters
    (named field-equality counts over the loaded rows),
    error_prefix, empty_result, and the output key names.
    Without a spec, the defaults are the canonical-signs shape
    the primitive was generalised from.
  LabelMapApplier (params["map_spec"])
    sources: an ordered fallback chain of {"kind": "db_table",
    "table"}, {"kind": "json_file", "path", "map_key",
    "k_key", "k_default"}, {"kind": "frequency_rank", "bins"}
    entries; the first source yielding assignments wins.
    unmapped_label and unavailable_error complete the spec.
  TemplateMiner: min/max template lengths, min_count, and the
    top_templates / top_slots cuts as plain params.
  ClusterContingencyProfile: the strata rule (field,
    prefix_len, prefix_suffix), critical_per_dof, site_limit,
    and verdict_template as params; target selection is the
    historical target_cluster / fixed_members param pair.
  SignRoleClassifier: the role-rule thresholds as params;
    numeral_signs defaults EMPTY here — a domain caller's set
    is data it passes in, never a code default.
  ValueRoleMapSource: base_map + family_tables (per-family
    specs: seed_roles, base_values, vocab_sources with
    per-module import failure isolation, vocab_mode "fill" |
    "classify", determinative/numeral value sets) + extra.
  AnchorSyllabifier: anchors/vocab file paths and keys, the
    confidence order, the transliteration (diacritic) table,
    the skip pattern, and the fallback lengths as params.
  AssociationAnchorDeriver: min_z / max_anchors plus the
    anchor_prefix a derived anchor's value carries.
  PMICentralityRanker: top_k / min_count.
  IconographicAnchorScorer (params["scorer_spec"]): the alias
    table (ordered [reading-key, aliases, family] entries),
    confidence weights + high-confidence bonus, and — when
    extension_bonus is set — the allograph mode: family
    resolution (the matching entry's family, else the last
    table entry whose key the reading contains) and the
    per-member extension bonus over the allograph_families
    input. Verdict text is a template.
  PhonemeMapCoverage (params["coverage_spec"]): the unknown
    token, uncertain marker, high-confidence label, the
    placeholder skeleton text, and the verdict template; the
    mechanism is per-seal phoneme resolution + readability.
  PhonemeMapPermutationTest (params["decoder_spec"]): the
    shuffle dimension ("confidence" | "value"), the confidence
    weight table, the optional compound-plausibility scoring
    (pattern pairs + per-pattern / per-repeat bonuses as
    data), the null map's gloss, the output key names, and
    the verdict template + interpretation as data.
  LengthMatchScorer (params["matcher_spec"]): the assignment
    mode ("all_pairs" | "bipartite" | "aggregate_pairs"), the
    score spec — {"kind": "tolerance"} (1 - delta/(tol+1),
    rounded, 0 beyond tolerance) or a named {"kind": "linear",
    "divisor": d} falloff (max(0, 1 - |delta|/d), unrounded) —
    the min-frequency default, and the verdict templates.
  LengthMatchPermutationTest (params["test_spec"]): the
    statistic ("best_match" | "bipartite"), the permutation /
    frequency defaults, the insufficient-data verdict text,
    the verdict bands, the optional observed-assignment
    output, and the interpretation as data.
  StratifiedPermutationTest (params["strata_spec"]): the
    stratum field + result key, the ordered substring->bucket
    rules with case sensitivity and value stripping as data,
    the empty-text and fallback buckets, the seed base
    (per-stratum seed = base + len(bucket name); the merged
    overall run uses the base itself), and the verdict
    template. Its per-stratum test is the same bipartite
    core LengthMatchPermutationTest uses.
  SkeletonTabletSearch (params["readout_spec"]): the scan
    list (each scan: a rendering source — a spec constant or
    an input port — its per-row hit key, and its output
    keys), the keyword gate, the minimum-hit rule, the line
    truncation, an optional derived count (a difference of
    two scan counts), the echoed rendering list, the error
    result, and the verdict template + optional
    interpretation.
  ReverseSkeletonSearch (params["search_spec"]): the shared
    scoring core (target positions, target length, the length
    / position / free weights), the rendering set with the
    optional dynamic allograph expansion (family name as
    data), and the candidate mode — "persons" (aggregate
    rows by name; substring matching; the suffix-penalty set
    as data), "pn" (ePSD2 entries over their alternate forms
    under the carried segmenter; exact token matching;
    min_icount filter), or "pn_cohorts" (the "pn" scoring
    binned by best-form segment count over the cohort table,
    with the concentration factor as data). Output key names,
    the empty result, and the verdict text pieces are spec
    data.
  PersonsAggregator (params["persons_spec"]): the input
    port key, the collected field sets (proveniences,
    source patterns, distinct tablets, segment counts), the
    known-name rule (a carried name set, the upstream
    is_known flag, or none), the example-line truncation
    (none / a character cap), and the output plan (count key
    names, the full row list, the by-pattern distribution)
    with the verdict template.
  InteractionSurplusProfile (params["profile_spec"]): the
    PMI-surplus significance cut for the bigram and trigram
    counts; min counts, top_k, and label stay plain params.
  OrderInformationProfile (params["profile_spec"]): the
    regime rule table — an ordered list of rules, each a
    regime name plus [metric, operator, threshold] conditions
    over the order-fraction ratios (f2_over_f1, f3_over_f2) —
    and the fallback regime when no rule matches.
  TokenContextAssociation (params["association_spec"]): the
    significance cut and the strong-verdict minimum, plus the
    optional length binning (the binned field name, its
    source field, the ordered [bound, name] bins, and the
    default bin); field, n_perm, seed, min_count, and top_k
    stay plain params.
  MetricFieldExtractor (params["field_map"]): an ordered
    list of extraction entries — each names an output key
    and a read (a field of an input dict, the first row's
    field of a carried list, the field of the list row whose
    n equals a carried value, or the field of a list row at
    an index), with a default. The node that delegates here
    gains its parameter surface from this list.
  SignatureComparator (params["comparator_spec"]): the
    candidate tag and candidate marker (substrings that mark
    a bundle as the candidate), the negative-tag set, and
    the verdict margin; target_label stays a plain param.
  EvidenceRuleAggregator (params["aggregator_spec"]): the
    evidence rule table (ordered rules of kinds range_pair,
    field_equals, list_fraction_checks, success_threshold —
    each producing a formatted evidence line on the for or
    against side), the language score threshold, the
    confidence threshold, and the three verdict templates.
    The CAS thresholds stay plain params named by the
    success_threshold rule.
  PositionalClassClassifier (params["classifier_spec"]):
    the class label set, the ordered position-class rules
    (a dominant position whose rate must reach the dominance
    threshold while the other positions stay under the
    secondary threshold), and the verdict template; the
    thresholds themselves stay plain params.
  SignPositionNullTest (params["null_spec"]): the z-verdict
    bands (ordered [|z| threshold, verdict] pairs) and the
    fallback verdict; target sign, test type, run count, and
    seed stay plain params.
"""
from __future__ import annotations

import importlib
import json
import logging
import math
import random
import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ── DB access (a copy of experiment_graph._sync_db_all's semantics) ─────────


def _default_db_path() -> Path:
    return Path(__file__).parents[1] / "data" / "glossa.db"


def _db_all(table: str, where: str = "", params: tuple = ()) -> list[dict]:
    """Fetch all rows from a table synchronously, coercing JSON strings."""
    db_path = _default_db_path()
    if not db_path.exists():
        return []
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        sql = f"SELECT * FROM {table}"  # noqa: S608
        if where:
            sql += f" WHERE {where}"
        rows = conn.execute(sql, params).fetchall()
        result = []
        for row in rows:
            d = dict(row)
            for k, v in d.items():
                if isinstance(v, str) and v and v[0] in ("{", "["):
                    try:
                        d[k] = json.loads(v)
                    except Exception:  # noqa: BLE001
                        pass
            result.append(d)
        return result
    finally:
        conn.close()


# ── RegistryTableLoader ──────────────────────────────────────────────────────

_DEFAULT_REGISTRY_FILTERS: list[dict[str, Any]] = [
    {"clause": "in_corpus = 1", "param": "in_corpus_only", "mode": "truthy",
     "default": True},
    {"clause": "numbering_system = ?", "param": "numbering_system", "mode": "arg"},
]


def registry_table_loader_execute(inputs: dict, params: dict) -> dict:
    """Load a registry table and project it as records + counts + id maps.

    Generalised from CanonicalSignLoader: the table, its filter
    clauses, the id/uuid fields, and the named filter-counts are
    spec data; the projection (records, total, per-filter counts,
    id->uuid map, id list) is the mechanism.
    """
    spec: dict[str, Any] = params.get("registry_spec") or {}
    table = spec.get("table") or params.get("table") or ""
    id_field = spec.get("id_field", "sign_id")
    uuid_field = spec.get("uuid_field", "internal_id")

    where_parts = ["1=1"]
    args: list = []
    for flt in spec.get("filters", _DEFAULT_REGISTRY_FILTERS):
        if flt.get("mode", "truthy") == "arg":
            value = params.get(flt["param"]) or None
            if value:
                where_parts.append(flt["clause"])
                args.append(value)
        elif bool(params.get(flt["param"], flt.get("default", False))):
            where_parts.append(flt["clause"])
    where = " AND ".join(where_parts)

    try:
        rows = _db_all(table, where, tuple(args))
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{spec.get('error_prefix', 'Failed to load registry: ')}{exc}"}

    if not rows:
        return dict(
            spec.get(
                "empty_result",
                {
                    "error": "Canonical sign registry is empty — run POST /canonical-signs/seed first",
                    "n_signs": 0,
                },
            )
        )

    result: dict[str, Any] = {
        spec.get("records_output", "registry"): rows,
        spec.get("total_output", "n_signs"): len(rows),
    }
    for count_filter in spec.get(
        "count_filters",
        [{"output": "n_parpola", "field": "numbering_system", "value": "parpola_1982"}],
    ):
        result[count_filter["output"]] = len(
            [r for r in rows if r[count_filter["field"]] == count_filter["value"]]
        )
    result[spec.get("map_output", "sign_id_to_uuid")] = {
        r[id_field]: r[uuid_field] for r in rows
    }
    result[spec.get("ids_output", "sign_ids")] = [r[id_field] for r in rows]
    return result


# ── LabelMapApplier ──────────────────────────────────────────────────────────


def label_map_applier_execute(inputs: dict, params: dict) -> dict:
    """Apply a sign->label map from the first source that yields one.

    Generalised from ClusterMapper: the map's sources (DB table,
    JSON file, frequency-rank binning) and the unmapped label are
    spec data; applying the map and reporting coverage is the
    mechanism. NO phonetic mapping is performed.
    """
    spec: dict[str, Any] = params.get("map_spec") or {}
    sources: list[dict[str, Any]] = spec.get("sources") or []
    if not sources:
        built: list[dict[str, Any]] = []
        if params.get("db_table"):
            built.append({"kind": "db_table", "table": params["db_table"]})
        if params.get("file_path"):
            built.append({"kind": "json_file", "path": params["file_path"]})
        built.append({"kind": "frequency_rank", "bins": int(params.get("bins", 40))})
        sources = built
    unmapped_label = spec.get("unmapped_label", params.get("unmapped_label", -1))

    assignments: list = []
    summary: dict = {}
    sign_field = spec.get("sign_field", "sign_id")
    label_field = spec.get("label_field", "cluster_label")

    for source in sources:
        if assignments:
            break
        kind = source.get("kind")
        if kind == "db_table":
            try:
                rows = _db_all(source["table"])
                if rows:
                    assignments = rows
                    n_clusters = len(
                        {a.get(source.get("label_field", "cluster_label")) for a in assignments}
                    )
                    best_k = (
                        assignments[0].get(source.get("k_field", "cluster_k"), n_clusters)
                        if assignments
                        else 0
                    )
                    summary = {
                        "n_clusters": n_clusters,
                        "cluster_k": best_k,
                        "n_signs": len(assignments),
                    }
            except Exception:  # noqa: BLE001
                assignments = []
        elif kind == "json_file":
            cluster_json = Path(source["path"])
            if cluster_json.exists():
                try:
                    data = json.loads(cluster_json.read_text("utf-8"))
                    best_k = data.get(source.get("k_key", "best_k"), source.get("k_default", 40))
                    s2c_raw: dict = data.get(source.get("map_key", "sign_to_cluster"), {})
                    assignments = [
                        {"sign_id": sid, "cluster_label": lbl}
                        for sid, lbl in s2c_raw.items()
                    ]
                    n_clusters = len(set(s2c_raw.values()))
                    summary = {
                        "n_clusters": n_clusters,
                        "cluster_k": best_k,
                        "n_signs": len(s2c_raw),
                    }
                except Exception:  # noqa: BLE001
                    assignments = []
        elif kind == "frequency_rank":
            sequences_in = inputs.get("sequences") or []
            flat = [s for seq in sequences_in for s in seq]
            if not flat:
                return {
                    "error": spec.get(
                        "unavailable_error",
                        "Cluster assignments unavailable and no sequences to generate from. "
                        "Seed via POST /sign-clusters/seed or run scripts/cgsa_pipeline.py",
                    ),
                    "n_assignments": 0,
                }
            freq = Counter(flat)
            ranked = [s for s, _ in freq.most_common()]
            n_clusters = min(int(source.get("bins", 40)), len(ranked))
            bin_size = max(1, len(ranked) // n_clusters)
            for i, sign in enumerate(ranked):
                cluster_lbl = min(i // bin_size, n_clusters - 1)
                assignments.append({"sign_id": sign, "cluster_label": cluster_lbl})
            summary = {
                "n_clusters": n_clusters,
                "cluster_k": n_clusters,
                "n_signs": len(ranked),
                "source": "frequency_rank_fallback",
            }
            logger.info(
                "LabelMapApplier: generated %d frequency-rank clusters for %d signs",
                n_clusters,
                len(ranked),
            )

    s2c: dict[str, int] = {a[sign_field]: a[label_field] for a in assignments}
    sequences = inputs.get("sequences") or []
    cluster_sequences: list[list[int]] = []
    n_mapped = 0
    n_unmapped = 0
    for seq in sequences:
        cs = []
        for sign in seq:
            lbl = s2c.get(sign, unmapped_label)
            cs.append(lbl)
            if lbl >= 0:
                n_mapped += 1
            else:
                n_unmapped += 1
        cluster_sequences.append(cs)

    total = n_mapped + n_unmapped
    return {
        "cluster_sequences": cluster_sequences,
        "n_sequences": len(cluster_sequences),
        "n_mapped_tokens": n_mapped,
        "n_unmapped_tokens": n_unmapped,
        "map_rate": round(n_mapped / total, 4) if total else 0,
        "n_clusters": summary.get("n_clusters", 0),
        "cluster_k": summary.get("cluster_k", 0),
        "sign_to_cluster": s2c,
    }


# ── TemplateMiner ────────────────────────────────────────────────────────────


def template_miner_execute(inputs: dict, params: dict) -> dict:
    """Find recurrent templates in label sequences, with slot statistics.

    Generalised from StructuralTemplateAnalyzer: label-sequence
    template mining (length range, minimum count, top-N cuts as
    params) plus the four summary fields a plain n-gram
    composition cannot carry in one node — dominant prefix and
    suffix labels, per-slot occupancy, and the class-sequence
    entropy. Outputs are structural class labels; NO phonetic
    claims are made.
    """
    cluster_sequences = inputs.get("cluster_sequences") or []
    min_count = int(params.get("min_count", 3))
    max_len = int(params.get("max_template_length", 5))
    min_len = int(params.get("min_template_length", 2))
    top_templates = int(params.get("top_templates", 50))
    top_slots = int(params.get("top_slots", 10))

    if not cluster_sequences:
        return {
            "error": params.get(
                "empty_error",
                "No cluster_sequences — connect ClusterMapper.cluster_sequences",
            )
        }

    template_ctr: Counter = Counter()
    prefix_ctr: Counter = Counter()
    suffix_ctr: Counter = Counter()
    slot_dist: dict = {"initial": Counter(), "terminal": Counter(), "internal": Counter()}

    for cs in cluster_sequences:
        if not cs:
            continue
        clean = [c for c in cs if c >= 0]
        if not clean:
            continue
        prefix_ctr[clean[0]] += 1
        suffix_ctr[clean[-1]] += 1
        for i, c in enumerate(cs):
            if c < 0:
                continue
            if i == 0:
                slot_dist["initial"][c] += 1
            elif i == len(cs) - 1:
                slot_dist["terminal"][c] += 1
            else:
                slot_dist["internal"][c] += 1
        for length in range(min_len, min(max_len + 1, len(clean) + 1)):
            for i in range(len(clean) - length + 1):
                t = tuple(clean[i : i + length])
                template_ctr[t] += 1

    recurrent = [
        {"template": list(t), "count": c, "length": len(t)}
        for t, c in template_ctr.most_common(top_templates)
        if c >= min_count
    ]

    seq_ctr: Counter = Counter(tuple(cs) for cs in cluster_sequences)
    total_seqs = len(cluster_sequences)
    h_class = (
        -sum(
            (c / total_seqs) * math.log2(c / total_seqs)
            for c in seq_ctr.values()
            if c > 0
        )
        if total_seqs
        else 0
    )

    return {
        "n_templates": len(recurrent),
        "recurrent_templates": recurrent,
        "dominant_prefix_clusters": dict(prefix_ctr.most_common(top_slots)),
        "dominant_suffix_clusters": dict(suffix_ctr.most_common(top_slots)),
        "slot_occupancy": {
            k: dict(v.most_common(top_slots)) for k, v in slot_dist.items()
        },
        "h_class_sequence": round(h_class, 4),
        "n_distinct_class_sequences": len(seq_ctr),
        "n_sequences": total_seqs,
    }


# ── ClusterContingencyProfile ────────────────────────────────────────────────


def _chi_squared(observed: list[list[int]]) -> tuple[float, int]:
    """Pearson chi-squared on a 2D contingency table; returns (chi2, dof)."""
    rows = len(observed)
    cols = len(observed[0]) if rows else 0
    if rows < 2 or cols < 2:
        return 0.0, 0
    row_tot = [sum(r) for r in observed]
    col_tot = [sum(observed[i][j] for i in range(rows)) for j in range(cols)]
    grand = sum(row_tot)
    if grand <= 0:
        return 0.0, 0
    chi2 = 0.0
    for i in range(rows):
        for j in range(cols):
            exp = row_tot[i] * col_tot[j] / grand
            if exp > 0:
                chi2 += (observed[i][j] - exp) ** 2 / exp
    return chi2, (rows - 1) * (cols - 1)


def cluster_contingency_profile_execute(inputs: dict, params: dict) -> dict:
    """Per-cluster contingency profile over record strata.

    Generalised from ClusterArchaeology: the strata derivation
    (a record field's prefix grouping), the significance rule
    (chi2 > critical x dof), the site-table limit, and the
    verdict template are params; the contingency machinery —
    site and length tables, enrichment rates, the chi-squared
    test of strata-vs-cluster independence — is the mechanism.
    """
    inscriptions: list[dict] = inputs.get("inscriptions") or []
    sign_to_cluster: dict[str, int] = inputs.get("sign_to_cluster") or {}
    target_cluster = int(params.get("target_cluster", 0))
    fixed_members = params.get("fixed_members") or []
    strata_field = str(params.get("strata_field", "site_code"))
    prefix_len = int(params.get("prefix_len", 2))
    prefix_suffix = str(params.get("prefix_suffix", "0000"))
    critical = float(params.get("critical_per_dof", 3.84))
    site_limit = int(params.get("site_limit", 25))
    verdict_template = str(
        params.get(
            "verdict_template",
            "{outcome}: chi2={chi2:.2f} dof={dof}; per-site rate range "
            "{min_rate:.3f}-{max_rate:.3f} (corpus baseline {baseline:.3f}).",
        )
    )

    target_signs: set[str] = set()
    if fixed_members:
        target_signs = {str(s) for s in fixed_members}
    else:
        target_signs = {s for s, c in sign_to_cluster.items() if c == target_cluster}

    if not target_signs:
        return {"error": "no signs in target cluster"}

    site_total: Counter[str] = Counter()
    site_with_cluster: Counter[str] = Counter()
    length_total: Counter[int] = Counter()
    length_with_cluster: Counter[int] = Counter()
    n_total = len(inscriptions)
    n_with = 0

    def site_grp(sc: str) -> str:
        return (sc[:prefix_len] + prefix_suffix) if len(sc) >= prefix_len else sc

    for ins in inscriptions:
        site_code = str(ins.get(strata_field, ""))
        grp = site_grp(site_code)
        seq = ins.get("sequence") or []
        length = int(ins.get("length", len(seq)))
        site_total[grp] += 1
        length_total[length] += 1
        has_cluster = any(s in target_signs for s in seq)
        if has_cluster:
            n_with += 1
            site_with_cluster[grp] += 1
            length_with_cluster[length] += 1

    sites = sorted(site_total.keys(), key=lambda s: -site_total[s])
    contingency: list[list[int]] = []
    for s in sites:
        contingency.append(
            [site_with_cluster.get(s, 0), site_total[s] - site_with_cluster.get(s, 0)]
        )
    chi2, dof = _chi_squared(contingency)

    overall_rate = n_with / max(1, n_total)
    site_table: list[dict] = []
    for s in sites[:site_limit]:
        n_s = site_total[s]
        n_s_w = site_with_cluster.get(s, 0)
        rate = n_s_w / max(1, n_s)
        site_table.append(
            {
                "site_prefix": s,
                "n_inscriptions": n_s,
                "n_with_cluster": n_s_w,
                "rate_with_cluster": round(rate, 4),
                "enrichment": round(rate / overall_rate, 3) if overall_rate > 0 else None,
            }
        )

    length_table: list[dict] = []
    for length in sorted(length_total.keys()):
        n_l = length_total[length]
        n_l_w = length_with_cluster.get(length, 0)
        length_table.append(
            {
                "length": length,
                "n_inscriptions": n_l,
                "n_with_cluster": n_l_w,
                "rate_with_cluster": round(n_l_w / max(1, n_l), 4),
            }
        )

    significant = chi2 > critical * max(1, dof)
    verdict = verdict_template.format(
        outcome="CONFIRMED" if significant else "NOT CONFIRMED",
        chi2=chi2,
        dof=dof,
        min_rate=min(r["rate_with_cluster"] for r in site_table),
        max_rate=max(r["rate_with_cluster"] for r in site_table),
        baseline=overall_rate,
    )
    return {
        "target_cluster_signs": sorted(target_signs),
        "n_target_signs": len(target_signs),
        "n_inscriptions_total": n_total,
        "n_inscriptions_with_cluster": n_with,
        "overall_rate": round(overall_rate, 4),
        "site_table": site_table,
        "length_table": length_table,
        "chi_squared": round(chi2, 4),
        "dof": dof,
        "significant_p05": significant,
        "verdict": verdict,
    }


# ── SignRoleClassifier ───────────────────────────────────────────────────────

_DEFAULT_ROLE_BITS = (
    "suffix",
    "determinative",
    "numeral",
    "phonetic",
    "logogram",
    "compound",
)


def sign_role_classifier_execute(inputs: dict, params: dict) -> dict:
    """Derive a role mask per sign from corpus statistics.

    Generalised from IndusSignRoleClassifier: positional rates,
    the strict/relaxed suffix rules, the numeral repetition
    heuristic, the behaviour-based logogram detector, and
    bigram-PMI compound detection are the mechanism, with every
    threshold a param. The one domain content the Indus node
    carried — its default numeral-sign set — is a parameter
    here and defaults EMPTY: a caller that wants a numeral set
    passes it as data.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    if not sequences:
        return {"role_table": {}, "n_signs": 0}

    role_bits = tuple(params.get("role_bits") or _DEFAULT_ROLE_BITS)
    t_thr = float(params.get("terminal_threshold", 0.85))
    t_thr_relaxed = float(params.get("terminal_relaxed", 0.45))
    i_thr = float(params.get("initial_threshold", 0.70))
    pmi_thr = float(params.get("compound_pmi_threshold", 4.0))
    min_count = int(params.get("min_count", 5))
    numeral_repetition_thr = float(params.get("numeral_repetition_threshold", 0.5))
    numeral_set = set(params.get("numeral_signs") or [])
    logo_min_count = int(params.get("logogram_min_count", 20))
    logo_pos_concentration = float(params.get("logogram_position_concentration", 0.55))
    logo_solo_rate = float(params.get("logogram_solo_rate", 0.05))

    tc: Counter[str] = Counter(s for seq in sequences for s in seq)
    te: Counter[str] = Counter(seq[-1] for seq in sequences if len(seq) >= 1)
    ic: Counter[str] = Counter(seq[0] for seq in sequences if len(seq) >= 1)

    solo_or_repeat_count: Counter[str] = Counter()
    solo_count: Counter[str] = Counter()
    medial_count: Counter[str] = Counter()
    for seq in sequences:
        if len(seq) == 0:
            continue
        if len(seq) == 1:
            solo_or_repeat_count[seq[0]] += 1
            solo_count[seq[0]] += 1
            continue
        if len(set(seq)) == 1:
            solo_or_repeat_count[seq[0]] += len(seq)
        for s in seq[1:-1]:
            medial_count[s] += 1

    bg: Counter[tuple[str, str]] = Counter()
    for seq in sequences:
        for i in range(len(seq) - 1):
            bg[(seq[i], seq[i + 1])] += 1
    total_bg = sum(bg.values()) or 1
    total_uni = sum(tc.values()) or 1
    compound_signs: set[str] = set()
    for (a, b), c in bg.items():
        if c < 5:
            continue
        p_ab = c / total_bg
        p_a = tc[a] / total_uni
        p_b = tc[b] / total_uni
        if p_a > 0 and p_b > 0:
            pmi = math.log2(p_ab / (p_a * p_b))
            if pmi >= pmi_thr:
                compound_signs.add(a)
                compound_signs.add(b)

    role_table: dict[str, list[str]] = {}
    n_logograms_detected = 0
    for sym, n in tc.items():
        if n < min_count:
            continue
        t_rate = te[sym] / n if n else 0.0
        i_rate = ic[sym] / n if n else 0.0
        rep_rate = solo_or_repeat_count[sym] / n if n else 0.0
        m_rate = medial_count[sym] / n if n else 0.0
        solo_rate = solo_count[sym] / n if n else 0.0
        non_solo = max(1e-12, 1.0 - solo_rate)
        p_i = i_rate / non_solo
        p_m = m_rate / non_solo
        p_t = t_rate / non_solo
        pos_conc = p_i * p_i + p_m * p_m + p_t * p_t
        roles: set[str] = set()
        if t_rate >= t_thr or (
            t_rate >= t_thr_relaxed and (i_rate == 0 or t_rate >= 1.5 * i_rate)
        ):
            roles.add("suffix")
        if i_rate >= i_thr:
            roles.add("determinative")
        if sym in numeral_set or rep_rate >= numeral_repetition_thr:
            roles.add("numeral")
        if t_rate < t_thr and i_rate < i_thr and "numeral" not in roles:
            roles.add("phonetic")
        is_logogram = (
            n >= logo_min_count
            and pos_conc >= logo_pos_concentration
            and solo_rate >= logo_solo_rate
        )
        if is_logogram:
            roles.add("logogram")
            n_logograms_detected += 1
        if sym in compound_signs:
            roles.add("compound")
        if roles:
            role_table[sym] = sorted(roles)

    summary = {role: sum(1 for r in role_table.values() if role in r) for role in role_bits}
    return {
        "role_table": role_table,
        "n_signs": len(role_table),
        "role_summary": summary,
        "compound_signs": sorted(compound_signs),
        "high_pmi_bigrams": sorted(
            [{"a": a, "b": b, "count": c} for (a, b), c in bg.most_common(50)],
            key=lambda x: -x["count"],
        )[:50],
        "n_logograms": n_logograms_detected,
    }


# ── ValueRoleMapSource ───────────────────────────────────────────────────────


def _build_family_map(fspec: dict[str, Any]) -> dict[str, str]:
    """Build one family's value->role map from its spec.

    seed_roles are applied first, then base_values (all one
    role), then the vocabulary words gathered from the spec's
    vocab_sources: in "fill" mode a word takes the default role
    only if unclassified; in "classify" mode each word is
    classified by the determinative/numeral value sets. A
    vocab module that fails to import, or lacks a named
    attribute, contributes nothing (the historical builders'
    failure shape).
    """
    out: dict[str, str] = {}
    for value, role in (fspec.get("seed_roles") or {}).items():
        out[value] = role
    for value in fspec.get("base_values") or []:
        out[value] = fspec.get("base_role", "phonetic")

    by_module: dict[str, list[dict[str, Any]]] = {}
    for src in fspec.get("vocab_sources") or []:
        by_module.setdefault(src["module"], []).append(src)
    words_all: list[str] = []
    for module_path, srcs in by_module.items():
        try:
            mod = importlib.import_module(module_path)
            collected: list[str] = []
            for src in srcs:
                obj = getattr(mod, src["attr"])
                if callable(obj):
                    obj = obj()
                if isinstance(obj, dict):
                    words = [str(k) for k in obj.keys()]
                elif isinstance(obj, (list, tuple, set)):
                    words = [str(w) for w in obj]
                else:
                    continue
                filt = src.get("filter") or {}
                if filt.get("lower"):
                    words = [w.lower() for w in words]
                if filt.get("alpha_only"):
                    words = [w for w in words if w.isalpha()]
                if filt.get("min_len") is not None:
                    words = [w for w in words if len(w) >= filt["min_len"]]
                if filt.get("max_len") is not None:
                    words = [w for w in words if len(w) <= filt["max_len"]]
                collected.extend(words)
            words_all.extend(collected)
        except Exception:  # noqa: BLE001
            continue

    determinative_values = set(fspec.get("determinative_values") or [])
    numeral_values = set(fspec.get("numeral_values") or [])
    default_role = fspec.get("vocab_role", "phonetic")
    if fspec.get("vocab_mode", "fill") == "classify":
        for w in words_all:
            if w in determinative_values:
                out[w] = "determinative"
            elif w in numeral_values:
                out[w] = "numeral"
            else:
                out[w] = default_role
    else:
        for w in words_all:
            out.setdefault(w, default_role)
    return out


def value_role_map_source_execute(inputs: dict, params: dict) -> dict:
    """Emit a value-role map merged from a base map + selected families.

    Generalised from DefaultIndusValueRoleMap: the base map and
    the per-family tables are data params (family_tables, keyed
    by lower-cased family name); the merge order — base, then
    each family in the order named, then `extra` overrides —
    and the unknown-family reporting are the mechanism.
    """
    families_raw = params.get("families", []) or []
    if isinstance(families_raw, str):
        families_list = [s.strip() for s in families_raw.split(",") if s.strip()]
    elif isinstance(families_raw, (list, tuple)):
        families_list = [str(s).strip() for s in families_raw if str(s).strip()]
    else:
        families_list = []

    extra: dict[str, str] = params.get("extra", {}) or {}
    include_default = bool(params.get("include_default", True))
    base_map: dict[str, str] = params.get("base_map") or {}
    family_tables: dict[str, Any] = params.get("family_tables") or {}

    out: dict[str, str] = dict(base_map) if include_default else {}
    family_sizes: dict[str, int] = {}
    unknown: list[str] = []
    for fam in families_list:
        fspec = family_tables.get(fam.lower())
        if fspec is None:
            unknown.append(fam)
            continue
        fmap = _build_family_map(fspec)
        out.update(fmap)
        family_sizes[fam] = len(fmap)
    out.update(extra)
    return {
        "value_role_map": out,
        "n_values": len(out),
        "families_applied": list(family_sizes.keys()),
        "family_sizes": family_sizes,
        "unknown_families": unknown,
        "json": out,
    }


# ── AnchorSyllabifier ────────────────────────────────────────────────────────

_DEFAULT_CONFIDENCE_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "UNCERTAIN": 0}


def anchor_syllabifier_execute(inputs: dict, params: dict) -> dict:
    """Map anchor readings to syllable tokens from an anchor file.

    Generalised from IndusAnchorSetSyllable: the anchor file and
    syllable-vocab file (paths + keys), the confidence order,
    the transliteration (diacritic) table, the positional-label
    skip pattern, and the fallback lengths are params/data; the
    conversion — strip diacritics, direct vocab hit, CV split,
    prefix fallbacks — is the mechanism.
    """
    anchors_path = Path(str(params.get("anchors_path") or ""))
    vocab_path = Path(str(params.get("vocab_path") or ""))
    anchors_key = str(params.get("anchors_key", "anchors"))
    reading_field = str(params.get("reading_field", "reading"))
    confidence_field = str(params.get("confidence_field", "confidence"))
    default_confidence = str(params.get("default_confidence", "LOW"))
    vocab_key = str(params.get("vocab_key", "vocab"))
    conf_order: dict[str, int] = params.get("confidence_order") or _DEFAULT_CONFIDENCE_ORDER
    diacritic_table = [tuple(pair) for pair in (params.get("diacritic_table") or [])]
    vowels = set(str(params.get("vowels", "aeiouāīū")))
    consonants = set(str(params.get("consonants", "bcdfghjklmnpqrstvwxyz")))
    skip_pattern = params.get("skip_pattern")
    uncertain_substring = str(params.get("uncertain_substring", "uncertain"))
    skip_values = params.get("skip_values") or ["?", "-"]
    fallback_lengths = [int(n) for n in (params.get("fallback_lengths") or [2, 3, 1])]
    max_token_length = int(params.get("max_token_length", 3))
    verdict_template = str(
        params.get(
            "verdict_template",
            "Loaded {n_anchors} syllable-level anchors ({min_confidence}+ confidence)",
        )
    )

    if not anchors_path.exists():
        return {
            "anchor_dict": {},
            "error": params.get("missing_error", "anchors file not found"),
        }

    syllable_vocab: set[str] = set()
    if vocab_path.exists():
        lm_data = json.loads(vocab_path.read_text("utf-8"))
        syllable_vocab = set(lm_data.get(vocab_key, []))

    anchors_data = json.loads(anchors_path.read_text("utf-8"))
    min_conf = str(params.get("min_confidence", "MEDIUM")).upper()
    min_conf_level = conf_order.get(min_conf, 2)

    def _strip_diacritics(s: str) -> str:
        s = s.lower()
        for src, dst in diacritic_table:
            s = s.replace(src, dst)
        return s

    def _split_syllables(word: str) -> list[str]:
        syllables: list[str] = []
        i = 0
        current = ""
        while i < len(word):
            c = word[i]
            current += c
            if c in vowels:
                if (
                    i + 1 < len(word)
                    and word[i + 1] in consonants
                    and (i + 2 >= len(word) or word[i + 2] in vowels)
                ):
                    i += 1
                    current += word[i]
                syllables.append(current)
                current = ""
            elif len(current) >= 3:
                syllables.append(current)
                current = ""
            i += 1
        if current:
            if syllables:
                syllables[-1] += current
            else:
                syllables.append(current)
        return [s for s in syllables if len(s) >= 1]

    def _to_syllable(reading: str) -> str | None:
        reading = reading.split("/")[0].strip()
        reading = re.sub(r"\(.*\)", "", reading).strip()
        reading = reading.rstrip("?")
        if skip_pattern and re.match(skip_pattern, reading.lower()):
            return None
        if not reading or uncertain_substring in reading.lower() or reading in skip_values:
            return None
        clean = _strip_diacritics(reading)
        clean = re.sub(r"[^a-z]", "", clean)
        if not clean:
            return None
        if clean in syllable_vocab:
            return clean
        sylls = _split_syllables(clean)
        for s in sylls:
            if s in syllable_vocab:
                return s
        if len(clean) >= 2:
            for length in fallback_lengths:
                candidate = clean[:length]
                if candidate in syllable_vocab:
                    return candidate
        return clean[:max_token_length] if len(clean) > max_token_length else clean

    anchor_dict: dict[str, str] = {}
    skipped = 0
    all_anchors = anchors_data.get(anchors_key, {})
    for sign_id, info in all_anchors.items():
        conf = str(info.get(confidence_field, default_confidence)).upper()
        if conf_order.get(conf, 0) < min_conf_level:
            continue
        reading = str(info.get(reading_field, ""))
        syllable = _to_syllable(reading)
        if syllable is None:
            skipped += 1
            continue
        anchor_dict[sign_id] = syllable

    return {
        "anchor_dict": anchor_dict,
        "n_anchors": len(anchor_dict),
        "n_skipped": skipped,
        "min_confidence": min_conf,
        "verdict": verdict_template.format(
            n_anchors=len(anchor_dict), min_confidence=min_conf
        ),
    }


# ── AssociationAnchorDeriver ─────────────────────────────────────────────────


def association_anchor_deriver_execute(inputs: dict, params: dict) -> dict:
    """Derive anchors from the top-K significant sign-context associations.

    Generalised from DerivedAnchorSet: associations are sorted
    by descending pmi_z; each sign's first association at or
    above min_z binds it to `anchor_prefix + context`, up to
    max_anchors. The prefix is a param — the Indus node's
    "ctx:" convention is data, not mechanism.
    """
    associations = inputs.get("associations") or []
    min_z = float(params.get("min_z", 2.0))
    max_anchors = int(params.get("max_anchors", 25))
    prefix = str(params.get("anchor_prefix", ""))

    anchors: dict[str, str] = {}
    seen_signs: set[str] = set()
    table: list[dict] = []
    for r in sorted(
        (x for x in associations if isinstance(x, dict)),
        key=lambda x: -float(x.get("pmi_z", 0.0)),
    ):
        if float(r.get("pmi_z", 0.0)) < min_z:
            break
        sign = str(r.get("sign", ""))
        ctx = str(r.get("context", ""))
        if not sign or not ctx or sign in seen_signs:
            continue
        anchors[sign] = f"{prefix}{ctx}"
        seen_signs.add(sign)
        table.append(r)
        if len(anchors) >= max_anchors:
            break

    return {
        "anchors": anchors,
        "n_anchors": len(anchors),
        "anchor_table": table,
        "min_z": min_z,
        "verdict": (f"Derived {len(anchors)} anchors from associations at z>={min_z}."),
    }


# ── PMICentralityRanker ──────────────────────────────────────────────────────


def _ngram_counts(seqs: list[list[str]], n: int) -> Counter:
    out: Counter = Counter()
    for s in seqs:
        if len(s) < n:
            continue
        for i in range(len(s) - n + 1):
            out[tuple(s[i : i + n])] += 1
    return out


def pmi_centrality_ranker_execute(inputs: dict, params: dict) -> dict:
    """Rank signs by PMI centrality over their bigram partners.

    Generalised from EpistaticAnchorRanker: centrality(s) is the
    sum over partners p of |PMI(s, p)| weighted by count — the
    information-theoretic criterion for which sign's value, when
    fixed, most constrains the others. No domain constants.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    top_k = max(1, int(params.get("top_k", 10)))
    min_count = max(1, int(params.get("min_count", 5)))

    if not sequences:
        return {"ranking": [], "verdict": "Empty corpus."}

    uni = _ngram_counts(sequences, 1)
    bi = _ngram_counts(sequences, 2)
    n_uni = sum(uni.values()) or 1
    n_bi = sum(bi.values()) or 1

    centrality: dict[str, float] = {}
    n_partners: dict[str, int] = {}
    weighted_pmi: dict[str, float] = {}
    for (a, b), c in bi.items():
        if c < min_count:
            continue
        p_a = uni[(a,)] / n_uni
        p_b = uni[(b,)] / n_uni
        p_ab = c / n_bi
        if p_a <= 0 or p_b <= 0:
            continue
        pmi = math.log(p_ab / (p_a * p_b))
        w = abs(pmi) * c
        centrality[a] = centrality.get(a, 0.0) + w
        centrality[b] = centrality.get(b, 0.0) + w
        n_partners[a] = n_partners.get(a, 0) + 1
        n_partners[b] = n_partners.get(b, 0) + 1
        weighted_pmi[a] = weighted_pmi.get(a, 0.0) + pmi * c
        weighted_pmi[b] = weighted_pmi.get(b, 0.0) + pmi * c

    ranking = sorted(
        (
            {
                "sign": s,
                "centrality": round(centrality[s], 4),
                "n_partners": n_partners.get(s, 0),
                "weighted_pmi_sum": round(weighted_pmi.get(s, 0.0), 4),
                "unigram_count": uni[(s,)],
            }
            for s in centrality
        ),
        key=lambda r: -r["centrality"],
    )[:top_k]

    return {
        "ranking": ranking,
        "n_signs_ranked": len(centrality),
        "top_k": top_k,
        "verdict": (
            f"Ranked {len(centrality)} signs by epistatic centrality; "
            f"top sign {ranking[0]['sign'] if ranking else '?'} "
            f"(centrality={ranking[0]['centrality'] if ranking else 0:.2f})."
        ),
    }


# ── Shared helpers for the F4 + F5 engines ───────────────────────────────────


def _safe_int(x: Any, default: int = 0) -> int:
    """The phase modules' coercion, verbatim: int(x), else the default."""
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


def _name_n_segments(name: str) -> int:
    """Count hyphen-separated segments in a candidate name."""
    return name.count("-") + 1 if name else 0


def _length_score(n_signs: int, n_segments: int, tolerance: int = 2) -> float:
    """Length compatibility: 1.0 at exact match, 0.0 once delta > tolerance."""
    delta = abs(n_signs - n_segments)
    if delta > tolerance:
        return 0.0
    return round(1.0 - delta / (tolerance + 1), 3)


def _score_by_spec(score_spec: dict, n_signs: int, n_segments: int,
                   tolerance: int) -> float:
    """Score one (seal length, name segments) pair under a named spec.

    "tolerance" is the family-shared falloff (_length_score);
    "linear" is a named divergent falloff — max(0, 1 - |delta|/divisor),
    unrounded — carried as data so a conversion never silently
    re-shapes it (the MeluhhaNameMatcher pin).
    """
    if score_spec.get("kind") == "linear":
        divisor = float(score_spec.get("divisor", 5.0))
        return max(0.0, 1.0 - abs(n_signs - n_segments) / divisor)
    return _length_score(n_signs, n_segments, tolerance)


def _greedy_assignment(score_mat: list[list[float]], occs: list[int]) -> list[int]:
    """Greedy one-to-one assignment over a score matrix: names in
    descending-occurrence order each take their highest-scoring
    still-unused seal (score must be > 0); -1 marks unassigned."""
    n_names = len(score_mat)
    n_seals = len(score_mat[0]) if n_names else 0
    order = sorted(range(n_names), key=lambda i: -occs[i])
    used: set[int] = set()
    assignment = [-1] * n_names
    for i in order:
        best_j = -1
        best_s = 0.0
        for j in range(n_seals):
            if j in used:
                continue
            s = score_mat[i][j]
            if s > best_s:
                best_s = s
                best_j = j
        if best_j >= 0 and best_s > 0:
            assignment[i] = best_j
            used.add(best_j)
    return assignment


def _assignment_sum(score_mat: list[list[float]], assignment: list[int]) -> float:
    return sum(
        score_mat[i][assignment[i]]
        for i in range(len(assignment))
        if assignment[i] >= 0
    )


def _bipartite_null(score_mat: list[list[float]], occs: list[int],
                    n_perms: int, seed: int):
    """Observed greedy-assignment sum + the random-assignment null.

    One rng stream, consumed exactly as the historical copies did:
    per permutation, shuffle the seal indices, then (only when
    names outnumber seals) sample the participating names.
    Returns (observed, obs_assignment, null_dist).
    """
    n_names = len(score_mat)
    n_seals = len(score_mat[0]) if n_names else 0
    obs_assignment = _greedy_assignment(score_mat, occs)
    observed = _assignment_sum(score_mat, obs_assignment)
    rng = random.Random(seed)
    null_dist: list[float] = []
    for _ in range(n_perms):
        shuffled_seal_idxs = list(range(n_seals))
        rng.shuffle(shuffled_seal_idxs)
        if n_names > n_seals:
            participating = rng.sample(range(n_names), n_seals)
        else:
            participating = list(range(n_names))
        random_assignment = [-1] * n_names
        for slot, name_i in enumerate(participating):
            random_assignment[name_i] = shuffled_seal_idxs[slot]
        null_dist.append(_assignment_sum(score_mat, random_assignment))
    return observed, obs_assignment, null_dist


def _bipartite_assignment_test(candidates: list[dict], seal_lengths: list[int],
                               n_perms: int, tolerance: int, seed: int) -> dict:
    """The shared bipartite readout core (the phase25/26/27 copies of
    _run_bipartite_test were one implementation in three files)."""
    n_names = len(candidates)
    n_seals = len(seal_lengths)
    if n_names == 0 or n_seals == 0:
        return {"p_value": None, "observed": 0.0,
                "n_names": n_names, "n_seals": n_seals,
                "reason": "empty inputs"}
    name_segs = [_name_n_segments(r["candidate_name"]) for r in candidates]
    score_mat = [
        [_length_score(seal_lengths[j], name_segs[i], tolerance)
         for j in range(n_seals)]
        for i in range(n_names)
    ]
    occs = [_safe_int(r.get("occurrences")) for r in candidates]
    observed, _assignment, null_dist = _bipartite_null(
        score_mat, occs, n_perms, seed
    )
    p = sum(1 for v in null_dist if v >= observed) / n_perms
    null_mean = sum(null_dist) / len(null_dist)
    return {
        "p_value": round(p, 6),
        "observed": round(observed, 4),
        "null_mean": round(null_mean, 4),
        "n_names": n_names,
        "n_seals": n_seals,
        "n_perms": n_perms,
    }


def _null_stats(null_dist: list[float], observed: float, n_perms: int):
    """(p_value, null_mean, null_sd, z) with the readout tests' exact
    arithmetic: p as the at-or-above fraction, the sample (n-1)
    standard deviation, z against it (0.0 when sd is 0)."""
    n_at_or_above = sum(1 for v in null_dist if v >= observed)
    p_value = n_at_or_above / n_perms
    null_mean = sum(null_dist) / len(null_dist)
    null_var = (sum((x - null_mean) ** 2 for x in null_dist)
                / max(1, len(null_dist) - 1))
    null_sd = math.sqrt(null_var) if null_var > 0 else 0.0
    z = ((observed - null_mean) / null_sd) if null_sd > 0 else 0.0
    return p_value, null_mean, null_sd, z


def _verdict_for_p(p_value: float, bands: list, default: str) -> str:
    """First band whose threshold strictly exceeds p wins."""
    for threshold, label in bands:
        if p_value < threshold:
            return label
    return default


# ── IconographicAnchorScorer ─────────────────────────────────────────────────

_DEFAULT_ALIAS_TABLE: list = [
    ("fish", ["miin"], None),
    ("fish/star", ["miin"], None),
    ("fig", ["vaTa"], None),
    ("banyan/fig", ["vaTa"], None),
    ("banyan", ["vaTa"], None),
    ("muruku", ["muruku"], None),
    ("intersecting circles", ["muruku"], None),
    ("squirrel", ["piLLai"], None),
    ("pot", ["kuTam"], None),
    ("pot/jar", ["kuTam"], None),
    ("veL", ["veL", "veLLi"], None),
    ("veN-miin", ["veL"], None),
    ("venus", ["veL", "veLLi"], None),
    ("pleiades", ["aru-", "miin"], None),
    ("ursa major", ["eZu-", "miin"], None),
    ("north star", ["vaTa", "miin"], None),
]

_DEFAULT_ANCHOR_WEIGHTS = {"high": 2.0, "medium": 1.0, "low": 0.5}


def iconographic_anchor_scorer_execute(inputs: dict, params: dict) -> dict:
    """Score iconographic anchors against a sign->phoneme map.

    Generalised from IconographicAnchorScore (Phase-27) and its
    allograph-aware extension (Phase-28): the reading->phoneme alias
    table, the confidence weights, and the high-confidence bonus are
    spec data; matching, scoring, and row assembly are the mechanism.
    With scorer_spec["extension_bonus"] set, the allograph mode is
    on: rows carry the resolved family (the matching entry's family,
    or — the historical second pass — the family of the last table
    entry whose key the reading contains), family members present in
    the map with the family's phoneme earn the extension bonus, and
    the outputs gain the extension counts.
    """
    spec: dict[str, Any] = params.get("scorer_spec") or {}
    alias_table = spec.get("alias_table") or _DEFAULT_ALIAS_TABLE
    weights = spec.get("weights") or _DEFAULT_ANCHOR_WEIGHTS
    high_bonus = float(spec.get("high_conf_bonus", 1.5))
    extension_bonus = spec.get("extension_bonus")
    family_mode = extension_bonus is not None
    empty_result = spec.get(
        "empty_result", {"verdict": "NO_ANCHORS", "score": 0.0, "n_anchors": 0}
    )

    anchors = inputs.get("iconographic_anchors") or []
    phoneme_map = inputs.get("phoneme_map") or {}
    families = inputs.get("allograph_families") or {}

    if not anchors:
        return dict(empty_result)

    # Family name (lowercased) -> {members as strings, phoneme}.
    iconic_to_family: dict[str, dict] = {}
    for fam_name, fam in families.items():
        members = fam.get("members") or []
        iconic_to_family[fam_name.lower()] = {
            "name": fam_name,
            "members": [str(m) for m in members],
            "phoneme": (fam.get("phoneme") or "").lower(),
        }

    rows: list[dict] = []
    total_score = 0.0
    n_matches = 0
    n_total_anchors = 0
    n_allograph_extensions = 0
    extended_signs: set[str] = set()

    for a in anchors:
        sid = str(a.get("sign_id", "")).split("+")[0]  # first sign of compound
        iconic = (a.get("iconic_reading", "") or "").lower()
        anchor_conf = (a.get("confidence") or "low").lower()
        n_total_anchors += 1
        ph_entry = phoneme_map.get(sid, {}) or {}
        ph_value = (ph_entry.get("phoneme", "") or "").lower()
        ph_conf = (ph_entry.get("confidence") or "none").lower()

        # Direct or alias match: the first table entry whose key the
        # reading contains and one of whose aliases the phoneme value
        # contains.
        match = False
        family_name = None
        for entry in alias_table:
            key, aliases = entry[0], entry[1]
            fam = entry[2] if len(entry) > 2 else None
            if key in iconic:
                for al in aliases:
                    if al.lower() in ph_value:
                        match = True
                        family_name = fam
                        break
                if match:
                    break
        if family_mode and not match:
            # Historical second pass: family is the last contained
            # entry's, whether or not its alias matched (it cannot
            # match — the first pass exhausted the table).
            for entry in alias_table:
                if entry[0] in iconic:
                    family_name = entry[2] if len(entry) > 2 else None

        anchor_score = 0.0
        if match:
            n_matches += 1
            if anchor_conf == "high":
                anchor_score = float(weights.get("high", 2.0))
            elif anchor_conf == "medium":
                anchor_score = float(weights.get("medium", 1.0))
            else:
                anchor_score = float(weights.get("low", 0.5))
            # Bonus if both anchor and phoneme are high-confidence
            if ph_conf == "high":
                anchor_score *= high_bonus

        row: dict[str, Any] = {
            "anchor_id": a.get("anchor_id"),
            "sign_id": sid,
            "object_id": a.get("object_id"),
            "iconic_reading": a.get("iconic_reading"),
            "phoneme_value": ph_value,
            "phoneme_confidence": ph_conf,
            "anchor_confidence": anchor_conf,
            "match": match,
        }
        if family_mode:
            # Allograph extension: additional family members whose
            # phoneme matches the family's phoneme.
            family_extensions: list[str] = []
            if match and family_name and family_name in iconic_to_family:
                fam = iconic_to_family[family_name]
                target_phoneme = fam["phoneme"]
                for member in fam["members"]:
                    if member == sid:
                        continue
                    m_entry = phoneme_map.get(member, {}) or {}
                    m_phon = (m_entry.get("phoneme", "") or "").lower()
                    if not m_phon:
                        continue
                    if target_phoneme and target_phoneme in m_phon:
                        family_extensions.append(member)
                        extended_signs.add(member)
                n_allograph_extensions += len(family_extensions)
                anchor_score += float(extension_bonus) * len(family_extensions)
            row["family"] = family_name
            row["family_extensions"] = family_extensions
            row["n_allograph_extensions"] = len(family_extensions)
        row["anchor_score"] = round(anchor_score, 3)
        total_score += anchor_score
        rows.append(row)

    rows.sort(key=lambda r: -r["anchor_score"])
    verdict = spec["verdict_template"].format(
        n_matches=n_matches,
        n_total_anchors=n_total_anchors,
        total_score=total_score,
        n_allograph_extensions=n_allograph_extensions,
        extended_sign_ids=sorted(extended_signs),
    )
    result: dict[str, Any] = {
        "n_total_anchors": n_total_anchors,
        "n_matches": n_matches,
    }
    if family_mode:
        result["n_allograph_extensions"] = n_allograph_extensions
        result["extended_sign_ids"] = sorted(extended_signs)
    result["total_score"] = round(total_score, 3)
    result["rows"] = rows
    result["verdict"] = verdict
    return result


# ── PhonemeMapCoverage ───────────────────────────────────────────────────────


def phoneme_map_coverage_execute(inputs: dict, params: dict) -> dict:
    """Apply a phoneme map to inscribed seals and report readability.

    Generalised from BlindHeldOutTest: a seal is readable when at
    least one of its real (non-placeholder) signs resolves to a
    phoneme that is neither the unknown token nor marked uncertain;
    the token, marker, and high-confidence label are spec data, as
    is the verdict template (the historical text names its study).
    Per-seal high-confidence counts and the seal-level count of
    seals carrying one are both reported, as historically.
    """
    spec: dict[str, Any] = params.get("coverage_spec") or {}
    unknown_token = spec.get("unknown_token", "?")
    uncertain_marker = spec.get("uncertain_marker", "uncertain")
    high_conf_label = spec.get("high_conf_label", "high")
    placeholder_skeleton = spec.get("placeholder_skeleton", "(all placeholders)")
    verdict_template = spec.get(
        "verdict_template",
        "Phoneme-map coverage: {n_seals} inscribed seals; {n_readable} "
        "readable; {n_high_conf} with at least one high-confidence phoneme.",
    )

    seals = inputs.get("inscribed_seals") or []
    phoneme_map = inputs.get("phoneme_map") or {}

    rows: list[dict] = []
    n_readable = 0
    n_high_conf = 0
    for s in seals:
        signs = s.get("indus_signs") or []
        # Skip placeholder-only seals (all unknown tokens)
        real_signs = [x for x in signs if x and x != unknown_token]
        if not real_signs:
            rows.append({
                "catalogue_id": s.get("catalogue_id"),
                "n_signs": len(signs),
                "real_signs": 0,
                "predicted_phoneme_skeleton": placeholder_skeleton,
                "n_high_conf": 0,
                "readable": False,
            })
            continue

        skel: list[str] = []
        n_hc = 0
        for sid in real_signs:
            ph = phoneme_map.get(str(sid), {})
            phoneme = ph.get("phoneme", "?")
            skel.append(phoneme)
            if ph.get("confidence") == high_conf_label:
                n_hc += 1

        readable = any(
            p != unknown_token and uncertain_marker not in p.lower()
            for p in skel
        )
        if readable:
            n_readable += 1
        if n_hc > 0:
            n_high_conf += 1

        rows.append({
            "catalogue_id": s.get("catalogue_id"),
            "n_signs": len(signs),
            "real_signs": len(real_signs),
            "predicted_phoneme_skeleton": "-".join(skel),
            "n_high_conf": n_hc,
            "readable": readable,
        })

    verdict = verdict_template.format(
        n_seals=len(seals), n_readable=n_readable, n_high_conf=n_high_conf
    )
    return {
        "n_seals": len(seals),
        "n_readable": n_readable,
        "n_high_conf": n_high_conf,
        "rows": rows,
        "verdict": verdict,
    }


# ── PhonemeMapPermutationTest ────────────────────────────────────────────────


def _seal_match_score(seal: dict, phoneme_map: dict, weights: dict,
                      collect_phonemes: bool) -> dict:
    """Per-seal phoneme-coverage score: confidence-weighted attribution.

    The confidence weight table is data; "high" also counts as
    high-confidence. When collect_phonemes is on (the plausibility
    mode), the attributed phonemes of high/medium signs are returned
    in seal order.
    """
    signs = [s for s in (seal.get("indus_signs") or []) if s and s != "?"]
    n_high = 0
    n_attr = 0
    weight = 0.0
    phonemes_seen: list[str] = []
    for sid in signs:
        ph = phoneme_map.get(str(sid), {}) or {}
        conf = (ph.get("confidence") or "none").lower()
        phon = ph.get("phoneme", "?")
        if conf in weights:
            n_attr += 1
            weight += float(weights[conf])
            if conf == "high":
                n_high += 1
            if collect_phonemes and conf in ("high", "medium"):
                if phon and phon != "?":
                    phonemes_seen.append(phon)
    return {
        "n_signs": len(signs),
        "n_high_conf": n_high,
        "n_attributed": n_attr,
        "weight": round(weight, 3),
        "phonemes_seen": phonemes_seen,
    }


def _compound_plausibility(phonemes: list[str], patterns: list,
                           pattern_bonus: float, repeat_bonus: float) -> float:
    """Compound-plausibility of a phoneme sequence: a bonus per
    attested (first, second) pattern whose components both occur,
    plus a per-repeat bonus over '/'-split tokens. The pattern
    table and both bonuses are data."""
    if len(phonemes) < 2:
        return 0.0
    score = 0.0
    pset = set(p.lower().split()[0] for p in phonemes if p)
    for pair in patterns:
        a, b = pair[0], pair[1]
        if a.lower() in str(pset) or any(a in p.lower() for p in phonemes):
            for p in phonemes:
                if b.lower() in p.lower():
                    score += pattern_bonus
                    break
    counts: Counter = Counter()
    for p in phonemes:
        if not p or p == "?":
            continue
        for token in p.lower().split("/"):
            counts[token.strip()] += 1
    for c in counts.values():
        if c >= 2:
            score += repeat_bonus * (c - 1)
    return round(score, 3)


def phoneme_map_permutation_test_execute(inputs: dict, params: dict) -> dict:
    """Permutation test of a phoneme map's assignment over seals.

    Generalised from BayesianDecoder (shuffle the map's confidence
    labels) and BayesianDecoderV2 (shuffle the phoneme values,
    score with compound plausibility): the shuffle dimension, the
    confidence weights, the plausibility patterns/bonuses, the
    null map's gloss, the output key names, and the verdict /
    interpretation texts are spec data; the observed/null scoring
    is the mechanism. Outputs are seed-determined.
    """
    spec: dict[str, Any] = params.get("decoder_spec") or {}
    dimension = spec.get("shuffle_dimension", "confidence")
    weights = spec.get(
        "confidence_weights", {"high": 1.0, "medium": 0.5, "low": 0.2}
    )
    patterns = spec.get("plausibility_patterns")
    pattern_bonus = float(spec.get("pattern_bonus", 1.0))
    repeat_bonus = float(spec.get("repeat_bonus", 0.2))
    null_gloss = spec.get("null_gloss", "(null permutation)")
    observed_key = spec.get("observed_key", "observed_total_weight")
    null_mean_key = spec.get("null_mean_key", "null_mean_weight")
    rows_key = spec.get("rows_key", "obs_per_seal_top10")
    rows_limit = spec.get("rows_limit", 10)
    collect = patterns is not None

    seals = inputs.get("inscribed_seals") or []
    phoneme_map = inputs.get("phoneme_map") or {}
    n_perms = max(200, _safe_int(params.get("n_permutations", 1000), 1000))
    seed = _safe_int(params.get("seed", 1234), 1234)

    if not seals or not phoneme_map:
        return {"verdict": "INSUFFICIENT_DATA",
                "p_value": None,
                "n_seals": len(seals),
                "n_phonemes_in_map": len(phoneme_map)}

    sign_ids = sorted(phoneme_map.keys())
    confidences = [(phoneme_map[s].get("confidence") or "none").lower()
                   for s in sign_ids]
    phonemes = [phoneme_map[s].get("phoneme", "?") for s in sign_ids]

    def seal_total(seal: dict, mapping: dict):
        sc = _seal_match_score(seal, mapping, weights, collect)
        if collect:
            plausibility = _compound_plausibility(
                sc["phonemes_seen"], patterns, pattern_bonus, repeat_bonus
            )
            return sc, plausibility, sc["weight"] * (1.0 + plausibility)
        return sc, None, sc["weight"]

    # Observed
    obs_total = 0.0
    obs_per_seal: list[dict] = []
    for s in seals:
        sc, plausibility, total = seal_total(s, phoneme_map)
        if collect:
            obs_per_seal.append({
                "catalogue_id": s.get("catalogue_id"),
                "n_signs": sc["n_signs"],
                "phonemes_seen": sc["phonemes_seen"],
                "compound_plausibility": plausibility,
                "weighted_score": round(total, 3),
            })
        else:
            obs_per_seal.append({
                "catalogue_id": s.get("catalogue_id"),
                "n_signs": sc["n_signs"],
                "n_attributed": sc["n_attributed"],
                "n_high_conf": sc["n_high_conf"],
                "weight": sc["weight"],
            })
        obs_total += total

    # Null permutations: shuffle one dimension of the map across the
    # same sign IDs, holding the other dimension fixed.
    rng = random.Random(seed)
    null_totals: list[float] = []
    n_at_or_above = 0
    for _ in range(n_perms):
        if dimension == "value":
            shuffled = list(phonemes)
            rng.shuffle(shuffled)
            null_map = {
                sid: {"confidence": conf, "phoneme": phon, "gloss": null_gloss}
                for sid, phon, conf in zip(sign_ids, shuffled, confidences)
            }
        else:
            shuffled = list(confidences)
            rng.shuffle(shuffled)
            null_map = {
                sid: {"confidence": conf, "phoneme": "?", "gloss": null_gloss}
                for sid, conf in zip(sign_ids, shuffled)
            }
        total = 0.0
        for s in seals:
            total += seal_total(s, null_map)[2]
        null_totals.append(total)
        if total >= obs_total:
            n_at_or_above += 1

    p_value = n_at_or_above / n_perms
    null_mean = sum(null_totals) / len(null_totals) if null_totals else 0.0

    verdict = spec["verdict_template"].format(
        observed=obs_total,
        n_seals=len(seals),
        null_mean=null_mean,
        n_perms=n_perms,
        p_value=p_value,
    )
    return {
        "n_seals": len(seals),
        "n_phonemes_in_map": len(phoneme_map),
        observed_key: round(obs_total, 3),
        null_mean_key: round(null_mean, 3),
        "p_value": round(p_value, 6),
        "n_perms": n_perms,
        rows_key: obs_per_seal[:rows_limit] if rows_limit is not None else obs_per_seal,
        "verdict": verdict,
        "interpretation": spec.get("interpretation", ""),
    }


# ── LengthMatchScorer ────────────────────────────────────────────────────────


def length_match_scorer_execute(inputs: dict, params: dict) -> dict:
    """Score name<->seal length pairings under a named score spec.

    Generalised from EnhancedNameMatcher (all-pairs),
    EnhancedNameMatcherV2 (greedy bipartite assignment), and
    MeluhhaNameMatcher (candidates aggregated from raw person rows;
    seals filtered to sign-bearing; a different, named linear
    falloff). The assignment mode, score spec, min-frequency
    default, candidate source, and verdict texts are spec data;
    scoring and pairing assembly are the mechanism. Each mode
    returns its historical output shape.
    """
    spec: dict[str, Any] = params.get("matcher_spec") or {}
    mode = spec.get("assignment", "all_pairs")
    score_spec = spec.get("score_spec") or {"kind": "tolerance"}
    min_freq_default = int(spec.get("min_name_freq_default", 2))
    min_name_freq = _safe_int(
        params.get("min_name_freq", min_freq_default), min_freq_default
    )
    tolerance = _safe_int(params.get("tolerance", 2), 2)

    if mode == "aggregate_pairs":
        return _length_match_aggregate_pairs(
            inputs, min_name_freq, score_spec, spec
        )

    persons_rows = inputs.get("rows_all") or inputs.get("rows_top50") or []
    seals = inputs.get("inscribed_seals") or []
    candidates = [r for r in persons_rows
                  if _safe_int(r.get("occurrences")) >= min_name_freq]

    if mode == "bipartite":
        return _length_match_bipartite(
            candidates, seals, min_name_freq, tolerance, spec
        )
    return _length_match_all_pairs(
        candidates, seals, min_name_freq, tolerance, spec
    )


def _length_match_all_pairs(candidates, seals, min_name_freq, tolerance, spec):
    if not candidates or not seals:
        return {
            "n_candidates": len(candidates),
            "n_seals": len(seals),
            "pairings": [],
            "n_pairings": 0,
            "best_per_name": [],
            "verdict": spec["insufficient_template"].format(
                n_candidates=len(candidates), n_seals=len(seals)
            ),
        }

    pairings: list[dict] = []
    best_per_name: dict[str, dict] = {}
    for r in candidates:
        name = r["candidate_name"]
        n_seg = _name_n_segments(name)
        for s in seals:
            n_signs = _safe_int(s.get("inscription_length"))
            score = _length_score(n_signs, n_seg, tolerance)
            if score <= 0.0:
                continue
            pair = {
                "candidate_name": name,
                "name_n_segments": n_seg,
                "name_occurrences": r.get("occurrences"),
                "is_known_meluhhan": r.get("is_known_meluhhan", False),
                "seal_id": s.get("catalogue_id"),
                "seal_n_signs": n_signs,
                "seal_signs_confidence": s.get("signs_confidence"),
                "length_score": score,
            }
            pairings.append(pair)
            if (name not in best_per_name
                    or pair["length_score"] > best_per_name[name]["length_score"]):
                best_per_name[name] = pair

    pairings.sort(key=lambda p: (-p["length_score"], -p.get("name_occurrences", 0)))
    best_list = sorted(
        best_per_name.values(),
        key=lambda p: (-p["length_score"], -p.get("name_occurrences", 0)),
    )

    verdict = spec["verdict_template"].format(
        n_pairings=len(pairings),
        n_seals=len(seals),
        n_candidates=len(candidates),
        min_name_freq=min_name_freq,
        tolerance=tolerance,
    )
    return {
        "n_candidates": len(candidates),
        "n_seals": len(seals),
        "pairings": pairings,
        "pairings_top50": pairings[:50],
        "n_pairings": len(pairings),
        "best_per_name": best_list,
        "verdict": verdict,
    }


def _length_match_bipartite(candidates, seals, min_name_freq, tolerance, spec):
    if not candidates or not seals:
        return {
            "n_candidates": len(candidates),
            "n_seals": len(seals),
            "pairings": [],
            "n_pairings": 0,
            "verdict": spec["insufficient_template"].format(
                n_candidates=len(candidates), n_seals=len(seals)
            ),
        }

    name_segs = [
        (r["candidate_name"], _name_n_segments(r["candidate_name"]),
         _safe_int(r.get("occurrences")))
        for r in candidates
    ]
    seal_lengths = [_safe_int(s.get("inscription_length")) for s in seals]

    # Greedy bipartite: names from highest-occurrence to lowest; each
    # takes the highest-scoring still-unused seal index.
    assigned: dict[str, tuple[int, float]] = {}
    used: set[int] = set()
    names_sorted = sorted(name_segs, key=lambda t: -t[2])
    for name, n_seg, _occ in names_sorted:
        best_idx = -1
        best_score = 0.0
        for idx, n_signs in enumerate(seal_lengths):
            if idx in used:
                continue
            sc = _length_score(n_signs, n_seg, tolerance)
            if sc > best_score:
                best_score = sc
                best_idx = idx
        if best_idx >= 0 and best_score > 0:
            assigned[name] = (best_idx, best_score)
            used.add(best_idx)
        else:
            assigned[name] = (-1, 0.0)

    pairings: list[dict] = []
    name_to_row = {r["candidate_name"]: r for r in candidates}
    for name, (seal_idx, score) in assigned.items():
        if seal_idx < 0:
            continue
        seal = seals[seal_idx]
        row = name_to_row.get(name) or {}
        pairings.append({
            "candidate_name": name,
            "name_n_segments": _name_n_segments(name),
            "name_occurrences": row.get("occurrences"),
            "is_known_meluhhan": row.get("is_known_meluhhan", False),
            "seal_idx": seal_idx,
            "seal_id": seal.get("catalogue_id"),
            "seal_n_signs": _safe_int(seal.get("inscription_length")),
            "seal_signs_confidence": seal.get("signs_confidence"),
            "length_score": score,
        })
    pairings.sort(key=lambda p: (-p["length_score"],
                                  -(p.get("name_occurrences") or 0)))

    total_score = sum(p["length_score"] for p in pairings)
    n_assigned = len(pairings)

    return {
        "n_candidates": len(candidates),
        "n_seals": len(seals),
        "n_assigned": n_assigned,
        "n_unassigned": len(candidates) - n_assigned,
        "pairings": pairings,
        "n_pairings": n_assigned,
        "total_length_score": round(total_score, 4),
        "verdict": spec["verdict_template"].format(
            n_assigned=n_assigned,
            n_candidates=len(candidates),
            n_seals=len(seals),
            total_length_score=round(total_score, 4),
        ),
    }


def _length_match_aggregate_pairs(inputs, min_name_freq, score_spec, spec):
    persons = inputs.get("persons") or []
    seals = inputs.get("seals_at_mesopotamia") or []

    # Aggregate names from the raw person rows.
    name_counts: Counter[str] = Counter(
        p.get("candidate_name", "") for p in persons
    )
    candidates = [(n, c) for n, c in name_counts.most_common()
                  if c >= min_name_freq and n]
    seal_with_signs = [s for s in seals
                       if s.get("indus_signs")
                       and isinstance(s["indus_signs"], list)
                       and len(s["indus_signs"]) > 0]

    pairings: list[dict] = []
    if not seal_with_signs:
        verdict = spec["no_signs_template"].format(
            n_candidates=len(candidates),
            min_name_freq=min_name_freq,
            n_seals_total=len(seals),
        )
    else:
        for seal in seal_with_signs:
            n_signs = len(seal["indus_signs"])
            for name, count in candidates:
                # Akkadian/Sumerian name segments are hyphenated; count + 1
                name_n_segments = name.count("-") + 1
                length_score = _score_by_spec(
                    score_spec, n_signs, name_n_segments, 0
                )
                if length_score == 0:
                    continue
                pairings.append({
                    "seal_id": seal.get("catalogue_id"),
                    "seal_n_signs": n_signs,
                    "candidate_name": name,
                    "name_n_segments": name_n_segments,
                    "name_occurrences": count,
                    "length_score": round(length_score, 3),
                })
        pairings.sort(key=lambda r: -r["length_score"])
        verdict = spec["verdict_template"].format(
            n_pairings=len(pairings),
            n_seals_with_signs=len(seal_with_signs),
            n_candidates=len(candidates),
        )

    return {
        "n_candidates": len(candidates),
        "n_seals_with_signs": len(seal_with_signs),
        "n_seals_total": len(seals),
        "pairings_top50": pairings[:50],
        "n_pairings": len(pairings),
        "verdict": verdict,
    }


# ── LengthMatchPermutationTest ───────────────────────────────────────────────


def length_match_permutation_test_execute(inputs: dict, params: dict) -> dict:
    """Permutation test over name<->seal length matching.

    Generalised from BilingualReadoutTest (statistic: per-name best
    length score, summed; null: shuffle the seal lengths) and
    BilingualReadoutTestV2 (statistic: the greedy bipartite
    assignment sum; null: random one-to-one assignments). The
    statistic, the defaults, the insufficient-data verdict, the
    verdict bands, the observed-assignment output, and the
    interpretation are spec data. Outputs are seed-determined.
    """
    spec: dict[str, Any] = params.get("test_spec") or {}
    statistic = spec.get("statistic", "best_match")
    perms_default = int(spec.get("n_permutations_default", 1000))
    min_freq_default = int(spec.get("min_name_freq_default", 2))
    n_perms = max(100, _safe_int(
        params.get("n_permutations", perms_default), perms_default
    ))
    min_name_freq = _safe_int(
        params.get("min_name_freq", min_freq_default), min_freq_default
    )
    tolerance = _safe_int(params.get("tolerance", 2), 2)
    seed = _safe_int(params.get("seed", 42), 42)
    bands = spec.get(
        "verdict_bands",
        [[0.01, "READOUT_SIGNIFICANT (p<0.01)"],
         [0.05, "READOUT_MARGINAL (p<0.05)"]],
    )
    verdict_default = spec.get("verdict_default", "READOUT_NOT_SIGNIFICANT")

    persons_rows = inputs.get("rows_all") or inputs.get("rows_top50") or []
    seals = inputs.get("inscribed_seals") or []

    candidates = [r for r in persons_rows
                  if _safe_int(r.get("occurrences")) >= min_name_freq]
    seal_lengths = [_safe_int(s.get("inscription_length")) for s in seals]
    if not candidates or not seal_lengths:
        return {
            "verdict": spec.get("insufficient_verdict", "INSUFFICIENT_DATA"),
            "p_value": None,
            "n_candidates": len(candidates),
            "n_seals": len(seal_lengths),
        }

    obs_assignment = None
    if statistic == "bipartite":
        name_segs = [_name_n_segments(r["candidate_name"]) for r in candidates]
        score_mat = [
            [_length_score(seal_lengths[j], name_segs[i], tolerance)
             for j in range(len(seal_lengths))]
            for i in range(len(candidates))
        ]
        occs = [_safe_int(r.get("occurrences")) for r in candidates]
        observed, obs_assignment, null_dist = _bipartite_null(
            score_mat, occs, n_perms, seed
        )
    else:
        name_segs_full = [
            (r["candidate_name"], _name_n_segments(r["candidate_name"]),
             _safe_int(r.get("occurrences")))
            for r in candidates
        ]

        def _stat(lengths: list[int]) -> float:
            total = 0.0
            for _, n_seg, _occ in name_segs_full:
                best = 0.0
                for n_sign in lengths:
                    s = _length_score(n_sign, n_seg, tolerance)
                    if s > best:
                        best = s
                total += best
            return total

        observed = _stat(seal_lengths)
        rng = random.Random(seed)
        null_dist = []
        permuted = list(seal_lengths)
        for _ in range(n_perms):
            rng.shuffle(permuted)
            null_dist.append(_stat(permuted))

    p_value, null_mean, null_sd, z = _null_stats(null_dist, observed, n_perms)
    verdict = _verdict_for_p(p_value, bands, verdict_default)

    result: dict[str, Any] = {
        "verdict": verdict,
        "p_value": round(p_value, 6),
        "observed": round(observed, 4),
        "null_mean": round(null_mean, 4),
        "null_sd": round(null_sd, 4),
        "z_score": round(z, 4),
        "n_permutations": n_perms,
        "n_candidates": len(candidates),
        "n_seals": len(seal_lengths),
        "tolerance": tolerance,
    }
    if spec.get("include_assignment") and obs_assignment is not None:
        name_segs = [_name_n_segments(r["candidate_name"]) for r in candidates]
        obs_pairings = []
        for i, j in enumerate(obs_assignment):
            if j < 0:
                continue
            obs_pairings.append({
                "candidate_name": candidates[i]["candidate_name"],
                "name_n_segments": name_segs[i],
                "seal_idx": j,
                "seal_id": seals[j].get("catalogue_id"),
                "seal_n_signs": seal_lengths[j],
                "length_score": _length_score(seal_lengths[j], name_segs[i], tolerance),
            })
        result["observed_assignment"] = obs_pairings
    result["interpretation"] = spec.get("interpretation", "")
    return result


# ── StratifiedPermutationTest ────────────────────────────────────────────────


def _classify_stratum(text: str, rules: list, case_insensitive: bool,
                      empty_bucket, fallback_bucket: str) -> str:
    """Ordered substring->bucket classification: the first bucket
    with a key contained in the text wins; empty text takes the
    empty bucket when one is named, else the fallback."""
    if not text:
        return empty_bucket if empty_bucket is not None else fallback_bucket
    t = text.lower() if case_insensitive else text
    for entry in rules:
        bucket, keys = entry[0], entry[1]
        for k in keys:
            if k in t:
                return bucket
    return fallback_bucket


def stratified_permutation_test_execute(inputs: dict, params: dict) -> dict:
    """Run the bipartite readout test per stratum + merged overall.

    Generalised from PeriodStratifiedReadout (case-sensitive inline
    period coarsening, seed base 42), PeriodStratifiedReadout6Bucket
    (an 8-bucket substring table, seed base 271), and
    ProvenienceStratifiedReadout (a 13-bucket table over a
    different person field, seed base 137): the stratum field,
    the ordered rules, case sensitivity, value stripping, the
    empty/fallback buckets, the seed base, and the verdict
    template are spec data. Strata with fewer than two distinct
    candidates are skipped; the overall run merges the tested
    strata's candidates. Proving the two period variants are one
    primitive is the same inputs under both rule sets.
    """
    spec: dict[str, Any] = params.get("strata_spec") or {}
    stratum_field = spec.get("stratum_field", "period")
    axis_key = spec.get("axis_key", stratum_field)
    rules = spec.get("strata_rules") or []
    case_insensitive = bool(spec.get("case_insensitive", True))
    strip_value = bool(spec.get("strip_value", False))
    empty_bucket = spec.get("empty_bucket")
    fallback_bucket = spec.get("fallback_bucket", "Other")
    seed_base = int(spec.get("seed_base", 42))
    min_stratum = int(spec.get("min_stratum_size", 2))
    verdict_template = spec.get(
        "verdict_template",
        "Stratified readout: {n_results} strata tested; "
        "{n_significant} achieve p<0.05.",
    )

    persons = inputs.get("persons_v3") or []
    seals = inputs.get("inscribed_seals") or []
    n_perms = max(500, _safe_int(params.get("n_permutations", 1000), 1000))
    tolerance = _safe_int(params.get("tolerance", 2), 2)

    seal_lengths = [_safe_int(s.get("inscription_length")) for s in seals]
    if not persons or not seal_lengths:
        return {"verdict": "INSUFFICIENT_DATA", "results": []}

    # Aggregate persons by candidate name within each stratum.
    candidates_by_stratum: dict[str, dict[str, dict]] = {}
    for p in persons:
        raw = p.get(stratum_field, "") or ""
        if strip_value:
            raw = raw.strip()
        bucket = _classify_stratum(
            raw, rules, case_insensitive, empty_bucket, fallback_bucket
        )
        cmap = candidates_by_stratum.setdefault(bucket, {})
        name = p.get("candidate_name", "")
        if not name:
            continue
        if name not in cmap:
            cmap[name] = {"candidate_name": name, "occurrences": 0}
        cmap[name]["occurrences"] += 1

    results: list[dict] = []
    overall_candidates: list[dict] = []
    for bucket, cmap in sorted(candidates_by_stratum.items()):
        cands = list(cmap.values())
        cands.sort(key=lambda r: -r["occurrences"])
        if len(cands) < min_stratum:
            continue
        r = _bipartite_assignment_test(
            cands, seal_lengths, n_perms, tolerance,
            seed=seed_base + len(bucket),
        )
        r[axis_key] = bucket
        r["n_unique_candidates"] = len(cands)
        results.append(r)
        overall_candidates.extend(cands)

    # Plus the overall (unstratified) result for comparison.
    if overall_candidates:
        merged: dict[str, dict] = {}
        for c in overall_candidates:
            n = c["candidate_name"]
            if n not in merged:
                merged[n] = {"candidate_name": n, "occurrences": 0}
            merged[n]["occurrences"] += c["occurrences"]
        overall = list(merged.values())
        overall.sort(key=lambda r: -r["occurrences"])
        r_all = _bipartite_assignment_test(
            overall, seal_lengths, n_perms, tolerance, seed=seed_base
        )
        r_all[axis_key] = "ALL (overall)"
        r_all["n_unique_candidates"] = len(overall)
        results.append(r_all)

    significant = [r for r in results if isinstance(r.get("p_value"), float)
                   and r["p_value"] < 0.05]
    verdict = verdict_template.format(
        n_results=len(results), n_significant=len(significant)
    )
    return {
        "results": results,
        "n_significant_strata": len(significant),
        "verdict": verdict,
    }


# ── SkeletonTabletSearch ─────────────────────────────────────────────────────


def _resolve_renderings(source: dict, inputs: dict) -> list:
    """A scan's rendering list: a constant carried in the spec, or a
    list arriving through an input port."""
    if "constant" in source:
        return list(source.get("constant") or [])
    return list(inputs.get(source.get("input", "")) or [])


def skeleton_tablet_search_execute(inputs: dict, params: dict) -> dict:
    """Predict a seal reading's phonetic skeleton and scan tablet
    lines for rendering matches.

    Generalised from JanabiyahPhoneticReadout (Phase-25: one scan
    over an 11-item rendering list carried as a code constant) and
    JanabiyahPhoneticReadoutV2 (Phase-26: two scans — direct-only
    and expanded — over rendering lists arriving through input
    ports). The scan list is spec data: each scan names its
    rendering source (constant or input port), its per-row hit
    key, and its output keys; the keyword gate, the minimum-hit
    rule, and the line truncation are spec data, as are the
    verdict template, the optional interpretation, and the
    optional derived count (a difference of two scan counts).
    The skeleton itself is the phoneme sequence the map assigns
    to the reading's signs; a sign the map lacks predicts the
    unknown token with the historical defaults.
    """
    spec: dict[str, Any] = params.get("readout_spec") or {}
    keyword_gate = spec.get("keyword_gate", "me-luh")
    min_hits = int(spec.get("min_hits", 2))
    line_limit = int(spec.get("line_limit", 160))
    top_n = int(spec.get("top_n", 20))
    scans = spec.get("scans") or []
    verdict_template = spec.get("verdict_template", "")

    janabiyah = inputs.get("janabiyah_reading") or {}
    phoneme_map = inputs.get("phoneme_map") or {}
    tablets = inputs.get("tablets") or []

    if not janabiyah or not phoneme_map:
        return dict(spec.get("error_result") or {
            "error": "Phoneme map or Janabiyah reading not available."
        })

    sign_seq = janabiyah.get("sign_sequence", [])
    predictions: list[dict] = []
    for sign_id in sign_seq:
        ph = phoneme_map.get(sign_id, {})
        predictions.append({
            "sign_id": sign_id,
            "phoneme": ph.get("phoneme", "?"),
            "gloss": ph.get("gloss", "(unmapped)"),
            "confidence": ph.get("confidence", "none"),
        })

    miin_count = sum(1 for p in predictions
                     if "miin" in (p["phoneme"] or "").lower())
    skeleton = "-".join(p["phoneme"] for p in predictions)

    out: dict[str, Any] = {
        "skeleton": skeleton,
        "predictions": predictions,
        "n_miin": miin_count,
        "n_signs": len(sign_seq),
    }
    counts: dict[str, int] = {}
    for scan in scans:
        renderings = _resolve_renderings(scan.get("renderings") or {}, inputs)
        hit_key = scan.get("hit_key", "n_hits")
        matches: list[dict] = []
        for t in tablets:
            kw = " ".join(t.get("matched_keywords") or []).lower()
            if keyword_gate not in kw:
                continue
            line_pool: list[str] = []
            line_pool.extend(t.get("atf_lines_with_match") or [])
            line_pool.extend(t.get("atf_excerpt_lines") or [])
            for line in line_pool:
                ll = line.lower()
                hits = sum(1 for r in renderings if r in ll)
                if hits >= min_hits:
                    matches.append({
                        "p_number": t.get("p_number"),
                        "period": t.get("period"),
                        "provenience": t.get("provenience"),
                        hit_key: hits,
                        "line": line[:line_limit],
                    })
        matches.sort(key=lambda m: -m[hit_key])
        out[scan.get("top_key", "matches_top20")] = matches[:top_n]
        counts[scan.get("count_key", "n_matches")] = len(matches)
        out[scan.get("count_key", "n_matches")] = len(matches)

    diff = spec.get("count_difference")
    if diff:
        out[diff["key"]] = counts[diff["minuend"]] - counts[diff["subtrahend"]]
    if spec.get("renderings_echo") is not None:
        out["miin_renderings_searched"] = _resolve_renderings(
            spec["renderings_echo"], inputs
        )

    context: dict[str, Any] = {
        "skeleton": skeleton,
        "n_miin": miin_count,
        "n_tablets": len(tablets),
    }
    context.update(counts)
    out["verdict"] = verdict_template.format(**context)
    if spec.get("interpretation") is not None:
        out["interpretation"] = spec["interpretation"]
    return out


# ── ReverseSkeletonSearch ────────────────────────────────────────────────────


def _skeleton_length_score(n_segs: int, target_length: int,
                           base: float, step: float) -> float:
    """The Janabiyah family's shared length component: a base score
    falling by a fixed step per segment of distance from the target
    length, floored at zero."""
    return max(0.0, base - step * abs(n_segs - target_length))


def _expand_renderings(base, phoneme_map: dict, families: dict,
                       family_name: str) -> set:
    """The Phase-28 dynamic rendering expansion: tokens of the
    phonemes the map assigns to the named allograph family's
    members join the base set (split on '/' or whitespace, length
    at least 2)."""
    renderings = set(base)
    members = {
        str(m) for m in (families.get(family_name) or {}).get("members") or []
    }
    for sid in members:
        ph = (phoneme_map.get(sid) or {}).get("phoneme", "")
        for tok in re.split(r"[/\s]", ph or ""):
            t = tok.strip().lower()
            if t and len(t) >= 2:
                renderings.add(t)
    return renderings


def _rendering_tokens(renderings) -> set:
    """The token set the ePSD2 modes match against: every rendering
    split on '-', keeping tokens of length at least 2."""
    tokens: set = set()
    for r in renderings:
        for t in r.split("-"):
            if t and len(t) >= 2:
                tokens.add(t)
    return tokens


def _epsd_segments(forms) -> list:
    """The ePSD2 segmenter (Phase-29/30): strip {…} determinatives,
    lowercase, split on hyphen runs, drop trailing subscript digits
    and empty parts; forms yielding no parts are dropped."""
    segs: list = []
    for f in forms or []:
        if not f:
            continue
        clean = re.sub(r"\{[^}]+\}", "", str(f).lower())
        parts = [p for p in re.split(r"[-]+", clean) if p and not p.isspace()]
        parts = [re.sub(r"[0-9]+$", "", p) for p in parts]
        parts = [p for p in parts if p]
        if parts:
            segs.append(parts)
    return segs


def _score_pn_forms(forms, periods, icount: int, headword: str,
                    tokens: set, core: dict):
    """Score one ePSD2 entry over its alternate forms, keeping the
    best-scoring form (the first form wins ties). Matching is exact
    token membership — the Phase-29/30 rule, distinct from the
    persons modes' substring rule. Returns None when no form
    segments."""
    all_segs = _epsd_segments(forms)
    if not all_segs:
        return None
    best_score = -999.0
    best_segs: list = []
    best_pmatch = 0
    best_free = 0
    best_positions: list = []
    for segs in all_segs:
        length_score = _skeleton_length_score(
            len(segs), core["target_length"],
            core["length_base"], core["length_step"],
        )
        pmatch = 0
        positions: list = []
        for i, seg in enumerate(segs):
            if i in core["target_positions"] and seg.lower() in tokens:
                pmatch += 1
                positions.append(i)
        free = sum(1 for s in segs if s.lower() in tokens)
        total = (length_score + pmatch * core["position_weight"]
                 + free * core["free_weight"])
        if total > best_score:
            best_score = total
            best_segs = segs
            best_pmatch = pmatch
            best_free = free
            best_positions = positions
    return {
        "headword": headword,
        "best_form": "-".join(best_segs),
        "n_segments": len(best_segs),
        "position_match": best_pmatch,
        "positions_matched": best_positions,
        "free_miin": best_free,
        "total_score": round(best_score, 3),
        "icount": icount,
        "periods": periods,
        "n_alternate_forms": len(all_segs),
    }


def reverse_skeleton_search_execute(inputs: dict, params: dict) -> dict:
    """Score candidate names against a predicted phonetic skeleton.

    Generalised from the four reverse Janabiyah searches
    (Phase-27/28 over aggregated person rows; Phase-29/30 over
    ePSD2 personal-name entries). All modes share one scoring
    core carried as spec data: the target segment positions
    ({1, 3, 6} historically), the target length (7), and the
    weights (length base 3.0 falling 0.5 per segment of distance;
    1.5 per position match; 0.5 per free occurrence). What
    differs is data, named in the spec:

    - candidate_mode "persons": person rows aggregated by
      candidate name (occurrences + first-seen meta); matching is
      substring over the rendering set; the -me-luh-ha /
      -me-luh-ha-ki suffix penalty applies (penalty_suffixes).
    - candidate_mode "pn": ePSD2 entries segmented by the ePSD2
      segmenter, filtered by min_icount, each scored over its
      alternate forms; matching is exact membership in the
      rendering TOKEN set; no penalty.
    - candidate_mode "pn_cohorts": the "pn" scoring, then the
      scored entries binned by best-form segment count over the
      cohort table (a param, with a spec default), per-cohort
      hit rates, and the concentration verdict (peak rate more
      than concentration_factor x the minimum rate).

    The rendering set is spec data; with expand_renderings set,
    the Phase-28 dynamic expansion from the phoneme map via the
    named allograph family is applied first. The target reading
    input is required (its emptiness is the insufficient-data
    condition) although the pattern itself is spec data — the
    historical behaviour of all four nodes.
    """
    spec: dict[str, Any] = params.get("search_spec") or {}
    mode = spec.get("candidate_mode", "persons")
    core = {
        "target_positions": set(spec.get("target_positions", [1, 3, 6])),
        "target_length": int(spec.get("target_length", 7)),
        "length_base": float(spec.get("length_base", 3.0)),
        "length_step": float(spec.get("length_step", 0.5)),
        "position_weight": float(spec.get("position_weight", 1.5)),
        "free_weight": float(spec.get("free_weight", 0.5)),
    }
    top_k_default = int(spec.get("top_k_default", 20))
    top_k_floor = int(spec.get("top_k_floor", 10))
    top_k = max(top_k_floor, _safe_int(params.get("top_k", top_k_default),
                                       top_k_default))

    janabiyah = inputs.get("janabiyah_reading") or {}
    renderings = set(spec.get("renderings") or [])
    if spec.get("expand_renderings"):
        renderings = _expand_renderings(
            renderings,
            inputs.get("phoneme_map") or {},
            inputs.get("allograph_families") or {},
            spec.get("expansion_family", "fish"),
        )

    if mode == "persons":
        persons = inputs.get(spec.get("candidates_input", "persons_v3")) or []
        if not persons or not janabiyah:
            return dict(spec.get("empty_result") or {
                "verdict": "INSUFFICIENT_DATA",
                "n_candidates": 0,
                "top_matches": [],
            })
        name_counts: Counter = Counter()
        name_meta: dict = {}
        for p in persons:
            n = p.get("candidate_name", "")
            if not n:
                continue
            name_counts[n] += 1
            if n not in name_meta:
                name_meta[n] = {
                    "first_period": p.get("period", ""),
                    "first_provenience": p.get("provenience", ""),
                    "first_p_number": p.get("p_number", ""),
                }
        penalty_suffixes = spec.get("penalty_suffixes") or []
        penalty_value = float(spec.get("penalty_value", -1.5))
        scored: list = []
        for name in name_counts.keys():
            segs = name.split("-")
            length_score = _skeleton_length_score(
                len(segs), core["target_length"],
                core["length_base"], core["length_step"],
            )
            position_match = 0
            positions_matched: list = []
            for i, seg in enumerate(segs):
                seg_l = seg.lower().strip("()? ")
                if (i in core["target_positions"]
                        and any(r in seg_l for r in renderings)):
                    position_match += 1
                    positions_matched.append(i)
            free_miin = sum(
                1 for s in segs
                if any(r in s.lower().strip("()? ") for r in renderings)
            )
            penalty = 0.0
            if any(name.endswith(sfx) for sfx in penalty_suffixes):
                penalty += penalty_value
            total = (length_score + position_match * core["position_weight"]
                     + free_miin * core["free_weight"] + penalty)
            scored.append({
                "candidate_name": name,
                "n_segments": len(segs),
                "length_score": round(length_score, 2),
                "position_match": position_match,
                "positions_matched": positions_matched,
                "free_miin": free_miin,
                "penalty": round(penalty, 2),
                "total_score": round(total, 3),
                "occurrences": name_counts[name],
                "first_period": name_meta[name].get("first_period", ""),
                "first_provenience": name_meta[name].get(
                    "first_provenience", ""),
            })
        scored.sort(key=lambda r: (-r["total_score"], -r["occurrences"]))
        top = scored[:top_k]
        n_pos = sum(1 for r in scored if r["position_match"] > 0)
        n_free = sum(1 for r in scored if r["free_miin"] > 0)
        out: dict[str, Any] = {"n_candidates": len(scored)}
        if spec.get("report_renderings_count"):
            out["n_renderings"] = len(renderings)
        out["n_with_position_match"] = n_pos
        out["n_with_free_miin"] = n_free
        out["top_matches"] = top
        if top:
            out["verdict"] = spec.get("verdict_template", "").format(
                n_candidates=len(scored),
                n_renderings=len(renderings),
                n_with_position_match=n_pos,
                n_with_free_miin=n_free,
                top_name=top[0]["candidate_name"],
                top_score=top[0]["total_score"],
                top_occurrences=top[0]["occurrences"],
            )
        else:
            out["verdict"] = spec.get("empty_top_text", "No candidates.")
        return out

    # ePSD2 modes ("pn", "pn_cohorts")
    epsd2_pns = inputs.get(
        spec.get("candidates_input", "epsd2_personal_names")) or []
    if not epsd2_pns or not janabiyah:
        return dict(spec.get("empty_result") or {
            "verdict": "INSUFFICIENT_DATA",
            "n_pns_searched": 0,
            "top_matches": [],
        })
    min_icount = max(1, _safe_int(params.get("min_icount", 1), 1))
    epsd2_pns = [
        p for p in epsd2_pns if int(p.get("icount", 0) or 0) >= min_icount
    ]
    tokens = _rendering_tokens(renderings)
    scored = []
    for pn in epsd2_pns:
        r = _score_pn_forms(
            pn.get("forms", []),
            pn.get("periods", []),
            int(pn.get("icount", 0) or 0),
            pn.get("headword", ""),
            tokens,
            core,
        )
        if r:
            scored.append(r)
    scored.sort(key=lambda r: (-r["total_score"], -r["icount"]))

    if mode == "pn":
        top = scored[:top_k]
        n_pos = sum(1 for r in scored if r["position_match"] > 0)
        n_free = sum(1 for r in scored if r["free_miin"] > 0)
        verdict = spec.get("verdict_template", "").format(
            n_pns_searched=len(scored),
            n_renderings=len(tokens),
            n_with_position_match=n_pos,
            n_with_free_miin=n_free,
        )
        if top:
            verdict += spec.get("verdict_top_template", "").format(
                top_headword=top[0]["headword"],
                top_score=top[0]["total_score"],
                top_icount=top[0]["icount"],
                top_periods=top[0]["periods"],
            )
        else:
            verdict += spec.get("verdict_no_top_text", "No candidates.")
        verdict += spec.get("verdict_suffix", "")
        return {
            "n_pns_searched": len(scored),
            "n_renderings": len(tokens),
            "n_with_position_match": n_pos,
            "n_with_free_miin": n_free,
            "top_matches": top,
            "verdict": verdict,
        }

    # "pn_cohorts": bin the scored entries by best-form segment count.
    default_cohorts = spec.get("cohorts_default") or [[3, 4], [5, 6], [7, 8],
                                                       [9, 99]]
    cohorts_param = params.get("cohorts") or default_cohorts
    if not isinstance(cohorts_param, list):
        cohorts_param = default_cohorts
    cohorts: list = []
    overall_pos = 0
    overall_free = 0
    for pair in cohorts_param:
        try:
            lo, hi = int(pair[0]), int(pair[1])
        except Exception:  # noqa: BLE001
            continue
        label = f"S{lo}-{hi}" if hi < 100 else f"S{lo}+"
        members = [r for r in scored if lo <= r["n_segments"] <= hi]
        if not members:
            cohorts.append({
                "cohort": label,
                "lo": lo, "hi": hi,
                "n_pns": 0,
                "n_with_position_match": 0,
                "n_with_free_miin": 0,
                "hit_rate_position": 0.0,
                "hit_rate_free": 0.0,
                "top_matches": [],
            })
            continue
        n_pos_c = sum(1 for r in members if r["position_match"] > 0)
        n_free_c = sum(1 for r in members if r["free_miin"] > 0)
        overall_pos += n_pos_c
        overall_free += n_free_c
        members_sorted = sorted(
            members, key=lambda r: (-r["total_score"], -r["icount"]))
        cohorts.append({
            "cohort": label,
            "lo": lo, "hi": hi,
            "n_pns": len(members),
            "n_with_position_match": n_pos_c,
            "n_with_free_miin": n_free_c,
            "hit_rate_position": round(n_pos_c / len(members), 4),
            "hit_rate_free": round(n_free_c / len(members), 4),
            "top_matches": members_sorted[:top_k],
        })

    pos_rates = [c["hit_rate_position"] for c in cohorts if c["n_pns"] > 0]
    if pos_rates:
        max_rate = max(pos_rates)
        min_rate = min(pos_rates)
        factor = float(spec.get("concentration_factor", 5.0))
        rises = max_rate > factor * max(1e-6, min_rate)
        peak = max(cohorts, key=lambda c: c["hit_rate_position"])
        verdict = spec.get("verdict_head_template", "").format(
            min_rate=min_rate,
            max_rate=max_rate,
            n_cohorts_tested=len(pos_rates),
        )
        if rises:
            verdict += spec.get("verdict_peak_template", "").format(
                peak_cohort=peak["cohort"],
                peak_rate=peak["hit_rate_position"],
                peak_pos=peak["n_with_position_match"],
                peak_n=peak["n_pns"],
            )
        else:
            verdict += spec.get("verdict_flat_text", "")
    else:
        verdict = spec.get("verdict_empty_text", "")
    return {
        "n_pns_searched": len(scored),
        "n_renderings": len(tokens),
        "n_cohorts": len(cohorts),
        "n_with_position_match_total": overall_pos,
        "n_with_free_miin_total": overall_free,
        "cohorts": cohorts,
        "verdict": verdict,
    }


# ── PersonsAggregator ────────────────────────────────────────────────────────


def persons_aggregator_execute(inputs: dict, params: dict) -> dict:
    """Aggregate person rows into per-name candidate counts.

    Generalised from the four Meluhhan persons extractors
    (Phase-22, the Phase-23 refined extractor, its Phase-24
    near-verbatim copy, and the Phase-25 persons-v3 reporter).
    The shared mechanism is one pass over the rows: count rows
    per candidate name (empty names skipped), collect each
    name's period set, first example line, and — as spec data
    dictates — provenience set, source-pattern set, distinct
    tablet (p_number) set, and segment-count enrichment; then
    emit rows in count order at or above min_freq. What differs
    between the four nodes is data, named in the spec:

    - input_key: which input port carries the rows;
    - the collected field sets (proveniences / patterns /
      distinct tablets / segment counts as booleans);
    - known: {"mode": "set", "names": [...]} confirms rows
      whose lowercased name is in the carried known-names set;
      {"mode": "upstream_flag"} takes each name's known flag
      from its rows' is_known field (any row suffices) and
      reports it per row; {"mode": "none"} reports no
      confirmation;
    - example_line_limit: None (untruncated) or a character cap
      (120 for Phase-24, 160 for Phase-25);
    - the output plan: the count key's name, whether the full
      row list is emitted alongside the top-50, the optional
      second count key, the optional by-pattern distribution
      (counted over ALL rows, empty names included), and the
      verdict template.
    """
    spec: dict[str, Any] = params.get("persons_spec") or {}
    persons = inputs.get(spec.get("input_key", "persons")) or []
    min_freq = _safe_int(params.get("min_freq", 1), 1)
    collect_proveniences = bool(spec.get("collect_proveniences", False))
    collect_patterns = bool(spec.get("collect_patterns", False))
    distinct_tablets = bool(spec.get("distinct_tablets", False))
    segment_count = bool(spec.get("segment_count", False))
    known_spec = spec.get("known") or {"mode": "none"}
    known_mode = known_spec.get("mode", "none")
    known_names = {str(n).lower() for n in known_spec.get("names") or []}
    line_limit = spec.get("example_line_limit")

    name_counts: Counter = Counter()
    name_periods: dict = {}
    name_provs: dict = {}
    name_lines: dict = {}
    name_patterns: dict = {}
    name_tablets: dict = {}
    name_known: dict = {}
    for p in persons:
        n = p.get("candidate_name", "")
        if not n:
            continue
        name_counts[n] += 1
        name_periods.setdefault(n, set()).add(p.get("period", "") or "")
        if collect_proveniences:
            name_provs.setdefault(n, set()).add(p.get("provenience", "") or "")
        name_lines.setdefault(n, []).append(p.get("line", ""))
        if collect_patterns:
            name_patterns.setdefault(n, set()).add(
                p.get("source_pattern", "") or "")
        if distinct_tablets:
            name_tablets.setdefault(n, set()).add(p["p_number"])
        if known_mode == "upstream_flag":
            name_known[n] = name_known.get(n, False) or bool(p.get("is_known"))

    rows: list = []
    for n, c in name_counts.most_common():
        if c < min_freq:
            continue
        line = name_lines[n][0] if name_lines.get(n) else ""
        if line_limit is not None:
            line = line[:int(line_limit)]
        row: dict[str, Any] = {"candidate_name": n, "occurrences": c}
        if distinct_tablets:
            row["n_distinct_tablets"] = len(name_tablets.get(n, set()))
        if segment_count:
            row["n_segments"] = _name_n_segments(n)
        row["periods"] = sorted(name_periods.get(n, set()))
        if collect_proveniences:
            row["proveniences"] = sorted(name_provs.get(n, set()))
        if collect_patterns:
            row["source_patterns"] = sorted(name_patterns.get(n, set()))
        if known_mode == "upstream_flag":
            row["is_known_meluhhan"] = bool(name_known.get(n, False))
        row["example_line"] = line
        rows.append(row)

    if known_mode == "set":
        confirmed = [r for r in rows
                     if r["candidate_name"].lower() in known_names]
    elif known_mode == "upstream_flag":
        confirmed = [r for r in rows if r["is_known_meluhhan"]]
    else:
        confirmed = []

    by_pattern = None
    if spec.get("by_pattern"):
        counter: Counter = Counter()
        for p in persons:
            counter[p.get("source_pattern", "")] += 1
        by_pattern = dict(counter.most_common())

    out: dict[str, Any] = {
        spec.get("n_key", "n_unique"): len(rows),
        "rows_top50": rows[:50],
    }
    if spec.get("rows_all", True):
        out["rows_all"] = rows
    if spec.get("extra_count_key"):
        out[spec["extra_count_key"]] = len(rows)
    if spec.get("confirmed", True):
        out["confirmed_hits"] = confirmed
    if by_pattern is not None:
        out["by_pattern"] = by_pattern
    out["verdict"] = spec.get("verdict_template", "").format(
        n_rows=len(rows),
        min_freq=min_freq,
        n_confirmed=len(confirmed),
        by_pattern=by_pattern,
    )
    return out


# ── Shared helper for the F9 profile engines ─────────────────────────────────


def _entropy_from_counts(counts: Counter) -> float:
    """Plain MLE Shannon entropy in nats of a count distribution."""
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    h = 0.0
    for v in counts.values():
        if v <= 0:
            continue
        p = v / total
        h -= p * math.log(p)
    return h


# ── InteractionSurplusProfile ────────────────────────────────────────────────


def interaction_surplus_profile_execute(inputs: dict, params: dict) -> dict:
    """Profile higher-order n-gram interactions beyond independence.

    Generalised from the Phase-14 EpistaticInteractionDetector.
    For each frequent bigram the score is its PMI (by construction
    the surplus over independence); for each frequent trigram the
    score is the interaction information beyond the pairwise
    baseline, log P(a,b,c) - log[P(a,b) * P(c)]. Scores at or
    above the spec's significance cut are counted as significant.
    The cut is the only fixed content, and it is spec data
    (params["profile_spec"]["significance_cut"], default 2.0
    nats); min counts, top_k, and the label stay plain params.
    """
    spec: dict[str, Any] = params.get("profile_spec") or {}
    cut = float(spec.get("significance_cut", 2.0))
    sequences: list[list[str]] = inputs.get("sequences") or []
    min_count_2 = max(2, int(params.get("min_count_2", 5)))
    min_count_3 = max(2, int(params.get("min_count_3", 3)))
    top_k = max(5, int(params.get("top_k", 25)))
    label = str(params.get("label", "unknown"))

    if not sequences:
        return {"label": label, "bigrams": [], "trigrams": [],
                "verdict": "Empty corpus."}

    uni = _ngram_counts(sequences, 1)
    bi = _ngram_counts(sequences, 2)
    tri = _ngram_counts(sequences, 3)
    n_uni = sum(uni.values()) or 1
    n_bi = sum(bi.values()) or 1
    n_tri = sum(tri.values()) or 1

    bigrams: list[dict] = []
    for (a, b), c in bi.items():
        if c < min_count_2:
            continue
        p_a = uni[(a,)] / n_uni
        p_b = uni[(b,)] / n_uni
        p_ab = c / n_bi
        if p_a <= 0 or p_b <= 0:
            continue
        pmi = math.log(p_ab / (p_a * p_b))
        bigrams.append({"a": a, "b": b, "count": c,
                        "pmi": round(pmi, 4)})

    trigrams: list[dict] = []
    for (a, b, c), n in tri.items():
        if n < min_count_3:
            continue
        p_ab = bi[(a, b)] / n_bi if (a, b) in bi else 0.0
        p_c = uni[(c,)] / n_uni
        p_abc = n / n_tri
        if p_ab <= 0 or p_c <= 0 or p_abc <= 0:
            continue
        surplus = math.log(p_abc / (p_ab * p_c))
        trigrams.append({"a": a, "b": b, "c": c, "count": n,
                         "surplus_3rd": round(surplus, 4)})

    bigrams.sort(key=lambda r: -r["pmi"])
    trigrams.sort(key=lambda r: -r["surplus_3rd"])

    n_significant_2 = sum(1 for r in bigrams if r["pmi"] >= cut)
    n_significant_3 = sum(1 for r in trigrams if r["surplus_3rd"] >= cut)

    return {
        "label": label,
        "bigrams": bigrams[:top_k],
        "trigrams": trigrams[:top_k],
        "n_significant_bigrams": n_significant_2,
        "n_significant_trigrams": n_significant_3,
        "n_total_bigrams_examined": len(bigrams),
        "n_total_trigrams_examined": len(trigrams),
        "verdict": (
            f"{label}: {n_significant_2} bigrams + {n_significant_3} trigrams "
            f"with surplus >= {cut} nats."
        ),
        "json": {
            "label": label,
            "n_significant_2nd": n_significant_2,
            "n_significant_3rd": n_significant_3,
            "top_bigrams": bigrams[:10],
            "top_trigrams": trigrams[:10],
        },
    }


# ── OrderInformationProfile ──────────────────────────────────────────────────


def _rule_matches(metrics: dict[str, float], conditions: list) -> bool:
    for metric, op, threshold in conditions:
        value = metrics.get(metric, 0.0)
        if op == ">=" and not value >= float(threshold):
            return False
        if op == "<" and not value < float(threshold):
            return False
        if op == ">" and not value > float(threshold):
            return False
        if op == "<=" and not value <= float(threshold):
            return False
    return True


def order_information_profile_execute(inputs: dict, params: dict) -> dict:
    """Decompose corpus information by interaction order (HED).

    Generalised from the Phase-14 EpistaticOrderProfile. The
    decomposition is fixed mechanism: per-symbol block entropies
    H(n)/n, successive differences as the order contributions,
    the unigram skew (H_max - H(1)) prepended as order 1. The
    regime classification is a rule table carried as spec data
    (params["profile_spec"]["regime_rules"]: an ordered list of
    {"regime", "conditions": [[metric, op, threshold], ...]}
    over the metrics f2_over_f1 and f3_over_f2, first match
    wins; "fallback_regime" names the regime when no rule
    matches). max_order and the label stay plain params.
    """
    spec: dict[str, Any] = params.get("profile_spec") or {}
    rules: list = spec.get("regime_rules") or []
    fallback = str(spec.get("fallback_regime", "ambiguous"))
    sequences: list[list[str]] = inputs.get("sequences") or []
    max_order = max(2, int(params.get("max_order", 4)))
    label = str(params.get("label", "unknown"))

    if not sequences:
        return {"label": label, "orders": [], "verdict": "Empty corpus."}

    flat = [s for seq in sequences for s in seq]
    n_symbols = len(set(flat))
    h_max = math.log(n_symbols) if n_symbols > 1 else 1.0

    per_symbol: list[float] = []
    for n in range(1, max_order + 2):
        ngrams = _ngram_counts(sequences, n)
        h = _entropy_from_counts(ngrams)
        per_symbol.append(h / n if n > 0 else 0.0)

    orders: list[dict] = []
    total = 0.0
    contribs: list[float] = []
    for k in range(1, max_order + 1):
        prev = per_symbol[k - 1] if k - 1 < len(per_symbol) else 0.0
        cur = per_symbol[k] if k < len(per_symbol) else 0.0
        d = max(0.0, prev - cur)
        contribs.append(d)
        total += d

    base = h_max - per_symbol[0]
    contribs = [base] + contribs
    total += base

    for k, c in enumerate(contribs):
        orders.append({
            "order": k + 1,
            "info_nats": round(c, 4),
            "fraction_of_total": round(c / total, 4) if total > 0 else 0.0,
        })

    f2_over_f1 = orders[1]["fraction_of_total"] / max(1e-9, orders[0]["fraction_of_total"])
    f3_over_f2 = (
        orders[2]["fraction_of_total"] / max(1e-9, orders[1]["fraction_of_total"])
        if len(orders) > 2 else 0.0
    )
    metrics = {"f2_over_f1": f2_over_f1, "f3_over_f2": f3_over_f2}
    regime = fallback
    for rule in rules:
        if _rule_matches(metrics, rule.get("conditions") or []):
            regime = str(rule.get("regime", fallback))
            break

    return {
        "label": label,
        "orders": orders,
        "per_symbol_entropy": [round(v, 4) for v in per_symbol],
        "regime": regime,
        "f2_over_f1": round(f2_over_f1, 4),
        "f3_over_f2": round(f3_over_f2, 4),
        "verdict": (
            f"{label}: HED regime={regime}, 2nd/1st={f2_over_f1:.3f}, "
            f"3rd/2nd={f3_over_f2:.3f}."
        ),
        "json": {
            "label": label,
            "orders": orders,
            "regime": regime,
            "epistatic_2nd_norm": orders[1]["fraction_of_total"] if len(orders) > 1 else 0.0,
            "epistatic_3rd_norm": orders[2]["fraction_of_total"] if len(orders) > 2 else 0.0,
        },
    }


# ── TokenContextAssociation ──────────────────────────────────────────────────


def token_context_association_execute(inputs: dict, params: dict) -> dict:
    """Permutation-tested association between tokens and a context field.

    Generalised from the Phase-14 SignContextAssociation. PMI is
    computed per (token, context) pair over token counts; a
    permutation null shuffles the context array n_perm times and
    recomputes each observed pair's PMI, giving a z-score and a
    surplus over the null mean. The fixed content is spec data
    (params["association_spec"]): the significance cut (default
    2.0), the strong-verdict minimum pair count (default 5), the
    three verdict templates, and the optional length binning —
    "binned_field" names the field whose value is synthesised
    from bins over "bin_source_field" (ordered [upper_bound,
    name] pairs plus a "default_bin"). Field, permutation count,
    seed, min_count, and top_k stay plain params.
    """
    spec: dict[str, Any] = params.get("association_spec") or {}
    cut = float(spec.get("significance_cut", 2.0))
    strong_min = int(spec.get("strong_min", 5))
    templates: dict = spec.get("verdict_templates") or {}
    binned_field = spec.get("binned_field")
    bin_source = spec.get("bin_source_field")
    bins: list = spec.get("bins") or []
    default_bin = str(spec.get("default_bin", "long"))

    sequences: list[list[str]] = inputs.get("sequences") or []
    metadata: list[dict] = inputs.get("metadata") or []
    field = str(params.get("field", "type"))
    n_perm = max(2, int(params.get("n_perm", 8)))
    seed = int(params.get("seed", 11))
    min_count = int(params.get("min_count", 5))
    top_k = int(params.get("top_k", 30))

    if not sequences or not metadata or len(sequences) != len(metadata):
        return {"associations": [], "field": field, "verdict":
                "Sequences and metadata must align (same length)."}

    def _ctx(m: dict) -> str:
        if binned_field and field == binned_field and bin_source:
            n = int(m.get(bin_source) or 0)
            for bound, name in bins:
                if n <= bound:
                    return str(name)
            return default_bin
        return str(m.get(field))

    contexts = [_ctx(m) for m in metadata]

    def _accumulate(ctxs: list[str]):
        sc: Counter = Counter()
        scc: Counter = Counter()
        cc: Counter = Counter()
        nt = 0
        for seq, c in zip(sequences, ctxs):
            for s in seq:
                sc[s] += 1
                scc[(s, c)] += 1
                cc[c] += 1
                nt += 1
        return sc, scc, cc, nt

    sign_count, sign_ctx, ctx_count, n_total = _accumulate(contexts)

    associations: list[dict] = []
    for (s, c), n_sc in sign_ctx.items():
        if n_sc < min_count:
            continue
        p_s = sign_count[s] / n_total
        p_c = ctx_count[c] / n_total
        p_sc = n_sc / n_total
        if p_s <= 0 or p_c <= 0 or p_sc <= 0:
            continue
        pmi = math.log(p_sc / (p_s * p_c))
        associations.append({"sign": s, "context": c, "n": n_sc,
                             "pmi": round(pmi, 4)})

    associations.sort(key=lambda r: -r["pmi"])

    rng = random.Random(seed)
    null_means: dict[tuple[str, str], list[float]] = {}
    for _ in range(n_perm):
        shuffled = list(contexts)
        rng.shuffle(shuffled)
        _, sc_perm, cc_perm, nt_perm = _accumulate(shuffled)
        for r in associations:
            n_sc_perm = sc_perm.get((r["sign"], r["context"]), 0)
            if n_sc_perm < 1 or nt_perm <= 0:
                pmi_perm = 0.0
            else:
                p_s_perm = sign_count[r["sign"]] / nt_perm
                p_c_perm = cc_perm[r["context"]] / nt_perm
                p_sc_perm = n_sc_perm / nt_perm
                if p_s_perm <= 0 or p_c_perm <= 0 or p_sc_perm <= 0:
                    pmi_perm = 0.0
                else:
                    pmi_perm = math.log(p_sc_perm / (p_s_perm * p_c_perm))
            null_means.setdefault((r["sign"], r["context"]), []).append(pmi_perm)

    for r in associations:
        nm = null_means.get((r["sign"], r["context"])) or [0.0]
        mean = sum(nm) / len(nm)
        var = sum((x - mean) ** 2 for x in nm) / max(1, len(nm) - 1)
        std = var ** 0.5
        r["pmi_null_mean"] = round(mean, 4)
        r["pmi_null_std"] = round(std, 4)
        r["pmi_z"] = round((r["pmi"] - mean) / std, 4) if std > 0 else 0.0
        r["surplus_pmi"] = round(r["pmi"] - mean, 4)

    associations.sort(key=lambda r: -r["pmi_z"])
    top = associations[:top_k]

    n_significant = sum(1 for r in associations if r["pmi_z"] >= cut)
    values = _FmtValues({"field": field, "n": n_significant, "cut": cut})
    if n_significant >= strong_min:
        verdict = str(templates.get("strong", "")).format_map(values)
    elif n_significant >= 1:
        verdict = str(templates.get("weak", "")).format_map(values)
    else:
        verdict = str(templates.get("none", "")).format_map(values)

    return {
        "associations": top,
        "n_significant": n_significant,
        "n_total_pairs": len(associations),
        "field": field,
        "verdict": verdict,
        "json": {"top": top, "n_significant": n_significant, "verdict": verdict},
    }


# ── MetricFieldExtractor ─────────────────────────────────────────────────────


def _field_map_read(entry: dict, inputs: dict) -> Any:
    """One field_map extraction entry against the wired inputs.

    An entry with "coerce": "float" returns float(value) — the
    delegating node's numeric reads keep their float shape.
    """
    kind = entry.get("kind", "field")
    default = entry.get("default", 0.0)
    src = inputs.get(entry.get("input", "")) or {}
    value: Any = default
    if kind == "field":
        value = src.get(entry.get("field", ""), default)
    elif kind == "list_first_field":
        rows = src.get(entry.get("list_key", "")) or []
        value = rows[0].get(entry.get("field", ""), default) if rows else default
    elif kind == "list_row_at_n_field":
        rows = src.get(entry.get("list_key", "")) or []
        for row in rows:
            if row.get("n") == entry.get("n"):
                value = row.get(entry.get("field", ""), default)
                break
    elif kind == "list_index_field":
        rows = src.get(entry.get("list_key", "")) or []
        index = int(entry.get("index", 0))
        if len(rows) > index:
            value = rows[index].get(entry.get("field", ""), default)
    if entry.get("coerce") == "float":
        return float(value)
    return value


def metric_field_extractor_execute(inputs: dict, params: dict) -> dict:
    """Extract a flat metric vector from wired analysis bundles.

    Generalised from the Phase-14 DoFExtractor. The mechanism is
    a field map: params["field_map"] is an ordered list of
    extraction entries, each {"out", "kind", "input", ...,
    "default"} — kind "field" reads a field of an input dict,
    "list_first_field" the first row's field of a carried list,
    "list_row_at_n_field" the field of the list row whose n
    equals the entry's n, "list_index_field" the field of the
    list row at an index. The delegating node supplies its
    fixed renaming table as the map's default, which is the
    parameter surface the triage calls for; with no map the
    extraction is empty.
    """
    field_map: list = params.get("field_map") or []
    dof: dict[str, float] = {}
    for entry in field_map:
        dof[str(entry.get("out", ""))] = _field_map_read(entry, inputs)
    return {"dof_values": dof, "n_dofs": len(dof)}


# ── SignatureComparator ──────────────────────────────────────────────────────


_SIGNATURE_FEATURE_KEYS = (
    "alpha", "gamma_mi", "plateau_norm", "epistatic_2", "epistatic_3",
    "h_norm_n3",
)


def _signature_feature_vec(bundle: dict) -> dict[str, float]:
    """Feature dict of a flat signature bundle (fixed mechanism).

    Reads the profiler fields under their primary names with the
    historical fallback names (zipf_alpha / zipf_r2 / gamma /
    r2_pow); the block list rides on the bundle itself.
    """
    block = bundle.get("block_entropies") or []
    h_norm_3 = next((float(e["H_norm"]) for e in block if e.get("n") == 3), 0.0)
    plateau_norm = 0.0
    if block:
        h1 = float(block[0].get("H_nats", 0.0))
        hk = float(block[-1].get("H_nats", 0.0))
        if h1 > 0:
            plateau_norm = hk / (len(block) * h1)
    return {
        "alpha": float(bundle.get("alpha", bundle.get("zipf_alpha", 0.0))),
        "r2_zipf": float(bundle.get("r_squared", bundle.get("zipf_r2", 0.0))),
        "gamma_mi": float(bundle.get("gamma_powerlaw", bundle.get("gamma", 0.0))),
        "r2_pow_mi": float(bundle.get("r2_powerlaw", bundle.get("r2_pow", 0.0))),
        "h_norm_n3": h_norm_3,
        "plateau_norm": plateau_norm,
        "epistatic_2": float(bundle.get("epistatic_2nd_norm", 0.0)),
        "epistatic_3": float(bundle.get("epistatic_3rd_norm", 0.0)),
    }


def signature_comparator_execute(inputs: dict, params: dict) -> dict:
    """Rank signature bundles by closeness to a language template.

    Generalised from the Phase-14 LanguageSignatureComparator.
    Bundles arrive one per port (a..f) in the flat signature
    shape. Classification is spec data (params["comparator_spec"]):
    a bundle is a negative when any of "negative_tags" appears in
    its lowercased label; the candidate when its label equals the
    target, or carries the "candidate_tag" / "candidate_marker"
    substrings; a reference otherwise (and when no reference
    exists, every bundle doubles as a reference). References form
    the language template (per-key mean) and the per-key spread
    normalises the Euclidean distances; candidates and all other
    bundles are ranked by distance to the language template and
    to the negative centroid. The target row's lang-minus-neg
    delta against the "verdict_margin" picks the verdict band;
    the four verdict texts are spec templates. target_label
    stays a plain param.
    """
    spec: dict[str, Any] = params.get("comparator_spec") or {}
    candidate_tag = str(spec.get("candidate_tag", ""))
    candidate_marker = str(spec.get("candidate_marker", "candidate"))
    negative_tags: list = spec.get("negative_tags") or []
    margin = float(spec.get("verdict_margin", 0.25))
    templates: dict = spec.get("verdict_templates") or {}
    keys = tuple(spec.get("feature_keys") or _SIGNATURE_FEATURE_KEYS)

    target_label = str(params.get("target_label", ""))
    bundles: list[dict] = []
    for p in ("a", "b", "c", "d", "e", "f"):
        v = inputs.get(p)
        if isinstance(v, dict):
            bundles.append(v)

    if not bundles:
        return {"ranked": [], "verdict": "No signature bundles supplied."}

    refs: list[dict] = []
    candidates: list[dict] = []
    negatives: list[dict] = []
    for b in bundles:
        lab = str(b.get("label", "")).lower()
        v = _signature_feature_vec(b)
        if any(t in lab for t in negative_tags):
            negatives.append({"label": lab, **v})
        elif lab and (lab == target_label.lower()
                      or (candidate_tag and candidate_tag in lab)
                      or candidate_marker in lab):
            candidates.append({"label": lab, **v})
        else:
            refs.append({"label": lab, **v})

    if not refs:
        refs = [{"label": str(b.get("label", "")).lower(),
                 **_signature_feature_vec(b)} for b in bundles]

    template = {k: sum(r[k] for r in refs) / max(1, len(refs)) for k in keys}
    spread = {
        k: max(1e-6, max(r[k] for r in refs) - min(r[k] for r in refs))
        for k in keys
    }

    def _dist(v: dict[str, float]) -> float:
        return sum(((v[k] - template[k]) / spread[k]) ** 2 for k in keys) ** 0.5

    ranked = []
    for b in bundles:
        v = _signature_feature_vec(b)
        d_lang = _dist(v)
        if negatives:
            t_neg = {k: sum(n[k] for n in negatives) / len(negatives)
                     for k in keys}
            d_neg = sum(((v[k] - t_neg[k]) / spread[k]) ** 2
                        for k in keys) ** 0.5
        else:
            d_neg = float("inf")
        ranked.append({
            "label": str(b.get("label", "")),
            "distance_to_language_template": round(d_lang, 4),
            "distance_to_negative_template": round(d_neg, 4),
            "lang_minus_neg": round(d_lang - d_neg, 4),
            **{k: round(v[k], 4) for k in keys},
        })
    ranked.sort(key=lambda r: r["distance_to_language_template"])

    target_row = next(
        (r for r in ranked if r["label"].lower() == target_label.lower()),
        None,
    )
    if target_row is not None:
        delta = target_row["lang_minus_neg"]
        values = _FmtValues({
            "target": target_label,
            "d_lang": target_row["distance_to_language_template"],
            "d_neg": target_row["distance_to_negative_template"],
            "delta": delta,
        })
        if delta < -margin:
            verdict = str(templates.get("language", "")).format_map(values)
        elif delta > margin:
            verdict = str(templates.get("negative", "")).format_map(values)
        else:
            verdict = str(templates.get("ambiguous", "")).format_map(values)
    else:
        verdict = str(templates.get("no_target",
                                    "No target_label supplied; ranking-only output."))

    return {
        "ranked": ranked,
        "language_template": template,
        "n_references": len(refs),
        "n_candidates": len(candidates),
        "n_negatives": len(negatives),
        "verdict": verdict,
        "json": {"ranked": ranked, "verdict": verdict},
    }


# ── EvidenceRuleAggregator ───────────────────────────────────────────────────


class _FmtValues(dict):
    """Format-map values: a missing numeric field formats as 0."""

    def __missing__(self, key: str) -> float:
        return 0.0


def _rule_values(rule: dict, src: dict) -> _FmtValues:
    """Resolve a rule's named values from its source dict."""
    values = _FmtValues(src)
    for out_name, field in (rule.get("values") or {}).items():
        values[out_name] = src.get(field, 0.0)
    return values


def _evidence_rule_fires(rule: dict, inputs: dict, params: dict) -> list[tuple[str, str]]:
    """Evaluate one aggregator rule; return (side, message) pairs."""
    kind = rule.get("kind", "")
    src = inputs.get(rule.get("input", "")) or {}
    if rule.get("skip_if_input_empty") and not src:
        return []
    if kind == "range_pair":
        a = float(src.get(rule.get("field_a", ""), 0.0) or 0.0)
        b_field = rule.get("field_b", "")
        if b_field in src:
            b = float(src.get(b_field, 0.0) or 0.0)
        else:
            b = float(src.get(rule.get("field_b_fallback", ""), 0.0) or 0.0)
        values = _rule_values(rule, src)
        values[rule.get("field_a", "")] = a
        values[b_field] = b
        lo, hi = (rule.get("a_range") or [0.0, 0.0])
        if lo <= a <= hi and b >= float(rule.get("b_min", 0.0)):
            return [("for", str(rule.get("for_template", "")).format_map(values))]
        if a < float(rule.get("a_floor", 0.0)) or b < float(rule.get("b_floor", 0.0)):
            return [("against", str(rule.get("against_template", "")).format_map(values))]
        return []
    if kind == "field_equals":
        value = src.get(rule.get("field", ""), rule.get("default"))
        if value != rule.get("equals"):
            return []
        side = str(rule.get("side", "for"))
        return [(side, str(rule.get("template", "")).format_map(
            _rule_values(rule, src)))]
    if kind == "list_fraction_checks":
        rows = src.get(rule.get("list_field", "")) or []
        out: list[tuple[str, str]] = []
        for check in rule.get("checks") or []:
            index = int(check.get("index", 0))
            if len(rows) <= index:
                continue
            value = float(rows[index].get(rule.get("value_field", ""), 0) or 0)
            threshold = float(check.get("threshold", 0.0))
            op = check.get("op", ">=")
            fires = value >= threshold if op == ">=" else value < threshold
            if fires:
                values = _FmtValues({"value": value})
                out.append((str(check.get("side", "for")),
                            str(check.get("template", "")).format_map(values)))
        return out
    if kind == "success_threshold":
        value = float(src.get(rule.get("value_field", ""),
                              rule.get("value_default", 1e9)) or 0.0)
        low = float(params.get(rule.get("low_param", ""),
                               rule.get("low_default", 0.1)))
        high = float(params.get(rule.get("high_param", ""),
                                rule.get("high_default", 1.0)))
        values = _FmtValues({"value": value})
        if src.get(rule.get("success_field", "")) and value <= low:
            return [("for", str(rule.get("for_template", "")).format_map(values))]
        if value > high:
            return [("against", str(rule.get("against_template", "")).format_map(values))]
        return []
    return []


def evidence_rule_aggregator_execute(inputs: dict, params: dict) -> dict:
    """Aggregate independent diagnostic verdicts into one judgement.

    Generalised from the Phase-14 LanguageDetectorVerdict. The
    evidence rules are data (params["aggregator_spec"]["rules"],
    evaluated in order): "range_pair" fires for when a primary
    field sits in a range and a secondary field clears its
    floor, against when either falls under its floor;
    "field_equals" fires a fixed line when a field equals a
    carried value; "list_fraction_checks" fires per carried
    index/threshold check over a list field;
    "success_threshold" fires for when a success flag holds
    and a value stays under the low threshold (a plain param
    named by the rule), against when the value exceeds the
    high threshold. The score is for minus against;
    "language_min_score" (default 2) marks the language call;
    the three verdict bands are format templates over the
    counts and confidence, gated by "confidence_threshold"
    (default 0.5).
    """
    spec: dict[str, Any] = params.get("aggregator_spec") or {}
    rules: list = spec.get("rules") or []
    language_min = int(spec.get("language_min_score", 2))
    conf_threshold = float(spec.get("confidence_threshold", 0.5))
    templates: dict = spec.get("verdict_templates") or {}

    for_list: list[str] = []
    against_list: list[str] = []
    for rule in rules:
        for side, message in _evidence_rule_fires(rule, inputs, params):
            (for_list if side == "for" else against_list).append(message)

    score = len(for_list) - len(against_list)
    total = max(1, len(for_list) + len(against_list))
    confidence = abs(score) / total
    is_language = score >= language_min

    values = _FmtValues({
        "n_for": len(for_list), "n_against": len(against_list),
        "confidence": confidence,
    })
    if is_language and confidence >= conf_threshold:
        verdict = str(templates.get("likely_for", "")).format_map(values)
    elif score <= -language_min and confidence >= conf_threshold:
        verdict = str(templates.get("likely_against", "")).format_map(values)
    else:
        verdict = str(templates.get("ambiguous", "")).format_map(values)

    return {
        "is_language": is_language,
        "confidence": round(confidence, 3),
        "score": score,
        "evidence_for": for_list,
        "evidence_against": against_list,
        "verdict": verdict,
        "json": {
            "is_language": is_language,
            "confidence": confidence,
            "score": score,
            "evidence_for": for_list,
            "evidence_against": against_list,
            "verdict": verdict,
        },
    }


# ── PositionalClassClassifier ────────────────────────────────────────────────


def positional_class_classifier_execute(inputs: dict, params: dict) -> dict:
    """Classify signs by their within-sequence position profile.

    Generalised from the Phase-20 FulsPositionalClassifier.
    Position counts are index-based (first token initial, last
    token terminal, a length-1 token both), rates normalise over
    the position-count total, and the repetition rate counts
    adjacent same-sign successors over tokens that have a
    successor. Classification is spec data
    (params["classifier_spec"]): the numerical class fires when
    the repetition rate reaches the numerical threshold;
    otherwise the ordered "position_classes" rules apply — each
    names a label key and a dominant position (I / M / T) whose
    rate must reach the dominance threshold while both other
    positions stay below the secondary threshold — and the
    fallback label classifies the rest. The label set
    ("class_labels": numerical / initial / medial / terminal /
    mixed) and the verdict template are spec data; the
    thresholds themselves stay plain params.
    """
    spec: dict[str, Any] = params.get("classifier_spec") or {}
    labels: dict = spec.get("class_labels") or {}
    position_classes: list = spec.get("position_classes") or []
    verdict_template = str(spec.get("verdict_template", ""))
    sequences: list[list[str]] = inputs.get("sequences") or []
    min_count = int(params.get("min_count", 5))
    dom_threshold = float(params.get("dom_threshold", 0.55))
    secondary = float(params.get("secondary_threshold", 0.30))
    numerical_rr = float(params.get("numerical_rr", 0.20))

    pos: dict[str, dict[str, int]] = {}
    freq: Counter = Counter()
    rep_counts: Counter = Counter()
    rep_total: Counter = Counter()
    for seq in sequences:
        n = len(seq)
        for i, s in enumerate(seq):
            freq[s] += 1
            row = pos.setdefault(s, {"I": 0, "M": 0, "T": 0})
            if n == 1:
                row["I"] += 1
                row["T"] += 1
            elif i == 0:
                row["I"] += 1
            elif i == n - 1:
                row["T"] += 1
            else:
                row["M"] += 1
            if i + 1 < n:
                rep_total[s] += 1
                if seq[i + 1] == s:
                    rep_counts[s] += 1

    eligible = [s for s, c in freq.items() if c >= min_count]
    table: list[dict] = []
    counts_by_class: Counter = Counter()
    for s in eligible:
        pc = pos[s]
        tot = pc["I"] + pc["M"] + pc["T"]
        if tot <= 0:
            continue
        rates = {"I": pc["I"] / tot, "M": pc["M"] / tot, "T": pc["T"] / tot}
        rr = (rep_counts[s] / rep_total[s]) if rep_total[s] > 0 else 0.0
        if rr >= numerical_rr:
            cls = str(labels.get("numerical", "NUMERICAL"))
        else:
            cls = str(labels.get("mixed", "MIXED"))
            for rule in position_classes:
                dominant = str(rule.get("dominant", ""))
                others = [p for p in ("I", "M", "T") if p != dominant]
                if (rates.get(dominant, 0.0) >= dom_threshold
                        and all(rates[o] < secondary for o in others)):
                    cls = str(labels.get(str(rule.get("label_key", "")), cls))
                    break
        counts_by_class[cls] += 1
        table.append({
            "sign": s, "freq": freq[s],
            "I_rate": round(rates["I"], 3), "M_rate": round(rates["M"], 3),
            "T_rate": round(rates["T"], 3),
            "repetition_rate": round(rr, 3),
            "class": cls,
        })

    table.sort(key=lambda r: (-r["freq"], r["sign"]))
    n = sum(counts_by_class.values())
    fractions = {k: round(v / max(1, n), 3) for k, v in counts_by_class.items()}
    n_logo = counts_by_class.get(str(labels.get("initial", "INITIAL")), 0) \
        + counts_by_class.get(str(labels.get("terminal", "TERMINAL")), 0)
    n_syll = counts_by_class.get(str(labels.get("medial", "MEDIAL")), 0) \
        + counts_by_class.get(str(labels.get("mixed", "MIXED")), 0)
    values = _FmtValues({
        "n": n, "fractions": fractions,
        "n_logo": n_logo, "n_syll": n_syll,
        "n_numerical": counts_by_class.get(str(labels.get("numerical", "NUMERICAL")), 0),
    })
    for label in labels.values():
        values[str(label)] = label
    verdict = verdict_template.format_map(values) if verdict_template else ""
    return {
        "params": {"min_count": min_count, "dom_threshold": dom_threshold,
                   "secondary_threshold": secondary, "numerical_rr": numerical_rr},
        "n_signs_classified": n,
        "counts_by_class": dict(counts_by_class),
        "fractions_by_class": fractions,
        "table": table,
        "verdict": verdict,
    }


# ── SignPositionNullTest ─────────────────────────────────────────────────────


def sign_position_null_test_execute(inputs: dict, params: dict) -> dict:
    """Test a sign's positional bias against a shuffle null.

    Generalised from the Indus-evidence IndusNullModelTest
    (Fuls-style positional-preference test). The observed rate of
    the target sign at the tested edge (initial, or terminal for
    any other test type) is compared against n_null_runs shuffled
    re-deals of every sequence; the z-score uses the population
    standard deviation of the null rates, the p-value is the
    one-sided share of null rates at or above the observed rate
    (floored at 1/n_null), and the verdict maps |z| through the
    spec's band table (params["null_spec"]: "verdict_bands" as
    ordered [|z| threshold, verdict] pairs, first match wins,
    "verdict_fallback" when none matches). The triage's caution
    is honoured: this is a sequence-shaped test and deliberately
    does NOT reuse the score-shaped generic PermutationTest.
    Target sign, test type, run count, and seed stay plain
    params; the RNG stream is the seeded global stream, as the
    original node's was.
    """
    spec: dict[str, Any] = params.get("null_spec") or {}
    bands: list = spec.get("verdict_bands") or []
    fallback = str(spec.get("verdict_fallback", "NOT_SIGNIFICANT"))
    sequences: list[list[str]] = inputs.get("sequences") or []
    if not sequences:
        return {"error": "No sequences — connect BuiltinCorpus or CorpusReader.sequences"}

    target_sign = str(params.get("target_sign", "") or "").strip()
    n_null = int(params.get("n_null_runs", 1000) or 1000)
    test_type = str(params.get("test_type", "initial") or "initial").lower()
    random.seed(int(params.get("random_seed", 42) or 42))

    if not target_sign:
        return {"error": "Set target_sign parameter to the sign to test (e.g. 'M77/72')"}

    flat = [s for seq in sequences for s in seq]
    tc = Counter(flat)
    if tc.get(target_sign, 0) == 0:
        return {"error": f"Sign '{target_sign}' not found in corpus"}

    def _obs_rate(seqs: list) -> float:
        if test_type == "initial":
            return sum(1 for seq in seqs if seq and seq[0] == target_sign) / max(len(seqs), 1)
        return sum(1 for seq in seqs if seq and seq[-1] == target_sign) / max(len(seqs), 1)

    observed = _obs_rate(sequences)

    null_rates: list[float] = []
    for _ in range(n_null):
        shuffled = [random.sample(seq, len(seq)) for seq in sequences]
        null_rates.append(_obs_rate(shuffled))

    null_mean = sum(null_rates) / len(null_rates)
    null_std = math.sqrt(
        sum((r - null_mean) ** 2 for r in null_rates) / max(len(null_rates), 1))
    z_score = (observed - null_mean) / max(null_std, 1e-9)
    p_approx = max(sum(1 for r in null_rates if r >= observed) / n_null, 1 / n_null)

    verdict = fallback
    for threshold, band_verdict in bands:
        if abs(z_score) >= float(threshold):
            verdict = str(band_verdict)
            break

    return {
        "sign": target_sign,
        "test_type": test_type,
        "observed_rate": round(observed, 5),
        "null_mean": round(null_mean, 5),
        "null_std": round(null_std, 6),
        "z_score": round(z_score, 3),
        "p_approx": round(p_approx, 4),
        "n_null_runs": n_null,
        "verdict": verdict,
        "number": round(z_score, 3),
        "json": {"sign": target_sign, "z_score": z_score, "verdict": verdict},
        "text": (f"Null model ({test_type}): {target_sign} z={z_score:.2f} "
                 f"p≈{p_approx:.3f} → {verdict}."),
    }


# ── PositionalClaimTester ───────────────────────────────────────────────────
# Spec 087 S3 PR-F (family F2). Tests claims of spec-named types against a
# sequence corpus: a claim is testable when its type contains one of the
# spec's keywords, it names at least one sign, and its normalized text
# names a position (the first matching position needle wins). For each of
# the claim's first `sign_cap` signs present in the corpus, the observed
# positional rate (positional occurrences / total occurrences, positional
# counts taken over sequences longer than `positional_min_length`) is
# compared against the corpus average rate over signs with at least
# `min_count_for_avg` occurrences, scaled by `support_multiplier`.
# Claims that fail any testability condition are skipped — the engine
# emits no row for them, exactly as the evidence tester it generalises.


def positional_claim_tester_execute(inputs: dict, params: dict) -> dict:
    spec = dict(params.get("tester_spec") or {})
    claims = inputs.get("claims") or []
    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"error": spec["no_sequences_error"]}
    if not claims:
        return {"error": spec["no_claims_error"]}

    keywords = spec.get("type_keywords") or []
    positions = spec.get("positions") or [["initial", "initial"],
                                          ["terminal", "terminal"]]
    min_len = spec.get("positional_min_length", 1)
    min_count = spec.get("min_count_for_avg", 3)
    multiplier = spec.get("support_multiplier", 1.2)
    sign_cap = spec.get("sign_cap", 4)
    truncate = spec.get("source_truncate", 100)
    round_obs = spec.get("round_observed", 4)
    round_avg = spec.get("round_average", 4)
    round_lift = spec.get("round_lift", 3)
    lift_floor = spec.get("lift_floor", 0.001)
    round_rate = spec.get("round_support_rate", 4)

    tc = Counter(s for seq in sequences for s in seq)
    ic = Counter(seq[0] for seq in sequences if len(seq) > min_len)
    te = Counter(seq[-1] for seq in sequences if len(seq) > min_len)
    counters = {label: (ic if label == "initial" else te)
                for _needle, label in positions}

    results: list[dict] = []
    for claim in claims:
        ct = claim.get("claim_type", "")
        if not any(k in ct for k in keywords):
            continue
        signs = claim.get("signs_involved") or []
        nc = claim.get("normalized_claim", "")
        pred_pos = None
        for needle, label in positions:
            if needle in nc.lower():
                pred_pos = label
                break
        if not signs or not pred_pos:
            continue
        pos_counter = counters[pred_pos]
        frequent = [s for s in tc if tc[s] >= min_count]
        avg_rate = (sum(pos_counter[s] / max(tc[s], 1) for s in frequent)
                    / max(len(frequent), 1))
        for sign in signs[:sign_cap]:
            n = tc.get(sign, 0)
            if n == 0:
                continue
            obs_rate = pos_counter[sign] / n
            supported = obs_rate >= avg_rate * multiplier
            results.append({
                "claim_id": claim.get("claim_id", ""),
                "sign": sign,
                "predicted_pos": pred_pos,
                "observed_rate": round(obs_rate, round_obs),
                "corpus_avg_rate": round(avg_rate, round_avg),
                "lift": round(obs_rate / max(avg_rate, lift_floor), round_lift),
                "n_occurrences": n,
                "test_verdict": (spec.get("supported_verdict", "supported")
                                 if supported else
                                 spec.get("unsupported_verdict", "not_supported")),
                "source_claim": nc[:truncate],
            })

    n_supp = sum(1 for r in results
                 if r["test_verdict"] == spec.get("supported_verdict", "supported"))
    n_total = len(results)
    support_rate = round(n_supp / max(n_total, 1), round_rate)
    return {
        "test_results": results,
        "n_tested": n_total,
        "n_supported": n_supp,
        "support_rate": support_rate,
        "json": {"test_results": results},
        "number": support_rate,
        "text": spec["text_template"].format(
            n_total=n_total, n_supp=n_supp,
            pct=round(100 * n_supp / max(n_total, 1))),
    }
