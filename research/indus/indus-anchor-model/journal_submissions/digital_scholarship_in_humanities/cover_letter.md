# Cover Letter
## Digital Scholarship in the Humanities (DSH)

---

Dear Editors,

Please consider the attached manuscript, **"A Falsifiable Computational Anchor Model for the Indus Script: Positional Grammar, Token Coverage, and Cross-Corpus Validation Targets"**, for publication in *Digital Scholarship in the Humanities*.

## Scope and fit

*Digital Scholarship in the Humanities* publishes work at the intersection of computational methods and humanities scholarship, with emphasis on methodology, reproducibility, and novel applications to cultural heritage problems. This manuscript presents a computational study of the Indus Valley Script — one of the longest-standing unsolved problems in historical linguistics — using positional analysis, collocational statistics, permutation tests, network betweenness centrality, and systematic candidate sign-anchor modeling. The study does not claim final decipherment. It proposes and tests a falsifiable model of Indus-script structure and candidate sign readings with explicit confidence tiers and documented cross-corpus validation targets.

## Core contribution

The manuscript's primary contribution is methodological: it separates high-confidence structural claims (non-random positional grammar, fish-sign compound-only behavior, betweenness centrality stratification) from lower-confidence candidate phonetic readings, and provides a public reproducibility package for testing both. The most important structural result is that 0/140 fish-sign occurrences across 9 sites and the Gulf deposit catalog appear in isolation — a site-invariant result that survives every adversarial challenge applied. The betweenness centrality stratification (20/161 H+M signs with BC > 0 as grammar candidates; 141/161 with BC = 0 as name-syllable candidates) is a novel application of network-science methods to corpus epigraphy.

## Manuscript details

- **Proposed title:** A Falsifiable Computational Anchor Model for the Indus Script: Positional Grammar, Token Coverage, and Cross-Corpus Validation Targets
- **Running title:** Indus Script Anchor Model
- **Approximate word count:** ~5,200 words (excluding tables and appendices)
- **Primary corpus:** Holdat LLC Indus Corpus v3, 1,670 seals, 7,002 tokens, 9 sites
- **Public repository:** https://github.com/BitConcepts/glossa-lab
- **Zenodo archive:** (to be assigned on submission)

## Companion submission

A companion data paper, **"A Reusable Anchor Table and Validation Package for Computational Analysis of the Indus Script"**, is being prepared for *Journal of Open Humanities Data*. The companion paper describes the public data tables and scripts in detail, emphasising reuse potential. If the editors consider a cross-reference appropriate, we are happy to coordinate timing.

## Data availability

All analysis scripts and public data tables are available in the GitHub repository. The primary corpus (Holdat LLC Indus Corpus v3) is not redistributed due to licensing; analysis scripts accept any equivalent corpus after sign-code crosswalking. All corpus-dependent results are labelled as requiring restricted access in the data dictionary. The ICIT corpus is identified as the public validation target.

## AI disclosure

This research was conducted with AI-assisted computational tooling (Glossa-Lab pipeline). All statistical tests were designed, executed, and interpreted by the author; AI tooling was used for scripting, data management, and literature search. The AI Disclosure section of the manuscript follows the conventions described in the preprint.

## Conflicts of interest

None to declare.

## Suggested reviewers

The manuscript would benefit from review by scholars with expertise in: (1) corpus linguistics and computational epigraphy; (2) Indus script scholarship (Mahadevan, Parpola, or Wells tradition); (3) network analysis in humanities contexts; (4) reproducibility standards in digital humanities. We do not oppose review by scholars skeptical of computational approaches to undeciphered scripts — rigorous adversarial review is welcome.

## Opposed reviewers

None.

Sincerely,

Tristen Kyle Pierson
Glossa-Lab / BitConcepts LLC
