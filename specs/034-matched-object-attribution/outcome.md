# Spec 034 — Outcome (Phase-398, executed 2026-10-13)

> ## EXECUTED — ATTRIBUTED TO COMPOSITION
>
> Execution of the frozen Spec 034 contract (freeze
> digest
> `696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a`;
> OSF registration https://osf.io/zd7uq/, DOI
> 10.17605/OSF.IO/ZD7UQ, approved and public before
> execution; registration record completed by PR
> #208) under the owner's 2026-10-13 order.
> Infrastructure PR #213. Full record:
> `reports/phase398_results.json` and
> `reports/phase398_matched_object_attribution.md`.

## Step 0 — the bridge census (gate arithmetic first)

Object pairs were built through the three frozen
routes, every pair cited data:

- **Route (a) — the CISI catalogue layer** (7,705
  rows; 3,493 distinct objects): attests **all 179**
  mayig-layer objects (all seals; 176 with site
  Mohenjo-Daro in the catalogue, 3 with the site
  blank on the catalogue row).
- **Route (b) — the Mahadevan side's published
  object references**, admitted through the
  Phase-130 intake schema (validation verdict:
  **pass**, 0 errors, 0 warnings; 5,018 inscriptions
  carrying a CISI reference, 4,074 distinct objects)
  and joined on `provenance.object_id` only:
  **179 matched objects** — every mayig object has
  exactly one ICIT inscription citing it, and no
  mayig object is left unmatched. Holdat
  `cisi_number` was never read and never used as a
  join key (F034-C06).
- **Route (c) — the 44 Phase-128 dossiers:** 61 of
  the gate objects carry a sign covered by a dossier
  (17 of the 44 dossier anchors touched). The
  dossiers contribute sign-level evidence, no object
  identity.

**The gate:** matched objects carrying texts of
three or more signs in both compilations: **169** —
the frozen gate is 150; **the gate passed**. Ten
matched objects fall below the text condition
(M-137: 1/1 signs; M-175: 3/2; M-60, M-96, M-150,
M-176, M-178, M-179, M-180, M-182: 2/2).
Sensitivity: counting only ICIT records the
Phase-116 build kept, the same figure is 159 — the
gate passes under both counts. Composition residue
at census level: 3,895 CISI objects are referenced
by the ICIT corpus but not transcribed in the mayig
layer; the mayig layer holds no object the ICIT
corpus fails to reference.

## Step 1 — the measurement

Phase-125's own measurement (total variation, count
floor 8, the 286 PRIMARY crosswalk pairs), computed
on the 169 matched objects only (mayig side: 169
inscriptions, 983 tokens, 180 signs; ICIT side: 169
inscriptions, 992 tokens, 150 signs):

- **Judgeable pairs: 25 of 286** (the corpus-level
  run had 16).
- **Matched-object median TV: 0.025694** (median W1
  the same; modal-class agreement share 1.0;
  Spearman ρ initial 0.898039, medial 0.932164,
  terminal 0.850948; pairing-shuffle null p = 0.001,
  null median of medians 0.25).
- Largest per-pair distance among the judgeable:
  P144/M086 at 0.270349 — below the transcription
  line; 4 judgeable pairs sit at exactly 0, and 15
  of the 25 at or below 0.05.

## The verdict (spec §6, lines fixed in advance)

**ATTRIBUTED TO COMPOSITION.** The matched-object
median TV of 0.025694 is at or below the frozen 0.20
line. On the same physical objects, the two
compilations' positional profiles agree almost
exactly; the corpus-level disagreement of 0.636931
is carried by the objects' composition — the two
compilations publish different inscriptions — not by
transcription of shared objects. In Phase-131's
persistence estimator, the matched-object residual
is **0.040340** of the corpus-level distance (against
Phase-131's 0.938679 unexplained share, which was
measured without an object bridge). The falsifier
did not fire: matched-object disagreement did not
remain anywhere near half the corpus-level distance
(0.32).

