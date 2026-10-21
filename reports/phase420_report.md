# Phase-420 — Spec 058 report (transcription-disagreement mechanism)

Claim: `STUDY-SPEC-023/PHASE-132+383` — SETTLED — CONTRADICTED, exactly as
recorded; this execution appends a mechanism account and
changes no verdict. Execution date: 2026-10-21. Freeze digest:
`8bdd4764380bf9e6cb442b1cc75a3b57f4507284676bcb65603e481a49435713`. OSF registration 86dgh (approved and
public). Phase-420, Wave 3 group 2 of the runnable-experiments
campaign. Arm A only; arm B is blocked and out of scope.

## Outcome: LOCALISED TO SIGNS

Headline paragraph (spec §5.2 wording, quantities filled):

> Re-analysed under Spec 058, the disagreement between the two recorded Phase-132 pilot passes is localised to signs: the 10 most-involved signs account for 54.5% of all mismatch involvement, led by UNK, P310, P144, UNMAPPED:M817, P145, P245, P119, P184, P268, P324. The pilot's failure stands exactly as recorded; this account names where its disagreement sits, in this pilot's passes, and says nothing about human coders. UNK — the passes' 'no identification' value — is itself among the most-involved values (27.7% of involvement); the localisation is in part a localisation to illegibility, stated as such.

Fence sentence: This account is about why two recorded AI pilot passes disagreed. It is not evidence about human transcription, and it changes no verdict.

## Step 0, gate by gate

- **Gate 0.1 — Committed-record integrity: PASS**
  - `specs/023-keyed-transcription-layer/spec.md` — match (c2e5d1668b270266d5a20e30b1ec87cd4c1d5d2ffe786a45331a9a5ade1275d2)
  - `reports/phase132_pilot_metrics.json` — match (e864fca57ecd1dc403c8e52ab9df6414372478d5781457f0aaca5e9084914554)
  - `reports/phase132_pilot_report.md` — match (e1df32da86f7d3fd276d0ad546b3c351b58fd88b73f4468461f61075f6460e00)
  - `data/keyed_transcription/phase132_pilot_frame.json` — match (a967144be0531c9d8396615d1ca07161dca0bc7347ca8c2c0d6a3c21a037a2ea)
  - `data/keyed_transcription/phase132_pilot_dataset_v1.json` — match (adb596a1745470835e46c5148c1848d8408c45a030687d96427f00dbb6f74400)
  - `data/keyed_transcription/phase132_pilot_dataset_v1_meta.json` — match (b2c607fae5f2602bb7b9634ff103f01df1de3885a1f1bbeeb6da3fc489cdefd4)
  - `reports/phase383_results.json` — match (4e52942dc6be25fed4ab2004823a1d9353c9abfe6f5428e1050ee8d0d9a98334)
  - `reports/phase383_report.md` — match (9f35f722611f6acd57e1ee05c9de0c8e95267ccf7f93b27eacb31bdff9cd08ca)
  - `backend/scripts/phase132_metrics.py` — match (238dfafa3bac17dc0ad610ff4b7e6cf4fa577462d04cd31a3c612537cbe21984)
  - `backend/scripts/phase383_pilot_rescoring.py` — match (b64b60de35d59bd99177e8ac3f68a80ffd2b0d31f8c75ea87312f69f927729ec)
  - `data/crosswalks/parpola_mahadevan_crosswalk_v1.json` — match (4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb)
  - `backend/reports/INDUS_FINAL_ANCHORS.json` — match (df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569)
- **Gate 0.2 — Pilot-pass record production: PASS**
  - Inventory: frame.json present; Pass A 50/50; Pass B 50/50; gold 10/10; adjudication 50/50; effort log 320 events. Manifest: 162 files (per-file SHA-256 in the results JSON).
- **Gate 0.3 — Frame identity: PASS**
- **Gate 0.4 — Reproduction of the committed metrics: PASS**
  - Full-record equality with the committed metrics file: True; exact-sequence 0.2 (P and M), per-token 0.479798 all-50 / 0.428571 gold, gold estimator 0.05, token totals 191/190/40/189.
- **Gate 0.5 — Adjudication-taxonomy cross-check: PASS**
  - Taxonomy recomputed: {'count': 11, 'identity': 93, 'key': 10, 'legibility': 45, 'order': 1, 'orientation': 2}
- **Gate 0.6 — Analysis census: PASS**
  - Census: 40 mismatched objects (full census in the results JSON and the outcome record).

## Tabulations (P space, primary)

Event total E = 103 over the 40 mismatched objects; summed involvement = 191.

### T1 — by sign (full ranked table in the results JSON)

