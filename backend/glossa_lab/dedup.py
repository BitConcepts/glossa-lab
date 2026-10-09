"""Shared deduplication protocol — spec 018 (Phase-119) §5,
lifted verbatim from `glossa_lab.pred_harness` by Phase-130
(spec 021, intake pack) so the Phase-119 harness and the
intake pipeline run ONE implementation. No behaviour change:
the algorithm, stage order, keep-first rule, UNK handling,
Stage-C length floor (>= 4 on UNK-stripped sequences) and
kept-anchor-only comparison are exactly the frozen §5 text
as implemented for Phase-119. `pred_harness.dedup` re-exports
this function; Phase-119's measured numbers (spec 018
Appendix A.6: input 4,531 -> kept 2,446; stage removals
1,468 / 370 / 247; cumulative removal 46.02% on the ICIT
converted layer, P-space) must reproduce through this module
— asserted in `tests/test_phase130_intake_pack.py`.

Records are plain dicts with a `tokens` list (adapter-emitted
P-space sequences for the harness; declared-space token lists
for pre-adapter intake pre-checks — the protocol is
space-agnostic, operating only on token equality).
"""
from __future__ import annotations


def levenshtein_le1(a: tuple, b: tuple) -> bool:
    """True iff Levenshtein distance between a and b is <= 1."""
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(1 for x, y in zip(a, b) if x != y) <= 1
    if len(a) > len(b):
        a, b = b, a
    i = j = diff = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            j += 1
            diff += 1
            if diff > 1:
                return False
    return True


# Backwards-compatible private alias (Phase-119 name).
_lev_le1 = levenshtein_le1


def dedup(records: list[dict]) -> tuple[list[dict], dict]:
    """Frozen dedup protocol (spec 018 section 5): stage A exact,
    stage B sentinel-normalized exact, stage C near-duplicate
    (Levenshtein <= 1 on UNK-stripped sequences of length >= 4,
    greedy keep-first against kept anchors only)."""
    def strip(tokens):
        return tuple(t for t in tokens if t != "UNK")

    seen_a: set = set()
    kept_a = []
    for r in records:
        key = tuple(r["tokens"])
        if key not in seen_a:
            seen_a.add(key)
            kept_a.append(r)
    seen_b: set = set()
    kept_b = []
    for r in kept_a:
        st = strip(r["tokens"])
        if st and st in seen_b:
            continue
        if st:
            seen_b.add(st)
        kept_b.append(r)
    anchors: list[tuple] = []
    kept_c = []
    removed_c = 0
    for r in kept_b:
        st = strip(r["tokens"])
        if len(st) >= 4:
            if any(levenshtein_le1(st, a) for a in anchors):
                removed_c += 1
                continue
            anchors.append(st)
        kept_c.append(r)
    counts = {
        "input": len(records),
        "stage_a_removed": len(records) - len(kept_a),
        "stage_b_removed": len(kept_a) - len(kept_b),
        "stage_c_removed": removed_c,
        "kept": len(kept_c),
    }
    return kept_c, counts
