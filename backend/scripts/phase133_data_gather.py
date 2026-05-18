"""Phase-133 data gathering for all sub-tasks."""
import json, sys, os
from pathlib import Path
from collections import Counter, defaultdict
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "glossa_lab" / "data"))

df = pd.read_csv(REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv")
anchors = json.loads((REPO / "backend/reports/INDUS_FINAL_ANCHORS.json").read_text())["anchors"]
hm = {k for k, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
seal_groups = df.groupby("form")["letters"].apply(list).to_dict()
seal_site = df.groupby("form")["site"].first().to_dict()
seal_icon = df.groupby("form")["iconography"].first().to_dict()
hm_readings = {k: v.get("reading", "?") for k, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

terminal_signs = {"M342","M176","M367","M336","M305","M048","M089"}
classifier_signs = {"M211","M062","M073","M045","M039","M016","M080","M006","M060","M067","M008","M013"}

# ── V11: Terminal-in-initial ─────────────────────────────────────────────────
print("=== V11: TERMINAL-IN-INITIAL SEALS ===")
tii_seals = []
for form, signs in seal_groups.items():
    if len(signs) >= 2 and signs[0] in terminal_signs:
        tii_seals.append({
            "form": form, "signs": signs, "first_sign": signs[0],
            "site": seal_site.get(form, "?"), "icon": seal_icon.get(form, "?"),
        })

print(f"Total terminal-in-initial seals: {len(tii_seals)}")
first_sign_counts = Counter(s["first_sign"] for s in tii_seals)
print("Terminal signs at initial pos:", dict(first_sign_counts))
site_counts = Counter(s["site"] for s in tii_seals)
print("Site distribution:", dict(site_counts))
icon_counts = Counter(s["icon"] for s in tii_seals)
print("Iconography:", dict(icon_counts.most_common(6)))
print("Examples:")
for s in tii_seals[:8]:
    print(f"  {s['form']} site={s['site']} icon={s['icon']}: {s['signs']}")
both_ends = [s for s in tii_seals if s["signs"][-1] in terminal_signs]
reversed_seals = [s for s in tii_seals if s["signs"][-1] in classifier_signs]
print(f"Both ends terminal: {len(both_ends)} ({len(both_ends)/len(tii_seals)*100:.0f}%)")
print(f"Classifier at END (reversed?): {len(reversed_seals)}")

# Are TII seals short?
lengths = Counter(len(s["signs"]) for s in tii_seals)
print("Length distribution:", dict(sorted(lengths.items())))

# What does M048/M089 look like at position 0 vs elsewhere?
for sign in ["M048","M089","M176","M342","M336"]:
    at_initial = sum(1 for signs in seal_groups.values() if len(signs)>=2 and signs[0]==sign)
    at_terminal = sum(1 for signs in seal_groups.values() if len(signs)>=2 and signs[-1]==sign)
    total = df[df["letters"]==sign].shape[0]
    print(f"  {sign} ({anchors.get(sign,{}).get('reading','?')}): total={total} initial={at_initial} terminal={at_terminal}")
print()

# ── 133b: Grammar model relaxed ──────────────────────────────────────────────
print("=== 133b: GRAMMAR MODEL RELAXED TEST ===")
full_strict = full_relaxed = partial = neither = total_multi = 0
for form, signs in seal_groups.items():
    if len(signs) < 2:
        continue
    total_multi += 1
    c_strict = signs[0] in classifier_signs
    c_relaxed = any(s in classifier_signs for s in signs[:2])
    t_strict = signs[-1] in terminal_signs
    t_relaxed = any(s in terminal_signs for s in signs[-2:])
    if c_strict and t_strict:
        full_strict += 1
    if c_relaxed and t_relaxed:
        full_relaxed += 1
    elif c_relaxed or t_relaxed:
        partial += 1
    else:
        neither += 1

print(f"Total multi-sign seals: {total_multi}")
print(f"Strict [C@0][T@-1]:         {full_strict}/{total_multi} = {full_strict/total_multi:.1%}")
print(f"Relaxed [C in 1-2][T in last 2]: {full_relaxed}/{total_multi} = {full_relaxed/total_multi:.1%}")
print(f"Partial (one of C or T):    {partial}/{total_multi} = {partial/total_multi:.1%}")
print(f"Neither:                    {neither}/{total_multi} = {neither/total_multi:.1%}")

# Explained variance: what fraction of sign-positions are predicted by the model?
correct_pos = 0; total_pos = 0
for form, signs in seal_groups.items():
    n = len(signs)
    for i, s in enumerate(signs):
        total_pos += 1
        if i == 0 and s in classifier_signs: correct_pos += 1
        elif i == n-1 and s in terminal_signs: correct_pos += 1
        elif 0 < i < n-1 and s not in classifier_signs and s not in terminal_signs: correct_pos += 1
explained = correct_pos / total_pos if total_pos else 0
print(f"Model explained variance (position accuracy): {explained:.3f} ({explained*100:.1f}%)")
print()

# ── 133c: Collocate mining for kur-parking signs ─────────────────────────────
print("=== 133c: KUR-PARKING COLLOCATE MINING ===")
kur_parking = {k for k, v in anchors.items()
               if v.get("confidence") == "LOW"
               and v.get("reading") == "kur"
               and "allograph" in str(v.get("basis", "")).lower()}
print(f"Total kur-parking LOW signs: {len(kur_parking)}")

# For each kur-parking sign, get its specific collocate fingerprint
kur_collocates = {}
for sign in list(kur_parking)[:20]:  # sample 20
    before, after = Counter(), Counter()
    for signs in seal_groups.values():
        for i, s in enumerate(signs):
            if s != sign: continue
            if i > 0: before[signs[i-1]] += 1
            if i < len(signs)-1: after[signs[i+1]] += 1
    freq = df[df["letters"]==sign].shape[0]
    top_b = [(s, c) for s, c in before.most_common(3)]
    top_a = [(s, c) for s, c in after.most_common(3)]
    # Check if before/after pattern is distinctive
    b_readings = [hm_readings.get(s, "?") for s, _ in top_b]
    a_readings = [hm_readings.get(s, "?") for s, _ in top_a]
    kur_collocates[sign] = {
        "freq": freq, "before": top_b, "after": top_a,
        "before_readings": b_readings, "after_readings": a_readings,
    }
    print(f"  {sign} f={freq}: before={b_readings} after={a_readings}")

# Are any collocate patterns distinctive enough to infer a reading?
# Pattern: sign before M342(ay) = likely name suffix → reading is TERMINAL-adjacent
before_terminal = []
after_classifier = []
for sign, data in kur_collocates.items():
    after_signs = [s for s, _ in data["after"]]
    before_signs = [s for s, _ in data["before"]]
    if "M342" in after_signs or "M176" in after_signs:
        before_terminal.append(sign)
    if any(s in classifier_signs for s in before_signs):
        after_classifier.append(sign)

print(f"Kur-parking signs immediately before terminal (→name suffix context): {before_terminal}")
print(f"Kur-parking signs immediately after classifier: {after_classifier}")
print()

# ── 133d: Decode audit corrected ─────────────────────────────────────────────
print("=== 133d: CORRECTED DECODE AUDIT (157 H+M) ===")
fully_decoded = sum(1 for signs in seal_groups.values() if all(s in hm for s in signs))
total_seals = len(seal_groups)
print(f"Total seals: {total_seals}")
print(f"Fully decoded: {fully_decoded} ({fully_decoded/total_seals:.1%})")
print(f"Not fully decoded: {total_seals-fully_decoded} ({(total_seals-fully_decoded)/total_seals:.1%})")
site_fd = defaultdict(lambda: {"total": 0, "fd": 0})
for form, signs in seal_groups.items():
    site = seal_site.get(form, "?")
    site_fd[site]["total"] += 1
    if all(s in hm for s in signs):
        site_fd[site]["fd"] += 1
for site in sorted(site_fd):
    d = site_fd[site]
    print(f"  {site}: {d['fd']}/{d['total']} ({100*d['fd']/d['total']:.0f}%)")

# Top blockers
blocker_counts = Counter()
for signs in seal_groups.values():
    for s in signs:
        if s not in hm:
            blocker_counts[s] += 1
print("Top 15 blockers:")
for sign, cnt in blocker_counts.most_common(15):
    conf = anchors.get(sign, {}).get("confidence", "MISSING")
    r = anchors.get(sign, {}).get("reading", "?")
    print(f"  {sign} ({conf}={r}): blocks {cnt} seals")
print()

# ── 133e: Phase-61 vowel harmony definition ───────────────────────────────────
print("=== 133e: PHASE-61 VOWEL HARMONY REPLICATION ===")
# Phase-61 definition: check sequential vowel pairs in inscription
# Dravidian harmony: consecutive words share front/back vowel quality
# Our Phase-61 check: uses the sequence approach
vowel_front = set("iīeē")
vowel_back = set("uūoō")
vowel_neutral = set("aā")

def get_vowel_class(reading):
    for ch in reading.lower():
        if ch in vowel_front: return "F"
        if ch in vowel_back: return "B"
        if ch in vowel_neutral: return "N"
    return "?"

harmony_seals = 0
harmony_pass = 0
harmony_violations = []
for form, signs in list(seal_groups.items())[:1000]:
    readings = [hm_readings.get(s, "") for s in signs if s in hm_readings and hm_readings.get(s, "") not in ("?", "")]
    if len(readings) < 2:
        continue
    classes = [get_vowel_class(r) for r in readings]
    classes = [c for c in classes if c != "?"]
    if len(classes) < 2:
        continue
    harmony_seals += 1
    # Harmony: no F-B or B-F transitions (N is neutral, compatible with both)
    violations_in_seal = 0
    for i in range(len(classes)-1):
        if (classes[i] == "F" and classes[i+1] == "B") or (classes[i] == "B" and classes[i+1] == "F"):
            violations_in_seal += 1
    if violations_in_seal == 0:
        harmony_pass += 1
    elif len(harmony_violations) < 3:
        harmony_violations.append(f"{form}: {list(zip(readings, classes))}")

harmony_rate = harmony_pass / harmony_seals if harmony_seals else 0
print(f"Harmony check (no F-B transitions): {harmony_pass}/{harmony_seals} = {harmony_rate:.3f} ({harmony_rate*100:.1f}%)")
print(f"Examples of violations: {harmony_violations[:3]}")
print(f"(Phase-61 target: >=85%; Phase-132 V12 used different method and got 74.6%)")
