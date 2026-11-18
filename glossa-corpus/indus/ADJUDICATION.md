# ADJUDICATION — external review findings against Indus paper v11

Pass: adjudication only. Nothing in the paper was edited. Every number below was
read from the record named beside it or recomputed in the foreground from a
hash-verified input.

**Materials.** Paper text: `pierson_2026_indus_decipherment_v11_final.tex` in this
directory. Records: fresh clone of AXIOVEX/glossa-lab at
`~/glossa-work/paper-adjudication/repo` on the mini-server, tip
`bd921ec99828ce06e635865b710ce3ee2c152b85` (the tip required by the charge).
The Holdat corpus CSV is not carried in git; the copy used is the live
checkout's restored file of record, SHA-256
`62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
(`corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`) — the
input file both generating scripts name. The canonical-export recompute used
the VM custody copy of `firestore_indusarrays_full.jsonl`, SHA-256
`073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578`, which is
the intake pin of record (PR #393); it was loaded through the repository's own
V3 loader, whose identity check passed and whose census reproduced the
Spec 095 Stage 1 record exactly (see Finding 1c).

---

## Finding 1 — Terminal rates vs bigrams (claimed blocker)

**Verdict: REAL — and stronger than the brief states.** The conflict is not a
conflation of two record-defined measures. The bigram counts and every
positional count in the records reproduce exactly, in one convention, from the
paper's own corpus snapshot — and in that same convention the §3.3 percentages
are not 96%/94% but 12.0%/19.1%. No record in the repository generates the
printed percentages under any measure I could identify.

### 1(a) The §3.3 table's M342/M176 rows

The printed measure is "% of them inscription-final" over token counts
(M342: 584 tokens, 96%; M176: 356 tokens, 94%). Records that compute position
on this corpus:

- `backend/reports/phase133_resolution.json` (SHA-256 `8b6d9ba3…`), §133a_v11
  dual-function signs: M342 — initial_count 12, terminal_count 70, total 584,
  initial_pct 0.021, verdict "PRIMARILY TERMINAL: 2.1% initial rate is
  noise/boustrophedon"; M176 — initial_count 13, terminal_count 68, total 356,
  initial_pct 0.037, verdict "PRIMARILY TERMINAL". Note what this record's
  verdict rests on: the low *initial* rate alone. Its own counts give medial
  remainders of 502 (M342) and 275 (M176) that the verdict text does not
  mention.
- `backend/reports/phase155_phonotactic_sibilant.json` (SHA-256 `c71cebad…`)
  and its script: t_rate = (seals of length > 1 ending in the sign) / (total
  tokens). M342 and M176 do not appear in its terminal list at all — see
  Finding 2.
- The anchor-model package's positional-profiles output is not in the public
  release (its README: "REQUIRES_RESTRICTED_CORPUS"), and its public check
  confirms "M342 terminal" from basis *keywords*, not from a computed share.

The 96% figure's only traceable ancestor is the paper's own preprint lineage:
`research/indus/pierson_2026_indus_preprint.md` carries the table row
"Terminal case suffix (584 tokens, 96% terminal)". No generating record,
script output, or profile table in the repository produces 96% (or 94%) for
these signs on this corpus.

### 1(b) The formula bigram table's source

- Generating record: `backend/scripts/phase142_collocate_network.py` →
  `backend/reports/phase142_collocate_network.json` (SHA-256 `9ed1cb11…`);
  supplemental file `research/indus/supplemental/formula_bigram_table.csv`
  (SHA-256 `bdb22c65…`).
- The script loads the same Holdat CSV, builds each inscription's sequence in
  the file's position order (verified: file order equals the `position`
  column ascending for all 1,670 forms), and counts adjacent pairs
  (seq[i], seq[i+1]) in that order — the order the paper calls reading order.
- "122" counts pair **occurrences**, not seals: the CSV row is
  `M342·M176, M342, M176, ay/ā, an/aṇ, 122, 2.432`. The 122 occurrences span
  **120 distinct seals**. The paper's §3.7 headline sentence says "appears on
  122 seals"; its own worked example in the same section says "M342·M176
  occurs 122 times". The record supports occurrences. (M176·M099: 74
  occurrences on 74 seals; M267·M099: 84 on 82; M099·M342: 81 on 80.)

### 1(c) Recompute from the one corpus snapshot (Holdat, position order)

Census reproduces exactly: 1,670 inscriptions, 7,002 tokens, 390 distinct
signs, 5,332 bigram tokens, 2,647 distinct bigrams; PMI for M342·M176
recomputes to 2.432 (printed 2.43).

| Sign | Tokens | First | Medial | Final (count) | Final share | Final on seals | Outgoing pair |
|---|---|---|---|---|---|---|---|
| M342 | 584 | 12 (2.1%) | 502 (85.9%) | 70 | **12.0%** | 70 | M342·M176 = 122 occ / 120 seals |
| M176 | 356 | 13 (3.7%) | 275 (77.2%) | 68 | **19.1%** | 68 | M176·M099 = 74 occ / 74 seals |

The reviewer's ceilings are arithmetically correct at the occurrence level
((584−122)/584 = 79.11%; (356−74)/356 = 79.21%): each outgoing occurrence is a
non-final occurrence of the first sign. The recomputed final shares sit far
below those ceilings, so the printed 96%/94% fail by a wide margin, not a
rounding margin. Reversing the direction convention does not rescue them: in
the reversed convention the final shares are the first-position shares,
2.1%/3.7%, and the printed bigram direction (M342·M176, not M176·M342) fixes
the convention the paper itself uses. The phase133 counts (12/70, 13/68) match
this recompute to the unit, so the records agree with each other and with the
corpus; the §3.3 percentages are the only unsupported element.

**Canonical-export recompute (as charged).** Through the V3 loader
(`backend/glossa_lab/data/indus_corpus_v3.py`), identity-verified as above;
loader census: 3,916 records / 2,665 dockeys / 3,137 sequences / 12,494 sign
instances — exactly the Spec 095 Stage 1 record's census and canonical export
pin `e90fd7ce41121529887b51dda11640741c23db94a224e946588628802503c659` (the
loader's identity check passed on this file; I did not independently
re-derive the pin's digest serialization). This is the RMRL / Mahadevan
concordance layer — a **different population** from the paper's Holdat corpus
(1,670 seals / 7,002 tokens) — so it cannot settle the §3.3 figures; its own
numbers, in stored sequence order: sign 342 — 1,318 tokens, 927 final
(70.3%); sign 176 — 344 tokens, 307 final (89.2%); 342→176 = 179 occurrences
/ 179 sequences; 176→99 = 1 occurrence. Internally consistent there too, and
neither 96% nor 94% appears.

**Corrective action the record supports.** Replace the two §3.3 basis
figures with the record values: M342 — "584 tokens, 70 of them
inscription-final (12.0%)"; M176 — "356 tokens, 68 of them inscription-final
(19.1%)". Dependent text the same records falsify: §3.3's note that M176's
94% figure "does not by itself meet §2.2's terminal-marker criterion (>95%)"
(at 19.1% the figure is nowhere near the criterion; the note's second half —
HIGH rests on the audit's recorded evidence pair — is the part the record
supports); §3.2's description of M342 as "most frequent terminal" (by final
count M342 ends 70 seals; M233 and M367 each end 92 — M342's record
distinction is most frequent sign overall, 584 tokens); §3.7's "122 seals" →
"122 occurrences on 120 seals". Whether the grammatical labels ("candidate
case suffix") survive on a 12.0%/19.1% final share with an 85.9%/77.2% medial
share is an interpretation decision for the author; the records support the
numbers, not a replacement interpretation, and none is offered here.

---

## Finding 2 — Terminal list omission (claimed blocker)

**Verdict: NOT REAL as a defect of §3.18.** The seven-sign list is exactly
its record's output under the record's own rule. The apparent contradiction
is manufactured entirely by Finding 1's unsupported §3.3 percentages.

**The record.** `backend/reports/phase155_phonotactic_sibilant.json`
(2026-05-19; SHA-256 `c71cebad…`), generated by
`backend/scripts/phase155_phonotactic_sibilant.py`. Its eligibility rule,
from the script: the sign is in the H+M set of `INDUS_FINAL_ANCHORS.json`
(the snapshot of that date), and t_rate ≥ 0.50, where t_rate = tc / freq with
tc = the count of inscriptions of length > 1 whose last sign (position order)
is the sign, and freq = the sign's total token count, both on the Holdat
load. There is **no further filter** — no frequency cap, no working-set
restriction; the seven signs' frequencies (62–171) are incidental.

**M342/M176 in that record's measure** (recomputed from the same input; the
record lists only signs passing the filter): M342 t_rate = 70/584 = **0.120**;
M176 t_rate = 68/356 = **0.191**. Both fall below 0.50, so their exclusion
follows the record's own rule mechanically. As a check on the measure, I
re-derived all seven listed signs' t_rates from the CSV and reproduced the
record to its printed three decimals (M233 0.538, M051 0.515, M065 0.545,
M305 0.976, M125 0.561, M249 0.959, M220 0.984), and the full H+M set meeting
the threshold under the current anchors file is the same seven signs.

**Corrective action the record supports.** None to §3.18's list, its seven,
or the 4/7 result — they stand as the record's output. The repair belongs to
§3.3 (Finding 1). One presentational gap is real: §3.18 never defines t_rate
for the reader, which is what allows §3.3's unlike percentages to read as the
same quantity; a single clause stating the record's definition (share of a
sign's tokens that are the last sign of a multi-sign inscription, on the
Holdat corpus) closes it.

---

## Finding 3 — Atlas population gap (claimed minor)

**Verdict: REAL, exactly as graded (minor; no outcome changes).** The record
accounts for the missing sign and its two occurrences by name; the paper's
§3.31.1 does not mention it.

**The record.** Spec 075 (depicted-kind endings atlas), `spec.md` §4.3
"Token 999 — the named exclusion (design R3)"; `step0-record.md` Gate 0.4
(SHA-256 `f19c1fc4…`); `outcome.md` (SHA-256 `006b3844…`).

- The missing sign is **token 999** — "the one primary-population sign with
  no published identity" (Spec 073's NO PUBLISHED IDENTITY schedule,
  `specs/073-keying-surface-repair/registry-v2/no-published-identity.json`).
- Disposition, in the record's words: a named exclusion "from every class and
  every comparison class", excluded in advance by name; "2 primary rows, 2
  occurrences — counted, never keyed or classed" (step0-record Gate 0.4).
- Arithmetic: identified kinds 423 signs / 11,322 occurrences + unidentified
  133 / 481 = 556 signs / 11,803 occurrences; + token 999 (1 sign, 2
  occurrences) = the stated 557 / 11,805. ✓
- Denominators: token 999's 2 occurrences sit inside the population total and
  therefore inside the corpus-wide final-rate denominator the paper prints
  (0.2579 = 3,045 / 11,805). It is a member of no kind class and no
  frequency-matched comparison class, so it enters **no** per-kind rate,
  ratio, or Fisher test. (Whether either of its rows ends in token 999 —
  contributing to the 3,045 final count — is not broken out in the record;
  the maximum possible effect is 2 rows, and no printed per-kind result can
  move.)

**Corrective action the record supports.** Add the population-accounting
sentence to §3.31.1 naming token 999, its 2 occurrences, and its
counted-but-never-keyed-or-classed disposition — the record's own wording
supplies it. No printed number changes.

---

## Finding 4 — The 43-pair estimate

**Verdict: REAL.** The subtraction exists in the record as the adversarial
recheck's assertion, and the paper reports it attributed to that recheck —
but no record supports it as an estimate of a genuine count, and the
recheck's own numbers cannot support it, because the expected-false-positive
figure belongs to a different selection rule from the one that produced the
63.

**The records.**

- Iconographic cross-encoding record: `backend/reports/phase143_iconographic_formula.json`
  (2026-05-19; SHA-256 `92ffe640…`), script
  `backend/scripts/phase143_iconographic_formula.py`. Its own numbers:
  **394** pairs tested (attested, filter-passing INITIAL-sign × iconography
  pairs); **63** enriched, selected by the script's criterion — single-cell
  contribution χ² = (O−E)²/E **> 1.0** with observed > expected (script:
  `enriched = [c for c in chi2_contributions if c["direction"]=="enriched"
  and c["chi2"]>1.0]`; record key finding: "63 enriched INITIAL × iconography
  pairs (χ²>1.0)"). **14** pairs stand at or above ≈14.7 on that statistic —
  verified against the record's top-20 values: the 14th value is 15.031 and
  the 15th is 8.964, so exactly 14 of the 63 reach the threshold.
- Adversarial recheck: `backend/reports/phase149_adversarial_challenge.json`
  (2026-05-19; SHA-256 `d0938ba3…`), challenge C2. Its test_result states
  verbatim: "Expected false positives ~20 — 63 enriched means ~43 genuinely
  significant", and its caveats: "The top ~40 pairs are robust; the bottom
  ~20 are marginal." The 19.7 is 394 × 0.05 — the expected false-positive
  count for a family of valid tests each conducted at an uncorrected 5%
  level (the paper itself prints this comparison correctly in its later
  sentences).

**Why the record does not support the estimate.** The 63 were not selected
by any 5%-level test; they were selected at single-cell χ² > 1.0 (for
scale: a full 1-df χ² of 1.0 corresponds to p ≈ 0.32, and the single-cell
contribution is one term of the full statistic, not the statistic). The
expected count of false positives *under the selection actually used* is
nowhere computed in any record. Subtracting the 5%-family expectation from
the χ²>1.0-selected count therefore mixes two different selection rules, and
no record — including the recheck itself, which asserts rather than derives
it — supports "about 43" as an estimate of genuinely significant pairs. One
further record defect worth naming: phase149 C2 is internally inconsistent —
its test_result also says "All top-20 pairs (chi2 range 4.9-158.5) survive
Bonferroni", contradicting its own adversarial_test line ("Top-20
associations with chi2>14.7 (Bonferroni threshold): 14/20") and the
phase143 values; the paper's "14" follows the adversarial_test line and the
phase143 record, not that sentence.

**Corrective action the record supports.** Remove the estimate sentence and
its two glosses ("genuinely significant", "'robust' … the roughly 43",
"the remaining roughly 20 … marginal remainder"). The record-supported
summary is: of 394 attested, filter-passing pairs, 63 had a single-cell
contribution above 1.0, and 14 crossed the reported numerical threshold of
approximately 14.7; neither count estimates the number of true associations.
(The paper already states the selection criterion and the 19.7 comparison at
the right strength in the sentences around the estimate; those stand.)

---

## Finding 5 — Claim-strength items (factual grounding only, as charged)

### 5(a) Sentences characterizing the language-family conclusion

From the final .tex, verbatim:

- **Abstract:** "the evidence is consistent with a Proto-Dravidian reading
  framework under the tested assumptions, though Dravidian superiority over
  proto-Munda has not been formally quantified."
- **§4.4 (Language-family baseline):** "A formal comparison against
  Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains
  necessary before the linguistic interpretation can be treated as
  discriminative rather than merely compatible with Proto-Dravidian. For the
  record, the comparisons that do exist are mixed: a syllabic language-model
  comparison favoured Dravidian over Sanskrit on the 157-sign set (the
  falsification suite's language-model comparison), while a
  phonological-profile comparison of the HIGH anchors found Dravidian and
  Sanskrit fits equal and rated the question AMBIGUOUS (the falsification
  suite's phonological-profile comparison)."
- **§5 (tier definitions):** "Tier 2 means a probable linguistic
  interpretation — supported, not proven; Tier 3, used below, means
  speculative or provisional, requiring explicit caveats."
- **§5 (Tier 2 application):** "The candidate Proto-Dravidian readings
  (161 H+M signs; 90.96% token coverage — assignment coverage in the sense
  of §2.2: the share of tokens whose sign carries a candidate reading, not a
  share of verified readings) are Tier 2 claims supported by multiple
  tests."
- **§5 (Tier 3 application):** "…interpretations — guild-identity semantics,
  the two DEDR-backed readings for which a Munda derivation was proposed but
  not established, individual seal translations — are Tier 3 claims
  requiring expert review and explicit caveats."
- **§5 (conclusion):** "Within that limit, the evidence favours a
  Proto-Dravidian reading framework under the tested assumptions."

### 5(b) The §2.4 SA-free sentence and the strict-94 definitions — record bases

- **§2.4 sentence (verbatim):** "That is a bound, not a recomputed headline:
  the audit file does not record whether any of the 43 also meets a non-SA
  MEDIUM criterion (a positional profile or allograph support), so a true
  SA-free headline cannot be computed from the records."
- **Strict-94 definitions (verbatim):** front matter — "the program's
  current candidate set is a strict core of 94 of those readings whose
  recorded history never passed through the program's original syllabic
  language-model simulation"; §5 — "the program's October 2026 evidence
  audit, which re-graded the 94 readings of the program's strict core one by
  one".
- **Do they rest on different record bases? Yes — factually, two different
  records answering two different questions:**
  - The §2.4 statement rests on the **status-audit table**,
    `glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv` (SHA-256 `f370a690…`):
    397 rows, one per sign, with an EvidenceType column (counts verified:
    SA+DEDR = exactly 43 rows, as §2.4 states). The table records each
    sign's promotion-route evidence type; it does not record whether a sign
    independently meets a non-SA MEDIUM criterion — which is precisely the
    gap the §2.4 sentence names. The question it answers is what the 161
    headline would become if the 43 SA+DEDR signs were removed, and the
    table cannot determine that.
  - The strict 94 rests on the **provenance audit**: the Phase-108
    provenance register, `reports/phase108_provenance_register.json`
    (SHA-256 `2b04fed4…`) — 287 per-sign records with a provenance category
    and SA-in-chain components (M342 and M176, for example, are category
    GRAMMAR) — together with the Phase-109 follow-through rule recorded in
    `backend/reports/INDUS_FINAL_ANCHORS.json`'s annotation
    (`strict_sa_independent_hm`: confidence in {HIGH, MEDIUM} AND register
    category not in {SA_DERIVED, SA_CONFIRMED_ONLY} AND register
    sa_in_chain is false; recorded strict_count 94). The question it
    answers is which readings' recorded provenance never passed through SA
    at all.
  - The two are consistent: "cannot be computed" in §2.4 is a statement
    about the status-audit table's contents, not about the provenance
    register, and the paper does not itself state that distinction in §2.4.

---

## Summary

Three of the four graded findings are real. Finding 1 is real and worse than
stated: the §3.7 bigram counts and every positional record reproduce exactly
from the paper's own Holdat snapshot in one convention, and in that
convention M342/M176 end 12.0%/19.1% of their occurrences — the printed
96%/94% have no generating record anywhere in the repository and cannot be
reconciled with the corpus by any direction or measure the records define.
Finding 4 is real: the "about 43 genuinely significant" estimate is the
adversarial recheck's assertion, built by subtracting a 5%-family
false-positive expectation (19.7) from a set selected at single-cell χ² > 1.0,
and no record supports it as an estimate. Finding 3 is real and minor: the
unaccounted sign is token 999 (2 occurrences), a named, counted exclusion in
the Spec 075 record that §3.31.1 never mentions, entering no per-kind result.
Finding 2 is not real as charged: §3.18's seven-sign list is exactly its
record's output — in the comparison record's measure M342 and M176 score
0.120 and 0.191, below its 0.50 rule, so nothing was omitted; the appearance
of a contradiction is produced wholly by Finding 1's unsupported §3.3
figures. Finding 5 is reported without verdict as charged: the "favours" /
"probable" / Tier-2 sentences stand as quoted, and the §2.4 SA-free sentence
and the strict-94 core do rest on different record bases — the status-audit
table and the Phase-108 provenance register respectively — which answer
different questions and do not contradict each other.
