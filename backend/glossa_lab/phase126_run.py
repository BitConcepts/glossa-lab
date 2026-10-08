"""Phase-126 — orchestration: load the two frozen inputs ->
assert counts + anchors hash -> build per-CANDIDATE Wells
treatment records -> cross-tabulate against the anchor
evidence features -> reports (results JSON + design-input
memo).

DESCRIPTIVE ONLY. This phase:

  * takes exactly the 113 anchors whose ``confidence`` field
    is ``CANDIDATE`` in
    ``backend/reports/INDUS_FINAL_ANCHORS.json``;
  * records, for each, its Wells treatment from the
    Phase-123 witness table
    (``data/crosswalks/wells_segmentation_witness_v1.json``;
    semantics per
    ``reports/phase123_wells_segmentation_witness.md``);
  * cross-tabulates treatment against the evidence features
    actually recorded in the anchors file (exact field names;
    see glossa_lab.phase126_wells_split);
  * writes a DESIGN-INPUT memo: facts a future battery spec
    may use. It phrases no adjudication of any sign's
    status, proposes no promotion or demotion, and changes
    no anchor. The anchors file is never opened for writing;
    its sha256 is asserted identical before and after.
  * does not touch the 44 ``pending_non_sa_validation``
    anchors (verified disjoint from the 113; excluded).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.phase126_wells_split import (  # noqa: E402
    build_cross_tabs, build_records,
    candidate_signs, headline_counts, pending_signs,
    shared_split_components, split_size_distribution,
)

ANCHORS_PATH = _BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
WITNESS_PATH = _REPO / "data" / "crosswalks" \
    / "wells_segmentation_witness_v1.json"
RESULTS_PATH = _REPO / "reports" \
    / "phase126_wells_split_candidates_results.json"
MEMO_PATH = _REPO / "reports" / "phase126_wells_split_candidates.md"
DATE = "2026-10-08"
ANCHORS_SHA256 = ("eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86"
                  "ebb1fa3b602cfaed")
EXPECTED_CANDIDATES = 113
EXPECTED_PENDING = 44
EXPECTED_WITNESS_ROWS = 157


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_results() -> dict:
    """Pure build (no writes, no clock): two calls return
    equal dicts."""
    anchors_doc = json.loads(ANCHORS_PATH.read_text("utf-8"))
    witness_doc = json.loads(WITNESS_PATH.read_text("utf-8"))
    witness_rows = witness_doc["rows"]
    assert len(witness_rows) == EXPECTED_WITNESS_ROWS

    candidates = candidate_signs(anchors_doc)
    pending = pending_signs(anchors_doc)
    assert len(candidates) == EXPECTED_CANDIDATES, len(candidates)
    assert len(pending) == EXPECTED_PENDING, len(pending)
    assert not (set(candidates) & pending)

    records = build_records(candidates, witness_rows)
    assert len(records) == EXPECTED_CANDIDATES
    assert {r["sign"] for r in records} == set(candidates)

    headline = headline_counts(records)
    assert sum(headline.values()) == EXPECTED_CANDIDATES

    return {
        "phase": 126,
        "date": DATE,
        "framing": (
            "Descriptive design input only. Records the "
            "Phase-123 Wells witness treatment of each of the "
            "113 CANDIDATE anchors and cross-tabulates it "
            "against the evidence features recorded in the "
            "anchors file. No adjudication of any sign's "
            "status, no promotion or demotion proposed, no "
            "anchor changed."),
        "inputs": {
            "anchors": {
                "path": "backend/reports/INDUS_FINAL_ANCHORS.json",
                "sha256": ANCHORS_SHA256,
                "analysis_set": "confidence == 'CANDIDATE'",
                "n_candidate": len(candidates),
                "n_pending_non_sa_validation_excluded": len(pending),
            },
            "wells_witness": {
                "path": "data/crosswalks/"
                        "wells_segmentation_witness_v1.json",
                "phase": 123,
                "n_rows": len(witness_rows),
                "semantics": "reports/"
                             "phase123_wells_segmentation_witness.md",
            },
        },
        "headline_counts": headline,
        "split_size_distribution": split_size_distribution(records),
        "shared_split_components": shared_split_components(records),
        "cross_tabs": build_cross_tabs(records),
        "records": records,
    }


def run_all(write: bool = True) -> dict:
    anchors_hash_before = _sha256(ANCHORS_PATH)
    assert anchors_hash_before == ANCHORS_SHA256, anchors_hash_before

    results = build_results()
    results["anchors_sha256_before"] = anchors_hash_before

    anchors_hash_after = _sha256(ANCHORS_PATH)
    assert anchors_hash_after == anchors_hash_before
    results["anchors_sha256_after"] = anchors_hash_after
    results["anchors_unchanged"] = anchors_hash_after == anchors_hash_before

    if write:
        RESULTS_PATH.write_text(
            json.dumps(results, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
        MEMO_PATH.write_text(_memo(results), encoding="utf-8")
    return results


# ── Memo rendering ────────────────────────────────────────

def _sign_list(records: list[dict], treatment: str) -> str:
    return ", ".join(r["sign"] for r in records
                     if r["wells_treatment"] == treatment)


def _tab_table(tab: dict) -> str:
    lines = ["| Key | split | merge | unit-same | not-covered "
             "| indeterminate | total |",
             "|---|---|---|---|---|---|---|"]
    for key, counts in tab.items():
        total = sum(counts.values())
        lines.append(
            f"| {key} | {counts['split']} | {counts['merge']} | "
            f"{counts['unit-same']} | {counts['not-covered']} | "
            f"{counts['indeterminate']} | {total} |")
    return "\n".join(lines)


def _split_table(records: list[dict]) -> str:
    lines = ["| Sign | Wells graphemes (split components) | "
             "n components | `basis` freq |",
             "|---|---|---|---|"]
    for r in records:
        if r["wells_treatment"] != "split":
            continue
        lines.append(
            f"| {r['sign']} | {'; '.join(r['wells_graphemes'])} | "
            f"{r['n_wells_graphemes']} | {r['basis_freq']} |")
    return "\n".join(lines)


def _memo(results: dict) -> str:
    h = results["headline_counts"]
    recs = results["records"]
    ct = results["cross_tabs"]
    sizes = results["split_size_distribution"]
    sizes_txt = ", ".join(f"{n} into {k}"
                          for k, n in sorted(
                              sizes.items(), key=lambda kv: int(kv[0])))
    shared = results["shared_split_components"]
    shared_txt = "; ".join(
        f"W{g} in the split sets of {', '.join(signs)}"
        for g, signs in shared.items())
    indet = [r for r in recs if r["wells_treatment"] == "indeterminate"]
    indet_txt = "\n".join(
        f"- {r['sign']} — witness note: {r['witness_note']}"
        for r in indet)
    notcov = [r for r in recs if r["wells_treatment"] == "not-covered"]
    notcov_txt = "\n".join(
        f"- {r['sign']} — witness note: {r['witness_note']}"
        for r in notcov)
    absent = [r["sign"] for r in recs if not r["witness_present"]]
    merges = [r for r in recs if r["wells_treatment"] == "merge"]
    merge_txt = "\n".join(
        f"- {r['sign']} → Wells grapheme "
        f"{'; '.join(r['wells_graphemes'])} "
        f"(method {r['correspondence_method']})"
        for r in merges)
    return f"""# Phase-126 — Wells-Split Descriptive Analysis of the 113 CANDIDATE Anchors (Design-Input Memo)