Subset description (carried with the verdict per
§7): the 169 matched objects are **all Mohenjo-daro
seals** — the CISI vols 1–2 object population
transcribed in the mayig layer — with Mahadevan-side
readings from the ICIT published corpus. Against the
full mixes (ICIT kept layer: 46.3% Harappa, 34.9%
Mohenjo-daro, seals 35.2% of types; Holdat layer:
36.3% Mohenjo-daro, 29.5% Harappa), the matched
subset is a single-site, single-type slice, and the
attribution is a statement about that slice.

## The decomposition (Phase-131 categories)

Of the 169 gate objects, **29 are decomposition-
eligible** under Phase-131's all-or-nothing PRIMARY
mapping (140 carry at least one Parpola sign outside
the 286-pair primary map — the same eligibility rule
that admitted 32 of 179 in Phase-131). Over the 29:
pair classes — **identical 22, order-only 1,
substitution 6**. The one order-only object (M-67)
carries the same signs in both compilations, rotated
by one position — a reading-start difference, not a
sign difference.

Difference-block token shares (Phase-131's
estimators, over 22 difference-block tokens):
**segmentation 0.0, substitution 0.909091,
insertion/deletion 0.090909**. The 10 substituted
positions were checked against the crosswalk as a
record of disagreement (never ground truth): **0 are
crosswalk conflict pairs, 0 are crosswalk-attested
alternatives, 10 have no crosswalk row** — they pair
a Parpola sign with a Mahadevan sign the crosswalk
does not list for it at all. Three difference blocks
involve an ICIT-side UNK (an attested position whose
sign the conversion could not map). Per-object
distances over the 29: median 0.0, p75 0.0, maximum
0.428571 (M-105).

The decomposition is a statement about the 29
mappable objects; the attribution verdict itself
rests on the profile measurement over all 169.

## Per-claim determinations (F034 register; the frozen register is not edited)

- **C01 — HELD.** The outcome attributes the
  residue only; no compilation is crowned (§8).
- **C02 — SUPPORTED.** The hypothesis (composition
  over transcription on matched objects) is the
  measured result: median TV 0.025694.
- **C03 — DONE.** The bridge was built through
  routes (a)–(c) as cited data; counts above.
- **C04 — MET.** 169 ≥ 150, with the ≥3-sign
  condition applied per object on both sides.
- **C05 — NOT TRIGGERED.** The gate passed; the
  TOO THIN closure was armed, and the census that
  would have been its finding is published anyway.
- **C06 — HELD.** Holdat `cisi_number` never used
  as a join key; the build tests carry a namesake
  fence for exactly this.
- **C07 — DONE.** Phase-125's distance and count
  floors, on the matched subset only, via its own
  `evaluate_arm` machinery.
- **C08 — DONE.** The decomposition uses
  Phase-131's alignment, block classes, and share
  estimators.
- **C09 — THE OUTCOME.** 0.025694 ≤ 0.20:
  ATTRIBUTED TO COMPOSITION.
- **C10 — NOT MET.** The transcription line (0.32)
  was not reached; the falsifier did not fire.
- **C11 — NOT TRIGGERED.** The median did not fall
  between the lines.
- **C12 — DONE.** The selection-bias mixes are
  reported (results JSON, `selection_bias`) and
  the verdict statement carries the subset's
  description.
- **C13 — HELD.** The crosswalk served as the
  frozen comparison frame and as a record of
  disagreement in the substitution check; never
  as ground truth.
- **C14 — HELD.** Nothing was written into the
  Phase-125/127/131 records; the anchors file is
  asserted byte-identical before and after the run
  (sha256 `eccea6d5…`, in code).

## What remains not understood

Why the residual differences that do exist take the
form they do: the 10 substitutions pair signs with
no crosswalk row at all, and neither this study nor
the crosswalk explains them; the corpus-level
composition attribution does not say which
compilation's *selection* of objects better
represents the script's population (a question this
design never asked); and the 140 objects the
PRIMARY map cannot carry remain unexamined at
object level — a fuller crosswalk, not a different
verdict, is what they wait for. The settled
Phase-125 verdict stands exactly as issued.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
