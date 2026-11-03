"""Generic corpus / dataset loader machinery (Spec 087 S3, family F1).

Two spec-driven loader engines back the generic primitives
``JsonCorpusLoader`` and ``DatasetRecordLoader`` (registered in
experiment_graph.py). The domain loaders converted in Spec 087 S3
(M77InscriptionLoader, ICITCorpusLoader, MathematicaEpigraphicaLoader,
MahadevanInscriptionLoader, EPSD2NamesLoader, ContactCorpusLoader)
keep their registered ids and parameter schemas; their
implementations delegate here with the domain content — corpus
identity, file paths, getter names, field mappings, verdict text —
carried in a declarative *spec* dict instead of in code. That is the
conversion contract: generic mechanism in this module, domain
content in parameters.

JsonCorpusLoader spec (params["corpus_spec"], or flat params):

  sources        fallback chain of file sources; the first existing
                 file wins. Each source: {"kind": "json", "path": ...}
                 or {"kind": "csv_grouped", "path": ..., "group_key",
                 "order_key", "value_key", "site_field"}.
  records_key    key holding the record list in a JSON source
                 (default "inscriptions"); a JSON top-level list is
                 unwrapped to its first element, as the M77 report is.
  field_map      for the sequence_corpus projection:
                 {"id", "site", "sequence", "raw"} record field names.
  projection     "sequence_corpus" (sequences + per-inscription
                 metadata + counts), "record_list" (records passed
                 through + a top-sites counter), or "cache_summary"
                 (record count + a count field + a metadata block).
  parse_error    "raise" (default) or "return" (an
                 {"available": False, "error": "parse error: ..."}
                 result, the cache loaders' historical shape).
  absent_result  result returned when no source exists; string
                 values are templates (see below).
  verdict_template / behaviour params (use_raw, min_length,
                 max_length, label) as in the domain loaders;
                 behavior_defaults carries a delegating node's
                 historical defaults for those params as spec data.

DatasetRecordLoader spec (params["dataset_spec"]):

  module         dotted path of a glossa_lab.data module.
  getters        {alias: {"name": getter_name, "kwargs": {kw:
                 {"from_param": param, "default": v, "safe_int": b,
                 "min": m, "max": M} or {"value": v}}}} — getters are
                 called once, in spec order.
  filters        [{"from": alias, "as": view_name, "rules": [...]}];
                 rule kinds: "substring_ci" (param needle in a record
                 field), "any_substring_ci" (needle in any item of a
                 list field), "equals" (record field == param value,
                 applied only when the param is non-empty).
  outputs        ordered assembly ops over the getter results and
                 filtered views: "value", "len", "sum_len",
                 "distinct_count", "counter_top", "echo_param",
                 "literal", and "verdict" (a template; see below).

Templates: "{name}" and "{dotted.name}" placeholders resolve from a
context of node params + outputs assembled so far + computed values;
a missing dotted leaf renders "?" (mirroring the historical
``md.get(key, '?')`` behaviour of the converted verdicts). Extra
context entries on a verdict op may be literals, param echoes, or
conditional templates (rendered only when a named param is
non-empty).
"""
from __future__ import annotations

import csv
import importlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

_PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_.]*)\}")


def _fill(template: str, context: dict[str, Any]) -> str:
    """Render {name} / {dotted.name} placeholders from a context dict.

    A missing leaf renders "?" — the converted loaders' verdicts were
    built with dict.get(key, '?') defaults, so absence is text, not an
    exception. Present values render with str(), as an f-string did.
    """

    def resolve(match: re.Match[str]) -> str:
        parts = match.group(1).split(".")
        current: Any = context
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return "?"
        return str(current)

    return _PLACEHOLDER_RE.sub(resolve, template)


