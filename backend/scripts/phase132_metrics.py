#!/usr/bin/env python3
"""Phase-132 (spec 023, FROZEN) — pilot metrics.

Implements the FROZEN definitions of spec 023 section 5.6
(freeze block, 2026-10-09) exactly:

- Comparison space: P space primary, M space secondary.
  A token's P value is the crosswalk-v1 primary counterpart
  of its matched M: the highest-confidence row for that M
  (confidence order high > medium > low > none), ties broken
  by lowest P number. All candidate rows and the conflict
  flag are carried per token. `UNK` compares as `UNK`.
- A token whose M has NO crosswalk row is
  crosswalk_unmapped. Its P-space comparison value is the
  placeholder "UNMAPPED:<M_ID>" — a distinct value per M, so
  two different unmapped signs never compare equal and an
  unmapped token never masquerades as a P sign or as UNK.
  (The freeze block defines the primary-counterpart rule and
  the unmapped category; this placeholder is the mechanical
  representation of "no counterpart" in a token sequence.)
- Exact-sequence agreement: per object 1 iff Pass A and
  Pass B sequences are identical, else 0; rate = mean over
  the scope. Stop-rule scope = all pilot objects; release
  gate (i) scope = the gold sample.
- Per-token agreement: minimum-edit alignment on token ID
  sequences (substitution preferred over insertion/deletion
  at equal cost); matches are aligned equal pairs; rate =
  sum(matches) / sum(max(lenA, lenB)) over the scope.
- Gold per-sign error estimator (three-way decomposition):
  per gold object align S2 (two-pass adjudicated) to S3
  (three-pass adjudicated) under the same alignment rule; a
  position differs if the aligned pair's IDs are unequal or
  the token exists on only one side; rate = sum(differing) /
  sum(max(lenS2, lenS3)) over the gold sample. This is the
  stop-rule's post-adjudication per-sign error rate and
  release gate (iii). Errors identical across all three
  passes are invisible to it (frozen stated limitation).

Also measured: UNK shares per pass / adjudicated S2 / gold,
crosswalk-unmapped share on adjudicated tokens, attestation
presence + token counts of P076 / P125 / P000 in adjudicated
P sequences (spec section 7 checks), and effort from the
store's effort_log.csv (per-role per-object seconds
distributions, tokens-per-object distribution for
adjudicated records, effort per token).

Verdicts computed and plainly labelled:
  stop_rule_fired = (estimator P > 0.05) OR
                    (exact-sequence agreement, all-50, P < 0.80)
  release gates on the gold scope: (i) exact-sequence >= 0.90,
  (ii) per-token >= 0.95, (iii) estimator <= 0.02.

Inputs live in the local store (never committed):
  corpora/downloads/cisi_image_layer/phase132_pilot/
Outputs: reports/phase132_pilot_metrics.json (repo root,
the Phase-130/131 results convention) + a printed summary.

Deterministic: no randomness, no wall-clock in the output,
stable ordering everywhere.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE = (Path.home() / "workspace" / "glossa-lab" / "corpora"
                 / "downloads" / "cisi_image_layer" / "phase132_pilot")
CROSSWALK_PATH = REPO_ROOT / "data" / "crosswalks" / \
    "parpola_mahadevan_crosswalk_v1.json"
DEFAULT_OUT = REPO_ROOT / "reports" / "phase132_pilot_metrics.json"

CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1, "none": 0}
UNK = "UNK"
UNMAPPED_PREFIX = "UNMAPPED:"
ATTESTATION_SIGNS = ("P076", "P125", "P000")

# Frozen gate thresholds (spec 023 sections 3.1 / 5.6).
STOP_ERROR_MAX = 0.05
STOP_EXACT_MIN = 0.80
GATE_EXACT_MIN = 0.90
GATE_PER_TOKEN_MIN = 0.95
GATE_ERROR_MAX = 0.02


def _round(x):
    return round(x, 6) if x is not None else None


def p_number(p_id: str) -> int:
    return int(p_id[1:])


# ── Crosswalk primary derivation (freeze block section 5.6) ──

def candidate_sort_key(row):
    return (-CONFIDENCE_RANK[row["confidence"]],
            p_number(row["parpola_id"]), row["parpola_id"])


def build_m_to_p(rows) -> dict:
    """M -> {primary, candidates, conflict, any_conflict}.

    Rows with an empty mahadevan_id are the crosswalk's
    P-side unmapped markers (P000/P225/P261/P358), not M rows;
    they play no part in the M -> P derivation."""
    by_m: dict[str, list] = {}
    for row in rows:
        m = row.get("mahadevan_id")
        if not m:
            continue
        by_m.setdefault(m, []).append(row)
    out = {}
    for m, mrows in by_m.items():
        cands = sorted(mrows, key=candidate_sort_key)
        primary = cands[0]
        out[m] = {
            "primary": primary["parpola_id"],
            "candidates": [
                {"parpola_id": r["parpola_id"],
                 "confidence": r["confidence"],
                 "conflict": bool(r["conflict"])}
                for r in cands],
            "conflict": bool(primary["conflict"]),
            "any_conflict": any(bool(r["conflict"]) for r in cands),
        }
    return out


def derive_token(m_id: str, m_to_p: dict) -> dict:
    """One token's derived values. Input is the transcriber's
    matched M ID (or the UNK sentinel)."""
    if m_id == UNK:
        return {"m_id": UNK, "p_id": None, "p_value": UNK,
                "is_unk": True, "crosswalk_unmapped": False,
                "crosswalk_conflict": False, "candidates": []}
    entry = m_to_p.get(m_id)
    if entry is None:
        return {"m_id": m_id, "p_id": None,
                "p_value": f"{UNMAPPED_PREFIX}{m_id}",
                "is_unk": False, "crosswalk_unmapped": True,
                "crosswalk_conflict": False, "candidates": []}
    return {"m_id": m_id, "p_id": entry["primary"],
            "p_value": entry["primary"],
            "is_unk": False, "crosswalk_unmapped": False,
            "crosswalk_conflict": entry["conflict"],
            "candidates": entry["candidates"]}


def derive_sequence(m_ids, m_to_p) -> list[dict]:
    return [derive_token(m, m_to_p) for m in m_ids]


def p_values(derived) -> list[str]:
    return [t["p_value"] for t in derived]


def m_values(derived) -> list[str]:
    return [t["m_id"] for t in derived]


# ── Minimum-edit alignment (substitution preferred) ─────────

def align(a, b) -> list[tuple]:
    """Optimal unit-cost alignment of token ID sequences as a
    list of (a_token_or_None, b_token_or_None) columns.
    Backtracking prefers the diagonal (match / substitution)
    over deletion over insertion at equal cost, so the result
    is deterministic and substitution is preferred over an
    insertion+deletion pair at equal cost (freeze block)."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = dp[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
            dp[i][j] = min(sub, dp[i - 1][j] + 1, dp[i][j - 1] + 1)
    cols = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            cost = 0 if a[i - 1] == b[j - 1] else 1
            if dp[i][j] == dp[i - 1][j - 1] + cost:
                cols.append((a[i - 1], b[j - 1]))
                i -= 1
                j -= 1
                continue
        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            cols.append((a[i - 1], None))
            i -= 1
            continue
        cols.append((None, b[j - 1]))
        j -= 1
    cols.reverse()
    return cols


