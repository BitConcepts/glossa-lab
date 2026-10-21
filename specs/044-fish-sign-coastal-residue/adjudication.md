# Spec 044 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign plan,
>    approved by the owner AS WRITTEN on
>    2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
>    Parts 1–4 and 8 read in full at this draft).
>    The campaign commissions this draft:
>    member 2 (design D-02), Wave 1, asset
>    builders first; decision E-6 places Asset
>    F's build inside this spec; decision E-2
>    and requirement R-7 place this spec under
>    the Roif gate.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-02 found **RIPE** — "The CISI-based
>    layer and the gazetteer are in hand, and
>    Spec 039 put published site geography
>    further on record. The fish-family list it
>    shares with D-04 can be frozen at its own
>    step 0 from Parpola's published list; it
>    need not wait for D-04's freeze."
> 3. **The Roif verification (post-plan,
>    2026-10-21).** Roif's preprint IS publicly
>    posted on Academia.edu and citable. This
>    satisfies at most one of the campaign
>    Part 8 gate's two conditions; publication
>    of this spec's results remains a standing
>    GATE for the owner (claim F044-C14). The
>    verification is not a freeze order, not an
>    execution order, and not a publication
>    clearance.
>
> These inputs commission this **draft**. The
> freeze and the execution of Spec 044 are
> separate later owner acts, and — builders
> before dependents, campaign Part 4 — this
> spec's freeze precedes Spec 045's (D-04).

## 1. The adopted basis (operative substance)

- **The design.** D-02 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
  §D-02): the sign-by-sign residue of the
  fish/coastal-traders claim — per-member
  coastal shares against the corpus-wide
  coastal share, exact test per sign,
  family-wise correction, ENRICHED at corrected
  5% and ratio ≥ 1.5, occurrence floor 30,
  outcomes ENRICHED member found / NO MEMBER
  ENRICHED / TOO THIN.
- **The claim.**
  `indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`:
  SETTLED, partially falsified on the
  family-level coastal test; its
  not-understood text names this residue
  verbatim.
- **The asset.** Asset F, the fish-family list,
  built and frozen at this spec's step 0 from
  Parpola's published list (spec §4 contract),
  consumed by D-04 by digest (campaign E-6,
  Part 3).
- **The geography.** Coastal status from the
  Spec 027 Stage 0 gazetteer (pinned, spec §2)
  and published site geography, frozen at
  step 0 — the "better site classification"
  the residue names, replacing the original
  test's CISI-published site types for the
  primary.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
via the GitHub API against `main` (head
`82b29490…`); the local checkout was not used:

- **Design D-02** — read in full: the open
  point, hypothesis, falsifier, data, method,
  fixed criteria (floor 30; corrected test at
  5%; ratio ≥ 1.5; TOO THIN below two tested
  members), controls (excavation-size,
  contested sites), and the closing limit
  (no meaning conclusion).
- **Design D-04** — read in full: its data note
  fixes family membership "in advance from
  Parpola's published list (the record names
  Mahadevan signs 72, 64, 70, and the Phase-43
  test's six fish candidates)" — the numbering
  tension §3 derivation C05/C06 resolves.
- **The claim record** — read on `main`:
  manual_002's normalized claim, status
  partially_falsified, stage explained, its
  explanation (family counted in CISI-based
  data; no enrichment at Lothal/Dholavira) and
  its not-understood residue text. File
  recomputed to SHA-256 `bc22d6f0…` at this
  draft.