**Status:** descriptive design input. **Date:** {DATE}. **Phase:** 126
(owner-ordered Glossa-Lab program, 2026-10-08, step 3).

**Framing (hard).** This memo records facts only: how the Phase-123
Wells segmentation witness treats each of the 113 CANDIDATE anchors,
and how that treatment distributes across the evidence features the
anchors file itself records for those signs. It is addressed to
future battery design. It phrases **no** adjudication of any sign's
status, proposes **no** promotion or demotion, and changes **no**
anchor: the anchors file is byte-identical before and after
(sha256 {results['anchors_sha256_after']}, asserted in code).

## 1. Inputs

- **Anchors:** `backend/reports/INDUS_FINAL_ANCHORS.json`. The
  analysis set is exactly the anchors whose `confidence` field is
  `CANDIDATE` — **113 signs**. The 44 anchors carrying
  `validation_status` = `pending_non_sa_validation` are a disjoint
  set and are not analysed here.
- **Wells witness:** `data/crosswalks/wells_segmentation_witness_v1.json`
  (Phase-123; 157 rows) with the classification semantics of
  `reports/phase123_wells_segmentation_witness.md` — SAME / SPLIT /
  MERGE / NOT-COVERED / INDETERMINATE. In this memo's vocabulary:
  SPLIT → **split**, MERGE → **merge**, SAME → **unit-same**,
  NOT-COVERED → **not-covered**, INDETERMINATE → **indeterminate**.
  "Split" means Wells segments what the program's signary treats as
  one sign into multiple graphemes (a compound-suspect under Wells);
  the split components are the witness table's `wells_graphemes`.

## 2. Headline counts (of the 113 CANDIDATEs)

| Wells treatment | Count |
|---|---|
| split | {h['split']} |
| merge | {h['merge']} |
| unit-same | {h['unit-same']} |
| not-covered | {h['not-covered']} |
| indeterminate | {h['indeterminate']} |
| **total** | **113** |

Wells treatment is determinable for
**{h['split'] + h['merge'] + h['unit-same']} of 113** signs
(split + merge + unit-same). The witness is silent, in the senses
recorded in §6, for the remaining
**{h['not-covered'] + h['indeterminate']}**.

## 3. Compound-suspects under Wells (split, {h['split']})

These are the CANDIDATE signs that Wells's segmentation divides
into multiple graphemes. Split-size distribution (signs into
graphemes): {sizes_txt}.

{_split_table(recs)}

Shared components (descriptive): {shared_txt}. In the witness's
own terms, the split sets of these signs are therefore not
disjoint partitions of the CANDIDATE set.

## 4. Unit-confirmed under Wells (unit-same, {h['unit-same']})

For these signs the witness records exactly one Wells grapheme,
unshared — Wells treats the sign as one unit, as the program's
signary does:

