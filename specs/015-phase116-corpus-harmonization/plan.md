# Plan — Spec 015 / Phase-116 Corpus-Harmonization Study

Diagnostic study (no anchor changes). Follows the Phase-113/115
execution pattern: frozen spec → keyed-layer build with
reproduction assertions → analysis module → H23 graph
registration → run → reports → suite/foundation → ledgers → PR.

## Approach

1. **Keyed layers.** Holdat keyed by its internal `cisi_number`
   (phase113 loader logic). ICIT rebuilt under the spec-014 §2
   conversion policy with full provenance retained (source row,
   `cisi`, site/material/type/sides/`dir.`, per-token conversion
   kind, kept/dropped flag). The kept subset must reproduce the
   Phase-115 v2 layer byte-for-byte in sequence content/order.
2. **Baseline gate.** Recompute T1 v2 (spec 014 §4) over
   STRICT94 and assert the published Phase-115 tallies
   (51 judged / 8 PASS / 43 FAIL / median TV 0.789474) before
   any hypothesis arm runs.
3. **Matcher.** Wildcard compatibility (ICIT sentinels) over the
   pre-Holdat-dedupe ICIT population (4,614) × Holdat (1,670);
   tiers A (direct), B (reversed), C (containment), all
   mutually unique; ambiguous-orientation pairs counted and
   excluded.
4. **Arms.** §5.0 permutation context (seeded, BH q=0.05);
   H-COMPOSITION paired core test on Tier A restricted layers
   + site/material descriptives; H-SEGMENTATION sentinel-strip
   re-judgment (S1), artifact-unit re-unitization on matched
   artifacts (S2), boundary descriptives (S3); H-MAPPING
   concentration + chain-share contrast + top-10 crosswalk
   audit table; H-DIRECTION matcher-orientation share (D1) +
   global-flip agreement (D2); H-DEFINITION continuous
   relative-position W1 / mean-r Spearman + 5-bin agreement.
5. **Verdicts + recommendation** assembled mechanically from
   the frozen §5 rules and §6 templates, including the
   future-battery assumptions list.

## Determinism

Pure counting/sorting in file order everywhere; the single
PRNG use (§5.0 permutations) runs under the frozen seed
116116. No GPU (torch absent; `gpu_device` recorded per H20
pattern in the results JSON).

## Risks registered

- Matcher yield may be low (short formulaic texts, sentinel
  wildcards): power gates are frozen in §5 so a low yield
  produces UNRESOLVED (power), not a post-hoc redesign.
- The kept v2 layer excludes the 83 best Holdat matches by
  construction; the matcher population (§2/§4) corrects this
  by design and the correction is itself reported.
