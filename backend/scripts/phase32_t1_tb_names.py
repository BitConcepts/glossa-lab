"""
Phase-32 T1: TB-NAMES corpus extraction.

Extracts proper names (donor, dedicatee, title-holder) from the
mahadevan_2003_tamil_brahmi.json romanized translations.

Name patterns in Tamil-Brahmi cave inscriptions:
  "Charity to X"       → donor giving to named person X
  "Given by X"         → donor X
  "The gift of X"      → donor X
  "Behold! [sentence with name]"
  "...made by X, the [title]"
  etc.

Also extracts the clean literal_aksharas sequences as a proper-name
syllable corpus for length-comparison with M77.

Output: reports/phase32_t1_tb_names.json
        backend/glossa_lab/data/tb_names_corpus.json
Citations: A.12 (Mahadevan 2003, Harvard Oriental Series 62)
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "backend"))
from glossa_lab.experiment_base import ExperimentBase  # noqa: E402

TB_PATH   = REPO / "backend/glossa_lab/data/mahadevan_2003_tamil_brahmi.json"
OUT_NAMES = REPO / "backend/glossa_lab/data/tb_names_corpus.json"
OUT_REPORT= REPO / "reports/phase32_t1_tb_names.json"


class Phase32T1TBNames(ExperimentBase):
    id            = "phase32_t1_tb_names"
    name          = "Phase-32 T1: TB-NAMES corpus extraction"
    category      = "Indus Script Decipherment"
    description   = (
        "Extract proper names from Mahadevan 2003 Tamil-Brahmi inscriptions "
        "(romanized translation field). Builds a TB-NAMES corpus of personal "
        "name tokens for length comparison with M77 (eliminating genre confound "
        "from Phase-31 T2). Also reports clean akshara sequence stats."
    )
    estimated_time = "< 30 seconds"

    def run(self, params=None, reporter=None):
        def _report(msg):
            if reporter: reporter.progress(msg)
            print(msg)

        if not TB_PATH.exists():
            return {"error": f"TB file not found: {TB_PATH}"}

        tb = json.loads(TB_PATH.read_text(encoding="utf-8"))
        inscriptions = tb.get("inscriptions", [])
        _report(f"Loaded {len(inscriptions)} TB inscriptions")

        # ── Name extraction patterns ─────────────────────────────────────────
        # These patterns come from analysis of Mahadevan 2003 translation style
        NAME_PATTERNS = [
            # "Charity to NAME" / "Gift to NAME"
            r"[Cc]harity\s+to\s+([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+){0,3})",
            r"[Gg]ift\s+to\s+([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+){0,3})",
            r"[Gg]iven\s+to\s+([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+){0,3})",
            # "Given/Made by NAME"
            r"(?:given|made|carved|caused to be carved)\s+by\s+([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+){0,3})",
            # "The gift of NAME"
            r"[Tt]he\s+gift\s+of\s+([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+){0,3})",
            # "NAME, the [title]"  — capture names before common titles
            r"([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+){0,2}),\s+the\s+(?:kani|merchant|monk|chief|king|prince|hermit|son|daughter)",
            # Explicit person fields if present
        ]

        names_found: list[dict] = []
        name_lengths: list[int] = []  # in syllables (from aksharas)

        for insc in inscriptions:
            text = insc.get("romanized_text_b_raw", "") or ""
            # Also check any translation fields
            for field in ["translation_partial", "english_translation", "translation"]:
                text += " " + (insc.get(field) or "")

            insc_names = []
            for pat in NAME_PATTERNS:
                for m in re.finditer(pat, text, re.IGNORECASE):
                    name = m.group(1).strip()
                    # Filter out obvious false positives (function words)
                    if name.lower() not in {"the", "a", "an", "this", "that", "his", "her"}:
                        insc_names.append(name)

            # Explicit donor field
            if insc.get("donor"):
                insc_names.append(str(insc["donor"]))
            if insc.get("dedicatee"):
                insc_names.append(str(insc["dedicatee"]))

            if insc_names:
                names_found.append({
                    "inscription_id": insc.get("inscription_id", "?"),
                    "site": insc.get("site", "?"),
                    "names": list(dict.fromkeys(insc_names)),  # deduplicate
                    "n_aksharas": insc.get("n_aksharas", 0),
                })
                name_lengths.append(insc.get("n_aksharas", 0))

        _report(f"Inscriptions with extracted names: {len(names_found)}")

        # ── Clean akshara stats ──────────────────────────────────────────────
        CYRILLIC_RE = re.compile(r"[\u0400-\u04ff]")
        clean_insc = []
        for insc in inscriptions:
            aksharas = insc.get("literal_aksharas", [])
            clean = [a for a in aksharas if a and not CYRILLIC_RE.search(a) and 1 <= len(a) <= 5]
            if clean:
                clean_insc.append({
                    "id": insc.get("inscription_id", "?"),
                    "site": insc.get("site", "?"),
                    "n_original": len(aksharas),
                    "n_clean": len(clean),
                    "pct_clean": round(100 * len(clean) / max(len(aksharas), 1), 1),
                    "clean_aksharas": clean,
                })

        total_clean = sum(i["n_clean"] for i in clean_insc)
        total_original = sum(i["n_original"] for i in clean_insc)
        _report(f"Clean aksharas: {total_clean}/{total_original} "
                f"({100*total_clean//max(total_original,1)}%) across {len(clean_insc)} inscriptions")

        # ── Length comparison: M77 vs TB-NAMES ───────────────────────────────
        m77_mean = 3.2  # known from Holdat corpus analysis
        tb_mean_all = (sum(i.get("n_aksharas", 0) for i in inscriptions) /
                       max(len(inscriptions), 1))
        tb_mean_named = (sum(name_lengths) / max(len(name_lengths), 1)) if name_lengths else 0

        _report(f"\nLength comparison:")
        _report(f"  M77 mean inscription length: {m77_mean:.1f} signs")
        _report(f"  TB mean akshara count (all): {tb_mean_all:.1f}")
        _report(f"  TB mean akshara count (name-bearing only): {tb_mean_named:.1f}")

        # Genre confound assessment
        if abs(tb_mean_named - m77_mean) < abs(tb_mean_all - m77_mean):
            genre_verdict = "FAVORABLE: name-bearing TB inscriptions closer in length to M77"
        else:
            genre_verdict = "NEUTRAL: name extraction did not reduce genre confound substantially"

        _report(f"Genre confound verdict: {genre_verdict}")

        # ── All unique names ─────────────────────────────────────────────────
        all_names = []
        for r in names_found:
            all_names.extend(r["names"])
        unique_names = sorted(set(all_names))
        _report(f"\nTotal unique names extracted: {len(unique_names)}")
        for n in unique_names[:20]:
            _report(f"  {n}")

        # ── Save ─────────────────────────────────────────────────────────────
        names_corpus = {
            "_citation": {"primary_sources": ["A.12"], "derivation": "Phase-32 T1 proper name extraction from Mahadevan 2003 Tamil-Brahmi inscriptions"},
            "n_inscriptions_total": len(inscriptions),
            "n_inscriptions_with_names": len(names_found),
            "unique_names": unique_names,
            "name_bearing_inscriptions": names_found,
            "clean_akshara_inscriptions": clean_insc,
            "stats": {
                "total_clean_aksharas": total_clean,
                "total_original_aksharas": total_original,
                "pct_clean": round(100 * total_clean / max(total_original, 1), 1),
                "m77_mean_length": m77_mean,
                "tb_mean_length_all": round(tb_mean_all, 2),
                "tb_mean_length_named": round(tb_mean_named, 2),
            },
        }
        OUT_NAMES.write_text(json.dumps(names_corpus, ensure_ascii=False, indent=2), encoding="utf-8")

        result = {
            "n_inscriptions": len(inscriptions),
            "n_with_names": len(names_found),
            "unique_names": unique_names,
            "n_unique_names": len(unique_names),
            "clean_inscriptions": len(clean_insc),
            "total_clean_aksharas": total_clean,
            "pct_clean": round(100 * total_clean / max(total_original, 1), 1),
            "m77_mean_length": m77_mean,
            "tb_mean_length_all": round(tb_mean_all, 2),
            "tb_mean_length_named": round(tb_mean_named, 2),
            "genre_confound_verdict": genre_verdict,
            "citations": ["A.12"],
        }
        OUT_REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        _report(f"\nSaved: {OUT_NAMES}")
        _report(f"Saved: {OUT_REPORT}")
        return result


if __name__ == "__main__":
    Phase32T1TBNames().run_cli()
