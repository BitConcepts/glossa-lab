# Route 2 tooling (indusarrays / RMRL Firestore)

Committed 2026-10-25 by the programme red team (finding E-8:
this tooling previously existed only in a goal's hidden_files —
single-copy, in no repository).

Contents: `route2_firestore_read.py` (the Firestore REST read),
`route2_verify_census.py` (the V1–V4 census verifier),
`run_route2_tests.py`, and `fixtures/` (synthetic 12-record
fixture set the tools were proven on).

Status (2026-10-25): the **data leg is superseded** — the
indusarrays file was located on TRISTEN-DESKTOP and intake-pinned
(PR #393), so no live read is needed for the data. The census
verifier remains the live instrument: it can check the held
file's counts (3,916 records / 2,665 dockeys / 3,137 sequences /
12,494 instances) with no owner session. A live re-read is
retained only if the RMRL permission basis requires one (owner
matter). See the Route 2 readiness record's supersession note
(2026-10-25) in the programme goal files.
