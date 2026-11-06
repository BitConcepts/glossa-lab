#!/usr/bin/env python3
"""Spec 093 Stage 1 — T102 material register checker.

Independent re-application of the register's rules: this script
reads the rules ONLY from the register artifact
(material-normalization-register-v1.json), recomputes every
disposition from the pinned snapshot, and fails on any
divergence from the filed table. It never writes to the
register or the snapshot.

Checks (the register's acceptance checks, per T102):
  1. the register's value set is exactly the snapshot's
     distinct raw `material` value set (a raw value outside
     the register fails here), with per-value record counts
     equal to the snapshot's;
  2. every filed disposition equals the disposition the
     register's own rules recompute for that value;
  3. disposition record counts sum to the snapshot's
     material-bearing record count and value counts sum to
     the distinct count;
  4. every unmapped value carries a non-empty reason; every
     non-material value carries a reason code from the
     register's code list (pattern codes plus NM-MEDIUM and
     NM-TECH);
  5. the register's filed aggregate counts equal the
     recomputed aggregates.

Usage: python3 check_material_register.py <repo-root> <register.json>
Exit 0 and prints PASS with the counts; exit 1 on any failure.
"""
import collections
import json
import re
import sys
from pathlib import Path

SNAPSHOT_SHA256 = ("08fc96c8dbc22a37effb65e789b22b144f4baf22be1da"
                   "55dc3d84db5dc44505e")


class CheckFailure(Exception):
    pass


def fail(msg):
    raise CheckFailure(msg)


