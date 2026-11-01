# G44-I validation run — record (2026-10-26)

**Outcome: HALTED BEFORE IMPLANTATION — the run was not built. No gate ran, no leg ran, and no instrument verdict is issued. This is a design-feasibility halt at ledger construction (a draft §4.3 design-record event), NOT an INCOMPLETE — IMPLANTATION DEFECT under draft §6, and it triggers none of the draft's kill criteria: KI-1 requires gate failures on implantation mechanics in two successive attempts (no implantation was attempted); KI-2 requires a passed gate (none ran); KI-3 requires a validation (none occurred). The scorer is unjudged by this record, exactly as it was unjudged by G44-S2's. Method M4 remains GATED — DRAFT ONLY, and the real 44 anchors were not scored — nothing here is a result about them.**

**Standing position, unchanged: the script is not deciphered.** This record is about whether a measuring tool could be built as designed. It says nothing about what any sign means.

---

## 1. What was ordered and what was done

The owner gave the word on 2026-10-26 ("Do the validation run") to execute, once and exactly as drafted, the validation designed in the G44-I implantation draft (`2026-10-26-spec-draft-step0g-implantation-instrument.md`, DRAFT — NOT FROZEN, SHA-256 `53b4ae9e…`). Per draft §10, the run proceeded in stages, checkpointed to disk in `~/workspace/glossa-run/g44i-validation-2026-10-26/`:

1. **Design-and-bars record first** — `DESIGN-AND-BARS-G44I.md` (SHA-256 `2a393f9f…`), written and hashed before any implementation, restating draft §§2–7, identifying the pinned population, recording fresh seeds (model 20270321, split 20270322, leg-2 null 20270323, leg-3 null 20270324 — no predecessor seed reused), and pinning the implementation-level details the draft leaves to the run (draw order, tie-breaks, rounding: round-half-up and largest-remainder, carried from G44-S2).
2. **Step 0 — PASSED EXACT.** The pinned population (Spec 075 §3 construction; corpus and row-grade pins verified by SHA-256; Registry v2 and M77 v3 pins also verified) re-derived from its pinned inputs: **3,045 inscriptions / 557 sign types / 11,805 tokens / 550 signs in sequences of length ≥ 2** — the exact frame, as in every predecessor run.
3. **Split built** (draft §3.2): fitting compilation 1,523 inscriptions / 6,049 tokens; scoring compilation 1,522 inscriptions / 5,756 tokens.
4. **Ledger drawn** (draft §5, order pinned in the design-and-bars record): 44 designated signs; position classes FIRST 14 / MIDDLE 17 / LAST 11 / ONLY 2 (no ONLY-cap reassignment needed; the 3-sign cap was not reached); neighbor classes FIRST 10 / MIDDLE 9 / LAST 8 / ONLY 17. Quotas drawn per compilation and budget-scaled under the draft's own §4.3 rule (the 20% budget engaged in both compilations: fitting 1,369 → 1,209; scoring 1,288 → 1,151 — that rule exists and was applied as written).
5. **Feasibility check (draft §§4.3, 4.7) — FAILED, and the run halted here.** Details in §2 below. Nothing was implanted; no profiles were computed for scoring; no batch, baseline, permutation, or fake batch was computed; legs 1, 1B, 2, 3A, and 3B did not run; the §6 gate did not run. The halt is the course the draft itself prescribes for this event: §4.3 states that if its margins fail to reproduce at the pinned counts, "that is a design-record event to be reported to the owner, not a discrepancy to be absorbed silently."

## 2. The feasibility failure, in numbers

The draft's §4.3/§4.7 feasibility arithmetic was done against the G44-S2 skeleton's proportions, which draft §3.1 quotes (BASE shares FIRST ≈ 0.2395, MIDDLE ≈ 0.5002, LAST ≈ 0.2395, **ONLY ≈ 0.0209** — "on the order of … **244 solo slots** in the full frame", "≈122 solo slots" per compilation, where "the 30-token cap binds"). The pinned frame's actual role totals, recomputed at step 0 and verified by an independent recount, are:

