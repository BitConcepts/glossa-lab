#!/usr/bin/env python3
"""Spec 098 test cases TC-098-01 and TC-098-02.

Run from the repository root:

    python3 -m pytest specs/098-identifiability-over-the-65/tests/ -q
    # or, stdlib only:
    python3 -m unittest discover -s specs/098-identifiability-over-the-65/tests -v

The tests exercise the frozen seal/split mechanism and the
frozen decision rules against a synthetic fixture corpus, via
the reference implementation in ../tools/seal_and_score.py.
They touch no real inscription and no held-out material.
"""

import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import seal_and_score as ss  # noqa: E402


def fixture_clusters(n=200):
    return [f"FIX-{i:04d}" for i in range(n)]


class TC098_01SealAndSplit(unittest.TestCase):
    """TC-098-01 — seal and split integrity (claims C098-1, C098-2)."""

    def test_split_is_deterministic_and_matches_frozen_rule(self):
        ids = fixture_clusters()
        dev1, held1 = ss.split_clusters(ids)
        dev2, held2 = ss.split_clusters(list(reversed(ids)))
        self.assertEqual(held1, held2)
        self.assertEqual(dev1, dev2)
        # Every assignment agrees with the rule as written in the freeze.
        for cid in ids:
            expect = (
                int(hashlib.sha256(("098-split-v1:" + cid).encode()).hexdigest(), 16)
                % 5
                == 0
            )
            self.assertEqual(cid in held1, expect, cid)
        self.assertFalse(set(dev1) & set(held1))
        self.assertEqual(len(dev1) + len(held1), len(ids))
        # A 20 percent rule over 200 fixture ids lands in a sane band.
        self.assertTrue(20 <= len(held1) <= 60, len(held1))

    def test_seal_recomputes_and_detects_tampering(self):
        _, held = ss.split_clusters(fixture_clusters())
        seal = ss.seal_hash(held)
        self.assertTrue(ss.verify_seal(held, seal))
        tampered = held[:-1] + ["FIX-9999"]
        self.assertFalse(ss.verify_seal(tampered, seal))
        self.assertFalse(ss.verify_seal(held + ["FIX-9998"], seal))

    def test_development_export_excludes_and_refuses_held_out(self):
        ids = fixture_clusters(50)
        dev, held = ss.split_clusters(ids)
        rows = [{"cluster_id": c} for c in dev]
        out = ss.development_export(rows, held)
        self.assertEqual(len(out), len(dev))
        self.assertFalse({r["cluster_id"] for r in out} & set(held))
        leaked = rows + [{"cluster_id": held[0]}]
        with self.assertRaises(ss.SealViolation):
            ss.development_export(leaked, held)


class TC098_02DecisionRules(unittest.TestCase):
    """TC-098-02 — decision-rule behaviour on planted cases
    (claims C098-4, C098-5, C098-6)."""

    def test_planted_discriminable_sign_passes_pseudo_arm(self):
        outcome = ss.decide(
            heldout_tokens=12,
            ll_candidate=-40.0,
            ll_best_rival=-58.0,
            null_p99=6.0,
        )
        self.assertEqual(outcome, ss.DISCRIMINATED_PSEUDO)

    def test_planted_discriminable_sign_passes_genuine_arm(self):
        outcome = ss.decide(
            heldout_tokens=12,
            ll_candidate=-40.0,
            ll_best_rival=-58.0,
            null_p99=6.0,
            genuine_holdout=True,
        )
        self.assertEqual(outcome, ss.IDENTIFIABLE)

    def test_planted_equivalent_sign_is_not_identifiable(self):
        outcome = ss.decide(
            heldout_tokens=12,
            ll_candidate=-50.0,
            ll_best_rival=-50.5,
            null_p99=6.0,
            genuine_holdout=True,
        )
        self.assertEqual(outcome, ss.NOT_IDENTIFIABLE)

    def test_margin_below_null_percentile_is_not_identifiable(self):
        outcome = ss.decide(
            heldout_tokens=30,
            ll_candidate=-40.0,
            ll_best_rival=-52.0,
            null_p99=14.0,
        )
        self.assertEqual(outcome, ss.NOT_IDENTIFIABLE)

    def test_low_count_is_undecidable_even_with_a_huge_margin(self):
        outcome = ss.decide(
            heldout_tokens=3,
            ll_candidate=-5.0,
            ll_best_rival=-90.0,
            null_p99=1.0,
            genuine_holdout=True,
        )
        self.assertEqual(outcome, ss.UNDECIDABLE)

    def test_no_accepted_sheet_is_not_identifiable_by_construction(self):
        outcome = ss.decide(
            heldout_tokens=20,
            ll_candidate=-10.0,
            ll_best_rival=-90.0,
            null_p99=1.0,
            prediction_sheet_accepted=False,
            genuine_holdout=True,
        )
        self.assertEqual(outcome, ss.NOT_IDENTIFIABLE)

    def test_flexibility_penalty_moves_a_variant_case_across_the_bar(self):
        # Raw margin 17 nats passes; six charged free choices
        # (variant alternations / homophony / gloss alternation)
        # cost 12 nats and the penalized margin of 5 fails.
        raw = ss.decide(
            heldout_tokens=15, ll_candidate=-30.0, ll_best_rival=-47.0, null_p99=4.0
        )
        penalized = ss.decide(
            heldout_tokens=15,
            ll_candidate=-30.0,
            ll_best_rival=-47.0,
            null_p99=4.0,
            candidate_free_choices=6,
        )
        self.assertEqual(raw, ss.DISCRIMINATED_PSEUDO)
        self.assertEqual(penalized, ss.NOT_IDENTIFIABLE)


if __name__ == "__main__":
    unittest.main()
