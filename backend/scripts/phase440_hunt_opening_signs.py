#!/usr/bin/env python3
"""Phase 440 — Spec 074 execution: are Shakti's opening-strong
signs the animal signs (Spec 070's question, re-asked on the
repaired keying surface)?

Runs the frozen Spec 074 contract (freeze digest
5416a0d331e76fcec720746849969f2e86e9d79f2cc0fa583e1050662ffba36c;
OSF registration cfe7z): the step-0 gates in order, then the one
join and the one exact test of section 4.

Gate order (spec section 5, fail-closed):
  0.1 Repaired-surface assertion. (a) Dependency state: Spec
      073's executed record shows both products frozen
      (registry-v2-freeze.json and asset-a-v2-freeze.json present
      under specs/073-keying-surface-repair/). (b) Digest
      assertion: Registry v2 and the Asset A v2 canonical CSV
      recompute to the digests the freeze quoted verbatim from
      Spec 073's executed record (42ab09fb... / 681e017d...),
      and the freeze record's per-kind counts for Asset A v2
      match the presented file's (animal 30, sky_cycle 0,
      object_goods 22, human 43, other 246, contested 0,
      unidentified 211 — the two zero kinds counted from the
      canonical CSV itself, Spec 073's per-kind map omitting
      both keys). A mismatch closes ASSET PIN MISMATCH.
  0.2 Shakti intake (P-F1 S1/S2): both restricted-local files
      hash to their pins; the census reproduces (5,704 rows;
      5,536 analyzable; grades 3,212/2,087/405; 4,904 of 5,536
      analyzable rows carrying a CISI identifier, cisi != '-').
  0.3 Input integrity: the section 3 inputs in the tree
      (reports/phase433_results.json — the recorded enumeration
      gate 0.4 runs against — the canonical Registry v1, the
      sign crosswalk of record, the anchors) hash to their
      freeze values, and this spec's own freeze record carries
      the frozen digest. A mismatch stops the run as INVALID.
  0.4 Population enumeration, reproduction, and keying: the
      section 2 battery over the primary population
      (documented-lineage rows only); O (INITIAL_STRONG)
      enumerated in full in Wells space and published (hashed)
      BEFORE any join (gate 0.6's proof); the enumeration
      asserted against Spec 070's recorded enumeration — the
      same 31 signs, each with the same I/M/T counts as
      published in reports/phase433_results.json, and the full
      battery class census equal to Spec 070's recorded census
      (220 signs at the floor: TERMINAL_STRONG 42,
      MEDIAL_STRONG 81, TERMINAL_MODERATE 37,
      INITIAL_MODERATE 6, MIXED 23, INITIAL_STRONG 31). A
      difference closes POPULATION NOT REPRODUCED. Every
      enumerated sign is then keyed to exactly one Asset A v2
      row under the two-leg route of DD-074-8: leg 1 is
      DD-070-9's rule over Registry v2 (a sign's ICIT code is
      its Wells number, resolved through the registry's
      parpola_1982 rows' wells_ids to exactly one Asset A v2
      sign_key); leg 2, for a sign leg 1 cannot resolve,
      consults Registry v2's icit_wells rows — the row whose
      sign_id is the Wells id itself — to the Asset A v2 row
      of that sign_key. Zero or multiple resolutions across
      both legs is unkeyable; an unkeyable sign closes the
      execution as POPULATION NOT KEYED (DD-074-10, DD-070-11
      carried unchanged).
  0.5 Comparison census and coverage: U (total >= 30 under
      the counting rule carried from DD-070-10) enumerated
      with per-sign counts; the S-B unicorn naming scan over
      Asset A v2's verbatim labels; the full battery class
      counts published (gate 0.4's publication); every O and
      U sign shown to carry an Asset A v2 row (else INVALID —
      an absent row is never treated as non-animal by
      default).
  0.6 Freeze-order proof: recorded in the results in order
      (freeze digest; the v2 digests; the population hash;
      the join after).

Battery (spec section 2, carried from Spec 070 verbatim): the
Phase-43 rules applied new to this ICIT corpus — sequences are
the population rows' sign sequences with the gated ICIT-000
placeholder removed (it is not a sign occurrence; the all-000
rows therefore contribute nothing, as the spec states); a
sequence of length >= 2 contributes one I (first), one T
(last) and M for positions between, in the corpus's recorded
order, no reversal. total = I+M+T; floor total >= 5; cascade
TERMINAL_STRONG t>=0.60, INITIAL_STRONG i>=0.55,
MEDIAL_STRONG m>=0.65, TERMINAL_MODERATE t>=0.40,
INITIAL_MODERATE i>=0.40, else MIXED (first match wins).
Threshold-only; no chance-baseline step exists in the battery
or in this script (G5 attestation).

Test (spec section 4): classification is exactly the frozen
Asset A v2's depicted_kind; the animal set is
depicted_kind = animal and nothing else. Contested and
unidentified members are counted, listed, and excluded from
both the numerator and the denominator of the primary (the
five formerly unkeyable signs are classified unidentified in
Asset A v2: they key, and are so counted and listed —
keying is not classification). R1 = animal share of O /
animal share of U over classified members; Fisher exact on
the disjoint 2x2 (O vs U minus O), the one-sided p the
criterion, the two-sided p published. R2 = among U's animal
signs the share in O over the same share for U's non-animal
signs, Fisher exact on the corresponding table. Precedence
(section 4.3): NOT SUPPORTED if R1 <= 1.0 or p >= 0.05;
SUPPORTED if R1 >= 1.5, p < 0.05 and R2 > 1.0; otherwise
INCONCLUSIVE. Sensitivities: S-A contested included under
CISI-governed labels (Asset A v2 carries zero contested
rows, so S-A is expected to equal the primary and is run
and reported as such); S-B unicorn removed, the sign(s)
named at gate 0.5 from the frozen asset's verbatim labels,
or not applicable with that fact stated; S-C the documented
+ corroborated population with classes re-derived, its
verdict computed under the same precedence and any change
reported as grade-sensitive (P-F1 S4).

The corpus and grades files are restricted-local and never
enter the repository; only derived quantities are written,
to reports/phase440_results.json. Counts are over distinct
signs (the test's units are signs, per section 4).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
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

SPEC073_DIR = REPO / "specs/073-keying-surface-repair"
REGISTRY_V2_FREEZE = SPEC073_DIR / "registry-v2" / "registry-v2-freeze.json"
ASSET_V2_FREEZE = SPEC073_DIR / "asset-a-v2" / "asset-a-v2-freeze.json"
ASSET_V2_CSV = SPEC073_DIR / "asset-a-v2" / "depicted-kind-classification.csv"
SPEC073_OUTCOME = SPEC073_DIR / "outcome.md"
REGISTRY_V2 = REPO / "data/crosswalks/canonical_sign_registry_v2.csv"
REGISTRY_V1 = REPO / "data/crosswalks/canonical_sign_registry.csv"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
PHASE433_RESULTS = REPO / "reports/phase433_results.json"
SPEC074_FREEZE = (
    REPO / "specs/074-hunt-opening-signs-repaired-surface/freeze.json"
)
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
RESULTS = REPO / "reports/phase440_results.json"

CLAIM_ID = (
    "without_kings_or_conquests_the_indus_scr_"
    "ce9d98cc_manual_003"
)
SPEC074_FREEZE_DIGEST = (
    "5416a0d331e76fcec720746849969f2e86e9d79f2cc0fa583e1050662ffba36c"
)
SPEC070_FREEZE_DIGEST = (
    "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e"
)
OSF_REGISTRATION = "cfe7z"
EXECUTION_DATE = "2026-10-24"
REGISTRY_V2_SHA256 = (
    "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"
)
ASSET_V2_SHA256 = (
    "681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193"
)
PHASE433_SHA256 = (
    "667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214"
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
    "animal": 30, "sky_cycle": 0, "object_goods": 22, "human": 43,
    "other": 246, "contested": 0, "unidentified": 211,
}
RECORDED_CENSUS = {
    "TERMINAL_STRONG": 42, "MEDIAL_STRONG": 81,
    "TERMINAL_MODERATE": 37, "INITIAL_MODERATE": 6,
    "MIXED": 23, "INITIAL_STRONG": 31,
}
LINEAGE_STATEMENT = (
    "This corpus is an ICIT-lineage corpus. Agreement between "
    "it and the program's earlier ICIT-lineage layer is "
    "consistency within one tradition, not independent "
    "corroboration."
)
HONESTY_FENCE = (
    "This test measures Hunt's claim against a positional "
    "framework measured on the graded ICIT corpus (the Shakti "
    "corpus). It does not test it against the Phase-43 "
    "framework. The recorded Phase-43 quantities — 805/2,267 "
    "and the 40/61/20 strong-sign classes — are never cited "
    "as this spec's basis: not as its population, not as its "
    "reference points, and not as quantities it reproduces "
    "or corrects."
)

GRADE_DOCUMENTED = "documented-lineage"
GRADE_CORROBORATED = "undocumented-corroborated"
GRADE_UNCORROBORATED = "undocumented-uncorroborated"


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


# ── Battery (spec section 2, carried verbatim from Spec 070) ─────

def derive_battery(rows):
    """rows: list of symbol lists. Returns per-sign counts/classes."""
    counts: dict[str, list[int]] = {}
    for symbols in rows:
        signs = [s for s in symbols if s != "000"]
        if len(signs) < 2:
            continue
        for pos, sign in enumerate(signs):
            slot = counts.setdefault(sign, [0, 0, 0])
            if pos == 0:
                slot[0] += 1
            elif pos == len(signs) - 1:
                slot[2] += 1
            else:
                slot[1] += 1
    derived = {}
    for sign, (i, m, t) in counts.items():
        total = i + m + t
        entry = {"I": i, "M": m, "T": t, "total": total, "class": None}
        if total >= 5:
            ir, mr, tr = i / total, m / total, t / total
            if tr >= 0.60:
                entry["class"] = "TERMINAL_STRONG"
            elif ir >= 0.55:
                entry["class"] = "INITIAL_STRONG"
            elif mr >= 0.65:
                entry["class"] = "MEDIAL_STRONG"
            elif tr >= 0.40:
                entry["class"] = "TERMINAL_MODERATE"
            elif ir >= 0.40:
                entry["class"] = "INITIAL_MODERATE"
            else:
                entry["class"] = "MIXED"
        derived[sign] = entry
    return derived


# ── Two-leg keying route (DD-074-8, in the form of F074-C08) ─────

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


def arm_quantities(o_set, u_set, kinds, contested_labels):
    """Compute one arm's quantities over classified members.

    kinds: sign_key -> depicted_kind for keyed signs.
    Returns the full quantity block for the (O, U) pair.
    (Carried verbatim from the Phase-433 instrument.)"""
    def classify(sign_keys):
        animal = [s for s in sign_keys if kinds[s] == "animal"]
        non = [s for s in sign_keys
               if kinds[s] not in ("animal", "contested", "unidentified")]
        contested = [s for s in sign_keys if kinds[s] == "contested"]
        unidentified = [s for s in sign_keys if kinds[s] == "unidentified"]
        return animal, non, contested, unidentified

    o_keys = [k for k in o_set.values()]
    u_keys = [k for k in u_set.values()]
    o_animal, o_non, o_cont, o_unid = classify(o_keys)
    u_animal, u_non, u_cont, u_unid = classify(u_keys)
    o_classified = set(o_animal) | set(o_non)
    # R1 table: O vs U\O (classified members only)
    a = len(o_animal)
    b = len(o_non)
    c = len([s for s in u_animal if s not in o_classified])
    d = len([s for s in u_non if s not in o_classified])
    share_o = a / (a + b) if (a + b) else None
    share_u = (a + c) / (a + b + c + d) if (a + b + c + d) else None
    r1 = (share_o / share_u) if (share_o is not None and share_u) else None
    p1_one, p1_two = fisher_exact([[a, b], [c, d]]) if (a + b + c + d) else (None, None)
    # R2 table: within U, (animal vs non-animal) x (in O vs not in O)
    a2 = len([s for s in u_animal if s in o_classified])
    b2 = len(u_animal) - a2
    c2 = len([s for s in u_non if s in o_classified])
    d2 = len(u_non) - c2
    share_animal_in_o = a2 / (a2 + b2) if (a2 + b2) else None
    share_non_in_o = c2 / (c2 + d2) if (c2 + d2) else None
    r2 = (share_animal_in_o / share_non_in_o) if (
        share_animal_in_o is not None and share_non_in_o) else None
    p2_one, p2_two = fisher_exact([[a2, b2], [c2, d2]]) if (a2 + b2 + c2 + d2) else (None, None)
    # S-A: contested included under CISI-governed labels.
    def classify_sa(sign_keys):
        animal = [s for s in sign_keys
                    if kinds[s] == "animal"
                    or (kinds[s] == "contested"
                        and contested_labels.get(s) == "animal")]
        non = [s for s in sign_keys
               if s not in animal and kinds[s] != "unidentified"]
        return animal, non
    oa, on = classify_sa(o_keys)
    ua, un = classify_sa(u_keys)
    oc = set(oa) | set(on)
    sa = len(oa); sb = len(on)
    sc_ = len([s for s in ua if s not in oc]); sd = len([s for s in un if s not in oc])
    share_o_sa = sa / (sa + sb) if (sa + sb) else None
    share_u_sa = (sa + sc_) / (sa + sb + sc_ + sd) if (sa + sb + sc_ + sd) else None
    r1_sa = (share_o_sa / share_u_sa) if (share_o_sa is not None and share_u_sa) else None
    psa_one, psa_two = fisher_exact([[sa, sb], [sc_, sd]]) if (sa + sb + sc_ + sd) else (None, None)
    return {
        "O_size": len(o_keys), "U_size": len(u_keys),
        "O_animal": a, "O_non_animal": b,
        "O_contested": len(o_cont), "O_unidentified": len(o_unid),
        "U_animal_total": a + c, "U_non_animal_total": b + d,
        "U_contested": len(u_cont), "U_unidentified": len(u_unid),
        "table_R1": [[a, b], [c, d]],
        "animal_share_O": share_o, "animal_share_U": share_u,
        "R1": r1, "p_one_sided": p1_one, "p_two_sided": p1_two,
        "table_R2": [[a2, b2], [c2, d2]],
        "animal_in_O_share_of_U_animals": share_animal_in_o,
        "non_animal_in_O_share_of_U_non_animals": share_non_in_o,
        "R2": r2, "R2_p_one_sided": p2_one, "R2_p_two_sided": p2_two,
        "S_A": {
            "table_R1": [[sa, sb], [sc_, sd]],
            "animal_share_O": share_o_sa, "animal_share_U": share_u_sa,
            "R1": r1_sa, "p_one_sided": psa_one, "p_two_sided": psa_two,
        },
    }


def verdict_of(q):
    """Section 4.3 precedence, carried verbatim."""
    r1, p, r2 = q["R1"], q["p_one_sided"], q["R2"]
    if r1 is None or p is None:
        return "INCONCLUSIVE"
    if r1 <= 1.0 or p >= 0.05:
        return "NOT SUPPORTED"
    if r1 >= 1.5 and p < 0.05 and (r2 is not None and r2 > 1.0):
        return "SUPPORTED"
    return "INCONCLUSIVE"


def _fmt_share(x) -> str:
    return "undefined" if x is None else f"{x:.4f}"


def _fmt_ratio(x) -> str:
    return "undefined" if x is None else f"{x:.4f}"


def _fmt_p(x) -> str:
    return "undefined" if x is None else f"{x:.4g}"


def headline_wording(outcome: str, q, detail: str = "") -> str:
    """The frozen section 4.6 forms, re-pointed to Spec 074 /
    Asset A v2, with the bracketed quantities filled."""
    if outcome == "SUPPORTED":
        return (
            "Measured on the graded ICIT corpus — a positional "
            "framework measured on that corpus, not the Phase-43 "
            f"framework — of the {q['O_size']} opening-strong signs "
            f"Shakti's own battery returns, {q['O_animal']} are animal "
            "signs under the frozen published-identification "
            f"classification (Asset A v2, SHA-256 {ASSET_V2_SHA256}) "
            f"— a share of {_fmt_share(q['animal_share_O'])} against "
            f"the animal share {_fmt_share(q['animal_share_U'])} of "
            f"the {q['U_size']} signs with at least 30 occurrences: "
            f"enrichment ratio {_fmt_ratio(q['R1'])}, exact test "
            f"p = {_fmt_p(q['p_one_sided'])}. The reversed arm agrees "
            f"in direction (ratio {_fmt_ratio(q['R2'])}). The animal "
            "half of Hunt's opening-sign claim is supported in its "
            "re-scoped form: on this corpus, the opening signs are "
            "the animal signs, at well above the base rate. This does "
            "not establish that animal signs marked identity, guild, "
            "or goods — position plus depiction is still not meaning."
        )
    if outcome == "NOT SUPPORTED":
        return (
            "Measured on the graded ICIT corpus, of the "
            f"{q['O_size']} opening-strong signs Shakti's own battery "
            f"returns, {q['O_animal']} are animal signs under the "
            f"frozen classification (Asset A v2, SHA-256 "
            f"{ASSET_V2_SHA256}) — a share of "
            f"{_fmt_share(q['animal_share_O'])} against the animal "
            f"share {_fmt_share(q['animal_share_U'])} of the "
            "comparison inventory: enrichment ratio "
            f"{_fmt_ratio(q['R1'])}, exact test "
            f"p = {_fmt_p(q['p_one_sided'])}. Animal signs appear "
            "among the opening-strong signs at no better than the "
            "base rate. The animal half of the claim "
            f"`{CLAIM_ID}` is not supported in its re-scoped form; "
            "the claim stands on its positional half alone, exactly "
            "as its record is amended to say by the dated append "
            "that carries this outcome."
        )
    if outcome == "INCONCLUSIVE":
        return (
            "Classified under the frozen Asset A v2 (SHA-256 "
            f"{ASSET_V2_SHA256}) and measured on the graded ICIT "
            "corpus, the opening-strong signs are animal at ratio "
            f"{_fmt_ratio(q['R1'])} against the inventory base rate "
            f"(exact test p = {_fmt_p(q['p_one_sided'])}; reversed "
            f"arm ratio {_fmt_ratio(q['R2'])}) — {detail}. The test "
            "does not settle the claim's animal half in its "
            "re-scoped form; the claim stands IN QUESTION with this "
            "attempt on its record, its counts published in full."
        )
    if outcome == "ASSET PIN MISMATCH":
        return (
            "Spec 074 closed at step 0: the repaired surface "
            f"presented at execution hashes to {detail}, which is "
            "not the digest quoted verbatim in this spec's freeze "
            "record from Spec 073's executed record. No join was "
            "performed and no quantity was computed. The claim "
            "stands as recorded."
        )
    if outcome == "ASSET NOT FROZEN":
        return (
            "Spec 074 closed at step 0: the repaired surface is "
            f"not frozen on record — Spec 073's {detail} at this "
            "execution. No join was made and no quantity was "
            "computed. The claim stands as recorded. This is a "
            "dependency closure on Spec 073's executed record, "
            "not a verdict on the claim."
        )
    if outcome == "SHAKTI INTAKE NOT REPRODUCED":
        return (
            "Spec 074 closed at step 0: the Shakti intake did "
            f"not reproduce — {detail}. No positional quantity "
            "was computed and no join was made. The claim stands "
            "as recorded."
        )
    if outcome == "POPULATION NOT REPRODUCED":
        return (
            "Spec 074 closed at step 0: the battery's "
            "enumeration on the primary population does not "
            f"reproduce Spec 070's recorded enumeration — {detail}. "
            "The corpus, grades, and battery are pinned "
            "identically to Spec 070's, so the difference is "
            "non-determinism or input drift, not a new "
            "measurement. No join was performed and no test "
            "quantity was computed. The claim stands as recorded."
        )
    if outcome == "POPULATION NOT KEYED":
        return (
            "Spec 074 closed at step 0: Shakti's opening-strong "
            f"set was enumerated in full ({detail}), and the "
            "signs that could not be keyed to exactly one Asset "
            "A v2 row in Wells space under either leg of the "
            "frozen keying route are listed with their reasons; "
            "under the disposition the freeze stated, the "
            "execution closes here. No join was performed and "
            "no test quantity was computed. The claim stands as "
            "recorded."
        )
    if outcome == "INVALID":
        return (
            "Spec 074 stopped before any test quantity: "
            f"{detail}. No verdict is recorded; the claim stands "
            "as recorded."
        )
    raise ValueError(outcome)


def main() -> int:
    gates: list[dict] = []
    results: dict = {
        "phase": 440, "spec": "074",
        "claim_id": CLAIM_ID,
        "contract": {
            "freeze_digest": SPEC074_FREEZE_DIGEST,
            "osf_registration": OSF_REGISTRATION,
            "spec070_freeze_digest": SPEC070_FREEZE_DIGEST,
            "asset_a_v2_sha256": ASSET_V2_SHA256,
            "registry_v2_sha256": REGISTRY_V2_SHA256,
            "phase433_results_sha256": PHASE433_SHA256,
        },
        "execution_order": [
            "freeze (Spec 074, digest quoted; OSF cfe7z approved and public)",
            "gate 0.1 repaired-surface assertion (Spec 073's executed record)",
            "gate 0.2 intake assertion (P-F1 S1/S2)",
            "gate 0.3 input integrity",
            "gate 0.4 population enumerated + published (hash) BEFORE any join; "
            "reproduction asserted against Spec 070's recorded enumeration; "
            "keying under the two-leg route (DD-074-8)",
            "gate 0.5 comparison census + coverage",
            "gate 0.6 freeze-order proof (this record's order)",
            "join + test (section 4)",
        ],
        "honesty_fence": HONESTY_FENCE,
        "lineage_statement_PF1_S3": LINEAGE_STATEMENT,
        "g5_attestation": (
            "The Phase-43 battery applied here is threshold-only: it "
            "contains no chance-baseline step - no permutation, shuffle, "
            "or expected-rate baseline - and none is restored or "
            "claimed. The inventory-share comparison of section 4 is "
            "this design's own test construction, not a Phase-43 element."
        ),
    }

    def close(outcome: str, **extra):
        results["outcome"] = outcome
        results["gates"] = gates
        results.update(extra)
        if "headline_wording" not in results:
            results["headline_wording"] = headline_wording(
                outcome, extra.get("primary") or {}, extra.get("detail", ""))
        results["outcome_append_text"] = (
            f"Spec 074 (Phase-440), executed {EXECUTION_DATE} "
            f"under the frozen contract (freeze digest "
            f"{SPEC074_FREEZE_DIGEST}; OSF registration "
            f"{OSF_REGISTRATION}): " + results["headline_wording"])
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

    # ── Gate 0.1: repaired surface (Spec 073's executed record) ──
    missing = [
        name for name, path in (
            ("registry-v2-freeze.json", REGISTRY_V2_FREEZE),
            ("asset-a-v2-freeze.json", ASSET_V2_FREEZE),
        ) if not path.exists()
    ]
    if missing or not SPEC073_OUTCOME.exists():
        detail = (
            f"{missing[0]} does not exist" if missing
            else "outcome.md does not exist"
        )
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": f"Spec 073 freeze record(s) absent: {detail}"})
        return close("ASSET NOT FROZEN", detail=detail)
    registry_freeze = json.loads(REGISTRY_V2_FREEZE.read_text(encoding="utf-8"))
    asset_freeze = json.loads(ASSET_V2_FREEZE.read_text(encoding="utf-8"))
    observed_registry_sha = sha256(REGISTRY_V2)
    observed_asset_sha = sha256(ASSET_V2_CSV)
    if (
        observed_registry_sha != REGISTRY_V2_SHA256
        or registry_freeze.get("sha256") != REGISTRY_V2_SHA256
    ):
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": f"Registry v2 digest {observed_registry_sha}"})
        return close("ASSET PIN MISMATCH", detail=observed_registry_sha)
    if (
        observed_asset_sha != ASSET_V2_SHA256
        or asset_freeze.get("sha256") != ASSET_V2_SHA256
    ):
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": f"Asset A v2 digest {observed_asset_sha}"})
        return close("ASSET PIN MISMATCH", detail=observed_asset_sha)
    with ASSET_V2_CSV.open(newline="", encoding="utf-8") as handle:
        asset_rows = list(csv.DictReader(handle))
    kinds: dict[str, str] = {}
    labels: dict[str, str] = {}
    contested_labels: dict[str, str] = {}
    per_kind: dict[str, int] = {}
    for row in asset_rows:
        kinds[row["sign_key"]] = row["depicted_kind"]
        labels[row["sign_key"]] = row["depicted_label_verbatim"]
        per_kind[row["depicted_kind"]] = per_kind.get(row["depicted_kind"], 0) + 1
    presented_counts = {
        kind: per_kind.get(kind, 0)
        for kind in ("animal", "sky_cycle", "object_goods", "human",
                     "other", "unidentified")
    }
    presented_counts["contested"] = sum(
        1 for row in asset_rows
        if row["dispute_status"] == "contested"
        or row["depicted_kind"] == "contested"
    )
    if presented_counts != ASSET_V2_PER_KIND:
        gates.append({"gate": "0.1", "result": "FAIL",
                      "detail": "Asset A v2 per-kind counts differ from "
                                f"the freeze record: {presented_counts}"})
        return close("ASSET PIN MISMATCH", detail=observed_asset_sha)
    gates.append({"gate": "0.1", "result": "PASS",
                  "detail": "Spec 073's executed record shows both products "
                            "frozen; Registry v2 recomputes to 42ab09fb... "
                            "and Asset A v2 to 681e017d...; Asset A v2 "
                            "per-kind counts match the freeze record "
                            "(animal 30, sky_cycle 0, object_goods 22, "
                            "human 43, other 246, contested 0, "
                            "unidentified 211)"})

    # ── Gate 0.2: Shakti intake, P-F1 S1/S2 ─────────────────────
    if sha256(CORPUS_FILE) != CORPUS_SHA256 or sha256(GRADES_FILE) != GRADES_SHA256:
        gates.append({"gate": "0.2", "result": "FAIL", "detail": "S1 hash mismatch"})
        return close("SHAKTI INTAKE NOT REPRODUCED",
                     detail="the S1 identity failure: a restricted-local "
                            "file's SHA-256 does not recompute to the "
                            "intake record's pin")
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    with GRADES_FILE.open(newline="", encoding="utf-8") as handle:
        grades_rows = list(csv.DictReader(handle))
    grade_of = {g["shakti_id"]: g["grade"] for g in grades_rows}
    grade_counts = {}
    for g in grade_of.values():
        grade_counts[g] = grade_counts.get(g, 0) + 1
    analyzable = [r for r in corpus if not all(s == "000" for s in r["symbols"])]
    cisi_carrying = sum(1 for r in analyzable if r["cisi"] != "-")
    census_ok = (
        len(corpus) == 5704 and len(analyzable) == 5536
        and grade_counts.get(GRADE_DOCUMENTED) == 3212
        and grade_counts.get(GRADE_CORROBORATED) == 2087
        and grade_counts.get(GRADE_UNCORROBORATED) == 405
        and cisi_carrying == 4904
        and all(r["id"] in grade_of for r in corpus)
    )
    if not census_ok:
        gates.append({"gate": "0.2", "result": "FAIL",
                      "detail": f"S2 census: rows={len(corpus)} analyzable={len(analyzable)} "
                                f"grades={grade_counts} cisi={cisi_carrying}"})
        return close("SHAKTI INTAKE NOT REPRODUCED",
                     detail=f"the S2 census failure: rows={len(corpus)}, "
                            f"analyzable={len(analyzable)}, "
                            f"grade counts={grade_counts}, "
                            f"CISI-carrying={cisi_carrying}")
    gates.append({"gate": "0.2", "result": "PASS",
                  "detail": "S1 hashes recompute; S2 census reproduces "
                            "(5,704 rows; 5,536 analyzable; 3,212/2,087/405; "
                            "4,904 CISI-carrying)"})

    # ── Gate 0.3: input integrity ────────────────────────────────
    spec074_freeze = json.loads(SPEC074_FREEZE.read_text(encoding="utf-8"))
    integrity_failures = []
    if sha256(PHASE433_RESULTS) != PHASE433_SHA256:
        integrity_failures.append("reports/phase433_results.json")
    if sha256(REGISTRY_V1) != REGISTRY_V1_SHA256:
        integrity_failures.append("canonical_sign_registry.csv (v1)")
    if sha256(CROSSWALK) != CROSSWALK_SHA256:
        integrity_failures.append("sign_crosswalk_master.csv")
    if anchors_before != ANCHORS_SHA256:
        integrity_failures.append("INDUS_FINAL_ANCHORS.json")
    if spec074_freeze.get("digest") != SPEC074_FREEZE_DIGEST:
        integrity_failures.append("specs/074 freeze.json digest")
    if integrity_failures:
        gates.append({"gate": "0.3", "result": "FAIL",
                      "detail": "section 3 input hash failure: "
                                + ", ".join(integrity_failures)})
        return close("INVALID",
                     detail="gate 0.3 (input integrity): a section 3 "
                            "input hashes away from its freeze-record "
                            "value — " + ", ".join(integrity_failures))
    gates.append({"gate": "0.3", "result": "PASS",
                  "detail": "the Phase-433 record, Registry v1, the "
                            "crosswalk and the anchors hash to their "
                            "freeze values; this spec's freeze record "
                            "carries digest 5416a0d3..."})

    # ── Populations ──────────────────────────────────────────────
    primary_rows = [r["symbols"] for r in corpus
                    if grade_of[r["id"]] == GRADE_DOCUMENTED]
    sc_rows = [r["symbols"] for r in corpus
               if grade_of[r["id"]] in (GRADE_DOCUMENTED, GRADE_CORROBORATED)]
    results["population_rows"] = {
        "primary_documented": len(primary_rows),
        "sensitivity_sc_documented_plus_corroborated": len(sc_rows),
    }

    derived_primary = derive_battery(primary_rows)
    class_counts: dict[str, int] = {}
    for e in derived_primary.values():
        if e["class"]:
            class_counts[e["class"]] = class_counts.get(e["class"], 0) + 1
    o_codes = sorted(
        s for s, e in derived_primary.items() if e["class"] == "INITIAL_STRONG"
    )
    population_publication = {
        "population": "primary (documented-lineage rows only)",
        "O_enumeration_wells_space": [
            {"wells_code": code,
             "I": derived_primary[code]["I"], "M": derived_primary[code]["M"],
             "T": derived_primary[code]["T"], "total": derived_primary[code]["total"]}
            for code in o_codes
        ],
        "battery_class_counts_primary": class_counts,
    }
    # Gate 0.4: publish (hash) the population BEFORE any join.
    pop_sha = canon_sha(population_publication)
    results["gate_0_4_population_publication_sha256"] = pop_sha
    results["population"] = population_publication

    # Gate 0.4, reproduction assertion (DD-074-9): the enumerated
    # set and per-sign counts, and the full class census, against
    # Spec 070's recorded measurement in reports/phase433_results.json.
    recorded = json.loads(PHASE433_RESULTS.read_text(encoding="utf-8"))
    recorded_enum = recorded["population"]["O_enumeration_wells_space"]
    recorded_census = recorded["population"]["battery_class_counts_primary"]
    mine_by_code = {
        e["wells_code"]: e for e in population_publication["O_enumeration_wells_space"]
    }
    recorded_by_code = {e["wells_code"]: e for e in recorded_enum}
    differing_signs = []
    for code in sorted(set(mine_by_code) | set(recorded_by_code)):
        mine, rec = mine_by_code.get(code), recorded_by_code.get(code)
        if mine != rec:
            differing_signs.append(
                {"wells_code": code, "executed": mine, "recorded": rec})
    differing_cells = {
        cls: {"executed": class_counts.get(cls, 0),
              "recorded": recorded_census.get(cls, 0)}
        for cls in sorted(set(class_counts) | set(recorded_census))
        if class_counts.get(cls, 0) != recorded_census.get(cls, 0)
    }
    reproduction = {
        "recorded_publication_sha256":
            recorded["gate_0_4_population_publication_sha256"],
        "executed_publication_sha256": pop_sha,
        "enumeration_equal": not differing_signs,
        "census_equal": not differing_cells,
        "differing_signs": differing_signs,
        "differing_census_cells": differing_cells,
    }
    results["gate_0_4_reproduction"] = reproduction
    if differing_signs or differing_cells:
        gates.append({"gate": "0.4", "result": "CLOSE",
                      "detail": "enumeration or census differs from Spec "
                                "070's recorded measurement (DD-074-9)"})
        parts = []
        if differing_signs:
            parts.append(
                "differing signs: " + ", ".join(
                    f"{d['wells_code']} (executed {d['executed']}, "
                    f"recorded {d['recorded']})" for d in differing_signs))
        if differing_cells:
            parts.append(
                "differing census cells: " + ", ".join(
                    f"{cls} executed {v['executed']} vs recorded "
                    f"{v['recorded']}" for cls, v in differing_cells.items()))
        return close("POPULATION NOT REPRODUCED", detail="; ".join(parts))

    # Gate 0.4, keying (DD-074-8, two legs).
    leg1, leg2 = keying_maps()
    o_keyed: dict[str, str] = {}
    o_legs: dict[str, str] = {}
    unkeyable = []
    for code in o_codes:
        sign_key, leg, reason = key_sign(code, leg1, leg2)
        if sign_key is None:
            unkeyable.append({"wells_code": code, "reason": reason})
        else:
            o_keyed[code] = sign_key
            o_legs[code] = leg
    if unkeyable:
        gates.append({"gate": "0.4", "result": "CLOSE",
                      "detail": f"{len(unkeyable)} unkeyable O sign(s); "
                                "DD-074-10 closure (DD-070-11 carried)"})
        return close("POPULATION NOT KEYED",
                     unkeyable_O_signs=unkeyable,
                     O_size=len(o_codes),
                     detail=f"{len(o_codes)} signs, published with this "
                            "closure in the machine record")
    gates.append({"gate": "0.4", "result": "PASS",
                  "detail": f"O enumerated in Wells space ({len(o_codes)} "
                            f"signs), publication sha {pop_sha[:16]}...; "
                            "the enumeration and the class census "
                            "reproduce Spec 070's recorded measurement "
                            "exactly (31 signs, per-sign I/M/T; census "
                            "220 at the floor); every sign keyed to "
                            "exactly one Asset A v2 row under the "
                            "two-leg route (DD-074-8)"})
    results["keyed_population"] = [
        {"wells_code": code, "sign_key": o_keyed[code],
         "keying_leg": o_legs[code],
         "depicted_kind": kinds.get(o_keyed[code]),
         "depicted_label_verbatim": labels.get(o_keyed[code])}
        for code in o_codes
    ]

    # ── Gate 0.5: census + coverage ──────────────────────────────
    u_codes = sorted(
        s for s, e in derived_primary.items() if e["total"] >= 30
    )
    u_keyed: dict[str, str] = {}
    missing_rows = []
    for code in u_codes:
        sign_key, leg, reason = key_sign(code, leg1, leg2)
        if sign_key is None or sign_key not in kinds:
            missing_rows.append(
                {"wells_code": code,
                 "reason": reason or "resolved key carries no Asset A v2 row"})
        else:
            u_keyed[code] = sign_key
    for code, sign_key in o_keyed.items():
        if sign_key not in kinds:
            missing_rows.append(
                {"wells_code": code, "reason": "no Asset A v2 row"})
    unicorn_signs = sorted(
        k for k, lab in labels.items() if "unicorn" in lab.lower()
    )
    results["gate_0_5"] = {
        "U_enumeration": [
            {"wells_code": code, "sign_key": u_keyed.get(code),
             "total": derived_primary[code]["total"]}
            for code in u_codes
        ],
        "unicorn_signs_named_from_asset_labels": unicorn_signs,
        "S_B": ("applicable" if unicorn_signs else
                "not applicable - no Asset A v2 verbatim label "
                "identifies a unicorn"),
    }
    if missing_rows:
        gates.append({"gate": "0.5", "result": "FAIL",
                      "detail": f"{len(missing_rows)} population sign(s) "
                                "without an Asset A v2 row"})
        return close("INVALID",
                     population_signs_without_asset_row=missing_rows,
                     detail="gate 0.5 (comparison census and coverage): "
                            f"{len(missing_rows)} population sign(s) "
                            "carry no Asset A v2 row — an absent row is "
                            "never treated as non-animal by default")
    gates.append({"gate": "0.5", "result": "PASS",
                  "detail": f"U enumerated ({len(u_codes)} signs, total "
                            ">= 30 under DD-070-10's counting rule); "
                            "every O and U sign carries an Asset A v2 "
                            "row; S-B unicorn naming: "
                            f"{unicorn_signs or 'none - not applicable'}"})
    gates.append({"gate": "0.6", "result": "PASS",
                  "detail": "order recorded in this file: the freeze "
                            "quoted the v2 digests from Spec 073's "
                            "executed record and the recorded "
                            "enumeration from Spec 070's; the "
                            "population was hashed at gate 0.4 before "
                            "the join below was computed"})

    # ── Per-sign classification tables (section 6, item 6) ───────
    results["classification_table_O"] = results["keyed_population"]
    results["classification_table_U"] = [
        {"wells_code": code, "sign_key": u_keyed[code],
         "depicted_kind": kinds[u_keyed[code]],
         "depicted_label_verbatim": labels[u_keyed[code]]}
        for code in u_codes
    ]

    # ── The join + test (only now) ───────────────────────────────
    o_map = {code: o_keyed[code] for code in o_codes}
    u_map = {code: u_keyed[code] for code in u_codes}
    primary_q = arm_quantities(o_map, u_map, kinds, contested_labels)
    outcome = verdict_of(primary_q)

    # S-B: remove unicorn-keyed signs (none on this asset).
    sb_q = None
    if unicorn_signs:
        o_sb = {c: k for c, k in o_map.items() if k not in unicorn_signs}
        u_sb = {c: k for c, k in u_map.items() if k not in unicorn_signs}
        sb_q = arm_quantities(o_sb, u_sb, kinds, contested_labels)

    # S-C: re-derive on documented + corroborated.
    derived_sc = derive_battery(sc_rows)
    o_sc_codes = sorted(
        s for s, e in derived_sc.items() if e["class"] == "INITIAL_STRONG"
    )
    u_sc_codes = sorted(
        s for s, e in derived_sc.items() if e["total"] >= 30
    )
    o_sc_map, u_sc_map, sc_unkeyable = {}, {}, []
    for code in o_sc_codes + [c for c in u_sc_codes if c not in o_sc_codes]:
        sign_key, leg, reason = key_sign(code, leg1, leg2)
        if sign_key is None or sign_key not in kinds:
            sc_unkeyable.append({"wells_code": code, "reason": reason})
        elif code in o_sc_codes:
            o_sc_map[code] = sign_key
        if sign_key is not None and sign_key in kinds and code in u_sc_codes:
            u_sc_map[code] = sign_key
    sc_q = arm_quantities(o_sc_map, u_sc_map, kinds, contested_labels)
    sc_verdict = verdict_of(sc_q)

    results["join_sha256"] = canon_sha(
        {"O": o_map, "U": u_map, "primary": primary_q}
    )
    results["primary"] = primary_q
    results["S_B_quantities"] = sb_q
    results["S_C"] = {
        "O_size": len(o_sc_codes), "U_size": len(u_sc_codes),
        "unkeyable_signs_named": sc_unkeyable,
        "quantities": sc_q,
        "verdict_under_same_precedence": sc_verdict,
        "grade_sensitive": sc_verdict != outcome,
    }

    # The headline wording, in the frozen section 4.6 form.
    detail = ""
    if outcome == "INCONCLUSIVE":
        r1, p, r2 = primary_q["R1"], primary_q["p_one_sided"], primary_q["R2"]
        if primary_q["U_animal_total"] == 0 or r1 is None:
            detail = ("the baseline is empty: no animal signs among "
                      "the comparison inventory's classified members, "
                      "so the ratio is undefined and the census is "
                      "the finding")
        elif r1 >= 1.5 and p < 0.05 and (r2 is None or r2 <= 1.0):
            detail = ("the arms disagree: the primary arm clears "
                      "the support threshold but the reversed arm "
                      "does not agree in direction (section 4.3, "
                      "rule 3)")
        else:
            detail = ("the band: the enrichment ratio falls "
                      "between 1.0 and 1.5 with the exact test "
                      "rejecting equality — above the base rate, "
                      "below the design's support threshold "
                      "(section 4.3, rule 3)")
    results["headline_wording"] = headline_wording(outcome, primary_q, detail)
    return close(outcome, primary=primary_q)


if __name__ == "__main__":
    raise SystemExit(main())
