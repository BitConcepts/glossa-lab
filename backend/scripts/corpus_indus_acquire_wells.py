"""Indus Corpus — Wells Books Acquisition (STUB — PURCHASE REQUIRED).

STUB: Placeholder for when the Wells monographs are purchased.

Books to purchase:
  (1) Wells, Bryan K. (2015). Epigraphic Approaches to Indus Writing.
      Oxbow Books. ~£35 paperback.
  (2) Wells, Bryan K. (2015). The Archaeology and Epigraphy of Indus Writing.
      Archaeopress. ~£25 paperback / £16 personal PDF.
      https://www.archaeopress.com

These books provide:
  - Full Wells 676-sign catalog (3-digit codes) — needed to complete the
    Wells column in IndusSignCrosswalk (currently only 21/676 entries)
  - Methodology for sign-list reconstruction
  - Corpus logic not available elsewhere in open form

After purchase:
  1. Digitize/extract the Wells sign catalog (Table of signs with 3-digit codes)
  2. Build full Wells 676-sign list mapping in:
     backend/glossa_lab/data/indus_sign_crosswalk.py (_WELLS_FULS_EXTENSIONS)
  3. Run crosswalk rebuild:
     shell.cmd python backend/glossa_lab/data/indus_sign_crosswalk.py
  4. Re-run normalize + export to upgrade crosswalk coverage

_citation:
  primary_sources: ["A.7"]
  derivation: "Stub for Wells book acquisition. See CITATIONS.md A.7."
"""
from __future__ import annotations

import sys


def main() -> int:
    print("=" * 60)
    print("STUB: Wells books acquisition not yet implemented.")
    print()
    print("PURCHASE REQUIRED:")
    print("  Epigraphic Approaches (Oxbow):       £35 paperback")
    print("  Archaeology and Epigraphy (Archaeopress): £25 paperback / £16 PDF")
    print("  Recommended minimum:                 £51 (Archaeopress PDF + Oxbow)")
    print()
    print("Purchase URLs:")
    print("  https://www.oxbowbooks.com")
    print("  https://www.archaeopress.com")
    print()
    print("After purchase, extract Wells 676-sign catalog and update:")
    print("  backend/glossa_lab/data/indus_sign_crosswalk.py")
    print("  (_WELLS_FULS_EXTENSIONS dict — currently 21/676 entries)")
    print("=" * 60)
    return 1  # stub


if __name__ == "__main__":
    sys.exit(main())
