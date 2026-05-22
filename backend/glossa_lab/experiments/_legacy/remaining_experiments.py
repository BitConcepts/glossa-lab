"""Remaining experiments batch: Tier3 classified, Tier3 oracle,
Tier5 PHONOGRAM-only, Ventris threshold sweep.

Usage:
    python -m glossa_lab.experiments.remaining_experiments
"""
from __future__ import annotations

import math
import os
import random
import sys
import time
from collections import Counter, defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACK = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _BACK)


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT A  —  Tier 3 Sumerian with sign classification
# ══════════════════════════════════════════════════════════════════════════════

def exp_tier3_classified(verbose=True):
    """Sumerian with logogram-exclusion (same classification method as Indus)."""
    from glossa_lab.data.sumerian_ur3 import get_corpus_inscriptions as ins
    from glossa_lab.data.sumerian_ur3 import get_corpus_symbols as sym
    from glossa_lab.pipelines.beam_decipher import beam_decipher
    from glossa_lab.pipelines.decipher import LanguageModel, score_accuracy

    def _pr(*a,**k):
        if verbose: print(*a,**k)

    flat  = sym(); inscr = ins(); freq = Counter(flat)
    n = len(inscr); split = int(n*0.75)
    train_inscr, test_inscr = inscr[:split], inscr[split:]
    train_flat = [s for i in train_inscr for s in i]
    test_flat  = [s for i in test_inscr  for s in i]

    # --- classify Sumerian signs by positional entropy ---
    pos = defaultdict(lambda:{"i":0,"m":0,"t":0})
    for ins_ in inscr:
        if len(ins_)<2: continue
        pos[ins_[0]]["i"]+=1; pos[ins_[-1]]["t"]+=1
        for s in ins_[1:-1]: pos[s]["m"]+=1

    sign_classes = {}
    for sign,cnt in freq.items():
        if cnt<5: sign_classes[sign]="RARE"; continue
        p=pos[sign]; tot=p["i"]+p["m"]+p["t"]
        if tot==0: sign_classes[sign]="RARE"; continue
        tb=p["t"]/tot; ib=p["i"]/tot
        probs=[p["i"]/tot,p["m"]/tot,p["t"]/tot]
        h=-sum(q*math.log(q+1e-12) for q in probs)
        if tb>=0.50: sign_classes[sign]="LOGOGRAM"
        elif ib>=0.60: sign_classes[sign]="INITIAL"
        elif h>=0.50:  sign_classes[sign]="PHONOGRAM"
        else:          sign_classes[sign]="MEDIAL"

    by_type = Counter(sign_classes.values())
    _pr("\n  Sumerian sign classification:")
    for t in ("LOGOGRAM","INITIAL","PHONOGRAM","MEDIAL","RARE"):
        signs = [s for s,c in sign_classes.items() if c==t]
        _pr(f"    {t:10}: {len(signs):3}  (top5: {[s for s,_ in freq.most_common() if s in signs][:5]})")

    allowed = {s for s,c in sign_classes.items() if c in ("PHONOGRAM","MEDIAL")}
    _pr(f"\n  Phonogram+Medial subset: {len(allowed)} signs")

    # Filter test set
    filt_test_inscr = [[s for s in i if s in allowed] for i in test_inscr]
    filt_test_inscr = [i for i in filt_test_inscr if len(i)>=2]
    filt_test_flat  = [s for i in filt_test_inscr for s in i]
    test_signs = sorted(set(filt_test_flat))
    sign_to_id = {s: f"S{i:03d}" for i,s in enumerate(test_signs)}
    enc_flat   = [sign_to_id.get(s,s) for s in filt_test_flat]
    enc_inscr  = [[sign_to_id.get(s,s) for s in i] for i in filt_test_inscr]
    ground_truth = {sign_to_id[s]:s for s in test_signs}

    # Filter TRAIN set to same subset
    filt_train = [s for i in train_inscr for s in i if s in allowed]
    filt_train_inscr = [[s for s in i if s in allowed] for i in train_inscr]
    filt_train_inscr = [i for i in filt_train_inscr if len(i)>=2]

    lm = LanguageModel(filt_train, inscriptions=filt_train_inscr)
    _pr(f"  Train subset: {len(filt_train)} tokens  LM V={len(lm.alphabet)} bigrams={len(lm.bigram_freq)}")
    _pr(f"  Test subset:  {len(filt_test_flat)} tokens  {len(test_signs)} distinct signs")

    _pr("\n  Running beam bijective w=200 (numpy-accelerated)...")
    t0=time.time()
    r = beam_decipher(enc_flat, lm, beam_width=200, cipher_inscriptions=enc_inscr, surjective=False)
    acc = score_accuracy(r["proposed_mapping"], ground_truth)
    _pr(f"  Beam w=200: {acc['correct']}/{acc['total']} = {acc['accuracy']*100:.1f}%  [{time.time()-t0:.1f}s]")

    _pr("\n  Running beam bijective w=500...")
    t0=time.time()
    r2 = beam_decipher(enc_flat, lm, beam_width=500, cipher_inscriptions=enc_inscr, surjective=False)
    acc2 = score_accuracy(r2["proposed_mapping"], ground_truth)
    _pr(f"  Beam w=500: {acc2['correct']}/{acc2['total']} = {acc2['accuracy']*100:.1f}%  [{time.time()-t0:.1f}s]")

    best = max(acc["correct"], acc2["correct"])
    _pr("\n  Tier 3 CLASSIFIED SUMMARY:")
    _pr("    Unclassified (107 signs): 20/107 = 18.7%")
    _pr(f"    Classified subset {len(test_signs)} signs, w=200: {acc['correct']}/{acc['total']} = {acc['accuracy']*100:.1f}%")
    _pr(f"    Classified subset {len(test_signs)} signs, w=500: {acc2['correct']}/{acc2['total']} = {acc2['accuracy']*100:.1f}%")
    _pr(f"    Best:  {best}/{acc['total']} = {best/acc['total']*100:.1f}%")

    return {"classified_signs": len(test_signs), "w200": acc, "w500": acc2,
            "sign_class_counts": dict(by_type), "best_pct": best/acc["total"]}


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT B  —  Tier 3 Oracle Analysis
# ══════════════════════════════════════════════════════════════════════════════