- **The original test's shape** — Phase-54's
  falsification battery (the M047
  site-enrichment prediction over CISI-keyed,
  site-attributed inscriptions) and Phase-46's
  header ("Phase-45 T6 found NO_ENRICHMENT for
  M047 at coastal sites (n=13, p=0.685)"),
  read on `main`. Claim F044-C02's boundary
  states exactly this scope.
- **The gazetteer** — `data/movement/gazetteer_rows.jsonl`
  recomputed at this draft to SHA-256
  `5ac76a30…`, matching Spec 039's carried pin;
  36 rows, 30 clusters per Spec 039's spec.
- **The Parpola list pin** — the program's
  Mahadevan–Parpola crosswalk file (recomputed
  to `9ebd7723…`) cites "Parpola, Asko. 1994b.
  Sign list (= Parpola 1994a fig. 5.1,
  pp. 70-78)" — the bibliographic pin spec §2
  and Asset F's `source_citation` carry.
- **The layer problem (recorded, not
  papered over)** — the Phase-45/46/54 scripts
  read `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`,
  a downloads-tree file **not present in the
  repository tree on `main`**; the repo's other
  CISI-derived layers include a 179-inscription
  corpus that is all Mohenjo-daro and cannot
  express a coastal contrast. Hence spec §2
  states no layer pin and gate 0.1 makes
  identification-and-pinning a fail-closed
  step-0 act (DD-044-3, OPEN-044-1).
- **Not done at draft, by design** — Asset F
  has **not** been built (no member is named
  anywhere in this draft), the coastal list
  has **not** been enumerated beyond the two
  sites the record itself names, no occurrence
  census has been computed, no count of any
  kind was made, no code was written or run,
  the AEE hooks have not run, and nothing was
  filed with OSF.

## 3. Double derivation of acceptance tests (doctrine requirement)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived **twice,
independently, from the claim alone** —
Derivation A from the claim's operative
sentence, Derivation B from its falsifier /
outcome side — and disagreements were resolved
in the draft, here. Agreements are recorded in
one line; disagreements in full.

| Claim | Derivation A (from the claim) | Derivation B (from the falsifier/outcome side) | Result |
|---|---|---|---|
| C01 | Inspect outputs for any statement beyond per-sign distribution in the pinned layer | Inspect outputs for the excluded statements (meaning, family verdict, other corpora) appearing anywhere | **Agree** — one inspection, both directions; the claim's falsification test is that inspection. |
| C02 | Recompute the claim file's hash and read manual_002's status | Check at close that no Spec 044 product edited/restated the family verdict | **Agree** — both are required; the claim carries both. |
| C03 | Run §5; hypothesis supported iff ≥1 tested member is ENRICHED | Run §5; hypothesis fails iff every tested member fails a criterion clause (→ C04) | **Agree** — complementary by construction; TOO THIN is neither, and is routed to C11, not silently to either side. |
| C04 | Outcome record carries NO MEMBER ENRICHED wording when condition holds | If any member is ENRICHED, C04's condition does not arise (→ ENRICHED MEMBER FOUND) | **Agree.** |
| C05 | Step-0 record exhibits Asset F in §4 form, locator per member | A member entered on a non-Parpola basis, or without a locator, breaks the asset (→ ASSET F FREEZE FAILED) | **Disagreement, resolved.** A reads D-04's record — "Mahadevan signs 72, 64, 70, and the Phase-43 test's six fish candidates" — as the membership list. B reads campaign Part 3 / D-02 — "frozen at its step 0 **from Parpola's published list**" — as the membership source. The texts conflict in numbering system and possibly in membership. **Resolution (DD-044-5):** Parpola's published list governs membership (the campaign plan, approved later and AS WRITTEN, is the governing text; D-04's parenthetical is its claim record's shorthand). Mahadevan numbers are carried as locators via the crosswalk. The Phase-43 six and the 72/64/70 trio are reported in the step-0 record as a cross-check against Asset F, with any divergence named — they do not add or remove members. OPEN-044-2 asks the freeze to confirm. |
| C06 | Digest recorded in step-0 record before census; recompute to verify | Any in-place edit shows as digest drift without a new version record | **Agree** — ordering check + drift check are the same record read two ways. One sub-point resolved: the digest excludes the `digest` field itself (§4.2), since a self-referential hash has no fixed point — Derivation A initially hashed the whole file; B's consumer-side recompute exposed the circularity. |
| C07 | Gate 0.1: identify, export, pin, reproduce the original population | A run counting on an unpinned/non-reproducing layer is non-compliant on its face | **Agree** — but see DD-044-3: neither derivation could name the layer as a repo file, because it is not one on `main`. The draft states that plainly instead of pinning a plausible-looking wrong file. |
| C08 | Gate 0.3 exhibits the frozen list with a per-site basis | A site classed by fish counts, or without basis, breaks the gate | **Disagreement, resolved.** A (from the claim record and Phase-45/46/54 scripts) fixes the coastal set as exactly {Lothal, Dholavira} — the original test's set. B (from D-02's data note) applies the rule — port or coastal zone — to every site in the layer, which may admit further sites. **Resolution (DD-044-7):** the design's rule governs the primary (the residue exists to use the better classification; freezing the old two-site set would re-run the original test's classification, not repair it), with Lothal and Dholavira members by name, every other admission carrying its gazetteer/geography basis in the frozen list, and comparability to the original test preserved by reporting the two named sites' results within the per-site sensitivity (§5b). OPEN-044-3 asks the freeze to confirm or to restrict the primary to the named pair, openly. |
| C09 | Gate verdicts precede quantities in the run record, in order | Any quantity preceding its gate falsifies compliance | **Agree.** |
| C10 | ENRICHED labels follow mechanically from the per-member tables | A near-miss member relabelled by dropping a clause falsifies the record | **Disagreement, resolved (×2).** (i) *Unit:* A reads "coastal share of its occurrences" as sign tokens; B reads the design's baseline phrase "corpus-wide coastal share of all inscriptions" as inscription units — the design mixes units in one sentence. **Resolution (DD-044-2):** the primary is token-consistent on both sides (a share compared to a share of the same kind of thing); the inscription-level version is a pre-registered sensitivity. (ii) *Correction:* A reads "family-wise correction" as Bonferroni (the literal family-wise bound); B reads it as Holm (uniformly more powerful, same family-wise guarantee). **Resolution (DD-044-4):** Bonferroni — the conservative literal reading, and the one a reader can recompute from the published tables without the tested set's p-value ordering. Both resolutions are OPEN-044-4 for the freeze to overturn before counting. |
| C11 | Headline derivable from gate record + tables alone | Headline must match §6's pre-written wording for its class | **Agree** — with one draft addition recorded: the design names three outcomes; the step-0 closure classes (ASSET F FREEZE FAILED / LAYER NOT PINNABLE / COASTAL LIST FAILED / INVALID) are this draft's fail-closed completion (DD-044-1), following Spec 042's NOT ADJUDICATED precedent. |
| C12 | All members' tables + all three sensitivities present at close | A headline following a sensitivity instead of the primary falsifies the boundary | **Agree.** |
| C13 | Inspect outputs for meaning/guild/trade claims | An enriched member presented as story-evidence falsifies compliance | **Agree** — one inspection, both directions. |
| C14 | Campaign public-surface audit finds nothing from this spec | Campaign reporting uses only the held-under-gate naming, no result content | **Agree.** |
| C15 | Every product carries layer label, Asset F digest, contested list | A product generalising across compilations falsifies the boundary | **Agree.** |