def alignment_matches(a, b) -> int:
    return sum(1 for x, y in align(a, b)
               if x is not None and x == y)


def alignment_differing(a, b) -> int:
    """Positions that differ under the alignment: unequal
    aligned pairs plus tokens present on only one side."""
    return sum(1 for x, y in align(a, b) if x != y)


# ── Agreement / estimator aggregates ────────────────────────

def exact_sequence_agreement(pairs) -> dict:
    """pairs: list of (seqA, seqB). Rate = mean of identity."""
    n = len(pairs)
    agree = sum(1 for a, b in pairs if list(a) == list(b))
    return {"n_objects": n, "n_exact": agree,
            "rate": _round(agree / n) if n else None}


def per_token_agreement(pairs) -> dict:
    """Rate = sum(matches) / sum(max(lenA, lenB))."""
    matches = denom = 0
    for a, b in pairs:
        matches += alignment_matches(a, b)
        denom += max(len(a), len(b))
    return {"n_objects": len(pairs), "matches": matches,
            "denominator": denom,
            "rate": _round(matches / denom) if denom else None}


def error_estimator(pairs) -> dict:
    """Rate = sum(differing positions) / sum(max(lenS2, lenS3))."""
    differing = denom = 0
    for s2, s3 in pairs:
        differing += alignment_differing(s2, s3)
        denom += max(len(s2), len(s3))
    return {"n_objects": len(pairs), "differing_positions": differing,
            "denominator": denom,
            "rate": _round(differing / denom) if denom else None}


