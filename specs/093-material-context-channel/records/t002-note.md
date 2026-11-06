# T002 — AEE validation of the C093 draft bundle (2026-11-05)

The bundle was validated with the pinned assessor in the
CI-faithful venv (`glossa-ci`, aee 1.5.3), run from the
package directory — the Spec 091/092 T002 pattern.

Command (verbatim):

```
~/workspace/venvs/glossa-ci/bin/aee validate aee-claims.json
```

Validate printed `valid: 14 claim(s) in aee-claims.json`
and exited 0.

Bundle generation: `aee-claims.json` was generated from
`claims.md` by script (statement + "does not establish"
folded into `text`, falsifier as the single falsification
test, whitespace collapsed, one asserted package evidence
entry per claim — the Spec 088/089/092 normalization). Set
identity verified mechanically: the 14 ids in
`aee-claims.json` equal the 14 ids in `claims.md`, in order
(C093-1..C093-14); every claim carries exactly one
falsifier and its folded does-not-establish line.

Scope of this reading: validation is a form check on the
draft bundle. No `aee assess` was run at drafting; the
adoption assessment is Stage 0's own act (T003), and its
outcome will be recorded verbatim there. Nothing in this
note is a claim about the claims' truth.
