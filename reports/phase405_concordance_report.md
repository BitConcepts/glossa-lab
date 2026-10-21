# Phase-405 — Spec 046 identification concordance report

Executed 2026-10-21 by Muse Spark via Muse (AI agent), under the
frozen Spec 046 contract (freeze-act digest
`80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405`; successor digest
`e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6` in freeze.json as merged; OSF
registration dnts8, approved + public before the run).

## Outcome

**IDENTIFICATION FAILED (sign unmatched)**

The fragment 'sign 297 is the horned tiger' cannot be carried to a concordance: the drawn sign could not be matched from Wells's published list. The record stays a stated gap. No statement about the sign is made, and nothing is fed to Asset A.

This result settles what the published lists say the drawn sign depicts. It is not evidence of what the sign meant in use.

## The passage (spec section 8, element 1)

> "Sign 532 and sign 297 are positioned in such a way as to resemble the position of the graphic element and several of their features are repeated in the image field. It is proposed here that sign 532 is a logograph for the anthropomorphic figure and that sign 297 represents the horned tiger, or perhaps just ‘tiger’ generically."

Locator: Wells (2015), printed p. 97 (held cleaned text,
lines [2941]).

## Step 0 (all gates passed)

Gate 0.1 — input integrity, every pin recomputed:

- `glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json` — SHA-256 `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a` (pin match: True)
- `glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt` — SHA-256 `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` (pin match: True)
- `glossa-indus/reports/phase104_claims_evaluation.json` — SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (pin match: True)
- `data/crosswalks/canonical_sign_registry.csv` — SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (pin match: True)
- `specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json` — SHA-256 `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` (pin match: True)

Gate 0.2 — the source book was produced from the held copy
and the passage located verbatim (above).

Gate 0.3 — all four lists accounted for as HELD or CITABLE
with citation plus locator form (CITATIONS.md §§A.1, A.2,
A.3, A.7, C.1; CISI Phase-124 catalogue layers): WELLS
HELD; CISI HELD; PARPOLA CITABLE; MAHADEVAN CITABLE.

## Step 1

The source's sign list is named from the book's own
apparatus: Wells's own sign list (Wells 2011), as given in
Wells 2015, Chapter 2, "The Indus Sign List" (Figure 2.6)
("Chapter 2 gives the Indus sign list used in this
analysis"; "The sign list used here (Wells 2011)").

The drawn-sign match failed. No crosswalk-registry entry carries the drawn sign: the only W297 occurrence in the pinned registry is one value inside the 17-value wells_ids cell on the P205 row ('Prismed light rays…'), which the frozen spec (section 4.3) names as a trap that does not by itself identify the passage's sign; no registry description names a tiger; the Phase-123 Wells segmentation witness carries no Wells grapheme 297. In Wells's published list itself (Figure 2.6), the drawn forms did not survive the held copy's text extraction (the figure pages carry captions only), so no drawn-sign reference the executor can inspect and defend exists in the held record. The prior in-repo search stands unrebutted: Spec 004 WS2 (glossa-indus/LEDGER.md, 2026-10-05) recorded three candidate referents — M297, P297, W297→P205/M180 — none matching the description in-repo. Matching by number is forbidden (F046-C07) and was not used.

## Step 2

Not reached. No list was scored, no concurrence state was
computed, and nothing is fed to Asset A: the delivery
(`specs/046-horned-tiger-concordance/concordance-297.json`)
carries an empty signs array and the closure block, in the
frozen section 6 form.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
