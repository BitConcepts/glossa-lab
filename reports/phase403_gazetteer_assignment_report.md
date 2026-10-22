# Phase-403 — Gazetteer Period Assignment Report (Spec 039)

**Execution of the frozen Spec 039 contract** (`specs/039-gazetteer-period-assignment/freeze.md`, freeze digest `ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742`), run 2026-10-20 as Phase-403. Contract registration: OSF <https://osf.io/w38ha/> (filed at the freeze; approval pending at the time of this report).

## What this act did, in plain terms

The gazetteer lists 30 sites. For each site, this act looked for a **published** determination of the site's period — a statement in print, by the site's excavators or in the scholarly literature — and, where one exists and the frozen mapping table has an entry for the published wording, recorded the programme's coarse period label (Early Harappan, Mature Harappan, or Late Harappan) with the evidence attached. Where no admissible published determination exists, the site stays blank with a recorded reason. Nothing was inferred, interpolated, or repaired, and no programme-derived dating was used (owner decision D2, Option 1).

**The labels are finding aids, not dating evidence.** This act changes **no study outcome**: **Q7 still fails its link-mass floors** (in-universe link mass **2 link-eligible sites / 1 linked pair** against floors of **8 eligible sites / 10 linked pairs**), and **Q6 remains NOT-YET-TESTABLE**.

## Methods note (the verification bar)

A determination is recorded only where the act verified the published statement in the publication's own text or in a published scholarly restatement quoting it with pagination. Determinations that could not be verified to that bar were not used, and the affected site is blank with `NO_PUBLISHED_DETERMINATION` — the code records the bar, not the absence of print. Citations are presented in the frozen four-tier hierarchy order (DD-039-2): 1 excavation reports and site monographs; 2 regional surveys and site catalogues with per-site assignments; 3 published compilations and site lists; 4 journal literature on individual sites. The order is presentation only and resolves nothing.