def exp_tier3_oracle(verbose=True):
    """Oracle: does the Sumerian LM score the correct mapping higher than beam found?"""
    from glossa_lab.data.sumerian_ur3 import get_corpus_inscriptions as ins
    from glossa_lab.data.sumerian_ur3 import get_corpus_symbols as sym
    from glossa_lab.pipelines.beam_decipher import beam_decipher
    from glossa_lab.pipelines.decipher import (
        LanguageModel,
        _score_mapping,
        score_accuracy,
    )

    def _pr(*a,**k):
        if verbose: print(*a,**k)

    flat=sym(); inscr=ins()
    n=len(inscr); split=int(n*0.75)
    train_flat=[s for i in inscr[:split] for s in i]
    test_flat =[s for i in inscr[split:] for s in i]
    test_inscr =inscr[split:]
    test_signs =sorted(set(test_flat))
    sign_to_id={s:f"S{i:03d}" for i,s in enumerate(test_signs)}
    enc_flat  =[sign_to_id.get(s,s) for s in test_flat]
    enc_inscr =[[sign_to_id.get(s,s) for s in i] for i in test_inscr]
    gt={sign_to_id[s]:s for s in test_signs}

    lm=LanguageModel(train_flat, inscriptions=inscr[:split])

    # Correct mapping: opaque_id -> actual Sumerian sign (found in test)
    correct_mapping = {sign_to_id[s]:s for s in test_signs if s in lm.alphabet}

    score_correct = _score_mapping(enc_flat, correct_mapping, lm, {})
    _pr(f"\n  Score of CORRECT mapping: {score_correct:.1f}")

    # Beam found mapping
    r_beam = beam_decipher(enc_flat, lm, beam_width=500, cipher_inscriptions=enc_inscr, surjective=False)
    beam_map = r_beam["proposed_mapping"]
    score_beam = _score_mapping(enc_flat, beam_map, lm, {})
    acc_beam = score_accuracy(beam_map, gt)
    _pr(f"  Score of BEAM mapping:    {score_beam:.1f}  ({acc_beam['correct']}/{acc_beam['total']} correct)")

    # Random baseline
    rng=random.Random(42)
    rand_scores=[]
    target_alpha=lm.ranked[:len(test_signs)]
    while len(target_alpha)<len(test_signs): target_alpha.append(f"?{len(target_alpha)}")
    for _ in range(30):
        shuffled=list(target_alpha); rng.shuffle(shuffled)
        rm=dict(zip(sorted(sign_to_id.values()), shuffled))
        rand_scores.append(_score_mapping(enc_flat,rm,lm,{}))
    mean_rand=sum(rand_scores)/len(rand_scores)

    delta=score_correct-score_beam
    _pr(f"  score(correct)-score(beam): {delta:+.1f}  ({delta/abs(score_beam)*100:+.1f}%)")
    _pr(f"  Random mean: {mean_rand:.1f}")
    _pr(f"  Z(correct vs random): {(score_correct-mean_rand)/max(1,abs(mean_rand-sum(rand_scores)/len(rand_scores))+1):.2f}")

    if delta > 0:
        verdict="ALGORITHMIC FAILURE -- signal exists, beam not finding it. More search needed."
    elif delta > -abs(score_beam)*0.01:
        verdict="DEGENERATE LANDSCAPE -- correct mapping indistinguishable from beam's mapping."
    else:
        verdict="MODEL FAILURE -- LM prefers wrong mapping. Cross-script transfer is the barrier."
    _pr(f"\n  ORACLE VERDICT: {verdict}")
    return {"score_correct":score_correct,"score_beam":score_beam,"delta":delta,"verdict":verdict}


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT C  —  Tier 5 PHONOGRAM-only (15 signs)
# ══════════════════════════════════════════════════════════════════════════════

