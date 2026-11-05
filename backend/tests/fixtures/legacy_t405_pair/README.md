# The departed T405 pair — test fixtures

The two pre-spec (headerless) settling run records of the
Spec 086 Stage 4 T405 pair, preserved byte-for-byte:

- `t405-incumbent-over-full-frame--d9f73e4c4e4e.json` —
  SHA-256 `17d7dbae6daa135ebbcd37387942268283f5be4e6672b9624ccb34c313565bf2`,
  git blob `49d06bd3bef4fdac07f1fdabb41528664e0bc787`
- `t405-full-register-over-full-frame--f8c86443e924.json` —
  SHA-256 `176ca660d2f43f8f1b68aa6ba27d745cdaf80b8c545962b896aab67449ee8123`,
  git blob `f960d1b24b6df75489fe3a817cb017f036fed186`

The pair stood in `glossa-indus/ledger/runs/` from Spec
089 Stage 2 until the Spec 093 adoption intake replay
(2026-11-05), when the settling refresh re-derived both
scenarios over the grown ledger and the stale-pinned
records left the store under the map builder's D-D rule.
Their departure is accounted in the store's run index by
the pair of `departure` acts (run-defs v2 §7.1), which
name the blob ids and hashes above; the records themselves
stand in git history at those blobs.

Tests that exercise the legacy derivation or the legacy
pair's junction behaviour source the pair's bytes here
(the standing store no longer carries them), and the
settling coverage test verifies these bytes hash to the
departure acts' `blob_sha256` values, so the fixtures
cannot silently drift from the accounting they serve.
