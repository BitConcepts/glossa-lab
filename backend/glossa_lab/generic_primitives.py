"""Generic graph-node machinery (Spec 087 S3, families F3 + F8).

Nine spec/parameter-driven engines back the generic primitives
registered in experiment_graph.py: RegistryTableLoader,
LabelMapApplier, TemplateMiner, ClusterContingencyProfile,
SignRoleClassifier, ValueRoleMapSource, AnchorSyllabifier,
AssociationAnchorDeriver, and PMICentralityRanker. The domain
nodes converted in Spec 087 S3 PR-B (CanonicalSignLoader,
ClusterMapper, StructuralTemplateAnalyzer, ClusterArchaeology,
IndusSignRoleClassifier, DefaultIndusValueRoleMap,
IndusAnchorSetSyllable, DerivedAnchorSet, EpistaticAnchorRanker)
keep their registered ids and parameter schemas; their
implementations delegate here with the domain content — table
names, file paths, numeral sets, value-role tables, diacritic
tables, verdict text — carried as parameters instead of code.
That is the conversion contract: generic mechanism in this
module, domain content in parameters.

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
"""
from __future__ import annotations

import importlib
import json
import logging
import math
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
