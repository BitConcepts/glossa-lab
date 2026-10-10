"""M77 calibration scoring machinery for the human-expert route.

This module grades a human coder's Mahadevan (M77) transcription of
the calibration set against the set's Parpola (P) reference sequences.
It implements the coder package's mapping discipline mechanically:

* only the crosswalk's high-confidence reliable core maps directly;
* an M sign whose core mapping has several P candidates is AMBIGUOUS
  -- the program never picks one silently;
* an M sign with no reliable-core mapping (conflict-register-only or
  unattested) is AMBIGUOUS, never guessed;
* segmentation differences are mapping-layer operations: two coder
  tokens that both map uniquely to one reference sign may merge onto
  it, and one coder token whose core candidates cover two adjacent
  reference signs is reported as an ambiguous split segment rather
  than resolved by fiat.

Ambiguous reference tokens are counted and reported separately. They
are neither agreements nor errors, and the per-token agreement rate's
denominator is agreements + errors only.

No coder data is bundled with this module. It scores records supplied
by the caller; the accompanying tests exercise it exclusively on
synthetic fixtures.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Sequence

M_TOKEN = re.compile(r"^M\d{3,4}$")
P_TOKEN = re.compile(r"^P\d{3}$")
NOMAP = "NOMAP"

DEFAULT_CROSSWALK = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "crosswalks"
    / "parpola_mahadevan_crosswalk_v1.csv"
)


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


@dataclass(frozen=True)
class Crosswalk:
    """M77 -> P candidate maps derived from the crosswalk pair table."""

    core_candidates: Mapping[str, tuple[str, ...]]
    all_candidates: Mapping[str, tuple[str, ...]]
    conflict_signs: frozenset[str]
    stats: Mapping[str, int]

    @classmethod
    def from_rows(cls, rows: Iterable[Mapping[str, object]]) -> "Crosswalk":
        core: dict[str, set[str]] = {}
        all_pairs: dict[str, set[str]] = {}
        conflict_signs: set[str] = set()
        asserted_pairs = 0
        core_pairs = 0
        row_count = 0
        for row in rows:
            row_count += 1
            m_sign = str(row.get("mahadevan_id", "")).strip()
            p_sign = str(row.get("parpola_id", "")).strip()
            if not m_sign or not p_sign:
                continue
            asserted_pairs += 1
            all_pairs.setdefault(m_sign, set()).add(p_sign)
            if _as_bool(row.get("conflict", False)):
                conflict_signs.add(m_sign)
            if (
                str(row.get("confidence", "")).strip().lower() == "high"
                and not _as_bool(row.get("candidate_only", False))
            ):
                core_pairs += 1
                core.setdefault(m_sign, set()).add(p_sign)
        core_candidates = {
            sign: tuple(sorted(candidates))
            for sign, candidates in sorted(core.items())
        }
        all_candidates = {
            sign: tuple(sorted(candidates))
            for sign, candidates in sorted(all_pairs.items())
        }
        stats = {
            "rows": row_count,
            "asserted_pairs": asserted_pairs,
            "core_pairs": core_pairs,
            "core_m_signs": len(core_candidates),
            "core_p_signs": len(
                {p for candidates in core_candidates.values() for p in candidates}
            ),
        }
        return cls(
            core_candidates=core_candidates,
            all_candidates=all_candidates,
            conflict_signs=frozenset(conflict_signs),
            stats=stats,
        )

    @classmethod
    def load_csv(cls, path: Path | str) -> "Crosswalk":
        with Path(path).open(newline="", encoding="utf-8") as handle:
            return cls.from_rows(csv.DictReader(handle))

    def mapping_for(self, m_sign: str) -> dict:
        """Classify one coder token without ever choosing among rivals."""
        if m_sign == NOMAP:
            return {
                "status": "ambiguous",
                "reason": "nomap_marker",
                "candidates": (),
            }
        candidates = self.core_candidates.get(m_sign, ())
        if len(candidates) == 1:
            return {
                "status": "mapped",
                "reason": "core_unique",
                "candidates": candidates,
            }
        if len(candidates) > 1:
            return {
                "status": "ambiguous",
                "reason": "core_one_to_many",
                "candidates": candidates,
            }
        if m_sign in self.all_candidates:
            return {
                "status": "ambiguous",
                "reason": "conflict_register_only",
                "candidates": (),
            }
        return {
            "status": "ambiguous",
            "reason": "unmapped_sign",
            "candidates": (),
        }


def _segment(
    *,
    operation: str,
    status: str,
    reason: str,
    coder_tokens: Sequence[str],
    reference_tokens: Sequence[str],
    candidates: Sequence[Sequence[str]],
    agreements: int = 0,
    errors: int = 0,
    ambiguous_tokens: int = 0,
) -> dict:
    return {
        "operation": operation,
        "status": status,
        "reason": reason,
        "coder_tokens": list(coder_tokens),
        "reference_tokens": list(reference_tokens),
        "mapped_candidates": [list(item) for item in candidates],
        "agreements": agreements,
        "errors": errors,
        "ambiguous_tokens": ambiguous_tokens,
    }


def _pair_segment(
    crosswalk: Crosswalk, coder_token: str, reference_token: str
) -> dict:
    mapping = crosswalk.mapping_for(coder_token)
    candidates = mapping["candidates"]
    if mapping["status"] == "mapped":
        mapped = candidates[0]
        if mapped == reference_token:
            return _segment(
                operation="pair",
                status="agreement",
                reason="core_unique_match",
                coder_tokens=[coder_token],
                reference_tokens=[reference_token],
                candidates=[candidates],
                agreements=1,
            )
        return _segment(
            operation="pair",
            status="error",
            reason="core_unique_mismatch",
            coder_tokens=[coder_token],
            reference_tokens=[reference_token],
            candidates=[candidates],
            errors=1,
        )
    return _segment(
        operation="pair",
        status="ambiguous",
        reason=str(mapping["reason"]),
        coder_tokens=[coder_token],
        reference_tokens=[reference_token],
        candidates=[candidates],
        ambiguous_tokens=1,
    )


def align_object(
    crosswalk: Crosswalk,
    coder_sequence: Sequence[str],
    reference_sequence: Sequence[str],
) -> list[dict]:
    """Deterministically align coder M77 tokens to reference P tokens.

    The search prefers, in order: more agreements, fewer errors, fewer
    ambiguous reference tokens, and more aligned reference tokens. It
    never uses the reference to choose among a coder token's rival core
    candidates: a one-to-many token paired with one reference token is
    ambiguous even when the reference is among the candidates.
    """
    coder = tuple(coder_sequence)
    reference = tuple(reference_sequence)
    for token in coder:
        if token != NOMAP and not M_TOKEN.match(token):
            raise ValueError(f"invalid M77 token in coder record: {token!r}")
    for token in reference:
        if not P_TOKEN.match(token):
            raise ValueError(f"invalid P token in reference: {token!r}")

    @lru_cache(maxsize=None)
    def best(i: int, j: int) -> tuple[tuple[int, int, int, int], tuple[dict, ...]]:
        if i == len(coder) and j == len(reference):
            return (0, 0, 0, 0), ()
        options: list[tuple[tuple[int, int, int, int], tuple[dict, ...]]] = []

        def consider(segment: dict, next_i: int, next_j: int) -> None:
            tail_key, tail = best(next_i, next_j)
            # tail_key stores errors and ambiguous counts as negatives.
            key = (
                segment["agreements"] + tail_key[0],
                -(segment["errors"] - tail_key[1]),
                -(segment["ambiguous_tokens"] - tail_key[2]),
                len(segment["reference_tokens"]) + tail_key[3],
            )
            options.append((key, (segment, *tail)))

        if i < len(coder) and j < len(reference):
            consider(_pair_segment(crosswalk, coder[i], reference[j]), i + 1, j + 1)

        # Split segment: one coder token, two adjacent reference signs,
        # both inside the token's rival core candidate set. Reported
        # ambiguous; the mapping layer does not resolve it here.
        if i < len(coder) and j + 1 < len(reference):
            candidates = crosswalk.core_candidates.get(coder[i], ())
            if len(candidates) > 1 and set(reference[j : j + 2]).issubset(
                set(candidates)
            ):
                consider(
                    _segment(
                        operation="split",
                        status="ambiguous",
                        reason="core_one_to_many_split_segment",
                        coder_tokens=[coder[i]],
                        reference_tokens=reference[j : j + 2],
                        candidates=[candidates],
                        ambiguous_tokens=2,
                    ),
                    i + 1,
                    j + 2,
                )

        # Merge segment: two coder tokens, both uniquely mapping to
        # the same single reference sign, contract onto that sign.
        if i + 1 < len(coder) and j < len(reference):
            first = crosswalk.mapping_for(coder[i])
            second = crosswalk.mapping_for(coder[i + 1])
            if (
                first["status"] == second["status"] == "mapped"
                and first["candidates"] == second["candidates"] == (reference[j],)
            ):
                consider(
                    _segment(
                        operation="merge",
                        status="agreement",
                        reason="two_m_tokens_contract_to_one_p",
                        coder_tokens=coder[i : i + 2],
                        reference_tokens=[reference[j]],
                        candidates=[first["candidates"], second["candidates"]],
                        agreements=1,
                    ),
                    i + 2,
                    j + 1,
                )

        if j < len(reference):
            consider(
                _segment(
                    operation="deletion",
                    status="error",
                    reason="reference_token_missing_from_coder_record",
                    coder_tokens=[],
                    reference_tokens=[reference[j]],
                    candidates=[],
                    errors=1,
                ),
                i,
                j + 1,
            )
        if i < len(coder):
            consider(
                _segment(
                    operation="insertion",
                    status="error",
                    reason="extra_coder_token",
                    coder_tokens=[coder[i]],
                    reference_tokens=[],
                    candidates=[crosswalk.mapping_for(coder[i])["candidates"]],
                    errors=1,
                ),
                i + 1,
                j,
            )
        return max(options, key=lambda item: item[0])

    return list(best(0, 0)[1])


def _load_json(path: Path | str) -> dict | list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _calibration_entries(calibration: Mapping) -> dict[str, list[str]]:
    entries = calibration.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("calibration set must contain a non-empty 'entries' list")
    references: dict[str, list[str]] = {}
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise ValueError("each calibration entry must be an object")
        key = entry.get("canonical_key")
        sequence = entry.get("reference_p_sequence")
        if not isinstance(key, str) or not key:
            raise ValueError("each calibration entry needs a canonical_key")
        if key in references:
            raise ValueError(f"duplicate calibration entry: {key}")
        if not isinstance(sequence, list) or not all(
            isinstance(token, str) for token in sequence
        ):
            raise ValueError(f"{key}: reference_p_sequence must be a list of tokens")
        references[key] = list(sequence)
    return references


def _coder_records(coder_data: Mapping | list) -> dict[str, list[str]]:
    if isinstance(coder_data, Mapping) and isinstance(
        coder_data.get("records_by_key"), Mapping
    ):
        raw_records = [
            {"canonical_key": key, "m77_sequence": sequence}
            for key, sequence in coder_data["records_by_key"].items()
        ]
    elif isinstance(coder_data, Mapping):
        raw_records = coder_data.get("records")
    else:
        raw_records = coder_data
    if not isinstance(raw_records, list) or not raw_records:
        raise ValueError("coder data must contain a non-empty records list")
    records: dict[str, list[str]] = {}
    for record in raw_records:
        if not isinstance(record, Mapping):
            raise ValueError("each coder record must be an object")
        key = record.get("canonical_key")
        sequence = (
            record.get("m77_sequence")
            or record.get("mahadevan_sequence")
            or record.get("tokens")
        )
        if not isinstance(key, str) or not key:
            raise ValueError("each coder record needs a canonical_key")
        if key in records:
            raise ValueError(f"duplicate coder record: {key}")
        if not isinstance(sequence, list) or not all(
            isinstance(token, str) for token in sequence
        ):
            raise ValueError(f"{key}: m77_sequence must be a list of tokens")
        records[key] = list(sequence)
    return records


def score_calibration(
    calibration: Mapping,
    coder_data: Mapping | list,
    crosswalk: Crosswalk,
) -> dict:
    """Score coder records against a calibration set.

    Returns per-object segment detail plus aggregate counts. The
    per-token agreement rate excludes ambiguous reference tokens from
    its denominator by design.
    """
    references = _calibration_entries(calibration)
    records = _coder_records(coder_data)
    missing = sorted(set(references) - set(records))
    extra = sorted(set(records) - set(references))
    if missing or extra:
        raise ValueError(
            "coder record set does not match calibration set: "
            f"missing={missing} extra={extra}"
        )

    objects = []
    totals = Counter()
    operation_counts = Counter()
    reason_counts = Counter()
    for key in sorted(references):
        reference = references[key]
        coder = records[key]
        segments = align_object(crosswalk, coder, reference)
        counts = Counter()
        for segment in segments:
            counts["agreements"] += segment["agreements"]
            counts["errors"] += segment["errors"]
            counts["ambiguous_tokens"] += segment["ambiguous_tokens"]
            operation_counts[segment["operation"]] += 1
            reason_counts[segment["reason"]] += 1
            for coder_token in segment["coder_tokens"]:
                if coder_token in crosswalk.conflict_signs:
                    counts["contested_core_tokens"] += 1
        scored = counts["agreements"] + counts["errors"]
        exact = (
            counts["errors"] == 0
            and counts["ambiguous_tokens"] == 0
            and counts["agreements"] == len(reference)
        )
        exact_excluding_ambiguous = counts["errors"] == 0 and counts["agreements"] > 0
        row = {
            "canonical_key": key,
            "coder_m77_sequence": coder,
            "reference_p_sequence": reference,
            "segments": segments,
            "reference_tokens": len(reference),
            "coder_tokens": len(coder),
            "agreements": counts["agreements"],
            "errors": counts["errors"],
            "ambiguous_tokens": counts["ambiguous_tokens"],
            "contested_core_tokens": counts["contested_core_tokens"],
            "per_token_agreement": (counts["agreements"] / scored) if scored else None,
            "exact_sequence": exact,
            "exact_excluding_ambiguous_tokens": exact_excluding_ambiguous,
        }
        objects.append(row)
        totals["reference_tokens"] += len(reference)
        totals["coder_tokens"] += len(coder)
        totals["agreements"] += counts["agreements"]
        totals["errors"] += counts["errors"]
        totals["ambiguous_tokens"] += counts["ambiguous_tokens"]
        totals["contested_core_tokens"] += counts["contested_core_tokens"]
        totals["exact_sequence_objects"] += int(exact)
        totals["exact_excluding_ambiguous_objects"] += int(
            exact_excluding_ambiguous
        )

    scored = totals["agreements"] + totals["errors"]
    return {
        "crosswalk": dict(crosswalk.stats),
        "aggregate": {
            "objects": len(objects),
            "reference_tokens": totals["reference_tokens"],
            "coder_tokens": totals["coder_tokens"],
            "agreements": totals["agreements"],
            "errors": totals["errors"],
            "ambiguous_tokens": totals["ambiguous_tokens"],
            "contested_core_tokens": totals["contested_core_tokens"],
            "scored_tokens": scored,
            "per_token_agreement": (totals["agreements"] / scored)
            if scored
            else None,
            "exact_sequence_objects": totals["exact_sequence_objects"],
            "exact_sequence_rate": totals["exact_sequence_objects"] / len(objects),
            "exact_excluding_ambiguous_objects": totals[
                "exact_excluding_ambiguous_objects"
            ],
            "exact_excluding_ambiguous_rate": totals[
                "exact_excluding_ambiguous_objects"
            ]
            / len(objects),
            "operations": dict(sorted(operation_counts.items())),
            "segment_reasons": dict(sorted(reason_counts.items())),
        },
        "objects": objects,
    }


def score_files(
    calibration_path: Path | str,
    coder_records_path: Path | str,
    crosswalk_path: Path | str = DEFAULT_CROSSWALK,
) -> dict:
    calibration = _load_json(calibration_path)
    coder_data = _load_json(coder_records_path)
    if not isinstance(calibration, Mapping):
        raise ValueError("calibration set JSON must be an object")
    return score_calibration(
        calibration, coder_data, Crosswalk.load_csv(crosswalk_path)
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score M77 calibration records against P references."
    )
    parser.add_argument("--calibration", required=True, type=Path)
    parser.add_argument("--coder-records", required=True, type=Path)
    parser.add_argument("--crosswalk", type=Path, default=DEFAULT_CROSSWALK)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    report = score_files(args.calibration, args.coder_records, args.crosswalk)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
