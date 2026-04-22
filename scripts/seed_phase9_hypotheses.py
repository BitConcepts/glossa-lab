"""
Seed Phase 9 Linguistic Hypothesis Tests into Glossa Lab DB.

These hypotheses appear in the UI Hypothesis Engine and are linked
to the corresponding Phase 9 graph experiments. Everything is
reproducible from Glossa Lab without the external agent.

Run: python scripts/seed_phase9_hypotheses.py
"""

import asyncio
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


HYPOTHESES = [
    {
        "title": "H1: P385 = Dravidian Genitive Suffix /n/",
        "statement": (
            "P385 (Cluster 21, TERMINAL class, end_rate=0.785, 349 corpus tokens, ICIT=ITM) "
            "represents the Dravidian genitive suffix -in/-n (Tamil: /-in/, contracted /-n/). "
            "Evidence: (1) P385 appears terminally in 78.5% of its occurrences; "
            "(2) it is the most frequent terminal sign in CISI; "
            "(3) the bigram P122→P385 (medial vowel → terminal) appears 29 times — "
            "consistent with CV+genitive suffix structure; "
            "(4) ICIT codes it as ITM (Initial Cluster Terminal Marker), implying grammatical function. "
            "Falsification: if SA with P385=n produces lower consistency than P385=other suffix, reject."
        ),
        "status": "active",
        "evidence": [
            "end_rate=0.785 (top 1 TERMINAL sign by end_rate in CISI)",
            "ICIT function code: ITM",
            "Bigram P122→P385: count=29 (strongest STEM→SUFFIX pattern)",
            "SA consistency with P385=n: 0.8591 (6-anchor set)",
            "Structural cluster 21: only member P385, 349 tokens",
        ],
        "exp_ids": ["indus_phase9_function_validation", "indus_phase9_cluster_anchored_sa"],
    },
    {
        "title": "H2: P324 = Proto-Dravidian Royal Title 'ko' (King/Chief)",
        "statement": (
            "P324 (Cluster 35, INITIAL class, start_rate=0.690, 1366 tokens, ICIT=ITM) "
            "represents the Proto-Dravidian royal title *ko (Tamil: ko = king/chief/bull). "
            "Evidence: (1) P324 appears initially in 69% of occurrences — the dominant INITIAL sign; "
            "(2) P324 NEVER precedes P122 (/a/ sign) — it is a full syllable, not a bare consonant; "
            "(3) P332 follows P324 in 91% of P332's occurrences, suggesting P324+P332 = CV pair 'ko'; "
            "(4) SA phonotactics assign P324→/k/ (consistent with 'ko' where /k/ dominates); "
            "(5) the inscription M-5A [P324+P096+P060+P256] reads structurally as 'ko-yi-i-l' → koyil (Tamil: temple). "
            "Falsification: if the P324 initial cluster distributes equally across sites without site-specific formula, reject title hypothesis."
        ),
        "status": "active",
        "evidence": [
            "start_rate=0.690, 1366 tokens (most frequent INITIAL sign in CISI)",
            "P324 never precedes P122 (0/98 co-occurrences) → full syllable not bare consonant",
            "P332 follows P324 in 91% of P332's 11 occurrences → CV pair structure",
            "6-anchor SA: P324=k gives consistency 0.8591 vs P324=o giving 0.817",
            "M-5A structural reading: koyil (Tamil temple) structurally consistent",
        ],
        "exp_ids": ["indus_phase9_function_validation", "indus_phase9_cluster_anchored_sa"],
    },
    {
        "title": "H3: Indus Inscriptions Encode INITIAL–MEDIAL*–TERMINAL Dravidian Structure",
        "statement": (
            "Hypothesis: Indus inscription structure matches Dravidian agglutinative morphology: "
            "(optional INITIAL determinative/title) + (one or more MEDIAL phonetic stems) + "
            "(TERMINAL grammatical suffix). "
            "Evidence: (1) 85.3% cross-site class stability for INITIAL/MEDIAL/TERMINAL classes — "
            "these are real script properties, not corpus artefacts; "
            "(2) 30 recurrent structural templates in cluster-space, dominant pattern is INITIAL+MEDIAL+TERMINAL; "
            "(3) Dravidian SA consistency 0.8591 with 6 structural anchors vs Pali 0.5702 — "
            "Dravidian phonotactics outperform MIA by 28.9pp; "
            "(4) the slot distribution (8 TERMINAL clusters, 8 INITIAL, 15 MEDIAL) matches "
            "a logosyllabic system with separate determinative and phonetic inventories. "
            "Falsification: if Sumerian or Sanskrit slot patterns fit better than Dravidian, reject."
        ),
        "status": "active",
        "evidence": [
            "Global class stability: 85.3% full, 95.1% partial (threshold: 70% — PASS)",
            "30 recurrent structural templates in 40-cluster-space",
            "Dravidian SA +28.9pp over Pali on real CISI bigrams",
            "8 TERMINAL, 8 INITIAL, 15 MEDIAL clusters — ratio consistent with logosyllabic system",
        ],
        "exp_ids": ["indus_phase9_dravidian_slot_test", "indus_phase9_template_readings"],
    },
    {
        "title": "H4: TERMINAL Clusters = Dravidian Grammatical Suffixes (Case/Verbal)",
        "statement": (
            "The 8 TERMINAL structural clusters contain Dravidian case suffixes and verbal endings. "
            "Dominant TERMINAL clusters: Cluster 21 (P385, end_rate=0.785), Cluster 39 (P378, end_rate=0.753), "
            "Cluster 9 (P226/P231/P359, end_rate=0.938). "
            "In Tamil Dravidian the main case suffixes are: -in (genitive), -ku (dative), -al (nominative), "
            "-atu (neuter noun), -il (locative). "
            "Prediction: TERMINAL clusters will show high ICIT ITM/TMK function code density, "
            "and SA phoneme assignments for TERMINAL signs will cluster around sonorants (/n/, /l/, /r/, /m/) "
            "consistent with Tamil suffix phonology. "
            "Falsification: if TERMINAL cluster signs receive stop consonant or vowel assignments "
            "predominantly (not sonorants), reject Dravidian suffix hypothesis."
        ),
        "status": "active",
        "evidence": [
            "Cluster 21: P385 end_rate=0.785, ICIT=ITM — top terminal sign",
            "Cluster 39: P378 end_rate=0.753, ICIT=ITM — secondary terminal",
            "Cluster 9: P226/P231/P359 end_rate=0.938 — ultra-terminal (boundary markers?)",
            "SA assigns P385→n, consistent with Tamil genitive sonorant suffix",
        ],
        "exp_ids": ["indus_phase9_function_validation", "indus_phase9_cluster_anchored_sa"],
    },
    {
        "title": "H5: Indus Script is a Logo-Syllabic System Encoding a Dravidian Language",
        "statement": (
            "The Indus script is a logosyllabic writing system (not purely alphabetic or purely logographic) "
            "encoding a Dravidian language (most likely Proto-Dravidian/Old Tamil). "
            "Evidence for logosyllabic: (1) Fuls 2023 estimates >700 distinct signs — more than a syllabary "
            "but fewer than pure logograms; (2) WritingSystemClassifier tier = Syllabary-compatible; "
            "(3) ICIT function codes include both LOG (logogram) and SYL (syllable) classes; "
            "(4) our cluster breakdown (8 INITIAL/determinative + 15 MEDIAL/phonetic + 8 TERMINAL/suffix) "
            "matches logosyllabic structure. "
            "Evidence for Dravidian: Dravidian SA outperforms Indo-Aryan (Sanskrit +24.1pp, Pali +28.9pp) "
            "on real CISI inscription bigrams. "
            "Falsification condition: if Farmer-Sproat-Witzel (2004) non-linguistic generator "
            "can reproduce all 4 Nair (2026) scorecard metrics simultaneously, reject linguistic encoding."
        ),
        "status": "active",
        "evidence": [
            "Dravidian SA: +24.1pp over Sanskrit, +28.9pp over Pali (real CISI bigrams)",
            "Nair 2026 scorecard: Indus occupies intermediate position — matches neither NL baseline",
            "Our 4-metric replication: 3/4 metrics consistent with linguistic encoding",
            "WritingSystemClassifier: Syllabary-compatible tier (H1≈1.10 on 179 CISI inscriptions)",
            "CGSA cluster structure: 40 clusters, 85.3% cross-site stable",
        ],
        "exp_ids": ["indus_phase9_template_readings", "indus_phase9_dravidian_slot_test"],
    },
    {
        "title": "H6: Cluster-Class Anchoring Outperforms Sign-Level SA (Test)",
        "statement": (
            "Anchoring phonemes to structural CLUSTERS rather than individual signs "
            "will produce higher SA consistency and lower mapping collapse. "
            "Rationale: individual sign anchoring risks phonotactic conflicts when the "
            "anchor sign is a logogram or determinative (not a phoneme carrier). "
            "Cluster-class anchoring ensures we only anchor signs in structurally appropriate classes "
            "(TERMINAL signs → sonorant suffixes; MEDIAL signs → vowels/sonorant stems). "
            "Prediction: 5-anchor set on TERMINAL/MEDIAL cluster members only will give "
            "higher consistency than the current 6-anchor set which includes P324 (possibly logographic). "
            "Falsification: if removing P324 from anchors reduces consistency, P324 IS a phoneme carrier."
        ),
        "status": "active",
        "evidence": [
            "Current 6-anchor consistency: 0.8591, HCI=88.4%",
            "P324 INITIAL cluster: logographic probability high (ICIT=ITM, never precedes /a/-sign)",
            "Cluster-class SA with only TERMINAL/MEDIAL anchors: pending experiment",
        ],
        "exp_ids": ["indus_phase9_cluster_anchored_sa"],
    },
]