## 4. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   spec §2 pin re-asserted against the merged
   record — or decline, leaving the residue
   exactly as the claim's not-understood text
   states it: not run.
2. **OPEN-044-1 (layer of record).** Identify
   the CISI-based corpus layer of record — the
   database layer the original family-level
   test used — and confirm gate 0.1's
   identify-export-pin procedure is the right
   fail-closed form, or name the layer and its
   pin in the freeze record itself. The draft
   could not pin it (§2 verification record);
   the freeze must not proceed on an unidentified
   layer.
3. **OPEN-044-2 (Asset F source).** Confirm
   Parpola 1994's sign list (fig. 5.1,
   pp. 70–78) as Asset F's source and the
   per-sign locator form, and confirm
   DD-044-5's resolution (Parpola list governs
   membership; 72/64/70 and the Phase-43 six
   are a reported cross-check) — or name a
   different published Parpola list, with its
   pin, in the freeze record.
4. **OPEN-044-3 (coastal list scope).**
   Confirm DD-044-7 (rule-built frozen list,
   Lothal and Dholavira by name) or restrict
   the primary to the original test's named
   pair, openly, before any counting.
5. **OPEN-044-4 (test form).** Confirm or
   overturn DD-044-2 (token primary,
   inscription sensitivity) and DD-044-4
   (Bonferroni; Fisher one-sided), before any
   counting. Either may be changed at freeze;
   neither may be changed after.
