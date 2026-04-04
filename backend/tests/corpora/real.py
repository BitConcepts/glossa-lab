"""Real corpus loaders for academic study replication.

Loads fixture data from backend/tests/corpora/fixtures/.
"""

from __future__ import annotations

from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_indus() -> list[str]:
    """Load Indus script sign sequence (generated from published statistics)."""
    from tests.corpora.indus_corpus import generate_indus_flat

    return generate_indus_flat(seed=42)


def load_tamil() -> list[str]:
    """Load Tamil text as character sequence (transliterated, lowercase)."""
    text = (FIXTURES_DIR / "tamil.txt").read_text(encoding="utf-8")
    return [c.lower() for c in text if c.isalpha()]


def load_sanskrit() -> list[str]:
    """Load Sanskrit text as character sequence (transliterated, lowercase)."""
    text = (FIXTURES_DIR / "sanskrit.txt").read_text(encoding="utf-8")
    return [c.lower() for c in text if c.isalpha()]


def load_linear_b_signs() -> list[str]:
    """Load Linear B syllable-level tokens from the Pylos/Knossos fixture.

    Each token is one syllable (e.g. 'wa', 'na', 'ka' from wa-na-ka).
    Returns ~700-900 syllable tokens from the representative tablet corpus.
    """
    from glossa_lab.data.linear_b_language import get_corpus_symbols

    return get_corpus_symbols()


def load_linear_a_signs(seed: int = 42) -> list[str]:
    """Load Linear A sign tokens (GORILA codes) from the statistical corpus.

    Returns ~7,400 sign tokens following published sign-frequency
    distributions (Packard 1974, Younger 2000).
    """
    from tests.corpora.linear_a_corpus import generate_linear_a_flat

    return generate_linear_a_flat(seed=seed)


def load_sumerian() -> list[str]:
    """Load Sumerian text as character sequence (transliterated, lowercase).

    Corpus is based on Ur III administrative tablet transliterations.
    Characters are extracted alphabetically; numerals and hyphens discarded,
    consistent with the treatment applied to Tamil and Sanskrit fixtures.
    """
    text = (FIXTURES_DIR / "sumerian.txt").read_text(encoding="utf-8")
    return [c.lower() for c in text if c.isalpha()]


def load_english() -> list[str]:
    """Load English text as character sequence (lowercase, no whitespace)."""
    text = (FIXTURES_DIR / "english.txt").read_text(encoding="utf-8")
    # Keep only alphabetic chars, lowercase
    return [c.lower() for c in text if c.isalpha()]


def load_dna() -> list[str]:
    """Load DNA sequence as list of bases (A, C, G, T)."""
    text = (FIXTURES_DIR / "dna.txt").read_text(encoding="utf-8")
    return [c.upper() for c in text.strip() if c.upper() in "ACGT"]


# Fortran keywords — tokens NOT in this set are mapped to "ID"
_FORTRAN_KEYWORDS = {
    "PROGRAM",
    "END",
    "SUBROUTINE",
    "FUNCTION",
    "MODULE",
    "USE",
    "IMPLICIT",
    "NONE",
    "INTEGER",
    "REAL",
    "DOUBLE",
    "PRECISION",
    "CHARACTER",
    "LOGICAL",
    "COMPLEX",
    "PARAMETER",
    "DIMENSION",
    "INTENT",
    "IN",
    "OUT",
    "INOUT",
    "ALLOCATABLE",
    "SAVE",
    "DATA",
    "COMMON",
    "EQUIVALENCE",
    "EXTERNAL",
    "INTRINSIC",
    "IF",
    "THEN",
    "ELSE",
    "ELSEIF",
    "ENDIF",
    "DO",
    "WHILE",
    "ENDDO",
    "CONTINUE",
    "GOTO",
    "RETURN",
    "STOP",
    "EXIT",
    "CYCLE",
    "SELECT",
    "CASE",
    "DEFAULT",
    "ENDSELECT",
    "CALL",
    "WRITE",
    "READ",
    "PRINT",
    "OPEN",
    "CLOSE",
    "FORMAT",
    "RESULT",
    "CONTAINS",
    "RECURSIVE",
    "PURE",
    "ELEMENTAL",
    "ABS",
    "MOD",
    "MAX",
    "MIN",
    "SQRT",
    "SIN",
    "COS",
    "LOG",
    "NOT",
    "AND",
    "OR",
}


def load_fortran() -> list[str]:
    """Load Fortran source as token sequence (keywords + normalised IDs).

    Non-keyword identifiers are mapped to 'ID' to reduce vocabulary
    diversity, matching how formal languages behave at scale (keyword
    repetition dominates).
    """
    text = (FIXTURES_DIR / "fortran.txt").read_text(encoding="utf-8")
    tokens = []
    for line in text.splitlines():
        # Strip comments
        line = line.split("!")[0]
        for word in line.split():
            cleaned = "".join(c for c in word if c.isalnum() or c == "_")
            if cleaned:
                upper = cleaned.upper()
                tokens.append(upper if upper in _FORTRAN_KEYWORDS else "ID")
    return tokens