NOTEBOOK_CONTENT = """# Phase 9 Research Session — Indus Script Linguistic Hypothesis Testing
**Date**: 2026-04-22 | **Status**: Active

## Overview

This notebook documents the Phase 9 linguistic hypothesis testing session, following
completion of CGSA Phases 1–8 (structural analysis, sign clustering, DoF extraction).

All experiments are graph-based and reproducible from the Experiment Builder.
All hypotheses are loaded in the Hypothesis Engine.

## Review Gate Status

- **Cross-site class stability**: PASS (85.3%, threshold 70%)
- **Multi-site coverage**: PASS (6 sites: Mohenjo-daro, Harappa, Dholavira, Lothal, Kalibangan, Chanhujo-daro)
- **Image-backed crosswalk**: BLOCKED (requires CISI print volumes — contact Parpola group)
- **Human review**: GRANTED (session 2026-04-22)

## Structural Foundation

From CGSA Phases 1–8:
- 803 canonical signs (396 Parpola + 407 Yajnadevam/ICIT)
- 40 structural clusters: 8 TERMINAL, 8 INITIAL, 15 MEDIAL, 1 BIMODAL, 8 MIXED
- 105 globally classifiable P-signs (freq >= 10)
- 30 recurrent structural templates in cluster-space

## Key Anchors (verified 6-anchor set, DB ID: dcf69e6e69fe)

| Sign | Class | Phoneme | Confidence | Evidence |
|------|-------|---------|------------|----------|
| P385 | TERMINAL | n | HIGH | end_rate=0.785, ICIT=ITM, 349 tokens |
| P324 | INITIAL | k | HIGH | start_rate=0.690, 1366 tokens |
| P122 | MEDIAL | a | MED | internal_rate=0.895, 76 tokens |
| P086 | MIXED | m | MED | end_rate=0.54 in short inscriptions |
| P060 | MIXED | i | MED | vowel candidate |
| P332 | MEDIAL | o | MED | follows P324 91% of occurrences |

## Experiments (Phase 9 graph experiments)

1. `indus_phase9_function_validation` — Cross-validate cluster classes vs ICIT sign functions
2. `indus_phase9_dravidian_slot_test` — Test INITIAL-MEDIAL-TERMINAL = Dravidian morphological structure
3. `indus_phase9_cluster_anchored_sa` — SA with cluster-class anchoring, Dravidian vs Pali control
4. `indus_phase9_template_readings` — CAS+Dravidian template reading attempts

## How to Reproduce (without agent)

1. Open Glossa Lab → Experiment Builder
2. Load any `indus_phase9_*` experiment from the graph library
3. Run via the Run button (jobs appear in Reports/Data)
4. Hypotheses: Hypothesis Engine tab → see H1–H6

## Open Questions

1. Is P324 a logogram (royal title 'ko') or a phoneme carrier /k/?
2. Does the 'ko-yil' (temple) reading of M-5A hold cross-validation?
3. Which MEDIAL cluster signs are phonemic vs logographic?
4. What is the reading of the Dholavira signboard inscription?
5. Can the CPSC constraint engine distinguish phoneme-carrier signs from logograms?
"""


