# C1 kill-test battery — results

Evaluator: `aee` **1.5.3** (applied-epistemic-engineering), run 2026-10-25T14:26:03Z.
Configuration: the freeze configuration (lenient load, evidence verification off,
no ledger). Case (iv) was additionally run with evidence verification on; its
determination rests on both runs. A finding counts as a correctness finding
unless it is an FR-2.3 draft-cap record (register hygiene, carried by every
draft register). Raw evaluator outputs: `raw/` beside this file.

## Case (i) — The real Spec 026-era design (Phase-114 blind affiliation, Spec 012)

Defect class: non-discriminating instrument in a real historical design (programme-falsified).
Expected catcher: none in the gate as operated — historically caught by execution, which is the gap this battery documents.
**The evaluator could not be run against this case.** evaluator could not be run against this case in the freeze configuration: Error: input bundle contains zero claims: an empty bundle is an input error, never a pass (Spec 003 FR-1.1)

**Result: NOT FLAGGED — NAMED BLIND SPOT.** The evaluator cannot be run against this case in its current form, so the gate has no reading on this defect class at all. Reason recorded: Error: input bundle contains zero claims: an empty bundle is an input error, never a pass (Spec 003 FR-1.1)


## Case (ii) — Planted unfalsifiable headline claim

Defect class: unfalsifiable headline claim (falsifier present in form, empty in substance).
Expected catcher: the evaluator's falsifiability/irreducibility challenges, if they bite on substance rather than form.
Assessed 2 claim(s); assessment outcome `iterate`; 2 draft-cap finding(s); 2 non-draft-cap finding(s), of which 0 address this case's defect.
Determination rule: Flagged only if a correctness finding against FB2-C01 names the falsifiability defect (empty/circular/untestable falsifier). Independence or hygiene findings do not count: they fire on sound registers too.
- FINDING on FB2-C01: Shared-evidence independence challenge (AEE-FB2-C01-INDEPENDENCE-UNMODELED) — does not address the defect
- FINDING on FB2-C02: Shared-evidence independence challenge (AEE-FB2-C02-INDEPENDENCE-UNMODELED) — does not address the defect
**Result: NOT FLAGGED — NAMED BLIND SPOT.** The evaluator does not detect a falsifier that is present in form and empty in substance: the planted headline claim FB2-C01 passes with no correctness finding naming its untestable test.

## Case (iii) — Planted wrong pin (52 against a source summing to 47)

Defect class: pinned quantity arithmetically wrong against its own cited source.
Expected catcher: C2 independent recomputation (the evaluator is not an arithmetic engine).
Assessed 3 claim(s); assessment outcome `iterate`; 3 draft-cap finding(s); 3 non-draft-cap finding(s), of which 0 address this case's defect.
Determination rule: Flagged only if a correctness finding identifies the pinned quantities as wrong against SOURCE.md. Independence or hygiene findings do not count.
- FINDING on FB3-C01: Shared-evidence independence challenge (AEE-FB3-C01-INDEPENDENCE-UNMODELED) — does not address the defect
- FINDING on FB3-C02: Shared-evidence independence challenge (AEE-FB3-C02-INDEPENDENCE-UNMODELED) — does not address the defect
- FINDING on FB3-C03: Shared-evidence independence challenge (AEE-FB3-C03-INDEPENDENCE-UNMODELED) — does not address the defect
**Result: NOT FLAGGED — NAMED BLIND SPOT.** The evaluator does not recompute pinned quantities against their cited sources: a total of 52 pinned against a source summing to 47 passes without a correctness finding. C2 (independent recomputation) is the component that carries this class.

## Case (iv) — Planted unsupported citations (claims stating the opposite of their cited records)

Defect class: evidence citation that does not support its claim.
Expected catcher: C3 evidence verification with a human/verifier read of the cited text (the engine checks resolution and hashes, not support).
Assessed 2 claim(s); assessment outcome `iterate`; 2 draft-cap finding(s); 0 non-draft-cap finding(s), of which 0 address this case's defect.
Determination rule: Flagged only if a correctness finding on an FB4 claim identifies that its cited evidence does not support it (in either run). missing_ref resolution findings do not count: the refs resolve inside the repo; support, not resolution, is the defect.
Evidence-verification run: 2 claim(s), outcome `iterate`, 0 correctness finding(s).
**Result: NOT FLAGGED — NAMED BLIND SPOT.** The evaluator verifies that citations resolve, not that they support: claims stating the opposite of their cited records pass in both the freeze configuration and with evidence verification on. C3's verification step — a verifier reading the cited text against the claim — is the component that carries this class.

## What this battery does and does not establish

It establishes whether the current evaluator, as the freezes run it,
flags these four named defect classes — nothing more. It does not
establish that the evaluator catches any other class of defect, and
a flagged case does not make the gate a correctness check on its own:
C2 and C3 carry the classes the evaluator is blind to, and C4 is what
makes any of it mechanical.
