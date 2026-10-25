#!/usr/bin/env python3
"""Phase 441 — Spec 075 execution: the depicted-kind
endings atlas. For each kind of thing the published sign
identifications depict (other, human, animal, object_goods),
do that kind's signs gather at the ends of inscriptions, on
the graded Shakti corpus over the keying surface Spec 073
repaired (Registry v2 / Asset A v2)?

Runs the frozen Spec 075 contract (freeze digest
aa06726f545218c5bcee4b3a5df94c920828fead4e06e2ccec1eeffce44ac5cf;
OSF registration jv74f, approved and public, DOI
10.17605/OSF.IO/JV74F): the step-0 gates of spec section 6
in order, fail-closed, then the per-kind battery of
section 5. This study mints its own claim family (F075);
it is not Spec 071's retired sky-signs question and not a
test of Hunt's claims in any form. The celestial class is
pre-registered EMPTY in Asset A v2 and is reported first,
never tested (spec sections 1.4, 5.5).

Gate order (spec section 6, fail-closed):
  0.1 Asset pins: Asset A v2 and Registry v2 asserted
      against Spec 073's executed record — both v2 freeze
      records present (else ASSET NOT FROZEN); the files'
      SHA-256 digests, row counts, and Asset A v2's
      per-kind and dispute-status counts recomputed and
      equal to section 3's pins (else ASSET PIN MISMATCH).
  0.2 Shakti intake: the corpus and row-grades files hash
      at their restricted-local paths to the intake
      record's pins; the grade counts are recounted (else
      SHAKTI INTAKE NOT REPRODUCED).
  0.3 Input integrity: the crosswalk, Registry v1, and
      anchors pins recomputed in the tree and equal; the
      anchors file asserted byte-identical before and
      after (else INVALID, the input named).
  0.4 Population reproduction and keying: the primary
      population (documented-lineage rows only; analyzable
      = recorded symbol list non-empty and not all 000;
      sequence = symbols with 000 dropped) must reproduce
      3,045 analyzable rows, 557 distinct signs, 550 in
      sequences of length >= 2 (else POPULATION NOT
      REPRODUCED). Every enumerated sign is then keyed to
      exactly one Asset A v2 row under the two-leg route
      of DD-075-5 (Spec 074's DD-074-8): leg 1, a sign's
      ICIT code (its Wells number) resolved through
      Registry v2's parpola_1982 rows' wells_ids to
      exactly one sign_key; leg 2, Registry v2's
      icit_wells rows, whose sign_id is the sign's own
      Wells code. Zero or multiple resolutions across
      both legs is unkeyable and closes POPULATION NOT
      KEYED, the sign named — with the single named
      exception of token 999, excluded in advance by
      section 4.3 and recorded here with its counts.
      (Flagged in the spec: this gate's population
      reproduction is a replay/drift gate over quantities
      verified at the freeze.)
  0.5 The census, published before rates: member signs
      and pooled occurrences per class (other, human,
      animal, object_goods), the unidentified count,
      token 999's count, and the corpus-wide
      final-position rate as descriptive context. The
      floors of section 4.5 (20 member signs, 30 pooled
      occurrences) are applied to the census here; a kind
      below either floor is TOO THIN in the census
      record itself. The borderline signs S1 will remove
      are named here.
  0.6 Freeze-order proof, each assertion cited to the
      external record, never to this spec's own outcome:
      this spec's freeze digest recomputed from the
      frozen sources and matched; the freeze PR's merge
      state read from the repo record (PR #389, merge
      commit fd9bd448); this spec's OSF registration read
      as approved and public from the OSF record
      (jv74f). A mismatch closes INVALID, the failed
      assertion named.

Battery (spec section 5): a sign occurrence is in
text-final position when it is the last sign of its
inscription's recorded sequence; sequences are the
population's recorded sequences in recorded order, no
reversal, no length floor beyond the population's own
construction. Per tested kind K: K's pooled
final-position rate against the pooled rate of K's
comparison class — the signs of the other identified
kinds whose total occurrence count lies within K's own
member band [min, max], inclusive; unidentified signs
are members of no class and no comparison class
(section 2.3, DD-075-4) — by Fisher's exact test
(two-sided) on the pooled 2x2 at the 5% level.
Verdicts per kind (section 5.2): SUPPORTED at
enrichment ratio >= 1.5, the exact test significant at
5%, and at least half the kind's occurrences from
member signs individually above the corpus-wide
final-position rate; NOT SUPPORTED at ratio <= 1.0 (the
falsifier's word, stated in advance); INCONCLUSIVE
between; TOO THIN below a floor. Four verdicts, no
pooled verdict. Per-sign tables are published in full
for every kind (section 5.3). Sensitivities (section
5.4), per kind, beside the primary, never replacing
its word: S1 borderline removed; S2 contested included
under CISI-governed labels (Asset A v2 carries zero
contested rows, so S2 is expected to equal the primary
and is reported as such); S3 the documented +
corroborated population, every quantity recomputed,
a verdict change reported as grade-sensitive.

The corpus and grades files are restricted-local and
never enter the repository; only derived quantities
are written, to reports/phase441_results.json.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DOWNLOADS = Path(
    "/home/hatch/workspace/research_notes/"
    "indus-data-deep-sweep-20261008/downloads"
)
CORPUS_FILE = (
    DOWNLOADS / "shaktiosindia-indus-sign-regimes-deposit"
    / "sanitized_corpus.json"
)
GRADES_FILE = DOWNLOADS / "shakti_row_grades_2026-10-22.csv"
OSF_API = Path("/home/hatch/workspace/skills/osf/bin/osf_api.py")

SPEC073_DIR = REPO / "specs/073-keying-surface-repair"
REGISTRY_V2_FREEZE = SPEC073_DIR / "registry-v2" / "registry-v2-freeze.json"
ASSET_V2_FREEZE = SPEC073_DIR / "asset-a-v2" / "asset-a-v2-freeze.json"
ASSET_V2_CSV = SPEC073_DIR / "asset-a-v2" / "depicted-kind-classification.csv"
REGISTRY_V2 = REPO / "data/crosswalks/canonical_sign_registry_v2.csv"
REGISTRY_V1 = REPO / "data/crosswalks/canonical_sign_registry.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
SPEC075_DIR = REPO / "specs/075-depicted-kind-endings-atlas"
SPEC075_FREEZE_JSON = SPEC075_DIR / "freeze.json"
SPEC075_BUILD_FREEZE = SPEC075_DIR / "build_freeze.py"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
RESULTS = REPO / "reports/phase441_results.json"

SPEC075_FREEZE_DIGEST = (
    "aa06726f545218c5bcee4b3a5df94c920828fead4e06e2ccec1eeffce44ac5cf"
)
OSF_REGISTRATION = "jv74f"
OSF_DOI = "10.17605/OSF.IO/JV74F"
FREEZE_PR = 389
FREEZE_MERGE_COMMIT = "fd9bd448"
EXECUTION_DATE = "2026-10-25"
REGISTRY_V2_SHA256 = (
    "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"
)
ASSET_V2_SHA256 = (
    "681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193"
)
REGISTRY_V1_SHA256 = (
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
)
CROSSWALK_SHA256 = (
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
CORPUS_SHA256 = (
    "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
)
GRADES_SHA256 = (
    "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
)
ASSET_V2_PER_KIND = {
    "other": 246, "unidentified": 211, "human": 43,
    "animal": 30, "object_goods": 22, "sky_cycle": 0,
}
ASSET_V2_DISPUTE = {"none": 548, "borderline": 4, "contested": 0}
IDENTIFIED_KINDS = ("other", "human", "animal", "object_goods")
POPULATION_FIGURES = {
    "analyzable_rows": 3045, "distinct_signs": 557,
    "signs_in_sequences_ge2": 550,
}
GRADE_COUNTS = {
    "documented-lineage": 3212,
    "undocumented-corroborated": 2087,
    "undocumented-uncorroborated": 405,
}
FLOOR_SIGNS = 20
FLOOR_OCCURRENCES = 30
LINEAGE_STATEMENT = (
    "This corpus is an ICIT-lineage corpus. Agreement between "
    "it and the program's earlier ICIT-lineage layer is "
    "consistency within one tradition, not independent "
    "corroboration."
)
CELESTIAL_ARM = (
    "The celestial class as frozen in Asset A v2 contains zero "
    "signs; there is no celestial rate. The empty class is the "
    "Spec 071 line's closing finding (retirement decision, "
    "2026-10-25), restated here because this atlas is where a "
    "reader would look for it. It establishes nothing new "
    "about sky signs."
)
FAMILY_STATEMENT = (
    "The verdicts of Spec 075 are per kind, four words "
    "published together with their per-sign tables in one "
    "outcome record, each computed by section 5.2's frozen "
    "criteria — and no pooled verdict over depicted kinds is "
    "computed, stated, or implied by any arrangement of "
    "the four."
)

GRADE_DOCUMENTED = "documented-lineage"
GRADE_CORROBORATED = "undocumented-corroborated"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon_sha(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


# ── Fisher exact test (exact integer hypergeometric) ──────────────

def _hypergeom_pmf(k, n_total, n_drawn, n_success):
    """P(X = k), X ~ Hypergeometric(N=n_total, K=n_success, n=n_drawn)."""
    if k < 0 or k > n_success or k > n_drawn or (n_drawn - k) > (n_total - n_success):
        return 0.0
    return (
        math.comb(n_success, k)
        * math.comb(n_total - n_success, n_drawn - k)
        / math.comb(n_total, n_drawn)
    )


def fisher_exact(table):
    """table [[a, b], [c, d]] -> (one-sided greater p, two-sided p)."""
    (a, b), (c, d) = table
    n = a + b + c + d
    row1 = a + b
    col1 = a + c
    lo = max(0, row1 - (n - col1))
    hi = min(row1, col1)
    p_obs = _hypergeom_pmf(a, n, row1, col1)
    p_greater = sum(
        _hypergeom_pmf(k, n, row1, col1) for k in range(a, hi + 1)
    )
    p_two = sum(
        p for k in range(lo, hi + 1)
        if (p := _hypergeom_pmf(k, n, row1, col1)) <= p_obs * (1 + 1e-9)
    )
    return p_greater, p_two


# ── Two-leg keying route (DD-075-5: DD-074-8 carried) ────────────

def keying_maps():
    """Returns (leg1, leg2): leg 1 maps a Wells id to the set of
    registry sign_ids reached through parpola_1982 rows'
    wells_ids over Registry v2; leg 2 is the set of sign_ids
    carried by Registry v2's icit_wells rows (the sign_id of
    such a row is the Wells id itself)."""
    leg1: dict[str, set[str]] = {}
    leg2: set[str] = set()
    with REGISTRY_V2.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["numbering_system"] == "parpola_1982":
                for token in (row["wells_ids"] or "").split("|"):
                    token = token.strip()
                    if token:
                        leg1.setdefault(token, set()).add(row["sign_id"])
            elif row["numbering_system"] == "icit_wells":
                leg2.add(row["sign_id"])
    return leg1, leg2


def key_sign(code: str, leg1, leg2):
    """DD-074-8: ICIT code n -> Wells token W + n zero-padded.

    Leg 1 (DD-070-9 carried): resolve through the registry's
    parpola_1982 rows' wells_ids to exactly one sign_key.
    Leg 2: the icit_wells row whose sign_id is the Wells id
    itself, to the Asset A v2 row of that sign_key.
    Zero or multiple resolutions across both legs is
    unkeyable. Returns (sign_key, leg, reason)."""
    token = "W" + code.zfill(3)
    hits = leg1.get(token, set())
    if len(hits) == 1:
        return next(iter(hits)), "leg1_parpola_1982", None
    if len(hits) > 1:
        return None, None, (
            f"Wells id {token} resolves to {len(hits)} distinct "
            "sign ids under leg 1 (parpola_1982 wells_ids)"
        )
    if token in leg2:
        return token, "leg2_icit_wells", None
    return None, None, (
        f"no parpola_1982 registry row carries Wells id {token} "
        f"and no icit_wells row carries sign id {token}"
    )


# ── Population and counting machinery (spec sections 2-3) ───────

def sequences_of(rows):
    """Analyzable sequences under section 3's construction:
    the recorded symbol list with 000 tokens dropped; a row
    is analyzable when the resulting sequence is non-empty."""
    seqs = []
    for symbols in rows:
        seq = [s for s in symbols if s != "000"]
        if seq:
            seqs.append(seq)
    return seqs


def sign_counts(seqs):
    """Per-sign (total, final) occurrence counts over a
    population's sequences, in recorded order: the last sign
    of each sequence is its text-final occurrence (section
    2.1). Returns (totals, finals)."""
    totals: dict[str, int] = {}
    finals: dict[str, int] = {}
    for seq in seqs:
        for sign in seq:
            totals[sign] = totals.get(sign, 0) + 1
        finals[seq[-1]] = finals.get(seq[-1], 0) + 1
    return totals, finals


def verdict_of(ratio, p_two, half_met):
    """Section 5.2's frozen bands."""
    if ratio is None or p_two is None:
        return "INCONCLUSIVE"
    if ratio <= 1.0:
        return "NOT SUPPORTED"
    if ratio >= 1.5 and p_two < 0.05 and half_met:
        return "SUPPORTED"
    return "INCONCLUSIVE"


