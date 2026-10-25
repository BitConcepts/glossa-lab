# Battery case (iv) — evidence citations that do not support their claims

**Artifact:** `claims.json` in this directory — a planted
register. Both citations point at real records in this repo.

**The defect, in plain words.** Each claim cites a genuine,
executed record — and states the opposite of what that record
says. FB4-C01 claims Asset A v2 contains 12 celestial
(`sky_cycle`) signs, citing Spec 073's outcome, which states
the class is **0**. FB4-C02 claims Spec 074 found opening-strong
signs predominantly animal, citing Spec 074's outcome, whose
verdict was **NOT SUPPORTED** (2 animal signs of 31). The
citations resolve; the files exist; nothing about the register's
form is wrong. Only reading the cited text against the claim
exposes it — which is precisely the step the gate, as operated
with evidence verification off, never performs. This is the
defect class the C3 sample (evidence verification switched on,
with a verifier who reads the cited text) exists for.

**What the battery asks of the evaluator.** The battery runs
the evaluator twice on this case: in the freeze configuration
(lenient load, evidence verification off) and with evidence
verification on. If neither run flags the unsupported citations
with a correctness finding, the battery records a named blind
spot: the evaluator verifies that citations resolve, not that
they support — and C3's human verification step is the
component that carries this class. If a run does flag them,
that is recorded as caught, with the finding quoted.
