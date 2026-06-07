"""Comprehensive anchor quality audit.

Checks ALL 605 anchors in INDUS_FINAL_ANCHORS.json against multiple
quality criteria to find potentially bad/uncertain data that could
taint downstream analysis.

Criteria checked:
1. DEDR support: does the reading have a Dravidian etymology?
2. Corpus presence: does the sign actually appear in the Holdat corpus?
3. Positional consistency: does the sign's T/I/M profile match its reading type?
4. Confidence vs evidence: are HIGH anchors well-supported?
5. Duplicate/conflicting readings: same reading assigned to multiple signs?
6. Orphan anchors: signs with no basis or source
7. Frequency sanity: HIGH-confidence signs should have reasonable corpus frequency
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"

# Load anchors
fa = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
anchors = fa.get("anchors", {})
print(f"=== ANCHOR QUALITY AUDIT ===")
print(f"Total anchors: {len(anchors)}")

by_conf = Counter(v.get("confidence", "?") for v in anchors.values())
print(f"By confidence: {dict(by_conf)}")
print()

# Load corpus
corpus_freq: Counter[str] = Counter()
corpus_seqs: list[list[str]] = []
if HOLDAT_PATH.exists():
    seals: dict[str, list] = defaultdict(list)
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sign = row.get("letters", "").strip()
            if sign:
                corpus_freq[sign] += 1
                seals[row["cisi_number"]].append(row)
    for rows in seals.values():
        rows_s = sorted(rows, key=lambda r: int(r.get("position", 0)))
        signs = [r["letters"] for r in rows_s if r.get("letters")]
        if signs:
            corpus_seqs.append(signs)
    print(f"Corpus: {len(corpus_seqs)} seals, {sum(corpus_freq.values())} tokens, {len(corpus_freq)} unique signs")
else:
    print("WARNING: Holdat corpus not found!")

# Load DEDR vocabulary
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "dravidian", REPO / "backend/glossa_lab/data/dravidian.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    dedr_vocab = {}
    dedr_vocab.update(getattr(mod, "VOCABULARY", {}))
    dedr_vocab.update(getattr(mod, "EXTENDED_VOCABULARY", {}))
    dedr_roots = set()
    for root in dedr_vocab:
        clean = re.sub(r"[^a-z]", "", root.lower())
        if len(clean) >= 2:
            dedr_roots.add(clean)
    print(f"DEDR vocabulary: {len(dedr_vocab)} entries, {len(dedr_roots)} roots")
except Exception as e:
    print(f"WARNING: Could not load DEDR vocab: {e}")
    dedr_roots = set()

print()

# ── Audit checks ──────────────────────────────────────────────────────

issues: list[dict] = []

# 1. Signs not in corpus
print("=== CHECK 1: Signs not in corpus ===")
not_in_corpus = []
for sid, info in anchors.items():
    if sid not in corpus_freq:
        not_in_corpus.append((sid, info.get("confidence", "?"), info.get("reading", "")))
print(f"  {len(not_in_corpus)} anchors for signs NOT in Holdat corpus")
for sid, conf, reading in not_in_corpus[:10]:
    print(f"    {sid} [{conf}] = '{reading}'")
    issues.append({"sign": sid, "issue": "not_in_corpus", "severity": "warn",
                   "detail": f"{sid} [{conf}] not found in Holdat corpus"})
if len(not_in_corpus) > 10:
    print(f"    ... and {len(not_in_corpus) - 10} more")

# 2. No DEDR support for reading
print("\n=== CHECK 2: Readings without DEDR etymology ===")
no_dedr = []
for sid, info in anchors.items():
    reading = info.get("reading", "")
    if not reading:
        continue
    # Check each variant
    has_support = False
    for variant in reading.split("/"):
        clean = re.sub(r"[^a-z]", "", variant.strip().lower())
        if len(clean) >= 2:
            # Check exact and prefix match
            if clean in dedr_roots or any(r.startswith(clean[:3]) for r in dedr_roots):
                has_support = True
                break
    if not has_support:
        conf = info.get("confidence", "?")
        no_dedr.append((sid, conf, reading))
        if conf in ("HIGH", "MEDIUM"):
            issues.append({"sign": sid, "issue": "no_dedr_support", "severity": "high" if conf == "HIGH" else "medium",
                           "detail": f"{sid} [{conf}] = '{reading}' has no DEDR etymology match"})

print(f"  {len(no_dedr)} anchors without DEDR support")
high_no_dedr = [(s, c, r) for s, c, r in no_dedr if c == "HIGH"]
med_no_dedr = [(s, c, r) for s, c, r in no_dedr if c == "MEDIUM"]
print(f"    HIGH without DEDR: {len(high_no_dedr)}")
for sid, conf, reading in high_no_dedr[:10]:
    print(f"      ⚠ {sid} [HIGH] = '{reading}'")
print(f"    MEDIUM without DEDR: {len(med_no_dedr)}")

# 3. No basis/source
print("\n=== CHECK 3: Anchors with no basis or source ===")
no_basis = []
for sid, info in anchors.items():
    basis = info.get("basis", "")
    source = info.get("source", "")
    if not basis and not source:
        no_basis.append((sid, info.get("confidence", "?"), info.get("reading", "")))
        issues.append({"sign": sid, "issue": "no_basis", "severity": "warn",
                       "detail": f"{sid} has no basis or source recorded"})

print(f"  {len(no_basis)} anchors with no basis AND no source")
for sid, conf, reading in no_basis[:10]:
    print(f"    {sid} [{conf}] = '{reading}'")

# 4. Duplicate readings (same reading on multiple signs)
print("\n=== CHECK 4: Duplicate readings ===")
reading_to_signs: dict[str, list[str]] = defaultdict(list)
for sid, info in anchors.items():
    reading = info.get("reading", "").strip().lower()
    if reading:
        reading_to_signs[reading].append(sid)

duplicates = {r: signs for r, signs in reading_to_signs.items() if len(signs) > 1}
print(f"  {len(duplicates)} readings assigned to multiple signs")
for reading, signs in sorted(duplicates.items(), key=lambda x: -len(x[1]))[:10]:
    confs = [anchors[s].get("confidence", "?") for s in signs]
    print(f"    '{reading}' → {signs} [{', '.join(confs)}]")
    if any(c == "HIGH" for c in confs):
        issues.append({"sign": signs[0], "issue": "duplicate_reading_high",
                       "severity": "high",
                       "detail": f"Reading '{reading}' assigned to {len(signs)} signs: {signs}"})

# 5. HIGH-confidence signs with very low corpus frequency
print("\n=== CHECK 5: HIGH anchors with low corpus frequency ===")
low_freq_high = []
for sid, info in anchors.items():
    if info.get("confidence") == "HIGH":
        freq = corpus_freq.get(sid, 0)
        if freq < 5:
            low_freq_high.append((sid, freq, info.get("reading", "")))
            issues.append({"sign": sid, "issue": "high_low_freq", "severity": "warn",
                           "detail": f"{sid} [HIGH] has only {freq} corpus occurrences"})

print(f"  {len(low_freq_high)} HIGH anchors with <5 corpus occurrences")
for sid, freq, reading in low_freq_high[:10]:
    print(f"    {sid} freq={freq} = '{reading}'")

# 6. Positional profile check (terminal markers should have high T-rate)
print("\n=== CHECK 6: Positional profile consistency ===")
if corpus_seqs:
    total_c = Counter(s for seq in corpus_seqs for s in seq)
    terminal_c = Counter(seq[-1] for seq in corpus_seqs if len(seq) > 1)
    initial_c = Counter(seq[0] for seq in corpus_seqs if len(seq) > 1)

    mismatches = []
    for sid, info in anchors.items():
        if info.get("confidence") not in ("HIGH", "MEDIUM"):
            continue
        basis = (info.get("basis") or "").lower()
        reading = (info.get("reading") or "").lower()
        n = total_c.get(sid, 0)
        if n < 10:
            continue

        t_rate = terminal_c.get(sid, 0) / n
        i_rate = initial_c.get(sid, 0) / n

        # Terminal markers should have high T-rate
        if any(kw in basis for kw in ("terminal", "suffix", "case marker", "ending")):
            if t_rate < 0.2:
                mismatches.append((sid, "terminal_marker_low_t", t_rate, info.get("reading", "")))
                issues.append({"sign": sid, "issue": "positional_mismatch",
                               "severity": "high",
                               "detail": f"{sid} labeled terminal but T-rate={t_rate:.2f} (<0.2)"})

        # Initial/prefix signs should have high I-rate
        if any(kw in basis for kw in ("initial", "prefix", "classifier", "determiner")):
            if i_rate < 0.2:
                mismatches.append((sid, "initial_marker_low_i", i_rate, info.get("reading", "")))
                issues.append({"sign": sid, "issue": "positional_mismatch",
                               "severity": "high",
                               "detail": f"{sid} labeled initial but I-rate={i_rate:.2f} (<0.2)"})

    print(f"  {len(mismatches)} positional mismatches found")
    for sid, issue_type, rate, reading in mismatches[:10]:
        print(f"    ⚠ {sid} = '{reading}': {issue_type} (rate={rate:.3f})")

# 7. Empty or very short readings
print("\n=== CHECK 7: Empty or suspicious readings ===")
empty_readings = []
for sid, info in anchors.items():
    reading = info.get("reading", "").strip()
    if not reading:
        empty_readings.append((sid, info.get("confidence", "?")))
        issues.append({"sign": sid, "issue": "empty_reading", "severity": "high",
                       "detail": f"{sid} [{info.get('confidence')}] has empty reading"})
    elif len(reading) > 50:
        # Suspiciously long reading (might be a description, not a reading)
        issues.append({"sign": sid, "issue": "long_reading", "severity": "warn",
                       "detail": f"{sid} reading is {len(reading)} chars (might be description)"})

print(f"  {len(empty_readings)} anchors with empty reading")

# ── Summary ──────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print(f"AUDIT SUMMARY")
print(f"{'='*60}")

high_issues = [i for i in issues if i["severity"] == "high"]
med_issues = [i for i in issues if i["severity"] == "medium"]
warn_issues = [i for i in issues if i["severity"] == "warn"]

print(f"Total issues found: {len(issues)}")
print(f"  🔴 HIGH severity: {len(high_issues)}")
print(f"  🟡 MEDIUM severity: {len(med_issues)}")
print(f"  ⚪ WARN severity: {len(warn_issues)}")

if high_issues:
    print(f"\n🔴 HIGH SEVERITY ISSUES (require review):")
    for i in high_issues[:20]:
        print(f"  {i['issue']}: {i['detail']}")

# Save report
report_path = REPO / "reports" / "anchor_quality_audit.json"
report_path.parent.mkdir(parents=True, exist_ok=True)
report = {
    "total_anchors": len(anchors),
    "by_confidence": dict(by_conf),
    "total_issues": len(issues),
    "high_issues": len(high_issues),
    "medium_issues": len(med_issues),
    "warn_issues": len(warn_issues),
    "not_in_corpus": len(not_in_corpus),
    "no_dedr_support": len(no_dedr),
    "no_basis": len(no_basis),
    "duplicate_readings": len(duplicates),
    "low_freq_high": len(low_freq_high),
    "empty_readings": len(empty_readings),
    "issues": issues,
}
report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nFull report saved to: {report_path}")
