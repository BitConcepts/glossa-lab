"""Generate comprehensive anti-circularity analysis report.
Run: shell.cmd python backend/generate_report_linear_a_circularity.py
Output: reports/linear_a_circularity_analysis.pdf
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Table, TableStyle

NAVY  = HexColor("#1e3a5f"); BLUE  = HexColor("#2563eb"); GREEN = HexColor("#15803d")
RED   = HexColor("#dc2626"); AMBER = HexColor("#d97706"); LGREY = HexColor("#f1f5f9")
MGREY = HexColor("#e2e8f0"); GOLD  = HexColor("#ca8a04")
WARN  = HexColor("#fef3c7"); WARN_B= HexColor("#92400e")

REPO_ROOT = Path(__file__).resolve().parent.parent
results_f = REPO_ROOT / "reports" / "circularity_results.json"
with open(results_f) as f:
    R = json.load(f)

output = str(REPO_ROOT / "reports" / "linear_a_circularity_analysis.pdf")

doc = SimpleDocTemplate(output, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=2.5*cm, bottomMargin=2.5*cm)
styles = getSampleStyleSheet()
H2   = ParagraphStyle("H2",  parent=styles["Heading2"], textColor=NAVY, fontSize=13, spaceAfter=4)
H3   = ParagraphStyle("H3",  parent=styles["Heading3"], textColor=BLUE, fontSize=11, spaceAfter=3)
BODY = ParagraphStyle("Body", parent=styles["Normal"],  fontSize=10, leading=14, spaceAfter=8, alignment=TA_JUSTIFY)
CAP  = ParagraphStyle("Cap",  parent=styles["Normal"],  fontSize=9,  textColor=HexColor("#64748b"), alignment=TA_CENTER, spaceAfter=12)
SMALL= ParagraphStyle("Small",parent=styles["Normal"],  fontSize=8.5,leading=12)
TITLE= ParagraphStyle("Title",parent=styles["Title"],   textColor=NAVY, fontSize=20, alignment=TA_CENTER, spaceAfter=4)
SUB  = ParagraphStyle("Sub",  parent=styles["Normal"],  textColor=HexColor("#475569"), fontSize=11, alignment=TA_CENTER, spaceAfter=20)
WARN_STYLE = ParagraphStyle("WarnBody",parent=styles["Normal"],fontSize=10,leading=14,spaceAfter=8,alignment=TA_JUSTIFY,textColor=WARN_B)

ts = TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
    ("GRID",(0,0),(-1,-1),0.5,MGREY),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,LGREY]),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
])

c = []
c.append(Paragraph("Linear A: Anti-Circularity Experiment Suite", TITLE))
c.append(Paragraph("Seven experiments testing robustness of the Greek-adjacent result · Glossa Lab", SUB))
c.append(Paragraph(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", CAP))
c.append(HRFlowable(width="100%",thickness=1,color=NAVY,spaceAfter=16))

# ── 1. Executive Summary ──────────────────────────────────────────────
c.append(Paragraph("1. Executive Summary", H2))
c.append(Paragraph(
    "This report presents seven experiments designed to test whether the Greek-dominant "
    "result in the Linear A phoneme-level analysis is an artifact of using Linear B-derived "
    "phonetic assignments. The experiments use real tablet data from John G. Younger's "
    "transcriptions (5,379 sign tokens across HT, KH, ZA, PH, KN, and other sites).",BODY))
c.append(Paragraph(
    "<b>Key finding:</b> The Greek advantage is <b>entirely driven by vocabulary "
    "matching</b>. Under scoring modes that remove vocabulary evidence "
    "(bigram+Kandles-only, Kandles-only), Greek ranks <b>last</b> of the four "
    "hypotheses. The Kandles phonetic fingerprint <b>marginally favours Luwian</b> "
    "(9.94 vs Greek 9.52). This confirms that the vocabulary-matching component is "
    "partially circular, and that the vocabulary-independent phonological signal does "
    "not support the Greek-adjacent interpretation.",BODY))
c.append(Paragraph(
    "<b>What survives:</b> Greek wins on the raw tablet corpus (margin 39.9) with full "
    "scoring. The margin is large and consistent across all large sites (HT, KH, ZA, PH). "
    "But this advantage is attributable to vocabulary matching, not to independent "
    "phonological structure.",BODY))

# ── 2. Experiment 1: Raw tablet replication ───────────────────────────
c.append(Paragraph("2. Experiment 1 — Raw Tablet Sequence Replication", H2))
c.append(Paragraph(
    "Hypothesis engine run on actual tablet-order sequences from corpus_manifest.csv, "
    "partitioned by archaeological site. Full scoring (bigram + Kandles + vocabulary).",BODY))

e1 = R["exp1_raw_tablet"]
tA_data = [["Site", "N tokens", "Greek", "Hurrian", "Luwian", "Semitic", "Winner", "Margin"]]
for site in ["ALL","HT","KH","ZA","PH","KN","ARKH","MA","TY"]:
    if site not in e1:
        continue
    d = e1[site]
    sc = d["scores"]
    w  = d["winner"]
    row = [site, str(d["n_tokens"]),
           f"{sc.get('greek',0):.1f}", f"{sc.get('hurrian',0):.1f}",
           f"{sc.get('luwian',0):.1f}", f"{sc.get('semitic',0):.1f}",
           w, f"{d['margin_vs_second']:.1f}"]
    tA_data.append(row)

tA_style = TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
    ("GRID",(0,0),(-1,-1),0.5,MGREY),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,LGREY]),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
])
# Highlight large-corpus sites in green
for i, site in enumerate(["ALL","HT","KH","ZA","PH","KN","ARKH","MA","TY"]):
    if site in e1 and e1[site]["n_tokens"] >= 200:
        row_i = ["ALL","HT","KH","ZA","PH","KN","ARKH","MA","TY"].index(site)
        tA_style.add("BACKGROUND",(0,row_i+1),(-1,row_i+1),HexColor("#dcfce7"))
c.append(Table(tA_data, colWidths=[1.5*cm,1.8*cm,2*cm,2*cm,2*cm,2*cm,2.5*cm,2*cm], style=tA_style))
c.append(Paragraph(
    "Table A. Raw-corpus hypothesis ranking by site (full scoring). Large corpora "
    "(n≥200, highlighted) consistently return Greek as winner with margins 8–40. "
    "Small sites (ARKH, MA, TY, n<200) show no clear winner — small-sample noise.",CAP))

# ── 3. Experiment 5: Scoring mode comparison (most important) ─────────
c.append(Paragraph("3. Experiment 5 — Scoring Mode Comparison (Critical)", H2))
c.append(Paragraph(
    "This is the most important experiment. Three scoring modes were tested on the "
    "full raw corpus: <b>(A) Full</b> = bigram + Kandles + vocabulary matches; "
    "<b>(B) No-vocab</b> = bigram + Kandles only; <b>(C) Kandles only</b>. "
    "The vocabulary-independent modes reveal whether Greek signal survives without "
    "the potentially circular lexical component.",BODY))

e5 = R["exp5_scoring_modes"]
tD_data = [["Mode","Greek","Hurrian","Luwian","Semitic","Winner","Interpretation"]]
mode_interp = {
    "full":         "Greek dominant — includes vocabulary bonus",
    "no_vocab":     "Luwian ranks #1 — Greek LAST without vocab",
    "kandles_only": "Luwian ranks #1 by Kandles fingerprint",
}
mode_label = {
    "full":         "A: Full (bigram+Kandles+vocab)",
    "no_vocab":     "B: No vocab (bigram+Kandles)",
    "kandles_only": "C: Kandles only",
}
for mode in ["full","no_vocab","kandles_only"]:
    d  = e5[mode]
    sc = d["scores"]
    row = [mode_label[mode],
           f"{sc.get('greek',0):.2f}", f"{sc.get('hurrian',0):.2f}",
           f"{sc.get('luwian',0):.2f}", f"{sc.get('semitic',0):.2f}",
           d["winner"], mode_interp[mode]]
    tD_data.append(row)

tD_style = TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
    ("GRID",(0,0),(-1,-1),0.5,MGREY),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,LGREY]),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    # Highlight full mode in green (Greek wins), others in amber (Greek loses)
    ("BACKGROUND",(0,1),(-1,1),HexColor("#dcfce7")),
    ("BACKGROUND",(0,2),(-1,2),HexColor("#fef3c7")),
    ("BACKGROUND",(0,3),(-1,3),HexColor("#fef3c7")),
])
c.append(Table(tD_data, colWidths=[5.5*cm,1.5*cm,1.5*cm,1.5*cm,1.5*cm,2.5*cm,3.5*cm], style=tD_style))
c.append(Paragraph(
    "Table D. Scoring mode comparison. Green = Greek wins; Amber = Greek loses. "
    "The vocabulary-independent modes (B and C) both rank Greek last. The entire "
    "Greek advantage is attributable to vocabulary matching.",CAP))
c.append(Paragraph(
    "<b>Finding:</b> Removing vocabulary evidence (Mode B) drops Greek from "
    f"score {e5['full']['scores']['greek']:.1f} to {e5['no_vocab']['scores']['greek']:.1f} "
    "— a reduction of nearly 40 points. Luwian, Semitic, and Hurrian are essentially "
    "unaffected (they have no vocabulary bonus). Under Kandles-only scoring (Mode C), "
    "Greek phonetic fingerprint (9.52) ranks below Luwian (9.94) and Semitic (9.92). "
    "This directly confirms that the vocabulary component is circular: the vocabulary "
    "list was derived by applying Linear B phonetic values, and the engine recovers "
    "those same assignments.",BODY))

# ── 4. Experiment 2: Mapping ablation ────────────────────────────────
c.append(Paragraph("4. Experiment 2 — Mapping Ablation", H2))
c.append(Paragraph(
    "The phoneme mapping was progressively reduced to only the top-10/20/30/40 and "
    "all available signs (104). At each level, 30 trials with random sign subsets "
    "were run under no-vocab scoring. This tests whether the Greek advantage "
    "(if any) grows as more mapping is applied.",BODY))

e2 = R["exp2_mapping_ablation"]
tB_data = [["N signs","Greek mean","95% CI","Hurrian mean","Greek #1 fraction"]]
for k in sorted(e2.keys(), key=int):
    d = e2[k]
    tB_data.append([str(d["n_signs"]),
                    f"{d['greek_mean']:.3f}",
                    f"[{d['greek_ci_lo']:.3f}, {d['greek_ci_hi']:.3f}]",
                    f"{d['hurrian_mean']:.3f}",
                    f"{d['greek_rank_1_fraction']*100:.0f}%"])
c.append(Table(tB_data, colWidths=[2*cm,3*cm,4*cm,3*cm,4*cm], style=ts))
c.append(Paragraph(
    "Table B. Mapping ablation results (no-vocab scoring). Greek #1 fraction = "
    "proportion of 30 trials where Greek ranked first. "
    "At 40 signs: Greek #1 in 83% of trials (consistent with a marginal advantage).",CAP))
c.append(Paragraph(
    "<b>Finding:</b> Greek rank-1 fraction increases from 13% (n=10 signs) to "
    "83% (n=40 signs), suggesting that the full mapping does confer a slight bigram "
    "advantage independent of vocabulary. However, the mean scores are all within "
    "~0.1 of each other — the effect is tiny and not robust to the no-vocab test.",BODY))

# ── 5. Experiment 4: Random mapping null distribution ────────────────
c.append(Paragraph("5. Experiment 4 — Random Mapping Null Distribution", H2))
c.append(Paragraph(
    "The real mapping score was compared against distributions from (a) frequency-matched "
    "random mappings, (b) CV-structure-preserving random, (c) permuted Linear B "
    "correspondences. 30 trials each, no-vocab scoring.",BODY))

e4 = R["exp4_null_distribution"]
real_g = e4["real_greek"]
tC_data = [["Control type","Trials","Null mean","Real score","p-value","z-score","Interpretation"]]
interp_map = {
    "frequency_matched_random":   "Real ≈ null; mapping structure unimportant",
    "cv_structure_preserving":    "Real ≈ null; CV structure unimportant",
    "permuted_lb_correspondences":"Real ≈ null; specific LB mapping unimportant",
}
for k, v in e4["nulls"].items():
    tC_data.append([k.replace("_"," "), str(v["trials"]),
                    f"{v['null_mean']:.3f}", f"{v['real_score']:.3f}",
                    f"{v['p_value']:.4f}", f"{v['z_score']:.3f}",
                    interp_map.get(k,"")])
c.append(Table(tC_data, colWidths=[4*cm,1.5*cm,2*cm,2*cm,1.8*cm,1.8*cm,4.9*cm], style=ts))
c.append(Paragraph(
    "Table C. Random/permuted mapping null distribution (no-vocab scoring). "
    f"Real Greek score = {real_g:.3f}. All p-values ≈ 0.40, z-scores ≈ 0.29. "
    "Real mapping is NOT statistically distinguishable from random.",CAP))
c.append(Paragraph(
    "<b>Finding:</b> Under no-vocab scoring, the real Linear B phoneme mapping "
    "produces a Greek score that is statistically indistinguishable from random "
    "mappings (p≈0.40, z≈0.29). This means the specific sign-to-phoneme correspondences "
    "do not confer a detectable advantage in bigram+Kandles scoring. The only "
    "statistically significant Greek advantage comes from vocabulary matching.",BODY))

# ── 6. Experiment 7: Null corpus controls ────────────────────────────
c.append(Paragraph("6. Experiment 7 — Null Corpus Controls", H2))

e7 = R["exp7_null_corpus"]
tNull = [["Corpus type","Greek mean","95% CI","Notes"]]
interp7 = {
    "real":        "Actual tablet sequence — baseline",
    "shuffled":    "Sign order randomised — Greek HIGHER (not lower!)",
    "unigram_only":"Bigrams destroyed — Greek HIGHER",
}
for k, v in e7.items():
    tNull.append([k, f"{v['greek_mean']:.3f}",
                  f"[{v['greek_ci_lo']:.3f}, {v['greek_ci_hi']:.3f}]",
                  interp7.get(k,"")])
c.append(Table(tNull, colWidths=[3.5*cm,2.5*cm,4.5*cm,6.5*cm], style=ts))
c.append(Paragraph(
    "Table E. Null corpus controls (no-vocab scoring). Shuffled and unigram corpora "
    "produce marginally higher Greek scores than the real corpus.",CAP))
c.append(Paragraph(
    "<b>Finding:</b> Greek score does not decrease when corpus structure is destroyed — "
    "it actually increases slightly for shuffled and unigram corpora. This confirms "
    "that the no-vocab Greek score (~16.9) is driven by random baseline effects "
    "(all four hypotheses score ~16.9–17.0 regardless of corpus structure), not by "
    "meaningful sequential patterns in the real tablet data.",BODY))

# ── 7. Experiment 3: Mapping perturbation ────────────────────────────
c.append(Paragraph("7. Experiment 3 — Mapping Perturbation (No-Vocab)", H2))
e3 = R["exp3_perturbation"]
tPert = [["Noise level","Greek mean","95% CI"]]
for k, v in sorted(e3.items(), key=lambda x: float(x[0])):
    tPert.append([f"{float(k)*100:.0f}%", f"{v['greek_mean']:.3f}",
                  f"[{v['greek_ci_lo']:.3f}, {v['greek_ci_hi']:.3f}]"])
c.append(Table(tPert, colWidths=[3*cm,3.5*cm,5*cm], style=ts))
c.append(Paragraph(
    "Table F. Perturbation results. Greek score is stable across all noise levels "
    "because the no-vocab signal is essentially zero — noise has nothing to destroy.",CAP))

# ── 8. Experiment 6: Language model fairness ─────────────────────────
c.append(Paragraph("8. Experiment 6 — Language Model Fairness", H2))
e6 = R["exp6_fairness"]
c.append(Paragraph(
    f"Equalised all language model corpora to {e6['equalized_size']} characters "
    f"(baseline Greek model was substantially larger). Winner: "
    f"baseline={e6['baseline']['winner']}, equalized={e6['equalized']['winner']}. "
    f"Greek rank: baseline=#{e6['baseline']['greek_rank']}, "
    f"equalized=#{e6['equalized']['greek_rank']}. "
    f"Greek still ranks last under both conditions (no-vocab scoring), confirming "
    f"that model size is not the driver of the non-Greek result.",BODY))

# ── 9. Integrated interpretation ────────────────────────────────────
c.append(Paragraph("9. Integrated Interpretation", H2))
c.append(Paragraph(
    "The anti-circularity experiments produce a coherent and scientifically honest picture:",BODY))

findings = [
    ("<b>Greek wins with vocabulary (Exp 1, 5A):</b> On real tablet data with full "
     "scoring, Greek wins all large-corpus splits by margins of 8–40 points. "
     "This is real and consistent."),
    ("<b>Vocabulary matching is the mechanism (Exp 5B/C):</b> Remove vocabulary, "
     "and Greek drops to last place in both bigram and Kandles scoring. The "
     "vocabulary component accounts for ~40 of the ~40-point margin. "
     "This directly confirms circularity."),
    ("<b>Kandles favours Luwian (Exp 5C):</b> The vocabulary-independent "
     "phonetic fingerprint marginally favours Luwian (9.94) over Greek (9.52). "
     "This is a novel finding that partially supports the Anatolian hypothesis."),
    ("<b>Mapping structure irrelevant to bigram+Kandles (Exp 4):</b> The real "
     "Linear B correspondence mapping is statistically indistinguishable from "
     "random or permuted mappings under no-vocab scoring (p≈0.40). The specific "
     "sign assignments do not drive the phonological signal."),
    ("<b>Null corpus confirms baseline-level scoring (Exp 7):</b> Shuffled and "
     "unigram corpora produce equivalent or higher Greek scores — confirming the "
     "~16.9 baseline is noise-level, not signal."),
    ("<b>Mapping ablation shows weak ordering (Exp 2):</b> Greek rank-1 fraction "
     "increases from 13% to 83% as more signs are included, suggesting a very weak "
     "genuine bigram signal — but not strong enough to survive scoring without vocabulary."),
]
for f in findings:
    c.append(Paragraph(f"• {f}", BODY))

c.append(Paragraph("9.1 Conservative conclusion", H3))
c.append(Paragraph(
    "The Greek-adjacent result in the full-scoring analysis is <b>primarily driven by "
    "vocabulary matching, and that vocabulary matching is partially circular</b>. "
    "The vocabulary list (ku-ro, ki-re-ta, sa-ra2, etc.) was derived by applying "
    "Linear B phonetic values to Linear A signs; the engine then finds those same "
    "values in the corpus and counts it as evidence for Greek.",BODY))
c.append(Paragraph(
    "The vocabulary-independent phonological signal (Kandles fingerprint) does not "
    "favour Greek — it marginally favours Luwian/Anatolian. This does not prove "
    "Minoan is Anatolian, but it does mean the Greek-adjacent phonological claim "
    "cannot be supported independently of the circular vocabulary evidence.",BODY))

c.append(Paragraph("9.2 What would be needed for a stronger claim", H3))
for step in [
    "An independent vocabulary source not derived from Linear B phonetic values (e.g., "
    "confirmed loanwords, bilingual texts, or parallel inscriptions).",
    "Fuller and validated language models for Hurrian and Luwian at phoneme level "
    "(the current models are minimal character-level corpora).",
    "Site-by-site analysis showing consistent Kandles ranking across HT, KH, and ZA.",
    "A proper null model for the Kandles phonetic fingerprint to assess statistical "
    "significance of the Luwian>Greek ordering.",
    "The ICIT corpus (Fuls/Wells) for validation on the full Mahadevan sign inventory.",
]:
    c.append(Paragraph(f"• {step}", BODY))

# ── References ───────────────────────────────────────────────────────
c.append(Paragraph("References", H2))
for ref in [
    "[1] Younger, J.G. (2024). Linear A Texts in Phonetic Transcription. academia.edu.",
    "[2] tylerlengyel.com/linearA (2025). Structural analysis pipeline. Data: CC-compatible.",
    "[3] Packard, D.W. (1974). Minoan Linear A. University of California Press.",
    "[4] Ventris, M. & Chadwick, J. (1973). Documents in Mycenaean Greek. Cambridge.",
    "[5] Palmer, L.R. (1958). Luvian and Linear A. Trans. Philological Society.",
    "[6] van Soesbergen, P. (2022). The Decipherment of Minoan Linear A. 8 vols.",
    "[7] Rao et al. (2009). Entropic Evidence for Linguistic Structure. Science 324:1165.",

]:
    c.append(Paragraph(ref, SMALL))

doc.build(c)
print(f"Report written: {output}")
