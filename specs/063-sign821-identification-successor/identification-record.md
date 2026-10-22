# Spec 063 / Phase-425 — Identification record (EXECUTED 2026-10-22)

> The evidence of the execution: the step-0 gate
> record (spec §3), both step D derivation sheets
> and the reconciliation with the comparison
> against the preserved descriptor (spec §5,
> step D), the step C continuity statement (step
> C), and the step M route record with the traps
> asserted (step M). The outcome record is
> `outcome.md` in this directory; the run's
> machine record is `reports/phase425_results.json`
> (SHA-256
> `c7b246e94258519e251acaf3a97179de02da1e453f01ef37945cca2a48737752`),
> produced by
> `backend/scripts/phase425_sign821_identification.py`,
> which verified every repository-side fact these
> sheets rest on — the formation passage verbatim
> in the pinned held text, the P378 anchor row,
> the registry and witness facts, the Figure 2.6
> caption lines — before any outcome was written;
> a second run reproduced both machine outputs
> byte-identically. **No image is committed
> anywhere in this spec**: the plate was produced
> from the pinned local thesis file at gate 0.3,
> read, and recorded here in text only.

## 1. The preserved reference (spec §8, element 1)

- **File:**
  `specs/063-sign821-identification-successor/drawn-form-reference-821.json`
- **Schema:** `glossa.drawn-form-reference/1`
- **SHA-256 (freeze-pinned, recomputed at gate
  0.1):**
  `695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999`
  (5,689 bytes)
- **Target:** Wells (2011), as given in Wells
  2015, Chapter 2 / Figure 2.6, sign 821;
  list-naming evidence at held-text lines 414
  and 665.
- **Descriptor of record (the drafted wording,
  compared only after reconciliation, §6
  below):** "Sign 821 is the doubled form of
  sign 820: two identical oval outlines side by
  side, touching at the vertical midline, each
  oval divided by three straight diameters (one
  vertical, two diagonal) into six sectors —
  two six-spoke wheels in oval outlines, side by
  side."

## 2. Step 0 — the gate record (spec §3; all passed)

