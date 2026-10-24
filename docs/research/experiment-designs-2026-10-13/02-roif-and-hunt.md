# Designs 02 — the Roif and Hunt claim families

Two published interpretations dominate the untested and half-tested claims:
Avishai Roif's reading of the script as an economic ledger of guilds and tribute,
and Treasure A. Hunt's reading of it as a civic-ritual system built in three
parts. Several of their claims share one missing input each — a classification
the repository does not yet hold. Where a design needs such a classification,
the classification is built **from published sources, entered as cited data,
and frozen before the test** — never tuned to the result.

---

## D-02 — The fish sign and the ports, tested sign by sign (residue design)

- **Claim:** `indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`
  (SETTLED — partially falsified: the claim's own coastal-enrichment test came
  back against it).
- **Feasibility:** RUNNABLE-TODAY.

**The open point.** The claim says the fish sign marked coastal traders. The
program counted fish signs across sites in its CISI-based data and found no
enrichment at coastal sites (Lothal, Dholavira). That verdict stands. The
residue its not-understood text names: the test treated the fish family
together and used site types as published in the CISI data — a finer test,
sign by sign and with a better site classification, has not been run. A finer
test could sharpen the falsification or find the one member it does not cover;
it cannot quietly resurrect the family-level claim.

**Hypothesis (the claim's, restated at sign level).** At least one individual
fish sign is enriched at coastal/maritime sites relative to inland sites.

**Falsifier.** No fish sign with at least 30 total occurrences shows coastal
enrichment at the criterion below — in which case the partial falsification is
recorded as covering the family member by member, and the residue closes.

**Data.** The program's CISI-based corpus layer as held in the database (the
same layer the original test used, so results are comparable); site coastal
status fixed in advance from the Spec 027 Stage 0 gazetteer and published site
geography (a site is coastal/maritime if its published location is a port or
within the coastal zone — the list is frozen in the design, not adjusted per
result). Fish family membership as frozen in D-04.

**Method.** For each family member with at least 30 occurrences: coastal share
of its occurrences versus the corpus-wide coastal share of all inscriptions,
with an exact test per sign and a family-wise correction across the members
tested. Report every member's counts, not only significant ones.

**Criteria fixed in advance.** A member is ENRICHED if its coastal share
exceeds the corpus coastal share with the corrected test at the 5% level and
the share ratio is at least 1.5. Residue outcome: ENRICHED member found (the
claim's record gains a dated note naming the member — the family verdict does
not change, because the family-level test already failed), or NO MEMBER
ENRICHED (residue closed), or TOO THIN (fewer than two members clear the
occurrence floor — counts stated).

**Controls and named confounders.** Excavation-size bias: big coastal sites
produce more of everything — the comparison is against the corpus-wide coastal
share, not against raw counts, and a site-size-matched sensitivity (each
coastal site's fish share versus its own total) is reported alongside. Site
classification disputes: any site whose coastal status is contested in the
literature is listed, and the test is rerun without it as a stated sensitivity.

**What it would NOT establish.** What the fish sign meant, even if a member is
enriched. Enrichment at ports is consistent with several stories; the claim's
specific guild-badge story remains untested by any distributional test.

---

## D-05 — Hunt's three parts: pattern, or meanings?

- **Claim:** `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`
  (IN QUESTION — partially supported for position only: 805 of 2,267 longer
  inscriptions follow the opening-middle-ending structure, 35.5% against 0.6%
  expected by chance; the test's own verdict states the pattern is "consistent
  with both Hunt model and Dravidian suffix model" and cannot distinguish them
  without visual sign classification).
- **Feasibility:** RUNNABLE-TODAY (uses the shared published-identification
  classification; see below).

**The question in plain words.** Inscriptions do fall into a three-part
positional pattern. Hunt says the parts *mean* things: identity/goods first,
action in the middle, cycles/jurisdiction last. The rival account says the
pattern is just grammar — in particular that the closing part is word endings.
Can the two accounts be told apart? Yes, if the signs are classified by what
they depict: Hunt's account predicts the *depicted kinds* of signs sort into
the parts (for example, cycle signs at the end); the grammar account predicts
position is driven by the sign's role in the sequence, whatever it depicts.

**Hypothesis.** Under a classification of signs by depicted kind, taken from
published sign lists and frozen in advance, the signs Hunt's model assigns to
each part are enriched in that part beyond what position alone predicts — and
the closing part's membership is better predicted by depicted kind (cycle/sky
and jurisdiction signs) than by the grammar model's predictor (behaving as a
word ending, measured by D-08's frozen closing-sign behaviour).

