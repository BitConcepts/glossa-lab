"""
P30-E1: Yajnadevam Sanskrit hypothesis falsification.

Runs the same V8-V24 distributional pipeline but uses the Yajnadevam Sanskrit
phoneme inventory instead of the Old Tamil / Dravidian inventory.

If Sanskrit TB-equivalent correlation < Dravidian TB correlation (0.907),
the Dravidian hypothesis survives one falsification round.
If Sanskrit ≥ 0.907, the framework does not distinguish them — needs more anchors.

Key question: does the sign positional structure in the Holdat corpus better match
a Tamil phoneme distribution or a Sanskrit phoneme distribution?

Output: reports/phase30_e1_yajnadevam_falsification.json
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from glossa_lab.experiment_base import ExperimentBase  # noqa: E402

REPO = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab")


class Phase30E1YajnadevamFalsification(ExperimentBase):
    id            = "phase30_e1_yajnadevam_falsification"
    name          = "P30-E1: Yajnadevam Sanskrit falsification run"
    category      = "Indus Script Decipherment"
    description   = (
        "Runs the same distributional pipeline as V8-V24 but with the Yajnadevam "
        "Sanskrit phoneme inventory. Compares resulting TB-correlation against "
        "the Dravidian result (0.907) to test whether the framework distinguishes "
        "Dravidian from Sanskrit."
    )
    estimated_time = "< 1 minute"
    params_schema  = {"type": "object", "properties": {}}

    # ── Sanskrit phoneme inventory from Yajnadevam hypothesis ──────────────
    # Sanskrit stops + nasals + approximants in initial position
    SANSKRIT_INITIALS = [
        "ka", "kha", "ga", "gha", "ṅa",  # velar
        "ca", "cha", "ja", "jha", "ña",   # palatal
        "ṭa", "ṭha", "ḍa", "ḍha", "ṇa",  # retroflex
        "ta", "tha", "da", "dha", "na",   # dental
        "pa", "pha", "ba", "bha", "ma",   # labial
        "ya", "ra", "la", "va",            # semivowels
        "śa", "ṣa", "sa", "ha",           # sibilants
    ]
    SANSKRIT_MEDIALS = [
        "ā", "i", "ī", "u", "ū", "e", "ai", "o", "au",  # vowel ligatures
        "ṃ", "ḥ",                                           # anusvara/visarga
        "kṣa", "tra",                                       # compound consonants
        "gar", "dur", "nau", "pat",
        "yaj", "agni", "indra", "vayu", "soma",
    ]
    SANSKRIT_TERMINALS = [
        "aḥ", "āḥ", "iḥ", "uḥ", "eḥ", "oḥ",   # visarga nominals
        "am", "ān", "āṃ", "iṃ", "uṃ",           # accusative/genitive
        "asya", "āya", "ena", "ā",               # common suffixes
        "svāhā", "namaḥ",                         # vedic endings
    ]
    # Sanskrit initial phoneme frequency (approximate Vedic Sanskrit distribution)
    SANSKRIT_FREQ = {
        "a": 0.18, "i": 0.06, "u": 0.05, "e": 0.03, "o": 0.02,
        "k": 0.10, "c": 0.03, "t": 0.07, "p": 0.07, "n": 0.08,
        "m": 0.06, "y": 0.04, "r": 0.07, "l": 0.02, "v": 0.04,
        "s": 0.05, "h": 0.03, "g": 0.03, "d": 0.03, "b": 0.01,
    }

    def run(self, params: dict | None = None, reporter=None) -> dict:  # type: ignore[override]
        def _report(msg: str) -> None:
            if reporter:
                reporter.progress(msg)
            print(msg)

        _report("P30-E1: Yajnadevam Sanskrit falsification …")

        # Load Holdat corpus
        HOLDAT = (
            REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
        )
        seals: dict = defaultdict(list)
        with open(HOLDAT, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                seals[row["cisi_number"]].append(row)
        corpus = [
            {"id": k, "signs": [r["letters"] for r in sorted(v, key=lambda x: int(x["position"]))]}
            for k, v in seals.items()
        ]
        sign_freq: Counter = Counter(s for e in corpus for s in e["signs"])
        _report(f"  Corpus: {len(corpus)} seals, {len(sign_freq)} signs")

        # Compute bigrams + position profiles
        bigrams: Counter = Counter()
        for e in corpus:
            for i in range(len(e["signs"]) - 1):
                bigrams[(e["signs"][i], e["signs"][i + 1])] += 1

        def classify_pos(sign):
            init = med = term = 0
            for e in corpus:
                seq = e["signs"]
                for i, s in enumerate(seq):
                    if s == sign:
                        if len(seq) == 1: med += 1
                        elif i == 0: init += 1
                        elif i == len(seq) - 1: term += 1
                        else: med += 1
            total = init + med + term
            if total == 0: return "MEDIAL", 0
            if init / total > 0.6: return "INITIAL", total
            if term / total > 0.4: return "TERMINAL", total
            return "MEDIAL", total

        def tb_corr_generic(assigned, freq_table):
            pf, tw = Counter(), 0
            for s, r in assigned.items():
                if r.startswith(("?","TERM-","INIT-","MED-")): continue
                fr = sign_freq.get(s, 1)
                if r and r[0].isalpha():
                    pf[r[0].lower()] += fr; tw += fr
            if tw == 0: return 0.0
            dist = {k: v/tw for k, v in pf.items()}
            sh   = set(dist) & set(freq_table)
            if len(sh) < 3: return 0.0
            x = [dist.get(k, 0)      for k in sorted(sh)]
            y = [freq_table.get(k, 0) for k in sorted(sh)]
            return round(float(np.corrcoef(x, y)[0, 1]), 4)

        _report("  Building Sanskrit distributional assignment …")
        rng = np.random.default_rng(42)
        skt_anchors: dict[str, str] = {}
        for sign, freq in sign_freq.most_common():
            pos, total = classify_pos(sign)
            if pos == "INITIAL":
                candidates = self.SANSKRIT_INITIALS
            elif pos == "TERMINAL":
                candidates = self.SANSKRIT_TERMINALS
            else:
                candidates = self.SANSKRIT_MEDIALS
            best_r, best_sc = candidates[0], -1
            for cand in candidates:
                sc = self.SANSKRIT_FREQ.get(cand[0], 0) * 10
                used = sum(1 for v in skt_anchors.values() if v == cand)
                sc += 2 if used == 0 else 1 if used == 1 else 0
                if sc > best_sc: best_sc, best_r = sc, cand
            skt_anchors[sign] = best_r

        # Also load Dravidian FINAL_ANCHORS for comparison
        fa_file = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
        dravidian_anchors: dict[str, str] = {}
        if fa_file.exists():
            fa = json.loads(fa_file.read_text(encoding="utf-8"))
            dravidian_anchors = {
                s: info["reading"]
                for s, info in fa["anchors"].items()
                if not info["reading"].startswith(("?","TERM-","INIT-","MED-"))
            }

        # Dravidian TB frequencies (empirical)
        DRAVIDIAN_FREQ = {
            "a": 0.1168, "i": 0.0778, "u": 0.0221, "e": 0.0438, "o": 0.0979,
            "k": 0.0576, "c": 0.0827, "t": 0.1608, "p": 0.0705, "n": 0.0631,
            "m": 0.0368, "y": 0.0168, "r": 0.0624, "l": 0.0668, "v": 0.0240,
        }

        # Compute both correlations
        skt_corr_vs_dravidian_freq   = tb_corr_generic(skt_anchors, DRAVIDIAN_FREQ)
        skt_corr_vs_sanskrit_freq    = tb_corr_generic(skt_anchors, self.SANSKRIT_FREQ)
        drav_corr_vs_dravidian_freq  = tb_corr_generic(dravidian_anchors, DRAVIDIAN_FREQ)
        drav_corr_vs_sanskrit_freq   = tb_corr_generic(dravidian_anchors, self.SANSKRIT_FREQ)

        _report(f"""
