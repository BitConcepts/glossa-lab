#!/usr/bin/env python3
"""Phase-122 builder: Parpola<->Mahadevan crosswalk v1 + mayig layer.

Deliverables (all committed; mayig data is MIT-licensed, see the
layer metadata):

  data/crosswalks/parpola_mahadevan_crosswalk_v1.csv
  data/crosswalks/parpola_mahadevan_crosswalk_v1.json
  data/corpus_layers/mayig_cisi_layer_v1.json
  data/corpus_layers/mayig_cisi_layer_v1_meta.json
  reports/phase122_crosswalk_mayig_results.json   (statistics)

Crosswalk sources (every row carries its source):

  canonical_registry  data/crosswalks/canonical_sign_registry.csv
      The program's canonical registry (spec 018 section A2: the
      primary cross-system map of record). The sparse
      mahadevan_parpola_crosswalk_v2.json map was explicitly
      REJECTED as canonical by spec 018 appendix A.4 (covers only
      131 of 284 attested M signs; inverts several high-frequency
      assignments, e.g. P385 receives 0 tokens under it). v2 is
      retained here only as a corroborating/ dissenting SOURCE,
      never as the map of record.
  mayig_features      mayig/indus-valley-script-corpus features/*.json
      `mahadevan_graphemes` per Parpola sign; the mayig README
      states these derive from the author's cross-match against
      Parpola (1982) allographs and Wells (2015). MIT license.
  crosswalk_v2        backend/glossa_lab/data/
                      mahadevan_parpola_crosswalk_v2.json
      Phase-28-era sparse map; per-entry `source` strings cite
      e.g. "Parpola 1994 Appendix B". Rejected as canonical
      (above); kept as a source so disagreements surface as
      flagged conflicts rather than silent picks.
  candidates_unadmitted  backend/glossa_lab/data/
                      mahadevan_parpola_crosswalk_candidates.json
      Spec 004 WS2 held candidates: pairs with NO explicit
      in-repo source stating the equivalence (number-identity
      inference). Emitted at LOW confidence only, flagged
      `candidate_only`, and excluded from the mapping-coverage
      computation.

Confidence rubric (frozen for v1):
  high   pair attested by BOTH canonical_registry and
         mayig_features (the two independent structured maps;
         in v1 their pair sets turned out identical, 372 pairs).
  medium pair attested by exactly one of {canonical_registry,
         mayig_features} and not contradicted by the other.
  low    pair attested only by crosswalk_v2 (the sparse map
         spec 018 rejected as canonical) or only by
         candidates_unadmitted (no explicit source).
  Conflicts are flagged separately from confidence: a pair is
  `conflict` when a source asserts a DISJOINT M set for the
  same P (or a disjoint P set for the same M) — a genuine
  identity disagreement; mere granularity differences between
  overlapping sets are recorded as set differences, not
  conflicts. In v1 nearly all conflicts are the documented
  crosswalk_v2-vs-registry inversions (spec 018 appendix A.4);
  the dissenting source is named in `conflict_detail`.

Relation type is computed per row from the union of the
non-candidate sources attesting that pair: for P with M-set Mp
and M with P-set Pm -- 1:1 (|Mp|=|Pm|=1), one-to-many
(|Mp|>1, |Pm|=1), many-to-one (|Mp|=1, |Pm|>1), many-to-many
(both >1). P signs with no M in any source (incl. candidates)
get one `unmapped` row; M signs attested in sources but claimed
by no P are listed separately in the JSON (`m_unmapped`).

No forced 1:1: splits and merges are represented as multiple
rows. Where sources disagree, BOTH mappings are kept with
their sources and flagged `conflict`.

Mayig layer: follows the Phase-115/116 converted-layer pattern
(builder + committed build metadata + per-inscription provenance:
source file, CISI object ID, side ID, description, token
sequence in source order, per-token feature vectors). Keyed by
CISI object ID (side IDs such as "M-1A" group under object
"M-1"). Because mayig is MIT-licensed, the converted layer is
committed as a first-class corpus layer under data/corpus_layers/
(unlike the ICIT layer, whose source terms keep it in the
gitignored downloads tree with statistics only published).

Coverage: each mayig token's P sign is resolved through the
v1 crosswalk (registry+mayig+v2 union, candidates excluded):
  clean     token's P resolves to exactly one M sign
  ambiguous token's P resolves to >1 M signs (split/merge)
  unmapped  token's P has no M in the crosswalk
An inscription is clean if all tokens are clean, partial if at
least one token resolves (clean or ambiguous) but not all are
clean, and none if no token resolves at all.

CISI overlap: mayig object IDs are compared against the CISI
object identifiers obtainable now: (a) M-prefixed IDs extracted
by regex from the djvu OCR text of the CISI Vol. 1 and Vol. 2
IA scans, (b) the Bhaskar et al. 2024 ESM13 catalogue's CISI ID
column (an updated CISI-derived object catalogue), and (c) the
`cisi` field of the Phase-116 keyed ICIT layer. OCR extraction
is partial (plates are images); figures are reported per basis
with their limits. Phase E will produce the full structured
CISI catalogue table; this overlap is provisional.

Re-running this builder on the same inputs reproduces the
outputs byte-identically (sorted keys, no timestamps inside
data files; run metadata lives only in the results JSON).
"""
from __future__ import annotations