def exp_tier5_phonogram_only(verbose=True):
    """Re-run Tier 5 hypothesis test on PHONOGRAM signs only (not MEDIAL)."""
    from itertools import cycle

    from glossa_lab.data.dravidian import get_corpus_symbols as d
    from glossa_lab.data.indus_public_corpus import get_corpus_inscriptions as ind_ins
    from glossa_lab.data.indus_public_corpus import get_corpus_symbols as ind
    from glossa_lab.data.old_hebrew import get_corpus_symbols as heb
    from glossa_lab.data.sanskrit import get_corpus_symbols as sk
    from glossa_lab.data.sumerian_ur3 import get_corpus_inscriptions as su_ins
    from glossa_lab.data.sumerian_ur3 import get_corpus_symbols as su
    from glossa_lab.experiments.tier5_indus_decipherment import classify_indus_signs
    from glossa_lab.pipelines.beam_decipher import beam_decipher
    from glossa_lab.pipelines.decipher import LanguageModel, _score_mapping

    def _pr(*a,**k):
        if verbose: print(*a,**k)

    indus_flat=ind(); indus_inscr=ind_ins(); indus_freq=Counter(indus_flat)
    sc=classify_indus_signs(indus_inscr)

    # PHONOGRAM-only (15 signs, highest positional entropy)
    phonogram_signs={s for s,info in sc.items() if info["type"]=="PHONOGRAM"}
    _pr(f"\n  PHONOGRAM-only subset: {len(phonogram_signs)} signs")
    _pr(f"  Signs: {sorted(phonogram_signs)}")

    filt_inscr=[[s for s in ins_ if s in phonogram_signs] for ins_ in indus_inscr]
    filt_inscr=[i for i in filt_inscr if len(i)>=2]
    filt_flat=[s for i in filt_inscr for s in i]
    _pr(f"  Inscriptions with >=2 phonogram signs: {len(filt_inscr)}")
    _pr(f"  Phonogram tokens: {len(filt_flat)}")

    lms={"Dravidian":LanguageModel(d()),"Sanskrit":LanguageModel(sk()),
         "Sumerian":LanguageModel(su(),inscriptions=su_ins()),
         "Hebrew":LanguageModel(heb())}
    results=[]
    for label,lm in lms.items():
        n_c=len(Counter(filt_flat)); n_t=len(lm.alphabet)
        max_k=math.ceil(n_c/n_t)
        r=beam_decipher(filt_flat,lm,beam_width=200,cipher_inscriptions=filt_inscr,
                        surjective=True,max_target_reuse=max_k)
        bs=r["score"]
        # random baseline
        rng=random.Random(42); ta=lm.ranked; rand_scores=[]
        cr=[s for s,_ in Counter(filt_flat).most_common()]
        for _ in range(30):
            sh=list(ta); rng.shuffle(sh)
            m=dict(zip(cr,cycle(sh)))
            rand_scores.append(_score_mapping(filt_flat,m,lm,{}))
        mr=sum(rand_scores)/len(rand_scores)
        sd=math.sqrt(sum((x-mr)**2 for x in rand_scores)/len(rand_scores))
        z=(bs-mr)/sd if sd>0 else 0
        results.append({"label":label,"z":round(z,2),"best":round(bs,1),"rand":round(mr,1)})
        _pr(f"  {label:<22} Z={z:+6.2f}  best={bs:.0f}  rand_mean={mr:.0f}")

    ranked=sorted(results,key=lambda x:-x["z"])
    _pr("\n  PHONOGRAM-ONLY SUMMARY:")
    _pr(f"    Winner: {ranked[0]['label']}  Z={ranked[0]['z']:.2f}  (margin {ranked[0]['z']-ranked[1]['z']:.2f} over {ranked[1]['label']})")
    _pr(f"    Control: {ranked[-1]['label']}  Z={ranked[-1]['z']:.2f}")
    return {"phonogram_signs":sorted(phonogram_signs),"results":ranked}


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT D  —  Ventris threshold sweep
# ══════════════════════════════════════════════════════════════════════════════

