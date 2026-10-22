# RESTORATION DRAFT — §3.32 Betweenness Centrality — HELD PENDING ROIF'S REPLY

**Status: PREPARED BUT HELD. This draft is NOT part of preprint v7
or of any other version. It must not be inserted into the preprint,
submitted, posted, or sent anywhere until Avishai Roif replies to
the owner's letter and agrees to the section's restoration as
co-author. Filed with the preprint package 2026-10-22 under the
owner-directed Roif credit addendum (Addendum 2) to the spec-025
audit fix commission.**

## Why this draft exists

Preprint v1 (May 2026) carried a §3.32 betweenness-centrality
section. The betweenness analysis in it was contributed by
Avishai Roif, who on 2026-05-22 accepted co-authorship of that
section. After a posting breached the agreed timing (his NCSI
framework paper was under review at *Semiotica*), the owner's
June 2026 correction removed the section entirely. The owner is
now writing to Roif to ask (a) the current status of the NCSI
paper at *Semiotica*, and (b) whether he wants the section
restored as co-author. This draft is what restoration would look
like, so the owner can show Roif exactly what is proposed.

## Agreed attribution (verbatim, as proposed by Roif 2026-05-22 and accepted by the owner)

> Betweenness centrality analysis in this section was conducted by A. Roif using network-theoretic methods developed independently; the full methodological framework will appear in Roif (forthcoming, Semiotica).

[Bracketed note for restoration time: if the NCSI paper is now in
press or published, this sentence updates to the full *Semiotica*
reference — title, volume, pages, DOI — in place of
"(forthcoming, Semiotica)". Roif's reply governs the wording.]

## Draft section text (reconstructed from the program's own Phase 172–177 records, 2026-05-22)

### 3.32 Betweenness Centrality and Positional Slots (Phases 172–177)

[Attribution sentence above goes here, at the head of the section.]

We computed betweenness centrality for all 161 HIGH+MEDIUM signs
on the full sign-co-occurrence graph of the Holdat LLC Indus
Corpus v3 (1,670 seal sequences; 414 edges at PMI > 0, minimum 2
seals per pair; Phase 172, 2026-05-22). The question the analysis
answers is which signs hold the inscription formula together —
which signs sit on the paths between otherwise separate clusters
of signs.

The highest-betweenness signs are the formula's grammatical
backbone, not its content words. M342 (*ay/ā*, betweenness
0.0554, rank 1) and M267 (*iN/in*, genitive particle, 0.0506,
rank 3) are MEDIAL bridges: they connect INITIAL classifiers to
TERMINAL suffixes. Stratifying betweenness by positional slot
(Phase 177) separates two different structural roles that a single
ranked list mixes together: MEDIAL bridges, which link slots, and
INITIAL hubs, which begin many formula types but do not bridge
clusters (the M059 case, Phase 176). The bridge structure is
independent support for the three-slot positional grammar: the
signs that hold the graph together are exactly the signs the
positional analysis places between the classifier slot and the
suffix slot.

Source records: `research/indus/phase_reports/phase172_betweenness_full.json`,
`phase173_irresolvable_check.json`, `phase174_filtered_name_matching.json`,
`phase175_site_proxy.json`, `phase176_m059_bridge_role.json`,
`phase177_bc_slot_mapping.json`; scripts
`backend/scripts/phase172_174_betweenness_stratification.py` and
`backend/scripts/phase175_178_network_deep.py`.

## Checks required before this draft could be restored (not yet done)

1. Roif's reply: consent to restoration as co-author of the
   section, and the current *Semiotica* status of the NCSI paper.
2. Every number above re-verified against the Phase 172–177
   records at restoration time. One known item to resolve: the
   Phase 176 record's description frames M059 as "rank 2" while
   its own data field gives rank 18 (betweenness 0.003027); the
   draft above takes no position on M059's rank.
3. The original v1 §3.32 wording does not survive in the
   repository; this draft is a reconstruction from the phase
   records, not a recovery of the original text. If Roif holds the
   original, his copy governs.

**Nothing in this draft has been submitted, posted, or sent.**