import collections
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SWEEP = (Path.home() / "workspace" / "research_notes"
         / "indus-data-deep-sweep-20261008" / "downloads")
MAYIG = SWEEP / "mayig-indus-valley-script-corpus"
DL = REPO / "corpora" / "downloads"
MAIN_DL = Path.home() / "workspace" / "glossa-lab" / "corpora" / "downloads"

REGISTRY = REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"
V2 = REPO / "backend" / "glossa_lab" / "data" / "mahadevan_parpola_crosswalk_v2.json"
CAND = (REPO / "backend" / "glossa_lab" / "data"
        / "mahadevan_parpola_crosswalk_candidates.json")

OUT_XW_CSV = REPO / "data" / "crosswalks" / "parpola_mahadevan_crosswalk_v1.csv"
OUT_XW_JSON = REPO / "data" / "crosswalks" / "parpola_mahadevan_crosswalk_v1.json"
OUT_LAYER = REPO / "data" / "corpus_layers" / "mayig_cisi_layer_v1.json"
OUT_LAYER_META = REPO / "data" / "corpus_layers" / "mayig_cisi_layer_v1_meta.json"
OUT_RESULTS = REPO / "reports" / "phase122_crosswalk_mayig_results.json"

SRC_REGISTRY = "canonical_registry"
SRC_MAYIG = "mayig_features"
SRC_V2 = "crosswalk_v2"
SRC_CAND = "candidates_unadmitted"
CORE_SOURCES = (SRC_REGISTRY, SRC_MAYIG, SRC_V2)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def norm_p(raw: str) -> str | None:
    m = re.fullmatch(r"P(\d{1,3})", (raw or "").strip())
    return f"P{int(m.group(1)):03d}" if m else None


def norm_m(raw: str) -> str | None:
    m = re.fullmatch(r"M(\d{1,3})", (raw or "").strip())
    return f"M{int(m.group(1)):03d}" if m else None


# ── Source extraction: source -> {P: set[M]} ────────────────────────────────

def registry_pairs() -> tuple[dict[str, set[str]], set[str]]:
    pairs: dict[str, set[str]] = collections.defaultdict(set)
    p_universe: set[str] = set()
    with REGISTRY.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("numbering_system") != "parpola_1982":
                continue
            p = norm_p(row.get("parpola_id") or row.get("sign_id") or "")
            if not p:
                continue
            p_universe.add(p)
            for raw in (row.get("mahadevan_ids") or "").split("|"):
                m = norm_m(raw)
                if m:
                    pairs[p].add(m)
    return pairs, p_universe