6. **OPEN-044-5 (OSF).** Whether the frozen
   spec files its own OSF registration —
   under campaign decision E-1, every
   specification in the pass gets its own OSF
   contract registration at its freeze, so the
   proposal is **yes**, following Specs
   036–039. Nothing is filed at draft. Note:
   the OSF registration registers the frozen
   contract; it does not publish results, and
   the Roif hold (F044-C14) is unaffected.
7. **OPEN-044-6 (phase number).** Allocate the
   execution phase number at the freeze act,
   from the merged record as it then stands
   (DD-044-6).

## 5. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-044-1 — Step-0 closures complete the
  outcome set.** Design D-02 names three
  outcomes; the frozen-spec form requires a
  pre-written wording for every way an
  execution can end. The draft adds ASSET F
  FREEZE FAILED, LAYER NOT PINNABLE, COASTAL
  LIST FAILED, and INVALID as step-0 /
  integrity classes with §6 wordings (claims
  C09, C11) — the Spec 042 DD-042-3 precedent.
- **DD-044-2 — Token-consistent primary.**
  Both sides of the §5 comparison count sign
  tokens; the inscription-level version is a
  stated sensitivity (§3 derivation C10).
- **DD-044-3 — No invented layer pin.** Spec
  §2 pins what was verified and says why the
  corpus layer carries no pin at draft; gate
  0.1 does the pinning as a fail-closed act.
- **DD-044-4 — Bonferroni, Fisher one-sided.**
  The family-wise correction is Bonferroni at
  the 5% family level; the exact test is
  Fisher's, one-sided in the enrichment
  direction (§3 derivation C10).
- **DD-044-5 — Parpola's list governs Asset F
  membership.** Mahadevan numbers are
  locators; the claim-record shorthand lists
  are a reported cross-check (§3 derivation
  C05).
- **DD-044-6 — No execution phase number at
  draft.** Allocated at the freeze act.
- **DD-044-7 — The coastal list is rule-built
  and frozen, with the original pair named.**
  (§3 derivation C08.)
- **DD-044-8 — Evidence carries `observed_at`
  from the draft.** The cited facts were
  verified first-hand today (the Spec 042
  DD-042-4 precedent).

## 6. Design defects and ambiguities found at drafting

Recorded per the campaign rule that a defect
is reported, never repaired silently:

1. **D-02 says fish membership is "as frozen in
   D-04"; the campaign (E-6, Part 3) and the
   triage say D-02 builds Asset F and D-04
   consumes it.** The packet's direction is
   reversed by the later, governing texts.
   The draft follows the campaign (D-02
   builds, D-04 consumes by digest) and
   records the packet line as superseded by
   the approval — Spec 045's draft must not
   cite the packet line as its basis.
2. **The design's measure mixes units in one
   sentence** ("coastal share of its
   occurrences versus the corpus-wide coastal
   share of all inscriptions"). Resolved at
   DD-044-2; OPEN-044-4 puts it to the freeze.
3. **"Family-wise correction" and "exact test"
   are unnamed as to method and direction.**
   Resolved at DD-044-4; OPEN-044-4.
4. **The coastal list is said to be "frozen in
   the design" but the design enumerates no
   list** — only the rule, plus Lothal and
   Dholavira by example in the claim record.
   Handled by gate 0.3's freeze act and
   DD-044-7; OPEN-044-3.
5. **The "CISI-based corpus layer as held in
   the database" is not a file in the
   repository on `main`** (§2 verification
   record). The triage's "in hand" is true of
   the program's database posture, not of a
   pinnable repo artifact. Handled by gate
   0.1 and DD-044-3; OPEN-044-1. If the freeze
   finds the layer cannot be identified as
   the original test's, this spec's honest
   outcome is its pre-written LAYER NOT
   PINNABLE closure — that is a result, not a
   drafting failure.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