- **0.1 Input integrity — PASS.** Every §2
  input recomputed at the run's base and equal
  to its freeze-record value: held cleaned text
  `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e`;
  crosswalk registry
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`;
  Phase-123 witness
  `ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da`;
  Spec 056 freeze file
  `8a7d13904d3e06cca0fcabbc0ab9d25af7c72176c5e1d7f3bdb957fd9075d759`
  (its digest
  `64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e`);
  Spec 056 outcome
  `ff16184aa265b68358865c51e8f43dc9c9ec40688a53614792640f1d2e2d844e`;
  Spec 056 extraction record
  `ad4a3f747d6ae4e0f13ae984c1169bd4a94570625e7dcc199146ff2ef73fb6ab`;
  Phase-104 evaluation
  `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d`;
  lane-2 drafts
  `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb`;
  anchors
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`;
  preserved reference `695dd35d…` (above). The
  Spec 063 freeze record's own digest asserted:
  `dc24a10ec177d5f1eb3b73d29ab6f646b4c77b02ae30da2ca86002cc57a49ed9`.
  The claim record was asserted in the Spec 038
  form: its freeze-time hash
  `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a`
  stands as the definition constant in the Spec
  063 freeze.json, and the fragment's facts were
  asserted on the live file — entry present
  (`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001`),
  wording "Sign value: 821 / it is used in a
  variety of contexts (Figure 6", status
  UNTESTED, stage created, and the appended
  `spec056_closure` entry present with outcome
  IDENTIFICATION FAILED. The passage of record
  (held-text lines 2783–2871) recomputed to
  5,354 bytes, SHA-256
  `51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604`.
- **0.2 Thesis file asserted — PASS, before any
  plate was read.** The local file
  `Wells2006_PhD_EpigraphicApproachesToIndusWriting.pdf`
  (held locally under
  `downloads/wells-phd-thesis-2006/`; open
  deposit, not committed) recomputed to SHA-256
  `4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e`,
  19,313,853 bytes — the frozen pin exactly.
  No other copy, edition, or download was used
  at any point.
- **0.3 Reference producible — PASS.** The
  preserved reference stands at its pinned
  digest (§1), and the plate page — thesis
  p. 92 / PDF p. 104, Figure 3.2, "The Indus
  signs by sign number" — was produced from the
  pinned local file asserted at gate 0.2: the
  file carries 296 PDF pages; page 104's
  embedded plate image (`Im106.tiff`, 47,034
  bytes, SHA-256
  `961ed7de59d45ccb8faa2262b537c2d5912bc9830f8a0c3bf3256807e94f08ee`)
  was extracted from that file and rendered for
  the step D readings. The render was an
  execution artefact only; no image is
  committed.

## 3. Derivation A — sequential plate read

**Method.** The plate was read row by row in
plate order. At the row of signs 804–830 the
entry labelled 821 was read in sequence — after
817, 818 and 820 — and its strokes were
recorded before it was compared with any other
entry; the named neighbours were then read on
the same plate for the discrimination list.
This sheet was made without sight of
Derivation B's sheet and without sight of the
preserved record's drafted descriptor wording.

**Plate locator.** Wells 2006, PhD thesis,
Figure 3.2, "The Indus signs by sign number",
thesis p. 92 / PDF p. 104; row of signs
804–830; the entry labelled 821 is the fourth
entry of the sub-row 817, 818, 820, 821, 822…

**Feature list.**

- *Outline:* two separate oval outlines, both
  tall (vertical) ovals, standing side by side
  and touching at the vertical midline.
- *Stroke count:* 8 stroke elements in total:
  2 oval outlines, and inside each oval 3
  straight diameters.
- *Internal divisions:* in each oval, one
  vertical diameter and two diagonal diameters,
  all crossing at the centre; the three
  diameters divide the oval into 6 sectors.
- *Doubling structure:* the left and right
  ovals are identical in outline and in
  internal division; the pair is one sign made
  of two copies of the single oval that stands
  at 820 on the same row.

**Descriptor A.** "Two identical vertical oval
outlines side by side, touching at the vertical
midline, each divided by three straight
diameters (one vertical, two diagonal) into
six sectors."

**Neighbour discriminations (A).**

- *818:* a single round outline (a circle, not
  an oval) with one vertical and one horizontal
  diameter — 4 sectors; single, not doubled.
- *820:* a single vertical oval with the same
  three diameters and six sectors — the single
  form; one outline only.
- *822:* one six-sector oval of the same kind,
  flanked by paired vertical strokes on both
  sides; one outline, not two.
- *823:* a single oval whose internal strokes
  cross more densely than six sectors (a
  latticed interior); one outline.
- *791:* two plain vertical ovals side by side,
  touching, with no internal strokes at all — a
  doubling without the spokes (read on the row
  above, signs 786–803).

## 4. Derivation B — neighbour-contrast read

**Method.** The named neighbour set was read
first — 791, 818, 820, 822, 823 — and what each
entry is was recorded; the entry labelled 821
was then read against that recorded set,
feature by feature. This sheet was made
without sight of Derivation A's sheet and
without sight of the preserved record's
drafted descriptor wording; the drafted
wording is compared only at reconciliation, by
the protocol.

**Plate locator.** As Derivation A: Wells
2006, PhD thesis, Figure 3.2, thesis p. 92 /
PDF p. 104; row of signs 804–830; 821 the
fourth entry of the sub-row 817, 818, 820,
821, 822…

**Feature list.**

- *Outline:* a pair of tall oval outlines in a
  row, touching at the middle vertical edge.
- *Stroke count:* each oval carries 3 internal
  straight strokes through its centre —
  counted: one upright, two slanting; 2
  outlines and 6 internal strokes in all.
- *Internal divisions:* the 3 strokes in each
  oval cut it into 6 wedge-shaped sectors,
  evenly angled around the centre.
- *Doubling structure:* exact repetition: the
  right oval repeats the left in size, outline
  and internal strokes; together they are twice
  the single entry at 820.

**Descriptor B.** "A doubled sign: two copies,
side by side and touching, of a vertical oval
divided by a vertical and two diagonal
diameters into six sectors."

**Neighbour discriminations (B).**

- *818:* one circle only, cut by a vertical
  and a horizontal stroke into 4 sectors —
  rounder, fewer sectors, not doubled.
- *820:* the single oval itself: one outline,
  three diameters, six sectors — the form the
  target doubles.
- *822:* a single spoked oval with pairs of
  vertical strokes standing outside it on both
  sides — the extra strokes are outside the
  oval, and there is only one oval.
- *823:* one oval whose interior is a denser
  lattice of crossing strokes, not six even
  sectors.
- *791:* a pair of empty ovals side by side —
  two outlines and no internal strokes at all,
  so the pair alone does not make the target:
  the target's ovals are spoked.

## 5. Reconciliation (by the recorded features)

- *Outline:* AGREE — both sheets record two
  tall oval outlines.
- *Arrangement:* AGREE — side by side,
  touching at the vertical midline.
- *Stroke count:* AGREE — 3 straight diameters
  inside each oval; 8 stroke elements in total
  (2 outlines + 6 diameters).
- *Internal divisions:* AGREE — one vertical
  and two diagonal diameters per oval, dividing
  it into 6 sectors.
- *Doubling structure:* AGREE — the two ovals
  are identical copies; the pair is the doubled
  form of the single entry at 820.
- *Neighbour discriminations:* AGREE on all
  five named neighbours (818, 820, 822, 823,
  791): each sheet records the same
  discriminating feature for each — 818 a
  single 4-sector circle; 820 the single oval;
  822 a single spoked oval flanked by paired
  vertical strokes; 823 a single oval with a
  denser-crossed interior; 791 two plain ovals
  with no internal strokes.

No disagreement arose between the sheets,
settled or unsettled, so the
against-identification rule (DD-056-14,
carried) was not needed.

**Reconciled descriptor.** "Sign 821 is two
identical vertical oval outlines side by side,
touching at the vertical midline, each oval
divided by three straight diameters (one
vertical, two diagonal) into six sectors — the
doubled form of the single six-sector oval
wheel at 820."

## 6. Comparison with the preserved descriptor

Feature by feature, the reconciled descriptor
and the preserved record's descriptor (§1)
state the same drawn form: two identical oval
outlines, side by side, touching at the
vertical midline; three straight diameters per
oval (one vertical, two diagonal); six sectors
per oval; the whole the doubled form of sign
820. The preserved record's discriminators
were each re-read on the plate by both
derivations and held. **Agreement — no
material difference.** The preserved
descriptor is therefore SUSTAINED at step D:
checked, not inherited.

**Step D result: PASS.**

## 7. Step C — continuity statement (821, by anchors)

What anchors the plate number to the 2011/2015
numbering, stated from the record:

1. **The formation passage.** The 2015 book's
   own Appendix II, "Doubled Signs" (printed
   pp. 128–129; held-text lines 3691–3704,
   heading line 3691), states, verbatim
   (lines 3692–3694, verified against the
   pinned held text by the phase script):
   "Signs can appear sometimes doubled. For
   example, sign 090 is doubled to form sign
   091 and sign 820 doubles to form sign 821.
   Double signs are not coded in the
   inscriptions as a pair of the single sign
   (i.e. 090-090), but are treated as a new
   sign." And (lines 3703–3704): "The second
   example is sign 820, a typically in the
   initial position. The doubled sign 821 is
   still often initial, but also frequently in
   late medial or terminal position."
2. **The registry's 2015-form cross-match.**
   Registry row **P378** carries `wells_ids`
   W820, `mahadevan_ids` M391, description
   "Wheel with 6 spokes with even angles" —
   the base sign in the 2015 numbering,
   described by its drawn form.
3. **The plate agreement.** Both step D
   derivations read the thesis plate at 820 as
   a single six-sector wheel in an oval outline
   (three diameters, six even sectors — the
   drawn form P378's description states), and
   at 821 as that wheel doubled.

The formation passage, the registry anchor,
and the two step D derivations all agree on
the doubled six-spoke-wheel form at 820/821.
The plate number by itself anchors nothing and
was used only to locate the entries; this
check rests on the anchors' agreement.

**Step C result: PASS — continuity is
sustained on the anchors' agreement.**

## 8. Step M — the match (routes, in the frozen order)

- **Route 1 (registry, by drawn form) —
  ATTEMPTED, FAILS.** The pinned registry
  (803 rows) was searched on its drawn
  descriptions: no row carries W821 in any
  form, and no row's description states the
  reconciled drawn form. The registry's only
  two "6 spokes" descriptions are **P378**
  ("Wheel with 6 spokes with even angles" — a
  SINGLE wheel: the base sign 820, `wells_ids`
  W820) and **P379** ("Wheel with 6 spokes with
  even angles, two tall vertical strokes on
  left, all caged by four small vertical
  strokes" — a SINGLE flanked wheel, the
  plate's 822 form; `wells_ids` empty). Nine
  rows in all describe a wheel (recorded in
  full in the machine record); none describes
  two six-spoke wheels side by side. The run
  did **not** fall back to P378, which is the
  base sign, not the target.
- **Route 2 (the list's own entry, through
  the preserved reference) — SATISFIED; THE
  ROUTE THAT IDENTIFIES THE SIGN.** The
  preserved reference record (§1) exists at
  its freeze-pinned digest, was sustained at
  step D (§6), and is anchored at step C (§7);
  it is cited here as the preserved drawn-form
  reference for the source list's own entry —
  Wells 2011, as given in Wells 2015,
  Chapter 2 / Figure 2.6, "An Indus Sign
  List", printed pp. 19–22 (held-text captions
  at lines 868, 872, 876, 880, verified
  against the pinned held text by the phase
  script). The sign list is named from the
  document itself: "Chapter 2 gives the Indus
  sign list used in this analysis" (held-text
  line 414); "The sign list used here (Wells
  2011)" (line 665).