def mayig_feature_pairs() -> tuple[dict[str, set[str]], set[str], set[str]]:
    pairs: dict[str, set[str]] = collections.defaultdict(set)
    p_universe: set[str] = set()
    m_seen: set[str] = set()
    for fp in sorted((MAYIG / "features").glob("P*.json")):
        d = json.loads(fp.read_text(encoding="utf-8"))
        p = norm_p(d.get("id") or fp.stem)
        if not p:
            continue
        p_universe.add(p)
        for raw in d.get("mahadevan_graphemes") or []:
            m = norm_m(raw)
            if m:
                pairs[p].add(m)
                m_seen.add(m)
    return pairs, p_universe, m_seen


def v2_pairs() -> tuple[dict[str, set[str]], dict[tuple[str, str], str]]:
    data = json.loads(V2.read_text(encoding="utf-8"))
    pairs: dict[str, set[str]] = collections.defaultdict(set)
    detail: dict[tuple[str, str], str] = {}
    for e in data.get("crosswalk", {}).values():
        p = norm_p(e.get("parpola_id") or "")
        m = norm_m(e.get("mahadevan_id") or "")
        if p and m:
            pairs[p].add(m)
            detail[(p, m)] = (f"{e.get('source', '')} "
                              f"[v2 confidence {e.get('confidence', '')}]").strip()
    return pairs, detail


def candidate_pairs() -> tuple[dict[str, set[str]], list]:
    data = json.loads(CAND.read_text(encoding="utf-8"))
    pairs: dict[str, set[str]] = collections.defaultdict(set)
    cand = data.get("candidates") or {}
    items = cand.items() if isinstance(cand, dict) else [
        (str(i), c) for i, c in enumerate(cand)]
    for _k, c in items:
        if not isinstance(c, dict):
            continue
        p_raw = c.get("parpola_id") or c.get("p_id") or ""
        if not p_raw and c.get("parpola_num") is not None:
            p_raw = f"P{int(c['parpola_num']):03d}"
        p = norm_p(str(p_raw))
        m = norm_m(c.get("mahadevan_id") or c.get("m_id") or "")
        if p and m:
            pairs[p].add(m)
    return pairs, data.get("known_conflicts_not_resolved") or []


# ── Crosswalk assembly ───────────────────────────────────────────────────────

