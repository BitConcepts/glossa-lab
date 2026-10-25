#!/usr/bin/env python3
"""Route 2 — census verification for a recovered `indusarrays` JSONL.

Implements Part 4 (gates V1–V4) of the Route 2 recovery procedure
(files/2026-10-24-route2-indusarrays-recovery.md). The reconstruction
mirrors, rule for rule, the repo's unmodified loader
`backend/glossa_lab/data/indus_corpus_v3.py` (the intake itself also
runs that loader; this tool is the standalone pre-check whose numbers
must agree with it). The positional profiles and `terminal_frac`
mirror `backend/scripts/phase43_part2.py` (the Phase-43 record of
record, T2.2/T2.4).

USAGE
  python3 route2_verify_census.py FILE.jsonl [--expect EXPECT.json]
  python3 route2_verify_census.py --lines-only FILE.jsonl   (V1 only)

Without --expect, the file is judged against the frozen T1_1 census:
  V1  lines == 3,916
  V2  sequences 3,137 · dockeys 2,665 · instances 12,494 ·
      numeric 12,868 · star 504 · range [1001, 9905] · mean 3.98
  V3  full top-20 sign frequencies (342=1,318, 99=642, 267=356,
      176=344, 87=344, 59=334, 89=299, 328=299, 67=269, 336=225,
      169=223, 211=218, 65=203, 162=202, 245=201, 123=187, 391=183,
      72=181, 343=168, 249=161)
  V4  terminal_frac(267) == 0.038 and terminal_frac(72) == 0.259
      under the Phase-43 definitions below.

With --expect, the same quantities are judged against the JSON file's
values (used by the fixture tests). Exit 0 = all gates pass, 1 = a
gate failed, 3 = usage/IO error. A JSON report is printed to stdout.

Phase-43 definitions (part2, verbatim semantics):
  - positional profiles are computed over reconstructed sequences;
    a sign with total < 5 gets no profile;
    role cascade: t_rate >= 0.60 TERMINAL_STRONG; i_rate >= 0.55
    INITIAL_STRONG; m_rate >= 0.65 MEDIAL_STRONG; t_rate >= 0.40
    TERMINAL_MODERATE; i_rate >= 0.40 INITIAL_MODERATE; else MIXED;
  - for a fish candidate F with total >= 10: bigrams_after counts the
    sign following each occurrence of F; terminal_after sums bigram
    counts whose follower's role is TERMINAL_STRONG/TERMINAL_MODERATE;
    terminal_frac = round(terminal_after / total_bigrams, 3).
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

S_FIELDS = [f"S{i}" for i in range(1, 15)]
FISH_CANDIDATES = [267, 72, 65, 59, 60, 64, 70]

T1_1 = {
    "lines": 3916,
    "parsed_records": 3916,
    "unique_dockeys": 2665,
    "total_sequences": 3137,
    "total_sign_instances": 12494,
    "mean_inscription_length": 3.98,
    "numeric_mahadevan": 12868,
    "star_nnn_filtered": 504,
    "dockey_range": [1001, 9905],
    "top_20": [[342, 1318], [99, 642], [267, 356], [176, 344], [87, 344],
               [59, 334], [89, 299], [328, 299], [67, 269], [336, 225],
               [169, 223], [211, 218], [65, 203], [162, 202], [245, 201],
               [123, 187], [391, 183], [72, 181], [343, 168], [249, 161]],
    "terminal_frac": {"267": 0.038, "72": 0.259},
}


def is_valid_sign(v) -> bool:
    """Mirror of the loader's _is_valid_sign."""
    if not v and v != 0:
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


def load_records(path: Path):
    lines = 0
    records = []
    raw = path.read_text(encoding="utf-8")
    for line in raw.splitlines():
        if line.strip():
            lines += 1
            try:
                records.append(json.loads(line))
            except Exception:
                pass
    return lines, records


def reconstruct(records):
    """Mirror of the loader's _reconstruct_sequences."""
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
        clean = [int(v) for v in texts if is_valid_sign(v)]
        if len(clean) < 2:
            clean = [int(r[sf]) for sf in S_FIELDS if is_valid_sign(r.get(sf, ""))]
        if len(clean) >= 2:
            key = (dockey, sideline)
            if key not in by_key or len(clean) > len(by_key[key]):
                by_key[key] = clean
    result: dict = defaultdict(list)
    for (dockey, _sideline), signs in by_key.items():
        result[dockey].append(signs)
    return dict(result)


def s_field_counts(records):
    numeric = star = 0
    for r in records:
        for sf in S_FIELDS:
            v = str(r.get(sf, ""))
            if not v or v == "0":
                continue
            elif v.startswith("*"):
                star += 1
            else:
                try:
                    int(v)
                    numeric += 1
                except ValueError:
                    pass
    return numeric, star


