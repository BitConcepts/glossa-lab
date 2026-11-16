# Spec 095 — claims

Seventeen claims, C095-1..C095-17, each with its falsifier and its does-not-establish line. The claims consolidate the fourteen NEW items the 2026-11-15 reconciliation register isolated from the external red-team review (register section N) plus this spec's governance claims (the register as scope of record, the corpus identity standard, and the derived-documents rule). Nothing here re-opens a settled verdict, and nothing here commissions a build stage: Stage 0 (reconciliation and register) is complete at adoption, and the build stages run in the adopted queue (D-095-2).

## The claims

**C095-1 — The reconciliation register is the scope of record.** The red-team reconciliation register of 2026-11-15 (43 rows, RT-01..RT-43) is this program's scope of record for the external red-team review of 2026-11-15: every row carries exactly one disposition (DUPLICATE-OF-RECORD with its owning vehicle named, NEW with its register section-N item named, or FACT-DISPUTED with the governing record named); the review's one confirmed defect (RT-03) sits inside the NEW rows as a micro-task on a duplicate family, and its one security risk requiring verification (RT-06) sits inside the duplicate rows under its Spec 083 vehicle; the 23 duplicate rows are worked only under their owning vehicles (Spec 092's remainder, Spec 094, Specs 091, 093, 088, 053 and 083, and the named gap-register entries), and no work item exists in this spec for a duplicate row.

*Falsifier:* A register row is found without a disposition, with two dispositions, or naming no owning vehicle or section-N item; or a stage task in this spec is found whose work duplicates a duplicate row's owning vehicle.

*Does not establish:* that any duplicate row's underlying work is complete, correct, or scheduled; the register maps scope, it does not discharge it.

**C095-2 — Pinnability remediation is locate-first and fail-closed.** The strict-corpus artifact firestore_indusarrays_full.jsonl is located and verified against its intake pin of record (PR #393, 2026-10-25: SHA-256 073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578; census 3,916 records / 3,137 sequences / 2,665 dockeys / 12,494 sign instances) before any use: a candidate file whose digest differs from the pin stops the remediation; a verified file is placed read-only at the canonical path glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl, its census and the canonical export pin of record (prefix e90fd7ce41121529) reproduce exactly through the V3 loader, and Spec 053's frozen step 0 is re-executed only under a new execution order with its gates unchanged.

*Falsifier:* The artifact is used, placed, or a re-execution is ordered with a digest that differs from the pin; the placed file is writable; the loader census or the export pin differs from the pinned census on the placed file; or Spec 053's gates are altered in the re-execution order.

*Does not establish:* anything about Spec 053's substantive result; the claim yadav_2009_arxiv_manual_001 stands as recorded until a re-execution under unchanged gates produces its own record.

**C095-3 — Every claim-bearing corpus carries an immutable identity, checked at load.** Every corpus a claim in this program rests on carries an immutable identity of record (version, content hash, source, licensing terms, object, inscription and sign counts under a named counting basis, and normalization rules) stated in the corpus's own intake or identity record, and every loader of a claim-bearing corpus fails closed, refusing to run and naming the mismatch, when the identity is missing or any element differs from the record.

*Falsifier:* A claim-bearing corpus is found in use without a complete identity of record; or a loader executes against a corpus whose hash, counts, or normalization differ from its identity record without refusing.

*Does not establish:* that any corpus's contents are correct or complete; identity pins what was used, not whether it was right.

**C095-4 — The twelve-case fail-closed loader battery runs as a named CI suite.** A named suite in CI exercises twelve fail-closed loader cases against the program's claim-bearing loaders (missing corpus, wrong content hash, same-name-different-corpus, empty loader result, duplicate identifiers, contradictory mappings, unknown signs, damaged spans, reversed reading order, partial availability, unauthorized access, and synthetic-presented-as-real), every case refuses or flags as its case definition requires, and the suite runs on every change to a covered loader.

*Falsifier:* Any of the twelve cases executes silently, returns data, or passes its fixture without the defined refusal or flag; or a covered loader changes without the suite running.

*Does not establish:* that loaders are correct on well-formed input; the battery proves refusal behavior on malformed identity and content, not analytic correctness.

**C095-5 — No v1 validator routine remains executable unguarded in a claim-bearing path.** No corrected-validator v1 routine remains executable in a claim-bearing path of the live application unguarded: each of the four live v1 node paths of record (phonotactics v1 via the Phase-58 and Phase-108 experiment nodes; site-statistics v1 via the Phase-69 node and the provenance recompute; crosswalk v1 via the Phase-96 node) is migrated to its corrected v2 module, retired from the node registry, or mechanically guarded so its output cannot enter a claim-bearing record unlabelled; and a pinning test that plants a legacy-rule call in a claim-bearing path fails.

*Falsifier:* Any of the four paths executes its v1 routine in the live app without migration, retirement, or a mechanical guard; or the planted legacy-rule call passes the pinning test.

*Does not establish:* that any historical result computed with a v1 routine is wrong; the exposure of record is prospective, and historical results stand or fall by their own revalidation entries (GR-088-03).

**C095-6 — The synthetic corpus is contained by census and a planted-fixture test.** Every consumer of the synthetic indus_public_corpus is enumerated and classified (test, demonstration, or claim-bearing) in a census of record, and no claim-bearing path consumes it: a planted fixture that presents the synthetic corpus as a real corpus in a claim-bearing path fails a pinning test, and the public loader's synthetic labelling is machine-checked, not comment-only.

*Falsifier:* A consumer of indus_public_corpus is found that the census does not name or misclassifies; or the planted synthetic-as-real fixture passes.

*Does not establish:* that the synthetic corpus is useless; it remains available to its classified test and demonstration consumers under its label.

**C095-7 — Contamination shapes are flagged mechanically at intake.** The claims-ledger gate carries a check class that flags, at intake, the six contamination shapes of record (a source-derived value labelled independent; a self-labelling derivative presented as source data; a translation or reading column presented as corpus data; a derived result presented as independent confirmation; the same data under two source identities; a summary or delivery presented as the underlying record), and the class re-detects the six historical instances of record (the GR-088-01, GR-088-11, GR-088-16 and GR-088-29 family) from their records in its acceptance fixtures.

*Falsifier:* An intake exhibiting one of the six shapes passes the gate unflagged; or any of the six historical instances is not re-detected from its record.

*Does not establish:* that flagged intakes are substantively wrong; the class flags provenance shape for adjudication, it does not rule on content.

**C095-8 — Equivalence and statistical reporting are stated once, program-wide.** Program-wide standards of record state, once, the program's equivalence and statistical-reporting rules: equivalence is claimed only against a preregistered margin with an equivalence test, never from a non-significant difference; and a statistical result is reportable only with its effect size, uncertainty interval, multiplicity handling, and achieved power or precision basis, never a p-value alone; studies adopted after this standard cite it instead of restating local rules.

*Falsifier:* A program record adopted after the standard claims equivalence from a non-significant difference, reports a p-value without the required companions, or restates a local equivalence rule in place of the standard.

*Does not establish:* that any past result retroactively satisfies the standard; earlier results keep the rules they were frozen under.

**C095-9 — Supported readings pass a rival-construction identifiability protocol.** Before a reading claim is scored SUPPORTED at any strength, a rival-construction exercise of record attempts to fit the same evidence with a rival sign function (and, where the claim is phonetic, a rival value from a named unrelated language family); the program's outcome vocabulary gains NOT IDENTIFIABLE by a recorded amendment when the rival construction fits comparably; and the protocol is first applied to the six independently supported anchors of record (M044, M047, M124, M202, M329, M330), whose standings are re-stated under the protocol's outcome, whatever it is.

*Falsifier:* A reading is scored SUPPORTED after the protocol's adoption with no rival-construction record; a rival fits comparably and the outcome is not recorded NOT IDENTIFIABLE; or the six anchors' re-statement under the protocol does not exist.

*Does not establish:* that any reading is false; NOT IDENTIFIABLE bounds what the evidence can distinguish, it does not disprove a reading.

**C095-10 — Reading direction is carried as data.** Reading direction is carried as data: every inscription-level record in a claim-bearing corpus states its orientation basis, every positional or sequential result names the orientation assumption it was computed under, and every such result is reported beside its reversed-orientation variant or an explicit statement of why reversal is undefined for it.

*Falsifier:* A positional or sequential result is found in a claim-bearing record with no named orientation assumption, or with no reversed variant and no undefined-reversal statement.

*Does not establish:* that either orientation is correct for any inscription; the claim governs reporting, not the undecided direction question.

**C095-11 — The multi-script abstraction is specified, and the Indus record instantiates it unchanged.** The multi-script data model is specified with claims and falsifiers of its own: seventeen entities (WritingSystem, LanguageHypothesis, Corpus, Artifact, Inscription, Sign, SignVariant, Transcription, ReadingHypothesis, TranslationHypothesis, Context, Evidence, Claim, Falsifier, Experiment, Execution, Result, Adjudication) with sign shape held separate from phonetic value and semantic interpretation, and no Indus-specific or Proto-Dravidian assumption inside the generic layer; the Indus record instantiates the model without changing a single Indus fact, count, or standing.

*Falsifier:* The specification lacks claims or falsifiers for any of the seventeen entities; a generic-layer rule names an Indus or Proto-Dravidian assumption; or instantiating the model alters any Indus record.

*Does not establish:* that any other script's data exists in the system; the model is specified and the Indus record instantiated, nothing more.

**C095-12 — The dashboard home and feature set are wireframe-first and name their refusals.** The platform gains a dashboard home and the feature set of record (program status, inscription explorer, hypothesis comparison, evidence inspection, experiment reproduction, researcher contribution), each built wireframe-first with the owner's approval of the wireframes by name and Playwright verification at desktop and mobile widths before any verified claim, and each feature naming its refusals in its specification (no automatic promotion of any candidate, no self-certification of any claim), with the Research Assistant boundary inherited from Spec 025 (advisory only) and Spec 094 (no automated approval).

*Falsifier:* A feature ships without owner-approved wireframes or without desktop and mobile rendered verification; a feature's specification omits its refusals; or any feature promotes or certifies automatically.

*Does not establish:* that the features are usable or used; usability is C095-13's question, and adoption of any feature by researchers is a separate matter.

**C095-13 — The functional and usability audit package runs scored, with screenshot evidence.** A scored functional and usability audit package runs on the Spec 083 acceptance vehicle: the functional checklist and the eight-step new-researcher protocol of record (arrive from the public page; establish what the system claims and does not claim; find one inscription and its evidence trail; distinguish observation, transcription, hypothesis and claim; reproduce one published result; submit one candidate with a falsifier; follow its adjudication; export the audit trail), plus an accessibility pass over the same surfaces; every failure is filed with its screenshot evidence, and the package's scores are stated against thresholds fixed before the run.

*Falsifier:* The audit runs without pre-fixed thresholds; a step is scored without evidence; a failure is filed without screenshot evidence; or the accessibility pass is absent.

*Does not establish:* that the platform is fit for any particular researcher; the package scores the audited tasks only.

**C095-14 — One composed thirteen-component release gate, exceptions only on the record.** Releases of the platform and its public claims are gated by one composed gate of thirteen components of record (unit tests, integration tests, frontend tests, end-to-end tests, ledger validation, corpus identity verification, anchor regression, claim-stage validation, provenance completeness, security checks, accessibility checks, reproducibility smoke test, public-claims consistency), each component's result recorded per release candidate, exceptions existing only as recorded owner-approved entries, and a planted stale public claim of the RT-03 shape blocks the candidate it is planted in.

*Falsifier:* A release ships with a component unrun or failed and no recorded owner-approved exception; or the planted stale claim does not block its candidate.

*Does not establish:* that a gated release is correct in substance; the gate proves the checks ran and passed, not that the science is right.

**C095-15 — Eteocypriot enters as proposal and preregistration draft only.** The Eteocypriot second-target work under this spec is a proposal and preregistration draft only: the draft states the corpus's legal status and source, the bilingual and sign-list basis, the held-out design, and the adjudication route before any analysis exists; no Eteocypriot analysis is executed under this spec, and execution requires a separate owner decision recorded outside this spec's stages.

*Falsifier:* Any Eteocypriot analysis output exists under this spec; or the draft lacks the legal status, the held-out design, or the adjudication route.

*Does not establish:* that Eteocypriot is tractable, related to any other script, or evidence about the Indus script in either direction.

**C095-16 — Meroitic enters as a scoped reproduction benchmark on the existing fixture.** The Meroitic work under this spec is the scoping of a reproduction benchmark as a study spec: an independent implementation reproduces published sign-frequency and positional results from the openly published 2025 Meroitic corpus, against success criteria and a falsifier fixed in the scoping record, using the existing fixture module as its starting inventory; the benchmark's execution is a separately commissioned study, not a stage of this spec.

*Falsifier:* Meroitic benchmark results are produced as a stage task of this spec; or the scoping record lacks fixed success criteria or a falsifier.

*Does not establish:* that the deciphered Meroitic values validate any Indus method; the benchmark tests pipeline fidelity on a solved script, and transfer to an undeciphered script is a separate claim requiring its own evidence.

**C095-17 — Red-team documents are derived only and carry no authority.** Any document under docs/red-team/ is a derived document: it names the records it derives from on its face, states no rule, verdict, or requirement of its own, and is never cited as authority for a program decision; the governing records remain the reconciliation register, this spec, and the vehicles the register names.

*Falsifier:* A docs/red-team/ document is found without its sources named, stating a rule or verdict of its own, or cited as authority in a program record.

*Does not establish:* that derived documents are complete or current; derivation is a reading aid, and staleness in a derived document is corrected by regenerating it, never by editing the record it derives from.
