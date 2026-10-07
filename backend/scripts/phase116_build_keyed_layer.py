#!/usr/bin/env python3
"""Phase-116 (spec 015 section 2) keyed ICIT converted layer builder.

Rebuilds the spec-014 section 2 conversion (the Phase-115 v2
layer policy) with full provenance retained per inscription:
source row index, source ``id``, ``cisi``, ``site``,
``material``, ``type``, ``sides``, ``dir.``, the emitted token
sequence, the per-token conversion kind
(direct/chain/placeholder/unmapped), and the inscription's
build status (kept / dropped_holdat_dup / dropped_intra_dup /
dropped_zero_mapped / empty_source).

The conversion policy is replicated exactly from
``phase115_build_layer_v2.py`` (spec 014 section 2): parse
``\\d{3}`` codes in file order; normalize the lookup key with
``str(int(code))``; map via the canonical registry (Wells->M
direct, else Wells->Parpola->crosswalk-v2 chain); placeholders
``000``/``999`` and unmapped codes emit the ``UNK`` sentinel;
zero-mapped inscriptions dropped; Holdat wildcard dedupe;
intra-layer exact dedupe.

Assertions (spec 015 section 2): the kept subset reproduces the
Phase-115 v2 layer exactly -- 4,531 inscriptions, 13,492 mapped
tokens, 2,388 sentinel tokens, sequences identical in order and
content to the stored ``icit_converted_v2.json`` -- and the
pre-Holdat-dedupe population (kept + dropped_holdat_dup) is
4,614 inscriptions.

Output (under corpora/downloads/, gitignored; statistics only
are ever published):
  icit_fieldcady/icit_converted_v2_keyed.json
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

CONF = {"HIGH": 3, "MEDIUM": 2, "CANDIDATE": 1}
DL = REPO / "corpora" / "downloads"
MAIN_DL = Path.home() / "workspace" / "glossa-lab" / "corpora" / "downloads"
SENTINEL = "UNK"
PLACEHOLDERS = {"000", "999"}


def downloads_dir() -> Path:
    """Worktree downloads if populated, else the main checkout's
    (Phase-113/115 fallback pattern)."""
    for cand in (DL, MAIN_DL):
        if (cand / "field_cady_icit").exists():
            return cand
    raise FileNotFoundError("corpora/downloads not found in worktree "
                            "or main checkout")


def load_holdat_sequences(dl: Path) -> list[list[str]]:
    """Exact replica of the phase113 loader grouping (loader
    logic only): Holdat CSV rows grouped by cisi_number at their
    position index, empties dropped."""
    csv_path = (dl / "external_repos" / "holdatllc_indus"
                / "indus_corpus 2.csv")
    seals: dict[str, list] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
    return [[s for s in v if s] for v in seals.values() if any(v)]


def p_to_m_map() -> dict[str, str]:
    data = json.loads(
        (REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json")
        .read_text())
    best: dict[str, tuple[str, int]] = {}
    for e in list(data["crosswalk"].values()):
        p = e.get("parpola_id") or e.get("p_id")
        m = e.get("mahadevan_id") or e.get("m_id")
        c = CONF.get(e.get("confidence", "CANDIDATE"), 1)
        if p and m and (p not in best or c > best[p][1]):
            best[p] = (m, c)
    return {p: m for p, (m, _) in best.items()}


def wells_maps() -> tuple[dict[str, str], dict[str, str]]:
    reg = list(
        csv.DictReader((REPO / "data/crosswalks/canonical_sign_registry.csv").open())
    )

    def single(v: str | None) -> str | None:
        v = (v or "").strip()
        return v if v and "|" not in v else None

    w2m: dict[str, str] = {}
    w2p: dict[str, str] = {}
    for r in reg:
        p, m = single(r.get("parpola_id")), single(r.get("mahadevan_ids"))
        for w in (r.get("wells_ids") or "").split("|"):
            w = w.strip().lstrip("Ww")
            if not w:
                continue
            k = str(int(w)) if w.isdigit() else w
            if m:
                w2m.setdefault(k, m)
            if p:
                w2p.setdefault(k, p)
    return w2m, w2p


def normalize_code(raw: str) -> str:
    """Zero-padded CSV code -> registry key form ('002' -> '2')."""
    return str(int(raw)) if raw.isdigit() else raw


def convert_code(raw: str, w2m, w2p, p2m) -> tuple[str, str]:
    """One source code -> (emitted token, kind); kind is one of
    'direct', 'chain', 'placeholder', 'unmapped'."""
    if raw in PLACEHOLDERS:
        return SENTINEL, "placeholder"
    k = normalize_code(raw)
    if k in w2m:
        return w2m[k], "direct"
    p = w2p.get(k)
    if p and p in p2m:
        return p2m[p], "chain"
    return SENTINEL, "unmapped"


def _matches_at_mapped_positions(candidate, holdat_seq) -> bool:
    if len(candidate) != len(holdat_seq):
        return False
    return all(c == h or c == SENTINEL
               for c, h in zip(candidate, holdat_seq))


def build_keyed_layer(rows, holdat_seqs, w2m, w2p, p2m):
    """Pure build replicating phase115 build_layer's decisions,
    retaining provenance. Returns (records, stats) where records
    cover every source row with codes (plus empty_source rows
    with an empty token list)."""
    holdat_by_len: dict[int, list] = collections.defaultdict(list)
    for s in holdat_seqs:
        if len(s) >= 3:
            holdat_by_len[len(s)].append(tuple(s))
    stats: collections.Counter = collections.Counter()
    records: list[dict] = []
    kept_exact: set = set()
    for idx, r in enumerate(rows):
        codes = re.findall(r"\d{3}", r.get("text") or "")
        rec = {
            "row": idx,
            "id": (r.get("id") or "").strip(),
            "cisi": (r.get("cisi") or "").strip(),
            "site": (r.get("site") or "").strip(),
            "material": (r.get("material") or "").strip(),
            "type": (r.get("type") or "").strip(),
            "sides": (r.get("sides") or "").strip(),
            "dir": (r.get("dir.") or "").strip(),
            "tokens": [],
            "kinds": [],
            "codes": [],
        }
        if not codes:
            stats["empty_source"] += 1
            rec["status"] = "empty_source"
            records.append(rec)
            continue
        stats["source_inscriptions"] += 1
        stats["source_tokens"] += len(codes)
        seq, kinds, n_mapped = [], [], 0
        for c in codes:
            tok, kind = convert_code(c, w2m, w2p, p2m)
            seq.append(tok)
            kinds.append(kind)
            stats[f"token_{kind}"] += 1
            if kind in ("direct", "chain"):
                n_mapped += 1
        rec["tokens"] = seq
        rec["kinds"] = kinds
        rec["codes"] = list(codes)
        if n_mapped == 0:
            stats["dropped_zero_mapped"] += 1
            rec["status"] = "dropped_zero_mapped"
        elif len(seq) >= 3 and n_mapped >= 2 and any(
                _matches_at_mapped_positions(seq, h)
                for h in holdat_by_len[len(seq)]):
            stats["dropped_dedupe_holdat"] += 1
            rec["status"] = "dropped_holdat_dup"
        elif len(seq) >= 3 and tuple(seq) in kept_exact:
            stats["dropped_dedupe_intra"] += 1
            rec["status"] = "dropped_intra_dup"
        else:
            rec["status"] = "kept"
            kept_exact.add(tuple(seq))
        records.append(rec)
    kept = [r for r in records if r["status"] == "kept"]
    mapped = sum(1 for r in kept for t in r["tokens"] if t != SENTINEL)
    sentinels = sum(1 for r in kept for t in r["tokens"] if t == SENTINEL)
    sign_counts = collections.Counter(
        t for r in kept for t in r["tokens"] if t != SENTINEL)
    stats.update({
        "kept_inscriptions": len(kept),
        "kept_mapped_tokens": mapped,
        "kept_sentinel_tokens": sentinels,
        "distinct_signs_attested": len(sign_counts),
        "signs_ge2": sum(1 for v in sign_counts.values() if v >= 2),
        "signs_ge3": sum(1 for v in sign_counts.values() if v >= 3),
        "signs_ge8": sum(1 for v in sign_counts.values() if v >= 8),
        "matcher_population": sum(
            1 for r in records
            if r["status"] in ("kept", "dropped_holdat_dup")),
    })
    non_placeholder = stats["source_tokens"] - stats["token_placeholder"]
    stats["token_map_coverage_excl_placeholders"] = round(
        (stats["token_direct"] + stats["token_chain"]) / non_placeholder, 6)
    return records, dict(stats)


def main() -> int:
    dl = downloads_dir()
    holdat_seqs = load_holdat_sequences(dl)
    assert len(holdat_seqs) == 1670, len(holdat_seqs)
    assert sum(len(s) for s in holdat_seqs) == 7002
    p2m = p_to_m_map()
    w2m, w2p = wells_maps()
    csv_path = (dl / "field_cady_icit" / "indus_valley_script_corpus-main"
                / "inscriptions.csv")
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    records, stats = build_keyed_layer(rows, holdat_seqs, w2m, w2p, p2m)

    # Spec 015 section 2 assertions: the kept subset reproduces
    # the Phase-115 v2 layer exactly.
    kept_seqs = [r["tokens"] for r in records if r["status"] == "kept"]
    assert stats["kept_inscriptions"] == 4531, stats["kept_inscriptions"]
    assert stats["kept_mapped_tokens"] == 13492, stats["kept_mapped_tokens"]
    assert stats["kept_sentinel_tokens"] == 2388, stats["kept_sentinel_tokens"]
    assert stats["matcher_population"] == 4614, stats["matcher_population"]
    v2_path = dl / "icit_fieldcady" / "icit_converted_v2.json"
    stored = json.loads(v2_path.read_text("utf-8"))["inscriptions"]
    assert kept_seqs == [list(x) for x in stored], \
        "kept sequences differ from stored icit_converted_v2.json"

    out_path = dl / "icit_fieldcady" / "icit_converted_v2_keyed.json"
    out_path.write_text(json.dumps({
        "source": "ICIT via Lipi repository CSV export, mirrored (MIT) in "
                  "field-cady/indus_valley_script_corpus; Wells/ICIT "
                  "numbers -> M via canonical sign registry (+ crosswalk "
                  "v2 chain), key-normalized; unmapped/placeholder "
                  "positions emitted as UNK sentinels (Phase-116, "
                  "spec 015 section 2: spec-014 policy with provenance "
                  "retained)",
        "build_stats": stats,
        "inscriptions": records,
    }))
    print(json.dumps(stats, indent=1))
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