def _fill_result(result: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Fill every string value of a result template dict."""
    return {
        key: (_fill(value, context) if isinstance(value, str) else value)
        for key, value in result.items()
    }


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── JsonCorpusLoader ────────────────────────────────────────────────────────


def _spec_from_flat_params(params: dict[str, Any]) -> dict[str, Any]:
    """Build a JsonCorpusLoader spec from flat node params (direct use)."""
    data_path = params.get("data_path") or ""
    return {
        "sources": [{"kind": "json", "path": str(data_path)}] if data_path else [],
        "records_key": params.get("records_key", "inscriptions"),
        "field_map": params.get("field_map") or {},
        "projection": params.get("projection", "sequence_corpus"),
        "parse_error": params.get("parse_error", "raise"),
        "data_path_display": str(data_path),
        "absent_result": {
            "available": False,
            "n_inscriptions": 0,
            "verdict": "Corpus not available at {data_path}.",
        },
    }


def _json_records(path: Path, parse_error: str) -> Any:
    """Parse a JSON source file; return (holder, error_result).

    The holder is the mapping the records live in: a top-level list is
    unwrapped to its first element (the decoded M77 report's shape).
    """
    if parse_error == "return":
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            return None, {"available": False, "error": f"parse error: {exc}"}
    else:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    holder = parsed[0] if isinstance(parsed, list) else parsed
    return holder, None


def _csv_grouped_records(source: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    """Read a grouped CSV source into unified records.

    Rows are grouped by the group key (first-seen order), sorted by the
    order key, and each group becomes one record whose sequence is the
    rows' value column. Mirrors the Holdat fallback of the historical
    M77 loader exactly.
    """
    group_key = source.get("group_key", "cisi_number")
    order_key = source.get("order_key", "position")
    value_key = source.get("value_key", "letters")
    site_field = source.get("site_field", "site")
    groups: dict[str, list[dict]] = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            groups[row[group_key]].append(row)
    records: list[dict[str, Any]] = []
    for group_value, rows in groups.items():
        rows_sorted = sorted(rows, key=lambda r: int(r.get(order_key) or 0))
        records.append(
            {
                "id": group_value,
                "site": rows_sorted[0].get(site_field, ""),
                "sequence": [r[value_key] for r in rows_sorted if r.get(value_key)],
                "_has_raw": False,
            }
        )
    return records


def _project_sequence_corpus(
    records: list[dict[str, Any]],
    params: dict[str, Any],
    source_path: Path,
    defaults: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The sequence-corpus projection: filtered sequences + metadata.

    Behaviour values resolve params -> the spec's behavior_defaults ->
    the engine's generic defaults, so a delegating domain node keeps
    its historical defaults (e.g. M77's label) as spec data.
    """
    defaults = defaults or {}
    use_raw = bool(params.get("use_raw", defaults.get("use_raw", False)))
    min_length = int(params.get("min_length", defaults.get("min_length", 1)))
    max_length = int(params.get("max_length", defaults.get("max_length", 0)))
    label = str(params.get("label", defaults.get("label", "corpus")))

    inscriptions: list[dict[str, Any]] = []
    sequences: list[list[str]] = []
    for record in records:
        if use_raw and record.get("_has_raw"):
            seq_str = record.get("raw") or ""
            seq = [c for c in seq_str if c and not c.isspace()]
        else:
            seq = list(record.get("sequence") or [])
        length = len(seq)
        if length < min_length:
            continue
        if max_length > 0 and length > max_length:
            continue
        inscriptions.append(
            {
                "id": record.get("id"),
                "site_code": record.get("site"),
                "length": length,
                "sequence": seq,
            }
        )
        sequences.append(seq)

    flat = [sign for seq in sequences for sign in seq]
    return {
        "label": label,
        "use_raw": use_raw,
        "n_inscriptions": len(inscriptions),
        "n_tokens": len(flat),
        "n_distinct_signs": len(set(flat)),
        "sequences": sequences,
        "inscriptions": inscriptions,
        "source": str(source_path),
    }


def json_corpus_loader_execute(inputs: dict, params: dict) -> dict:
    """JsonCorpusLoader engine: fallback chain + field map + projection."""
    spec = params.get("corpus_spec") or _spec_from_flat_params(params)
    sources: list[dict[str, Any]] = spec.get("sources") or []
    records_key = spec.get("records_key", "inscriptions")
    parse_error = spec.get("parse_error", "raise")
    projection = spec.get("projection", "sequence_corpus")

    winning: dict[str, Any] | None = None
    winning_path: Path | None = None
    for source in sources:
        candidate = Path(source["path"])
        if candidate.exists():
            winning, winning_path = source, candidate
            break

    context: dict[str, Any] = {
        "data_path": spec.get(
            "data_path_display", sources[0]["path"] if sources else ""
        ),
        "source_path": str(Path(sources[0]["path"])) if sources else "",
        "source_name": Path(sources[0]["path"]).name if sources else "",
        "fallback_path": str(Path(sources[1]["path"])) if len(sources) > 1 else "",
    }
    if winning is None or winning_path is None:
        return _fill_result(spec.get("absent_result") or {"available": False}, context)

    context["source_path"] = str(winning_path)
    context["source_name"] = winning_path.name

    behavior_defaults = spec.get("behavior_defaults") or {}
    if winning.get("kind") == "csv_grouped":
        records = _csv_grouped_records(winning, winning_path)
        return _project_sequence_corpus(
            records, params, winning_path, behavior_defaults
        )

    holder, error = _json_records(winning_path, parse_error)
    if error is not None:
        return error

    if projection == "sequence_corpus":
        field_map = {
            "id": "id",
            "site": "site_code",
            "sequence": "sequence",
            "raw": "raw",
            **(spec.get("field_map") or {}),
        }
        coerce_site = bool(winning.get("site_coerce_str", spec.get("site_coerce_str")))
        raw_records = holder.get(records_key) or []
        records = []
        for entry in raw_records:
            site_value = entry.get(field_map["site"], "")
            records.append(
                {
                    "id": entry.get(field_map["id"]),
                    "site": str(site_value) if coerce_site else site_value,
                    "sequence": entry.get(field_map["sequence"]),
                    "raw": entry.get(field_map["raw"]),
                    # Raw mode applies to every JSON-source record: a
                    # record without raw text yields an empty sequence
                    # (the primary branch's entry.get("raw") or "").
                    # Only the grouped-CSV records carry _has_raw False —
                    # the CSV fallback ignores use_raw entirely.
                    "_has_raw": True,
                }
            )
        return _project_sequence_corpus(
            records, params, winning_path, behavior_defaults
        )

    if projection == "record_list":
        records = holder.get(records_key) or []
        site_field = spec.get("site_field", "site")
        sites: Counter = Counter()
        for record in records:
            site = (record.get(site_field) or "").upper()
            if site:
                sites[site] += 1
        context.update(
            {"n_inscriptions": len(records), "n_sites": len(sites)}
        )
        return {
            "available": True,
            "n_inscriptions": len(records),
            "inscriptions": records,
            "sites_top": sites.most_common(spec.get("sites_top_n", 10)),
            "verdict": _fill(spec.get("verdict_template", ""), context),
        }

    if projection == "cache_summary":
        records = holder.get(records_key) or []
        context.update({"n_inscriptions": len(records)})
        return {
            "available": True,
            "n_inscriptions": len(records),
            "n_signs": holder.get(spec.get("count_field", "n_signs"), 0),
            "metadata": holder.get(spec.get("metadata_key", "metadata"), {}),
            "verdict": _fill(spec.get("verdict_template", ""), context),
        }

    return {"error": f"JsonCorpusLoader: unknown projection {projection!r}"}


# ── DatasetRecordLoader ─────────────────────────────────────────────────────


def _getter_kwargs(rule: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    for kwarg, kwarg_rule in (rule.get("kwargs") or {}).items():
        if "from_param" not in kwarg_rule:
            kwargs[kwarg] = kwarg_rule.get("value")
            continue
        value = params.get(kwarg_rule["from_param"], kwarg_rule.get("default"))
        if kwarg_rule.get("safe_int"):
            value = _safe_int(value, kwarg_rule.get("default", 0))
        if "min" in kwarg_rule:
            value = max(kwarg_rule["min"], value)
        if "max" in kwarg_rule:
            value = min(kwarg_rule["max"], value)
        kwargs[kwarg] = value
    return kwargs


def _rule_keeps(rule: dict[str, Any], record: dict, params: dict[str, Any]) -> bool:
    kind = rule["kind"]
    field = rule["field"]
    if kind == "substring_ci":
        needle = (params.get(rule["param"]) or "").strip().lower()
        if not needle:
            return True
        return needle in (record.get(field, "")).lower()
    if kind == "any_substring_ci":
        needle = (params.get(rule["param"]) or "").strip().lower()
        if not needle:
            return True
        return any(needle in item.lower() for item in (record.get(field) or []))
    if kind == "equals":
        value = params.get(rule["param"]) or ""
        if not value:
            return True
        return record.get(field) == value
    raise ValueError(f"DatasetRecordLoader: unknown filter rule kind {kind!r}")


def _verdict_context(
    op: dict[str, Any], params: dict[str, Any], outputs: dict[str, Any]
) -> dict[str, Any]:
    context: dict[str, Any] = {**outputs, **params}
    for name, entry in (op.get("context") or {}).items():
        if "template" in entry:
            when = entry.get("when") or {}
            gate = when.get("param_nonempty")
            if gate is not None and not (params.get(gate) or ""):
                context[name] = ""
            else:
                context[name] = _fill(entry["template"], context)
        elif "from_param" in entry:
            context[name] = params.get(entry["from_param"])
        else:
            context[name] = entry.get("value")
    return context


def dataset_record_loader_execute(inputs: dict, params: dict) -> dict:
    """DatasetRecordLoader engine: named getters + filters + assembly."""
    spec = params.get("dataset_spec")
    if spec is None:
        spec = {
            key: params[key]
            for key in ("module", "getters", "filters", "outputs")
            if key in params
        }
    if "module" not in spec or "getters" not in spec:
        return {
            "error": "DatasetRecordLoader requires a dataset_spec param "
            "(module, getters, outputs)"
        }

    try:
        module = importlib.import_module(spec["module"])
        getters = {
            alias: getattr(module, rule["name"])
            for alias, rule in spec["getters"].items()
        }
    except Exception as exc:  # noqa: BLE001
        template = spec.get(
            "import_error_template", "data module not available: {error}"
        )
        return {"error": _fill(template, {"error": str(exc)})}

    views: dict[str, Any] = {}
    for alias, rule in spec["getters"].items():
        views[alias] = getters[alias](**_getter_kwargs(rule, params))

    for filter_spec in spec.get("filters") or []:
        source_view = views[filter_spec["from"]]
        rules = filter_spec["rules"]
        views[filter_spec["as"]] = [
            record
            for record in source_view
            if all(_rule_keeps(rule, record, params) for rule in rules)
        ]

    outputs: dict[str, Any] = {}
    for op in spec.get("outputs") or []:
        kind = op["op"]
        key = op["key"]
        if kind == "value":
            outputs[key] = views[op["of"]]
        elif kind == "len":
            outputs[key] = len(views[op["of"]])
        elif kind == "sum_len":
            outputs[key] = sum(len(item) for item in views[op["of"]])
        elif kind == "distinct_count":
            outputs[key] = len(
                {sign for item in views[op["of"]] for sign in item}
            )
        elif kind == "counter_top":
            counter = Counter(
                sign for item in views[op["of"]] for sign in item
            )
            outputs[key] = counter.most_common(op.get("n", 20))
        elif kind == "echo_param":
            value = params.get(op["param"]) or ""
            outputs[key] = value if value else op.get("empty_value", "")
        elif kind == "literal":
            outputs[key] = op.get("value")
        elif kind == "verdict":
            outputs[key] = _fill(
                op["template"], _verdict_context(op, params, outputs)
            )
        else:
            return {"error": f"DatasetRecordLoader: unknown output op {kind!r}"}
    return outputs