**Falsifier.** The hypothesis fails if depicted kind adds no predictive power
over position class alone, or if the closing part is predicted as well or
better by word-ending behaviour than by depicted kind.

**Data.** The shared classification asset: sign-by-sign depicted-kind labels
(animal, sky/cycle, object/goods, human, other) entered from published
identifications — the CISI volumes (Vol. 1 and Vol. 2 are held digitally and
complete) and Parpola's published sign identifications — each label carrying
its source. The positional framework and corpus are the program's existing
ones (the hunt_tripartite_test data and the strict corpus).

**Method.** Fit two pre-registered predictive models of each inscription's
part-membership (opening/middle/closing sign classes as recorded): model P
uses position behaviour only; model PH adds depicted kind. Compare out-of-sample
fit (pre-registered split: odd/even inscription IDs) by a fixed margin.
Separately, test the closing class head-on: for each closing-strong sign,
score (a) suffix-like behaviour — the rate at which it follows many different
signs as a final element (the grammar signature) and (b) depicted-kind
membership in the cycle/sky class. The two scores' agreement with closing
membership is compared directly.

**Criteria fixed in advance.** DISCRIMINATED FOR HUNT: model PH beats model P
by the fixed fit margin **and** depicted kind predicts closing membership
better than suffix behaviour does. DISCRIMINATED FOR THE GRAMMAR ACCOUNT:
suffix behaviour predicts closing membership at least as well as depicted kind
and PH adds less than the margin. NOT DISCRIMINATED: anything else — which
leaves the claim exactly as it stands, with the attempt recorded. (Fit margins
are set at freeze from the recorded Phase-43 effect sizes, before the
classification is joined to the corpus.)

**Controls and named confounders.** Classification circularity: the labels come
from published identifications made for other purposes, entered by a worker who
does not see the positional results; labels are frozen before the join.
Frequency: rare depicted kinds are pooled as "other" by a rule fixed in
advance. The pattern's weakness as evidence (many record systems develop fixed
field orders): the design does not test whether a pattern exists — that is
settled — only which account of it fits better.

**What it would move.** The claim from IN QUESTION to discriminated-for /
discriminated-against / still-undiscriminated — the first evidence addressed
to the claim's actual content (the meanings) rather than its positional shadow.

**What it would NOT establish.** That Hunt's specific glosses (this sign =
guild, that part = tribute) are right. Even a clean win for depicted kind
shows the parts sort by kind; the meanings of the kinds remain readings, not
measurements.

---

## D-06 — Are the opening signs the animal signs?