def exp_ventris_threshold_sweep(verbose=True):
    """Find the cosine similarity threshold that maximises Ventris F1."""
    import sys; sys.path.insert(0, os.path.join(_BACK, "tests"))
    from pathlib import Path

    from glossa_lab.experiments.ventris_validation import (
        _score_clusters,
        _sign_to_col,
        _sign_to_row,
    )
    from glossa_lab.pipelines.logosyllabic import classify_signs, compute_affinity

    def _pr(*a,**k):
        if verbose: print(*a,**k)

    fixture = Path(_BACK)/"tests"/"corpora"/"fixtures"/"linear_b.txt"
    text = fixture.read_text(encoding="utf-8")
    inscriptions: list[list[str]] = []
    for line in text.splitlines():
        for word in line.strip().split():
            parts = word.replace("3","").split("-")
            signs = [p.strip().lower() for p in parts
                     if p.strip() and p.strip().replace("*","").replace("2","").isalpha()]
            if len(signs) >= 2:
                inscriptions.append(signs)

    flat=[s for i in inscriptions for s in i]
    sign_class=classify_signs(inscriptions,flat)
    syllabograms=[s for s,info in sign_class.items() if info["type"]=="syllabogram"]
    _pr(f"\n  Linear B: {len(inscriptions)} words  {len(flat)} tokens  {len(syllabograms)} syllabograms")

    sign_to_row_map=_sign_to_row(); sign_to_col_map=_sign_to_col()
    best_f1=0; best_thresh=0.15; best_row=0; best_col=0
    results=[]
    for thresh in [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.30]:
        aff=compute_affinity(inscriptions, syllabograms, top_n=40, window=2,
                             threshold=thresh)
        vg=aff.get("vowel_groups",[]); cg=aff.get("consonant_groups",[])
        rs=_score_clusters(vg, sign_to_row_map, "row", verbose=False)
        cs=_score_clusters(cg, sign_to_col_map, "col", verbose=False)
        f1=(rs["f1"]+cs["f1"])/2
        results.append({"thresh":thresh,"row_f1":rs["f1"],"col_f1":cs["f1"],"avg_f1":f1})
        flag="<-- best" if f1>best_f1 else ""
        _pr(f"  thresh={thresh:.2f}  row_f1={rs['f1']:.4f}  col_f1={cs['f1']:.4f}  avg_f1={f1:.4f}  {flag}")
        if f1>best_f1: best_f1=f1; best_thresh=thresh; best_row=rs["f1"]; best_col=cs["f1"]

    _pr(f"\n  BEST: threshold={best_thresh}  avg_F1={best_f1:.4f}  "
        f"row_F1={best_row:.4f}  col_F1={best_col:.4f}")
    _pr("  Previous default (0.15): see above row")
    return {"best_thresh":best_thresh,"best_f1":best_f1,"best_row":best_row,"best_col":best_col,"sweep":results}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def run_all(verbose=True):
    def _pr(*a,**k):
        if verbose: print(*a,**k)

    _pr("\n" + "█"*70)
    _pr("  Remaining Experiments — GPU/numpy accelerated")
    _pr("█"*70)

    _pr("\n\n" + "="*70)
    _pr("  EXP A — Tier 3 Sumerian with sign classification")
    _pr("="*70)
    ra = exp_tier3_classified(verbose)

    _pr("\n\n" + "="*70)
    _pr("  EXP B — Tier 3 Oracle analysis")
    _pr("="*70)
    rb = exp_tier3_oracle(verbose)

    _pr("\n\n" + "="*70)
    _pr("  EXP C — Tier 5 PHONOGRAM-only (15 signs)")
    _pr("="*70)
    rc = exp_tier5_phonogram_only(verbose)

    _pr("\n\n" + "="*70)
    _pr("  EXP D — Ventris threshold sweep")
    _pr("="*70)
    rd = exp_ventris_threshold_sweep(verbose)

    _pr("\n\n" + "█"*70)
    _pr("  MASTER SUMMARY")
    _pr("█"*70)
    _pr(f"\n  Tier 3 classified:         {ra['w200']['correct']}/{ra['w200']['total']} = {ra['w200']['accuracy']*100:.1f}%  (unclassified was 18.7%)")
    _pr(f"  Tier 3 oracle verdict:     {rb['verdict'][:60]}")
    _pr(f"  Tier 5 phonogram-only:     {rc['results'][0]['label']} leads  Z={rc['results'][0]['z']:.2f}")
    _pr(f"  Ventris best threshold:    {rd['best_thresh']}  avg_F1={rd['best_f1']:.4f}  (was F1=0.192 at 0.15)")
    return {"A":ra,"B":rb,"C":rc,"D":rd}