def build_crosswalk() -> dict:
    reg, reg_universe = registry_pairs()
    may, may_universe, may_m = mayig_feature_pairs()
    v2, v2_detail = v2_pairs()
    cand, known_conflicts = candidate_pairs()
    by_source = {SRC_REGISTRY: reg, SRC_MAYIG: may, SRC_V2: v2,
                 SRC_CAND: cand}

    p_universe = reg_universe | may_universe | set(v2) | set(cand)
    # pair -> set of attesting sources
    pair_sources: dict[tuple[str, str], set[str]] = collections.defaultdict(set)
    for src, pmap in by_source.items():
        for p, ms in pmap.items():
            for m in ms:
                pair_sources[(p, m)].add(src)

    # union M-set per P / P-set per M, per source and overall-core
    def union_map(srcs) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
        pm: dict[str, set[str]] = collections.defaultdict(set)
        mp: dict[str, set[str]] = collections.defaultdict(set)
        for (p, m), ss in pair_sources.items():
            if ss & set(srcs):
                pm[p].add(m)
                mp[m].add(p)
        return pm, mp

    core_pm, core_mp = union_map(CORE_SOURCES)

    def relation(p: str, m: str, pm, mp) -> str:
        np_, nm = len(pm.get(p, ())), len(mp.get(m, ()))
        if np_ == 1 and nm == 1:
            return "1:1"
        if np_ > 1 and nm == 1:
            return "one-to-many"
        if np_ == 1 and nm > 1:
            return "many-to-one"
        return "many-to-many"

    rows = []
    for (p, m) in sorted(pair_sources):
        srcs = pair_sources[(p, m)]
        core_srcs = srcs & set(CORE_SOURCES)
        # conflict: a core source asserts an M-set for p (or a
        # P-set for m) that is DISJOINT from the set asserted by
        # the sources attesting this pair — a genuine disagreement
        # about identity. Sets that merely differ in granularity
        # (one source lists all M grapheme variants, another a
        # subset) overlap and are NOT conflicts; they are recorded
        # in conflict_detail as set differences for transparency.
        conflict = False
        dissent = []
        attest_m = set().union(*[by_source[s].get(p, set())
                                 for s in core_srcs]) if core_srcs else set()
        attest_p = set()
        for s in core_srcs:
            attest_p |= {pp for pp, ms in by_source[s].items() if m in ms}
        for src in CORE_SOURCES:
            if src in core_srcs:
                continue
            sm = by_source[src].get(p)
            if sm and attest_m and not (sm & attest_m):
                conflict = True
                dissent.append(f"{src}: P->{sorted(sm)} (disjoint)")
            sp = {pp for pp, ms in by_source[src].items() if m in ms}
            if sp and attest_p and not (sp & attest_p):
                conflict = True
                dissent.append(f"{src}: M->{sorted(sp)} (disjoint)")
        # granularity notes: attesting sources whose sets differ
        for src in sorted(core_srcs):
            sm = by_source[src].get(p)
            if sm and sm != attest_m:
                dissent.append(f"set-difference {src}: P->{sorted(sm)}")
        candidate_only = not core_srcs
        if candidate_only:
            conf = "low"
            cand_pm, cand_mp = union_map((SRC_CAND,))
            rel = relation(p, m, cand_pm, cand_mp)
        elif SRC_REGISTRY in srcs and SRC_MAYIG in srcs:
            conf = "high"
            rel = relation(p, m, core_pm, core_mp)
        elif SRC_REGISTRY in srcs or SRC_MAYIG in srcs:
            conf = "medium"
            rel = relation(p, m, core_pm, core_mp)
        else:  # crosswalk_v2 only — the rejected sparse map
            conf = "low"
            rel = relation(p, m, core_pm, core_mp)
        rows.append({
            "parpola_id": p,
            "mahadevan_id": m,
            "relation_type": rel,
            "confidence": conf,
            "sources": sorted(srcs),
            "source_detail": v2_detail.get((p, m), ""),
            "conflict": conflict,
            "conflict_detail": "; ".join(sorted(set(dissent))),
            "candidate_only": candidate_only,
        })

    # unmapped P signs: in the P universe but no pair in any source
    mapped_p = {p for (p, _m) in pair_sources}
    unmapped_rows = [{
        "parpola_id": p, "mahadevan_id": "", "relation_type": "unmapped",
        "confidence": "none", "sources": [], "source_detail": "",
        "conflict": False, "conflict_detail": "", "candidate_only": False,
    } for p in sorted(p_universe - mapped_p)]

    # M signs attested (mayig features / v2 / candidates) but unclaimed
    all_m = set(may_m)
    for pmap in (v2, cand):
        for ms in pmap.values():
            all_m |= ms
    for row in csv.DictReader(REGISTRY.open(newline="", encoding="utf-8")):
        for raw in (row.get("mahadevan_ids") or "").split("|"):
            mm = norm_m(raw)
            if mm:
                all_m.add(mm)
    claimed_m = {m for (_p, m) in pair_sources}
    m_unmapped = sorted(all_m - claimed_m)

    all_rows = rows + unmapped_rows
    stats = {
        "n_rows": len(all_rows),
        "n_pairs": len(rows),
        "p_signs_covered": len({r["parpola_id"] for r in rows}),
        "p_signs_unmapped": len(unmapped_rows),
        "m_signs_covered": len(claimed_m),
        "m_signs_unmapped": len(m_unmapped),
        "relation_breakdown": dict(collections.Counter(
            r["relation_type"] for r in all_rows)),
        "confidence_breakdown": dict(collections.Counter(
            r["confidence"] for r in rows)),
        "conflict_pairs": sum(1 for r in rows if r["conflict"]),
        "conflict_p_signs": len({r["parpola_id"] for r in rows
                                  if r["conflict"]}),
        "candidate_only_pairs": sum(1 for r in rows if r["candidate_only"]),
        "pairs_by_source": {s: sum(1 for r in rows if s in r["sources"])
                            for s in by_source},
        "known_conflicts_from_candidates_file": known_conflicts,
    }
    return {"rows": all_rows, "m_unmapped": m_unmapped, "stats": stats,
            "core_pm": core_pm}


