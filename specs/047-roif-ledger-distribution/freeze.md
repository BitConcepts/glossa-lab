# Spec 047 — Freeze Record (Roif's Ledger Thesis: the Distribution Test, Design D-09)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan approved
> by the owner as written on 2026-10-21 (the
> campaign's Wave 2 freeze wave; `adjudication.md`
> §§1, 7). The AEE lifecycle hooks ran over the
> register first (register recovered to 0.7-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-047-8;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-406**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no site has been classified, no ledger-sign list
> has been extracted, and no inscription has been
> counted.

## 1. Basis

The contract implements design D-09 (campaign
member 8) under the campaign plan's decisions
E-2/E-6 and requirements R-2/R-7: the
distribution test the Phase-104 record of claim
`indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
proposed and could not run (verdict
*stays untested*, rule RULE-SITE — no
site-function classification existed), with the
missing classification built inside this spec's
step 1 as shared **Asset B** for the D-10
specification to consume by digest pin. Only the
thesis's distribution component is tested; the
guild-authority and Akkadian-influence components
are carried as explicitly untested (spec §1,
§11; F047-C05).

The freeze decided the open points
(`adjudication.md` §7): **DD-047-8** (the spec
files its own OSF contract registration at the
freeze, under campaign E-1, with the Roif-gate
reading confirmed — the registration carries the
frozen contract, a design text, and no result),
**DD-047-9** (no second corpus layer runs under
this contract), **DD-047-10** (the permutation
seed is 20261021), **DD-047-11** (D-10 proceeds
under its own gates against a frozen-but-thin
Asset B), **DD-047-12** (the spine-only
population is confirmed), **DD-047-13** (the
all-UNMAPPED ledger case proceeds on measure (a)
alone under the amended partition of spec
§6.3), **DD-047-14** (the §4.3 verification pass
suffices as the classification audit),
**DD-047-15** (the execution phase is
Phase-406), and **DD-047-16** (the DD-038-10 /
DD-037-9 AEE gate reading adopted). DD-047-1
(thinness is a test gate, not a build gate) and
DD-047-2 (an empty side fires the same
classification gate) are **confirmed** as
drafted.

## 2. Pin verification (two routes, at the freeze)

This spec's draft carried a pin incident (four
wrong pins, corrected on its record;
`adjudication.md` §2). The freeze therefore
re-derived **every** §2 pin in the foreground by
two independent routes — the contents-API raw
route and the git-blob route — both at the
merged record (`main` at
`83b6a563402b02809ab1143848e4dd2c0cfd9de3`). The
two routes agree byte-for-byte on every file,
and every recomputed hash equals its pin:

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `data/movement/gazetteer_rows.jsonl` | `5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6` | 38,019 |
| `backend/glossa_lab/data/yajnadevam_inscriptions.csv` | `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` | 1,204,144 |
| `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv` | `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2` | 24,860 |
| `glossa-indus/reports/phase104_claims_evaluation.json` | `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` | 17,475 |
| `backend/scripts/seed_citations.py` | `39d28112e21151ccba0f5a370801c78d87575c6ff61695bb8fafc5c14c08b8f9` | 12,946 |
| `glossa-indus/hypotheses/models/roif_guild_ledger.yaml` | `c5f08461cc1a37b91cb5a17981e2e4d7c02958312e1e7b6b9a49618a154c9586` | 5,430 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |
| `specs/027-movement-culture-language/spec.md` (register evidence pin) | `7fff5d5a90b0af5697afa17a631e6901702b521f7e61c3c2bb444f08e369f9b0` | 45,774 |

The facts the design rests on were re-read from
the pinned bytes in the same pass: the gazetteer
carries 36 rows over exactly 30 distinct
`program_site_id` clusters; the primary layer
carries 5,679 records under a header with `site`
and sign-sequence columns; the Phase-104 entry
for the claim reads *stays_untested* under
RULE-SITE with its site-typology reason verbatim;
the citation record's `roif_indus_ledger` key
carries "Roif, A.", Academia.edu, empty year,
empty DOI, and the Academia.edu root as its URL;
and the hypothesis-model file carries the §2.2
defect as recorded (a malformed `document_id`;
a `doi` matching neither Academia.edu posting).
`backend/tests/test_spec047_freeze.py` pins all
of these facts so later drift fails loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/047-roif-ledger-distribution/freeze.md` (this
  document)
- `specs/047-roif-ledger-distribution/spec.md`
- `specs/047-roif-ledger-distribution/claims.json`
- `specs/047-roif-ledger-distribution/adjudication.md`
- `specs/047-roif-ledger-distribution/aee/freeze-aee-note.md`
- `specs/047-roif-ledger-distribution/build_freeze.py`
- `backend/tests/test_spec047_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-047-8: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The component fence** (spec §1 / F047-C01,
  C05, C19): the distribution component only;
  guild authority and Akkadian influence stay
  untested; no outcome states a ledger entry, a
  guild, or a meaning.
- **The Asset B contract** (spec §4 / F047-C06
  to C12): the 30-cluster spine universe; the
  closed six-class vocabulary with its mapping
  rule; the pooled ADMIN-TRADE-GATEWAY grouping
  against the domestic/ritual contrast; the
  two-source agreement rule with per-source
  mapping, citation and locator, and the
  verification pass; dispute handling by rule
  with no tiebreak (`DISAGREED` / `SINGLE-SOURCE`
  / `NO-SOURCE` / agreed `mixed/unknown`, all
  listed by name and excluded); the circularity
  and blindness discipline; the step-1 freeze
  point with digest pinning for dependents and
  the unsound-asset rule; and the fail-closed
  build gates B1–B4. Thinness is not a build
  gate (DD-047-1, confirmed).
- **The ledger-sign list's construction** (spec
  §5 / F047-C13): extraction from the two
  Academia.edu postings of record only, under
  the explicit-economic-function rule, with
  UNMAPPED entries excluded by rule and the
  extraction census published; the all-UNMAPPED
  case ruled (DD-047-13) and its amended
  partition frozen in spec §6.3.
- **The step-0 gates** (spec §3 / F047-C14):
  input integrity, spine reproduction, and the
  join census, each stopping the run as INVALID
  before anything is built or counted.
- **The test** (spec §6 / F047-C15 to C17): the
  shares design (R and R_ledger), the 9,999-shuffle
  permutation test at the 5% level with the seed
  fixed at this freeze (20261021, DD-047-10), the
  12-testable-site classification gate with the
  empty-side clause (DD-047-2, confirmed), the
  mechanical verdict partition, and the
  sensitivities reported beside the primary,
  never verdict-changing. One corpus layer only
  (DD-047-9).
- **The verdict wordings** (spec §7): every
  outcome in the partition, plus CLOSED AT
  STEP 1 and INVALID, pre-written before any
  site is classified or any inscription counted.

## 5. What the freeze does not do

- **It does not build Asset B.** The freeze pins
  Asset B's *contract* (spec §4) — the asset
  itself is built at execution step 1, inside
  Phase-406, and frozen there by its own digest.
  No site has been classified, and no
  classification exists anywhere at this freeze.
- **It extracts no ledger-sign list and counts
  nothing.** No per-site count, share, ratio, or
  permutation quantity has been computed.
- **It changes no verdict.** The claim stands
  UNTESTED on its Phase-104 record, which stands
  unedited; this spec's outcome will append to
  that record as a dated entry at execution.
- **The Roif publication hold stands (R-7).**
  This spec's records are internal; nothing
  derived from its results is surfaced on any
  public surface, and campaign reporting names
  this member only as "executed — held under
  the Roif gate". Publication remains the
  owner's separate GATE act. The OSF
  registration filed at this freeze carries the
  frozen contract (a design text) only — it
  carries no result and clears nothing under
  the gate.
- **It does not freeze D-10.** The D-10
  specification is a separate later draft and
  freeze; this act gives it the Asset B contract
  to be drafted against (and, per DD-047-11, the
  ruling that a frozen-but-thin Asset B does not
  close it).
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  awaits the parent's approval click completing
  the OSF registration's approval act, and a
  separate execution order (§3's gate note;
  DD-047-8).

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec047_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.7-draft` →
`0.7-MUTATED`) and the suite was run — the
freeze-replay test and the register-integrity
test went red, as they must, because a covered
source no longer matched its frozen hash and
the register no longer carried its frozen
version. The file was then restored
byte-identically (its SHA-256 re-verified
against the value recorded in `freeze.json`'s
sources) and the full freeze suite was run
again green. The mutation touched no committed
byte; the frozen record replays exactly over
the restored tree.

## 7. OSF registration and the execution gate

Under DD-047-8 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-406, the Asset B contract, the
step-0 and build gates, the pre-registered
measures and verdict partition, the freeze
rulings, and the Roif hold stated as a limit on
results rather than on the contract. The filing
record is `osf-spec-registration.md`, completed
by append after filing. The registration stands
**pending approval** after filing; its approval
act is the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution
(Phase-406) does not begin while the
registration stands pending: it awaits that
approval act and a separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