{_sign_list(recs, 'unit-same')}

## 5. Merge ({h['merge']})

For these signs the sign's one Wells grapheme is shared with
other Mahadevan signs in the witness table:

{merge_txt}

## 6. Where the witness is silent ({h['not-covered'] + h['indeterminate']})

**Not-covered ({h['not-covered']}).** Signs the witness classed
NOT-COVERED (glyph searched for in the Phase-123 plates and not
found, per the witness note):

{notcov_txt}

CANDIDATE signs absent from the witness table altogether:
**{len(absent)}**{(" (" + ", ".join(absent) + ")") if absent else ""}.
Any such sign would be counted and listed here as not-covered by
construction of the builder; none occurs in the current inputs.

**Indeterminate ({h['indeterminate']}).** Signs for which the
witness records no determinable treatment, with the witness's
reason per sign:

{indet_txt}

## 7. Cross-tabulations (counts only)

Treatment is cross-tabulated against the evidence features
actually present in the anchors file for these 113 signs, named
by their exact field names. Three features are constant across
the set and are stated as facts rather than tabulated:
`basis` records the positional profile I=0.000 / T=0.000 /
M=1.000 (medial-only) for **all 113** signs, and `source` is
`Phase-111` for **all 113**; `validation_status` is
`premise_superseded` for **all 113** (the tables below carry
these fields in full regardless).

### 7.1 By attestation count parsed from `basis` (`freq=`)

{_tab_table(ct['by_basis_freq'])}

### 7.2 By `validation_status` field

{_tab_table(ct['by_validation_status_field'])}

### 7.3 By `_phase132_note` presence in the anchor entry

{_tab_table(ct['by_phase132_note_presence'])}

### 7.4 By `phase109_annotation` presence in the anchor entry

{_tab_table(ct['by_phase109_annotation_presence'])}

### 7.5 By Phase-252 cohort fields (`phase_upgraded` present)

The four signs carrying `phase_upgraded` are the same four
carrying `dedr` / `dedr_source` / `upgrade_basis`
(the Phase-252 allograph cohort recorded in the anchors file):

{_tab_table(ct['by_phase252_cohort'])}

### 7.6 By witness `correspondence_method` (witness-table field)

{_tab_table(ct['by_correspondence_method'])}

### 7.7 By witness `verification` (Phase-123 hand-verification)

{_tab_table(ct['by_verification'])}

## 8. Design-input facts (for a future battery spec)

Stated as facts about the recorded material; what a future
spec does with them is that spec's decision, not this memo's.

1. Of the 113 CANDIDATEs, **{h['split']}** are compound-suspects
   under Wells: a battery whose unit of analysis is the pooled
   sign would, for these signs, be pooling tokens that Wells's
   segmentation assigns to two or more graphemes (§3).
2. **{h['unit-same']}** CANDIDATEs are unit-confirmed under
   Wells: the witness records one unshared grapheme for each
   (§4).
3. **{h['merge']}** CANDIDATEs share their single Wells grapheme
   with other Mahadevan signs (§5); in the witness's terms their
   token sets are not separable from those signs' token sets by
   Wells grapheme identity alone.
4. For **{h['not-covered'] + h['indeterminate']}** CANDIDATEs
   the Wells witness states no determinable treatment (§6); a
   future design that needs a Wells-treatment value for every
   CANDIDATE has no recorded value for these signs in the
   Phase-123 table.
5. The split components overlap across CANDIDATEs (§3): the
   recorded Wells graphemes are shared between the split sets
   of {len({s for signs in shared.values() for s in signs})}
   distinct CANDIDATE signs.
6. Every CANDIDATE's `basis` records the same positional
   profile (I=0.000 / T=0.000 / M=1.000) and one of four
   attestation counts (freq 1–4); the cross-tab in §7.1 is the
   full joint distribution of Wells treatment against that
   recorded attestation count.
7. The witness's determinate treatments for CANDIDATEs rest on
   the `correspondence_method` distribution in §7.6 (registry
   cross-match vs hand glyph match vs glyph-search-negative),
   and the Phase-123 hand-verification in §7.7 covers
   {sum(1 for r in recs if r['verification'])} of the 113.

## 9. What this memo does not do

It does not adjudicate any sign's status; it does not propose
adopting, rejecting, or hybridising Wells's segmentation; it
does not rank Wells's segmentation against any other; and it
draws no conclusion about any anchor's reading. "Compound-
suspect" and "unit-confirmed" above are descriptions of the
witness's treatment of a sign, nothing more.

## 10. Reproducibility

```
~/workspace/venvs/glossa-lab/bin/python backend/scripts/phase126_wells_split_candidates.py
~/workspace/venvs/glossa-lab/bin/python -m pytest backend/tests/test_phase126_wells_split_candidates.py
```

The builder reads only the two committed inputs named in §1,
asserts the anchors sha256 before and after, and is
deterministic (two runs byte-identical).

---

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
"""


if __name__ == "__main__":
    out = run_all()
    print(json.dumps(out["headline_counts"], indent=1))
    print("anchors_unchanged:", out["anchors_unchanged"])