# ── Mayig layer ──────────────────────────────────────────────────────────────

def build_layer() -> tuple[dict, dict]:
    files = sorted((MAYIG / "corpus").rglob("*.json"))
    inscriptions = []
    tokens_total = 0
    signs = collections.Counter()
    for fp in files:
        sides = json.loads(fp.read_text(encoding="utf-8"))
        for side in sides:
            side_id = (side.get("id") or "").strip()
            m = re.fullmatch(r"([A-Za-z]+-\d+)([A-Za-z]?)", side_id)
            obj = m.group(1) if m else side_id
            graphemes = side.get("graphemes") or []
            tokens, feats = [], []
            for g in graphemes:
                p = norm_p(g.get("id") or "")
                tokens.append(p or (g.get("id") or ""))
                feats.append(g.get("features") or [])
                if p:
                    signs[p] += 1
            tokens_total += len(tokens)
            inscriptions.append({
                "cisi_object_id": obj,
                "side_id": side_id,
                "description": side.get("description") or "",
                "source_file": str(fp.relative_to(MAYIG)),
                "tokens": tokens,
                "features": feats,
                "token_count": len(tokens),
            })
    inscriptions.sort(key=lambda r: (r["cisi_object_id"], r["side_id"]))
    meta = {
        "layer": "mayig_cisi_layer_v1",
        "phase": 122,
        "source_repo": "https://github.com/mayig/indus-valley-script-corpus",
        "source_commit": "ad2f1e218a34b8c33c57de0d6cb8d99272765bbb",
        "source_commit_date": "2025-04-16",
        "license": "MIT (LICENSE in source repo root: 'MIT License, "
                   "Copyright (c) 2024 Michael Carlson' — verified "
                   "from the LICENSE file at acquisition, 2026-10-08)",
        "provenance_record": "research_notes/indus-data-deep-sweep-"
                             "20261008/downloads/PROVENANCE.md entry 1",
        "lineage": "Hand digitisation of the printed CISI volumes "
                   "(Parpola P-numbering, Parpola 1982 allographs, "
                   "Wells 2015 cross-match features). Independent "
                   "transcription lineage vs the held Holdat / "
                   "Mahadevan IC77 / ICIT extractions, over a "
                   "substantially overlapping artefact population; "
                   "deduplicate by CISI artefact ID before any "
                   "independence claim.",
        "keying": "Inscriptions keyed by CISI object ID "
                  "(e.g. 'M-1'); side IDs (e.g. 'M-1A') retained "
                  "per record.",
        "ordering": "Tokens in the source's own order (graphemes "
                    "recorded left-to-right on the artefact side; "
                    "script read right-to-left per the mayig "
                    "README). No adapter reverses a sequence.",
        "n_source_files": len(files),
        "n_inscriptions": len(inscriptions),
        "n_objects": len({r["cisi_object_id"] for r in inscriptions}),
        "n_sign_tokens": tokens_total,
        "n_distinct_signs": len(signs),
    }
    layer = {"source": meta, "inscriptions": inscriptions}
    return layer, meta


# ── Coverage + CISI overlap ──────────────────────────────────────────────────

def downloads_dir() -> Path:
    for cand in (DL, MAIN_DL):
        if (cand / "icit_fieldcady").exists():
            return cand
    raise FileNotFoundError("corpora/downloads not found")


