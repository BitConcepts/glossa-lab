# Spec 027 — Plan

> ## DRAFT — PROPOSAL FOR OWNER ADJUDICATION
>
> This plan executes nothing. Its stage sequence becomes
> operative only after the owner answers spec §13, and each
> stage still requires its own freeze before execution.

**Governing documents:** `spec.md`, `claims.json`, and
`checklists/requirements.md` in this directory; Spec 026's
framework artifacts; the Glossa constitution; and governance
rules H2, H6, H13, and H15/H23.

**Tooling record:** `working/tooling.md`. Versions pinned for
this draft's lifecycle runs: specify CLI 1.0.10; AEE extension
v1.1.0; evaluator extension v1.0.0; AEE package 1.0.4 from the
Glossa venv on PATH. The spec-kit venv carries AEE package
1.0.2, so every AEE invocation in this spec must state and pin
its PATH rather than rely on the ambient environment.

## 1. Draft lifecycle (this PR)

1. **Constitution check** — spec §14 and §4 below.
2. **Specify** — `spec.md` plus the structured claim register
   `claims.json`; integrity checked with Spec 026 machinery.
3. **Clarify** — unresolved choices are carried as spec §13
   decision asks, not filled in by implication.
4. **Plan** — this document.
5. **Requirements checklist** — `checklists/requirements.md`.
6. **Tasks** — `tasks.md`, with every future execution task
   gated on adjudication and a stage freeze.
7. **Analyze** — requirements, claims, plan, checklist, and
   tasks cross-checked for traceability and orphan work.
8. **AEE hooks** — AEE assess plus evaluator-contract outputs
   saved under `aee/` after specify, plan, and tasks. Any
   outcome stricter than `warn` blocks draft closure until its
   recovery record is complete.
9. **Draft PR** — bannered DRAFT, left open and unmerged;
   append-only entries in both ledgers record that the draft
   was opened.

## 2. Stage sequence after adjudication

Each stage is expected to be its own PR sequence, merged on CI
verified from the run's own conclusion and job logs. No stage
inherits execution authority from the prior stage's success.

### Stage 0 — Gazetteer and chronology spine

**Purpose:** descriptive infrastructure only (spec §6).

Work packages, in dependency order:

1. **Source and licence audit**
   - Enumerate the Possehl, Law, TwoRains, and any owner-added
     published gazetteer sources.
   - Assign each source a §5.1 licence state from inspected
     terms.
   - Enumerate XRONOS and the underlying databases reached
     through c14bazAAR; record versions and retrieval dates in
     the eventual freeze.
   - Stop condition: a source with `unverified` or
     `permission_required` status is catalogued, not copied.
2. **Gazetteer schema and validation**
   - Implement the §6.2 row schema as a versioned data contract.
   - Validators assert source, locator, period scheme, licence,
     coordinate state, and origin group on every retained row.
   - Clustering into `program_site_id` is a separate governed
     rule; source rows are never overwritten by a cluster.
3. **Gazetteer build**
   - Transcribe or transform only lawfully reusable fields.
   - Preserve source disagreements; produce coverage, duplicate,
     conflict, and survey-bias reports.
   - Restricted coordinates remain at or below source precision.
4. **Chronology-spine schema and validation**
   - Implement the §6.4 row schema.
   - Validators reject aggregate period assertions as timing
     rows and require material plus context-association grade.
   - Charcoal and other long-lived material carry old-wood risk;
     short-lived status is explicit or `unknown`.
5. **Chronology build**
   - Trace each date to its underlying database and publication.
   - Preserve competing chronology assertions as scenarios,
     including both Mehrgarh chronologies with Mutin et al.
     marked CONTESTED.
6. **Stage 0 closeout**
   - Descriptive report by question (Q1–Q9 fitness), claim
     integrity check, foundation check if any phase/data result
     is introduced, and ledger entries.
   - Publication only under the owner's §13 Ask 4 choice and
     only through the release gate; no publication is part of
     the stage's scientific closeout.

**Stage 0 freeze must name:** source versions, licence evidence,
schemas, clustering rule, calibration curve/version, chronology
scenario treatment, phase number and graph nodes (H15/H23),
input/output hashes, and validation tests.

### Stage 1 — Q2 repertoire gate

**Purpose:** decide whether the bounded recorded-repertoire
site effect survives the frozen controls (spec §7).

Sequence:

1. **Owner values inserted** — governing sign list (Ask 2) and
   corpus inclusion rules (Ask 3) from adjudication.
2. **Margins-only corpus audit** — population flow, sign-list
   version coverage, object-type and stratum completeness,
   permutable-cell projections, and dominant-site shares. No
   repertoire outcome is computed in the audit.
3. **Stage 1 freeze** — estimand, practical margin, interval
   rule, rarefaction rule and seed, permutation strata,
   jackknife, positive/negative controls, completeness grid,
   corpus hash, crosswalk sensitivity if any, and verdict rules
   from spec §7.6.