| value | involvement | involvement share | frequency | frequency share |
|---|---|---|---|---|
| UNK | 53 | 27.7% | 149 | 39.1% |
| P310 | 13 | 6.8% | 29 | 7.6% |
| P144 | 6 | 3.1% | 12 | 3.1% |
| UNMAPPED:M817 | 6 | 3.1% | 6 | 1.6% |
| P145 | 5 | 2.6% | 13 | 3.4% |
| P245 | 5 | 2.6% | 5 | 1.3% |
| P119 | 4 | 2.1% | 12 | 3.1% |
| P184 | 4 | 2.1% | 4 | 1.0% |
| P268 | 4 | 2.1% | 4 | 1.0% |
| P324 | 4 | 2.1% | 4 | 1.0% |
| P098 | 3 | 1.6% | 5 | 1.3% |
| P123 | 3 | 1.6% | 9 | 2.4% |
| P240 | 3 | 1.6% | 7 | 1.8% |
| P315 | 3 | 1.6% | 3 | 0.8% |
| P085 | 2 | 1.0% | 2 | 0.5% |
| P121 | 2 | 1.0% | 2 | 0.5% |
| P124 | 2 | 1.0% | 2 | 0.5% |
| P147 | 2 | 1.0% | 6 | 1.6% |
| P202 | 2 | 1.0% | 2 | 0.5% |
| P224 | 2 | 1.0% | 2 | 0.5% |
| P282 | 2 | 1.0% | 2 | 0.5% |
| P316 | 2 | 1.0% | 2 | 0.5% |
| P332 | 2 | 1.0% | 2 | 0.5% |
| P355 | 2 | 1.0% | 2 | 0.5% |
| P378 | 2 | 1.0% | 4 | 1.0% |
| UNMAPPED:M615 | 2 | 1.0% | 2 | 0.5% |
| UNMAPPED:M700 | 2 | 1.0% | 2 | 0.5% |
| P009 | 1 | 0.5% | 1 | 0.3% |
| P058 | 1 | 0.5% | 1 | 0.3% |
| P086 | 1 | 0.5% | 3 | 0.8% |
| P120 | 1 | 0.5% | 1 | 0.3% |
| P125 | 1 | 0.5% | 1 | 0.3% |
| P131 | 1 | 0.5% | 1 | 0.3% |
| P148 | 1 | 0.5% | 1 | 0.3% |
| P150 | 1 | 0.5% | 1 | 0.3% |
| P154 | 1 | 0.5% | 3 | 0.8% |
| P163 | 1 | 0.5% | 1 | 0.3% |
| P185 | 1 | 0.5% | 1 | 0.3% |
| P197 | 1 | 0.5% | 1 | 0.3% |
| P204 | 1 | 0.5% | 1 | 0.3% |
| P209 | 1 | 0.5% | 1 | 0.3% |
| P217 | 1 | 0.5% | 5 | 1.3% |
| P230 | 1 | 0.5% | 1 | 0.3% |
| P244 | 1 | 0.5% | 1 | 0.3% |
| P256 | 1 | 0.5% | 1 | 0.3% |
| P269 | 1 | 0.5% | 1 | 0.3% |
| P272 | 1 | 0.5% | 1 | 0.3% |
| P283 | 1 | 0.5% | 1 | 0.3% |
| P285 | 1 | 0.5% | 1 | 0.3% |
| P294 | 1 | 0.5% | 1 | 0.3% |
| P296 | 1 | 0.5% | 1 | 0.3% |
| P308 | 1 | 0.5% | 1 | 0.3% |
| P327 | 1 | 0.5% | 1 | 0.3% |
| P364 | 1 | 0.5% | 3 | 0.8% |
| P365 | 1 | 0.5% | 1 | 0.3% |
| P366 | 1 | 0.5% | 1 | 0.3% |
| P372 | 1 | 0.5% | 1 | 0.3% |
| P375 | 1 | 0.5% | 1 | 0.3% |
| P382 | 1 | 0.5% | 1 | 0.3% |
| P385 | 1 | 0.5% | 5 | 1.3% |
| P390 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M442 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M452 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M500 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M503 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M516 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M527 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M600 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M705 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M745 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M803 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M804 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M805 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M806 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M808 | 1 | 0.5% | 1 | 0.3% |
| UNMAPPED:M812 | 1 | 0.5% | 1 | 0.3% |

Top-10 share 54.5% over summed involvement; frequency share of the same 10 values 62.5%; state CONCENTRATED; sign locus FIRES.

### T2 — by object type

| recorded type | events | event share | objects | object share | mismatched objects |
|---|---|---|---|---|---|
| Seals | 80 | 77.7% | 34 | 68.0% | 30 |
| Tablets | 18 | 17.5% | 11 | 22.0% | 7 |
| Unrecorded | 5 | 4.9% | 5 | 10.0% | 3 |

