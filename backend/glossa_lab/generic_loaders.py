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

  sources        chain of file sources; the first existing file wins
                 among the eligible sources. Each source:
                 {"kind": "json", "path": ...} or {"kind":
                 "csv_grouped", "path": ..., "group_key", "order_key",
                 "value_key", "site_field"}. A source may carry a
                 "name" and "explicit_only": an explicit-only source is
                 never picked up by the default chain — it serves only
                 when named through source_select_param (Spec 087 S3
                 fallback retirement: no silent substitution).
  source_select_param
                 optional name of a node param that selects one source
                 by its "name". When the param is present, the chain is
                 restricted to the named source (an unknown name is an
                 explicit error); when it is absent, explicit-only
                 sources are skipped.
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
    rows' value column. Mirrors the Holdat path of the M77 loader
    exactly (the silent fallback before Spec 087 S3; an explicit
    source selection since the fallback retirement).
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
    """JsonCorpusLoader engine: source chain + field map + projection."""
    spec = params.get("corpus_spec") or _spec_from_flat_params(params)
    sources: list[dict[str, Any]] = spec.get("sources") or []
    records_key = spec.get("records_key", "inscriptions")
    parse_error = spec.get("parse_error", "raise")
    projection = spec.get("projection", "sequence_corpus")

    # Source eligibility (Spec 087 S3): when the spec names a select
    # param and the caller set it, the chain is exactly the named
    # source — an explicit choice is honoured exactly, never widened.
    # Without a selection, explicit-only sources are skipped, so no
    # corpus is ever substituted silently for the default source.
    select_param = spec.get("source_select_param")
    selected = params.get(select_param) if select_param else None
    if selected is not None:
        eligible = [s for s in sources if s.get("name") == selected]
        if not eligible:
            choices = ", ".join(
                str(s["name"]) for s in sources if s.get("name")
            )
            return {
                "error": (
                    f"JsonCorpusLoader: unknown source {selected!r}; "
                    f"choose one of: {choices}"
                )
            }
    else:
        eligible = [s for s in sources if not s.get("explicit_only")]

    winning: dict[str, Any] | None = None
    winning_path: Path | None = None
    for source in eligible:
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
                    # the CSV (Holdat) path ignores use_raw entirely.
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


# ── JsonRecordDirLoader ─────────────────────────────────────────────────────
# Spec 087 S3 PR-F (family F2). A directory of one-JSON-record-per-file
# documents, in two modes:
#
#   "search"  — project each parseable record through a field map, with an
#               optional substring query over two named fields and an
#               optional cross-reference count read from a sibling
#               directory's per-record files.
#   "records" — flatten the item lists of every parseable record file
#               (optionally restricted to the files named by an upstream
#               input), applying param-driven filters, per-field value
#               counts, and a cap.
#
# The spec carries the domain specifics (directory, field names, filter
# wiring, count fields, text templates); the engine is the machinery.
# Unparseable files are skipped silently in both modes — the behaviour of
# the evidence loaders this engine generalises.


def _record_dir_files(directory: str, ensure_dir: bool) -> list[Path]:
    root = Path(directory)
    if ensure_dir:
        root.mkdir(parents=True, exist_ok=True)
    return sorted(root.glob("*.json"))


def _project_record(record: dict, stem: str, projection: list[dict]) -> dict:
    out: dict[str, Any] = {}
    for entry in projection:
        if "stem" in entry:
            out[entry["out"]] = stem
        elif entry.get("default_stem"):
            out[entry["out"]] = record.get(entry["from"], stem)
        else:
            out[entry["out"]] = record.get(entry["from"], entry.get("default"))
    return out


def _cross_ref_count(record: dict, stem: str, count_from: dict) -> Any:
    name = record.get(count_from["key_field"], stem)
    target = Path(count_from["directory"]) / f"{name}.json"
    default = count_from.get("default", 0)
    if not target.exists():
        return default
    try:
        return json.loads(target.read_text("utf-8")).get(
            count_from["value_field"], default)
    except Exception:  # noqa: BLE001
        return default