4. **H15/H23 gate** — future phase script, graph module,
   registration, and registration verification in order before
   the run.
5. **Execution and report** — effect plus interval beside any
   permutation result; per-object-type report where the grid
   supports it; all sensitivities and model variants reported.
6. **Closure branch**
   - SUPPORTED: downstream work still requires a new proposal;
   - CONTRADICTED: negative closure — all downstream
     repertoire-geography work under Spec 027 stops;
   - INCONCLUSIVE: no downstream work on the unadjudicated
     estimand;
   - INVALID: instrument record preserved; a corrected design
     is a new version and new freeze, never a silent rerun.

**Stage 1 timing:** Ask 5 decides whether Stage 1 proceeds on
the adjudicated design after Stage 0 and its freeze, or returns
for a separate owner go.

### Stage 2A — Q7 material and craft networks

May enter design only after Stage 0 closes and the D8
provenance/licence audit is complete.

1. Build the provenance-link register with method per link.
2. Freeze site-pair matrices, geographic and river controls,
   period eligibility, sample-size rules, network statistic,
   practical margin, jackknife, and negative controls.
3. Model ceramic similarity and craft-technique similarity
   separately.
4. Report only the bounded material/technique result. Any
   people or language wording is a hard-limit defect requiring
   correction before closeout.

### Stage 2B — Q6 standardisation timing

May enter design only if the Stage 0 report evidences the
§8.2 support conditions without inspecting timing outcomes.

1. Freeze the trait list and the site/region completeness grid.
2. Freeze the timing model, priors or equivalent assumptions,
   chronology scenario, rival patterns, and decision thresholds.
3. Execute once under the freeze.
4. If support conditions are not met, record NOT-YET-TESTABLE
   and stop; period-label co-occurrence is not a fallback test.

## 3. Blocked-question maintenance

Q1, Q3, Q4, Q5, Q8, and Q9 are maintained in a register, not in
an execution queue.

- A blocked question changes status only when its §9 data
  condition is evidenced in a dated record.
- The changed condition supports a **new design and freeze**;
  it does not retroactively authorize the registered draft
  design.
- Q4's fallback is a separate design with its weaker ceiling
  written into its freeze and every headline.
- Q8 cannot be unblocked by AI recruitment, additional prompts,
  model diversity, or agreement between correlated systems.
- Q9 cannot be unblocked by genetics or modern geography.

## 4. Constitution check

- **§I Provenance:** every Stage 0 row is source-traced;
  catalogue-only material is not copied.
- **§II Ledger:** draft opening and every future stage are
  append-only ledger events in both program ledgers.
- **§III Foundation gate:** no anchor, language-model, or phase
  result changes occur in this draft. Future stages run the
  foundation check whenever H21 is triggered.
- **§IV Falsifiable claims:** `claims.json`, §3.2 fields,
  §3.3 taxonomy, §12 boundaries, and AEE as the same engine.
- **§V Public/private:** no correspondence or personal data;
  restricted coordinates inherit source restrictions.
- **§VI AI disclosure:** present in spec, plan, tasks, and
  ledger entries.
- **§VII SDD:** sequential spec number, spec/plan/tasks,
  AEE hooks, and graph-first future phases.
- **§VIII Verification:** JSON validity, claim integrity,
  requirements traceability, CI on the draft PR, and recorded
  tool versions. No version string is introduced outside the
  tooling record's observed tool versions.

## 5. Principal risks and mitigations

| Risk | Mitigation in design |
|---|---|
| Gazetteer manufactures a false site universe | Source-asserted rows, clustering as a governed rule, conflict reports |
| A source is open to read but not to reuse | §5.1 licence states; catalogue-only default when uncertain |
| Charcoal dates are treated as direct event dates | Material and context-association audit; old-wood flag |
| Contested Mehrgarh revision is silently adopted | Competing scenarios preserved; Mutin status CONTESTED |
| Sign-list mixing recreates a corpus artefact | One governing list, version field, crosswalk sensitivity only |
| Q2 pooled result is really object-type composition | Stratification, single-type report, discriminating controls |
| Network language drifts from objects to people | Q7 licensed-conclusion rule and hard limits |
| Later language maps become hidden premises | Teleology ban; temporal model plus shift/loss rivals required |
| Correlated sources are counted as independent | Origin-group accounting; Poseidon/AADR as one group |
| Blocked questions are answered by weaker substitutes | §9 fidelity rule; unblocking requires a new freeze |

## 6. What this plan never does

Freeze or execute a stage in this draft; reserve a phase number;
copy a restricted source; publish a gazetteer; generate primary
isotope/aDNA data; use AI as Q8 coders; move an anchor; score
PRED-2026; or contact any external party.
