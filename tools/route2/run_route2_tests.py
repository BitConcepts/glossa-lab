#!/usr/bin/env python3
"""Route 2 tooling tests — proves the read script and the census tool
offline, before any live session exists.

Run:  python3 run_route2_tests.py        (exit 0 = all pass)

Coverage:
  T1  read script, fixture mode: two REST pages -> artifacts; unwrap,
      paging, _id, extra-field preservation, companion `fields` union.
  T2  read script on a mis-shaped page 1: SHAPE-FAIL exit 2, no artifacts.
  T3  census tool on the 12-record handcrafted fixture vs hand-computed
      expectations (loader-mirror semantics: longest-per-(dockey,
      sideline), texts-then-S fallback, *NNN/0/empty filtering, skipped
      dockeys, dockeys with no kept sequence not counted).
  T4  census tool on the same fixture vs the real T1_1 constants FAILS
      (the tool can say no).
  T5  census tool on the read script's own fixture output (round trip).
  T6  terminal_frac / positional profiles on synthetic sequences with
      hand-computed values (Phase-43 part2 semantics).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import route2_verify_census as vc  # noqa: E402

FAILURES = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def run(args):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="route2-tests-"))

    print("T1 — read script, fixture mode")
    out1 = tmp / "out1"
    r = run([str(HERE / "route2_firestore_read.py"), "fixture",
             "--pages", str(HERE / "fixtures/rest_pages"), "--out", str(out1)])
    check("exit 0", r.returncode == 0, r.stderr.strip())
    comp = json.loads((out1 / "firestore_indusarrays_full.json").read_text())
    lines = (out1 / "firestore_indusarrays_full.jsonl").read_text().strip().splitlines()
    check("5 documents", len(comp["documents"]) == 5)
    check("5 jsonl lines", len(lines) == 5)
    check("fields union = 19", len(comp["fields"]) == 19, str(comp["fields"]))
    d1 = comp["documents"][0]
    check("dockey unwrapped to int", d1["dockey"] == 1001)
    check("texts unwrapped", d1["texts"] == ["342", "99"])
    check("_id from name", d1["_id"] == "doc001")
    check("extra field preserved (textnum)", d1.get("textnum") == 1)
    check("empty texts array unwraps to []", comp["documents"][2]["texts"] == [])
    check("extra field preserved (fs80)", comp["documents"][3].get("fs80") == "x")

    print("T2 — read script, mis-shaped page 1")
    out2 = tmp / "out2"
    r = run([str(HERE / "route2_firestore_read.py"), "fixture",
             "--pages", str(HERE / "fixtures/badpage"), "--out", str(out2)])
    check("exit 2", r.returncode == 2, f"rc={r.returncode}")
    check("SHAPE-FAIL reported", "SHAPE-FAIL" in r.stderr)
    check("no artifacts written", not (out2 / "firestore_indusarrays_full.jsonl").exists())

    print("T3 — census vs hand-computed fixture expectations")
    r = run([str(HERE / "route2_verify_census.py"),
             str(HERE / "fixtures/fixture_records.jsonl"),
             "--expect", str(HERE / "fixtures/fixture_expect.json")])
    check("exit 0 (all gates pass)", r.returncode == 0, r.stdout[-400:] + r.stderr)

    print("T4 — census vs the real T1_1 constants must FAIL on the fixture")
    r = run([str(HERE / "route2_verify_census.py"),
             str(HERE / "fixtures/fixture_records.jsonl")])
    check("exit 1", r.returncode == 1, f"rc={r.returncode}")

    print("T5 — round trip: census of the read script's fixture output")
    r = run([str(HERE / "route2_verify_census.py"),
             str(out1 / "firestore_indusarrays_full.jsonl"),
             "--expect", str(HERE / "fixtures/roundtrip_expect.json")])
    check("exit 0 (all gates pass)", r.returncode == 0, r.stdout[-400:] + r.stderr)

    print("T6 — terminal_frac / profiles, hand-computed")
    seqs = [[267, 500]] * 6 + [[267, 501]] * 4
    profiles = vc.positional_profiles(seqs)
    check("500 is TERMINAL_STRONG (t=1.0)",
          profiles.get(500, {}).get("role") == "TERMINAL_STRONG")
    check("501 (total 4) gets no profile", 501 not in profiles)
    check("267 is INITIAL_STRONG", profiles.get(267, {}).get("role") == "INITIAL_STRONG")
    check("terminal_frac(267) == 0.6", vc.terminal_frac(seqs, profiles, 267) == 0.6)
    m = vc.census(HERE / "fixtures/fixture_records.jsonl")
    check("fixture 99 profile MIXED (I1 M3 T2)",
          m["profiles"].get("99", {}).get("role") == "MIXED")
    check("fixture has no fish result (all totals < 10)", m["terminal_frac"] == {})

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
        return 1
    print("ALL ROUTE 2 TOOLING TESTS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
