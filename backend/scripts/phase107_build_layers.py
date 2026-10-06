#!/usr/bin/env python3
"""Phase-107 Step 4 layer builder: convert the ICIT export to an M-sign layer.

Output (under corpora/downloads/, gitignored):
  icit_fieldcady/icit_converted.json — ICIT inscriptions as exported by the
      Lipi repository and mirrored (MIT) in field-cady/indus_valley_script_corpus
      (inscriptions.csv, Wells/ICIT sign numbers), converted to M-signs via
      the canonical sign registry (Wells->M direct, else Wells->Parpola->
      M via crosswalk v2); fully-convertible inscriptions only ('000' =
      illegible-sign placeholder excludes an inscription).

(The in-repo CISI subset is converted by phase107_corpus_pool.py itself,
which owns the crosswalk-inversion logic; it is not duplicated here.)

The layer is deduplicated against the Holdat corpus (exact sign-sequence
match, length >= 3). Conversion coverage is printed and also written to
corpora/downloads/layer_build_meta.json.

CORRECTION (2026-10-05, continuation audit): the first build indexed the
Holdat *flat token list* instead of its inscription sequences, so the
seen-set held per-sign character tuples and NO Holdat dedupe actually
fired (only intra-ICIT dedupe did). Fixed below to index inscription
sequences; the layer was rebuilt and reports/phase107_acquisition_log.json
corrected before first commit. The pooling script
(phase107_corpus_pool.py) independently re-dedupes every layer against
the accumulated pool, so pooled-run numbers were never affected.
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


def p_to_m_map() -> dict[str, str]:
    data = json.loads(
        (REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json").read_text()
    )
    entries = list(data["crosswalk"].values())
    best: dict[str, tuple[str, int]] = {}
    for e in entries:
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


def main() -> int:
    holdat_seqs = load_holdat_corpus()[1]  # inscriptions, NOT the flat list
    seen = {tuple(s) for s in holdat_seqs if len(s) >= 3}
    p2m = p_to_m_map()
    meta: dict = {"holdat_sequences_indexed": len(seen)}

    # ---- ICIT layer (field-cady MIT mirror of Lipi exports) ----
    csv_path = (
        DL
        / "field_cady_icit"
        / "indus_valley_script_corpus-main"
        / "inscriptions.csv"
    )
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    w2m, w2p = wells_maps()

    def conv_code(code: str) -> str | None:
        if code in w2m:
            return w2m[code]
        p = w2p.get(code)
        if p and p in p2m:
            return p2m[p]
        return None

    seqs = [re.findall(r"\d{3}", r.get("text") or "") for r in rows]
    total_tokens = sum(len(s) for s in seqs)
    mapped_tokens = sum(
        1 for s in seqs for c in s if c != "000" and conv_code(c)
    )
    conv2 = []
    for s in seqs:
        if not s or any(c == "000" or conv_code(c) is None for c in s):
            continue
        conv2.append([conv_code(c) for c in s])
    kept2 = []
    for s in conv2:
        t = tuple(s)
        if len(s) >= 3 and t in seen:
            continue
        seen.add(t)
        kept2.append(s)
    out_dir2 = DL / "icit_fieldcady"
    out_dir2.mkdir(parents=True, exist_ok=True)
    (out_dir2 / "icit_converted.json").write_text(
        json.dumps(
            {
                "source": "ICIT via Lipi repository CSV export, mirrored (MIT) in "
                "field-cady/indus_valley_script_corpus; Wells/ICIT numbers -> M via "
                "canonical sign registry (+ crosswalk v2 chain)",
                "inscriptions": kept2,
            }
        )
    )
    meta["icit"] = {
        "source_inscriptions": len(rows),
        "source_tokens": total_tokens,
        "token_map_coverage_excl_000": mapped_tokens,
        "fully_convertible": len(conv2),
        "after_dedupe": len(kept2),
        "tokens_kept": sum(len(s) for s in kept2),
    }
    print(json.dumps(meta, indent=1))
    (DL / "layer_build_meta.json").write_text(json.dumps(meta, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
