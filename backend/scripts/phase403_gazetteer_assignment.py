#!/usr/bin/env python3
"""Phase-403 — Spec 039 gazetteer period-assignment act.

Executes the frozen Spec 039 contract
(specs/039-gazetteer-period-assignment/freeze.md, digest
ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742):
the 30 gazetteer sites receive program period assignments
from published determinations ONLY (owner decision D2,
Option 1), mapped through the frozen mapping table (§4 of
the frozen spec), each assignment carrying its evidence
(citation, locator, published value, period scheme).
Undetermined sites stay null with a recorded reason code;
nothing is inferred and nothing is repaired.

Outputs:
  A — data/movement/gazetteer_rows_assigned.jsonl (new
      file; all 36 rows byte-identical to the pre-act file
      outside `program_period_assignment`; the pre-act file
      is verified against its frozen pin and never edited).
  B — reports/phase403_results.json (the results record;
      the per-site report is
      reports/phase403_gazetteer_assignment_report.md).

Verification step (DD-039-5): the Phase-395 period-
eligibility gate is re-run over Output A under Spec 031's
frozen rule F031-C10 — a site is period-eligible iff its
record indicates a Mature Harappan presence — reported
both ways for contested sites. The step is confined to
that gate; it records the link-mass floor closure and
reopens no Q7 machinery. Standing fences: the labels are
finding aids, not dating evidence; the act changes no
study outcome; Q7 still fails its link-mass floors
(in-universe link mass 2 link-eligible sites / 1 linked
pair against floors of 8 eligible sites / 10 linked
pairs); Q6 remains NOT-YET-TESTABLE; Spec 030 Ask 2
remains RESERVED.

Determinations were assembled against a verification bar:
a determination is recorded only where the act verified
the published statement in the publication's own text or
in a published scholarly restatement quoting it with
pagination. A site with determinations whose mapped label
sets differ is contested; a single determination's own
multi-period statement is a multi-label record, not a
contest.

Fail-closed: any pin, shape, or mapping-table violation
aborts before any output is written.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_PRE_ACT = _REPO / "data/movement/gazetteer_rows.jsonl"
_OUT_A = _REPO / "data/movement/gazetteer_rows_assigned.jsonl"
_OUT_B = _REPO / "reports/phase403_results.json"

PRE_ACT_SHA256 = (
    "5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6")
FREEZE_DIGEST = (
    "ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742")
REVIEWER = "Muse Spark via Muse (AI agent)"

EARLY = "Early Harappan"
MATURE = "Mature Harappan"
LATE = "Late Harappan"
LABEL_SET = {EARLY, MATURE, LATE}

# The frozen mapping table (spec §4). Execution adds no
# entries and improvises none.
MAPPING_RULES = {
    "MAP-EXPLICIT-EARLY", "MAP-EXPLICIT-MATURE",
    "MAP-EXPLICIT-LATE", "MAP-EXPLICIT-MULTI",
    "MAP-RANGE-EARLY-MATURE", "MAP-RANGE-MATURE-LATE",
    "MAP-RANGE-EARLY-LATE", "MAP-HARP-RAVI",
    "MAP-HARP-KOTDIJI", "MAP-HARP-HARAPPAN",
    "MAP-HARP-CEMETERY-H", "MAP-JHUKAR", "MAP-CEMETERY-H",
}

# Link-mass floors and the standing in-universe link mass,
# from the frozen Phase-395 record (spec §8 / DD-039-5).
FLOOR_ELIGIBLE_SITES = 8
FLOOR_LINKED_PAIRS = 10
LINK_MASS_SITES = 2
LINK_MASS_PAIRS = 1


def det(tier, citation, locator, value, scheme, rules, labels,
        note=None):
    d = {
        "source_tier": tier,
        "citation": citation,
        "locator": locator,
        "published_value": value,
        "period_scheme": scheme,
        "mapping_rules": rules,
        "mapped_labels": labels,
    }
    if note:
        d["note"] = note
    return d


# ── The assembled determinations (published only) ────────
# Site → (determinations, blank_reason_or_None, blank_note)
EVIDENCE: dict[str, tuple[list, str | None, str | None]] = {
    "amri": ([
        det(1,
            "Casal, J.-M. (1964) Fouilles d'Amri. Paris: "
            "Klincksieck (Commission des Fouilles "
            "Archéologiques).",
            "The Amri period sequence: Period III is the "
            "Harappan occupation and Period IIID the Jhukar "
            "level; the Period IIID Jhukar equation is "
            "discussed in Mughal (1990).",
            "Period III — Harappan (Mature) occupation; "
            "Period IIID — Jhukar",
            "Amri site sequence (Casal 1964)",
            ["MAP-EXPLICIT-MATURE", "MAP-JHUKAR"],
            [MATURE, LATE]),
    ], None, None),
    "banawali": ([
        det(1,
            "Bisht, R.S. (1982) 'Excavations at Banawali: "
            "1974–77', in Possehl, G.L. (ed.) Harappan "
            "Civilization: A Contemporary Perspective. New "
            "Delhi: Oxford & IBH / AIIS, pp. 113–124.",
            "The Banawali period sequence, pp. 113–124.",
            "Period I — Pre-Harappan (Kalibangan industry); "
            "Period II — Mature Harappan; Period III — "
            "Post-Harappan (Banawali-Bara)",
            "Banawali site sequence (Bisht 1982)",
            ["MAP-EXPLICIT-MATURE"], [MATURE],
            "Period I ('Pre-Harappan') and Period III "
            "('Post-Harappan') carry no frozen mapping-table "
            "entry and map to nothing."),
        det(4,
            "'Archaeobotanical evidence of millets in the "
            "Indian subcontinent with some observations on "
            "their role in the Indus civilization', Journal "
            "of Archaeological Science (2014), review of the "
            "Saraswat/Pokharia archaeobotanical corpus.",
            "Core-zone summary: sorghum recorded from the "
            "Early Harappan (3000–2500 BC) at Kunal and "
            "Banawali and from the Mature Harappan "
            "(2500–2000 BC) at Banawali and Rohira.",
            "Early Harappan and Mature Harappan levels at "
            "Banawali",
            "Three-period Harappan scheme",
            ["MAP-EXPLICIT-EARLY", "MAP-EXPLICIT-MATURE"],
            [EARLY, MATURE]),
    ], None, None),
    "chagylly": ([
        det(3,
            "XRONOS export record, as carried in the "
            "gazetteer row itself (record_id 73011).",
            "The row's period_label_as_published field.",
            "PN, Neo.",
            "XRONOS periods field",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "PN/Neo. stand affirmatively outside the Harappan "
        "sequence; the frozen spec §4 names them outside "
        "the label set."),
    "desalpur": ([], "NO_PUBLISHED_DETERMINATION",
        "Assembly located only a passing transitional-phase "
        "mention (Desalpur IB) in the regional Kathiawar "
        "literature; no admissible determination verified "
        "under the act's bar."),
    "harappa": ([
        det(4,
            "Meadow, R.H. & Kenoyer, J.M. (2001) 'Recent "
            "discoveries and highlights from excavations at "
            "Harappa: 1998–2000', Indo-Koko-Kenkyu (Indian "
            "Archaeological Studies) 22: 19–36.",
            "The five-period Harappa sequence stated in the "
            "article (pp. 19–36).",
            "Period 1 — Ravi aspect of the Hakra Phase; "
            "Period 2 — Kot Diji (Early Harappa) Phase; "
            "Period 3 — Harappa Phase; Period 4 — Harappa / "
            "Late Harappa transitional; Period 5 — Late "
            "Harappa Phase (Cemetery H)",
            "Harappa five-period sequence (HARP)",
            ["MAP-HARP-RAVI", "MAP-HARP-KOTDIJI",
             "MAP-HARP-HARAPPAN", "MAP-HARP-CEMETERY-H"],
            [EARLY, MATURE, LATE]),
        det(3,
            "Kenoyer, J.M. (2008) 'Indus Valley Tradition', "
            "in Pearsall, D.M. (ed.) Encyclopedia of "
            "Archaeology. New York: Academic Press — Table 1 "
            "(chronology of Harappa).",
            "Table 1: Period 1 Ravi Phase and Period 2 Kot "
            "Diji Phase = Early Harappan; Period 3 Harappa "
            "Phase = Mature Harappan; Period 5 Late "
            "Harappan (Cemetery H).",
            "Ravi Phase, Kot Diji Phase (Early Harappan); "
            "Harappa Phase (Mature Harappan); Cemetery H "
            "(Late Harappan)",
            "Harappa five-period sequence (HARP)",
            ["MAP-HARP-RAVI", "MAP-HARP-KOTDIJI",
             "MAP-HARP-HARAPPAN", "MAP-HARP-CEMETERY-H"],
            [EARLY, MATURE, LATE]),
    ], None, None),
    "hiregudda": ([
        det(4,
            "Fuller, D.Q., Korisettar, R., "
            "Venkatasubbaiah, P.C. & Jones, M.K. (2007) "
            "'Dating the Neolithic of South India: new "
            "radiometric evidence for key economic, social "
            "and ritual transformations' (published journal "
            "article).",
            "The Hiregudda and Sannarachamma discussion: "
            "'the evidence from Hiregudda and Sannarachamma "
            "indicate that the Neolithic period in the "
            "Sanganakallu-Kupgal area begins with ashmound "
            "creation activities'.",
            "Neolithic occupation",
            "South Indian Neolithic sequence",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "'Neolithic' stands affirmatively outside the "
        "Harappan sequence."),
    "islam chowki": ([], "NO_PUBLISHED_DETERMINATION",
        "A Cholistan survey site of the Mughal (1997) "
        "gazetteer universe; no per-site published "
        "determination verified in this act's assembly."),
    "jhukar": ([
        det(4,
            "Mughal, M.R. (1990) 'The Decline of the Indus "
            "Civilization and the Late Harappan Period in "
            "the Indus Valley', Lahore Museum Bulletin "
            "3(2).",
            "The Jhukar site discussion: Early, Middle and "
            "Late Jhukar Phases treated as the Late Harappan "
            "manifestation in Sindh; a Harappan Period "
            "occupation is recorded in trench CIV.",
            "Jhukar Phases (Early, Middle, Late) within the "
            "Late Harappan Period; underlying Harappan "
            "Period occupation",
            "Jhukar phase sequence (Mughal 1990)",
            ["MAP-JHUKAR"], [LATE],
            "The unqualified 'Harappan Period occupation' "
            "carries no mapping-table entry and maps to "
            "nothing."),
    ], None, None),
    "joenniemi": ([], "NO_PUBLISHED_DETERMINATION",
        "No published determination located in this act's "
        "assembly."),
    "kalibangan": ([
        det(1,
            "Lal, B.B. et al. (2003) Excavations at "
            "Kalibangan: The Harappans (1960–69), Part 1. "
            "New Delhi: Archaeological Survey of India; and "
            "Lal, B.B. et al. (2015) Part 2, Memoirs of the "
            "Archaeological Survey of India 110.",
            "Part 1 covers 'the Early Harappan times "
            "(Period I)'; Part 2 Preface (MASI 110): 'the "
            "first one dealt mainly with the Early Harappan "
            "settlement (Period I)… the present one is "
            "devoted to the Mature Harappan settlement "
            "(Period II)'.",
            "Period I — Early Harappan; Period II — Mature "
            "Harappan",
            "Kalibangan site sequence, equated in the "
            "excavation report itself",
            ["MAP-EXPLICIT-EARLY", "MAP-EXPLICIT-MATURE"],
            [EARLY, MATURE]),
    ], None, None),
    "kanispur": ([
        det(1,
            "Mani, B.R., excavation reports on Kanispur in "
            "Indian Archaeology — A Review (1998–99 season; "
            "summarised IAR 2004: 30–40; Mani 2000: 139).",
            "The Kanispur period sequence as published in "
            "the ASI reports.",
            "Period I — Aceramic Neolithic; Period II — "
            "Ceramic Neolithic; later Kushan-period (early "
            "historic) occupation",
            "Kanispur site sequence (ASI)",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "'Neolithic' stands affirmatively outside the "
        "Harappan sequence."),
    "khirsara": ([
        det(4,
            "Nath, J., Kumaran, R.N. & Kulkarni, S. (2012) "
            "'A Preliminary Report on the Excavations at "
            "Khirsara, Gujarat', Puratattva 42: 122–132.",
            "Excavation-season report, pp. 122–132.",
            "The entire cultural deposit at Khirsara "
            "belongs to the mature phase of the Harappan "
            "culture",
            "Three-period Harappan scheme",
            ["MAP-EXPLICIT-MATURE"], [MATURE]),
        det(4,
            "Pokharia, A.K. et al. (2017) 'Ancient Indian "
            "rice (Oryza sativa L.) processing and "
            "agricultural adaptations at Khirsara, a "
            "Harappan site in western India', PLoS ONE "
            "12(10): e0185684.",
            "Site description: a mature Harappan phase "
            "occupation (c. 2600–2100 BCE).",
            "Mature Harappan phase occupation",
            "Three-period Harappan scheme",
            ["MAP-EXPLICIT-MATURE"], [MATURE]),
    ], None, None),
    "kunal": ([
        det(4,
            "Khatri, J.S. & Acharya, M. (1995) 'Kunal: A "
            "New Indus-Saraswati (Early Harappan) site in "
            "Haryana', Puratattva 25: 84–86.",
            "Excavation report, pp. 84–86.",
            "Early Harappan (Hakra ware) settlement",
            "Three-period Harappan scheme",
            ["MAP-EXPLICIT-EARLY"], [EARLY]),
        det(4,
            "'Archaeobotanical evidence of millets in the "
            "Indian subcontinent with some observations on "
            "their role in the Indus civilization', Journal "
            "of Archaeological Science (2014).",
            "Core-zone summary: sorghum recorded from the "
            "Early Harappan (3000–2500 BC) at Kunal and "
            "Banawali.",
            "Early Harappan levels at Kunal",
            "Three-period Harappan scheme",
            ["MAP-EXPLICIT-EARLY"], [EARLY]),
    ], None, None),
    "lothal": ([
        det(1,
            "Rao, S.R. (1979) Lothal: A Harappan Port Town "
            "(1955–62), Vol. I. New Delhi: Archaeological "
            "Survey of India (Memoirs 78).",
            "pp. 28–36: Period A, the Mature phase, at "
            "pp. 28–33; Period B, the Late Harappan "
            "occupation, at pp. 33–36 (pagination as cited "
            "in Frenez's published survey of the Lothal "
            "evidence).",
            "Period A — Mature phase; Period B — Late "
            "Harappan occupation",
            "Lothal site sequence (Rao 1979)",
            ["MAP-EXPLICIT-MATURE", "MAP-EXPLICIT-LATE"],
            [MATURE, LATE]),
    ], None, None),
    "mohenjo daro": ([
        det(1,
            "Dales, G.F. & Kenoyer, J.M. (1986) Excavations "
            "at Mohenjo-Daro, Pakistan: The Pottery. "
            "Philadelphia: University Museum, University of "
            "Pennsylvania (University Museum Monograph 53).",
            "The Phase A / Phase B periodisation of the "
            "Mohenjo-daro pottery; the Phase B Jhukar "
            "material at Fig. 13.1, Pl. 18F, Figs. 63.1 and "
            "86.1–7, as cited in Mughal (1990).",
            "Phase A — Mature Harappan occupation; Phase B "
            "— Jhukar pottery in the upper levels",
            "Mohenjo-daro pottery phases (Dales & Kenoyer)",
            ["MAP-EXPLICIT-MATURE", "MAP-JHUKAR"],
            [MATURE, LATE]),
    ], None, None),
    "mullali": ([
        det(3,
            "XRONOS export record, as carried in the "
            "gazetteer row itself (record_id 73022).",
            "The row's period_label_as_published field.",
            "PN, Neo.?",
            "XRONOS periods field",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "PN/Neo. stand affirmatively outside the Harappan "
        "sequence; the frozen spec §4 names them outside "
        "the label set."),
    "ojiyana": ([
        det(1,
            "Meena, B.R. & Tripathi, A., Ojiyana excavation "
            "reports, Indian Archaeology — A Review "
            "(1999–2000, 2000–01, 2001–02 seasons).",
            "The Ojiyana cultural sequence as published in "
            "the ASI season reports.",
            "A single Chalcolithic deposit belonging "
            "entirely to the Ahar Culture, in three phases",
            "Ojiyana site sequence (ASI)",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "The Ahar-culture Chalcolithic stands affirmatively "
        "outside the Harappan sequence."),
    "piklihal": ([
        det(1,
            "Allchin, F.R. (1960) Piklihal Excavations. "
            "Hyderabad: Government of Andhra Pradesh "
            "(Archaeological Series 8).",
            "The Piklihal sequence: Neolithic occupation "
            "(Lower and Upper Neolithic), followed by "
            "Megalithic.",
            "Neolithic",
            "Piklihal site sequence (Allchin 1960)",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "'Neolithic' stands affirmatively outside the "
        "Harappan sequence."),
    "qasim bagh": ([], "NO_PUBLISHED_DETERMINATION",
        "A Cholistan survey site of the Mughal (1997) "
        "gazetteer universe; no per-site published "
        "determination verified in this act's assembly."),
    "rangpur": ([
        det(1,
            "Rao, S.R. (1963) 'Excavations at Rangpur and "
            "Other Explorations in Gujarat', Ancient India "
            "18–19: 5–207.",
            "The Rangpur period sequence in the excavation "
            "report.",
            "Period IIA — late phase of the Mature "
            "Harappan culture; Period IIB — late phase of "
            "the Mature Harappan culture; Period IIC — "
            "Transition; Period III — Post-Harappan "
            "(Lustrous Red Ware)",
            "Rangpur site sequence (Rao 1963)",
            ["MAP-EXPLICIT-MATURE"], [MATURE],
            "Period IIC ('Transition') and Period III "
            "('Post-Harappan') carry no mapping-table entry "
            "and map to nothing."),
    ], None, None),
    "rojdi": ([
        det(1,
            "Possehl, G.L. & Raval, M.H. (1989) Harappan "
            "Civilization and Rojdi. New Delhi: Oxford & "
            "IBH / AIIS.",
            "p. 13: Rojdi A–C classed as Sorath Harappan.",
            "Rojdi A, B and C — Sorath Harappan, a regional "
            "expression of the Harappan Urban Phase",
            "Rojdi site sequence (Possehl & Raval 1989)",
            [], [],
            "'Sorath Harappan' and the 'Urban Phase' carry "
            "no mapping-table entry and map to nothing."),
        det(4,
            "Weber, S.A. (1991) 'Plants and Harappan "
            "Subsistence: An Example of Stability and "
            "Change from Rojdi' (published study of the "
            "Rojdi sequence).",
            "The Rojdi A/B/C period discussion (pp. 165–183 "
            "as cited in the published literature).",
            "Rojdi A and Rojdi B fall into the Harappan "
            "Period; Rojdi C (2000–1700 BC) represents the "
            "Late Harappan Period",
            "Rojdi site sequence",
            ["MAP-EXPLICIT-LATE"], [LATE]),
    ], None, None),
    "sannarachamma": ([
        det(4,
            "Fuller, D.Q., Korisettar, R., "
            "Venkatasubbaiah, P.C. & Jones, M.K. (2007) "
            "'Dating the Neolithic of South India: new "
            "radiometric evidence for key economic, social "
            "and ritual transformations' (published journal "
            "article).",
            "The Hiregudda and Sannarachamma discussion "
            "(as for hiregudda).",
            "Neolithic occupation",
            "South Indian Neolithic sequence",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "'Neolithic' stands affirmatively outside the "
        "Harappan sequence."),
    "shahr i sokhta": ([
        det(4,
            "Provenance study of archaeological ceramics "
            "from Shahr-i Sokhta, Archaeological and "
            "Anthropological Sciences (2021), Springer; "
            "restating Tosi (1976), Biscione et al. (1977) "
            "and Salvatori & Tosi (2005).",
            "'Four periods of settlement can be "
            "distinguished… at the Shahr-i Sokhta site "
            "based on eleven structural layers (Tosi 1976; "
            "Biscione et al. 1977; Sajjadi 2004)'.",
            "Periods I, II, III and IV of the site sequence",
            "Shahr-i Sokhta site sequence",
            [], []),
    ], "UNMAPPED_SCHEME_VALUE",
        "A site-scheme ordinal sequence with no "
        "mapping-table entry; generic ordinals never map "
        "across schemes (frozen §4). A revised sequence "
        "(Ascalone & Vecchio) exists in print; both schemes "
        "are unmapped, so the blank stands either way."),
    "sheri khan tarakai": ([
        det(1,
            "Petrie, C.A., Khan, F. & Knox, J.R. (eds) "
            "(2010) Sheri Khan Tarakai and Early Village "
            "Life in the Borderlands of North-West Pakistan. "
            "Oxford: Oxbow (Bannu Archaeological Project).",
            "The monograph's occupation account; the site "
            "is treated as a late Neolithic village "
            "occupation, c. 4500–3000 BC.",
            "Neolithic (the Sheri Khan Tarakai Phase)",
            "Bannu basin regional sequence",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "'Neolithic' stands affirmatively outside the "
        "Harappan sequence."),
    "sheri khan tarakai 3": ([], "NO_PUBLISHED_DETERMINATION",
        "A survey locus of the Bannu Archaeological "
        "Project; no locus-level published determination "
        "verified in this act's assembly."),
    "sheri khan tarakai 4": ([], "NO_PUBLISHED_DETERMINATION",
        "A survey locus of the Bannu Archaeological "
        "Project; no locus-level published determination "
        "verified in this act's assembly."),
    "surkotada": ([], "NO_PUBLISHED_DETERMINATION",
        "The site monograph (Joshi 1990, Memoirs of the "
        "ASI 87) publishes a Period IA/IB/IC sequence; no "
        "statement equating that sequence to a label-set "
        "value could be verified under the act's "
        "verification bar in this assembly. The blank "
        "records the bar, not the absence of print."),
    "ter kala dheri": ([
        det(1,
            "Petrie, C.A., Khan, F. & Knox, J.R. (eds) "
            "(2010) Sheri Khan Tarakai and Early Village "
            "Life in the Borderlands of North-West Pakistan. "
            "Oxford: Oxbow (Bannu Archaeological Project).",
            "Chapter 10.3 discussion of the regional phase "
            "sequence: transitional deposits at Ter Kala "
            "Dheri straddle the Sheri Khan Tarakai and "
            "Tochi-Gomal Phases.",
            "Transitional between the Sheri Khan Tarakai "
            "Phase and the Tochi-Gomal Phase",
            "Bannu basin regional sequence",
            [], []),
    ], "UNMAPPED_SCHEME_VALUE",
        "Named regional phases with no mapping-table "
        "entry."),
    "tigrana": ([], "NO_PUBLISHED_DETERMINATION",
        "The recent excavations (Central University of "
        "Haryana, 2016–2021) are reported in press and "
        "institutional summaries; no published "
        "determination with a verifiable locator was "
        "assembled under the act's bar."),
    "yalangach": ([
        det(3,
            "XRONOS export record, as carried in the "
            "gazetteer row itself (record_id 73026).",
            "The row's period_label_as_published field.",
            "PN, Neo.?",
            "XRONOS periods field",
            [], []),
    ], "OUTSIDE_LABEL_SET",
        "PN/Neo. stand affirmatively outside the Harappan "
        "sequence; the frozen spec §4 names them outside "
        "the label set."),
}


def fail(msg: str) -> None:
    print(f"PHASE-403 FAIL-CLOSED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def build_assignment(dets: list) -> tuple[dict | None, list[str], bool]:
    """Apply the frozen mapping table to one site's
    determinations. Returns (assignment, label_set,
    contested). A determination whose mapped label set is
    empty contributes no labels; two or more mapping
    determinations whose label sets differ make the site
    contested (frozen §5)."""
    label_sets = []
    for d in dets:
        for r in d["mapping_rules"]:
            if r not in MAPPING_RULES:
                fail(f"mapping rule not in the frozen table: {r}")
        if set(d["mapped_labels"]) - LABEL_SET:
            fail(f"label outside the frozen label set: "
                 f"{d['mapped_labels']}")
        if d["mapped_labels"]:
            label_sets.append(set(d["mapped_labels"]))
    if not label_sets:
        return None, [], False
    union: set[str] = set().union(*label_sets)
    order = [EARLY, MATURE, LATE]
    labels = [x for x in order if x in union]
    contested = len({frozenset(s) for s in label_sets}) > 1
    rules_used: list[str] = []
    for d in dets:
        for r in d["mapping_rules"]:
            if r not in rules_used:
                rules_used.append(r)
    evidence = []
    for d in dets:
        e = {
            "source": f"tier {d['source_tier']} (frozen "
                      f"citation hierarchy, DD-039-2)",
            "citation": d["citation"],
            "locator": d["locator"],
            "published_value": d["published_value"],
            "period_scheme": d["period_scheme"],
            "mapping_rule": d["mapping_rules"] or None,
            "mapped_labels": d["mapped_labels"],
        }
        if d.get("note"):
            e["note"] = d["note"]
        evidence.append(e)
    assignment = {
        "label": labels[0] if len(labels) == 1 else labels,
        "mapping_rule": rules_used,
        "reviewer": REVIEWER,
        "evidence": evidence,
    }
    if contested:
        assignment["contested"] = True
    return assignment, labels, contested


def main() -> int:
    # ── Step 0: input integrity, fail-closed ─────────────
    raw = _PRE_ACT.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PRE_ACT_SHA256:
        fail(f"pre-act gazetteer pin mismatch: {digest}")
    text = raw.decode("utf-8")
    lines = text.splitlines()
    if len(lines) != 36:
        fail(f"expected 36 rows, found {len(lines)}")
    rows = [json.loads(ln) for ln in lines]
    sites = sorted({r["program_site_id"] for r in rows})
    if len(sites) != 30:
        fail(f"expected 30 sites, found {len(sites)}")
    if any(r["program_period_assignment"] is not None
           for r in rows):
        fail("pre-act assignments are not all null")
    if set(EVIDENCE) != set(sites):
        fail(f"evidence table does not cover exactly the "
             f"30 sites: missing="
             f"{set(sites) - set(EVIDENCE)}, extra="
             f"{set(EVIDENCE) - set(sites)}")
    for ln in lines:
        if ln.count('"program_period_assignment": null') != 1:
            fail("assignment field token not unique in a row")

    # ── Step 1: per-site assignments ─────────────────────
    per_site: dict[str, dict] = {}
    for site in sites:
        dets, blank_reason, blank_note = EVIDENCE[site]
        assignment, labels, contested = build_assignment(dets)
        rec: dict = {
            "determinations": len(dets),
            "evidence": dets,
        }
        if assignment is not None:
            if blank_reason is not None:
                fail(f"{site}: has both an assignment and a "
                     f"blank reason")
            rec.update({
                "status": "assigned",
                "labels": labels,
                "contested": contested,
                "assignment": assignment,
            })
        else:
            if blank_reason is None:
                fail(f"{site}: no assignment and no blank "
                     f"reason")
            rec.update({
                "status": "blank",
                "reason_code": blank_reason,
                "note": blank_note,
            })
        per_site[site] = rec

    assigned = {s: r for s, r in per_site.items()
                if r["status"] == "assigned"}
    blanks = {s: r for s, r in per_site.items()
              if r["status"] == "blank"}
    contested_sites = sorted(
        s for s, r in assigned.items() if r["contested"])

    # ── Step 2: Output A by byte-preserving surgery ──────
    out_lines = []
    for ln, row in zip(lines, rows):
        site = row["program_site_id"]
        rec = per_site[site]
        if rec["status"] == "assigned":
            payload = json.dumps(
                rec["assignment"], ensure_ascii=False,
                sort_keys=True)
            out_lines.append(ln.replace(
                '"program_period_assignment": null',
                f'"program_period_assignment": {payload}', 1))
        else:
            out_lines.append(ln)
    out_a_text = "\n".join(out_lines) + "\n"
    # Verify: byte-identical outside the assignment field.
    check = [json.loads(ln) for ln in out_a_text.splitlines()]
    if len(check) != 36:
        fail("output A row count changed")
    for before, after in zip(rows, check):
        b = dict(before)
        a = dict(after)
        b.pop("program_period_assignment")
        a.pop("program_period_assignment")
        if b != a:
            fail("output A differs outside the assignment "
                 "field")
    _OUT_A.write_text(out_a_text, encoding="utf-8")
    out_a_sha = hashlib.sha256(
        out_a_text.encode("utf-8")).hexdigest()

    # ── Step 3: the margins verification step (DD-039-5) ─
    # Frozen rule F031-C10 over Output A: a site is
    # period-eligible iff its gazetteer record indicates a
    # Mature Harappan presence (period_label_as_published
    # or the program assignment, after this act).
    def indicates_mature(row: dict, assignment) -> bool:
        vals = row.get("period_label_as_published") or []
        if any("Mature" in str(v) for v in vals):
            return True
        if assignment is not None:
            lab = assignment["label"]
            labs = lab if isinstance(lab, list) else [lab]
            if MATURE in labs:
                return True
        return False

    site_rows: dict[str, list] = {}
    for row in check:
        site_rows.setdefault(row["program_site_id"],
                             []).append(row)
    eligible_counted, eligible_excl = [], []
    for site in sites:
        rec = per_site[site]
        asg = rec.get("assignment")
        ok = any(indicates_mature(r, asg)
                 for r in site_rows[site])
        if ok:
            eligible_counted.append(site)
            if not rec.get("contested"):
                eligible_excl.append(site)
    margins = {
        "rule": "F031-C10 (frozen, Spec 031): period-"
                "eligible iff the gazetteer record "
                "indicates a Mature Harappan presence",
        "eligible_sites_contested_counted": eligible_counted,
        "eligible_count_contested_counted":
            len(eligible_counted),
        "eligible_sites_contested_excluded": eligible_excl,
        "eligible_count_contested_excluded":
            len(eligible_excl),
        "floor_eligible_sites": FLOOR_ELIGIBLE_SITES,
        "in_universe_link_mass": {
            "link_eligible_sites": LINK_MASS_SITES,
            "linked_pairs": LINK_MASS_PAIRS,
            "floor_sites": FLOOR_ELIGIBLE_SITES,
            "floor_pairs": FLOOR_LINKED_PAIRS,
        },
        "closure": "The step closes at the link-mass "
                   "floor: in-universe link mass is 2 "
                   "link-eligible sites and 1 linked pair "
                   "against floors of 8 eligible sites and "
                   "10 linked pairs. Q7 still fails its "
                   "link-mass floors; this act changes no "
                   "study outcome; Q6 remains "
                   "NOT-YET-TESTABLE.",
    }

    # ── Step 4: §6.3 completeness by source ──────────────
    by_source: dict[str, dict] = {}
    for row in rows:
        src = row["source_gazetteer"]
        e = by_source.setdefault(src, {
            "rows": 0, "sites": set(), "assigned_sites": set(),
            "contested_sites": set()})
        e["rows"] += 1
        e["sites"].add(row["program_site_id"])
        if row["program_site_id"] in assigned:
            e["assigned_sites"].add(row["program_site_id"])
        if row["program_site_id"] in contested_sites:
            e["contested_sites"].add(row["program_site_id"])
    completeness = {}
    for src, e in sorted(by_source.items()):
        completeness[src] = {
            "rows_catalogued": e["rows"],
            "sites": len(e["sites"]),
            "sites_assigned": len(e["assigned_sites"]),
            "sites_contested": len(e["contested_sites"]),
        }

    label_tally: dict[str, int] = {}
    for r in assigned.values():
        for lab in r["labels"]:
            label_tally[lab] = label_tally.get(lab, 0) + 1
    reason_tally: dict[str, int] = {}
    for r in blanks.values():
        reason_tally[r["reason_code"]] = (
            reason_tally.get(r["reason_code"], 0) + 1)

    results = {
        "phase": 403,
        "spec": "039-gazetteer-period-assignment",
        "freeze_digest": FREEZE_DIGEST,
        "executed": "2026-10-20",
        "input": {
            "file": "data/movement/gazetteer_rows.jsonl",
            "sha256": digest,
            "rows": 36,
            "sites": 30,
            "assignments_null_pre_act": 36,
        },
        "output_a": {
            "file": "data/movement/"
                    "gazetteer_rows_assigned.jsonl",
            "sha256": out_a_sha,
            "rows": 36,
            "byte_identical_outside_assignment_field": True,
            "pre_act_file_modified": False,
        },
        "coverage": {
            "sites_total": 30,
            "sites_assigned": len(assigned),
            "sites_blank": len(blanks),
            "label_tally": label_tally,
            "blank_reason_tally": reason_tally,
        },
        "contested_sites": contested_sites,
        "per_site": {
            s: {k: v for k, v in rec.items()
                if k != "assignment"}
            for s, rec in sorted(per_site.items())
        },
        "assignments": {
            s: rec["assignment"]
            for s, rec in sorted(assigned.items())
        },
        "margins_verification": margins,
        "completeness_by_source": completeness,
        "standing_fences": [
            "The labels are finding aids, not dating "
            "evidence.",
            "The act changes no study outcome.",
            "Q7 still fails its link-mass floors (link "
            "mass 2 sites / 1 pair vs floors 8 / 10).",
            "Q6 remains NOT-YET-TESTABLE.",
            "Spec 030 Ask 2 remains RESERVED.",
        ],
    }
    _OUT_B.write_text(
        json.dumps(results, indent=2, ensure_ascii=False,
                   sort_keys=True) + "\n", encoding="utf-8")
    print(f"Phase-403 complete: assigned "
          f"{len(assigned)}/30 sites; contested "
          f"{contested_sites}; blanks {len(blanks)} "
          f"{reason_tally}; eligible counted "
          f"{len(eligible_counted)}, excluded "
          f"{len(eligible_excl)}; output A sha256 "
          f"{out_a_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
