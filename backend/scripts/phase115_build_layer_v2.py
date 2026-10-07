#!/usr/bin/env python3
"""Phase-115 (spec 014 section 2) ICIT converted layer v2 builder.

Deterministic extension of the Phase-107 builder
(phase107_build_layers.py). Repairs the two measured v1 losses:

  1. Leading-zero key mismatch: the ICIT CSV writes Wells codes
     zero-padded ('002'); the canonical registry's Wells keys are
     integer-normalized ('2'). v1 looked up the raw padded code,
     so every sub-100 Wells sign failed (4,014 tokens). v2
     normalizes the lookup key with str(int(code)).
  2. All-or-nothing inscriptions: v1 discarded any inscription
     containing a placeholder ('000') or an unmapped code. v2
     emits sentinel positions ('UNK') for placeholders ('000'
     illegible, '999' blank — the source's own non-sign
     encodings) and for unmapped codes, retaining the
     inscription and the positional geometry of its mapped
     signs.

Dedupe (file order, keep first; Phase-107 independence rule
extended — spec 014 section 2.6): vs Holdat, an inscription of
length >= 3 with >= 2 mapped tokens is dropped if a Holdat
inscription of the same length matches it at every mapped
position; intra-layer, exact emitted-sequence equality
(length >= 3). Inscriptions with zero mapped tokens are dropped.

Outputs (under corpora/downloads/, gitignored; statistics only
are ever published):
  icit_fieldcady/icit_converted_v2.json
  layer_build_meta_v2.json   (v1 meta embedded for provenance)

Re-running this builder on the same inputs reproduces both
files byte-identically (verified at build time in Phase-115).
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

from glossa_lab.pipelines.sa_validation import load_holdat_corpus  # noqa: E402

CONF = {"HIGH": 3, "MEDIUM": 2, "CANDIDATE": 1}
DL = REPO / "corpora" / "downloads"
MAIN_DL = Path.home() / "workspace" / "glossa-lab" / "corpora" / "downloads"
SENTINEL = "UNK"
PLACEHOLDERS = {"000", "999"}


def downloads_dir() -> Path:
    """Worktree downloads if populated, else the main checkout's
    (Phase-113 fallback pattern)."""
    for cand in (DL, MAIN_DL):
        if (cand / "field_cady_icit").exists():
            return cand
    raise FileNotFoundError("corpora/downloads not found in worktree "
                            "or main checkout")


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
    'direct', 'chain', 'placeholder', 'unmapped'. Unmapped and
    placeholder codes emit the sentinel (spec 014 section 2)."""
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


def build_layer(rows, holdat_seqs, w2m, w2p, p2m):
    """Pure build: (kept inscriptions, stats dict). `rows` are
    CSV dicts with a 'text' field; deterministic in file order."""
    holdat_by_len: dict[int, list] = collections.defaultdict(list)
    for s in holdat_seqs:
        if len(s) >= 3:
            holdat_by_len[len(s)].append(tuple(s))
    stats: collections.Counter = collections.Counter()
    kept: list[list[str]] = []
    kept_exact: set = set()
    for r in rows:
        codes = re.findall(r"\d{3}", r.get("text") or "")
        if not codes:
            stats["empty_source"] += 1
            continue
        stats["source_inscriptions"] += 1
        stats["source_tokens"] += len(codes)
        seq, n_mapped = [], 0
        for c in codes:
            tok, kind = convert_code(c, w2m, w2p, p2m)
            seq.append(tok)
            stats[f"token_{kind}"] += 1
            if kind in ("direct", "chain"):
                n_mapped += 1
        if n_mapped == 0:
            stats["dropped_zero_mapped"] += 1
            continue
        if len(seq) >= 3 and n_mapped >= 2 and any(
                _matches_at_mapped_positions(seq, h)
                for h in holdat_by_len[len(seq)]):
            stats["dropped_dedupe_holdat"] += 1
            continue
        if len(seq) >= 3 and tuple(seq) in kept_exact:
            stats["dropped_dedupe_intra"] += 1
            continue
        kept.append(seq)
        kept_exact.add(tuple(seq))
    mapped = sum(1 for s in kept for t in s if t != SENTINEL)
    sentinels = sum(1 for s in kept for t in s if t == SENTINEL)
    sign_counts = collections.Counter(
        t for s in kept for t in s if t != SENTINEL)
    stats.update({
        "kept_inscriptions": len(kept),
        "kept_mapped_tokens": mapped,
        "kept_sentinel_tokens": sentinels,
        "distinct_signs_attested": len(sign_counts),
        "signs_ge2": sum(1 for v in sign_counts.values() if v >= 2),
        "signs_ge3": sum(1 for v in sign_counts.values() if v >= 3),
        "signs_ge8": sum(1 for v in sign_counts.values() if v >= 8),
    })
    non_placeholder = stats["source_tokens"] - stats["token_placeholder"]
    stats["token_map_coverage_excl_placeholders"] = round(
        (stats["token_direct"] + stats["token_chain"]) / non_placeholder, 6)
    return kept, dict(stats)


def main() -> int:
    dl = downloads_dir()
    holdat_seqs = load_holdat_corpus()[1]
    p2m = p_to_m_map()
    w2m, w2p = wells_maps()
    csv_path = (dl / "field_cady_icit" / "indus_valley_script_corpus-main"
                / "inscriptions.csv")
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    kept, stats = build_layer(rows, holdat_seqs, w2m, w2p, p2m)
    out_dir = dl / "icit_fieldcady"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "icit_converted_v2.json").write_text(json.dumps({
        "source": "ICIT via Lipi repository CSV export, mirrored (MIT) in "
                  "field-cady/indus_valley_script_corpus; Wells/ICIT "
                  "numbers -> M via canonical sign registry (+ crosswalk "
                  "v2 chain), key-normalized; unmapped/placeholder "
                  "positions emitted as UNK sentinels (Phase-115, "
                  "spec 014 section 2)",
        "inscriptions": kept,
    }))
    meta = {"icit_v2": stats}
    v1_meta_path = dl / "layer_build_meta.json"
    if v1_meta_path.exists():
        meta["icit_v1_phase107"] = json.loads(
            v1_meta_path.read_text()).get("icit")
    (dl / "layer_build_meta_v2.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
