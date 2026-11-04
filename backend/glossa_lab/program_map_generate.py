"""Spec 088 Stage S1 — the generated program map (T103).

The whole-program picture of Spec 088, under the Spec 086
discipline (one source of truth, generated downstream, a
gate on drift) applied to the program itself:

- one node per ledger claim and one per study (spec
  directory), grouped by the curated taxonomy;
- every standing derived mechanically from the ledger under
  ``program-map-defs v1``
  (``glossa-indus/map/PROGRAM-MAP-DEFINITIONS.md``) — the
  builder reads the ledger, the taxonomy, and the spec
  tree's directory names, and nothing else (C2: no prose
  standings, ever);
- coverage is total, exact, and fail-closed: a duplicate,
  omissions, unknown ids, undeclared domains/subdomains,
  unregistered statuses, and in-flight emission are each a
  named refusal and nothing is written.

This module is the pure builder; the CLI wrapper is
``tools/map/generate_program_map.py``. The committed
artifacts (``program-map.json``, ``program-map-finds.json``)
land in Stage S2; the Spec 086 gate gains the independent
recomputation (class V10) in Stage S3.
"""

from __future__ import annotations

import json
from pathlib import Path

from glossa_lab.ledger_intake import sha256_file

DEFS_VERSION = "program-map-defs v1"
TAXONOMY_VERSION = "program-map-taxonomy v1"
LEDGER_SCHEMA_VERSION = "ledger-schema v1"

LEDGER_REL = "glossa-indus/ledger/claims.jsonl"
TAXONOMY_REL = "glossa-indus/map/program-map-taxonomy.json"
MAP_REL = "glossa-indus/map/program-map.json"
FINDS_REL = "glossa-indus/map/program-map-finds.json"
SPECS_REL = "specs"

# program-map-defs v1 §4.2 — the derivation table (D-088-3).
# A machine copy of the registered table; the defs document
# is the registration of record, and the Stage 3 gate will
# carry its own copies. A status outside this table fails
# the build.
STATUS_TO_CLASS = {
    "strongly_supported": "positive",
    "contradicted": "negative",
    "unsupported": "negative",
    "partially_falsified": "negative",
    "superseded": "closed_other",
    "draft": "open",
    "untested": "open",
    "partially_supported": "open",
}

CLAIM_CLASSES = ("positive", "negative", "open", "closed_other")
STUDY_CLASSES = CLAIM_CLASSES + ("unjudged",)
IN_FLIGHT = "in_flight"

# program-map-defs v1 §7 — the registered name-only forms.
RESTRICTED_NAME_ONLY = {
    "072-fish-family-profiles-redesign": "executed — held under the Roif gate",
}

# program-map-defs v1 §8 — keys the taxonomy format must
# never carry, anywhere, at any depth (no standings by
# construction, C088-17).
FORBIDDEN_TAXONOMY_KEYS = frozenset(
    {
        "standing",
        "standing_text",
        "status",
        "class",
        "verdict",
        "score",
        "curated",
    }
)

# program-map-defs v1 §6 — the find kinds.
FIND_BUNDLE_LESS_STUDY = "bundle_less_study"
FIND_JUDGMENT_CALL = "judgment_call"
FIND_EXTRACTED_NULL_FALSIFIER = "extracted_null_falsifier"
FIND_RESTRICTED_NODE = "restricted_node"

_STANDING_TEMPLATE = (
    "Ledger standing: status {status} · stage {stage} · falsifier {falsifier}"
)


class ProgramMapBuildError(Exception):
    """A named refusal: the generation cannot proceed as specified."""


# ── Inputs ───────────────────────────────────────────────────────────────────


def _read_ledger(root: Path) -> list[dict]:
    path = root / LEDGER_REL
    if not path.is_file():
        raise ProgramMapBuildError(f"ledger not found: {path}")
    rows: list[dict] = []
    for lineno, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ProgramMapBuildError(
                f"ledger line {lineno} is not JSON: {exc}"
            ) from exc
    return rows


def _spec_dirs(root: Path) -> list[str]:
    specs = root / SPECS_REL
    if not specs.is_dir():
        raise ProgramMapBuildError(f"spec tree not found: {specs}")
    return sorted(p.name for p in specs.iterdir() if p.is_dir())


