# Freeze-gate statistics (C5)

Generated 2026-10-25 by `tools/freeze-gate/gate_statistics.py` from the
records on main. Do not edit by hand; regenerate.

## The strengthened gate (C1–C4)

- Freezes carrying gate records so far: **1** (075-depicted-kind-endings-atlas)
- Freezes blocked by C2 (spot-check outcome not PASS): **0**
- Freezes blocked by C3 (evidence-sample outcome not PASS): **0**
- C2 mismatches recorded (resolved + unresolved): **0**
- C3 unverified sampled claims recorded: **0**

## C1 battery (current evaluator)

Evaluator `aee` 1.5.3, run 2026-10-25T14:26:03Z (lenient load; evidence verification off (freeze configuration); case iv additionally run with evidence verification on).

| Case | Defect class | Result |
|---|---|---|
| (i) The real Spec 026-era design (Phase-114 blind affiliation, Spec 012) | non-discriminating instrument in a real historical design (programme-falsified) | NOT flagged — named blind spot |
| (ii) Planted unfalsifiable headline claim | unfalsifiable headline claim (falsifier present in form, empty in substance) | NOT flagged — named blind spot |
| (iii) Planted wrong pin (52 against a source summing to 47) | pinned quantity arithmetically wrong against its own cited source | NOT flagged — named blind spot |
| (iv) Planted unsupported citations (claims stating the opposite of their cited records) | evidence citation that does not support its claim | NOT flagged — named blind spot |

Named blind spots, in plain words:

- Case (i), non-discriminating instrument in a real historical design (programme-falsified): The evaluator cannot be run against this case in its current form, so the gate has no reading on this defect class at all. Reason recorded: Error: input bundle contains zero claims: an empty bundle is an input error, never a pass (Spec 003 FR-1.1)

- Case (ii), unfalsifiable headline claim (falsifier present in form, empty in substance): The evaluator does not detect a falsifier that is present in form and empty in substance: the planted headline claim FB2-C01 passes with no correctness finding naming its untestable test.
- Case (iii), pinned quantity arithmetically wrong against its own cited source: The evaluator does not recompute pinned quantities against their cited sources: a total of 52 pinned against a source summing to 47 passes without a correctness finding. C2 (independent recomputation) is the component that carries this class.
- Case (iv), evidence citation that does not support its claim: The evaluator verifies that citations resolve, not that they support: claims stating the opposite of their cited records pass in both the freeze configuration and with evidence verification on. C3's verification step — a verifier reading the cited text against the claim — is the component that carries this class.

## The register-discipline gate (for scale)

- Freezes with an AEE freeze note on main: **47** (counted from `specs/*/aee/freeze-aee-note.md`; the notes are prose and are not parsed by this generator). Across those freezes the gate's recorded findings were FR-2.3 draft-cap hygiene records; it blocked no freeze. That is the finding (RT-01) this machinery answers.

## What these statistics do and do not establish

They summarise the gate's own records, arithmetically. They do not
establish anything about past freezes, whose verdicts stand on their
own records, and a quiet table (few blocks) does not by itself show
the gate is weak or strong — the battery's blind spots above are the
honest measure of what the evaluator, as operated, cannot see.