- **Route 3 (composition) — NOT USED.** The
  frozen routes are taken in order and exactly
  one route identifies the sign; route 2
  satisfied the match, so route 3 was not used
  as the route of identification. (The
  formation passage and the plate confirmation
  appear in this run as step C anchors and as
  step D's plate, which are distinct acts from
  a step M route.)

**Traps asserted, by name (every run record):**

- **`Yunmapped_0821`** — registry row:
  `numbering_system` `yajnadevam_glyphid`,
  `wells_ids` empty, `corpus_freq` 10,
  description empty. A Yajnadevam glyph
  identifier — a number collision, not Wells's
  821. Asserted as a trap; never used as
  evidence or as a match.
- **Sign 861** — the passage's Fuls paragraph
  (held-text lines 2848–2853; Figure 6.12,
  "person in front of a structure") associates
  sign 861 with "city" as a DIFFERENT sign: a
  reading-confusion trap for K-1. No evidence
  about 861 was used to identify 821, and this
  identification lends no support to any claim
  about 861.
- **P378 used as the target's match** — P378
  is sign 820's registry row (the base sign).
  It is used in this run only as the base-sign
  anchor at step C; it is not, and was not
  used as, the target's match.
- **Number-only matching in any form** — none
  was used: the registry search ran on drawn
  descriptions, and the plate number was used
  only to locate the plate entries, with
  continuity established at step C on the
  anchors' agreement — never a plate number
  read without step C.

