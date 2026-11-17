"""Corpus identity standard — registry, verification, enforcement.

Spec 095 Stage 1 (T104). The prose standard lives at
``glossa-indus/CORPUS_IDENTITY_STANDARD.md``; this module is its
machine-readable form. Every claim-bearing Indus corpus has one
identity of record here: version, content hash, source, licensing,
counts under a named basis, and normalization rules.

Fail-closed rules (the standard, enforced by the covered loaders):

- A corpus file that is PRESENT but whose SHA-256 differs from its
  identity pin is refused at load time (``enforce_file_identity``,
  called from each covered loader's load path). A differing corpus
  is never silently loaded, and a loader never falls back to another
  corpus because the file at its path failed identity.
- ``verify_corpus_identity`` additionally refuses a MISSING corpus,
  an unreadable corpus, and a census that differs from the identity
  record under its named basis. ``load_corpus_verified`` entry
  points refuse on absence as well.
- Absence on the legacy load paths keeps each loader's documented
  historical behaviour (for example the V3 loader loads zero
  records); absence is a flagged state, detectable at any time
  through ``verify_corpus_identity`` — it is never a silent
  substitution of a different corpus.

_citation:
  derivation: "Spec 095 Stage 1 (T104/T105). Pins of record: the V3
               strict corpus carries its PR #393 intake pin
               (2026-10-25); the Holdat layer carries its Spec 054
               arm-2 pin; the remaining pins were established by
               this stage's measurement of the in-tree files at
               registration (2026-11-16) and are stated as such in
               the stage record."
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from dataclasses import dataclass
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]

V3_KEY = "indus_v3_firestore_strict"
V1_KEY = "indus_v1_research_export"
ICIT_KEY = "indus_icit_export"
CISI_KEY = "indus_cisi_compilation"
MAYIG_KEY = "mayig_cisi_layer"
M77_KEY = "indus_m77_flat"
SITE_KEY = "indus_site_attributed_csv"
HOLDAT_KEY = "holdat_downloads_layer"


class CorpusIdentityError(RuntimeError):
    """A corpus failed its identity of record; loading is refused."""


@dataclass(frozen=True)
class CorpusIdentity:
    """The identity of record for one claim-bearing corpus."""

    key: str
    name: str
    version: str
    source: str
    licensing: str
    paths: tuple[str, ...]
    sha256: str | None
    census_basis: str
    census: dict | None
    normalization: str
    loaders: tuple[str, ...]


CORPUS_IDENTITIES: dict[str, CorpusIdentity] = {
    V3_KEY: CorpusIdentity(
        key=V3_KEY,
        name="Indus strict corpus (Firestore 'indusarrays' reconstruction)",
        version="acquired 2026-05-14; intake-pinned 2026-10-25 (PR #393)",
        source=(
            "indusscript.in Firestore 'indusarrays' collection, RMRL Indus "
            "Research Centre; acquired with user permission via the "
            "Firebase REST API"
        ),
        licensing=(
            "RMRL research-use material; do not redistribute without "
            "contact. Held restricted-local; the raw file is never "
            "committed (gitignored subtree)"
        ),
        paths=(
            "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/"
            "firestore_indusarrays_full.jsonl",
        ),
        sha256="073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578",
        census_basis=(
            "V3 loader basis (indus_corpus_v3.corpus_stats): records = "
            "parsed JSONL records; dockeys/sequences/instances after the "
            "loader's reconstruction (texts primary, S1..S14 fallback, "
            "*NNN filtered, longest per (dockey, sideline), length >= 2)"
        ),
        census={
            "records": 3916,
            "unique_dockeys": 2665,
            "total_sequences": 3137,
            "total_sign_instances": 12494,
        },
        normalization=(
            "Mahadevan M77 integer sign IDs; 'texts' array is primary, "
            "S1..S14 fields are the fallback; empty/'0' entries and RMRL "
            "supplementary *NNN signs are filtered at load; sequence "
            "order as stored (no reversal); longest sequence kept per "
            "(dockey, sideline)"
        ),
        loaders=("indus_corpus_v3", "indus_corpus_firestore"),
    ),
    V1_KEY: CorpusIdentity(
        key=V1_KEY,
        name="Indus V1 research export (multi-source)",
        version="V1, date-tracked; built 2026-05-14 (CORPUS_VERSIONS.md)",
        source=(
            "Program-built rights-cleared research export "
            "(corpus_indus_export.py): mayig-CISI, Penn Museum, Met Open "
            "Access, Cleveland Museum of Art, indusscript.in (M77)"
        ),
        licensing=(
            "Per-source licences in glossa-indus/CORPUS_VERSIONS.md "
            "(mayig MIT; Penn Museum CC BY 4.0; Met and Cleveland CC0; "
            "the indusscript.in component carries RMRL research-use terms)"
        ),
        paths=("glossa-corpus/indus/exports/indus_research.jsonl",),
        sha256="08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e",
        census_basis=(
            "Export record basis: one JSON object per non-empty JSONL "
            "line, as the V2 loader reads them"
        ),
        census={"records": 15508},
        normalization=(
            "Parpola P-number source IDs converted to integer Mahadevan "
            "IDs where a crosswalk entry exists (unmapped signs keep the "
            "P-number as fallback int); Fuls/Wells 3-digit IDs preserved"
        ),
        loaders=("indus_corpus_v2",),
    ),
    ICIT_KEY: CorpusIdentity(
        key=ICIT_KEY,
        name="Indus ICIT-format export",
        version="as labelled in the file's own 'version' field",
        source="Program-built ICIT-format export of the V1 source set",
        licensing="Per-source licences as for the V1 research export",
        paths=("glossa-corpus/indus/exports/indus_icit_format.json",),
        sha256="e4ddfd064e9f97871cd4c498f39f238c7cecb2f6a646733b0a65f22f81bd7e2d",
        census_basis=(
            "File-declared basis: the file's own 'total_sequences' field "
            "against the length of its 'sequences' list"
        ),
        census={"total_sequences": 3085},
        normalization="Sequences as exported; no load-time transformation",
        loaders=("indus_corpus_v2 (status accounting)",),
    ),
    CISI_KEY: CorpusIdentity(
        key=CISI_KEY,
        name="Indus CISI compilation (Mohenjo-daro subset)",
        version="Phase-44 rebuild format (dict with 'inscriptions')",
        source=(
            "CISI-based compilation held by the program (mayig CISI "
            "lineage); 179 Mohenjo-daro inscriptions"
        ),
        licensing=(
            "CISI-derived: statistics are publishable; the underlying "
            "CISI scans are never redistributed"
        ),
        paths=(
            "data/indus_cisi_corpus.json",
            "backend/data/indus_cisi_corpus.json",
            "backend/glossa_lab/data/indus_cisi_corpus.json",
        ),
        sha256="f9633c7045ad0a74fc0dff66164e24117b3f9de1850e0257d16f1b8505e314c1",
        census_basis=(
            "Compilation basis: entries in the file's 'inscriptions' "
            "list (legacy form: entries in the top-level list)"
        ),
        census={"inscriptions": 179},
        normalization=(
            "Parpola sign IDs as stored; the loader normalises the "
            "Phase-44 'signs' form to the legacy 'graphemes' form"
        ),
        loaders=("indus_cisi",),
    ),
    MAYIG_KEY: CorpusIdentity(
        key=MAYIG_KEY,
        name="mayig CISI layer (v1)",
        version="layer v1, built by phase122_build_crosswalk_mayig",
        source="Built from the mayig CISI data by the program's phase122 build",
        licensing="mayig CISI data: MIT (CORPUS_VERSIONS.md)",
        paths=("data/corpus_layers/mayig_cisi_layer_v1.json",),
        sha256="6a7664c605079373ca80e70b7e9559c1527613e3f67b579a817ced785e129860",
        census_basis="Layer basis: entries in the file's 'inscriptions' list",
        census={"inscriptions": 179},
        normalization="As built by phase122; no load-time transformation",
        loaders=("mayig_layer",),
    ),
    M77_KEY: CorpusIdentity(
        key=M77_KEY,
        name="Mahadevan 1977 concordance flat text",
        version="program-held flat text copy",
        source="Mahadevan (1977) concordance, flat text form",
        licensing="Research-use concordance data held by the program",
        paths=(
            "reports/mahadevan_corpus_flat.txt",
            "data/mahadevan_corpus_flat.txt",
            "data_raw/mahadevan_1977/mahadevan_corpus_flat.txt",
        ),
        sha256="878fd2231929f2105cb5c7fb37507ee7eceb7d83f355f1fa4d8e793926785c18",
        census_basis=(
            "Flat-text basis: one inscription per non-empty line, as the "
            "M77 loader parses them"
        ),
        census={"lines": 1669},
        normalization=(
            "Whitespace-separated sign tokens, one inscription per line, "
            "order as stored"
        ),
        loaders=("indus_m77",),
    ),
    SITE_KEY: CorpusIdentity(
        key=SITE_KEY,
        name="Indus site-attributed layer (yajnadevam inscriptions CSV)",
        version="program-held CSV, as stored",
        source="Site-attributed inscription layer (yajnadevam corpus work)",
        licensing="Research-use data held by the program",
        paths=("backend/glossa_lab/data/yajnadevam_inscriptions.csv",),
        sha256="c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98",
        census_basis="CSV basis: data rows excluding the header row",
        census={"data_rows": 5679},
        normalization="Rows as stored; no load-time transformation",
        loaders=("(script-level consumers; no data-module loader)",),
    ),
    HOLDAT_KEY: CorpusIdentity(
        key=HOLDAT_KEY,
        name="Holdat downloads layer (arm-2 corpus)",
        version="as downloaded; pinned at Spec 054 gate G4 (run 2)",
        source="Holdat LLC Indus corpus downloads (holdatllc_indus)",
        licensing="Holdat research-use download terms",
        paths=(
            "corpora/downloads/external_repos/holdatllc_indus/"
            "indus_corpus 2.csv",
        ),
        sha256="62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e",
        census_basis=(
            "Spec 054 arm-2 basis (phase438 instrument census): 1,670 "
            "sequences / 7,002 tokens / 390 distinct signs — recorded "
            "here; machine census is the phase438 instrument's, so this "
            "identity is verified by pin (and by absence) only"
        ),
        census=None,
        normalization="As downloaded; the phase438 instrument's basis applies",
        loaders=("(phase438 instrument; no data-module loader)",),
    ),
}


def get_identity(key: str) -> CorpusIdentity:
    """Return the identity of record for ``key`` or refuse."""
    try:
        return CORPUS_IDENTITIES[key]
    except KeyError:
        raise CorpusIdentityError(
            f"no corpus identity of record for {key!r}; a claim-bearing "
            "corpus without an identity record must not be loaded"
        ) from None


def file_sha256(path: Path) -> str:
    """SHA-256 of a file's bytes."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _resolve(identity: CorpusIdentity, root: Path) -> Path | None:
    for rel in identity.paths:
        candidate = root / rel
        if candidate.exists():
            return candidate
    return None


