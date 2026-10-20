# Spec 037 — Freeze Record (CISI 3.1 concordance spine and HARP provenance annex)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-20
>
> This record is finalised at the freeze act.
> The digest in `freeze.json` at this draft is a
> **draft digest**, computed by `build_freeze.py`
> over this draft contract (register 0.5-draft)
> under the owner's draft order of 2026-10-20
> (`adjudication.md`). At the freeze act — on the
> owner's freeze order — the AEE lifecycle hooks
> run over the register first, and the digest is
> recomputed **exactly once** over the recovered
> register and the finalised freeze texts (the
> Spec 035 ordering). The draft digest decides
> nothing and is not the freeze digest.

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

The draft-stage position is stated plainly so
the freeze decision is made with open eyes: the
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

The freeze also decides the open design
proposals (`adjudication.md` §3): **DD-037-5**
(the hand-check stratum size), **DD-037-6**
(Workstream B's placement; recommended: inside
Phase-401, gated on step 0 only), and
**DD-037-7** (whether this frozen spec files
its own OSF registration; proposal: yes,
following the Spec 027/030 study-design
pattern). The halt threshold (DD-037-4) is
confirmed at the freeze — or changed openly,
before any join is computed, with the change
recorded in `adjudication.md`.

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

## 3. What the freeze would fix

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
  20% of all candidates as drafted — halts the
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
