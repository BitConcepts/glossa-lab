# Phase-422 Report — Spec 060 (D-23): the Holdat site effect, margin curve and shared population

Execution date: 2026-10-21. Frozen contract: specs/060-f2-margin-curve/freeze.md (digest 8c04b1a8bf742d80ea6da41021fe569686a854cdecd1cb22f4b12f1c385be1a3); OSF registration https://osf.io/8ywxc/ (approved and public).

Corpus labels: the Holdat compilation layer (SHA-256 62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e) and the ICIT-lineage layer (horus84) (SHA-256 c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef).

## Step 0 — the gates, in order

- Gate 0.1 (Input integrity): PASS
- Gate 0.2 (Population reproduction, both layers): PASS
- Gate 0.3 (Estimator regression): PASS
- Gate 0.4 (Shared-population census (arm 2's gate)): PASS

## Arm 1 — the margin curve (sensitivity display)

Margin curve for STUDY-SPEC-024/F2-HOLDAT (sensitivity display — the recorded verdict at the declared margin 0.10 stands, CONTRADICTED, and is not moved by this curve): governing basic-bootstrap interval [0.058939204306206666, 0.0777941604081594], point V 0.11539837515155212, on the Holdat layer's 1,670-inscription analysis population, recomputed under the Phase-384 v2 estimator. At margin 0.05: SUPPORTED AT 0.05. At margin 0.075: STRADDLES 0.075. At margin 0.10: CONTRADICTED AT 0.10. At margin 0.125: CONTRADICTED AT 0.125. At margin 0.15: CONTRADICTED AT 0.15.

## Arm 2 — the shared population

Shared sites (6): Chanhu-daro, Dholavira, Harappa, Kalibangan, Lothal, Mohenjo-daro. Per-site counts (Holdat / ICIT SEAL): Chanhu-daro 78 / 59; Dholavira 106 / 136; Harappa 492 / 440; Kalibangan 110 / 58; Lothal 124 / 94; Mohenjo-daro 606 / 1352.

Holdat governing interval [0.055251710457321024, 0.07607996659365032], point V 0.11537928745216733, on 1516 inscriptions. ICIT governing interval [0.08368810617885544, 0.10835095759573735], point V 0.13488340055820888, on 2139 inscriptions.

Outcome: COMPOSITION DOES NOT.

Period mix, Holdat layer: PERIOD MIX NOT DESCRIBED FOR THIS LAYER - FIELD NOT CARRIED.
Period mix, ICIT-lineage layer: PERIOD MIX NOT DESCRIBED FOR THIS LAYER - FIELD NOT CARRIED.

No verdict moves under this spec: F2 stands CONTRADICTED at the declared margin 0.10 and F3 stands SUPPORTED at the declared margin 0.10, exactly as recorded.

Anchors asserted byte-identical before and after: True (df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569).

*AI disclosure: Executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution sec.VI.*