def _record_dir_search(inputs: dict, params: dict, spec: dict) -> dict:
    q = str(params.get(spec.get("query_param", "query"), "") or "").lower()
    max_items = int(params.get(spec.get("max_param", "max_items"),
                               spec.get("max_default", 200)) or spec.get("max_default", 200))
    title_field = spec["search_title_field"]
    authors_field = spec["search_authors_field"]
    items: list[dict[str, Any]] = []
    for f in _record_dir_files(spec["directory"], spec.get("ensure_dir", False)):
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if q:
            hay = ((d.get(title_field) or "") + " "
                   + " ".join(d.get(authors_field) or [])).lower()
            if q not in hay:
                continue
        row = _project_record(d, f.stem, spec["projection"])
        if "count_from" in spec:
            row[spec["count_from"]["out"]] = _cross_ref_count(
                d, f.stem, spec["count_from"])
        items.append(row)
        if len(items) >= max_items:
            break
    out = {spec.get("items_key", "items"): items,
           spec.get("count_key", "total"): len(items)}
    if "text_template" in spec:
        out["text"] = _fill(spec["text_template"], {"n": len(items)})
    return out


def _record_filter_keeps(claim: dict, filters: list[dict], params: dict) -> bool:
    for flt in filters:
        kind = flt["kind"]
        if kind == "equals":
            value = str(params.get(flt["param"], "") or "").strip()
            if value and claim.get(flt["field"]) != value:
                return False
        elif kind == "substring_any":
            needle = str(params.get(flt["param"], "") or "").lower().strip()
            if needle:
                hit = False
                for field in flt["fields"]:
                    raw = claim.get(field)
                    hay = (" ".join(raw) if isinstance(raw, list)
                           else (raw or ""))
                    if needle in str(hay).lower():
                        hit = True
                        break
                if not hit:
                    return False
    return True


def _record_dir_records(inputs: dict, params: dict, spec: dict) -> dict:
    max_items = int(params.get(spec.get("max_param", "max_items"),
                               spec.get("max_default", 500)) or spec.get("max_default", 500))
    restrict = spec.get("restrict") or {}
    upstream = inputs.get(restrict.get("input_key", "")) or []
    allowed = None
    if restrict and upstream:
        allowed = {p.get(restrict.get("id_field", "document_id"), "")
                   for p in upstream}
    defaults = spec.get("schema_defaults") or {}
    items: list[dict] = []
    source_files: list[str] = []
    for f in _record_dir_files(spec["directory"], spec.get("ensure_dir", False)):
        if allowed is not None and f.stem not in allowed:
            continue
        try:
            record = json.loads(f.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        source_files.append(f.stem)
        for raw_item in record.get(spec.get("items_key", "items"), []):
            item = {**defaults, **raw_item} if defaults else raw_item
            if not _record_filter_keeps(item, spec.get("filters") or [], params):
                continue
            items.append(item)
            if len(items) >= max_items:
                break
        if len(items) >= max_items:
            break
    out: dict[str, Any] = {spec.get("out_items_key", "items"): items,
                           spec.get("count_key", "total"): len(items),
                           spec.get("sources_key", "source_docs"): len(source_files)}
    counts: dict[str, dict[str, int]] = {}
    for count_spec in spec.get("counts") or []:
        table: dict[str, int] = {}
        field = count_spec["field"]
        default = count_spec.get("default", "unknown")
        for item in items:
            key = item.get(field, default)
            table[key] = table.get(key, 0) + 1
        counts[count_spec["out"]] = table
        out[count_spec["out"]] = table
    if "json_counts" in spec:
        embedded = {spec.get("out_items_key", "items"): items}
        for name in spec["json_counts"]:
            embedded[name] = counts[name]
        out["json"] = embedded
    if "text_template" in spec:
        context = {"n": len(items), "n_sources": len(source_files)}
        types_from = (spec.get("text_types") or {}).get("from_counts")
        if types_from:
            table = counts[types_from]
            limit = (spec.get("text_types") or {}).get("limit", 5)
            context["types"] = ", ".join(
                f"{k}={v}" for k, v in sorted(table.items())[:limit])
        out["text"] = _fill(spec["text_template"], context)
    return out


def json_record_dir_loader_execute(inputs: dict, params: dict) -> dict:
    """JsonRecordDirLoader engine: see the section header above."""
    spec = dict(params.get("loader_spec") or {})
    if spec.get("mode") == "records":
        return _record_dir_records(inputs, params, spec)
    return _record_dir_search(inputs, params, spec)