- **Claim:** `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
  (IN QUESTION — the record's own words: "40 INITIAL_STRONG signs identified;
  faunal-initial enrichment not yet sign-classified [STRUCTURAL SUPPORT ONLY]").
- **Feasibility:** RUNNABLE-TODAY (same shared classification as D-05).

**The question in plain words.** Forty signs strongly prefer the opening of
inscriptions. Hunt's claim says the opening signs are the animal signs (fish,
unicorn, buffalo, rhinoceros, tiger, elephant). Nobody has ever checked
whether the forty are the animals. Now they can be.

**Hypothesis.** Animal signs are enriched among the opening-strong signs
relative to their share of the sign inventory.

**Falsifier.** The hypothesis fails — and the claim's animal half is recorded
as not supported — if animal signs appear among the opening-strong set at or
below the rate the inventory share predicts, under the criterion below. This
is the test the claim's own record states ("animal signs enriched in opening
position above a random baseline"); the design runs it exactly.

**Data.** The 40 opening-strong signs from the recorded Phase-43 result; the
shared published-identification classification (D-05) marking the animal
signs — fish, unicorn, buffalo, rhinoceros, tiger, elephant, and any further
faunal signs the published sources identify, the list frozen before the join.

**Method.** One join, one test: the share of animal signs among the 40
opening-strong signs versus the animal share of all signs with at least 30
occurrences, exact test, counts published in full. A second pre-registered
arm reverses the direction: among all animal signs with at least 30
occurrences, the share that are opening-strong, versus the same share for
non-animal signs.

**Criteria fixed in advance.** SUPPORTED: enrichment ratio at least 1.5 with
the exact test at the 5% level in the primary arm. NOT SUPPORTED: ratio at or
below 1.0, or the test cannot reject equality. INCONCLUSIVE: ratio between
1.0 and 1.5, or the arms disagree. Whatever lands, the claim's record gains
the second half it has always lacked; the positional half is not re-run.

**Controls and named confounders.** Frequency (common signs are more often
classifiable as position-strong): the comparison population is restricted to
signs with at least 30 occurrences in both arms. Classification disputes:
signs whose animal status is contested in the published sources are named,
and the test is rerun without them as a stated sensitivity. The unicorn
problem (the commonest "animal" is a composite creature whose identification
is conventional): it is included as published sources classify it, and a
sensitivity without it is pre-registered.

**What it would move.** The claim from IN QUESTION to a two-half verdict:
positional half supported (already), animal half supported / not supported /
inconclusive (new).

**What it would NOT establish.** That animal signs marked identity, guild, or
goods. Position plus depiction is still not meaning.

---

## D-09 — Roif's ledger thesis: the distribution test its own record proposes

- **Claim:** `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
  (UNTESTED — Phase-104 found its stated test could not run: the corpus
  carries site names but no classification of sites by function).
- **Feasibility:** RUNNABLE-TODAY (the design builds the missing classification
  as cited data in step 1; step 2 is the test).

**The question in plain words.** Roif's thesis bundles three claims: the script
is an economic ledger; it served guild authority; it was influenced by
Akkadian practice. Only the first makes a prediction this program can test:
if the signs are a ledger notation for administration and trade, they should
cluster at administrative, trade, and gateway sites rather than domestic or
purely ritual ones. This design tests that component only, and says so. The
guild-authority and Akkadian-influence components are declared **not tested
by this design** — the program holds no contact evidence for the second, and
the first is an interpretation layered on the distribution, not a separate
measurement.

**Hypothesis.** Inscription density and the ledger-candidate sign classes
concentrate at sites classed as administrative/trade/gateway, beyond what
site size predicts.

**Falsifier.** The hypothesis fails if, with site size controlled, the
administrative/trade/gateway class shows no excess over domestic/ritual
sites — the outcome the claim's own record states as its failure condition.

**Data.** Step 1 (the shared site-function asset): every site in the Spec 027
Stage 0 gazetteer (30 clusters) classed by primary function from the published
excavation literature, two independent published sources per site where they
exist; a site enters the test only if both sources agree on its class, and
disagreed sites are listed and excluded by rule, not by judgement after the
fact. Classes: gateway/border, administrative, port/trade, domestic,
ritual, mixed/unknown. Step 2 data: the program's corpus layers with site
attribution, as held.

**Method.** With the classification frozen: compare inscription counts and
sign-class shares across site classes, controlling for excavated volume
proxied by total inscription count per site (the size control is the total
itself — the test is about *shares*, not counts). Pre-registered measures:
(a) each site class's share of all inscriptions versus its share of sites;
(b) the same for the sign classes Roif's text names as ledger notation, the
list extracted from the source document and frozen before counting.

**Criteria fixed in advance.** SUPPORTED (bounded to the distribution
component): administrative/trade/gateway sites carry a share of inscriptions
at least 1.5 times their share of testable sites, with the permutation test
(site labels shuffled, 9,999 times) at the 5% level, and the named
ledger-sign classes show the same direction. NOT SUPPORTED: the ratio at or
below 1.0 or the permutation test does not reject. INCONCLUSIVE: between,
or fewer than 12 sites survive the two-source agreement rule (the
classification then is the finding, reported with its disagreements).

