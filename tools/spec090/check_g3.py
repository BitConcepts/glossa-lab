#!/usr/bin/env python3
"""Spec 090 Stage G3 — T403 hand-check of the separator
implementation in `run_g3.py`, on a toy table whose
profile is worked by hand below from the freeze's
definitions (stage-g3-freeze-record.md §6/§7) and stated
as constants. The script under test must reproduce the
hand values exactly; any mismatch exits 1 with both
values printed.

The toy table (four objects, three codes):

    S1 = [a, b, a]        S2 = [a]
    S3 = [b, a]           S4 = [c, a, b, a]

HAND DERIVATION — A0 (the recorded coding).
Tokens: a = 2+1+1+2 = 6; b = 1+1+1 = 3; c = 1; total
10 tokens over 4 objects.
  |Sigma| = 3.  M = [6, 3, 1].
  L: lengths 3, 1, 2, 4, once each
     -> [[1,1],[2,1],[3,1],[4,1]].
  X: a: initial S1p0, S2p0 = 2; final S1p2, S2p0
     (one-token sequence counts in both), S3p1, S4p3
     = 4; medial S4p1 = 1  -> (2,4,1).
     b: initial S3p0 = 1; final none = 0; medial
     S1p1, S4p2 = 2  -> (1,0,2).
     c: initial S4p0 = 1; final 0; medial 0
     -> (1,0,0).
     X sorted -> [[1,0,0],[1,0,2],[2,4,1]].
  B: (a,b) in S1, S4 = 2; (b,a) in S1, S3, S4 = 3;
     (c,a) in S4 = 1 -> values sorted descending
     [3, 2, 1].

HAND DERIVATION — A1 (split the most frequent code,
a, by initial position; a's initial occurrences are
S1p0 and S2p0, 2 of its 6).
Type sequences: S1 = [aI, b, aN]; S2 = [aI];
S3 = [b, aN]; S4 = [c, aN, b, aN].
  Multiplicities: aI = 2, aN = 4, b = 3, c = 1
  -> |Sigma| = 4, M = [4, 3, 2, 1].  L unchanged.
  X: aI = (2,1,0) (final: S2's one-token sequence);
     aN = (0,3,1) (final S1p2, S3p1, S4p3; medial
     S4p1); b = (1,0,2); c = (1,0,0)
     -> [[0,3,1],[1,0,0],[1,0,2],[2,1,0]].
  B: (aI,b) = 1; (b,aN) = 3 (S1, S3, S4);
     (c,aN) = 1; (aN,b) = 1 -> [3, 1, 1, 1].

HAND DERIVATION — A3 (merge the two most frequent
codes, a (6) and b (3), into one type m).
Type sequences: S1 = [m, m, m]; S2 = [m];
S3 = [m, m]; S4 = [c, m, m, m].
  |Sigma| = 2.  M = [9, 1].  L unchanged.
  X: m: initial S1p0, S2p0, S3p0 = 3; final S1p2,
     S2p0, S3p1, S4p3 = 4; medial S1p1, S4p1, S4p2
     = 3 -> (3,4,3).  c = (1,0,0)
     -> [[1,0,0],[3,4,3]].
  B: (m,m) = 2 (S1) + 1 (S3) + 2 (S4) = 5;
     (c,m) = 1 -> [5, 1].

A2 ON THE TOY: the floor is 10 and the toy's largest
multiplicity is 6, so no two codes qualify — the case
must refuse as not formable (freeze §7), which is
also the floor branch's only mechanical test short of
H1 itself.

C1 ON THE TOY: the seeded bijection over [a, b, c]
must be a permutation, must rebuild identically, and
must leave the profile exactly A0's (the invariance
the control exists to test). C2 must equal A0.

Usage: python3 tools/spec090/check_g3.py
Prints one PASS line per check; exit 0 iff all pass.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("run_g3", HERE / "run_g3.py")
run_g3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_g3)

TOY = [
    ["a", "b", "a"],
    ["a"],
    ["b", "a"],
    ["c", "a", "b", "a"],
]

EXPECTED = {
    "A0": {
        "inventory_size": 3,
        "M": [6, 3, 1],
        "L": [[1, 1], [2, 1], [3, 1], [4, 1]],
        "X": [[1, 0, 0], [1, 0, 2], [2, 4, 1]],
        "B": [3, 2, 1],
    },
    "A1": {
        "inventory_size": 4,
        "M": [4, 3, 2, 1],
        "L": [[1, 1], [2, 1], [3, 1], [4, 1]],
        "X": [[0, 3, 1], [1, 0, 0], [1, 0, 2], [2, 1, 0]],
        "B": [3, 1, 1, 1],
    },
    "A3": {
        "inventory_size": 2,
        "M": [9, 1],
        "L": [[1, 1], [2, 1], [3, 1], [4, 1]],
        "X": [[1, 0, 0], [3, 4, 3]],
        "B": [5, 1],
    },
}

failures = 0


def check(name: str, actual, expected) -> None:
    global failures
    if actual == expected:
        print(f"PASS {name}")
    else:
        failures += 1
        print(f"FAIL {name}\n  expected: {expected!r}\n  actual:   {actual!r}")


def main() -> int:
    # A0: the full profile, by hand against the script.
    seqs, facts = run_g3.build_case("A0", TOY)
    check("toy A0 object count", len(seqs), 4)
    check("toy A0 token total", sum(len(s) for s in seqs), 10)
    check("toy A0 profile", run_g3.profile(seqs), EXPECTED["A0"])

    # A1: the positional split, by hand.
    seqs, facts = run_g3.build_case("A1", TOY)
    check("toy A1 split code", facts["split_code"], "a")
    check("toy A1 initial occurrences", facts["initial_occurrences"], 2)
    check("toy A1 other occurrences", facts["other_occurrences"], 4)
    check("toy A1 profile", run_g3.profile(seqs), EXPECTED["A1"])

    # A3: the head merger, by hand.
    seqs, facts = run_g3.build_case("A3", TOY)
    check("toy A3 merged codes", facts["merged_codes"], ["a", "b"])
    check("toy A3 multiplicities", facts["multiplicities"], [6, 3])
    check("toy A3 profile", run_g3.profile(seqs), EXPECTED["A3"])

    # A2: the floor refuses on the toy (no code >= 10).
    try:
        run_g3.build_case("A2", TOY)
    except run_g3.CaseNotFormable:
        print("PASS toy A2 floor refusal")
    else:
        check("toy A2 floor refusal", "case formed", "CaseNotFormable")

    # C1: permutation, deterministic, profile-invariant.
    seqs1, facts1 = run_g3.build_case("C1", TOY)
    seqs2, facts2 = run_g3.build_case("C1", TOY)
    check("toy C1 deterministic rebuild", seqs1, seqs2)
    check(
        "toy C1 bijection fingerprint stable",
        facts1["bijection_sha256"],
        facts2["bijection_sha256"],
    )
    check("toy C1 codes permuted", facts1["codes_permuted"], 3)
    check("toy C1 profile == A0 profile", run_g3.profile(seqs1), EXPECTED["A0"])

    # C2: the identity control equals A0.
    seqs, _ = run_g3.build_case("C2", TOY)
    check("toy C2 profile == A0 profile", run_g3.profile(seqs), EXPECTED["A0"])

    if failures:
        print(f"{failures} hand-check(s) FAILED")
        return 1
    print("all hand-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