def positional_profiles(seqs):
    sign_pos = defaultdict(lambda: {"I": 0, "M": 0, "T": 0, "total": 0})
    for seq in seqs:
        if len(seq) < 2:
            continue
        for i, s in enumerate(seq):
            sign_pos[s]["total"] += 1
            if i == 0:
                sign_pos[s]["I"] += 1
            elif i == len(seq) - 1:
                sign_pos[s]["T"] += 1
            else:
                sign_pos[s]["M"] += 1
    profiles = {}
    for s, c in sign_pos.items():
        tot = c["total"]
        if tot < 5:
            continue
        t, ii, m = c["T"] / tot, c["I"] / tot, c["M"] / tot
        if t >= 0.60:
            role = "TERMINAL_STRONG"
        elif ii >= 0.55:
            role = "INITIAL_STRONG"
        elif m >= 0.65:
            role = "MEDIAL_STRONG"
        elif t >= 0.40:
            role = "TERMINAL_MODERATE"
        elif ii >= 0.40:
            role = "INITIAL_MODERATE"
        else:
            role = "MIXED"
        profiles[s] = {"t_rate": round(t, 3), "i_rate": round(ii, 3),
                       "m_rate": round(m, 3), "total": tot, "role": role}
    return profiles


def terminal_frac(seqs, profiles, fish):
    bigrams_after = Counter()
    fish_total = 0
    for seq in seqs:
        for i, s in enumerate(seq):
            if s == fish:
                fish_total += 1
                if i < len(seq) - 1:
                    bigrams_after[seq[i + 1]] += 1
    if fish_total < 10:
        return None
    terminal_after = sum(
        v for k, v in bigrams_after.items()
        if profiles.get(k, {}).get("role") in ("TERMINAL_STRONG", "TERMINAL_MODERATE"))
    return round(terminal_after / max(sum(bigrams_after.values()), 1), 3)


def census(path: Path) -> dict:
    lines, records = load_records(path)
    seqs_by_dockey = reconstruct(records)
    all_seqs = [seq for seqs in seqs_by_dockey.values() for seq in seqs]
    all_signs = [s for seq in all_seqs for s in seq]
    numeric, star = s_field_counts(records)
    profiles = positional_profiles(all_seqs)
    fracs = {}
    for fish in FISH_CANDIDATES:
        f = terminal_frac(all_seqs, profiles, fish)
        if f is not None:
            fracs[str(fish)] = f
    return {
        "lines": lines,
        "parsed_records": len(records),
        "unique_dockeys": len(seqs_by_dockey),
        "total_sequences": len(all_seqs),
        "total_sign_instances": len(all_signs),
        "mean_inscription_length": round(
            sum(len(s) for s in all_seqs) / max(len(all_seqs), 1), 2),
        "numeric_mahadevan": numeric,
        "star_nnn_filtered": star,
        "dockey_range": ([min(seqs_by_dockey), max(seqs_by_dockey)]
                         if seqs_by_dockey else []),
        "top_20": [[s, c] for s, c in Counter(all_signs).most_common(20)],
        "sign_frequencies": {str(s): c for s, c in Counter(all_signs).items()},
        "terminal_frac": fracs,
        "profiles": {str(s): p for s, p in profiles.items()},
    }


def judge(measured: dict, expect: dict) -> dict:
    gates = {}
    gates["V1_lines"] = measured["lines"] == expect["lines"]
    v2_keys = ["unique_dockeys", "total_sequences", "total_sign_instances",
               "numeric_mahadevan", "star_nnn_filtered", "dockey_range",
               "mean_inscription_length"]
    gates["V2_census"] = all(measured[k] == expect[k] for k in v2_keys)
    gates["V3_top20"] = measured["top_20"] == [list(p) for p in expect["top_20"]]
    exp_frac = {str(k): v for k, v in expect.get("terminal_frac", {}).items()}
    gates["V4_terminal_frac"] = all(
        measured["terminal_frac"].get(k) == v for k, v in exp_frac.items())
    gates["ALL"] = all(gates.values())
    return gates


def main(argv: list[str]) -> int:
    rest = list(argv[1:])
    expect = T1_1
    if "--expect" in rest:
        i = rest.index("--expect")
        expect = json.loads(Path(rest[i + 1]).read_text(encoding="utf-8"))
        del rest[i:i + 2]
    lines_only = "--lines-only" in rest
    args = [a for a in rest if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 3
    path = Path(args[0])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 3
    measured = census(path)
    if lines_only:
        print(json.dumps({"lines": measured["lines"],
                          "V1_lines": measured["lines"] == expect["lines"]}))
        return 0 if measured["lines"] == expect["lines"] else 1
    gates = judge(measured, expect)
    report = {"file": str(path), "measured": {k: v for k, v in measured.items()
                                              if k not in ("sign_frequencies", "profiles")},
              "gates": gates}
    print(json.dumps(report, indent=1))
    return 0 if gates["ALL"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
