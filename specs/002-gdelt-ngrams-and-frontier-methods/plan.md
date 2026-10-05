# Plan 002 — GDELT Web Ngrams switch + frontier methods

## Implemented (i)

- `gdelt_ngrams.py` fetcher on the existing `Fetcher` base contract:
  bounded heartbeat walk-back, gzip parsing, keyword/ngram matching
  (`build_patterns` / `match_keywords`), TOC cross-reference, topic
  exclusions, `.glossa-state/` watermark.
- Registry change in `fetchers/__init__.py`: `GDELTNgramsFetcher`
  registered; `GDELTFetcher` (DOC API) gated to opt-in in
  `_build_fetchers` (explicit source request or topic override
  `gdelt.enabled`), with the pause documented in `gdelt.py`'s docstring.
- Unit tests with synthetic in-test .gz fixtures; live smoke test at
  migration time (one-off script, not a unit test).

## Not implemented (recorded only)

- (ii) Daily fully-cited briefing — future spec when scheduled; needs
  model/provider choice and a review-gate design first.
- (iii) Vision passes for seals/tablets — design notes only; any
  future implementation starts as its own spec with the two method
  rules (physical metadata up front; discrete passes) as requirements,
  and follows the repo's graph-first experiment rules (H15/H23).
