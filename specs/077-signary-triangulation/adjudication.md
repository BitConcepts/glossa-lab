# Spec 077 — Adjudication (freeze drafting record)

Drafted 2026-10-26 at the freeze act, under the owner's
order of 2026-10-26 09:32 EDT ("do all now" — M7
freeze-and-execute from the what's-next board). The
design frozen here is the M7 draft of 2026-10-25
(program goal record,
`2026-10-25-spec-draft-m7-signary-triangulation.md`,
SHA-256
2e9f9967ec30a558e3a31f93f54540b3d8450e25080c447d37ecd598175c1369),
as amended by its own 2026-10-25 iteration-pass
amendment. Rulings DD-077-1 … DD-077-8.

- **DD-077-1 — Numbering and phase.** The next spec
  number is 077 (076 consumed by the M12 freeze of
  2026-10-26) and the next phase is 443 (075 = Phase
  441, 076 = Phase 442, read from their freeze
  records). Slug: `077-signary-triangulation`, on the
  pattern of the adjacent freezes. Claim family F077.
- **DD-077-2 — The claim set.** The register carries
  the design's two claims as F077-C01 (the 90%
  witnessing claim) and F077-C02 (the token 999
  attack), and the design's own machinery as eight
  further claims: step-0 pin verification (C03), the
  population reproduction and 999's reference
  behavior (C04), the ancestry map (C05), the 13-id
  resolution (C06), sensitivities S1 and S2 (C07,
  C08), the gap-list deliverable (C09), and the
  Table I input condition (C10). F077-C01 and
  F077-C02 are the verdict-bearing claims. The
  design prescribed no pre-freeze pilot and no step-0
  gate of its own beyond §4.1's step 0, which the
  frozen spec carries as the execution's step 0; no
  pilot-closes-route question arises.
- **DD-077-3 — AEE hook findings.** The hooks ran
  at the freeze under the pinned evaluator (aee
  1.5.3) in the freeze configuration; each of the
  three artifacts carries 21 findings — the 10
  FR-2.3 draft caps (one per claim), 10
  irreducibility challenges (one per claim), and 1
  negation-conflict challenge (F077-C01 against
  F077-C03) — with no claim below the 0.70
  confidence threshold (minimum propagated 0.7200)
  and no findings of independence, ambiguity, or
  evidence-resolution kind. The challenges are
  answered in `aee/freeze-aee-note.md` from the
  spec's own structure: the register's two
  verdict-bearing claims carry the design's claims
  and everything else is filed as its own claim so
  it can fail on its own (irreducibility); and C01
  and C03 are a claim and its gate, not a
  contradiction — a step-0 failure files no C01
  verdict in either direction. The register was
  not reworded to silence the challenges.
- **DD-077-4 — The witness set (FF-2).** The draft's
  "Wells 1998 sign list / Wells 2006" is completed as
  follows. What is held and extracted is the 1998
  list (thesis pinned at SHA 5720dc01…; dataset
  22bde128…). Wells 2006 — the doctoral thesis whose
  Fig. 3.2 plates the Phase-123 witness cites — is
  held in plate form only and was never extracted as
  a sign list; a freeze may not count a witness it
  cannot pin, so the counted Wells witness is the
  1998 list, which is also the list the draft's §3
  pins by hash. The Wells/ICIT list in its 2015 form
  is excluded from the witness set: the population
  is keyed in its numbers, so counting it would make
  C01 true by construction at 557 of 557 and the
  claim untestable. This exclusion is the
  conservative direction (it can only lower the
  witnessed share) and it is what gives S2 its
  administration (DD-077-7).
- **DD-077-5 — No OSF registration.** The M7 design
  names no OSF registration and no filing provision;
  under the precedent of DD-076-5, none is filed.
  The repo freeze record governs. The absence is
  recorded here and in freeze.md, not improvised
  around.
- **DD-077-6 — Table I pinned by acceptance form
  (FF-7).** A deviation from the adjacent freezes'
  practice of pinning every input by hash, recorded
  openly: C02's Mahadevan arm needs per-sign
  occurrence totals and final counts, whose only
  source is Mahadevan's Table I, and the adjudicated
  Table I dataset had not landed in the canonical
  store when this freeze was built (Phase A, 203 of
  417 rows certain, is in the store at SHA
  aeec9cd1…; the adjudication was still running).
  Freezing the partial file as the input would have
  violated F077-C10's own standard and the draft's
  step-0 discipline. The freeze therefore pins the
  acceptance form — mechanical and exact: row
  equations on every complete row, the column sums
  reconciling exactly with the printed totals row
  under the landing record's stated residuals,
  unsettled cells empty and named — and step 0
  records the landed file's hash, which binds the
  execution from that point. Any file failing the
  form closes the execution exactly as a hash
  mismatch would.
- **DD-077-7 — The ancestry and S2 administrations
  (FF-5, FF-8).** The draft §4.1 requires the
  falsifier to apply to the ancestry-adjusted number
  "if it is lower"; the only administration under
  which the adjusted number can be lower is the
  root-list reading (a sign counts when witnessed in
  the lineage's root list), so FF-5 adopts it, with
  the merged reading reported alongside. S2's
  exclusion set is empty under the frozen witness
  definitions (DD-077-4); FF-8 says so on the record
  rather than dressing an empty recomputation as a
  measurement, and the per-witness breakdown is
  reported in full so the circularity question can
  be re-derived from the filed numbers by any reader.
- **DD-077-8 — C02's occurrence condition read in
  absolute counts (FF-6).** The draft pairs
  "occurrence count" with "999's population
  behavior"; 999's behavior in the population is a
  count (2) and a rate (0.0). The freeze administers
  condition 1 on the count as stated: a witness
  total of exactly 2 (2 ± 20% admits no other
  integer). The alternative share-of-corpus reading
  was considered and rejected: it would compare
  quantities the draft does not pair, and at these
  counts it admits the same Mahadevan candidates.
  999's reference values were derived at this freeze
  from Spec 075's pinned inputs under its frozen
  construction and are re-derived as a check at
  step 0 (F077-C04) — they are frozen as values to
  be reproduced, not assumed.
- **DD-077-9 — Required-C4 freeze.** This freeze is
  a required-C4 freeze, as Spec 076's was: the C4
  records check has been a required
  branch-protection check since 2026-10-25, and the
  gate records under `gate-records/` must pass it in
  CI on the freeze PR before any merge.

*What this adjudication establishes: the drafting
decisions of this freeze and their reasons. What it
does not establish: any outcome of the execution —
the witnessing shares, the gap list, and 999's
identity status are the execution's to file.*