### T3 — by divergence type

SUBSTITUTION 88 (85.4%); INDEL 15 (14.6%). The INDEL share is the registered segmentation proxy (spec §8(4): an indel cannot be separated into a different cut of the same glyphs versus a sign one pass recorded and the other omitted). Segmentation locus does not fire; object-type locus does not fire.

## Descriptive secondary (UNK-excluded) and M-space sensitivity

Secondary (events involving UNK excluded): E = 50; top-10 sign share 41.5% (state BETWEEN); indel share 12.0%. The secondary is descriptive only and carries no headline. Full secondary tables are in the results JSON.
M-space sensitivity (descriptive only): E = 103; top-10 sign share 53.9% (state CONCENTRATED); indel share 14.6%. Full M-space tables are in the results JSON; they move no headline (DD-058-4).

## First divergence

Per-object first-divergence table is in the results JSON. Distribution by position: {'1': 21, '2': 11, '3': 5, '4': 2, '5': 1}; by type: {'INDEL': 10, 'SUBSTITUTION': 30}.

## Produced-set manifest

Per-file SHA-256 of the 162-file produced set (gate 0.2):

- `adjudication/cisi:v1:H-139.json` — `b81e46419c5bdbe2e5a6f178c1acc609ee46df3efbd6c64fb7588b88006e04ac`
- `adjudication/cisi:v1:H-212.json` — `84bcf3908789c0b35dd7993e1b6e675453698854787081e603a294821d922e0d`
- `adjudication/cisi:v1:H-305.json` — `c36ff9eb08aeed34cee3638a3617de61af3c28857af958cba5eefeecec08feff`
- `adjudication/cisi:v1:H-66.json` — `d58484305a2f97f3a5f5dd172cab130dcc8443c1c5c6f5717951bfe9e3a3935e`
- `adjudication/cisi:v1:K-21.json` — `a18dfd116035878c77ae545e6105bc4c411f6cd61914338e94df8033073459f3`
- `adjudication/cisi:v1:K-42.json` — `78dc319bb914b6b6b16b3a76b15d2bcfff1d90b44ad1c57600933b9180382e6e`
- `adjudication/cisi:v1:K-63.json` — `c5e0d2cfe6bf658a863b537fe695455f0cfee7eb549548bfb58b8255088fa7e1`
- `adjudication/cisi:v1:K-88.json` — `851b39f6de2ff38ca387dc516af6a543cb8c2803fdc0d6d21ddb0f90cf184b0b`
- `adjudication/cisi:v1:L-132.json` — `0ccfb7aba1f98ec91977ac5ab523d0b90e0715883b14d45e2f608fdeb513e55a`
- `adjudication/cisi:v1:L-165.json` — `48695a2c741386760cd1a02754cf1b22b6bc5d4a371b58af62914c5400a3adfe`
- `adjudication/cisi:v1:L-227.json` — `5c3c268b4b1cd24215604b8b98cada78da4cb97b17664828af79c7a7d979a27e`
- `adjudication/cisi:v1:L-33.json` — `1ef01922b9345d385d33a9dc82e68bb5b366b7b733755f376636b5955755fa74`
- `adjudication/cisi:v1:L-66.json` — `69b46391074e688459da21a703dc74dad70aa3cf525055550d1bf9d6682bccd6`
- `adjudication/cisi:v1:L-98.json` — `eac3c70ecd141c2a268c8ce3f45edd3033a6dc213716ec425e4ac7ca492cff6a`
- `adjudication/cisi:v1:M-110.json` — `9bcabc155cecf94abb6d63bd8224c281263794ec15f08409c189b0b5b5b12bdf`
- `adjudication/cisi:v1:M-127.json` — `7b062a268e4a27928190184bbab3ef62ed89aa54a73575da8f0046b2ad0f2a57`
- `adjudication/cisi:v1:M-144.json` — `3a1f4524c0e6ac87e3e1f821fa2bc23f4c2b8a4e150280790925733c046b2bdd`
- `adjudication/cisi:v1:M-162.json` — `9f2293dde5a1cb31439ab8f8d3d2d1db15018f6729d3100acd812f98eef25242`
- `adjudication/cisi:v1:M-195.json` — `09d6a20fd099f93244843bc56628e444a173eef7e961f68f3e428be0a7d71e38`
- `adjudication/cisi:v1:M-21.json` — `1211fb1a99b93d75d17434d4bcc88638192a88db31d4e54a781669cfc67eae76`
- `adjudication/cisi:v1:M-250.json` — `cf775f34de35fa7a3acbffa8b3669c6d73a0342ef1e7320ea9cdfde5566df3e9`
- `adjudication/cisi:v1:M-3.json` — `866a06f90de3f057859110d91b2b3526bc82ed0ad1852e2f08321b94085addc3`
- `adjudication/cisi:v1:M-321.json` — `13d86b94add472ce224d2bae0a7890b75403829454686477e944642b07804306`
- `adjudication/cisi:v1:M-41.json` — `68b367153d2912b4b21f6be7f919d4bb62ba4852bd21338180cbc44344c86cf6`
- `adjudication/cisi:v1:M-480.json` — `1d3c8e5cda252a110dc671f8eed21ddfea2595bf1890735b281a94f4a4e68d36`
- `adjudication/cisi:v1:M-517.json` — `48131d2513ef5cffaa64d36e0422b9fc3d1df350ceb38cbfbd9283543ca8acf7`
- `adjudication/cisi:v1:M-566.json` — `aaaf29ae64400c242a417f3c1c733bd8fdb286ef9bd31b2aad7f2fdfa5bf96be`
- `adjudication/cisi:v1:M-58.json` — `b2e443d75dd86b1916448eefed688b480dddf38795e24c8763ec9eb10f7f3215`
- `adjudication/cisi:v1:M-75.json` — `f98af4bf05f482f65a7fa9790fce4367de4a105ff7a649b16e8b3ac4fc4d5097`
- `adjudication/cisi:v1:M-93.json` — `08a473b80fb2d43067d7e87fde12ea3780c6965dece2777803001cddcf113a28`
- `adjudication/cisi:v2:H-271.json` — `b7082348d7fc77b839483b9357c36ac89252a2c6fb38aa2b3201b64e898bc6ae`
- `adjudication/cisi:v2:H-451.json` — `af0f6229f70ed5dd61fff7fffca7ba241a533b14a15aa3e1fc68712e0b78c99e`
- `adjudication/cisi:v2:H-523.json` — `2d673420711733f54170b73ede8d66378dbe5bc85f6673b2ee3913f90b46a122`
- `adjudication/cisi:v2:H-596.json` — `81a744377ee7e1f2fc36bcaf62f40c9133b282d44a3ce6ddc38d0c631426542b`
- `adjudication/cisi:v2:H-669.json` — `583cf4ec96fc1646989ef142090b1c8b91073c49f85f82f5a74574c7e5226fe0`
- `adjudication/cisi:v2:H-743.json` — `ca9bdcb03ab134f1e5de8e810f3938a872a506fb8b349944b185aa22068e838d`
- `adjudication/cisi:v2:H-814.json` — `5158b3f8a9fe3c0ffba339811baf732669a230fdc23e4a097306c0dc41126979`
- `adjudication/cisi:v2:H-886.json` — `183671d9146239dcc035e344832c2c390a86b103b5675fc9ac515fb123e4b4e0`
- `adjudication/cisi:v2:H-960.json` — `ce2478a4bf4cac19c7ed3ad4cbaec1617c40d656901e54c5f7dabe8da183911f`
- `adjudication/cisi:v2:M-1044.json` — `4e0112c189dbee2f357b7b96aeb80091b898cc82ff87120a00b266dced9a7b1d`
- `adjudication/cisi:v2:M-1247.json` — `19d33ac4900c7ae9b550bdeb1f9540474a98930bd0364148cc8aa18d4320e382`
- `adjudication/cisi:v2:M-1352.json` — `fe3dbbabfe5c8a3b640927af215f981f29e8541ce7ae7d39c6504b77d1e515c1`
- `adjudication/cisi:v2:M-1448.json` — `88c598e876c6fefcb1ca4bba23a15ebe4444f269de1c84a015d59be967fc24a8`
- `adjudication/cisi:v2:M-1542.json` — `31f5f04982e8071c28b5919e3de14d202f12f2fa6673489a800e3b3496501339`
- `adjudication/cisi:v2:M-658.json` — `be5d55085be4030b5931d89d4fde21b6f0aba9c7b30b77c23a19f2507e9af963`
- `adjudication/cisi:v2:M-819.json` — `8c0733e8fd3f46c1f5357fa0f6887ea8400ffa682f411b82102778342c25a4a7`
- `adjudication/cisi:v2:M-926.json` — `63df9fb8cb9e359edf3dd4ba6f127b90759d99f3bf8b8008142df68d99371823`
- `adjudication/cisi:v2:M-983.json` — `0a31a2c4e240552200c6e994410ec19c3fe2de4c5541d1db35d8b823fa50acad`
- `adjudication/cisi:v2:Pk-24.json` — `d90f6e9e1f0beede6dd753f124b325fb8154efd2958a37a790f88167238b38be`
- `adjudication/cisi:v2:Skh-7.json` — `96e4ac1ecb92107ded5b412f323973a5ad3c48e98139800100faa86c9220075f`
- `effort_log.csv` — `6822330a7c702ac2fd0731302a62b4b29d33489e7b9a89761097544bff25c6fb`
- `frame.json` — `a967144be0531c9d8396615d1ca07161dca0bc7347ca8c2c0d6a3c21a037a2ea`
- `pass_a/cisi:v1:H-139.json` — `3821364c92c27f9e98ad9dd2e9eca61f5958f2fc031aeb3a7da093ae11c4c89c`
- `pass_a/cisi:v1:H-212.json` — `2ec0bfb9130994bb5b904b03fc1659cbd0086453b47ad66748c734562ffc6e44`
- `pass_a/cisi:v1:H-305.json` — `3ed4c6932e41be26db0a64b3081749d89345b64e4dc80c7abd4025df42b329f4`
- `pass_a/cisi:v1:H-66.json` — `5a2f1e30158d6b3c841e12bed99587faeea7aa76397650809d410c329b143e43`
- `pass_a/cisi:v1:K-21.json` — `94c2697e10feea0293085b5a593591fef734e063a7580cec74e69a71c02f3f78`
- `pass_a/cisi:v1:K-42.json` — `810b8a88f2b81fa19dd25620ba39b213c08295d409c2e1fd8ec415b8d6fe38d0`
- `pass_a/cisi:v1:K-63.json` — `29e2f2f41e7ebfbaae4cc857cf0b3235cf3d984b73ddd5e421cc52fb1d48a15a`
- `pass_a/cisi:v1:K-88.json` — `53f277f89cf99676df1c3878088d8759f59075c1efbbc96b25babad48c70244a`
- `pass_a/cisi:v1:L-132.json` — `8502613633bb1f7f81bf3a925d538dca93b943151116c4159fa543d302561b09`
- `pass_a/cisi:v1:L-165.json` — `041db200cc7aae2e37f7913f032a5e470b2114f4e153c3e4b31176048960bb94`
- `pass_a/cisi:v1:L-227.json` — `574a55269ffb32113a8088f3ec7d88cc887e7c1dc607417b2d99d07d3db779fd`
- `pass_a/cisi:v1:L-33.json` — `e4c8f7e142016a6ef8821d14a97b6ee4c0e5359d01e7a690c49311acc3ad8491`
- `pass_a/cisi:v1:L-66.json` — `2bd1e2648671d729fe5265c678d44a1b0f6fd98d0ecb2dd7bb6bdf8446381503`
- `pass_a/cisi:v1:L-98.json` — `107530a1be9eb4658a537c0401bf1ac6621817d131e5592e156a1d3bfaeaba72`
- `pass_a/cisi:v1:M-110.json` — `3825b92e3b4982056b1bbfb07238183460b387a587b086fb9f81d359b942159d`
- `pass_a/cisi:v1:M-127.json` — `4eef5c16b3453b8fc2502fb977d85b3d52ac11728ab96f9b4023d6699c846642`
- `pass_a/cisi:v1:M-144.json` — `6c62b1279e40a6082580339eb80cc76bf1517a5dd0f4f3857a18738b197e0e48`
- `pass_a/cisi:v1:M-162.json` — `4e75f1edb4918ea588b9a940e8bc32e8be9b2d1363287c5dd0ebf2ab51f579e5`
- `pass_a/cisi:v1:M-195.json` — `39d0e89cf1a9f4110b2471fea91b34a55e23a53bf7bb6d41e64d2c122db276c3`
- `pass_a/cisi:v1:M-21.json` — `ed38d8a43461e63b911b2fdd3b1e3b1fe80c8d054677a6b7a72fe3a84659a6f6`
- `pass_a/cisi:v1:M-250.json` — `3e3ffb8da677c838cdbcd8561e9f7830bbb6a2d03b912a9e56d5881cc4fcf424`
- `pass_a/cisi:v1:M-3.json` — `84212c55f95ddfb13f1d07831588bf07fb7eb37e846c64bc18891803fff055e2`
- `pass_a/cisi:v1:M-321.json` — `3053cdc214bf0c006b86681154324980153e700c9c28deae64c6c95c3b72533e`
- `pass_a/cisi:v1:M-41.json` — `1c146e6c44e72d88db0412a22dd1604d1d3895113b14559128baf9377eaae746`
- `pass_a/cisi:v1:M-480.json` — `12d85726762f0befaa39ddee4ae5b7417c02693f9439e42fef139d0e51484159`
- `pass_a/cisi:v1:M-517.json` — `58f26b3b039ecb7118946500993daaef8e1a53e906fa858a3ad0c78d693a6155`
- `pass_a/cisi:v1:M-566.json` — `fd6cdbbda4a19bf299a2c9e35e20d6ce2dde64cef25a5bc583365ba9aa93fdfb`
- `pass_a/cisi:v1:M-58.json` — `9580201d027879c8d1d2796c6e73cd8cfa7cb18ddb1333821c7eeea6f2618e03`
- `pass_a/cisi:v1:M-75.json` — `425743feb3bd31a464b52a2f59c228039f4b61ab037f3476f24e04a09a6c6ec6`
- `pass_a/cisi:v1:M-93.json` — `ecf2b2e72311a80f2350b0cb590dcb56fc289bf02241bcce944f2524523683e4`
- `pass_a/cisi:v2:H-271.json` — `6048f569e785f5f2545d91bdf574b3291a19c4a7a40c0a70e3087e03bf8562ce`
- `pass_a/cisi:v2:H-451.json` — `b3806121c2601b6c14ce1b996f939713981705fb8e66a42c1c1f20d9f3567906`
- `pass_a/cisi:v2:H-523.json` — `abafb3d645dbc68a757468dfe8f5f8518e8c4cb1a839da8d8418baa1139e905f`
- `pass_a/cisi:v2:H-596.json` — `ff4b898d01cfed1e5e83d812fec268d6b05a09d7cf6f5f65d9e3eaa3f99a3e13`
- `pass_a/cisi:v2:H-669.json` — `f2eddc4bf91926d7e863ffe627076501ec44f7ca6b9a35a0fc87597d2bf76236`
- `pass_a/cisi:v2:H-743.json` — `fc4dc63079c238b58006c50cdf91d9aeb399878be75261c13f0542b9cec96ddb`
- `pass_a/cisi:v2:H-814.json` — `11a6e080505b8021fe36f8e0ba8ec89221ad14f22ae8587106f134fd6ff15dba`
- `pass_a/cisi:v2:H-886.json` — `02289fe41f03db323dba4ea0a25163b9dd3e962104513763f1419fba986040aa`
- `pass_a/cisi:v2:H-960.json` — `4378bd9a8323ce6daf4ac9079c2ff7b6bd1a924094c59f5ad59b5a1ba15cdc20`
- `pass_a/cisi:v2:M-1044.json` — `efdb4a488871eac8db4befd1ee5abf650f200641d4359c4b5c3f79b2f2e8e530`
- `pass_a/cisi:v2:M-1247.json` — `c7a0e5feb4cefaa509388e9f18628bcbb4bdb195b9252f5e659c7311fa4d09e4`
- `pass_a/cisi:v2:M-1352.json` — `0139fd7abb2c253fccc7e05fa997b4506658e35e373b8285329d7acf07d4261a`
- `pass_a/cisi:v2:M-1448.json` — `a92ef631d5d49b8f6a63b10de25f5973bb78ab53e6be0c4e94d5e57d1bd18a9d`
- `pass_a/cisi:v2:M-1542.json` — `faf96ab1f46a56f6b85368a39d0944e0b36a99f2bc95c1b4b14c8aa042d5348d`
- `pass_a/cisi:v2:M-658.json` — `15a64ff3a3961b61ed57065a3c54b86f6e1f9cb901fbfcf2353d110435bbbd77`
- `pass_a/cisi:v2:M-819.json` — `f22972d2f7d8b98697494fa095533b26100113783b673b976fcb928d3c5e8220`
- `pass_a/cisi:v2:M-926.json` — `6cf1f3374fba9844c7fe1cfde085501a392946dd4ac9955d76d2458ec1fd0886`
- `pass_a/cisi:v2:M-983.json` — `fb90239839e084ef56306cfd5a204236d9fda3bc8454b6d923ac126828321cc3`
- `pass_a/cisi:v2:Pk-24.json` — `d8b1075459812e149bbf887d3477018d15079dd814adab869a2c39dc3f037b70`
- `pass_a/cisi:v2:Skh-7.json` — `45ac0b811d4132739d13320ab1ed71e9aa9e5b16ed1ac9298df78de4982b9d13`
- `pass_b/cisi:v1:H-139.json` — `0e40be9258602f85597421e0ace21c3e25e4460bd3d302bed619858b36d253e8`
- `pass_b/cisi:v1:H-212.json` — `f6b317cd3898bce957f4579668a06520360115e70d98388299cfc41b8ead9298`
- `pass_b/cisi:v1:H-305.json` — `31b0c29e4a667589b2c650acc9fc0a4fa5df5c1ce92e8ddda817e565546d841d`
- `pass_b/cisi:v1:H-66.json` — `ebc9650ef826f4bbc2edb4b330c7b17d6833f49592db7dd11bdf733583725d62`
- `pass_b/cisi:v1:K-21.json` — `50e087de43f930540174e6463f7b955a7c18d9a06df40199494e6a9792fdc57e`
- `pass_b/cisi:v1:K-42.json` — `37da83771c06684d79007c5c882faec54070484797669848904088a38d9f7d3a`
- `pass_b/cisi:v1:K-63.json` — `38383a0ef77d4016e72e7f34d87e225ef7caf8858859c82a79898238dd3f665f`
- `pass_b/cisi:v1:K-88.json` — `8697ac73c7aeb93240fd1d770f9a4b356c50d53298a94597b9535237c95bbc83`
- `pass_b/cisi:v1:L-132.json` — `cdc69aa06dfc6e79878e4fedbfbeca28bd30cee925784a86155905918df703e2`
- `pass_b/cisi:v1:L-165.json` — `4a21d7c69631ec3d12873afa085e2d4ae9c721fc3fc8d91aea9d75d8d3c7e42c`
- `pass_b/cisi:v1:L-227.json` — `4a736f0212b5ec1d5c7bc5df8614807cc044b4228c6e706ec683576d9be8473d`
- `pass_b/cisi:v1:L-33.json` — `74a94202e8805e027c490fae9d672f76e340c6ad031f4f37f41b71775088f4b3`
- `pass_b/cisi:v1:L-66.json` — `f3eef0b16349339f7da6104699f45131c203731b15c8c348226371748812f167`
- `pass_b/cisi:v1:L-98.json` — `1d343fe033f3f0ba8175c30084c39c903d0e143cd9af36cdf4956817fa31c593`
- `pass_b/cisi:v1:M-110.json` — `abb6f0d7608eeabf50d183a0db799f94e65b81519be961825913aaa4a6844e9a`
- `pass_b/cisi:v1:M-127.json` — `c2d6a1483645f8baed15954f6a38d1012ff5ccff8fcfc67a0f335df9d4a28521`
- `pass_b/cisi:v1:M-144.json` — `a0eba4c007d4253bfcb0e3bff216d03a4bc3fb8c43468dbcf383abba4dea6e1f`
- `pass_b/cisi:v1:M-162.json` — `348671460501f1f55a8bea64d02cd4950109a8afc062d23dc3286aeb2d9adc4e`
- `pass_b/cisi:v1:M-195.json` — `b15190f24864f3919fb645317d8150cbdee07c400971538e0d956168fe2ec499`
- `pass_b/cisi:v1:M-21.json` — `36b5f1656704429c9d624ebf0e3647f5a8f225e689e0aa085b2c14eb092bc7a7`
- `pass_b/cisi:v1:M-250.json` — `ab40f8d880e1ebacd36c2a75ff859e2dfedb3beef54127a003197b6dbda45dbf`
- `pass_b/cisi:v1:M-3.json` — `418e8a9bf433baa930d2f69f764fc307696b0d346be544a4229da03996bb56a1`
- `pass_b/cisi:v1:M-321.json` — `8d2ed8dcf3579f86a26a3ffbb135863de71ae5b822876253d9fe906ae5d058ed`
- `pass_b/cisi:v1:M-41.json` — `eb1a6059d58d2915d3354aadccd3e96fef888e67d5c9af2ca9108912b3af9e3e`
- `pass_b/cisi:v1:M-480.json` — `2c134db876b37ecad3fa8296c7c7f0124b7d5eb555462f09e09246a9ba96d0f0`
- `pass_b/cisi:v1:M-517.json` — `600dc755728bc876cc3beb3837e1d235f4844b748f6411b1b31f31857ee36545`
- `pass_b/cisi:v1:M-566.json` — `2da2c930fad6bf2410b29799870231214778a3a57b2eb93977035ccc702b69ec`
- `pass_b/cisi:v1:M-58.json` — `022f77f98fbbc05bc71d165004c5bdcbd6c003a7854241bbce4fd8a4fe4b099d`
- `pass_b/cisi:v1:M-75.json` — `1f5239b79b6ac9d20e3ca63d68e955142badc37067334393fd394bf678f5fc1e`
- `pass_b/cisi:v1:M-93.json` — `ddbb3ff3f86b77eb4f045c03f382dd442f7d3acf0e58870171a982a725261f45`
- `pass_b/cisi:v2:H-271.json` — `51894cacb96078101499c98098a06f9512abf150d27567d5c40761d8c6bb1c49`
- `pass_b/cisi:v2:H-451.json` — `57363c64fd8631cf4e25e000f9a99a99da256b51a47608b043f7dbd469b15d5c`
- `pass_b/cisi:v2:H-523.json` — `44410c6f761b51d256b6cbce1f70a0e0312338dcc2be5ec406f03b9d1315eb2c`
- `pass_b/cisi:v2:H-596.json` — `e6c06c0113447803ba2504dce8b91dc5f1bcfc3d4fd65600208abbb78ca8e640`
- `pass_b/cisi:v2:H-669.json` — `f7658d7e1dfd579c164215d8ff9412710bdcd0a216dc7fd7957979b73bc993fa`
- `pass_b/cisi:v2:H-743.json` — `02fbde69a86277c15cb0940994eb81e7665ab544c0a884071c0948273dc5fbac`
- `pass_b/cisi:v2:H-814.json` — `74beab039de12ba980344ac26e42754bfc8d3f89f364b2711d792e99003cad4e`
- `pass_b/cisi:v2:H-886.json` — `f86d2b8ccb3c13ccb3d6fa81cf7eee03928fb4a1f7e87dbb4de9bf0ad63aad83`
- `pass_b/cisi:v2:H-960.json` — `f693ddd8f661c4f9e6914d2ce3592093dc20390f91d10c94caf24e70b69a799e`
- `pass_b/cisi:v2:M-1044.json` — `bf30419891c5c3988be32b47546f2caf3c6c0d32f6807984a0a7d25e9fdfafc3`
- `pass_b/cisi:v2:M-1247.json` — `3c1f297680dcae97ad871549a17ed263d6badc79157df69772502b75678fa48f`
- `pass_b/cisi:v2:M-1352.json` — `d5bbca166202d5b77b97bb5524536338a9e8d43ab007dd02a49f1a659bfd811c`
- `pass_b/cisi:v2:M-1448.json` — `389ce36b1b9bc02a39230041e3ee7498b6414553f3762e4455be9ab3bfa7ea3b`
- `pass_b/cisi:v2:M-1542.json` — `87c6f0848847f06aa2f519ecbd7944b0b69ee7a2f48adb24994848102af5c812`
- `pass_b/cisi:v2:M-658.json` — `c3b53ee776b8d3bffadd39c6d677f63011bcd64648abe5d228575d989322af15`
- `pass_b/cisi:v2:M-819.json` — `84ed9e6422530ab1352b66386d2adab2abacab4f8e9bc2fd95519f3b5df84997`
- `pass_b/cisi:v2:M-926.json` — `9e5d77a4836f6f4332465a5c683f967ec143e68ebc2f17cc7a5bbc5000b362b9`
- `pass_b/cisi:v2:M-983.json` — `d782b2b722c4b72fbe759d2bd789dd4a2a9243a69537d3d4bda87356776052c2`
- `pass_b/cisi:v2:Pk-24.json` — `fb767eb9cc70414fe6d81ee65f4662c40ec44e94c9075bf1cf350f8e742ddf8a`
- `pass_b/cisi:v2:Skh-7.json` — `0397475c8fe472ab4416b25327b928ab0e156cae7ddcf20c334dd51a08ad1453`
- `pass_gold/cisi:v1:K-63.json` — `13734deebac5a09a0c264804db756478fa12ee0a0ee9d6ae963ae0886489f27b`
- `pass_gold/cisi:v1:K-88.json` — `a71c0b73bff3a624ce44b3b217d930c16a0b7e52cc37eb76d5e45820efc00848`
- `pass_gold/cisi:v1:L-66.json` — `0b451c23d598c9892ca5c9bb72d008959ee93757d8d21252145a71d0b1f9e885`
- `pass_gold/cisi:v1:L-98.json` — `e805b6bc558c11f39c15eb9ac1f694228b8e1740e89d2dc5334a4b21ee244eac`
- `pass_gold/cisi:v1:M-144.json` — `3fe1d71c9092344f3506d8b352ae922dccca941049235441d15d39163a0a2807`
- `pass_gold/cisi:v1:M-250.json` — `ca6819015ac1324891c8fdd296c6aab1f5b960942c76952faad3e99090a1ed80`
- `pass_gold/cisi:v1:M-93.json` — `56e15536df0a990fb5d98da3befb1689b624937072c2a211527733a50f77e015`
- `pass_gold/cisi:v2:H-271.json` — `cf57d521fca9cbdabcc9f6eeb73f192df04bb15fdca53c3ba752a1670cae1dc7`
- `pass_gold/cisi:v2:H-743.json` — `7aa612a606ff9467a8d28ac366af2590f2559037fb296859ee80a5973ddab58b`
- `pass_gold/cisi:v2:M-1247.json` — `0b7e43640d6e01f78e259f1bcb0fff8feda27deebd7d92da83f253f00de534ee`

Anchors asserted byte-identical before and after: `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both readings.

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution section VI.*