def kind_block(kind, totals, finals, kinds_of, keyed, asset,
               corpus_wide_rate, apply_floors):
    """One kind's test block (section 5.1-5.3) over one
    population and one sign universe.

    kinds_of: corpus code -> depicted kind (the arm's
    universe; signs absent from it are in no class).
    keyed: corpus code -> Asset A v2 sign_key.
    asset: sign_key -> Asset A v2 row (label, citations).
    """
    members = sorted(
        s for s in totals if kinds_of.get(s) == kind)
    member_signs = len(members)
    pooled_occ = sum(totals[s] for s in members)
    block = {
        "member_signs": member_signs,
        "pooled_occurrences": pooled_occ,
    }
    if apply_floors and (
            member_signs < FLOOR_SIGNS
            or pooled_occ < FLOOR_OCCURRENCES):
        block["verdict"] = "TOO THIN"
        block["floor_failure"] = {
            "sign_floor": FLOOR_SIGNS,
            "occurrence_floor": FLOOR_OCCURRENCES,
            "member_signs": member_signs,
            "pooled_occurrences": pooled_occ,
        }
        return block
    pooled_final = sum(finals.get(s, 0) for s in members)
    rate = pooled_final / pooled_occ if pooled_occ else None
    band = [min(totals[s] for s in members),
            max(totals[s] for s in members)]
    comp = sorted(
        s for s in totals
        if kinds_of.get(s) in IDENTIFIED_KINDS
        and kinds_of.get(s) != kind
        and band[0] <= totals[s] <= band[1])
    comp_occ = sum(totals[s] for s in comp)
    comp_final = sum(finals.get(s, 0) for s in comp)
    comp_rate = comp_final / comp_occ if comp_occ else None
    ratio = (rate / comp_rate) if (rate is not None and comp_rate) else None
    table = [[pooled_final, pooled_occ - pooled_final],
             [comp_final, comp_occ - comp_final]]
    p_one, p_two = fisher_exact(table) if comp_occ else (None, None)
    above_occ = sum(
        totals[s] for s in members
        if totals[s] and finals.get(s, 0) / totals[s] > corpus_wide_rate)
    half_share = above_occ / pooled_occ if pooled_occ else None
    half_met = half_share is not None and half_share >= 0.5
    per_sign = []
    for s in members:
        row = asset[keyed[s]]
        s_rate = finals.get(s, 0) / totals[s] if totals[s] else None
        per_sign.append({
            "sign": s,
            "sign_key": keyed[s],
            "depicted_label_verbatim": row["depicted_label_verbatim"],
            "source_citations": row["source_citations"],
            "total_occurrences": totals[s],
            "final_occurrences": finals.get(s, 0),
            "final_position_rate": s_rate,
            "above_corpus_wide_rate": (
                s_rate is not None and s_rate > corpus_wide_rate),
        })
    block.update({
        "pooled_final_occurrences": pooled_final,
        "pooled_final_position_rate": rate,
        "member_frequency_band": band,
        "comparison_class": {
            "signs": len(comp),
            "pooled_occurrences": comp_occ,
            "pooled_final_occurrences": comp_final,
            "pooled_final_position_rate": comp_rate,
            "sign_list": comp,
        },
        "table_2x2": table,
        "enrichment_ratio": ratio,
        "fisher_p_two_sided": p_two,
        "fisher_p_one_sided_greater": p_one,
        "half_occurrences_condition": {
            "occurrences_from_signs_above_corpus_wide_rate": above_occ,
            "share_of_kind_occurrences": half_share,
            "met": half_met,
        },
        "verdict": verdict_of(ratio, p_two, half_met),
        "per_sign_table": per_sign,
    })
    return block


