# Spec 096 — Meroitic Reproduction Benchmark Program

**Status: ADOPTED 2026-11-20** (owner's direction in chat,
2026-11-20: the benchmark commissioned in parallel with the other
ancient-language decoding work, and then directed to stand as its
own separate program in Glossa-Lab rather than as a deliverable
inside Spec 095's package). Stage 0 of this package is the adoption
and registration itself (tasks T001–T004, including the program's
registration inside the live platform). Execution runs under
this spec's own records from step 0 onward.

**Provenance.** The founding record is the Spec 095 Stage 5
scoping: `specs/095-red-team-remediation/second-targets/meroitic-benchmark-scoping-2026-11-17.md`,
summarized at
`specs/095-red-team-remediation/records/stage-5-scoping-record-2026-11-17.md`
section 3. That scoping fixed the target, the three legs, the
success criteria and the falsifier before any execution was
commissioned, and it stays in place, unedited, as this program's
provenance. Claim C095-16 scoped the benchmark as a study under
Spec 095; the owner's 2026-11-20 direction supersedes that
placement, not the scoping's substance. The criteria and the
falsifier carried into section 3 are the scoping's, in substance
verbatim; nothing was re-derived after execution began.

## 1. What this spec is

A reproduction benchmark, run as the program's own implementation,
of one published computational decipherment-adjacent study:
Giorgos Otten and Antonios Anastasopoulos, "Towards Ancient
Meroitic Decipherment: A Computational Approach", ALP workshop at
NAACL 2025, pp. 208–219 (ACL Anthology 2025.alp-1.11, DOI
10.18653/v1/2025.alp-1.11). Meroitic is the right calibration
target for the projected-constraint machinery precisely because it
is deciphered at the sign level and undeciphered at the language
level: sign values are known, so the machinery's statistics can be
checked against ground truth, while no reading produced here can
borrow authority from a decipherment that does not exist.

The benchmark stands alone. It touches no Indus claim, anchor, or
standing; it writes no Indus record; its fixture
(`backend/glossa_lab/data/meroitic.py`) is the benchmark's
starting inventory, not its data; and the platform's legacy
Meroitic benchmark output is not a reproduction target.

## 2. The grounding

- The fixture module carries 19 signs (ME01–ME19) in stated
  frequency-rank order (a n r e t k l s m i b w d y q h o p g), a
  50-line / 551-token constructed corpus, and the convention that
  the paper's /o/ is written E in the Millet-paradigm
  transliteration the corpus uses.
- The paper's published record under reproduction: the corpus
  census (its Table 1 and section 5.3 counts), the bilingual
  dictionaries (its Table 2), and the alignment headlines (its
  sections 6 and 6.2: 0 percent unseen-dictionary precision at 10;
  training-dictionary accuracy at most about 20 percent, best the
  numerals dictionary at 100 dimensions; a French–English skyline
  of 70 percent at 100d and about 68 percent at 50d, which the
  scoping froze out of re-execution).
- `docs/undeciphered_scripts.md` already names Meroitic the next
  target on the program's multi-script priority map, on the
  strength of the same properties.

## 3. The fixed criteria (carried from the scoping, unmoved)

**Step 0 (gates everything).** The paper's corpus repository is
located, pinned by exact commit, and its license recorded on a
C095-3-style identity record before any computation. If the
repository is unavailable or unlicensable, the outcome is NOT
EXECUTABLE AS SCOPED and the benchmark stops.

**Independence rule.** The benchmark is the program's own
implementation, written from the paper's stated methods. The
authors' code may be read for the mapping scheme only, and every
such reading is recorded.

**Leg A (census).** All ten published counts reproduced exactly,
or each divergence named with its cause: Table 1's 193 translated
Meroitic words, 897 Meroitic phrases, 302 Egyptian texts, 708
Nubian pages; section 5.3's 871 phrases pre-augmentation, Egyptian
1,729 types and 99,338 tokens, and post-augmentation 1,868 forms,
17,257 phrases, 782,761 words; and Table 2's dictionary sizes
26/18/15/14/9/6/3 (nouns, names, numbers, verbs, titularies,
adjectives/adverbs, prepositions).

**Leg B (sign statistics).** (i) The corpus's attested sign set
equals the fixture's 19 after explicit reconciliation of the
paper's E-for-/o/ convention; (ii) computed frequency ranks agree
with the fixture's ME rank order at Spearman rho at least 0.90;
(iii) positional (initial/medial/final) distributions are computed
and archived.

**Leg C (alignment).** Under the paper's hyperparameters, with
attempts accounted: unseen-dictionary precision at 10 equals
0 percent; training-dictionary accuracy sits in the at-most-25
percent band; the numerals dictionary is best or tied at 100
dimensions.

**The falsifier.** The premise (the paper's published record is
reproducible from its published corpus by its stated methods) is
falsified if Leg A fails on a majority of its counts with the
divergences tracing to the published corpus or the paper's stated
methods, by re-derivation; the outcome is then NOT REPRODUCED. A
step-0 failure gives NOT EXECUTABLE AS SCOPED. Otherwise each leg
is reported exactly as its criteria read: REPRODUCED, DIVERGED
(with the named cause), or NOT REPRODUCED.

## 4. Decisions

- **D-096-1 (number).** 096 was the next free spec number at the
  check of 2026-11-20 (highest landed package 095; no 096
  directory, branch, or open PR on origin). A second program (the
  Eteocypriot pilot) is being set up in parallel; if that package
  lands 096 first, this package renumbers before merge rather than
  colliding, and the renumbering is recorded.
- **D-096-2 (program-map placement).** Taxonomy domain "Sign
  inventory & corpus", subdomain "Signary & corpus models": the
  three legs are a corpus census, signary statistics, and an
  embedding alignment over an external corpus.
- **D-096-3 (licensing posture).** If the pinned corpus carries
  no license, the benchmark proceeds only on the posture recorded
  in its step-0 identity record: scholarly reproduction, held
  custody, no redistribution of the corpus, the authors' code, or
  their embeddings; only the program's own code and derived
  aggregate statistics are published. The step-0 record states the
  evidence for the stricter reading openly alongside the ruling.

## 5. Stages

- **Stage 0** — adoption and registration (this package; ledger
  intake; program-map registration).
- **Stage 1** — step 0: pin, license, identity record, execution
  freeze.
- **Stage 2** — the three legs, under the freeze.
- **Stage 3** — the benchmark outcome record, claim adjudication,
  and closeout.
