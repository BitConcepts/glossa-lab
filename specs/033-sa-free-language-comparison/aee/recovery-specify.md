# AEE recovery — Spec 033 register (after_specify)

Register: `specs/033-sa-free-language-comparison/claims.json`
(F033-C01…C15). Recovery follows the Spec 029/030/031/032
pattern: atomic rewrites, enumerations carried into
boundaries verbatim-in-substance, pairwise boundary
confirmations for every flagged pair — and a split only
where a claim genuinely carries two independently
falsifiable bars. Propositions, falsifiers, and verdict
rules are unchanged throughout.

## Round 1 — 2026-10-13T11:09:44Z — iterate (9 failure modes)

Artifact: `aee-after_specify-20261013T110944Z.json`
(0 claims below the 0.70 threshold).

- **Irreducibility (7):** C02 (the hypothesis against
  three named rivals), C03 (semantic anchoring and
  anchor promotion as two bars), C08 ("every family and
  every control"), C09 (two controls plus the pass
  condition), C10 (the SUPPORTED rule's two conditions),
  C11 and C12 (two verdict triggers each).
- **Precision (1):** C10 ("best rival" undefined in the
  claim's own terms).
- **Negation conflict (1):** C10↔C11.

**Recovery (register 0.1-draft → 0.2-draft, 14 → 15
claims).** Texts rewritten as single atomic
propositions; the named rival set (C02), the
anchor-promotion bar (C03), the baseline control (C09),
and the second triggers of C11 and C12 were carried
into their boundaries verbatim-in-substance. "Best
rival" is now defined in C10's boundary (the
highest-scoring of the Sanskrit, Munda, and baseline
assignments on the primary run). The SUPPORTED rule's
percentile condition was **split into its own claim,
F033-C15**: the margin over the best rival and the
percentile against the random distribution are two
independently falsifiable bars, and the established
pattern splits exactly there; C11 and C12 now depend
on both C10 and C15, and the verdict-rule partition
(C10/C15/C11/C12) is confirmed pairwise in the
boundary confirmations.

## Round 2 — 2026-10-13T11:10:25Z — iterate (5 failure modes)

Artifact: `aee-after_specify-20261013T111025Z.json`.

- **Negation conflict (3):** C03↔C08 (the barred
  machinery against the pipeline that replaces it);
  C10↔C11 (again); C11↔C15 (the new claim against
  the NOT SUPPORTED rule).
- **Precision (1):** C10, repeated ("best rival"
  still read as undefined from the text alone).
- **Irreducibility (1):** C11 (its boundary carried
  the second trigger plus the status consequence).

**Recovery (register 0.2-draft → 0.3-draft).** Per the
Spec 031 finding that the negation pairing reads
claim texts alone, the paired texts were de-mirrored:
C03 now states the bar without the word "pipeline";
C11 is keyed to finishing strictly first; C15 is
keyed to the percentile bar itself. C10's text names
the highest-scoring rival assignment directly, which
is the definition its boundary already carried.
C11's boundary was trimmed to its trigger statement;
the status consequence stands governed by spec §6.
Pairwise confirmations were extended for C03–C08 and
C11–C15, and C11's confirmation now states the full
outcome partition. Propositions, falsifiers, and
verdict rules unchanged.

## Round 3 — 2026-10-13T11:10:52Z — iterate (1 failure mode)

Artifact: `aee-after_specify-20261013T111052Z.json`.

- **Negation conflict (1):** C11↔C12 (the two rules
  shared the "Dravidian first" surface with opposite
  verdicts).

**Recovery (register 0.3-draft → 0.4-draft).** C12's
text was keyed to the winning margin instead of
Dravidian's placing; the outcome partition is
confirmed pairwise in both claims' boundary
confirmations. Propositions, falsifiers, and verdict
rules unchanged.

## Outcome — PASS (register 0.4-draft)

Re-run at after_specify on 2026-10-13T11:11:04Z:
**pass** (15 claims, 0 failure modes, 0 below the
0.70 threshold; artifact
`aee-after_specify-20261013T111104Z.json`). The
after_plan and after_tasks assessments over the same
register also return **pass** with the same summary.
The frozen register is the recovered register
(`0.4-draft`, 15 claims F033-C01…C15 — C15 split from
the SUPPORTED rule at recovery round 1); the
pre-recovery draft was never frozen.