def _check_readable(identity: CorpusIdentity, path: Path) -> None:
    if path.stat().st_mode & 0o444 == 0:
        raise CorpusIdentityError(
            f"{identity.key}: corpus at {path} carries no read "
            "permission (unauthorized access); refusing to treat it "
            "as absent or empty"
        )


# ── Census functions (one per named basis) ──────────────────────────

_S_FIELDS = [f"S{i}" for i in range(1, 15)]


def _v3_is_valid_sign(v) -> bool:
    if not v:
        return False
    v = str(v).strip()
    if not v or v == "0":
        return False
    if v.startswith("*"):
        return False
    try:
        int(v)
        return True
    except ValueError:
        return False


def _census_v3(path: Path) -> dict:
    """Mirror of the V3 loader's reconstruction (its named basis)."""
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except Exception:
                pass
    by_key: dict = {}
    for r in records:
        raw_dockey = r.get("dockey")
        if raw_dockey is None:
            continue
        try:
            dockey = int(str(raw_dockey))
        except (ValueError, TypeError):
            continue
        sideline = str(r.get("sideline", "0"))
        texts = r.get("texts") or []
        clean = [int(v) for v in texts if _v3_is_valid_sign(str(v))]
        if len(clean) < 2:
            clean = [
                int(r[sf]) for sf in _S_FIELDS if _v3_is_valid_sign(str(r.get(sf, "")))
            ]
        if len(clean) >= 2:
            k = (dockey, sideline)
            if k not in by_key or len(clean) > len(by_key[k]):
                by_key[k] = clean
    seqs = list(by_key.values())
    dockeys = {d for (d, _s) in by_key}
    return {
        "records": len(records),
        "unique_dockeys": len(dockeys),
        "total_sequences": len(seqs),
        "total_sign_instances": sum(len(s) for s in seqs),
    }


