# Phase-427 (Spec 065) — report

Freeze digest: `f50a6e9c45d96fe15e737ee83a46b83c2c7e150e4a29421ccb5ec2be7a428c09`. OSF registration 34s9u (approved + public before the run). Date: 2026-10-22.

## Step 0 gates (recorded before any per-source row)

- Gate 0.1 (input integrity): **PASS**
- Gate 0.2 (acquired-file assertion (S-5)): **PASS**
- Gate 0.3 (S-1 intake determination): **PASS**
- Gate 0.4 (order): **PASS**

## Accounting

| # | Source claim_id | Document searched or blocker ref | Outcome | Evidence |
|---|---|---|---|---|
| S-1 | `ancient_writing_and_modern_technologies_51831ac9_statisti_0004` | local research store: downloads/fuls-studies-on-indus-script-2020/BLOCKED.md; PROVENANCE.md S-1 sections after entry 23 (no provenance entry taken) | STILL UNLOCATED — ACQUISITION BLOCKED | the blocker record itself (gate 0.3 determination): no intake-S1.json before the run, no delivered S-1 file in the downloads tree, the ILL portion-copy request of 2026-10-22 pending with nothing intake-pinned |
| S-5 | `without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002` | 77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665 | HEADING ABSENT FROM DOCUMENT | the searched file's SHA-256 77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665 (the acquired file, gate 0.2) and the extraction artifact at SHA-256 74e42f8e3e4af6488c14540dd8c5b32e2cd5eed0cfdc03eaf82a7043dfcc155d |

## Headline — B — S-5 RESOLVED, S-1 STILL BLOCKED

One of Spec 057's two unlocated rows is resolved on the document itself. S-5: HEADING ABSENT FROM DOCUMENT (no sub-result; no claim recovered — the row's evidence is the searched file's hash and its single judged occurrence), on the acquired file at SHA-256 77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665. S-1 remains STILL UNLOCATED — ACQUISITION BLOCKED: no document was handed over before the run, no search was run for S-1, and nothing about the chapter is found or implied. The unblocking act remains the owner account act named on S-1's row.

Disposition: superseded-not-retired (class B): the heading record stands exactly as Spec 057 left it — superseded by Spec 057's two recovered claims, not retired. The appended, dated note records S-5's resolution (HEADING ABSENT FROM DOCUMENT, on the acquired file at SHA-256 77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665) and S-1's blocked posture (STILL UNLOCATED — ACQUISITION BLOCKED), and states that retirement is not available while S-1 remains unlocated (spec section 7.2).

This act searched two documents for a heading. It checked nothing either passage states.