=== P30-E1 FALSIFICATION RESULTS ===

  Sanskrit assignment vs Tamil-Brahmi freq:  {skt_corr_vs_dravidian_freq}
  Sanskrit assignment vs Sanskrit freq:       {skt_corr_vs_sanskrit_freq}
  Dravidian assignment vs Tamil-Brahmi freq:  {drav_corr_vs_dravidian_freq}  (V24 result)
  Dravidian assignment vs Sanskrit freq:      {drav_corr_vs_sanskrit_freq}
""")

        if drav_corr_vs_dravidian_freq > skt_corr_vs_dravidian_freq:
            verdict = (
                f"DRAVIDIAN SURVIVES: Dravidian assignment ({drav_corr_vs_dravidian_freq}) "
                f"> Sanskrit assignment ({skt_corr_vs_dravidian_freq}) vs TB freq"
            )
        elif abs(drav_corr_vs_dravidian_freq - skt_corr_vs_dravidian_freq) < 0.05:
            verdict = (
                f"INDISTINGUISHABLE: Dravidian ({drav_corr_vs_dravidian_freq}) ≈ "
                f"Sanskrit ({skt_corr_vs_dravidian_freq}) — framework doesn't separate them"
            )
        else:
            verdict = (
                f"SANSKRIT SCORES HIGHER: Sanskrit ({skt_corr_vs_dravidian_freq}) "
                f"> Dravidian ({drav_corr_vs_dravidian_freq}) — reconsider Dravidian hypothesis"
            )

        _report(f"  Verdict: {verdict}")

        return {
            "sanskrit_corr_vs_tb_freq":       skt_corr_vs_dravidian_freq,
            "sanskrit_corr_vs_skt_freq":      skt_corr_vs_sanskrit_freq,
            "dravidian_corr_vs_tb_freq":      drav_corr_vs_dravidian_freq,
            "dravidian_corr_vs_skt_freq":     drav_corr_vs_sanskrit_freq,
            "verdict":                         verdict,
            "n_signs_assigned_sanskrit":       len(skt_anchors),
            "n_signs_in_dravidian":            len(dravidian_anchors),
        }


if __name__ == "__main__":
    Phase30E1YajnadevamFalsification().run_cli()