| Class | Pinned frame (actual) | Draft §3.1 skeleton proportions |
|---|---|---|
| FIRST | 2,942 (0.2492) | ≈ 0.2395 |
| MIDDLE | 5,818 (0.4928) | ≈ 0.5002 |
| LAST | 2,942 (0.2492) | ≈ 0.2395 |
| ONLY | **103 (0.0087)** | **≈ 244 (0.0209)** |

The full frame contains **103 solo inscriptions, not ~244** — the solo pool is about 42% of the size the design's arithmetic assumed. (Draft §3.1 anticipated a discrepancy and stated the exact pinned counts govern; its insurance was that the margins were "wide enough that the small difference … cannot decide it." For FIRST, MIDDLE, and LAST that insurance holds — drawn family demand per compilation, e.g. fitting 374 / 501 / 306, sits far inside the real pools 1,473 / 3,053 / 1,473. For ONLY the difference is not small, and it decides everything below.)

Per compilation, the §4.7 family ONLY cap is therefore **min(30, 25% of solo slots)** = min(30, 12.5) = **12.5 cells** (fitting, 50 solo slots) and min(30, 13.25) = **13.25 cells** (scoring, 53 solo slots) — not the 30 the design expected to bind. The drawn ledger's family ONLY cells (spillover from non-ONLY signs contributed 0 in both compilations; the whole total is the two ONLY-planted signs' own cells):

| Compilation | Family ONLY cells | Cap | Result |
|---|---|---|---|
| Fitting | **28** (G44I-19: 12; G44I-25: 16) | 12.5 | **breach, 2.2×** |
| Scoring | **24** (G44I-19: 12; G44I-25: 12) | 13.25 | **breach, 1.8×** |

The breach is not a marginal artifact of this particular draw. An ONLY-planted sign's minimum possible cell is set by the draft's own floors (quota in [20, 28] before budget scaling, concentration in [0.55, 0.70]): even after budget scaling, G44I-25's fitting cell alone (16) exceeds the fitting cap (12.5). Under the pinned solo pool, the cap leaves room for **at most one minimum-size ONLY-planted sign per compilation**, while the §5 draw (weight 0.04 over 44 signs, hard cap 3) expects ~1.76 ONLY-planted signs and will produce two or more in about half of all draws. The draft's ONLY rules are jointly satisfiable only for a minority of draws, and then only at minimum parameter values.

**Why the run halted rather than adapted.** Draft §4.7 states the cap is "enforced at ledger construction" but names **no reduction operation** for it — unlike the §4.3 token budget, which has an explicit largest-remainder scaling rule (applied above, as written). Every available cure would be a design decision the draft does not contain: scaling ONLY-planted quotas or concentrations below their §4.7 floors, reassigning ONLY-planted signs beyond the stated 3-sign cap rule, raising the cap fraction above 25% of solo slots, or changing the model seed after feasibility output had been seen (forbidden by the run discipline: no seed changes after any output is seen, and the feasibility print is an output of the drawn ledger). Under the standing rule for this line — a failed or unbuildable instrument yields a new draft with new pre-committed material, never a patch inside a run — the run stopped, and this record is its result.

**A secondary observation, recorded and not acted on:** 17 of 44 designated signs drew ONLY as their neighbor class. Whether the §4.7 pool-eligibility census (P(ONLY) ≥ 300) would have reassigned many of them was never evaluated — the census sits after fitting implantation in the draft's order of operations, which was never reached. It is noted because a successor draft will have to face it alongside the cap arithmetic: with only 103 solo inscriptions in the frame, ONLY-heavy neighbor evidence is scarce by the same arithmetic that broke the position side.

## 3. Verdict

None — and the absence is the finding. In the draft's §7.5 vocabulary: the run is not VALIDATED (no leg passed; none ran), not FAILED (no leg that ran failed; the instrument was never exercised), and not INCOMPLETE — IMPLANTATION DEFECT (that verdict is reserved by §6 to a recount gate failing after implantation; no implantation exists to recount). The accurate filing, in the draft's own terms, is the §4.3 event: **the design's feasibility margins do not reproduce at the pinned counts; the ledger as drawn cannot be constructed under the draft's rules; reported to the owner as a design-record event.** No kill criterion is triggered (see the headnote), so this record does **not** close the implantation approach, does not convict the scorer, and does not close the Step 0-G line. It closes this run.

