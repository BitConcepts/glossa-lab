# Spec 037 — Freeze Record (CISI 3.1 concordance spine and HARP provenance annex)

> ## FROZEN — 2026-10-20
>
> This contract was frozen on 2026-10-20 under
> the owner's standing pipeline authorisation of
> 2026-10-20 (freeze order 038, then 037, then
> 039, then 040; `adjudication.md` §4). The AEE
> lifecycle hooks ran over the register first
> (register recovered to 0.7-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze also filed this spec's
> own OSF registration (DD-037-7;
> `osf-spec-registration.md`). Execution runs
> as **Phase-402** under this frozen contract.

## 1. Basis

The contract implemented is the study the CISI
3.1 intake assessed as its first two candidate
uses (intake report §7.5, 2026-10-20), over
material held under the Phase-130 gate
(restricted store PROVENANCE entry 22, recorded
before any processing): the portion PDF
(8,206,446 bytes, SHA-256 `514338b1…`) and its
extracted local table (2,123 records / 2,101
distinct catalogue numbers), against
`corpus_master` on `main` (SHA-256 `b19cfe95…`).

The position at freeze is stated plainly: the
pilot's 693 candidates exist as a count in the
intake record, and **no candidate has been
graded** — the verified rate this study exists
to measure is unknown at freeze, in either
direction. The freeze buys the measurement
under a ladder fixed before any join is
examined, plus — unless the halt rule fires —
the local spine, and the descriptive annex.
The fences are part of the basis, not
qualifications added later: a string match is
not a join; the concordance is a finding aid,
not evidence about readings; no prediction can
be scored from this material (it carries no
sign transcriptions); row-level products never
leave the restricted local store.

The freeze decided the open design proposals
(`adjudication.md` §4): **DD-037-5** (the
hand-check stratum is 60: 30 VERIFIED / 15
CONFLICT / 15 UNRESOLVED, the whole class where
a class is smaller, the seed recorded before
sampling), **DD-037-6** (Workstream B runs
inside Phase-402, gated on step 0 only), and
**DD-037-7** (this spec files its own OSF
registration; filed at the freeze,
`osf-spec-registration.md`). The halt threshold
(DD-037-4) is confirmed at 20% of all
candidates, and the phase allocation is
Phase-402 (DD-037-8).

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/037-cisi31-concordance-spine/freeze.md` (this
  document)
- `specs/037-cisi31-concordance-spine/spec.md`
- `specs/037-cisi31-concordance-spine/claims.json`
- `specs/037-cisi31-concordance-spine/adjudication.md`
- `specs/037-cisi31-concordance-spine/aee/freeze-aee-note.md`
- `specs/037-cisi31-concordance-spine/build_freeze.py`
- `backend/tests/test_spec037_freeze.py`

`plan.md`, `tasks.md`, and `outcome.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds).

## 3. What the freeze fixes

- **The ladder** (spec §4.3 / F037-C03): site
  mandatory; type mandatory where graded, seal
  and seal impression distinct classes; FC /
  excavation / museum corroboration under the
  fixed normalisation, contradiction = conflict;
  number-level ambiguity bars VERIFIED; exactly
  three outcome classes.
- **The census and the reporting set** (spec
  §§4.2, 4.4 / F037-C10, C11): all 693
  candidates graded; the aggregate set, its
  stratifications, and its named bases fixed;
  UNRESOLVED always its own class.
- **The halt rule** (spec §4.7 / F037-C05): a
  conflict share above the frozen threshold —
  20% of all candidates (DD-037-4) — halts the
  spine build; the pilot reports in full either
  way.
- **The gate handling** (spec §§2, 4.5, 7 /
  F037-C08, C09): row-level products in the
  restricted local store only; step 0's five
  verifications, fail-closed, before any join;
  repo cleanliness checked again before the
  outcome commit.
- **The annex limits** (spec §5 / F037-C12,
  C13): descriptive quantities as printed, the
  period-fill floor caveat attached, and no
  movement of the Spec 031 (Q7) record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
