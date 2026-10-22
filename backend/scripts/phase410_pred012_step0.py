#!/usr/bin/env python3
"""Phase-410 — Spec 043 step 0 (PRED-2026-012 at full
population, corrected registry frame; successor to
Spec 038 / Phase-401).

Executes STEP 0 of the frozen Spec 043 contract
(specs/043-pred-2026-007-registry-frame/freeze.md;
freeze digest
8a8a334f13577cbb704fc96e6d4c0451cb1277a3470b90c98b3f86c362475987;
OSF registration vmcra, approved and public before
this run) under the owner's approval of the
runnable-experiments campaign plan AS WRITTEN on
2026-10-21, which orders this member's execution in
Wave 3 (adjudication.md section 7.6). Checks run in
the frozen order, fail-closed:

  0.1 Sources and pins — every source of spec
      section 4 present and hashed to the frozen
      record's pin; the PRED-2026-012 register entry
      located standing as registered (criterion
      verbatim; Outcome PENDING). A missing source
      or a differing hash closes the study as
      CANNOT BE RUN AS WRITTEN.
  0.2 Enumeration, re-derivation, cross-check —
      the registry's icit_function read mechanically
      over all 803 rows; all 803 values re-derived
      from the pinned builder rule (_WELLS_FUNCTIONS,
      first matching key in table order over each
      row's split wells_ids); reconciliation against
      the draft census (ITM = {P056, P324, P378,
      P385}; 12 coded); held-record verification
      (P385, P378 enumerated ITM; P098 not ITM); the
      cross-check read over the whole CGSA analysis
      file with every disagreement recorded
      sign-by-sign (expected in kind: the field is
      uncoded, per Spec 038's execution record).
      Any census, re-derivation, or within-primary
      ambiguity failure closes the study as CANNOT
      BE RUN AS WRITTEN.
  0.3 The provenance gate — evidence set D1-D4
      fixed by the frozen contract. D1 (the pinned
      builder) and D2 (the pinned parser, with its
      test) are read mechanically. D3 (Fuls 2013,
      "Positional Analysis of Indus Signs", the
      taxonomy source the builder cites) and D4
      (Wells' published sign list as carried in
      Wells 2015, "The Archaeology and Epigraphy of
      Indus Writing", whose chapter 2 presents the
      Wells 2011 sign list and whose chapter 3
      defines the ICTM class) are produced from the
      programme's held cleaned texts, pinned here by
      SHA-256 (each hash derived by two independent
      routes at execution: the worktree file and the
      GitHub contents API at the run's base commit,
      identical). Every basis statement the gate
      rests on is quoted with a locator and verified
      against the pinned text by normalised search
      in this script. The three limbs are then
      determined under the freeze standard
      (DD-043-10: a basis counts only if stated in
      words, with a locator; inference from a class
      name, builder glosses, or reputation does not
      count; silence is failure). Any limb failure
      closes the study as PROVENANCE - CANNOT BE RUN
      AS WRITTEN, unscored. The LOG assignments are
      traced through the same evidence set in the
      same form; the trace gates nothing
      (DD-043-12, enumerated-only).
  0.4 Recorded Phase 5 output verification —
      reached ONLY if check 0.3 passes in full.
      This script does not open the recorded
      clustering or characterisation for assignments
      on any other path: on a gate failure the
      scoring files stand byte-hashed at 0.1 for
      integrity and are never parsed. The sanity
      anchor is a Phase 5 lookup and is not run
      before the gate.

Scoring (spec sections 6-7) is implemented below
and runs only behind a full step-0 pass. On a
step-0 closure no share, coverage figure, or
verdict exists.

Outputs (written on every terminal outcome):
  - reports/phase410_results.json (the step-0
    record, hashed before any scoring)
  - reports/phase410_step0_report.md (the step-0
    report)

The script is deterministic: a second run
reproduces both output files byte-identically.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

FREEZE_DIGEST = (
    "8a8a334f13577cbb704fc96e6d4c0451cb1277a3470b90c98b3f86c362475987"
)
FREEZE_MERGE = "a679448d"
SPEC_REG_ID = "vmcra"
EXECUTION_DATE = "2026-10-21"
CLOSURE_SOURCE = "CANNOT BE RUN AS WRITTEN"
CLOSURE_PROVENANCE = "PROVENANCE - CANNOT BE RUN AS WRITTEN"
CRITERION_SHARE = 0.70
COVERAGE_FLOOR = 0.80

# Frozen pins (spec section 4, check 0.1; freeze
# record; adjudication.md section 7.7).
PIN_REGISTER = (
    "docs/PREDICTION_REGISTER.md",
    "254ccf039cf04cf2882e04c8658381cc05573163651ed5d478697058aa424984",
)
PIN_PRIMARY = (
    "data/crosswalks/canonical_sign_registry.csv",
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
)
PIN_CROSSCHECK = (
    "reports/indus_cgsa_cluster_analysis.json",
    "8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3",
)
PIN_BUILDER = (
    "scripts/cgsa_pipeline.py",
    "4af822f1ad5c924defed7852df967f8633899b27a27fdaea84e2cdad8744efb0",
)
PIN_PARSER = (
    "backend/glossa_lab/data/fuls_parser.py",
    "9b57f0ecc10905c0746f1e7fb8e0622ac18e3b08e62bb2eb34fbec4bbd8ef615",
)
PIN_SIGN_CLUSTERS = (
    "outputs/analysis/sign_clusters.json",
    "623a787dd9cc93c4d3d36377890c4753e3427f57cf7ad70adcd6e8256ba1394a",
)
PIN_CHARACTERIZATION = (
    "reports/cluster_characterization.md",
    "54ebf660873fd853a64ce91c7e30d8c4cedc5bc3a0a1555db1f6281a52e3c476",
)
# Execution-produced evidence documents (check 0.3).
# Held cleaned texts of the two published sources;
# hashes derived two-route at this execution (see
# the outcome record).
PIN_D3 = (
    "glossa-indus/processed/cleaned_text/"
    "positional_analysis_of_indus_signs_a2bedc93.txt",
    "9ed24098c006fcde5bb0ca7be6a6fa188011c3bc7bb8db46796abc77961a0708",
)
PIN_D4 = (
    "glossa-indus/processed/cleaned_text/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt",
    "62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e",
)
PIN_PARSER_TEST = (
    "backend/tests/test_fuls_parser.py",
    "705b29b001eede68b7764d4c3559fbb9eb2ccb3c4b1083e5c8ecee7420b5fe70",
)

DRAFT_CENSUS = {
    "rows": 803, "uncoded": 791, "coded": 12,
    "ITM": ["P056", "P324", "P378", "P385"],
    "LOG": ["P217", "P310"],
    "counts": {"SYL": 1, "ITM": 4, "NUM": 2, "TMK": 2,
               "SHN": 1, "LOG": 2},
}
ANCHOR = {"P385": 21, "P378": 39, "P098": 10}

RESULTS_JSON = REPO / "reports" / "phase410_results.json"
REPORT_MD = REPO / "reports" / "phase410_step0_report.md"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_json(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, indent=1).encode("utf-8")
    ).hexdigest()


def _norm(text: str) -> str:
    """Normalise held cleaned text for quote search:
    join hyphenated line breaks, map ligatures,
    collapse all whitespace."""
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text)


def _pin_record(rel: str, pin: str) -> dict:
    path = REPO / rel
    if not path.exists():
        return {"file": rel, "pin": pin, "observed": None,
                "present": False, "match": False}
    observed = sha256_bytes(path.read_bytes())
    return {"file": rel, "pin": pin, "observed": observed,
            "present": True, "match": observed == pin}


# ── Check 0.1 ──────────────────────────────────────

def check_0_1() -> tuple[dict, dict]:
    rec: dict = {}
    ctx: dict = {}
    problems: list[str] = []
    pins = {}
    for name, (rel, pin) in (
        ("register", PIN_REGISTER),
        ("primary", PIN_PRIMARY),
        ("crosscheck", PIN_CROSSCHECK),
        ("builder", PIN_BUILDER),
        ("parser", PIN_PARSER),
        ("sign_clusters", PIN_SIGN_CLUSTERS),
        ("characterization", PIN_CHARACTERIZATION),
    ):
        r = _pin_record(rel, pin)
        pins[name] = r
        if not r["match"]:
            problems.append(f"{name} missing or hash differs "
                            f"from the frozen pin")
        else:
            ctx[name + "_raw"] = (REPO / rel).read_bytes()
    rec["source_pins"] = pins

    text = ctx.get("register_raw", b"").decode("utf-8")
    if "PRED-2026-012" in text:
        start = text.index("### PRED-2026-012")
        nxt = text.find("\n### ", start + 10)
        entry = text[start:] if nxt < 0 else text[start:nxt]
        rec["entry_located"] = True
        rec["criterion_line_present"] = (
            "≥ 70% of ITM-coded signs are TERMINAL or cluster "
            "in TERMINAL clusters" in entry
        )
        rec["standing_outcome"] = (
            "PENDING" if "**Outcome**: PENDING" in entry else None
        )
        rec["registered_date_present"] = "2026-10-21" in entry
        if not rec["criterion_line_present"] or \
                rec["standing_outcome"] is None:
            problems.append("PRED-2026-012 entry does not stand "
                            "as registered")
    else:
        rec["entry_located"] = False
        problems.append("PRED-2026-012 entry not located in the "
                        "register")
    rec["problems"] = problems
    rec["status"] = "PASS" if not problems else "FAIL"
    return rec, ctx


# ── Check 0.2 ──────────────────────────────────────

def _builder_table(builder_text: str) -> list[tuple[str, str]]:
    """The pinned _WELLS_FUNCTIONS table, in table
    order, parsed from the pinned builder source."""
    m = re.search(r"_WELLS_FUNCTIONS\s*=\s*\{(.*?)\n\}",
                  builder_text, re.S)
    pairs = re.findall(r'"(W\d+)":\s*"([A-Z]+)"', m.group(1))
    return pairs


def check_0_2(ctx: dict) -> tuple[dict, dict | None]:
    primary_text = ctx["primary_raw"].decode("utf-8")
    rdr = csv.DictReader(io.StringIO(primary_text))
    rows = list(rdr)
    rec: dict = {}
    rec["fieldnames_present"] = (
        rdr.fieldnames is not None
        and "icit_function" in rdr.fieldnames
        and "parpola_id" in rdr.fieldnames
        and "wells_ids" in rdr.fieldnames
    )
    rec["rows_read"] = len(rows)

    census = Counter(r["icit_function"] for r in rows)
    coded = {k: v for k, v in census.items() if k}
    rec["census"] = {
        "rows": len(rows),
        "uncoded": census.get("", 0),
        "coded": sum(coded.values()),
        "coded_counts": dict(sorted(coded.items())),
        "coded_signs": {
            code: sorted(r["parpola_id"] for r in rows
                         if r["icit_function"] == code)
            for code in sorted(coded)
        },
    }
    itm = sorted(r["parpola_id"] for r in rows
                 if r["icit_function"] == "ITM")
    enumeration = {
        "rule": "icit_function value in the primary source "
                "(canonical_sign_registry.csv) equals exactly "
                "ITM (spec s.2)",
        "source": PIN_PRIMARY[0],
        "source_sha256": PIN_PRIMARY[1],
        "rows_read": len(rows),
        "itm_signs": itm,
        "population_size": len(itm),
    }
    rec["enumeration"] = enumeration
    rec["enumeration_sha256"] = sha256_json(enumeration)

    # Re-derivation from the pinned builder rule.
    table = _builder_table(ctx["builder_raw"].decode("utf-8"))
    ctx["builder_table"] = table
    mismatches = []
    for r in rows:
        wells = r["wells_ids"].split("|") if r["wells_ids"] else []
        derived = next((v for k, v in table if k in wells), "")
        if derived != r["icit_function"]:
            mismatches.append({
                "parpola_id": r["parpola_id"],
                "recorded": r["icit_function"],
                "derived": derived,
            })
    rec["rederivation"] = {
        "table_keys": [k for k, _ in table],
        "rows_checked": len(rows),
        "mismatches": mismatches,
        "exact_agreement": not mismatches,
    }

    # Within-primary ambiguity: conflicting codes
    # for one sign.
    by_sign: dict[str, set] = {}
    for r in rows:
        if r["parpola_id"]:
            by_sign.setdefault(r["parpola_id"], set()).add(
                r["icit_function"])
    rec["within_primary_conflicts"] = {
        s: sorted(v) for s, v in by_sign.items() if len(v) > 1
    }

    rec["held_records"] = {
        "P385": {"condition": "enumerated as ITM",
                 "met": "P385" in itm},
        "P378": {"condition": "enumerated as ITM",
                 "met": "P378" in itm},
        "P098": {"condition": "not ITM (carries no code)",
                 "registry_code": next(
                     (r["icit_function"] for r in rows
                      if r["parpola_id"] == "P098"), None),
                 "met": "P098" not in itm},
    }

    # Cross-check over the whole file.
    cg = json.loads(ctx["crosscheck_raw"])
    a_rows = cg["data"]["a"]
    values = Counter(r.get("icit_function", "") for r in a_rows)
    gloss = sum(v for k, v in values.items() if k)
    rec["crosscheck"] = {
        "records_read": len(a_rows),
        "empty_values": values.get("", 0),
        "nonempty_values": gloss,
        "coded_itm_values": values.get("ITM", 0),
        "coded_log_values": values.get("LOG", 0),
        "expectation": "uncoded field: 579 empty, 32 free-text "
                       "glosses, no ITM and no LOG values (Spec "
                       "038 execution record)",
        "expectation_met": (
            values.get("", 0) == 579 and gloss == 32
            and values.get("ITM", 0) == 0
            and values.get("LOG", 0) == 0
        ),
    }
    by_cc: dict[str, dict] = {}
    for r in a_rows:
        by_cc.setdefault(r.get("sign_id"), r)
    disagreements = []
    for r in rows:
        if not r["icit_function"]:
            continue
        sign = r["parpola_id"]
        cc = by_cc.get(sign)
        disagreements.append({
            "sign": sign,
            "registry_code": r["icit_function"],
            "crosscheck": (
                "no record" if cc is None
                else ("empty value" if not cc.get("icit_function")
                      else cc.get("icit_function"))),
            "kind": "expected: the cross-check field is uncoded; "
                    "the primary governs membership (DD-043-1)",
        })
    p098_cc = by_cc.get("P098")
    disagreements.append({
        "sign": "P098",
        "registry_code": rec["held_records"]["P098"]["registry_code"],
        "crosscheck": ("no record" if p098_cc is None else
                        p098_cc.get("icit_function")),
        "kind": "expected: uncoded in both sources; excluded by "
                "the inclusion rule (DD-043-5)",
    })
    rec["crosscheck_disagreements"] = disagreements
    rec["unexplained_discrepancy"] = None

    problems = []
    if len(rows) != DRAFT_CENSUS["rows"]:
        problems.append("row count differs from the draft census")
    if itm != DRAFT_CENSUS["ITM"]:
        problems.append("ITM enumeration differs from the draft "
                        "census")
    if rec["census"]["coded_counts"] != DRAFT_CENSUS["counts"]:
        problems.append("coded census differs from the draft "
                        "census")
    if mismatches:
        problems.append("re-derivation mismatches over the "
                        "registry")
    if rec["within_primary_conflicts"]:
        problems.append("conflicting codes within the primary")
    if not all(h["met"] for h in rec["held_records"].values()):
        problems.append("held-record verification failed")
    rec["problems"] = problems
    rec["status"] = "PASS" if not problems else "FAIL"
    return rec, (enumeration if not problems else None)


# ── Check 0.3: the provenance gate ─────────────────

# Basis statements, quoted from the produced
# documents, with locators. Each quote is verified
# against the pinned held text by normalised
# search at run time; a quote that does not verify
# is recorded as unverified and the gate cannot
# rest on it.
D3_QUOTES = [
    {
        "id": "D3-Q1",
        "locator": "Fuls 2013, s.2 'Methods of Sign Analysis' "
                   "(held cleaned text lines 163-179; journal "
                   "pp. 255-256)",
        "quote": "It is well known that some signs like sign 740 "
                 "are mostly located in the terminal position "
                 "of texts, while others are very often in "
                 "initial position of texts. The preferred sign "
                 "positions gives us some clues about the "
                 "possible sign function assuming a language "
                 "with a fixed syntax. ... The distribution of "
                 "a sign position can be used to evaluate "
                 "possible sign functions. B. Wells classifies "
                 "some signs according to their preferred text "
                 "position as Initial signs (INS), Terminal "
                 "Marker (TMK), and Post-Terminal Marker "
                 "(PTM). He also discovered, that sign 60 "
                 "appears only in position 1 to 4 (except 5 "
                 "two-lined texts), which is often replaced by "
                 "sign 1 or sign 2. They are called Initial "
                 "Cluster Terminal Marker (ICTM).",
        "search": "according to their preferred text "
                  "position as Initial signs (INS), Terminal "
                  "Marker (TMK), and Post-Terminal Marker "
                  "(PTM)",
    },
    {
        "id": "D3-Q2",
        "locator": "Fuls 2013, s.3.7 'Medial Sign Classification' "
                   "(held cleaned text lines 347-356; journal "
                   "p. 264)",
        "quote": "Signs which have a maximum at positions 3 to "
                 "4 are called Early-Medial signs. Sign 2 and "
                 "60 are known as a marker after initial signs "
                 "or initial sign clusters. ... Wells (2006) "
                 "calls them, together with sign 1, Initial "
                 "Cluster Terminal Marker (ICTM), since they "
                 "mark the end of initial clusters.",
        "search": "Initial Cluster Terminal Marker (ICTM), "
                  "since they mark the end of initial clusters",
    },
    {
        "id": "D3-Q3",
        "locator": "Fuls 2013, s.3.1 'Initial signs' (held "
                   "cleaned text lines 270-282; journal "
                   "pp. 260-261)",
        "quote": "Initial signs are known from structural "
                 "analysis and appear very often in first "
                 "position. ... Signs 690, 790, 824, 850, and "
                 "921 are graphically similar to the Initial "
                 "signs 692, 817, 820, 861, and 921, "
                 "respectively. But the positional frequency "
                 "shows, that they locate in different "
                 "positions, not exclusively initial.",
        "search": "graphically similar to the Initial signs "
                  "692, 817, 820, 861, and 921",
    },
    {
        "id": "D3-Q4",
        "locator": "Fuls 2013, s.3.2 'Terminal Markers' (held "
                   "cleaned text lines 298-307; journal "
                   "pp. 261-262)",
        "quote": "Terminal markers are discussed by Wells "
                 "(2006, p. 198-200). They appear often at the "
                 "end of texts. ... Sign 741 is similar to "
                 "sign 740 with a maximum at position 5 but "
                 "not terminal as sign 740.",
        "search": "not terminal as sign 740",
    },
    {
        "id": "D3-Q5",
        "locator": "Fuls 2013, s.4 'Doubled Signs' (held "
                   "cleaned text line 394; journal p. 266)",
        "quote": "sign 820, a typical sign in initial position",
        "search": "sign 820, a typical sign in initial position",
    },
]
D4_QUOTES = [
    {
        "id": "D4-Q1",
        "locator": "Wells 2015, ch. 3 'Initial Clusters' (held "
                   "cleaned text lines 969-972; book p. 26)",
        "quote": "In its simplest form an Initial Cluster "
                 "consists of two signs, an initial sign and an "
                 "ICTM. There are only three ICTMs used in "
                 "Indus texts: Sign 060, Sign 001, Sign 002.",
        "search": "There are only three ICTMs used in Indus "
                  "texts",
    },
    {
        "id": "D4-Q2",
        "locator": "Wells 2015, ch. 3 (held cleaned text lines "
                   "1003-1008; book pp. 26-27)",
        "quote": "In their tersest form initial clusters "
                 "consist of two signs: an initial sign "
                 "followed by an ICTM. ... The possibility "
                 "that ICTMs are grammatical elements seems "
                 "likely (case, mode, tense, gender, clitics "
                 "and post-positions are all possible).",
        "search": "The possibility that ICTMs are grammatical "
                  "elements seems likely",
    },
    {
        "id": "D4-Q3",
        "locator": "Wells 2015, ch. 3 (held cleaned text lines "
                   "1081-1082 and 1137-1139; book pp. 30-32)",
        "quote": "Set 1 initial signs (signs: 817, 861, 820, "
                 "692 and 920; Figure 3.12). They are most "
                 "frequently found in IC and very often are "
                 "the only sign right adjacent to ICTMs. ... "
                 "I will suggest based on Figure 3.15 that "
                 "signs 861, 817, 820, 920, 550 and 692 are "
                 "logographs and signs 390, 031, 220, 368 and "
                 "595 are syllabic signs.",
        "search": "signs 861, 817, 820, 920, 550 and 692 are "
                  "logographs",
    },
    {
        "id": "D4-Q4",
        "locator": "Wells 2015, ch. 3 (held cleaned text line "
                   "1048; book p. 29)",
        "quote": "sign 861, that is most often a single sign "
                 "initial cluster",
        "search": "sign 861, that is most often a single sign "
                  "initial cluster",
    },
    {
        "id": "D4-Q5",
        "locator": "Wells 2015, ch. 6 (held cleaned text lines "
                   "2688-2696; book p. 87)",
        "quote": "What is clear from Figure 6.2 is that sign "
                 "820 occurs terminally in short (Segment) "
                 "texts ... Figure 6.3 Shows sign 820 is a "
                 "terminal marker.",
        "search": "Shows sign 820 is a terminal marker",
    },
    {
        "id": "D4-Q6",
        "locator": "Wells 2015, ch. 2 'The Indus Sign List' "
                   "(held cleaned text lines 658-666; book "
                   "p. 13)",
        "quote": "The sign list used here (Wells 2011) was "
                 "constructed using a uniform method. This "
                 "method begins with signs that have similar "
                 "graphs.",
        "search": "The sign list used here (Wells 2011) was "
                  "constructed using a uniform method",
    },
]
LOG_QUOTES = [
    {
        "id": "LOG-Q1",
        "locator": "Wells 2015, ch. 6 (held cleaned text lines "
                   "2979-2982; book p. 99)",
        "quote": "We know from the structural analysis given "
                 "in Chapter 3 that they are TMs, and the "
                 "values assigned to signs 740 (*-ay) and 032 "
                 "(*-ir) are found in terminal contexts in "
                 "Dravidian languages. ... it seems a logical "
                 "extension of this pattern to assign the "
                 "other common TM (sign 520) to the 3rd "
                 "person non-masculine.",
        "search": "assign the other common TM (sign 520)",
    },
    {
        "id": "LOG-Q2",
        "locator": "Wells 2015, ch. 5 (held cleaned text lines "
                   "2184-2185; book p. 72)",
        "quote": "I have posited in Chapter 4 that these sign "
                 "sequences (Sign 700 + #) are various values "
                 "in the Indus volumetric system.",
        "search": "these sign sequences (Sign 700 + #) are "
                  "various values in the Indus volumetric "
                  "system",
    },
]

PER_SIGN_BASIS = [
    {
        "sign": "P056", "wells_ids": ["W231"],
        "d3": "no statement: sign 231 does not occur in "
              "Fuls 2013 (searched in full at execution)",
        "d4": "no assignment: sign 231 is not assigned ITM "
              "or any function in Wells 2015 (the only "
              "'231' in the text is a token count, 'n = 231', "
              "ch. 5)",
        "basis_stated": None,
        "determination": "FAIL - no checkable stated basis "
                         "(silence is failure, DD-043-10); no "
                         "published list assigns W231 ITM "
                         "(omission where the builder table "
                         "asserts it)",
    },
    {
        "sign": "P324", "wells_ids": ["W740"],
        "d3": "s.2: sign 740 'mostly located in the terminal "
              "position of texts' (D3-Q1); s.3.2: terminal-"
              "marker discussion, 'not terminal as sign 740' "
              "(D3-Q4)",
        "d4": "ch. 6: sign 740 is a TM (terminal marker) "
              "whose assigned value is 'found in terminal "
              "contexts' (LOG-Q1's passage); ch. 3: 740 is "
              "the terminal-cluster counterpart of the "
              "conjunctive signs",
        "basis_stated": "positional: terminal-position "
                        "distribution",
        "determination": "FAIL - the stated basis is "
                         "positional, and the published "
                         "class is terminal marker, not ITM",
    },
    {
        "sign": "P378", "wells_ids": ["W820"],
        "d3": "s.3.1: sign 820 is one of the 'Initial signs "
              "692, 817, 820, 861, and 921' (D3-Q3); s.4: "
              "'a typical sign in initial position' (D3-Q5)",
        "d4": "ch. 3: sign 820 is a Set 1 initial sign and a "
              "suggested logograph (D4-Q3); ch. 6: 'sign 820 "
              "is a terminal marker' (D4-Q5)",
        "basis_stated": "positional: initial-position "
                        "distribution (D3); initial-cluster "
                        "membership and terminal occurrence "
                        "(D4)",
        "determination": "FAIL - the stated bases are "
                         "positional, and the published "
                         "classes (initial sign; logograph; "
                         "terminal marker) are not ITM",
    },
    {
        "sign": "P385", "wells_ids": ["W817", "W861"],
        "d3": "s.3.1: signs 817 and 861 are 'Initial signs' "
              "(D3-Q3)",
        "d4": "ch. 3: signs 817 and 861 are Set 1 initial "
              "signs and suggested logographs (D4-Q3); sign "
              "861 'most often a single sign initial "
              "cluster' (D4-Q4); only signs 861 and 817 pair "
              "with ICTM sign 002 alone - they stand "
              "adjacent to ICTMs, they are not ICTMs "
              "(D4-Q1: the ICTMs are 060, 001, 002)",
        "basis_stated": "positional: initial-cluster "
                        "distribution",
        "determination": "FAIL - the stated bases are "
                         "positional, and the published "
                         "classes (initial signs; logographs) "
                         "are not ITM",
    },
]


def check_0_3(ctx: dict) -> dict:
    rec: dict = {}
    problems: list[str] = []

    # D1 - the pinned builder, read mechanically.
    builder_text = ctx["builder_raw"].decode("utf-8")
    table = ctx.get("builder_table") or _builder_table(
        builder_text)
    glosses = dict(re.findall(
        r'"(W\d+)":\s*"[A-Z]+",\s*#\s*(.+)', builder_text))
    rec["D1_builder"] = {
        "file": PIN_BUILDER[0], "sha256": PIN_BUILDER[1],
        "table_comment": "Known ICIT/Wells sign function "
                         "assignments (from ICIT docs + Fuls "
                         "2013)",
        "table": [{"wells_id": k, "code": v,
                   "gloss": glosses.get(k)} for k, v in table],
        "itm_keys": [k for k, v in table if v == "ITM"],
        "summary_citation": "Fuls 2013 paper: NWSP method "
                            "reference + sign function taxonomy",
    }

    # D2 - the pinned parser, with its test.
    parser_text = ctx["parser_raw"].decode("utf-8")
    fn_vocab = re.search(
        r"for func in \[([^\]]+)\]", parser_text)
    test_text = (REPO / PIN_PARSER_TEST[0]).read_bytes().decode(
        "utf-8")
    rec["D2_parser"] = {
        "file": PIN_PARSER[0], "sha256": PIN_PARSER[1],
        "annotation": "Function classification (from Wells)",
        "function_vocabulary": fn_vocab.group(1) if fn_vocab
                               else None,
        "same_line_reading": "parse_sign_catalog_entry "
                             "extracts, from one catalog line, "
                             "a frequency, a positional "
                             "classification (initial / terminal "
                             "/ medial / post-terminal) and a "
                             "function classification",
        "test_fixture": "Sign 342: frequency 580, terminal, "
                        "TMK",
        "test_fixture_present": "Sign 342" in test_text
                                and "TMK" in test_text,
        "parser_test_pin": _pin_record(*PIN_PARSER_TEST),
    }

    # D3 / D4 - produced from the held cleaned texts.
    produced = {}
    for name, pin in (("D3", PIN_D3), ("D4", PIN_D4)):
        r = _pin_record(*pin)
        produced[name] = r
        if not r["match"]:
            problems.append(f"{name} document cannot be "
                            f"produced at its pinned bytes")
    rec["D3_production"] = {
        **produced["D3"],
        "document": "Fuls, Andreas. 2013. 'Positional Analysis "
                    "of Indus Signs.' Voprosi Epigrafiki "
                    "7(1): 253-275 (the taxonomy source the "
                    "builder cites; CITATIONS.md s.D.9)",
    }
    rec["D4_production"] = {
        **produced["D4"],
        "document": "Wells, Bryan K. 2015. 'The Archaeology "
                    "and Epigraphy of Indus Writing.' "
                    "Archaeopress (ch. 2 presents the Wells "
                    "2011 sign list; ch. 3 defines the ICTM "
                    "class; CITATIONS.md s.A.7)",
    }
    d3_norm = _norm((REPO / PIN_D3[0]).read_bytes().decode(
        "utf-8")) if produced["D3"]["match"] else ""
    d4_norm = _norm((REPO / PIN_D4[0]).read_bytes().decode(
        "utf-8")) if produced["D4"]["match"] else ""

    def verify(quotes, norm):
        out = []
        for q in quotes:
            found = _norm(q["search"]) in norm
            out.append({**q, "verified_in_pinned_text": found})
            if not found:
                problems.append(f"quote {q['id']} does not "
                                f"verify in the pinned text")
        return out

    rec["D3_quotes"] = verify(D3_QUOTES, d3_norm)
    rec["D4_quotes"] = verify(D4_QUOTES, d4_norm)
    rec["per_sign_basis"] = PER_SIGN_BASIS

    rec["limbs"] = {
        "limb_1_class_definition": {
            "requirement": "the produced documents state "
                           "what ITM is, and the stated "
                           "definition is not a positional "
                           "one",
            "finding": "FAIL",
            "evidence": "D3 (D3-Q1, D3-Q2): Wells classifies "
                        "signs 'according to their preferred "
                        "text position', and the ICTM class "
                        "is the signs that 'mark the end of "
                        "initial clusters' - a definition by "
                        "cluster-final behaviour, drawn from "
                        "positional distribution. D4 (D4-Q1): "
                        "the ICTM is defined by its role "
                        "terminating an initial cluster. "
                        "D4-Q2's suggestion that ICTMs may be "
                        "grammatical elements is a hypothesis "
                        "about what the class might mean, "
                        "offered for a class already delimited "
                        "positionally; it is not a stated "
                        "definition of the class and not a "
                        "basis of any assignment, and under "
                        "DD-043-10 it cannot be counted as "
                        "one.",
        },
        "limb_2_per_sign_basis": {
            "requirement": "for each of the four ITM signs, "
                           "the produced documents state a "
                           "position-independent basis",
            "finding": "FAIL",
            "evidence": "every basis the produced documents "
                        "state is positional (terminal-"
                        "position distribution for W740; "
                        "initial-position / initial-cluster "
                        "distribution for W820, W817, W861), "
                        "and for W231 (P056) the produced "
                        "documents state no basis at all - "
                        "silence, which the frozen standard "
                        "fixes as failure. Per-sign record in "
                        "per_sign_basis.",
        },
        "limb_3_source_agreement": {
            "requirement": "where the produced published "
                           "documents list per-sign function "
                           "assignments, they agree with the "
                           "builder table for all four ITM "
                           "signs",
            "finding": "FAIL",
            "evidence": "D4-Q1: the published ICTM class has "
                        "exactly three members - signs 060, "
                        "001, 002 - none of them a builder "
                        "ITM key. D3-Q3 and D4-Q3 assign "
                        "817, 820, 861 as initial signs; "
                        "D4-Q5 assigns 820 as a terminal "
                        "marker; D3-Q1/Q4 and D4 assign 740 "
                        "terminally. W231 is omitted by both "
                        "documents where the table asserts "
                        "ITM. The published lists therefore "
                        "assign different functions to the "
                        "four signs, and omit the fourth - a "
                        "gate failure under the limb's own "
                        "wording.",
        },
    }

    # The LOG trace (same evidence set, same form;
    # gates nothing, DD-043-12).
    log_quotes = verify(LOG_QUOTES, d4_norm)
    rec["log_trace"] = {
        "quotes": log_quotes,
        "assignments": [
            {
                "sign": "P217", "wells_ids": ["W520"],
                "builder": "LOG (no gloss in the table)",
                "d3": "no per-sign statement for sign 520 "
                      "in Fuls 2013",
                "d4": "ch. 6 (LOG-Q1): sign 520 is 'the "
                      "other common TM' - a terminal marker, "
                      "a positional class, not LOG",
                "finding": "the published source assigns a "
                           "different, positional class; "
                           "recorded for the trace only",
            },
            {
                "sign": "P310", "wells_ids": ["W700"],
                "builder": "LOG, glossed 'Logogram (most "
                           "common at Harappa)'",
                "d3": "no per-sign statement for sign 700 "
                      "in Fuls 2013",
                "d4": "ch. 4-5 (LOG-Q2): sign 700 with "
                      "stroke numerals is posited as values "
                      "in the Indus volumetric system; no "
                      "per-sign LOG assignment is stated",
                "finding": "no stated per-sign LOG basis "
                           "in the produced documents; "
                           "recorded for the trace only",
            },
        ],
        "gates": "nothing (DD-043-12: LOG is "
                 "enumerated-only; no LOG quantity is "
                 "scored)",
    }

    limbs_fail = [k for k, v in rec["limbs"].items()
                  if v["finding"] != "PASS"]
    rec["problems"] = problems
    rec["determination"] = (
        "FAIL" if (limbs_fail or problems) else "PASS")
    rec["status"] = "PASS" if rec["determination"] == "PASS" \
        else "FAIL"
    return rec


# ── Check 0.4 + scoring (reached only behind a full
#    step-0 pass) ───────────────────────────────────

def check_0_4(ctx: dict) -> dict:
    rec: dict = {}
    sc = json.loads(ctx["sign_clusters_raw"])
    s2c = sc.get("sign_to_cluster") or {}
    rec["best_k"] = sc.get("best_k")
    rec["assigned_signs"] = len(s2c)
    anchor = {}
    ok = sc.get("best_k") == 40 and len(s2c) == 160
    for sign, cluster in ANCHOR.items():
        got = s2c.get(sign)
        anchor[sign] = {"expected_cluster": cluster,
                        "recorded_cluster": got,
                        "match": got == cluster}
        ok = ok and got == cluster
    rec["sanity_anchor"] = anchor
    rec["status"] = "PASS" if ok else "FAIL"
    ctx["sign_to_cluster"] = s2c
    return rec


def parse_cluster_classes(md_text: str) -> dict[int, str]:
    classes: dict[int, str] = {}
    for m in re.finditer(
            r"^### Cluster (\d+) — ([A-Z/]+) \(", md_text, re.M):
        classes[int(m.group(1))] = m.group(2)
    return classes


def score(ctx: dict, enumeration: dict) -> dict:
    s2c = ctx["sign_to_cluster"]
    classes = parse_cluster_classes(
        ctx["characterization_raw"].decode("utf-8"))
    population = enumeration["itm_signs"]
    table = []
    assigned = 0
    numerator = 0
    unassigned = []
    for sign in population:
        cluster = s2c.get(sign)
        cclass = classes.get(cluster) if cluster is not None \
            else None
        is_assigned = cluster is not None and cclass is not None
        counts = bool(is_assigned
                      and "TERMINAL" in cclass.split("/"))
        if is_assigned:
            assigned += 1
            numerator += 1 if counts else 0
        else:
            unassigned.append(sign)
        table.append({
            "sign": sign, "cluster": cluster,
            "cluster_class": cclass, "assigned": is_assigned,
            "counts_toward_criterion": counts if is_assigned
                                       else None,
        })
    coverage = assigned / len(population) if population else 0.0
    share = numerator / assigned if assigned else None
    decisive = False
    if share is not None and population:
        worst = numerator / len(population)
        best = (numerator + len(unassigned)) / len(population)
        now = share >= CRITERION_SHARE
        decisive = (worst >= CRITERION_SHARE) == now and \
            (best >= CRITERION_SHARE) == now
    partial = bool(share is not None
                   and coverage < COVERAGE_FLOOR and not decisive)
    verdict = None
    if share is not None:
        verdict = "CONFIRMED" if share >= CRITERION_SHARE \
            else "NOT CONFIRMED"
    return {
        "population_size": len(population),
        "assigned": assigned,
        "unassigned_signs": unassigned,
        "numerator_terminal": numerator,
        "share": share, "coverage": coverage,
        "coverage_decisive": decisive,
        "run_at_partial_scope": partial,
        "verdict": verdict,
        "per_sign_table": table,
    }


# ── Main ───────────────────────────────────────────

def main() -> int:
    step0: dict = {}
    c1, ctx = check_0_1()
    step0["check_0_1"] = c1
    closure_check = None
    closure_kind = None
    enumeration = None
    scoring = None

    if c1["status"] != "PASS":
        closure_check, closure_kind = "0.1", CLOSURE_SOURCE
    else:
        c2, enumeration = check_0_2(ctx)
        step0["check_0_2"] = c2
        if c2["status"] != "PASS":
            closure_check, closure_kind = "0.2", CLOSURE_SOURCE
        else:
            c3 = check_0_3(ctx)
            step0["check_0_3"] = c3
            if c3["status"] != "PASS":
                closure_check = "0.3"
                closure_kind = CLOSURE_PROVENANCE
            else:
                c4 = check_0_4(ctx)
                step0["check_0_4"] = c4
                if c4["status"] != "PASS":
                    closure_check = "0.4"
                    closure_kind = CLOSURE_SOURCE
    step0["phase5_output_opened"] = "check_0_4" in step0
    step0["phase5_assignments_looked_up"] = (
        "check_0_4" in step0)

    if closure_check is None:
        scoring = score(ctx, enumeration)
        if scoring["run_at_partial_scope"]:
            outcome = {
                "type": "run_at_partial_scope",
                "verdict": None,
                "share": scoring["share"],
                "coverage": scoring["coverage"],
                "population_size": scoring["population_size"],
            }
        else:
            outcome = {
                "type": "verdict",
                "verdict": scoring["verdict"],
                "share": scoring["share"],
                "coverage": scoring["coverage"],
                "population_size": scoring["population_size"],
            }
    else:
        outcome = {
            "type": "step0_closure",
            "closure": closure_kind,
            "failed_check": closure_check,
            "prediction_state": "UNSCORED - PRED-2026-012's s.3 "
                                "Outcome stands PENDING; "
                                "PRED-2026-007's stands "
                                "PARTIALLY CONFIRMED, untouched",
            "scoring_run": False,
            "verdict": None,
        }

    results = {
        "experiment_id": "spec043-pred-2026-007-registry-frame",
        "spec": "043-pred-2026-007-registry-frame",
        "phase": 410,
        "freeze_digest": FREEZE_DIGEST,
        "freeze_merge": FREEZE_MERGE,
        "execution_date": EXECUTION_DATE,
        "prediction": {
            "id": "PRED-2026-012",
            "registered": "2026-10-21",
            "criterion": {
                "verbatim": ">= 70% of ITM-coded signs are "
                            "TERMINAL or cluster in TERMINAL "
                            "clusters",
                "share_min": CRITERION_SHARE,
            },
        },
        "registration": {
            "prediction_registration": {
                "record": "docs/PREDICTION_REGISTER.md s.3, "
                          "PRED-2026-012 (registered "
                          "2026-10-21 under campaign ruling "
                          "E-4)",
            },
            "spec_contract_registration": {
                "osf": f"https://osf.io/{SPEC_REG_ID}/",
                "state": "APPROVED + PUBLIC before this run "
                         "(parent-verified; campaign state "
                         "file, 2026-10-21)",
            },
            "execution_authorization": "the owner's approval "
                                       "of the runnable-"
                                       "experiments campaign "
                                       "plan AS WRITTEN on "
                                       "2026-10-21 (Wave 3; "
                                       "adjudication.md "
                                       "s.7.6)",
        },
        "step0_record": step0,
        "step0_record_sha256": sha256_json(step0),
        "scoring_record": scoring,
        "scoring_record_sha256": sha256_json(scoring)
                                 if scoring else None,
        "outcome": outcome,
    }
    RESULTS_JSON.write_text(
        json.dumps(results, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")

    outcome_title = (outcome.get("closure")
                     or outcome.get("verdict")
                     or outcome["type"])
    lines = [
        "# Phase-410 — Spec 043 step-0 report",
        "",
        "Prediction: PRED-2026-012 (H4 successor: ICIT "
        "Function Alignment) — standing PENDING, unscored. "
        "Execution date: 2026-10-21. Freeze digest: "
        f"`{FREEZE_DIGEST}`. OSF registration vmcra "
        "(approved and public). Execution authorized by the "
        "owner's approval of the runnable-experiments "
        "campaign plan AS WRITTEN on 2026-10-21 (Wave 3).",
        "",
        f"## Outcome: {outcome_title}",
        "",
        "## Checks, in frozen order",
        "",
        f"- **Check 0.1 — Sources and pins: "
        f"{c1['status']}** — all seven frozen sources "
        "present and hashed to the freeze record's pins; "
        "the PRED-2026-012 entry located standing as "
        "registered (criterion verbatim; Outcome PENDING).",
    ]
    if "check_0_2" in step0:
        c2 = step0["check_0_2"]
        lines += [
            f"- **Check 0.2 — Enumeration, re-derivation, "
            f"cross-check: {c2['status']}** — 803 rows read; "
            "census 791 uncoded, 12 coded (ITM 4, LOG 2, "
            "NUM 2, TMK 2, SHN 1, SYL 1); ITM = {P056, "
            "P324, P378, P385}; re-derivation of all 803 "
            "values from the pinned builder rule exact "
            "(zero mismatches); held records verified "
            "(P385, P378 ITM; P098 no code); cross-check "
            "read in full (611 records: 579 empty, 32 "
            "free-text glosses, no ITM, no LOG) with every "
            "disagreement recorded sign-by-sign in the "
            "step-0 record, as expected in kind.",
        ]
    if "check_0_3" in step0:
        c3 = step0["check_0_3"]
        lines += [
            f"- **Check 0.3 — Provenance gate: "
            f"{c3['status']}** — evidence set D1-D4 "
            "produced and adjudicated under DD-043-10. "
            "All three limbs FAIL. Class definition: the "
            "produced documents define the ICTM class by "
            "cluster-final behaviour — Wells classifies "
            "signs 'according to their preferred text "
            "position' and ICTM signs are those that "
            "'mark the end of initial clusters' (Fuls "
            "2013, s.2, s.3.7). Per-sign basis: every "
            "stated basis is positional (W740 terminal "
            "distribution; W820, W817, W861 initial "
            "distribution), and W231 has no stated basis "
            "at all. Source agreement: Wells' published "
            "ICTM class is exactly signs 060, 001, 002 "
            "(Wells 2015, ch. 3); 817, 820, 861 are "
            "published as initial signs, 820 also as a "
            "terminal marker — different functions from "
            "the builder table, and W231 omitted. The "
            "study therefore closes as PROVENANCE — "
            "CANNOT BE RUN AS WRITTEN, unscored. The LOG "
            "trace is recorded in the step-0 record and "
            "gates nothing (DD-043-12).",
        ]
    lines += [
        "- **Check 0.4 — Recorded Phase 5 output "
        "verification: NOT RUN** — the frozen order "
        "reaches it only behind a passed gate. The "
        "recorded clustering and characterisation were "
        "byte-hashed at check 0.1 for integrity and "
        "never opened for assignments; the sanity "
        "anchor was not reproduced, because the check "
        "that reads it was never reached. No Phase 5 "
        "assignment was looked up for any sign.",
        "",
        "## What was not done",
        "",
        "No scoring ran: no share, coverage figure, or "
        "verdict exists. PRED-2026-012 remains unscored "
        "and its registered Outcome stands PENDING; "
        "PRED-2026-007's PARTIALLY CONFIRMED stands "
        "untouched as its own pre-execution record. "
        "This closure records what the classification's "
        "assignments rest on; it is not a verdict on "
        "the criterion and not a refutation.",
        "",
        f"Step-0 record: `reports/phase410_results.json` "
        f"(step-0 record SHA-256 "
        f"`{results['step0_record_sha256']}`).",
        "",
        "*AI disclosure: executed by an AI agent (Muse "
        "Spark, via Muse) at the direction of Tristen "
        "Pierson, per constitution section VI.*",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "step0": {k: v.get("status") for k, v in step0.items()
                  if isinstance(v, dict) and "status" in v},
        "outcome": outcome,
        "step0_record_sha256": results["step0_record_sha256"],
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