def distribution(values) -> dict:
    vals = list(values)
    if not vals:
        return {"n": 0, "mean": None, "median": None, "min": None,
                "max": None, "total": 0}
    return {"n": len(vals), "mean": _round(statistics.fmean(vals)),
            "median": _round(statistics.median(vals)),
            "min": min(vals), "max": max(vals),
            "total": _round(sum(vals))}


# ── Local-store loading ─────────────────────────────────────

def _read_json(path: Path):
    return json.loads(path.read_text("utf-8"))


def load_store(store: Path) -> dict:
    frame_doc = _read_json(store / "frame.json")
    frame = frame_doc["frame"]
    keys = [e["canonical_key"] for e in frame]
    gold_keys = [e["canonical_key"] for e in frame if e.get("gold")]

    def load_pass(sub, field="tokens"):
        out = {}
        for key in keys:
            path = store / sub / f"{key}.json"
            if not path.exists():
                continue
            rec = _read_json(path)
            toks = sorted(rec[field], key=lambda t: t["position"])
            out[key] = toks
        return out

    passes = {"pass_a": load_pass("pass_a"),
              "pass_b": load_pass("pass_b"),
              "pass_gold": load_pass("pass_gold")}
    adjudication = {}
    for key in keys:
        rec = _read_json(store / "adjudication" / f"{key}.json")
        adjudication[key] = rec
    s2 = {k: sorted(r["s2_tokens"], key=lambda t: t["position"])
          for k, r in adjudication.items()}
    s3 = {k: sorted(r["s3_tokens"], key=lambda t: t["position"])
          for k, r in adjudication.items() if "s3_tokens" in r}
    final = {k: (s3[k] if k in s3 else s2[k]) for k in keys}
    return {"frame": frame, "keys": keys, "gold_keys": gold_keys,
            "passes": passes, "adjudication": adjudication,
            "s2": s2, "s3": s3, "final": final}


def token_share(derived_seqs) -> dict:
    """UNK / crosswalk-unmapped shares over a set of derived
    token sequences (iterable of derived-token lists)."""
    total = unk = unmapped = conflict = 0
    unmapped_ids: Counter = Counter()
    for seq in derived_seqs:
        for t in seq:
            total += 1
            if t["is_unk"]:
                unk += 1
            if t["crosswalk_unmapped"]:
                unmapped += 1
                unmapped_ids[t["m_id"]] += 1
            if t["crosswalk_conflict"]:
                conflict += 1
    return {"tokens": total, "unk": unk,
            "unk_share": _round(unk / total) if total else None,
            "crosswalk_unmapped": unmapped,
            "crosswalk_unmapped_share":
                _round(unmapped / total) if total else None,
            "unk_plus_unmapped": unk + unmapped,
            "unk_plus_unmapped_share":
                _round((unk + unmapped) / total) if total else None,
            "crosswalk_conflict_tokens": conflict,
            "unmapped_m_ids": dict(sorted(unmapped_ids.items()))}