def cisi_id_sets() -> dict[str, set[str]]:
    sets: dict[str, set[str]] = {}
    for vol in ("cisi-1-ia-scan", "cisi-2-ia-scan"):
        txt = next((SWEEP / vol).glob("*djvu.txt")).read_text(
            encoding="utf-8", errors="replace")
        sets[vol] = set(re.findall(r"\bM-\d+\b", txt))
    try:
        import openpyxl
        wb = openpyxl.load_workbook(
            SWEEP / "bhaskar-2024-esm" / "43539_2023_102_MOESM13_ESM.xlsx",
            read_only=True)
        ws = wb.active
        sets["bhaskar2024_esm13"] = {
            r[0].strip() for r in ws.iter_rows(values_only=True)
            if r and isinstance(r[0], str)
            and re.fullmatch(r"[A-Za-z]+-\d+", r[0].strip())}
    except Exception:  # noqa: BLE001 — basis documented as unavailable
        sets["bhaskar2024_esm13"] = set()
    keyed = json.loads((downloads_dir() / "icit_fieldcady"
                        / "icit_converted_v2_keyed.json").read_text())
    sets["icit_keyed_layer"] = {
        r["cisi"] for r in keyed["inscriptions"]
        if isinstance(r.get("cisi"), str)
        and re.fullmatch(r"[A-Za-z]+-\d+", r["cisi"])}
    return sets


