#!/bin/bash
# W4 RESEARCH-CHECK stage runs, serial. Started 2026-10-22 by worker W4.
cd ~/workspace/glossa-audit/backend || exit 1
set -a; . ~/workspace/glossa-run/research-api-keys.env; set +a
export PAPER_SEARCH_MCP_CORE_API_KEY="$CORE_API_KEY" PAPER_SEARCH_MCP_OPENALEX_API_KEY="$OPENALEX_API_KEY"
PY=~/workspace/venvs/glossa-lab/bin/python
EC=~/workspace/glossa-audit/glossa-indus/claims/extracted_claims
LOGD=~/workspace/glossa-audit/specs/025-paper-search-research-check/audit-2026-10-22/raw

run() {
  local tag="$1" file="$2" id="$3" alt="$4"
  echo "=== START $tag $(date -Iseconds) ===" >> "$LOGD/W4_stage_runs.log"
  "$PY" -m glossa_lab.research_check --claim-file "$EC/$file" --claim-id "$id" --alt-phrasing "$alt" > "$LOGD/W4_stage_${tag}.log" 2>&1
  echo "=== DONE $tag rc=$? $(date -Iseconds) ===" >> "$LOGD/W4_stage_runs.log"
}

WK=without_kings_or_conquests_the_indus_scr_ce9d98cc.json
PA=positional_analysis_of_indus_signs_a2bedc93.json
WL=the_archaeology_and_epigraphy_of_indus_w_27f45a68.json

run manual_001 "$WK" without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001 "Indus inscriptions segmented into initial medial and terminal sign positions: a prefix middle suffix positional structure or grammar of Indus texts, with sign classes defined by preferred text position"
run manual_003 "$WK" without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003 "animal and faunal signs in the Indus script occur preferentially in initial inscription position: positional frequency distribution of unicorn bull fish signs at the beginning of Indus texts"
run manual_004 "$WK" without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004 "Indus signs preferentially in terminal inscription position: the most frequent final sign of Indus texts as a suffix or grammatical ending marker, Mahadevan terminal sign positional frequency"
run manual_002 "$WK" without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002 "Indus script as a non royal administrative and ritual symbol system: the non-linguistic symbol thesis of Farmer Sproat and Witzel and the debate over whether Indus signs encode language"
run manual_005 "$WK" without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_005 "classification of the Indus sign list into sign groups and clusters by frequency co-occurrence and positional behaviour: Fuls catalog of Indus signs, Mahadevan concordance tables, Parpola sign list"
run wk_statisti_0002 "$WK" without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002 "Andreas Fuls positional analysis of Indus signs: normalized weighted sign position histograms classifying signs as initial early-medial mid-medial late-medial terminal or post-terminal across the ICIT corpus of Indus inscriptions"
run pa_statisti_0001 "$PA" positional_analysis_of_indus_signs_a2bedc93_statisti_0001 "Fuls 2013 positional analysis of Indus signs in Problems of Epigraphy: positional histograms distinguish allographs from distinct signs and classify Indus signs by preferred position in 2474 complete texts"
run wl_statisti_0003 "$WL" the_archaeology_and_epigraphy_of_indus_w_27f45a68_statisti_0003 "Fuls positional analysis of Indus signs reproduced as appendix in Wells The Archaeology and Epigraphy of Indus Writing: signs classified initial medial terminal by positional frequency histograms"
run wl_sign_val_0001 "$WL" the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001 "Bryan Wells Indus sign 821 the doubled sign read as city in the Dholavira signboard and used in a variety of contexts: positional distribution of sign 820 and 821 in patterned and complex texts"
run wl_sign_val_0002 "$WL" the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002 "Bryan Wells Indus sign 297 identified as the horned tiger from iconographic correspondence on seal M-1919: tiger signs in the Indus sign lists of Wells Fuls Mahadevan and Parpola"
echo "ALL W4 STAGE RUNS COMPLETE $(date -Iseconds)" >> "$LOGD/W4_stage_runs.log"