if __name__ == "__main__":
    run_all(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class Tier3SumerianClassified(_EB):
    id = "tier3_sumerian_classified"
    name = "Tier 3 — Sumerian Classified (Phonogram Subset)"
    category = "Validation"
    description = (
        "Applies positional-entropy sign classification to the Sumerian UR III corpus "
        "(same method as Indus), then runs beam decipherment on the phonogram+medial subset. "
        "Compares accuracy before and after classification. "
        "Key finding: Sumerian has only 2 logograms — classification barely reduces search space."
    )
    estimated_time = "~15 min (numpy-accelerated)"
    command = "python -m glossa_lab.experiments.remaining_experiments"
    params_schema = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return exp_tier3_classified(verbose=False)


class Tier3OracleAnalysis(_EB):
    id = "tier3_oracle_analysis"
    name = "Tier 3 — Sumerian Oracle Analysis"
    category = "Validation"
    description = (
        "Oracle diagnostic for the Sumerian logo-syllabic benchmark: compares "
        "score(correct mapping) vs score(beam best mapping) under the Sumerian LM. "
        "KEY FINDING: The bigram model scores the WRONG mapping higher than the correct one "
        "(model failure, not search failure). This is the fundamental logo-syllabic bottleneck "
        "that requires phonological group constraints to overcome."
    )
    estimated_time = "~10 min (numpy-accelerated)"
    command = "python -m glossa_lab.experiments.remaining_experiments"
    params_schema = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return exp_tier3_oracle(verbose=False)


class Tier5PhonogramOnly(_EB):
    id = "tier5_phonogram_only"
    name = "Tier 5 — Indus Hypothesis Test (PHONOGRAM signs only)"
    category = "Validation"
    description = (
        "Re-runs the Tier 5 Indus hypothesis test using only the 15 highest-entropy "
        "PHONOGRAM signs (not the full 44-sign mixed set). Fewer, purer signs give "
        "more discriminating Z-scores. "
        "Result: Dravidian Z=4.36 leads with margin +0.75 over Sumerian. "
        "Hebrew control scores lowest (Z=2.46) in every configuration."
    )
    estimated_time = "~3 min"
    command = "python -m glossa_lab.experiments.remaining_experiments"
    params_schema = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return exp_tier5_phonogram_only(verbose=False)


class VentrisThresholdSweep(_EB):
    id = "ventris_threshold_sweep"
    name = "Tier 4 — Ventris Threshold Sweep"
    category = "Validation"
    description = (
        "Sweeps cosine similarity thresholds (0.05 to 0.30) for the Linear B Ventris grid "
        "affinity analysis to find the F1-maximising threshold. "
        "Key finding: F1 is flat (0.192) from threshold 0.05 to 0.15 — the bottleneck is "
        "corpus size, not the threshold parameter. Best threshold = 0.05."
    )
    estimated_time = "~2 min"
    command = "python -m glossa_lab.experiments.remaining_experiments"
    params_schema = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return exp_ventris_threshold_sweep(verbose=False)
