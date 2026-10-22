# Adversarial pass — preprint v6 (2026-10-22)

Standing rule (AGENTS.md, 2026-10-22): before any paper is submitted,
an independent adversarial review runs — a different engine/reviewer
given the manuscript + bibliography, briefed to attack novelty/priority
claims, constants, and overclaims — every finding is adjudicated
against primary sources, and the adjudication is filed. Findings are
claims until verified. This file is that record for preprint v6. The
pass was run on the v6 source (with the P9 bibliography additions and
the count qualifiers applied).

## Reviewer and route

- **Reviewer:** OpenAI GPT-4-Turbo (`gpt-4-turbo-2024-04-09`) via the
  OpenAI API connector — a different engine from the manuscript's
  authoring/review chain. Brief: attack novelty/priority claims,
  underived constants, overclaims, citation integrity, and internal
  consistency; quote the passage attacked; mark anything it could not
  verify as UNVERIFIED-SUSPICION; never fabricate a reference.
- **Input:** the complete v6 `.tex` (18,759 prompt tokens). Output:
  721 completion tokens, finish_reason "stop"; five findings + a
  most-damaging ranking. Raw findings filed verbatim at
  `raw/fix_adversarial_findings_gpt4turbo.md`.
- **Route history (for the record):** the first-choice route
  (OpenRouter, house frontier arm) returned HTTP 402 (no credit for
  the call); two OpenAI frontier model ids returned 404 on chat
  completions (not enabled for that endpoint on this account);
  GPT-4-Turbo answered. The pass is therefore a real independent read,
  but a shallow one — its findings are mostly generic, and the
  adjudication below weights them accordingly. A deeper pass with a
  frontier reasoning model remains advisable before any actual
  submission; this record does not overstate what was run.

## Adjudication (each finding checked against primary sources)

**F1 — Novelty: "To my knowledge, no prior work has claimed >90% token
coverage with a published sign-by-sign evidence record" (§1.2, verified
present verbatim). Reviewer: CRITICAL overclaim.**
**Verdict: NOT SUSTAINED as an error; sustained as a caution, already
carried by the paper.** The sentence is knowledge-hedged ("To my
knowledge") and narrowly scoped (coverage *with a published
sign-by-sign evidence record*). The reviewer names no prior work that
makes such a claim, and neither did the material audit's literature
search. The real exposure is different: the coverage rests on the
unreleased Holdat corpus, so readers cannot check it — and the paper
itself discloses exactly that in its abstract, its limitations (§4.4),
and its reproducibility statement (§6). No text change; the caution is
recorded here and in the submission summary.

**F2 — Constant: "Frequency distribution follows Zipf's law (exponent
~ 1.7), consistent with a natural language writing system" (§2.1,
verified present; the v5 corrections already removed the wrong Rao
attribution from this sentence). Reviewer: MAJOR — exact number
without derivation.**
**Verdict: SUSTAINED in narrow form.** The ~1.7 exponent is the
paper's own statistic on the unreleased Holdat corpus (audit
corrections log item 6; reliance map in the audit report): no text
read reports it for any other corpus, the paper gives no derivation a
reader can follow, and the corpus is not public, so the number is
uncheckable as printed. This matches the audit's own finding that
every Holdat-derived number is unverifiable externally. **Recommended
owner action at submission time:** either add the derivation/fit
details for this exponent or qualify the sentence in place as the
program's own corpus statistic. The fix commission did not rewrite a
results sentence on a reviewer's say-so; the finding and the
recommendation are filed here and in the submission summary.

**F3 — Overclaim: "the evidence favours a Proto-Dravidian reading
framework under the tested assumptions" (§7, verified present).
Reviewer: CRITICAL — conclusion stronger than the evidence.**
**Verdict: NOT SUSTAINED as stated.** The sentence is conditional on
its face ("under the tested assumptions"), and the paper's limitations
sections carry the caveats the reviewer asks for. The reviewer names
no passage claiming more than the assumptions support. Noted for the
record: the program's own dossier posture on the underlying language
claim is more cautious (status "unsupported", stage "explained" —
`glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json`),
which is context the owner may weigh at submission; it does not make
the conditional sentence an overclaim.

**F4 — Citation integrity: reliance on Nair 2026 (a preprint) for
validation. Reviewer: MAJOR.**
**Verdict: NOT SUSTAINED.** After the v5 corrections the paper does
not rely on Nair for validation of the anchors or the grammar — it
describes Nair accurately as an independent scorecard study on a
separate digitisation of the same published assemblage, with a
different statistic and a hedged, intermediate conclusion (audit
report; corrections log item 7). Nair is cited as an arXiv preprint,
which the text does not disguise. The reviewer's premise ("heavily
relies on this source for validation") does not match the corrected
text.

**F5 — Internal inconsistency: "The 161 H+M anchors (75 HIGH + 86
MEDIUM) cover 6,363 of 7,002 corpus tokens." Reviewer: MINOR —
"minor inconsistency in the math or reporting".**
**Verdict: NOT SUSTAINED — checked and exact.** 75 + 86 = 161;
6,363 / 7,002 = 90.87%, consistent with the paper's ">90%" coverage
statement. The reviewer identified no actual discrepancy.

## Outcome

Five findings: one sustained in narrow form (F2, with a recommended
owner action), one sustained as a caution already carried by the paper
(F1), three not sustained (F3, F4, F5). **No finding required a text
change before this package could be assembled**, and none was made on
the reviewer's word alone. The package is submission-ready in the
commission's sense — corrected source + regenerated PDF + this
adjudication + the summary — and it stops here: deposit or submission
is the owner's act, on the actual text, and a deeper frontier-model
pass is recommended before that act (see the route history above).
