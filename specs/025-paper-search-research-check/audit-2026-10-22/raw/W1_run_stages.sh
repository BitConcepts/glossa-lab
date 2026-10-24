#!/bin/bash
cd ~/workspace/glossa-audit/backend
set -a; . ~/workspace/glossa-run/research-api-keys.env; set +a
export PAPER_SEARCH_MCP_CORE_API_KEY="$CORE_API_KEY" PAPER_SEARCH_MCP_OPENALEX_API_KEY="$OPENALEX_API_KEY"
RAW=~/workspace/glossa-audit/specs/025-paper-search-research-check/audit-2026-10-22/raw
PY=~/workspace/venvs/glossa-lab/bin/python
echo "START $(date -Is)" > $RAW/W1_stages.log
$PY -m glossa_lab.research_check --claim-file ~/workspace/glossa-audit/glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json --claim-id yadav_2009_arxiv_manual_001 --alt-phrasing "rank frequency power law fit for sign counts in the Mahadevan Indus corpus undeciphered script" --doi 10.1371/journal.pone.0009506 >> $RAW/W1_stages.log 2>&1; echo "001-2009 exit:$?" >> $RAW/W1_stages.log
$PY -m glossa_lab.research_check --claim-file ~/workspace/glossa-audit/glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json --claim-id yadav_2009_arxiv_manual_002 --alt-phrasing "signs occurring disproportionately at the start or end of short Indus inscriptions positional frequency analysis" --doi 10.1371/journal.pone.0009506 >> $RAW/W1_stages.log 2>&1; echo "002-2009 exit:$?" >> $RAW/W1_stages.log
$PY -m glossa_lab.research_check --claim-file ~/workspace/glossa-audit/glossa-indus/claims/extracted_claims/yadav_2010_ngrams.json --claim-id yadav_2010_ngrams_manual_001 --alt-phrasing "rank frequency power law fit for sign counts in the Mahadevan Indus corpus undeciphered script" --doi 10.1371/journal.pone.0009506 >> $RAW/W1_stages.log 2>&1; echo "001-2010 exit:$?" >> $RAW/W1_stages.log
$PY -m glossa_lab.research_check --claim-file ~/workspace/glossa-audit/glossa-indus/claims/extracted_claims/yadav_2010_ngrams.json --claim-id yadav_2010_ngrams_manual_002 --alt-phrasing "signs occurring disproportionately at the start or end of short Indus inscriptions positional frequency analysis" --doi 10.1371/journal.pone.0009506 >> $RAW/W1_stages.log 2>&1; echo "002-2010 exit:$?" >> $RAW/W1_stages.log
echo "DONE $(date -Is)" >> $RAW/W1_stages.log