## 9. The recovery test for K-1 (spec §4)

- **R-1 PASS** — of record in Spec 056's
  executed record (the passage's own
  suggestion, in its own words). Not re-run
  under this spec (DD-063-2).
- **R-2 PASS** — of record in Spec 056's
  executed record (a specific reading —
  "city", determinative or word — in the
  stated Dholavira signboard contexts). Not
  re-run (DD-063-2).
- **R-3 PASS** — run afresh under §5 on the
  new record: list named from the document
  itself; step D sustained; step C passed;
  step M satisfied by route 2.
- **R-4 PASS** — of record in Spec 056's
  executed record. Falsification condition,
  from the passage's own logic: the claim
  counts as falsified if sign 821 in Dholavira
  signboard contexts is shown to carry a
  different established value, or if the
  signboard sequence's locative (place-name)
  element is shown to be carried by other
  signs, with sign 821 outside it — either
  result removes the basis the passage itself
  states for the "city" suggestion. The
  passage rules one observation out as a
  falsifier in its own words: the
  non-attestation of eyil-ay or eyil-i
  (collocation with sign 740) is expressly
  "not a nullification of the reading", so
  that absence cannot serve as the condition.
- **R-5 PASS** — of record in Spec 056's
  executed record (the Dholavira signboard
  contexts; the determinative-or-word
  alternative; all four candidate glosses with
  their DED numbers — DED 752 ūr, DED 808
  eyil, DED 3568 nakar, DED 4112 pāri; the
  eyil preference with its reason; and the
  passage's hedge). Not re-run (DD-063-2).

Candidate K-1's verbatim quote (verified
verbatim against the pinned passage by the
phase script): "It is suggested here that sign
821, in the Dholavira signboard contexts, has
a meaning of ‘city’, either as a determinative
or as a word." (Wells 2015, printed p. 92;
held-text lines 2835–2836.)

**Outcome: RECOVERED** — K-1 passes R-1
through R-5 on the new record, R-3 satisfied
under §5 by route 2.

**Fence sentence (spec §8, element 8).** "This
act is identification on a preserved reference.
It establishes, at most, whether the drawn sign
candidate K-1 names is identified in the
program's claim form — never whether K-1's
suggested meaning is right, and nothing about
sign 821 itself beyond the identification."

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
