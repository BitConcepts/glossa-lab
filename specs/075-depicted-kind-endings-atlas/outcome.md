# Spec 075 — Execution outcome

**Date:** 2026-10-25
**Execution:** Phase-441, two runs, byte-identical results
(`reports/phase441_results.json`, SHA-256
`f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29`)
**Freeze:** digest `aa06726f545218c5bcee4b3a5df94c920828fead4e06e2ccec1eeffce44ac5cf`
(freeze PR #389, merged `fd9bd448`)
**Registration:** OSF jv74f (filed 2026-10-25; approved by the owner and
public the same day), DOI 10.17605/OSF.IO/JV74F
**Owner's order:** 2026-10-25 12:03 EDT — execution begins when the freeze
completes; the freeze record completed (PR #389 merged on genuine CI
including the C4 gate-records check; the registration approved and
API-verified) and this execution ran under that order.

**Lineage (P-F1 S3, verbatim).** This corpus is an ICIT-lineage corpus. Agreement between it and the program's earlier ICIT-lineage layer is consistency within one tradition, not independent corroboration.

## The celestial arm (pre-registered, reported first)

The celestial class as frozen in Asset A v2 contains zero signs; there is
no celestial rate. The empty class is the Spec 071 line's closing finding
(retirement decision, 2026-10-25), restated here because this atlas is
where a reader would look for it. It establishes nothing new about sky
signs.

## Outcome: the four per-kind verdicts

All six step-0 gates passed (step0-record.md). The population reproduced
exactly (3,045 analyzable documented-lineage rows, 557 distinct signs,
550 in sequences of length ≥ 2), every sign keyed under the frozen
two-leg route (556 signs keyed — 423 by leg 1, 133 by leg 2 — to 424
distinct Asset A v2 rows; token 999 the named exclusion, 2 occurrences),
and the census was published before any rate: other 307 signs / 7,006
occurrences, human 53 / 978, animal 39 / 1,179, object_goods 24 / 2,159;
unidentified 133 signs / 481 occurrences as context; the corpus-wide
final-position rate 0.2579 (3,045 of 11,805). No kind was TOO THIN.

Measured per kind against the frequency-matched comparison class of
section 2.3 (the other identified kinds, in the kind's own member band),
under section 5.2's frozen bands:

| Kind | Kind rate | Comparison rate | Ratio | Fisher (two-sided) p | Verdict |
|---|---|---|---|---|---|
| other | 0.2900 (2,032/7,006) | 0.2686 (807/3,004) | 1.0796 | 0.0295 | **INCONCLUSIVE** |
| human | 0.2526 (247/978) | 0.3244 (1,778/5,481) | 0.7785 | 6.93e-06 | **NOT SUPPORTED** |
| animal | 0.2774 (327/1,179) | 0.3112 (2,128/6,838) | 0.8912 | 0.0200 | **NOT SUPPORTED** |
| object_goods | 0.1153 (249/2,159) | 0.2844 (2,606/9,163) | 0.4055 | 2.34e-67 | **NOT SUPPORTED** |

**Kind other: INCONCLUSIVE.** Its signs end inscriptions a little above
the comparison rate (ratio 1.0796; the exact test is significant at
p = 0.0295), but the ratio stands far below the design's 1.5 support
threshold, and the half-of-occurrences condition also fails, narrowly:
0.4970 of the kind's occurrences come from signs individually above the
corpus-wide rate, against the required half. The word falls between the
frozen bands and is recorded as it falls.

**Kind human: NOT SUPPORTED.** Ratio 0.7785, at or below 1.0 — the
falsifier's word. Human signs end inscriptions *less* often than signs of
comparable frequency from the other identified kinds (p = 6.93e-06 for
the difference).

**Kind animal: NOT SUPPORTED.** Ratio 0.8912, at or below 1.0 — the
falsifier's word. This is a verdict on the animal kind's ending behaviour
in this study's own claim family; it is not Spec 071's retired question
and not a test of Hunt's claims in any form, and it moves neither.

**Kind object_goods: NOT SUPPORTED.** Ratio 0.4055 — the strongest
departure in the atlas, in the depleting direction: object-and-goods
signs end inscriptions at well under half the rate of comparable signs
(p = 2.34e-67). Only 0.1579 of the kind's occurrences come from signs
individually above the corpus-wide rate.

The family's hypothesis (F075-C03 — at least one identified kind is
enriched at endings) therefore stands **in question**: no kind returned
SUPPORTED, and the family does not speak with one word (three
falsifier-word verdicts and one inconclusive). The dated append
`spec075_outcome_append_2026_10_25` carries this disposition, and the
step-0 and reporting dispositions for F075-C05, C06, C07, C08 and C11,
onto the claim family's record in the machine record. **No pooled
depicted-kinds verdict was computed, stated, or implied** (F075-C11):
the four words above are the whole result, published together with
their per-sign tables in `reports/phase441_results.json` and
`reports/phase441_report.md`.

**The sensitivities agree with the primaries in every word.** S1
(borderline removed — signs 255, 256, 520, 716, 717) returns the same
four words (ratios: other 1.0043, human 0.7840, animal 0.8256,
object_goods 0.4589). S2 (contested included) equals the primary exactly,
as the freeze expected: Asset A v2 carries zero contested rows, so the
inclusion set is empty. S3 (the documented + corroborated population:
5,131 analyzable rows, 707 distinct signs, every sign keyed, none
unkeyable) returns the same four words (ratios: other 1.0581, human
0.8664, animal 0.8835, object_goods 0.5586) — **no verdict is
grade-sensitive**. Agreement across arms is not independence (spec
section 5.4): the arms run on compilations of substantially the same
excavated objects, within the same corpus and the same lineage.

**Position is not meaning (spec section 9.1, binding).** These words
state positional facts about the published identification layer on this
corpus. They do not establish scheduling, ritual, calendars, cycles,
trade, identity-marking, or any reading of any sign — and the depletions
(human, object_goods ending *less* often than comparable signs) are
positional facts of the same limited kind, not evidence about what
those signs meant or did.

**Classification (spec section 9.2).** Asset A v2 — SHA-256
`681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`;
552 rows; per-kind counts: other 246, unidentified 211, human 43,
animal 30, object_goods 22, sky_cycle 0; dispute: none 548, borderline
4, contested 0. A verdict under this spec is a statement about that
published-identification layer, not ground truth. The census counts in
this record are population signs keyed under the frozen route (gate
0.4's note: the route is many-to-one — 556 population signs to 424
distinct asset rows), which is why a kind's member-sign count can
exceed its count of asset rows.

**Cross-compilation caution (spec section 9.3).** Spec 037's census
found object-type labels diverging between the CISI volumes and the
programme's corpus in 49% of matched cases. That caution travels with
this result: depiction here is the published identification layer for
this compilation, constructed as Spec 073's answer to the caution —
restated, never presented as a refutation of the census.

## What was executed

1. **Step-0 gates (spec section 6), fail-closed, in order — all PASS.**
   Gate 0.1: both v2 freeze records present; Registry v2 and Asset A v2
   recompute to their digests, row counts and Asset A v2's per-kind and
   dispute counts equal to section 3's pins. Gate 0.2: the corpus and
   row-grades hash to the intake record's pins; the intake census
   reproduces (5,704 rows; 5,536 analyzable; grades 3,212 / 2,087 /
   405). Gate 0.3: the crosswalk, Registry v1, and the anchors recompute
   to their pins; the anchors asserted byte-identical before and after.
   Gate 0.4: the population reproduced exactly and keyed in full (above);
   token 999 recorded as the named exclusion. Gate 0.5: the census
   published before any kind rate, the floors applied — no kind TOO
   THIN — and the S1 borderline signs named. Gate 0.6: the freeze-order
   proof from the external records — the freeze digest recomputed from
   the frozen sources; PR #389 read merged at `fd9bd448` from the repo
   record; OSF jv74f read approved and public from the OSF record.
2. **The frozen section 5 battery, exactly.** Per kind: the pooled
   final-position rate against the frequency-matched comparison class,
   Fisher's exact test (two-sided) on the pooled 2×2, the verdict by
   section 5.2's bands, and the full per-sign table (every member sign's
   verbatim label, citations, total and final occurrences, its own
   rate, and whether it stands above the corpus-wide rate). Then the
   three sensitivities per kind, beside the primaries.