async def main() -> None:
    from glossa_lab.database import init_db  # noqa: PLC0415
    db = await init_db(ROOT / "data")

    exp_ids_all = [
        "indus_phase9_function_validation",
        "indus_phase9_dravidian_slot_test",
        "indus_phase9_cluster_anchored_sa",
        "indus_phase9_template_readings",
    ]

    # Seed hypotheses
    for h in HYPOTHESES:
        import uuid  # noqa: PLC0415
        hid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"glossa:hypothesis:{h['title']}"))[:12]
        # Check if exists (upsert pattern via delete+insert)
        await db._conn.execute("DELETE FROM hypotheses WHERE title=?", (h["title"],))
        import json  # noqa: PLC0415
        await db._conn.execute(
            """INSERT INTO hypotheses (id,title,statement,status,evidence,study_ids,exp_ids,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                hid, h["title"], h["statement"], h["status"],
                json.dumps(h["evidence"]),
                json.dumps([]),
                json.dumps(h["exp_ids"]),
                now(), now(),
            )
        )
        print(f"  Seeded: {h['title'][:60]}")
    await db._conn.commit()
    print(f"\nSeeded {len(HYPOTHESES)} hypotheses")

    # Seed research notebook
    nb_id = "phase9_research_nb"
    await db._conn.execute("DELETE FROM notebooks WHERE id=?", (nb_id,))
    await db._conn.execute(
        """INSERT INTO notebooks (id,title,content,study_id,tags,created_at,updated_at)
           VALUES (?,?,?,?,?,?,?)""",
        (
            nb_id,
            "Phase 9: Indus Linguistic Hypothesis Testing",
            NOTEBOOK_CONTENT,
            None,
            json.dumps(["indus", "phase9", "dravidian", "decipherment", "cgsa"]),
            now(), now(),
        )
    )
    await db._conn.commit()
    print("Seeded research notebook: Phase 9 Indus Linguistic Hypothesis Testing")

    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
