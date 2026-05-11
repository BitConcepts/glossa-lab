"""
Phase-32 T4: SA decipherment M77 → Tamil-Brahmi LM.

This is the BIG TEST: run SimulatedAnnealing with:
  - Cipher corpus: Mahadevan 1977 M77 inscriptions (1,669 from indus_public_corpus)
  - Language model: Tamil-Brahmi bigram LM (from 121-inscription updated corpus)
  - Anchors: Parpola phoneme map (parpola_phonemes.json, 35+ entries)
  - Seeds: 5 parallel (ProcessPoolExecutor per H10.2)

Expected: if SA finds a high-scoring mapping, it is the strongest non-circular result yet.
Null result (score < random) = strong evidence against Dravidian hypothesis.

Output: reports/phase32_sa_m77_tb.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from glossa_lab.experiment_base import ExperimentBase  # noqa: E402

REPO = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab")


class Phase32SAM77TB(ExperimentBase):
    id            = "phase32_sa_m77_tb"
    name          = "Phase-32 T4: SA M77 → Tamil-Brahmi LM"
    category      = "Indus Script Decipherment"
    description   = (
        "SimulatedAnnealing decipherment of M77 corpus using Tamil-Brahmi bigram LM "
        "from 121-inscription updated corpus. 5 seeds, 10000 iters each. "
        "Phase-32 T4 — the critical non-circular test."
    )
    estimated_time = "15-30 minutes (GPU) / 60-90 minutes (CPU)"
    params_schema  = {
        "type": "object",
        "properties": {
            "n_seeds":    {"type": "integer", "default": 5,     "minimum": 1, "maximum": 20},
            "n_iters":    {"type": "integer", "default": 10000, "minimum": 1000},
            "temp_start": {"type": "number",  "default": 1.0},
            "temp_end":   {"type": "number",  "default": 0.001},
        },
    }

    def run(self, params: dict | None = None, reporter=None) -> dict:  # type: ignore[override]
        import math
        import random
        import numpy as np
        from collections import Counter, defaultdict
        from concurrent.futures import ProcessPoolExecutor, as_completed

        params  = params or {}
        n_seeds = int(params.get("n_seeds", 5))
        n_iters = int(params.get("n_iters", 10000))
        T_start = float(params.get("temp_start", 1.0))
        T_end   = float(params.get("temp_end", 0.001))

        def _report(msg: str) -> None:
            if reporter:
                reporter.progress(msg)
            print(msg)

        _report("Loading M77 corpus …")
        m77_corpus = self._load_m77()
        _report(f"  M77: {len(m77_corpus)} inscriptions")

        _report("Loading Tamil-Brahmi LM …")
        tb_lm = self._load_tb_lm()
        _report(f"  TB LM: {len(tb_lm)} bigrams")

        _report("Loading Parpola phoneme anchors …")
        anchors = self._load_parpola_anchors()
        _report(f"  Anchors: {len(anchors)} sign→phoneme pairs")

        # Build sign frequency and vocabulary
        sign_freq: Counter = Counter()
        for seq in m77_corpus:
            sign_freq.update(seq)
        signs = list(sign_freq.keys())
        phonemes = list({p for p in anchors.values()} | set(tb_lm.get("vocab", [])))

        _report(f"  Signs: {len(signs)}, Phonemes: {len(phonemes)}, Tokens: {sum(sign_freq.values())}")

        def sa_one_seed(seed: int) -> dict:
            """Run one SA seed. Must be top-level for ProcessPoolExecutor."""
            rng = random.Random(seed)
            nrng = np.random.default_rng(seed)

            # Initialize: start with anchors, fill rest randomly
            mapping: dict[str, str] = dict(anchors)
            free_signs   = [s for s in signs if s not in mapping]
            free_phonemes = [p for p in phonemes if p not in mapping.values()]
            for s in free_signs:
                p = rng.choice(phonemes) if phonemes else s
                mapping[s] = p

            def score(m: dict) -> float:
                """NLL of M77 corpus under bigram LM given mapping m."""
                total = 0.0
                for seq in m77_corpus:
                    decoded = [m.get(s, "") for s in seq]
                    for i in range(len(decoded) - 1):
                        a, b = decoded[i], decoded[i + 1]
                        if a and b:
                            total += tb_lm.get("bigrams", {}).get(f"{a}|{b}", -8.0)
                return total

            best_mapping = dict(mapping)
            best_score   = score(mapping)
            current_score = best_score

            cool_rate = (T_end / T_start) ** (1 / max(n_iters, 1))
            T = T_start

            for iteration in range(n_iters):
                # Propose swap: swap two non-anchor signs' phoneme assignments
                swap_signs = [s for s in signs if s not in anchors]
                if len(swap_signs) < 2:
                    break
                s1, s2 = rng.sample(swap_signs, 2)
                mapping[s1], mapping[s2] = mapping[s2], mapping[s1]

                new_score = score(mapping)
                delta = new_score - current_score
                if delta > 0 or rng.random() < math.exp(delta / max(T, 1e-10)):
                    current_score = new_score
                    if current_score > best_score:
                        best_score   = current_score
                        best_mapping = dict(mapping)
                else:
                    mapping[s1], mapping[s2] = mapping[s2], mapping[s1]

                T *= cool_rate

            return {
                "seed":          seed,
                "best_score":    best_score,
                "n_iters":       n_iters,
                "mapping_sample": {s: best_mapping[s] for s in list(signs)[:15]},
                "top5_decoded":  self._top5_decoded(m77_corpus, best_mapping, sign_freq),
            }

        _report(f"Running SA: {n_seeds} seeds × {n_iters} iters …")
        seed_results = []
        workers = min(n_seeds, 4)
        try:
            with ProcessPoolExecutor(max_workers=workers) as ex:
                futs = {ex.submit(sa_one_seed, s): s for s in range(n_seeds)}
                for i, fut in enumerate(as_completed(futs)):
                    r = fut.result()
                    seed_results.append(r)
                    _report(f"  Seed {r['seed']} done: score={r['best_score']:.1f}")
        except Exception as e:
            _report(f"  Parallel failed ({e}), running sequential …")
            for s in range(n_seeds):
                r = sa_one_seed(s)
                seed_results.append(r)
                _report(f"  Seed {r['seed']} done: score={r['best_score']:.1f}")

        seed_results.sort(key=lambda x: -x["best_score"])
        best = seed_results[0]

        # Random null: what score does a random mapping get?
        rng2 = random.Random(99999)
        null_mappings = []
        for _ in range(20):
            null_m = dict(anchors)
            shuffled = list(phonemes)
            rng2.shuffle(shuffled)
            for j, s in enumerate([s for s in signs if s not in anchors]):
                null_m[s] = shuffled[j % len(shuffled)] if shuffled else ""
            null_score = 0.0
            for seq in m77_corpus[:100]:
                dec = [null_m.get(s, "") for s in seq]
                for k in range(len(dec) - 1):
                    a, b = dec[k], dec[k + 1]
                    if a and b:
                        null_score += tb_lm.get("bigrams", {}).get(f"{a}|{b}", -8.0)
            null_mappings.append(null_score)
        null_mean = sum(null_mappings) / len(null_mappings)

        lift = best["best_score"] - null_mean
        verdict = (
            "FAVORABLE: SA finds mapping significantly above null"
            if lift > 100 else
            "NEUTRAL: SA result close to null — inconclusive"
            if lift > -50 else
            "UNFAVORABLE: SA score below null — against Dravidian hypothesis"
        )

        _report(f"\nBest SA score:   {best['best_score']:.1f}")
        _report(f"Null mean score: {null_mean:.1f}")
        _report(f"Lift:            {lift:.1f}")
        _report(f"Verdict:         {verdict}")

        return {
            "best_score":     best["best_score"],
            "null_mean":      null_mean,
            "lift":           lift,
            "verdict":        verdict,
            "n_seeds":        n_seeds,
            "n_iters":        n_iters,
            "n_anchors":      len(anchors),
            "n_signs":        len(signs),
            "seed_results":   seed_results,
            "top5_decoded":   best["top5_decoded"],
        }

    # ---------- helpers ----------

    def _load_m77(self) -> list[list[str]]:
        """Load M77 Indus corpus sign sequences (Mahadevan 1977, M-numbers)."""
        # Try indus_public_corpus.py data
        try:
            from glossa_lab.data.indus_public_corpus import get_corpus
            raw = get_corpus()
            return [entry.get("signs", entry.get("sequence", [])) for entry in raw if entry]
        except Exception:
            pass
        # Fallback: Holdat CSV (already Mahadevan M-numbers)
        import csv as _csv
        from collections import defaultdict as _dd
        HOLDAT = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
        seals: dict = _dd(list)
        with open(HOLDAT, encoding="utf-8") as f:
            for row in _csv.DictReader(f):
                seals[row["cisi_number"]].append(row)
        return [
            [r["letters"] for r in sorted(v, key=lambda x: int(x["position"]))]
            for v in seals.values()
        ]

    def _load_tb_lm(self) -> dict:
        """Load the clean Dravidian Tamil bigram LM.

        Uses dravidian_tamil_lm.json (DEDR + Parpola + Sangam corpus, CLEAN).
        See CITATIONS.md sections E.1 (DEDR/Burrow+Emeneau), E.2 (Krishnamurti),
        E.3 (Sangam), C.1/C.2 (Parpola).
        Built by: backend/scripts/build_dravidian_lm.py
        """
        # Primary: clean Dravidian LM from dravidian.py (DEDR + Sangam + Parpola)
        clean_lm = REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json"
        if clean_lm.exists():
            d = json.loads(clean_lm.read_text(encoding="utf-8"))
            # Convert bigram keys back to native dict (already log-probs)
            return {
                "bigrams": d.get("bigrams", {}),
                "vocab":   d.get("vocab", []),
                "source":  "dravidian_tamil_lm.json (DEDR+Sangam+Parpola, CLEAN)",
                "n_bigrams": d.get("n_bigrams", 0),
            }
        # Fallback: build from TB inscriptions (noisy but better than empty)
        import math as _math
        tb_json = REPO / "backend/glossa_lab/data/mahadevan_2003_tamil_brahmi.json"
        if not tb_json.exists():
            return {"bigrams": {}, "vocab": []}
        tb = json.loads(tb_json.read_text(encoding="utf-8"))
        inscriptions = tb.get("inscriptions", [])
        bigram_counts: Counter = Counter()
        unigram_counts: Counter = Counter()
        for insc in inscriptions:
            aksharas = insc.get("literal_aksharas", [])
            if len(aksharas) < 2:
                continue
            for a in aksharas:
                unigram_counts[a] += 1
            for i in range(len(aksharas) - 1):
                bigram_counts[(aksharas[i], aksharas[i + 1])] += 1
        vocab = list(unigram_counts.keys())
        V     = len(vocab)
        lm: dict[str, float] = {}
        for (a, b), cnt in bigram_counts.items():
            prob = (cnt + 1) / (unigram_counts.get(a, 0) + V + 1)
            lm[f"{a}|{b}"] = _math.log(prob)
        return {"bigrams": lm, "vocab": vocab, "source": "mahadevan_2003 (fallback, noisy)"}

    def _load_parpola_anchors(self) -> dict[str, str]:
        """Load Parpola phoneme map as sign→phoneme anchors (M-number format where possible)."""
        parpola_file = REPO / "backend/glossa_lab/data/parpola_phonemes.json"
        if not parpola_file.exists():
            return {}
        raw = json.loads(parpola_file.read_text(encoding="utf-8"))
        if isinstance(raw, list) and raw:
            raw = raw[0] if isinstance(raw[0], dict) else {}
        anchors: dict[str, str] = {}
        # Try to get sign_id → phoneme_value pairs
        entries = raw.get("entries", raw) if isinstance(raw, dict) else []
        if isinstance(entries, list):
            for entry in entries:
                sid = entry.get("sign_id", "")
                pv  = entry.get("phoneme_value", "")
                if sid and pv:
                    anchors[sid] = pv
        # Also use INDUS_FINAL_ANCHORS HIGH/MEDIUM entries
        final_file = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
        if final_file.exists():
            fa = json.loads(final_file.read_text(encoding="utf-8"))
            for sid, info in fa.get("anchors", {}).items():
                if info.get("confidence") in ("HIGH", "MEDIUM") and "?" not in info.get("reading", "?"):
                    anchors[sid] = info["reading"]
        return anchors

    def _top5_decoded(
        self,
        corpus: list[list[str]],
        mapping: dict[str, str],
        sign_freq: Counter,
    ) -> list[dict]:
        """Return 5 representative decoded inscriptions."""
        top_seals = [
            seq for seq in sorted(corpus, key=lambda s: -sum(sign_freq.get(x, 0) for x in s))
            if len(seq) >= 3
        ][:5]
        return [
            {"indus": seq, "decoded": [mapping.get(s, "?") for s in seq]}
            for seq in top_seals
        ]


if __name__ == "__main__":
    Phase32SAM77TB().run_cli()
