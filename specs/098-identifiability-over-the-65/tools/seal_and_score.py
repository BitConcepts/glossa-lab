#!/usr/bin/env python3
"""Spec 098 — reference implementation of the frozen seal and
decision rules (freeze v1, 2026-11-21).

Implements, at fixture scale, exactly the mechanisms the freeze
fixes for the study:

- the split rule: a cluster is held out iff
  int(SHA-256("098-split-v1:" + cluster_id)) mod 5 == 0;
- the seal: SHA-256 over the sorted held-out cluster ids, one
  per line; verification recomputes it and refuses a tampered
  list;
- the development-export guard: the scoring path refuses any
  development input containing a held-out cluster id;
- the decision rules of spec section 4, in their frozen
  precedence: UNDECIDABLE AT THIS POWER (held-out tokens < 5),
  then the pass outcomes (penalized margin >= 10 nats and above
  the permutation null's 99th percentile, on an accepted
  value-relevant prediction sheet), else NOT IDENTIFIABLE.
  The pass outcome's name depends on the arm: IDENTIFIABLE ON
  HELD-OUT for the genuine-holdout subset, DISCRIMINATED ON
  PSEUDO-HELD-OUT for the in-corpus arm (claim C098-6).

Standard library only. This module is the executable form of
the freeze for test cases TC-098-01 and TC-098-02; the study's
Stage 3 scoring path must implement the same rules, and any
divergence between this module and a Stage 3 implementation
is a defect against claim C098-5.
"""

from __future__ import annotations

import hashlib

SPLIT_DOMAIN = "098-split-v1:"
SPLIT_MODULUS = 5
MIN_HELDOUT_TOKENS = 5
MARGIN_BAR_NATS = 10.0
FLEX_PENALTY_NATS = 2.0

UNDECIDABLE = "UNDECIDABLE AT THIS POWER"
NOT_IDENTIFIABLE = "NOT IDENTIFIABLE"
IDENTIFIABLE = "IDENTIFIABLE ON HELD-OUT"
DISCRIMINATED_PSEUDO = "DISCRIMINATED ON PSEUDO-HELD-OUT"


def is_held_out(cluster_id: str) -> bool:
    digest = hashlib.sha256((SPLIT_DOMAIN + cluster_id).encode()).hexdigest()
    return int(digest, 16) % SPLIT_MODULUS == 0


def split_clusters(cluster_ids):
    """Deterministic split under the frozen rule."""
    held = sorted(c for c in cluster_ids if is_held_out(c))
    dev = sorted(c for c in cluster_ids if not is_held_out(c))
    return dev, held


def seal_hash(held_out_ids) -> str:
    payload = "".join(c + "\n" for c in sorted(held_out_ids))
    return hashlib.sha256(payload.encode()).hexdigest()


def verify_seal(held_out_ids, expected_hash: str) -> bool:
    return seal_hash(held_out_ids) == expected_hash


class SealViolation(Exception):
    """A development input contained a held-out cluster id."""


def development_export(rows, held_out_ids):
    """Return the development rows, refusing any held-out leak.

    `rows` is an iterable of dicts carrying a `cluster_id` key.
    The scoring path may only ever see the returned rows before
    the single recorded release of the held-out list.
    """
    held = set(held_out_ids)
    out = []
    for row in rows:
        if row["cluster_id"] in held:
            raise SealViolation(
                f"held-out cluster {row['cluster_id']} in development input"
            )
        out.append(row)
    return out


def decide(
    *,
    heldout_tokens: int,
    ll_candidate: float,
    ll_best_rival: float,
    null_p99: float,
    candidate_free_choices: int = 0,
    rival_free_choices: int = 0,
    prediction_sheet_accepted: bool = True,
    genuine_holdout: bool = False,
) -> str:
    """The frozen decision rules of spec section 4, in precedence
    order. Margins are candidate minus best rival, in nats, after
    the frozen flexibility penalty charged to each side."""
    if heldout_tokens < MIN_HELDOUT_TOKENS:
        return UNDECIDABLE
    if not prediction_sheet_accepted:
        return NOT_IDENTIFIABLE
    margin = (ll_candidate - FLEX_PENALTY_NATS * candidate_free_choices) - (
        ll_best_rival - FLEX_PENALTY_NATS * rival_free_choices
    )
    if margin >= MARGIN_BAR_NATS and margin > null_p99:
        return IDENTIFIABLE if genuine_holdout else DISCRIMINATED_PSEUDO
    return NOT_IDENTIFIABLE