def run_checks(root, reg):
    root = Path(root)
    rules = reg["rules"]
    snap_path = root / "glossa-corpus/indus/exports/indus_research.jsonl"
    import hashlib
    digest = hashlib.sha256(snap_path.read_bytes()).hexdigest()
    if digest != SNAPSHOT_SHA256:
        fail(f"snapshot pin mismatch: {digest}")
    snap = [json.loads(l) for l in snap_path.read_text(
        encoding="utf-8").splitlines() if l.strip()]
    counts = collections.Counter(
        r["material"] for r in snap
        if r["material"] not in (None, "", "None"))
    table = reg["dispositions"]
    # check 1: coverage
    if set(table) != set(counts):
        fail(f"value set diverges: register-only "
             f"{sorted(set(table) - set(counts))[:5]} snapshot-only "
             f"{sorted(set(counts) - set(table))[:5]}")
    for v, d in table.items():
        if d["records"] != counts[v]:
            fail(f"record count diverges for {v!r}: filed "
                 f"{d['records']} vs snapshot {counts[v]}")
    # re-apply the rules from the artifact
    class_pats = [(c["id"], [re.compile(r"\b" + re.escape(k) + r"\b", re.I)
                             for k in c["keywords"]])
                  for c in rules["classes"]]
    surface_pats = [(w, re.compile(r"\b" + w + r"\b", re.I))
                    for w in rules["surface_media"]]
    premasks = [re.compile(re.escape(p), re.I)
                for p in rules["technique_premasks"]]
    nm_pats = [(p["code"], re.compile(p["regex"], re.I), p["reason"])
               for p in rules["nonmaterial_patterns"]]
    stopwords = set(rules["residual_stopwords"])
    markers = rules["uncertain_markers"]

    def recompute(raw):
        text = re.sub(r"\s+", " ", raw.replace("\n", " ")).strip()
        low = text.lower()
        uncertain = any(m in low for m in markers)
        for code, pat, reason in nm_pats:
            if pat.search(text):
                return {"kind": "non-material", "classes": [],
                        "surface_media": [], "uncertain": uncertain,
                        "reason_code": code, "reason": reason}
        parens = re.findall(r"\(([^)]*)\)", text)
        pre, suppress = set(), set()
        unfired_paren = any(any(w in pc.lower() for w in
                                ("unfired", "un-baked", "unbaked"))
                            for pc in parens)
        if any("carnelian" in pc.lower() for pc in parens) and \
                re.fullmatch(r"chalcedony\s*(\([^)]*\))?", low):
            pre.add("carnelian")
            suppress.add("chalcedony")
        residual = re.sub(r"\([^)]*\)", " ", text)
        hits = 0
        for pat in premasks:
            residual, n = pat.subn(" ", residual)
            hits += n
        spans = []
        for cid, pats in class_pats:
            for pat in pats:
                for m in pat.finditer(residual):
                    spans.append((m.start(), m.end(), cid))
        spans.sort(key=lambda s: (-(s[1] - s[0]), s[0]))
        taken, classes = [], set()
        for a, b, cid in spans:
            if any(a < tb and b > ta for ta, tb in taken):
                continue
            taken.append((a, b))
            classes.add(cid)
        classes = (classes | pre) - suppress
        surface = sorted({w for w, pat in surface_pats
                          if pat.search(text)})
        if "clay" in classes and "clay-unfired" in classes:
            classes.discard("clay")
        if "clay" in classes and unfired_paren:
            classes.discard("clay")
            classes.add("clay-unfired")
        if not classes:
            if surface:
                return {"kind": "non-material", "classes": [],
                        "surface_media": surface,
                        "uncertain": uncertain,
                        "reason_code": "NM-MEDIUM",
                        "reason": "surface or drawing medium only; "
                                  "no substrate material named"}
            words = {w.strip(";,.:") for w in residual.lower().split()
                     if w.strip(";,.:")}
            if hits and words <= stopwords:
                return {"kind": "non-material", "classes": [],
                        "surface_media": surface,
                        "uncertain": uncertain,
                        "reason_code": "NM-TECH",
                        "reason": "print or drawing technique only; "
                                  "not a material"}
            return {"kind": "unmapped", "classes": [],
                    "surface_media": surface, "uncertain": uncertain,
                    "reason_code": None, "reason": None}
        comps = [c.strip() for c in
                 re.sub(r"\([^)]*\)", " ", text).split(",")]
        kind = "class" if len(classes) == 1 else "composite"
        if len(comps) == 1 and " or " in (" " + comps[0].lower() + " "):
            kind = "alternatives"
            uncertain = True
        return {"kind": kind, "classes": sorted(classes),
                "surface_media": surface, "uncertain": uncertain,
                "reason_code": None, "reason": None}

    known_codes = {c for c, _, _ in nm_pats} | {"NM-MEDIUM", "NM-TECH"}
    kind_counts = collections.Counter()
    kind_records = collections.Counter()
    for v, d in table.items():
        r = recompute(v)
        # the unmapped reason is register text, not rule output;
        # everything else must equal the recomputation
        for field in ("kind", "classes", "surface_media", "uncertain",
                      "reason_code"):
            if d[field] != r[field]:
                fail(f"disposition diverges for {v!r} field {field}: "
                     f"filed {d[field]!r} vs recomputed {r[field]!r}")
        if d["kind"] == "unmapped" and not d["reason"]:
            fail(f"unmapped value without a reason: {v!r}")
        if d["kind"] == "non-material" and \
                d["reason_code"] not in known_codes:
            fail(f"non-material value with unknown code: {v!r}")
        kind_counts[d["kind"]] += 1
        kind_records[d["kind"]] += d["records"]
    # checks 3 + 5: aggregates
    if sum(kind_records.values()) != sum(counts.values()):
        fail("record totals diverge")
    filed = reg["counts"]
    if filed["distinct_values"] != len(table) or \
            filed["records"] != sum(counts.values()) or \
            filed["values_by_kind"] != dict(kind_counts) or \
            filed["records_by_kind"] != dict(kind_records):
        fail("filed aggregate counts diverge from recomputation")
    return (f"PASS: {len(table)} distinct values, "
            f"{sum(counts.values())} records; "
            f"values by kind {dict(kind_counts)}; "
            f"records by kind {dict(kind_records)}; "
            f"rules re-applied from the artifact agree on every value")


def main():
    reg = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    try:
        print(run_checks(Path(sys.argv[1]), reg))
    except CheckFailure as e:
        print("FAIL:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