def _walk_keys(value: object, trail: str = "$") -> list[str]:
    """Every mapping key in a parsed JSON value, with its path."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, sub in value.items():
            found.append(f"{trail}.{key}")
            found.extend(_walk_keys(sub, f"{trail}.{key}"))
    elif isinstance(value, list):
        for i, sub in enumerate(value):
            found.extend(_walk_keys(sub, f"{trail}[{i}]"))
    return found


def _read_taxonomy(root: Path) -> dict:
    path = root / TAXONOMY_REL
    if not path.is_file():
        raise ProgramMapBuildError(f"taxonomy not found: {path}")
    try:
        tax = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProgramMapBuildError(f"taxonomy is not JSON: {exc}") from exc
    if not isinstance(tax, dict):
        raise ProgramMapBuildError("taxonomy is not a JSON object")
    for key_path in _walk_keys(tax):
        key = key_path.rsplit(".", 1)[-1].split("[")[0]
        if key in FORBIDDEN_TAXONOMY_KEYS:
            raise ProgramMapBuildError(
                f"taxonomy carries the forbidden standing-shaped key "
                f"{key!r} at {key_path} (defs §8: the format carries "
                "no standings)"
            )
    if tax.get("version") != TAXONOMY_VERSION:
        raise ProgramMapBuildError(
            f"taxonomy version is {tax.get('version')!r}, expected "
            f"{TAXONOMY_VERSION!r}"
        )
    domains = tax.get("domains")
    if (
        not isinstance(domains, list)
        or not domains
        or len(set(domains)) != len(domains)
        or not all(isinstance(d, str) and d for d in domains)
    ):
        raise ProgramMapBuildError(
            "taxonomy 'domains' must be a non-empty list of unique names"
        )
    subdomains = tax.get("subdomains")
    if not isinstance(subdomains, dict) or set(subdomains) != set(domains):
        raise ProgramMapBuildError(
            "taxonomy 'subdomains' must declare exactly the domains"
        )
    for domain in domains:
        subs = subdomains[domain]
        if (
            not isinstance(subs, list)
            or not subs
            or len(set(subs)) != len(subs)
            or not all(isinstance(s, str) and s for s in subs)
        ):
            raise ProgramMapBuildError(
                f"taxonomy subdomains for {domain!r} must be a non-empty "
                "list of unique names"
            )

    def _assignments(kind: str, id_key: str) -> dict[str, dict]:
        raw = tax.get(kind)
        if not isinstance(raw, list):
            raise ProgramMapBuildError(f"taxonomy {kind!r} must be a list")
        out: dict[str, dict] = {}
        for entry in raw:
            if not isinstance(entry, dict) or set(entry) != {
                id_key,
                "domain",
                "subdomain",
            }:
                raise ProgramMapBuildError(
                    f"taxonomy {kind} entry must carry exactly "
                    f"{{{id_key}, domain, subdomain}}: {entry!r}"
                )
            ident = entry[id_key]
            if ident in out:
                raise ProgramMapBuildError(
                    f"taxonomy assigns {ident!r} more than once ({kind})"
                )
            if entry["domain"] not in domains:
                raise ProgramMapBuildError(
                    f"taxonomy assigns {ident!r} to the undeclared domain "
                    f"{entry['domain']!r}"
                )
            if entry["subdomain"] not in subdomains[entry["domain"]]:
                raise ProgramMapBuildError(
                    f"taxonomy assigns {ident!r} to "
                    f"{entry['subdomain']!r}, not declared under "
                    f"{entry['domain']!r}"
                )
            out[ident] = entry
        return out

    studies = _assignments("studies", "spec_dir")
    documents = _assignments("extracted_documents", "document")
    restricted = tax.get("restricted")
    if not isinstance(restricted, list) or not all(
        isinstance(r, str) for r in restricted
    ):
        raise ProgramMapBuildError("taxonomy 'restricted' must be a list")
    if len(set(restricted)) != len(restricted):
        raise ProgramMapBuildError("taxonomy 'restricted' has duplicates")
    for spec_dir in restricted:
        if spec_dir not in studies:
            raise ProgramMapBuildError(
                f"restricted study {spec_dir!r} has no taxonomy assignment"
            )
        if spec_dir not in RESTRICTED_NAME_ONLY:
            raise ProgramMapBuildError(
                f"restricted study {spec_dir!r} has no registered "
                "name-only form (defs §7)"
            )
    return {
        "domains": domains,
        "subdomains": subdomains,
        "studies": studies,
        "documents": documents,
        "restricted": list(restricted),
    }


# ── Derivation ───────────────────────────────────────────────────────────────


def _governing_entries(rows: list[dict]) -> list[dict]:
    """Claim entries with reclassification chains applied (defs §3)."""
    claims: dict[str, dict] = {}
    order: list[str] = []
    for row in rows:
        if row.get("kind") != "claim":
            continue
        cid = row.get("id")
        if cid in claims:
            raise ProgramMapBuildError(f"duplicate claim id in ledger: {cid}")
        claims[cid] = dict(row)
        order.append(cid)
    for row in rows:
        if row.get("kind") != "reclassification":
            continue
        target = row.get("supersedes")
        if target not in claims:
            raise ProgramMapBuildError(
                f"reclassification {row.get('id')!r} supersedes "
                f"{target!r}, which is not a claim entry"
            )
        for field in ("status", "stage"):
            if field in row:
                claims[target][field] = row[field]
    return [claims[cid] for cid in order]


def _falsifier_present(entry: dict) -> bool:
    return bool(entry.get("falsifier"))


def _derive_class(entry: dict) -> str:
    status = entry.get("status")
    if status not in STATUS_TO_CLASS:
        raise ProgramMapBuildError(
            f"claim {entry.get('id')!r} carries the unregistered status "
            f"{status!r} (defs §4.2: the derivation table is total over "
            "the registered vocabulary; anything else fails the build)"
        )
    cls = STATUS_TO_CLASS[status]
    if cls == IN_FLIGHT:
        raise ProgramMapBuildError(
            f"claim {entry.get('id')!r} derived the in_flight class, "
            "which has no derivation rule in v1 (defs §11)"
        )
    return cls


def _source_of_record(entry: dict) -> dict:
    sors = [
        s
        for s in entry.get("sources") or []
        if isinstance(s, dict) and s.get("role") == "source_of_record"
    ]
    if len(sors) != 1:
        raise ProgramMapBuildError(
            f"claim {entry.get('id')!r} has {len(sors)} source-of-record "
            "sources; exactly one is required to place it"
        )
    return sors[0]


def _roll_up(counts: dict[str, int]) -> tuple[str, bool]:
    """The defs §5 precedence. Returns (class, is_judgment_call)."""
    total = sum(counts.values())
    if total == 0:
        return "unjudged", False
    if counts["positive"] > 0 and counts["negative"] > 0:
        return "open", True
    if counts["closed_other"] == total:
        return "closed_other", False
    if counts["negative"] > 0:
        return "negative", False
    if counts["positive"] > 0:
        return "positive", False
    return "open", False


# ── The build ────────────────────────────────────────────────────────────────


def _dump(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def build_artifacts(root: Path) -> dict[str, str]:
    """Build both artifacts' text in memory, from the defs' inputs only."""
    rows = _read_ledger(root)
    tax = _read_taxonomy(root)
    spec_dirs = _spec_dirs(root)

    # Coverage over the taxonomy is exact and bidirectional (defs §8).
    assigned = set(tax["studies"])
    actual = set(spec_dirs)
    if assigned != actual:
        problems = []
        if actual - assigned:
            problems.append(
                f"spec directories with no assignment: "
                f"{sorted(actual - assigned)}"
            )
        if assigned - actual:
            problems.append(
                f"assignments naming no directory: "
                f"{sorted(assigned - actual)}"
            )
        raise ProgramMapBuildError("; ".join(problems))

    entries = _governing_entries(rows)
    dates = [str(r.get("date")) for r in rows if r.get("date")]
    stamp = {
        "ledger_latest_entry_date": max(dates) if dates else None,
        "ledger_lines": len(rows),
        "ledger_schema": LEDGER_SCHEMA_VERSION,
        "ledger_sha256": sha256_file(root / LEDGER_REL),
        "program_map_defs": DEFS_VERSION,
        "program_map_taxonomy": TAXONOMY_VERSION,
    }

    claim_nodes: list[dict] = []
    members: dict[str, list[str]] = {d: [] for d in spec_dirs}
    multi_spec_claims: list[str] = []
    null_falsifier_extracted: list[dict] = []
    falsifier_present_count = 0
    documents_seen: set[str] = set()

    for entry in entries:
        cls = _derive_class(entry)
        present = _falsifier_present(entry)
        if present:
            falsifier_present_count += 1
        standing = _STANDING_TEMPLATE.format(
            status=entry.get("status"),
            stage=entry.get("stage") if entry.get("stage") else "none",
            falsifier="present" if present else "absent",
        )
        node = {
            "class": cls,
            "document": None,
            "domain": None,
            "falsifier_present": present,
            "id": entry.get("id"),
            "kind": "claim",
            "population": entry.get("population"),
            "stage": entry.get("stage"),
            "standing": standing,
            "status": entry.get("status"),
            "study": None,
            "subdomain": None,
        }
        population = entry.get("population")
        if population == "bundle":
            home = _source_of_record(entry).get("spec")
            if not home or home not in actual:
                raise ProgramMapBuildError(
                    f"bundle claim {entry.get('id')!r} names the home "
                    f"study {home!r}, which is not a spec directory "
                    "(citation does not resolve)"
                )
            specs_named = {
                s.get("spec")
                for s in entry.get("sources") or []
                if isinstance(s, dict) and s.get("spec")
            }
            if len(specs_named) > 1:
                multi_spec_claims.append(entry["id"])
            assignment = tax["studies"][home]
            node["study"] = home
            node["domain"] = assignment["domain"]
            node["subdomain"] = assignment["subdomain"]
            members[home].append(cls)
        elif population == "extracted":
            document = _source_of_record(entry).get("document_id")
            if not document or document not in tax["documents"]:
                raise ProgramMapBuildError(
                    f"extracted claim {entry.get('id')!r} names the "
                    f"source document {document!r}, which has no "
                    "taxonomy assignment"
                )
            documents_seen.add(document)
            assignment = tax["documents"][document]
            node["document"] = document
            node["domain"] = assignment["domain"]
            node["subdomain"] = assignment["subdomain"]
            if not present:
                null_falsifier_extracted.append(
                    {"document": document, "id": entry["id"]}
                )
        else:
            raise ProgramMapBuildError(
                f"claim {entry.get('id')!r} has population "
                f"{population!r}, which has no registered assignment "
                "route in program-map-defs v1 (§4.1)"
            )
        claim_nodes.append(node)

    unassigned_documents = set(tax["documents"]) - documents_seen
    if unassigned_documents:
        raise ProgramMapBuildError(
            "taxonomy assigns extracted documents the ledger does not "
            f"carry: {sorted(unassigned_documents)}"
        )

    restricted = set(tax["restricted"])
    study_nodes: list[dict] = []
    finds: list[dict] = []
    unjudged_studies: list[str] = []
    judgment_calls: list[str] = []
    for spec_dir in spec_dirs:
        assignment = tax["studies"][spec_dir]
        if spec_dir in restricted:
            study_nodes.append(
                {
                    "class": None,
                    "domain": assignment["domain"],
                    "id": spec_dir,
                    "kind": "study",
                    "restricted": True,
                    "standing": RESTRICTED_NAME_ONLY[spec_dir],
                    "subdomain": assignment["subdomain"],
                }
            )
            finds.append({"kind": FIND_RESTRICTED_NODE, "subject": spec_dir})
            continue
        counts = {cls: 0 for cls in CLAIM_CLASSES}
        for cls in members[spec_dir]:
            counts[cls] += 1
        cls, is_judgment = _roll_up(counts)
        if cls == IN_FLIGHT:
            raise ProgramMapBuildError(
                f"study {spec_dir!r} derived the in_flight class, which "
                "has no derivation rule in v1 (defs §11)"
            )
        study_nodes.append(
            {
                "class": cls,
                "domain": assignment["domain"],
                "id": spec_dir,
                "judgment_call": is_judgment,
                "kind": "study",
                "member_counts": {**counts, "total": sum(counts.values())},
                "restricted": False,
                "subdomain": assignment["subdomain"],
            }
        )
        if cls == "unjudged":
            unjudged_studies.append(spec_dir)
            finds.append(
                {"kind": FIND_BUNDLE_LESS_STUDY, "subject": spec_dir}
            )
        if is_judgment:
            judgment_calls.append(spec_dir)
            finds.append(
                {
                    "kind": FIND_JUDGMENT_CALL,
                    "negative": counts["negative"],
                    "positive": counts["positive"],
                    "subject": spec_dir,
                    "total": sum(counts.values()),
                }
            )
    for item in null_falsifier_extracted:
        finds.append(
            {
                "document": item["document"],
                "kind": FIND_EXTRACTED_NULL_FALSIFIER,
                "subject": item["id"],
            }
        )
    finds.sort(key=lambda f: (f["kind"], f["subject"]))
    claim_nodes.sort(key=lambda n: n["id"])
    study_nodes.sort(key=lambda n: n["id"])

    # The coverage block (defs §9). Counts per domain only —
    # no cross-domain aggregate progress figure exists (C088-14).
    def _class_counts(nodes: list[dict], classes: tuple[str, ...]) -> dict:
        out = {cls: 0 for cls in classes}
        for node in nodes:
            if node["class"] in out:
                out[node["class"]] += 1
        return out

    domains_block: dict[str, dict] = {}
    for domain in tax["domains"]:
        d_claims = [n for n in claim_nodes if n["domain"] == domain]
        d_studies = [n for n in study_nodes if n["domain"] == domain]
        domains_block[domain] = {
            "claims": len(d_claims),
            "claims_by_class": _class_counts(d_claims, CLAIM_CLASSES),
            "restricted_studies": sum(
                1 for n in d_studies if n["restricted"]
            ),
            "studies": len(d_studies),
            "studies_by_class": _class_counts(d_studies, STUDY_CLASSES),
        }
    coverage = {
        "claims": {
            "by_class": _class_counts(claim_nodes, CLAIM_CLASSES),
            "by_population": {
                pop: sum(
                    1 for n in claim_nodes if n["population"] == pop
                )
                for pop in sorted({n["population"] for n in claim_nodes})
            },
            "total": len(claim_nodes),
        },
        "domains": domains_block,
        "falsifier_coverage": {
            "null_extracted_claims": sorted(
                item["id"] for item in null_falsifier_extracted
            ),
            "present": falsifier_present_count,
            "total": len(claim_nodes),
        },
        "judgment_call_studies": sorted(judgment_calls),
        "multi_spec_claims": sorted(multi_spec_claims),
        "studies": {
            "by_class": _class_counts(study_nodes, STUDY_CLASSES),
            "restricted": len(restricted),
            "total": len(study_nodes),
        },
        "unjudged_studies": sorted(unjudged_studies),
    }

    program_map = {
        "coverage": coverage,
        "defs_version": DEFS_VERSION,
        "nodes": {"claims": claim_nodes, "studies": study_nodes},
        "stamp": stamp,
        "taxonomy_version": TAXONOMY_VERSION,
    }
    finds_doc = {
        "defs_version": DEFS_VERSION,
        "finds": finds,
        "stamp": stamp,
        "taxonomy_version": TAXONOMY_VERSION,
    }
    return {MAP_REL: _dump(program_map), FINDS_REL: _dump(finds_doc)}


def build_outputs(root: Path) -> dict[Path, str]:
    """Build the full new text of every generated artifact, in memory."""
    return {
        root / rel: text for rel, text in build_artifacts(root).items()
    }


def check_outputs(root: Path) -> list[str]:
    """Names of artifacts whose committed bytes differ from a fresh build."""
    drifted: list[str] = []
    for path, fresh in build_outputs(root).items():
        if not path.is_file() or path.read_bytes() != fresh.encode("utf-8"):
            drifted.append(str(path.relative_to(root)))
    return drifted


def write_outputs(root: Path) -> list[str]:
    """Write every artifact (all builds succeed first, or none is written)."""
    outputs = build_outputs(root)
    written: list[str] = []
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        written.append(str(path.relative_to(root)))
    return written
