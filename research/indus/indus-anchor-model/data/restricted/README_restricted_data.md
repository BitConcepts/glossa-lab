# Restricted Data Notice

The Holdat LLC Indus Corpus v3 is not redistributed in this repository. Some counts and outputs were derived from that corpus. Scripts are provided so that the analyses can be rerun by authorized users with access to Holdat or by researchers using a compatible public corpus after sign-code crosswalking, such as ICIT.

## What requires restricted corpus access

The following outputs in the preprint are derived from the Holdat LLC Indus Corpus v3 and cannot be reproduced without authorized access to that corpus or an equivalent:

| Claim / Output | Requires |
|---|---|
| Token coverage: 90.96% H+M (6,363/7,002 tokens) | Holdat v3 or ICIT crosswalk |
| Positional rates (I/M/T percentages per sign) | Holdat v3 or ICIT crosswalk |
| Permutation null test result (z=10.3, 0/2000) | Holdat v3 raw seal sequences |
| Bootstrap CI for site-level KL divergences | Holdat v3 site metadata |
| Phase 172 betweenness centrality from full corpus | Holdat v3 unified seal sequences |
| Site-level token counts (Mohenjo-daro n=606, etc.) | Holdat v3 |

## What does NOT require restricted access

The following can be tested from the public tables in `data/public/`:

- Fish-sign compound-only pattern (0/113 isolated)
- Formula bigram backbone (M342·M176 top PMI pair)
- Iconographic co-selection enrichment (63 pairs)
- Betweenness centrality rankings from the public bigram table
- Anchor table integrity (397 signs, 161 H+M)
- Polysemy permutation summary statistics

## How to request corpus access

The Holdat LLC Indus Corpus v3 is maintained by William Miller (Miller 2025). For access, contact the data provider directly. This repository provides no brokerage for that access.

## ICIT as an alternative

The ICIT corpus (Fuls 2014; ~5,318 inscriptions) is available through the International Centre for Indus Texts and Images. A Mahadevan-to-ICIT crosswalk would be required before rerunning corpus-dependent scripts. See `docs/icit_validation_plan.md` for the proposed crosswalk and test plan.