3. **Scored only in the frozen section 5.2 words**, carried in the
   section 5.5 wording forms in the machine record and the report.

## What this does NOT establish (spec section 9, binding)

- **No meaning conclusion.** Position is not meaning: no kind's word —
  supported, not supported, or inconclusive — says anything about what
  any sign means, marks, or was for.
- **Depiction is not ground truth.** The kinds are the published
  identifications under Spec 073's governing hierarchy, carrying Spec
  037's 49% cross-compilation caution.
- **Nothing about Spec 071's retired question.** The celestial arm
  republishes a settled finding in its proper place; this execution
  does not reopen, retest, soften, or satisfy the reopening trigger of
  the retirement, and Spec 071's claim stands UNTESTED exactly as
  recorded. The animal kind's NOT SUPPORTED here is this family's own
  per-kind word on its own question — not a verdict on Hunt's claims
  in any form.
- **Nothing about the unidentified signs or token 999.** They are
  counted and published as context (section 4.4); no claim is made
  about them, individually or as a group, and 999's exclusion is not
  a finding.
- **No independence from the sensitivities.** S1–S3 agree with the
  primaries; that agreement is reported as agreement on substantially
  the same excavated objects, never as corroboration from a second
  source.
- **No claim status or stage change beyond the dated appends.** The
  claim family's standing is amended only by the appends recorded in
  the machine record (`spec075_outcome_append_2026_10_25`); frozen
  and closed records are unedited (F075-C12).

## Landing

Execution PR: Phase-441 + the Spec 075 execution records — the
instrument and graph node, step0-record.md, outcome.md,
`reports/phase441_report.md`, `reports/phase441_results.json`, the
programme-ledger append, the regenerated foundation-check report, and
the execution tests — on genuine CI read from the run's own job
conclusions; the foundation posture at the merge is reported as
measured in the landing record appended to this file.

## Records

- `reports/phase441_results.json` — the machine record (contract,
  gates in order, the keying publication and its hash, the census, the
  four per-kind primaries with their per-sign tables, sensitivities
  S1–S3 in full, the verdict wordings, the claim-family appends, the
  anchors assertion; SHA-256
  `f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29`,
  byte-identical across the two runs).
- `reports/phase441_report.md` — the plain-language report carrying
  the section 10 headline block and the full per-kind tables.
- `specs/075-depicted-kind-endings-atlas/step0-record.md` — the
  step-0 record.
- `specs/075-depicted-kind-endings-atlas/osf-spec-registration.md` —
  the registration record (jv74f, approved; DOI
  10.17605/OSF.IO/JV74F), landed ahead of this execution.
- The claim-family appends `spec075_outcome_append_2026_10_25`
  (F075-C03, C05, C06, C07, C08, C11), recorded in the machine
  record's `claim_family_appends`.
- Anchors asserted byte-identical before and after
  (`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at
  both readings).

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.*