def run_arm(seqs, kinds_of, keyed, asset, removed_signs):
    """One arm's full battery over one population/universe:
    the corpus-wide rate over the arm's universe (all signs
    of the population except the arm's removed signs), then
    the four kind blocks with floors applied."""
    totals_all, finals_all = sign_counts(seqs)
    totals = {s: t for s, t in totals_all.items()
              if s not in removed_signs}
    finals = {s: f for s, f in finals_all.items()
              if s not in removed_signs}
    total_occ = sum(totals.values())
    total_final = sum(finals.values())
    cw_rate = total_final / total_occ if total_occ else None
    arm = {
        "corpus_wide_final_position_rate": {
            "final_occurrences": total_final,
            "total_occurrences": total_occ,
            "rate": cw_rate,
        },
        "kinds": {},
    }
    for kind in IDENTIFIED_KINDS:
        arm["kinds"][kind] = kind_block(
            kind, totals, finals, kinds_of, keyed, asset,
            cw_rate, apply_floors=True)
    return arm


def _fmt_rate(x) -> str:
    return "undefined" if x is None else f"{x:.4f}"


def _fmt_ratio(x) -> str:
    return "undefined" if x is None else f"{x:.4f}"


def _fmt_p(x) -> str:
    return "undefined" if x is None else f"{x:.4g}"