A site is **contested** where two or more admissible determinations map to different label sets; every conflicting determination is retained and none is suppressed or voted away. A single determination whose own statement spans several periods (a site report's full sequence, for example) grounds a multi-label record and is **not** a contest.

## Result

- **Assigned: 11 of 30 sites** (17 of 36 gazetteer rows carry an assignment). Label incidences across assigned sites: Early Harappan 4, Mature Harappan 8, Late Harappan 6.
- **Contested: 1 site** (banawali).
- **Blank: 19 sites** — `OUTSIDE_LABEL_SET` 9, `NO_PUBLISHED_DETERMINATION` 8, `UNMAPPED_SCHEME_VALUE` 2.

Output A: `data/movement/gazetteer_rows_assigned.jsonl` (SHA-256 `64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4`), all 36 rows byte-identical to the pre-act file outside `program_period_assignment`. The pre-act file `data/movement/gazetteer_rows.jsonl` (SHA-256 `5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6`) is unmodified. Reviewer of record on every assignment: Muse Spark via Muse (AI agent).

## Per-site assignments

| Site | Labels | Rules | Evidence (tier; citation; locator) |
|---|---|---|---|
| amri | Mature Harappan, Late Harappan | MAP-EXPLICIT-MATURE, MAP-JHUKAR | Tier 1 — Casal (1964), *Fouilles d'Amri*: Period III is the Harappan occupation, Period IIID the Jhukar level (Jhukar equation as discussed in Mughal 1990). |
| banawali ⚠ contested | Early Harappan, Mature Harappan | MAP-EXPLICIT-EARLY, MAP-EXPLICIT-MATURE | Tier 1 — Bisht (1982), in Possehl (ed.), *Harappan Civilization: A Contemporary Perspective*, pp. 113–124: Period II = Mature Harappan (Periods I "Pre-Harappan" and III "Post-Harappan" unmapped). Tier 4 — *Journal of Archaeological Science* (2014) archaeobotany review: Early Harappan and Mature Harappan levels at Banawali. The two determinations map to different label sets ({Mature} vs {Early, Mature}); both are retained. |
| harappa | Early Harappan, Mature Harappan, Late Harappan | MAP-HARP-RAVI, MAP-HARP-KOTDIJI, MAP-HARP-HARAPPAN, MAP-HARP-CEMETERY-H | Tier 4 — Meadow & Kenoyer (2001), *Indo-Koko-Kenkyu* 22: 19–36: the five-period sequence (Ravi aspect; Kot Diji (Early Harappa) Phase; Harappa Phase; transitional; Late Harappa Phase (Cemetery H)). Tier 3 — Kenoyer (2008), Table 1 (chronology of Harappa), same equations. One scheme, one label set: not contested. |
| jhukar | Late Harappan | MAP-JHUKAR | Tier 4 — Mughal (1990), *Lahore Museum Bulletin* 3(2): the site's Early/Middle/Late Jhukar Phases treated as the Late Harappan manifestation in Sindh (the underlying unqualified "Harappan Period occupation" in trench CIV maps to nothing). |
| kalibangan | Early Harappan, Mature Harappan | MAP-EXPLICIT-EARLY, MAP-EXPLICIT-MATURE | Tier 1 — Lal et al. (2003) *Excavations at Kalibangan: The Harappans (1960–69)*, Part 1 (Period I = Early Harappan) and Part 2 (2015, MASI 110), Preface: "the present one is devoted to the Mature Harappan settlement (Period II)". |
| khirsara | Mature Harappan | MAP-EXPLICIT-MATURE | Tier 4 — Nath, Kumaran & Kulkarni (2012), *Puratattva* 42: 122–132: the entire deposit belongs to the mature phase. Tier 4 — Pokharia et al. (2017), *PLoS ONE* 12(10): e0185684: mature phase occupation. |
| kunal | Early Harappan | MAP-EXPLICIT-EARLY | Tier 4 — Khatri & Acharya (1995), *Puratattva* 25: 84–86: Early Harappan (Hakra ware) settlement. Tier 4 — *Journal of Archaeological Science* (2014): Early Harappan levels at Kunal. |
| lothal | Mature Harappan, Late Harappan | MAP-EXPLICIT-MATURE, MAP-EXPLICIT-LATE | Tier 1 — Rao (1979), *Lothal: A Harappan Port Town*, Vol. I (MASI 78), pp. 28–36: Period A = Mature phase (pp. 28–33), Period B = Late Harappan occupation (pp. 33–36); pagination as cited in Frenez's published survey of the Lothal evidence. |
| mohenjo daro | Mature Harappan, Late Harappan | MAP-EXPLICIT-MATURE, MAP-JHUKAR | Tier 1 — Dales & Kenoyer (1986), *Excavations at Mohenjo-Daro, Pakistan: The Pottery* (University Museum Monograph 53): Phase A = Mature Harappan occupation; Phase B = Jhukar pottery in the upper levels (Fig. 13.1, Pl. 18F, Figs. 63.1, 86.1–7, as cited in Mughal 1990). |
| rangpur | Mature Harappan | MAP-EXPLICIT-MATURE | Tier 1 — Rao (1963), *Ancient India* 18–19: 5–207: Period IIA and IIB = late phase of the Mature Harappan culture (Period IIC "Transition" and Period III "Post-Harappan" unmapped). |
| rojdi | Late Harappan | MAP-EXPLICIT-LATE | Tier 1 — Possehl & Raval (1989), *Harappan Civilization and Rojdi*, p. 13: Rojdi A–C = Sorath Harappan, a regional expression of the Harappan Urban Phase (unmapped). Tier 4 — Weber (1991), the published Rojdi palaeobotanical study (pp. 165–183 as cited): Rojdi C represents the Late Harappan Period. Only one determination maps, so there is no contest. |

## Contested list

- **banawali** — Bisht (1982), the site report, maps to {Mature Harappan} (its Period I is named "Pre-Harappan", which has no mapping-table entry); the 2014 *Journal of Archaeological Science* review records Early Harappan levels at Banawali, mapping to {Early Harappan, Mature Harappan}. The union is recorded with `contested: true` and both determinations retained, per the frozen §5.

## Blank list (reason codes)

| Site | Reason | Basis |
|---|---|---|
| chagylly | OUTSIDE_LABEL_SET | The gazetteer row's own published values (`PN`, `Neo.`, XRONOS record 73011) stand outside the Harappan sequence; the frozen §4 names them outside the label set. |
| mullali | OUTSIDE_LABEL_SET | Same, XRONOS record 73022 (`PN`, `Neo.?`). |
| yalangach | OUTSIDE_LABEL_SET | Same, XRONOS record 73026 (`PN`, `Neo.?`). |
| piklihal | OUTSIDE_LABEL_SET | Allchin (1960), *Piklihal Excavations* (tier 1): Neolithic occupation, followed by Megalithic. |
| kanispur | OUTSIDE_LABEL_SET | Mani, ASI excavation reports (IAR): Period I aceramic Neolithic, Period II ceramic Neolithic, then Kushan-period occupation. |
| ojiyana | OUTSIDE_LABEL_SET | Meena & Tripathi, ASI season reports (IAR 1999–2000 to 2001–02): a single Chalcolithic deposit belonging entirely to the Ahar Culture. |
| hiregudda | OUTSIDE_LABEL_SET | Fuller et al. (2007): Neolithic occupation (Sanganakallu-Kupgal ashmound complex). |
| sannarachamma | OUTSIDE_LABEL_SET | Fuller et al. (2007): Neolithic occupation (same complex). |
| sheri khan tarakai | OUTSIDE_LABEL_SET | Petrie, Khan & Knox (eds) (2010), Bannu Archaeological Project monograph (tier 1): late Neolithic village occupation, c. 4500–3000 BC. |
| shahr i sokhta | UNMAPPED_SCHEME_VALUE | Published sequence of four site periods (I–IV; Tosi 1976; Biscione et al. 1977; Salvatori & Tosi 2005, as restated 2021): site-scheme ordinals, no mapping-table entry. A revised sequence exists in print; both schemes are unmapped, so the blank stands either way. |
| ter kala dheri | UNMAPPED_SCHEME_VALUE | Petrie, Khan & Knox (2010), ch. 10.3: transitional deposits between the Sheri Khan Tarakai Phase and the Tochi-Gomal Phase — named regional phases, no mapping-table entry. |
| desalpur | NO_PUBLISHED_DETERMINATION | Only a passing transitional-phase mention (Desalpur IB) in the regional literature was located; no admissible determination verified under the bar. |
| islam chowki | NO_PUBLISHED_DETERMINATION | Cholistan survey site (Mughal 1997 universe); no per-site published determination verified in this assembly. |
| joenniemi | NO_PUBLISHED_DETERMINATION | No published determination located in this assembly. |
| qasim bagh | NO_PUBLISHED_DETERMINATION | Cholistan survey site (Mughal 1997 universe); no per-site published determination verified in this assembly. |
| sheri khan tarakai 3 | NO_PUBLISHED_DETERMINATION | Bannu Archaeological Project survey locus; no locus-level published determination verified. |
| sheri khan tarakai 4 | NO_PUBLISHED_DETERMINATION | Bannu Archaeological Project survey locus; no locus-level published determination verified. |
| surkotada | NO_PUBLISHED_DETERMINATION | The site monograph (Joshi 1990, MASI 87) publishes a Period IA/IB/IC sequence; no statement equating it to a label-set value could be verified under the bar in this assembly. |
| tigrana | NO_PUBLISHED_DETERMINATION | Recent excavations (Central University of Haryana, 2016–2021) are reported in press and institutional summaries; no published determination with a verifiable locator was assembled under the bar. |

## Completeness by source (frozen §6.3)

| Gazetteer source | Rows catalogued | Sites | Sites assigned | Sites contested |
|---|---|---|---|---|
| XRONOS | 21 | 21 | 4 | 1 |
| CISI Vol. 1 catalogue (Phase-124 layer) | 11 | 11 | 9 | 1 |
| CISI Vol. 2 catalogue (Phase-124 layer) | 4 | 4 | 4 | 0 |

(Site counts are per source; four sites appear in more than one source, so the site columns sum to more than the 30 distinct sites. Assignments grounded per evidence base: every assignment above rests on tier-1 or tier-4 published determinations assembled under the verification bar; no tier-2 or tier-3 determination was needed except Kenoyer (2008) at Harappa, corroborating the tier-4 statement. Disagreements carried: the one contested site, banawali.)

## Margins verification step (DD-039-5)

The Phase-395 period-eligibility gate was re-run over Output A under Spec 031's frozen rule F031-C10 (a site is period-eligible iff its gazetteer record indicates a Mature Harappan presence):

- **Period-eligible sites, contested counted: 8 of 30** — amri, banawali, harappa, kalibangan, khirsara, lothal, mohenjo daro, rangpur.
- **Period-eligible sites, contested excluded: 7 of 30** (banawali removed).

The step is confined to that gate. It records the closure it was frozen to record: **in-universe link mass is 2 link-eligible sites and 1 linked pair, against floors of 8 eligible sites and 10 linked pairs — the step closes at the link-mass floor.** No response, matrix, permutation, or Q7 verdict was computed. **Q7 still fails its link-mass floors; this act changes no study outcome; Q6 remains NOT-YET-TESTABLE.** The labels are finding aids, not dating evidence. Spec 030 Ask 2 remains RESERVED and is untouched by this act.
