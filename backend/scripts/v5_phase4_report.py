"""
V5 Phase 4: Register experiment graphs + email comprehensive report.
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REPORT_DIR = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports")
GRAPHS_DIR = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\glossa_lab\experiments\graphs")
RECIPIENT = "tpierson@bitconcepts.tech"


def register_v5_graphs():
    """Register V5 experiment graph JSONs."""
    graphs = [
        {
            "id": "indus_v5_spectral_grid",
            "name": "Indus V5 — Spectral Syllabic Grid",
            "description": "Spectral clustering (normalized Laplacian) on co-substitution matrix of 151 frequent signs from 1,670 Holdat corpus seals. Tests for consonant×vowel grid structure. Result: 10 clusters with positional specialization (Initial/Medial/Terminal) rather than C×V.",
            "auto_migrated": False,
            "nodes": [
                {"id": "load", "type": "expNode", "data": {"atomicId": "HoldatCorpusLoader", "label": "Load Holdat 1670", "params": {}}, "position": {"x": 60, "y": 200}},
                {"id": "cosub", "type": "expNode", "data": {"atomicId": "CoSubstitutionMatrix", "label": "Co-sub matrix (bigram contexts)", "params": {"freq_threshold": 5}}, "position": {"x": 360, "y": 200}},
                {"id": "spectral", "type": "expNode", "data": {"atomicId": "SpectralClustering", "label": "Spectral clustering (k=4..10)", "params": {"k_range": [4, 5, 6, 7, 8, 10]}}, "position": {"x": 660, "y": 200}},
                {"id": "out", "type": "expNode", "data": {"atomicId": "JSONExport", "label": "Save spectral grid", "params": {"filename": "INDUS_V5_SPECTRAL_GRID.json"}}, "position": {"x": 960, "y": 200}}
            ],
            "edges": [
                {"id": "e1", "source": "load", "target": "cosub", "sourcePort": "corpus", "targetPort": "corpus"},
                {"id": "e2", "source": "cosub", "target": "spectral", "sourcePort": "matrix", "targetPort": "matrix"},
                {"id": "e3", "source": "spectral", "target": "out", "sourcePort": "grid", "targetPort": "data"}
            ]
        },
        {
            "id": "indus_v5_anchor_validation",
            "name": "Indus V5 — Anchor Validation (SNR test)",
            "description": "Decode top-50 longest inscriptions with 12 anchors. Scrambled control: randomly select 12 different signs as fake anchors across 100 trials. Real decode=57.1%, scrambled=11.3%±5.7%, SNR=8.02.",
            "auto_migrated": False,
            "nodes": [
                {"id": "load", "type": "expNode", "data": {"atomicId": "HoldatCorpusLoader", "label": "Load Holdat 1670", "params": {}}, "position": {"x": 60, "y": 200}},
                {"id": "decode", "type": "expNode", "data": {"atomicId": "AnchorDecoder", "label": "Decode with 12 anchors", "params": {"n_longest": 50}}, "position": {"x": 360, "y": 200}},
                {"id": "control", "type": "expNode", "data": {"atomicId": "ScrambledControl", "label": "Scrambled control (100 trials)", "params": {"n_trials": 100}}, "position": {"x": 660, "y": 200}},
                {"id": "out", "type": "expNode", "data": {"atomicId": "JSONExport", "label": "Save validation", "params": {"filename": "INDUS_V5_PHASES_1_3.json"}}, "position": {"x": 960, "y": 200}}
            ],
            "edges": [
                {"id": "e1", "source": "load", "target": "decode", "sourcePort": "corpus", "targetPort": "corpus"},
                {"id": "e2", "source": "decode", "target": "control", "sourcePort": "results", "targetPort": "real_results"},
                {"id": "e3", "source": "control", "target": "out", "sourcePort": "validation", "targetPort": "data"}
            ]
        },
        {
            "id": "indus_v5_data_corrections",
            "name": "Indus V5 — Data Corrections & Corpus Unification",
            "description": "Phase 1: Fix Dholavira signboard count (10 signs, not 26), document M-314 (17-sign longest single-face), M-494/495 (26-sign 3-face amulet). Unified corpus: 1,670 seals from 9 sites, 390 signs, 7,002 tokens.",
            "auto_migrated": False,
            "nodes": [
                {"id": "corrections", "type": "expNode", "data": {"atomicId": "DataCorrections", "label": "Apply V5 corrections", "params": {}}, "position": {"x": 60, "y": 200}},
                {"id": "unify", "type": "expNode", "data": {"atomicId": "CorpusUnifier", "label": "Unify Holdat + CISI mayig", "params": {}}, "position": {"x": 360, "y": 200}},
                {"id": "out", "type": "expNode", "data": {"atomicId": "JSONExport", "label": "Save corrections report", "params": {"filename": "INDUS_V5_PHASES_1_3.json"}}, "position": {"x": 660, "y": 200}}
            ],
            "edges": [
                {"id": "e1", "source": "corrections", "target": "unify", "sourcePort": "corrections", "targetPort": "corrections"},
                {"id": "e2", "source": "unify", "target": "out", "sourcePort": "corpus", "targetPort": "data"}
            ]
        }
    ]

    for g in graphs:
        path = GRAPHS_DIR / f"{g['id']}.json"
        with open(path, "w") as f:
            json.dump(g, f, indent=2)
        print(f"  Registered graph: {path.name}")

    return len(graphs)


def build_email_body():
    """Build comprehensive email report from V5 results."""
    # Load the report
    report_path = REPORT_DIR / "INDUS_V5_PHASES_1_3.json"
    with open(report_path) as f:
        report = json.load(f)

    p1 = report["phase1_corrections"]
    p1s = report["phase1_corpus_stats"]
    p2 = report["phase2_spectral_grid"]
    p3 = report["phase3_longest_texts"]

    subject = "Indus Script V5 — Spectral Grid, Anchor Validation & Data Corrections"

    body = f"""INDUS SCRIPT DECIPHERMENT V5 — COMPREHENSIVE REPORT
{'='*60}
Generated: {report['timestamp']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1: DATA CORRECTIONS & CORPUS UNIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORPUS:
• Holdat LLC corpus: {p1s['holdat_seals']} seals from 9 sites
• CISI mayig corpus: {p1s['cisi_mayig_inscriptions']} inscriptions (supplementary)
• Distinct signs: {p1s['distinct_signs_holdat']} | Total tokens: {p1s['total_tokens']}
• Mean inscription length: {p1s['mean_length']} | Max: {p1s['max_length']}

SITES: {', '.join(f"{k}: {v}" for k,v in p1s['sites'].items())}

TOP 10 SIGNS: {', '.join(f"{s}({c})" for s,c in p1s['top_20_signs'][:10])}

KEY CORRECTIONS:
1. DHOLAVIRA SIGNBOARD: {p1['dholavira_signboard']['corrected_sign_count']} signs (NOT 26)
   {p1['dholavira_signboard']['note']}

2. LONGEST SINGLE-FACE (M-314): {p1['longest_single_face']['sign_count']} signs
   {p1['longest_single_face']['description']}
   NOTE: {p1['longest_single_face']['note_holdat']}

3. LONGEST MULTI-FACE (M-494/495): {p1['longest_multi_face']['total_sign_count']} signs across {p1['longest_multi_face']['faces']} faces
   {p1['longest_multi_face']['description']}

4. DHOLAVIRA IN CORPUS: {p1['dholavira_in_corpus']['count']} inscriptions (max {p1['dholavira_in_corpus']['max_length_in_corpus']} signs)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2: SPECTRAL SYLLABIC GRID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHOD: Normalized Laplacian spectral clustering on co-substitution matrix
SIGNS ANALYZED: {p2['n_signs_analyzed']} (freq >= {p2['freq_threshold']})
BEST k: {p2['best_k']} clusters (lowest coefficient of variation)

CRITICAL FINDING: The spectral grid does NOT reveal a consonant×vowel
structure. Instead, it reveals a 3-SLOT POSITIONAL GRAMMAR:

"""
    clusters = p2.get("clusters", {})
    for cl_id, info in sorted(clusters.items(), key=lambda x: int(x[0])):
        pos = info.get("positional_bias", {})
        top3 = info.get("top_signs", [])[:3]
        top_str = ", ".join(f"{s[0]}({s[1]})" for s in top3)
        pos_label = "INITIAL" if pos.get("initial", 0) > 0.7 else \
                    "TERMINAL" if pos.get("terminal", 0) > 0.4 else "MEDIAL"
        body += f"  Cluster {cl_id} [{pos_label}]: {info['n_signs']} signs, freq={info['total_freq']}\n"
        body += f"    Top: {top_str}\n"
        body += f"    Position: I={pos.get('initial',0):.0%} M={pos.get('medial',0):.0%} T={pos.get('terminal',0):.0%}\n\n"

    body += """
INTERPRETATION:
• 3 clusters are pure INITIAL (77+ signs combined) — these are "name/title" openers
• 5 clusters are pure MEDIAL — core descriptive/relational signs
• 1 cluster is TERMINAL-biased (M293, M059, M367) — closers/classifiers
• The high-frequency core (M342, M267, M099) forms its own medial cluster
• This pattern is consistent with a LOGOGRAPHIC/logo-syllabic system
  with fixed positional grammar, NOT a pure syllabary

"""

    control = p3.get("scrambled_control", {})
    body += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3: LONGEST-TEXT ANALYSIS & ANCHOR VALIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANCHOR SET: 12 signs (4 HIGH, 6 MEDIUM, 2 LOW confidence)
  HIGH: M342=ay/ā, M176=an/aṇ, M267=min/mīn, M099=kol/koḷ
  MEDIUM: M233=ūr, M391=ka/kaṇ, M162=il/iḷ, M328=ā/āl, M059=ēḷ/eḷ, M051=pū/puḷ
  LOW: M089=tu/tū, M048=mu/muṉ

DECODE RESULTS (top-50 longest inscriptions):
  Real decode rate: {control.get('real_decode_rate', 'N/A')} ({float(control.get('real_decode_rate', 0))*100:.1f}%)
  Scrambled control: {control.get('scrambled_decode_rate', 'N/A')} ± {control.get('scrambled_std', 'N/A')}
  SIGNAL-TO-NOISE RATIO: {control.get('snr', 'N/A')}

** SNR of 8.0 is HIGHLY SIGNIFICANT — our anchors are not random. **
The 12 anchor signs cover 57% of tokens in the longest inscriptions,
far above the 11% baseline from random sign selection.

TOP DECODED INSCRIPTIONS:
"""
    for r in p3.get("top_10", [])[:10]:
        body += f"  {r['id']} ({r['site']}, {r['iconography']}): "
        body += f"{r['n_decoded']}/{r['n_signs']} = {r['pct_decoded']*100:.0f}%\n"
        body += f"    Signs: {' '.join(r['signs'])}\n"
        body += f"    Read:  {r['reading']}\n\n"

    body += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT'S STILL MISSING FOR FULL DECIPHERMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. FULL CISI CORPUS: We have 1,670 seals (Holdat) + 179 (CISI mayig).
   The complete CISI has ~4,000+ inscriptions. The upcoming CISID
   (Ameri, Jamison, Kenoyer, Uesugi) digital edition would be transformative.

2. MULTI-LINE INSCRIPTIONS: Our corpus maxes at 8 signs per seal.
   The full M-314 (17 signs, 3 lines) and M-494/495 (26 signs, 3 faces)
   are not fully digitized in any open-access dataset.

3. MORE ANCHORS: 12 anchors cover 57% of long-text tokens, but we need
   30-50 to approach >80% coverage. Key targets:
   - M211 (freq=249): highly frequent, needs phoneme assignment
   - M293 (freq=232): terminal-biased, possible classifier
   - M087, M065, M012: medium-frequency signs needing validation

4. BILINGUAL EVIDENCE: Mesopotamian "Meluhhan" names in cuneiform texts
   remain the best untapped source. Cross-referencing Gulf-type round
   seals with Akkadian personal name lists could yield 2-3 new anchors.

5. MORPHOLOGICAL TEMPLATES: Identifying multi-sign words requires
   bigram/trigram PMI analysis to distinguish collocations from free
   combinations.

6. ARCHAEOLOGICAL CONTEXT: Stratified analysis by artifact type
   (seal vs tablet vs pottery) may reveal register-specific vocabulary.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. Acquire Fuls/ICIT corpus from epigraphica.de (~4,400 inscriptions)
B. OCR Bisht 2015 Dholavira draft from archive.org for 150 inscriptions
C. Build bigram PMI matrix to identify collocations/morphemes
D. Cross-reference Holdat constraint-based analysis with spectral clusters
E. Implement Bayesian decoder with positional grammar constraints
F. Attempt reconstruction of M-314 full 17-sign text from literature

Report saved: {report_path}
"""
    return subject, body


def send_email(subject, body):
    """Send email via Resend API or fallback to file."""
    try:
        from glossa_lab.notifications.resend import ResendConfig, send_mail
        cfg = ResendConfig.from_settings()
        if cfg.is_configured():
            result = send_mail(
                cfg,
                recipient=RECIPIENT,
                subject=subject,
                body_text=body,
            )
            if result.success:
                print(f"  Email sent to {RECIPIENT} (id: {result.message_id})")
                return True
            else:
                print(f"  Resend send failed: {result.error}")
        else:
            print("  Resend API key not configured")
    except Exception as e:
        print(f"  Email error: {e}")

    # Fallback: save as file
    fallback = REPORT_DIR / "INDUS_V5_EMAIL_REPORT.txt"
    with open(fallback, "w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\nTo: {RECIPIENT}\n\n{body}")
    print(f"  Email saved to file: {fallback}")
    return False


def main():
    print("=" * 60)
    print("V5 PHASE 4: Experiments + Email Report")
    print("=" * 60)

    # Register graphs
    print("\n--- Registering V5 Experiment Graphs ---")
    n = register_v5_graphs()
    print(f"  {n} graphs registered")

    # Build and send email
    print("\n--- Building Comprehensive Report ---")
    subject, body = build_email_body()
    print(f"  Subject: {subject}")
    print(f"  Body length: {len(body)} chars")

    print("\n--- Sending Email ---")
    send_email(subject, body)

    print("\n" + "=" * 60)
    print("PHASE 4 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
