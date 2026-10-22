# Phase-43 positional battery — provenance note

Provenance for the Phase-43 battery deposit (owner-approved 2026-10-21).
The methods record is `docs/phase43-battery-methods.md`.

## The restored scripts

- `backend/scripts/phase43_part2.py` — restored byte-for-byte from commit
  `3e0ab651fb3f38aed0385c73c66600819cc04f1c` (2026-05-15, "Phase-43: V3 corpus
  (Firestore) + Dravidian confirmed independent + terminal signs mapped").
  SHA-256: `6d5a079d47113937afd3340ab4b35781d1b7202644b180ba814d15f03f49699e`.
  This is the producing script of the Phase-43 results file. Restored, not
  re-authored; no annotation was added inside the file, so the pinned hash
  stays the hash of the code that ran.
- `backend/scripts/phase43_all.py` — restored byte-for-byte from the same
  commit. SHA-256:
  `6a3bc7764ea32ddc4b578cad66881fdcb2b542ab03daa3f9a0ddcac6c30fb133`.
  The sibling Phase-43 run; it did not produce the deposited results (see
  the methods record).

Both scripts were byte-identical between their creation commit and their
deletion.

## The deletion

Both scripts were deleted in commit
`fac2f2c8f97f3982178b8f869b1542e1ffb4c389` (2026-05-17, "chore: comprehensive
repository cleanup"), one of 113 phase30–43 one-off scripts removed in that
cleanup. They do not exist anywhere in current main's rewritten history or
tree.

## The recovery source

The scripts were recovered from pre-purge history retained in the local
mirror `~/workspace/glossa-run/verify-remote.git` (a bare mirror of
BitConcepts/glossa-lab with refs frozen at the 2026-10-08/09 purge window),
at commit `3e0ab651fb3f38aed0385c73c66600819cc04f1c`.

## Pins

- Results file of record: `outputs/phase43_all.json`, SHA-256
  `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4`
  (timestamp in file `2026-05-15T22:56:26Z`).
- Loader: `backend/glossa_lab/data/indus_corpus_v3.py` as it stands on main.
  Its loading logic is byte-identical to the Phase-43 original; one cosmetic
  line in the `__main__` demonstration block differs (line 216:
  `print("Sample sequences:")` vs the original
  `print(f"Sample sequences:")`).

## What this deposit does not establish

This deposit establishes that the Phase-43 battery's rules survive verbatim
in the producing script and are now pinned as a record. It does not
establish that the frozen classes can be reproduced today — the corpus dump
is missing and gates G3/G4 (corpus reproduction and class re-derivation)
have never run — nor that the Phase-43 results are correct, nor that Specs
049 / 052 / 054 pass their other gates.
