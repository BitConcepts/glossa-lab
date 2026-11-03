"""Generic graph-node machinery (Spec 087 S3, families F3 + F8
and F4 + F5).

Fifteen spec/parameter-driven engines back the generic primitives
registered in experiment_graph.py: RegistryTableLoader,
LabelMapApplier, TemplateMiner, ClusterContingencyProfile,
SignRoleClassifier, ValueRoleMapSource, AnchorSyllabifier,
AssociationAnchorDeriver, and PMICentralityRanker (PR-B), plus
IconographicAnchorScorer, PhonemeMapCoverage,
PhonemeMapPermutationTest, LengthMatchScorer,
LengthMatchPermutationTest, and StratifiedPermutationTest
(PR-C). The domain nodes converted in Spec 087 S3 PR-B
(CanonicalSignLoader, ClusterMapper, StructuralTemplateAnalyzer,
ClusterArchaeology, IndusSignRoleClassifier,
DefaultIndusValueRoleMap, IndusAnchorSetSyllable,
DerivedAnchorSet, EpistaticAnchorRanker) and PR-C
(IconographicAnchorScore, AllographAwareIconographicScore,
BlindHeldOutTest, BayesianDecoder, BayesianDecoderV2,
EnhancedNameMatcher, EnhancedNameMatcherV2, MeluhhaNameMatcher,
BilingualReadoutTest, BilingualReadoutTestV2,
PeriodStratifiedReadout, PeriodStratifiedReadout6Bucket,
ProvenienceStratifiedReadout) keep their registered ids and
parameter schemas; their implementations delegate here with the
domain content — table names, file paths, numeral sets,
value-role tables, diacritic tables, alias tables, strata rules,
verdict text — carried as parameters instead of code. That is
the conversion contract: generic mechanism in this module,
domain content in parameters.

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
