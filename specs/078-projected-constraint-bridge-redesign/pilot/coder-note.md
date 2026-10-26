# Coder's note — Spec 078 (Method M13) successor pilot, step 3′ positive control

Blind coding of the 94 strict-core signs in `strict-coding-input.json`, using only each sign's `basis` text and rules NC-1 through NC-8. One coding is recorded per component per sign; where a basis restates the same position at the same sample size (for example a Round assignment followed by a "consistent X (n=…)" upgrade line), both statements are listed in `assertions` and the component is coded once.

## Counts

- Distributional type-claims (NC-1): **0**
- Functional codings (NC-2): **12** — TERM-FUNC 6 (M176, M267, M305, M336, M342, M367), MED-FUNC 4 (M347, M351, M362, M374), INIT-FUNC 2 (M362, M375), SOLO-FUNC 0
- Summaries (NC-3): **38** — INITIAL 27, TERMINAL 5 (M048, M089, M305, M336, M367), MEDIAL 6 (M128, M151, M329, M362, M375, M398)
- Total codings: **50**, across 44 signs. The other 50 signs carry no checkable claim and no summary (`codings: []`), with their assertions still listed.

No basis states a positional universal. Every positional statement in the set is either sample-marked ("(freq=…)", "(n=…)", "distributional assignment", "consistent X", "Pos=…; Freq=…"), which makes it a summary under NC-3, or a role/slot statement, which makes it functional under NC-2. The word "Exclusive" appears often, but always as "Exclusive to [animal] seals" — exclusivity over seal motifs, not over positions — so NC-1 does not fire on it, and the frequency or lift figure standing next to it changes nothing (NC-4).

## Residue

Two residue candidates:

- **M222** — "evidence_type=compound_slot_coherence": this names a compound slot but gives no anchor position (initial, medial, final, or solo), no positional statement, and no sample size, so no functional type under NC-2 and no summary under NC-3 can be assigned without inventing an anchor.
- **M233** — "Settlement/place marker": "marker" suggests a place-marking function, but the basis names no anchor position and no role term from the NC-2 vocabulary (no suffix, prefix, terminal marker, or slot label), so no functional type can be assigned; the remaining content is semantic.

Generic "slot" mentions in a phonological context (M165, M202, M330: "partial coverage for Shu-ilishu /su/ phonological slot") were treated as pure phonological content under NC-5, not as residue: they describe a sound slot in an external name, not this sign's position or role in an inscription.

## Rules that were hard to apply, stated plainly

1. **Superseded material inside a basis.** Three bases (M047, M063, M267) quote an earlier assignment and state in the same text that it was wrong or overridden. NC-1 through NC-8 do not say what to do with a retracted assertion. I coded only the current assertions and recorded each quoted earlier text, verbatim, in that sign's `ambiguities` with the reason. Coding the retracted text as a live claim would have misrepresented what the basis actually asserts.
2. **"Prefix" in literary name usage.** M362 ("aṇi- prefix in personal names") and M375 ("taṇ- is a common personal name prefix") use the role term for Sangam-literature word forms, not for an inscription position. I coded INIT-FUNC under NC-2 as written, let it coexist with those signs' MEDIAL codings under NC-4 and NC-6, and recorded the ambiguity in both entries.
3. **Terminal form descriptions.** "Terminal pinch mark" (M305) is honestly ambiguous between a description of the sign's shape and a terminal mark in the role sense. I coded it as TERM-FUNC under NC-2 and recorded the ambiguity; the clearer parallels (M336 "locative case marker", M367 "neuter suffix") need no such judgment. In all three cases the separate "consistent TERMINAL position (n=…)" statement is coded as a summary, so both components stand under NC-4.
4. **Consistency values with no named position.** Many bases carry only a phase recalibration line such as "SA-cons=0.12✓ DEDR✓" (for example M032, M042, M052). That is a consistency value with no position named, so there is nothing a summary could record; those signs are coded with no components. The same applies to counts of seals a sign "appears on" with no position stated (for example M007, M065).
5. **NC-7 was needed only at the margins.** Where a sample marker or a specific NC-2 pattern (a "between" pattern, a slot label) was present, the choice between summary and functional was settled by the specific rule — M351 is the one case I flagged, since its "MEDIAL after … and before …" statement has neither a quantifier nor a sample marker.