def kind_wording(kind, block):
    """Section 5.5's per-kind wordings: the SUPPORTED form
    is the frozen text; the other words are the same form
    with their section 5.2 conditions stated."""
    if block["verdict"] == "TOO THIN":
        return (
            f"**Kind {kind}: TOO THIN.** On the "
            "documented-lineage primary population of the "
            f"Shakti corpus, the {kind} class stands below a "
            "floor of section 4.5 at the step-0 census: "
            f"{block['member_signs']} member signs keyed in "
            f"the population and {block['pooled_occurrences']} "
            "pooled occurrences, against floors of 20 signs "
            "and 30 occurrences. No rate is stated for the "
            "kind: the census is its record, and it is "
            "reported, never dropped or merged into a "
            "neighbour to clear a floor."
        )
    rate = _fmt_rate(block["pooled_final_position_rate"])
    comp = block["comparison_class"]
    comp_rate = _fmt_rate(comp["pooled_final_position_rate"])
    ratio = _fmt_ratio(block["enrichment_ratio"])
    p = _fmt_p(block["fisher_p_two_sided"])
    share = _fmt_rate(
        block["half_occurrences_condition"]
        ["share_of_kind_occurrences"])
    if block["verdict"] == "SUPPORTED":
        return (
            f"**Kind {kind}: SUPPORTED.** On the "
            "documented-lineage primary population of the "
            f"Shakti corpus, the {kind} signs end "
            f"inscriptions at {rate} against {comp_rate} for "
            "signs of comparable frequency from the other "
            f"identified kinds — an enrichment ratio of "
            f"{ratio}, Fisher exact (two-sided) p = {p}, "
            f"with {share} of the kind's occurrences from "
            "signs individually above the corpus-wide "
            "final-position rate. Position is not meaning: "
            "this word states a positional fact about the "
            "published identification layer on this corpus, "
            "and nothing about what any sign means."
        )
    if block["verdict"] == "NOT SUPPORTED":
        return (
            f"**Kind {kind}: NOT SUPPORTED.** On the "
            "documented-lineage primary population of the "
            f"Shakti corpus, the {kind} signs end "
            f"inscriptions at {rate} against {comp_rate} for "
            "signs of comparable frequency from the other "
            f"identified kinds — an enrichment ratio of "
            f"{ratio}, at or below 1.0, the falsifier's "
            "condition of section 1.2: the kind is not "
            "enriched at endings, at the rate signs of "
            "comparable frequency show (Fisher exact "
            f"(two-sided) p = {p}). Position is not meaning: "
            "this word states a positional fact about the "
            "published identification layer on this corpus, "
            "and nothing about what any sign means."
        )
    return (
        f"**Kind {kind}: INCONCLUSIVE.** On the "
        "documented-lineage primary population of the "
        f"Shakti corpus, the {kind} signs end inscriptions "
        f"at {rate} against {comp_rate} for signs of "
        "comparable frequency from the other identified "
        f"kinds — an enrichment ratio of {ratio}, Fisher "
        f"exact (two-sided) p = {p}, with {share} of the "
        "kind's occurrences from signs individually above "
        "the corpus-wide final-position rate. The word "
        "falls between section 5.2's bands: the ratio is "
        "not at or below 1.0, and the SUPPORTED conditions "
        "(ratio at least 1.5, the exact test significant "
        "at the 5% level, and the half-of-occurrences "
        "condition) are not all met. Position is not "
        "meaning: this word states a positional fact about "
        "the published identification layer on this corpus, "
        "and nothing about what any sign means."
    )


# ── Gate 0.6 external readings ────────────────────────────────────