## 4. What this means for M4

- Step 0-G remains unsatisfied. M4 stays **GATED — DRAFT ONLY**; its §8 pilot remains inside the gate and may not run. The 44 pending readings are untouched and unscored, carrying no weight, exactly as before.
- The path forward is the owner's decision, and it is a design act, not a run: a successor draft (or a re-issue of this one) whose ONLY rules are derived from the pinned frame's actual solo pool — 103 solo inscriptions in the full frame, ~50 per compilation — rather than from the skeleton's proportions. The arithmetic constraints any such repair must satisfy simultaneously, stated as constraints and not as a design: (i) the family ONLY cap at 25% of solo slots is ≈ 13 cells per compilation; (ii) one ONLY-planted sign at the current floors (quota ≥ 20, concentration ≥ 0.55) needs ≈ 11–16 cells by itself; (iii) spillover cells, drawn totals, and the 3-sign cap all compete for the same ≈ 13 cells. Something in (i)–(iii) — the cap fraction, the quota/concentration floors for ONLY-planted signs, the ONLY draw weight and sign cap, or the split of the solo pool — must give, on the face of a new draft, with the bars of §7 unchanged. This record does not choose among those; choosing inside the halted run is exactly what the halt refused.
- Leg 1B / OD-1: no quantities exist (no baseline was computed). OD-1 remains the owner's open decision, unaffected.

## 5. What this establishes / does not establish

**Establishes:** (a) the pinned census frame reproduces exactly for the fourth instrument in this line (3,045 / 557 / 11,805 / 550, pins verified) — the frame is not in doubt; (b) the pinned frame's solo pool is 103 inscriptions (share 0.0087), materially smaller than the ~244 the G44-I draft's feasibility arithmetic assumed from the G44-S2 skeleton's proportions — a fact about the frame that every future design in this line must now use; (c) the G44-I draft as written cannot fund its own ONLY rules at the pinned counts for a typical ledger draw, for the arithmetic reasons in §2 — the draft's parameter family, not its bars and not its scorer, is what failed to survive contact with the pinned frame; (d) the line's pre-commitment discipline worked as intended: the failure surfaced at ledger construction, before any implantation, scoring, or verdict existed to be attached to.

**Does not establish:** anything about the implantation mechanics (never exercised — KI-1 is not triggered and implantation as an approach is neither convicted nor vindicated); anything about the profile scorer (never run — KI-2 is not triggered); anything about the fake-background arms (never built); anything about the real 44 pending readings, the 94 strict-core readings, any sign's value, or decipherment.

## 6. Run provenance and fences

- Governing draft: `2026-10-26-spec-draft-step0g-implantation-instrument.md` (SHA-256 `53b4ae9e3b00c13643057119b073a8fa14af8216101928608f66a6e2125389da`). Design-and-bars record: `DESIGN-AND-BARS-G44I.md` (SHA-256 `2a393f9f8b501eb5d4304b6e715d2646c8ad12daec23b6fd3f4c10fca3267a4d`), written and hashed before implementation. Implementation (stage 1 only): `stage1_population_ledger.py` (population, split, ledger draws, cells, feasibility), with outputs `stage1.json` and `ledger_working.json` in the run scratch, `~/workspace/glossa-run/g44i-validation-2026-10-26/`. Seeds: model 20270321, split 20270322, leg-2 null 20270323, leg-3 null 20270324 (the null seeds were recorded but never consumed). Python 3.12, standard library only.
- Discipline observed: design and bars fixed and hashed before code; fresh seeds; feasibility checked at ledger construction, before implantation, as the draft orders; no seed change, no parameter adjustment, no cap reinterpretation after the feasibility output was seen; the independent recount of the frame's role totals and the ledger's ONLY cells (separate code path, from the saved population and ledger) agrees with the stage-1 outputs on every number reported here.
- Fences observed: no OSF action, no freeze, no sends, no publishing; the protected local checkout was not used; no restricted data was involved (the population derives from the program's published working frame inputs, pin-verified); implanted streams do not exist and nothing implanted entered any repository; the real 44 anchors were not scored.
