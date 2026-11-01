#!/usr/bin/env python3
"""Build the Spec 077 claims register (claims.json).

Written at the freeze act of 2026-10-26. The register is
drafted directly in the recovered (0.7) form used by Specs
074/075/076: every claim carries text / boundary / evidence /
falsification_tests / kind / status, and metadata carrying
boundary_confirmation, evidence_origin_groups,
forbidden_assumptions, framework_kind, layer,
strongest_rival, verdict_rule. The register carries the M7
design draft's claims D-M7-C01/C02 as F077-C01/C02 and the
design's step-0, ancestry, collision, sensitivity, gap-list
and Table I conditions as F077-C03 ... F077-C10.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

DRAFT = {
    "description": (
        "The M7 design draft of 2026-10-25 (program goal record): "
        "three-witness sign-list triangulation of the 557-sign "
        "population frame against Mahadevan 1977 and Wells "
        "1998/2006 through Registry v2, with the token 999 attack, "
        "as amended by its 2026-10-25 iteration-pass amendment "
        "(single trigger-census extraction consumed; the "
        "positional_class data-quality note). SHA-256 "
        "2e9f9967ec30a558e3a31f93f54540b3d8450e25080c447d37ecd598175c1369."
    ),
    "direction": "supports",
    "kind": "observed",
    "observed_at": "2026-10-25",
    "ref": "2026-10-25-spec-draft-m7-signary-triangulation.md (program goal record, files/)",
    "source_id": "m7 design draft (2026-10-25, goal record)",
    "source_quality": "artifact",
    "independent_of": ["owner freeze order (2026-10-26)"],
}

ORDER = {
    "description": (
        "The owner's order of 2026-10-26 09:32 EDT ('do all now' "
        "over the what's-next board), which names M7 "
        "freeze-and-execute among the acts to complete."
    ),
    "direction": "supports",
    "kind": "observed",
    "observed_at": "2026-10-26",
    "ref": "owner order 2026-10-26 (main chat)",
    "source_id": "owner freeze-and-execute order (2026-10-26)",
    "source_quality": "artifact",
    "independent_of": ["m7 design draft (2026-10-25, goal record)"],
}


def ev(description, ref, source_id, independent_of, observed_at="2026-10-26"):
    return {
        "description": description,
        "direction": "supports",
        "kind": "observed",
        "observed_at": observed_at,
        "ref": ref,
        "source_id": source_id,
        "source_quality": "artifact",
        "independent_of": independent_of,
    }


def claim(cid, text, boundary, evidence, falsification, rival, verdict_rule,
          framework_kind="empirical-measurement", layer="I",
          depends_on=None):
    return {
        "id": cid,
        "kind": "requirement",
        "status": "draft",
        "text": text,
        "boundary": boundary,
        "evidence": evidence,
        "falsification_tests": [falsification],
        "assumptions": ["ASM-APPEND-ONLY"],
        "depends_on": depends_on or [],
        "alternatives": [],
        "metadata": {
            "boundary_confirmation": "stated-in-claim",
            "evidence_origin_groups": ["m7-design", "owner-order", "spec-073-record", "spec-075-record"],
            "forbidden_assumptions": [],
            "framework_kind": framework_kind,
            "layer": layer,
            "strongest_rival": rival,
            "verdict_rule": verdict_rule,
        },
    }


CLAIMS = [
    claim(
        "F077-C01",
        "At least 90% of the 557 population signs - at least 502 of 557 - are witnessed in at least one external sign list (the Mahadevan 1977 sign list as extracted in dataset v3, or the Wells 1998 sign list as extracted from the held thesis), under Spec 077's frozen match rules (spec sections 0 and 4), and the ancestry-adjusted share - signs witnessed in the lineage's root list, M77 - is also at least 90% whenever it is the lower of the two shares.",
        "The scope is witness presence by sign number only, over the 557-sign population of Spec 075's primary population as enumerated in its pinned machine record, matched through Registry v2's crosswalk columns under FF-3/FF-4. It excludes any statement about glyph shapes, about any reading's value, and about whether any list's division of the material into signs is correct.",
        [DRAFT, ORDER,
         ev("Spec 073's keying-surface accounting (2026-10-25), which names the population frame, Registry v2's construction (396 parpola_1982 + 407 yajnadevam_glyphid + 210 icit_wells rows), the 13 duplicated Mahadevan ids, and the adopted C-7 canonical pin. Filed in the repository at specs/073-keying-surface-repair/keying-surface-accounting-2026-10-25.md.",
            "specs/073-keying-surface-repair/keying-surface-accounting-2026-10-25.md",
            "spec 073 keying-surface accounting",
            ["m7 design draft (2026-10-25, goal record)"], "2026-10-25"),
         ev("The two witness extractions as pinned in spec section 3: M77 dataset v3 (SHA-256 9c619bfe2520e63e2968be0ab4ddc9cef1f9aff7dfa3f8eddbf58f21fb414f7e; 417 rows; the printed section 11.4 checksum met exactly) and the Wells 1998 dataset (SHA-256 22bde128551adbd6d91cd76bb41b4f40199ab3e45af76d500a1008d27c5bea95; 588 rows, 587 printed entries).",
            "glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.csv; glossa-corpus/indus/sources/wells-1998/wells1998_sign_list.csv",
            "witness extraction datasets (2026-10-25/26)",
            ["m7 design draft (2026-10-25, goal record)"])],
        "an ancestry-adjusted share below 90% - fewer than 502 of 557 signs M77-witnessed under the frozen match rules - falsifies this claim and closes F077-C01 NOT SUPPORTED under the closure word SIGNARY NOT WITNESSED AT THE STATED LEVEL",
        "the reading in which presence in the descendant list (Wells 1998) corroborates a sign independently of the root list; on the filed ancestry map Wells 1998 descends from Mahadevan's concordance, so its corroboration is not independent, and the draft's falsifier is administered against the ancestry-adjusted share",
        "SUPPORTED if the ancestry-adjusted share is at least 90% (502 of 557); NOT SUPPORTED, with the closure word, below it; the raw share is reported either way",
    ),
    claim(
        "F077-C02",
        "Token 999's identity is settled by the frozen two-condition attack: a witness sign is 999's identity only if its occurrence count is within 20% of 999's population behavior (2 occurrences; administered as a witness total of exactly 2) AND its final-position rate is within 10 points of 999's (0.0; administered as a final rate of at most 0.10, at a total of 2 a final count of 0) - an M77 sign through its Table I TOT and FIN, a Wells 1998 sign through its dataset total and its Figure 3.6 pair's Table I final rate; if no witness sign meets both conditions, 999 stands NO PUBLISHED IDENTITY with the attack recorded as run.",
        "The scope is the identity question for the single population sign 999, under the two conditions the design draft states and the freeze-fixed administration of spec section 0 (FF-6/FF-7). It excludes any reading of what 999, or any candidate, means, and any identity claim sourced from outside the two witness lists.",
        [DRAFT,
         ev("Spec 073's record, which names token 999 as the one population sign with no published identity (registry-v2/no-published-identity.json) and records its 2 primary rows and 2 occurrences; Spec 075's outcome carries the same count.",
            "specs/073-keying-surface-repair/registry-v2/no-published-identity.json; specs/075-depicted-kind-endings-atlas/outcome.md",
            "spec 073/075 records on token 999",
            ["m7 design draft (2026-10-25, goal record)"], "2026-10-25"),
         ev("Token 999's reference behavior derived at this freeze from Spec 075's pinned inputs under its frozen construction (documented-lineage rows; 000 tokens dropped): 2 occurrences, 0 text-final, final-position rate 0.0; to be re-derived as a check at step 0 (F077-C04).",
            "spec section 0 (FF-6); reports/phase441_results.json census.token_999",
            "freeze derivation of 999's reference behavior",
            ["m7 design draft (2026-10-25, goal record)"])],
        "a witness sign meeting both administered conditions falsifies the NO PUBLISHED IDENTITY default and names the identity; if no witness sign meets both, the default stands and any claim of an identity for 999 from this record is falsified",
        "the reading in which a candidate matching on occurrence count alone, or on final rate alone, identifies 999; the design requires both, and a Wells sign with no Figure 3.6 pairing cannot meet the second condition at all",
        "identity named if at least one witness sign meets both conditions; otherwise NO PUBLISHED IDENTITY, with the full candidate table filed either way",
    ),
    claim(
        "F077-C03",
        "At the execution's step 0, every input pin named in spec section 3 verifies first-hand against the file as held or as fetched from repository main - Registry v2, Spec 075's machine record, both witness datasets and their JSON twins, the Figure 3.6 cross-reference file, the C-7 canonical M77 raw text, the held Wells thesis, and the restricted-local derivation inputs - and the actual columns and content of every witness table and crosswalk counted from are verified against the frozen descriptions, not taken from any artifact's self-description.",
        "The scope is the input integrity of this spec's execution only. It excludes any claim that a verified input is correct in substance - a hash match establishes identity of the file, not truth of its contents.",
        [DRAFT,
         ev("The pins as verified first-hand at this freeze act from repository main and the canonical store (registry 42ab09fb..., phase441 record f55ae911..., dataset v3 9c619bfe..., Wells dataset 22bde128..., Figure 3.6 file b0ef40da..., M77 raw text 11441e38...; thesis 5720dc01... and the volume pin ef68fe8d...e110 from their intake records).",
            "spec section 3 (inputs)",
            "freeze-act pin verification",
            ["owner freeze order (2026-10-26)"])],
        "any pin mismatch, or any witness table whose actual columns or content diverge from the frozen description, falsifies this claim and closes the execution CANNOT BE RUN AS WRITTEN naming the failed item",
        "the practice of trusting an artifact's dictionary or description over its committed content - the positional_class divergence recorded in the draft's amendment is the standing counterexample",
        "the execution proceeds only if every pin verifies; any failure closes it at step 0",
        framework_kind="integrity-gate",
    ),
    claim(
        "F077-C04",
        "Spec 075's population construction, re-run at step 0 over its pinned restricted-local inputs, reproduces the frozen census exactly - 3,045 analyzable rows, 557 distinct signs, 550 signs in sequences of length at least 2 - and token 999's reference behavior with it: 2 occurrences, 0 text-final, final-position rate 0.0.",
        "The scope is the reproduction of Spec 075's primary population under its own frozen construction (documented-lineage rows; recorded symbol lists with 000 tokens dropped; text-final position is the last sign of a sequence). It excludes the corroborated population, which enters this spec as context only.",
        [ev("Spec 075's machine record (reports/phase441_results.json, SHA-256 f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29): census.population 3,045 / 557 / 550; census.token_999 2 rows / 2 occurrences.",
            "reports/phase441_results.json",
            "spec 075 machine record",
            ["m7 design draft (2026-10-25, goal record)"], "2026-10-25"),
         ev("The reproduction performed at this freeze over the hash-verified restricted-local inputs (corpus 345241b1..., grades 02394241...) under Spec 075 section 3's construction: 3,045 analyzable sequences, 557 distinct signs, 550 in sequences of length at least 2; token 999 in exactly 2 sequences, medial in both.",
            "freeze-act reproduction (this freeze's working record)",
            "freeze-act population reproduction",
            ["spec 075 machine record"])],
        "any reproduced figure differing from the frozen census - rows, distinct signs, sequence-length count, or 999's occurrences or finals - falsifies this claim and closes the execution at step 0 as a premise failure",
        "the reading in which the population is whatever the current corpus deposit contains; the population is the frozen construction over the pinned inputs, and drift in either input or construction is a failure, not an update",
        "exact reproduction is required; any mismatch is a step-0 halt-and-report",
        framework_kind="integrity-gate",
    ),
    claim(
        "F077-C05",
        "The witness-ancestry map filed at spec section 4.1 before counting is correct on the sources it cites: Mahadevan 1977 is the root list of the modern tradition; Parpola's list and Registry v2's crosswalk columns descend from it; Wells 1998 descends from Mahadevan's concordance (its corpus is Mahadevan's texts re-segmented, and its Figure 3.6 compares its divisions against Mahadevan 1977, Fairservis 1992 and Parpola 1994); Wells 2006/2015 continues Wells 1998 - so the two counted witness lists share one lineage, and the ancestry adjustment of FF-5 applies.",
        "The scope is the descent relations among the named lists as the cited records state them. It excludes any claim that descent makes a list's contents wrong - descent bears on independence of corroboration, not on correctness.",
        [ev("The Wells 1998 extraction record (repository): Table 3.2 prints no Mahadevan numbers; the only printed Mahadevan cross-references are Figure 3.6's 55 pairings; Wells-1998 numbers do not join Registry v2's Wells-2015 wells_ids.",
            "glossa-corpus/indus/sources/wells-1998/wells_1998_sign_list_extraction_2026-10-25.md",
            "wells 1998 extraction record",
            ["m7 design draft (2026-10-25, goal record)"], "2026-10-25"),
         ev("The Phase-123 Wells segmentation witness (repository, data/crosswalks/wells_segmentation_witness_v1.csv), which sources Wells's later list to his PhD 2006 Fig. 3.2 in the Wells 2015 form of the Wells/ICIT list - the same scholar's continuation of the 1998 list.",
            "data/crosswalks/wells_segmentation_witness_v1.csv",
            "phase-123 wells witness",
            ["wells 1998 extraction record"], "2026-10-25"),
         ev("Spec 073's record of Registry v2's construction from Parpola 1982 rows, ICIT Wells rows and Yajnadevam glyph rows.",
            "specs/073-keying-surface-repair/outcome.md",
            "spec 073 outcome (registry construction)",
            ["m7 design draft (2026-10-25, goal record)"], "2026-10-25")],
        "a cited source showing a witness list compiled independently of the Mahadevan lineage - for instance a Wells list built from a corpus not derived from Mahadevan's concordance - falsifies this claim and with it the FF-5 adjustment as administered",
        "the reading in which two lists by different authors are independent witnesses by default; independence is a property of their descent, and here the descent is documented",
        "the ancestry adjustment stands or falls with this map; if the map is falsified, the adjustment is re-ruled on the record before any verdict is filed",
    ),
    claim(
        "F077-C06",
        "The 13 duplicated Mahadevan ids named in Spec 073's keying-surface accounting (M002, M050, M064, M076, M099, M103, M161, M167, M168, M199, M216, M264, M409) are resolved on the record before counting, under the frozen rule of FF-4: the step-0 record states each id's two claiming Registry v2 rows and their wells_ids sets, and a population sign is witnessed through a duplicated id only when exactly one claiming row carries its token; every other case counts as NOT witnessed through that id.",
        "The scope is the administration of the named 13 collisions for this spec's counting. It excludes adjudicating whether Mahadevan's own list or the registry's transcription is at fault in any collision - that is future registry work, as Spec 073's accounting states.",
        [ev("Spec 073's keying-surface accounting (2026-10-25): the 13 ids and their claiming row pairs - M002 {P015,P016}, M050 {P043,P044}, M064 {P054,P055}, M076 {P066,P071}, M161 {P085,P086}, M167 {P086,P101}, M168 {P086,P100}, M099 {P119,P122}, M103 {P123,P139}, M216 {P230,P234}, M264 {P260,P359}, M199 {P292,P293}, M409 {P346,P348} - with the direction that any future spec keying through mahadevan_ids must resolve these first, on the record.",
            "specs/073-keying-surface-repair/keying-surface-accounting-2026-10-25.md",
            "spec 073 keying-surface accounting",
            ["m7 design draft (2026-10-25, goal record)"], "2026-10-25")],
        "a step-0 record that cannot state a duplicated id's claiming rows from the pinned registry, or a count that witnesses a sign through a duplicated id outside the FF-4 rule, falsifies this claim",
        "the reading in which a duplicated id witnesses every sign of both claiming rows; that double-counts exactly the ambiguity the accounting named, and the draft states the conservative direction in advance",
        "counting proceeds only with the resolution table filed; unresolved-for-a-sign counts as not witnessed for that sign",
        framework_kind="integrity-gate",
    ),
    claim(
        "F077-C07",
        "Sensitivity S1 - the C01 share recomputed under the ancestry map's strictest reading, all lists sharing any lineage counted as one - is computed and reported on its own line in the outcome record; on the filed map (F077-C05) every witness shares the M77 lineage, so S1's share equals the ancestry-adjusted share, and the record says why the two coincide.",
        "The scope is the S1 recomputation as the design's section 6 states it. It excludes any use of S1 to replace the headline verdict rule, which the design fixes at section 4.1.",
        [DRAFT],
        "an S1 recomputation that differs from the ancestry-adjusted share without a difference in the underlying ancestry reading falsifies this claim's account of the two numbers",
        "the reading in which a sensitivity that coincides with the headline number was not run; S1 is run and reported, and its coincidence with the adjusted share is itself a consequence of the filed map",
        "S1 is reported beside the verdict; it does not move the verdict",
        framework_kind="sensitivity",
    ),
    claim(
        "F077-C08",
        "Sensitivity S2 - the C01 share recomputed excluding signs whose only witness is a list the registry itself was built from - is administered as FF-8 states: Registry v2 was built from Parpola 1982's list, the ICIT/Wells list and Yajnadevam's glyph list, none of which is a counted witness under FF-2, so the exclusion set is empty and S2's share equals the raw share; the outcome record states this and its reason, and reports the per-witness breakdown (M77-witnessed, Wells-1998-witnessed, witnessed by both, witnessed only by the descendant list) in full.",
        "The scope is the circularity check as the design's section 6 states it, under the frozen witness definitions. It excludes treating the registry-mediated Figure 3.6 join as a construction source: the pairings are Wells's own printed cross-references, extracted from the thesis, and the registry supplies only the population-side numbers they join to.",
        [DRAFT,
         ev("Spec 073's record of Registry v2's construction inputs (Parpola 1982, ICIT Wells, Yajnadevam), the same record F077-C05 cites for the registry's descent.",
            "specs/073-keying-surface-repair/outcome.md",
            "spec 073 outcome (registry construction)",
            ["m7 design draft (2026-10-25, goal record)"], "2026-10-25")],
        "a showing that a counted witness list is among Registry v2's construction inputs falsifies the empty-exclusion-set administration, and S2 must then be recomputed with that list's sole-witness signs excluded before any verdict is filed",
        "the reading in which the ICIT/Wells-2015 surface is both the population's keying frame and an external witness; FF-2 excludes it from the witness set for exactly this reason, and S2's emptiness follows from that exclusion, not from an oversight",
        "S2 is reported beside the verdict with its reasoning; it does not move the verdict unless its own falsifier fires",
        framework_kind="sensitivity",
    ),
    claim(
        "F077-C09",
        "The gap list - every population sign not witnessed under the frozen match rules, named by its Wells code - is computed and filed in the outcome record whether F077-C01 is supported or not, as the design's section 5 requires.",
        "The scope is the deliverable itself: the list of unwitnessed signs by list position. It excludes any interpretation of why a sign is unwitnessed, and any use of the list beyond the design's stated one (the shopping list for ICIT-route questions if the owner opens Gate G1).",
        [DRAFT],
        "an outcome record without the gap list, or a gap list inconsistent with the filed per-sign witness table, falsifies this claim",
        "the reading in which the gap list is owed only on a shortfall; the design states it is a deliverable either way",
        "the gap list is filed with the outcome record in all cases",
        framework_kind="deliverable",
    ),
    claim(
        "F077-C10",
        "C02's Mahadevan arm runs only on a Table I dataset that meets the acceptance form frozen at FF-7 - the adjudicated m77_table1_occurrences.csv in the canonical store, row equations holding wherever all five cells are present, column sums over the complete rows reconciling exactly with the printed totals row (SOL 190 / INI 3010 / MED 7196 / FIN 2976 / TOT 13372) under the landing record's stated residuals, unsettled cells carried empty and never guessed, its SHA-256 recorded at step 0 - and a sign whose TOT or FIN cell is empty is not shown to meet C02's conditions and cannot be 999's identity; if the dataset has not landed in that form when step 0 runs, the execution closes CANNOT BE RUN AS WRITTEN and no counting runs.",
        "The scope is the Table I input condition for this spec's C02 arm. It excludes the Phase A partial extraction (203 of 417 rows certain, the rest carried uncertain) as an execution input: its certain rows may be complete in themselves, but the frozen form requires the adjudicated, reconciled dataset, and substituting the partial file would change the input after the freeze.",
        [DRAFT,
         ev("The Table I Phase A extraction in the canonical store (m77_table1_occurrences.csv, SHA-256 aeec9cd1181c5d29455fba99bdfba29ac3c27e8cf852d3babd82ea9af9c0d7a6): 417 rows, 203 certain under the stated rule (all five cells clean and TOT = SOL+INI+MED+FIN), 214 uncertain with occurrences carried empty; printed totals row as frozen at FF-7.",
            "glossa-corpus/indus/sources/mahadevan-1977/m77_table1_occurrences.csv",
            "table I phase A extraction",
            ["m7 design draft (2026-10-25, goal record)"])],
        "an execution that counts C02 candidates from a Table I file failing any element of the FF-7 form - a violated row equation, a reconciliation that does not close on the printed totals row, a guessed cell - falsifies this claim and voids the run",
        "the reading in which a substantially complete Table I is close enough; the acceptance form is exact and mechanical precisely so that no judgment call about completeness is available at execution time",
        "the C02 arm runs only on the FF-7 form; otherwise the execution closes at step 0 with the input named",
        framework_kind="integrity-gate",
    ),
]

NOTE = (
    "Register drafted directly in the recovered (0.7) register form used by "
    "Specs 074/075/076's registers: every claim carries text / boundary / "
    "evidence / falsification_tests / kind / status, and metadata carrying "
    "boundary_confirmation, evidence_origin_groups, forbidden_assumptions, "
    "framework_kind, layer, strongest_rival, verdict_rule; every evidence "
    "item carries independent_of naming the other sources cited in the same "
    "claim. Assumptions referenced by id and defined here: ASM-APPEND-ONLY = "
    "program records are append-only; frozen, closed, and retired records "
    "are read under their pins and never edited; a freeze's completions of "
    "its design are stated in the spec and ruled in the adjudication, never "
    "introduced silently. The register carries the M7 design's claims "
    "D-M7-C01/C02 as F077-C01/C02, its step-0 pin and population conditions "
    "as F077-C03/C04, its ancestry map as F077-C05, its 13-collision "
    "administration as F077-C06, its sensitivities as F077-C07/C08, its "
    "gap-list deliverable as F077-C09, and the Table I input condition the "
    "freeze fixes for C02's Mahadevan arm as F077-C10. F077-C01 and "
    "F077-C02 are the verdict-bearing claims. Status values use the verified "
    "vocabulary of the adjacent registers (draft / supported / contradicted "
    "/ untested / in question / partially supported); at this freeze every "
    "claim is draft. The evaluator-side verdict on this register at the "
    "freeze is recorded in the freeze record, not here; the draft cap of "
    "the evaluator's FR-2.3 (claims in draft cap at 0.70) applies to every "
    "claim until an execution adjudicates them."
)


def main() -> int:
    bundle = {
        "spec": "077-signary-triangulation",
        "register_version": "0.7-draft",
        "note": NOTE,
        "claims": CLAIMS,
    }
    out = HERE / "claims.json"
    out.write_text(json.dumps(bundle, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} with {len(CLAIMS)} claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