def main() -> None:
    xw = build_crosswalk()
    layer, meta = build_layer()
    # coverage resolves through the crosswalk's usable map:
    # high+medium pairs only (canonical_registry / mayig_features).
    # crosswalk_v2-only and candidate-only pairs are LOW and are
    # excluded — v2 is the rejected map, candidates have no source.
    core_pm: dict[str, set[str]] = collections.defaultdict(set)
    for r in xw["rows"]:
        if r["confidence"] in ("high", "medium") and r["mahadevan_id"]:
            core_pm[r["parpola_id"]].add(r["mahadevan_id"])

    # token/inscription coverage through crosswalk v1 (core sources)
    tok = collections.Counter()
    insc = collections.Counter()
    fail_signs = collections.Counter()
    for rec in layer["inscriptions"]:
        kinds = []
        for t in rec["tokens"]:
            ms = core_pm.get(t, set())
            k = ("clean" if len(ms) == 1 else
                 "ambiguous" if len(ms) > 1 else "unmapped")
            kinds.append(k)
            tok[k] += 1
            if k != "clean":
                fail_signs[t] += 1
        if kinds and all(k == "clean" for k in kinds):
            insc["clean"] += 1
        elif any(k != "unmapped" for k in kinds):
            insc["partial"] += 1
        else:
            insc["none"] += 1

    # secondary coverage: canonical registry alone (the map of
    # record), for comparison with the union figure above
    reg_pm, _ = registry_pairs()
    tok_r = collections.Counter()
    insc_r = collections.Counter()
    for rec in layer["inscriptions"]:
        kinds = []
        for t in rec["tokens"]:
            ms = reg_pm.get(t, set())
            k = ("clean" if len(ms) == 1 else
                 "ambiguous" if len(ms) > 1 else "unmapped")
            kinds.append(k)
            tok_r[k] += 1
        if kinds and all(k == "clean" for k in kinds):
            insc_r["clean"] += 1
        elif any(k != "unmapped" for k in kinds):
            insc_r["partial"] += 1
        else:
            insc_r["none"] += 1

    id_sets = cisi_id_sets()
    mayig_objs = {r["cisi_object_id"] for r in layer["inscriptions"]}
    overlap = {}
    for name, s in id_sets.items():
        m_only = {i for i in s if i.startswith("M-")}
        overlap[name] = {
            "n_ids_total": len(s), "n_m_ids": len(m_only),
            "n_mayig_objects_in_set": len(mayig_objs & m_only),
            "mayig_coverage": round(len(mayig_objs & m_only)
                                    / len(mayig_objs), 4) if mayig_objs else 0,
        }
    union_m = set().union(*[{i for i in s if i.startswith("M-")}
                            for s in id_sets.values()]) if id_sets else set()
    overlap["union_of_bases"] = {
        "n_m_ids": len(union_m),
        "n_mayig_objects_in_set": len(mayig_objs & union_m),
        "mayig_coverage": round(len(mayig_objs & union_m)
                                / len(mayig_objs), 4) if mayig_objs else 0,
    }

    # ── write crosswalk ──
    OUT_XW_CSV.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=[
        "parpola_id", "mahadevan_id", "relation_type", "confidence",
        "sources", "source_detail", "conflict", "conflict_detail",
        "candidate_only"])
    w.writeheader()
    for r in xw["rows"]:
        w.writerow({**r, "sources": "|".join(r["sources"])})
    OUT_XW_CSV.write_text(buf.getvalue(), encoding="utf-8")

    xw_json = {
        "crosswalk": "parpola_mahadevan_crosswalk_v1",
        "phase": 122,
        "canonical_basis": {
            "map_of_record": "data/crosswalks/canonical_sign_registry.csv",
            "sha256": sha256_file(REGISTRY),
            "why_canonical": "Spec 018 (Phase-119) section A2 names the "
                             "registry the program's primary cross-system "
                             "map; appendix A.4 explicitly rejects "
                             "mahadevan_parpola_crosswalk_v2.json as "
                             "canonical (sparse: 131/284 attested M signs; "
                             "inverts high-frequency assignments). v2 is "
                             "used here only as a labelled source.",
        },
        "confidence_rubric": {
            "high": "attested by BOTH canonical_registry and "
                    "mayig_features (independent structured maps)",
            "medium": "attested by exactly one of canonical_registry "
                      "/ mayig_features, not contradicted by the other",
            "low": "attested only by crosswalk_v2 (rejected as "
                   "canonical, spec 018 A.4) or only by "
                   "candidates_unadmitted (no explicit source)",
            "none": "unmapped row (no M asserted by any source)",
        },
        "non_claims": [
            "Working v1 with stated confidence — not an adjudication "
            "of sign identity.",
            "No positional comparison study was run in this phase.",
            "No anchor-status implications follow from any row.",
        ],
        "marshall_numbering_note": "Kondratov's tables (Phase-121) use "
            "MARSHALL numbers, a third numbering. No Marshall<->M/P "
            "pairs were extractable from sources on main in this phase; "
            "no Marshall rows are asserted in v1.",
        "stats": xw["stats"],
        "rows": xw["rows"],
        "m_unmapped": xw["m_unmapped"],
    }
    OUT_XW_JSON.write_text(json.dumps(xw_json, indent=1, sort_keys=True),
                           encoding="utf-8")

    OUT_LAYER.parent.mkdir(parents=True, exist_ok=True)
    OUT_LAYER.write_text(json.dumps(layer, indent=1, sort_keys=True),
                         encoding="utf-8")
    OUT_LAYER_META.write_text(json.dumps(meta, indent=1, sort_keys=True),
                              encoding="utf-8")

    results = {
        "phase": 122,
        "crosswalk_stats": xw["stats"],
        "mayig_layer": meta,
        "coverage_tokens": dict(tok),
        "coverage_inscriptions": dict(insc),
        "coverage_tokens_registry_only": dict(tok_r),
        "coverage_inscriptions_registry_only": dict(insc_r),
        "top_failure_signs": fail_signs.most_common(15),
        "cisi_overlap": overlap,
        "cisi_overlap_basis": "Per-basis M-prefixed CISI object IDs "
            "obtainable now: djvu OCR regex extraction from the CISI "
            "Vol. 1 / Vol. 2 IA scans (partial — plates are images, "
            "OCR misses IDs), Bhaskar et al. 2024 ESM13 catalogue CISI "
            "ID column, and the Phase-116 keyed ICIT layer `cisi` "
            "field. Phase E will produce the full structured CISI "
            "catalogue table; these figures are provisional.",
        "artifacts": {
            "crosswalk_csv": str(OUT_XW_CSV.relative_to(REPO)),
            "crosswalk_json": str(OUT_XW_JSON.relative_to(REPO)),
            "mayig_layer": str(OUT_LAYER.relative_to(REPO)),
            "mayig_layer_meta": str(OUT_LAYER_META.relative_to(REPO)),
        },
    }
    OUT_RESULTS.write_text(json.dumps(results, indent=1, sort_keys=True),
                           encoding="utf-8")
    print(json.dumps({"crosswalk": xw["stats"], "mayig": meta,
                      "coverage_tokens": dict(tok),
                      "coverage_inscriptions": dict(insc),
                      "cisi_overlap": overlap}, indent=1))


if __name__ == "__main__":
    main()
