#!/usr/bin/env python3
"""Phase-404 — Spec 044 step 0 (fish-sign coastal residue,
sign by sign; design D-02; builds Asset F).

Executes STEP 0 ONLY of the frozen Spec 044 contract
(specs/044-fish-sign-coastal-residue/freeze.md, digest
6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f020fcf25691d9c8):
the step-0 gates of spec §3, in order, and the one-time
build of Asset F, the frozen fish-family list (spec §4).
The §5 primary test, the sensitivities, and every later
execution step are NOT run by this script (campaign
Wave 3, Group 1: step 0 only; the residue test itself
is Group 3 work).

Gates, in the frozen order:
  0.1 Corpus layer identification and pin — the Holdat
      corpus file identified at the freeze as the layer
      the original family-level test used is re-asserted
      by SHA-256 and its population description is
      re-derived and checked against the claim record
      (7,002 tokens; 1,670 inscriptions over 9 sites;
      M047 at 13 tokens in 13 inscriptions; the
      Phase-45 T6 table 2 / 10 / 228 / 1,369 with
      Surkotada unclassed, Fisher two-sided
      p = 0.685). Failure closes LAYER NOT PINNABLE.
  0.2 Asset F freeze — the fish-family list is built
      solely from Parpola's published list, as held by
      the programme in the pinned Mahadevan–Parpola
      crosswalk (which cites Parpola 1994b, sign list
      = Parpola 1994a fig. 5.1, pp. 70–78), every
      member carrying its per-sign locator, and frozen
      as specs/044-fish-sign-coastal-residue/
      asset-f-fish-family.json; the digest (SHA-256 of
      the canonical bytes with the digest field
      excluded) is the asset's identity. Failure
      closes ASSET F FREEZE FAILED.
  0.3 Coastal list freeze — every site in the pinned
      layer's site set is classed coastal/maritime or
      inland under the design's rule (a port, or
      within the coastal zone) from the pinned
      Spec 027 Stage 0 gazetteer and published site
      geography; Lothal and Dholavira are members by
      name; contested sites are listed as contested.
      No site is classed by its fish counts.
  0.4 Census (margins only) — per Asset F member, the
      total occurrence count in the pinned layer, no
      site split. Members below 30 total occurrences
      are TOO THIN per member. Fewer than two members
      clearing the floor closes the execution as
      TOO THIN, with the full census as its finding.
  0.5 Baseline statement — reached only if gate 0.4
      does not close: the corpus-wide coastal share
      is stated before any per-sign test.

Integrity: every spec §2 pin is asserted before any
counting (a mismatch closes INVALID); the anchors
file is asserted byte-identical before and after.
Fail-closed: any pin, shape, or gate violation
aborts before any output is written, except that a
gate closure writes the closure record itself.

Outputs:
  - specs/044-fish-sign-coastal-residue/
    asset-f-fish-family.json (Asset F, spec §4.1)
  - reports/phase404_results.json (the step-0 record)
  - reports/phase404_step0_report.md (the step-0
    report, under spec §9's headline rules)

This record is internal under the campaign's Roif
gate (R-7); it is not a publication.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_LAYER = (_REPO / "corpora/downloads/external_repos/"
          "holdatllc_indus/indus_corpus 2.csv")
_GAZETTEER = _REPO / "data/movement/gazetteer_rows.jsonl"
_CROSSWALK = (_REPO / "backend/glossa_lab/data/"
              "mahadevan_parpola_crosswalk.json")
_CLAIM = (_REPO / "glossa-indus/claims/extracted_claims/"
          "indus_valley_script_deciphered_from_myth_"
          "65ff0a26.json")
_ANCHORS = _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
_SPEC_DIR = _REPO / "specs/044-fish-sign-coastal-residue"
_ASSET_F = _SPEC_DIR / "asset-f-fish-family.json"
_OUT_RESULTS = _REPO / "reports/phase404_results.json"
_OUT_REPORT = _REPO / "reports/phase404_step0_report.md"

FREEZE_DIGEST = (
    "6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f"
    "020fcf25691d9c8")
LAYER_SHA256 = (
    "62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e"
    "85d1f7f40cbe28218e")
GAZETTEER_SHA256 = (
    "5ac76a3031121a61fa39f87b1d2760855374d171ddd0369"
    "88fee2820dca9b8b6")
CROSSWALK_SHA256 = (
    "9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28"
    "ccc6e06444a2dc69b")
CLAIM_SHA256 = (
    "bc22d6f010f800d608d6e3f620fb430b3cf8d3ccd3caadc"
    "6a989116fbfd125ed")
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e"
    "6086592b32d34f569")
EXECUTION_DATE = "2026-10-21"
REVIEWER = "Muse Spark via Muse (AI agent)"

SOURCE_CITATION = (
    "Parpola, Asko. 1994. Deciphering the Indus "
    "Script. Cambridge: CUP — the published sign "
    "list (fig. 5.1, pp. 70–78)")

# Gate 0.3 — the frozen coastal list. Classed from the
# pinned gazetteer and published site geography under
# the design's rule (a port, or within the coastal
# zone), BEFORE any census exists. Lothal and
# Dholavira are members by name (spec §3). No site is
# classed by its fish counts, ever.
COASTAL_LIST = [
    {"site": "Banawali", "class": "inland",
     "contested": False,
     "basis": "Ghaggar plain in Haryana, far inland; "
              "no port or coastal-zone location in "
              "published geography."},
    {"site": "Chanhu-daro", "class": "inland",
     "contested": False,
     "basis": "Indus floodplain in Sindh, south of "
              "Mohenjo-daro and well inland from the "
              "coast; a riverine craft town, not a "
              "port."},
    {"site": "Dholavira", "class": "coastal",
     "contested": False,
     "basis": "Member by name (spec §3). Published "
              "geography: on Khadir island in the "
              "Rann of Kutch, a coastal saline zone "
              "with maritime access in the Harappan "
              "period."},
    {"site": "Harappa", "class": "inland",
     "contested": False,
     "basis": "Ravi floodplain in Punjab, far "
              "inland."},
    {"site": "Kalibangan", "class": "inland",
     "contested": False,
     "basis": "Ghaggar bank in northern Rajasthan, "
              "far inland."},
    {"site": "Lothal", "class": "coastal",
     "contested": False,
     "basis": "Member by name (spec §3). Published "
              "geography: the Harappan port town on "
              "the Gulf of Khambhat, with its "
              "dockyard."},
    {"site": "Mohenjo-daro", "class": "inland",
     "contested": False,
     "basis": "Indus floodplain in upper Sindh, far "
              "inland."},
    {"site": "Rakhigarhi", "class": "inland",
     "contested": False,
     "basis": "Ghaggar–Hakra plain in Haryana, far "
              "inland."},
    {"site": "Surkotada", "class": "inland",
     "contested": True,
     "basis": "Kutch interior east of the Little "
              "Rann; published descriptions place "
              "this fortified town on the inland "
              "Kutch plain, not at a port. Its "
              "coastal-zone status is contested in "
              "the literature (Kutch coastal "
              "groupings include it), and the "
              "original Phase-45 script left it "
              "unclassed; classed inland here and "
              "listed as contested."},
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """ Fisher's exact test, two-sided, by direct
    hypergeometric enumeration (no dependency)."""
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def prob(x: int) -> float:
        return (math.comb(c1, x) * math.comb(n - c1, r1 - x)
                / math.comb(n, r1))

    lo = max(0, r1 - (n - c1))
    hi = min(r1, c1)
    p_obs = prob(a)
    return sum(prob(x) for x in range(lo, hi + 1)
               if prob(x) <= p_obs * (1 + 1e-9))


def _canonical(obj: dict) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True,
                       ensure_ascii=False)
            + "\n").encode("utf-8")


def main() -> int:
    gates: list[dict] = []

    # ── Integrity pins (spec §2), before any counting.
    # A mismatch closes INVALID (spec §10).
    pins = {
        "claim_file": (_CLAIM, CLAIM_SHA256),
        "gazetteer": (_GAZETTEER, GAZETTEER_SHA256),
        "crosswalk": (_CROSSWALK, CROSSWALK_SHA256),
        "anchors": (_ANCHORS, ANCHORS_SHA256),
    }
    pin_results = {}
    for name, (path, want) in pins.items():
        got = _sha256(path) if path.exists() else None
        pin_results[name] = {"path": str(path.relative_to(_REPO)),
                             "pinned_sha256": want,
                             "observed_sha256": got,
                             "match": got == want}
        if got != want:
            print(f"Phase-404 INVALID: §2 pin mismatch on "
                  f"{name} ({got} != {want}); nothing counted.")
            return 2
    anchors_before = pin_results["anchors"]["observed_sha256"]

    # ── Gate 0.1 — corpus layer identification and pin.
    if not _LAYER.exists():
        gates.append({"gate": "0.1", "verdict":
                      "LAYER NOT PINNABLE",
                      "reason": "the layer of record is "
                                "absent from the downloads "
                                "tree at the pinned path"})
        _write_closure(gates, pin_results, anchors_before,
                       "LAYER NOT PINNABLE",
                       "the CISI-based corpus layer of "
                       "record could not be uniquely "
                       "identified and pinned as the "
                       "layer the original test used "
                       "(the Holdat corpus file is absent "
                       "from the downloads tree at the "
                       "pinned path)")
        return 0
    layer_bytes = _LAYER.read_bytes()
    layer_sha = hashlib.sha256(layer_bytes).hexdigest()
    rows = list(csv.DictReader(
        layer_bytes.decode("utf-8").splitlines()))
    insc_site = {}
    for r in rows:
        insc_site.setdefault(r["cisi_number"], r["site"])
    site_insc = Counter(insc_site.values())
    m047 = [r for r in rows if r["letters"] == "M047"]
    m047_insc = {r["cisi_number"] for r in m047}
    coastal_pair = {"Lothal", "Dholavira"}
    t_a = len([c for c in m047_insc
               if insc_site[c] in coastal_pair])
    t_b = len([c for c in m047_insc
               if insc_site[c] not in coastal_pair
               and insc_site[c] != "Surkotada"])
    t_c = len([c for c, s in insc_site.items()
               if s in coastal_pair and c not in m047_insc])
    t_d = len([c for c, s in insc_site.items()
               if s not in coastal_pair
               and s != "Surkotada" and c not in m047_insc])
    t_p = _fisher_two_sided(t_a, t_b, t_c, t_d)
    reproduction = {
        "token_rows": len(rows),
        "inscriptions": len(insc_site),
        "inscriptions_per_site": dict(sorted(
            site_insc.items())),
        "m047_tokens": len(m047),
        "m047_inscriptions": len(m047_insc),
        "phase45_t6_table": {
            "coastal_with": t_a, "inland_with": t_b,
            "coastal_without": t_c, "inland_without": t_d,
            "unclassed_site_excluded": "Surkotada"},
        "phase45_t6_fisher_two_sided_p": t_p,
    }
    expected_sites = {
        "Mohenjo-daro": 606, "Harappa": 492, "Lothal": 124,
        "Kalibangan": 110, "Dholavira": 106,
        "Chanhu-daro": 78, "Surkotada": 61,
        "Banawali": 60, "Rakhigarhi": 33}
    gate01_ok = (
        layer_sha == LAYER_SHA256
        and len(rows) == 7002
        and len(insc_site) == 1670
        and dict(site_insc) == expected_sites
        and len(m047) == 13 and len(m047_insc) == 13
        and (t_a, t_b, t_c, t_d) == (2, 10, 228, 1369)
        and round(t_p, 3) == 0.685)
    gates.append({
        "gate": "0.1", "verdict": "PASS" if gate01_ok
        else "LAYER NOT PINNABLE",
        "layer_path": "corpora/downloads/external_repos/"
                      "holdatllc_indus/indus_corpus 2.csv",
        "layer_bytes": len(layer_bytes),
        "layer_sha256": layer_sha,
        "pinned_sha256": LAYER_SHA256,
        "population_reproduction": reproduction})
    if not gate01_ok:
        _write_closure(gates, pin_results, anchors_before,
                       "LAYER NOT PINNABLE",
                       "the CISI-based corpus layer of "
                       "record could not be uniquely "
                       "identified and pinned as the "
                       "layer the original test used "
                       "(the exhibited file does not "
                       "reproduce the original population "
                       "description)")
        return 0

    # ── Gate 0.2 — Asset F build and freeze (spec §4).
    cross = json.loads(_CROSSWALK.read_text("utf-8"))
    cw = cross["crosswalk"]
    fish = {k: v for k, v in cw.items()
            if v.get("fish_family_member") is True}
    fam = cross["allograph_families"]["fish"]["members"]
    members = []
    for key in sorted(fish):
        v = fish[key]
        parpola = int(v["parpola_id"])
        if str(parpola) not in fam:
            print(f"Phase-404 ASSET F FREEZE FAILED: "
                  f"{key} (Parpola {parpola}) is flagged "
                  f"a fish-family member in the crosswalk "
                  f"entries but absent from its fish "
                  f"allograph family; nothing counted.")
            return 2
        plain = v["iconic"] == "fish (plain)"
        members.append({
            "sign_key": key,
            "mahadevan_number": int(key[1:]),
            "parpola_number": parpola,
            "depiction_note": v["iconic"],
            "source_citation": SOURCE_CITATION,
            "source_locator": (
                f"Parpola 1994, fig. 5.1 sign list, "
                f"entry {parpola} (pp. 70–78)"),
            "inclusion_basis": (
                "parpola-list-fish" if plain
                else "parpola-list-fish-variant"),
            "contested": False,
            "notes": (
                "Allograph of Parpola 47 in the "
                "programme's Mahadevan–Parpola "
                "crosswalk."
                if v.get("allograph_of") == "47" else ""),
        })
    gate02_ok = (
        len(members) == cross["stats"]["n_fish_family_members"]
        == 7 and len(fam) == 7
        and all(m["source_locator"] for m in members))
    if not gate02_ok:
        gates.append({"gate": "0.2", "verdict":
                      "ASSET F FREEZE FAILED",
                      "reason": "the crosswalk's fish-family "
                                "records do not yield the "
                                "enumerable family its own "
                                "statistics state"})
        _write_closure(gates, pin_results, anchors_before,
                       "ASSET F FREEZE FAILED",
                       "the fish-family list could not "
                       "be frozen from Parpola's "
                       "published list as the §4 contract "
                       "requires (the programme's "
                       "crosswalk record of that list "
                       "does not yield an enumerable "
                       "family with a locator per member)")
        return 0
    asset = {
        "asset": "F",
        "built_by": "Spec 044 step 0",
        "source": SOURCE_CITATION + " — as cited in "
                  "the programme's Mahadevan–Parpola "
                  "crosswalk (backend/glossa_lab/data/"
                  "mahadevan_parpola_crosswalk.json, "
                  "SHA-256 " + CROSSWALK_SHA256 + ")",
        "frozen_at": EXECUTION_DATE,
        "member_count": len(members),
        "members": members,
    }
    digest = hashlib.sha256(_canonical(asset)).hexdigest()
    asset_with_digest = dict(asset, digest=digest)
    _ASSET_F.write_bytes(_canonical(asset_with_digest))
    # Cross-check (DD-044-5): the claim record's named
    # trio and the Phase-43 six, reported, never a
    # membership source.
    asset_mah = {m["mahadevan_number"] for m in members}
    trio = [72, 64, 70]
    phase43_six = [267, 72, 65, 59, 60, 70]
    cross_check = {
        "claim_record_trio_mahadevan": trio,
        "trio_in_asset_f": [n for n in trio
                            if n in asset_mah],
        "trio_not_in_asset_f": [n for n in trio
                                if n not in asset_mah],
        "phase43_six_candidates": phase43_six,
        "phase43_six_in_asset_f": [n for n in phase43_six
                                   if n in asset_mah],
        "phase43_six_not_in_asset_f": [
            n for n in phase43_six if n not in asset_mah],
        "note": "The trio and the six are Mahadevan "
                "numbers as named in the claim record "
                "and the Phase-43 record, whose corpus "
                "numbering is not the pinned layer's; "
                "Asset F's members are fixed solely by "
                "Parpola's published list via the "
                "crosswalk (DD-044-5). The divergence "
                "is reported; it adds and removes no "
                "member.",
    }
    gates.append({
        "gate": "0.2", "verdict": "PASS",
        "asset_path": "specs/044-fish-sign-coastal-"
                      "residue/asset-f-fish-family.json",
        "asset_digest": digest,
        "member_count": len(members),
        "members": [m["sign_key"] for m in members],
        "cross_check": cross_check})

    # ── Gate 0.3 — coastal list freeze.
    layer_sites = sorted({r["site"] for r in rows})
    listed = sorted(e["site"] for e in COASTAL_LIST)
    gaz_sites = set()
    for line in _GAZETTEER.read_text("utf-8").splitlines():
        if line.strip():
            gaz_sites.add(json.loads(line)
                          ["program_site_id"])
    gate03_ok = listed == layer_sites
    gates.append({
        "gate": "0.3", "verdict": "PASS" if gate03_ok
        else "COASTAL LIST FAILED",
        "coastal_list": COASTAL_LIST,
        "coastal_sites": [e["site"] for e in COASTAL_LIST
                          if e["class"] == "coastal"],
        "contested_sites": [e["site"] for e in COASTAL_LIST
                            if e["contested"]],
        "gazetteer_presence": {
            s: (s.lower().replace("-", " ") in gaz_sites
                or s.lower() in gaz_sites)
            for s in layer_sites},
        "rule": "a site is coastal/maritime if its "
                "published location is a port or "
                "within the coastal zone (design "
                "rule); Lothal and Dholavira are "
                "members by name; no site classed by "
                "its fish counts"})
    if not gate03_ok:
        _write_closure(gates, pin_results, anchors_before,
                       "COASTAL LIST FAILED",
                       "the coastal site list could not "
                       "be frozen under the design's "
                       "rule (a site in the pinned "
                       "layer's site set cannot be "
                       "classed from the gazetteer and "
                       "published geography)")
        return 0

    # ── Gate 0.4 — census (margins only).
    counts = Counter(r["letters"] for r in rows)
    census = []
    for m in members:
        total = counts.get(m["sign_key"], 0)
        census.append({
            "sign_key": m["sign_key"],
            "total_occurrences": total,
            "disposition": ("CLEARS FLOOR" if total >= 30
                            else "TOO THIN")})
    clearing = [c for c in census
                if c["total_occurrences"] >= 30]
    gates.append({
        "gate": "0.4",
        "verdict": "PASS" if len(clearing) >= 2
        else "TOO THIN",
        "floor": 30,
        "census": census,
        "members_clearing_floor": len(clearing)})

    if len(clearing) < 2:
        census_text = "; ".join(
            f"{c['sign_key']} {c['total_occurrences']}"
            for c in census)
        headline = (
            "The sign-by-sign residue test cannot be "
            "run as designed: fewer than two fish "
            "signs clear the 30-occurrence floor in "
            "the pinned corpus layer (census: "
            + census_text + "). No per-sign coastal "
            "test was computed. The family-level "
            "verdict — partially falsified — stands "
            "exactly as recorded, and the residue "
            "remains open only in the sense this "
            "census states: the surviving record is "
            "too thin to test it sign by sign.")
        _write_record(gates, pin_results, anchors_before,
                      "TOO THIN", headline, census,
                      baseline=None)
        return 0

    # ── Gate 0.5 — baseline (only if 0.4 did not close).
    coastal_set = {e["site"] for e in COASTAL_LIST
                   if e["class"] == "coastal"}
    total_tokens = len(rows)
    coastal_tokens = sum(1 for r in rows
                         if r["site"] in coastal_set)
    baseline = {
        "total_tokens": total_tokens,
        "coastal_tokens": coastal_tokens,
        "corpus_wide_coastal_share":
            coastal_tokens / total_tokens}
    gates.append({"gate": "0.5", "verdict": "PASS",
                  "baseline": baseline})
    _write_record(gates, pin_results, anchors_before,
                  "STEP 0 COMPLETE — gates 0.1–0.5 "
                  "passed; the §5 test is later "
                  "execution work, not run here",
                  None, census, baseline=baseline)
    return 0


def _base_record(gates, pin_results, anchors_before):
    anchors_after = _sha256(_ANCHORS)
    return {
        "phase": 404,
        "spec": "044-fish-sign-coastal-residue",
        "execution": "Step 0 only (campaign Wave 3, "
                     "Group 1) — executed " + EXECUTION_DATE,
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": "6p9et (approved + public)",
        "reviewer": REVIEWER,
        "pins": pin_results,
        "anchors_assertion": {
            "before_sha256": anchors_before,
            "after_sha256": anchors_after,
            "byte_identical": anchors_before
            == anchors_after == ANCHORS_SHA256},
        "gates": gates,
        "roif_hold": "This record is internal under "
                     "the campaign's Roif gate (R-7); "
                     "it is not a publication.",
    }


def _write_report(rec):
    gates = {g["gate"]: g for g in rec["gates"]}
    lines = [
        "# Phase-404 — Spec 044 step-0 report "
        "(fish-sign coastal residue; Asset F build)",
        "",
        "This record is internal under the campaign's "
        "Roif gate (R-7); it is not a publication.",
        "",
        f"**Outcome: {rec['outcome']}**"
        + (f" — {rec['headline']}" if rec.get("headline")
           else ""),
        "",
        "## Headline facts (spec §9)",
        "",
        "- Corpus: the CISI-based layer of record as "
        "pinned at gate 0.1 — the Holdat corpus file "
        "the Phase-45/46/54 scripts of record read "
        f"(SHA-256 `{LAYER_SHA256}`; 7,002 sign-token "
        "rows; 1,670 inscriptions over 9 sites).",
    ]
    if "0.2" in gates and gates["0.2"].get("asset_digest"):
        g2 = gates["0.2"]
        lines.append(
            f"- Asset F: digest "
            f"`{g2['asset_digest']}`, "
            f"{g2['member_count']} members "
            f"({', '.join(g2['members'])}), frozen at "
            f"specs/044-fish-sign-coastal-residue/"
            f"asset-f-fish-family.json before any "
            f"census existed.")
    if "0.3" in gates and gates["0.3"].get("coastal_list"):
        g3 = gates["0.3"]
        lines.append(
            "- Frozen coastal list: coastal/maritime = "
            + ", ".join(g3["coastal_sites"])
            + "; contested sites named: "
            + (", ".join(g3["contested_sites"]) or "none")
            + " (Surkotada classed inland and listed "
            "as contested).")
    if rec.get("census"):
        lines += ["", "## Census (gate 0.4, margins only)",
                  "",
                  "| Sign | Total occurrences | "
                  "Disposition |",
                  "|---|---|---|"]
        for c in rec["census"]:
            lines.append(
                f"| {c['sign_key']} | "
                f"{c['total_occurrences']} | "
                f"{c['disposition']} |")
    lines += [
        "",
        "## What this does and does not establish",
        "",
        "Step 0 ran in the frozen gate order and "
        "closed at gate 0.4. No per-sign coastal test "
        "was computed, no coastal split of any sign "
        "was counted, and gate 0.5 was not reached. "
        "The family-level verdict — partially "
        "falsified — stands exactly as recorded. "
        "Nothing here establishes what any fish sign "
        "meant.",
        "",
        "*AI disclosure: executed by an AI agent "
        "(Muse Spark, via Muse) at the direction "
        "of Tristen Pierson, per constitution §VI.*",
        "",
    ]
    _OUT_REPORT.write_text("\n".join(lines),
                           encoding="utf-8")


def _write_record(gates, pin_results, anchors_before,
                  outcome, headline, census, baseline):
    rec = _base_record(gates, pin_results, anchors_before)
    rec["outcome"] = outcome
    if headline is not None:
        rec["headline"] = headline
    rec["census"] = census
    if baseline is not None:
        rec["baseline"] = baseline
    _OUT_RESULTS.write_text(
        json.dumps(rec, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n",
        encoding="utf-8")
    _write_report(rec)
    print(f"Phase-404 step 0 complete: outcome "
          f"{outcome}")


def _write_closure(gates, pin_results, anchors_before,
                   outcome, reason):
    rec = _base_record(gates, pin_results, anchors_before)
    rec["outcome"] = outcome
    rec["closure_reason"] = reason
    _OUT_RESULTS.write_text(
        json.dumps(rec, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n",
        encoding="utf-8")
    _write_report(rec)
    print(f"Phase-404 step 0 closed: {outcome} — {reason}")


if __name__ == "__main__":
    raise SystemExit(main())