**Controls and named confounders.** Excavation and publication bias (big
famous sites are more dug and more published): the shares-not-counts design
and the size control address volume, and a sensitivity restricted to the five
largest sites' classes is reported. Classification contestability: the
two-source rule, plus a rerun under each source alone. Circularity: site
classes come from excavation literature, never from inscription content.

**What it would move.** The claim from UNTESTED to checked for its
distribution component (supported / not supported / inconclusive), with the
other two components explicitly carried as untested sub-claims — the
decomposition the framework requires instead of one verdict over a bundle.

**What it would NOT establish.** That any inscription is a ledger entry, that
guilds existed as Roif describes, or anything about Akkadian influence.

---

## D-10 — The arrow sign: border marker, or city sign?

- **Claim:** `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`
  (UNTESTED — same missing classification as D-09; the counts that exist lean
  the other way: Mahadevan sign 391 is counted at Mohenjo-daro 75, Harappa 52,
  Dholavira 16, Lothal 14, Kalibangan 10 — mostly the great cities).
- **Feasibility:** RUNNABLE-TODAY (uses D-09's frozen site-function asset).

**The question in plain words.** The claim says the arrow sign marks border
enforcement — a sign for checkpoints. Its own proposed test: the sign should
cluster at gateway and border sites. The counts already on the record sit in
the biggest cities. Is that just because the big cities have more of
everything, or is the sign genuinely a city sign?

**Hypothesis (the claim's).** Relative to each site's total inscriptions, the
arrow sign's share is higher at gateway/border sites than elsewhere.

**Falsifier.** The hypothesis fails if the arrow sign's share at
gateway/border sites is at or below its share at the great-city sites once
totals are controlled — the comparison the claim's own falsifier states.

**Data.** The frozen site-function classification (D-09 step 1); sign 391
counts per site from the program's corpus layers (the recorded counts above
are the starting census, re-derived from the database at run time under H16);
site totals as the exposure control. A rival explanation is measured in the
same run: the program's role data treats sign 391 as a possible case-ending
marker — if so, its distribution should track text length and corpus size,
not site function. Both predictions are scored.

**Method.** Per-site arrow-sign share (arrow occurrences / site inscriptions),
compared across site classes with an exact test and a permutation control;
the same shares regressed on site size alone to test the case-ending rival
(if size explains the shares and class adds nothing, the rival wins).

**Criteria fixed in advance.** SUPPORTED: gateway/border share exceeds the
great-city share by a ratio of at least 1.5 at the 5% level, and site class
adds predictive power beyond size. NOT SUPPORTED: ratio at or below 1.0, or
size alone explains the pattern. INCONCLUSIVE: between, or fewer than 3
gateway/border sites carry the sign at all (counts stated).

**Controls and named confounders.** Small counts at small sites (exact tests,
floors stated); classification disputes (D-09's two-source rule carries
over); the descriptive city-lean already on the record (stated in the design
so the result, whichever way it lands, is read against it honestly).

**What it would move.** The claim from UNTESTED to checked.

**What it would NOT establish.** That the sign *meant* border enforcement —
a distribution can fit the story without proving the gloss — nor that its
possible case-ending role is false; both roles could coexist, and the design
reports the two scores separately rather than forcing a choice.

---

## D-11 — The horned deity at Kalibangan: a context test that needs context data

- **Claim:** `indus_valley_script_deciphered_from_myth_65ff0a26_manual_004`
  (UNTESTED — Phase-104: the claim names what it needs, site metadata with a
  fire-altar classification, and no such dataset exists in the repository).
- **Feasibility:** BLOCKED.

**The question in plain words.** The claim ties one sign (the horned deity)
to fire-altar ritual at Kalibangan, the site known for its fire altars. Its
test: the sign should concentrate in fire-altar structures rather than
domestic contexts. That test needs to know, for each Kalibangan find, what
kind of structure it came from. The corpus carries site names only — no
structure contexts at all.

**Why it is blocked, precisely.** The missing dataset is not a clerical gap.
Fire-altar attribution is an archaeological judgement that varies between
reports, so the dataset must be built from the published Kalibangan
excavation reports (the ASI reporting tradition for Kalibangan I/II), with
each context's classification carrying its report citation and disagreements
recorded rather than averaged away. That build is a cited-data intake act
through the Phase-130 pack, and it has not been done.

**The design, ready to run when the data exists.** Hypothesis: the horned-deity
sign's occurrences at Kalibangan concentrate in contexts classed as
fire-altar/ritual over domestic contexts, relative to all signs' distribution
across the same contexts. Falsifier: its context distribution matches the
corpus-wide one, or leans domestic. Method: exact test on the two-way table
(this sign / all other signs × ritual / domestic contexts), with contexts
whose classification is disputed between reports excluded by rule and listed.
Criteria fixed in advance: SUPPORTED at a concentration ratio of 1.5 or more
at the 5% level with at least 10 occurrences of the sign in classified
contexts; NOT SUPPORTED at ratio 1.0 or below; INCONCLUSIVE between, or below
the occurrence floor — in which case the honest verdict is that one site's
surviving record cannot carry this claim, stated as such. What it would NOT
establish even if supported: the deity's identity or the ritual's content —
a context association is not a translation. Unblocking act: extraction of
the Kalibangan context dataset from the published reports as cited data
(Phase-130 intake), with per-context citations and a stated dispute rule.

---

## D-12 — Hunt's civic order: a comparison that needs find contexts

- **Claim:** `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002`
  (UNTESTED — marked on its own record as only indirectly testable; Phase-104
  found the comparison cannot run: no classification of contexts as palatial,
  royal, civic, or infrastructural exists in the repository).
- **Feasibility:** BLOCKED.

**The question in plain words.** Hunt reads the inscriptions as the paperwork
of a shared civic order, not of kings. The claim's own test is comparative:
sign distributions should track civic and infrastructure contexts more than
palatial or royal ones. That needs inscriptions labelled by the kind of place
they were found in. The program's data has sites, not contexts.

**Why it is blocked, precisely.** Two gaps, not one. (1) The find-context
dataset (per-inscription context class from the excavation literature) does
not exist in the repository. (2) A prior question the design must state
honestly: "palatial/royal context" may be an empty class in the Indus record —
the absence of identified palaces is itself part of Hunt's argument — so the
comparison risks testing against a category with no members. The design
handles this in advance rather than discovering it mid-run.

**The design, ready to run when the data exists.** Step 0 (classification
census): build the find-context classification from published excavation
reports as cited data (Phase-130 intake), classes: palatial/royal, civic/
administrative, infrastructure, domestic, ritual, workshop/trade, unknown.
If the palatial/royal class has zero classifiable inscriptions, the design
closes at step 0 with that census as its finding — itself a relevant,
reportable fact about the claim's testability, recorded as NOT-YET-TESTABLE
rather than as support for Hunt (an empty rival class is not evidence the
civic reading is right; it is evidence the comparison cannot be run).
Hypothesis (if the census passes): inscriptions' sign-class profiles differ
by context class, with civic/infrastructure contexts carrying the shared,
cross-site profile the claim predicts, and palatial contexts (if any)
carrying a distinct one. Falsifier: context class explains no more of the
profile variation than chance (permutation test on context labels), or
palatial contexts are indistinguishable from civic ones. Criteria and margins
are set at freeze once the census fixes the class sizes — fixing numeric
margins now, before the classes' sizes are known, would be inventing
precision; the *form* of the criterion (permutation test at the 5% level;
distinctness measured by the same Cramér's V framework as the site studies,
with 0.10 as the practical margin by precedent) is fixed here.
What it would NOT establish: the social reading itself. Context statistics
can be consistent with a civic order without showing anyone intended one.
Unblocking act: the find-context dataset (shared in kind with D-11's need,
but at context level across sites rather than structure level at one site).

---

## D-13 — Sky signs at the ends of texts

- **Claim:** `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
  (UNTESTED — Phase-104, RULE-CLASS: the claim's falsifier requires a defined
  class of celestial signs, and no such classification exists in the
  repository's data; this is the one part of Hunt's scheme where not even the
  positional shadow has been measured).
- **Feasibility:** RUNNABLE-TODAY (the shared published-identification
  classification from D-05 supplies the celestial class).

**The question in plain words.** Hunt's closing part should be sky signs —
sun, star, moon — standing for cycles and calendars. Which signs are sky
signs is a visual judgement; the published sign lists make it. With that
class defined, does it actually gather at the ends of inscriptions?

**Hypothesis.** Signs in the celestial class are enriched in text-final
position relative to their overall frequency.

**Falsifier.** The hypothesis fails if the celestial class's final-position
rate is at or below the corpus-wide final-position rate for signs of
comparable frequency — the test the claim's falsifier states (terminal
enrichment for the class).

**Data.** The celestial class from the shared classification (D-05): signs
the published identifications describe as sun, star, moon, or celestial
bodies, the list frozen before counting, each entry cited. Corpus and
positional framework as in D-06/D-08.

**Method.** Class-level test: pooled final-position rate of celestial-class
signs (with at least 30 class occurrences in total and per-sign counts
reported) versus the rate for a frequency-matched comparison class (all
non-celestial signs in the same frequency band). Per-sign results reported
alongside the pooled one, so one frequent sign cannot carry the class
silently.

**Criteria fixed in advance.** SUPPORTED: pooled enrichment ratio at least
1.5 at the 5% level, and at least half the class's occurrences come from
signs individually above the corpus rate. NOT SUPPORTED: ratio at or below
1.0. INCONCLUSIVE: between, or the class totals fewer than 30 occurrences
(the class then is the finding: too small to test, stated plainly).

**Controls and named confounders.** Classification discretion (which signs
count as "sky" is the whole ballgame): published-source citation per sign,
a named sensitivity with borderline signs removed, and the list frozen
before any positional number is computed. Frequency confounding: the matched
comparison class. Meaning creep: a positive result shows sky signs cluster
at endings — it does not show they marked calendars, and the verdict wording
says so.

**What it would move.** The claim from UNTESTED to checked — completing the
positional measurement of Hunt's scheme (openings D-06, middles/pattern D-05,
endings here).

**What it would NOT establish.** Scheduling, ritual calendars, or any cycle
content. Position is not meaning; this design measures position.

---

## D-14 — Hunt's Translation Atlas: the test waits for the atlas

- **Claim:** `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_005`
  (UNTESTED — Phase-104, RULE-REF: the 24 cluster definitions are not in the
  repository; the program has clusterings of its own, but testing them would
  test a different claim).
- **Feasibility:** BLOCKED.

**The question in plain words.** Hunt groups the signs into 24 semantic
clusters — a "Translation Atlas" — whose members should behave alike: each
cluster should show its own distinct pattern of positions and neighbours.
The claim is crisp and falsifiable. Its object is simply absent: the
membership lists exist in Hunt's published work, not in this repository.

**The design, ready to run on acquisition.** Data precondition: the 24
cluster definitions extracted from the source publication and entered as
cited data with provenance (Phase-130 intake), each sign's cluster
assignment carrying its page-level citation. Hypothesis: clusters have
distinct behavioural profiles. Falsifier (the claim's own terms): if two
clusters behave identically, the grouping fails. Method fixed here: for
each cluster, build its profile — position distribution (initial/medial/
final shares) and neighbour distribution (the signs it most often stands
beside) — over the strict corpus; measure pairwise profile distances;
compare against 999 random reassignments of signs to same-sized clusters.
Criteria fixed in advance: the atlas is SUPPORTED if the real clusters'
profiles are more distinct than the 95th percentile of the random
reassignments **and** no pair of clusters is closer than the closest pair
arising in the median random reassignment; NOT SUPPORTED if distinctness
falls inside the random range or a cluster pair is effectively identical;
INCONCLUSIVE between. What it would NOT establish: that the clusters'
*meanings* are as Hunt glosses them — behavioural distinctness tests the
grouping, not the translations. Unblocking act: acquisition and cited-data
entry of the atlas definitions from the source publication. No contact with
any person is required or proposed; this is a publication-intake act.
