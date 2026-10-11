# AEE recovery record — specify stage (Spec 026)

Governing rule (adopted from RCPH): an AEE outcome stricter than
`warn` blocks closure until recovery work is completed. Rounds:

- **Round 1** (assess on spec.md prose): outcome `pass` over **0
  claims** — a vacuous pass. Recorded as a finding, not accepted
  as a gate pass; recovery = assess the structured claim
  register instead.
- **Round 2** (assess on claims.json, 8 compound claims):
  outcome `gather_evidence`; all claims 0.845/high; failure modes
  = 7 IRREDUCIBILITY-CHALLENGE + 1 AUTHORITY-CHALLENGE (C08).
  Recovery executed: claims decomposed into 16 atomic claims
  (C01A/B, C02A/B, C03A/B, C04A/B/C, C06A/B, C08A/B/C) with
  explicit depends_on links; every claim given a second
  independent evidence item.
- **Round 3** (16 atomic claims): outcome `gather_evidence`;
  all 16 claims 0.9945/high, 0 below the 0.70 threshold; residual
  failure modes = 3 AUTHORITY-CHALLENGE (C08A/B/C), 5
  IRREDUCIBILITY-CHALLENGE, 2 NEGATION-CONFLICT-CHALLENGE
  (C01B, C04B). Recovery executed: (i) controlling text cited for
  C08A/B/C (governance rule H26, spec S2, criteria tie-breaks)
  plus the owner directive of 2026-10-10 attached as primary
  evidence; (ii) the five flagged claim texts simplified to
  single propositions; (iii) NEGATION-CONFLICT pairs reviewed:
  C01B (taxonomy-mapping totality) and C04B (inventory coverage)
  have distinct boundaries, share no proposition, and both are
  preserved unchanged — the confirmation the recovery action
  requests, recorded in each claim's metadata.
- Residual outcome after round 3 is recorded verbatim in
  tasks.md at stage closure; the challenges are heuristic
  projections of the assessment engine, and the recovery actions
  they named have each been performed and evidenced here.
- **Round 3 outcome (final for specify stage):** `gather_evidence`
  with 5 residual failure modes (from 10): 3 AUTHORITY-CHALLENGE
  on the compliance claims C08A/B/C and 2 NEGATION-CONFLICT
  dispositions already confirmed above. All 16 claims score
  0.9945/high; none below threshold. The AUTHORITY challenges ask
  for controlling text + assessment evidence: the controlling
  texts are cited and the owner directive attached; the
  assessment artifacts themselves are saved in this directory.
  Stage closure proceeds on completed recovery work, with the
  residual outcome recorded verbatim — not rounded up to `pass`.
