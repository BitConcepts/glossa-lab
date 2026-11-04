"""Spec 087 Stage S4 — the generated manual blocks (T401).

One generation feeds every manual surface, under the Spec 086
discipline (one source of truth, generated downstream, a gate on
drift) applied to the node registry:

- the Node Reference block in ``docs/user-manual.md`` (delimited),
- the HelpView node-reference data module
  (``frontend/src/components/help/nodeReference.generated.ts``),
- the active-experiments block in ``docs/USER_GUIDE.md``
  (delimited, generated from the graph files on disk).

The node model comes from the LIVE registry
(``glossa_lab.experiment_graph.ATOMIC_NODES``): exactly the
palette set of claim C087-4 (registered-minus-legacy), with each
node's category, ports, and params as the registry states them
(C087-8). The experiments model comes from the graph JSON files
under ``backend/glossa_lab/experiments/graphs/`` (``_archive/``
excluded), so USER_GUIDE's list is the files on disk, neither
more nor fewer (C087-9).

The generator refuses to write outside its delimited blocks: a
target whose begin/end markers are missing, duplicated, or out
of order is a named refusal and nothing is written at all (all
outputs are built in memory before any file is touched).

This module is the pure builder; the CLI wrapper is
``tools/manual/generate_node_reference.py`` and the CI gate is
``backend/tests/test_manual_conformance.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

BEGIN_NODE_REFERENCE = "<!-- BEGIN GENERATED node-reference -->"
END_NODE_REFERENCE = "<!-- END GENERATED node-reference -->"
BEGIN_EXPERIMENTS = "<!-- BEGIN GENERATED experiments-table -->"
END_EXPERIMENTS = "<!-- END GENERATED experiments-table -->"

GENERATOR_REL = "tools/manual/generate_node_reference.py"

USER_MANUAL_REL = "docs/user-manual.md"
USER_GUIDE_REL = "docs/USER_GUIDE.md"
HELPVIEW_MODULE_REL = "frontend/src/components/help/nodeReference.generated.ts"
GRAPHS_REL = "backend/glossa_lab/experiments/graphs"


class ManualBuildError(Exception):
    """A named refusal: the generation cannot proceed as specified."""


# ── The model ────────────────────────────────────────────────────────────────


def _collapse(text: str) -> str:
    return " ".join(str(text).split())


def _norm_port(port: dict) -> dict:
    return {
        "name": str(port["name"]),
        "type": str(port["type"]),
        "required": bool(port.get("required", False)),
    }


def _norm_params(schema: object) -> list[dict]:
    """Normalize a node's params_schema to a flat param list.

    Two shapes exist in the registry: a JSON-schema object with a
    ``properties`` dict (130 of 131 palette nodes at S4 build), and
    one flat dict that IS the properties dict (ResearchLoopRunner).
    Declared order is preserved — it is the author's order, and the
    registry build is deterministic, so regeneration is stable.
    """
    if not isinstance(schema, dict) or not schema:
        return []
    props = schema.get("properties")
    if not isinstance(props, dict):
        props = schema
    params: list[dict] = []
    for name, spec in props.items():
        if not isinstance(spec, dict):
            spec = {}
        params.append(
            {
                "name": str(name),
                "type": str(spec.get("type", "any")),
                "has_default": "default" in spec,
                "default": spec.get("default"),
                "description": _collapse(
                    spec.get("description") or spec.get("title") or ""
                ),
            }
        )
    return params


def build_node_model() -> tuple[list[dict], dict]:
    """The palette set from the live registry, sorted for output."""
    from glossa_lab.experiment_graph import ATOMIC_NODES

    palette = [d for d in ATOMIC_NODES.values() if not d.legacy]
    model = [
        {
            "id": d.id,
            "name": d.name,
            "category": d.category,
            "description": _collapse(d.description),
            "inputs": [_norm_port(p) for p in d.inputs],
            "outputs": [_norm_port(p) for p in d.outputs],
            "params": _norm_params(d.params_schema),
        }
        for d in palette
    ]
    model.sort(key=lambda n: (n["category"], n["id"]))
    counts = {
        "registered": len(ATOMIC_NODES),
        "legacy": len(ATOMIC_NODES) - len(palette),
        "palette": len(palette),
        "categories": len({n["category"] for n in model}),
    }
    return model, counts


def build_experiments_model(root: Path) -> list[dict]:
    """The registered graph experiments, from the files on disk."""
    graphs_dir = root / GRAPHS_REL
    if not graphs_dir.is_dir():
        raise ManualBuildError(f"graph directory not found: {graphs_dir}")
    model: list[dict] = []
    for path in sorted(graphs_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ManualBuildError(
                f"cannot read graph file {path.name}: {exc}"
            ) from exc
        model.append(
            {
                "id": str(data.get("id") or path.stem),
                "name": _collapse(data.get("name") or path.stem),
                "description": _collapse(data.get("description") or ""),
                "nodes": len(data.get("nodes") or []),
            }
        )
    model.sort(key=lambda e: e["id"])
    return model


# ── Renderers (one model, three surfaces) ────────────────────────────────────


def _fmt_default(param: dict) -> str:
    if not param["has_default"]:
        return ""
    rendered = json.dumps(param["default"], ensure_ascii=False)
    return f", default `{rendered}`"


def _fmt_ports(ports: list[dict], *, mark_required: bool) -> str:
    if not ports:
        return "none"
    parts = []
    for port in ports:
        label = f"`{port['name']}` ({port['type']}"
        if mark_required and port["required"]:
            label += ", required"
        parts.append(label + ")")
    return ", ".join(parts)


def render_node_markdown(model: list[dict], counts: dict) -> str:
    """The shared per-node markdown layout (manual block + HelpView)."""
    lines = [
        f"Palette: **{counts['palette']} nodes** in "
        f"{counts['categories']} categories · registry: "
        f"{counts['registered']} registered / {counts['legacy']} legacy "
        "(legacy nodes are excluded — they stay resolvable for saved "
        "experiments but are not offered in the palette).",
        "",
    ]
    category: str | None = None
    for node in model:
        if node["category"] != category:
            category = node["category"]
            lines += [f"#### {category}", ""]
        lines += [
            f"**`{node['id']}` — {node['name']}**",
            "",
            node["description"],
            "",
            f"- Inputs: {_fmt_ports(node['inputs'], mark_required=True)}",
            f"- Outputs: {_fmt_ports(node['outputs'], mark_required=False)}",
        ]
        if node["params"]:
            lines.append("- Params:")
            for param in node["params"]:
                line = (
                    f"  - `{param['name']}` ({param['type']}"
                    f"{_fmt_default(param)})"
                )
                if param["description"]:
                    line += f" — {param['description']}"
                lines.append(line)
        else:
            lines.append("- Params: none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_experiments_markdown(model: list[dict]) -> str:
    def cell(text: str) -> str:
        return text.replace("|", "\\|")

    lines = [
        f"Registered graph experiments on disk: **{len(model)}**.",
        "",
        "| ID | Experiment | Nodes | Description |",
        "|---|---|---|---|",
    ]
    for exp in model:
        lines.append(
            f"| `{exp['id']}` | {cell(exp['name'])} | {exp['nodes']} "
            f"| {cell(exp['description'])} |"
        )
    return "\n".join(lines) + "\n"


def render_helpview_module(model: list[dict], counts: dict) -> str:
    header = (
        "/**\n"
        " * GENERATED by tools/manual/generate_node_reference.py —\n"
        " * do not edit. Source of truth: the live node registry\n"
        " * (backend/glossa_lab/experiment_graph.py ATOMIC_NODES,\n"
        " * palette set = registered-minus-legacy, Spec 087 S4).\n"
        " * Regenerate: python tools/manual/generate_node_reference.py\n"
        " * Drift is a CI failure (backend/tests/"
        "test_manual_conformance.py).\n"
        " */\n"
    )
    types = (
        "export interface NodeReferencePort {\n"
        "  name: string;\n"
        "  type: string;\n"
        "  required: boolean;\n"
        "}\n\n"
        "export interface NodeReferenceParam {\n"
        "  name: string;\n"
        "  type: string;\n"
        "  hasDefault: boolean;\n"
        "  default: unknown;\n"
        "  description: string;\n"
        "}\n\n"
        "export interface NodeReferenceEntry {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  category: string;\n"
        "  description: string;\n"
        "  inputs: NodeReferencePort[];\n"
        "  outputs: NodeReferencePort[];\n"
        "  params: NodeReferenceParam[];\n"
        "}\n\n"
    )
    ts_model = [
        {
            "id": n["id"],
            "name": n["name"],
            "category": n["category"],
            "description": n["description"],
            "inputs": n["inputs"],
            "outputs": n["outputs"],
            "params": [
                {
                    "name": p["name"],
                    "type": p["type"],
                    "hasDefault": p["has_default"],
                    "default": p["default"],
                    "description": p["description"],
                }
                for p in n["params"]
            ],
        }
        for n in model
    ]
    body = json.dumps(ts_model, indent=2, ensure_ascii=False)
    counts_body = json.dumps(
        {
            "registered": counts["registered"],
            "legacy": counts["legacy"],
            "palette": counts["palette"],
        },
        indent=2,
    )
    return (
        header
        + "\n"
        + types
        + f"export const NODE_REFERENCE: NodeReferenceEntry[] = {body};\n\n"
        + "export const NODE_REFERENCE_COUNTS = "
        + f"{counts_body} as const;\n"
    )


# ── Splicing + whole-file builds ─────────────────────────────────────────────


def _splice(text: str, begin: str, end: str, body: str, label: str) -> str:
    """Replace the content between the unique begin/end marker lines.

    Refuses (ManualBuildError) unless exactly one begin and one end
    marker exist, in order — the generator never writes outside its
    delimited blocks and never guesses.
    """
    lines = text.split("\n")
    begins = [i for i, line in enumerate(lines) if line.strip() == begin]
    ends = [i for i, line in enumerate(lines) if line.strip() == end]
    if len(begins) != 1 or len(ends) != 1 or ends[0] <= begins[0]:
        raise ManualBuildError(
            f"{label}: expected exactly one '{begin}' line before one "
            f"'{end}' line; found {len(begins)} begin / {len(ends)} end"
        )
    body_lines = body.rstrip("\n").split("\n")
    return "\n".join(lines[: begins[0] + 1] + body_lines + lines[ends[0]:])


def build_outputs(root: Path) -> dict[Path, str]:
    """Build the full new text of every generated surface, in memory."""
    model, counts = build_node_model()
    experiments = build_experiments_model(root)

    manual_path = root / USER_MANUAL_REL
    guide_path = root / USER_GUIDE_REL
    module_path = root / HELPVIEW_MODULE_REL
    for path in (manual_path, guide_path):
        if not path.is_file():
            raise ManualBuildError(f"manual surface not found: {path}")

    manual_text = manual_path.read_text(encoding="utf-8")
    guide_text = guide_path.read_text(encoding="utf-8")
    return {
        manual_path: _splice(
            manual_text,
            BEGIN_NODE_REFERENCE,
            END_NODE_REFERENCE,
            render_node_markdown(model, counts),
            USER_MANUAL_REL,
        ),
        guide_path: _splice(
            guide_text,
            BEGIN_EXPERIMENTS,
            END_EXPERIMENTS,
            render_experiments_markdown(experiments),
            USER_GUIDE_REL,
        ),
        module_path: render_helpview_module(model, counts),
    }


def check_outputs(root: Path) -> list[str]:
    """Names of surfaces whose committed bytes differ from a fresh build."""
    drifted: list[str] = []
    for path, fresh in build_outputs(root).items():
        if not path.is_file() or path.read_bytes() != fresh.encode("utf-8"):
            drifted.append(str(path.relative_to(root)))
    return drifted


def write_outputs(root: Path) -> list[str]:
    """Write every surface (all builds succeed first, or none is written)."""
    outputs = build_outputs(root)
    written: list[str] = []
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        written.append(str(path.relative_to(root)))
    return written
