"""Corpus seeder — pre-populates the database with all built-in corpora.

Run automatically on first startup (when DB has 0 texts).
Safe to re-run: skips corpora that already exist by name.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from glossa_lab.database import Database

log = logging.getLogger(__name__)

BUILT_IN_CORPORA = [
    "ugaritic",
    "linear_b",
    "hebrew",
    "indus_synthetic",
    "sumerian_ur3",
    "geez",
    "nw_semitic",
]


async def seed_corpora(db: "Database") -> None:
    """Seed built-in corpora into the database if not already present."""
    try:
        existing = await db.list_texts()
        existing_names = {t["name"] for t in existing}
    except Exception:
        return  # DB not ready

    if len(existing) > 0 and all(_corpus_name(c) in existing_names for c in BUILT_IN_CORPORA):
        return  # Already seeded

    log.info("Seeding built-in corpora...")
    for corpus_id in BUILT_IN_CORPORA:
        name = _corpus_name(corpus_id)
        if name in existing_names:
            continue
        try:
            corpus_data = _load_corpus(corpus_id)
            if corpus_data is None:
                continue
            now = datetime.now(timezone.utc).isoformat()
            await db.create_text(
                name=name,
                corpus_type=corpus_data["corpus_type"],
                content=corpus_data["content"],
                metadata=corpus_data.get("metadata", {}),
                created_at=now,
            )
            n = len(corpus_data["content"])
            log.info("Seeded corpus: %s (%d symbols)", name, n)
        except Exception as exc:
            log.warning("Failed to seed %s: %s", corpus_id, exc)


def _corpus_name(corpus_id: str) -> str:
    return {
        "ugaritic": "Ugaritic Baal Cycle (KTU 1.1-1.6)",
        "linear_b": "Mycenaean Linear B (Pylos tablets)",
        "hebrew": "Old Hebrew (Gen-Prov, consonantal)",
        "indus_synthetic": "Indus Script (synthetic, Yadav 2010 / Fuls 2014)",
        "sumerian_ur3": "Sumerian Ur III (CDLI statistics)",
        "geez":      "Geez Genesis (Ethiopic syllabic, Dr. Fuls)",
        "nw_semitic": "NW Semitic Test1 (undeciphered, Dr. Fuls)",
    }.get(corpus_id, corpus_id)


def _load_corpus(corpus_id: str) -> dict | None:
    """Load a built-in corpus and return {content, corpus_type, metadata}."""
    try:
        if corpus_id == "ugaritic":
            import os
            import sys

            _tests = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests")
            if _tests not in sys.path:
                sys.path.insert(0, _tests)
            from corpora.ugaritic import get_undeciphered_corpus  # noqa: I001

            c = get_undeciphered_corpus()
            flat = c["flat_signs"]
            return {
                "corpus_type": "ancient",
                "content": flat,
                "metadata": {
                    "source": "KTU 1.1-1.6 Baal Cycle, encoded with opaque sign IDs",
                    "n_inscriptions": len(c["inscriptions"]),
                    "alphabet_size": c["alphabet_size"],
                    "note": "Ugaritic abjad — all signs are phonetic (SYL in ICIT terms)",
                },
            }

        elif corpus_id == "linear_b":
            from pathlib import Path

            from glossa_lab.data.linear_b_language import get_corpus_symbols

            flat = get_corpus_symbols()
            fixture = (
                Path(__file__).resolve().parent.parent
                / "tests"
                / "corpora"
                / "fixtures"
                / "linear_b.txt"
            )
            # Also store word-level inscriptions as metadata
            inscriptions: list[list[str]] = []
            if fixture.exists():
                for line in fixture.read_text(encoding="utf-8").splitlines():
                    for word in line.strip().split():
                        parts = word.replace("3", "").split("-")
                        signs = [
                            p.strip().lower()
                            for p in parts
                            if p.strip() and p.strip().replace("*", "").replace("2", "").isalpha()
                        ]
                        if len(signs) >= 2:
                            inscriptions.append(signs)
            return {
                "corpus_type": "ancient",
                "content": flat,
                "metadata": {
                    "source": "Pylos tablets (PY series), Ventris/Chadwick conventions",
                    "n_words": len(inscriptions),
                    "alphabet_size": len(set(flat)),
                    "writing_type": "syllabary",
                    "note": "Linear B — syllabary, ~87 signs, fully deciphered",
                },
            }

        elif corpus_id == "hebrew":
            from glossa_lab.data.old_hebrew import get_corpus_inscriptions, get_corpus_symbols

            flat = get_corpus_symbols()
            inscs = get_corpus_inscriptions()
            return {
                "corpus_type": "ancient",
                "content": flat,
                "metadata": {
                    "source": "Genesis, Psalms, Proverbs — consonantal Hebrew",
                    "n_inscriptions": len(inscs),
                    "alphabet_size": 22,
                    "writing_type": "abjad",
                    "note": "Old Hebrew — all 22 consonants are phonetic (abjad)",
                },
            }

        elif corpus_id == "indus_synthetic":
            from glossa_lab.data.indus_public_corpus import corpus_statistics, get_corpus_symbols

            flat = get_corpus_symbols()
            stats = corpus_statistics()
            return {
                "corpus_type": "ancient",
                "content": flat,
                "metadata": {
                    "source": "Synthetic — calibrated to Yadav 2010 (α=1.00, β=2.74) and Fuls 2014",
                    "n_inscriptions": stats["n_inscriptions"],
                    "distinct_signs": stats["distinct_signs"],
                    "writing_type": "logo-syllabic (undeciphered)",
                    "note": "Indus signs use Fuls (2014) 3-digit numbering 001-676",
                    "status": "SYNTHETIC — real statistics, generated sequences",
                },
            }

        elif corpus_id == "sumerian_ur3":
            from glossa_lab.data.sumerian_ur3 import corpus_statistics, get_corpus_symbols

            flat = get_corpus_symbols()
            stats = corpus_statistics()
            return {
                "corpus_type": "ancient",
                "content": flat,
                "metadata": {
                    "source": "CDLI Ur III statistics — cdli.earth, 83,741 real tablets",
                    "real_tokens": stats["real_cdli_stats"]["n_tokens"],
                    "real_signs": stats["real_cdli_stats"]["distinct_signs"],
                    "writing_type": "logo-syllabic (Tier 5 reference)",
                    "note": "Synthetic corpus calibrated to CDLI Ur III frequency data",
                },
            }

        elif corpus_id == "nw_semitic":
            from glossa_lab.data.nw_semitic import (
                corpus_statistics, get_corpus_inscriptions, get_corpus_symbols, FULS_ANCHORS
            )
            flat  = get_corpus_symbols()
            inscs = get_corpus_inscriptions()
            stats = corpus_statistics()
            return {
                "corpus_type": "ancient",
                "content": flat,
                "reading_direction": "rtl",
                "metadata": {
                    "source": "Provided by Dr. Andreas Fuls for collaborative decipherment",
                    "n_words":    stats["n_words"],
                    "distinct_signs": stats["n_distinct"],
                    "tokens_per_sign": stats["tokens_per_sign"],
                    "writing_type": "syllabic CV (undeciphered NW Semitic)",
                    "reading_direction": "rtl",
                    "provided_by": "Dr. Andreas Fuls",
                    "anchors": FULS_ANCHORS,
                    "note": (
                        "Reading direction: RIGHT-TO-LEFT (confirmed Apr 2026). "
                        "78 distinct signs, ~450 tokens. "
                        "Verified anchor signs: 004=T, 066=M, 208=N, 133=ayin, 128=L, 080=W."
                    ),
                    "inscriptions": inscs,   # word-level structure for RTL detection
                },
            }

        elif corpus_id == "geez":
            from glossa_lab.data.geez import (
                corpus_statistics, get_corpus_inscriptions, get_corpus_symbols
            )

            flat  = get_corpus_symbols()
            inscs = get_corpus_inscriptions()
            stats = corpus_statistics()
            return {
                "corpus_type": "ancient",
                "content": flat,
                "reading_direction": "ltr",
                "metadata": {
                    "source": "Book of Genesis in Ethiopic script (Tigrinya Bible)",
                    "n_words": stats["n_words"],
                    "distinct_signs": stats["inventory_size"],
                    "writing_type": "abugida-syllabic (fully deciphered)",
                    "reading_direction": "ltr",
                    "language": "Tigrinya / Geez",
                    "language_family": "Afro-Asiatic / Ethiosemitic",
                    "provided_by": "Dr. Andreas Fuls",
                    "note": (
                        "26 consonant rows x 7 vowel orders = ~200 syllabic signs. "
                        "Used as controlled syllabic benchmark for the "
                        "anchor-convergence validation experiment."
                    ),
                    "inscriptions": inscs,   # word-level structure for Ashraf detection
                },
            }

    except Exception as exc:
        log.warning("Could not load corpus %s: %s", corpus_id, exc)
    return None
