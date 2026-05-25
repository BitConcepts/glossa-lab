# Grammar Model Scripts

## Purpose

Implements and validates the three-slot positional grammar model for the
Indus script: INITIAL (title/determinative) → MEDIAL (name/qualifier) →
TERMINAL (case suffix/grammatical marker).

This is the core structural claim (Tier 1) of the falsifiable computational
anchor model.

## Planned scripts

- `run_grammar_inference.py` — Infer positional slot assignments for all
  417 Mahadevan signs from corpus data using the method described in
  preprint §3.7. Outputs slot probabilities and dominant-slot assignments.
- `run_grammar_validation.py` — Cross-validate inferred slots against the
  known HIGH-confidence anchors. Compute precision/recall for slot
  prediction using the H+M anchor set as ground truth.
- `run_trigram_model.py` — Fit a trigram language model over the slot
  sequence (I→M→T) and compute perplexity to quantify how well the
  three-slot grammar explains observed sequences.

## Inputs

- **Holdat LLC Indus Corpus v3** (required) — per-seal sign sequences.
- `anchor_table.csv` — sign IDs, readings, and confidence tiers.
- `formula_bigram_table.csv` — bigram frequencies for structural validation.

## Outputs

- `outputs/tables/grammar_slot_assignments.csv`
- `outputs/tables/grammar_cross_validation.csv`
- `outputs/tables/trigram_model_perplexity.csv`
- `outputs/logs/grammar_model_report.txt`

## Reproducibility status

**REQUIRES_RESTRICTED_CORPUS** — Grammar inference requires the full
per-seal sign-sequence data from the Holdat LLC corpus. The released
anchor table and bigram table provide partial evidence (positional
keywords in Basis field, bigram directionality), but independent
recomputation of slot probabilities requires corpus access.

## Claim tier

**Tier 1 (structural)** — The three-slot grammar is a falsifiable
structural property.  If the grammar model fails to achieve low
perplexity or if slot assignments are random, the model is falsified.