def load_effort(store: Path) -> dict:
    """Per (role, key) seconds from effort_log.csv start/stop
    pairs. Asserts the log is well-formed (exactly one start
    and one stop per role+key, stop after start)."""
    events: dict[tuple, dict] = {}
    with open(store / "effort_log.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            slot = events.setdefault((row["role"], row["key"]), {})
            assert row["event"] not in slot, \
                f"duplicate {row['event']} for {row['role']} {row['key']}"
            slot[row["event"]] = int(row["epoch_seconds"])
    durations: dict[str, dict[str, float]] = {}
    for (role, key), slot in sorted(events.items()):
        assert set(slot) == {"start", "stop"}, \
            f"unpaired effort events for {role} {key}: {sorted(slot)}"
        dur = slot["stop"] - slot["start"]
        assert dur >= 0, f"negative duration for {role} {key}"
        durations.setdefault(role, {})[key] = dur
    return durations


# ── Main computation ────────────────────────────────────────

def compute_metrics(store: Path) -> dict:
    crosswalk_bytes = CROSSWALK_PATH.read_bytes()
    crosswalk = json.loads(crosswalk_bytes)
    m_to_p = build_m_to_p(crosswalk["rows"])
    data = load_store(store)
    keys, gold_keys = data["keys"], data["gold_keys"]
    assert len(keys) == 50, f"expected 50 frame objects, got {len(keys)}"
    assert len(gold_keys) == 10, \
        f"expected 10 gold objects, got {len(gold_keys)}"
    for sub in ("pass_a", "pass_b"):
        assert set(data["passes"][sub]) == set(keys), sub
    assert set(data["passes"]["pass_gold"]) == set(gold_keys)
    assert set(data["s3"]) == set(gold_keys)

    def derived(token_records):
        return derive_sequence([t["m_id"] for t in token_records],
                               m_to_p)

    seq = {  # key -> derived tokens, per sequence set
        "pass_a": {k: derived(data["passes"]["pass_a"][k]) for k in keys},
        "pass_b": {k: derived(data["passes"]["pass_b"][k]) for k in keys},
        "pass_gold": {k: derived(data["passes"]["pass_gold"][k])
                      for k in gold_keys},
        "s2": {k: derived(data["s2"][k]) for k in keys},
        "s3": {k: derived(data["s3"][k]) for k in gold_keys},
        "final": {k: derived(data["final"][k]) for k in keys},
    }

    def pairs(scope_keys, space):
        val = p_values if space == "p" else m_values
        return [(val(seq["pass_a"][k]), val(seq["pass_b"][k]))
                for k in scope_keys]

    scopes = {"all_50": keys, "gold_sample": gold_keys}
    exact = {sname: {space: exact_sequence_agreement(pairs(ks, space))
                     for space in ("p", "m")}
             for sname, ks in scopes.items()}
    per_token = {sname: {space: per_token_agreement(pairs(ks, space))
                         for space in ("p", "m")}
                 for sname, ks in scopes.items()}

    est_pairs = {space: [(val(seq["s2"][k]), val(seq["s3"][k]))
                         for k in gold_keys]
                 for space, val in (("p", p_values), ("m", m_values))}
    estimator = {space: error_estimator(prs)
                 for space, prs in est_pairs.items()}

    shares = {
        "pass_a": token_share(seq["pass_a"].values()),
        "pass_b": token_share(seq["pass_b"].values()),
        "pass_gold": token_share(seq["pass_gold"].values()),
        "adjudicated_s2": token_share(seq["s2"].values()),
        "adjudicated_s3_gold": token_share(seq["s3"].values()),
        "adjudicated_final": token_share(seq["final"].values()),
    }

    def attestation(which):
        counts = Counter(t["p_value"] for s in seq[which].values()
                         for t in s)
        return {sign: {"attested": counts.get(sign, 0) > 0,
                       "token_count": counts.get(sign, 0)}
                for sign in ATTESTATION_SIGNS}

    # ── Effort ──
    durations = load_effort(store)
    role_tokens = {
        "pass_a": sum(len(seq["pass_a"][k]) for k in keys),
        "pass_b": sum(len(seq["pass_b"][k]) for k in keys),
        "pass_gold": sum(len(seq["pass_gold"][k]) for k in gold_keys),
        # The adjudicator's direct product is the two-pass
        # adjudicated (S2) sequence set.
        "adjudicator": sum(len(seq["s2"][k]) for k in keys),
    }
    effort_roles = {}
    for role in ("pass_a", "pass_b", "pass_gold", "adjudicator"):
        durs = durations.get(role, {})
        dist = distribution(durs.values())
        effort_roles[role] = {
            "per_object_seconds": dist,
            "tokens_produced": role_tokens[role],
            "seconds_per_token":
                _round(dist["total"] / role_tokens[role])
                if role_tokens[role] else None,
        }
    tokens_per_object = distribution(len(seq["final"][k]) for k in keys)
    total_seconds = sum(d["total"] for d in
                        (effort_roles[r]["per_object_seconds"]
                         for r in effort_roles))
    final_tokens = sum(len(seq["final"][k]) for k in keys)

    # ── Verdicts (computed, plainly labelled) ──
    est_p = estimator["p"]["rate"]
    exact_all_p = exact["all_50"]["p"]["rate"]
    exact_gold_p = exact["gold_sample"]["p"]["rate"]
    tok_gold_p = per_token["gold_sample"]["p"]["rate"]
    stop_rule = {
        "definition": "stop if gold error estimator (P) > 0.05 OR "
                      "exact-sequence agreement all-50 (P) < 0.80 "
                      "(spec 023 sections 3.1 / 5.6 freeze block)",
        "gold_error_estimator_p": est_p,
        "error_threshold": STOP_ERROR_MAX,
        "error_condition_fires": est_p > STOP_ERROR_MAX,
        "exact_sequence_agreement_all_50_p": exact_all_p,
        "exact_threshold": STOP_EXACT_MIN,
        "exact_condition_fires": exact_all_p < STOP_EXACT_MIN,
        "stop_rule_fired": (est_p > STOP_ERROR_MAX
                            or exact_all_p < STOP_EXACT_MIN),
    }
    gates = {
        "scope": "gold sample (10 objects), P space",
        "gate_i_exact_sequence": {
            "value": exact_gold_p, "threshold": GATE_EXACT_MIN,
            "pass": exact_gold_p >= GATE_EXACT_MIN},
        "gate_ii_per_token": {
            "value": tok_gold_p, "threshold": GATE_PER_TOKEN_MIN,
            "pass": tok_gold_p >= GATE_PER_TOKEN_MIN},
        "gate_iii_gold_error_estimator": {
            "value": est_p, "threshold": GATE_ERROR_MAX,
            "pass": est_p <= GATE_ERROR_MAX},
    }
    gates["all_pass"] = all(gates[g]["pass"] for g in
                            ("gate_i_exact_sequence", "gate_ii_per_token",
                             "gate_iii_gold_error_estimator"))

    per_object = []
    for k in keys:
        row = {"key": k, "gold": k in gold_keys,
               "len_pass_a": len(seq["pass_a"][k]),
               "len_pass_b": len(seq["pass_b"][k]),
               "len_adjudicated_final": len(seq["final"][k])}
        for space, val in (("p", p_values), ("m", m_values)):
            a, b = val(seq["pass_a"][k]), val(seq["pass_b"][k])
            row[f"exact_{space}"] = a == b
            row[f"matches_{space}"] = alignment_matches(a, b)
        if k in gold_keys:
            for space, val in (("p", p_values), ("m", m_values)):
                row[f"estimator_differing_{space}"] = \
                    alignment_differing(val(seq["s2"][k]),
                                        val(seq["s3"][k]))
        per_object.append(row)

    return {
        "phase": "132",
        "spec": "023 (FROZEN 2026-10-09), section 5.6 freeze block",
        "dataset_scope": "Stage P pilot: 50 frame objects, "
                           "10-object gold sample (seed 20261009)",
        "conventions": {
            "p_derivation": "crosswalk-v1 primary counterpart of the "
                            "matched M: highest-confidence row "
                            "(high > medium > low > none), tie -> "
                            "lowest P number; all candidate rows and "
                            "the primary row's conflict flag carried "
                            "per token",
            "unmapped_p_value": "UNMAPPED:<M_ID> (distinct per M; "
                                "never a P ID, never UNK)",
            "alignment": "minimum-edit alignment on token ID "
                         "sequences; substitution preferred over "
                         "insertion/deletion at equal cost "
                         "(diagonal > deletion > insertion backtrack)",
            "estimator_limitation": "errors identical across all "
                                    "three passes are invisible to "
                                    "the gold estimator (frozen "
                                    "stated limitation)",
        },
        "crosswalk": {
            "path": "data/crosswalks/parpola_mahadevan_crosswalk_v1.json",
            "sha256": hashlib.sha256(crosswalk_bytes).hexdigest(),
            "rows": len(crosswalk["rows"]),
            "m_ids_with_rows": len(m_to_p),
        },
        "counts": {
            "n_objects": len(keys),
            "n_gold_objects": len(gold_keys),
            "gold_keys": gold_keys,
            "total_tokens_pass_a": shares["pass_a"]["tokens"],
            "total_tokens_pass_b": shares["pass_b"]["tokens"],
            "total_tokens_pass_gold": shares["pass_gold"]["tokens"],
            "total_tokens_adjudicated_s2": shares["adjudicated_s2"]["tokens"],
            "total_tokens_adjudicated_final":
                shares["adjudicated_final"]["tokens"],
        },
        "exact_sequence_agreement": exact,
        "per_token_agreement": per_token,
        "gold_error_estimator": estimator,
        "unk_and_unmapped_shares": shares,
        "attestation": {
            "adjudicated_final_p_sequences": attestation("final"),
            "adjudicated_s2_p_sequences": attestation("s2"),
        },
        "effort": {
            "roles": effort_roles,
            "tokens_per_object_adjudicated_final": tokens_per_object,
            "all_roles_total_seconds": total_seconds,
            "all_roles_seconds_per_final_token":
                _round(total_seconds / final_tokens) if final_tokens
                else None,
        },
        "verdicts": {"stop_rule": stop_rule, "release_gates": gates},
        "per_object": per_object,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--store", type=Path, default=DEFAULT_STORE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    metrics = compute_metrics(args.store)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(metrics, indent=2,
                                   ensure_ascii=False) + "\n", "utf-8")
    v = metrics["verdicts"]
    print(f"Phase-132 pilot metrics -> {args.out}")
    print(f"  exact-seq agreement  all-50  P={metrics['exact_sequence_agreement']['all_50']['p']['rate']}  M={metrics['exact_sequence_agreement']['all_50']['m']['rate']}")
    print(f"  exact-seq agreement  gold    P={metrics['exact_sequence_agreement']['gold_sample']['p']['rate']}  M={metrics['exact_sequence_agreement']['gold_sample']['m']['rate']}")
    print(f"  per-token agreement  all-50  P={metrics['per_token_agreement']['all_50']['p']['rate']}  M={metrics['per_token_agreement']['all_50']['m']['rate']}")
    print(f"  per-token agreement  gold    P={metrics['per_token_agreement']['gold_sample']['p']['rate']}  M={metrics['per_token_agreement']['gold_sample']['m']['rate']}")
    print(f"  gold error estimator         P={metrics['gold_error_estimator']['p']['rate']}  M={metrics['gold_error_estimator']['m']['rate']}")
    print(f"  stop_rule_fired: {v['stop_rule']['stop_rule_fired']}")
    print(f"  release gates all_pass: {v['release_gates']['all_pass']} "
          f"(i={v['release_gates']['gate_i_exact_sequence']['pass']}, "
          f"ii={v['release_gates']['gate_ii_per_token']['pass']}, "
          f"iii={v['release_gates']['gate_iii_gold_error_estimator']['pass']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