def recompute_freeze_digest():
    """Recompute this spec's freeze digest from the frozen
    sources, through the spec's own build_freeze machinery
    (framework026), without writing freeze.json."""
    import types

    pkg = types.ModuleType("glossa_lab")
    pkg.__path__ = [str(REPO / "backend" / "glossa_lab")]
    sys.modules.setdefault("glossa_lab", pkg)
    spec = importlib.util.spec_from_file_location(
        "spec075_build_freeze", SPEC075_BUILD_FREEZE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    from glossa_lab.framework026 import build_freeze

    record = build_freeze(module.DEFINITION, REPO, module.SOURCES)
    return record["digest"]


def read_freeze_pr_state():
    """The freeze PR's merge state, read from the repo
    record (GitHub API via gh)."""
    out = subprocess.run(
        ["gh", "api",
         f"repos/BitConcepts/glossa-lab/pulls/{FREEZE_PR}"],
        capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        return None, f"gh api failed: {out.stderr.strip()[:200]}"
    pr = json.loads(out.stdout)
    return {
        "number": pr["number"],
        "state": pr["state"],
        "merged_at": pr["merged_at"],
        "merge_commit_sha": pr["merge_commit_sha"],
    }, None


def read_osf_state():
    """This spec's OSF registration state, read from the
    OSF record via the programme's OSF API client."""
    out = subprocess.run(
        [sys.executable, str(OSF_API), "get",
         f"/registrations/{OSF_REGISTRATION}/"],
        capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        return None, f"osf api failed: {out.stderr.strip()[:200]}"
    start = out.stdout.find("{")
    if start < 0:
        return None, "osf api returned no JSON body"
    attrs = json.loads(out.stdout[start:])["data"]["attributes"]
    return {
        "public": attrs["public"],
        "pending_registration_approval":
            attrs["pending_registration_approval"],
        "reviews_state": attrs["reviews_state"],
        "date_registered": attrs["date_registered"],
    }, None


def closure_wording(outcome: str, detail: str) -> str:
    if outcome == "ASSET NOT FROZEN":
        return (
            "Spec 075 closed at step 0: the repaired surface is "
            f"not frozen on record — Spec 073's {detail}. No "
            "class was counted and no quantity was computed. "
            "The claim family stands as recorded."
        )
    if outcome == "ASSET PIN MISMATCH":
        return (
            "Spec 075 closed at step 0: a recomputed asset pin "
            f"disagrees with section 3 — {detail}. No class was "
            "counted and no quantity was computed. The claim "
            "family stands as recorded."
        )
    if outcome == "SHAKTI INTAKE NOT REPRODUCED":
        return (
            "Spec 075 closed at step 0: the Shakti intake did "
            f"not reproduce — {detail}. No class was counted "
            "and no quantity was computed. The claim family "
            "stands as recorded."
        )
    if outcome == "POPULATION NOT REPRODUCED":
        return (
            "Spec 075 closed at step 0: the enumerated primary "
            f"population disagrees with section 3's figures — "
            f"{detail}. The corpus, grades, and construction "
            "are pinned identically to the freeze, so the "
            "difference is non-determinism or input drift, "
            "not a new measurement. No class was counted past "
            "the enumeration and no rate was computed. The "
            "claim family stands as recorded."
        )
    if outcome == "POPULATION NOT KEYED":
        return (
            "Spec 075 closed at step 0: the primary population "
            f"was enumerated in full ({detail}), and the signs "
            "that could not be keyed to exactly one Asset A "
            "v2 row under either leg of the frozen keying "
            "route are listed with their reasons in the "
            "machine record. No class was counted and no rate "
            "was computed. The claim family stands as recorded."
        )
    if outcome == "INVALID":
        return (
            "Spec 075 stopped at step 0 before any "
            f"final-position quantity: {detail}. No verdict "
            "is recorded; the claim family stands as recorded."
        )
    raise ValueError(outcome)


def main() -> int:
    gates: list[dict] = []
    results: dict = {
        "phase": 441, "spec": "075",
        "claim_family": "F075",
        "contract": {
            "freeze_digest": SPEC075_FREEZE_DIGEST,
            "osf_registration": OSF_REGISTRATION,
            "osf_doi": OSF_DOI,
            "freeze_pr": FREEZE_PR,
            "asset_a_v2_sha256": ASSET_V2_SHA256,
            "registry_v2_sha256": REGISTRY_V2_SHA256,
            "registry_v1_sha256": REGISTRY_V1_SHA256,
            "crosswalk_sha256": CROSSWALK_SHA256,
            "anchors_sha256": ANCHORS_SHA256,
        },
        "execution_order": [
            "freeze (Spec 075, digest quoted; freeze PR #389 merged "
            "fd9bd448; OSF jv74f approved and public)",
            "gate 0.1 asset pins (Spec 073's executed record)",
            "gate 0.2 Shakti intake (P-F1 S1/S2)",
            "gate 0.3 input integrity",
            "gate 0.4 population reproduction (3,045 / 557 / 550) "
            "and keying under the two-leg route (DD-075-5); token "
            "999 the named exclusion",
            "gate 0.5 the census, published before any rate; the "
            "floors applied",
            "gate 0.6 freeze-order proof from the external records",
            "the per-kind battery (section 5) and sensitivities "
            "S1-S3",
        ],
        "lineage_statement_PF1_S3": LINEAGE_STATEMENT,
        "celestial_arm": CELESTIAL_ARM,
        "family_statement": FAMILY_STATEMENT,
    }

    def close(outcome: str, **extra):
        results["outcome"] = outcome
        results["gates"] = gates
        results.update(extra)
        if "headline_wording" not in results:
            results["headline_wording"] = closure_wording(
                outcome, extra.get("detail", ""))
        results["anchors"] = {
            "before": anchors_before,
            "after": sha256(ANCHORS),
        }
        results["anchors"]["byte_identical"] = (
            results["anchors"]["before"]
            == results["anchors"]["after"]
            == ANCHORS_SHA256
        )
        RESULTS.write_text(
            json.dumps(results, indent=1) + "\n", encoding="utf-8")
        print(outcome)
        return 0

    anchors_before = sha256(ANCHORS)

    # ── Gate 0.1: asset pins (Spec 073's executed record) ───
    missing = [
        name for name, path in (
            ("registry-v2-freeze.json", REGISTRY_V2_FREEZE),
            ("asset-a-v2-freeze.json", ASSET_V2_FREEZE),
        ) if not path.exists()
    ]
    if missing:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "Spec 073 freeze record(s) absent: "
                                + ", ".join(missing)})
        return close("ASSET NOT FROZEN",
                     detail=f"{missing[0]} does not exist")
    registry_freeze = json.loads(
        REGISTRY_V2_FREEZE.read_text(encoding="utf-8"))
    asset_freeze = json.loads(
        ASSET_V2_FREEZE.read_text(encoding="utf-8"))
    observed_registry_sha = sha256(REGISTRY_V2)
    observed_asset_sha = sha256(ASSET_V2_CSV)
    pin_failures = []
    if (observed_registry_sha != REGISTRY_V2_SHA256
            or registry_freeze.get("sha256") != REGISTRY_V2_SHA256):
        pin_failures.append(
            f"Registry v2 digest {observed_registry_sha}")
    if (observed_asset_sha != ASSET_V2_SHA256
            or asset_freeze.get("sha256") != ASSET_V2_SHA256):
        pin_failures.append(f"Asset A v2 digest {observed_asset_sha}")
    with REGISTRY_V2.open(newline="", encoding="utf-8") as handle:
        registry_rows = list(csv.DictReader(handle))
    with ASSET_V2_CSV.open(newline="", encoding="utf-8") as handle:
        asset_rows = list(csv.DictReader(handle))
    if len(registry_rows) != 1013:
        pin_failures.append(
            f"Registry v2 row count {len(registry_rows)} != 1013")
    if len(asset_rows) != 552:
        pin_failures.append(
            f"Asset A v2 row count {len(asset_rows)} != 552")
    per_kind: dict[str, int] = {}
    dispute: dict[str, int] = {}
    asset: dict[str, dict] = {}
    for row in asset_rows:
        asset[row["sign_key"]] = row
        per_kind[row["depicted_kind"]] = (
            per_kind.get(row["depicted_kind"], 0) + 1)
        dispute[row["dispute_status"]] = (
            dispute.get(row["dispute_status"], 0) + 1)
    presented_kinds = {
        k: per_kind.get(k, 0) for k in ASSET_V2_PER_KIND}
    presented_dispute = {
        k: dispute.get(k, 0) for k in ASSET_V2_DISPUTE}
    if presented_kinds != ASSET_V2_PER_KIND:
        pin_failures.append(
            f"Asset A v2 per-kind counts {presented_kinds}")
    if presented_dispute != ASSET_V2_DISPUTE:
        pin_failures.append(
            f"Asset A v2 dispute counts {presented_dispute}")
    if pin_failures:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "; ".join(pin_failures)})
        return close("ASSET PIN MISMATCH",
                     detail="; ".join(pin_failures))
    gates.append({"gate": "0.1", "result": "PASS",
                  "detail": "Spec 073's executed record shows both "
                            "products frozen; Registry v2 recomputes "
                            "to 42ab09fb... (1,013 rows) and Asset "
                            "A v2 to 681e017d... (552 rows); Asset "
                            "A v2 per-kind counts (other 246, "
                            "unidentified 211, human 43, animal 30, "
                            "object_goods 22, sky_cycle 0) and "
                            "dispute counts (none 548, borderline "
                            "4, contested 0) match section 3"})

    # ── Gate 0.2: Shakti intake, P-F1 S1/S2 ──────────────────
    if (sha256(CORPUS_FILE) != CORPUS_SHA256
            or sha256(GRADES_FILE) != GRADES_SHA256):
        gates.append({"gate": "0.2", "result": "FAIL",
                      "detail": "S1 hash mismatch"})
        return close(
            "SHAKTI INTAKE NOT REPRODUCED",
            detail="the S1 identity failure: a restricted-local "
                   "file's SHA-256 does not recompute to the "
                   "intake record's pin")
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    with GRADES_FILE.open(newline="", encoding="utf-8") as handle:
        grades_rows = list(csv.DictReader(handle))
    grade_of = {g["shakti_id"]: g["grade"] for g in grades_rows}
    grade_counts: dict[str, int] = {}
    for g in grade_of.values():
        grade_counts[g] = grade_counts.get(g, 0) + 1
    analyzable_all = [
        r for r in corpus
        if [s for s in r["symbols"] if s != "000"]]
    intake_ok = (
        len(corpus) == 5704
        and len(analyzable_all) == 5536
        and grade_counts == GRADE_COUNTS
        and all(r["id"] in grade_of for r in corpus)
    )
    if not intake_ok:
        detail = (
            f"rows={len(corpus)}, analyzable={len(analyzable_all)}, "
            f"grade counts={grade_counts}")
        gates.append({"gate": "0.2", "result": "FAIL",
                      "detail": f"S2 census: {detail}"})
        return close("SHAKTI INTAKE NOT REPRODUCED",
                     detail=f"the S2 census failure: {detail}")
    gates.append({"gate": "0.2", "result": "PASS",
                  "detail": "S1 hashes recompute to the intake "
                            "record's pins (corpus 345241b1..., "
                            "grades 02394241...); the census "
                            "reproduces: 5,704 rows, 5,536 "
                            "analyzable, grade counts 3,212 "
                            "documented-lineage / 2,087 "
                            "undocumented-corroborated / 405 "
                            "undocumented-uncorroborated"})

    # ── Gate 0.3: input integrity ────────────────────────────
    integrity_failures = []
    if sha256(CROSSWALK) != CROSSWALK_SHA256:
        integrity_failures.append("sign_crosswalk_master.csv")
    if sha256(REGISTRY_V1) != REGISTRY_V1_SHA256:
        integrity_failures.append("canonical_sign_registry.csv (v1)")
    if anchors_before != ANCHORS_SHA256:
        integrity_failures.append("INDUS_FINAL_ANCHORS.json")
    if integrity_failures:
        gates.append({"gate": "0.3", "result": "FAIL",
                      "detail": "section 3 input hash failure: "
                                + ", ".join(integrity_failures)})
        return close(
            "INVALID",
            detail="gate 0.3 (input integrity): a section 3 "
                   "input hashes away from its pin — "
                   + ", ".join(integrity_failures))
    gates.append({"gate": "0.3", "result": "PASS",
                  "detail": "the crosswalk (4ace1a61...), Registry "
                            "v1 (8a0b2a82...) and the anchors "
                            "(df0cf620...) recompute to their "
                            "section 3 pins; the anchors assertion "
                            "is repeated after the run in this "
                            "record"})

    # ── Populations (section 3 construction) ──────────────────
    primary_rows = [r for r in corpus
                    if grade_of[r["id"]] == GRADE_DOCUMENTED]
    sc_rows = [r for r in corpus
               if grade_of[r["id"]] in (GRADE_DOCUMENTED,
                                        GRADE_CORROBORATED)]
    primary_seqs = sequences_of([r["symbols"] for r in primary_rows])
    sc_seqs = sequences_of([r["symbols"] for r in sc_rows])
    distinct_signs = sorted({s for seq in primary_seqs for s in seq})
    signs_ge2 = sorted({s for seq in primary_seqs if len(seq) >= 2
                        for s in seq})

    # ── Gate 0.4: population reproduction ─────────────────────
    observed_figures = {
        "analyzable_rows": len(primary_seqs),
        "distinct_signs": len(distinct_signs),
        "signs_in_sequences_ge2": len(signs_ge2),
    }
    if observed_figures != POPULATION_FIGURES:
        detail = (
            f"observed {observed_figures} against the frozen "
            f"{POPULATION_FIGURES}")
        gates.append({"gate": "0.4", "result": "FAIL",
                      "detail": detail})
        return close("POPULATION NOT REPRODUCED", detail=detail)

    # ── Gate 0.4: keying (DD-075-5), token 999 excepted ──────
    leg1, leg2 = keying_maps()
    keyed: dict[str, str] = {}
    keying_legs: dict[str, str] = {}
    unkeyable = []
    for code in distinct_signs:
        if code == "999":
            continue
        sign_key, leg, reason = key_sign(code, leg1, leg2)
        if sign_key is None or sign_key not in asset:
            unkeyable.append({
                "sign": code,
                "reason": reason or (
                    "resolved key carries no Asset A v2 row"),
            })
        else:
            keyed[code] = sign_key
            keying_legs[code] = leg
    token_999 = {
        "primary_rows": sum(
            1 for r in primary_rows if "999" in r["symbols"]),
        "occurrences": sum(
            r["symbols"].count("999") for r in primary_rows),
    }
    if unkeyable:
        gates.append({"gate": "0.4", "result": "CLOSE",
                      "detail": f"{len(unkeyable)} unkeyable "
                                "sign(s) under the two-leg route; "
                                "DD-075-5 closure"})
        return close(
            "POPULATION NOT KEYED",
            unkeyable_signs=unkeyable,
            detail=f"{len(distinct_signs)} signs enumerated, "
                   f"{len(unkeyable)} unkeyable, named in this "
                   "record")
    kinds_of = {code: asset[key]["depicted_kind"]
                for code, key in keyed.items()}
    keying_publication = {
        "sign_to_sign_key": keyed,
        "sign_to_leg": keying_legs,
        "token_999_named_exclusion": token_999,
    }
    results["keying_publication_sha256"] = canon_sha(keying_publication)
    results["keyed_population"] = [
        {"sign": code, "sign_key": keyed[code],
         "keying_leg": keying_legs[code],
         "depicted_kind": kinds_of[code],
         "depicted_label_verbatim":
             asset[keyed[code]]["depicted_label_verbatim"]}
        for code in sorted(keyed)
    ]
    gates.append({"gate": "0.4", "result": "PASS",
                  "detail": "the primary population reproduces "
                            "section 3 exactly (3,045 analyzable "
                            "rows, 557 distinct signs, 550 in "
                            "sequences of length >= 2 — a "
                            "replay/drift gate over quantities "
                            "verified at the freeze, as the spec "
                            "flags); every sign keys to exactly "
                            "one Asset A v2 row under the two-leg "
                            "route (DD-075-5); token 999 stands "
                            "as the named exclusion "
                            f"({token_999['primary_rows']} primary "
                            f"rows, {token_999['occurrences']} "
                            "occurrences), counted, never keyed "
                            "or classed"})

    # ── Gate 0.5: the census, before any kind rate ────────────
    totals_p, finals_p = sign_counts(primary_seqs)
    census_classes = {}
    for kind in IDENTIFIED_KINDS:
        members = [s for s in totals_p if kinds_of.get(s) == kind]
        census_classes[kind] = {
            "member_signs": len(members),
            "pooled_occurrences": sum(totals_p[s] for s in members),
        }
    unidentified_signs = [
        s for s in totals_p if kinds_of.get(s) == "unidentified"]
    total_occ_all = sum(totals_p.values())
    total_final_all = sum(finals_p.values())
    borderline_members = sorted(
        s for s in totals_p
        if kinds_of.get(s) in IDENTIFIED_KINDS
        and asset[keyed[s]]["dispute_status"] == "borderline")
    census = {
        "population": dict(POPULATION_FIGURES),
        "classes": census_classes,
        "unidentified": {
            "signs": len(unidentified_signs),
            "pooled_occurrences": sum(
                totals_p[s] for s in unidentified_signs),
        },
        "token_999": token_999,
        "corpus_wide_final_position_rate": {
            "final_occurrences": total_final_all,
            "total_occurrences": total_occ_all,
            "rate": total_final_all / total_occ_all,
        },
        "floors": {
            kind: {
                "sign_floor": FLOOR_SIGNS,
                "occurrence_floor": FLOOR_OCCURRENCES,
                "member_signs": census_classes[kind]["member_signs"],
                "pooled_occurrences":
                    census_classes[kind]["pooled_occurrences"],
                "too_thin": (
                    census_classes[kind]["member_signs"] < FLOOR_SIGNS
                    or census_classes[kind]["pooled_occurrences"]
                    < FLOOR_OCCURRENCES),
            } for kind in IDENTIFIED_KINDS
        },
        "borderline_signs_named_for_S1": [
            {"sign": s, "sign_key": keyed[s],
             "depicted_kind": kinds_of[s]}
            for s in borderline_members
        ],
    }
    results["census"] = census
    thin = [k for k in IDENTIFIED_KINDS if census["floors"][k]["too_thin"]]
    gates.append({"gate": "0.5", "result": "PASS",
                  "detail": "the census is published in this "
                            "record before any kind rate exists: "
                            + "; ".join(
                                f"{k} {census_classes[k]['member_signs']} "
                                f"signs / {census_classes[k]['pooled_occurrences']} "
                                "occurrences" for k in IDENTIFIED_KINDS)
                            + f"; unidentified {len(unidentified_signs)} "
                            f"signs; token 999 {token_999['occurrences']} "
                            "occurrences; the floors of section 4.5 "
                            "applied to the census"
                            + (f"; TOO THIN at the census: {', '.join(thin)}"
                               if thin else "; no kind is TOO THIN")})

    # ── Gate 0.6: freeze-order proof (external records) ──────
    proof_failures = []
    digest_reading = None
    try:
        digest_reading = recompute_freeze_digest()
    except Exception as exc:  # noqa: BLE001
        proof_failures.append(
            f"freeze digest recomputation raised {type(exc).__name__}")
    freeze_json_digest = json.loads(
        SPEC075_FREEZE_JSON.read_text(encoding="utf-8"))["digest"]
    if digest_reading != SPEC075_FREEZE_DIGEST \
            or freeze_json_digest != SPEC075_FREEZE_DIGEST:
        proof_failures.append(
            "the recomputed freeze digest "
            f"({digest_reading}) or freeze.json's digest "
            f"({freeze_json_digest}) differs from the frozen "
            f"digest {SPEC075_FREEZE_DIGEST}")
    pr_state, pr_err = read_freeze_pr_state()
    if pr_err or pr_state is None \
            or pr_state["state"] != "closed" \
            or not pr_state["merged_at"] \
            or not pr_state["merge_commit_sha"].startswith(
                FREEZE_MERGE_COMMIT):
        proof_failures.append(
            "the freeze PR's merge state read from the repo "
            f"record is not merged at {FREEZE_MERGE_COMMIT} "
            f"(reading: {pr_state or pr_err})")
    osf_state, osf_err = read_osf_state()
    if osf_err or osf_state is None \
            or osf_state["public"] is not True \
            or osf_state["pending_registration_approval"] is not False \
            or osf_state["reviews_state"] != "accepted":
        proof_failures.append(
            "the OSF registration jv74f does not read as "
            "approved and public from the OSF record "
            f"(reading: {osf_state or osf_err})")
    results["gate_0_6_readings"] = {
        "freeze_digest_recomputed": digest_reading,
        "freeze_pr": pr_state or {"error": pr_err},
        "osf_registration": osf_state or {"error": osf_err},
    }
    if proof_failures:
        gates.append({"gate": "0.6", "result": "FAIL",
                      "detail": "; ".join(proof_failures)})
        return close("INVALID",
                     detail="gate 0.6 (freeze-order proof): "
                            + "; ".join(proof_failures))
    gates.append({"gate": "0.6", "result": "PASS",
                  "detail": "the freeze digest recomputes from "
                            "the frozen sources to aa06726f...; "
                            "the freeze PR #389 reads merged at "
                            "fd9bd448 from the repo record; OSF "
                            "registration jv74f reads approved "
                            "and public from the OSF record "
                            "(reviews_state accepted, DOI "
                            "10.17605/OSF.IO/JV74F) — each cited "
                            "to its external record"})

    # ── The battery (section 5), only past a clean step 0 ────
    primary_arm = run_arm(
        primary_seqs, kinds_of, keyed, asset, removed_signs=set())
    primary_arm["population"] = (
        "primary (documented-lineage rows only)")

    # S1: borderline removed.
    s1_removed = set(borderline_members)
    s1_arm = run_arm(
        primary_seqs, kinds_of, keyed, asset, removed_signs=s1_removed)
    s1_arm["population"] = (
        "primary, borderline members removed (S1)")
    s1_arm["removed_signs_named"] = census[
        "borderline_signs_named_for_S1"]

    # S2: contested included under CISI-governed labels. Asset
    # A v2 carries zero contested rows (gate 0.1), so the
    # inclusion set is empty and the arm runs on the primary
    # universe; the machinery is stated so any contested row
    # would enter under its governing (depicted) kind.
    contested_rows = [
        row for row in asset_rows
        if row["dispute_status"] == "contested"]
    s2_inclusions = [
        {"sign_key": row["sign_key"],
         "depicted_kind": row["depicted_kind"],
         "governing_source": row["governing_source"],
         "depicted_label_verbatim": row["depicted_label_verbatim"]}
        for row in contested_rows]
    s2_arm = run_arm(
        primary_seqs, kinds_of, keyed, asset, removed_signs=set())
    s2_arm["population"] = (
        "primary, contested included under CISI-governed "
        "labels (S2)")
    s2_arm["included_signs_named"] = s2_inclusions
    s2_arm["equals_primary"] = all(
        s2_arm["kinds"][k]["verdict"] == primary_arm["kinds"][k]["verdict"]
        and s2_arm["kinds"][k].get("table_2x2")
        == primary_arm["kinds"][k].get("table_2x2")
        for k in IDENTIFIED_KINDS)

    # S3: documented + corroborated population, recomputed.
    s3_keyed = dict(keyed)
    s3_unkeyable = []
    s3_codes = sorted({s for seq in sc_seqs for s in seq})
    for code in s3_codes:
        if code == "999" or code in s3_keyed:
            continue
        sign_key, leg, reason = key_sign(code, leg1, leg2)
        if sign_key is None or sign_key not in asset:
            s3_unkeyable.append({"sign": code, "reason": reason})
        else:
            s3_keyed[code] = sign_key
    s3_kinds_of = {code: asset[key]["depicted_kind"]
                   for code, key in s3_keyed.items()}
    s3_arm = run_arm(sc_seqs, s3_kinds_of, s3_keyed, asset,
                     removed_signs=set())
    s3_arm["population"] = "documented + corroborated (S3)"
    s3_arm["population_figures"] = {
        "analyzable_rows": len(sc_seqs),
        "distinct_signs": len(s3_codes),
    }
    s3_arm["unkeyable_signs_named"] = s3_unkeyable
    token_999_s3 = {
        "rows": sum(1 for r in sc_rows if "999" in r["symbols"]),
        "occurrences": sum(
            r["symbols"].count("999") for r in sc_rows),
    }
    s3_arm["token_999"] = token_999_s3

    results["primary"] = primary_arm
    results["sensitivities"] = {
        "S1": s1_arm, "S2": s2_arm, "S3": s3_arm}
    verdicts = {k: primary_arm["kinds"][k]["verdict"]
                for k in IDENTIFIED_KINDS}
    results["verdicts"] = verdicts
    results["grade_sensitivity"] = {
        k: {
            "primary_verdict": verdicts[k],
            "S3_verdict": s3_arm["kinds"][k]["verdict"],
            "grade_sensitive":
                s3_arm["kinds"][k]["verdict"] != verdicts[k],
        } for k in IDENTIFIED_KINDS}
    results["wordings"] = {
        k: kind_wording(k, primary_arm["kinds"][k])
        for k in IDENTIFIED_KINDS}
    supported_kinds = [k for k in IDENTIFIED_KINDS
                        if verdicts[k] == "SUPPORTED"]
    not_supported_kinds = [k for k in IDENTIFIED_KINDS
                           if verdicts[k] == "NOT SUPPORTED"]
    if supported_kinds:
        c03 = (
            "supported in its per-kind sense: kind(s) "
            + ", ".join(supported_kinds)
            + " returned SUPPORTED under section 5.2's frozen "
            "bands; the family's other words stand beside it in "
            "the outcome record, and no pooled verdict exists")
    elif len(not_supported_kinds) == len(IDENTIFIED_KINDS):
        c03 = (
            "contradicted: no identified kind is enriched at "
            "endings — all four kinds returned NOT SUPPORTED, "
            "the falsifiable shape section 1.2 named in advance")
    else:
        c03 = (
            "in question: no kind returned SUPPORTED and the "
            "family does not speak with one word — "
            + "; ".join(f"{k} {verdicts[k]}" for k in IDENTIFIED_KINDS))
    append_texts = {
        "F075-C03": (
            f"Spec 075 (Phase-441), executed {EXECUTION_DATE} "
            f"under the frozen contract (freeze digest "
            f"{SPEC075_FREEZE_DIGEST}; OSF registration "
            f"{OSF_REGISTRATION}): the hypothesis is {c03}."),
        "F075-C05": (
            f"Spec 075 (Phase-441), executed {EXECUTION_DATE}: "
            "step 0 asserted the frozen state of the repaired "
            "surface before any class was counted — gates "
            "0.1-0.6 all PASS, in order, recorded in "
            "reports/phase441_results.json."),
        "F075-C06": (
            f"Spec 075 (Phase-441), executed {EXECUTION_DATE}: "
            "the primary population was the documented-lineage "
            "rows only and reproduced at gate 0.4 as 3,045 "
            "analyzable rows / 557 distinct signs / 550 in "
            "sequences of length >= 2."),
        "F075-C07": (
            f"Spec 075 (Phase-441), executed {EXECUTION_DATE}: "
            "the census was published at gate 0.5 before any "
            "kind rate existed and the floors of section 4.5 "
            "were applied to it ("
            + ("; ".join(f"{k} TOO THIN" for k in thin)
               if thin else "no kind TOO THIN")
            + ")."),
        "F075-C08": (
            f"Spec 075 (Phase-441), executed {EXECUTION_DATE}: "
            "every enumerated sign keyed to exactly one Asset "
            "A v2 row in Wells space under the two-leg route, "
            "except token 999, the named exclusion "
            f"({token_999['occurrences']} occurrences in "
            f"{token_999['primary_rows']} primary rows), "
            "counted and never classed."),
        "F075-C11": (
            f"Spec 075 (Phase-441), executed {EXECUTION_DATE}: "
            "the verdicts are per kind — "
            + "; ".join(f"{k} {verdicts[k]}"
                        for k in IDENTIFIED_KINDS)
            + " — published together with their per-sign tables; "
            "no pooled depicted-kinds verdict was computed, "
            "stated, or implied."),
    }
    results["claim_family_appends"] = {
        "append_key": f"spec075_outcome_append_{EXECUTION_DATE.replace('-', '_')}",
        "appends": append_texts,
    }
    results["headline_wording"] = (
        "The depicted-kind endings atlas (Phase-441), executed "
        f"{EXECUTION_DATE} under the frozen Spec 075 contract: "
        + "; ".join(f"{k} {verdicts[k]}" for k in IDENTIFIED_KINDS)
        + ". " + FAMILY_STATEMENT)
    return close("PER-KIND VERDICTS")


if __name__ == "__main__":
    raise SystemExit(main())
