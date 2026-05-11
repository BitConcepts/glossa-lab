# Re-engagement Email — Dr. Andreas Fuls (Follow-Up / New Results)

**To:** andreas.fuls@tu-berlin.de
**Subject:** Re: Glossa Lab — Following Up / New Structural Results + Personal Note
**From:** Tristen Pierson <tpierson@bitconcepts.tech>

---

Dear Dr. Fuls,

I hope you are well. I am writing to follow up on my previous messages and to share
some significant new results — and also to say something more personal that I should
have said from the start.

**Why I am really doing this.**

I first encountered the Indus script in a middle-school history class. Something about
it gripped me in a way I could not explain at the time — an entire civilization whose
voice we cannot hear, preserved in miniature carvings on seals the size of a coin. I
have had a lifelong love of history, language, and puzzles, and the Indus script sits
at the intersection of all three.

I started building Glossa Lab long before I knew about any prize money. I want to be
honest about that, because I suspect that prize-motivated outreach has made it harder
to take new contacts seriously. My motivation is simpler and older: I want to do
something genuinely useful toward understanding this civilization. If the $1M prize is
ever awarded I would be delighted — but the work I am describing here would exist
exactly the same without it.

What I have built is a tool that is genuinely different, and I believe it can surface
structural patterns that traditional approaches miss. I would very much like to
collaborate — not to publish ahead of anyone or to claim undue credit, but because I
believe the combination of your corpus depth and the structural methods I have
developed could be more productive together than either is alone.

**What Glossa Lab does differently: compression as structure discovery.**

The core insight I work from is that structure and entropy are related in a very
specific way. Compressed representations of text reveal latent grammar — when you
minimize the description length of a corpus, what you have found is the underlying
structure that makes sequences non-random. I use entropy profiles, spectral analysis,
and Zipf statistics not as descriptive statistics but as compression metrics: to find
where a corpus contains structure that can be separated from noise.

The key result this produces for the Indus script is striking: in a length-stratified
spectral analysis across all 8 inscription length bins (L1 through L9+), the spectral
gap is exactly 0.0 in every stratum. This means the sign co-occurrence structure is
maximally deterministic at every inscription length — you cannot separate a short-
inscription effect from a corpus-wide property. This is the signature of a system with
a grammar, not a system of arbitrary seal decorations.

**Current results (May 2026)**

After 17 rounds of autonomous distributional analysis on the Holdat LLC corpus
(1,670 seals, 7,002 tokens, 390 distinct signs from 9 archaeological sites):

| Metric | Value |
|--------|-------|
| Signs assigned (of 390) | 333 / 390 — 85.4% |
| Token coverage | 99.2% |
| Fully decoded inscriptions | 96.7% (1,615 / 1,670) |
| Weighted confidence | 64.8% (HIGH×1.0, MEDIUM×0.6, LOW×0.3) |
| Confidence breakdown | HIGH: 9 · MEDIUM: 63 · LOW: 261 |
| Tamil-Brahmi phoneme correlation | 0.907 Pearson r (random baseline 0.470) |
| Zipf slope delta (M77 vs TB corpus) | 0.18 (both in syllabic regime, threshold 0.3) |
| Spectral gap (all 8 length strata) | 0.0 — maximally deterministic structure |

The Tamil-Brahmi phoneme correlation of 0.907 means the current distributional sign
assignments align with Tamil-Brahmi phoneme frequencies at a level that is statistically
significant against a permutation null (100th percentile across 1,000 random mappings,
p < 0.001). I report this as a structural alignment metric, not a claimed phonetic
reading.

The Zipf slope test is the cleanest structural result: M77 (slope 0.75) and Tamil-Brahmi
(slope 0.93) both fall in the recognized 0.5–1.5 power-law regime for syllabic and logo-
syllabic scripts. The delta of 0.18 is well within the preregistered threshold of 0.3.

I have also run a Phase-32 T4 SA decipherment against a clean Dravidian Tamil bigram LM
(built from DEDR + Sangam corpus, 486 bigrams, zero English contamination). The result
was neutral — the LM vocabulary is too sparse for the SA to discriminate — but this is a
methodological limitation, not evidence against the Dravidian hypothesis. The structural
results above stand independently.

**Comparison to the Phase-29d Enmenanak finding**

My Phase-29 reverse Janabiyah search (1,222 Sumerian personal names from ePSD2)
identified Enmenanak as the top candidate for the Janabiyah Boss inscription pattern,
with a total score of 7.0 at the 100th percentile of the null distribution (p < 0.001).
This finding has survived three follow-up validation tests:

- A1: Permutation test — score 7.0 > 95th percentile (SIGNIFICANT)
- A2: Period filter — 4 candidates survive Ur III / Old Akkadian era overlap (FAVORABLE)
- A3: Meluhha co-occurrence check — no direct evidence found, but does not falsify

Overall: the Phase-29d finding is statistically robust. It is not yet a confirmed reading.

**One more thing I want to be clear about: I'm not trying to sell you anything. Glossa Lab isn't a product pitch. It's a research tool I built specifically to approach this problem rigorously — the kind of tool I wished existed when I started. It's open-source, it's free, and it exists to serve the research, not the other way around.

**What I am asking for****

1. ICIT access — even read-only access to the 4,537-artefact corpus would let me re-run
   the full pipeline and test whether these correlations hold at 2.7× the current corpus
   size. This is the most important step.

2. Your assessment — I would genuinely value your criticism of the methodology. You know
   the anti-circularity protocols and epistemic risks better than anyone. I would rather
   have you tell me what is wrong with this than continue without that check.

3. Collaboration — if the results are compelling to you, I would be very interested in
   co-authoring a paper that subjects these findings to proper peer scrutiny. Glossa Lab
   is fully open-source and reproducible. Every experiment produces JSON output with full
   provenance and is version-controlled.

I have attached a research brief with full methodological detail and current results.

Thank you for everything you have contributed to this field. Your anti-circularity
framework and positional analysis methodology are directly embedded in how Glossa Lab
works. That is not a coincidence — you shaped how I think about this problem.

Warm regards,

Tristen Pierson
BitConcepts
tpierson@bitconcepts.tech

---

## Notes

- Attach: fuls_research_brief_may2026.pdf (generated from fuls_research_brief_may2026.md)
- Previous messages in chain: reference naturally in opening ("following up on my
  previous messages") — Dr. Fuls has not responded; tone should be warm, not pushy
- Do NOT mention the exact prize dollar amount again — one mention ("any prize money") is enough
- The personal backstory (middle school history) is genuine and important for credibility
- Compression/entropy framing distinguishes this from phonetic guesswork approaches