def _census_jsonl_records(path: Path) -> dict:
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            n += 1
    return {"records": n}


def _census_icit(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {"total_sequences": len(data.get("sequences", []))}


def _census_inscriptions(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return {"inscriptions": len(data.get("inscriptions", []))}
    return {"inscriptions": len(data)}


def _census_flat_lines(path: Path) -> dict:
    n = sum(
        1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    )
    return {"lines": n}


def _census_csv_rows(path: Path) -> dict:
    rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"))))
    return {"data_rows": max(len(rows) - 1, 0)}


_CENSUS_FUNCS = {
    V3_KEY: _census_v3,
    V1_KEY: _census_jsonl_records,
    ICIT_KEY: _census_icit,
    CISI_KEY: _census_inscriptions,
    MAYIG_KEY: _census_inscriptions,
    M77_KEY: _census_flat_lines,
    SITE_KEY: _census_csv_rows,
    HOLDAT_KEY: None,
}


def corpus_census(key: str, path: Path) -> dict | None:
    """Census of ``path`` under the named basis of ``key``'s identity."""
    func = _CENSUS_FUNCS[get_identity(key).key]
    if func is None:
        return None
    return func(path)


# ── Verification and enforcement ────────────────────────────────────

_ENFORCED: dict[tuple[str, int, int], bool] = {}


def enforce_file_identity(key: str, path: Path) -> None:
    """Load-path guard: a PRESENT corpus file must match its pin.

    Absence is not judged here (each loader's documented absence
    behaviour stands, and ``verify_corpus_identity`` refuses absence
    on the verified paths). A present file whose digest differs from
    the identity pin — or a registered corpus with no pin — raises
    :class:`CorpusIdentityError`.
    """
    identity = get_identity(key)
    if not path.exists():
        return
    _check_readable(identity, path)
    if identity.sha256 is None:
        raise CorpusIdentityError(
            f"{key}: corpus at {path} has no identity pin of record; "
            "refusing to load an unpinned claim-bearing corpus"
        )
    stat = path.stat()
    cache_key = (str(path), stat.st_mtime_ns, stat.st_size)
    if cache_key in _ENFORCED:
        return
    observed = file_sha256(path)
    if observed != identity.sha256:
        raise CorpusIdentityError(
            f"{key}: corpus at {path} hashes to {observed}, which "
            f"differs from its identity pin {identity.sha256}; "
            "refusing to load a corpus that is not the corpus of record"
        )
    _ENFORCED[cache_key] = True


def verify_corpus_identity(key: str, root: Path | None = None) -> dict:
    """Verify one corpus against its identity of record, or refuse.

    Refuses (raises :class:`CorpusIdentityError`) when the identity
    is unknown, the corpus file is missing, the file is unreadable,
    its digest differs from the pin, or its census under the named
    basis differs from the identity record. On success returns the
    verification record.
    """
    identity = get_identity(key)
    root = _REPO if root is None else root
    path = _resolve(identity, root)
    if path is None:
        raise CorpusIdentityError(
            f"{key}: corpus missing — none of its identity paths "
            f"exists under {root}: {list(identity.paths)}"
        )
    _check_readable(identity, path)
    if identity.sha256 is None:
        raise CorpusIdentityError(
            f"{key}: no identity pin of record; refusing to verify"
        )
    observed = file_sha256(path)
    if observed != identity.sha256:
        raise CorpusIdentityError(
            f"{key}: corpus at {path} hashes to {observed}, which "
            f"differs from its identity pin {identity.sha256}"
        )
    measured = corpus_census(key, path) if identity.census is not None else None
    if identity.census is not None and measured != identity.census:
        raise CorpusIdentityError(
            f"{key}: census under the named basis differs from the "
            f"identity record: measured {measured}, identity "
            f"{identity.census}"
        )
    return {
        "key": key,
        "path": str(path),
        "sha256": observed,
        "census": measured,
        "identity": identity,
    }


def verify_all_identities(root: Path | None = None) -> dict:
    """Verify every registered corpus; refuse if any fails.

    A partially available corpus set is a refusal, naming every
    corpus that failed (the T105 partial-availability case).
    """
    results: dict[str, dict] = {}
    failures: dict[str, str] = {}
    for key in CORPUS_IDENTITIES:
        try:
            results[key] = verify_corpus_identity(key, root=root)
        except CorpusIdentityError as exc:
            failures[key] = str(exc)
    if failures:
        raise CorpusIdentityError(
            "corpus set only partially available / verified: "
            + "; ".join(f"{k}: {v}" for k, v in sorted(failures.items()))
        )
    return results


# ── Audit (flags; the T105 battery's diagnostic leg) ────────────────


def canonical_export_pin(sequences_by_dockey: dict) -> str:
    """The canonical export pin for the strict corpus.

    The construction of record (phase438 instrument, gate G2):
    SHA-256 over the sort-keys JSON dump of the source label and the
    sequences-by-dockey mapping.
    """
    export = json.dumps(
        {
            "source": "indusscript.in Firestore 'indusarrays' (2026-05-14)",
            "sequences_by_dockey": sequences_by_dockey,
        },
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(export).hexdigest()


def audit_export_orientation(reference: dict, candidate: dict) -> list[str]:
    """Flag a candidate export whose reading order is reversed.

    Returns ``["reversed_reading_order"]`` when the candidate's
    sequences are the element-wise reverse of the reference export's
    (and the candidate is not identical to the reference). A reversed
    corpus also fails the canonical export pin; this audit names the
    defect.
    """
    def norm(sbd: dict) -> dict:
        return {str(k): [list(s) for s in v] for k, v in sbd.items()}

    ref, cand = norm(reference), norm(candidate)
    if cand == ref:
        return []
    reversed_ref = {k: [list(reversed(s)) for s in v] for k, v in ref.items()}
    if cand == reversed_ref:
        return ["reversed_reading_order"]
    return []


def audit_v3_records(records: list, lines: int) -> list[str]:
    """Audit parsed V3-basis records; return flag names.

    Flags: ``damaged_spans`` (unparseable lines), ``duplicate_identifiers``
    (exact duplicate records), ``contradictory_mappings`` (one
    (dockey, sideline) carrying two different sign sequences),
    ``unknown_signs`` (foreign-numbering tokens, e.g. Parpola
    P-prefixed IDs, inside an M77-basis file), ``schema_mismatch``
    (records without the corpus's identifying fields).
    """
    flags: list[str] = []
    parsed = len(records)
    if parsed < lines:
        flags.append("damaged_spans")
    seen_records: set[str] = set()
    by_pair: dict[tuple, tuple] = {}
    for r in records:
        if not isinstance(r, dict) or "dockey" not in r or "texts" not in r:
            if "schema_mismatch" not in flags:
                flags.append("schema_mismatch")
            continue
        blob = json.dumps(r, sort_keys=True, default=str)
        if blob in seen_records and "duplicate_identifiers" not in flags:
            flags.append("duplicate_identifiers")
        seen_records.add(blob)
        pair = (str(r.get("dockey")), str(r.get("sideline", "0")))
        seq = tuple(str(v) for v in (r.get("texts") or []))
        if pair in by_pair and by_pair[pair] != seq:
            if "contradictory_mappings" not in flags:
                flags.append("contradictory_mappings")
        by_pair.setdefault(pair, seq)
        for v in r.get("texts") or []:
            s = str(v).strip()
            if s and not _v3_is_valid_sign(s) and not s.startswith("*"):
                if any(ch.isalpha() for ch in s):
                    if "unknown_signs" not in flags:
                        flags.append("unknown_signs")
    return flags


def audit_corpus_file(key: str, path: Path) -> list[str]:
    """Audit a corpus file against its identity; return flag names.

    Always includes ``content_hash_mismatch`` when the file's digest
    differs from the identity pin. For the strict corpus, the
    record-level flags of :func:`audit_v3_records` are added.
    """
    identity = get_identity(key)
    flags: list[str] = []
    if identity.sha256 is not None and file_sha256(path) != identity.sha256:
        flags.append("content_hash_mismatch")
    if key == V3_KEY:
        lines = 0
        records: list = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                lines += 1
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
        flags.extend(f for f in audit_v3_records(records, lines) if f not in flags)
    return flags
