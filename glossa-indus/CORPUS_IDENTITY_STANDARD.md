# Corpus Identity Standard — Glossa-Lab Indus Evidence Graph

**Status:** adopted with Spec 095 Stage 1 (T104), 2026-11-16.
**Machine-readable form:** `backend/glossa_lab/data/corpus_identity.py`
(the registry `CORPUS_IDENTITIES`, verification, enforcement, and
audit functions). This document states the standard; the module is
its operative form. The fail-closed battery that exercises it is
`backend/tests/test_spec095_corpus_battery.py` (T105).

## 1. The standard

Every claim-bearing corpus has exactly one **identity of record**,
stating:

- **version** — the version or acquisition label of record;
- **content hash** — a SHA-256 pin over the corpus file's bytes;
- **source** — where the corpus came from;
- **licensing** — the terms the corpus is held under;
- **counts under a named basis** — the census the corpus must
  reproduce, with the counting basis named (counts without a named
  basis are not an identity);
- **normalization rules** — the transformations between the stored
  form and the loaded form.

A corpus with no identity of record is not loaded. A corpus whose
file, hash, counts, or normalization differ from its identity of
record is refused, not repaired, substituted, or silently used.

## 2. Fail-closed rules

1. **Present but different → refused at load.** Each covered loader
   checks the file at its path against the identity pin on every
   load (`enforce_file_identity`). A mismatch raises
   `CorpusIdentityError`. A loader never falls back to another
   corpus because the file at its path failed identity (the V1
   loader's tier fallback applies to absence, never to a failed
   identity).
2. **Missing → refused on the verified paths.**
   `verify_corpus_identity` and the `load_corpus_verified` entry
   points refuse a missing corpus. On the legacy load paths, absence
   keeps each loader's documented historical behaviour (for example,
   the V3 loader loads zero records); absence is a flagged state,
   detectable at any time through verification — it is never a
   silent substitution of a different corpus.
3. **Unreadable → refused as unauthorized.** A corpus file carrying
   no read permission is refused as unauthorized access; it is never
   treated as absent or empty.
4. **Census → verified under the named basis.** Verification
   recomputes the census under the identity's named basis and
   refuses on any difference.
5. **Partial availability → refused as a set.**
   `verify_all_identities` refuses when any registered corpus fails,
   naming each failure.

## 3. Covered corpora

The registry covers the claim-bearing Indus corpora: the strict
Firestore corpus (V3 loader and its twin), the V1 research export,
the ICIT-format export, the CISI compilation, the mayig CISI layer,
the Mahadevan 1977 flat text, the site-attributed CSV layer, and the
Holdat downloads layer. Pins of record: the strict corpus carries
its PR #393 intake pin (2026-10-25); the Holdat layer carries its
Spec 054 arm-2 pin; the remaining pins were established by Spec 095
Stage 1's measurement of the in-tree files at registration
(2026-11-16). Non-Indus corpora and the synthetic prototype are
outside this standard's registry: the synthetic prototype is not a
claim-bearing corpus and is contained separately (Spec 095 Stage 2);
presenting synthetic output at a covered corpus's path is refused
and flagged under this standard (battery case 12).

## 4. Changing an identity

An identity changes only by a recorded act: a new pin, census, or
normalization rule is registered with its provenance (what was
measured, when, under whose order), in the same change that adopts
the new corpus. Editing a pin to match a drifted file without that
record is a violation of this standard — drift is a finding, not an
update.

## 5. Orientation basis (added 2026-11-16, Spec 095 Stage 3, T304)

Reading direction is data, not a default. Every identity in the
registry carries an `orientation_basis`: what the corpus itself
states about the reading direction of its sequences. A positional
or sequential result in a claim-bearing record must name the
orientation basis it rests on — the corpus's recorded basis where
one exists, or the assumption it adopts where none does — and must
either file its reversed variant (the same computation with every
sequence read in the opposite direction) or state why a reversal
is not defined for it.

As registered on 2026-11-16, none of the eight covered corpora
records a reading-direction basis: each registry entry states that
plainly, and each states the standing assumption positional use
makes in its place (stored order taken as reading order). An
assumption named in the registry is still an assumption; it does
not become a corpus fact by being registered. Where a corpus or a
future acquisition does record a direction, the basis is entered
in the registry under section 4's rule, in the same change that
adopts it.

Anchor-level direction notes (for example, the `reading_direction`
field carried by some entries of the Phase-108 anchor trails) are
not a corpus orientation basis: they record an assumption made
about individual anchor entries, and they do not discharge the
requirement above for any corpus or any positional result.
