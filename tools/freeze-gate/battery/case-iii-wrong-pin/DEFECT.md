# Battery case (iii) — a pinned quantity arithmetically wrong against its own cited source

**Artifacts:** `claims.json` (the planted register) and
`SOURCE.md` (the source it cites), both in this directory.

**The defect, in plain words.** The register pins a population
total of **52** signs. Its own cited source lists four counts —
12, 9, 14, 12 — which sum to **47**. Every derived pin inherits
the error: the pinned mean is 13.0 (the source's mean is 11.75)
and M-003's pinned share is 0.269 (the source's share is
14/47 ≈ 0.298). The claims are well-formed, falsifiable, and
neatly evidenced — and false, in a way ten seconds of arithmetic
exposes. This is the defect class the C2 spot-check exists for:
quantities a freeze pins without anyone re-adding the column.

**What the battery asks of the evaluator.** The evaluator is
not an arithmetic engine and is not expected to re-add the
source's column; if it passes this register silently, the
battery records exactly that, as a named blind spot of the
evaluator — and records C2 (independent recomputation) as the
component that carries this class. If it does flag the pin,
that is recorded too, as caught.
