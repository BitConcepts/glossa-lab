#!/usr/bin/env python3
"""Spec 090 Stage G3 — T404 INDEPENDENT AUDIT of the T403
administration.

Written from the freeze record alone
(`records/stage-g3-freeze-record.md`, sections 1-9): the
extraction (section 2), the profile P(T) (section 6),
the case constructions and tie-breaking (section 7),
the C1 seed rule and bijection construction (section
8), and the bar (section 9). This script does NOT
import or execute tools/spec090/run_g3.py; the
executor's tool was read only to learn the run records'
format and the bijection hash's canonical serialization
(JSON list of [from, to] pairs in ascending code order),
which this script reproduces from its own independently
regenerated bijection.

It recomputes every profile from the pinned snapshot,
compares component by component against the six
committed run records, re-applies the frozen bar to the
recomputed profiles, verifies the outcome record's
quoted numbers (including the profile and result-block
SHA-256 values under the canonical JSON form that
reproduces them (sorted keys, default separators,
ensure_ascii=False, UTF-8; identified among the standard
candidates and verified against every quoted value), and
checks the arithmetic identities the outcome record
cites. Prints an AUDIT-SUMMARY block; exit 0 iff every
recomputation agrees (fidelity findings about evidence
location are printed, not folded into the exit code).

Usage: python3 tools/spec090/audit_g3.py [--repo PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

FROZEN_SNAPSHOT_SHA256 = (
    "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e"
)
FROZEN_FLAT_SHA256 = (
    "878fd2231929f2105cb5c7fb37507ee7eceb7d83f355f1fa4d8e793926785c18"
)
FROZEN_SEED_DIGEST = (
    "0b9797c580fd2ca2786c98bcd2fd484b706d178da7968c05de423bf696e501b4"
)
FROZEN_SEED = 835303130428943522
FROZEN_RECORDS = 2906
FROZEN_TOKENS = 12639
A2_FLOOR = 10

# The outcome record's quoted values (stage-g3-outcome-record.md).
QUOTED_PROFILE_SHA256 = {
    "A0": "6e58de70a7e92c8abc121b4a79486d55e0ecf71795f120589a85eba89f84edfa",
    "A1": "868a2cae71b88992b150f783eec8e9e47e4fc359ae5645a1644aeb0d4081bc01",
    "A2": "805dcc3119f23efcc27e9e77b48bf5fadc5ec699c2ae1b94c8c85bfdbe31fd20",
    "A3": "3e1eb15d777eb8d7dc7c4689633f90738ab6e0fddeee106b5bded5889f306bbb",
    "C1": "6e58de70a7e92c8abc121b4a79486d55e0ecf71795f120589a85eba89f84edfa",
    "C2": "6e58de70a7e92c8abc121b4a79486d55e0ecf71795f120589a85eba89f84edfa",
}
QUOTED_RESULT_SHA256 = {  # outcome section 2(a): both runs, one value
    "A0": "801b36a145c952a5346a35fd158cca4654353feb31cabf82c7b92633e1a0b70f",
    "A1": "c9c8918162a0f25b4a8623ac13ebf707924cb04811349aa90083cc8d31e5ce04",
    "A2": "1617cea688152955100e5e03f106d8299320a46aedf912f130ec015c4b958d0b",
    "A3": "242fb3895baa5ab52aadefac764d789e70030544bd92533b5d713e8a638da6d3",
    "C1": "8db4a284db0a4790dc5d076a7048f549099767e33d70757df606595af9f783f3",
    "C2": "1672a6c90f7dbf4dcb1366b77886c2cf0707a08f98021f09e568fc85231167f3",
}
QUOTED_BIJECTION_SHA256 = (
    "cc4c4803984d60043cace35b473d167c7777c77e47e47d43f28111b0896bc61b"
)
ADMIN_RUN_IDS = {
    "A0": "study-20261112T152008Z-ec336a",
    "A1": "study-20261112T152009Z-22d5aa",
    "A2": "study-20261112T152010Z-82d88c",
    "A3": "study-20261112T152010Z-2ca7ad",
    "C1": "study-20261112T152011Z-aa19c6",
    "C2": "study-20261112T152011Z-95250e",
}

problems: list[str] = []


def note(ok: bool, label: str, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        problems.append(label)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha256(payload) -> str:
    # The form that reproduces the outcome record's quoted
    # profile and result-block hashes: sorted keys, JSON
    # default separators, ensure_ascii=False, UTF-8.
    data = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Freeze section 2: extraction. Freeze section 6: P(T). Written for this
# audit from those definitions.


def extract_h1(snapshot: Path):
    sequences: list[list[str]] = []
    by_system: Counter[str] = Counter()
    m77_records = 0
    empty_lists = 0
    nonstring_elements = 0
    total_records = 0
    with snapshot.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            total_records += 1
            record = json.loads(line)
            by_system[record.get("source_system")] += 1
            if record.get("source_system") != "indusscript-m77":
                continue
            m77_records += 1
            seq = record.get("canonical_grapheme_ids")
            if not seq:
                empty_lists += 1
                continue
            for element in seq:
                if not isinstance(element, str):
                    nonstring_elements += 1
            sequences.append(list(seq))
    return sequences, {
        "total_records": total_records,
        "by_system": dict(by_system),
        "m77_records": m77_records,
        "empty_lists": empty_lists,
        "nonstring_elements": nonstring_elements,
    }


def profile_of(sequences):
    """P(T) per freeze section 6; returns (profile, multiplicity)."""
    multiplicity: Counter[str] = Counter()
    length_counts: Counter[int] = Counter()
    positional: dict[str, list[int]] = {}
    pair_counts: Counter[tuple[str, str]] = Counter()
    for seq in sequences:
        n = len(seq)
        length_counts[n] += 1
        for i, tok in enumerate(seq):
            multiplicity[tok] += 1
            triple = positional.setdefault(tok, [0, 0, 0])
            if i == 0:
                triple[0] += 1
            if i == n - 1:
                triple[1] += 1
            if 0 < i < n - 1:
                triple[2] += 1
            if i + 1 < n:
                pair_counts[(tok, seq[i + 1])] += 1
    prof = {
        "inventory_size": len(multiplicity),
        "M": sorted(multiplicity.values(), reverse=True),
        "L": [[length, length_counts[length]] for length in sorted(length_counts)],
        "X": sorted(positional.values()),
        "B": sorted(pair_counts.values(), reverse=True),
    }
    return prof, multiplicity


def build_cases(sequences, multiplicity):
    """Freeze section 7 constructions + section 8 bijection."""
    desc = sorted(multiplicity, key=lambda c: (-multiplicity[c], c))
    asc = sorted(multiplicity, key=lambda c: (multiplicity[c], c))
    cases: dict[str, list[list[str]]] = {}
    facts: dict[str, dict] = {}

    cases["A0"] = [list(s) for s in sequences]
    facts["A0"] = {}
    cases["C2"] = [list(s) for s in sequences]
    facts["C2"] = {}

    head = desc[0]
    init_label, other_label = f"{head}#pos-initial", f"{head}#pos-other"
    out, n_init = [], 0
    for seq in sequences:
        mapped = []
        for i, tok in enumerate(seq):
            if tok == head and i == 0:
                mapped.append(init_label)
                n_init += 1
            elif tok == head:
                mapped.append(other_label)
            else:
                mapped.append(tok)
        out.append(mapped)
    cases["A1"] = out
    facts["A1"] = {
        "split_code": head,
        "split_code_multiplicity": multiplicity[head],
        "initial_occurrences": n_init,
        "other_occurrences": multiplicity[head] - n_init,
    }

    candidates = [c for c in asc if multiplicity[c] >= A2_FLOOR]
    a, b = candidates[0], candidates[1]
    label = f"merged#{a}+{b}"
    cases["A2"] = [
        [label if tok in (a, b) else tok for tok in seq] for seq in sequences
    ]
    facts["A2"] = {
        "merged_codes": [a, b],
        "multiplicities": [multiplicity[a], multiplicity[b]],
        "floor": A2_FLOOR,
        "codes_below_floor": sum(
            1 for c in multiplicity if multiplicity[c] < A2_FLOOR
        ),
    }

    a3, b3 = desc[0], desc[1]
    label3 = f"merged#{a3}+{b3}"
    cases["A3"] = [
        [label3 if tok in (a3, b3) else tok for tok in seq] for seq in sequences
    ]
    facts["A3"] = {
        "merged_codes": [a3, b3],
        "multiplicities": [multiplicity[a3], multiplicity[b3]],
    }

    digest = hashlib.sha256(
        "glossa-lab/spec090/g3/c1-relabeling-seed".encode("utf-8")
    ).digest()
    seed = int.from_bytes(digest[:8], "big")
    codes = sorted(multiplicity)
    shuffled = list(codes)
    random.Random(seed).shuffle(shuffled)
    mapping = dict(zip(codes, shuffled))
    cases["C1"] = [[mapping[tok] for tok in seq] for seq in sequences]
    facts["C1"] = {
        "seed_digest": digest.hex(),
        "seed": seed,
        "codes_permuted": len(codes),
        "bijection_sha256": hashlib.sha256(
            json.dumps(
                [[c, mapping[c]] for c in codes], ensure_ascii=False
            ).encode("utf-8")
        ).hexdigest(),
        "fixed_points": sum(1 for c in codes if mapping[c] == c),
    }
    return cases, facts


COMPONENTS = ("inventory_size", "M", "L", "X", "B")
COMPONENT_NAMES = {
    "inventory_size": "inventory size",
    "M": "M",
    "L": "L",
    "X": "X",
    "B": "B",
}


def differing_components(p, q) -> list[str]:
    return [COMPONENT_NAMES[c] for c in COMPONENTS if p[c] != q[c]]


def identities_hold(prof, object_count: int, token_total: int) -> list[str]:
    """Outcome section 2(c)'s identities; returns the failures."""
    fails = []
    if sum(prof["M"]) != token_total:
        fails.append("sum M != token total")
    if sum(c for _, c in prof["L"]) != object_count:
        fails.append("sum L counts != object count")
    if sum(length * c for length, c in prof["L"]) != token_total:
        fails.append("sum (length x count) over L != token total")
    sum_init = sum(t[0] for t in prof["X"])
    sum_fin = sum(t[1] for t in prof["X"])
    sum_med = sum(t[2] for t in prof["X"])
    if sum_init != object_count:
        fails.append("sum initial over X != object count")
    if sum_fin != object_count:
        fails.append("sum final over X != object count")
    len1 = dict(prof["L"]).get(1, 0)
    if sum_med != token_total - sum_init - sum_fin + len1:
        fails.append("sum medial over X != tokens - initial - final + len-1 count")
    if sum(prof["B"]) != token_total - object_count:
        fails.append("sum B != token total - object count")
    if not (len(prof["M"]) == len(prof["X"]) == prof["inventory_size"]):
        fails.append("|M| = |X| = inventory size fails")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    args = ap.parse_args()
    root = args.repo
    spec_records = (
        root
        / "specs/090-projected-constraints-generalization-study/records"
    )

    print("== Leg 1: input integrity ==")
    snap_sha = sha256_file(root / "glossa-corpus/indus/exports/indus_research.jsonl")
    flat_sha = sha256_file(root / "reports/mahadevan_corpus_flat.txt")
    note(snap_sha == FROZEN_SNAPSHOT_SHA256, "snapshot SHA-256", snap_sha)
    note(flat_sha == FROZEN_FLAT_SHA256, "M77 flat file SHA-256", flat_sha)

    print("== Extraction (freeze section 2) ==")
    sequences, census = extract_h1(
        root / "glossa-corpus/indus/exports/indus_research.jsonl"
    )
    token_total = sum(len(s) for s in sequences)
    print(f"  census: {census}")
    note(census["total_records"] == 15508, "snapshot record total", str(census["total_records"]))
    note(len(sequences) == FROZEN_RECORDS, "H1 record count", str(len(sequences)))
    note(token_total == FROZEN_TOKENS, "H1 token total", str(token_total))
    note(census["empty_lists"] == 0, "empty-list exclusions", str(census["empty_lists"]))
    note(census["nonstring_elements"] == 0, "non-string code elements", str(census["nonstring_elements"]))

    print("== Leg 2: independent recomputation ==")
    cases, facts = build_cases(sequences, profile_of(sequences)[1])
    note(
        facts["C1"]["seed_digest"] == FROZEN_SEED_DIGEST,
        "C1 seed digest (freeze section 8)",
        facts["C1"]["seed_digest"],
    )
    note(facts["C1"]["seed"] == FROZEN_SEED, "C1 seed value", str(facts["C1"]["seed"]))
    note(
        facts["C1"]["bijection_sha256"] == QUOTED_BIJECTION_SHA256,
        "C1 bijection SHA-256 vs outcome record",
        facts["C1"]["bijection_sha256"],
    )
    print(f"  C1 fixed points under the bijection: {facts['C1']['fixed_points']}")

    committed = {}
    for case, run_id in ADMIN_RUN_IDS.items():
        record = json.loads((spec_records / f"{run_id}.json").read_text())
        committed[case] = record
        note(
            record["run"]["run_id"] == run_id and record["result"]["case"] == case,
            f"{case} run record identity",
            run_id,
        )

    mine = {}
    for case in ("A0", "A1", "A2", "A3", "C1", "C2"):
        prof, _ = profile_of(cases[case])
        mine[case] = prof
        theirs = committed[case]["result"]["profile"]
        diffs = [c for c in COMPONENTS if prof[c] != theirs[c]]
        note(
            not diffs,
            f"{case} profile identical to run record",
            "differs in: " + ", ".join(diffs) if diffs else "all 5 components",
        )
        note(
            committed[case]["result"]["object_count"] == len(cases[case])
            and committed[case]["result"]["token_total"]
            == sum(len(s) for s in cases[case]),
            f"{case} object/token totals in record",
            f"{committed[case]['result']['object_count']}/"
            f"{committed[case]['result']['token_total']}",
        )
        # case facts fidelity (record vs independent construction)
        rfacts = committed[case]["result"]["case_facts"]
        if case == "A1":
            same = all(rfacts[k] == facts["A1"][k] for k in facts["A1"])
            note(same, "A1 case facts", json.dumps(facts["A1"]))
        if case == "A2":
            same = all(
                rfacts[k] == facts["A2"][k]
                for k in ("merged_codes", "multiplicities", "floor")
            )
            note(same, "A2 case facts", json.dumps(facts["A2"]))
        if case == "A3":
            same = all(rfacts[k] == facts["A3"][k] for k in facts["A3"])
            note(same, "A3 case facts", json.dumps(facts["A3"]))
        if case == "C1":
            same = (
                rfacts["seed"] == facts["C1"]["seed"]
                and rfacts["codes_permuted"] == facts["C1"]["codes_permuted"]
                and rfacts["bijection_sha256"] == facts["C1"]["bijection_sha256"]
            )
            note(same, "C1 case facts", f"seed/fingerprint agree")

    print("== Leg 3: bar application on the recomputed profiles ==")
    distinct_pairs = [("A0", "A1"), ("A0", "A2"), ("A0", "A3")]
    invariance_pairs = [("A0", "C1"), ("A0", "C2")]
    cond1 = True
    for a, b in distinct_pairs:
        d = differing_components(mine[a], mine[b])
        print(f"  ({a}, {b}) differing components: {d}")
        cond1 = cond1 and len(d) >= 1
    cond2 = True
    for a, b in invariance_pairs:
        same = mine[a] == mine[b]
        print(f"  ({a}, {b}) identical in every component: {same}")
        cond2 = cond2 and same
    totals = {
        (len(cases[c]), sum(len(s) for s in cases[c]))
        for c in ("A0", "A1", "A2", "A3", "C1", "C2")
    }
    cond3 = len(totals) == 1
    print(f"  distinct (objects, tokens) totals across cases: {totals}")
    note(cond1, "bar condition 1 (distinctness)")
    note(cond2, "bar condition 2 (invariance)")
    note(cond3, "bar condition 3 (no count separation)")
    print(f"  BAR VERDICT ON RECOMPUTED PROFILES: "
          f"{'SEPARATED' if (cond1 and cond2 and cond3) else 'NOT SEPARATED'}")

    print("== Leg 4: outcome-record fidelity ==")
    for case in ("A0", "A1", "A2", "A3", "C1", "C2"):
        ph = canonical_sha256(committed[case]["result"]["profile"])
        note(
            ph == QUOTED_PROFILE_SHA256[case],
            f"{case} profile SHA-256 (canonical, from run record)",
            ph,
        )
        rh = canonical_sha256(committed[case]["result"])
        note(
            rh == QUOTED_RESULT_SHA256[case],
            f"{case} result-block SHA-256 (canonical, from run record)",
            rh,
        )
    a0 = committed["A0"]["result"]["profile"]
    note(a0["M"][:12] == [1274, 680, 615, 342, 338, 317, 261, 255, 219, 209, 206, 192],
         "A0 M head (12 values, outcome section 3)", str(a0["M"][:12]))
    note(a0["M"].count(1) == 159, "A0 hapax count", str(a0["M"].count(1)))
    note(a0["L"] == [[1, 84], [2, 387], [3, 633], [4, 597], [5, 500], [6, 305],
                     [7, 205], [8, 109], [9, 37], [10, 27], [11, 17], [12, 1],
                     [13, 1], [14, 3]], "A0 L in full (outcome section 3)")
    note(len(a0["B"]) == 3188, "A0 distinct adjacent pairs", str(len(a0["B"])))
    a3 = committed["A3"]["result"]["profile"]
    note(len(a3["B"]) == 3071, "A3 distinct adjacent pairs", str(len(a3["B"])))
    note(max(committed["A3"]["result"]["profile"]["M"]) == 1954,
         "A3 merged-type multiplicity", str(max(a3["M"])))
    l_all_same = all(
        committed[c]["result"]["profile"]["L"] == a0["L"]
        for c in ("A1", "A2", "A3", "C1", "C2")
    )
    note(l_all_same, "L identical across all six run records")
    for case in ("A0", "A1", "A2", "A3", "C1", "C2"):
        r = committed[case]["result"]
        fails = identities_hold(r["profile"], r["object_count"], r["token_total"])
        note(not fails, f"{case} section-2(c) identities on committed profile",
             "; ".join(fails))

    print("== AUDIT-SUMMARY ==")
    if problems:
        print(f"DISCREPANCIES: {len(problems)}")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("ALL RECOMPUTATIONS AGREE; BAR RE-APPLIES AS SEPARATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
